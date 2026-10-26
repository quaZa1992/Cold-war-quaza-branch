# IMPERIA CW — Cold War: Egypt 1970 content generator.
# COLDWAR | Compiles the German design effect lines into Clausewitz code (MD 2000 style).
import re
from cw_common import *
import egy_dsl as D

SHORT_IDX = {v: k for k, v in D.SHORT.items()}
SUBIDEO = {0: "Western_Autocracy", 1: "conservatism", 2: "liberalism", 3: "socialism", 4: "communist_state",
           5: "anarchist_communism", 6: "Conservative", 7: "Autocracy", 8: "Mod_Vilayat_e_Faqih", 9: "Vilayat_e_Faqih",
           10: "Kingdom", 11: "Caliphate", 12: "Neutral_Muslim_Brotherhood", 13: "Neutral_Autocracy",
           14: "Neutral_conservatism", 15: "oligarchism", 16: "Neutral_Libertarian", 17: "Neutral_green",
           18: "neutral_Social", 19: "Neutral_Communism", 20: "Nat_Populism", 21: "Nat_Fascism", 22: "Nat_Autocracy",
           23: "Monarchist"}
GROUP_TRAIT = {range(0, 4): "western", range(4, 10): "emerging", range(10, 12): "salafist",
               range(12, 20): "neutrality", range(20, 24): "nationalist"}


def ideology_trait(i):
    for r, g in GROUP_TRAIT.items():
        if i in r:
            return f"{g}_{SUBIDEO[i]}"


OUTLOOK_ID = {"Western": 0, "Emerging": 1, "Salafist": 2, "Non-Aligned": 3, "Nationalist": 4}
PARTY_BY_NAME = {v: k for k, v in D.PARTY.items()}
STATES = {213, 214, 215, 216, 217, 218, 219, 1102}

BUILD_HELPER_OK = {"one_state_agriculture_district", "one_state_infrastructure", "one_state_office_construction",
                   "one_state_energy_infrastructure", "one_state_fossil_fuel_powerplant", "one_state_industrial_complex",
                   "one_state_rail_terminal", "one_state_nuclear_reactor", "one_state_arms_factory", "one_state_anti_air",
                   "one_state_renewable_energy_infra", "one_state_air_base"}

DYN_GROUP = {"Staat": "state", "Wirtschaftsmodell": "economy", "Streitkräfte": "armed_forces"}

# leader names in English (design placeholders resolved to persons)
LEADER_EN = {
    "Großimam Abd al-Halim Mahmud": ("Abd al-Halim Mahmud", None),
    "ASU-Kandidat": ("Hussein el-Shafei", None),
    "Ali Sabri": ("Ali Sabri", None),
    "Mohamed Fawzi": ("Mohamed Fawzi", None),
    "Saad el-Shazly oder Mohamed Fawzi": ("Saad el-Shazly", None),
    "Generalsekretär der ECP": ("Michel Kamel", None),
    "Kandidat der Freihandelslobby": ("Abdel Aziz Hegazy", None),
    "Kandidat der Nil-Ökologen": ("Rushdi Said", None),
    "Revolutionsführer": ("Hassan al-Masri", None),
    "Umda-Kandidat der Notabeln": ("Mahmoud Abu Wafia", None),
    "Osman Ahmed Osman": ("Osman Ahmed Osman", None),
    "Emir der Jama'a": ("Muhammad Abd al-Salam Faraj", None),
    "Fathi Shiqaqi": ("Fathi Shiqaqi", None),
    "Mustafa Kamel Murad": ("Mustafa Kamel Murad", None),
    "Mamdouh Salem": ("Mamdouh Salem", None),
    "Umar al-Tilmisani": ("Umar al-Tilmisani", None),
    "amtierender Präsident": ("Anwar as-Sadat", None),
    "Fouad Serageddin": ("Fouad Serageddin", None),
    "radikaler Oberst": ("Hassan Abd el-Rahman", None),
    "Sprecher der Räte": ("Kamal Khalil", None),
    "König Fuad II. (Porträt vorhanden)": ("Fuad II", "gfx/leaders/EGY/Fuad_II.dds"),
    "Ibrahim Shukri": ("Ibrahim Shukri", None),
    "Khaled Mohieddin": ("Khaled Mohieddin", "gfx/leaders/EGY/Khaled_Mohieddin.dds"),
    "Zakaria Mohieddin": ("Zakaria Mohieddin", None),
    "Kandidat von Misr al-Fatat": ("Ahmed Hussein", None),
    # 'Neuer Staatschef' lines
    "Abd al-Ghani al-Gamasy": ("Abd al-Ghani al-Gamasy", None),
    "Abu al-Ela Madi": ("Abu al-Ela Madi", None),
    "Ali Sabri oder Khaled Mohieddin (ASU)": ("Ali Sabri", None),
    "Fouad Mohieddin (NDP-Generalsekretär)": ("Fouad Mohieddin", None),
    "Hosni Mubarak (ASU)": ("Hosni Mubarak", "gfx/leaders/EGY/hosni_mubarak.dds"),
    "Hosni Mubarak": ("Hosni Mubarak", "gfx/leaders/EGY/hosni_mubarak.dds"),
    "Khaled Mohieddin (Porträt vorhanden)": ("Khaled Mohieddin", "gfx/leaders/EGY/Khaled_Mohieddin.dds"),
    "Mustafa Khalil (Premier)": ("Mustafa Khalil", None),
    "Mustafa Mashhur (Porträt vorhanden)": ("Mustafa Mashhur", "gfx/leaders/EGY/Mustafa_Mashhur.dds"),
    "Omar Abd al-Rahman": ("Omar Abd al-Rahman", None),
    "Sami Sharaf": ("Sami Sharaf", None),
    "Sharawi Gomaa": ("Sharawi Gomaa", None),
    "Saad el-Shazly": ("Saad el-Shazly", None),
}
# COLDWAR | 1970 portrait overrides for all named focus leaders.
LEADER_PORTRAITS_1970 = {'Gamal Abdel Nasser': 'gfx/leaders/EGY/1970/nasser.dds', 'Anwar as-Sadat': 'gfx/leaders/EGY/1970/sadat.dds', 'Zakaria Mohieddin': 'gfx/leaders/EGY/1970/zakaria_mohieddin.dds', 'Fouad Serageddin': 'gfx/leaders/EGY/1970/serageddin.dds', 'Osman Ahmed Osman': 'gfx/leaders/EGY/1970/osman.dds', 'Ibrahim Shukri': 'gfx/leaders/EGY/1970/ibrahim_shukri.dds', 'Fuad Mursi': 'gfx/leaders/EGY/1970/fuad_mursi.dds', 'Henri Curiel': 'gfx/leaders/EGY/1970/henri_curiel.dds', 'Hussein el-Shafei': 'gfx/leaders/EGY/1970/hussein_shafei.dds', 'Ali Sabri': 'gfx/leaders/EGY/1970/ali_sabri.dds', 'Abd al-Razzaq Afifi': 'gfx/leaders/EGY/1970/afifi.dds', 'Hassan al-Hudaybi': 'gfx/leaders/EGY/1970/hudaybi.dds', 'Pope Cyril VI': 'gfx/leaders/EGY/1970/cyril_vi.dds', 'Abdel Aziz Hegazy': 'gfx/leaders/EGY/1970/hegazy.dds', 'Rushdi Said': 'gfx/leaders/EGY/1970/rushdi_said.dds', 'Khaled Mohieddin': 'gfx/leaders/EGY/1970/khaled_mohieddin.dds', 'Kamal el-Din Hussein': 'gfx/leaders/EGY/1970/kamal_hussein.dds', 'Mohamed Fawzi': 'gfx/leaders/EGY/1970/fawzi.dds', 'Fuad II': 'gfx/leaders/EGY/1970/fuad_ii.dds', 'Mohammed Ahmed Sadek': 'gfx/leaders/EGY/1970/sadek.dds', 'Saad el-Shazly': 'gfx/leaders/EGY/1970/shazly.dds', 'Abdel Ghani el-Gamasy': 'gfx/leaders/EGY/1970/gamasy.dds', 'Mahmoud Abdel Rahman Fahmy': 'gfx/leaders/EGY/1970/fahmy.dds', 'Fouad Mohamed Abou Zikry': 'gfx/leaders/EGY/1970/zikri.dds', 'Ali Mustafa Baghdady': 'gfx/leaders/EGY/1970/baghdady.dds', 'Mohammed Ali Fahmy': 'gfx/leaders/EGY/1970/air_defence_fahmy.dds', 'Hosni Mubarak': 'gfx/leaders/EGY/1970/mubarak.dds', 'Ahmad Ismail Ali': 'gfx/leaders/EGY/1970/ahmad_ismail.dds', 'Mohammed Ali Fahmi': 'gfx/leaders/EGY/1970/air_defence_fahmy.dds'}
LEADER_EN = {k: (name, LEADER_PORTRAITS_1970.get(name, pic))
             for k, (name, pic) in LEADER_EN.items()}

# COLDWAR | Party accession casting for formerly unpictured candidates.
COLDWAR_EGY_1970_PARTY_CAST = {0: ('Anwar as-Sadat', 'gfx/leaders/EGY/1970/sadat.dds'), 1: ('Zakaria Mohieddin', 'gfx/leaders/EGY/1970/zakaria_mohieddin.dds'), 2: ('Osman Ahmed Osman', 'gfx/leaders/EGY/1970/osman.dds'), 3: ('Ibrahim Shukri', 'gfx/leaders/EGY/1970/ibrahim_shukri.dds'), 4: ('Khaled Mohieddin', 'gfx/leaders/EGY/1970/khaled_mohieddin.dds'), 5: ('Henri Curiel', 'gfx/leaders/EGY/1970/henri_curiel.dds'), 6: ('Hussein el-Shafei', 'gfx/leaders/EGY/1970/hussein_shafei.dds'), 7: ('Ali Sabri', 'gfx/leaders/EGY/1970/ali_sabri.dds'), 8: ("Shi'a Reform Council", 'gfx/leaders/EGY/1970/shia_reform_council.dds'), 9: ('Council of Islamic Jurists', 'gfx/leaders/EGY/1970/shia_guardian_council.dds'), 10: ('Abd al-Razzaq Afifi', 'gfx/leaders/EGY/1970/afifi.dds'), 11: ('Sinai Leadership Council', 'gfx/leaders/EGY/1970/sinai_council.dds'), 12: ('Hassan al-Hudaybi', 'gfx/leaders/EGY/1970/hudaybi.dds'), 13: ('Pope Cyril VI', 'gfx/leaders/EGY/1970/cyril_vi.dds'), 14: ('Fouad Serageddin', 'gfx/leaders/EGY/1970/serageddin.dds'), 15: ('Osman Ahmed Osman', 'gfx/leaders/EGY/1970/osman.dds'), 16: ('Abdel Aziz Hegazy', 'gfx/leaders/EGY/1970/hegazy.dds'), 17: ('Rushdi Said', 'gfx/leaders/EGY/1970/rushdi_said.dds'), 18: ('Gamal Abdel Nasser', 'gfx/leaders/EGY/1970/nasser.dds'), 19: ('Khaled Mohieddin', 'gfx/leaders/EGY/1970/khaled_mohieddin.dds'), 20: ('Kamal el-Din Hussein', 'gfx/leaders/EGY/1970/kamal_hussein.dds'), 21: ("Egyptian Ba'ath Regional Command", 'gfx/leaders/EGY/1970/baath_council.dds'), 22: ('Mohamed Fawzi', 'gfx/leaders/EGY/1970/fawzi.dds'), 23: ('Fuad II', 'gfx/leaders/EGY/1970/fuad_ii.dds')}
LEADER_EN.update({f"COLDWAR_EGY_1970_candidate_{idx}": value
                  for idx, value in COLDWAR_EGY_1970_PARTY_CAST.items()})

NEW_TRAITS = {"Field Marshal": "COLDWAR_EGY_field_marshal", "Air Force Hero": "COLDWAR_EGY_air_force_hero",
              "Technocrat-in-Chief": "COLDWAR_EGY_technocrat_in_chief", "Ailing Rais": "COLDWAR_EGY_ailing_rais",
              "Consolidated Rule": "COLDWAR_EGY_consolidated_rule", "Rais for Life": "COLDWAR_EGY_rais_for_life"}


class Reg:
    """Collects everything the focus effects reference."""

    def __init__(self):
        self.ideas = {}          # id -> dict(name, mods, timed_days)
        self.dyn = {}            # group -> ordered list of modifier keys
        self.tt = {}             # custom tooltip key -> English text
        self.flags = set()
        self.events = set()
        self.offers = set()
        self.opinions = {}       # modifier id -> (value, trade?)
        self.cosmetic = {}       # tag -> (name, adj)
        self.traits = set()
        self.unhandled = []
        self.trees = {}

    def dynkey(self, group, key):
        self.dyn.setdefault(group, [])
        if key not in self.dyn[group]:
            self.dyn[group].append(key)
        return f"{PFX}{group}_{key}"


R = Reg()


def tt(key, text):
    k = f"{PFX}{key}_tt"
    R.tt[k] = text
    return f"custom_effect_tooltip = {k}"


def dyn_change(group, mods, modname=None):
    modname = modname or f"{PFX}{group}_modifier"
    out = [f"if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {modname} }} }} }} hidden_effect = {{ add_dynamic_modifier = {{ modifier = {modname} }} }} }}",
           f"custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {modname} }}"]
    for k, v in mods:
        var = R.dynkey(group, k)
        out.append(f"add_to_variable = {{ {var} = {fmt(v)} tooltip = @TT:{k}@ }}")
    return out


TOOLTIP_KEYS = set()   # filled by compile with existing *_tt loc keys
NEW_MOD_TT = {}


def tooltip_for(k):
    if f"{k}_tt" in TOOLTIP_KEYS:
        return f"{k}_tt"
    key = f"COLDWAR_{k}_tt"
    NEW_MOD_TT[key] = k
    return key


def idea_id(name):
    return PFX + slug(name)


def reg_idea(name, mods, days=None, **kw):
    iid = idea_id(name)
    R.ideas.setdefault(iid, dict(name=name, mods=mods, days=days, **kw))
    return iid


def gdp(effect, share):
    return [f"set_temp_variable = {{ {PFX}gdp_share = {fmt(share)} }}", f"{effect} = yes"]


def party_pop(idx, p, o):
    return [f"set_temp_variable = {{ party_index = {idx} }}",
            f"set_temp_variable = {{ party_popularity_increase = {fmt(p / 100)} }}",
            f"set_temp_variable = {{ temp_outlook_increase = {fmt(o / 100)} }}",
            "change_relative_party_popularity = yes"]


def faction(f, n):
    return [f"set_temp_variable = {{ temp_opinion = {n} }}", f"{PFX}change_{f}_opinion_exact = yes"]


def opinion(tag, n):
    mid = f"{PFX}{'positive' if n > 0 else 'negative'}_{abs(n)}"
    R.opinions[mid] = n
    return [f"add_opinion_modifier = {{ target = {tag} modifier = {mid} }}"]


def leader(idx, name_key, trait=None):
    name, pic = LEADER_EN.get(name_key, (name_key, None))
    traits = [ideology_trait(idx)]
    if trait:
        traits.append(NEW_TRAITS[trait])
        R.traits.add(trait)
    p = f' picture = "{pic}"' if pic else ""
    return [f'create_country_leader = {{ name = "{name}"{p} ideology = {SUBIDEO[idx]} traits = {{ {" ".join(traits)} }} }}']


def ruling_party(idx):
    return [f"set_temp_variable = {{ rul_party_temp = {idx} }}", "change_ruling_party_effect = yes"]


def current_party_index_of(focus):
    """party index for party-tree foci (section title 'Partei: ... (N)')"""
    return focus.get("_party")


# --------------------------------------------------------------- the compiler
def compile_line(e, f):
    fid = f["id"]
    short = fid.replace("EGY_1970_", "")
    if (short, e) in MAN:
        return MAN[(short, e)](f) if callable(MAN[(short, e)]) else MAN[(short, e)]
    if e in MANL:
        return MANL[e](f) if callable(MANL[e]) else MANL[e]
    if e.startswith("RAW:"):
        return e[4:].split("\n")
    m = re.match(r"^PP ([+-]\d+) `add_political_power`$", e)
    if m:
        return [f"add_political_power = {int(m.group(1))}"]
    m = re.match(r"^Stabilität ([+-]\d+) % `add_stability`$", e)
    if m:
        return [f"add_stability = {fmt(int(m.group(1)) / 100)}"]
    m = re.match(r"^Kriegsunterstützung ([+-]\d+) % `add_war_support`$", e)
    if m:
        return [f"add_war_support = {fmt(int(m.group(1)) / 100)}"]
    m = re.match(r"^.+ ([+-]\d+) `EGY_1970_change_(\w+)_exact` → `change_\w+_opinion`$", e)
    if m:
        return faction(m.group(2), int(m.group(1)))
    m = re.match(r"^(.+) ([+-][\d.]+) % Popularität \(Outlook ([+-][\d.]+) %\) `change_relative_party_popularity`$", e)
    if m:
        return party_pop(SHORT_IDX[m.group(1)], num(m.group(2)), num(m.group(3)))
    m = re.match(r"^Outlook (\S+) ([+-][\d.]+) % `change_relative_party_popularity`$", e)
    if m:
        return [f"set_temp_variable = {{ {PFX}outlook_id = {OUTLOOK_ID[m.group(1)]} }}",
                f"set_temp_variable = {{ {PFX}outlook_amount = {fmt(num(m.group(2)) / 100)} }}",
                f"{PFX}change_outlook_popularity = yes"]
    m = re.match(r"^Kosten ([\d.]+) % BIP `EGY_1970_pay_gdp_share`$", e)
    if m:
        return gdp(f"{PFX}pay_gdp_share", float(m.group(1)) / 100)
    m = re.match(r"^Kredit \+([\d.]+) % BIP Treasury, Schulden \+([\d.]+) % BIP", e)
    if m:
        return gdp(f"{PFX}receive_gdp_share", float(m.group(1)) / 100) + gdp(f"{PFX}change_debt_gdp_share", float(m.group(2)) / 100)
    m = re.match(r"^(Staat|Wirtschaftsmodell|Streitkräfte): (.*) `EGY_1970_\w+_modifier`$", e)
    if m:
        return dyn_change(DYN_GROUP[m.group(1)], parse_mods(m.group(2)))
    m = re.match(r"^Partei-Programm: (.*) `EGY_1970_(\w+)_programme`$", e)
    if m:
        txt = re.sub(r"^zusätzlich\s+", "", m.group(1))
        key = m.group(2)
        return dyn_change(f"{key}_programme", parse_mods(txt), modname=f"{PFX}{key}_programme")
    m = re.match(r"^Idee „(.+?)“: (.*?)(?: \((\d+) Tage `add_timed_idea`\)| `add_ideas`)$", e)
    if m:
        name, txt, days = m.group(1), m.group(2), m.group(3)
        iid = reg_idea(name, parse_mods(txt), int(days) if days else None)
        return [f"add_timed_idea = {{ idea = {iid} days = {days} }}"] if days else [f"add_ideas = {iid}"]
    m = re.match(r"^Regierungspartei → (.+?) `change_ruling_party_effect`(?:, Staatschef (.+?) `create_country_leader`)?$", e)
    if m:
        idx = PARTY_BY_NAME[m.group(1)]
        if m.group(2) and "power_to" in short and not LEADER_EN.get(m.group(2), (None, None))[1]:
            name_key = f"COLDWAR_EGY_1970_candidate_{idx}"
            leader_name = COLDWAR_EGY_1970_PARTY_CAST[idx][0]
            tooltip_key = f"{PFX}new_leader_{slug(leader_name)}_tt"
            R.tt[tooltip_key] = f"§Y{leader_name}§! becomes the leader of [ROOT.GetNameDef]."
            return [f"custom_effect_tooltip = {tooltip_key}", "hidden_effect = {"] + leader(idx, name_key) + ["}"] + ruling_party(idx)
        out = []
        if m.group(2):
            out += ["hidden_effect = {"] + leader(idx, m.group(2)) + ["}"]
            out.insert(0, f"custom_effect_tooltip = {PFX}new_leader_{slug(LEADER_EN.get(m.group(2), (m.group(2),))[0])}_tt")
            R.tt[f"{PFX}new_leader_{slug(LEADER_EN.get(m.group(2), (m.group(2),))[0])}_tt"] = \
                f"§Y{LEADER_EN.get(m.group(2), (m.group(2),))[0]}§! becomes the leader of [ROOT.GetNameDef]."
        return out + ruling_party(idx)
    m = re.match(r"^Neuer Staatschef: (.+?)(?:, Trait „(.+?)“)? `create_country_leader`$", e)
    if m:
        idx = f.get("_party")
        if idx is None:
            idx = 18
        if m.group(1).startswith("amtierender Präsident"):
            R.traits.add(m.group(2))
            return [f"add_country_leader_trait = {NEW_TRAITS[m.group(2)]}"]
        name = LEADER_EN.get(m.group(1), (m.group(1),))[0]
        key = f"{PFX}new_leader_{slug(name)}_tt"
        R.tt[key] = f"§Y{name}§! becomes the leader of [ROOT.GetNameDef]."
        return [f"custom_effect_tooltip = {key}", "hidden_effect = {", "retire_country_leader = yes"] + leader(idx, m.group(1), m.group(2)) + ["}"]
    m = re.match(r"^Angebot an ", e)
    if m:
        R.offers.add(short)
        return [f"{PFX}offer_{short} = yes"]
    m = re.match(r"^Einfluss ([+-]\d+) % in (.+?) `change_influence_percentage`$", e)
    if m:
        p, tgt = int(m.group(1)), m.group(2)
        if "Arabische-Liga" in tgt:
            return [f"set_temp_variable = {{ {PFX}influence_amount = {p} }}", f"{PFX}influence_arab_league = yes"]
        out = []
        for t in re.split(r",\s*", tgt):
            t = {"SYE": "YEM"}.get(t, t)
            out += [f"if = {{ limit = {{ country_exists = {t} }}",
                    "set_temp_variable = { tag_index = ROOT.id }", f"set_temp_variable = {{ influence_target = {t}.id }}",
                    f"set_temp_variable = {{ percent_change = {p} }}", "change_influence_percentage = yes", "}"]
        return out
    m = re.match(r"^Meinung (\w+) ([+-]\d+) `add_opinion_modifier`$", e)
    if m:
        return opinion(m.group(1), int(m.group(2)))
    m = re.match(r"^Forschungsbonus (\w+) \+(\d+) % ×(\d) `add_tech_bonus`$", e)
    if m:
        return [f"add_tech_bonus = {{ name = {fid.replace('EGY_1970_', PFX)} bonus = {fmt(int(m.group(2)) / 100)} uses = {m.group(3)} category = {m.group(1)} }}"]
    m = re.match(r"^Gebäude: \+(\d) (.+?) in (.+?) `([\w /]+?)`", e)
    if m:
        n, what, where, helpers = int(m.group(1)), m.group(2), m.group(3), m.group(4)
        states = [int(s) for s in re.findall(r"\b(\d{3,4})\b", where)]
        helpers = [h.strip() for h in helpers.split("/")]
        out = ["set_temp_variable = { skip_payment = 1 }"]
        if helpers == ["add_building_construction land_fort"]:
            for s in states:
                out.append(f"{s} = {{ add_building_construction = {{ type = bunker level = {n} instant_build = yes province = {{ all_provinces = yes limit_to_border = yes }} }} }}")
            out.append("clear_variable = skip_payment")
            return out
        per = max(1, n // len(states)) if len(helpers) == 1 else 1
        for s in states:
            for h in helpers:
                assert h in BUILD_HELPER_OK, h
                for _ in range(per):
                    out.append(f"{s} = {{ {h} = yes }}")
        out.append("set_temp_variable = { skip_payment = 0 }")
        return out
    m = re.match(r"^Flag `(\w+)`$", e)
    if m:
        R.flags.add(cid(m.group(1)))
        return [f"set_country_flag = {cid(m.group(1))}"]
    m = re.match(r"^Einkommensteuersatz ([+-]\d+) Pkt", e)
    if m:
        return [f"set_temp_variable = {{ pop_change = {int(m.group(1))} }}", "modify_population_tax_rate_effect = yes"]
    m = re.match(r"^Unternehmenssteuersatz ([+-]\d+) Pkt", e)
    if m:
        return [f"set_temp_variable = {{ corp_change = {int(m.group(1))} }}", "modify_corporate_tax_rate_effect = yes"]
    if e.startswith("Handelsgesetz eine Stufe offener"):
        return ["increase_exports = yes"]
    if e.startswith("Handelsgesetz eine Stufe geschlossener"):
        return ["decrease_exports = yes"]
    if e.startswith("Konjunktur eine Stufe besser"):
        return ["increase_economic_growth = yes"]
    m = re.match(r"^Produktivität ([+-]\d+) `flat_productivity_change_effect`$", e)
    if m:
        return [f"set_temp_variable = {{ temp_productivity_change = {int(m.group(1))} }}", "flat_productivity_change_effect = yes"]
    m = re.match(r"^\S+ (?:[+−]1) Stufe `(\w+)`$", e)
    if m:
        return [f"{m.group(1)} = yes"]
    m = re.match(r"^Auslandsvermögen ([+-][\d.]+) % BIP", e)
    if m:
        return gdp(f"{PFX}change_intinv_gdp_share", float(m.group(1)) / 100)
    m = re.match(r"^Neue Fraktion: .+? \(Meinung (\d+)\) `add_ideas`(?: `(\w+)`)?$", e)
    if m:
        fac = m.group(2) or {"Kader": "communist_cadres", "Ölindustrie": "fossil_fuel_industry"}[re.match(r"^Neue Fraktion: (\S+)", e).group(1)]
        return [f"if = {{ limit = {{ NOT = {{ has_idea = {fac} }} }}", f"add_ideas = {fac}",
                f"set_variable = {{ {fac}_opinion = {m.group(1)} }}", "hidden_effect = { initialize_internal_faction_dynamic_modifiers = yes }", "}"]
    m = re.match(r"^Treasury ([+-][\d.,]+) % BIP", e)
    if m:
        v = num(m.group(1)) / 100
        return gdp(f"{PFX}receive_gdp_share", v) if v > 0 else gdp(f"{PFX}pay_gdp_share", -v)
    m = re.match(r"^Schaltet Decisions „(.+?)“ frei", e)
    if m:
        k = f"unlock_{slug(m.group(1))}"
        R.tt[f"{PFX}{k}_tt"] = f"Unlocks decisions: §Y{m.group(1)}§!"
        return [f"custom_effect_tooltip = {PFX}{k}_tt"]
    m = re.match(r"^(.+?) wird Koalitionspartner \(`add_col_one` (\d+)\)", e)
    if m:
        return [f"set_temp_variable = {{ add_col_one = {m.group(2)} }}", "add_coalition_members_effect = yes"]
    R.unhandled.append((fid, e))
    return [f"# UNHANDLED: {e}"]


# ------------------------------------------------------------- manual lines
def social_con(n):
    return [f"set_temp_variable = {{ temp_modify_social_con_government = {n} }}", "modify_social_conservatism_government = yes"]


def literacy(p):
    return [f"set_temp_variable = {{ LR_change = {fmt(p / 100)} }}", "update_literacy_rate = yes"]


def coptic(n):
    return [f"set_temp_variable = {{ coptic_opinion_change = {n} }}", "modify_coptic_opinion_effect = yes"]


def elections(years=None):
    return [f"{PFX}allow_elections = yes"]


def res(state, r, n):
    return [f"{state} = {{ add_resource = {{ type = {r} amount = {n} }} }}"]


def cosmetic(tag, name, adj):
    R.cosmetic[tag] = (name, adj)
    return [f"set_cosmetic_tag = {tag}"]


def cw_join(al):
    return [f"set_temp_variable = {{ mdcw_cw_new_alignment = {al} }}", "set_temp_variable = { mdcw_cw_t_free = 1 }", "mdcw_cw_change_alignment = yes"]


def unban_all_except(*banned):
    out = []
    for i in range(24):
        if i in banned:
            continue
        out.append(f"set_variable = {{ party_banned_array^{i} = 0 }}")
    return ["hidden_effect = {"] + out + ["update_dirty_politicsview_expanded = yes", "}", tt("parties_legalised", "All parties except the jihadist movements may now organise legally.")]


def ban_all_but_ruling():
    return [tt("parties_banned", "§RAll other parties are banned.§!"), "hidden_effect = {",
            "for_loop_effect = { end = 24 value = p",
            "if = { limit = { NOT = { check_variable = { ruling_party = p } } } set_variable = { party_banned_array^p = 1 } }", "}",
            "update_dirty_politicsview_expanded = yes", "}"]


def flag(f):
    R.flags.add(f)
    return [f"set_country_flag = {f}"]


MAN = {
    ("shadow_of_the_naksa", "Aktiviert die drei Länder-Modifier „Der ägyptische Staat“, „Wirtschaftsmodell“, „Streitkräfte“ (Startwerte 0) `add_dynamic_modifier`"):
        [f"add_dynamic_modifier = {{ modifier = {PFX}state_modifier }}", f"add_dynamic_modifier = {{ modifier = {PFX}economy_modifier }}",
         f"add_dynamic_modifier = {{ modifier = {PFX}armed_forces_modifier }}"],
    ("doctors_from_moscow", "Nasser bleibt: Leader ohne Ablaufdatum neu erstellt, Trait „Ailing Rais“ `create_country_leader`"):
        lambda f: (R.traits.add("Ailing Rais"), [tt("nasser_stays", "§YGamal Abdel Nasser§! remains President. His ill health is now a permanent concern."),
                   "hidden_effect = {", "retire_country_leader = yes",
                   'create_country_leader = { name = "Gamal Abdel Nasser" picture = "gfx/leaders/EGY/1970/nasser.dds" ideology = neutral_Social traits = { neutrality_neutral_Social COLDWAR_EGY_ailing_rais } }',
                   "}"] + flag(f"{PFX}nasser_ailing"))[1],
    ("the_heir_apparent", "Anwar as-Sadat wird Präsident (ASU) `create_country_leader`"):
        [tt("sadat_president", "§YAnwar as-Sadat§! becomes President of Egypt."), "hidden_effect = {", "retire_country_leader = yes",
         'create_country_leader = { name = "Anwar as-Sadat" picture = "gfx/leaders/EGY/1970/sadat.dds" ideology = neutral_Social traits = { neutrality_neutral_Social } }', "}"],
    ("a_president_in_his_own_right", "Leader erhält Trait „Consolidated Rule“"):
        lambda f: (R.traits.add("Consolidated Rule"), ["add_country_leader_trait = COLDWAR_EGY_consolidated_rule"])[1],
    ("a_president_in_his_own_right", "Löscht `EGY_1970_succession_open`"): [f"clr_country_flag = {PFX}succession_open"],
    ("open_the_platforms", "Wahlen erlaubt, Turnus 60 Monate `set_politics`"): elections(5),
    ("open_the_platforms", "Alle Parteien legal außer 10/11 `party_banned_array`"): unban_all_except(10, 11),
    ("one_party_one_nation", "Wahlen bleiben gesperrt"): [f"{PFX}suspend_elections = yes"],
    ("na_the_brioni_spirit", "Meinung SER (Jugoslawien) +25 `add_opinion_modifier`"): opinion("SER", 25),
    ("tag_the_yugoslav_model", "Meinung SER (Jugoslawien) +25 `add_opinion_modifier`"): opinion("SER", 25),
    ("na_the_brioni_spirit", "Verbessertes Handelsabkommen mit RAJ `set_improved_trade_agreement`"):
        ["if = { limit = { country_exists = RAJ }", "set_temp_variable = { receiver_nation = ROOT.id }", "set_temp_variable = { sender_nation = RAJ.id }", "set_improved_trade_agreement = yes", "}"],
    ("tag_the_yugoslav_model", "Verbessertes Handelsabkommen `set_improved_trade_agreement`"):
        ["if = { limit = { country_exists = SER }", "set_temp_variable = { receiver_nation = ROOT.id }", "set_temp_variable = { sender_nation = SER.id }", "set_improved_trade_agreement = yes", "}"],
    ("na_legalise_the_brotherhood", "Zusätzlich: Verbot der Muslimbrüder aufgehoben `party_banned_array`"):
        ["set_variable = { party_banned_array^12 = 0 }", "hidden_effect = { update_dirty_politicsview_expanded = yes }", tt("mb_legal", "The §YMuslim Brotherhood§! is no longer banned.")],
    ("na_the_new_class", "Zusätzlich verfügbar nur mit `EGY_1970_infitah_flag`"): [],
    ("na_the_free_economy", "Nur mit `EGY_1970_infitah_flag`"): [],
    ("na_lead_the_nam", "Cold War: „Non-Aligned Summit Diplomacy“ kostet −25 PP weniger `mdcw_cw_` decision"):
        flag(f"{PFX}nam_leader") + [tt("nam_leader", "Egypt is recognised as a leader of the Non-Aligned Movement.")],
    ("em_advisers_in_every_ministry", "SOV-Einfluss in Ägypten +5 % (`change_influence_percentage` im SOV-Scope)"):
        ["if = { limit = { country_exists = SOV }", "set_temp_variable = { tag_index = SOV.id }", "set_temp_variable = { influence_target = ROOT.id }",
         "set_temp_variable = { percent_change = 5 }", "change_influence_percentage = yes", "}"],
    ("em_power_to_the_councils", "Zusätzlich: Gewerkschaften ≥ 70"): [],
    ("em_power_to_the_islamic_front", "Zusätzlich: Datum ≥ 1979"): [],
    ("em_power_to_the_guardians", "Zusätzlich: Datum ≥ 1979; Militär −20"): faction("the_military", -20),
    ("em_join_the_socialist_camp", "Cold War: Beitritt zum Sowjetblock bzw. Pekinger Lager ohne PP-Kosten (`mdcw_cw_new_alignment`, `mdcw_cw_t_free`) `mdcw_cw_change_alignment`"):
        ["if = { limit = { mdcw_cw_can_join_soviet = yes }"] + cw_join(2) + ["}", "else_if = { limit = { mdcw_cw_can_join_beijing = yes }"] + cw_join(3) + ["}"],
    ("we_power_to_the_wafd", "Nur mit `EGY_1970_platforms_open`"): [],
    ("we_power_to_the_liberals", "Nur mit `EGY_1970_platforms_open`"): [],
    ("we_power_to_socialist_labour", "Nur mit `EGY_1970_platforms_open`"): [],
    ("we_the_imf_standby", "Schulden −2 % BIP `modify_debt_effect`"): gdp(f"{PFX}change_debt_gdp_share", -0.02),
    ("we_step_by_step_diplomacy", "Schaltet „Kissinger's Shuttle“ im Bereich Supermächte ohne Voraussetzung frei"):
        flag(f"{PFX}us_mediation") + [tt("us_mediation_step", "American step-by-step diplomacy makes §YIsrael§! far more willing to accept §YKilometre 101§! and §YThe Sinai Agreement§!.")],
    ("we_join_the_free_world", "Cold War: Beitritt zum Westblock ohne PP-Kosten `mdcw_cw_change_alignment`"):
        ["if = { limit = { mdcw_cw_can_join_west = yes }"] + cw_join(1) + ["}"],
    ("join_the_soviet_bloc", "Cold War: Sowjetblock ohne PP-Kosten `mdcw_cw_change_alignment`"):
        ["if = { limit = { mdcw_cw_can_join_soviet = yes }"] + cw_join(2) + ["}"],
    ("join_the_western_bloc", "Cold War: Westblock ohne PP-Kosten `mdcw_cw_change_alignment`"):
        ["if = { limit = { mdcw_cw_can_join_west = yes }"] + cw_join(1) + ["}"],
    ("sa_the_hisba", "Sozialer Konservatismus +10"): social_con(10),
    ("sa_power_to_the_jamaat", "Zusätzlich: Militär −20, Stabilität −10 % (Zeitidee) – ein Umsturz von unten"):
        faction("the_military", -20) + [f"add_timed_idea = {{ idea = {reg_idea('Upheaval from Below', [('stability_factor', -0.10)], 365)} days = 365 }}"],
    ("sa_the_islamic_order", "Cosmetic Tag „Islamic State of Egypt“ `set_cosmetic_tag`"): cosmetic("COLDWAR_EGY_ISLAMIC_STATE", "Islamic State of Egypt", "Egyptian"),
    ("sa_dar_al_islam", "„Islamic Government“ → „Dar al-Islam“: Stabilität +5 %, PP-Faktor +5 %, Forschung −3 % `swap_ideas`"):
        lambda f: [f"swap_ideas = {{ remove_idea = {idea_id('Islamic Government')} add_idea = {reg_idea('Dar al-Islam', [('stability_factor', 0.05), ('political_power_factor', 0.05), ('research_speed_factor', -0.03)])} }}"],
    ("nt_pharaonic_heritage", "Meinung aller Arabische-Liga-Staaten −5 `add_opinion_modifier`"):
        (lambda: (R.opinions.__setitem__(f"{PFX}negative_5", -5), [f"every_country = {{ limit = {{ {PFX}is_arab_league_state = yes NOT = {{ tag = ROOT }} }} add_opinion_modifier = {{ target = ROOT modifier = {PFX}negative_5 }} }}"])[1])(),
    ("nt_restore_the_crown", "Nur mit Royalisten ≥ 15 % und Militär ≥ 60"): [],
    ("asu_the_graduate_guarantee", "Alphabetisierung +2,5 % `update_literacy_rate`"): literacy(2.5),
    ("asu_the_believer_president", "Sozialer Konservatismus +5 `modify_social_conservatism_government`"): social_con(5),
    ("asu_dissolve_the_union", "ASU-Programm entfernt `remove_dynamic_modifier`"): [f"remove_dynamic_modifier = {{ modifier = {PFX}asu_programme }}"],
    ("asu_the_second_era", "Datum ≥ 1975 empfohlen; schaltet die zweite Weiche frei"): [],
    ("asu_the_rais_for_life", "Amtszeitbegrenzung aufgehoben: PP-Faktor +10 % `add_country_leader_trait`"):
        lambda f: (R.traits.add("Rais for Life"), ["add_country_leader_trait = COLDWAR_EGY_rais_for_life"])[1],
    ("asu_heavy_industry_first", "215 Cairo: Stahl +2 `add_resource`"): res(215, "steel", 2),
    ("asu_the_eastern_flank", "Fraktion „Arab Joint Defense Command“: Kriegsunterstützung +3 % für alle Mitglieder (Event)"):
        ["every_country = {", "limit = { is_in_faction_with = ROOT NOT = { tag = ROOT } }", "add_war_support = 0.03", f"country_event = {{ id = {NS}.10 }}", "}",
         tt("eastern_flank", "All members of our faction gain §G+3%§! war support.")],
    ("tp_growth_first", "Schulden +1 % BIP `modify_debt_effect`"): gdp(f"{PFX}change_debt_gdp_share", 0.01),
    ("tp_return_power_to_the_assembly", "Wahlen erlaubt `set_politics`"): elections(),
    ("tp_budget_discipline", "Schulden −0,5 % BIP `modify_debt_effect`"): gdp(f"{PFX}change_debt_gdp_share", -0.005),
    ("tp_energy_price_reform", "Energieverbrauch Bevölkerung −5 % `pop_energy_use_multiplier`"): dyn_change("tp_programme", [("pop_energy_use_multiplier", -0.05)], modname=f"{PFX}tp_programme"),
    ("tp_technical_education", "Alphabetisierung +2 % `update_literacy_rate`"): literacy(2),
    ("mb_the_guidance_office", "Sozialer Konservatismus +10 `modify_social_conservatism_government`"): social_con(10),
    ("mb_electoral_islam", "Wahlen erlaubt `set_politics`"): elections(),
    ("mb_al_dawa_magazine", "Non-Aligned-Kampagnenkosten −15 % `nonaligned_outlook_campaign_cost_modifier`"):
        dyn_change("mb_programme", [("nonaligned_outlook_campaign_cost_modifier", -0.15)], modname=f"{PFX}mb_programme"),
    ("mb_gradual_islamisation", "Sozialer Konservatismus +5"): social_con(5),
    ("mb_the_secret_apparatus", "Terror-Erkennung +10 % `terror_threat_detection_modifier`"):
        dyn_change("mb_programme", [("terror_threat_detection_modifier", 0.10)], modname=f"{PFX}mb_programme"),
    ("mb_end_the_jahiliyya", "Sozialer Konservatismus +10"): social_con(10),
    ("mb_codify_the_sharia", "Sozialer Konservatismus +15"): social_con(15),
    ("mb_the_islamic_order", "Cosmetic Tag „Islamic Republic of Egypt“ `set_cosmetic_tag`"): cosmetic("COLDWAR_EGY_ISLAMIC_REPUBLIC", "Islamic Republic of Egypt", "Egyptian"),
    ("mb_an_islamic_curriculum", "Alphabetisierung +2 % `update_literacy_rate`"): literacy(2),
    ("mb_the_coptic_compact", "Koptische Meinung +10 `modify_coptic_opinion_effect`"): coptic(10),
    ("mb_the_dhimma_laws", "Koptische Meinung −15 `modify_coptic_opinion_effect`"): coptic(-15),
    ("tag_al_ahali", "Non-Aligned-Kampagnenkosten −15 %"): dyn_change("tag_programme", [("nonaligned_outlook_campaign_cost_modifier", -0.15)], modname=f"{PFX}tag_programme"),
    ("tag_open_elections", "Wahlen erlaubt `set_politics`"): elections(),
    ("tag_free_education_restored", "Alphabetisierung +2,5 %"): literacy(2.5),
    ("nb_rule_through_the_umdas", "Zentralisierung −1 `decrease_centralization`"): ["decrease_centralization = yes"],
    ("nb_the_notables_assembly", "Wahlen erlaubt `set_politics`"): elections(),
    ("nb_family_and_faith", "Sozialer Konservatismus +5"): social_con(5),
    ("nb_balanced_budgets", "Schulden −1 % BIP `modify_debt_effect`"): gdp(f"{PFX}change_debt_gdp_share", -0.01),
    ("fe_minimal_regulations", "Regulierungsgesetz → `minimal_regulations` `add_ideas`"): [f"{PFX}set_regulation_law_minimal = yes"],
    ("fn_clean_industry", "Umweltgesetz → `partial_environmental_protections` `add_ideas`"): [f"{PFX}set_environment_law_partial = yes"],
    ("fn_stockholm_1972", "Handelsmeinung +5 % `trade_opinion_factor`"): dyn_change("fn_programme", [("trade_opinion_factor", 0.05)], modname=f"{PFX}fn_programme"),
    ("cp_files_on_everyone", "Terror-Erkennung +15 % `terror_threat_detection_modifier`"): dyn_change("cp_programme", [("terror_threat_detection_modifier", 0.15)], modname=f"{PFX}cp_programme"),
    ("cp_soviet_specialists_in_helwan", "215: Stahl +3 `add_resource`"): res(215, "steel", 3),
    ("cp_mass_literacy_campaign", "Alphabetisierung +5 % `update_literacy_rate`"): literacy(5),
    ("ecp_the_peoples_republic", "Cosmetic Tag „People's Republic of Egypt“ `set_cosmetic_tag`"): cosmetic("COLDWAR_EGY_PEOPLES_REPUBLIC", "People's Republic of Egypt", "Egyptian"),
    ("ecp_red_universities", "Alphabetisierung +2,5 %"): literacy(2.5),
    ("wc_abolish_the_bureaucracy", "Bürokratiegesetz −1 (Ideen bureau_0X) `swap_ideas`"): ["decrease_centralization = yes"],
    ("wc_dissolve_the_mukhabarat", "Fraktion Mukhabarat entfernt `remove_ideas`"):
        ["if = { limit = { has_idea = intelligence_community }", "remove_ideas = intelligence_community", "clear_variable = intelligence_community_opinion", "}"],
    ("misr_managed_platforms", "Wahlen erlaubt, Wahlschwelle erhöht `modify_election_threshold`"): elections() + ["set_temp_variable = { threshold_change = 0.05 }", "modify_election_threshold = yes"],
    ("misr_patriotic_media", "Emerging-Kampagnenkosten −15 % `emerging_outlook_campaign_cost_modifier`"):
        dyn_change("misr_programme", [("emerging_outlook_campaign_cost_modifier", -0.15)], modname=f"{PFX}misr_programme"),
    ("misr_loyal_governors", "Zentralisierung +1"): ["increase_centralization = yes"],
    ("misr_energy_sovereignty", "214: Öl +4 `add_resource`"): res(214, "oil", 4),
    ("irf_the_islamic_revolution_of_the_nile", "Cosmetic Tag „Islamic Republic of Egypt“ `set_cosmetic_tag`"): cosmetic("COLDWAR_EGY_ISLAMIC_REPUBLIC", "Islamic Republic of Egypt", "Egyptian"),
    ("irf_an_islamic_consultative_assembly", "Wahlen erlaubt `set_politics`"): elections(),
    ("grd_the_basij", "Rekrutierungsgesetz +1 Stufe `increase_conscription_effect`"): ["increase_conscription_effect = yes"],
    ("ndp_controlled_pluralism", "Wahlen erlaubt, Opposition legal außer 10/11 `set_politics`"): elections() + unban_all_except(10, 11),
    ("ndp_the_gulf_of_suez_oil_boom", "214: Öl +4, 219: Öl +3 `add_resource`"): res(214, "oil", 4) + res(219, "oil", 3),
    ("ndp_expand_the_universities", "Alphabetisierung +2 %"): literacy(2),
    ("ndp_the_jerusalem_initiative", "Bei Annahme: Flag `EGY_1970_peace_with_israel`, USA +25, alle Arabische-Liga-Staaten −30, Suspendierung aus der Liga (Event)"):
        [tt("jerusalem_consequences", "If Israel accepts: the §YUnited States§! improve their opinion of us (§G+25§!), every Arab League state worsens its opinion (§R-30§!), and Egypt is §Rsuspended from the Arab League§!.")],
    ("ndp_bright_star", "Armee-Erfahrung +25 `army_experience`"): ["army_experience = 25"],
    ("ndp_mediterranean_friends", "Handelsabkommen mit FRA, ITA `set_improved_trade_agreement`"):
        sum([[f"if = {{ limit = {{ country_exists = {t} }}", "set_temp_variable = { receiver_nation = ROOT.id }", f"set_temp_variable = {{ sender_nation = {t}.id }}", "set_improved_trade_agreement = yes", "}"] for t in ("FRA", "ITA")], []),
    ("wafd_the_spirit_of_1923", "Wahlen erlaubt `set_politics`"): elections(),
    ("wafd_crescent_and_cross", "Koptische Meinung +15 `modify_coptic_opinion_effect`"): coptic(15),
    ("wafd_secular_courts", "Korruption −1 Stufe"): ["decrease_corruption = yes"],
    ("lib_light_regulations", "Regulierungsgesetz → `light_regulations` `add_ideas`"): [f"{PFX}set_regulation_law_light = yes"],
    ("lib_civil_liberties_act", "Wahlen erlaubt `set_politics`"): elections(),
    ("lib_decentralise_the_governorates", "Zentralisierung −1 `decrease_centralization`"): ["decrease_centralization = yes"],
    ("azh_the_saudi_model", "Sozialer Konservatismus +10"): social_con(10),
    ("azh_sharia_courts", "Sozialer Konservatismus +10"): social_con(10),
    ("azh_the_dhimma_question", "Koptische Meinung −15 `modify_coptic_opinion_effect`"): coptic(-15),
    ("azh_the_azhar_university_system", "Alphabetisierung +2,5 % `update_literacy_rate`"): literacy(2.5),
    ("ij_the_gamaa_of_upper_egypt", "Sozialer Konservatismus +10"): social_con(10),
    ("ij_abolish_the_parties", "Alle anderen Parteien verboten `ban_party_scripted_call`"): ban_all_but_ruling(),
    ("ij_war_on_the_occupier", "Kriegsziel gegen ISR, falls nicht im Krieg `create_wargoal`"):
        ["if = { limit = { country_exists = ISR NOT = { has_war_with = ISR } }", "create_wargoal = { type = annex_everything target = ISR }", "}"],
    ("arm_fawzis_total_mobilisation", "Rekrutierungsgesetz +1 Stufe `increase_conscription_effect`"): ["increase_conscription_effect = yes"],
    ("arm_the_general_intelligence_directorate", "Terror-Erkennung +10 %"): dyn_change("arm_programme", [("terror_threat_detection_modifier", 0.10)], modname=f"{PFX}arm_programme"),
    ("arm_civilian_handover", "Wahlen erlaubt `set_politics`"): elections(),
    ("arm_the_arab_military_pact", "Fraktionsmitgliedern: Angebot gemeinsames Oberkommando (Event)"): lambda f: (R.offers.add("arm_the_arab_military_pact"), [f"{PFX}offer_arm_the_arab_military_pact = yes"])[1],
    ("ye_pharaonic_nationalism", "Koptische Meinung +10 `modify_coptic_opinion_effect`"): coptic(10),
    ("ye_national_youth_service", "Rekrutierungsgesetz +1 Stufe `increase_conscription_effect`"): ["increase_conscription_effect = yes"],
    ("ye_the_unity_of_the_nile_valley", "Ansprüche auf 220–225 (Sudan) `add_state_claim`"): [f"add_state_claim = {s}" for s in range(220, 226)],
    ("rcc_militarise_society", "Rekrutierungsgesetz +1 Stufe `increase_conscription_effect`"): ["increase_conscription_effect = yes"],
    ("mon_the_return_of_the_king", "Cosmetic Tag „Kingdom of Egypt“ `set_cosmetic_tag`"): cosmetic("COLDWAR_EGY_KINGDOM", "Kingdom of Egypt", "Egyptian"),
    ("mon_a_constitutional_monarchy", "Wahlen erlaubt `set_politics`"): elections(),
    ("mon_king_of_egypt_and_the_sudan", "Ansprüche auf 220–222 `add_state_claim`"): [f"add_state_claim = {s}" for s in range(220, 223)],
    ("irf_the_oil_of_the_revolution", "214: Öl +3 `add_resource`"): res(214, "oil", 3),
    ("irf_cultural_revolution", "Sozialer Konservatismus +10"): social_con(10),
    ("fn_green_assembly", "Wahlen erlaubt `set_politics`"): elections(),
    ("fn_work_with_the_dam", "217: Wasserkraft +0,5 GW `add_hydroelectric_energy_production_effect`"):
        ["217 = { set_temp_variable = { electric_addition = 0.5 } add_hydroelectric_energy_production_effect = yes }"],
    ("ij_the_blind_sheikh", "Sozialer Konservatismus +10"): social_con(10),
    ("wc_council_schools", "Alphabetisierung +2,5 %"): literacy(2.5),
    ("wc_council_democracy", "Wahlen erlaubt `set_politics`"): elections(),
    ("ye_a_national_republic", "Wahlen erlaubt `set_politics`"): elections(),
    ("the_war_of_attrition", "Armee-Erfahrung +25 `army_experience`"): ["army_experience = 25"],
    ("commandos_across_the_canal", "Armee-Erfahrung +25"): ["army_experience = 25"],
    ("accept_the_ceasefire", "Bei Annahme: Stabilität +5 %, Kriegsunterstützung −5 %, USA +10, Flag `EGY_1970_ceasefire`"):
        [tt("ceasefire_accept", "If Israel accepts: the war ends with the current front line, §G+5%§! stability, §R-5%§! war support and better relations with the §YUnited States§!.")],
    ("accept_the_ceasefire", "Bei Ablehnung: Kriegsunterstützung +5 %"): [tt("ceasefire_decline", "If Israel declines: §G+5%§! war support.")],
    ("the_crossing", "Entfernt „Shadow of the Naksa“ `remove_ideas`"): [f"remove_ideas = {PFX}shadow_of_the_naksa"],
    ("reopen_the_suez_canal", "Entfernt „The Closed Canal“"): [f"remove_ideas = {PFX}the_closed_canal"],
    ("honour_regained", "Feiertag 6. Oktober: Militär-Mindestmeinung +10 dauerhaft"):
        lambda f: [f"add_ideas = {reg_idea('Armed Forces Day', [('if_the_military_minimum_opinion', 10)])}"],
    ("the_uar_reborn", "MD-Formable VAR (`special_formable_id` 103) `commit_special_formable`"):
        ["set_global_flag = COLDWAR_EGY_uar_reborn", "mark_formed_country_formable = yes",
         "if = { limit = { has_government = communism } set_cosmetic_tag = UAR_communism }",
         "else_if = { limit = { has_government = nationalist } set_cosmetic_tag = UAR_nationalist }",
         "set_temp_variable = { special_formable_id = 103 }", "commit_special_formable = yes", "custom_effect_tooltip = create_uar_effect_tt"],
    ("the_uar_reborn", "`update_arabic_country_gdp_total_effect`"): ["update_arabic_country_gdp_total_effect = yes"],
    ("kissingers_shuttle", "Halbiert die Kosten von „Kilometre 101“ und „The Sinai Agreement“"):
        flag(f"{PFX}us_mediation") + [tt("us_mediation", "American mediation makes §YIsrael§! far more willing to accept §YKilometre 101§! and §YThe Sinai Agreement§!.")],
    ("infitah", "Korruptionschance +1 `increase_corruption_chance`"): ["increase_corruption_chance = yes"],
    ("the_high_dam_completed", "217: Wasserkraft +2,1 GW `hydroelectric_energy_production_var`"):
        ["217 = { set_temp_variable = { electric_addition = 2.1 } add_hydroelectric_energy_production_effect = yes }"],
    ("cotton_is_king", "Nur mit MD-Agrarsystem: Cash-Crop-Anteil +10 % `AGRI_price_change_all_crops`"):
        ["if = { limit = { is_agrarian_economy = yes }", "set_temp_variable = { allocation_change = -0.1 }", "AGRI_shift_crop_allocation = yes", "}"],
    ("the_gift_of_the_nile", "„The High Dam“ → „Gift of the Nile“: Agrarproduktivität +15 %, Stabilität +3 % `swap_ideas`"):
        lambda f: [f"swap_ideas = {{ remove_idea = {idea_id('The High Dam')} add_idea = {reg_idea('Gift of the Nile', [('agricolture_productivity_modifier', 0.15), ('stability_factor', 0.03)])} }}"],
    ("helwan_steel", "215 Cairo: Stahl +4 `add_resource`"): res(215, "steel", 4),
    ("helwan_steel", "Mit „The Moscow Anchor“ oder Emerging-Regierung: Kosten halbiert (sowjetischer Kredit)"):
        ["if = { limit = { OR = { has_completed_focus = COLDWAR_EGY_the_moscow_anchor has_government = communism } }",
         "set_temp_variable = { COLDWAR_EGY_gdp_share = 0.006 }", "COLDWAR_EGY_receive_gdp_share = yes", "}",
         tt("helwan_soviet_credit", "With §YThe Moscow Anchor§! or an Emerging government a Soviet credit pays half of the cost.")],
    ("nag_hammadi_aluminium", "217: Aluminium +6 `add_resource`"): res(217, "aluminium", 6),
    ("oil_of_the_gulf_of_suez", "214: Öl +6, 219: Öl +4 `add_resource`"): res(214, "oil", 6) + res(219, "oil", 4),
    ("rebuild_the_armed_forces", "Armee-Erfahrung +50"): ["army_experience = 50"],
    ("rebuild_the_armed_forces", "Kommandomacht +20 `add_command_power`"): ["add_command_power = 20"],
    ("end_the_amer_clique", "Offiziersausbildung +1 Stufe `increase_officer_training_level`"): ["increase_officer_training_level = yes"],
    ("the_republican_guard", "Militär-Mindestmeinung +10 `if_the_military_minimum_opinion`"):
        dyn_change("armed_forces", [("if_the_military_minimum_opinion", 10)]),
    ("rebuild_the_air_force", "Luftwaffen-Erfahrung +25 `air_experience`"): ["air_experience = 25"],
    ("missile_boats", "Marine-Erfahrung +15 `navy_experience`"): ["navy_experience = 15"],
    ("blockade_bab_el_mandeb", "Marine-Erfahrung +15"): ["navy_experience = 15"],
}

# generic manual line patterns (exact text, any focus)
MANL = {}
for t, code in [("Korruption −1 Stufe `decrease_corruption`", ["decrease_corruption = yes"]),
                ("Korruption +1 Stufe `increase_corruption`", ["increase_corruption = yes"]),
                ("Korruptionschance +1 `increase_corruption_chance`", ["increase_corruption_chance = yes"]),
                ("Zentralisierung +1 `increase_centralization`", ["increase_centralization = yes"]),
                ("Zentralisierung −1 `decrease_centralization`", ["decrease_centralization = yes"]),
                ("Wahlen erlaubt `set_politics`", elections()),
                ("Rekrutierungsgesetz +1 Stufe `increase_conscription_effect`", ["increase_conscription_effect = yes"]),
                ("Alphabetisierung +2,5 %", literacy(2.5)), ("Alphabetisierung +2 %", literacy(2)),
                ("Sozialer Konservatismus +10", social_con(10))]:
    MANL[t] = code


# event-backed lines: (focus, line) -> code
def event_line(n, days=0, extra=()):
    R.events.add(n)
    d = f" days = {days}" if days else ""
    return list(extra) + [f"country_event = {{ id = {NS}.{n}{d} }}"]


EVLINES = {
    "shadow_of_the_naksa": event_line(1),
    "the_succession_question": event_line(2),
    "the_corrective_revolution": event_line(3, 14),
    "we_the_imf_standby": event_line(4, 30, [f"set_variable = {{ {PFX}subsidy_restore = 0.05 }}"]),
    "ndp_subsidy_reform": event_line(4, 30, [f"set_variable = {{ {PFX}subsidy_restore = 0.05 }}"]),
    "cut_the_subsidies": event_line(4, 30, [f"set_variable = {{ {PFX}subsidy_restore = 0.075 }}"]),
    "mb_islamic_investment_companies": event_line(5, 1095),
    "azh_the_dhimma_question": event_line(6, 7),
    "ndp_cheap_order": flag(f"{PFX}cheap_order") + [tt("csf_risk", "Underpaid conscripts may one day §Rmutiny§!.")],
    "the_uar_reborn": ["news_event = { id = COLDWAR_EGY.12 hours = 6 }"],
}
R.events.update({7, 8, 9, 10, 11, 12})


# special idea lines
def _rais_health(f):
    iid = reg_idea("The Rais's Fragile Health", [("political_power_factor", 0.10), ("stability_factor", 0.05)], 1095)
    R.events.add(9)
    return [f"add_timed_idea = {{ idea = {iid} days = 1095 }}",
            tt("rais_health", "Each year the President's heart may §Rfail him§!.")]


def _egyptian_model(f):
    a = reg_idea("Egyptian Model: Socialism", [("production_speed_buildings_factor", 0.05), ("stability_factor", 0.03)])
    b = reg_idea("Egyptian Model: Infitah", [("office_park_income_tax_modifier", 0.08), ("return_on_investment_modifier", 0.025)])
    c = reg_idea("Egyptian Model: Islamic Economy", [("social_cost_multiplier_modifier", -0.08), ("stability_factor", 0.03)])
    return [f"if = {{ limit = {{ OR = {{ has_country_flag = {PFX}infitah_flag has_government = democratic }} }} add_ideas = {b} }}",
            f"else_if = {{ limit = {{ OR = {{ has_government = fascism neutrality_neutral_muslim_brotherhood_are_in_power = yes }} }} add_ideas = {c} }}",
            f"else = {{ add_ideas = {a} }}"]


MAN[("doctors_from_moscow", "Idee „The Rais's Fragile Health“: PP-Faktor +10 % `political_power_factor`, Stabilität +5 % `stability_factor`; jährliches Gesundheits-Event kann ihn trotzdem töten (1095 Tage `add_timed_idea`)")] = _rais_health
MAN[("an_egyptian_economic_model", "Idee „Egyptian Model“: je nach Weg: Sozialismus (Baugeschw. +5 %, Stabilität +3 %) / Infitah (Büroeinkommen +8 %, ROI +0,25) / Islamisch (Sozialkosten −8 %, Stabilität +3 %) `add_ideas`")] = _egyptian_model
MAN[("ij_the_emirate", "Partei-Programm: Stabilität −5 % statt −10 %, Rekrutierung +2 % `EGY_1970_ij_programme`")] = \
    dyn_change("ij_programme", [("stability_factor", 0.05), ("conscription", 0.02)], modname=f"{PFX}ij_programme")
MAN[("sharia_as_a_principal_source", "Sozialer Konservatismus Regierung +10 `modify_social_conservatism_government`")] = social_con(10)
MAN[("the_secular_charter", "Sozialer Konservatismus Regierung −10 `modify_social_conservatism_government`")] = social_con(-10)
MAN[("expel_the_soviet_advisers", "Entfernt „Soviet Military Mission“ (Luftverteidigungsbonus fällt weg) `remove_ideas`")] = [f"remove_ideas = {PFX}soviet_military_mission"]
