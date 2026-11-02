# IMPERIA COLD WAR — Retire the legacy Greek Cyprus crisis branch.
"""Small, repeatable adapter for retiring obsolete Greek Cyprus outputs."""

from pathlib import Path
import re
import sys
import importlib.util
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from multiplayer_quality.native_compat import blocks


LEGACY_FOCUS_PREFIX = "COLDWAR_GRE_1970_cyprus_"
LEGACY_HELPER_PREFIX = "COLDWAR_CYP_1970_"
RETIRED_EVENT_IDS = {103, 104, *range(122, 138)}


def prepare_greek_design(design):
    """Filter obsolete Cyprus catalogue nodes before Greece compilation.

    The retained IoA 15/16 focuses are local receipts for the new R2 actor
    route. They no longer create a second foreign proposal or event menu.
    """
    design["focuses"] = [node for node in design["focuses"] if node.get("section") != "cyprus"]
    design["sections"] = [section for section in design["sections"] if section.get("id") != "cyprus"]
    for node in design["focuses"]:
        if node.get("key") in ("ioa_15", "ioa_16"):
            node["event_contract"] = ""
            node["execution_mode"] = "receipt"
    return design


def retire_generated_cyprus(root):
    """Surgically remove stale generated Cyprus-only decision/event/effect blocks.

    Invoke after the canonical Greek compiler when migrating an old generated
    checkout. Focus-tree imports are handled by the Greek compiler integration.
    """
    root = Path(root)
    paths = (
        root / "common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt",
        root / "common/decisions/COLDWAR_GRE_1970_tree_decisions.txt",
        root / "events/COLDWAR_GRE_1970_tree_events.txt",
    )
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig")
        if "tree_effects" in path.name:
            text = _retire_effects(text)
        elif "tree_decisions" in path.name:
            text = _remove_nodes(text, lambda node, body: node["parent"] is not None and
                                 bool(re.fullmatch(r"COLDWAR_GRE_1970_retry_cyprus_\d+", node["key"])))
        elif "tree_events" in path.name:
            text = _remove_nodes(text, lambda node, body: node["parent"] is None and (
                bool(re.search(r"\bCOLDWAR_GRE_TREE\.(?:103|104|12[2-9]|13[0-7])\b", body)) or
                LEGACY_FOCUS_PREFIX in body))
        text = re.sub(r"(?m)^\s*# IMPERIA COLD WAR — CYP R2 RETIREMENT FILTER\n", "", text)
        _atomic_write(path, text.rstrip() + "\n")

    loc = root / "localisation/english/COLDWAR_GRE_1970_tree_l_english.yml"
    if loc.exists():
        rows = [line for line in loc.read_text(encoding="utf-8-sig").splitlines()
                if not re.match(r"\s*COLDWAR_GRE_1970_(?:cyprus_|retry_cyprus_)", line)
                and not re.match(r"\s*COLDWAR_GRE_1970_event_(?:103|104|12[2-9]|13[0-7])_[td]:", line)]
        _atomic_write(loc, "\n".join(rows).rstrip() + "\n", bom=True)
    return patch_ioa_receipt_focuses(root)


def patch_ioa_receipt_focuses(root):
    """Patch only IoA15/16 plus their local grant/receipt helpers canonically."""
    root = Path(root)
    compiler = root / "tools/greece_1970/compile.py"
    sys.path.insert(0, str(root / "tools/greece_1970"))
    sys.path.insert(0, str(root / "tools"))
    spec = importlib.util.spec_from_file_location("greek_compile_receipt_patch", compiler)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    emitted = {}
    module.write = lambda rel, text, bom=False: emitted.__setitem__(rel, text)
    module.compile_reconcile()
    module.compile_rewards()
    module.compile_proposals()
    module.compile_tick()
    module.compile_tree()

    rel = "common/national_focus/COLDWAR_GRE_1970_focus.txt"
    path = root / rel
    current = path.read_text(encoding="utf-8-sig")
    canonical = module.native_compatibility(emitted[rel], rel)
    old_blocks = _focus_blocks(current)
    new_blocks = _focus_blocks(canonical)
    targets = ("COLDWAR_GRE_1970_ioa_15", "COLDWAR_GRE_1970_ioa_16")
    if any(key not in old_blocks or key not in new_blocks for key in targets):
        raise RuntimeError("Both retained Greek IOA receipt focuses must exist before patching.")
    for key in targets:
        body = new_blocks[key][2]
        if "COLDWAR_CYP_R2_greek_" not in body or "COLDWAR_GRE_1970_complete_" + key.removeprefix("COLDWAR_GRE_1970_") + " = yes" not in body:
            raise RuntimeError(f"Canonical {key} is missing its R2 availability or local completion guard.")
    for key in sorted(targets, key=lambda item: old_blocks[item][0], reverse=True):
        start, end, _ = old_blocks[key]
        current = current[:start] + new_blocks[key][2] + current[end:]
    after_blocks = _focus_blocks(current)
    if any(after_blocks[key][2] != new_blocks[key][2] for key in targets):
        raise RuntimeError("Canonical Greek receipt focus blocks did not apply exactly.")
    _atomic_write(path, current)

    effect_rel = "common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt"
    effect_path = root / effect_rel
    effect_source = effect_path.read_text(encoding="utf-8-sig")
    canonical_effects = module.native_compatibility(module.HEADER + "\n".join(module.EFFECTS), effect_rel)
    effect_names = {
        "COLDWAR_GRE_1970_reconcile_programmes_effect",
        "COLDWAR_GRE_1970_clear_regime_programmes_effect",
        "COLDWAR_GRE_1970_tree_initialize",
        "COLDWAR_GRE_1970_tree_weekly_tick",
        *("COLDWAR_GRE_1970_" + prefix + key for prefix in ("grant_", "complete_") for key in ("ioa_15", "ioa_16")),
    }
    effect_source = _replace_named_blocks(effect_source, canonical_effects, effect_names, top_level_only=True)
    _atomic_write(effect_path, effect_source)

    decision_rel = "common/decisions/COLDWAR_GRE_1970_tree_decisions.txt"
    decision_path = root / decision_rel
    decision_source = decision_path.read_text(encoding="utf-8-sig")
    canonical_decisions = module.native_compatibility(
        module.HEADER + module.block(module.P + "tree_programmes", "\n".join(module.DECISIONS)), decision_rel)
    decision_source = _replace_named_blocks(
        decision_source, canonical_decisions,
        {"COLDWAR_GRE_1970_retry_ioa_15", "COLDWAR_GRE_1970_retry_ioa_16"},
        top_level_only=False, required_parent="COLDWAR_GRE_1970_tree_programmes")
    _atomic_write(decision_path, decision_source)

    loc_path = root / "localisation/english/COLDWAR_GRE_1970_tree_l_english.yml"
    loc = loc_path.read_text(encoding="utf-8-sig")
    loc = loc.replace("# IMPERIA CW — Cold War: greece 1970 English localisation.",
                      "# IMPERIA COLD WAR — Greece 1970 English localisation.")
    keys = (*targets, *(key + "_desc" for key in targets),
            "COLDWAR_GRE_1970_ioa_15_r2_receipt_tt", "COLDWAR_GRE_1970_ioa_16_r2_receipt_tt")
    for key in keys:
        line = " " + key + ":0 " + __import__("json").dumps(module.LOC[key], ensure_ascii=False)
        pattern = re.compile(r"(?m)^\s*" + re.escape(key) + r":0.*$")
        loc = pattern.sub(line, loc) if pattern.search(loc) else loc.rstrip() + "\n" + line + "\n"
    _atomic_write(loc_path, loc, bom=True)
    return {"focuses": list(targets), "effects": sorted(effect_names),
            "decisions": ["COLDWAR_GRE_1970_retry_ioa_15", "COLDWAR_GRE_1970_retry_ioa_16"],
            "localisation_keys": list(keys)}


def _focus_blocks(text):
    result = {}
    for node in blocks(text):
        if node["key"] != "focus" or node["parent"] is None:
            continue
        body = text[node["open"] + 1:node["end"] - 1]
        ident = re.search(r"\bid\s*=\s*(\S+)", body)
        if ident:
            start = text.rfind("\n", 0, node["open"]) + 1
            result[ident[1]] = (start, node["end"], text[start:node["end"]])
    return result


def _replace_named_blocks(current, canonical, names, top_level_only=False, required_parent=None):
    def selected(text):
        result = {}
        for node in blocks(text):
            if node["key"] not in names:
                continue
            if top_level_only and node["parent"] is not None:
                continue
            if required_parent and (node["parent"] is None or node["parent"]["key"] != required_parent):
                continue
            start = text.rfind("\n", 0, node["open"]) + 1
            result[node["key"]] = (start, node["end"], text[start:node["end"]])
        return result

    old, new = selected(current), selected(canonical)
    if set(names) - set(old) or set(names) - set(new):
        raise RuntimeError("Canonical Greek output is missing a requested retained block.")
    for key in sorted(names, key=lambda item: old[item][0], reverse=True):
        start, end, _ = old[key]
        current = current[:start] + new[key][2] + current[end:]
    return current


def _atomic_write(path, text, bom=False):
    path = Path(path)
    expected = ("\ufeff" if bom else "") + text
    if path.exists() and path.read_bytes() == expected.encode("utf-8"):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=path.name + ".",
                                     suffix=".tmp", delete=False) as handle:
        temp = Path(handle.name)
        handle.write(expected.encode("utf-8"))
        handle.flush()
    temp.replace(path)
    return True


def remove_retired_focus_shortcuts(source):
    """Drop every Greek shortcut aimed at a retired legacy Cyprus focus."""
    out = []
    cursor = 0
    while True:
        match = re.search(r"(?m)^\s*shortcut\s*=\s*\{", source[cursor:])
        if not match:
            out.append(source[cursor:])
            break
        start = cursor + match.start()
        open_at = cursor + match.end() - 1
        depth = 0
        quoted = escaped = False
        end = None
        for i in range(open_at, len(source)):
            ch = source[i]
            if quoted:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    quoted = False
                continue
            if ch == '"':
                quoted = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            out.append(source[cursor:])
            break
        block = source[start:end]
        if re.search(r"\btarget\s*=\s*COLDWAR_GRE_1970_cyprus_\d+\b", block):
            out.append(source[cursor:start])
            cursor = end
        else:
            out.append(source[cursor:end])
            cursor = end
    return "".join(out)


def _remove_nodes(text, predicate):
    nodes = blocks(text)
    selected = []
    selected_objects = set()
    for node in nodes:
        body = text[node["open"] + 1:node["end"] - 1]
        if predicate(node, body):
            selected.append(node)
            selected_objects.add(id(node))
    spans = []
    for node in selected:
        parent = node["parent"]
        covered = False
        while parent is not None:
            if id(parent) in selected_objects:
                covered = True
                break
            parent = parent["parent"]
        if not covered:
            spans.append((text.rfind("\n", 0, node["open"]) + 1, node["end"]))
    for start, end in sorted(spans, reverse=True):
        text = text[:start] + text[end:]
    return text


def _retire_effects(text):
    def remove(node, body):
        if node["parent"] is None and node["key"]:
            if re.fullmatch(r"COLDWAR_GRE_1970_(?:grant|complete|send)_cyprus_\d+", node["key"]):
                return True
            # These two stale offer dispatchers are replaced by local receipt
            # completions in the canonical compiler, not removed as focuses.
            if node["key"] in ("COLDWAR_GRE_1970_send_ioa_15", "COLDWAR_GRE_1970_send_ioa_16"):
                return True
        return False

    text = _remove_nodes(text, remove)
    # Existing IOA15/16 completion blocks become guarded local grants; the
    # canonical source has no event instance or counterpart-acceptance gates.
    for key in ("ioa_15", "ioa_16"):
        top = re.search(r"(?ms)^COLDWAR_GRE_1970_grant_" + key + r"\s*=\s*\{.*?^\}", text)
        if top:
            body = top.group(0)
            body = re.sub(r"(?m)^\s*has_country_flag = COLDWAR_GRE_1970_" + key + r"_accepted_CYP\s*$", "", body)
            body = re.sub(r"(?m)^\s*check_variable = \{ var = COLDWAR_GRE_1970_" + key + r"_offer_instance[^\n]*\}\s*$", "", body)
            if key == "ioa_15":
                body = re.sub(r"(?m)^\s*CYP = \{ if = \{ limit = \{ NOT = \{ has_country_flag = COLDWAR_CYP_1970_gre_sponsorship_accepted \} \} set_country_flag = COLDWAR_CYP_1970_gre_sponsorship_accepted add_to_variable = \{ COLDWAR_CYP_1970_coup_pressure = 10 \} clamp_variable = \{ var = COLDWAR_CYP_1970_coup_pressure min = 0 max = 100 \} \} \}\s*$", "", body)
            text = text[:top.start()] + body + text[top.end():]
        text = text.replace("COLDWAR_GRE_1970_send_" + key + " = yes",
                            "COLDWAR_GRE_1970_grant_" + key + " = yes")
    return text
