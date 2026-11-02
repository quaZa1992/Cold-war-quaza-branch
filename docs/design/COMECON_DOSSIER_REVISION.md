IMPERIA COLD WAR: COMECON Project Dossiers
========================================

Aktueller Vorrang bei Umfang, Laufzeiten und Programmkatalog: [COMECON_SCALE_DAYS_PROGRAMMES.md](COMECON_SCALE_DAYS_PROGRAMMES.md). Die Partnerleistungen skalieren inzwischen mit +3% / +5% / +8%, die Anzeige verwendet aktive Tage, das Register hat keine Programmjahre und enthält elf zivile Investitionsvorlagen. Die früheren festen +5%- und Wochenlaufzeitangaben unten sind dadurch überholt.

Stand: 24. Oktober 2026. Maßgebliche Revision für Gestaltung, aktuelle Länderflaggen und die auswählbare Gegenleistung eines Gemeinschaftsprojekts. Sie ersetzt die rote Dashboard-Gestaltung und den ausschließlich vorgegebenen Produktionsbonus in `COMECON_SHARED_PRODUCTION_REVISION.md`. Die dortigen Finanzierungs-, SSR- und Ausführungsregeln gelten weiter, soweit hier nicht ausdrücklich geändert. Konzept und interaktive Vorschau, keine native Laufzeitimplementierung.

## Gestaltung und aktuelle Flaggen

Die Organisation erscheint als bearbeitete Projektakte: sandfarbener Umschlag, helles Papier, Register, Formularlinien, Schreibmaschinenschrift für Aktenangaben und bordeauxfarbene Stempel. Drei Ansichten: **Programme**, **Contributions**, **Signatures**. Keine zusätzliche Währungsverwaltung im Fenster.

Das echte RGW-Emblem mit dem Gebäude und dem umlaufenden Organisationsnamen wird als vorhandene Grafik verwendet. Quelle, Urheber und Rechteangaben stehen unten und in der Begleitdatei der Vorschau.

**Jede Flagge der späteren Spieloberfläche stammt vom aktuell dargestellten Land über dessen natives `GetFlag`.** Das gilt für Mitgliedsübersicht, Beitragsliste, Ratsdelegation, Anlagenstandort und Ergebnisempfänger. Regierungswechsel und Cosmetic Tags dürfen nicht durch fest hinterlegte historische PNGs übergangen werden. Ein Anlagenstandort in einer SSR zeigt die aktuelle SSR-Flagge; die sowjetische Ratsdelegation zeigt weiterhin die aktuelle sowjetische Flagge.

Vorhandenes natives Muster: `common/scripted_guis/01_european_union_guis.txt`, etwa `image = "[?global.eucouncil.GetFlag]"`. Die genaue Scope-Zuweisung ist Bestandteil der späteren GUI-Implementierung. Die HTML-Vorschau zeigt lediglich konvertierte Beispiele aus den vorhandenen Mod-Flaggen. Sie liest keinen laufenden Spielstand und simuliert keinen tatsächlichen Flaggenwechsel.

## Projekt und Gegenleistung

Eine Vertragsfassung enthält Vorlage, Anlagenempfänger, Umfang, Standortanforderungen, eigene Finanzierungsangebote und **ein gemeinsames Paket für die anderen zahlenden Teilnehmer**:

* **Production Co-operation**: bei Industrieprojekten beispielsweise **+5% civilian industry productivity**.
* **Construction Assistance**: beim selben Projekt stattdessen **+5% civilian industry construction speed**.

Bei Energie-, Agrar- oder Büroprojekten werden die passenden sektoralen Effekte vorgegeben. Keine freie Auswahl beliebiger Modifier. Die Wahl gilt für dieses Projekt und wird vor der Zustimmung festgelegt. Eine Änderung benötigt neue Unterschriften. Der Anlagenempfänger erhält die Gebäude; er erhält aus derselben Beteiligung keinen zweiten Zeitbonus.

Nicht-Hosts mit wenigstens 5% bezahltem Anteil erhalten das gewählte Paket nach bezahlter Fertigstellung. Die Laufzeit beträgt `min(156, Anteil in Prozent * 5.2)` aktive Wochen. Ein 20%-Anteil ergibt 104 aktive Wochen, ein 50%-Anteil 156. Kein Bonus auf Basis eines unbezahlten Versprechens. Identische Programme stapeln ihre Stärke nicht mehrfach.

Jeder Nicht-Host trägt während seiner aktiven Leistung vorgeschlagen 0.010% seines BIP pro Woche. Der Host zahlt $20M pro Woche gemeinsame Betreuung, solange mindestens ein Partnerprogramm aktiv ist. Native Gebäude-, Personal-, Brennstoff- und Energiekosten gelten daneben. Die spätere native Vorschau muss den konkret aufgelösten Geldbetrag für jedes Land vor der Unterschrift zeigen. Die Vorschau besitzt keine aktuellen BIP-Werte und zeigt deshalb die Bemessungsregel.

## Historisch begründete Vorlagen

| Akte | Historische Grundlage | Anlage im Spiel | Produktionspaket oder Baupaket |
|---|---|---|---|
| Intermetal | Metallurgische Kooperation, gegründet 1964 | Civilian factory | Civilian industry productivity / civilian industry construction speed |
| Agromash | Landmaschinenkooperation, gegründet 1964 | Civilian factory für Maschinenfertigung | Agricultural district income / agricultural district construction speed |
| Interkhim | Spezialchemie; Vertrag 1969, Inkrafttreten 20. Juli 1970 | Civilian factory | Civilian industry productivity / civilian industry construction speed |
| Common Wagon Pool | Gemeinsamer Güterwagenpool, 1964 | Infrastructure | Civilian industry productivity / infrastructure construction speed |
| United Power Grid | Vereinbarung zur Netzkooperation, 1962 | Fossil power plant | Fossil power generation / fossil power plant construction speed |
| Ikarus | Gemeinsame Investition und Fahrzeugspezialisierung | Civilian factory für Fahrzeugproduktion | Civilian industry productivity / civilian industry construction speed |
| Scientific Information Network | International Centre for Scientific and Technical Information, 1969 | Office | Office productivity / office construction speed |
| Interatomenergo | Nukleare Ausrüstungskooperation, 1973 | Civilian nuclear reactor | Nuclear power generation / nuclear reactor construction speed |

Die Organisationen, Gemeinschaftsunternehmen und Mitgliedschaften waren unterschiedlich. Eine RGW-Mitgliedschaft bedeutete nicht automatisch die Teilnahme an jeder Fachorganisation. Agromash begann beispielsweise als bulgarisch-ungarisches Unternehmen. Ein Standort außerhalb Ungarns im Ikarus-Programm benötigt einen passenden Montage-, Lizenz- oder Zuliefervertrag; die Marke allein legitimiert keine beliebige Fabrik. Der konkrete Vertrags- und Standortnachweis bleibt eine Bedingung der nativen Umsetzung.

Die Anlagen und +5%-Pakete sind Spielabstraktionen, keine behaupteten historischen Vertragskonditionen. Beim Wagenpool abstrahiert zivile Produktivität den wirtschaftlichen Nutzen besserer Logistik. Eine Netzverbindung war historisch kein kostenloser Neubau eines Kraftwerks; die Spielvorlage finanziert ausdrücklich zusätzliche Erzeugung und Anschluss. Das Informationszentrum von 1969 darf nicht mit dem späteren gleichnamigen internationalen Council in Paris verwechselt werden.

Interkhim und Interatomenergo haben in der Vorschau eine eigene institutionelle Vereinbarung. Eine Gründung 1970 wäre bei Interatomenergo eine bewusst verhandelte Vorverlegung, kein historischer Ausgangszustand. Die Vorschau verlangt bei einer neuen gemeinsamen institutionellen Vereinbarung alle acht dargestellten RGW-Delegationen. Das ist eine Spielregel für diese Organisationsentscheidung. Normale Fachprojekte binden ihre tatsächlichen Vertragsparteien; historische Fachmitgliedschaften werden dadurch nicht rückwirkend behauptet.

## Hohe Budgets

Alle Beträge sind vorgeschlagene MD-Spielbudgets, keine historischen Dollarpreise. Sie sind noch nicht an Kassenbeständen eines konkreten Spielstands gemessen. Limited / Standard / Major:

| Vorlage | Gesamtbudget in $B | Bezahlte Wochen | Gebäudestufen |
|---|---|---|---|
| Intermetal | 31.200 / 62.400 / 124.800 | 104 / 156 / 208 | 1 / 2 / 4 |
| Agromash | 26.000 / 62.400 / 124.800 | 104 / 156 / 208 | 1 / 2 / 4 |
| Interkhim | 31.200 / 62.400 / 124.800 | 104 / 156 / 208 | 1 / 2 / 4 |
| Common Wagon Pool | 15.600 / 31.200 / 62.400 | 104 / 156 / 208 | 1 / 2 / 4 |
| United Power Grid | 20.800 / 62.400 / 124.800 | 104 / 156 / 208 | 1 / 2 / 4 |
| Ikarus | 24.960 / 49.920 / 99.840 | 104 / 156 / 208 | 1 / 2 / 4 |
| Scientific Information | 41.600 / 83.200 / 166.400 | 104 / 156 / 208 | 1 / 2 / 4 |
| Interatomenergo | 52.000 / 156.000 / 312.000 | 156 / 260 / 416 | 1 / 2 / 3 |

Wochenrate = Gesamtbudget / bezahlte Wochen. Länderanteil = Wochenrate * zugesagter Prozentanteil. Nur das eigene Land darf sein Beitragsangebot ändern. 5%-Schritte, keine automatische Umverteilung. Vollständige Deckung erfordert genau 100%. Die verfügbaren Bauplätze, native Stufenobergrenzen, tatsächliche Kontrolle und Eigentum werden vor Vergabe separat geprüft. Für jede Gebäudestufe wird zuerst ein zusätzlicher shared building slot im gleichen Staat gewährt, auch bei Infrastruktur. Wenn ein Paket nicht in einen Staat passt, braucht der Vertrag mehrere geeignete, konkret benannte Staaten.

## Zustimmung, SSRs und Bedienung

Die Vorschau verwendet die Sowjetunion als Entwurfsverantwortlichen. Das ist keine Behauptung eines historischen ausschließlichen sowjetischen Antragsrechts. In der nativen Konzeption dürfen Mitgliedsländer eigene Anträge einreichen; jeweils ein eindeutig bestimmter Entwurfsverantwortlicher bearbeitet eine Vertragsfassung. Finanzierungsangebote und Zustimmung bleiben bei den beteiligten Ländern.

Alle verpflichteten Delegationen einschließlich des Hosts stimmen ausdrücklich zu. Eine SSR erhält keinen zusätzlichen Ratsplatz. Die Sowjetunion vertritt ihre Union mit einer Stimme und genau einem vereinbarten Ergebnisempfänger. Lokale SSR-Durchführung mit eigenen Kosten verlangt separat deren Zustimmung. Die lokale Zustimmung ersetzt die sowjetische Unterschrift nicht und erhöht kein Ratsquorum.

Die einzelne sowjetische Ratsstimme gilt für den RGW. In der UN-Generalversammlung behalten die Ukrainische SSR und die Belarussische SSR dagegen ihre eigenen Sitze und Stimmen neben der UdSSR. Sie waren 1945 Gründungsmitglieder und sind im vorhandenen 1970-UN-Code bereits getrennt eingetragen. Ihr SSR-Status darf diese Mitgliedschaften nicht entfernen. Daraus folgen keine eigenen ständigen Sicherheitsratssitze und keine zusätzlichen RGW-Ratsstimmen. [UN-Gründungsmitglieder](https://research.un.org/en/unmembers/founders)

Die **Country view** unten ist ausschließlich eine Bedienhilfe der Vorschau. Im Spiel wird das tatsächlich kontrollierte Land verwendet. Änderungen an Vorlage, Host, Umfang, Paket oder Finanzierungsanteilen erzeugen eine neue Fassung und entfernen die früheren Unterschriften. Nach Ratifikation sind die vereinbarten Bedingungen gesperrt. Ein Änderungsvertrag braucht eine neue Zustimmung; er vergibt nicht erneut bereits gebaute Anlagen.

## Weitere Kampagnen

Die separaten bezahlten Kampagnen aus `COMECON_INSTITUTIONS_CAMPAIGNS.md` bleiben vorgesehen: Arbeitsproduktivität, Ausbilderaustausch, Standardisierung, Qualitätskontrolle, Kraftwerkswartung, Brennstoffersparnis, Agrarberatung und gemeinsame Forschung. Sie bekommen denselben Aktenrahmen, mit nationalen Durchführungskosten und bezahlten Wirkungsstufen statt eines beliebig verschiebbaren Fabrikpreises. Eine historische Themenzuordnung ist noch kein Nachweis für genau diese Spielwerte. Die acht bedienbaren Akten bilden zunächst die gemeinschaftlichen Investitionsvorlagen ab.

## Umsetzung, Nachweise und Herkunft

Ein gemeinsamer autoritativer Wochenlauf verarbeitet nur aktive Projekt- und Teilnehmerlisten. Anzeige und Fensteröffnung buchen kein Geld. Flaggen und Texte werden bei tatsächlichen Länder-, Vertrags- oder Empfängeränderungen aktualisiert. Keine täglichen Länder- oder Staatenvollscans durch GUI-Properties. Abschlussbelege, Restzahlungen und aktive Bonuswochen müssen Speicherung, Ausfall und Wiederaufnahme ohne doppelte Vergabe überstehen.

Geprüfte lokale Leser: `civilian_factories_productivity`, `offices_productivity` und `agriculture_district_income_tax_modifier` in der MD-Geldberechnung; `fossil_pp_energy_generation_modifier` und `nuclear_energy_generation_modifier` in der Energieabrechnung; passende `production_speed_*_factor` im Investitionssystem. Zivile Produktivität beeinflusst hier Steuerbasis/BIP und ist kein militärischer Fabrikausstoß. Native GUI-Synchronisierung und echte Multiplayer-Stabilität sind noch nicht getestet.

Die Vorschau wurde auf Initialisierung, 144 eindeutige Elemente, 11 eingebettete Bilddateien und 50 Interaktionsbedingungen geprüft. Die Desktopansicht wurde im Headless-Browser gerendert und visuell geprüft. Diese Nachweise betreffen die Konzeptvorschau, nicht die spätere HOI4-Laufzeit.

Historische Quellen:

* [UNIDO 1978: Institutional mechanisms](https://downloads.unido.org/ot/47/91/4791252/00001-10000_07981_1978.pdf): Fachorganisationen, Daten und Aufgaben. Zeitgenössische institutionelle Darstellung; Erfolgsangaben werden nicht als unabhängige Wirkungsnachweise übernommen.
* [UN Treaty Series, Volume 856](https://treaties.un.org/doc/publication/UNTS/Volume%20856/v856.pdf): Interkhim-Vertrag und Inkrafttreten.
* [IAEA TECDOC 922](https://www-pub.iaea.org/MTCD/Publications/PDF/te_0922_scr.pdf): Interatomenergo und nukleare Kooperation.
* [International Centre for Scientific and Technical Information, institutionelle Präsentation](https://niscpr.res.in/includes/images/icsti/ppt/sept1919/Session1/Olga-Andreeva.pdf): Zentrum von 1969.
* [UNIDO, Ikarus-Investitionsbeispiel](https://downloads.unido.org/ot/47/91/4791253/00001-10000_07981_1981.pdf): dokumentierter Investitionskontext, keine Quelle der Spielpreise.
* [RGW-Emblem auf Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Logo_of_Comecon.svg): SVG von Vladimir Lobachev, 15. Oktober 2018. Dateiseite nennt PD-RU-exempt; strukturierte Metadaten nennen zusätzlich CC BY-SA 4.0. Beide Angaben sind in der Bildprovenienz festgehalten. Die unveränderte vollständige Emblemzeichnung wurde für die Vorschau gerastert; Urheber und Quelle werden genannt.

Eigenständiger Konzepttext und Bedienlogik für IMPERIA COLD WAR. Native Systeme: Paradox Interactive, MD-Team und Projektbeitragende. Einzelne Urheber und Lizenzen vorhandener Mod-Flaggen sind nicht abschließend bekannt. Die Begleitdatei der Vorschau dokumentiert die tatsächlichen Quelldateien. Der Projektname behauptet keine Urheberschaft an fremden Symbolen oder Flaggen.
