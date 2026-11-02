IMPERIA COLD WAR

# France 1970 asset-reward review

## Scope and evidence

Static review of the current compiled design, asset overlay, emitted focus and scripted-effect files, and native building definitions. No source edits, compiler run, or native-engine test were performed for this review.

- Compiled design: `tools/france_1970_runtime/runtime_design.json`, SHA-256 `00d5e2721934ad527360ce0265f1213e345a1df8b0f1999c22599f23199dbbe9`.
- Asset overlay: `tools/france_1970_runtime/asset_reward_revision.py`, SHA-256 `b05e3bcbbdbfd1c5e9f454b4703b4b18df23dec1743f2dad595cfad63ffab410`.
- Compiled English localisation: SHA-256 `d8d14b7e1d248ccb2bd84b607a1af4b5fef02e6e21586d05569867f9cf9df274`.
- The compile manifest reports 156 focuses, 35 offers and 1,031 English localisation keys. It reports 91 building levels in the compiled design: 63 focus assets, 25 bilateral-offer assets and 3 decision assets. There are 14 foreign offers with one or more assets.

## Main findings

The overlay replaces 22 positive productivity modifier entries across 20 domestic focuses with 22 extra building levels: six industrial complexes and sixteen offices. Focuses retain their named modifier, research and faction effects unless they were among the targeted positive productivity modifiers. The asset change does not alter any of the 35 signed bilateral packages.

The changed domestic focus fees range from 0.10% to 0.60% of the payer's current GDP at payment. The sum of those twenty percentages is 7.60% if every changed focus were completed; this is a gross policy sum, not one reachable branch total. Several changed focuses are explicitly mutually exclusive, and each payment uses GDP at that focus's completion date. The transaction has no arbitrary treasury-balance gate; it requires positive GDP and charges once.

The 20 focus changes are:

| Focus | Setup fee | Removed positive modifier | Added building levels |
|---|---:|---|---|
| Private Innovation | 0.50% | Country productivity growth +7% | Industrial complex, state 60; offices, state 56 |
| National Champions | 0.40% | Civilian factories productivity +4% | Offices, state 55 |
| Gaullist Participation | 0.35% | Civilian factories productivity +3% | Industrial complex, state 58 |
| Managerial Autonomy | 0.25% | Civilian productivity +4%; offices productivity +3% | Offices, state 56 |
| Labour Compact | 0.30% | Civilian factories productivity +3% | Offices, state 58 |
| Productive Compact | 0.55% | Civilian productivity +7%; factory efficiency growth +4% | Industrial complex, state 54; offices, state 57 |
| Public Bank Credit | 0.50% | Offices productivity +3% | Offices, state 54 |
| Republican Left | 0.25% | Offices productivity +3% | Offices, state 60 |
| Civilian Social State | 0.45% | Offices productivity +5% | Offices, states 58 and 64 |
| Shopkeepers' Credit | 0.35% | Offices productivity +4% | Offices, state 64 |
| Industrial Champions | 0.60% | Civilian factories productivity +6% | Industrial complex, state 55 |
| Regional Industry | 0.60% | Civilian factories productivity +4% | Offices, state 63 |
| Industrial Basins | 0.45% | Factory efficiency growth +4% | Industrial complex, state 54 |
| Social Renewal | 0.25% | Factory efficiency growth +4% | Offices, state 56 |
| Worker Self-Rule | 0.50% | Factory efficiency growth +6% | Offices, state 58 |
| Workers on the Board | 0.25% | Factory efficiency growth +5% | Offices, state 62 |
| Party Discipline | 0.10% | Factory efficiency growth +4% | No building; finite industry research and political-power effects remain |
| Social Settlement | 0.30% | Factory efficiency growth +3% | Offices, state 57 |
| Statutory Labour Pact | 0.35% | Factory efficiency growth +6% | Industrial complex, state 55 |
| Compatible Systems | 0.30% | Factory efficiency growth +6% | Offices, state 56 |

These are investments with tangible construction, not equivalent copies of the removed percentage modifiers. Their value now depends on the state's infrastructure, other production and office modifiers, and remaining slots. The one exception is Party Discipline: its original efficiency-growth bonus is exchanged for a GDP cost while its finite industry research and political-power reward remain. This is internally consistent as a party-apparatus choice but is not one of the new building rewards.

## Transaction and capacity audit

Domestic focus and decision helpers perform a whole-package asset preflight before the GDP debit. The preflight checks state ownership, control and full control; it checks the live physical building level against the native cap, and province-specific naval-base levels against that province's cap. If any required target fails, the focus or decision does not complete and the fee is not charged. The actual helper repeats its per-asset guard, awards one shared state slot per building level, then adds construction and records its receipt. State-level capacity is checked against the full quantity, not just one level.

Bilateral acceptance checks asset ownership, control, full control and live physical capacity for every asset on both sides before charging either country. It then charges each signatory against its own current GDP, grants one shared slot per level, and applies the accepted assets in the same transaction. Bilateral offers currently use state-level targets; the generator rejects province-specific foreign assets until a province preflight is explicitly supported. The checks are dynamic, so a target that changed hands or reached its limit after an offer was sent blocks acceptance.

All 91 current asset rows use `amount = slots = 1` and `once = yes`; no row failed that contract. The 66 emitted France focus/decision building helpers are unique. Bilateral asset effects are emitted inline under their own named acceptance transaction and do not share helper IDs. Repeated same-state/building assets within a single offer are rejected by the generator; the current design has none. Each state receives the slot before construction, including infrastructure and energy buildings that do not consume shared slots.

The cap values used by both generators match the current native definitions in `common/buildings/00_buildings.txt`:

| Building | Native limit | Definition source |
|---|---:|---|
| Infrastructure | 6 per state | `00_buildings.txt`, infrastructure definition |
| Industrial complex | 50 per state | `00_buildings.txt`, `level_cap.state_max` |
| Offices | 50 per state | `00_buildings.txt`, `level_cap.state_max` |
| Agriculture district | 10 per state | `00_buildings.txt`, `level_cap.state_max` |
| Arms factory | 35 per state | `00_buildings.txt`, `level_cap.state_max` |
| Fossil powerplant | 20 per state | `00_buildings.txt`, `level_cap.state_max` |
| Internet station | 11 per state | `00_buildings.txt`, `level_cap.state_max` |
| Dockyard | 20 per state | `00_buildings.txt`, `level_cap.state_max` |
| Naval base | 10 per province | `00_buildings.txt`, `level_cap.province_max` |
| Nuclear reactor | 20 per state | `00_buildings.txt`, `level_cap.state_max` |

The France domestic targets use native 1970 state IDs: 54 Hauts-de-France, 55 Normandie, 56 Île-de-France, 57 Alsace-Lorraine, 58 Bourgogne, 60 Aquitaine, 62 Rhône-Alpes, 63 Provence, and 64 Bretagne. These states are French-owned in their history files. The existing regional naval-base reward targets province 11834 in Provence; its 1970 history has 3 naval-base levels there against a province cap of 10. The reactor decision targets Loire, state 59, whose history starts with 3 reactor levels against the state cap of 20.

Foreign asset targets include GER states 42 and 1080, USA state 811, ALG state 386, ITA state 265 and SOV states 652 and 661. The bilateral helper verifies the current recipient ownership and full control at acceptance rather than assuming these 1970 owners remain unchanged. Where several agreements can invest in GER state 42, each acceptance rechecks the live level; offices, internet stations, infrastructure and industrial complexes each use their separate native cap.

## Route and save behavior

A focus with multiple buildings charges one fee for its complete package. For example, Regional Industry charges 0.60% GDP for its full set of three levels: an existing industrial-complex reward in state 54, a province-specific naval base in Provence, and the new office in Provence. Public Bank Credit charges 0.50% for its two offices. The availability guard checks all listed assets before either focus can complete.

The current migration flag, `COLDWAR_FRA2_party_revision_20261029_investment_migrated`, rebuilds earned domestic programme modifier pools from existing focus receipts. It clears old pool values and adds back only current modifiers for already completed focuses. It never invokes building helpers or charges new fees. Existing saves therefore retain previously earned buildings and prior payments, but do not receive the newly substituted buildings for past focus completions. New completions receive the new fee and asset bundle once. Signed bilateral packages retain their separately managed agreements and are not part of this domestic modifier-pool rebuild.

This avoids duplicating the old productivity buffs or replaying paid rewards. It also means an old save with completed investment focuses can have fewer buildings than a fresh game that completes those same focuses after the update; that is the explicitly selected no-replay policy.

## Geographic copy refresh

The six mismatches from the previous review have been corrected in `asset_reward_revision.py` and recompiled. The current descriptions now match the target state IDs: Private Innovation and Republican Left use Aquitaine for state 60; Civilian Social State and Worker Self-Rule use Bourgogne for state 58; Shopkeepers' Credit uses Aquitaine and Bretagne for states 60 and 64; Regional Industry uses Provence for state 63. The Productive Compact description now names Alsace-Lorraine for state 57. I found no remaining geographic mismatch in the corrected descriptions checked for this refresh.

## Source references

- Overlay content and fee setup: `tools/france_1970_runtime/asset_reward_revision.py:10-96`.
- Physical cap and full-control preflight, slot grant order and receipt: `tools/france_1970_runtime/core.py:351-399`.
- Whole-focus and decision asset guards: `tools/france_1970_runtime/core.py:400-425`, `tools/france_1970_runtime/core.py:695-703`.
- Bilateral capacity preflight and slot-before-construction transaction: `tools/france_1970_runtime/diplomacy.py:193-230`, acceptance checks at `tools/france_1970_runtime/diplomacy.py:403-428` and transaction at `tools/france_1970_runtime/diplomacy.py:479-518`.
- Completed-focus modifier rebuild without replaying construction: `tools/france_1970_runtime/core.py:132-162`, with the one-time migration flag at line 15.
- Native building caps: `common/buildings/00_buildings.txt`, definitions beginning at lines 43, 59, 75, 93, 109, 170, 255, 269, 346 and 369.
- State evidence: `history/states/54-Haute-de-France.txt`, `55-Normandie.txt`, `56-Ile de France.txt`, `57-Alsace-Lorraine.txt`, `58-Bourgogne.txt`, `60-Aquitaine.txt`, `62-Rhone-Alpes.txt`, `63-Provence.txt`, `64-Bretagne.txt`, and the named foreign state files.

The manifest's static counts are source/output evidence, not a native engine or multiplayer test. The geographic copy findings are resolved; no other issue was found in this bounded refresh.
