> **Archived CWEC material.** The custom system was removed on 18 October 2026. [Native MD restoration status](native_restore.md) supersedes the implementation claims below.

# Technischer Einbauplan für Europa 1970

Das EG-System wird als 1970-Verfahrensschicht an die vorhandenen MD-Schnittstellen angeschlossen. Bestehende Mitgliedsidee, Mitgliederarray, Finanzbuchung und Oberfläche bleiben die Verbindung zum restlichen Spiel. Neue Skripte regeln Verträge, Kompetenzen und historische Verfahren. Der Einbau erfolgt über ausdrückliche Verzweigungen in den bestehenden Funktionen; gleichnamige Effekte in zusätzlichen Dateien zu definieren und auf eine Lade-Reihenfolge zu hoffen, wäre keine belastbare Integration.

Dieser Plan konkretisiert die Recherche vom 18. Oktober 2026. Alle `CWEC_*`-Namen und genannten neuen Dateien sind Vorschläge. Es wurden keine Laufzeitdateien geändert. Historische Grundlage und Agentenberichte stehen im [Gesamtkonzept](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/docs/europe_1970_audit/europa_1970_konzept.md>).

Verbindliche Nutzervorgabe: Sämtliche neuen Ingame-Texte erscheinen ausschließlich auf Englisch in `l_english`-Lokalisierung. Das betrifft Entscheidungen, Ereignisse, Ideen, Oberflächen, Statusanzeigen und Tooltips. Keine neuen deutschen Lokalisierungsdateien. Die deutschsprachigen Konzeptdateien sind Entwicklungsunterlagen.

Verbindliche MP-Vorgabe nach ausdrücklicher Nutzerklärung: Alle politischen Abstimmungen einschließlich Rat, Parlament, Haushalt, Erweiterung, Vertragsratifikation und Ämterwahl werden ausschließlich durch menschliche Spieler entschieden. KI-Länder können institutionelle Mitglieder und finanzielle Teilnehmer bleiben, erhalten aber keine Stimme, kein automatisches Ja und kein automatisches Veto. Die frühere Idee eines historischen AI-Abstimmungsmodus wird damit ersetzt. Historische Verfahrenszahlen bleiben Referenzen; die darauf aufbauenden Regeln für einen reinen Spielerkreis sind ausdrücklich MP-Anpassungen.

## Verbindliche Schnittstellen

| Bestehender Zustand | Bedeutung nach dem Umbau | Regel |
| --- | --- | --- |
| Idea `EU_member` | Vollmitglied der Europäischen Gemeinschaften | Bleibt der Mitgliedschaftstest für Collections, Geldsystem und andere MD-Mechaniken. Angezeigter Name und Effekte werden für 1970 angepasst. |
| `global.EU_member` | Abgeleitete Liste aller Vollmitglieder | Nicht unabhängig von der Idea verwalten. Ein- und Austritt über gemeinsame Effekte; Konsistenzabgleich berücksichtigt Bürgerkrieg und Annexion. |
| `global.EU_potential` | Für die Europafunktionen technisch erfasste Länder | Bedeutet weder Kandidatur noch Beitrittsrecht. Zugriff zusätzlich nach Existenz, Status und Dossier prüfen. |
| `EU_candidate` | Anerkannter Bewerber | Erlaubt Verhandlungen, aber keine Ratsstimme und keine eigenmächtige Aufnahme. |
| `europeanism` | Nationales Integrationsvertrauen | Kann politische Kosten und nationale Folgen beeinflussen, erzeugt aber keine automatischen Stimmen. |
| `global.EU_passed_votes` | Tatsächlich in Kraft gesetzte Beschlüsse | Ein vorläufiger Ratsbeschluss über einen noch unratifizierten Vertrag gehört nicht hinein. |
| `EU_budget_contribution_weekly` | Wöchentlicher nationaler Beitrag | Wird bereits vom MD-Geldsystem abgebucht. Nicht zusätzlich monatlich Treasury abziehen. |
| Bestehende Zuschussvariablen | Bewilligte nationale Rückflüsse | Weiter über das MD-Geldsystem verrechnen; pro Neuberechnung zurücksetzen und aus dem genehmigten Haushalt ableiten. |
| `global.EU_dirty_update_var` | Aktualisierung der bestehenden Oberfläche | Nach Änderung auslösen; Wirtschaftswerte zusätzlich über die vorhandene Finanzberechnung aktualisieren. |

Belege: [Mitgliedsidee mit on_add und on_remove](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/ideas/Organizations.txt:4>), [Collections](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/collections/collections.txt:3>), [Einnahmenbuchung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/00_money_system.txt:1032>), [Beitragsbuchung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/00_money_system.txt:4012>).

## Die vorhandenen Eintrittspunkte gezielt umbauen

| Vorhandener Einstieg | Erforderliche Änderung für 1970 |
| --- | --- |
| `on_startup_euu_action` | Gemeinsame Spielregelbehandlung behalten. Danach zwischen eigenem 1970-Initializer und modernem Initializer verzweigen. |
| `EU_adopt_passed_laws` | Für 1970 `CWEC_sync_member_contracts` aufrufen; moderne Gesetzesübernahme bleibt im anderen Zweig. |
| `EU_apply_for_membership` | 1970 nur Antrag beziehungsweise Verhandlungsfortschritt; Mitgliedsidee erst beim ratifizierten Abschluss vergeben. |
| `EU_voting_decision_result_trigger` | Auf einen verfahrensabhängigen Ergebnistrigger verzweigen. Anzeige benutzt dieselben berechneten Summen. |
| `apply_EU_QMV_result` | 1970-Auswertung muss vor dem heutigen Sonderfall EU111 liegen. Ratifikation und Inkrafttreten trennen. |
| `EU_finalize_passed_agenda` | Die parlamentarische Stufe 1970 als Stellungnahme behandeln; negative Stellungnahme darf gewöhnliche Ratsvorlagen nicht automatisch wie ein modernes allgemeines Zustimmungserfordernis blockieren. |
| `cleanup_european_union_voting` | Technisches Schließen und Eintragen eines geltenden Beschlusses trennen. Ratifikation beginnt ohne vorzeitigen Eintrag in `EU_passed_votes`. |
| Ratsbuttons und Abstimmungsevents | Zentralen Stimmrechtstrigger und gemeinsame Effekte für Ja, Nein und Enthaltung benutzen. Auch im Effekt erneut validieren. |
| Haushaltsmissionen und Änderungsbuttons | Zuständigkeit auf 1970-Verfahren umstellen; Entwurfswerte von geltenden Beiträgen und Ausgaben trennen. |
| EU-Monatsblock und europäische Wahlereignisse | 1970-eigene Pflege und Wahlregeln; keine zusätzlich parallel laufende moderne Ereigniskette. |
| `leaving_EU` und Mitgliedschaftsverlust | Gemeinsames Cleanup behalten und um 1970-Verträge, Zuschüsse, Ämter und Ratifikationen ergänzen. Politisches Austrittsverfahren getrennt regeln. |

Quellstellen: [Startup](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:613>), [Gesetzesübernahme](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1927>), [Aufnahme](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:1634>), [Ergebnistrigger](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/99_EU_voting_scripted_triggers.txt:16>), [Ergebnisdispatcher](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:316>), [Parlamentsabschluss](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:1091>), [Cleanup](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_EU_voting_scripted_effects.txt:1154>), [Monatsblock](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/MD_on_actions.txt:724>), [Austritt](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:343>).

Eine besonders wichtige Nebenwirkung ist bereits belegt: `EU_member.on_add` ruft `EU_adopt_passed_laws` auf. Letzterer vergibt ohne moderne DSGVO-/Asylbeschlüsse automatisch `foreign_data_kraken` und `asylum_shopping`. Ein neuer Startup allein behebt das nicht. Der 1970-Zweig der Gesetzesübernahme muss vor der ersten Vergabe von Mitgliedsideen eingebaut sein. [DSGVO-Standardfolge](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:2026>), [Asyl-Standardfolge](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:2057>).

## Initialisierung in fester Reihenfolge

Der bestehende einmalige Aufruf liegt nach der Länderinitialisierung. Diesen Einbaupunkt nutzen; kein unabhängiges zweites Startup mit ungesicherter Reihenfolge ergänzen. [Aufruf in der Hauptinitialisierung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/00_on_actions.txt:1953>).

1. EU-Abschaltregel und Abstimmungs-Cooldowns wie bisher einlesen. Für deaktiviertes System keine EG-Inhalte starten.
2. Bei `IMP_is_1970_scenario` den 1970-Zweig wählen. Initialisierungs- und Schemaversion prüfen; beim erneuten Laden keinen historischen Reset ausführen.
3. Amtszeiger, benötigte Arrays, Wahl-/Delegationsdaten und zulässige 1970-Agenden vorbereiten. EUU bleibt technischer Institutionsscope, kein automatisch freigesetzter Staat.
4. Geltende Ausgangsverträge und Kompetenzflags setzen, damit die anschließende Mitgliedschaftssynchronisierung die richtigen Inhalte übernimmt.
5. FRA, GER, ITA, BEL, HOL und LUX über `add_ideas = EU_member` aufnehmen. Der vorhandene on_add-Hook schreibt das Array; nicht noch einmal dieselben Tags hineinschreiben.
6. Ratsgewichte, Delegationssitze, nationalen Integrationsvertrauensstand und rotierenden Vorsitz initialisieren. Keine moderne EP-Direktwahlmission aktivieren.
7. Nach verfügbaren nationalen Wirtschaftswerten `set_EU_gdp` und die benötigten Beitrags-/Verteilungsberechnungen ausführen. Ein anfänglicher gültiger Haushalt besteht unabhängig von einer späteren Reformkonferenz.
8. Mitgliedschaft, Budget und Oberfläche aktualisieren; Initialisierung als abgeschlossen markieren. Moderne Timer und Agenden werden in diesem Zweig gar nicht erst gestartet.

Für die erste Lieferung einen neuen Kampagnenstart als Abnahmegrundlage verwenden. Eine spätere Save-Migration benötigt eine eigene Funktion: laufende alte Abstimmungen abwickeln oder verwerfen, Entwürfe zurücksetzen und vorhandene legitime Mitgliedschaften erhalten. Ein pauschales Zurücksetzen auf die Sechs bei jedem Laden wäre falsch.

## Gemeinsames Vertragsverfahren

Für die erste Fassung genügt ein gleichzeitig laufender ratifikationspflichtiger Vertrag. Weitere Anträge bleiben in der vorhandenen Warteschlange. Das verhindert, dass neue Verhandlungen globale Daten eines noch offenen Vertrags überschreiben.

| Phase | Gespeicherter Zustand | Wirkung |
| --- | --- | --- |
| Antrag | Dossier-ID, Antragsteller, betroffene Länder, Vorschlagsversion | Ein nachvollziehbarer Gegenstand liegt vor. |
| Beratung | Festgelegter Text und finanzielle Bedingungen | Parlamentarische Stellungnahme und Regierungsgespräche. Änderungen erzeugen eine neue Version. |
| Rat | Berechtigte Wähler und passende Gewichte als Momentaufnahme | Ja, Nein, bewusste Enthaltung und fehlende Antwort getrennt zählen. |
| Ratifikation | Unveränderliche Vertragsversion und erforderliche Ratifikationsparteien | Jede Regierung entscheidet nach dem vorgesehenen nationalen Verfahren. |
| Inkrafttreten | Abschlussmarkierung vor Anwendung der Folgen | Nur jetzt geltende Verträge, Mitgliedschaft und Beiträge ändern; Wirkung genau einmal ausführen. |
| Scheitern | Ablehnungs-/Fristgrund und technischer Abschluss | Entwurf und Missionen aufräumen; bestehende Verträge gelten weiter. |

Vorgeschlagene Helfer: `CWEC_begin_proposal`, `CWEC_cast_vote`, `CWEC_recalculate_tally`, `CWEC_finish_council`, `CWEC_begin_ratification`, `CWEC_commit_treaty` und `CWEC_close_proposal`.

Antrag und Abschluss haben unterschiedliche Aufrufscopes: Ein Button läuft im Spielerland, die zentrale Verarbeitung in einem ausdrücklich festgelegten Institutionsscope, Mitgliedseffekte im betroffenen Land. Antragsteller-ID und Vertragsparteien vor dem Scopewechsel speichern. Nach Annexion oder Arrayänderung keine implizite ROOT/PREV-Kette für die ursprünglichen Parteien voraussetzen.

Die Ja-/Nein-Buttons rufen denselben zentralen Abstimmungseffekt auf wie menschlich beantwortete Ereignisse. Der Effekt prüft menschliche Kontrolle, Phase, Dossier-Version und Berechtigung erneut. Automatische AI-Stimmen und indirekte Unterstützung durch AI-Parteien sind ausgeschlossen. Bei Stimmenwechsel wird der alte Zustand ersetzt und anschließend die Summe aus den gültigen Stimmen neu berechnet. Ein offenes Ereignis aus einer alten Vertragsversion darf keine neue Abstimmung beeinflussen.

Gewöhnliche Sachbeschlüsse können nach der passenden Ratsentscheidung unmittelbar gelten. Grundlegende Verträge brauchen Ratifikation. Die spätere Aufnahme weiterer Staaten ändert die Ratszusammensetzung und erfordert mit dem Aufnahmevertrag eine neue Gewichtstabelle und Schwelle. Die 17/12-Regel darf deshalb nicht für jede künftige Mitgliederzahl fest im Ergebnistrigger stehen.

Vorschlagsdaten werden im HOI4-Skript über Variablen, Flags, Arrays und ausdrückliche Dispatcher umgesetzt. Eine beliebige JSON-Objektstruktur wäre keine unmittelbar ausführbare Spielmechanik. Bei vielen Dossiers kann ein Entwicklungswerkzeug aus einem Katalog die wiederkehrenden Skript- und Lokalisierungsteile erzeugen; die Mod lädt weiterhin reguläre Spielskripte.

## Budget und Projekte an das MD Geldsystem anschließen

Das bestehende Geldsystem setzt seine zusätzlichen Einnahmen und Ausgaben bei Neuberechnung zurück und baut sie aus einzelnen Quellen wieder auf. Ein eigener dauerhafter Zuschlag direkt auf `additional_income_rate` wäre deshalb nicht stabil. Beiträge und Projektwirkungen müssen über benannte Quellvariablen in diese Berechnung einfließen. [Einnahmenberechnung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/00_money_system.txt:800>), [Ausgabenberechnung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/00_money_system.txt:3617>).

Die vorhandenen EG-Beiträge und Zuschussvariablen als Buchungsschnittstellen weiterverwenden und um eine gemeinsame, tatsächlich gedeckte Kasse ergänzen. Gemeinsame Projekte erhalten einen Anteil des genehmigten Budgets; zusätzliche nationale Zahlungen werden ausdrücklich ausgewiesen. Derselbe Betrag darf nicht zugleich als voller nationaler Zuschuss und als Gemeinschaftsprojekt ausgegeben werden. Jede Zuführung und Auszahlung benötigt eine Gegenbuchung. Die genauere Ausführung steht unten in den Abschnitten zu Zahlungslauf und Förderarten.

Finanzwerte tragen eine eindeutige Zeiteinheit. Der heutige Beitrag wird jährlich berechnet und durch 52 geteilt; die Einnahmenseite nutzt dagegen pauschal 0,019. Für 1970 eine gemeinsame Umrechnung festlegen, damit geplante Einnahmen und Ausgaben übereinstimmen. Die native Budgetfunktion verbraucht außerdem `EU_seigniorage_pool`; sie eignet sich deshalb nicht als beliebig oft aufgerufene reine Entwurfsvorschau. [Budgetberechnung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1312>).

Entwürfe bekommen eigene `CWEC_draft_*`-Werte. Die bestehenden Buttons ändern derzeit geltende Callrates und berechnen Beiträge unmittelbar neu. Solche Änderungen dürfen während der Ratifikation noch keine echten wöchentlichen Zahlungen verändern. Erst `CWEC_commit_treaty` übernimmt die Entwurfswerte, berechnet nationale Beiträge und Zuschüsse neu und aktualisiert Finanzberechnung sowie Anzeigen. [Heutiger Callrate-Button](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:2677>).

Projektwirkung und Finanzierung ebenfalls trennen. Beispiel Euratom: nationaler Beitrag und genehmigter Gemeinschaftsanteil finanzieren das Vorhaben; ein ländergebundener Modifier gewährt nur während gültiger Teilnahme den vereinbarten Forschungsbonus. Die gesamte Technologie eines Partners wird dadurch nicht automatisch geerbt. Abschluss, Abbruch und Austritt haben jeweils einen definierten Effekt.

## Länderpolitik und Bündnisse getrennt anbinden

- EG-Vollmitgliedschaft, EFTA, Assoziierung, Währung und Verteidigung erhalten unterschiedliche Teilnehmermengen. Ein Staatsvertrag darf keine militärischen Folgen aus einer bloßen gemeinsamen Wirtschaftsmitgliedschaft ableiten.
- Nationale Foki stellen Anträge oder verändern Verhandlungspositionen. Sie vergeben keine EG-Mitgliedschaft und setzen keine gesamteuropäischen Vertragsfolgen eigenmächtig durch.
- Griechenlands bestehendes Rüge-/Überwachungsverfahren schaltet mögliche Gespräche frei. Der eigentliche Beitritt bleibt beim gemeinsamen Verfahren. Zypernentscheidungen gehen weiter über die beteiligten nationalen Systeme.
- Die EU-Monatsprüfung bekommt für 1970 passende Vertrags- und Finanzpflege. Mitgliedschaftsänderungen rufen dieselbe Pflege sofort auf. Keine zweite unabhängige tägliche Gesamtsimulation ergänzen.
- NATO-Wechsel, Flottentransfer und Staatsvereinigung brauchen jeweils ausdrücklich zustimmende Teilnehmer. Die Zustimmung zu einem Wirtschaftsvertrag ist dafür kein Ersatz.
- Reine Oberflächenauswahl im betrachtenden Spielerland speichern. Geteilte globale Werte sind nur für den gemeinsamen politischen Zustand vorgesehen.

## Konkreter erster spielbarer Durchlauf

Als ersten vollständigen Vertrag einen britischen Aufnahmeprozess implementieren. Eine dynamische Erweiterung in diesem Beispiel muss zugleich Stimmgewichte und Delegationen für die tatsächlich entstehende Mitgliedermenge festlegen; sie darf nicht stillschweigend eine historische Neunergemeinschaft voraussetzen.

1. ENG stellt einen Antrag und erhält den Verhandlungsstatus. Eine echte Mitgliedschaft entsteht noch nicht.
2. Ein Vertragspaket legt Beitrag, Agrar-/Handelsbedingungen, Übergangsfristen, Sitze und die künftigen Ratsregeln fest.
3. Die menschlich vertretenen Mitglieder beraten und entscheiden im vorgesehenen Ratsverfahren. ENG sieht seinen Status, hat aber keine Mitgliederstimme.
4. Das feststehende Paket wird von den erforderlichen menschlich vertretenen Vertragsparteien ratifiziert. Ein menschlich gespieltes ENG muss selbst zustimmen. Bei einem KI-Bewerber beschließt der menschliche Spielerkreis dessen Aufnahme nach der festgelegten MP-Ordnung; es gibt keine zusätzliche KI-Ratifikationsabstimmung. Ein Gegenentwurf hebt frühere Zustimmungen zu einer anderen Version auf.
5. Beim Inkrafttreten erhält ENG einmal `EU_member`. `CWEC_sync_member_contracts` übernimmt nur geltende EG-Regeln; die neue Gewichtung und die Finanzierung werden aktiviert.
6. Der bestehende MD-Wochenhaushalt bucht den Beitrag und die bewilligten Rückflüsse. NATO-Mitgliedschaft und nationale Armeen folgen weiterhin ihren eigenen Verträgen.
7. Bei Ablehnung werden Verhandlung und Missionen geschlossen. ENG behält seine bisherigen Beziehungen und kann eine separate EFTA-/Freihandelsoption verfolgen.

Danach auf denselben Ablauf Haushaltsreform, andere Bewerber, Werner-Kooperation und Forschung aufsetzen. Die Dossiers unterscheiden sich in Parteien, Verfahren und Wirkungen; sie benötigen keine jeweils eigene parallele Verwaltungsmechanik.

## Dateien und Lieferungsschritte

Neue Inhalte sinnvoll in `CWEC_1970_effects.txt`, `CWEC_1970_triggers.txt`, `CWEC_1970_decisions.txt`, `CWEC_1970_events.txt` und `CWEC_1970_l_english.yml` bündeln. Dazu nur die oben benannten Verbindungen in den bestehenden Systemdateien ändern. Neue numerische Agenden-IDs nach Kollisionsprüfung reservieren; 998 und 999 sind bereits besondere Haushalts-IDs. Alle GUI-, Tooltip-, AI- und Ergebnisregistrierungen gemeinsam ergänzen.

| Lieferung | Enthaltene Arbeit | Abnahme |
| --- | --- | --- |
| A Systemgrundlage | Startup, Mitgliedschaftszyklus, historische Ämter, Delegierte, passende Agenden und Budgetzuständigkeit | Start, Laden, Monatswechsel und Bürgerkriegsende erhalten konsistente Mitglieder und Werte. |
| B Gemeinsames Vertragsverfahren | Stimmrechte, Verfahrenswahl, Ratifikation, einmaliger Abschluss und Oberflächenzustände | Zwei Spieler können parallel bedienen; Kandidaten stimmen nicht mit; alte Ereignisse ändern keine neuen Dossiers. |
| C Erster Aufnahmevertrag | Ein vollständiger ENG-Durchlauf mit Beitrag, Ratifikation und neuen institutionellen Werten | Aufnahme und Ablehnung funktionieren; Geld wird genau einmal gebucht; keine automatische Bündnisänderung. |
| D Weitere historische Dossiers | Haushalt, Landwirtschaft, politische Kooperation und weitere Bewerber | Neue Dossiers benutzen dieselben Schnittstellen und übernehmen keine modernen Standardfolgen. |
| E Alternative Verträge | EFTA/NORDEK, Währung, politische Union und freiwillige Verteidigung | Unterschiedliche Teilnehmergruppen und Austritte werden vollständig abgewickelt. |

Vor Freigabe passende statische Prüfungen für eindeutige IDs, definierte Effekte und konsistente Agenden ergänzen. Im Spiel die Zustandswechsel, Geldsummen, mehrere menschliche Regierungen, Amtsverlust und Speichern/Laden mit offenem Vertrag prüfen. Ein einmal erfolgreich gestartetes Spiel ersetzt diese Integrationsprüfung nicht.

## Beschlüsse wirksam verabschieden und umsetzen

Die drei Ebenen Vertragsgrundlage, einzelner Beschluss und nationale Umsetzung bekommen unterschiedliche Regeln. Eine nationale Ratifikation ist für grundlegende Vertragsänderungen und Beitritte vorgesehen. Ein gewöhnlicher Beschluss innerhalb bereits übertragener Zuständigkeiten folgt dem dafür festgelegten Ratsverfahren. Eine überstimmte Regierung bleibt daran gebunden. Ihr Nein ist kein nachträgliches Opt-out.

Der Vertrag von Rom unterscheidet unmittelbar geltende Verordnungen, hinsichtlich ihres Ziels bindende Richtlinien und für ihre Adressaten bindende Entscheidungen. Vertragsverletzungen konnten über Kommission und Gerichtshof behandelt werden. Diese Unterscheidung ist die historische Grundlage; der folgende Spielablauf ist ein Umsetzungsvorschlag. [Originalvertrag Artikel 169 bis 171 und 189](https://www.wipo.int/wipolex/en/text/473854).

| Beschlussart | Wirkung im Spiel | Nationale Handlung |
| --- | --- | --- |
| Geltende Verordnung oder Haushaltsentscheidung | Regel, Zahlungspflicht oder Förderbedingung wird zum festgelegten Termin aktiviert. | Erfüllung ist die reguläre Folge der Mitgliedschaft. Eine ausdrückliche Nichtbefolgung ist ein eigener politischer Konflikt. |
| Richtlinie oder Umsetzungsprogramm | Frist, Kosten und überprüfbares Ziel werden gesetzt. | Wahl zwischen zulässigen Umsetzungspfaden, jeweils mit eigenen Kosten und Wirkungen. |
| Vertragsreform oder Beitritt | Neue Zuständigkeiten erst nach erforderlichen Ratifikationen. | Nationale Zustimmung, Ablehnung oder Neuverhandlung. |
| Freiwilliges Zusatzprogramm | Nur unterzeichnende und tatsächlich teilnehmende Länder erhalten Pflichten und Vorteile. | Beitritt und Austritt nach den vereinbarten Bedingungen. |

Historische Inhalte werden durch auswählbare Dossiers konkret angeboten. Voraussetzungen und historische Referenztermine machen passende Vorlagen sichtbar; Spieler bringen sie ein und stimmen ab. Es gibt keine KI-Stimmen und keine automatisch aus nationalen Parteiwerten berechneten politischen Zustimmungen. Bereits vor 1970 geltende Ausgangsregeln gehören zum Startzustand. Ein neuer historischer Beschluss braucht ein Spielergebnis; historische Referenztermine erzwingen kein Ergebnis.

Für Richtlinien beispielsweise `CWEC_implementation_status`, Frist und dossierbezogene Erfüllungsbedingungen pro Land speichern. Erfüllung wird aus dem realen Zustand geprüft, etwa einer tatsächlich aktivierten Regel oder geleisteten Kofinanzierung. Nicht allein ein Ja-Ereignis als Erfolg verbuchen. Bereits erbrachte Umsetzung wird nach Laden und Regierungswechsel erhalten.

Bei ausdrücklicher Nichtbefolgung folgen begründete Mitteilung, Antwortfrist, mögliche gerichtliche Feststellung und politischer Konflikt. Eine programmspezifische Auszahlung kann ausbleiben, wenn ihre genehmigten Förderbedingungen nicht erfüllt sind. Ein pauschaler Entzug sämtlicher Gemeinschaftsmittel oder moderne tägliche Strafzahlungen werden daraus nicht automatisch abgeleitet. Ein alternatives neues Sanktionsregime muss selbst vertraglich beschlossen werden.

## Eine gedeckte Gemeinschaftskasse mit echtem Zahlungslauf

Zusätzlich zu den bestehenden MD-Schnittstellen vorgeschlagene Buchhaltungswerte anlegen: `global.CWEC_cash_balance`, `global.CWEC_funds_committed`, `CWEC_contribution_due`, `CWEC_contribution_paid`, `CWEC_contribution_arrears`, `CWEC_grants_paid` und eine Abrechnungsnummer. Reservierte Mittel sind ein Teil der vorhandenen Kasse und werden bei der Berechnung freier Liquidität abgezogen; sie sind kein zusätzliches Geld.

Die verbindliche Gleichung je Abrechnungszeitraum lautet:

`Closing Cash = Opening Cash + Actual Receipts - Actual Disbursements`

Bewilligte Mittel und angekündigte Einnahmen werden separat angezeigt. Sie erhöhen den Kassenbestand nicht. Ein zusätzlicher Fonds erhält sein Geld durch Umbuchung aus der Gemeinschaftskasse, nicht durch erneutes Addieren derselben Beiträge.

Im vorhandenen MD-Code berechnet `ingame_update_setup` Finanzwerte auch bei manuellen Aktualisierungen neu. Der tatsächliche wöchentliche Treasury-Zugang liegt dagegen in `on_weekly` bei der Anwendung von `treasury_rate_gain`. Genau dort wird ein 1970-Abrechnungshook eingebaut; eine reine Neuberechnung darf kein Geld in die Gemeinschaftskasse einzahlen. [Finanzneuberechnung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/00_money_system.txt:220>), [tatsächliche Wochenbuchung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/MD_on_actions.txt:137>).

Der konkrete Zahlungslauf:

1. Einmal global pro Woche die fälligen Beiträge und bereits aus vorhandenem Bargeld gedeckten Auszahlungen vorbereiten. Die Auszahlungen werden reserviert. Anfangs gibt es einen tatsächlich eingezahlten Vorschuss oder einen ersten Einzahlungszeitraum vor Auszahlungen.
2. Die nationalen MD-Einnahmen und Ausgaben lesen genau diese vorbereiteten Beträge. Geltende Beiträge verschlechtern die nationale Budgetbilanz; bewilligte staatliche Zuschüsse verbessern sie entsprechend.
3. Direkt nach der nationalen Wochenbuchung bestätigt `CWEC_record_country_settlement` einmal pro Abrechnungsnummer die gebuchten EG-Positionen. Derselbe Beitragsbetrag wird der gemeinsamen Kasse gutgeschrieben, derselbe Auszahlungsbetrag wird ihr entnommen. Kein zusätzlicher Treasury-Abzug neben der MD-Ausgabenposition.
4. Neue Einnahmen stehen für den nächsten Zahlungslauf bereit. Bereits reservierte Auszahlungen hängen dadurch nicht von der Reihenfolge ab, in der Länder ihren Wochentick erhalten.
5. Bei deaktiviertem nationalem Wirtschaftssystem wird keine Zahlung bestätigt. Bei bewusster Beitragszurückhaltung sinkt der tatsächlich gebuchte Beitrag; die Differenz zur Pflicht wird Rückstand. Der Fonds verteilt diesen fehlenden Betrag nicht.
6. Länder mit Defiziten nutzen grundsätzlich die bestehende MD-Finanzierung einschließlich ihrer Schuldenlogik. Eine politische Zahlungssperre wird als solche modelliert; sie ergibt sich nicht automatisch allein aus einem negativen Haushaltssaldo.

Bei Mittelknappheit gelten die genehmigten Prioritäten: bereits reservierte Zahlungen, vertragliche Pflichtausgaben und danach neue Projektzusagen. Ungedeckte Ansprüche erscheinen als offen; sie erzeugen eine Nachtragsbudget- oder Kürzungsentscheidung. Die Gemeinschaft erhält keine unbegrenzte automatische Kreditaufnahme.

## Historisch passende Einnahmen und Ausgabenregeln

Für 1970 eine kalibrierte Ausgangsfinanzierung verwenden. Nach einer ratifizierten Eigenmittelreform werden Agrarabschöpfungen, Außenzolleinnahmen und ergänzende nationale Beiträge getrennt berechnet. Die MD-Rohstoffimporte allein bilden den gesamten Warenhandel nicht ab; bis eine breitere Handelsbasis vorhanden ist, sind entsprechende Einnahmen ausdrücklich Schätzgrößen.

Der ursprüngliche Eigenmittelbeschluss von 1970 sah für 1971 bis 1974 einen Schlüssel für die ergänzenden Beiträge vor: BEL 6,8 %, GER 32,9 %, FRA 32,6 %, ITA 20,2 %, LUX 0,2 %, HOL 7,3 %. Das sind Anteile des nötigen Restbeitrags, keine pauschalen Prozentsätze des nationalen BIP. Einbehaltene Erhebungskosten und Übergangsregeln sind zusätzlich zu berücksichtigen. Bei Erweiterung muss der Beitragsschlüssel angepasst werden. [Beschluss 70/243 Artikel 3](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A31970D0243).

Die Ausgabenseite folgt dem beschlossenen Programm. Agrarförderung orientiert sich an förderfähiger Landwirtschaft und anerkannten Ausgaben; Sozialförderung an genehmigten Beschäftigungs- und Ausbildungsprogrammen; Investitionen an bewilligten Projekten und Kofinanzierung. Niedriges BIP pro Kopf allein begründet keinen automatischen Anspruch auf alle Budgetkörbe.

Gewichte und Ausgangsproduktion werden vor den eigenen Förderwirkungen festgehalten und regelmäßig überprüft. Dadurch erhöht ein Zuschuss nicht im selben Zahlungslauf seine eigene Bemessungsgrundlage. Förderfähigkeit, Obergrenzen, tatsächlich geleistete nationale Anteile und mögliche Rückforderungen sind eigene Zustände.

## Geldempfänger und wirtschaftliche Wirkung unterscheiden

| Förderart | Buchung | Tatsächlicher Vorteil und mögliche Kosten |
| --- | --- | --- |
| Staatlicher Haushaltszuschuss | Gemeinschaft zahlt, nationale Treasury erhält. Zweckbindung bei Bedarf getrennt erfassen. | Mehr finanzierbarer nationaler Spielraum; Beitrag und Bedingungen bleiben belastend. |
| Agrarstützung an Produzenten | Gemeinschaft finanziert ein sektorales Programm. Eine über die Regierung laufende Zahlung bekommt eine entsprechende zweckgebundene Programmausgabe. | Einkommens-/Preisstabilisierung im Sektor; mögliche Überproduktion, Lager-/Exportkosten und Belastung von Verbrauchern. Produktivitätszuwachs erst durch gesonderte Modernisierung. |
| Bau- oder Modernisierungszuschuss | Gemeinschaftsanteil plus nationaler Eigenanteil finanzieren einen konkreten Auftrag. | Tatsächlicher Baufortschritt oder Fertigstellung im Zielstaat; Bauzeit, Arbeitskräfte, Betriebskosten und Eigenanteil bleiben relevant. |
| Forschung | Bewilligte Mittel finanzieren das laufende Projekt. | Begrenzter sachbezogener Forschungsbonus während gültiger Teilnahme; keine vollständige Technologievererbung. |
| Darlehen | Auszahlung schafft beim Kreditnehmer Liquidität und Schuld, beim Kreditgeber eine Forderung. Tilgung und Zinsen werden separat verbucht. | Früher realisierbares Projekt gegen spätere Rückzahlung; ein Kredit ist kein Zuschuss. |

Die Steuerberechnung besitzt bereits landwirtschaftliche Bemessungsgrößen und Produktivitätsmodifikatoren. Preis-/Einkommensstützung benötigt jedoch eine eigene begrenzte Wirkungsberechnung; eine bloße Erhöhung des Produktivitätswerts würde eine andere Politik simulieren. Die vollständige Lebensmittelpreisbildung ist damit noch nicht abgebildet. [Agrarsteuerberechnung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/00_money_system.txt:398>), [Landwirtschaftsdistrikte](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/00_money_system.txt:535>).

Der vorhandene Investitionsstart `start_project_two` zieht Geld ab und erhöht das internationale Investmentportfolio des Investors. Er kann deshalb nicht unverändert als Gemeinschaftszuschuss dienen. Die Projekt-/Bauabwicklung lässt sich nach Trennung von Zahlungsquelle und privater Investorenrendite wiederverwenden. Ein öffentlich finanzierter Zuschuss darf keine zusätzliche frei handelbare Kapitalanlage erzeugen. [Investitionsstart](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_investment_scripted_effects.txt:486>).

Die EIB bietet historisch eine geeignete Grundlage für die gesonderte Kreditschiene. Ihr Jahresbericht 1970 beschreibt konkrete Darlehen und regionale Investitionsvorhaben. Das begründet projektbezogene Kreditbedingungen, nicht einen automatisch ausgeschütteten Fonds ohne Rückzahlung. [EIB Jahresbericht 1970](https://www.eib.org/files/publications/general/reports/ar1970en.pdf).

## Rechenbeispiel für eine geschlossene Umverteilung

Nur ein erfundenes Spielbeispiel, keine Rekonstruktion historischer Auszahlungen. Angenommen, der ergänzende nationale Wochenbeitrag beträgt insgesamt 100 Millionen Mod-Geldeinheiten und der ursprüngliche Schlüssel für 1971 bis 1974 gilt. Die beschlossenen nationalen Rückflüsse betragen 94 Millionen, Verwaltungsleistungen 4 Millionen; 2 Millionen verbleiben in der Kasse.

| Land | Einzahlung | Rückflüsse in das Land | Brutto Nettoposition |
| --- | ---: | ---: | ---: |
| GER | 32,9 | 20,0 | −12,9 |
| FRA | 32,6 | 30,0 | −2,6 |
| ITA | 20,2 | 32,0 | +11,8 |
| HOL | 7,3 | 6,0 | −1,3 |
| BEL | 6,8 | 5,0 | −1,8 |
| LUX | 0,2 | 1,0 | +0,8 |
| Gesamt | 100,0 | 94,0 | −6,0 |

Die Brutto Nettoposition enthält sektorale Förderungen und Projektzahlungen. Sie ist deshalb nicht identisch mit frei verfügbarem Regierungseinkommen. Zusätzliche Handelsvorteile, Verbraucherkosten, nationale Eigenanteile und spätere Steuereffekte werden daneben ausgewiesen.

Ein Staat kann also Nettozahler sein und dennoch wirtschaftlich gewinnen. Umgekehrt kann ein Land hohe Rückflüsse erhalten, aber durch Eigenanteile oder ungeeignete Projekte belastet werden. Genau daraus entstehen sinnvolle Budgetverhandlungen.

## Englische Anzeigen und wirtschaftliche Abnahme

Alle folgenden Bezeichnungen sind englische Ingame-Texte: `Community Budget`, `National Contribution`, `Funds Received`, `Sectoral Support`, `Project Co-financing`, `Net Budget Position`, `Outstanding Contributions`, `Funds Committed`, `Funds Disbursed`, `Implementation Deadline` und `Non-compliance`.

Vor einer Abstimmung zeigt der Spieler seine erwartete wöchentliche Zahlung, zweckgebundene Rückflüsse, Eigenanteile, Umsetzungsfrist und sachliche Wirkung. Geschätzte Effekte werden als `Estimated` bezeichnet. Während der Durchführung zeigt die Oberfläche bewilligte, tatsächlich gezahlte und noch offene Mittel getrennt. Nationale Gesamtbilanz und Gemeinschaftskasse müssen auf denselben gebuchten Beträgen beruhen.

Für die spätere Abnahme gezielt nachweisen: Summe aller Einzahlungen entspricht den Gemeinschaftseinnahmen; Auszahlung überschreitet keine freie Kasse; wiederholter Finanzrefresh bucht nichts; Speichern/Laden verdoppelt keine Zahlung; Rückstände sind keine verfügbaren Mittel; zweckgebundene Förderung erzeugt keine doppelte freie Treasury; Darlehen hat Schuld und Forderung; Ausbau der Landwirtschaft füttert nicht unmittelbar seinen eigenen Förderschlüssel.

## Geldflüsse in der Oberfläche nachverfolgen

Die Haushaltsoberfläche erhält zusammengehörige Ansichten `Overview`, `Contributions`, `Programmes`, `Projects` und `Transactions`. Sie zeigen denselben Buchungsstand. Ein Spieler kann vom Gesamtbudget zum Programm, von dort zum Empfängerland und anschließend zum konkreten Projekt und dessen Zahlungen wechseln.

| Ansicht | Sichtbare Angaben |
| --- | --- |
| `Overview` | Anfangskasse, tatsächliche Einnahmen, tatsächliche Ausgaben, gebundene Mittel, freie Liquidität und Jahresansatz. |
| `Contributions` | Je Land fällig, gezahlt, zurückständig, Erhebungskosten und beschlossener Beitragsschlüssel. |
| `Programmes` | Bewilligter Rahmen, gebundene Mittel, ausgezahlte Mittel, offene Ansprüche und Empfängerländer. |
| `Projects` | Projektname, Zielstaat oder Zielregion, Begünstigte, Gesamtkosten, Gemeinschaftsanteil, Eigenanteil, Zahlungstranchen, Fortschritt und erwartete Fertigstellung. |
| `Transactions` | Buchungsnummer, Abrechnungszeitraum, Zahler, Empfänger, Betrag, Programm, optionales Projekt und Buchungsgrund. |

Bei Förderungen sind zahlungsabwickelnde Regierung und eigentliche Begünstigte getrennt sichtbar. Beispiel: `Recipient Country: France`, `Beneficiary: Agricultural Producers`, `Programme: Common Agricultural Policy`. Das ist etwas anderes als ein frei verfügbarer Zuschuss an die französische Regierung.

Alle Geldmittel gehen zunächst in einen gemeinsamen Topf. Das Protokoll zeigt daher die wirklichen Schritte `Germany → Community Budget` und `Community Budget → Italian Infrastructure Project`. Eine erfundene exakte bilaterale Zuordnung von deutschen Beiträgen zu einer bestimmten italienischen Auszahlung wird nicht angezeigt. Eine anteilige Herkunftsschätzung müsste ausdrücklich als Schätzung gekennzeichnet werden.

Transaktionen entstehen erst bei tatsächlicher Buchung. Bewilligungen und Reservierungen stehen in eigenen Feldern. Jede Zahlung hat eine eindeutige Nummer; Rückzahlung oder Korrektur erzeugt eine neue Gegenbuchung mit Bezug auf die ursprüngliche Nummer. Vergangene Buchungen werden nicht rückwirkend umgeschrieben.

Für die Scripted GUI lassen sich die Datensätze über parallele Arrays und dynamische Listen abbilden. Ein begrenztes Detailprotokoll und dauerhaft gespeicherte Jahres-/Programm-/Landessummen halten Savegröße und Oberfläche beherrschbar. Die genaue Anzahl aufbewahrter Einzelzeilen wird bei der Implementierung anhand des Umfangs festgelegt. Die vorhandene `EU_dirty_update_var` aktualisiert die Ansichten nach einer Buchung; das Öffnen der Ansicht selbst verändert keine Geldbeträge.

## Auswählbare Integrationsprojekte und Erweiterungen

Die neue Ansicht `Integration Projects` bietet Karten oder Listeneinträge mit Voraussetzungen, beteiligten Staaten, finanziellen Folgen und einem Antragstellerknopf. Gesperrte Vorhaben bleiben mit einem konkreten Sperrgrund sichtbar. Statuswerte lauten `Available`, `Under Negotiation`, `Voting`, `Ratification`, `Implementation`, `In Force` und `Failed`.

| Englischer Ingame-Eintrag | Inhalt |
| --- | --- |
| `Own Resources Decision` | Reform der gemeinschaftlichen Finanzierung mit verbindlicher Einnahmen- und Ausgabenrechnung. |
| `First Enlargement` | Vertragspaket für ENG, IRE und DEN; NRY als eigene historische Alternativoption. |
| `Greek Accession` | Eigenes Aufnahmeverfahren mit politischen und wirtschaftlichen Bedingungen. |
| `Iberian Enlargement` | SPR und POR als einzeln abschließbare Teile eines Verhandlungspakets. |
| `1995 Enlargement` | AUS, FIN und SWE, abhängig von der tatsächlichen politischen Lage der Kampagne. |
| `Direct European Elections` | Reform von Delegationsbestellung und Sitzprofil; im MP werden politische Entscheidungen weiter ausschließlich von Spielern getroffen. |
| `Schengen Agreement` | Freiwilliger Vertrag über den schrittweisen Abbau von Binnengrenzkontrollen. |
| `Schengen Implementation Convention` | Begleitregeln, Zusammenarbeit, Finanzierung und tatsächliche Umsetzungsbedingungen. |
| `Single European Act` | Vertragspaket für weitere Binnenmarktreformen und entsprechende Kompetenzen. |
| `Treaty on European Union` | Wählbare institutionelle Reform mit gesondert ausgewiesenen Kompetenzen und Namenswechsel. |
| `European Regional Development Fund` | Späterer gemeinsamer Regionalfonds mit Projektbewilligung und Kofinanzierung. |

Historische Erweiterungen waren 1973 ENG/IRE/DEN, 1981 GRE, 1986 SPR/POR und 1995 AUS/FIN/SWE. Die Dossiers verwenden diese als Referenzgruppen. Der tatsächliche Beitritt hängt vom Spielbeschluss und den Bedingungen ab. Einzelne Ablehnungen dürfen nicht versehentlich sämtliche anderen Bewerber sperren. [Rat zur Erweiterungsgeschichte](https://www.consilium.europa.eu/en/policies/how-enlargement-works/timeline-accession-eu-member-states/).

Bei abweichendem Verlauf können Spieler andere Teilnehmer und Zeitpunkte vereinbaren. Für jede Abweichung müssen Aufnahmevertrag, Beitragsschlüssel, Ratssitze, Parlamentsmandate und Übergangsfristen aus der tatsächlichen Mitgliederliste entstehen. Eine historische Jahreszahl allein führt keinen Staat automatisch in die Gemeinschaft. Spätere Erweiterungsrunden können dieselbe Architektur nutzen, wenn die lange Kampagne sie politisch erreicht.

## Schengen mit tatsächlichen Umsetzungsschritten

Historische Referenz: 1985 unterzeichneten BEL, GER, FRA, LUX und HOL das Schengener Abkommen; die Durchführungsvereinbarung folgte 1990, die praktische Anwendung begann 1995. [EUR Lex zum Schengener Abkommen](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=LEGISSUM%3Aschengen_agreement), [Ratschronologie](https://www.consilium.europa.eu/en/history/).

Im Spiel werden Unterzeichnung, Ratifikation und tatsächliche Anwendung pro Teilnehmer getrennt gespeichert. Ein früheres alternatives Abkommen ist möglich, benötigt aber die vereinbarten Voraussetzungen, administrative Zusammenarbeit und Finanzierung. Nicht alle EG-Mitglieder müssen teilnehmen. Ein EG-Beitritt ist auch kein automatischer Schengen-Beitritt.

Vorteile entstehen aus tatsächlich geöffneten Verbindungen zwischen teilnehmenden Ländern. Vorgesehen sind begrenzte abstrahierte Erleichterungen für zivile Mobilität und grenzüberschreitende Wirtschaft. Kosten entstehen durch Umstellung, Begleitverwaltung und die vereinbarte Außengrenzenzusammenarbeit. Eine allgemeine Abschaffung aller Grenzkosten oder die Gewährung von Militärzugang folgt daraus nicht.

Eine Wiedereinführung von Kontrollen erhält einen eigenen zeitlich begrenzten Zustand mit Kosten und Rechtsfolgen gemäß dem beschlossenen Vertrag. Einfache Grenzöffnung und vollständiger Binnenmarkt bleiben unterschiedliche Projekte.

## Parlament und Rat wachsen mit den tatsächlichen Mitgliedern

Die alte feste Zielgröße von 732/750/1000 Sitzen wird im 1970-Modus durch Sitzprofile und länderspezifische Mandate ersetzt. Die Gesamtzahl ist stets die Summe der Mandate tatsächlicher Mitglieder. Ein Kandidat vergrößert das Parlament noch nicht. Eine Aufnahme oder ein Austritt löst die gemeinsame Neuberechnung von Mitgliedschaft, Parlament, Ratsgewichtung und Budget aus. [Heutige feste Zielgrößen](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1582>).

| Historisches Referenzprofil | Gesamtmandate bei entsprechender historischer Mitgliederliste |
| --- | ---: |
| Delegiertenversammlung der Sechs | 142 |
| Delegiertenversammlung nach der Erweiterung 1973 | 198 |
| Direktwahlprofil 1979 | 410 |
| Profil nach dem griechischen Beitritt 1981 | 434 |
| Profil nach der iberischen Erweiterung 1986 | 518 |

Quellen: [EWG-Vertrag Artikel 138](https://www.wipo.int/wipolex/en/text/473854), [Europäisches Parlament zur historischen Entwicklung](https://www.europarl.europa.eu/factsheets/IT/sheet/11/il-parlamento-europeo-contesto-storico), [erste Direktwahl beim Europäischen Parlament](https://www.europarl.europa.eu/infographic/european-parliament-timeline/index_en.html).

Ein Sitzprofilwechsel ist eine eigene Reform und nicht identisch mit einer Erweiterung. Für alternative Mitgliederlisten werden einzelne Mandate nach einem beschlossenen Schlüssel vergeben; fehlende Länder werden nicht trotzdem mitgezählt. Bei neuer Sitzverteilung benötigen Rundung, Mindestmandate und Gesamtzahl eine gemeinsame ganzzahlige Berechnung.

Im MP werden zwei Größen angezeigt: `Total Parliament Seats` für die ganze Institution und `Player-represented Seats` für das jeweils stimmberechtigte menschliche Parlament. KI-Mitgliedern zugeordnete Mandate bleiben als `Unrepresented Delegation` sichtbar und wirken nicht auf Abstimmungsergebnisse. Ein KI-Beitritt kann also die Institution vergrößern, ohne neue KI-Stimmen zu erzeugen.

## Sämtliche politischen Abstimmungen ausschließlich durch Spieler

Der vorgeschlagene `CWEC_can_cast_vote` verlangt Mitglieds-/Teilnehmerberechtigung, menschliche Kontrolle, die richtige Abstimmungsphase und die richtige Dossier-Version. Diese Prüfung steht in Buttons, Ereignissen und den eigentlichen Buchungseffekten. Die Wählerliste wird beim Öffnen der Abstimmung festgelegt; KI-Länder stehen weder im Zähler noch im Nenner.

Die bestehende AI-Ratswertung wird im 1970-Modus nicht aufgerufen. Ebenso dürfen `set_ruling_party_PG_support`, aus `party_pop_array` erzeugte automatische Fraktionszustimmungen und die bisherigen POTEF-Gesamtbevölkerungswerte kein Ergebnis liefern. Nationale Parteimechaniken können weiterlaufen; sie sind keine EU-Stimmabgabe. [Heutiger Ratsstart mit AI-Aufruf](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:4382>), [heutige POTEF-Stimmenberechnung](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1024>).

Als einfache erste MP-Fassung stimmt ein menschlicher Spieler für seine nationale Delegation ausdrücklich mit `For`, `Against` oder `Abstain`. Die Delegation bringt ihre festgelegten Mandate ein. Eine spätere Aufteilung in von Spielern kontrollierte politische Gruppen kann ergänzt werden; die KI erhält auch darüber keine versteckte Stimme. Ämter werden aus ausdrücklich nominierten menschlichen Kandidaten gewählt, ohne nachträglichen Einfluss einer simulierten KI-Bevölkerungswahl.

Empfohlene MP-Mehrheiten, bei Implementierung als gemeinsame Regel festzulegen:

- Gewöhnliche Parlamentsmehrheit: mehr als die Hälfte der für diese Abstimmung menschlich vertretenen Mandate.
- Qualifizierter Ministerratsbeschluss: auf die menschlichen Ratsgewichte umgerechnete Vertragsschwelle und zusätzlich eine Mehrheit der stimmberechtigten Spielerstaaten. Das ist eine erkennbare MP-Anpassung der historischen Gewichte.
- Einstimmiger Ratsbeschluss: keine Gegenstimme, bewusste Stimmabgabe aller erforderlichen Spielerstaaten; rechtlich zulässige Enthaltung gesondert behandeln.
- Vertragsratifikation: ausdrückliches Ja jeder erforderlichen menschlich vertretenen Vertragspartei. Keine fingierte Zustimmung aufgrund fehlender Antwort.
- Teilnahmequorum: als Ausgangsvorschlag mindestens zwei Drittel der beim Start festgelegten Spielerstaaten; mindestens zwei menschliche Mitgliedstaaten für eine reguläre MP-Abstimmung. Bei zu wenigen Spielern wartet das Verfahren sichtbar. Diese Quoren sind Balancingvorschläge, keine historischen Rechtszahlen.

Beispiel: Nur FRA und GER sind menschlich vertreten und verfügen im Delegiertenprofil zusammen über 72 Mandate. Die übrigen 70 Mandate bleiben institutionell sichtbar. Die Parlamentsmehrheit im menschlichen Kreis liegt bei 37; weder KI-Mitglieder noch deren Parteipopularität verändern sie.

Ein Disconnect entfernt ein zuvor berechtigtes Spielerland nicht aus dem laufenden Abstimmungskreis. Eine vorhandene Stimme bleibt erhalten; die KI gibt keine neue ab. Fehlende Stimmen bleiben sichtbar. Beim Fristablauf scheitert eine Vorlage am fehlenden Quorum beziehungsweise an ausbleibender notwendiger Ratifikation oder wird nach ausdrücklich geregelter Verlängerung neu angesetzt. Hotjoin und Mitgliederwechsel ändern die nächste Abstimmung, nicht rückwirkend die laufende.

KI-Mitglieder zahlen regulär Beiträge und erhalten regelgebundene Leistungen. Beschlüsse des menschlichen Spielerkreises werden nach der vereinbarten MP-Ordnung administrativ auf sie angewendet. Für die Aufnahme eines KI-Bewerbers gibt es keinen zusätzlichen AI-Annahmewurf. Ein menschlich gespielter Bewerber muss seiner eigenen Aufnahme zustimmen. Diese Vertretungsordnung ist eine bewusste Abweichung von der historischen politischen Repräsentation.

Das Abschließen und Auszählen übernimmt ein neutraler Skriptablauf. Ein vakantes Amt oder ein KI-Institutionsmonitor darf keine Stimme ersetzen und keinen Sieger auswählen. Ohne gültiges Ergebnis bleibt bei Ämtern nur eine definierte kommissarische Verwaltung bestehen; neue politische Befugnisse entstehen daraus nicht.

## Wählbarer Übergang von den Gemeinschaften zur Europäischen Union

Der Organisationsname wird über eine zentrale Scripted Localisation ausgegeben: zunächst `European Communities`, nach entsprechender Entscheidung `European Union`. Eine rein symbolische Entscheidung `Adopt the European Union Name` kann von einer umfassenderen Vertragsreform `Treaty on European Union` getrennt werden. Beide zeigen ausdrücklich, ob sie nur die Bezeichnung oder auch konkrete Zuständigkeiten ändern.

Historischer Referenzpunkt für die Entstehung der Europäischen Union ist das Inkrafttreten des Maastricht-Vertrags am 1. November 1993. Ein früherer Namenswechsel ist eine wählbare Alternative und löst allein weder Euro noch Staatsvereinigung aus. [EU Geschichte der 1990er Jahre](https://european-union.europa.eu/principles-countries-history/history-eu/1990-99_en).

Die Oberfläche enthält derzeit zahlreiche feste EU-Texte. Titel, Tooltips, Beschlüsse und Ereignisse werden für die neue englische Lokalisierung auf den gemeinsamen Organisationsnamen umgestellt. Interne `EU_*`-IDs bleiben bestehen. Das Umbenennen einer Institution benötigt keinen Austausch der nationalen Ländertags und keine Annexion. Ein echter späterer Bundesstaat bleibt ein eigenes Projekt. [Heutiger fester Fenstertitel](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/localisation/english/MD_focus_EU_l_english.yml:67>).

Zusätzliche spätere Abnahmefälle: KI zahlt und empfängt, kann aber über keinen Pfad abstimmen; KI-Parteien und Bevölkerungswerte ändern keinen Wahlsieger; 142 Gesamtmandate und 72 menschliche Mandate werden korrekt getrennt; neue Mitglieder ändern Sitzprofile und Finanzen; laufende Abstimmungen behalten ihre Anfangsbasis; Disconnect und Hotjoin erzeugen keine Ersatzstimme; Schengen-Unterzeichnung allein öffnet noch keine Grenze; der Namenswechsel verändert ausschließlich seine ausdrücklich beschlossenen Wirkungen; Transaktionsprotokoll und tatsächliche Kasse stimmen überein.
