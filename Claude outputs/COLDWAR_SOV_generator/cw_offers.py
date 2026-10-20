# COLDWAR | The 48 offer events of the Soviet tree (English texts).
# Multiplayer rule: the focus only sends the offer. The other country (player or AI) decides,
# and every effect - on both sides - happens in its answer. THIS = the receiver, FROM = the Soviet Union.
from cw_common import *
import cw_effects as E

PIC = {
    "kremlin": "GFX_news_event_SOV_supreme_soviet", "sign": "GFX_news_event_generic_sign_treaty1", "sign2": "GFX_news_event_generic_sign_treaty2",
    "sign3": "GFX_news_event_generic_sign_treaty3", "hand": "GFX_report_event_generic_handshake", "usa": "GFX_report_event_generic_usa_treaty",
    "space": "GFX_russia_israel_soyuz", "navy": "GFX_news_event_ast_navy", "gas": "GFX_baku_gas_lines_country", "pipe": "GFX_CAN_keystone_pipeline_building",
    "china": "GFX_CHI_event_china_russian_flag", "mongol": "GFX_report_event_SOV_mongolia_fortify_border", "india": "GFX_india_flag",
    "vietnam": "GFX_FRA_indochina_war", "warsaw": "GFX_warsaw_exercises", "pact": "GFX_warsaw1_ovd", "poland": "GFX_arm_polish_cooperate",
    "flag": "GFX_soviet_union_flag", "cuba": "GFX_cuba_wants_protec_rus", "syria": "GFX_syrian_arab_army", "iraq": "GFX_report_event_generic_troops_in_iraq",
    "angola": "GFX_news_angolan_civil_war", "ethiopia": "GFX_news_communist_ethiopia", "somalia": "GFX_news_somalia_civil_war",
    "afghan": "GFX_AFG_russian_airlift", "germany": "GFX_warsaw1_frg", "berlin": "GFX_warsaw_bund", "europe": "GFX_report_event_generic_conference",
    "royal": "GFX_report_event_royal_parade", "slavic": "GFX_sov_russ_unified", "army": "GFX_report_event_soviet_tank_parade",
    "research": "GFX_report_event_SOV_national_academy_of_sciences", "missiles": "GFX_news_missilesOnRoad",
}

OFFERS = {}
OFFER_IDEAS = {   # id -> (name, mods, days)
    "arms_limitation": ("Arms Limitation", [("military_spending_cost_factor", -0.10), ("war_support_factor", -0.02)], None),
    "basic_principles": ("Basic Principles of Relations", [("trade_opinion_factor", 0.10), ("stability_factor", 0.01)], 1825),
    "space_cooperation": ("Space Cooperation", [("research_speed_factor", 0.03)], 730),
    "scientific_cooperation": ("Scientific Cooperation", [("research_speed_factor", 0.03)], None),
    "salt_ii": ("SALT II", [("military_spending_cost_factor", -0.05)], None),
    "inf_treaty": ("The INF Treaty", [("military_spending_cost_factor", -0.05)], None),
    "soviet_advisers": ("Soviet Military Advisers", [("army_org_factor", 0.05)], 1095),
    "soviet_arms_package": ("Soviet Arms Package", [("army_defence_factor", 0.05)], 1095),
    "soviet_combat_support": ("Soviet and Cuban Support", [("army_attack_factor", 0.10)], 730),
    "interkosmos_flight": ("Interkosmos Flight", [("stability_factor", 0.05)], 365),
    "soviet_gas": ("Soviet Gas Contract", [("energy_gain_multiplier", 0.05)], None),
    "soviet_garrison": ("Soviet Garrison", [("army_defence_factor", 0.05)], None),
    "oil_for_sugar": ("Oil for Sugar", [("stability_factor", 0.05), ("tax_gain_multiplier_modifier", 0.03)], None),
    "limited_contingent": ("The Limited Contingent", [("army_defence_factor", 0.10), ("army_org_factor", 0.05)], None),
    "afghan_burden": ("The Afghan Burden", [("stability_factor", -0.03), ("war_support_factor", -0.05)], None),
    "slavic_union_member": ("The Slavic Union", [("stability_factor", 0.03), ("political_power_factor", 0.05)], None),
    "union_treaty_member": ("The New Union Treaty", [("stability_factor", 0.03), ("political_power_factor", 0.03)], None),
    # eased start spirits (an accepted treaty softens them)
    "shadow_of_prague_eased": ("The Shadow of Prague", [("research_speed_factor", -0.03), ("drift_defence_factor", 0.10), ("foreign_influence_defense_modifier", 0.10)], None),
    "burden_of_parity_eased": ("The Burden of Parity", [("production_speed_arms_factory_factor", 0.10), ("military_factories_productivity", 0.05),
                                                       ("consumer_goods_factor", 0.025), ("civilian_industry_tax_modifier", -0.025), ("military_spending_cost_factor", 0.05)], None),
    "ussuri_frontier_eased": ("The Ussuri Frontier", [("war_support_factor", 0.05), ("army_personnel_cost_multiplier_modifier", 0.10)], None),
}
for k, (n, m, d) in OFFER_IDEAS.items():
    E.R.ideas[PFX + k] = dict(name=n, mods=m, days=d)

OPINION_EXTRA = {   # opinion modifiers used by the answers
    "COLDWAR_SOV_summit_diplomacy": (10, "Summit Diplomacy"), "COLDWAR_SOV_detente_partner": (15, "Detente Partner"),
    "COLDWAR_SOV_treaty_partner": (20, "Treaty Partner"), "COLDWAR_SOV_friendship_treaty": (25, "Treaty of Friendship"),
    "COLDWAR_SOV_reconciliation": (30, "Reconciliation"), "COLDWAR_SOV_space_partners": (15, "Partners in Space"),
    "COLDWAR_SOV_royal_recognition": (25, "Recognition of the Crown"), "COLDWAR_SOV_brothers_in_arms": (20, "Brothers in Arms"),
    "COLDWAR_SOV_world_market_prices": (-10, "World Market Prices"), "COLDWAR_SOV_olympic_guest": (10, "Olympic Guest"),
    "COLDWAR_SOV_karabakh_support": (25, "Support on Karabakh"), "COLDWAR_SOV_karabakh_betrayal": (-25, "Betrayal on Karabakh"),
}


def offer(key, n, pic, targets, title, desc, accept, code, decline="We must decline.", ai_base=50, ai_mods="", decline_code=""):
    OFFERS[PFX + "offer_" + key] = dict(n=n, pic=PIC.get(pic, pic), targets=targets, title=title, desc=desc, accept=accept,
                                        code=code, decline=decline, ai_base=ai_base, ai_mods=ai_mods, decline_code=decline_code)


# ---------------------------------------------------------------- code helpers (receiver scope, FROM = Soviet Union)
def J(*parts):
    out = []
    for p in parts:
        out += p if isinstance(p, list) else [p]
    return out


def tension(v):
    return [f"set_temp_variable = {{ mdcw_cw_tension_delta = {fmt(v)} }}", "mdcw_cw_add_tension = yes"]


def mutual(mod):
    return [f"add_opinion_modifier = {{ target = FROM modifier = {mod} }}", f"reverse_add_opinion_modifier = {{ target = FROM modifier = {mod} }}"]


TRADE = ["set_temp_variable = { receiver_nation = THIS.id }", "set_temp_variable = { sender_nation = FROM.id }", "set_improved_trade_agreement = yes"]


def sov(lines):
    return ["FROM = {"] + lines + ["}"]


def sov_dyn(group, mods):
    return sov(E.dyn_change(f"{PFX}{group}_modifier", f"{PFX}{group}", mods))


def idea(k, both=False):
    iid = PFX + k
    days = OFFER_IDEAS[k][2]
    add = f"add_timed_idea = {{ idea = {iid} days = {days} }}" if days else f"add_ideas = {iid}"
    own = [f"if = {{ limit = {{ NOT = {{ has_idea = {iid} }} }} {add} }}"]
    return own + (sov(own) if both else [])


def swap(old, new):
    return sov([f"if = {{ limit = {{ has_idea = {PFX}{old} }} swap_ideas = {{ remove_idea = {PFX}{old} add_idea = {PFX}{new} }} }}"])


def remove_ussuri():
    return sov([f"if = {{ limit = {{ has_idea = {PFX}ussuri_frontier }} remove_ideas = {PFX}ussuri_frontier }}",
                f"if = {{ limit = {{ has_idea = {PFX}ussuri_frontier_eased }} remove_ideas = {PFX}ussuri_frontier_eased }}"])


def aid(share):
    """the Soviet Union transfers `share` of its GDP to the receiver"""
    return ["set_temp_variable = { COLDWAR_SOV_transfer_target = THIS.id }"] + \
        sov([f"set_temp_variable = {{ {PFX}gdp_share = {fmt(share)} }}", f"{PFX}transfer_gdp_share = yes"])


def tech(k, cat, uses=1, both=False, bonus=0.5):
    line = f"add_tech_bonus = {{ name = {PFX}offer_{k} bonus = {fmt(bonus)} uses = {uses} category = {cat} }}"
    return ([line] if both else []) + sov([line])


def influence(v):
    return ["set_temp_variable = { influence_target = THIS.id }"] + \
        sov(["set_temp_variable = { tag_index = THIS.id }", f"set_temp_variable = {{ percent_change = {fmt(v)} }}", "change_influence_percentage = yes"])


def first(key, lines):
    """effects that only the first acceptance among several partners brings"""
    return [f"if = {{ limit = {{ NOT = {{ has_global_flag = {PFX}{key}_signed }} }}", f"set_global_flag = {PFX}{key}_signed"] + lines + ["}"]


def tt(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"custom_effect_tooltip = {PFX}{key}_tt"


OPINION_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
              "modifier = { factor = 2 has_opinion = { target = FROM value > 50 } }\n"
              "modifier = { factor = 0.25 has_opinion = { target = FROM value < 0 } }")
DETENTE_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
              "modifier = { factor = 1.5 check_variable = { global.mdcw_cw_tension > 60 } }\n"
              "modifier = { factor = 0.5 check_variable = { global.mdcw_cw_tension < 30 } }")
BLOC_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
           "modifier = { factor = 1.5 is_in_faction_with = FROM }\n"
           "modifier = { factor = 0.3 NOT = { has_government = communism } }")

# ---------------------------------------------------------------- West Germany, France, Europe
offer("gas_for_pipes", 100, "gas", ["GER"], "Gas for Pipes",
      "Moscow proposes a deal without precedent: large-diameter steel pipes from Mannesmann, financed on credit by German banks, in exchange for "
      "Soviet natural gas delivered through the new trunk line from 1973 for twenty years. Industry is enthusiastic; Washington is not.",
      "Sign the pipeline deal.",
      J(idea("soviet_gas"), TRADE, tech("gas_for_pipes", "CAT_infrastructure"), sov_dyn("gosplan", {"trade_opinion_factor": 0.10}),
        sov(E.gdp("receive_gdp_share", 0.005) + E.gdp("change_debt_gdp_share", 0.005))), ai_base=60, ai_mods=DETENTE_AI)
offer("moscow_treaty", 104, "germany", ["GER"], "The Moscow Treaty",
      "The Soviet government offers the Federal Republic a treaty renouncing the use of force and recognising the existing frontiers in Europe, "
      "including the Oder-Neisse line and the inner German border. It would open the door to trade and to an agreement on Berlin.",
      "Sign the treaty.", J(tension(-2), mutual(f"{PFX}treaty_partner"), TRADE, swap("shadow_of_prague", "shadow_of_prague_eased")),
      ai_base=55, ai_mods=DETENTE_AI)
offer("berlin_agreement", 105, "berlin", ["USA", "ENG", "FRA"], "The Four Power Agreement on Berlin",
      "Moscow proposes to settle the Berlin question among the four powers: guaranteed transit between West Berlin and the Federal Republic, "
      "visits for West Berliners in the East, and an end to the crises that have haunted the divided city since 1948.",
      "Join the agreement.",
      J(mutual(f"{PFX}detente_partner"), f"add_to_variable = {{ global.{PFX}berlin_signatures = 1 }}",
        tt("berlin_all_three", "Once §Yall three Western powers§! have signed, Cold War tension falls by §G2§! and the transit routes to Berlin are secured."),
        "if = {", f"limit = {{ check_variable = {{ global.{PFX}berlin_signatures > 2 }} NOT = {{ has_global_flag = {PFX}berlin_agreement }} }}",
        f"set_global_flag = {PFX}berlin_agreement", tension(-2), "}"), ai_base=50, ai_mods=DETENTE_AI)
offer("paris_axis", 108, "europe", ["FRA"], "A Franco-Soviet Partnership",
      "President Pompidou's Paris and Moscow share a mistrust of Anglo-American hegemony. The Soviet side proposes regular consultations "
      "and joint work in electronics, colour television and space research.",
      "Deepen the partnership.", J(mutual(f"{PFX}treaty_partner"), tech("paris_axis", "CAT_electronics", both=True)), ai_base=45, ai_mods=DETENTE_AI)
offer("helsinki", 110, "europe", ["USA", "GER", "FRA", "ENG"], "The Final Act of Helsinki",
      "The Conference on Security and Cooperation in Europe has reached its conclusion. The Final Act recognises the inviolability of frontiers, "
      "opens trade and exchanges, and commits its signatories to respect human rights. Moscow asks us to sign.",
      "Sign the Final Act.",
      J(mutual(f"{PFX}detente_partner"), f"add_to_variable = {{ global.{PFX}helsinki_signatures = 1 }}",
        tt("helsinki_signature", "Every signature lowers Cold War tension by §G1§! (at most §G3§! in total)."),
        f"if = {{ limit = {{ check_variable = {{ global.{PFX}helsinki_signatures < 4 }} }}", tension(-1), "}"), ai_base=60, ai_mods=DETENTE_AI)
offer("pipelines_to_europe", 133, "pipe", ["GER", "ITA", "FRA"], "Long-Term Gas Contracts",
      "The Soviet Ministry of Gas Industry offers long-term supply contracts at stable prices. The gas would come from Siberia through the new export lines; "
      "payment would be in hard currency and machinery.",
      "Sign the contract.",
      J(idea("soviet_gas"), mutual(f"{PFX}summit_diplomacy"), first("pipelines_to_europe", sov_dyn("gosplan", {"oil_export_multiplier_modifier": 0.05}))),
      ai_base=55, ai_mods=DETENTE_AI)
offer("social_democratic_partners", 144, "europe", ["GER", "SWE"], "A Social Democratic Partnership",
      "The new Soviet leadership speaks the language of European social democracy. It proposes party contacts, cultural exchange and a trade agreement "
      "between our governments.", "Accept the partnership.", J(mutual(f"{PFX}treaty_partner"), TRADE), ai_base=55, ai_mods=DETENTE_AI)
offer("royal_houses", 147, "royal", ["ENG", "SPR"], "The Romanovs Return",
      "The restored Russian crown asks the royal houses of Europe for recognition. A Romanov on the throne in Moscow, the Soviet era over: "
      "the courts of Europe must decide how to receive their long-lost cousin.", "Recognise the crown.", J(mutual(f"{PFX}royal_recognition")),
      ai_base=60)

# ---------------------------------------------------------------- the United States
offer("soyuz_apollo", 101, "space", ["USA"], "Apollo-Soyuz",
      "The Soviet Academy of Sciences proposes a joint flight: an American Apollo and a Soviet Soyuz would dock in orbit, and their crews would shake hands "
      "two hundred kilometres above the Earth. A docking module and common procedures would have to be developed together.",
      "Fly together.", J(idea("space_cooperation", both=True), tension(-1), mutual(f"{PFX}space_partners")), ai_base=55, ai_mods=DETENTE_AI)
offer("salt_i", 106, "missiles", ["USA"], "SALT I and the ABM Treaty",
      "After two and a half years of talks in Helsinki and Vienna the delegations have a text: a freeze on strategic missile launchers and a strict limit "
      "on anti-ballistic missile defences. Moscow is ready to sign.",
      "Sign the treaties.", J(idea("arms_limitation", both=True), tension(-3), swap("burden_of_parity", "burden_of_parity_eased")),
      ai_base=55, ai_mods=DETENTE_AI)
offer("moscow_summit", 107, "usa", ["USA"], "Summit in Moscow",
      "The Soviet leadership invites the President of the United States to Moscow. On the table: the Basic Principles of Relations, "
      "agreements on trade, health, the environment and space, and a common commitment to avoid confrontation.",
      "Travel to Moscow.", J(tension(-2), idea("basic_principles", both=True), mutual(f"{PFX}detente_partner")), ai_base=55, ai_mods=DETENTE_AI)
offer("vladivostok", 109, "usa", ["USA"], "The Vladivostok Accord",
      "At an air base near Vladivostok the Soviet side proposes the framework for a second strategic arms treaty: an equal ceiling of 2,400 launchers each.",
      "Agree to the framework.", J(tension(-1), mutual(f"{PFX}summit_diplomacy")), ai_base=55, ai_mods=DETENTE_AI)
offer("salt_ii", 111, "missiles", ["USA"], "SALT II",
      "In Vienna the General Secretary is ready to sign the second strategic arms limitation treaty. Ratification in the Senate will not be easy.",
      "Sign in Vienna.", J(tension(-2), idea("salt_ii", both=True)), ai_base=50, ai_mods=DETENTE_AI)
offer("brezhnev_visit", 132, "usa", ["USA"], "The Prevention of Nuclear War",
      "During his visit to the United States the General Secretary proposes an agreement on the prevention of nuclear war: both powers would consult "
      "each other whenever a crisis threatens to escalate.", "Sign the agreement.", J(tension(-2), mutual(f"{PFX}detente_partner")),
      ai_base=55, ai_mods=DETENTE_AI)
offer("kosygin_summit", 134, "usa", ["USA"], "A Summit with the Premier",
      "Premier Kosygin proposes a summit in the spirit of Glassboro: talks on arms, trade and the conflicts of the Third World, without the ceremonies of a state visit.",
      "Meet the Premier.", J(tension(-2), TRADE, mutual(f"{PFX}detente_partner")), ai_base=55, ai_mods=DETENTE_AI)
offer("chernenko_talks", 138, "usa", ["USA"], "New Talks in Geneva",
      "Moscow proposes to resume the talks on strategic and intermediate-range weapons that broke off over the Euromissiles.",
      "Return to Geneva.", J(tension(-2)), ai_base=45, ai_mods=DETENTE_AI)
offer("inf_treaty", 139, "missiles", ["USA"], "The Zero Option",
      "The General Secretary accepts what Moscow rejected for years: the destruction of all intermediate-range nuclear missiles in Europe, "
      "verified by inspectors of both sides.", "Sign the INF Treaty.", J(tension(-4), idea("inf_treaty", both=True)), ai_base=60, ai_mods=DETENTE_AI)
offer("cocom", 142, "research", ["USA"], "Relaxing the Export Controls",
      "Moscow asks Washington to relax the CoCom lists that bar Western computers and machine tools from the socialist countries, in exchange for "
      "political concessions and an end to the arms race.", "Relax the controls.", J(tension(-2), tech("cocom", "CAT_electronics", uses=2)),
      ai_base=35, ai_mods=DETENTE_AI)
offer("convergence_treaty", 143, "research", ["USA"], "The Convergence Treaty",
      "In the spirit of Sakharov's vision the new Soviet government proposes a treaty of joint disarmament and scientific cooperation: "
      "the two systems would meet halfway instead of preparing to destroy each other.",
      "Sign the treaty.", J(tension(-5), idea("scientific_cooperation", both=True), mutual(f"{PFX}treaty_partner")), ai_base=55, ai_mods=DETENTE_AI)

# ---------------------------------------------------------------- China and Asia
offer("border_talks", 112, "china", ["CHI"], "Border Talks in Beijing",
      "Since October 1969 Soviet and Chinese delegations have been meeting in Beijing. Moscow now proposes a practical step: an end to patrols "
      "in the disputed sectors and a hotline between the frontier commands.",
      "Agree to the measures.", J(tension(-1), swap("ussuri_frontier", "ussuri_frontier_eased")), ai_base=40, ai_mods=OPINION_AI)
offer("sino_soviet_truce", 116, "china", ["CHI"], "An Ideological Truce",
      "The Soviet leadership proposes to end the polemics: no more open letters, no more broadcasts against each other, and a return of the ambassadors. "
      "The question of the socialist camp would remain open, and with it Beijing's own choice of camp.",
      "End the polemics.",
      J(remove_ussuri(), tension(-2), mutual(f"{PFX}reconciliation"),
        tt("truce_camp", "Whether China returns to the Soviet camp remains §YBeijing's own decision§! (Cold War alignment).")),
      ai_base=35, ai_mods=OPINION_AI)
offer("damansky_settlement", 117, "china", ["CHI"], "The Damansky Settlement",
      "Moscow offers to draw the river frontier along the main navigation channel. Damansky Island, called Zhenbao by the Chinese, "
      "would belong to China, and the bloodiest dispute of 1969 would be closed.",
      "Accept the settlement.", J(remove_ussuri(), tension(-1), mutual(f"{PFX}summit_diplomacy")), ai_base=60, ai_mods=OPINION_AI)
offer("shelepin_china", 135, "china", ["CHI"], "Two Camps of the Pure Line",
      "The new General Secretary proposes talks between two parties that both reject revisionism. The border commands would stand down their alert.",
      "Open the talks.", J(mutual(f"{PFX}treaty_partner"), swap("ussuri_frontier", "ussuri_frontier_eased")), ai_base=40, ai_mods=OPINION_AI)
offer("andropov_china", 136, "china", ["CHI"], "Resuming the Consultations",
      "Moscow proposes to resume the consultations between the deputy foreign ministers, suspended since the invasion of Afghanistan.",
      "Resume the consultations.", J(mutual(f"{PFX}detente_partner"), tension(-1)), ai_base=50, ai_mods=OPINION_AI)
offer("stalinist_reconciliation", 140, "china", ["CHI"], "Back to the Pure Line",
      "The new leadership in Moscow has repudiated de-Stalinisation. It proposes a joint return to the line of Lenin and Stalin and an end to the split of 1960.",
      "Restore the friendship.", J(mutual(f"{PFX}reconciliation"), remove_ussuri()), ai_base=45, ai_mods=OPINION_AI)
offer("komsomol_china", 141, "china", ["CHI"], "A Pragmatic Opening",
      "The leaders in Moscow and Beijing both rule without ideology now. A pragmatic rapprochement is proposed: trade, border crossings and quiet frontiers.",
      "Accept the opening.", J(mutual(f"{PFX}treaty_partner"), tension(-1)), ai_base=50, ai_mods=OPINION_AI)
offer("mongolian_garrison", 113, "mongol", ["MON"], "The Mongolian Shield",
      "The Soviet Union proposes to station the 39th Army in Mongolia. The garrison would protect the People's Republic against China; "
      "Moscow would pay for its upkeep and for new roads and barracks.",
      "Welcome the army.",
      J(idea("soviet_garrison"), "give_military_access = FROM", f"set_country_flag = {PFX}garrison_host",
        tt("garrison_aid", "While the garrison stays, the Soviet Union pays us §G0.2%§! of its GDP every year.")), ai_base=80, ai_mods=BLOC_AI)
offer("india_treaty", 114, "india", ["RAJ"], "Treaty of Peace, Friendship and Cooperation",
      "Moscow offers New Delhi a twenty-year treaty: mutual consultations in case of a threat, Soviet arms on easy terms and a trade agreement in rupees.",
      "Sign the treaty.", J(idea("soviet_arms_package"), mutual(f"{PFX}friendship_treaty"), TRADE), ai_base=65, ai_mods=OPINION_AI)
offer("vietnam_treaty", 115, "vietnam", ["VIE"], "A Treaty against Beijing",
      "Moscow offers Hanoi a treaty of friendship and cooperation. The Soviet Pacific Fleet would use Cam Ranh Bay, and both sides would stand "
      "together against Chinese pressure.",
      "Sign the treaty.",
      J(mutual(f"{PFX}friendship_treaty"), "give_military_access = FROM",
        f"if = {{ limit = {{ country_exists = CHI }} CHI = {{ add_opinion_modifier = {{ target = ROOT modifier = {PFX}sino_split }} add_opinion_modifier = {{ target = FROM modifier = {PFX}sino_split }} }} }}"),
      ai_base=60, ai_mods=OPINION_AI)
offer("arms_for_hanoi", 124, "vietnam", ["VIE"], "Arms for Hanoi",
      "Surface-to-air missiles, MiG fighters, trucks and rice: Moscow offers a new aid package for the war against the Americans and their allies.",
      "Accept the aid.", J(idea("soviet_arms_package"), aid(0.004), mutual(f"{PFX}brothers_in_arms")), ai_base=85)
offer("naval_access", 103, "navy", ["SOM", "SYE", "VIE"], "Port Rights for the Soviet Navy",
      "The Soviet Navy asks for the right to use our harbour as a supply point and anchorage. In return Moscow offers economic aid and protection.",
      "Grant the port rights.",
      J("give_military_access = FROM", aid(0.003), sov_dyn("armed_forces", {"navy_max_range_factor": 0.05})), ai_base=60, ai_mods=OPINION_AI)

# ---------------------------------------------------------------- the socialist community
offer("soyuz_pipeline", 118, "pipe", ["DDR", "POL", "CZE", "HUN", "ROM", "BUL"], "The Soyuz Pipeline",
      "Comecon has decided on its largest joint project: a gas pipeline from Orenburg to the western border of the Soviet Union. Every member is asked "
      "to contribute workers, money and machinery, and will receive gas for decades in return.",
      "Join the project.",
      J(f"set_temp_variable = {{ {PFX}gdp_share = 0.002 }}", f"{PFX}pay_gdp_share = yes", idea("soviet_gas"),
        first("soyuz_pipeline", sov_dyn("gosplan", {"production_speed_buildings_factor": 0.03}))), ai_base=70, ai_mods=BLOC_AI)
offer("joint_exercises", 119, "warsaw", ["DDR", "POL", "CZE", "HUN", "ROM", "BUL"], "Shield and Brotherhood in Arms",
      "The High Command of the Warsaw Pact invites our army to the joint manoeuvres of this year.",
      "Send our divisions.", J("army_experience = 25", sov(["army_experience = 25"]), mutual(f"{PFX}brothers_in_arms")), ai_base=75, ai_mods=BLOC_AI)
offer("credits_for_poland", 120, "poland", ["POL"], "Credits for Gierek",
      "Moscow offers raw materials on credit, grain and a hard-currency loan to the new Polish leadership, so that the price increases that toppled Gomulka "
      "can be withdrawn.", "Accept the credits.", J(aid(0.004), "add_stability = 0.05"), ai_base=90)
offer("interkosmos", 121, "space", ["DDR", "POL", "CZE", "HUN", "ROM", "BUL", "CUB", "MON", "VIE"], "Interkosmos",
      "Within the Interkosmos programme a cosmonaut from our country is offered a seat on a Soviet Soyuz. The whole nation would watch the launch from Baikonur.",
      "Send our cosmonaut.", J(idea("interkosmos_flight"), mutual(f"{PFX}space_partners")), ai_base=90)
offer("sugar_for_oil", 125, "cuba", ["CUB"], "Oil for Sugar",
      "Moscow offers a long-term exchange at preferential prices: Soviet oil for Cuban sugar, well above the world market price for the sugar.",
      "Accept the exchange.", J(idea("oil_for_sugar"), sov_dyn("commonwealth", {"tax_gain_multiplier_modifier": -0.01})), ai_base=90)

# ---------------------------------------------------------------- Middle East, Africa, Afghanistan
offer("tartus_supply_point", 102, "syria", ["SYR"], "A Supply Point in Tartus",
      "The Soviet Mediterranean squadron needs a port. Moscow proposes a naval supply point in Tartus, in exchange for military aid and advisers.",
      "Grant the supply point.",
      J("give_military_access = FROM", idea("soviet_advisers"), sov_dyn("armed_forces", {"navy_max_range_factor": 0.05})), ai_base=70, ai_mods=OPINION_AI)
offer("operation_kavkaz", 122, "flag", ["EGY"], "Operation Kavkaz",
      "Moscow offers to send a complete air defence division with SA-3 batteries and MiG-21 squadrons flown by Soviet pilots to the Suez Canal. "
      "The deep-penetration raids of the Israeli air force would end.",
      "Accept the division.",
      J("if = { limit = { NOT = { has_idea = COLDWAR_EGY_operation_kavkaz } } add_ideas = COLDWAR_EGY_operation_kavkaz }", sov(["air_experience = 25"]), tension(1)),
      ai_base=80, ai_mods=OPINION_AI)
offer("egypt_treaty", 123, "sign", ["EGY"], "A Treaty of Friendship with Egypt",
      "Moscow offers Cairo a fifteen-year treaty of friendship and cooperation: consultations, arms and economic aid.",
      "Sign the treaty.", J(mutual(f"{PFX}friendship_treaty"), influence(5)), ai_base=65, ai_mods=OPINION_AI)
offer("iraq_treaty", 126, "iraq", ["IRQ"], "A Treaty of Friendship with Iraq",
      "Moscow offers Baghdad a treaty of friendship and cooperation, with Soviet help for the national oil industry after the nationalisation of the IPC.",
      "Sign the treaty.", J(mutual(f"{PFX}treaty_partner"), TRADE), ai_base=65, ai_mods=OPINION_AI)
offer("syria_arms", 127, "syria", ["SYR"], "An Arms Package for Syria",
      "Tanks, artillery and air defence missiles, delivered with Soviet advisers to train the Syrian army.",
      "Accept the package.", J(idea("soviet_arms_package"), mutual(f"{PFX}treaty_partner")), ai_base=80, ai_mods=OPINION_AI)
offer("gre_advisers", 137, "army", ["EGY", "SYR", "IRQ"], "Soviet Military Advisers",
      "The Ministry of Defence of the USSR offers to send military advisers and to train our officers at Soviet academies.",
      "Accept the advisers.", J(idea("soviet_advisers"), mutual(f"{PFX}detente_partner")), ai_base=70, ai_mods=OPINION_AI)
offer("angola_support", 128, "angola", ["AGL"], "Support for the MPLA",
      "Moscow offers weapons, transport aircraft and coordination with the Cuban expeditionary force against the FNLA, UNITA and their foreign backers.",
      "Accept the support.", J(idea("soviet_combat_support"), mutual(f"{PFX}brothers_in_arms")), ai_base=85)
offer("ethiopia_airlift", 129, "ethiopia", ["ETH"], "An Airlift to Addis Ababa",
      "An air bridge of Antonovs and Ilyushins, Soviet generals and Cuban brigades are offered to the Derg against the Somali invasion.",
      "Accept the airlift.", J(idea("soviet_combat_support"), mutual(f"{PFX}brothers_in_arms")), ai_base=85)
offer("somalia_support", 130, "somalia", ["SOM"], "Arms for Somalia",
      "Moscow offers weapons and advisers for the Somali army, on condition that the naval facilities in Berbera remain at the disposal of the Soviet fleet.",
      "Accept the offer.", J(idea("soviet_combat_support"), "give_military_access = FROM"), ai_base=75, ai_mods=OPINION_AI)
offer("limited_contingent", 131, "afghan", ["AFG"], "The Limited Contingent",
      "The Soviet leadership is ready to answer the repeated requests of the Afghan government: a limited contingent of Soviet troops would secure "
      "the cities and the roads against the insurgency. The decision lies with Kabul.",
      "Request the troops.",
      J(idea("limited_contingent"), sov([f"if = {{ limit = {{ NOT = {{ has_idea = {PFX}afghan_burden }} }} add_ideas = {PFX}afghan_burden }}"]),
        tt("afghan_burden_cost", "§YThe Afghan Burden§! costs the Soviet Union §R0.3%§! of its GDP every month until the troops withdraw.")),
      ai_base=70, ai_mods=OPINION_AI)

# ---------------------------------------------------------------- the Union republics (party trees)
offer("slavic_union", 145, "slavic", ["UKR", "BLR", "KAZ"], "The Slavic Union",
      "The new government in Moscow proposes a union of the three East Slavic peoples and Kazakhstan. Our republic would remain in the Union "
      "with broader autonomy and an equal voice.", "Join the Slavic Union.", J(idea("slavic_union_member"), mutual(f"{PFX}treaty_partner")),
      decline="We will go our own way.", ai_base=70)
offer("slavic_core", 146, "slavic", ["UKR", "BLR"], "A Closer Union of the East Slavs",
      "Moscow proposes a closer union of Russians, Ukrainians and Belarusians within the Soviet state. Our autonomy would stay as it is.",
      "Accept the closer union.", J(mutual(f"{PFX}treaty_partner"), first("slavic_core", E.cohesion(5))), decline="We must decline.", ai_base=65)


# ---------------------------------------------------------------- generated code
def offer_effects():
    L = []
    for key in sorted(E.R.offers):
        o = OFFERS[key]
        names = ", ".join(f"[{t}.GetNameDef]" for t in o["targets"])
        LOC[f"{key}_tt"] = f"We send a proposal to {names}. §YThey decide§! whether to accept; its terms take effect only then."
        L += [f"{key} = {{", f"custom_effect_tooltip = {key}_tt", "hidden_effect = {"]
        for t in o["targets"]:
            L += [f"if = {{ limit = {{ country_exists = {t} NOT = {{ tag = ROOT }} }} {t} = {{ country_event = {{ id = {NS}.{o['n']} days = 1 }} }} }}"]
        L += ["}", "}", ""]
    return L


def offer_events(ev_loc):
    L = []
    for key in sorted(E.R.offers, key=lambda k: OFFERS[k]["n"]):
        o = OFFERS[key]
        eid = f"{NS}.{o['n']}"
        L += [f"# COLDWAR | offer {key}", "country_event = {", f"id = {eid}", f"title = {eid}.t", f"desc = {eid}.d", f"picture = {o['pic']}", "",
              "is_triggered_only = yes", ""]
        opts = [(o["accept"], o["code"], o["ai_base"], o["ai_mods"]), (o["decline"], o["decline_code"], 100 - o["ai_base"], "")]
        for i, (t, code, ai, mods) in enumerate(opts):
            code = code if isinstance(code, list) else [c for c in code.split("\n") if c]
            L += ["option = {", f"name = {eid}.{'ab'[i]}", "ai_chance = {", f"base = {ai}"] + [m for m in mods.split("\n") if m] + ["}"]
            L += [f'log = "[GetDateText]: [Root.GetName]: event {eid} option {"ab"[i]}"'] + code
            L.append(f"FROM = {{ country_event = {{ id = {NS}.{900 if i == 0 else 901} days = 1 }} }}")
            L.append("}")
        L += ["}", ""]
        ev_loc(eid, o["title"], o["desc"], [x[0] for x in opts])
    return L
