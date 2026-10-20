from sov_dsl import *
from d_politics import POWER_IDS

OUT_ROOT = {0: "we_a_democratic_union", 1: "em_the_leading_role_of_the_party",
            3: "na_neither_moscow_nor_washington", 4: "nt_russia_first"}


def root(i, fid, name, sec, prog_key, prog_name, mods, extra=(), c=3, ai="", n=""):
    pre = f"{POWER_IDS[i]}|{OUT_ROOT[OUTLOOK_OF[i]]}"
    F(fid, name, sec, pre, av=inpower(i), c=c, ai=ai,
      e=[pm(prog_key, mods, name=prog_name)] + list(extra),
      n=n or "Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.")


def P(i):
    return inpower(i)


# ------------------------------------------------------------------ 5 Free Councils of Labour
s, A = "wc", P(5)
root(5, "wc_all_power_to_the_councils", "All Power to the Councils", s, "wc", "Council Communism",
     {"stability_factor": -0.03, "consumer_goods_factor": -0.03, "communism_drift": 0.02, "bureaucracy_cost_multiplier_modifier": -0.10})
F("wc_the_novocherkassk_memory", "The Novocherkassk Memory", s, "wc_all_power_to_the_councils", av=A, e=[stab(3), fac("labour_unions", 15)],
  n="Juni 1962: Streik und Massaker von Nowotscherkassk – Pjotr Siuda war dabei.")
F("wc_dissolve_the_ministries", "Dissolve the Ministries", s, "wc_all_power_to_the_councils", av=A, e=[
    fac("industrial_conglomerates", -20), dm("ps", {"bureaucracy_cost_multiplier_modifier": -0.10}),
    idea("self_management_transition", "Transition to Self-Management", {"productivity_growth_modifier": -0.05, "stability_factor": -0.03}, days=365)])
F("wc_the_council_question", "Factory or Village?", s, "wc_the_novocherkassk_memory,wc_dissolve_the_ministries", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("wc_factory_councils", "Factory Councils", s, "wc_the_council_question", mx="wc_the_rural_communes", av=A, e=[
    pm("wc", {"productivity_growth_modifier": 0.04, "civilian_industry_tax_modifier": 0.03})])
F("wc_the_congress_of_councils", "The Congress of Councils", s, "wc_factory_councils", av=A, e=[stab(3), dm("ps", {"political_power_factor": 0.03})])
F("wc_the_rural_communes", "The Rural Communes", s, "wc_the_council_question", mx="wc_factory_councils", av=A, e=[
    pm("wc", {"agricolture_productivity_modifier": 0.08}), fac("farmers", 10)])
F("wc_land_to_the_communes", "Land to the Communes", s, "wc_the_rural_communes", av=A, e=[dm("gp", {"consumer_goods_factor": -0.02}), stab(2)])
F("wc_the_federation_of_councils", "The Federation of Councils", s, "wc_the_congress_of_councils|wc_land_to_the_communes", av=A, e=[coh(5)])
F("wc_abolish_the_nomenklatura", "Abolish the Nomenklatura", s, "wc_the_federation_of_councils", av=A, e=[
    corr(-2), fac("communist_cadres", -25), stab(-3)])
F("wc_workers_militias", "Workers' Militias", s, "wc_the_federation_of_councils", av=A, e=[
    dm("af", {"conscription_factor": 0.05, "army_org_factor": -0.03}), manpower(30000)])
F("wc_leave_the_arms_race", "Leave the Arms Race", s, "wc_workers_militias", av=A, e=[
    law("decrease_military_spending", "Verteidigungshaushalt −1 Stufe"), tension(-2), fac("the_military", -15)])
F("wc_international_of_councils", "International of Councils", s, "wc_abolish_the_nomenklatura", av=A, e=[
    op("SER", 15, key="COLDWAR_SOV_third_way"), dm("cw", {"mdcw_cw_support_effectiveness": 0.05})])
F("wc_the_revolutions_course", "The Revolution's Course", s, "wc_leave_the_arms_race,wc_international_of_councils", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("wc_permanent_revolution", "Permanent Revolution", s, "wc_the_revolutions_course", mx="wc_the_councils_settle", av=A, e=[
    stab(-5), ws(5), dm("cw", {"mdcw_cw_support_effectiveness": 0.15})])
F("wc_the_councils_settle", "The Councils Settle", s, "wc_the_revolutions_course", mx="wc_permanent_revolution", av=A, e=[
    stab(5), dm("gp", {"productivity_growth_modifier": 0.03})])
F("wc_the_commune_state", "The Commune State", s, "wc_permanent_revolution|wc_the_councils_settle", av=A, c=7, e=[
    idea("commune_state", "The Commune State", {"stability_factor": 0.03, "productivity_growth_modifier": 0.03, "communism_drift": 0.02})])

# ------------------------------------------------------------------ 6 Neo-Stalinist Platform
s, A = "ns", P(6)
root(6, "ns_the_iron_line", "The Iron Line", s, "ns", "The Iron Line",
     {"stability_factor": 0.05, "political_power_factor": 0.05, "research_speed_factor": -0.03, "drift_defence_factor": 0.15,
      "productivity_growth_modifier": -0.03})
F("ns_rehabilitate_the_vozhd", "Rehabilitate the Vozhd", s, "ns_the_iron_line", av=A, e=[
    party(6, 5), coh(-4), op("CHI", 10, key="COLDWAR_SOV_stalin_question"), stab(2)],
  n="Peking hat Stalin nie verurteilt – ein unerwartetes Signal an Mao.")
F("ns_the_mobilisation_economy", "The Mobilisation Economy", s, "ns_the_iron_line", av=A, e=[
    build("mil2", 1.2), dm("gp", {"consumer_goods_factor": 0.03, "productivity_growth_modifier": -0.02})])
F("ns_the_question", "Plans or Cadres?", s, "ns_rehabilitate_the_vozhd,ns_the_mobilisation_economy", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("ns_the_new_industrialisation", "The New Industrialisation", s, "ns_the_question", mx="ns_cadres_decide_everything", av=A, e=[
    pm("ns", {"industrial_capacity_factory": 0.05}), stab(-3)])
F("ns_shock_workers", "Shock Workers", s, "ns_the_new_industrialisation", av=A, e=[dm("gp", {"production_factory_efficiency_gain_factor": 0.05}), fac("labour_unions", -5)])
F("ns_cadres_decide_everything", "Cadres Decide Everything", s, "ns_the_question", mx="ns_the_new_industrialisation", av=A, e=[
    fac("communist_cadres", 15), pm("ns", {"political_power_factor": 0.05})])
F("ns_the_new_purge", "The New Purge", s, "ns_cadres_decide_everything", av=A, e=[
    corr(-2), stab(-5), fac("communist_cadres", -10), fac("intelligence_community", 10)])
F("ns_the_patriotic_spirit", "The Great Patriotic Spirit", s, "ns_shock_workers|ns_the_new_purge", av=A, e=[ws(5), dm("af", {"army_morale_factor": 0.03})])
F("ns_the_closed_economy", "The Closed Economy", s, "ns_the_patriotic_spirit", av=A, e=[
    set_law("md_closed_economy", "Handelsgesetz → Geschlossene Wirtschaft"), dm("ps", {"imp_sanction_resistance": 0.10})])
F("ns_collective_farms_tightened", "Tighten the Kolkhozy", s, "ns_the_patriotic_spirit", av=A, e=[
    dm("gp", {"agricolture_productivity_modifier": 0.03}), fac("farmers", -10)])
F("ns_reconcile_with_mao", "A Stalinist Hand to Mao", s, "ns_the_closed_economy", av=A, e=[
    offer("stalinist_reconciliation", "CHI", "Gemeinsame Rückkehr zur „reinen Linie“. Bei Annahme: Meinung +30, „The Ussuri Frontier“ entfällt")])
F("ns_the_iron_curtain_reinforced", "The Iron Curtain Reinforced", s, "ns_collective_farms_tightened", av=A, e=[
    dm("ps", {"drift_defence_factor": 0.10}), dm("gp", {"trade_opinion_factor": -0.10})])
F("ns_the_leadership_question", "A New Vozhd?", s, "ns_reconcile_with_mao,ns_the_iron_curtain_reinforced", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("ns_a_new_vozhd", "A New Vozhd", s, "ns_the_leadership_question", mx="ns_collective_stalinism", av=A, e=[
    pm("ns", {"political_power_factor": 0.10, "stability_factor": 0.03}), trait("new_vozhd", "The New Vozhd")])
F("ns_collective_stalinism", "Collective Stalinism", s, "ns_the_leadership_question", mx="ns_a_new_vozhd", av=A, e=[stab(4), fac("communist_cadres", 10)])
F("ns_the_second_industrialisation", "The Second Industrialisation", s, "ns_a_new_vozhd|ns_collective_stalinism", av=A, c=7, e=[
    idea("second_industrialisation", "The Second Industrialisation", {"industrial_capacity_factory": 0.05, "production_speed_buildings_factor": 0.05,
                                                                       "consumer_goods_factor": 0.02})])

# ------------------------------------------------------------------ 7 Komsomol Vanguard
s, A = "kv", P(7)
root(7, "kv_the_leader_state", "The Leader State", s, "kv", "The Komsomol Vanguard",
     {"political_power_factor": 0.10, "stability_factor": 0.03, "drift_defence_factor": 0.10, "police_cost_multiplier_modifier": 0.05})
F("kv_the_vozhd_principle", "The Vozhd Principle", s, "kv_the_leader_state", av=A, e=[trait("vozhd", "Vozhd"), pp(50)])
F("kv_the_youth_vanguard", "The Youth Vanguard", s, "kv_the_leader_state", av=A, e=[manpower(20000), dm("gp", {"production_speed_buildings_factor": 0.03})])
F("kv_the_pillar", "Which Pillar?", s, "kv_the_vozhd_principle,kv_the_youth_vanguard", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("kv_the_security_state", "The Security State", s, "kv_the_pillar", mx="kv_mass_mobilisation", av=A, e=[
    pm("kv", {"mdcw_cw_ideological_defence": 0.15}), fac("intelligence_community", 15)])
F("kv_the_informers", "Every Third an Informer", s, "kv_the_security_state", av=A, e=[dm("ps", {"foreign_subversive_activites": -0.15}), stab(-2)])
F("kv_mass_mobilisation", "Mass Mobilisation", s, "kv_the_pillar", mx="kv_the_security_state", av=A, e=[
    pm("kv", {"war_support_factor": 0.05}), party(7, 5)])
F("kv_the_great_campaigns", "The Great Campaigns", s, "kv_mass_mobilisation", av=A, e=[dm("gp", {"production_speed_buildings_factor": 0.05}), stab(2)])
F("kv_purge_the_old_men", "Purge the Old Men", s, "kv_the_informers|kv_the_great_campaigns", av=A, e=[
    fac("communist_cadres", -20), rmidea("stability_of_cadres", "Stability of Cadres"), stab(-3)])
F("kv_construction_battalions", "Construction Battalions", s, "kv_purge_the_old_men", av=A, e=[build("inf2"), dm("gp", {"production_speed_infrastructure_factor": 0.10})])
F("kv_discipline_in_the_factories", "Discipline in the Factories", s, "kv_purge_the_old_men", av=A, e=[dm("gp", {"productivity_growth_modifier": 0.04}), fac("labour_unions", -10)])
F("kv_the_iron_fist_abroad", "The Iron Fist Abroad", s, "kv_construction_battalions", av=A, e=[tension(2), dm("af", {"army_attack_factor": 0.02})])
F("kv_the_eastern_opening", "The Eastern Opening", s, "kv_discipline_in_the_factories", av=A, e=[
    offer("komsomol_china", "CHI", "Pragmatische Annäherung zweier Führerstaaten. Bei Annahme: Meinung +20, Spannung −1")])
F("kv_the_succession", "After the Vozhd", s, "kv_the_iron_fist_abroad,kv_the_eastern_opening", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("kv_heir_semichastny", "Heir: Semichastny", s, "kv_the_succession", mx="kv_return_to_the_party", av=A, e=[flag("heir_semichastny"), fac("intelligence_community", 5)])
F("kv_return_to_the_party", "Return to the Party", s, "kv_the_succession", mx="kv_heir_semichastny", av=A, e=[rp(4, "Alexander Shelepin"), stab(3)],
  n="Die Herrschaft kehrt in die KPdSU zurück; das Plenum kann neu entscheiden.")
F("kv_the_vanguard_state", "The Vanguard State", s, "kv_heir_semichastny", av=A, c=7, e=[
    idea("vanguard_state", "The Vanguard State", {"political_power_factor": 0.05, "stability_factor": 0.04, "drift_defence_factor": 0.10})])

# ------------------------------------------------------------------ 0 Systems Directorate
s, A = "sd", P(0)
root(0, "sd_the_systems_men_rule", "The Systems Men Rule", s, "sd", "The Systems Directorate",
     {"productivity_growth_modifier": 0.05, "research_speed_factor": 0.03, "stability_factor": -0.03, "democratic_drift": 0.01})
F("sd_the_iiasa_partnership", "The IIASA Partnership", s, "sd_the_systems_men_rule", av=A, e=[dm("ps", {"research_speed_factor": 0.03}), op("USA", 10, key="COLDWAR_SOV_detente")],
  n="Das Internationale Institut für Angewandte Systemanalyse (Laxenburg, 1972).")
F("sd_the_managerial_revolution", "The Managerial Revolution", s, "sd_the_systems_men_rule", av=A, e=[
    fac("communist_cadres", -15), dm("gp", {"productivity_growth_modifier": 0.03})])
F("sd_the_form", "Technocracy or Corporation?", s, "sd_the_iiasa_partnership,sd_the_managerial_revolution", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("sd_the_technocratic_state", "The Technocratic State", s, "sd_the_form", mx="sd_the_corporate_union", av=A, e=[
    pm("sd", {"political_power_factor": 0.05, "police_cost_multiplier_modifier": 0.05}), stab(3)])
F("sd_the_corporate_union", "The Corporate Union", s, "sd_the_form", mx="sd_the_technocratic_state", av=A, e=[
    pm("sd", {"receiving_investment_cost_modifier": -0.15, "trade_opinion_factor": 0.10}), debt(1.0)])
F("sd_western_licences", "Western Licences", s, "sd_the_technocratic_state|sd_the_corporate_union", av=A, e=[
    tech(["CAT_production_lines", "CAT_electronics"], 1, 50)])
F("sd_the_computer_ministry", "The Computer Ministry", s, "sd_western_licences", av=A, e=[build("chip", 1.0), tech("CAT_computing", 1, 50)])
F("sd_rationalise_the_army", "Rationalise the Army", s, "sd_the_technocratic_state|sd_the_corporate_union", av=A, e=[
    law("decrease_military_spending", "Verteidigungshaushalt −1 Stufe"), dm("af", {"equipment_cost_multiplier_modifier": -0.05}), fac("the_military", -10)])
F("sd_cocom_relaxation", "Lift the CoCom Lists", s, "sd_rationalise_the_army", av=A, e=[
    offer("cocom", "USA", "Lockerung der westlichen Exportkontrollen. Bei Annahme: Forschungsbonus Elektronik ×2, Spannung −2")])
F("sd_the_future_of_the_directorate", "The Future of the Directorate", s, "sd_the_computer_ministry,sd_cocom_relaxation", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("sd_the_permanent_directorate", "The Permanent Directorate", s, "sd_the_future_of_the_directorate", mx="sd_hand_over_to_parliament", av=A, e=[
    pm("sd", {"stability_factor": 0.03}), pp(50)])
F("sd_hand_over_to_parliament", "Hand Over to Parliament", s, "sd_the_future_of_the_directorate", mx="sd_the_permanent_directorate", av=A, e=[
    elections(True), rp(2), stab(-3)], n="Übergabe an Partei 2 (Liberale).")
F("sd_the_managed_union", "The Managed Union", s, "sd_the_permanent_directorate", av=A, c=7, e=[
    idea("managed_union", "The Managed Union", {"productivity_growth_modifier": 0.05, "research_speed_factor": 0.03})])

# ------------------------------------------------------------------ 1 People's Labour Union (NTS)
s, A = "nts", P(1)
root(1, "nts_the_solidarists_return", "The Solidarists Return", s, "nts", "Russian Solidarism",
     {"democratic_drift": 0.02, "stability_factor": -0.03, "trade_opinion_factor": 0.10},
     extra=[custom("Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 60)", ["the_clergy"])])
F("nts_the_church_restored", "The Church Restored", s, "nts_the_solidarists_return", av=A, e=[stab(3), fac("the_clergy", 10), party(23, 2)])
F("nts_private_property", "Private Property Restored", s, "nts_the_solidarists_return", av=A, e=[
    dm("gp", {"productivity_growth_modifier": 0.05, "consumer_goods_factor": -0.03}), fac("communist_cadres", -20)])
F("nts_the_model", "Solidarism or Free Market?", s, "nts_the_church_restored,nts_private_property", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("nts_solidarist_corporatism", "Solidarist Corporatism", s, "nts_the_model", mx="nts_free_market_russia", av=A, e=[
    pm("nts", {"stability_factor": 0.03}), fac("labour_unions", 10)])
F("nts_free_market_russia", "A Free Market", s, "nts_the_model", mx="nts_solidarist_corporatism", av=A, e=[
    pm("nts", {"productivity_growth_modifier": 0.05, "stability_factor": -0.02}), set_law("mixed_economy", "Handelsgesetz → Gemischte Wirtschaft")])
F("nts_decollectivisation", "Decollectivisation", s, "nts_solidarist_corporatism|nts_free_market_russia", av=A, e=[
    dm("gp", {"agricolture_productivity_modifier": 0.10}), fac("farmers", 15), stab(-2)])
F("nts_the_constituent_assembly", "The Constituent Assembly", s, "nts_decollectivisation", av=A, e=[elections(True), stab(-3), coh(-3)],
  n="Die Antwort auf 1918.")
F("nts_into_the_west", "Into the West", s, "nts_the_constituent_assembly", av=A, e=[
    cw_join("west", "Cold War: Wechsel in den Westblock"), op("GER", 20, key="COLDWAR_SOV_detente"), tension(-3)])
F("nts_the_republics_question", "The Republics Question", s, "nts_into_the_west", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("nts_a_russian_federation", "A Russian Federation", s, "nts_the_republics_question", mx="nts_a_union_of_nations", av=A, e=[
    coh(-15), stab(5), txt("Jede Republik erhält ein Angebot zur Unabhängigkeit (Event; Spieler-Republiken entscheiden selbst)")])
F("nts_a_union_of_nations", "A Union of Nations", s, "nts_the_republics_question", mx="nts_a_russian_federation", av=A, e=[coh(8), stab(-2)])
F("nts_the_new_russia", "The New Russia", s, "nts_a_russian_federation|nts_a_union_of_nations", av=A, c=7, e=[
    idea("new_russia", "The New Russia", {"productivity_growth_modifier": 0.04, "trade_opinion_factor": 0.10, "stability_factor": 0.02})])

# ------------------------------------------------------------------ 2 Committee for Human Rights (Sakharov)
s, A = "chr", P(2)
root(2, "chr_the_committee_governs", "The Committee Governs", s, "chr", "Sakharov's Convergence",
     {"research_speed_factor": 0.05, "democratic_drift": 0.03, "stability_factor": -0.05, "trade_opinion_factor": 0.15})
F("chr_release_the_prisoners", "Release the Prisoners of Conscience", s, "chr_the_committee_governs", av=A, e=[
    stab(-2), op("USA", 20, key="COLDWAR_SOV_human_rights"), rmidea("dissent", "Samizdat and Dissent")])
F("chr_end_the_party_monopoly", "End the Party Monopoly", s, "chr_the_committee_governs", av=A, e=[
    elections(True), fac("communist_cadres", -25), party(4, -10)])
F("chr_the_economic_question", "Convergence or Social Market?", s, "chr_release_the_prisoners,chr_end_the_party_monopoly", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("chr_the_convergence_economy", "The Convergence Economy", s, "chr_the_economic_question", mx="chr_the_social_market", av=A, e=[
    pm("chr", {"productivity_growth_modifier": 0.05}), set_law("mixed_economy", "Handelsgesetz → Gemischte Wirtschaft")])
F("chr_the_social_market", "The Social Market", s, "chr_the_economic_question", mx="chr_the_convergence_economy", av=A, e=[
    pm("chr", {"stability_factor": 0.03, "social_cost_multiplier_modifier": 0.05})])
F("chr_the_rule_of_law", "The Rule of Law", s, "chr_the_convergence_economy|chr_the_social_market", av=A, e=[
    corr(-1), dm("ps", {"police_cost_multiplier_modifier": -0.05})])
F("chr_a_free_press", "A Free Press", s, "chr_the_rule_of_law", av=A, e=[dm("ps", {"drift_defence_factor": -0.10, "research_speed_factor": 0.02})])
F("chr_disarmament", "Disarmament", s, "chr_the_committee_governs", av=A, e=[
    law("decrease_military_spending", "Verteidigungshaushalt −1 Stufe"), law("decrease_military_spending", "Verteidigungshaushalt −1 Stufe"),
    tension(-5), fac("the_military", -20)])
F("chr_the_convergence_treaty", "The Convergence Treaty", s, "chr_disarmament", av=A, e=[
    offer("convergence_treaty", "USA", "Gemeinsame Abrüstung und Wissenschaftskooperation. Bei Annahme: Spannung −5, beide +3 % Forschung")])
F("chr_the_union_question", "The Right to Leave", s, "chr_a_free_press,chr_the_convergence_treaty", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("chr_the_right_of_secession", "The Right of Secession", s, "chr_the_union_question", mx="chr_a_democratic_federation", av=A, e=[
    coh(-10), stab(3), txt("Republiken erhalten ein Austrittsangebot (Event)")])
F("chr_a_democratic_federation", "A Democratic Federation", s, "chr_the_union_question", mx="chr_the_right_of_secession", av=A, e=[coh(6)])
F("chr_join_the_free_world", "Join the Free World", s, "chr_the_right_of_secession|chr_a_democratic_federation", av=A, e=[
    cw_join("west", "Cold War: Wechsel in den Westblock"), tension(-3)])
F("chr_the_open_society", "The Open Society", s, "chr_join_the_free_world", av=A, c=7, e=[
    idea("open_society", "The Open Society", {"research_speed_factor": 0.05, "trade_opinion_factor": 0.10, "stability_factor": 0.02})])

# ------------------------------------------------------------------ 3 Union of Democratic Socialists (Roy Medvedev)
s, A = "uds", P(3)
root(3, "uds_socialist_democracy", "Socialist Democracy", s, "uds", "Socialist Democracy",
     {"democratic_drift": 0.02, "stability_factor": -0.02, "research_speed_factor": 0.03, "consumer_goods_factor": -0.02})
F("uds_multi_party_socialism", "Multi-Party Socialism", s, "uds_socialist_democracy", av=A, e=[elections(True), party(3, 5)])
F("uds_the_rehabilitations", "The Rehabilitations", s, "uds_socialist_democracy", av=A, e=[stab(-2), dm("ps", {"research_speed_factor": 0.02})],
  n="Medwedews „Lasst die Geschichte urteilen“ als Staatsprogramm.")
F("uds_the_model", "Rome or Stockholm?", s, "uds_multi_party_socialism,uds_the_rehabilitations", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("uds_eurocommunist_alliance", "The Eurocommunist Alliance", s, "uds_the_model", mx="uds_the_scandinavian_model", av=A, e=[
    op("ITA", 20, key="COLDWAR_SOV_eurocommunism"), op("FRA", 15, key="COLDWAR_SOV_eurocommunism"), pm("uds", {"trade_opinion_factor": 0.05})])
F("uds_the_scandinavian_model", "The Scandinavian Model", s, "uds_the_model", mx="uds_eurocommunist_alliance", av=A, e=[
    pm("uds", {"social_cost_multiplier_modifier": 0.05, "stability_factor": 0.05})])
F("uds_workers_participation", "Workers' Participation", s, "uds_eurocommunist_alliance|uds_the_scandinavian_model", av=A, e=[
    dm("gp", {"productivity_growth_modifier": 0.03}), fac("labour_unions", 10)])
F("uds_cut_the_defence_budget", "Cut the Defence Budget", s, "uds_workers_participation", av=A, e=[
    law("decrease_military_spending", "Verteidigungshaushalt −1 Stufe"), fac("the_military", -10), tension(-2)])
F("uds_detente_partners", "Detente Partners", s, "uds_cut_the_defence_budget", av=A, e=[
    offer("social_democratic_partners", ["GER", "SWE"], "Sozialdemokratische Partnerschaft. Bei Annahme: Meinung +20, Handelsabkommen")])
F("uds_the_final_question", "How Far?", s, "uds_detente_partners", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("uds_socialism_remains", "Socialism Remains", s, "uds_the_final_question", mx="uds_full_democracy", av=A, e=[stab(3), party(3, 3)])
F("uds_full_democracy", "Full Democracy", s, "uds_the_final_question", mx="uds_socialism_remains", av=A, e=[stab(-2), dm("ps", {"democratic_drift": 0.02})])
F("uds_socialism_with_a_human_face", "Socialism with a Human Face", s, "uds_socialism_remains|uds_full_democracy", av=A, c=7, e=[
    idea("human_face", "Socialism with a Human Face", {"stability_factor": 0.03, "research_speed_factor": 0.03, "productivity_growth_modifier": 0.02})])

# ------------------------------------------------------------------ 13 Gosplan Technocracy
s, A = "gt", P(13)
root(13, "gt_the_planners_govern", "The Planners Govern", s, "gt", "Rule of the Planners",
     {"production_factory_efficiency_gain_factor": 0.05, "bureaucracy_cost_multiplier_modifier": -0.05, "political_power_factor": -0.03})
F("gt_ideology_retired", "Ideology Retired", s, "gt_the_planners_govern", av=A, e=[
    fac("communist_cadres", -20), dm("ps", {"drift_defence_factor": -0.05}), dm("gp", {"productivity_growth_modifier": 0.03})])
F("gt_the_material_balances", "The Material Balances", s, "gt_the_planners_govern", av=A, e=[dm("gp", {"production_factory_efficiency_gain_factor": 0.03})])
F("gt_the_model", "Engineers or Resources?", s, "gt_ideology_retired,gt_the_material_balances", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("gt_the_engineers_state", "The Engineers' State", s, "gt_the_model", mx="gt_the_resource_state", av=A, e=[pm("gt", {"industrial_capacity_factory": 0.05})])
F("gt_the_resource_state", "The Resource State", s, "gt_the_model", mx="gt_the_engineers_state", av=A, e=[
    pm("gt", {"oil_export_multiplier_modifier": 0.10, "resource_export_multiplier_modifier": 0.05})])
F("gt_siberian_projects", "Siberian Projects", s, "gt_the_engineers_state|gt_the_resource_state", av=A, e=[gdp(1.5), build("inf2")])
F("gt_military_conversion", "Military Conversion", s, "gt_siberian_projects", av=A, e=[
    law("decrease_military_spending", "Verteidigungshaushalt −1 Stufe"), dm("gp", {"consumer_goods_factor": -0.03}), fac("defense_industry", -10)])
F("gt_trade_with_all", "Trade with All", s, "gt_siberian_projects", av=A, e=[dm("gp", {"trade_opinion_factor": 0.10}), tension(-1)])
F("gt_the_future", "Technocracy Forever?", s, "gt_military_conversion,gt_trade_with_all", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("gt_permanent_technocracy", "Permanent Technocracy", s, "gt_the_future", mx="gt_return_to_party_rule", av=A, e=[pm("gt", {"stability_factor": 0.03})])
F("gt_return_to_party_rule", "Return to Party Rule", s, "gt_the_future", mx="gt_permanent_technocracy", av=A, e=[rp(4), stab(3)])
F("gt_the_planned_society", "The Planned Society", s, "gt_permanent_technocracy", av=A, c=7, e=[
    idea("planned_society", "The Planned Society", {"production_factory_max_efficiency_factor": 0.05, "productivity_growth_modifier": 0.03})])

# ------------------------------------------------------------------ 14 Live Not by Lies (Solzhenitsyn)
s, A = "lnl", P(14)
root(14, "lnl_live_not_by_lies", "Live Not by Lies", s, "lnl", "Repentance and Self-Limitation",
     {"stability_factor": 0.03, "research_speed_factor": -0.02, "communism_drift": -0.02, "nationalist_drift": 0.01},
     extra=[custom("Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 65)", ["the_clergy"])])
F("lnl_letter_to_the_soviet_leaders", "Letter to the Soviet Leaders", s, "lnl_live_not_by_lies", av=A, e=[
    party(4, -10), fac("communist_cadres", -20), stab(2)], n="1973: Ideologie aufgeben, den Nordosten erschließen, das Imperium beenden.")
F("lnl_the_north_east", "Develop the North-East", s, "lnl_live_not_by_lies", av=A, e=[gdp(1.0), build("inf2"), dm("gp", {"resource_export_multiplier_modifier": 0.03})])
F("lnl_the_form", "Orthodoxy or Zemstvo?", s, "lnl_letter_to_the_soviet_leaders,lnl_the_north_east", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("lnl_authoritarian_orthodoxy", "Authoritarian Orthodoxy", s, "lnl_the_form", mx="lnl_the_zemstvo", av=A, e=[
    pm("lnl", {"stability_factor": 0.05, "drift_defence_factor": 0.10}), fac("the_clergy", 10)])
F("lnl_the_zemstvo", "The Zemstvo Revived", s, "lnl_the_form", mx="lnl_authoritarian_orthodoxy", av=A, e=[
    pm("lnl", {"stability_factor": 0.02, "democratic_drift": 0.01}), dm("ps", {"bureaucracy_cost_multiplier_modifier": -0.05})])
F("lnl_end_the_foreign_adventures", "End the Foreign Adventures", s, "lnl_authoritarian_orthodoxy|lnl_the_zemstvo", av=A, e=[
    dm("cw", {"tax_gain_multiplier_modifier": 0.05, "foreign_influence_modifier": -0.10}), tension(-2)])
F("lnl_the_village_restored", "The Village Restored", s, "lnl_end_the_foreign_adventures", av=A, e=[
    dm("gp", {"agricolture_productivity_modifier": 0.05}), fac("farmers", 10)])
F("lnl_release_the_republics", "Release the Non-Slavic Republics", s, "lnl_end_the_foreign_adventures", av=A, e=[
    coh(-20), stab(5), txt("Baltikum, Kaukasus und Zentralasien erhalten Unabhängigkeitsangebote (Event)")],
  n="Solschenizyns „Russlands Weg aus der Krise“ (1990), zwanzig Jahre früher.")
F("lnl_the_slavic_question", "The Slavic Question", s, "lnl_the_village_restored,lnl_release_the_republics", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("lnl_the_slavic_union", "The Slavic Union", s, "lnl_the_slavic_question", mx="lnl_russia_alone", av=A, e=[
    offer("slavic_union", ["UKR", "BLR", "KAZ"], "Union der drei ostslawischen Völker (und Kasachstans). Bei Annahme: bleibt Unionsrepublik mit erweiterter Autonomie")])
F("lnl_russia_alone", "Russia Alone", s, "lnl_the_slavic_question", mx="lnl_the_slavic_union", av=A, e=[stab(3), coh(-10)])
F("lnl_repentance_and_self_limitation", "Repentance and Self-Limitation", s, "lnl_the_slavic_union|lnl_russia_alone", av=A, c=7, e=[
    idea("self_limitation", "Repentance and Self-Limitation", {"stability_factor": 0.05, "consumer_goods_factor": -0.02, "war_support_factor": -0.03})])

# ------------------------------------------------------------------ 15 The Red Directors (Shchelokov)
s, A = "rd", P(15)
root(15, "rd_the_directors_take_over", "The Directors Take Over", s, "rd", "The Red Directors",
     {"corporate_tax_income_multiplier_modifier": 0.10, "corruption_cost_factor": 0.10, "productivity_growth_modifier": 0.03, "consumer_goods_factor": -0.03},
     extra=[custom("Fügt die Fraktion „Schattenwirtschaft“ hinzu (`oligarchs`, Meinung 70)", ["oligarchs"])])
F("rd_shadow_capitalism", "Shadow Capitalism Legalised", s, "rd_the_directors_take_over", av=A, e=[
    idea("shadow_capitalism", "Shadow Capitalism", {"tax_gain_multiplier_modifier": 0.03, "corruption_cost_factor": 0.10, "consumer_goods_factor": -0.03},
         swap="The Second Economy"), fac("oligarchs", 10)])
F("rd_the_mvd_state", "The MVD State", s, "rd_the_directors_take_over", av=A, e=[stab(2), dm("ps", {"police_cost_multiplier_modifier": -0.05})])
F("rd_the_model", "Nomenklatura or Clans?", s, "rd_shadow_capitalism,rd_the_mvd_state", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("rd_nomenklatura_privatisation", "Nomenklatura Privatisation", s, "rd_the_model", mx="rd_the_clan_economy", av=A, e=[
    pm("rd", {"productivity_growth_modifier": 0.05}), fac("communist_cadres", 15), stab(-3)])
F("rd_the_clan_economy", "The Clan Economy", s, "rd_the_model", mx="rd_nomenklatura_privatisation", av=A, e=[coh(5), corr(1)])
F("rd_cotton_and_caviar", "Cotton and Caviar", s, "rd_nomenklatura_privatisation|rd_the_clan_economy", av=A, e=[dm("gp", {"resource_export_multiplier_modifier": 0.10})])
F("rd_the_directors_banks", "The Directors' Banks", s, "rd_cotton_and_caviar", av=A, e=[
    dm("gp", {"interest_rate_multiplier_modifier": -0.05, "office_park_income_tax_modifier": 0.05}), build("off", 0.6)])
F("rd_western_accounts", "Western Accounts", s, "rd_cotton_and_caviar", av=A, e=[gdp(0.5), fac("oligarchs", 10), stab(-2)],
  n="Kapitalflucht: die Direktoren sichern sich ab.")
F("rd_the_question", "Who Owns the Union?", s, "rd_the_directors_banks,rd_western_accounts", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("rd_the_directors_republic", "The Directors' Republic", s, "rd_the_question", mx="rd_buy_the_people", av=A, e=[pm("rd", {"corporate_tax_income_multiplier_modifier": 0.05})])
F("rd_buy_the_people", "Buy the People", s, "rd_the_question", mx="rd_the_directors_republic", av=A, e=[stab(5), dm("gp", {"social_cost_multiplier_modifier": 0.05})])
F("rd_the_corporate_union", "The Corporate Union", s, "rd_the_directors_republic|rd_buy_the_people", av=A, c=7, e=[
    idea("corporate_union", "The Corporate Union", {"productivity_growth_modifier": 0.04, "corruption_cost_factor": 0.05, "tax_gain_multiplier_modifier": 0.03})])

# ------------------------------------------------------------------ 16 Free Enterprise League
s, A = "fel", P(16)
root(16, "fel_the_free_enterprise_cabinet", "The Free Enterprise Cabinet", s, "fel", "Free Enterprise",
     {"productivity_growth_modifier": 0.08, "stability_factor": -0.06, "consumer_goods_factor": -0.04}, ai="0")
F("fel_free_the_prices", "Free the Prices", s, "fel_the_free_enterprise_cabinet", av=A, ai="0", e=[stab(-5), rmidea("second_economy", "The Second Economy"), dm("gp", {"tax_gain_multiplier_modifier": 0.05})])
F("fel_the_rouble_convertible", "A Convertible Rouble", s, "fel_the_free_enterprise_cabinet", av=A, ai="0", e=[dm("gp", {"trade_opinion_factor": 0.10, "interest_rate_multiplier_modifier": 0.05})])
F("fel_the_speed", "Shock or Steps?", s, "fel_free_the_prices,fel_the_rouble_convertible", av=A, ai="0", c=3, e=[txt("Gegenseitig exklusiv")])
F("fel_shock_therapy", "Shock Therapy", s, "fel_the_speed", mx="fel_step_by_step", av=A, ai="0", e=[pm("fel", {"productivity_growth_modifier": 0.05}), stab(-8)])
F("fel_step_by_step", "Step by Step", s, "fel_the_speed", mx="fel_shock_therapy", av=A, ai="0", e=[pm("fel", {"stability_factor": 0.03})])
F("fel_voucher_privatisation", "Voucher Privatisation", s, "fel_shock_therapy|fel_step_by_step", av=A, ai="0", e=[
    dm("gp", {"corporate_tax_income_multiplier_modifier": 0.10}), fac("communist_cadres", -20)])
F("fel_open_to_investment", "Open to Investment", s, "fel_voucher_privatisation", av=A, ai="0", e=[dm("gp", {"receiving_investment_cost_modifier": -0.20}), debt(1.0)])
F("fel_the_market_union", "The Market Union", s, "fel_open_to_investment", av=A, ai="0", c=7, e=[
    idea("market_union", "The Market Union", {"productivity_growth_modifier": 0.05, "trade_opinion_factor": 0.10})])

# ------------------------------------------------------------------ 17 Friends of Baikal
s, A = "fob", P(17)
root(17, "fob_the_green_cabinet", "The Green Cabinet", s, "fob", "Friends of Baikal",
     {"stability_factor": 0.02, "productivity_growth_modifier": -0.02, "renewable_energy_gain_multiplier": 0.10})
F("fob_save_baikal", "Save Baikal", s, "fob_the_green_cabinet", av=A, e=[stab(2), dm("gp", {"industrial_capacity_factory": -0.01}), party(17, 3)],
  n="Das Zellstoffkombinat Baikalsk wird geschlossen.")
F("fob_stop_the_rivers", "Stop the River Reversal", s, "fob_the_green_cabinet", av=A, e=[stab(2), coh(-2)])
F("fob_the_path", "Green Socialism or Conservation?", s, "fob_save_baikal,fob_stop_the_rivers", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("fob_green_socialism", "Green Socialism", s, "fob_the_path", mx="fob_conservation_first", av=A, e=[pm("fob", {"stability_factor": 0.02, "consumer_goods_factor": -0.02})])
F("fob_conservation_first", "Conservation First", s, "fob_the_path", mx="fob_green_socialism", av=A, e=[
    set_law("full_environmental_protections", "Bergbaugesetz → Voller Umweltschutz"), pm("fob", {"stability_factor": 0.03})])
F("fob_save_the_aral", "Save the Aral", s, "fob_green_socialism|fob_conservation_first", av=A, e=[coh(4), dm("gp", {"agriculture_tax_modifier": -0.03})])
F("fob_close_semipalatinsk", "Close Semipalatinsk", s, "fob_save_the_aral", av=A, e=[coh(4), tension(-1), fac("the_military", -10)])
F("fob_the_rbmk_question", "The Reactor Question", s, "fob_save_the_aral", av=A, e=[
    dm("gp", {"energy_gain_multiplier": -0.05}), txt("Entfernt das RBMK-Risikoflag `COLDWAR_SOV_rbmk`")])
F("fob_the_green_union", "The Green Union", s, "fob_close_semipalatinsk,fob_the_rbmk_question", av=A, c=7, e=[
    idea("green_union", "The Green Union", {"stability_factor": 0.04, "renewable_energy_gain_multiplier": 0.10})])

# ------------------------------------------------------------------ 18 Socialist Market Commonwealth (Yakovlev)
s, A = "smc", P(18)
root(18, "smc_the_market_socialists", "The Market Socialists", s, "smc", "Socialist Market Commonwealth",
     {"productivity_growth_modifier": 0.05, "consumer_goods_factor": -0.03, "democratic_drift": 0.01})
F("smc_an_early_glasnost", "An Early Glasnost", s, "smc_the_market_socialists", av=A, e=[dm("ps", {"research_speed_factor": 0.03, "drift_defence_factor": -0.05}), stab(-2)])
F("smc_the_cooperative_law", "The Cooperative Law", s, "smc_the_market_socialists", av=A, e=[
    idea("cooperative_sector", "Cooperative Sector", {"tax_gain_multiplier_modifier": 0.03, "consumer_goods_factor": -0.03, "corruption_cost_factor": 0.05},
         swap="The Second Economy")])
F("smc_the_model", "Belgrade or Budapest?", s, "smc_an_early_glasnost,smc_the_cooperative_law", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("smc_self_management", "Self-Management", s, "smc_the_model", mx="smc_the_new_mechanism", av=A, e=[pm("smc", {"stability_factor": 0.02}), fac("labour_unions", 10), op("SER", 15, key="COLDWAR_SOV_third_way")])
F("smc_the_new_mechanism", "The New Economic Mechanism", s, "smc_the_model", mx="smc_self_management", av=A, e=[pm("smc", {"productivity_growth_modifier": 0.04}), op("HUN", 15, key="COLDWAR_SOV_economic_partners")])
F("smc_open_to_the_world", "Open to the World", s, "smc_self_management|smc_the_new_mechanism", av=A, e=[dm("gp", {"trade_opinion_factor": 0.10}), tension(-1)])
F("smc_federal_reform", "Federal Reform", s, "smc_open_to_the_world", av=A, e=[coh(6)])
F("smc_the_question", "How Far the Market?", s, "smc_federal_reform", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("smc_socialist_market", "A Socialist Market", s, "smc_the_question", mx="smc_the_mixed_economy", av=A, e=[stab(3)])
F("smc_the_mixed_economy", "The Mixed Economy", s, "smc_the_question", mx="smc_socialist_market", av=A, e=[set_law("mixed_economy", "Handelsgesetz → Gemischte Wirtschaft"), stab(-2)])
F("smc_the_commonwealth", "The Commonwealth", s, "smc_socialist_market|smc_the_mixed_economy", av=A, c=7, e=[
    idea("market_commonwealth", "The Market Commonwealth", {"productivity_growth_modifier": 0.05, "stability_factor": 0.02})])

# ------------------------------------------------------------------ 19 Union of Sovereign Republics (Shelest)
s, A = "usr", P(19)
root(19, "usr_a_union_of_sovereign_republics", "A Union of Sovereign Republics", s, "usr", "National Communism",
     {"stability_factor": 0.02, "political_power_factor": -0.05, "nationalist_drift": 0.01}, extra=[coh(10)])
F("usr_the_new_union_treaty", "The New Union Treaty", s, "usr_a_union_of_sovereign_republics", av=A, e=[
    coh(10), txt("Jede Unionsrepublik erhält das Angebot, den neuen Vertrag zu unterzeichnen (mehr Autonomie, kein Austritt erzwungen)")])
F("usr_our_soviet_ukraine", "Our Soviet Ukraine", s, "usr_a_union_of_sovereign_republics", av=A, e=[op("UKR", 20, key="COLDWAR_SOV_republics"), coh(3)])
F("usr_the_model", "Many Paths or a Kiev Axis?", s, "usr_the_new_union_treaty,usr_our_soviet_ukraine", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("usr_many_paths", "Many Paths to Socialism", s, "usr_the_model", mx="usr_the_kiev_axis", av=A, e=[coh(8), pm("usr", {"political_power_factor": -0.03})])
F("usr_the_kiev_axis", "The Kiev Axis", s, "usr_the_model", mx="usr_many_paths", av=A, e=[coh(4), pm("usr", {"political_power_factor": 0.03})])
F("usr_economic_sovereignty", "Economic Sovereignty", s, "usr_many_paths|usr_the_kiev_axis", av=A, e=[dm("gp", {"productivity_growth_modifier": 0.03}), coh(3)])
F("usr_republic_formations", "Republican Formations", s, "usr_economic_sovereignty", av=A, e=[manpower(20000), coh(2)])
F("usr_the_commonwealth_of_soviet_states", "The Commonwealth of Soviet States", s, "usr_republic_formations", av=A, c=7, e=[
    idea("commonwealth_of_soviet_states", "Commonwealth of Soviet States", {"stability_factor": 0.04, "nationalist_drift": -0.02}), coh(10)])

# ------------------------------------------------------------------ 20 The Russian Party (Polyansky)
s, A = "rp", P(20)
root(20, "rp_the_russian_party", "The Russian Party", s, "rp", "The Russian Party",
     {"nationalist_drift": 0.02, "war_support_factor": 0.03, "stability_factor": 0.02}, extra=[coh(-5)])
F("rp_the_molodaya_gvardiya_line", "The Molodaya Gvardiya Line", s, "rp_the_russian_party", av=A, e=[party(20, 5), dm("ps", {"drift_defence_factor": 0.05})])
F("rp_the_russian_village_first", "The Russian Village First", s, "rp_the_russian_party", av=A, e=[dm("gp", {"agricolture_productivity_modifier": 0.05}), fac("farmers", 10)])
F("rp_the_model", "Red or White?", s, "rp_the_molodaya_gvardiya_line,rp_the_russian_village_first", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("rp_national_bolshevism", "National Bolshevism", s, "rp_the_model", mx="rp_orthodox_nationalism", av=A, e=[pm("rp", {"communism_drift": 0.01, "political_power_factor": 0.05}), party(4, 3)])
F("rp_orthodox_nationalism", "Orthodox Nationalism", s, "rp_the_model", mx="rp_national_bolshevism", av=A, e=[
    custom("Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 60)", ["the_clergy"]), pm("rp", {"stability_factor": 0.03})])
F("rp_a_communist_party_for_the_rsfsr", "A Party for the RSFSR", s, "rp_national_bolshevism|rp_orthodox_nationalism", av=A, e=[coh(-5), dm("ps", {"political_power_factor": 0.05})])
F("rp_the_slavic_core", "The Slavic Core", s, "rp_a_communist_party_for_the_rsfsr", av=A, e=[
    offer("slavic_core", ["UKR", "BLR"], "Engere Union der Ostslawen. Bei Annahme: Meinung +20, Autonomie bleibt, Zusammenhalt +5")])
F("rp_the_great_power_army", "The Great Power Army", s, "rp_a_communist_party_for_the_rsfsr", av=A, e=[dm("af", {"army_morale_factor": 0.05}), fac("the_military", 10)])
F("rp_the_question", "Empire or Nation?", s, "rp_the_slavic_core,rp_the_great_power_army", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("rp_the_empire", "The Empire", s, "rp_the_question", mx="rp_the_nation", av=A, e=[coh(5), ws(5), dm("ps", {"police_cost_multiplier_modifier": 0.10})])
F("rp_the_nation", "The Nation", s, "rp_the_question", mx="rp_the_empire", av=A, e=[coh(-10), stab(5)])
F("rp_great_russia", "Great Russia", s, "rp_the_empire|rp_the_nation", av=A, c=7, e=[
    idea("great_russia", "Great Russia", {"war_support_factor": 0.05, "stability_factor": 0.03, "nationalist_drift": 0.01})])

# ------------------------------------------------------------------ 21 Committee of National Rebirth (player only)
s, A = "cnr", P(21)
root(21, "cnr_the_national_rebirth", "The National Rebirth", s, "cnr", "National Rebirth",
     {"war_support_factor": 0.10, "stability_factor": -0.05, "drift_defence_factor": 0.15, "trade_opinion_factor": -0.20}, ai="0")
F("cnr_the_emergency_committee", "The Emergency Committee", s, "cnr_the_national_rebirth", av=A, ai="0", e=[pp(75), fac("communist_cadres", -25)])
F("cnr_militarise_the_nation", "Militarise the Nation", s, "cnr_the_national_rebirth", av=A, ai="0", e=[
    law("increase_military_spending", "Verteidigungshaushalt +1 Stufe"), manpower(50000)])
F("cnr_the_path", "Isolation or Expansion?", s, "cnr_the_emergency_committee,cnr_militarise_the_nation", av=A, ai="0", c=3, e=[txt("Gegenseitig exklusiv")])
F("cnr_fortress_russia", "Fortress Russia", s, "cnr_the_path", mx="cnr_the_revanche", av=A, ai="0", e=[
    set_law("md_closed_economy", "Handelsgesetz → Geschlossene Wirtschaft"), dm("af", {"army_core_defence_factor": 0.05})])
F("cnr_the_revanche", "The Revanche", s, "cnr_the_path", mx="cnr_fortress_russia", av=A, ai="0", e=[tension(5), dm("af", {"army_attack_factor": 0.03})])
F("cnr_the_rebirth_state", "The Rebirth State", s, "cnr_fortress_russia|cnr_the_revanche", av=A, ai="0", c=7, e=[
    idea("rebirth_state", "The Rebirth State", {"war_support_factor": 0.05, "stability_factor": 0.02, "research_speed_factor": -0.03})])

# ------------------------------------------------------------------ 22 Council of Marshals (Grechko)
s, A = "com", P(22)
root(22, "com_the_marshals_govern", "The Marshals Govern", s, "com", "The Council of Marshals",
     {"army_org_factor": 0.05, "war_support_factor": 0.05, "stability_factor": -0.03, "political_power_factor": -0.05})
F("com_the_general_staff_governs", "The General Staff Governs", s, "com_the_marshals_govern", av=A, e=[fac("the_military", 15), cp(50)])
F("com_order_and_discipline", "Order and Discipline", s, "com_the_marshals_govern", av=A, e=[stab(4), corr(-1)])
F("com_the_model", "Ogarkov or the Old Marshals?", s, "com_the_general_staff_governs,com_order_and_discipline", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("com_the_modernisers", "The Modernisers", s, "com_the_model", mx="com_the_old_marshals", av=A, e=[
    pm("com", {"research_speed_factor": 0.03, "production_factory_efficiency_gain_factor": 0.03}), tech("CAT_command_and_control_equipment", 1, 75)])
F("com_the_old_marshals", "The Old Marshals", s, "com_the_model", mx="com_the_modernisers", av=A, e=[
    pm("com", {"conscription_factor": 0.05, "army_defence_factor": 0.03}), manpower(50000)])
F("com_the_military_economy", "The Military Economy", s, "com_the_modernisers|com_the_old_marshals", av=A, e=[build("mil2", 1.2), dm("gp", {"consumer_goods_factor": 0.03})])
F("com_the_defence_council", "The Defence Council", s, "com_the_military_economy", av=A, e=[pp(75), dm("af", {"planning_speed": 0.05})])
F("com_strategic_deterrence", "Strategic Deterrence", s, "com_the_military_economy", av=A, e=[tech("CAT_intercontinental_ballistic_missiles", 1, 50), tension(2)])
F("com_the_question", "How Long?", s, "com_the_defence_council,com_strategic_deterrence", av=A, c=3, e=[txt("Gegenseitig exklusiv")])
F("com_return_to_the_barracks", "Return to the Barracks", s, "com_the_question", mx="com_the_permanent_stavka", av=A, e=[rp(4), stab(5), fac("the_military", -10)],
  n="Übergabe zurück an die KPdSU.")
F("com_the_permanent_stavka", "The Permanent Stavka", s, "com_the_question", mx="com_return_to_the_barracks", av=A, e=[pm("com", {"political_power_factor": 0.05, "stability_factor": 0.03})])
F("com_the_garrison_state", "The Garrison State", s, "com_the_permanent_stavka", av=A, c=7, e=[
    idea("garrison_state", "The Garrison State", {"army_attack_factor": 0.02, "army_defence_factor": 0.03, "consumer_goods_factor": 0.02})])

# ------------------------------------------------------------------ 23 House of Romanov
s, A = "rom", P(23)
root(23, "rom_the_return_of_the_tsar", "The Return of the Romanovs", s, "rom", "The Restored Crown",
     {"stability_factor": 0.03, "nationalist_drift": 0.02, "political_power_factor": 0.03},
     extra=[leader("Vladimir Kirillovich", 23, "head_of_the_house", "Head of the House of Romanov")], ai="0")
F("rom_the_coronation", "The Coronation", s, "rom_the_return_of_the_tsar", av=A, ai="0", e=[stab(5), pp(50)])
F("rom_the_church_and_the_crown", "The Church and the Crown", s, "rom_the_return_of_the_tsar", av=A, ai="0", e=[
    custom("Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 75)", ["the_clergy"]), stab(3)])
F("rom_the_form", "Duma or Autocrat?", s, "rom_the_coronation,rom_the_church_and_the_crown", av=A, ai="0", c=3, e=[txt("Gegenseitig exklusiv")])
F("rom_constitutional_monarchy", "Constitutional Monarchy", s, "rom_the_form", mx="rom_the_autocrat", av=A, ai="0", e=[elections(True), pm("rom", {"democratic_drift": 0.01, "stability_factor": 0.02})])
F("rom_the_autocrat", "The Autocrat", s, "rom_the_form", mx="rom_constitutional_monarchy", av=A, ai="0", e=[pm("rom", {"political_power_factor": 0.05, "drift_defence_factor": 0.10})])
F("rom_the_emigres_return", "The Émigrés Return", s, "rom_constitutional_monarchy|rom_the_autocrat", av=A, ai="0", e=[dm("ps", {"research_speed_factor": 0.02}), dm("gp", {"trade_opinion_factor": 0.10})])
F("rom_the_crown_and_the_republics", "The Crown and the Republics", s, "rom_the_emigres_return", av=A, ai="0", e=[coh(-5), stab(2)])
F("rom_the_royal_houses", "The Royal Houses of Europe", s, "rom_the_emigres_return", av=A, ai="0", e=[
    offer("royal_houses", ["ENG", "SPR"], "Anerkennung der restaurierten Krone. Bei Annahme: Meinung +25")])
F("rom_the_restored_empire", "The Restored Empire", s, "rom_the_crown_and_the_republics,rom_the_royal_houses", av=A, ai="0", c=7, e=[
    idea("restored_empire", "The Restored Empire", {"stability_factor": 0.05, "nationalist_drift": 0.01, "war_support_factor": 0.03})])
