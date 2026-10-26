# IMPERIA CW — Cold War: Cold War SOV design — d leaders.
from sov_dsl import *

P4 = inpower(4)
NAMES = {"bre": "Leonid Breschnew", "kos": "Alexei Kossygin", "pod": "Nikolai Podgorny", "sus": "Michail Suslow",
         "she": "Alexander Schelepin", "and": "Juri Andropow", "gre": "Andrei Gretschko", "ust": "Dmitri Ustinow",
         "gro": "Grigori Romanow", "che": "Konstantin Tschernenko", "gor": "Michail Gorbatschow"}


def A(k, extra=""):
    return f"{P4}; {NAMES[k]} ist Generalsekretär (`COLDWAR_SOV_gensec_{k}`)" + (f"; {extra}" if extra else "")


SHAKEUP = lambda: idea("plenum_shakeup", "Plenum Shake-up", {"stability_factor": -0.05, "political_power_factor": -0.10}, days=120)

# ================================================================== THE POLITBURO: changes of leadership (no exclusions)
F("ple_the_politburo", "The Politburo", "ple", av=P4, c=1, h=1, e=[
    pp(25), txt("Breschnew ist zum Start Generalsekretär (`COLDWAR_SOV_gensec_bre` aus dem Init). Die Politbüro-Fokusse unten schließen sich nicht aus: "
                "jeder baut eine Kandidatur auf; gewählt wird im Plenum, in dem auch die 3 Republiksitze abstimmen."),
], n="Muster wie die „Power to X“-Fokusse in Ägypten Rev. 7: jeder Wechsel einmal, nie gegenseitig gesperrt. Die KI wechselt nur über die historischen Todesfälle.")

PLENUM = [
    ("kos", "The Premier's Plenum", "Datum < 18.12.1980 (Tod Kossygins); Politbüro-Balance ≤ −0,15 ODER „Deepen the Kosygin Reform“/„OGAS: Cybernetic Planning“ erledigt; Branchenministerien ≥ 40; Stabilität ≥ 40 %",
     [fac("industrial_conglomerates", 10), fac("communist_cadres", -10), bop(-0.05)], [("economist_premier", "Economist-Premier")]),
    ("pod", "The Presidium Takes the Lead", "Datum < 12.01.1983; Stabilität ≥ 50 %; Zusammenhalt der Union ≥ 50",
     [coh(3), fac("communist_cadres", -5)], [("head_of_state", "Head of State")]),
    ("sus", "The Grey Cardinal Steps Forward", "Datum < 25.01.1982; Nomenklatura ≥ 60; Politbüro-Balance ≥ 0",
     [fac("communist_cadres", 5), bop(0.05)], [("chief_ideologue", "Chief Ideologue")]),
    ("she", "Iron Shurik's Return", "Datum < 16.04.1975 (danach nicht mehr im Politbüro); Gewerkschaften ≥ 55; KGB ≥ 50; Politbüro-Balance ≥ 0,25",
     [fac("labour_unions", 10), fac("communist_cadres", -15), bop(0.10)], [("iron_shurik", "Iron Shurik")]),
    ("and", "The Chekist Plenum", "Datum ≥ 27.04.1973 und < 09.02.1984; KGB ≥ 70",
     [fac("intelligence_community", 10), fac("communist_cadres", -5)], [("chekist", "Chekist")]),
    ("gre", "The Marshal's Hour", "Datum ≥ 27.04.1973 und < 26.04.1976; Armee ≥ 75; Cold-War-Spannung ≥ 55 ODER im Krieg ODER Politbüro-Balance ≥ 0,4",
     [fac("the_military", 15), fac("communist_cadres", -10), bop(0.10), ws(3)], [("marshal_of_the_soviet_union", "Marshal of the Soviet Union")]),
    ("ust", "The Armourer's Plenum", "Datum ≥ 05.03.1976 und < 20.12.1984; Rüstungskomplex ≥ 80; Armee ≥ 60",
     [fac("defense_industry", 15), fac("the_military", 5), bop(0.05)], [("the_armourer", "The Armourer")]),
    ("gro", "The Leningrad Plenum", "Datum ≥ 05.03.1976; Politbüro-Balance ≥ 0,15; Branchenministerien ≥ 50; Nomenklatura ≥ 50",
     [fac("industrial_conglomerates", 5), bop(0.10)], [("leningrad_boss", "Leningrad Boss")]),
    ("che", "The Apparatchik's Plenum", "Datum ≥ 27.11.1978 und < 10.03.1985; Nomenklatura ≥ 70",
     [fac("communist_cadres", 10), dm("gp", {"productivity_growth_modifier": -0.01})], [("apparatchik", "Apparatchik")]),
    ("gor", "The New Generation", "Datum ≥ 21.10.1980; Politbüro-Balance ≤ −0,2 ODER „Renew the Cadres“ erledigt",
     [fac("communist_cadres", -10), bop(-0.10)], [("new_generation", "The New Generation")]),
]
LEAN = {"kos": -1, "pod": 0, "sus": 1, "she": 1, "and": 0, "gre": 1, "ust": 1, "gro": 1, "che": 1, "gor": -1}
LEAN_TXT = {-1: "reformerisch", 0: "neutral", 1: "orthodox"}
for k, name, av, extra, traits in PLENUM:
    F(f"ple_{k}", name, "ple", "ple_the_politburo", av=f"{P4}; {NAMES[k]} ist nicht Generalsekretär; {av}", c=5,
      h=1 if k in ("and", "che", "gor") else 0,
      e=[dec(f"convene_plenum_{k}", f"„Convene the Plenum: {NAMES[k]}“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; "
                                    f"Bedingungen wie oben): Abstimmung im Politbüro, Richtung {LEAN_TXT[LEAN[k]]}, die 3 Republiksitze stimmen mit"),
         txt("Bei Mehrheit (verbindlich):"), gensec(k, NAMES[k], traits), stab(-5), SHAKEUP()] + extra +
        [txt("Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten")],
      n=("Historisch: " + {"and": "Andropow folgt Breschnew im November 1982.", "che": "Tschernenko folgt Andropow im Februar 1984.",
                           "gor": "Gorbatschow folgt Tschernenko im März 1985."}[k]) if k in ("and", "che", "gor") else
      "Alt-Hist. Die Kandidatur kann jederzeit aufgebaut werden, auch wenn ein anderer Generalsekretär seinen Baum halb fertig hat; "
      "entscheiden muss das Politbüro.")

# ================================================================== BREZHNEV
k = "bre"
F("bre_dear_leonid_ilyich", "Dear Leonid Ilyich", k, "ple_the_politburo", av=A(k), c=3, h=1, e=[
    pm(k, {"political_power_factor": 0.05, "stability_factor": 0.03}, name="Brezhnev's Course"), fac("communist_cadres", 5)])
F("bre_the_dnepropetrovsk_clan", "The Dnepropetrovsk Clan", k, "bre_dear_leonid_ilyich", av=A(k), c=5, h=1, e=[
    pm(k, {"political_power_factor": 0.03, "corruption_cost_factor": 0.05}), fac("communist_cadres", 5)],
  n="Kirilenko (Zweiter Sekretär), Schtscholokow (MWD), Tichonow (Ministerrat) – die Seilschaft aus Dnipropetrowsk.")
F("bre_the_general_department", "The General Department", k, "bre_dear_leonid_ilyich", av=A(k), c=5, h=1, e=[
    dm("ps", {"bureaucracy_cost_multiplier_modifier": -0.05}), pm(k, {"political_power_factor": 0.02})],
  n="Tschernenkos Allgemeine Abteilung: jedes Papier des Politbüros läuft über sie.")
F("bre_balance_the_troika", "Balance the Troika", k, "bre_dear_leonid_ilyich", av=A(k), c=5, h=1, e=[
    stab(2), custom("Politbüro-Balance 0,10 Richtung Mitte `add_power_balance_value`", ["add_power_balance_value"])])
F("bre_the_first_choice", "Detente or Doctrine?", k, "bre_the_dnepropetrovsk_clan,bre_balance_the_troika", av=A(k), c=3, h=1, e=[
    txt("Außenpolitische Weiche – gegenseitig exklusiv")])
F("bre_detente_from_strength", "Detente from Strength", k, "bre_the_first_choice", mx="bre_the_doctrine_hawk", av=A(k), c=5, h=1, e=[
    pm(k, {"trade_opinion_factor": 0.10}), tension(-1), bop(-0.05)])
F("bre_the_crimean_talks", "The Crimean Talks", k, "bre_detente_from_strength", av=A(k), c=5, h=1, e=[
    op("GER", 15, key="COLDWAR_SOV_detente"), dm("cw", {"trade_opinion_factor": 0.05})], n="Oreanda, September 1971: Breschnew und Brandt.")
F("bre_brezhnev_in_washington", "Brezhnev in Washington", k, "bre_the_crimean_talks", av=A(k, "Datum ≥ 01.06.1973"), c=5, h=1, e=[
    offer("brezhnev_visit", "USA", "Abkommen zur Verhütung von Atomkriegen. Bei Annahme: Spannung −2, Meinung +15"), stab(2)])
F("bre_the_helsinki_triumph", "The Helsinki Triumph", k, "bre_brezhnev_in_washington", av=A(k, "„The Helsinki Conference“ erledigt"), c=5, h=1, e=[
    stab(3), pm(k, {"political_power_factor": 0.03}), party(4, 3)], n="Die Grenzen von 1945 sind anerkannt – Breschnews größter Erfolg.")
F("bre_the_doctrine_hawk", "The Doctrine Hawk", k, "bre_the_first_choice", mx="bre_detente_from_strength", av=A(k), c=5, e=[
    pm(k, {"war_support_factor": 0.03, "mdcw_cw_ideological_defence": 0.10}), tension(2), bop(0.10), fac("the_military", 5)])
F("bre_the_iron_bloc", "The Iron Bloc", k, "bre_the_doctrine_hawk", av=A(k), c=5, e=[
    dm("cw", {"foreign_influence_modifier": 0.05}), dm("af", {"army_org_factor": 0.02})])
F("bre_answer_every_challenge", "Answer Every Challenge", k, "bre_the_iron_bloc", av=A(k), c=5, e=[
    dm("af", {"equipment_cost_multiplier_modifier": -0.03}), tension(1), fac("defense_industry", 5)])
F("bre_the_internationalist_duty", "The Internationalist Duty", k, "bre_answer_every_challenge", av=A(k), c=5, e=[
    dm("cw", {"mdcw_cw_support_effectiveness": 0.10, "send_volunteer_size": 1}), tension(1)])
F("bre_the_tula_speech", "The Tula Speech", k, "bre_the_helsinki_triumph|bre_the_internationalist_duty", av=A(k, "Datum ≥ 01.01.1977"), c=5, h=1, e=[
    tension(-2), fac("the_military", -5), stab(2)], n="Januar 1977: „Wir streben nicht nach Überlegenheit.“")
F("bre_the_second_choice", "Butter, Guns or Oil?", k, "bre_the_general_department", av=A(k), c=3, h=1, e=[txt("Wirtschaftsweiche – gegenseitig exklusiv")])
F("bre_consumer_socialism", "Consumer Socialism", k, "bre_the_second_choice", mx="bre_guns_before_butter,bre_the_oil_bet", av=A(k), c=5, h=1, e=[
    pm(k, {"consumer_goods_factor": -0.03, "stability_factor": 0.02}), dm("gp", {"social_cost_multiplier_modifier": 0.03})])
F("bre_the_little_deal", "The Little Deal", k, "bre_consumer_socialism", av=A(k), c=5, h=1, e=[
    idea("little_deal", "The Little Deal", {"stability_factor": 0.04, "tax_gain_multiplier_modifier": -0.02, "corruption_cost_factor": 0.05},
         swap="The Second Economy")], n="James Millars „kleiner Deal“: der Staat duldet Nebengeschäfte, die Bürger dulden den Staat.")
F("bre_a_flat_for_every_family", "A Flat for Every Family", k, "bre_the_little_deal", av=A(k), c=7, h=1, e=[
    build("inf", 0.6), stab(3), dm("gp", {"social_cost_multiplier_modifier": 0.02})])
F("bre_guns_before_butter", "Guns before Butter", k, "bre_the_second_choice", mx="bre_consumer_socialism,bre_the_oil_bet", av=A(k), c=5, e=[
    pm(k, {"military_industry_tax_modifier": 0.05, "consumer_goods_factor": 0.03}), fac("defense_industry", 10)])
F("bre_the_military_industrial_commission", "The Military-Industrial Commission", k, "bre_guns_before_butter", av=A(k), c=5, e=[
    build("mil2", 1.2), fac("defense_industry", 5)])
F("bre_the_tank_parks", "The Tank Parks", k, "bre_the_military_industrial_commission", av=A(k), c=5, e=[
    dm("af", {"equipment_cost_multiplier_modifier": -0.03}), tech("CAT_main_battle_tanks", 1, 50)])
F("bre_the_oil_bet", "The Oil Bet", k, "bre_the_second_choice", mx="bre_consumer_socialism,bre_guns_before_butter", av=A(k), c=5, e=[
    pm(k, {"oil_export_multiplier_modifier": 0.08}), dm("gp", {"productivity_growth_modifier": -0.02})])
F("bre_oil_for_grain", "Oil for Grain", k, "bre_the_oil_bet", av=A(k), c=5, e=[gdp_gain(0.5), dm("gp", {"agricolture_productivity_modifier": 0.02})])
F("bre_pipelines_to_europe", "Pipelines to Europe", k, "bre_oil_for_grain", av=A(k), c=5, e=[
    offer("pipelines_to_europe", ["GER", "ITA", "FRA"], "Langfristige Gaslieferverträge. Bei Annahme: Partner Energie +5 %, wir Öl-Exporterlöse +5 %, Meinung +10")])
F("bre_kgb_or_mvd", "Andropov or Shchelokov?", k, "bre_the_general_department", av=A(k), c=3, h=1, e=[txt("Wer hält die Ordnung? Gegenseitig exklusiv")])
F("bre_back_the_kgb", "Back the KGB", k, "bre_kgb_or_mvd", mx="bre_back_the_mvd", av=A(k), c=5, e=[
    fac("intelligence_community", 10), dm("ps", {"corruption_cost_factor": -0.05}), corr(-1)])
F("bre_back_the_mvd", "Back the MVD", k, "bre_kgb_or_mvd", mx="bre_back_the_kgb", av=A(k), c=5, h=1, e=[
    stab(2), dm("ps", {"police_cost_multiplier_modifier": -0.05, "corruption_cost_factor": 0.05})], n="Schtscholokows Miliz – loyal, bequem, korrupt.")
F("bre_trust_the_republics", "Trust in the Republican Cadres", k, "bre_back_the_kgb|bre_back_the_mvd", av=A(k), c=5, h=1, e=[
    coh(5), dm("ps", {"corruption_cost_factor": 0.03})])
F("bre_malaya_zemlya", "Malaya Zemlya", k, "bre_dear_leonid_ilyich", av=A(k, "Datum ≥ 01.01.1976"), c=5, h=1, e=[
    pm(k, {"political_power_factor": 0.05}), dm("ps", {"research_speed_factor": -0.01}), trait("four_times_hero", "Four Times Hero")],
  n="Memoiren, Orden, Marschallstab – der Personenkult der Spätzeit.")
F("bre_marshal_brezhnev", "Marshal Brezhnev", k, "bre_malaya_zemlya", av=A(k, "Datum ≥ 01.05.1976"), c=3, h=1, e=[fac("the_military", 5), pp(25)])
F("bre_chairman_of_the_presidium", "Chairman of the Presidium", k, "bre_marshal_brezhnev", av=A(k, "Datum ≥ 01.05.1977"), c=5, h=1, e=[
    pp(75), pm(k, {"political_power_factor": 0.03}), fac("communist_cadres", 5)], n="Juni 1977: Podgorny wird abgesetzt.")
F("bre_the_leaders_health", "The General Secretary's Health", k, "bre_chairman_of_the_presidium", av=A(k, "Datum ≥ 01.01.1978"), c=3, h=1, e=[
    txt("Gegenseitig exklusiv")])
F("bre_the_kremlin_doctors", "The Kremlin Doctors", k, "bre_the_leaders_health", mx="bre_a_dignified_retirement", av=A(k), c=5, h=1, e=[
    trait("ailing_leader", "Ailing Leader"), pm(k, {"political_power_factor": -0.05, "stability_factor": 0.02})],
  n="Jewgeni Tschasow und die 4. Hauptverwaltung halten ihn bis 1982 im Amt.")
F("bre_a_dignified_retirement", "A Dignified Retirement", k, "bre_the_leaders_health", mx="bre_the_kremlin_doctors", av=A(k), c=5, e=[
    stab(-3), pp(100), flag("bre_retiring", "Breschnew kündigt den Rücktritt an: der danach gewählte Erbe übernimmt sofort, ohne auf das Todes-Event zu warten (`COLDWAR_SOV_bre_retiring`)")],
  n="Breschnew bat 1979 tatsächlich darum, gehen zu dürfen.")
F("bre_the_succession", "The Succession", k, "bre_the_kremlin_doctors|bre_a_dignified_retirement", av=A(k), c=3, h=1, e=[
    txt("Wer folgt Breschnew? Gegenseitig exklusiv")])
for hk, nm, h_, e_ in [("andropov", "Heir: Andropov", 1, [corr(-1), fac("intelligence_community", 10)]),
                       ("chernenko", "Heir: Chernenko", 0, [stab(3), fac("communist_cadres", 10)]),
                       ("romanov", "Heir: Romanov", 0, [bop(0.10)]),
                       ("gorbachev", "Heir: An Early Gorbachev", 0, [bop(-0.15), fac("communist_cadres", -10)])]:
    others = ",".join(f"bre_heir_{x}" for x in ("andropov", "chernenko", "romanov", "gorbachev") if x != hk)
    F(f"bre_heir_{hk}", nm, k, "bre_the_succession", mx=others, av=A(k), c=5, h=h_,
      e=[heir({"andropov": "and", "chernenko": "che", "romanov": "gro", "gorbachev": "gor"}[hk], nm.split(": ")[1])] + e_)
F("bre_developed_socialism_achieved", "Developed Socialism Achieved", k,
  "bre_the_tula_speech,bre_a_flat_for_every_family|bre_the_tank_parks|bre_pipelines_to_europe,bre_trust_the_republics", av=A(k), c=7, h=1, e=[
      idea("developed_socialism", "Developed Socialism", {"stability_factor": 0.05, "political_power_factor": 0.05, "productivity_growth_modifier": -0.02}),
      pm(k, {"stability_factor": 0.02})], n="Abschluss: braucht Außen-, Wirtschafts- und Sicherheitsweiche.")

# ================================================================== KOSYGIN
k = "kos"
F("kos_the_premier_takes_the_party", "The Premier Takes the Party", k, "ple_kos", av=A(k), c=3, e=[
    pm(k, {"productivity_growth_modifier": 0.05, "research_speed_factor": 0.02, "political_power_factor": -0.03}, name="Kosygin's Reform Course")])
F("kos_baibakov_at_gosplan", "Baibakov at Gosplan", k, "kos_the_premier_takes_the_party", av=A(k), c=5, e=[
    dm("gp", {"production_factory_efficiency_gain_factor": 0.03}), fac("industrial_conglomerates", 5)])
F("kos_the_systems_men", "The Systems Men", k, "kos_the_premier_takes_the_party", av=A(k), c=5, e=[
    dm("ps", {"research_speed_factor": 0.02}), tech("CAT_computing", 1, 50), party(0, 2)], n="Dschermen Gwischiani und das Staatskomitee für Wissenschaft und Technik.")
F("kos_government_before_party", "Government before Party", k, "kos_the_premier_takes_the_party", av=A(k), c=5, e=[
    pm(k, {"bureaucracy_cost_multiplier_modifier": -0.05}), bop(-0.10), fac("communist_cadres", -5)])
F("kos_the_reform_model", "Which Reform?", k, "kos_baibakov_at_gosplan,kos_the_systems_men", av=A(k), c=3, e=[txt("Erste Weiche – drei Wege, gegenseitig exklusiv")])
F("kos_market_socialism", "Market Socialism", k, "kos_the_reform_model", mx="kos_cybernetic_communism,kos_reform_within_the_plan", av=A(k), c=5, e=[
    pm(k, {"productivity_growth_modifier": 0.05, "consumer_goods_factor": -0.03}), party(18, 3), bop(-0.10)])
F("kos_flexible_prices", "Flexible Prices", k, "kos_market_socialism", av=A(k), c=5, e=[
    stab(-4), dm("gp", {"consumer_goods_factor": -0.02, "tax_gain_multiplier_modifier": 0.03}), rmidea("second_economy", "The Second Economy")])
F("kos_the_enterprise_law", "The Law on the Socialist Enterprise", k, "kos_flexible_prices", av=A(k), c=5, e=[
    dm("gp", {"productivity_growth_modifier": 0.04}), fac("labour_unions", -5)])
F("kos_joint_ventures", "Joint Ventures with the West", k, "kos_the_enterprise_law", av=A(k), c=5, e=[
    dm("gp", {"trade_opinion_factor": 0.10, "receiving_investment_cost_modifier": -0.10}), debt(0.5)])
F("kos_cybernetic_communism", "Cybernetic Communism", k, "kos_the_reform_model", mx="kos_market_socialism,kos_reform_within_the_plan", av=A(k), c=5, e=[
    pm(k, {"production_factory_efficiency_gain_factor": 0.05, "production_factory_max_efficiency_factor": 0.03}), gdp(1.0)])
F("kos_the_ogas_grid", "The OGAS Grid", k, "kos_cybernetic_communism", av=A(k), c=7, e=[build("off2", 1.4), dm("gp", {"production_factory_efficiency_gain_factor": 0.05})])
F("kos_the_electronic_rouble", "The Electronic Rouble", k, "kos_the_ogas_grid", av=A(k), c=5, e=[
    corr(-1), rmidea("second_economy", "The Second Economy"), fac("communist_cadres", -5)], n="Gluschkows bargeldloser Plan.")
F("kos_the_planometric_institutes", "The Planometric Institutes", k, "kos_the_electronic_rouble", av=A(k), c=5, e=[
    dm("ps", {"research_speed_factor": 0.02}), dm("gp", {"productivity_growth_modifier": 0.03})], n="Zentrales Ökonomisch-Mathematisches Institut (CEMI).")
F("kos_reform_within_the_plan", "Reform within the Plan", k, "kos_the_reform_model", mx="kos_market_socialism,kos_cybernetic_communism", av=A(k), c=5, e=[
    pm(k, {"productivity_growth_modifier": 0.03, "stability_factor": 0.02}), fac("industrial_conglomerates", 5)],
  n="Kossygins eigener, vorsichtiger Weg: die Reform von 1965 retten, ohne das System anzutasten.")
F("kos_profit_and_bonus", "Plan, Profit, Bonus", k, "kos_reform_within_the_plan", av=A(k), c=5, e=[
    dm("gp", {"productivity_growth_modifier": 0.03, "civilian_industry_tax_modifier": 0.03})], n="Jewsei Libermans Prawda-Artikel von 1962.")
F("kos_the_production_associations", "Production Associations", k, "kos_profit_and_bonus", av=A(k), c=5, e=[
    dm("gp", {"production_factory_max_efficiency_factor": 0.03}), dm("ps", {"bureaucracy_cost_multiplier_modifier": -0.03})], n="Die Vereinigungen von 1973.")
F("kos_the_apparatus_resists", "The Apparatus Resists", k, "kos_joint_ventures|kos_the_planometric_institutes|kos_the_production_associations", av=A(k), c=3, e=[
    txt("Zweite Weiche: die Partei wehrt sich – gegenseitig exklusiv")])
F("kos_bring_the_party_along", "Bring the Party Along", k, "kos_the_apparatus_resists", mx="kos_break_the_apparatus", av=A(k), c=5, e=[
    pp(50), fac("communist_cadres", 10), dm("gp", {"productivity_growth_modifier": -0.01})])
F("kos_break_the_apparatus", "Break the Apparatus", k, "kos_the_apparatus_resists", mx="kos_bring_the_party_along", av=A(k), c=7, e=[
    fac("communist_cadres", -20), stab(-5), dm("gp", {"productivity_growth_modifier": 0.05}), rmidea("stability_of_cadres", "Stability of Cadres")])
F("kos_curb_the_military_budget", "Curb the Military Budget", k, "kos_government_before_party", av=A(k), c=5, e=[
    law("decrease_military_spending", "Verteidigungshaushalt −1 Stufe"), fac("the_military", -10), fac("defense_industry", -10), pm(k, {"consumer_goods_factor": -0.03})])
F("kos_conversion_of_defence_plants", "Conversion of Defence Plants", k, "kos_curb_the_military_budget", av=A(k), c=5, e=[
    build("civ", 0.8), dm("gp", {"consumer_goods_factor": -0.02}), fac("defense_industry", -5)])
F("kos_trade_not_tanks", "Trade, Not Tanks", k, "kos_government_before_party", av=A(k), c=5, e=[
    pm(k, {"trade_opinion_factor": 0.10}), tension(-1), op("FRA", 10, key="COLDWAR_SOV_detente")])
F("kos_the_glassboro_spirit", "The Glassboro Spirit", k, "kos_trade_not_tanks", av=A(k), c=5, e=[
    offer("kosygin_summit", "USA", "Gipfel mit dem Premier. Bei Annahme: Spannung −2, Handelsabkommen, Meinung +15")], n="Erinnerung an Glassboro 1967.")
F("kos_the_tashkent_mediator", "The Tashkent Mediator", k, "kos_trade_not_tanks", av=A(k), c=5, e=[
    infl(["RAJ", "PAK"], 3), op("RAJ", 10, key="COLDWAR_SOV_asian_security"), op("PAK", 10, key="COLDWAR_SOV_asian_security")],
  n="Kossygin vermittelte 1966 in Taschkent zwischen Indien und Pakistan.")
F("kos_not_a_single_soldier", "Not a Single Soldier", k, "kos_the_glassboro_spirit|kos_the_tashkent_mediator", av=A(k, "Datum ≥ 01.03.1979"), c=3, e=[
    stab(2), op("AFG", -10, key="COLDWAR_SOV_afghan_question")], n="März 1979: „Wir können das afghanische Volk nicht ersetzen.“")
F("kos_the_premiers_heart", "The Premier's Heart", k, "kos_bring_the_party_along|kos_break_the_apparatus", av=A(k, "Datum ≥ 01.10.1976"), c=3, e=[
    txt("Nachfolge – gegenseitig exklusiv (Kossygin stirbt historisch im Dezember 1980)")])
F("kos_heir_gorbachev", "Heir: Gorbachev's Generation", k, "kos_the_premiers_heart", mx="kos_heir_andropov,kos_rule_of_the_planners", av=A(k), c=5, e=[
    heir("gor", "Michail Gorbatschow"), bop(-0.10)])
F("kos_heir_andropov", "Heir: Andropov", k, "kos_the_premiers_heart", mx="kos_heir_gorbachev,kos_rule_of_the_planners", av=A(k), c=5, e=[
    heir("and", "Juri Andropow"), fac("intelligence_community", 5)])
F("kos_rule_of_the_planners", "Rule of the Planners", k, "kos_the_premiers_heart", mx="kos_heir_gorbachev,kos_heir_andropov", av=A(k), c=5, e=[
    rp(13, "Nikolai Baibakov", "Technokratie ohne Partei"), stab(-5)], n="Endet den KPdSU-Weg: Wechsel zu Partei 13 (Gosplan Technocracy).")
F("kos_socialism_that_works", "Socialism That Works", k, "kos_heir_gorbachev|kos_heir_andropov,kos_conversion_of_defence_plants,kos_not_a_single_soldier", av=A(k), c=7, e=[
    idea("reformed_economy", "Reformed Socialist Economy", {"productivity_growth_modifier": 0.05, "production_factory_max_efficiency_factor": 0.03}), stab(3)])

# ================================================================== PODGORNY
k = "pod"
F("pod_the_president_of_the_presidium", "The President of the Presidium", k, "ple_pod", av=A(k), c=3, e=[
    pm(k, {"stability_factor": 0.02, "political_power_factor": 0.03}, name="Podgorny's State"), coh(3)])
F("pod_the_supreme_soviet_awakens", "The Supreme Soviet Awakens", k, "pod_the_president_of_the_presidium", av=A(k), c=5, e=[
    pm(k, {"political_power_factor": 0.03}), fac("communist_cadres", -5), bop(-0.05)])
F("pod_the_kharkov_connection", "The Kharkov Connection", k, "pod_the_president_of_the_presidium", av=A(k), c=5, e=[coh(3), party(19, 2)],
  n="Podgornys ukrainische Basis (Charkiw, Kiew).")
F("pod_the_council_of_ministers_alliance", "An Alliance with the Ministers", k, "pod_the_president_of_the_presidium", av=A(k), c=5, e=[
    fac("industrial_conglomerates", 10), dm("gp", {"production_factory_efficiency_gain_factor": 0.02})])
F("pod_the_state_question", "Federation or Presidium?", k, "pod_the_supreme_soviet_awakens,pod_the_kharkov_connection", av=A(k), c=3, e=[
    txt("Erste Weiche – gegenseitig exklusiv")])
F("pod_a_federal_union", "A Federal Union", k, "pod_the_state_question", mx="pod_the_strong_presidium", av=A(k), c=5, e=[
    coh(10), pm(k, {"stability_factor": 0.03, "nationalist_drift": -0.02}), bop(-0.05)])
F("pod_republic_councils", "Republic Councils of Ministers", k, "pod_a_federal_union", av=A(k), c=5, e=[coh(4), dm("ps", {"bureaucracy_cost_multiplier_modifier": 0.03})])
F("pod_republican_accounting", "Republican Cost Accounting", k, "pod_republic_councils", av=A(k), c=5, e=[
    coh(3), dm("gp", {"productivity_growth_modifier": 0.02})], n="Die Republiken wirtschaften auf eigene Rechnung.")
F("pod_the_soviet_of_nationalities", "The Soviet of Nationalities", k, "pod_republican_accounting", av=A(k), c=5, e=[coh(5), dm("un", {"drift_defence_factor": 0.05})])
F("pod_the_strong_presidium", "The Strong Presidium", k, "pod_the_state_question", mx="pod_a_federal_union", av=A(k), c=5, e=[
    pm(k, {"political_power_factor": 0.05, "bureaucracy_cost_multiplier_modifier": -0.05}), fac("communist_cadres", -10), coh(-2)])
F("pod_ministers_answer_to_the_state", "Ministers Answer to the State", k, "pod_the_strong_presidium", av=A(k), c=5, e=[
    dm("gp", {"production_factory_efficiency_gain_factor": 0.03}), fac("industrial_conglomerates", 5)])
F("pod_presidential_decrees", "Presidential Decrees", k, "pod_ministers_answer_to_the_state", av=A(k), c=5, e=[pp(75), stab(2)])
F("pod_the_state_security_council", "The State Security Council", k, "pod_presidential_decrees", av=A(k), c=5, e=[
    fac("intelligence_community", 5), dm("ps", {"drift_defence_factor": 0.05})])
F("pod_head_of_state_diplomacy", "Head-of-State Diplomacy", k, "pod_the_council_of_ministers_alliance", av=A(k), c=5, e=[
    infl(["EGY", "SYR", "SOM", "ETH", "AGL", "MOZ"], 3), op("EGY", 10, key="COLDWAR_SOV_third_world")], n="Podgornys Afrikareise 1977.")
F("pod_the_treaty_signer", "The Treaty Signer", k, "pod_head_of_state_diplomacy", av=A(k), c=5, e=[
    dm("cw", {"mdcw_cw_support_effectiveness": 0.05}), txt("Freundschaftsverträge (Ägypten, Irak, Indien) kosten 25 PP weniger Zeit: −30 % Fokuszeit für diese Fokusse")],
  n="Podgorny unterschrieb im Mai 1971 den Vertrag mit Ägypten.")
F("pod_ukrainian_breadbasket", "The Ukrainian Breadbasket", k, "pod_the_kharkov_connection", av=A(k), c=5, e=[
    dm("gp", {"agricolture_productivity_modifier": 0.04}), coh(2)])
F("pod_donbass_coal", "Donbass Coal", k, "pod_ukrainian_breadbasket", av=A(k), c=5, e=[build("energy", 0.8), fac("labour_unions", 5)])
F("pod_the_final_form", "The Final Form of the State", k, "pod_the_soviet_of_nationalities|pod_the_state_security_council,pod_donbass_coal", av=A(k), c=3, e=[
    txt("Zweite Weiche – gegenseitig exklusiv")])
F("pod_union_of_sovereign_states", "A Union of Sovereign States", k, "pod_the_final_form", mx="pod_the_soviet_presidency", av=A(k), c=7, e=[
    rp(19, "Pyotr Shelest", "Nationalkommunistische Union"), coh(10), stab(-5)], n="Endet den KPdSU-Weg: Wechsel zu Partei 19.")
F("pod_the_soviet_presidency", "The Soviet Presidency", k, "pod_the_final_form", mx="pod_union_of_sovereign_states", av=A(k), c=5, e=[
    pm(k, {"political_power_factor": 0.05, "stability_factor": 0.02}), trait("president_of_the_ussr", "President of the USSR")])
F("pod_the_soviet_state", "The Soviet State", k, "pod_the_soviet_presidency,pod_the_treaty_signer", av=A(k), c=7, e=[
    idea("soviet_state", "The Soviet State", {"stability_factor": 0.04, "political_power_factor": 0.05, "bureaucracy_cost_multiplier_modifier": -0.05}), coh(5)])

# ================================================================== SUSLOV (hardliner – ideology)
k = "sus"
F("sus_the_grey_cardinal_rules", "The Grey Cardinal Rules", k, "ple_sus", av=A(k), c=3, e=[
    pm(k, {"mdcw_cw_ideological_defence": 0.15, "drift_defence_factor": 0.10, "research_speed_factor": -0.02, "political_power_factor": 0.05},
       name="Suslov's Orthodoxy")])
F("sus_the_ideological_commission", "The Ideological Commission", k, "sus_the_grey_cardinal_rules", av=A(k), c=5, e=[party(4, 3), fac("communist_cadres", 5)])
F("sus_ponomarevs_department", "Ponomarev's Department", k, "sus_the_grey_cardinal_rules", av=A(k), c=5, e=[
    dm("cw", {"mdcw_cw_support_effectiveness": 0.05}), infl(["CUB", "VIE", "MON"], 2)], n="Boris Ponomarjow und die Internationale Abteilung des ZK.")
F("sus_trapeznikovs_science_department", "Trapeznikov's Science Department", k, "sus_the_grey_cardinal_rules", av=A(k), c=5, e=[
    party(6, 2), dm("ps", {"research_speed_factor": -0.01, "drift_defence_factor": 0.05})])
F("sus_the_line", "The Correct Line", k, "sus_the_ideological_commission,sus_trapeznikovs_science_department", av=A(k), c=3, e=[txt("Erste Weiche – gegenseitig exklusiv")])
F("sus_ideological_purity", "Ideological Purity", k, "sus_the_line", mx="sus_militant_internationalism", av=A(k), c=5, e=[
    bop(0.15), stab(3),
    idea("silenced_dissent", "Silenced Dissent", {"stability_factor": 0.03, "drift_defence_factor": 0.10, "research_speed_factor": -0.02,
                                                  "trade_opinion_factor": -0.05}, swap="Samizdat and Dissent")])
F("sus_rewrite_the_history", "Rewrite the History", k, "sus_ideological_purity", av=A(k), c=5, e=[party(6, 3), pm(k, {"stability_factor": 0.02}), bop(0.05)],
  n="Stalin als „Organisator des Sieges“ – die schleichende Rehabilitierung.")
F("sus_the_glavlit_offensive", "The Glavlit Offensive", k, "sus_rewrite_the_history", av=A(k), c=5, e=[
    dm("ps", {"foreign_subversive_activites": -0.10, "research_speed_factor": -0.01}), stab(2)])
F("sus_the_closed_society", "The Closed Society", k, "sus_the_glavlit_offensive", av=A(k), c=5, e=[
    pm(k, {"drift_defence_factor": 0.10, "trade_opinion_factor": -0.05})])
F("sus_militant_internationalism", "Militant Internationalism", k, "sus_the_line", mx="sus_ideological_purity", av=A(k), c=5, e=[
    pm(k, {"mdcw_cw_support_effectiveness": 0.15, "foreign_influence_modifier": 0.10, "tax_gain_multiplier_modifier": -0.02}), tension(2)])
F("sus_the_liberation_movements", "The Liberation Movements", k, "sus_militant_internationalism", av=A(k), c=5, e=[
    infl(["AGL", "MOZ", "ETH", "YEM", "SYE"], 3), dm("cw", {"mdcw_cw_military_programme_cost": -0.10})])
F("sus_against_eurocommunism", "Against Eurocommunism", k, "sus_the_liberation_movements", av=A(k, "Datum ≥ 01.01.1975"), c=5, e=[
    dm("cw", {"opinion_gain_monthly_same_ideology_factor": 0.05}), op("ITA", -10, key="COLDWAR_SOV_eurocommunism"), op("FRA", -5, key="COLDWAR_SOV_eurocommunism")],
  n="Berliner Konferenz 1976: Berlinguer, Marchais und Carrillo gehen eigene Wege.")
F("sus_the_world_conference", "The World Conference", k, "sus_against_eurocommunism", av=A(k), c=5, e=[
    dm("cw", {"mdcw_cw_support_effectiveness": 0.05}), pp(50)], n="Wie die Moskauer Konferenz von 1969 – mit Moskau als Zentrum.")
F("sus_moral_incentives", "Moral Incentives", k, "sus_the_ideological_commission", av=A(k), c=5, e=[
    dm("gp", {"production_factory_efficiency_gain_factor": 0.02, "productivity_growth_modifier": -0.01}), stab(2)],
  n="Ehrentafeln und Wanderfahnen statt Prämien.")
F("sus_against_the_market", "Against the Market", k, "sus_moral_incentives", av=A(k), c=5, e=[
    fac("communist_cadres", 5), dm("gp", {"productivity_growth_modifier": -0.02}), rmidea("cooperative_sector", "Cooperative Sector"), bop(0.05)])
F("sus_the_drawing_together_of_nations", "The Drawing Together of Nations", k, "sus_marxism_leninism_in_every_school", av=A(k), c=5, e=[
    coh(3), dm("un", {"nationalist_drift": -0.01})], n="„Sblischenije“ – die Annäherung der Nationen zum Sowjetvolk.")
F("sus_marxism_leninism_in_every_school", "Marxism-Leninism in Every School", k, "sus_ponomarevs_department", av=A(k), c=5, e=[
    pm(k, {"communism_drift": 0.03}), dm("gp", {"education_cost_multiplier_modifier": 0.03})])
F("sus_no_gods_in_the_kremlin", "No Gods in the Kremlin", k, "sus_the_drawing_together_of_nations", av=A(k), c=5, e=[
    dm("ps", {"drift_defence_factor": 0.05}), party(14, -3), party(23, -2), stab(-1)])
F("sus_the_polemic_with_beijing", "The Polemic with Beijing", k, "sus_the_closed_society|sus_the_world_conference", av=A(k), c=5, e=[
    dm("ps", {"drift_defence_factor": 0.05}), dm("cw", {"mdcw_cw_support_effectiveness": 0.05}), op("CHI", -10, key="COLDWAR_SOV_sino_split")])
F("sus_the_heir_question", "The Ideologue's Heir", k, "sus_the_polemic_with_beijing,sus_against_the_market", av=A(k, "Datum ≥ 01.01.1978"), c=3, e=[
    txt("Nachfolge – gegenseitig exklusiv (Suslow stirbt historisch im Januar 1982)")])
F("sus_heir_chernenko", "Heir: Chernenko", k, "sus_the_heir_question", mx="sus_heir_romanov,sus_the_iron_line_inherits", av=A(k), c=5, e=[
    heir("che", "Konstantin Tschernenko"), stab(2)])
F("sus_heir_romanov", "Heir: Romanov", k, "sus_the_heir_question", mx="sus_heir_chernenko,sus_the_iron_line_inherits", av=A(k), c=5, e=[
    heir("gro", "Grigori Romanow"), bop(0.05)])
F("sus_the_iron_line_inherits", "The Iron Line Inherits", k, "sus_the_heir_question", mx="sus_heir_chernenko,sus_heir_romanov", av=A(k), c=5, e=[
    rp(6, "Sergei Trapeznikov", "Neostalinistische Plattform übernimmt"), bop(0.15)], n="Endet den KPdSU-Weg: Wechsel zu Partei 6.")
F("sus_the_orthodox_union", "The Orthodox Union", k, "sus_heir_chernenko|sus_heir_romanov,sus_no_gods_in_the_kremlin", av=A(k), c=7, e=[
    idea("orthodox_union", "The Orthodox Union", {"drift_defence_factor": 0.15, "stability_factor": 0.04, "research_speed_factor": -0.02})])

# ================================================================== SHELEPIN (hardliner – order)
k = "she"
F("she_iron_shurik", "Iron Shurik", k, "ple_she", av=A(k), c=3, e=[
    pm(k, {"stability_factor": 0.05, "political_power_factor": 0.05, "drift_defence_factor": 0.10, "corruption_cost_factor": -0.10}, name="Shelepin's Order")])
F("she_the_komsomoltsy", "The Komsomoltsy", k, "she_iron_shurik", av=A(k), c=5, e=[party(7, 3), fac("communist_cadres", -5)],
  n="Jegorytschew, Mesjazew, Tikunow – Schelepins Netzwerk aus Komsomol und KGB.")
F("she_semichastny_returns", "Semichastny Returns", k, "she_iron_shurik", av=A(k), c=5, e=[
    fac("intelligence_community", 10), dm("ps", {"foreign_subversive_activites": -0.10})], n="Wladimir Semitschastny, KGB-Chef bis 1967.")
F("she_the_trade_union_base", "The Trade Union Base", k, "she_iron_shurik", av=A(k), c=5, e=[fac("labour_unions", 10), stab(2)],
  n="Schelepin führte seit 1967 den Gewerkschaftsbund VTsSPS.")
F("she_the_labour_question", "The Labour Question", k, "she_the_komsomoltsy,she_the_trade_union_base", av=A(k), c=3, e=[txt("Erste Weiche – gegenseitig exklusiv")])
F("she_labour_discipline", "Labour Discipline", k, "she_the_labour_question", mx="she_workers_socialism", av=A(k), c=5, e=[
    pm(k, {"productivity_growth_modifier": 0.05}), stab(-2), fac("labour_unions", -10)])
F("she_the_absenteeism_raids", "The Absenteeism Raids", k, "she_labour_discipline", av=A(k), c=5, e=[
    dm("gp", {"productivity_growth_modifier": 0.03}), dm("ps", {"police_cost_multiplier_modifier": 0.05})])
F("she_the_war_on_drunkenness", "The War on Drunkenness", k, "she_the_absenteeism_raids", av=A(k), c=5, e=[
    dm("gp", {"productivity_growth_modifier": 0.02, "tax_gain_multiplier_modifier": -0.02}), stab(-2)])
F("she_workers_socialism", "Workers' Socialism", k, "she_the_labour_question", mx="she_labour_discipline", av=A(k), c=5, e=[
    pm(k, {"consumer_goods_factor": -0.02, "stability_factor": 0.03}), fac("labour_unions", 15), party(5, 2)])
F("she_the_union_councils", "The Union Councils", k, "she_workers_socialism", av=A(k), c=5, e=[dm("gp", {"social_cost_multiplier_modifier": 0.03}), stab(2)])
F("she_the_workers_control", "Workers' Control Commissions", k, "she_the_union_councils", av=A(k), c=5, e=[corr(-1), fac("industrial_conglomerates", -10)])
F("she_order_in_the_streets", "Order in the Streets", k, "she_semichastny_returns", av=A(k), c=5, e=[
    law("increase_policing_budget", "Polizeibudget +1 Stufe"), stab(3)])
F("she_the_war_on_corruption", "The War on Corruption", k, "she_order_in_the_streets", av=A(k), c=5, e=[corr(-1), fac("communist_cadres", -10)])
F("she_purge_the_brezhnevites", "Purge the Brezhnevites", k, "she_the_war_on_corruption,she_the_war_on_drunkenness|she_the_workers_control", av=A(k), c=7, e=[
    fac("communist_cadres", -15), corr(-1), stab(-3), bop(0.05), rmidea("stability_of_cadres", "Stability of Cadres")])
F("she_youth_brigades", "Youth Brigades", k, "she_the_komsomoltsy", av=A(k), c=5, e=[dm("gp", {"production_speed_buildings_factor": 0.05}), manpower(15000)])
F("she_the_komsomol_economy", "The Komsomol Economy", k, "she_youth_brigades", av=A(k), c=5, e=[build("inf", 0.6), dm("gp", {"production_speed_infrastructure_factor": 0.10})])
F("she_the_foreign_line", "East or West?", k, "she_the_komsomol_economy", av=A(k), c=3, e=[txt("Gegenseitig exklusiv")])
F("she_talk_to_beijing", "Talk to Beijing", k, "she_the_foreign_line", mx="she_confront_the_west", av=A(k), c=5, e=[
    offer("shelepin_china", "CHI", "Gespräche zwischen zwei Lagern der „reinen Linie“. Bei Annahme: Meinung +20, Spannung an der Grenze sinkt (Ussuri-Geist mildert sich)")],
  n="Schelepin galt in Peking als Mann, mit dem man reden könne.")
F("she_confront_the_west", "Confront the West", k, "she_the_foreign_line", mx="she_talk_to_beijing", av=A(k), c=5, e=[tension(2), ws(3), dm("af", {"army_morale_factor": 0.03})])
F("she_the_final_question", "The Shape of Power", k, "she_purge_the_brezhnevites,she_talk_to_beijing|she_confront_the_west", av=A(k), c=3, e=[
    txt("Zweite Weiche – gegenseitig exklusiv")])
F("she_the_leader_state", "The Leader State", k, "she_the_final_question", mx="she_collective_discipline", av=A(k), c=7, e=[
    rp(7, "Alexander Shelepin", "Schelepin bleibt Staatschef"), trait("vozhd", "Vozhd"), bop(0.15)],
  n="Endet den KPdSU-Weg: Wechsel zu Partei 7 (Komsomol Vanguard) – deren Baum öffnet sich.")
F("she_collective_discipline", "Collective Discipline", k, "she_the_final_question", mx="she_the_leader_state", av=A(k), c=5, e=[
    stab(5), pm(k, {"political_power_factor": 0.03}), heir("and", "Juri Andropow", "Schelepins Disziplin geht an den KGB über")])
F("she_the_iron_order", "The Iron Order", k, "she_collective_discipline", av=A(k), c=7, e=[
    idea("iron_order", "The Iron Order", {"stability_factor": 0.05, "productivity_growth_modifier": 0.03, "research_speed_factor": -0.02})])

# ================================================================== ANDROPOV
k = "and"
F("and_the_chekist_takes_power", "The Chekist Takes Power", k, "ple_and", av=A(k), c=3, h=1, e=[
    pm(k, {"corruption_cost_factor": -0.10, "drift_defence_factor": 0.10, "productivity_growth_modifier": 0.03, "political_power_factor": 0.03},
       name="Andropov's Course")])
F("and_kgb_men_in_the_kremlin", "KGB Men in the Kremlin", k, "and_the_chekist_takes_power", av=A(k), c=5, h=1, e=[
    fac("intelligence_community", 10), dm("ps", {"intel_network_gain_factor": 0.05})], n="Tschebrikow, Krjutschkow, Alijew.")
F("and_the_young_reformers", "The Young Reformers", k, "and_the_chekist_takes_power", av=A(k), c=5, h=1, e=[
    bop(-0.05), dm("ps", {"research_speed_factor": 0.02})], n="Gorbatschow, Ryschkow, Ligatschow – Andropows Team.")
F("and_lessons_of_budapest", "Lessons of Budapest", k, "and_the_chekist_takes_power", av=A(k), c=5, e=[
    dm("gp", {"consumer_goods_factor": -0.02}), op("HUN", 10, key="COLDWAR_SOV_economic_partners")], n="Botschafter in Budapest 1956.")
F("and_the_discipline_campaign", "The Discipline Campaign", k, "and_kgb_men_in_the_kremlin", av=A(k), c=5, h=1, e=[
    pm(k, {"productivity_growth_modifier": 0.04}), stab(-2)], n="Razzien in Kinos und Badehäusern während der Arbeitszeit.")
F("and_the_road", "Order or Reform?", k, "and_the_discipline_campaign,and_the_young_reformers", av=A(k), c=3, h=1, e=[txt("Erste Weiche – gegenseitig exklusiv")])
F("and_order_and_reform", "Order and Reform", k, "and_the_road", mx="and_the_chekist_state", av=A(k), c=5, h=1, e=[pm(k, {"productivity_growth_modifier": 0.05}), bop(-0.10)])
F("and_the_large_scale_experiment", "The Large-Scale Economic Experiment", k, "and_order_and_reform", av=A(k), c=5, h=1, e=[
    dm("gp", {"productivity_growth_modifier": 0.03, "production_factory_efficiency_gain_factor": 0.03})], n="1983/84 in fünf Ministerien.")
F("and_the_economic_department", "Ryzhkov's Economic Department", k, "and_the_large_scale_experiment", av=A(k), c=5, e=[
    dm("gp", {"production_factory_max_efficiency_factor": 0.03}), dm("ps", {"bureaucracy_cost_multiplier_modifier": -0.03})])
F("and_the_technology_gap", "The Technology Gap", k, "and_the_economic_department", av=A(k), c=5, e=[
    tech(["CAT_computing", "CAT_microchips"], 1, 50), dm("ps", {"research_speed_factor": 0.02})])
F("and_the_chekist_state", "The Chekist State", k, "and_the_road", mx="and_order_and_reform", av=A(k), c=5, e=[
    pm(k, {"mdcw_cw_ideological_defence": 0.15, "intel_network_gain_factor": 0.10, "stability_factor": 0.03, "research_speed_factor": -0.02}),
    bop(0.10), fac("intelligence_community", 10)])
F("and_gorky_for_sakharov", "Gorky for Sakharov", k, "and_the_chekist_state", av=A(k), c=5, e=[
    party(2, -5), dm("ps", {"drift_defence_factor": 0.05}), op("USA", -10, key="COLDWAR_SOV_human_rights")])
F("and_the_kgb_economy", "The KGB Economy", k, "and_gorky_for_sakharov", av=A(k), c=5, e=[corr(-1), dm("ps", {"corruption_cost_factor": -0.05}), fac("communist_cadres", -10)])
F("and_the_informant_society", "The Informant Society", k, "and_the_kgb_economy", av=A(k), c=5, e=[
    dm("ps", {"foreign_subversive_activites": -0.15}), stab(-1), dm("ps", {"research_speed_factor": -0.01})])
F("and_the_cotton_affair_exposed", "The Cotton Affair Exposed", k, "and_lessons_of_budapest", av=A(k), c=5, h=1, e=[corr(-1), coh(-3), fac("communist_cadres", -5)])
F("and_the_shchelokov_purge", "The Shchelokov Purge", k, "and_the_cotton_affair_exposed", av=A(k), c=5, h=1, e=[
    corr(-1), dm("ps", {"police_cost_multiplier_modifier": -0.05}), fac("communist_cadres", -5)], n="Dezember 1982: Schtscholokow wird abgesetzt, die Miliz gesäubert.")
F("and_a_way_out_of_afghanistan", "A Way Out", k, "and_the_shchelokov_purge", av=A(k), c=5, e=[
    txt("Wenn „The Afghan Burden“ aktiv ist: Rückzugsplan (Event an AFG); sonst Spannung −1"), tension(-1), stab(2)])
F("and_talks_with_beijing", "Talks with Beijing", k, "and_a_way_out_of_afghanistan", av=A(k), c=5, e=[
    offer("andropov_china", "CHI", "Wiederaufnahme der Konsultationen (1982). Bei Annahme: Meinung +15, Spannung −1")])
F("and_the_succession", "Andropov's Kidneys", k, "and_the_technology_gap|and_the_informant_society,and_talks_with_beijing", av=A(k), c=3, h=1, e=[
    txt("Nachfolge – gegenseitig exklusiv (Andropow stirbt historisch im Februar 1984)")])
F("and_heir_gorbachev", "Heir: Mikhail Gorbachev", k, "and_the_succession", mx="and_heir_chernenko,and_heir_aliyev", av=A(k), c=5, e=[
    heir("gor", "Michail Gorbatschow"), bop(-0.05)], n="Andropows Protegé aus Stawropol.")
F("and_heir_chernenko", "Heir: Chernenko", k, "and_the_succession", mx="and_heir_gorbachev,and_heir_aliyev", av=A(k), c=5, h=1, e=[
    heir("che", "Konstantin Tschernenko"), stab(2)], n="Historisch: die Alten setzen Tschernenko durch.")
F("and_heir_aliyev", "Heir: The Chekist from Baku", k, "and_the_succession", mx="and_heir_gorbachev,and_heir_chernenko", av=A(k), c=5, e=[
    leader("Heydar Aliyev", 4, "chekist_from_baku", "Chekist from Baku", "beim Tod Andropows; kein eigener Baum, Andropows Programm bleibt"),
    coh(6), fac("intelligence_community", 5)], n="Heydar Alijew, KGB-General, seit 1982 Erster Vizepremier.")
F("and_the_disciplined_union", "The Disciplined Union", k, "and_heir_gorbachev|and_heir_chernenko|and_heir_aliyev", av=A(k), c=7, e=[
    idea("disciplined_union", "The Disciplined Union", {"productivity_growth_modifier": 0.04, "corruption_cost_factor": -0.10, "stability_factor": 0.02})])

# ================================================================== GRECHKO (general)
k = "gre"
F("gre_the_marshals_hour", "The Marshal's Hour", k, "ple_gre", av=A(k), c=3, e=[
    pm(k, {"army_org_factor": 0.03, "war_support_factor": 0.03, "political_power_factor": 0.03, "consumer_goods_factor": 0.02},
       name="The Marshal's Party"), fac("the_military", 10)],
  n="Realistisch: kein Putsch, sondern der Verteidigungsminister an der Spitze der Partei – die Armee bekommt die Stimme, die sie 1957 (Schukow) verlor.")
F("gre_the_general_staff_in_the_politburo", "The General Staff in the Politburo", k, "gre_the_marshals_hour", av=A(k), c=5, e=[
    cp(50), dm("af", {"planning_speed": 0.05})], n="Kulikow, später Ogarkow.")
F("gre_yepishevs_political_directorate", "Yepishev's Political Directorate", k, "gre_the_marshals_hour", av=A(k), c=5, e=[
    dm("af", {"army_morale_factor": 0.04}), fac("communist_cadres", 5)], n="Die Politoffiziere unter Armeegeneral Jepischew.")
F("gre_the_defence_council", "The Defence Council", k, "gre_the_marshals_hour", av=A(k), c=5, e=[
    pp(50), pm(k, {"political_power_factor": 0.02})], n="Der Verteidigungsrat der UdSSR wird zum eigentlichen Machtzentrum.")
F("gre_the_doctrine", "Mass Army or Nuclear Shield?", k, "gre_the_general_staff_in_the_politburo,gre_yepishevs_political_directorate", av=A(k), c=3, e=[
    txt("Erste Weiche – gegenseitig exklusiv")])
F("gre_the_mass_army", "The Mass Army", k, "gre_the_doctrine", mx="gre_the_nuclear_shield", av=A(k), c=5, e=[
    pm(k, {"conscription_factor": 0.05, "army_defence_factor": 0.02}), manpower(50000)], n="Gretschkos Vorliebe: Panzerarmeen und Reserven.")
F("gre_the_tank_armies_of_the_west", "The Tank Armies of the West", k, "gre_the_mass_army", av=A(k), c=5, e=[
    dm("af", {"breakthrough_factor": 0.03}), tech("CAT_main_battle_tanks", 1, 50)], n="Die Gruppe der Sowjetischen Streitkräfte in Deutschland.")
F("gre_mobilisation_reserves", "Mobilisation Reserves", k, "gre_the_tank_armies_of_the_west", av=A(k), c=5, e=[
    dm("af", {"mobilization_speed": 0.10}), dm("gp", {"consumer_goods_factor": 0.01})])
F("gre_the_nuclear_shield", "The Nuclear Shield", k, "gre_the_doctrine", mx="gre_the_mass_army", av=A(k), c=5, e=[
    tech("CAT_intercontinental_ballistic_missiles", 1, 75), pm(k, {"enemy_justify_war_goal_time": 0.10})])
F("gre_the_strategic_triad", "The Strategic Triad", k, "gre_the_nuclear_shield", av=A(k), c=5, e=[
    tech(["CAT_missile_submarines", "CAT_heavy_aircraft"], 1, 50), tension(1)])
F("gre_against_salt", "Against SALT", k, "gre_the_strategic_triad", av=A(k), c=5, e=[tension(2), fac("the_military", 5), fac("defense_industry", 5)])
F("gre_the_far_eastern_command", "The Far Eastern Command", k, "gre_the_defence_council", av=A(k), c=5, e=[
    dm("af", {"army_core_defence_factor": 0.05}), build("air")], n="Ab 1979 als eigenes Oberkommando.")
F("gre_suvorov_schools", "Suvorov and Nakhimov Schools", k, "gre_the_far_eastern_command", av=A(k), c=5, e=[
    dm("af", {"training_time_factor": -0.05}), law("increase_officer_training_level", "Offiziersausbildung +1 Stufe")])
F("gre_the_school_of_the_nation", "The Army as the School of the Nation", k, "gre_suvorov_schools", av=A(k), c=5, e=[
    coh(4), dm("un", {"drift_defence_factor": 0.03})], n="Russisch als Kommandosprache, Völkerfreundschaft in der Kaserne.")
F("gre_arms_for_allies", "Arms for Allies", k, "gre_the_defence_council", av=A(k), c=5, e=[
    dm("af", {"international_market_income_modifier": 0.10}), dm("cw", {"mdcw_cw_military_programme_cost": -0.10})])
F("gre_the_military_advisers", "The Military Advisers", k, "gre_arms_for_allies", av=A(k), c=5, e=[
    offer("gre_advisers", ["EGY", "SYR", "IRQ"], "Militärberater und Ausbildung. Bei Annahme: Partner +5 % Organisation, Meinung +15")])
F("gre_the_heir_of_the_marshal", "After the Marshal", k, "gre_mobilisation_reserves|gre_against_salt,gre_the_school_of_the_nation,gre_the_military_advisers",
  av=A(k, "Datum ≥ 01.01.1975"), c=3, e=[txt("Gretschko stirbt historisch im April 1976 – zweite Weiche, gegenseitig exklusiv")])
F("gre_heir_ustinov", "Heir: Ustinov", k, "gre_the_heir_of_the_marshal", mx="gre_return_to_civilian_rule,gre_the_council_of_marshals", av=A(k), c=5, e=[
    heir("ust", "Dmitri Ustinow"), fac("defense_industry", 5)], n="Historisch wurde Ustinow 1976 Gretschkos Nachfolger als Minister.")
F("gre_return_to_civilian_rule", "Return to Civilian Rule", k, "gre_the_heir_of_the_marshal", mx="gre_heir_ustinov,gre_the_council_of_marshals", av=A(k), c=5, e=[
    heir("che", "Konstantin Tschernenko"), stab(3), fac("communist_cadres", 10)])
F("gre_the_council_of_marshals", "The Council of Marshals", k, "gre_the_heir_of_the_marshal", mx="gre_heir_ustinov,gre_return_to_civilian_rule", av=A(k), c=7, e=[
    rp(22, "Andrei Grechko", "Militärregierung"), stab(-5)], n="Endet den KPdSU-Weg: Wechsel zu Partei 22 (Council of Marshals).")
F("gre_the_garrison_party", "The Garrison Party", k, "gre_heir_ustinov|gre_return_to_civilian_rule", av=A(k), c=7, e=[
    idea("garrison_party", "The Garrison Party", {"army_org_factor": 0.03, "army_defence_factor": 0.02, "war_support_factor": 0.03, "consumer_goods_factor": 0.02})])

# ================================================================== USTINOV (general – defence industry)
k = "ust"
F("ust_the_armourer", "The Armourer", k, "ple_ust", av=A(k), c=3, e=[
    pm(k, {"equipment_cost_multiplier_modifier": -0.05, "military_industry_tax_modifier": 0.05, "research_speed_factor": 0.02, "consumer_goods_factor": 0.02},
       name="The Armourer's Course"), fac("defense_industry", 10)], n="Volkskommissar für Rüstung schon 1941, Marschall ab 1976.")
F("ust_the_military_industrial_commission", "Smirnov's Commission", k, "ust_the_armourer", av=A(k), c=5, e=[
    dm("gp", {"production_speed_arms_factory_factor": 0.10}), fac("defense_industry", 5)], n="Leonid Smirnow und die VPK beim Ministerrat.")
F("ust_the_design_bureaus", "The Design Bureaus", k, "ust_the_armourer", av=A(k), c=5, e=[
    build("airfac"), dm("ps", {"research_speed_factor": 0.02})], n="Tupolew, Suchoi, Mikojan, Tschelomei, Jangel.")
F("ust_the_nine_ministries", "The Nine Ministries", k, "ust_the_armourer", av=A(k), c=5, e=[
    dm("af", {"equipment_cost_multiplier_modifier": -0.03}), dm("ps", {"bureaucracy_cost_multiplier_modifier": 0.03})])
F("ust_quality_or_quantity", "Quality or Quantity?", k, "ust_the_military_industrial_commission,ust_the_design_bureaus", av=A(k), c=3, e=[
    txt("Erste Weiche – gegenseitig exklusiv")])
F("ust_quality", "Quality", k, "ust_quality_or_quantity", mx="ust_quantity", av=A(k), c=5, e=[
    pm(k, {"research_speed_factor": 0.03}), dm("af", {"equipment_cost_multiplier_modifier": 0.03})])
F("ust_the_fourth_generation", "The Fourth Generation", k, "ust_quality", av=A(k), c=7, e=[tech("CAT_medium_aircraft", 2, 50), sp("sp_aircraft_project", 15)])
F("ust_t80_and_the_gas_turbine", "T-80 and the Gas Turbine", k, "ust_the_fourth_generation", av=A(k), c=5, e=[tech(["CAT_main_battle_tanks", "CAT_tank_engines"], 1, 50)])
F("ust_quantity", "Quantity", k, "ust_quality_or_quantity", mx="ust_quality", av=A(k), c=5, e=[
    build("mil2", 1.2), dm("af", {"equipment_cost_multiplier_modifier": -0.04})])
F("ust_standardise_the_arsenal", "Standardise the Arsenal", k, "ust_quantity", av=A(k), c=5, e=[
    dm("af", {"line_change_production_efficiency_factor": 0.10}), dm("gp", {"production_factory_efficiency_gain_factor": 0.02})])
F("ust_the_stockpiles", "The Stockpiles", k, "ust_standardise_the_arsenal", av=A(k), c=5, e=[build("fuel"), dm("af", {"supply_consumption_factor": -0.02})])
F("ust_the_rocket_men", "The Rocket Men", k, "ust_the_nine_ministries", av=A(k), c=5, e=[
    tech(["CAT_intercontinental_ballistic_missiles", "CAT_orbital_launch_vehicles"], 1, 50)], n="Gluschko, Tschelomei, Utkin.")
F("ust_ss20_deployment", "SS-20 Deployment", k, "ust_the_rocket_men", av=A(k), c=5, e=[
    tech("CAT_intermediate_range_ballistic_missiles", 1, 75), tension(2), op("GER", -10, key="COLDWAR_SOV_euromissiles")])
F("ust_energia_buran", "Energia-Buran", k, "ust_ss20_deployment", av=A(k), c=7, e=[gdp(2.0), sp("sp_space_program", 20), fac("defense_industry", 5)])
F("ust_the_closed_cities", "The Closed Cities", k, "ust_the_design_bureaus", av=A(k), c=5, e=[build("nucfac"), dm("af", {"equipment_cost_multiplier_modifier": -0.02})])
F("ust_dual_use_lines", "Dual-Use Lines", k, "ust_the_closed_cities", av=A(k), c=5, e=[dm("gp", {"consumer_goods_factor": -0.02}), build("civ", 0.8)],
  n="Die Rüstungsministerien liefern Kühlschränke und Fernseher – das Einzige, was die Konsumenten von ihnen sehen.")
F("ust_the_foreign_line", "The Afghan Question", k, "ust_dual_use_lines,ust_energia_buran", av=A(k), c=3, e=[txt("Gegenseitig exklusiv")])
F("ust_the_hawk", "The Hawk of Kabul", k, "ust_the_foreign_line", mx="ust_arms_not_soldiers", av=A(k), c=5, e=[
    dm("af", {"experience_gain_army": 0.02}), tension(2), fac("the_military", 5)], n="Ustinow drängte im Dezember 1979 auf die Intervention.")
F("ust_arms_not_soldiers", "Arms, Not Soldiers", k, "ust_the_foreign_line", mx="ust_the_hawk", av=A(k), c=5, e=[
    dm("af", {"international_market_income_modifier": 0.10}), stab(2)])
F("ust_the_heir", "The Armourer's Heir", k, "ust_the_hawk|ust_arms_not_soldiers,ust_t80_and_the_gas_turbine|ust_the_stockpiles", av=A(k), c=3, e=[
    txt("Nachfolge – gegenseitig exklusiv (Ustinow stirbt historisch im Dezember 1984)")])
F("ust_heir_romanov", "Heir: Romanov", k, "ust_the_heir", mx="ust_heir_gorbachev", av=A(k), c=5, e=[heir("gro", "Grigori Romanow"), fac("defense_industry", 5)])
F("ust_heir_gorbachev", "Heir: Gorbachev", k, "ust_the_heir", mx="ust_heir_romanov", av=A(k), c=5, e=[heir("gor", "Michail Gorbatschow"), bop(-0.05)])
F("ust_the_arsenal_of_socialism", "The Arsenal of Socialism", k, "ust_heir_romanov|ust_heir_gorbachev", av=A(k), c=7, e=[
    idea("arsenal_of_socialism", "The Arsenal of Socialism", {"equipment_cost_multiplier_modifier": -0.05, "production_speed_arms_factory_factor": 0.10,
                                                              "consumer_goods_factor": 0.02})])

# ================================================================== ROMANOV (hardliner – technocrat)
k = "gro"
F("gro_the_leningrad_order", "The Leningrad Order", k, "ple_gro", av=A(k), c=3, e=[
    pm(k, {"industrial_capacity_factory": 0.03, "drift_defence_factor": 0.05, "corruption_cost_factor": -0.05, "stability_factor": 0.02},
       name="The Leningrad Order")])
F("gro_the_leningrad_cadres", "The Leningrad Cadres", k, "gro_the_leningrad_order", av=A(k), c=5, e=[fac("communist_cadres", -5), pm(k, {"political_power_factor": 0.03})])
F("gro_the_kirov_works", "The Kirov Works", k, "gro_the_leningrad_order", av=A(k), c=5, e=[build("mil", 1.0), fac("defense_industry", 5)],
  n="Kirow-Werk, LOMO, Admiralitätswerft – Leningrads Rüstungsgürtel.")
F("gro_science_production_associations", "Science-Production Associations", k, "gro_the_leningrad_order", av=A(k), c=5, e=[
    dm("ps", {"research_speed_factor": 0.03}), dm("gp", {"production_factory_max_efficiency_factor": 0.02})], n="Das Leningrader Modell der NPOs.")
F("gro_the_path", "Technocracy or Iron Discipline?", k, "gro_the_leningrad_cadres,gro_science_production_associations", av=A(k), c=3, e=[
    txt("Erste Weiche – gegenseitig exklusiv")])
F("gro_hardline_technocracy", "Hardline Technocracy", k, "gro_the_path", mx="gro_iron_discipline", av=A(k), c=5, e=[
    pm(k, {"productivity_growth_modifier": 0.04, "research_speed_factor": 0.02}), bop(0.05)])
F("gro_the_intensive_economy", "The Intensive Economy", k, "gro_hardline_technocracy", av=A(k), c=5, e=[dm("gp", {"productivity_growth_modifier": 0.03})])
F("gro_automated_plants", "Automated Plants", k, "gro_the_intensive_economy", av=A(k), c=5, e=[tech("CAT_robotics", 1, 50), build("chip", 1.0)])
F("gro_iron_discipline", "Iron Discipline", k, "gro_the_path", mx="gro_hardline_technocracy", av=A(k), c=5, e=[
    pm(k, {"stability_factor": 0.04, "drift_defence_factor": 0.10}), bop(0.10), fac("intelligence_community", 5)])
F("gro_no_rock_no_jeans", "No Rock, No Jeans", k, "gro_iron_discipline", av=A(k), c=5, e=[
    dm("ps", {"foreign_subversive_activites": -0.10}), stab(-1), party(2, -2)], n="Romanows Leningrad war berüchtigt für seine Härte gegen die Subkultur.")
F("gro_the_purge_of_the_lazy", "The Purge of the Lazy", k, "gro_no_rock_no_jeans", av=A(k), c=5, e=[corr(-1), fac("communist_cadres", -10), dm("gp", {"productivity_growth_modifier": 0.02})])
F("gro_the_naval_capital", "The Naval Capital", k, "gro_the_kirov_works", av=A(k), c=5, e=[build("dock", 1.0), dm("af", {"navy_org_factor": 0.03})])
F("gro_no_concessions", "No Concessions", k, "gro_the_naval_capital", av=A(k), c=5, e=[tension(2), fac("the_military", 5), dm("cw", {"trade_opinion_factor": -0.05})])
F("gro_the_baltic_fortress", "The Baltic Fortress", k, "gro_no_concessions", av=A(k), c=5, e=[
    dm("af", {"army_core_defence_factor": 0.03}), coh(-2), dm("un", {"drift_defence_factor": 0.03})])
F("gro_the_heir", "Romanov's Line", k, "gro_automated_plants|gro_the_purge_of_the_lazy,gro_the_baltic_fortress", av=A(k), c=3, e=[txt("Zweite Weiche – gegenseitig exklusiv")])
F("gro_the_strong_hand", "The Strong Hand", k, "gro_the_heir", mx="gro_the_technocrats_succession", av=A(k), c=5, e=[
    pm(k, {"political_power_factor": 0.05, "stability_factor": 0.02}), trait("strong_hand", "Strong Hand")])
F("gro_the_technocrats_succession", "The Technocrats' Succession", k, "gro_the_heir", mx="gro_the_strong_hand", av=A(k), c=5, e=[
    heir("ust", "Dmitri Ustinow"), dm("gp", {"production_factory_efficiency_gain_factor": 0.02})])
F("gro_the_ordered_union", "The Ordered Union", k, "gro_the_strong_hand|gro_the_technocrats_succession", av=A(k), c=7, e=[
    idea("ordered_union", "The Ordered Union", {"productivity_growth_modifier": 0.04, "stability_factor": 0.03, "drift_defence_factor": 0.05})])

# ================================================================== CHERNENKO
k = "che"
F("che_the_apparatchik", "The Apparatchik", k, "ple_che", av=A(k), c=3, h=1, e=[
    pm(k, {"political_power_factor": 0.05, "bureaucracy_cost_multiplier_modifier": 0.05, "stability_factor": 0.03, "productivity_growth_modifier": -0.03},
       name="Chernenko's Continuity")])
F("che_the_general_department", "The General Department", k, "che_the_apparatchik", av=A(k), c=5, h=1, e=[dm("ps", {"bureaucracy_cost_multiplier_modifier": -0.05}), pp(50)])
F("che_letters_from_the_people", "Letters from the People", k, "che_the_apparatchik", av=A(k), c=5, h=1, e=[stab(3), dm("ps", {"political_power_factor": 0.02})],
  n="Tschernenkos Abteilung für Bürgerbriefe – das Ohr des Apparats.")
F("che_the_path", "Continuity or Opening?", k, "che_the_general_department,che_letters_from_the_people", av=A(k), c=3, h=1, e=[txt("Erste Weiche – gegenseitig exklusiv")])
F("che_continuity", "Continuity", k, "che_the_path", mx="che_a_cautious_opening", av=A(k), c=5, h=1, e=[pm(k, {"stability_factor": 0.03}), fac("communist_cadres", 10)])
F("che_the_ideology_plenum", "The Ideology Plenum", k, "che_continuity", av=A(k), c=5, h=1, e=[dm("ps", {"drift_defence_factor": 0.05}), party(4, 2)], n="Juni 1983.")
F("che_a_cautious_opening", "A Cautious Opening", k, "che_the_path", mx="che_continuity", av=A(k), c=5, e=[pm(k, {"productivity_growth_modifier": 0.03}), bop(-0.05)])
F("che_the_school_reform", "The School Reform", k, "che_a_cautious_opening", av=A(k), c=5, h=1, e=[
    dm("gp", {"education_cost_multiplier_modifier": 0.03, "total_workforce_modifier": 0.02})], n="1984: Berufsbildung in allen Schulen.")
F("che_the_food_programme_continued", "The Food Programme Continued", k, "che_the_ideology_plenum|che_the_school_reform", av=A(k), c=5, h=1, e=[
    dm("gp", {"agricolture_productivity_modifier": 0.03})])
F("che_the_foreign_line", "Talk or Boycott?", k, "che_the_food_programme_continued", av=A(k), c=3, e=[txt("Gegenseitig exklusiv")])
F("che_the_peace_offensive", "The Peace Offensive", k, "che_the_foreign_line", mx="che_the_olympic_boycott", av=A(k), c=5, e=[
    offer("chernenko_talks", "USA", "Neue Abrüstungsgespräche in Genf. Bei Annahme: Spannung −2")])
F("che_the_olympic_boycott", "The Olympic Boycott", k, "che_the_foreign_line", mx="che_the_peace_offensive", av=A(k), c=5, h=1, e=[
    op("USA", -15, key="COLDWAR_SOV_olympic_boycott"), stab(2), tension(1)], n="Los Angeles 1984.")
F("che_the_emphysema", "The Emphysema", k, "che_the_peace_offensive|che_the_olympic_boycott", av=A(k), c=3, h=1, e=[
    txt("Nachfolge – gegenseitig exklusiv (Tschernenko stirbt historisch im März 1985)")])
F("che_heir_gorbachev", "Heir: Gorbachev", k, "che_the_emphysema", mx="che_heir_grishin,che_heir_romanov", av=A(k), c=5, h=1, e=[heir("gor", "Michail Gorbatschow")])
F("che_heir_grishin", "Heir: Grishin", k, "che_the_emphysema", mx="che_heir_gorbachev,che_heir_romanov", av=A(k), c=5, e=[
    leader("Viktor Grishin", 4, "moscow_boss", "Moscow Boss", "beim Tod Tschernenkos; Tschernenkos Programm bleibt"), fac("communist_cadres", 10)],
  n="Moskaus Parteichef seit 1967 – der Kandidat der Alten.")
F("che_heir_romanov", "Heir: Romanov", k, "che_the_emphysema", mx="che_heir_gorbachev,che_heir_grishin", av=A(k), c=5, e=[heir("gro", "Grigori Romanow")])
F("che_the_last_of_the_old_guard", "The Last of the Old Guard", k, "che_heir_gorbachev|che_heir_grishin|che_heir_romanov", av=A(k), c=5, e=[
    idea("old_guard", "The Old Guard", {"stability_factor": 0.04, "political_power_factor": 0.04, "productivity_growth_modifier": -0.02})])

# ================================================================== GORBACHEV
k = "gor"
F("gor_the_new_generation", "The New Generation", k, "ple_gor", av=A(k), c=3, h=1, e=[
    pm(k, {"research_speed_factor": 0.03, "productivity_growth_modifier": 0.03, "democratic_drift": 0.01, "stability_factor": -0.02},
       name="Perestroika")])
F("gor_ryzhkov_and_ligachev", "Ryzhkov and Ligachev", k, "gor_the_new_generation", av=A(k), c=5, h=1, e=[
    dm("gp", {"production_factory_efficiency_gain_factor": 0.02}), corr(-1)])
F("gor_yakovlev_returns", "Yakovlev Returns from Ottawa", k, "gor_the_new_generation", av=A(k), c=5, h=1, e=[party(18, 3), bop(-0.05)])
F("gor_shevardnadze_at_the_foreign_ministry", "Shevardnadze at the Foreign Ministry", k, "gor_the_new_generation", av=A(k), c=5, h=1, e=[
    tension(-1), coh(2)])
F("gor_the_path", "Acceleration or Glasnost?", k, "gor_ryzhkov_and_ligachev,gor_yakovlev_returns", av=A(k), c=3, h=1, e=[txt("Erste Weiche – gegenseitig exklusiv")])
F("gor_uskorenie", "Uskorenie", k, "gor_the_path", mx="gor_glasnost_first", av=A(k), c=5, h=1, e=[
    pm(k, {"productivity_growth_modifier": 0.04}), gdp(1.0), tech("CAT_production_lines", 1, 50)], n="1985/86: Beschleunigung durch Maschinenbau.")
F("gor_the_anti_alcohol_campaign", "The Anti-Alcohol Campaign", k, "gor_uskorenie", av=A(k), c=5, h=1, e=[
    dm("gp", {"tax_gain_multiplier_modifier": -0.05, "productivity_growth_modifier": 0.02}), stab(-3)], n="Mai 1985: der Staatshaushalt verliert die Wodkaeinnahmen.")
F("gor_the_state_enterprise_law", "The State Enterprise Law", k, "gor_the_anti_alcohol_campaign", av=A(k), c=5, h=1, e=[
    dm("gp", {"productivity_growth_modifier": 0.04}), fac("industrial_conglomerates", -10)])
F("gor_glasnost_first", "Glasnost First", k, "gor_the_path", mx="gor_uskorenie", av=A(k), c=5, e=[
    pm(k, {"research_speed_factor": 0.03, "drift_defence_factor": -0.10}), stab(-2)])
F("gor_the_blank_spots", "The Blank Spots of History", k, "gor_glasnost_first", av=A(k), c=5, e=[stab(-2), party(3, 3), party(2, 2)])
F("gor_release_sakharov", "Release Sakharov", k, "gor_the_blank_spots", av=A(k), c=5, e=[
    rmidea("dissent", "Samizdat and Dissent"), op("USA", 15, key="COLDWAR_SOV_human_rights"), party(2, 3)], n="Dezember 1986: der Anruf in Gorki.")
F("gor_the_cooperative_law", "The Cooperative Law", k, "gor_the_state_enterprise_law|gor_release_sakharov", av=A(k), c=5, h=1, e=[
    idea("cooperative_sector", "Cooperative Sector", {"tax_gain_multiplier_modifier": 0.03, "consumer_goods_factor": -0.03, "corruption_cost_factor": 0.05},
         swap="The Second Economy")])
F("gor_new_thinking", "New Thinking", k, "gor_shevardnadze_at_the_foreign_ministry", av=A(k), c=5, h=1, e=[tension(-3), dm("cw", {"trade_opinion_factor": 0.05})])
F("gor_the_zero_option", "The Zero Option", k, "gor_new_thinking", av=A(k), c=5, h=1, e=[
    offer("inf_treaty", "USA", "Abbau aller Mittelstreckenraketen (INF). Bei Annahme: Spannung −4, beide Kosten Verteidigungshaushalt −5 %"),
    fac("the_military", -10)])
F("gor_leave_afghanistan", "Leave Afghanistan", k, "gor_the_zero_option", av=A(k), c=5, h=1, e=[
    txt("Beendet „The Afghan Burden“ mit Rückzugsplan (Event an AFG)"), stab(3), fac("the_military", -5)])
F("gor_the_sinatra_doctrine", "The Sinatra Doctrine", k, "gor_leave_afghanistan", av=A(k), c=5, h=1, e=[
    tension(-3), rmidea("brezhnev_doctrine", "The Brezhnev Doctrine"), dm("cw", {"tax_gain_multiplier_modifier": 0.03}), coh(-3)])
F("gor_democratisation", "Demokratizatsiya", k, "gor_the_cooperative_law", av=A(k), c=5, h=1, e=[
    stab(-3), bop(-0.10), fac("communist_cadres", -15)])
F("gor_the_congress_of_peoples_deputies", "The Congress of People's Deputies", k, "gor_democratisation", av=A(k), c=7, h=1, e=[
    elections(True, "Halbfreie Wahlen erlaubt `set_politics`"), party(4, -5), stab(-3)])
F("gor_the_union_treaty", "The New Union Treaty", k, "gor_the_congress_of_peoples_deputies,gor_the_sinatra_doctrine", av=A(k), c=7, h=1, e=[
    coh(12), dm("ps", {"political_power_factor": -0.05})])
F("gor_how_far", "How Far?", k, "gor_the_union_treaty", av=A(k), c=3, h=1, e=[txt("Zweite Weiche – gegenseitig exklusiv")])
F("gor_humane_democratic_socialism", "Humane, Democratic Socialism", k, "gor_how_far", mx="gor_the_social_democratic_turn,gor_the_presidency", av=A(k), c=5, e=[
    stab(3), pm(k, {"stability_factor": 0.03})], n="Die Programmerklärung von 1990 – innerhalb der KPdSU.")
F("gor_the_social_democratic_turn", "The Social-Democratic Turn", k, "gor_how_far", mx="gor_humane_democratic_socialism,gor_the_presidency", av=A(k), c=7, e=[
    rp(3, "Mikhail Gorbachev", "Gorbatschow führt die Sozialdemokraten"), stab(-3)], n="Endet den KPdSU-Weg: Wechsel zu Partei 3.")
F("gor_the_presidency", "The Presidency of the USSR", k, "gor_how_far", mx="gor_humane_democratic_socialism,gor_the_social_democratic_turn", av=A(k), c=5, h=1, e=[
    trait("president_of_the_ussr", "President of the USSR"), pp(100), rmidea("stability_of_cadres", "Stability of Cadres")], n="März 1990.")
F("gor_the_common_european_home", "The Common European Home", k, "gor_humane_democratic_socialism|gor_the_presidency", av=A(k), c=7, e=[
    idea("common_european_home", "The Common European Home", {"trade_opinion_factor": 0.15, "research_speed_factor": 0.03, "stability_factor": 0.02})])
