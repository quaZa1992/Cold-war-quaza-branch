# IMPERIA CW — Cold War: Cold War SOV design — d sections.
from sov_dsl import *

# ---------------------------------------------------------------- sections (tabs)
G_POL, G_LEAD, G_PARTY, G_ECO, G_MIL, G_STATE, G_FOR = ("Politbüro & Outlooks", "KPdSU & Generalsekretäre",
                                                         "Parteien", "Wirtschaft", "Militär", "Staat & Union", "Außenpolitik")

S("pol", "Die kollektive Führung", G_POL, "#b8860b",
  "Gemeinsamer Stamm für jede Regierung: Januar 1970, Troika Breschnew–Kossygin–Podgorny. Lenin-Jahrhundert, Politbüro-Balance, "
  "XXIV. Parteitag und die Richtungsfrage „Whither the Union?“, die ein Outlook stärkt.")
S("em", "Outlook: Emerging", G_POL, "#b22222",
  "Oben (über „The Leading Role of the Party“): Emerging-Outlook stärken und Macht an eine andere Emerging-Partei übergeben. "
  "Unten: freigeschaltet, sobald eine Emerging-Partei regiert (`has_government = communism`) – zum Start also sofort.")
S("we", "Outlook: Western", G_POL, "#2f5d9c",
  "Oben (über „The Convergence Memorandum“, Sacharows Konvergenztheorie 1968): Westliches Outlook stärken, Machtübergabe. "
  "Unten: freigeschaltet bei `has_government = democratic`.")
S("na", "Outlook: Non-Aligned", G_POL, "#3f8f5a",
  "Oben (über „A Third Way for Socialism“): Reform außerhalb der Parteilinie, Technokraten, Konservative, Grüne. "
  "Unten: freigeschaltet bei `has_government = neutrality`.")
S("nt", "Outlook: Nationalist", G_POL, "#6b4f9a",
  "Oben (über „The Russian Idea“): Russische Partei, Marschälle, Romanows. Kostet den Zusammenhalt der Union. "
  "Unten: freigeschaltet bei `has_government = nationalist`.")

from d_leader_sections import *

PARTY_SEC = {5: ("wc", "#d35400"), 6: ("ns", "#7e5109"), 7: ("kv", "#943126"),
             0: ("sd", "#1f4e79"), 1: ("nts", "#2e6da4"), 2: ("chr", "#5b9bd5"), 3: ("uds", "#8fb0dc"),
             13: ("gt", "#2e7d32"), 14: ("lnl", "#6d8f3a"), 15: ("rd", "#827717"),
             16: ("fel", "#9ccc65"), 17: ("fob", "#26a69a"), 18: ("smc", "#43a047"), 19: ("usr", "#7cb342"),
             20: ("rp", "#5b2c6f"), 21: ("cnr", "#4a235a"), 22: ("com", "#6c3483"), 23: ("rom", "#8e44ad")}
PARTY_DESC = {
    5: "Alt-Hist: Die Erinnerung an Nowotscherkassk 1962 wird zur Räterevolution. Fabrikräte oder Kommunen, Selbstverwaltung statt Ministerien.",
    6: "Neostalinistische Plattform um Sergei Trapesnikow (ZK-Wissenschaftsabteilung): Rehabilitierung Stalins, Mobilisierungswirtschaft, Kampagnen.",
    7: "Schelepins „Komsomolzen“ als persönliche Herrschaft: der Führerstaat, Jugendbrigaden, Sicherheitsapparat. Auch Endpunkt von Schelepins KPdSU-Weg.",
    0: "Alt-Hist: Die „Systemleute“ um Dschermen Gwischiani (Kossygins Schwiegersohn, IIASA-Gründer) – autoritäre, westlich orientierte Managerherrschaft.",
    1: "Alt-Hist: Der Volksarbeitsbund (NTS) aus Frankfurt kehrt zurück – Solidarismus, Privateigentum, Kirche, Westbindung.",
    2: "Andrei Sacharows Komitee für Menschenrechte (gegründet November 1970) übernimmt: Konvergenz, Rechtsstaat, Abrüstung.",
    3: "Roy Medwedews „sozialistische Demokratie“ – Eurokommunismus, Mehrparteiensystem innerhalb des Sozialismus.",
    13: "Gosplan-Chef Nikolai Baibakow und die Technokraten: Herrschaft der Planer ohne Ideologie.",
    14: "Alexander Solschenizyns „Brief an die Sowjetführer“ (1973): autoritär, orthodox, Russland zuerst, Abkehr von Ideologie und Imperium.",
    15: "Die Roten Direktoren und das MWD von Nikolai Schtscholokow: Schattenwirtschaft, Clan-Netzwerke, Privatisierung der Nomenklatura.",
    16: "Alt-Hist: Ökonomen um Nikolai Schmeljow – schnelle Marktöffnung, Preisfreigabe, Privatisierung.",
    17: "Die Freunde des Baikalsees um den Limnologen Grigori Galasi – Umweltschutz gegen die Gigantomanie der Planer.",
    18: "Alexander Jakowlew und ein sowjetischer „Sozialismus mit menschlichem Antlitz“: Marktsozialismus nach jugoslawisch-ungarischem Muster.",
    19: "Pjotr Schelest (bis 1972 Erster Sekretär der Ukraine): Nationalkommunismus der Republiken – eine lose Union souveräner Sowjetstaaten.",
    20: "Die „Russische Partei“ um Politbüromitglied Dmitri Poljanski und die Zeitschrift Molodaja Gwardija – Russland vor dem Imperium.",
    21: "Ultranationalistischer Untergrund (kollektive Führung) – Diktatur der „nationalen Wiedergeburt“, Säuberungen, Isolation.",
    22: "Der Rat der Marschälle um Verteidigungsminister Andrei Gretschko – Militärdiktatur, Mobilisierung, Generalstab statt Politbüro.",
    23: "Großfürst Wladimir Kirillowitsch, Chef des Hauses Romanow – Restauration einer konstitutionellen oder autokratischen Monarchie.",
}
for i, (k, col) in PARTY_SEC.items():
    S(k, f"Partei: {PARTY[i][0]} ({i})", G_PARTY, col, PARTY_DESC[i], i)

S("eco", "Gosplan & Fünfjahrpläne", G_ECO, "#1f7a7a",
  "Kossygin-Reform (vertiefen, kybernetisch planen oder zurücknehmen), IX. bis XI. Fünfjahrplan mit Prioritätswahl (Gruppe A/B/Rüstung), "
  "Togliatti und KamAZ, Preisfrage, Computer (IBM-Klon oder BESM), Schtschokino-Methode, wissenschaftlich-technische Revolution.")
S("agr", "Landwirtschaft & Getreide", G_ECO, "#7a9a1f",
  "Das ewige Agrarproblem: Kolchosen, Hoflandwirtschaft, Nicht-Schwarzerde-Programm, Bewässerung (Baumwolle und Aralsee), Getreideimporte nach 1972, Lebensmittelprogramm.")
S("en", "Energie, Sibirien & BAM", G_ECO, "#a0522d",
  "Samotlor und Westsibirien, Erdgas für Röhren (Ruhrgas-Mannesmann 1970), Druschba und Sojus, Kernkraft (RBMK oder WWER), Wasserkraft, die Baikal-Amur-Magistrale.")
S("sci", "Wissenschaft & Kosmos", G_ECO, "#4a6fa5",
  "Akademie der Wissenschaften, Akademgorodok, Lunochod, N1-Mondrakete oder Raumstationen (Saljut), Sojus-Apollo, Großforschung.")
S("army", "Sowjetarmee", G_MIL, "#556b2f",
  "Gretschko/Ustinow: Tiefe Operation, operative Manövergruppen, T-64/T-72, BMP, Luftlandetruppen, Fernostfront, Doktrin.")
S("str", "Strategische Kräfte & Luftverteidigung", G_MIL, "#4b5320",
  "Strategische Raketentruppen, Parität und SS-18/SS-20, PWO, Luftstreitkräfte, Raketenabwehr um Moskau.")
S("navy", "Hochseeflotte", G_MIL, "#2c3e50",
  "Gorschkows Hochseeflotte: Okean-70, U-Boot-Flotte, Kiew-Klasse, Mittelmeergeschwader (5. Eskadra), Stützpunkte nur per Angebot.")
S("kgb", "KGB & innere Sicherheit", G_STATE, "#34495e",
  "Andropows KGB: Fünfte Verwaltung, Dissidenten (Psychiatrie, Ausweisung oder Duldung), jüdische Emigration, Auslandsaufklärung, aktive Maßnahmen.")
S("union", "Die Union der Republiken", G_STATE, "#996515",
  "Der Zusammenhalt der Union: Ukraine (Schelest oder Schtscherbizki), Baltikum, Kaukasus, Zentralasien, Russifizierung oder Föderalisierung, Kaderrotation.")
S("soc", "Sowjetgesellschaft", G_STATE, "#8e6c8a",
  "Alkohol, Wohnungen, Sport (Olympia 1980), Kultur zwischen Tauwetter und Zensur, Kirche, Frauen, die Sowjetmenschen.")
S("det", "Entspannung & der Westen", G_FOR, "#5d6d7e",
  "Friedensprogramm des XXIV. Parteitags: Moskauer Vertrag mit der BRD, SALT und ABM, Helsinki (KSZE), Handel mit dem Westen, Nahrungsmittel gegen Entspannung.")
S("chi", "Die chinesische Frage", G_FOR, "#c0392b",
  "Nach Damanski und Tielieketi (1969): Grenzgespräche, Aufrüstung im Fernen Osten, Präventivschlag-Debatte, Eindämmung oder Versöhnung mit Peking.")
S("bloc", "Warschauer Pakt & RGW", G_FOR, "#7d3c98",
  "Breschnew-Doktrin, Komplexprogramm des RGW (1971), billiges Öl, Polen 1970, Rumäniens Eigenweg, gemeinsame Manöver – alles mit Zustimmung der Partner.")
S("tw", "Dritte Welt & Internationalismus", G_FOR, "#a04000",
  "Ägypten (Operation Kavkaz), Vietnam, Kuba, Indien (Vertrag 1971), Syrien und Irak, später Angola, Äthiopien und Afghanistan – Hilfe kostet.")
