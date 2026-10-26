# IMPERIA CW — Cold War: Cold War SOV design — d mil state.
from sov_dsl import *

ROOT_AV = "`COLDWAR_SOV_the_collective_leadership` erledigt"

# ============================================================== SOVIET ARMY
F("the_soviet_army", "The Soviet Army", "army", c=3, h=1, av=ROOT_AV, e=[xp("army", 25), cp(20), dm("af", {"planning_speed": 0.05})])
F("grechkos_ministry", "Grechko's Ministry", "army", "the_soviet_army", c=5, h=1, e=[
    fac("the_military", 5), dm("af", {"army_org_factor": 0.02}), tech("CAT_infantry_weapons", 1, 50)],
  n="Marschall Andrei Gretschko, Verteidigungsminister 1967–1976.")
F("the_doctrine_debate", "The Doctrine Debate", "army", "grechkos_ministry", c=3, h=1, e=[
    txt("Konventionell tief oder nuklear? Gegenseitig exklusiv")])
F("deep_operations_revived", "Deep Operations Revived", "army", "the_doctrine_debate", mx="the_nuclear_battlefield", c=5, h=1, e=[
    mastery("land", 50), dm("af", {"breakthrough_factor": 0.03, "planning_speed": 0.05})],
  n="Tuchatschewskis Tiefe Operation, ab Mitte der 1970er wieder Leitbild.")
F("the_nuclear_battlefield", "The Nuclear Battlefield", "army", "the_doctrine_debate", mx="deep_operations_revived", c=5, e=[
    dm("af", {"army_defence_factor": 0.02, "army_org_factor": 0.03}), tech("CAT_ballistic_missiles", 1, 50)],
  n="Sokolowskis „Militärstrategie“ (1962): jeder Krieg in Europa wird nuklear.")
F("operational_manoeuvre_groups", "Operational Manoeuvre Groups", "army", "deep_operations_revived", av="Datum ≥ 01.01.1977", c=7, e=[
    dm("af", {"breakthrough_factor": 0.03, "army_speed_factor": 0.03}), mastery("land", 50)], n="Ogarkows OMG-Konzept.")
F("theatres_of_military_operations", "Theatres of Military Operations", "army", "deep_operations_revived|the_nuclear_battlefield",
  av="Datum ≥ 01.01.1979", c=5, h=1, e=[dm("af", {"max_planning_factor": 0.05}), cp(30)],
  n="1979: Oberkommandos für die TVD West, Südwest, Süd und Fernost.")
F("the_tank_question", "The Tank Question", "army", "the_soviet_army", c=3, h=1, e=[txt("Ein Hauptpanzer oder zwei? Gegenseitig exklusiv")])
F("t64_morozovs_masterpiece", "T-64: Morozov's Masterpiece", "army", "the_tank_question", mx="t72_the_mass_tank", c=5, e=[
    tech("CAT_main_battle_tanks", 2, 50), dm("af", {"equipment_cost_multiplier_modifier": 0.03}), fac("defense_industry", 5)],
  n="Charkiw: modernster Panzer der Welt, teuer und kompliziert.")
F("t72_the_mass_tank", "T-72: The Mass Tank", "army", "the_tank_question", mx="t64_morozovs_masterpiece", c=5, h=1, e=[
    tech("CAT_main_battle_tanks", 1, 50), dm("af", {"equipment_cost_multiplier_modifier": -0.04}), build("mil", 1.0)],
  n="Uralwagonsawod: der Mobilisierungspanzer, auch für den Export.")
F("t80_gas_turbine", "T-80: The Gas Turbine Tank", "army", "t64_morozovs_masterpiece|t72_the_mass_tank", av="Datum ≥ 01.01.1976", c=5, e=[
    tech(["CAT_main_battle_tanks", "CAT_tank_engines"], 1, 50)])
F("bmp_infantry_in_armour", "BMP: Infantry in Armour", "army", "the_tank_question", c=5, h=1, e=[
    tech("CAT_infantry_fighting_vehicles", 1, 75), dm("af", {"mechanized_attack_factor": 0.02})])
F("ak74", "AK-74", "army", "grechkos_ministry", c=5, h=1, e=[tech("CAT_small_arms", 1, 50)], n="Eingeführt 1974.")
F("the_praporshchiki", "The Praporshchiki", "army", "grechkos_ministry", c=5, h=1, e=[
    dm("af", {"army_org_factor": 0.03}), dm("af", {"army_personnel_cost_multiplier_modifier": 0.02})],
  n="1972: Fähnriche als Berufskader zwischen Wehrpflichtigen und Offizieren.")
F("against_dedovshchina", "Against Dedovshchina", "army", "the_praporshchiki", c=5, e=[
    dm("af", {"army_morale_factor": 0.04}), fac("the_military", -5)], n="Die Schikane der „Großväter“ – Reform kostet die Altgedienten.")
F("margelovs_airborne", "Margelov's Airborne", "army", "the_soviet_army", c=5, h=1, e=[
    dm("af", {"paradrop_organization_factor": 0.10, "special_forces_cap": 0.05}), tech("CAT_special_forces_equipment", 1, 50)],
  n="„Onkel Wasjas Truppen“ – die WDW werden zur strategischen Reserve.")
F("spetsnaz_of_the_gru", "Spetsnaz of the GRU", "army", "margelovs_airborne", c=5, e=[
    dm("af", {"special_forces_attack_factor": 0.05, "special_forces_cap": 0.05})])
F("mi24_the_flying_tank", "Mi-24: The Flying Tank", "army", "margelovs_airborne", c=5, h=1, e=[
    tech("CAT_attack_helicopters", 1, 75)])
F("rocket_artillery", "Grad and Uragan", "army", "the_tank_question", c=5, e=[
    tech("CAT_artillery", 1, 50), dm("af", {"rocket_attack_factor": 0.05})])
F("universal_military_duty", "Universal Military Duty", "army", "grechkos_ministry", c=5, h=1, e=[
    dm("af", {"conscription_factor": 0.05, "training_time_factor": -0.05}), fac("the_military", 5)],
  n="Wehrgesetz von 1967: zwei Jahre Dienst, DOSAAF-Vorausbildung.")
F("ustinovs_ministry", "Ustinov's Ministry", "army", "theatres_of_military_operations|against_dedovshchina",
  av="Datum ≥ 01.05.1976", c=5, h=1, e=[
      dm("af", {"equipment_cost_multiplier_modifier": -0.03}), fac("defense_industry", 10), fac("the_military", -5)],
  n="Dmitri Ustinow, der „Rüstungsmanager“, wird 1976 Verteidigungsminister.")
F("the_army_of_a_superpower", "The Army of a Superpower", "army", "ustinovs_ministry,t80_gas_turbine|operational_manoeuvre_groups", c=7, e=[
    idea("army_of_a_superpower", "Army of a Superpower", {"army_attack_factor": 0.02, "army_defence_factor": 0.02, "army_org_factor": 0.03}),
    xp("army", 50)])

# ============================================================== STRATEGIC FORCES & AIR DEFENCE
F("strategic_rocket_forces", "Strategic Rocket Forces", "str", c=3, h=1, av=ROOT_AV, e=[
    tech("CAT_intercontinental_ballistic_missiles", 1, 50), fac("the_military", 3)])
F("nuclear_parity", "Nuclear Parity", "str", "strategic_rocket_forces", c=5, h=1, e=[
    ws(3), idea("nuclear_parity", "Nuclear Parity", {"war_support_factor": 0.02, "enemy_justify_war_goal_time": 0.10}), tension(1)],
  n="1969/70 erreicht die UdSSR erstmals die Zahl amerikanischer Interkontinentalraketen.")
F("the_heavy_icbm", "R-36M: The Heavy ICBM", "str", "nuclear_parity", mx="mirv_and_mobile_launchers", c=7, e=[
    tech("CAT_intercontinental_ballistic_missiles", 2, 50), tension(2), fac("defense_industry", 5)],
  n="SS-18 „Satan“ – Erstschlagsfähigkeit gegen Minuteman-Silos.")
F("mirv_and_mobile_launchers", "MIRVs and Mobile Launchers", "str", "nuclear_parity", mx="the_heavy_icbm", c=7, e=[
    tech("CAT_transporter_erector_launchers", 1, 75), tech("CAT_intercontinental_ballistic_missiles", 1, 50)],
  n="Überlebensfähigkeit statt Masse.")
F("pioneer_the_ss20", "Pioneer: The SS-20", "str", "the_heavy_icbm|mirv_and_mobile_launchers", av="Datum ≥ 01.01.1976", c=5, e=[
    tech("CAT_intermediate_range_ballistic_missiles", 1, 75), tension(2), op("GER", -10, key="COLDWAR_SOV_euromissiles")],
  n="Löst die Nachrüstungskrise aus – Europa als Geisel.")
F("pvo_strany", "PVO Strany", "str", "strategic_rocket_forces", c=5, h=1, e=[
    tech("CAT_surface_to_air_missiles", 1, 50), dm("af", {"static_anti_air_damage_factor": 0.10})],
  n="Die Luftverteidigung des Landes – eigene Teilstreitkraft.")
F("the_moscow_shield", "A-35: The Moscow Shield", "str", "pvo_strany", c=7, h=1, e=[
    build("aa"), build("aa"), tech("CAT_anti_air", 1, 50), gdp(0.6)])
F("frontal_aviation", "Frontal Aviation", "str", "strategic_rocket_forces", c=5, h=1, e=[mastery("air", 50), xp("air", 25)])
F("swing_wings", "Swing Wings: MiG-23 and Su-24", "str", "frontal_aviation", c=5, h=1, e=[
    tech(["CAT_wing_designs", "CAT_medium_aircraft"], 1, 50)])
F("mig25_foxbat", "MiG-25 Foxbat", "str", "frontal_aviation", c=5, h=1, e=[tech("CAT_air_engines", 1, 50), dm("af", {"air_intercept_efficiency": 0.05})])
F("long_range_aviation", "Long-Range Aviation", "str", "frontal_aviation", c=5, h=1, e=[tech("CAT_heavy_aircraft", 1, 50)], n="Tu-22M „Backfire“.")
F("the_fourth_generation", "The Fourth Generation", "str", "swing_wings|mig25_foxbat", av="Datum ≥ 01.01.1977", c=7, e=[
    tech("CAT_medium_aircraft", 2, 50), sp("sp_aircraft_project", 15)], n="Su-27 und MiG-29.")
F("civil_defence_of_the_ussr", "Civil Defence of the USSR", "str", "pvo_strany", c=5, h=1, e=[
    dm("af", {"army_core_defence_factor": 0.03}), stab(1), dm("gp", {"social_cost_multiplier_modifier": 0.02})])
F("strategic_superiority", "The Correlation of Forces", "str", "pioneer_the_ss20|the_moscow_shield,the_fourth_generation", c=7, e=[
    idea("correlation_of_forces", "The Correlation of Forces", {"war_support_factor": 0.03, "political_power_factor": 0.03,
                                                               "enemy_justify_war_goal_time": 0.15}),
    tension(1)], n="„Das Kräfteverhältnis hat sich zugunsten des Sozialismus verschoben“ (XXV. Parteitag 1976).")

# ============================================================== NAVY
F("gorshkovs_navy", "Gorshkov's Ocean-Going Navy", "navy", c=3, h=1, av=ROOT_AV, e=[
    xp("navy", 25), dm("af", {"navy_max_range_factor": 0.05})], n="Admiral Sergei Gorschkow, Oberbefehlshaber 1956–1985.")
F("okean_70", "Exercise Okean-70", "navy", "gorshkovs_navy", av="Datum < 01.01.1972", c=3, h=1, e=[
    xp("navy", 50), ws(2), tension(1)], n="April 1970: das größte Marinemanöver der Nachkriegszeit, alle vier Flotten.")
F("the_navy_question", "Sea Power of the State", "navy", "gorshkovs_navy", c=3, h=1, e=[txt("U-Boote oder Überwasserflotte? Gegenseitig exklusiv")])
F("the_submarine_fleet", "The Submarine Fleet", "navy", "the_navy_question", mx="carriers_and_cruisers", c=5, h=1, e=[
    tech(["CAT_missile_submarines", "CAT_attack_submarines"], 1, 50)])
F("the_bastion_strategy", "The Bastion Strategy", "navy", "the_submarine_fleet", c=5, h=1, e=[
    dm("af", {"navy_submarine_attack_factor": 0.05}), tech("CAT_naval_sonar", 1, 50)],
  n="SSBN in geschützten Bastionen (Barentssee, Ochotskisches Meer).")
F("lira_the_titanium_submarine", "Lira: The Titanium Submarine", "navy", "the_submarine_fleet", c=7, e=[
    tech("CAT_submarine_engines", 1, 75), gdp(0.5)], n="Projekt 705 „Alfa“.")
F("akula_the_typhoon", "Akula: The Typhoon", "navy", "the_bastion_strategy|lira_the_titanium_submarine", av="Datum ≥ 01.01.1977", c=7, e=[
    tech("CAT_missile_submarines", 2, 50), sp("sp_naval_vessel_project", 15)])
F("carriers_and_cruisers", "Carriers and Cruisers", "navy", "the_navy_question", mx="the_submarine_fleet", c=5, e=[
    tech(["CAT_aircraft_carriers", "CAT_cruisers"], 1, 50), build("dock", 1.0)])
F("the_kiev_class", "The Kiev Class", "navy", "carriers_and_cruisers", c=7, e=[
    tech("CAT_aircraft_carriers", 1, 75), dm("af", {"industrial_capacity_dockyard": 0.05})], n="Schwere Flugzeugträgerkreuzer ab 1975.")
F("kirov_the_battlecruiser", "Kirov: The Battlecruiser", "navy", "carriers_and_cruisers", av="Datum ≥ 01.01.1977", c=7, e=[
    tech(["CAT_cruisers", "CAT_naval_anti_ship_missiles"], 1, 50)])
F("the_fifth_eskadra", "The Fifth Eskadra", "navy", "okean_70|the_navy_question", c=5, h=1, e=[
    dm("af", {"navy_max_range_factor": 0.05}),
    offer("tartus_supply_point", "SYR", "Marine-Versorgungspunkt Tartus (1971). Bei Annahme: Syrien erhält Militärhilfe (+5 % Organisation), UdSSR Reichweite Marine +5 %"),
    txt("Antwortet auf Ägyptens Angebot „Facilities for the Eskadra“ (EGY-Baum), falls angenommen"),
], n="Das Mittelmeergeschwader, Gegengewicht zur 6. US-Flotte.")
F("naval_missile_aviation", "Naval Missile Aviation", "navy", "the_navy_question", c=5, h=1, e=[tech("CAT_air_to_naval_weapons", 1, 50)])
F("bases_on_three_oceans", "Bases on Three Oceans", "navy", "the_fifth_eskadra", c=5, e=[
    offer("naval_access", ["SOM", "SYE", "VIE"], "Hafenrechte (Berbera, Aden, Cam Ranh). Bei Annahme: Partner erhält Hilfe 0,3 % unseres BIP; wir Reichweite Marine +5 % je Hafen"),
], n="Nur per Angebot – kein Partner wird gezwungen.")
F("the_shipyards_of_the_north", "Severodvinsk and Nikolaev", "navy", "the_navy_question", c=7, h=1, e=[build("dock", 1.0), build("dock", 1.0)])
F("a_navy_of_a_superpower", "A Navy of a Superpower", "navy", "akula_the_typhoon|kirov_the_battlecruiser|the_kiev_class,bases_on_three_oceans", c=7, e=[
    idea("blue_water_navy", "Blue-Water Navy", {"navy_max_range_factor": 0.10, "naval_damage_factor": 0.03, "navy_org_factor": 0.03}),
    xp("navy", 50)])

# ============================================================== KGB
F("andropovs_kgb", "Andropov's KGB", "kgb", c=3, h=1, av=ROOT_AV, e=[
    dm("ps", {"drift_defence_factor": 0.05}), fac("intelligence_community", 5)], n="Juri Andropow, KGB-Vorsitzender 1967–1982.")
F("the_fifth_directorate", "The Fifth Directorate", "kgb", "andropovs_kgb", c=5, h=1, e=[
    dm("ps", {"mdcw_cw_ideological_defence": 0.10, "foreign_subversive_activites": -0.10}), fac("intelligence_community", 5)],
  n="1967 gegründet zur Bekämpfung „ideologischer Diversion“.")
F("the_dissident_question", "The Dissident Question", "kgb", "the_fifth_directorate", c=3, h=1, e=[txt("Drei Antworten, gegenseitig exklusiv")])
F("punitive_psychiatry", "Punitive Psychiatry", "kgb", "the_dissident_question", mx="exile_and_expulsion,tolerate_the_samizdat", c=5, e=[
    idea("silenced_dissent", "Silenced Dissent", {"stability_factor": 0.03, "drift_defence_factor": 0.10, "research_speed_factor": -0.02,
                                                  "trade_opinion_factor": -0.05}, swap="Samizdat and Dissent"),
    fac("intelligence_community", 5), op("USA", -5, key="COLDWAR_SOV_human_rights")],
  n="Die „Psychuschka“ – Diagnose „träge Schizophrenie“.")
F("exile_and_expulsion", "Exile and Expulsion", "kgb", "the_dissident_question", mx="punitive_psychiatry,tolerate_the_samizdat", c=5, h=1, e=[
    idea("dissent_abroad", "Dissent Abroad", {"stability_factor": 0.01, "democratic_drift": 0.01, "trade_opinion_factor": -0.03},
         swap="Samizdat and Dissent"),
    ev("solzhenitsyn_expelled", "Solschenizyn wird ausgebürgert und nach Frankfurt ausgeflogen")],
  n="Historischer Mittelweg: Gorki-Verbannung für Sacharow, Ausbürgerung für Solschenizyn (1974).")
F("tolerate_the_samizdat", "Tolerate the Samizdat", "kgb", "the_dissident_question", mx="punitive_psychiatry,exile_and_expulsion", c=5, e=[
    idea("socialist_pluralism", "Socialist Pluralism", {"research_speed_factor": 0.03, "democratic_drift": 0.03, "stability_factor": -0.02},
         swap="Samizdat and Dissent"),
    bop(-0.10), fac("intelligence_community", -10), party(2, 3)])
F("the_refusenik_question", "The Refusenik Question", "kgb", "the_fifth_directorate", c=3, h=1, e=[txt("Jüdische Emigration – gegenseitig exklusiv")])
F("open_the_gates", "Open the Gates", "kgb", "the_refusenik_question", mx="the_diploma_tax", c=5, e=[
    dm("gp", {"trade_opinion_factor": 0.10}), dm("ps", {"research_speed_factor": -0.01}), op("USA", 10, key="COLDWAR_SOV_human_rights"),
    op("ISR", 5, key="COLDWAR_SOV_human_rights")], n="Erleichtert den Handel (Jackson-Vanik), kostet Fachkräfte.")
F("the_diploma_tax", "The Diploma Tax", "kgb", "the_refusenik_question", mx="open_the_gates", c=3, h=1, e=[
    gdp_gain(0.1), dm("gp", {"trade_opinion_factor": -0.10}), op("USA", -10, key="COLDWAR_SOV_human_rights")],
  n="August 1972: Ausreisende müssen ihre Ausbildung zurückzahlen.")
F("the_first_chief_directorate", "The First Chief Directorate", "kgb", "andropovs_kgb", c=5, h=1, e=[
    dm("ps", {"intel_network_gain_factor": 0.10, "decryption_factor": 0.05})])
F("active_measures", "Active Measures", "kgb", "the_first_chief_directorate", c=5, h=1, e=[
    dm("cw", {"mdcw_cw_support_effectiveness": 0.10}), dm("ps", {"foreign_influence_modifier": 0.05})], n="Dienst A: Desinformation, Fälschungen, Friedensbewegungen.")
F("the_illegals", "The Illegals", "kgb", "the_first_chief_directorate", c=5, e=[dm("ps", {"intel_network_gain_factor": 0.10, "encryption_factor": 0.05})])
F("kgb_border_troops", "KGB Border Troops", "kgb", "andropovs_kgb", c=5, h=1, e=[coh(2), dm("ps", {"foreign_subversive_activites": -0.05})])
F("operation_ryan", "Operation RYaN", "kgb", "active_measures|the_illegals", av="Datum ≥ 01.05.1981", c=5, h=1, e=[
    dm("af", {"planning_speed": 0.05}), tension(1), ws(2)], n="Raketno-Jadernoje Napadenije – Suche nach Anzeichen eines westlichen Erstschlags.")
F("the_anti_corruption_drive", "The Anti-Corruption Drive", "kgb", "kgb_border_troops|the_first_chief_directorate", c=7, e=[
    corr(-1), dm("ps", {"corruption_cost_factor": -0.10}), fac("communist_cadres", -10), bop(0.05)])
F("the_shield_and_the_sword", "The Shield and the Sword", "kgb", "the_anti_corruption_drive|operation_ryan", c=7, e=[
    idea("shield_and_sword", "The Shield and the Sword", {"intelligence_agency_defense": 0.15, "drift_defence_factor": 0.05,
                                                          "foreign_subversive_activites": -0.10}), fac("intelligence_community", 5)])

# ============================================================== THE UNION OF REPUBLICS
F("the_union_of_republics", "The Union of Republics", "union", c=3, h=1, av=ROOT_AV, e=[
    coh(3), dec("union_category", "Kategorie „Die Union“: Entwicklungsfonds der Republiken, Kaderrotation, Russischkampagne, souveräne Rechte – "
                                  "jede Entscheidung verschiebt den Zusammenhalt und kostet PP oder BIP")],
  n="Die 14 Unionsrepubliken sind 1970 eigene Subjekt-Länder (Autonomie „Sowjetrepublik“). Zusammenhalt 0–100, Start 62.")
F("local_barons_or_moscows_men", "Local Barons or Moscow's Men?", "union", "the_union_of_republics", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("trust_the_local_barons", "Trust the Local Barons", "union", "local_barons_or_moscows_men", mx="rotate_the_cadres", c=5, h=1, e=[
    coh(6), dm("ps", {"corruption_cost_factor": 0.05}), dm("un", {"stability_factor": 0.02})],
  n="Kunajew, Raschidow, Alijew, Schtscherbizki – Loyalität gegen Freiraum.")
F("rotate_the_cadres", "Rotate the Cadres", "union", "local_barons_or_moscows_men", mx="trust_the_local_barons", c=5, e=[
    coh(-3), dm("ps", {"corruption_cost_factor": -0.05, "mdcw_cw_ideological_defence": 0.05}), fac("communist_cadres", -5)],
  n="Russische Zweite Sekretäre in allen Republiken – Kontrolle statt Vertrauen.")
F("the_ukrainian_question", "The Ukrainian Question", "union", "the_union_of_republics", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("shelests_ukraine", "Shelest's Ukraine", "union", "the_ukrainian_question", mx="the_shcherbytsky_line", c=5, e=[
    coh(4), party(19, 3), dm("un", {"nationalist_drift": 0.01})], n="Alt-Hist: Schelests „Unsere Sowjetukraine“ bleibt Linie.")
F("the_shcherbytsky_line", "The Shcherbytsky Line", "union", "the_ukrainian_question", mx="shelests_ukraine", c=5, h=1, e=[
    coh(2), dm("un", {"drift_defence_factor": 0.05}), fac("communist_cadres", 5), party(19, -2)],
  n="1972: Schelest gestürzt, Säuberung der ukrainischen Intelligenz.")
F("the_baltic_question", "The Baltic Showcase", "union", "the_union_of_republics", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("the_soviet_west", "The Soviet West", "union", "the_baltic_question", mx="industrial_migration", c=5, e=[
    coh(3), dm("gp", {"consumer_goods_factor": -0.01}), dm("cw", {"trade_opinion_factor": 0.03})],
  n="Das Baltikum als Schaufenster: Konsum, Design, Tallinner Fernsehen aus Finnland.")
F("industrial_migration", "Industrial Migration", "union", "the_baltic_question", mx="the_soviet_west", c=5, h=1, e=[
    build("civ", 0.8), coh(-2), dm("un", {"nationalist_drift": 0.01})],
  n="Russische Arbeiter für neue Kombinate in Riga und Tallinn – Wachstum gegen Ressentiment.")
F("the_caucasus", "The Caucasus", "union", "the_union_of_republics", c=5, h=1, e=[coh(1)])
F("shevardnadze_cleans_tbilisi", "Shevardnadze Cleans Up Tbilisi", "union", "the_caucasus", c=5, h=1, e=[
    corr(-1), coh(2), fac("communist_cadres", -3)], n="1972: Eduard Schewardnadse ersetzt Mschawanadse.")
F("aliyev_in_baku", "Aliyev in Baku", "union", "the_caucasus", c=5, h=1, e=[coh(2), dm("gp", {"oil_export_multiplier_modifier": 0.02})])
F("the_karabakh_petitions", "The Karabakh Petitions", "union", "shevardnadze_cleans_tbilisi,aliyev_in_baku", c=3, e=[
    txt("Status quo (Zusammenhalt +2) oder Übergabe an Armenien (Zusammenhalt −4, Meinung ARM +25, AZE −25) – im Event")],
  n="Die Frage, die 1988 die Union zu sprengen beginnt.")
F("the_central_asian_barons", "The Central Asian Barons", "union", "the_union_of_republics", c=5, h=1, e=[coh(2)])
F("the_cotton_affair", "The Cotton Affair", "union", "the_central_asian_barons", c=7, e=[
    corr(-1), coh(-4), dm("ps", {"corruption_cost_factor": -0.05}), fac("intelligence_community", 5)],
  n="Die „Usbekische Affäre“ – Milliarden für Baumwolle, die es nicht gab.")
F("the_language_question", "The Language Question", "union", "trust_the_local_barons|rotate_the_cadres", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("russian_as_lingua_franca", "Russian as the Language of Inter-Ethnic Communication", "union", "the_language_question", mx="native_language_schools", c=5, h=1, e=[
    coh(-2), dm("af", {"training_time_factor": -0.03}), dm("un", {"drift_defence_factor": 0.03})], n="Erlass von 1978.")
F("native_language_schools", "Native Language Schools", "union", "the_language_question", mx="russian_as_lingua_franca", c=5, e=[
    coh(4), dm("af", {"training_time_factor": 0.02})])
F("the_union_treaty_question", "The Union Treaty Question", "union", "the_language_question",
  av="Zusammenhalt der Union < 40 ODER Datum ≥ 01.01.1985", c=3, e=[txt("Die Krise der Union – gegenseitig exklusiv")],
  n="Krisenzweig: wird erst gebraucht, wenn die Union wackelt.")
F("the_renewed_federation", "The Renewed Federation", "union", "the_union_treaty_question", mx="the_iron_union", c=7, e=[
    coh(15), dm("ps", {"political_power_factor": -0.05}), bop(-0.10),
    idea("renewed_federation", "Renewed Federation", {"stability_factor": 0.03, "subjects_autonomy_gain": 0.10, "nationalist_drift": -0.02})])
F("the_iron_union", "The Iron Union", "union", "the_union_treaty_question", mx="the_renewed_federation", c=7, e=[
    coh(8), stab(-5), dm("ps", {"police_cost_multiplier_modifier": 0.10}), bop(0.10), fac("intelligence_community", 5)])
F("the_soviet_people_realised", "The Soviet People", "union", "russian_as_lingua_franca|native_language_schools,the_karabakh_petitions,the_cotton_affair|the_central_asian_barons", c=7, e=[
    coh(8), idea("soviet_people", "The Soviet People", {"stability_factor": 0.02, "nationalist_drift": -0.02, "conscription_factor": 0.02})])

# ============================================================== SOVIET SOCIETY
F("the_soviet_way_of_life", "The Soviet Way of Life", "soc", c=3, h=1, av=ROOT_AV, e=[stab(2), pp(10)])
F("the_alcohol_problem", "The Alcohol Problem", "soc", "the_soviet_way_of_life", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("the_vodka_monopoly", "The Vodka Monopoly", "soc", "the_alcohol_problem", mx="the_1972_temperance_decree", c=3, h=1, e=[
    dm("gp", {"tax_gain_multiplier_modifier": 0.04, "health_cost_multiplier_modifier": 0.05}), dm("gp", {"productivity_growth_modifier": -0.01})],
  n="Ein Viertel der Einzelhandelsumsätze.")
F("the_1972_temperance_decree", "The 1972 Temperance Decree", "soc", "the_alcohol_problem", mx="the_vodka_monopoly", c=5, e=[
    dm("gp", {"tax_gain_multiplier_modifier": -0.03, "productivity_growth_modifier": 0.02, "health_cost_multiplier_modifier": -0.03}), stab(-2)])
F("the_sporting_superpower", "The Sporting Superpower", "soc", "the_soviet_way_of_life", c=5, h=1, e=[stab(2), dm("ps", {"political_power_factor": 0.02})])
F("the_moscow_olympics", "The Moscow Olympics", "soc", "the_sporting_superpower", av="Datum ≥ 01.01.1979", c=7, h=1, e=[
    stab(5), gdp(0.8), build("inf"), ev("olympics", "Olympische Sommerspiele Moskau 1980 – Mischka, Boykott oder Weltfest")],
  n="Vergeben 1974. Boykott durch westliche Spieler ist ein Event mit Wahl.")
F("culture_question", "Between Thaw and Frost", "soc", "the_soviet_way_of_life", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("glavlit_holds_the_line", "Glavlit Holds the Line", "soc", "culture_question", mx="cultural_detente", c=5, h=1, e=[
    dm("ps", {"stability_factor": 0.02, "research_speed_factor": -0.01}), bop(0.05)])
F("cultural_detente", "Cultural Detente", "soc", "culture_question", mx="glavlit_holds_the_line", c=5, e=[
    dm("ps", {"research_speed_factor": 0.01}), dm("ps", {"democratic_drift": 0.01}), stab(1), bop(-0.05)],
  n="Taganka-Theater, Wyssozki, Tarkowski – geduldet statt verboten.")
F("the_church_question", "The Church Question", "soc", "the_soviet_way_of_life", c=3, h=1, e=[txt("Gegenseitig exklusiv")])
F("scientific_atheism", "Scientific Atheism", "soc", "the_church_question", mx="accord_with_the_patriarchate", c=5, h=1, e=[
    dm("ps", {"drift_defence_factor": 0.03}), party(14, -2), party(23, -1)])
F("accord_with_the_patriarchate", "Accord with the Patriarchate", "soc", "the_church_question", mx="scientific_atheism", c=5, e=[
    custom("Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 45) `add_ideas`", ["the_clergy"]),
    stab(3), party(14, 2), party(23, 1), bop(-0.05)])
F("the_double_burden", "The Double Burden", "soc", "the_soviet_way_of_life", c=5, e=[
    dm("gp", {"total_workforce_modifier": 0.02, "social_cost_multiplier_modifier": 0.03}), stab(1)],
  n="Frauen: 51 % der Arbeitskräfte und der ganze Haushalt.")
F("the_demographic_gap", "The Demographic Gap", "soc", "the_double_burden", c=5, e=[
    dm("gp", {"social_cost_multiplier_modifier": 0.03}), dm("ps", {"monthly_population": 0.05}), coh(-1)],
  n="Geburtenraten: Russland 1,9, Usbekistan 5,6 – die Union verschiebt sich nach Süden.")
F("the_developed_socialist_society", "The Developed Socialist Society", "soc", "the_moscow_olympics|the_demographic_gap,glavlit_holds_the_line|cultural_detente", c=7, e=[
    idea("socialist_way_of_life", "The Socialist Way of Life", {"stability_factor": 0.03, "war_support_factor": 0.02})])
