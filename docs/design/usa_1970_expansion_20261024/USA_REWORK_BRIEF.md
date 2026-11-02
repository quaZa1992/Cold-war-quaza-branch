IMPERIA COLD WAR

# USA: Analyse und Ausbauentwurf

Umsetzungsstand: Der genehmigte Ausbau ist integriert. Der [Implementierungsbericht](IMPLEMENTATION.md) dokumentiert den installierten Baum, die Bereinigung, Prüfungen und Ansichten. Die folgende Analyse bleibt als ursprüngliche Entwurfsgrundlage erhalten.

Stand: 24. Oktober 2026. Untersucht wurden der geladene 1970-Baum, seine relevanten Effekte, Gesetze, Entscheidungen und Ereignisse sowie der originale USA-Baum aus dem installierten Millennium Dawn 2.0.2. Alle 25 projektspezifischen Skills wurden nach Anwendbarkeit ausgewertet. Dies ist ein Konzept mit konkreten Zahlen, keine Änderung am geladenen Spielcode.

## Die wichtigste Designentscheidung

Der US-Baum braucht vor allem stärkere Programmidentitäten und mehr nutzbare Fortsetzungen. Ich empfehle einen ersten Ausbau auf **281 Fokusse**: **52 neue Fokusse**, **13 überarbeitete Belohnungspakete**, dazu gezielte Änderungen an Voraussetzungen und Ausschlüssen. Die Zahl ergibt sich aus diesen Programmen und ist weder Mindestgröße noch Obergrenze.

Der originale MD-Baum ist mit 776 Fokussen erheblich größer. Allerdings entfallen 442 auf alternative Parteiprogramme. Der heutige Baum hat 229 Fokusse, davon 50 im Nixon-Programm und 113 in späteren Wahlperioden. Beide Bäume haben bereits 28 einzigartige Ausschlusspaare. Mehr Ausschlüsse allein lösen deshalb das Problem nicht.

Übernehmen würde ich aus MD die Spezialisierung der Streitkräfte, regionale Entwicklung mit benannten Orten und Programme mit erkennbaren Institutionen. Moderne Parteien, spätere Raumfahrtprojekte und die Gesamtgröße des Originals sind keine historischen Vorlagen für Januar 1970. Der vollständige [Quellenvergleich](md_comparison.md) enthält Versionen, Hashes, aktuelle Zeilen und konkrete MD-Belohnungsbeispiele.

## Was bereits gut ist

Der aktuelle Baum verwendet Kongress, Wall Street, Regulierung, Haushalte und native US-Modifikatoren. Vietnam und die militärische Überdehnung bilden echte Ausgangsprobleme. Der Baum vergibt außerdem bereits viele materielle Belohnungen: 51 Fokusse enthalten direkte Gebäudebefehle. Eine bloße allgemeine Erhöhung von Fabrik-, Forschungs- oder Angriffsboni wäre daher keine überzeugende Vertiefung.

Auch echte Diplomatie existiert schon. China, Sowjetunion, Japan und Südvietnam bekommen tatsächliche Angebote und können antworten. Weitere Kanäle verwenden Handelsabkommen, Zugang und Partnerregistrierungen. Neue Abkommen sollen diese Kanäle zusammenführen und aufwerten, statt die gleichen historischen Vorgänge in einem zweiten System erneut auszuzahlen.

Die Wehrpflichtwahl ist ebenfalls bereits bedeutend. Der native Wechsel von Draft Army zu Volunteer Army verändert unter anderem Organisation um +20 Prozentpunkte und Personalkosten um +80 Prozentpunkte, während die Grundrekrutierung um 2,5 Prozentpunkte sinkt. Diese Gesetzeseffekte sind größer als viele kleine Fokusboni. Neue Programme dürfen sie weder übersehen noch verschleiern. Die vollständige Gegenüberstellung steht im [aktuellen Audit](current_audit.md).

## Wo der aktuelle Baum an Tiefe verliert

- Die Wahl der Geheimdienstaufsicht bestimmt zugleich, ob AirLand Battle oder Second Offset erreichbar ist. Diese Politikfelder sollten unabhängig sein. Heeresentwicklung bekommt danach eine eigene, sachliche Beschaffungs- und Einsatzwahl.
- Federal Industrial Grants und Market Investment Zones sperren Teile der Landwirtschaft, Verkehrsentwicklung beziehungsweise Beschaffung und Stadtentwicklung gegeneinander. Das Fördermodell darf exklusiv sein; normale komplementäre Entwicklung soll erreichbar bleiben.
- The Atlantic Bargain ist unter der interventionistischen Doktrin nicht erreichbar. Eine sicherheitspolitisch aktive USA muss trotzdem mit NATO-Partnern zusammenarbeiten können.
- Israelhilfe, Vermittlung sowie arabischer Handel sind derzeit als ganze Wege ausgeschlossen. Stattdessen sollen konkrete konkurrierende Zusagen, Mandate oder Vertragsmodelle exklusiv sein.
- Viele Belohnungen wiederholen allgemeine Forschungsgeschwindigkeit, Bürokratiekosten, Stabilität und PP. Spezielle Forschungsboni und Doktrinvergünstigungen fehlen in den geprüften US-Fokus- und Hilfsmodulen.
- Bei 48 von 51 direkten Gebäude-Fokussen fehlen die zusätzlich vorgeschriebenen gemeinsamen Bauplätze. Dies ist ein konkreter Integrationsbefund. Er sollte vor oder gemeinsam mit einem Belohnungsumbau behoben werden.
- Die späteren Parteiprogramme lesen überwiegend historische Wahlbelege. Aktive parteigebundene Programme brauchen zusätzlich die tatsächlich regierende Partei, ihre Abschaltung und gegebenenfalls spätere Wiederaufnahme.

Die Befunde sind mit aktuellen Codebeispielen in [current_audit.md](current_audit.md) belegt. Alte Projektmarker, tägliche Golf-Abrechnungen mit zu langen Dezimalzahlen und andere bestehende Probleme wurden während dieser Analyse nicht verändert.

## Attraktive Wahlprogramme

Die Zahlen unten sind vorgeschlagene **Ersatzpakete**, keine zusätzliche Schicht auf allen bisherigen Boni. Mehrere kompatible Programme können zusammenwirken, müssen vor Umsetzung aber mit Ausgangsgesetzen, Nixon-Entscheidungen, späteren Regierungen und bestehenden Obergrenzen verrechnet werden.

| Priorität | Alternative A | Alternative B | Sachlicher Preis |
| --- | --- | --- | --- |
| Industrielle Förderung | National Industrial Renewal: +5% Fabrikausstoß, +5% Effizienzwachstum, 2 zivile Fabriken und 2 Bauplätze | Competitive Investment Zones: +7% Baugeschwindigkeit, +3% Effizienzmaximum, 2 Büros und 2 Bauplätze | A: +1% Konsumgüterfaktor; B: -2% Steuereffizienz. Eigene Maschinenbau-/Ausbildungs- beziehungsweise Kredit-/Elektronikfortsetzungen. |
| Strukturwandel | Civilian Technology Network: +3% Forschung, +5% Effizienzwachstum, 2 begrenzte Elektronikboni | Regional Adjustment Compact: +4% Stabilität, +8% Effizienzerhalt, 2 Büros und 2 Bauplätze | A: +3% Bildungskosten; B: +1% Konsumgüterfaktor. Je ein praktisches Folgeprojekt. |
| Erste große Energie-Demonstrationsförderung | Standard Reactor Programme: +10% nukleare Energieerzeugung, +10% Reaktorbau, +2% Forschung | Industrial Energy Efficiency: -6% Energieverbrauch, +3% Fabrikausstoß, 2 Infrastruktur und 2 Bauplätze | A: 0,03 MD-Milliarden pro Woche; B: nur für 730 Tage -2% Baugeschwindigkeit. Grundlegende Kernenergie, Netzbau und Einsparungen bleiben gemeinsam nutzbar. |
| Rekrutierung | Native Volunteer Army plus Professional Force Establishment | Native Draft Army plus National Service Establishment | Die vollständigen echten Gesetzeseffekte bleiben erhalten. Berufspersonal und Führungskontinuität stehen einer billigeren größeren Mobilisierungsbasis mit schlechterer Expeditionsqualität gegenüber. |
| Geheimdienstführung | Statutory Intelligence Oversight: +3% Stabilität, +5% Verschlüsselung | Executive Intelligence Direction: +5% zivile Aufklärung, -10% Ausbauzeit der Agentur | A: +5% Ausbauzeit; B: -2% Stabilität. Keine Sperre für Heeresmodernisierung. |
| Einsatzkonzept des Heeres | Continental Sustainment Doctrine: -6% Versorgung, +10% Planung, 2 Doktrinvergünstigungen | Rapid Deployment Doctrine: +3% Organisation, +5% Planung, 2 begrenzte Forschungsboni | A: +3% Heeres-Treibstoffverbrauch; B: +3% Ausrüstungskosten. Eigene Logistikschulen beziehungsweise Erprobungsplätze. |
| Marineförderung | Carrier Readiness Programme: +5% Marineorganisation, +10% Marine-XP, 2 Doktrinvergünstigungen | Atlantic Escort Programme: +8% Geleitschutz, +5% U-Boot-Ortung, 2 Forschungsboni | A: +4% Marinepersonalkosten; B: +3%. Eine konkrete Förderpriorität, kein Verbot aller anderen Schiffstypen. |
| Umsetzung der Bürgerrechte | Federal Civil Rights Enforcement: +4% Stabilität, +5% ideologische Verteidigung, 1 Büro mit Bauplatz | State Compliance Agreements: +4% Baugeschwindigkeit, +2% Steuereffizienz, 2 Infrastruktur mit Bauplätzen | A: -3% PP-Gewinn; B: -2% PP-Gewinn und langsamere Entspannung. Der lokale Weg setzt durchsetzbare Rechte voraus. |

Nicht jeder Einzelfokus braucht einen Malus. Ein gut begründeter Nachteil pro dauerhaftem Programm und die verlorene Alternative reichen häufig. Gemeinsame sinnvolle Entwicklung bleibt gemeinsam.

## Mehr Entscheidungen nach den Wahlen

Der Entwurf ergänzt vier interne Förderentscheidungen mit jeweils unterschiedlichen Fortsetzungen. Dies vermeidet einen Ausbau, der praktisch nur Nixon interessanter macht.

- Demokraten 1972: Public Employment Works oder Employment and Training Credits. Öffentliche Beschäftigung und Infrastruktur gegen private Einstellung und Ausbildung mit geringerer Steuerbasis.
- Republikaner 1972: State Revenue Compacts oder Federal Performance Contracts. Weniger Bundesverwaltung und mehr einzelstaatlicher Spielraum gegen stärkere nationale Kontrolle und Industriestandards.
- Demokraten 1980: Industrial Retooling Boards oder Regional Enterprise Funds. Bestehende Produktionsnetze und Effizienzerhalt gegen neue Unternehmen und regionales Wachstum.
- Republikaner 1980: Accelerated Investment Allowances oder Fiscal Consolidation Bargain. Stärkere steuerliche Investitionsanreize gegen verlässlichere Einnahmen und geringere Verwaltungskosten.

Das sind Förderprioritäten innerhalb realer Parteien, keine neu erfundenen amerikanischen Ideologien. `western_liberals_are_in_power` und `western_conservatism_are_in_power` prüfen die vorhandenen Slots 2 und 1. Alle Karten bleiben sichtbar. Physische Investitionen überleben einen Regierungswechsel; aktive Parteiprogramme werden deaktiviert und bei zulässiger Rückkehr ohne erneute Einmalbelohnung wieder aktiviert.

1976 und spätere Wahlperioden behalten zunächst ihre bestehenden Programme. Weitere Vertiefung sollte aus einem konkreten politischen Konflikt entstehen, nicht aus einer gleichen Fokusquote für jeden Präsidenten. Der 1980-Entwurf ist teilweise bewusste plausible Alternativgeschichte, keine Behauptung tatsächlich verabschiedeter Gesetze.

## Der außenpolitische Ausbau

Geplant sind **16 konkrete Angebote und Folgeprogramme** für zwölf mögliche Partnerländer. Die beiden deutschen Vertragsmodelle schließen sich aus. Chinaöffnung und sowjetische Entspannung können gleichzeitig verfolgt werden. Atlantische, pazifische und nahöstliche Kontakte bleiben grundsätzlich unter allen drei US-Doktrinen erreichbar.

| Angebot | Dauer | Beide Seiten erhalten einen sichtbaren Gegenwert |
| --- | --- | --- |
| Bonn Forward Defence Agreement | Dauerhaft | USA: Organisation und Planung gegen Unterhalt. BRD: Organisation, Erholung und Doktrinbonus gegen Offsetzahlung und Ausrüstungskosten. |
| Bonn European Sustainment Agreement | Dauerhaft, exklusiv zum ersten Modell | USA: geringere Personalkosten und Erfahrung. BRD: Versorgung, Produktion, eine bezahlte Rüstungsfabrik mit Bauplatz und Forschung. |
| Expand the Auto Pact | Dauerhaft | Industrielle Produktivität, Effizienz und Forschung auf beiden Seiten, kanadische Zulieferfabrik mit Bauplatz; begrenzte Steuereinbußen. |
| North Atlantic Escort Exercises | 365 Tage | USA und Großbritannien: Geleitschutz, Erfahrung und Doktrinbonus gegen gemeinsame laufende Kosten. |
| Pacific Alliance Consultation | Dauerhaft | USA: Versorgung und Marineorganisation. Japan: Effizienzerhalt, Geleitschutz und Doktrin; laufende beziehungsweise politische Verpflichtungen für beide. |
| A Defined Advisory Mission | 730 Tage | USA: militärisches Lernen gegen bezahltes Engagement. Südvietnam: Ausbildung und Organisation gegen höhere Betriebskosten. |
| A Limited Commercial Opening | Dauerhaft | USA und China: begrenzte Produktion und industrielle Anpassung; keine erzwungene Taiwanregelung. |
| Scientific Exchange with Moscow | 730 Tage | Beide: Forschung und ein Industriebonus gegen Austauschkosten und geringere Verschlüsselung. Kein vorgetäuschtes SALT-System. |
| Bahrain Naval Facilities Agreement | Dauerhaft | Bahrain: echte Zahlung, laufende Miete, Hafeninvestition und Bauplatz. USA: bezahlte Unterstützungskapazität. Alternative zum vorhandenen Abtretungsvertrag. |
| Defensive Industrial Assistance | 730 Tage | Israel: Produktion, Ausbildung und Verteidigung. USA: Industriekontinuität und Erfahrung gegen finanzierte Hilfe. |
| Saudi Technical Services Commission | Dauerhaft | USA: bezahlte technische Aufträge. Saudi-Arabien: Aufbau- und Produktionsfähigkeit gegen Zahlungen und Ausbildungskosten. Historischer Anschluss 1974; früher ausdrücklich alternativ. |
| Border Industrial Development | Dauerhaft | Mexiko: zivile Fabrik mit Bauplatz und Ausbildung. USA: industrielle Kooperation gegen Investition und Steuereinbußen. |
| A Renewed Rogers Initiative | 180 Tage | USA: Vermittlungsmandat. Ägypten und Israel: begrenzte Stabilität, PP und Effizienzerhalt, jeweils erst nach Zustimmung beider Empfänger. |
| Transatlantic Standards Board | 730 Tage | Zweites zustimmungspflichtiges deutsches Folgeprogramm mit Forschung und Standards. |
| Joint Automotive Retooling | 730 Tage | Zweites kanadisches Folgeprogramm mit je einer bezahlten Fabrik samt Bauplatz und Effizienz, gegen Investition und Konsumgüteranteil. |
| Pacific Maintenance Standards | 730 Tage | Zweites japanisches Folgeprogramm mit Marineorganisation und Doktrin, gegen Investition und Marinepersonalkosten. |

Die vollständigen exakten Zahlen für jede Seite stehen im klickbaren Entwurf und in [proposal.json](proposal.json). Die Dauern laufen ab endgültiger Annahme. Bei dreiseitigen Gesprächen läuft die Frist erst nach der letzten erforderlichen Zustimmung.

Alle 15 miteinander kombinierbaren US-Vertragspakete kosten im theoretischen Überschneidungsfall **77 MD-Milliarden einmalig** und **0,15 MD-Milliarden pro Woche netto**. Darin sind 0,19 laufende Ausgaben und 0,04 deutsche beziehungsweise saudische Einnahmen enthalten. Personalkosten, Ausrüstungskosten, Steuereffekte und andere Modifikatoren kommen hinzu. Die Zahl ist eine Belastungsrechnung des Entwurfs, kein Nachweis, dass diese Kombination im normalen Spiel gleichzeitig verfügbar oder bereits ausbalanciert ist.

## Zustimmung und Laufzeit

1. Der konkrete US-Fokus eröffnet ein bestimmtes Angebot. Der Fokusabschluss vergibt dessen Vertragsbelohnungen noch nicht.
2. Das benannte Empfängerland erhält die wirkliche Annahme-/Ablehnungsentscheidung. Nach 90 Tagen ohne Antwort endet das offene Angebot. Schweigen ist keine Zustimmung.
3. Die Annahme prüft erneut beide Länder, wirkliche Kosten, notwendige Elternabkommen, Embargos, Sanktionen und gegebenenfalls Baukapazität. Die dreiseitige Rogers-Initiative aktiviert erst nach beiden Empfängerantworten.
4. Erst die gültige Gesamtannahme führt die Setup-Transaktion einmal aus und aktiviert die benannten Spirits auf beiden Seiten.
5. Dauerhafte Verträge bleiben bis Kündigung bestehen. Bei bilateraler Blockierung werden beide Spirits und zugehörige wöchentliche Zahlungsströme ausgesetzt.
6. Nach Wegfall der Blockierung werden sie ohne Wiederholung von Zahlungen, Bauprojekten, Erfahrung oder Forschungsboni wiederhergestellt. Zeitlich befristete Programme behalten ihr ursprüngliches Kalenderende.
7. Auch Kündigung, Neuverhandlung oder ein Wechsel des deutschen Vertragsmodells setzt die Belege bereits verdienter Einmalbelohnungen nicht zurück. Erneut bezahlte Übungen sind ein eigener, klar begrenzter Wiederholungsvertrag.

Ablehnung braucht keine automatische Meinungsstrafe. Für die Wiederaufnahme des konkreten fokusgebundenen Angebots reicht nach 90 Tagen ein bestehender diplomatischer Kanal. Das ist keine Verlagerung aller US-Angebote in ein neues Auswahlmenü.

Der Rogers-Kanal prüft die Beziehungen USA-Ägypten und USA-Israel. Ein ägyptisch-israelischer Krieg verhindert das Gesprächsangebot nicht. Eine Waffenruhe, Friedensregelung, Grenzänderung oder Öffnung des Suezkanals braucht einen eigenen, ausdrücklich von allen betroffenen Spielern angenommenen Schritt.

Für stehende Abkommen werden ein natives Embargo und alle vier Imperia-Sanktionsklassen in beiden Richtungen geprüft. Sanktionen eines unbeteiligten Drittlandes beenden kein amerikanisch-kanadisches Abkommen. NATO-spezifische Angebote verlangen den tatsächlichen aktiven `NATO_member`-Spirit. Folgeprogramme verlangen ihren aktiven Elternvertrag.

## Historische Verankerung und bewusste Grenzen

New Federalism und die Family Assistance Plan-Debatte verbinden bundesweite Sozialpolitik, Arbeitsanreize und Zuständigkeiten. Das begründet unterschiedliche institutionelle Kosten, ohne jedem US-Programm dieselbe Bürokratiestrafe zu geben. [Nixons Botschaft von 1969](https://www.presidency.ucsb.edu/documents/special-message-the-congress-reform-the-nations-welfare-system)

Die Entstehung der EPA 1970 zeigt, dass Forschung, bundesweite Standards und reale Umsetzungskapazität zusammengehören. Der bestehende Clean-Air-Weg sollte darauf aufbauen; eine zusätzliche Anti-Umwelt-Standardroute ist nicht nötig. [EPA zur Gründung](https://www.epa.gov/history/origins-epa)

Die deutsche Offsetdebatte verknüpfte tatsächliche Verteidigungskosten, Beschaffung und regionale Verantwortung. Daraus lassen sich zwei lohnende Vertragsformen ableiten. Die Entwurfszahlen sind keine Umrechnung der historischen Dollarbeträge. [Unterzeichnetes Offsetabkommen von 1971](https://history.state.gov/historicaldocuments/frus1969-76v41/d78)

Die Chinaöffnung und SALT wurden parallel betrieben. Sie sind deshalb keine sinnvollen gegenseitigen Ausschlüsse. Ein echtes SALT-Abkommen muss später mit dem vorhandenen Nuklearsystem und tatsächlich überprüften Begrenzungen verbunden werden. Ein Forschungsbonus mit sinkender Kriegsunterstützung allein stellt keine Rüstungskontrolle dar. [Chinaöffnung](https://history.state.gov/milestones/1969-1976/rapprochement-china), [SALT](https://history.state.gov/milestones/1969-1976/salt)

Bei Okinawa beginnt die Hauptinsel im aktuellen Mod bereits japanisch; die US-Basis ist ein eigener Staat. Der Entwurf verhandelt Konsultation, nicht die unzutreffende Rückgabe einer vermeintlich vollständig amerikanischen Insel. Das vorhandene Bahrain-Abtretungsangebot bleibt als bewusst andere Alternative erhalten. [Zeitgenössische Okinawa-Verhandlungen](https://history.state.gov/historicaldocuments/frus1969-76v19p2/d4)

Auto Pact und mexikanische Grenzindustrialisierung existierten seit 1965. Die Fokusse vertiefen diese Grundlagen; sie gründen weder NAFTA noch einen neuen modernen Handelsblock. [Kanadischer Vertragstext](https://www.treaty-accord.gc.ca/text-texte.aspx?id=100604), [mexikanisches Wirtschaftsministerium](https://www.economia-snci.gob.mx/sic_php/pages/importa/abc_maquiladora.php)

Rogers II zeigt die historische Grundlage für getrennte Zustimmung Israels und Ägyptens. Die saudische Kommission gehört historisch 1974 in die Fortsetzung. [Rogers-Initiative 1970](https://history.state.gov/milestones/1969-1976/arab-israeli-war-1973), [saudische Kommission 1974](https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d104)

## Umsetzung in sinnvollen Etappen

Zuerst die belegten Integrationsprobleme lösen: zusätzliche Bauplätze, exakte Parteibindung, vollständige Gesetzesvorschau, verständliche Voraussetzungen und korrekte wöchentliche Kosten. Bestehende IDs und verdiente Belege bleiben erhalten. Der historische US-Generator fehlt im Checkout; die vorhandenen Narrative-Overlays und Golfgeneratoren haben getrennte Zuständigkeiten.

Danach die 13 bestehenden Belohnungspakete samt wirtschaftlichen und militärischen Fortsetzungen überarbeiten. Die 16 späteren Wahlfokusse erhalten echte Parteiprogramm-Abschaltung. Die ursprünglichen Ausgangsprobleme bleiben real. Keine automatische Weltverbesserung und keine generelle Anhebung aller US-Kampfwerte.

Als erste Diplomatie-Ausbaustufe eignen sich BRD, Kanada und Japan besonders gut: vorhandene Beziehungen, deutlich unterscheidbare Interessen und überschaubare bilaterale Transaktionen. Danach China, Sowjetunion, Südvietnam und die weiteren regionalen Angebote. Die drei-seitige Vermittlung folgt nach einem nachgewiesenen Zwei-Länder-Ablauf.

Wöchentliche feste Geldströme müssen beim tatsächlichen MD-Einkommens- und Ausgabenverbraucher genau einmal ankommen. Bestehende Kuba-Spirits sind ein guter Lebenszyklusspender, aber kein Beleg einer bereits integrierten US-Wochenzahlung. Konkrete Modifier- und Forschungszuordnungen, deren technische Prüfung noch offen ist, sind im Manifest gekennzeichnet.

Für die spätere native Prüfung sind Annahme, Ablehnung, veränderte Finanzen, ausgebuchte Staaten, doppelte Antworten, parallele Angebote, Sanktionen in beiden Richtungen, Krieg, Aufhebung, Elternvertragsverlust, Regierungswechsel, Ablauf, Speichern/Laden und Rehost mit zwei menschlichen Ländern nötig. Die interaktive Vorschau ist eine Quellen- und Konzeptdarstellung, kein Beweis für HOI4-Laden, native Tooltipdarstellung oder Multiplayer-Stabilität.

## Dateien und Nachweis

- [Vollständiger aktueller Audit](current_audit.md)
- [Original-MD-Vergleich mit numerischen Vorbildern](md_comparison.md)
- [Zuordnung aller 25 Projekt-Skills](skills_and_diplomacy.md)
- [Maschinenlesbarer Ausbauentwurf mit allen Zahlen](proposal.json)
- [Unabhängiger korrigierter Konzeptreview](concept_review.md)
- [Abschließende Quellen- und Vorschauprüfung](VERIFICATION.md)
- `current_inventory.json` und `original_inventory.json`: vollständige Quelleninventare.
- `build_proposal.py`: baut ausschließlich das Konzeptmanifest.
- `build_visual.py` und `review_fragment.html`: erstellen ausschließlich die Vorschau aus demselben Manifest und den Quelleninventaren.

Quellcode und bestehende MD-Grafiken stammen von den jeweiligen Projekt- und Millennium-Dawn-Autoren. Ihre gesonderte Weitergabeberechtigung ist unbekannt; dieser Entwurf ist eine lokale Projektanalyse. Quellen bleiben unverändert. Die Vorschau reduziert bestehende Icons und nähert Verbindungen und Schrift an; sie ist kein Live-Spielbild. Detailprovenienz steht in `preview_provenance.json`.
