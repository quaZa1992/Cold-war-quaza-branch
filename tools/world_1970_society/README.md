IMPERIA COLD WAR

# Währung, Religion und innere Machtgruppen am 1. Januar 1970

Die neuen Startwerte stehen direkt in den `1970.1.1`-Blöcken von **393 Länder-History-Dateien**. Auch spätere freilassbare Länder sind enthalten. **ALN, ZOM, C01 und ADS wurden nicht verändert.** Der Nutzer möchte diese Sonder-Tags vor einer möglichen Änderung selbst beurteilen.

Die vollständige Übersicht steht in [COUNTRIES.md](COUNTRIES.md). Die dortigen Namen sind die Bezeichnungen der Länderdateien, keine Behauptung über den damaligen Staatsnamen. Insbesondere repräsentieren SOV die Sowjetunion, SER Jugoslawien, CZE die Tschechoslowakei, GER die Bundesrepublik und UAE die Vertragsstaaten vor der Föderation.

## Recherchierte Felder

**Währung:** Ein vorhandener nativer `reserve_currency`-Eintrag und dessen korrekter `no_foreign_reserve`-Wert. MD hat weiterhin eine einzige Auswahl. Sie wird als außenwirtschaftliche Reserve-/Zahlungsbindung mit den bereits vorhandenen Landeswährungs-Ausnahmen abgebildet. Beispielsweise bleibt Indien im belegten Sterling-Kontext, die Sowjetunion im Rubel-System, Frankreich beim vorhandenen Franc und Italien bei der vorhandenen Lira. Ein solcher Eintrag bedeutet weder, dass die Bevölkerung mit dieser Reservewährung bezahlt, noch dass sämtliche Reserven aus dieser Währung bestehen.

Für Franken-/CFA-Zahlungsräume ohne erlaubte native Reserveoption bleibt eine Modellgrenze: Das Projekt erfindet keine US-Bindung und schreibt keinen France-only-Franc auf andere Länder. Die genaue Begründung steht je Land in `currency.json`. Sie erscheint nicht als Zusatzhinweis im Spiel. Euro, Bitcoin und der erst 1994 eingeführte brasilianische Real werden nicht auf 1970 zurückdatiert. Es wurden keine vermeintlich exakten Reservequoten oder historischen Werte für MDs abstrakte `currency_strength` erfunden.

**Religion:** Eine bestehende native Religionskategorie anhand der kulturellen und institutionellen Verhältnisse um 1970. Grundlage sind unter anderem die 1970-Beobachtungen des World Religion Dataset und zeitnahe amtliche Zählungen. Konfession, staatliche Religionspolitik und universelle Zustimmung werden nicht gleichgesetzt. Die großen Unionen werden als Ganzes bewertet. SOV und SER erhalten deshalb pluralistische Gesamtprofile; regional freilassbare Tags können andere Kategorien erhalten. Die native Kategorie `christian` fasst katholische und protestantische Traditionen zusammen. `buddism` ist die tatsächliche Schreibweise der nativen ID.

**Innere Machtgruppen:** Drei recherchierte, repräsentative native Gruppen je Länderdatei. Die bereits in besonderen Länderprogrammen vorhandenen Gruppen werden zusätzlich erhalten. Es wird kein willkürliches Drei-Gruppen-Limit über die Sowjetunion, DDR oder andere eigens verfasste nationale Systeme gelegt. Vorhandene verfasste Meinungswerte bleiben erhalten, einschließlich null. Nur fehlende Werte starten bei MDs neutralem Wert 50. Diese Zahl ist eine Spielvoreinstellung und keine behauptete historische Zustimmungsmessung.

## Quellen und Aussagegrenzen

Die Quellenkataloge enthalten pro Land Begründung, Verknüpfung, Evidenzstatus und Grenzen:

- [currency.json](currency.json): IMF-Berichte 1969/1970, Bank-of-England-Archiv und Geschäftsberichte, zeitgenössische OECD-/Weltbank-Berichte sowie Zentralbank- und Clearing-Institutionen. [currency_RESEARCH.md](currency_RESEARCH.md) und [currency_secondary_review.md](currency_secondary_review.md) erläutern die Zuordnung.
- [religion.json](religion.json): World Religion Dataset, UN Demographic Yearbooks 1971/1973 und weitere amtliche/historische Quellen. [religion_notes.md](religion_notes.md) nennt Zählungsjahre, Seiten und regionale Grenzen. Die 1970-Beobachtung ist keine weltweit am 1. Januar durchgeführte Volkszählung.
- [factions.json](factions.json): zeitgenössische OECD-, ILO-, diplomatische und institutionelle Quellen. [factions_notes.md](factions_notes.md) trennt direkt belegte Institutionen von breiteren strukturellen Zuordnungen. Der CIA-Factbook-Vergleich 1973 wird nicht als Beweis verwendet, dass ein erst späterer Regierungswechsel bereits 1970 stattgefunden hätte.

Bei späteren Staaten und Organisationen wird die tatsächliche Gesellschaft ihres Gebiets im Jahr 1970 zugrunde gelegt. Beispielsweise erhalten spätere Taliban-, Hamas- oder Kartell-Tags keine rückdatierten modernen Organisationen. Ein solcher territorialer Startwert behauptet nicht, dass deren spätere Regierung schon 1970 bestand.

Keine zusätzliche sichtbare Kennzeichnung, kein Ersatzwert-Hinweis und keine Recherche-Meldung werden ins Spiel eingefügt. Normale englische Institutionsnamen ersetzen lediglich eindeutig anachronistische Anzeigenamen.

## Integration und Leistung

Die Ergänzungen sind durch Projektkommentare in den betroffenen History-Blöcken abgegrenzt. Alle ursprünglichen Bytes außerhalb dieser Ergänzungen bleiben erhalten. Die drei Dateien mit zwei vorhandenen `1970.1.1`-Blöcken erhalten in beiden Blöcken dasselbe Profil. Kein bestehender History-Block wird verschoben oder zusammengelegt.

Ein `has_start_date`-basierter 1970-Guard isoliert die neuen Einträge vom 1985-, 2000- und 2017-Bookmark. Er benötigt kein erst später gesetztes Startup-Flag. Die History-Änderung gilt beim Erstellen eines neuen 1970-Spielstands; bestehende Saves werden nicht rückwirkend umgeschrieben.

Die initialen Meinungswerte werden vor Gruppenänderungen gesichert und danach wiederhergestellt. Bereits vorhandene Gruppen werden nicht erneut hinzugefügt. Dadurch ist die Ergänzung auch gegenüber nativen `on_add`-Resets und der Bereinigung noch inaktiver Gruppenvariablen robust. Bei einem bestehenden Land mit neu hinzugekommenen Gruppen werden ihre vorhandenen nativen Modifikatoren nach der Wiederherstellung einmal initialisiert. Noch nicht bestehende Freilassungs-Tags behalten ihre History-Werte; ihre späteren Modifikatoren übernimmt MDs vorhandenes `ingame_startup_nations_effect` mit `setup_init_factions`. Eine zusätzliche volle Wirtschaftsberechnung wird nicht ausdrücklich aufgerufen.

Es gibt keine neuen täglichen, wöchentlichen oder monatlichen Simulationsabläufe, Länder-/Staatenscans, Arrays oder Schuldenkonten. Die bestehenden MD-Start- und Monatsberechnungen bleiben maßgeblich. Historische Gruppen müssen beim Start ihre normalen nativen Modifikatoren erhalten; das ist einmalige Initialisierung und keine neue laufende Simulation. Es wurde keine Engine-Zeitmessung durchgeführt.

30 ausgewählte oder bereits verfasste Fraktionsnamen verwenden eine kleine englische Namensroute für das 1970-Bookmark. Außerhalb davon wird der exakte bestehende native Text verwendet. Iran behält zusätzlich die native regierungsabhängige Umschaltung nach einem späteren schiitischen Regimewechsel; die imperialen Namen gelten nur für das entsprechende imperiale Profil. Die Namensroute hat keine Simulations-Callbacks.

## Überprüfung und Reproduktion

```powershell
python -B tools/world_1970_society/implement.py
python -B tools/world_1970_society/implement.py --apply
python -B tools/world_1970_society/labels.py
python -B tools/world_1970_society/test_history_patch.py
python -B tools/world_1970_society/validate.py
python -B tools/world_1970_society/currency_validate.py --actual
python -B tools/world_1970_society/factions_validate.py
```

`implement.py` ohne `--apply` erzeugt einen geprüften Plan. `--apply` schreibt ausschließlich die abgegrenzten History-Ergänzungen und lehnt unerwartete zwischenzeitliche Änderungen an den Ursprungsdateien ab. Erneute Ausführung ist idempotent. Die vier offenen Tags werden ausdrücklich vom Schreiben ausgeschlossen und gegen ihre ursprünglichen Hashes geprüft.

`inventory.json` enthält die Ausgangshashes aller 397 Dateien. `profiles.json` enthält den gemeinsamen Datensatz, `changes.json` die Hashes der 393 bearbeiteten Dateien. Entfernt man ausschließlich die markierten Ergänzungen, ergeben sich wieder exakt die Ausgangshashes. Andere Änderungen aus früheren Arbeiten werden damit nicht zurückgesetzt.

Die Prüfberichte `validation.json`, `currency_validation.json` und `factions_validation.json` dokumentieren die aktuelle Kontrolle. Die fokussierten Tests prüfen unter anderem tatsächliche native Fraktions-`on_add`-/Cleanup-Befehle, Nullwerte, doppelte Aufrufe, doppelte Datumsblöcke, unveränderte spätere Bookmarks, Encoding und bytegenaue Wiederherstellung. Dies ist kein vollständiger Interpreter aller MD-Dateien und kein HOI4-Multiplayer-/OOS-Test. Die bestehenden sowjetischen Industriegruppen sind ein dokumentierter verfasster Altbestand trotz der allgemeinen nativen Tagbeschränkung; die neue repräsentative Auswahl führt diese Ausnahme nicht neu ein.

## Herkunft und Rechte

Recherchezuordnungen, Integrationswerkzeuge und neue zeitgenössische englische Bezeichnungen wurden im Auftrag des Nutzers für IMPERIA COLD WAR erstellt. Eine neue Weiterverteilungslizenz wird damit nicht festgelegt. Native MD-Logik und vorhandene Autorenhinweise bleiben erhalten. Die ursprüngliche Fraktions-Lokalisierung nennt Birdy und Killerrabbit. Individuelle Autoren und blockbezogene Lizenzen weiterer bestehender MD-/Projektinhalte sind, soweit nicht ausdrücklich belegt, unbekannt.

Die externen Quellen bleiben bei ihren Herausgebern. Das Paket enthält keine kopierten Quellenbilder, keine vollständigen Quellen-PDFs und keine Rohkopie des eingeschränkt weiterverteilbaren World Religion Dataset. Die abgelegten Kategorien und Begründungen sind eigene qualitative Spielzuordnungen. Quelle, Autor, Datum, URL, Zugriffsgrenzen und bekannte oder unbekannte Nutzungsrechte stehen in den jeweiligen Quellenkatalogen. Der Projektmarker begründet keine Eigentumsrechte an fremdem Material.
