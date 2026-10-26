# Native MD reference: South Korea tree layout and syntax

Read-only reference for a proposed January 1970 South Korean national focus concept. No donor or loaded mod files were changed.

## Source and limits

- Donor: Steam Workshop `2777392649`, `descriptor.mod` identifies **Millennium Dawn 2.0.2** and `supported_version = "1.19.*"`.
- Primary files: `common/national_focus/05_south_korea.txt` (219 focus blocks), `05_russia.txt` (806), `00_generic.txt` (158), `interface/nationalfocusview.gui`, `interface/nationalfocusview.gfx`, `common/national_focus/00_titlebar_styles.txt`.
- Target checkout at research time: `C:\Users\sonyz\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar-main`.
- The donor South Korea tree header itself says last modified 14/02/2022. Its content is a modern-era tree (F-35, Korean space programme, smartphones, and engagement with modern India). Treat it as **syntax and rendering grammar**, not a 1970 historical or reward blueprint. Shared Korea unification files were out of scope for this reference.
- Coordinates below are HOI4 focus-grid values. A relative child resolves to `anchor absolute + child x/y`; prerequisite wiring is separate. I measured source coordinate declarations and manually resolved the representative anchors below; this is not a rendered engine preview.

## Tree grammar and measured geometry

All three trees declare ordinary `focus_tree`, focus blocks, named icon sprites, numeric costs, grouped prerequisites, availability, mutually exclusive choices, reward blocks, and AI weights. South Korea uses `original_tag = KOR` behind a `factor = 0` tree country weight, with `add = 20` (05_south_korea.txt:3-15). Focuses usually set `search_filters`, `completion_reward`, and `ai_will_do`; `relative_position_id` appears on most child blocks.

| Example | Declaration and resolved grid position | Evidence |
|---|---|---|
| KOR military root | `KOR_the_rok_armed_forces` at `(0,0)` | 05_south_korea.txt:19-38 |
| KOR political root | `KOR_state_of_the_republic` at `(27,0)` | 05_south_korea.txt:1541-58 |
| KOR diplomacy root | `KOR_middle_power_diplomacy` at `(61,0)` | 05_south_korea.txt:4972-89 |
| KOR procurement | relative `(-9,+1)` from military root; absolute `(-9,1)` | 05_south_korea.txt:40-58 |
| KOR aircraft fork and join | `KOR_p8_poseidon` `(-10,+2)` and `KOR_c295` `(-8,+2)` relative to military root; `KOR_upgrade_f16s` `(-9,+3)` | 05_south_korea.txt:68-80, 140-52, 200-12 |
| KOR political outlook split | left and right focus cards are `(-4,+1)` and `(+4,+1)` from political root; absolute `(23,1)` and `(31,1)` | 05_south_korea.txt:1560-79, 3533-59 |
| SOV entry / Putin root | `SOV_reign_of_yeltsin` `(62,0)`; Putin relative `(+13,+1)` => `(75,1)` | 05_russia.txt:51-79, 107-53 |
| SOV economic outcomes | three alternatives anchored to Putin at `(-1,+7)`, `(+1,+7)`, `(+3,+7)` => `(74,8)`, `(76,8)`, `(78,8)` | 05_russia.txt:552-98, 600-47, 649-94 |
| Generic political root / children | root `GENERIC_political_reform` `(-7,0)`; children use relative `(-4,+1)` / `(-2,+1)` => `(-11,1)` / `(-9,1)` | 00_generic.txt:54-78, 80-107, 109-36 |

Spacing patterns measured in these examples:

- South Korea typically puts sibling rows one grid unit lower (`y +1`) and uses a two-unit horizontal spread for a two-way fork. The join is centered one row lower, with one OR prerequisite block listing both alternatives (KOR aircraft example, lines above). Other branches are straight, narrow spines: the navy line runs from root-relative `(-5,1)` then `(-6,2..5)`, while a parallel root-relative line continues at `(-2,2..5)` (05_south_korea.txt:302-83, 642-91). This creates several parallel bands without chaining every coordinate to the previous focus.
- South Korea places major sections far apart on explicit independent roots at x=0, 27, and 61; this is specific to its *very large* 219-focus tree, not a spacing quota for a compact 1970 tree. Political root `(27,0)` is a deliberate section root and all its branches use that anchor (e.g. lines 1560-79 and 3533-59). Diplomacy is separately rooted at `(61,0)` and its many modern programme branches span around it (lines 4972-4990 onward).
- Russia demonstrates a large opening root with sibling branches and a deeply placed, explicit multi-outcome economic row; the row's three mutually exclusive endings each require both of the same two prior focuses through two separate prerequisite blocks (AND), then use separate political viability checks. Do not flatten the two AND groups into an OR when designing a join (05_russia.txt:552-76, 600-27, 649-78).
- Generic uses the same relative-anchor pattern, but with tighter single-purpose clusters. Its `focus_tree` also provides several `shortcut` entries for major sections (00_generic.txt:1-52); Russia sets `initial_show_position = { x = 2 y = 0 }` and five shortcuts (05_russia.txt:11-49). South Korea sets `continuous_focus_position = { x = 0 y = 1000 }`; Generic uses `(5,830)` (05_south_korea.txt:16; 00_generic.txt:4). The large y values are reserved panel placement, not ordinary tree scale.

### Grid and art footprint

`nationalfocusview.gui` puts the focus tree in a scrollable `tree` container (lines 109-115), then places a `grid_window` with a 1x1 background `gridboxtype` (lines 133-140). Crucially, the same GUI declares the actual focus item and spacing: `national_focus_item` is 165x128 px (lines 446-449); its background is placed at (5,40), the symbol at (5,-44), and its name field at (15,58), with `hoi_16mbs` and max text bounds 147x20 (lines 463-493). `focus_spacing` is 96x130 px, with `national_focus_center` at (130,32) and link spacing 16x16 (lines 573-585). On this source geometry, one horizontal focus grid unit is 96 px (a single-column difference is narrower than the 165 px item width); the measured two-column fork separation gives 192 px between corresponding positions, about 27 px more than the item width. One vertical grid unit is 130 px against a 128 px item height. These values explain why deliberate horizontal fan spacing matters. They are authored GUI values, while final connector routing and icon artwork extents still merit a rendered preview/in-game check. The same file has separate 38x30 progress-grid cells and other unrelated controls (lines 208-253); don't confuse those with the focus item.

GFX registers native connector sprites and shared unavailable/available/completed/current titlebar sprites (nationalfocusview.gfx:42-112, 131-207). `00_titlebar_styles.txt:1-8` maps `default_style` to those four states. South Korea focuses declare named MD icon sprites via `icon = ...` (e.g. `rok_armed_forces`, `united_states_dollar`, `modern_bomber`, `navy`; 05_south_korea.txt:19-22, 40-43, 68-71, 302-05). The target workspace's `interface/nationalfocusview.gui` and `.gfx` match the donor counterparts (SHA-256 matches for both files), so the measured GUI geometry applies directly to the target checkout at research time.

## Choice and party-gate patterns

- KOR procurement is a clear two-card mutually exclusive equipment choice: both alternatives have one prerequisite on `KOR_foreign_procurement`, have reciprocal `mutually_exclusive` declarations, and require political/industrial availability checks inside each focus (05_south_korea.txt:68-95 and 140-72). The sequel `KOR_upgrade_f16s` uses one prerequisite block with both focus fields, meaning **either** aircraft option unlocks it (lines 200-12). Preserve this distinction: repeated `prerequisite` blocks are AND; repeated `focus =` entries in one block are OR.
- KOR political branches use actual government triggers under `available`, not solely the drawing connector: the left entry accepts progressive or liberal government (05_south_korea.txt:1560-88); the right accepts conservative or western liberal at entry, then narrows certain downstream focuses to conservative (3533-60, 3562-80). The 1970 concept must use the project's current MD subparty/outlook checks and historical starting government, not copy these 2020-era trigger names.
- Russia's Putin focus shows a native political eligibility gate (`emerging_reactionaries_are_in_power = yes`) while retaining the drawn predecessor connector, then changes government and applies its actual economic/political outcomes (05_russia.txt:107-53). Its later choices also gate on event-derived economic verdict variables and required policy milestones (552-76, 600-27, 649-78). This is a useful example of keeping substantive party/policy checks distinct from connector-only prerequisites.
- Native focus costs in these samples range from 1/2 at Russia's entry chain and 5 for policy outcomes, through 8/10 in South Korea's equipment branches and 8.6/10 in Generic. These are literal `cost` values from the donor, not proposed KOR1970 prices.

## Reward shape examples and execution trace

| Function | Native example | What the source actually grants | Trace / caveat |
|---|---|---|---|
| Military entry / capability | `KOR_the_rok_armed_forces` | +25 army, navy, and air experience; cost 8 | Direct one-time effects (05_south_korea.txt:19-38). The focus can bundle programme-wide military readiness across three services. |
| Paid capital project | `KOR_jeju_complex` | treasury change `-2`; instant level-2 naval base in state 608 / province 1177; cost 5 | Effect directly calls `modify_treasury_effect` then construction (05_south_korea.txt:483-518). Shared provider in `common/scripted_effects/00_budget_effects.txt:1484-94` adds `treasury_change` to `treasury` and refreshes the money-dirty variable. The coordinates/state IDs are modern donor data and must not be copied blindly. |
| Broader investment project | `KOR_expand_dockyards` | treasury change `-15`; coastal state gets +2 shared slots and two dockyards; cost 10 | A real economy-plus-naval bundle (05_south_korea.txt:520-60), with explicit AI suppression for bankruptcy and inability to staff dockyards (lines 549-58). This is a scale/pattern reference only; benefit and price should be designed for the 1970 balance. |
| Economic institution | `KOR_growth_by_innovation` | grants `KOR_idea_growth_by_innovation` | Focus grant at 05_south_korea.txt:2575-2602. Provider at `common/ideas/Korea.txt:1439-46` gives +5% research speed and +10% building production speed. This is a persistent modifier idea, not an instant abstract “innovation” bonus. |
| Institutional diplomacy | `KOR_middle_power_diplomacy` | grants `KOR_global_korea` | Focus at 05_south_korea.txt:4972-89; idea at `common/ideas/Korea.txt:1018-26` gives +25% trade opinion factor, +0.2 political-power gain, and +0.1 monthly opinion-gain factor. The national idea is the consumer-visible lasting effect. |
| Bilateral diplomacy | `KOR_rapprochement_with_russia` | SOV receives `political_outreach` opinion modifier toward KOR; requires no war and SOV opinion > -1 | Focus availability and reward at 05_south_korea.txt:5013-48. This is a direct country-scope diplomatic action, not a generic relation reward to ROOT. |
| International economic diplomacy | `KOR_national_highways` | deducts 14 treasury; India receives two instant infrastructure levels in states 431 and 432, a trade-mission opinion modifier, and increased KOR influence | Focus at 05_south_korea.txt:7297-48. It combines an own-state expense with a foreign-state benefit. The named `modify_treasury_effect` provider above handles the own deduction. Recheck third-party ownership/consent and state assignment for a 1970 design; donor IDs and modern investment logic are not portable. |

The KOR political/economic reward chain also illustrates idea effects and scripted effects used for systemic reforms: `KOR_income_led_growth` calls `increase_social_spending`, `change_chaebols_opinion`, and `liberal_policy_effect_small` (05_south_korea.txt:2542-73); `KOR_growth_by_innovation` then grants the idea above. For a new concept, every promised policy consequence should be traced to its effect/helper and any idea/modifier consumer, rather than inferred from focus title text.

## Practical design guidance for the KOR1970 concept

1. Use the South Korea tree's native block shape (`id`, `icon`, `x/y` and optional `relative_position_id`, `cost`, grouped `prerequisite`, eligibility, reward, AI weight), but build a much smaller number of clear 1970 programme clusters. Pick stable anchor foci for political, economic, diplomatic, and security sections, then resolve every child to absolute coordinates before review.
2. Keep drawn dependencies and political availability checks separate. Put true alternatives on a deliberate row, reciprocal exclusions on alternatives, and a later join at its own position; only place OR alternatives in one prerequisite block when either is intended to satisfy the gate. Avoid AND joins across mutually exclusive outcomes.
3. Use actual MD native party/outlook conditions as gates and keep the historically available founding/admission route reachable before any organization-member-only branch. Use project-specific triggers rather than the donor's contemporary Korean government helpers.
4. Prefer meaningful outcomes in institutional bundles: military doctrine/equipment/R&D or readiness; state-specific industrial or transport development; national spirits/ideas with concrete modifiers; diplomacy with correctly scoped counterparties. The donor rewards are examples of shape; choose 1970 amounts, costs, provinces, leaders, parties, and historical claims from project systems and evidence.
5. Native custom titlebar style is the default state mapping unless a tree explicitly opts into a shared-focus style. Reuse native `icon =` sprites where their actual imagery suits the policy. The UI definition alone does not establish exact rendered title/card bounds.

## Evidence references

All line references in this report point to the donor root `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2777392649` as inspected on 2026-10-24. Key location list:

- Version: `descriptor.mod:1-17`.
- South Korea full tree, header and entry: `common/national_focus/05_south_korea.txt:3-38`; sections begin around lines 18 (`##MILITARY##`), 1540 (`##POLITICAL##`), 4971 (`##DIPLOMATIC#`).
- Generic tree: `common/national_focus/00_generic.txt:1-52` header/shortcuts; political example at 54-136.
- Russia tree: `common/national_focus/05_russia.txt:1-49` header/navigation; entry and political route at 51-153; economic policy alternatives at 552-694.
- Focus UI and art states: `interface/nationalfocusview.gui:109-140,446-493,573-599`; `interface/nationalfocusview.gfx:42-112,131-207`; `common/national_focus/00_titlebar_styles.txt:1-8`.
- Reward providers: `common/scripted_effects/00_budget_effects.txt:1484-94`; `common/ideas/Korea.txt:1018-26,1439-46`.


