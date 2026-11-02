IMPERIA COLD WAR: Interactive COMECON Financing and Effect Catalogue
==================================================================

Aktueller Nutzerstand: [Shared Production Revision](COMECON_SHARED_PRODUCTION_REVISION.md). Der normale Projekttyp verteilt Anlagen an einen auswählbaren Host und befristete Produktionsboni an die anderen zahlenden Teilnehmer. Die früheren Kredit- und Lieferkonto-Varianten dieses Dokuments sind hierfür nicht mehr der Standardablauf; die aktuelle Revision besitzt höhere Industriepreise.

Stand: 24. Oktober 2026. Konkretisierung des Organisationskonzepts auf Wunsch des Nutzers. Vorgeschlagene Spielmechanik und Balance, keine implementierten Laufzeiteffekte. Neue UI-Namen sind Englisch. Dieses Dokument ersetzt die feste Beitragsverteilung und pauschalen Teilnehmerboni des ersten Ikarus-Beispiels. Die Preise sind nach dem Nutzerhinweis auf Geldüberschüsse erhöht; [Institutionen und gemeinsame Programme](COMECON_INSTITUTIONS_CAMPAIGNS.md) erläutert historische Arbeitsweise, Preisreferenzen und Kampagnen.

Die Ergänzung [Rücklieferungen und sowjetische Vertretung](COMECON_DELIVERIES_COUNCIL_SSR.md) konkretisiert die Alternative zur Geldtilgung: befristete, gebäudespezifische Bauunterstützung gegen begrenzte Ansprüche, mit tatsächlicher Lieferkapazität sowie Host- und Empfängerauswahl. Die SSRs können Standorte und Empfänger sein; die Sowjetunion stellt die einzige offizielle Unionsdelegation.

## 1. Die wichtigste Entscheidung

Jedes Projekt erhält einen feststehenden Umfang mit konkreten Ergebnissen, Gesamtkosten, Mindestbauzeit und Betriebsvoraussetzungen. Länder bestimmen selbst, welchen Anteil sie übernehmen und in welcher Vertragsform. Der größere Beitrag eines Landes erzeugt größere vertragliche Ansprüche, aber keine zusätzlichen Kopien des Bauwerks und keine unbegrenzten landesweiten Boni.

Nicht jedes Mitglied muss an jedem Projekt teilnehmen. Für ein ausdrücklich als Gemeinschaftsprojekt angelegtes Vorhaben sind mindestens zwei zustimmende Länder erforderlich. Ein allein finanzierter nationaler Ausbau bleibt über nationale Investitionen erreichbar. Verlangt ein Vertrag die Beteiligung aller Mitglieder, müssen alle diesem Vertrag zustimmen.

## 2. Historische Herleitung

Bei gemeinsamen Investitionen wurden Beiträge unter anderem als Geld, Maschinen, technische Unterlagen und Bauleistungen geleistet. Als Gegenleistung konnten beteiligte Länder spätere Lieferungen aus dem Projekt erhalten; diese waren an ihre Kreditanteile gekoppelt. Die UNIDO-Studie nennt die Finanzierung der Sojuz-Leitung durch die Tschechoslowakei und anschließende Gaslieferungen. [UNIDO 1984, gedruckte S. 12-13](https://downloads.unido.org/ot/47/94/4794479/10001-15000_13995.pdf)

Das stützt als Spielmodell zweckgebundene Beiträge mit vorab vereinbarter Gegenleistung. Die dort beschriebene formale Freiwilligkeit bildet nicht jeden politischen Druck innerhalb des Ostblocks ab. Wirtschaftliche Abhängigkeit und sowjetische Macht werden deshalb durch konkrete Liefer- und Finanzierungspositionen dargestellt. Die unten vorgeschlagenen Prozentschalter sind eine Bedienvereinfachung und keine Behauptung über historische RGW-Menüs oder feste Beitragstarife.

Die IIB verfügte über eingezahltes Kapital und andere Finanzierungsquellen. Ihre Kapitalquoten orientierten sich am Anteil der Länder am gegenseitigen Export; Einzahlungsmodalitäten wurden vereinbart. Bankkapital und der Beitrag zu einem einzelnen Projekt sind deshalb getrennte Größen. [UNIDO 1981, gedruckte S. 51-52](https://downloads.unido.org/ot/47/91/4791253/00001-10000_07981_1981.pdf)

## 3. Interaktion im Spiel

Der Projektinspektor enthält vier Ansichten: **Project**, **Contributions**, **Agreements** und **Effects**. Das bestehende Factions-Layout mit Karten, Länderflaggen und seitlichem Fenster bleibt die gestalterische Vorlage.

1. **Propose Project**: Typ, Standort und Ausbaustufe auswählen. Die Vorlage berechnet daraus Kosten, Mindestzeit und Ergebnisse. Ein Land kann nur einen eigenen kontrollierten Standort anbieten; andere Standortstaaten müssen selbst zustimmen.
2. **Offer Contribution**: Jedes Land wählt seinen eigenen Anteil. Schnellwahl: **None 0%**, **Limited 5%**, **Standard 10%**, **Major 20%**, **Lead 40%**. Dazu kommen kleine Plus-/Minus-Schritte. Ein führender Finanzier darf auch mehr als 40% übernehmen. Diese Namen bezeichnen Angebotshilfen, keine Pflichtquoten.
3. Neben dem Anteil stehen die Kosten pro Woche, Gesamtverpflichtung, verbleibende Laufzeit und der Betrag im Verhältnis zur eigenen Wirtschaftsleistung. Der Anteil bezieht sich immer auf dieses Projekt, nicht auf das BIP.
4. **Choose Terms**: Zuschuss, rückzahlbarer Beitrag oder Vertrag über reale Lieferleistungen auswählen, soweit die Projektvorlage diese Form unterstützt. Ein Bankkredit ist ein zusätzlicher Vertrag mit dem Kreditnehmer.
5. **Review Agreement**: Die Länder prüfen sämtliche eigenen und fremden Verpflichtungen und Ergebnisse. Erst ausdrückliche Zustimmung bindet den jeweiligen Teilnehmer. Der Initiator kann anderen Ländern keine Zahlung zuweisen.
6. **Ratify Project**: Start erst bei vollständig gedecktem Finanzierungsplan, Zustimmung aller verpflichteten Parteien und gültigen Standorten. Die Unterschrift gilt für genau diese Vertragsfassung.

Ein unvollständiger Finanzierungsplan bleibt offen. Bei 80% Deckung zeigt das Fenster 20% Finanzierungslücke. Bei 120% stehen 20% Überzeichnung zur Verhandlung. Es wird nicht heimlich auf 100% normalisiert. **Cover Remaining Share** kann die aktuelle Lücke ausdrücklich dem eigenen Angebot hinzufügen. Ein Restkredit benötigt die Zustimmung von Bank und Schuldner.

Neue Mitglieder, zusätzliche Fabriken, andere Beiträge oder geänderte Rückzahlungen ergeben eine Vertragsänderung. Betroffene Länder müssen neu zustimmen. Nach Projektstart können Beiträge durch einen bezahlten Ersatzfinanzier oder eine neue Vereinbarung verändert werden, nicht durch einseitiges Herunterstellen des Reglers.

## 4. Was ein größerer Beitrag bringt

Vier Größen bleiben sichtbar getrennt:

- **Committed Share**: unterschriebene Verpflichtung;
- **Paid Contribution**: tatsächlich bezahlter oder nachweisbar erbrachter Beitrag;
- **Outstanding Claim**: noch offener vertraglicher Rückzahlungs- oder Lieferanspruch;
- **Delivered Benefits**: bereits erhaltene Gegenleistungen.

Ein höherer rückzahlbarer Beitrag bedeutet einen höheren Anspruch. Ein höherer Zuschuss bedeutet eine größere tatsächlich geleistete Unterstützung. Ein Liefervertrag kann aus einem höheren Beitrag größere Abnahmemengen ableiten. Eine Zusage ohne Zahlung schafft weder Ansprüche noch zusätzlichen Einfluss im Diagramm.

Physische Anlagen gehören grundsätzlich dem Standortstaat, soweit der gewählte Vertrag nichts gesondert regelt. Finanzierungsanteile sind keine automatische territoriale oder staatliche Eigentumsübertragung. Ein Land mit 50% Finanzierung erhält nicht die Hälfte jedes gebauten Gebäudes.

Einflussdarstellung: tatsächliche laufende Unterstützung und ausstehende Forderungen getrennt anzeigen. Rückgezahlte historische Beiträge dürfen nicht unbegrenzt politischen Einfluss akkumulieren. Formale Ratsstimmen werden nicht gekauft. Ein Zuschuss kann Beziehungen und eine begrenzte politische Annäherung begründen, sofern der konkrete Vertrag solche Effekte enthält.

## 5. Welche Beitragsarten sinnvoll sind

Es gibt zwei Finanzierungsebenen. Alle Mitglieder tragen einen kleinen, gemeinsam vereinbarten Verwaltungsbeitrag. Als noch zu kalibrierender Vorschlag: **0.001% des eigenen BIP pro Woche**; bei 100 Milliarden BIP entspricht das 0.001 Milliarden pro Woche. Diese BIP-Formel ist eine Spielvereinfachung, kein belegter historischer RGW-Tarif. Sie finanziert klar ausgewiesene Verwaltung und schafft keine automatische Fabrikfinanzierung. Änderungen der Beitragsordnung benötigen Zustimmung nach den beschlossenen Organisationsregeln. Darüber hinaus werden die viel größeren Projektbeiträge einzeln gewählt und unterschrieben. Ein Mitglied ohne Beteiligung an einem bestimmten Werk trägt nur seinen normalen Verwaltungsbeitrag.

| Beitragsform | Echter Einsatz | Sinnvolle Gegenleistung | Einführungsstatus |
|---|---|---|---|
| Geldzuschuss | Tatsächlicher wöchentlicher Abzug und Gutschrift auf das Projektkonto | Vereinbartes öffentliches Projekt, begrenzte diplomatische Leistung | Gut für die erste Fassung |
| Rückzahlbarer Geldbeitrag | Wie Zuschuss, zusätzlich belegte Forderung gegen den Schuldner | Befristete Geldrückzahlung oder dokumentierte Warenrücklieferung | Geldrückzahlung gut abbildbar; eigener Vertrags- und Forderungsbestand nötig |
| IIB-Kredit | Auszahlung aus real finanzierten Bankmitteln, einmalige Schuldverbuchung | Tilgung und vereinbarte Zinsen | Eigene Bankanbindung, keine automatische Geldschöpfung |
| Bau-/Maschinenleistung | Verbindlich bezahltes Leistungspaket oder belegbar gebundene Kapazität | Ein fest bewerteter Teil des Projektbudgets | Als Geld-finanziertes Paket früh möglich; abstrakte gebundene Fabrikkapazität benötigt eigene Umsetzung |
| Technologietransfer | Anbieter besitzt das erforderliche Verfahren und finanziert ein begrenztes Programm | Forschungshilfe für benannte Teilnehmer | Native Forschungsboni vorhanden; Zugangs- und Beitragsregeln zusätzlich nötig |
| Energie-/Rohstofflieferung | Tatsächlicher Überschuss, verfügbares Lager oder ausführbarer Lieferweg | Vertraglicher Budgetbeitrag oder spätere Gegenlieferung | Integration in vorhandene Energie-/Rohstoffsysteme erforderlich |
| Spezialistenteam | Finanziertes Ausbildungs-/Beratungsprogramm mit tatsächlicher Fachkompetenz | Kürzere Projektvorbereitung oder begrenzter Forschungsbonus | Als klar bepreistes Programm möglich; kein neues universelles Personalinventar vortäuschen |

Ein Beitrag wird nur einmal bewertet. Ein bereits als Geld bezahltes Maschinenpaket erhöht nicht zusätzlich den Geld- und Sachbeitragsanteil. Nicht existierende zivile Maschinenbestände werden nicht durch beliebige militärische Ausrüstung ersetzt. Sachleistungen erhalten bei Vertragsabschluss feste Preise und Grenzen; politische Umbenennung erzeugt keinen Ressourcenwert.

## 6. Abrechnung und Baufortschritt

Jeder Teilnehmer erhält eine feste Gesamtverpflichtung und den vereinbarten Wochenplan. Tatsächliche Zahlungen gehen auf ein Projektkonto, aus dem genau belegte Bauabschnitte bezahlt werden. Die Summe eingezahlter Gelder, verfügbarer Restmittel und bezahlter Bauabschnitte muss nachvollziehbar bleiben.

Mehrere Länder können dasselbe Projekt finanzieren. Das Projekt wird einmal gebaut. Seine Mindestdauer lässt sich durch eine höhere Vorauszahlung nicht unterschreiten. Eine schnellere Bauvariante muss als teurere, vorab definierte Vorlage angeboten werden und weiterhin technische Voraussetzungen erfüllen.

Bei Zahlungsproblemen zeigt das Fenster einen Verzug. Vereinbarte Reserven können einen Bauabschnitt weitertragen. Danach sind Pause, ausdrücklich genehmigte Ersatzfinanzierung oder ein kleinerer neu vereinbarter Umfang möglich. Kein anderes Land wird automatisch belastet. Neue Beiträge nach einem Ausfall ändern künftige Ansprüche erst mit neuem Vertrag; bereits bezahlte Forderungen bleiben nachvollziehbar.

Nicht verbrauchte Einzahlungen können bei Abbruch entsprechend ihrem noch vorhandenen Anteil erstattet werden. Bereits verbrauchte Beiträge sind versunkene Kosten oder bleiben nach den Vertragsbedingungen Forderungen. Eine volle Erstattung trotz fertiger Gebäude ist ausgeschlossen.

## 7. Vorgegebene Effekte statt beliebiger Bonuswahl

Die Spieler wählen Projektart, Größe, Ort, Partner und Finanzierung. Die Ergebnisvorlagen sind vorher festgelegt und vollständig einsehbar. Aus einem Stromnetz lässt sich durch Finanzierungsauswahl kein beliebiger Forschungs-, Steuer- oder Armeebonus erzeugen.

| Effektfamilie | Im untersuchten Mod nachgewiesener Baustein | Vorgesehene Anwendung |
|---|---|---|
| Staatsgeld | `modify_treasury_effect`, `treasury_change` | Einzahlung, Auszahlung, Geldrückzahlung, Betriebs- oder Wartungskosten |
| Staatsschuld | `modify_debt_effect`, `debt_change` | Einmalige Aufnahme und Tilgung; Gläubigeranspruch separat führen und nicht doppelt belasten |
| Gebäude | Registrierte Zivilfabriken, Agrarbezirke, Büros, Mikrochip-/Verbundstoffwerke, Kraftwerke und weitere Anlagen | Konkreter bezahlter Ausbau in benannten Staaten; Stufe und Standort begrenzen |
| Bauplätze | Native State-Effekte bereits in Kuba-Verträgen verwendet | Vor jeder gewährten Gebäudestufe ein zusätzlicher gemeinsamer Bauplatz im selben Staat |
| Verkehr und Infrastruktur | Registrierte Infrastruktur, Eisenbahn, Versorgungsknoten und Häfen | Standortbezogene Investitionen; Staaten-, Provinz- und native Obergrenzen beachten |
| Begrenzte Forschung | `add_tech_bonus`; tatsächlich verwendete Kategorien `CAT_industry`, `CAT_electronics`, `CAT_infrastructure`, `CAT_agriculture` | Vorab festgelegter Prozentsatz und Zahl der Anwendungen für berechtigte Teilnehmer |
| Zivile Produktivität | `civilian_factories_productivity` wird in Steuer- und BIP-Berechnung gelesen | Gezieltes, begrenztes Kooperationsprogramm; kein pauschaler Baugeschwindigkeitsbonus |
| Landwirtschaftlicher Ertrag | `agriculture_district_income_tax_modifier` wird in der Agrar-Einnahmenberechnung gelesen | Bezahltes Verfahren-/Düngerprogramm mit exakt ausgewiesener Wirkung |
| Exporterlöse | Allgemeine und rohstoffbezogene Exportmodifikatoren mit Lesern in `00_money_system.txt` | Nur sachlich passende Erlösänderung; ersetzt keinen echten Warentransfer |
| Energieversorgung | Vorhandenes Energy Load Sharing mit Überschuss- und Defizitprüfung | Echter Ausgleich zwischen verbundenen Partnern; mehrere Lieferquellen und feste Lieferanteile benötigen Erweiterung |
| Brennstoff und Rohstoffe | Bestehende Ressourcen-, Förder- und Lagermodelle | Bezahlte Förderung oder echte Lieferungen; Absenderverlust und Empfängergewinn zusammen prüfen |
| Nationale Programme | Ideen und dynamische Modifikatoren mit bestehenden MD-Verbrauchern | Wartung, Abnahmebindung, Ausbildung und Spezialisierung; abhängig vom jeweiligen Vertrag |

Quellennachweise: `common/scripted_effects/00_budget_effects.txt`, `00_money_system.txt`, `!_energy_effects.txt`, `COLDWAR_CUB_1970_foreign_contracts.txt`; `common/buildings/00_buildings.txt`, `common/resources/00_resources.txt`, `common/modifier_definitions/money_modifier_definitions.txt` und `common/technology_tags/00_technology.txt`.

Wichtige Grenzen: `interest_rate_multiplier_modifier` wird zum Zinswert addiert und anschließend begrenzt; es ist kein frei interpretierbarer prozentualer Rabatt. `civilian_factories_productivity` verändert im untersuchten Code unter anderem die zivile Steuerbasis und das BIP. Eine virtuelle Pipeline, ein zusätzliches Wareninventar oder mehrere garantierte Stromlieferanteile entstehen nicht allein durch einen passenden Modifikatornamen. Solche Funktionen bleiben eigene Erweiterungen.

## 8. Erste bezifferte Projektvorlagen

Alle folgenden Geldwerte sind vorgeschlagene MD-Milliarden, keine historischen Preise. Der Betrag pro Woche gilt für das ganze Projekt und wird auf die zustimmenden Teilnehmer verteilt. Beiträge und Resultate sind vor Umsetzung an den 1970-Volkswirtschaften zu kalibrieren. Jeder Standortbau setzt die echte Kapazität, Kontrolle und passende Technik voraus.

| Vorlage | Umfang | Wochen | Gesamt | Pro Woche | Einmaliges physisches Ergebnis |
|---|---|---:|---:|---:|---|
| **Industrial Expansion: Limited** | Klein | 104 | 18.720 | 0.180 | +1 civilian factory, +1 shared building slot |
| **Industrial Expansion: Standard** | Mittel | 156 | 37.440 | 0.240 | +2 civilian factories, +2 shared building slots |
| **Industrial Expansion: Major** | Groß | 208 | 74.880 | 0.360 | +4 civilian factories, +4 shared building slots |
| **Agricultural Development: Limited** | Klein | 104 | 9.048 | 0.087 | +1 agriculture district, +1 shared building slot |
| **Agricultural Development: Standard** | Mittel | 156 | 18.096 | 0.116 | +2 agriculture districts, +2 shared building slots |
| **Agricultural Development: Major** | Groß | 208 | 36.192 | 0.174 | +4 agriculture districts, +4 shared building slots |
| **Transport Corridor: Limited** | Klein | 104 | 8.580 | 0.0825 | +1 infrastructure level, +1 shared building slot |
| **Transport Corridor: Standard** | Mittel | 156 | 17.160 | 0.110 | Insgesamt +2 infrastructure levels, +2 slots in den jeweiligen Staaten |
| **Transport Corridor: Major** | Groß | 208 | 34.320 | 0.165 | Insgesamt +4 infrastructure levels, +4 slots in den jeweiligen Staaten |

Weitere feste Vorlagen sind möglich: konventionelle Kraftwerke, zivile Reaktoren, Mikrochipwerke, Lager und Ausbildung. Diese werden erst beziffert, nachdem Baukosten, Brennstoff-/Arbeitskräftebedarf, Technik und spätere Betriebskosten zusammen erfasst sind. Nukleare Waffen sind kein automatisches Ergebnis ziviler Reaktorkooperation. Uranprojekte verlangen eine bezahlte Erschließung eines nachgewiesenen Vorkommens und beginnen ohne kostenlose Förderung oder Mine.

Ein eigenständiges **Joint Industrial Research** kann als Vorschlag einen Teilnehmerkreis von zwei bis sechs Ländern und im Standard ein Programm von 104 Wochen vorsehen: Koordination 0.020 Milliarden pro Woche plus 0.020 Milliarden pro Woche für jedes begünstigte Land. Ergebnis je begünstigtem Land: **1 x 25% industry research bonus**. Bei vier Begünstigten sind das 0.100 Milliarden pro Woche und 10.400 Milliarden insgesamt. Der Kreis wird vor Unterschrift fixiert; ein weiteres Land erhöht Kosten und verlangt eine neue Vertragsfassung. Größere Geldanteile duplizieren den Forschungsbonus nicht. Ein finanzschwaches Land kann ein ausdrücklich mitfinanziertes Stipendium erhalten.

Militärfabriken, Werften und andere native Bauwerke sind technisch mögliche Bausteine. Ihre Nutzung verlangt einen passenden gesonderten Industrie-/Rüstungsvertrag und ist kein Standardergebnis aller RGW-Projekte. Allgemeine Steuer-, Stabilitäts- und Armeeboni werden nicht als frei zusammenstellbarer Belohnungsladen angeboten.

## 9. Beispiel mit frei wählbarer gemeinsamer Finanzierung

**Joint Industrial Plant: Standard** in Ungarn. Budget 37.440 Milliarden, 156 bezahlte Bauwochen. Installation, Schulung und Abwicklung sind im genehmigten Budget enthalten, keine zusätzliche doppelte Einrichtungsgebühr. Ergebnis in Ungarn: **+2 shared building slots**, danach **+2 civilian factories**. Die Forschungsvorlage ist ein gesondertes Programm und wird nicht kostenlos angehängt.

| Land | Gewählter Anteil | Bauzahlung pro Woche | Beitrag insgesamt | Anspruch bei rückzahlbarer Beteiligung |
|---|---:|---:|---:|---:|
| Sowjetunion | 50% | 0.120 | 18.720 | 18.720 |
| Ungarn | 20% | 0.048 | 7.488 | Eigenanteil, keine Forderung gegen sich selbst |
| DDR | 15% | 0.036 | 5.616 | 5.616 |
| Tschechoslowakei | 15% | 0.036 | 5.616 | 5.616 |
| Summe | 100% | 0.240 | 37.440 | 29.952 externe Forderungen |

Vor Vertragsstart könnte die Sowjetunion ihren Anteil auf 30% reduzieren und Polen 20% anbieten. Das unveränderte Projekt bleibt damit vollständig finanziert. Ohne Ersatzangebot fehlen 20%; der Start wird nicht freigegeben. Ein kleineres Projekt kann als neue Vorlage neu verhandelt werden.

Die bezahlte externe Finanzierung wird als vorgeschlagene günstige Kreditform nach Fertigstellung in 780 Wochen getilgt. Hinzu kommt wöchentlich ein Zins von 1/2600 der jeweiligen verbleibenden Hauptforderung, gerundet 0.03846% pro Woche. Die Kapitaltilgung beträgt für die Sowjetunion **+0.024 Milliarden pro Woche**, für DDR und Tschechoslowakei jeweils **+0.0072**. Die erste Gesamtzahlung einschließlich Zinsen beträgt **+0.0312**, **+0.00936** und **+0.00936**; Ungarn zahlt entsprechend zuerst **-0.04992 Milliarden pro Woche**. Der Zinsanteil sinkt mit der verbleibenden Hauptforderung. Dies sind Balancevorschläge, keine historischen Standardbedingungen. Die Bauzahlungen enden vor Beginn der Rückzahlungsphase. Reale laufende Gebäudekosten fallen zusätzlich im bestehenden MD-System an und müssen in der Vertragsvorschau berücksichtigt werden.

Alternativ kann ein Finanzier seinen Anteil als Zuschuss anbieten. Dann fällt genau dessen spätere Forderung weg. Ein Zuschuss der Sowjetunion über 50% senkt die externe Hauptforderung in diesem Beispiel von 29.952 auf 11.232 Milliarden und die erste ungarische Rückzahlungsrate einschließlich Zinsen auf **0.01872 Milliarden pro Woche**. Der Zuschuss erzeugt keine zweite Fabrik.

Ein späteres Warenmodell ersetzt die entsprechende Geldrate durch genau bewertete echte Lieferungen. Warenlieferung und volle parallele Geldtilgung dürfen nicht dieselbe Forderung doppelt bedienen. Nach Tilgung endet der Anspruch. Ein anschließendes Lieferabkommen ist ein neuer Vertrag. Ungarn behält die Anlage; es kann bei ausbleibender Tilgung in Verzug geraten, verliert aber nicht automatisch Land oder die ganze Fabrik.

Die illustrative 780-Wochen-Tilgung verteilt das höhere Investitionsbudget auf einen längeren Zeitraum. Die frühe Umsetzung muss bei Rundungsresten die letzte Rate an den verbliebenen Anspruch anpassen. Die Vorschau zeigt Hauptforderung, Zinsregel, erste Wochenrate, sinkende Folgeraten und Endrate in den nativen Formaten. Dieselbe Hauptforderung darf nicht zusätzlich voll im nativen Marktzinssystem belastet werden.

## 10. Was das System im Multiplayer interessant macht

Ein kleines Land kann mit einem kleinen bezahlbaren Anteil teilnehmen, als Standortstaat einen Ausbau einwerben oder für ein begrenztes Forschungsprogramm mitfinanziert werden. Ein großes Land kann eine Lücke schließen, dafür höhere spätere Lieferansprüche erhalten oder bewusst einen Zuschuss als außenpolitische Unterstützung anbieten.

Ein Staat kann Lieferant sein, ohne Standort des Hauptwerks zu werden. Ein Transitland muss die Nutzung seines Territoriums genehmigen und kann eine klar bezifferte Transitvereinbarung verlangen. Ein hoch entwickeltes Land kann Technik beisteuern; diese Leistung muss bepreist und die Technologie tatsächlich vorhanden sein. Damit gibt es verschiedene Rollen statt einer einzigen Spendenhöhe.

Ein Land darf mehrere Projekte finanzieren. Die Übersicht zeigt sämtliche wöchentlichen Verpflichtungen zusammen und die zugesagten späteren Gegenleistungen. Ein Finanzier kann vor der Zustimmung erkennen, ob er seine eigenen Vorhaben verdrängt. Der Rat darf niemanden durch eine Mehrheitsentscheidung ohne dessen Vertragszustimmung zu neuen Projektzahlungen verpflichten.

## 11. Prüfung und Status

Bestätigt sind die genannten lokalen Bausteine und die historischen Finanzierungsformen. Nicht bestätigt sind ein vollständig funktionierendes RGW-System, dessen Multiplayer-Verhalten oder die endgültige Balance der vorgeschlagenen Zahlen. Die zugehörige interaktive Darstellung ist ein Rechenbeispiel mit frei veränderlichen Anteilen, kein Screenshot aus HOI4.

Vor Umsetzung zu prüfen: genaue Folgekosten der Gebäude, Bau- und Standortobergrenzen, Technologieabdeckung der Forschungsboni, Vertrags-/MD-Schuldendarstellung ohne Doppelzählung, Rundung, Zahlungsunfähigkeit, bereits verbrauchte Mittel, Teilabbruch, Speichern/Laden und gleichzeitig abgegebene Angebote. Die Vorschau selbst führt keine wirtschaftlichen Effekte aus. Alle laufenden Geldbeträge verwenden Wochen und höchstens fünf Nachkommastellen in Scriptliteralen.

## 12. Provenienz

Eigenständiger Konzepttext und eigene Balancevorschläge für IMPERIA COLD WAR. Native und lokale Codepfade werden als überprüfbare technische Quellen genannt; es wurden daraus keine neuen Laufzeitdateien erzeugt. Native APIs stammen von Paradox Interactive, Modsysteme vom MD-Team und jeweiligen Projektbeitragenden. Einzelautorenschaft einzelner lokaler Änderungen und deren genaue Lizenz bleiben unbekannt.

Historische Quellen: UNIDO 1981, institutionelle Beschreibung der Finanzierung; UNIDO/IS.486, 27. September 1984, *The Development of Chemical and Petrochemical Industries in the European CMEA Countries*, verfasst von V. G. Gerts als UNIDO-Berater und Mitarbeiter des sowjetischen Außenhandelsministeriums. Dessen institutionelle Perspektive ist bei Aussagen über Freiwilligkeit zu berücksichtigen. Die UNIDO-Veröffentlichung nennt die Möglichkeit wissenschaftlicher und pädagogischer Zitate mit Quellenangabe. Hier werden kurze historische Befunde paraphrasiert; keine Abbildungen übernommen. Weitere Rechte sind damit nicht beansprucht.
