# IMPERIA CW — Cold War: Syria 1970 content imported from quaZa.
"""Retire the user-authorized Syria 2000 programme without breaking other trees.

Only the explicit file allowlist is removed. Originals and the incoming-reference
inventory live under tools/ (outside HOI4's content loader). Shared definitions
actually consumed by foreign countries are transplanted unchanged, not stubbed.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil

from politics import closing_brace, write

FILES = [
    "common/national_focus/05_syria.txt",
    "common/ideas/Syrian.txt",
    "common/decisions/Syria.txt",
    "common/decisions/categories/99_SYR_decision_categories.txt",
    "common/on_actions/99_SYR_on_actions.txt",
    "events/Syria.txt",
    "common/scripted_effects/99_SYR_scripted_effects.txt",
    "common/scripted_effects/SYR_political_leaders.txt",
    "common/scripted_triggers/99_SYR_scripted_triggers.txt",
    "common/dynamic_modifiers/99_SYR_dynamic_modifiers.txt",
    "common/factions/templates/99_SYR.txt",
    "common/ai_strategy/SYR.txt",
    "common/ai_strategy_plans/SYR_strategy_plans.txt",
    "common/bop/SYR.txt",
    "common/characters/SYR.txt",
    "common/opinion_modifiers/Syria.txt",
    "history/units/SYR_2000_nsb.txt",
    "history/units/SYR_2000_nonnsb.txt",
    "history/units/SYR_2000_nonbba.txt",
    "history/units/SYR_2000_naval_mtg.txt",
    "history/units/SYR_2000_bba.txt",
    "history/units/SYR_SSNP_2000_units.txt",
]
HISTORY = "history/countries/SYR - Syria.txt"
HEADER = "# COLDWAR_SYR | Foreign/shared contracts formerly stored in the retired Syria 2000 files.\n# No modern Syrian tree, succession or political programme is loaded here.\n"


def blocks(text):
    end = -1
    for match in re.finditer(r"(?m)^\s*([A-Za-z_]\w*)\s*=\s*\{", text):
        if match.start() < end:
            continue
        end = closing_brace(text, text.index("{", match.start())) + 1
        yield match.group(1), text[match.start():end].strip()


def children(block):
    return blocks(block[block.index("{") + 1:-1])


def definitions(relative, text):
    result = {}
    kind = Path(relative).parent.name
    if relative == "common/national_focus/05_syria.txt":
        for key, block in blocks(text):
            candidates = children(block) if key == "focus_tree" else [(key, block)]
            for child, source in candidates:
                if child in ("focus", "shared_focus"):
                    match = re.search(r"\bid\s*=\s*(\w+)", source)
                    if match:
                        result[match.group(1)] = ("focus", source)
    elif relative == "common/ideas/Syrian.txt":
        for key, block in blocks(text):
            for child, source in children(block):
                if child == "country":
                    for id_, idea in children(source):
                        result[id_] = ("idea", idea)
    elif relative == "events/Syria.txt":
        for key, block in blocks(text):
            if key in ("country_event", "news_event"):
                match = re.search(r"\bid\s*=\s*([\w.]+)", block)
                if match:
                    result[match.group(1)] = ("event", block)
    elif kind in ("scripted_effects", "scripted_triggers", "dynamic_modifiers", "templates"):
        for id_, block in blocks(text):
            result[id_] = (kind, block)
    elif kind == "opinion_modifiers":
        for key, block in blocks(text):
            for id_, source in children(block):
                result[id_] = ("opinion", source)
    elif kind == "characters":
        for key, block in blocks(text):
            for id_, source in children(block):
                result[id_] = ("character", source)
    return result


def tokens(text):
    # Comments/localised strings do not constitute executable incoming references.
    clean = re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*', "", text)
    return set(re.findall(r"\b[A-Za-z_]\w*(?:\.\d+)?\b", clean))


def backup(root, relative):
    source = root / relative
    destination = root / "tools/syria_1970/retired_modern" / relative
    if source.is_file() and not destination.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return destination


def install(root):
    root = Path(root).resolve()
    report_path = root / "tools/syria_1970/retirement_report.json"
    # This is a migration, not a generator that regenerates foreign files from
    # stale backups on every build. Idempotent subsequent runs retain the report.
    if not any((root / name).is_file() for name in FILES):
        return json.loads(report_path.read_text(encoding="utf-8")) if report_path.is_file() else {}
    registry, sources, hashes = {}, {}, {}
    for relative in FILES:
        path = root / relative
        if not path.is_file():
            continue
        original = path.read_text(encoding="utf-8-sig")
        sources[relative] = original
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        registry.update(definitions(relative, original))
        backup(root, relative)

    # Inventory before touching anything. The report provides exact foreign
    # locations, IDs and their definition category, including old focus reads.
    incoming = {}
    texts = {}
    for folder in ("common", "events", "history"):
        for path in (root / folder).rglob("*.txt"):
            relative = path.relative_to(root).as_posix()
            if relative in FILES or relative == HISTORY or path.name.startswith("COLDWAR_SYR_shared_legacy"):
                continue
            text = path.read_text(encoding="utf-8-sig")
            hits = tokens(text) & registry.keys()
            if hits:
                incoming[relative] = sorted(hits)
                texts[relative] = text

    # Existing shared definitions elsewhere win: the legacy Syrian idea file
    # itself contains some duplicate generic/Arab definitions.
    existing_ideas = set()
    for path in (root / "common/ideas").glob("*.txt"):
        if path.name == "Syrian.txt":
            continue
        for key, block in blocks(path.read_text(encoding="utf-8-sig")):
            if key != "ideas":
                continue
            for child, source in children(block):
                if child == "country":
                    existing_ideas.update(id_ for id_, _ in children(source))

    retained = set()
    for ids in incoming.values():
        for id_ in ids:
            kind, _ = registry[id_]
            if kind in ("idea", "dynamic_modifiers", "templates", "event", "opinion", "character"):
                if id_ == "SyriaFocus.39" or (kind == "idea" and id_ in existing_ideas):
                    continue
                retained.add(id_)
    # Transitively preserve only dependencies of the shared native contracts.
    while True:
        previous = retained.copy()
        for id_ in previous:
            for dependency in tokens(registry[id_][1]) & registry.keys():
                kind, _ = registry[dependency]
                if kind not in ("focus", "scripted_triggers") and not (kind == "idea" and dependency in existing_ideas):
                    retained.add(dependency)
        if retained == previous:
            break

    patched = {}
    old_focus_ids = set(definitions("common/national_focus/05_syria.txt", sources.get("common/national_focus/05_syria.txt", "")))
    focus_pattern = r"\bhas_completed_focus\s*=\s*(" + "|".join(sorted(map(re.escape, old_focus_ids), key=len, reverse=True)) + r")\b"
    old_triggers = {id_ for id_, (kind, _) in registry.items() if kind == "scripted_triggers"}
    # Foreign 2000 conditions on a deleted Syrian programme remain false. This
    # eliminates dangling focus IDs without adding invisible dummy focuses.
    for relative, text in texts.items():
        original = text
        text, count = re.subn(focus_pattern, "always = no", text)
        if "SyriaFocus.39" in text:
            text, removed = re.subn(r"country_event\s*=\s*\{[^{}]*\bid\s*=\s*SyriaFocus\.39\b[^{}]*\}", "# COLDWAR_SYR: modern Assad-family succession retired.\n", text)
            count += removed
        if text != original:
            backup(root, relative)
            (root / relative).write_text(text, encoding="utf-8")
            patched[relative] = count

    # Global generic code may still ask the public historical-path helper. It
    # must return false rather than re-enable the deleted modern Syria AI chain.
    used_triggers = sorted(set().union(*[set(ids) for ids in incoming.values()]) & old_triggers) if incoming else []
    trigger_text = HEADER + "\n".join(f"{id_} = {{ always = no }}" for id_ in used_triggers) + "\n"
    if used_triggers:
        write(root, "common/scripted_triggers/COLDWAR_SYR_shared_legacy_triggers.txt", trigger_text)
    by_kind = {}
    for id_ in sorted(retained):
        kind, source = registry[id_]
        source = re.sub(focus_pattern, "always = no # COLDWAR_SYR: retired modern Syrian programme.\n", source)
        by_kind.setdefault(kind, []).append(source)
    output = {
        "idea": ("common/ideas", "ideas = { country = {\n", "\n} }"),
        "event": ("events", "", ""),
        "dynamic_modifiers": ("common/dynamic_modifiers", "", ""),
        "templates": ("common/factions/templates", "", ""),
        "opinion": ("common/opinion_modifiers", "opinion_modifiers = {\n", "\n}"),
        "character": ("common/characters", "characters = {\n", "\n}"),
        "scripted_effects": ("common/scripted_effects", "", ""),
    }
    for kind, sources_ in by_kind.items():
        folder, prefix, suffix = output[kind]
        if kind == "event":
            namespaces = sorted({id_.split(".")[0] for id_ in retained if registry[id_][0] == "event"})
            prefix = "\n".join("add_namespace = " + namespace for namespace in namespaces) + "\n\n"
        write(root, f"{folder}/COLDWAR_SYR_shared_legacy_{kind}.txt", HEADER + prefix + "\n\n".join(sources_) + suffix + "\n")
    write(root, "common/scripted_effects/COLDWAR_SYR_shared_legacy_callbacks.txt", HEADER + """# Public MD dispatcher compatibility: the historical roster owns Syria now.
set_leader_SYR = { COLDWAR_SYR_1970_set_leader = yes }
""")

    # Retire the modern Syrian AI choices in the shared rule UI and its startup
    # dispatcher. Exact block boundaries protect neighbouring countries.
    for relative, selector in (("common/game_rules/00_game_rules.txt", "SYR_ai_behavior"),
                               ("common/on_actions/999_game_rules_on_actions.txt", "SYR")):
        path = root / relative
        text = path.read_text(encoding="utf-8-sig")
        candidates = list(re.finditer(r"(?m)^\s*" + selector + r"\s*=\s*\{", text))
        removed_count = 0
        for match in reversed(candidates):
            end = closing_brace(text, text.index("{", match.start())) + 1
            if selector == "SYR" and "rule = SYR_ai_behavior" not in text[match.start():end]:
                continue
            if not removed_count:
                backup(root, relative)
            text = text[:match.start()] + "\n# COLDWAR_SYR: modern Syrian AI programme retired.\n" + text[end:]
            removed_count += 1
        if removed_count:
            path.write_text(text, encoding="utf-8")
            patched[relative] = removed_count

    path = root / HISTORY
    history = path.read_text(encoding="utf-8-sig")
    backup(root, HISTORY)
    # Retain every pre-2000 block and all undated content. This migration never
    # modifies the currently authored 1970 snapshot or its deferred empty OOBs.
    dated = list(re.finditer(r"(?m)^\s*((?:20\d\d)\.\d+\.\d+)\s*=\s*\{", history))
    for match in reversed(dated):
        end = closing_brace(history, history.index("{", match.start())) + 1
        history = history[:match.start()] + history[end:]
    history = history.replace("# Authored Cold War 1970 snapshot; native later history retained.", "# COLDWAR_SYR: authored Cold War 1970 snapshot; modern history retired by user request.")
    path.write_text(history, encoding="utf-8")

    removed = []
    for relative in FILES:
        path = (root / relative).resolve()
        assert path.is_relative_to(root), path
        if path.is_file():
            path.unlink()
            removed.append(relative)
    report = {"retired_files": removed, "sha256_originals": hashes,
              "incoming_references_before_migration": incoming,
              "retained_shared_definitions": sorted(retained),
              "retired_foreign_focus_conditions": patched,
              "false_legacy_ai_triggers": used_triggers,
              "history_blocks_removed": [m.group(1) for m in dated],
              "backup_directory": "tools/syria_1970/retired_modern"}
    write(root, "tools/syria_1970/retirement_report.json", json.dumps(report, indent=2) + "\n")
    return report


def retire_auxiliary(root):
    """Retire unused modern unit files and prune the dedicated old text bundle.

    Live foreign contracts keep the English keys they actually consume, plus
    their substitution dependencies. Historical art and generic MD infrastructure
    are intentionally reused rather than treated as modern Syrian programmes.
    """
    root = Path(root).resolve()
    report_path = root / 'tools/syria_1970/retirement_auxiliary_report.json'
    if report_path.is_file():
        return json.loads(report_path.read_text(encoding='utf-8'))
    old_localisation = sorted((root/'localisation').glob('*/MD_focus_SYR_l_*.yml'))
    english = root/'localisation/english/MD_focus_SYR_l_english.yml'
    keys = {}
    if english.is_file():
        for line in english.read_text(encoding='utf-8-sig').splitlines():
            match = re.match(r'^\s+([\w.]+):(?:\d+)?\s+"', line)
            if match:
                keys[match.group(1)] = line
    all_tokens, unit_references = set(), {}
    units = sorted((root/'history/units').glob('SYR_*_units.txt'))
    units += sorted((root/'history/units').glob('Syrian_Arab_Army_Remnants_*.txt'))
    unit_names = {p.stem for p in units}
    for folder in ('common', 'events', 'history', 'interface'):
        for path in (root/folder).rglob('*'):
            if not path.is_file() or path.suffix not in ('.txt', '.gui', '.gfx') or path in units:
                continue
            text = path.read_text(encoding='utf-8-sig')
            executable = re.sub(r'#[^\n]*', '', text)
            found = set(re.findall(r'[A-Za-z_][\w.]*', executable))
            all_tokens.update(found & keys.keys())
            for unit in unit_names & found:
                unit_references.setdefault(unit, []).append(path.relative_to(root).as_posix())
    for path in (root/'localisation/english').rglob('*.yml'):
        if path == english:
            continue
        substitutions = set(re.findall(r'\$([\w.]+)(?:\|[^$]+)?\$', path.read_text(encoding='utf-8-sig')))
        all_tokens.update(substitutions & keys.keys())
    retained = all_tokens & keys.keys()
    while True:
        previous = retained.copy()
        for key in previous:
            if key+'_desc' in keys:
                retained.add(key+'_desc')
            retained.update(set(re.findall(r'\$([\w.]+)(?:\|[^$]+)?\$', keys[key])) & keys.keys())
        if retained == previous:
            break
    if retained:
        text = 'l_english:\n # COLDWAR_SYR | Text required by retained foreign/shared MD contracts.\n'
        text += '\n'.join(keys[key] for key in sorted(retained))+'\n'
        write(root, 'localisation/english/COLDWAR_SYR_shared_legacy_l_english.yml', text, bom=True)
    removed = []
    for path in [*old_localisation, *[p for p in units if p.stem not in unit_references]]:
        resolved = path.resolve()
        assert resolved.is_relative_to(root), resolved
        relative = path.relative_to(root).as_posix()
        backup(root, relative)
        path.unlink()
        removed.append(relative)
    report = {'retired_files': removed, 'retained_english_keys': sorted(retained),
              'retained_unit_files_with_incoming_references': unit_references,
              'backup_directory': 'tools/syria_1970/retired_modern'}
    write(root, 'tools/syria_1970/retirement_auxiliary_report.json', json.dumps(report, indent=2)+'\n')
    return report


def retire_remaining_focus_awards(root):
    """Keep foreign peace settlements while dropping completions of deleted foci."""
    root = Path(root).resolve()
    report_path = root/'tools/syria_1970/retirement_awards_report.json'
    report = json.loads(report_path.read_text(encoding='utf-8')) if report_path.is_file() else {}
    source = root/'tools/syria_1970/retired_modern/common/national_focus/05_syria.txt'
    ids = definitions('common/national_focus/05_syria.txt', source.read_text(encoding='utf-8-sig'))
    pattern = r'\b(?:complete_national_focus|uncomplete_national_focus)\s*=\s*(?:'+ '|'.join(sorted(map(re.escape, ids), key=len, reverse=True))+r')\b'
    for folder in ('common', 'events', 'history'):
        for path in (root/folder).rglob('*.txt'):
            original = path.read_text(encoding='utf-8-sig')
            updated, count = re.subn(pattern, '# COLDWAR_SYR | Retired modern focus award; the diplomatic agreement itself remains.\n', original)
            if count:
                relative = path.relative_to(root).as_posix()
                backup(root, relative)
                path.write_text(updated, encoding='utf-8')
                report[relative] = report.get(relative, 0)+count
    write(root, 'tools/syria_1970/retirement_awards_report.json', json.dumps(report, indent=2)+'\n')
    return report
