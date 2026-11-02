IMPERIA COLD WAR: COMECON Institutions, Higher Costs and Joint Programmes
=======================================================================

Aktueller Preis- und Ergebnisstand des normalen Gemeinschaftsprojekts: [Shared Production Revision](COMECON_SHARED_PRODUCTION_REVISION.md). Dessen aktualisierte Industriepreise und automatische Teilnehmerboni ersetzen für diesen Projekttyp die älteren Werte unten. Historische Institutionsrecherche und die getrennten Fachprogramme bleiben als ergänzender Entwurf erhalten.

Stand: 24. Oktober 2026. Konzeptrevision auf ausdrücklichen Wunsch nach höheren Projektkosten und möglichst realistischer Organisation. Keine Laufzeitimplementierung. Die neuen Preis- und Finanzierungsregeln ersetzen die früheren günstigen Beispiele; die Organisations- und Kampagnenarchitektur ergänzt sie. Geldwerte sind MD-Spielwerte, keine rekonstruierten historischen Dollarpreise.

## 1. Wie die Organisation arbeitete

Die Ratstagung bildete das oberste Organ. Der Exekutivausschuss koordinierte die Ausführung, Fachkommissionen bearbeiteten einzelne Wirtschaftsbereiche, das Moskauer Sekretariat bereitete Unterlagen vor. Reguläre Ratstagungen fanden typischerweise jährlich statt, Exekutivausschusssitzungen vierteljährlich. [UNIDO 1978, gedruckte S. 6-8](https://downloads.unido.org/ot/47/91/4791252/00001-10000_07981_1978.pdf)

Das ist der institutionelle Ausgangspunkt für Rat, laufende Projektverwaltung und sektorale Programme im Spiel. Empfehlungen mussten in staatliche Planung und konkrete Verträge umgesetzt werden. Ein Mehrheitsklick im Organisationsfenster ersetzt nicht die Zustimmung eines betroffenen Standortstaats oder Finanzierers. Die formale Gleichberechtigung beseitigte das tatsächliche Machtgefälle gegenüber der Sowjetunion nicht.

Handelsbeziehungen wurden überwiegend staatlich vereinbart: Fünfjahresabkommen erhielten jährliche Protokolle über Mengen und Preise. [IWF 1991: The CMEA System](https://www.elibrary.imf.org/view/journals/024/1991/001/article-A001-en.xml). Ein automatischer gemeinsamer Markt mit freier Verfügbarkeit aller Güter wäre deshalb ein falscher Ausgangspunkt. Vertragspreise, Liefertermine und zwischenstaatliche Aushandlung bleiben zentral.

Institutionen entwickelten sich weiter. Die Ausschüsse für Planungszusammenarbeit sowie Wissenschaft und Technik entstanden 1971; das Standardisierungsinstitut bestand seit 1962. [UNIDO 1978, gedruckte S. 8 und 11](https://downloads.unido.org/ot/47/91/4791252/00001-10000_07981_1978.pdf). Die Konvention zur Anwendung von RGW-Standards wurde 1974 geschlossen und trat 1975 in Kraft. [UN-Vertragsregister, Nr. 13921](https://treaties.un.org/Pages/showDetails.aspx?clang=_en&objid=0800000280109211)

Im Januar-1970-Start werden spätere Institutionen daher nicht als bereits historisch vorhanden dargestellt. Eine Gründungsvereinbarung kann ihre Arbeitsweise im RP früher einführen; das wäre ausdrücklich eine alternative Entwicklung. Bestehende Facharbeit und Projekte müssen vorher trotzdem spielbar sein.

## 2. Was wir daraus für das Spiel übernehmen

| Historische Funktion | Interaktion im Spiel |
|---|---|
| Ratstagung | Mehrjährige Prioritäten und Organisationsregeln beschließen, Mitgliedschaften verhandeln |
| Exekutivausschuss | Projektberichte, Vertragsänderungen und Finanzierungsprobleme bearbeiten |
| Fachkommissionen | Produktions-, Energie-, Agrar-, Verkehrs-, Forschungs- und Ausbildungsprogramme vorschlagen |
| Sekretariat | Vergleichbare Statistiken, Angebote, bezahlte Beiträge und Lieferstände anzeigen |
| Nationale Planung | Jeder Teilnehmer übernimmt die eigenen vereinbarten Verpflichtungen und Maßnahmen |
| Jahresprotokolle | Liefermengen, nächste Finanzierungsabschnitte und Preise prüfen und gegebenenfalls neu vereinbaren |
| IBEC und IIB | Verrechnung und Investitionsfinanzierung mit getrennten Konten und Verträgen |

Das Organisationsfenster bleibt jederzeit bedienbar. Die jährliche oder vierteljährliche historische Arbeitsweise wird über Berichte und Vertragsabschnitte dargestellt; sie darf das Multiplayer-RP nicht bis zu einem einzelnen Sitzungstag blockieren. Bereits unterschriebene Zahlungen laufen ohne wiederholte Bestätigung jeder Rate.

Fünfjährige Pläne legen Schwerpunkte fest, aber garantieren keine fertigen Fabriken. Eine gemeinsame Programmbeschreibung verpflichtet noch keine nationale Wirtschaft. Projektverträge, Lieferprotokolle und nationale Durchführung werden im Fenster getrennt sichtbar.

## 3. Kostenkorrektur anhand vorhandener MD-Preise

Der lokale Investitionskatalog enthält folgende unveränderte Ausgangswerte: Zivilfabrik 12, Agrarbezirk 5.8, Infrastrukturstufe 5.5, konventionelles Kraftwerk 5.2, ziviler Reaktor 14.4 Milliarden. `project_monetary_cost_calculation` liest den Gebäudepreis, wendet Länder-/Investitionsmodifikatoren an und multipliziert mit der Zahl der Stufen. Nachweis: `common/scripted_effects/99_investment_scripted_effects.txt`, insbesondere `init_investment_system` und `project_monetary_cost_calculation`.

Das frühere Beispiel von 1.040 Milliarden für zwei Zivilfabriken lag schon weit unter dem vorhandenen Grundpreis von 24 Milliarden. Das war keine brauchbare Kalibrierung. Es wird vollständig ersetzt.

Neuer Vorschlag für ein gemeinsames Baupaket: Gebäudewert aus der MD-Referenz multipliziert mit **1.56**. Der zusätzliche Budgetanteil steht im Entwurf für Erschließung, Installation, Schulung und Projektabwicklung. Der Faktor ist ein Balancevorschlag angesichts des vom Nutzer gemeldeten Geldüberschusses und kein historisch gemessener RGW-Aufschlag. Ein einfaches Projekt kostet dadurch etwa anderthalbmal so viel wie sein unveränderter nativer Gebäudewert.

Die erste Angebotssumme wird beim Vertragsabschluss eingefroren. Ein Wechsel der Wirtschaftspolitik darf keine laufende Rechnung rückwirkend verbilligen. Bei späterer Umsetzung werden passende reale Standort- und Investitionsbedingungen in das Angebot einbezogen und in dessen Endsumme offengelegt. Rabatte benötigen einen benannten und finanzierten Zuschuss, wenn sie die echte Projektleistung unverändert lassen.

| Projektgröße | Umfang | Bauwochen | Gesamtbudget | Gesamtrate pro Woche |
|---|---|---:|---:|---:|
| Industrial Expansion: Limited | 1 Zivilfabrik und 1 Bauplatz | 104 | 18.720 | 0.180 |
| Industrial Expansion: Standard | 2 Zivilfabriken und 2 Bauplätze | 156 | 37.440 | 0.240 |
| Industrial Expansion: Major | 4 Zivilfabriken und 4 Bauplätze | 208 | 74.880 | 0.360 |
| Agricultural Development: Limited | 1 Agrarbezirk und 1 Bauplatz | 104 | 9.048 | 0.087 |
| Agricultural Development: Standard | 2 Agrarbezirke und 2 Bauplätze | 156 | 18.096 | 0.116 |
| Agricultural Development: Major | 4 Agrarbezirke und 4 Bauplätze | 208 | 36.192 | 0.174 |
| Transport Corridor: Limited | Insgesamt 1 Infrastrukturstufe und 1 Bauplatz | 104 | 8.580 | 0.0825 |
| Transport Corridor: Standard | Insgesamt 2 Infrastrukturstufen und 2 Bauplätze | 156 | 17.160 | 0.110 |
| Transport Corridor: Major | Insgesamt 4 Infrastrukturstufen und 4 Bauplätze | 208 | 34.320 | 0.165 |

Die Bauplätze liegen jeweils im selben Staat wie die dazugehörigen Stufen und werden vor den Stufen gewährt. Mindestdauer, Finanzierung und Bau-/Technikvoraussetzungen müssen gleichzeitig erfüllt sein. Eine höhere Einzahlung verkürzt die Mindestzeit nicht beliebig. Bei Großanlagen bleiben Brennstoff, Arbeitskräfte, Netzanschlüsse und Betriebsbudget zusätzliche reale Bedingungen.

Alle bisherigen Forschungsprojekte werden ebenfalls neu bepreist. Beispiel für Joint Industrial Research: Pilotprogramm 52 Wochen mit 0.010 Milliarden Koordination plus 0.010 je Begünstigtem pro Woche; Standardprogramm 104 Wochen mit 0.020 plus 0.020 je Begünstigtem; Intensivprogramm 156 Wochen mit 0.040 plus 0.040 je Begünstigtem. Ergebnisse je Begünstigtem: Pilot 1 x 15%, Standard 1 x 25%, Intensiv 2 x 25% Industrieforschungsbonus. Bei vier Begünstigten kostet das Standardprogramm insgesamt 10.400 Milliarden. Das ist ein eigenständiges Forschungsprogramm; ein bloßer Beitrag zu einem Fabrikbau schaltet es nicht kostenlos frei.

Diese Preise sind statisch an aktuellen Mod-Bausteinen orientiert. Aktuelle Kassenbestände und freie Wochenüberschüsse eines laufenden Multiplayer-Spielstands wurden nicht gemessen. Nach einem Spieltest sind Leistbarkeit, Konkurrenz zu normalen Investitionen und Wirkung auf das verfügbare Geld zu prüfen. Historisch plausible Institutionen und eine brauchbare Spielbalance sind getrennte Nachweise.

## 4. Langfristige Finanzierung statt unrealistischer Kurztilgung

Der vorherige Nullzinskredit mit 104 Rückzahlungswochen wird für das neue Großprojekt ersetzt. Vorschlag: **780 Wochen Laufzeit**, gleichmäßige Kapitaltilgung und **1/2600 der verbleibenden Hauptforderung pro Woche** als Zins. Im Tooltip entspricht das gerundet **0.03846% pro Woche**. Das ist eine vorgeschlagene günstige Kreditbedingung, keine allgemeine historische RGW-Kondition. Die IIB gewährte je nach Kreditform unterschiedliche Laufzeiten und Zinsen; der frühere UNIDO-Nachweis beschreibt langfristige Kredite bis zu 15 Jahren.

Die erste Zahlung ist größer als die spätere, weil der Zinsanteil mit der Restschuld sinkt. Ein zugesagter Zuschuss bleibt ein Zuschuss und erzeugt weder Tilgung noch Zinsen. Rücklieferungen können vereinbarte Ansprüche bedienen, wenn tatsächliche Waren-/Energieleistungen zu festen Vertragswerten verbucht werden. Die letzte Rate wird auf die echte verbleibende Forderung begrenzt.

Im technischen Entwurf sind Marktverschuldung und Projektverbindlichkeiten abzustimmen. Derselbe Vertrag darf nicht zusätzlich die volle native Marktverzinsung und seine eigene volle Verzinsung auslösen. Ein reiner Nebenzähler ohne Einbindung in Gesamtschuld, Risiko und Budget ist keine abgeschlossene Kreditimplementierung.

## 5. Gemeinsame Kampagnen sind bezahlte Programme

Eine Kampagne wird als fachlich betreutes mehrjähriges Programm angeboten. Sie benennt Ziele, nationale Durchführung, gemeinsame Leistungen und Kosten. Produktivität, Qualität und Anwendung von Wissenschaft und Technik waren tatsächlich Themen der RGW-Zusammenarbeit; die gemeinsame wissenschaftliche und technische Arbeit wurde institutionell koordiniert. [RGW-Bericht vor dem UN-Wirtschafts- und Sozialrat 1976](https://digitallibrary.un.org/record/824105/files/E_SR.2011-EN.pdf)

Eine griffige Spielbezeichnung ist erlaubt. Historisch übertriebene Behauptungen, wonach Moskau jede nationale Produktivitätskampagne zentral ausgeführt hätte, werden vermieden. Der RGW organisiert ein Angebot; die beteiligten Regierungen müssen die Maßnahmen finanzieren und umsetzen.

Für geeignete mehrjährige nationale Programme gilt als erster Kostenentwurf:

| Intensität | Nationaler Wochenbetrag | Gemeinsame Koordination pro Woche und Programm |
|---|---:|---:|
| Pilot | 0.010% des BIP des teilnehmenden Landes | 0.010 Milliarden, auf die Unterzeichner verteilt |
| Standard | 0.020% des BIP des teilnehmenden Landes | 0.020 Milliarden, auf die Unterzeichner verteilt |
| Intensive | 0.040% des BIP des teilnehmenden Landes | 0.040 Milliarden, auf die Unterzeichner verteilt |

Die nationale Durchführung richtet sich nach dem eigenen BIP. Ein großer Finanzierungsanteil an der gemeinsamen Koordination vervielfacht nicht die Wirkungen im eigenen Land. Ein Partner kann ausdrücklich nationale Durchführungskosten eines kleineren Landes mittragen. Die Anzeige trennt eigenes Budget, erhaltenen Zuschuss und eigene Restzahlung.

Die BIP-Bemessungsgrundlage wird für einen vereinbarten 13-Wochen-Abschnitt festgelegt. Änderungen der nationalen Bemessungsgrundlage folgen der unterschriebenen Indexierungsregel; größere Kosten- oder Leistungsänderungen benötigen neue Zustimmung. Der vollständige geplante Wochenbetrag ist vor der Unterschrift sichtbar. Kein Fensteraufruf berechnet eine zusätzliche Zahlung.

Ein Standardprogramm über 156 Wochen bindet bei unveränderter Bemessungsgrundlage insgesamt 3.12% des BIP an nationaler Durchführung zuzüglich des eigenen Koordinationsanteils. Die laufenden Wochenraten sind die Spieleranzeige. Das höhere Gesamtbudget soll eine echte Alternative zu Fabrik-, Energie- und Infrastrukturinvestitionen sein.

## 6. Produktivitätsprogramm als genauer Ablauf

Vorschlag für **Industrial Labour Productivity Programme**, Standard, 156 bezahlte Wochen:

1. Wochen 1-26: Betriebsaufnahme, Bestandsaufnahme, Lehrpläne und Schulung der Ausbilder. Noch kein Produktivitätsbonus.
2. Ab bezahlter Woche 27: **+5% Country Productivity Growth**.
3. Ab bezahlter Woche 53: **+10% Country Productivity Growth** insgesamt.
4. Ab bezahlter Woche 79: **+15% Country Productivity Growth** insgesamt.
5. Ab bezahlter Woche 105: **+20% Country Productivity Growth** insgesamt bis zum Ende des Programms.

Es werden jeweils die Stufen ersetzt; sie werden nicht zu +50% aufaddiert. Der Pilot endet nach 104 bezahlten Wochen und erreicht höchstens +10%, die Intensivfassung nach 208 und höchstens +30%. Zeitplan und höhere Dauer stehen vor der Annahme fest. Der Intensivplan ergänzt nach der Standardstufe je eine weitere Stufe bei bezahlter Woche 131 und 157.

Die native Umsetzung benutzt den Wachstumsmodifikator, nicht einen direkten Sprung von +20% Gesamtproduktivität. Der Unterschied ist wesentlich: In `00_productivity_effects.txt` multipliziert `country_productivity_growth_modifier` den bereits vorhandenen Wachstumsansatz; staatlicher Aufholeffekt und weitere Bedingungen bleiben erhalten. Die angezeigten +20% sind weder 20 Prozentpunkte jährliches Wachstum noch eine Garantie einer um 20% größeren Wirtschaft. Bei bestehenden Wachstumsmodifikatoren ist die tatsächliche zusätzliche Änderung geringer oder größer als ein isoliert berechneter Anteil.

Ein Programm ohne Finanzierung erhält nach einer vereinbarten Übergangsfrist keine laufende zusätzliche Organisationsleistung. Bereits tatsächlich entstandene Produktivitätszuwächse bleiben im bestehenden MD-System erhalten; das Programm erhält nach Ende keinen zusätzlichen pauschalen permanenten Bonus. Ein abgeschlossener Durchlauf kann später eine neue bezahlte Aufbauphase rechtfertigen, aber nicht dieselbe Forschung oder dieselben Anlagen ein zweites Mal vergeben.

## 7. Kampagnenkatalog

Die Bezeichnungen und Zahlen sind vorgeschlagene, vorab feste Standardpakete. Intensitätsvarianten werden eigenständig bepreist und begrenzt. Die folgenden Programme dauern im Standard zunächst 156 bezahlte Wochen, außer dem ausdrücklich separaten Forschungsprogramm. Die meisten Effekte beginnen erst nach 26 oder 52 bezahlten Wochen. Gebäude und bezifferte Lieferungen werden als eigene Projektleistung finanziert.

| Programm | Konkretes Ziel | Vorgeschlagene Standardwirkung | Reale Grenze oder Verpflichtung |
|---|---|---|---|
| **Industrial Labour Productivity Programme** | Arbeitsorganisation und Verfahren schrittweise verbessern | Gestuft bis +20% Country Productivity Growth | Nationale Durchführung und Betreuung dauerhaft bezahlen; kein sofortiger Produktivitätssprung |
| **Technical Instructor Exchange** | Ausbilder und Fachwissen zwischen Teilnehmern vermitteln | +10% State Productivity Growth in höchstens drei vorher benannten kontrollierten Staaten des Empfängers | Finanzierte Expertenleistung, echte beteiligte Fachinstitution; Förderstaaten und Kompetenzen müssen vereinbart sein |
| **Industrial Standardisation Programme** | Maße, Komponenten und Arbeitsverfahren angleichen | Nach Einführung +2% Civilian Factory Productivity | Umrüstung und Schulung; vorhandene nationale Produktionsverfahren werden nicht kostenlos ersetzt |
| **Industrial Quality Control Programme** | Ausschuss und Prozessfehler reduzieren | Nach Einführung +3% Civilian Factory Productivity | Prüf- und Wartungsorganisation finanzieren; kein automatischer Absatz auf westlichen Märkten |
| **Power Station Efficiency Programme** | Betrieb und Wartung vorhandener thermischer Anlagen verbessern | -5% Fossil Power Plant Fuel Consumption | Nur nützlich mit tatsächlich betriebenen passenden Kraftwerken; keine zusätzliche kostenlose Stromerzeugung |
| **Fuel Economy Programme** | Verbrauch außerhalb der Stromerzeugung senken | -3% Non-Electric Fuel Consumption | Nationale Umrüstung und Verbrauchsorganisation; reale Brennstoffversorgung bleibt nötig |
| **Agricultural Mechanisation Programme** | Maschinen, Anwendung und Fachkenntnisse verbessern | +5% Agriculture District Income, nach Finanzierung 1 x 25% Agriculture Research Bonus | Maschinenfinanzierung und agrarische Forschungsbasis; keine automatische neue Ackerfläche |
| **Agricultural Extension Programme** | Beratung und bessere Nutzung vorhandener Verfahren | +3% Agriculture District Income | Bezahlt Beratung und Anwendung; ersetzt keine Wetter-, Wasser- oder Erntephysik |
| **Transport Coordination Programme** | Bau und Betrieb kompatibler Verbindungen vorbereiten | +10% Infrastructure Construction Speed; einmalig 1 x 25% Infrastructure Research Bonus | Tatsächliche Verkehrswege entstehen nur über bezahlte Bauprojekte; Bauzeitvorteil ist keine Gütermenge |
| **Joint Industrial Research** | Einen abgegrenzten Themenplan gemeinsam bearbeiten | Standard: 1 x 25% Industry Research Bonus je vereinbartem Begünstigtem | Eigene 104-Wochen-Vorlage und eigene Kosten; keine unbegrenzte Wiederholung desselben Abschlussbonus |
| **Electronics Research Cooperation** | Elektronische Verfahren und Bauteile entwickeln | Bei bezahltem Abschluss 1 x 25% Electronics Research Bonus | Themenplan und real vorhandene Forschungstechnik; ein Mikrochipwerk ist ein zusätzliches Bauprojekt |
| **Joint Project Preparation Programme** | Standorte, Bauunterlagen und technische Prüfung koordinieren | Für nachfolgende qualifizierte RGW-Projekte 13 statt 26 Wochen Vorbereitung | Eigene RGW-Projektlogik erforderlich; kein erfundener nativer Spezialmodifikator |

Die Wirkungen sind MD-Abstraktionen. Zivile Produktivitätsmodifikatoren werden im geprüften Mod unter anderem in Steuer- und BIP-Berechnungen gelesen; sie sind kein direkter Bonus für zivile Waren, die das Spiel gar nicht als Bestand führt. Forschungskategorien müssen jeweils tatsächliche passende Technologien enthalten. Die genannten Energieverbrauchsmodifikatoren besitzen echte Leser in `!_energy_effects.txt`. Staatsbezogene Wachstumsförderung greift auf den nativen positiven Wachstumszweig und dessen Aufholregeln zu; sie garantiert keinen festen absoluten Ertrag.

Weitere Themen können nach einer eigenen Wirkungsprüfung folgen: Bergbausicherheit, Lagerhaltung und Kühlketten, Bewässerung, Tourismus, medizinische Forschung, nukleare Betriebssicherheit und elektronische Planungsdaten. Wo ein wirklicher Verbraucher fehlt, wird zuerst eine kleine nachvollziehbare Mechanik entworfen. Ein neuer Spiritname allein ist keine solche Mechanik.

## 8. Grenzen gegen den unbegrenzten Kauf von Wachstum

Wiederholte identische Programme ersetzen oder verlängern ein bestehendes Programm; sie addieren dessen Stufen nicht nochmals. Als erste RGW-eigene Obergrenzen gelten +30% landesweites Produktivitätswachstum aus dieser Programmgruppe, +5% zivile Produktivität aus Standardisierung und Qualitätskontrolle zusammen sowie +8% Agrarertrag aus den beiden Agrarprogrammen zusammen. Länderbezogene und staatliche Wachstumsförderung müssen außerdem gemeinsam auf Überschneidungen geprüft werden. Vorhandene nationale Wirtschaftsmodelle und unabhängig erworbene Leistungen werden nicht durch einen globalen Reset verändert.

Ein Land mit großem Kassenbestand kann mehr Vorhaben finanzieren. Es braucht weiterhin Zeit, Standorte, passende Technik, Arbeitskräfte, Energie und tatsächlich verfügbare Partnerleistungen. Ein Finanzier kann deshalb kein unendliches Wachstum durch wiederholtes Annehmen derselben kleinen Kampagne kaufen. Unterschiedliche Programme dürfen sich ergänzen, wenn sie unterschiedliche reale Maßnahmen finanzieren.

Die Organisation ist auch kein automatischer Erfolgsgarant. Nationaler Widerstand, inkompatible Standards, Terminprobleme und die Bevorzugung vollständiger eigener Industrien begrenzten historische Kooperation. Eine zeitgenössische Untersuchung beschreibt unter anderem schwache direkte Unternehmenskontakte und Koordinationsprobleme. [Bela Balassa, World Bank Staff Working Paper 185, 1974](https://documents.worldbank.org/curated/en/832621467980499934/pdf/SWP185000Types0of0economic0integration.pdf). Diese Grenzen werden über sichtbare Voraussetzungen, tatsächliche Lieferausfälle und neu verhandelbare Verträge abgebildet.

## 9. Darstellungs- und Prüfumfang

In der UI erhalten Bauprojekte und Programme getrennte Filter innerhalb der vertrauten Zielkarten. Ein Programm zeigt Fachbereich, Teilnehmer, eigene Wochenkosten, Kostenanteile der Partner, bezahlte Phase und nächste konkrete Wirkungsstufe. Die Effects-Ansicht zeigt die vollständigen benannten/numerischen Folgen auch vor der Zustimmung und bei aktuell unerfüllten Voraussetzungen. Eine politische Erklärung ersetzt keine Effektliste.

Implementierungspriorität: ein Bauprojekt und ein Produktivitätsprogramm mit allen Zustimmungs-, Zahlungs-, Vorschau- und Wiederaufnahmewegen. Danach folgen weitere geprüfte Vorlagen. Der vorliegende Entwurf selbst verändert weder die globale Wirtschaft noch laufende nationale Programme. Die aktualisierte Finanzierungssimulation zeigt die höheren Baupreise und langfristigen Rückzahlungsbedingungen, keine fertige Spieloberfläche.

## 10. Quellen, Herkunft und Grenzen

Eigenständiger Konzepttext für IMPERIA COLD WAR. Lokale Preis- und Formelbefunde stammen aus dem genannten MD-Cold-War-Checkout, gelesen am 24. Oktober 2026. Aktuelle Spielstandwerte wurden nicht erhoben. Code und Preise wurden nicht als historische Messwerte ausgegeben.

Native Spielmechaniken: Paradox Interactive. MD- und Projektanpassungen: MD-Team und jeweilige Projektbeitragende; einzelne Urheber und genaue Weiterverwendungslizenz der betrachteten lokalen Zeilen sind nicht vollständig bekannt. Es wurden keine fremden Bilder kopiert und keine fremden Codeblöcke in neue Laufzeitdateien übernommen.

Historische Quellen: UNIDO-Bericht 1978 zur Institutionsstruktur, IWF-Analyse 1991 zur staatlichen Handelsabwicklung, UN-Vertragsregister zur Standardisierungskonvention, zeitgenössische UN-Sitzungsprotokolle und Bela Balassas Working Paper 185 von 1974. Die IWF-Seite sowie die UN-Sitzungsprotokolle waren im Direktabruf teilweise nicht erreichbar; dort wurden die recherchierbaren Textauszüge verwendet. Für die Konvention wurde die bibliografische Registrierung ausgewertet, nicht ein vollständig gelesener Vertragstext.

Ergänzend recherchiert: *Instruments and Methods for the Economic Co-operation and Integration of the Member Countries of the CMEA, Particularly in Relation to Industrial Development*, 1979, herausgegeben über UNIDO und verfasst vom RGW-Institut für die wirtschaftlichen Probleme des sozialistischen Weltsystems. Diese Quelle dokumentiert die eigene institutionelle Perspektive; ihre Erfolgsbehauptungen und Produktivitätsstatistiken werden hier nicht als unabhängig bestätigte Leistungswerte übernommen. Auch die Rede von 1976 enthält Selbstdarstellungen der Organisation. Die Kampagnenwirkungen sind eigene Balancevorschläge.

Die UNIDO-Publikationen erlauben wissenschaftliche beziehungsweise pädagogische Zitate unter Quellenangabe. Weitergehende Rechte an den übrigen Quellen und an individueller fremder Gestaltung sind nicht ermittelt und bleiben unbekannt. Die Quellen werden knapp paraphrasiert; kein fremdes Bildmaterial wird übernommen.
