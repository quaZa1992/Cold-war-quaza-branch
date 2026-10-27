#!/usr/bin/env python3
# IMPERIA CW — Cold War: guarded Japan diplomatic responses and sender notices.
"""Guard Japan 1970 foreign responses and notify Japan after each transaction.

The staged foreign event/decision files are the source of truth. Running this
script updates those files and their active copies. It is idempotent and checks
that every event maps to a registered focus/helper before writing anything.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STAGED = ROOT / "tools" / "japan_1970" / "staging" / "foreign"

EVENT_FILES = (
    (STAGED / "COLDWAR_JAP70_bilateral_events.txt", ROOT / "events" / "COLDWAR_JAP70_bilateral_events.txt"),
    (STAGED / "COLDWAR_JAP70_multilateral_invitation_events.txt", ROOT / "events" / "COLDWAR_JAP70_multilateral_invitation_events.txt"),
)
DECISION_FILE = (
    STAGED / "COLDWAR_JAP70_foreign_project_decisions.txt",
    ROOT / "common" / "decisions" / "COLDWAR_JAP70_foreign_project_decisions.txt",
)
PROJECT_FOCI = (
    "seoul_industrial_cooperation",
    "asean_infrastructure",
    "mekong_development",
    "indochina_reconstruction",
)


def matching_brace(text: str, opening: int) -> int:
    """Return the closing brace for an opening brace, ignoring comments/strings."""
    if text[opening] != "{":
        raise ValueError(f"expected '{{' at offset {opening}")
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for index in range(opening, len(text)):
        char = text[index]
        if comment:
            if char == "\n":
                comment = False
            continue
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "#":
            comment = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"unclosed brace at offset {opening}")


def blocks(text: str, pattern: str):
    """Yield (start, opening-brace, closing-brace) for regex-matched blocks."""
    for match in re.finditer(pattern, text, re.MULTILINE):
        opening = text.find("{", match.start(), match.end())
        if opening < 0:
            opening = text.find("{", match.end())
        if opening < 0:
            raise ValueError(f"block has no opening brace: {match.group(0)!r}")
        yield match.start(), opening, matching_brace(text, opening)


def named_block(text: str, pattern: str):
    found = list(blocks(text, pattern))
    if len(found) != 1:
        raise ValueError(f"expected one block for {pattern!r}, found {len(found)}")
    return found[0]


def load_focuses() -> tuple[str, ...]:
    registry = json.loads((STAGED / "foreign_helper_registry.json").read_text(encoding="utf-8"))
    focuses = tuple(sorted({row["focus"] for row in registry}, key=len, reverse=True))
    missing = set(PROJECT_FOCI) - set(focuses)
    if missing:
        raise ValueError(f"project focuses missing from registry: {sorted(missing)}")
    return focuses


def focus_from_option(option: str, focuses: tuple[str, ...]) -> tuple[str, str, str]:
    pending = re.search(r"has_country_flag\s*=\s*(COLDWAR_JAP70_[A-Za-z0-9_]+_pending)", option)
    if not pending:
        raise ValueError("option has no pending-flag guard")
    pending_flag = pending.group(1)
    resolved_flag = pending_flag.removesuffix("_pending") + "_resolved"
    focus = next((name for name in focuses if re.search(rf"(?:^|_){re.escape(name)}(?:_|$)", pending_flag)), None)
    if not focus:
        raise ValueError(f"cannot map {pending_flag} to a registered focus")
    return focus, pending_flag, resolved_flag


def insert_japan_guard(option: str) -> str:
    trigger = named_block(option, r"\btrigger\s*=\s*\{")
    _, opening, closing = trigger
    body = option[opening + 1 : closing]
    if re.search(r"\bJAP\s*=\s*\{\s*exists\s*=\s*yes\s*\}", body):
        return option
    return option[:closing] + " JAP = { exists = yes }" + option[closing:]


def guard_accept(option: str, focuses: tuple[str, ...]) -> str:
    focus, pending, resolved = focus_from_option(option, focuses)
    helper = f"COLDWAR_JAP70_notice_{focus}_accepted = yes"
    option = insert_japan_guard(option)
    if helper in option:
        return option
    _, opening, closing = named_block(option, r"\bhidden_effect\s*=\s*\{")
    old_body = option[opening + 1 : closing]
    guard = (
        f" if = {{ limit = {{ has_country_flag = {pending} "
        f"NOT = {{ has_country_flag = {resolved} }} JAP = {{ exists = yes }} }}"
    )
    return option[: opening + 1] + guard + old_body + f"\n   {helper}\n  }} " + option[closing:]


def guard_refusal(option: str, focuses: tuple[str, ...]) -> str:
    focus, pending, resolved = focus_from_option(option, focuses)
    helper = f"COLDWAR_JAP70_notice_{focus}_refused = yes"
    _, _, option_close = named_block(option, r"\boption\s*=\s*\{")
    _, _, trigger_close = named_block(option, r"\btrigger\s*=\s*\{")
    old_body = option[trigger_close + 1 : option_close]
    if (
        helper in old_body
        and old_body.count("hidden_effect") == 1
        and f"set_country_flag = {resolved}" in old_body
        and f"clr_country_flag = {pending}" in old_body
        and f"has_country_flag = {pending}" in old_body
        and f"has_country_flag = {resolved}" in old_body
    ):
        return option
    body = (
        " hidden_effect = { if = { limit = { "
        f"has_country_flag = {pending} NOT = {{ has_country_flag = {resolved} }} "
        f"}} set_country_flag = {resolved} clr_country_flag = {pending} {helper} }} }} "
    )
    return option[: trigger_close + 1] + body + option[option_close:]


def edit_event_file(text: str, focuses: tuple[str, ...], expected_accepts: int, expected_refusals: int) -> tuple[str, int, int]:
    accept_count = 0
    refusal_count = 0
    found_ids = 0
    for start, opening, closing in reversed(list(blocks(text, r"^country_event\s*=\s*\{"))):
        event = text[start : closing + 1]
        event_id = re.search(r"\bid\s*=\s*COLDWAR_JAP70_[A-Z]+\.(\d+)", event)
        if not event_id:
            continue
        number = int(event_id.group(1))
        if 7130 <= number <= 7132:
            found_ids += 1
        elif 7140 <= number <= 7154:
            found_ids += 1
        elif 7101 <= number <= 7122:
            found_ids += 1
        else:
            continue
        options = list(blocks(event, r"\boption\s*=\s*\{"))
        changed = event
        for option_start, option_open, option_close in reversed(options):
            option = changed[option_start : option_close + 1]
            name = re.search(r"\bname\s*=\s*([A-Za-z0-9_]+)", option)
            if not name:
                continue
            option_name = name.group(1)
            if option_name.endswith("_accept") or option_name == "COLDWAR_JAP70_project_accept":
                # Event 7133 is a timed cleanup event, not an invitation.
                option = guard_accept(option, focuses)
                accept_count += 1
            elif option_name.endswith("_refuse") or option_name == "COLDWAR_JAP70_project_refuse":
                option = guard_refusal(option, focuses)
                refusal_count += 1
            else:
                continue
            changed = changed[:option_start] + option + changed[option_close + 1 :]
        text = text[:start] + changed + text[closing + 1 :]
    if found_ids == 0:
        raise ValueError("no Japan foreign invitation events found")
    if accept_count != expected_accepts or refusal_count != expected_refusals:
        raise ValueError(
            f"event option coverage changed: accepts={accept_count}, refusals={refusal_count}; "
            f"expected {expected_accepts}/{expected_refusals}"
        )
    return text, accept_count, refusal_count


def edit_project_decisions(text: str) -> tuple[str, int]:
    changed_count = 0
    for focus in reversed(PROJECT_FOCI):
        pattern = rf"\bCOLDWAR_JAP70_{re.escape(focus)}_site\s*=\s*\{{"
        start, opening, closing = named_block(text, pattern)
        decision = text[start : closing + 1]
        _, hidden_open, hidden_close = named_block(decision, r"\bhidden_effect\s*=\s*\{")
        hidden = decision[hidden_open + 1 : hidden_close]
        helper = f"COLDWAR_JAP70_notice_{focus}_completed = yes"
        if "add_building_construction" not in hidden or "modify_treasury_effect" not in hidden:
            raise ValueError(f"{focus} decision is missing its guarded build or Japan charge")
        changed_count += 1
        if helper in hidden:
            continue
        # The successful location payout is the one guarded IF in this hidden effect.
        if_start, if_open, if_close = named_block(hidden, r"\bif\s*=\s*\{")
        if_body = hidden[if_open + 1 : if_close]
        if "add_building_construction" not in if_body or "modify_treasury_effect" not in if_body:
            raise ValueError(f"{focus} payout guard lacks the build and Japan charge")
        new_if = hidden[:if_close] + f"\n   {helper}\n  " + hidden[if_close:]
        new_hidden = decision[: hidden_open + 1] + new_if + decision[hidden_close:]
        text = text[:start] + new_hidden + text[closing + 1 :]
    for focus in PROJECT_FOCI:
        if text.count(f"COLDWAR_JAP70_notice_{focus}_completed = yes") != 1:
            raise ValueError(f"expected one completion notice for {focus}")
    if changed_count != len(PROJECT_FOCI):
        raise ValueError(f"validated {changed_count} project site decisions, expected {len(PROJECT_FOCI)}")
    return text, changed_count


def validate_event_shapes(text: str, expected_events: int) -> tuple[int, set[str]]:
    focuses = load_focuses()
    event_count = 0
    covered_focuses: set[str] = set()
    for start, _, closing in blocks(text, r"^country_event\s*=\s*\{"):
        event = text[start : closing + 1]
        event_id = re.search(r"\bid\s*=\s*COLDWAR_JAP70_[A-Z]+\.(\d+)", event)
        if not event_id:
            continue
        number = int(event_id.group(1))
        if not (
            7101 <= number <= 7122
            or 7130 <= number <= 7132
            or 7140 <= number <= 7154
        ):
            continue
        options = list(blocks(event, r"\boption\s*=\s*\{"))
        if len(options) != 2:
            raise ValueError(f"event {event_id.group(0)} has {len(options)} direct option blocks, expected 2")
        accept = refuse = False
        for option_start, _, option_close in options:
            option = event[option_start : option_close + 1]
            name = re.search(r"\bname\s*=\s*([A-Za-z0-9_]+)", option)
            if not name:
                raise ValueError(f"event {event_id.group(0)} has an unnamed option")
            option_name = name.group(1)
            focus, pending, resolved = focus_from_option(option, focuses)
            covered_focuses.add(focus)
            _, hidden_open, hidden_close = named_block(option, r"\bhidden_effect\s*=\s*\{")
            actual_effect = option[hidden_open + 1 : hidden_close]
            if option_name.endswith("_accept") or option_name == "COLDWAR_JAP70_project_accept":
                accept = True
                if f"COLDWAR_JAP70_notice_{focus}_accepted = yes" not in option:
                    raise ValueError(f"event {event_id.group(0)} lacks its accepted sender notice")
                if not re.search(
                    rf"has_country_flag\s*=\s*{re.escape(pending)}[\s\S]*?NOT\s*=\s*\{{\s*has_country_flag\s*=\s*{re.escape(resolved)}\s*\}}[\s\S]*?JAP\s*=\s*\{{\s*exists\s*=\s*yes\s*\}}",
                    actual_effect,
                ):
                    raise ValueError(f"event {event_id.group(0)} accept payout lacks the pending/resolved/JAP guard")
            elif option_name.endswith("_refuse") or option_name == "COLDWAR_JAP70_project_refuse":
                refuse = True
                if f"COLDWAR_JAP70_notice_{focus}_refused = yes" not in option:
                    raise ValueError(f"event {event_id.group(0)} lacks its refused sender notice")
                if not re.search(
                    rf"has_country_flag\s*=\s*{re.escape(pending)}[\s\S]*?NOT\s*=\s*\{{\s*has_country_flag\s*=\s*{re.escape(resolved)}\s*\}}",
                    actual_effect,
                ):
                    raise ValueError(f"event {event_id.group(0)} refusal lacks the pending/resolved guard")
                if re.search(r"JAP\s*=\s*\{\s*exists\s*=\s*yes\s*\}", actual_effect):
                    raise ValueError(f"event {event_id.group(0)} refusal incorrectly requires Japan")
            else:
                raise ValueError(f"event {event_id.group(0)} has unexpected option {option_name}")
        if not accept or not refuse:
            raise ValueError(f"event {event_id.group(0)} is missing its accept or refuse option")
        event_count += 1
    if event_count != expected_events:
        raise ValueError(f"found {event_count} diplomatic response events, expected {expected_events}")
    return event_count, covered_focuses


def write_utf8(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_bytes(text.encode("utf-8"))
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def update_pair(staged: Path, live: Path, transform) -> tuple[int, str]:
    original = staged.read_text(encoding="utf-8-sig")
    repaired, count = transform(original)
    if "\ufeff" in repaired:
        raise ValueError(f"unexpected BOM in script file {staged}")
    write_utf8(staged, repaired)
    write_utf8(live, repaired)
    return count, repaired


def main() -> None:
    focuses = load_focuses()
    bilateral_accepts, bilateral_refusals = [0], [0]
    multi_accepts, multi_refusals = [0], [0]

    def bilateral_transform(text):
        updated, accepts, refusals = edit_event_file(text, focuses, 25, 25)
        validate_event_shapes(updated, 25)
        bilateral_accepts[0] = accepts
        bilateral_refusals[0] = refusals
        return updated, accepts + refusals

    def multilateral_transform(text):
        updated, accepts, refusals = edit_event_file(text, focuses, 15, 15)
        validate_event_shapes(updated, 15)
        multi_accepts[0] = accepts
        multi_refusals[0] = refusals
        return updated, accepts + refusals

    counts = []
    for staged, live in EVENT_FILES:
        transform = bilateral_transform if "bilateral_events" in staged.name else multilateral_transform
        count, _ = update_pair(staged, live, transform)
        counts.append(count)
    decision_count, _ = update_pair(*DECISION_FILE, edit_project_decisions)

    print(
        "Validated diplomatic response repair: "
        f"{bilateral_accepts[0]} bilateral accepts, {bilateral_refusals[0]} bilateral refusals, "
        f"{multi_accepts[0]} multilateral accepts, {multi_refusals[0]} multilateral refusals, "
        f"{decision_count} project completion notices."
    )
    print("Updated staged sources and matching active event/decision files as UTF-8 without BOM.")


if __name__ == "__main__":
    main()
