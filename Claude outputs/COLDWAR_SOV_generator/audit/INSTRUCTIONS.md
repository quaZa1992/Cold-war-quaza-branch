# Phase 2 – Effect audit of the COLDWAR_SOV 1970 tree (one group of sections per agent)

Goal (from the mod author, Enes): "The focus effects do not make sense everywhere. Orient yourself on how the MD 2000 Russia tree rewards its foci, and build in our Imperia features and the Cold War features we added, where they fit."

You review EVERY focus of your group and decide `ok` or `fix`. For `fix` you give precise edits in our effect DSL. You do not touch layout, prerequisites, names or descriptions.

## Inputs
- Your group's foci: `/home/claude/audit/phase2/<group>.json` – per focus: id, section, English name, cost, prerequisites, mutually_exclusive, German `available_de`, English `desc_en`, and `effects` = list of `{idx, e (DSL dict), t_de (German summary)}`.
- Reference lists: `/home/claude/audit/phase2/reference.json` (build helpers, dynamic-modifier groups and their keys, all existing ideas with modifiers, factions, tech categories, parties 0–23, outlook ids).
- MD norms (read first): `/home/claude/audit/md_russia_effects.md` (section "Rulebook for COLDWAR_SOV (DSL)") and `/home/claude/audit/md_effect_norms.json` (`per_cost`, `value_ranges`, `themes`, `never`).
- Imperia / Cold War hooks: `/home/claude/audit/imperia_coldwar_hooks.md` and `.json` (`proposals` filtered to your sections; apply the P1/P2 ones that fit, P3 where it clearly improves the focus).
- Compiler (exact field meaning): `/home/claude/sovgen/cw_effects.py` → `compile_effect`.

## Output: `/home/claude/audit/overrides/<group>.json`
```json
{
  "foci": {
    "COLDWAR_SOV_x": {"verdict": "ok"},
    "COLDWAR_SOV_y": {
      "verdict": "fix",
      "problem": "one English sentence: what did not make sense",
      "set": [{"idx": 2, "e": {"k": "dyn", "g": "gosplan", "mods": {"production_speed_buildings_factor": 0.05}}}],
      "del": [3],
      "add": [{"k": "build", "helper": "one_random_industrial_complex", "cost": 0.008}],
      "cost": 5,
      "available_add": ["has_stability > 0.399"]
    }
  },
  "new_ideas": {"COLDWAR_SOV_new_id": {"name": "English Name", "mods": {"stability_factor": 0.03}, "days": 365, "picture_hint": "theme words"}},
  "new_loc": {"COLDWAR_SOV_something_tt": "English tooltip text with §Y..§! colour codes"},
  "new_opinions": {"COLDWAR_SOV_key": {"value": 10, "name": "English Name"}}
}
```
- There MUST be an entry for every focus id of your group (coverage is checked).
- `set`/`del` use the `idx` of the input effects. `add` appends. Omit what you do not need.
- Prefer small precise edits over rewriting whole lists.

## DSL (fields and units – exactly as compile_effect expects)
| kind | fields | notes |
|---|---|---|
| pp | v (int) | political power |
| stab / ws | v (fraction, 0.03 = 3 %) | stability / war support |
| fac | f, v (int) | internal faction opinion; f in reference.factions |
| party | i (0–23), v, o (fractions) | party popularity (+ outlook) |
| outlook | o (0–4), v (fraction) | outlook popularity via the ruling/main party |
| dyn | g (party_state, gosplan, armed_forces, union, commonwealth), mods {modifier: value} | permanent cumulative lines on our 5 country dynamic modifiers – the MD Russia main reward |
| prog | g (programme key = section key: bre, kos, …, wc, ns, …, cpsu), mods | lines on the programme modifier of that GS/party, only active while they rule |
| idea | id, days (optional), swap_id (optional, idea to replace if present) | id must exist in reference.ideas or in your new_ideas |
| rmidea | id | |
| coh | v (int) | Union cohesion |
| bop | v (fraction, − reformers / + orthodox) | Politburo balance |
| tension | v (number) | Cold War tension |
| build | helper (reference.build_helpers), cost (GDP share, e.g. 0.008 for one civilian factory) | always paid |
| gdp / gdp_gain / debt | v (GDP share) | pay / receive / receive as debt |
| tech | cats [CAT_…], b (0.5 = 50 %), n (uses) | |
| xp | kind (army/navy/air), v | |
| cp / manpower | v | |
| mastery | v, folder | |
| sp | project, v | special project progress ratio |
| space | – | MD space programme progress |
| infl | tags [..], v (percent points) | our influence in them |
| op | tag, key, v | OUR opinion modifier of them (allowed). New keys need new_opinions. |
| corr | helper (increase_corruption / decrease_corruption), v (count) | |
| raw | code [lines] | for Imperia / Cold War hooks that have no DSL kind. Every custom_effect_tooltip key you use must be defined in new_loc. Keep raw rare and correct Clausewitz. |
Do not add kinds rp, leader, heir, gensec, offer, event, decision, flag, cwjoin, elections, setlaw, law, trait, note, custom – they belong to the systems. KEEP existing effects of these kinds unless they are clearly wrong (then explain).

## Rules
1. **Fit the theme.** The reward must match the focus name and description (an oil-field focus pays in resources/oil income/energy, not in research). Fix mismatches.
2. **Budget by cost** (md_effect_norms.json per_cost): cost 2 ≈ 2–3.5 points, 3 ≈ 3–4, 5 ≈ 5–6, 7 ≈ 7–9 (1 point ≈ one typical MD line: 50 PP, +2 % stability, one dyn line of 0.03, one paid factory, tech 0.5×1, 25 XP, ±3–5 faction, +0.02 party). Note foci (only a German note/choice text) must give a small real reward. You may change `cost` if the focus is clearly over- or under-sized, but keep the MD scale 2/3/5/7.
3. **Downsides only where they make sense** (Enes' rule). About a third of the foci in MD have one. Every downside must be visible and logically follow from the focus.
4. **Value ranges and the `never` list** of md_effect_norms.json apply (no tooltip-only foci, no unpaid buildings, no stand-alone small combat buffs, stability ≤ +0.06 and PP ≤ 150 outside capstones, ≤ 6 dyn/prog lines per focus, tech b ≤ 1.0 and ≤ 3 uses).
5. **Multiplayer:** nothing executed in another country's scope; diplomacy only through the existing `offer` effects (keep them). No forced war, alliance, bases, territory.
6. **Oil is player-only:** no effect that moves the oil price or OPEC level; reading `global.mdcw_cw_oil_ratio` is fine.
7. **No parallel systems:** use the existing Imperia/Cold War modifiers and ideas (`mdcw_cw_*` modifiers, `imp_*` modifiers, Cold War ideas like `mdcw_cw_show_of_strength`, Imperia national idea discount windows) as the hooks file proposes. Dynamic-modifier keys must be real modifiers (reference.extra_valid_modifiers_mod_defined or vanilla HOI4 modifiers already used in reference.dyn_groups_existing_keys / ideas).
8. **Politburo/system foci:** plenum candidacy foci (section ple), power foci (`power_*`), direction foci (`dir_*`), resolution foci (they contain a "Politbüro-Beschluss" note), heirs and General-Secretary entry foci keep their system effects; you may still tune their bundle.
9. English only for any text you write.

## Final message
Report: number of foci reviewed, number fixed, the 5 most important kinds of problems you found (with 2 example ids each), new ideas created, and anything you were unsure about. Under 300 words.
