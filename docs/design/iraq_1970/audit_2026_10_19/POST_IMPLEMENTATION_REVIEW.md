# Gegenprüfung der tatsächlich installierten Irak-/US-Revision

**Status nach Korrektur:** Alle fünf unten dokumentierten Befunde wurden mit Revision `audit_2026_10_19_v2` im Generator und in den geladenen Mod-Dateien behoben. [POST_REVIEW_FIXES.md](POST_REVIEW_FIXES.md) beschreibt die Korrekturen und die erneuten Gegenprüfungen. Der folgende Text bleibt als ursprünglicher Prüfstand erhalten.

19. Oktober 2026, ursprüngliches Ergebnis vor der Korrektur: **Die Einbindung war korrekt, die Umsetzung enthielt fünf bestätigte Fehler.** Die damaligen bestandenen Standardprüfungen deckten diese Gegenbeispiele nicht ab. Die Prüfskripte erzeugten teilweise Code im Speicher; sie hatten keine Gameplaydateien geändert oder neu im Mod gespeichert. Ein neuer nativer Spielstart wurde in dieser Gegenprüfung nicht ausgeführt.

Geprüftes Manifest: `ccf8e4ee94bb72af3ff784817ed205df106ac30c6a384adb0057a56a201502b2`. Alle 103 generierten Dateien und neun Integrationen entsprechen diesem Manifest. Drei unabhängige Gegenprüfer haben jeweils fremde Teilimplementierungen gelesen. Die neuen Gegenbeispiele führen die installierte AST-Logik aus; native Diplomatie, Anzeige und Mehrspieler-Synchronisation bleiben ausdrücklich Grenzen der Interpreter.

## 1. P2 – Die Kassenprüfung beim US-vermittelten Autonomievertrag ist falsch gruppiert

**Installierte Stellen:** `events/COLDWAR_USA_gulf_events.txt:647` und `:712`. **Quelle:** `tools/iraq_1970/usa_module.py:642` und `:650`.

Das OR enthält drei unabhängige Alternativen: bereits bezahlt, Kostenmodus nicht übersprungen oder ausreichend Geld. Bei einem normalen Irak ist die zweite Alternative unabhängig vom Kontostand wahr. Außerdem fehlen eine positive BIP- und eine positive Rechnungsbedingung für die erste Zahlung.

Die tatsächlichen Kategorie-, Entscheidungs- und Antwortbedingungen lassen die folgenden Fälle zu; es handelt sich nicht um einen illegal direkt aufgerufenen Annahmehelfer:

| Irak zu Beginn | Rechnung | Tatsächlicher Vertragsabschluss |
|---|---:|---|
| BIP 10, Staatskasse 0,1 | 0,2 | Staatskasse −0,1; Zahlung als erledigt markiert; KUR erhält den autonomen Unterstaatstatus |
| BIP 10, Staatskasse 10, `MD_skip_treasury_cost` | 0,2 | Staatskasse unverändert 10; trotzdem Zahlung markiert und Autonomie hergestellt |
| BIP 0, Staatskasse 10 | 0 | Staatskasse unverändert 10; trotzdem Zahlung markiert und Autonomie hergestellt |

Der zweite Fall wurde mit dem tatsächlichen nativen `modify_treasury_effect` aus `common/scripted_effects/00_budget_effects.txt:1487` ausgeführt: Dieser überspringt die Zahlung bei gesetztem Flag. Im ersten Fall entsteht zunächst eine negative Kasse, keine unmittelbare Schuld. Bleibt sie unverändert bis zur wöchentlichen MD-Defizitaufnahme, kann daraus eine tatsächliche zusätzliche Staatsverschuldung entstehen. Das ist keine im Angebot ausgewiesene oder separat vereinbarte Kreditfinanzierung. Die 25 PP sind der deklarierte native US-Entscheidungspreis; dessen Engine-Abzug wird vom Interpreter nicht simuliert.

**Korrekturvertrag:** Bereits belegte Zahlung als eigene Ausnahme behalten; der unbezahlte Zweig benötigt gemeinsam positive BIP/Rechnung, ausgeschalteten Skip-Modus und ausreichende Kasse. Sowohl die Angebotserstellung als auch die spätere tatsächliche Ratifikation müssen dieselben Bedingungen prüfen.

## 2. P2 – Eine akzeptierte externe Schutzverpflichtung kann am nächsten Tag verschwinden

**Installierte Stellen:** `common/scripted_triggers/COLDWAR_USA_gulf_triggers.txt:246`, `common/scripted_effects/COLDWAR_USA_gulf_effects.txt:1555`, `:1175` und `:1184`. **Quelle:** `tools/iraq_1970/usa_module.py:437` und der neue externe Verpflichtungsabschnitt um `:827`.

Ein unabhängiger, friedlicher kurdischer Akteur mit ungelöster Nordfrage, offener Route, frischer Gastgeberzustimmung und tatsächlich eingesetzten Flugzeugen kann die externe US-Verpflichtung erhalten, ohne dass gerade eine akute humanitäre Krise besteht. Kategorie, Entscheidung und Antwort sind zulässig. Die Annahme setzt aktuelle Politik 2, Schutzdauer 90 Tage und die neue Garantie.

Der Luftschutzstart verlangt jedoch zusätzlich die akute humanitäre Krise. Er startet deshalb nicht. Die tägliche Schutzfinanzierung verlangt dieselbe zusätzliche Krise und setzt die Schutzdauer am folgenden US-Tag auf null; die Garantie verschwindet. Die angekündigte 90-Tage-Verpflichtung hält damit weniger als einen Tag, obwohl Zugang, Zustimmung und Finanzierung vorhanden sind.

```text
decision: category=True, visible=True, available=True, declared cost=25 PP
humanitarian_crisis=False; recipient acceptance=True
after acceptance: policy=2, protection_days=90, air=False, guarantee=True
after one US tick: protection_days=0, guarantee=False
```

**Korrekturvertrag:** Anforderung, Ratifikation, Luftaktivierung und fortlaufende Finanzierung brauchen eine konsistente Grundlage. Der neue externe Schutzvertrag darf nicht stillschweigend von einer zusätzlichen Bedingung des älteren humanitären Safe-Haven-Programms aufgehoben werden. Ob außerhalb einer akuten Krise schon das Angebot ausgeschlossen werden soll oder die gültige Schutzvereinbarung selbst die laufende Grundlage ist, muss beim Fix ausdrücklich mit dem freigegebenen 90-Tage-Vertrag abgeglichen werden.

## 3. P2 – Ein bereits eingefrorenes Angebot eines zusammengelegten Projekts verliert seine Preisgrundlage

**Installierte Stellen:** `common/scripted_effects/COLDWAR_IRQ_1970_audit_migration.txt:1723`, `:2237` und `common/decisions/COLDWAR_IRQ_1970_pending.txt:18571`. **Quelle:** `tools/iraq_1970/audit_migration.py:54`, `:75` und `:85`.

Gegenbeispiel eines bestehenden Spielstands: Heavy wurde bei BIP 10 für 0,2 bezahlt. Steel ist abgeschlossen, unbezahlt und pending; seine positive Rechnung ist bereits auf 0,5 eingefroren. Vor der Migration wächst das BIP auf 100.

Die Migration entfernt Steel aus der Warteschlange; eine direkte Steel-Lieferentscheidung existiert nicht mehr. Seine alte Rechnung bleibt als Variable erhalten, wird aber bei der neuen Preisbasis nicht verwendet. Die neue Heavy-Ergänzung rechnet stattdessen 5% des aktuellen BIP minus tatsächlich gezahlte 0,2: **4,8**. Mit den bisherigen 0,5 Kassenmitteln ist der Ersatz sichtbar, aber nicht ausführbar. Bei der Migration selbst wird noch kein Geld abgebucht.

```json
{
  "old_steel_quote": 0.5,
  "old_steel_quoted": true,
  "old_steel_pending_after_migration": false,
  "old_direct_delivery_registered": false,
  "replacement_pending": true,
  "replacement_quote": 4.8,
  "replacement_available_with_treasury_0_5": false
}
```

Aktuelles BIP für bisher nicht angebotene neue Arbeit ist bewusst vorgesehen und hier nicht der Befund. Betroffen ist die vorhandene positive alte Verpflichtung. Der bestehende Vertrag über eingefrorene Rechnungen steht in `docs/design/iraq_1970/implementation/README.md:57`. Die Migration muss dessen historische Preisgrundlage berücksichtigen; die unbezahlten 0,5 dürfen dabei nicht als bereits gezahltes Guthaben angerechnet werden.

## 4. P2 – Die Konzession kann vor Prüfung der zugesagten Infrastruktur bezahlt werden

**Installierte Stellen:** `events/COLDWAR_IRQ_1970_decisions.txt:11256` und `:11324`; spätere Bauprüfung in `common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt:8829`. **Quelle:** `tools/iraq_1970/decisions_module.py:438`.

Die britische Annahme prüft Partei-/Angebotszustand, Geld und Frieden, aber nicht irakisches Eigentum, Kontrolle oder Infrastrukturkapazität in Basra 171. Die Gebühr wird unwiderruflich überwiesen. Erst die spätere Konzessionslieferung prüft den benötigten Bauplatz.

Zwei unabhängig ausgeführte Fälle – Basra gehört Iran beziehungsweise Basra hat keine freie Infrastrukturkapazität – ergeben jeweils: Annahme verfügbar; Irak 1 → 0,9 Mrd.; ENG 10 → 10,1 Mrd.; Vertrag akzeptiert; anschließende Lieferung pending; kein Gebäude geliefert.

Andere Vertragswirkungen bleiben bestehen. Der Befund lautet deshalb nicht, dass überhaupt kein Vertragsnutzen entsteht, sondern dass für die neu zugesagte physische Leistung die ausdrücklich vorgeschriebene Vorprüfung fehlt. `tools/iraq_1970/AUDIT_REWARDS.md:76` verlangt Eigentum/Kontrolle/Kapazität sowohl vor der Vertragszahlung als auch vor der Lieferung. Bei nachträglicher Kapazitätsänderung bleiben die normalen erneuten Lieferprüfungen weiterhin nötig.

## 5. P2 – Front-/Monopol-Vorschau kündigt unbedingte Werte an, die zunächst nicht gelten

**Installierte Stellen:** `common/national_focus/COLDWAR_IRQ_1970_focus.txt:813`, `common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt:588`, `common/scripted_effects/COLDWAR_IRQ_1970_programmes.txt:405` und `:420`. **Quelle:** `tools/iraq_1970/compile.py:139` und `tools/iraq_1970/presentation.py:54`.

National Front zeigt unmittelbar +10% Effizienzaufbau, +4% Forschung und +3% Bürokratiekosten. Der Fokus selbst braucht keine angenommene Frontvereinbarung und soll die Verhandlungen erst freischalten. Die tatsächliche Programmeinrechnung benötigt dagegen `front_contract_active`.

Normale Folge: Regional Command und den Front-Fokus abschließen, anschließend das ICP-Angebot nicht annehmen oder ablehnen. Der Fokus ist erledigt und seine 1%-BIP-Rechnung bezahlt; seine drei angekündigten Programmbeiträge sind null. Die echten Werte sind implementiert, aber ihre Vertragsbedingung fehlt in der Vorschau. Ein isolierter Lauf der installierten Helfer mit BIP 10 bestätigt: Front geliefert, Vertrag falsch, Forschungsbeitrag 0, Effizienzbeitrag 0, zusätzlicher Bürokratiebeitrag 0, Kasse 10 → 9,9.

Ein entsprechender Monopolfall ist über die ab Start angebotene Kommunistenentscheidung erreichbar: zunächst eine Front vereinbaren, danach den Monopol-Fokus wählen. Der Fokus verlangt keinen vorherigen Austritt; seine Programmwerte bleiben bis zum tatsächlichen Ende der Front inaktiv.

**Korrekturvertrag:** Entweder einen echten Vertragszustand bereits als Voraussetzung verlangen oder die Belohnung als ausdrücklich bedingte Wirkung darstellen. Eine Verhandlungsfreischaltung darf nicht wie ein bereits umgesetztes, sofort wirksames Programm erscheinen. Der vorhandene Abgleich für aktive und suspendierte Programme soll erhalten bleiben.

## Bestätigte Einbindung und Prüfgrenzen

- Die tatsächliche `mod/mdcoldwar.mod` zeigt auf den aktuellen Projektordner; die Benutzer-`dlc_load.json` aktiviert diese Mod, Sprache Englisch.
- Iraks 1970-History lädt den Baum und hinterlegt sieben gewöhnliche Start-Spirits. Der Generic-Fallback nimmt Irak ausdrücklich aus; die Initialisierung lädt den Baum nur bei tatsächlich fehlendem Baum nach.
- 426 irakische IDs bleiben erhalten, davon 410 aktiv und 16 verborgene Kompatibilitätseinträge. Der US-Baum behält seine 214 ursprünglichen Foki und ergänzt 15 IDs, davon 14 aktive Karten.
- Alle 115 alten Entscheidungsereignisse sind genau einmal registriert; neue IDs sind ab 10000 reserviert. Keine neue fehlende Referenz wurde gefunden.
- Erneut bestanden: 28 Daten-/Strukturtests, 14 Migrations-/Transaktionsszenarien, 18 Politik-, 21 neue US-, acht Kern-, neun Start-Spirit- und acht Präsentationsprüfungen; zusätzlich die statische Gesamtprüfung. Diese Prüfungen enthalten die oben beschriebenen Gegenfälle bisher nicht.
- Der letzte native Startversuch unter demselben Manifest brach nach 196,2 Sekunden vor den Irak-Prüfmarken ab. Die Ursache ist nicht zugeordnet. Keine neue native Hover-, Save-Load- oder Mehrspielerprüfung wurde in dieser Gegenprüfung vorgenommen.

Die Entfernung des July-State-Spirits allein nach der Wahl des Frontmodells bleibt eine **Designfrage**: Der alte freigegebene Entwurf erlaubt ausdrücklich den Ersatz durch das gewählte Institutionenmodell. Trotz nachvollziehbarer Vertragsfrage wird das hier nicht als sechster bestätigter Exploit gezählt.
