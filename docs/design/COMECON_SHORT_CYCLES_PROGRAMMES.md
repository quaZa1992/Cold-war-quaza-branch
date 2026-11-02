IMPERIA COLD WAR: Short Project Cycles and Independent Joint Programmes
======================================================================

Stand: 24. Oktober 2026. Vorrangige Nutzerkorrektur zu `COMECON_AGREEMENT_CATALOGUE.md`: nur eine Host-Gebäudestufe je Gebäudetyp, ungefähr drei Monate Projektdauer, danach ungefähr drei Monate Partnerleistungen sowie eigenständige sechsmonatige Gemeinschaftsprogramme. Nach Rückfrage lehnt der Nutzer einen in 90 Tagen geschenkten Reaktor ausdrücklich ab und wünscht dort höchstens eine passende Baugeschwindigkeitsförderung. Konzept und bedienbare Vorschau; keine native Laufzeitimplementierung.

## 1. Gebäude: genau eine Stufe je Host-Gebäudetyp

Limited, Standard und Major vergeben beim Hauptland jeweils höchstens **eine Stufe des vereinbarten Gebäudetyps**. Beispielsweise gibt Ikarus auch bei Major nur +1 civilian factory und vorher +1 shared building slot. Intermetal hat zwei tatsächlich vereinbarte Gebäudetypen: +1 civilian factory und +1 infrastructure level. Dafür sind insgesamt zwei zusätzliche Bauplätze nötig, jeweils im tatsächlich betroffenen Staat vor dem Gebäude.

Agromash erhält eine Agrardistriktstufe, der Wagenpool eine Infrastrukturstufe und einen Supply Hub, das Informationsnetz ein Büro. Modernisierung ohne Bau erhält weiterhin keine erfundenen zusätzlichen Gebäude oder Bauplätze. Keine pauschale Umschreibung aller Leistungen in einen einzigen Bauplatz.

Die Begrenzung betrifft ausdrücklich das Hauptland. Bereits separat finanzierte Partneranlagen, etwa die 1 / 1 / 2 Infrastrukturstufen bei entsprechenden Auslands-Angeboten, bleiben unverändert. Bonusstärken, Zielstaatenzahl, Lieferquoten und übrige nichtzeitliche Werte bleiben erhalten, soweit die unten genannten Änderungen keine andere Leistungsart verlangen. Die hohen Budgets werden nicht automatisch entsprechend der geringeren Gebäudemenge gesenkt.

## 2. Ein 90-Tage-Projekt mit anschließenden 90-Tage-Leistungen

Alle elf bisherigen Projekteinträge und ihre 33 Vertragsvarianten verwenden jetzt **90 finanzierte Projekttage**. Nach bezahltem Abschluss folgen bei Betriebs-, Ausbildungs- und Forschungsleistungen **90 aktive Tage**. Die 5%-Mindestbeteiligung und selbst gewählte Finanzierung bleiben erhalten. Unterschiedliche Finanzierungsanteile ändern die individuelle Zahlung und gegebenenfalls Liefermenge, nicht mehr die Laufzeit des Partnerbonus. Der Umfang bestimmt weiterhin die fachliche Stärke.

Vorhandene Host-Modernisierungswirkungen werden ebenfalls auf 90 aktive Tage begrenzt. Dauerhafte einmalig gebaute Anlagen, tatsächlich übergebene Züge und die unten beschriebene Verbesserung vorhandener Stahlproduktion werden nach 90 Tagen nicht wieder gelöscht. Sie sind einmalige Vertragsleistungen und keine zeitweiligen Modifier. Die frühere Lieferung von Stahlreserven entfällt.

Für den Spielfluss gelten feste 90 Tage als ungefähr drei Monate. Dies ist eine gewünschte Abstraktion des Multiplayer-Tempos und keine Behauptung, jedes der realen Industrievorhaben sei historisch in drei Monaten fertiggestellt worden.

## 3. Reaktorunterstützung statt sofortigem Reaktor

Die frühere Variante `Joint Reactor Construction` wird zu **Reactor Construction Support**. Alle geeigneten tatsächlichen Teilnehmer einschließlich des Koordinators erhalten für 90 aktive Tage:

* +5% / +10% / +15% Nuclear Reactor Construction Speed über den vorhandenen Modifier `production_speed_nuclear_reactor_factor`.
* +15% / +25% / +35% Civilian Reactor Research Speed als zeitweiliger Fachforschungsbonus.

Es werden keine Reaktoren, Bauplätze, Uraniumvorkommen, Minen, Anreicherungsanlagen oder fertigen Technologien vergeben. Passende Technik, genehmigte Bau- beziehungsweise Betreiberrechte, Standort, Lieferpartner und Brennstoffversorgung bleiben erforderlich.

Der vorhandene normale Reaktorbau kann vom Baugeschwindigkeitsmodifier profitieren. Das alte schlüsselfertige Angebot hat dagegen einen fest geplanten Fertigstellungstermin nach 1460 Tagen in `events/COLDWAR_nuclear_power_events.txt`; ein normaler Construction-Speed-Modifier verkürzt diesen Eventtermin nicht. Der Entwurf verändert diesen bestehenden Vertrag nicht. Diese Einschränkung steht auch bei den Teilnahmebedingungen der Bauunterstützung.

Die Dienstleistungsvariante verwendet ein eigenes Basisbudget von $10.4B / $20.8B / $41.6B zuzüglich $1.04B / $2.08B / $4.16B je Teilnehmer. Der frühere Preis eines vollständigen neuen Kernkraftwerks wird damit nicht als Dienstleistungspreis ausgegeben. Die anderen drei Nuklearangebote behalten ihre fachlichen Werte, erhalten aber ebenfalls den 90-Tage-Projektzyklus und 90 aktive Leistungstage. Sicherheitsziel, monatliche Annäherung, national gewähltes Wartungsregime und echte Brennstoffberechnung bleiben Bestandteil des vorhandenen Nuklearsystems.

## 4. Forschung ist jetzt tatsächlich zeitlich begrenzt

Die neu vereinbarte Forschungsförderung wird als befristete **Research Speed** für die konkrete Technologiegruppe konzipiert. Sie verwendet `research_bonus = { CAT_... = Wert }` in einem zeitweiligen, eindeutig diesem Vertrag zugeordneten Spirit. Solche Kategorieblöcke existieren bereits in normalen MD-Länderideen, beispielsweise `common/ideas/05_china.txt`, und nicht nur bei Designfirmen.

Die bisherige Anzeige `1 x` beziehungsweise `2 x` eines unbegrenzt vorgehaltenen Tech-Bonus entfällt bei diesen neuen RGW-Verträgen. Die Prozentwerte bleiben erhalten; der Bonus endet nach 90 beziehungsweise 180 aktiven Tagen. Tatsächlich bereits erzielter Forschungsfortschritt und fertig erforschte Technik werden nicht rückgängig gemacht. Andere nationale oder früher erworbene Forschungsboni werden nicht entfernt. Ein einfaches `add_tech_bonus` wird nicht mit einer unbewiesenen Ablauf-Funktion versehen.

## 5. Eigenständiges Register: Joint Programmes

Neben dem bisherigen Projektregister gibt es ein getrenntes Register mit **elf unabhängigen Gemeinschaftsprogrammen**. Sie benötigen keinen aktiven Ikarus-, Intermetal- oder anderen Investitionsvertrag. Die tatsächliche RGW-Mitgliedschaft und die realen jeweiligen Sektorbedingungen bleiben erforderlich. Die feste Mitgliedsliste der Vorschau ersetzt keine spätere Mitgliedschaftsprüfung in der Laufzeit.

Ein Gemeinschaftsprogramm beginnt mit der ratifizierten, finanzierten Durchführung und läuft **180 aktive finanzierte Tage**. Die Effekte gelten während dieser 180 Tage. Es gibt nicht erst sechs Monate Vorbereitung und danach weitere sechs Monate Bonus. Alle tatsächlichen berechtigten Teilnehmer einschließlich des Koordinators erhalten dieselbe Stärke und Laufzeit. Eine SSR bleibt Empfänger der einen sowjetischen Zuweisung mit lokaler Durchführungsgenehmigung, ohne zusätzliche Ratsstimme.

| Gemeinschaftsprogramm | Limited / Standard / Major | Reale native Wirkung und Bedingung |
|---|---|---|
| Material Supply Management | -5% / -10% / -15% Factory Resource Shortage Production Penalty | `production_lack_of_resource_penalty_factor`; geringere Produktionsverluste bei Rohstoffmangel, keine behauptete Senkung der verbrauchten Ressourcenmenge. Militärische Produktion und gesonderte militärisch-technische Vereinbarung nötig. |
| Resource Recovery Programme | +3% / +5% / +8% Resource Extraction | `local_resources_factor`; erhöht den Ertrag bereits entwickelter Ressourcenproduktion. Ein nur untersuchtes Vorkommen produziert dadurch nichts. |
| Production Planning Programme | +5% / +10% / +15% Military Factory Efficiency Growth | `production_factory_efficiency_gain_factor`; vorhandene militärische Fertigung und gesonderte militärisch-technische Vereinbarung nötig. |
| Production Standardisation | +3% / +5% / +8% Military Factory Maximum Efficiency | `production_factory_max_efficiency_factor`; kein allgemeiner Angriffswert und keine zivile Steuereffizienz. Gleiche militärischen Vertragsvoraussetzungen. |
| Labour Productivity Programme | +5% / +10% / +15% National Productivity Growth | `country_productivity_growth_modifier`; bezahlt Fachausbilder und Arbeitsorganisation. Beschleunigt den vorhandenen Wachstumsansatz, kein sofortiger gleich großer BIP-Sprung. |
| Industrial Quality Control | +2% / +4% / +6% Civilian Industry Productivity | `civilian_factories_productivity`; vorhandene zivile Industrie und nationale Prüfinstitutionen. Native MD-Steuer-/BIP-Abstraktion. |
| Power Station Maintenance | -3% / -5% / -8% Fossil Power Plant Upkeep | `fossil_infra_cost_multiplier_modifier`; vorhandene Kraftwerke und nationale Wartungsorganisation. |
| Fuel Economy Programme | -2% / -3% / -5% Non-electric Fuel Consumption | `non_electric_fuel_consumption_modifier`; nationale Verbrauchs- und Wartungsmaßnahmen. Breiter nativer Wirkungsbereich, keine separat simulierte Busflotte. |
| Agricultural Extension | +3% / +5% / +8% Agricultural District Income | `agriculture_district_income_tax_modifier`; vorhandene Agrardistrikte und bezahlte Beratung beziehungsweise Maschinenbetreuung. |
| Infrastructure Engineering Teams | +5% / +10% / +15% Infrastructure Construction Speed | `production_speed_infrastructure_factor`; tatsächliche nationale Bauvorhaben bleiben gesondert zu bezahlen. |
| Scientific and Technical Exchange | +10% / +15% / +20% Computing Research Speed | Zeitweilige Kategorie-Forschungsförderung über `CAT_computing`; passende Forschungseinrichtungen und Technologie. |

Damit wird der allgemeine Wunsch nach Ressourceneffizienz durch zwei klar benannte, tatsächlich vorhandene Mechaniken abgebildet: Ertragsverbesserung und geringere Mangelverluste. Es wird kein erfundener universeller Resource Consumption Modifier versprochen. Eine echte direkte Senkung aller Materialinputs wäre eine weitere getrennt zu entwickelnde Mechanik.

Die beiden Programme für Produktionslinien und das Materialmangelprogramm haben militärische native Wirkungen. Sie werden nicht als ausschließlich zivile Effekte getarnt. Ihre zusätzliche Abkommensvoraussetzung ist Teil dieses Konzepts, keine als vorhanden behauptete neue Runtime-API oder automatische Teilnahme aller RGW-Länder am Warschauer Pakt.

## 6. Hohe Budgets und korrekte Wochenabrechnung

Bei den bisherigen nichtnuklearen Projekten bleiben die hohen Gesamtbudgets und die bereits ausgewiesenen Empfängeraufschläge bestehen. Weil die Finanzierung nun in 90 Tagen erfolgt, steigt die Wochenrate entsprechend. Das ist die Folge des vom Nutzer gewünschten kürzeren Takts und keine still reduzierte Rechnung.

Für die neuen Gemeinschaftsprogramme gilt als erster Kostenentwurf:

* Basisbudget $5.2B / $10.4B / $20.8B plus $0.52B / $1.04B / $2.08B je tatsächlichem Teilnehmer.
* Power Station Maintenance hat wegen der spezialisierten Leistungen $7.8B / $15.6B / $31.2B als Basis, denselben Teilnehmeraufschlag.
* Laufende nationale Durchführung bei Fachleistungen weiterhin 0.006% / 0.010% / 0.016% des eigenen BIP pro Woche. Beim reinen befristeten Forschungsangebot ist die vereinbarte Forschungsbetreuung im gemeinsamen Budget enthalten.
* Beim 180-Tage-Programm ist die gemeinsame Koordination bereits im laufenden gemeinsamen Budget enthalten. Sie wird dem Koordinator nicht zusätzlich nochmals als private Koordinationsgebühr berechnet.

Beispiel Standard mit vier Teilnehmern: $14.56B gemeinsames Budget für 180 Tage, entsprechend ungefähr $0.56622B pro Woche. Finanzierungsanteile bestimmen die jeweilige Wochenzahlung; die Fachleistung bleibt für jeden gleich.

Berechnung: `Wochenrate = Gesamtbudget * 7 / Laufzeittage`. 90 und 180 Tage werden nicht einfach als 13 beziehungsweise 26 volle Wochen abgerechnet. Die erste vereinbarte Teilzahlung kann die Aktivierung finanzieren; jede weitere Zahlung wird gegen das verbleibende Vertragsbudget begrenzt. Für einen 90-Tage-Zyklus entsprechen zwölf volle Wochenraten und eine Restabrechnung für sechs Tage dem Gesamtbudget; bei 180 Tagen sind es 25 volle Wochenraten und fünf Resttage. In einer Umsetzung mit Teilzahlungsbeginn bei Ratifikation sind dies vorausbezahlte Leistungsabschnitte, keine zusätzliche Startgebühr.

Runtime-Beträge bleiben in wöchentlichen MD-Einheiten. Native Literale höchstens fünf Nachkommastellen; die letzte Rechnung benutzt den tatsächlich offenen Restbetrag, damit Rundung weder Geld erzeugt noch zu viel abbucht. Ein offenes Fenster und eine Anzeigeaktualisierung buchen keine Zahlung. Ein Vertrag ohne gedeckte Finanzierung darf nicht trotzdem alle Bufftage verbrauchen und anschließend gratis verlängert werden.

## 7. Unterbrechung, Stapelung und Performance

Aktive Resttage und bereits bezahlte Budgetanteile werden getrennt geführt. Bei Aussetzung werden nur die diesem Vertrag gehörenden laufenden Effekte entfernt beziehungsweise pausiert. Geleistete Lieferungen und einmalige Gebäude bleiben erhalten. Wiederaufnahme füllt weder Geld noch Laufzeit auf und vergibt keine zweite Anlage.

Ein Programm derselben Fachgruppe wird nicht mehrfach addiert. Treffen ein 90-Tage-Projekteffekt und ein entsprechendes 180-Tage-Gemeinschaftsprogramm zusammen, gilt für dieselbe Gruppe die stärkste berechtigte Leistung; eigenständige Restlaufzeiten bleiben nachprüfbar. Es gibt keinen globalen Reset bestehender nationaler Technologien, Geister oder Forschung. Die vorhandenen Vorgaben für konkrete Zustimmungs- und Effektvorschauen bleiben maßgeblich.

Die spätere Abrechnung benötigt nur aktive Projekt-/Programm- und Teilnehmerlisten, einen Wochenlauf und gezielt geplante Abschluss-/Ablaufereignisse. Kein neuer täglicher Länder-/Staatenvollscan. Kurzfristige finanzierte Leistungsabschnitte können an die bezahlten Resttage gebunden werden; eine versäumte Rate darf nicht unbegrenzt ein langes Gratis-Spirit laufen lassen. Nukleare Sicherheitsannäherung und bestehende Flottenverwaltung bleiben beim vorhandenen monatlichen System.

## 8. Intermetal: Förderung und Standortverbesserung statt Stahlreserven

Die Nutzerrevision ersetzt `Agreed Steel Deliveries` durch **Steel Extraction and Recovery**. Nach 90 finanzierten Projekttagen erhält jedes tatsächlich teilnehmende berechtigte Land, einschließlich des Hauptlands:

* +2% / +3% / +5% Resource Extraction für 90 aktive Tage, abhängig von Limited / Standard / Major. Nativer Länder-Modifier: `local_resources_factor`. Der native Wirkungsbereich umfasst die vorhandene Ressourcenförderung des Empfängers, nicht ausschließlich Stahl.
* Dauerhaft +1 Steel im Rohstoffbasiswert genau eines vereinbarten, eigenen und kontrollierten Staats mit bereits bestehender entwickelter Stahlproduktion. Die eine Einheit bleibt in allen Investitionsstufen gleich. Sie ist weder +1 jeder Rohstoffart noch eine Lagergutschrift oder garantierter Nettoexport nach Technologie-, Handels- und anderen Modifikatoren.

Das Hauptland behält seine unveränderten +1 Civilian Factory und +1 Infrastructure Level mit vorher insgesamt zwei zusätzlichen Bauplätzen. Die neue Rohstoffleistung kommt ausdrücklich auch dort hinzu. Der sowjetische Anteil hat weiterhin nur einen tatsächlichen Empfänger: Union oder vereinbarte SSR, keine doppelte Zuteilung und keine weitere Ratsstimme. Nicht teilnehmende Länder erhalten keinen Ausbau.

Das Programm bildet verbesserte Förderung und Rückgewinnung an bestehenden Produktionsstätten ab. Es erzeugt keine neuen Vorkommen, Uraniumproduktion oder Uraniumminen. Hat ein Land keinen geeigneten Stahlstandort, ist diese Vertragsvariante für dieses Teilnehmerpaket nicht verfügbar; andere Intermetal-Angebote bleiben Alternativen. Die konkrete Standortwahl wird bei Vertragsannahme gespeichert und beim Abschluss erneut geprüft. Fehlt dann die Berechtigung, wird die betreffende Zuteilung ausgesetzt, statt heimlich einen anderen Staat oder Rohstoff zu verwenden.

Bei nativer Umsetzung wird `add_resource = { type = steel amount = 1 }` im gespeicherten Staat genau einmal gebucht. Nachweis: Die vorhandenen `00_resources_expansion_decisions.txt` verwenden bereits `has_resources_amount` und `add_resource` für den Ausbau vorhandener Förderung. Dies belegt die technische Wirkung, keine historische RGW-Prämie. Eigentum und Kontrolle werden zusätzlich geprüft. Der Vertragsbeleg verhindert Wiederholung durch erneut geöffnete Vorschauen, Wiederaufnahme oder doppelte Abschlussereignisse. Derselbe Stahlstandort erhält diesen RGW-Ausbau nur einmal; eine weitere Investition benötigt ein anderes geeignetes Ausbaugebiet. Ein Rohstoffausbau ist kein Gebäude und bekommt deshalb keinen erfundenen Bauplatz.

Der kleine 90-Tage-Förderbonus fällt in dieselbe Fachgruppe wie das eigenständige 180-Tage-Resource-Recovery-Programm. Es gilt die stärkste aktive Förderung statt Addition. Ablauf entfernt nur den befristeten RGW-Modifier; die bereits ausgebaute +1-Stahl-Basis bleibt erhalten. Es braucht keine tägliche Suche über alle Staaten, sondern gespeicherte Vertragsziele und Abschluss-/Ablaufereignisse.

Das hohe Intermetal-Basisbudget bleibt bei $31.2B / $62.4B / $124.8B. Die bisherigen Bereitstellungssätze $0.52B / $1.04B / $2.08B werden nun für jeden tatsächlich begünstigten Teilnehmer einschließlich des Hauptlands gerechnet. Standard mit vier Teilnehmern kostet damit $66.56B, etwa $5.17689B pro Woche über 90 Tage. Nationale Durchführung während der 90 aktiven Bonustage: 0.006% / 0.010% / 0.016% BIP pro Woche je Empfänger, zuzüglich der bisherigen Host-Betreuung von $12M / $20M / $32M pro Woche. Keine Entnahme aus einem Stahlreservelager und keine Abhängigkeit vom Reserven-Spielmodus.

Diese Werte sind ausdrücklich Spielgestaltung. Die zuvor dokumentierte reale Intermetal-Kooperation bei Metalllieferungen und technischer Zusammenarbeit bleibt die historische Grundlage; die neue Förderung ist eine vom Nutzer gewählte spielmechanische Anpassung, kein behaupteter historischer Standardvertrag.

## 9. Nachweise und Grenzen

Die Vorschau enthält jetzt 22 Registereinträge mit 44 fachlichen Angeboten: elf bisherige Projekte und elf eigenständige Programme. Die Umsetzung ist weiterhin ein Konzept mit bedienbarer Vorschau. Echte nationale Geldwerte, Bestände, Sektorbedingungen, Provinzen und Multiplayerabläufe sind nicht an einen Live-Spielstand angebunden.

Lokale Nachweise: `common/ideas/05_china.txt` für Kategorie-Forschungsboni in normalen Länderideen; `00_generic_defense_companies.txt` für weitere Kategorie-Beispiele; `05_Australia.txt` für `local_resources_factor`; `common/technologies/engineering.txt` und vorhandene Ideen für Mangelstrafen und Produktionseffizienz; vorhandene MD-Geld-, Energie- und Produktivitätsleser für die übrigen Effekte. Für Reaktorbau gilt der normale native Modifier, für den alten Turnkey-Vertrag dessen festes Ereignisdatum. Es wurden hierfür keine bestehenden Laufzeitdateien geändert.

Historische Grundlage: [UNIDO, Institutional mechanisms, 1978](https://downloads.unido.org/ot/47/91/4791252/00001-10000_07981_1978.pdf). Beschrieben werden unter anderem Fachkooperation, Ausbildung, technische Information, industrielle Spezialisierung und vertragliche Finanzierung. Die Namen, 90-/180-Tage-Takte, Modifier und Preise dieses Entwurfs sind eigene Spielgestaltung, keine behaupteten historischen sechsmonatigen RGW-Vertragskonditionen.

Eigenständiger Konzepttext und UI-Logik für IMPERIA COLD WAR. Vorhandene native Systeme und Grafiken: Paradox Interactive, MD-Team und Projektbeitragende, soweit bekannt. Bildquellen und unbekannte Einzelrechte stehen in der begleitenden Vorschau-Provenienz. Das Nutzerlogo und die Bindung aktueller Ingame-Flaggen bleiben erhalten.
