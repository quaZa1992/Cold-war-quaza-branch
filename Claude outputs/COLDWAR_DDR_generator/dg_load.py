# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Loads the approved GDR design (v2, 18.10.2026): ddr_tree.json (foci, positions, effects), ddr_concept.json (systems,
# registries), page_data.json (English names and descriptions). The layout is final in the design: x/y are grid cells,
# `rel` is the anchor of relative_position_id (MD 2000 style).
from dg_common import *

T = json.load(open(os.path.join(DESIGN, "ddr_tree.json"), encoding="utf-8"))
C = None
P = json.load(open(os.path.join(DESIGN, "page_data.json"), encoding="utf-8"))
C = P["concept"]                                 # concept + registries (ideas with modifier lines, offers, uses)

FOCI = T["foci"]
BYID = {f["id"]: f for f in FOCI}
PAGE = {PFX + f["i"]: f for f in P["foci"]}
for f in FOCI:
    pg = PAGE[f["id"]]
    f["sec"] = f["section"]
    f["desc"] = pg["d"]
    f["hist"] = pg["h"]
    f["note"] = pg["o"]
    f["etext"] = [e[2] for e in pg["e"]]          # the English line of every effect (tooltips, review)
    f["bypass_text"] = pg["b"]
    assert len(f["etext"]) == len(f["eff"]), f["id"]

POS = {f["id"]: (f["x"], f["y"]) for f in FOCI}
ANCHOR = {f["id"]: f["rel"] for f in FOCI}
SECTIONS = P["sections"]                         # k, t (title), b (block), col, d, party, g (gate)
SECT = {s["k"]: s for s in SECTIONS}
ORDER = [s["k"] for s in SECTIONS]
BLOCKS = list(P["stats"]["blocks"].keys())
NAME2ID = {}
for f in FOCI:
    NAME2ID.setdefault(f["name"], f["id"])

IDEAS = T["ideas"]                               # id -> {name, mods, days, ...} (focus ideas, ladder steps, start spirits)
for k, v in C["ideas"].items():
    IDEAS.setdefault(k, v)
    IDEAS[k]["start"] = v.get("start", False)
    IDEAS[k]["desc"] = v.get("desc", "")
OFFERS = C["offers"]                             # id -> {tags, text}
EVENTS = C["events"]                             # id -> text
DECISIONS = C["decisions"]                       # id -> text
TRAITS = C["traits"]                             # id -> name
OPINIONS = {k: v[0] for k, v in C["opinions"].items()}
OPINION_NAMES = {k: v[1] for k, v in C["opinions"].items()}
LADDERS = C["ladders"]
PROGS = C["programmes"]                          # key -> {name, lines, total}
PARTY = {int(k): v for k, v in C["parties"].items() if v["leader"] != "-"}   # slots 8-12 stay empty (no Salafi/Shia paths)
LEADERS = C["leaders"]                           # (name, key, candidacy, death, profile, heirs)
LEADER_NAME = C["leader_names"]
USES = C["uses"]

# MD sub-ideologies: party index -> trigger base (`<base>_are_in_power`), MD sub-ideology id, outlook (MD government)
TRIG = {0: "western_autocrats", 1: "western_conservatism", 2: "western_liberals", 3: "western_social_democrats",
        4: "emerging_communist_state", 5: "emerging_anarchist_communism", 6: "emerging_reactionaries", 7: "emerging_autocracy",
        8: "emerging_moderate_shiite", 9: "emerging_hardline_shiite", 10: "salafist_kingdom", 11: "salafist_caliphate",
        12: "neutrality_neutral_muslim_brotherhood", 13: "neutrality_neutral_autocracy", 14: "neutrality_neutral_conservatism",
        15: "neutrality_neutral_oligarch", 16: "neutrality_neutral_libertarians", 17: "neutrality_neutral_green",
        18: "neutrality_neutral_social", 19: "neutrality_neutral_communism", 20: "nationalist_right_wing_populists",
        21: "nationalist_fascist", 22: "nationalist_military_junta", 23: "nationalist_monarchists"}
SUBIDEO = {0: "Western_Autocracy", 1: "conservatism", 2: "liberalism", 3: "socialism", 4: "communist_state",
           5: "anarchist_communism", 6: "Conservative", 7: "Autocracy", 8: "Mod_Vilayat_e_Faqih", 9: "Vilayat_e_Faqih",
           10: "Kingdom", 11: "Caliphate", 12: "Neutral_Muslim_Brotherhood", 13: "Neutral_Autocracy",
           14: "Neutral_conservatism", 15: "oligarchism", 16: "Neutral_Libertarian", 17: "Neutral_green",
           18: "neutral_Social", 19: "Neutral_Communism", 20: "Nat_Populism", 21: "Nat_Fascism", 22: "Nat_Autocracy",
           23: "Monarchist"}
GROUP_TRAIT = {range(0, 4): "western", range(4, 10): "emerging", range(10, 12): "salafist",
               range(12, 20): "neutrality", range(20, 24): "nationalist"}
GOV_OF = {0: "democratic", 1: "communism", 2: "fascism", 3: "neutrality", 4: "nationalist"}


def outlook_of(i):
    return 0 if i < 4 else 1 if i < 10 else 2 if i < 12 else 3 if i < 20 else 4


def ideology_trait(i):
    for r, g in GROUP_TRAIT.items():
        if i in r:
            return f"{g}_{SUBIDEO[i]}"


# faction ids of the design -> English names (MD internal factions)
FACTION = {"communist_cadres": "SED Nomenklatura", "intelligence_community": "MfS (Stasi)", "the_military": "NVA Command",
           "industrial_conglomerates": "Kombinat Directors", "labour_unions": "FDGB Trade Unions", "farmers": "LPG Cooperative Farmers",
           "the_clergy": "Protestant Church", "small_medium_business_owners": "Craftsmen & Semi-State Firms",
           "maritime_industry": "Baltic Shipyards", "defense_industry": "Arms Industry"}
FACTION_BY_NAME = {v: k for k, v in FACTION.items()}
# country dynamic modifier groups of the design
DYN = {"party_state": "The Party State", "planned_economy": "The Planned Economy", "nva": "The National People's Army",
       "mfs": "Shield and Sword", "socialist_camp": "The Socialist Camp"}
LEADER_KEYS = ["ulb", "hon", "sto", "mit", "hag", "hof", "lam", "kro", "kre", "mod"]
PARTY_SECTIONS = {v["section"]: k for k, v in PARTY.items() if v.get("section")}
