# Vietnam reward rework

Implemented in the loaded mod source on 19 October 2026. This supersedes the earlier proposal-only impact audit. All 307 focuses received an explicit reward review: 95 common, 144 political and 68 campaign focuses. The tree now has 55 reciprocal exclusive pairs, two more than before. All 48 original decision programmes received explicit replacement effects; the 30 campaign actions retain real offers, verification and paid-renewal functions.

The canonical revision is `tools/vietnam_1970/reward_rework.json`, applied by the import-safe runtime adapter over the two immutable original approval snapshots. New values replace previous contributions. They are not bonuses added on top of the old values. Existing country history, starting armies, equipment, technologies and the native political succession provider were not regenerated.

## The immediate example: Party Schools

| Focus | Useful effects | Cost |
|---|---|---|
| Party Schools | Bureaucracy expenses 6% lower; construction 5% faster; one 50% industry research bonus | Education expenses 1% higher; one contribution of $0.025 billion |
| Hear the Economists | Research 3% faster; civilian-industry construction 6% faster; corporate-tax income factor 4% higher; one 50% electronics research bonus | Education expenses 1.5% higher; one contribution of $0.025 billion |

These are the competing uses of the next extraordinary training/advisory allocation: district implementers versus specialist economic review. Neither choice declares the other profession historically impossible. Both are now immediately after Chinh's opening focus. The 70-day opening plus one 70-day choice fits his short historical tenure. Their institution survives ordinary Communist succession, pauses when the party leaves, and returns without granting research again. The later personal political programme still requires its actual leader.

## What changed throughout the tree

- Generic signed-productivity-growth rewards were removed from the revised focuses and decision programmes. They could amplify negative growth. They were replaced by actual construction, production, fiscal, administration, research or training outcomes that match the subject.
- The next extraordinary cadre allocation now chooses reserve-training networks or provincial civil offices. Front participation and sovereignty remain compatible with both. This replaces an initially considered but historically artificial four-way outlook ban.
- Linh's capital policies are a separate direct choice after either Party monopoly or political pluralism. Screened domestic industrial development gives civilian construction, tax collection and sanctions resilience with administrative cost. Broader investment support gives construction and a finite construction-research bonus with market exposure. Neither focus controls the native FDI menu.
- Le Duan's heavy programme combines military output, efficiency and an industrial research opportunity, with a small agricultural cost. Civilian recovery instead brings stronger agriculture and construction with a small military-output cost. The finite research opportunity also gives the industrial choice value before a large military-production base exists.
- Capital Goods First now rewards industrial knowledge and investment execution rather than simply calling machine-building an armament-output bonus. Northern workshop equipment creates an actual queued military-factory project.
- Hanoi rehabilitation is now a 70-day funded focus that completes one civilian complex in state 522. The old later civilian-complex grant is replaced by civilian toolmaking, so this does not create a duplicate seventeenth building reward. Fifteen other projects remain ordinary construction. Existing staffing and consumer-goods rules still apply.
- Aircrew Training now grants 35 air experience and one 25% air-doctrine cost reduction, with education cost. It no longer grants generic research or requires dockyard repairs. Its independent branch is placed at (32,20) to avoid drawing through the fleet card.
- Training schools and liaison institutions have durable replacement stages and finite usable research/experience rewards. They do not expire while the next two focuses are being completed.
- Military operations use funded finite terms. Prepared plans can be earned before a short real war and activate immediately when their genuine conditions begin. Peace/expiry does not refill them. Renewals remain paid.
- China homeland-defence values are preserved exactly, including entrenchment, core defence and genuine forest/jungle defence, without a new supply penalty. Counteroffensive programmes remain a distinct alternative.
- Cambodian offensive and real-victory incentives remain substantial. New withdrawal, reconstruction and cooperation dividends require actual deployments, drawdown, current agreements or native assistance where promised. No focus invents a victory, troop movement, peace or acceptance by another player.
- Civil and political associations improve oversight and political capacity. They do not grant an unexplained electronics breakthrough. Procurement improves provisioning or administration, and military experience is given to real training/staff work.
- Decision programmes now give material temporary outcomes. For example, local pilots give 10% civilian-industry construction and 10% repair speed at 1.5% bureaucracy cost; enterprise reform gives 10% civilian-industry construction and 6% tax income at a 2-point stability cost. Funding and one-per-family controls remain in execution.
- Foreign programmes use partner families, allowing unrelated Soviet cooperation, Chinese commerce and negotiations to coexist. Accepting legacy agreements now displays the actual Vietnamese contribution and timed idea through a non-executing native preview, with a short English description.

## Preservation, units and persistence

The per-focus packages are explicit contributions, not advertised family totals. Campaign family stages are complete replacements. Exact party/leader gates remain in adoption; ordinary national construction and finite knowledge are not reversed by a political change. The two cadre-education alternatives have their separate party-bound institutional modifier.

0.01 billion means $10 million. Expense modifiers affect the named expenditure component, not the entire state budget. Corporate-tax modifiers affect receipts, not the nominal tax-rate setting. Agricultural productivity is a real MD economic modifier, not an invented food stock. Flat entrenchment levels are distinguished from percentage modifiers. Forest/jungle defence is army terrain training owned by its active policy; China-targeted bonuses apply against China across fronts.

Existing saves rebuild earned programme values once from successful implementation flags. This migration executes no building, money, experience or research transactions. Completed old projects are not converted retroactively into different factories, and old completed focuses do not receive a second research payment. Native save loading and multiplayer balance still need an actual HOI4 session.

Concurrent historical-party localisation and roster edits were preserved. They were not reverted to the pre-rework backup. The repeat-build check compares the currently shared/manual files before and after compilation.

## Verification

The main, campaign and numeric-revision source checks pass. Selected execution tests pass: 21 base transaction scenarios, 21 campaign scenarios and 14 native politics scenarios. They cover funding, real ownership/slots, inert previews, no duplicate grants, party return, inherited cadre training, once-only migration, prepaid war activation, timed expiry, terrain cleanup and recipient-owned agreements. A second build changes none of 63 tracked output/integration/input files and preserves current manual files.

The installed source reconstruction supports all 307 focus selections and pointer click targets, all 110 sides of the 55 exclusive pairs, pan/zoom and saved-state restoration. A native-art Chinh branch proof was visually inspected. Browser execution and HOI4 engine execution have not been observed; DOM mocks and Clausewitz interpreters are not engine tests.

Useful source files:

- `tools/vietnam_1970/reward_rework.json`: complete explicit implementation data
- `tools/vietnam_1970/reward_rework.py`: import-safe overlay and native reward serialization
- `tools/vietnam_1970/compile.py` and `campaigns.py`: actual generation, transaction and lifecycle code
- `tools/vietnam_1970/validate_rewards.py`: numeric comparisons against emitted native code
- `tools/vietnam_1970/README.md`: installed contracts and rebuild commands
- `common/national_focus/COLDWAR_VIE_1970_focus.txt`: loaded focus tree
- `history_review.md`: pure historical review of all 307 original cards and source constraints
- `common.json`, `politics.json`, `campaigns.json`: specialist catalogues used to assemble the explicit revision

The historical review and prior mechanics audit contain primary sources and 29 normal-MD reward examples. Current code also verifies native CAT_industry, CAT_construction, CAT_electronics, CAT_infantry_weapons and CAT_special_forces_equipment categories; native air/naval/land doctrine-cost reductions; and actual consumers for agriculture, expenses, tax, market exposure and sanctions resilience. Historical sources justify the programme and opportunity cost; the game values are balance choices requiring live playtesting.
