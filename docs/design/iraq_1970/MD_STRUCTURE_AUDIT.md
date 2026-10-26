# COLDWAR IRQ 1970 — current MD structure, geometry and reward audit

Read-only reference audit, 18 October 2026. This report and an audit contact sheet are design artifacts. No loaded focus, history, idea, localisation, GUI, GFX, event or scripted-effect file was changed, and no project generator was run. The Iraq concept remains subject to the owner's approval.

## Sources and audit boundary

`MD` below means `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`; `GAME` means `E:/SteamLibrary/steamapps/common/Hearts of Iron IV`; `CW` means `C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar`.

`MD/descriptor.mod:1` declares version **2.0.2**; line 13 declares HOI4 **1.19.***. Read the current files, rather than the older Soviet audit PNGs, to measure the reference. There is no AGENTS.md in the target checkout. Applied the `mdcw-national-trees` and `mdcw-tree-layout` skills and their project-contract, source-map, soviet-patterns and layout-method references. The national-tree skill separates party eligibility from outlook eligibility and preserves the design approval boundary.

SHA-256 fingerprints of the inspected source snapshot:

| Relative MD file | SHA-256 |
|---|---|
| `common/national_focus/00_generic.txt` | `C3F2E55DF976B712E423FA906AFD18B9E638C838D1CB34A13FB80BFA2EA82AC5` |
| `common/national_focus/05_russia.txt` | `DB03D72E1FDBC239076EBA9F7E9259E1791E909EAB425186304CD6B14858B602` |
| `common/national_focus/05_iraq.txt` | `A4990FE134901BCCF4041BFC10E2183CDDF8BB516E532EC5BB75B45E2396D8D2` |
| `common/national_focus/05_germany.txt` | `9D7D1D21EC5C29149481BD481E7A3063668DB5EFF1F1A6B4841E73768B9D11BF` |
| `interface/nationalfocusview.gui` | `21CA95612E3F51FA369ADAA09A4A1C56DBD4A6C43E41144BDB7DE3C6BCF9A5DE` |

The CW copy of `interface/nationalfocusview.gui` has the **same hash** as MD. Its pixel measurements therefore apply directly to the target. This audit parsed every local `focus` block in all four reference trees, recursively resolved relative anchors and measured base coordinates. Imported shared focuses are excluded from the totals below. None of these four files contains a local `offset` block; conditional offsets elsewhere and imported/shared focus footprints remain a separate integration check.

## Measured native geometry

These are node-center grid coordinates, not pixels. Bounds are for all local focuses in the source, including unavailable political alternatives.

| Tree | Local focuses | Relative anchors | Resolved x range | Resolved y range | Adjacent same-row gaps of 2 | Parent→child dy=1 / all drawn local edges |
|---|---:|---:|---|---|---:|---:|
| Generic | 158 | 150 | −13 … 51 | 0 … 10 | 101 | 169 / 189 |
| Russia | 806 | 800 | 0 … 235 | 0 … 26 | 423 | 1100 / 1200 |
| Native Iraq | 321 | 308 | −2 … 109 | 0 … 19 | 170 | 380 / 400 |
| Germany | 588 | 583 | 23 … 209 | 0 … 19 | 293 | 767 / 787 |

Same-row gaps are counted between adjacent sorted nodes on each complete row; they are not all intentional sibling pairs. Drawn edges count every local prerequisite reference, including OR alternatives. Counts do not mean each edge can be active in one political playthrough.

Russia same-row gap frequencies: 2×423, 3×108, 4×68, 5×40, 6×36, 7×26, 8×13, 9×11. Its edge vertical deltas are 1×1100, 2×95, 0×3, 3×2. Its most common absolute horizontal deltas are 1×454, 0×289, 2×201, 3×81. Generic same-row pitch 2 appears 101 times versus pitch 3 on 23 occasions; its edge deltas are dy1×169, dy2×12, dy3×7, dy4×1.

**Transfer to Iraq:** use leaf pitch **2**, normal next row **1**, centered forks and joins, occasional dy2 for a deliberate gap, and short vertical spines between policy choices. The reference supports very broad independent policy sectors, with many short, interconnected programmes. It does not justify stretching every choice to a 6–10-unit gap or putting hundreds of focuses on a single vertical trunk. It also does not make every native MD edge an ideal routing example: rare dy0 and long cross-sector links need individual review.

### Exact generic examples

From `MD/common/national_focus/00_generic.txt`:

| Focus | Source line | Emitted x,y | Anchor | Resolved x,y | Geometry/logic |
|---|---:|---|---|---|---|
| `GENERIC_political_reform` | 55 | −7,0 | none | −7,0 | Section root |
| `GENERIC_cabinet_reform` | 81 | −4,1 | political_reform | −11,1 | Left member of a paired prerequisite |
| `GENERIC_strengthen_government` | 110 | −2,1 | political_reform | −9,1 | Pair pitch 2 |
| `GENERIC_political_games` | 139 | −3,2 | political_reform | −10,2 | Centered AND join of both focuses above |
| `GENERIC_public_service_announcement` | 165 | −4,3 | political_reform | −11,3 | Fan from centered join |
| `GENERIC_the_establishment` | 198 | −2,3 | political_reform | −9,3 | Second member, pitch 2 |
| `GENERIC_the_state` | 223 | −3,4 | political_reform | −10,4 | Another centered AND join |
| `GENERIC_expand_the_secret_service` | 267 | −6,1 | political_reform | −13,1 | Parallel vertical intelligence spine at x−13 |
| `GENERIC_agricultural_district_subsidization` | 2456 | 8,1 | ease_of_business_reforms=(14,0) | 22,1 | Subprogramme root |
| `GENERIC_subsistence_agriculture_investments` | 2497 | 7,2 | ease_of_business_reforms | 21,2 | Mutually exclusive alternative |
| `GENERIC_commercialized_agriculture_investments` | 2564 | 9,2 | ease_of_business_reforms | 23,2 | Reciprocal exclusion; pitch 2 |
| `GENERIC_a_new_breadbasket` | 2636 | 8,4 | ease_of_business_reforms | 22,4 | Centered OR join after the two route follow-ups at y3 |

This yields the reusable native pattern: root at `(0,0)` → mutually exclusive choices at `(−1,1)` and `(1,1)` → optional distinct follow-ups at `(−1,2)` and `(1,2)` → **OR** join at `(0,3)`. The source's `prerequisite` group contains both route IDs in a single block at the join. Using two separate blocks would incorrectly require both mutually exclusive histories.

Some generic outlook focuses use fractional x positions (−6.5, −4.5). A whole-tree integer-only linter would falsely reject valid reference content. For this new concept, integer coordinates at the measured normal pitch are simpler unless a genuine half-column layout benefit is demonstrated.

### Russia's party fans and chapter footprints

`MD/common/national_focus/05_russia.txt:50` places `SOV_reign_of_yeltsin` at `(62,0)`. Its immediate prerequisite children are **not** spaced uniformly: Zyuganov `(10,1)`, liberals `(27,1)`, New Russia `(49,1)`, subjects `(62,1)`, Putin `(75,1)`, Zhirinovsky `(93,1)`, Nazbols `(122,1)`. Their different widths determine the root positions. Source entries: Putin line 109; western path 4224; Zhirinovsky 4837; Nazbols 10442; Zyuganov 12139; New Russia 15748.

The following footprints group each branch by **relative-anchor descendants**, including its root. This is a spatial grouping, not a claim that every node has the same eligibility or prerequisite ancestry.

| Relative-anchor chapter | Root | Focuses | Complete center bounding box |
|---|---|---:|---|
| Zyuganov | 10,1 | 67 | x0…17, y1…16 |
| Western path | 27,1 | 105 | x16…54, y1…15 |
| New Russia | 49,1 | 44 | x36…59, y1…10 |
| Subjects | 62,1 | 8 | x58…67, y1…3 |
| Putin | 75,1 | 110 | x63…86, y1…26 |
| Zhirinovsky | 93,1 | 117 | x83…119, y1…14 |
| Nazbols | 122,1 | 29 | x119…129, y1…12 |
| Common economy | 152,0 | 129 | x131…189, y0…8 |
| Grozny/army | 194,0 | 86 | x183…203, y0…18 |

The rectangular boxes overlap because rows interlock; a box overlap alone is not a collision. Check full cards by row before declaring a defect. Conversely, checking only root distance would miss the Western path's expansion or Putin's deep continuation. Russia has tucked roots without drawn prerequisites, e.g. `SOV_oligarchs_democracy=(72,9)`, `SOV_usr=(59,7)`, `SOV_referendum_start=(53,7)`, `SOV_western_russia=(63,18)`. Eligibility and stable relative anchoring provide these subordinate sections; the absence of a drawn parent is deliberate, not proof that the section is freely available.

The Putin opening at lines 109–257 uses `(75,1)` → grand bargain `(75,2)` → NPP `(73,3)` and Kasyanov `(77,3)`, leaving their subsequent subtree needs sufficient room. The triple economic choice at lines 553–690 resolves to `(74,8)`, `(76,8)`, `(78,8)` for oligarchic republic, combined economic system and state corporatism, using actual mutual exclusions. This is a useful model for three meaningful policy alternatives inside an already eligible party programme.

### Native Iraq and Germany reference profiles

Iraq's current 2000 tree uses separate roots rather than one mandatory political unlock focus. Spatial families: Baath root `(14,0)`, 35 anchor descendants occupying x9…19,y0…9; National Accord `(44,0)`, 22 occupying x39…49,y0…7; Congress `(54,0)`, 22 occupying x51…57,y0…8; Dawa `(62,0)`,20 occupying x59…65,y0…7; ICP `(70,0)`,22 occupying x68…72,y0…9. **These 2000 party labels and leaders are not evidence for their historical appropriateness in January 1970.** Their geometry and gating are the reference.

Germany's institutional root `GER_german_politics` is at `(112,0)` (`05_germany.txt:15158`). Its branches explicitly distinguish governing subparties: SPD Agenda 2010 at offset `(3,1)`, CDU root `(−8,1)` (`15867`), FDP root `(−19,1)` (`16712`). CDU's entry allows western conservatism in power **or coalition**, but later programme focuses normally require the party in power. FDP accepts western liberals or neutral libertarians in government/coalition at entry. This shows an intentional distinction between outlook, subparty and coalition; an Iraq gate must encode the desired political contract explicitly rather than broadening all parties of an outlook to one identical route.

## Native UI: exact pixel geometry and real art

`MD/interface/nationalfocusview.gui:446` (`national_focus_item`):

| Element | Measured declaration |
|---|---|
| Node container | 165×128, clipping=no |
| Native titlebar/background button | position `(5,40)`, sprite `GFX_technology_unavailable_item_bg`; actual focus state style supplies titlebar sprites |
| Focus symbol | position `(5,−44)`, centerposition=yes, Orientation=CENTER |
| English focus title | position `(15,58)`, font `hoi_16mbs`, maxWidth=147, maxHeight=20, centered both ways |
| Highlight/continuous glow | position `(17,−40)` |
| Overlay | position `(−9,−28)` |
| Historical marker | position `(140,71)` |
| Focus spacing | **96×130 pixels per grid unit**, line 574 |
| Declared national focus center | `(130,32)`, line 578 |
| Native connector tile spacing | 16×16, line 582 |
| Connector offsets | `(0,32)`, line 586 |
| Connector begin/end | `(80,64)` / `(80,0)`, lines 590,594 |
| Exclusion offsets | `(172,24)` / `(12,24)`, lines 598,602 |
| Exclusion positioning | `(2,0)`, line 606 |

Thus normal same-row pitch2 means **192px**, with a native **164px titlebar**; one-row steps mean **130px**. Preview conversion should use exactly these scales, not research-GUI card sizes. The symbol's origin is engine-relative; use a faithful approximation and disclose it rather than claiming an engine screenshot. Many real focus DDS textures are 90–110px across; scaling every icon to 160px would change MD's visual grammar and cause collisions. A single title line has only 147px: keep English focus names short, or use a verified native wrapping solution. A readable long label in a browser rectangle does not prove it fits the game.

Default style: `MD/common/national_focus/00_titlebar_styles.txt:1` uses unavailable=`GFX_focus_unavailable`, completed=`GFX_focus_completed`, available=`GFX_focus_can_start`, current=`GFX_focus_current`. Their registrations are in `MD/interface/nationalfocusview.gfx:132,136,153,188`. Textures are **inherited from the base game**, not present at the same paths in MD:

* `GAME/gfx/interface/focusview/titlebar/focus_unavailable_bg.dds` — 164×50.
* `GAME/gfx/interface/focusview/titlebar/focus_can_start_bg.dds` — 164×50; also current-state animation base.
* `GAME/gfx/interface/focusview/titlebar/focus_completed_bg.dds` — 164×50.

Native animated glow/shining, connector frames and unavailable/available/completed/current treatment are distinct from a plain static exported approximation. No global GUI/font/art changes are justified for this design.

### Verified sprite candidates and visual exclusions

The focus files use **bare sprite names**, e.g. `icon = baathist_iraq`; blindly adding `GFX_` would reference a different/missing sprite. All registrations below exist in `MD/interface/goals.gfx`, and the DDS files were opened with Pillow to check dimensions. A contact sheet of 24 assets was visually inspected at `C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82/COLDWAR_IRQ_md_icon_audit.png`.

Texture column is relative to `MD/gfx/interface/goals/`.

| Bare sprite | goals.gfx line | Texture | Pixels | Use/visual finding |
|---|---:|---|---|---|
| `baathist_iraq` | 24379 | `iraq/baathist_iraq.dds` | 94×84 | Abstract Iraqi map/eagle; suitable Baath/institutional candidate |
| `IRQ_iraq_communism` | 24703 | `iraq/IRQ_iraq_communism.dds` | 90×90 | Party hammer/sickle emblem; communist family candidate |
| `IRQ_dawa_party` | 24699 | `iraq/IRQ_dawa_party.dds` | 90×90 | Party logo; historical logo chronology still needs source check |
| `tuwaitha_reconstruct` | 24803 | `iraq/tuwaitha_reconstruct.dds` | 91×70 | Building/tools, no visibly modern national flag; suitable science/construction candidate |
| `niniweh` | 24731 | `iraq/niniweh.dds` | 94×99 | Ancient winged symbol; heritage candidate |
| `saddamsreign` | 24763 | `iraq/saddamsreign.dds` | 90×90 | Saddam portrait; use only for an appropriate Saddam programme, not generic 1970 government |
| `Election_graphics` | 8697 | `00_politics/Election_graphics.dds` | 94×80 | Neutral electoral/institutional art |
| `government_beu` | 9133 | `00_politics/government_beu.dds` | 85×85 | Neutral administration |
| `self_management` | 9353 | `00_politics/self_management.dds` | 100×88 | Neutral assembly/institution |
| `propaganda` | 9321 | `00_politics/propaganda.dds` | 94×81 | Native propaganda candidate; inspect final use |
| `Generic_State_Socialism` | 5897 | `00_economy/Generic_State_Socialism.dds` | 94×77 | Industrial/state-economy art |
| `decentralized_economy` | 5441 | `00_economy/decentralized_economy.dds` | 99×87 | Domestic economic organisation |
| `balance_buget` | 4721 | `00_economy/balance_buget.dds` | 89×78 | Actual native typo in sprite name; budget/scales |
| `economic_water_supply` | 5561 | `00_economy/economic_water_supply.dds` | 100×88 | Water/irrigation infrastructure |
| `oil_production2` | 6433 | `00_energy_resources/oil_production2.dds` | 94×77 | Neutral oil installation, preferable to modern flag assets |
| `welfare` | 9429 | `00_politics/welfare.dds` | 96×86 | Neutral social services |
| `generic_hospital` | 5857 | `00_economy/generic_hospital.dds` | 90×79 | Health programme |
| `focus_generic_university_3` | 10617 | `00_science/focus_generic_university_3.dds` | 100×88 | University/science; inspect final asset visually |
| `focus_generic_agricultural_subsidies` | 5653 | `00_economy/focus_generic_agricultural_subsidies.dds` | 100×88 | Agriculture; inspect final asset visually |
| `soldiers` | 2545 | `00_army/soldiers/soldiers.dds` | 90×87 | Neutral armed-forces candidate |
| `shia_politics` | 10477 | `00_religion/shia_politics.dds` | 99×87 | Shia religious/institutional candidate, relevant to Iraq; not a generic Muslim-country template |

**Do not auto-reuse these simply because their filenames say Iraq:** `Iraqi_Army_1`, `iraqi_farmer`, `iraq_farming_incentive`, `increase_oil_prod`, `start_nuke_prog`, `iraq_states_hand`, `at_crossroads_iraq`. Their visible flags have the three stars **and Arabic script**, so they do not depict the unlettered 1970 flag. The precise revision date belongs in the history report; the visual exclusion already stands. `iraqi_protest` looks like modern protest art and needs a provenance check. These are asset-content problems, not missing-file problems.

## Prerequisites, party gates and temporary programmes

Whole-file counts show the actual native grammar:

| Tree | Focuses with available | Focuses with allow_branch | Focuses with exclusions | OR prerequisite groups |
|---|---:|---:|---:|---:|
| Generic | 74 | 2 | 29 | 14 |
| Russia | 724 | 2 | 85 | 100 |
| Native Iraq | 286 | 1 | 31 | 11 |
| Germany | 346 | 1 | 58 | 51 |

`available` is the usual party programme gate. It controls eligibility; it is **not** a declaration to hide the entire branch and does **not** remove a completed focus's spirit. `allow_branch` is rare here and used for special situations/game rules: Iraq's missile focus checks the nuclear-weapons rule; Germany's Austrian invasion excludes the monarchist programme. No freely invented `visible` field from decision syntax should be put into focus blocks. A requirement that whole branches disappear and return needs separate engine validation; the design can honestly show locked/grey political routes with reliably detached/reattached programme spirits.

Separate prerequisite blocks mean **AND**; multiple focus entries inside one block mean **OR**. `relative_position_id` is a geometric anchor and need not be a prerequisite. `mutually_exclusive` should encode real choices with reciprocal references; it does not authorize drawing losing cards at identical positions.

Native 2000 Iraq's exact programme predicates:

| Entry focus | File line | Availability predicate |
|---|---:|---|
| `IRQ_the_baathist_party` | 3371 | `nationalist_fascist_are_in_power = yes` |
| `IRQ_the_national_accord` | 6585 | `western_liberals_are_in_power = yes` plus completed occupation-era order |
| `IRQ_national_congress` | 7414 | `western_social_democrats_are_in_power = yes` |
| `IRQ_al_dawa` | 8237 | `emerging_reactionaries_are_in_power = yes` |
| `IRQ_communist_party_of_iraq` | 9007 | `neutrality_neutral_communism_are_in_power = yes` |

These predicates prove which MD slots the reference currently uses. They do not establish a new 1970 party's assignment, and native 2000 prerequisite events should not be copied into 1970. Existing CW political content must decide the exact historical mapping. An outlook-strengthening programme can coexist with party programmes, but should not be a redundant required unlock of a party that already governs.

### Direct MD precedent for removing and restoring political spirits

This request has an exact provider in current MD: `MD/common/scripted_effects/99_SOV_scripted_effects.txt:10968`, **`SOV_update_political_modifiers`**. Its comment explicitly says backing variables survive detachment so accumulated bonuses return if the ideology returns.

The effect:

1. Removes attached political dynamic modifiers only when `has_dynamic_modifier` confirms they exist.
2. Reattaches completed and currently eligible programmes. For example, completed `SOV_zyuganov` plus `emerging_communist_state_are_in_power` OR `neutrality_neutral_communism_are_in_power` restores `SOV_revived_politburo_modifier`.
3. Preserves national backing variables. It does not replay focus completion, factories, money, equipment, research grants or foreign annexations.
4. Includes special route flags/exclusions (e.g. Putin's later replacement programmes). A programme is not always equivalent to a single party test.

Provider/consumer proof: `MD/common/dynamic_modifiers/99_SOV_dynamic_modifiers.txt:4` maps Politburo variables to `research_speed_factor`, `production_speed_buildings_factor`, `office_park_income_tax_modifier`, etc.; line145 maps `SOV_putin_politic_modifier` variables to actual PP, stability and drift modifiers. `05_russia.txt:12139` awards the Politburo variables and attaches the modifier at the Zyuganov focus. Native aggregate update calls preserve those values while changing attachment.

**Both update routes matter.** `MD/common/on_actions/00_on_actions.txt:1964` starts `on_government_change`; line1981 calls `SOV_government_change`. The latter is defined in `99_SOV_scripted_effects.txt:10915` and calls the political refresh near10961. `MD/common/scripted_effects/00_MD_politicsview_scripted_effects.txt:1979` defines `change_ruling_party_effect`, which calls `SOV_update_political_modifiers` at2050, after `set_leader`. Its comment explicitly notes **subideology swaps keep the same ideology group, so on_government_change cannot carry these**. Iraq implementation must integrate with both existing outlook and subparty changes, plus relevant leader changes and a guarded load/initialisation refresh. Merely attaching an idea to a focus and relying on outlook on_actions would leave stale party programmes.

For the concept, classify each reward as: permanent national development; one-time grant; timed burden; government-bound programme; or leader-bound programme. Only the latter two suspend on government/leader loss. Persist earned values for later restoration. Do not classify an already built refinery as removable party property or replay its construction when the party returns.

## Costs, rewards and supported effect shapes

`GAME/common/defines/00_defines.lua:3599` sets `FOCUS_POINT_DAYS = 7` (one point=one week). No override for this define was found in MD. Therefore cost3=21 nominal days,5=35,7=49,10=70. Decimal cost7.19 gives **50.33 nominal days**,8.6=60.2,7.86=55.02,4.3=30.1. Exact integer-day UI/engine rounding was not tested; do not label cost7.19 as exactly 50 or70 without that qualification. Prefer explicit, readable integer cost tiers for new design unless matching a tested native duration convention matters.

Reference cost frequencies:

* Generic: cost10=103;7.86=29;8.6=10;5=9;6.8=3;7.1=2;7.2=1;2=1.
* Russia: cost3=314;5=216;7=168;2=76;1=17;4=8;6=6;10=1.
* Iraq: cost7.19=93;10=61;5.72=54;5=43;8.6=29;3=12;8.70=11;8.60=7;2=6;8.80=2;7=2;7.20=1.
* Germany uses varied shorter tiers, notably4.3=152,6.5=119,6=107. The reference does **not** establish a universal70-day rule.

The reference's normal block order is `id`, `icon`, x/y/relative anchor, `cost`, grouped prerequisites/exclusions, `search_filters`, `available`/`bypass` where relevant, `completion_reward`, `ai_will_do`. Completion rewards generally start with a searchable `log = "[GetDateText]: [Root.GetName]: Focus ..."`. Reuse appropriate filters, normal native tooltips, MD scripted economic helpers and scope discipline. Comments aid maintainers; they do not create in-game section bands.

### Concrete reward bundles, including real costs

| Reference | Executed shape | Design lesson |
|---|---|---|
| Generic heavy industry, `00_generic.txt:2866` | treasury−7.5 through `modify_treasury_effect`; capital gains shared slot and instant arms_factory1; extra factory helpers scale with existing factories; defence-industry opinion+5; GDP/no-war gate | Buildings and their economic payment belong together; tier size must suit Iraq, not Russia |
| Agriculture subsidy, `00_generic.txt:2456` | `one_random_agriculture_district`; agricultural investment idea; farmer opinion+10,landowner+5 | Native building helper is a real sector building, not an arbitrary PP proxy |
| Subsistence route, `2497` and follow-up2531 | farmer opinion; swap agricultural investment spirit to its improved version | Persistent policy identity with a distinct continuation |
| Commercial route, `2564` and follow-up `2603` (`GENERIC_encourage_more_commercial_agriculture`) | `two_random_agriculture_district`; farmer opinion; later distinct commercial investment spirit | Distinct construction/organisation alternative; do not pretend both routes are stackable |
| Breadbasket OR join, `2636` | farmer opinion+5; `skip_payment=1`; one random agriculture district | Deliberate free closing reward explicitly suppresses the helper's normal cost |
| Russia oligarch return, `05_russia.txt:883` (`SOV_move_oligarchic_entites_back_to_russia`) | treasury+60; political dynamic modifier corruption-cost+0.07 and office-income+0.05 | Native gain plus institutional downside; source values are a superpower benchmark, not Iraq's budget |
| Russia natural wealth, `05_russia.txt:918` | treasury−7.50; state683 oil+8; oligarch resource-factor+0.07 and drift+0.03 | State resource gain needs **Iraqi state scope**, ownership/control and real budget |
| Zyuganov entry, `05_russia.txt:12139` | party event; current-party setup; programme drift+0.05,drift-defence+0.10; attach mapped dynamic modifier | Programme accumulation and active-party attachment are separate operations |
| Mechanized renovations, `05_russia.txt:23030` | faction opinion; 2-use0.35 research bonuses in exact armored categories | Research rewards use actual MD categories and finite uses; names alone are insufficient |
| Native Baath army recovery, `05_iraq.txt:3396` | military opinion+10; army XP25; command power25; `increase_military_spending` | Military modernisation can increase ongoing expenditure rather than granting only combat buffs |

Source line numbers are snapshot pointers, not permanent IDs.

Helper consumers were checked, not just their names:

* `MD/common/scripted_effects/00_scripted_effects.txt:4`, `one_random_arms_factory`, selects one controlled state with a free shared slot, adds a slot and instant arms factory, then charges treasury7.5 unless `skip_payment=1`.
* `00_scripted_effects.txt:2070`, `one_random_agriculture_district`, similarly adds one `agriculture_district` and charges treasury3.75 unless skipped. `two_random_agriculture_district` at2126 selects two states and charges7.5.
* Their charge is outside the state-selection loop. With no valid state, they can charge despite no construction; a new focus should establish a valid target/slot or use an explicitly checked scoped construction contract.
* `MD/common/scripted_effects/00_budget_effects.txt:1487`, `modify_treasury_effect`, adds `treasury_change` to `treasury`, updates money-dirty state, and honours the explicit start/setup `MD_skip_treasury_cost` flag.
* `00_budget_effects.txt:1499`, `modify_debt_effect`, adds `debt_change`, clamps debt to minimum0 and updates the money-dirty state.
* Adding a second explicit payment before a helper that already charges would double-charge. If making a district grant free, show that intentionally and suppress the helper charge correctly. Do not rely on inherited temporary variable values.

Actual supported programme downside families visible in `99_SOV_dynamic_modifiers.txt` include education/health/bureaucracy/personnel/police cost multipliers, corruption cost, consumer-goods/tax costs, investment conditions, drift, construction, productivity and tax-income modifiers. They are preferable to inventing unconsumed `kurdish_loyalty` or `oil_dependency` modifiers. For custom historical concepts, use real modifiers **and** the actual project state variables/decisions that consume them, with a truthful tooltip. The mechanics agent must still verify every final concept effect and amount, especially all Imperia-only consumers and percentage units.

## Camera and navigation

Generic (`00_generic.txt:1–50`) has continuous panel pixel position `(5,830)` and four shortcuts to politics,diplomacy,ease-of-business and army with `scroll_wheel_factor=0.80`; imports shared regional/EU/custom trees. Russia (`05_russia.txt:11–46`) has continuous panel `(17000,1000)`, initial_show_position grid `(2,0)` and six shortcuts to army,economy,Zhirinovsky,Putin,Zyuganov,liberals, each0.80. Its actual Yeltsin root is atx62, so blindly copying its initial-show coordinates would not center the new starting government. Native Iraq has panel `(0,2500)`, initial `(0,0)`; Germany has panel `(5300,3040)`, initial `(100,0)` and five shortcuts.

The continuous panel is **770×380px**, declared in `nationalfocusview.gui:175`; the focus entries inside it use an independent grid (`180×120px` slots). A raw focus x-coordinate is not a panel pixel coordinate. Place it in a verified free pocket beyond the full subtree footprint, and include shared focuses in the final integration preview. A large Iraq concept benefits from shortcuts to actual political,leadership,economic,military and diplomatic roots. Shortcuts should target real displayed nodes. Do not reproduce Russia's canvas size or shortcut count as a quota.

## Independent concept review acceptance record

For the proposed concept before approval, verify:

1. Every manifest ID resolves once; all have `COLDWAR_IRQ_` namespace, short English title, sprite, chapter/root, emitted offsets and resolved coordinates, grouped prerequisites, exclusions, party/leader availability, cost, exact effects, and reward ownership.
2. Pair choices are native pitch2, normal rowsdy1, centered OR/AND joins use the intended logic, and their full descendants stay in reserved row space. No AND join requires mutually exclusive histories.
3. Show all simultaneously visible political alternatives in a complete overview and a normal-scale start/party detail view. Toggled party/leader views must use the same coordinates as the manifest.
4. Show real native titlebars and sprites at measured size. Flag approximated font, connector routing and glows honestly. Check every English label fits the native147×20 text area; do not make fonts globally smaller.
5. Check unavailable neighbouring cards, icon protrusions, horizontal bar crossings, long cross-chapter edges, clipping and panel occupancy, not only center-to-center distances.
6. A current party unlocks its own programme directly. Optional outlook-building branches serve an actual political purpose; they are not mandatory ceremony.
7. Government/leader-bound programmes detach and restore persistent accumulated values. Permanent infrastructure stays; money/building/equipment grants execute once. Concept should name same-outlook subparty refresh and leader refresh requirements explicitly.
8. Historical route eligibility in January1970 and alternative leaders/parties comes from the separate history report and existing CW systems. Do not import 2000 Iraqi occupation/ISIS/Sadrist content just because it has code or art.
9. Native source patterns establish API existence and presentation, not final balance. Each final reward still needs its provider→consumer proof and country budget review.

Not performed: HOI4 launch/hover test, engine connector routing, dynamic branch hide/return tests, exact decimal-cost rounding, multiplayer/saveload transitions, or complete final-concept mechanics review. No claim of 1:1 engine reproduction or full implementation correctness is made by this static reference audit.

## Reusable read-only parsing method

The measurements used a brace/quote/comment-aware token parser rather than matching nested focus bodies with one regex. Existing `CW/tools/israel_1970/validate_layout.py` and `CW/tools/greece_1970/layout.py` are useful integration references but have country-specific thresholds and may have side effects; no generator/validator was run for this audit. The following compact independent method preserves repeated prerequisite blocks and detects missing/cyclic relative anchors. It is a structural subset, not a complete HOI4 scripting validator; evaluate conditional offsets/shared roots separately when present.

```python
import re

def parse(text):
    # Quotes are a single token, so braces and '#' inside strings are harmless.
    tokens = [m.group() for m in re.finditer(
        r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}=]|[^\s{}=#]+', text)
        if not m.group().startswith('#')]

    def block(i, nested=False):
        out = []
        while i < len(tokens) and tokens[i] != '}':
            key = tokens[i]; i += 1
            value = None
            if i < len(tokens) and tokens[i] == '=':
                i += 1
                if i >= len(tokens):
                    raise ValueError('missing value for ' + key)
                if tokens[i] == '{':
                    value, i = block(i + 1, True)
                else:
                    value = tokens[i]; i += 1
            out.append((key, value))
        if nested:
            if i >= len(tokens):
                raise ValueError('unclosed block')
            return out, i + 1
        if i != len(tokens):
            raise ValueError('unmatched closing brace')
        return out, i
    return block(0)[0]

def values(node, key):
    return [value for name, value in node if name == key]

def first(node, key, default=None):
    return next(iter(values(node, key)), default)

def resolve_tree(ast):
    tree = first(ast, 'focus_tree')
    focuses = values(tree, 'focus')
    by_id = {}
    for focus in focuses:
        focus_id = first(focus, 'id')
        if not focus_id or focus_id in by_id:
            raise ValueError('missing/duplicate focus ID: ' + str(focus_id))
        by_id[focus_id] = focus
    coordinates, active = {}, set()

    def xy(focus_id):
        if focus_id in coordinates:
            return coordinates[focus_id]
        if focus_id in active:
            raise ValueError('cyclic relative anchor: ' + focus_id)
        if focus_id not in by_id:
            raise ValueError('missing relative anchor: ' + focus_id)
        active.add(focus_id)
        focus = by_id[focus_id]
        x, y = float(first(focus, 'x', 0)), float(first(focus, 'y', 0))
        anchor = first(focus, 'relative_position_id')
        if anchor:
            ax, ay = xy(anchor); x += ax; y += ay
        active.remove(focus_id)
        coordinates[focus_id] = x, y
        return x, y

    for focus_id in by_id:
        xy(focus_id)
    prerequisites = {
        focus_id: [values(group, 'focus')
                   for group in values(focus, 'prerequisite')]
        for focus_id, focus in by_id.items()
    }
    return by_id, coordinates, prerequisites
```

Read with UTF-8-sig to accept BOMs. Additional shared focuses must be collected from their providers before resolving cross-file anchors. Preserve prerequisite list-of-lists in the concept and preview; flattening it destroys AND/OR semantics. For conditional offset states, add only offsets whose triggers hold in the displayed state and compare each state separately.
