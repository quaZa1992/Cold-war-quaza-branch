# IMPERIA CW — Cold War: Cold War SOV design — d concept.
from sov_dsl import *

# ------------------------------------------------------------------ starting national spirits (init effect)
START_SPIRITS = [
    ("stability_of_cadres", "Stability of Cadres",
     {"political_power_factor": 0.10, "stability_factor": 0.05, "bureaucracy_cost_multiplier_modifier": 0.15,
      "productivity_growth_modifier": -0.05, "corruption_cost_factor": 0.10},
     "Breschnews Versprechen von 1964: niemand verliert seinen Posten. Bequem und starr.",
     "„The Gerontocracy Question“ (Trunk): „Renew the Cadres“ entfernt ihn, „Respect for Seniority“ macht daraus „Era of Stagnation“. "
     "Kossygins Team („Government Before Party“), Schelepins Säuberung, Gorbatschows Präsidentschaft und einige Parteibäume entfernen ihn ebenfalls."),
    ("burden_of_parity", "The Burden of Parity",
     {"production_speed_arms_factory_factor": 0.10, "military_factories_productivity": 0.05, "consumer_goods_factor": 0.05,
      "civilian_industry_tax_modifier": -0.05, "military_spending_cost_factor": 0.10},
     "Gleichstand mit den USA – um den Preis von 12–15 % des Sozialprodukts.",
     "SALT I (angenommen) halbiert die Nachteile; „Superiority, Not Parity“ verschärft ihn zum „Arms Race“; Parteien mit Abrüstung entfernen ihn."),
    ("agrarian_problem", "The Agrarian Problem",
     {"agricolture_productivity_modifier": -0.15, "agriculture_workers_modifier": 0.10, "consumer_goods_factor": 0.02, "stability_factor": -0.02},
     "Kolchosen, Transportverluste, Missernten – jedes fünfte Jahr fehlt Getreide.",
     "Wird erst mit „The Food Programme“ (Landwirtschaft) entfernt."),
    ("ussuri_frontier", "The Ussuri Frontier",
     {"war_support_factor": 0.05, "army_personnel_cost_multiplier_modifier": 0.10, "stability_factor": -0.02},
     "Nach Damanski und Tielieketi stehen sich 1,5 Mio. Soldaten am Amur gegenüber.",
     "Grenzgespräche (angenommen) mildern ihn; „The Trans-Baikal Buildup“ macht daraus „The Eastern Fortress“; Versöhnung oder Damanski-Regelung entfernen ihn."),
    ("shadow_of_prague", "The Shadow of Prague",
     {"trade_opinion_factor": -0.15, "research_speed_factor": -0.03, "drift_defence_factor": 0.10, "foreign_influence_defense_modifier": 0.10},
     "August 1968 – der Westen misstraut, die Intelligenz schweigt.",
     "Moskauer Vertrag (angenommen) entfernt die Handelsstrafe; Helsinki oder „Let Them Go Their Way“ entfernen ihn ganz."),
    ("second_economy", "The Second Economy",
     {"tax_gain_multiplier_modifier": -0.05, "corruption_cost_factor": 0.10, "consumer_goods_factor": -0.02, "stability_factor": 0.02},
     "Blat, Tolkatschi, Schwarzmarkt – die Schattenwirtschaft hält die Läden halb voll.",
     "Je nach Weg: legalisiert (Kooperativen, „The Little Deal“, „Shadow Capitalism“) oder zerschlagen (Preisreform, elektronischer Rubel)."),
    ("dissent", "Samizdat and Dissent",
     {"democratic_drift": 0.02, "nationalist_drift": 0.01, "stability_factor": -0.02},
     "Chronik der laufenden Ereignisse (seit 1968), Sacharow, Solschenizyn, die Refuseniks.",
     "„The Dissident Question“ (KGB) entscheidet: Psychiatrie, Ausweisung oder Duldung."),
]
for k, n, m, _, _ in START_SPIRITS:
    IDEAS[PFX + k] = dict(name=n, mods=m, days=None, start=True)

ALREADY_THERE = [
    ("Warsaw_Pact_member", "Warschauer Pakt (MD) – bleibt"),
    ("mdcw_cw_bloc_modifier_soviet", "Soviet Bloc (Cold War Equilibrium, Blockführer) – bleibt"),
    ("Imperia National Ideas", "Bleiben frei wählbar; „Border Regime and Exit Controls“ passt zum Start"),
]

START_LAWS = [("bureau_04", "Bürokratie hoch"), ("defence_07", "Verteidigung sehr hoch"), ("police_04", "Polizei hoch"),
              ("edu_04", "Bildung hoch"), ("health_03", "Gesundheit mittel"), ("social_04", "Soziales hoch"),
              ("draft_army", "Wehrpflichtarmee"), ("intervention_global_interventionism", "Globale Intervention"),
              ("officer_military_academy", "Militärakademien"), ("md_closed_economy", "Geschlossene Wirtschaft"),
              ("comprehensive_regulations", "Umfassende Regulierung"), ("fully_nationalized_healthcare", "Staatliches Gesundheitswesen"),
              ("economic_motivated_mining", "Bergbau ohne Umweltrücksicht"), ("censored_nation_05", "Zensur (Glawlit)")]

START_FACTIONS = [("communist_cadres", "Nomenklatura", 75), ("the_military", "Armee & Generalstab", 70),
                  ("intelligence_community", "KGB", 70), ("defense_industry", "Rüstungskomplex (VPK)", 80),
                  ("industrial_conglomerates", "Branchenministerien", 60), ("farmers", "Kolchosbauern", 45),
                  ("labour_unions", "Gewerkschaften (VTsSPS)", 55)]

DYNMODS = [
    ("party_state", "Der Parteistaat", "Politik", "PP-Gewinn, Stabilität, Bürokratie-/Polizeikosten, Driftabwehr, ideologische Abwehr (Cold War), "
     "Abwehr fremden Einflusses, Korruptionskosten, Forschung", "alle 0"),
    ("gosplan", "Gosplan – Planwirtschaft", "Wirtschaft", "Bau, Effizienzzuwachs, Max. Effizienz, Produktivitätswachstum, Konsumgüter, Zivil-/Rüstungssteuer, "
     "Steuereinnahmen, Agrarproduktivität, Fabrikleistung, Öl-/Rohstoffexporte, Energie, Sozial-/Gesundheitskosten, Handelsmeinung", "alle 0"),
    ("armed_forces", "Streitkräfte der UdSSR", "Militär", "Angriff, Verteidigung, Organisation, Moral, Ausbildung, Planung, Personal-/Ausrüstungskosten, "
     "Rekrutierung, Durchbruch, Marine-Reichweite, Luftverteidigung", "Personalkosten Heer +5 % (Großarmee)"),
    ("union", "Union der Republiken", "Staat", "Stabilität, nationalistische Drift, Driftabwehr – plus die Stufe des Zusammenhalts (siehe unten)",
     "Zusammenhalt 62 → Stufe „Fraternal Republics“"),
    ("commonwealth", "Sozialistische Gemeinschaft", "Außen", "Kosten des Imperiums: Steuereinnahmen, Öl-Exporterlöse (Vorzugspreise RGW), "
     "Auslandseinfluss, Meinungsgewinn gleicher Ideologie, Unterstützungskampagnen (Cold War), Hilfsprogramm-Kapazität, Forschungsteilung",
     "Steuern −3 %, Öl-Exporterlöse −10 %, Kampagnen +10 %, Meinungsgewinn +10 %, Einfluss +5 %"),
]

BOP = dict(
    id="COLDWAR_SOV_politburo_bop", initial=0.15, left="Reformer & Technokraten", right="Orthodoxe & Silowiki",
    ranges=[
        ("−1,0 bis −0,7", "Revisionist Crisis", "Forschung +6 %, Produktivitätswachstum +8 %, Stabilität −10 %, demokratische Drift +0,05",
         "Beim Eintritt: Event „Die Orthodoxen verschwören sich“ (Putschgefahr, Wahl: Zugeständnis oder Säuberung)"),
        ("−0,7 bis −0,4", "Reform Ascendancy", "Forschung +5 %, Produktivitätswachstum +6 %, Handelsmeinung +10 %, Stabilität −3 %, Driftabwehr −15 %", ""),
        ("−0,4 bis −0,15", "Reform Current", "Forschung +3 %, Produktivitätswachstum +3 %, Driftabwehr −5 %", ""),
        ("−0,15 bis +0,15", "Collective Leadership", "Stabilität +2 %, PP-Gewinn +3 %", "Die Mitte ist der sichere Ort – aber ohne Dynamik"),
        ("+0,15 bis +0,4", "Orthodox Course", "Stabilität +3 %, Driftabwehr +10 %, Forschung −2 %", "Startbereich (0,15)"),
        ("+0,4 bis +0,7", "Neo-Stalinist Tide", "Stabilität +5 %, PP +5 %, Driftabwehr +20 %, Polizeikosten +10 %, Forschung −5 %, Produktivitätswachstum −5 %", ""),
        ("+0,7 bis +1,0", "Reaction", "Driftabwehr +25 %, Kriegsunterstützung +5 %, Forschung −8 %, Produktivitätswachstum −8 %, Stabilität −5 %",
         "Beim Eintritt: Event „Die Reformer rufen die Armee“ (Wahl: Rückzug oder Härte)"),
    ],
    drift="Ohne Eingriff wandert die Balance monatlich 0,01 Richtung Mitte; Krisen (Missernte, Krieg, Unruhen in Polen) schieben sie nach rechts.",
    decisions="Kategorie „Das Politbüro“ (gebunden an die Balance): Rally the Reformers (−0,10, 50 PP, Nomenklatura −5), Rally the Orthodox (+0,10, 50 PP, Forschung −1 % für 180 Tage), "
              "Retire a Veteran (Richtung Mitte 0,05, 75 PP, Nomenklatura −10), Promote Regional Cadres (Zusammenhalt +3, 50 PP, Korruptionskosten +3 %).")

COHESION = dict(
    var="COLDWAR_SOV_union_cohesion", start=62, rng="0–100",
    tiers=[("75–100", "Unbreakable Union", "Stabilität +3 %, PP +3 %, nationalistische Drift −0,02"),
           ("55–74", "Fraternal Republics", "keine Wirkung (Start)"),
           ("35–54", "Strained Union", "Stabilität −3 %, Driftabwehr −10 %, Steuereinnahmen −5 %"),
           ("15–34", "Union in Crisis", "Stabilität −8 %, nationalistische Drift +0,05, Steuereinnahmen −10 %; Krisenzweig „The Union Treaty Question“ öffnet sich"),
           ("0–14", "Disintegration", "Stabilität −15 %; Republiken (KI) erklären Souveränität per Event, Spieler-Republiken entscheiden selbst")],
    monthly="Monatlich: −1 bei Stabilität < 40 %, −1 bei Krieg mit über 100.000 Verlusten, −1 bei Korruptionsstufe ≥ 7, +1 bei Stabilität > 70 %; Grenze 0–100.",
    tools="Fokusse (Zweig Union, Parteibäume), Entscheidungen der Kategorie „Die Union“, Events (Aralsee, Karabach, Baltikum).")

DECISIONS_C = [
    ("Das Politbüro", "Politbüro-Balance steuern (siehe oben). Freigeschaltet durch „Kremlin Politics“."),
    ("Fünfjahrpläne", "IX. (1971–75), X. (1976–80), XI. (1981–85) Plan: je eine Priorität – Gruppe A (Bau +10 %, Konsumgüter +3 %), Gruppe B (Konsumgüter −4 %, Stabilität +3 %, Bau −5 %), "
                      "Rüstung (Rüstungsfabriken +15 %, Konsumgüter +4 %), Landwirtschaft (Agrarproduktivität +10 %, Fabrikleistung −3 %). 150 PP, gültig bis Planende."),
    ("Die Union", "Entwicklungsfonds der Republiken (0,5 % BIP, Zusammenhalt +5), Kaderrotation (50 PP, Zusammenhalt −3, Korruption −1), "
                  "Russischkampagne (25 PP, Zusammenhalt −4, Ausbildungszeit −3 %), Souveräne Rechte (100 PP, Zusammenhalt +8, PP-Gewinn −5 % für 1 Jahr)."),
    ("Getreideimporte", "Nach „Buy Grain Abroad“: bei Missernte-Event Getreide kaufen (0,5 % BIP, verhindert −5 % Stabilität)."),
]

EVENTS_C = [
    ("Januar 1970: Die Troika", "Intro (Fokus 1)"), ("Lenin-Jahrhundert", "22.04.1970"), ("Operation Kavkaz", "Antwort auf Ägyptens Bitte (EGY-Baum) oder unser Angebot"),
    ("Danzig, Dezember 1970", "Polnische Krise: Gomułka stürzt – Kredite oder Disziplin"), ("Solschenizyns Nobelpreis", "Oktober 1970, Wahl der Reaktion"),
    ("Die Ernte von 1972", "Missernte, öffnet „The Harvest of 1972“"), ("Sojus 11", "Juni 1971: Tod der Besatzung – Raumfahrt-Stabilität"),
    ("Tod des Generalsekretärs", "am historischen Todesdatum des Amtsinhabers (Tabelle unten), ± 60 Tage; „The Kremlin Doctors“ schiebt Breschnews Tod um bis zu 2 Jahre. "
     "Der gewählte Erbe (`COLDWAR_SOV_heir_<name>`) wird dem Politbüro zur Abstimmung gestellt (die 3 Republiksitze stimmen mit), sofern er noch lebt; ohne Erben oder ohne Mehrheit: Plenum-Event mit 2–3 lebenden Kandidaten."),
    ("Rücktritt", "„A Dignified Retirement“ (Breschnew) oder ein gewonnenes Plenum: der Vorgänger geht in Rente, der Nachfolger übernimmt sofort; erledigte Fokusse bleiben."),
    ("Tod eines Kandidaten", "stirbt ein Politbüromitglied, verfällt sein Plenum-Fokus (Datumsgrenze) und ein auf ihn gesetzter Erbe-Flag wird gelöscht."),
    ("Der sterbende Aralsee", "ab 1980, wenn „Irrigate the Desert“"), ("Reaktorunfall", "Risiko bei „RBMK“, nicht vor 1975, sinkt mit „VVER“-Nachrüstung"),
    ("Die Karabach-Petitionen", "Wahl Status quo / Übergabe"), ("Politbüro-Krisen", "an den Rändern der Balance"),
    ("Die Union zerbricht?", "bei Zusammenhalt < 15"), ("Olympia 1980", "Boykott westlicher Spieler als Wahl"),
]

# historical life data of the CPSU candidates: plenum window and death event
NO_TREE = ("Die MD-Slots 8–12 (islamische Parteien: Vilayat-e Faqih, Salafisten, Muslimbruderschaft) bleiben im Spiel als Partei-Slots, "
           "bekommen aber keinen Baum, keinen Power-Fokus und keine Outlook-Richtung: In der Sowjetunion von 1970 hatten sie keine Machtbasis. "
           "Das Init setzt ihre Popularität auf 0 %; Events, die sie stärken, gibt es nicht.")

LEADERS_C = [
    ("Leonid Breschnew", "bre", "Start (1964)", "10.11.1982", "Startführer; Baum offen ab Tag 1", "Andropow, Tschernenko, Romanow, Gorbatschow"),
    ("Alexei Kossygin", "kos", "jederzeit bis Tod", "18.12.1980", "Reformer, Premier", "Gorbatschow, Andropow · Partei 13 (Technokraten)"),
    ("Nikolai Podgorny", "pod", "jederzeit bis Tod", "12.01.1983", "Staatsoberhaupt, Föderalist", "Partei 19 (Union souveräner Staaten) oder Präsidialsystem"),
    ("Michail Suslow", "sus", "jederzeit bis Tod", "25.01.1982", "Hardliner (Ideologie)", "Tschernenko, Romanow · Partei 6 (Neostalinisten)"),
    ("Alexander Schelepin", "she", "bis 16.04.1975", "lebt bis 1994", "Hardliner (Ordnung, Ex-KGB)", "Andropow · Partei 7 (Führerstaat)"),
    ("Juri Andropow", "and", "27.04.1973 – 09.02.1984", "09.02.1984", "KGB, Disziplin + Reform", "Gorbatschow, Tschernenko, Alijew"),
    ("Andrei Gretschko", "gre", "27.04.1973 – 26.04.1976", "26.04.1976", "General (Verteidigungsminister)", "Ustinow, Tschernenko · Partei 22 (Rat der Marschälle)"),
    ("Dmitri Ustinow", "ust", "05.03.1976 – 20.12.1984", "20.12.1984", "General (Rüstungskomplex)", "Romanow, Gorbatschow"),
    ("Grigori Romanow", "gro", "ab 05.03.1976", "lebt bis 2008", "Hardliner-Technokrat", "Ustinow oder starke Hand"),
    ("Konstantin Tschernenko", "che", "27.11.1978 – 10.03.1985", "10.03.1985", "Apparatschik", "Gorbatschow, Grischin, Romanow"),
    ("Michail Gorbatschow", "gor", "ab 21.10.1980", "lebt bis 2022", "Reformer der neuen Generation", "Präsidentschaft oder Partei 3 (Sozialdemokratie)"),
]

PORTRAITS = [("Leonid Brezhnev", "vorhanden (SOV_Coldwar_Brezhnev.dds)"), ("Mikhail Gorbachev", "vorhanden"), ("Konstantin Chernenko", "vorhanden"),
             ("Alexei Kosygin", "neu"), ("Nikolai Podgorny", "neu"), ("Mikhail Suslov", "neu"), ("Alexander Shelepin", "neu"), ("Yuri Andropov", "neu"),
             ("Marshal Andrei Grechko", "neu (Uniform)"), ("Marshal Dmitry Ustinov", "neu (Uniform)"), ("Grigory Romanov", "neu"),
             ("Viktor Grishin", "neu (Erbe Tschernenkos)"), ("Heydar Aliyev", "neu (Erbe Andropows)"), ("Nikolai Ryzhkov", "neu"),
             ("Andrei Sakharov", "neu"), ("Aleksandr Solzhenitsyn", "neu"), ("Roy Medvedev", "neu"), ("Dzhermen Gvishiani", "neu"),
             ("Vladimir Poremsky", "neu"), ("Pyotr Siuda", "neu"), ("Sergei Trapeznikov", "neu"), ("Nikolai Baibakov", "neu"),
             ("Nikolai Shchelokov", "neu"), ("Nikolai Shmelyov", "neu"), ("Grigory Galazy", "neu"), ("Alexander Yakovlev", "neu"), ("Pyotr Shelest", "neu"),
             ("Dmitry Polyansky", "neu"), ("Grand Duke Vladimir Kirillovich", "neu"),
             ("Komitee der nationalen Wiedergeburt (21)", "kollektive Führung, Emblem statt Porträt")]

FILES = [
    ("common/national_focus/COLDWAR_SOV_1970_focus.txt", "Tree `COLDWAR_SOV_1970_focus`, alle Fokusse"),
    ("common/ideas/COLDWAR_SOV_1970_ideas.txt", "Startgeister und Fokus-Ideen"),
    ("common/dynamic_modifiers/COLDWAR_SOV_1970_dynamic_modifiers.txt", "5 Länder-Modifier, Zusammenhaltsstufen, Partei- und Führerprogramme"),
    ("common/bop/COLDWAR_SOV_1970.txt", "Politbüro-Balance"),
    ("common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt", "Init, BIP-Kosten, exakte Fraktionsänderung, Outlook-Popularität, Zusammenhalt, Angebote"),
    ("common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt", "Pfad- und Führertrigger"),
    ("common/decisions/COLDWAR_SOV_1970_decisions.txt (+ categories)", "Politbüro, Fünfjahrpläne, Union, Getreide"),
    ("events/COLDWAR_SOV_1970_events.txt", "Events und Angebots-Events (Namespace `COLDWAR_SOV`)"),
    ("common/on_actions/COLDWAR_SOV_1970_on_actions.txt", "Monatliches Zusammenhalts-Update (`on_monthly_SOV`)"),
    ("common/opinion_modifiers, country_leader traits, interface/*.gfx", "Meinungen, Traits, Fokus-Icons aus den Cold-War-GFX-Ordnern"),
    ("localisation/english/COLDWAR_SOV_1970_l_english.yml", "nur Englisch, UTF-8 mit BOM"),
    ("history/countries/SOV - Russia.txt (Patch)", "`load_focus_tree = COLDWAR_SOV_1970_focus`, `COLDWAR_SOV_initialize_1970 = yes`"),
    ("mdcw_1970_focus_tree_effects.txt (Patch)", "SOV aus dem Generic-Fallback ausnehmen"),
]
