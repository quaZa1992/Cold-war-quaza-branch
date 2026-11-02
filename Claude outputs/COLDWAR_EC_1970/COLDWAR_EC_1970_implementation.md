# EG 1970 – Umsetzung „The European Communities" (Stand 30.10.2026)

Design: `claude/mdcw_ec_1970_ideensammlung.md` (Systemdesign v3.4) · Visualisierung: [Artifact „EC 1970 System"](https://claude.ai/artifact/AtEHwfjAQbMaup3k9Dr32d)
Mod: `mdcoldwar` (MD 2.0.3-Hotfix / HOI4 1.19), Szenario 1.1.1970, MP-Rollenspiel. Präfix `COLDWAR_EC_`. Spieltexte Englisch.
**Status:** im Mod-Ordner (199 Dateien, 30.10.2026), Prüfsummen nach dem Schreiben verglichen. Kein git commit/push.

---

## 1. Generator

- Ort: `Claude outputs/COLDWAR_EC_generator/` (Python, keine Handänderungen am erzeugten Code).
- Bauen und prüfen: `python3 run.py <mod_root> <out_dir> <idx_mdcw.json>` → `18 files, 0 errors`. Der Validator prüft Kodierung (UTF-8, BOM nur in `.yml`, LF), Klammern, kein `>=`/`<=`, unbekannte Effekte/Trigger/Ideen/Modifier/Events/Tags, Scripted-Loc und Loc-Schlüssel, nie gesetzte Variablen, GUI-Elemente und Listen, Schriften, Texturen, Überlappungen und Fensterränder. Die Fremd-Datei-Patches meldet der Build einzeln.
- Vorschau: `python3 run_preview.py <mod_root> <out_dir> <png_dir> <geo_dir> [Szenarien]` rendert die Fenster mit den echten Bitmap-Schriften und einem Interpreter für Trigger/Scripted-Loc; meldet Texte, die nicht passen. Szenarien in `scenarios.py` (council_1970/1986, council_desk, parl_1986, prop_1986, prop_target, prog_1986, proj_1986, comm_1986).
- Module: `data.py` (Katalog, Gewichte, Sitze, Kalender, Fristen) · `core.py` (Start, Mitglieder, Uhr, Zählung) · `offices.py` (Präsidentschaft, Kommission, Parlament, Zustimmung, Takt) · `procs.py` (Akten-Slots, Verfahren, Abstimmung) · `cat.py` (Wirkungen, Verfügbarkeit, Texte) · `money.py` (Haushalt, Darlehen) · `prog.py` (Projekte, Hilfe, Gegenleistungen, Kapazität, Gerichtshof, Kalender) · `ui.py`/`ui2.py`/`ui3.py` (Reiter) · `uifx.py` (Fensterberechnung, Event-Texte) · `look.py`/`fontgen.py`/`bmfont.py`/`art.py` (Texturen, Schriften) · `patches.py` (Fremd-Dateien) · `misc.py` (Events, On-Actions, Game Rule, Ideen).

## 2. Dateien im Mod

| Datei | Inhalt |
|---|---|
| `common/scripted_effects/COLDWAR_EC_1970_effects.txt` | Start, Mitgliedschaft, Uhr, Präsidentschaft, Kommission, Parlament, Zustimmung, Beitritt |
| `…_procedures.txt` | 10 Akten-Slots (1–8 Anträge, 9 Haushalt, 10 Kommission), Rat, Parlament, Ratifizierung, Angebote |
| `…_catalogue.txt` | Wirkungen A1–E8, Teilnahme-Teile, Sonderfälle |
| `…_budget.txt` | Beitrag, Rückfluss, Salden, Darlehen B10 |
| `…_programmes.txt` | Projekte P1–P8, Hilfe für Drittländer, Gegenleistungen, Kapazität, Gerichtshof, Kommissionskalender |
| `…_ui.txt` | Fensterberechnung (nur beim Klick des Betrachters) |
| `common/scripted_triggers/COLDWAR_EC_1970_triggers.txt` | 109 Trigger |
| `common/scripted_guis/COLDWAR_EC_1970.txt`, `interface/COLDWAR_EC_1970.gui/.gfx` | Fenster 1080 × 700, Toolbar-Knopf, Reiter als Child-GUIs |
| `common/scripted_localisation/COLDWAR_EC_1970_scripted_localisation.txt` | Texte des Fensters und der Events |
| `gfx/interface/coldwar_ec/` (147 Texturen), `gfx/fonts/COLDWAR_EC/` (13 Schriften + Lizenz) | Grafik |
| `common/ideas`, `dynamic_modifiers`, `opinion_modifiers`, `game_rules` (`COLDWAR_EC_1970_*`) | Ideen, Gemeinschafts-/Teilnahme-/Extern-Modifier, Meinungen, Regel „Commission Calendar" |
| `events/COLDWAR_EC_1970_events.txt` | 18 News-Events, nur „Noted." (kein Optionen-Event) |
| `common/on_actions/zzzzzzzz_COLDWAR_EC_1970.txt` | Start, Wochen- und Monatstakt |
| `localisation/english/COLDWAR_EC_1970_l_english.yml` | Englische Texte |

## 3. Eingriffe in fremde Dateien (nur `# COLDWAR`-Zeilen)

| Datei | Eingriff |
|---|---|
| `99_eu_scripted_effects.txt` | MD-EU im 1970-Szenario aus; Stufe-1-Hook entfernt |
| `00_money_system.txt` | Gemeinschaftshaushalt als wöchentliche Ausgabe/Einnahme (neben den Team-Hooks vom 30.10. `icwt_programme_fiscal`, `COLDWAR_FRA2_add_weekly_income`, unverändert) |
| `mdcw_cold_war_effects.txt` | EG-Programme zählen beim Empfänger (`mdcw_cw_r_*`) vor den Deckeln; Rabatt „Western Alignment" bei den Wechselkosten |
| `01_european_union_guis.txt`, `EU_voting_decisions.txt`, `99_EU_scripted_triggers.txt`, `MD_focus_EU_l_english.yml` | Stufe-1-Hooks zurück auf MD |

Der Generator wendet jeden Patch idempotent an und meldet „applied / already applied / nothing to revert".

## 4. Ablauf im Spiel

- **Start:** `on_startup` → `COLDWAR_EC_initialize` in FRA (nur 1970-Szenario). Mitglieder, Antragsteller, Assoziierte, Gewichte, Sitze, Präsidentschaft BEL, Haushalt.
- **Uhr:** Wochen- und Monatstakt laufen im Puls eines „Uhr-Landes" (`global.cwec_clock`, Trigger `COLDWAR_EC_is_clock`); verschwindet es, übernimmt das nächste Land, das pulst. So kommt jeder Takt genau einmal, obwohl HOI4 die Pulse der Länder verteilt.
  - Woche: Kalender (Präsidentschaft, Haushalt, Kommission, Wahlen), Akten-Fristen, Ratsabstimmung, Programme, Zählung, Fenster-Refresh.
  - Monat: Zustimmungsdrift, tote Mitglieder, Austritte, Gegenleistungen, Haushalt, Modifier, Assoziierte, Gerichtshof, Kommissionskalender.
- **Akten:** Jeder Antrag belegt einen Slot mit Nummer, Phase, Frist, Antragsteller, Ziel. Eine Ratsabstimmung zur Zeit (Reihenfolge nach Ticket). Nur Spieler-Mitglieder zählen (Gewichte 70,5 %, Einstimmigkeit, einfache Mehrheit; Parlament über Spieler-Sitze).
- **Fenster:** Klicks prüfen Zustand und Vorgangsnummer erneut; `dirty = global.cwec_dirty`; KI sieht keine Knöpfe.

## 5. Oberfläche

- Fünf Reiter genau nach der freigegebenen Visualisierung (Geometrie aus dem Artifact gemessen, `geo.json`); Vergleichsbilder Artifact ↔ Generator-Vorschau für alle Reiter.
- Schriften: eigene Bitmap-Schriften (Ubuntu 13/14/15/20 px, fett 14/15/20; Share Tech Mono 13–30 px), weiße Glyphen, Farbe und Farbcodes (`§B`, `§N`, `§M` …) in der `.gfx`.
- Überlappungen: Der Validator prüft jedes Element gegen jedes andere derselben Sichtbarkeitsgruppe und gegen den Fensterrand. Stand: 0 Fehler. Texte, die nicht passen, meldet die Vorschau: Stand 0.
- Gewinn/Preis auf den Karten: Kurzfassung (kurze Bezeichnungen, Modifier je Zielgruppe zusammengefasst, höchstens drei Zeilen, sonst „+ N more · hover for all"); Tooltip mit der vollständigen Liste.
- Kommission im Kopf: Flagge des Spieler-Präsidenten, sonst des historischen (Rey/BEL, Malfatti/ITA, Mansholt/HOL, Ortoli/FRA, Jenkins/ENG, Thorn/LUX, Delors/FRA, Santer/LUX).

## 6. Korrekturen dieser Runde (QA-Liste 1–16)

1. Darlehen nur ausgezahlt, wenn ein Darlehensplatz frei war; höchstens eine B10-Akte offen.
2. Austritt: Kreditnehmer zahlt den Rest sofort an die Mitglieder (nach BIP), eigene Hilfsprogramme enden, Kandidatur zurückgezogen.
3. Kommissionskalender legt jeden historischen Beschluss nur einmal vor (`COLDWAR_EC_cal_<ID>`); D8 geht an den COMECON-Vorsitz bzw. SOV und ist nach der Annahme erledigt (ADOPTED).
4. Jedes News-Event liest eigene Variablen `cwec_ev<N>_*` (beim Registrieren der Effekte umgeschrieben, mit Prüfung) und eigene Textkopien; zwei verschiedene Nachrichten in einer Woche überschreiben sich nicht mehr.
5. D5/D6: `every_country` bleibt – läuft nur einmal bei der Annahme, nicht periodisch.
6. Takt im Puls des Uhr-Landes statt Flaggen mit Tagesdauer.
7. Teilnahme-Modifier enthält jetzt `BK` (Airbus, Ariane); Variable wird zurückgesetzt.
8. Blättern in allen Listen (neues Layout).
9. Akten, deren Partner oder Antragsteller nicht mehr existiert, schließen ohne Wirkung.
10. Temporäre Arrays eindeutig benannt und geleert (`cwec_t_dead`, `cwec_t_closed`).
11. Verschwundene Mitglieder: Präsidentschaft rotiert neu, Kommissionspräsident entfällt, Darlehen und Programme schließen.
12. „Vital Interest" nur mit genug PP (genaue Schwellen).
13. Haushalts-Stellungnahme des Parlaments zählt wie eine Anhörung.
14. Assoziierte kommen in `global.cwec_ext` und erhalten den externen Modifier.
15. Monatlich zuerst Gegenleistungen, dann Haushalt.
16. Schreibtisch: „END NOW" beendet das neueste eigene Programm.

## 7. Abweichungen vom Design

- Schriften Ubuntu/Share Tech Mono statt MD-Atlanten (§14, Grund dort).
- Gastarbeiter-Rückkehr über EG-Modifier, nicht über `mdcw_gw_complete_agreement_*`.
- EG-Programme wirken über `mdcw_cw_r_*`-Summen und erscheinen nicht in der Programmliste des Cold-War-Fensters.
- D3–D7 treten nach der Annahme automatisch in Kraft (keine Annahme eines Partners).
- Kommissionspräsident: Kandidat des Mitglieds mit dem größten Ratsgewicht geht zur Abstimmung.
- Parlamentsfraktionen werden berechnet und nur als Leiste gezeigt.

## 8. Performance

- Keine tägliche Arbeit, keine periodische Weltschleife. Wochentakt: höchstens zehn Akten, drei Programme, zwei Darlehen, die Mitglieder. Monatstakt: Mitglieder, Beobachtungsliste, laufende Programme.
- Empfängerliste und Zielauswahl entstehen nur beim Klick des Betrachters.
- Abwesende Spieler: Flag `COLDWAR_EC_player_seen` (365 Tage) beim Öffnen, Klicken, Zählen und bei Angeboten; Angebote und Ratifizierungen warten.

## 9. Offen / Rückfragen

- **FRA2-/SPR-Bäume** prüfen `has_idea = EU_member` (z. B. `COLDWAR_FRA2_1970_focus.txt` Z. 865, 1261, 1502, 2339; `COLDWAR_SPR_v2_*`). Im 1970-Szenario vergibt niemand mehr `EU_member`, diese Bedingungen sind also nie erfüllt. Vorschlag: `# COLDWAR`-Umstellung auf `COLDWAR_EC_is_member = yes` – nur nach Freigabe (Team-Dateien).
- Nicht mehr benutzte Texturen älterer Stände gibt es im Mod nicht (Ordner war neu).
- Kalibrierung von Abrufsatz, Rückflüssen und Programmkosten nach dem ersten MP-Test.

## 10. Testliste im Spiel

1. Start 1970: Toolbar-Knopf, Fenster öffnet, Emblem 6 Sterne, Präsidentschaft BEL, Kommission Rey/BEL, keine MD-EU-Elemente.
2. Proposals: Kapitel wechseln, blättern, Eintrag wählen, Anforderung (50 PP) → Agenda zeigt „Commission drafting".
3. Ratsabstimmung mit zwei Spielern: For/Against/Abstain, Balken und Schwelle, Ergebnis-News, Vital Interest mit/ohne genug PP.
4. Vertrag (A1 oder A7): Konferenz, Schlussakte, Ratifizierung (Parlament/Referendum), passive Länder mit Resttagen, Inkrafttreten.
5. Beitritt D1 (ENG als Spieler): Antrag, Verhandlungen, Ratifizierung, Mitglied am 1.1., Sterne 7+.
6. Parliament: Halbrund, Delegationsstimme, Europawahl nach A4.
7. Programmes: Empfängerliste (nur Spieler außerhalb), Kontinentfilter, Gegenleistung mit echten Werten, Kapazität vorher → nachher, „END NOW" auf dem Schreibtisch.
8. Projekt P1: Planung, Bau, Gebäude, Haushaltszeile.
9. Community: Salden, „Who pays whom", Budgetbalken, Teilnahme (Snake/ERM), Austritt per Referendum.
10. Darlehen B10: Auszahlung, wöchentliche Rückzahlung, zweite B10-Akte gesperrt; Austritt des Kreditnehmers.
11. Zwei Nachrichten in derselben Woche (z. B. Ergebnis + Programmstart): beide zeigen ihren eigenen Text.
12. Spieler verlässt das Spiel und kommt zurück: Angebot wartet unter „Your Desk".
13. Performance: Spieltempo 5 über zehn Jahre ohne Ruckler am Wochenwechsel.
