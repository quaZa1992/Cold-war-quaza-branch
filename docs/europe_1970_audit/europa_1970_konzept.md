> **Archived CWEC material.** The custom system was removed on 18 October 2026. [Native MD restoration status](native_restore.md) supersedes the implementation claims below.

# Europäische Gemeinschaften ab 1970 im MD System

Für die Multiplayer-RP-Mod empfiehlt sich ein Umbau des vorhandenen EU-Systems zur Europäischen Gemeinschaft der Sechs mit verhandelbaren Verträgen. Die MD-Oberfläche, Mitgliederverwaltung, Antragswarteschlangen und Geldanbindung sind brauchbare Bausteine. Institutionen, Stimmregeln, Aufnahmeverfahren und politische Inhalte brauchen eine eigene 1970-Fassung. Wirtschaftliche Integration, Währungskooperation und Verteidigung sollten unabhängig voneinander wachsen können.

Untersuchungsstand: 18. Oktober 2026. Grundlage ist der lokale, bereits veränderte Workspace mit MD 2.0.2 und Start am 1. Januar 1970. Das ist keine Prüfung eines möglicherweise neueren externen MD-Releases. Erstellt wurden drei Agentenprüfungen und diese Synthese; geändert wurden ausschließlich Recherchedateien. Die technischen Befunde sind statisch geprüft, noch nicht im Spiel oder Multiplayer erprobt.

Verbindliche Sprachvorgabe: Neue Ingame-Inhalte erhalten ausschließlich englische `l_english`-Lokalisierung. Die konkrete Umsetzung einschließlich Beschlusswirkung, Zahlungslauf und zweckgebundener Förderung steht im [technischen Einbauplan](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/docs/europe_1970_audit/einbauplan_1970.md>).

Aktuelle MP-Vorgabe: Alle politischen Abstimmungen werden ausschließlich durch menschliche Spieler entschieden. KI-Länder können wirtschaftliche Mitglieder bleiben; ihre Sitze und Bevölkerung erzeugen keine Stimmen oder Mehrheitshürden. Die nachfolgend beschriebenen historischen Regeln sind die Referenz, ihre Anpassung an den menschlichen Wählerkreis steht im Einbauplan. Frühere Vorschläge für AI-Abstimmungsverhalten in den Agentenberichten sind damit als Designoption verworfen. Hinzu kommen ein sichtbares Zahlungsprotokoll, auswählbare Integrationsprojekte einschließlich Schengen und Erweiterungen, mitwachsende Institutionen und ein wählbarer Organisationsname.

- [Kernsystem und Initialisierung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/docs/europe_1970_audit/agent_core.md>)
- [Abstimmungen und Oberfläche](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/docs/europe_1970_audit/agent_voting_ui.md>)
- [Fokusse und politische Pfade](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/docs/europe_1970_audit/agent_paths.md>)

## Historische Ausgangslage

1970 bestehen EWG, EGKS und Euratom mit Frankreich, Bundesrepublik Deutschland, Italien, Belgien, Niederlanden und Luxemburg. Seit 1967 haben die Gemeinschaften eine gemeinsame Kommission und einen gemeinsamen Rat. Die Zollunion ist seit Juli 1968 verwirklicht; Agrarpolitik besteht bereits. Diese Errungenschaften gehören deshalb zum Startzustand und sollten nicht erst durch neue Integrationsfoki erworben werden. [EU Geschichte 1960 bis 1969](https://european-union.europa.eu/principles-countries-history/history-eu/1960-69_en).

Für die Institutionen ergibt sich folgendes Startmodell. Das spätere Rechtsverfahren hängt vom Gegenstand ab; nicht jede Entscheidung wird gleich abgestimmt.

| Bereich | Historischer Ausgangspunkt | Konsequenz für die Mod |
| --- | --- | --- |
| Ministerrat | Nationale Regierungen, sechsmonatiger Vorsitz; Belgien im ersten und BRD im zweiten Halbjahr 1970. | Rotierende Tagesordnungs- und Vermittlungsrolle. Kein fünfjähriger ständiger Präsident als Startamt. |
| Gewichtete Ratsabstimmung | FRA, GER, ITA je 4; BEL, HOL je 2; LUX 1 Stimme. | 17 Vertragsstimmen; nicht die moderne Bevölkerungsmehrheit verwenden. |
| Parlament | Nationale parlamentarische Delegierte: FRA, GER, ITA je 36; BEL, HOL je 14; LUX 6. | 142 Sitze. Zunächst Anhörung und Kontrolle; allgemeines modernes Mitgesetzgebungsrecht ist kein Startzustand. |
| Integration | Vertragsänderung und Aufnahme brauchen nationale Ratifikationen. | Ratsbeschluss, Unterschrift und nationale Ratifikation als getrennte Schritte speichern. |

Belege: [Originalvertrag Artikel 138 und 146 bis 148 sowie 236 bis 237](https://www.wipo.int/wipolex/en/text/473854), [amtliche Ratspräsidentschaften Seite 4](https://www.consilium.europa.eu/media/rgpdgmgc/past-presidencies.pdf). Bei qualifizierter Mehrheit gelten mindestens 12 Stimmen auf Kommissionsvorlage; sonst zusätzlich mindestens vier zustimmende Staaten. Enthaltung anwesender oder vertretener Mitglieder verhindert vertragsrechtliche Einstimmigkeit nicht. Eine noch unbeantwortete Spielerentscheidung ist davon technisch zu unterscheiden.

Der Luxemburger Kompromiss von 1966 verlangt bei geltend gemachten wichtigen Interessen politisches Bemühen um eine gemeinsame Lösung. Für RP eignet sich eine Verhandlungspause mit Regierungskrise oder Kompromisspaket. Ein universelles rechtliches Einzelveto über jeden Sachbeschluss wäre eine zusätzliche Spielregel. [Offizielle Ratsgeschichte Seiten 12 bis 13](https://www.consilium.europa.eu/media/30558/qc3112311en.pdf).

Die wichtigsten Entwicklungsmöglichkeiten sind 1970 bereits angelegt, aber noch keine fertigen modernen EU-Institutionen:

| Historischer Bezug | Datum oder Zeitraum | Spielbare Weiterentwicklung |
| --- | --- | --- |
| Luxemburger Haushaltsvertrag | Unterzeichnung 22. April 1970, Inkrafttreten 1. Januar 1971. | Eigenmittel und zusätzliche parlamentarische Haushaltsrechte aushandeln und ratifizieren. |
| Werner-Bericht | Oktober 1970; schrittweise Wirtschafts- und Währungsunion als Ziel. | Wechselkurskoordination und später eine alternative erfolgreiche Währungsunion. |
| Davignon-Bericht | 27. Oktober 1970. | Europäische Politische Zusammenarbeit als regelmäßige Regierungskonsultation. |
| Norderweiterung | Historisch ENG, IRE, DEN ab Januar 1973. | Mitgliedschaft jedes Bewerbers abhängig von Verhandlungen und nationalem Ergebnis. |
| Europäischer Rat | Gründung 1974, erstes Treffen 1975. | Gipfel zunächst als gelegentliche Regierungskonferenz, später als dauerhafte Struktur. |
| Regionalfonds und Direktwahl | Regionalfonds 1975, erste EP-Direktwahl 1979. | Eigene spätere Reformen, bei anderem Vertragsverlauf auch vorziehbar. |

Quellen: [Haushaltsvertrag beim Europäischen Parlament](https://www.europarl.europa.eu/about-parliament/en/in-the-past/the-parliament-and-the-treaties/treaty-of-luxembourg), [EUR Lex zur Währungsintegration](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=legissum%3Al25007), [Davignon Originalbericht](https://aei.pitt.edu/4543/1/epc_first_report_oct_1970.pdf), [Entstehung des Europäischen Rates](https://www.consilium.europa.eu/en/50-years-of-working-together/), [EU Geschichte 1970 bis 1979](https://european-union.europa.eu/principles-countries-history/history-eu/1970-79_en).

EFTA braucht eine eigene wirtschaftspolitische Rolle. Am Jahresanfang gehören ENG, DEN, NRY, POR, AUS, SWE und SWI dazu; FIN ist assoziiert. ICE folgt am 1. März 1970. Freihandel ohne EG-Mitgliedschaft bietet diesen Ländern eine dauerhafte Alternative. Ein Beitritt zur EG ist damit politisch interessant und nicht die einzig sinnvolle Spielentscheidung. [EFTA Geschichte](https://www.efta.int/about-efta/european-free-trade-association/history), [Schweizer SECO zur ursprünglichen Freihandelsorganisation](https://www.seco.admin.ch/en/european-free-trade-association-efta), [Isländische Regierung zum Beitrittsdatum](https://www.stjornarradid.is/page/d2a7ee5d-2caa-43c7-954e-f2aa892cc57e/).

Griechenlands Assoziierung war nach dem Putsch politisch eingefroren; die Türkei befand sich im Assoziierungsprozess des Ankara-Abkommens. Beide sind 1970 keine Vollmitglieder. Assoziation, Handelsvorteile, Demokratisierung und Beitritt sollen deshalb eigene Zustände sein. [Griechisches Außenministerium](https://www.mfa.gr/brussels/en/permanent-representation-eu/greece-in-the-eu/greeces-course-in-the-eu.html), [EU Delegation zum Ankara Abkommen und seinen Phasen](https://www.eeas.europa.eu/delegations/t%C3%BCrkiye/customs-union-supporting-growth-eu-t%C3%BCrkiye-trade-0_en).

## Vorhandene MD Möglichkeiten und ihre Wiederverwendung

| Vorhandenes System | Tatsächliche Fähigkeiten | Verwendung ab 1970 |
| --- | --- | --- |
| Mitgliedschaft | `EU_member`, Mitgliederarray, Kandidatenflag, Austrittscleanup, Übernahme beschlossener Gesetze. | Als kanonischen EG-Mitgliedsstatus behalten; zusätzliche Assoziations- und Vertragsteilnahme getrennt speichern. |
| Politisches Mandat | `europeanism` mit nationaler Änderung, gemeinschaftlicher Änderung und laufender Entwicklung. | Öffentliches Integrationsvertrauen; materielle Interessen und bewusste Spielerentscheidung ergänzen. |
| Gesetzgebung | Antrag → Parlament → Rat, Warteschlangen, beschlossene IDs, Ja/Nein-Listen, Timer, AI-Gewichte. | Gemeinsame Verfahrensmaschine behalten, Anhörung und je Dossier passende Ratsregel einbauen. |
| Ämter und Oberfläche | Kommission, Rat, Parlament, Haushaltsansicht und dynamische Listen. | Historische Ämter und Zuständigkeiten einsetzen; moderne Ministerien erst durch neue Verträge freischalten. |
| Haushalt | BIP-abhängige Beiträge, vier Ausgabenkörbe, Nettozahlerwerte, Entwurf und Rollback, tatsächliche Staatseinnahmen und Ausgaben. | Landwirtschaft, Sozialfonds, Forschung und bewilligte Projekte finanzieren. Alte Verteilung nicht als historisch korrekt übernehmen. |
| Erweiterung | Kandidatengruppen und individuelle Aufnahmeentscheidung. | Als Antrag und Verhandlungsbeginn nutzen; Zustimmung der bestehenden Mitglieder und nationale Ratifikation hinzufügen. |
| POTEF | Gemeinsame Präsidentschaft, regionale Projekte, dynamische Boni; Staaten bestehen fort. | Grundlage für spätere vertraglich begrenzte politische Kooperation. Inhalte und Machtbefugnisse einzeln prüfen. |
| USoE | Vollständige staatliche Vereinigung, Truppen-, Technologie- und Finanzübertragung. | Separates alternatives Endspiel nach ausdrücklicher nationaler Teilnahme. |
| Sicherheit | EuroArmy, EuroNavy, gemeinsame Übungen und EDU-Fraktion. | Übungen und freiwillige Projekte zuerst; stehende Truppen und Bündniswechsel sind eigene Verträge. |

Codeeinstiege: [Mitgliedsidee](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/ideas/Organizations.txt:4>), [Europäismus](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:29>), [Abstimmungsergebnis](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/99_EU_voting_scripted_triggers.txt:16>), [Haushalt](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1312>), [politische Föderation EU112](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:875>), [gemeinsame Übungen](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:1351>).

## Zuerst zu behebende Codeprobleme

1. **Der Startzustand ist widersprüchlich.** Der Initializer trägt 15 moderne Tags in `global.EU_member` ein, vergibt dabei aber keine Mitgliedsidee. In den geprüften Gründerstaaten ist diese erst im Historyblock 2000 enthalten. Viele Funktionen prüfen dagegen die Idea. Der einzige allgemeine Array-Abgleich hängt am Ende eines Bürgerkriegs und kann die Geisterliste dann leeren. Ein eigener 1970-Initializer muss vor dem modernen Startup verzweigen und genau sechs konsistente Mitgliedschaften anlegen. [Initializer](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:691>), [15 Tags](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:760>), [einziger Resync-Aufruf](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/MD_on_actions.txt:611>).
2. **Moderne Inhalte laufen trotzdem an.** Dazu gehören Datenschutz-/Asyl-Strafideen, moderne Agenden und ein relativer EP-Wahltimer von 1625 Tagen. Der erzeugt ab 1970 einen Wahlaufruf um 1974. Eigene Agendenliste und Delegiertenmodus sind nötig. Der Euro ist dagegen bereits in Effekt und Idea vor 1999 gesperrt; eine alternative Frühwährung braucht neue Logik. [Startinhalte](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:776>), [Eurogate](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1829>).
3. **EU111 kann Nichtabstimmer annektieren.** Der Dispatcher umgeht den normalen Mehrheitstrigger. Anschließend werden ausdrückliche Ablehner entfernt und übrige Mitglieder vereinigt. Für MP muss daraus eine Liste ausdrücklich ratifizierender Teilnehmer werden. [Sonderfall](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:316>), [Annexionshandler](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:406>).
4. **Manuelle Ratsbuttons prüfen das Stimmrecht nicht vollständig.** Kandidaten können den Rat aufrufen; die Ja/Nein-Buttons verlangen weder Mitgliedsidee noch nicht suspendiertes Stimmrecht. Außerdem teilen Spieler globale Variablen für Parteidetailansichten. Berechtigungen zentral prüfen und Ansichtsdaten im jeweiligen Spielerland halten. Dies belegt noch keine OOS-Störung. [Ratsbuttons](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:1323>), [globale Parteiauswahl](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:1999>).
5. **Der Haushalt hängt an der EZB.** `ECB_president` finalisiert die bestehenden Budget- und MFF-Verhandlungen. Das Amt nur auszublenden würde den Abschluss verhindern. Zuständigkeit ändern; bei jedem Verteilungslauf alte Amtszuschüsse zurücksetzen. [Budgetabschluss](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:476>), [Zuschussverteilung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1484>).
6. **Sicherheitsmechaniken verändern Staaten und Bündnisse erheblich.** EDU entfernt NATO-Ideen und erstellt eine gemeinsame Fraktion; EuroNavy bündelt alle Technologien und bietet komplette Flottenübertragung. EuroArmy lädt eine 2000-OOB. Diese Effekte benötigen eigenständige Teilnahmeverfahren und zeitgerechte Einheiten. [EDU](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:1303>), [EuroNavy](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:1246>), [EuroArmy](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:1271>).
7. **Moderne Foki sind nicht automatisch aktive 1970-Foki.** FRA, GER, ENG und TUR laden den generischen 1970-Baum. Dieser bindet die USoE-/POTEF-Wurzeln nicht ein. Die großen EU-Pakete mit 90 beziehungsweise 74 Shared-Foki einfach umzuschreiben reicht deshalb nicht. Erste Inhalte besser über gemeinsame Entscheidungen und Ereignisse anbieten. [FRA-Zuweisung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/FRA - France.txt:8>), [Fallbackschutz](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/mdcw_1970_focus_tree_effects.txt:4>).

## Zehn konkrete Dossiers für historisches Roleplay

Die folgenden Abläufe und Zahlen für Verhandlungsdauer oder Spielboni sind Designvorschläge. Historische Ereignisse dienen als Anlass; der Spielstand und die beteiligten Regierungen bestimmen das Ergebnis.

### Norderweiterung mit echten Verhandlungen

ENG, IRE, DEN und NRY erhalten je einen Verhandlungsstatus. Ein Paket umfasst Haushaltsbeitrag, Agrarmarkt, Fischerei, Commonwealth-Handel und Übergangsfristen. Zugeständnisse erzeugen sichtbare Kosten und Vorteile. Ministerrat und nationale Ratifikationen schließen den Prozess ab; ein ablehnender Bewerber bleibt draußen, ohne automatisch die übrigen zu blockieren. Der bestehende `EU_apply_for_membership` darf erst am Ende die Mitgliedsidee vergeben. [Aufnahmeentscheidung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:1634>).

Für Norwegen ist ein anderes Referendumsergebnis eine naheliegende Alternative: Historisch lehnte die Bevölkerung 1972 den Beitritt ab. [Norwegische Regierung](https://www.regjeringen.no/no/om-regjeringa/tidligere-regjeringer-og-historie/sok-i-regjeringer-siden-1814/historiske-regjeringer/regjeringer/trygve-brattelis-forste-regjering-1971-1/id438723/). Ein späterer britischer Streit über Beiträge, Landwirtschaft und Souveränität kann die Neuverhandlung von 1974/75 aufgreifen. Ein früher britischer Austritt wäre dann eine Abweichung mit konkretem Anlass. [House of Commons Library](https://commonslibrary.parliament.uk/research-briefings/cbp-7253/).

### Landwirtschaft gegen gemeinsame Finanzierung

Die Mitgliedschaft enthält bereits die grundlegende Agrargemeinschaft. Spielbar werden Anpassungen der Preisstützung, Überschusskosten und Verteilung. Frankreich kann Agrargarantien verlangen, Deutschland Finanzierungsgrenzen, Italien stärkere Strukturhilfen und die Niederlande offenere Märkte. Das sind vorgeschlagene nationale Verhandlungsprofile, keine festgeschriebenen Spielerentscheidungen. Die vorhandenen Budgetkörbe liefern den Unterbau; Agrarauszahlungen brauchen einen eigenen Landwirtschaftsindex statt der heutigen BIP-pro-Kopf-Leiter. [Verteilung natürlicher Ausgaben](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1446>).

### Eigenmittel und Haushaltsrechte

Der Vertrag von 1970 bietet direkt eine erste große RP-Konferenz. Die Regierungen entscheiden über den Übergang von Beiträgen zu gemeinschaftlichen Einnahmen und parlamentarischen Haushaltsrechten. Im Spiel werden Zoll-/Agrarabschöpfungen zunächst transparent als vereinfachte Einnahmegrößen abgebildet. Die heutige BIP-Callrate ist ein brauchbarer Ersatz für die erste Fassung, muss aber als Abstraktion kenntlich bleiben. Keine historische Steuerstatistik oder branchengenaue Zollsimulation ist im bestehenden Budgetcode enthalten. Entwurf, Gegenentwurf und Rollback bestehen bereits. [Entwurfsspeicherung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1256>).

### Werner Plan und Währungsschlange

Zuerst nationale Währungen mit Wechselkurskoordination und begrenzten Stützungskrediten; anschließend gemeinsame Verrechnung und engere Bindung. Spekulativer Druck, nationale Ausgabenpolitik und externe Wirtschaftsschocks belasten den Verbund. Regierungen können abwerten, Geld zuschießen, austreten oder Kompetenzen übertragen. Eine erfolgreiche gemeinsame Währung bis etwa 1980 wäre die alternative Fortsetzung des Werner-Ziels. Die reale Währungsschlange begann 1972; der bestehende moderne Euro-/OMT-Code ist dafür nur technische Referenz. [EUR Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=legissum%3Al25007).

### Europäische Politische Zusammenarbeit

Gemeinsame Erklärungen zu Nahost, Entspannung, Anerkennungsfragen oder Hilfsprogrammen benötigen Zustimmung der beteiligten Regierungen. Erfolg kann diplomatisches Gewicht oder Vertragsvertrauen geben; Uneinigkeit bleibt ein spielbares Ergebnis. Der Davignon-Bericht sah zunächst Konsultation und Abstimmung der Außenpolitik vor. Ein europäischer Außenminister mit eigener Befehlsgewalt wäre eine zusätzliche alternative Reform. [Originalbericht Teil Zwei](https://aei.pitt.edu/4543/1/epc_first_report_oct_1970.pdf).

### Euratom und zivile Industrieprojekte

Bezahlte Gemeinschaftsprojekte fördern zivile Kernenergie, Materialforschung und Ausbildung. Teilnehmer leisten Beiträge und erhalten begrenzte, projektbezogene Forschungsboni. Rüstungskooperation kann daneben als eigener Vertrag bestehen. Das vollständige `inherit_technology`-Pooling der Marine wäre für Forschungszusammenarbeit viel zu weitreichend. Die variablengesteuerten POTEF-Modifikatoren können stattdessen gedeckelte Projektboni tragen. [POTEF Modifier](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/dynamic_modifiers/05_POTEF_dynamic_modifiers.txt:1>).

### Investitionsbank und regionale Entwicklung

Regierungen schlagen konkret benannte Infrastruktur-, Energie- und Industrievorhaben vor. Bewilligung bindet Mittel; nationale Kofinanzierung und Abschlussbedingungen verhindern kostenlose Dauerboni. Vor einem späteren Regionalfonds laufen solche Vorhaben über ein begrenztes Projektbudget. Das schafft Verhandlungsmacht für kleinere Staaten. Das bestehende `invest_in_EU_single_market_infra` ist ein Effekt zum Prüfen und Anpassen, keine fertige historische Investitionsbank. [Infrastruktureffekt](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:217>).

### EFTA als eigenständige Freihandelsoption

EFTA-Länder behalten nationale Außenhandelspolitik und können bilaterale Abkommen mit der EG schließen. Für Angebote, Annahme, Ablehnung und Kündigung existiert bereits `propose_improved_trade_agreement` als Muster. Dessen Effekte setzen Flags, Beziehungen, Einfluss und Zähler; eine Zollsimulation entsteht dadurch noch nicht. Neue EFTA-Teilnahme und Handelswirkungen sind erforderlich. Die moderne Agenda `EU609` erteilt nur Kandidatenflags an einige Länder und Kleinstaaten. Sie bildet weder die EFTA von 1970 noch einen echten EWR ab. [Bilaterales Angebot](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_diplomatic_actions/00_scripted_diplomatic_actions.txt:48>), [EU609](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:962>).

### Demokratisierung und Assoziationsbeziehungen im Süden

GRE startet mit eingefrorener politischer Annäherung. Der vorhandene griechische Pfad für Überwachung und Aufhebung europäischer Rüge kann eine Wiederaufnahme von Gesprächen erlauben. Danach folgen eigenständige Wirtschafts- und Aufnahmeverträge. SPR und POR erhalten vergleichbare Verhandlungsmöglichkeiten abhängig von ihrem tatsächlichen politischen Verlauf. TUR erhält sektorale Assoziationsschritte. Für CYP bleiben Zustimmung der Konfliktparteien und das eigene 1970-System maßgeblich: Der alte `POTEF452` annektiert NCY unmittelbar und darf den bestehenden Konflikt nicht umgehen. [Griechischer Anknüpfungspunkt](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt:15045>), [moderner Zypernfokus](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/02_EU_POTEF_shared.txt:4797>).

### Ölkrise und gemeinsame Versorgung

Wenn Krieg, Embargo oder Versorgungsprobleme im Spiel eintreten, entscheiden Länder zwischen nationalen Lieferverträgen, gemeinsamer Beschaffung, Einsparungen und Energieinvestitionen. Unterschiedliche Energieabhängigkeit erzeugt Interessenkonflikte. Ein Solidaritätsfonds kann politisch scheitern oder tiefere Kooperation begründen. Der reale Schock von 1973 liefert das historische Motiv; in RP sollte eine abweichende Nahostentwicklung auch die europäische Krise verändern. [EU Geschichte zur Ölkrise](https://european-union.europa.eu/principles-countries-history/history-eu/1970-79_en).

## Alternative europäische Ordnungen

Diese Optionen sind neue Spielentwürfe. Sie sollen dauerhafte, gegeneinander abwägbare Ordnungen bilden. Höhere Integration bringt gemeinsame Möglichkeiten und verlangt Beiträge, innenpolitisches Mandat oder die Abgabe von Zuständigkeiten.

| Alternative | Konkreter Auslöser und Verlauf | Vorhandener technischer Ansatz |
| --- | --- | --- |
| Europa der Staaten | Regierungen stärken Konsultation und Einstimmigkeit, begrenzen zentrale Ämter und behalten nationale Wirtschaftssteuerung. | Antragsmaschine und ländererhaltende POTEF-Struktur; Kompetenzregeln neu schreiben. |
| Erfolgreicher Werner Plan | Länder finanzieren Stützung und stimmen der schrittweisen Übertragung von Währungskompetenzen zu. | Geldsystem, Ideen und Vertragsflags; neue Vor-Euro-Logik nötig. |
| Britisch geprägtes Freihandelseuropa | ENG verzichtet auf EG-Beitritt oder scheidet später aus und baut EFTA-Handel sowie sektorale Partnerschaften aus. | Bilaterale Vertragsangebote; separate EFTA-Mitgliedschaft neu entwickeln. |
| NORDEK gelingt | FIN, SWE, DEN und NRY lösen Neutralitäts-, Handels- und Landwirtschaftskonflikte und ratifizieren die nordische Wirtschaftsunion. | Neue regionale Vertragsparteien auf derselben Entscheidungsarchitektur. EG-, NATO- und Neutralitätsfragen getrennt verhandeln. |
| Politische Union mit nationalen Regierungen | Eine freiwillige Gruppe ratifiziert gemeinsame Kompetenzen, Haushalt und Präsidentschaft. Andere EG-Staaten bleiben beim bisherigen Vertrag. | EU112/POTEF als Strukturvorlage; Teilnehmerarray und Opt-outs ergänzen. |
| Eigenständige Sicherheitsunion | Freiwillige Beschaffung und Manöver führen eventuell zu einem eigenen Verteidigungsvertrag und bewusstem Wechsel aus bisherigen Bündnissen. | Manöver wiederverwenden; EDU erst als ausdrücklich alternatives Bündnis einsetzen. USA und UdSSR erhalten eigene Reaktionsentscheidungen. |
| Europäischer Bundesstaat | Nur ausdrücklich ratifizierende Staaten vereinigen sich; die übrigen Spieler behalten ihre Länder und Vertragsbeziehungen. | EU111/USoE-Transfercode nach vollständigem Ersatz seines Zustimmungsverfahrens. |
| Sozialistische oder blockübergreifende Kooperation | Nationaler politischer Wandel und Entspannung eröffnen sektorale Handels- und Forschungsabkommen. Vollmitgliedschaft verlangt einen gesonderten Vertrag. | Ideen, Projekte und Annahmeereignisse; heutige pauschale Ideologie-Verstoßpunkte ersetzen. |

NORDEK ist besonders passend zum Startjahr: Der Plan wurde im Februar 1970 behandelt, scheiterte aber an Finnlands Nicht-Ratifikation im März und der Spannung zwischen sowjetischen Beziehungen und möglichem EWG-Beitritt anderer Partner. Damit gibt es einen realen frühen Entscheidungspunkt für alternatives RP. [Nordischer Rat](https://www.norden.org/en/information/history-nordic-council). Die anderen Alternativen sind hier vorgeschlagene Kombinationen der geprüften Mechaniken, keine Behauptung eines historisch beschlossenen Gesamtplans.

## Technischer Aufbau für die Umsetzung

Die folgenden `CWEC_*`-Bezeichner sind vorgeschlagene neue Namen. Die unterschiedlichen Präfixe in den drei Agentenberichten bezeichnen Entwürfe und sollten bei der Implementierung vereinheitlicht werden.

1. **Szenarioinitialisierung.** Im bestehenden Startup vor `on_startup_euu_action` anhand des vorhandenen `IMP_is_1970_scenario` verzweigen. `CWEC_initialize_1970` setzt Mitgliedschaften, Startverträge, 142 Delegierte, Ratssitze, Haushaltszuständigkeit und passende Agenden einmalig. Bereits ausgelöste moderne Eventketten erst hinterher aufzuräumen wäre fehleranfälliger. [Szenariotrigger](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/IMP_cold_war_scenario_triggers.txt:1>).
2. **Ein Mitgliedsstatus mit mehreren Vertragsebenen.** `EU_member` und `global.EU_member` als kanonischen Vollmitgliedsstatus behalten und seine Boni für 1970 anpassen. Assoziation, EFTA, Währungs-, Forschungs- und Verteidigungsteilnahme bekommen eigene Länderflags oder Teilnehmerarrays. Keine zweite widersprüchliche EG-Mitgliedsliste anlegen.
3. **Berechtigte Wähler und Verfahren.** `CWEC_can_cast_council_vote`, `CWEC_active_procedure`, nationale `CWEC_council_weight` und eine eingefrorene Wählerliste ergänzen. Anzeige und Ergebnistrigger benutzen dieselbe Neuberechnung. Enthaltung, Nein und noch keine Stimme sind eigene Zustände. Beitritt und Staatsvereinigung benötigen zusätzliche nationale Ratifikationen.
4. **Unabhängige Reformachsen.** Etwa `CWEC_direct_elections`, `CWEC_EPC`, `CWEC_budget_reform_1970`, `CWEC_monetary_stage` und `CWEC_defence_treaty`. So kann ein Land währungspolitisch kooperieren, ohne automatisch gemeinsame Truppen oder eine Föderation zu akzeptieren. Keine universelle Integrationsstufe soll alle Bereiche zugleich einschalten.
5. **Dossiers registrieren.** Für jedes neue Dossier Verfahrensart, Antragsteller, betroffene Parteien, Laufzeit, AI-Interessen, Kosten, Ergebnis und Aufräumlogik zusammen definieren. Bestehende numerische Agenden werden in GUI, Lokalisierung, AI und Ergebnisdispatcher an mehreren Stellen behandelt; nur eine neue ID ins Array einzutragen reicht nicht.
6. **Projektfinanzierung begrenzen.** Bei jeder Neuberechnung alte Zuschüsse nullen; zugesagte Mittel, Einzahlungen und Auszahlungen getrennt buchen. Gemeinschaftsverwaltung und Projektbudgets sollen nicht allein wegen eines Amtsbesitzes als frei verfügbare nationale Einnahmen entstehen. Jahresbudget zuerst; ein Mehrjahresrahmen ist eine gesonderte Vertragsentscheidung.
7. **Aktive Inhalte anbinden.** Neue gemeinsame Entscheidungen und Ereignisse zuerst. Spätere Shared-Foki im tatsächlich aktiven generischen oder nationalen 1970-Baum einbinden. Keine wiederholten Baumwechsel, die bestehenden Länderfortschritt überschreiben. GRE, CYP und andere eigene 1970-Systeme über gezielte Hooks verbinden.
8. **Ausschließlich Menschen stimmen ab.** Für Rat, Parlament, Haushalt, Ratifikation und Ämterwahl zählt der ausdrücklich festgelegte menschliche Wählerkreis. KI-Staaten werden administrativ und finanziell berücksichtigt, geben aber keine automatischen Stimmen ab. Disconnect oder Timeout bewirkt keine Ratifikation, keinen Flottentransfer und keine staatliche Vereinigung.

## Empfohlene Reihenfolge

| Paket | Umfang | Fertig, wenn |
| --- | --- | --- |
| 1 Historischer Grundzustand | Eigener Startup, sechs Mitglieder, richtige Oberfläche und Ratsregeln, Delegiertenparlament, moderne Inhalte sperren, Haushalt ohne EZB, MP-Stimmrechte. | Tag 1, Monatswechsel, Bürgerkriegsende und Speichern/Laden erhalten denselben konsistenten Grundzustand. |
| 2 Erste RP Runde | Norderweiterung, Agrar-/Eigenmittelpaket, rotierender Vorsitz, Assoziation und gemeinsame Stellungnahmen. | Spieler können Verträge aushandeln, ablehnen und ratifizieren; Zahlungen und Rechte entsprechen dem Ergebnis. |
| 3 Krisen und Konkurrenz | Werner/Währungsschlange, EFTA/NORDEK, Energiekrise, Forschungs- und Infrastrukturprojekte. | Teilnahme, Kosten, Austritt und gescheiterte Projekte werden sauber abgewickelt. |
| 4 Alternative Ordnungen | Europa der Staaten, politische Union, eigene Sicherheitsunion, optional Bundesstaat. | Nur explizite Teilnehmer übertragen die jeweils beschlossenen Kompetenzen; übrige Spieler bleiben eigenständig. |

Die erste spielbare Fassung sollte Paket 1 und 2 abdecken. Das bietet bereits fortlaufende Diplomatie für große und kleine Staaten. Währung, Sicherheit und Bundesstaat können anschließend auf dieser Vertragslogik aufbauen.

Bei der späteren Abnahme besonders prüfen: parallele Spieleransichten, Stimmenwechsel, Kandidaten ohne Stimmrecht, exakt 12 gewichtete Ja-Stimmen, Vierstaatenbedingung, nationale Ablehnung, Amtswechsel ohne doppelte Zuschüsse, Beitritt ohne NATO-Wechsel, Zypern ohne fremden Sofortfokus und laufende Ratifikation über Speichern/Laden. Das sind vorgeschlagene Integrationsprüfungen; diese Recherche enthält keine Laufzeitfreigabe.
