# COLDWAR Soviet Union 1970 – design sources

Design of the Soviet Union 1970 focus tree (`COLDWAR_SOV_1970_focus`), design v3 (15 Oct 2026). Not yet game code.

- `sov_dsl.py` – design DSL: every effect is a dict with kind, parameters and German design text.
- `d_sections.py`, `d_trunk_eco.py`, `d_mil_state.py`, `d_foreign.py`, `d_politics.py`, `d_leader_sections.py`, `d_leaders.py`, `d_parties.py` – the foci (`d_leaders.py`: Politburo plenum foci and the 11 General Secretary trees, non-exclusive).
- `d_republics.py` – The Politburo and the Republics: 3 seats for the SSR players, votes, intrigue, hooks into the key foci.
- `d_concept.py` – starting spirits, Politburo balance, union cohesion, country modifiers, decisions, events, portraits, files.
- `validate.py` – static check against the mod index (`idx_mdcw.json` from the generic-tree tools) and `modkeys.json`
  (all modifier keys used in the mod's ideas and dynamic modifiers, built by `modkeys.py`).
- `export.py` + `template.html` → `soviet_union_1970_focus_tree.html` (the visualisation).
- `sov_tree_full.json` – full machine-readable design (generator input for the code step).
- `gen_doc.py` – writes the German design doc `mdcw_sov_1970_focus_tree_design.md` and `sov_tree_full.json`.

Run: `python3 validate.py && python3 export.py && python3 gen_doc.py`. Paths in the scripts point to the cloud session; adjust them to your machine.
Naming: everything new carries COLDWAR (`COLDWAR_SOV_*`, events `COLDWAR_SOV.N`, comments `# COLDWAR |`).
