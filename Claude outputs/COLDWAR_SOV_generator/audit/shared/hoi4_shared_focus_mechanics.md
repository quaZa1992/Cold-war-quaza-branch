# HOI4 shared and joint focus mechanics: research for a Soviet + SSR "Five-Year Plan" tree

Research date: 17 Oct 2026. Target mod: MD Cold War. The uploaded copy's `descriptor.mod` says `version="2.0.2"`, `supported_version="1.19.*"`. The project playbook from 28 Sep 2026 still names 1.18 as the target. Every mechanic below exists in both versions. Joint focuses need 1.13.1 or later.

**Evidence labels**

| Label | Meaning |
|---|---|
| **[V]** | Verified on the web; the source is linked. |
| **[MD]** | Verified in the real script of the uploaded mod at `/mnt/user-data/uploads/mdcoldwar/`. That code is MD 2.x code that ships and loads. |
| **[I]** | My inference from the sources. It is not stated anywhere. |
| **[U]** | Unverified: I could not confirm it. Test it in game before relying on it. |

---

## 0. Summary

| | **Shared focus** (`shared_focus = { … }`) | **Joint focus** (`joint_focus = { … }`) |
|---|---|---|
| Introduced | Patch 1.5 "Cornflakes", 2018-03-08, with Waking the Tiger [V] | Patch 1.13.1, 2023-10-10, with Arms Against Tyranny [V] |
| DLC-gated? | No. It is an engine feature; WtT is now base game [V] | The engine feature appears in the general changelog, not the DLC section. Vanilla *content* using it checks `has_dlc`. MD uses it with no DLC check [V/MD]. Treat it as not gated [I]. |
| Completion | **Per country.** Every tree that includes it has its own copy. Two countries can both research and complete it, and each gets the rewards. No sync. [V/I] | **Synced.** One member researches it, and it "will complete in every relevant country" whose `joint_trigger` is true [V] |
| Simultaneous research | Yes, each country in its own tree | **No.** While one member researches it, the others see that member's flag and cannot select it [V, dev reply] |
| Progress pooling | No | **No.** Only the originator's research counts. Every country still has one focus slot, so a joint focus uses the originator's slot [V, dev reply] |
| Rewards | `completion_reward` for the country that completes it | `completion_reward` runs for **every** member. `completion_reward_joint_originator` runs only for the completer. `completion_reward_joint_member` runs for every member except the completer [V] |
| Attached to a tree via | `shared_focus = <root_id>` inside `focus_tree = { }` | The same line: `shared_focus = <root joint id>` [MD] |

---

## 1. Shared focuses

### 1.1 Version and history [V]

The Patch 1.5 "Cornflakes" modding changelog (2018-03-08, Waking the Tiger) contains these lines:

- "Added support for having national focuses that are shared between national focus trees"
- "Added effect to change focus tree, that also retains already completed shared focuses"
- "National focus can now handle multiple position offsets."

Source: https://hoi4.paradoxwikis.com/index.php?title=Patch_1.5

### 1.2 Syntax

**Definition.** A shared focus is a top-level block in any file under `common/national_focus/`, outside every `focus_tree`. It takes the same attributes as a normal `focus` [V Bitmode wiki]:

```
shared_focus = {
    id = shared_1
    x = 10
    offset = {              # several offset blocks are allowed; each adds x/y when its trigger is true at tree load
        x = 10
        trigger = { tag = LIT }
    }
    select_effect = { add_political_power = 10 }
    completion_reward = { army_experience = 10 }
}
```

**Inclusion.** You include it in a tree with `shared_focus = shared_1`. That line inserts "the referenced shared focus and its dependants", meaning everything that hangs off it through `prerequisite`. The line can appear many times in one tree [V]. Setting it to an ID that does not exist "causes a game crash when loading into the main menu" [V, wiki].

Real MD tree header [MD `05_russia.txt`]:

```
focus_tree = {
    default = no
    id = russia_focus
    country = { base = 0 }
    continuous_focus_position = { x = 17000 y = 1000 }
    initial_show_position = { x = 2 y = 0 }

    shared_focus = USoE001                              # EU shared tree root
    shared_focus = POTEF001
    shared_focus = CHI_SOV_treaty_good_neighbourliness  # a JOINT focus root, attached the same way

    shortcut = { name = SOV_military_tree_shortcut target = SOV_groznyy_offensive scroll_wheel_factor = 0.80 }
```

**Positioning.**

- The root of a shared branch needs absolute `x`/`y`, plus one `offset = { x y trigger = {…} }` for every tree or tag that hosts it.
  - MD's EU root `USoE001` carries more than 30 per-tag offsets [MD `01_EU_USoE_shared.txt`].
  - The Commonwealth root keys its offsets on `has_focus_tree = <tree id>` instead [MD `Commonwealth_shared.txt`]. That is cleaner when one tree hosts many tags:

    ```
    offset = { x = 38 y = 20 trigger = { has_focus_tree = ENG_1985_focus } }
    offset = { x = 34 y = 3  trigger = { has_focus_tree = india_focus } }
    ```

- Children use `relative_position_id = <another focus in the same shared branch>` [MD, used throughout].
  - The wiki prefers relative positioning: moving a parent moves its branch.
  - Circular `relative_position_id` chains can crash the game [V].
- Keep `relative_position_id` inside the shared branch [I]. A shared focus placed relative to a focus that exists in only one host tree has no anchor in the other trees [U: the exact behaviour was not tested].
- `offset` and `allow_branch` are evaluated **once, at tree load**. To re-evaluate them mid-game, use `mark_focus_tree_layout_dirty = yes` [V wiki; MD `00_focus_utilities.txt`].
- `initial_show_position` also accepts `offset` blocks [V].

**Visibility.** `allow_branch = { … }` hides the branch for countries that fail the trigger, evaluated at load [V].

- A focus with its own `allow_branch` ignores its parent's result. The first focus of every sub-branch must therefore repeat the parent's condition [V wiki].
- Example of a real gate on a global vote result [MD]:

  ```
  allow_branch = { is_in_array = { array = global.EU_passed_votes value = 111 } … }
  ```

**Cross-tree links.**

- `prerequisite` and `mutually_exclusive` may name focuses that are not in the current tree. The wiki says this works with shared focuses [V].
- OR logic goes in one block: `prerequisite = { focus = A focus = B }`. AND logic uses separate blocks [V].
- A mutual-exclusion line between a shared focus and a national focus is legal [V]. The arrows are drawn only when both sides are in the tree and exclude each other [V].

**Other attributes seen in MD shared trees** [MD]:

- `search_filters = { … }`
- `select_effect = { }`, which runs when the focus is *selected*
- `continue_if_invalid = yes`
- `ai_will_do`
- `log = "[GetDateText]: [Root.GetName]: Focus X"`, an MD convention

### 1.3 Behaviour

- Completion is stored per country. `SOV = { has_completed_focus = X }` and `UKR = { has_completed_focus = X }` are independent [I, consistent with the wiki and MD's "unlock for members" helpers, which exist because there is no sync].
- `has_completed_focus` is **false inside the focus's own `completion_reward`**. The focus is marked complete only after its effects run [V wiki].
- Duplicate focus IDs across trees break prerequisite lines, `complete_national_focus` and `has_completed_focus` [V wiki]. Shared focuses exist to avoid exactly this.
- The 1.5 changelog says changing tree with `load_focus_tree` can keep completed shared focuses [V]. The exact parameter is unverified: it is usually written `load_focus_tree = { tree = X keep_completed = yes }` [U]. The mod itself only uses the plain form `load_focus_tree = mdcw_1970_generic_focus` in country history [MD].

---

## 2. Joint focuses

### 2.1 Version and sources

- **Patch 1.13.1, released 2023-10-10 with Arms Against Tyranny.** 1.13 itself was never released. The changelog's Feature section says: "Added modding and script support for 'joint' national focuses", allowing several countries to progress in one shared focus branch [V].
  - Source: https://hoi4.paradoxwikis.com/Patch_1.13
- The "Joint Focus Tree" dev diary was published 2023-07-26 by Carlo; it covers the Nordic tree.
  - https://store.steampowered.com/news/app/394360/view/5925098517647303884
  - https://devtrackers.gg/heartsofiron/p/83a8023c-developer-diary-joint-focus-tree
- The modding dev diary was published 2023-09-13.
  - https://forum.paradoxplaza.com/forum/developer-diary/developer-diary-modding.1598797/

### 2.2 Syntax

This is real, loading MD code [MD `03_china_russia_joint.txt` and `03_benelux_shared.txt`]. The block keyword is `joint_focus`; everything else is the normal focus syntax.

```
joint_focus = {
    id = CHI_SOV_turn_to_east
    icon = diplomacy
    text_icon = JOINT_SOV_focus_style          # title-bar style, flags of the participants (see 2.4)

    x = -2
    y = 1
    relative_position_id = CHI_SOV_sco_framework
    cost = 10
    prerequisite = { focus = CHI_SOV_sco_framework }
    search_filters = { FOCUS_FILTER_POLITICAL }

    joint_trigger = {                          # WHO is a member and receives the effects
        OR = { original_tag = CHI original_tag = SOV }
    }

    available = {                              # WHO may research it ("single-flag" focus: only SOV)
        original_tag = SOV
        CHI_SOV_joint_focus_available = yes
    }

    completion_reward_joint_originator = {     # only the completer
        add_political_power = 50
        add_stability = 0.02
    }
    completion_reward_joint_member = {         # every member except the completer
        add_opinion_modifier = { target = SOV modifier = mutual_trade_agreement }
    }
    ai_will_do = { base = 8 modifier = { factor = 0 date < 2004.1.1 } }
}
```

Benelux uses a `completion_reward` that runs for every member, alongside the originator and member blocks [MD]:

```
joint_focus = {
    id = BNL_benelux_union_treaty
    text_icon = JOINT_BEL_LUX_HOL_focus_style
    x = 60  y = 0
    offset = { trigger = { original_tag = HOL } x = 70 }
    cost = 10
    allow_branch = { is_benelux_country = yes }
    joint_trigger = { is_benelux_nation = yes }
    available = { benelux_cooperation_trigger = yes }
    completion_reward = {                      # EVERY member runs this in its own scope
        add_dynamic_modifier = { modifier = BNL_dynmod_union }
        add_to_variable = { BNL_integration = 15 tooltip = BNL_integration_tt }
    }
    completion_reward_joint_originator = { add_political_power = 150 add_stability = 0.02 }
    completion_reward_joint_member     = { add_political_power = 50 }
    ai_will_do = { base = 1 }
}
```

**Membership triggers in MD** [MD]:

| Tree | `joint_trigger` |
|---|---|
| CHI–SOV, CHI–NKO, Korea | Tag lists |
| Benelux | `is_benelux_nation = yes` |
| MERCOSUR | `has_dynamic_modifier = mercosur_member_state_modifier`, with `allow_branch = { is_in_array = { global.mercosur_potential = THIS } }` |

The dev diary's own example checks "the alliance leader flag or whether the country is in a faction with the focus owner". The code itself is only shown as an image [V].

**Scope inside `joint_trigger`.** THIS is the candidate country; every MD example is written that way [MD]. Whether ROOT or FROM points to the originator is not documented [U].

A developer's forum reply on how these files are organised: "It's a regular old shared national focus file, the 'jointness' of them is defined focus by focus" [V]. A file can therefore mix plain `shared_focus` and `joint_focus` blocks; `03_benelux_shared.txt` contains only `joint_focus` [MD]. Whether a plain shared focus can be a child of a joint focus is untested [U]. MD keeps each file to one kind.

### 2.3 Behaviour

Developer statements, quoted from the dev diary and replies [V]:

| Question | Answer |
|---|---|
| Who can complete it | "anyone can complete focuses in it", meaning any member, and "Denmark can complete any focus that requires it while Norway does another focus." |
| Sync | "they will complete in every relevant country, giving effects to all … members". The wiki adds that the focus "will automatically complete for the other nations in the faction". |
| Locking | Players see the flag of the country researching a joint focus, and nobody else can select that focus. Other joint focuses stay open. |
| Focus slot | "you can only do one at a time", so researching a joint focus uses the country's single focus slot. |
| Rewards | Originator effects are usually better. In the Nordic Joint Military Exercises focus, the completer gets 80 army XP and two 75% doctrine bonuses; every other member gets 60 XP and two 50% bonuses. |
| Instances | "There can only be one instance of each Joint Focus Tree" (forum reply). Several *different* joint trees can run at once. |
| Leaving | In the Nordic tree, changing ideology or becoming a puppet removes access to the tree and its spirit. Factories, techs and manpower already gained are kept. |
| Access | "It's a trigger, whatever countries meet that trigger will have access to it." Any group can share one; it does not have to be a faction. The modding diary's examples are a continent, all communist countries, and both sides of a war. |
| AI | Vanilla Nordic: "Right now, I have it so the AI will never start the Joint Focus tree", and "AI will not touch mutually exclusive focuses". This is a content choice. The engine uses normal `ai_will_do`; MD gives joint focuses AI weights [MD]. |

Inferences and open points:

- **Fixed-tag effects in `completion_reward` run once per member** [I]. The block runs "for every valid country", so `SOV = { add_political_power = 50 }` placed there fires N times; with 15 members, 15 times. Put one-off and global effects in `completion_reward_joint_originator`, or guard them with `if = { limit = { tag = SOV } }`.
  - MD `KOR_joint_peace` has `KOR = { support_for_reunification_2 = yes }` inside `completion_reward`. If the inference is right, that effect fires twice; it may be an MD bug [I].
- **Late joiners.** Whether a country that meets `joint_trigger` *after* some joint focuses are done gets them retroactively is undocumented [U]. Plan a catch-up effect (pattern B in §8).
- **Members without the focus in their tree.** Whether a member gets the completion when its tree does not include the joint focus is undocumented [U]. Vanilla and MD always include the joint root in **every** member's tree. Do the same.
- **The originator stops qualifying mid-research.** Behaviour is undocumented when the originator stops meeting `joint_trigger` or is annexed while researching [U]. Use `continue_if_invalid` or `cancel_if_invalid` deliberately.

### 2.4 Related 1.13 modding features [V, modding diary; MD]

- `text_icon = <style>` sets a title-bar style per focus.
  - Styles are defined in `common/national_focus/00_titlebar_styles.txt` as `style = { name = … unavailable = GFX completed = GFX available = GFX current = GFX }`. Each style needs four sprites in a `.gfx` file.
  - The mod already has `JOINT_SOV_focus_style`, `JOINT_SOV_CHI_focus_style`, `JOINT_AFG_IRQ_PER_TUR_focus_style` (the Saadabad style), `JOINT_BEL_COG_focus_style` and others [MD].
  - **There are no SSR styles yet.** `JOINT_TAI_CHI_` and `JOINT_TAI_` are each defined twice; harmless, but worth cleaning up.
- Dynamic icons: `icon = { gfx_a = { trigger } gfx_b = { trigger } gfx_default = yes }` plus `dynamic = yes`. The first true entry wins.
  - MD `05_centralasia.txt` uses this. It is one tree for Kazakhstan, Kyrgyzstan and Uzbekistan, with per-tag icons.
  - Its names use localisation such as `CES_our_state_kaz: "Our [ROOT.GetName]"` [MD].
- `event_option_tooltip` effect [V].
- Tree `shortcut = { name target scroll_wheel_factor }` [MD].
- **Focus inlay windows**, documented in `common/focus_inlay_windows/documentation.md` and shipped in the mod [MD]:

  ```
  my_inlay = {
      window_name = gui_component_name
      internal = yes/no              # yes = only visible to the country itself
      visible = { … }
      scripted_images = { icon_name = { gfx_a = { trigger } gfx_b = yes } }
      scripted_buttons = { button_name = { available = { } click_effect = { } } }
  }
  # in the focus_tree:
  inlay_window = { id = my_inlay position = { x = 1200 y = 50 } }
  ```

  Patch 1.17 added "support for buttons with scripted effects in the focus tree inlay window" [V].
- `reduce_focus_completion_cost = { focus = { X } cost = 25 }` [MD `common/ideas/05_china.txt`; the 1.19 changelog fixes its tooltip]. Whether `cost` is in days or percent is unverified [U].

---

## 3. Vanilla reference trees

### 3.1 Saadabad Pact: Graveyard of Empires (2025-03-04, patch 1.16) [V]

**Members and requirements.** Afghanistan, Iraq, Iran and Turkey. Requires Graveyard of Empires. Iran can found the treaty from its historical "reforms" branch, and the treaty "is no longer strictly available to Turkey" [V Iran dev diary].

**Founding.** The root focus, The Saadabad Pact, requires:
- that the `saadabad_pact_rejected` flag is not set
- peace with all four countries

**Membership.**
- The originator gets the dynamic modifier "The Saadabad Pact" (+5% stability) and sets the `SSB_leader` variable.
- The other three countries get an event inviting them to join.
- Membership is tracked by that modifier. Later focuses check "Has Modifier: The Saadabad Pact", which works as a joint-trigger-style gate.

**Leaving.** "Starting an offensive war against any member … will cause you to permanently lose this spirit." The wiki says nothing else about leaving.

**Rewards.** Rewards are split between "Originator" and "Every/Other Member":
- Expand our Influence: the originator gets −20% war goal time, −20% annex cost and +12.5% political power. The others get −15%, −15% and +7.5%.
- SAVAK to Protect Us All also requires Iran's national focus Form SAVAK. This is a cross-tree gate.
- Integration of our Infrastructure gives everyone a trade spirit with −30% trade cost towards the other members.
- Several focuses are bypassed if their conditions fail, for example the railway focus when a member is in civil war. The 1.19 changelog fixed an empty bypass tooltip on "Expand Road and Rail Connections".

**Attachment.** The wiki says the branch is "available for" the four trees. I infer that it is included in each of the four trees through `shared_focus` [I].

Sources:
- https://hoi4.paradoxwikis.com/Saadabad_Pact_joint_national_focus_tree_branches
- https://devtrackers.gg/heartsofiron/p/59f3158e-developer-diary-historical-iran
- https://hoi4.paradoxwikis.com/Patch_1.16

### 3.2 Belgium and Belgian Congo: Götterdämmerung (2024-11-14, Expansion Pass 1) [V]

The patch number is probably 1.15 [I].

**Subject status.** Congo starts as a Belgian colony, which uses the puppet autonomy system. Without the DLC, Belgium owns the Congo as colonial states and the Congo is only a releasable.

**The shared Colonial Branch.**
- **Flags show who can take a focus.** Focuses with a single flag can be taken only by that country. Focuses with both flags side by side can be taken by either.
- "As one country completes a focus in this section, it will also be completed for the other, with both nations getting something from it."
- **Entry points:**
  - Belgium enters through Monetary Reconstruction, then Congo Investments.
  - The Congo enters through Belgian Congo, then The Heart of Africa.
- **Gates.** Some focuses are gates: "one country needs to complete a focus before the other can progress down a mini branch".

**Two directions on the axis of exploitation.**
- The left side extracts resources: CCCI and Forminière mining firms, gold, diamonds and Shinkolobwe uranium. It **raises** Congo's autonomy.
- The right side develops the colony: rubber, agriculture and infrastructure. It **lowers** autonomy.
- Belgium's later Overlord branch "generally takes things from Congo, without recompense."
- Belgium's Uranium Development Trust helps nuclear special projects for its whole faction. The Congo can smuggle uranium to other majors.

**Status outcomes.** At the tier-3 focus "Congo's Place in the World", the current autonomy decides the Congo's status:

| Status | Result |
|---|---|
| Congo Free State | Belgium annexes the Congo |
| Overseas Department | Puppet |
| Dominion | Dominion |
| Republic | Independence |

**Branch lock.** "If Belgium is no longer the Overlord, then this whole Colonial Branch will be locked."

**Other content.**
- Belgium's "Belgian Miracle" focus needs a kept status plus Engine of the Economy.
- The Force Publique is locked to Belgium unless the Congo is at war.
- Independence also has a peaceful route: democracy support plus an independence score.

**Patch 1.19 fixes.** "Belgium will no longer get a puppet war goal on Congo." The Republic of Congo focus now bypasses correctly when the Congo is at war.

Sources:
- https://admin-forum.paradoxplaza.com/forum/developer-diary/developer-diary-congo.1712644
- https://devtrackers.gg/heartsofiron/p/233414a2-developer-diary-congo
- https://hoi4.paradoxwikis.com/Belgian_Congo
- https://hoi4.paradoxwikis.com/Belgium
- https://hoi4.paradoxwikis.com/Patch_1.19

### 3.3 Other vanilla examples

**Nordic joint tree** (AAT, 1.13.1) [V]: Denmark, Finland, Iceland, Norway and Sweden.
- Form the Nordic Council requires being a fully independent faction leader whose allies are all Nordic.
- One tree serves three ideological alliances: Nordic Council, Northern People's Union and Norden League. Names, icons and effects are dynamic.
- Sub-branches: Northern Command (military), Political Cooperation (a free intelligence agency) and the Nordic Research Council.
- https://hoi4.paradoxwikis.com/Nordic_joint_national_focus_tree_branches

**Austro-Hungarian joint branch** (Götterdämmerung) [V]: Austria, Hungary, Czechoslovakia, Albania and many releasables. **This is the closest analogue to "a union of member republics".**
- Austria unlocks it with Danubian Federation or Demand Hungarian Submission. Hungary unlocks it with Lands of the Crown of Saint Stephen or A Danubian Federation.
- Eligibility is built on subject and faction ties: "can only be done by the originator, or a contingent state if it is a subject or is in a faction with the originator".
- Example rewards:
  - Indivisible and Inseparable: +150 PP for the originator, +50 for the others.
  - Common Army gives every member a shared spirit.
  - The final Imperial Diet focus upgrades every member's spirit and adds **daily autonomy loss**.
- https://hoi4.paradoxwikis.com/Austro-Hungarian_joint_national_focus_tree_branches

**Chinese shared branches** (Waking the Tiger; reworked in No Compromise, No Surrender, 1.17) [V]: shared by Manchukuo and the Reorganized National Government, **both Japanese subjects**, and by warlords who become leader of China. It is the classic "subjects share a tree" case.
- https://hoi4.paradoxwikis.com/Chinese_shared_national_focus_tree_branches

**Liangguang Incident** and **Ma Clique** joint branches (NCNS) [V]: two warlord cliques; some focuses are clique-specific, and rewards split into originator and every member.
- https://hoi4.paradoxwikis.com/Liangguang_Incident_joint_national_focus_tree_branches

**Baltic shared branches** (No Step Back) [V]: Estonia, Latvia and Lithuania. This is a plain shared branch: each country completes it independently. It has no Soviet-subject or SSR mechanics.
- https://hoi4.paradoxwikis.com/Baltic_shared_national_focus_tree_branches

**British Raj and the UK** [V]: a colony with **no** joint branch. Independence runs through the Raj's own loyalty branch ("All three sections must be completed to become free"). A Princely States spirit gives −0.1 daily autonomy progress. Revolts and Forward Bloc give war routes against the UK.
- This is an example of overlord–subject interaction done with plain focuses, decisions and autonomy.
- Graveyard of Empires rewrote the tree. Patch 1.19 added "Raj: … 'Five Year Plan'" focus filters, so a Raj Five Year Plan focus exists.
- https://hoi4.paradoxwikis.com/index.php?mobileaction=toggle_view_desktop&title=British_Raj

**Patch 1.17** added "the Warsaw Pact focus for the Soviet Union" and the new **faction system**: faction rules, goals, theatres and shared intelligence [V]. https://hoi4.paradoxwikis.com/Patch_1.17

The full list of wiki "joint" and "shared" pages also includes ABDACOM, Indonesia, Paraguay/Uruguay and the Trial of Allegiance shared military branches [V].
- https://hoi4.paradoxwikis.com/Category:National_focus_trees

---

## 4. How Millennium Dawn uses shared and joint trees (from the uploaded mod files)

| File | Type | Count | How it is attached | Membership and synchronisation |
|---|---|---|---|---|
| `01_EU_USoE_shared.txt`, `02_EU_POTEF_shared.txt` | shared | 90 / 74 | `shared_focus = USoE001 / POTEF001` in the generic, Russia, Ukraine and Belarus trees, among others | `allow_branch` uses a long `original_tag` list plus **global vote results** (`global.EU_passed_votes`). The voting machinery uses global arrays (`EU_member`, `EU_active_vote_supporters`, `EU_active_vote_rejecters`), missions as vote timers, and on_actions that clean up on annexation |
| `Commonwealth_shared.txt` | shared | 23 | generic, UK, Canada, India and other trees, with offsets on `has_focus_tree` | `has_idea = commonwealth_of_nations_member`. Sync is emulated: the scripted effect `COMMONWEALTH_unlock_<focus>_for_members` loops over `every_other_country` with that idea and runs `unlock_national_focus` where the focus is not yet complete |
| `06_AfricanUnion_shared.txt` | shared | 39 | generic tree | `global.AU_member` array. **Reservation pattern:** `select_effect` sets `<focus>_reserved`, `available` blocks it for others, `continue_if_invalid = yes`. Then `completion_reward` loops the array and runs `unlock_national_focus` plus a smaller reward for every other member |
| `gulf_shared.txt`, `06_czehcoslavakia_shared.txt`, `03_shared_korea_unified.txt` | shared | 21 / 33 / 86 | tag lists | per country |
| `03_benelux_shared.txt`, `06_MERCOSUR_shared.txt`, `03_china_russia_joint.txt`, `03_china_north_korea_joint.txt`, `03_joint_korea_confederation.txt` | **joint** | 33 / 22 / 29 / 59 / 28 | `shared_focus = <root>` | `joint_trigger` built from tags, a scripted trigger or a dynamic modifier |
| `05_centralasia.txt` | one *tree* for several tags | 1 tree | `load_focus_tree` | Dynamic icons and `[ROOT.GetName]` names |

Conclusion: MD's older shared trees (EU, Commonwealth, African Union) **emulate joint behaviour by hand** with `unlock_national_focus`, global arrays and reservation flags, because they predate 1.13. The newer trees (Benelux, MERCOSUR, CHI–SOV, Korea) use the native `joint_focus`. Russia's `05_russia.txt` already includes the CHI–SOV joint root, so joint focuses demonstrably work in the SOV context of this mod.

A player comment on the Steam dev-diary thread notes that "shared focuses already existed in Millennium Dawn" before vanilla's joint trees [V]. https://steamcommunity.com/app/394360/eventcomments/3802778195610233442

**Current mod state that matters for the SSR tree** [MD; project doc `claude/mdcw_sov_1970_implementation.md`]:

- **SSR subject status.** The SSRs are subjects through `set_autonomy = { target = UKR autonomy_state = autonomy_soviet_republic_1985 }`, set for all 14 in `history/countries/SOV - Russia.txt`. **Warsaw Pact countries are also subjects of SOV** (`autonomy_warsaw`: DDR, POL, …), so `is_subject_of = SOV` alone is **not** a valid SSR test.
- **Trigger to reuse.** `COLDWAR_SOV_is_union_republic` (`is_subject_of = SOV` plus a 14-tag list) already exists in the SOV generator output. Reuse it in `joint_trigger` and `allow_branch`.
- **Trees.**
  - The SSRs load `mdcw_1970_generic_focus` (349 focuses), which **many other countries share**.
  - SOV loads `COLDWAR_SOV_1970_focus` (836 focuses).
  - The shared root therefore needs two offsets, `has_focus_tree = COLDWAR_SOV_1970_focus` and `has_focus_tree = mdcw_1970_generic_focus`, plus an `allow_branch` that hides it from non-SSR users of the generic tree. The alternative is a dedicated SSR tree.
- **Existing SOV plan system.** SOV's tree already has the 9th, 10th and 11th Five-Year-Plan focuses, plus decision categories "Five-Year Plans", "The Union" (cohesion) and Politburo votes. The shared tree should plug into these. Do not duplicate them.

---

## 5. Mechanics toolbox for a multiplayer union tree

| Need | Tool (exact names) | Notes |
|---|---|---|
| Union-wide milestone that every republic gets | `joint_focus` + `joint_trigger` | Native sync. Only one researcher at a time; it uses that country's slot |
| Moscow-only directive ("single flag") | `available = { original_tag = SOV }` on a joint focus | The Belgium–Congo pattern. MD `CHI_SOV_turn_to_east` |
| Task for one specific republic | `available = { original_tag = KAZ }` | Its originator reward is local; its member reward is union-wide |
| Republic-local copy, done by each republic itself | plain `shared_focus` | Completion is per country; two republics can do it at once |
| Effects on everyone | `completion_reward` (joint), `every_country = { limit = { COLDWAR_SOV_is_union_republic = yes } }`, `every_subject_country` (added 1.11) [V], `for_each_scope_loop = { array = global.X }` [MD] | In joint focuses, avoid fixed-tag effects in `completion_reward` (they run N times) |
| Overlord effects only | `completion_reward_joint_originator` with `if = { limit = { tag = SOV } }`, or `SOV = { … }` | |
| Shared progress meter | `global.<var>` via `add_to_variable` / `check_variable`; reading another country's variable (`value = SOV.var` [MD]) | Global variables are the safest. Writing as `var = SOV.x` is unverified [U]; scope into `SOV = { }` instead |
| Shared effect object | `add_dynamic_modifier = { modifier = X scope = SOV }` (the `scope` parameter is documented) [V] | Variable-driven modifiers, as in MD BNL. Modifiers update daily, or immediately with `force_update_dynamic_modifier` |
| Contributions shorten union focuses | `reduce_focus_completion_cost = { focus = { X } cost = N }` [MD] | The cost unit is unverified [U] |
| Membership list | `add_to_array` / `remove_from_array` / `is_in_array` on `global.<array>` [MD] | Keep it updated from `on_subject_free`, `on_puppet`, `on_annex` (vanilla on_actions doc) [MD] |
| Re-show or hide a branch after status changes | `mark_focus_tree_layout_dirty = yes` | Re-evaluates `allow_branch` and `offset` [V] |
| Mark done without effects | `unlock_national_focus = X` | MD uses it to sync members and then applies its own smaller effects. That implies it skips `completion_reward` [MD/I] |
| Mark done with effects | `complete_national_focus = X` | Runs the rewards. MD uses `SER = { complete_national_focus = SER_union_state }` |
| Reset a cycle | `uncomplete_national_focus = { focus = X uncomplete_children = yes refund_political_power = no }` [MD] | Behaviour on joint focuses is untested [U] |
| Cross-country gates | `available = { SOV = { has_completed_focus = X } }` or `custom_trigger_tooltip` | Draws no line. It is the Belgium–Congo "gate" pattern |
| Competition and ranking | Per-country variables updated monthly, plus a loop to find the leader | The leader gets a dynamic modifier |
| Voting | MD EU pattern: global supporter and rejecter arrays, a mission as timer (`activate_mission`), a decision per member, AI auto-vote in an on_action, and the result stored in a global array or flag that gates `allow_branch` or `available` | SOV already has "votes, proposals" scripted effects |
| Dashboard | `inlay_window` with `scripted_images` and `scripted_buttons` (1.17+) | `internal = no` lets every republic see the union plan status |
| Faction-level goal (optional) | 1.17 faction goals with `ratio_progress = { total_amount / completed_amount }` or collections (`common/factions/_documentation.md`) [MD] | Only if all SSRs are in SOV's faction. It covers the whole faction, Warsaw Pact included |

**Why forcing `complete_national_focus` on other players is bad in MP** [I]:

- It runs another player's rewards without consent.
- It can complete a focus that is mutually exclusive with that player's chosen path, which permanently locks them out.
- The target gets no prompt, and tooltips appear only to the caller.
- If the target is researching that focus, the outcome is untested [U].

What to use instead:
- the native `joint_focus`, which is designed for this;
- an event with options;
- `unlock_national_focus` only for pure bookkeeping, with a notification;
- forced completion restricted with `limit = { is_ai = yes }`.

---

## 6. Pitfalls

1. **Crash on bad references.** A missing `shared_focus` ID crashes at the main menu [V]. Circular `relative_position_id` chains can crash [V].
2. **Duplicate IDs** break lines and `has_completed_focus` [V]. Prefix everything (`COLDWAR_SU_…`).
3. **`allow_branch` runs only at load.**
   - It also does not cascade: every sub-branch head must repeat the condition [V].
   - Call `mark_focus_tree_layout_dirty` after an SSR becomes independent, for example from `on_subject_free`.
   - Lock the union branch then, as Belgium–Congo does.
4. **A generic tree shared by many tags.** Every user of `mdcw_1970_generic_focus` loads the branch layout. `allow_branch` must hide it cleanly, and offsets must be keyed on `has_focus_tree`.
5. **Joint pacing.**
   - Up to 15 countries can each research a different joint focus at the same time, so a joint branch can finish many times faster than a national tree.
   - Gate it with dates (24th Party Congress 30 Mar–9 Apr 1971; 25th, Feb–Mar 1976; 26th, Feb–Mar 1981; 27th, Feb–Mar 1986) and/or a global plan-year variable [I].
6. **AI.**
   - Joint focuses use normal `ai_will_do`. With 14 AI republics, whichever selects first takes the focus, which can snipe "Moscow's" focuses from a human SOV player. Make directives SOV-only.
   - Low `ai_will_do` values are picked less often than intuition suggests, and a focus whose prerequisite was just completed gets ×1.5 [V wiki].
   - Vanilla deliberately keeps the AI from starting the Nordic tree [V].
   - MD sometimes leaves `base = 1`, so the AI effectively ignores the branch [MD].
7. **N-fold effects.** In `completion_reward` of a joint focus, effects on fixed tags or globals run once per member [I]. Put them in `completion_reward_joint_originator`.
8. **Late joiners and leavers.** Membership changes are not retroactive [U]. Write explicit catch-up and lock logic.
9. **Localisation and icons.**
   - Each focus ID needs one name key and one description key. Use `[ROOT.GetName]` or scripted localisation for per-republic text [MD].
   - Icons use `icon = { … } dynamic = yes`.
   - Joint title bars need new `style` entries with four GFX each; none exist for the SSRs.
   - In `common/national_focus/00_titlebar_styles.txt`, `JOINT_TAI_CHI_focus_style` and `JOINT_TAI_focus_style` are defined twice.
10. **Performance.**
    - No hard limit on tree size was found [U]. MD Russia (806 focuses) and SOV 1970 (836) load fine.
    - Keep `available`, `bypass` and `joint_trigger` cheap: scripted triggers on flags and variables, not `any_country` scans.
    - A Paradox performance diary notes that bypass checks once scanned every focus and are now limited to focuses that could plausibly bypass. A player reported a scripted-localisation tooltip that recalculated every tick while its window was open [V]. https://admin-forum.paradoxplaza.com/forum/developer-diary/developer-diary-performance-modding.1713814
    - MD's game rule `obsolete_focus_branches_visibility = HIDE` plus `mark_focus_tree_layout_dirty` hides dead branches [MD].
11. **Saves** [I/U].
    - Completed focuses are stored by ID per country. Adding new shared or joint focuses to an existing tree is generally safe for old saves, and the layout is rebuilt at load.
    - Renaming or removing IDs loses progress or strands prerequisites.
    - Moving a country to another tree needs `load_focus_tree` in an on_action for existing saves.
12. **`has_completed_focus` inside its own reward** is false [V]. Use a flag if logic in the same reward needs it.

---

## 7. Version notes for this mod (1.18 / 1.19)

Everything above is available:

| Feature | Since |
|---|---|
| Shared focuses | 1.5 |
| `every_subject_country` | 1.11 |
| Joint focuses, `text_icon`, dynamic icons | 1.13.1 |
| Faction rework, inlay buttons | 1.17 |
| `reduce_focus_completion_cost` tooltip fix | 1.19 |

The DLC dates come from https://hoi4.paradoxwikis.com/Downloadable_content:

| DLC | Release |
|---|---|
| AAT | 2023-10-10 |
| Trial of Allegiance | 2024-03-07 |
| Götterdämmerung | 2024-11-14 |
| GoE | 2025-03-04 |
| NCNS | 2025-11-20 |
| Peace for Our Time | 2026-04-22 |
| Thunder at Our Gates | 2026-06-11 (patch page: 06-10) |

---

## 8. Design patterns for a Soviet + SSR Five-Year-Plan tree

### A. One joint root with Belgium–Congo-style flags

Build one joint root, included in both host trees. Inside it, mark each focus by who can take it:
- **Union directives**, SOV only.
- **Republic commissions**, open to a named republic or region.
- **Open focuses**, any member.

```
joint_focus = {
    id = COLDWAR_SU_ninth_plan_directives
    text_icon = JOINT_SOV_focus_style
    x = 0  y = 0
    offset = { trigger = { has_focus_tree = COLDWAR_SOV_1970_focus } x = 200 y = 14 }   # numbers: placeholders
    offset = { trigger = { has_focus_tree = mdcw_1970_generic_focus } x = 40 y = 0 }
    cost = 5
    allow_branch = { OR = { original_tag = SOV COLDWAR_SOV_is_union_republic = yes } }
    joint_trigger = { OR = { original_tag = SOV COLDWAR_SOV_is_union_republic = yes } }
    available = { original_tag = SOV date > 1971.4.9 }          # only Moscow opens the plan
    search_filters = { FOCUS_FILTER_INDUSTRY }
    completion_reward = {                                       # every member, own scope only
        log = "[GetDateText]: [Root.GetName]: Focus COLDWAR_SU_ninth_plan_directives"
        add_dynamic_modifier = { modifier = COLDWAR_SU_plan_member_modifier }
    }
    completion_reward_joint_originator = {                      # once: globals here
        set_global_flag = COLDWAR_SU_plan9_active
        set_variable = { global.COLDWAR_SU_plan_fund = 0 }
    }
    ai_will_do = { base = 50 }
}

joint_focus = {
    id = COLDWAR_SU_virgin_lands_second_wave                    # republic commission
    text_icon = JOINT_SOV_focus_style                           # better: a KAZ+SOV style
    x = -3  y = 1
    relative_position_id = COLDWAR_SU_ninth_plan_directives
    cost = 7
    prerequisite = { focus = COLDWAR_SU_ninth_plan_directives }
    joint_trigger = { OR = { original_tag = SOV COLDWAR_SOV_is_union_republic = yes } }
    available = { original_tag = KAZ }                          # only Kazakhstan can research it
    completion_reward_joint_originator = { add_stability = 0.03 }      # local reward
    completion_reward_joint_member = { add_political_power = 10 }      # small union reward
    ai_will_do = { base = 30 modifier = { factor = 0 NOT = { original_tag = KAZ } } }
}
```

### B. Membership, catch-up and lock

Keep `global.COLDWAR_SU_members` as an array. When a republic leaves (`on_subject_free`):
- remove it from the array;
- set a flag such as `COLDWAR_SU_left_union`, so its `allow_branch` and `available` fail;
- call `mark_focus_tree_layout_dirty = yes`.

When a republic joins or re-joins, `unlock_national_focus` every union directive that is already complete, using a scripted effect like MD's `COMMONWEALTH_unlock_<focus>_for_members`. That way joint progress is not lost.

Mirror Belgium–Congo: if SOV is no longer the overlord, the plan branch locks.

### C. Contributions: Gosplan fund and plan fulfilment

A decision category visible to members while `COLDWAR_SU_plan9_active` is set provides "Deliver Above Plan" and "Ship Equipment to the Union Fund". Each costs political power or factories and:
- adds to `global.COLDWAR_SU_plan_fund`;
- adds to the republic's own `COLDWAR_SU_emulation_score`;
- runs `SOV = { reduce_focus_completion_cost = { focus = { COLDWAR_SU_ninth_plan_review } cost = N } }`.

SOV's review focus requires `check_variable = { global.COLDWAR_SU_plan_fund > X }`. Moscow then spends the fund (investment events or decisions per republic). This creates real progress pooling, which the engine does not provide [I].

### D. Socialist emulation: competition between republics

Socialist emulation was a real Soviet institution: the "Challenge Red Banner" awards between republics.
- A monthly on_action ranks the members by score.
- First place gets a 6-month dynamic modifier and a Moscow investment.
- Last place gets a Gosplan audit event.

Add an extraction-versus-development axis like Belgium–Congo's:
- Extraction focuses (raw materials for the centre) pay SOV and **lower union cohesion** or raise nationalist drift.
- Development focuses (consumer goods, local industry) cost SOV but **raise cohesion**.
- Tie this into SOV's existing "The Union" cohesion system.

### E. Council of Nationalities vote

A SOV-only joint focus opens the vote. Each republic votes with a decision on the plan's priority (Group A heavy industry, Group B consumer goods, agriculture), within a mission timer. AI republics vote in an on_action. The result is a global flag that sets `available` on the following directives, so the branches become mutually exclusive by vote. Reuse SOV's existing vote and proposal scripted effects.

### Extras

- **Pacing.** Gate each Five-Year-Plan stage to its Party Congress dates.
- **Dashboard.** Show plan status in an `inlay_window` with per-republic fulfilment bars and a "pledge" `scripted_button`.
- **Text.** Use `[ROOT.GetName]` and dynamic icons per republic.
- **Title bars.** Make a `JOINT_SOV_SSR_focus_style` plus regional styles for the Baltics, the Caucasus and Central Asia.
- **Force AI only.** Never call `complete_national_focus` on human SSRs; restrict forced completion with `is_ai = yes`.

---

## 9. Could not verify / blocked

- **Wiki page "National focus modding".**
  - The direct fetch of https://hoi4.paradoxwikis.com/National_focus_modding timed out on a permission request.
  - The variant reached through search (`index.php?section=29&title=National_focus_modding&veaction=edit`) loaded, but the text is cut off at about 100k characters, before the "Shared focuses", "Joint focuses" and "Continuous focuses" sections.
  - `curl` to hoi4.paradoxwikis.com is blocked by the session's egress proxy (403).
  - The wiki's sections on `joint_trigger` scopes, late joiners and focus-tree limits were therefore not read.
- **Blocked by the provenance rule:** https://forum.paradoxplaza.com/forum/threads/developer-diary-joint-focus-tree.1594536/ and https://github.com/klimPaskov/Agentic-HOI4-Modding/tree/main/.agents/skills/hoi4-focus-trees.
- **Effects page.** https://hoi4.paradoxwikis.com/Commands is too long; the focus and autonomy effect rows were not reachable. The exact semantics of `unlock_national_focus`, `complete_national_focus` and `load_focus_tree … keep_completed` therefore rest on MD usage and inference.
- **Joint focus open points:**
  - the ROOT/FROM scope inside `joint_trigger`;
  - retroactive completion for late joiners;
  - members whose tree lacks the joint focus;
  - mixing plain shared and joint focuses in one prerequisite chain;
  - `uncomplete_national_focus` on joint focuses;
  - the unit of `reduce_focus_completion_cost`'s `cost`.
- **Saadabad attachment.** That the branch is attached through `shared_focus` in all four trees is an inference. The vanilla file was not read.
- **Götterdämmerung patch number.** "1.15" is inferred from the release order.

## 10. Sources

**Paradox and developer diaries**
- https://forum.paradoxplaza.com/forum/developer-diary/developer-diary-modding.1598797/ (modding DD, 2023-09-13)
- https://store.steampowered.com/news/posts/?feed=steam_community_announcements&appids=394360&enddate=1695130519
- https://store.steampowered.com/news/app/394360/view/5925098517647303884 (Joint Focus Tree DD, 2023-07-26)
- https://devtrackers.gg/heartsofiron/p/83a8023c-developer-diary-joint-focus-tree
- https://admin-forum.paradoxplaza.com/forum/developer-diary/developer-diary-joint-focus-tree.1594536/page-2 (developer replies)
- https://admin-forum.paradoxplaza.com/forum/developer-diary/developer-diary-joint-focus-tree.1594536/page-3
- https://staging2.eip.gg/hoi4/news/patch-1-13-dev-diary-joint-focus-tree
- https://admin-forum.paradoxplaza.com/forum/developer-diary/developer-diary-congo.1712644
- https://devtrackers.gg/heartsofiron/p/233414a2-developer-diary-congo
- https://devtrackers.gg/heartsofiron/p/59f3158e-developer-diary-historical-iran
- https://admin-forum.paradoxplaza.com/forum/developer-diary/developer-diary-performance-modding.1713814
- https://admin-forum.paradoxplaza.com/forum/developer-diary/hoi4-dev-diary-1-5-2-update-2-and-modding-goodies.1084627/post-24020177 (scripted GUIs can attach to the focus tree)
- https://steamcommunity.com/app/394360/eventcomments/3802778195610233442

**Wiki**
- https://hoi4.paradoxwikis.com/index.php?section=29&title=National_focus_modding&veaction=edit (partial)
- https://hoi4.paradoxwikis.com/index.php?title=User%3ABitmode%2FNational_focus_modding
- https://hoi4.paradoxwikis.com/Commands (partial)
- Patches: https://hoi4.paradoxwikis.com/index.php?title=Patch_1.5 · https://hoi4.paradoxwikis.com/Patch_1.13 · https://hoi4.paradoxwikis.com/Patch_1.16 · https://hoi4.paradoxwikis.com/Patch_1.17 · https://hoi4.paradoxwikis.com/Patch_1.18 · https://hoi4.paradoxwikis.com/Patch_1.19
- https://hoi4.paradoxwikis.com/Downloadable_content
- Joint and shared branches: https://hoi4.paradoxwikis.com/Nordic_joint_national_focus_tree_branches · https://hoi4.paradoxwikis.com/Saadabad_Pact_joint_national_focus_tree_branches · https://hoi4.paradoxwikis.com/Austro-Hungarian_joint_national_focus_tree_branches · https://hoi4.paradoxwikis.com/Liangguang_Incident_joint_national_focus_tree_branches · https://hoi4.paradoxwikis.com/Chinese_shared_national_focus_tree_branches · https://hoi4.paradoxwikis.com/Baltic_shared_national_focus_tree_branches · https://hoi4.paradoxwikis.com/Category:National_focus_trees
- Countries: https://hoi4.paradoxwikis.com/Belgian_Congolese_national_focus_tree · https://hoi4.paradoxwikis.com/Belgian_Congo · https://hoi4.paradoxwikis.com/Belgium · https://hoi4.paradoxwikis.com/index.php?mobileaction=toggle_view_desktop&title=British_Raj

**Other**
- https://skillsmp.com/creators/klimpaskov/agentic-hoi4-modding/agents-skills-hoi4-focus-trees (design advice: "If every country using a shared tree reads and plays the same, the tree has failed.")

**Local evidence** (`/mnt/user-data/uploads/mdcoldwar/`)
- National focus files: `common/national_focus/{03_china_russia_joint,03_benelux_shared,03_joint_korea_confederation,06_MERCOSUR_shared,06_AfricanUnion_shared,Commonwealth_shared,01_EU_USoE_shared,00_generic,05_russia,05_centralasia,00_titlebar_styles}.txt`
- Other script: `common/scripted_effects/{00_focus_utilities,99_Commonwealth_scripted_effects}.txt`, `common/autonomous_states/99_1985_soviet_republic_autonomies.txt`, `history/countries/SOV - Russia.txt`
- Vanilla docs: `common/focus_inlay_windows/documentation.md`, `common/factions/_documentation.md`, `common/on_actions/_documentation.md`
- SOV generator output: `/home/claude/sovgen/out/common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt`
