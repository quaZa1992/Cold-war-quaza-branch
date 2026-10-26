# IMPERIA CW — Cold War: Syria 1970 content imported from quaZa.
"""Read-only calibrated source attribution for the two supplied crash dumps.

No private symbols are available. Field meanings are inferred from multiple
independent source matches, and uncaptured strings are never reconstructed as
though their bytes were present in the dump. Run from the mod root.
"""
from pathlib import Path
import json
import re
import struct
import argparse

from inspect_repeat_dump import ROOT, parse

VF = 0x7FF7FC72B710
MOD_ROOT = Path(__file__).resolve().parents[2]
DEFINITION = re.compile(r"^([A-Za-z_0-9]+)\s*=\s*\{")


def definitions():
    result = {}
    # Match the observed source inventory's ordinal filename order explicitly.
    # Sorting Windows Path objects casefolds and places COL_political_leaders
    # before COLDWAR_*, shifting this group while leaving CSB/DAG unchanged.
    files = sorted((MOD_ROOT / "common/scripted_effects").glob("*.txt"), key=lambda path: path.name)
    for path in files:
        for line, text in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1):
            match = DEFINITION.match(text)
            if match:
                name = match.group(1)
                result.setdefault((line, len(name)), []).append({
                    "file": path.name, "line": line, "name": name,
                })
    return result, files


def inspect(name, sources, source_files):
    parsed = parse(name)
    raw = (ROOT / name / "minidump.dmp").read_bytes()
    memory = []
    for kind, (_, rva) in parsed["streams"].items():
        if kind == 5:
            count = struct.unpack_from("<I", raw, rva)[0]
            memory.extend(struct.unpack_from("<QII", raw, rva + 4 + i * 16) for i in range(count))
        elif kind == 9:
            count, data_rva = struct.unpack_from("<QQ", raw, rva)
            for i in range(count):
                address, size = struct.unpack_from("<QQ", raw, rva + 16 + i * 16)
                memory.append((address, size, data_rva))
                data_rva += size

    def read(address, size):
        for start, length, rva in memory:
            if start <= address and address + size <= start + length:
                return raw[rva + address - start:rva + address - start + size]
        return None

    templates = []
    literal_syria_identifiers = []
    for start, size, rva in memory:
        block = raw[rva:rva + size]
        literal_syria_identifiers.extend(m.group().decode() for m in re.finditer(rb"COLDWAR_SYR_[A-Za-z_0-9.]+", block))
        for match in re.finditer(re.escape(struct.pack("<Q", VF)), block):
            address = start + match.start()
            obj = read(address, 128)
            if obj is None:
                continue
            # These offsets are calibrated using known short inline names and
            # several neighboring source declarations; they are not symbols.
            source_id, source_line = struct.unpack_from("<II", obj, 0x2C)
            length, capacity = struct.unpack_from("<QQ", obj, 0x70)
            if length > 512 or capacity < length:
                continue
            pointer = struct.unpack_from("<Q", obj, 0x60)[0]
            name_bytes = obj[0x60:0x60 + length] if capacity <= 15 else read(pointer, length)
            captured_name = name_bytes.decode("ascii", errors="replace") if name_bytes is not None else None
            candidates = sources.get((source_line, length), [])
            if captured_name:
                candidates = [candidate for candidate in candidates if candidate["name"] == captured_name]
            templates.append({
                "address": hex(address),
                "is_r12": address == int(parsed["registers"]["R12"], 16),
                "source_id_field_0x2c": source_id,
                "source_line_field_0x30": source_line,
                "name_length_field_0x70": length,
                "name_capacity_field_0x78": capacity,
                "captured_name": captured_name,
                "candidate_definitions": candidates,
            })

    groups = {}
    for obj in templates:
        key = obj["source_id_field_0x2c"]
        files = {candidate["file"] for candidate in obj["candidate_definitions"]}
        groups[key] = files if key not in groups else groups[key] & files
    file_indices = {path.name: i for i, path in enumerate(source_files)}
    calibrations = []
    for obj in templates:
        if obj["captured_name"] and len(obj["candidate_definitions"]) == 1:
            source_file = obj["candidate_definitions"][0]["file"]
            index = file_indices[source_file]
            calibrations.append({
                "captured_name": obj["captured_name"],
                "file": source_file,
                "file_index": index,
                "source_id": obj["source_id_field_0x2c"],
                "source_id_minus_file_index": obj["source_id_field_0x2c"] - index,
            })
    offsets = {item["source_id_minus_file_index"] for item in calibrations}
    offset = next(iter(offsets)) if len(offsets) == 1 else None
    contradictions = []
    if offset is not None:
        for obj in templates:
            index = obj["source_id_field_0x2c"] - offset
            if 0 <= index < len(source_files):
                source_file = source_files[index].name
                obj["calibrated_file_index"] = index
                obj["calibrated_source_file"] = source_file
                matches = [candidate for candidate in obj["candidate_definitions"] if candidate["file"] == source_file]
                obj["calibrated_declaration"] = matches[0] if len(matches) == 1 else None
                if obj["candidate_definitions"] and not obj["calibrated_declaration"]:
                    contradictions.append({"address": obj["address"], "mapped_file": source_file})
    if contradictions:
        raise RuntimeError(f"Source ordering contradicts captured declaration metadata in {name}: {contradictions}")
    return {
        "name": name,
        "source_file_order": "case-sensitive ordinal Path.name",
        "literal_syria_identifiers": sorted(set(literal_syria_identifiers)),
        "literal_name_calibrations": calibrations,
        "calibrated_source_id_offset": offset,
        "validated_declaration_count": sum(bool(obj.get("calibrated_declaration")) for obj in templates),
        "unmatched_current_declaration_count": sum(not obj.get("calibrated_declaration") for obj in templates),
        "source_group_consistent_files": {str(key): sorted(value) for key, value in sorted(groups.items())},
        "templates": templates,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_definitions, source_files = definitions()
    result = [
        inspect(name, source_definitions, source_files)
        for name in ("hoi4_20261019_100834", "hoi4_20261019_103748")
    ]
    encoded = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
        print(f"Wrote {args.output}: {sum(len(item['templates']) for item in result)} captured templates")
    else:
        print(encoded, end="")
