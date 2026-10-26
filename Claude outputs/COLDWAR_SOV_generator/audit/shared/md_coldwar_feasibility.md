# Shared Union focus tree (SOV + 14 SSRs): feasibility in mdcoldwar

Audit 17.10.2026, read-only. Sources: local mod copy `/mnt/user-data/uploads/mdcoldwar/` (plus files staged from the device today: descriptor, changelog, all 14 SSR histories, the four MD joint/shared files that were missing, 85 SSR state files, Cold War triggers/effects, MD helpers), repo index `/home/claude/egygen/repo_paths.json`, generator `/home/claude/sovgen/` and its output `out/`, hooks audit `/home/claude/audit/imperia_coldwar_hooks.md`, project docs (`mdcw_coding_playbook.md`, `mdcw_sov_1970_implementation.md`, `mdcw_1970_generic_focus_tree.md`).
Paths below are relative to the mod root unless they start with `/home/claude` or `out/` (= `/home/claude/sovgen/out/`).

## Verdict

| Question | Answer |
| --- | --- |
| Can SOV and the 14 SSRs share one focus tree? | **Yes.** The engine (HOI4 1.19, MD 2.0.2) supports both `shared_focus` and `joint_focus`. MD uses them in 12 files, including a mixed joint and shared tree for CZE/SLO that is the closest template. |
| Can it hook into the Five-Year Plans, cohesion, Politburo and Comecon without new parallel systems? | **Yes.** Every hook exists as a callable effect or a readable variable: `global.COLDWAR_SOV_plan`, `COLDWAR_SOV_change_union_cohesion`, `COLDWAR_SOV_start_vote`, `COLDWAR_SOV_build_union_project`, `COLDWAR_SOV_execute_proposal`, the GDP money helpers and the `mdcw_cw_bp_2` flag. |
| MP rule (offers only)? | **Yes, with a design rule.** Shared foci are individual and safe. Joint foci complete for other members automatically, so they need an opt-in `joint_trigger` and must never be mutually exclusive or carry costs for the member. |
| Biggest blockers | (1) Where the SSRs host the tree: they run `mdcw_1970_generic_focus`, which comes from another generator. (2) SSR economies are almost empty in 1970: 10 civilian factories and 0 military factories across 85 states. (3) `allow_branch` and `offset` are only re-evaluated on load or on `mark_focus_tree_layout_dirty`. |

---

## 1. How MD implements shared trees

### 1.1 Two block types and the inventory

`shared_focus = { … }` is a focus that several trees include. Each country researches it on its own, with its own focus time.
`joint_focus = { … }` works like a shared focus with one difference. When one country completes it, the engine also completes it for every other country whose tree contains it and that passes `joint_trigger`. Joint foci have extra reward blocks:

- `completion_reward_joint_originator`: only the country that researched the focus.
- `completion_reward_joint_member`: only the countries that got the completion through the joint mechanic.
- `completion_reward`: everyone.

Both block types sit at file top level in `common/national_focus/`. A tree attaches the root with `shared_focus = <root id>`, and every focus chained to the root comes with it. That line attaches joint roots too: `05_russia.txt:12` attaches the joint root `CHI_SOV_treaty_good_neighbourliness` this way.

| File | shared | joint | Root gate (`allow_branch`, root only) | Typical cost |
| --- | --- | --- | --- | --- |
| 01_EU_USoE_shared.txt | 90 | 0 | `original_tag` list + `global.EU_passed_votes` (l.176-283) | 10 (root 26) |
| 02_EU_POTEF_shared.txt | 74 | 0 | yes | 10 |
| Commonwealth_shared.txt | 23 | 0 | `has_idea = commonwealth_of_nations_member` (l.5-7) | 18 |
| gulf_shared.txt | 21 | 0 | `original_tag` list (l.30-44) | 10 / 7.9 / 14.35 |
| 06_AfricanUnion_shared.txt | 39 | 0 | `has_country_flag = african_nation_flag` (l.69) | 10 (root 1) |
| 03_shared_korea_unified.txt | 86 | 0 | per branch (24×) | 5 / 10 |
| 06_czehcoslavakia_shared.txt | 33 | 26 | `original_tag = CZE/SLO` (l.17-22) | 5 |
| 03_benelux_shared.txt | 0 | 33 | `is_benelux_country = yes` (l.15) | 8 / 10 |
| 06_MERCOSUR_shared.txt | 0 | 22 | `is_in_array = { global.mercosur_potential = THIS }` (l.25) | 7 |
| 03_china_russia_joint.txt | 0 | 29 | `original_tag = CHI/SOV` (l.19-24) | 10 |
| 03_china_north_korea_joint.txt | 0 | 59 | yes | 10 / 7 |
| 03_joint_korea_confederation.txt | 0 | 28 | none (gated by `available`) | 10 |

No `is_joint` trigger appears anywhere in the staged mod. Joint behaviour comes only from the `joint_focus` block type and `joint_trigger`.

### 1.2 Attachment and position

- Attachment lines: `00_generic.txt:2-31` attaches 9 roots (Commonwealth, GCC, USoE, POTEF, Gagauzia, AU, CZE_SLO, Sahrawi, MERCOSUR, Benelux). Others: `05_russia.txt:10-12`, `05_ukraine.txt:7-8`, `05_belarus.txt:15091-15092`, `uk_1985.txt:11`, `gulf.txt:12588`.
- **`mdcw_1970_generic_focus.txt`, the tree all 14 SSRs run, has no `shared_focus` lines.** `COLDWAR_SOV_1970_focus` has none either (header written by `/home/claude/sovgen/cw_focus.py:226-230`).
- Position: the root has absolute `x/y`. Each host tree moves it with `offset = { x y trigger }`, and every child uses `relative_position_id`. Older files trigger the offset on the tag (`01_EU_USoE_shared.txt:8-172`, 31 offsets). Newer files trigger it on the host tree, which suits us better:

```
offset = { x = 14 y = 19 trigger = { has_focus_tree = LBA_1970_focus } }   # 06_AfricanUnion_shared.txt:2-8
offset = { x = 20 y = 0  trigger = { has_focus_tree = united_kingdom_focus } }   # Commonwealth_shared.txt:17-21
```

- Free space: the SOV tree spans about x -85…422 (836 foci, continuous focus at x = 31200 px). The generic tree spans x 0…226, y 0…7 (continuous focus at y = 1250 px). A Union tree fits at x ≥ 430 (SOV) and x ≥ 230 or y ≥ 12 (generic).
- MD never links a shared focus to a country focus through `prerequisite` or `relative_position_id`. Country-specific gating goes into `available`, for example `has_completed_focus = …` or a flag.

### 1.3 Gating members

- **`allow_branch` only on the root** hides the whole group for non-members (1 per file, table above). The engine evaluates it, and `offset` triggers, at load and when `mark_focus_tree_layout_dirty = yes` runs. MD wraps that call in `update_focus_tree_obsolete_branches` (`common/scripted_effects/00_focus_utilities.txt:5-17`), but the wrapper only fires under game rule `obsolete_focus_branches_visibility = HIDE`.
- **`available`** carries the live membership test: `has_country_flag = USoE`, `has_idea = commonwealth_of_nations_member`, `has_dynamic_modifier = mercosur_member_state_modifier` + `is_subject = no` (MERCOSUR l.29-34), or scripted triggers (`CHI_SOV_joint_focus_available`, `benelux_cooperation_trigger`).
- **Subject status** is never the gate in MD. For us the natural gate is the existing trigger `COLDWAR_SOV_is_union_republic` (`out/common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt:6`, `is_subject_of = SOV` + SSR tag list).
- **Shared progress:** GCC bypasses a focus once any member completed it: `bypass = { custom_trigger_tooltip = { tooltip = gcc_focus_completed_tt has_global_flag = GCC_the_gcc_completed } has_idea = idea_gcc_member_state }` (`gulf_shared.txt:55-61`). The AU root is never taken by hand (`available = { always = no }`, `06_AfricanUnion_shared.txt:73-78`); script grants it.

### 1.4 How effects reach other members (five MD patterns)

1. **Joint completion (engine):** `completion_reward_joint_member` runs in each member. For example Benelux gives the originator +150 PP and members +50 PP (`03_benelux_shared.txt:31-36`). CHI-SOV member rewards add opinion (`03_china_russia_joint.txt:156-161`).
2. **Joint completion that sends an offer (MP-safe):** CZE_SLO_stop_border_controls has `completion_reward_joint_member = { country_event = CZE_SLO_event.1 custom_effect_tooltip = CZE_SLO_guarantee_if_accept }` (`06_czehcoslavakia_shared.txt:289-292`). The member decides.
3. **Originator loops over members:** Commonwealth applies a global effect once, through a global flag plus `every_country = { limit = { has_idea = commonwealth_of_nations_member } … }` (`common/scripted_effects/99_Commonwealth_scripted_effects.txt:131-140`). It also marks the focus done for the others: `every_other_country = { limit = { … } unlock_national_focus = COMMONWEALTH_shared_focus }` (l.887-895; unlock completes the focus without running its reward). AU does the same over a global array: `for_each_scope_loop = { array = global.AU_member … unlock_national_focus = … }` (`06_AfricanUnion_shared.txt:128-141`). Benelux's originator fires events to the other members with `every_other_country` (`03_benelux_shared.txt`).
4. **Reservation, so two members do not research the same focus:** `select_effect = { set_global_flag = AU_create_investment_bank_reserved }` plus `available = { NOT = { has_global_flag = …_reserved } }`, cleared again in the reward (`06_AfricanUnion_shared.txt:108, 116, 144-148`). The originator pays 10 % of GDP and members get half the modifier.
5. **AI de-duplication for joint foci:** `select_effect = { set_global_flag = BRA_americas_unity_in_progress }` plus `ai_will_do = { modifier = { add = -1000 has_global_flag = …_in_progress } }` (`06_MERCOSUR_shared.txt:74-85`). This implies the engine does not stop several members from researching the same joint focus in parallel.

MD also uses mutually exclusive joint foci (CHI_NKO 12, CZE_SLO 6, MERCOSUR 2). There, one country's pick locks the alternative for its partner.

### 1.5 Costs, AI, localisation, filters, title bar

- **Costs:** a flat 5-18 per file (table). Our SOV tree uses 1/3/5/7/10.
- **AI:** `ai_will_do = { base = N }` with `factor = 0` guards (debt, bankruptcy, membership). Examples: AU base 200, Commonwealth 20, GCC 10, CHI_SOV 8 with a date factor, MERCOSUR 25 with the -1000 in-progress rule.
- **Localisation:** one yml per shared tree (`MD_focus_GCC_l_english.yml`, `Commonwealth_l_english.yml`, `MD_focus_African_Union_l_english.yml`), keys `<id>` / `<id>_desc`, and `_tt` keys for "all members count this as completed" (`Commonwealth_l_english.yml:49`). UTF-8 with BOM.
- **search_filters:** existing tags (`FOCUS_FILTER_POLITICAL/ECONOMY/INDUSTRY/DIPLOMACY/EUROPEAN_UNION/KOREAN_PENINSULA/MERCOSUR …`). A new tag needs a loc key (see `localisation/english/replace/replaced_from_focus_filter_tag_l_english.yml`) and a sprite `GFX_<TAG>` (`interface/MD_focus_filters.gfx`). The SOV tree uses only existing filters (INTERNAL_FACTION, POLITICAL, STABILITY, INFLUENCE, MILITARY_LAWS, INDUSTRY, RESEARCH, EXPENDITURE, WAR_SUPPORT, CORRUPTION).
- **Title bar:** joint foci set `text_icon = <style>`. A red Soviet style exists: `JOINT_SOV_focus_style` (`common/national_focus/00_titlebar_styles.txt:263-269`; dds files in `gfx/interface/focusview/titlebar/focus_*_joint_SOV_bg.dds`). Styles are `style = {}` blocks in the national_focus folder, so a `COLDWAR_` style file is possible.
- **Inlay window:** a focus tree can show a scripted GUI panel (`common/focus_inlay_windows/documentation.md`: `inlay_window = { id position }`, scripted images and buttons). This is an option for showing the plan number and Union cohesion on the shared tree. It needs a .gui file.

### 1.6 MD helpers we can reuse

| Helper | Where | Use |
| --- | --- | --- |
| `modify_treasury_effect` (`treasury_change`), `modify_debt_effect` (`debt_change`), `modify_international_investment_effect` | `common/scripted_effects/00_budget_effects.txt:1487, 1499, 1530` | Prices and payments |
| `one_random_industrial_complex` / `_arms_factory` / `_infrastructure` / `_fossil_fuel_powerplant` / `_agriculture_district`, `one_state_industrial_complex` | `00_scripted_effects.txt:223, 4, 442, 1899, 2070, 239` | Build in THIS country's controlled states. Each charges 7.5 treasury unless `skip_payment = 1`. |
| `change_relative_party_popularity` (`party_index`, `party_popularity_increase`, `temp_outlook_increase`) | MD politics | National party (index 20) for the sovereignty path, as `COLDWAR_SOV_popular_front` already does |
| `change_<faction>_opinion` (`temp_opinion`) | `00_internal_faction_effects.txt:1031-1480` | Only works if the country has the faction idea (see §2) |
| `mark_focus_tree_layout_dirty`, `update_focus_tree_obsolete_branches` | engine / `00_focus_utilities.txt:5` | Refresh `allow_branch` after a republic leaves or joins |
| `unlock_national_focus`, `for_each_scope_loop = { array = … }`, `every_other_country` | patterns above | Shared progress |

---

## 2. The SSRs in 1970

### 2.1 Setup (history, verified in all 14 files)

| Tag | Capital | Tree | Profile | Leader (expire) | Productivity |
| --- | --- | --- | --- | --- | --- |
| UKR | 698 | mdcw_1970_generic_focus | communist_state | Petro Shelest (1972.5.25) | 361.9 |
| BLR | 703 | " | " | Pyotr Masherov (1980.10.4) | 357.2 |
| EST | 105 | " | " | Johannes Kabin (1978.7.26) | 441.8 |
| LAT | 107 | " | " | Augusts Voss (1984.4.14) | 423.0 |
| LIT | 110 | " | " | Antanas Snieckus (1974.1.22) | 404.2 |
| ARM | 709 | " | " | Anton Kochinyan (1974.11.27) | 329.0 |
| AZE | 713 | " | " | Heydar Aliyev (1982.12.3) | 310.2 |
| GEO | 707 | " | " | Vasil Mzhavanadze (1972.9.29) | 338.4 |
| KAZ | 716 | " | " | Dinmukhamed Kunaev (1986.12.16) | 357.2 |
| KYR | 720 | " | " | Turdakun Usubaliyev (1985.11.2) | 282.0 |
| TAJ | 724 | " | " | Jabbor Rasulov (1982.4.4) | 244.4 |
| TRK | 729 | " | " | Muhammetnazar Gapurov (1985.12.21) | 300.8 |
| UZB | 725 | " | " | Sharof Rashidov (1983.10.31) | 282.0 |
| MLV | 147 | " | " | Ivan Bodiul (1980.12.22) | 183.35 |

Every 1970 block has the same shape (for example `history/countries/UKR - Ukraine.txt:15-35`):

```
mdcw_apply_1970_infantry_research = yes
load_focus_tree = mdcw_1970_generic_focus
set_variable = { gdp_per_capita = 1.429 }
IMP_1970_profile_communist_state = yes
set_cosmetic_tag = <TAG>_Coldwar_Communism
create_country_leader = { … expire = "…" ideology = communist_state }
set_oob = "mdcw_1970_empty_land"   # plus empty naval and air OOBs ("temporary user decision")
```

- **Politics:** `IMP_1970_profile_communist_state` (`common/scripted_effects/IMP_1970_world_politics_effects.txt:95-110`) sets communism 90 %, party 4 (communist_state) at 0.78, ruling party 4, no elections. There are also small shares for parties 1, 5, 7, 13, 19 and 22.
- **Laws and interest groups:** none are set in the 1970 block. Laws and factions only appear in the 2000 blocks. In-game, faction helpers (`change_communist_cadres_opinion`) are therefore probably no-ops for SSRs. Our `COLDWAR_SOV_change_<f>_opinion_exact` wrappers already check `has_idea` first.
- **Playable:** yes. They are ordinary tags and selectable through the "---" (minor) entry of the 1970 bookmark (`common/bookmarks/blitzkrieg.txt`, `COLD_WAR_1970`).
- **No AI exclusion:** `mdcw_load_1970_fallback_tree` (`common/scripted_effects/mdcw_1970_focus_tree_effects.txt:4-30`) excludes only USA/SPR/LBA/EGY/SOV/CYP/ISR/GRE. Without an exclusion, an SSR given its own tree would get the generic tree reloaded by any old event that calls this effect.

### 2.2 Subject type

All 14 are set in `history/countries/SOV - Russia.txt:22-36` (generated copy `out/history/countries/SOV - Russia.txt`) as `set_autonomy = { target = X autonomy_state = autonomy_soviet_republic_1985 }`, behind the overlord flag `SOV_1985_soviet_republic_autonomies_enabled`. Definition (`common/autonomous_states/99_1985_soviet_republic_autonomies.txt`):

```
is_puppet = no   use_overlord_color = yes   min_freedom_level = 0.0   manpower_influence = 0.2
rule = { can_not_declare_war = yes can_decline_call_to_war = no units_deployed_to_overlord = yes can_send_volunteers = no }
modifier = { cic_to_overlord_factor = 0.25 mic_to_overlord_factor = 0.25 can_master_build_for_us = 1 autonomy_manpower_share = 0.2
             extra_trade_to_overlord_factor = 0.6 overlord_trade_cost_factor = -0.6 research_sharing_per_country_bonus_factor = -0.4
             autonomy_gain_global_factor = -0.4 }
can_take_level = { always = no }   can_lose_level = { always = no }
```

It is a single level with no neighbouring level, so `add_autonomy_ratio` and `add_autonomy_score` move the bar but never change status. The SSRs are not in the Warsaw Pact faction; only DDR, POL, CZE, HUN, ROM and BUL are added. As subjects they cannot refuse SOV's calls to war.

### 2.3 Economy (parse of 85 state files: base block + `1970.1.1` overrides)

| Tag | States | Civ | Mil | Dock | Infra | Offices | Agri |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UKR | 29 | 6 | 0 | 2 | 46 | 6 | 5 |
| BLR | 6 | 0 | 0 | 0 | 9 | 1 | 0 |
| EST | 4 | 0 | 0 | 0 | 10 | 0 | 0 |
| LAT | 4 | 1 | 0 | 0 | 8 | 0 | 0 |
| LIT | 4 | 1 | 0 | 0 | 10 | 0 | 0 |
| ARM | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| AZE | 8 | 0 | 0 | 0 | 10 | 0 | 0 |
| GEO | 6 | 1 | 0 | 0 | 6 | 0 | 0 |
| KAZ | 6 | 1 | 0 | 0 | 11 | 1 | 1 |
| KYR | 3 | 0 | 0 | 0 | 1 | 0 | 0 |
| TAJ | 3 | 0 | 0 | 0 | 2 | 0 | 2 |
| TRK | 2 | 0 | 0 | 0 | 4 | 0 | 0 |
| UZB | 3 | 0 | 0 | 0 | 3 | 0 | 2 |
| MLV | 4 | 0 | 0 | 0 | 4 | 0 | 0 |
| **Total** | **85** | **10** | **0** | **2** | 127 | 8 | 10 |

- Fossil power plants are 0 in every 1970 block. `IMP_1970_fossil_starting_capacity` rebuilds them at startup ("historical demand helper"; file not staged).
- Special-project facilities survive from the base block: Kyiv (air, land, nuclear), Kharkiv (land, nuclear), Lviv (nuclear), Dnipropetrovsk (air), Zaporizhzhia (air), Mykolaiv (naval), Minsk (land).
- The parse script is at `/tmp/claude-0/-home-claude/eb6e4907-0276-5c02-abcf-5cee86bec5c0/scratchpad/ssr_states.py`. States were selected by name, so a few SSR-owned states could be missing.

Consequence: percentage modifiers to industry are close to worthless for republics. Content has to build things, through Union projects or MD helpers. A quarter of every SSR factory also flows to SOV (`cic_to_overlord_factor`).

### 2.4 Cold War system status

- On setup, a subject copies its overlord's bloc (`common/scripted_effects/mdcw_cold_war_effects.txt:47-61`), so the SSRs sit in bloc 2 (Soviet).
- They cannot change alignment: `mdcw_cw_can_change_alignment` requires `is_subject = no` (`common/scripted_triggers/mdcw_cold_war_triggers.txt:150-166`).
- They always fit their bloc (`mdcw_cw_fits_own_bloc`, `is_subject = yes`, l.130-148).
- They follow SOV on any bloc change ("Subjects follow their overlord", `mdcw_cold_war_effects.txt:3719`).
- As bloc-2 members they get the Soviet bloc profile and, while Comecon runs (`has_global_flag = mdcw_cw_bp_2`), +5 % efficiency growth and +10 % oil price resistance (`mdcw_cold_war_effects.txt:1157-1210`).

### 2.5 How the Politburo of the Republics already involves them (generated SOV system)

| Element | Code | Notes |
| --- | --- | --- |
| Membership trigger | `COLDWAR_SOV_is_union_republic` (triggers l.6) | `is_subject_of = SOV` + 14 tags |
| Seats (3) | `COLDWAR_SOV_setup_politburo` (`out/common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt:67`): UKR and KAZ start seated. `take/grant/leave/dismiss_seat` (l.1044-1080), idea `COLDWAR_SOV_politburo_seat` (PP +15 %, stability +5 %, construction +10 %) | Seat decisions are Moscow's (category `COLDWAR_SOV_politburo_seats_category`) |
| Votes | `COLDWAR_SOV_start_vote` (l.1084; temp `vt` 1 resolution, 2 plan, 3 leadership, 4 proposal; `vl` lean; `vs` subject; `vu` Union question), ballot event 11, tally event 12 (Moscow block = round(3.5 + 3.5 × bop × lean) + General Secretary + 1 per seat; ×2 on Union questions with Podgorny's federal union) | Only seat holders vote |
| Proposals | republic decisions `COLDWAR_SOV_propose_project_1..5`, `_plan_relief`, `_cadre_protection` (`out/common/decisions/COLDWAR_SOV_1970_decisions.txt:1218-1455`) → SOV event 20 → `COLDWAR_SOV_execute_proposal` (effects l.1513), or a refused proposal → `bring_before_politburo` → vote type 4 → event 22 | One proposal per session, 120-day lock, AI every 730 days |
| Union projects / aid | `COLDWAR_SOV_build_union_project` (l.1472; THIS = republic; SOV pays 0.4-0.8 % of its GDP; cohesion +1). Event 25 at each new plan for seat holders; petition event 29 for non-seat republics; SOV decision `development_fund` (0.5 % GDP, cohesion +5, not targeted) | |
| Plan side for republics | `propose_plan_relief` (republic gets `plan_relief`, SOV gets `plan_shortfall`), `report_overfulfilment` (pripiski, once per plan, `global.COLDWAR_SOV_plan`) | |
| Intrigue | kompromat (event 17/18), seek a patron (23), promotion to Moscow (19), KGB investigation | |
| Sovereignty path | `popular_front` (party 20 +5 %, cohesion -2) → `declare_sovereignty` (SOV cohesion < 55) → `independence_referendum` (cohesion < 35) → SOV event 24 (negotiate → event 61 Union Treaty offer; recognise → `end_puppet`; refuse). SOV offers: event 60 "Moscow offers independence" (republic decides), 61 "New Union Treaty" (decisions l.1581-1660; events l.538-572, 1476-1530) | Already offer-based and MP-safe |

---

## 3. Hooks a shared Union tree can use (no parallel systems)

| System | Entry point (read / write) | How the shared tree uses it | Caveat |
| --- | --- | --- | --- |
| Five-Year Plan clock | read `global.COLDWAR_SOV_plan` (8 → 9-12). Session event 10 sets it in windows ±20 days around 1 January 1971/76/81/86 (`out/events/COLDWAR_SOV_1970_events.txt:213-216`) and calls `COLDWAR_SOV_start_plan` (effects l.1594) | Gate one plan branch per plan (`check_variable = { global.COLDWAR_SOV_plan > 9 }`). Scale rewards by plan. | The value moves with the calendar, which effectively makes it a date gate; the README rule "no date gates" (17.10.2026) should rule on this. **SOV already has its own plan foci** (`COLDWAR_SOV_the_ninth_five_year_plan`, `…tenth…`, flag `COLDWAR_SOV_ninth_plan`) that do not read the global. Pick one plan clock. |
| Plan priority | SOV ideas `COLDWAR_SOV_plan_group_a/_b/_armaments/_agriculture` (PLAN_PRIOS, `/home/claude/sovgen/cw_sys_effects.py:532-535`), chosen by SOV decision + vote type 2 | Republic foci read `SOV = { has_idea = COLDWAR_SOV_plan_armaments }` and pay out accordingly (for example a military factory instead of agriculture) | Ideas exist only on SOV |
| Union project (event 25) | `set_temp_variable = { COLDWAR_SOV_prop_building = 1..5 } COLDWAR_SOV_build_union_project = yes` in republic scope | The main reward type for republics: builds in the SSR, Moscow pays a share of GDP, cohesion +1 | **Loc bug:** events 25, 31 and 81 have an option named `.d`, which overwrites the description key `COLDWAR_SOV.25.d` ("Build an agriculture district …" shows as the event text). Fix in `cw_events.py` (option keys or `desc` key). |
| Proposals | `COLDWAR_SOV_prop_type` 1/2/3 + `COLDWAR_SOV_execute_proposal`; SOV event 20 | A republic focus "submits the plan contribution" → Moscow approves or refuses (MP-safe) | Must respect `proposal_made`/`proposal_locked`, or the seat holders' privilege disappears |
| Union cohesion | `set_temp_variable = { COLDWAR_SOV_cohesion_delta = N } COLDWAR_SOV_change_union_cohesion = yes` works from **any** scope and redirects to SOV (effects l.296-307); tiers are SOV dynamic modifiers (>74, 35-54, 15-34, <15) | Republic foci move the Union-wide value; gates read `SOV = { check_variable = { COLDWAR_SOV_union_cohesion > 54 } }` | Design rule: no per-republic loyalty meters (`/home/claude/sov/d_republics.py` docstring) |
| Politburo votes | `COLDWAR_SOV_start_vote` / `COLDWAR_SOV_queue_resolution` (l.1409; RESOLUTIONS list in `d_republics.py`) | Union-wide decisions as a Politburo resolution (vote type 1, `vu = 1`) | Results of type 1 only touch SOV (PP/stability or "Defying the Politburo"). New resolution subjects need entries in RESOLUTIONS and the vote-subject scripted loc. |
| GDP money | `COLDWAR_SOV_pay_gdp_share`, `_receive_gdp_share`, `_transfer_gdp_share` (l.82-130; generic for THIS → `var:COLDWAR_SOV_transfer_target`), `_change_debt_gdp_share` (l.138) | Republic → Moscow contributions, Moscow → republic credits (inside an accepted event) | SSR treasury start value is not set in the 1970 block (MD default) |
| Comecon (Cold War) | read `has_global_flag = mdcw_cw_bp_2`; decision `mdcw_cw_dec_comecon` is player-only (SOV, 75 PP, `common/decisions/mdcw_cold_war_decisions.txt:46-78`) | Republic foci get a bonus "while the Comecon programme runs". A refund pattern exists (`COLDWAR_SOV_monthly_comecon_refund`). | Never call the programme effects from a focus |
| Cold War tension | `mdcw_cw_add_tension` (`mdcw_cw_tension_delta`) | Rarely; only for showcase foci | The generic tree's `GEN_1970_change_tension` writes the global directly (hooks audit l.279) |
| Cold War modifiers | `mdcw_cw_ideological_defence`, `mdcw_cw_market_exposure`, … plus `mdcw_cw_recalculate_country` | Small republic flavour | Recalculate after changes (hooks audit l.290) |
| Imperia investments | MD investment system is offer-based (`send_pending_investment_offer` / `accept_pending_investment_offer`, `common/scripted_effects/99_investment_scripted_effects.txt:81-101`); modifiers `imp_investment_in_extra`, `receiving_investment_cost_modifier` | "Union investment" foci: cheaper or more incoming slots, never forced projects | |
| Interest groups | MD internal factions (`change_<f>_opinion`, our `_exact` wrappers) | Mostly SOV side | SSRs have no faction ideas in 1970 |
| Sanctions / globalism / development | read-only arrays and tiers; `imp_sanction_resistance`, `globalism_equilibrium` as modifiers | Minor | Never write the sanction arrays or `globalism_value` |
| Oil | allowed: `add_resource = { type = oil }` in AZE/KAZ/TRK states, `oil_export_multiplier_modifier`, `imp_oil_price_resistance` | Baku and Mangyshlak flavour | **Player-only price.** No `imp_spike_oil_price`, OPEC vote or embargo calls, no `imp_oil_prices_ask_*` (hooks audit l.27, 31, 135) |
| Autonomy | `add_autonomy_ratio` (bar only); a new `COLDWAR_` autonomy state (for example "Union Treaty republic") is possible as a new file in `common/autonomous_states/` (replace_path; `allowed` must name SOV + SSR) | Treaty status as a real subject level, set only by an SOV-side accepted offer | The current state has `can_take_level = always no` |
| Special projects | `add_project_completion_progress` (facility scope, `common/special_projects/special_projects_documentation.md:400`); facilities in UKR/BLR states | Optional ("Kharkiv design bureau") | `imp_projects.txt` is empty |
| Inlay window | `common/focus_inlay_windows` | Show plan number, priority and cohesion on the Union tree | Needs GUI work |

---

## 4. Hard constraints

- **Engine and base:** `descriptor.mod` has `version="2.0.2"`, `supported_version="1.19.*"`, and `replace_path = "common/national_focus"`, `"common/autonomous_states"` and `"history/countries"`, so only mod files count. The Changelog header is v2.0.2. (The playbook from 28.09 still says 1.18; the generic-tree doc confirms MD 2.0.2 / HOI4 1.19 since 13.10.2026.)
- **`shared_focus`: available.** 9 roots in `00_generic.txt` and more elsewhere.
- **`joint_focus`: available.** 197 joint foci in 6 files, including `joint_trigger`, `completion_reward_joint_originator/_member`, `text_icon`, `select_effect` and `continue_if_invalid`. **No `is_joint` trigger** is used in the mod; do not plan with it.
- **Multiplayer rule:** no focus may force war, alliance, bases, territory, a bloc or annexation on another country; the other side gets offers and decides (hooks audit l.5; playbook §7). MD itself breaks this in shared trees: USoE101 has `will_lead_to_war_with = USA` + `create_wargoal` (`01_EU_USoE_shared.txt:488-503`), and Commonwealth/AU complete foci for all members via `unlock_national_focus`. Our consequences:
  - Joint foci may only be originated by one side and only include members that opted in. Example: `available = { original_tag = SOV … }` (the `03_china_russia_joint.txt:144-149` pattern) with `joint_trigger = { COLDWAR_SOV_is_union_republic = yes has_country_flag = COLDWAR_…_signed }`, where the flag comes from an accepted offer.
  - No mutually exclusive joint foci, and no costs in `completion_reward` or `completion_reward_joint_member`. Costs go into `completion_reward_joint_originator` or into the member's own accepted event (the CZE pattern).
  - No `end_puppet`, `set_autonomy`, `annex_country` or bloc change from a focus. Those stay in the existing offer events (24, 60, 61).
- **Naming and localisation:** every ID, flag, variable, idea, event namespace, file and loc key carries `COLDWAR_` (`/home/claude/sovgen/cw_common.py:1-3`). Proposal: prefix `COLDWAR_UNION_`, or keep `COLDWAR_SOV_` to stay inside the SOV generator, with namespace `COLDWAR_UNION`. English only, `localisation/english/*_l_english.yml`, UTF-8 with BOM. Custom search filters break the prefix rule (`FOCUS_FILTER_*`), so reuse MD filters or name a new one `COLDWAR_FOCUS_FILTER_UNION` with sprite `GFX_COLDWAR_FOCUS_FILTER_UNION`. No date gates in foci (README 17.10.2026).

---

## 5. Two ways to host it

| | A: attach to the generic tree | B: own SSR tree |
| --- | --- | --- |
| How | Add `shared_focus = COLDWAR_UNION_root` to `mdcw_1970_generic_focus` (another generator: `tools/generate_1970_generic_focus_tree.py`) and to `COLDWAR_SOV_1970_focus` (`cw_focus.py:226`); root `allow_branch = { OR = { original_tag = SOV COLDWAR_SOV_is_union_republic = yes } }`; `offset` triggered on `has_focus_tree` | New `COLDWAR_SSR_1970_focus` (shared root + per-republic content) loaded in the 14 SSR histories; add SSRs to `mdcw_load_1970_fallback_tree` |
| For | SSRs keep the 349-focus generic content; one line per host tree | Clean, small, republic-specific; no evaluation on 380 generic countries |
| Against | Touches a generator we do not own; `allow_branch` is evaluated for about 380 countries | 14 history patches; SSRs lose the generic political paths; `load_focus_tree` resets progress (use `keep_completed = yes` if ever reloaded) |

Recommended structure in both cases: a CZE-style mix.

- **Joint trunk:** Moscow originates, signed republics are members. One milestone per plan congress: "The IX Plan is adopted" … "XII".
- **Shared branches:** each republic researches its own plan contribution. Rewards come through `COLDWAR_SOV_build_union_project`, a proposal to Moscow (event 20), or cohesion.
- **SOV-side foci:** they send offers (Union investment credits, the treaty) instead of acting on republics directly.

---

## 6. Technical risks

1. **Joint completion acts on human players.** Rewards run in the member country without its input, and a member's mutually exclusive alternative gets locked. Mitigation: opt-in `joint_trigger`, no exclusive joint foci, no member costs, and an SOV-only originator. Also the reverse case: if an AI republic can originate, a human SOV player gets the completion too.
2. **Stale `allow_branch` and `offset`.** These are evaluated only at load and on `mark_focus_tree_layout_dirty`. Event 24 (`end_puppet`), event 60 and annexations should call `mark_focus_tree_layout_dirty = yes` in the affected country. `available` must re-check `COLDWAR_SOV_is_union_republic` (with default `cancel_if_invalid`). The same issue affects the existing decision category `COLDWAR_SOV_republic_politburo_category` (`allowed` is checked at start only).
3. **Tree hosting** (§5). With option B, forgetting the fallback whitelist lets old events reload the generic tree.
4. **Empty republic economies** (§2.3) make percentage rewards meaningless. Plan on buildings, flat PP/stability, and Moscow-paid projects. The MD helpers charge 7.5 treasury per building to a republic of unknown treasury unless `skip_payment = 1`.
5. **Two plan clocks:** SOV plan foci versus `global.COLDWAR_SOV_plan` (§3). Also, plan starts depend on session event 10 hitting the ±20-day windows; an extra session does not move the calendar, so this is fine, but gating on the plan number is a calendar gate in disguise.
6. **Focus time:** SOV already has 836 foci (21 years ≈ 1,100 cost units). The shared tree competes with them. Joint completion can save the members' focus time.
7. **AI duplication:** use MERCOSUR's `select_effect` + in-progress flag (joint) or AU's reservation flag (shared).
8. **Existing loc collision:** events 25, 31 and 81 (`.d` option versus `.d` description). It hits the Union-project event the tree would reuse.
9. **Interest-group effects are no-ops** in SSRs (no faction ideas in the 1970 block).
10. **Not verified here** (engine details to test in game):
    - whether a joint member needs the prerequisites;
    - whether parallel research of one joint focus is blocked;
    - the scope of FROM inside `completion_reward_joint_member` (MD never uses it);
    - whether a shortcut can target a shared focus;
    - the SSR starting treasury and laws.
