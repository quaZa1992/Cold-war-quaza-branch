# Localisation audit – Soviet Union 1970 tree (17.10.2026)

Sandbox: `/home/claude/sovgen_loc/` (generator copy). `/home/claude/sovgen/` was not touched.
Build `python3 cw_build.py` → validator `python3 validate_sov.py`: **0 errors, 8 warnings** (the same 8 "effect never used" warnings as before).
Re-check script: `/home/claude/audit/shared/loc_audit_check.py [outdir]` (read-only; run with `MODS=1` to print how each modifier is localised).

## Trigger and how HOI4 names modifiers

`COLDWAR_SOV_ni_window_society/economy/military` use `imp_national_ideas_1/2/3_cost_factor = -0.5`. HOI4 creates a
`<idea category>_cost_factor` modifier for every idea category, but the text has to come from a loc key. MD's own categories are
localised **by the bare modifier name**: `replace/replaced_from_vanilla_modifiers_l_english.yml` has
`social_budget_cost_factor`, `education_budget_cost_factor`, `bureaucracy_cost_factor`, `crime_fighting_cost_factor`,
`corruption_cost_factor`, `military_spending_cost_factor` and others. Only vanilla's own law categories use `MODIFIER_economy_cost_factor`.
Custom modifiers (modifier_definitions) also use the bare name. Built-in modifiers use `MODIFIER_<UPPER>`.
Imperia's pools are named in `mdcw_imperia_national_ideas_l_english.yml` (`imp_national_ideas_1/2/3` = Our Society / Our Economy / Our Military),
but no file has a `*_cost_factor` key for them. That is why the game printed the raw key.

To check against the whole mod, I staged the full English loc of the mod from the user's PC into `/mnt/user-data/uploads/mdcoldwar/localisation/english/`
(396 files from repo_paths plus 14 that exist only on the device; 439 files in total). These are read-only copies, and I did not write anything to the device.
The deployed `COLDWAR_SOV_1970_l_english.yml` was **not** staged, so it cannot hide missing keys. With the full loc, the build output of the
unchanged generator stayed identical (no extra keys skipped).

## 1. Modifiers without loc: 3 found, 3 fixed

I checked 106 distinct modifiers from ideas, dynamic modifiers, traits, the BOP ranges and decision/event modifier blocks. The opinion modifiers carry only values.

| How the modifier is localised | Count |
|---|---|
| MD bare key (custom / MD category modifiers) | 49 |
| `MODIFIER_<UPPER>` in MD loc (vanilla texts MD carries) | 40 |
| Vanilla engine modifier, text only in vanilla (cannot be checked here, MD uses them itself) | 14 |
| **No loc anywhere** → raw key in game | **3** |

- Missing: `imp_national_ideas_1_cost_factor`, `imp_national_ideas_2_cost_factor`, `imp_national_ideas_3_cost_factor` (the three policy-window ideas).
- Fix: the keys are now written into our yml under the exact modifier name, following MD's convention (exempt from the COLDWAR_ prefix rule):
  `imp_national_ideas_1_cost_factor:0 "Political Power Cost of National Ideas (Our Society)"`, likewise for (Our Economy) and (Our Military).
- Assumed vanilla (14): army_attack_factor, army_core_defence_factor, army_defence_factor, breakthrough_factor, experience_gain_army,
  foreign_subversive_activites, industrial_capacity_dockyard, industrial_capacity_factory, monthly_population, production_speed_arms_factory_factor,
  production_speed_infrastructure_factor, production_speed_nuclear_reactor_factor, production_speed_rail_way_factor, subjects_autonomy_gain.

## 2. Referenced loc keys: 3,077 distinct keys checked, 3 missing and fixed

Kinds checked: focus names and descs (836 + 836), ideas (112), decisions (56) and their descs, categories (7) and their descs, events
(title/desc/options, 494), custom_effect_tooltip (219), localization_key (223), `tooltip =` (112), shortcuts (10), opinion modifiers (38 defined, 35 used),
traits (19 defined, 38 references), dynamic modifiers (39), BOP id/sides/ranges (10), MD ideas used (152), `name =` references (114, mostly tech bonuses),
every `COLDWAR_SOV_*_tt/_desc/_txt` token anywhere in the code (339), focus search filters (10), and the `tooltip_side` of the Politburo BOP.

- **Missing (3), fixed:** tech-bonus names of three offers. `add_tech_bonus = { name = COLDWAR_SOV_offer_<k> }` is shown in the research screen:
  `COLDWAR_SOV_offer_cocom`, `COLDWAR_SOV_offer_gas_for_pipes` and `COLDWAR_SOV_offer_paris_axis`. They now take the offer's event title
  ("Relaxing the Export Controls", "Gas for Pipes", "A Franco-Soviet Partnership").
- False positive: `censored_nation_05` (MD law idea), which MD names with `name = censored_nation`. That key exists.
- Scripted loc: all 17 distinct `[COLDWAR_SOV_Get*]` functions used in texts are defined. All `[?var]` variables are set by our code (or are MD globals:
  `mdcw_cw_oil_ratio`, `imp_oil_price_display`). All 29 country tags used in `[TAG.GetNameDef]` have loc. All 13 `$MODIFIER_X$` used inside our texts exist in MD loc.
- **Optional, not changed:** 108 of 112 ideas, all 19 traits and all 39 dynamic modifiers have no `_desc`. HOI4 leaves an absent description out
  (it does not print the key), so nothing raw shows. Writing ~170 flavour texts would be a content task and is not a loc fix. Every decision and every category has its `_desc`.

## 3. Text quality

- German leftovers: **0**. The hits ("die", "Oder", "Nur") are English or proper names: "die in office", "Oder-Neisse line", "Lop Nur", "Nur Muhammad Taraki".
  There are no ä/ö/ü/ß. The non-ASCII characters (é, á, ł, ń, ő, ș, Š in Gdańsk, Gomułka, Ceaușescu, Šik, Nyers) are also used in MD's own loc.
- Unbalanced `§X…§!`: 0. Broken `[…]` calls: 0. Raw keys or snake_case tokens in texts: 0. TODO: 0. Unintended empty strings: 0 (`COLDWAR_SOV_empty` is empty on purpose). Text equal to key: 0.
  Mojibake: 0. Trailing spaces: 0. Space before punctuation: 0.
- Double spaces: 0 real. The 56 hits are the intended indentation after `\n` in the vote and seat lines.
- **Labels with the wrong meaning (3), fixed.** The custom tooltips of the dynamic-modifier variables (`COLDWAR_SOV_mod_<mod>_tt`) disagreed with the modifier line the player sees:
  - `corruption_cost_factor`: "Corruption Costs" → "Political Power Cost to change Corruption Laws" (in MD this is a category cost factor)
  - `military_spending_cost_factor`: "Defence Spending Costs" → "Political Power Cost to change Military Spending" (same reason)
  - `consumer_goods_factor`: "Consumer Goods Factories" → "Tax Cost Factor (Consumer Goods)" (MD relabels it "Tax Cost Factor")
- **Policy-window tooltips (15), harmonised.** Two named no pool (military_advisers, development_agency), the quoting was inconsistent, and ten said only
  "adopting X costs half", but the modifier halves the cost of the whole pool. I checked each idea's pool against `mdcw_imperia_national_ideas_1/2/3.txt`
  and `mdcw_cold_war_national_ideas.txt` (all 15 were in the right pool). They now share one wording:
  "For one year, national ideas of the §Y<pool>§! pool (Government screen), such as §Y<idea>§!, cost §G50%§! less political power."

## 4. yml format

UTF-8 with BOM, first line `l_english:`, and every other line is ` key:0 "text"` or a comment. No unescaped quotes (the writer turns `"` into `'`),
no tabs or CR, no stray backslashes, no duplicate keys. There are now 3,074 keys.

## Changes (generator)

- `cw_common.py`: MOD_EN labels for the 3 cost factors, plus `NEEDS_LOC` and `modifier_loc()`, which writes loc keys that equal the modifier name.
  `md_loc_keys()` reads the whole mod loc. `_vanilla_modifier_label` now finds `MODIFIER_<UPPER>`, `MODIFIER_<name>` or the bare key anywhere in the mod
  (before, it read only the replace file). The `.title()` fallback is replaced by an assert, so a missing label stops the build. The 3 label meaning fixes are here too.
- `cw_misc.py`: the ideas, dynamic-modifier, BOP and traits writers call `modifier_loc()` for every modifier they write.
- `cw_offers.py`: `offer()` registers the loc of the offer's tech-bonus name.
- `cw_layout.py`: `NI_WINDOW_TT` gives the 15 policy-window tooltips one wording.
- `validate_sov.py` (new guards, both tested by deleting the keys): `modifier without loc` (a used modifier with no `MODIFIER_` key, bare key or our key, unless it is a
  known vanilla modifier) and `missing tech bonus loc`. MD loc files named COLDWAR_SOV are now ignored, so a deployed old copy cannot hide missing keys.

Output diff against the pre-audit build: only the yml changed. There are 6 new keys, and 18 texts changed (15 policy-window tooltips and 3 modifier tooltips).

## Not verified / open

- Not tested in game. The bare-key convention is taken from MD's own category cost factors. If the engine ignored bare keys for these categories, a
  `MODIFIER_imp_national_ideas_N_cost_factor` copy would be the fallback. No evidence points that way, since MD's bare keys render.
- Vanilla's own modifier texts are not available here, so the 14 "assumed vanilla" modifiers are unverified. MD uses all of them in its own content.
- If another COLDWAR tree later uses `imp_national_ideas_N_cost_factor`, define the keys once. cw_build already skips keys that exist in another mod loc file.
