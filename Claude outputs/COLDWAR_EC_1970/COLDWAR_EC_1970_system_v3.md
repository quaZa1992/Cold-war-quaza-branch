# EG 1970 – neues System „The European Communities" (Systemdesign v3.4)

Stand 30.10.2026 · MD Cold War (`mdcoldwar`, MD 2.0.3-Hotfix / HOI4 1.19), Start 1.1.1970, MP-Rollenspiel
**Status: umgesetzt (Code im Mod seit 30.10.2026, Umsetzung: `claude/mdcw_ec_1970_implementation.md`).** Ersetzt v2 („MD-EU mit 1970-Daten", Stufe 1 vom 18.10.2026) und die Regel G2.
Visualisierung: [Artifact „EC 1970 System"](https://claude.ai/artifact/AtEHwfjAQbMaup3k9Dr32d). Spieltexte Englisch, Doku Deutsch. Präfix `COLDWAR_EC_`.
Dieses Doc ersetzt am selben Pfad die v2-Ideensammlung; v2 und die Stufe-1-Sicherungen liegen lokal in `Claude outputs\COLDWAR_EC_1970\`.

**Aufträge Enes (29.10.2026):**
1. Neues System statt MD-EU: simple UI, automatisiert, Spieler stimmen ab und schlagen vor.
2. Historisches Logo, Umbenennung in EU sichtbar; Stimmrechte, Parlament usw. korrekt und im MP machbar; historische und alt-historische Proposals; alles bringt allen Mitgliedern Gutes und Schlechtes.
3. Folgende Wünsche:
   - **KI aus den Abstimmungen, nur Spieler stimmen; die KI interagiert gar nicht**, sie bekommt nur die Spirits und zahlt ein.
   - Schrift wie MD, weniger gequetscht.
   - Blaues Design verbessern.
   - Preise teils erhöhen.
   - Gemeinschaftsprojekte (Gebäude) und EG-Hilfe für andere Länder gegen eine Gegenleistung, Western Support.
   - **„Date-Begrenzungen soll es nicht geben! Aber es soll teilweise dauern, bis sowas ratifiziert wird, Bürokratie symbolisieren."**

**Änderungen v3.3 → v3.4 (Umsetzung, 30.10.2026)** (Enes: „plus einmal pro Woche ein Abgleich – das ist nicht gut … performance-freundlich"; „Überlappungen vermeiden! Es soll genau so aussehen wie in der Visualisierung"):
- Kein wöchentlicher Abgleich mehr: Die Empfängerliste entsteht nur beim Klick des Betrachters; Spieler-Anwesenheit wird nebenbei gemerkt (Flag beim Öffnen, Klicken, Abstimmen), ohne Weltschleife (§11.5).
- Uhr: Wochen- und Monatstakt laufen im Puls eines einzigen „Uhr-Landes" (das Spiel verteilt die Pulse der Länder über Woche und Monat), nicht täglich (§2 Regel 7).
- Oberfläche genau nach der freigegebenen Visualisierung: eigene Bitmap-Schriften Ubuntu und Share Tech Mono, Layout pixelgenau, Überlappungsprüfung im Generator (§14).
- Gewinn/Preis auf den Karten als Kurzfassung (höchstens drei Zeilen), die vollständige Liste im Tooltip (§14).

**Änderungen v3.2 → v3.3** (Enes: „die in-return-Werte sollen dynamisch sein … Assistance Programme in allen Spieler-Ländern, Filter nach Kontinent, performance-freundlich über mehrere Sessions … Mitgliedstaaten verlieren −1 oder −2 Kapazität, wer unter die Schwelle fällt, verliert sein aktuelles Programm"):
- Gegenleistungen hängen von BIP, Rohstoffen, Arbeitslosigkeit, Globalismus, Regierung, Ausrichtung und Machtrang des Empfängers ab (§11.2).
- Empfänger sind alle Spieler-Länder außerhalb der EG, mit Kontinentfilter (§11.5).
- EG-Programme kosten alle Mitglieder Kapazität; wer darüber liegt, verliert ein eigenes Programm. Der CW-Code hatte dafür noch keine Regel (§11.3).
- Abwesende Spieler: Angebote und Ratifizierungen warten auf sie (§11.5).

**Änderungen v3.1 → v3.2:**
- Nur Spieler stimmen ab, Schwellen zählen nur Spieler-Gewichte (§2a).
- Keine Datumssperren; stattdessen Bürokratie-Fristen (§6a).
- Preise erhöht (§8).
- Haushalt mit „Wer zahlt an wen" und Gemeinschaftsdarlehen (§9).
- Neu: Gemeinschaftsprojekte (§10), Hilfe für Drittländer und Western Support (§11).
- UI: MD-Schriften, größeres Fenster, Reiter „Programmes" (§14).

---

## 0. Kurzfassung

- **Ein Fenster, fünf Reiter:** Council · Parliament · Proposals · Programmes · Community. 1080 × 700, MD-Schriften (Ubuntu Bold `hoi_16mbs`/`hoi_18mbs`, Orator `hoi_24header`/`hoi_36header`), Toolbar-Knopf an der Stelle des MD-EU-Knopfs.
- **Nur Spieler handeln.**
  - Spieler-Regierungen bringen ein, stimmen im Rat und im Parlament (mit ihrer Delegation) und ratifizieren.
  - KI-Länder sind **passive Mitglieder**: Sie zahlen ein, bekommen Rückflüsse und Spirits und ratifizieren nach einer Bürokratie-Frist automatisch. Sie stimmen nie, schlagen nichts vor, beantragen nichts und entscheiden nichts.
- **Keine Datumssperren.** Alles ist jederzeit möglich, nur logische Vorgänger zählen. Dafür dauert es: Kommissionsentwurf, Parlamentslesung, Umsetzungsfristen, Regierungskonferenz, Ratifizierung.
- **Institutionen wie in den Verträgen:** Kommission schlägt vor, Parlament gewinnt Rechte, Rat entscheidet mit den historischen Gewichten (unter Spielern), Verträge brauchen Konferenz und Ratifizierung.
- **Geld:** Mitglieder zahlen einen Anteil ihres BIP in den Gemeinschaftshaushalt; er fließt nach festen Schlüsseln zurück. Nettozahler zahlen so an Nettoempfänger. Dazu kommen Gemeinschaftsprojekte mit Gebäuden und Hilfsprogramme für Drittländer gegen eine Gegenleistung, die im Cold-War-System als westliche Hilfe zählen.
- **Emblem:** EGKS-Flagge mit einem Stern je Mitglied, ab „A People's Europe" die Europaflagge, mit dem Unionsvertrag „The European Union".

---

## 1. Warum ersetzen, was wir von COMECON übernehmen

**Probleme der MD-EU im 1970-Spiel:**
- Zombie-Start mit den 15 Mitgliedern von 2000.
- Parlament mit 24 Fraktionsarrays, 11 Ämter, Haushaltsentwurf, MFF und Kampagnen.
- Sieben Code-Stellen je Agenda in MD-Dateien.
- Unsichtbare KI-Tabellen.

**Vom Team-COMECON übernommen** (`tools/comecon/README.md`, `docs/design/comecon/COUNCIL_ELECTION.md`):
- Toolbar-Knopf, ein zentriertes Fenster, Seitenwechsel statt Scrollen, Child-Scripted-GUIs je Reiter.
- Organisationsuhr, `dirty`-Variable, Klicks prüfen Zustand und Vorgangsnummer erneut.
- **KI ist passiv** wie bei COMECON („AI governments cannot propose, finance, vote … may receive agreed benefits as passive hosts or recipients").
- Python-Generator mit Validator, Wiederverwendung von `pagination.py` und `controls.py`.

**Nicht übernommen:**
- Finanzierungsanteile in 5-%-Schritten, Unterschriftenbögen, vier parallele Akten.
- Die eigenen BMFont-Atlanten. Wir nutzen die MD-/Vanilla-Schriften wie das MD-EU-Fenster (`interface/eu.gui`: `hoi_16mbs` 98×, `hoi_18mbs` 69×, `hoi_24header` 4×, `hoi_36header` 1×).

---

## 2. Grundregeln

1. **Verfahren wie in den Verträgen** (EWGV 1957, Fusionsvertrag 1965, Einheitliche Akte 1986, Unionsvertrag 1992). Vereinfachungen stehen dabei.
2. **Nur Spieler stimmen und entscheiden** (§2a). Die KI interagiert nicht mit dem System.
3. **Keine Datumssperren.** Ein Beschluss ist verfügbar, sobald seine logischen Vorgänger angenommen sind. Historische Daten stehen nur als Information im Katalog und im optionalen Kommissionskalender.
4. **Bürokratie kostet Zeit** (§6a): Entwurf, Lesung, Abstimmung, Umsetzung und Ratifizierung haben Fristen. Mehrere laufende Verfahren verlängern sie („Commission workload").
5. **Jeder Beschluss bringt allen Mitgliedern einen Gewinn und einen Preis** (G6), dazu Folgen für einzelne Länder. Keine Kampfboni (G7), keine automatischen Sanktionen (G12).
6. **Nichts wird Spielern aufgezwungen** (M1): Ein Spieler-Drittland nimmt Abkommen an oder lehnt ab; Austritt und Teilnahme entscheidet jedes Spieler-Land selbst.
7. **Performance** (G17): Ein Wochen- und ein Monatstakt im Puls eines Uhr-Landes; der Wochentakt liest nur die offenen Akten (höchstens zehn), die laufenden Programme und den Kalender, nie die Welt. Monatlich Zustimmung, Haushalt, Gegenleistungen. Geld wöchentlich über den MD-Geldsystem-Hook. Das Fenster rechnet nur beim Klick des Betrachters.

---

## 2a. Nur Spieler stimmen

**Wer handelt:**

| | Spieler-Land | KI-Land |
|---|---|---|
| Mitglied | bringt ein, stimmt im Rat und mit seiner Delegation im Parlament, ratifiziert (Parlament oder Referendum), wählt Teilnahme (Schlange, Schengen, Währung) | **passiv**: zahlt Beiträge, erhält Rückflüsse, Spirits und Modifier, ratifiziert Verträge nach seiner Bürokratie-Frist automatisch, nimmt an allen Teilnahme-Teilen teil |
| Drittland | beantragt Beitritt oder Assoziierung, nimmt Abkommen und Hilfsprogramme an oder lehnt ab | **passiv**: Abkommen und Hilfsprogramme, die die Spieler beschließen, treten automatisch in Kraft; beantragt nie etwas |

**Schwellen** zählen nur die Spieler-Mitglieder (die „sitzenden Delegationen"):
- **Qualifizierte Mehrheit:** 70,5 % der Gewichte der Spieler-Mitglieder, aufgerundet.
- **Einstimmigkeit:** kein Spieler stimmt Against.
- **Einfache Mehrheit** (Regierungskonferenz einberufen): mehr als die Hälfte der Spieler-Mitglieder.
- **Parlament:** zählt nur die Sitze der Spieler-Delegationen.

| Beispiel 1970 | Spieler | Spieler-Gewicht | Q-Schwelle | Folge |
|---|---|---|---|---|
| zwei Große | FRA, GER | 20 | 15 | beide nötig |
| drei Große | FRA, GER, ITA | 30 | 22 | zwei Große reichen nicht (20) → faktisch alle drei |
| drei Große + BEL | FRA, GER, ITA, BEL | 35 | 25 | zwei Große + BEL (25) reichen |
| sechs Spieler | alle | 42 | 30 | wie historisch |

**Sonderfälle:**
- **Ein einziger Spieler-Mitglied:** Er entscheidet allein; Verträge brauchen trotzdem die Ratifizierungsfristen der KI-Mitglieder.
- **Kein Spieler-Mitglied:** Der Rat tagt nicht. Laufende Fristen, Haushalt und Projekte laufen weiter, nichts Neues wird beschlossen. Die Kommission legt optional ihren Kalender vor; ohne Spieler bleibt er liegen.
- **Quorum (Frage 2):** Mehrheitsbeschlüsse brauchen mindestens zwei abgegebene Spieler-Stimmen, außer es gibt nur einen Spieler.

---

## 3. Emblem und Name

**Historische Lage:**
- Die EG hatte 1970 kein eigenes Emblem. Die einzige Flagge einer der drei Gemeinschaften war die EGKS-Flagge: blau oben, schwarz unten, ein goldener Stern je Mitglied, nahe der Mittellinie auf beide Hälften verteilt, bei ungerader Zahl einer weniger oben. 6 Sterne 1958–1972, 9 ab 1973, 10 ab 1981, 12 ab 1986, eingeholt 23.7.2002.
- Europaflagge: Vorschlag des Parlaments 11.4.1983, Europäischer Rat Mailand 28./29.6.1985, erstmals gehisst 29.5.1986.

**Im Spiel:**

| Zustand | Emblem | Name | Kopfzeile |
|---|---|---|---|
| Start | EGKS-Flagge, Sterne = Mitglieder (4–16) | The European Communities | Council of the European Communities · Brussels |
| nach A6 „A People's Europe" | Europaflagge, immer 12 Sterne | The European Communities | unverändert |
| nach A9 Unionsvertrag | Europaflagge | The European Union | Council of the European Union; Aktenzeichen „EU/…" |
| alt: A11 Tindemans / A12 Spinelli | bisheriges Emblem | The European Union | Council of the European Union |
| alt: A10 Staatenunion | EGKS-Flagge | The Union of States | Council of the Union |

- Das Emblem steht im Fensterkopf, auf dem Toolbar-Knopf und in jeder News.
- Technik: Sprite mit Frames (EGKS 4–16 Sterne + Europaflagge) vom Generator gezeichnet, `frame = global.COLDWAR_EC_emblem_frame`; Name über `COLDWAR_EC_GetOrgName`.

---

## 4. Status der Länder und Start 1970

| Stufe | Bedeutung | Weg |
|---|---|---|
| 0 Third country | kein Verhältnis | – |
| 1 Associate | Assoziierung (Art. 238) | D2 + Annahme (Spieler) bzw. automatisch (KI) |
| 1F Associate (frozen) | ausgesetzt | Diktatur; taut auf, sobald die Demokratieklausel erfüllt ist |
| 2 Applicant | Antrag (Art. 237) | nur Spieler-Länder per Decision; KI beantragt nie |
| 3 Candidate | verhandelt | Rat einstimmig |
| 4 Acceding | Vertrag unterzeichnet | Rat einstimmig (+ Parlament ab A7) |
| 5 Member | ab dem nächsten 1. Januar nach allen Ratifizierungen | Idee `COLDWAR_EC_member` |

**Demokratieklausel** (Birkelbach-Bericht 1962): freie Wahlen und keine autoritäre oder kommunistische Regierungspartei (MD-Indizes 0, 4, 5, 7, 13, 19–23; prüfen).

**Start 1.1.1970:**
- Mitglieder FRA, GER, ITA, BEL, HOL, LUX
- Antragsteller ENG, IRE, DEN, NRY (Anträge 1967, Den Haag 1969). Ein KI-Antragsteller kann von den Spielern aufgenommen werden und tritt dann passiv bei, ohne Referendum.
- Assoziiert TUR; GRE assoziiert und eingefroren
- Bestand: Zollunion, Gemeinsame Agrarpolitik, Parlament mit 142 ernannten Abgeordneten

---

## 5. Institutionen

### 5.1 Ministerrat

- **Gewichte** (CVCE, Skala 1973): FRA, GER, ITA, ENG 10 · SPR 8 · BEL, HOL, GRE, POR 5 · AUS, SWE 4 · DEN, IRE, FIN, NRY 3 · LUX 2; andere nach Bevölkerung (ab 50 Mio. 10, ab 25 Mio. 8, ab 12 Mio. 5, ab 7 Mio. 4, ab 3 Mio. 3, sonst 2).
- **Mehrheiten** (Art. 148), gezählt unter Spielern (§2a):
  - einfache Mehrheit für die Einberufung einer Regierungskonferenz (Mailand 1985: 7 : 3)
  - qualifizierte Mehrheit (70,5 %) für Agrar, Handel (Art. 113), Haushalt, nach A7 Binnenmarkt
  - Einstimmigkeit für Verträge, Beitritt, Assoziierung, Eigenmittel, Art. 235, Ernennungen, Gipfel- und EPZ-Konsens; Enthaltung blockiert nicht
- **Luxemburger Kompromiss** (29.1.1966), „Invoke a Vital National Interest":
  - bei Q-Beschlüssen; das eigene Against blockiert
  - Preis 75 PP (jede weitere Nutzung im Jahr doppelt), Meinung aller anderen Mitglieder −15 für ein Jahr
  - nach A5 doppelt so teuer, nach A7 200 PP; nach A12 abgeschafft; nach A10 kostenlos
  - Präsidentschaft und Land des Kommissionspräsidenten zahlen doppelt

### 5.2 Kommission

- **Initiativrecht:** Gesetze legt nur die Kommission vor. Spieler fordern sie an (Art. 152, 50 PP); danach folgt die Entwurfsfrist (§6a).
  - Hat ein Spieler das Amt des Kommissionspräsidenten: Event „Table / Decline" (ohne Antwort in 30 Tagen „Table").
  - Sonst legt die Kommission automatisch vor (System, keine KI-Entscheidung).
- **Kommissionskalender** (Game Rule, Standard an): Die Kommission legt die historischen Beschlüsse zu ihren historischen Daten vor. Das ist keine Sperre: Alles kann früher eingebracht werden, und der Kalender wartet auf Spielerstimmen.
- **Stellungnahme zu Beitrittsanträgen:** Spieler-Kommissionspräsident frei, sonst günstig bei Demokratieklausel. Nur Information; abstimmen tun die Spieler.
- **Ernennung im Einvernehmen der Regierungen** (Art. 11 Fusionsvertrag), R2 ohne Ende:
  - erste Ernennung 1.7.1970, danach alle 4 Jahre; nach jeder Erweiterung beginnt am Beitrittstag eine neue Amtszeit (so entstehen die historischen Termine 1973, 1977, 1981, 1985, 1989); ab A9 alle 5 Jahre
  - Spieler kandidieren per Decision (50 PP); die Spieler-Präsidentschaft schlägt vor; die Spieler stimmen einstimmig.
  - Ohne Spieler-Kandidaten oder ohne Einigung bleibt das Amt ohne Wirkung bei der bisherigen Nationalität; die historischen Präsidenten (ITA 1970, FRA 1973, ENG 1977, LUX 1981, FRA 1985/1989) sind nur Anzeige.
  - Ab A9 stimmt zusätzlich das Parlament zu.
- **Amt:** PP-Gewinn +5 %, Stabilität +1 % · Bürokratiekosten +3 %, Luxemburger Kompromiss doppelt.

### 5.3 Europäisches Parlament

**Zusammensetzung** (historische Sitze):
- 1970: 142 ernannt (FRA, GER, ITA 36; BEL, HOL 14; LUX 6)
- 1973: 198 (+ ENG 36, DEN 10, IRE 10)
- ab A4 direkt gewählt: 410 (FRA, GER, ITA, ENG 81; HOL 25; BEL 24; DEN 16; IRE 15; LUX 6); GRE 24, SPR 60, POR 24
- neue Länder nach Bevölkerungstabelle

**Abstimmung:**
- Es stimmen nur die Delegationen der Spieler-Mitglieder.
- Jede Spieler-Delegation stimmt einheitlich; der Spieler setzt die Stimme in der Lesung (For / Against / Abstain). Ohne Eingabe stimmt sie wie die Regierung im Rat.
- Die Fraktionen (Christdemokraten, Sozialisten, Liberale, Gaullisten, Konservative, Kommunisten …) werden aus der Parteipopularität berechnet und nur angezeigt.
- Schwellen über die Spieler-Sitze:
  - Stellungnahme: Mehrheit der abgegebenen Stimmen
  - Ablehnung in der Zusammenarbeit oder Mitentscheidung, Zustimmung: absolute Mehrheit der Spieler-Sitze
  - Haushalt ablehnen: absolute Mehrheit und zwei Drittel der abgegebenen Stimmen
  - Misstrauensantrag: zwei Drittel der abgegebenen Stimmen und absolute Mehrheit

**Rechte nach Beschluss:**

| Recht | ab | Wirkung |
|---|---|---|
| Anhörung, Misstrauensantrag | Start | Übergeht der Rat ein Nein des Parlaments: Zustimmung −2 in allen Mitgliedern |
| Haushalt: letztes Wort bei nicht-obligatorischen Ausgaben | A1 | Parlament stimmt beim Jahreshaushalt mit (ohne Veto) |
| Haushalt ablehnen | A3 | Ablehnung → vorläufige Zwölftel |
| Direktwahl | A4 | erste Europawahl im Juni nach dem Inkrafttreten von A4 (mindestens 365 Tage danach), dann alle 5 Jahre ohne Ende (hist. 1979, 1984, 1989, 1994 …); Sitze neu, Kampagnen-Decision |
| Zusammenarbeit, Zustimmung | A7 | Parlaments-Nein → Rat nur einstimmig; Beitritt/Assoziierung brauchen das Parlament |
| Mitentscheidung | A9 | Parlaments-Nein → Beschluss scheitert |
| alt: Mitentscheidung für alles | A12 | – |
| alt: nur Anhörung | A10 | Direktwahl gesperrt |

### 5.4 Europäischer Rat, EPZ, Präsidentschaft, Gerichtshof

- **Gipfel / Europäischer Rat** (ab A2): Konsens der Spieler, ohne Parlament.
- **EPZ** (ab E1): Außenminister der Spieler, Konsens.
- **Präsidentschaft:** rotiert halbjährlich in der Reihenfolge der Landesnamen in Landessprache (Belgique, Danmark, Deutschland, Ellas, España, France, Ireland, Italia, Luxembourg, Nederland, Portugal, United Kingdom; belegt 1970 BEL → GER, 1971 FRA → ITA, 1972 LUX → HOL, 1973 BEL → DEN).
  - Ist das Präsidentschaftsland ein KI-Land, gibt es keine Sonderrechte.
  - Spieler-Präsidentschaft: einen Eintrag vorziehen, Kommissionskandidaten vorschlagen, ab A2 ein freier Vorschlag.
  - Idee: PP-Gewinn +5 %, Stabilität +1 % · Bürokratiekosten +3 %.
- **Gerichtshof** (Stufe 2): Vertragsverletzung, wenn ein Mitglied Imperia-Sanktionen gegen ein anderes Mitglied verhängt; Urteil nach 180 Tagen: Zustimmung −3, Meinung −10; ab A9 Zwangsgeld 0,05 % BIP.

---

## 6. Verfahren

| Code | Verfahren | Schritte | Schwelle |
|---|---|---|---|
| **LEG** | Gesetzgebung | Anforderung → Kommissionsentwurf → Parlamentslesung → Rat → Umsetzungsfrist → Wirkung | Rat Q oder U; Parlament: Anhörung, ab A7 Zusammenarbeit, ab A9 Mitentscheidung |
| **VERTRAG** | Art. 236 | Vorschlag einer Regierung → Rat beruft Regierungskonferenz ein → Konferenz → Schlussakte → Ratifizierung in jedem Mitglied → in Kraft | Einberufung einfache Mehrheit; Schlussakte einstimmig; jede Ratifizierung |
| **RATSAKT** | Ratsbeschluss mit Ratifizierung (Eigenmittel Art. 201, Direktwahlakt) | Kommissionsentwurf → Rat → Ratifizierung | einstimmig + alle Ratifizierungen |
| **RAT** | Ratsentschließung | Vorschlag → Rat | einstimmig |
| **GIPFEL · EPZ** | Europäischer Rat · Politische Zusammenarbeit | Vorschlag einer Regierung → Abstimmung | Konsens |
| **BEITRITT** | Art. 237 | Antrag (Spieler) → Stellungnahme → Rat eröffnet → Verhandlungen → Beitrittsvertrag (+ Parlament ab A7) → Ratifizierung aller und des Kandidaten → Mitglied am 1.1. | einstimmig |
| **ASSOZ · HANDEL** | Art. 238 · Art. 113 | Anforderung → Kommissionsentwurf → Rat → Annahme (Spieler-Drittland) bzw. automatisch (KI-Drittland) | Assoziierung einstimmig (+ Parlament ab A7) · Handel Q |
| **FREIWILLIG** | Teilnahme | Rahmenbeschluss → Spieler-Mitglieder wählen per Decision; KI-Mitglieder nehmen teil | – |
| **PROJEKT · HILFE** | §10, §11 | Anforderung → Kommissionsentwurf → Rat → Planung → Bau bzw. Laufzeit | Q |
| **R1** | Jahreshaushalt | jeden Oktober | Rat Q; Parlament ab A1 mit, ab A3 Vetorecht |

### 6a. Bürokratie-Fristen (keine Datumssperren)

| Schritt | Dauer | Anzeige |
|---|---|---|
| Kommissionsentwurf nach einer Anforderung | 45 Tage (Gesetz), 30 Tage (Handel, Hilfe) | „The Commission is drafting" |
| Parlamentslesung | 20 Tage (läuft am Anfang der Ratsabstimmung) | – |
| Ratsabstimmung | 30 Tage | – |
| Umsetzungsfrist (Richtlinien) | 180 Tage nach der Annahme, danach wirken die Zeilen | „Transposition until …" |
| Regierungskonferenz | 180 Tage (Frage 3: 90) | „Intergovernmental Conference" |
| Ratifizierung Spieler | Parlament 90 Tage Verfahren; Referendum 60 Tage Kampagne; Entscheidung binnen 365 Tagen, sonst automatisch im Parlament | Stempel RATIFIED / REFERENDUM |
| Ratifizierung KI-Mitglied | feste Landesfrist: LUX 60, BEL/HOL 120, FRA/GER 150, DEN/IRE 200, GRE/POR/SPR 240, ITA 270, ENG 300 Tage; andere 180 | „ratifies in 120 days" |
| Inkrafttreten | 1. des übernächsten Monats nach der letzten Ratifizierung | – |
| Beitrittsverhandlungen | 540 Tage; Mitglied am 1. Januar danach | – |
| Projekte | Planung 90 Tage + Bauzeit der Gebäude | Fortschrittsbalken |

- **Commission workload:** Laufen mehr als drei Verfahren gleichzeitig (Entwurf, Konferenz, Ratifizierung, Projektplanung), verlängert sich jede neue Entwurfs- und Planungsfrist um 15 % je weiterem Verfahren (Deckel +60 %).
- **Wirkung tritt immer am Ende der Frist ein.** Bis dahin zeigt das Fenster den Beschluss als „adopted, in transposition" mit Restzeit.

**Ratifizierung im Detail:**
- Spieler: „Ratify in Parliament" (50 PP, Stabilität −2 % für 180 Tage) oder „Hold a Referendum" (Ja-Anteil = Zustimmung ± 6; Ja → Stabilität +3 %, Zustimmung +5).
- Nach einem Nein: „Seek an Opt-out" (Edinburgh 1992: draußen bei den freiwilligen Teilen, Zustimmung +8, zweites Referendum nach 180 Tagen) oder „Accept Defeat" (Vertrag scheitert, 365 Tage gesperrt).

**MP-Sicherheit:** Jeder Vorgang hat Nummer, Phase und Frist; Klicks und Events wirken nur auf die aktuelle Nummer. Ratsabstimmungen laufen in einer Spur, Fristen parallel.

---

## 7. Keine KI-Stimmen

- KI-Regierungen stimmen nicht, bringen nichts ein, beantragen nichts, wählen nichts.
- KI-Mitglieder zählen weder für Schwellen noch für das Parlament. Sie zahlen, erhalten, bekommen alle Modifier und Spirits, nehmen an allen Teilnahme-Teilen teil und ratifizieren nach ihrer Frist (§6a).
- KI-Drittländer: Abkommen und Hilfe, die die Spieler beschließen, treten nach der Kommissionsfrist automatisch in Kraft.
- Damit entfallen K1/K2/K3, die Fraktions-Haltungstabelle, die KI-Antragsteller-Daten und die KI-Referenden.

---

## 8. Katalog

### 8.1 Wertesystem

- `COLDWAR_EC_community` (alle Mitglieder) und `COLDWAR_EC_participation` (Teilnehmer).
- Einmaliges als Effekt.
- Kürzel:
  - HM Handelsmeinung · ZS Zivilindustrie-Steuer · AS Agrar-Steuer · AP Agrarproduktivität
  - ZP Zivilfabrik-Produktivität · PW Produktivitätswachstum · FO Forschung · ZI Zinsen
  - ST Stabilität · PP PP-Gewinn · BK Bürokratiekosten · SK Sozialkosten · KG Konsumgüter
  - WE Weltmarkt-Exposition (CW) · ÖR Ölpreis-Resistenz · IB Infrastruktur-Bautempo · AK Erwerbsbevölkerung
  - DD demokratische Drift · GL Globalismus · Z Zustimmung · AR Abrufsatz (% BIP) · M Meinung · Sp Spannung
- Deckel wie v3.1 (HM +0,35, ZP +0,10, PP −0,20, BK +0,15 …).
- **Mitgliedschaft:** HM +10 %, ZS +3 %, AS +5 % · PP −5 %, KG +2 %.
- **Einbringen:** Anforderung bei der Kommission 50 PP; Vertrag 100 PP; Gipfel, EPZ, Rat 50 PP.
- **Erhöhte Preise** gegenüber v3.1 sind mit ↑ markiert.

### 8.2 Kapitel A – Verträge und Institutionen

| ID | Beschluss (EN) | hist. Datum (Info) | Verf. | Gewinn für alle | Preis für alle | Besonders |
|---|---|---|---|---|---|---|
| A1 | The Hague Package: Own Resources and the Treaty of Luxembourg | 21./22.4.1970 | RATSAKT | AS +2, ST +1; EP Haushaltsrecht 1 | AR 0,7 → 0,9 % | Agrarländer erhalten mehr, Importländer zahlen mehr |
| A2 | The European Council (Paris Summit) | 10.12.1974 | GIPFEL | ST +1; Präsidentschaft: freier Vorschlag | ↑ PP −2, BK +1 | – |
| A3 | Second Budgetary Treaty and the Court of Auditors | 22.7.1975 | VERTRAG | BK −2, Z +2 | ↑ AR +0,03, PP −1; EP darf den Haushalt ablehnen | braucht A1 |
| A4 | Act on Direct Elections | 20.9.1976 | RATSAKT | Z +5, DD +0,01 | ↑ PP −3, BK +1 | braucht A2 |
| A5 | Overriding the Veto: the Farm Price Vote | 18.5.1982 | RAT (Q) | AS +1; Luxemburger Kompromiss doppelt | Z −2, ST −1 für 1 Jahr | wer zuletzt ein Veto einlegte: Z −5 |
| A6 | A People's Europe (Adonnino Report) | 28./29.6.1985 | GIPFEL | Europaflagge, Z +5, ST +1 | ↑ AR +0,02, BK +2 | – |
| A7 | Single European Act | 17./28.2.1986 | VERTRAG | ZP +5, PW +1, HM +5; Binnenmarkt Q; EP Zusammenarbeit | ↑ BK +5, PP −4, KG +1; Luxemburger Kompromiss 200 PP | braucht A4, B3 |
| A8 | The Schengen Agreement | 14.6.1985 | FREIWILLIG | Teiln.: HM +3, AK +1 | ↑ Teiln.: Polizeikosten +8 | – |
| A9 | Treaty on European Union | 7.2.1992 | VERTRAG | Name „European Union", HM +5, ST +2; EP Mitentscheidung | ↑ PP −5, BK +3, Z −5 | Opt-outs möglich; braucht A7, B6 |
| A10 | *(alt)* A Union of States (Fouchet Plan) | 1961/62 | VERTRAG | PP-Malus der Mitgliedschaft entfällt, Luxemburger Kompromiss kostenlos; Name „The Union of States" | HM −5, FO −1; sperrt A4, A7, A9, A11, A12 | Z +5 bei nationalen Regierungen, −5 in Benelux |
| A11 | *(alt)* The Tindemans Union | Bericht 29.12.1975 | VERTRAG | Name „European Union", HM +5, ST +1; EPZ-Vorschläge halber Preis | PP −4, BK +3, Z −3 | braucht A2 |
| A12 | *(alt)* The Spinelli Treaty | EP-Entwurf 14.2.1984 | VERTRAG | Name „European Union", alle Gesetze Q mit Mitentscheidung, ZP +5, FO +3 | PP −10, kein Veto | Z −10 in Mitgliedern unter 60; braucht A4 |

### 8.3 Kapitel B – Wirtschaft und Währung

| ID | Beschluss (EN) | hist. Datum | Verf. | Gewinn | Preis | Besonders |
|---|---|---|---|---|---|---|
| B1 | The Werner Plan: Stage One | 22.3.1971 | RAT | alle: ZI −3, HM +2 | ↑ alle: ST −1, PP −2 | braucht A1 |
| B2 | The Snake in the Tunnel | 24.4.1972 | FREIWILLIG | Teiln.: ZI −3, HM +5 | ↑ Teiln.: WE +6, ST −2 | Leave / Rejoin per Decision |
| B3 | European Monetary System and the ECU | 13.3.1979 | FREIWILLIG | ERM: ZI −5, ZS +2 | ↑ ERM: ST −1, KG +2, PP −1 | ersetzt B2 |
| B4 | The Internal Market Programme | 14.6.1985 | GIPFEL | alle: HM +5, ZP +3, GL +5 | ↑ alle: BK +4, WE +6 | Agrarländer Z −2 |
| B5 | Liberalisation of Capital Movements | 24.6.1988 | LEG Q | alle: ZI −2, ZS +2 | ↑ alle: WE +8, ST −2 | braucht A7 |
| B6 | The Delors Report: EMU Stage One | 1.7.1990 | GIPFEL | alle: ZI −2, HM +2 | ↑ alle: PP −2, ST −1 | braucht B3 |
| B7 | Economic and Monetary Union | 9./10.12.1991 | VERTRAG | Währung: HM +10, ZI −5 | ↑ Währung: PP −6, Z −5, ST −1 | Opt-out möglich |
| B8 | *(alt)* Werner Stage Three: Irrevocable Parities | Ziel 1980 | VERTRAG | Teiln.: HM +8, ZI −5 | Teiln.: PP −5, ST −2, WE +5 | braucht B2 |
| B9 | *(alt)* Community Energy Solidarity | Kopenhagen 12/1973 | GIPFEL | alle: ÖR +10; Lieferangebote an Mitglieder unter Embargo | alle: PP −1; M OAPEC −10 | liest das Ölsystem nur |
| B10 | Community Loan to [member] | VO 397/75 vom 17.2.1975; ITA, IRE 1976 | RAT (Q) | Empfänger: Treasury +1,5 % BIP sofort | übrige Mitglieder zahlen den Betrag nach BIP-Anteil; Empfänger zahlt 5 Jahre zurück (+2 % Zinsen jährlich an die Geber) | §9.3 |

### 8.4 Kapitel C – Gemeinsame Politiken

| ID | Beschluss (EN) | hist. Datum | Verf. | Gewinn | Preis | Besonders |
|---|---|---|---|---|---|---|
| C1 | Common Fisheries Policy | 20.10.1970 | LEG Q | alle: AS +1 | ↑ alle: BK +2 | Z −8 NRY, ICE; −3 DEN, IRE, ENG |
| C2 | The Mansholt Plan | 17.4.1972 | LEG Q | alle: AP +10 | alle: ST −2 für 2 Jahre, AR +0,02 | Z −3 FRA, BEL, ITA |
| C3 | First Environmental Action Programme | 22.11.1973 | LEG U | alle: ST +1, KG −1 | ↑ alle: ZP −3, BK +2 | – |
| C4 | Social Action Programme and Equal Treatment | 21.1.1974 | LEG U | alle: ST +2, AK +1 | ↑ alle: SK +5, ZS −2 | – |
| C5 | European Regional Development Fund | 18.3.1975 | LEG U | Empfänger: IB +10; alle: ST +1 | ↑ alle: AR +0,06, BK +1 | braucht A1 |
| C7 | Research Framework Programme and ESPRIT | 25.7.1983 / 28.2.1984 | LEG U | alle: FO +3, ZP +1 | ↑ alle: AR +0,06, BK +1 | braucht A1 |
| C8 | Milk Quotas | 31.3.1984 | LEG Q | alle: AR −0,05, ST +1 | ↑ alle: AS −3 | Z −3 HOL, DEN, IRE, FRA |
| C9 | Budget Correction for [member] | 25./26.6.1984 | GIPFEL | Antragsteller: Nettobeitrag −66 % | übrige Nettozahler tragen den Rest, Z −2 | nur ein Nettozahler für sich |
| C10 | Integrated Mediterranean Programmes | 23.7.1985 | LEG Q | Mittelmeer-Mitglieder: IB +10, AP +5 | ↑ alle: AR +0,04 | – |
| C11 | Erasmus | 15.6.1987 | LEG Q | alle: FO +1, Z +3 | ↑ alle: AR +0,02, BK +1 | – |
| C12 | Delors I: Reform of the Structural Funds | 11.–13.2.1988 | GIPFEL + RATSAKT | Empfänger: IB +10, AP +5; alle ST +1 | ↑ alle: AR +0,10 (Obergrenze 1,2 %), AS −2 | braucht C5 |
| C13 | Community Charter of Fundamental Social Rights | 9.12.1989 | FREIWILLIG | Teiln.: ST +2, DD +0,01 | ↑ Teiln.: SK +6, ZS −2 | – |
| C14 | *(alt)* Dismantling the Price Guarantees | Mansholt 1968 | LEG Q | alle: AR −0,20, KG −2, ZP +2 | alle: AS −5, ST −3 für 2 Jahre | Z −8 in Agrarländern |

C6 (JET) ist jetzt das Projekt P3 (§10).

### 8.5 Kapitel D – Erweiterung und Außenhandel; Kapitel E – Politische Zusammenarbeit

| ID | Beschluss (EN) | hist. Datum | Verf. | Gewinn | Preis | Besonders |
|---|---|---|---|---|---|---|
| D1 | Enlargement: [bis zu 4 Länder] | 30.6.1970 / 22.1.1972 | BEITRITT | beim Beitritt alle: HM +3, GL +2 | ↑ alle: ST −2 für 1 Jahr; Agrar-Rückflüsse neu geteilt | neues Mitglied 5 Jahre Übergang (Beitrag −50 %) |
| D2 | Association Agreement: [country] | MLT 5.12.1970, CYP 19.12.1972 | ASSOZ | alle: HM +1; Assoziierter: Handelsabkommen, Z +5 | ↑ alle: AR +0,02 | – |
| D3 | Preferential Agreements: Spain and Israel | 29.6.1970 | HANDEL | alle: HM +1 | ↑ alle: AS −1; ITA, FRA weitere −1 | – |
| D4 | Free Trade Agreements with EFTA | 22.7.1972 | HANDEL | alle: HM +3, GL +2 | ↑ alle: ZS −2, WE +3 | braucht D1 |
| D5 | Generalised System of Preferences | 1.7.1971 | HANDEL | alle: HM +1; M Entwicklungsländer +10 | ↑ alle: ZS −2 | – |
| D6 | The Lomé Convention | 28.2.1975 | ASSOZ | alle: HM +2; M AKP +15 | ↑ alle: AR +0,04 | – |
| D7 | Global Mediterranean Policy | 1975/76 | HANDEL | alle: HM +2; M Maghreb/Maschrek +10 | ↑ alle: AS −2, AR +0,01 | – |
| D8 | The EC–CMEA Joint Declaration | 25.6.1988 | HANDEL + Angebot an den COMECON-Vorsitz | alle: HM +2; Sp −1 | ↑ alle: WE +3; M USA −5 | – |
| D9 | Integration of the Former GDR | 3.10.1990 | GIPFEL, nur bei Vereinigung | GER: IB +10; alle: HM +2 | ↑ alle: AR +0,05; Z −3 in Nettozahlern | – |
| E1 | European Political Cooperation (Davignon Report) | 27.10.1970 | EPZ | M untereinander +10; schaltet E frei | ↑ alle: PP −2 | – |
| E2 | Copenhagen Report and the Declaration on European Identity | 14.12.1973 | EPZ | M untereinander +5, ST +1 | ↑ M USA −10 | braucht E1 |
| E3 | The Euro-Arab Dialogue | 31.7.1974 | EPZ | ÖR +5; M arabische Staaten +15 | M ISR −20, M USA −5 | braucht E1 |
| E4 | A Common Position at Helsinki | 1.8.1975 | EPZ | Sp −1; M Neutrale +10 | ↑ M Warschauer Pakt −10 | braucht E1 |
| E5 | The Venice Declaration on the Middle East | 13.6.1980 | EPZ | ÖR +5; M arabische Staaten +15 | M ISR −25, M USA −10 | braucht E1 |
| E6 | Common Position on [country] | z. B. 15.1.1980 | EPZ | Support: M Ziel +20 / Condemn: M → Ziel −20 | Ziel: M zu allen −10; Condemn gegen Warschauer Pakt: Sp +1 | Embargo-Empfehlung: Spieler verhängen Imperia-Sanktionen selbst |
| E7 | *(alt)* A Common Foreign Policy by Majority | – | VERTRAG | EPZ per Q; M untereinander +10 | PP −5, Z −5 | braucht E1 |
| E8 | *(alt)* Europe as a Third Force | – | GIPFEL | Sp −2, PP +2; M SOV +10 | M USA −20, WE +3 | braucht E1 |

**Wiederkehrend, ohne Enddatum** (laufen in ihrem Takt, solange das Spiel läuft):
- R1 Jahreshaushalt: jeden Oktober (§9.4)
- R2 Ernennung der Kommission: alle 4 Jahre, nach einer Erweiterung neu, ab A9 alle 5 Jahre (§5.2)
- R3 Europawahl: alle 5 Jahre ab der ersten Wahl nach A4
- Präsidentschaft: jeden 1.1. und 1.7.
- Parlamentspräsident: alle 2,5 Jahre
- ernannte Delegationen: jeden 1. Januar neu, bis zur ersten Europawahl

**Kommissionskalender** (Game Rule, nur Vorlage, keine Sperre): die historischen Daten der Tabellen.

---

## 9. Geld: wie eingezahlt wird und wer an wen zahlt

### 9.1 Einzahlung

- **Beitrag:** Jedes Mitglied zahlt jährlich *Abrufsatz × eigenes BIP*, wöchentlich in Raten. Das gilt für Spieler und KI.
  - Abrufsatz 1970: 0,7 %. Er steigt oder fällt mit den Beschlüssen (Spalte AR), höchstens 1,2 %.
  - Beispiel: GER mit 210 Mrd. BIP zahlt 0,7 % = 1,47 Mrd. im Jahr = 28 Mio. pro Woche.
- **Topf:** Alle Beiträge bilden den Gemeinschaftshaushalt. 1970: Agrar 85 %, Verwaltung 5 %, Sonstiges 10 %. Beschlüsse verschieben die Anteile (Regionalfonds, Forschung, Strukturfonds).
- **Rückfluss:**
  - Agrar nach Anteil der Agrargebäude (`agriculture_district`) an allen Mitgliedern
  - Regional an Mitglieder unter 90 % des durchschnittlichen BIP je Kopf, nach Abstand
  - Forschung und Sonstiges nach BIP-Anteil
  - Verwaltung an BEL (70 %) und LUX (30 %) als Sitzländer
- **Saldo:** Rückfluss − Beitrag. Er erscheint als eine Zeile „European Communities" im wöchentlichen MD-Haushalt (ein `# COLDWAR`-Hook in `00_money_system.txt`, Muster `cc_calculate_weekly_expense`).
- **Geschlossener Kreislauf:** Die Summe aller Salden ist null. Was Nettozahler mehr einzahlen, erhalten Nettoempfänger.

### 9.2 Beispiel 1970, die Sechs (Beispielwerte, Kalibrierung offen)

| Land | Beitrag $M/Woche | Rückfluss $M/Woche | Saldo $M/Woche |
|---|---|---|---|
| GER | 28,4 | 16,2 | **−12,2** |
| FRA | 20,2 | 24,0 | +3,8 |
| ITA | 14,8 | 16,8 | +2,0 |
| HOL | 4,8 | 6,6 | +1,8 |
| BEL | 3,7 | 6,9 | +3,2 |
| LUX | 0,2 | 1,4 | +1,2 |

Deutschland zahlt so über den Topf an Frankreich, Belgien, Italien, die Niederlande und Luxemburg. Das Fenster zeigt die Flüsse im Reiter Community („Who pays whom").

### 9.3 Zahlungen an andere Mitglieder

- **Heute im System:** nur indirekt über den Haushalt.
- **Direkt zwischen zwei Ländern:** die vorhandene Imperia-Diplomatieaktion „Money Transfer" (`imp_money_transfer`); das EG-System baut nichts Paralleles.
- **Neu: B10 Community Loan** (historisch VO 397/75, Kredite an Italien und Irland 1976):
  - Empfänger: sofort 1,5 % BIP Treasury.
  - Die anderen Mitglieder zahlen den Betrag einmalig nach BIP-Anteil.
  - Der Empfänger zahlt 5 Jahre wöchentlich zurück, mit 2 % Zinsen im Jahr an die Geber.
  - Über `modify_treasury_effect` bzw. `modify_debt_effect` (Temp-Variablen direkt davor, C8).
- **C9 Budget Correction:** senkt den Nettobeitrag eines Nettozahlers; die anderen tragen den Rest.

### 9.4 Jahreshaushalt (R1)

- Jeden Oktober: Rat Q; Parlament stimmt ab A1 mit, ab A3 darf es ablehnen.
- Ablehnung → vorläufige Zwölftel im nächsten Jahr: Regional, Forschung und Projekte halbiert, Zustimmung −2 in allen Mitgliedern.

---

## 10. Gemeinschaftsprojekte (Gebäude)

**Ablauf:**
1. Ein Spieler fordert ein Projekt an und wählt Ort und Größe (50 PP).
2. Kommissionsentwurf (45 Tage) → Parlamentslesung → Rat Q.
3. Planung 90 Tage, dann Bau der Gebäude im Zielstaat, bezahlt aus dem Gemeinschaftshaushalt.
   - MD-Bauhelfer mit Zahlung (B2: Gebäude nie gratis); vorher wird ein zusätzlicher Bauplatz geschaffen, wie bei COMECON.

**Finanzierung:**
- Ein Zuschlag auf den Abrufsatz für die Bauzeit; alle Mitglieder zahlen nach BIP-Anteil, auch KI-Mitglieder.
- Das Gastland trägt zusätzlich 20 % selbst.
- Höchstens drei laufende Projekte.

**Wirkung:** Gebäude und ein Spezial-Modifier für das Gastland, ein kleiner Mitnahme-Effekt für alle Mitglieder.

| ID | Projekt (EN) | historischer Bezug | Gastland erhält | alle Mitglieder | Kosten (Gemeinschaft) | Preis |
|---|---|---|---|---|---|---|
| P1 | EIB Infrastructure Loan: [state] | Europäische Investitionsbank seit 1958, Mezzogiorno | +2 Infrastruktur, +1 Zivilfabrik | HM +1 | 0,8 Mrd. über 2 Jahre | Gastland: Schulden +0,3 % BIP (Darlehen, 10 Jahre) |
| P2 | Euratom Joint Research Centre: [state] | Ispra, Geel, Karlsruhe, Petten | FO +3 %, Reaktor-Bautempo +10 % | FO +1 % | 1,0 Mrd. über 3 Jahre | AR-Zuschlag; Gastland BK +2 % |
| P3 | Joint European Torus: [state] | Culham (Ende 1977), Betrieb ab 1983 | FO +4 %, Kernenergie +1 % | FO +1 % | 1,2 Mrd. über 5 Jahre | Spieler konkurrieren um den Ort |
| P4 | Airbus Consortium | Airbus Industrie 18.12.1970 | +1 Zivilfabrik am Gastort | nur Teilnehmer: Luftfahrt-Forschungsbonus, ZS +2 % | Teilnehmer zahlen 0,3 % BIP über 3 Jahre | freiwillig; Teilnehmer BK +2 % |
| P5 | Channel Tunnel | Vertrag von Canterbury 12.2.1986, eröffnet 1994 | FRA und ENG: je +2 Infrastruktur, Schienen in Nord-Pas-de-Calais und Kent | HM +2 | 3,0 Mrd. über 7 Jahre | braucht FRA und ENG als Mitglieder; Spieler unter beiden müssen For stimmen |
| P6 | Trans-European Networks: [3 Staaten] | Unionsvertrag 1992 | je +1 Infrastruktur, Schiene | HM +1 | 1,5 Mrd. über 4 Jahre | AR-Zuschlag |
| P7 | Regional Development Programme: [state] | Regionalfonds, Strukturfonds | +2 Zivilfabrik, +1 Infrastruktur | ST +1 % | 1,5 Mrd. über 3 Jahre | braucht C5 |
| P8 | European Launcher (Ariane) | ESA 1975, erster Start 24.12.1979 | Raumfahrt-Forschungsbonus über das Cold-War-Raumfahrtsystem (Schnittstelle prüfen) | FO +1 % | 2,0 Mrd. über 5 Jahre | freiwillig wie P4 |

---

## 11. Hilfe für Drittländer und Western Support

**Idee:** Die EG unterstützt ein Land außerhalb mit Produktivität, Demokratie, Bau, Forschung oder Landwirtschaft. Das Land gibt der EG etwas zurück.

**Historische Vorbilder:**
- Finanzprotokolle mit GRE (1962) und TUR (1963, 1970, 1977)
- Sonderhilfe für Portugal nach 1974/75 (EIB)
- Lomé (STABEX, 1975)
- PHARE für Polen und Ungarn (VO 3906/89 vom 18.12.1989)
- EIB-Kredite an Jugoslawien in den 1980ern

**Wer, an wen:**
- Jedes Spieler-Mitglied kann ein Programm anfordern (50 PP).
- Empfänger kann **jedes Spieler-Land außerhalb der EG** sein, weltweit. KI-Länder sind keine Empfänger (sie interagieren nicht).
- Mitglieder bekommen keine Programme; für sie gibt es Regionalfonds und Projekte.

**Ablauf:**
1. Programm anfordern: Empfänger, Art, Größe, Gegenleistung. Das Fenster rechnet Wirkung, Gegenleistung, Kosten und Kapazitätsfolgen sofort aus (§11.2–11.4).
2. Kommissionsentwurf (30 Tage), dann Rat Q.
3. Angebot an den Empfänger, beantwortet im EG-Fenster unter „Offers to us". Nichtmitglieder sehen das Fenster lesend wie bei COMECON.
4. Laufzeit 2 Jahre, verlängerbar. Höchstens drei EG-Programme gleichzeitig.

**Kosten:**
- Monatlicher Betrag der Cold-War-Programmart (mittel: Bau 0,4 Mrd., Technik 0,3, Industrie 0,5, Produktivität 0,3, Verwaltung 0,2; Größe ×0,5/×1/×1,5; Empfänger im Ostblock ×1,5).
- Bezahlt aus dem Gemeinschaftshaushalt, also von allen Mitgliedern nach BIP-Anteil. Das Fenster zeigt den eigenen Anteil.

### 11.1 Was der Empfänger bekommt

- Werte der Cold-War-Programmtypen × Größe (×0,5/×1/×1,5) × Wirkungsfaktor E.
- E kommt aus dem Cold-War-Code (`mdcw_cw_recalculate_country`): Entwicklungsstufe (Developing ×1,25, Emerging ×1, Developed ×0,6), Westblock-Empfänger ×1,25 × Stufenfaktor, Ostblock-Empfänger ×0,75, Great Power Competition ×1,1, Modifier „Assistance Effectiveness".
- Die Werte zählen gegen dieselben Deckel je Empfänger wie die Cold-War-Programme (Bau +20 %, Forschung +15 %, Produktivität +6 % …).

| Art (EN) | CW-Vorbild | Empfänger erhält (mittel, vor E) |
|---|---|---|
| Construction Aid | Construction Assistance | Bautempo +8 % |
| Technical Cooperation | Technical Mission | Forschung +6 % |
| Productivity Programme | Productivity Mission | Produktivitätswachstum +3 % |
| Industrial Modernisation | Industrial Equipment Program | Effizienzwachstum +10 %, max. Effizienz +3 % |
| Democracy and Administration | Administrative Assistance + EG-Zeile | PP +5 %, Bürokratie −3 %, demokratische Drift +0,02 |
| Agricultural Aid | EG-eigen (eigener Deckel +12 %) | Agrarproduktivität +8 % |

### 11.2 Dynamische Gegenleistung

Die Gegenleistung hängt von echten Werten des Empfängers ab. Gelesen werden sie beim Angebot und danach monatlich (nur für laufende Programme, höchstens drei):

| Wert | Quelle im Spiel |
|---|---|
| BIP | `gdp_total` (MD) |
| Bevölkerung | `population_total` (MD, Einheit prüfen) |
| Arbeitslosigkeit | `total_unemployed_percentage_display` (MD-Beschäftigung) |
| Rohstoffüberschuss | `resource_produced@X − resource_consumed@X` für Öl, Stahl, Aluminium, Chrom, Wolfram, Gummi (bereits im CW-Code genutzt) |
| Globalismus | Imperia `globalism_value` |
| Entwicklungsstufe | `imp_eco_1/2/3_dynamic_modifier` |
| Regierung | Demokratieklausel, kommunistische Partei (MD `ruling_party`) |
| Ausrichtung | `mdcw_cw_alignment` (0 blockfrei, 1 West, 2 Ost, 3 China) |
| Machtrang | MD-Idee `super_power` … `non_power` |

S = Größe (×0,5/×1/×1,5). Alle Werte sind gedeckelt.

| Gegenleistung (EN) | Faktor | EG-Mitglieder erhalten | Empfänger gibt |
|---|---|---|---|
| Market Access | Markt M = BIP / 50, Grenzen 0,2–2,0; Offenheit O = 1 + (50 − Globalismus) / 100, Grenzen 0,5–1,5 | HM +1,5 % × M × S (max 3 %), ZS +0,5 % × M × S | GL +5 × O × S, ZS −1 % × O × S (Konkurrenz); dafür HM +3 % × S |
| Raw Material Partnership | größter Überschuss V des Empfängers, R = V / 20, Grenzen 0,25–2,0; nur ab V ≥ 5 | Öl: Ölpreis-Resistenz +4 % × R × S (max 10 %) · Stahl/Aluminium: Fabrik-Output +1 % × R × S · Chrom/Wolfram: Rüstungs-Output +1 % × R × S · Gummi: Konsumgüter −0,5 % × R × S | Rohstoff-Exporterlöse −8 % × S (Festpreis); Rohstoffsektor-BIP +1 % × R × S (sicherer Abnehmer) |
| Guest Workers | Angebot U = Arbeitslosigkeit / 8 %, Grenzen 0,25–2,0 → 25 000 × U × S, gerundet auf 25/50/100 Tsd. | Zielland (der Antragsteller) erhält die Arbeitskräfte über das vorhandene Gastarbeiter-System (`mdcw_gw_complete_agreement_*`); alle Mitglieder Z −1 (Einwanderungsdebatte) | Bevölkerung geht, Rücküberweisungen kommen (vorhandenes System), Stabilität +1 % (weniger Arbeitslose) |
| Reform Commitment | Abstand G: Demokratie 0,5 · autoritär 1,0 · kommunistisch 1,5 | Z +1 × G × S | demokratische Drift +0,02 × G × S; Stabilität −2 % × G × S für 1 Jahr; spätere Beitrittsstellungnahme günstig |
| Western Alignment | Gewicht W nach Machtrang: super 2,0 · great 1,6 · large 1,3 · regional 1,0 · minor 0,7 · non 0,5; je nach Ausrichtung | blockfrei: Kosten für den Wechsel in den Westblock −25 % (wie ein US-Programm), M → Mitglieder +10 × S · West: Stabilität +1 % × S · Ost: Wechselkosten West −15 %, Spannung +0,5 | M der SOV zu allen Mitgliedern −5 × W (Ost-Empfänger −15 × W); kein erzwungener Blockwechsel (G11) |

**Rechenbeispiel (Beispielwerte 1970):**
- Iran: BIP 11 Mrd., Ölüberschuss 80, Schah-Regierung, Westblock, Regionalmacht.
- „Raw Material Partnership", mittel: R = 2,0 (gedeckelt) → Mitglieder Ölpreis-Resistenz +8 %; Iran Exporterlöse −8 %, Rohstoffsektor-BIP +2 %.
- „Market Access" lohnt bei Iran kaum: M = 0,22 → Handelsmeinung nur +0,3 %.
- Das Fenster zeigt jede Option mit dem echten Wert; Optionen ohne Grundlage (kein Rohstoffüberschuss) sind ausgegraut.

### 11.3 Kapazität der Mitglieder

- Solange ein EG-Programm läuft, verlieren **alle Mitgliedstaaten** Cold-War-Assistance-Capacity: klein/mittel −1, groß −2; mehrere EG-Programme addieren sich, höchstens −3.
- **Technik:** Dynamic Modifier `COLDWAR_EC_shared_aid` mit `mdcw_cw_assistance_capacity` (der CW-Code liest ihn in `mdcw_cw_recalculate_capacity`: `cap_max` aus Machtrang 8/6/4/3/2/1 + Blockführer-Bonus + Modifier; `cap_free = cap_max − cap_used`, `cap_used` = Summe der Größen aller laufenden und ausgesetzten eigenen Programme, Public Support zählt 1).
- **Befund im CW-Code:** Er prüft die Kapazität nur beim Start (`mdcw_cw_start_pending_program`: `cap_free < size` → Abbruch). Sinkt die Kapazität später, laufen Programme heute über der Grenze weiter. Das EG-System bringt die fehlende Regel mit:
  1. Beim Start eines EG-Programms: Modifier setzen, `mdcw_cw_recalculate_country` je Mitglied (C11).
  2. Ist `cap_free < 0`: Ein Spieler-Mitglied bekommt ein Event mit seinen Programmen und wählt binnen 7 Tagen, welches endet.
  3. Ohne Wahl endet automatisch das **neueste** Programm (größtes `mdcw_cw_p<n>_end@TARGET`), dann das nächste, bis `cap_free ≥ 0`. Beendet wird über die vorhandenen Effekte `mdcw_cw_end_program_<n>` bzw. `mdcw_cw_end_pps`; der Empfänger bekommt die übliche CW-Nachricht.
  4. Endet das EG-Programm, kommt die Kapazität zurück; beendete nationale Programme bleiben beendet.
- **Beispiel:**
  - Westdeutschland ist Großmacht: Kapazität 6. Belegt: „Industrial Equipment · Iran" (groß, 3, neuer) und „Technical Mission · Turkey" (mittel, 2), also 5.
  - Die EG beschließt ein großes Programm → Kapazität 4 < 5.
  - Westdeutschland wählt selbst oder verliert automatisch das neuere Iran-Programm. Danach belegt 2 von 4, das Türkei-Programm läuft weiter.
- **Vor der Abstimmung** zeigt das Fenster jedem Spieler-Mitglied: Kapazität vorher → nachher und welche Programme enden würden. Wer stimmt, weiß, was er riskiert.
- Ist kein Mitglied über der Grenze, passiert nichts außer der niedrigeren Kapazität für neue nationale Programme.

### 11.4 Western Support und Anbindung an das Cold-War-System

- **Empfängerseite:** ein `# COLDWAR`-Hook in `mdcw_cw_recalculate_country` direkt vor „Receiver caps". Er addiert die EG-Programmwerte zu `mdcw_cw_r_*` des Empfängers, bevor die Deckel greifen. Die EG zählt dabei als westlicher Geber: Faktor ×1,25 für Westblock-Empfänger, ×0,75 für Ostblock-Empfänger.
- **Wechselkosten:** ein `# COLDWAR`-Hook in `mdcw_cw_calculate_switch_costs`. Ein laufendes EG-Programm mit „Western Alignment" gibt −25 % auf den Wechsel in den Westblock, wie ein US-Programm heute; der Rabatt bleibt gedeckelt bei 50 %.
- **Spannung:** Ostblock-Empfänger: Spannung +0,5 beim Start über `mdcw_cw_add_tension` (CW-Regel).
- **Anzeige:** Die EG-Programme erscheinen im Reiter „Programmes" des Cold-War-Fensters als „European Communities" und im Developments-Log.
- Kein eigener Geber-Staat nötig; der CW-Generator ist archiviert, die Runtime-Datei wird laut P3 direkt bearbeitet (Zeilen mit `# COLDWAR` markiert).

### 11.5 Spieler kommen und gehen (mehrere Sessions)

- **Empfängerliste:** Sie wird nur gebaut, wenn ein Spieler den Reiter öffnet, einen Filter klickt oder blättert (`every_country` mit `is_ai = no` oder Flag `COLDWAR_EC_player_seen`, nur für den Betrachter, `player_context`). Es gibt keinen periodischen Abgleich und keine Weltschleife im Takt.
- **Filter:** Kontinent (All, Europe, Middle East, Asia, Africa, Americas, Oceania) über die MD-Trigger `is_in_europe`, `is_in_the_middle_east`, `is_in_asia`, `is_in_africa`, `is_in_the_americas`, `is_in_oceania`. Sechs Länder je Seite, Seitenwechsel wie COMECON.
- **Spieler-Gedächtnis:** Ein Spieler-Land bekommt das Flag `COLDWAR_EC_player_seen` (365 Tage), wenn es das Fenster öffnet oder klickt, wenn es als Spieler-Mitglied gezählt wird (wöchentliche Zählung nur über die Mitglieder) und wenn es als Spieler ein Angebot erhält. Ein Land mit diesem Flag gilt bis zu 365 Tage als „abwesender Spieler", auch wenn es gerade die KI steuert:
  - Angebote an ihn bleiben liegen, die Frist läuft nur in Wochen mit Spieler (60 Tage Spielerzeit). Kommt der Spieler nächste Session zurück, sieht er sie sofort unter „Offers to us".
  - Laufende Programme mit ihm laufen weiter (er ist in der Zwischenzeit passiv); nichts wird abgebrochen.
  - Seine Ratifizierungen warten auf ihn bis zur 365-Tage-Frist, statt nach der KI-Frist automatisch zu laufen; danach automatisch im Parlament.
  - Bei Abstimmungen zählen nur anwesende Spieler.
- **Keine Optionen-Events:** Angebote werden über das Fenster beantwortet, nicht über Events mit Optionen (die würde die KI eines abwesenden Spielers sofort beantworten). Die Benachrichtigung ist eine News mit nur „OK".

---

## 12. Öffentliche Zustimmung („Support for Europe", 0–100)

- **Start:** LUX 80; BEL, HOL, ITA, IRE 75; GER 70; FRA 60; DEN 62; NRY 52; ENG 35; SPR, POR, GRE, TUR 50; AUS, SWE, SWI, FIN 35; ICE 40; andere 30.
- **Monatliche Drift** 0,5 zum Ziel: Startwert + Haushalt (Nettoempfänger +5, Nettozahler über 0,3 % BIP −5) + Regierungsfamilie (national −10, kommunistisch −20).
- **Spieler-Decisions:** „Campaign for Europe" (50 PP + 0,1 % BIP, +5, einmal im Jahr), „Eurosceptic Campaign" (−5).
- **Wofür:** Referenden der Spieler, Anzeige. KI-Länder halten keine Referenden.

---

## 13. Beitritt, Assoziierung, Austritt

- **Beitritt:** nur Spieler-Länder beantragen (50 PP; europäisch, Demokratieklausel, kein Krieg mit einem Mitglied, nicht im Warschauer Pakt). Die Start-Antragsteller ENG, IRE, DEN, NRY können als KI aufgenommen werden; sie ratifizieren passiv nach ihrer Frist.
- **Assoziierung:** Spieler-Mitglied fordert D2 an, oder ein Spieler-Drittland fragt per Decision an.
- **Austritt** (nur Spieler):
  - „Put Membership to a Referendum" (UK 1975): Ja → Zustimmung +10, Stabilität +2 %; Nein → Austritt nach 365 Tagen.
  - „Leave the Communities": Stabilität −5 %, Meinung der Mitglieder −25.
  - Wiederbeitritt nach 3 Jahren.
- Nach jedem Beitritt und Austritt werden Gewichte, Schwellen, Sitze, Präsidentschaftsfolge und Sterne neu berechnet.

---

## 14. Oberfläche

**Maße und Schrift:**
- 1080 × 700 statt 900 × 580, damit nichts gequetscht ist.
- MD-Schriften:
  - Fließtext `hoi_16mbs` (Ubuntu Bold 16)
  - größere Werte `hoi_18mbs` (Ubuntu Bold 18)
  - Abschnittstitel `hoi_24header` (Orator, Großbuchstaben)
  - Fenstertitel `hoi_36header`
  - Aktenzeichen und Stempel `hoi_16typewriter`
- Keine Schrift unter 16 px; was nicht passt, wandert in native Tooltips oder auf die nächste Seite. Keine abgeschnittenen Texte.
- **Umgesetzt (v3.4):** Statt der MD-Schriften eigene Bitmap-Schriften in `gfx/fonts/COLDWAR_EC/` (Ubuntu 13–20 px, Share Tech Mono 13–30 px, weiße Glyphen, Farbe aus der `.gfx`), genau wie in der freigegebenen Visualisierung. Grund: HOI4 multipliziert Glyphe × Textfarbe; die MD-Atlanten haben Schatten und Farbe eingebacken und sahen im Fenster grau und gedrängt aus. Lizenzen (Ubuntu Font Licence, SIL OFL) liegen bei den Schriften. Auf Wunsch zurück auf Orator/MD umstellbar (eine Tabelle im Generator).

**Design-Verbesserungen am Blau:**
1. Navy-Kopfband mit goldener Haarlinie darunter (Farben der Europaflagge); das Emblem größer, links.
2. Abschnittstitel als schmale Navy-Leisten mit Orator-Großbuchstaben, wie HOI4-Panels; darunter weißes „Journal"-Papier mit feinen blauen Linien.
3. Pro Karte nur das Wichtigste; Zahlen und Details per Hover (natives `pdx_tooltip`).
4. Feste Farbsprache: Grün = For/Adopted/Gewinn, Rot = Against/Rejected/Preis, Gold = läuft (Frist), Grau = passiv (KI).
5. KI-Mitglieder als kleine graue Flaggenreihe „Passive members", Spieler groß mit Stimme. Das spart Platz und zeigt, wer entscheidet.
6. Fristen als Gold-Balken mit Resttagen („Ratification · 120 days").
7. Stempel ADOPTED / REJECTED / RATIFIED größer, Schreibmaschinen-Schrift.

**Reiter:**
- **Council:** laufende Abstimmung (Aktenzeichen, Titel, Grundlage, Verfahrensleiste, Gewinn/Preis, Balken mit Schwelle unter Spielern, Spieler-Stimmen, passive Mitglieder); rechts Warteschlange und laufende Fristen.
- **Parliament:** Halbrund nach Delegationen (Spieler farbig nach Stimme, passiv grau), Rechte-Leiter, eigene Delegation mit For / Against / Abstain, Fraktionen als Info-Leiste.
- **Proposals:** Kapitel A–E, sechs Einträge je Seite; rechts Verfahren, Fristen, Gewinn und Preis, Knopf „Request from the Commission" bzw. „Table Proposal".
- **Programmes:** laufende Projekte und Hilfsprogramme mit Fortschritt; rechts der Katalog P1–P8 und der Programm-Baukasten (Empfänger, Art, Größe, Gegenleistung, Kosten).
- **Community:** Länderliste (Status, Gewicht, Sitze, Zustimmung, Saldo), „Who pays whom", Haushaltsanteile, Teilnahme, Besitzstand, eigene Aktionen.

---

## 15. Technik

**Dateien** (Generator `Claude outputs/COLDWAR_EC_generator/`, `run.py` baut und prüft; Liste und Hooks in `claude/mdcw_ec_1970_implementation.md`):
- `common/scripted_effects/COLDWAR_EC_1970_{effects,procedures,catalogue,budget,programmes,ui}.txt`, `common/scripted_triggers/COLDWAR_EC_1970_triggers.txt`
- `common/scripted_guis/COLDWAR_EC_1970.txt`, `common/scripted_localisation/COLDWAR_EC_1970_scripted_localisation.txt`, `interface/COLDWAR_EC_1970.gui/.gfx`, `gfx/interface/coldwar_ec/`, `gfx/fonts/COLDWAR_EC/`
- `common/ideas/…`, `common/dynamic_modifiers/…`, `common/opinion_modifiers/…`, `common/game_rules/…` (alle `COLDWAR_EC_1970_*`)
- `events/COLDWAR_EC_1970_events.txt`, `common/on_actions/zzzzzzzz_COLDWAR_EC_1970.txt`, `localisation/english/COLDWAR_EC_1970_l_english.yml`
- Aktionen der Spieler (Beitritt, Austritt, Referendum, Kampagnen, Teilnahme) laufen über Knöpfe im Fenster, nicht über Decisions.

**Zustand:** Ratsspur mit Vorgangsnummer; Vorgangsliste (Phase, Frist, Beteiligte); Projekte und Programme als Arrays; je Land Status, Gewicht, Sitze, Zustimmung, Saldo, Teilnahme-Flags; globale Flags `COLDWAR_EC_passed_<id>`.

**MP-Sicherheit (M6/C15):** `player_context`, `dirty`, `is_ai = no` im `visible`, keine Effekte in Triggern, erneute Prüfung bei jedem Klick; KI-Länder sehen keine Knöpfe, ihre Schritte laufen nur über Fristen.

**Schnittstelle für Länderbäume:** `COLDWAR_EC_submit_application`, `COLDWAR_EC_request_association`, `COLDWAR_EC_change_support`; Trigger `COLDWAR_EC_is_member`, `_is_candidate`, `_is_associate`, `COLDWAR_EC_democratic_clause`, `COLDWAR_EC_participates_<teil>`.

**Ersatz der MD-EU:** `# COLDWAR`-Hook in `on_startup_euu_action`: im 1970-Szenario `GAME_RULE_eu_disabled` setzen, MD-Start überspringen (Umfang im Code bestätigen).

**Rückbau Stufe 1:** Hooks mit `COLDWAR_EC_*`-Triggern zurück auf MD; vorher mit `backup_stage1` vergleichen (Änderungen anderer am 20. und 23.10.2026); MD-Bugfixes können bleiben.

**Andockpunkte:**
- SPR `SPR_1970.227` → `COLDWAR_EC_submit_application` (nur wenn SPR ein Spieler ist; als KI passiert nichts)
- GRE taut auf; CYP-Fokus → `COLDWAR_EC_request_association`
- D8 an `global.cc_chair`
- Hilfsprogramme an den Cold-War-Programmrahmen (§11)

**Aufwand (Schätzung):**
- Stufe 1, ca. 3 Wochen: Kern, Verfahren, Fristen, Parlament, Katalog A–E, Haushalt, Darlehen, Emblem, Fenster
- Stufe 2, ca. 1,5 Wochen: Projekte P1–P8, Hilfsprogramme mit Cold-War-Anbindung, Gerichtshof, Kalibrierung

---

## 16. Offene Fragen

1. **Mehrheit unter wenigen Spielern:** 70,5 % der Spieler-Gewichte (bei drei Großen faktisch Einstimmigkeit) oder eine niedrigere Spieler-Schwelle, z. B. 60 %?
2. **Quorum:** mindestens zwei Spieler-Stimmen für Mehrheitsbeschlüsse?
3. **Regierungskonferenz:** 180 Tage (historisch) oder 90?
4. **Kommissionskalender** als Game Rule standardmäßig an?
5. **Haushalt H1** (Nettosaldo im Geldsystem) wie beschrieben?
6. **Kapazität über der Grenze:** Spieler wählt binnen 7 Tagen, sonst endet das neueste Programm (Vorschlag). Oder sofort automatisch das neueste?
7. **Kapazitätsabzug** für alle Mitglieder (wie gewünscht) oder nur für die, die For gestimmt haben?
8. **Stufe 1** freigeben?

Entschieden mit den Rückmeldungen vom 29.10.2026:
- Look „Official Journal" mit MD-Schriften.
- Das Parlament ist dabei.
- Die KI ist passiv.
- Es gibt keine Datumssperren, dafür Bürokratie-Fristen.
- Wiederkehrendes läuft ohne Enddatum in seinem Takt.
- Die Kommission wird im Einvernehmen ernannt.

---

## 17. Quellen

- Stimmgewichte: [CVCE](https://www.cvce.eu/content/publication/2004/5/13/091ecbcb-7f7d-4772-ac95-9c51b041a7ff/publishable_en.pdf)
- Präsidentschaften: [Penguin Companion to the EU](https://penguincompaniontoeu.com/?p=683)
- EGKS-Flagge: [Wikipedia](https://en.wikipedia.org/wiki/Flag_of_the_European_Coal_and_Steel_Community)
- Europaflagge: [Rat der EU](https://www.consilium.europa.eu/en/infographics/european-flag/)
- Fraktionen: [CVCE](https://www.cvce.eu/content/publication/1997/10/13/35c2d1b5-1661-4c33-a65a-db49ade0c5ac/publishable_en.pdf)
- JET: [Wikipedia](https://en.wikipedia.org/wiki/Joint_European_Torus)
- Vertragsartikel: EWGV 1957 (113, 144, 148, 149, 152, 189, 201, 203, 235–238), Fusionsvertrag 1965 (11, 14), Einheitliche Akte, Unionsvertrag (189b)
- Schriften: `hoi_16mbs.fnt`/`hoi_18mbs.fnt` (face „Ubuntu", bold), `hoi_24header.fnt`/`hoi_36header.fnt` (face „Orator Std HoI Medium"), `hoi_16typewriter.fnt` („Times New Roman"), HOI4-Installation; Nutzung in `interface/eu.gui`
- Cold-War-Programme: `claude/mdcw_cold_war_spec.md` §4, `claude/mdcw_coldwar_imperia_hooks.md` §F
- Team-Referenz: `tools/comecon/README.md`, `docs/design/comecon/COUNCIL_ELECTION.md`
- Daten und Referenden: `claude/mdcw_ec_1970_history_report.md`
