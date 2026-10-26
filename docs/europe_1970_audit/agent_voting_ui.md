> **Archived CWEC material.** The custom system was removed on 18 October 2026. [Native MD restoration status](native_restore.md) supersedes the implementation claims below.

# Agentenprüfung Abstimmungen Parlament und Oberfläche für Europa 1970

Stand: 18. Oktober 2026. Ausschließlich statische Prüfung des lokalen Modcodes; keine Gameplay-Dateien geändert, kein Spiel-/Mehrspielertest ausgeführt. Historische Zielwerte unten wurden vom Hauptagenten anhand des Originalvertrags verifiziert. Neue Bezeichner sind ausdrücklich Designvorschläge und existieren noch nicht im Code.

## Ergebnis

Die vorhandene MD-Oberfläche und ihre Antragslisten sind eine gute technische Grundlage. Die Entscheidungslogik bildet aber ein modernes, stark vereinfachtes EU-System ab. Für 1970 sollte daraus ein System der Europäischen Gemeinschaften mit Kommissionsvorlage, beratendem Parlament, gewichtetem Ministerrat und nationaler Ratifikation werden. Bloßes Umbenennen würde moderne Zuständigkeiten und Mehrheiten unverändert lassen.

Für Multiplayer ist besonders wichtig: Mitgliedschaft, Stimmrecht, Antragstellung, staatliche Zustimmung und tatsächlicher Beitritt zu einer Föderation brauchen voneinander getrennte Prüfungen. Der bestehende Vereinigungsbeschluss `111` kann bei Ablauf Mitglieder einschließlich Nichtabstimmern annektieren.

## Belegstellen im vorhandenen Code

| Bereich | Tatsächliche Implementierung | Beleg |
| --- | --- | --- |
| Antragswarteschlange | Ein globaler EP-Antrag `global.current_active_agenda_disp`, danach `global.EU_council_votes`, danach ein globaler Ratsantrag `global.current_active_vote_disp`; beschlossene IDs stehen in `global.EU_passed_votes`. | [EP-Abschluss](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:1091>), [Rat starten](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:4382>), [Rat aufräumen](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:1154>) |
| Reihenfolge | Der Vorschlag geht zuerst ins Parlament. Erst dessen Zustimmung schiebt ihn auf die Ratsliste. | [Antrag einreichen](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:4989>), [Weiterleitung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:1114>) |
| EP-Zeitfenster | 14 Tage. Frühzeitige Annahme über Spielerknopf möglich; bei Timeout vergleicht der Kommissionspräsident beziehungsweise Caretaker aktive Unterstützung mit der Mehrheit. | [EP-Mission](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:22>), [Annahmeknopf](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:1219>) |
| Ratszeitfenster | 14 Tage; alle Mitglieder erhalten die Mission. Die Auswertung läuft beim Kommissionspräsidenten oder genau einem Caretaker. | [Ratsmission](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:383>) |
| Ratsmehrheit | Strikt `global.EU_pop_ratio_yes > 0.65` UND Ja-Staaten/alle Mitglieder `> 0.55`. Keine gewichteten Vertragsstimmen, keine allgemeine Einstimmigkeit und keine Sperrminorität aus vier Staaten in diesem Trigger. | [`EU_voting_decision_result_trigger`](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/99_EU_voting_scripted_triggers.txt:16>) |
| Anzeige der Mehrheit | Die Oberfläche berechnet `round(Mitglieder * 0.55)` als Anzeigegröße. Tatsächlicher Ergebnistrigger benutzt den ungerundeten Anteil und striktes `>`. Anzeige und Auswertung sind getrennte Berechnungen. | [`EU_update_vars`](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:90>), [Tooltip](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/localisation/english/MD_focus_EU_l_english.yml:316>) |
| EP-Sitze | `election_EU_Parliament`: Zielgröße 732 ohne Lissabon, 750 mit Lissabon, 1000 mit erweitertem Rahmen. Nationale Sitze werden aus Bevölkerungsanteil berechnet und gekappt; Rundungen können die Zielgröße verändern. | [Sitzregeln](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1582>), [nationale Verteilung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1677>) |
| EP-Parteien | 24 nationale Subideologien; `party_pop_array` bestimmt die Sitzverteilung. `MEP_Majority = MEP_Total * 0.5 + 1`. Keine eigene europäische Wahlpräferenz oder historische Delegationsbestellung. | [Parteisitze](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1693>), [Mehrheit](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1673>) |
| EP-Unterstützung | Die Subideologie der antragstellenden Regierung unterstützt mit sämtlichen entsprechenden EP-Sitzen aller Länder. Andere ganze Subideologieblöcke lassen sich für zwei politische Macht pro Sitz gewinnen. | [`set_ruling_party_PG_support`](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1769>), [Einflussknopf](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:2025>) |
| Wahlkalender | Initialisierung löst eine Wahl sofort und die nächste nach 1625 Tagen aus; danach 1825 Tage Zyklus. Der Code kommentiert dies ausdrücklich als Wahltermin Juni 2004 ab Start 2000. Bei unveränderter Anwendung auf 1970 entsteht der erste Folgetermin circa 1974. | [Initialisierung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:794>), [Wahlereignis](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/events/EU_events.txt:481>), [1825-Tage-Mission](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:2>) |
| Antragshürden | Ratsantrag benötigt Amt, Einfluss auf andere Mitglieder oder mehr als 500 politische Macht. Es muss ein Kommissionspräsident existieren, außer bei weniger als zwei Mitgliedern. | [Ratsantrag erlauben](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:4257>) |
| Sperrfristen | Bestehende Spielregelpfade setzen 1/60/90/120/180/210 Tage; AI erhält teils zusätzlich 14 Tage. Dies lässt sich für verhandelbare Sitzungsrhythmen nutzen. | [Parlament](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:881>), [Rat](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:958>) |
| AI-Stimmen | Eine deterministische Summe aus Regierungsfamilie, Antragsgewichten, Europäismus, Einfluss, Fremdeinfluss, Untertanstatus und Schwierigkeitsgrad entscheidet über Ja/Nein. Positive Summe stimmt zu; es gibt keinen allgemeinen AI-Enthaltungspfad. | [allgemeine Wertung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:5>), [Gewichtstabelle](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:170>), [Auswertung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:255>) |
| Oberfläche | Bereits vorhanden: Ämter, Parlament, Rat, Haushalt, Europäismus; dynamische Mitglieds-, Unterstützer-, Gegner- und Gesetzeslisten. Aktualisierung über `global.EU_dirty_update_var`. | [Scripted GUI](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:39>), [Fenster und Navigation](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/interface/eu.gui:21>) |

## Historisches Zielmodell 1970

Der Originalvertrag liefert direkt umsetzbare Zahlen: Art. 138 nennt nationale parlamentarische Delegationen mit 142 Sitzen; Art. 146 einen sechsmonatigen Ratsvorsitz; Art. 148 gewichtete Ratsstimmen. Vertragsänderungen und Beitritte bedürfen nationaler Ratifikation nach Art. 236/237. Quelle: [EWG-Vertrag, amtlicher Text bei WIPO](https://www.wipo.int/wipolex/en/text/473854). Die Umsetzungsregeln müssen danach von späteren Reformen getrennt werden.

| Staat | Delegierte | Ratsstimmen |
| --- | ---: | ---: |
| Belgien | 14 | 2 |
| Bundesrepublik Deutschland | 36 | 4 |
| Frankreich | 36 | 4 |
| Italien | 36 | 4 |
| Luxemburg | 6 | 1 |
| Niederlande | 14 | 2 |
| Gesamt | 142 | 17 |

Qualifizierte Mehrheit: mindestens 12 von 17 Stimmen bei Kommissionsvorlage; sonst mindestens 12 Stimmen aus mindestens vier Mitgliedstaaten. Bei vertragsrechtlicher Einstimmigkeit verhindern Enthaltungen anwesender beziehungsweise vertretener Mitglieder die Annahme nicht. Unbeantwortete Spielerentscheidungen sollten deshalb technisch als „noch keine Stimme“ geführt und nicht stillschweigend in juristische Enthaltungen verwandelt werden. [EWG-Vertrag, Art. 148](https://www.wipo.int/wipolex/en/text/473854).

Der Luxemburger Kompromiss eignet sich für einen politischen Krisen- und Wiederverhandlungsmechanismus bei geltend gemachtem vitalem Interesse. Er sollte als eigene politische Praxis modelliert werden; eine Umwandlung jedes Sachbeschlusses in ein absolutes rechtliches Einzelveto wäre eine zusätzliche Spielregel. Quellen: [Ratsgeschichte](https://www.consilium.europa.eu/en/history/), [offizielle historische Darstellung des Rates](https://www.consilium.europa.eu/media/30558/qc3112311en.pdf).

## Konkrete Umsetzungsvorschläge

### Gemeinsame Abstimmungsmaschine behalten Verfahrensart ergänzen

Neue vorgeschlagene Variablen: `global.CWEC_active_procedure` mit `1 = einfache Mehrheit`, `2 = gewichtete QMV auf Kommissionsvorlage`, `3 = gewichtete QMV ohne Kommissionsvorlage`, `4 = Einstimmigkeit`, `5 = nationale Ratifikation`; dazu `CWEC_council_weight` im jeweiligen Land, `global.CWEC_yes_weight` und `global.CWEC_yes_states`.

Den bestehenden Ergebnis-Hook `EU_voting_decision_result_trigger` durch einen Verfahren-Dispatcher ersetzen beziehungsweise dort auf einen neuen Trigger `CWEC_current_proposal_passes` verzweigen. Die IDs und Warteschlangen können zunächst bestehen bleiben. Für neue 1970er Dossiers neue, reservierte numerische IDs festlegen und alle dazugehörigen Anzeige-, AI- und Ergebnishooks gemeinsam registrieren. Keine bestehende moderne ID kommentarlos mit anderem Inhalt neu belegen.

Beim Stimmenwechsel die Summen aus den aktuellen gültigen Stimmen neu berechnen; nicht allein inkrementell Bevölkerung addieren/subtrahieren. `CWEC_recalculate_council_tally` soll dieselbe Berechnung für Anzeige und Ergebnis benutzen. Die ursprüngliche Bevölkerungsspalte bleibt informativ oder wird erst durch eine spätere Vertragsreform rechtlich relevant.

### Parlament 1970 als Delegiertenversammlung

In `election_EU_Parliament_in_member_state` für das Anfangsregime feste Delegationssitze aus einer nationalen Variable `CWEC_assembly_seats` verwenden. Die bestehende 24er-Parteiarray-Struktur kann vorerst als interne Repräsentation erhalten bleiben. Sitzbestellung aus nationalen parlamentarischen Kräfteverhältnissen ableiten und nach nationalen Wahlen, Aufnahme neuer Mitglieder sowie einer Verfahrensreform neu berechnen.

Den Fünfjahres-EP-Wahlzyklus erst nach einer Direktwahlreform freischalten. Die 1625-Tage-Initialisierung entfernen beziehungsweise durch eine datierte Einführung ersetzen. „Direktwahl bereits früher“ ist dann eine klar sichtbare alternative Reform, nicht der versteckte Standard.

Die EP-Stufe des bestehenden Ablaufs zunächst als Anhörung/Stellungnahme nutzen. Positive Stellungnahme kann politische Kosten senken oder Legitimität geben; negative Stellungnahme erhöht die Verhandlungskosten. Gewöhnliche Rechtsakte sollen 1970 nicht automatisch am heutigen allgemeinen EP-Zustimmungstor scheitern. Haushaltsrechte als eigenen Verfahrenszweig und spätere Vertragsreformen getrennt behandeln. Das ist eine bewusste Verfahrensänderung am heutigen `EU_finalize_passed_agenda`, keine Lokalisierungsänderung.

### Ratsvorsitz und tatsächliche Institutionen im UI trennen

Den Rat-Tab „Ministerrat“ beziehungsweise „Rat der Europäischen Gemeinschaften“ nennen. Der bestehende Code mischt „European Council“ und „Council of the European Union“; moderne Tooltips behaupten unter anderem 27 Staats-/Regierungschefs. [Betroffener Tooltip](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/localisation/english/MD_focus_EU_l_english.yml:101>).

Eine neue Variable `global.CWEC_council_presidency` und einen sechsmonatigen Rotationstimer ergänzen. Ratsvorsitz sollte Tagesordnung und Vermittlung beeinflussen, nicht als persönliches fünfjähriges Bonusamt funktionieren. Kommissionspräsident als Person und das spielergesteuerte Land als politischer Träger sollten im Text erkennbar getrennt sein. Den modernen ständigen Präsidenten des Europäischen Rates nur nach institutioneller Reform zeigen.

In `interface/eu.gui` vorhandene Listen und Buttons wiederverwenden; zusätzlich Verfahrensart, benötigte/erreichte Stimmen, Frist, fehlende Stimmen, gültige Vetos und nationale Ratifikationen anzeigen. Farben und ausgeblendete Felder allein reichen nicht: Der Hovertext muss konkret erläutern, warum ein Dossier blockiert ist.

### Luxemburger Kompromiss als RP Spielzug

Vorgeschlagene Entscheidung `CWEC_invoke_vital_interest` nur während gewichteter Sachabstimmungen: politisches Kapital bezahlen, Gegenstand benennen, 30 bis 60 Tage Vermittlung auslösen, Anwendung des Beschlusses vorläufig aussetzen. Nach Verhandlung Auswahl „Kompromisspaket“, „Interesse zurückziehen“ oder „institutionelle Krise“. Die genaue Frist ist MP-Balancing, keine historische Zahl.

Damit entstehen konkrete RP-Anlässe: französische Agrarinteressen gegen gemeinsame Finanzierung, niederländische Offenheit gegen Protektionismus, italienische Regionalförderung gegen Haushaltsdisziplin. Statt nur Europäismus zu würfeln, soll die AI auf die materiellen Dossierkosten und angebotenen Zugeständnisse reagieren. Für Spieler bleibt die Entscheidung frei.

### Vertrag und Föderation nur durch bewusste nationale Teilnahme

Neue separate Zustände `CWEC_treaty_signed`, `CWEC_treaty_ratified`, `CWEC_federal_opt_in`; ausdrücklich nicht aus Rats-Ja oder aus unterlassener Ablehnung ableiten. Vertragsänderungen und Beitritt erhalten den Ratifikationszweig, bevor Mitgliedschaft und Rechtswirkungen wechseln. Eine verstärkte Zusammenarbeit kann für eine willige Untergruppe starten, sofern dies als alternatives neues Vertragsmodell beschlossen wurde.

Den Sonderpfad `111` vor einer MP-Version ersetzen: erst explizite Opt-ins sammeln, dann demokratische oder nationale Verfahren abarbeiten, erst danach gewünschte Teilnehmer zusammenführen. Für RP ist die vorhandene Föderationsstruktur mit weiterhin spielbaren Staaten oft geeigneter als unmittelbare Annexion; die konkrete Auswahl prüfen die anderen Agenten.

### Verhandelbare AI statt pauschaler Integrationsschalter

Die vorhandenen Tabellen `global.EU_vote_w1` bis `w6` und `global.EU_vote_hist` sind brauchbare Erweiterungspunkte. Pro Dossier Gewicht nach sektoraler Betroffenheit, Nettozahlung, Landwirtschaft, Außenhandel, Bündnispolitik und nationalem Regierungsprogramm addieren. `europeanism` als politisches Integrationsvertrauen behalten, aber nicht alle Fragen zu einer einzigen Integrationsskala reduzieren.

`EUU_all_nations_vote_yes` und Schwierigkeitsboni nicht zur historischen Hauptlogik machen. Die bestehende AI stimmt am Anfang des Ratsvotums anhand einer Gewichtssumme ab; spätere Ereignisse oder Konzessionen ändern diese Stimme ohne zusätzliche Neubewertung nicht automatisch. Eine neue `CWEC_reassess_ai_vote` nach konkreter Vertragsänderung oder Kompromissangebot erlaubt nachvollziehbare Bewegung. Menschliche Stimmen nie durch denselben AI-Pfad verändern.

## MP Risiken und Korrekturen vor Einführung

| Priorität | Befund und Folge | Korrekturvorschlag |
| --- | --- | --- |
| Hoch | `apply_EU_QMV_result` behandelt Dossier `111` ohne normalen Mehrheitstrigger. Der Handler entfernt explizite Nein-Staaten aus der Mitgliedschaft und annektiert den Rest. Nichtabstimmer werden dabei als verbleibende Mitglieder mit erfasst. [Dispatcher](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:316>), [Handler](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:406>), [Annexion](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:461>). | Opt-in und Ratifikation, keine Wirkung aus Nichtabstimmung. |
| Hoch | Kandidaten dürfen den Rat-Tab öffnen. Die Ja/Nein-Buttons prüfen nur laufenden Beschluss und bisherige Seite, weder `EU_member` noch Suspendierung. Das ergibt im statischen Codepfad Stimmzugriff für Kandidaten und suspendierte Mitglieder. [Navigation](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:113>), [Buttons](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:1323>). AI-Stimmen schließen Suspendierte dagegen ausdrücklich aus. [AI-Schleife](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:4424>). | Zentraler Trigger `CWEC_can_cast_council_vote` in allen Buttons, Events und AI-Effekten; bei Auswertung nur berechtigte Staaten zählen. |
| Mittel | Der Nenner der heutigen QMV ist die gesamte `EU_member`-Anzahl; Suspendierte bleiben Mitglieder. Der Trigger filtert sie nicht heraus. | Wählerliste beim Start festlegen; Quorum aus der für das jeweilige Verfahren gültigen Grundgesamtheit bilden. |
| Mittel | Bei Parteidetailansichten sind `global.EU_selected_party`, `global.EU_MEP_members_current` und Hilfswerte im Mitgliedsland global beziehungsweise gemeinsam. Zwei Spieler können gegenseitig die ausgewählte Partei und gelisteten Daten verändern. [Auswahlknöpfe](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:1999>), [Liste aufbauen](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1747>). | Reine Ansichtsdaten in Spielerland-Scope halten; dynamische Liste an das betrachtende Land binden, keine geteilten Auswahlvariablen. |
| Mittel | AI-Stimmen werden unmittelbar beim Start ermittelt; manuelle Stimmen können später wechseln. Die Summen werden inkrementell gespeichert. Austritt, Annexion, Mitgliedschaft oder Bevölkerungsänderung während der Frist müssen konsistent behandelt werden. [Start](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:4382>), [Stimmenwechsel](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:2638>). | Fixierte berechtigte Wählerliste und daraus bei jedem Abschluss neu berechnete Summen; explizite Regel für Staaten, die während der Abstimmung wegfallen. |
| Mittel | Umstimmen eines AI-Lands prüft politische Macht anhand `200 * Bevölkerungsanteil * 25`, zieht anschließend anhand `300 * Anteil * 25` mit anderer Kappung ab. Der angezeigte beziehungsweise geprüfte Aufwand kann vom tatsächlichen Aufwand abweichen. [Prüfung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:4357>), [Abbuchung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:4453>). | Eine gemeinsame Kostenberechnung für Freigabe, Tooltip und Effekt verwenden. Keine automatische Umstimmung menschlicher Staaten. |
| Mittel | Werte-Sanktionen sind keine Ratsabstimmung: Kommissionspräsident oder Einflussbedingungen gewähren direkt die Autorität; je 100 politische Macht. Die Schwellen liegen über drei beziehungsweise vier „breaches“. [Breach-Entscheidung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:127>), [Suspendierung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:209>), [Autoritätstrigger](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/99_EU_scripted_triggers.txt:388>). | 1970 zunächst ausblenden; Vertragsverletzung, politische Ächtung und spätere förmliche Sanktionsregeln getrennt freischalten. |
| Niedrig | `MEP_Majority = Total * 0.5 + 1` ist für gerade Gesamtzahlen passend, bei ungeraden Zahlen kann der Bruchwert eine Stimme mehr als eine einfache absolute Mehrheit verlangen. | Ganzzahlig `floor(Total / 2) + 1` berechnen. Mit 142 Startdelegierten tritt der Fall zunächst nicht auf. |

Die genannten GUI- und Mehrheitsbefunde sind Codebefunde. Eine tatsächliche OOS-/Desynchronisationsstörung wurde nicht beobachtet und wird hier nicht behauptet. Gemeinsame globale Ansichtsdaten können bereits ohne OOS störend sein.

## Sinnvolle Abnahmeszenarien nach einer späteren Umsetzung

1. Sechs Gründungsstaaten: FRA+GER+ITA erreichen 12 Stimmen und können eine Kommissionsvorlage annehmen; eine sonstige Vorlage mit denselben drei Ländern scheitert am zusätzlichen Vierstaatenerfordernis.
2. Einstimmigkeit: fünf Ja, eine bewusste Enthaltung ist zulässig; ein ausdrückliches Nein blockiert; eine noch unbeantwortete Stimme wird sichtbar und entsprechend der festgelegten Sitzungspolitik behandelt.
3. Kandidat und suspendierter Staat können keine Stimmen abgeben; Zustimmung, Ablehnung und Seitenwechsel ändern die Summe genau einmal.
4. Ein Spieler öffnet die sozialistische Delegationsansicht, ein anderer die liberale; beide behalten ihre Auswahl.
5. Föderationsvertrag mit zwei Opt-ins und vier Nichtteilnehmern erfasst nur die beiden ausdrücklich ratifizierenden Staaten; Timeout oder Disconnect erzeugt kein Opt-in.
6. Kommissionspräsidentschaft vakant, Mitglied tritt während laufendem Dossier aus, Ratifikationsfrist läuft aus: genau ein Abschluss, keine doppelte Anwendung, keine steckengebliebene Mission.
7. 1970er Start lädt 142 Delegierte und keine EP-Direktwahl 1974; eine freigeschaltete alternative Direktwahlreform startet erst ihren eigenen Wahlkalender.
