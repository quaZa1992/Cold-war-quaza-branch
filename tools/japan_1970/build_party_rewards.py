# IMPERIA COLD WAR — Japan 1970 party reward source writer.
"""Build effective JAP party runtime fragments in staging only."""
from __future__ import annotations

import json
from pathlib import Path
import sys

from reward_revision import effective_party_map, load_overlay
from check_script_grammar import parse
from generate_staged_effects import state_building_guard

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "staging" / "party"
PREFIX = "COLDWAR_JAP_1970"
PARTY_NAMES = {
    "LDP": ("Liberal Democratic Party Programme", "Cabinet continuity and business-led development."),
    "DSP": ("Democratic Socialist Party Programme", "Labour reform and social partnership."),
    "JSP": ("Japan Socialist Party Programme", "Parliamentary social reform and public provision."),
    "JCP": ("Japanese Communist Party Programme", "Collective ownership and distributive reform."),
    "KMT": ("Komeito Programme", "Civic welfare and consensus government."),
}


def quote(text):
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base = json.loads((ROOT / "party_map.json").read_text(encoding="utf-8"))
    mapping = effective_party_map(base)
    helpers = mapping["focus_helpers"]
    dm_names = mapping["party_dynamic_modifiers"]
    ids = dict(mapping["party_registry"])
    ids["KMT"] = ids["Komeito"]
    lines = ["# IMPERIA COLD WAR — Japan party programme rewards.", f"# {PREFIX} party-bound programme rewards."]
    init = [f"{PREFIX}_party_modifiers_initialize = {{", "\tif = {",
            f"\t\tlimit = {{ original_tag = JAP IMP_is_1970_scenario = yes NOT = {{ has_country_flag = {PREFIX}_party_modifiers_initialized }} }}",
            f"\t\tset_variable = {{ var = {PREFIX}_factional_stability_factor value = -0.05 }}",
            f"\t\tset_variable = {{ var = {PREFIX}_factional_bureaucracy_cost_modifier value = 0.05 }}"]
    for party, modifier in dm_names.items():
        init.append(f"\t\tif = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {modifier} }} }} }} add_dynamic_modifier = {{ modifier = {modifier} }} }}")
    init += [f"\t\tif = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {PREFIX}_factional_government }} }} }} add_dynamic_modifier = {{ modifier = {PREFIX}_factional_government }} }}",
             f"\t\tset_country_flag = {PREFIX}_party_modifiers_initialized", "\t\tforce_update_dynamic_modifier = yes", "\t}", "}", ""]
    lines.extend(init)

    for ident, record in helpers.items():
        effect = record["effect"]
        flag = record["once_flag"]
        party = record["party"]
        variable_prefix = f"{PREFIX}_{party}_"
        gate = ["original_tag = JAP", "IMP_is_1970_scenario = yes", "has_variable = ruling_party",
                f"check_variable = {{ ruling_party = {record['ruling_party']} }}",
                f"NOT = {{ has_country_flag = {flag} }}"]
        asset_rewards = [reward for reward in record.get("one_time_effects", []) if reward.get("type") == "building"]
        gdp_shares = [reward.get("share", 0) for reward in record.get("one_time_effects", [])
                      if reward.get("type") == "treasury_gdp_share"]
        if len(gdp_shares) > 1 or any(share <= 0 or len(f"{share:.5f}".partition(".")[2]) > 5 for share in gdp_shares):
            raise ValueError(f"{ident}: invalid or duplicate GDP-priced party programme cost")
        if gdp_shares:
            gate.append("check_variable = { gdp_total > 0 }")
        for asset in asset_rewards:
            level = int(asset["level"])
            gate.append(state_building_guard(asset["state_id"], asset["building"], level, level))
        if record.get("scenario_guard") != "IMP_is_1970_scenario = yes":
            raise ValueError(f"{ident}: unsupported scenario guard {record.get('scenario_guard')}")
        lines += [f"{effect} = {{", "\tif = {", "\t\tlimit = {", *[f"\t\t\t{x}" for x in gate], "\t\t}",
                  f"\t\t{PREFIX}_party_modifiers_initialize = yes"]
        for modifier, amount in sorted(record.get("modifier_increments", {}).items()):
            lines.append(f"\t\tadd_to_variable = {{ {variable_prefix}{modifier} = {amount:.5f} }}")
        for reward in record.get("one_time_effects", []):
            kind = reward.get("type")
            if kind == "treasury":
                lines += [f"\t\tset_temp_variable = {{ treasury_change = {reward['amount']:.5f} }}", "\t\tmodify_treasury_effect = yes"]
            elif kind == "treasury_gdp_share":
                lines += [
                    f"\t\tset_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{reward['share']:.5f} }} }}",
                    "\t\tmodify_treasury_effect = yes",
                ]
            elif kind == "political_power":
                lines.append(f"\t\tadd_political_power = {reward['amount']:g}")
            elif kind == "research_bonus":
                if reward.get("category") not in {"CAT_industry", "CAT_agriculture"}:
                    raise ValueError(f"{ident}: unverified party research category {reward.get('category')}")
                name = reward.get("name", f"{PREFIX}_{ident}_research")
                lines += ["\t\tadd_tech_bonus = {", f"\t\t\tname = {name}",
                          f"\t\t\tbonus = {reward['bonus']:.2f}", f"\t\t\tuses = {reward['uses']}",
                          f"\t\t\tcategory = {reward['category']}", "\t\t}"]
            elif kind == "building":
                state_id = reward["state_id"]
                building = reward["building"]
                level = int(reward["level"])
                lines += [f"\t\t{state_id} = {{",
                          f"\t\t\tadd_extra_state_shared_building_slots = {level}",
                          f"\t\t\tadd_building_construction = {{ type = {building} level = {level} instant_build = yes }}",
                          "\t\t}"]
            else:
                raise ValueError(f"{ident}: unsupported one-time reward {reward}")
        lines += [f"\t\tset_country_flag = {flag}", "\t\tforce_update_dynamic_modifier = yes", "\t}", "}", ""]

    party_effects = "\n".join(lines) + "\n"
    parse(party_effects)

    dynamic = ["# IMPERIA COLD WAR — Japan current-party programme modifiers.", f"# {PREFIX} ruling-party dynamic modifiers."]
    party_to_keys = {party: set() for party in dm_names}
    for record in helpers.values():
        party_to_keys[record["party"]].update(record.get("modifier_increments", {}))
    for party, modifier in dm_names.items():
        dynamic += [f"{modifier} = {{", "\ticon = GFX_idea_JAP_japanese_economy", "\tenable = {",
                    "\t\toriginal_tag = JAP", "\t\tIMP_is_1970_scenario = yes", "\t\thas_variable = ruling_party",
                    f"\t\tcheck_variable = {{ ruling_party = {ids[party]} }}", "\t}"]
        for key in sorted(party_to_keys[party]):
            dynamic.append(f"\t{key} = {PREFIX}_{party}_{key}")
        dynamic += ["}", ""]
    dynamic += [f"# {PREFIX} LDP factional-government starting modifier.", f"{PREFIX}_factional_government = {{",
                "\ticon = GFX_idea_JAP_japanese_economy", "\tenable = {", "\t\toriginal_tag = JAP",
                "\t\tIMP_is_1970_scenario = yes", "\t\thas_variable = ruling_party",
                f"\t\tcheck_variable = {{ ruling_party = {ids['LDP']} }}", "\t}",
                f"\tstability_factor = {PREFIX}_factional_stability_factor",
                f"\tbureaucracy_cost_multiplier_modifier = {PREFIX}_factional_bureaucracy_cost_modifier", "}", ""]
    dynamic_text = "\n".join(dynamic)
    parse(dynamic_text)

    loc = ["l_english:", f"# IMPERIA COLD WAR — {PREFIX} party modifier localization."]
    loc.append(' COLDWAR_experience_gain_navy_factor_tt: "$MODIFIER_XP_GAIN_NAVY_FACTOR$: $RIGHT|+=%1$"')
    for party, (title, desc) in PARTY_NAMES.items():
        modifier = dm_names[party]
        loc += [f" {modifier}:0 {quote(title)}", f" {modifier}_desc:0 {quote(desc)}"]
    loc += [f" {PREFIX}_factional_government:0 {quote('Factional Government')}",
            f" {PREFIX}_factional_government_desc:0 {quote('Factional patronage lowers cabinet stability and raises bureaucracy expenditure while the Liberal Democratic Party governs.')}"]
    for record in helpers.values():
        for reward in record.get("one_time_effects", []):
            if reward.get("type") == "research_bonus":
                name = reward.get("name", f"{PREFIX}_{record['effect']}_research")
                loc.append(f" {name}:0 {quote('Industrial Research Commission')}")
    localization = "\n".join(loc) + "\n"

    (OUT / "COLDWAR_JAP_1970_party_effects.txt").write_text(party_effects, encoding="utf-8")
    (OUT / "COLDWAR_JAP_1970_party_dynamic_modifiers.txt").write_text(dynamic_text, encoding="utf-8")
    (OUT / "COLDWAR_JAP_1970_party_modifiers_l_english.yml").write_text(localization, encoding="utf-8-sig")
    print(f"Staged {len(helpers)} guarded party rewards across {len(dm_names)} ruling-party modifiers in {OUT}; no runtime files were written.")


if __name__ == "__main__":
    main()
