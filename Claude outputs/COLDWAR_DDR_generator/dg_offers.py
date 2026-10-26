# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | The 69 offers of the GDR tree (English texts, MD agreement-event style).
# Multiplayer rule: the focus only sends the proposal. The other country (player or AI) decides, and every effect - on both sides -
# happens in its answer, shown there as concrete option effects. THIS = the receiver, FROM = the GDR.
from dg_common import *
import dg_effects as E
import json
import re

PICS = json.load(open(os.path.join(HERE, "gfxsel", "gfx_pick.json"), encoding="utf-8"))["events"]
OFFERS = {}
OFFER_IDEAS = {}      # id (without prefix) -> (name, [(mod, value)], days)
OPINION_EXTRA = {     # mutual opinion modifiers of the answers
    f"{PFX}treaty_partner": (20, "Treaty Partner"), f"{PFX}good_neighbours": (15, "Good Neighbours"),
    f"{PFX}border_partners": (10, "Agreed Borders"), f"{PFX}detente_partner": (15, "German-German Détente"),
    f"{PFX}friendship_treaty": (20, "Treaty of Friendship"), f"{PFX}solidarity_partner": (20, "Socialist Solidarity"),
    f"{PFX}reconciliation": (25, "Reconciliation"), f"{PFX}diplomatic_relations": (15, "Diplomatic Relations"),
    f"{PFX}recognition_india": (20, "Recognition and Friendship"), f"{PFX}comrades_in_arms": (25, "Comrades in Arms"),
    f"{PFX}a_cosmonaut_from_berlin": (15, "A Cosmonaut from Berlin"), f"{PFX}friends_of_the_crown": (20, "Frederick Comes Home"),
    f"{PFX}terror_condemned": (-25, "Terror in East Berlin"), f"{PFX}ambassador_recalled": (-15, "Ambassador Recalled"),
    f"{PFX}socialist_neighbours": (15, "Open Socialist Borders"), f"{PFX}trading_partner": (10, "Trading Partner"),
    f"{PFX}coffee_partner": (15, "Coffee Partnership"),
}


def idea(k, name, mods, days=None):
    OFFER_IDEAS[k] = (name, mods, days)
    return k


# ---- ideas the answers give (ours and the partners')
idea("german_confederation", "The German Confederation", [("trade_opinion_factor", 0.15), ("research_speed_factor", 0.03)])
idea("erfurt_partnership", "The Erfurt Partnership", [("trade_opinion_factor", 0.10), ("research_speed_factor", 0.02)], 730)
idea("national_confederation", "The National Confederation", [("trade_opinion_factor", 0.10), ("stability_factor", 0.02)])
idea("union_treaty", "The Union Treaty", [("stability_factor", 0.05), ("political_power_factor", 0.10), ("energy_gain_multiplier", 0.10)])
idea("ethiopian_coffee", "Coffee from Ethiopia", [("consumer_goods_factor", -0.02), ("stability_factor", 0.02)], 730)
idea("gdr_advisers_ethiopia", "GDR Security Advisers", [("army_org_factor", 0.03), ("police_cost_multiplier_modifier", -0.10)], 730)
idea("gdr_engineers_mozambique", "GDR Engineers and Teachers", [("education_cost_multiplier_modifier", -0.10), ("local_resources_factor", 0.05)], 1095)
idea("mozambican_contract_workers", "Contract Workers from Mozambique", [("total_workforce_modifier", 0.02)], 1095)
idea("gdr_ship_orders", "Ships from Wismar and Rostock", [("industrial_capacity_dockyard", 0.05)], 730)
idea("gdr_pipeline_builders", "The Drushba Route Builders", [("production_speed_buildings_factor", 0.05)], 730)
idea("dak_lak_plantations", "Coffee Plantations in Dak Lak", [("agricolture_productivity_modifier", 0.05)], 1095)
idea("cultural_exchange", "German-German Cultural Exchange", [("research_speed_factor", 0.02)], 730)
idea("common_security", "Common Security", [("military_spending_cost_factor", -0.05)], 1095)
idea("gdr_engineers", "GDR Engineers and Teachers", [("production_speed_buildings_factor", 0.03)], 730)
idea("open_socialist_borders", "Open Socialist Borders", [("stability_factor", 0.02)], 730)
idea("gdr_solidarity_shipments", "Solidarity Shipments from the GDR", [("stability_factor", 0.03)], 365)
idea("trained_workers_from_the_gdr", "Workers Trained in the GDR", [("productivity_growth_modifier", 0.02)], 1095)
idea("gdr_hospital", "The GDR Hospital", [("stability_factor", 0.03)], 365)
idea("gdr_trained_security", "Security Training from the GDR", [("intelligence_agency_defense", 0.10)], 730)
idea("gdr_trucks_and_machinery", "IFA Trucks and Machinery", [("production_speed_buildings_factor", 0.05)], 1095)
idea("nva_instructors", "NVA Instructors", [("army_org_factor", 0.05)], 730)
idea("mfs_advisers", "MfS Advisers", [("intelligence_agency_defense", 0.10)], 1095)
idea("tropical_coffee", "Coffee from the Tropics", [("stability_factor", 0.02)], 365)
idea("gdr_arms_deliveries", "Arms from the GDR", [("army_org_factor", 0.03)], 730)
idea("grain_contract", "The Grain Contract", [("stability_factor", 0.02), ("agricolture_productivity_modifier", 0.03)], 1825)
idea("grain_customer", "A Customer in East Berlin", [("trade_opinion_factor", 0.05)], 1825)
idea("yugoslav_partnership", "Partnership Outside the Blocs", [("trade_opinion_factor", 0.05), ("research_speed_factor", 0.02)], 1825)
idea("clean_air_treaty", "The Clean Air Treaty", [("stability_factor", 0.02), ("agricolture_productivity_modifier", 0.02)], 1825)
idea("reconciliation_trade", "Reconciliation on the Oder", [("trade_opinion_factor", 0.05)], 1825)
idea("soviet_advisers_gdr", "Soviet Advisers in Every Ministry", [("research_speed_factor", 0.03), ("production_factory_efficiency_gain_factor", 0.03)], 1095)
idea("eastern_social_charter", "The Social Charter of the East", [("social_cost_multiplier_modifier", 0.10), ("stability_factor", 0.03)], 1825)
idea("accession_transition", "Accession: The Transition Year", [("political_power_factor", -0.10), ("stability_factor", 0.05)], 365)
for k, (n, m, d) in OFFER_IDEAS.items():
    E.R.ideas[PFX + k] = dict(name=n, mods=m, days=d, desc="")


def offer(key, pic, title, desc, accept, code, decline="We must decline.", ai_base=50, ai_mods="", decline_code=(), from_code=()):
    k = PFX + "offer_" + key
    from dg_load import OFFERS as DESIGN
    assert k in DESIGN, k
    OFFERS[k] = dict(targets=[E.tag(t) for t in DESIGN[k]["tags"]], pic=PICS.get(k, pic), title=title, desc=desc, accept=accept,
                     code=list(code), decline=decline, ai_base=ai_base, ai_mods=ai_mods, decline_code=list(decline_code))


# ---------------------------------------------------------------- code helpers (receiver scope, FROM = the GDR)
def J(*parts):
    out = []
    for p in parts:
        out += p if isinstance(p, list) else [p]
    return out


def us(*lines):
    """effects for the GDR (FROM)"""
    return ["FROM = {"] + J(*lines) + ["}"]


def them_idea(k):
    iid = PFX + k
    d = OFFER_IDEAS[k][2]
    add = f"add_timed_idea = {{ idea = {iid} days = {d} }}" if d else f"add_ideas = {iid}"
    return [f"if = {{ limit = {{ NOT = {{ has_idea = {iid} }} }} {add} }}"]


def our_idea(k):
    return us(them_idea(k))


def mutual(mod):
    return [f"add_opinion_modifier = {{ target = FROM modifier = {mod} }}", f"reverse_add_opinion_modifier = {{ target = FROM modifier = {mod} }}"]


def our_opinion(mod):
    """the GDR's own opinion of the partner"""
    return [f"reverse_add_opinion_modifier = {{ target = FROM modifier = {mod} }}"]


def their_opinion(mod):
    return [f"add_opinion_modifier = {{ target = FROM modifier = {mod} }}"]


TRADE = ["set_temp_variable = { receiver_nation = THIS.id }", "set_temp_variable = { sender_nation = FROM.id }", "set_improved_trade_agreement = yes"]


def first(key, lines):
    """effects that only the first acceptance among several partners brings"""
    return [f"if = {{ limit = {{ NOT = {{ has_global_flag = {PFX}{key}_signed }} }}", f"set_global_flag = {PFX}{key}_signed"] + J(lines) + ["}"]


def tt(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def contract_workers():
    """'Contract Workers'; if already present it becomes 'The Contract Worker Programme'"""
    a, b = f"{PFX}sol_contract_workers", f"{PFX}sol_contract_worker_programme"
    return us(f"if = {{ limit = {{ has_idea = {a} }} swap_ideas = {{ remove_idea = {a} add_idea = {b} }} }}",
              f"else_if = {{ limit = {{ NOT = {{ has_idea = {b} }} }} add_ideas = {a} }}")


def soviet_pay(share):
    """the GDR pays the Soviet Union (THIS) a share of its GDP"""
    return us(f"set_temp_variable = {{ {PFX}transfer_target = ROOT.id }}", f"set_temp_variable = {{ {PFX}gdp_share = {fmt(share)} }}",
              f"{PFX}transfer_gdp_share = yes")


def bonn_pays(share):
    """the partner (THIS) pays the GDR a sum worth `share` of the GDR's GDP - both treasuries show it"""
    return [f"set_temp_variable = {{ {PFX}amount = FROM.gdp_total }}", f"multiply_temp_variable = {{ {PFX}amount = {fmt(share)} }}",
            f"set_temp_variable = {{ treasury_change = {PFX}amount }}", "multiply_temp_variable = { treasury_change = -1 }", "modify_treasury_effect = yes",
            f"FROM = {{ set_temp_variable = {{ treasury_change = {PFX}amount }} modify_treasury_effect = yes }}"]


def garrison_withdrawal(days):
    return us(f"{PFX}start_garrison_withdrawal_{days} = yes")


def notice(kind):
    """a human Soviet Union hears of it and may endorse or object (its decision)"""
    return us(f"{PFX}notify_kremlin_{kind} = yes")


DETENTE_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
              "modifier = { factor = 1.5 check_variable = { global.mdcw_cw_tension > 60 } }\n"
              "modifier = { factor = 0.5 has_opinion = { target = FROM value < -20 } }")
BONN_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
           "modifier = { factor = 1.5 FROM = { check_variable = { COLDWAR_DDR_course > 0.19 } } }\n"
           "modifier = { factor = 0.5 FROM = { check_variable = { COLDWAR_DDR_course < -0.39 } } }")
UNITY_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
            "modifier = { factor = 0 FROM = { has_war = yes } }\n"
            "modifier = { factor = 1.5 FROM = { NOT = { has_government = communism } } }")
MOSCOW_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
             "modifier = { factor = 1.5 FROM = { check_variable = { COLDWAR_DDR_moscow_trust > 64 } } }\n"
             "modifier = { factor = 0.5 FROM = { check_variable = { COLDWAR_DDR_moscow_trust < 35 } } }")
RELEASE_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
              "modifier = { factor = 6 NOT = { has_government = communism } }\n"
              "modifier = { factor = 3 has_country_flag = COLDWAR_SOV_gensec_gor }\n"
              "modifier = { factor = 2 check_variable = { global.mdcw_cw_tension < 30 } }\n"
              "modifier = { factor = 0.3 check_variable = { global.mdcw_cw_tension > 60 } }\n"
              "modifier = { factor = 1.5 FROM = { check_variable = { COLDWAR_DDR_moscow_trust > 64 } } }")
FRIEND_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
             "modifier = { factor = 1.5 has_government = communism }\n"
             "modifier = { factor = 0.3 has_opinion = { target = FROM value < 0 } }")

# ================================================================ the Soviet Union
offer("release_west", "flag", "East Berlin Asks to Leave",
      "The government in East Berlin asks to be released from the Warsaw Pact and from its treaty ties with the Soviet Union. "
      "The Group of Soviet Forces would withdraw over two years.",
      "Let them go.", J("end_puppet = FROM", E.tension(-2), us(f"country_event = {{ id = {NS}.62 days = 1 }}")),
      decline="The answer is no.", ai_base=5, ai_mods=RELEASE_AI,
      decline_code=us(E.trust(-10), f"set_country_flag = {{ flag = {PFX}release_refused days = 365 }}"))
offer("release_neutral", "flag", "Armed Neutrality on the Elbe",
      "East Berlin proposes to leave the Warsaw Pact for armed neutrality: the treaty ties end, the garrison withdraws over two years, and the republic "
      "promises never to join NATO.",
      "Accept a neutral Germany in the East.", J("end_puppet = FROM", E.tension(-1), us(f"country_event = {{ id = {NS}.62 days = 1 }}")),
      decline="Out of the question.", ai_base=5, ai_mods=RELEASE_AI,
      decline_code=us(E.trust(-10), f"country_event = {{ id = {NS}.32 days = 3 }}"))
offer("cdu_garrison_withdrawal", "flag", "A Phased Withdrawal",
      "East Berlin asks for a phased withdrawal of the Group of Soviet Forces in Germany over three years and offers to pay for the housing of the returning officers.",
      "Bring the soldiers home.", J(E.tension(-2), soviet_pay(0.01), garrison_withdrawal(1095)),
      decline="The garrison stays.", ai_base=15, ai_mods=RELEASE_AI, decline_code=J(E.tension(2), us(E.trust(-10))))
offer("spd_garrison_withdrawal", "flag", "A Treaty of Friendship and Withdrawal",
      "A social-democratic government in East Berlin proposes a treaty of friendship and non-aggression: the Group of Soviet Forces withdraws in stages, "
      "the republic stays in Comecon, and East Berlin pays for barracks and housing in the Soviet Union.",
      "Sign the treaty.", J(E.tension(-2), soviet_pay(0.01), garrison_withdrawal(1095), mutual(f"{PFX}treaty_partner")),
      decline="The garrison stays.", ai_base=15, ai_mods=RELEASE_AI, decline_code=J(E.tension(1), us(E.trust(-5))))
offer("kis_garrison_withdrawal", "flag", "The Soldiers Go Home",
      "The church government in East Berlin asks the Soviet Union to withdraw its forces within five years. Swords into ploughshares, it says.",
      "Withdraw within five years.", J(E.tension(-2), garrison_withdrawal(1825), us(E.trust(-10))),
      decline="The garrison stays.", ai_base=10, ai_mods=RELEASE_AI)
offer("tws_garrison_withdrawal", "flag", "In Step with the West",
      "East Berlin proposes a neutral Germany on the Austrian model: the Group of Soviet Forces withdraws in step with the Western armies.",
      "Withdraw in step with the West.", J(E.tension(-2), garrison_withdrawal(730)),
      decline="The garrison stays.", ai_base=10, ai_mods=RELEASE_AI)
offer("mcn_brotherhood_in_arms", "warsaw", "Brotherhood in Arms",
      "The Military Council of the NVA invites the Soviet Army to a joint exercise on its soil, like 'Brotherhood in Arms 70'.",
      "Send our divisions.", J("army_experience = 25", us("army_experience = 25", E.trust(5)), E.tension(1)), ai_base=70, ai_mods=MOSCOW_AI)
offer("ldk_loyalty_pledge", "flag", "The Kádár Compromise",
      "The new leadership in East Berlin pledges to stay in the Warsaw Pact and in Comecon - and asks Moscow to tolerate its internal reforms.",
      "Tolerate the reforms.", J(us(E.trust(10))), ai_base=45, ai_mods=MOSCOW_AI)
offer("tg_soviet_advisers", "flag", "Advisers in Every Ministry",
      "The Thälmann Guard asks for Soviet advisers in every ministry and every Kombinat.",
      "Send the advisers.", J(our_idea("soviet_advisers_gdr"), us(E.trust(5))), ai_base=75, ai_mods=MOSCOW_AI)
offer("kro_confederation", "flag", "The Closest Union",
      "East Berlin proposes a confederation with the Soviet Union: a joint foreign and defence policy and a joint currency board for the transferable rouble. "
      "The GDR would keep its own government.",
      "Accept the confederation.", J(our_idea("union_treaty"), us(E.trust(25)), mutual(f"{PFX}friendship_treaty")),
      decline="A gesture we appreciate - but no.", ai_base=40, ai_mods=MOSCOW_AI, decline_code=us(E.trust(5)))
offer("soviet_ship_orders", "navy", "Ships for the Soviet Union",
      "The shipyards of Wismar, Rostock and Stralsund offer a long-term order of trawlers and freighters for the Soviet fleet.",
      "Place the order.", J(them_idea("gdr_ship_orders"), us(E.trust(5), E.country_dyn("planned_economy", {"industrial_capacity_dockyard": 0.05}))),
      ai_base=70, ai_mods=MOSCOW_AI)
offer("soyuz_pipeline", "pipe", "The Orenburg Pipeline",
      "East Berlin offers to build its section of the Soyuz pipeline from Orenburg - with its own workers and machines - in return for natural gas.",
      "Accept the builders.", J(them_idea("gdr_pipeline_builders"),
                                us(E.trust(5), E.country_dyn("planned_economy", {"energy_gain_multiplier": 0.05}), f"set_country_flag = {PFX}soyuz_gas")),
      ai_base=80, ai_mods=MOSCOW_AI)
offer("interkosmos_cosmonaut", "space", "A German in Space",
      "The GDR asks for a seat on a Soyuz mission of the Interkosmos programme for one of its pilots.",
      "Fly the German comrade.", J(their_opinion(f"{PFX}a_cosmonaut_from_berlin"), us(f"country_event = {{ id = {NS}.24 days = 1 }}")),
      ai_base=80, ai_mods=MOSCOW_AI, decline_code=us(E.trust(-2)))
offer("friendship_treaty_1975", "sign", "The Treaty of 1975",
      "East Berlin proposes a new Treaty of Friendship, Cooperation and Mutual Assistance for twenty-five years, binding the NVA to the Unified Command.",
      "Sign the treaty.", J(mutual(f"{PFX}friendship_treaty"), us(E.trust(5))), ai_base=85, ai_mods=MOSCOW_AI)
offer("ust_ilimsk", "sign", "The Ust-Ilimsk Combine",
      "The GDR offers to build its share of the pulp combine at Ust-Ilimsk in return for pulp and paper over ten years.",
      "Accept the investment.", J(them_idea("gdr_engineers"), us(E.country_dyn("planned_economy", {"consumer_goods_factor": -0.01}))),
      ai_base=80, ai_mods=MOSCOW_AI)
offer("fraternal_assistance_poland", "warsaw", "Three Divisions for Poland",
      "East Berlin urges joint action of the Warsaw Pact in Poland and offers three NVA divisions. What happens in Poland remains the Soviet Union's decision.",
      "Accept the offer.", J(us(E.trust(5), "army_experience = 25")), decline="Not now.", ai_base=50, ai_mods=MOSCOW_AI)
offer("counter_deployment", "missiles", "Missiles on the Elbe",
      "East Berlin offers bases for Soviet operational-tactical missiles on its territory.",
      "Deploy the missiles.", J(us(E.trust(5)), E.tension(1)), ai_base=60, ai_mods=MOSCOW_AI)

# ================================================================ the Federal Republic
offer("national_confederation", "germany", "A German Confederation",
      "East Berlin proposes a German confederation under a joint national council. Both states would keep their armies; the inner-German border would open.",
      "Accept the confederation.", J(mutual(f"{PFX}detente_partner"), us(E.course(0.30))), ai_base=25, ai_mods=BONN_AI)
offer("koko_bavarian_credit", "bank", "A Billion from Bavaria",
      "Commercial Coordination asks for a bank credit of one billion D-Mark guaranteed by the federal government. In return the SM-70 spring guns on the border "
      "would be dismantled and family visits made easier.",
      "Guarantee the credit.", J(us(E.credit(0.015), E.course(0.10), E.trust(-3), f"set_country_flag = {PFX}sm70_dismantled"), notice("western_credit"),
                                 tt("sm70", "The SM-70 spring guns on the inner-German border are dismantled and family visits become easier.")),
      ai_base=55, ai_mods=BONN_AI)
offer("cdu_accession", "germany", "Accession under Article 23",
      "The government in East Berlin asks for the accession of the five restored states to the Federal Republic under Article 23 of the Basic Law. "
      "After a transition year the republic would join the Federal Republic peacefully.",
      "Welcome them.", J(us(f"{PFX}start_accession = yes")), ai_base=70, ai_mods=UNITY_AI,
      decline_code=us(E.course(0.10), "add_stability = -0.03"))
offer("ldpd_confederation", "germany", "Customs and Currency Union",
      "East Berlin proposes a German confederation: a customs and currency union and a joint council of ministers; both states keep their governments and alliances.",
      "Accept the confederation.", J(them_idea("german_confederation"), our_idea("german_confederation"), us(E.course(0.30))),
      ai_base=45, ai_mods=BONN_AI, decline_code=us(E.course(0.05)))
offer("ldpd_accession", "germany", "Unity in Freedom",
      "The liberal government in East Berlin asks to join the Federal Republic. After a transition year the republic would join peacefully.",
      "Welcome them.", J(us(f"{PFX}start_accession = yes")), ai_base=70, ai_mods=UNITY_AI, decline_code=us("add_stability = -0.03"))
offer("spd_erfurt_revisited", "germany", "Erfurt Revisited",
      "Two social-democratic governments meet in Erfurt again - this time without police lines.",
      "Travel to Erfurt.", J(them_idea("erfurt_partnership"), our_idea("erfurt_partnership"), us(E.course(0.10))), ai_base=60, ai_mods=BONN_AI)
offer("spd_unity_treaty", "germany", "A Treaty of Unity",
      "East Berlin proposes to merge both states into one federal republic with a new constitution under Article 146. The social rights of the East "
      "would be kept for five years.",
      "Sign the treaty of unity.", J(us(f"{PFX}start_accession = yes", f"set_country_flag = {PFX}social_charter")), ai_base=60, ai_mods=UNITY_AI,
      decline_code=us(E.course(0.05), "add_stability = -0.02"))
offer("ndpd_national_confederation", "germany", "A Confederation of the Nation",
      "The national government in East Berlin proposes common citizenship and a joint national assembly; each state keeps its army and its alliance.",
      "Accept the confederation.", J(them_idea("national_confederation"), our_idea("national_confederation"), us(E.course(0.30))),
      ai_base=30, ai_mods=BONN_AI, decline_code=us(E.outlook(4, 0.03)))
offer("pcc_frederick_comes_home", "royal", "Frederick Comes Home",
      "The Prussian Crown Council asks for the coffins of Frederick the Great and Frederick William I to be returned from Hohenzollern Castle to Potsdam.",
      "Let the kings go home.", J(us("add_stability = 0.03", "add_political_power = 100", E.course(0.05)), our_opinion(f"{PFX}friends_of_the_crown")),
      ai_base=60, ai_mods=BONN_AI, decline_code=us(E.outlook(4, 0.02)))
offer("spk_swing_credit", "bank", "Raise the Swing",
      "The Planning Commission asks Bonn to raise the interest-free 'swing' overdraft of inner-German trade.",
      "Raise the swing.", J(bonn_pays(0.005), us(E.course(0.05))), ai_base=55, ai_mods=BONN_AI)
offer("kis_church_transfers", "church", "Partners of the Union",
      "The West German churches and the federal government are asked to pay in goods and hard currency for the church's hospitals and homes in the East.",
      "Pay for the hospitals.", J(bonn_pays(0.005), us(E.course(0.10))), ai_base=60, ai_mods=BONN_AI)
offer("kd_joint_ventures", "factory", "Joint Ventures with the West",
      "West German firms may hold up to 49 percent in joint ventures with the Kombinate.",
      "Allow the investments.", J(us("set_temp_variable = { skip_payment = 1 }", "one_random_industrial_complex = yes", "one_random_industrial_complex = yes",
                                     "set_temp_variable = { skip_payment = 0 }", E.course(0.10))), ai_base=55, ai_mods=BONN_AI)
offer("uct_open_trade", "trade", "Trade Without Quotas",
      "Inner-German trade without quotas and with free private contracts.",
      "Open the trade.", J(TRADE, us(E.country_dyn("planned_economy", {"trade_opinion_factor": 0.10}), E.receive(0.005), E.course(0.10))),
      ai_base=60, ai_mods=BONN_AI)
offer("gl_elbe_commission", "green", "An Elbe Commission",
      "A joint Elbe commission: Hamburg pays part of the sewage plants upstream.",
      "Pay for clean water.", J(bonn_pays(0.005), us(E.course(0.05))), ai_base=60, ai_mods=BONN_AI)
offer("tws_neutral_germany", "germany", "The Austrian Solution",
      "East Berlin proposes a treaty of neutrality: both German states leave NATO and the Warsaw Pact, foreign troops leave, and a joint commission prepares "
      "all-German elections.",
      "Accept neutrality.", J(us(E.course(0.30)), E.tension(-3)), ai_base=10, ai_mods=BONN_AI)
offer("tws_socialist_confederation", "germany", "A Confederation of Two States",
      "A confederation of the two German states with a joint council, free movement and a common market.",
      "Accept the confederation.", J(us(E.course(0.20), E.country_dyn("socialist_camp", {"trade_opinion_factor": 0.10})), mutual(f"{PFX}detente_partner")),
      ai_base=30, ai_mods=BONN_AI)
offer("hon_billion_credit", "bank", "The Billion from Bavaria",
      "East Berlin asks for a bank credit of one billion D-Mark guaranteed by the federal government. In return the automatic firing devices on the border are dismantled.",
      "Guarantee the credit.", J(us(E.credit(0.02), E.course(0.10), E.trust(-3), f"set_country_flag = {PFX}sm70_dismantled"), notice("western_credit"),
                                 tt("sm70_hon", "The automatic firing devices on the inner-German border are dismantled.")),
      ai_base=55, ai_mods=BONN_AI)
offer("hon_bonn_visit", "germany", "A State Visit to Bonn",
      "The General Secretary of the SED asks for a state visit to Bonn with full military honours.",
      "Receive him with full honours.", J(us("add_stability = 0.05", E.course(0.10)), mutual(f"{PFX}treaty_partner")), ai_base=50, ai_mods=BONN_AI)
offer("sto_heads_of_government", "germany", "The Erfurt Channel",
      "The Chairman of the Council of Ministers proposes a permanent channel between the two heads of government.",
      "Open the channel.", J(mutual(f"{PFX}good_neighbours"), us(E.course(0.05))), ai_base=60, ai_mods=BONN_AI)
offer("kre_travel_credit", "germany", "Freedom of Travel for Credit",
      "East Berlin proposes that every citizen of the GDR may travel to the West - if the Federal Republic finances a travel-currency fund and a large credit line.",
      "Finance the travel fund.", J(us(E.credit(0.01), E.course(0.10)), our_opinion(f"{PFX}good_neighbours"), notice("western_credit")),
      ai_base=50, ai_mods=BONN_AI, decline_code=us(E.course(-0.05)))
offer("mod_treaty_community", "germany", "A Treaty Community",
      "East Berlin proposes a Treaty Community: joint commissions for the economy, transport, environment and culture, and a long-term trade and credit agreement.",
      "Sign the treaty.", J(us(E.course(0.20), E.credit(0.01), E.country_dyn("socialist_camp", {"trade_opinion_factor": 0.15})), mutual(f"{PFX}detente_partner")),
      ai_base=55, ai_mods=BONN_AI, decline_code=us(E.course(-0.05)))
offer("vw_engine_licence", "factory", "A Volkswagen Licence",
      "A four-stroke engine plant in Karl-Marx-Stadt under Volkswagen licence, paid in counter-trade.",
      "Grant the licence.", J(us("set_temp_variable = { skip_payment = 1 }", "one_random_industrial_complex = yes", "set_temp_variable = { skip_payment = 0 }",
                                 E.pay(0.008), E.course(0.05)),
                              "set_temp_variable = { tag_index = THIS.id }", "set_temp_variable = { influence_target = FROM.id }",
                              "set_temp_variable = { percent_change = 3 }", "change_influence_percentage = yes"), ai_base=60, ai_mods=BONN_AI)
offer("warning_shots", "germany", "No More Shooting",
      "The republic has ordered its border troops to fire warning shots only. Bonn is asked to answer the gesture with a goodwill trade credit.",
      "Grant the credit.", J(bonn_pays(0.005), us(E.course(0.05))), ai_base=65, ai_mods=BONN_AI)
offer("transit_agreement", "germany", "The Transit Agreement",
      "Transit between the Federal Republic and West Berlin through the territory of the GDR, without searches, against a yearly lump sum.",
      "Sign the agreement.", J(mutual(f"{PFX}good_neighbours"), E.tension(-1), us(f"set_country_flag = {PFX}transit_agreement_accepted"),
                               tt("transit", "Secure access to West Berlin for the Federal Republic.")), ai_base=70, ai_mods=DETENTE_AI)
offer("basic_treaty", "sign", "The Basic Treaty",
      "A Treaty on the Basis of Relations: equal sovereign states, an inviolable border, permanent missions in Bonn and East Berlin.",
      "Sign the Basic Treaty.", J(mutual(f"{PFX}treaty_partner"), E.tension(-2), us(f"set_country_flag = {PFX}basic_treaty_accepted"), notice("basic_treaty"),
                                  tt("basic_treaty", "Travel relief and family reunions for the citizens of the Federal Republic.")), ai_base=60, ai_mods=DETENTE_AI)
offer("border_commission", "germany", "The Border Commission",
      "A joint commission surveys and marks the whole inner-German border as a state border, the Elbe in mid-river.",
      "Mark the border.", J(mutual(f"{PFX}border_partners"), E.tension(-1), us("add_stability = 0.02"),
                            tt("border_commission", "Agreed rules for border waters, fishing and accidents.")), ai_base=60, ai_mods=DETENTE_AI)
offer("billion_credit", "bank", "The Strauß Credit",
      "A credit of one billion marks from a West German bank consortium, guaranteed by Bonn. In return the self-firing devices come off the border fence "
      "and children no longer pay the minimum exchange.",
      "Guarantee the credit.", J(us(E.credit(0.02), f"set_country_flag = {PFX}sm70_dismantled"), mutual(f"{PFX}good_neighbours"), notice("western_credit"),
                                 tt("strauss", "The self-firing devices come off the border fence; children are exempt from the minimum exchange.")),
      ai_base=55, ai_mods=BONN_AI)
offer("cultural_agreement", "germany", "The Cultural Agreement",
      "Exchanges of exhibitions, orchestras and scholars, the return of displaced art treasures and town twinnings.",
      "Sign the agreement.", J(mutual(f"{PFX}good_neighbours"), them_idea("cultural_exchange"), our_idea("cultural_exchange")), ai_base=65, ai_mods=DETENTE_AI)
offer("common_security", "sign", "Common Security",
      "A treaty on a chemical-weapons-free zone and a nuclear-free corridor in Central Europe, based on the SED-SPD drafts.",
      "Sign the treaty.", J(E.tension(-2), mutual(f"{PFX}treaty_partner"), them_idea("common_security"), our_idea("common_security")),
      ai_base=45, ai_mods=DETENTE_AI)

# ================================================================ neighbours, the bloc and the world
offer("kis_reconciliation_poland", "church", "Action Reconciliation",
      "A treaty of reconciliation: church partnerships, joint youth work camps and open crossings on the Oder.",
      "Sign the treaty.", J(mutual(f"{PFX}reconciliation"), them_idea("reconciliation_trade"), our_idea("reconciliation_trade")), ai_base=65, ai_mods=FRIEND_AI)
offer("gl_clean_air_treaty", "green", "Clean Air for the Ore Mountains",
      "Both sides fit desulphurisation to their power stations on the border, to save the forests of the Ore Mountains.",
      "Sign the treaty.", J(them_idea("clean_air_treaty"), our_idea("clean_air_treaty")), ai_base=55, ai_mods=FRIEND_AI)
offer("dbd_grain_contract", "grain", "A Five-Year Grain Contract",
      "A five-year grain supply contract at world-market prices.",
      "Sign the contract.", J(our_idea("grain_contract"), them_idea("grain_customer")), ai_base=55, ai_mods=DETENTE_AI)
offer("tws_yugoslav_partnership", "flag", "The Yugoslav Lesson",
      "A partnership of two socialist states outside the blocs: advisers on self-management and preferential trade.",
      "Accept the partnership.", J(them_idea("yugoslav_partnership"), our_idea("yugoslav_partnership")), ai_base=65, ai_mods=FRIEND_AI)
offer("ldk_appeal_for_solidarity", "flag", "Guarantee the Berlin Spring",
      "The democratic communists in East Berlin ask us to guarantee their reforms publicly.",
      "Guarantee the Berlin Spring.", J(mutual(f"{PFX}reconciliation"), E.tension(1)), ai_base=45, ai_mods=FRIEND_AI)
offer("ssp_security_advisers", "spy", "MfS Advisers",
      "The Ministry for State Security offers to build up our state security service.",
      "Accept the advisers.", J(mutual(f"{PFX}comrades_in_arms"), them_idea("mfs_advisers"), us(E.country_dyn("mfs", {"intel_network_gain_factor": 0.05}))),
      ai_base=70, ai_mods=FRIEND_AI)
offer("lam_ethiopia", "ethiopia", "Comrades in Addis Ababa",
      "A treaty of friendship: GDR security advisers and IFA trucks for Ethiopia, Ethiopian coffee at friendship prices for the GDR.",
      "Sign the treaty.", J(them_idea("gdr_advisers_ethiopia"), our_idea("ethiopian_coffee"), our_opinion(f"{PFX}friendship_treaty")),
      ai_base=75, ai_mods=FRIEND_AI)
offer("lam_mozambique", "mozambique", "Comrades in Maputo",
      "A treaty of friendship: GDR engineers for the Moatize coal mines and teachers for FRELIMO schools; contract workers for the GDR.",
      "Sign the treaty.", J(them_idea("gdr_engineers_mozambique"), our_idea("mozambican_contract_workers"), our_opinion(f"{PFX}friendship_treaty")),
      ai_base=75, ai_mods=FRIEND_AI)
offer("coffee_plantations", "vietnam", "Coffee from the Central Highlands",
      "East Berlin offers to finance coffee plantations in Dak Lak and to be paid in coffee.",
      "Plant the coffee.", J(them_idea("dak_lak_plantations"), us(E.country_dyn("planned_economy", {"consumer_goods_factor": -0.02})),
                             our_opinion(f"{PFX}coffee_partner")), ai_base=75, ai_mods=FRIEND_AI)
offer("arab_friendship", "arab", "Friends in the Arab World",
      "Agreements on friendship, trade and technical cooperation: GDR engineers and teachers, oil and cotton at fixed prices.",
      "Sign the agreements.", J(mutual(f"{PFX}good_neighbours"), them_idea("gdr_engineers")), ai_base=60, ai_mods=FRIEND_AI)
offer("recognition_india", "india", "The Road to New Delhi",
      "Full diplomatic relations and a trade agreement with the German Democratic Republic; machine tools and engineering scholarships for India.",
      "Recognise the GDR.", J(mutual(f"{PFX}recognition_india"), "set_temp_variable = { influence_target = THIS.id }",
                              us("set_temp_variable = { tag_index = THIS.id }", "set_temp_variable = { percent_change = 5 }", "change_influence_percentage = yes")),
      ai_base=55, ai_mods=DETENTE_AI)
offer("paris_and_london", "sign", "Paris and London",
      "The German Democratic Republic asks for diplomatic relations.",
      "Establish relations.", J(mutual(f"{PFX}diplomatic_relations"), TRADE, us(f"set_country_flag = {PFX}west_recognition")), ai_base=50, ai_mods=DETENTE_AI)
offer("neutral_capitals", "sign", "The Neutral Capitals",
      "The German Democratic Republic asks for diplomatic relations and a trade agreement.",
      "Establish relations.", J(mutual(f"{PFX}diplomatic_relations"), TRADE, us(f"set_country_flag = {PFX}west_recognition")), ai_base=65, ai_mods=DETENTE_AI)
offer("washington", "usa", "An Embassy in Washington",
      "The German Democratic Republic asks for diplomatic relations with the United States, a consular agreement and talks on American property claims.",
      "Establish relations.", J(mutual(f"{PFX}diplomatic_relations"), E.tension(-1)), ai_base=45, ai_mods=DETENTE_AI)
offer("open_socialist_borders", "warsaw", "Visa-Free to Warsaw and Prague",
      "Visa-free travel with identity cards in both directions.",
      "Open the border.", J(mutual(f"{PFX}socialist_neighbours"), them_idea("open_socialist_borders"), our_idea("open_socialist_borders")),
      ai_base=65, ai_mods=FRIEND_AI)
offer("vietnam_aid", "vietnam", "Solidarity with Vietnam",
      "Solidarity shipments of medicine, trucks and hospital equipment, and university places for Vietnamese students.",
      "Accept the shipments.", J(mutual(f"{PFX}solidarity_partner"), them_idea("gdr_solidarity_shipments")), ai_base=85, ai_mods=FRIEND_AI)
offer("vietnam_contract_workers", "vietnam", "Workers from Hanoi",
      "An agreement on the employment and training of Vietnamese workers in the factories of the GDR.",
      "Sign the agreement.", J(contract_workers(), them_idea("trained_workers_from_the_gdr")), ai_base=75, ai_mods=FRIEND_AI)
offer("cuba_trade", "cuba", "Ernst Thälmann Island",
      "IFA trucks, machine tools and a cement works for sugar, citrus and nickel at fixed prices, and apprenticeships for Cuban workers.",
      "Sign the agreement.", J(mutual(f"{PFX}solidarity_partner"), contract_workers(), them_idea("gdr_engineers")), ai_base=80, ai_mods=FRIEND_AI)
offer("nicaragua", "flag", "Sandinista Nicaragua",
      "Doctors, teachers, a hospital and training for the police and state security.",
      "Accept the help.", J(mutual(f"{PFX}solidarity_partner"), them_idea("gdr_hospital"), them_idea("gdr_trained_security")), ai_base=85, ai_mods=FRIEND_AI)
offer("mozambique", "mozambique", "FRELIMO's Mozambique",
      "A treaty of friendship, the Moatize coal mine and a contract-worker agreement.",
      "Sign the treaty.", J(mutual(f"{PFX}solidarity_partner"), them_idea("gdr_trucks_and_machinery"), contract_workers(),
                            us(E.country_dyn("planned_economy", {"energy_gain_multiplier": 0.03}))), ai_base=80, ai_mods=FRIEND_AI)
offer("angola", "angola", "The MPLA in Luanda",
      "Weapons, NVA instructors and trucks for the government in Luanda, paid partly in coffee.",
      "Accept the help.", J(mutual(f"{PFX}solidarity_partner"), them_idea("nva_instructors"), our_idea("tropical_coffee")), ai_base=85, ai_mods=FRIEND_AI)
offer("ethiopia", "ethiopia", "The Ethiopian Revolution",
      "MfS advisers for the Ethiopian state security, trucks and weapons for the Ogaden war - coffee in return.",
      "Accept the help.", J(mutual(f"{PFX}solidarity_partner"), them_idea("mfs_advisers"), our_idea("tropical_coffee")), ai_base=85, ai_mods=FRIEND_AI)
offer("arms_for_oil", "arab", "Solidarity Must Pay",
      "Weapons, trucks and training - for oil and hard currency.",
      "Buy the weapons.", J(them_idea("gdr_arms_deliveries"), mutual(f"{PFX}trading_partner"),
                            us(E.receive(0.003), f"country_event = {{ id = {NS}.63 days = 365 }}", f"country_event = {{ id = {NS}.63 days = 730 }}"),
                            tt("arms_for_oil", "The GDR receives §G0.3%§! of its GDP now and again after one and two years.")),
      ai_base=55, ai_mods=FRIEND_AI)


# ---------------------------------------------------------------- generated code
def numbering():
    from dg_load import OFFERS as DESIGN
    return {k: 100 + i for i, k in enumerate(DESIGN)}


NUM = numbering()


def _tooltip_code(lines, target):
    """the answer's code as the focus shows it (MD: effect_tooltip = { UKR = { CSTO_join = yes } }): in the answer ROOT is the partner and
    FROM is us; in the focus ROOT is us - so ROOT becomes the partner's tag first, then FROM becomes ROOT"""
    return [re.sub(r"\bFROM\b", "ROOT", re.sub(r"\bROOT\b", target, l)) for l in lines]


def offer_lines(key):
    """MD form (SOV_CSTO_enlargement_with_ukr): the proposal goes to the partner, the focus only shows what happens if they accept or reject.
    No effect in the partner's scope - the partner decides in its own answer (multiplayer rule)."""
    o = OFFERS[key]
    out = [f"if = {{ limit = {{ country_exists = {t} NOT = {{ tag = {t} }} }} {t} = {{ country_event = {{ id = {NS}.{NUM[key]} days = 1 }} }} }}"
           for t in o["targets"]]
    t0 = o["targets"][0]
    if len(o["targets"]) > 1:
        LOC[f"{PFX}offer_each_partner_tt"] = "Each partner decides for itself; the terms are the same for every partner."
        out.append(f"custom_effect_tooltip = {PFX}offer_each_partner_tt")
    out += ["custom_effect_tooltip = TT_IF_THEY_ACCEPT", "effect_tooltip = {", f"{t0} = {{"] + _tooltip_code(o["code"], t0) + ["}", "}"]
    if o["decline_code"]:
        out += ["custom_effect_tooltip = TT_IF_THEY_REJECT", "effect_tooltip = {", f"{t0} = {{"] + _tooltip_code(o["decline_code"], t0) + ["}", "}"]
    return out


def offer_events(ev_loc):
    L = []
    for key in sorted(E.R.offers, key=lambda k: NUM[k]):
        o = OFFERS[key]
        eid = f"{NS}.{NUM[key]}"
        L += [f"# COLDWAR | offer {key}", "country_event = {", f"id = {eid}", f"title = {eid}.t", f"desc = {eid}.d", f"picture = {o['pic']}", "",
              "is_triggered_only = yes", ""]
        opts = [(o["accept"], o["code"], o["ai_base"], o["ai_mods"]), (o["decline"], o["decline_code"], 100 - o["ai_base"], "")]
        for i, (t, code, ai, mods) in enumerate(opts):
            L += ["option = {", f"name = {eid}.{'ab'[i]}", "ai_chance = {", f"base = {ai}"] + [m for m in mods.split("\n") if m] + ["}"]
            L += [f'log = "[GetDateText]: [Root.GetName]: event {eid} option {"ab"[i]}"'] + list(code)
            L.append(f"FROM = {{ country_event = {{ id = {NS}.{900 if i == 0 else 901} days = 1 }} }}")
            L.append("}")
        L += ["}", ""]
        ev_loc(eid, o["title"], o["desc"], [x[0] for x in opts])
    return L
