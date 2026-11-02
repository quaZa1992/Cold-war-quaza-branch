IMPERIA COLD WAR

# France party expansion independent mechanics review

## Scope and result

Reviewed the design-only `proposal.json` and `ADDITIONS.json` at SHA256 `C8E6AB3933BF72A14B043C3A92D846826F3D1937F902EFC7CC3D0DD64364C055` and `27D407C6196551CF8D816136380E788C2A6B20A548DE39DAC90DEC165E115DAD`, respectively. This final bounded refresh rechecked the changed focus parents and infrastructure targets against the guards and current state history. The full review covers 20 added focuses, prerequisites and exclusions, effects, locations, capacity guards, GDP fees, native icon aliases, the reused PS decision, and the two declared CID lifecycle changes. No runtime or builder files were changed.

**Result:** no blocking mechanics or balance defect identified in the latest proposal snapshot. State names, site-preparation guards, conservative infrastructure placement and CID date-pool findings are corrected. The proposal's `DESIGN_CHECKS.json` reports the matching proposal hash, no issues, preserved runtime baseline and `native_engine_tested: false`. This remains a source and design review, not an engine or tooltip test.

### Final bounded refresh

The latest geometry and prerequisite cleanup moves the RI, Radical and Ecology choice pairs to their respective terminal alternatives, and the PS pair can follow Public Bank Credit or Social Contract. These routes still resolve to valid nodes and do not change any effect payload or the recorded compatible modifier totals. The two moved infrastructure levels are now in state 962 Auvergne and state 959 Pays de la Loire. Both states are French-owned and controlled in the 1970 history; each starts at infrastructure level 3, so the added level reaches 4 of 6. Each node's latest reward guards check party, scenario, one-time receipt, positive GDP, ownership, control, full control and the type cap. The matching `DESIGN_CHECKS.json` report is design-only and does not claim an engine test.

The new [README.md](README.md) accurately describes this as a proposal-only package: 176 focuses, 20 additions, 35 existing agreements, no new decision, a broadened prerequisite on the existing PS fund, and no runtime installation. It separates browser/source validation from engine, save, performance and multiplayer validation. It reports 32 new building levels plus five standalone slots, consistent with the current design checks. The README also identifies `DESIGN_CHECKS.json`, `LAYOUT_REVIEW.md`, `PREVIEW_QA.json` and `PREVIEW_BUILD.json` as the evidence files. No native test is implied by this review.

## Graph, gating and package review

- The proposal has 176 unique focus nodes, 20 added focuses, and no dangling prerequisite or exclusion references. Each new node's party predicate matches its party group's native trigger, appears again in its reward guard, and includes the 1970 scenario and positive-GDP checks. Every new package is one-time.
- The eight new party pairs are mutually exclusive within each pair. Their two sides have real differences in asset type, finite research, faction opinion, revenue or named service-cost consequences. No pair is plainly dominated by the other side. The branch economics are not reduced to repeated productivity boosts.
- All 20 setup debits are shares of the paying country's current `gdp_total`, between 0.30% and 0.65% of GDP, with five or fewer fractional digits. There are no new recurring money streams and no new bilateral offer. The existing recipient-approved offers are unchanged by this addition set.
- The initially proposed extra PS payment was removed. `Conversion Boards` now unlocks the existing `Regional Conversion Fund`; that decision accepts either Public Bank Credit or Conversion Boards as its parent. Its original 0.40% GDP debit, one Hauts-de-France industrial complex plus one slot, and finite industry bonus remain the single transaction under the existing once-only receipt. Conversion Boards adds its own 0.08% GDP preparation package, two state slots, one finite industry bonus, and the existing decision unlock. This is not a duplicate payment or building grant.

## Native effects and assets

- The unique modifiers in the additions use supported MD keys: corporate-tax income, education, social and health cost multipliers; `training_time_army_factor`; industrial-complex construction speed; `energy_use_modifier_civs`; equipment cost; and air-force personnel cost. The 6% positive army training-time value is a cost: it lengthens army training. The new research categories are `CAT_industry`, `CAT_electronics`, `CAT_infrastructure`, `CAT_armor` and `CAT_aircraft`.
- `CAT_infrastructure` is registered in MD at `common/technology_tags/00_technology.txt:193` and used by real industry technologies at `common/technologies/industry.txt:7048+`. It was absent from the previous palette list; I added it to `MECHANICS.md`.
- Every focus building transaction has its own-state ownership, controller/full-control and native building-level guard. Each building grant adds one shared slot before the building. The two standalone site-preparation rewards also verify ownership and full control of every target state. I checked each guard against the native caps: industrial complexes and offices 50, infrastructure 6, arms factories 35, agriculture districts 10 and fossil powerplants 20. All 20 added nodes passed this per-building guard check.
- All physical targets are French metropolitan states at the January 1970 start. They are comfortably below the type caps. The largest linked industrial build is the PS route in Hauts-de-France: its starting 2 industrial complexes can receive one level from Basin Conversion and one from the existing Regional Conversion Fund, reaching 4 of 50. State 61 has starting infrastructure level 3 and one added level reaches 4 of 6.
- The project override displays state 61 as `Midi-Pyrénées` (`localisation/english/state_names_l_english.yml:64`); the history file is `history/states/61-Midi Pyrenees.txt`. All four new descriptions and their visible state conditions now use `Midi-Pyrenees`, identifying the correct scenario state. The upstream MD label `Occitanie` is intentionally overridden for this 1970 scenario.
- Every added `icon_source` maps to an existing focus sprite alias in `interface/COLDWAR_FRA2_polish_art.gfx`. The `FRA_christian_socialism` and `FRA_ruralism` aliases use their actual registered `FRA_*` spellings.
- The three new faction-opinion changes call the actual MD helpers for labour unions, industrial conglomerates and farmers. Those helpers clamp opinion to 0-100; the French 1970 history starts the corresponding faction ideas. The changes are one-time, so party switching or returning cannot farm them. No minister effect was added.

## Compatible route totals

These totals include the new package and compatible earlier focuses in that party group. Alternative branches are not summed together.

| Party | Compatible total or range | Route notes |
|---|---|---|
| RI | Corporate-tax income multiplier can reach -7% with SME Risk Capital or +1% with Export Finance. | The latter stacks with Sound Franc and Business (+3 - 6 + 4). SME Capital stacks with Credit Expansion (-4 - 3); it does not combine with Export Finance. |
| Centre | Health cost multiplier can reach -8%; social cost can reach +9%. | The first is Mutuals and Mutual Districts (-4 - 4). The second is Mutuals and Family Services (+5 + 4). These are different new alternatives. |
| Radical | Education cost can reach +12%; corporate-tax income can reach -8%; Civil Service Trials adds +6% army training time. | Education combines American Challenge (+4) and Secular School (+8). Enterprise and Open Orders combine the two tax reductions (-5 - 3). The civilian-service route's military training penalty is a real opportunity cost, not a civilian training reward. |
| PS | Social cost can reach +10%; industrial-complex construction speed nets +1% on the Redistribution plus Workplace Charters route. | The social-cost path is Social Contract (+6) plus Basin Conversion (+4). The added choice can follow either Public Bank Credit or Social Contract; both still reach the same stated stack ceiling. Redistribution's +6% build speed combines with Workplace Charters' -5%; the Competitiveness path retains the full -5% construction delay. |
| PCF | Social cost can reach +11%; health cost falls by 4% on Municipal Health. | Municipal Socialism (+6) can be followed by Municipal Health (+5). Supply Contracts is the alternate, with a 4% corporate-tax income reduction. |
| PSU | Social cost can reach +11%; corporate-tax income can fall by 7%. | Union Autonomy (+7) plus Tenants Councils (+4) form the social-service route. Union Institutes (-2), Cooperative Markets (-3) and Land Banks (-2) form the distinct tax-revenue route. |
| Ecology | Civilian energy demand can fall by 11% through Environment Account, Efficiency Ecology and Municipal Heat. | This is an additive energy-use route; it does not stack with Local Generation as an alternative to Efficiency Ecology. The latter can instead combine its existing +6% energy-gain multiplier with Municipal Heat. |
| CID / FN | CID corporate-tax income can fall by 10%. FN Arsenal Orders adds 4% equipment cost; this can temporarily stack with the starting deterrent's 5% equipment-cost burden until the defence chapter replaces that inherited spirit. | CID and FN are separate identity phases with no cross-phase exclusion. CID programmes are now confined to the pre-5 October 1972 pool. FN Export Inspection uses a different cost base, the air-force personnel bill (+5%), plus finite air experience and aircraft research. |

Service-cost, tax and energy multipliers affect the named MD calculation, not cash directly. The values above describe additive modifier totals, not exact money amounts. A final tooltip review should keep those bases explicit.

## CID date-pool and save note

`cid_tax` and `cid_cooperatives` now point to the same `COLDWAR_FRA2_CID_programme` pool as the new CID pair, with slot-20 rule and `date < 1972.10.5` activation. Their amounts, fee, assets, prerequisites and geometry are unchanged. Their former idea-pool membership is recorded in `ADDITIONS.json` as two lifecycle-only focus changes. This fixes the earlier leak where old CID modifiers could remain active during the FN identity. Runtime integration must migrate old idea membership without replaying completed-focus fees, assets or one-time rewards. The proposal itself does not claim that save migration has been implemented or tested.

## Verification limits

Source checks confirm effect providers, technology categories, focus sprite aliases, history states and native caps. A read-only structural pass found 176 unique nodes with no missing prerequisite or exclusion references. A local guard check found all 20 added nodes have party/scenario/GDP guards and each building/site slot has target ownership and full-control checks, including the two new infrastructure states. The package has no `README` inconsistency in the scope described above. No native load, game execution, tooltip screenshot, performance run or multiplayer test was performed.
