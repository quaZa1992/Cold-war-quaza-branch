# IMPERIA CW — Cold War: Japan staged reference checker.
"""Read-only consistency checks for staged Japan content and active JAP files.

This checker is deliberately not a game parser. It catches common unresolved
references, brace/encoding mistakes, duplicate localization/event keys, and
custom interface icon references. Missing references are reported as
INCOMPLETE because staged fragments may intentionally await integration.

Run from any directory with Python 3:
    python tools/japan_1970/check_staged_refs.py
The script only reads files and prints findings; it never rewrites project data.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
STAGING = Path(__file__).resolve().parent / "staging"
FOREIGN = STAGING / "foreign"

SCRIPT_SUFFIXES = {".txt", ".gfx", ".gui"}
LOC_SUFFIXES = {".yml", ".yaml"}


def unique_paths(paths):
    return sorted({path.resolve() for path in paths if path.is_file()})


def candidate_files():
    staged = [p for p in STAGING.rglob("*") if p.suffix.lower() in SCRIPT_SUFFIXES | LOC_SUFFIXES]
    active = []
    active_dirs = [
        ROOT / "common" / "scripted_effects",
        ROOT / "common" / "scripted_triggers",
        ROOT / "common" / "dynamic_modifiers",
        ROOT / "common" / "ideas",
        ROOT / "common" / "decisions",
        ROOT / "common" / "opinion_modifiers",
        ROOT / "events",
        ROOT / "history" / "countries",
        ROOT / "interface",
        ROOT / "localisation" / "english",
    ]
    for directory in active_dirs:
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            name = path.name.casefold()
            # Include Japan custom files and the native definitions needed to
            # resolve their idea/modifier/icon references.
            japan_custom = (
                ("coldwar_jap" in name or name.startswith("jap ") or name.startswith("jap_"))
                and name != "jap_political_leaders.txt"
            )
            idea_defs = directory == ROOT / "common" / "ideas" and path.suffix.lower() == ".txt"
            modifier_defs = directory == ROOT / "common" / "dynamic_modifiers" and path.suffix.lower() == ".txt"
            opinion_defs = directory == ROOT / "common" / "opinion_modifiers" and path.suffix.lower() == ".txt"
            if path.suffix.lower() in SCRIPT_SUFFIXES | LOC_SUFFIXES and (
                japan_custom or idea_defs or modifier_defs or opinion_defs
            ):
                active.append(path)
    return unique_paths(staged), unique_paths(active)


def read_text(path):
    # utf-8-sig accepts both required BOM and no-BOM files for inspection.
    return path.read_text(encoding="utf-8-sig")


def rel(path):
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def brace_issues(text):
    """Return simple brace/quote imbalance diagnostics, ignoring comments."""
    depth = 0
    quote = False
    escaped = False
    line = 1
    opens = []
    errors = []
    for char in text:
        if char == "\n":
            line += 1
            if not quote:
                # Comment state ends at newline; comments are handled below by
                # replacing them before this scanner.
                pass
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "{":
            depth += 1
            opens.append(line)
        elif char == "}":
            depth -= 1
            if depth < 0:
                errors.append(f"extra closing brace at line {line}")
                depth = 0
            elif opens:
                opens.pop()
    if quote:
        errors.append("unterminated quoted string")
    if depth:
        errors.append(f"{depth} unclosed brace(s), opened at line(s) {opens[-5:]}")
    return errors


def strip_comments(text):
    """Remove # comments outside strings while preserving line positions."""
    output = []
    for line in text.splitlines(keepends=True):
        quote = False
        escaped = False
        cut = len(line)
        for index, char in enumerate(line):
            if quote:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quote = False
            elif char == '"':
                quote = True
            elif char == "#":
                cut = index
                break
        output.append(line[:cut])
    return "".join(output)


def line_matches(paths, pattern):
    compiled = re.compile(pattern)
    for path in paths:
        try:
            text = read_text(path)
        except (UnicodeDecodeError, OSError):
            continue
        for match in compiled.finditer(text):
            yield path, text.count("\n", 0, match.start()) + 1, match


def check_encoding(staged, active, add):
    checked = 0
    japan_active = [p for p in active if p.name.casefold() != "jap_political_leaders.txt" and (
        "coldwar_jap" in p.name.casefold()
        or p.name.casefold().startswith("jap ")
        or p.name.casefold().startswith("jap_")
    )]
    for path in unique_paths(staged + japan_active):
        suffix = path.suffix.lower()
        if suffix not in SCRIPT_SUFFIXES | LOC_SUFFIXES:
            continue
        checked += 1
        raw = path.read_bytes()
        has_bom = raw.startswith(b"\xef\xbb\xbf")
        if suffix in SCRIPT_SUFFIXES and has_bom:
            add("ERROR", "encoding", path, 1, "script-like file has UTF-8 BOM")
        elif suffix in LOC_SUFFIXES and not has_bom:
            add("ERROR", "encoding", path, 1, "localization file lacks required UTF-8 BOM")
        try:
            raw.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            add("ERROR", "encoding", path, 1, f"not valid UTF-8: {error}")
    return checked


def check_braces(staged, active, add):
    checked = 0
    japan_active = [p for p in active if p.name.casefold() != "jap_political_leaders.txt" and (
        "coldwar_jap" in p.name.casefold()
        or p.name.casefold().startswith("jap ")
        or p.name.casefold().startswith("jap_")
    )]
    for path in unique_paths(staged + japan_active):
        if path.suffix.lower() not in SCRIPT_SUFFIXES:
            continue
        checked += 1
        try:
            text = strip_comments(read_text(path))
        except (UnicodeDecodeError, OSError) as error:
            add("ERROR", "braces", path, 1, f"cannot read: {error}")
            continue
        for issue in brace_issues(text):
            add("ERROR", "braces", path, 1, issue)
    return checked


def check_localization(staged, active, add):
    files = [p for p in unique_paths(staged + active) if p.suffix.lower() in LOC_SUFFIXES]
    keys = defaultdict(list)
    key_re = re.compile(r"(?m)^\s*([A-Za-z0-9_.-]+):(?:\d+)?\s*(.*)$")
    for path in files:
        try:
            text = read_text(path)
        except (UnicodeDecodeError, OSError):
            continue
        for match in key_re.finditer(text):
            key = match.group(1)
            if key.casefold() == "l_english":
                continue
            line = text.count("\n", 0, match.start()) + 1
            # Values are compared after trimming; duplicate values are still
            # reported, but marked same-value versus conflicting-value.
            value = match.group(2).strip()
            keys[key].append((path, line, value))
    for key, rows in sorted(keys.items()):
        if len(rows) < 2:
            continue
        values = {row[2] for row in rows}
        kind = "conflicting duplicate localization key" if len(values) > 1 else "duplicate localization key"
        details = "; ".join(f"{rel(path)}:{line}" for path, line, _ in rows)
        add("REVIEW", "localization", rows[-1][0], rows[-1][1], f"{kind} {key}: {details}")
    return len(files)


def check_events(staged, active, add):
    # Only staged and JAP-authored active scripts are event candidates. Native
    # unrelated events can be referenced by staged effects, but are outside
    # this checker’s local duplicate/reference audit.
    scripts = [p for p in unique_paths(staged + active) if p.suffix.lower() in SCRIPT_SUFFIXES and (
        p in staged or "coldwar_jap" in p.name.casefold()
        or p.name.casefold().startswith(("jap ", "jap_"))
    )]
    definitions = defaultdict(list)
    references = defaultdict(list)
    id_re = re.compile(r"\bid\s*=\s*([A-Za-z0-9_]+\.\d+)")
    ref_re = re.compile(r"\bcountry_event\s*=\s*\{\s*id\s*=\s*([A-Za-z0-9_]+\.\d+)")
    for path in scripts:
        text = strip_comments(read_text(path))
        # A definition block has an event ID and title/desc/is_triggered_only;
        # inline `country_event = { id = ... }` blocks are references.
        for block in re.finditer(r"\bcountry_event\s*=\s*\{", text):
            start = block.end()
            depth = 1
            quote = False
            escaped = False
            end = start
            while end < len(text) and depth:
                char = text[end]
                if quote:
                    if escaped:
                        escaped = False
                    elif char == "\\":
                        escaped = True
                    elif char == '"':
                        quote = False
                elif char == '"':
                    quote = True
                elif char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                end += 1
            body = text[start:end]
            if not re.search(r"\b(?:title|desc|is_triggered_only)\s*=", body):
                continue
            match = id_re.search(body)
            if match:
                definitions[match.group(1)].append((path, text.count("\n", 0, block.start()) + 1))
        for match in ref_re.finditer(text):
            references[match.group(1)].append((path, text.count("\n", 0, match.start()) + 1))
    for event_id, rows in sorted(definitions.items()):
        if len(rows) > 1:
            details = "; ".join(f"{rel(path)}:{line}" for path, line in rows)
            add("ERROR", "events", rows[-1][0], rows[-1][1], f"duplicate event id {event_id}: {details}")
    for event_id, rows in sorted(references.items()):
        if event_id not in definitions:
            path, line = rows[0]
            add("INCOMPLETE", "events", path, line, f"event reference {event_id} has no definition in active/staged candidates")


def extract_top_level_ids(paths):
    ids = defaultdict(list)
    pattern = re.compile(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_.-]*)\s*=\s*\{")
    for path in paths:
        try:
            text = strip_comments(read_text(path))
        except (UnicodeDecodeError, OSError):
            continue
        for match in pattern.finditer(text):
            # Top-level-ish declaration: exclude deeply indented lines. A
            # single tab/space level is allowed for nested idea definitions.
            indent = len(match.group(0)) - len(match.group(0).lstrip(" \t"))
            if indent <= 8:
                ids[match.group(1)].append((path, text.count("\n", 0, match.start()) + 1))
    return ids


def check_scripted_helpers(staged, active, add):
    helper_files = [p for p in unique_paths(staged + active) if p.suffix.lower() == ".txt" and (
        "scripted_effects" in p.parts or "scripted_triggers" in p.parts
        or p.parent == STAGING / "constitution"
        or p.name.endswith("effects.txt")
    )]
    providers = extract_top_level_ids(helper_files)
    graphs = [p for p in staged if p.name == "focus_tree.txt"]
    call_re = re.compile(r"\b(COLDWAR_JAP(?:70)?_[A-Za-z0-9_]+_(?:apply|effect|offer|init|confirm|abolish|support_\d+))\s*=\s*yes\b")
    for path, line, match in line_matches(graphs, call_re.pattern):
        helper = match.group(1)
        if helper not in providers:
            add("INCOMPLETE", "helpers", path, line, f"staged focus calls {helper}, no active/staged provider found")
    return len(providers)


def check_modifier_idea_refs(staged, active, add):
    all_scripts = [p for p in unique_paths(staged + active) if p.suffix.lower() in SCRIPT_SUFFIXES]
    dynamic_dirs = [ROOT / "common" / "dynamic_modifiers"]
    idea_dirs = [ROOT / "common" / "ideas"]
    opinion_dirs = [ROOT / "common" / "opinion_modifiers"]
    definition_files = list(staged)
    for directory in dynamic_dirs + idea_dirs + opinion_dirs:
        if directory.exists():
            definition_files.extend(directory.rglob("*.txt"))
    definitions = extract_top_level_ids(unique_paths(definition_files))

    dynamic_refs = defaultdict(list)
    opinion_refs = defaultdict(list)
    idea_refs = defaultdict(list)
    patterns = {
        "dynamic": re.compile(r"(?:add_dynamic_modifier|has_dynamic_modifier)\s*=\s*\{[^}]*?modifier\s*=\s*([A-Za-z_][A-Za-z0-9_.-]*)", re.S),
        "opinion": re.compile(r"add_opinion_modifier\s*=\s*\{[^}]*?modifier\s*=\s*([A-Za-z_][A-Za-z0-9_.-]*)", re.S),
        "ideas": re.compile(r"(?:add_timed_idea|add_ideas|remove_ideas|has_idea)\s*=\s*(?:\{\s*idea\s*=\s*)?([A-Za-z_][A-Za-z0-9_.-]*)", re.S),
    }
    target_map = {"dynamic": dynamic_refs, "opinion": opinion_refs, "ideas": idea_refs}
    for path in all_scripts:
        text = strip_comments(read_text(path))
        for kind, pattern in patterns.items():
            for match in pattern.finditer(text):
                ident = match.group(1)
                line = text.count("\n", 0, match.start()) + 1
                target_map[kind][ident].append((path, line))

    known_ids = set(definitions)
    for kind, refs in (("dynamic modifier", dynamic_refs), ("opinion modifier", opinion_refs), ("idea", idea_refs)):
        for ident, rows in sorted(refs.items()):
            if ident not in known_ids:
                path, line = rows[0]
                add("INCOMPLETE", "definitions", path, line, f"{kind} reference {ident} has no definition in active/staged candidates")


def check_custom_icons(staged, active, add):
    interface_files = [p for p in ROOT.joinpath("interface").rglob("*.gfx") if p.is_file()]
    declared = set()
    decl_re = re.compile(r"\bname\s*=\s*\"(GFX_[A-Za-z0-9_]+)\"")
    for path in interface_files:
        try:
            declared.update(decl_re.findall(strip_comments(read_text(path))))
        except (UnicodeDecodeError, OSError):
            continue
    candidates = [p for p in unique_paths(staged + active) if p.suffix.lower() in SCRIPT_SUFFIXES and (
        p in staged or "coldwar_jap" in p.name.casefold()
        or p.name.casefold().startswith(("jap ", "jap_"))
    )]
    gfx_ref_re = re.compile(r"\b(?:icon|picture)\s*=\s*(GFX_[A-Za-z0-9_]+)")
    idea_picture_re = re.compile(r"\bpicture\s*=\s*((?:JAP|IMP|COLDWAR)[A-Za-z0-9_]+)")
    checked = set()

    def validate(path, line, icon):
        checked.add(icon)
        if icon not in declared:
            add("INCOMPLETE", "icons", path, line, f"custom icon {icon} is not declared in interface/*.gfx")

    for path, line, match in line_matches(candidates, gfx_ref_re.pattern):
        icon = match.group(1)
        if icon.startswith(("GFX_COLDWAR", "GFX_JAP", "GFX_IMP")):
            validate(path, line, icon)
    for path, line, match in line_matches(candidates, idea_picture_re.pattern):
        # Country idea picture IDs omit the GFX_idea_ namespace in script.
        validate(path, line, "GFX_idea_" + match.group(1))
    return len(checked)


def main():
    staged, active = candidate_files()
    findings = []

    def add(level, category, path, line, message):
        findings.append((level, category, path, line, message))

    n_encoding = check_encoding(staged, active, add)
    n_braces = check_braces(staged, active, add)
    n_loc = check_localization(staged, active, add)
    check_events(staged, active, add)
    n_helpers = check_scripted_helpers(staged, active, add)
    check_modifier_idea_refs(staged, active, add)
    n_icons = check_custom_icons(staged, active, add)

    print("Japan staged-reference audit (read-only; not an engine parser)")
    print(f"Candidates: {len(staged)} staged files, {len(active)} active/native reference files")
    print(f"Scanned: {n_encoding} encoding files, {n_braces} script-like files, {n_loc} localization files, {n_helpers} helper providers, {n_icons} custom icon IDs")
    if findings:
        for level, category, path, line, message in findings:
            print(f"{level} [{category}] {rel(path)}:{line}: {message}")
    else:
        print("No findings in scanned candidates.")
    errors = sum(level == "ERROR" for level, *_ in findings)
    incomplete = sum(level == "INCOMPLETE" for level, *_ in findings)
    reviews = sum(level == "REVIEW" for level, *_ in findings)
    print(f"Summary: {errors} errors, {incomplete} incomplete references, {reviews} review findings")
    # Incomplete references are expected for fragments awaiting integration;
    # only definite local format/duplicate-event errors give a failing exit.
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
