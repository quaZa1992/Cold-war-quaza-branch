# Irak 1970: mehr Wirkung und bessere Entscheidungen

**Umsetzungsstand:** Die anschließend vom Nutzer freigegebenen festen Pakete sind implementiert. Aktueller Codeumfang, Werte, Migration und Prüfgrenzen: [IMPLEMENTATION.md](IMPLEMENTATION.md). Der folgende Text bleibt der ursprüngliche freigegebene Auditentwurf; seine damaligen Statusangaben sind historisch.

Stand: 19. Oktober 2026. **Audit und Änderungsvorschläge, noch keine Balance- oder Strukturänderung im geladenen Mod.** Geprüft wurden die 426 irakischen Foki und der ergänzte US-Golf-/Kurdistan-Abschnitt. Die Zahlen unten sind neue Balancevorschläge, keine historisch belegten Prozentwerte. Englische Fokustitel sind Vorschläge für die Spieloberfläche; dieser Bericht ist auf Deutsch.

## Urteil

Der Baum braucht vor allem **weniger kleine Verwaltungsschritte und stärker unterschiedliche Programme**. Er enthält bereits 46 exklusive Wahlpaare. Zusätzliche Gabelungen helfen nur, wenn sie einen echten Konflikt um Geld, Macht, Ausbildung oder eine Vertragsregelung ausdrücken.

Die auffälligsten Verteilungen: 148 Foki verändern Bürokratiekosten, 136 Stabilität und 88 politischen Machtgewinn. Dagegen gibt es nur fünf Foki mit Armee-XP und keinen direkten Technologie- oder Doktrinbonus. Ein Entscheidungspaket kann trotzdem einen echten Nutzen haben: Diese Zählung erklärt deshalb nicht jeden einzelnen Fokus als leer.

Khuzestan, Kuwait, die Schuldenkrise und der echte US-Kriegsgrund sind bereits große Kampagnenbelohnungen. Dort ist eine pauschale Erhöhung unnötig. Die normalen Wirtschafts-, Militär- und Regierungsprogramme müssen vorher interessanter werden.

## Zuerst entfernen oder zusammenlegen

| Fokus | Tatsächlicher unmittelbarer Ertrag | Empfehlung |
|---|---|---|
| `COLDWAR_IRQ_defence_accounts` | 21 Tage; ausschließlich +2 % Bürokratiekosten | In die Stabsausbildung integrieren. Falls als Einstieg behalten: 14 Tage, 20 Armee-XP, kein permanenter Verwaltungsmalus. XP nicht zusätzlich beim Zusammenlegen vergeben. |
| `COLDWAR_IRQ_society_literacy_accounts` | 35 Tage und 0,5 % BIP; ausschließlich +1 % Bürokratiekosten | Mit dem gewählten Bildungsprogramm zusammenlegen. Keine eigene Rechnung für eine reine Rechnungskontrolle. |
| `COLDWAR_IRQ_industry_survey` | 21 Tage; +2 % Bürokratiekosten und Zugang zur Projektprüfung | Prüfentscheidung mit dem Industrieeinstieg freischalten; die separate Karte entfällt. |
| `COLDWAR_IRQ_industry_maintenance` und `industry_quality` | Wiederholte kleine Effizienz-/Verwaltungsänderungen | Ein gemeinsamer 35-Tage-Fokus: +8 % Effizienzaufbau, +2 % Effizienzmaximum, −1 % Militärfabrikleistung, +2 % Bürokratiekosten; einmalig 2 % BIP. |
| `COLDWAR_IRQ_oil_technical_training` und `oil_operators` | Jeweils +2 % Effizienzaufbau und +1 % allgemeine Forschung | Ein echter Ausbildungsmeilenstein mit begrenztem Forschungsbonus; die spätere Bedienerausbildung in die Raffinerieentwicklung aufnehmen. |
| Routineprüfungen am Ende großer Zweige | Teilweise 49 Tage für eine weitere Prüfentscheidung | Prüfentscheidungen früher geben. Den Schlussfokus für ein neues Ergebnis verwenden oder mit der Reform zusammenlegen. |

Bestehende Fokus-IDs und einmalig erhaltene Belohnungen benötigen bei einer Umsetzung eine Save-Migration. Entfernen bedeutet nicht, bereits gebaute Fabriken rückgängig zu machen oder sie erneut auszuzahlen.

## Sechs konkrete, stärkere Wahlpaare

**Lesart:** Dauerhafte Programmwerte gelten nur bei der passenden Regierung und ausgewählten Politik. Fabriken, XP, Alphabetisierung und verbrauchte Forschungsboni sind einmalige Ergebnisse. Die vorgeschlagenen Pakete ersetzen die genannten alten Werte; sie werden nicht zusätzlich daraufgerechnet. BIP-Kosten sind einmalige Staatskassenkosten, getrennt von laufenden Ausgaben. Folgefoki bleiben nur erhalten, wo ausdrücklich genannt.

### 1. Basic Industries First / Consumer Expansion

**Heute:** Heavy Industry plus Industrial Workshops kostet 84 Fokustage und 7 % BIP: eine Zivilfabrik, +3 % Effizienzmaximum, +2 % Konsumgüterfaktor. Light Industry plus Consumer Industry kostet ebenfalls 84 Tage und 5,5 % BIP: eine Zivilfabrik, +3 % Effizienzaufbau, −2 % Militärfabrikleistung. Der zentrale Industriekonflikt wirkt viel kleiner, als seine Namen versprechen.

**Vorschlag: je ein zusammengelegtes 49-Tage-Programm.**

| | Basic Industries First | Consumer Expansion |
|---|---|---|
| Einmalige Lieferung | 1 Zivilfabrik in State 557; 1 × 35 % Industrieforschung | 1 Zivilfabrik in State 166 |
| Laufender Vorteil | +10 % Effizienzmaximum; +5 % Militärfabrikleistung | +8 % Baugeschwindigkeit |
| Kleiner laufender Nachteil | +2 % relativer Konsumgüterfaktor | +2 % Bürokratiekosten |
| Einmaliger Preis | 5 % BIP | 4 % BIP |

Die bestehende jeweilige Fabrik wird **in das Paket verschoben**, nicht verdoppelt. Strom, Transport und spätere normale Investitionen bleiben gemeinsam. Exklusiv ist die erste staatliche Investitionspriorität samt ihrem laufenden Schwerpunkt; nicht die Existenz ganzer Industriezweige.

Historischer Anknüpfungspunkt: Diversifizierung, Grundstoffindustrie und Konsumproduktion konkurrierten um technische Kapazität und Umsetzungskapazität. Der zeitgenössische Bericht beschreibt sowohl Entwicklungsinvestitionen als auch deren Grenzen. Daraus leiten wir einen Spielkonflikt ab. [CIA-Länderstudie, November 1976, Wirtschaftsabschnitt](https://history.state.gov/historicaldocuments/frus1969-76v27/d317).

### 2. A Professional Core / A Mass Reserve Army

**Heute:** Berufskern +4 % Organisation / +6 % Personalkosten; Reserve +6 % relativer Wehrpflichtfaktor / −3 % Organisation. Beide dauern 35 Tage und haben hier keinen einmaligen BIP-Preis.

| Neuer 35-Tage-Fokus | Berufskern | Nationale Reserve |
|---|---|---|
| Vorteil | +8 % Organisation; 25 Armee-XP | +15 % relativer Wehrpflichtfaktor; +8 % Organisationserholung; 25 Armee-XP |
| Nachteil | +6 % Armee-Personalkosten | −3 % Organisation |
| Einmaliger Preis | 1 % BIP | 1 % BIP |

Der Berufskern belohnt kleinere, einsatzfähige Verbände. Die Reserve lohnt sich bei Verlusten und längerem Krieg. +15 % Wehrpflichtfaktor bedeutet **nicht** zusätzliche 15 Prozentpunkte der Bevölkerung. Bestehende Ausbildung/Logistik muss in der Gesamtbilanz mitgerechnet werden.

### 3. Presidential Guard / The Regular Army

**Heute:** Garde +3 % Organisation / +8 % Personalkosten; reguläre Armee +4 % Organisation / +5 % Ausbildungszeit. Die Garde erscheint wenig verlockend.

| Neuer 35-Tage-Fokus | Presidential Guard | The Regular Army |
|---|---|---|
| Vorteil | +3 % Organisation; +4 % Verteidigung | +6 % Organisationserholung; −8 % Ausbildungszeit |
| Nachteil | +10 % Armee-Personalkosten | +4 % Armee-Personalkosten |
| Einmaliger Preis | 2 % BIP | 2 % BIP |

Der bisherige zusätzliche +3-%-Organisationsbonus aus Staff Training entfällt zugunsten von XP und Doktrinkostenreduktion. Die reguläre Armee erhält hier keinen weiteren Organisationsbonus. Die Folgefoki zu Versorgung bzw. Stabsakademie bleiben eingerechnet. Diese Werte sind nationale Abstraktionen. Sie betreffen technisch nicht ausschließlich Gardedivisionen. Eine divisionsspezifische Sondertruppe wäre ein eigener, nachzuweisender Mechanikentwurf. Kein kostenloses Heer nach dem Vorbild von 1988 im Januar 1970.

Historisch ist der Konflikt zwischen Regimesicherung, privilegierten Formationen und professioneller militärischer Selbständigkeit belastbar. Das rechtfertigt die Prioritätswahl, nicht bestimmte Prozentwerte. [Zeitgenössische Länderstudie, Militärabschnitt](https://history.state.gov/historicaldocuments/frus1969-76v27/d317).

### 4. Mass Literacy / Train Teachers First

**Heute:** Massenkampagne +2,5 Prozentpunkte Alphabetisierung; Lehrerausbildung +2 % Forschung bei +3 % Sozialkosten. Beide dauern 35 Tage und kosten 2,5 % BIP.

| Neuer 35-Tage-Fokus | Mass Literacy | Train Teachers First |
|---|---|---|
| Vorteil | +6 Prozentpunkte Alphabetisierung sofort | +5 % Forschung; 1 × 25 % Industrieforschung |
| Nachteil | +3 % Sozialausgaben | +3 % Sozialausgaben |
| Einmaliger Preis | 2,5 % BIP | 2,5 % BIP |
| Bestehende spätere Lieferung | Abendkurse bleiben +2 Prozentpunkte Alphabetisierung | Einsatz der Lehrer bleibt +3,5 Prozentpunkte Alphabetisierung |

So entsteht eine echte Zeitentscheidung: frühe breite Entlastung der niedrigen Alphabetisierung oder zunächst bessere Bildungskapazität. Die dauerhaften Folgen der Alphabetisierung bleiben bei Regierungswechsel bestehen; das zusätzliche Regierungsprogramm darf nicht stapeln. Allgemeine Forschung bleibt hier eine bewusst begrenzte Ausnahme für landesweite Bildung, kein Standardbonus für jede Werkstatt.

### 5. An Oil Revenue State / Beyond Oil

**Heute:** Ölrente +8 % Ölexportertrag / −3 % Steuerertrag. Diversifizierung +3 % Baugeschwindigkeit / −3 % Ölexportertrag, einmalig 3 % BIP. Die jeweiligen Infrastruktur-/Fabrikfolgen stehen zusätzlich dahinter.

**Vorschlag: die gewählte Lieferung in ein 49-Tage-Paket aufnehmen.**

| | An Oil Revenue State | Beyond Oil |
|---|---|---|
| Einmalige Lieferung | 1 Infrastruktur in State 171 | 1 Zivilfabrik in State 557 |
| Laufender Vorteil | +18 % tatsächlicher Ölexportertrag | +8 % Baugeschwindigkeit |
| Nachteil | −3 % Steuerertrag | −3 % Ölexportertrag |
| Einmaliger Gesamtpreis | 3,5 % BIP | 4 % BIP |

Export Terminals bzw. Industrial Fund gehen in diese Programme ein; ihre vorhandene Lieferung darf **kein zweites Mal** ausgezahlt werden. Die Ölrente schafft keine Ölressourcen und hilft nur bei tatsächlichem Export. Diversifizierung kauft eine weniger exportabhängige Basis. Die echte Eigentumsentscheidung IPC-Verstaatlichung/Vertrag liegt davor und bleibt davon getrennt.

### 6. National Front / Exclusive Party State

**Heute:** Nationale Front +4 Prozentpunkte Stabilität / −2 % politischer Machtgewinn; Parteimonopol +6 % politischer Machtgewinn / −4 Prozentpunkte Stabilität. Das ist für zwei politische Ordnungen dürftig. Positive Programmstabilität wird zudem insgesamt bei +15 Punkten gedeckelt.

| Neuer 35-Tage-Fokus | National Front | Exclusive Party State |
|---|---|---|
| Vorteil | +10 % Effizienzaufbau; +4 % Forschung | +15 % politischer Machtgewinn; +15 % ideologische Abwehr |
| Nachteil | +3 % Bürokratiekosten | −3 % Forschung |
| Einmaliger Preis | 1 % BIP | keiner |

Diese Werte ersetzen die bisherigen Stabilitäts-/PP-Pakete. Die Front gewinnt einen konkreten wirtschaftlichen Nutzen aus eingebundenen Fachleuten; das Monopol gewinnt zentrale Handlungsfähigkeit. Beteiligungsrechte und spätere Kabinetts-/Gewerkschaftsentscheidungen müssen sichtbar verschieden bleiben. Der Kongress folgt erst der tatsächlich umgesetzten Frontcharta oder Parteikontrolle.

Historisch blieb reale Macht trotz Nationaler Front bei der Baath; die ICP war über die Beteiligung gespalten. Eine echte Teilhabe wäre deshalb eine bewusst alternative, ausgehandelte Entwicklung. Eine kommunistische Koalitionsbeteiligung darf nicht automatisch alle Boni einer kommunistischen Regierung freischalten. [CIA-Länderstudie, Parteienabschnitt](https://history.state.gov/historicaldocuments/frus1969-76v27/d317).

## Weitere gute Konflikte – politische Verträge statt weiterer Schablonen

Diese vier Themen sind historisch sinnvoll, aber noch keine abschließend bezifferten Ersatzpakete:

- **IPC verstaatlichen / Beteiligungsvertrag:** größerer langfristiger eigener Ertrag gegen vorübergehende Absatzprobleme und Abwicklungskosten; alternativ frühere Liquidität und eine tatsächlich akzeptierte technische Lieferung gegen fortdauernde ausländische Beteiligung. Kein erfundener dauerhafter technischer Zusammenbruch nach Verstaatlichung. Die zeitgenössische Bewertung sah vor allem Absatzrisiken. [CIA, Juni 1972](https://history.state.gov/historicaldocuments/frus1969-76ve04/d311).
- **Kooperative Mechanisierung / Kleinbauernkredit:** größerer Produktivitäts-/Maschinenpool gegen Verwaltung und Kapitaleinsatz; alternativ günstigere frühe ländliche Entlastung gegen weniger Skaleneffekt. Wasser, Wege und Kliniken bleiben gemeinsam. Die historisch nebeneinander bestehenden Betriebsformen werden nicht dauerhaft gegenseitig verboten.
- **Einnahmenteilung im Norden / zentrale Ölverwaltung mit akzeptierten lokalen Garantien:** größere Sicherheitsentlastung und Regionalentwicklung gegen einen geringeren Bagdader Einnahmenanteil; alternativ mehr Zentralertrag gegen kleinere Entlastung und höhere fortdauernde Sicherheitskosten. Kirkuk, Einnahmen und tatsächliche Zuständigkeiten gehören in den Vertrag. Dieser Konflikt war für das Scheitern der Autonomieverhandlungen wesentlich. [Colby-Memorandum, 21. März 1974](https://history.state.gov/historicaldocuments/frus1969-76v27/d243).
- **Sowjetische Standardisierung / Lieferantenmix:** bessere Ersatzteil- und Versorgungsökonomie gegen Abhängigkeit; alternativ zusätzliche konkrete technische Fähigkeit gegen teurere Lagerhaltung. Transfers brauchen tatsächliche Lieferungen und Zustimmung. Die bisherige kleine Fabrikeffizienz im Lieferantenmix ist kein überzeugender Ersatz.

## Was strukturell „weird“ ist

### 1. Zu oft dieselbe Schablone

22 der 23 Kapitel bestehen aus genau 18 Foki. Zwölf haben denselben logischen Aufbau: kleine Gabel, Zusammenführung, zweite kleine Gabel, Zusammenführung, drei Sammelarme, Abschluss. Das ist kein Positionsfehler, wirkt aber wie ein ausgefülltes Formular.

**Ändern:** Politische Hauptentscheidungen erhalten zwei bis vier Folgen mit eigenen Entscheidungen. Routinemäßige Verwaltung wird integriert. Kein festes Soll von 18 Foki pro Partei. Historisch relevante Parteien und Führer bleiben erhalten.

### 2. Große Abschlüsse schon nach einem Nebenarm

State Compact, Baath Future und mehrere weitere große Abschlüsse verlangen jeweils nur einen der drei gezeichneten Nebenarme. Eine einzelne Voraussetzungsklammer mit mehreren `focus`-Einträgen ist OR. Der Code ist gültig; die große Gesamtabschluss-Erzählung passt teilweise nicht dazu.

**Ändern:** Entweder eine echte Gesamtreform mit bewusstem AND und einer entsprechend starken Belohnung, oder ein politischer Abschluss nach der relevanten politischen Entscheidung. Nicht jeden Schluss zur sechs Foki langen Sammelpflicht machen.

### 3. Opposition erst nach der Machtübernahme

Kommunistische Frontstrategie, Untergrund und Aziz’ Road to Power verlangen bereits die ICP-Regierung; bei Aziz zusätzlich seinen tatsächlichen Amtsantritt. Parteibaum und Führerbaum wiederholen denselben strategischen Konflikt.

**Ändern:** Vorherige Legalisierung, Frontbeteiligung und Opposition bleiben beim amtierenden Regime als politische Entscheidungen erreichbar. Die Regierungsfoki behandeln danach Kabinettsrechte, Parteiorganisation, Rückkehr von Kadern und Wirtschaftsprogramme. Eine einzige Stelle besitzt die strategische Front-/Oppositionsentscheidung. Aziz bekommt deren eigene konkrete Umsetzung, keine Wiederholung des Parteieinstiegs.

### 4. Ölpolitik ohne tatsächliche Umsetzung

Die Ingenieurausbildung und spätere Ölentwicklung können derzeit bereits nach der Eigentumsentscheidung beginnen. National Oil Service oder der tatsächlich erfüllte Konzessionsvertrag müssen nicht umgesetzt sein.

**Konkrete Positionsänderung:** Beide Umsetzungsfoki bleiben bei (42,17)/(48,17). Train Iraqi Oil Engineers wird von (45,17) nach (45,18) verschoben und verlangt als OR **einen dieser zwei umgesetzten Wege**. Die Ausbildung und ihre zwölf nachfolgenden Ölfoki gehen eine Zeile nach unten; Sovereign Accounts endet dann bei (45,23). Fußabdruck x42–48/y15–23, weiterhin neben Industrie x50–55. Die Ablehnung eines Konzessionsangebots braucht eine eigene mögliche politische Reaktion; sie darf keine kostenlose Lieferung fingieren.

### 5. Kredite nur für den kurzen Krieg, Ersatzteile nur für den langen

Das sind zwei optionale 21-Tage-Sackgassen. Im Iran-Zweig liegt der eigene direkte Kreditzugang ausgerechnet am Kurzkriegsarm. Über Saddams separaten Kreditfokus kann auch ein anderer Freischaltungsweg bestehen; ein langer Krieg ist deshalb nicht grundsätzlich von Golfkrediten ausgeschlossen.

**Ändern:** Beide Verhandlungsfreischaltungen in Southern War Plan aufnehmen. Kreditgeberzustimmung, echte Kredite, Kosten und Lieferbedingungen bleiben erhalten. Kurzfeldzug und Durchhaltekrieg werden danach die eigentliche operative Wahl. Optional kann die bevorzugte Finanzierung eigene Bedingungen bekommen; normale Kredite und Steuern dürfen nicht historisch falsch gegenseitig verboten werden.

### 6. Begrenzter Krieg verlangt vorher die große Territorialforderung

Southern War Plan benötigt beide Vorarbeiten; die neutrale Einschätzung der iranischen Armee liegt hinter der Arabistan-Forderung. Selbst eine Shatt-Strategie muss dadurch zuvor Khuzestan verlangen.

**Ändern:** Neutrale Lagebewertung gemeinsam voranstellen. Danach eine explizite Wahl des Kriegsziels prüfen: begrenzte Grenzrevision oder Arabistan-Anspruch mit Besetzung/Integration. Die vorhandene starke Khuzestan-Core-Route bleibt beim expansiven Ziel erhalten. Eine begrenzte Kriegsroute ist erst fertig entworfen, wenn ihr echter, beiderseits ausführbarer Friedensvertrag und ihr Ertrag feststehen.

### 7. KDP-Autonomie endet trotzdem bei „Federal Republic“

Autonomie und Föderation schließen sich am Einstieg aus, aber der gemeinsame letzte Fokus heißt Federal Republic. Das ist mindestens ein bestätigter Textwiderspruch; er beweist für sich keine tatsächliche Verfassungsänderung.

**Ändern:** Neutraler gemeinsamer Abschluss wie A Common Republic; die gewählte Staatsordnung bleibt erhalten. Autonomievereinbarungen für Bagdad nicht hinter einer KDP-Regierung für ganz Irak verstecken.

### 8. Zehn politische Abschlüsse mit derselben Kleinbelohnung

Zehn 49-Tage-Abschlüsse geben +3 Prozentpunkte Stabilität und −2 % politischen Machtgewinn. Die positive Stabilität bringt nach Erreichen des gemeinsamen +15-Punkte-Deckels keinen zusätzlichen nationalen Stabilitätsbonus.

**Ändern:** Deckel behalten. Nachfolge, gültige Verfassung, akzeptierten Nordvertrag oder eine spürbare Institution belohnen. Routineüberprüfung verkürzen/integrieren. Nicht einfach +3 auf +10 erhöhen und weiterhin gegen denselben Deckel laufen lassen.

### 9. Einzelne Bilder und Namen passen nicht

- Commercial Services erzeugt Büros, zeigt aber ein großes Wohlfahrtsherz. Das vorhandene MD-Bild `generic_office_construct` passt; Registry und tatsächliche Textur wurden geprüft.
- Dasselbe Saddam-Porträt erscheint auf sechs unterschiedlichen Themen einschließlich Stabsausbildung und Iran-Dossier. Auf Präsidentschaft und echtem Führungsmeilenstein behalten, sonst thematische MD-Bilder verwenden.
- Credit from Territory ist tatsächlich eine zustimmungsabhängige Schuldenprüfung ohne Territorialeffekt. In Regional Debt Settlement umbenennen; Kuwait-Kriegsziele gehören in die ausdrückliche Nachkriegskrise.

### 10. Zwei US-Endzustände ohne klare politische Beziehung

Baghdad Accord und Guarantee Self-Rule sind beide sammelbar und führen über OR zur Erholung. Sie können eine zeitliche Entwicklung oder konkurrierende Verpflichtungen bedeuten – der Baum erklärt die Beziehung nicht.

**Ändern:** Eine aktuelle Haltung definieren: mit Bagdad vereinbarte Autonomie oder extern geschützte De-facto-Selbstverwaltung. Verpflichtungen, laufende Kosten und Eskalationsrisiko unterscheiden. Ein späterer Wechsel erfolgt durch tatsächliche Neuverhandlung statt durch doppelten Bonus. Humanitäre Hilfe bleibt unabhängig erreichbar; der 14-Tage-Desert-Storm-Zugang wird nicht verlängert.

## Mehr unmittelbare Wirkung ohne weitere Dauerboni

Native MD-Vorbilder zeigen, dass Forschung und Ausbildung selten nur aus +1 % allgemeiner Forschung bestehen müssen:

| Geplanter Irak-Fokus | Konkreter Ersatzvorschlag |
|---|---|
| Industry Machine Tools | Statt +1 % allgemeiner Forschung: 2 × 35 % Industrieforschung; +3 % Effizienzmaximum und 2,5 % BIP-Preis bleiben. Bei Zusammenlegung mit dem neuen Industriepaket zuerst den gesamten erreichbaren Forschungsbonusbestand prüfen. |
| Technical Colleges | Statt +3 % allgemeiner Forschung: 1 × 50 % Bauforschung und 1 × 25 % Industrieforschung; +3 % Sozialausgaben, 3 % BIP bleiben. |
| Air Maintenance | Statt +2 % allgemeiner Forschung: 1 × 35 % Flugzeugforschung und 15 Luft-XP; +2 % Bürokratie und 2,5 % BIP bleiben. |
| Staff Training | 15 → 35 Armee-XP; zusätzlich 1 × 25 % Landdoktrin-Kostenreduktion. Der bisherige +3-%-Organisationsbonus entfällt; +4 % Ausbildungszeit und 2 % BIP bleiben. Mit dem zusammengelegten Einstieg keine doppelte XP-Lieferung. |
| Readiness Cycle, wiederholbare Entscheidung | Heute 2 % BIP für 90 Tage +3 % Organisation / +4 % Personalkosten. Vorschlag: 0,5 % BIP für 90 Tage +4 % Organisation und +4 % Erholung / +4 % Personalkosten; bestehende 180-Tage-Abklingzeit. Keine wiederholbaren XP. |

Das sind Alternativen zur vorherigen Kleinteiligkeit, kein Aufruf, jeden Vorschlag ungeprüft auf alle bestehenden Foki zu addieren.

### Ganze Militärroute statt isolierter schöner Zahlen

Ein erster stärkerer Einzelentwurf wurde vor dieser Empfehlung verworfen: Zusammen hätte er bei kompatiblen Foki bis +32/+36 % Organisation einschließlich Bereitschaft erzeugt. Die oben konsolidierte Empfehlung nimmt den doppelten Stabsausbildungsbonus heraus und verteilt die Wirkung zwischen Organisation, Erholung, Ausbildung und einmaligen XP/Doktrinboni.

| Kompatible Beispielroute, jeweils mit Bereitschaft | Organisation heute → Vorschlag | Erholung | Ausbildungszeit | Personalkosten |
|---|---:|---:|---:|---:|
| Baath/Saddam, Berufsarmee, Garde, entsprechende Staats-/Verteidigungsfolgefoki | +18 → +20 % | +3 → +7 % | +4 → +4 % | +29 → +31 % |
| Baath/Saddam, Berufsarmee, reguläre Armee, langwieriger Irankrieg und entsprechende Folgefoki | +27 → +25 % | +6 → +16 % | +9 → −4 % | +68 → +72 % |

Die Zahlen sind additive Beiträge dieser konkreten Fokus-/Bereitschaftsrouten, keine finalen Divisionswerte. Startspirits, Technologie, Gesetze und automatische Kriegskosten sind nicht heimlich Teil der Prozentzahlen. Die genaue Fokusliste und Abgrenzung stehen im Mechanikbericht. Ein einzelner Organisationswert darf hier bewusst geringer werden, während die Route durch Erholung, Ausbildung, Doktrin und günstigere Bereitschaft wirksamer wird. Das ist keine pauschale Erhöhung sämtlicher Kampfwerte und kein neuer stiller Deckel.

## MD-2000-Referenzen und tatsächliche Mechaniken

Die Referenzen wurden in der aktuell installierten Hauptmod gelesen, nicht aus einer früheren Erinnerung übernommen. BIP-Preise des Irak sind eigene Vorschläge; deutsche oder israelische Dollarpreise aus 2000 werden nicht auf 1970 übertragen.

| Land / Fokus | Tatsächlicher Referenzertrag |
|---|---|
| Russland `SOV_military_education` | 21 Tage: 35 Armee-XP und native Offiziersausbildung |
| Russland `SOV_aero_improvements` | 21 Tage: 1 × 25 % Flugzeugforschung, −10 % Flugunfälle, 3 Mrd. $ |
| Israel `ISR_deliver_computers` | 35 Tage: 1 × 25 % IT-Forschung, 3 Mrd. $ |
| Israel `ISR_assam_ibrahims_mission` | Bei akzeptierter Zusammenarbeit: 25 Armee-XP, 15 Command Power, 1 × 25 % Spezialkräfte-Forschung, 1 × 25 % Landdoktrin-Kostenreduktion; −100 PP |
| Deutschland `GER_modernise_mining_equipment` | Geschriebene Kosten 6,5 Fokuseinheiten: 1 × 40 % Bauforschung, 10 Mrd. $ |
| Türkei `TUR_industrial_research` | Geschriebene Kosten 5,72 Einheiten: 2 × 50 % Industrieforschung |
| Türkei `TUR_turkish_agriculture` | 5,72 Einheiten: 1 Zivilfabrik und 1 × 25 % Genetikforschung |

`add_tech_bonus`, `add_doctrine_cost_reduction`, XP, bestehende nationale Modifikatoren und kontrollierte Bau-Lieferungen sind belegt. Passende Industrie-, Bau- und Flugzeugkategorien existieren auch in der 1970-Erweiterung. Ob im konkreten Spielstand noch eine passende Technologie offen ist, muss vor endgültiger Umsetzung geprüft werden. Kein zusätzlicher Ahead-of-time-Bypass.

Die MD-Budgetleser wurden für Bürokratie, Steuern, Armeepersonal, Ölexport und Konsumgüter geprüft. Wichtig für die Darstellung: +2 % `consumer_goods_factor` ist ein **relativer Faktor**, nicht +2 Prozentpunkte Steuersatz. Ein Exportbonus schafft keine Ölproduktion. Personalkosten betreffen die tatsächliche Lohnkomponente, nicht automatisch alle Militärausgaben. Die bestehende echte Iran-Kriegskosteneskalation bleibt unverändert.

## Reihenfolge einer Umsetzung

1. Reine Malus-/Prüffoki integrieren; falsche Voraussetzungen, Oppositionszeitpunkt und Namen korrigieren.
2. Sechs bestehende Wahlpaare neu bündeln; keine doppelten Fabriken, Forschung, XP oder Alphabetisierung bei Überprüfung/Regierungsrückkehr.
3. Front-/Monopol- sowie Garde-/Generalstabswege mit unterschiedlichen Folgeentscheidungen vertiefen; dadurch abwechslungsreiche Länge und Form.
4. Echte verfassungsrechtliche Konflikte über einen aktuellen Vertrag und kostenpflichtige Revision lösen. Keine pauschalen lebenslangen Sperren zwischen sämtlichen Parteienbäumen.
5. Kompatible aktive Routen inklusive Startspirits und Entscheidungen berechnen; 1970-Frieden und späteren tatsächlichen Iran-Krieg wirtschaftlich testen. Danach neue native Ansichten und Tooltips prüfen.

**Prüfgrenze:** Quellcode, vorhandene native Karten-/Art-Render und Mechanikleser sind geprüft. Keine neue Ingame-Tooltip-, Kampagnen- oder Mehrspieler-Balancebestätigung. Es wurden keine Kartenkollisionen oder fehlenden relativen Anker gefunden. Die vorhandenen Render sind Annäherungen mit nativen Assets, keine neuen Spiel-Screenshots.

Die interaktive Gegenüberstellung wurde im Browser mit allen sechs Programmpaaren und sechs Strukturausschnitten bei 320, 400, 560, 736 und 1024 Pixeln geprüft, einschließlich Zustandswechseln und Hell-/Dunkelansicht. Alle 97 generierten Paketdateien und der freigegebene Katalog entsprechen dem Beginn-Snapshot. Drei gemeinsam genutzte Integrationsdateien haben außerhalb dieser Audit-Schreiboperationen andere Hashes erhalten; sie wurden nicht zurückgesetzt. Deshalb wird keine Unverändertheit des gesamten gleichzeitig genutzten Arbeitsverzeichnisses behauptet. Nachweise: `BROWSER_QA.json` und `RUNTIME_SNAPSHOT_CHECK.json`.

Detailbelege: [Mechaniken und genaue MD-Dateianker](MECHANICS.md), [Struktur mit IDs und Koordinaten](STRUCTURE.md), [historische Begründungen](HISTORY.md). Die konsolidierten Industrie-/Ölpakete dieses Berichts verschieben die bestehende Lieferung ausdrücklich in den Schwerpunktfokus; sie präzisieren die Einzelwerte aus dem Mechanikbericht. Rohdaten und der Beginn-Snapshot stehen daneben.
