# COLDWAR_DDR_generator - German Democratic Republic 1970

Generates the GDR 1970 focus tree and all of its systems from the approved design (layout v3 of 20.10.2026: every party tree
directly under its "Power to ..." focus, First Secretaries under their candidacies, two floors; project doc
`claude/mdcw_ddr_1970_focus_tree_design.md`, data in `design/`, design sources in `../COLDWAR_DDR_design_v3.zip`).
The code follows MD's Russia tree (05_russia.txt) line by line - field order, MD tooltips, MD money and faction helpers,
MD offer form (TT_IF_THEY_ACCEPT), AI via scripted triggers (skill coldwar-tree-build).
Edit the generator or the design, never the generated files.

    python3 dg_build.py      # writes out/ (mirrors the mod paths)
    python3 validate_ddr.py  # static checks (braces, loc, effects, ideas, modifiers, sprites, flags, patches,
                             # MD style like Russia 2000, layout: party trees under their power focus, unique icons, Cold War hooks)

Inside the mod the generator reads the mod files it patches from the mod root (`../../`) and the shared
index files from `../COLDWAR_EGY_generator` (goal_sprites.json, idea_gfx.txt, repo_paths.json) and
`tools/generic_1970_focus_tree/idx_mdcw.json`.

| Module | Content |
|---|---|
| dg_common.py | paths, prefix COLDWAR_DDR_, helpers, English modifier labels |
| dg_load.py | loads the design (foci, ideas, offers, parties, leaders) |
| dg_avail.py | English `available` texts -> triggers (no date conditions in foci, house rule) |
| dg_effects.py | effect dicts -> Clausewitz (MD helpers, dynamic modifiers, ladders, trust, course) |
| dg_focus.py | focus tree file, icons (gfxsel/gfx_pick.json), AI weights |
| dg_events.py | system and historical events, deaths, succession, Kremlin, accession |
| dg_offers.py | 69 offers in MD form: the focus sends the event, TT_IF_THEY_ACCEPT/REJECT show the answer; the partner decides |
| dg_decisions.py | Central Committee, German Question, Moscow, Five-Year Plans, Hard Currency, ... |
| dg_sys.py | scripted effects/triggers: init, money, factions, trust, First Secretaries, Warsaw Pact |
| dg_misc.py | ideas, dynamic modifiers, balance of power, opinions, traits, on_actions, events file |
| dg_build.py | writes everything; patches history, fallback list and party names (idempotent, # COLDWAR) |

The opening event `COLDWAR_DDR.1` uses historical narrative without tutorial
variables or trust-meter explanations. Its dedicated `GFX_COLDWAR_DDR_intro`
sprite is a native217×163 country-event picture with MD's original frame and
a proportional180×150 photo crop. The shared event GUI is unchanged. Export
the existing MD photograph with `python tools/event_art/export_ddr_intro.py`
from the mod root; the generator archives the resulting DDS in `art/dds/`
and stages both the texture and sprite on the next build. Script outputs use
UTF-8 without BOM; localisation alone uses UTF-8 with BOM.

Patched existing files (marker `# COLDWAR`): `history/countries/DDR - East Germany.txt` (tree, init,
Ulbricht without expire), `common/scripted_effects/mdcw_1970_focus_tree_effects.txt` (fallback list),
`common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt` and
`mdcw_historical_parties.txt` (GDR 1970 party names, first line of each block).
