# Union Missions and the Joint Union Tree: Implementation Plan

Feasibility study, 18.10.2026. Read-only audit. Nothing has been built.

**Scope**
- The approved concept `/home/claude/mdcw_union_missions_concept.md` (German).
- The author's decision: the shared Union tree uses `joint_focus`, Saadabad style.

**Base**
- Cold War mod on MD 2.0.2 and HOI4 1.19.
- Generator `/home/claude/sovgen` and its output `out/`.

**Evidence labels**

| Label | Meaning |
|---|---|
| **[MD]** | Shipping MD 2.0.2 script. File and line are under `/mnt/user-data/uploads/mdcoldwar/`. |
| **[OURS]** | Already in our generated SOV output. It is statically validated but **not yet tested in game**: `mdcw_sov_1970_implementation.md` §"Status" says the first 1970 start is still open. |
| **[V]** | Vanilla engine feature, documented or stated by the developers, but not used by MD or by us. |
| **[I]** | Our inference. |
| **[TEST]** | Must be confirmed in game. See §7. |

---

## 0. Recommendation in short

1. **Attach the Union branch to the existing trees.**
   - Write one joint-focus file, `common/national_focus/COLDWAR_UNI_1970_union_joint.txt`.
   - Attach it to `COLDWAR_SOV_1970_focus` and `mdcw_1970_generic_focus` with one `shared_focus =` line each.
   - Place it per tree with `offset = { trigger = { has_focus_tree = … } }`.
   - **Do not create a separate republic tree.** The SSRs would lose the 349 generic foci. Generic foci are plain `focus` blocks and cannot be shared into another tree.
2. **The Union tree is all joint, Saadabad style.** Each focus states who may *originate* it:
   - Moscow only (`JOINT_SOV_focus_style` title bar)
   - republics only
   - any member

   Members receive only positive rewards. Per-republic tools are **decisions unlocked union-wide** by the joint focus, so each republic uses or ignores them itself. Plain `shared_focus` is kept in reserve for leaves that every republic must take separately; the skeleton needs none.
3. **Missions are a system independent of the tree.** It is driven from the January Politburo session (`COLDWAR_SOV.10`). Annual targets and Moscow's directives are mission decisions (`days_mission_timeout`), activated with `activate_mission` in the republic's scope. A timeout sends the judgement event `COLDWAR_UNI.10` to Moscow.
4. **Targets are measured with MD's weekly building totals.** `update_state_variables` provides `industrial_complex_total`, `agriculture_district_total`, `number_of_fossil_pps` and others. A baseline variable is taken when the mission starts. No new per-republic meter is needed: only baselines, flags and two small per-plan counters.
5. **Prefix `COLDWAR_UNI_`, namespace `COLDWAR_UNI`.** Build it in `sovgen` as a new module `cw_union.py` with its own output files. Make small hooks into `cw_events`, `cw_sys_effects`, `cw_misc`, `cw_focus`, `cw_layout`, `cw_build` and `validate_sov`.
6. **Prerequisite: smoke-test the SOV 1970 system in game first.** The mission system builds on the vote engine, the session event, cohesion and the money helpers, and none of them has run in game yet.

---

## 1. Joint focus architecture

### 1.1 What is known about joint foci (MD usage and developer statements)

| Item | Behaviour | Evidence |
|---|---|---|
| Block keyword | `joint_focus = { … }` at file top level in `common/national_focus/`. A file may mix it with `shared_focus = { … }`. | [MD] `06_czehcoslavakia_shared.txt`: 26 joint and 33 shared foci |
| Attaching to a tree | `shared_focus = <root id>` inside `focus_tree`. The same line works for joint roots. | [MD] `05_russia.txt:10-12` attaches `CHI_SOV_treaty_good_neighbourliness` |
| Shared child under a joint parent | Works. `CZE_SLO_defensive_posture` (shared, l.924) has `prerequisite = { focus = CZE_SLO_no_more_dividing }` (joint, l.876). The same holds at l.1263, l.1443, l.2037, l.2550 and l.2663. | [MD]. This closes the old "[U] can shared hang under joint?" question. |
| Who is a member | Every country whose `joint_trigger` (THIS = candidate) is true **and** that has the focus in its tree. MD always includes the root in every member's tree. | [MD] for tag lists, scripted triggers and dynamic modifiers. The "focus must be in the tree" part is [I/TEST]. |
| Root without `joint_trigger` | MERCOSUR's root `BRA_americas_unity` has none (`06_MERCOSUR_shared.txt:2-86`). Its `completion_reward` still fires a per-member invitation, guarded by `NOT = { has_country_flag = mercosur.30_received }`. | [MD]. Behaviour is unclear: **always set `joint_trigger`**. |
| Who may research | `available` is checked for the originator only. Moscow-only example: `CHI_SOV_turn_to_east`, `available = { original_tag = SOV … }` (`03_china_russia_joint.txt:146-149`). CHI-only: `CHI_SOV_bri_russia_corridor` (l.198-201). | [MD] |
| `completion_reward` | Runs in **every** member's own scope, the originator included. Benelux uses it for per-member dynamic modifier variables (`03_benelux_shared.txt:22-29`). | [MD] |
| `completion_reward_joint_originator` | Runs for the completer only. Examples: Benelux +150 PP (l.31-34), CZE −7.5 treasury (l.190-193). | [MD] |
| `completion_reward_joint_member` | Runs for every member **except** the completer. Examples: Benelux +50 PP, CZE +7.5 treasury (l.195-198), and the MP-safe offer at CZE l.289-292: `country_event = CZE_SLO_event.1`. | [MD]. FROM inside it is unknown [TEST]. |
| Fixed-tag effects | `SOV = { … }` placed in `completion_reward` runs once **per member**. MD `CHI_SOV_bri_russia_corridor` (l.203-220) adds `SOV`/`CHI` variables inside `completion_reward` with two members, so it probably applies twice. | [I], and an MD pitfall to avoid. Put one-off and global effects in `_originator`. |
| `select_effect` | Runs when the originator *selects* the focus. MERCOSUR uses it for an AI de-duplication flag: `select_effect = { set_global_flag = BRA_americas_unity_in_progress }` plus `ai_will_do = { modifier = { add = -1000 has_global_flag = … } }` (l.74-85). The flag is never cleared, so a cancelled research blocks the AI for good. | [MD]. Our fix: a timed global flag `set_global_flag = { flag = X days = N }`, the syntax used at `MD_on_actions.txt:11`. |
| Parallel research | Developers: while one member researches a joint focus, the others see its flag and cannot pick it. MD still adds AI flags. | [V]/[TEST] |
| Focus slot, running focus | The joint focus uses the originator's slot. Members' running foci are not touched. | [V]/[TEST] |
| Members' prerequisites | Continuous members share every joint completion, so prerequisites are automatically equal. Late joiners and leavers are undocumented. | [I]/[TEST] |
| `has_completed_focus` inside its own reward | False | [V] |
| `allow_branch` and `offset` | Evaluated at tree load and on `mark_focus_tree_layout_dirty = yes` | [V], [MD] `00_focus_utilities.txt` |
| Title bar | `text_icon = JOINT_SOV_focus_style` (red Soviet bar) exists, with sprites, at `00_titlebar_styles.txt:263-269`. Without `text_icon` the default bar is used (CZE file). | [MD] |

### 1.2 Hosting: recommendation A (attach), not B (own republic tree)

| | **A: attach to `mdcw_1970_generic_focus` and `COLDWAR_SOV_1970_focus` (recommended)** | B: new `COLDWAR_UNI_1970_republic_focus` for the 14 SSRs |
|---|---|---|
| SSR content | Keeps all 349 generic foci (politics, economy, outlooks) | Loses them. Generic foci are not shared foci and cannot be included elsewhere. |
| Code | One header line in each host tree | New tree, 14 history patches, and 14 tags added to the fallback whitelist in `mdcw_load_1970_fallback_tree` |
| Coupling | The generic tree is produced by `/home/claude/gentools/generic_1970_focus_tree/generate_1970_generic_focus_tree.py` (header at l.346-356). One `w(...)` line must be added there. | None outside sovgen |
| Load cost | `allow_branch` is evaluated for every generic-tree user at load; it is a tag list, so cheap. | None |
| Crash risk | A missing `shared_focus` ID crashes at the main menu ([V], see `hoi4_shared_focus_mechanics.md` §1.2). The union file and the header line must therefore always ship together. Validator check in §6.4. | Same for the SOV tree |

**Change in the generic generator**, after l.352, before the shortcuts:

```python
w('\tshared_focus = COLDWAR_UNI_the_union_plan   # COLDWAR | Union branch (joint); allow_branch shows it to SOV and the 14 SSRs only')
```

- If the generic generator must not be touched, `cw_build.py` can patch the output file, like it already patches `mdcw_1970_focus_tree_effects.txt` (l.65-71): assert an anchor, insert the line, and write `common/national_focus/mdcw_1970_generic_focus.txt` to `out/`.
- Two generators would then own one file. Prefer the one-line change in the generic generator.

**SOV header** (`cw_focus.focus_file`, l.224-233). Add the attach line and an 11th shortcut:

```
	shared_focus = COLDWAR_UNI_the_union_plan
	shortcut = { name = COLDWAR_SOV_shortcut_union_plan target = COLDWAR_UNI_the_union_plan scroll_wheel_factor = 0.80 }   # [TEST] shortcut to a joint focus
```

- Do **not** add a shortcut to the generic tree. Shortcuts have no trigger, and for the roughly 250 non-SSR users the target would be hidden [U].

### 1.3 Placement (free space)

- **SOV tree.** The canvas is 427 × 19 (x 0-426, y 0-18).
  - Measured from `out/`: block `state_union` spans x 325-377 with its deepest focus at y 5. The continuous-focus panel sits at x 325-331, y 8-13 (`continuous_focus_position = { x = 31200 y = 1040 }`, from `cw_focus._continuous_pocket`).
  - Free box: **x 334-377 × y 7-18** (44 × 12). It lies directly under "The Union of Republics", which is the thematically right place, and the canvas stays 427 wide.
  - The alternative is x ≥ 430, which widens the tree.
- **Generic tree.** Foci span x 0-226 × y 0-7. The continuous panel is at about x 0, y 9.6.
  - Place the branch at **x 232, y 0** (MD style: wide, shallow).
- **One definition for both trees.** The default position is for SOV; one offset handles the generic tree. Offsets keyed on the host tree follow the Commonwealth pattern (`Commonwealth_shared.txt:12-21`).

```
	x = 336
	y = 8
	offset = { x = -104 y = -8 trigger = { has_focus_tree = mdcw_1970_generic_focus } }   # -> (232, 0)
```

- **Layout guard.**
  - `cw_layout`/`cw_focus._continuous_pocket` must treat the union box (`UNION_BOX = (334, 7, 377, 18)`) as occupied. Otherwise a future relayout can put the continuous panel over it.
  - The validator also checks that no SOV focus and no part of the continuous-panel box intersects the union box.

### 1.4 Membership, originators and rewards (code sketches)

**Scripted triggers**, new file `common/scripted_triggers/COLDWAR_UNI_1970_scripted_triggers.txt`:

```
# who receives joint completions (THIS = candidate)
COLDWAR_UNI_is_member = {
	OR = {
		AND = { original_tag = SOV has_global_flag = COLDWAR_SOV_politburo_system }
		AND = {
			COLDWAR_SOV_is_union_republic = yes                              # is_subject_of = SOV + 14 tags (existing, l.6)
			NOT = { has_idea = COLDWAR_SOV_declaration_of_sovereignty }      # opt-out by sovereignty (author decision, §8)
		}
	}
}
# load-order-proof static list for allow_branch / category "allowed" (subject relations may not exist yet at tree load)
COLDWAR_UNI_union_tag = {
	OR = { original_tag = SOV original_tag = UKR original_tag = BLR original_tag = EST original_tag = LAT original_tag = LIT
	       original_tag = ARM original_tag = AZE original_tag = GEO original_tag = KAZ original_tag = KYR original_tag = TAJ
	       original_tag = TRK original_tag = UZB original_tag = MLV }
}
```

Why `allow_branch` uses tags rather than `is_subject_of` [I/TEST]:
- At tree load, SOV's history may not have run `set_autonomy` yet. A live subject test could then hide the branch for every SSR.
- MD's CZE, Benelux and CHI roots all use static tag lists in `allow_branch`.
- Live membership goes into `joint_trigger` and `available`.

**Root**, any member may originate it (`COLDWAR_UNI_1970_union_joint.txt`):

```
joint_focus = {
	id = COLDWAR_UNI_the_union_plan
	icon = GFX_COLDWAR_goal_…                      # via cw_focus.icon_of / goal_sprites.json
	x = 336
	y = 8
	offset = { x = -104 y = -8 trigger = { has_focus_tree = mdcw_1970_generic_focus } }
	cost = 2
	allow_branch = {
		COLDWAR_UNI_union_tag = yes
		NOT = { has_country_flag = COLDWAR_UNI_left_union }       # set on leaving + mark_focus_tree_layout_dirty
	}
	search_filters = { FOCUS_FILTER_INDUSTRY FOCUS_FILTER_POLITICAL }
	joint_trigger = { COLDWAR_UNI_is_member = yes }
	available = { COLDWAR_UNI_is_member = yes }
	select_effect = { set_global_flag = { flag = COLDWAR_UNI_the_union_plan_in_progress days = 30 } }
	completion_reward = {                          # every member, own scope only: no fixed tags, no globals, no costs
		log = "[GetDateText]: [Root.GetName]: Focus COLDWAR_UNI_the_union_plan"
		add_political_power = 10
		set_country_flag = COLDWAR_UNI_tree_started
	}
	completion_reward_joint_originator = {         # once: globals and the originator bonus go here
		add_political_power = 25
		custom_effect_tooltip = COLDWAR_UNI_joint_all_members_tt     # "Completes for Moscow and every Union republic."
	}
	ai_will_do = { base = 10 modifier = { factor = 0 has_global_flag = COLDWAR_UNI_the_union_plan_in_progress } }
}
```

**Moscow-only lever.** The Belgium–Congo "single flag" pattern, shown as in `03_china_russia_joint.txt:124-174`:

```
joint_focus = {
	id = COLDWAR_UNI_gosplan_directives
	text_icon = JOINT_SOV_focus_style              # red bar = only Moscow can take it
	x = -3  y = 1  relative_position_id = COLDWAR_UNI_the_union_plan
	cost = 3
	prerequisite = { focus = COLDWAR_UNI_the_union_plan }
	search_filters = { FOCUS_FILTER_INDUSTRY }
	joint_trigger = { COLDWAR_UNI_is_member = yes }
	available = { original_tag = SOV }
	completion_reward_joint_originator = {
		log = "[GetDateText]: [Root.GetName]: Focus COLDWAR_UNI_gosplan_directives"
		set_country_flag = COLDWAR_UNI_cheap_directives            # directive 15 PP instead of 25 (§2.4)
		custom_effect_tooltip = COLDWAR_UNI_cheap_directives_tt
	}
	completion_reward_joint_member = { add_political_power = 15 }  # positive only
	ai_will_do = { base = 5 }
}
```

**Republic-originated tool.** It unlocks a decision for every republic:

```
joint_focus = {
	id = COLDWAR_UNI_the_tolkachi
	x = 1  y = 1  relative_position_id = COLDWAR_UNI_the_union_plan
	cost = 3
	prerequisite = { focus = COLDWAR_UNI_the_union_plan }
	search_filters = { FOCUS_FILTER_INDUSTRY }
	joint_trigger = { COLDWAR_UNI_is_member = yes }
	available = { COLDWAR_SOV_is_union_republic = yes }          # only republics originate
	select_effect = { set_global_flag = { flag = COLDWAR_UNI_the_tolkachi_in_progress days = 35 } }
	completion_reward = {
		log = "[GetDateText]: [Root.GetName]: Focus COLDWAR_UNI_the_tolkachi"
		if = { limit = { COLDWAR_SOV_is_union_republic = yes } set_country_flag = COLDWAR_UNI_tolkachi_unlocked }
		custom_effect_tooltip = COLDWAR_UNI_tolkachi_unlock_tt     # "Every Union republic may use Send the Tolkachi (once per plan)."
	}
	completion_reward_joint_originator = { add_political_power = 25 }
	ai_will_do = { base = 3 modifier = { factor = 0 has_global_flag = COLDWAR_UNI_the_tolkachi_in_progress } }
}
```

**Rules the generator enforces** (validator §6.4):
- Every `joint_focus` has `joint_trigger = { COLDWAR_UNI_is_member = yes }`.
- No `mutually_exclusive` in the joint branch.
- `completion_reward` and `completion_reward_joint_member` contain no negative values, no `treasury_change = -`, no `cohesion_delta = -`, no fixed-tag scopes (`SOV = {`, `UKR = {` …) and no global writes. Costs only go into `_originator`.
- Every focus has `select_effect` with a timed in-progress flag and the matching `ai_will_do` factor.
- No `complete_national_focus`, `unlock_national_focus` or `uncomplete_national_focus` is used on members.

### 1.5 Multiplayer safety and player control

- **Nothing negative reaches a player through the tree.** A joint completion only grants positive rewards, flags or unlocked decisions. Costs (stability, PP, treasury) are paid by whoever *uses* a tool decision or *originates* a focus.
- **Membership is automatic for Union republics. Opting in is not needed** because membership has no downside.
  - **Opt-out** is the existing national path: a Declaration of Sovereignty (if the author agrees, §8) ends union-tree membership, and independence ends it in any case.
  - On leaving, set `COLDWAR_UNI_left_union` and call `mark_focus_tree_layout_dirty = yes` on the republic. Hooks: event `COLDWAR_SOV.24` "Recognise", event `COLDWAR_SOV.60` accept, and the vanilla on_action `on_subject_free` (listed in `common/on_actions/_documentation.md:57`; scope [TEST]).
- **Originator race.**
  - Keep originator bonuses small. Saadabad uses about 100 % for the originator and 60-70 % for members. Then sniping a focus gains little.
  - Moscow-only foci cannot be sniped (`available`).
- **Missions are not part of the tree.** Punishments exist only after a **failed** mission, with escalation limits (§2.5). This is the concept's §10 exception to the "offers only" rule, and the author must adopt that sentence into the MP rule.

### 1.6 AI

- **AI SOV:** moderate weights on the Moscow-only foci (base 5).
- **AI SSRs:** low weights (base 2-5) on republic foci, the timed in-progress de-duplication, and `factor = 0` while the originator condition is false. AI weights may use dates; only `available` must not (README 17.10.2026).
- **Optional.** The vanilla Nordic tree keeps the AI from starting the joint tree at all. If AI SSRs race human players too much, add `modifier = { factor = 0.2 any_country = { COLDWAR_SOV_is_union_republic = yes is_ai = no } }`.

### 1.7 Proposed skeleton of the branch (about 12 foci, 4 rows, about 20 columns)

| Row | ID (`COLDWAR_UNI_…`) | Originator | Cost | Every member (`completion_reward`) | Originator | Member |
|---|---|---|---|---|---|---|
| 0 | `the_union_plan` | any member | 2 | +10 PP, flag `tree_started` | +25 PP | – |
| 1 | `gosplan_directives` | SOV | 3 | – | directive cost 15 PP | +15 PP |
| 1 | `the_peoples_control` | SOV | 3 | – | flag `peoples_control`: an audit of reported fulfilments at the settlement (§2.8); investigation cost −25 PP | +10 PP |
| 1 | `the_tolkachi` | republic | 3 | republics: decision "Send the Tolkachi" | +25 PP | – |
| 1 | `storming_the_plan` | republic | 3 | republics: decision "Storm the Plan" | +25 PP | – |
| 1 | `the_counter_plan` | republic | 3 | republics: decision "Adopt a Counter-Plan" | +25 PP | – |
| 2 | `keep_reserves_in_hand` | republic | 3 | republics: flag `reserves` (audit chance −10) | +25 PP | – |
| 2 | `socialist_emulation` | any member | 3 | Red Banner flag (optional, concept §6) | +25 PP | – |
| 2 | `the_plan_year_fulfilled` | any member, `available` = `global.COLDWAR_UNI_years_fulfilled > 0` | 5 | +1 % stability, +25 PP | +25 PP | – |
| 3 | four plan capstones (IX–XII) | any member, gated by `global.COLDWAR_UNI_years_fulfilled` thresholds (2/4/6/8), not by dates | 5 | small timed idea | +50 PP | – |

- Expansion from `shared_union_tree_ideas.md` (megaprojects, endgame) can follow the same pattern later.
- The General Secretary rules are **not** foci here. They read the existing SOV flags (§4.5).

---

## 2. Missions

### 2.1 Proven mission syntax

| Need | Syntax | Evidence |
|---|---|---|
| Mission = decision with a timer | `days_mission_timeout = N` | [MD] `Russia.txt:4029, 4823, 5601, 7123` |
| Timer from a variable | `days_mission_timeout = <country var>` | [MD] `investments_decisions.txt:481` (`project_target_construction_duration`, set before activation in `99_investment_scripted_effects.txt:650-656`) |
| Started only by script | `allowed = { always = no }` + `activate_mission = X` in the owner's scope | [MD] `Russia.txt:4817-4822` (`SOV_reunification_mission`) and l.4562 |
| Success = `available` true → `complete_effect` | `available = { has_country_flag = SOV_mission_space_ended }` | [MD] `Russia.txt:5586-5622` (Buran hangar) |
| Failure | `timeout_effect` | [MD] same |
| Success via cancel (alternative) | `cancel_trigger` → `cancel_effect` | [MD] `Russia.txt:4026-4046`, l.7121-7148 |
| Re-arming inside its own timeout | `activate_mission = SOV_reunification_mission` inside its `timeout_effect` | [MD] `Russia.txt:4823-4862` (Tolkachi pattern) |
| Status / removal | `has_active_mission = X`, `remove_mission = X` | [MD] `05_ukraine.txt:992`, `MD_on_actions.txt:314` |
| Targeted decision | `targets = { UKR … }`, `target_trigger = { FROM = { … } }` | [OURS] `COLDWAR_SOV_appoint_seat` (decisions l.922-934) |
| Dynamic cost | `custom_cost_trigger`, `custom_cost_text` | [MD] `Russia.txt:32ff, 5636ff` |

### 2.2 Two families, one table

- **Mission types** are generated from one Python table (`cw_union.MISSIONS`). Each type is one measurement key:

| key | Measures | Concept missions using it |
|---|---|---|
| `civ` | civilian factory +1 | 1 Industrial Plan |
| `arms` / `civ_or_arms` | military factory, or either | Steel and Tractors (armaments priority: arms only, reward ×1.5) |
| `power` | fossil, nuclear or renewable plant +1 | 2 Power for the Plan, Nurek and Toktogul (directive) |
| `nuclear` | nuclear reactor +1 | Atoms for the Republic (directive) |
| `agri` | agriculture district +1 | 3 Harvest Quota, White Gold, Virgin Lands, Orchards and Vineyards |
| `infra_any` / `infra_two` / `infra_state` | infrastructure +1 in any state, in two states, or in one named state | 4 Roads of the Union, Baikonur |
| `dock` | dockyard +1 | Ports of the Union |
| `refinery` | synthetic refinery +1 | AZE oil (Black Sea and Caspian) |
| `deliver` | decision "Deliver to the Union Fund" taken | 5 Plan Deliveries |
| `stability` | stability ≥ 50 % at the deadline | 6 Party Discipline |
| `komsomol` | decision "Send the Komsomol Brigades" taken | 7 Komsomol Brigades |
| `corruption` | corruption one level below the start | 8 Clean Up the Apparatus (directive only) |

- **Two families:**
  - `COLDWAR_UNI_target_<key>`: the annual target, baseline variables `COLDWAR_UNI_t_*`.
  - `COLDWAR_UNI_directive_<key>`: Moscow's directive, baseline variables `COLDWAR_UNI_d_*`.
  - About 2 × 14 ≈ 28 mission decisions.
  - A country can run each mission only once at a time, so the two families must be separate decisions.
  - A directive may not use the key of the running annual target; the option trigger enforces this. One factory then never satisfies both.
- **Regional names.**
  - The decision name contains a scripted-loc call, for example `COLDWAR_UNI_target_agri: "[COLDWAR_UNI_GetHarvestName]"` → "White Gold" for UZB/TAJ/TRK/KYR, "Virgin Lands Harvest" for KAZ, "Orchards and Vineyards" for MLV, otherwise "The Harvest Quota".
  - Scripted loc in decision titles and descriptions works in our decision descriptions [OURS: `[COLDWAR_SOV_GetPlanName]`]. For mission titles it is [TEST].
  - The fallback is one decision per regional variant: more decisions, same code.

**Mission sketch**, generated from the table (`common/decisions/COLDWAR_UNI_1970_decisions.txt`):

```
COLDWAR_UNI_republic_plan_category = {
	COLDWAR_UNI_target_civ = {
		icon = GFX_decision_generic_factory
		allowed = { always = no }                       # started only by activate_mission (MD SOV_reunification_mission)
		activation = { always = no }
		fire_only_once = no
		is_good = yes
		selectable_mission = no
		days_mission_timeout = COLDWAR_UNI_t_days       # variable (MD investments)
		available = {
			OR = {
				custom_trigger_tooltip = {
					tooltip = COLDWAR_UNI_goal_civ_tt       # "A new civilian factory: now §Y[?industrial_complex_total]§!, at the start §Y[?COLDWAR_UNI_t_base]§!."
					check_variable = { industrial_complex_total > COLDWAR_UNI_t_base }
				}
				hidden_trigger = { has_country_flag = COLDWAR_UNI_t_reported }   # pripiski (§2.8)
				hidden_trigger = { has_country_flag = COLDWAR_UNI_t_stormed }    # Storming the Plan
				hidden_trigger = { has_country_flag = COLDWAR_UNI_t_ai_done }    # AI floor fallback
			}
		}
		cancel_trigger = { NOT = { COLDWAR_SOV_is_union_republic = yes } }
		cancel_effect = { log = "[GetDateText]: [Root.GetName]: Mission cancelled COLDWAR_UNI_target_civ" COLDWAR_UNI_clear_target = yes }
		complete_effect = {
			log = "[GetDateText]: [Root.GetName]: Mission COLDWAR_UNI_target_civ"
			set_temp_variable = { COLDWAR_UNI_key = 1 }          # 1 = civ (table index)
			COLDWAR_UNI_target_success = yes                       # reward, Moscow's share, flags (§5)
		}
		timeout_effect = {
			log = "[GetDateText]: [Root.GetName]: Mission timeout COLDWAR_UNI_target_civ"
			custom_effect_tooltip = COLDWAR_UNI_failure_tt        # "Moscow judges the failure. [COLDWAR_UNI_GetJudgementLevels]"
			COLDWAR_UNI_target_failure = yes
		}
		ai_will_do = { base = 0 }
	}
	# … one block per key, plus COLDWAR_UNI_directive_<key> with d_ variables
}
```

**Deadline-evaluated types** (`stability`): `available = { always = no }`, and the `timeout_effect` branches. This is the Buran/reunification pattern:

```
timeout_effect = {
	if = { limit = { has_stability > 0.49 } set_temp_variable = { COLDWAR_UNI_key = 10 } COLDWAR_UNI_target_success = yes }
	else = { COLDWAR_UNI_target_failure = yes }
}
```

### 2.3 Annual targets from the January session

**Hook.** In `cw_events.SESSION` (l.96-104) the January session is the branch that sets `global.COLDWAR_SOV_session_half` from 1 to 0:
- The chain is: `on_startup` → `COLDWAR_SOV.10` after 181 days ≈ 1 Jul 1970; then 184 days ≈ 1 Jan 1971; then alternating.
- Extra sessions (flag `COLDWAR_SOV_extra_session`) skip that branch, so they never issue targets.
- Mark the branch with a temp variable and call the hook **after** the plan-start lines, so a new plan number is already set:

```python
# cw_events.SESSION, inside the session_half = 1 branch:
f"set_temp_variable = {{ COLDWAR_UNI_january = 1 }}",
# … after the four plan-start ifs:
"if = { limit = { check_variable = { COLDWAR_UNI_january = 1 } } COLDWAR_UNI_january_session = yes }",
```

**Scripted effects** (`common/scripted_effects/COLDWAR_UNI_1970_scripted_effects.txt`):

```
COLDWAR_UNI_january_session = {                      # SOV scope
	if = { limit = { has_global_flag = COLDWAR_UNI_system } COLDWAR_UNI_settle_year = yes }   # §5; not in Jan 1971
	set_global_flag = COLDWAR_UNI_system
	country_event = { id = COLDWAR_UNI.1 days = 14 }   # Gosplan publishes the targets 14 days later:
}                                                     # Moscow can still set the priority of a new plan (COLDWAR_SOV_start_plan removed it)

# COLDWAR_UNI.1 (hidden, SOV) immediate:
every_country = {
	limit = { COLDWAR_SOV_is_union_republic = yes NOT = { has_country_flag = COLDWAR_UNI_target_active } }
	COLDWAR_UNI_issue_annual_target = yes
}
news_event = { id = COLDWAR_UNI.2 hours = 6 }          # "Gosplan Publishes the Plan for the Year"

COLDWAR_UNI_issue_annual_target = {                    # republic scope
	set_variable = { COLDWAR_UNI_t_days = 300 }
	set_temp_variable_to_random = { var = COLDWAR_UNI_r min = 0 max = 21 }
	round_temp_variable = COLDWAR_UNI_r
	add_to_variable = { COLDWAR_UNI_t_days = COLDWAR_UNI_r }   # stagger: deadlines spread over three weeks (judgement spam, §7)
	clr_country_flag = COLDWAR_UNI_target_fulfilled
	clr_country_flag = COLDWAR_UNI_target_failed
	clr_country_flag = COLDWAR_UNI_t_reported
	clr_country_flag = COLDWAR_UNI_t_stormed
	clr_country_flag = COLDWAR_UNI_t_ai_done
	set_country_flag = COLDWAR_UNI_target_active
	# type: Moscow's plan priority (ideas on SOV, PLAN_PRIOS in cw_sys_effects.py:532) + the republic's region
	if = {
		limit = { SOV = { has_idea = COLDWAR_SOV_plan_armaments } OR = { original_tag = UKR original_tag = BLR } }
		set_variable = { COLDWAR_UNI_t_base = military_factory_total }
		set_variable = { COLDWAR_UNI_t_key = 2 }
		activate_mission = COLDWAR_UNI_target_arms
	}
	else_if = {
		limit = { SOV = { has_idea = COLDWAR_SOV_plan_agriculture } }
		set_variable = { COLDWAR_UNI_t_base = agriculture_district_total }
		set_variable = { COLDWAR_UNI_t_key = 5 }
		activate_mission = COLDWAR_UNI_target_agri        # regional name via scripted loc
	}
	else_if = {
		limit = { SOV = { has_idea = COLDWAR_SOV_plan_group_b } }
		COLDWAR_UNI_start_roads_or_discipline = yes        # alternates by year parity
	}
	else = { COLDWAR_UNI_start_regional_default = yes }    # Group A or no priority yet: industry / ports / harvest by region
	if = { limit = { is_ai = yes } COLDWAR_UNI_ai_floor_roll = yes }
	country_event = { id = COLDWAR_UNI.3 days = 1 }         # notice: target, deadline, [COLDWAR_UNI_GetJudgementLevels]
}
```

**Timing defaults** (author to confirm, §8):
- The annual target runs 300-321 days and ends by early December.
- The judgement event has a 15-day timeout.
- So every annual result is known before the next January settlement.
- With the concept's 365 days plus 90 for the Tolkachi, missions would overlap the next issue.

### 2.4 Moscow's directives (maximum 2 per republic and plan)

- **Category.** A new SOV category, `COLDWAR_UNI_gosplan_category` "Gosplan and the Republics":
  - `allowed = { original_tag = SOV }`
  - `visible = { has_global_flag = COLDWAR_UNI_system }`
- Generated with a prefix-aware copy of `cw_decisions.dec` (l.22-45).

```
COLDWAR_UNI_issue_directive = {
	icon = GFX_decision_generic_industry
	cost = 25                                   # variant _cheap with cost = 15 and visible = { has_country_flag = COLDWAR_UNI_cheap_directives }
	fire_only_once = no
	target_root_trigger = { always = yes }
	targets = { UKR BLR EST LAT LIT ARM AZE GEO KAZ KYR TAJ TRK UZB MLV }
	target_non_existing = no
	target_trigger = {
		FROM = {
			COLDWAR_SOV_is_union_republic = yes
			NOT = { has_country_flag = COLDWAR_UNI_directive_active }
			NOT = { AND = { check_variable = { COLDWAR_UNI_dir_plan = global.COLDWAR_SOV_plan } check_variable = { COLDWAR_UNI_dir_count > 1 } } }
		}
	}
	visible = { NOT = { has_country_flag = COLDWAR_UNI_cheap_directives } }
	available = { NOT = { has_global_flag = COLDWAR_UNI_directive_drafting } }
	complete_effect = {
		log = "[GetDateText]: [Root.GetName]: Decision COLDWAR_UNI_issue_directive"
		FROM = { set_country_flag = COLDWAR_UNI_directive_pending }
		set_global_flag = COLDWAR_UNI_directive_drafting
		country_event = { id = COLDWAR_UNI.20 }      # choose the directive
	}
	ai_will_do = { base = 0 }                       # AI Moscow issues no directives (concept §8)
}
```

**Event `COLDWAR_UNI.20`** "Gosplan Drafts a Directive":
- Text: "for [COLDWAR_UNI_GetDirectiveTarget]", using the flag-based scripted loc of `COLDWAR_SOV_GetAccused`.
- `timeout_days = 7`.
- **The first option is "Shelve the draft"**, which refunds the cost. On timeout the first option applies [V; our event 11 relies on the same rule].
- Each further option has a trigger such as `any_country = { has_country_flag = COLDWAR_UNI_directive_pending COLDWAR_UNI_region_baltic = yes NOT = { check_variable = { COLDWAR_UNI_t_key = 8 } } }`.
- Effect:

```
every_country = {
	limit = { has_country_flag = COLDWAR_UNI_directive_pending }
	clr_country_flag = COLDWAR_UNI_directive_pending
	COLDWAR_UNI_count_directive = yes        # dir_plan / dir_count, reset when the plan number changes
	set_variable = { COLDWAR_UNI_d_days = 270 }
	set_variable = { COLDWAR_UNI_d_base = naval_factory_total }
	set_variable = { COLDWAR_UNI_d_key = 8 }
	set_country_flag = COLDWAR_UNI_directive_active
	activate_mission = COLDWAR_UNI_directive_dock
	country_event = { id = COLDWAR_UNI.21 days = 1 }   # the republic is told; nothing to accept (a directive is an order)
}
clr_global_flag = COLDWAR_UNI_directive_drafting
```

### 2.5 Timeout → Moscow's judgement

**`COLDWAR_UNI_target_failure`** (republic scope, also used by directives):

```
COLDWAR_UNI_target_failure = {
	set_country_flag = COLDWAR_UNI_target_failed
	clr_country_flag = COLDWAR_UNI_target_active
	COLDWAR_UNI_count_failure = yes                   # fail_plan / fail_count (resets with the plan number)
	if = {
		limit = { SOV = { COLDWAR_UNI_khozraschet_rule = yes } }   # Gorbachev: no judgement (§4.5)
		add_timed_idea = { idea = COLDWAR_SOV_plan_shortfall days = 365 }
	}
	else = { SOV = { country_event = { id = COLDWAR_UNI.10 days = 1 } } }   # FROM = this republic ([OURS] pattern, e.g. proposals -> event 20)
}
```

**Judgement event `COLDWAR_UNI.10`** "Plan Failure in [FROM.GetNameDef]":
- `timeout_days = 15`.
- Option letters skip `d`/`t` (`cw_misc.OPT_LETTERS`).

| Option | Trigger (`FROM` = republic) | Effect | AI chance (SOV) |
|---|---|---|---|
| **a – 0 Accept Their Explanations** (first, so it is the timeout default) | none | `FROM = { country_event = COLDWAR_UNI.16 }`. Cohesion +1 only if `NOT = { has_country_flag = COLDWAR_UNI_pardon_bonus }` (365-day flag). BOP 0.01 toward reform. | ×4 with `gensec_kos`/`gensec_gor` |
| **b – 1 A Severe Party Reprimand** | `FROM = { COLDWAR_UNI_level1_allowed = yes }` | `FROM = { add_political_power = -50 add_timed_idea = { idea = COLDWAR_UNI_reprimanded days = 90 } country_event = COLDWAR_UNI.11 }`. BOP 0.01 orthodox. `COLDWAR_UNI_moscow_punishment_cost = yes`. | ×4 with `gensec_bre` |
| **c – 2a Requisition Their Capacity** | `FROM = { COLDWAR_UNI_level2_allowed = yes check_variable = { industrial_complex_total > 0 } }` | §4.1 | ×4 with an orthodox General Secretary (`sus`, `and`, `gro`, `ust`, `gre`) |
| **e – 2b Gosplan Takes the Offices** | level 2 + `FROM = { check_variable = { office_park_total > 0 } }` (only UKR, BLR and KAZ have offices in 1970) | §4.1 | ×2 orthodox |
| **f – 2c Levy the Shortfall** | level 2 | §4.1 | ×2 orthodox |
| **g – 3 Replace the First Secretary** | `FROM = { COLDWAR_UNI_level3_allowed = yes }`, `NOT = { has_global_flag = COLDWAR_SOV_vote_running }`, `has_political_power > 99` | Puts the cadre question to the Politburo (§4.2) | ×2 orthodox with `FROM = { has_country_flag = COLDWAR_UNI_pripiski_exposed }` |

- Hidden options are invisible, so the description says why a level is missing: `[FROM.COLDWAR_UNI_GetJudgementLevels]` (§2.6).
- Every punishing option calls `COLDWAR_UNI_moscow_punishment_cost`:

```
COLDWAR_UNI_moscow_punishment_cost = {      # SOV scope; temp COLDWAR_UNI_lvl = 1/2/3
	set_temp_variable = { COLDWAR_SOV_cohesion_delta = 0 }
	if = { limit = { check_variable = { COLDWAR_UNI_lvl = 2 } NOT = { has_country_flag = COLDWAR_SOV_iron_discipline } } add_to_temp_variable = { COLDWAR_SOV_cohesion_delta = -1 } }   # Romanov: free
	if = { limit = { FROM = { has_country_flag = COLDWAR_SOV_seat } } add_to_temp_variable = { COLDWAR_SOV_cohesion_delta = -1 } }   # seat holders cost extra
	COLDWAR_SOV_change_union_cohesion = yes        # existing, l.296 (works from any scope)
}
```

### 2.6 Showing the allowed levels in advance

The levels are computed live by scripted triggers in republic scope. This needs no stored meter: only existing flags, ideas and the two per-plan counters.

```
COLDWAR_UNI_level1_allowed = { NOT = { SOV = { COLDWAR_UNI_khozraschet_rule = yes } } }
COLDWAR_UNI_level2_allowed = {
	COLDWAR_UNI_level1_allowed = yes
	NOT = { has_idea = COLDWAR_SOV_patron_in_moscow }                     # Patron: max level 1
	NOT = { has_country_flag = COLDWAR_UNI_level2_cooldown }              # 365-day flag
	NOT = { SOV = { has_country_flag = COLDWAR_SOV_local_barons has_country_flag = COLDWAR_SOV_gensec_bre } }   # Brezhnev's barons: max 1
}
COLDWAR_UNI_level3_allowed = {
	COLDWAR_UNI_level1_allowed = yes
	NOT = { has_idea = COLDWAR_SOV_patron_in_moscow }
	NOT = { has_country_flag = COLDWAR_SOV_cadre_protection }             # proposal type 3 blocks level 3
	NOT = { SOV = { has_country_flag = COLDWAR_SOV_local_barons has_country_flag = COLDWAR_SOV_gensec_bre } }
	NOT = { check_variable = { COLDWAR_UNI_cadre_plan = global.COLDWAR_SOV_plan } }    # once per plan and republic
	OR = {
		has_country_flag = COLDWAR_UNI_pripiski_exposed
		AND = { check_variable = { COLDWAR_UNI_fail_plan = global.COLDWAR_SOV_plan } check_variable = { COLDWAR_UNI_fail_count > 1 } }
		AND = { SOV = { has_country_flag = COLDWAR_SOV_discipline_campaign } has_country_flag = COLDWAR_SOV_pripiski }   # Andropov
	}
}
```

Scripted loc (`common/scripted_localisation/COLDWAR_UNI_1970_scripted_localisation.txt`), used in the mission description, the failure tooltip, the notice event 3 and judgement event 10:

```
defined_text = {
	name = COLDWAR_UNI_GetJudgementLevels
	text = { trigger = { SOV = { COLDWAR_UNI_khozraschet_rule = yes } } localization_key = COLDWAR_UNI_levels_none }   # "No judgement: Plan Shortfall only."
	text = { trigger = { COLDWAR_UNI_level3_allowed = yes } localization_key = COLDWAR_UNI_levels_3 }   # "Moscow may pardon, reprimand, requisition, levy, or put our First Secretary to a Politburo vote."
	text = { trigger = { COLDWAR_UNI_level2_allowed = yes } localization_key = COLDWAR_UNI_levels_2 }
	text = { trigger = { COLDWAR_UNI_level1_allowed = yes } localization_key = COLDWAR_UNI_levels_1 }
	text = { localization_key = COLDWAR_UNI_levels_0 }
}
```

- These triggers are cheap: flags, ideas and three variable comparisons.
- This matters because scripted loc in an open tooltip is re-evaluated continuously (performance diary, cited in `hoi4_shared_focus_mechanics.md` §6.10).

### 2.7 State inventory (rule of 15.10: statuses and plain counters only)

| Name | Kind | Scope | Lifetime |
|---|---|---|---|
| `COLDWAR_UNI_t_base`/`_t_base2`/`_t_base3`, `_d_base…` | baseline | republic | overwritten at each start |
| `COLDWAR_UNI_t_key`, `_d_key`, `_t_days`, `_d_days` | type and timer | republic | per mission |
| `COLDWAR_UNI_fail_plan` + `_fail_count` | counter | republic | reset when the plan number changes (the `pripiski_plan` pattern) |
| `COLDWAR_UNI_dir_plan` + `_dir_count` | counter | republic | same |
| `COLDWAR_UNI_cadre_plan` | plan stamp | republic | once per plan |
| `COLDWAR_UNI_req` | requisition size | republic | 60 days |
| `COLDWAR_UNI_target_active`, `_target_fulfilled`, `_target_failed`, `_directive_active`, `_t_reported`, `_t_stormed`, `_t_ai_done`, `_pripiski_exposed`, `_level2_cooldown` (365 days), `_cadre_target`, `_left_union`, `_tolkachi_used` (plan stamp) | flags | republic | as noted |
| `global.COLDWAR_UNI_fulfilled`, `_members`, `_years_fulfilled`, `_cadre_target` | globals | – | settlement and vote |
| `COLDWAR_UNI_union_requisition_civilian_factory_use` | modifier variable | SOV | sum of running requisitions |

### 2.8 Tools and pripiski (decisions in `COLDWAR_UNI_republic_plan_category`)

**Category settings:**
- `allowed = { COLDWAR_UNI_union_tag = yes NOT = { original_tag = SOV } }`. Static, for load order.
- `visible = { COLDWAR_SOV_is_union_republic = yes has_global_flag = COLDWAR_UNI_system }`.

**Decisions:**
- **Report Fulfilment** (pripiski).
  - Visible while `COLDWAR_UNI_target_active`.
  - Effect: `set_country_flag = COLDWAR_UNI_t_reported`, so the mission completes on the next check with its full reward. It also sets the existing `COLDWAR_SOV_pripiski` and `COLDWAR_SOV_pripiski_plan`, and `increase_corruption = yes` (as in `report_overfulfilment`, `cw_decisions.py:300`).
  - AI weight 0.
  - **Exposure** is a hook in `COLDWAR_SOV_investigate_republic` (effects l.1536; generator `cw_sys_effects.py:489`): in the proven branch, `if = { limit = { has_country_flag = COLDWAR_UNI_reported_false } COLDWAR_UNI_pripiski_exposed = yes }`. That effect:
    - removes the mission reward idea
    - clears `target_fulfilled`
    - `count_failure`
    - sets `pripiski_exposed`
    - sends `SOV = { country_event = COLDWAR_UNI.10 }`
  - **Settlement audit.** With `COLDWAR_UNI_peoples_control` or Andropov's flag, `COLDWAR_UNI_settle_year` rolls the same chance for each false reporter.
  - Refactor needed: split the chance calculation out of `investigate_republic` into `COLDWAR_SOV_investigation_chance` (temp `COLDWAR_SOV_chance`), so audits do not fire kompromat news 18.
- **Send the Tolkachi** (flag `tolkachi_unlocked`, once per plan).
  - Sets `COLDWAR_UNI_tolkachi_armed`.
  - The failure handler then re-arms instead of failing: `set_variable = { COLDWAR_UNI_t_days = 45 } activate_mission = <same mission>`. This is MD's re-activation in `timeout_effect`.
  - Proposed +45 days instead of +90 (timing, §8).
- **Storm the Plan.**
  - `set_country_flag = COLDWAR_UNI_t_stormed`, `add_stability = -0.03`, once per plan.
- **Adopt a Counter-Plan.**
  - Sets `COLDWAR_UNI_counter_plan`. The next annual target needs +2 instead of +1: at issue, store `COLDWAR_UNI_t_goal = t_base + 1` and test `check_variable = { industrial_complex_total > COLDWAR_UNI_t_goal }`. Success pays the reward idea `_plus` (×1.5).
- **Deliver to the Union Fund** (mission `deliver`):

```
set_temp_variable = { COLDWAR_SOV_gdp_share = 0.002 }
set_temp_variable = { COLDWAR_SOV_transfer_target = SOV.id }
COLDWAR_SOV_transfer_gdp_share = yes          # effects l.97: THIS pays a share of its GDP to the target (generic, not SOV-only)
set_country_flag = COLDWAR_UNI_delivered      # the mission's available
```

- **Send the Komsomol Brigades** (mission `komsomol`): `add_manpower = -5000`, `SOV = { add_manpower = 5000 }`, flag.

---

## 3. Measuring targets

### 3.1 MD's ready-made totals

MD computes per-country building totals in `update_state_variables` (`common/scripted_effects/00_money_system.txt:4663`):
- Each total sums `building_level@<building>` over `controlled_states_collection`.
- It is called by `ingame_update_setup` (l.220-222), which `on_weekly` runs **for every country** (`common/on_actions/MD_on_actions.txt:4-38`).
- So the SSRs have current totals with at most a 7-day lag.

| Target | Variable | Line in `00_money_system.txt` |
|---|---|---|
| Civilian factories | `industrial_complex_total` | 4719 |
| Military factories | `military_factory_total` | 4728 |
| Dockyards | `naval_factory_total` | 4737 |
| Agriculture districts | `agriculture_district_total` | 4701 |
| Offices | `office_park_total` | 4710 |
| Fossil power plants | `number_of_fossil_pps` | 4800 |
| Nuclear reactors | `nuclear_reactors` | 4755 |
| Renewable plants | `renewable_energy_infra` | 4746 |
| Refineries | `synthetic_refinery_total` | 4863 |
| Infrastructure | **no total.** State game variable `infrastructure_level` (`mdcw_imperia_infrastructure_effects.txt:29-30`, inside `every_owned_state`) | – |

Why these and not `num_of_civilian_factories`:
- `num_of_civilian_factories` and its siblings also work as variables (`00_productivity_effects.txt:122-125`, `00_money_system.txt:2710`).
- But they count factories gained from trade, and for a subject with `cic_to_overlord_factor = 0.25` they are not the number of buildings.
- **Use MD's `*_total` variables (real buildings).**

### 3.2 Compare patterns

```
# single building (baseline at start, comparison in available)  [OURS: var-vs-var check_variable]
check_variable = { industrial_complex_total > COLDWAR_UNI_t_base }

# power: three baselines, any one of them rising
set_variable = { COLDWAR_UNI_t_base = number_of_fossil_pps }
set_variable = { COLDWAR_UNI_t_base2 = nuclear_reactors }
set_variable = { COLDWAR_UNI_t_base3 = renewable_energy_infra }
# available:
OR = {
	check_variable = { number_of_fossil_pps > COLDWAR_UNI_t_base }
	check_variable = { nuclear_reactors > COLDWAR_UNI_t_base2 }
	check_variable = { renewable_energy_infra > COLDWAR_UNI_t_base3 }
}

# infrastructure +1 in any state: per-state baseline (state variables, MD-proven state scope)
every_owned_state = { set_variable = { COLDWAR_UNI_infra_base = infrastructure_level } }
# available:
any_owned_state = { has_variable = COLDWAR_UNI_infra_base check_variable = { infrastructure_level > COLDWAR_UNI_infra_base } }   # [TEST] state game var in check_variable

# infrastructure in two states (directive): counted monthly from on_monthly_SOV
# (playbook: country hooks, no world loops)
every_country = {
	limit = { has_country_flag = COLDWAR_UNI_infra_two_running }
	set_variable = { COLDWAR_UNI_infra_up = 0 }
	every_owned_state = {
		limit = { has_variable = COLDWAR_UNI_infra_base check_variable = { infrastructure_level > COLDWAR_UNI_infra_base } }
		add_to_variable = { PREV.COLDWAR_UNI_infra_up = 1 }   # MD pattern add_to_variable = { PREV.x = … }
	}
}
# available: check_variable = { COLDWAR_UNI_infra_up > 1 }

# corruption one level lower: snapshot as a number from corruption_level_01..10 (MD ideas, 00_budget_effects.txt:675/783)
if = { limit = { has_idea = corruption_level_01 } set_variable = { COLDWAR_UNI_d_base = 1 } } … (10 lines)
# available: COLDWAR_UNI_corruption_below_base = yes  (10 AND lines: has_idea = corruption_level_0N + check_variable = { COLDWAR_UNI_d_base > N })
```

Stability is checked at the deadline with `has_stability > 0.49`.

### 3.3 Pitfalls

1. **Weekly lag.** A finished building counts at the next weekly tick. That is fine for missions of 270-320 days.
2. **Controlled states.** Occupation lowers the totals, and liberation raises them. That is acceptable, and SSRs are rarely at war.
3. **Corruption.** The SSRs' 1970 block sets no laws (`md_coldwar_feasibility.md` §2.1). They may have **no corruption idea**, which makes mission 8 impossible.
   - [TEST] `has_idea = corruption_level_0X` on an SSR at start.
   - If false, drop mission 8 or make it a stability or PP task.
4. **AI floor.** It builds with MD helpers (`one_random_industrial_complex` and the others, `00_scripted_effects.txt:223-236`).
   - These charge 7.5 treasury **even when no state has a free slot**.
   - So guard with `any_controlled_state = { free_shared_building_slots = yes }`. Otherwise set the fallback flag `COLDWAR_UNI_t_ai_done`.
5. **Empty economies.** In 1970 the 14 SSRs have 10 civilian factories, 0 military factories and 2 dockyards in total (feasibility audit §2.3). "+1 building" targets are reachable but expensive for a small treasury; "+1 military factory" is a big ask for most of them. Keep targets small.

---

## 4. Punishments

### 4.1 Levels 1 and 2

**Level 2a, requisition.**
- Mechanism: a dynamic modifier on a variable, held for 60 days.
- MD uses `civilian_factory_use` in ideas and decisions:
  - `ideas/Iranian.txt:248`, `Polish.txt:2942`, `USA_1970_policy_decisions.txt:43`
  - **negative** in `ideas/05_china.txt:2123`: `CHI_pearls_economic_partner`, a bonus idea, where −1 means a factory is freed.
- **MD never puts it in a dynamic modifier**, and never uses `add_dynamic_modifier … days` [V/TEST].

```
COLDWAR_UNI_apply_requisition = {                              # republic scope (FROM of event 10); SOV = Moscow
	set_variable = { COLDWAR_UNI_req = industrial_complex_total }
	multiply_variable = { COLDWAR_UNI_req = 0.25 }
	round_variable = COLDWAR_UNI_req                           # UKR 6 -> 2 (1.5 rounds up); author may prefer floor (§8)
	clamp_variable = { var = COLDWAR_UNI_req min = 1 max = 50 }
	set_variable = { COLDWAR_UNI_requisition_civilian_factory_use = COLDWAR_UNI_req }
	add_dynamic_modifier = { modifier = COLDWAR_UNI_requisition days = 60 }     # [V/TEST]; fallback: delayed event + remove_dynamic_modifier
	force_update_dynamic_modifier = yes
	set_country_flag = { flag = COLDWAR_UNI_level2_cooldown days = 365 }
	SOV = {
		subtract_from_variable = { COLDWAR_UNI_union_requisition_civilian_factory_use = PREV.COLDWAR_UNI_req }   # negative = factories freed
		add_dynamic_modifier = { modifier = COLDWAR_UNI_union_requisition }      # permanent holder, value is the running sum
		force_update_dynamic_modifier = yes
		country_event = { id = COLDWAR_UNI.15 days = 60 }      # hidden; FROM = republic: add FROM.COLDWAR_UNI_req back, re-update
	}
	country_event = { id = COLDWAR_UNI.12 days = 1 }            # the republic is told; option "Comply" only
}
# dynamic modifiers (COLDWAR_UNI_1970_dynamic_modifiers.txt)
COLDWAR_UNI_requisition = { icon = GFX_idea_… civilian_factory_use = COLDWAR_UNI_requisition_civilian_factory_use }
COLDWAR_UNI_union_requisition = { icon = GFX_idea_… civilian_factory_use = COLDWAR_UNI_union_requisition_civilian_factory_use }
```

- A sum variable on SOV plus a delayed give-back event is needed because a dynamic modifier is unique per country. Several republics can be requisitioned at once.
- Reading `FROM.var` after 60 days is safe because of the 365-day cooldown.
- The `PREV.x`/`FROM.x` value pattern is MD-proven (`99_investment_scripted_effects.txt:654`).
- Note the overlap with the autonomy rule `cic_to_overlord_factor = 0.25`: Moscow already receives a quarter of every SSR factory.

**Level 2b, offices.**
- Dynamic modifier `COLDWAR_UNI_offices_taken` with fixed values: `offices_productivity = -0.25` and `office_park_income_tax_modifier = -0.2`, for 60 days.
- Both modifiers are MD's: `00_MD_dynamic_modifiers.txt:172`, `05_internal_factions_modifiers.txt:26`, and both are in the index `moddefs`.
- SOV gets the timed idea `COLDWAR_UNI_offices_requisitioned` (`tax_gain_multiplier_modifier = 0.01`) for 60 days.
- Available only with `office_park_total > 0`, so only 3 of 14 republics in 1970.

**Level 2c, levy.** `FROM = { set_temp_variable = { COLDWAR_SOV_gdp_share = 0.003 } set_temp_variable = { COLDWAR_SOV_transfer_target = SOV.id } COLDWAR_SOV_transfer_gdp_share = yes }`.
- The temp-variable target pattern is the one in `COLDWAR_SOV_monthly_aid` (effects l.110-116).
- The SSR treasury can go negative, which MD turns into debt. That is acceptable, or require `check_variable = { treasury > 0 }`.

**Level 1, reprimand.** −50 PP and the timed idea `COLDWAR_UNI_reprimanded` (`stability_factor = -0.02`) for 90 days.

### 4.2 Level 3: the cadre question (new vote type 5)

**Start, from option g of event 10:**

```
add_political_power = -50                                    # the other 50 only if the vote passes (author, §8)
FROM = { set_country_flag = COLDWAR_UNI_cadre_target set_variable = { COLDWAR_UNI_cadre_plan = global.COLDWAR_SOV_plan } }
set_variable = { global.COLDWAR_UNI_cadre_target = FROM.id }
set_temp_variable = { COLDWAR_SOV_vt = 5 }                   # new type
set_temp_variable = { COLDWAR_SOV_vl = 1 }                   # the Moscow block votes with the orthodox (bop > 0 = orthodox)
set_temp_variable = { COLDWAR_SOV_vu = 1 }                   # a Union question: republican votes x2 with Podgorny's federal union
set_temp_variable = { COLDWAR_SOV_vs = 0 }
COLDWAR_SOV_start_vote = yes                                 # effects l.1084: seat holders get ballot event 11, tally event 12 in 10 days
```

**Generator changes:**
- `cw_sys_effects.py`:
  - l.383: comment, add type 5.
  - Tally chain `res` (l.403-424): add a type-5 branch:

```
else_if = { limit = { check_variable = { global.COLDWAR_SOV_vote_type = 5 } }
	set_temp_variable = { COLDWAR_UNI_ct = global.COLDWAR_UNI_cadre_target }
	if = { limit = { has_global_flag = COLDWAR_SOV_vote_passed }
		add_political_power = -50
		set_temp_variable = { COLDWAR_SOV_cohesion_delta = -3 } COLDWAR_SOV_change_union_cohesion = yes
		add_power_balance_value = { id = COLDWAR_SOV_politburo_bop value = 0.05 tooltip_side = COLDWAR_SOV_politburo_bop_right_side }
		hidden_effect = { add_to_variable = { COLDWAR_SOV_bop = 0.05 } clamp_variable = { var = COLDWAR_SOV_bop min = -1 max = 1 } }
		var:COLDWAR_UNI_ct = { COLDWAR_UNI_replace_first_secretary = yes }
	}
	else = { var:COLDWAR_UNI_ct = { COLDWAR_UNI_apply_reprimand = yes } }    # fallback (author, §8)
	var:COLDWAR_UNI_ct = { clr_country_flag = COLDWAR_UNI_cadre_target }
}
```

  - The `var:` on a stored country id is the pattern already used by the type-4 branch (effects l.1393-1397).
- `cw_misc.scripted_loc_file`, l.286-306: add 14 entries to `GetVoteSubject` and to `GetLastVoteSubject`:

```python
for t in SSR:
    ent.append(([g(f"{ty} = 5"), f"{t} = {{ has_country_flag = COLDWAR_UNI_cadre_target }}"], f"{PFX}{kp}_cadre_{t}",
                f"the cadre question: replacing the First Secretary of the §Y{SSR_NAME[t]}§!"))
```

  - `GetVoteLean` needs nothing new: `vote_lean = 1` gives "vote with the orthodox".
- `cw_events.py` l.110 (ballot event 11). AI seat holders currently vote yes with weight 10.
  - On type 5, lower "in favour" (`modifier = { factor = 0.2 check_variable = { global.COLDWAR_SOV_vote_type = 5 } }`).
  - Make the target vote against (`factor = 100 has_country_flag = COLDWAR_UNI_cadre_target` on "against").
  - The `ai` field already accepts strings.
- **One vote at a time.** `COLDWAR_SOV_vote_running` is a single lane, and the queue (`COLDWAR_SOV_queue_resolution`) holds only type-1 subjects. Option g therefore requires no running vote.
  - Extending the queue to type 5 is possible later.

**The replacement** (republic scope):

```
COLDWAR_UNI_replace_first_secretary = {
	custom_effect_tooltip = COLDWAR_UNI_replace_tt
	hidden_effect = {
		retire_country_leader = yes
		if = { limit = { original_tag = UKR }
			create_country_leader = { name = "Volodymyr Shcherbytsky" picture = "gfx/leaders/UKR/shcherbytsky.dds" ideology = communist_state
			                          traits = { emerging_communist_state COLDWAR_UNI_moscows_man } }
		}
		else_if = { limit = { original_tag = KAZ }
			create_country_leader = { name = "Gennady Kolbin" ideology = communist_state traits = { emerging_communist_state COLDWAR_UNI_moscows_man } }   # no portrait: generic
		}
		# … one line per tag from the table in §4.3
	}
	set_country_flag = COLDWAR_UNI_moscows_man                  # kompromat immunity: investigate_republic sets chance 0 (like cadre_protection)
	add_timed_idea = { idea = COLDWAR_UNI_moscows_choice days = 180 }     # stability -10 %
	country_event = { id = COLDWAR_UNI.17 days = 1 }              # reaction (§4.4)
	news_event = { id = COLDWAR_UNI.18 hours = 6 }
}
```

- **Ideology and traits:**
  - The SSRs run `ideology = communist_state` with ruling party 4 (`IMP_1970_profile_communist_state`, history 1970 blocks).
  - MD's ideology trait for party 4 is `emerging_communist_state` (`00_leader_setup_scripted_effects.txt:219-224`, `set_correct_ideology_trait`).
  - Our own leader installs do the same: `COLDWAR_SOV_install_gensec_*`, effects l.408-425.
- **Do not call MD `set_leader`.** It (`00_leader_setup_scripted_effects.txt:9-41`) kills the leader and runs `set_leader_<TAG>`, MD's 2000-era rosters.
- New trait file: `common/country_leader/COLDWAR_UNI_1970_traits.txt` with `COLDWAR_UNI_moscows_man = { random = no political_power_factor = -0.10 }`.

### 4.3 Successor table (historical successors; portraits from `repo_paths.json`)

| Tag | Successor | Portrait |
|---|---|---|
| UKR | Volodymyr Shcherbytsky | `gfx/leaders/UKR/shcherbytsky.dds` |
| BLR | Tikhon Kiselyov | none |
| EST | Karl Vaino | `gfx/leaders/EST/vaino.dds` (check that it is Karl Vaino) |
| LAT | Boris Pugo | `gfx/leaders/LAT/pugo.dds` |
| LIT | Petras Griškevičius (loc without diacritics) | none |
| ARM | Karen Demirchyan | none. `ARM/stepan_demirchyan.dds` is his son: do not use it. |
| AZE | Kamran Baghirov | none |
| GEO | Eduard Shevardnadze | `gfx/leaders/GEO/eduard_shevardnadze.dds` (probably a later portrait) |
| KAZ | Gennady Kolbin (the historical "Moscow's man", 1986) | none |
| KYR | Absamat Masaliyev | none |
| TAJ | Rahmon Nabiyev | none |
| TRK | Saparmurat Niyazov | `gfx/leaders/TRK/Saparmurat_Niyazov.dds` (later portrait) |
| UZB | Inamzhon Usmankhodzhaev | none |
| MLV | Semion Grossu | none |

- A second replacement in the same republic, or a successor already in office, needs a generic name ("Second Secretary …"). That is an author decision.
- "None" means the picture is left out, so the game uses its generic portrait [TEST].

### 4.4 Reaction event (`COLDWAR_UNI.17`, republic)

- **a – Accept Moscow's Choice.** `country_event = { id = COLDWAR_UNI.19 days = 90 }` (hidden) swaps `COLDWAR_UNI_moscows_choice` (−10 %) for `COLDWAR_UNI_moscows_choice_eased` (−5 %, the remaining 90 days).
- **b – The Streets Answer.**
  - Cohesion −5 (`COLDWAR_SOV_change_union_cohesion`).
  - The Popular Front effect for free: `set_temp_variable` party 20 +5 %, using the same lines as decision `COLDWAR_SOV_popular_front` (`cw_decisions.py`, `E.party_pop(20, 0.05, 0.05)`).
  - A flag that waives that decision's cooldown.
  - The stability penalty stays.
  - Moscow gets news `COLDWAR_UNI.18`, variant "Unrest in …".
- **AI:** a 70/30 split, and 30/70 for KAZ, GEO and the Baltics (Jeltoqsan 1986, Tbilisi 1978).

### 4.5 Escalation, protection and General Secretary rules

| Concept rule | Implementation |
|---|---|
| Only after a failure, one judgement per failure | Event 10 is fired only from `COLDWAR_UNI_target_failure` and `COLDWAR_UNI_pripiski_exposed` |
| Level 2 at most once per 365 days | Flag `COLDWAR_UNI_level2_cooldown` with `days = 365` |
| Level 3 after 2 failures in a plan or exposed pripiski, Politburo vote, once per plan | `COLDWAR_UNI_level3_allowed` (§2.6), vote type 5 |
| Cadre protection blocks level 3 | `has_country_flag = COLDWAR_SOV_cadre_protection` (set by proposal type 3, effects l.1530; cleared at the congress, events l.2033) |
| Patron in Moscow: max level 1 | `has_idea = COLDWAR_SOV_patron_in_moscow` |
| Seat holder: extra cohesion −1 | `COLDWAR_UNI_moscow_punishment_cost` |
| Brezhnev's barons: max level 1 | SOV flag `COLDWAR_SOV_local_barons` (focus `COLDWAR_SOV_trust_the_local_barons`) **and** `COLDWAR_SOV_gensec_bre`. The flag is never cleared, so without the GS check it would bind every later leader. |
| Andropov: level 3 after one failure with pripiski | SOV `COLDWAR_SOV_discipline_campaign` (`COLDWAR_SOV_and_the_discipline_campaign`) + the republic's `COLDWAR_SOV_pripiski` |
| Romanov: level 2 costs no cohesion | SOV `COLDWAR_SOV_iron_discipline` (`COLDWAR_SOV_gro_iron_discipline`) |
| Gorbachev, khozraschet: no judgement, Plan Shortfall only | **No flag exists yet.** Proposal: `COLDWAR_UNI_khozraschet_rule = { has_country_flag = COLDWAR_SOV_gensec_gor has_completed_focus = COLDWAR_SOV_gor_the_state_enterprise_law }` (author, §8) |
| Absent SOV player → no punishment | Event 10 option a first + `timeout_days = 15` |
| AI Moscow judges by camp | `ai_chance` modifiers on `COLDWAR_SOV_gensec_<key>` (§2.5 table) |

---

## 5. Rewards and the yearly settlement

**Personal reward** (`COLDWAR_UNI_target_success`, republic scope; temp `COLDWAR_UNI_key`):

```
COLDWAR_UNI_target_success = {
	clr_country_flag = COLDWAR_UNI_target_active
	if = { limit = { has_country_flag = COLDWAR_UNI_t_reported } set_country_flag = COLDWAR_UNI_reported_false }
	set_country_flag = COLDWAR_UNI_target_fulfilled               # counted at the settlement (annual family only)
	if = { limit = { check_variable = { COLDWAR_UNI_key = 1 } }
		add_timed_idea = { idea = COLDWAR_UNI_reward_industry days = 180 }        # construction +5 %, PP +5 %
		SOV = { add_timed_idea = { idea = COLDWAR_UNI_sov_share_industry days = 180 } }   # refreshes, does not stack
	}
	else_if = { limit = { check_variable = { COLDWAR_UNI_key = 2 } } … }
	# … one branch per key (from the MISSIONS table); counter-plan / armaments variant: the _plus idea (x1.5)
}
```

- About 12 republic reward ideas plus 4-5 `_plus` variants, and 6 Moscow share ideas. Flat contributions (PP +15, PP +10, manpower) need no idea.
- **Note:** percentage rewards are weak for SSRs with almost no industry (feasibility audit §2.3). The values are the approved ones; this is a balancing note, not a blocker.

**Settlement in the January session**, before new targets are issued:

```
COLDWAR_UNI_settle_year = {                                       # SOV scope
	set_variable = { global.COLDWAR_UNI_fulfilled = 0 }
	set_variable = { global.COLDWAR_UNI_members = 0 }
	if = { limit = { OR = { has_country_flag = COLDWAR_UNI_peoples_control has_country_flag = COLDWAR_SOV_discipline_campaign } }
		every_country = { limit = { has_country_flag = COLDWAR_UNI_reported_false } COLDWAR_UNI_audit_report = yes }   # quiet roll, may expose
	}
	every_country = {
		limit = { COLDWAR_SOV_is_union_republic = yes }
		add_to_variable = { global.COLDWAR_UNI_members = 1 }
		if = { limit = { has_country_flag = COLDWAR_UNI_target_fulfilled } add_to_variable = { global.COLDWAR_UNI_fulfilled = 1 } }
		COLDWAR_UNI_copy_year_line = yes                              # last_ copies for the news, like the vote lines
	}
	set_temp_variable = { COLDWAR_UNI_share = global.COLDWAR_UNI_fulfilled }
	divide_temp_variable = { COLDWAR_UNI_share = global.COLDWAR_UNI_members }   # members >= 1 guaranteed by the limit above (guard anyway)
	if = {
		limit = { check_variable = { COLDWAR_UNI_share > 0.599 } }   # 9 of 14 (0.643); 8 of 14 = 0.571 fails; scales if republics leave
		every_country = { limit = { has_country_flag = COLDWAR_UNI_target_fulfilled } add_timed_idea = { idea = COLDWAR_UNI_plan_is_fulfilled days = 365 } }
		add_timed_idea = { idea = COLDWAR_UNI_plan_is_fulfilled days = 365 }        # stability +3 %, construction +5 %
		set_temp_variable = { COLDWAR_SOV_cohesion_delta = 2 } COLDWAR_SOV_change_union_cohesion = yes
		add_to_variable = { global.COLDWAR_UNI_years_fulfilled = 1 }
	}
	else_if = {
		limit = { check_variable = { COLDWAR_UNI_share < 0.35 } }    # below 5 of 14
		add_timed_idea = { idea = COLDWAR_SOV_plan_shortfall days = 365 }       # existing idea (tax -1 %)
	}
	news_event = { id = COLDWAR_UNI.30 hours = 6 }   # "The Plan Year [year]": [?global.COLDWAR_UNI_fulfilled] of [?global.COLDWAR_UNI_members], one line per republic ([UKR.COLDWAR_UNI_GetYearLine] …)
}
```

- **AI floor**, about 75 % (`COLDWAR_UNI_ai_floor_roll`, run when the target is issued to an AI republic):
  - `random_list = { 75 = { random_list = { 25 = { country_event = { id = COLDWAR_UNI.90 days = 120 } } 25 = { … days = 180 } 25 = { … 240 } 25 = { … 280 } } } 25 = { } }`. Fixed delays avoid relying on `random_days`.
  - Event 90 (hidden) builds the target building with the MD helper, **paid by the AI republic**, with the free-slot guard. For non-building keys, or when no slot is free, it sets `COLDWAR_UNI_t_ai_done`.
  - AI republics never report pripiski (weight 0).
- **Transferable Red Banner** (optional): the settlement picks the fulfiller with the most fulfilled missions in the plan, using a per-plan counter. That would be a third small counter (rule of 15.10). It is only built if the author wants it.

---

## 6. Integration into the generator

### 6.1 New module and files

**`sovgen/cw_union.py`** holds the tables (`MISSIONS`, `REWARDS`, `SUCCESSORS`, `UNION_FOCI`, regions) and the writers. Output files:

| Output | Content |
|---|---|
| `common/national_focus/COLDWAR_UNI_1970_union_joint.txt` | about 12 joint foci (MD focus style, `log` line in every reward) |
| `common/decisions/COLDWAR_UNI_1970_decisions.txt` + `categories/COLDWAR_UNI_1970_decision_categories.txt` | about 28 missions, the directive decision (2 variants), about 6 tool decisions, 2 categories |
| `events/COLDWAR_UNI_1970_events.txt` | namespace `COLDWAR_UNI`: 1-3 issue/notice, 10-19 judgement/consequences/reaction, 20-21 directive, 30 settlement news, 31 pripiski exposed, 90 AI floor |
| `common/scripted_effects/COLDWAR_UNI_1970_scripted_effects.txt` | issue, snapshot, success, failure, judgement levels, requisition, replacement, settlement, audit, AI floor |
| `common/scripted_triggers/COLDWAR_UNI_1970_scripted_triggers.txt` | membership, regions, `level1/2/3_allowed`, `khozraschet_rule`, `corruption_below_base` |
| `common/ideas/COLDWAR_UNI_1970_ideas.txt` | about 25 timed ideas (rewards, Moscow shares, reprimand, union buff, Moscow's choice) |
| `common/dynamic_modifiers/COLDWAR_UNI_1970_dynamic_modifiers.txt` | requisition (republic and SOV), offices |
| `common/scripted_localisation/COLDWAR_UNI_1970_scripted_localisation.txt` | judgement levels, regional mission names, directive target, year lines |
| `common/country_leader/COLDWAR_UNI_1970_traits.txt` | `COLDWAR_UNI_moscows_man` |
| `common/on_actions/COLDWAR_UNI_1970_on_actions.txt` | `on_subject_free` (leave flag + layout refresh) |
| `localisation/english/COLDWAR_UNI_1970_l_english.yml` | UTF-8 with BOM. Split from the shared `LOC` dict by key prefix `COLDWAR_UNI`/`COLDWAR_SOV_*_cadre_*`. About 400 keys. |

### 6.2 Hooks into existing modules

| File | Function / line | Change |
|---|---|---|
| `cw_events.py` | `SESSION` l.96-104 | Temp marker in the January branch; call `COLDWAR_UNI_january_session` after the plan-start ifs |
| `cw_events.py` | `ev(11, …)` l.110 | AI chance on vote type 5 |
| `cw_sys_effects.py` | votes l.383-424 | Vote type 5 (comment, tally branch) |
| `cw_sys_effects.py` | `COLDWAR_SOV_investigate_republic` l.489-505 | Split out the chance; immunity for `COLDWAR_UNI_moscows_man` and `_reserves` (−10); exposure hook |
| `cw_sys_effects.py` | `COLDWAR_SOV_start_plan` (l.516) | Nothing required: the counters reset by plan stamp. Optionally clear `COLDWAR_UNI_tolkachi_used` and similar flags here. |
| `cw_misc.py` | `scripted_loc_file` l.286-306 | Cadre-question subject lines |
| `cw_misc.py` | `ON_ACTIONS` l.240-264 | `on_monthly_SOV`: `COLDWAR_UNI_monthly = yes` (infrastructure-in-two-states counter) |
| `cw_focus.py` | `focus_file` l.224-233 | `shared_focus = COLDWAR_UNI_the_union_plan` + shortcut |
| `cw_layout.py` / `cw_focus._continuous_pocket` | l.210-221 | Reserve `UNION_BOX` |
| `cw_decisions.py` | `dec`/`cat`/`tt`/`ttrig` l.15-60 | Add a `pfx=PFX` parameter so `cw_union` can reuse them |
| `cw_build.py` | `FILES` l.106-125, `loc_file` l.93 | New outputs, a second yml, and optionally the generic-tree patch |
| gentools `generate_1970_generic_focus_tree.py` | l.346-356 | One `shared_focus` line (§1.2) |

### 6.3 IDs and prefix

- **Recommendation: `COLDWAR_UNI_`** for every new ID, flag, variable, idea, modifier, loc key and file, and the namespace `COLDWAR_UNI`.
- The existing `COLDWAR_SOV_` effects (cohesion, money, votes, investigate) and statuses (seat, patron, cadre protection, pripiski) are reused unchanged.
- Reasons:
  - The joint IDs live in 15 countries' trees and saves; they are not Soviet-only.
  - It gives a clean event namespace: SOV uses 1-147 and 900/901.
  - It keeps a separate loc file.
  - The module can later move into its own generator.
- Cost: the validator regexes must accept both prefixes (§6.4).

### 6.4 Validator extensions (`validate_sov.py`)

1. Widen the patterns:
   - `OWN`: also `"COLDWAR_UNI" in p`.
   - The ID, flag, variable, event and effect regexes: `COLDWAR_(?:SOV|UNI)_`.
   - Events: `COLDWAR_(?:SOV|UNI)\.\d+`.
   - Second yml.
   - Marker whitelist: `common/national_focus/mdcw_1970_generic_focus.txt` if it is patched.
   - `KNOWN_VAN` += `civilian_factory_use`.
2. Joint rules (§1.4):
   - every `joint_focus` has `joint_trigger`
   - no `mutually_exclusive`
   - no negative or global or fixed-tag effects in `completion_reward`/`_joint_member`
   - `select_effect` and in-progress flag present
   - `relative_position_id` and prerequisites stay inside the union file
3. Attachment:
   - the root ID appears as `shared_focus =` in the SOV output **and** in the generic tree (`MOD` copy or `out/` patch)
   - every `shared_focus =` line points to a defined root (crash guard)
4. Layout: no union focus inside the SOV `POS` or the continuous-panel box, and the generic offset position is right of x 226.
5. Missions:
   - every `COLDWAR_UNI_target_*`/`directive_*` has `days_mission_timeout`, `timeout_effect`, `complete_effect` and `allowed = { always = no }`
   - every `activate_mission = X` points to a defined mission
   - every mission key in `MISSIONS` has a reward branch and loc
6. Judgement:
   - event 10 has `timeout_days = 15`
   - option a has no trigger
   - every punishing option calls `COLDWAR_UNI_moscow_punishment_cost`
7. Vote type 5 has a tally branch and 14×2 scripted-loc entries.
8. Leader table: every portrait path exists in `repo_paths.json`, and every trait is defined.

### 6.5 Effort estimate (generator work, in hours)

| Part | Content | Hours |
|---|---|---|
| 0 | First in-game smoke test of SOV 1970 (vote engine, event 10, decisions); prerequisite | 3-4 |
| 1 | Joint skeleton (about 12 foci, icons, loc, descriptions), attachment in both trees, offsets, layout box | 8-10 |
| 2 | Missions from the table (about 28), issue logic and timing, regional names, directives (decision + event), AI floor | 12-16 |
| 3 | Measuring (snapshots, triggers, infrastructure loop, corruption) | 3-4 |
| 4 | Judgement event, levels 0-2c, consequence events, dynamic modifiers, cooldowns, scripted loc | 6-8 |
| 5 | Vote type 5, replacement, successor table, reaction, investigate refactor | 5-7 |
| 6 | Rewards, Moscow shares, settlement, news, union buff, shortfall | 5-6 |
| 7 | Tools (Tolkachi, Storming, Counter-Plan, Deliveries, Komsomol), pripiski exposure and audit | 4-5 |
| 8 | Validator extensions | 4-5 |
| 9 | In-game test rounds (3), fixes | 10-15 |
| | **Total** | **about 60-80 h (8-10 working days)** |

---

## 7. Risks and in-game test checklist

### 7.1 Main risks

1. **Untested base.**
   - The SOV 1970 system the missions build on has not run in game yet: vote engine, session event, decision categories, money helpers.
   - An error there breaks the whole mission loop.
   - Mitigation: part 0 first.
2. **Joint focus behaviour in our setup:**
   - members' running foci
   - the parallel-research lock
   - completion for members whose tree is the shared generic tree
   - leavers and late joiners
   - `allow_branch` load order (subject relations)
   - FROM in member rewards

   Fallback: turn the branch into `shared_focus` with GCC-style "one completes for all" `bypass` flags (`gulf_shared.txt:55-61`). Rewards then go through flags; the content stays the same.
3. **Two generators, one crash.**
   - A `shared_focus` line without the union file, or the reverse, crashes at the main menu.
   - The generic tree is generated elsewhere.
   - Mitigation: one atomic deploy, plus the validator check in both directions.
4. **Unproven modifier mechanics in punishments:**
   - `civilian_factory_use` in a *dynamic* modifier with a variable
   - negative values for Moscow
   - rounding
   - `add_dynamic_modifier … days`
   - the interplay with MD's factory-based economy and with `cic_to_overlord_factor`

   On top of that, the SSRs' empty economies make targets and punishments either toothless (offices: 11 of 14 have none) or harsh (UKR loses 2 of 6 factories).
5. **MP load and AI behaviour:**
   - Up to 14 judgements per year land on a human Moscow; the deadlines are staggered over 3 weeks, but the load stays.
   - The single-lane Politburo vote collides with resolutions.
   - AI seat holders vote yes on cadre questions unless reweighted.
   - The AI floor makes AI-heavy games reach 9 of 14 almost every year.
   - The General Secretary flags (`local_barons`) persist after the leader changes.

### 7.2 What cannot be checked statically (test checklist)

Start in 1970 with `-debug`. Add a hidden debug category (`visible = { is_debug = yes }`) with:
- activate a 5-day `COLDWAR_UNI_target_civ` on UKR
- build one civilian factory on UKR (MD helper)
- force the settlement
- start a cadre vote on KAZ

**A. Joint tree**
1. The branch is visible for SOV at (336, 8) and for all 14 SSRs at (232, 0). It is hidden for a non-SSR generic-tree country such as FIN. It does not overlap the continuous panel, and the shortcut works.
2. UKR completes a republic focus. It completes for SOV and the 13 other SSRs, with one `log` line per member in `game.log`. Originator and member blocks are correct.
3. KAZ is researching a generic focus at that moment. Its focus continues unchanged.
4. While UKR researches focus X, KAZ cannot select X. The AI never picks a focus with the in-progress flag.
5. A Moscow-only focus cannot be selected by an SSR. The `JOINT_SOV` title bar renders.
6. Release UKR (`end_puppet`). It receives no further completions and the branch disappears after the layout refresh. Re-puppet it and check the catch-up.

**B. Missions**

7. `activate_mission` with `allowed = { always = no }` shows the mission with a countdown, using the variable days.
8. The goal tooltip shows `[?industrial_complex_total]` and `[?COLDWAR_UNI_t_base]`. The regional name resolves (scripted loc in the mission title).
9. Building a factory completes the mission within 7 days (weekly MD tick).
10. Timeout fires `COLDWAR_UNI.10` to SOV with FROM = UKR. Options are hidden per trigger. No answer → option a after 15 days.
11. The Tolkachi re-activation inside `timeout_effect` works with the new variable timer.
12. Save and load mid-mission: the mission, its timer and the baselines survive.
13. The SSRs have a corruption idea in 1970 (needed for mission 8).

**C. Punishments**

14. Requisition: UKR's free civilian factories drop by n and Moscow's rise by n. Both return after 60 days with no residual modifier. Two republics requisitioned at once sum up correctly.
15. The offices modifiers show and apply. The levy moves treasury (check UKR's MD budget screen).
16. Cadre vote: ballot event 11 names the republic, the AI votes as weighted, the tally runs the type-5 branch, and the leader, trait and portrait appear. MD's leader failsafe does not overwrite them. The reaction event works, and the stability idea halves after 90 days.
17. The AI Moscow judgement distribution under Brezhnev and under Andropov (observe mode).

**D. Settlement**

18. The hook runs once per January and not in extra sessions.
19. Counts, news lines, the union buff for fulfillers and SOV, and the shortfall below 35 %. The threshold scales after one republic leaves.
20. The AI floor gives about 75 % fulfilment over 3 observed years. The building is paid, and no treasury is charged without a slot.

**E. Technical**

21. `error.log` is clean.
22. No lag with two missions and the judgement-level tooltip open.
23. A 2-player MP session (SOV + UKR) runs without desync: random rolls in effects, joint completion and judgement.

---

## 8. Decisions the author must still make

1. **Timing.** Annual target 300-321 days and Tolkachi +45 days, so everything is settled by 1 January. The concept had 365 and +90, which overlaps the next issue.
2. **Membership opt-out.** Does a Declaration of Sovereignty end union-tree membership (no more joint completions)?
3. **Failed cadre vote.** Fall back to a reprimand automatically? Is the cost split 50 PP at the proposal and 50 PP on success? Does the targeted republic vote on its own case?
4. **Successors.** The historical successors with the portraits listed, or a generic "Moscow's man"? What happens on a second replacement?
5. **Gorbachev rule trigger.** Suggestion: `COLDWAR_SOV_gor_the_state_enterprise_law` completed while Gorbachev is General Secretary.
6. **Smaller points:**
   - Requisition rounding: UKR 6 → 2, or floor → 1.
   - Keep offices (level 2b) although only 3 republics have offices?
   - Keep the old plan-level `report_overfulfilment` next to the per-mission "Report Fulfilment", or merge them?
   - Drop mission 8 if SSRs have no corruption idea?
   - Does the AI floor build real (paid) buildings, or only flags?
   - Red Banner: yes or no?
7. **Generic generator.** Add the one `shared_focus` line there (recommended), or patch it from `cw_build`?
8. **MP rule.** Adopt the concept's §10 exception sentence.
