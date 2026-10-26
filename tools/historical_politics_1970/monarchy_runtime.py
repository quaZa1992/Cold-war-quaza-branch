# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Rebuild only the four explicitly aligned historical royal leader pools.

The canonical catalogue owns the MD family and explicit personal traits.  This
adapter reuses the normal approved-portrait and native-counter providers, then
splices only these countries into the installed runtime.  It does not run the
global installer, change country history, or restore governments periodically.
"""
from __future__ import annotations

import re
from collections import defaultdict

from build import Builder, ROOT
from dispatch import (
    POOL_FILE, POOL_TRIGGER_FILE, SYNC_EFFECT, _find_block_end,
    _pool_text, _validated_people, _wrap_native_setter,
)
from native_retirement import alternative_trigger


TAGS = ("BHR", "JOR", "KUW", "PER")
RETIREMENT = "common/scripted_triggers/mdcw_historical_retirement_alternatives.txt"
TAG_PATTERN = "(?:" + "|".join(TAGS) + ")"


def _script_block(text: str, key: str) -> str:
    match = re.search(r"(?m)^" + re.escape(key) + r"\s*=\s*\{", text)
    if not match:
        raise ValueError("Missing runtime block: " + key)
    return text[match.start():_find_block_end(text, text.index("{", match.start()))]


def _blocks(text: str, pattern: str) -> list[tuple[int, int, str]]:
    result = []
    for match in re.finditer(pattern, text, re.M):
        start = match.start()
        end = _find_block_end(text, text.index("{", start))
        if end < len(text) and text[end] == "\n":
            end += 1
        result.append((start, end, text[start:end]))
    return result


def _splice(text: str, spans: list[tuple[int, int, str]], replacement: str) -> str:
    if not spans:
        raise ValueError("Expected existing country runtime rows")
    first = spans[0][0]
    for start, end, _ in reversed(spans):
        text = text[:start] + text[end:]
    return text[:first] + replacement + text[first:]


def _country_rows(text: str, pattern: str) -> list[tuple[int, int, str]]:
    """Return exact single-line country tests without rewriting their neighbours."""
    return [(m.start(), m.end(), m.group()) for m in re.finditer(pattern, text, re.M)]


def build(countries: dict) -> dict[str, str]:
    """Return seven narrowly patched loaded files; perform no writes."""
    missing = set(TAGS) - set(countries)
    if missing:
        raise ValueError("Missing monarchy catalogue countries: " + ", ".join(sorted(missing)))
    selected = {tag: countries[tag] for tag in TAGS}
    builder = Builder(selected)
    builder.leaders()
    people = _validated_people(ROOT, selected, builder.ready)
    grouped = defaultdict(list)
    families = defaultdict(lambda: defaultdict(list))
    for person in people:
        grouped[(person["tag"], person["party_index"])].append(person)
        families[person["tag"]][person["party_index"]].append(person)
    for tag in TAGS:
        if (tag, 0) not in grouped or (tag, 23) in grouped:
            raise ValueError(f"{tag}: expected reviewed Western Autocracy pool and no old Monarchist pool")

    generated_pools, generated_trigger = _pool_text(ROOT, grouped)
    pool_text = (ROOT / POOL_FILE).read_text(encoding="utf-8-sig")
    # Country helpers and counter-sync branches are separate contracts. Preserve
    # every unrelated country byte-for-byte in both sections.
    helper_pattern = r"^MDCW_HP_native_pool_" + TAG_PATTERN + r"_\d+\s*=\s*\{"
    helper_rows = _blocks(generated_pools, helper_pattern)
    pool_text = _splice(pool_text, _blocks(pool_text, helper_pattern), "".join(r[2] for r in helper_rows))
    sync = _script_block(pool_text, SYNC_EFFECT)
    generated_sync = _script_block(generated_pools, SYNC_EFFECT)
    sync_pattern = r"^\tif = \{\n\t\tlimit = \{ original_tag = " + TAG_PATTERN + r" check_variable = \{ ruling_party = \d+ \} \}"
    new_sync = _splice(sync, _blocks(sync, sync_pattern), "".join(r[2] for r in _blocks(generated_sync, sync_pattern)))
    pool_text = pool_text.replace(sync, new_sync, 1)

    trigger_text = (ROOT / POOL_TRIGGER_FILE).read_text(encoding="utf-8-sig")
    test_pattern = r"^\t\tAND = \{ original_tag = " + TAG_PATTERN + r" check_variable = \{ ruling_party = \d+ \} \}[^\n]*\n"
    trigger_text = _splice(trigger_text, _country_rows(trigger_text, test_pattern),
                           "".join(r[2] for r in _country_rows(generated_trigger, test_pattern)))

    retirement_text = (ROOT / RETIREMENT).read_text(encoding="utf-8-sig")
    generated_retirement = alternative_trigger(ROOT, people, {})
    retirement_pattern = r"^\t\tAND = \{ original_tag = " + TAG_PATTERN + r" check_variable = \{ ruling_party = \d+ \}[^\n]*\n"
    old_retirement = _country_rows(retirement_text, retirement_pattern)
    new_retirement = "".join(r[2] for r in _country_rows(generated_retirement, retirement_pattern))
    if old_retirement:
        retirement_text = _splice(retirement_text, old_retirement, new_retirement)
    elif new_retirement:
        # Keep future catalogue additions valid if previously sole approved
        # candidates acquire reviewed successors, or new sole pools appear.
        close = retirement_text.rfind("\t} }")
        if close < 0:
            raise ValueError("Missing retirement alternatives container")
        retirement_text = retirement_text[:close] + new_retirement + retirement_text[close:]

    result = {POOL_FILE: pool_text, POOL_TRIGGER_FILE: trigger_text, RETIREMENT: retirement_text}
    for tag in TAGS:
        result[f"common/scripted_effects/{tag}_political_leaders.txt"] = _wrap_native_setter(ROOT, tag, families[tag])
    return result
