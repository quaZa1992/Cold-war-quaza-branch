# Korrekturen der fünf Gegenprüfungsbefunde

19. Oktober 2026. **Alle fünf bestätigten Befunde sind in Revision `audit_2026_10_19_v2` im Generator und im aktiven Mod korrigiert.** Der ursprüngliche [Prüfbericht](POST_IMPLEMENTATION_REVIEW.md) bleibt als Vorher-Zustand erhalten. Die freigegebenen Werte, Koordinaten, gegenseitigen Ausschlüsse und Länderpfade wurden dafür nicht neu entworfen.

Installiertes Manifest: `c1d2b81b6f9508f635cd7b426563d2cb20213bc97d4bc766664a7623e23b2f3f`. Umfang: 103 generierte Dateien und neun begrenzte Integrationen. Der Irak behält 410 aktive Foki und 16 verborgene Kompatibilitätseinträge; die USA behalten alle 214 ursprünglichen Foki und den freigegebenen Golfabschnitt.

## 1. Irakische Autonomiezahlung

`tools/iraq_1970/usa_module.py` verwendet bei Angebot und Ratifikation denselben Zahlungs-Trigger. Eine belegte frühere Zahlung bleibt eine eigene Ausnahme. Jede erste Zahlung verlangt gemeinsam positives BIP, einen positiven vereinbarten Betrag, ausgeschalteten Kosten-Skip und ausreichende Staatskasse. Eine vorhandene positive Rechnung bleibt über BIP-Wachstum und erneut geöffnete Gespräche erhalten. Die Anforderung zeigt einen englischen Text mit dem konkreten irakischen Betrag statt interner Variablennamen.

Die tatsächliche native `modify_treasury_effect`-Implementierung wurde im begrenzten Interpreter ausgeführt. 0,1 Mrd. Kasse bei 0,2 Mrd. Beitrag, BIP null, Null-/Negativrechnung und Skip-Modus führen zu keiner Zahlung, keinem Bezahlt-Marker und keiner Autonomie. Exakt 0,2 Mrd. werden einmal bezahlt. Die Ratifikation prüft Geldverlust, BIP-Verlust und einen nachträglich aktivierten Skip erneut. Eine bereits bezahlte Vereinbarung verlangt keine zweite Zahlung.

## 2. Externer amerikanischer Schutz

Die gültige, tatsächlich angenommene externe Vereinbarung ist jetzt die gemeinsame Grundlage für Luftaktivierung und laufende Schutzfinanzierung. Eine zusätzliche akute Krise des älteren Safe-Haven-Programms beendet diese Vereinbarung nicht mehr. Zustimmung, ungelöste Nordfrage, Gastgeberzugang, tatsächliche eingesetzte Flugzeuge und Finanzierung bleiben erforderlich. Nach Ablauf oder bei Ungültigkeit werden die eigenen Vertrags-, Luft- und Liaisonboni entfernt.

Der Gegenfall mit friedlichem selbständigem KUR besteht über alle 90 Tage: täglich genau 0,05/7 Mrd. US-Kosten, danach Ablauf ohne automatische Erneuerung. Acht Invaliditätsfälle beenden die Verpflichtung ohne weitere Abbuchung. Alte humanitäre Safe-Haven-Bedingungen bleiben wirksam; sie können einen abgelaufenen externen Vertrag nicht unter Umgehung neuer Zustimmung verlängern.

## 3. Bereits angebotene zusammengelegte Projekte

`audit_migration.py` rekonstruiert aus einem positiven, noch unbezahlten Angebot eines entfernten Teilprojekts dessen historische BIP-Grundlage: Rechnung geteilt durch ursprünglichen BIP-Anteil. Bei mehreren gültigen offenen Angeboten gilt deterministisch die niedrigste implizierte Grundlage. Das ist eine Preisgrundlage, kein bereits bezahltes Guthaben. Nur belegte tatsächliche Zahlungen werden von den neuen Gesamtkosten abgezogen.

Im bestätigten Heavy-/Steel-Fall ergeben 0,5 Mrd. Steel bei 5% Anteil ein historisches BIP von 10 Mrd. Das neue Heavy-Paket kostet damit 0,5 Mrd.; bezahlt sind bereits 0,2 Mrd.; offen bleiben **0,3 statt 4,8 Mrd.** Ein eigener einmaliger v2-Marker repariert auch einen bereits durch v1 migrierten Spielstand mit gelöschtem Teilprojekt-Pending und falsch eingefrorener Ergänzungsrechnung. Abgeschlossene Lieferungen werden weder erneut vergeben noch erstattet. Neue Arbeit ohne gültiges altes Angebot verwendet weiterhin das aktuelle BIP.

Acht zusätzliche Szenariogruppen prüfen diesen Übergang vor/nach v1, ländliche Mehrfachangebote, Ölprojekte, ungültige Altbeträge, bloße Fokus-/Policy-Marker, abgeschlossene Lieferungen und wiederholte Aufrufe. Die tatsächliche alte Save-Datei wurde nicht in HOI4 geladen.

## 4. Konzession und Basra

`decisions_module.py` liest Staat, Gebäudetyp und Umfang aus der tatsächlichen `oil_concession_delivery`-Definition. Die britische Annahme prüft jetzt vor beiden Geldbewegungen irakisches Eigentum, Kontrolle und freie Infrastrukturkapazität in Basra 171. Sichtbare Option und tatsächliche Ausführung verwenden denselben Guard. Die native Infrastrukturprüfung verwendet keinen Shared-Slot-Parameter.

Verlorenes Eigentum, verlorene Kontrolle und volle Infrastruktur verhindern Zahlung und Vertragsmarker. Der letzte freie Platz und exakt 0,1 Mrd. Kasse erlauben die eingefrorene 1%-Gebühr einmalig. Die spätere physische Lieferung behält ihre erneute Kapazitätsprüfung; zwischen Zustimmung und Lieferung kann sich die Lage weiterhin ändern.

## 5. Front-/Monopol-Vorschau

`presentation.reward_preview()` erhält an beiden Compiler-Aufrufstellen dieselbe zusätzliche Vertragsbedingung wie das echte Programmeinkommen. Die Zahlen stehen in einem nativen bedingten Effekt: Frontvereinbarung tatsächlich in Kraft beziehungsweise keine Frontvereinbarung in Kraft. Englische Bedingungstexte ersetzen technische Kennungen. Verhandlungen werden weiterhin durch den Einstiegsfokus freigeschaltet; eine vorab erzwungene Vereinbarung würde diesen Zugang blockieren.

Auf Fokus- und Lieferentscheidungsfläche sind alle Zahlen vollständig bedingt. Acht Zustände vergleichen die angezeigte Bedingung mit dem tatsächlichen Programmverbraucher: keine Vereinbarung, gültig unterzeichnet, fehlende Legalisierung und fehlende Koalitionsgarantie, jeweils für Front und Monopol. Zahlen, Kosten und einmalige tatsächliche Ausführung bleiben erhalten.

## Gegenprüfung und Grenzen

Die Implementierungen wurden jeweils von einem anderen Bearbeiter geprüft. [POST_REVIEW_INSTALLED_TESTS.json](POST_REVIEW_INSTALLED_TESTS.json) führt die neuen Gegenfälle gegen geladene manifestierte Dateien aus; Generatoraufrufe werden dazu durch diese installierten Inhalte ersetzt. Die Dateien bleiben während der Prüfung unverändert. Die statische Gesamtprüfung findet keine fehlenden Referenzen. Byte-identischer Neuaufbau und 17 Chromium-Prüfungen der aktualisierten Gesamtansicht werden im [Gesamtbericht](IMPLEMENTATION_CHECKS.json) festgehalten.

Diese Revision wurde nicht erneut nativ gestartet. Der frühere vollständige Startversuch unter dem vorigen Manifest brach vor den Irak-Prüfmarken ab; die Ursache ist weiterhin nicht zugeordnet. Die fünf Skriptfehler sind korrigiert und gegen ihre Gegenbeispiele geprüft. Native Tooltippdarstellung, echter alter Save-Load, Flugmissionen, langfristiger Spielverlauf und Mehrspieler bleiben gesondert ungeprüft.
