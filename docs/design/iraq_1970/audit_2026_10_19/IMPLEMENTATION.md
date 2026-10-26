# Irak-Audit: umgesetzte Revision vom 19. Oktober 2026

**Korrekturstand v2:** Alle fünf Befunde aus [POST_IMPLEMENTATION_REVIEW.md](POST_IMPLEMENTATION_REVIEW.md) sind im Generator und in den geladenen Dateien behoben. Die ursprünglichen Gegenfälle wurden erneut gegen die installierten Provider ausgeführt. [POST_REVIEW_FIXES.md](POST_REVIEW_FIXES.md) und [POST_REVIEW_INSTALLED_TESTS.json](POST_REVIEW_INSTALLED_TESTS.json) enthalten Änderungen und Prüfergebnisse.

Die freigegebenen festen Änderungspakete aus [AUDIT.md](AUDIT.md) sind im geladenen Mod umgesetzt. Auch die vier dort qualitativ beschriebenen Wirtschafts-/Vertragskonflikte haben konkrete Kosten, Vorteile, Nachteile und Entscheidungen erhalten. Das ursprüngliche Audit bleibt als freigegebener Entwurf erhalten; dieser Bericht beschreibt den tatsächlich implementierten Stand.

**Aktive Spielinstallation erneut geprüft:** `mod/mdcoldwar.mod` zeigt auf diesen Projektordner; die tatsächliche Benutzer-`dlc_load.json` aktiviert diese Mod. Irak lädt den Baum direkt aus seiner 1970-Historie einschließlich der Start-Spirits; der Generic-Fallback nimmt Irak ausdrücklich aus. Die 103 generierten Dateien und neun Integrationen wurden erneut byte-identisch gebaut und geprüft. Ein vollständiger Neustart von HOI4 lädt diese Dateien; die Vorschau ist kein Installationsschritt. Der erneute automatisierte Startversuch mit genau diesem Manifest endete nach 196,2 Sekunden vor den Irak-Prüfmarken. Es wird weiterhin kein erfolgreicher vollständiger Ingame-Start behauptet.

Der Baum enthält **410 aktive Irak-Foki in 23 Kapiteln**. Alle 426 bisherigen IDs bleiben registriert; 16 zusammengelegte Verwaltungs-/Lieferkarten sind unsichtbare, unbelohnte Kompatibilitätseinträge. Beim US-Baum bleiben die 214 ursprünglichen Foki erhalten. Der Golfabschnitt hat 14 aktive Karten und einen verborgenen alten Kontakteintrag. Alle neuen Spieltexte sind Englisch.

Eine eigene begrenzte Shatt-Kriegs-/Friedensroute war im Audit ausdrücklich erst nach Entwurf eines beiderseits ausführbaren Friedensvertrags vorgesehen. Sie wird hier **nicht als fertig implementiert behauptet**: Die neutrale Aufklärung und die gemeinsamen Vorbereitungen sind vom Arabistan-Anspruch gelöst; der bestehende territoriale Ultimatum-/Core-Pfad verlangt weiterhin die ausdrückliche Gebietsforderung. Es wurde kein wirkungsloser zusätzlicher Friedensfokus eingesetzt.

## Die sechs verbindlichen Wahlpaare

Die Werte ersetzen ihre bisherigen Paketwerte. Dauerhafte Programme folgen der aktuell gewählten Politik und der zuständigen Regierung; gebaute Anlagen, XP, Alphabetisierung und Forschungsboni sind einmalige Lieferungen. Prozentuale BIP-Preise sind einmalige Kassenkosten. Forschung verwendet begrenzte native Boni ohne zusätzlichen Ahead-of-time-Bypass.

| Wahl | Aktuelles Paket | Dauer / Preis |
|---|---|---|
| Basic Industries First | Eine Zivilfabrik in Baghdad 557; 1×35% Industrieforschung; +10% Effizienzmaximum, +5% Militärfabrikleistung; +2% relativer Konsumgüterfaktor | 49 Tage / 5% BIP |
| Consumer Expansion | Eine Zivilfabrik in Nineveh 166; +8% Baugeschwindigkeit; +2% Bürokratiekosten | 49 Tage / 4% BIP |
| A Professional Core | +8% Organisation, 25 Armee-XP; +6% Armee-Personalkosten | 35 Tage / 1% BIP |
| A Mass Reserve Army | +15% relativer Wehrpflichtfaktor, +8% Erholung, 25 Armee-XP; −3% Organisation | 35 Tage / 1% BIP |
| Presidential Guard | +3% Organisation, +4% Verteidigung; +10% Armee-Personalkosten | 35 Tage / 2% BIP |
| The Regular Army | +6% Erholung, −8% Ausbildungszeit; +4% Armee-Personalkosten | 35 Tage / 2% BIP |
| Mass Literacy | +6 Prozentpunkte Alphabetisierung; +3% Sozialausgaben; spätere Abendkurse bleiben +2 Punkte | 35 Tage / 2,5% BIP |
| Train Teachers First | +5% Forschung, 1×25% Industrieforschung; +3% Sozialausgaben; späterer Lehrereinsatz bleibt +3,5 Alphabetisierungspunkte | 35 Tage / 2,5% BIP |
| An Oil Revenue State | Eine Infrastruktur in Basra 171; +18% tatsächlicher Ölexportertrag; −3% Steuerertrag | 49 Tage / 3,5% BIP |
| Beyond Oil | Eine Zivilfabrik in Baghdad 557; +8% Baugeschwindigkeit; −3% Ölexportertrag | 49 Tage / 4% BIP |
| National Front | +10% Effizienzaufbau, +4% Forschung; +3% Bürokratiekosten; aktive Frontrechte erforderlich | 35 Tage / 1% BIP |
| Exclusive Party State | +15% politischer Machtgewinn, +15% ideologische Abwehr; −3% Forschung | 35 Tage / kein BIP-Preis |

Die bisherigen zusätzlichen Fabrik-/Terminalkarten sind in das jeweilige Paket integriert. Strom, Infrastruktur und gewöhnliche spätere Entwicklung bleiben gemeinsam erreichbar. Die Wahl betrifft die Investitionspriorität, nicht ein lebenslanges Verbot gewöhnlicher Entwicklung.

## Vollständige Audit-Abdeckung

| Auditpunkt | Implementiertes Ergebnis |
|---|---|
| Reine Verwaltungs-/Prüfmalus-Einstiege | Defence Accounts, Literacy Accounts und Industry Survey entfallen als spielbare Schritte. Entscheidungen liegen an den echten Reformen. |
| Maintenance + Quality | Ein 35-Tage-/2%-BIP-Paket: +8% Effizienzaufbau, +2% Effizienzmaximum, −1% Militärfabrikleistung, +2% Bürokratiekosten. |
| Ausbildungsfolgen im Ölsektor | Ingenieurausbildung: 1×35% Industrieforschung und +2% Effizienzaufbau. Bedienerausbildung steckt in Baiji: +6% Treibstoffgewinn, +2% Effizienzaufbau, +2% Bürokratiekosten. |
| Politische Endpunkte | State Compact und Baath Future verlangen die tatsächlichen Gesamtreformen. Andere Abschlüsse folgen ihrem eigenen politischen Gegenstand statt einer beliebigen Nebenarm-OR-Bedingung. Bakrs Nachfolgeschritt dauert 21 Tage und bewirkt den Übergang. |
| Unterschiedliche Institutionen | ICP: +5% Militärfabrikleistung/+3% Sozialkosten. Aziz: −4% Bürokratie/+3% Steuern. Civic: +6% Steuern/−3% Bürokratie. Royal: +8% Einfluss/+2% Bürokratie. KDP: −5% Armee-Personal/+3% Bürokratie bei gültigen Nordgarantien. PUK: +8% Effizienzaufbau/+2% Sozialkosten. Dawa: +4% Forschung/+3% Sozialkosten. SCIRI: +3% Organisation/+4% Armee-Personal. IIP: +6% Effizienzaufbau/−2% Steuern. |
| Saddam-Abschluss | +8% politischer Machtgewinn, −3% Bürokratie, −2% Steuern; kein weiteres am Stabilitätsdeckel verlorenes Schlussgeschenk. |
| Opposition vor Regierungsantritt | Legalisierung, Frontgespräche und bezahlte unabhängige ICP-Organisation sind beim amtierenden Regime erreichbar. Koalitionsbeteiligung ändert nicht automatisch die herrschende Partei und vergibt keine kommunistischen Regierungsprogramme. ICP-/Aziz-Regierungsfoki behandeln anschließend Kabinett, Kader und Institutionen. |
| Verfassungsentscheidung | Ein aktuell geltender Exekutiv-/Repräsentativvertrag mit kostenpflichtiger Revision: 1% BIP und 100 PP. Abhängige Regierungsprogramme folgen dem gültigen Vertrag. Keine pauschale lebenslange Sperre aller anderen Parteienbäume. |
| Front-/Monopolfolgen | Bezahlte 180-Tage-Arbeitscharta: +5% Effizienzaufbau/+2% Sozialkosten, 1% BIP, nur bei gewahrten Frontrechten. Monopol-Mobilisierung: +5% PP/+2% Bürokratie, 1% BIP, 180 Tage. Sie sind keine gleichzeitig sammelbaren Vertragsboni. |
| Garde-/Generalstabsfolgen | Verschiedene nationale Programme und Folgeschritte; bezahlte Prioritätsrevision für 1% BIP ohne erneute ursprüngliche XP-/Sachlieferung. |
| Öl-Umsetzung vor Ausbau | National Oil Service bei (42,17) bzw. tatsächlich akzeptierte Konzessionslieferung bei (48,17). Train Iraqi Oil Engineers folgt als OR bei (45,18). Sovereign Accounts endet bei (45,23). |
| IPC-Eigentumskonflikt | Neue Verstaatlichung: 90 Tage −8% Ölexportertrag/+2% Bürokratie als Absatzumstellung. Kein nachträglicher Störmalus für alte Verstaatlichungen. Tatsächlich akzeptierte Konzession: zusätzlich eine Infrastruktur in 171 und 1×25% Industrieforschung; die bestehende echte Vertragsgebühr von 1% BIP an ENG bleibt die einzige Gebühr. Ablehnung liefert nichts. |
| Öl-Prioritätsprüfung | Bezahlter Wechsel zwischen Exporterlös- und Diversifizierungspriorität; keine Rückabwicklung der Verstaatlichung und keine erfundenen Konzessionsrechte. Keine erneute Fabrik. |
| Kooperativen/Kleinbauern | Kooperativen: 49 Tage, 4% BIP, +12% Agrarproduktivität/+3% Bürokratie, bisheriger Wasit-Agrarbezirk 1141 integriert. Kleinbauern: 35 Tage, 2,5% BIP, +8% Agrarproduktivität/−2% relativer Konsumgüterfaktor/+2% Sozialkosten. Wasser, Kliniken und gemeinsame Bewässerung bleiben von beiden Seiten erreichbar. |
| Nordvertrag | Reale KUR-/PUK-Zustimmung bzw. inländische Delegierte, wenn diese Länder fehlen. Einnahmenteilung: 2% BIP, −5% zentraler Steuerertrag/+2% Bürokratie und bestehende stärkere föderale Entlastung. Zentrale Verwaltung mit Garantien: 2% BIP, +3% Armee-Personal/+1% Bürokratie und bestehende schmalere Autonomieentlastung. |
| Nordvertrag: Abgrenzung | Einnahmenteilung ist eine zentrale Ertragsabstraktion, keine vorgetäuschte regelmäßige Einzahlung in eine fremde Staatskasse. Der stärkere Weg benutzt die bestehende föderale Regelung. KDPs gemeinsamer Abschluss heißt A Common Republic und behauptet bei gewöhnlicher Autonomie keine automatische föderale Verfassung. |
| Sowjetstandardisierung/Lieferantenmix | Standardisierung: −10% Versorgungsverbrauch/−3% Einfluss, 2% BIP. Mix: 1×35% Flugzeugforschung/+3% Versorgungsverbrauch, 2% BIP. Erste bezahlte akzeptierte französische oder britische Beratermission: zusätzlich 1×25% Artillerieforschung einmalig; tatsächliche Zustimmung, Kosten und Unterhalt bleiben erforderlich. |
| Gemeinsame Iran-Vorbereitung | Golfkredit- und Lieferantenzugang liegen im Southern War Plan. Beide 21-Tage-Hilfskarten sind zusammengelegt. Kurzkrieg/Durchhalten bleiben operative Alternativen; der lange Krieg verliert dadurch keinen normalen Finanzierungszugang. |
| Neutrale Iran-Aufklärung | Direkter Zugang vom Grenzlagefokus; bei (98,16) neben Anspruchskarten, ohne Verbindung durch die Arabistan-Karte. Zeitneutrale Beschreibung funktioniert auch vor 1979. Eine echte spätere Krise bleibt Bedingung der entsprechenden Zusatzentscheidung. |
| Titel/Bilder | Commercial Services nutzt das MD-Bürobild, Power Dispatch das Stromnetz. Saddam-Porträt bleibt für die Führung; Stab, Technokraten, Diplomatie und Iran-Dossier haben Themenbilder. Credit from Territory heißt Regional Debt Settlement und behauptet keine Gebietslieferung. |
| US-Kontaktverwaltung | Kontakte und Appell stecken in Open Northern Channels, 21 Tage. Humanitäre Hilfe und Zugang bleiben eigenständige Einstiege; Desert Storm bleibt ein direkter 14-Tage-Krisenfokus. |
| Zwei US-Endzustände | Eine aktuelle, bezahlte Verpflichtung: anerkannte ausgehandelte Autonomie oder externe De-facto-Schutzhaltung. Wechsel nur durch echte neue Zustimmung, 100 PP und $0,25 Mrd.; keine doppelten widersprüchlichen Endboni. |

## Forschung, Ausbildung und ganze Routen

| Fokus/Entscheidung | Aktueller Ertrag |
|---|---|
| Machine-Tool Skills | 2×35% Industrieforschung; +3% Effizienzmaximum; 2,5% BIP |
| Technical Colleges | 1×50% Bauforschung und 1×25% Industrieforschung; +3% Sozialkosten; 3% BIP |
| Air Maintenance | 1×35% Flugzeugforschung und 15 Luft-XP; +2% Bürokratie; 2,5% BIP |
| Staff Training | 35 Armee-XP und 1×25% Landdoktrin-Kostenreduktion; +4% Ausbildungszeit; 2% BIP. Der alte zusätzliche +3%-Organisationsbonus entfällt. |
| Readiness Cycle | 0,5% BIP; 90 Tage +4% Organisation/+4% Erholung/+4% Armee-Personal; 180 Tage Abklingzeit; keine wiederholbaren XP |

Die beiden im Audit definierten kompatiblen Militärbeispiele erreichen einschließlich Bereitschaft genau die konsolidierten Zielbeiträge: Garde-Route +20% Organisation/+7% Erholung/+4% Ausbildungszeit/+31% Personalkosten; reguläre lange Kriegsroute +25%/+16%/−4%/+72%. Das sind additive Beiträge der benannten Route, keine fertigen Divisionswerte. Start-Spirits, Technologien, Gesetze und automatische Iran-Kriegskostentiers sind davon getrennt. Der bestehende Stabilitätsdeckel bleibt; ein neuer versteckter Kampfwertdeckel wurde nicht eingeführt.

Die Kategorien wurden gegen echte 1970-Technologien und die aktuelle MD-Registry geprüft. Beispielsweise bekommt die Öl-Ausbildung Industrie statt einer erst später nutzbaren Raffineriekategorie. Ein im konkreten Spielstand vollständig erforschter Bereich kann selbstverständlich keine weitere noch offene Technologie verbilligen.

## Iran, Kuwait und amerikanische Reaktion

Die bestehende tatsächliche Iran-Kriegskosteneskalation bleibt erhalten: anfangs +100% Armee-Personalkosten/+50% native Ausrüstungskosten, nach 180 Tagen +175%/+100%, nach 365 Tagen +250%/+150%. Normale MD-Budgetabrechnung und Defizitaufnahme erzeugen die echte Finanzierungslast. Es wird keine zweite pauschale Rechnung für denselben Verbrauch aufgesetzt.

Der lange Krieg und erhebliche tatsächliche Neuverschuldung können die bestehende Nachkriegskrise auslösen: −30% Baugeschwindigkeit, −20% Steuerertrag, −10 Stabilitätspunkte, +2 Zinsaufschlagspunkte und +20% relativer Konsumgüterfaktor. Echte arabische Kreditgeber, Forderungsverweigerung, Ultimatum, Kuwait-Kriegsgrund, Eroberungsentlastung und bezahlte stabile Integration bleiben erhalten. Die Khuzestan- und Kuwait-Core-Bedingungen werden nicht durch einen bloßen Fokusabschluss ersetzt. Die vorhandenen Gegenleistungen sind damit weiterhin große Kampagnenziele.

Die USA behalten den echten 14-Tage-Desert-Storm-Kriegsgrund nach einem tatsächlichen irakischen Angriff auf Kuwait. Anerkannte Autonomie kostet die neue US-Entwicklungsverpflichtung $0,025 Mrd./Woche. Akzeptierte lokale Verwaltungen erhalten +8% Baugeschwindigkeit/+3% Bürokratie; Irak erhält bei gewahrter Regelung −8% Armee-Personal/−2% Steuern. Externer Schutz verwendet den vorhandenen einzelnen $0,05-Mrd./Woche-Schutzetat und gibt zustimmenden selbständigen Verwaltungen zusätzlich +5% Verteidigung gegen IRQ/+5% Armee-Personal. Bereits bestehende bezahlte Berater-/Luftverbindungen bleiben gesondert und sind in [US_IMPLEMENTATION.md](US_IMPLEMENTATION.md) zusammengezählt.

Aktuelle tatsächliche Kämpfe zwischen Irak und einem geschützten zustimmenden Akteur können einen bezahlten 60-Tage-Befreiungskriegsgrund öffnen: 100 PP und $0,50 Mrd. Kriegserklärung bleibt Spielerentscheidung. Die begrenzte US-Haltung reduziert echte Flüchtlingshilfe von $0,025 auf $0,020 Mrd./Woche; Bewaffnung erfordert weiterhin reale Abgaben und Zustimmung. Northern Air Shield benutzt vorhandene Luft-/Empfängermodifikatoren und tatsächlichen Zugang/Kräfte; es behauptet keine geografisch erzwungene Flugverbotszone.

## Bestehende Spielstände und saubere Transaktionen

`approved_iraq.json` bleibt unverändert. `audit_design.py` wendet die aktuelle freigegebene Revision auf eine Kopie an; `current_design.json` zeigt die tatsächlich generierte Form. Historische Ereignisnummern sind fest registriert: alle 115 alten Entscheidungsereignisse bleiben an ihrem Zweck, 14 neue benutzen reservierte Nummern ab 10000. Neue Menüs verschieben keine gespeicherten alten Antworten auf andere Ereignisse.

Die Versionsmigration erkennt tatsächliche erfolgreiche Lieferbelege, nicht nur abgeschlossene Fokusabzeichen oder Programmflags. Bereits gebaute Fabriken bleiben erhalten und werden nicht nochmals geliefert. Alte 15 Stabs-XP ergeben nur 20 zusätzliche XP; alte +2,5 Alphabetisierungspunkte ergeben nur +3,5 weitere. Neue Forschung wird einmalig separat verbucht. Neue oder geänderte Entscheidungszugänge werden auch bei schon früher reparierten Spielständen wiederhergestellt.

Unbezahlte alte positive Angebote werden einmal anhand ihres ursprünglichen BIP auf das neue Paket umgerechnet. Bei bezahlten Teilprojekten zählt der tatsächlich gespeicherte Rechnungsbetrag: etwa neues Gesamtpaket 1,0 minus belegte historische Zahlung 0,2 = einmal eingefrorener Restpreis 0,8. Fehlende historische Rechnungen erzeugen keinen erfundenen Rabatt. Eine schon gelieferte Fabrik wird nicht wegen später gestiegenen BIP erneut finanziert. Reine zusätzliche Forschungs-/Balanceboni bereits finanzierter Programme bleiben nach dem festgelegten Upgradevertrag kostenlos. Ausstehende echte neue Arbeit erscheint als ausführbare Entscheidung mit erneut geprüften Kassen-, Regierungs-, Vertrags-, Besitz-, Kontroll- und Bauplatzbedingungen.

Parteiverlust bzw. Führungswechsel entfernt zuständige aktive Programmwerte; eine gültige Rückkehr stellt verdiente Werte wieder her. Die Ableitung spielt keine Fabriken, Erfahrung, Geld, Forschungsboni oder Ansprüche erneut ab. Eine politische Prioritätsprüfung ändert die aktuelle Politik und erfüllt nicht automatisch die Rechnung eines alten Bauprojekts.

## Nachweise und verbleibende Prüfgrenzen

Aktuelle Dateihashes, Prüfresultate und die eng begrenzte native Laufzeitprobe stehen in [IMPLEMENTATION_CHECKS.json](IMPLEMENTATION_CHECKS.json). Der manifestierte Umfang beträgt 103 generierte Dateien und neun eng begrenzte Integrationen. Alle 214 bestehenden US-Fokusdefinitionen sind gegen die Integrationsbasis erhalten. Neue MD-2000-Vergleiche und eine unabhängige Stichprobe der tatsächlich ausgegebenen Texte/Effekte sind in [REVIEW_IMPLEMENTED_AUDIT.md](REVIEW_IMPLEMENTED_AUDIT.md) dokumentiert.

Bestanden sind 15 Belohnungs-, 13 Struktur-, 22 Migration-/Transaktions-, 18 politische, 21 neue US-, 17 bisherige US-, 14 zusätzliche US-Gegenfall-, sechs Konzessions-, acht Kern-, 15 bisherige Entscheidungs-, neun Start-Spirit-, neun Präsentations- und zehn Metadaten-Szenarien sowie 75 Golfprüfungen. Die installierte Gegenprüfung wiederholt darunter acht neue Migrationsgruppen, sechs Konzessionsfälle, 14 US-Gruppen und acht Front-/Monopolzustände auf beiden Anzeigeflächen. Diese Prüfungen haben jeweils ihren beschriebenen Geltungsbereich; native API-Aufrufe im Interpreter sind ausdrücklich Grenzen des Tests. Sie beweisen keine gesamte Kampagnenökonomie oder Mehrspielerbalance. Für v2 wurde kein neuer nativer Spielstart durchgeführt; die frühere ungeklärte Startabbruch-Ursache bleibt offen.

16 aktualisierte native Asset-Render zeigen die installierten Koordinaten. Industrie, Öl, Iran und der neue US-Zweig neben den bestehenden Militärfoki wurden visuell gelesen. Die Render approximieren Verbindungen und Kartenstatus; sie sind keine HOI4-Screenshots. Ein Rohbreitenhinweis bei Regional Debt Settlement misst eine einzelne Zeile, nicht bestätigtes Abschneiden im nativen Spiel. Keine globale Schriftverkleinerung wurde dafür vorgenommen.

Die aktualisierte Gesamtansicht zeigt alle 410 aktiven irakischen und 228 aktiven US-Foki mit den tatsächlich installierten Effekten. Chromium hat alle 638 Detailansichten, Ziehen mit allen Maustasten, normales und horizontales Scrollen, Zoom am Mauszeiger, Minikarte, Durchquerung des gesamten Baums und Breiten 320/736/1024 geprüft. Es gab keine Browserfehler oder Seiten-/Bedienleistenüberläufe.

Die native Laufzeitprobe verwendet ein isoliertes Testprofil und einen nicht im Benutzer-Spielset aktiven Zusatzmod. Ihr exaktes Ergebnis und die getestete Manifestversion stehen im verlinkten Prüfbericht. Native Tooltipp-Hovers, langfristige Einnahmen-/Kriegskostenentwicklung, ein tatsächlicher alter Save-Load, KI-Spielverläufe und Mehrspieler-Synchronisation sind nicht vollständig geprüft. Andere bestehende Modfehler dürfen nicht als durch dieses Audit behoben gelten.

Der gezielte native Test um 14:35:52 bestätigte tatsächlich Baghdad 1 → 2 Zivilfabriken, eine Zahlung von 0,5 Mrd. bei synthetischem BIP 10 Mrd. und keinen zweiten Bau/keine zweite Zahlung. Dieser Lauf verwendete Manifest `ff7b7cb8c64877b27bd1a79826995eb497b9c7cd5d008067a2fb95f79da71eca`. Spätere Wiederholungen am nachgeführten Stand sind **kein finales Ingame-Pass**: vollständige Starts und ein gezielter Wiederholungsstart endeten vor den Prüfmarken; ein weiterer früher Test lieferte die Fabrik nicht. Die genauen zuletzt erreichten Marken bleiben in den JSON-Berichten. Die Absturzursache ist nicht zugeordnet. Der erste erfolgreiche Test wird deshalb nicht als Beweis eines fehlerfreien finalen Kampagnenstarts ausgegeben.

Während der Arbeit wurden die gemeinsame Parteianzeige und danach die irakische History außerhalb dieses Audit-Generators verändert. Die aktuelle Namens-/Icon-Vorlage wird nun rein lesend vom irakischen Generator wiederverwendet; alle 36 Schlüssel entsprechen exakt der gemeinsamen Ausgabe. Die neue History-Formatierung und die dort vermerkte vorübergehende Zurückstellung der Startarmeen bleiben erhalten. Ein erster gemeinsamer Unittest-Aufruf importierte wegen eines Python-Suchpfadkonflikts unbeabsichtigt den Vietnam-Compiler und generierte dessen aktuellen Quellenstand neu. Der Suchpfadfehler ist behoben; spätere gemeinsame Testläufe schreiben keine Länderinhalte. Unbekannte gleichzeitige Vietnam-Arbeit wurde nicht spekulativ zurückgesetzt. Eine Unverändertheit des gesamten Arbeitsverzeichnisses wird ausdrücklich nicht behauptet.

Die gewünschte Autorenregel ist tatsächlich in `mdcw-national-trees/SKILL.md`, dessen `project-contract.md` und `mdcw-modifier-audit/SKILL.md` gespeichert: Beide historisch begründeten exklusiven Programme sollen begehrenswert sein, unterschiedliche spürbare Ergebnisse bieten und ihre plausiblen Kosten oder Nachteile haben. Ganze kompatible Routen sind zu prüfen; gewöhnliche gemeinsame Entwicklung und schwierige historische Startbedingungen bleiben erhalten. Installierter Inhalt und unveränderte Skill-Metadaten wurden gegen die vorbereiteten Änderungen geprüft.
