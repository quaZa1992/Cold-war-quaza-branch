# COLDWAR_GEN_generator – Parteipfade des generischen 1970-Baums

Setzt das freigegebene Design der 24 Parteipfade und 5 Outlook-Stämme (`design/`, Projekt-Doc `claude/mdcw_1970_generic_party_paths_design.md`) als Spielcode im MD-Russland-Stil um und legt den Baum auf zwei Etagen.

## Aufruf

```
python3 gen_build.py <mod_root>      # liest die aktuellen Mod-Dateien, schreibt ./out/<Mod-Pfad> + out/build_report.json
python3 validate_gen.py <mod_root>   # prüft ./out (0 Fehler nötig)
```

**Reihenfolge:** Der alte Generator `tools/generate_1970_generic_focus_tree.py` schreibt dieselben Dateien neu (Fokus-Datei, Loc, Programme, Effekte). Nach jedem Lauf des alten Generators diesen hier erneut laufen lassen. Der Lauf ist wiederholbar: Domänenblöcke werden über ihre Bounding-Box verschoben (zweiter Lauf = keine Verschiebung), eigene Loc-Schlüssel werden aus der alten Loc entfernt und neu geschrieben.

## Module

| Datei | Aufgabe |
|---|---|
| `gen_common.py` | Pfade, Layout-Konstanten (Etagen, Abstände, GCC-Lücke), BIP-Preis der Gebäude, KI-Gewichte |
| `gen_load.py` | Fokus-Datei lesen: Kopf, Sektionen, Fokus-Felder als Rohtext; Positionen; Footprint von GCC/UNI |
| `gen_effects.py` | Design-Effekte → MD-Code (Programmzeilen, Ideen, Popularität, Gesetze mit Guard, Gebäude, Geld, Technik, XP, Fraktionen, Spannung, CW-Neuberechnung); eigene Tooltips (`COLDWAR_TT`): MDs `<modifier>_tt` nur, wenn ihn eine Loc-Datei der Mod **definiert** (MD-Fokusse benutzen einige, die nirgends stehen, z. B. `research_speed_factor_tt`), sonst `COLDWAR_<modifier>_tt` |
| `gen_icons.py`, `icon_picks.py` | Icons der 336 neuen Fokusse und Bilder der 86 Ideen (Handauswahl in `icon_picks.py`, Score nur als Rückfall) |
| `gen_focus.py` | Fokus-Datei schreiben: Kopf erhalten, Stämme und Parteipfade aus dem Design, Domänenblöcke auf Etage 2, MD-Feldreihenfolge |
| `gen_misc.py` | Ideen-Datei, Parteiprogramme (Dynamic Modifier), Loc (neu + alte bereinigt), gemeinsame Tooltip-Datei, Spannungs-Helper |
| `gen_build.py` | Ablauf |
| `validate_gen.py` | Klammern, Kodierung, Feldreihenfolge, Referenzen, mx-Symmetrie, Layout (auch gegen GCC/UNI), Linien, Effekte/Trigger/Ideen/Sprites gegen `index/idx_mdcw.json`, Programme, Loc, Tooltips (nur definierte Schlüssel; die gemeinsame Tooltip-Datei verliert keinen Schlüssel), Glyphen (Windows-1252) |
| `design/` | Design-Daten (dsl.py, build.py, parts/*.py) – Quelle der Wahrheit für Inhalte |
| `index/` | Namensindex der Mod (`idx_mdcw.json`), Sprites, Ideenbilder, Modifier-Referenz; `md_focus_tts.txt` (von MD-Fokussen benutzte Tooltips) nur noch zur Info |

## Ausgabe

- `common/national_focus/mdcw_1970_generic_focus.txt` (ersetzt)
- `common/dynamic_modifiers/mdcw_1970_generic_party_programmes.txt` (ersetzt)
- `common/ideas/COLDWAR_GEN_1970_party_ideas.txt` (neu)
- `common/scripted_effects/mdcw_1970_generic_focus_effects.txt` (Spannungs-Helper → `mdcw_cw_add_tension`)
- `localisation/english/COLDWAR_GEN_1970_party_paths_l_english.yml` (neu), `mdcw_1970_generic_focus_l_english.yml` (eigene Schlüssel entfernt), `COLDWAR_modifier_tooltips_l_english.yml` (gemeinsam für alle COLDWAR-Bäume: vorhandene Schlüssel bleiben unverändert, fehlende kommen dazu, sortiert, Kopf und Format wie beim DDR-Generator – `$MODIFIER_X$: $RIGHT|+=%1$`, Name aus dem Spiel, sonst englisch). **Vor dem Commit frisch stagen und neu bauen**, damit Schlüssel anderer Bäume nicht verloren gehen

## Werte zum Nachjustieren (`gen_common.py`)

`FIRST_ENTRY_X`, `FLOOR2_ROW`, `FLOOR2_X`, `BLOCK_GAP`, `CONTINUOUS_FOCUS_POSITION`, `BUILD_PRICE_PER_BN` (Fabrik = 1 % BIP), `AI_BASE_NEW`, `AI_OVERRIDE`.
