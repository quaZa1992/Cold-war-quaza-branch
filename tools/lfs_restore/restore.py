# IMPERIA COLD WAR — Restore exact Git LFS runtime assets in ZIP installations.
"""Download only LFS placeholders; preserve existing assets and gameplay files."""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
from http.client import HTTPException, HTTPSConnection
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import ssl
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[2]
REPOSITORY = "https://github.com/Imperia-MD/mdcoldwar"
ENDPOINT = REPOSITORY + ".git/info/lfs/objects/batch"
POINTER = re.compile(
    rb"version https://git-lfs.github.com/spec/v1\r?\n"
    rb"oid sha256:([0-9a-f]{64})\r?\nsize ([0-9]+)\r?\n?"
)
EXCLUDED = {".git", ".claude", "Claude outputs", "docs", "tools", "node_modules", "__pycache__"}
SOURCE_EXTENSIONS = {".zip", ".psd", ".xcf", ".pdn", ".xlsx", ".blend"}
REPORT = Path(__file__).with_name("restoration.json")
LOCAL = threading.local()


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        redirected = super().redirect_request(request, fp, code, message, headers, new_url)
        if redirected and urlsplit(request.full_url).netloc != urlsplit(new_url).netloc:
            redirected.remove_header("Authorization")
            redirected.remove_header("Proxy-Authorization")
        return redirected


def download_connection(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https":
        raise RuntimeError("LFS download requires HTTPS")
    if not hasattr(LOCAL, "connections"):
        LOCAL.connections = {}
        LOCAL.tls = ssl.create_default_context()
    key = parsed.netloc
    if key not in LOCAL.connections:
        LOCAL.connections[key] = HTTPSConnection(parsed.hostname, port=parsed.port,
                                                timeout=60, context=LOCAL.tls)
    return LOCAL.connections[key], parsed.path + ("?" + parsed.query if parsed.query else "")


def scan():
    records = []
    skipped_reparse = 0
    stack = [ROOT]
    visited = 0
    last_log = time.monotonic()
    while stack:
        with os.scandir(stack.pop()) as entries:
            for entry in entries:
                if entry.name in EXCLUDED:
                    continue
                if entry.is_dir(follow_symlinks=False):
                    if entry.stat(follow_symlinks=False).st_file_attributes & 0x400:
                        skipped_reparse += 1
                    else:
                        stack.append(Path(entry.path))
                    continue
                if not entry.is_file(follow_symlinks=False):
                    continue
                path = Path(entry.path)
                if path.suffix.lower() in SOURCE_EXTENSIONS:
                    continue
                stat = entry.stat(follow_symlinks=False)
                if stat.st_file_attributes & 0x400:
                    skipped_reparse += 1
                    continue
                visited += 1
                if stat.st_size <= 1024:
                    match = POINTER.fullmatch(path.read_bytes())
                    if match:
                        records.append({"path": path.relative_to(ROOT).as_posix(),
                                        "oid": match[1].decode(), "size": int(match[2])})
                if time.monotonic() - last_log > 15:
                    print(f"Scan: {visited:,} files; {len(records):,} LFS placeholders", flush=True)
                    last_log = time.monotonic()
    return records, skipped_reparse


def authorization(git):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    result = subprocess.run([git, "credential", "fill"],
                            input="protocol=https\nhost=github.com\n\n",
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env=env, check=True)
    credentials = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    token = base64.b64encode((credentials["username"] + ":" + credentials["password"]).encode()).decode()
    return "Basic " + token


def batch(objects, auth):
    headers = {"Accept": "application/vnd.git-lfs+json",
               "Content-Type": "application/vnd.git-lfs+json",
               "Authorization": auth,
               "User-Agent": "IMPERIA-COLD-WAR-LFS-Restore/1.0"}
    payload = {"operation": "download", "transfers": ["basic"],
               "objects": [{"oid": oid, "size": rows[0]["size"]} for oid, rows in objects]}
    for attempt in range(4):
        try:
            request = Request(ENDPOINT, data=json.dumps(payload).encode(), headers=headers)
            with build_opener(SafeRedirect()).open(request, timeout=60) as response:
                return json.load(response)["objects"]
        except HTTPError as error:
            if error.code in (401, 403):
                raise RuntimeError(f"LFS authorization refused: HTTP {error.code}") from None
            if attempt == 3:
                raise RuntimeError(f"LFS batch request failed: HTTP {error.code}") from None
            time.sleep(2 ** attempt)
        except (URLError, ValueError, TimeoutError, OSError, HTTPException):
            if attempt == 3:
                raise RuntimeError("LFS batch request failed after four attempts") from None
            time.sleep(2 ** attempt)


def restore_object(obj, rows):
    if "error" in obj:
        raise RuntimeError(f"LFS object unavailable: {obj['error'].get('code', 'unknown')}")
    action = obj.get("actions", {}).get("download")
    if not action:
        raise RuntimeError("LFS server returned no download action")
    first = ROOT / rows[0]["path"]
    part = first.with_name(first.name + ".imperia-lfs-part")
    connection, request_path = download_connection(action["href"])
    try:
        for attempt in range(4):
            try:
                digest = hashlib.sha256()
                size = 0
                connection.request("GET", request_path, headers=action.get("header", {}))
                with connection.getresponse() as response:
                    if response.status != 200:
                        raise RuntimeError(f"Object endpoint returned HTTP {response.status}")
                    with part.open("wb") as output:
                        while chunk := response.read(1024 * 1024):
                            output.write(chunk)
                            digest.update(chunk)
                            size += len(chunk)
                if size != rows[0]["size"] or digest.hexdigest() != rows[0]["oid"]:
                    raise RuntimeError("Downloaded object failed its SHA-256 or size check")
                break
            except (URLError, TimeoutError, OSError, RuntimeError, HTTPException):
                connection.close()
                if attempt == 3:
                    raise RuntimeError("Object download or checksum failed after four attempts") from None
                time.sleep(2 ** attempt)
        for row in rows:
            target = ROOT / row["path"]
            current = POINTER.fullmatch(target.read_bytes())
            if not current or current[1].decode() != row["oid"] or int(current[2]) != row["size"]:
                raise RuntimeError("Target changed since scan; preserved current file")
            if target == first:
                continue
            copy = target.with_name(target.name + ".imperia-lfs-part")
            try:
                shutil.copyfile(part, copy)
                copy.replace(target)
            finally:
                copy.unlink(missing_ok=True)
        part.replace(first)
        return len(rows), rows[0]["size"]
    finally:
        part.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--restore", action="store_true")
    parser.add_argument("--git", default="git")
    parser.add_argument("--workers", type=int, default=48)
    args = parser.parse_args()
    records, skipped = scan()
    grouped = defaultdict(list)
    for row in records:
        grouped[row["oid"]].append(row)
    total_bytes = sum(rows[0]["size"] for rows in grouped.values())
    print(json.dumps({"placeholders": len(records), "unique_objects": len(grouped),
                      "download_bytes": total_bytes, "groups": dict(Counter(row["path"].split('/')[0] for row in records)),
                      "skipped_reparse_points": skipped}), flush=True)
    if not args.restore:
        return
    required_space = sum(row["size"] for row in records)
    if shutil.disk_usage(ROOT).free < required_space + 1024 ** 3:
        raise RuntimeError("Insufficient free disk space for runtime assets")
    report = {"project": "IMPERIA COLD WAR", "source": REPOSITORY,
              "started_utc": datetime.now(timezone.utc).isoformat(), "initial_placeholders": len(records),
              "unique_objects": len(grouped), "expected_download_bytes": total_bytes,
              "restored_files": 0, "verified_download_bytes": 0, "failures": [],
              "verification": "Every downloaded object must match its original LFS SHA-256 and byte size.",
              "scope": "Runtime LFS placeholders; development records and source archives excluded.",
              "skipped_reparse_points": skipped}
    auth = authorization(args.git) if records else None
    objects = list(grouped.items())
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for offset in range(0, len(objects), 100):
            chunk = objects[offset:offset + 100]
            responses = batch(chunk, auth)
            futures = {pool.submit(restore_object, obj, grouped[obj["oid"]]): obj["oid"] for obj in responses}
            for future in as_completed(futures):
                oid = futures[future]
                try:
                    count, size = future.result()
                    report["restored_files"] += count
                    report["verified_download_bytes"] += size
                except Exception as error:
                    report["failures"].append({"oid": oid, "paths": [row["path"] for row in grouped[oid]],
                                               "error": type(error).__name__ + ": " + str(error)})
            REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(f"Restored {report['restored_files']:,}/{len(records):,} files; "
                  f"{report['verified_download_bytes'] / 1024**3:.2f} GiB verified; "
                  f"{len(report['failures'])} failed objects", flush=True)
    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["remaining_placeholders"] = len(scan()[0])
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)
    if report["remaining_placeholders"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
