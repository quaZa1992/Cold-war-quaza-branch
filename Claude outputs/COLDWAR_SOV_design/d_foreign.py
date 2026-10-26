# IMPERIA CW — Cold War: Cold War SOV design — d foreign.
from sov_dsl import *

ROOT_AV = "`COLDWAR_SOV_the_collective_leadership` erledigt"
WP = ["DDR", "POL", "CZE", "HUN", "ROM", "BUL"]

# ============================================================== DETENTE & THE WEST
F("peaceful_coexistence", "Peaceful Coexistence", "det", c=3, h=1, av=ROOT_AV, e=[pp(15), tension(-1)])
F("the_moscow_treaty", "The Moscow Treaty", "det", "peaceful_coexistence", c=5, h=1, e=[
    offer("moscow_treaty", "GER", "Gewaltverzicht und Anerkennung der Nachkriegsgrenzen. Bei Annahme: Spannung −2, Meinung +20 beidseitig, "
                                  "verbessertes Handelsabkommen; „The Shadow of Prague“ verliert die Handelsstrafe"),
], n="12.08.1970, Brandts Ostpolitik. Nur als Angebot.")
F("the_peace_programme", "The Peace Programme", "det", "peaceful_coexistence", av="`COLDWAR_SOV_the_24th_party_congress` erledigt", c=5, h=1, e=[
    tension(-1), dm("cw", {"trade_opinion_factor": 0.05}), op("USA", 5, key="COLDWAR_SOV_detente")])
F("the_berlin_agreement", "The Quadripartite Agreement", "det", "the_moscow_treaty", c=5, h=1, e=[
    offer("berlin_agreement", ["USA", "ENG", "FRA"], "Viermächteabkommen über Berlin (1971). Bei Annahme aller: Spannung −2, DDR/BRD-Transit gesichert"),
])
F("salt_negotiations", "SALT Negotiations", "det", "the_peace_programme", c=3, h=1, e=[txt("Rüstungskontrolle oder Überlegenheit – gegenseitig exklusiv")])
F("salt_i_and_the_abm_treaty", "SALT I and the ABM Treaty", "det", "salt_negotiations", mx="superiority_not_parity", c=5, h=1, e=[
    offer("salt_i", "USA", "SALT I und ABM-Vertrag. Bei Annahme: beide erhalten „Arms Limitation“ (Kosten Verteidigungshaushalt −10 %, "
                          "Kriegsunterstützung −2 %), Spannung −3; „The Burden of Parity“ wird abgeschwächt"),
    fac("the_military", -5)], n="Moskau, Mai 1972.")
F("superiority_not_parity", "Superiority, Not Parity", "det", "salt_negotiations", mx="salt_i_and_the_abm_treaty", c=5, e=[
    tension(3), fac("the_military", 10), fac("defense_industry", 10),
    idea("arms_race", "The Arms Race", {"production_speed_arms_factory_factor": 0.10, "consumer_goods_factor": 0.03, "war_support_factor": 0.03}),
    bop(0.10)])
F("the_moscow_summit", "The Moscow Summit", "det", "salt_i_and_the_abm_treaty", c=5, h=1, e=[
    offer("moscow_summit", "USA", "Gipfel in Moskau (Mai 1972). Bei Annahme: Spannung −2, „Basic Principles of Relations“, Meinung +15"),
    stab(2)])
F("trade_and_credits", "Western Credits and Technology", "det", "the_peace_programme", c=5, h=1, e=[
    debt(1.0), tech(["CAT_industry", "CAT_production_lines"], 1, 50), dm("cw", {"trade_opinion_factor": 0.05}), bop(-0.05)])
F("the_paris_axis", "The Paris Axis", "det", "the_peace_programme", c=5, h=1, e=[
    offer("paris_axis", "FRA", "Französisch-sowjetische Zusammenarbeit (Pompidou 1970/71). Bei Annahme: Forschungsbonus Elektronik für beide, Meinung +20")])
F("vladivostok_accords", "The Vladivostok Accords", "det", "the_moscow_summit|superiority_not_parity", av="Datum ≥ 01.11.1974", c=5, h=1, e=[
    offer("vladivostok", "USA", "Rahmen für SALT II. Bei Annahme: Spannung −1, Meinung +10")])
F("the_helsinki_conference", "The Helsinki Conference", "det", "the_berlin_agreement,vladivostok_accords|the_paris_axis",
  av="Datum ≥ 01.07.1975", c=7, h=1, e=[
      offer("helsinki", ["USA", "GER", "FRA", "ENG"], "Schlussakte der KSZE. Bei Annahme: Unverletzlichkeit der Grenzen; Spannung −3"),
      rmidea("shadow_of_prague", "The Shadow of Prague"),
      idea("basket_three", "Basket Three", {"trade_opinion_factor": 0.10, "democratic_drift": 0.01}),
      ev("helsinki_groups", "Die Moskauer Helsinki-Gruppe (1976) beruft sich auf Korb III")],
  n="Die UdSSR bekommt ihre Grenzen anerkannt – und die Dissidenten ein Dokument.")
F("salt_ii", "SALT II", "det", "the_helsinki_conference", av="Datum ≥ 01.06.1979", c=5, h=1, e=[
    offer("salt_ii", "USA", "SALT II in Wien. Bei Annahme: Spannung −2, Kosten Verteidigungshaushalt −5 % für beide")])
F("the_end_of_detente", "The End of Detente?", "det", "salt_ii|superiority_not_parity", av="Cold-War-Spannung ≥ 60 ODER Datum ≥ 01.01.1980", c=3, e=[
    txt("Gegenseitig exklusiv: retten oder abschreiben")])
F("save_detente", "Save Detente", "det", "the_end_of_detente", mx="the_second_cold_war", c=5, e=[
    tension(-2), pp(-50), op("USA", 10, key="COLDWAR_SOV_detente"), bop(-0.05)])
F("the_second_cold_war", "The Second Cold War", "det", "the_end_of_detente", mx="save_detente", c=5, e=[
    tension(3), ws(5), dm("af", {"equipment_cost_multiplier_modifier": -0.02}), fac("the_military", 5)])

# ============================================================== THE CHINESE QUESTION
F("the_chinese_question", "The Chinese Question", "chi", c=3, h=1, av=ROOT_AV, e=[
    pp(15), txt("Damanski (März 1969) und Tielieketi (August 1969) liegen kein Jahr zurück")])
F("the_beijing_border_talks", "The Beijing Border Talks", "chi", "the_chinese_question", c=5, h=1, e=[
    offer("border_talks", "CHI", "Grenzgespräche (seit Oktober 1969). Bei Annahme: Spannung −1, „The Ussuri Frontier“ verliert die Stabilitätsstrafe"),
])
F("three_roads_to_beijing", "Three Roads to Beijing", "chi", "the_beijing_border_talks", c=3, h=1, e=[txt("Eindämmen, zuschlagen oder versöhnen – gegenseitig exklusiv")])
F("contain_china", "Contain China", "chi", "three_roads_to_beijing", mx="the_surgical_strike_option,reconcile_with_beijing", c=5, h=1, e=[
    dm("af", {"army_core_defence_factor": 0.03}), fac("the_military", 5)])
F("the_trans_baikal_buildup", "The Trans-Baikal Buildup", "chi", "contain_china", c=7, h=1, e=[
    build("air"), build("mil", 0.8), manpower(20000),
    idea("eastern_fortress", "The Eastern Fortress", {"war_support_factor": 0.05, "army_core_defence_factor": 0.05,
                                                      "army_personnel_cost_multiplier_modifier": 0.10}, swap="The Ussuri Frontier")],
  n="1969–1972 wächst die Fernostgruppierung von 15 auf über 40 Divisionen.")
F("the_amur_fortified_districts", "The Amur Fortified Districts", "chi", "the_trans_baikal_buildup", c=5, h=1, e=[
    dm("af", {"army_core_defence_factor": 0.05}), custom("Bunker in zwei Grenzstaaten `add_building_construction` (bunker)", ["add_building_construction"])])
F("the_mongolian_shield", "The Mongolian Shield", "chi", "the_trans_baikal_buildup", c=5, h=1, e=[
    offer("mongolian_garrison", "MON", "Stationierung der 39. Armee in der Mongolei. Bei Annahme: MON erhält Hilfe 0,2 % BIP/Jahr und Verteidigung +5 %")])
F("asian_collective_security", "Asian Collective Security", "chi", "contain_china", c=5, h=1, e=[
    infl(["RAJ", "VIE", "MON", "AFG"], 3), op("RAJ", 10, key="COLDWAR_SOV_asian_security")], n="Breschnews Vorschlag von 1969 – gegen China gerichtet.")
F("treaty_with_india", "Treaty with India", "chi", "asian_collective_security", c=5, h=1, e=[
    offer("india_treaty", "RAJ", "Vertrag über Frieden, Freundschaft und Zusammenarbeit (August 1971). Bei Annahme: Rüstungshilfe, Meinung +25, Handelsabkommen")])
F("vietnam_against_china", "Vietnam against China", "chi", "asian_collective_security", av="Datum ≥ 01.01.1978", c=5, h=1, e=[
    offer("vietnam_treaty", "VIE", "Freundschaftsvertrag (November 1978). Bei Annahme: Cam-Ranh-Rechte und gemeinsame Front gegen China")])
F("the_surgical_strike_option", "The Surgical Strike Option", "chi", "three_roads_to_beijing", mx="contain_china,reconcile_with_beijing", c=5, ai="0", e=[
    tension(5), fac("the_military", 5), fac("communist_cadres", -5),
    txt("Alt-Hist, nur Spieler. Die im Herbst 1969 diskutierte Option eines Schlags gegen Lop Nor")])
F("plan_lop_nur", "Plan Lop Nur", "chi", "the_surgical_strike_option", c=7, ai="0", e=[
    dm("af", {"planning_speed": 0.10}), tech("CAT_ballistic_missiles", 1, 50),
    custom("Kriegsziel gegen CHI (`create_wargoal`, Typ `topple_government`); Erklärung bleibt Entscheidung des Spielers", ["create_wargoal"])])
F("strike_at_dawn", "Strike at Dawn", "chi", "plan_lop_nur", av="Im Krieg mit CHI", c=3, ai="0", e=[
    idea("strike_at_dawn", "Strike at Dawn", {"army_attack_factor": 0.05, "breakthrough_factor": 0.05}, days=180), tension(10),
    ev("lop_nur_world", "Weltreaktion: Washington, Delhi und Tokio verurteilen den Schlag")])
F("reconcile_with_beijing", "Reconcile with Beijing", "chi", "three_roads_to_beijing", mx="contain_china,the_surgical_strike_option", c=5, ai="0", e=[
    bop(-0.05), offer("sino_soviet_truce", "CHI", "Ideologischer Waffenstillstand. Bei Annahme: „The Ussuri Frontier“ entfällt, Spannung −2, Meinung +30; "
                                                "Peking kann ins sowjetische Lager zurück (Cold-War-Blockwechsel bleibt Pekings Entscheidung)")],
  n="Alt-Hist: Die Kosygin-Zhou-Begegnung vom September 1969 wird zum Wendepunkt.")
F("settle_damansky", "Settle Damansky", "chi", "reconcile_with_beijing|the_beijing_border_talks", c=5, e=[
    offer("damansky_settlement", "CHI", "Damanski/Zhenbao an China, Flussgrenze in der Fahrrinne. Bei Annahme: „The Ussuri Frontier“ wird entfernt, Spannung −1")],
  n="Historisch erst 1991 geregelt.")
F("the_eastern_front_secured", "The Eastern Front Secured", "chi", "the_amur_fortified_districts|settle_damansky|strike_at_dawn", c=7, e=[
    stab(3), dm("af", {"army_personnel_cost_multiplier_modifier": -0.05}), txt("Mit „BAM Open to Traffic“: zusätzlich Versorgung −2 %")])

# ============================================================== WARSAW PACT & COMECON
F("the_socialist_commonwealth", "The Socialist Commonwealth", "bloc", c=3, h=1, av=ROOT_AV, e=[
    dm("cw", {"opinion_gain_monthly_same_ideology_factor": 0.05})])
F("the_doctrine_question", "Limited Sovereignty?", "bloc", "the_socialist_commonwealth", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("the_brezhnev_doctrine", "The Brezhnev Doctrine", "bloc", "the_doctrine_question", mx="let_them_go_their_way", c=5, h=1, e=[
    dm("cw", {"foreign_influence_modifier": 0.05}), dm("ps", {"mdcw_cw_ideological_defence": 0.05}), tension(1),
    idea("brezhnev_doctrine", "The Brezhnev Doctrine", {"drift_defence_factor": 0.05, "trade_opinion_factor": -0.05})],
  n="„Die Souveränität jedes sozialistischen Landes ist begrenzt“ – Prag 1968 als Regel.")
F("let_them_go_their_way", "Let Them Go Their Way", "bloc", "the_doctrine_question", mx="the_brezhnev_doctrine", c=5, ai="0", e=[
    bop(-0.10), tension(-2), rmidea("shadow_of_prague", "The Shadow of Prague"), coh(-3),
    dm("cw", {"tax_gain_multiplier_modifier": 0.03}), op("ROM", 15, key="COLDWAR_SOV_bloc_relations")],
  n="Alt-Hist: eine „Sinatra-Doktrin“ zwanzig Jahre früher.")
F("the_comprehensive_programme", "The Comprehensive Programme", "bloc", "the_socialist_commonwealth", c=5, h=1, e=[
    dm("cw", {"research_sharing_per_country_bonus_factor": 0.05, "opinion_gain_monthly_same_ideology_factor": 0.05}),
    txt("Cold War: Decision „Comecon Integration Programme“ kostet für uns 25 PP weniger (`COLDWAR_SOV_comprehensive_programme` Flag)"),
    flag("comprehensive_programme")], n="RGW-Gipfel Bukarest, Juli 1971.")
F("the_oil_price_question", "Fraternal Oil", "bloc", "the_comprehensive_programme", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("subsidised_oil", "Subsidised Oil", "bloc", "the_oil_price_question", mx="world_market_prices", c=5, h=1, e=[
    dm("cw", {"oil_export_multiplier_modifier": -0.05, "opinion_gain_monthly_same_ideology_factor": 0.10}),
    op("POL", 10, key="COLDWAR_SOV_bloc_relations"), op("DDR", 10, key="COLDWAR_SOV_bloc_relations")])
F("world_market_prices", "World Market Prices", "bloc", "the_oil_price_question", mx="subsidised_oil", c=5, e=[
    dm("cw", {"oil_export_multiplier_modifier": 0.05}), gdp_gain(0.3),
    custom("Meinung −10 bei allen RGW-Partnern (DDR, POL, CZE, HUN, ROM, BUL) `add_opinion_modifier`", ["add_opinion_modifier"])],
  n="Der „Bukarester Mechanismus“ von 1975 mit gleitenden Durchschnittspreisen – konsequent zu Ende gedacht.")
F("the_soyuz_pipeline", "The Soyuz Pipeline", "bloc", "subsidised_oil|world_market_prices", av="Datum ≥ 01.01.1975", c=7, h=1, e=[
    offer("soyuz_pipeline", WP, "Gemeinsamer Bau der Orenburg-Gasleitung. Bei Annahme: Partner zahlt 0,2 % BIP und erhält Energie +5 %; UdSSR erhält Bau +3 %")])
F("shield_and_brotherhood", "Shield and Brotherhood", "bloc", "the_brezhnev_doctrine|let_them_go_their_way", c=5, h=1, e=[
    offer("joint_exercises", WP, "Gemeinsame Manöver „Schild“/„Waffenbrüderschaft“. Bei Annahme: beide +25 Heereserfahrung"),
    xp("army", 25)])
F("kulikovs_unified_command", "Kulikov's Unified Command", "bloc", "shield_and_brotherhood", av="Datum ≥ 01.01.1977", c=5, h=1, e=[
    dm("cw", {"research_sharing_per_country_bonus_factor": 0.05}), dm("af", {"planning_speed": 0.05})])
F("the_polish_question", "The Polish Question", "bloc", "the_socialist_commonwealth", c=3, h=1, e=[
    txt("Danzig, Dezember 1970 – Gomułka stürzt, Gierek übernimmt. Gegenseitig exklusiv")])
F("credits_for_gierek", "Credits for Gierek", "bloc", "the_polish_question", mx="discipline_warsaw", c=5, h=1, e=[
    offer("credits_for_poland", "POL", "Rohstoffkredite und Getreide. Bei Annahme: POL erhält 0,4 % unseres BIP, Stabilität +5 %; wir zahlen"),
    gdp(0.4)])
F("discipline_warsaw", "Discipline Warsaw", "bloc", "the_polish_question", mx="credits_for_gierek", c=5, e=[
    op("POL", -15, key="COLDWAR_SOV_bloc_relations"), dm("ps", {"mdcw_cw_ideological_defence": 0.05}),
    ev("warsaw_discipline", "Die polnische Führung wird nach Moskau bestellt – Antwort liegt bei Polen")])
F("romanias_maverick_course", "Romania's Maverick Course", "bloc", "the_socialist_commonwealth", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("tolerate_bucharest", "Tolerate Bucharest", "bloc", "romanias_maverick_course", mx="isolate_bucharest", c=3, h=1, e=[
    op("ROM", 5, key="COLDWAR_SOV_bloc_relations"), pp(25)])
F("isolate_bucharest", "Isolate Bucharest", "bloc", "romanias_maverick_course", mx="tolerate_bucharest", c=5, e=[
    op("ROM", -20, key="COLDWAR_SOV_bloc_relations"), dm("cw", {"foreign_influence_modifier": 0.03}), tension(1)])
F("interkosmos", "Interkosmos", "bloc", "the_comprehensive_programme", av="Datum ≥ 01.01.1977", c=5, h=1, e=[
    offer("interkosmos", WP + ["CUB", "MON", "VIE"], "Ein Kosmonaut des Partners fliegt mit Sojus. Bei Annahme: Partner +5 % Stabilität (1 Jahr), Meinung +20"),
    space()])
F("the_commonwealth_of_socialist_nations", "The Commonwealth of Socialist Nations", "bloc",
  "kulikovs_unified_command,the_soyuz_pipeline|interkosmos", c=7, e=[
      idea("socialist_commonwealth", "The Socialist Commonwealth", {"opinion_gain_monthly_same_ideology_factor": 0.10,
                                                                   "research_sharing_per_country_bonus_factor": 0.05}),
      dm("cw", {"mdcw_cw_assistance_capacity": 1})])

# ============================================================== THIRD WORLD & INTERNATIONALISM
F("proletarian_internationalism", "Proletarian Internationalism", "tw", c=3, h=1, av=ROOT_AV, e=[
    dm("cw", {"mdcw_cw_support_effectiveness": 0.05}), pp(10)])
F("operation_kavkaz", "Operation Kavkaz", "tw", "proletarian_internationalism", av="Datum < 01.01.1972; EGY existiert", c=5, h=1, e=[
    offer("operation_kavkaz", "EGY", "Eine Flugabwehrdivision und MiG-21-Staffeln am Suezkanal. Bei Annahme: EGY Luftverteidigung, wir +25 Lufterfahrung, Spannung +1"),
    txt("Wird automatisch erfüllt, wenn Ägypten uns vorher um Operation Kavkaz gebeten und wir angenommen haben (EGY-Baum)")],
  n="Januar–März 1970: 10.000 sowjetische Soldaten in Ägypten.")
F("the_treaty_with_egypt", "The Treaty with Egypt", "tw", "operation_kavkaz", c=5, h=1, e=[
    offer("egypt_treaty", "EGY", "Freundschaftsvertrag (Mai 1971). Bei Annahme: Meinung +25, Einfluss +5 %")])
F("lifeline_to_hanoi", "Lifeline to Hanoi", "tw", "proletarian_internationalism", c=5, h=1, e=[
    offer("arms_for_hanoi", "VIE", "Luftabwehrraketen, MiGs und Reis. Bei Annahme: VIE erhält Ausrüstung und Verteidigung +5 %; wir zahlen 0,4 % BIP"),
    tension(1)])
F("the_island_of_freedom", "The Island of Freedom", "tw", "proletarian_internationalism", c=5, h=1, e=[
    offer("sugar_for_oil", "CUB", "Öl gegen Zucker zu Vorzugspreisen. Bei Annahme: CUB Stabilität +5 %, Wirtschaft +; wir Sozialistische Gemeinschaft: Steuern −1 %"),
    dm("cw", {"tax_gain_multiplier_modifier": -0.01})])
F("syria_and_iraq", "Syria and Iraq", "tw", "the_treaty_with_egypt", c=5, h=1, e=[
    offer("iraq_treaty", "IRQ", "Freundschaftsvertrag (April 1972). Bei Annahme: Meinung +20, Ölkooperation"),
    offer("syria_arms", "SYR", "Rüstungspaket und Berater. Bei Annahme: SYR +5 % Verteidigung, Meinung +20")])
F("patrice_lumumba_university", "Patrice Lumumba University", "tw", "proletarian_internationalism", c=5, h=1, e=[
    dm("cw", {"mdcw_cw_support_effectiveness": 0.10}), dm("gp", {"education_cost_multiplier_modifier": 0.02})])
F("military_advisers", "Military Advisers", "tw", "patrice_lumumba_university", c=5, h=1, e=[
    dm("cw", {"mdcw_cw_military_programme_cost": -0.15, "send_volunteer_size": 1})])
F("the_question_of_aid", "Aid or Arms?", "tw", "military_advisers", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("economic_aid_programmes", "Economic Aid Programmes", "tw", "the_question_of_aid", mx="arms_on_credit", c=5, e=[
    dm("cw", {"mdcw_cw_assistance_capacity": 2, "tax_gain_multiplier_modifier": -0.02}), dm("cw", {"foreign_influence_modifier": 0.05})])
F("arms_on_credit", "Arms on Credit", "tw", "the_question_of_aid", mx="economic_aid_programmes", c=5, h=1, e=[
    dm("af", {"international_market_income_modifier": 0.10}), dm("cw", {"foreign_influence_modifier": 0.03}), fac("defense_industry", 5)])
F("the_cuban_bridge", "The Cuban Bridge to Angola", "tw", "the_island_of_freedom,military_advisers", av="Datum ≥ 01.06.1975", c=5, h=1, e=[
    offer("angola_support", "AGL", "Unterstützung der MPLA mit Waffen und kubanischen Truppen. Bei Annahme: AGL +10 % Angriff (2 Jahre)"),
    tension(2)])
F("the_horn_of_africa", "The Horn of Africa", "tw", "the_cuban_bridge", av="Datum ≥ 01.01.1977", c=3, h=1, e=[txt("Ogaden – gegenseitig exklusiv")])
F("back_ethiopia", "Back the Derg", "tw", "the_horn_of_africa", mx="back_somalia", c=5, h=1, e=[
    offer("ethiopia_airlift", "ETH", "Luftbrücke und kubanische Brigaden (1977/78). Bei Annahme: ETH Angriff +10 %"),
    op("SOM", -30, key="COLDWAR_SOV_horn_of_africa")])
F("back_somalia", "Back Siad Barre", "tw", "the_horn_of_africa", mx="back_ethiopia", c=5, e=[
    offer("somalia_support", "SOM", "Waffen und Berater. Bei Annahme: SOM Angriff +10 %, Berbera bleibt sowjetisch"),
    op("ETH", -30, key="COLDWAR_SOV_horn_of_africa")])
F("the_afghan_question", "The Afghan Question", "tw", "syria_and_iraq|military_advisers", av="Datum ≥ 01.04.1978", c=3, h=1, e=[
    txt("Saur-Revolution und Herat-Aufstand – gegenseitig exklusiv")])
F("the_limited_contingent", "The Limited Contingent", "tw", "the_afghan_question", mx="no_soviet_soldier", c=5, h=1, e=[
    offer("limited_contingent", "AFG", "Die afghanische Regierung bittet um Truppen (Dezember 1979). Bei Annahme: Expeditionsstreitkräfte, "
                                       "wir erhalten „The Afghan Burden“ (Stabilität −3 %, Kriegsunterstützung −5 %, 0,3 % BIP/Monat) solange der Krieg läuft"),
    tension(4)], n="Kein automatischer Einmarsch: Afghanistan muss annehmen (Spieler oder KI).")
F("no_soviet_soldier", "Not a Single Soviet Soldier", "tw", "the_afghan_question", mx="the_limited_contingent", c=3, e=[
    stab(2), op("AFG", -10, key="COLDWAR_SOV_afghan_question"), bop(-0.05)],
  n="Kossygin im März 1979: „Wir können das afghanische Volk nicht ersetzen.“")
F("vanguard_of_world_revolution", "Vanguard of World Revolution", "tw", "back_ethiopia|back_somalia|economic_aid_programmes|arms_on_credit", c=7, e=[
    idea("vanguard_of_revolution", "Vanguard of World Revolution", {"foreign_influence_modifier": 0.10, "mdcw_cw_support_effectiveness": 0.10,
                                                                     "tax_gain_multiplier_modifier": -0.02})])
