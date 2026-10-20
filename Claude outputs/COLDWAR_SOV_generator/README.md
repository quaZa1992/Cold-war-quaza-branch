# COLDWAR_SOV_generator - Soviet Union 1970 (Cold War mod)

Generates every file of the Soviet 1970 focus tree and the Politburo of the Republics from the approved design
(`../COLDWAR_SOV_design`, visualised in `soviet_union_1970_focus_tree.html`). Edit the generator or the design, not the output.

Run (Python 3.10+):

    python cw_build.py        # writes ./out (same folder layout as the mod)
    python validate_sov.py    # static checks: braces, loc, references, sprites, ideas, modifiers, events, flags

Modules:
- cw_layout.py: loads the design and lays out the 836 foci on one canvas (tidy tree per section, sections stacked)
- cw_avail.py / cw_effects.py / cw_manual.py: convert the design's conditions and effects into MD-style code
- cw_focus.py: the focus tree file (MD 2000 focus style, log line in every reward)
- cw_sys_effects.py: init, money, factions, cohesion, Politburo balance, General Secretaries, seats, votes, proposals, kompromat
- cw_decisions.py: decision categories and decisions (Moscow and the republics)
- cw_events.py / cw_offers.py: events (Politburo, congresses, deaths, crises) and the 48 offers (the partner decides)
- cw_misc.py: ideas, dynamic modifiers, balance of power, opinion modifiers, traits, on_actions, scripted localisation
- desc/: English focus descriptions and icon choices (out_N.json, icons_N.json)

Index files are shared with `../COLDWAR_EGY_generator` (goal_sprites.json, idea_gfx.txt, repo_paths.json, our_*.txt).
