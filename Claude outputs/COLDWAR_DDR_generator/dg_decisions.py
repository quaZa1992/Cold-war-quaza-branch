# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Decision categories and decisions of the GDR 1970 tree: the Central Committee, the German Question, Moscow,
# the Five-Year Plans, Hard Currency (KoKo), the Housing Programme, the Kombinat contracts, the Military Council,
# talks with Moscow on leaving the Pact, and the Soviet side ("The German Comrades": endorse a change, Fraternal Assistance).
from dg_common import *
import dg_effects as E
import dg_offers as OF
import dg_avail as A
from dg_load import BYID, LEADER_KEYS, LEADER_NAME, PARTY
from dg_events import EV, SOV_HUMAN

CATS = []        # (key, name, desc, icon, priority, allowed, visible)
DECS = {}
DDR_T = ["original_tag = DDR"]
INIT = f"has_country_flag = {PFX}initialized"
SED = "emerging_communist_state_are_in_power = yes"


def cat(key, name, desc, icon, prio, allowed, visible):
    if allowed is DDR_T:
        visible = [INIT] + list(visible)
    CATS.append((key, name, desc, icon, prio, allowed, visible))
    LOC[key] = name
    LOC[key + "_desc"] = desc
    DECS[key] = []


def dec(category, key, name, desc, icon, effect, cost=0, visible=(), available=(), ai="base = 0", re_enable=None, once=False, extra=()):
    k = PFX + key
    LOC[k] = name
    LOC[k + "_desc"] = desc
    L = [f"{k} = {{", f"icon = {icon}"]
    if cost:
        L.append(f"cost = {cost}")
    if re_enable:
        L.append(f"days_re_enable = {re_enable}")
    L.append(f"fire_only_once = {'yes' if once else 'no'}")
    L += list(extra)
    if visible:
        L += ["visible = {"] + list(visible) + ["}"]
    if available:
        L += ["available = {"] + list(available) + ["}"]
    L += ["complete_effect = {", f'log = "[GetDateText]: [Root.GetName]: Decision {k}"'] + list(effect) + ["}"]
    L += ["ai_will_do = {"] + ai.split("\n") + ["}", "}", ""]
    DECS[category].append(L)


def tt(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def ttrig(key, text, body):
    LOC[f"{PFX}{key}_trig_tt"] = text
    return ["custom_trigger_tooltip = {", f"tooltip = {PFX}{key}_trig_tt"] + list(body) + ["}"]


def unlocked(key):
    return f"has_country_flag = {PFX}{key}_unlocked"


def av_lines(fid, drop=()):
    """the support conditions of a focus as decision conditions"""
    av = A.convert(BYID[PFX + fid])
    return [l for l in av.split("\n") if l.strip() and not any(d in l for d in drop)]


# ================================================================ the Central Committee
C = f"{PFX}cc_category"
cat(C, "The Central Committee",
    "The First Secretary is not overthrown - he is relieved by the Central Committee. Every candidacy prepared in the focus tree can be put to the plenum here. "
    "The candidate needs the support named in his candidacy; if the Soviet Union is led by a player, the Kremlin is consulted first and may veto him "
    "(the candidate must then wait 180 days).",
    "GFX_decision_category_generic_communism", 190, DDR_T, [unlocked("central_committee")])
for i, k in enumerate(LEADER_KEYS):
    name = LEADER_NAME[k]
    dec(C, f"convene_cc_{k}", f"Convene the Central Committee: {name}",
        f"The Politburo proposes §Y{name}§! to the Central Committee as First Secretary of the SED.",
        "GFX_decision_generic_political_discourse",
        [f"set_variable = {{ global.{PFX}cc_candidate = {i + 1} }}",
         "if = {", f"limit = {{ {SOV_HUMAN} }}",
         tt(f"cc_kremlin_{k}", f"The Kremlin is consulted first: if Moscow agrees, §Y{name}§! becomes First Secretary; if it vetoes, he must wait 180 days."),
         f"set_country_flag = {PFX}cc_pending", f"SOV = {{ country_event = {{ id = {NS}.{EV[PFX + 'kremlin_consulted']} days = 1 }} }}", "}",
         f"else = {{ {PFX}install_first_sec_{k} = yes }}"],
        cost=50,
        visible=[unlocked(f"convene_cc_{k}"), f"{PFX}alive_{k} = yes", f"NOT = {{ has_country_flag = {PFX}first_sec_{k} }}"],
        available=[SED] + ttrig("no_cc_pending", "No vote of the Central Committee is waiting for Moscow's answer.", [f"NOT = {{ has_country_flag = {PFX}cc_pending }}"]) +
                  [f"NOT = {{ has_country_flag = {PFX}cc_failed_{k} }}"] + av_lines(f"cc_{k}", drop=("are_in_power", f"first_sec_{k}", f"alive_{k}")))

# ================================================================ the German Question
C = f"{PFX}german_question_category"
cat(C, "The German Question",
    "Two states in one nation. Demarcation keeps Moscow content and the republic closed; Rapprochement brings credits, visits and Western television "
    "into every living room.\n\nInner-German course: §Y[?COLDWAR_DDR_course|2]§! (-1 Demarcation, +1 Rapprochement).",
    "GFX_decision_category_generic_foreign_policy", 191, DDR_T, [unlocked("german_question")])
dec(C, "demarcation_campaign", "Demarcation Campaign",
    "Abgrenzung: new road signs say 'Capital of the GDR', the anthem loses its text about 'Germany, united fatherland', the constitution its German nation.",
    "GFX_decision_generic_political_rally", E.course(-0.10), cost=50, re_enable=90)
dec(C, "transit_talks", "Transit Talks",
    "State secretaries Kohl and Bahr meet again: transit routes, visitor passes, postal traffic. Every agreement is a small step towards Bonn.",
    "GFX_decision_generic_political_discourse", E.course(0.10) + E.trust(-2), cost=50, re_enable=90)
dec(C, "raise_the_minimum_exchange", "Raise the Minimum Exchange",
    "Every Western visitor must change more D-Marks at one to one. The visits drop; the hard currency rises.",
    "GFX_decision_generic_consumer_goods", E.course(-0.05) + E.receive(0.002), re_enable=180)
dec(C, "freikauf", "Freikauf",
    "Another list of political prisoners for the lawyer Wolfgang Vogel. Bonn pays in goods, through the Protestant church.",
    "GFX_decision_generic_arrest", E.course(0.05) + E.receive(0.003) + ["add_stability = -0.01", f"add_to_variable = {{ {PFX}hard_currency_deals = 1 }}"],
    visible=[unlocked("freikauf")], re_enable=180)

# ================================================================ Moscow
C = f"{PFX}moscow_category"
cat(C, "Moscow",
    "Every road from East Berlin leads through Moscow. Reports, delegations and credits keep the Soviet comrades well disposed.\n\n"
    "Moscow's Trust: §Y[?COLDWAR_DDR_moscow_trust|0]§!",
    "GFX_decision_category_union_state", 192, DDR_T, [unlocked("moscow")])
dec(C, "report_to_the_kremlin", "Report to the Kremlin",
    "The First Secretary reports in person on plan fulfilment, the Western contacts and the mood in the party.",
    "GFX_decision_generic_speech", E.trust(3), cost=25, re_enable=90, ai="base = 1")
dec(C, "host_a_soviet_delegation", "Host a Soviet Delegation",
    "A Soviet delegation tours the Kombinate, lays a wreath at Treptow and is received at Wandlitz.",
    "GFX_decision_generic_political_rally", E.pay(0.002) + E.trust(5), re_enable=180, ai="base = 1")
dec(C, "request_soviet_credit", "Request Soviet Credit",
    "Moscow can help with a credit in transferable roubles - at the price of a little more dependence.",
    "GFX_decision_generic_factory", E.trust(-5) + E.credit(0.005), re_enable=365)

# ================================================================ talks on leaving the Pact
C = f"{PFX}pact_talks_category"
cat(C, "Talks with Moscow",
    "The Soviet Union has rejected our request to leave the Warsaw Pact. After a year the talks can be renewed.",
    "GFX_decision_category_generic_independence", 193, DDR_T,
    [f"OR = {{ has_completed_focus = {PFX}we_the_moscow_negotiations has_completed_focus = {PFX}na_leave_the_warsaw_pact }}", "is_subject_of = SOV"])
dec(C, "renew_the_moscow_negotiations", "Renew the Moscow Negotiations",
    "A new delegation travels to Moscow with the same request.",
    "GFX_decision_generic_independence",
    ["if = {", f"limit = {{ has_completed_focus = {PFX}we_the_moscow_negotiations }}"] + OF.offer_lines(f"{PFX}offer_release_west") +
    ["}", "else = {"] + OF.offer_lines(f"{PFX}offer_release_neutral") + ["}"],
    cost=50, re_enable=365, available=[f"NOT = {{ has_country_flag = {PFX}release_refused }}", "country_exists = SOV"], ai="base = 1")
E.R.offers.update({f"{PFX}offer_release_west", f"{PFX}offer_release_neutral"})

# ================================================================ the Five-Year Plans
C = f"{PFX}five_year_plan_category"
PLAN_PRIOS = [("housing", "Housing", "Flats first: the panel factories run in three shifts.", "GFX_decision_generic_construction",
               [("stability_factor", 0.03), ("consumer_goods_factor", -0.03)]),
              ("key_industries", "Key Industries", "Chemistry, machine building and electronics get the best of everything.", "GFX_decision_generic_industry",
               [("production_speed_buildings_factor", 0.10), ("consumer_goods_factor", 0.03)]),
              ("exports", "Exports for Hard Currency", "What sells in the West is exported, whatever the shops at home lack.", "GFX_decision_generic_consumer_goods",
               [("tax_gain_multiplier_modifier", 0.05), ("consumer_goods_factor", 0.02)]),
              ("defence", "Defence", "The NVA and the Group of Soviet Forces order first.", "GFX_decision_generic_military",
               [("production_speed_arms_factory_factor", 0.15)])]
PERIODS = [(1971, "1971.1.1", "1975.12.31"), (1976, "1975.12.31", "1980.12.31"), (1981, "1980.12.31", "1985.12.31")]
for k, n, d, icon, mods in PLAN_PRIOS:
    E.R.ideas[f"{PFX}plan_{k}"] = dict(name=f"Five-Year Plan: {n}", mods=mods, days=None, desc=d)
cat(C, "The Five-Year Plans",
    "The State Planning Commission drafts, the Party Congress approves, the Volkskammer makes it law. Each plan has one priority; "
    "it applies until the plan ends.",
    "GFX_decision_category_generic_economy", 194, DDR_T,
    ["OR = {"] + [unlocked(f"five_year_plan_{y}") for y, *_ in PERIODS] + ["}"])
for y, start, end in PERIODS:
    for k, n, d, icon, mods in PLAN_PRIOS:
        dec(C, f"plan_{y}_{k}", f"Plan {y}-{y + 4}: {n}", d, icon,
            [f"{PFX}clear_plan_priority = yes", f"add_ideas = {PFX}plan_{k}", f"set_country_flag = {PFX}plan_{y}_chosen"] +
            [f"set_country_flag = {PFX}plan_{z}_ended" for z, *_ in PERIODS if z < y] + [
             tt(f"plan_end_{y}", f"The priority applies until §Y31 December {y + 4}§!.")],
            cost=150, visible=[unlocked(f"five_year_plan_{y}"), f"NOT = {{ has_country_flag = {PFX}plan_{y}_chosen }}", f"date < {end}"],
            available=[f"date > {start}" if y > 1971 else "always = yes", f"date < {end}"],
            ai="base = 1" if k in ("housing", "key_industries") else "base = 0")

# ================================================================ Hard Currency (KoKo)
C = f"{PFX}hard_currency_category"
E.R.ideas[f"{PFX}intershop_network"] = dict(name="The Intershop Network", mods=[("democratic_drift", 0.01)], days=180, desc="")
E.R.ideas[f"{PFX}kombinat_contracts_chemistry"] = dict(name="Contracts: Chemistry", mods=[("industrial_capacity_factory", 0.03)], days=365, desc="")
E.R.ideas[f"{PFX}kombinat_contracts_machines"] = dict(name="Contracts: Machine Building", mods=[("production_factory_efficiency_gain_factor", 0.05)], days=365, desc="")
E.R.ideas[f"{PFX}kombinat_contracts_electronics"] = dict(name="Contracts: Electronics", mods=[("research_speed_factor", 0.02)], days=365, desc="")
E.R.ideas[f"{PFX}housing_drive"] = dict(name="The Building Drive", mods=[("stability_factor", 0.02), ("production_speed_buildings_factor", -0.10)], days=365, desc="")
DEAL = f"add_to_variable = {{ {PFX}hard_currency_deals = 1 }}"
cat(C, "Hard Currency",
    "Alexander Schalck-Golodkowski's Commercial Coordination earns D-Marks by any means. The Politburo prefers not to ask how.",
    "GFX_decision_category_generic_trade", 195, DDR_T,
    [f"OR = {{ {unlocked('hard_currency')} {unlocked('ssp_prison_labour')} {unlocked('koko_imes_arms_sales')} }}"])
dec(C, "intershop", "The Intershop Network",
    "Western goods for Western money - in shops at every border crossing, hotel and port. Citizens with relatives in the West shop there too.",
    "GFX_decision_generic_consumer_goods", E.receive(0.004) + [f"add_timed_idea = {{ idea = {PFX}intershop_network days = 180 }}", DEAL],
    visible=[unlocked("hard_currency")], re_enable=180, ai="base = 1")
dec(C, "genex", "The Genex Gift Service",
    "West Germans order cars, fridges and holidays for their relatives in the East - and pay in D-Marks.",
    "GFX_decision_generic_welfare", E.receive(0.003) + ["add_stability = 0.01", DEAL], visible=[unlocked("hard_currency")], re_enable=180, ai="base = 1")
dec(C, "art_and_antiques", "Art and Antiques",
    "The Kunst und Antiquitäten GmbH sells furniture, paintings and porcelain to Western dealers - much of it taken from private collectors by tax inspectors.",
    "GFX_decision_generic_arrest", E.receive(0.005) + E.faction("small_medium_business_owners", -5) + [DEAL],
    visible=[unlocked("hard_currency")], re_enable=365, ai="base = 1")
dec(C, "prisoner_ransom", "Prisoners for Goods",
    "Another list for Wolfgang Vogel: political prisoners for oil, copper and coffee.",
    "GFX_decision_generic_arrest", E.receive(0.004) + E.course(0.05) + ["add_stability = -0.01", DEAL],
    visible=[unlocked("hard_currency")], re_enable=365)
dec(C, "imes_arms_sales", "Arms Exports (IMES)",
    "IMES sells rifles, ammunition and trucks from the depot at Kavelstorf to whoever pays in hard currency.",
    "GFX_decision_arms_industry", E.receive(0.006) + E.tension(1) + [DEAL], visible=[unlocked("koko_imes_arms_sales")], re_enable=365, ai="base = 1")
dec(C, "prison_labour", "Prison Labour Contracts",
    "Western mail-order houses buy goods made in Bautzen and Hoheneck.",
    "GFX_decision_generic_factory", E.receive(0.004) + ["add_stability = -0.01", DEAL], visible=[unlocked("ssp_prison_labour")], re_enable=365, ai="base = 1")

# ================================================================ the Housing Programme
C = f"{PFX}housing_category"
cat(C, "The Housing Programme",
    "'Every family its own flat by 1990.' Each year the housing construction Kombinate can be driven to build more - at the cost of every other site.",
    "GFX_decision_category_generic_industry", 196, DDR_T, [unlocked("housing_programme")])
dec(C, "building_drive", "The Building Drive of the Year",
    "Panel factories in three shifts, FDJ brigades from every district: Marzahn, Halle-Neustadt and Rostock-Lütten Klein grow by another few thousand flats.",
    "GFX_decision_generic_construction", E.pay(0.005) + [f"add_timed_idea = {{ idea = {PFX}housing_drive days = 365 }}"],
    cost=50, re_enable=365, available=["date > 1972.12.31"], ai="base = 1")

# ================================================================ the Kombinat contracts (Ulbricht's reform)
C = f"{PFX}kombinat_category"
cat(C, "The Kombinat Contracts",
    "The Kombinate trade with each other by economic contract, not by order from above, and keep a share of what they earn. One sector a year can be "
    "put on contracts.",
    "GFX_decision_category_economic", 197, DDR_T, [unlocked("ulb_kombinat_contracts")])
for k, n, icon in (("chemistry", "Chemistry", "GFX_decision_oil"), ("machines", "Machine Building", "GFX_decision_generic_industry"),
                   ("electronics", "Electronics", "GFX_decision_generic_factory")):
    dec(C, f"contracts_{k}", f"Contracts in {n}", f"The Kombinate of {n.lower()} trade with each other by contract for a year.", icon,
        [f"add_timed_idea = {{ idea = {PFX}kombinat_contracts_{k} days = 365 }}"], cost=50, re_enable=365, ai="base = 1",
        available=ttrig("one_sector", "No sector is on contracts yet this year.",
                        [f"NOT = {{ has_idea = {PFX}kombinat_contracts_{x} }}" for x in ("chemistry", "machines", "electronics")]))

# ================================================================ the Military Council
C = f"{PFX}military_council_category"
cat(C, "The Military Council",
    "The generals promised to return to the barracks. Free elections under the army's guard decide who governs after them.",
    "GFX_decision_category_generic_political_actions", 198, DDR_T, [unlocked("mcn_return_to_civilian_rule")])
best = []
for i, p in sorted(PARTY.items()):
    if i in (4, 22):
        continue
    best.append(f"if = {{ limit = {{ check_variable = {{ {PFX}best = {i} }} }} retire_country_leader = yes {E.leader_line(i, p['leader'])} }}")
dec(C, "return_to_civilian_rule", "Return to Civilian Rule",
    "Free elections under the army's guard; the strongest civilian party forms the government and the generals return to Strausberg.",
    "GFX_decision_generic_independence",
    [tt("civilian_rule", "The most popular party other than the Military Council forms the government; elections are allowed."),
     "hidden_effect = {", f"set_temp_variable = {{ {PFX}best = 4 }}", f"set_temp_variable = {{ {PFX}best_pop = 0 }}",
     "for_loop_effect = {", "start = 0", "end = 24", "value = i", "if = {",
     f"limit = {{ NOT = {{ check_variable = {{ i = 22 }} }} NOT = {{ check_variable = {{ i = 8 }} }} NOT = {{ check_variable = {{ i = 9 }} }} "
     f"NOT = {{ check_variable = {{ i = 10 }} }} NOT = {{ check_variable = {{ i = 11 }} }} NOT = {{ check_variable = {{ i = 12 }} }} "
     f"check_variable = {{ party_pop_array^i > {PFX}best_pop }} }}",
     f"set_temp_variable = {{ {PFX}best = i }}", f"set_temp_variable = {{ {PFX}best_pop = party_pop_array^i }}", "}", "}", "}",
     f"if = {{ limit = {{ check_variable = {{ {PFX}best = 4 }} }} {PFX}restore_party_rule = yes }}",
     "else = {", f"set_temp_variable = {{ rul_party_temp = {PFX}best }}", "change_ruling_party_effect = yes", "hidden_effect = {"] + best + ["}", "}",
     f"{PFX}allow_elections = yes"],
    cost=50, once=True, visible=["nationalist_military_junta_are_in_power = yes"], ai="base = 0")

# ================================================================ the Soviet side
C = f"{PFX}german_comrades_category"
SOV_T = ["original_tag = SOV"]
cat(C, "The German Comrades",
    "The German Democratic Republic is the Soviet Union's most important ally - and its most stubborn one. Moscow's Trust in East Berlin: "
    "§Y[?DDR.COLDWAR_DDR_moscow_trust|0]§!",
    "GFX_decision_category_power_struggle", 199, SOV_T,
    ["country_exists = DDR", f"DDR = {{ has_country_flag = {PFX}initialized OR = {{ check_variable = {{ {PFX}moscow_trust < 31 }} has_country_flag = {PFX}fraternal_assistance_open }} }}"])
dec(C, "endorse_a_change", "Endorse a Change in East Berlin",
    "The ambassador lets it be known that Moscow would welcome a change at the top of the SED. A Moscow loyalist may then stand for First Secretary.",
    "GFX_decision_generic_political_discourse", [f"DDR = {{ country_event = {{ id = {NS}.{EV[PFX + 'soviet_endorses']} days = 1 }} }}"], cost=25,
    available=[f"DDR = {{ check_variable = {{ {PFX}moscow_trust < 31 }} {SED} NOT = {{ has_country_flag = {PFX}soviet_endorses_change }} }}"])
dec(C, "fraternal_assistance", "Fraternal Assistance",
    "East Berlin has defied the Soviet Union. An ultimatum would give it one night to return to the path of socialism - or to face the Soviet Army.",
    "GFX_decision_generic_military", [f"DDR = {{ country_event = {{ id = {NS}.{EV[PFX + 'fraternal_assistance']} days = 1 }} }}", "add_war_support = 0.03"],
    cost=100, visible=[f"DDR = {{ has_country_flag = {PFX}fraternal_assistance_open }}"], available=["has_war = no", "NOT = { has_war_with = DDR }"],
    ai="base = 1\nmodifier = { factor = 0 DDR = { check_variable = { COLDWAR_DDR_moscow_trust > 20 } } }\nmodifier = { factor = 0 NOT = { has_government = communism } }")


# ---------------------------------------------------------------- files
def categories_file():
    L = [HEADER]
    for key, name, desc, icon, prio, allowed, visible in CATS:
        L += [f"{key} = {{", f"icon = {icon}", f"priority = {prio}", "allowed = {"] + allowed + ["}"]
        if visible:
            L += ["visible = {"] + visible + ["}"]
        L += ["}", ""]
    return "\n".join(block(L)) + "\n"


def decisions_file():
    L = [HEADER]
    for key, *_ in CATS:
        L += [f"{key} = {{"]
        for d in DECS[key]:
            L += d
        L += ["}", ""]
    return "\n".join(block(L)) + "\n"


def plan_effects():
    """removes the plan priority (when a new plan starts or the old one ends)"""
    s = [f"{PFX}clear_plan_priority = {{"] + [f"if = {{ limit = {{ has_idea = {PFX}plan_{k} }} remove_ideas = {PFX}plan_{k} }}" for k, *_ in PLAN_PRIOS] + ["}", "",
         "# monthly: a priority ends with its plan",
         f"{PFX}monthly_plan = {{"]
    for y, start, end in PERIODS:
        s += ["if = {", f"limit = {{ has_country_flag = {PFX}plan_{y}_chosen date > {end} NOT = {{ has_country_flag = {PFX}plan_{y}_ended }} }}",
              f"set_country_flag = {PFX}plan_{y}_ended", f"{PFX}clear_plan_priority = yes", "}"]
    s += ["}", ""]
    return s
