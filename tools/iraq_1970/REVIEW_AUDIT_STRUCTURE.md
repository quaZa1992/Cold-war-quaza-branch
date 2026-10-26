# Independent review: assembled Iraqi audit structure

Reviewed19October2026 while the root integration was being completed. This is source/graph review, not a HOI4 visual or campaign certificate. The reviewer authored only test_audit_structure.py and this note during this pass; audit_design.py was not edited by the reviewer.

## Snapshot and result

- Source: tools/iraq_1970/audit_design.py, SHA256 18a9cbc71b4395ff517348a5878417d3a141ac94a2756a916f42af91769bd2f9.
- Original IDs retained:426; active focuses:410; retired empty compatibility entries:16.
- Independent test suite:13/13PASS at the last run, covering graph references, symmetric exclusions, cycle detection, DNF reachability with native AND/OR groups, each compatible policy combination for shared finales, collision-free grid positions, descending prerequisite edges, resolved relative anchors, entry splicing, retired reward removal, exact oil reorder and common Iran-war support unlocks.
- Grid points do not collide and every parent is above its child. These properties do not prove that native rendered labels or routed connectors never overlap.

## Findings corrected during this independent review

1. Initial final-parent declarations named nonexistent civic_courts/civic_civil_service,royal_civil_service,puk_revenue_settlement/puk_union_councils. A conditional silently skipped the rewrite. Root corrected actual IDs and now asserts their existence.
2. Mandatory Civic commercial courts initially stranded the social-republic route; mandatory PUK joint services stranded independent-movement alternatives. Root made the relevant branches legitimate alternatives. Policy-combination tests cover this regression.
3. Mandatory KDP shared revenue initially made the supposedly neutral Common Republic depend on a particular fiscal/federal development. Root now follows local policing and requires the northern guarantees to remain respected for its active reward. It does not silently rename every autonomy constitution a federation.
4. Added AND links to an institution that was already an ancestor of the other parent created cosmetic complexity and long connectors without new gameplay. Root simplified Civic,Royal,KDP and the postwar milestone to their actual political subjects.
5. Moving Wasit into the cooperative package could redirect a shared irrigation prerequisite into a mandatory cooperative choice. Root uses a specific agri_wasit -> agri_large_irrigation graph alias while preserving cooperative historical building credits. Smallholders+large irrigation remains possible.

## Current binding endpoint parents

| Focus | Native prerequisite groups (OR within parentheses; AND between groups) |
|---|---|
| state_compact | (autonomy_guarantees) AND (professional_command) AND (tax_registry) |
| baath_future | (enterprise_accounts) AND (baath_citizenship) AND (party_social_bargain) |
| bakr_succession_plan | (bakr_guarantees OR bakr_deputy_budget) |
| saddam_legacy | (saddam_local_procurement) AND (saddam_bounded_deterrence OR saddam_debt_service) |
| officer_settlement | (officer_reintegration) AND (officer_continuity) |
| arab_republic_endures | (arab_training_network) |
| icp_socialist_republic | (icp_safety_inspection) AND (icp_peasant_credit) |
| aziz_party_renewal | (aziz_workplace_delegates) AND (aziz_safe_return) |
| civic_mandate | (civic_security_oversight) |
| royal_settlement | (royal_service) |
| kdp_common_republic | (kdp_local_policing) |
| puk_federal_mandate | (puk_payroll) AND (puk_trade_routes) |
| dawa_government_review | (dawa_literacy) AND (dawa_medical_network) |
| sciri_iraqi_mandate | (sciri_civil_review) |
| iip_government_mandate | (iip_public_service) AND (iip_medical_welfare) |
| war_peace_dividend | (war_reintegration) |
| agri_reform_delivery | (agri_distribution) AND (agri_water_inspection) AND (agri_clinics) |

KDP Common Republic additionally has active_requires=[Northern guarantees fulfilled]. Contract gating is a runtime condition, not a graph edge; breaking and restoring the northern contract should be tested in the game independently of the graph check.

## Shape diversity

A label-independent recursive fingerprint preserves AND/OR grouping, exclusivity and prerequisite depth. The old design had12identical chapter graphs. Current repeated clusters are:

- officers, communists, aziz, dawa, sunni.
- nasserist, kurds, sciri, war.
- state, baath.

This is a real reduction in repeated structure, with separate industry, oil, defence, education, leadership and constitutional milestone shapes. Several18-card political chapters remain structurally similar. That is a remaining editorial/design characteristic, not a collision or deadlock. Distinct conditional decisions and meaningful institutions matter more than changing parent requirements solely to make a fingerprint unique. Avoid manufacturing long redundant AND connectors for cosmetic variety.

## Audit coverage and conditional promises

| Topic | Source coverage | Remaining boundary |
|---|---|---|
| Administrative filler |Penalty-only entry/review cards retired; substantive maintenance/quality and rural credit consolidated |Loaded stubs, queue suppression and save-credits require compiler/runtime validation |
| Six headline choices |Reward transformation matches consolidated values and conservative military addendum |Native hovers and actual affordability not observed |
| ICP/Aziz opposition timing |Governing paths renamed for cabinet/party institutions; preaccession decisions exist at the incumbent regime |Government/coalition consent and expiry need runtime checks |
| IPC ownership |Actual acceptedENGcontract remains; early concession infrastructure/research, new90-day marketing cost on genuinely new nationalisation, policy review |No extra invented free foreign liquidity. Old accepted contracts must not pay another2%fee or replay grants |
| Agriculture |Cooperative credit+Wasit district, smallholder credit and meaningful productive/consumer choices; paid current-priority review |Old district and credit receipts must reduce upgrade obligations; no double Wasit grant |
| Northern settlement |Two current fiscal ideas, actual existingKUR/PUKrecipient response, domestic delegates when absent, live-contract cleanup; KDP neutrality repaired |Current revenue-sharing path also writes federal_settlement. If autonomy revenue-sharing without federalisation is intended, that is a further constitutional design choice, not something the text can conceal |
| Supplier diversity |French/British recipient-owned advisory offer behind mixed supply; actual treasury/upkeep guards |At review the accepted mission still reused genericAdvisers(+3%org,+5%personnel,180days), without the concrete limited technical gain suggested in the audit. Root was notified |
| Iran war objective |Assessment precedes territorial claim; shared operational planning opens credit and supplier access; annexation remains explicit before the territorial ultimatum/core |No separate limited Shatt-only war goal/reciprocal peace contract is designed here. AUDIT.md explicitly made that route conditional on a real executable bilateral treaty. Do not claim this was implemented as a new limited war |
| US constitutional stance |Owned by the parallel USA integration |This review does not certify its new current-stance decision or event transaction |

## Presentation follow-up

The neutral Iranian assessment is available before the1979crisis. Its initial rewritten text stated that political upheavals had already unsettled Iran’s army. Root was notified to use time-neutral assessment language and reserve real-crisis assertions for the conditionally available disarray decision.

The whole-tree source positions and native asset references remain separate from actual native focus hovers. Inspect the condensed two-entry Industry branch, the oil ownership/delivery join at45,18, the new state three-institution join and each political endpoint in a fresh1970start. No screenshot or HTML is being represented as a native engine check by this review.

## Next checks after generation

Run the independent structure and reward suites again after the final root edits. Trace all changed catalogue consumers, hidden compatibility stubs, actual new-focus callbacks and individual save upgrades. Then verify a fresh campaign, one old-save migration, party change, broken/restored treaty and receiver refusal/acceptance. Source-level feasibility does not establish native rendering or networked player behaviour.

## Procurement finding resolved in the final reward source

After the generic-advisory finding, the parent specified a material direct policy distinction. audit_rewards.py now supplies Soviet standardisation-10%supply,-3%foreign influence,2%GDP versus mixed supply+3%supply,one35%Aircraft research use,2%GDP. The separate political owner is adding one25%Artillery research use only on the first genuinely acceptedFRA/ENGmission. The direct focus is not pretending that an aircraft or foreign equipment transfer occurred. Reward source tests15/15 and structure tests13/13passed together after these final source edits. No loader/compiled-output/engine claim follows from that result.

## Additional independent migration review

A follow-up inspection of audit_migration.py found that its initial upgrade quote subtracted currentGDP times an old percentage rather than the source's preserved actual invoice. That can overcredit a growing economy and overcharge a shrinking economy despite the correct historical invoice variables already being present in audit_legacy_cost_credits. Root was notified before final generation. Use the actual positive stored invoice of an implemented paid source; a quoted unimplemented focus must never earn a paid credit. Example: old Heavy invoice0.2, currentGDP20,new5%package1.0 ->0.8top-up. If currentGDP5,new5%package0.25 ->0.05top-up. The percentages describe the old price rule, not an actual historical payment after GDP changes. Confirm the corrected generated quote, not just the module's introductory comment.
