# Irak: Fokusbelohnungen statt Verwaltungsmenüs

Stand: 21. Oktober 2026. Im Mod eingebaut; noch kein HOI4-Spieltest.

## Umfang

| Inhalt | Vorher | Nachher |
| --- | ---: | ---: |
| Allgemeine Irak-Entscheidungen | 88 | 25 |
| Allgemeine Irak-Ereignisse | 129 | 65 |
| Laufende Golfkrisen-Entscheidungen | 12 | 12 |
| US-Golfkrisen-Entscheidungen | 50 | 48 |
| Sichtbare Irak-Foki | 410 | 410 |

Die 16 ausgeblendeten Kompatibilitäts-Fokus-IDs bleiben ebenfalls erhalten. Positionen, Verbindungen und Ausschlüsse wurden gegenüber dem gesicherten Spielcode nicht verändert. Das separate, noch nicht freigegebene Saddam-Konzept wird hierdurch nicht eingebaut.

## Was direkt aus dem Fokus kommt

- Verfassungswege setzen ihre jeweilige Verfassungsordnung selbst um. Ein zusätzliches Verfassungsmenü entfällt.
- **A Political Amnesty** setzt politische Garantien um und löst noch erreichbare Fälle lebender Gefangener. Todesvermerke und historische Fristen bleiben wirksam. Die dauerhaften Kosten der Garantien sind im Fokus sichtbar.
- **National Front** und der entsprechende kommunistische Weg bilden die tatsächliche innerirakische Koalition. Der Regierungsführer wird dadurch nicht automatisch ausgetauscht.
- **The Coalition Charter** gibt unter anderem **+5% zivile Fabrikproduktivität** bei **+2% Sozialausgaben**; der frühere zusätzliche Arbeitscharta-Klick entfällt.
- **Exclusive Party State** gibt **+8% Mobilisierungsgeschwindigkeit**, **+8% Kommandopunktgewinn**, **+15% politische Driftverteidigung** und einmalig **25 Kommandopunkte** bei **−3% Forschungsgeschwindigkeit**. Die konkurrierende Front bleibt ausgeschlossen.
- **Defence Readiness** bezahlt sein 90-Tage-Programm selbst: **+4% Organisation**, **+4% Erholungsrate**, **+4% Armeepersonalkosten**, zusätzlich zu den bestehenden Fokusbelohnungen.
- **Gulf Commercial Office** errichtet einmalig **1 Büroindustrie in Basrah** und stärkt die Bürosteuereinnahmen. Es ist kein erforderliches Kuwait-Zustimmungsereignis mehr.
- Mehrere reine Beziehungsgespräche werden zu heimischen Beschaffungs-, Verkehrs-, Verwaltungs- oder Handelsprogrammen mit unmittelbaren irakischen Belohnungen.
- Der Friedensdividenden-Fokus beendet den aktiven Notstandshaushalt. Bereits eingegangene befristete Personalrechnungen laufen weiter.
- Nachträgliche Menüs zum beliebigen Wechseln bereits ausgeschlossener Verfassungs-, Armee- und Wirtschaftsprogramme entfallen.

## Was bewusst als Entscheidung/Ereignis bleibt

- Eine echte Führungswahl, Parteiwechsel und Wahlen bleiben bewusste politische Handlungen.
- Kredite, Rüstungslieferungen, Ölverträge, Grenz- und Autonomieabkommen behalten echte Zustimmung der betroffenen Gegenpartei. Der passende Fokus eröffnet das Angebot unmittelbar. Bei mehreren möglichen Partnern bleibt die Partnerauswahl.
- **Reopen Diplomatic Negotiations** bündelt spätere Versuche in einem einzigen kostenlosen Zugang. Fehlende, bereits gebundene oder aktuell unzulässige Gegenparteien können dadurch nicht zur Zusage gezwungen werden.
- Ein gemeinsamer Rückzahlungskanal ersetzt mehrere fast gleiche Kreditmenüs; echte Verpflichtungen und Treasury-Grenzen bleiben bestehen.
- Kriegsermächtigung, zeitlich begrenzte Iran-Offensiven, Vermittlung und Sanktionen bleiben dort aktiv wählbar, wo der aktuelle Kriegsverlauf entscheidend ist.
- Die Golfkrisen-Mechanik mit laufenden Krediten, Kriegskosten, Kuwait und US-Intervention bleibt bestehen. Bei den USA entfallen nur zwei doppelte Zugangsmenüs; die konkreten Handlungen bleiben erreichbar.

## Ältere Spielstände

Neue Belohnungen werden bei einer bloßen Regierungs- oder Programmaktualisierung nicht erneut ausgezahlt. Bereits gelieferte Fabriken, Ausbildung und andere Einmalbelohnungen werden angerechnet. Zusätzliche Kosten werden einmalig eingefroren; eine bereits ausgestellte Rechnung behält ihre GDP-Basis.

Nur ältere, bereits abgeschlossene Programme können eine passende Nachlieferung im bestehenden Projektmenü erhalten. Die 53 möglichen Kompatibilitätsaktionen sind keine 53 neuen regulären Irak-Entscheidungen und erscheinen nicht pauschal in einem neuen Spiel.

Bereits umgesetzte Front-, Legalisierungs- und Übergangsabkommen erhalten Kostenanrechnung. Die frühere Gefangenenprüfung speicherte keinen eindeutigen Zahlungsbeleg; vorhandene Freilassungs-/Schutzresultate werden deshalb zugunsten des Spielers angerechnet. Eine noch offene, entfernte Gefangenenprüfung erstattet ihren reservierten politischen Einsatz.

## Prüfung und Grenzen

- 20 Tests gegen die erzeugten Skriptbäume bestanden: Zahlungsgrenzen, einmalige Auszahlung, fremde Zustimmung, Angebotswiederaufnahme, Fristen/Todesvermerke, Regierungsaktualisierung und mehrere alte Spielstandsrevisionen.
- Zweite Generierung vor dem letzten reinen Textdurchgang: alle 22 begrenzten Ausgaben bytegleich; Script-/Lokalisierungskodierungen korrekt.
- Begrenzte Integrationsprüfung: 426 Fokus-IDs, 410 aktive Foki, Positionen, gruppierte Voraussetzungen, 12.790 eigene Skriptaufrufe und verwendete Modifier gegen lokale MD-/Engine-Definitionen geprüft; keine fehlenden Verweise.
- Der alte globale Integrationsprüfer vergleicht USA mit einem älteren Projektstand und meldet dessen zwischenzeitliche Änderungen. Der neue Aufruf `validate.py --streamlining` vergleicht diesen Eingriff ausdrücklich mit seinem tatsächlichen Vorher-Snapshot und bestätigt die unveränderten USA-Foki. Fremde Änderungen werden nicht zurückgesetzt.
- Kein Test von HOI4-Oberfläche, realer Engine-Ausführung, Save/Load oder einer laufenden Multiplayer-Sitzung. Die Testausführung prüft unsere Skripte; native Spielsysteme sind markierte Schnittstellen.

Technische Belege: `IMPLEMENTATION_REPORT.json`, `VALIDATION_REPORT.json`, `INDEPENDENT_REWARD_REVIEW.md`; gesicherter Ausgangscode in `before.zip`.
