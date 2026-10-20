# Sowjetunion 1970 – Focus-Tree-Design (Entwurf v3, 15.10.2026)

Status: **Design, noch kein Code** (Approval-Gate). Visualisierung: Artifact „Soviet Union 1970 Focus Tree“ (https://claude.ai/artifact/43ToufYGLjP7mezpQayZqU). Tree-ID `COLDWAR_SOV_1970_focus`, Präfix `COLDWAR_SOV_`, Events `COLDWAR_SOV.N`. Maschinenlesbare Daten: `claude/mdcw_sov_1970_focus_tree_data.json` (Generator-Eingabe, Effekte mit Typ und Parametern). Quellen (DSL, Validator, Export) im Mod-Ordner unter `Claude outputs/COLDWAR_SOV_design/`.

Umfang: **836 Fokusse** in 50 Bereichen · 83 Ideen (davon 7 Startgeister) · 30 Partei-/Führerprogramme · 48 Angebote an andere Länder · 19 Traits. Statische Prüfung gegen die Mod (MD 2.0.2 + Imperia + MDCW): 0 Fehler. 36 % der Fokusse haben einen Preis, 204 sind Teil einer exklusiven Wahl, 253 historisch.

## Änderungen in v2 und v3

- **Generalsekretäre schließen sich nicht mehr aus.** Neuer Bereich „Das Politbüro: Machtwechsel“: Breschnew regiert zum Start (Flag `COLDWAR_SOV_gensec_bre` aus dem Init). Jeder andere Kandidat hat einen eigenen Politbüro-Fokus, der nur prüft, ob er lebt, im Politbüro sitzt und seine Fraktionen hinter sich hat. Kein Fokus sperrt einen anderen; man kann mitten in Breschnews Baum zu Kossygin wechseln und später zu Andropow.
- **Ein Baum pro Generalsekretär, offen solange er regiert** (`COLDWAR_SOV_gensec_<name>`). Erledigte Fokusse bleiben, das Programm des Vorgängers fällt weg.
- **Elf Generalsekretäre statt sechs**, jeder detailliert (Team, erste Weiche, Politikzweige, zweite Weiche, Nachfolge, Abschluss): Breschnew, Kossygin, Podgorny, Andropow, Tschernenko, Gorbatschow; **Hardliner** Suslow, Schelepin, Romanow; **Marschälle** Gretschko und Ustinow.
- **Nachfolge über Erben-Flags** (`COLDWAR_SOV_heir_<name>`) und ein Todes-Event am historischen Todesdatum des Amtsinhabers.
- **Salafistische, schiitische und islamische Wege entfernt** (Outlook-Block, Richtung im Stamm, Power-Fokusse, Parteibäume 8–12).
- **Das Politbüro und die Republiken:** 3 Sitze für die SSR-Spieler, Abstimmungen bei Machtwechsel, Beschlüssen, Planpriorität und Anträgen; Intrige über Bewerbung, Kompromat, Pripiski und Beförderung. Der Machtwechsel läuft jetzt über Kandidatur-Fokus plus Plenum-Abstimmung.

## Leitideen

- MD-2000er-Stil (Russland/Generic): `relative_position_id`, Log in jedem `completion_reward`, `search_filters` überall, `ai_will_do` mit `is_historical_focus_on`, Kosten 1/3/5/7/10.
- Drei Kernsysteme machen das Zusammenhalten schwer, aber machbar: **7 Startgeister**, **Politbüro-Balance** (BOP wie `SOV_west_east_bop`), **Zusammenhalt der Union** (0–100, Start 62).
- Fünf Länder-Modifier mit Variablen (Muster `SOV_economy_modifier` / US-Departments): Parteistaat, Gosplan, Streitkräfte, Union, Sozialistische Gemeinschaft.
- Politik in drei Ebenen wie Ägypten Rev. 7: Stamm mit Richtungswahl (vier Richtungen) → Outlook stärken + „Power to …“ → Outlook-Einstieg (`has_government`) → Parteibäume (`*_are_in_power`). Neben der KPdSU haben 18 Parteien einen Baum.
- KPdSU: gemeinsamer Parteibaum + Politbüro-Bereich + 11 Generalsekretär-Bäume ohne gegenseitigen Ausschluss. Sechs Wege führen aus dem Parteistaat hinaus: Suslow → 6, Schelepin → 7, Kossygin → 13, Podgorny → 19, Gretschko → 22, Gorbatschow → 3.
- Nachteile nur, wo sie aus der Sache folgen. Multiplayer: kein Fokus erzwingt etwas bei einem anderen Land, alles über Angebote (Dispatcher-Event, keine Vorab-Belohnung).
- Cold-War-Integration: `mdcw_cw_add_tension`, `mdcw_cw_change_alignment`, CW-Custom-Modifier (Kampagnen, Hilfskapazität, Militärprogrammkosten, ideologische Abwehr).

## Startgeister

- **Stability of Cadres** `COLDWAR_SOV_stability_of_cadres`: PP-Gewinn +10 %, Stabilität +5 %, Bürokratiekosten +15 %, Produktivitätswachstum -5 %, Korruptionskosten +10 %. Breschnews Versprechen von 1964: niemand verliert seinen Posten. Bequem und starr. *Weg hinaus:* „The Gerontocracy Question“ (Trunk): „Renew the Cadres“ entfernt ihn, „Respect for Seniority“ macht daraus „Era of Stagnation“. Kossygins Team („Government Before Party“), Schelepins Säuberung, Gorbatschows Präsidentschaft und einige Parteibäume entfernen ihn ebenfalls.
- **The Burden of Parity** `COLDWAR_SOV_burden_of_parity`: Bau Rüstungsfabriken +10 %, Produktivität Rüstungsfabriken +5 %, Konsumgüter +5 %, Steuer Zivilindustrie -5 %, Kosten Verteidigungshaushalt +10 %. Gleichstand mit den USA – um den Preis von 12–15 % des Sozialprodukts. *Weg hinaus:* SALT I (angenommen) halbiert die Nachteile; „Superiority, Not Parity“ verschärft ihn zum „Arms Race“; Parteien mit Abrüstung entfernen ihn.
- **The Agrarian Problem** `COLDWAR_SOV_agrarian_problem`: Agrarproduktivität -15 %, Arbeitskräftebedarf Landwirtschaft +10 %, Konsumgüter +2 %, Stabilität -2 %. Kolchosen, Transportverluste, Missernten – jedes fünfte Jahr fehlt Getreide. *Weg hinaus:* Wird erst mit „The Food Programme“ (Landwirtschaft) entfernt.
- **The Ussuri Frontier** `COLDWAR_SOV_ussuri_frontier`: Kriegsunterstützung +5 %, Personalkosten Heer +10 %, Stabilität -2 %. Nach Damanski und Tielieketi stehen sich 1,5 Mio. Soldaten am Amur gegenüber. *Weg hinaus:* Grenzgespräche (angenommen) mildern ihn; „The Trans-Baikal Buildup“ macht daraus „The Eastern Fortress“; Versöhnung oder Damanski-Regelung entfernen ihn.
- **The Shadow of Prague** `COLDWAR_SOV_shadow_of_prague`: Handelsmeinung -15 %, Forschung -3 %, Ideologische Driftabwehr +10 %, Abwehr fremden Einflusses +10 %. August 1968 – der Westen misstraut, die Intelligenz schweigt. *Weg hinaus:* Moskauer Vertrag (angenommen) entfernt die Handelsstrafe; Helsinki oder „Let Them Go Their Way“ entfernen ihn ganz.
- **The Second Economy** `COLDWAR_SOV_second_economy`: Steuereinnahmen -5 %, Korruptionskosten +10 %, Konsumgüter -2 %, Stabilität +2 %. Blat, Tolkatschi, Schwarzmarkt – die Schattenwirtschaft hält die Läden halb voll. *Weg hinaus:* Je nach Weg: legalisiert (Kooperativen, „The Little Deal“, „Shadow Capitalism“) oder zerschlagen (Preisreform, elektronischer Rubel).
- **Samizdat and Dissent** `COLDWAR_SOV_dissent`: Demokratische Drift +0.02, Nationalistische Drift +0.01, Stabilität -2 %. Chronik der laufenden Ereignisse (seit 1968), Sacharow, Solschenizyn, die Refuseniks. *Weg hinaus:* „The Dissident Question“ (KGB) entscheidet: Psychiatrie, Ausweisung oder Duldung.

Startgesetze: `bureau_04`, `defence_07`, `police_04`, `edu_04`, `health_03`, `social_04`, `draft_army`, `intervention_global_interventionism`, `officer_military_academy`, `md_closed_economy`, `comprehensive_regulations`, `fully_nationalized_healthcare`, `economic_motivated_mining`, `censored_nation_05`.

Startfraktionen: Nomenklatura 75, Armee & Generalstab 70, KGB 70, Rüstungskomplex (VPK) 80, Branchenministerien 60, Kolchosbauern 45, Gewerkschaften (VTsSPS) 55.

## Politbüro-Balance `COLDWAR_SOV_politburo_bop` (Start 0,15)

- −1,0 bis −0,7 **Revisionist Crisis**: Forschung +6 %, Produktivitätswachstum +8 %, Stabilität −10 %, demokratische Drift +0,05 – Beim Eintritt: Event „Die Orthodoxen verschwören sich“ (Putschgefahr, Wahl: Zugeständnis oder Säuberung)
- −0,7 bis −0,4 **Reform Ascendancy**: Forschung +5 %, Produktivitätswachstum +6 %, Handelsmeinung +10 %, Stabilität −3 %, Driftabwehr −15 %
- −0,4 bis −0,15 **Reform Current**: Forschung +3 %, Produktivitätswachstum +3 %, Driftabwehr −5 %
- −0,15 bis +0,15 **Collective Leadership**: Stabilität +2 %, PP-Gewinn +3 % – Die Mitte ist der sichere Ort – aber ohne Dynamik
- +0,15 bis +0,4 **Orthodox Course**: Stabilität +3 %, Driftabwehr +10 %, Forschung −2 % – Startbereich (0,15)
- +0,4 bis +0,7 **Neo-Stalinist Tide**: Stabilität +5 %, PP +5 %, Driftabwehr +20 %, Polizeikosten +10 %, Forschung −5 %, Produktivitätswachstum −5 %
- +0,7 bis +1,0 **Reaction**: Driftabwehr +25 %, Kriegsunterstützung +5 %, Forschung −8 %, Produktivitätswachstum −8 %, Stabilität −5 % – Beim Eintritt: Event „Die Reformer rufen die Armee“ (Wahl: Rückzug oder Härte)

Ohne Eingriff wandert die Balance monatlich 0,01 Richtung Mitte; Krisen (Missernte, Krieg, Unruhen in Polen) schieben sie nach rechts. Kategorie „Das Politbüro“ (gebunden an die Balance): Rally the Reformers (−0,10, 50 PP, Nomenklatura −5), Rally the Orthodox (+0,10, 50 PP, Forschung −1 % für 180 Tage), Retire a Veteran (Richtung Mitte 0,05, 75 PP, Nomenklatura −10), Promote Regional Cadres (Zusammenhalt +3, 50 PP, Korruptionskosten +3 %).

## Zusammenhalt der Union `COLDWAR_SOV_union_cohesion` (Start 62)

- 75–100 **Unbreakable Union**: Stabilität +3 %, PP +3 %, nationalistische Drift −0,02
- 55–74 **Fraternal Republics**: keine Wirkung (Start)
- 35–54 **Strained Union**: Stabilität −3 %, Driftabwehr −10 %, Steuereinnahmen −5 %
- 15–34 **Union in Crisis**: Stabilität −8 %, nationalistische Drift +0,05, Steuereinnahmen −10 %; Krisenzweig „The Union Treaty Question“ öffnet sich
- 0–14 **Disintegration**: Stabilität −15 %; Republiken (KI) erklären Souveränität per Event, Spieler-Republiken entscheiden selbst

Monatlich: −1 bei Stabilität < 40 %, −1 bei Krieg mit über 100.000 Verlusten, −1 bei Korruptionsstufe ≥ 7, +1 bei Stabilität > 70 %; Grenze 0–100. Werkzeuge: Fokusse (Zweig Union, Parteibäume), Entscheidungen der Kategorie „Die Union“, Events (Aralsee, Karabach, Baltikum).

## Länder-Modifier

- **Der Parteistaat** `COLDWAR_SOV_party_state_modifier`: PP-Gewinn, Stabilität, Bürokratie-/Polizeikosten, Driftabwehr, ideologische Abwehr (Cold War), Abwehr fremden Einflusses, Korruptionskosten, Forschung. Start: alle 0.
- **Gosplan – Planwirtschaft** `COLDWAR_SOV_gosplan_modifier`: Bau, Effizienzzuwachs, Max. Effizienz, Produktivitätswachstum, Konsumgüter, Zivil-/Rüstungssteuer, Steuereinnahmen, Agrarproduktivität, Fabrikleistung, Öl-/Rohstoffexporte, Energie, Sozial-/Gesundheitskosten, Handelsmeinung. Start: alle 0.
- **Streitkräfte der UdSSR** `COLDWAR_SOV_armed_forces_modifier`: Angriff, Verteidigung, Organisation, Moral, Ausbildung, Planung, Personal-/Ausrüstungskosten, Rekrutierung, Durchbruch, Marine-Reichweite, Luftverteidigung. Start: Personalkosten Heer +5 % (Großarmee).
- **Union der Republiken** `COLDWAR_SOV_union_modifier`: Stabilität, nationalistische Drift, Driftabwehr – plus die Stufe des Zusammenhalts (siehe unten). Start: Zusammenhalt 62 → Stufe „Fraternal Republics“.
- **Sozialistische Gemeinschaft** `COLDWAR_SOV_commonwealth_modifier`: Kosten des Imperiums: Steuereinnahmen, Öl-Exporterlöse (Vorzugspreise RGW), Auslandseinfluss, Meinungsgewinn gleicher Ideologie, Unterstützungskampagnen (Cold War), Hilfsprogramm-Kapazität, Forschungsteilung. Start: Steuern −3 %, Öl-Exporterlöse −10 %, Kampagnen +10 %, Meinungsgewinn +10 %, Einfluss +5 %.

## Entscheidungen

- **Das Politbüro**: Politbüro-Balance steuern (siehe oben). Freigeschaltet durch „Kremlin Politics“.
- **Fünfjahrpläne**: IX. (1971–75), X. (1976–80), XI. (1981–85) Plan: je eine Priorität – Gruppe A (Bau +10 %, Konsumgüter +3 %), Gruppe B (Konsumgüter −4 %, Stabilität +3 %, Bau −5 %), Rüstung (Rüstungsfabriken +15 %, Konsumgüter +4 %), Landwirtschaft (Agrarproduktivität +10 %, Fabrikleistung −3 %). 150 PP, gültig bis Planende.
- **Die Union**: Entwicklungsfonds der Republiken (0,5 % BIP, Zusammenhalt +5), Kaderrotation (50 PP, Zusammenhalt −3, Korruption −1), Russischkampagne (25 PP, Zusammenhalt −4, Ausbildungszeit −3 %), Souveräne Rechte (100 PP, Zusammenhalt +8, PP-Gewinn −5 % für 1 Jahr).
- **Getreideimporte**: Nach „Buy Grain Abroad“: bei Missernte-Event Getreide kaufen (0,5 % BIP, verhindert −5 % Stabilität).

## Events

- **Januar 1970: Die Troika**: Intro (Fokus 1)
- **Lenin-Jahrhundert**: 22.04.1970
- **Operation Kavkaz**: Antwort auf Ägyptens Bitte (EGY-Baum) oder unser Angebot
- **Danzig, Dezember 1970**: Polnische Krise: Gomułka stürzt – Kredite oder Disziplin
- **Solschenizyns Nobelpreis**: Oktober 1970, Wahl der Reaktion
- **Die Ernte von 1972**: Missernte, öffnet „The Harvest of 1972“
- **Sojus 11**: Juni 1971: Tod der Besatzung – Raumfahrt-Stabilität
- **Tod des Generalsekretärs**: am historischen Todesdatum des Amtsinhabers (Tabelle unten), ± 60 Tage; „The Kremlin Doctors“ schiebt Breschnews Tod um bis zu 2 Jahre. Der gewählte Erbe (`COLDWAR_SOV_heir_<name>`) wird dem Politbüro zur Abstimmung gestellt (die 3 Republiksitze stimmen mit), sofern er noch lebt; ohne Erben oder ohne Mehrheit: Plenum-Event mit 2–3 lebenden Kandidaten.
- **Rücktritt**: „A Dignified Retirement“ (Breschnew) oder ein gewonnenes Plenum: der Vorgänger geht in Rente, der Nachfolger übernimmt sofort; erledigte Fokusse bleiben.
- **Tod eines Kandidaten**: stirbt ein Politbüromitglied, verfällt sein Plenum-Fokus (Datumsgrenze) und ein auf ihn gesetzter Erbe-Flag wird gelöscht.
- **Der sterbende Aralsee**: ab 1980, wenn „Irrigate the Desert“
- **Reaktorunfall**: Risiko bei „RBMK“, nicht vor 1975, sinkt mit „VVER“-Nachrüstung
- **Die Karabach-Petitionen**: Wahl Status quo / Übergabe
- **Politbüro-Krisen**: an den Rändern der Balance
- **Die Union zerbricht?**: bei Zusammenhalt < 15
- **Olympia 1980**: Boykott westlicher Spieler als Wahl

## KPdSU: Politbüro und Generalsekretäre

Ablauf: `ple_the_politburo` (Kosten 1) öffnet die Politbüro-Fokusse und Breschnews Baum. Jeder Politbüro-Fokus (`ple_<name>`, Kosten 5) baut eine Kandidatur auf und öffnet die Entscheidung „Convene the Plenum: <Name>“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag). Das Politbüro stimmt ab (Generalsekretär 1, Moskauer Block 7 nach Balance und Richtung des Kandidaten, 3 Republiksitze). Bei Mehrheit setzt `COLDWAR_SOV_install_gensec` den neuen Generalsekretär ein (Flag tauschen, `create_country_leader` / `promote_character`, Traits), mit Stabilität −5 %, „Plenum Shake-up“ (Stabilität −5 %, PP −10 %, 120 Tage) und Fraktionsänderungen nach Kandidat; ohne Mehrheit kein Wechsel, Stabilität −3 %, Balance 0,05 gegen ihn. Kein Politbüro-Fokus ist exklusiv. Ein Generalsekretär-Baum hat als `available` `communist_states_are_in_power` + `has_country_flag = COLDWAR_SOV_gensec_<name>`.

Erben: Die Nachfolgeweiche in jedem Baum setzt `COLDWAR_SOV_heir_<name>`. Das Todes-Event am historischen Datum des Amtsinhabers stellt den Erben dem Politbüro zur Abstimmung (ohne Fokus-Kosten; der Politbüro-Fokus wird per `unlock_national_focus` als erledigt markiert), sofern der Erbe dann noch lebt; ohne Erben oder ohne Mehrheit folgt ein Plenum-Event mit den lebenden Kandidaten. Die KI folgt den historischen Todesfällen und nimmt keine alt-hist Politbüro-Fokusse.

| Generalsekretär | Typ | Politbüro-Fokus | Tod | Erben und Endpunkte | Fokusse |
|---|---|---|---|---|---|
| Leonid Breschnew | Startführer; Baum offen ab Tag 1 | Start (1964) | 10.11.1982 | Andropow, Tschernenko, Romanow, Gorbatschow | 40 |
| Alexei Kossygin | Reformer, Premier | jederzeit bis Tod | 18.12.1980 | Gorbatschow, Andropow · Partei 13 (Technokraten) | 30 |
| Nikolai Podgorny | Staatsoberhaupt, Föderalist | jederzeit bis Tod | 12.01.1983 | Partei 19 (Union souveräner Staaten) oder Präsidialsystem | 21 |
| Michail Suslow | Hardliner (Ideologie) | jederzeit bis Tod | 25.01.1982 | Tschernenko, Romanow · Partei 6 (Neostalinisten) | 24 |
| Alexander Schelepin | Hardliner (Ordnung, Ex-KGB) | bis 16.04.1975 | lebt bis 1994 | Andropow · Partei 7 (Führerstaat) | 23 |
| Juri Andropow | KGB, Disziplin + Reform | 27.04.1973 – 09.02.1984 | 09.02.1984 | Gorbatschow, Tschernenko, Alijew | 23 |
| Andrei Gretschko | General (Verteidigungsminister) | 27.04.1973 – 26.04.1976 | 26.04.1976 | Ustinow, Tschernenko · Partei 22 (Rat der Marschälle) | 21 |
| Dmitri Ustinow | General (Rüstungskomplex) | 05.03.1976 – 20.12.1984 | 20.12.1984 | Romanow, Gorbatschow | 23 |
| Grigori Romanow | Hardliner-Technokrat | ab 05.03.1976 | lebt bis 2008 | Ustinow oder starke Hand | 18 |
| Konstantin Tschernenko | Apparatschik | 27.11.1978 – 10.03.1985 | 10.03.1985 | Gorbatschow, Grischin, Romanow | 17 |
| Michail Gorbatschow | Reformer der neuen Generation | ab 21.10.1980 | lebt bis 2022 | Präsidentschaft oder Partei 3 (Sozialdemokratie) | 24 |

## Das Politbüro und die Republiken (3 Sitze)

Multiplayer-RP-System: Die 14 Unionsrepubliken (SSR-Spieler) kämpfen um 3 Sitze im Politbüro. Verhandelt wird im Discord; das Spiel hält Sitze, Abstimmungen und Folgen fest und meldet jedes Ergebnis allen Spielern als News. Keine Loyalitätswerte pro Republik. Außenpolitische Mitsprache ist bewusst noch nicht enthalten.

- **Sitze**: 3 Sitze im Politbüro für die 14 Unionsrepubliken (die RSFSR ist Moskau selbst). Vollmitglied mit Stimme, keine Kandidatenstufe.
- **Wer vergibt**: Moskau (SOV) per gezielter Entscheidung auf eine SSR. Kostenlos im 30-Tage-Fenster eines Parteitags, sonst nur per außerordentlichem Plenum (100 PP, Stabilität −3 %).
- **Start 1970**: Ukraine (Pjotr Schelest, Vollmitglied seit 1964) und Kasachstan (Dinmuchamed Kunajew, historisch ab April 1971 Vollmitglied). Der dritte Sitz ist frei bis zum XXIV. Parteitag (30.03.1971): die erste Intrige der Partie.
- **Keine Zähler**: Keine Loyalitätswerte pro Republik. Das Spiel kennt nur Status (Sitz, In Disgrace, Slanderer, Patron, Pripiski, Souveränität), feste Termine und sichtbare Abstimmungen. Verhandelt wird im Discord.

**Seat in the Politburo**: PP-Gewinn +15 %, Stabilität +5 %, Baugeschwindigkeit +10 %. Rechte: 1 Stimme in jeder Abstimmung (Machtwechsel, Beschlüsse, Planpriorität, Anträge); 1 Antrag pro Sitzung (Unionsprojekt, Planentlastung, Kaderschutz); 1 Unionsprojekt pro Fünfjahrplan automatisch: ein Gebäude nach Wahl in der eigenen Republik, Moskau zahlt. „Moskaus Auge“: Wer einen Sitz hat, kann keine nationalen Entscheidungen nehmen (Volksfront, Souveränität, Referendum). Der Sitz bindet an die Zentrale.

**Rhythmus:** Parteitage XXIV. 30.03.1971, XXV. 24.02.1976, XXVI. 23.02.1981, XXVII. 25.02.1986, XXVIII. 02.07.1990; Fünfjahrpläne IX. 1971–1975, X. 1976–1980, XI. 1981–1985, XII. 1986–1990. Bewerbungen öffnen 90 Tage vor jedem Parteitag; im Parteitag 30 Tage Umbesetzung. Sitzungen am 1. Januar und 1. Juli (erste: 01.07.1970); Moskau kann eine zusätzliche Sitzung einberufen (50 PP).

**Abstimmung:** Generalsekretär (SOV-Spieler): 1 Stimme, frei. Moskauer Block: 7 Stimmen, folgen der Politbüro-Balance. Ja-Stimmen = runden(3,5 + 3,5 × Balance × Richtung), Richtung −1 reformerisch, 0 neutral, +1 orthodox. Bei Anträgen der Republiken immer 3 Ja (die Zentrale ist skeptisch). Republiken: je 1 Stimme (mit Podgornys „A Federal Union“ 2 bei Unionsfragen). Ohne Antwort nach 10 Tagen: Enthaltung. Mehrheit: mehr als die Hälfte aller Stimmen (6 von 11). Enthaltung zählt nicht als Ja.

| Gegenstand | Von | Richtung | Wann | Folgen |
|---|---|---|---|---|
| Machtwechsel | Moskau | nach Kandidat | Politbüro-Fokus = Kandidatur, dann Entscheidung „Convene the Plenum“ (wiederholbar) | Verbindlich. Ja: neuer Generalsekretär. Nein: kein Wechsel, Stabilität −3 %, Balance 0,05 gegen den Kandidaten, 180 Tage Sperre. |
| Nachfolge nach Tod | Event | nach Erbe | Der gewählte Erbe wird zur Abstimmung gestellt | Verbindlich. Nein: Plenum-Event mit den anderen lebenden Kandidaten, erneute Abstimmung. |
| Politbüro-Beschluss | Moskau | je Fokus | 11 innenpolitische Schlüsselfokusse (Kader, Kossygin-Reform, Preise, Sprache, Unionsvertrag) | Ja: Mandat (PP +25, Stabilität +2 %). Nein: „Defying the Politburo“ und Zusammenhalt −2. Der Fokus gilt trotzdem. |
| Planpriorität | Moskau | neutral | Zu Beginn jedes Fünfjahrplans (1971, 1976, 1981, 1986) | Ja: Plan gilt, PP +50. Nein: Plan gilt, „Defying the Politburo“. |
| Antrag einer Republik | Mitglied | Moskauer Block 3 Ja | Erst entscheidet Moskau; lehnt Moskau ab, kann das Mitglied vor das Politbüro gehen | Ja: Moskau setzt um oder trägt „Defying the Politburo“. Nein: Antrag fällt. |

Politbüro-Beschlüsse im Baum: `renew_the_cadres` (reformerisch), `respect_for_seniority` (orthodox), `deepen_the_kosygin_reform` (reformerisch), `cybernetic_planning` (neutral), `the_ministries_restored` (orthodox), `raise_retail_prices` (reformerisch), `hold_the_prices` (orthodox), `russian_as_lingua_franca` (orthodox), `native_language_schools` (reformerisch), `the_renewed_federation` (reformerisch), `the_iron_union` (orthodox).

**Anträge der Mitglieder** (1 pro Sitzung; erst entscheidet Moskau, bei Ablehnung Abstimmung):

- **Unionsprojekt**: Ein Gebäude in der eigenen Republik: Zivilfabrik, Infrastruktur, Kraftwerk, Agrar oder Rüstungsfabrik. Moskau zahlt 0,5 % BIP (Rüstung 0,8 %) über `skip_payment`; Zusammenhalt +1.
- **Planentlastung**: Die Republik bekommt „Plan Relief“ (Stabilität +3 %, PP +5 %, 2 Jahre). Moskau bekommt „Plan Shortfall“ (Steuereinnahmen −1 %, 2 Jahre).
- **Kaderschutz**: Immunität gegen Kompromat bis zum nächsten Parteitag. Kostet Moskau nichts außer einem Werkzeug.

**Intrige:**

- **Bewerbung** (Jede SSR ohne „Slanderer“): 90 Tage vor dem Parteitag ein verdecktes Gebot: 25, 50 oder 100 PP, sofort bezahlt. Nur Moskau sieht die Gebote. Moskau erhält die Gebote der Gewählten; die anderen bekommen die Hälfte zurück.
- **Kompromat** (Jede SSR (50 PP)): Gegen einen Sitzinhaber. Moskau ermittelt (25 PP) oder ignoriert. Chance: 15 % + 5 % je Korruptionsstufe (`corruption_level_01`–`10`), +25 % bei Pripiski, +20 % Andropow, −10 % Barone, 0 % mit Kaderschutz, höchstens 90 %. Erfolg: Sitz weg, „In Disgrace“ bis zum übernächsten Parteitag, Angebot den Ersten Sekretär zu ersetzen, Zusammenhalt −1. Fehlschlag: Ankläger wird „Slanderer“ bis zum nächsten Parteitag.
- **Pripiski** (Jede SSR, einmal pro Plan): Plan übererfüllt melden: PP +50, die News zeigt „Planerfüllung 108 %“. Korruption +1 Stufe und das Flag Pripiski, bis es aufgedeckt wird. Leichtes Ziel für Kompromat und die Baumwollaffäre.
- **Beförderung nach Moskau** (Moskau → Sitzinhaber): Angebot (wie Alijew 1982, Schewardnadse 1985): Der Erste Sekretär geht nach Moskau. Annahme: neuer Erster Sekretär, der Sitz wird sofort frei (ohne Plenum-Kosten), die Republik bekommt dauerhaft „Patron in Moscow“ (PP +5 %, 1 Antrag pro Jahr auch ohne Sitz). Ablehnung: keine Strafe.

**Ohne Sitz:**

- **Petition**: 1 pro Jahr an Moskau, Inhalt wie ein Unionsprojekt. Moskau kann sie kostenlos ignorieren.
- **Klient**: Ein Mitglied stellt seinen Antrag für eine Klient-Republik; das Projekt entsteht dort, beide stehen in der News. Netzwerke entstehen.
- **Volksfront**: Nur ohne Sitz: nationale Partei der SSR +5 % Popularität; Zusammenhalt −2.
- **Souveränitätserklärung**: Nur ohne Sitz, ab Zusammenhalt < 55 oder 1985: „Declaration of Sovereignty“ (Stabilität +3 %, PP +5 %); Zusammenhalt −8, Moskau Steuereinnahmen −1 %.
- **Referendum**: Nur ohne Sitz, ab Zusammenhalt < 35: Moskau verhandelt (Unionsvertrag), erkennt an (Republik entlassen) oder lehnt ab. Gewalt nur per normaler Kriegserklärung.

**Zusammenhalt** (nur feste Schritte): Sitz vergeben +1, Unionsprojekt oder Antrag umgesetzt +1, Kompromat erfolgreich −1, Sitz entzogen −2, Mehrheit übergangen −2, Volksfront −2, Souveränitätserklärung −8, Referendum −10.

**Die Generalsekretäre ändern die Regeln** (Zahl der Sitze bleibt 3):

- `trust_the_local_barons` (Breschnew / Union): Sitze nur noch auf Parteitagen änderbar (kein außerordentliches Plenum); Kompromat-Chance −10 %
- `rotate_the_cadres` (Union): Auf jedem Parteitag muss mindestens ein Sitz die Republik wechseln (Moskau wählt welchen)
- `and_the_discipline_campaign` (Andropow): Kompromat-Chance +20 %; der KGB darf ohne Ankläger gegen einen Sitzinhaber ermitteln (50 PP)
- `and_the_cotton_affair_exposed` (Andropow): Jede Republik mit Pripiski-Flag wird sofort untersucht
- `pod_a_federal_union` (Podgorny): Republikstimmen zählen doppelt bei Unionsfragen (Sprache, Unionsvertrag, Anträge der Republiken)
- `she_purge_the_brezhnevites` (Schelepin): Einmal: einen Sitzinhaber ohne Plenum-Kosten absetzen
- `gro_iron_discipline` (Romanow): Pripiski kosten zusätzlich Stabilität −3 % bei der Republik, die sie meldet
- `gor_the_presidency` (Gorbatschow): Föderationsrat (März 1990): Das Sitz-System endet, alle Republiken beraten den Präsidenten, Sitz-Buffs entfallen

**KI:**

- **Moskau als KI**: Historische Sitze: Ukraine und Kasachstan, auf dem XXIV. Parteitag Belarus (Mascherow), nach Mascherows Tod (Oktober 1980) auf dem XXVI. Parteitag Aserbaidschan (Alijew). Keine Beförderung, kein Kompromat.
- **Republik als KI**: Stimmt mit dem Generalsekretär; bewirbt sich mit 25 PP; alle 2 Jahre ein Unionsprojekt-Antrag; kein Kompromat, keine Pripiski, keine nationale Bewegung vor Zusammenhalt < 15.
- **Abwesende Spieler**: Nach 10 Tagen zählt keine Antwort als Enthaltung. Kein Spieler kann eine Abstimmung blockieren.

**Dateien:**

- `common/decisions/COLDWAR_SOV_politburo_decisions.txt`: Moskau: „Seats of the Republics“ (gezielt auf SSRs, `target_trigger` Subjekt der UdSSR mit `autonomy_soviet_republic_1985`); SSR: „The Republic and the Politburo“
- `common/scripted_effects/COLDWAR_SOV_politburo_effects.txt`: Sitz vergeben/entziehen, Abstimmung starten, Moskauer Block berechnen, auszählen, Kompromat würfeln
- `events/COLDWAR_SOV_politburo_events.txt`: Sitzung, Abstimmung je Mitglied, Auszählung, News an alle, Parteitag, Kompromat, Beförderung, Referendum
- `common/ideas/COLDWAR_SOV_politburo_ideas.txt`: Seat in the Politburo, Defying the Politburo, Patron in Moscow, In Disgrace, Slanderer, Plan Relief, Plan Shortfall, Declaration of Sovereignty
- `Variablen`: `global.COLDWAR_politburo_seats` (Array der Länder), `global.COLDWAR_vote_yes/no`, Flags auf den SSRs (`COLDWAR_SSR_seat`, `_pripiski`, `_disgrace`, `_slanderer`, `_cadre_protection`)
- `später: interface/COLDWAR_politburo_window.gui`: Politbüro-Fenster als Scripted GUI nach den MDCW-UI-Regeln (`player_context`, dirty-Variable, KI wertet nie aus)

## Parteien

| # | Partei | Ideologie | Führung 1970 | Baum |
|---|---|---|---|---|
| 0 | Systems Directorate | Western Autocracy | Dzhermen Gvishiani | 14 Fokusse |
| 1 | People's Labour Union (NTS) | Conservatism | Vladimir Poremsky | 13 Fokusse |
| 2 | Committee for Human Rights | Liberalism | Andrei Sakharov | 15 Fokusse |
| 3 | Union of Democratic Socialists | Socialism | Roy Medvedev | 13 Fokusse |
| 4 | Communist Party of the Soviet Union | Communist State | Leonid Brezhnev | KPdSU + Politbüro + Generalsekretäre |
| 5 | Free Councils of Labour | Anarchist Communism | Pyotr Siuda | 17 Fokusse |
| 6 | Neo-Stalinist Platform | Emerging Conservative | Sergei Trapeznikov | 17 Fokusse |
| 7 | Komsomol Vanguard | Emerging Autocracy | Alexander Shelepin | 17 Fokusse |
| 8 | Transcaucasian Islamic Revival | Moderate Vilayat-e Faqih | Shia Revival Council | kein Baum |
| 9 | Guardians of the Faith | Vilayat-e Faqih | Council of Guardians | kein Baum |
| 10 | Bukharan Restoration | Salafist Kingdom | Bukharan Regency Council | kein Baum |
| 11 | Basmachi Revival | Caliphate | Ferghana Mujahideen Council | kein Baum |
| 12 | Muslim Spiritual Reformists | Muslim Brotherhood | Ziyauddin Babakhanov | kein Baum |
| 13 | Gosplan Technocracy | Neutral Autocracy | Nikolai Baibakov | 13 Fokusse |
| 14 | Live Not by Lies | Neutral Conservatism | Aleksandr Solzhenitsyn | 13 Fokusse |
| 15 | The Red Directors | Oligarchism | Nikolai Shchelokov | 13 Fokusse |
| 16 | Free Enterprise League | Neutral Libertarian | Nikolai Shmelyov | 9 Fokusse |
| 17 | Friends of Baikal | Neutral Green | Grigory Galazy | 10 Fokusse |
| 18 | Socialist Market Commonwealth | Neutral Social | Alexander Yakovlev | 12 Fokusse |
| 19 | Union of Sovereign Republics | Neutral Communism | Pyotr Shelest | 9 Fokusse |
| 20 | The Russian Party | Nationalist Populism | Dmitry Polyansky | 13 Fokusse |
| 21 | Committee of National Rebirth | Nationalist Fascism | Committee of National Rebirth | 7 Fokusse |
| 22 | Council of Marshals | Military Junta | Andrei Grechko | 13 Fokusse |
| 23 | House of Romanov | Monarchism | Grand Duke Vladimir Kirillovich | 10 Fokusse |

Die MD-Slots 8–12 (islamische Parteien: Vilayat-e Faqih, Salafisten, Muslimbruderschaft) bleiben im Spiel als Partei-Slots, bekommen aber keinen Baum, keinen Power-Fokus und keine Outlook-Richtung: In der Sowjetunion von 1970 hatten sie keine Machtbasis. Das Init setzt ihre Popularität auf 0 %; Events, die sie stärken, gibt es nicht.

## Angebote (Multiplayer)

- `COLDWAR_SOV_offer_gas_for_pipes` → GER: Röhren von Mannesmann auf Kredit gegen sowjetisches Erdgas ab 1973. Bei Annahme: UdSSR erhält Forschungsbonus Infrastruktur, Handelsmeinung +10 %, Schulden 0,5 % BIP; BRD erhält Energiebonus
- `COLDWAR_SOV_offer_soyuz_apollo` → USA: Gemeinsamer Flug (ASTP). Bei Annahme: beide +3 % Forschung für 2 Jahre, Spannung −1, Meinung +15
- `COLDWAR_SOV_offer_tartus_supply_point` → SYR: Marine-Versorgungspunkt Tartus (1971). Bei Annahme: Syrien erhält Militärhilfe (+5 % Organisation), UdSSR Reichweite Marine +5 %
- `COLDWAR_SOV_offer_naval_access` → SOM, SYE, VIE: Hafenrechte (Berbera, Aden, Cam Ranh). Bei Annahme: Partner erhält Hilfe 0,3 % unseres BIP; wir Reichweite Marine +5 % je Hafen
- `COLDWAR_SOV_offer_moscow_treaty` → GER: Gewaltverzicht und Anerkennung der Nachkriegsgrenzen. Bei Annahme: Spannung −2, Meinung +20 beidseitig, verbessertes Handelsabkommen; „The Shadow of Prague“ verliert die Handelsstrafe
- `COLDWAR_SOV_offer_berlin_agreement` → USA, ENG, FRA: Viermächteabkommen über Berlin (1971). Bei Annahme aller: Spannung −2, DDR/BRD-Transit gesichert
- `COLDWAR_SOV_offer_salt_i` → USA: SALT I und ABM-Vertrag. Bei Annahme: beide erhalten „Arms Limitation“ (Kosten Verteidigungshaushalt −10 %, Kriegsunterstützung −2 %), Spannung −3; „The Burden of Parity“ wird abgeschwächt
- `COLDWAR_SOV_offer_moscow_summit` → USA: Gipfel in Moskau (Mai 1972). Bei Annahme: Spannung −2, „Basic Principles of Relations“, Meinung +15
- `COLDWAR_SOV_offer_paris_axis` → FRA: Französisch-sowjetische Zusammenarbeit (Pompidou 1970/71). Bei Annahme: Forschungsbonus Elektronik für beide, Meinung +20
- `COLDWAR_SOV_offer_vladivostok` → USA: Rahmen für SALT II. Bei Annahme: Spannung −1, Meinung +10
- `COLDWAR_SOV_offer_helsinki` → USA, GER, FRA, ENG: Schlussakte der KSZE. Bei Annahme: Unverletzlichkeit der Grenzen; Spannung −3
- `COLDWAR_SOV_offer_salt_ii` → USA: SALT II in Wien. Bei Annahme: Spannung −2, Kosten Verteidigungshaushalt −5 % für beide
- `COLDWAR_SOV_offer_border_talks` → CHI: Grenzgespräche (seit Oktober 1969). Bei Annahme: Spannung −1, „The Ussuri Frontier“ verliert die Stabilitätsstrafe
- `COLDWAR_SOV_offer_mongolian_garrison` → MON: Stationierung der 39. Armee in der Mongolei. Bei Annahme: MON erhält Hilfe 0,2 % BIP/Jahr und Verteidigung +5 %
- `COLDWAR_SOV_offer_india_treaty` → RAJ: Vertrag über Frieden, Freundschaft und Zusammenarbeit (August 1971). Bei Annahme: Rüstungshilfe, Meinung +25, Handelsabkommen
- `COLDWAR_SOV_offer_vietnam_treaty` → VIE: Freundschaftsvertrag (November 1978). Bei Annahme: Cam-Ranh-Rechte und gemeinsame Front gegen China
- `COLDWAR_SOV_offer_sino_soviet_truce` → CHI: Ideologischer Waffenstillstand. Bei Annahme: „The Ussuri Frontier“ entfällt, Spannung −2, Meinung +30; Peking kann ins sowjetische Lager zurück (Cold-War-Blockwechsel bleibt Pekings Entscheidung)
- `COLDWAR_SOV_offer_damansky_settlement` → CHI: Damanski/Zhenbao an China, Flussgrenze in der Fahrrinne. Bei Annahme: „The Ussuri Frontier“ wird entfernt, Spannung −1
- `COLDWAR_SOV_offer_soyuz_pipeline` → DDR, POL, CZE, HUN, ROM, BUL: Gemeinsamer Bau der Orenburg-Gasleitung. Bei Annahme: Partner zahlt 0,2 % BIP und erhält Energie +5 %; UdSSR erhält Bau +3 %
- `COLDWAR_SOV_offer_joint_exercises` → DDR, POL, CZE, HUN, ROM, BUL: Gemeinsame Manöver „Schild“/„Waffenbrüderschaft“. Bei Annahme: beide +25 Heereserfahrung
- `COLDWAR_SOV_offer_credits_for_poland` → POL: Rohstoffkredite und Getreide. Bei Annahme: POL erhält 0,4 % unseres BIP, Stabilität +5 %; wir zahlen
- `COLDWAR_SOV_offer_interkosmos` → DDR, POL, CZE, HUN, ROM, BUL, CUB, MON, VIE: Ein Kosmonaut des Partners fliegt mit Sojus. Bei Annahme: Partner +5 % Stabilität (1 Jahr), Meinung +20
- `COLDWAR_SOV_offer_operation_kavkaz` → EGY: Eine Flugabwehrdivision und MiG-21-Staffeln am Suezkanal. Bei Annahme: EGY Luftverteidigung, wir +25 Lufterfahrung, Spannung +1
- `COLDWAR_SOV_offer_egypt_treaty` → EGY: Freundschaftsvertrag (Mai 1971). Bei Annahme: Meinung +25, Einfluss +5 %
- `COLDWAR_SOV_offer_arms_for_hanoi` → VIE: Luftabwehrraketen, MiGs und Reis. Bei Annahme: VIE erhält Ausrüstung und Verteidigung +5 %; wir zahlen 0,4 % BIP
- `COLDWAR_SOV_offer_sugar_for_oil` → CUB: Öl gegen Zucker zu Vorzugspreisen. Bei Annahme: CUB Stabilität +5 %, Wirtschaft +; wir Sozialistische Gemeinschaft: Steuern −1 %
- `COLDWAR_SOV_offer_iraq_treaty` → IRQ: Freundschaftsvertrag (April 1972). Bei Annahme: Meinung +20, Ölkooperation
- `COLDWAR_SOV_offer_syria_arms` → SYR: Rüstungspaket und Berater. Bei Annahme: SYR +5 % Verteidigung, Meinung +20
- `COLDWAR_SOV_offer_angola_support` → AGL: Unterstützung der MPLA mit Waffen und kubanischen Truppen. Bei Annahme: AGL +10 % Angriff (2 Jahre)
- `COLDWAR_SOV_offer_ethiopia_airlift` → ETH: Luftbrücke und kubanische Brigaden (1977/78). Bei Annahme: ETH Angriff +10 %
- `COLDWAR_SOV_offer_somalia_support` → SOM: Waffen und Berater. Bei Annahme: SOM Angriff +10 %, Berbera bleibt sowjetisch
- `COLDWAR_SOV_offer_limited_contingent` → AFG: Die afghanische Regierung bittet um Truppen (Dezember 1979). Bei Annahme: Expeditionsstreitkräfte, wir erhalten „The Afghan Burden“ (Stabilität −3 %, Kriegsunterstützung −5 %, 0,3 % BIP/Monat) solange der Krieg läuft
- `COLDWAR_SOV_offer_brezhnev_visit` → USA: Abkommen zur Verhütung von Atomkriegen. Bei Annahme: Spannung −2, Meinung +15
- `COLDWAR_SOV_offer_pipelines_to_europe` → GER, ITA, FRA: Langfristige Gaslieferverträge. Bei Annahme: Partner Energie +5 %, wir Öl-Exporterlöse +5 %, Meinung +10
- `COLDWAR_SOV_offer_kosygin_summit` → USA: Gipfel mit dem Premier. Bei Annahme: Spannung −2, Handelsabkommen, Meinung +15
- `COLDWAR_SOV_offer_shelepin_china` → CHI: Gespräche zwischen zwei Lagern der „reinen Linie“. Bei Annahme: Meinung +20, Spannung an der Grenze sinkt (Ussuri-Geist mildert sich)
- `COLDWAR_SOV_offer_andropov_china` → CHI: Wiederaufnahme der Konsultationen (1982). Bei Annahme: Meinung +15, Spannung −1
- `COLDWAR_SOV_offer_gre_advisers` → EGY, SYR, IRQ: Militärberater und Ausbildung. Bei Annahme: Partner +5 % Organisation, Meinung +15
- `COLDWAR_SOV_offer_chernenko_talks` → USA: Neue Abrüstungsgespräche in Genf. Bei Annahme: Spannung −2
- `COLDWAR_SOV_offer_inf_treaty` → USA: Abbau aller Mittelstreckenraketen (INF). Bei Annahme: Spannung −4, beide Kosten Verteidigungshaushalt −5 %
- `COLDWAR_SOV_offer_stalinist_reconciliation` → CHI: Gemeinsame Rückkehr zur „reinen Linie“. Bei Annahme: Meinung +30, „The Ussuri Frontier“ entfällt
- `COLDWAR_SOV_offer_komsomol_china` → CHI: Pragmatische Annäherung zweier Führerstaaten. Bei Annahme: Meinung +20, Spannung −1
- `COLDWAR_SOV_offer_cocom` → USA: Lockerung der westlichen Exportkontrollen. Bei Annahme: Forschungsbonus Elektronik ×2, Spannung −2
- `COLDWAR_SOV_offer_convergence_treaty` → USA: Gemeinsame Abrüstung und Wissenschaftskooperation. Bei Annahme: Spannung −5, beide +3 % Forschung
- `COLDWAR_SOV_offer_social_democratic_partners` → GER, SWE: Sozialdemokratische Partnerschaft. Bei Annahme: Meinung +20, Handelsabkommen
- `COLDWAR_SOV_offer_slavic_union` → UKR, BLR, KAZ: Union der drei ostslawischen Völker (und Kasachstans). Bei Annahme: bleibt Unionsrepublik mit erweiterter Autonomie
- `COLDWAR_SOV_offer_slavic_core` → UKR, BLR: Engere Union der Ostslawen. Bei Annahme: Meinung +20, Autonomie bleibt, Zusammenhalt +5
- `COLDWAR_SOV_offer_royal_houses` → ENG, SPR: Anerkennung der restaurierten Krone. Bei Annahme: Meinung +25

## Fokusse

### Die kollektive Führung (14)

Gemeinsamer Stamm für jede Regierung: Januar 1970, Troika Breschnew–Kossygin–Podgorny. Lenin-Jahrhundert, Politbüro-Balance, XXIV. Parteitag und die Richtungsfrage „Whither the Union?“, die ein Outlook stärkt.

- **The Collective Leadership** `COLDWAR_SOV_the_collective_leadership` · Kosten 1 · hist. · benötigt: –
  - PP +50 `add_political_power`
  - Event: „Januar 1970: Die Troika“ – Breschnew, Kossygin, Podgorny; erklärt Politbüro-Balance, Zusammenhalt der Union und die Startgeister
  - Aktiviert die fünf Länder-Modifier „Der Parteistaat“, „Gosplan – Planwirtschaft“, „Streitkräfte der UdSSR“, „Union der Republiken“ und „Sozialistische Gemeinschaft“ (Startwerte siehe Konzept) `add_dynamic_modifier`
  - _Anmerkung:_ Startknoten wie SOV_reign_of_yeltsin (Kosten 1). Alle anderen Bereiche verlangen ihn per `available` (keine Linien quer durch den Baum).
- **The Lenin Centenary** `COLDWAR_SOV_the_lenin_centenary` · Kosten 3 · hist. · benötigt: the_collective_leadership
  - Stabilität +3 % `add_stability`
  - Communist Party of the Soviet Union +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Der Parteistaat: PP-Gewinn +3 % `COLDWAR_SOV_party_state_modifier`
  - Event: 22. April 1970 – Jubiläumsmedaille, Kundgebungen, die „Leniniana“ im Fernsehen
  - _Anmerkung:_ Die größte Propagandakampagne des Jahrzehnts.
- **Kremlin Politics** `COLDWAR_SOV_kremlin_politics` · Kosten 3 · hist. · benötigt: the_collective_leadership
  - PP +25 `add_political_power`
  - Schaltet Entscheidung frei: Kategorie „Das Politbüro“ (an die Politbüro-Balance gebunden): Reformer stärken, Orthodoxe stärken, Veteranen pensionieren, Regionalkader nach Moskau holen – jede Entscheidung kostet PP und Fraktionsmeinung `unlock_decision_tooltip`
  - _Anmerkung:_ Die Politbüro-Balance existiert ab Spielstart (Init); dieser Fokus öffnet die Werkzeuge, sie zu steuern.
- **The XXIV Party Congress** `COLDWAR_SOV_the_24th_party_congress` · Kosten 5 · hist. · benötigt: the_lenin_centenary · verfügbar: Datum ≥ 01.03.1971
  - PP +75 `add_political_power`
  - Stabilität +2 % `add_stability`
  - Öffnet „The Ninth Five-Year Plan“ (Gosplan) und „The Peace Programme“ (Entspannung) über `available`
  - _Anmerkung:_ 30.03.–09.04.1971: Breschnews Friedensprogramm und der IX. Fünfjahrplan.
- **The Doctrine of Developed Socialism** `COLDWAR_SOV_the_doctrine_of_developed_socialism` · Kosten 5 · hist. · benötigt: the_24th_party_congress
  - Der Parteistaat: Stabilität +2 %, Ideologische Driftabwehr +5 % `COLDWAR_SOV_party_state_modifier`
  - Communist Party of the Soviet Union +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
- **The Gerontocracy Question** `COLDWAR_SOV_the_gerontocracy_question` · Kosten 3 · hist. · benötigt: the_doctrine_of_developed_socialism · verfügbar: Datum ≥ 01.01.1975; hat „Stability of Cadres“
  - PP +25 `add_political_power`
  - Zwei Antworten, gegenseitig exklusiv
  - _Anmerkung:_ Durchschnittsalter des Politbüros 1975: über 65 Jahre. Die wichtigste Strukturentscheidung des Parteistaats.
- **Renew the Cadres** `COLDWAR_SOV_renew_the_cadres` · Kosten 7 · benötigt: the_gerontocracy_question · schließt aus: respect_for_seniority
  - Entfernt „Stability of Cadres“ `remove_ideas`
  - Idee „Cadre Renewal“: Produktivitätswachstum +3 %, Forschung +2 %, Stabilität -3 % (730 Tage `add_timed_idea`)
  - Nomenklatura -15 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
  - Politbüro-Beschluss (reformerisch): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
  - _Anmerkung:_ Ersetzt die Generation von 1964 – kurzfristig Unruhe, langfristig Dynamik.
- **Respect for Seniority** `COLDWAR_SOV_respect_for_seniority` · Kosten 5 · hist. · benötigt: the_gerontocracy_question · schließt aus: renew_the_cadres
  - ersetzt „Stability of Cadres“: Idee „Era of Stagnation“: PP-Gewinn +10 %, Stabilität +5 %, Produktivitätswachstum -8 %, Forschung -3 %, Korruptionskosten +15 %, Bürokratiekosten +15 % (`swap_ideas`)
  - Nomenklatura +10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
  - Politbüro-Beschluss (orthodox): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
  - _Anmerkung:_ Historisch: Zastoi. Bequem für die Partei, teuer für alles andere – kann später nur durch eine Reformführung aufgelöst werden.
- **The 1977 Constitution** `COLDWAR_SOV_the_1977_constitution` · Kosten 5 · hist. · benötigt: the_doctrine_of_developed_socialism · verfügbar: Datum ≥ 01.06.1977
  - Der Parteistaat: PP-Gewinn +5 %, Stabilität +2 % `COLDWAR_SOV_party_state_modifier`
  - Zusammenhalt der Union +4 `COLDWAR_SOV_change_union_cohesion`
  - Event: Die „Breschnew-Verfassung“: Artikel 6 (führende Rolle der Partei) und das „Sowjetvolk“ als neue historische Gemeinschaft
- **Whither the Union?** `COLDWAR_SOV_whither_the_union` · Kosten 3 · hist. · benötigt: the_24th_party_congress
  - PP +25 `add_political_power`
  - Richtungswahl wie GENERIC_station_in_the_world (vier Richtungen; Salafist/Schia gibt es für die UdSSR nicht). Eine weitere Richtung öffnet sich erst, wenn inzwischen eine Partei dieses Outlooks regiert (Muster Ägypten Rev. 7)
- **The Leading Role of the Party** `COLDWAR_SOV_dir_the_leading_role` · Kosten 5 · hist. · benötigt: whither_the_union · verfügbar: Keine andere Richtung erledigt – ODER `has_government = communism` und noch keine Richtung unter dieser Regierung
  - Outlook Emerging +5 % `COLDWAR_SOV_change_outlook_popularity`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
  - Idee „Party Mobilisation“: Kommunistische Drift +0.03, Ideologische Driftabwehr +5 % (365 Tage `add_timed_idea`)
- **The Convergence Memorandum** `COLDWAR_SOV_dir_convergence` · Kosten 5 · benötigt: whither_the_union · verfügbar: Keine andere Richtung erledigt – ODER `has_government = democratic` und noch keine Richtung unter dieser Regierung
  - Outlook Western +5 % `COLDWAR_SOV_change_outlook_popularity`
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Stabilität -3 % `add_stability`
  - Idee „Thaw Atmosphere“: Demokratische Drift +0.03, Forschung +3 % (365 Tage `add_timed_idea`)
  - _Anmerkung:_ Sacharows „Gedanken über Fortschritt, friedliche Koexistenz und geistige Freiheit“ (1968) als offizielle Debatte.
- **A Third Way for Socialism** `COLDWAR_SOV_dir_third_way` · Kosten 5 · benötigt: whither_the_union · verfügbar: Keine andere Richtung erledigt – ODER `has_government = neutrality` und noch keine Richtung unter dieser Regierung
  - Outlook Non-Aligned +5 % `COLDWAR_SOV_change_outlook_popularity`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - Idee „The Third Way Debate“: Blockfreie Drift +0.03, Produktivitätswachstum +2 % (365 Tage `add_timed_idea`)
- **The Russian Idea** `COLDWAR_SOV_dir_the_russian_idea` · Kosten 5 · benötigt: whither_the_union · verfügbar: Keine andere Richtung erledigt – ODER `has_government = nationalist` und noch keine Richtung unter dieser Regierung
  - Outlook Nationalist +5 % `COLDWAR_SOV_change_outlook_popularity`
  - Zusammenhalt der Union -5 `COLDWAR_SOV_change_union_cohesion`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Idee „Russian Revival“: Nationalistische Drift +0.03, Kriegsunterstützung +3 % (365 Tage `add_timed_idea`)
  - _Anmerkung:_ Kostet Zusammenhalt: Nicht-Russen lesen „russisch“ als „Russifizierung“.

### Outlook: Emerging (11)

Oben (über „The Leading Role of the Party“): Emerging-Outlook stärken und Macht an eine andere Emerging-Partei übergeben. Unten: freigeschaltet, sobald eine Emerging-Partei regiert (`has_government = communism`) – zum Start also sofort.

- **The Party of a New Type** `COLDWAR_SOV_em_the_party_of_a_new_type` · Kosten 5 · benötigt: dir_the_leading_role
  - Outlook Emerging +3 % `COLDWAR_SOV_change_outlook_popularity`
  - Der Parteistaat: PP-Gewinn +2 % `COLDWAR_SOV_party_state_modifier`
- **Komsomol Mobilisation** `COLDWAR_SOV_em_komsomol_mobilisation` · Kosten 5 · benötigt: dir_the_leading_role
  - Outlook Emerging +3 % `COLDWAR_SOV_change_outlook_popularity`
  - Stabilität +1 % `add_stability`
  - Mannstärke +10.000 `add_manpower`
- **The Workers' State** `COLDWAR_SOV_em_the_workers_state` · Kosten 5 · benötigt: em_the_party_of_a_new_type, em_komsomol_mobilisation
  - Outlook Emerging +5 % `COLDWAR_SOV_change_outlook_popularity`
  - Gewerkschaften (VTsSPS) +5 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
- **Restore the Party of Lenin** `COLDWAR_SOV_power_the_cpsu` · Kosten 5 · benötigt: em_the_workers_state · verfügbar: Popularität Communist Party of the Soviet Union ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg
  - Regierungspartei → Communist Party of the Soviet Union (Communist State) `change_ruling_party_effect`, Staatschef Leonid Brezhnev `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **All Power to the Councils** `COLDWAR_SOV_power_councils` · Kosten 5 · benötigt: em_the_workers_state · verfügbar: Popularität Free Councils of Labour ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≤ −0,2 (Reformer) oder Gewerkschaften ≥ 70
  - Regierungspartei → Free Councils of Labour (Anarchist Communism) `change_ruling_party_effect`, Staatschef Pyotr Siuda `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The Iron Line Takes Power** `COLDWAR_SOV_power_iron_line` · Kosten 5 · benötigt: em_the_workers_state · verfügbar: Popularität Neo-Stalinist Platform ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≥ 0,4 (Orthodoxe)
  - Regierungspartei → Neo-Stalinist Platform (Emerging Conservative) `change_ruling_party_effect`, Staatschef Sergei Trapeznikov `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The Komsomol Vanguard Takes Power** `COLDWAR_SOV_power_komsomol` · Kosten 5 · benötigt: em_the_workers_state · verfügbar: Popularität Komsomol Vanguard ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≥ 0,3; KGB-Meinung ≥ 60
  - Regierungspartei → Komsomol Vanguard (Emerging Autocracy) `change_ruling_party_effect`, Staatschef Alexander Shelepin `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The Leading Role of the Party** `COLDWAR_SOV_em_the_leading_role_of_the_party` · Kosten 3 · hist. · benötigt: – · verfügbar: `has_government = communism`
  - PP +50 `add_political_power`
  - Idee „Socialist State“: Kommunistische Drift +0.02, Ideologische Abwehr (Cold War) +5 % (`add_ideas`)
  - _Anmerkung:_ Einstieg in den Regierungsteil – kein Richtungsfokus nötig, auch nach Putsch oder Machtübergabe erreichbar.
- **Socialist Emulation** `COLDWAR_SOV_em_socialist_emulation` · Kosten 5 · hist. · benötigt: em_the_leading_role_of_the_party
  - Gosplan – Planwirtschaft: Effizienzzuwachs +3 % `COLDWAR_SOV_gosplan_modifier`
  - Communist Party of the Soviet Union +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
  - _Anmerkung:_ Sozialistischer Wettbewerb der Brigaden.
- **People's Control** `COLDWAR_SOV_em_peoples_control` · Kosten 5 · hist. · benötigt: em_the_leading_role_of_the_party
  - Korruption −1 Stufe `decrease_corruption`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **Peace and Socialism** `COLDWAR_SOV_em_peace_and_socialism` · Kosten 5 · benötigt: em_socialist_emulation, em_peoples_control
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Outlook Emerging +3 % `COLDWAR_SOV_change_outlook_popularity`
  - _Anmerkung:_ Die Prager Zeitschrift der Weltbewegung als Plattform.

### Outlook: Western (11)

Oben (über „The Convergence Memorandum“, Sacharows Konvergenztheorie 1968): Westliches Outlook stärken, Machtübergabe. Unten: freigeschaltet bei `has_government = democratic`.

- **Tolerate the Samizdat Presses** `COLDWAR_SOV_we_the_samizdat_presses` · Kosten 5 · benötigt: dir_convergence
  - Outlook Western +3 % `COLDWAR_SOV_change_outlook_popularity`
  - Stabilität -1 % `add_stability`
- **Stop the Jamming** `COLDWAR_SOV_we_stop_the_jamming` · Kosten 5 · benötigt: dir_convergence
  - Outlook Western +3 % `COLDWAR_SOV_change_outlook_popularity`
  - Sozialistische Gemeinschaft: Handelsmeinung +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Der Parteistaat: Ideologische Driftabwehr -5 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ 1973 wurde das Stören von Voice of America und BBC kurz eingestellt.
- **Recognise the Human Rights Committee** `COLDWAR_SOV_we_recognise_the_human_rights_committee` · Kosten 5 · benötigt: we_the_samizdat_presses, we_stop_the_jamming
  - Outlook Western +5 % `COLDWAR_SOV_change_outlook_popularity`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - KGB -10 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
- **The Systems Men Take Charge** `COLDWAR_SOV_power_systems_men` · Kosten 5 · benötigt: we_recognise_the_human_rights_committee · verfügbar: Popularität Systems Directorate ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≤ −0,4 (Reformer) ODER Stabilität < 30 % · nur Spieler (KI nie)
  - Regierungspartei → Systems Directorate (Western Autocracy) `change_ruling_party_effect`, Staatschef Dzhermen Gvishiani `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - Zusammenhalt der Union -10 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Ein Regimewechsel weg vom Parteistaat: zusätzlich Zusammenhalt −10. Die KI übergibt nie an den Westen.
- **The Solidarists Return** `COLDWAR_SOV_power_solidarists` · Kosten 5 · benötigt: we_recognise_the_human_rights_committee · verfügbar: Popularität People's Labour Union (NTS) ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≤ −0,4 (Reformer) ODER Stabilität < 30 % · nur Spieler (KI nie)
  - Regierungspartei → People's Labour Union (NTS) (Conservatism) `change_ruling_party_effect`, Staatschef Vladimir Poremsky `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - Zusammenhalt der Union -10 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Ein Regimewechsel weg vom Parteistaat: zusätzlich Zusammenhalt −10. Die KI übergibt nie an den Westen.
- **Power to the Human Rights Committee** `COLDWAR_SOV_power_human_rights` · Kosten 5 · benötigt: we_recognise_the_human_rights_committee · verfügbar: Popularität Committee for Human Rights ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≤ −0,4 (Reformer) ODER Stabilität < 30 % · nur Spieler (KI nie)
  - Regierungspartei → Committee for Human Rights (Liberalism) `change_ruling_party_effect`, Staatschef Andrei Sakharov `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - Zusammenhalt der Union -10 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Ein Regimewechsel weg vom Parteistaat: zusätzlich Zusammenhalt −10. Die KI übergibt nie an den Westen.
- **Power to the Democratic Socialists** `COLDWAR_SOV_power_democratic_socialists` · Kosten 5 · benötigt: we_recognise_the_human_rights_committee · verfügbar: Popularität Union of Democratic Socialists ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≤ −0,4 (Reformer) ODER Stabilität < 30 % · nur Spieler (KI nie)
  - Regierungspartei → Union of Democratic Socialists (Socialism) `change_ruling_party_effect`, Staatschef Roy Medvedev `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - Zusammenhalt der Union -10 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Ein Regimewechsel weg vom Parteistaat: zusätzlich Zusammenhalt −10. Die KI übergibt nie an den Westen.
- **A Democratic Union** `COLDWAR_SOV_we_a_democratic_union` · Kosten 3 · benötigt: – · verfügbar: `has_government = democratic`
  - PP +50 `add_political_power`
  - Idee „A Free Union“: Demokratische Drift +0.02, Forschung +3 %, Stabilität -3 % (`add_ideas`)
- **Free Elections** `COLDWAR_SOV_we_free_elections` · Kosten 5 · benötigt: we_a_democratic_union
  - Wahlen erlaubt, Turnus 48 Monate `set_politics`
  - Stabilität -3 % `add_stability`
  - Zusammenhalt der Union -3 `COLDWAR_SOV_change_union_cohesion`
  - Committee for Human Rights +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
- **The Market Returns** `COLDWAR_SOV_we_the_market_returns` · Kosten 5 · benötigt: we_a_democratic_union
  - Handelsgesetz → Gemischte Wirtschaft `add_ideas` (mixed_economy)
  - Gosplan – Planwirtschaft: Produktivitätswachstum +5 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität -3 % `add_stability`
- **Join the Free World** `COLDWAR_SOV_we_join_the_free_world` · Kosten 5 · benötigt: we_free_elections, we_the_market_returns
  - Cold War: Wechsel in den Westblock, nur wenn `mdcw_cw_can_join_west` (PP-frei, Fokus ist die Wahl) `mdcw_cw_change_alignment`
  - Cold-War-Spannung -3 `mdcw_cw_add_tension`

### Outlook: Non-Aligned (15)

Oben (über „A Third Way for Socialism“): Reform außerhalb der Parteilinie, Technokraten, Konservative, Grüne. Unten: freigeschaltet bei `has_government = neutrality`.

- **The Yugoslav Model** `COLDWAR_SOV_na_the_yugoslav_model` · Kosten 5 · benötigt: dir_third_way
  - Outlook Non-Aligned +3 % `COLDWAR_SOV_change_outlook_popularity`
  - Meinung SER +15 `add_opinion_modifier`
  - _Anmerkung:_ Belgrad als Vorbild der Selbstverwaltung.
- **The Technocrats** `COLDWAR_SOV_na_the_technocrats` · Kosten 5 · benötigt: dir_third_way
  - Outlook Non-Aligned +3 % `COLDWAR_SOV_change_outlook_popularity`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +2 % `COLDWAR_SOV_gosplan_modifier`
- **The Village Prose** `COLDWAR_SOV_na_the_village_prose` · Kosten 5 · benötigt: dir_third_way
  - Outlook Non-Aligned +2 % `COLDWAR_SOV_change_outlook_popularity`
  - Live Not by Lies +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
  - _Anmerkung:_ Rasputin, Below, Schukschin – die Dorfprosa als konservative Gegenkultur.
- **The Third Force** `COLDWAR_SOV_na_the_third_force` · Kosten 5 · benötigt: na_the_yugoslav_model, na_the_technocrats oder na_the_village_prose
  - Outlook Non-Aligned +5 % `COLDWAR_SOV_change_outlook_popularity`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
- **The Planners' Government** `COLDWAR_SOV_power_planners` · Kosten 5 · benötigt: na_the_third_force · verfügbar: Popularität Gosplan Technocracy ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance zwischen −0,4 und 0,4
  - Regierungspartei → Gosplan Technocracy (Neutral Autocracy) `change_ruling_party_effect`, Staatschef Nikolai Baibakov `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **Live Not by Lies in Power** `COLDWAR_SOV_power_solzhenitsyn` · Kosten 5 · benötigt: na_the_third_force · verfügbar: Popularität Live Not by Lies ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Stabilität < 45 % ODER Politbüro-Balance ≥ 0,4
  - Regierungspartei → Live Not by Lies (Neutral Conservatism) `change_ruling_party_effect`, Staatschef Aleksandr Solzhenitsyn `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The Directors Take Over** `COLDWAR_SOV_power_directors` · Kosten 5 · benötigt: na_the_third_force · verfügbar: Popularität The Red Directors ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Korruptionsstufe ≥ 6
  - Regierungspartei → The Red Directors (Oligarchism) `change_ruling_party_effect`, Staatschef Nikolai Shchelokov `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The Free Enterprise Cabinet** `COLDWAR_SOV_power_free_enterprise` · Kosten 5 · benötigt: na_the_third_force · verfügbar: Popularität Free Enterprise League ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≤ −0,5 · nur Spieler (KI nie)
  - Regierungspartei → Free Enterprise League (Neutral Libertarian) `change_ruling_party_effect`, Staatschef Nikolai Shmelyov `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The Green Cabinet** `COLDWAR_SOV_power_greens` · Kosten 5 · benötigt: na_the_third_force · verfügbar: Popularität Friends of Baikal ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; `COLDWAR_SOV_aral_disaster` gesetzt ODER `COLDWAR_SOV_rbmk` gesetzt
  - Regierungspartei → Friends of Baikal (Neutral Green) `change_ruling_party_effect`, Staatschef Grigory Galazy `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The Market Socialists Take Power** `COLDWAR_SOV_power_market_socialists` · Kosten 5 · benötigt: na_the_third_force · verfügbar: Popularität Socialist Market Commonwealth ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≤ −0,3
  - Regierungspartei → Socialist Market Commonwealth (Neutral Social) `change_ruling_party_effect`, Staatschef Alexander Yakovlev `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **A Union of Sovereign Republics** `COLDWAR_SOV_power_sovereign_republics` · Kosten 5 · benötigt: na_the_third_force · verfügbar: Popularität Union of Sovereign Republics ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Zusammenhalt der Union < 45
  - Regierungspartei → Union of Sovereign Republics (Neutral Communism) `change_ruling_party_effect`, Staatschef Pyotr Shelest `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - Zusammenhalt der Union -5 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **Neither Moscow nor Washington** `COLDWAR_SOV_na_neither_moscow_nor_washington` · Kosten 3 · benötigt: – · verfügbar: `has_government = neutrality`
  - PP +50 `add_political_power`
  - Idee „Non-Aligned Union“: Blockfreie Drift +0.02, Abwehr fremden Einflusses +5 % (`add_ideas`)
- **The Third Way Economy** `COLDWAR_SOV_na_the_third_way_economy` · Kosten 5 · benötigt: na_neither_moscow_nor_washington
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 %, Handelsmeinung +5 % `COLDWAR_SOV_gosplan_modifier`
- **Dissolve the Warsaw Pact?** `COLDWAR_SOV_na_dissolve_the_pact` · Kosten 5 · benötigt: na_neither_moscow_nor_washington · nur Spieler (KI nie)
  - Löst unsere Fraktion auf, Mitglieder werden über Event informiert und entscheiden selbst über neue Bündnisse `dismantle_faction`
  - Cold-War-Spannung -3 `mdcw_cw_add_tension`
  - Zusammenhalt der Union -5 `COLDWAR_SOV_change_union_cohesion`
- **Join the Non-Aligned Movement** `COLDWAR_SOV_na_join_the_movement` · Kosten 5 · benötigt: na_the_third_way_economy, na_dissolve_the_pact
  - Cold War: Wechsel zu den Blockfreien (PP-frei, Fokus ist die Wahl) `mdcw_cw_change_alignment`
  - Meinung RAJ +20 `add_opinion_modifier`

### Outlook: Nationalist (11)

Oben (über „The Russian Idea“): Russische Partei, Marschälle, Romanows. Kostet den Zusammenhalt der Union. Unten: freigeschaltet bei `has_government = nationalist`.

- **Molodaya Gvardiya** `COLDWAR_SOV_nt_molodaya_gvardiya` · Kosten 5 · benötigt: dir_the_russian_idea
  - Outlook Nationalist +3 % `COLDWAR_SOV_change_outlook_popularity`
  - Zusammenhalt der Union -2 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Die Zeitschrift der „Russischen Partei“ im Komsomol-Verlag.
- **The Cult of Victory** `COLDWAR_SOV_nt_the_victory_cult` · Kosten 5 · hist. · benötigt: dir_the_russian_idea
  - Outlook Nationalist +2 % `COLDWAR_SOV_change_outlook_popularity`
  - Kriegsunterstützung +3 % `add_war_support`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - _Anmerkung:_ Mamajew-Kurgan, Ewige Flammen, der 9. Mai als Staatsreligion.
- **Vozrozhdenie** `COLDWAR_SOV_nt_vozrozhdenie` · Kosten 5 · benötigt: nt_molodaya_gvardiya, nt_the_victory_cult
  - Outlook Nationalist +5 % `COLDWAR_SOV_change_outlook_popularity`
  - Zusammenhalt der Union -3 `COLDWAR_SOV_change_union_cohesion`
- **The Russian Party Takes Power** `COLDWAR_SOV_power_russian_party` · Kosten 5 · benötigt: nt_vozrozhdenie · verfügbar: Popularität The Russian Party ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Politbüro-Balance ≥ 0,2
  - Regierungspartei → The Russian Party (Nationalist Populism) `change_ruling_party_effect`, Staatschef Dmitry Polyansky `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - Zusammenhalt der Union -8 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The National Rebirth** `COLDWAR_SOV_power_national_rebirth` · Kosten 5 · benötigt: nt_vozrozhdenie · verfügbar: Popularität Committee of National Rebirth ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; nur Spieler; Stabilität < 30 % · nur Spieler (KI nie)
  - Regierungspartei → Committee of National Rebirth (Nationalist Fascism) `change_ruling_party_effect`, Staatschef Committee of National Rebirth `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - Zusammenhalt der Union -8 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The Marshals Step In** `COLDWAR_SOV_power_marshals` · Kosten 5 · benötigt: nt_vozrozhdenie · verfügbar: Popularität Council of Marshals ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; Armee-Meinung ≥ 75 ODER Stabilität < 25 %
  - Regierungspartei → Council of Marshals (Military Junta) `change_ruling_party_effect`, Staatschef Andrei Grechko `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - Zusammenhalt der Union -8 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **The Return of the Romanovs** `COLDWAR_SOV_power_romanovs` · Kosten 5 · benötigt: nt_vozrozhdenie · verfügbar: Popularität House of Romanov ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg; nur Spieler; „Accord with the Patriarchate“ erledigt · nur Spieler (KI nie)
  - Regierungspartei → House of Romanov (Monarchism) `change_ruling_party_effect`, Staatschef Grand Duke Vladimir Kirillovich `create_country_leader`
  - Idee „Transition of Power“: Stabilität -10 %, PP-Gewinn -15 % (180 Tage `add_timed_idea`)
  - Zusammenhalt der Union -8 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.
- **Russia First** `COLDWAR_SOV_nt_russia_first` · Kosten 3 · benötigt: – · verfügbar: `has_government = nationalist`
  - PP +50 `add_political_power`
  - Idee „Russia First“: Nationalistische Drift +0.02, Kriegsunterstützung +5 % (`add_ideas`)
  - Zusammenhalt der Union -5 `COLDWAR_SOV_change_union_cohesion`
- **Institutions for the RSFSR** `COLDWAR_SOV_nt_the_rsfsr_institutions` · Kosten 5 · benötigt: nt_russia_first
  - Der Parteistaat: PP-Gewinn +3 % `COLDWAR_SOV_party_state_modifier`
  - Zusammenhalt der Union -3 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Russland bekommt, was jede andere Republik hat: eigene Partei, Akademie, KGB.
- **The Army of the Nation** `COLDWAR_SOV_nt_the_army_of_the_nation` · Kosten 5 · benötigt: nt_russia_first
  - Streitkräfte der UdSSR: Moral (Heer) +5 % `COLDWAR_SOV_armed_forces_modifier`
  - Kriegsunterstützung +3 % `add_war_support`
- **The Imperial Question** `COLDWAR_SOV_nt_the_imperial_question` · Kosten 5 · benötigt: nt_the_rsfsr_institutions, nt_the_army_of_the_nation
  - Im Event: Union halten (Zusammenhalt +5, Polizeikosten +10 %) oder kleinere russische Union (Republiken dürfen per Angebot austreten)

### KPdSU: Partei Lenins (7)

Partei 4 (Communist State). Gemeinsamer Parteibaum für jeden Generalsekretär: Nomenklatura, Komsomol, Parteibuchumtausch, Artikel 6.

- **The Party of Lenin** `COLDWAR_SOV_cpsu_the_party_of_lenin` · Kosten 3 · hist. · benötigt: power_the_cpsu oder em_the_leading_role_of_the_party · verfügbar: `emerging_communist_state_are_in_power`
  - PP +50 `add_political_power`
  - Programm „The Party of Lenin“: PP-Gewinn +5 %, Stabilität +3 %, Kommunistische Drift +0.02, Ideologische Abwehr (Cold War) +5 % `COLDWAR_SOV_cpsu_programme`
  - _Anmerkung:_ Programm-Modifier wie SOV_putin_politic_modifier; entfällt per `remove_trigger`, wenn die KPdSU nicht mehr regiert.
- **The Nomenklatura** `COLDWAR_SOV_cpsu_the_nomenklatura` · Kosten 5 · hist. · benötigt: cpsu_the_party_of_lenin
  - Nomenklatura +10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Programm „The Party of Lenin“: Bürokratiekosten +3 %, PP-Gewinn +2 % `COLDWAR_SOV_cpsu_programme`
- **The Komsomol** `COLDWAR_SOV_cpsu_the_komsomol` · Kosten 5 · hist. · benötigt: cpsu_the_party_of_lenin
  - Communist Party of the Soviet Union +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Programm „The Party of Lenin“: Kriegsunterstützung +2 % `COLDWAR_SOV_cpsu_programme`
  - Mannstärke +10.000 `add_manpower`
- **The Party Card Exchange** `COLDWAR_SOV_cpsu_the_party_card_exchange` · Kosten 5 · hist. · benötigt: cpsu_the_nomenklatura
  - PP +50 `add_political_power`
  - Stabilität +2 % `add_stability`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Korruption −1 Stufe `decrease_corruption`
  - _Anmerkung:_ 1973–1974: Austausch der Parteibücher – eine stille Säuberung.
- **Democratic Centralism** `COLDWAR_SOV_cpsu_democratic_centralism` · Kosten 5 · hist. · benötigt: cpsu_the_komsomol
  - Programm „The Party of Lenin“: Ideologische Driftabwehr +5 % `COLDWAR_SOV_cpsu_programme`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
- **Article Six** `COLDWAR_SOV_cpsu_the_constitution_of_developed_socialism` · Kosten 5 · hist. · benötigt: cpsu_the_party_card_exchange, cpsu_democratic_centralism
  - Programm „The Party of Lenin“: Stabilität +2 %, PP-Gewinn +3 % `COLDWAR_SOV_cpsu_programme`
  - _Anmerkung:_ „Die führende und lenkende Kraft der sowjetischen Gesellschaft …“
- **The Party of the Whole People** `COLDWAR_SOV_cpsu_the_party_of_the_whole_people` · Kosten 7 · hist. · benötigt: cpsu_the_constitution_of_developed_socialism
  - Communist Party of the Soviet Union +5 % Popularität (Outlook +5 %) `change_relative_party_popularity`
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
  - Programm „The Party of Lenin“: Kommunistische Drift +0.02 `COLDWAR_SOV_cpsu_programme`

### Das Politbüro: Machtwechsel (11)

Kein Generalsekretär schließt einen anderen aus. Breschnew regiert zum Start. Jeder Politbüro-Fokus baut eine Kandidatur auf und öffnet die Entscheidung „Convene the Plenum“: Das Politbüro stimmt ab (Generalsekretär 1 Stimme, Moskauer Block 7 nach der Balance, die 3 Republiksitze). Mehrheit setzt den Kandidaten ein, auch mitten in einem anderen Baum. Der Baum eines Generalsekretärs ist nur offen, solange er regiert (`COLDWAR_SOV_gensec_<name>`); Erledigtes bleibt, sein Programm-Modifier fällt beim Wechsel weg. Stirbt ein Generalsekretär, wird der in seinem Baum gewählte Erbe zur Abstimmung gestellt.

- **The Politburo** `COLDWAR_SOV_ple_the_politburo` · Kosten 1 · hist. · benötigt: – · verfügbar: `emerging_communist_state_are_in_power`
  - PP +25 `add_political_power`
  - Breschnew ist zum Start Generalsekretär (`COLDWAR_SOV_gensec_bre` aus dem Init). Die Politbüro-Fokusse unten schließen sich nicht aus: jeder baut eine Kandidatur auf; gewählt wird im Plenum, in dem auch die 3 Republiksitze abstimmen.
  - _Anmerkung:_ Muster wie die „Power to X“-Fokusse in Ägypten Rev. 7: jeder Wechsel einmal, nie gegenseitig gesperrt. Die KI wechselt nur über die historischen Todesfälle.
- **The Premier's Plenum** `COLDWAR_SOV_ple_kos` · Kosten 5 · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist nicht Generalsekretär; Datum < 18.12.1980 (Tod Kossygins); Politbüro-Balance ≤ −0,15 ODER „Deepen the Kosygin Reform“/„OGAS: Cybernetic Planning“ erledigt; Branchenministerien ≥ 40; Stabilität ≥ 40 %
  - Schaltet Entscheidung frei: „Convene the Plenum: Alexei Kossygin“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung reformerisch, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Alexei Kossygin; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_kos`) `COLDWAR_SOV_install_gensec`; Traits „Economist-Premier“ `COLDWAR_SOV_economist_premier`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - Branchenministerien +10 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Alt-Hist. Die Kandidatur kann jederzeit aufgebaut werden, auch wenn ein anderer Generalsekretär seinen Baum halb fertig hat; entscheiden muss das Politbüro.
- **The Presidium Takes the Lead** `COLDWAR_SOV_ple_pod` · Kosten 5 · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist nicht Generalsekretär; Datum < 12.01.1983; Stabilität ≥ 50 %; Zusammenhalt der Union ≥ 50
  - Schaltet Entscheidung frei: „Convene the Plenum: Nikolai Podgorny“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung neutral, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Nikolai Podgorny; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_pod`) `COLDWAR_SOV_install_gensec`; Traits „Head of State“ `COLDWAR_SOV_head_of_state`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Alt-Hist. Die Kandidatur kann jederzeit aufgebaut werden, auch wenn ein anderer Generalsekretär seinen Baum halb fertig hat; entscheiden muss das Politbüro.
- **The Grey Cardinal Steps Forward** `COLDWAR_SOV_ple_sus` · Kosten 5 · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist nicht Generalsekretär; Datum < 25.01.1982; Nomenklatura ≥ 60; Politbüro-Balance ≥ 0
  - Schaltet Entscheidung frei: „Convene the Plenum: Michail Suslow“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung orthodox, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Michail Suslow; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_sus`) `COLDWAR_SOV_install_gensec`; Traits „Chief Ideologue“ `COLDWAR_SOV_chief_ideologue`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - Nomenklatura +5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Alt-Hist. Die Kandidatur kann jederzeit aufgebaut werden, auch wenn ein anderer Generalsekretär seinen Baum halb fertig hat; entscheiden muss das Politbüro.
- **Iron Shurik's Return** `COLDWAR_SOV_ple_she` · Kosten 5 · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist nicht Generalsekretär; Datum < 16.04.1975 (danach nicht mehr im Politbüro); Gewerkschaften ≥ 55; KGB ≥ 50; Politbüro-Balance ≥ 0,25
  - Schaltet Entscheidung frei: „Convene the Plenum: Alexander Schelepin“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung orthodox, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Alexander Schelepin; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_she`) `COLDWAR_SOV_install_gensec`; Traits „Iron Shurik“ `COLDWAR_SOV_iron_shurik`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - Gewerkschaften (VTsSPS) +10 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
  - Nomenklatura -15 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance +0.10 Richtung Orthodoxe `add_power_balance_value`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Alt-Hist. Die Kandidatur kann jederzeit aufgebaut werden, auch wenn ein anderer Generalsekretär seinen Baum halb fertig hat; entscheiden muss das Politbüro.
- **The Chekist Plenum** `COLDWAR_SOV_ple_and` · Kosten 5 · hist. · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist nicht Generalsekretär; Datum ≥ 27.04.1973 und < 09.02.1984; KGB ≥ 70
  - Schaltet Entscheidung frei: „Convene the Plenum: Juri Andropow“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung neutral, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Juri Andropow; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_and`) `COLDWAR_SOV_install_gensec`; Traits „Chekist“ `COLDWAR_SOV_chekist`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - KGB +10 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Historisch: Andropow folgt Breschnew im November 1982.
- **The Marshal's Hour** `COLDWAR_SOV_ple_gre` · Kosten 5 · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist nicht Generalsekretär; Datum ≥ 27.04.1973 und < 26.04.1976; Armee ≥ 75; Cold-War-Spannung ≥ 55 ODER im Krieg ODER Politbüro-Balance ≥ 0,4
  - Schaltet Entscheidung frei: „Convene the Plenum: Andrei Gretschko“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung orthodox, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Andrei Gretschko; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_gre`) `COLDWAR_SOV_install_gensec`; Traits „Marshal of the Soviet Union“ `COLDWAR_SOV_marshal_of_the_soviet_union`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - Armee & Generalstab +15 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance +0.10 Richtung Orthodoxe `add_power_balance_value`
  - Kriegsunterstützung +3 % `add_war_support`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Alt-Hist. Die Kandidatur kann jederzeit aufgebaut werden, auch wenn ein anderer Generalsekretär seinen Baum halb fertig hat; entscheiden muss das Politbüro.
- **The Armourer's Plenum** `COLDWAR_SOV_ple_ust` · Kosten 5 · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist nicht Generalsekretär; Datum ≥ 05.03.1976 und < 20.12.1984; Rüstungskomplex ≥ 80; Armee ≥ 60
  - Schaltet Entscheidung frei: „Convene the Plenum: Dmitri Ustinow“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung orthodox, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Dmitri Ustinow; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_ust`) `COLDWAR_SOV_install_gensec`; Traits „The Armourer“ `COLDWAR_SOV_the_armourer`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - Rüstungskomplex (VPK) +15 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Alt-Hist. Die Kandidatur kann jederzeit aufgebaut werden, auch wenn ein anderer Generalsekretär seinen Baum halb fertig hat; entscheiden muss das Politbüro.
- **The Leningrad Plenum** `COLDWAR_SOV_ple_gro` · Kosten 5 · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist nicht Generalsekretär; Datum ≥ 05.03.1976; Politbüro-Balance ≥ 0,15; Branchenministerien ≥ 50; Nomenklatura ≥ 50
  - Schaltet Entscheidung frei: „Convene the Plenum: Grigori Romanow“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung orthodox, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Grigori Romanow; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_gro`) `COLDWAR_SOV_install_gensec`; Traits „Leningrad Boss“ `COLDWAR_SOV_leningrad_boss`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - Branchenministerien +5 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
  - Politbüro-Balance +0.10 Richtung Orthodoxe `add_power_balance_value`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Alt-Hist. Die Kandidatur kann jederzeit aufgebaut werden, auch wenn ein anderer Generalsekretär seinen Baum halb fertig hat; entscheiden muss das Politbüro.
- **The Apparatchik's Plenum** `COLDWAR_SOV_ple_che` · Kosten 5 · hist. · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist nicht Generalsekretär; Datum ≥ 27.11.1978 und < 10.03.1985; Nomenklatura ≥ 70
  - Schaltet Entscheidung frei: „Convene the Plenum: Konstantin Tschernenko“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung orthodox, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Konstantin Tschernenko; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_che`) `COLDWAR_SOV_install_gensec`; Traits „Apparatchik“ `COLDWAR_SOV_apparatchik`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - Nomenklatura +10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Gosplan – Planwirtschaft: Produktivitätswachstum -1 % `COLDWAR_SOV_gosplan_modifier`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Historisch: Tschernenko folgt Andropow im Februar 1984.
- **The New Generation** `COLDWAR_SOV_ple_gor` · Kosten 5 · hist. · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist nicht Generalsekretär; Datum ≥ 21.10.1980; Politbüro-Balance ≤ −0,2 ODER „Renew the Cadres“ erledigt
  - Schaltet Entscheidung frei: „Convene the Plenum: Michail Gorbatschow“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag; Bedingungen wie oben): Abstimmung im Politbüro, Richtung reformerisch, die 3 Republiksitze stimmen mit `unlock_decision_tooltip`
  - Bei Mehrheit (verbindlich):
  - Neuer Generalsekretär: Michail Gorbatschow; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg (Flag `COLDWAR_SOV_gensec_gor`) `COLDWAR_SOV_install_gensec`; Traits „The New Generation“ `COLDWAR_SOV_new_generation`
  - Stabilität -5 % `add_stability`
  - Idee „Plenum Shake-up“: Stabilität -5 %, PP-Gewinn -10 % (120 Tage `add_timed_idea`)
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
  - Ohne Mehrheit: kein Wechsel, Stabilität −3 %, Politbüro-Balance 0,05 gegen den Kandidaten
  - _Anmerkung:_ Historisch: Gorbatschow folgt Tschernenko im März 1985.

### Generalsekretär: Leonid Breschnew (40)

Start-Generalsekretär (1964–1982). Stabilität der Kader, Entspannung aus der Stärke oder Breschnew-Doktrin, Konsum, Rüstung oder Öl, Personenkult, Gesundheit und Nachfolge.

- **Dear Leonid Ilyich** `COLDWAR_SOV_bre_dear_leonid_ilyich` · Kosten 3 · hist. · benötigt: ple_the_politburo · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Programm „Brezhnev's Course“: PP-Gewinn +5 %, Stabilität +3 % `COLDWAR_SOV_bre_programme`
  - Nomenklatura +5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **The Dnepropetrovsk Clan** `COLDWAR_SOV_bre_the_dnepropetrovsk_clan` · Kosten 5 · hist. · benötigt: bre_dear_leonid_ilyich · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Programm „Brezhnev's Course“: PP-Gewinn +3 %, Korruptionskosten +5 % `COLDWAR_SOV_bre_programme`
  - Nomenklatura +5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ Kirilenko (Zweiter Sekretär), Schtscholokow (MWD), Tichonow (Ministerrat) – die Seilschaft aus Dnipropetrowsk.
- **The General Department** `COLDWAR_SOV_bre_the_general_department` · Kosten 5 · hist. · benötigt: bre_dear_leonid_ilyich · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Der Parteistaat: Bürokratiekosten -5 % `COLDWAR_SOV_party_state_modifier`
  - Programm „Brezhnev's Course“: PP-Gewinn +2 % `COLDWAR_SOV_bre_programme`
  - _Anmerkung:_ Tschernenkos Allgemeine Abteilung: jedes Papier des Politbüros läuft über sie.
- **Balance the Troika** `COLDWAR_SOV_bre_balance_the_troika` · Kosten 5 · hist. · benötigt: bre_dear_leonid_ilyich · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Stabilität +2 % `add_stability`
  - Politbüro-Balance 0,10 Richtung Mitte `add_power_balance_value`
- **Detente or Doctrine?** `COLDWAR_SOV_bre_the_first_choice` · Kosten 3 · hist. · benötigt: bre_the_dnepropetrovsk_clan, bre_balance_the_troika · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Außenpolitische Weiche – gegenseitig exklusiv
- **Detente from Strength** `COLDWAR_SOV_bre_detente_from_strength` · Kosten 5 · hist. · benötigt: bre_the_first_choice · schließt aus: bre_the_doctrine_hawk · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Programm „Brezhnev's Course“: Handelsmeinung +10 % `COLDWAR_SOV_bre_programme`
  - Cold-War-Spannung -1 `mdcw_cw_add_tension`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
- **The Crimean Talks** `COLDWAR_SOV_bre_the_crimean_talks` · Kosten 5 · hist. · benötigt: bre_detente_from_strength · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Meinung GER +15 `add_opinion_modifier`
  - Sozialistische Gemeinschaft: Handelsmeinung +5 % `COLDWAR_SOV_commonwealth_modifier`
  - _Anmerkung:_ Oreanda, September 1971: Breschnew und Brandt.
- **Brezhnev in Washington** `COLDWAR_SOV_bre_brezhnev_in_washington` · Kosten 5 · hist. · benötigt: bre_the_crimean_talks · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`); Datum ≥ 01.06.1973
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Abkommen zur Verhütung von Atomkriegen. Bei Annahme: Spannung −2, Meinung +15 `COLDWAR_SOV_offer_brezhnev_visit`
  - Stabilität +2 % `add_stability`
- **The Helsinki Triumph** `COLDWAR_SOV_bre_the_helsinki_triumph` · Kosten 5 · hist. · benötigt: bre_brezhnev_in_washington · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`); „The Helsinki Conference“ erledigt
  - Stabilität +3 % `add_stability`
  - Programm „Brezhnev's Course“: PP-Gewinn +3 % `COLDWAR_SOV_bre_programme`
  - Communist Party of the Soviet Union +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - _Anmerkung:_ Die Grenzen von 1945 sind anerkannt – Breschnews größter Erfolg.
- **The Doctrine Hawk** `COLDWAR_SOV_bre_the_doctrine_hawk` · Kosten 5 · benötigt: bre_the_first_choice · schließt aus: bre_detente_from_strength · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Programm „Brezhnev's Course“: Kriegsunterstützung +3 %, Ideologische Abwehr (Cold War) +10 % `COLDWAR_SOV_bre_programme`
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
  - Politbüro-Balance +0.10 Richtung Orthodoxe `add_power_balance_value`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **The Iron Bloc** `COLDWAR_SOV_bre_the_iron_bloc` · Kosten 5 · benötigt: bre_the_doctrine_hawk · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Sozialistische Gemeinschaft: Auslandseinfluss +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Streitkräfte der UdSSR: Organisation (Heer) +2 % `COLDWAR_SOV_armed_forces_modifier`
- **Answer Every Challenge** `COLDWAR_SOV_bre_answer_every_challenge` · Kosten 5 · benötigt: bre_the_iron_bloc · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Streitkräfte der UdSSR: Ausrüstungskosten -3 % `COLDWAR_SOV_armed_forces_modifier`
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
- **The Internationalist Duty** `COLDWAR_SOV_bre_the_internationalist_duty` · Kosten 5 · benötigt: bre_answer_every_challenge · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +10 %, Freiwilligen-Kontingent +1 `COLDWAR_SOV_commonwealth_modifier`
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
- **The Tula Speech** `COLDWAR_SOV_bre_the_tula_speech` · Kosten 5 · hist. · benötigt: bre_the_helsinki_triumph oder bre_the_internationalist_duty · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`); Datum ≥ 01.01.1977
  - Cold-War-Spannung -2 `mdcw_cw_add_tension`
  - Armee & Generalstab -5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Stabilität +2 % `add_stability`
  - _Anmerkung:_ Januar 1977: „Wir streben nicht nach Überlegenheit.“
- **Butter, Guns or Oil?** `COLDWAR_SOV_bre_the_second_choice` · Kosten 3 · hist. · benötigt: bre_the_general_department · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Wirtschaftsweiche – gegenseitig exklusiv
- **Consumer Socialism** `COLDWAR_SOV_bre_consumer_socialism` · Kosten 5 · hist. · benötigt: bre_the_second_choice · schließt aus: bre_guns_before_butter, bre_the_oil_bet · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Programm „Brezhnev's Course“: Konsumgüter -3 %, Stabilität +2 % `COLDWAR_SOV_bre_programme`
  - Gosplan – Planwirtschaft: Sozialkosten +3 % `COLDWAR_SOV_gosplan_modifier`
- **The Little Deal** `COLDWAR_SOV_bre_the_little_deal` · Kosten 5 · hist. · benötigt: bre_consumer_socialism · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - ersetzt „The Second Economy“: Idee „The Little Deal“: Stabilität +4 %, Steuereinnahmen -2 %, Korruptionskosten +5 % (`swap_ideas`)
  - _Anmerkung:_ James Millars „kleiner Deal“: der Staat duldet Nebengeschäfte, die Bürger dulden den Staat.
- **A Flat for Every Family** `COLDWAR_SOV_bre_a_flat_for_every_family` · Kosten 7 · hist. · benötigt: bre_the_little_deal · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Gebäude: Infrastruktur `one_random_infrastructure`, Kosten 0.6 % BIP statt MD-Pauschale (`skip_payment`)
  - Stabilität +3 % `add_stability`
  - Gosplan – Planwirtschaft: Sozialkosten +2 % `COLDWAR_SOV_gosplan_modifier`
- **Guns before Butter** `COLDWAR_SOV_bre_guns_before_butter` · Kosten 5 · benötigt: bre_the_second_choice · schließt aus: bre_consumer_socialism, bre_the_oil_bet · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Programm „Brezhnev's Course“: Steuer Rüstungsindustrie +5 %, Konsumgüter +3 % `COLDWAR_SOV_bre_programme`
  - Rüstungskomplex (VPK) +10 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
- **The Military-Industrial Commission** `COLDWAR_SOV_bre_the_military_industrial_commission` · Kosten 5 · benötigt: bre_guns_before_butter · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Gebäude: Rüstungsfabriken `two_random_arms_factory`, Kosten 1.2 % BIP statt MD-Pauschale (`skip_payment`)
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
- **The Tank Parks** `COLDWAR_SOV_bre_the_tank_parks` · Kosten 5 · benötigt: bre_the_military_industrial_commission · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Streitkräfte der UdSSR: Ausrüstungskosten -3 % `COLDWAR_SOV_armed_forces_modifier`
  - Forschungsbonus CAT_main_battle_tanks +50 % ×1 `add_tech_bonus`
- **The Oil Bet** `COLDWAR_SOV_bre_the_oil_bet` · Kosten 5 · benötigt: bre_the_second_choice · schließt aus: bre_consumer_socialism, bre_guns_before_butter · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Programm „Brezhnev's Course“: Öl-Exporterlöse +8 % `COLDWAR_SOV_bre_programme`
  - Gosplan – Planwirtschaft: Produktivitätswachstum -2 % `COLDWAR_SOV_gosplan_modifier`
- **Oil for Grain** `COLDWAR_SOV_bre_oil_for_grain` · Kosten 5 · benötigt: bre_the_oil_bet · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Einnahme +0.5 % BIP `COLDWAR_SOV_receive_gdp_share`
  - Gosplan – Planwirtschaft: Agrarproduktivität +2 % `COLDWAR_SOV_gosplan_modifier`
- **Pipelines to Europe** `COLDWAR_SOV_bre_pipelines_to_europe` · Kosten 5 · benötigt: bre_oil_for_grain · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Angebot an GER, ITA, FRA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Langfristige Gaslieferverträge. Bei Annahme: Partner Energie +5 %, wir Öl-Exporterlöse +5 %, Meinung +10 `COLDWAR_SOV_offer_pipelines_to_europe`
- **Andropov or Shchelokov?** `COLDWAR_SOV_bre_kgb_or_mvd` · Kosten 3 · hist. · benötigt: bre_the_general_department · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Wer hält die Ordnung? Gegenseitig exklusiv
- **Back the KGB** `COLDWAR_SOV_bre_back_the_kgb` · Kosten 5 · benötigt: bre_kgb_or_mvd · schließt aus: bre_back_the_mvd · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - KGB +10 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - Der Parteistaat: Korruptionskosten -5 % `COLDWAR_SOV_party_state_modifier`
  - Korruption −1 Stufe `decrease_corruption`
- **Back the MVD** `COLDWAR_SOV_bre_back_the_mvd` · Kosten 5 · hist. · benötigt: bre_kgb_or_mvd · schließt aus: bre_back_the_kgb · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Stabilität +2 % `add_stability`
  - Der Parteistaat: Polizeikosten -5 %, Korruptionskosten +5 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Schtscholokows Miliz – loyal, bequem, korrupt.
- **Trust in the Republican Cadres** `COLDWAR_SOV_bre_trust_the_republics` · Kosten 5 · hist. · benötigt: bre_back_the_kgb oder bre_back_the_mvd · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Zusammenhalt der Union +5 `COLDWAR_SOV_change_union_cohesion`
  - Der Parteistaat: Korruptionskosten +3 % `COLDWAR_SOV_party_state_modifier`
- **Malaya Zemlya** `COLDWAR_SOV_bre_malaya_zemlya` · Kosten 5 · hist. · benötigt: bre_dear_leonid_ilyich · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`); Datum ≥ 01.01.1976
  - Programm „Brezhnev's Course“: PP-Gewinn +5 % `COLDWAR_SOV_bre_programme`
  - Der Parteistaat: Forschung -1 % `COLDWAR_SOV_party_state_modifier`
  - Staatschef erhält Trait „Four Times Hero“ `add_country_leader_trait`
  - _Anmerkung:_ Memoiren, Orden, Marschallstab – der Personenkult der Spätzeit.
- **Marshal Brezhnev** `COLDWAR_SOV_bre_marshal_brezhnev` · Kosten 3 · hist. · benötigt: bre_malaya_zemlya · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`); Datum ≥ 01.05.1976
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - PP +25 `add_political_power`
- **Chairman of the Presidium** `COLDWAR_SOV_bre_chairman_of_the_presidium` · Kosten 5 · hist. · benötigt: bre_marshal_brezhnev · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`); Datum ≥ 01.05.1977
  - PP +75 `add_political_power`
  - Programm „Brezhnev's Course“: PP-Gewinn +3 % `COLDWAR_SOV_bre_programme`
  - Nomenklatura +5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ Juni 1977: Podgorny wird abgesetzt.
- **The General Secretary's Health** `COLDWAR_SOV_bre_the_leaders_health` · Kosten 3 · hist. · benötigt: bre_chairman_of_the_presidium · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`); Datum ≥ 01.01.1978
  - Gegenseitig exklusiv
- **The Kremlin Doctors** `COLDWAR_SOV_bre_the_kremlin_doctors` · Kosten 5 · hist. · benötigt: bre_the_leaders_health · schließt aus: bre_a_dignified_retirement · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Staatschef erhält Trait „Ailing Leader“ `add_country_leader_trait`
  - Programm „Brezhnev's Course“: PP-Gewinn -5 %, Stabilität +2 % `COLDWAR_SOV_bre_programme`
  - _Anmerkung:_ Jewgeni Tschasow und die 4. Hauptverwaltung halten ihn bis 1982 im Amt.
- **A Dignified Retirement** `COLDWAR_SOV_bre_a_dignified_retirement` · Kosten 5 · benötigt: bre_the_leaders_health · schließt aus: bre_the_kremlin_doctors · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Stabilität -3 % `add_stability`
  - PP +100 `add_political_power`
  - Breschnew kündigt den Rücktritt an: der danach gewählte Erbe übernimmt sofort, ohne auf das Todes-Event zu warten (`COLDWAR_SOV_bre_retiring`)
  - _Anmerkung:_ Breschnew bat 1979 tatsächlich darum, gehen zu dürfen.
- **The Succession** `COLDWAR_SOV_bre_the_succession` · Kosten 3 · hist. · benötigt: bre_the_kremlin_doctors oder bre_a_dignified_retirement · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Wer folgt Breschnew? Gegenseitig exklusiv
- **Heir: Andropov** `COLDWAR_SOV_bre_heir_andropov` · Kosten 5 · hist. · benötigt: bre_the_succession · schließt aus: bre_heir_chernenko, bre_heir_romanov, bre_heir_gorbachev · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Erbe festgelegt: Andropov übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_and`, Event setzt den Politbüro-Fokus um)
  - Korruption −1 Stufe `decrease_corruption`
  - KGB +10 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
- **Heir: Chernenko** `COLDWAR_SOV_bre_heir_chernenko` · Kosten 5 · benötigt: bre_the_succession · schließt aus: bre_heir_andropov, bre_heir_romanov, bre_heir_gorbachev · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Erbe festgelegt: Chernenko übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_che`, Event setzt den Politbüro-Fokus um)
  - Stabilität +3 % `add_stability`
  - Nomenklatura +10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **Heir: Romanov** `COLDWAR_SOV_bre_heir_romanov` · Kosten 5 · benötigt: bre_the_succession · schließt aus: bre_heir_andropov, bre_heir_chernenko, bre_heir_gorbachev · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Erbe festgelegt: Romanov übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_gro`, Event setzt den Politbüro-Fokus um)
  - Politbüro-Balance +0.10 Richtung Orthodoxe `add_power_balance_value`
- **Heir: An Early Gorbachev** `COLDWAR_SOV_bre_heir_gorbachev` · Kosten 5 · benötigt: bre_the_succession · schließt aus: bre_heir_andropov, bre_heir_chernenko, bre_heir_romanov · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Erbe festgelegt: An Early Gorbachev übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_gor`, Event setzt den Politbüro-Fokus um)
  - Politbüro-Balance -0.15 Richtung Reformer `add_power_balance_value`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **Developed Socialism Achieved** `COLDWAR_SOV_bre_developed_socialism_achieved` · Kosten 7 · hist. · benötigt: bre_the_tula_speech, bre_a_flat_for_every_family oder bre_the_tank_parks oder bre_pipelines_to_europe, bre_trust_the_republics · verfügbar: `emerging_communist_state_are_in_power`; Leonid Breschnew ist Generalsekretär (`COLDWAR_SOV_gensec_bre`)
  - Idee „Developed Socialism“: Stabilität +5 %, PP-Gewinn +5 %, Produktivitätswachstum -2 % (`add_ideas`)
  - Programm „Brezhnev's Course“: Stabilität +2 % `COLDWAR_SOV_bre_programme`
  - _Anmerkung:_ Abschluss: braucht Außen-, Wirtschafts- und Sicherheitsweiche.

### Generalsekretär: Alexei Kossygin (30)

Der Premier (bis 1980). Marktsozialismus, kybernetische Planung oder Reform im Plan; Kampf mit dem Parteiapparat, Handel statt Panzer, Tashkent-Diplomatie.

- **The Premier Takes the Party** `COLDWAR_SOV_kos_the_premier_takes_the_party` · Kosten 3 · benötigt: ple_kos · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Programm „Kosygin's Reform Course“: Produktivitätswachstum +5 %, Forschung +2 %, PP-Gewinn -3 % `COLDWAR_SOV_kos_programme`
- **Baibakov at Gosplan** `COLDWAR_SOV_kos_baibakov_at_gosplan` · Kosten 5 · benötigt: kos_the_premier_takes_the_party · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Gosplan – Planwirtschaft: Effizienzzuwachs +3 % `COLDWAR_SOV_gosplan_modifier`
  - Branchenministerien +5 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
- **The Systems Men** `COLDWAR_SOV_kos_the_systems_men` · Kosten 5 · benötigt: kos_the_premier_takes_the_party · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - Forschungsbonus CAT_computing +50 % ×1 `add_tech_bonus`
  - Systems Directorate +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
  - _Anmerkung:_ Dschermen Gwischiani und das Staatskomitee für Wissenschaft und Technik.
- **Government before Party** `COLDWAR_SOV_kos_government_before_party` · Kosten 5 · benötigt: kos_the_premier_takes_the_party · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Programm „Kosygin's Reform Course“: Bürokratiekosten -5 % `COLDWAR_SOV_kos_programme`
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **Which Reform?** `COLDWAR_SOV_kos_the_reform_model` · Kosten 3 · benötigt: kos_baibakov_at_gosplan, kos_the_systems_men · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Erste Weiche – drei Wege, gegenseitig exklusiv
- **Market Socialism** `COLDWAR_SOV_kos_market_socialism` · Kosten 5 · benötigt: kos_the_reform_model · schließt aus: kos_cybernetic_communism, kos_reform_within_the_plan · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Programm „Kosygin's Reform Course“: Produktivitätswachstum +5 %, Konsumgüter -3 % `COLDWAR_SOV_kos_programme`
  - Socialist Market Commonwealth +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
- **Flexible Prices** `COLDWAR_SOV_kos_flexible_prices` · Kosten 5 · benötigt: kos_market_socialism · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Stabilität -4 % `add_stability`
  - Gosplan – Planwirtschaft: Konsumgüter -2 %, Steuereinnahmen +3 % `COLDWAR_SOV_gosplan_modifier`
  - Entfernt „The Second Economy“ `remove_ideas`
- **The Law on the Socialist Enterprise** `COLDWAR_SOV_kos_the_enterprise_law` · Kosten 5 · benötigt: kos_flexible_prices · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Gosplan – Planwirtschaft: Produktivitätswachstum +4 % `COLDWAR_SOV_gosplan_modifier`
  - Gewerkschaften (VTsSPS) -5 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
- **Joint Ventures with the West** `COLDWAR_SOV_kos_joint_ventures` · Kosten 5 · benötigt: kos_the_enterprise_law · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Gosplan – Planwirtschaft: Handelsmeinung +10 %, Kosten für Investoren bei uns -10 % `COLDWAR_SOV_gosplan_modifier`
  - Kredit: Treasury +0.5 % BIP, Schulden +0.5 % BIP `COLDWAR_SOV_receive_gdp_share` `modify_debt_effect`
- **Cybernetic Communism** `COLDWAR_SOV_kos_cybernetic_communism` · Kosten 5 · benötigt: kos_the_reform_model · schließt aus: kos_market_socialism, kos_reform_within_the_plan · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Programm „Kosygin's Reform Course“: Effizienzzuwachs +5 %, Max. Fabrikeffizienz +3 % `COLDWAR_SOV_kos_programme`
  - Kosten 1 % BIP `COLDWAR_SOV_pay_gdp_share`
- **The OGAS Grid** `COLDWAR_SOV_kos_the_ogas_grid` · Kosten 7 · benötigt: kos_cybernetic_communism · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Gebäude: Büros `two_office_construction`, Kosten 1.4 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Effizienzzuwachs +5 % `COLDWAR_SOV_gosplan_modifier`
- **The Electronic Rouble** `COLDWAR_SOV_kos_the_electronic_rouble` · Kosten 5 · benötigt: kos_the_ogas_grid · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Korruption −1 Stufe `decrease_corruption`
  - Entfernt „The Second Economy“ `remove_ideas`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ Gluschkows bargeldloser Plan.
- **The Planometric Institutes** `COLDWAR_SOV_kos_the_planometric_institutes` · Kosten 5 · benötigt: kos_the_electronic_rouble · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Zentrales Ökonomisch-Mathematisches Institut (CEMI).
- **Reform within the Plan** `COLDWAR_SOV_kos_reform_within_the_plan` · Kosten 5 · benötigt: kos_the_reform_model · schließt aus: kos_market_socialism, kos_cybernetic_communism · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Programm „Kosygin's Reform Course“: Produktivitätswachstum +3 %, Stabilität +2 % `COLDWAR_SOV_kos_programme`
  - Branchenministerien +5 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
  - _Anmerkung:_ Kossygins eigener, vorsichtiger Weg: die Reform von 1965 retten, ohne das System anzutasten.
- **Plan, Profit, Bonus** `COLDWAR_SOV_kos_profit_and_bonus` · Kosten 5 · benötigt: kos_reform_within_the_plan · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 %, Steuer Zivilindustrie +3 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Jewsei Libermans Prawda-Artikel von 1962.
- **Production Associations** `COLDWAR_SOV_kos_the_production_associations` · Kosten 5 · benötigt: kos_profit_and_bonus · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Gosplan – Planwirtschaft: Max. Fabrikeffizienz +3 % `COLDWAR_SOV_gosplan_modifier`
  - Der Parteistaat: Bürokratiekosten -3 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Die Vereinigungen von 1973.
- **The Apparatus Resists** `COLDWAR_SOV_kos_the_apparatus_resists` · Kosten 3 · benötigt: kos_joint_ventures oder kos_the_planometric_institutes oder kos_the_production_associations · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Zweite Weiche: die Partei wehrt sich – gegenseitig exklusiv
- **Bring the Party Along** `COLDWAR_SOV_kos_bring_the_party_along` · Kosten 5 · benötigt: kos_the_apparatus_resists · schließt aus: kos_break_the_apparatus · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - PP +50 `add_political_power`
  - Nomenklatura +10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Gosplan – Planwirtschaft: Produktivitätswachstum -1 % `COLDWAR_SOV_gosplan_modifier`
- **Break the Apparatus** `COLDWAR_SOV_kos_break_the_apparatus` · Kosten 7 · benötigt: kos_the_apparatus_resists · schließt aus: kos_bring_the_party_along · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Nomenklatura -20 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Stabilität -5 % `add_stability`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +5 % `COLDWAR_SOV_gosplan_modifier`
  - Entfernt „Stability of Cadres“ `remove_ideas`
- **Curb the Military Budget** `COLDWAR_SOV_kos_curb_the_military_budget` · Kosten 5 · benötigt: kos_government_before_party · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Verteidigungshaushalt −1 Stufe `decrease_military_spending`
  - Armee & Generalstab -10 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Rüstungskomplex (VPK) -10 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - Programm „Kosygin's Reform Course“: Konsumgüter -3 % `COLDWAR_SOV_kos_programme`
- **Conversion of Defence Plants** `COLDWAR_SOV_kos_conversion_of_defence_plants` · Kosten 5 · benötigt: kos_curb_the_military_budget · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Gebäude: Zivilfabrik `one_random_industrial_complex`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Konsumgüter -2 % `COLDWAR_SOV_gosplan_modifier`
  - Rüstungskomplex (VPK) -5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
- **Trade, Not Tanks** `COLDWAR_SOV_kos_trade_not_tanks` · Kosten 5 · benötigt: kos_government_before_party · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Programm „Kosygin's Reform Course“: Handelsmeinung +10 % `COLDWAR_SOV_kos_programme`
  - Cold-War-Spannung -1 `mdcw_cw_add_tension`
  - Meinung FRA +10 `add_opinion_modifier`
- **The Glassboro Spirit** `COLDWAR_SOV_kos_the_glassboro_spirit` · Kosten 5 · benötigt: kos_trade_not_tanks · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Gipfel mit dem Premier. Bei Annahme: Spannung −2, Handelsabkommen, Meinung +15 `COLDWAR_SOV_offer_kosygin_summit`
  - _Anmerkung:_ Erinnerung an Glassboro 1967.
- **The Tashkent Mediator** `COLDWAR_SOV_kos_the_tashkent_mediator` · Kosten 5 · benötigt: kos_trade_not_tanks · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Einfluss +3 % in RAJ, PAK `change_influence_percentage`
  - Meinung RAJ +10 `add_opinion_modifier`
  - Meinung PAK +10 `add_opinion_modifier`
  - _Anmerkung:_ Kossygin vermittelte 1966 in Taschkent zwischen Indien und Pakistan.
- **Not a Single Soldier** `COLDWAR_SOV_kos_not_a_single_soldier` · Kosten 3 · benötigt: kos_the_glassboro_spirit oder kos_the_tashkent_mediator · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`); Datum ≥ 01.03.1979
  - Stabilität +2 % `add_stability`
  - Meinung AFG -10 `add_opinion_modifier`
  - _Anmerkung:_ März 1979: „Wir können das afghanische Volk nicht ersetzen.“
- **The Premier's Heart** `COLDWAR_SOV_kos_the_premiers_heart` · Kosten 3 · benötigt: kos_bring_the_party_along oder kos_break_the_apparatus · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`); Datum ≥ 01.10.1976
  - Nachfolge – gegenseitig exklusiv (Kossygin stirbt historisch im Dezember 1980)
- **Heir: Gorbachev's Generation** `COLDWAR_SOV_kos_heir_gorbachev` · Kosten 5 · benötigt: kos_the_premiers_heart · schließt aus: kos_heir_andropov, kos_rule_of_the_planners · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Erbe festgelegt: Michail Gorbatschow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_gor`, Event setzt den Politbüro-Fokus um)
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
- **Heir: Andropov** `COLDWAR_SOV_kos_heir_andropov` · Kosten 5 · benötigt: kos_the_premiers_heart · schließt aus: kos_heir_gorbachev, kos_rule_of_the_planners · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Erbe festgelegt: Juri Andropow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_and`, Event setzt den Politbüro-Fokus um)
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
- **Rule of the Planners** `COLDWAR_SOV_kos_rule_of_the_planners` · Kosten 5 · benötigt: kos_the_premiers_heart · schließt aus: kos_heir_gorbachev, kos_heir_andropov · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Regierungspartei → Gosplan Technocracy (Neutral Autocracy) `change_ruling_party_effect`, Staatschef Nikolai Baibakov `create_country_leader` – Technokratie ohne Partei
  - Stabilität -5 % `add_stability`
  - _Anmerkung:_ Endet den KPdSU-Weg: Wechsel zu Partei 13 (Gosplan Technocracy).
- **Socialism That Works** `COLDWAR_SOV_kos_socialism_that_works` · Kosten 7 · benötigt: kos_heir_gorbachev oder kos_heir_andropov, kos_conversion_of_defence_plants, kos_not_a_single_soldier · verfügbar: `emerging_communist_state_are_in_power`; Alexei Kossygin ist Generalsekretär (`COLDWAR_SOV_gensec_kos`)
  - Idee „Reformed Socialist Economy“: Produktivitätswachstum +5 %, Max. Fabrikeffizienz +3 % (`add_ideas`)
  - Stabilität +3 % `add_stability`

### Generalsekretär: Nikolai Podgorny (21)

Vorsitzender des Präsidiums (bis 1977 im Amt, lebt bis 1983). Föderale Union oder starkes Präsidium; der Staat über der Partei.

- **The President of the Presidium** `COLDWAR_SOV_pod_the_president_of_the_presidium` · Kosten 3 · benötigt: ple_pod · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Programm „Podgorny's State“: Stabilität +2 %, PP-Gewinn +3 % `COLDWAR_SOV_pod_programme`
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
- **The Supreme Soviet Awakens** `COLDWAR_SOV_pod_the_supreme_soviet_awakens` · Kosten 5 · benötigt: pod_the_president_of_the_presidium · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Programm „Podgorny's State“: PP-Gewinn +3 % `COLDWAR_SOV_pod_programme`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
- **The Kharkov Connection** `COLDWAR_SOV_pod_the_kharkov_connection` · Kosten 5 · benötigt: pod_the_president_of_the_presidium · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
  - Union of Sovereign Republics +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
  - _Anmerkung:_ Podgornys ukrainische Basis (Charkiw, Kiew).
- **An Alliance with the Ministers** `COLDWAR_SOV_pod_the_council_of_ministers_alliance` · Kosten 5 · benötigt: pod_the_president_of_the_presidium · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Branchenministerien +10 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
  - Gosplan – Planwirtschaft: Effizienzzuwachs +2 % `COLDWAR_SOV_gosplan_modifier`
- **Federation or Presidium?** `COLDWAR_SOV_pod_the_state_question` · Kosten 3 · benötigt: pod_the_supreme_soviet_awakens, pod_the_kharkov_connection · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Erste Weiche – gegenseitig exklusiv
- **A Federal Union** `COLDWAR_SOV_pod_a_federal_union` · Kosten 5 · benötigt: pod_the_state_question · schließt aus: pod_the_strong_presidium · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Zusammenhalt der Union +10 `COLDWAR_SOV_change_union_cohesion`
  - Programm „Podgorny's State“: Stabilität +3 %, Nationalistische Drift -0.02 `COLDWAR_SOV_pod_programme`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - Politbüro der Republiken: Republikstimmen zählen doppelt bei Unionsfragen (Sprache, Unionsvertrag, Anträge der Republiken)
- **Republic Councils of Ministers** `COLDWAR_SOV_pod_republic_councils` · Kosten 5 · benötigt: pod_a_federal_union · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Zusammenhalt der Union +4 `COLDWAR_SOV_change_union_cohesion`
  - Der Parteistaat: Bürokratiekosten +3 % `COLDWAR_SOV_party_state_modifier`
- **Republican Cost Accounting** `COLDWAR_SOV_pod_republican_accounting` · Kosten 5 · benötigt: pod_republic_councils · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +2 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Die Republiken wirtschaften auf eigene Rechnung.
- **The Soviet of Nationalities** `COLDWAR_SOV_pod_the_soviet_of_nationalities` · Kosten 5 · benötigt: pod_republican_accounting · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Zusammenhalt der Union +5 `COLDWAR_SOV_change_union_cohesion`
  - Union der Republiken: Ideologische Driftabwehr +5 % `COLDWAR_SOV_union_modifier`
- **The Strong Presidium** `COLDWAR_SOV_pod_the_strong_presidium` · Kosten 5 · benötigt: pod_the_state_question · schließt aus: pod_a_federal_union · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Programm „Podgorny's State“: PP-Gewinn +5 %, Bürokratiekosten -5 % `COLDWAR_SOV_pod_programme`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Zusammenhalt der Union -2 `COLDWAR_SOV_change_union_cohesion`
- **Ministers Answer to the State** `COLDWAR_SOV_pod_ministers_answer_to_the_state` · Kosten 5 · benötigt: pod_the_strong_presidium · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Gosplan – Planwirtschaft: Effizienzzuwachs +3 % `COLDWAR_SOV_gosplan_modifier`
  - Branchenministerien +5 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
- **Presidential Decrees** `COLDWAR_SOV_pod_presidential_decrees` · Kosten 5 · benötigt: pod_ministers_answer_to_the_state · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - PP +75 `add_political_power`
  - Stabilität +2 % `add_stability`
- **The State Security Council** `COLDWAR_SOV_pod_the_state_security_council` · Kosten 5 · benötigt: pod_presidential_decrees · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - Der Parteistaat: Ideologische Driftabwehr +5 % `COLDWAR_SOV_party_state_modifier`
- **Head-of-State Diplomacy** `COLDWAR_SOV_pod_head_of_state_diplomacy` · Kosten 5 · benötigt: pod_the_council_of_ministers_alliance · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Einfluss +3 % in EGY, SYR, SOM, ETH, AGL, MOZ `change_influence_percentage`
  - Meinung EGY +10 `add_opinion_modifier`
  - _Anmerkung:_ Podgornys Afrikareise 1977.
- **The Treaty Signer** `COLDWAR_SOV_pod_the_treaty_signer` · Kosten 5 · benötigt: pod_head_of_state_diplomacy · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Freundschaftsverträge (Ägypten, Irak, Indien) kosten 25 PP weniger Zeit: −30 % Fokuszeit für diese Fokusse
  - _Anmerkung:_ Podgorny unterschrieb im Mai 1971 den Vertrag mit Ägypten.
- **The Ukrainian Breadbasket** `COLDWAR_SOV_pod_ukrainian_breadbasket` · Kosten 5 · benötigt: pod_the_kharkov_connection · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Gosplan – Planwirtschaft: Agrarproduktivität +4 % `COLDWAR_SOV_gosplan_modifier`
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
- **Donbass Coal** `COLDWAR_SOV_pod_donbass_coal` · Kosten 5 · benötigt: pod_ukrainian_breadbasket · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Gebäude: Energieinfrastruktur `one_random_energy_infrastructure`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Gewerkschaften (VTsSPS) +5 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
- **The Final Form of the State** `COLDWAR_SOV_pod_the_final_form` · Kosten 3 · benötigt: pod_the_soviet_of_nationalities oder pod_the_state_security_council, pod_donbass_coal · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Zweite Weiche – gegenseitig exklusiv
- **A Union of Sovereign States** `COLDWAR_SOV_pod_union_of_sovereign_states` · Kosten 7 · benötigt: pod_the_final_form · schließt aus: pod_the_soviet_presidency · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Regierungspartei → Union of Sovereign Republics (Neutral Communism) `change_ruling_party_effect`, Staatschef Pyotr Shelest `create_country_leader` – Nationalkommunistische Union
  - Zusammenhalt der Union +10 `COLDWAR_SOV_change_union_cohesion`
  - Stabilität -5 % `add_stability`
  - _Anmerkung:_ Endet den KPdSU-Weg: Wechsel zu Partei 19.
- **The Soviet Presidency** `COLDWAR_SOV_pod_the_soviet_presidency` · Kosten 5 · benötigt: pod_the_final_form · schließt aus: pod_union_of_sovereign_states · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Programm „Podgorny's State“: PP-Gewinn +5 %, Stabilität +2 % `COLDWAR_SOV_pod_programme`
  - Staatschef erhält Trait „President of the USSR“ `add_country_leader_trait`
- **The Soviet State** `COLDWAR_SOV_pod_the_soviet_state` · Kosten 7 · benötigt: pod_the_soviet_presidency, pod_the_treaty_signer · verfügbar: `emerging_communist_state_are_in_power`; Nikolai Podgorny ist Generalsekretär (`COLDWAR_SOV_gensec_pod`)
  - Idee „The Soviet State“: Stabilität +4 %, PP-Gewinn +5 %, Bürokratiekosten -5 % (`add_ideas`)
  - Zusammenhalt der Union +5 `COLDWAR_SOV_change_union_cohesion`

### Generalsekretär: Michail Suslow (24)

Hardliner der Ideologie (bis 1982). Ideologische Reinheit oder militanter Internationalismus, moralische statt materieller Anreize, Kampf gegen Peking und Eurokommunismus.

- **The Grey Cardinal Rules** `COLDWAR_SOV_sus_the_grey_cardinal_rules` · Kosten 3 · benötigt: ple_sus · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Programm „Suslov's Orthodoxy“: Ideologische Abwehr (Cold War) +15 %, Ideologische Driftabwehr +10 %, Forschung -2 %, PP-Gewinn +5 % `COLDWAR_SOV_sus_programme`
- **The Ideological Commission** `COLDWAR_SOV_sus_the_ideological_commission` · Kosten 5 · benötigt: sus_the_grey_cardinal_rules · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Communist Party of the Soviet Union +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Nomenklatura +5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **Ponomarev's Department** `COLDWAR_SOV_sus_ponomarevs_department` · Kosten 5 · benötigt: sus_the_grey_cardinal_rules · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Einfluss +2 % in CUB, VIE, MON `change_influence_percentage`
  - _Anmerkung:_ Boris Ponomarjow und die Internationale Abteilung des ZK.
- **Trapeznikov's Science Department** `COLDWAR_SOV_sus_trapeznikovs_science_department` · Kosten 5 · benötigt: sus_the_grey_cardinal_rules · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Neo-Stalinist Platform +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
  - Der Parteistaat: Forschung -1 %, Ideologische Driftabwehr +5 % `COLDWAR_SOV_party_state_modifier`
- **The Correct Line** `COLDWAR_SOV_sus_the_line` · Kosten 3 · benötigt: sus_the_ideological_commission, sus_trapeznikovs_science_department · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Erste Weiche – gegenseitig exklusiv
- **Ideological Purity** `COLDWAR_SOV_sus_ideological_purity` · Kosten 5 · benötigt: sus_the_line · schließt aus: sus_militant_internationalism · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Politbüro-Balance +0.15 Richtung Orthodoxe `add_power_balance_value`
  - Stabilität +3 % `add_stability`
  - ersetzt „Samizdat and Dissent“: Idee „Silenced Dissent“: Stabilität +3 %, Ideologische Driftabwehr +10 %, Forschung -2 %, Handelsmeinung -5 % (`swap_ideas`)
- **Rewrite the History** `COLDWAR_SOV_sus_rewrite_the_history` · Kosten 5 · benötigt: sus_ideological_purity · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Neo-Stalinist Platform +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Programm „Suslov's Orthodoxy“: Stabilität +2 % `COLDWAR_SOV_sus_programme`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
  - _Anmerkung:_ Stalin als „Organisator des Sieges“ – die schleichende Rehabilitierung.
- **The Glavlit Offensive** `COLDWAR_SOV_sus_the_glavlit_offensive` · Kosten 5 · benötigt: sus_rewrite_the_history · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Der Parteistaat: Fremde Subversion -10 %, Forschung -1 % `COLDWAR_SOV_party_state_modifier`
  - Stabilität +2 % `add_stability`
- **The Closed Society** `COLDWAR_SOV_sus_the_closed_society` · Kosten 5 · benötigt: sus_the_glavlit_offensive · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Programm „Suslov's Orthodoxy“: Ideologische Driftabwehr +10 %, Handelsmeinung -5 % `COLDWAR_SOV_sus_programme`
- **Militant Internationalism** `COLDWAR_SOV_sus_militant_internationalism` · Kosten 5 · benötigt: sus_the_line · schließt aus: sus_ideological_purity · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Programm „Suslov's Orthodoxy“: Unterstützungskampagnen (Cold War) +15 %, Auslandseinfluss +10 %, Steuereinnahmen -2 % `COLDWAR_SOV_sus_programme`
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
- **The Liberation Movements** `COLDWAR_SOV_sus_the_liberation_movements` · Kosten 5 · benötigt: sus_militant_internationalism · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Einfluss +3 % in AGL, MOZ, ETH, YEM, SYE `change_influence_percentage`
  - Sozialistische Gemeinschaft: Kosten Militärprogramme (Cold War) -10 % `COLDWAR_SOV_commonwealth_modifier`
- **Against Eurocommunism** `COLDWAR_SOV_sus_against_eurocommunism` · Kosten 5 · benötigt: sus_the_liberation_movements · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`); Datum ≥ 01.01.1975
  - Sozialistische Gemeinschaft: Meinungsgewinn gleiche Ideologie +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Meinung ITA -10 `add_opinion_modifier`
  - Meinung FRA -5 `add_opinion_modifier`
  - _Anmerkung:_ Berliner Konferenz 1976: Berlinguer, Marchais und Carrillo gehen eigene Wege.
- **The World Conference** `COLDWAR_SOV_sus_the_world_conference` · Kosten 5 · benötigt: sus_against_eurocommunism · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +5 % `COLDWAR_SOV_commonwealth_modifier`
  - PP +50 `add_political_power`
  - _Anmerkung:_ Wie die Moskauer Konferenz von 1969 – mit Moskau als Zentrum.
- **Moral Incentives** `COLDWAR_SOV_sus_moral_incentives` · Kosten 5 · benötigt: sus_the_ideological_commission · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Gosplan – Planwirtschaft: Effizienzzuwachs +2 %, Produktivitätswachstum -1 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität +2 % `add_stability`
  - _Anmerkung:_ Ehrentafeln und Wanderfahnen statt Prämien.
- **Against the Market** `COLDWAR_SOV_sus_against_the_market` · Kosten 5 · benötigt: sus_moral_incentives · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Nomenklatura +5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Gosplan – Planwirtschaft: Produktivitätswachstum -2 % `COLDWAR_SOV_gosplan_modifier`
  - Entfernt „Cooperative Sector“ `remove_ideas`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
- **The Drawing Together of Nations** `COLDWAR_SOV_sus_the_drawing_together_of_nations` · Kosten 5 · benötigt: sus_marxism_leninism_in_every_school · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
  - Union der Republiken: Nationalistische Drift -0.01 `COLDWAR_SOV_union_modifier`
  - _Anmerkung:_ „Sblischenije“ – die Annäherung der Nationen zum Sowjetvolk.
- **Marxism-Leninism in Every School** `COLDWAR_SOV_sus_marxism_leninism_in_every_school` · Kosten 5 · benötigt: sus_ponomarevs_department · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Programm „Suslov's Orthodoxy“: Kommunistische Drift +0.03 `COLDWAR_SOV_sus_programme`
  - Gosplan – Planwirtschaft: Bildungskosten +3 % `COLDWAR_SOV_gosplan_modifier`
- **No Gods in the Kremlin** `COLDWAR_SOV_sus_no_gods_in_the_kremlin` · Kosten 5 · benötigt: sus_the_drawing_together_of_nations · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Der Parteistaat: Ideologische Driftabwehr +5 % `COLDWAR_SOV_party_state_modifier`
  - Live Not by Lies -3 % Popularität (Outlook -3 %) `change_relative_party_popularity`
  - House of Romanov -2 % Popularität (Outlook -2 %) `change_relative_party_popularity`
  - Stabilität -1 % `add_stability`
- **The Polemic with Beijing** `COLDWAR_SOV_sus_the_polemic_with_beijing` · Kosten 5 · benötigt: sus_the_closed_society oder sus_the_world_conference · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Der Parteistaat: Ideologische Driftabwehr +5 % `COLDWAR_SOV_party_state_modifier`
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Meinung CHI -10 `add_opinion_modifier`
- **The Ideologue's Heir** `COLDWAR_SOV_sus_the_heir_question` · Kosten 3 · benötigt: sus_the_polemic_with_beijing, sus_against_the_market · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`); Datum ≥ 01.01.1978
  - Nachfolge – gegenseitig exklusiv (Suslow stirbt historisch im Januar 1982)
- **Heir: Chernenko** `COLDWAR_SOV_sus_heir_chernenko` · Kosten 5 · benötigt: sus_the_heir_question · schließt aus: sus_heir_romanov, sus_the_iron_line_inherits · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Erbe festgelegt: Konstantin Tschernenko übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_che`, Event setzt den Politbüro-Fokus um)
  - Stabilität +2 % `add_stability`
- **Heir: Romanov** `COLDWAR_SOV_sus_heir_romanov` · Kosten 5 · benötigt: sus_the_heir_question · schließt aus: sus_heir_chernenko, sus_the_iron_line_inherits · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Erbe festgelegt: Grigori Romanow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_gro`, Event setzt den Politbüro-Fokus um)
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
- **The Iron Line Inherits** `COLDWAR_SOV_sus_the_iron_line_inherits` · Kosten 5 · benötigt: sus_the_heir_question · schließt aus: sus_heir_chernenko, sus_heir_romanov · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Regierungspartei → Neo-Stalinist Platform (Emerging Conservative) `change_ruling_party_effect`, Staatschef Sergei Trapeznikov `create_country_leader` – Neostalinistische Plattform übernimmt
  - Politbüro-Balance +0.15 Richtung Orthodoxe `add_power_balance_value`
  - _Anmerkung:_ Endet den KPdSU-Weg: Wechsel zu Partei 6.
- **The Orthodox Union** `COLDWAR_SOV_sus_the_orthodox_union` · Kosten 7 · benötigt: sus_heir_chernenko oder sus_heir_romanov, sus_no_gods_in_the_kremlin · verfügbar: `emerging_communist_state_are_in_power`; Michail Suslow ist Generalsekretär (`COLDWAR_SOV_gensec_sus`)
  - Idee „The Orthodox Union“: Ideologische Driftabwehr +15 %, Stabilität +4 %, Forschung -2 % (`add_ideas`)

### Generalsekretär: Alexander Schelepin (23)

Hardliner der Ordnung: Ex-KGB-Chef, Gewerkschaftsboss, Kopf der „Komsomolzen“ (Politbüro bis April 1975). Disziplin oder Arbeitersozialismus, Säuberung der Breschnew-Leute.

- **Iron Shurik** `COLDWAR_SOV_she_iron_shurik` · Kosten 3 · benötigt: ple_she · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Programm „Shelepin's Order“: Stabilität +5 %, PP-Gewinn +5 %, Ideologische Driftabwehr +10 %, Korruptionskosten -10 % `COLDWAR_SOV_she_programme`
- **The Komsomoltsy** `COLDWAR_SOV_she_the_komsomoltsy` · Kosten 5 · benötigt: she_iron_shurik · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Komsomol Vanguard +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ Jegorytschew, Mesjazew, Tikunow – Schelepins Netzwerk aus Komsomol und KGB.
- **Semichastny Returns** `COLDWAR_SOV_she_semichastny_returns` · Kosten 5 · benötigt: she_iron_shurik · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - KGB +10 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - Der Parteistaat: Fremde Subversion -10 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Wladimir Semitschastny, KGB-Chef bis 1967.
- **The Trade Union Base** `COLDWAR_SOV_she_the_trade_union_base` · Kosten 5 · benötigt: she_iron_shurik · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Gewerkschaften (VTsSPS) +10 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
  - Stabilität +2 % `add_stability`
  - _Anmerkung:_ Schelepin führte seit 1967 den Gewerkschaftsbund VTsSPS.
- **The Labour Question** `COLDWAR_SOV_she_the_labour_question` · Kosten 3 · benötigt: she_the_komsomoltsy, she_the_trade_union_base · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Erste Weiche – gegenseitig exklusiv
- **Labour Discipline** `COLDWAR_SOV_she_labour_discipline` · Kosten 5 · benötigt: she_the_labour_question · schließt aus: she_workers_socialism · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Programm „Shelepin's Order“: Produktivitätswachstum +5 % `COLDWAR_SOV_she_programme`
  - Stabilität -2 % `add_stability`
  - Gewerkschaften (VTsSPS) -10 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
- **The Absenteeism Raids** `COLDWAR_SOV_she_the_absenteeism_raids` · Kosten 5 · benötigt: she_labour_discipline · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
  - Der Parteistaat: Polizeikosten +5 % `COLDWAR_SOV_party_state_modifier`
- **The War on Drunkenness** `COLDWAR_SOV_she_the_war_on_drunkenness` · Kosten 5 · benötigt: she_the_absenteeism_raids · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Gosplan – Planwirtschaft: Produktivitätswachstum +2 %, Steuereinnahmen -2 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität -2 % `add_stability`
- **Workers' Socialism** `COLDWAR_SOV_she_workers_socialism` · Kosten 5 · benötigt: she_the_labour_question · schließt aus: she_labour_discipline · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Programm „Shelepin's Order“: Konsumgüter -2 %, Stabilität +3 % `COLDWAR_SOV_she_programme`
  - Gewerkschaften (VTsSPS) +15 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
  - Free Councils of Labour +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
- **The Union Councils** `COLDWAR_SOV_she_the_union_councils` · Kosten 5 · benötigt: she_workers_socialism · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Gosplan – Planwirtschaft: Sozialkosten +3 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität +2 % `add_stability`
- **Workers' Control Commissions** `COLDWAR_SOV_she_the_workers_control` · Kosten 5 · benötigt: she_the_union_councils · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Korruption −1 Stufe `decrease_corruption`
  - Branchenministerien -10 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
- **Order in the Streets** `COLDWAR_SOV_she_order_in_the_streets` · Kosten 5 · benötigt: she_semichastny_returns · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Polizeibudget +1 Stufe `increase_policing_budget`
  - Stabilität +3 % `add_stability`
- **The War on Corruption** `COLDWAR_SOV_she_the_war_on_corruption` · Kosten 5 · benötigt: she_order_in_the_streets · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Korruption −1 Stufe `decrease_corruption`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **Purge the Brezhnevites** `COLDWAR_SOV_she_purge_the_brezhnevites` · Kosten 7 · benötigt: she_the_war_on_corruption, she_the_war_on_drunkenness oder she_the_workers_control · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Nomenklatura -15 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Korruption −1 Stufe `decrease_corruption`
  - Stabilität -3 % `add_stability`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
  - Entfernt „Stability of Cadres“ `remove_ideas`
  - Politbüro der Republiken: Einmal: einen Sitzinhaber ohne Plenum-Kosten absetzen
- **Youth Brigades** `COLDWAR_SOV_she_youth_brigades` · Kosten 5 · benötigt: she_the_komsomoltsy · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Gosplan – Planwirtschaft: Baugeschwindigkeit +5 % `COLDWAR_SOV_gosplan_modifier`
  - Mannstärke +15.000 `add_manpower`
- **The Komsomol Economy** `COLDWAR_SOV_she_the_komsomol_economy` · Kosten 5 · benötigt: she_youth_brigades · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Gebäude: Infrastruktur `one_random_infrastructure`, Kosten 0.6 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Bau Infrastruktur +10 % `COLDWAR_SOV_gosplan_modifier`
- **East or West?** `COLDWAR_SOV_she_the_foreign_line` · Kosten 3 · benötigt: she_the_komsomol_economy · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Gegenseitig exklusiv
- **Talk to Beijing** `COLDWAR_SOV_she_talk_to_beijing` · Kosten 5 · benötigt: she_the_foreign_line · schließt aus: she_confront_the_west · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Angebot an CHI (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Gespräche zwischen zwei Lagern der „reinen Linie“. Bei Annahme: Meinung +20, Spannung an der Grenze sinkt (Ussuri-Geist mildert sich) `COLDWAR_SOV_offer_shelepin_china`
  - _Anmerkung:_ Schelepin galt in Peking als Mann, mit dem man reden könne.
- **Confront the West** `COLDWAR_SOV_she_confront_the_west` · Kosten 5 · benötigt: she_the_foreign_line · schließt aus: she_talk_to_beijing · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
  - Kriegsunterstützung +3 % `add_war_support`
  - Streitkräfte der UdSSR: Moral (Heer) +3 % `COLDWAR_SOV_armed_forces_modifier`
- **The Shape of Power** `COLDWAR_SOV_she_the_final_question` · Kosten 3 · benötigt: she_purge_the_brezhnevites, she_talk_to_beijing oder she_confront_the_west · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Zweite Weiche – gegenseitig exklusiv
- **The Leader State** `COLDWAR_SOV_she_the_leader_state` · Kosten 7 · benötigt: she_the_final_question · schließt aus: she_collective_discipline · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Regierungspartei → Komsomol Vanguard (Emerging Autocracy) `change_ruling_party_effect`, Staatschef Alexander Shelepin `create_country_leader` – Schelepin bleibt Staatschef
  - Staatschef erhält Trait „Vozhd“ `add_country_leader_trait`
  - Politbüro-Balance +0.15 Richtung Orthodoxe `add_power_balance_value`
  - _Anmerkung:_ Endet den KPdSU-Weg: Wechsel zu Partei 7 (Komsomol Vanguard) – deren Baum öffnet sich.
- **Collective Discipline** `COLDWAR_SOV_she_collective_discipline` · Kosten 5 · benötigt: she_the_final_question · schließt aus: she_the_leader_state · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Stabilität +5 % `add_stability`
  - Programm „Shelepin's Order“: PP-Gewinn +3 % `COLDWAR_SOV_she_programme`
  - Erbe festgelegt: Juri Andropow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_and`, Event setzt den Politbüro-Fokus um) – Schelepins Disziplin geht an den KGB über
- **The Iron Order** `COLDWAR_SOV_she_the_iron_order` · Kosten 7 · benötigt: she_collective_discipline · verfügbar: `emerging_communist_state_are_in_power`; Alexander Schelepin ist Generalsekretär (`COLDWAR_SOV_gensec_she`)
  - Idee „The Iron Order“: Stabilität +5 %, Produktivitätswachstum +3 %, Forschung -2 % (`add_ideas`)

### Generalsekretär: Juri Andropow (23)

KGB-Chef (Politbüro ab April 1973, lebt bis 1984). Ordnung und Reform oder tschekistischer Staat; Disziplinkampagne, Baumwollaffäre, Ausweg aus Afghanistan.

- **The Chekist Takes Power** `COLDWAR_SOV_and_the_chekist_takes_power` · Kosten 3 · hist. · benötigt: ple_and · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Programm „Andropov's Course“: Korruptionskosten -10 %, Ideologische Driftabwehr +10 %, Produktivitätswachstum +3 %, PP-Gewinn +3 % `COLDWAR_SOV_and_programme`
- **KGB Men in the Kremlin** `COLDWAR_SOV_and_kgb_men_in_the_kremlin` · Kosten 5 · hist. · benötigt: and_the_chekist_takes_power · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - KGB +10 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - Der Parteistaat: Geheimdienstnetz-Zuwachs +5 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Tschebrikow, Krjutschkow, Alijew.
- **The Young Reformers** `COLDWAR_SOV_and_the_young_reformers` · Kosten 5 · hist. · benötigt: and_the_chekist_takes_power · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Gorbatschow, Ryschkow, Ligatschow – Andropows Team.
- **Lessons of Budapest** `COLDWAR_SOV_and_lessons_of_budapest` · Kosten 5 · benötigt: and_the_chekist_takes_power · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Gosplan – Planwirtschaft: Konsumgüter -2 % `COLDWAR_SOV_gosplan_modifier`
  - Meinung HUN +10 `add_opinion_modifier`
  - _Anmerkung:_ Botschafter in Budapest 1956.
- **The Discipline Campaign** `COLDWAR_SOV_and_the_discipline_campaign` · Kosten 5 · hist. · benötigt: and_kgb_men_in_the_kremlin · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Programm „Andropov's Course“: Produktivitätswachstum +4 % `COLDWAR_SOV_and_programme`
  - Stabilität -2 % `add_stability`
  - Politbüro der Republiken: Kompromat-Chance +20 %; der KGB darf ohne Ankläger gegen einen Sitzinhaber ermitteln (50 PP)
  - _Anmerkung:_ Razzien in Kinos und Badehäusern während der Arbeitszeit.
- **Order or Reform?** `COLDWAR_SOV_and_the_road` · Kosten 3 · hist. · benötigt: and_the_discipline_campaign, and_the_young_reformers · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Erste Weiche – gegenseitig exklusiv
- **Order and Reform** `COLDWAR_SOV_and_order_and_reform` · Kosten 5 · hist. · benötigt: and_the_road · schließt aus: and_the_chekist_state · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Programm „Andropov's Course“: Produktivitätswachstum +5 % `COLDWAR_SOV_and_programme`
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
- **The Large-Scale Economic Experiment** `COLDWAR_SOV_and_the_large_scale_experiment` · Kosten 5 · hist. · benötigt: and_order_and_reform · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 %, Effizienzzuwachs +3 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ 1983/84 in fünf Ministerien.
- **Ryzhkov's Economic Department** `COLDWAR_SOV_and_the_economic_department` · Kosten 5 · benötigt: and_the_large_scale_experiment · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Gosplan – Planwirtschaft: Max. Fabrikeffizienz +3 % `COLDWAR_SOV_gosplan_modifier`
  - Der Parteistaat: Bürokratiekosten -3 % `COLDWAR_SOV_party_state_modifier`
- **The Technology Gap** `COLDWAR_SOV_and_the_technology_gap` · Kosten 5 · benötigt: and_the_economic_department · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Forschungsbonus CAT_computing, CAT_microchips +50 % ×1 `add_tech_bonus`
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
- **The Chekist State** `COLDWAR_SOV_and_the_chekist_state` · Kosten 5 · benötigt: and_the_road · schließt aus: and_order_and_reform · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Programm „Andropov's Course“: Ideologische Abwehr (Cold War) +15 %, Geheimdienstnetz-Zuwachs +10 %, Stabilität +3 %, Forschung -2 % `COLDWAR_SOV_and_programme`
  - Politbüro-Balance +0.10 Richtung Orthodoxe `add_power_balance_value`
  - KGB +10 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
- **Gorky for Sakharov** `COLDWAR_SOV_and_gorky_for_sakharov` · Kosten 5 · benötigt: and_the_chekist_state · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Committee for Human Rights -5 % Popularität (Outlook -5 %) `change_relative_party_popularity`
  - Der Parteistaat: Ideologische Driftabwehr +5 % `COLDWAR_SOV_party_state_modifier`
  - Meinung USA -10 `add_opinion_modifier`
- **The KGB Economy** `COLDWAR_SOV_and_the_kgb_economy` · Kosten 5 · benötigt: and_gorky_for_sakharov · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Korruption −1 Stufe `decrease_corruption`
  - Der Parteistaat: Korruptionskosten -5 % `COLDWAR_SOV_party_state_modifier`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **The Informant Society** `COLDWAR_SOV_and_the_informant_society` · Kosten 5 · benötigt: and_the_kgb_economy · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Der Parteistaat: Fremde Subversion -15 % `COLDWAR_SOV_party_state_modifier`
  - Stabilität -1 % `add_stability`
  - Der Parteistaat: Forschung -1 % `COLDWAR_SOV_party_state_modifier`
- **The Cotton Affair Exposed** `COLDWAR_SOV_and_the_cotton_affair_exposed` · Kosten 5 · hist. · benötigt: and_lessons_of_budapest · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Korruption −1 Stufe `decrease_corruption`
  - Zusammenhalt der Union -3 `COLDWAR_SOV_change_union_cohesion`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro der Republiken: Jede Republik mit Pripiski-Flag wird sofort untersucht
- **The Shchelokov Purge** `COLDWAR_SOV_and_the_shchelokov_purge` · Kosten 5 · hist. · benötigt: and_the_cotton_affair_exposed · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Korruption −1 Stufe `decrease_corruption`
  - Der Parteistaat: Polizeikosten -5 % `COLDWAR_SOV_party_state_modifier`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ Dezember 1982: Schtscholokow wird abgesetzt, die Miliz gesäubert.
- **A Way Out** `COLDWAR_SOV_and_a_way_out_of_afghanistan` · Kosten 5 · benötigt: and_the_shchelokov_purge · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Wenn „The Afghan Burden“ aktiv ist: Rückzugsplan (Event an AFG); sonst Spannung −1
  - Cold-War-Spannung -1 `mdcw_cw_add_tension`
  - Stabilität +2 % `add_stability`
- **Talks with Beijing** `COLDWAR_SOV_and_talks_with_beijing` · Kosten 5 · benötigt: and_a_way_out_of_afghanistan · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Angebot an CHI (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Wiederaufnahme der Konsultationen (1982). Bei Annahme: Meinung +15, Spannung −1 `COLDWAR_SOV_offer_andropov_china`
- **Andropov's Kidneys** `COLDWAR_SOV_and_the_succession` · Kosten 3 · hist. · benötigt: and_the_technology_gap oder and_the_informant_society, and_talks_with_beijing · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Nachfolge – gegenseitig exklusiv (Andropow stirbt historisch im Februar 1984)
- **Heir: Mikhail Gorbachev** `COLDWAR_SOV_and_heir_gorbachev` · Kosten 5 · benötigt: and_the_succession · schließt aus: and_heir_chernenko, and_heir_aliyev · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Erbe festgelegt: Michail Gorbatschow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_gor`, Event setzt den Politbüro-Fokus um)
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - _Anmerkung:_ Andropows Protegé aus Stawropol.
- **Heir: Chernenko** `COLDWAR_SOV_and_heir_chernenko` · Kosten 5 · hist. · benötigt: and_the_succession · schließt aus: and_heir_gorbachev, and_heir_aliyev · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Erbe festgelegt: Konstantin Tschernenko übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_che`, Event setzt den Politbüro-Fokus um)
  - Stabilität +2 % `add_stability`
  - _Anmerkung:_ Historisch: die Alten setzen Tschernenko durch.
- **Heir: The Chekist from Baku** `COLDWAR_SOV_and_heir_aliyev` · Kosten 5 · benötigt: and_the_succession · schließt aus: and_heir_gorbachev, and_heir_chernenko · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Neuer Staatschef: Heydar Aliyev `create_country_leader`, Trait „Chekist from Baku“ `COLDWAR_SOV_chekist_from_baku` – beim Tod Andropows; kein eigener Baum, Andropows Programm bleibt
  - Zusammenhalt der Union +6 `COLDWAR_SOV_change_union_cohesion`
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - _Anmerkung:_ Heydar Alijew, KGB-General, seit 1982 Erster Vizepremier.
- **The Disciplined Union** `COLDWAR_SOV_and_the_disciplined_union` · Kosten 7 · benötigt: and_heir_gorbachev oder and_heir_chernenko oder and_heir_aliyev · verfügbar: `emerging_communist_state_are_in_power`; Juri Andropow ist Generalsekretär (`COLDWAR_SOV_gensec_and`)
  - Idee „The Disciplined Union“: Produktivitätswachstum +4 %, Korruptionskosten -10 %, Stabilität +2 % (`add_ideas`)

### Generalsekretär: Marschall Andrei Gretschko (21)

General: Verteidigungsminister, Politbüro ab April 1973, stirbt April 1976. Massenarmee oder nuklearer Schild, Generalstab im Politbüro, Waffen für Verbündete.

- **The Marshal's Hour** `COLDWAR_SOV_gre_the_marshals_hour` · Kosten 3 · benötigt: ple_gre · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Programm „The Marshal's Party“: Organisation (Heer) +3 %, Kriegsunterstützung +3 %, PP-Gewinn +3 %, Konsumgüter +2 % `COLDWAR_SOV_gre_programme`
  - Armee & Generalstab +10 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - _Anmerkung:_ Realistisch: kein Putsch, sondern der Verteidigungsminister an der Spitze der Partei – die Armee bekommt die Stimme, die sie 1957 (Schukow) verlor.
- **The General Staff in the Politburo** `COLDWAR_SOV_gre_the_general_staff_in_the_politburo` · Kosten 5 · benötigt: gre_the_marshals_hour · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Kommandomacht +50 `add_command_power`
  - Streitkräfte der UdSSR: Planungsgeschwindigkeit +0.05 `COLDWAR_SOV_armed_forces_modifier`
  - _Anmerkung:_ Kulikow, später Ogarkow.
- **Yepishev's Political Directorate** `COLDWAR_SOV_gre_yepishevs_political_directorate` · Kosten 5 · benötigt: gre_the_marshals_hour · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Streitkräfte der UdSSR: Moral (Heer) +4 % `COLDWAR_SOV_armed_forces_modifier`
  - Nomenklatura +5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ Die Politoffiziere unter Armeegeneral Jepischew.
- **The Defence Council** `COLDWAR_SOV_gre_the_defence_council` · Kosten 5 · benötigt: gre_the_marshals_hour · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - PP +50 `add_political_power`
  - Programm „The Marshal's Party“: PP-Gewinn +2 % `COLDWAR_SOV_gre_programme`
  - _Anmerkung:_ Der Verteidigungsrat der UdSSR wird zum eigentlichen Machtzentrum.
- **Mass Army or Nuclear Shield?** `COLDWAR_SOV_gre_the_doctrine` · Kosten 3 · benötigt: gre_the_general_staff_in_the_politburo, gre_yepishevs_political_directorate · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Erste Weiche – gegenseitig exklusiv
- **The Mass Army** `COLDWAR_SOV_gre_the_mass_army` · Kosten 5 · benötigt: gre_the_doctrine · schließt aus: gre_the_nuclear_shield · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Programm „The Marshal's Party“: Rekrutierbare Bevölkerung +5 %, Verteidigung (Heer) +2 % `COLDWAR_SOV_gre_programme`
  - Mannstärke +50.000 `add_manpower`
  - _Anmerkung:_ Gretschkos Vorliebe: Panzerarmeen und Reserven.
- **The Tank Armies of the West** `COLDWAR_SOV_gre_the_tank_armies_of_the_west` · Kosten 5 · benötigt: gre_the_mass_army · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Streitkräfte der UdSSR: Durchbruch +3 % `COLDWAR_SOV_armed_forces_modifier`
  - Forschungsbonus CAT_main_battle_tanks +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ Die Gruppe der Sowjetischen Streitkräfte in Deutschland.
- **Mobilisation Reserves** `COLDWAR_SOV_gre_mobilisation_reserves` · Kosten 5 · benötigt: gre_the_tank_armies_of_the_west · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Streitkräfte der UdSSR: Mobilmachungsgeschwindigkeit +10 % `COLDWAR_SOV_armed_forces_modifier`
  - Gosplan – Planwirtschaft: Konsumgüter +1 % `COLDWAR_SOV_gosplan_modifier`
- **The Nuclear Shield** `COLDWAR_SOV_gre_the_nuclear_shield` · Kosten 5 · benötigt: gre_the_doctrine · schließt aus: gre_the_mass_army · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Forschungsbonus CAT_intercontinental_ballistic_missiles +75 % ×1 `add_tech_bonus`
  - Programm „The Marshal's Party“: Kriegsgrund-Zeit gegen uns +10 % `COLDWAR_SOV_gre_programme`
- **The Strategic Triad** `COLDWAR_SOV_gre_the_strategic_triad` · Kosten 5 · benötigt: gre_the_nuclear_shield · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Forschungsbonus CAT_missile_submarines, CAT_heavy_aircraft +50 % ×1 `add_tech_bonus`
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
- **Against SALT** `COLDWAR_SOV_gre_against_salt` · Kosten 5 · benötigt: gre_the_strategic_triad · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
- **The Far Eastern Command** `COLDWAR_SOV_gre_the_far_eastern_command` · Kosten 5 · benötigt: gre_the_defence_council · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Streitkräfte der UdSSR: Verteidigung auf Kerngebiet +5 % `COLDWAR_SOV_armed_forces_modifier`
  - Gebäude: Luftwaffenbasis `one_air_base`
  - _Anmerkung:_ Ab 1979 als eigenes Oberkommando.
- **Suvorov and Nakhimov Schools** `COLDWAR_SOV_gre_suvorov_schools` · Kosten 5 · benötigt: gre_the_far_eastern_command · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Streitkräfte der UdSSR: Ausbildungszeit -5 % `COLDWAR_SOV_armed_forces_modifier`
  - Offiziersausbildung +1 Stufe `increase_officer_training_level`
- **The Army as the School of the Nation** `COLDWAR_SOV_gre_the_school_of_the_nation` · Kosten 5 · benötigt: gre_suvorov_schools · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Zusammenhalt der Union +4 `COLDWAR_SOV_change_union_cohesion`
  - Union der Republiken: Ideologische Driftabwehr +3 % `COLDWAR_SOV_union_modifier`
  - _Anmerkung:_ Russisch als Kommandosprache, Völkerfreundschaft in der Kaserne.
- **Arms for Allies** `COLDWAR_SOV_gre_arms_for_allies` · Kosten 5 · benötigt: gre_the_defence_council · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Streitkräfte der UdSSR: Erlöse Waffenmarkt +10 % `COLDWAR_SOV_armed_forces_modifier`
  - Sozialistische Gemeinschaft: Kosten Militärprogramme (Cold War) -10 % `COLDWAR_SOV_commonwealth_modifier`
- **The Military Advisers** `COLDWAR_SOV_gre_the_military_advisers` · Kosten 5 · benötigt: gre_arms_for_allies · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Angebot an EGY, SYR, IRQ (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Militärberater und Ausbildung. Bei Annahme: Partner +5 % Organisation, Meinung +15 `COLDWAR_SOV_offer_gre_advisers`
- **After the Marshal** `COLDWAR_SOV_gre_the_heir_of_the_marshal` · Kosten 3 · benötigt: gre_mobilisation_reserves oder gre_against_salt, gre_the_school_of_the_nation, gre_the_military_advisers · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`); Datum ≥ 01.01.1975
  - Gretschko stirbt historisch im April 1976 – zweite Weiche, gegenseitig exklusiv
- **Heir: Ustinov** `COLDWAR_SOV_gre_heir_ustinov` · Kosten 5 · benötigt: gre_the_heir_of_the_marshal · schließt aus: gre_return_to_civilian_rule, gre_the_council_of_marshals · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Erbe festgelegt: Dmitri Ustinow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_ust`, Event setzt den Politbüro-Fokus um)
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - _Anmerkung:_ Historisch wurde Ustinow 1976 Gretschkos Nachfolger als Minister.
- **Return to Civilian Rule** `COLDWAR_SOV_gre_return_to_civilian_rule` · Kosten 5 · benötigt: gre_the_heir_of_the_marshal · schließt aus: gre_heir_ustinov, gre_the_council_of_marshals · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Erbe festgelegt: Konstantin Tschernenko übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_che`, Event setzt den Politbüro-Fokus um)
  - Stabilität +3 % `add_stability`
  - Nomenklatura +10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **The Council of Marshals** `COLDWAR_SOV_gre_the_council_of_marshals` · Kosten 7 · benötigt: gre_the_heir_of_the_marshal · schließt aus: gre_heir_ustinov, gre_return_to_civilian_rule · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Regierungspartei → Council of Marshals (Military Junta) `change_ruling_party_effect`, Staatschef Andrei Grechko `create_country_leader` – Militärregierung
  - Stabilität -5 % `add_stability`
  - _Anmerkung:_ Endet den KPdSU-Weg: Wechsel zu Partei 22 (Council of Marshals).
- **The Garrison Party** `COLDWAR_SOV_gre_the_garrison_party` · Kosten 7 · benötigt: gre_heir_ustinov oder gre_return_to_civilian_rule · verfügbar: `emerging_communist_state_are_in_power`; Andrei Gretschko ist Generalsekretär (`COLDWAR_SOV_gensec_gre`)
  - Idee „The Garrison Party“: Organisation (Heer) +3 %, Verteidigung (Heer) +2 %, Kriegsunterstützung +3 %, Konsumgüter +2 % (`add_ideas`)

### Generalsekretär: Marschall Dmitri Ustinow (23)

General des Rüstungskomplexes: ZK-Sekretär für Verteidigungsindustrie, Politbüro ab März 1976, lebt bis Dezember 1984. Qualität oder Masse, Raketenmänner, SS-20.

- **The Armourer** `COLDWAR_SOV_ust_the_armourer` · Kosten 3 · benötigt: ple_ust · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Programm „The Armourer's Course“: Ausrüstungskosten -5 %, Steuer Rüstungsindustrie +5 %, Forschung +2 %, Konsumgüter +2 % `COLDWAR_SOV_ust_programme`
  - Rüstungskomplex (VPK) +10 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - _Anmerkung:_ Volkskommissar für Rüstung schon 1941, Marschall ab 1976.
- **Smirnov's Commission** `COLDWAR_SOV_ust_the_military_industrial_commission` · Kosten 5 · benötigt: ust_the_armourer · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Gosplan – Planwirtschaft: Bau Rüstungsfabriken +10 % `COLDWAR_SOV_gosplan_modifier`
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - _Anmerkung:_ Leonid Smirnow und die VPK beim Ministerrat.
- **The Design Bureaus** `COLDWAR_SOV_ust_the_design_bureaus` · Kosten 5 · benötigt: ust_the_armourer · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Gebäude: Luftfahrt-Versuchsanstalt `one_random_air_facility`
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Tupolew, Suchoi, Mikojan, Tschelomei, Jangel.
- **The Nine Ministries** `COLDWAR_SOV_ust_the_nine_ministries` · Kosten 5 · benötigt: ust_the_armourer · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Streitkräfte der UdSSR: Ausrüstungskosten -3 % `COLDWAR_SOV_armed_forces_modifier`
  - Der Parteistaat: Bürokratiekosten +3 % `COLDWAR_SOV_party_state_modifier`
- **Quality or Quantity?** `COLDWAR_SOV_ust_quality_or_quantity` · Kosten 3 · benötigt: ust_the_military_industrial_commission, ust_the_design_bureaus · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Erste Weiche – gegenseitig exklusiv
- **Quality** `COLDWAR_SOV_ust_quality` · Kosten 5 · benötigt: ust_quality_or_quantity · schließt aus: ust_quantity · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Programm „The Armourer's Course“: Forschung +3 % `COLDWAR_SOV_ust_programme`
  - Streitkräfte der UdSSR: Ausrüstungskosten +3 % `COLDWAR_SOV_armed_forces_modifier`
- **The Fourth Generation** `COLDWAR_SOV_ust_the_fourth_generation` · Kosten 7 · benötigt: ust_quality · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Forschungsbonus CAT_medium_aircraft +50 % ×2 `add_tech_bonus`
  - Spezialprojekt `sp:sp_aircraft_project` +15 % Fortschritt `add_project_progress_ratio`
- **T-80 and the Gas Turbine** `COLDWAR_SOV_ust_t80_and_the_gas_turbine` · Kosten 5 · benötigt: ust_the_fourth_generation · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Forschungsbonus CAT_main_battle_tanks, CAT_tank_engines +50 % ×1 `add_tech_bonus`
- **Quantity** `COLDWAR_SOV_ust_quantity` · Kosten 5 · benötigt: ust_quality_or_quantity · schließt aus: ust_quality · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Gebäude: Rüstungsfabriken `two_random_arms_factory`, Kosten 1.2 % BIP statt MD-Pauschale (`skip_payment`)
  - Streitkräfte der UdSSR: Ausrüstungskosten -4 % `COLDWAR_SOV_armed_forces_modifier`
- **Standardise the Arsenal** `COLDWAR_SOV_ust_standardise_the_arsenal` · Kosten 5 · benötigt: ust_quantity · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Streitkräfte der UdSSR: Effizienzerhalt bei Linienwechsel +10 % `COLDWAR_SOV_armed_forces_modifier`
  - Gosplan – Planwirtschaft: Effizienzzuwachs +2 % `COLDWAR_SOV_gosplan_modifier`
- **The Stockpiles** `COLDWAR_SOV_ust_the_stockpiles` · Kosten 5 · benötigt: ust_standardise_the_arsenal · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Gebäude: Treibstofflager `one_fuel_reserve`
  - Streitkräfte der UdSSR: Versorgungsverbrauch -2 % `COLDWAR_SOV_armed_forces_modifier`
- **The Rocket Men** `COLDWAR_SOV_ust_the_rocket_men` · Kosten 5 · benötigt: ust_the_nine_ministries · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Forschungsbonus CAT_intercontinental_ballistic_missiles, CAT_orbital_launch_vehicles +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ Gluschko, Tschelomei, Utkin.
- **SS-20 Deployment** `COLDWAR_SOV_ust_ss20_deployment` · Kosten 5 · benötigt: ust_the_rocket_men · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Forschungsbonus CAT_intermediate_range_ballistic_missiles +75 % ×1 `add_tech_bonus`
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
  - Meinung GER -10 `add_opinion_modifier`
- **Energia-Buran** `COLDWAR_SOV_ust_energia_buran` · Kosten 7 · benötigt: ust_ss20_deployment · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Kosten 2 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Spezialprojekt `sp:sp_space_program` +20 % Fortschritt `add_project_progress_ratio`
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
- **The Closed Cities** `COLDWAR_SOV_ust_the_closed_cities` · Kosten 5 · benötigt: ust_the_design_bureaus · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Gebäude: Kernforschungsanlage `one_random_nuclear_facility`
  - Streitkräfte der UdSSR: Ausrüstungskosten -2 % `COLDWAR_SOV_armed_forces_modifier`
- **Dual-Use Lines** `COLDWAR_SOV_ust_dual_use_lines` · Kosten 5 · benötigt: ust_the_closed_cities · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Gosplan – Planwirtschaft: Konsumgüter -2 % `COLDWAR_SOV_gosplan_modifier`
  - Gebäude: Zivilfabrik `one_random_industrial_complex`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - _Anmerkung:_ Die Rüstungsministerien liefern Kühlschränke und Fernseher – das Einzige, was die Konsumenten von ihnen sehen.
- **The Afghan Question** `COLDWAR_SOV_ust_the_foreign_line` · Kosten 3 · benötigt: ust_dual_use_lines, ust_energia_buran · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Gegenseitig exklusiv
- **The Hawk of Kabul** `COLDWAR_SOV_ust_the_hawk` · Kosten 5 · benötigt: ust_the_foreign_line · schließt aus: ust_arms_not_soldiers · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Streitkräfte der UdSSR: Heereserfahrung/Tag +0.02 `COLDWAR_SOV_armed_forces_modifier`
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - _Anmerkung:_ Ustinow drängte im Dezember 1979 auf die Intervention.
- **Arms, Not Soldiers** `COLDWAR_SOV_ust_arms_not_soldiers` · Kosten 5 · benötigt: ust_the_foreign_line · schließt aus: ust_the_hawk · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Streitkräfte der UdSSR: Erlöse Waffenmarkt +10 % `COLDWAR_SOV_armed_forces_modifier`
  - Stabilität +2 % `add_stability`
- **The Armourer's Heir** `COLDWAR_SOV_ust_the_heir` · Kosten 3 · benötigt: ust_the_hawk oder ust_arms_not_soldiers, ust_t80_and_the_gas_turbine oder ust_the_stockpiles · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Nachfolge – gegenseitig exklusiv (Ustinow stirbt historisch im Dezember 1984)
- **Heir: Romanov** `COLDWAR_SOV_ust_heir_romanov` · Kosten 5 · benötigt: ust_the_heir · schließt aus: ust_heir_gorbachev · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Erbe festgelegt: Grigori Romanow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_gro`, Event setzt den Politbüro-Fokus um)
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
- **Heir: Gorbachev** `COLDWAR_SOV_ust_heir_gorbachev` · Kosten 5 · benötigt: ust_the_heir · schließt aus: ust_heir_romanov · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Erbe festgelegt: Michail Gorbatschow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_gor`, Event setzt den Politbüro-Fokus um)
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
- **The Arsenal of Socialism** `COLDWAR_SOV_ust_the_arsenal_of_socialism` · Kosten 7 · benötigt: ust_heir_romanov oder ust_heir_gorbachev · verfügbar: `emerging_communist_state_are_in_power`; Dmitri Ustinow ist Generalsekretär (`COLDWAR_SOV_gensec_ust`)
  - Idee „The Arsenal of Socialism“: Ausrüstungskosten -5 %, Bau Rüstungsfabriken +10 %, Konsumgüter +2 % (`add_ideas`)

### Generalsekretär: Grigori Romanow (18)

Hardliner-Technokrat aus Leningrad (Erster Sekretär ab 1970, Politbüro ab März 1976). Technokratische Härte oder eiserne Disziplin, Wissenschafts-Produktions-Vereinigungen, Flottenstadt Leningrad.

- **The Leningrad Order** `COLDWAR_SOV_gro_the_leningrad_order` · Kosten 3 · benötigt: ple_gro · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Programm „The Leningrad Order“: Fabrikleistung (zivil) +3 %, Ideologische Driftabwehr +5 %, Korruptionskosten -5 %, Stabilität +2 % `COLDWAR_SOV_gro_programme`
- **The Leningrad Cadres** `COLDWAR_SOV_gro_the_leningrad_cadres` · Kosten 5 · benötigt: gro_the_leningrad_order · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Programm „The Leningrad Order“: PP-Gewinn +3 % `COLDWAR_SOV_gro_programme`
- **The Kirov Works** `COLDWAR_SOV_gro_the_kirov_works` · Kosten 5 · benötigt: gro_the_leningrad_order · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Gebäude: Rüstungsfabrik `one_random_arms_factory`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - _Anmerkung:_ Kirow-Werk, LOMO, Admiralitätswerft – Leningrads Rüstungsgürtel.
- **Science-Production Associations** `COLDWAR_SOV_gro_science_production_associations` · Kosten 5 · benötigt: gro_the_leningrad_order · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Der Parteistaat: Forschung +3 % `COLDWAR_SOV_party_state_modifier`
  - Gosplan – Planwirtschaft: Max. Fabrikeffizienz +2 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Das Leningrader Modell der NPOs.
- **Technocracy or Iron Discipline?** `COLDWAR_SOV_gro_the_path` · Kosten 3 · benötigt: gro_the_leningrad_cadres, gro_science_production_associations · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Erste Weiche – gegenseitig exklusiv
- **Hardline Technocracy** `COLDWAR_SOV_gro_hardline_technocracy` · Kosten 5 · benötigt: gro_the_path · schließt aus: gro_iron_discipline · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Programm „The Leningrad Order“: Produktivitätswachstum +4 %, Forschung +2 % `COLDWAR_SOV_gro_programme`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
- **The Intensive Economy** `COLDWAR_SOV_gro_the_intensive_economy` · Kosten 5 · benötigt: gro_hardline_technocracy · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
- **Automated Plants** `COLDWAR_SOV_gro_automated_plants` · Kosten 5 · benötigt: gro_the_intensive_economy · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Forschungsbonus CAT_robotics +50 % ×1 `add_tech_bonus`
  - Gebäude: Mikrochipwerk `one_random_microchip_plant`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
- **Iron Discipline** `COLDWAR_SOV_gro_iron_discipline` · Kosten 5 · benötigt: gro_the_path · schließt aus: gro_hardline_technocracy · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Programm „The Leningrad Order“: Stabilität +4 %, Ideologische Driftabwehr +10 % `COLDWAR_SOV_gro_programme`
  - Politbüro-Balance +0.10 Richtung Orthodoxe `add_power_balance_value`
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - Politbüro der Republiken: Pripiski kosten zusätzlich Stabilität −3 % bei der Republik, die sie meldet
- **No Rock, No Jeans** `COLDWAR_SOV_gro_no_rock_no_jeans` · Kosten 5 · benötigt: gro_iron_discipline · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Der Parteistaat: Fremde Subversion -10 % `COLDWAR_SOV_party_state_modifier`
  - Stabilität -1 % `add_stability`
  - Committee for Human Rights -2 % Popularität (Outlook -2 %) `change_relative_party_popularity`
  - _Anmerkung:_ Romanows Leningrad war berüchtigt für seine Härte gegen die Subkultur.
- **The Purge of the Lazy** `COLDWAR_SOV_gro_the_purge_of_the_lazy` · Kosten 5 · benötigt: gro_no_rock_no_jeans · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Korruption −1 Stufe `decrease_corruption`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +2 % `COLDWAR_SOV_gosplan_modifier`
- **The Naval Capital** `COLDWAR_SOV_gro_the_naval_capital` · Kosten 5 · benötigt: gro_the_kirov_works · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Gebäude: Werft `one_random_dockyard`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
  - Streitkräfte der UdSSR: Organisation Marine +3 % `COLDWAR_SOV_armed_forces_modifier`
- **No Concessions** `COLDWAR_SOV_gro_no_concessions` · Kosten 5 · benötigt: gro_the_naval_capital · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Sozialistische Gemeinschaft: Handelsmeinung -5 % `COLDWAR_SOV_commonwealth_modifier`
- **The Baltic Fortress** `COLDWAR_SOV_gro_the_baltic_fortress` · Kosten 5 · benötigt: gro_no_concessions · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Streitkräfte der UdSSR: Verteidigung auf Kerngebiet +3 % `COLDWAR_SOV_armed_forces_modifier`
  - Zusammenhalt der Union -2 `COLDWAR_SOV_change_union_cohesion`
  - Union der Republiken: Ideologische Driftabwehr +3 % `COLDWAR_SOV_union_modifier`
- **Romanov's Line** `COLDWAR_SOV_gro_the_heir` · Kosten 3 · benötigt: gro_automated_plants oder gro_the_purge_of_the_lazy, gro_the_baltic_fortress · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Zweite Weiche – gegenseitig exklusiv
- **The Strong Hand** `COLDWAR_SOV_gro_the_strong_hand` · Kosten 5 · benötigt: gro_the_heir · schließt aus: gro_the_technocrats_succession · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Programm „The Leningrad Order“: PP-Gewinn +5 %, Stabilität +2 % `COLDWAR_SOV_gro_programme`
  - Staatschef erhält Trait „Strong Hand“ `add_country_leader_trait`
- **The Technocrats' Succession** `COLDWAR_SOV_gro_the_technocrats_succession` · Kosten 5 · benötigt: gro_the_heir · schließt aus: gro_the_strong_hand · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Erbe festgelegt: Dmitri Ustinow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_ust`, Event setzt den Politbüro-Fokus um)
  - Gosplan – Planwirtschaft: Effizienzzuwachs +2 % `COLDWAR_SOV_gosplan_modifier`
- **The Ordered Union** `COLDWAR_SOV_gro_the_ordered_union` · Kosten 7 · benötigt: gro_the_strong_hand oder gro_the_technocrats_succession · verfügbar: `emerging_communist_state_are_in_power`; Grigori Romanow ist Generalsekretär (`COLDWAR_SOV_gensec_gro`)
  - Idee „The Ordered Union“: Produktivitätswachstum +4 %, Stabilität +3 %, Ideologische Driftabwehr +5 % (`add_ideas`)

### Generalsekretär: Konstantin Tschernenko (17)

Der Apparatschik (Politbüro ab November 1978, lebt bis März 1985). Kontinuität oder vorsichtige Öffnung, Briefe des Volkes, Schulreform, kranker Mann im Kreml.

- **The Apparatchik** `COLDWAR_SOV_che_the_apparatchik` · Kosten 3 · hist. · benötigt: ple_che · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Programm „Chernenko's Continuity“: PP-Gewinn +5 %, Bürokratiekosten +5 %, Stabilität +3 %, Produktivitätswachstum -3 % `COLDWAR_SOV_che_programme`
- **The General Department** `COLDWAR_SOV_che_the_general_department` · Kosten 5 · hist. · benötigt: che_the_apparatchik · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Der Parteistaat: Bürokratiekosten -5 % `COLDWAR_SOV_party_state_modifier`
  - PP +50 `add_political_power`
- **Letters from the People** `COLDWAR_SOV_che_letters_from_the_people` · Kosten 5 · hist. · benötigt: che_the_apparatchik · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Stabilität +3 % `add_stability`
  - Der Parteistaat: PP-Gewinn +2 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Tschernenkos Abteilung für Bürgerbriefe – das Ohr des Apparats.
- **Continuity or Opening?** `COLDWAR_SOV_che_the_path` · Kosten 3 · hist. · benötigt: che_the_general_department, che_letters_from_the_people · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Erste Weiche – gegenseitig exklusiv
- **Continuity** `COLDWAR_SOV_che_continuity` · Kosten 5 · hist. · benötigt: che_the_path · schließt aus: che_a_cautious_opening · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Programm „Chernenko's Continuity“: Stabilität +3 % `COLDWAR_SOV_che_programme`
  - Nomenklatura +10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **The Ideology Plenum** `COLDWAR_SOV_che_the_ideology_plenum` · Kosten 5 · hist. · benötigt: che_continuity · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Der Parteistaat: Ideologische Driftabwehr +5 % `COLDWAR_SOV_party_state_modifier`
  - Communist Party of the Soviet Union +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
  - _Anmerkung:_ Juni 1983.
- **A Cautious Opening** `COLDWAR_SOV_che_a_cautious_opening` · Kosten 5 · benötigt: che_the_path · schließt aus: che_continuity · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Programm „Chernenko's Continuity“: Produktivitätswachstum +3 % `COLDWAR_SOV_che_programme`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
- **The School Reform** `COLDWAR_SOV_che_the_school_reform` · Kosten 5 · hist. · benötigt: che_a_cautious_opening · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Gosplan – Planwirtschaft: Bildungskosten +3 %, Arbeitskräfte +2 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ 1984: Berufsbildung in allen Schulen.
- **The Food Programme Continued** `COLDWAR_SOV_che_the_food_programme_continued` · Kosten 5 · hist. · benötigt: che_the_ideology_plenum oder che_the_school_reform · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Gosplan – Planwirtschaft: Agrarproduktivität +3 % `COLDWAR_SOV_gosplan_modifier`
- **Talk or Boycott?** `COLDWAR_SOV_che_the_foreign_line` · Kosten 3 · benötigt: che_the_food_programme_continued · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Gegenseitig exklusiv
- **The Peace Offensive** `COLDWAR_SOV_che_the_peace_offensive` · Kosten 5 · benötigt: che_the_foreign_line · schließt aus: che_the_olympic_boycott · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Neue Abrüstungsgespräche in Genf. Bei Annahme: Spannung −2 `COLDWAR_SOV_offer_chernenko_talks`
- **The Olympic Boycott** `COLDWAR_SOV_che_the_olympic_boycott` · Kosten 5 · hist. · benötigt: che_the_foreign_line · schließt aus: che_the_peace_offensive · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Meinung USA -15 `add_opinion_modifier`
  - Stabilität +2 % `add_stability`
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
  - _Anmerkung:_ Los Angeles 1984.
- **The Emphysema** `COLDWAR_SOV_che_the_emphysema` · Kosten 3 · hist. · benötigt: che_the_peace_offensive oder che_the_olympic_boycott · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Nachfolge – gegenseitig exklusiv (Tschernenko stirbt historisch im März 1985)
- **Heir: Gorbachev** `COLDWAR_SOV_che_heir_gorbachev` · Kosten 5 · hist. · benötigt: che_the_emphysema · schließt aus: che_heir_grishin, che_heir_romanov · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Erbe festgelegt: Michail Gorbatschow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_gor`, Event setzt den Politbüro-Fokus um)
- **Heir: Grishin** `COLDWAR_SOV_che_heir_grishin` · Kosten 5 · benötigt: che_the_emphysema · schließt aus: che_heir_gorbachev, che_heir_romanov · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Neuer Staatschef: Viktor Grishin `create_country_leader`, Trait „Moscow Boss“ `COLDWAR_SOV_moscow_boss` – beim Tod Tschernenkos; Tschernenkos Programm bleibt
  - Nomenklatura +10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ Moskaus Parteichef seit 1967 – der Kandidat der Alten.
- **Heir: Romanov** `COLDWAR_SOV_che_heir_romanov` · Kosten 5 · benötigt: che_the_emphysema · schließt aus: che_heir_gorbachev, che_heir_grishin · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Erbe festgelegt: Grigori Romanow übernimmt beim Tod oder Rücktritt (Flag `COLDWAR_SOV_heir_gro`, Event setzt den Politbüro-Fokus um)
- **The Last of the Old Guard** `COLDWAR_SOV_che_the_last_of_the_old_guard` · Kosten 5 · benötigt: che_heir_gorbachev oder che_heir_grishin oder che_heir_romanov · verfügbar: `emerging_communist_state_are_in_power`; Konstantin Tschernenko ist Generalsekretär (`COLDWAR_SOV_gensec_che`)
  - Idee „The Old Guard“: Stabilität +4 %, PP-Gewinn +4 %, Produktivitätswachstum -2 % (`add_ideas`)

### Generalsekretär: Michail Gorbatschow (24)

Die neue Generation (Politbüro ab Oktober 1980). Beschleunigung oder Glasnost zuerst, Perestroika, neues Denken, Unionsvertrag – und die Frage, wie weit die Reform geht.

- **The New Generation** `COLDWAR_SOV_gor_the_new_generation` · Kosten 3 · hist. · benötigt: ple_gor · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Programm „Perestroika“: Forschung +3 %, Produktivitätswachstum +3 %, Demokratische Drift +0.01, Stabilität -2 % `COLDWAR_SOV_gor_programme`
- **Ryzhkov and Ligachev** `COLDWAR_SOV_gor_ryzhkov_and_ligachev` · Kosten 5 · hist. · benötigt: gor_the_new_generation · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Gosplan – Planwirtschaft: Effizienzzuwachs +2 % `COLDWAR_SOV_gosplan_modifier`
  - Korruption −1 Stufe `decrease_corruption`
- **Yakovlev Returns from Ottawa** `COLDWAR_SOV_gor_yakovlev_returns` · Kosten 5 · hist. · benötigt: gor_the_new_generation · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Socialist Market Commonwealth +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
- **Shevardnadze at the Foreign Ministry** `COLDWAR_SOV_gor_shevardnadze_at_the_foreign_ministry` · Kosten 5 · hist. · benötigt: gor_the_new_generation · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Cold-War-Spannung -1 `mdcw_cw_add_tension`
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
- **Acceleration or Glasnost?** `COLDWAR_SOV_gor_the_path` · Kosten 3 · hist. · benötigt: gor_ryzhkov_and_ligachev, gor_yakovlev_returns · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Erste Weiche – gegenseitig exklusiv
- **Uskorenie** `COLDWAR_SOV_gor_uskorenie` · Kosten 5 · hist. · benötigt: gor_the_path · schließt aus: gor_glasnost_first · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Programm „Perestroika“: Produktivitätswachstum +4 % `COLDWAR_SOV_gor_programme`
  - Kosten 1 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Forschungsbonus CAT_production_lines +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ 1985/86: Beschleunigung durch Maschinenbau.
- **The Anti-Alcohol Campaign** `COLDWAR_SOV_gor_the_anti_alcohol_campaign` · Kosten 5 · hist. · benötigt: gor_uskorenie · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Gosplan – Planwirtschaft: Steuereinnahmen -5 %, Produktivitätswachstum +2 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität -3 % `add_stability`
  - _Anmerkung:_ Mai 1985: der Staatshaushalt verliert die Wodkaeinnahmen.
- **The State Enterprise Law** `COLDWAR_SOV_gor_the_state_enterprise_law` · Kosten 5 · hist. · benötigt: gor_the_anti_alcohol_campaign · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Gosplan – Planwirtschaft: Produktivitätswachstum +4 % `COLDWAR_SOV_gosplan_modifier`
  - Branchenministerien -10 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
- **Glasnost First** `COLDWAR_SOV_gor_glasnost_first` · Kosten 5 · benötigt: gor_the_path · schließt aus: gor_uskorenie · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Programm „Perestroika“: Forschung +3 %, Ideologische Driftabwehr -10 % `COLDWAR_SOV_gor_programme`
  - Stabilität -2 % `add_stability`
- **The Blank Spots of History** `COLDWAR_SOV_gor_the_blank_spots` · Kosten 5 · benötigt: gor_glasnost_first · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Stabilität -2 % `add_stability`
  - Union of Democratic Socialists +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Committee for Human Rights +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
- **Release Sakharov** `COLDWAR_SOV_gor_release_sakharov` · Kosten 5 · benötigt: gor_the_blank_spots · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Entfernt „Samizdat and Dissent“ `remove_ideas`
  - Meinung USA +15 `add_opinion_modifier`
  - Committee for Human Rights +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - _Anmerkung:_ Dezember 1986: der Anruf in Gorki.
- **The Cooperative Law** `COLDWAR_SOV_gor_the_cooperative_law` · Kosten 5 · hist. · benötigt: gor_the_state_enterprise_law oder gor_release_sakharov · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - ersetzt „The Second Economy“: Idee „Cooperative Sector“: Steuereinnahmen +3 %, Konsumgüter -3 %, Korruptionskosten +5 % (`swap_ideas`)
- **New Thinking** `COLDWAR_SOV_gor_new_thinking` · Kosten 5 · hist. · benötigt: gor_shevardnadze_at_the_foreign_ministry · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Cold-War-Spannung -3 `mdcw_cw_add_tension`
  - Sozialistische Gemeinschaft: Handelsmeinung +5 % `COLDWAR_SOV_commonwealth_modifier`
- **The Zero Option** `COLDWAR_SOV_gor_the_zero_option` · Kosten 5 · hist. · benötigt: gor_new_thinking · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Abbau aller Mittelstreckenraketen (INF). Bei Annahme: Spannung −4, beide Kosten Verteidigungshaushalt −5 % `COLDWAR_SOV_offer_inf_treaty`
  - Armee & Generalstab -10 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **Leave Afghanistan** `COLDWAR_SOV_gor_leave_afghanistan` · Kosten 5 · hist. · benötigt: gor_the_zero_option · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Beendet „The Afghan Burden“ mit Rückzugsplan (Event an AFG)
  - Stabilität +3 % `add_stability`
  - Armee & Generalstab -5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **The Sinatra Doctrine** `COLDWAR_SOV_gor_the_sinatra_doctrine` · Kosten 5 · hist. · benötigt: gor_leave_afghanistan · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Cold-War-Spannung -3 `mdcw_cw_add_tension`
  - Entfernt „The Brezhnev Doctrine“ `remove_ideas`
  - Sozialistische Gemeinschaft: Steuereinnahmen +3 % `COLDWAR_SOV_commonwealth_modifier`
  - Zusammenhalt der Union -3 `COLDWAR_SOV_change_union_cohesion`
- **Demokratizatsiya** `COLDWAR_SOV_gor_democratisation` · Kosten 5 · hist. · benötigt: gor_the_cooperative_law · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Stabilität -3 % `add_stability`
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
  - Nomenklatura -15 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **The Congress of People's Deputies** `COLDWAR_SOV_gor_the_congress_of_peoples_deputies` · Kosten 7 · hist. · benötigt: gor_democratisation · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Halbfreie Wahlen erlaubt `set_politics`
  - Communist Party of the Soviet Union -5 % Popularität (Outlook -5 %) `change_relative_party_popularity`
  - Stabilität -3 % `add_stability`
- **The New Union Treaty** `COLDWAR_SOV_gor_the_union_treaty` · Kosten 7 · hist. · benötigt: gor_the_congress_of_peoples_deputies, gor_the_sinatra_doctrine · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Zusammenhalt der Union +12 `COLDWAR_SOV_change_union_cohesion`
  - Der Parteistaat: PP-Gewinn -5 % `COLDWAR_SOV_party_state_modifier`
- **How Far?** `COLDWAR_SOV_gor_how_far` · Kosten 3 · hist. · benötigt: gor_the_union_treaty · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Zweite Weiche – gegenseitig exklusiv
- **Humane, Democratic Socialism** `COLDWAR_SOV_gor_humane_democratic_socialism` · Kosten 5 · benötigt: gor_how_far · schließt aus: gor_the_social_democratic_turn, gor_the_presidency · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Stabilität +3 % `add_stability`
  - Programm „Perestroika“: Stabilität +3 % `COLDWAR_SOV_gor_programme`
  - _Anmerkung:_ Die Programmerklärung von 1990 – innerhalb der KPdSU.
- **The Social-Democratic Turn** `COLDWAR_SOV_gor_the_social_democratic_turn` · Kosten 7 · benötigt: gor_how_far · schließt aus: gor_humane_democratic_socialism, gor_the_presidency · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Regierungspartei → Union of Democratic Socialists (Socialism) `change_ruling_party_effect`, Staatschef Mikhail Gorbachev `create_country_leader` – Gorbatschow führt die Sozialdemokraten
  - Stabilität -3 % `add_stability`
  - _Anmerkung:_ Endet den KPdSU-Weg: Wechsel zu Partei 3.
- **The Presidency of the USSR** `COLDWAR_SOV_gor_the_presidency` · Kosten 5 · hist. · benötigt: gor_how_far · schließt aus: gor_humane_democratic_socialism, gor_the_social_democratic_turn · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Staatschef erhält Trait „President of the USSR“ `add_country_leader_trait`
  - PP +100 `add_political_power`
  - Entfernt „Stability of Cadres“ `remove_ideas`
  - Politbüro der Republiken: Föderationsrat (März 1990): Das Sitz-System endet, alle Republiken beraten den Präsidenten, Sitz-Buffs entfallen
  - _Anmerkung:_ März 1990.
- **The Common European Home** `COLDWAR_SOV_gor_the_common_european_home` · Kosten 7 · benötigt: gor_humane_democratic_socialism oder gor_the_presidency · verfügbar: `emerging_communist_state_are_in_power`; Michail Gorbatschow ist Generalsekretär (`COLDWAR_SOV_gensec_gor`)
  - Idee „The Common European Home“: Handelsmeinung +15 %, Forschung +3 %, Stabilität +2 % (`add_ideas`)

### Partei: Free Councils of Labour (5) (17)

Alt-Hist: Die Erinnerung an Nowotscherkassk 1962 wird zur Räterevolution. Fabrikräte oder Kommunen, Selbstverwaltung statt Ministerien.

- **All Power to the Councils** `COLDWAR_SOV_wc_all_power_to_the_councils` · Kosten 3 · benötigt: power_councils oder em_the_leading_role_of_the_party · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Programm „Council Communism“: Stabilität -3 %, Konsumgüter -3 %, Kommunistische Drift +0.02, Bürokratiekosten -10 % `COLDWAR_SOV_wc_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **The Novocherkassk Memory** `COLDWAR_SOV_wc_the_novocherkassk_memory` · Kosten 5 · benötigt: wc_all_power_to_the_councils · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Stabilität +3 % `add_stability`
  - Gewerkschaften (VTsSPS) +15 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
  - _Anmerkung:_ Juni 1962: Streik und Massaker von Nowotscherkassk – Pjotr Siuda war dabei.
- **Dissolve the Ministries** `COLDWAR_SOV_wc_dissolve_the_ministries` · Kosten 5 · benötigt: wc_all_power_to_the_councils · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Branchenministerien -20 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
  - Der Parteistaat: Bürokratiekosten -10 % `COLDWAR_SOV_party_state_modifier`
  - Idee „Transition to Self-Management“: Produktivitätswachstum -5 %, Stabilität -3 % (365 Tage `add_timed_idea`)
- **Factory or Village?** `COLDWAR_SOV_wc_the_council_question` · Kosten 3 · benötigt: wc_the_novocherkassk_memory, wc_dissolve_the_ministries · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Gegenseitig exklusiv
- **Factory Councils** `COLDWAR_SOV_wc_factory_councils` · Kosten 5 · benötigt: wc_the_council_question · schließt aus: wc_the_rural_communes · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Programm „Council Communism“: Produktivitätswachstum +4 %, Steuer Zivilindustrie +3 % `COLDWAR_SOV_wc_programme`
- **The Congress of Councils** `COLDWAR_SOV_wc_the_congress_of_councils` · Kosten 5 · benötigt: wc_factory_councils · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Stabilität +3 % `add_stability`
  - Der Parteistaat: PP-Gewinn +3 % `COLDWAR_SOV_party_state_modifier`
- **The Rural Communes** `COLDWAR_SOV_wc_the_rural_communes` · Kosten 5 · benötigt: wc_the_council_question · schließt aus: wc_factory_councils · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Programm „Council Communism“: Agrarproduktivität +8 % `COLDWAR_SOV_wc_programme`
  - Kolchosbauern +10 `COLDWAR_SOV_change_farmers_opinion_exact` → `change_farmers_opinion`
- **Land to the Communes** `COLDWAR_SOV_wc_land_to_the_communes` · Kosten 5 · benötigt: wc_the_rural_communes · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Gosplan – Planwirtschaft: Konsumgüter -2 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität +2 % `add_stability`
- **The Federation of Councils** `COLDWAR_SOV_wc_the_federation_of_councils` · Kosten 5 · benötigt: wc_the_congress_of_councils oder wc_land_to_the_communes · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Zusammenhalt der Union +5 `COLDWAR_SOV_change_union_cohesion`
- **Abolish the Nomenklatura** `COLDWAR_SOV_wc_abolish_the_nomenklatura` · Kosten 5 · benötigt: wc_the_federation_of_councils · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Korruption −2 Stufe `decrease_corruption`
  - Nomenklatura -25 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Stabilität -3 % `add_stability`
- **Workers' Militias** `COLDWAR_SOV_wc_workers_militias` · Kosten 5 · benötigt: wc_the_federation_of_councils · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Streitkräfte der UdSSR: Rekrutierbare Bevölkerung +5 %, Organisation (Heer) -3 % `COLDWAR_SOV_armed_forces_modifier`
  - Mannstärke +30.000 `add_manpower`
- **Leave the Arms Race** `COLDWAR_SOV_wc_leave_the_arms_race` · Kosten 5 · benötigt: wc_workers_militias · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Verteidigungshaushalt −1 Stufe `decrease_military_spending`
  - Cold-War-Spannung -2 `mdcw_cw_add_tension`
  - Armee & Generalstab -15 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **International of Councils** `COLDWAR_SOV_wc_international_of_councils` · Kosten 5 · benötigt: wc_abolish_the_nomenklatura · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Meinung SER +15 `add_opinion_modifier`
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +5 % `COLDWAR_SOV_commonwealth_modifier`
- **The Revolution's Course** `COLDWAR_SOV_wc_the_revolutions_course` · Kosten 3 · benötigt: wc_leave_the_arms_race, wc_international_of_councils · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Gegenseitig exklusiv
- **Permanent Revolution** `COLDWAR_SOV_wc_permanent_revolution` · Kosten 5 · benötigt: wc_the_revolutions_course · schließt aus: wc_the_councils_settle · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Stabilität -5 % `add_stability`
  - Kriegsunterstützung +5 % `add_war_support`
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +15 % `COLDWAR_SOV_commonwealth_modifier`
- **The Councils Settle** `COLDWAR_SOV_wc_the_councils_settle` · Kosten 5 · benötigt: wc_the_revolutions_course · schließt aus: wc_permanent_revolution · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Stabilität +5 % `add_stability`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
- **The Commune State** `COLDWAR_SOV_wc_the_commune_state` · Kosten 7 · benötigt: wc_permanent_revolution oder wc_the_councils_settle · verfügbar: `emerging_anarchist_communism_are_in_power`
  - Idee „The Commune State“: Stabilität +3 %, Produktivitätswachstum +3 %, Kommunistische Drift +0.02 (`add_ideas`)

### Partei: Neo-Stalinist Platform (6) (17)

Neostalinistische Plattform um Sergei Trapesnikow (ZK-Wissenschaftsabteilung): Rehabilitierung Stalins, Mobilisierungswirtschaft, Kampagnen.

- **The Iron Line** `COLDWAR_SOV_ns_the_iron_line` · Kosten 3 · benötigt: power_iron_line oder em_the_leading_role_of_the_party · verfügbar: `emerging_reactionaries_are_in_power`
  - Programm „The Iron Line“: Stabilität +5 %, PP-Gewinn +5 %, Forschung -3 %, Ideologische Driftabwehr +15 %, Produktivitätswachstum -3 % `COLDWAR_SOV_ns_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **Rehabilitate the Vozhd** `COLDWAR_SOV_ns_rehabilitate_the_vozhd` · Kosten 5 · benötigt: ns_the_iron_line · verfügbar: `emerging_reactionaries_are_in_power`
  - Neo-Stalinist Platform +5 % Popularität (Outlook +5 %) `change_relative_party_popularity`
  - Zusammenhalt der Union -4 `COLDWAR_SOV_change_union_cohesion`
  - Meinung CHI +10 `add_opinion_modifier`
  - Stabilität +2 % `add_stability`
  - _Anmerkung:_ Peking hat Stalin nie verurteilt – ein unerwartetes Signal an Mao.
- **The Mobilisation Economy** `COLDWAR_SOV_ns_the_mobilisation_economy` · Kosten 5 · benötigt: ns_the_iron_line · verfügbar: `emerging_reactionaries_are_in_power`
  - Gebäude: Rüstungsfabriken `two_random_arms_factory`, Kosten 1.2 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Konsumgüter +3 %, Produktivitätswachstum -2 % `COLDWAR_SOV_gosplan_modifier`
- **Plans or Cadres?** `COLDWAR_SOV_ns_the_question` · Kosten 3 · benötigt: ns_rehabilitate_the_vozhd, ns_the_mobilisation_economy · verfügbar: `emerging_reactionaries_are_in_power`
  - Gegenseitig exklusiv
- **The New Industrialisation** `COLDWAR_SOV_ns_the_new_industrialisation` · Kosten 5 · benötigt: ns_the_question · schließt aus: ns_cadres_decide_everything · verfügbar: `emerging_reactionaries_are_in_power`
  - Programm „The Iron Line“: Fabrikleistung (zivil) +5 % `COLDWAR_SOV_ns_programme`
  - Stabilität -3 % `add_stability`
- **Shock Workers** `COLDWAR_SOV_ns_shock_workers` · Kosten 5 · benötigt: ns_the_new_industrialisation · verfügbar: `emerging_reactionaries_are_in_power`
  - Gosplan – Planwirtschaft: Effizienzzuwachs +5 % `COLDWAR_SOV_gosplan_modifier`
  - Gewerkschaften (VTsSPS) -5 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
- **Cadres Decide Everything** `COLDWAR_SOV_ns_cadres_decide_everything` · Kosten 5 · benötigt: ns_the_question · schließt aus: ns_the_new_industrialisation · verfügbar: `emerging_reactionaries_are_in_power`
  - Nomenklatura +15 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Programm „The Iron Line“: PP-Gewinn +5 % `COLDWAR_SOV_ns_programme`
- **The New Purge** `COLDWAR_SOV_ns_the_new_purge` · Kosten 5 · benötigt: ns_cadres_decide_everything · verfügbar: `emerging_reactionaries_are_in_power`
  - Korruption −2 Stufe `decrease_corruption`
  - Stabilität -5 % `add_stability`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - KGB +10 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
- **The Great Patriotic Spirit** `COLDWAR_SOV_ns_the_patriotic_spirit` · Kosten 5 · benötigt: ns_shock_workers oder ns_the_new_purge · verfügbar: `emerging_reactionaries_are_in_power`
  - Kriegsunterstützung +5 % `add_war_support`
  - Streitkräfte der UdSSR: Moral (Heer) +3 % `COLDWAR_SOV_armed_forces_modifier`
- **The Closed Economy** `COLDWAR_SOV_ns_the_closed_economy` · Kosten 5 · benötigt: ns_the_patriotic_spirit · verfügbar: `emerging_reactionaries_are_in_power`
  - Handelsgesetz → Geschlossene Wirtschaft `add_ideas` (md_closed_economy)
  - Der Parteistaat: Sanktionsresistenz (Imperia) +10 % `COLDWAR_SOV_party_state_modifier`
- **Tighten the Kolkhozy** `COLDWAR_SOV_ns_collective_farms_tightened` · Kosten 5 · benötigt: ns_the_patriotic_spirit · verfügbar: `emerging_reactionaries_are_in_power`
  - Gosplan – Planwirtschaft: Agrarproduktivität +3 % `COLDWAR_SOV_gosplan_modifier`
  - Kolchosbauern -10 `COLDWAR_SOV_change_farmers_opinion_exact` → `change_farmers_opinion`
- **A Stalinist Hand to Mao** `COLDWAR_SOV_ns_reconcile_with_mao` · Kosten 5 · benötigt: ns_the_closed_economy · verfügbar: `emerging_reactionaries_are_in_power`
  - Angebot an CHI (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Gemeinsame Rückkehr zur „reinen Linie“. Bei Annahme: Meinung +30, „The Ussuri Frontier“ entfällt `COLDWAR_SOV_offer_stalinist_reconciliation`
- **The Iron Curtain Reinforced** `COLDWAR_SOV_ns_the_iron_curtain_reinforced` · Kosten 5 · benötigt: ns_collective_farms_tightened · verfügbar: `emerging_reactionaries_are_in_power`
  - Der Parteistaat: Ideologische Driftabwehr +10 % `COLDWAR_SOV_party_state_modifier`
  - Gosplan – Planwirtschaft: Handelsmeinung -10 % `COLDWAR_SOV_gosplan_modifier`
- **A New Vozhd?** `COLDWAR_SOV_ns_the_leadership_question` · Kosten 3 · benötigt: ns_reconcile_with_mao, ns_the_iron_curtain_reinforced · verfügbar: `emerging_reactionaries_are_in_power`
  - Gegenseitig exklusiv
- **A New Vozhd** `COLDWAR_SOV_ns_a_new_vozhd` · Kosten 5 · benötigt: ns_the_leadership_question · schließt aus: ns_collective_stalinism · verfügbar: `emerging_reactionaries_are_in_power`
  - Programm „The Iron Line“: PP-Gewinn +10 %, Stabilität +3 % `COLDWAR_SOV_ns_programme`
  - Staatschef erhält Trait „The New Vozhd“ `add_country_leader_trait`
- **Collective Stalinism** `COLDWAR_SOV_ns_collective_stalinism` · Kosten 5 · benötigt: ns_the_leadership_question · schließt aus: ns_a_new_vozhd · verfügbar: `emerging_reactionaries_are_in_power`
  - Stabilität +4 % `add_stability`
  - Nomenklatura +10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **The Second Industrialisation** `COLDWAR_SOV_ns_the_second_industrialisation` · Kosten 7 · benötigt: ns_a_new_vozhd oder ns_collective_stalinism · verfügbar: `emerging_reactionaries_are_in_power`
  - Idee „The Second Industrialisation“: Fabrikleistung (zivil) +5 %, Baugeschwindigkeit +5 %, Konsumgüter +2 % (`add_ideas`)

### Partei: Komsomol Vanguard (7) (17)

Schelepins „Komsomolzen“ als persönliche Herrschaft: der Führerstaat, Jugendbrigaden, Sicherheitsapparat. Auch Endpunkt von Schelepins KPdSU-Weg.

- **The Leader State** `COLDWAR_SOV_kv_the_leader_state` · Kosten 3 · benötigt: power_komsomol oder em_the_leading_role_of_the_party · verfügbar: `emerging_autocracy_are_in_power`
  - Programm „The Komsomol Vanguard“: PP-Gewinn +10 %, Stabilität +3 %, Ideologische Driftabwehr +10 %, Polizeikosten +5 % `COLDWAR_SOV_kv_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **The Vozhd Principle** `COLDWAR_SOV_kv_the_vozhd_principle` · Kosten 5 · benötigt: kv_the_leader_state · verfügbar: `emerging_autocracy_are_in_power`
  - Staatschef erhält Trait „Vozhd“ `add_country_leader_trait`
  - PP +50 `add_political_power`
- **The Youth Vanguard** `COLDWAR_SOV_kv_the_youth_vanguard` · Kosten 5 · benötigt: kv_the_leader_state · verfügbar: `emerging_autocracy_are_in_power`
  - Mannstärke +20.000 `add_manpower`
  - Gosplan – Planwirtschaft: Baugeschwindigkeit +3 % `COLDWAR_SOV_gosplan_modifier`
- **Which Pillar?** `COLDWAR_SOV_kv_the_pillar` · Kosten 3 · benötigt: kv_the_vozhd_principle, kv_the_youth_vanguard · verfügbar: `emerging_autocracy_are_in_power`
  - Gegenseitig exklusiv
- **The Security State** `COLDWAR_SOV_kv_the_security_state` · Kosten 5 · benötigt: kv_the_pillar · schließt aus: kv_mass_mobilisation · verfügbar: `emerging_autocracy_are_in_power`
  - Programm „The Komsomol Vanguard“: Ideologische Abwehr (Cold War) +15 % `COLDWAR_SOV_kv_programme`
  - KGB +15 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
- **Every Third an Informer** `COLDWAR_SOV_kv_the_informers` · Kosten 5 · benötigt: kv_the_security_state · verfügbar: `emerging_autocracy_are_in_power`
  - Der Parteistaat: Fremde Subversion -15 % `COLDWAR_SOV_party_state_modifier`
  - Stabilität -2 % `add_stability`
- **Mass Mobilisation** `COLDWAR_SOV_kv_mass_mobilisation` · Kosten 5 · benötigt: kv_the_pillar · schließt aus: kv_the_security_state · verfügbar: `emerging_autocracy_are_in_power`
  - Programm „The Komsomol Vanguard“: Kriegsunterstützung +5 % `COLDWAR_SOV_kv_programme`
  - Komsomol Vanguard +5 % Popularität (Outlook +5 %) `change_relative_party_popularity`
- **The Great Campaigns** `COLDWAR_SOV_kv_the_great_campaigns` · Kosten 5 · benötigt: kv_mass_mobilisation · verfügbar: `emerging_autocracy_are_in_power`
  - Gosplan – Planwirtschaft: Baugeschwindigkeit +5 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität +2 % `add_stability`
- **Purge the Old Men** `COLDWAR_SOV_kv_purge_the_old_men` · Kosten 5 · benötigt: kv_the_informers oder kv_the_great_campaigns · verfügbar: `emerging_autocracy_are_in_power`
  - Nomenklatura -20 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Entfernt „Stability of Cadres“ `remove_ideas`
  - Stabilität -3 % `add_stability`
- **Construction Battalions** `COLDWAR_SOV_kv_construction_battalions` · Kosten 5 · benötigt: kv_purge_the_old_men · verfügbar: `emerging_autocracy_are_in_power`
  - Gebäude: Infrastruktur `two_random_infrastructure`
  - Gosplan – Planwirtschaft: Bau Infrastruktur +10 % `COLDWAR_SOV_gosplan_modifier`
- **Discipline in the Factories** `COLDWAR_SOV_kv_discipline_in_the_factories` · Kosten 5 · benötigt: kv_purge_the_old_men · verfügbar: `emerging_autocracy_are_in_power`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +4 % `COLDWAR_SOV_gosplan_modifier`
  - Gewerkschaften (VTsSPS) -10 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
- **The Iron Fist Abroad** `COLDWAR_SOV_kv_the_iron_fist_abroad` · Kosten 5 · benötigt: kv_construction_battalions · verfügbar: `emerging_autocracy_are_in_power`
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
  - Streitkräfte der UdSSR: Angriff (Heer) +2 % `COLDWAR_SOV_armed_forces_modifier`
- **The Eastern Opening** `COLDWAR_SOV_kv_the_eastern_opening` · Kosten 5 · benötigt: kv_discipline_in_the_factories · verfügbar: `emerging_autocracy_are_in_power`
  - Angebot an CHI (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Pragmatische Annäherung zweier Führerstaaten. Bei Annahme: Meinung +20, Spannung −1 `COLDWAR_SOV_offer_komsomol_china`
- **After the Vozhd** `COLDWAR_SOV_kv_the_succession` · Kosten 3 · benötigt: kv_the_iron_fist_abroad, kv_the_eastern_opening · verfügbar: `emerging_autocracy_are_in_power`
  - Gegenseitig exklusiv
- **Heir: Semichastny** `COLDWAR_SOV_kv_heir_semichastny` · Kosten 5 · benötigt: kv_the_succession · schließt aus: kv_return_to_the_party · verfügbar: `emerging_autocracy_are_in_power`
  - Flag `COLDWAR_SOV_heir_semichastny`
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
- **Return to the Party** `COLDWAR_SOV_kv_return_to_the_party` · Kosten 5 · benötigt: kv_the_succession · schließt aus: kv_heir_semichastny · verfügbar: `emerging_autocracy_are_in_power`
  - Regierungspartei → Communist Party of the Soviet Union (Communist State) `change_ruling_party_effect`, Staatschef Alexander Shelepin `create_country_leader`
  - Stabilität +3 % `add_stability`
  - _Anmerkung:_ Die Herrschaft kehrt in die KPdSU zurück; das Plenum kann neu entscheiden.
- **The Vanguard State** `COLDWAR_SOV_kv_the_vanguard_state` · Kosten 7 · benötigt: kv_heir_semichastny · verfügbar: `emerging_autocracy_are_in_power`
  - Idee „The Vanguard State“: PP-Gewinn +5 %, Stabilität +4 %, Ideologische Driftabwehr +10 % (`add_ideas`)

### Partei: Systems Directorate (0) (14)

Alt-Hist: Die „Systemleute“ um Dschermen Gwischiani (Kossygins Schwiegersohn, IIASA-Gründer) – autoritäre, westlich orientierte Managerherrschaft.

- **The Systems Men Rule** `COLDWAR_SOV_sd_the_systems_men_rule` · Kosten 3 · benötigt: power_systems_men oder we_a_democratic_union · verfügbar: `western_autocrats_are_in_power`
  - Programm „The Systems Directorate“: Produktivitätswachstum +5 %, Forschung +3 %, Stabilität -3 %, Demokratische Drift +0.01 `COLDWAR_SOV_sd_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **The IIASA Partnership** `COLDWAR_SOV_sd_the_iiasa_partnership` · Kosten 5 · benötigt: sd_the_systems_men_rule · verfügbar: `western_autocrats_are_in_power`
  - Der Parteistaat: Forschung +3 % `COLDWAR_SOV_party_state_modifier`
  - Meinung USA +10 `add_opinion_modifier`
  - _Anmerkung:_ Das Internationale Institut für Angewandte Systemanalyse (Laxenburg, 1972).
- **The Managerial Revolution** `COLDWAR_SOV_sd_the_managerial_revolution` · Kosten 5 · benötigt: sd_the_systems_men_rule · verfügbar: `western_autocrats_are_in_power`
  - Nomenklatura -15 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
- **Technocracy or Corporation?** `COLDWAR_SOV_sd_the_form` · Kosten 3 · benötigt: sd_the_iiasa_partnership, sd_the_managerial_revolution · verfügbar: `western_autocrats_are_in_power`
  - Gegenseitig exklusiv
- **The Technocratic State** `COLDWAR_SOV_sd_the_technocratic_state` · Kosten 5 · benötigt: sd_the_form · schließt aus: sd_the_corporate_union · verfügbar: `western_autocrats_are_in_power`
  - Programm „The Systems Directorate“: PP-Gewinn +5 %, Polizeikosten +5 % `COLDWAR_SOV_sd_programme`
  - Stabilität +3 % `add_stability`
- **The Corporate Union** `COLDWAR_SOV_sd_the_corporate_union` · Kosten 5 · benötigt: sd_the_form · schließt aus: sd_the_technocratic_state · verfügbar: `western_autocrats_are_in_power`
  - Programm „The Systems Directorate“: Kosten für Investoren bei uns -15 %, Handelsmeinung +10 % `COLDWAR_SOV_sd_programme`
  - Kredit: Treasury +1 % BIP, Schulden +1 % BIP `COLDWAR_SOV_receive_gdp_share` `modify_debt_effect`
- **Western Licences** `COLDWAR_SOV_sd_western_licences` · Kosten 5 · benötigt: sd_the_technocratic_state oder sd_the_corporate_union · verfügbar: `western_autocrats_are_in_power`
  - Forschungsbonus CAT_production_lines, CAT_electronics +50 % ×1 `add_tech_bonus`
- **The Computer Ministry** `COLDWAR_SOV_sd_the_computer_ministry` · Kosten 5 · benötigt: sd_western_licences · verfügbar: `western_autocrats_are_in_power`
  - Gebäude: Mikrochipwerk `one_random_microchip_plant`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
  - Forschungsbonus CAT_computing +50 % ×1 `add_tech_bonus`
- **Rationalise the Army** `COLDWAR_SOV_sd_rationalise_the_army` · Kosten 5 · benötigt: sd_the_technocratic_state oder sd_the_corporate_union · verfügbar: `western_autocrats_are_in_power`
  - Verteidigungshaushalt −1 Stufe `decrease_military_spending`
  - Streitkräfte der UdSSR: Ausrüstungskosten -5 % `COLDWAR_SOV_armed_forces_modifier`
  - Armee & Generalstab -10 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **Lift the CoCom Lists** `COLDWAR_SOV_sd_cocom_relaxation` · Kosten 5 · benötigt: sd_rationalise_the_army · verfügbar: `western_autocrats_are_in_power`
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Lockerung der westlichen Exportkontrollen. Bei Annahme: Forschungsbonus Elektronik ×2, Spannung −2 `COLDWAR_SOV_offer_cocom`
- **The Future of the Directorate** `COLDWAR_SOV_sd_the_future_of_the_directorate` · Kosten 3 · benötigt: sd_the_computer_ministry, sd_cocom_relaxation · verfügbar: `western_autocrats_are_in_power`
  - Gegenseitig exklusiv
- **The Permanent Directorate** `COLDWAR_SOV_sd_the_permanent_directorate` · Kosten 5 · benötigt: sd_the_future_of_the_directorate · schließt aus: sd_hand_over_to_parliament · verfügbar: `western_autocrats_are_in_power`
  - Programm „The Systems Directorate“: Stabilität +3 % `COLDWAR_SOV_sd_programme`
  - PP +50 `add_political_power`
- **Hand Over to Parliament** `COLDWAR_SOV_sd_hand_over_to_parliament` · Kosten 5 · benötigt: sd_the_future_of_the_directorate · schließt aus: sd_the_permanent_directorate · verfügbar: `western_autocrats_are_in_power`
  - Wahlen erlaubt `set_politics`
  - Regierungspartei → Committee for Human Rights (Liberalism) `change_ruling_party_effect`, Staatschef Andrei Sakharov `create_country_leader`
  - Stabilität -3 % `add_stability`
  - _Anmerkung:_ Übergabe an Partei 2 (Liberale).
- **The Managed Union** `COLDWAR_SOV_sd_the_managed_union` · Kosten 7 · benötigt: sd_the_permanent_directorate · verfügbar: `western_autocrats_are_in_power`
  - Idee „The Managed Union“: Produktivitätswachstum +5 %, Forschung +3 % (`add_ideas`)

### Partei: People's Labour Union (NTS) (1) (13)

Alt-Hist: Der Volksarbeitsbund (NTS) aus Frankfurt kehrt zurück – Solidarismus, Privateigentum, Kirche, Westbindung.

- **The Solidarists Return** `COLDWAR_SOV_nts_the_solidarists_return` · Kosten 3 · benötigt: power_solidarists oder we_a_democratic_union · verfügbar: `western_conservatism_are_in_power`
  - Programm „Russian Solidarism“: Demokratische Drift +0.02, Stabilität -3 %, Handelsmeinung +10 % `COLDWAR_SOV_nts_programme`
  - Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 60)
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **The Church Restored** `COLDWAR_SOV_nts_the_church_restored` · Kosten 5 · benötigt: nts_the_solidarists_return · verfügbar: `western_conservatism_are_in_power`
  - Stabilität +3 % `add_stability`
  - Moskauer Patriarchat +10 `COLDWAR_SOV_change_the_clergy_opinion_exact` → `change_the_clergy_opinion`
  - House of Romanov +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
- **Private Property Restored** `COLDWAR_SOV_nts_private_property` · Kosten 5 · benötigt: nts_the_solidarists_return · verfügbar: `western_conservatism_are_in_power`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +5 %, Konsumgüter -3 % `COLDWAR_SOV_gosplan_modifier`
  - Nomenklatura -20 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **Solidarism or Free Market?** `COLDWAR_SOV_nts_the_model` · Kosten 3 · benötigt: nts_the_church_restored, nts_private_property · verfügbar: `western_conservatism_are_in_power`
  - Gegenseitig exklusiv
- **Solidarist Corporatism** `COLDWAR_SOV_nts_solidarist_corporatism` · Kosten 5 · benötigt: nts_the_model · schließt aus: nts_free_market_russia · verfügbar: `western_conservatism_are_in_power`
  - Programm „Russian Solidarism“: Stabilität +3 % `COLDWAR_SOV_nts_programme`
  - Gewerkschaften (VTsSPS) +10 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
- **A Free Market** `COLDWAR_SOV_nts_free_market_russia` · Kosten 5 · benötigt: nts_the_model · schließt aus: nts_solidarist_corporatism · verfügbar: `western_conservatism_are_in_power`
  - Programm „Russian Solidarism“: Produktivitätswachstum +5 %, Stabilität -2 % `COLDWAR_SOV_nts_programme`
  - Handelsgesetz → Gemischte Wirtschaft `add_ideas` (mixed_economy)
- **Decollectivisation** `COLDWAR_SOV_nts_decollectivisation` · Kosten 5 · benötigt: nts_solidarist_corporatism oder nts_free_market_russia · verfügbar: `western_conservatism_are_in_power`
  - Gosplan – Planwirtschaft: Agrarproduktivität +10 % `COLDWAR_SOV_gosplan_modifier`
  - Kolchosbauern +15 `COLDWAR_SOV_change_farmers_opinion_exact` → `change_farmers_opinion`
  - Stabilität -2 % `add_stability`
- **The Constituent Assembly** `COLDWAR_SOV_nts_the_constituent_assembly` · Kosten 5 · benötigt: nts_decollectivisation · verfügbar: `western_conservatism_are_in_power`
  - Wahlen erlaubt `set_politics`
  - Stabilität -3 % `add_stability`
  - Zusammenhalt der Union -3 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Die Antwort auf 1918.
- **Into the West** `COLDWAR_SOV_nts_into_the_west` · Kosten 5 · benötigt: nts_the_constituent_assembly · verfügbar: `western_conservatism_are_in_power`
  - Cold War: Wechsel in den Westblock (PP-frei, Fokus ist die Wahl) `mdcw_cw_change_alignment`
  - Meinung GER +20 `add_opinion_modifier`
  - Cold-War-Spannung -3 `mdcw_cw_add_tension`
- **The Republics Question** `COLDWAR_SOV_nts_the_republics_question` · Kosten 3 · benötigt: nts_into_the_west · verfügbar: `western_conservatism_are_in_power`
  - Gegenseitig exklusiv
- **A Russian Federation** `COLDWAR_SOV_nts_a_russian_federation` · Kosten 5 · benötigt: nts_the_republics_question · schließt aus: nts_a_union_of_nations · verfügbar: `western_conservatism_are_in_power`
  - Zusammenhalt der Union -15 `COLDWAR_SOV_change_union_cohesion`
  - Stabilität +5 % `add_stability`
  - Jede Republik erhält ein Angebot zur Unabhängigkeit (Event; Spieler-Republiken entscheiden selbst)
- **A Union of Nations** `COLDWAR_SOV_nts_a_union_of_nations` · Kosten 5 · benötigt: nts_the_republics_question · schließt aus: nts_a_russian_federation · verfügbar: `western_conservatism_are_in_power`
  - Zusammenhalt der Union +8 `COLDWAR_SOV_change_union_cohesion`
  - Stabilität -2 % `add_stability`
- **The New Russia** `COLDWAR_SOV_nts_the_new_russia` · Kosten 7 · benötigt: nts_a_russian_federation oder nts_a_union_of_nations · verfügbar: `western_conservatism_are_in_power`
  - Idee „The New Russia“: Produktivitätswachstum +4 %, Handelsmeinung +10 %, Stabilität +2 % (`add_ideas`)

### Partei: Committee for Human Rights (2) (15)

Andrei Sacharows Komitee für Menschenrechte (gegründet November 1970) übernimmt: Konvergenz, Rechtsstaat, Abrüstung.

- **The Committee Governs** `COLDWAR_SOV_chr_the_committee_governs` · Kosten 3 · benötigt: power_human_rights oder we_a_democratic_union · verfügbar: `western_liberals_are_in_power`
  - Programm „Sakharov's Convergence“: Forschung +5 %, Demokratische Drift +0.03, Stabilität -5 %, Handelsmeinung +15 % `COLDWAR_SOV_chr_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **Release the Prisoners of Conscience** `COLDWAR_SOV_chr_release_the_prisoners` · Kosten 5 · benötigt: chr_the_committee_governs · verfügbar: `western_liberals_are_in_power`
  - Stabilität -2 % `add_stability`
  - Meinung USA +20 `add_opinion_modifier`
  - Entfernt „Samizdat and Dissent“ `remove_ideas`
- **End the Party Monopoly** `COLDWAR_SOV_chr_end_the_party_monopoly` · Kosten 5 · benötigt: chr_the_committee_governs · verfügbar: `western_liberals_are_in_power`
  - Wahlen erlaubt `set_politics`
  - Nomenklatura -25 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Communist Party of the Soviet Union -10 % Popularität (Outlook -10 %) `change_relative_party_popularity`
- **Convergence or Social Market?** `COLDWAR_SOV_chr_the_economic_question` · Kosten 3 · benötigt: chr_release_the_prisoners, chr_end_the_party_monopoly · verfügbar: `western_liberals_are_in_power`
  - Gegenseitig exklusiv
- **The Convergence Economy** `COLDWAR_SOV_chr_the_convergence_economy` · Kosten 5 · benötigt: chr_the_economic_question · schließt aus: chr_the_social_market · verfügbar: `western_liberals_are_in_power`
  - Programm „Sakharov's Convergence“: Produktivitätswachstum +5 % `COLDWAR_SOV_chr_programme`
  - Handelsgesetz → Gemischte Wirtschaft `add_ideas` (mixed_economy)
- **The Social Market** `COLDWAR_SOV_chr_the_social_market` · Kosten 5 · benötigt: chr_the_economic_question · schließt aus: chr_the_convergence_economy · verfügbar: `western_liberals_are_in_power`
  - Programm „Sakharov's Convergence“: Stabilität +3 %, Sozialkosten +5 % `COLDWAR_SOV_chr_programme`
- **The Rule of Law** `COLDWAR_SOV_chr_the_rule_of_law` · Kosten 5 · benötigt: chr_the_convergence_economy oder chr_the_social_market · verfügbar: `western_liberals_are_in_power`
  - Korruption −1 Stufe `decrease_corruption`
  - Der Parteistaat: Polizeikosten -5 % `COLDWAR_SOV_party_state_modifier`
- **A Free Press** `COLDWAR_SOV_chr_a_free_press` · Kosten 5 · benötigt: chr_the_rule_of_law · verfügbar: `western_liberals_are_in_power`
  - Der Parteistaat: Ideologische Driftabwehr -10 %, Forschung +2 % `COLDWAR_SOV_party_state_modifier`
- **Disarmament** `COLDWAR_SOV_chr_disarmament` · Kosten 5 · benötigt: chr_the_committee_governs · verfügbar: `western_liberals_are_in_power`
  - Verteidigungshaushalt −1 Stufe `decrease_military_spending`
  - Verteidigungshaushalt −1 Stufe `decrease_military_spending`
  - Cold-War-Spannung -5 `mdcw_cw_add_tension`
  - Armee & Generalstab -20 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **The Convergence Treaty** `COLDWAR_SOV_chr_the_convergence_treaty` · Kosten 5 · benötigt: chr_disarmament · verfügbar: `western_liberals_are_in_power`
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Gemeinsame Abrüstung und Wissenschaftskooperation. Bei Annahme: Spannung −5, beide +3 % Forschung `COLDWAR_SOV_offer_convergence_treaty`
- **The Right to Leave** `COLDWAR_SOV_chr_the_union_question` · Kosten 3 · benötigt: chr_a_free_press, chr_the_convergence_treaty · verfügbar: `western_liberals_are_in_power`
  - Gegenseitig exklusiv
- **The Right of Secession** `COLDWAR_SOV_chr_the_right_of_secession` · Kosten 5 · benötigt: chr_the_union_question · schließt aus: chr_a_democratic_federation · verfügbar: `western_liberals_are_in_power`
  - Zusammenhalt der Union -10 `COLDWAR_SOV_change_union_cohesion`
  - Stabilität +3 % `add_stability`
  - Republiken erhalten ein Austrittsangebot (Event)
- **A Democratic Federation** `COLDWAR_SOV_chr_a_democratic_federation` · Kosten 5 · benötigt: chr_the_union_question · schließt aus: chr_the_right_of_secession · verfügbar: `western_liberals_are_in_power`
  - Zusammenhalt der Union +6 `COLDWAR_SOV_change_union_cohesion`
- **Join the Free World** `COLDWAR_SOV_chr_join_the_free_world` · Kosten 5 · benötigt: chr_the_right_of_secession oder chr_a_democratic_federation · verfügbar: `western_liberals_are_in_power`
  - Cold War: Wechsel in den Westblock (PP-frei, Fokus ist die Wahl) `mdcw_cw_change_alignment`
  - Cold-War-Spannung -3 `mdcw_cw_add_tension`
- **The Open Society** `COLDWAR_SOV_chr_the_open_society` · Kosten 7 · benötigt: chr_join_the_free_world · verfügbar: `western_liberals_are_in_power`
  - Idee „The Open Society“: Forschung +5 %, Handelsmeinung +10 %, Stabilität +2 % (`add_ideas`)

### Partei: Union of Democratic Socialists (3) (13)

Roy Medwedews „sozialistische Demokratie“ – Eurokommunismus, Mehrparteiensystem innerhalb des Sozialismus.

- **Socialist Democracy** `COLDWAR_SOV_uds_socialist_democracy` · Kosten 3 · benötigt: power_democratic_socialists oder we_a_democratic_union · verfügbar: `western_social_democrats_are_in_power`
  - Programm „Socialist Democracy“: Demokratische Drift +0.02, Stabilität -2 %, Forschung +3 %, Konsumgüter -2 % `COLDWAR_SOV_uds_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **Multi-Party Socialism** `COLDWAR_SOV_uds_multi_party_socialism` · Kosten 5 · benötigt: uds_socialist_democracy · verfügbar: `western_social_democrats_are_in_power`
  - Wahlen erlaubt `set_politics`
  - Union of Democratic Socialists +5 % Popularität (Outlook +5 %) `change_relative_party_popularity`
- **The Rehabilitations** `COLDWAR_SOV_uds_the_rehabilitations` · Kosten 5 · benötigt: uds_socialist_democracy · verfügbar: `western_social_democrats_are_in_power`
  - Stabilität -2 % `add_stability`
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Medwedews „Lasst die Geschichte urteilen“ als Staatsprogramm.
- **Rome or Stockholm?** `COLDWAR_SOV_uds_the_model` · Kosten 3 · benötigt: uds_multi_party_socialism, uds_the_rehabilitations · verfügbar: `western_social_democrats_are_in_power`
  - Gegenseitig exklusiv
- **The Eurocommunist Alliance** `COLDWAR_SOV_uds_eurocommunist_alliance` · Kosten 5 · benötigt: uds_the_model · schließt aus: uds_the_scandinavian_model · verfügbar: `western_social_democrats_are_in_power`
  - Meinung ITA +20 `add_opinion_modifier`
  - Meinung FRA +15 `add_opinion_modifier`
  - Programm „Socialist Democracy“: Handelsmeinung +5 % `COLDWAR_SOV_uds_programme`
- **The Scandinavian Model** `COLDWAR_SOV_uds_the_scandinavian_model` · Kosten 5 · benötigt: uds_the_model · schließt aus: uds_eurocommunist_alliance · verfügbar: `western_social_democrats_are_in_power`
  - Programm „Socialist Democracy“: Sozialkosten +5 %, Stabilität +5 % `COLDWAR_SOV_uds_programme`
- **Workers' Participation** `COLDWAR_SOV_uds_workers_participation` · Kosten 5 · benötigt: uds_eurocommunist_alliance oder uds_the_scandinavian_model · verfügbar: `western_social_democrats_are_in_power`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
  - Gewerkschaften (VTsSPS) +10 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
- **Cut the Defence Budget** `COLDWAR_SOV_uds_cut_the_defence_budget` · Kosten 5 · benötigt: uds_workers_participation · verfügbar: `western_social_democrats_are_in_power`
  - Verteidigungshaushalt −1 Stufe `decrease_military_spending`
  - Armee & Generalstab -10 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Cold-War-Spannung -2 `mdcw_cw_add_tension`
- **Detente Partners** `COLDWAR_SOV_uds_detente_partners` · Kosten 5 · benötigt: uds_cut_the_defence_budget · verfügbar: `western_social_democrats_are_in_power`
  - Angebot an GER, SWE (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Sozialdemokratische Partnerschaft. Bei Annahme: Meinung +20, Handelsabkommen `COLDWAR_SOV_offer_social_democratic_partners`
- **How Far?** `COLDWAR_SOV_uds_the_final_question` · Kosten 3 · benötigt: uds_detente_partners · verfügbar: `western_social_democrats_are_in_power`
  - Gegenseitig exklusiv
- **Socialism Remains** `COLDWAR_SOV_uds_socialism_remains` · Kosten 5 · benötigt: uds_the_final_question · schließt aus: uds_full_democracy · verfügbar: `western_social_democrats_are_in_power`
  - Stabilität +3 % `add_stability`
  - Union of Democratic Socialists +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
- **Full Democracy** `COLDWAR_SOV_uds_full_democracy` · Kosten 5 · benötigt: uds_the_final_question · schließt aus: uds_socialism_remains · verfügbar: `western_social_democrats_are_in_power`
  - Stabilität -2 % `add_stability`
  - Der Parteistaat: Demokratische Drift +0.02 `COLDWAR_SOV_party_state_modifier`
- **Socialism with a Human Face** `COLDWAR_SOV_uds_socialism_with_a_human_face` · Kosten 7 · benötigt: uds_socialism_remains oder uds_full_democracy · verfügbar: `western_social_democrats_are_in_power`
  - Idee „Socialism with a Human Face“: Stabilität +3 %, Forschung +3 %, Produktivitätswachstum +2 % (`add_ideas`)

### Partei: Gosplan Technocracy (13) (13)

Gosplan-Chef Nikolai Baibakow und die Technokraten: Herrschaft der Planer ohne Ideologie.

- **The Planners Govern** `COLDWAR_SOV_gt_the_planners_govern` · Kosten 3 · benötigt: power_planners oder na_neither_moscow_nor_washington · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Programm „Rule of the Planners“: Effizienzzuwachs +5 %, Bürokratiekosten -5 %, PP-Gewinn -3 % `COLDWAR_SOV_gt_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **Ideology Retired** `COLDWAR_SOV_gt_ideology_retired` · Kosten 5 · benötigt: gt_the_planners_govern · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Nomenklatura -20 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Der Parteistaat: Ideologische Driftabwehr -5 % `COLDWAR_SOV_party_state_modifier`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
- **The Material Balances** `COLDWAR_SOV_gt_the_material_balances` · Kosten 5 · benötigt: gt_the_planners_govern · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Gosplan – Planwirtschaft: Effizienzzuwachs +3 % `COLDWAR_SOV_gosplan_modifier`
- **Engineers or Resources?** `COLDWAR_SOV_gt_the_model` · Kosten 3 · benötigt: gt_ideology_retired, gt_the_material_balances · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Gegenseitig exklusiv
- **The Engineers' State** `COLDWAR_SOV_gt_the_engineers_state` · Kosten 5 · benötigt: gt_the_model · schließt aus: gt_the_resource_state · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Programm „Rule of the Planners“: Fabrikleistung (zivil) +5 % `COLDWAR_SOV_gt_programme`
- **The Resource State** `COLDWAR_SOV_gt_the_resource_state` · Kosten 5 · benötigt: gt_the_model · schließt aus: gt_the_engineers_state · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Programm „Rule of the Planners“: Öl-Exporterlöse +10 %, Rohstoff-Exporterlöse +5 % `COLDWAR_SOV_gt_programme`
- **Siberian Projects** `COLDWAR_SOV_gt_siberian_projects` · Kosten 5 · benötigt: gt_the_engineers_state oder gt_the_resource_state · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Kosten 1.5 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Gebäude: Infrastruktur `two_random_infrastructure`
- **Military Conversion** `COLDWAR_SOV_gt_military_conversion` · Kosten 5 · benötigt: gt_siberian_projects · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Verteidigungshaushalt −1 Stufe `decrease_military_spending`
  - Gosplan – Planwirtschaft: Konsumgüter -3 % `COLDWAR_SOV_gosplan_modifier`
  - Rüstungskomplex (VPK) -10 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
- **Trade with All** `COLDWAR_SOV_gt_trade_with_all` · Kosten 5 · benötigt: gt_siberian_projects · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Gosplan – Planwirtschaft: Handelsmeinung +10 % `COLDWAR_SOV_gosplan_modifier`
  - Cold-War-Spannung -1 `mdcw_cw_add_tension`
- **Technocracy Forever?** `COLDWAR_SOV_gt_the_future` · Kosten 3 · benötigt: gt_military_conversion, gt_trade_with_all · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Gegenseitig exklusiv
- **Permanent Technocracy** `COLDWAR_SOV_gt_permanent_technocracy` · Kosten 5 · benötigt: gt_the_future · schließt aus: gt_return_to_party_rule · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Programm „Rule of the Planners“: Stabilität +3 % `COLDWAR_SOV_gt_programme`
- **Return to Party Rule** `COLDWAR_SOV_gt_return_to_party_rule` · Kosten 5 · benötigt: gt_the_future · schließt aus: gt_permanent_technocracy · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Regierungspartei → Communist Party of the Soviet Union (Communist State) `change_ruling_party_effect`, Staatschef Leonid Brezhnev `create_country_leader`
  - Stabilität +3 % `add_stability`
- **The Planned Society** `COLDWAR_SOV_gt_the_planned_society` · Kosten 7 · benötigt: gt_permanent_technocracy · verfügbar: `neutrality_neutral_autocracy_are_in_power`
  - Idee „The Planned Society“: Max. Fabrikeffizienz +5 %, Produktivitätswachstum +3 % (`add_ideas`)

### Partei: Live Not by Lies (14) (13)

Alexander Solschenizyns „Brief an die Sowjetführer“ (1973): autoritär, orthodox, Russland zuerst, Abkehr von Ideologie und Imperium.

- **Live Not by Lies** `COLDWAR_SOV_lnl_live_not_by_lies` · Kosten 3 · benötigt: power_solzhenitsyn oder na_neither_moscow_nor_washington · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Programm „Repentance and Self-Limitation“: Stabilität +3 %, Forschung -2 %, Kommunistische Drift -0.02, Nationalistische Drift +0.01 `COLDWAR_SOV_lnl_programme`
  - Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 65)
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **Letter to the Soviet Leaders** `COLDWAR_SOV_lnl_letter_to_the_soviet_leaders` · Kosten 5 · benötigt: lnl_live_not_by_lies · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Communist Party of the Soviet Union -10 % Popularität (Outlook -10 %) `change_relative_party_popularity`
  - Nomenklatura -20 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Stabilität +2 % `add_stability`
  - _Anmerkung:_ 1973: Ideologie aufgeben, den Nordosten erschließen, das Imperium beenden.
- **Develop the North-East** `COLDWAR_SOV_lnl_the_north_east` · Kosten 5 · benötigt: lnl_live_not_by_lies · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Kosten 1 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Gebäude: Infrastruktur `two_random_infrastructure`
  - Gosplan – Planwirtschaft: Rohstoff-Exporterlöse +3 % `COLDWAR_SOV_gosplan_modifier`
- **Orthodoxy or Zemstvo?** `COLDWAR_SOV_lnl_the_form` · Kosten 3 · benötigt: lnl_letter_to_the_soviet_leaders, lnl_the_north_east · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Gegenseitig exklusiv
- **Authoritarian Orthodoxy** `COLDWAR_SOV_lnl_authoritarian_orthodoxy` · Kosten 5 · benötigt: lnl_the_form · schließt aus: lnl_the_zemstvo · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Programm „Repentance and Self-Limitation“: Stabilität +5 %, Ideologische Driftabwehr +10 % `COLDWAR_SOV_lnl_programme`
  - Moskauer Patriarchat +10 `COLDWAR_SOV_change_the_clergy_opinion_exact` → `change_the_clergy_opinion`
- **The Zemstvo Revived** `COLDWAR_SOV_lnl_the_zemstvo` · Kosten 5 · benötigt: lnl_the_form · schließt aus: lnl_authoritarian_orthodoxy · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Programm „Repentance and Self-Limitation“: Stabilität +2 %, Demokratische Drift +0.01 `COLDWAR_SOV_lnl_programme`
  - Der Parteistaat: Bürokratiekosten -5 % `COLDWAR_SOV_party_state_modifier`
- **End the Foreign Adventures** `COLDWAR_SOV_lnl_end_the_foreign_adventures` · Kosten 5 · benötigt: lnl_authoritarian_orthodoxy oder lnl_the_zemstvo · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Sozialistische Gemeinschaft: Steuereinnahmen +5 %, Auslandseinfluss -10 % `COLDWAR_SOV_commonwealth_modifier`
  - Cold-War-Spannung -2 `mdcw_cw_add_tension`
- **The Village Restored** `COLDWAR_SOV_lnl_the_village_restored` · Kosten 5 · benötigt: lnl_end_the_foreign_adventures · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Gosplan – Planwirtschaft: Agrarproduktivität +5 % `COLDWAR_SOV_gosplan_modifier`
  - Kolchosbauern +10 `COLDWAR_SOV_change_farmers_opinion_exact` → `change_farmers_opinion`
- **Release the Non-Slavic Republics** `COLDWAR_SOV_lnl_release_the_republics` · Kosten 5 · benötigt: lnl_end_the_foreign_adventures · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Zusammenhalt der Union -20 `COLDWAR_SOV_change_union_cohesion`
  - Stabilität +5 % `add_stability`
  - Baltikum, Kaukasus und Zentralasien erhalten Unabhängigkeitsangebote (Event)
  - _Anmerkung:_ Solschenizyns „Russlands Weg aus der Krise“ (1990), zwanzig Jahre früher.
- **The Slavic Question** `COLDWAR_SOV_lnl_the_slavic_question` · Kosten 3 · benötigt: lnl_the_village_restored, lnl_release_the_republics · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Gegenseitig exklusiv
- **The Slavic Union** `COLDWAR_SOV_lnl_the_slavic_union` · Kosten 5 · benötigt: lnl_the_slavic_question · schließt aus: lnl_russia_alone · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Angebot an UKR, BLR, KAZ (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Union der drei ostslawischen Völker (und Kasachstans). Bei Annahme: bleibt Unionsrepublik mit erweiterter Autonomie `COLDWAR_SOV_offer_slavic_union`
- **Russia Alone** `COLDWAR_SOV_lnl_russia_alone` · Kosten 5 · benötigt: lnl_the_slavic_question · schließt aus: lnl_the_slavic_union · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Stabilität +3 % `add_stability`
  - Zusammenhalt der Union -10 `COLDWAR_SOV_change_union_cohesion`
- **Repentance and Self-Limitation** `COLDWAR_SOV_lnl_repentance_and_self_limitation` · Kosten 7 · benötigt: lnl_the_slavic_union oder lnl_russia_alone · verfügbar: `neutrality_neutral_conservatism_are_in_power`
  - Idee „Repentance and Self-Limitation“: Stabilität +5 %, Konsumgüter -2 %, Kriegsunterstützung -3 % (`add_ideas`)

### Partei: The Red Directors (15) (13)

Die Roten Direktoren und das MWD von Nikolai Schtscholokow: Schattenwirtschaft, Clan-Netzwerke, Privatisierung der Nomenklatura.

- **The Directors Take Over** `COLDWAR_SOV_rd_the_directors_take_over` · Kosten 3 · benötigt: power_directors oder na_neither_moscow_nor_washington · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Programm „The Red Directors“: Körperschaftsteuer-Einnahmen +10 %, Korruptionskosten +10 %, Produktivitätswachstum +3 %, Konsumgüter -3 % `COLDWAR_SOV_rd_programme`
  - Fügt die Fraktion „Schattenwirtschaft“ hinzu (`oligarchs`, Meinung 70)
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **Shadow Capitalism Legalised** `COLDWAR_SOV_rd_shadow_capitalism` · Kosten 5 · benötigt: rd_the_directors_take_over · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - ersetzt „The Second Economy“: Idee „Shadow Capitalism“: Steuereinnahmen +3 %, Korruptionskosten +10 %, Konsumgüter -3 % (`swap_ideas`)
  - Schattenwirtschaft +10 `COLDWAR_SOV_change_oligarchs_opinion_exact` → `change_oligarchs_opinion`
- **The MVD State** `COLDWAR_SOV_rd_the_mvd_state` · Kosten 5 · benötigt: rd_the_directors_take_over · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Stabilität +2 % `add_stability`
  - Der Parteistaat: Polizeikosten -5 % `COLDWAR_SOV_party_state_modifier`
- **Nomenklatura or Clans?** `COLDWAR_SOV_rd_the_model` · Kosten 3 · benötigt: rd_shadow_capitalism, rd_the_mvd_state · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Gegenseitig exklusiv
- **Nomenklatura Privatisation** `COLDWAR_SOV_rd_nomenklatura_privatisation` · Kosten 5 · benötigt: rd_the_model · schließt aus: rd_the_clan_economy · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Programm „The Red Directors“: Produktivitätswachstum +5 % `COLDWAR_SOV_rd_programme`
  - Nomenklatura +15 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Stabilität -3 % `add_stability`
- **The Clan Economy** `COLDWAR_SOV_rd_the_clan_economy` · Kosten 5 · benötigt: rd_the_model · schließt aus: rd_nomenklatura_privatisation · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Zusammenhalt der Union +5 `COLDWAR_SOV_change_union_cohesion`
  - Korruption +1 Stufe `increase_corruption`
- **Cotton and Caviar** `COLDWAR_SOV_rd_cotton_and_caviar` · Kosten 5 · benötigt: rd_nomenklatura_privatisation oder rd_the_clan_economy · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Gosplan – Planwirtschaft: Rohstoff-Exporterlöse +10 % `COLDWAR_SOV_gosplan_modifier`
- **The Directors' Banks** `COLDWAR_SOV_rd_the_directors_banks` · Kosten 5 · benötigt: rd_cotton_and_caviar · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Gosplan – Planwirtschaft: Zinsen -5 %, Büro-Einnahmen +5 % `COLDWAR_SOV_gosplan_modifier`
  - Gebäude: Büro `one_office_construction`, Kosten 0.6 % BIP statt MD-Pauschale (`skip_payment`)
- **Western Accounts** `COLDWAR_SOV_rd_western_accounts` · Kosten 5 · benötigt: rd_cotton_and_caviar · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Kosten 0.5 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Schattenwirtschaft +10 `COLDWAR_SOV_change_oligarchs_opinion_exact` → `change_oligarchs_opinion`
  - Stabilität -2 % `add_stability`
  - _Anmerkung:_ Kapitalflucht: die Direktoren sichern sich ab.
- **Who Owns the Union?** `COLDWAR_SOV_rd_the_question` · Kosten 3 · benötigt: rd_the_directors_banks, rd_western_accounts · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Gegenseitig exklusiv
- **The Directors' Republic** `COLDWAR_SOV_rd_the_directors_republic` · Kosten 5 · benötigt: rd_the_question · schließt aus: rd_buy_the_people · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Programm „The Red Directors“: Körperschaftsteuer-Einnahmen +5 % `COLDWAR_SOV_rd_programme`
- **Buy the People** `COLDWAR_SOV_rd_buy_the_people` · Kosten 5 · benötigt: rd_the_question · schließt aus: rd_the_directors_republic · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Stabilität +5 % `add_stability`
  - Gosplan – Planwirtschaft: Sozialkosten +5 % `COLDWAR_SOV_gosplan_modifier`
- **The Corporate Union** `COLDWAR_SOV_rd_the_corporate_union` · Kosten 7 · benötigt: rd_the_directors_republic oder rd_buy_the_people · verfügbar: `neutrality_neutral_oligarch_are_in_power`
  - Idee „The Corporate Union“: Produktivitätswachstum +4 %, Korruptionskosten +5 %, Steuereinnahmen +3 % (`add_ideas`)

### Partei: Free Enterprise League (16) (9)

Alt-Hist: Ökonomen um Nikolai Schmeljow – schnelle Marktöffnung, Preisfreigabe, Privatisierung.

- **The Free Enterprise Cabinet** `COLDWAR_SOV_fel_the_free_enterprise_cabinet` · Kosten 3 · benötigt: power_free_enterprise oder na_neither_moscow_nor_washington · verfügbar: `neutrality_neutral_libertarians_are_in_power` · nur Spieler (KI nie)
  - Programm „Free Enterprise“: Produktivitätswachstum +8 %, Stabilität -6 %, Konsumgüter -4 % `COLDWAR_SOV_fel_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **Free the Prices** `COLDWAR_SOV_fel_free_the_prices` · Kosten 5 · benötigt: fel_the_free_enterprise_cabinet · verfügbar: `neutrality_neutral_libertarians_are_in_power` · nur Spieler (KI nie)
  - Stabilität -5 % `add_stability`
  - Entfernt „The Second Economy“ `remove_ideas`
  - Gosplan – Planwirtschaft: Steuereinnahmen +5 % `COLDWAR_SOV_gosplan_modifier`
- **A Convertible Rouble** `COLDWAR_SOV_fel_the_rouble_convertible` · Kosten 5 · benötigt: fel_the_free_enterprise_cabinet · verfügbar: `neutrality_neutral_libertarians_are_in_power` · nur Spieler (KI nie)
  - Gosplan – Planwirtschaft: Handelsmeinung +10 %, Zinsen +5 % `COLDWAR_SOV_gosplan_modifier`
- **Shock or Steps?** `COLDWAR_SOV_fel_the_speed` · Kosten 3 · benötigt: fel_free_the_prices, fel_the_rouble_convertible · verfügbar: `neutrality_neutral_libertarians_are_in_power` · nur Spieler (KI nie)
  - Gegenseitig exklusiv
- **Shock Therapy** `COLDWAR_SOV_fel_shock_therapy` · Kosten 5 · benötigt: fel_the_speed · schließt aus: fel_step_by_step · verfügbar: `neutrality_neutral_libertarians_are_in_power` · nur Spieler (KI nie)
  - Programm „Free Enterprise“: Produktivitätswachstum +5 % `COLDWAR_SOV_fel_programme`
  - Stabilität -8 % `add_stability`
- **Step by Step** `COLDWAR_SOV_fel_step_by_step` · Kosten 5 · benötigt: fel_the_speed · schließt aus: fel_shock_therapy · verfügbar: `neutrality_neutral_libertarians_are_in_power` · nur Spieler (KI nie)
  - Programm „Free Enterprise“: Stabilität +3 % `COLDWAR_SOV_fel_programme`
- **Voucher Privatisation** `COLDWAR_SOV_fel_voucher_privatisation` · Kosten 5 · benötigt: fel_shock_therapy oder fel_step_by_step · verfügbar: `neutrality_neutral_libertarians_are_in_power` · nur Spieler (KI nie)
  - Gosplan – Planwirtschaft: Körperschaftsteuer-Einnahmen +10 % `COLDWAR_SOV_gosplan_modifier`
  - Nomenklatura -20 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **Open to Investment** `COLDWAR_SOV_fel_open_to_investment` · Kosten 5 · benötigt: fel_voucher_privatisation · verfügbar: `neutrality_neutral_libertarians_are_in_power` · nur Spieler (KI nie)
  - Gosplan – Planwirtschaft: Kosten für Investoren bei uns -20 % `COLDWAR_SOV_gosplan_modifier`
  - Kredit: Treasury +1 % BIP, Schulden +1 % BIP `COLDWAR_SOV_receive_gdp_share` `modify_debt_effect`
- **The Market Union** `COLDWAR_SOV_fel_the_market_union` · Kosten 7 · benötigt: fel_open_to_investment · verfügbar: `neutrality_neutral_libertarians_are_in_power` · nur Spieler (KI nie)
  - Idee „The Market Union“: Produktivitätswachstum +5 %, Handelsmeinung +10 % (`add_ideas`)

### Partei: Friends of Baikal (17) (10)

Die Freunde des Baikalsees um den Limnologen Grigori Galasi – Umweltschutz gegen die Gigantomanie der Planer.

- **The Green Cabinet** `COLDWAR_SOV_fob_the_green_cabinet` · Kosten 3 · benötigt: power_greens oder na_neither_moscow_nor_washington · verfügbar: `neutrality_neutral_green_are_in_power`
  - Programm „Friends of Baikal“: Stabilität +2 %, Produktivitätswachstum -2 %, Erneuerbare Energie +10 % `COLDWAR_SOV_fob_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **Save Baikal** `COLDWAR_SOV_fob_save_baikal` · Kosten 5 · benötigt: fob_the_green_cabinet · verfügbar: `neutrality_neutral_green_are_in_power`
  - Stabilität +2 % `add_stability`
  - Gosplan – Planwirtschaft: Fabrikleistung (zivil) -1 % `COLDWAR_SOV_gosplan_modifier`
  - Friends of Baikal +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - _Anmerkung:_ Das Zellstoffkombinat Baikalsk wird geschlossen.
- **Stop the River Reversal** `COLDWAR_SOV_fob_stop_the_rivers` · Kosten 5 · benötigt: fob_the_green_cabinet · verfügbar: `neutrality_neutral_green_are_in_power`
  - Stabilität +2 % `add_stability`
  - Zusammenhalt der Union -2 `COLDWAR_SOV_change_union_cohesion`
- **Green Socialism or Conservation?** `COLDWAR_SOV_fob_the_path` · Kosten 3 · benötigt: fob_save_baikal, fob_stop_the_rivers · verfügbar: `neutrality_neutral_green_are_in_power`
  - Gegenseitig exklusiv
- **Green Socialism** `COLDWAR_SOV_fob_green_socialism` · Kosten 5 · benötigt: fob_the_path · schließt aus: fob_conservation_first · verfügbar: `neutrality_neutral_green_are_in_power`
  - Programm „Friends of Baikal“: Stabilität +2 %, Konsumgüter -2 % `COLDWAR_SOV_fob_programme`
- **Conservation First** `COLDWAR_SOV_fob_conservation_first` · Kosten 5 · benötigt: fob_the_path · schließt aus: fob_green_socialism · verfügbar: `neutrality_neutral_green_are_in_power`
  - Bergbaugesetz → Voller Umweltschutz `add_ideas` (full_environmental_protections)
  - Programm „Friends of Baikal“: Stabilität +3 % `COLDWAR_SOV_fob_programme`
- **Save the Aral** `COLDWAR_SOV_fob_save_the_aral` · Kosten 5 · benötigt: fob_green_socialism oder fob_conservation_first · verfügbar: `neutrality_neutral_green_are_in_power`
  - Zusammenhalt der Union +4 `COLDWAR_SOV_change_union_cohesion`
  - Gosplan – Planwirtschaft: Agrarsteuer -3 % `COLDWAR_SOV_gosplan_modifier`
- **Close Semipalatinsk** `COLDWAR_SOV_fob_close_semipalatinsk` · Kosten 5 · benötigt: fob_save_the_aral · verfügbar: `neutrality_neutral_green_are_in_power`
  - Zusammenhalt der Union +4 `COLDWAR_SOV_change_union_cohesion`
  - Cold-War-Spannung -1 `mdcw_cw_add_tension`
  - Armee & Generalstab -10 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **The Reactor Question** `COLDWAR_SOV_fob_the_rbmk_question` · Kosten 5 · benötigt: fob_save_the_aral · verfügbar: `neutrality_neutral_green_are_in_power`
  - Gosplan – Planwirtschaft: Energieerzeugung -5 % `COLDWAR_SOV_gosplan_modifier`
  - Entfernt das RBMK-Risikoflag `COLDWAR_SOV_rbmk`
- **The Green Union** `COLDWAR_SOV_fob_the_green_union` · Kosten 7 · benötigt: fob_close_semipalatinsk, fob_the_rbmk_question · verfügbar: `neutrality_neutral_green_are_in_power`
  - Idee „The Green Union“: Stabilität +4 %, Erneuerbare Energie +10 % (`add_ideas`)

### Partei: Socialist Market Commonwealth (18) (12)

Alexander Jakowlew und ein sowjetischer „Sozialismus mit menschlichem Antlitz“: Marktsozialismus nach jugoslawisch-ungarischem Muster.

- **The Market Socialists** `COLDWAR_SOV_smc_the_market_socialists` · Kosten 3 · benötigt: power_market_socialists oder na_neither_moscow_nor_washington · verfügbar: `neutrality_neutral_social_are_in_power`
  - Programm „Socialist Market Commonwealth“: Produktivitätswachstum +5 %, Konsumgüter -3 %, Demokratische Drift +0.01 `COLDWAR_SOV_smc_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **An Early Glasnost** `COLDWAR_SOV_smc_an_early_glasnost` · Kosten 5 · benötigt: smc_the_market_socialists · verfügbar: `neutrality_neutral_social_are_in_power`
  - Der Parteistaat: Forschung +3 %, Ideologische Driftabwehr -5 % `COLDWAR_SOV_party_state_modifier`
  - Stabilität -2 % `add_stability`
- **The Cooperative Law** `COLDWAR_SOV_smc_the_cooperative_law` · Kosten 5 · benötigt: smc_the_market_socialists · verfügbar: `neutrality_neutral_social_are_in_power`
  - ersetzt „The Second Economy“: Idee „Cooperative Sector“: Steuereinnahmen +3 %, Konsumgüter -3 %, Korruptionskosten +5 % (`swap_ideas`)
- **Belgrade or Budapest?** `COLDWAR_SOV_smc_the_model` · Kosten 3 · benötigt: smc_an_early_glasnost, smc_the_cooperative_law · verfügbar: `neutrality_neutral_social_are_in_power`
  - Gegenseitig exklusiv
- **Self-Management** `COLDWAR_SOV_smc_self_management` · Kosten 5 · benötigt: smc_the_model · schließt aus: smc_the_new_mechanism · verfügbar: `neutrality_neutral_social_are_in_power`
  - Programm „Socialist Market Commonwealth“: Stabilität +2 % `COLDWAR_SOV_smc_programme`
  - Gewerkschaften (VTsSPS) +10 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
  - Meinung SER +15 `add_opinion_modifier`
- **The New Economic Mechanism** `COLDWAR_SOV_smc_the_new_mechanism` · Kosten 5 · benötigt: smc_the_model · schließt aus: smc_self_management · verfügbar: `neutrality_neutral_social_are_in_power`
  - Programm „Socialist Market Commonwealth“: Produktivitätswachstum +4 % `COLDWAR_SOV_smc_programme`
  - Meinung HUN +15 `add_opinion_modifier`
- **Open to the World** `COLDWAR_SOV_smc_open_to_the_world` · Kosten 5 · benötigt: smc_self_management oder smc_the_new_mechanism · verfügbar: `neutrality_neutral_social_are_in_power`
  - Gosplan – Planwirtschaft: Handelsmeinung +10 % `COLDWAR_SOV_gosplan_modifier`
  - Cold-War-Spannung -1 `mdcw_cw_add_tension`
- **Federal Reform** `COLDWAR_SOV_smc_federal_reform` · Kosten 5 · benötigt: smc_open_to_the_world · verfügbar: `neutrality_neutral_social_are_in_power`
  - Zusammenhalt der Union +6 `COLDWAR_SOV_change_union_cohesion`
- **How Far the Market?** `COLDWAR_SOV_smc_the_question` · Kosten 3 · benötigt: smc_federal_reform · verfügbar: `neutrality_neutral_social_are_in_power`
  - Gegenseitig exklusiv
- **A Socialist Market** `COLDWAR_SOV_smc_socialist_market` · Kosten 5 · benötigt: smc_the_question · schließt aus: smc_the_mixed_economy · verfügbar: `neutrality_neutral_social_are_in_power`
  - Stabilität +3 % `add_stability`
- **The Mixed Economy** `COLDWAR_SOV_smc_the_mixed_economy` · Kosten 5 · benötigt: smc_the_question · schließt aus: smc_socialist_market · verfügbar: `neutrality_neutral_social_are_in_power`
  - Handelsgesetz → Gemischte Wirtschaft `add_ideas` (mixed_economy)
  - Stabilität -2 % `add_stability`
- **The Commonwealth** `COLDWAR_SOV_smc_the_commonwealth` · Kosten 7 · benötigt: smc_socialist_market oder smc_the_mixed_economy · verfügbar: `neutrality_neutral_social_are_in_power`
  - Idee „The Market Commonwealth“: Produktivitätswachstum +5 %, Stabilität +2 % (`add_ideas`)

### Partei: Union of Sovereign Republics (19) (9)

Pjotr Schelest (bis 1972 Erster Sekretär der Ukraine): Nationalkommunismus der Republiken – eine lose Union souveräner Sowjetstaaten.

- **A Union of Sovereign Republics** `COLDWAR_SOV_usr_a_union_of_sovereign_republics` · Kosten 3 · benötigt: power_sovereign_republics oder na_neither_moscow_nor_washington · verfügbar: `neutrality_neutral_communism_are_in_power`
  - Programm „National Communism“: Stabilität +2 %, PP-Gewinn -5 %, Nationalistische Drift +0.01 `COLDWAR_SOV_usr_programme`
  - Zusammenhalt der Union +10 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **The New Union Treaty** `COLDWAR_SOV_usr_the_new_union_treaty` · Kosten 5 · benötigt: usr_a_union_of_sovereign_republics · verfügbar: `neutrality_neutral_communism_are_in_power`
  - Zusammenhalt der Union +10 `COLDWAR_SOV_change_union_cohesion`
  - Jede Unionsrepublik erhält das Angebot, den neuen Vertrag zu unterzeichnen (mehr Autonomie, kein Austritt erzwungen)
- **Our Soviet Ukraine** `COLDWAR_SOV_usr_our_soviet_ukraine` · Kosten 5 · benötigt: usr_a_union_of_sovereign_republics · verfügbar: `neutrality_neutral_communism_are_in_power`
  - Meinung UKR +20 `add_opinion_modifier`
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
- **Many Paths or a Kiev Axis?** `COLDWAR_SOV_usr_the_model` · Kosten 3 · benötigt: usr_the_new_union_treaty, usr_our_soviet_ukraine · verfügbar: `neutrality_neutral_communism_are_in_power`
  - Gegenseitig exklusiv
- **Many Paths to Socialism** `COLDWAR_SOV_usr_many_paths` · Kosten 5 · benötigt: usr_the_model · schließt aus: usr_the_kiev_axis · verfügbar: `neutrality_neutral_communism_are_in_power`
  - Zusammenhalt der Union +8 `COLDWAR_SOV_change_union_cohesion`
  - Programm „National Communism“: PP-Gewinn -3 % `COLDWAR_SOV_usr_programme`
- **The Kiev Axis** `COLDWAR_SOV_usr_the_kiev_axis` · Kosten 5 · benötigt: usr_the_model · schließt aus: usr_many_paths · verfügbar: `neutrality_neutral_communism_are_in_power`
  - Zusammenhalt der Union +4 `COLDWAR_SOV_change_union_cohesion`
  - Programm „National Communism“: PP-Gewinn +3 % `COLDWAR_SOV_usr_programme`
- **Economic Sovereignty** `COLDWAR_SOV_usr_economic_sovereignty` · Kosten 5 · benötigt: usr_many_paths oder usr_the_kiev_axis · verfügbar: `neutrality_neutral_communism_are_in_power`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
- **Republican Formations** `COLDWAR_SOV_usr_republic_formations` · Kosten 5 · benötigt: usr_economic_sovereignty · verfügbar: `neutrality_neutral_communism_are_in_power`
  - Mannstärke +20.000 `add_manpower`
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
- **The Commonwealth of Soviet States** `COLDWAR_SOV_usr_the_commonwealth_of_soviet_states` · Kosten 7 · benötigt: usr_republic_formations · verfügbar: `neutrality_neutral_communism_are_in_power`
  - Idee „Commonwealth of Soviet States“: Stabilität +4 %, Nationalistische Drift -0.02 (`add_ideas`)
  - Zusammenhalt der Union +10 `COLDWAR_SOV_change_union_cohesion`

### Partei: The Russian Party (20) (13)

Die „Russische Partei“ um Politbüromitglied Dmitri Poljanski und die Zeitschrift Molodaja Gwardija – Russland vor dem Imperium.

- **The Russian Party** `COLDWAR_SOV_rp_the_russian_party` · Kosten 3 · benötigt: power_russian_party oder nt_russia_first · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Programm „The Russian Party“: Nationalistische Drift +0.02, Kriegsunterstützung +3 %, Stabilität +2 % `COLDWAR_SOV_rp_programme`
  - Zusammenhalt der Union -5 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **The Molodaya Gvardiya Line** `COLDWAR_SOV_rp_the_molodaya_gvardiya_line` · Kosten 5 · benötigt: rp_the_russian_party · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - The Russian Party +5 % Popularität (Outlook +5 %) `change_relative_party_popularity`
  - Der Parteistaat: Ideologische Driftabwehr +5 % `COLDWAR_SOV_party_state_modifier`
- **The Russian Village First** `COLDWAR_SOV_rp_the_russian_village_first` · Kosten 5 · benötigt: rp_the_russian_party · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Gosplan – Planwirtschaft: Agrarproduktivität +5 % `COLDWAR_SOV_gosplan_modifier`
  - Kolchosbauern +10 `COLDWAR_SOV_change_farmers_opinion_exact` → `change_farmers_opinion`
- **Red or White?** `COLDWAR_SOV_rp_the_model` · Kosten 3 · benötigt: rp_the_molodaya_gvardiya_line, rp_the_russian_village_first · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Gegenseitig exklusiv
- **National Bolshevism** `COLDWAR_SOV_rp_national_bolshevism` · Kosten 5 · benötigt: rp_the_model · schließt aus: rp_orthodox_nationalism · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Programm „The Russian Party“: Kommunistische Drift +0.01, PP-Gewinn +5 % `COLDWAR_SOV_rp_programme`
  - Communist Party of the Soviet Union +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
- **Orthodox Nationalism** `COLDWAR_SOV_rp_orthodox_nationalism` · Kosten 5 · benötigt: rp_the_model · schließt aus: rp_national_bolshevism · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 60)
  - Programm „The Russian Party“: Stabilität +3 % `COLDWAR_SOV_rp_programme`
- **A Party for the RSFSR** `COLDWAR_SOV_rp_a_communist_party_for_the_rsfsr` · Kosten 5 · benötigt: rp_national_bolshevism oder rp_orthodox_nationalism · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Zusammenhalt der Union -5 `COLDWAR_SOV_change_union_cohesion`
  - Der Parteistaat: PP-Gewinn +5 % `COLDWAR_SOV_party_state_modifier`
- **The Slavic Core** `COLDWAR_SOV_rp_the_slavic_core` · Kosten 5 · benötigt: rp_a_communist_party_for_the_rsfsr · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Angebot an UKR, BLR (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Engere Union der Ostslawen. Bei Annahme: Meinung +20, Autonomie bleibt, Zusammenhalt +5 `COLDWAR_SOV_offer_slavic_core`
- **The Great Power Army** `COLDWAR_SOV_rp_the_great_power_army` · Kosten 5 · benötigt: rp_a_communist_party_for_the_rsfsr · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Streitkräfte der UdSSR: Moral (Heer) +5 % `COLDWAR_SOV_armed_forces_modifier`
  - Armee & Generalstab +10 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **Empire or Nation?** `COLDWAR_SOV_rp_the_question` · Kosten 3 · benötigt: rp_the_slavic_core, rp_the_great_power_army · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Gegenseitig exklusiv
- **The Empire** `COLDWAR_SOV_rp_the_empire` · Kosten 5 · benötigt: rp_the_question · schließt aus: rp_the_nation · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Zusammenhalt der Union +5 `COLDWAR_SOV_change_union_cohesion`
  - Kriegsunterstützung +5 % `add_war_support`
  - Der Parteistaat: Polizeikosten +10 % `COLDWAR_SOV_party_state_modifier`
- **The Nation** `COLDWAR_SOV_rp_the_nation` · Kosten 5 · benötigt: rp_the_question · schließt aus: rp_the_empire · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Zusammenhalt der Union -10 `COLDWAR_SOV_change_union_cohesion`
  - Stabilität +5 % `add_stability`
- **Great Russia** `COLDWAR_SOV_rp_great_russia` · Kosten 7 · benötigt: rp_the_empire oder rp_the_nation · verfügbar: `nationalist_right_wing_populists_are_in_power`
  - Idee „Great Russia“: Kriegsunterstützung +5 %, Stabilität +3 %, Nationalistische Drift +0.01 (`add_ideas`)

### Partei: Committee of National Rebirth (21) (7)

Ultranationalistischer Untergrund (kollektive Führung) – Diktatur der „nationalen Wiedergeburt“, Säuberungen, Isolation.

- **The National Rebirth** `COLDWAR_SOV_cnr_the_national_rebirth` · Kosten 3 · benötigt: power_national_rebirth oder nt_russia_first · verfügbar: `nationalist_fascist_are_in_power` · nur Spieler (KI nie)
  - Programm „National Rebirth“: Kriegsunterstützung +10 %, Stabilität -5 %, Ideologische Driftabwehr +15 %, Handelsmeinung -20 % `COLDWAR_SOV_cnr_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **The Emergency Committee** `COLDWAR_SOV_cnr_the_emergency_committee` · Kosten 5 · benötigt: cnr_the_national_rebirth · verfügbar: `nationalist_fascist_are_in_power` · nur Spieler (KI nie)
  - PP +75 `add_political_power`
  - Nomenklatura -25 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **Militarise the Nation** `COLDWAR_SOV_cnr_militarise_the_nation` · Kosten 5 · benötigt: cnr_the_national_rebirth · verfügbar: `nationalist_fascist_are_in_power` · nur Spieler (KI nie)
  - Verteidigungshaushalt +1 Stufe `increase_military_spending`
  - Mannstärke +50.000 `add_manpower`
- **Isolation or Expansion?** `COLDWAR_SOV_cnr_the_path` · Kosten 3 · benötigt: cnr_the_emergency_committee, cnr_militarise_the_nation · verfügbar: `nationalist_fascist_are_in_power` · nur Spieler (KI nie)
  - Gegenseitig exklusiv
- **Fortress Russia** `COLDWAR_SOV_cnr_fortress_russia` · Kosten 5 · benötigt: cnr_the_path · schließt aus: cnr_the_revanche · verfügbar: `nationalist_fascist_are_in_power` · nur Spieler (KI nie)
  - Handelsgesetz → Geschlossene Wirtschaft `add_ideas` (md_closed_economy)
  - Streitkräfte der UdSSR: Verteidigung auf Kerngebiet +5 % `COLDWAR_SOV_armed_forces_modifier`
- **The Revanche** `COLDWAR_SOV_cnr_the_revanche` · Kosten 5 · benötigt: cnr_the_path · schließt aus: cnr_fortress_russia · verfügbar: `nationalist_fascist_are_in_power` · nur Spieler (KI nie)
  - Cold-War-Spannung +5 `mdcw_cw_add_tension`
  - Streitkräfte der UdSSR: Angriff (Heer) +3 % `COLDWAR_SOV_armed_forces_modifier`
- **The Rebirth State** `COLDWAR_SOV_cnr_the_rebirth_state` · Kosten 7 · benötigt: cnr_fortress_russia oder cnr_the_revanche · verfügbar: `nationalist_fascist_are_in_power` · nur Spieler (KI nie)
  - Idee „The Rebirth State“: Kriegsunterstützung +5 %, Stabilität +2 %, Forschung -3 % (`add_ideas`)

### Partei: Council of Marshals (22) (13)

Der Rat der Marschälle um Verteidigungsminister Andrei Gretschko – Militärdiktatur, Mobilisierung, Generalstab statt Politbüro.

- **The Marshals Govern** `COLDWAR_SOV_com_the_marshals_govern` · Kosten 3 · benötigt: power_marshals oder nt_russia_first · verfügbar: `nationalist_military_junta_are_in_power`
  - Programm „The Council of Marshals“: Organisation (Heer) +5 %, Kriegsunterstützung +5 %, Stabilität -3 %, PP-Gewinn -5 % `COLDWAR_SOV_com_programme`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **The General Staff Governs** `COLDWAR_SOV_com_the_general_staff_governs` · Kosten 5 · benötigt: com_the_marshals_govern · verfügbar: `nationalist_military_junta_are_in_power`
  - Armee & Generalstab +15 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Kommandomacht +50 `add_command_power`
- **Order and Discipline** `COLDWAR_SOV_com_order_and_discipline` · Kosten 5 · benötigt: com_the_marshals_govern · verfügbar: `nationalist_military_junta_are_in_power`
  - Stabilität +4 % `add_stability`
  - Korruption −1 Stufe `decrease_corruption`
- **Ogarkov or the Old Marshals?** `COLDWAR_SOV_com_the_model` · Kosten 3 · benötigt: com_the_general_staff_governs, com_order_and_discipline · verfügbar: `nationalist_military_junta_are_in_power`
  - Gegenseitig exklusiv
- **The Modernisers** `COLDWAR_SOV_com_the_modernisers` · Kosten 5 · benötigt: com_the_model · schließt aus: com_the_old_marshals · verfügbar: `nationalist_military_junta_are_in_power`
  - Programm „The Council of Marshals“: Forschung +3 %, Effizienzzuwachs +3 % `COLDWAR_SOV_com_programme`
  - Forschungsbonus CAT_command_and_control_equipment +75 % ×1 `add_tech_bonus`
- **The Old Marshals** `COLDWAR_SOV_com_the_old_marshals` · Kosten 5 · benötigt: com_the_model · schließt aus: com_the_modernisers · verfügbar: `nationalist_military_junta_are_in_power`
  - Programm „The Council of Marshals“: Rekrutierbare Bevölkerung +5 %, Verteidigung (Heer) +3 % `COLDWAR_SOV_com_programme`
  - Mannstärke +50.000 `add_manpower`
- **The Military Economy** `COLDWAR_SOV_com_the_military_economy` · Kosten 5 · benötigt: com_the_modernisers oder com_the_old_marshals · verfügbar: `nationalist_military_junta_are_in_power`
  - Gebäude: Rüstungsfabriken `two_random_arms_factory`, Kosten 1.2 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Konsumgüter +3 % `COLDWAR_SOV_gosplan_modifier`
- **The Defence Council** `COLDWAR_SOV_com_the_defence_council` · Kosten 5 · benötigt: com_the_military_economy · verfügbar: `nationalist_military_junta_are_in_power`
  - PP +75 `add_political_power`
  - Streitkräfte der UdSSR: Planungsgeschwindigkeit +0.05 `COLDWAR_SOV_armed_forces_modifier`
- **Strategic Deterrence** `COLDWAR_SOV_com_strategic_deterrence` · Kosten 5 · benötigt: com_the_military_economy · verfügbar: `nationalist_military_junta_are_in_power`
  - Forschungsbonus CAT_intercontinental_ballistic_missiles +50 % ×1 `add_tech_bonus`
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
- **How Long?** `COLDWAR_SOV_com_the_question` · Kosten 3 · benötigt: com_the_defence_council, com_strategic_deterrence · verfügbar: `nationalist_military_junta_are_in_power`
  - Gegenseitig exklusiv
- **Return to the Barracks** `COLDWAR_SOV_com_return_to_the_barracks` · Kosten 5 · benötigt: com_the_question · schließt aus: com_the_permanent_stavka · verfügbar: `nationalist_military_junta_are_in_power`
  - Regierungspartei → Communist Party of the Soviet Union (Communist State) `change_ruling_party_effect`, Staatschef Leonid Brezhnev `create_country_leader`
  - Stabilität +5 % `add_stability`
  - Armee & Generalstab -10 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - _Anmerkung:_ Übergabe zurück an die KPdSU.
- **The Permanent Stavka** `COLDWAR_SOV_com_the_permanent_stavka` · Kosten 5 · benötigt: com_the_question · schließt aus: com_return_to_the_barracks · verfügbar: `nationalist_military_junta_are_in_power`
  - Programm „The Council of Marshals“: PP-Gewinn +5 %, Stabilität +3 % `COLDWAR_SOV_com_programme`
- **The Garrison State** `COLDWAR_SOV_com_the_garrison_state` · Kosten 7 · benötigt: com_the_permanent_stavka · verfügbar: `nationalist_military_junta_are_in_power`
  - Idee „The Garrison State“: Angriff (Heer) +2 %, Verteidigung (Heer) +3 %, Konsumgüter +2 % (`add_ideas`)

### Partei: House of Romanov (23) (10)

Großfürst Wladimir Kirillowitsch, Chef des Hauses Romanow – Restauration einer konstitutionellen oder autokratischen Monarchie.

- **The Return of the Romanovs** `COLDWAR_SOV_rom_the_return_of_the_tsar` · Kosten 3 · benötigt: power_romanovs oder nt_russia_first · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Programm „The Restored Crown“: Stabilität +3 %, Nationalistische Drift +0.02, PP-Gewinn +3 % `COLDWAR_SOV_rom_programme`
  - Neuer Staatschef: Vladimir Kirillovich `create_country_leader`, Trait „Head of the House of Romanov“ `COLDWAR_SOV_head_of_the_house`
  - _Anmerkung:_ Partei-Einstieg: zwei Linien führen hinein (Machtübergabe ODER Outlook regiert). Das Programm entfällt, wenn die Partei die Macht verliert.
- **The Coronation** `COLDWAR_SOV_rom_the_coronation` · Kosten 5 · benötigt: rom_the_return_of_the_tsar · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Stabilität +5 % `add_stability`
  - PP +50 `add_political_power`
- **The Church and the Crown** `COLDWAR_SOV_rom_the_church_and_the_crown` · Kosten 5 · benötigt: rom_the_return_of_the_tsar · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 75)
  - Stabilität +3 % `add_stability`
- **Duma or Autocrat?** `COLDWAR_SOV_rom_the_form` · Kosten 3 · benötigt: rom_the_coronation, rom_the_church_and_the_crown · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Gegenseitig exklusiv
- **Constitutional Monarchy** `COLDWAR_SOV_rom_constitutional_monarchy` · Kosten 5 · benötigt: rom_the_form · schließt aus: rom_the_autocrat · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Wahlen erlaubt `set_politics`
  - Programm „The Restored Crown“: Demokratische Drift +0.01, Stabilität +2 % `COLDWAR_SOV_rom_programme`
- **The Autocrat** `COLDWAR_SOV_rom_the_autocrat` · Kosten 5 · benötigt: rom_the_form · schließt aus: rom_constitutional_monarchy · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Programm „The Restored Crown“: PP-Gewinn +5 %, Ideologische Driftabwehr +10 % `COLDWAR_SOV_rom_programme`
- **The Émigrés Return** `COLDWAR_SOV_rom_the_emigres_return` · Kosten 5 · benötigt: rom_constitutional_monarchy oder rom_the_autocrat · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - Gosplan – Planwirtschaft: Handelsmeinung +10 % `COLDWAR_SOV_gosplan_modifier`
- **The Crown and the Republics** `COLDWAR_SOV_rom_the_crown_and_the_republics` · Kosten 5 · benötigt: rom_the_emigres_return · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Zusammenhalt der Union -5 `COLDWAR_SOV_change_union_cohesion`
  - Stabilität +2 % `add_stability`
- **The Royal Houses of Europe** `COLDWAR_SOV_rom_the_royal_houses` · Kosten 5 · benötigt: rom_the_emigres_return · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Angebot an ENG, SPR (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Anerkennung der restaurierten Krone. Bei Annahme: Meinung +25 `COLDWAR_SOV_offer_royal_houses`
- **The Restored Empire** `COLDWAR_SOV_rom_the_restored_empire` · Kosten 7 · benötigt: rom_the_crown_and_the_republics, rom_the_royal_houses · verfügbar: `nationalist_monarchists_are_in_power` · nur Spieler (KI nie)
  - Idee „The Restored Empire“: Stabilität +5 %, Nationalistische Drift +0.01, Kriegsunterstützung +3 % (`add_ideas`)

### Gosplan & Fünfjahrpläne (39)

Kossygin-Reform (vertiefen, kybernetisch planen oder zurücknehmen), IX. bis XI. Fünfjahrplan mit Prioritätswahl (Gruppe A/B/Rüstung), Togliatti und KamAZ, Preisfrage, Computer (IBM-Klon oder BESM), Schtschokino-Methode, wissenschaftlich-technische Revolution.

- **Gosplan Directives** `COLDWAR_SOV_gosplan_directives` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Gosplan – Planwirtschaft: Baugeschwindigkeit +2 % `COLDWAR_SOV_gosplan_modifier`
  - Schaltet Entscheidung frei: Kategorie „Fünfjahrpläne“: ab dem IX. Plan wählt der Spieler pro Plan eine Priorität (5 Jahre, Wirkung und Kosten) `unlock_decision_tooltip`
- **Complete the Eighth Five-Year Plan** `COLDWAR_SOV_complete_the_eighth_plan` · Kosten 5 · hist. · benötigt: gosplan_directives
  - Gebäude: Zivilfabrik `one_random_industrial_complex`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Effizienzzuwachs +3 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ 1966–1970, der wachstumsstärkste Plan der Nachkriegszeit.
- **The Kosygin Reform Question** `COLDWAR_SOV_the_kosygin_reform_question` · Kosten 3 · hist. · benötigt: gosplan_directives
  - PP +25 `add_political_power`
  - Drei Wege, gegenseitig exklusiv
  - _Anmerkung:_ Die Reform von 1965 (Gewinn, Prämien, Betriebsautonomie) wird nach Prag schleichend zurückgenommen.
- **Deepen the Kosygin Reform** `COLDWAR_SOV_deepen_the_kosygin_reform` · Kosten 5 · benötigt: the_kosygin_reform_question · schließt aus: cybernetic_planning, the_ministries_restored
  - Gosplan – Planwirtschaft: Produktivitätswachstum +5 %, Steuer Zivilindustrie +5 % `COLDWAR_SOV_gosplan_modifier`
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
  - Branchenministerien -10 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Flag `COLDWAR_SOV_market_reform`
  - Politbüro-Beschluss (reformerisch): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
- **Khozraschyot: Enterprise Self-Financing** `COLDWAR_SOV_enterprise_self_financing` · Kosten 5 · benötigt: deepen_the_kosygin_reform
  - Gosplan – Planwirtschaft: Körperschaftsteuer-Einnahmen +5 %, Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
  - Gewerkschaften (VTsSPS) -5 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
  - Stabilität -2 % `add_stability`
- **Lessons from Budapest** `COLDWAR_SOV_lessons_from_budapest` · Kosten 5 · benötigt: deepen_the_kosygin_reform
  - Meinung HUN +15 `add_opinion_modifier`
  - Gosplan – Planwirtschaft: Konsumgüter -2 %, Handelsmeinung +5 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Ungarns Neuer Ökonomischer Mechanismus (seit 1968) als Vorbild.
- **Legalise the Cooperatives** `COLDWAR_SOV_legalise_the_cooperatives` · Kosten 7 · benötigt: enterprise_self_financing, lessons_from_budapest
  - ersetzt „The Second Economy“: Idee „Cooperative Sector“: Steuereinnahmen +3 %, Konsumgüter -3 %, Korruptionskosten +5 % (`swap_ideas`)
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Socialist Market Commonwealth +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - _Anmerkung:_ Aus der Schattenwirtschaft wird ein legaler Sektor – die Nomenklatura verliert ihre Pfründe.
- **OGAS: Cybernetic Planning** `COLDWAR_SOV_cybernetic_planning` · Kosten 5 · benötigt: the_kosygin_reform_question · schließt aus: deepen_the_kosygin_reform, the_ministries_restored
  - Gosplan – Planwirtschaft: Effizienzzuwachs +5 % `COLDWAR_SOV_gosplan_modifier`
  - Forschungsbonus CAT_computing +50 % ×1 `add_tech_bonus`
  - Kosten 0.6 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Branchenministerien -5 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
  - Flag `COLDWAR_SOV_ogas`
  - Politbüro-Beschluss (neutral): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
  - _Anmerkung:_ Viktor Gluschkows Gesamtstaatliches Automatisiertes System – 1970 vom Politbüro vertagt, hier umgesetzt.
- **The OGAS Network** `COLDWAR_SOV_the_ogas_network` · Kosten 7 · benötigt: cybernetic_planning
  - Gebäude: Büro `one_office_construction`, Kosten 0.7 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Effizienzzuwachs +5 %, Max. Fabrikeffizienz +3 % `COLDWAR_SOV_gosplan_modifier`
  - Kosten 0.8 % BIP `COLDWAR_SOV_pay_gdp_share`
- **Kantorovich's Optimal Prices** `COLDWAR_SOV_kantorovich_optimal_prices` · Kosten 5 · benötigt: cybernetic_planning
  - Gosplan – Planwirtschaft: Produktivitätswachstum +4 %, Konsumgüter -2 % `COLDWAR_SOV_gosplan_modifier`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ Leonid Kantorowitsch, Nobelpreis 1975 für lineare Optimierung.
- **Computing Centres of the Republics** `COLDWAR_SOV_computing_centres_of_the_republics` · Kosten 7 · benötigt: the_ogas_network, kantorovich_optimal_prices
  - Forschungsbonus CAT_information_technology +50 % ×1 `add_tech_bonus`
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
- **The Ministries Restored** `COLDWAR_SOV_the_ministries_restored` · Kosten 5 · hist. · benötigt: the_kosygin_reform_question · schließt aus: deepen_the_kosygin_reform, cybernetic_planning
  - Gosplan – Planwirtschaft: Baugeschwindigkeit +3 %, Produktivitätswachstum -2 % `COLDWAR_SOV_gosplan_modifier`
  - Branchenministerien +10 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
  - Nomenklatura +5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
  - Politbüro-Beschluss (orthodox): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
- **New Union Ministries** `COLDWAR_SOV_new_union_ministries` · Kosten 5 · hist. · benötigt: the_ministries_restored
  - Gosplan – Planwirtschaft: Baugeschwindigkeit +3 % `COLDWAR_SOV_gosplan_modifier`
  - Der Parteistaat: Bürokratiekosten +5 % `COLDWAR_SOV_party_state_modifier`
  - Branchenministerien +5 `COLDWAR_SOV_change_industrial_conglomerates_opinion_exact` → `change_industrial_conglomerates_opinion`
- **The Tolkachi** `COLDWAR_SOV_the_tolkachi` · Kosten 5 · hist. · benötigt: the_ministries_restored
  - Gosplan – Planwirtschaft: Effizienzzuwachs +3 % `COLDWAR_SOV_gosplan_modifier`
  - Der Parteistaat: Korruptionskosten +5 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Die „Schieber“ der Betriebe, die Material am Plan vorbei beschaffen – sie halten die Fabriken am Laufen.
- **Plan Fulfilment Campaigns** `COLDWAR_SOV_plan_fulfilment_campaigns` · Kosten 5 · hist. · benötigt: new_union_ministries, the_tolkachi
  - Gosplan – Planwirtschaft: Fabrikleistung (zivil) +3 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität +2 % `add_stability`
  - Communist Party of the Soviet Union +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
- **The Ninth Five-Year Plan** `COLDWAR_SOV_the_ninth_five_year_plan` · Kosten 5 · hist. · benötigt: legalise_the_cooperatives oder computing_centres_of_the_republics oder plan_fulfilment_campaigns oder deepen_the_kosygin_reform oder cybernetic_planning oder the_ministries_restored · verfügbar: `COLDWAR_SOV_the_24th_party_congress` erledigt
  - PP +50 `add_political_power`
  - Prioritätswahl für 1971–1975 (gegenseitig exklusiv)
  - Flag `COLDWAR_SOV_ninth_plan`
- **Group B: Goods for the People** `COLDWAR_SOV_group_b_goods_for_the_people` · Kosten 5 · hist. · benötigt: the_ninth_five_year_plan · schließt aus: group_a_means_of_production, the_defence_sector_first
  - Gosplan – Planwirtschaft: Konsumgüter -3 %, Steuer Zivilindustrie +3 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität +3 % `add_stability`
  - Rüstungskomplex (VPK) -5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - _Anmerkung:_ Der IX. Plan sah erstmals ein schnelleres Wachstum der Konsumgüter (Gruppe B) als der Produktionsmittel vor – auf dem Papier.
- **The Brezhnevka** `COLDWAR_SOV_the_brezhnevka` · Kosten 5 · hist. · benötigt: group_b_goods_for_the_people
  - Stabilität +3 % `add_stability`
  - Gosplan – Planwirtschaft: Sozialkosten +3 % `COLDWAR_SOV_gosplan_modifier`
  - Gebäude: Infrastruktur `one_random_infrastructure`, Kosten 0.6 % BIP statt MD-Pauschale (`skip_payment`)
  - Union der Republiken: Stabilität +1 % `COLDWAR_SOV_union_modifier`
  - _Anmerkung:_ Neun- bis sechzehngeschossige Plattenbauten lösen die Chruschtschowka ab.
- **Refrigerators and Televisions** `COLDWAR_SOV_refrigerators_and_televisions` · Kosten 5 · benötigt: group_b_goods_for_the_people
  - Gebäude: Zivilfabrik `one_random_industrial_complex`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Konsumgüter -2 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität +2 % `add_stability`
- **Group A: Means of Production** `COLDWAR_SOV_group_a_means_of_production` · Kosten 5 · benötigt: the_ninth_five_year_plan · schließt aus: group_b_goods_for_the_people, the_defence_sector_first
  - Gosplan – Planwirtschaft: Fabrikleistung (zivil) +3 %, Baugeschwindigkeit +4 %, Konsumgüter +2 % `COLDWAR_SOV_gosplan_modifier`
  - Gebäude: Zivilfabriken `two_random_industrial_complex`, Kosten 1.5 % BIP statt MD-Pauschale (`skip_payment`)
- **Magnitka and Cherepovets** `COLDWAR_SOV_steel_cities` · Kosten 5 · benötigt: group_a_means_of_production
  - Ressource: +8 Stahl in einem eigenen Staat mit Stahl `random_owned_controlled_state` `add_resource`
  - Gebäude: Industrieinfrastruktur `one_random_industrial_infrastructure`, Kosten 0.6 % BIP statt MD-Pauschale (`skip_payment`)
- **Machine-Building First** `COLDWAR_SOV_machine_building_first` · Kosten 5 · benötigt: group_a_means_of_production
  - Gosplan – Planwirtschaft: Max. Fabrikeffizienz +4 % `COLDWAR_SOV_gosplan_modifier`
  - Forschungsbonus CAT_production_lines +50 % ×1 `add_tech_bonus`
- **The Defence Sector First** `COLDWAR_SOV_the_defence_sector_first` · Kosten 5 · benötigt: the_ninth_five_year_plan · schließt aus: group_b_goods_for_the_people, group_a_means_of_production
  - Gebäude: Rüstungsfabriken `two_random_arms_factory`, Kosten 1.2 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Steuer Rüstungsindustrie +5 %, Konsumgüter +3 % `COLDWAR_SOV_gosplan_modifier`
  - Rüstungskomplex (VPK) +10 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
- **The Nine Defence Ministries** `COLDWAR_SOV_the_nine_ministries` · Kosten 5 · benötigt: the_defence_sector_first
  - Streitkräfte der UdSSR: Ausrüstungskosten -3 % `COLDWAR_SOV_armed_forces_modifier`
  - Gosplan – Planwirtschaft: Bau Rüstungsfabriken +10 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Die „Neun“ des Rüstungskomplexes (Mittelmaschinenbau, Luftfahrt, Schiffbau …) mit eigenen Städten und Schulen.
- **Dual-Use Factories** `COLDWAR_SOV_dual_use_factories` · Kosten 5 · benötigt: the_defence_sector_first
  - Gosplan – Planwirtschaft: Konsumgüter -2 %, Steuer Rüstungsindustrie +2 % `COLDWAR_SOV_gosplan_modifier`
  - Gebäude: Zivilfabrik `one_random_industrial_complex`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - _Anmerkung:_ Panzerfabriken bauen nebenher Kühlschränke – schlecht, aber besser als keine.
- **AvtoVAZ: The Zhiguli** `COLDWAR_SOV_avtovaz_the_zhiguli` · Kosten 5 · hist. · benötigt: complete_the_eighth_plan
  - Gebäude: Zivilfabrik `one_random_industrial_complex`, Kosten 0.9 % BIP statt MD-Pauschale (`skip_payment`)
  - Meinung ITA +10 `add_opinion_modifier`
  - Gosplan – Planwirtschaft: Konsumgüter -2 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Togliatti, erster Lada am 19.04.1970 – Fiat-Lizenz von 1966.
- **KamAZ: The Kama Truck Works** `COLDWAR_SOV_kamaz_the_kama_truck_works` · Kosten 7 · hist. · benötigt: avtovaz_the_zhiguli
  - Gebäude: Zivilfabrik `one_random_industrial_complex`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
  - Forschungsbonus CAT_utility_vehicles +50 % ×1 `add_tech_bonus`
  - Streitkräfte der UdSSR: Versorgungsverbrauch -2 % `COLDWAR_SOV_armed_forces_modifier`
  - _Anmerkung:_ Naberezhnye Chelny, gebaut 1969–1976 mit westlichen Werkzeugmaschinen.
- **The Price Question** `COLDWAR_SOV_the_price_question` · Kosten 3 · hist. · benötigt: the_ninth_five_year_plan
  - Novotscherkassk 1962 sitzt der Führung im Nacken – gegenseitig exklusiv
- **Raise Retail Prices** `COLDWAR_SOV_raise_retail_prices` · Kosten 5 · benötigt: the_price_question · schließt aus: hold_the_prices
  - Gosplan – Planwirtschaft: Steuereinnahmen +5 %, Konsumgüter -2 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität -6 % `add_stability`
  - Gewerkschaften (VTsSPS) -10 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
  - Entfernt „The Second Economy“ `remove_ideas`
  - Politbüro-Beschluss (reformerisch): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
  - _Anmerkung:_ Ehrliche Preise entziehen dem Schwarzmarkt die Grundlage – um den Preis von Unruhen.
- **Hold the Prices** `COLDWAR_SOV_hold_the_prices` · Kosten 3 · hist. · benötigt: the_price_question · schließt aus: raise_retail_prices
  - Stabilität +3 % `add_stability`
  - Gosplan – Planwirtschaft: Steuereinnahmen -3 %, Konsumgüter +2 % `COLDWAR_SOV_gosplan_modifier`
  - Politbüro-Beschluss (orthodox): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
  - _Anmerkung:_ Brot kostet 1980 so viel wie 1955 – subventioniert, oft nicht erhältlich.
- **The Unified System Question** `COLDWAR_SOV_the_unified_system_question` · Kosten 3 · hist. · benötigt: the_ninth_five_year_plan
  - Welche Computer baut der Ostblock? Gegenseitig exklusiv
- **Ryad: Copy the IBM/360** `COLDWAR_SOV_ryad_copy_the_ibm_360` · Kosten 5 · hist. · benötigt: the_unified_system_question · schließt aus: continue_the_besm_line
  - Forschungsbonus CAT_computing +50 % ×2 `add_tech_bonus`
  - Der Parteistaat: Forschung -1 % `COLDWAR_SOV_party_state_modifier`
  - Sozialistische Gemeinschaft: Forschungsteilung +5 % `COLDWAR_SOV_commonwealth_modifier`
  - _Anmerkung:_ Die Entscheidung von 1969/70: schnelle Kompatibilität, aber eigene Entwicklung verkümmert.
- **Continue the BESM Line** `COLDWAR_SOV_continue_the_besm_line` · Kosten 7 · benötigt: the_unified_system_question · schließt aus: ryad_copy_the_ibm_360
  - Forschungsbonus CAT_computing +25 % ×1 `add_tech_bonus`
  - Der Parteistaat: Forschung +3 % `COLDWAR_SOV_party_state_modifier`
  - Kosten 0.6 % BIP `COLDWAR_SOV_pay_gdp_share`
  - _Anmerkung:_ Lebedews eigene Architektur – langsamer, aber unabhängig.
- **Microelectronics of Zelenograd** `COLDWAR_SOV_microelectronics_of_zelenograd` · Kosten 7 · benötigt: ryad_copy_the_ibm_360 oder continue_the_besm_line
  - Gebäude: Mikrochipwerk `one_random_microchip_plant`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
  - Forschungsbonus CAT_microchips +50 % ×1 `add_tech_bonus`
- **The Tenth Five-Year Plan** `COLDWAR_SOV_the_tenth_five_year_plan` · Kosten 5 · hist. · benötigt: the_brezhnevka oder refrigerators_and_televisions oder steel_cities oder machine_building_first oder the_nine_ministries oder dual_use_factories · verfügbar: Datum ≥ 01.01.1976
  - PP +50 `add_political_power`
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 % `COLDWAR_SOV_gosplan_modifier`
  - „Plan der Effizienz und Qualität“; neue Prioritätswahl in der Kategorie Fünfjahrpläne
- **The Shchekino Method** `COLDWAR_SOV_the_shchekino_method` · Kosten 5 · benötigt: the_tenth_five_year_plan
  - Gosplan – Planwirtschaft: Produktivitätswachstum +4 % `COLDWAR_SOV_gosplan_modifier`
  - Gewerkschaften (VTsSPS) -10 `COLDWAR_SOV_change_labour_unions_opinion_exact` → `change_labour_unions_opinion`
  - Stabilität -2 % `add_stability`
  - _Anmerkung:_ Chemiekombinat Schtschokino (1967): weniger Arbeiter, gleicher Lohnfonds, höhere Prämien.
- **The State Quality Mark** `COLDWAR_SOV_quality_mark_of_the_ussr` · Kosten 5 · hist. · benötigt: the_tenth_five_year_plan
  - Gosplan – Planwirtschaft: Max. Fabrikeffizienz +3 % `COLDWAR_SOV_gosplan_modifier`
  - Sozialistische Gemeinschaft: Handelsmeinung +5 % `COLDWAR_SOV_commonwealth_modifier`
- **The 1979 Economic Mechanism** `COLDWAR_SOV_the_1979_economic_mechanism` · Kosten 5 · hist. · benötigt: the_shchekino_method oder quality_mark_of_the_ussr · verfügbar: Datum ≥ 01.07.1979
  - Gosplan – Planwirtschaft: Produktivitätswachstum +3 %, Effizienzzuwachs +3 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Die letzte große Planreform der Breschnew-Zeit.
- **The Scientific-Technical Revolution** `COLDWAR_SOV_the_scientific_technical_revolution` · Kosten 10 · benötigt: the_1979_economic_mechanism, microelectronics_of_zelenograd
  - Gosplan – Planwirtschaft: Produktivitätswachstum +5 % `COLDWAR_SOV_gosplan_modifier`
  - Der Parteistaat: Forschung +3 % `COLDWAR_SOV_party_state_modifier`
  - Idee „Scientific-Technical Revolution“: Max. Fabrikeffizienz +5 %, Forschung +3 % (`add_ideas`)
  - _Anmerkung:_ Abschluss des Wirtschaftszweigs.

### Landwirtschaft & Getreide (18)

Das ewige Agrarproblem: Kolchosen, Hoflandwirtschaft, Nicht-Schwarzerde-Programm, Bewässerung (Baumwolle und Aralsee), Getreideimporte nach 1972, Lebensmittelprogramm.

- **The Agrarian Problem** `COLDWAR_SOV_the_agrarian_problem` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - PP +15 `add_political_power`
  - Gosplan – Planwirtschaft: Agrarproduktivität +3 % `COLDWAR_SOV_gosplan_modifier`
  - Zwei Grundwege, gegenseitig exklusiv
  - _Anmerkung:_ Ein Viertel aller Investitionen fließt in die Landwirtschaft – und die Ernten schwanken trotzdem um 20 %.
- **Pour Capital into the Kolkhozy** `COLDWAR_SOV_pour_capital_into_the_kolkhozy` · Kosten 5 · hist. · benötigt: the_agrarian_problem · schließt aus: the_link_system
  - Gebäude: Agrarbezirk `one_random_agriculture_district`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Agrarproduktivität +3 % `COLDWAR_SOV_gosplan_modifier`
  - Kolchosbauern +5 `COLDWAR_SOV_change_farmers_opinion_exact` → `change_farmers_opinion`
  - Kosten 0.4 % BIP `COLDWAR_SOV_pay_gdp_share`
- **Fertiliser and Machinery** `COLDWAR_SOV_fertiliser_and_machinery` · Kosten 5 · hist. · benötigt: pour_capital_into_the_kolkhozy
  - Gebäude: Agrarbezirk `one_random_agriculture_district`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Forschungsbonus CAT_agriculture +50 % ×1 `add_tech_bonus`
- **Land Melioration** `COLDWAR_SOV_land_melioration` · Kosten 5 · hist. · benötigt: pour_capital_into_the_kolkhozy
  - Gosplan – Planwirtschaft: Agrarproduktivität +4 % `COLDWAR_SOV_gosplan_modifier`
  - Kosten 0.8 % BIP `COLDWAR_SOV_pay_gdp_share`
- **The Non-Black-Earth Programme** `COLDWAR_SOV_the_non_black_earth_programme` · Kosten 7 · hist. · benötigt: fertiliser_and_machinery, land_melioration · verfügbar: Datum ≥ 01.03.1974
  - Gosplan – Planwirtschaft: Agrarproduktivität +5 % `COLDWAR_SOV_gosplan_modifier`
  - Gebäude: Agrarbezirke `two_random_agriculture_district`, Kosten 1.4 % BIP statt MD-Pauschale (`skip_payment`)
  - Zusammenhalt der Union -2 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ 1974: das russische Kernland bekommt, was bisher Ukraine und Kasachstan bekamen.
- **The Link System** `COLDWAR_SOV_the_link_system` · Kosten 5 · benötigt: the_agrarian_problem · schließt aus: pour_capital_into_the_kolkhozy
  - Gosplan – Planwirtschaft: Agrarproduktivität +8 %, Arbeitskräftebedarf Landwirtschaft -10 % `COLDWAR_SOV_gosplan_modifier`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - Kolchosbauern +10 `COLDWAR_SOV_change_farmers_opinion_exact` → `change_farmers_opinion`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ Iwan Chudenkos Experiment mit kleinen autonomen Brigaden (Ilijsk 1960er) – historisch abgebrochen, Chudenko starb 1974 in Haft.
- **Enlarge the Private Plots** `COLDWAR_SOV_enlarge_the_private_plots` · Kosten 5 · benötigt: the_link_system
  - Gosplan – Planwirtschaft: Konsumgüter -3 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität +2 % `add_stability`
  - Kolchosbauern +5 `COLDWAR_SOV_change_farmers_opinion_exact` → `change_farmers_opinion`
  - _Anmerkung:_ Die Hofparzellen: 3 % der Fläche, ein Viertel der Lebensmittel.
- **Free Kolkhoz Markets** `COLDWAR_SOV_kolkhoz_markets` · Kosten 5 · benötigt: the_link_system
  - Gosplan – Planwirtschaft: Agrarsteuer +5 % `COLDWAR_SOV_gosplan_modifier`
  - Der Parteistaat: Korruptionskosten -3 % `COLDWAR_SOV_party_state_modifier`
- **Contract Farming** `COLDWAR_SOV_contract_farming` · Kosten 7 · benötigt: enlarge_the_private_plots, kolkhoz_markets
  - Gosplan – Planwirtschaft: Agrarproduktivität +6 % `COLDWAR_SOV_gosplan_modifier`
  - Socialist Market Commonwealth +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
- **The Harvest of 1972** `COLDWAR_SOV_the_harvest_of_1972` · Kosten 3 · hist. · benötigt: the_agrarian_problem · verfügbar: Datum ≥ 01.08.1972
  - Dürre und Frost: Getreideernte 13 % unter Plan. Zwei Antworten, gegenseitig exklusiv
- **Buy Grain Abroad** `COLDWAR_SOV_buy_grain_abroad` · Kosten 3 · hist. · benötigt: the_harvest_of_1972 · schließt aus: tighten_the_belts
  - Kosten 1 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Stabilität +3 % `add_stability`
  - Meinung USA +5 `add_opinion_modifier`
  - Flag `COLDWAR_SOV_grain_importer`
  - Schaltet Entscheidung frei: Wiederholbare Getreidekäufe bei Missernten (Kosten nach BIP) `unlock_decision_tooltip`
  - _Anmerkung:_ Der „Große Getreideraub“ 1972: Moskau kauft still ein Viertel der US-Ernte.
- **Tighten the Belts** `COLDWAR_SOV_tighten_the_belts` · Kosten 3 · benötigt: the_harvest_of_1972 · schließt aus: buy_grain_abroad
  - Stabilität -6 % `add_stability`
  - Gosplan – Planwirtschaft: Konsumgüter +2 % `COLDWAR_SOV_gosplan_modifier`
  - Kolchosbauern -5 `COLDWAR_SOV_change_farmers_opinion_exact` → `change_farmers_opinion`
  - _Anmerkung:_ Keine Devisen für Getreide – die Schlangen werden länger.
- **Virgin Lands Renewal** `COLDWAR_SOV_virgin_lands_renewal` · Kosten 5 · hist. · benötigt: the_agrarian_problem
  - Gebäude: Agrarbezirk `one_random_agriculture_district`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Agrarproduktivität +3 % `COLDWAR_SOV_gosplan_modifier`
  - Zusammenhalt der Union +1 `COLDWAR_SOV_change_union_cohesion`
- **White Gold** `COLDWAR_SOV_white_gold` · Kosten 3 · hist. · benötigt: virgin_lands_renewal
  - Baumwolle aus Usbekistan – gegenseitig exklusiv
- **Irrigate the Desert** `COLDWAR_SOV_irrigate_the_desert` · Kosten 5 · hist. · benötigt: white_gold · schließt aus: save_the_aral_sea
  - Gosplan – Planwirtschaft: Agrarsteuer +6 %, Rohstoff-Exporterlöse +3 % `COLDWAR_SOV_gosplan_modifier`
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
  - Flag `COLDWAR_SOV_aral_disaster`
  - Der Parteistaat: Korruptionskosten +3 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Amu-Darja und Syr-Darja werden umgeleitet. Ab 1980 kann das Event „Der sterbende Aralsee“ feuern (Stabilität, Zusammenhalt).
- **Save the Aral Sea** `COLDWAR_SOV_save_the_aral_sea` · Kosten 5 · benötigt: white_gold · schließt aus: irrigate_the_desert
  - Gosplan – Planwirtschaft: Agrarsteuer -2 % `COLDWAR_SOV_gosplan_modifier`
  - Friends of Baikal +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Zusammenhalt der Union -2 `COLDWAR_SOV_change_union_cohesion`
- **Turn the Siberian Rivers** `COLDWAR_SOV_turn_the_siberian_rivers` · Kosten 10 · benötigt: irrigate_the_desert
  - Kosten 3 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Gosplan – Planwirtschaft: Agrarproduktivität +10 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität -3 % `add_stability`
  - Friends of Baikal -3 % Popularität (Outlook -3 %) `change_relative_party_popularity`
  - Zusammenhalt der Union +4 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Das Sibaral-Projekt (Planung ab 1970er, 1986 abgesagt): Wasser aus Ob und Irtysch nach Zentralasien.
- **The Food Programme** `COLDWAR_SOV_the_food_programme` · Kosten 7 · hist. · benötigt: the_non_black_earth_programme oder contract_farming · verfügbar: Datum ≥ 01.05.1982 ODER `COLDWAR_SOV_contract_farming` erledigt
  - Entfernt „The Agrarian Problem“ `remove_ideas`
  - Gosplan – Planwirtschaft: Agrarproduktivität +4 %, Konsumgüter -2 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Erst hier verschwindet der Startgeist „The Agrarian Problem“.

### Energie, Sibirien & BAM (15)

Samotlor und Westsibirien, Erdgas für Röhren (Ruhrgas-Mannesmann 1970), Druschba und Sojus, Kernkraft (RBMK oder WWER), Wasserkraft, die Baikal-Amur-Magistrale.

- **Samotlor: West Siberian Oil** `COLDWAR_SOV_samotlor` · Kosten 5 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Ressource: +10 Öl in einem eigenen Staat mit Öl `random_owned_controlled_state` `add_resource`
  - Gosplan – Planwirtschaft: Öl-Exporterlöse +5 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Das größte Ölfeld der UdSSR (entdeckt 1965); Förderung verzehnfacht sich bis 1980.
- **The Tyumen Oil and Gas Complex** `COLDWAR_SOV_the_tyumen_complex` · Kosten 5 · hist. · benötigt: samotlor
  - Gebäude: Infrastruktur `one_random_infrastructure`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Ressource: +8 Öl in einem eigenen Staat mit Öl `add_resource`
  - Gosplan – Planwirtschaft: Rohstoff-Exporterlöse +3 % `COLDWAR_SOV_gosplan_modifier`
- **Gas for Pipes** `COLDWAR_SOV_gas_for_pipes` · Kosten 5 · hist. · benötigt: samotlor
  - Angebot an GER (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Röhren von Mannesmann auf Kredit gegen sowjetisches Erdgas ab 1973. Bei Annahme: UdSSR erhält Forschungsbonus Infrastruktur, Handelsmeinung +10 %, Schulden 0,5 % BIP; BRD erhält Energiebonus `COLDWAR_SOV_offer_gas_for_pipes`
  - Meinung GER +10 `add_opinion_modifier`
  - _Anmerkung:_ Februar 1970, Ruhrgas–Mannesmann–Sojusnefteexport. Nur als Angebot (Spieler-BRD entscheidet).
- **Urengoy: The Gas Giant** `COLDWAR_SOV_urengoy` · Kosten 7 · benötigt: the_tyumen_complex
  - Gosplan – Planwirtschaft: Energieerzeugung +5 %, Öl-Exporterlöse +5 % `COLDWAR_SOV_gosplan_modifier`
  - Gebäude: Energieinfrastruktur `one_random_energy_infrastructure`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
- **Petrodollars** `COLDWAR_SOV_petrodollars` · Kosten 5 · benötigt: urengoy oder the_tyumen_complex · verfügbar: Ölpreis-Level (Cold War) ≥ 2 ODER Datum ≥ 01.01.1974
  - Einnahme +1 % BIP `COLDWAR_SOV_receive_gdp_share`
  - Idee „Oil Dependency“: Öl-Exporterlöse +10 %, Produktivitätswachstum -3 % (`add_ideas`)
  - _Anmerkung:_ Nach 1973 finanzieren Öl und Gas Getreideimporte und Klientelstaaten – und ersetzen die Reform.
- **The Atomic Power Programme** `COLDWAR_SOV_the_atomic_power_programme` · Kosten 3 · hist. · benötigt: samotlor
  - Welcher Reaktortyp? Gegenseitig exklusiv
- **RBMK: Channel Reactors** `COLDWAR_SOV_rbmk_reactors` · Kosten 5 · hist. · benötigt: the_atomic_power_programme · schließt aus: vver_reactors
  - Gosplan – Planwirtschaft: Bau Kernreaktoren +20 %, Kernenergie-Erzeugung +5 % `COLDWAR_SOV_gosplan_modifier`
  - Flag `COLDWAR_SOV_rbmk`
  - _Anmerkung:_ Billig, groß, ohne Containment. Setzt ein Risikoflag: Unfälle sind später per Event möglich.
- **VVER: Pressurised Reactors** `COLDWAR_SOV_vver_reactors` · Kosten 7 · benötigt: the_atomic_power_programme · schließt aus: rbmk_reactors
  - Gosplan – Planwirtschaft: Kernenergie-Erzeugung +10 % `COLDWAR_SOV_gosplan_modifier`
  - Kosten 0.8 % BIP `COLDWAR_SOV_pay_gdp_share`
- **The Leningrad Station** `COLDWAR_SOV_the_leningrad_station` · Kosten 7 · hist. · benötigt: rbmk_reactors oder vver_reactors
  - Gebäude: Kernreaktor `one_random_nuclear_reactor`, Kosten 1.2 % BIP statt MD-Pauschale (`skip_payment`)
  - _Anmerkung:_ Sosnowy Bor, erster Block 1973.
- **Atoms for the Republics** `COLDWAR_SOV_atoms_for_the_republics` · Kosten 7 · benötigt: the_leningrad_station
  - Gebäude: Kernreaktor `one_random_nuclear_reactor`, Kosten 1.2 % BIP statt MD-Pauschale (`skip_payment`)
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
- **The Great Siberian Dams** `COLDWAR_SOV_the_great_siberian_dams` · Kosten 7 · hist. · benötigt: samotlor
  - Gebäude: Erneuerbare-Energie-Anlage `one_random_renewable_energy_infra`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Energieerzeugung +5 % `COLDWAR_SOV_gosplan_modifier`
  - Friends of Baikal -1 % Popularität (Outlook -1 %) `change_relative_party_popularity`
  - _Anmerkung:_ Krasnojarsk (1972), Sajano-Schuschenskaja (Baubeginn 1968).
- **The Baikal-Amur Mainline** `COLDWAR_SOV_the_baikal_amur_mainline` · Kosten 10 · hist. · benötigt: the_great_siberian_dams oder the_tyumen_complex · verfügbar: Datum ≥ 01.04.1974
  - Kosten 2 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Gebäude: Infrastruktur `three_random_infrastructure`
  - Communist Party of the Soviet Union +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
  - Streitkräfte der UdSSR: Versorgungsverbrauch -2 % `COLDWAR_SOV_armed_forces_modifier`
  - Idee „Construction of the Century“: Bau Eisenbahn +25 %, Konsumgüter +2 % (1825 Tage `add_timed_idea`)
  - _Anmerkung:_ „Baustelle des Jahrhunderts“ – Komsomol-Freiwillige, 4.300 km durch Taiga und Permafrost.
- **BAM Open to Traffic** `COLDWAR_SOV_bam_open_to_traffic` · Kosten 7 · benötigt: the_baikal_amur_mainline · verfügbar: Datum ≥ 01.01.1980
  - Gebäude: Infrastruktur `two_random_infrastructure`
  - Gosplan – Planwirtschaft: Rohstoff-Exporterlöse +5 % `COLDWAR_SOV_gosplan_modifier`
  - Streitkräfte der UdSSR: Versorgungsverbrauch -2 % `COLDWAR_SOV_armed_forces_modifier`
  - Bonus für „The Chinese Question“: Nachschub im Fernen Osten verbessert (`COLDWAR_SOV_bam_open`)
  - Flag `COLDWAR_SOV_bam_open`
- **Kuzbass and Ekibastuz** `COLDWAR_SOV_kuzbass_and_ekibastuz` · Kosten 5 · hist. · benötigt: the_tyumen_complex
  - Gebäude: Energieinfrastruktur `one_random_energy_infrastructure`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Erzeugung fossiler Kraftwerke +5 % `COLDWAR_SOV_gosplan_modifier`
  - Zusammenhalt der Union +1 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Kohle aus dem Kusnezker Becken und Ekibastus (Kasachstan) für die Kraftwerke des Urals.
- **The Unified Energy System** `COLDWAR_SOV_the_unified_energy_system` · Kosten 7 · hist. · benötigt: kuzbass_and_ekibastuz, the_leningrad_station oder the_great_siberian_dams
  - Gebäude: Energieinfrastruktur `one_random_energy_infrastructure`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
  - Gosplan – Planwirtschaft: Energieerzeugung +5 % `COLDWAR_SOV_gosplan_modifier`
  - Sozialistische Gemeinschaft: Handelsmeinung im Bündnis +5 % `COLDWAR_SOV_commonwealth_modifier`
  - _Anmerkung:_ Das Verbundnetz „Mir“ verbindet die Netze des RGW.

### Wissenschaft & Kosmos (17)

Akademie der Wissenschaften, Akademgorodok, Lunochod, N1-Mondrakete oder Raumstationen (Saljut), Sojus-Apollo, Großforschung.

- **The Academy of Sciences** `COLDWAR_SOV_the_academy_of_sciences` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - PP +15 `add_political_power`
- **Akademgorodok** `COLDWAR_SOV_akademgorodok` · Kosten 5 · hist. · benötigt: the_academy_of_sciences
  - Gebäude: Büro `one_office_construction`, Kosten 0.6 % BIP statt MD-Pauschale (`skip_payment`)
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - Forschungsbonus CAT_computing +25 % ×1 `add_tech_bonus`
- **The Naukograds** `COLDWAR_SOV_the_naukograds` · Kosten 7 · hist. · benötigt: akademgorodok
  - Gebäude: Kernforschungsanlage `one_random_nuclear_facility`
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - Streitkräfte der UdSSR: Ausrüstungskosten -2 % `COLDWAR_SOV_armed_forces_modifier`
  - _Anmerkung:_ Geschlossene Wissenschaftsstädte (Arsamas-16, Obninsk, Dubna).
- **Genetics Rehabilitated** `COLDWAR_SOV_genetics_rehabilitated` · Kosten 5 · benötigt: the_academy_of_sciences
  - Forschungsbonus CAT_genetics +50 % ×1 `add_tech_bonus`
  - Gosplan – Planwirtschaft: Agrarproduktivität +3 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Lyssenko ist seit 1965 entmachtet; die Biologie holt auf.
- **Scientific Exchange with the West** `COLDWAR_SOV_scientific_exchange` · Kosten 5 · benötigt: akademgorodok
  - Der Parteistaat: Forschung +3 %, Ideologische Driftabwehr -5 % `COLDWAR_SOV_party_state_modifier`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - _Anmerkung:_ IIASA in Laxenburg (1972), gemeinsame Kommissionen mit den USA.
- **The Space Race Question** `COLDWAR_SOV_the_space_race_question` · Kosten 3 · hist. · benötigt: the_academy_of_sciences
  - Raumfahrtprogramm-Fortschritt `add_space_program_progress`
  - N1 oder Raumstationen – gegenseitig exklusiv
- **Lunokhod** `COLDWAR_SOV_lunokhod` · Kosten 5 · hist. · benötigt: the_space_race_question
  - Raumfahrtprogramm-Fortschritt `add_space_program_progress`
  - Stabilität +2 % `add_stability`
  - Forschungsbonus CAT_satellites +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ 17.11.1970: das erste ferngesteuerte Fahrzeug auf dem Mond.
- **Venera: The Road to Venus** `COLDWAR_SOV_venera` · Kosten 5 · hist. · benötigt: lunokhod
  - Raumfahrtprogramm-Fortschritt `add_space_program_progress`
  - Der Parteistaat: Forschung +1 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ 15.12.1970: Venera 7, erste Landung auf einem anderen Planeten.
- **Korolev's Dream: The N1** `COLDWAR_SOV_the_n1_moon_rocket` · Kosten 7 · benötigt: the_space_race_question · schließt aus: the_orbital_stations
  - Kosten 1.5 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Raumfahrtprogramm-Fortschritt `add_space_program_progress`
  - Forschungsbonus CAT_orbital_launch_vehicles +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ Alt-Hist: Das Mondprogramm wird nach vier Fehlstarts nicht eingestellt.
- **The Soviet Moonshot** `COLDWAR_SOV_the_soviet_moonshot` · Kosten 10 · benötigt: the_n1_moon_rocket
  - Kosten 2.5 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Raumfahrtprogramm-Fortschritt `add_space_program_progress`
  - Raumfahrtprogramm-Fortschritt `add_space_program_progress`
  - Idee „Red Moon“: Stabilität +5 %, Kriegsunterstützung +3 %, Forschung +3 % (1095 Tage `add_timed_idea`)
  - Event: Ein Kosmonaut auf dem Mond – Weltpresse, Jubel in Moskau
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
- **The Orbital Stations** `COLDWAR_SOV_the_orbital_stations` · Kosten 5 · hist. · benötigt: the_space_race_question · schließt aus: the_n1_moon_rocket
  - Raumfahrtprogramm-Fortschritt `add_space_program_progress`
  - Forschungsbonus CAT_satellites +50 % ×1 `add_tech_bonus`
  - Der Parteistaat: Forschung +2 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Saljut 1 (April 1971).
- **Soyuz-Apollo** `COLDWAR_SOV_soyuz_apollo` · Kosten 5 · hist. · benötigt: the_orbital_stations · verfügbar: Datum ≥ 01.01.1975
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Gemeinsamer Flug (ASTP). Bei Annahme: beide +3 % Forschung für 2 Jahre, Spannung −1, Meinung +15 `COLDWAR_SOV_offer_soyuz_apollo`
  - _Anmerkung:_ Juli 1975.
- **Answer the Space Shuttle** `COLDWAR_SOV_the_space_shuttle_answer` · Kosten 3 · benötigt: soyuz_apollo oder the_soviet_moonshot
  - Gegenseitig exklusiv: Buran oder Mir
- **Energia-Buran** `COLDWAR_SOV_energia_buran` · Kosten 10 · benötigt: the_space_shuttle_answer · schließt aus: mir_station
  - Kosten 3 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Spezialprojekt `sp:sp_space_program` +25 % Fortschritt `add_project_progress_ratio`
  - Rüstungskomplex (VPK) +10 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - Forschungsbonus CAT_orbital_launch_vehicles +50 % ×1 `add_tech_bonus`
- **Mir: The Permanent Station** `COLDWAR_SOV_mir_station` · Kosten 7 · benötigt: the_space_shuttle_answer · schließt aus: energia_buran
  - Raumfahrtprogramm-Fortschritt `add_space_program_progress`
  - Der Parteistaat: Forschung +3 % `COLDWAR_SOV_party_state_modifier`
  - Stabilität +2 % `add_stability`
- **Zenit: Eyes in Orbit** `COLDWAR_SOV_eyes_in_orbit` · Kosten 5 · hist. · benötigt: the_orbital_stations oder the_n1_moon_rocket
  - Forschungsbonus CAT_reconnaissance_satellites +50 % ×1 `add_tech_bonus`
  - Streitkräfte der UdSSR: Planungsgeschwindigkeit +0.05 `COLDWAR_SOV_armed_forces_modifier`
- **The Scientific Superpower** `COLDWAR_SOV_the_scientific_superpower` · Kosten 7 · benötigt: the_naukograds, mir_station oder energia_buran
  - Idee „Scientific Superpower“: Forschung +5 % (`add_ideas`)
  - Stabilität +2 % `add_stability`

### Sowjetarmee (22)

Gretschko/Ustinow: Tiefe Operation, operative Manövergruppen, T-64/T-72, BMP, Luftlandetruppen, Fernostfront, Doktrin.

- **The Soviet Army** `COLDWAR_SOV_the_soviet_army` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Heereserfahrung +25 `army_experience`
  - Kommandomacht +20 `add_command_power`
  - Streitkräfte der UdSSR: Planungsgeschwindigkeit +0.05 `COLDWAR_SOV_armed_forces_modifier`
- **Grechko's Ministry** `COLDWAR_SOV_grechkos_ministry` · Kosten 5 · hist. · benötigt: the_soviet_army
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Streitkräfte der UdSSR: Organisation (Heer) +2 % `COLDWAR_SOV_armed_forces_modifier`
  - Forschungsbonus CAT_infantry_weapons +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ Marschall Andrei Gretschko, Verteidigungsminister 1967–1976.
- **The Doctrine Debate** `COLDWAR_SOV_the_doctrine_debate` · Kosten 3 · hist. · benötigt: grechkos_ministry
  - Konventionell tief oder nuklear? Gegenseitig exklusiv
- **Deep Operations Revived** `COLDWAR_SOV_deep_operations_revived` · Kosten 5 · hist. · benötigt: the_doctrine_debate · schließt aus: the_nuclear_battlefield
  - Doktrin-Mastery land +50 `add_mastery`
  - Streitkräfte der UdSSR: Durchbruch +3 %, Planungsgeschwindigkeit +0.05 `COLDWAR_SOV_armed_forces_modifier`
  - _Anmerkung:_ Tuchatschewskis Tiefe Operation, ab Mitte der 1970er wieder Leitbild.
- **The Nuclear Battlefield** `COLDWAR_SOV_the_nuclear_battlefield` · Kosten 5 · benötigt: the_doctrine_debate · schließt aus: deep_operations_revived
  - Streitkräfte der UdSSR: Verteidigung (Heer) +2 %, Organisation (Heer) +3 % `COLDWAR_SOV_armed_forces_modifier`
  - Forschungsbonus CAT_ballistic_missiles +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ Sokolowskis „Militärstrategie“ (1962): jeder Krieg in Europa wird nuklear.
- **Operational Manoeuvre Groups** `COLDWAR_SOV_operational_manoeuvre_groups` · Kosten 7 · benötigt: deep_operations_revived · verfügbar: Datum ≥ 01.01.1977
  - Streitkräfte der UdSSR: Durchbruch +3 %, Heeresgeschwindigkeit +3 % `COLDWAR_SOV_armed_forces_modifier`
  - Doktrin-Mastery land +50 `add_mastery`
  - _Anmerkung:_ Ogarkows OMG-Konzept.
- **Theatres of Military Operations** `COLDWAR_SOV_theatres_of_military_operations` · Kosten 5 · hist. · benötigt: deep_operations_revived oder the_nuclear_battlefield · verfügbar: Datum ≥ 01.01.1979
  - Streitkräfte der UdSSR: Max. Planung +5 % `COLDWAR_SOV_armed_forces_modifier`
  - Kommandomacht +30 `add_command_power`
  - _Anmerkung:_ 1979: Oberkommandos für die TVD West, Südwest, Süd und Fernost.
- **The Tank Question** `COLDWAR_SOV_the_tank_question` · Kosten 3 · hist. · benötigt: the_soviet_army
  - Ein Hauptpanzer oder zwei? Gegenseitig exklusiv
- **T-64: Morozov's Masterpiece** `COLDWAR_SOV_t64_morozovs_masterpiece` · Kosten 5 · benötigt: the_tank_question · schließt aus: t72_the_mass_tank
  - Forschungsbonus CAT_main_battle_tanks +50 % ×2 `add_tech_bonus`
  - Streitkräfte der UdSSR: Ausrüstungskosten +3 % `COLDWAR_SOV_armed_forces_modifier`
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - _Anmerkung:_ Charkiw: modernster Panzer der Welt, teuer und kompliziert.
- **T-72: The Mass Tank** `COLDWAR_SOV_t72_the_mass_tank` · Kosten 5 · hist. · benötigt: the_tank_question · schließt aus: t64_morozovs_masterpiece
  - Forschungsbonus CAT_main_battle_tanks +50 % ×1 `add_tech_bonus`
  - Streitkräfte der UdSSR: Ausrüstungskosten -4 % `COLDWAR_SOV_armed_forces_modifier`
  - Gebäude: Rüstungsfabrik `one_random_arms_factory`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
  - _Anmerkung:_ Uralwagonsawod: der Mobilisierungspanzer, auch für den Export.
- **T-80: The Gas Turbine Tank** `COLDWAR_SOV_t80_gas_turbine` · Kosten 5 · benötigt: t64_morozovs_masterpiece oder t72_the_mass_tank · verfügbar: Datum ≥ 01.01.1976
  - Forschungsbonus CAT_main_battle_tanks, CAT_tank_engines +50 % ×1 `add_tech_bonus`
- **BMP: Infantry in Armour** `COLDWAR_SOV_bmp_infantry_in_armour` · Kosten 5 · hist. · benötigt: the_tank_question
  - Forschungsbonus CAT_infantry_fighting_vehicles +75 % ×1 `add_tech_bonus`
  - Streitkräfte der UdSSR: Mechanisiert-Angriff +2 % `COLDWAR_SOV_armed_forces_modifier`
- **AK-74** `COLDWAR_SOV_ak74` · Kosten 5 · hist. · benötigt: grechkos_ministry
  - Forschungsbonus CAT_small_arms +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ Eingeführt 1974.
- **The Praporshchiki** `COLDWAR_SOV_the_praporshchiki` · Kosten 5 · hist. · benötigt: grechkos_ministry
  - Streitkräfte der UdSSR: Organisation (Heer) +3 % `COLDWAR_SOV_armed_forces_modifier`
  - Streitkräfte der UdSSR: Personalkosten Heer +2 % `COLDWAR_SOV_armed_forces_modifier`
  - _Anmerkung:_ 1972: Fähnriche als Berufskader zwischen Wehrpflichtigen und Offizieren.
- **Against Dedovshchina** `COLDWAR_SOV_against_dedovshchina` · Kosten 5 · benötigt: the_praporshchiki
  - Streitkräfte der UdSSR: Moral (Heer) +4 % `COLDWAR_SOV_armed_forces_modifier`
  - Armee & Generalstab -5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - _Anmerkung:_ Die Schikane der „Großväter“ – Reform kostet die Altgedienten.
- **Margelov's Airborne** `COLDWAR_SOV_margelovs_airborne` · Kosten 5 · hist. · benötigt: the_soviet_army
  - Streitkräfte der UdSSR: Luftlande-Organisation +10 %, Spezialkräfte-Limit +0.05 `COLDWAR_SOV_armed_forces_modifier`
  - Forschungsbonus CAT_special_forces_equipment +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ „Onkel Wasjas Truppen“ – die WDW werden zur strategischen Reserve.
- **Spetsnaz of the GRU** `COLDWAR_SOV_spetsnaz_of_the_gru` · Kosten 5 · benötigt: margelovs_airborne
  - Streitkräfte der UdSSR: Spezialkräfte-Angriff +5 %, Spezialkräfte-Limit +0.05 `COLDWAR_SOV_armed_forces_modifier`
- **Mi-24: The Flying Tank** `COLDWAR_SOV_mi24_the_flying_tank` · Kosten 5 · hist. · benötigt: margelovs_airborne
  - Forschungsbonus CAT_attack_helicopters +75 % ×1 `add_tech_bonus`
- **Grad and Uragan** `COLDWAR_SOV_rocket_artillery` · Kosten 5 · benötigt: the_tank_question
  - Forschungsbonus CAT_artillery +50 % ×1 `add_tech_bonus`
  - Streitkräfte der UdSSR: Raketenartillerie-Angriff +5 % `COLDWAR_SOV_armed_forces_modifier`
- **Universal Military Duty** `COLDWAR_SOV_universal_military_duty` · Kosten 5 · hist. · benötigt: grechkos_ministry
  - Streitkräfte der UdSSR: Rekrutierbare Bevölkerung +5 %, Ausbildungszeit -5 % `COLDWAR_SOV_armed_forces_modifier`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - _Anmerkung:_ Wehrgesetz von 1967: zwei Jahre Dienst, DOSAAF-Vorausbildung.
- **Ustinov's Ministry** `COLDWAR_SOV_ustinovs_ministry` · Kosten 5 · hist. · benötigt: theatres_of_military_operations oder against_dedovshchina · verfügbar: Datum ≥ 01.05.1976
  - Streitkräfte der UdSSR: Ausrüstungskosten -3 % `COLDWAR_SOV_armed_forces_modifier`
  - Rüstungskomplex (VPK) +10 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - Armee & Generalstab -5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - _Anmerkung:_ Dmitri Ustinow, der „Rüstungsmanager“, wird 1976 Verteidigungsminister.
- **The Army of a Superpower** `COLDWAR_SOV_the_army_of_a_superpower` · Kosten 7 · benötigt: ustinovs_ministry, t80_gas_turbine oder operational_manoeuvre_groups
  - Idee „Army of a Superpower“: Angriff (Heer) +2 %, Verteidigung (Heer) +2 %, Organisation (Heer) +3 % (`add_ideas`)
  - Heereserfahrung +50 `army_experience`

### Strategische Kräfte & Luftverteidigung (14)

Strategische Raketentruppen, Parität und SS-18/SS-20, PWO, Luftstreitkräfte, Raketenabwehr um Moskau.

- **Strategic Rocket Forces** `COLDWAR_SOV_strategic_rocket_forces` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Forschungsbonus CAT_intercontinental_ballistic_missiles +50 % ×1 `add_tech_bonus`
  - Armee & Generalstab +3 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **Nuclear Parity** `COLDWAR_SOV_nuclear_parity` · Kosten 5 · hist. · benötigt: strategic_rocket_forces
  - Kriegsunterstützung +3 % `add_war_support`
  - Idee „Nuclear Parity“: Kriegsunterstützung +2 %, Kriegsgrund-Zeit gegen uns +10 % (`add_ideas`)
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
  - _Anmerkung:_ 1969/70 erreicht die UdSSR erstmals die Zahl amerikanischer Interkontinentalraketen.
- **R-36M: The Heavy ICBM** `COLDWAR_SOV_the_heavy_icbm` · Kosten 7 · benötigt: nuclear_parity · schließt aus: mirv_and_mobile_launchers
  - Forschungsbonus CAT_intercontinental_ballistic_missiles +50 % ×2 `add_tech_bonus`
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - _Anmerkung:_ SS-18 „Satan“ – Erstschlagsfähigkeit gegen Minuteman-Silos.
- **MIRVs and Mobile Launchers** `COLDWAR_SOV_mirv_and_mobile_launchers` · Kosten 7 · benötigt: nuclear_parity · schließt aus: the_heavy_icbm
  - Forschungsbonus CAT_transporter_erector_launchers +75 % ×1 `add_tech_bonus`
  - Forschungsbonus CAT_intercontinental_ballistic_missiles +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ Überlebensfähigkeit statt Masse.
- **Pioneer: The SS-20** `COLDWAR_SOV_pioneer_the_ss20` · Kosten 5 · benötigt: the_heavy_icbm oder mirv_and_mobile_launchers · verfügbar: Datum ≥ 01.01.1976
  - Forschungsbonus CAT_intermediate_range_ballistic_missiles +75 % ×1 `add_tech_bonus`
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
  - Meinung GER -10 `add_opinion_modifier`
  - _Anmerkung:_ Löst die Nachrüstungskrise aus – Europa als Geisel.
- **PVO Strany** `COLDWAR_SOV_pvo_strany` · Kosten 5 · hist. · benötigt: strategic_rocket_forces
  - Forschungsbonus CAT_surface_to_air_missiles +50 % ×1 `add_tech_bonus`
  - Streitkräfte der UdSSR: Flak-Schaden (stationär) +10 % `COLDWAR_SOV_armed_forces_modifier`
  - _Anmerkung:_ Die Luftverteidigung des Landes – eigene Teilstreitkraft.
- **A-35: The Moscow Shield** `COLDWAR_SOV_the_moscow_shield` · Kosten 7 · hist. · benötigt: pvo_strany
  - Gebäude: Flugabwehrstellung `one_anti_air`
  - Gebäude: Flugabwehrstellung `one_anti_air`
  - Forschungsbonus CAT_anti_air +50 % ×1 `add_tech_bonus`
  - Kosten 0.6 % BIP `COLDWAR_SOV_pay_gdp_share`
- **Frontal Aviation** `COLDWAR_SOV_frontal_aviation` · Kosten 5 · hist. · benötigt: strategic_rocket_forces
  - Doktrin-Mastery air +50 `add_mastery`
  - Lufterfahrung +25 `air_experience`
- **Swing Wings: MiG-23 and Su-24** `COLDWAR_SOV_swing_wings` · Kosten 5 · hist. · benötigt: frontal_aviation
  - Forschungsbonus CAT_wing_designs, CAT_medium_aircraft +50 % ×1 `add_tech_bonus`
- **MiG-25 Foxbat** `COLDWAR_SOV_mig25_foxbat` · Kosten 5 · hist. · benötigt: frontal_aviation
  - Forschungsbonus CAT_air_engines +50 % ×1 `add_tech_bonus`
  - Streitkräfte der UdSSR: Abfang-Effizienz +5 % `COLDWAR_SOV_armed_forces_modifier`
- **Long-Range Aviation** `COLDWAR_SOV_long_range_aviation` · Kosten 5 · hist. · benötigt: frontal_aviation
  - Forschungsbonus CAT_heavy_aircraft +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ Tu-22M „Backfire“.
- **The Fourth Generation** `COLDWAR_SOV_the_fourth_generation` · Kosten 7 · benötigt: swing_wings oder mig25_foxbat · verfügbar: Datum ≥ 01.01.1977
  - Forschungsbonus CAT_medium_aircraft +50 % ×2 `add_tech_bonus`
  - Spezialprojekt `sp:sp_aircraft_project` +15 % Fortschritt `add_project_progress_ratio`
  - _Anmerkung:_ Su-27 und MiG-29.
- **Civil Defence of the USSR** `COLDWAR_SOV_civil_defence_of_the_ussr` · Kosten 5 · hist. · benötigt: pvo_strany
  - Streitkräfte der UdSSR: Verteidigung auf Kerngebiet +3 % `COLDWAR_SOV_armed_forces_modifier`
  - Stabilität +1 % `add_stability`
  - Gosplan – Planwirtschaft: Sozialkosten +2 % `COLDWAR_SOV_gosplan_modifier`
- **The Correlation of Forces** `COLDWAR_SOV_strategic_superiority` · Kosten 7 · benötigt: pioneer_the_ss20 oder the_moscow_shield, the_fourth_generation
  - Idee „The Correlation of Forces“: Kriegsunterstützung +3 %, PP-Gewinn +3 %, Kriegsgrund-Zeit gegen uns +15 % (`add_ideas`)
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
  - _Anmerkung:_ „Das Kräfteverhältnis hat sich zugunsten des Sozialismus verschoben“ (XXV. Parteitag 1976).

### Hochseeflotte (15)

Gorschkows Hochseeflotte: Okean-70, U-Boot-Flotte, Kiew-Klasse, Mittelmeergeschwader (5. Eskadra), Stützpunkte nur per Angebot.

- **Gorshkov's Ocean-Going Navy** `COLDWAR_SOV_gorshkovs_navy` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Marineerfahrung +25 `navy_experience`
  - Streitkräfte der UdSSR: Reichweite Marine +5 % `COLDWAR_SOV_armed_forces_modifier`
  - _Anmerkung:_ Admiral Sergei Gorschkow, Oberbefehlshaber 1956–1985.
- **Exercise Okean-70** `COLDWAR_SOV_okean_70` · Kosten 3 · hist. · benötigt: gorshkovs_navy · verfügbar: Datum < 01.01.1972
  - Marineerfahrung +50 `navy_experience`
  - Kriegsunterstützung +2 % `add_war_support`
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
  - _Anmerkung:_ April 1970: das größte Marinemanöver der Nachkriegszeit, alle vier Flotten.
- **Sea Power of the State** `COLDWAR_SOV_the_navy_question` · Kosten 3 · hist. · benötigt: gorshkovs_navy
  - U-Boote oder Überwasserflotte? Gegenseitig exklusiv
- **The Submarine Fleet** `COLDWAR_SOV_the_submarine_fleet` · Kosten 5 · hist. · benötigt: the_navy_question · schließt aus: carriers_and_cruisers
  - Forschungsbonus CAT_missile_submarines, CAT_attack_submarines +50 % ×1 `add_tech_bonus`
- **The Bastion Strategy** `COLDWAR_SOV_the_bastion_strategy` · Kosten 5 · hist. · benötigt: the_submarine_fleet
  - Streitkräfte der UdSSR: U-Boot-Angriff +5 % `COLDWAR_SOV_armed_forces_modifier`
  - Forschungsbonus CAT_naval_sonar +50 % ×1 `add_tech_bonus`
  - _Anmerkung:_ SSBN in geschützten Bastionen (Barentssee, Ochotskisches Meer).
- **Lira: The Titanium Submarine** `COLDWAR_SOV_lira_the_titanium_submarine` · Kosten 7 · benötigt: the_submarine_fleet
  - Forschungsbonus CAT_submarine_engines +75 % ×1 `add_tech_bonus`
  - Kosten 0.5 % BIP `COLDWAR_SOV_pay_gdp_share`
  - _Anmerkung:_ Projekt 705 „Alfa“.
- **Akula: The Typhoon** `COLDWAR_SOV_akula_the_typhoon` · Kosten 7 · benötigt: the_bastion_strategy oder lira_the_titanium_submarine · verfügbar: Datum ≥ 01.01.1977
  - Forschungsbonus CAT_missile_submarines +50 % ×2 `add_tech_bonus`
  - Spezialprojekt `sp:sp_naval_vessel_project` +15 % Fortschritt `add_project_progress_ratio`
- **Carriers and Cruisers** `COLDWAR_SOV_carriers_and_cruisers` · Kosten 5 · benötigt: the_navy_question · schließt aus: the_submarine_fleet
  - Forschungsbonus CAT_aircraft_carriers, CAT_cruisers +50 % ×1 `add_tech_bonus`
  - Gebäude: Werft `one_random_dockyard`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
- **The Kiev Class** `COLDWAR_SOV_the_kiev_class` · Kosten 7 · benötigt: carriers_and_cruisers
  - Forschungsbonus CAT_aircraft_carriers +75 % ×1 `add_tech_bonus`
  - Streitkräfte der UdSSR: Werftleistung +5 % `COLDWAR_SOV_armed_forces_modifier`
  - _Anmerkung:_ Schwere Flugzeugträgerkreuzer ab 1975.
- **Kirov: The Battlecruiser** `COLDWAR_SOV_kirov_the_battlecruiser` · Kosten 7 · benötigt: carriers_and_cruisers · verfügbar: Datum ≥ 01.01.1977
  - Forschungsbonus CAT_cruisers, CAT_naval_anti_ship_missiles +50 % ×1 `add_tech_bonus`
- **The Fifth Eskadra** `COLDWAR_SOV_the_fifth_eskadra` · Kosten 5 · hist. · benötigt: okean_70 oder the_navy_question
  - Streitkräfte der UdSSR: Reichweite Marine +5 % `COLDWAR_SOV_armed_forces_modifier`
  - Angebot an SYR (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Marine-Versorgungspunkt Tartus (1971). Bei Annahme: Syrien erhält Militärhilfe (+5 % Organisation), UdSSR Reichweite Marine +5 % `COLDWAR_SOV_offer_tartus_supply_point`
  - Antwortet auf Ägyptens Angebot „Facilities for the Eskadra“ (EGY-Baum), falls angenommen
  - _Anmerkung:_ Das Mittelmeergeschwader, Gegengewicht zur 6. US-Flotte.
- **Naval Missile Aviation** `COLDWAR_SOV_naval_missile_aviation` · Kosten 5 · hist. · benötigt: the_navy_question
  - Forschungsbonus CAT_air_to_naval_weapons +50 % ×1 `add_tech_bonus`
- **Bases on Three Oceans** `COLDWAR_SOV_bases_on_three_oceans` · Kosten 5 · benötigt: the_fifth_eskadra
  - Angebot an SOM, SYE, VIE (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Hafenrechte (Berbera, Aden, Cam Ranh). Bei Annahme: Partner erhält Hilfe 0,3 % unseres BIP; wir Reichweite Marine +5 % je Hafen `COLDWAR_SOV_offer_naval_access`
  - _Anmerkung:_ Nur per Angebot – kein Partner wird gezwungen.
- **Severodvinsk and Nikolaev** `COLDWAR_SOV_the_shipyards_of_the_north` · Kosten 7 · hist. · benötigt: the_navy_question
  - Gebäude: Werft `one_random_dockyard`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
  - Gebäude: Werft `one_random_dockyard`, Kosten 1 % BIP statt MD-Pauschale (`skip_payment`)
- **A Navy of a Superpower** `COLDWAR_SOV_a_navy_of_a_superpower` · Kosten 7 · benötigt: akula_the_typhoon oder kirov_the_battlecruiser oder the_kiev_class, bases_on_three_oceans
  - Idee „Blue-Water Navy“: Reichweite Marine +10 %, Marine-Schaden +3 %, Organisation Marine +3 % (`add_ideas`)
  - Marineerfahrung +50 `navy_experience`

### KGB & innere Sicherheit (16)

Andropows KGB: Fünfte Verwaltung, Dissidenten (Psychiatrie, Ausweisung oder Duldung), jüdische Emigration, Auslandsaufklärung, aktive Maßnahmen.

- **Andropov's KGB** `COLDWAR_SOV_andropovs_kgb` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Der Parteistaat: Ideologische Driftabwehr +5 % `COLDWAR_SOV_party_state_modifier`
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - _Anmerkung:_ Juri Andropow, KGB-Vorsitzender 1967–1982.
- **The Fifth Directorate** `COLDWAR_SOV_the_fifth_directorate` · Kosten 5 · hist. · benötigt: andropovs_kgb
  - Der Parteistaat: Ideologische Abwehr (Cold War) +10 %, Fremde Subversion -10 % `COLDWAR_SOV_party_state_modifier`
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - _Anmerkung:_ 1967 gegründet zur Bekämpfung „ideologischer Diversion“.
- **The Dissident Question** `COLDWAR_SOV_the_dissident_question` · Kosten 3 · hist. · benötigt: the_fifth_directorate
  - Drei Antworten, gegenseitig exklusiv
- **Punitive Psychiatry** `COLDWAR_SOV_punitive_psychiatry` · Kosten 5 · benötigt: the_dissident_question · schließt aus: exile_and_expulsion, tolerate_the_samizdat
  - ersetzt „Samizdat and Dissent“: Idee „Silenced Dissent“: Stabilität +3 %, Ideologische Driftabwehr +10 %, Forschung -2 %, Handelsmeinung -5 % (`swap_ideas`)
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - Meinung USA -5 `add_opinion_modifier`
  - _Anmerkung:_ Die „Psychuschka“ – Diagnose „träge Schizophrenie“.
- **Exile and Expulsion** `COLDWAR_SOV_exile_and_expulsion` · Kosten 5 · hist. · benötigt: the_dissident_question · schließt aus: punitive_psychiatry, tolerate_the_samizdat
  - ersetzt „Samizdat and Dissent“: Idee „Dissent Abroad“: Stabilität +1 %, Demokratische Drift +0.01, Handelsmeinung -3 % (`swap_ideas`)
  - Event: Solschenizyn wird ausgebürgert und nach Frankfurt ausgeflogen
  - _Anmerkung:_ Historischer Mittelweg: Gorki-Verbannung für Sacharow, Ausbürgerung für Solschenizyn (1974).
- **Tolerate the Samizdat** `COLDWAR_SOV_tolerate_the_samizdat` · Kosten 5 · benötigt: the_dissident_question · schließt aus: punitive_psychiatry, exile_and_expulsion
  - ersetzt „Samizdat and Dissent“: Idee „Socialist Pluralism“: Forschung +3 %, Demokratische Drift +0.03, Stabilität -2 % (`swap_ideas`)
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
  - KGB -10 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - Committee for Human Rights +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
- **The Refusenik Question** `COLDWAR_SOV_the_refusenik_question` · Kosten 3 · hist. · benötigt: the_fifth_directorate
  - Jüdische Emigration – gegenseitig exklusiv
- **Open the Gates** `COLDWAR_SOV_open_the_gates` · Kosten 5 · benötigt: the_refusenik_question · schließt aus: the_diploma_tax
  - Gosplan – Planwirtschaft: Handelsmeinung +10 % `COLDWAR_SOV_gosplan_modifier`
  - Der Parteistaat: Forschung -1 % `COLDWAR_SOV_party_state_modifier`
  - Meinung USA +10 `add_opinion_modifier`
  - Meinung ISR +5 `add_opinion_modifier`
  - _Anmerkung:_ Erleichtert den Handel (Jackson-Vanik), kostet Fachkräfte.
- **The Diploma Tax** `COLDWAR_SOV_the_diploma_tax` · Kosten 3 · hist. · benötigt: the_refusenik_question · schließt aus: open_the_gates
  - Einnahme +0.1 % BIP `COLDWAR_SOV_receive_gdp_share`
  - Gosplan – Planwirtschaft: Handelsmeinung -10 % `COLDWAR_SOV_gosplan_modifier`
  - Meinung USA -10 `add_opinion_modifier`
  - _Anmerkung:_ August 1972: Ausreisende müssen ihre Ausbildung zurückzahlen.
- **The First Chief Directorate** `COLDWAR_SOV_the_first_chief_directorate` · Kosten 5 · hist. · benötigt: andropovs_kgb
  - Der Parteistaat: Geheimdienstnetz-Zuwachs +10 %, Entschlüsselung +5 % `COLDWAR_SOV_party_state_modifier`
- **Active Measures** `COLDWAR_SOV_active_measures` · Kosten 5 · hist. · benötigt: the_first_chief_directorate
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +10 % `COLDWAR_SOV_commonwealth_modifier`
  - Der Parteistaat: Auslandseinfluss +5 % `COLDWAR_SOV_party_state_modifier`
  - _Anmerkung:_ Dienst A: Desinformation, Fälschungen, Friedensbewegungen.
- **The Illegals** `COLDWAR_SOV_the_illegals` · Kosten 5 · benötigt: the_first_chief_directorate
  - Der Parteistaat: Geheimdienstnetz-Zuwachs +10 %, Verschlüsselung +5 % `COLDWAR_SOV_party_state_modifier`
- **KGB Border Troops** `COLDWAR_SOV_kgb_border_troops` · Kosten 5 · hist. · benötigt: andropovs_kgb
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
  - Der Parteistaat: Fremde Subversion -5 % `COLDWAR_SOV_party_state_modifier`
- **Operation RYaN** `COLDWAR_SOV_operation_ryan` · Kosten 5 · hist. · benötigt: active_measures oder the_illegals · verfügbar: Datum ≥ 01.05.1981
  - Streitkräfte der UdSSR: Planungsgeschwindigkeit +0.05 `COLDWAR_SOV_armed_forces_modifier`
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
  - Kriegsunterstützung +2 % `add_war_support`
  - _Anmerkung:_ Raketno-Jadernoje Napadenije – Suche nach Anzeichen eines westlichen Erstschlags.
- **The Anti-Corruption Drive** `COLDWAR_SOV_the_anti_corruption_drive` · Kosten 7 · benötigt: kgb_border_troops oder the_first_chief_directorate
  - Korruption −1 Stufe `decrease_corruption`
  - Der Parteistaat: Korruptionskosten -10 % `COLDWAR_SOV_party_state_modifier`
  - Nomenklatura -10 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
- **The Shield and the Sword** `COLDWAR_SOV_the_shield_and_the_sword` · Kosten 7 · benötigt: the_anti_corruption_drive oder operation_ryan
  - Idee „The Shield and the Sword“: Spionageabwehr +15 %, Ideologische Driftabwehr +5 %, Fremde Subversion -10 % (`add_ideas`)
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`

### Die Union der Republiken (23)

Der Zusammenhalt der Union: Ukraine (Schelest oder Schtscherbizki), Baltikum, Kaukasus, Zentralasien, Russifizierung oder Föderalisierung, Kaderrotation.

- **The Union of Republics** `COLDWAR_SOV_the_union_of_republics` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
  - Schaltet Entscheidung frei: Kategorie „Die Union“: Entwicklungsfonds der Republiken, Kaderrotation, Russischkampagne, souveräne Rechte – jede Entscheidung verschiebt den Zusammenhalt und kostet PP oder BIP `unlock_decision_tooltip`
  - _Anmerkung:_ Die 14 Unionsrepubliken sind 1970 eigene Subjekt-Länder (Autonomie „Sowjetrepublik“). Zusammenhalt 0–100, Start 62.
- **Local Barons or Moscow's Men?** `COLDWAR_SOV_local_barons_or_moscows_men` · Kosten 3 · hist. · benötigt: the_union_of_republics
  - Gegenseitig exklusiv
- **Trust the Local Barons** `COLDWAR_SOV_trust_the_local_barons` · Kosten 5 · hist. · benötigt: local_barons_or_moscows_men · schließt aus: rotate_the_cadres
  - Zusammenhalt der Union +6 `COLDWAR_SOV_change_union_cohesion`
  - Der Parteistaat: Korruptionskosten +5 % `COLDWAR_SOV_party_state_modifier`
  - Union der Republiken: Stabilität +2 % `COLDWAR_SOV_union_modifier`
  - Politbüro der Republiken: Sitze nur noch auf Parteitagen änderbar (kein außerordentliches Plenum); Kompromat-Chance −10 %
  - _Anmerkung:_ Kunajew, Raschidow, Alijew, Schtscherbizki – Loyalität gegen Freiraum.
- **Rotate the Cadres** `COLDWAR_SOV_rotate_the_cadres` · Kosten 5 · benötigt: local_barons_or_moscows_men · schließt aus: trust_the_local_barons
  - Zusammenhalt der Union -3 `COLDWAR_SOV_change_union_cohesion`
  - Der Parteistaat: Korruptionskosten -5 %, Ideologische Abwehr (Cold War) +5 % `COLDWAR_SOV_party_state_modifier`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Politbüro der Republiken: Auf jedem Parteitag muss mindestens ein Sitz die Republik wechseln (Moskau wählt welchen)
  - _Anmerkung:_ Russische Zweite Sekretäre in allen Republiken – Kontrolle statt Vertrauen.
- **The Ukrainian Question** `COLDWAR_SOV_the_ukrainian_question` · Kosten 3 · hist. · benötigt: the_union_of_republics
  - Gegenseitig exklusiv
- **Shelest's Ukraine** `COLDWAR_SOV_shelests_ukraine` · Kosten 5 · benötigt: the_ukrainian_question · schließt aus: the_shcherbytsky_line
  - Zusammenhalt der Union +4 `COLDWAR_SOV_change_union_cohesion`
  - Union of Sovereign Republics +3 % Popularität (Outlook +3 %) `change_relative_party_popularity`
  - Union der Republiken: Nationalistische Drift +0.01 `COLDWAR_SOV_union_modifier`
  - _Anmerkung:_ Alt-Hist: Schelests „Unsere Sowjetukraine“ bleibt Linie.
- **The Shcherbytsky Line** `COLDWAR_SOV_the_shcherbytsky_line` · Kosten 5 · hist. · benötigt: the_ukrainian_question · schließt aus: shelests_ukraine
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
  - Union der Republiken: Ideologische Driftabwehr +5 % `COLDWAR_SOV_union_modifier`
  - Nomenklatura +5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Union of Sovereign Republics -2 % Popularität (Outlook -2 %) `change_relative_party_popularity`
  - _Anmerkung:_ 1972: Schelest gestürzt, Säuberung der ukrainischen Intelligenz.
- **The Baltic Showcase** `COLDWAR_SOV_the_baltic_question` · Kosten 3 · hist. · benötigt: the_union_of_republics
  - Gegenseitig exklusiv
- **The Soviet West** `COLDWAR_SOV_the_soviet_west` · Kosten 5 · benötigt: the_baltic_question · schließt aus: industrial_migration
  - Zusammenhalt der Union +3 `COLDWAR_SOV_change_union_cohesion`
  - Gosplan – Planwirtschaft: Konsumgüter -1 % `COLDWAR_SOV_gosplan_modifier`
  - Sozialistische Gemeinschaft: Handelsmeinung +3 % `COLDWAR_SOV_commonwealth_modifier`
  - _Anmerkung:_ Das Baltikum als Schaufenster: Konsum, Design, Tallinner Fernsehen aus Finnland.
- **Industrial Migration** `COLDWAR_SOV_industrial_migration` · Kosten 5 · hist. · benötigt: the_baltic_question · schließt aus: the_soviet_west
  - Gebäude: Zivilfabrik `one_random_industrial_complex`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Zusammenhalt der Union -2 `COLDWAR_SOV_change_union_cohesion`
  - Union der Republiken: Nationalistische Drift +0.01 `COLDWAR_SOV_union_modifier`
  - _Anmerkung:_ Russische Arbeiter für neue Kombinate in Riga und Tallinn – Wachstum gegen Ressentiment.
- **The Caucasus** `COLDWAR_SOV_the_caucasus` · Kosten 5 · hist. · benötigt: the_union_of_republics
  - Zusammenhalt der Union +1 `COLDWAR_SOV_change_union_cohesion`
- **Shevardnadze Cleans Up Tbilisi** `COLDWAR_SOV_shevardnadze_cleans_tbilisi` · Kosten 5 · hist. · benötigt: the_caucasus
  - Korruption −1 Stufe `decrease_corruption`
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
  - Nomenklatura -3 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - _Anmerkung:_ 1972: Eduard Schewardnadse ersetzt Mschawanadse.
- **Aliyev in Baku** `COLDWAR_SOV_aliyev_in_baku` · Kosten 5 · hist. · benötigt: the_caucasus
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
  - Gosplan – Planwirtschaft: Öl-Exporterlöse +2 % `COLDWAR_SOV_gosplan_modifier`
- **The Karabakh Petitions** `COLDWAR_SOV_the_karabakh_petitions` · Kosten 3 · benötigt: shevardnadze_cleans_tbilisi, aliyev_in_baku
  - Status quo (Zusammenhalt +2) oder Übergabe an Armenien (Zusammenhalt −4, Meinung ARM +25, AZE −25) – im Event
  - _Anmerkung:_ Die Frage, die 1988 die Union zu sprengen beginnt.
- **The Central Asian Barons** `COLDWAR_SOV_the_central_asian_barons` · Kosten 5 · hist. · benötigt: the_union_of_republics
  - Zusammenhalt der Union +2 `COLDWAR_SOV_change_union_cohesion`
- **The Cotton Affair** `COLDWAR_SOV_the_cotton_affair` · Kosten 7 · benötigt: the_central_asian_barons
  - Korruption −1 Stufe `decrease_corruption`
  - Zusammenhalt der Union -4 `COLDWAR_SOV_change_union_cohesion`
  - Der Parteistaat: Korruptionskosten -5 % `COLDWAR_SOV_party_state_modifier`
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - _Anmerkung:_ Die „Usbekische Affäre“ – Milliarden für Baumwolle, die es nicht gab.
- **The Language Question** `COLDWAR_SOV_the_language_question` · Kosten 3 · hist. · benötigt: trust_the_local_barons oder rotate_the_cadres
  - Gegenseitig exklusiv
- **Russian as the Language of Inter-Ethnic Communication** `COLDWAR_SOV_russian_as_lingua_franca` · Kosten 5 · hist. · benötigt: the_language_question · schließt aus: native_language_schools
  - Zusammenhalt der Union -2 `COLDWAR_SOV_change_union_cohesion`
  - Streitkräfte der UdSSR: Ausbildungszeit -3 % `COLDWAR_SOV_armed_forces_modifier`
  - Union der Republiken: Ideologische Driftabwehr +3 % `COLDWAR_SOV_union_modifier`
  - Politbüro-Beschluss (orthodox): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
  - _Anmerkung:_ Erlass von 1978.
- **Native Language Schools** `COLDWAR_SOV_native_language_schools` · Kosten 5 · benötigt: the_language_question · schließt aus: russian_as_lingua_franca
  - Zusammenhalt der Union +4 `COLDWAR_SOV_change_union_cohesion`
  - Streitkräfte der UdSSR: Ausbildungszeit +2 % `COLDWAR_SOV_armed_forces_modifier`
  - Politbüro-Beschluss (reformerisch): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
- **The Union Treaty Question** `COLDWAR_SOV_the_union_treaty_question` · Kosten 3 · benötigt: the_language_question · verfügbar: Zusammenhalt der Union < 40 ODER Datum ≥ 01.01.1985
  - Die Krise der Union – gegenseitig exklusiv
  - _Anmerkung:_ Krisenzweig: wird erst gebraucht, wenn die Union wackelt.
- **The Renewed Federation** `COLDWAR_SOV_the_renewed_federation` · Kosten 7 · benötigt: the_union_treaty_question · schließt aus: the_iron_union
  - Zusammenhalt der Union +15 `COLDWAR_SOV_change_union_cohesion`
  - Der Parteistaat: PP-Gewinn -5 % `COLDWAR_SOV_party_state_modifier`
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
  - Idee „Renewed Federation“: Stabilität +3 %, Autonomiezuwachs der Republiken +0.1, Nationalistische Drift -0.02 (`add_ideas`)
  - Politbüro-Beschluss (reformerisch): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
- **The Iron Union** `COLDWAR_SOV_the_iron_union` · Kosten 7 · benötigt: the_union_treaty_question · schließt aus: the_renewed_federation
  - Zusammenhalt der Union +8 `COLDWAR_SOV_change_union_cohesion`
  - Stabilität -5 % `add_stability`
  - Der Parteistaat: Polizeikosten +10 % `COLDWAR_SOV_party_state_modifier`
  - Politbüro-Balance +0.10 Richtung Orthodoxe `add_power_balance_value`
  - KGB +5 `COLDWAR_SOV_change_intelligence_community_opinion_exact` → `change_intelligence_community_opinion`
  - Politbüro-Beschluss (orthodox): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2
- **The Soviet People** `COLDWAR_SOV_the_soviet_people_realised` · Kosten 7 · benötigt: russian_as_lingua_franca oder native_language_schools, the_karabakh_petitions, the_cotton_affair oder the_central_asian_barons
  - Zusammenhalt der Union +8 `COLDWAR_SOV_change_union_cohesion`
  - Idee „The Soviet People“: Stabilität +2 %, Nationalistische Drift -0.02, Rekrutierbare Bevölkerung +2 % (`add_ideas`)

### Sowjetgesellschaft (15)

Alkohol, Wohnungen, Sport (Olympia 1980), Kultur zwischen Tauwetter und Zensur, Kirche, Frauen, die Sowjetmenschen.

- **The Soviet Way of Life** `COLDWAR_SOV_the_soviet_way_of_life` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Stabilität +2 % `add_stability`
  - PP +10 `add_political_power`
- **The Alcohol Problem** `COLDWAR_SOV_the_alcohol_problem` · Kosten 3 · hist. · benötigt: the_soviet_way_of_life
  - Gegenseitig exklusiv
- **The Vodka Monopoly** `COLDWAR_SOV_the_vodka_monopoly` · Kosten 3 · hist. · benötigt: the_alcohol_problem · schließt aus: the_1972_temperance_decree
  - Gosplan – Planwirtschaft: Steuereinnahmen +4 %, Gesundheitskosten +5 % `COLDWAR_SOV_gosplan_modifier`
  - Gosplan – Planwirtschaft: Produktivitätswachstum -1 % `COLDWAR_SOV_gosplan_modifier`
  - _Anmerkung:_ Ein Viertel der Einzelhandelsumsätze.
- **The 1972 Temperance Decree** `COLDWAR_SOV_the_1972_temperance_decree` · Kosten 5 · benötigt: the_alcohol_problem · schließt aus: the_vodka_monopoly
  - Gosplan – Planwirtschaft: Steuereinnahmen -3 %, Produktivitätswachstum +2 %, Gesundheitskosten -3 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität -2 % `add_stability`
- **The Sporting Superpower** `COLDWAR_SOV_the_sporting_superpower` · Kosten 5 · hist. · benötigt: the_soviet_way_of_life
  - Stabilität +2 % `add_stability`
  - Der Parteistaat: PP-Gewinn +2 % `COLDWAR_SOV_party_state_modifier`
- **The Moscow Olympics** `COLDWAR_SOV_the_moscow_olympics` · Kosten 7 · hist. · benötigt: the_sporting_superpower · verfügbar: Datum ≥ 01.01.1979
  - Stabilität +5 % `add_stability`
  - Kosten 0.8 % BIP `COLDWAR_SOV_pay_gdp_share`
  - Gebäude: Infrastruktur `one_random_infrastructure`
  - Event: Olympische Sommerspiele Moskau 1980 – Mischka, Boykott oder Weltfest
  - _Anmerkung:_ Vergeben 1974. Boykott durch westliche Spieler ist ein Event mit Wahl.
- **Between Thaw and Frost** `COLDWAR_SOV_culture_question` · Kosten 3 · hist. · benötigt: the_soviet_way_of_life
  - Gegenseitig exklusiv
- **Glavlit Holds the Line** `COLDWAR_SOV_glavlit_holds_the_line` · Kosten 5 · hist. · benötigt: culture_question · schließt aus: cultural_detente
  - Der Parteistaat: Stabilität +2 %, Forschung -1 % `COLDWAR_SOV_party_state_modifier`
  - Politbüro-Balance +0.05 Richtung Orthodoxe `add_power_balance_value`
- **Cultural Detente** `COLDWAR_SOV_cultural_detente` · Kosten 5 · benötigt: culture_question · schließt aus: glavlit_holds_the_line
  - Der Parteistaat: Forschung +1 % `COLDWAR_SOV_party_state_modifier`
  - Der Parteistaat: Demokratische Drift +0.01 `COLDWAR_SOV_party_state_modifier`
  - Stabilität +1 % `add_stability`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - _Anmerkung:_ Taganka-Theater, Wyssozki, Tarkowski – geduldet statt verboten.
- **The Church Question** `COLDWAR_SOV_the_church_question` · Kosten 3 · hist. · benötigt: the_soviet_way_of_life
  - Gegenseitig exklusiv
- **Scientific Atheism** `COLDWAR_SOV_scientific_atheism` · Kosten 5 · hist. · benötigt: the_church_question · schließt aus: accord_with_the_patriarchate
  - Der Parteistaat: Ideologische Driftabwehr +3 % `COLDWAR_SOV_party_state_modifier`
  - Live Not by Lies -2 % Popularität (Outlook -2 %) `change_relative_party_popularity`
  - House of Romanov -1 % Popularität (Outlook -1 %) `change_relative_party_popularity`
- **Accord with the Patriarchate** `COLDWAR_SOV_accord_with_the_patriarchate` · Kosten 5 · benötigt: the_church_question · schließt aus: scientific_atheism
  - Fügt die Fraktion „Moskauer Patriarchat“ hinzu (`the_clergy`, Meinung 45) `add_ideas`
  - Stabilität +3 % `add_stability`
  - Live Not by Lies +2 % Popularität (Outlook +2 %) `change_relative_party_popularity`
  - House of Romanov +1 % Popularität (Outlook +1 %) `change_relative_party_popularity`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
- **The Double Burden** `COLDWAR_SOV_the_double_burden` · Kosten 5 · benötigt: the_soviet_way_of_life
  - Gosplan – Planwirtschaft: Arbeitskräfte +2 %, Sozialkosten +3 % `COLDWAR_SOV_gosplan_modifier`
  - Stabilität +1 % `add_stability`
  - _Anmerkung:_ Frauen: 51 % der Arbeitskräfte und der ganze Haushalt.
- **The Demographic Gap** `COLDWAR_SOV_the_demographic_gap` · Kosten 5 · benötigt: the_double_burden
  - Gosplan – Planwirtschaft: Sozialkosten +3 % `COLDWAR_SOV_gosplan_modifier`
  - Der Parteistaat: Bevölkerungswachstum +0.05 `COLDWAR_SOV_party_state_modifier`
  - Zusammenhalt der Union -1 `COLDWAR_SOV_change_union_cohesion`
  - _Anmerkung:_ Geburtenraten: Russland 1,9, Usbekistan 5,6 – die Union verschiebt sich nach Süden.
- **The Developed Socialist Society** `COLDWAR_SOV_the_developed_socialist_society` · Kosten 7 · benötigt: the_moscow_olympics oder the_demographic_gap, glavlit_holds_the_line oder cultural_detente
  - Idee „The Socialist Way of Life“: Stabilität +3 %, Kriegsunterstützung +2 % (`add_ideas`)

### Entspannung & der Westen (16)

Friedensprogramm des XXIV. Parteitags: Moskauer Vertrag mit der BRD, SALT und ABM, Helsinki (KSZE), Handel mit dem Westen, Nahrungsmittel gegen Entspannung.

- **Peaceful Coexistence** `COLDWAR_SOV_peaceful_coexistence` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - PP +15 `add_political_power`
  - Cold-War-Spannung -1 `mdcw_cw_add_tension`
- **The Moscow Treaty** `COLDWAR_SOV_the_moscow_treaty` · Kosten 5 · hist. · benötigt: peaceful_coexistence
  - Angebot an GER (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Gewaltverzicht und Anerkennung der Nachkriegsgrenzen. Bei Annahme: Spannung −2, Meinung +20 beidseitig, verbessertes Handelsabkommen; „The Shadow of Prague“ verliert die Handelsstrafe `COLDWAR_SOV_offer_moscow_treaty`
  - _Anmerkung:_ 12.08.1970, Brandts Ostpolitik. Nur als Angebot.
- **The Peace Programme** `COLDWAR_SOV_the_peace_programme` · Kosten 5 · hist. · benötigt: peaceful_coexistence · verfügbar: `COLDWAR_SOV_the_24th_party_congress` erledigt
  - Cold-War-Spannung -1 `mdcw_cw_add_tension`
  - Sozialistische Gemeinschaft: Handelsmeinung +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Meinung USA +5 `add_opinion_modifier`
- **The Quadripartite Agreement** `COLDWAR_SOV_the_berlin_agreement` · Kosten 5 · hist. · benötigt: the_moscow_treaty
  - Angebot an USA, ENG, FRA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Viermächteabkommen über Berlin (1971). Bei Annahme aller: Spannung −2, DDR/BRD-Transit gesichert `COLDWAR_SOV_offer_berlin_agreement`
- **SALT Negotiations** `COLDWAR_SOV_salt_negotiations` · Kosten 3 · hist. · benötigt: the_peace_programme
  - Rüstungskontrolle oder Überlegenheit – gegenseitig exklusiv
- **SALT I and the ABM Treaty** `COLDWAR_SOV_salt_i_and_the_abm_treaty` · Kosten 5 · hist. · benötigt: salt_negotiations · schließt aus: superiority_not_parity
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): SALT I und ABM-Vertrag. Bei Annahme: beide erhalten „Arms Limitation“ (Kosten Verteidigungshaushalt −10 %, Kriegsunterstützung −2 %), Spannung −3; „The Burden of Parity“ wird abgeschwächt `COLDWAR_SOV_offer_salt_i`
  - Armee & Generalstab -5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - _Anmerkung:_ Moskau, Mai 1972.
- **Superiority, Not Parity** `COLDWAR_SOV_superiority_not_parity` · Kosten 5 · benötigt: salt_negotiations · schließt aus: salt_i_and_the_abm_treaty
  - Cold-War-Spannung +3 `mdcw_cw_add_tension`
  - Armee & Generalstab +10 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Rüstungskomplex (VPK) +10 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
  - Idee „The Arms Race“: Bau Rüstungsfabriken +10 %, Konsumgüter +3 %, Kriegsunterstützung +3 % (`add_ideas`)
  - Politbüro-Balance +0.10 Richtung Orthodoxe `add_power_balance_value`
- **The Moscow Summit** `COLDWAR_SOV_the_moscow_summit` · Kosten 5 · hist. · benötigt: salt_i_and_the_abm_treaty
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Gipfel in Moskau (Mai 1972). Bei Annahme: Spannung −2, „Basic Principles of Relations“, Meinung +15 `COLDWAR_SOV_offer_moscow_summit`
  - Stabilität +2 % `add_stability`
- **Western Credits and Technology** `COLDWAR_SOV_trade_and_credits` · Kosten 5 · hist. · benötigt: the_peace_programme
  - Kredit: Treasury +1 % BIP, Schulden +1 % BIP `COLDWAR_SOV_receive_gdp_share` `modify_debt_effect`
  - Forschungsbonus CAT_industry, CAT_production_lines +50 % ×1 `add_tech_bonus`
  - Sozialistische Gemeinschaft: Handelsmeinung +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
- **The Paris Axis** `COLDWAR_SOV_the_paris_axis` · Kosten 5 · hist. · benötigt: the_peace_programme
  - Angebot an FRA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Französisch-sowjetische Zusammenarbeit (Pompidou 1970/71). Bei Annahme: Forschungsbonus Elektronik für beide, Meinung +20 `COLDWAR_SOV_offer_paris_axis`
- **The Vladivostok Accords** `COLDWAR_SOV_vladivostok_accords` · Kosten 5 · hist. · benötigt: the_moscow_summit oder superiority_not_parity · verfügbar: Datum ≥ 01.11.1974
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Rahmen für SALT II. Bei Annahme: Spannung −1, Meinung +10 `COLDWAR_SOV_offer_vladivostok`
- **The Helsinki Conference** `COLDWAR_SOV_the_helsinki_conference` · Kosten 7 · hist. · benötigt: the_berlin_agreement, vladivostok_accords oder the_paris_axis · verfügbar: Datum ≥ 01.07.1975
  - Angebot an USA, GER, FRA, ENG (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Schlussakte der KSZE. Bei Annahme: Unverletzlichkeit der Grenzen; Spannung −3 `COLDWAR_SOV_offer_helsinki`
  - Entfernt „The Shadow of Prague“ `remove_ideas`
  - Idee „Basket Three“: Handelsmeinung +10 %, Demokratische Drift +0.01 (`add_ideas`)
  - Event: Die Moskauer Helsinki-Gruppe (1976) beruft sich auf Korb III
  - _Anmerkung:_ Die UdSSR bekommt ihre Grenzen anerkannt – und die Dissidenten ein Dokument.
- **SALT II** `COLDWAR_SOV_salt_ii` · Kosten 5 · hist. · benötigt: the_helsinki_conference · verfügbar: Datum ≥ 01.06.1979
  - Angebot an USA (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): SALT II in Wien. Bei Annahme: Spannung −2, Kosten Verteidigungshaushalt −5 % für beide `COLDWAR_SOV_offer_salt_ii`
- **The End of Detente?** `COLDWAR_SOV_the_end_of_detente` · Kosten 3 · benötigt: salt_ii oder superiority_not_parity · verfügbar: Cold-War-Spannung ≥ 60 ODER Datum ≥ 01.01.1980
  - Gegenseitig exklusiv: retten oder abschreiben
- **Save Detente** `COLDWAR_SOV_save_detente` · Kosten 5 · benötigt: the_end_of_detente · schließt aus: the_second_cold_war
  - Cold-War-Spannung -2 `mdcw_cw_add_tension`
  - PP -50 `add_political_power`
  - Meinung USA +10 `add_opinion_modifier`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
- **The Second Cold War** `COLDWAR_SOV_the_second_cold_war` · Kosten 5 · benötigt: the_end_of_detente · schließt aus: save_detente
  - Cold-War-Spannung +3 `mdcw_cw_add_tension`
  - Kriegsunterstützung +5 % `add_war_support`
  - Streitkräfte der UdSSR: Ausrüstungskosten -2 % `COLDWAR_SOV_armed_forces_modifier`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`

### Die chinesische Frage (16)

Nach Damanski und Tielieketi (1969): Grenzgespräche, Aufrüstung im Fernen Osten, Präventivschlag-Debatte, Eindämmung oder Versöhnung mit Peking.

- **The Chinese Question** `COLDWAR_SOV_the_chinese_question` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - PP +15 `add_political_power`
  - Damanski (März 1969) und Tielieketi (August 1969) liegen kein Jahr zurück
- **The Beijing Border Talks** `COLDWAR_SOV_the_beijing_border_talks` · Kosten 5 · hist. · benötigt: the_chinese_question
  - Angebot an CHI (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Grenzgespräche (seit Oktober 1969). Bei Annahme: Spannung −1, „The Ussuri Frontier“ verliert die Stabilitätsstrafe `COLDWAR_SOV_offer_border_talks`
- **Three Roads to Beijing** `COLDWAR_SOV_three_roads_to_beijing` · Kosten 3 · hist. · benötigt: the_beijing_border_talks
  - Eindämmen, zuschlagen oder versöhnen – gegenseitig exklusiv
- **Contain China** `COLDWAR_SOV_contain_china` · Kosten 5 · hist. · benötigt: three_roads_to_beijing · schließt aus: the_surgical_strike_option, reconcile_with_beijing
  - Streitkräfte der UdSSR: Verteidigung auf Kerngebiet +3 % `COLDWAR_SOV_armed_forces_modifier`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
- **The Trans-Baikal Buildup** `COLDWAR_SOV_the_trans_baikal_buildup` · Kosten 7 · hist. · benötigt: contain_china
  - Gebäude: Luftwaffenbasis `one_air_base`
  - Gebäude: Rüstungsfabrik `one_random_arms_factory`, Kosten 0.8 % BIP statt MD-Pauschale (`skip_payment`)
  - Mannstärke +20.000 `add_manpower`
  - ersetzt „The Ussuri Frontier“: Idee „The Eastern Fortress“: Kriegsunterstützung +5 %, Verteidigung auf Kerngebiet +5 %, Personalkosten Heer +10 % (`swap_ideas`)
  - _Anmerkung:_ 1969–1972 wächst die Fernostgruppierung von 15 auf über 40 Divisionen.
- **The Amur Fortified Districts** `COLDWAR_SOV_the_amur_fortified_districts` · Kosten 5 · hist. · benötigt: the_trans_baikal_buildup
  - Streitkräfte der UdSSR: Verteidigung auf Kerngebiet +5 % `COLDWAR_SOV_armed_forces_modifier`
  - Bunker in zwei Grenzstaaten `add_building_construction` (bunker)
- **The Mongolian Shield** `COLDWAR_SOV_the_mongolian_shield` · Kosten 5 · hist. · benötigt: the_trans_baikal_buildup
  - Angebot an MON (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Stationierung der 39. Armee in der Mongolei. Bei Annahme: MON erhält Hilfe 0,2 % BIP/Jahr und Verteidigung +5 % `COLDWAR_SOV_offer_mongolian_garrison`
- **Asian Collective Security** `COLDWAR_SOV_asian_collective_security` · Kosten 5 · hist. · benötigt: contain_china
  - Einfluss +3 % in RAJ, VIE, MON, AFG `change_influence_percentage`
  - Meinung RAJ +10 `add_opinion_modifier`
  - _Anmerkung:_ Breschnews Vorschlag von 1969 – gegen China gerichtet.
- **Treaty with India** `COLDWAR_SOV_treaty_with_india` · Kosten 5 · hist. · benötigt: asian_collective_security
  - Angebot an RAJ (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Vertrag über Frieden, Freundschaft und Zusammenarbeit (August 1971). Bei Annahme: Rüstungshilfe, Meinung +25, Handelsabkommen `COLDWAR_SOV_offer_india_treaty`
- **Vietnam against China** `COLDWAR_SOV_vietnam_against_china` · Kosten 5 · hist. · benötigt: asian_collective_security · verfügbar: Datum ≥ 01.01.1978
  - Angebot an VIE (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Freundschaftsvertrag (November 1978). Bei Annahme: Cam-Ranh-Rechte und gemeinsame Front gegen China `COLDWAR_SOV_offer_vietnam_treaty`
- **The Surgical Strike Option** `COLDWAR_SOV_the_surgical_strike_option` · Kosten 5 · benötigt: three_roads_to_beijing · schließt aus: contain_china, reconcile_with_beijing · nur Spieler (KI nie)
  - Cold-War-Spannung +5 `mdcw_cw_add_tension`
  - Armee & Generalstab +5 `COLDWAR_SOV_change_the_military_opinion_exact` → `change_the_military_opinion`
  - Nomenklatura -5 `COLDWAR_SOV_change_communist_cadres_opinion_exact` → `change_communist_cadres_opinion`
  - Alt-Hist, nur Spieler. Die im Herbst 1969 diskutierte Option eines Schlags gegen Lop Nor
- **Plan Lop Nur** `COLDWAR_SOV_plan_lop_nur` · Kosten 7 · benötigt: the_surgical_strike_option · nur Spieler (KI nie)
  - Streitkräfte der UdSSR: Planungsgeschwindigkeit +0.1 `COLDWAR_SOV_armed_forces_modifier`
  - Forschungsbonus CAT_ballistic_missiles +50 % ×1 `add_tech_bonus`
  - Kriegsziel gegen CHI (`create_wargoal`, Typ `topple_government`); Erklärung bleibt Entscheidung des Spielers
- **Strike at Dawn** `COLDWAR_SOV_strike_at_dawn` · Kosten 3 · benötigt: plan_lop_nur · verfügbar: Im Krieg mit CHI · nur Spieler (KI nie)
  - Idee „Strike at Dawn“: Angriff (Heer) +5 %, Durchbruch +5 % (180 Tage `add_timed_idea`)
  - Cold-War-Spannung +10 `mdcw_cw_add_tension`
  - Event: Weltreaktion: Washington, Delhi und Tokio verurteilen den Schlag
- **Reconcile with Beijing** `COLDWAR_SOV_reconcile_with_beijing` · Kosten 5 · benötigt: three_roads_to_beijing · schließt aus: contain_china, the_surgical_strike_option · nur Spieler (KI nie)
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - Angebot an CHI (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Ideologischer Waffenstillstand. Bei Annahme: „The Ussuri Frontier“ entfällt, Spannung −2, Meinung +30; Peking kann ins sowjetische Lager zurück (Cold-War-Blockwechsel bleibt Pekings Entscheidung) `COLDWAR_SOV_offer_sino_soviet_truce`
  - _Anmerkung:_ Alt-Hist: Die Kosygin-Zhou-Begegnung vom September 1969 wird zum Wendepunkt.
- **Settle Damansky** `COLDWAR_SOV_settle_damansky` · Kosten 5 · benötigt: reconcile_with_beijing oder the_beijing_border_talks
  - Angebot an CHI (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Damanski/Zhenbao an China, Flussgrenze in der Fahrrinne. Bei Annahme: „The Ussuri Frontier“ wird entfernt, Spannung −1 `COLDWAR_SOV_offer_damansky_settlement`
  - _Anmerkung:_ Historisch erst 1991 geregelt.
- **The Eastern Front Secured** `COLDWAR_SOV_the_eastern_front_secured` · Kosten 7 · benötigt: the_amur_fortified_districts oder settle_damansky oder strike_at_dawn
  - Stabilität +3 % `add_stability`
  - Streitkräfte der UdSSR: Personalkosten Heer -5 % `COLDWAR_SOV_armed_forces_modifier`
  - Mit „BAM Open to Traffic“: zusätzlich Versorgung −2 %

### Warschauer Pakt & RGW (19)

Breschnew-Doktrin, Komplexprogramm des RGW (1971), billiges Öl, Polen 1970, Rumäniens Eigenweg, gemeinsame Manöver – alles mit Zustimmung der Partner.

- **The Socialist Commonwealth** `COLDWAR_SOV_the_socialist_commonwealth` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Sozialistische Gemeinschaft: Meinungsgewinn gleiche Ideologie +5 % `COLDWAR_SOV_commonwealth_modifier`
- **Limited Sovereignty?** `COLDWAR_SOV_the_doctrine_question` · Kosten 3 · hist. · benötigt: the_socialist_commonwealth
  - Gegenseitig exklusiv
- **The Brezhnev Doctrine** `COLDWAR_SOV_the_brezhnev_doctrine` · Kosten 5 · hist. · benötigt: the_doctrine_question · schließt aus: let_them_go_their_way
  - Sozialistische Gemeinschaft: Auslandseinfluss +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Der Parteistaat: Ideologische Abwehr (Cold War) +5 % `COLDWAR_SOV_party_state_modifier`
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
  - Idee „The Brezhnev Doctrine“: Ideologische Driftabwehr +5 %, Handelsmeinung -5 % (`add_ideas`)
  - _Anmerkung:_ „Die Souveränität jedes sozialistischen Landes ist begrenzt“ – Prag 1968 als Regel.
- **Let Them Go Their Way** `COLDWAR_SOV_let_them_go_their_way` · Kosten 5 · benötigt: the_doctrine_question · schließt aus: the_brezhnev_doctrine · nur Spieler (KI nie)
  - Politbüro-Balance -0.10 Richtung Reformer `add_power_balance_value`
  - Cold-War-Spannung -2 `mdcw_cw_add_tension`
  - Entfernt „The Shadow of Prague“ `remove_ideas`
  - Zusammenhalt der Union -3 `COLDWAR_SOV_change_union_cohesion`
  - Sozialistische Gemeinschaft: Steuereinnahmen +3 % `COLDWAR_SOV_commonwealth_modifier`
  - Meinung ROM +15 `add_opinion_modifier`
  - _Anmerkung:_ Alt-Hist: eine „Sinatra-Doktrin“ zwanzig Jahre früher.
- **The Comprehensive Programme** `COLDWAR_SOV_the_comprehensive_programme` · Kosten 5 · hist. · benötigt: the_socialist_commonwealth
  - Sozialistische Gemeinschaft: Forschungsteilung +5 %, Meinungsgewinn gleiche Ideologie +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Cold War: Decision „Comecon Integration Programme“ kostet für uns 25 PP weniger (`COLDWAR_SOV_comprehensive_programme` Flag)
  - Flag `COLDWAR_SOV_comprehensive_programme`
  - _Anmerkung:_ RGW-Gipfel Bukarest, Juli 1971.
- **Fraternal Oil** `COLDWAR_SOV_the_oil_price_question` · Kosten 3 · hist. · benötigt: the_comprehensive_programme
  - Gegenseitig exklusiv
- **Subsidised Oil** `COLDWAR_SOV_subsidised_oil` · Kosten 5 · hist. · benötigt: the_oil_price_question · schließt aus: world_market_prices
  - Sozialistische Gemeinschaft: Öl-Exporterlöse -5 %, Meinungsgewinn gleiche Ideologie +10 % `COLDWAR_SOV_commonwealth_modifier`
  - Meinung POL +10 `add_opinion_modifier`
  - Meinung DDR +10 `add_opinion_modifier`
- **World Market Prices** `COLDWAR_SOV_world_market_prices` · Kosten 5 · benötigt: the_oil_price_question · schließt aus: subsidised_oil
  - Sozialistische Gemeinschaft: Öl-Exporterlöse +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Einnahme +0.3 % BIP `COLDWAR_SOV_receive_gdp_share`
  - Meinung −10 bei allen RGW-Partnern (DDR, POL, CZE, HUN, ROM, BUL) `add_opinion_modifier`
  - _Anmerkung:_ Der „Bukarester Mechanismus“ von 1975 mit gleitenden Durchschnittspreisen – konsequent zu Ende gedacht.
- **The Soyuz Pipeline** `COLDWAR_SOV_the_soyuz_pipeline` · Kosten 7 · hist. · benötigt: subsidised_oil oder world_market_prices · verfügbar: Datum ≥ 01.01.1975
  - Angebot an DDR, POL, CZE, HUN, ROM, BUL (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Gemeinsamer Bau der Orenburg-Gasleitung. Bei Annahme: Partner zahlt 0,2 % BIP und erhält Energie +5 %; UdSSR erhält Bau +3 % `COLDWAR_SOV_offer_soyuz_pipeline`
- **Shield and Brotherhood** `COLDWAR_SOV_shield_and_brotherhood` · Kosten 5 · hist. · benötigt: the_brezhnev_doctrine oder let_them_go_their_way
  - Angebot an DDR, POL, CZE, HUN, ROM, BUL (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Gemeinsame Manöver „Schild“/„Waffenbrüderschaft“. Bei Annahme: beide +25 Heereserfahrung `COLDWAR_SOV_offer_joint_exercises`
  - Heereserfahrung +25 `army_experience`
- **Kulikov's Unified Command** `COLDWAR_SOV_kulikovs_unified_command` · Kosten 5 · hist. · benötigt: shield_and_brotherhood · verfügbar: Datum ≥ 01.01.1977
  - Sozialistische Gemeinschaft: Forschungsteilung +5 % `COLDWAR_SOV_commonwealth_modifier`
  - Streitkräfte der UdSSR: Planungsgeschwindigkeit +0.05 `COLDWAR_SOV_armed_forces_modifier`
- **The Polish Question** `COLDWAR_SOV_the_polish_question` · Kosten 3 · hist. · benötigt: the_socialist_commonwealth
  - Danzig, Dezember 1970 – Gomułka stürzt, Gierek übernimmt. Gegenseitig exklusiv
- **Credits for Gierek** `COLDWAR_SOV_credits_for_gierek` · Kosten 5 · hist. · benötigt: the_polish_question · schließt aus: discipline_warsaw
  - Angebot an POL (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Rohstoffkredite und Getreide. Bei Annahme: POL erhält 0,4 % unseres BIP, Stabilität +5 %; wir zahlen `COLDWAR_SOV_offer_credits_for_poland`
  - Kosten 0.4 % BIP `COLDWAR_SOV_pay_gdp_share`
- **Discipline Warsaw** `COLDWAR_SOV_discipline_warsaw` · Kosten 5 · benötigt: the_polish_question · schließt aus: credits_for_gierek
  - Meinung POL -15 `add_opinion_modifier`
  - Der Parteistaat: Ideologische Abwehr (Cold War) +5 % `COLDWAR_SOV_party_state_modifier`
  - Event: Die polnische Führung wird nach Moskau bestellt – Antwort liegt bei Polen
- **Romania's Maverick Course** `COLDWAR_SOV_romanias_maverick_course` · Kosten 3 · hist. · benötigt: the_socialist_commonwealth
  - Gegenseitig exklusiv
- **Tolerate Bucharest** `COLDWAR_SOV_tolerate_bucharest` · Kosten 3 · hist. · benötigt: romanias_maverick_course · schließt aus: isolate_bucharest
  - Meinung ROM +5 `add_opinion_modifier`
  - PP +25 `add_political_power`
- **Isolate Bucharest** `COLDWAR_SOV_isolate_bucharest` · Kosten 5 · benötigt: romanias_maverick_course · schließt aus: tolerate_bucharest
  - Meinung ROM -20 `add_opinion_modifier`
  - Sozialistische Gemeinschaft: Auslandseinfluss +3 % `COLDWAR_SOV_commonwealth_modifier`
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
- **Interkosmos** `COLDWAR_SOV_interkosmos` · Kosten 5 · hist. · benötigt: the_comprehensive_programme · verfügbar: Datum ≥ 01.01.1977
  - Angebot an DDR, POL, CZE, HUN, ROM, BUL, CUB, MON, VIE (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Ein Kosmonaut des Partners fliegt mit Sojus. Bei Annahme: Partner +5 % Stabilität (1 Jahr), Meinung +20 `COLDWAR_SOV_offer_interkosmos`
  - Raumfahrtprogramm-Fortschritt `add_space_program_progress`
- **The Commonwealth of Socialist Nations** `COLDWAR_SOV_the_commonwealth_of_socialist_nations` · Kosten 7 · benötigt: kulikovs_unified_command, the_soyuz_pipeline oder interkosmos
  - Idee „The Socialist Commonwealth“: Meinungsgewinn gleiche Ideologie +10 %, Forschungsteilung +5 % (`add_ideas`)
  - Sozialistische Gemeinschaft: Hilfsprogramm-Kapazität (Cold War) +1 `COLDWAR_SOV_commonwealth_modifier`

### Dritte Welt & Internationalismus (19)

Ägypten (Operation Kavkaz), Vietnam, Kuba, Indien (Vertrag 1971), Syrien und Irak, später Angola, Äthiopien und Afghanistan – Hilfe kostet.

- **Proletarian Internationalism** `COLDWAR_SOV_proletarian_internationalism` · Kosten 3 · hist. · benötigt: – · verfügbar: `COLDWAR_SOV_the_collective_leadership` erledigt
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +5 % `COLDWAR_SOV_commonwealth_modifier`
  - PP +10 `add_political_power`
- **Operation Kavkaz** `COLDWAR_SOV_operation_kavkaz` · Kosten 5 · hist. · benötigt: proletarian_internationalism · verfügbar: Datum < 01.01.1972; EGY existiert
  - Angebot an EGY (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Eine Flugabwehrdivision und MiG-21-Staffeln am Suezkanal. Bei Annahme: EGY Luftverteidigung, wir +25 Lufterfahrung, Spannung +1 `COLDWAR_SOV_offer_operation_kavkaz`
  - Wird automatisch erfüllt, wenn Ägypten uns vorher um Operation Kavkaz gebeten und wir angenommen haben (EGY-Baum)
  - _Anmerkung:_ Januar–März 1970: 10.000 sowjetische Soldaten in Ägypten.
- **The Treaty with Egypt** `COLDWAR_SOV_the_treaty_with_egypt` · Kosten 5 · hist. · benötigt: operation_kavkaz
  - Angebot an EGY (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Freundschaftsvertrag (Mai 1971). Bei Annahme: Meinung +25, Einfluss +5 % `COLDWAR_SOV_offer_egypt_treaty`
- **Lifeline to Hanoi** `COLDWAR_SOV_lifeline_to_hanoi` · Kosten 5 · hist. · benötigt: proletarian_internationalism
  - Angebot an VIE (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Luftabwehrraketen, MiGs und Reis. Bei Annahme: VIE erhält Ausrüstung und Verteidigung +5 %; wir zahlen 0,4 % BIP `COLDWAR_SOV_offer_arms_for_hanoi`
  - Cold-War-Spannung +1 `mdcw_cw_add_tension`
- **The Island of Freedom** `COLDWAR_SOV_the_island_of_freedom` · Kosten 5 · hist. · benötigt: proletarian_internationalism
  - Angebot an CUB (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Öl gegen Zucker zu Vorzugspreisen. Bei Annahme: CUB Stabilität +5 %, Wirtschaft +; wir Sozialistische Gemeinschaft: Steuern −1 % `COLDWAR_SOV_offer_sugar_for_oil`
  - Sozialistische Gemeinschaft: Steuereinnahmen -1 % `COLDWAR_SOV_commonwealth_modifier`
- **Syria and Iraq** `COLDWAR_SOV_syria_and_iraq` · Kosten 5 · hist. · benötigt: the_treaty_with_egypt
  - Angebot an IRQ (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Freundschaftsvertrag (April 1972). Bei Annahme: Meinung +20, Ölkooperation `COLDWAR_SOV_offer_iraq_treaty`
  - Angebot an SYR (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Rüstungspaket und Berater. Bei Annahme: SYR +5 % Verteidigung, Meinung +20 `COLDWAR_SOV_offer_syria_arms`
- **Patrice Lumumba University** `COLDWAR_SOV_patrice_lumumba_university` · Kosten 5 · hist. · benötigt: proletarian_internationalism
  - Sozialistische Gemeinschaft: Unterstützungskampagnen (Cold War) +10 % `COLDWAR_SOV_commonwealth_modifier`
  - Gosplan – Planwirtschaft: Bildungskosten +2 % `COLDWAR_SOV_gosplan_modifier`
- **Military Advisers** `COLDWAR_SOV_military_advisers` · Kosten 5 · hist. · benötigt: patrice_lumumba_university
  - Sozialistische Gemeinschaft: Kosten Militärprogramme (Cold War) -15 %, Freiwilligen-Kontingent +1 `COLDWAR_SOV_commonwealth_modifier`
- **Aid or Arms?** `COLDWAR_SOV_the_question_of_aid` · Kosten 3 · hist. · benötigt: military_advisers
  - Gegenseitig exklusiv
- **Economic Aid Programmes** `COLDWAR_SOV_economic_aid_programmes` · Kosten 5 · benötigt: the_question_of_aid · schließt aus: arms_on_credit
  - Sozialistische Gemeinschaft: Hilfsprogramm-Kapazität (Cold War) +2, Steuereinnahmen -2 % `COLDWAR_SOV_commonwealth_modifier`
  - Sozialistische Gemeinschaft: Auslandseinfluss +5 % `COLDWAR_SOV_commonwealth_modifier`
- **Arms on Credit** `COLDWAR_SOV_arms_on_credit` · Kosten 5 · hist. · benötigt: the_question_of_aid · schließt aus: economic_aid_programmes
  - Streitkräfte der UdSSR: Erlöse Waffenmarkt +10 % `COLDWAR_SOV_armed_forces_modifier`
  - Sozialistische Gemeinschaft: Auslandseinfluss +3 % `COLDWAR_SOV_commonwealth_modifier`
  - Rüstungskomplex (VPK) +5 `COLDWAR_SOV_change_defense_industry_opinion_exact` → `change_defense_industry_opinion`
- **The Cuban Bridge to Angola** `COLDWAR_SOV_the_cuban_bridge` · Kosten 5 · hist. · benötigt: the_island_of_freedom, military_advisers · verfügbar: Datum ≥ 01.06.1975
  - Angebot an AGL (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Unterstützung der MPLA mit Waffen und kubanischen Truppen. Bei Annahme: AGL +10 % Angriff (2 Jahre) `COLDWAR_SOV_offer_angola_support`
  - Cold-War-Spannung +2 `mdcw_cw_add_tension`
- **The Horn of Africa** `COLDWAR_SOV_the_horn_of_africa` · Kosten 3 · hist. · benötigt: the_cuban_bridge · verfügbar: Datum ≥ 01.01.1977
  - Ogaden – gegenseitig exklusiv
- **Back the Derg** `COLDWAR_SOV_back_ethiopia` · Kosten 5 · hist. · benötigt: the_horn_of_africa · schließt aus: back_somalia
  - Angebot an ETH (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Luftbrücke und kubanische Brigaden (1977/78). Bei Annahme: ETH Angriff +10 % `COLDWAR_SOV_offer_ethiopia_airlift`
  - Meinung SOM -30 `add_opinion_modifier`
- **Back Siad Barre** `COLDWAR_SOV_back_somalia` · Kosten 5 · benötigt: the_horn_of_africa · schließt aus: back_ethiopia
  - Angebot an SOM (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Waffen und Berater. Bei Annahme: SOM Angriff +10 %, Berbera bleibt sowjetisch `COLDWAR_SOV_offer_somalia_support`
  - Meinung ETH -30 `add_opinion_modifier`
- **The Afghan Question** `COLDWAR_SOV_the_afghan_question` · Kosten 3 · hist. · benötigt: syria_and_iraq oder military_advisers · verfügbar: Datum ≥ 01.04.1978
  - Saur-Revolution und Herat-Aufstand – gegenseitig exklusiv
- **The Limited Contingent** `COLDWAR_SOV_the_limited_contingent` · Kosten 5 · hist. · benötigt: the_afghan_question · schließt aus: no_soviet_soldier
  - Angebot an AFG (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): Die afghanische Regierung bittet um Truppen (Dezember 1979). Bei Annahme: Expeditionsstreitkräfte, wir erhalten „The Afghan Burden“ (Stabilität −3 %, Kriegsunterstützung −5 %, 0,3 % BIP/Monat) solange der Krieg läuft `COLDWAR_SOV_offer_limited_contingent`
  - Cold-War-Spannung +4 `mdcw_cw_add_tension`
  - _Anmerkung:_ Kein automatischer Einmarsch: Afghanistan muss annehmen (Spieler oder KI).
- **Not a Single Soviet Soldier** `COLDWAR_SOV_no_soviet_soldier` · Kosten 3 · benötigt: the_afghan_question · schließt aus: the_limited_contingent
  - Stabilität +2 % `add_stability`
  - Meinung AFG -10 `add_opinion_modifier`
  - Politbüro-Balance -0.05 Richtung Reformer `add_power_balance_value`
  - _Anmerkung:_ Kossygin im März 1979: „Wir können das afghanische Volk nicht ersetzen.“
- **Vanguard of World Revolution** `COLDWAR_SOV_vanguard_of_world_revolution` · Kosten 7 · benötigt: back_ethiopia oder back_somalia oder economic_aid_programmes oder arms_on_credit
  - Idee „Vanguard of World Revolution“: Auslandseinfluss +10 %, Unterstützungskampagnen (Cold War) +10 %, Steuereinnahmen -2 % (`add_ideas`)

## Dateien (Umsetzung)

- `common/national_focus/COLDWAR_SOV_1970_focus.txt`: Tree `COLDWAR_SOV_1970_focus`, alle Fokusse
- `common/ideas/COLDWAR_SOV_1970_ideas.txt`: Startgeister und Fokus-Ideen
- `common/dynamic_modifiers/COLDWAR_SOV_1970_dynamic_modifiers.txt`: 5 Länder-Modifier, Zusammenhaltsstufen, Partei- und Führerprogramme
- `common/bop/COLDWAR_SOV_1970.txt`: Politbüro-Balance
- `common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt`: Init, BIP-Kosten, exakte Fraktionsänderung, Outlook-Popularität, Zusammenhalt, Angebote
- `common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt`: Pfad- und Führertrigger
- `common/decisions/COLDWAR_SOV_1970_decisions.txt (+ categories)`: Politbüro, Fünfjahrpläne, Union, Getreide
- `events/COLDWAR_SOV_1970_events.txt`: Events und Angebots-Events (Namespace `COLDWAR_SOV`)
- `common/on_actions/COLDWAR_SOV_1970_on_actions.txt`: Monatliches Zusammenhalts-Update (`on_monthly_SOV`)
- `common/opinion_modifiers, country_leader traits, interface/*.gfx`: Meinungen, Traits, Fokus-Icons aus den Cold-War-GFX-Ordnern
- `localisation/english/COLDWAR_SOV_1970_l_english.yml`: nur Englisch, UTF-8 mit BOM
- `history/countries/SOV - Russia.txt (Patch)`: `load_focus_tree = COLDWAR_SOV_1970_focus`, `COLDWAR_SOV_initialize_1970 = yes`
- `mdcw_1970_focus_tree_effects.txt (Patch)`: SOV aus dem Generic-Fallback ausnehmen

## Porträts

Leonid Brezhnev (vorhanden (SOV_Coldwar_Brezhnev.dds)), Mikhail Gorbachev (vorhanden), Konstantin Chernenko (vorhanden), Alexei Kosygin (neu), Nikolai Podgorny (neu), Mikhail Suslov (neu), Alexander Shelepin (neu), Yuri Andropov (neu), Marshal Andrei Grechko (neu (Uniform)), Marshal Dmitry Ustinov (neu (Uniform)), Grigory Romanov (neu), Viktor Grishin (neu (Erbe Tschernenkos)), Heydar Aliyev (neu (Erbe Andropows)), Nikolai Ryzhkov (neu), Andrei Sakharov (neu), Aleksandr Solzhenitsyn (neu), Roy Medvedev (neu), Dzhermen Gvishiani (neu), Vladimir Poremsky (neu), Pyotr Siuda (neu), Sergei Trapeznikov (neu), Nikolai Baibakov (neu), Nikolai Shchelokov (neu), Nikolai Shmelyov (neu), Grigory Galazy (neu), Alexander Yakovlev (neu), Pyotr Shelest (neu), Dmitry Polyansky (neu), Grand Duke Vladimir Kirillovich (neu), Komitee der nationalen Wiedergeburt (21) (kollektive Führung, Emblem statt Porträt)

## Offen für die Umsetzung

- Fokus-Icons aus den Cold-War-GFX-Ordnern zuordnen (wie Ägypten: Icon + 2 Alternativen pro Fokus).
- Staats-IDs für Samotlor/Tjumen, Magnitka, Amur-Bunker prüfen (derzeit `random_owned_controlled_state` mit Limit).
- Getreideimporte und Fünfjahrpläne als Decisions ausformulieren; Kosten der MD-Bau-Helfer über `skip_payment` + BIP-Anteil (BIP SOV ≈ 186).
- `COLDWAR_SOV_install_gensec`: Charaktere für alle elf Kandidaten plus Grischin und Alijew anlegen (Porträts siehe oben); Todesdaten als Game-Rule-abhängige Events.
- Ingame-Test HOI4 1.19 mit frischem `error.log`; KI-Beobachtung (Breschnew-Weg, Nachfolge 1982–1985).
