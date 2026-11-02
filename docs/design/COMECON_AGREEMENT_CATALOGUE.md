IMPERIA COLD WAR: Distinct Co-operation Agreements and Civil Nuclear Integration
=============================================================================

Aktuelle Nutzerrevision: [COMECON_SHORT_CYCLES_PROGRAMMES.md](COMECON_SHORT_CYCLES_PROGRAMMES.md). Host-Gebäude sind auf eine Stufe je Typ reduziert. Projekte dauern 90 Tage, ihre laufenden Leistungen weitere 90 Tage. Elf unabhängige Gemeinschaftsprogramme wirken während 180 finanzierter Tage. Nuklearbau ist auf Bauunterstützung geändert; es gibt keinen in 90 Tagen geschenkten Reaktor. Frühere lange Laufzeiten und bankbare Forschungszuteilungen unten sind dadurch überholt.

Stand: 24. Oktober 2026. Vorrangige Revision zu `COMECON_HOST_REWARDS.md`: Die früheren zwei universellen Partneroptionen werden vollständig durch projektbezogene Vertragsangebote ersetzt. Der Nuklearteil wird an den tatsächlich vorhandenen zivilen Nuklearfunktionen ausgerichtet. Aktualisierte Konzeptvorschau, keine native Laufzeitimplementierung.

Die elf Registereinträge haben jetzt insgesamt **33 Angebote**. Sie umfassen reale Bestandslieferungen, einmalige Forschungsförderung, laufende Fachprogramme, zusätzlich finanzierte Infrastruktur und gemeinsame Betreiberleistungen. Ein Projekt besitzt zwei, drei oder vier passende Angebote. Die bloße Umbenennung desselben Civ-Baubonus gilt nicht als neue Gegenleistung.

## 1. Untersuchte Nuklearfunktionen

Der lokale Code enthält bereits folgende Mechaniken:

* `common/scripted_effects/COLDWAR_nuclear_power_effects.txt`: monatliche Reaktorverwaltung, Flottenalter, gewähltes Wartungsregime, Sicherheitsziel und tatsächlicher Sicherheitswert, Unfallberechnung, Brennstoffverträge und reale Reaktorbrennstoffbestände.
* `common/scripted_triggers/COLDWAR_nuclear_power_triggers.txt`: eigenes Nuklearprogramm für Spieler mit Reaktoren; die normale wirtschaftliche Zugangsvoraussetzung nutzt die vorhandenen Entwicklungsstufen.
* `common/ideas/COLDWAR_nuclear_power_ideas.txt` und passende Dynamic Modifiers: Brennstoffverbrauch, Nuklearunterhalt, Zielwert für Sicherheit, Reaktorauslegung und bestehende Forschungsresultate.
* `events/COLDWAR_nuclear_power_events.txt`: Brennstoffangebote und schlüsselfertige Reaktorangebote mit tatsächlicher Empfängerannahme. Das bisherige Turnkey-Angebot plant einen Reaktor nach 1460 Tagen.
* `common/decisions/COLDWAR_nuclear_power_decisions.txt`: qualifizierter Anbieter über `COLDWAR_reactor_design_flag`; vorhandener Turnkey-Empfängerpfad für Entwicklungsländer. Dieser Pfad ist keine allgemeine Bau-API für jeden Staat.
* `common/special_projects/projects/COLDWAR_nuclear_civil_projects.txt`: eigene zivile Forschungsprojekte für unter anderem Reaktordesign und Brennstoffkreislauf. Eine RGW-Unterschrift ist kein Ersatz für deren Abschluss.
* `common/scripted_effects/!_energy_effects.txt` und Uranium-Integration: echte Brennstofferzeugung, tatsächlicher Brennstoffverbrauch, Bestände und die Abhängigkeit der Anreicherung von natürlichem Uranium.

Der Sicherheitszielwert wird aus Basis, Technik, Ideen und Wartungsregime berechnet, auf 0 bis 100 begrenzt und verändert den aktuellen Sicherheitswert um höchstens zwei Punkte pro Monat. Eine neue Zielwerterhöhung bedeutet daher weder einen sofortigen gleich großen Sprung der aktuellen Sicherheit noch garantierte Unfallfreiheit. Das gewählte Wartungsregime und die Flottenalterung bleiben erhalten.

## 2. Vier eigenständige zivile Nuklearangebote

Die Zahlen sind Balancevorschläge. Sie verwenden vorhandene Effekte und Voraussetzungen, ohne die entsprechenden neuen RGW-Verträge als bereits implementiert auszugeben.

### Joint Reactor Construction

Der gewählte Anlagenempfänger erhält Limited / Standard / Major **1 / 2 / 3 zivile Kernreaktoren** und jeweils dieselbe Zahl zusätzlicher shared building slots vor den Reaktoren im tatsächlich geprüften Standortstaat. Die anderen zahlenden Partner erhalten **1 / 1 / 2 Forschungsboni mit +15% / +25% / +35% auf Civilian Reactor Research**. Kategorie: `CAT_nuclear_reactors`, nicht die breitere Kategorie für sämtliche nuklearen Anwendungen.

Basisbudget: **$52B / $156B / $312B**. Hinzu kommen **$0.52B / $1.04B / $2.08B je Forschungsbegünstigtem**. Bezahlte Finanzierungsabschnitte: 208 / 312 / 416 Wochen. Mindestfertigstellung: **1460 / 2190 / 2920 Tage**. Der Unterschied zwischen ganzen Finanzierungswochen und der Mindestbauzeit wird ausdrücklich beibehalten: vollständige Bezahlung allein zieht die Fertigstellung nicht vor die Mindestzeit. Beim Standard mit drei Partnern sind das $159.12B, $510M pro Finanzierungswoche und 2190 Tage Mindestbauzeit.

Voraussetzungen: kontrollierter geeigneter Standort, echte Kapazität, passende zivile Technik oder ein tatsächlich genehmigter Turnkey-Betreiberpfad, qualifizierter Design-/Lizenzpartner, Netz- und Brennstoffversorgung. Der bisherige Anbieter- und Zustimmungspfad wird respektiert. Für ein Entwicklungsland braucht es den passenden genehmigten Betreibervertrag; die normale eigene Forschung behält ihre echten wirtschaftlichen und technischen Voraussetzungen.

Die Reaktoren treten in die bestehende Energie-, Unterhalts-, Alterungs-, Wartungs- und Brennstoffberechnung ein. Es gibt keinen zweiten pauschalen Erzeugungsbonus zusätzlich zum Gebäude. Keine automatische eigene Anreicherung, Uraniumproduktion, Minenanlage, neue Technologie oder Vollendung eines Spezialprojekts.

### Joint Operator and Safety Programme

Alle **geeigneten tatsächlichen Teilnehmer**, einschließlich der koordinierenden Delegation, erhalten dieselbe Staffel:

| Umfang | Zeitweilige Leistung je geeignetem Teilnehmer | Einmalige zivile Reaktorforschung | Gemeinsame Leistungsdauer |
|---|---|---|---|
| Limited | +5 Nuclear Safety Target, +2% Nuclear Plant Upkeep | 1 x +15% | 728 active days |
| Standard | +10 Nuclear Safety Target, +3% Nuclear Plant Upkeep | 1 x +25% | 1092 active days |
| Major | +15 Nuclear Safety Target, +5% Nuclear Plant Upkeep | 2 x +35% | 1456 active days |

Vorhandene Leser: `mdcw_nuclear_safety_target` und `nuclear_infra_cost_multiplier_modifier`. Die eigene Durchführung kostet je aktivem Land zusätzlich **0.006% / 0.010% / 0.016% seines BIP pro Woche**. Der Koordinator übernimmt $12M / $20M / $32M pro Woche gemeinsame Betreuung. Beide Pflichten stehen vor Zustimmung fest.

Basisbudget $10.4B / $20.8B / $41.6B plus $1.04B / $2.08B / $4.16B je Teilnehmer. Vorbereitung 364 / 728 / 1092 bezahlte Tage. Beispiel Standard mit vier Teilnehmern: $29.12B Gesamtbudget und $280M pro Finanzierungswoche.

Die vorhandene Sicherheitsverwaltung läuft nur für tatsächliche Spieler-Nuklearprogramme mit Reaktoren. Darauf wird die Teilnahme am Sicherheitsvertrag beschränkt, solange diese native Mechanik nicht ausdrücklich erweitert wird. Ein Land ohne Reaktor erhält keinen wirkungslosen als Ertrag ausgegebenen Sicherheitsbonus. Es kann stattdessen am nachfolgenden Forschungsangebot teilnehmen. AI-Finanzierung oder Mitgliedschaft macht aus einem Land kein vorhandenes Spieler-Nuklearprogramm.

Die Effekte werden als eigene RGW-Betreibervereinbarung geführt. Es wird kein Unfallereignis ausgelöst, um dessen Lessons-Learned-Spirit zweckzuentfremden. Vorhandene Initialisierung, Wartungswahl und aktueller Sicherheitsstand werden beim Beitritt nicht zurückgesetzt.

### Shared Fuel-Management Services

Alle geeigneten teilnehmenden Reaktorbetreiber einschließlich des Koordinators erhalten **-3% / -5% / -8% Nuclear Fuel Consumption** und **+2% / +3% / +5% Nuclear Plant Upkeep**, jeweils für 728 / 1092 / 1456 aktive Tage. Leser: `nuclear_fuel_consumption_modifier` und `nuclear_infra_cost_multiplier_modifier`.

Basisbudget $15.6B / $31.2B / $62.4B plus $1.04B / $2.08B / $4.16B je Teilnehmer. Vorbereitung 364 / 728 / 1092 bezahlte Tage. Nationale Durchführung und Koordination wie beim Sicherheitsprogramm.

Dies finanziert qualifizierten Betrieb, Brennstoffhandhabung und Betreuung. Es vergibt **keinen** Brennstoffbestand. Die bestehende Verbrauchsberechnung und echte Bestände wirken weiter. Wissen über Brennstofffertigung und vorhandene Reaktoren bleiben Voraussetzungen. Die vollen Resultate von Brennstoffaufbereitung, Zentrifugen oder Brüterforschung werden nicht verschenkt; die vorhandenen zivilen Spezialprojekte bleiben eigenständig.

Eine tatsächliche künftige Brennstofflieferung müsste Lieferant, Bestand, Menge, Preis und Empfängerbedarf explizit vereinbaren und den Lieferantenbestand vor einer Gutschrift vollständig decken. Diese zusätzliche Liefermechanik ist nicht mit einem pauschalen Erzeugungsbuff gleichgesetzt.

### Joint Civilian Reactor Research

Alle beteiligten wissenschaftlichen Einrichtungen beziehungsweise Delegationen, einschließlich des Koordinators, erhalten dieselbe einmalige Forschungsförderung: **1 x +25% / 1 x +35% / 2 x +50% Civilian Reactor Research**. Kein Reaktor ist dafür nötig. Geeignete Forschungseinrichtungen und tatsächlich passende Technologien sind nötig. Keine zusätzliche Bauanlage, kein pauschaler Sicherheitswert und kein Spezialprojektabschluss.

Basisbudget $15.6B / $31.2B / $62.4B plus $1.04B / $2.08B / $4.16B je Teilnehmer. Vorbereitung 364 / 728 / 1092 bezahlte Tage. Nach der einmaligen Leistung gibt es keine weitere RGW-Durchführungsgebühr. Das ist die einfache gemeinsame Variante, wenn alle Unterzeichner dieselbe wissenschaftliche Leistung erhalten sollen, auch bevor sie Reaktoren betreiben.

## 3. Eigene Angebote für jedes andere Programm

Forschungswerte gelten pro vereinbartem Thema, nicht als unbegrenzte allgemeine Forschungsgeschwindigkeit. Die folgende Tabelle beschreibt die wählbaren Leistungen für die anderen zahlenden Teilnehmer. Die jüngst korrigierten fachlichen Host-Anlagen bleiben bei diesen zehn Vorlagen bestehen.

| Programm | Angebot | Konkrete Partnerleistung Limited / Standard / Major |
|---|---|---|
| Intermetal | Steel Extraction and Recovery | +2% / +3% / +5% Resource Extraction für 90 aktive Tage sowie dauerhaft +1 Steel in einem vorhandenen Produktionsstaat je Teilnehmer, einschließlich Host. Aktuelle Regeln in COMECON_SHORT_CYCLES_PROGRAMMES.md, Abschnitt 8. |
| Intermetal | Joint Metallurgy Research | 1 x +15% / 1 x +25% / 2 x +35% Industry Research |
| Intermetal | Steelworks Engineering Teams | +3% / +5% / +8% Civilian Industry Construction Speed |
| Agromash | Machinery and Agronomy Research | 1 x +25% / 1 x +35% / 2 x +50% Agriculture Research |
| Agromash | Mechanisation and Servicing | +3% / +5% / +8% Agricultural District Income |
| Agromash | Farm Machinery Instructors | +10% / +15% / +20% State Productivity Growth in 1 / 2 / 3 geeigneten Agrarstaaten |
| Interkhim | Shared Laboratory Research | 1 x +15% / 1 x +25% / 2 x +35% Industry Research |
| Interkhim | Agrochemical Application Services | +2% / +4% / +6% Agricultural District Income |
| Interkhim | Chemical Quality and Standards | +2% / +4% / +6% Civilian Industry Productivity |
| Wagon Pool | Co-funded Train Deliveries | 1 / 2 / 3 vorhandene Züge je 5% bezahltem Anteil |
| Wagon Pool | Joint Railway Engineering | 1 x +25% / 1 x +35% / 2 x +50% Infrastructure Research |
| Wagon Pool | Freight Terminal Engineering | +5% / +10% / +15% Supply Hub Construction Speed |
| Power Grid | Joint Dispatch and Fuel Economy | -3% / -5% / -8% Fossil Power Plant Fuel Consumption |
| Power Grid | Network Engineering Research | 1 x +25% / 1 x +35% / 2 x +50% Electrification Research |
| Power Grid | Shared Maintenance Services | -3% / -5% / -8% Fossil Power Plant Upkeep |
| Ikarus | Vehicle Engineering Exchange | 1 x +15% / 1 x +25% / 2 x +35% Industry Research |
| Ikarus | Public Transport Operating Programme | -2% / -3% / -5% Non-electric Fuel Consumption |
| Ikarus | Co-funded Depot Access Works | +1 / +1 / +2 Infrastructure Levels und gleich viele Bauplätze je begünstigtem Partner |
| Scientific Information | Computing Documentation Exchange | 1 x +25% / 1 x +35% / 2 x +50% Computing Research |
| Scientific Information | Industrial Technical Information | 1 x +15% / 1 x +25% / 2 x +35% Industry Research |
| Scientific Information | Technical Instructor Exchange | +5% / +10% / +15% National Productivity Growth |
| Precision Bearings | Precision Engineering and Metrology | 1 x +25% / 1 x +35% / 2 x +50% Industry Research |
| Precision Bearings | Machine-tool Training Exchange | +10% / +15% / +20% State Productivity Growth in 1 / 2 / 3 geeigneten Industriestaaten |
| Textile Machinery | Textile Machinery Research | 1 x +25% / 1 x +35% / 2 x +50% Industry Research |
| Textile Machinery | Loom and Mill Training Programme | +10% / +15% / +20% State Productivity Growth in 1 / 2 / 3 geeigneten Industriestaaten |
| Textile Machinery | Textile Quality-control Services | +2% / +4% / +6% Civilian Industry Productivity |
| Material Recovery | Reclamation Engineering Research | 1 x +25% / 1 x +35% / 2 x +50% Construction Research |
| Material Recovery | Material Recovery Methods | 1 x +15% / 1 x +25% / 2 x +35% Excavation Research |
| Material Recovery | Co-funded Industrial Access Works | +1 / +1 / +2 Infrastructure Levels und gleich viele Bauplätze je begünstigtem Partner |

Der Maschinenbau wird damit nicht fälschlich pauschal als militärischer Fabrikausstoß belohnt. Ikarus vergibt keine erfundenen Busbestände und keine Militärfahrzeuge als Ersatz für zivile Busse. Die vorhandenen Wachstums-, Einkommens- und Kraftstoffmodifikatoren bleiben breitere MD-Abstraktionen. Beispielsweise bildet Non-electric Fuel Consumption keine separat gezählte Busflotte ab; der Vertragsname erklärt die bezahlten Maßnahmen, der Effekt nennt ausdrücklich den breiteren nativen Wirkungsbereich.

## 4. Drei verschiedene Verteilungsregeln

1. **Gemeinsames Wissen und einmaliger Ausbau:** Alle zahlenden berechtigten Partner erhalten dieselbe vereinbarte Forschungsförderung beziehungsweise dieselbe mitfinanzierte Infrastrukturstufe. Höhere Anteile stellen zusätzliche Finanzierung bereit und vergrößern diese öffentliche Leistung nicht automatisch individuell. Bei der gemeinsamen Nuklearforschung erhält auch der Koordinator dieselbe Leistung.
2. **Bestandslieferungen:** Die Stückmenge wächst mit dem bezahlten Anteil. Beim Standard-Zugpaket mit SOV 50%, DDR 20%, CZE 10%, Host HUN 20% sind es 20 / 8 / 4 vorhandene Züge und insgesamt 32 Züge als Abgang beim Host. Das frühere Intermetal-Stahlreservenpaket entfällt. Sein Ersatz vergibt die gleiche Förderleistung und +1 Steel pro berechtigtem Teilnehmer, unabhängig von dessen Finanzierungsanteil; der gewählte Investitionsumfang bestimmt die Bonusstärke.
3. **Laufende Fachleistungen:** Außer den ausdrücklich gleichberechtigten gemeinsamen Nuklearbetreiberprogrammen bestimmen die bezahlten Anteile die aktiven Resttage: 182 bei 5%, 364 bei 10%, 728 bei 20%, maximal 1092 ab 30%. Der Umfang bestimmt den jeweiligen fachlichen Effekt. Nationale Durchführung kostet während aktiver Leistung 0.006% / 0.010% / 0.016% des eigenen BIP pro Woche. Einmalige Forschung und Lieferungen lösen diese Gebühr nach Lieferung nicht aus.

Der Host erhält aus seinem Anteil nicht zusätzlich sein eigenes Nicht-Host-Paket, außer beim ausdrücklich auch für ihn vereinbarten Steel Extraction and Recovery. Ein Lieferhost gibt die vertraglichen Waren tatsächlich ab und erhält seine ausdrücklich finanzierten Host-Anlagen. Die gemeinsamen Nuklearbetreiberangebote sowie die gemeinsame Reaktorforschung haben ebenfalls denselben Leistungsanspruch für den Koordinator und die anderen tatsächlichen Teilnehmer.

Nichtzahlende Mitgliedsländer erhalten keine automatische Leistung. Eine erforderliche institutionelle Gründungszustimmung ist von der Liste der eigentlichen Projektbegünstigten zu unterscheiden. Eine SSR hat keinen zusätzlichen Ratsplatz; der Unionsanteil hat einen tatsächlichen Ergebnisempfänger. Dessen echte Bestände, Kapazität, Reaktoren und Kosten sind maßgeblich. Lokale SSR-Durchführung braucht weiterhin gesonderte Zustimmung.

## 5. Finanzierung folgt den gewählten Leistungen

Das hohe Host-Basisbudget bleibt bei den zehn nichtnuklearen Vorlagen bestehen. Das gewählte Angebot fügt eine ausdrücklich sichtbare Partnerbereitstellung hinzu:

* Einmalige Forschung und Bestandslogistik: $0.52B / $1.04B / $2.08B je Partner.
* Laufende Fachprogramme: $1.04B / $2.08B / $4.16B je Partner. Eigene nationale Durchführung während aktiver Leistung zusätzlich wie oben.
* Zusätzliche Infrastruktur: $11.44B / $11.44B / $22.88B je Partner für 1 / 1 / 2 zusätzliche Stufen. Das setzt den hohen Kapitalpreisentwurf fort.
* Nuklearangebote: eigene ausdrücklich oben genannte Basisbudgets, Vorbereitungszeiten und Teilnehmerkosten.

Wenn ein weiterer tatsächlicher Empfänger hinzukommt oder ein anderes Angebot gewählt wird, ändern sich Gesamtbudget und individuelle Wochenrate. Jede solche Änderung braucht eine neue Vertragsfassung und neue Unterschriften. Die Finanzierung wird nicht still automatisch auf andere Länder verteilt. 100% Deckung ist weiter erforderlich. Vorhandene Anlagen-, Arbeitskräfte- und Betriebskosten bleiben bestehen.

Die Host-Betreuung von $12M / $20M / $32M pro Woche läuft nur, solange tatsächlich ein vereinbartes laufendes Host- oder Partnerprogramm aktiv ist. Ein reines einmaliges Forschungs-/Lieferpaket ohne eigenen laufenden Host-Bonus erhält nach Abschluss keine künstliche dauernde Betreuungsgebühr. Aufbau- und Koordinationsleistungen bis zur Fertigstellung sind bereits im unterschriebenen gemeinsamen Budget enthalten.

## 6. Tatsächliche Übergabe und vorhandene Grenzen

**Stahlförderung:** Die frühere Lagerübergabe entfällt. Der aktuelle Entwurf nutzt `local_resources_factor` befristet sowie einmalig `add_resource = { type = steel amount = 1 }` in einem gespeicherten eigenen und kontrollierten Staat mit bestehender Stahlproduktion. Vollständige Teilnahme-, Standort-, Budget- und Ablaufregeln stehen in `COMECON_SHORT_CYCLES_PROGRAMMES.md`, Abschnitt 8. Kein Stahlreservelager wird belastet oder gutgeschrieben.

**Züge:** Es existiert tatsächlich frühes Bahnequipment in `common/units/equipment/mdcw_historical_rail_equipment.txt`: `mdcw_steam_train_equipment_1940`. Es gibt ausdrücklich keine automatischen Startbestände. Die zugehörige frühere Technik steht in `common/technologies/mdcw_early_railway.txt`. Der spätere MD-Typ `train_equipment_1` wird erst über eine spätere Technologie freigegeben und wird hier nicht als kostenlose historische Belohnung verwendet. Die spätere Übergabe braucht vorhandene passende Lagerbestände, einen vereinbarten konkreten Typ und eine gleiche Quellen-/Zielmenge. Keine Erzeugung beliebiger Züge durch ein Geschenk-Event und kein erfundener automatischer Leihvertrag mit versprochener Rückgabe.

**Gebäude:** Auch zusätzliche Partneranlagen benötigen pro Gebäudestufe vorher einen zusätzlichen gemeinsamen Bauplatz im tatsächlich gewählten Staat. Eigentum, Kontrolle, Provinz-/Staatsobergrenzen und echte Anschlüsse werden vor Ausführung erneut geprüft. Die Vorschau zeigt Paketwerte und Voraussetzungen; sie kennt keine aktuellen Provinzen oder Bestände eines laufenden Spielstands.

**Nukleare Altereignisse:** Der bisherige Turnkey-Annahmeweg belastet den Empfänger unmittelbar mit 1.8% seines BIP und schreibt dem Lieferanten 1.35% gut. Der Fertigstellungsweg setzt einen Reaktor direkt im Hauptstadtstaat. Diese Handler dürfen nicht zusätzlich zu einem vollständig finanzierten RGW-Bauvertrag unverändert ausgelöst werden. Das würde eine zweite Zahlung beziehungsweise eine andere Standort- und Abschlusslogik einführen. Ein eigener geprüfter Abschlussadapter muss das gewählte Standortpaket mit Bauplätzen und einmaligem Beleg liefern; die vorhandenen Diplomatie- und Betreiberfunktionen sind dabei fachliche Anschlussstellen.

**Brennstoffverträge:** Die vorhandenen älteren monatlichen Käufer-/Lieferantenläufe sind nicht bereits ein abgesicherter gemeinsamer Reservetransfer: Der Käufer prüft nur positiven Lieferantenbestand und schreibt den gesamten Bedarf gut; die Lieferantenseite bucht separat ab und begrenzt auf null. Für einen neuen gemeinsamen Liefervertrag reicht das nicht als Nachweis vollständiger Bestandsdeckung oder einer atomaren Übergabe. Die bestehenden Dateien werden in dieser Konzeptarbeit nicht geändert. Als Größenordnung entsprechen die dortigen alten Entgelte vor Inflation etwa $0.00462B pro Reaktor und Woche auf Käuferseite beziehungsweise $0.00346B Lieferanteneinnahme. Die hier vorgestellten Betriebsprogramme vergeben ohnehin keinen Brennstoffbestand.

## 7. Stapelung, Forschung und Multiplayer

Gleiche Leistungen werden nicht mehrfach addiert. Die Wahl erfolgt pro Projekt aus dem tatsächlichen Fachkatalog und bleibt beim Wechsel des Registers erhalten. Eine neue Auswahl verwirft alte Unterschriften. Spezialprojektresultate, Technologien, Wartungsregime und bestehende Kooperationsleistungen werden beim Beitritt nicht zurückgesetzt oder pauschal überschrieben.

Für die spätere gemeinsame Verwaltung gelten als RGW-Gruppenobergrenzen: +20% State Productivity Growth aus überlappenden Host- und Partner-Modernisierungen auf demselben Staat, +15 Nuclear Safety Target aus dieser Betreibergruppe und höchstens -8% Nuclear Fuel Consumption aus diesen Brennstoffdiensten. Mehrere gleichartige Verträge dürfen Restzeiten verwalten, vervielfachen aber nicht die Stärke. Vorhandene nationale Technologien und unabhängig erworbene native Ideen werden dabei nicht entfernt oder durch einen globalen Reset verändert.

Forschungszuweisungen benötigen konkrete Themen-/Abschlussbelege. Doppelte Anträge auf dasselbe Thema dürfen nicht durch neue Projektnamen beliebig viele identische Forschungsboni erzeugen. Einmal tatsächlich erbrachtes Wissen bleibt nach Aussetzung vorhanden; eine neue Betriebsphase vergibt es nicht erneut.

Aktive Fachprogramme benutzen begrenzte Teilnehmerlisten und den zentralen Wochenlauf. Nukleare Sicherheit und Flottenalter nutzen die bestehende monatliche Berechnung; es wird kein zweiter paralleler Risiko-Würfel eingeführt. Einmalige Lieferungen, Forschung und Bauabschlüsse brauchen keinen täglichen globalen Suchlauf. Fensteröffnung und Anzeigeänderungen führen keine Zahlungen oder Lieferungen aus.

## 8. Quellen und Herkunft

Lokale Dateien wurden am 24. Oktober 2026 gelesen. Die obigen Werte und neuen Vertragskombinationen sind eigene Balancevorschläge, keine behaupteten historischen Konditionen oder native bereits vorhandene RGW-APIs.

* [IAEA-TECDOC-922](https://www-pub.iaea.org/MTCD/Publications/PDF/te_0922_scr.pdf): internationale WWER-Zusammenarbeit, Komponentenversorgung, Betriebserfahrung und zentralisierte Ausbildung für Betreiber aus verschiedenen Ländern. Der Bericht beschreibt unter anderem das Ausbildungszentrum in Nowoworonesch. Er begründet die institutionellen Tätigkeiten, nicht die hier verwendeten Zahlen.
* [UNIDO 1978: Institutional mechanisms](https://downloads.unido.org/ot/47/91/4791252/00001-10000_07981_1978.pdf): unterschiedliche Fachorganisationen und Kooperationsleistungen. Intermetal arbeitete unter anderem mit vertraglich benannten Mengen und Sortimenten von Metalllieferungen; daraus folgt kein historischer universeller nationaler +5%-Bonus.
* Weitere vorhandene Leser: `00_money_system.txt` für Agrar-/Industrieeinkommen und Kraftwerksunterhalt, `!_energy_effects.txt` für tatsächlichen Brennstoffverbrauch und Nuklearversorgung, `00_productivity_effects.txt` für echte Wachstumsmodifikatoren. Die Forschungskategorien sind in `common/technology_tags/00_technology.txt` und tatsächlichen Technologien vorhanden. `production_speed_supply_node_factor` besitzt vorhandene MD-Ideenbeispiele.

Eigenständiger Konzepttext und interaktive UI für IMPERIA COLD WAR. Native Systeme: Paradox Interactive, MD-Team und Projektbeitragende. Die vorhandenen Bildquellen und unbekannten Einzelrechte sind weiterhin in der Vorschau-Provenienz dokumentiert; Nutzerlogo und aktuelle Länderflaggenvorgabe bleiben erhalten. Keine Änderungen an den vorhandenen Nuklear-, Uranium-, Wirtschafts- oder Technologie-Laufzeitdateien.

Prüfung der Konzeptvorschau: 529 Interaktionsprüfungen bestanden, einschließlich sämtlicher 33 Angebote in drei Umfängen und vier Empfängersichten, tatsächlicher Kostenaufschläge, Quellen-/Zielmengen, gemeinsamer Nuklearleistungen, alter Vertragsmigration und SSR-/Abstimmungsregeln. Sechs Browserfälle für Reaktorbau, Sicherheit, gemeinsame Forschung, Stahl, Züge und Partnerinfrastruktur zeigten bei 1024 beziehungsweise 320 Pixel keine fehlenden Bilder oder horizontalen Überläufe. Diese Nachweise betreffen die Vorschau, keine native Welt-, Bestands-, Provinz- oder Multiplayerprüfung. Der exportierte Vertragskatalog und die Prüfberichte liegen neben der Vorschau.
