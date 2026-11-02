IMPERIA COLD WAR: Programme-specific Host Deliveries
==================================================

Aktuelle Vertrags- und Nuklearrevision: [COMECON_AGREEMENT_CATALOGUE.md](COMECON_AGREEMENT_CATALOGUE.md). Die zwei universellen Partneroptionen sind durch 33 fachliche Angebote ersetzt. Insbesondere die Nuklearangebote haben jetzt eigene Bau-, Betriebs-, Sicherheits- und Forschungspakete samt Kosten und Bedingungen; die früheren Nuklear- und allgemeinen Partnerangaben unten sind insoweit überholt.

Stand: 24. Oktober 2026. Vorrangige Korrektur zu `COMECON_SCALE_DAYS_PROGRAMMES.md`. Der Nutzer beanstandet die bisher fast durchgängige Vergabe von Zivilfabriken. Diese Revision ersetzt die Host-Pakete aller elf zivilen Vorlagen. Hohe gemeinsame Budgets, selbst gewählte Beiträge, skalierende Partnerpakete, aktive Tage, das Nutzerlogo, aktuelle Ingame-Flaggen und SSR-Regeln bleiben erhalten. Konzept und interaktive Vorschau; keine native Laufzeitimplementierung.

## Grundsatz

Der Host erhält die konkret finanzierte Leistung: neue Fertigung, einen Anschluss, einen Güterknoten, Agrarkapazität, einen Informationsdienst oder die Modernisierung bereits vorhandener Anlagen. Eine Fachorganisation ist für sich genommen keine neue Fabrik. Die Bezeichnung des Programms und seine tatsächlich ausgewiesenen Effekte müssen zusammenpassen.

Zivile Fabriken bleiben bei drei Vorlagen sinnvoll: Metallurgie, Spezialchemie und Fahrzeugmontage. Das native Spiel besitzt für diese drei Produktionsbereiche keinen jeweils eigenen Gebäudetyp. `industrial_complex` ist hier die ehrliche gemeinsame Gebäudeabstraktion. Eine Spezialchemieanlage wird nicht zur synthetischen Raffinerie umbenannt, die im untersuchten MD-System andere konkrete Produkte erzeugt. Eigene Stahlwerke, Chemiewerke oder Textilfabriken wären eine neue Gebäudemechanik und werden nicht als bereits vorhanden ausgegeben.

## Konkrete Host-Pakete

Die Spalten zeigen Limited / Standard / Major. Alle Forschungsboni gelten einmal für jeweils eine passende Technologie. Die Stärke des separat gewählten Partnerpakets bleibt +3% / +5% / +8%; dessen Laufzeit folgt weiterhin dem bezahlten Länderanteil.

| Programm | Dauerhafte Host-Anlagen | Weitere Host-Leistung |
|---|---|---|
| Intermetal | +1 / +2 / +3 civilian factories; +1 / +1 / +2 infrastructure levels | Keine zusätzliche pauschale Host-Prämie |
| Agromash Mechanisation | +1 / +2 / +3 agricultural district levels in einer bestehenden Agrarregion | 1 x +15% / +25% / +35% Agriculture research bonus |
| Interkhim | +1 / +2 / +3 civilian factories als Spezialchemie-Kapazität | 1 x +15% / +25% / +35% Industry research bonus |
| Common Wagon Pool | +1 / +2 / +3 infrastructure levels; +1 / +1 / +2 supply hubs | Keine automatisch erfundene Bahnstrecke |
| United Power Grid | +1 / +2 / +3 infrastructure levels als Anschluss- und Zugangsinvestition | -3% / -5% / -8% fossil power plant fuel consumption für 728 / 1092 / 1456 active days |
| Ikarus | +1 / +2 / +4 civilian factories als Fahrzeugmontage und Zulieferfertigung | Keine zusätzliche pauschale Host-Prämie |
| Scientific Information Network | +1 / +2 / +3 offices | 1 x +15% / +25% / +35% Computing research bonus |
| Interatomenergo | +1 / +2 / +3 civilian nuclear reactors | Native Brennstoff-, Energie-, Personal- und Betriebskosten gelten weiterhin |
| Precision Bearings | Keine zusätzlichen Gebäude | +10% / +15% / +20% State Productivity Growth in 1 / 2 / 3 vereinbarten Industriestaaten für 728 / 1092 / 1456 active days; 1 x +15% / +25% / +35% Industry research bonus |
| Textile Machinery | Keine zusätzlichen Gebäude | +10% / +15% / +20% State Productivity Growth in 1 / 2 / 3 vereinbarten Industriestaaten für 728 / 1092 / 1456 active days; 1 x +15% / +25% / +35% Construction research bonus |
| Material Recovery and Reclamation | +1 / +2 / +3 infrastructure levels für Zugang und Standorterschließung | +3% / +5% / +8% civilian industry construction speed für 728 / 1092 / 1456 active days |

Es werden nicht aus Gründen der Abwechslung beliebige Gebäude verteilt. Kugellager- und Textilprogramme können beide eine vorhandene industrielle Basis modernisieren. Der konkrete Branchenbezug wird über Vertrag, Standort, Beschreibung und geeignete Forschung festgelegt. MDs staatlicher Wachstumsmodifikator bleibt eine breitere Abstraktion und simuliert keine separat gezählte Kugellager- oder Textilproduktion.

Bei Agromash finanziert die gewählte Vorlage die Lieferung und Anwendung von Maschinen, Lagertechnik und Dienstleistungen in einer vorhandenen Agrarregion. Die zusätzlichen nativen Agrardistriktstufen stehen für den Ausbau ihrer agroindustriellen Kapazität. Die Vorlage behauptet nicht, eine Landmaschinenorganisation habe automatisch neues Ackerland geschaffen. Eine spätere separate Landmaschinenfabrik wäre wieder ein eigener Industriebauvertrag.

## Anforderungen und Grenzen

* Metallurgie und Chemie: geeignetes kontrolliertes Industriegebiet, Rohstoffversorgung, Baukapazität und passende Technik. Keine freien Rohstoffvorkommen.
* Agrarprogramm: vorhandene Agrardistrikte, zusätzlicher Ausbau unter deren tatsächlicher Obergrenze, Arbeitskräfte und nationale Durchführung.
* Wagenpool: konkrete kontrollierte Verkehrsstandorte, geeignete Provinzen ohne bereits vorhandenen maximalen Supply Hub und eine tatsächliche Bahnverbindung. Ein Supply Hub allein erzeugt keine funktionierende Bahnlogistik. Die native Datei begrenzt `supply_node` auf eine Stufe je Provinz; mehrere Hubs benötigen verschiedene Provinzen.
* Stromnetz: vorhandene thermische Erzeugung, konkrete Anschlussstaaten und ein Vertrag der beteiligten Netzbetreiber. Eine Netzkopplung vergibt keine neuen Kraftwerke. Infrastruktur und Brennstoffeffizienz abstrahieren Anschlussbau und bessere Systemauslastung. Tatsächliche grenzüberschreitende Stromflüsse sind damit noch nicht implementiert.
* Ikarus: Montage-, Lizenz- oder Zuliefervertrag. Die Auswahl eines Landes gewährt keine fremden Fahrzeugentwürfe.
* Informationsnetz: beteiligte wissenschaftliche Einrichtungen, geeigneter Dienstleistungsstandort und tatsächlich verfügbare Computing-Technologie. Keine universelle Forschungsbeschleunigung.
* Kernenergie: Reaktorstandort, Technik, Netzanschluss, Brennstoffversorgung, Personal und Betriebsmittel.
* Kugellager/Textilien: für den gewählten Umfang 1 / 2 / 3 konkret benannte, kontrollierte Staaten mit bestehender ziviler Industrie. Wachstumseffekte gleicher Modernisierungsgruppen werden auf demselben Staat nicht addiert. Beide Gruppen zusammen höchstens +20% State Productivity Growth; die laufenden Ansprüche und ihre Restdauer bleiben getrennt nachprüfbar.
* Rekultivierung: bestehender industrieller Umbaubereich und Kapazität für die Zugangsinvestition. Der native nationale Baubonus ist eine grobe wirtschaftliche Abstraktion, keine Simulation einer Abraum-Massenbilanz. Keine erfundenen Kohlevorkommen, frei erzeugten Metallbestände oder still hinzugefügten Bergwerke.

Für **jede** tatsächlich vergebene Gebäudestufe wird vorher ein zusätzlicher gemeinsamer Bauplatz im selben Staat gewährt. Infrastruktur, Supply Hubs und Kernreaktoren sind eingeschlossen. Modernisierungsmodifier und Forschungsboni erhalten keine Bauplätze. Mehrere Gebäude in verschiedenen Staaten brauchen jeweils ihre eigene Zuweisung; die native Vorschau muss die tatsächlichen Staaten, Provinzen und Zahlen zeigen. Die Konzeptvorschau zeigt zunächst die Paketgesamtwerte und benennt die Standortanforderungen, ohne einen Live-Spielstand oder echte Provinzprüfung vorzutäuschen.

## Ablauf und Kosten

Die teuren Gesamtbudgets und bezahlten Vorbereitungs-/Bauzeiten bleiben wie in der vorherigen Revision. Die neuen Leistungspakete sind Balancevorschläge und noch nicht anhand eines Spielstands auf Rendite getestet. Die Preise werden nicht automatisch gesenkt, nur weil ein Programm vorhandene Kapazität verbessert.

Bauprojekte vergeben die vereinbarten Anlagen einmalig nach vollständiger bezahlter Fertigstellung und erneut geprüfter Standortberechtigung. Reine Modernisierungsvorlagen zeigen **Paid preparation**, keine fiktive Bauleistung. Nach bezahlter Vorbereitung beginnen ihre finanzierten Host-Programme. Host-Laufzeiten betragen 728 / 1092 / 1456 aktive Tage und hängen am Umfang, nicht am eigenen Finanzierungsanteil. Die Nicht-Host-Laufzeit hängt weiter am Anteil. Ausgesetzte Zeit wird nicht als erbrachte Leistung abgebucht.

Forschungsboni entstehen einmal bei erfülltem Abschluss. Erneute Fensteröffnung, Vertragswiederaufnahme oder Überschreiben eines Modifiers dürfen sie nicht erneut vergeben. Exakt identische Folgeprojekte dürfen keine billige Quelle unbegrenzter Forschungsboni werden; ein neuer Vertrag braucht einen tatsächlich neuen Modernisierungsumfang beziehungsweise neue geeignete Standorte.

Die Betreuung kostet den Host $12M / $20M / $32M pro Woche, solange mindestens ein vertragliches Host- oder Partnerprogramm aktiv ist. Wenn das Host-Paket einen zeitweiligen eigenen Betriebs-/Modernisierungsbonus enthält, zahlt er während dessen aktiver Laufzeit zusätzlich 0.006% / 0.010% / 0.016% seines eigenen BIP pro Woche. Gebäudeunterhalt und nationale Arbeitskräfte-/Energiesysteme gelten zusätzlich. Die spätere Spiel-UI muss diese Kosten als tatsächliche Zahlen vor Zustimmung auflösen.

Ein Host bekommt keinen zweiten Nicht-Host-Bonus aus seinem Finanzierungsanteil. Eigene zeitweilige Wirkungen eines Host-Pakets, beispielsweise der Stromnetzbetrieb, sind ausdrücklich vereinbarte Host-Leistungen. Der sowjetische Anteil wird weiterhin genau einem Empfänger zugewiesen; eine SSR als Host erzeugt keine zusätzliche sowjetische Teilnehmerprämie. Neue Kosten und Leistungen benötigen neue Unterschriften. Die Vorschau bewahrt die bisher gewählten Länder, Anteile, Umfang und Partneroption, verwirft aber die Zustimmung zu alten Host-Paketen.

## Historischer und technischer Nachweis

[UNIDO 1978: Institutional mechanisms](https://downloads.unido.org/ot/47/91/4791252/00001-10000_07981_1978.pdf) beschreibt Netzverbindungen und koordinierte Stromversorgung, abgestimmte Metallkapazitäten, landwirtschaftliche Maschinen und deren Anwendung, Spezialisierung bestehender Betriebe, Wagenpool, Textilmaschinen und wissenschaftliche Information. Diese Aufgaben begründen die Unterscheidung zwischen Neubau und Verbesserung vorhandener Kapazitäten. Die konkreten Gebäudezahlen und Modifier bleiben eigenständige Spielvorschläge.

Lokale Quellen, am 24. Oktober 2026 gelesen:

* `common/buildings/00_buildings.txt`: vorhandene Gebäude, Wirkungen und Obergrenzen. Keine neuen Gebäudedefinitionen für diesen Entwurf.
* `common/technology_tags/00_technology.txt` und vorhandene Technologien: `CAT_agriculture`, `CAT_industry`, `CAT_construction`, `CAT_computing`. Vorhandene native Forschungsbonus-Beispiele verwenden diese Kategorien.
* `common/modifier_definitions/money_modifier_definitions.txt`: `state_productivity_growth_modifier` ist ein Staatsmodifikator.
* `common/scripted_effects/00_productivity_effects.txt`: der Modifier multipliziert den positiven Wachstumszweig mit bestehenden Aufholregeln. +20% Wachstumsmodifier sind weder +20% aktueller Output noch 20 Prozentpunkte jährliches Wachstum.
* `common/scripted_effects/!_energy_effects.txt`: tatsächlicher Leser für `fossil_pp_fuel_consumption_modifier`. Niedrigerer Wert senkt den ermittelten Brennstoffverbrauch vorhandener fossiler Erzeugung.
* `common/scripted_effects/99_investment_scripted_effects.txt`: vorhandene gebäudespezifische Baugeschwindigkeitswerte. Der nationale Baubonus verwendet einen bestehenden Effekt, keinen erfundenen Rekultivierungsmodifier.

Prüfung der Konzeptvorschau: 62 Interaktionsprüfungen bestanden, darunter die drei verbliebenen Civ-Vorlagen, gemischte Gebäudepakete und Bauplätze, Agrar- und Forschungsleistungen, befristete Modernisierung, Umfang, Anteilslaufzeiten, neue Zustimmung und SSR-Zuweisung. Vier Browseransichten für Güterverkehr, Modernisierung, Agrar und Stromnetz hatten keine fehlenden Bilder oder horizontalen Überläufe; geprüft bei 1024 beziehungsweise 320 Pixel Inhaltsbreite. Dies belegt keine native Provinzprüfung oder Multiplayer-Stabilität.

Eigenständiger Konzepttext und UI-Logik für IMPERIA COLD WAR. Native Systeme und vorhandene Grafiken stammen von Paradox Interactive, MD-Team und Projektbeitragenden, soweit bekannt. Individuelle Bildrechte bleiben in der bestehenden Vorschau-Provenienz dokumentiert beziehungsweise unbekannt. Nutzerlogo und aktuelle Flaggenvorgabe bleiben unverändert.
