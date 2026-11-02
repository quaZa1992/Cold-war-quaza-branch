# IMPERIA COLD WAR — Konkretes Beispiel für Reservebindung und Dollarschulden

Stand: 23. Oktober 2026. **Inaktiver, ausführbarer Codeentwurf.** Die Dateien unter `runtime/` liegen außerhalb der von HOI4 geladenen Verzeichnisse. Die laufende Wirtschaft wird durch dieses Paket nicht umgebaut. Die bereits ergänzten Franc-/Lira-Optionen bleiben der bisherige, getrennte Arbeitsschritt.

## Was dieses Beispiel abbildet

Frankreich kann den Franc als Landeswährung führen und trotzdem Dollarreserven sowie Dollarverbindlichkeiten besitzen. Dafür verwaltet der Entwurf drei unabhängige Werte:

| Wert | Beispiel | Bedeutung |
|---|---:|---|
| `COLDWAR_MON_reserve_usd_share` | 0.8 | Dollaranteil der Währungsreserven, nicht der nationalen Geldmenge |
| `COLDWAR_MON_new_usd_share` | 0.6 | Dollaranteil tatsächlich neu aufgenommener Schulden laut gesonderter Finanzierungsvereinbarung |
| `COLDWAR_MON_usd_principal` | 40 | Bereits bestehender Dollar-Schuldenbestand in MDs Milliarden-Rechnungseinheit |

`debt` und `treasury` bleiben die maßgeblichen MD-Konten. Das Beispiel führt kein zweites Geldsystem ein. Der Rest des Schuldenbestands wird in dieser ersten Stufe ohne eigenes Währungsrisiko behandelt. Es ist ein Modell **Dollar / übrige Finanzierung**, noch kein vollständiges Portfolio für Pfund, Mark, Franc, Lira und Gold.

Die Dollar-Schuldenvariable ist ein Teilbestand des MD-Schuldenkontos. Sie ist keine Anleihedatenbank und kein separat zum Tageskurs bewerteter Dollar-Nennbetrag. Auch MDs `currency_strength` bleibt ein abstrakter Belastungsindex und wird nicht als historischer Franc-Dollar-Wechselkurs ausgegeben.

## Durchgerechnetes Beispiel

Angenommen: 100 Mrd. GDP, 100 Mrd. Schulden, davon 40 Mrd. Dollarverbindlichkeiten, Währungsstärke 0.8. Alle Länderwerte hier sind **erfundene Testwerte**, keine Rekonstruktion französischer Staatsfinanzen.

Der währungsbedingte Faktor des MD-Schuldendienstes ergibt sich aus dem tatsächlichen Schuldenmix:

```text
Dollar-Schuldenanteil = 40 / 100 = 0.4
Dollar-Faktor = clamp(1 / Währungsstärke, 0.5, 2)
Schuldendienst-Faktor = 1 + (Dollar-Faktor - 1) * Dollar-Schuldenanteil
                     = 1 + (1.25 - 1) * 0.4
                     = 1.10
```

MD berechnet seine Zinsen weiterhin selbst. Der Faktor 1.10 bedeutet hier 10% zusätzlichen Schuldendienst gegenüber dem ansonsten gleichen MD-Kredit; er ist kein neuer Zinssatz von 10%.

Der Beschluss **Authorise Reserve Diversification** setzt einen alternativen Zahlungsverbund voraus. Er kostet einmalig 75 PP und $0.025bn. Über 24 Monatsprüfungen sinkt die Dollarreservequote von 80% auf 40%. Währenddessen läuft eine Verwaltungsbewilligung über MDs Wochenbudget:

```text
Wochenkosten = clamp(GDP * 0.00002, 0.001, 0.025) Milliarden
Bei GDP 100: $0.002bn pro Woche = $2 Mio. pro Woche.
```

Diese Kosten, Grenzen, 24 Monate und die Zielquote sind entworfene Spielbalance. Die Wochenrate entspricht im Beispiel etwa 0.104% GDP pro 52 Wochen. Die endgültige Balance braucht eigene RP-Spieltests.

| Größe | Vor Beschluss | Nach 24 Monatsprüfungen, ohne weitere Kredite/Tilgungen |
|---|---:|---:|
| Landeswährung | French Franc | French Franc |
| Dollarreservequote | 80% | 40% |
| Bestehende Dollarverbindlichkeiten | 40 Mrd. | 40 Mrd. |
| Dollaranteil künftiger Kredite | 60% | 60% |
| MD-Schuldendienst-Faktor bei Stärke 0.8 | 1.10 | 1.10 |
| Gewichtung des bestehenden MD-Dollar-Netzwerkvorteils | 0.8 | 0.4 |
| Zusätzliche Wochenbewilligung | 0 | 0 nach Abschluss; währenddessen 0.002 Mrd. |

Ein Menüwechsel beseitigt somit keine Dollarverträge. Weniger Dollarreserven reduzieren zugleich den aus MDs bestehender Dollarprojektion abgeleiteten Handels-/Investitionsvorteil. Für den nicht in Dollar gehaltenen Anteil erfindet dieses Beispiel keinen automatisch gleichwertigen Ersatzbonus.

Ein neuer nativer Kredit mit 10 Mrd. Auszahlung und 10.1 Mrd. Schuldenzugang erhöht bei 60% Dollarfinanzierung den Dollarbestand um **6.06 Mrd.** Die native Gebühr wird damit berücksichtigt. Eine spätere Tilgung von 10% des Gesamtbestands reduziert beide Schuldenanteile proportional. Eine gesondert akzeptierte neue Finanzierungsvereinbarung kann den Anteil zukünftiger Kredite ändern; sie schreibt alte Verträge nicht um.

## Warum ein Staat im Dollarverbund bleibt

Der Nutzen kommt aus bestehendem Zahlungsverkehr, Finanzierung und Vertragsbestand. Im Beispiel entsteht deshalb kein kostenloser Ausstieg durch die Wahl einer Landeswährung:

1. Die Zentralbank kann ohne bestätigten alternativen Zahlungszugang keinen Umschichtungsbeschluss ausführen.
2. Der Aufbau kostet politische Autorität, Geld und Zeit. Ein Wiedereinstieg in denselben Beschluss ist während der Laufzeit und der ursprünglichen 730-Tage-Sperre ausgeschlossen.
3. Der Dollar-Netzwerkvorteil sinkt mit der erreichten Reservequote. Die Umstellung des Reservemixes allein bietet keinen kostenlosen Gegenbonus.
4. Bestehende Dollarverbindlichkeiten und ihr Wechselkursrisiko bleiben erhalten. Auch der Dollaranteil neuer Kredite bleibt unverändert, bis eine **andere, tatsächlich angenommene Kreditvereinbarung** gilt.
5. Geht der alternative Zahlungszugang verloren, endet das Programm bei der erreichten Quote. Es gibt keine Erstattung, keinen sofortigen Sprung zum Ziel und keine neue freie Umschichtung.

Ein vollständiger Ausstieg oder die Rückkehr zum Dollar ist in diesem begrenzten Beispiel noch kein auswählbarer Beschluss. Dafür wären dieselben Vertrags-, Kosten- und Laufzeitregeln in gesonderten Vereinbarungen anzuwenden. Politisch gewünschte Entdollarisierung bleibt möglich; die Institutionen müssen sie tragen.

## Dateien und Ausführung

- `runtime/common/scripted_effects/COLDWAR_MON_reserves.txt`: Initialisierung, Schuldenbuchung, Finanzierungsbedingungen, monatliche Reserveumschichtung, Wochenkosten und gewichtete Reserveteilnahme.
- `runtime/common/scripted_triggers/COLDWAR_MON_reserves.txt`: gemeinsame Ausführungsbedingungen und ausdrücklich bestätigte Startwerte.
- `runtime/common/decisions/` und `runtime/localisation/english/`: native Beschlussstruktur und englische Treasury-/Central-Bank-Texte. Keine deutschen Spieltexte.
- `integration.py`: liest die aktuellen MD-Funktionen und fügt die Beispielaufrufe **nur im Arbeitsspeicher** ein. Die Ausgabe zeigt die konkrete Einbindung in echte MD-Kreditfunktionen.
- `INTEGRATION.md`: Einbaupunkte, Startwerte, Zustimmung und Grenzen vor einer Live-Aktivierung.
- `runtime_model.py` und `test_example.py`: strikter Interpreter für den verwendeten Script-Ausschnitt und Tests gegen dessen tatsächliche AST, einschließlich ausgewählter nativer MD-Funktionen.
- `live_inputs.json`: Hashes der unveränderten Live-Wirtschaftsdateien zum Beginn dieses Entwurfs.

Aus dem Mod-Hauptverzeichnis:

```powershell
python -B tools/reserve_currency_example/integration.py
python -B tools/reserve_currency_example/test_example.py
```

`integration.py` schreibt ausschließlich auf stdout. Es kopiert oder verändert keine Live-Dateien. Die Tests schreiben nur den Prüfbericht in diesem Beispielpaket.

## Leistung und Multiplayer-Zustand

Der Entwurf nutzt MDs vorhandenen Monatsablauf und den vorhandenen Reserven-Recount. Er ergänzt keinen täglichen oder wöchentlichen Länder-/Staatenscan. Ein gespeicherter globaler Monatszähler wird einmal innerhalb des bestehenden MD-Monatsguards erhöht. Jedes Land verarbeitet jede Zählerstufe höchstens einmal. Er wird beim Laden nicht zurückgesetzt; `global.month` eignet sich dafür nicht, weil MD diesen Wert in `on_startup` auf 1 setzt.

Monatsfortschritt, Vorschau und Zahlung sind getrennt. Das Aktualisieren abgeleiteter Werte bewegt keine Reservequote und zieht kein Geld ab. Die Wochenkosten werden nach dem nativen Zurücksetzen des Ausgabenakkumulators genau einmal addiert; die eigentliche Geldbewegung bleibt beim MD-Budget. Ein angenommener Spielerbeschluss darf einmal `ingame_update_setup` ausführen. Monatliche Helfer lösen keine zusätzliche vollständige Wirtschafts-/Staatenberechnung aus.

Die globalen MD-Dollarprojektionen werden im vorhandenen globalen Monatsteil berechnet, bevor die Länder ihre neue Quote verarbeiten. Alle Länder nutzen denselben gespeicherten Stand. Geänderte Quoten gehen deshalb erst beim folgenden Recount in die globale Netzwerkprojektion ein. Dieser bewusste Monatsverzug vermeidet einen neuen Recount nach jedem Land oder jedem Klick.

Das folgt der im Projekt dokumentierten Trennung von Simulation, teurer Aktualisierung und sichtbarer Oberfläche in `tools/west_germany_1970/PERFORMANCE.md`. Eine spätere eigene GUI soll länderspezifische Dirty-Variablen verwenden und Details nur für Menschen mit geöffnetem Fenster aufbauen.

Der aktuelle Prüfbericht enthält **32 bestandene Tests**. Darunter: native Gebühren und Kreditgrenzen, automatische Finanzierung, manuelle/AI-Tilgung, Schuldenschnitt, doppelte Klicks, fehlende Mittel, verlorener Zahlungszugang, Nullschulden, numerische Begrenzung, 24 Monatsstufen mit Rundung sowie Fortsetzung gespeicherter Modellzustände in umgekehrter Länderreihenfolge. Der modellierte aktive Monatslauf benötigt 43 AST-Operationen, ein inaktiver 29, ein wiederholter Monatsaufruf 4. Das sind Interpreter-Zählungen einschließlich des globalen Zählerschritts, keine HOI4-Zeitmessungen.

**Ein echter HOI4-Save/Load- und Multiplayer/OOS-Test wurde nicht durchgeführt.** Der Interpreter ersetzt unter anderem die vollständige native Wirtschaftsaktualisierung durch eine begrenzte Testfunktion. Bei unbekannten Scriptoperationen bricht er ab. Er prüft die gezeigten Buchungen und Guards, nicht den gesamten Engine-Ablauf. Vor Live-Nutzung sind die Integrationslücken in `INTEGRATION.md` zu schließen.

## Historische Grundlage und Abstraktion

Die Trennung folgt historischen Institutionen: Bretton Woods verband nationale Währungen mit dem Dollar; es ersetzte sie nicht durch Dollar als allgemeine Landeswährung. Die Federal Reserve dokumentiert die Dollarabwicklung sowie Swap-Vereinbarungen mit Frankreich, Italien und weiteren Zentralbanken seit 1962. Der Entwurf leitet daraus die Voraussetzung eines alternativen institutionellen Zahlungszugangs ab. Eine fest vorgeschriebene 24-Monatsfrist oder die Beispielkosten liefert diese Quelle nicht. [Federal Reserve History, Sandra Kollen Ghizoni, „Nixon Ends Convertibility of U.S. Dollars to Gold and Announces Wage/Price Controls“](https://www.federalreservehistory.org/essays/gold-convertibility-ends).

Die IMF-Studie beschreibt Reservehaltung, internationale Zahlungen und ausländische Finanzierung als miteinander verbundene, aber unterschiedliche Funktionen. Sie untersucht die Beständigkeit von Reserveanteilen und Finanzverbindungen. Daraus ist hier die langsame Umschichtung samt fortbestehender Kreditbindung abgeleitet; die Studie wird nicht als Schätzung konkreter französischer oder italienischer Startquoten verwendet. [IMF staff team led by Alina Iancu, „Reserve Currencies in an Evolving International Monetary System“, DP/20/02, 2020, besonders Kapitel 2–3](https://www.imf.org/-/media/files/publications/dp/2020/english/rceimsea.pdf).

## Herkunft und Rechte

Entwurf und Tests: im Auftrag des Nutzers für IMPERIA COLD WAR erstellt. Eine gesonderte Veröffentlichungs-/Weiterverteilungslizenz für diese neuen Dateien wurde nicht festgelegt. Das Paket enthält keine neu übernommenen Bilddateien. Die Beschlussdefinition verweist auf das bestehende native politische Symbol; dessen individueller Urheber und separate Weiterverteilungsrechte sind hier unbekannt.

`integration.py` liest bestehende Millennium-Dawn-/Projektdateien lokal; die eingefügten Buchungsaufrufe sind der hier erstellte Beispielentwurf. Native Funktionen werden für die Tests im Speicher abgeleitet. Die native Logik und die Prüfparser-Datei `tools/spain_1970_v2/script_ast.py` behalten ihre vorhandenen Urheberhinweise; individuelle MD-Autoren und die konkrete Lizenz der jeweiligen lokalen Ursprungsblöcke sind in diesem Paket nicht abschließend zugeordnet und daher unbekannt. Quellen werden nicht durch den Projektmarker neu lizenziert. Die historischen Webseiten/Papiere werden referenziert, nicht in das Paket kopiert.
