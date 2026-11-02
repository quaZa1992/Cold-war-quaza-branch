IMPERIA COLD WAR: Programme Scales, Active Days and Further Co-operation
======================================================================

Aktuelle Host-Belohnungen: [COMECON_HOST_REWARDS.md](COMECON_HOST_REWARDS.md) ersetzt die früheren generischen Anlagenpakete. Nur drei der elf Vorlagen vergeben noch Zivilfabriken; die übrigen verwenden Agrarkapazität, Logistik, Netzanschlüsse, Büros, Reaktoren oder die Modernisierung vorhandener Werke.

Stand: 24. Oktober 2026. Vorrangige Ergänzung zu `COMECON_DOSSIER_REVISION.md`: Der Nutzer verlangt skalierende Partnerleistungen, aktive Tage, Programmsymbole mit RGW-Bezug und keine sichtbaren Programmjahre. Weiterhin Konzept und interaktive Vorschau; keine native Laufzeitänderung.

Verbindliche Logo-Korrektur des Nutzers: Das weiße verschlungene Zeichen mit rotem Stern auf rotem Grund aus der beigefügten PNG ist die gewünschte visuelle Identität. Es ersetzt das zuvor ausgewählte Gebäudeemblem in Kopf und Programmkennungen. Die ursprüngliche Datei wird unverändert verwendet. Originalurheber und Lizenz sind unbekannt; die Nutzerangabe ist keine eigenständige historische oder rechtliche Herkunftsprüfung. Dateihash und Herkunft stehen in `user-emblem-record.json` bei der Vorschau.

## Investitionsumfang bestimmt die Stärke

| Investment scale | Gewählter sektoraler Partnerbonus | Nationale Durchführung pro aktiver Woche | Betreuung durch den Host pro aktiver Woche |
|---|---:|---:|---:|
| Limited | +3% | 0.006% des eigenen BIP | $12M |
| Standard | +5% | 0.010% des eigenen BIP | $20M |
| Major | +8% | 0.016% des eigenen BIP | $32M |

Die Preise und Anlagenstufen der bisherigen teuren Projektpakete bleiben erhalten. Der Umfang bestimmt die Stärke des gewählten Produktivitäts- oder Baubonus; der tatsächlich bezahlte Länderanteil bestimmt seine Laufzeit. Damit hat ein größeres Vorhaben mehr Wirkung, längere Bauzeit und höhere laufende Durchführungskosten. Nicht-Hosts erhalten nicht zusätzlich eine zweite Belohnung aus demselben Anteil. Der Host erhält weiterhin die Anlage und den zugehörigen Bauplatz, keinen zweiten Partnerbonus.

Diese Zahlen ersetzen den bisher einheitlichen +5%-Bonus und den einheitlichen laufenden Betreuungsbetrag. Es sind Spielwerte, keine historischen Renditen. Die Stärke gleicher Programme wird nicht addiert. Eine freiwillige Finanzierung über den maximal belohnten Anteil hinaus bleibt ausdrücklich sichtbare Unterstützung, kein unbegrenzter Kauf von Bonuslaufzeit.

## Tage anzeigen, Wochenkosten erhalten

Die Spieleranzeige verwendet **active days**. Die bisherige Dauer wird korrekt mit sieben multipliziert, nicht nur umbenannt:

| Bezahlter Anteil eines Nicht-Hosts | Partnerlaufzeit |
|---:|---:|
| 5% | 182 active days |
| 10% | 364 active days |
| 20% | 728 active days |
| 30% oder mehr | 1092 active days |

Formel: `min(1092, round(Anteil in Prozent * 36.4))`. Da die Eingabe in 5%-Schritten erfolgt, sind dies ganze Tage. Die Bauzeiten erscheinen ebenfalls in Tagen, etwa 104 Wochen als 728 Tage. Geldbeträge bleiben entsprechend der bestehenden MD-Wirtschaft ausdrücklich **pro Woche**. Pause, Restlaufzeit und wöchentliche Zahlung sind unterschiedliche Größen.

Der Laufzeitentwurf kann ganze bezahlte Siebentagesabschnitte speichern. Bei einer Unterbrechung beginnt oder endet die nächste bezahlte Leistungsperiode an derselben zentralen Abrechnungsgrenze. Die UI zeigt ihren verbleibenden Wert in Tagen. Eine tagesgenau anteilige Abrechnung wäre eine zusätzliche Mechanik und ist mit der Bezeichnung allein nicht implementiert. Kein neuer täglicher Länder- oder Staatenvollscan wird benötigt.

## Keine Programmjahre in der Auswahl

Register, Namen und Kurzbeschreibungen enthalten keine Gründungsjahre. Keine Vorlage erhält eine reine Jahresfreischaltung. Wiederholte oder spätere Teilnahme wird als neuer Ausbau, Anschlussvertrag, Fortsetzung oder Beitritt formuliert. Nachweise und historische Jahreszahlen bleiben in der Projektdokumentation erhalten.

Reale Anforderungen gelten weiterhin: geeignete Technik, existierende und passende Institutionen beziehungsweise eine separat genehmigte Gründungsvereinbarung, Standort, Kontrolle, Kapazität, Rohstoffe und Finanzierung. Eine fehlende Jahreszahl gewährt weder kostenlose Kerntechnik noch unbegrenzte Wiederholungsprämien. Später historisch gegründete Einrichtungen dürfen im RP bewusst früher vereinbart werden; die tatsächlichen Gründungsjahre werden dadurch nicht umgeschrieben.

## Symbole mit Bezug zum RGW

Jede Programmkennung kombiniert das unverändert übernommene weißrote Nutzerlogo mit einem passenden vorhandenen Modmotiv: Metallurgie, Landmaschinen, Labor, Bahn, Energie, Fahrzeugproduktion, Information, Kernenergie, Präzisionsfertigung, Textilmaschinen oder Recycling. Das sind neu komponierte Kennungen dieser Spieloberfläche, keine als historisch ausgegebenen Fachorganisationslogos.

Die Bestandteile bleiben getrennte Bilder. Quellen und Quelldateien der 13 Motive stehen in `programme-symbol-records.json` neben der Vorschau; individuelle Künstler und Lizenzen dieser vorhandenen Modbilder sind unbekannt. Die gesonderte Logo-Provenienz nennt das Nutzerbild als aktuelle Quelle; die frühere Gebäudezeichnung bleibt nur Referenzmaterial. Alle Länderflaggen bleiben an den aktuellen Länderzustand über natives `GetFlag` gebunden; die Vorschau verwendet lokale Modbeispiele.

## Drei zusätzliche bedienbare Investitionsvorlagen

| Vorlage | Historischer Anhaltspunkt | Anlage und auswählbares Partnerpaket | Gesamtbudget Limited / Standard / Major |
|---|---|---|---|
| Precision Bearings Co-operation | Gemeinsame Spezialisierung und Versorgung mit Kugellagern | 1 / 2 / 4 civilian factories und Bauplätze; civilian industry productivity oder civilian industry construction speed | $31.2B / $62.4B / $124.8B |
| Textile Machinery Co-operation | Intertextilmash: Maschinen, Ersatzteile, gemeinsame Entwicklung und Wartung | 1 / 2 / 4 civilian factories und Bauplätze; dieselben beiden Industriepakete | $31.2B / $62.4B / $124.8B |
| Material Recovery and Reclamation | Haldex: ungarisch-polnische Rückgewinnung aus Abraum und Rekultivierung | 1 / 2 / 4 civilian factories und Bauplätze; dieselben beiden Industriepakete | $26B / $52B / $104B |

Alle drei verwenden 728 / 1092 / 1456 bezahlte Bautage. Die Wiedergewinnung wird hier als zivile Verarbeitungskapazität abstrahiert. Es werden keine erfundenen Kohlebestände oder automatischen Rohstoffvorkommen gewährt. Die Textilvorlage kann eine eigene Gründungs- beziehungsweise Teilnahmevereinbarung einschließen. Die Quelle belegt die Einrichtungen und Tätigkeiten, nicht die hier vorgeschlagenen Gebäude oder +3% / +5% / +8%.

Grundlage: [UNIDO, Institutional mechanisms for economic and industrial co-operation, 1978](https://downloads.unido.org/ot/47/91/4791252/00001-10000_07981_1978.pdf), gedruckte Seiten 25-26 und 32-35. Dort werden unter anderem gemeinsame Spezialisierung, Ersatzteilversorgung, gleiche beziehungsweise vertraglich geregelte Beiträge und organisatorische Eigenständigkeit beschrieben. Die historische Fachmitgliedschaft wird nicht automatisch mit jeder RGW-Mitgliedschaft gleichgesetzt.

## Militärische Programme

Militärisch-technische Zusammenarbeit, Rüstungsplanung und Standardisierung sind historisch belegt. Ein archivierter Beschlussauszug betrifft koordinierte Produktionspläne und gegenseitige Rüstungslieferungen und sieht auch eine koordinierende RGW-Rolle vor. Es wäre daher zu pauschal zu behaupten, der RGW habe damit nie etwas zu tun gehabt. Die militärische Befehlsgewalt lag dadurch jedoch nicht beim normalen wirtschaftlichen Projektfenster.

Für das Spiel empfiehlt sich im gleichen Aktenstil die eigene Vertragsgruppe **Military-Technical Co-operation**. Zugang und Zustimmung beruhen auf einem tatsächlichen Militärabkommen oder passenden Bündniszusammenhang, nicht allein auf dem RGW-Mitgliedsstatus. Es werden weder alle RGW-Mitglieder automatisch beteiligt noch neutrale beziehungsweise nicht beteiligte Länder überstimmt. Die Regel zur sowjetischen Delegation und getrennten lokalen SSR-Zustimmung bleibt erhalten.

Konkrete erste Vorschläge, noch nicht in die zivile Vorschau eingebaut:

* **Joint Defence Industrial Expansion**: Host erhält 1 / 2 / 4 military factories und gleich viele Bauplätze. Nicht-Hosts wählen als gemeinsame Gegenleistung +3% / +5% / +8% Production Efficiency Growth oder Military Factory Construction Speed. Gesamtbudget $62.4B / $124.8B / $249.6B, 1092 / 1456 / 2184 bezahlte Bautage. Wochenraten $400M / $600M / $800M. Nationale Durchführung und Bonuslaufzeit folgen der obigen Staffel. Keine automatische Freigabe fremder Ausrüstungsdesigns; echte Lizenzvereinbarungen bleiben erforderlich.
* **Ammunition and Spare Parts Standardisation**: gemeinsame Standards, Prüfverfahren und Ersatzteilverwaltung. Als enger Spielvorschlag -2% / -3% / -5% Army Supply Consumption während eines finanzierten Programms. Nationale Kosten 0.010% / 0.020% / 0.040% des eigenen BIP pro Woche, gemeinsame Koordination $50M / $100M / $200M pro Woche, 728 / 1092 / 1456 bezahlte Programmtage. Kein zusätzlicher allgemeiner Angriffsbonus. Der nationale Modifier ist eine breite Abstraktion und keine Simulation einzelner Munitionskaliber.
* **Joint Vehicle Production Agreement**: gemeinsamer Fahrzeugentwurf, aufgeteilte Komponentenfertigung, vereinbarte Abnahme und Wartung. Historischer Anhaltspunkt: OT-64/SKOT-Kooperation zwischen Polen und der Tschechoslowakei. Im Spiel an tatsächliche vorhandene Technik, Produktions- und Lizenzmechaniken binden; keine kostenlose spätere Technik durch bloße Zahlung. Mengen und Lieferfristen werden pro konkretem Ausrüstungstyp vereinbart und sind noch nicht beziffert.
* **Technical Training and Maintenance Exchange**: Ausbildung von Technikern, Instandsetzung und standardisierte Wartung. Ein eigenständiger RP-Vertrag ist sinnvoll; konkrete Modifier brauchen eine getrennte Prüfung. Keine pauschale Stapelung von Ausbildung, Organisation, Angriff und Produktionsausstoß in einem günstigen Paket.

Die ersten beiden Preis-/Effektpakete sind überprüfbare Balancevorschläge. Die beiden weiteren Vertragsideen haben noch keine fertige Kosten- und Wirkungsvorlage. Bestehende lokale Beispiele verwenden `production_factory_efficiency_gain_factor`, `production_speed_arms_factory_factor` und `supply_consumption_factor`; native Detailwirkung und Stapelung müssten vor einer Laufzeitimplementierung geprüft werden.

Historische Nachweise:

* [ETH Parallel History Project: Beschlussauszug zu Rüstungsplanung und gegenseitigen Lieferungen](https://www.php.isn.ethz.ch/lory1.ethz.ch/collections/colltopiced0a.html?id=16692&lng=en&navinfo=16161). Erschließung verweist auf RGAE 4372/79/792, Blätter 123-126. Verwendet wurde die archivische Beschreibung; der direkte Volltextabruf scheiterte. Keine Behauptung, das gesamte Original gelesen zu haben.
* [ETH: Bericht des Technischen Komitees zur Integration und Standardisierung](https://phpisn.ethz.ch/lory1.ethz.ch/collections/colltopic68cb.html?id=21669&lng=en&navinfo=14565). BA-MA DVW 1/71033. Die Beschreibung nennt gemeinsame Rüstungsvorhaben und ungelöste Standardisierungsprobleme. Ebenfalls auf Grundlage der archivischen Erschließung.
* [NATO, Force Comparisons 1984](https://archives.nato.int/uploads/r/null/1/3/137795/0228_NATO_and_the_Warsaw_Pact_1984-Force_Comparisons_ENG.pdf), Abschnitt Military Production and Technology Capabilities. Zeitgenössische NATO-Perspektive, kein neutraler Wirkungsnachweis; direkter PDF-Abruf blockiert, recherchierbarer Textauszug verwendet.
* [Slowakisches Militärhistorisches Institut: OT-64A SKOT](https://www.vhu.sk/data/att/b0a/17566.eb88b7.pdf): bilaterale gemeinsame Produktion. Der Nachweis dient dem Kooperationsmodell, nicht dem Nachbau einer bestimmten Waffe.

## Weitere zivile Programme

Geeignete nächste Verträge sind die bereits entworfenen Produktivitätskampagnen, Fachkräfte-/Ausbilderaustausch, Qualitätskontrolle, Standardisierung und Metrologie, Kraftwerkswartung, Brennstoffeffizienz, agrarische Beratung und gemeinsame Forschung. Sie brauchen eigene nationale Durchführung, bezahlte Phasen und passende Voraussetzungen. Ein Investitionsprojekt ersetzt diese Arbeit nicht kostenlos.

**Intercosmos Scientific Co-operation** eignet sich als zusätzliche friedliche Wissenschaftskooperation: nationale Instrumente, Bodenbeobachtung, meteorologische Forschung, Datenverarbeitung und Austausch. Ein gemeinsamer finanzieller Sondervertrag ist denkbar. Der Vertragstext sieht nationale Finanzierung als Grundregel vor und lässt besondere Vereinbarungen zu; er gewährt keinen pauschalen RGW-Anspruch auf kostenlose Raumfahrt oder militärische Raketen. Für diesen separaten Forschungsprogrammtyp sind noch keine endgültigen Gebäudepakete oder Modifier freigegeben.

Quelle: [Bei JAXA wiedergegebener Vertragstext](https://www.jaxa.jp/library/space_law/chapter_2/2-2-2-7_e.html), insbesondere Artikel 2, 6 und 8. Die Überschrift der Seite nennt 1973, der Schluss des wiedergegebenen Vertragstextes 13. Juli 1976. Für die Datierung wird diese Abweichung ausdrücklich festgehalten; die Programmoberfläche benötigt kein Gründungsjahr.

## Prüfung und Herkunft

Die erweiterte Vorschau besteht aus elf zivilen Investitionsvorlagen. 90 Interaktions- und Bildprüfungen bestanden: Staffelung beider Bonusoptionen, korrekte Umrechnung in Tage, wöchentliche Geldwerte, Host-Ergebnis, Anteilslaufzeiten, Beitragsrechte, SSR-Zustimmung, Abstimmung, Sperre nach Ratifikation und Migration älterer Vertragsfassungen. 174 eindeutige Elemente, 24 eingebettete Quellbilder, unter 1 MB. Ältere Unterschriften werden bei der geänderten Leistungsstaffel verworfen; die gewählte Vorlage und Finanzierungsanteile bleiben erhalten.

Eigenständiger Konzepttext und UI-Zusammenstellung für IMPERIA COLD WAR. Native Systeme und Modmotive stammen von Paradox Interactive, MD-Team und Projektbeitragenden, soweit bekannt. Die jeweiligen konkreten Bildurheber und Rechte sind in der Begleitprovenienz beziehungsweise als unbekannt dokumentiert. Keine native Multiplayer-Prüfung und kein fertig implementiertes Militärsystem.
