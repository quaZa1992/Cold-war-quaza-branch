IMPERIA COLD WAR: COMECON System Concept
========================================

Aktueller maßgeblicher Nutzerstand: [Gemeinsames Produktionsprojekt und rote Oberfläche](COMECON_SHARED_PRODUCTION_REVISION.md). Ein gewählter Host erhält die Anlagen, die anderen zahlenden Teilnehmer automatisch zeitweilige sektorale Produktionsboni. Diese Revision ersetzt für den normalen Projekttyp den vorher entworfenen Einzelabruf von Lieferpaketen und erhöht die Industriepreise erneut. Ältere Varianten unten bleiben als Entstehungs- und Quellenkontext gekennzeichnet.

Stand: 24. Oktober 2026. Konzept zur Diskussion, keine Freigabe zur Implementierung. Die geladenen Spieldateien wurden nicht geändert. Deutsche Erläuterungen sind Projektdokumentation; vorgeschlagene Spielnamen und UI-Beschriftungen sind Englisch. Die ergänzende Revision [Institutionen, höhere Kosten und gemeinsame Programme](COMECON_INSTITUTIONS_CAMPAIGNS.md) konkretisiert die historische Arbeitsweise und ergänzt Produktivitäts- und weitere Fachprogramme.

Die aktuelle Ergänzung [Rücklieferungen, Standortwahl und sowjetische Vertretung](COMECON_DELIVERIES_COUNCIL_SSR.md) beschreibt gebäudespezifische Lieferprogramme, Vertragsabstimmungen und SSR-Empfänger ohne zusätzliche Ratsstimme. Dazu besteht eine interaktive Bedienvorschau, keine native Spielimplementierung.

## 1. Empfehlung

COMECON erhält eine eigenständige Wirtschaftsorganisation mit der Bildsprache und Bedienung des vorhandenen Factions-Fensters: gleicher Fenstertyp, Kopfbereich, Mitgliederflaggen, Einflussdarstellung, Zielkarten, Tabs, Fortschrittsbalken und seitliche Detailfenster. Die Wirtschaftsinhalte erhalten eigene Daten und Regeln. Militärbündnis und Wirtschaftsmitgliedschaft bleiben unabhängig.

Das zentrale Spielversprechen: Ein Land kann mit Partnern eine Industrie aufbauen, Lieferungen sichern und Forschung finanzieren. Dafür bindet es Geld, Produktionsmöglichkeiten und seine außenwirtschaftlichen Optionen. Größere Integration bringt stärkere gemeinsame Leistungen und höhere Abhängigkeit von konkreten Partnern.

## 2. Was die vorhandenen Factions tatsächlich bereitstellen

Untersuchter Stand: Der Checkout deklariert MD 2.0.2 und HOI4 1.19.*. Das ist eine Dateiangabe, kein Nachweis der aktuell laufenden Spielversion.

| Vorhandener Baustein | Befund | Geplante Verwendung |
|---|---|---|
| Hauptfenster | `interface/factions/countryfactionview.gui`: 550 Einheiten Breite, Organisationstitel, Manifest und Fortschritt, Mitgliedereinfluss, fünf Tabs | Dieselbe Anordnung und vorhandene Grafikressourcen als Vorlage |
| Ziele | Drei Spalten für kurz-, mittel- und langfristige Ziele; Karten mit 174 x 84 Einheiten | Lieferprotokolle, Investitionsvorhaben und mehrjährige Integrationsziele |
| Regeln | Native Regelgruppen mit Bedingungen, Modifikatoren und Änderungskosten | Darstellungsprinzip für Ratsbeschlüsse; eigene wirtschaftliche Abstimmungslogik |
| Forschung | Forschungsverbesserungen sowie Ansichten für Programme, Einrichtungen und Wissenschaftler | Forschungsabkommen und zivile Gemeinschaftsprogramme |
| Projekt-Detailfenster | `interface/factions/faction_research.gui`: seitliches Fenster mit 450 Einheiten Breite | Eigener Projektinspektor mit Beiträgen, Standort und Ergebnissen |
| Native Upgrades | Dokumentiert sind Forschungs-, Geheimdienst- und Doktrinkooperation sowie Personalbeiträge | Wirtschaftliche Aufträge und Banken benötigen zusätzliche Mechanik |
| Organisationsoberflächen im Mod | `common/scripted_guis/01_european_union_guis.txt` verwendet Spielerkontext, Länderlisten, Abstimmungen und Aktualisierungsvariablen | Technisches Referenzmuster für eine eigenständige, netzwerksynchronisierte Wirtschaftsorganisation |

Wichtige Grenze: Die mitgelieferte Faction-Dokumentation beschreibt bei `can_leader_join_other_factions = yes` die Auflösung des bisherigen Bündnisses, wenn dessen Führer einem anderen Bündnis beitritt. Das ist keine belegte Lösung für parallele RGW- und Warschauer-Pakt-Mitgliedschaften. Die native Oberfläche ist außerdem an ihre Faction-Daten gebunden. Ein bloßes Kopieren und Umbenennen der GUI erzeugt kein zweites unabhängiges System.

Daraus folgt die Architekturentscheidung: vorhandene Faction-Grafiken und Interaktionsmuster wiederverwenden; Datenanbindung, Projekte, Rat, Abrechnung und Mitgliedschaften als eigene Scripted GUI umsetzen. Die nativen Militärfunktionen werden im Wirtschaftsfenster durch fachlich passende Funktionen ersetzt. Eine pixelgleiche Darstellung und jede Listen-/Tooltipfunktion brauchen später einen Prototyp und einen Test im Spiel.

## 3. Historische Ausgangslage und Grenzen

Für Januar 1970: aktive Mitglieder Sowjetunion, DDR, Polen, Tschechoslowakei, Ungarn, Rumänien, Bulgarien und Mongolei. Albanien erhält einen inaktiven historischen Status statt aktiver Mitgliedervorteile. Jugoslawien wird als Kooperationspartner geführt. Kuba und Vietnam können aufgenommen werden; die historischen Bezugspunkte sind 1972 beziehungsweise 1978. Diese Daten beschreiben die Geschichte und rechtfertigen keine pauschale Sperre für einen im RP anders ausgehandelten Beitritt. [Mitgliederübersicht](https://www.encyclopedia.com/social-sciences-and-law/political-science-and-government/international-organizations/council-mutual-economic-assistance)

Der Rat arbeitet nach dem Konsens der interessierten Länder. Ein Land kann sich bei einem Vorhaben für nicht interessiert erklären; die übrigen können es weiterverfolgen. [UNIDO 1978, gedruckte S. 14-15](https://downloads.unido.org/ot/47/91/4791252/00001-10000_07981_1978.pdf)

Zwei Finanzinstitutionen bleiben getrennt: Die IBEC dient dem Zahlungsverkehr und Clearing, die IIB der Investitionsfinanzierung. Der Transferrubel wird als Verrechnungseinheit behandelt. Guthaben sind kein frei verfügbares Dollarvermögen und ersetzen nicht die nationalen Währungen. Das 1971 beschlossene Comprehensive Programme ist der historische Bezugspunkt für vertiefte Integration. [IWF 1976](https://www.elibrary.imf.org/view/journals/024/1976/003/article-A008-en.xml), [IIB: Gründungsabkommen vom 10. Juli 1970](https://iib.int/en/about)

## 4. Oberfläche

Zugang über einen eigenen Organisationsknopf neben den vorhandenen internationalen Organisationen. Das Militärbündnisfenster bleibt erreichbar. Mitglieder, Beitrittskandidaten und projektbezogene Partner erhalten passende Ansichten; externe Staaten können öffentliche Informationen sehen.

Kopfbereich: **Council for Mutual Economic Assistance**, Organisationssymbol, **Secretariat: Moscow**, laufender Plan und **Plan Fulfilment**. Der Erfüllungsgrad ergibt sich aus den für diesen Plan bestätigten Meilensteinen und tatsächlich erfüllten Lieferungen. Rein angekündigte Beiträge erhöhen ihn nicht. Der Plan ist nach Beginn festgelegt; Streichungen werden als Änderungen dokumentiert und verbessern nicht rückwirkend die Quote.

Mitgliederbereich: Flaggen, Status und wirtschaftlicher Beitrag. Das Kreisdiagramm zeigt den Anteil tatsächlich eingebrachter Finanzierung und Lieferleistungen. Sein Tooltip trennt wirtschaftliches Gewicht von formaler Stimmabgabe. Ein großer Finanzier erhält dadurch keine zusätzlichen Ratsstimmen. Institutioneller Vorsitz und sowjetische Wirtschaftsmacht sind unterschiedliche Größen.

| Tab im Wirtschaftsfenster | Inhalt und Aktionen |
|---|---|
| **Plans** | Zielkarten in den drei bekannten Zeithorizonten, Projekte vorschlagen, teilnehmen, Fortschritt und abgeschlossene Pläne prüfen |
| **Council** | Offene Vorschläge, Zustimmung, Ablehnung, Nichtteilnahme, Vertragsbedingungen, Aufnahme und Änderung gemeinsamer Regeln |
| **Research** | Forschungsbeiträge, bereits verfügbare Verfahren, zivile Programme, gemeinsame Standards und vereinbarte Technologieübertragung |
| **Trade & Specialisation** | Lieferverträge, sektorale Spezialisierungen, Abnehmer, ausstehende Lieferungen und konkrete Abhängigkeiten |
| **Finance** | IBEC-Abrechnung, IIB-Kredite, eingezahltes Kapital, Projektkonten, wöchentliche Verpflichtungen und Rückzahlung |

Ein Kartenklick öffnet rechts den Projektinspektor. Er zeigt Teilnehmer, Standort, Laufzeit, bereits gezahlte Beträge, verbleibende Beiträge, Bauvoraussetzungen und die vollständigen Ergebnisse für jedes Land. Geplante, laufende, pausierte, abgeschlossene und abgelehnte Projekte bleiben unterscheidbar.

## 5. Gemeinsames Projekt: der vollständige Ablauf

1. Ein Mitglied schlägt ein Vorhaben vor. Es benennt Standort, Partner, Zweck und ein Angebot mit festen Zahlen.
2. Die betroffenen Länder entscheiden selbst. Die Antwortmöglichkeiten sind Zustimmung, Ablehnung und Nichtteilnahme. Geänderte Bedingungen bilden einen neuen Vorschlag und verlangen neue Zustimmung. Schweigen erzeugt keine Verpflichtung.
3. Das Vorhaben beginnt, sobald die erforderlichen Länder, der Standortstaat und die vereinbarte Mindestfinanzierung zugestimmt haben. Ein nicht interessiertes Land blockiert ein unabhängiges Projekt nicht. Für eine Leitung durch sein Territorium oder seinen Produktionsbeitrag bleibt seine ausdrückliche Zustimmung erforderlich.
4. Wöchentliche Zahlungen und vereinbarte Leistungen erzeugen Fortschritt. Der Projektinspektor zeigt getrennt Geld, Lieferungen und Bauzeit. Ein überwiesener Betrag ersetzt keine fehlende technische Voraussetzung.
5. Meilensteine gewähren konkret vereinbarte Gebäude, Infrastruktur, Forschungsboni oder andere Leistungen. Projektteilnahme allein vergibt keine vollständige Fabrik.
6. Nach Fertigstellung verbleiben Gebäude beim tatsächlichen Standortstaat. Laufende Liefer-, Wartungs- oder Kooperationsvorteile hängen von ihren Verträgen ab. Ein Austritt entfernt keine errichtete Fabrik, beendet aber vertraglich abhängige Leistungen nach den vereinbarten Bedingungen.

Projekte können gemeinsam finanzierte Infrastruktur, nationale Investitionen mit Partnerkredit oder reine Liefer-/Forschungsabkommen sein. Nicht jedes historische Vorhaben war ein Eigentumsprojekt des gesamten RGW. Die Oberfläche zeigt deshalb nur die tatsächlichen Vertragspartner und Begünstigten.

## 6. Projektkatalog

Die folgenden Namen sind Vorschläge für englische Spieltexte. Ergebnisse und Nachteile sind Designvorschläge; sie beschreiben keine bereits implementierten Effekte.

| Vorhaben | Historischer Bezug | Möglicher Spielgewinn | Kosten und institutioneller Konflikt |
|---|---|---|---|
| **Interconnected Power Grid** | Zwischenstaatliche Stromnetzkoordination | Bezahlter Netzausbau, regional nutzbarer Kapazitätsausgleich | Kraftwerke und Leitungen müssen real vorhanden sein; Ausfall eines Exporteurs betrifft seine angeschlossenen Abnehmer |
| **Common Wagon Pool** | Gemeinsamer Güterwagenpool | Bessere Nutzung vorhandener Logistikkapazität, abgestimmte Transportinvestitionen | Beiträge und Wartung; Vorteile nur für angeschlossene Teilnehmer und passende Netze |
| **Ikarus Production Expansion** | IIB-finanzierter ungarischer Werksausbau | Industrieausbau am Standort, vereinbarte Zulieferaufträge und Verfahrenstransfer | Finanzierungsbindung, Spezialisierung auf Partnerabsatz, vertragliche Ersatzteilabhängigkeit |
| **Intermetal Production Agreement** | Internationale Stahlkoordination und Spezialisierung | Gezielt finanzierter Metallurgieausbau, besser nutzbare Kapazitäten | Großinvestitionen und Abnahmeverpflichtungen; geringere kurzfristige Flexibilität |
| **Soyuz Gas Development** | Orenburg-/Sojuz-Gemeinschaftsvorhaben | Gasförderung, Transit und vereinbarte Versorgung für beteiligte Länder | Mehrjährige Kapitalbindung, Bedarf an Transitgenehmigung, Abhängigkeit vom Lieferstaat |
| **Interatomenergo Programme** | Nukleare Anlagen- und Komponentenkooperation ab 1973 | Reaktor- und Komponentenprogramme, zivile Forschungsboni und Standardisierung | Hohe Bau- und Unterhaltskosten, Brennstoff- und Dienstleistungsbindung, tatsächliche Technologie- und Sicherheitsvoraussetzungen |
| **Joint Mineral Development** | Beispielsweise sowjetisch-mongolischer Erdenet-Ausbau | Bezahlte Erschließung, lokale Infrastruktur und vereinbarte Abnahme | Lange Vorlaufzeit und Finanzierung; Förderstandort und Käufer haben unterschiedliche Interessen |
| **Agricultural Supply Protocol** | Langfristige zwischenstaatliche Lieferabkommen | Planbarer Absatz für Erzeuger und gesicherte Lieferungen für Abnehmer | Subventionen werden von einem benannten Land bezahlt; günstige Vertragspreise haben Opportunitätskosten |

Die Vorbilder dienen unterschiedlichen Funktionen. Ein Energieverbund ist eine technische Verbindung; ein Lieferprotokoll ist ein Vertrag; ein Werk ist eine Investition. Diese Vorhaben dürfen nicht alle denselben pauschalen Produktivitätsbonus erhalten.

Belege: UNIDO dokumentiert Stromnetzkoordination, Intermetal, Güterwagenpool und den Ikarus-Kredit. [UNIDO 1981](https://downloads.unido.org/ot/47/91/4791253/00001-10000_07981_1981.pdf). Das Orenburg-/Sojuz-Vorhaben war eine gemeinsame Investition mit Fertigstellung der Leitung 1978. [US Country Study, Appendix B](https://www.marines.mil/Portals/1/Publications/Czechoslovakia%20Study_4.pdf). Interatomenergo wurde im Dezember 1973 gegründet. [IAEA-TECDOC-922, gedruckte S. 163](https://www-pub.iaea.org/MTCD/Publications/PDF/te_0922_scr.pdf). Der Erdenet-Betreiber dokumentiert das bilaterale Abkommen von 1973 und den ersten Ausbau von 1978; dieses Beispiel wird nicht als allseitiges RGW-Eigentum ausgegeben. [Erdenet: Unternehmensgeschichte](https://www.erdenetmc.mn/en/about)

## 7. Spezialisierung und wirtschaftspolitische Entscheidungen

Jedes Land wählt seine Verpflichtungen selbst. Historische Stärken liefern Angebote, aber kein Land wird dauerhaft auf eine wirtschaftliche Rolle festgelegt. Angebote enthalten den Ausbau des gewählten Sektors und konkrete Gegenleistungen der Partner.

Beispiel eines realen Zielkonflikts: Ungarn kann eine größere Busproduktion für den gemeinsamen Markt aufbauen. Ein breit gestreutes nationales Industrieprogramm bietet stattdessen mehr Eigenständigkeit, verlangt aber eigene Finanzierung und einen eigenen Absatzmarkt. Rumänien kann einzelne Spezialisierungsabkommen ablehnen und dennoch an Energie- oder Transportprojekten teilnehmen.

Eine Vertiefung der Integration erweitert gemeinsam vereinbarte Standards, Lieferbindungen und Investitionen. Eine souveränitätsorientierte Politik hält den Vertragsumfang kleiner. Beide Wege sollen substanzielle, unterschiedliche Ergebnisse liefern. Forschungsleistungen ersetzen dabei nicht automatisch westlichen Technologietransfer; bestehende Embargos und Zugangsbedingungen gelten weiterhin.

Für Rohstoffexporteure bedeutet ein subventionierter Vertrag geringere Einnahmen oder bezahlte Zuschüsse zugunsten eines Partners. Für industrielle Zulieferer bedeutet ein garantierter Auftrag gesicherten Absatz und gebundene Kapazität. Für ein Entwicklungsland bedeutet ein Großprojekt Kapital und Ausbildung, aber auch Kreditdienst und Lieferverpflichtungen. Diese Unterschiede sollen die Verhandlungen tragen.

## 8. Finanzen ohne fiktiven gemeinsamen Geldtopf

Es gibt getrennte Abrechnungskreise: einen kleinen vereinbarten Verwaltungsbeitrag, finanzierte Projektkonten, IBEC-Verrechnungspositionen und IIB-Kapital beziehungsweise Kredite. Eine Mitgliedschaft überweist nicht automatisch einen großen Anteil des Staatshaushalts an Moskau.

Alle wiederkehrenden Spielerbeträge werden in MD-Geldeinheiten pro Woche ausgewiesen. Für jede Verpflichtung sind Zahler, Empfänger, Betrag, Beginn und Ende sichtbar. Historische Budgets werden vor der Integration in diese Einheiten umgerechnet; die endgültigen Werte brauchen eine Kalibrierung an den tatsächlichen Volkswirtschaften des 1970-Starts.

Eine Kreditzusage ist noch kein ausgezahltes Geld. Bankauszahlungen benötigen eingezahltes Kapital oder ausdrücklich vereinbarte Finanzierung. Sie erzeugen beim Kreditnehmer genau eine Schuldposition. Tilgung mindert diese Position und zahlt Geld an den Gläubiger zurück; Zinsen sind davon getrennt. Entweder werden diese Schulden konsistent in die MD-Schuldendarstellung eingebunden oder eindeutig separat ausgewiesen. Eine doppelte Verbuchung in beiden Systemen ist ausgeschlossen.

Clearingguthaben geben einen Anspruch auf vereinbarte Leistungen innerhalb des Vertragsnetzes. Sie können nicht beliebig in MD-Staatsgeld oder Devisen umgewandelt werden. Eine vereinfachte erste Fassung kann stattdessen nur finanzierte Projektkonten und reale Geldtransfers anbieten, bis das Clearing sinnvoll integriert ist.

## 9. Ein vollständig beziffertes Beispiel

Das überarbeitete [Finanzierungsmodell und der Effektkatalog](COMECON_INTERACTIVE_FINANCING.md) ersetzen das ursprüngliche Ikarus-Beispiel mit festen Beiträgen und gleichen nationalen Teilnehmerboni. Jedes Land wählt seinen Projektanteil und die Vertragsform. Der Standortstaat erhält die Anlage; externe Finanzierung begründet vereinbarte, begrenzte Ansprüche.

Aktuelles Rechenbeispiel nach der Kostenrevision: **Joint Industrial Plant: Standard** in Ungarn, 37.440 Milliarden Gesamtbudget über 156 bezahlte Wochen. Die frei wählbare Beispielverteilung beträgt Sowjetunion 50%, Ungarn 20%, DDR 15%, Tschechoslowakei 15%. Daraus folgen Bauzahlungen von 0.120, 0.048, 0.036 und 0.036 Milliarden pro Woche. Ergebnis: **+2 shared building slots**, danach **+2 civilian factories** in Ungarn.

Wer seinen externen Beitrag rückzahlbar anbietet, erhält einen entsprechenden Anspruch; wer einen Zuschuss wählt, erhält keine Forderung. Der neue Vorschlag sieht 780 Wochen Kapitaltilgung und einen sinkenden wöchentlichen Zins auf die verbleibende Hauptforderung vor. Die erste ungarische Gesamtzahlung beträgt im Beispiel 0.04992 Milliarden pro Woche. Diese Bedingungen sind Balancevorschläge; der ergänzende Finanzierungsentwurf zeigt Formel und Länderbeträge. Zusätzliche Forschung, Liefervereinbarungen, nationale Fachprogramme und Betriebskosten werden gesondert bepreist und angezeigt.

## 10. Krisen, Ausstieg und reale Nachteile

Auslöser werden aus tatsächlichen Zuständen abgeleitet: unbezahlte Beiträge, fehlende Energie, ausstehende Waren, verlorener Standort, Sanktionen oder Krieg zwischen Vertragspartnern. Betroffen sind zunächst die zugehörigen Verträge und angeschlossenen Projektteile. Ein Krieg eines Mitglieds gegen ein Drittland löst nicht automatisch den gesamten RGW auf.

Bei einem Lieferausfall kann der Abnehmer einen Ersatzlieferanten suchen, Marktimporte bezahlen, einen Überbrückungskredit beantragen oder sein Programm reduzieren. Der Lieferant kann Reserven einsetzen, neue Preise vorschlagen oder eine geordnete Vertragsauflösung verhandeln. Neue Bedingungen gelten erst nach Zustimmung der betroffenen Länder.

Ein Austritt beendet Mitgliedervorteile und verhindert neue Mitgliederprojekte. Bestehende Schulden, bereits errichtete Anlagen und ausdrücklich weiterlaufende Einzelverträge werden getrennt abgewickelt. Ein wieder eintretendes Land erhält keine Wiederholung derselben Einmalbelohnung. Seine Rückkehr löscht keine frühere Schuld.

Für den Einstieg empfehle ich die konkreten Projekt-, Preis- und Kreditkonflikte. Ein umfangreiches zusätzliches System zufälliger Krisen und pauschaler Stabilitätsstrafen ist dafür nicht erforderlich.

## 11. Einbindung in den vorhandenen Mod

Vor einer Implementierung werden vorhandene Comecon-Leistungen inventarisiert: `mdcw_cw_dec_comecon` setzt bereits ein zeitweiliges Blockprogramm; der sowjetische Fokus `COLDWAR_SOV_the_comprehensive_programme` setzt eigene Leistungen und einen dazugehörigen Status; `COLDWAR_SOV_monthly_comecon_refund` gewährt unter Bedingungen eine einmalige PP-Erstattung. Die DDR besitzt mehrere Spezialisierungs- und Kooperationsinhalte.

Kuba besitzt bereits einen echten Mitgliedschaftsspirit `COLDWAR_CUB_cmea_member` und bilaterale, zustimmungsabhängige Verträge. Diese werden nicht durch ein widersprechendes zweites Kuba-Beitrittsmenü ersetzt. Kubanische bilaterale Angebote bleiben in ihren genehmigten nationalen Fokussen verankert. Das Organisationsfenster zeigt ihren Status und ihre Projekte an. Änderungen an diesen genehmigten Angeboten brauchen einen gesonderten Abgleich mit der jeweiligen Designquelle.

Der Warschauer Pakt besitzt bereits eine Forschungsgruppe. Eine zusätzliche RGW-Mitgliedschaft darf nicht dieselbe Zusammenarbeit nochmals unbegrenzt belohnen. Für wirtschaftliche Kooperation sind gezielte zivile Boni und klar begrenzte Programme vorzuziehen. Eine native technologiebezogene Nachholgruppe wird erst eingeplant, wenn ihre Filter und Stapelung im aktuellen Spiel geprüft sind.

Eine gemeinsame Mitgliedschaftsquelle und klar abgegrenzte Verträge verhindern widersprüchliche Anzeigen. Langfristig lesen Organisationsfokusse den tatsächlichen Mitgliedschaftsstatus sowohl bei Verfügbarkeit als auch bei Belohnung. Ein Beitrittsweg muss davor erreichbar sein.

## 12. Vorschlag für die erste spielbare Fassung

1. Native Faction-Bildsprache mit eigenem Mitgliederbereich, Zielkarten und Projektinspektor; alle 1970-Mitglieder und sinnvolle Partnerstatus.
2. Ratsbeschlüsse, echte Zustimmung der betroffenen Spieler und finanzierte Projektkonten mit Wochenabrechnung.
3. Vier vollständige Projektfamilien: Stromverbund, Güterwagen-/Transportkooperation, Industrieausbau und Entwicklungsinvestition.
4. Spezialisierungsverträge, Lieferbindungen, Pausierung, Wiederaufnahme und geordneter Austritt.
5. Abgleich der sowjetischen, DDR- und kubanischen Inhalte sowie vorhandener Forschungsboni.

Als Erweiterung folgen IIB-Kredite, IBEC-Clearing, große Gas- und Nuklearvorhaben und zusätzliche Forschungseinrichtungen. Eine frühe Oberfläche darf diese Bereiche als geplante spätere Funktionen kennzeichnen; sie darf keine funktionsfähige Bank simulieren, solange nur ein Zähler dahinterliegt.

## 13. Anforderungen an spätere Umsetzung und Nachweis

Nur der Spielzustand rechnet Zahlungen, Stimmen und Projektfortschritt ab. Das Öffnen oder Aktualisieren eines Fensters bewirkt keine Zahlung und keinen Fortschritt. Der Projektinspektor zeigt vollständige native numerische Effekte für jedes betroffene Land auch vor Annahme und bei nicht erfüllten Voraussetzungen. Laufende Kosten verwenden Wochenbeträge; Scriptliterale besitzen höchstens fünf Nachkommastellen.

Gebäude erhalten vor jeder gewährten Stufe einen zusätzlichen gemeinsamen Bauplatz im selben Staat. Eigentum, Kontrolle, Kapazität, Abrechnung und Einmaligkeit werden bei Ausführung separat geprüft. Eine reine Vorschau führt keine Effekte aus. Diplomatische, kriegs- und sanktionsabhängige Abkommen benötigen konkrete Aussetzungs- und Wiederherstellungsregeln; bereits genehmigte kubanische Verträge behalten ihre strengeren bestehenden Regeln.

Zu testen sind insbesondere zwei gleichzeitige Vorschläge, veränderte Bedingungen nach einer Antwort, fehlende Zahlung, Standortverlust, Abbruch nach Teilzahlung, Aufnahme außerhalb des Militärbündnisses, Aus-/Wiedereintritt, Regierungskrise, Speichern/Laden und Multiplayer-Synchronisierung. Auf grafischer Seite sind alle Tabs, benachbarten Elemente, Listenlimits, Tooltips, Auflösungen und das seitliche Detailfenster im Spiel zu prüfen. Quellcodeinspektion beweist diese Laufzeiteigenschaften nicht.

## 14. Quellen- und Provenienzvermerk

Dieser Entwurf ist für IMPERIA COLD WAR verfasst. Quellen wurden am 24. Oktober 2026 recherchiert. Historische Tatsachen, vorgeschlagene Spielabstraktionen und Befunde aus dem lokalen Quelltext sind im Dokument unterschieden. Es wurden keine fremden Texturen kopiert, Bilder erzeugt oder Laufzeitdateien verändert.

- Native Factions: lokale Spielinstallation `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/common/factions/_documentation.md` und genannte MD-GUI-Dateien. Urheber: Paradox Interactive für die nativen Systeme; MD-Team beziehungsweise jeweilige Beitragende für Modanpassungen. Exakte Urheber einzelner Grafikdateien und deren Weiterverwendungslizenz wurden für dieses Konzept nicht verifiziert und bleiben unbekannt. Eine spätere Nutzung muss vorhandene Rechte und Attributionen wahren.
- Organisationsoberfläche: bestehende MD-/Projekt-EU-Datei `common/scripted_guis/01_european_union_guis.txt` als technischer Vergleich, ohne Änderung oder Übernahme politischer EU-Inhalte. Einzelautorenschaft und genaue Lizenz dieser lokalen Fassung: unbekannt.
- UNIDO, *Institutional Mechanisms for Economic and Industrial Co-operation among Member Countries of the CMEA*, Fassungen 1978 und 1981, oben verlinkt. Institutioneller Autor: UNIDO/International Centre for Industrial Studies. Die Veröffentlichungsseite nennt eine Verwendung von Zitaten und Verweisen für Bildung und Forschung unter Quellenangabe. Hier werden historische Befunde knapp paraphrasiert.
- IWF 1976, oben verlinkt: analytische Quelle zu Zahlungen, Konvertibilität und Integrationsprogramm. Vollständiger Artikelabruf war gesperrt; ausgewertet wurden die recherchierbaren Textauszüge. Individuelle Autorenschaft und weitergehende Lizenz wurden nicht verifiziert.
- IIB, oben verlinkt: Selbstauskunft zur Gründung. Direkter Seitenabruf schlug fehl; das Gründungsdatum war im Suchauszug verfügbar. Weitergehende Lizenz und individueller Seitenautor: unbekannt.
- IAEA-TECDOC-922, Januar 1997: institutioneller Bericht zu WWER-Anlagen und historischer Kooperation. Einzelautorenschaft des historischen Abschnitts und Weiterverwendungslizenz: nicht verifiziert.
- *Czechoslovakia: A Country Study*, Appendix B, gehostet vom US Marine Corps: historische Einordnung gemeinsamer Investitionen. Der Host ist kein Beleg für die Urheberschaft jeder enthaltenen Passage. Einzelautorenschaft dieses Abschnitts und genaue Rechte der vorliegenden Ausgabe: unbekannt.
- Erdenet Mining Corporation: Betreiberchronik, ergänzend das oben recherchierte Unternehmensarchiv. Individueller Seitenautor und Lizenz: unbekannt. Die englische Chronik enthält eine widersprüchliche Formulierung zur ersten Produktion; verwendet wird der durch ihre Zeitleiste und das Unternehmensarchiv übereinstimmend belegte Bezug 1978.
- Encyclopedia.com, *Council for Mutual Economic Assistance*, oben verlinkt: sekundäre Übersicht für Mitgliedschaftsdaten. Individuelle Autorenschaft und Lizenz der Seite: nicht verifiziert.

Die Spielwerte im Beispiel wurden eigenständig als verhandelbare Balancevorschläge erstellt. Sie wurden weder im Spiel getestet noch als historisch gemessene Erträge oder Investitionskosten ausgegeben.
