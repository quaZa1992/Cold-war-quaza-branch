# IMPERIA COLD WAR — Compiled French foreign-policy runtime checker.
"""Read-only source/AST checks for the compiled France foreign-policy runtime."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "tools/france_1970_runtime"


def read(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8-sig") if path.is_file() else ""


def sha(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def block(text: str, marker: str) -> str:
    """Extract one balanced HOI block beginning at marker."""
    pos = text.find(marker)
    if pos < 0:
        return ""
    start = text.find("{", pos)
    if start < 0:
        return ""
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:index]
    return ""


def block_from(text: str, start: int) -> str:
    opening = text.find("{", start)
    if opening < 0:
        return ""
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[opening + 1:index]
    return ""


def main() -> int:
    design_path = RUNTIME / "runtime_design.json"
    manifest_path = RUNTIME / "manifest.json"
    design = json.loads(design_path.read_text(encoding="utf-8")) if design_path.is_file() else {}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    effects = read("common/scripted_effects/COLDWAR_FRA2_diplomacy_effects.txt")
    triggers = read("common/scripted_triggers/COLDWAR_FRA2_diplomacy_triggers.txt")
    decisions = read("common/decisions/COLDWAR_FRA2_diplomacy_decisions.txt")
    focus = read("common/national_focus/COLDWAR_FRA2_1970_focus.txt")
    core_effects = read("common/scripted_effects/COLDWAR_FRA2_1970_effects.txt")
    loc = read("localisation/english/COLDWAR_FRA2_1970_l_english.yml")
    money = read("common/scripted_effects/00_money_system.txt")
    ideas = read("common/ideas/COLDWAR_FRA2_diplomacy_ideas.txt")
    on_actions = read("common/on_actions/COLDWAR_FRA2_1970_on_actions.txt")
    budget_loc = read("localisation/english/MD_money_l_english.yml")
    budget_defined = read("common/scripted_localisation/COLDWAR_FRA2_cooperation_budget.txt")

    issues: list[str] = []
    notes: list[str] = []
    weekly_expense_effect = block(effects, "COLDWAR_FRA2_add_weekly_expenses = {")
    weekly_income_effect = block(effects, "COLDWAR_FRA2_add_weekly_income = {")
    pair_effect = block(effects, "COLDWAR_FRA2_sync_treaties = {")
    orphan_cleanup = block(effects, "COLDWAR_FRA2_cleanup_orphaned_recipient_ideas = {")
    offers = [(node["key"], node["offer"]) for node in design.get("nodes", []) if "offer" in node]
    nodes_by_key = {node["key"]: node for node in design.get("nodes", [])}
    new_keys = set(design.get("foreign_policy_revision", {}).get("added_focus_keys", []))
    new_offers = [(key, offer) for key, offer in offers if key in new_keys]
    if len(offers) != 67 or len(new_offers) != 32:
        issues.append(f"Compiled runtime offer counts are {len(offers)} total / {len(new_offers)} new; expected 67 / 32.")
    if not effects or not triggers or not decisions or not focus:
        issues.append("Compiled runtime files are missing; compile the approved design before running this checker.")
    if not manifest.get("approved_foreign_policy_sha256"):
        issues.append("Manifest does not record the approved foreign-policy input hash.")

    checked_pairs = 0
    checked_relations = 0
    for key, offer in offers:
        node = nodes_by_key[key]
        partner = offer["partner"]
        acceptance = block(effects, f"COLDWAR_FRA2_accept_{key} = {{")
        send = block(triggers, f"COLDWAR_FRA2_offer_can_send_{key} = {{")
        accept_trigger = block(triggers, f"COLDWAR_FRA2_offer_can_accept_{key} = {{")
        active = block(triggers, f"COLDWAR_FRA2_offer_active_{key} = {{")
        preview = block(effects, f"COLDWAR_FRA2_offer_preview_{key} = {{")
        recipient_decision = block(decisions, f"COLDWAR_FRA2_accept_{key} = {{")
        focus_id = next((node.get(field) for field in ("id", "focus_id") if node.get(field)), f"COLDWAR_FRA2_{key}")
        focus_match = re.search(r"(?m)^\s*id\s*=\s*" + re.escape(str(focus_id)) + r"\s*$", focus)
        focus_pos = focus_match.start() if focus_match else -1
        focus_start = focus.rfind("focus = {", 0, focus_pos) if focus_pos >= 0 else -1
        source_focus = block_from(focus, focus_start) if focus_start >= 0 else ""
        if not all((acceptance, send, accept_trigger, active, preview, recipient_decision, source_focus)):
            issues.append(f"{key}: missing emitted helper, guard, preview, recipient decision or source-focus block.")
            continue

        if f"COLDWAR_FRA2_offer_can_accept_{key} = yes" not in acceptance:
            issues.append(f"{key}: acceptance transaction does not recheck the acceptance trigger.")
        if f"FRA = {{ has_country_flag = COLDWAR_FRA2_pending_{key}" not in acceptance:
            issues.append(f"{key}: recipient transaction lacks the paired French pending receipt.")
        if f"COLDWAR_FRA2_offer_preview_{key} = yes" not in recipient_decision:
            issues.append(f"{key}: recipient decision does not show the full prospective terms.")
        if "TT_IF_THEY_ACCEPT" not in preview:
            issues.append(f"{key}: focus preview lacks the native acceptance heading.")
        completion = block(core_effects, f"COLDWAR_FRA2_complete_{key} = {{")
        if f"COLDWAR_FRA2_offer_{key} = yes" not in completion:
            issues.append(f"{key}: focus completion helper does not execute its named offer helper.")
        if f"COLDWAR_FRA2_offer_preview_{key} = yes" not in source_focus:
            issues.append(f"{key}: source focus does not call the nonexecuting preview helper.")
        if "effect_tooltip = {" not in source_focus:
            issues.append(f"{key}: focus preview is not contained in native effect_tooltip scope.")
        if "modify_treasury_effect = yes" not in preview or preview.count("modify_treasury_effect = yes") != 2:
            issues.append(f"{key}: bilateral setup-cost preview is missing a native treasury effect for one or both sides.")

        for side in ("france", "recipient"):
            side_data = offer[side]
            spirit = side_data["spirit"]
            idea_body = block(ideas, f"{spirit} = {{")
            if f"add_ideas = {spirit}" not in preview:
                issues.append(f"{key}/{side}: prospective spirit is not shown in the focus preview.")
            for reward in side_data["effects"]:
                kind = reward["kind"]
                if kind == "modifier":
                    value = str(reward["value"])
                    if not re.search(rf"(?m)^\s*{re.escape(reward['key'])}\s*=\s*{re.escape(value)}\s*$", idea_body):
                        # Decimal rendering in generated script is normalized, so compare numeric tokens too.
                        try:
                            present = any(abs(float(found) - float(value)) < 1e-9 for found in re.findall(rf"(?m)^\s*{re.escape(reward['key'])}\s*=\s*(-?[0-9.]+)\s*$", idea_body))
                        except (TypeError, ValueError):
                            present = False
                        if not present:
                            issues.append(f"{key}/{side}: signed modifier {reward['key']}={value} is missing from the prospective idea.")
                elif kind == "building":
                    state = int(reward["state"])
                    construction_pattern = rf"type\s*=\s*{re.escape(reward['building'])}\s+level\s*=\s*{int(reward['amount'])}\s+instant_build\s*=\s*yes"
                    slot = f"add_extra_state_shared_building_slots = {reward['slots']}"
                    if slot not in preview or not re.search(construction_pattern, preview):
                        issues.append(f"{key}/{side}: asset {reward['building']} and its shared slot are incomplete in preview.")
                    side_tag = "FRA" if side == "france" else offer["partner"]
                    side_heading = "COLDWAR_FRA2_france_accept_heading" if side == "france" else f"COLDWAR_FRA2_{key}_recipient_heading"
                    heading_pos = preview.find(side_heading)
                    side_pos = preview.find(f"{side_tag} = {{", heading_pos)
                    side_scope = block_from(preview, side_pos) if side_pos >= 0 else ""
                    state_blocks = [block_from(side_scope, match.start()) for match in re.finditer(rf"(?m)^\s*{state}\s*=\s*\{{", side_scope)]
                    valid_state_block = False
                    for state_block in state_blocks:
                        construction_match = re.search(construction_pattern, state_block)
                        slot_position = state_block.find(slot)
                        if construction_match and 0 <= slot_position < construction_match.start():
                            valid_state_block = True
                            break
                    if not valid_state_block:
                        issues.append(f"{key}/{side}: asset preview is not scoped to state {state} with instant construction.")
                elif kind == "research":
                    if f"category = {reward['category']} bonus = {reward['bonus']} uses = {reward['uses']}" not in preview:
                        issues.append(f"{key}/{side}: finite {reward['category']} research is missing from preview.")
                elif kind == "doctrine":
                    if f"category = {reward['category']} cost_reduction = {reward['reduction']} uses = {reward['uses']}" not in preview:
                        issues.append(f"{key}/{side}: finite {reward['category']} doctrine reduction is missing from preview.")
                elif kind == "experience":
                    command = {"army": "army_experience", "navy": "navy_experience", "air": "air_experience"}[reward["service"]]
                    if f"{command} = {reward['amount']}" not in preview:
                        issues.append(f"{key}/{side}: {command} award is missing from preview.")
                elif kind == "faction_opinion":
                    if f"{reward['provider']} = yes" not in preview:
                        issues.append(f"{key}/{side}: native {reward['provider']} opinion effect is missing from preview.")
                elif kind == "access":
                    if f"{reward['grantor']} = {{ give_military_access = {reward['beneficiary']} }}" not in preview:
                        issues.append(f"{key}/{side}: military access term is missing from prospective effects.")
                elif kind == "resource_rights":
                    if f"{reward['grantor']} = {{ give_resource_rights = {{ receiver = {reward['beneficiary']} state = {reward['state']} resources = {{ {' '.join(reward['resources'])} }} }} }}" not in preview:
                        issues.append(f"{key}/{side}: resource-rights term is missing from prospective effects.")
                elif kind == "weekly_gdp_expense":
                    if f"COLDWAR_FRA2_offer_{key}_{side}_weekly_share" not in preview or "Million/week" not in loc:
                        issues.append(f"{key}/{side}: native weekly expense amount/label is missing from prospective effects.")
                elif kind == "weekly_transfer":
                    if f"COLDWAR_FRA2_offer_{key}_{side}_weekly_transfer_" not in preview:
                        issues.append(f"{key}/{side}: matched weekly transfer amount is missing from prospective effects.")

        # Acceptance's final trigger must be before any receipt, fee or one-time award.
        guard_pos = acceptance.find(f"COLDWAR_FRA2_offer_can_accept_{key} = yes")
        mutation_positions = [p for token in ("set_country_flag = COLDWAR_FRA2_signed_", "modify_treasury_effect = yes", "add_building_construction =", "add_tech_bonus =", "add_doctrine_cost_reduction =") if (p := acceptance.find(token)) >= 0]
        if mutation_positions and (guard_pos < 0 or guard_pos > min(mutation_positions)):
            issues.append(f"{key}: acceptance mutates state before its final guard.")

        for guard_name, guard in (("send", send), ("acceptance", accept_trigger)):
            if f"COLDWAR_FRA2_pair_{partner}_clear = yes" not in guard:
                issues.append(f"{key}: {guard_name} guard lacks bilateral peace/embargo/sanction check.")
        if f"country_exists = {partner}" not in send:
            issues.append(f"{key}: send guard does not require the named recipient to exist.")
        pair_guard = block(triggers, f"COLDWAR_FRA2_pair_{partner}_clear = {{")
        if f"country_exists = {partner}" not in pair_guard or f"NOT = {{ has_war_with = {partner} }}" not in pair_guard or f"NOT = {{ is_embargoing = {partner} }}" not in pair_guard or f"NOT = {{ has_war_with = FRA }}" not in pair_guard or f"NOT = {{ is_embargoing = FRA }}" not in pair_guard:
            issues.append(f"{key}: bilateral activity guard omits country existence, bilateral peace or embargo status.")
        for family in ("dip", "fin", "eco", "mil"):
            for direction in ("on", "by"):
                if f"imp_{family}_sanc_{direction}_us" not in block(triggers, f"COLDWAR_FRA2_pair_{partner}_clear = {{"):
                    issues.append(f"{key}: pair guard omits mirrored {family}/{direction} sanction class.")

        if f"COLDWAR_FRA2_signed_{key}" not in active or f"{partner} = {{ has_country_flag = COLDWAR_FRA2_signed_{key} }}" not in active:
            issues.append(f"{key}: standing activation does not require both signed receipts.")
        spirit_ids = [offer[side]["spirit"] for side in ("france", "recipient")]
        for spirit in spirit_ids:
            spirit_body = block(ideas, f"{spirit} = {{")
            if not spirit_body:
                issues.append(f"{key}: permanent bilateral spirit {spirit} is missing from emitted ideas.")
            elif re.search(r"\bdays\s*=", spirit_body):
                issues.append(f"{key}: bilateral spirit {spirit} has a timed expiry.")

        transfer_rows = [row for side in ("france", "recipient") for row in offer[side]["effects"] if row["kind"] == "weekly_transfer"]
        if len(transfer_rows) % 2:
            issues.append(f"{key}: design has an unmatched weekly transfer record.")
        else:
            for index in range(len(transfer_rows) // 2):
                quote_var = f"COLDWAR_FRA2_transfer_quote_{key}_{index}"
                if quote_var not in effects:
                    issues.append(f"{key}: emitted helper lacks shared transfer quote {index}.")
                if f"additional_expenses_rate = FRA.{quote_var}" not in block(effects, "COLDWAR_FRA2_add_weekly_expenses = {"):
                    issues.append(f"{key}: expense callback does not debit shared quote {index}.")
                if f"additional_income_rate = FRA.{quote_var}" not in block(effects, "COLDWAR_FRA2_add_weekly_income = {"):
                    issues.append(f"{key}: income callback does not credit shared quote {index}.")
                cache = block(effects, f"COLDWAR_FRA2_cache_transfer_quote_{key}_{index} = {{")
                france_transfer_rows = [row for row in offer["france"]["effects"] if row["kind"] == "weekly_transfer"]
                payer = france_transfer_rows[index]["payer"]
                expected_payer_scope = "FRA" if payer == "FRA" else payer
                if f"{expected_payer_scope}.gdp_total" not in cache or "divide = 52" not in cache:
                    issues.append(f"{key}: shared quote {index} is not computed from payer {payer}'s GDP divided by 52.")
                if "value = 1 days = 7" not in cache:
                    issues.append(f"{key}: shared quote {index} lacks the seven-day cache expiry.")
                france_rows = [row for row in offer["france"]["effects"] if row["kind"] == "weekly_transfer"]
                recipient_rows = [row for row in offer["recipient"]["effects"] if row["kind"] == "weekly_transfer"]
                base = {name: value for name, value in france_rows[index].items() if name != "flow"}
                counterpart = next((row for row in recipient_rows if {name: value for name, value in row.items() if name != "flow"} == base), None)
                paired = [france_rows[index], counterpart] if counterpart else []
                expense = next((row for row in paired if row and row.get("flow") == "expense"), {})
                income = next((row for row in paired if row and row.get("flow") == "income"), {})
                for side_effect, aggregator, expected_country in ((expense, weekly_expense_effect, expense.get("payer")), (income, weekly_income_effect, income.get("recipient"))):
                    contribution = f"{('additional_expenses_rate' if side_effect is expense else 'additional_income_rate')} = FRA.{quote_var}"
                    summary_contribution = f"COLDWAR_FRA2_cooperation_weekly_{('expenses' if side_effect is expense else 'income')} = FRA.{quote_var}"
                    positions = [match.start() for match in re.finditer(re.escape(contribution), aggregator)]
                    if len(positions) != 1:
                        issues.append(f"{key}: matched transfer {index} has {len(positions)} {contribution} contributions, expected one.")
                        continue
                    parent_if = aggregator.rfind("if = {", 0, positions[0])
                    contribution_block = block_from(aggregator, parent_if) if parent_if >= 0 else ""
                    if f"tag = {expected_country}" not in contribution_block or f"has_country_flag = COLDWAR_FRA2_signed_{key}" not in contribution_block or f"COLDWAR_FRA2_offer_active_{key} = yes" not in contribution_block:
                        issues.append(f"{key}: {side_effect.get('flow')} callback can contribute without its country, signature and active-pair guards.")
                    if summary_contribution not in aggregator:
                        issues.append(f"{key}: matched transfer {index} is not included in the displayed budget total.")
                checked_pairs += 1

        for side, tag in (("france", "FRA"), ("recipient", partner)):
            for weekly in (row for row in offer[side]["effects"] if row["kind"] == "weekly_gdp_expense"):
                var = f"COLDWAR_FRA2_weekly_{key}_{side}"
                rate_row = f"additional_expenses_rate = {var}"
                positions = [match.start() for match in re.finditer(re.escape(rate_row), weekly_expense_effect)]
                if len(positions) != 1:
                    issues.append(f"{key}/{side}: programme expense contributes {len(positions)} times, expected once.")
                    continue
                parent_if = weekly_expense_effect.rfind("if = {", 0, positions[0])
                stream_block = block_from(weekly_expense_effect, parent_if) if parent_if >= 0 else ""
                if f"tag = {tag}" not in stream_block or f"has_country_flag = COLDWAR_FRA2_signed_{key}" not in stream_block or f"COLDWAR_FRA2_offer_active_{key} = yes" not in stream_block:
                    issues.append(f"{key}/{side}: programme expense is not guarded by its country, signature and active pair.")
                formula = re.search(r"value\s*=\s*gdp_total\s+multiply\s*=\s*(-?[0-9.]+)\s+divide\s*=\s*52", stream_block)
                if not formula or abs(float(formula.group(1)) - float(weekly["gdp_fraction"])) > 1e-10:
                    issues.append(f"{key}/{side}: programme expense is not recomputed from own GDP/52.")
                if f"COLDWAR_FRA2_cooperation_weekly_expenses = {var}" not in weekly_expense_effect:
                    issues.append(f"{key}/{side}: programme expense is missing from the native budget total.")

        for effect_kind in ("access", "resource_rights"):
            relation_rows = [row for side in ("france", "recipient") for row in offer[side]["effects"] if row["kind"] == effect_kind]
            if not relation_rows:
                continue
            checked_relations += len(relation_rows) // 2
            for row in relation_rows:
                if row["kind"] == "access":
                    receipt = f"COLDWAR_FRA2_access_owned_{key}_{row['grantor']}"
                    normalized_sync = re.sub(r"\s+", " ", pair_effect)
                    # Native trigger docs: beneficiary has access TO grantor.
                    # MD Tajikistan's paired check/revoke likewise performs
                    # diplomatic_relation removal in the beneficiary scope.
                    grant = (f"if = {{ limit = {{ {row['beneficiary']} = {{ NOT = {{ has_military_access_to = {row['grantor']} }} }} }} "
                             f"{row['grantor']} = {{ give_military_access = {row['beneficiary']} set_country_flag = {receipt} }} }}")
                    revoke = (f"if = {{ limit = {{ {row['grantor']} = {{ has_country_flag = {receipt} }} }} "
                              f"{row['beneficiary']} = {{ if = {{ limit = {{ has_military_access_to = {row['grantor']} }} "
                              f"diplomatic_relation = {{ country = {row['grantor']} relation = military_access active = no }} }} }} "
                              f"{row['grantor']} = {{ clr_country_flag = {receipt} }} }}")
                    if grant not in normalized_sync:
                        issues.append(f"{key}: military access is not granted only when missing, with an agreement-owned receipt.")
                    if revoke not in normalized_sync:
                        issues.append(f"{key}: suspension can revoke preexisting military access or lacks a receipt-scoped revoke.")
                else:
                    state = int(row["state"])
                    receipt = f"COLDWAR_FRA2_resource_rights_owned_{key}_{state}"
                    if row["grantor"] != "NGR" or row["beneficiary"] != "FRA" or state != 329 or row["resources"] != ["uranium"]:
                        issues.append(f"{key}: resource-right contract exceeds the reviewed Niger uranium scope.")
                    if receipt not in effects or f"remove_resource_rights = {state}" not in effects:
                        issues.append(f"{key}: resource-right cleanup lacks its state-specific owned receipt.")

    if "COLDWAR_FRA2_add_weekly_expenses" not in effects or "COLDWAR_FRA2_add_weekly_income" not in effects:
        issues.append("Compiled diplomacy runtime lacks the per-country expense/income aggregators.")
    if money.count("COLDWAR_FRA2_add_weekly_expenses = yes") != 1 or money.count("COLDWAR_FRA2_add_weekly_income = yes") != 1:
        issues.append("Native money integration does not call each France bilateral stream exactly once.")
    if not pair_effect:
        issues.append("Compiled diplomacy runtime lacks the treaty synchronizer.")
    elif any(term in pair_effect for term in ("modify_treasury_effect", "add_building_construction", "add_extra_state_shared_building_slots =", "add_tech_bonus =", "add_doctrine_cost_reduction =", "army_experience =", "navy_experience =", "air_experience =")):
        issues.append("Treaty suspend/restore helper replays a fee, building or finite reward.")
    if "set_variable = { COLDWAR_FRA2_cooperation_weekly_expenses = 0 }" not in weekly_expense_effect:
        issues.append("Weekly expense aggregate does not reset to zero before active contributions.")
    if "set_variable = { COLDWAR_FRA2_cooperation_weekly_income = 0 }" not in weekly_income_effect:
        issues.append("Weekly income aggregate does not reset to zero before active contributions.")
    if "COLDWAR_FRA2_add_domestic_weekly_expenses = yes" not in weekly_expense_effect:
        issues.append("Foreign expense wrapper does not include the France domestic expense helper.")
    if not all(token in on_actions for token in ("COLDWAR_FRA2_sync_treaties = yes", "COLDWAR_FRA2_cleanup_orphaned_recipient_ideas = yes")):
        issues.append("Daily reconciliation/orphan-cleanup hooks are not installed.")
    if "COLDWAR_FRA2_sync_treaties = yes" in on_actions:
        daily = block(on_actions, "on_daily = {")
        if daily.find("COLDWAR_FRA2_sync_treaties = yes") > daily.find("COLDWAR_FRA2_sync_programmes = yes"):
            issues.append("Daily treaty sync runs after domestic programme sync.")
        cleanup_pos = daily.find("COLDWAR_FRA2_cleanup_orphaned_recipient_ideas = yes")
        if cleanup_pos >= 0:
            depth = 0
            for char in daily[:cleanup_pos]:
                depth += char == "{"
                depth -= char == "}"
            if depth != 1:
                issues.append("Orphan cleanup is nested inside the France-only on_daily condition.")
    partners = {offer["partner"] for _, offer in offers}
    for partner in partners:
        if f"tag = {partner}" not in orphan_cleanup or "NOT = { country_exists = FRA }" not in orphan_cleanup:
            issues.append(f"Recipient tag {partner} is not covered by France-death orphan cleanup.")
        for _, offer in (item for item in offers if item[1]["partner"] == partner):
            recipient_spirit = offer["recipient"]["spirit"]
            if f"remove_ideas = {recipient_spirit}" not in orphan_cleanup:
                issues.append(f"Orphan cleanup omits recipient spirit {recipient_spirit} for {partner}.")

    # The uranium right is a managed treaty relation, never an output or mine grant.
    niger_offer = next((offer for key, offer in offers if key == "fp_niger_rights"), None)
    if niger_offer:
        send = block(triggers, "COLDWAR_FRA2_offer_can_send_fp_niger_rights = {")
        accept_trigger = block(triggers, "COLDWAR_FRA2_offer_can_accept_fp_niger_rights = {")
        active = block(triggers, "COLDWAR_FRA2_offer_active_fp_niger_rights = {")
        niger_guard_text = "has_country_flag = COLDWAR_FRA2_signed_fp_niger_rights NGR = { has_country_flag = COLDWAR_FRA2_signed_fp_niger_rights } COLDWAR_FRA2_offer_active_fp_niger_rights = yes"
        niger_guard_pos = pair_effect.find(niger_guard_text)
        niger_if_pos = pair_effect.rfind("if = {", 0, niger_guard_pos) if niger_guard_pos >= 0 else -1
        niger_sync = block_from(pair_effect, niger_if_pos) if niger_if_pos >= 0 else ""
        expected_preflight = "NOT = { FRA = { has_resources_rights = { state = 329 } } }"
        for name, guard in (("send", send), ("acceptance", accept_trigger)):
            if expected_preflight not in guard:
                issues.append(f"Niger resource rights are not preflighted at {name}; existing France rights could be revoked.")
            if "owns_state = 329" not in guard or "controls_state = 329" not in guard or "has_full_control_of_state = 329" not in guard or "imp_uranium_deposit_kt > 0" not in guard:
                issues.append(f"Niger state ownership/control/deposit checks are incomplete at {name}.")
        if "owns_state = 329" not in active or "controls_state = 329" not in active or "has_full_control_of_state = 329" not in active or "imp_uranium_deposit_kt > 0" not in active:
            issues.append("Niger uranium agreement does not suspend when Niger loses state 329 or the deposit ceases to qualify.")
        if expected_preflight in active:
            issues.append("Niger resource-right send preflight leaked into active state and would suspend the agreement after its own grant.")
        if "NOT = { has_resources_rights = { state = 329 } }" not in niger_sync:
            issues.append("Niger rights grant is not conditional on absence of an existing state right.")
        receipt = "COLDWAR_FRA2_resource_rights_owned_fp_niger_rights_329"
        if receipt not in pair_effect or "remove_resource_rights = 329" not in pair_effect or f"has_country_flag = {receipt} has_resources_rights = {{ state = 329 resources = {{ uranium }} }}" not in pair_effect:
            issues.append("Niger rights removal is not limited to an agreement-created uranium right in state 329.")
        if re.search(r"(?:add_building_construction\s*=\s*\{[^}]*type\s*=\s*uranium|uranium\s*=\s*\d+)", niger_sync, re.S):
            issues.append("Niger standing agreement directly grants uranium production or a mine.")
        if any(row["kind"] == "resource_rights" for side in ("france", "recipient") for row in niger_offer[side]["effects"]) and "give_resource_rights = { receiver = FRA state = 329 resources = { uranium } }" not in block(effects, "COLDWAR_FRA2_offer_preview_fp_niger_rights = {"):
            issues.append("Niger uranium rights are missing from prospective acceptance preview.")

    for token in ("COLDWAR_FRA2_cooperation_weekly_income_display", "COLDWAR_FRA2_cooperation_weekly_expense_display"):
        if token not in budget_loc or token not in budget_defined:
            issues.append(f"Native money tooltip row {token} is not connected through generated defined-text and MD money localisation.")
    if "COLDWAR_FRA2_cooperation_weekly_income = 0" not in weekly_income_effect or "COLDWAR_FRA2_cooperation_weekly_expenses = 0" not in weekly_expense_effect:
        issues.append("Bilateral fiscal summary totals are missing their zero baselines.")

    # Player-facing fiscal totals must be numeric native rows, with expense and income signs separated.
    for token in ("Additional Expenses", "Additional Income", "Million/week"):
        if token not in loc:
            notes.append(f"Localisation does not contain the native budget label {token!r}; inspect emitted budget presentation.")

    paths = [RUNTIME / "runtime_design.json", RUNTIME / "manifest.json", ROOT / "common/scripted_effects/COLDWAR_FRA2_diplomacy_effects.txt", ROOT / "common/scripted_triggers/COLDWAR_FRA2_diplomacy_triggers.txt", ROOT / "common/scripted_effects/COLDWAR_FRA2_1970_effects.txt", ROOT / "common/decisions/COLDWAR_FRA2_diplomacy_decisions.txt", ROOT / "common/national_focus/COLDWAR_FRA2_1970_focus.txt", ROOT / "localisation/english/COLDWAR_FRA2_1970_l_english.yml", ROOT / "common/scripted_effects/00_money_system.txt", ROOT / "common/on_actions/COLDWAR_FRA2_1970_on_actions.txt", ROOT / "common/scripted_localisation/COLDWAR_FRA2_cooperation_budget.txt", ROOT / "localisation/english/MD_money_l_english.yml"]
    result = {
        "project": "IMPERIA COLD WAR",
        "check": "compiled foreign-policy runtime source/AST",
        "runtime_design_sha256": sha(design_path),
        "manifest_sha256": sha(manifest_path),
        "approved_foreign_policy_sha256": manifest.get("approved_foreign_policy_sha256"),
        "focus_count": len(design.get("nodes", [])),
        "offer_count": len(offers),
        "new_offer_count": len(new_offers),
        "transfer_pairs_checked": checked_pairs,
        "standing_relations_checked": checked_relations,
        "source_hashes": {str(path.relative_to(ROOT)).replace("\\", "/"): sha(path) for path in paths},
        "issues": issues,
        "notes": notes,
        "native_engine_tested": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
