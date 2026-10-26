# IMPERIA CW — Cold War: Egypt 1970 content generator.
# COLDWAR | 'available' conditions of the design converted to triggers.
import re
from cw_common import PFX

NASSER = 'has_country_leader = { name = "Gamal Abdel Nasser" ruling_only = yes }'
TRANSFER = ("check_variable = {{ party_pop_array^{i} > 0.199 }}\nhas_stability > 0.399\nhas_civil_war = no")

AV = {
    "Krieg mit ISR `has_war_with`": "has_war_with = ISR",
    "Nasser ist Staatschef `has_country_leader` und Datum < 20.09.1970": f"{NASSER}\ndate < 1970.9.20",
    "Nasser ist nicht mehr Staatschef; `neutrality_neutral_social_are_in_power`": f"NOT = {{ {NASSER} }}\nneutrality_neutral_social_are_in_power = yes",
    "Nasser nicht mehr Staatschef; Mukhabarat-Meinung ≥ 60; Outlook Emerging ≥ 12 %":
        f"NOT = {{ {NASSER} }}\ncheck_variable = {{ intelligence_community_opinion > 59 }}\n{PFX}outlook_at_least_emerging_12 = yes",
    "Nasser nicht mehr Staatschef; PP ≥ 100; Stabilität ≥ 45 %": f"NOT = {{ {NASSER} }}\nhas_political_power > 99\nhas_stability > 0.449",
    "Nasser nicht mehr Staatschef; Militär-Meinung ≥ 70": f"NOT = {{ {NASSER} }}\ncheck_variable = {{ the_military_opinion > 69 }}",
    "`EGY_1970_sadat_path`; Datum ≥ 01.01.1971": f"has_country_flag = {PFX}sadat_path\ndate > 1970.12.31",
    "`has_government = communism` und `mdcw_cw_can_join_soviet` oder `mdcw_cw_can_join_beijing`":
        "has_government = communism\nOR = { mdcw_cw_can_join_soviet = yes mdcw_cw_can_join_beijing = yes }",
    "`has_government = democratic`; USA existiert": "has_government = democratic\ncountry_exists = USA",
    "`has_government = democratic` und `mdcw_cw_can_join_west`": "has_government = democratic\nmdcw_cw_can_join_west = yes",
    "`neutrality_neutral_social_are_in_power`; `EGY_1970_platforms_open`": f"neutrality_neutral_social_are_in_power = yes\nhas_country_flag = {PFX}platforms_open",
    "`neutrality_neutral_autocracy_are_in_power`; 214 Suez kontrolliert": "neutrality_neutral_autocracy_are_in_power = yes\n214 = { is_controlled_by = ROOT }",
    "`neutrality_neutral_oligarch_are_in_power`; 214 Suez kontrolliert": "neutrality_neutral_oligarch_are_in_power = yes\n214 = { is_controlled_by = ROOT }",
    "`neutrality_neutral_oligarch_are_in_power`; nicht `EGY_1970_no_privatisation`": f"neutrality_neutral_oligarch_are_in_power = yes\nNOT = {{ has_country_flag = {PFX}no_privatisation }}",
    "`western_autocrats_are_in_power`; `EGY_1970_peace_with_israel`": f"western_autocrats_are_in_power = yes\nhas_country_flag = {PFX}peace_with_israel",
    "`western_liberals_are_in_power`; nicht im Krieg": "western_liberals_are_in_power = yes\nhas_war = no",
    "`nationalist_right_wing_populists_are_in_power`; SUD existiert": "nationalist_right_wing_populists_are_in_power = yes\ncountry_exists = SUD",
    "`western_autocrats_are_in_power`; `EGY_1970_canal_reopened`": f"western_autocrats_are_in_power = yes\nhas_country_flag = {PFX}canal_reopened",
    "Krieg mit ISR `has_war_with`; 213 Sinai nicht unter eigener Kontrolle `is_controlled_by`": "has_war_with = ISR\n213 = { NOT = { is_controlled_by = ROOT } }",
    "213 Sinai oder dessen Kanalufer unter eigener Kontrolle": "213 = { is_controlled_by = ROOT }",
    "Krieg mit ISR `has_war_with`; SAU existiert": "has_war_with = ISR\ncountry_exists = SAU",
    "`EGY_1970_disengagement`": f"has_country_flag = {PFX}disengagement",
    "214 Suez kontrolliert; nicht im Krieg mit ISR oder 213 kontrolliert":
        "214 = { is_controlled_by = ROOT }\nOR = {\nNOT = { has_war_with = ISR }\n213 = { is_controlled_by = ROOT }\n}",
    "Datum < 01.01.1971; JOR und PAL existieren": "date < 1971.1.1\ncountry_exists = JOR\ncountry_exists = PAL",
    "Non-Aligned, Emerging oder Nationalist regiert; LBA und SYR integriert oder Untertanen":
        "OR = { has_government = neutrality has_government = communism has_government = nationalist }\n"
        "OR = { NOT = { country_exists = LBA } LBA = { is_subject_of = ROOT } }\n"
        "OR = { NOT = { country_exists = SYR } SYR = { is_subject_of = ROOT } }",
    "SOV existiert; Datum < 1972": "country_exists = SOV\ndate < 1972.1.1",
    "SOV-Meinung ≥ 50": "SOV = { has_opinion = { target = ROOT value > 49 } }",
    "`mdcw_cw_can_join_soviet`": "mdcw_cw_can_join_soviet = yes",
    "`mdcw_cw_can_join_west`": "mdcw_cw_can_join_west = yes",
    "SOV-Meinung < 25": "OR = { NOT = { country_exists = SOV } SOV = { has_opinion = { target = ROOT value < 25 } } }",
    "Datum ≥ 1974 oder `EGY_1970_infitah_flag`": f"OR = {{ date > 1973.12.31 has_country_flag = {PFX}infitah_flag }}",
    "Salafist oder Muslimbrüder regieren, oder „Sharia as a Principal Source“":
        f"OR = {{ has_government = fascism neutrality_neutral_muslim_brotherhood_are_in_power = yes has_completed_focus = {PFX}sharia_as_a_principal_source }}",
    "SOV-Meinung ≥ 25": "SOV = { has_opinion = { target = ROOT value > 24 } }",
    "214 Suez kontrolliert": "214 = { is_controlled_by = ROOT }",
    "nicht im Krieg": "has_war = no",
    "Datum ≥ 21.07.1970": "date > 1970.7.20",
    "Technologie `reactor1`": "has_tech = reactor1",
    "USA-Meinung ≥ 50": "USA = { has_opinion = { target = ROOT value > 49 } }",
    "Küstenstaat; YEM oder SYE nicht feindlich": "OR = { NOT = { country_exists = YEM } YEM = { NOT = { has_war_with = ROOT } } }",
}

# extra conditions taken from effect lines ("Nur mit ...", "Zusätzlich ...")
EXTRA_AV = {
    "na_the_new_class": f"has_country_flag = {PFX}infitah_flag",
    "na_the_free_economy": f"has_country_flag = {PFX}infitah_flag",
    "em_power_to_the_councils": "check_variable = { labour_unions_opinion > 69 }",
    "em_power_to_the_islamic_front": "date > 1978.12.31",
    "em_power_to_the_guardians": "date > 1978.12.31",
    "we_power_to_the_wafd": f"has_country_flag = {PFX}platforms_open",
    "we_power_to_the_liberals": f"has_country_flag = {PFX}platforms_open",
    "we_power_to_socialist_labour": f"has_country_flag = {PFX}platforms_open",
    "nt_restore_the_crown": "check_variable = { party_pop_array^23 > 0.149 }\ncheck_variable = { the_military_opinion > 59 }",
    "asu_the_second_era": "date > 1974.12.31",
}


def convert(av, party_idx=None):
    av = av.strip()
    if not av:
        return ""
    m = re.match(r"^`(\w+)`$", av)
    if m and m.group(1).startswith("EGY_1970_"):
        return f"has_country_flag = {m.group(1).replace('EGY_1970_', PFX)}"
    if m:
        return f"{m.group(1)} = yes"
    m = re.match(r"^`has_government = (\w+)`$", av)
    if m:
        return f"has_government = {m.group(1)}"
    if av.startswith("Popularität der Partei"):
        return TRANSFER.format(i=party_idx)
    if av in AV:
        return AV[av]
    m = re.match(r"^`(\w+_are_in_power)`; (.+)$", av)
    if m and m.group(2) in AV:
        return f"{m.group(1)} = yes\n{AV[m.group(2)]}"
    raise KeyError(av)
