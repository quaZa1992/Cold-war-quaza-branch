from sov_dsl import *

# ============================================================== TRUNK: The Collective Leadership
F("the_collective_leadership", "The Collective Leadership", "pol", c=1, h=1, e=[
    pp(50),
    ev("intro", "„Januar 1970: Die Troika“ – Breschnew, Kossygin, Podgorny; erklärt Politbüro-Balance, Zusammenhalt der Union und die Startgeister"),
    custom("Aktiviert die fünf Länder-Modifier „Der Parteistaat“, „Gosplan – Planwirtschaft“, „Streitkräfte der UdSSR“, „Union der Republiken“ "
           "und „Sozialistische Gemeinschaft“ (Startwerte siehe Konzept) `add_dynamic_modifier`", ["add_dynamic_modifier"]),
], n="Startknoten wie SOV_reign_of_yeltsin (Kosten 1). Alle anderen Bereiche verlangen ihn per `available` (keine Linien quer durch den Baum).")

F("the_lenin_centenary", "The Lenin Centenary", "pol", "the_collective_leadership", c=3, h=1, e=[
    stab(3), party(4, 3), dm("ps", {"political_power_factor": 0.03}),
    ev("lenin_centenary", "22. April 1970 – Jubiläumsmedaille, Kundgebungen, die „Leniniana“ im Fernsehen"),
], n="Die größte Propagandakampagne des Jahrzehnts.")

F("kremlin_politics", "Kremlin Politics", "pol", "the_collective_leadership", c=3, h=1, e=[
    pp(25),
    dec("politburo_category", "Kategorie „Das Politbüro“ (an die Politbüro-Balance gebunden): Reformer stärken, Orthodoxe stärken, "
        "Veteranen pensionieren, Regionalkader nach Moskau holen – jede Entscheidung kostet PP und Fraktionsmeinung"),
], n="Die Politbüro-Balance existiert ab Spielstart (Init); dieser Fokus öffnet die Werkzeuge, sie zu steuern.")

F("the_24th_party_congress", "The XXIV Party Congress", "pol", "the_lenin_centenary", av="Datum ≥ 01.03.1971", c=5, h=1, e=[
    pp(75), stab(2),
    txt("Öffnet „The Ninth Five-Year Plan“ (Gosplan) und „The Peace Programme“ (Entspannung) über `available`"),
], n="30.03.–09.04.1971: Breschnews Friedensprogramm und der IX. Fünfjahrplan.")

F("the_doctrine_of_developed_socialism", "The Doctrine of Developed Socialism", "pol", "the_24th_party_congress", c=5, h=1, e=[
    dm("ps", {"stability_factor": 0.02, "drift_defence_factor": 0.05}), party(4, 3), bop(0.05),
])

F("the_gerontocracy_question", "The Gerontocracy Question", "pol", "the_doctrine_of_developed_socialism",
  av="Datum ≥ 01.01.1975; hat „Stability of Cadres“", c=3, h=1, e=[
      pp(25), txt("Zwei Antworten, gegenseitig exklusiv"),
  ], n="Durchschnittsalter des Politbüros 1975: über 65 Jahre. Die wichtigste Strukturentscheidung des Parteistaats.")

F("renew_the_cadres", "Renew the Cadres", "pol", "the_gerontocracy_question", mx="respect_for_seniority", c=7, e=[
    rmidea("stability_of_cadres", "Stability of Cadres"),
    idea("cadre_renewal", "Cadre Renewal", {"productivity_growth_modifier": 0.03, "research_speed_factor": 0.02, "stability_factor": -0.03}, days=730),
    fac("communist_cadres", -15), bop(-0.10),
], n="Ersetzt die Generation von 1964 – kurzfristig Unruhe, langfristig Dynamik.")

F("respect_for_seniority", "Respect for Seniority", "pol", "the_gerontocracy_question", mx="renew_the_cadres", c=5, h=1, e=[
    idea("era_of_stagnation", "Era of Stagnation",
         {"political_power_factor": 0.10, "stability_factor": 0.05, "productivity_growth_modifier": -0.08,
          "research_speed_factor": -0.03, "corruption_cost_factor": 0.15, "bureaucracy_cost_multiplier_modifier": 0.15},
         swap="Stability of Cadres"),
    fac("communist_cadres", 10), bop(0.05),
], n="Historisch: Zastoi. Bequem für die Partei, teuer für alles andere – kann später nur durch eine Reformführung aufgelöst werden.")

F("the_1977_constitution", "The 1977 Constitution", "pol", "the_doctrine_of_developed_socialism", av="Datum ≥ 01.06.1977", c=5, h=1, e=[
    dm("ps", {"political_power_factor": 0.05, "stability_factor": 0.02}), coh(4),
    ev("constitution_1977", "Die „Breschnew-Verfassung“: Artikel 6 (führende Rolle der Partei) und das „Sowjetvolk“ als neue historische Gemeinschaft"),
])

F("whither_the_union", "Whither the Union?", "pol", "the_24th_party_congress", c=3, h=1, e=[
    pp(25), txt("Richtungswahl wie GENERIC_station_in_the_world (vier Richtungen; Salafist/Schia gibt es für die UdSSR nicht). Eine weitere Richtung öffnet sich erst, wenn inzwischen eine Partei dieses Outlooks regiert (Muster Ägypten Rev. 7)"),
])

_dirs = ["dir_the_leading_role", "dir_convergence", "dir_third_way", "dir_the_russian_idea"]


def _other(me):
    return ",".join(d for d in _dirs if d != me)


F("dir_the_leading_role", "The Leading Role of the Party", "pol", "whither_the_union", c=5, h=1,
  av="Keine andere Richtung erledigt – ODER `has_government = communism` und noch keine Richtung unter dieser Regierung", e=[
      outl(1, 5), bop(0.05),
      idea("party_mobilisation", "Party Mobilisation", {"communism_drift": 0.03, "drift_defence_factor": 0.05}, days=365),
  ])
F("dir_convergence", "The Convergence Memorandum", "pol", "whither_the_union", c=5,
  av="Keine andere Richtung erledigt – ODER `has_government = democratic` und noch keine Richtung unter dieser Regierung", e=[
      outl(0, 5), bop(-0.10), fac("communist_cadres", -10), stab(-3),
      idea("thaw_atmosphere", "Thaw Atmosphere", {"democratic_drift": 0.03, "research_speed_factor": 0.03}, days=365),
  ], n="Sacharows „Gedanken über Fortschritt, friedliche Koexistenz und geistige Freiheit“ (1968) als offizielle Debatte.")
F("dir_third_way", "A Third Way for Socialism", "pol", "whither_the_union", c=5,
  av="Keine andere Richtung erledigt – ODER `has_government = neutrality` und noch keine Richtung unter dieser Regierung", e=[
      outl(3, 5), bop(-0.05),
      idea("third_way_debate", "The Third Way Debate", {"neutrality_drift": 0.03, "productivity_growth_modifier": 0.02}, days=365),
  ])
F("dir_the_russian_idea", "The Russian Idea", "pol", "whither_the_union", c=5,
  av="Keine andere Richtung erledigt – ODER `has_government = nationalist` und noch keine Richtung unter dieser Regierung", e=[
      outl(4, 5), coh(-5), fac("the_military", 5),
      idea("russian_revival", "Russian Revival", {"nationalist_drift": 0.03, "war_support_factor": 0.03}, days=365),
  ], n="Kostet Zusammenhalt: Nicht-Russen lesen „russisch“ als „Russifizierung“.")

# ============================================================== GOSPLAN
F("gosplan_directives", "Gosplan Directives", "eco", c=3, h=1, av="`COLDWAR_SOV_the_collective_leadership` erledigt", e=[
    dm("gp", {"production_speed_buildings_factor": 0.02}),
    dec("five_year_plan_category", "Kategorie „Fünfjahrpläne“: ab dem IX. Plan wählt der Spieler pro Plan eine Priorität (5 Jahre, Wirkung und Kosten)"),
])
F("complete_the_eighth_plan", "Complete the Eighth Five-Year Plan", "eco", "gosplan_directives", c=5, h=1, e=[
    build("civ", 0.8), dm("gp", {"production_factory_efficiency_gain_factor": 0.03}),
], n="1966–1970, der wachstumsstärkste Plan der Nachkriegszeit.")
F("the_kosygin_reform_question", "The Kosygin Reform Question", "eco", "gosplan_directives", c=3, h=1, e=[
    pp(25), txt("Drei Wege, gegenseitig exklusiv"),
], n="Die Reform von 1965 (Gewinn, Prämien, Betriebsautonomie) wird nach Prag schleichend zurückgenommen.")

F("deepen_the_kosygin_reform", "Deepen the Kosygin Reform", "eco", "the_kosygin_reform_question",
  mx="cybernetic_planning,the_ministries_restored", c=5, e=[
      dm("gp", {"productivity_growth_modifier": 0.05, "civilian_industry_tax_modifier": 0.05}),
      bop(-0.10), fac("industrial_conglomerates", -10), fac("communist_cadres", -5), flag("market_reform"),
  ])
F("enterprise_self_financing", "Khozraschyot: Enterprise Self-Financing", "eco", "deepen_the_kosygin_reform", c=5, e=[
    dm("gp", {"corporate_tax_income_multiplier_modifier": 0.05, "productivity_growth_modifier": 0.03}),
    fac("labour_unions", -5), stab(-2),
])
F("lessons_from_budapest", "Lessons from Budapest", "eco", "deepen_the_kosygin_reform", c=5, e=[
    op("HUN", 15, key="COLDWAR_SOV_economic_partners"), dm("gp", {"consumer_goods_factor": -0.02, "trade_opinion_factor": 0.05}),
], n="Ungarns Neuer Ökonomischer Mechanismus (seit 1968) als Vorbild.")
F("legalise_the_cooperatives", "Legalise the Cooperatives", "eco", "enterprise_self_financing,lessons_from_budapest", c=7, e=[
    idea("cooperative_sector", "Cooperative Sector",
         {"tax_gain_multiplier_modifier": 0.03, "consumer_goods_factor": -0.03, "corruption_cost_factor": 0.05},
         swap="The Second Economy"),
    fac("communist_cadres", -10), party(18, 3),
], n="Aus der Schattenwirtschaft wird ein legaler Sektor – die Nomenklatura verliert ihre Pfründe.")

F("cybernetic_planning", "OGAS: Cybernetic Planning", "eco", "the_kosygin_reform_question",
  mx="deepen_the_kosygin_reform,the_ministries_restored", c=5, e=[
      dm("gp", {"production_factory_efficiency_gain_factor": 0.05}), tech("CAT_computing", 1, 50), gdp(0.6),
      fac("industrial_conglomerates", -5), flag("ogas"),
  ], n="Viktor Gluschkows Gesamtstaatliches Automatisiertes System – 1970 vom Politbüro vertagt, hier umgesetzt.")
F("the_ogas_network", "The OGAS Network", "eco", "cybernetic_planning", c=7, e=[
    build("off", 0.7), dm("gp", {"production_factory_efficiency_gain_factor": 0.05, "production_factory_max_efficiency_factor": 0.03}), gdp(0.8),
])
F("kantorovich_optimal_prices", "Kantorovich's Optimal Prices", "eco", "cybernetic_planning", c=5, e=[
    dm("gp", {"productivity_growth_modifier": 0.04, "consumer_goods_factor": -0.02}), fac("communist_cadres", -5),
], n="Leonid Kantorowitsch, Nobelpreis 1975 für lineare Optimierung.")
F("computing_centres_of_the_republics", "Computing Centres of the Republics", "eco", "the_ogas_network,kantorovich_optimal_prices", c=7, e=[
    tech("CAT_information_technology", 1, 50), dm("ps", {"research_speed_factor": 0.02}), coh(2),
])

F("the_ministries_restored", "The Ministries Restored", "eco", "the_kosygin_reform_question",
  mx="deepen_the_kosygin_reform,cybernetic_planning", c=5, h=1, e=[
      dm("gp", {"production_speed_buildings_factor": 0.03, "productivity_growth_modifier": -0.02}),
      fac("industrial_conglomerates", 10), fac("communist_cadres", 5), bop(0.05),
  ])
F("new_union_ministries", "New Union Ministries", "eco", "the_ministries_restored", c=5, h=1, e=[
    dm("gp", {"production_speed_buildings_factor": 0.03}), dm("ps", {"bureaucracy_cost_multiplier_modifier": 0.05}),
    fac("industrial_conglomerates", 5),
])
F("the_tolkachi", "The Tolkachi", "eco", "the_ministries_restored", c=5, h=1, e=[
    dm("gp", {"production_factory_efficiency_gain_factor": 0.03}), dm("ps", {"corruption_cost_factor": 0.05}),
], n="Die „Schieber“ der Betriebe, die Material am Plan vorbei beschaffen – sie halten die Fabriken am Laufen.")
F("plan_fulfilment_campaigns", "Plan Fulfilment Campaigns", "eco", "new_union_ministries,the_tolkachi", c=5, h=1, e=[
    dm("gp", {"industrial_capacity_factory": 0.03}), stab(2), party(4, 2),
])

F("the_ninth_five_year_plan", "The Ninth Five-Year Plan", "eco",
  "legalise_the_cooperatives|computing_centres_of_the_republics|plan_fulfilment_campaigns|deepen_the_kosygin_reform|cybernetic_planning|the_ministries_restored",
  av="`COLDWAR_SOV_the_24th_party_congress` erledigt", c=5, h=1, e=[
      pp(50), txt("Prioritätswahl für 1971–1975 (gegenseitig exklusiv)"), flag("ninth_plan"),
  ])
F("group_b_goods_for_the_people", "Group B: Goods for the People", "eco", "the_ninth_five_year_plan",
  mx="group_a_means_of_production,the_defence_sector_first", c=5, h=1, e=[
      dm("gp", {"consumer_goods_factor": -0.03, "civilian_industry_tax_modifier": 0.03}), stab(3), fac("defense_industry", -5),
  ], n="Der IX. Plan sah erstmals ein schnelleres Wachstum der Konsumgüter (Gruppe B) als der Produktionsmittel vor – auf dem Papier.")
F("the_brezhnevka", "The Brezhnevka", "eco", "group_b_goods_for_the_people", c=5, h=1, e=[
    stab(3), dm("gp", {"social_cost_multiplier_modifier": 0.03}), build("inf", 0.6), dm("un", {"stability_factor": 0.01}),
], n="Neun- bis sechzehngeschossige Plattenbauten lösen die Chruschtschowka ab.")
F("refrigerators_and_televisions", "Refrigerators and Televisions", "eco", "group_b_goods_for_the_people", c=5, e=[
    build("civ", 0.8), dm("gp", {"consumer_goods_factor": -0.02}), stab(2),
])
F("group_a_means_of_production", "Group A: Means of Production", "eco", "the_ninth_five_year_plan",
  mx="group_b_goods_for_the_people,the_defence_sector_first", c=5, e=[
      dm("gp", {"industrial_capacity_factory": 0.03, "production_speed_buildings_factor": 0.04, "consumer_goods_factor": 0.02}),
      build("civ2", 1.5),
  ])
F("steel_cities", "Magnitka and Cherepovets", "eco", "group_a_means_of_production", c=5, e=[
    custom("Ressource: +8 Stahl in einem eigenen Staat mit Stahl `random_owned_controlled_state` `add_resource`", ["add_resource"]),
    build("indinf", 0.6),
])
F("machine_building_first", "Machine-Building First", "eco", "group_a_means_of_production", c=5, e=[
    dm("gp", {"production_factory_max_efficiency_factor": 0.04}), tech("CAT_production_lines", 1, 50),
])
F("the_defence_sector_first", "The Defence Sector First", "eco", "the_ninth_five_year_plan",
  mx="group_b_goods_for_the_people,group_a_means_of_production", c=5, e=[
      build("mil2", 1.2), dm("gp", {"military_industry_tax_modifier": 0.05, "consumer_goods_factor": 0.03}),
      fac("defense_industry", 10), bop(0.05),
  ])
F("the_nine_ministries", "The Nine Defence Ministries", "eco", "the_defence_sector_first", c=5, e=[
    dm("af", {"equipment_cost_multiplier_modifier": -0.03}), dm("gp", {"production_speed_arms_factory_factor": 0.10}),
], n="Die „Neun“ des Rüstungskomplexes (Mittelmaschinenbau, Luftfahrt, Schiffbau …) mit eigenen Städten und Schulen.")
F("dual_use_factories", "Dual-Use Factories", "eco", "the_defence_sector_first", c=5, e=[
    dm("gp", {"consumer_goods_factor": -0.02, "military_industry_tax_modifier": 0.02}), build("civ", 0.8),
], n="Panzerfabriken bauen nebenher Kühlschränke – schlecht, aber besser als keine.")

F("avtovaz_the_zhiguli", "AvtoVAZ: The Zhiguli", "eco", "complete_the_eighth_plan", c=5, h=1, e=[
    build("civ", 0.9), op("ITA", 10, key="COLDWAR_SOV_economic_partners"), dm("gp", {"consumer_goods_factor": -0.02}),
], n="Togliatti, erster Lada am 19.04.1970 – Fiat-Lizenz von 1966.")
F("kamaz_the_kama_truck_works", "KamAZ: The Kama Truck Works", "eco", "avtovaz_the_zhiguli", c=7, h=1, e=[
    build("civ", 1.0), tech("CAT_utility_vehicles", 1, 50), dm("af", {"supply_consumption_factor": -0.02}),
], n="Naberezhnye Chelny, gebaut 1969–1976 mit westlichen Werkzeugmaschinen.")

F("the_price_question", "The Price Question", "eco", "the_ninth_five_year_plan", c=3, h=1, e=[
    txt("Novotscherkassk 1962 sitzt der Führung im Nacken – gegenseitig exklusiv"),
])
F("raise_retail_prices", "Raise Retail Prices", "eco", "the_price_question", mx="hold_the_prices", c=5, e=[
    dm("gp", {"tax_gain_multiplier_modifier": 0.05, "consumer_goods_factor": -0.02}), stab(-6), fac("labour_unions", -10),
    rmidea("second_economy", "The Second Economy"),
], n="Ehrliche Preise entziehen dem Schwarzmarkt die Grundlage – um den Preis von Unruhen.")
F("hold_the_prices", "Hold the Prices", "eco", "the_price_question", mx="raise_retail_prices", c=3, h=1, e=[
    stab(3), dm("gp", {"tax_gain_multiplier_modifier": -0.03, "consumer_goods_factor": 0.02}),
], n="Brot kostet 1980 so viel wie 1955 – subventioniert, oft nicht erhältlich.")

F("the_unified_system_question", "The Unified System Question", "eco", "the_ninth_five_year_plan", c=3, h=1, e=[
    txt("Welche Computer baut der Ostblock? Gegenseitig exklusiv"),
])
F("ryad_copy_the_ibm_360", "Ryad: Copy the IBM/360", "eco", "the_unified_system_question", mx="continue_the_besm_line", c=5, h=1, e=[
    tech("CAT_computing", 2, 50), dm("ps", {"research_speed_factor": -0.01}),
    dm("cw", {"research_sharing_per_country_bonus_factor": 0.05}),
], n="Die Entscheidung von 1969/70: schnelle Kompatibilität, aber eigene Entwicklung verkümmert.")
F("continue_the_besm_line", "Continue the BESM Line", "eco", "the_unified_system_question", mx="ryad_copy_the_ibm_360", c=7, e=[
    tech("CAT_computing", 1, 25), dm("ps", {"research_speed_factor": 0.03}), gdp(0.6),
], n="Lebedews eigene Architektur – langsamer, aber unabhängig.")
F("microelectronics_of_zelenograd", "Microelectronics of Zelenograd", "eco", "ryad_copy_the_ibm_360|continue_the_besm_line", c=7, e=[
    build("chip", 1.0), tech("CAT_microchips", 1, 50),
])

F("the_tenth_five_year_plan", "The Tenth Five-Year Plan", "eco",
  "the_brezhnevka|refrigerators_and_televisions|steel_cities|machine_building_first|the_nine_ministries|dual_use_factories",
  av="Datum ≥ 01.01.1976", c=5, h=1, e=[
      pp(50), dm("gp", {"productivity_growth_modifier": 0.03}), txt("„Plan der Effizienz und Qualität“; neue Prioritätswahl in der Kategorie Fünfjahrpläne"),
  ])
F("the_shchekino_method", "The Shchekino Method", "eco", "the_tenth_five_year_plan", c=5, e=[
    dm("gp", {"productivity_growth_modifier": 0.04}), fac("labour_unions", -10), stab(-2),
], n="Chemiekombinat Schtschokino (1967): weniger Arbeiter, gleicher Lohnfonds, höhere Prämien.")
F("quality_mark_of_the_ussr", "The State Quality Mark", "eco", "the_tenth_five_year_plan", c=5, h=1, e=[
    dm("gp", {"production_factory_max_efficiency_factor": 0.03}), dm("cw", {"trade_opinion_factor": 0.05}),
])
F("the_1979_economic_mechanism", "The 1979 Economic Mechanism", "eco", "the_shchekino_method|quality_mark_of_the_ussr",
  av="Datum ≥ 01.07.1979", c=5, h=1, e=[
      dm("gp", {"productivity_growth_modifier": 0.03, "production_factory_efficiency_gain_factor": 0.03}),
  ], n="Die letzte große Planreform der Breschnew-Zeit.")
F("the_scientific_technical_revolution", "The Scientific-Technical Revolution", "eco",
  "the_1979_economic_mechanism,microelectronics_of_zelenograd", c=10, e=[
      dm("gp", {"productivity_growth_modifier": 0.05}), dm("ps", {"research_speed_factor": 0.03}),
      idea("scientific_technical_revolution", "Scientific-Technical Revolution",
           {"production_factory_max_efficiency_factor": 0.05, "research_speed_factor": 0.03}),
  ], n="Abschluss des Wirtschaftszweigs.")

# ============================================================== AGRICULTURE
F("the_agrarian_problem", "The Agrarian Problem", "agr", c=3, h=1, av="`COLDWAR_SOV_the_collective_leadership` erledigt", e=[
    pp(15), dm("gp", {"agricolture_productivity_modifier": 0.03}), txt("Zwei Grundwege, gegenseitig exklusiv"),
], n="Ein Viertel aller Investitionen fließt in die Landwirtschaft – und die Ernten schwanken trotzdem um 20 %.")
F("pour_capital_into_the_kolkhozy", "Pour Capital into the Kolkhozy", "agr", "the_agrarian_problem", mx="the_link_system", c=5, h=1, e=[
    build("agr", 0.8), dm("gp", {"agricolture_productivity_modifier": 0.03}), fac("farmers", 5), gdp(0.4),
])
F("fertiliser_and_machinery", "Fertiliser and Machinery", "agr", "pour_capital_into_the_kolkhozy", c=5, h=1, e=[
    build("agr", 0.8), tech("CAT_agriculture", 1, 50),
])
F("land_melioration", "Land Melioration", "agr", "pour_capital_into_the_kolkhozy", c=5, h=1, e=[
    dm("gp", {"agricolture_productivity_modifier": 0.04}), gdp(0.8),
])
F("the_non_black_earth_programme", "The Non-Black-Earth Programme", "agr", "fertiliser_and_machinery,land_melioration",
  av="Datum ≥ 01.03.1974", c=7, h=1, e=[
      dm("gp", {"agricolture_productivity_modifier": 0.05}), build("agr2", 1.4), coh(-2),
  ], n="1974: das russische Kernland bekommt, was bisher Ukraine und Kasachstan bekamen.")
F("the_link_system", "The Link System", "agr", "the_agrarian_problem", mx="pour_capital_into_the_kolkhozy", c=5, e=[
    dm("gp", {"agricolture_productivity_modifier": 0.08, "agriculture_workers_modifier": -0.10}),
    bop(-0.05), fac("farmers", 10), fac("communist_cadres", -5),
], n="Iwan Chudenkos Experiment mit kleinen autonomen Brigaden (Ilijsk 1960er) – historisch abgebrochen, Chudenko starb 1974 in Haft.")
F("enlarge_the_private_plots", "Enlarge the Private Plots", "agr", "the_link_system", c=5, e=[
    dm("gp", {"consumer_goods_factor": -0.03}), stab(2), fac("farmers", 5),
], n="Die Hofparzellen: 3 % der Fläche, ein Viertel der Lebensmittel.")
F("kolkhoz_markets", "Free Kolkhoz Markets", "agr", "the_link_system", c=5, e=[
    dm("gp", {"agriculture_tax_modifier": 0.05}), dm("ps", {"corruption_cost_factor": -0.03}),
])
F("contract_farming", "Contract Farming", "agr", "enlarge_the_private_plots,kolkhoz_markets", c=7, e=[
    dm("gp", {"agricolture_productivity_modifier": 0.06}), party(18, 2), fac("communist_cadres", -5),
])
F("the_harvest_of_1972", "The Harvest of 1972", "agr", "the_agrarian_problem", av="Datum ≥ 01.08.1972", c=3, h=1, e=[
    txt("Dürre und Frost: Getreideernte 13 % unter Plan. Zwei Antworten, gegenseitig exklusiv"),
])
F("buy_grain_abroad", "Buy Grain Abroad", "agr", "the_harvest_of_1972", mx="tighten_the_belts", c=3, h=1, e=[
    gdp(1.0), stab(3), op("USA", 5, key="COLDWAR_SOV_grain_customer"), flag("grain_importer"),
    dec("grain_import_decisions", "Wiederholbare Getreidekäufe bei Missernten (Kosten nach BIP)"),
], n="Der „Große Getreideraub“ 1972: Moskau kauft still ein Viertel der US-Ernte.")
F("tighten_the_belts", "Tighten the Belts", "agr", "the_harvest_of_1972", mx="buy_grain_abroad", c=3, e=[
    stab(-6), dm("gp", {"consumer_goods_factor": 0.02}), fac("farmers", -5),
], n="Keine Devisen für Getreide – die Schlangen werden länger.")
F("virgin_lands_renewal", "Virgin Lands Renewal", "agr", "the_agrarian_problem", c=5, h=1, e=[
    build("agr", 0.8), dm("gp", {"agricolture_productivity_modifier": 0.03}), coh(1),
])
F("white_gold", "White Gold", "agr", "virgin_lands_renewal", c=3, h=1, e=[txt("Baumwolle aus Usbekistan – gegenseitig exklusiv")])
F("irrigate_the_desert", "Irrigate the Desert", "agr", "white_gold", mx="save_the_aral_sea", c=5, h=1, e=[
    dm("gp", {"agriculture_tax_modifier": 0.06, "resource_export_multiplier_modifier": 0.03}), coh(3), flag("aral_disaster"),
    dm("ps", {"corruption_cost_factor": 0.03}),
], n="Amu-Darja und Syr-Darja werden umgeleitet. Ab 1980 kann das Event „Der sterbende Aralsee“ feuern (Stabilität, Zusammenhalt).")
F("save_the_aral_sea", "Save the Aral Sea", "agr", "white_gold", mx="irrigate_the_desert", c=5, e=[
    dm("gp", {"agriculture_tax_modifier": -0.02}), party(17, 3), coh(-2),
])
F("turn_the_siberian_rivers", "Turn the Siberian Rivers", "agr", "irrigate_the_desert", c=10, e=[
    gdp(3.0), dm("gp", {"agricolture_productivity_modifier": 0.10}), stab(-3), party(17, -3), coh(4),
], n="Das Sibaral-Projekt (Planung ab 1970er, 1986 abgesagt): Wasser aus Ob und Irtysch nach Zentralasien.")
F("the_food_programme", "The Food Programme", "agr", "the_non_black_earth_programme|contract_farming",
  av="Datum ≥ 01.05.1982 ODER `COLDWAR_SOV_contract_farming` erledigt", c=7, h=1, e=[
      rmidea("agrarian_problem", "The Agrarian Problem"), dm("gp", {"agricolture_productivity_modifier": 0.04, "consumer_goods_factor": -0.02}),
  ], n="Erst hier verschwindet der Startgeist „The Agrarian Problem“.")

# ============================================================== ENERGY, SIBERIA, BAM
F("samotlor", "Samotlor: West Siberian Oil", "en", c=5, h=1, av="`COLDWAR_SOV_the_collective_leadership` erledigt", e=[
    custom("Ressource: +10 Öl in einem eigenen Staat mit Öl `random_owned_controlled_state` `add_resource`", ["add_resource"]),
    dm("gp", {"oil_export_multiplier_modifier": 0.05}),
], n="Das größte Ölfeld der UdSSR (entdeckt 1965); Förderung verzehnfacht sich bis 1980.")
F("the_tyumen_complex", "The Tyumen Oil and Gas Complex", "en", "samotlor", c=5, h=1, e=[
    build("inf", 0.8), custom("Ressource: +8 Öl in einem eigenen Staat mit Öl `add_resource`", ["add_resource"]),
    dm("gp", {"resource_export_multiplier_modifier": 0.03}),
])
F("gas_for_pipes", "Gas for Pipes", "en", "samotlor", c=5, h=1, e=[
    offer("gas_for_pipes", "GER", "Röhren von Mannesmann auf Kredit gegen sowjetisches Erdgas ab 1973. Bei Annahme: UdSSR erhält Forschungsbonus Infrastruktur, Handelsmeinung +10 %, Schulden 0,5 % BIP; BRD erhält Energiebonus"),
    op("GER", 10, key="COLDWAR_SOV_energy_partner"),
], n="Februar 1970, Ruhrgas–Mannesmann–Sojusnefteexport. Nur als Angebot (Spieler-BRD entscheidet).")
F("urengoy", "Urengoy: The Gas Giant", "en", "the_tyumen_complex", c=7, e=[
    dm("gp", {"energy_gain_multiplier": 0.05, "oil_export_multiplier_modifier": 0.05}), build("energy", 0.8),
])
F("petrodollars", "Petrodollars", "en", "urengoy|the_tyumen_complex", av="Ölpreis-Level (Cold War) ≥ 2 ODER Datum ≥ 01.01.1974", c=5, e=[
    gdp_gain(1.0),
    idea("oil_dependency", "Oil Dependency", {"oil_export_multiplier_modifier": 0.10, "productivity_growth_modifier": -0.03}),
], n="Nach 1973 finanzieren Öl und Gas Getreideimporte und Klientelstaaten – und ersetzen die Reform.")
F("the_atomic_power_programme", "The Atomic Power Programme", "en", "samotlor", c=3, h=1, e=[
    txt("Welcher Reaktortyp? Gegenseitig exklusiv")])
F("rbmk_reactors", "RBMK: Channel Reactors", "en", "the_atomic_power_programme", mx="vver_reactors", c=5, h=1, e=[
    dm("gp", {"production_speed_nuclear_reactor_factor": 0.20, "nuclear_energy_generation_modifier": 0.05}), flag("rbmk"),
], n="Billig, groß, ohne Containment. Setzt ein Risikoflag: Unfälle sind später per Event möglich.")
F("vver_reactors", "VVER: Pressurised Reactors", "en", "the_atomic_power_programme", mx="rbmk_reactors", c=7, e=[
    dm("gp", {"nuclear_energy_generation_modifier": 0.10}), gdp(0.8),
])
F("the_leningrad_station", "The Leningrad Station", "en", "rbmk_reactors|vver_reactors", c=7, h=1, e=[
    build("nuc", 1.2)], n="Sosnowy Bor, erster Block 1973.")
F("atoms_for_the_republics", "Atoms for the Republics", "en", "the_leningrad_station", c=7, e=[
    build("nuc", 1.2), coh(2)])
F("the_great_siberian_dams", "The Great Siberian Dams", "en", "samotlor", c=7, h=1, e=[
    build("ren", 0.8), dm("gp", {"energy_gain_multiplier": 0.05}), party(17, -1),
], n="Krasnojarsk (1972), Sajano-Schuschenskaja (Baubeginn 1968).")
F("the_baikal_amur_mainline", "The Baikal-Amur Mainline", "en", "the_great_siberian_dams|the_tyumen_complex",
  av="Datum ≥ 01.04.1974", c=10, h=1, e=[
      gdp(2.0), build("inf3"), party(4, 2), dm("af", {"supply_consumption_factor": -0.02}),
      idea("bam_construction", "Construction of the Century", {"production_speed_rail_way_factor": 0.25, "consumer_goods_factor": 0.02}, days=1825),
  ], n="„Baustelle des Jahrhunderts“ – Komsomol-Freiwillige, 4.300 km durch Taiga und Permafrost.")
F("bam_open_to_traffic", "BAM Open to Traffic", "en", "the_baikal_amur_mainline", av="Datum ≥ 01.01.1980", c=7, e=[
    build("inf2"), dm("gp", {"resource_export_multiplier_modifier": 0.05}), dm("af", {"supply_consumption_factor": -0.02}),
    txt("Bonus für „The Chinese Question“: Nachschub im Fernen Osten verbessert (`COLDWAR_SOV_bam_open`)"), flag("bam_open"),
])

F("kuzbass_and_ekibastuz", "Kuzbass and Ekibastuz", "en", "the_tyumen_complex", c=5, h=1, e=[
    build("energy", 0.8), dm("gp", {"fossil_pp_energy_generation_modifier": 0.05}), coh(1)],
  n="Kohle aus dem Kusnezker Becken und Ekibastus (Kasachstan) für die Kraftwerke des Urals.")
F("the_unified_energy_system", "The Unified Energy System", "en", "kuzbass_and_ekibastuz,the_leningrad_station|the_great_siberian_dams", c=7, h=1, e=[
    build("energy", 1.0), dm("gp", {"energy_gain_multiplier": 0.05}), dm("cw", {"faction_trade_opinion_factor": 0.05})],
  n="Das Verbundnetz „Mir“ verbindet die Netze des RGW.")

# ============================================================== SCIENCE & SPACE
F("the_academy_of_sciences", "The Academy of Sciences", "sci", c=3, h=1, av="`COLDWAR_SOV_the_collective_leadership` erledigt", e=[
    dm("ps", {"research_speed_factor": 0.02}), pp(15)])
F("akademgorodok", "Akademgorodok", "sci", "the_academy_of_sciences", c=5, h=1, e=[
    build("off", 0.6), dm("ps", {"research_speed_factor": 0.02}), tech("CAT_computing", 1, 25)])
F("the_naukograds", "The Naukograds", "sci", "akademgorodok", c=7, h=1, e=[
    build("nucfac"), dm("ps", {"research_speed_factor": 0.02}), dm("af", {"equipment_cost_multiplier_modifier": -0.02})],
  n="Geschlossene Wissenschaftsstädte (Arsamas-16, Obninsk, Dubna).")
F("genetics_rehabilitated", "Genetics Rehabilitated", "sci", "the_academy_of_sciences", c=5, e=[
    tech("CAT_genetics", 1, 50), dm("gp", {"agricolture_productivity_modifier": 0.03})], n="Lyssenko ist seit 1965 entmachtet; die Biologie holt auf.")
F("scientific_exchange", "Scientific Exchange with the West", "sci", "akademgorodok", c=5, e=[
    dm("ps", {"research_speed_factor": 0.03, "drift_defence_factor": -0.05}), bop(-0.05)],
  n="IIASA in Laxenburg (1972), gemeinsame Kommissionen mit den USA.")
F("the_space_race_question", "The Space Race Question", "sci", "the_academy_of_sciences", c=3, h=1, e=[
    space(), txt("N1 oder Raumstationen – gegenseitig exklusiv")])
F("lunokhod", "Lunokhod", "sci", "the_space_race_question", c=5, h=1, e=[
    space(), stab(2), tech("CAT_satellites", 1, 50)], n="17.11.1970: das erste ferngesteuerte Fahrzeug auf dem Mond.")
F("venera", "Venera: The Road to Venus", "sci", "lunokhod", c=5, h=1, e=[
    space(), dm("ps", {"research_speed_factor": 0.01})], n="15.12.1970: Venera 7, erste Landung auf einem anderen Planeten.")
F("the_n1_moon_rocket", "Korolev's Dream: The N1", "sci", "the_space_race_question", mx="the_orbital_stations", c=7, e=[
    gdp(1.5), space(), tech("CAT_orbital_launch_vehicles", 1, 50)], n="Alt-Hist: Das Mondprogramm wird nach vier Fehlstarts nicht eingestellt.")
F("the_soviet_moonshot", "The Soviet Moonshot", "sci", "the_n1_moon_rocket", c=10, e=[
    gdp(2.5), space(), space(),
    idea("red_moon", "Red Moon", {"stability_factor": 0.05, "war_support_factor": 0.03, "research_speed_factor": 0.03}, days=1095),
    ev("moonshot", "Ein Kosmonaut auf dem Mond – Weltpresse, Jubel in Moskau"), tension(1),
])
F("the_orbital_stations", "The Orbital Stations", "sci", "the_space_race_question", mx="the_n1_moon_rocket", c=5, h=1, e=[
    space(), tech("CAT_satellites", 1, 50), dm("ps", {"research_speed_factor": 0.02})], n="Saljut 1 (April 1971).")
F("soyuz_apollo", "Soyuz-Apollo", "sci", "the_orbital_stations", av="Datum ≥ 01.01.1975", c=5, h=1, e=[
    offer("soyuz_apollo", "USA", "Gemeinsamer Flug (ASTP). Bei Annahme: beide +3 % Forschung für 2 Jahre, Spannung −1, Meinung +15"),
], n="Juli 1975.")
F("the_space_shuttle_answer", "Answer the Space Shuttle", "sci", "soyuz_apollo|the_soviet_moonshot", c=3, e=[
    txt("Gegenseitig exklusiv: Buran oder Mir")])
F("energia_buran", "Energia-Buran", "sci", "the_space_shuttle_answer", mx="mir_station", c=10, e=[
    gdp(3.0), sp("sp_space_program", 25), fac("defense_industry", 10), tech("CAT_orbital_launch_vehicles", 1, 50)])
F("mir_station", "Mir: The Permanent Station", "sci", "the_space_shuttle_answer", mx="energia_buran", c=7, e=[
    space(), dm("ps", {"research_speed_factor": 0.03}), stab(2)])
F("eyes_in_orbit", "Zenit: Eyes in Orbit", "sci", "the_orbital_stations|the_n1_moon_rocket", c=5, h=1, e=[
    tech("CAT_reconnaissance_satellites", 1, 50), dm("af", {"planning_speed": 0.05})])
F("the_scientific_superpower", "The Scientific Superpower", "sci", "the_naukograds,mir_station|energia_buran", c=7, e=[
    idea("scientific_superpower", "Scientific Superpower", {"research_speed_factor": 0.05}), stab(2)])
