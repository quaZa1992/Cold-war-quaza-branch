COLDWAR 1970 economy generator (Claude, 20.10.2026)
Inputs: states_full.json / blds_split.json (parsed history/states), IMP_1970_gdp_scripted_effects.txt (targets, state productivity), state_category, game.log calibration, wb2000.txt (World Bank NY.GDP.MKTP.CD 2000).
Run: python3 emit.py -> common/scripted_effects/COLDWAR_1970_starting_buildings.txt, dynamic modifier, localisation.
Paths inside data.py point to the Claude workspace; adjust before re-running.
