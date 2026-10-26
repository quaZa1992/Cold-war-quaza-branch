# Iraq and US Gulf structural audit - 19 October 2026

Read-only audit of the currently installed 426 Iraqi focuses and the 15 new US Gulf focuses. These are proposals; no live focus, reward, exclusion or generator was changed.

## What actually looks strange

The main issue is the repetitive policy architecture, not card collisions. **22 of 23 sections have exactly 18 cards and every section has exactly two exclusive pairs. Twelve sections share exactly the same prerequisite/exclusion skeleton.** The overview visibly repeats the same double-diamond and three-spur ending. Country-specific paths should remain, but should stop all having the same shape and pacing.

**No current overlap, missing anchor or cyclic relative position was found.** Existing labels match the inspected installed native-card renders and fit their previously measured native title fields. The large empty strip between the upper political sections ending around y=10/11 and lower section roots at y=15 is visible, but reducing it is an aesthetic/navigation preference, not a functional defect. The width is intentional for many visible alternatives and is not itself proof of bad design.

## Prioritized changes

### STR01 - Eighteen-card template overwhelms country-specific shape (high)

22 of 23 sections contain exactly 18 focuses, every section exactly two mutually exclusive pairs. Twelve sections have exactly the same ordered prerequisite/exclusion graph, irrespective of geometry. Their recurring pattern is root, two two-step choice arms, merge, another two two-step arms, merge, three two-step collectible spurs, finale. The overview visibly resembles repeated stamps.

**Change:** Keep all historically supported parties. Stop enforcing equal counts: combine small administration cards with the policy they implement; give major political choices separate three- or four-card developments; retain shared economic projects beside those choices. Do not compact by deleting alternate governments or forcing global fixed widths.

**Current cards:** `COLDWAR_IRQ_bakr_presidency` (20.0,2.0), `COLDWAR_IRQ_saddam_presidency` (28.0,2.0), `COLDWAR_IRQ_officer_council` (36.0,2.0), `COLDWAR_IRQ_aziz_secretariat` (60.0,2.0), `COLDWAR_IRQ_dawa_civil_government` (20.0,15.0), `COLDWAR_IRQ_sciri_exile_council` (28.0,15.0).

### STR02 - Grand finale accepts just one minor delivery (high)

Each named finale has a single prerequisite block containing three focuses: ANY one suffices, although the converging three-way graphic and sweeping names suggest a finished national programme. This is valid engine OR syntax, not a parser bug. The other two spurs remain collectible afterwards.

**Change:** Decide intentionally per programme. A truly comprehensive capstone should use three separate prerequisite blocks (AND) and give a substantial resulting settlement. A political mandate should instead depend on one relevant political outcome and should not draw misleading lines from unrelated farm/credit/workplace rewards. Avoid making every finale an obligatory six-card checklist.

**Current cards:** `COLDWAR_IRQ_state_compact` (4.0,11.0), `COLDWAR_IRQ_baath_future` (13.0,10.0), `COLDWAR_IRQ_saddam_legacy` (28.0,11.0), `COLDWAR_IRQ_icp_socialist_republic` (53.0,10.0), `COLDWAR_IRQ_kdp_common_republic` (4.0,23.0), `COLDWAR_IRQ_oil_sovereignty` (45.0,22.0), `COLDWAR_IRQ_war_peace_dividend` (84.0,24.0).

### STR03 - Opposition strategy chapters require already being the government (high)

The current emitted availability requires governing party slot 4 throughout; Aziz also requires the actual office-holder. Thus a government studies a Road to Power, organizes a Democratic Opposition and establishes underground cells; the important historical Baath-front/legalization struggle cannot be played while the Baath governs. Localization confirms this is not merely an abstract intelligence programme.

**Change:** Separate pre-accession opposition/coalition activity from the government programme. Keep consent-based legalization and front negotiations in political decisions under the incumbent; bring their result into the later ICP government. Recast governing cards as coalition cabinet rights, internal party organization and returning exiled cadres, or explicitly unlock a bounded opposition chapter without granting government-bound buffs. Do not activate the entire Communist state programme from a coalition seat alone. No proposed geometry until that political contract is selected.

**Current cards:** `COLDWAR_IRQ_icp_front_strategy` (52.0,3.0), `COLDWAR_IRQ_icp_legal_cells` (50.0,4.0), `COLDWAR_IRQ_icp_underground` (56.0,4.0), `COLDWAR_IRQ_aziz_negotiated_road` (58.0,3.0), `COLDWAR_IRQ_aziz_opposition_road` (60.0,3.0), `COLDWAR_IRQ_aziz_united_opposition` (59.0,9.0), `COLDWAR_IRQ_aziz_safe_return` (59.0,10.0).

### STR04 - Oil policy implementation can be bypassed (high)

National Oil Service and Revised Oil Contract are optional side leaves at row 17. Train Iraqi Oil Engineers also sits at row 17 and depends only on Nationalize the IPC/New Concession Terms, so later oil development and Sovereign Accounts can proceed without delivering either chosen institutional arrangement.

**Change:** Set oil_technical_training prerequisites to one OR group containing oil_state_company and oil_concession_delivery. Move training and every subsequent oil card down one row. This reserves actual implementation before shared downstream development while respecting the accepted concession gate. Whether an unaccepted concession should offer a costly unilateral fallback is a separate diplomacy/balance decision.

**Current cards:** `COLDWAR_IRQ_oil_state_company` (42.0,17.0), `COLDWAR_IRQ_oil_concession_delivery` (48.0,17.0), `COLDWAR_IRQ_oil_technical_training` (45.0,17.0), `COLDWAR_IRQ_oil_revenue_state` (44.0,18.0), `COLDWAR_IRQ_oil_diversification` (46.0,18.0), `COLDWAR_IRQ_oil_sovereignty` (45.0,22.0).

### STR05 - Iran war financing/supply are assigned to artificial plan-specific leaves (medium)

Seek Gulf Backing is a short-war-only optional dead end; Secure Foreign Spares is a sustained-war-only optional dead end. Credit and foreign spare parts were not mutually incompatible needs tied to those respective operational plans. Each adds 21 focus days merely to unlock a recipient negotiation. This concerns the direct unlock inside the Iran chapter, not every possible credit source: COLDWAR_IRQ_saddam_credit also unlocks decision_gulf_credit, whose creditor options call COLDWAR_IRQ_gulf_unlock_credit (decisions_module.py302-305), so a sustained-war player can obtain credit through that separate route.

**Change:** Preferred smaller structure: merge both decision unlocks into iran_operational_plan, preserving all actual consent, treasury, debt, equipment and supplier checks. Retire the two standalone unlock-only cards from the proposed next revision, never delete their decisions or ledgers. If dedicated focuses are desired, both must be shared optional support spurs accessible from either plan, not new mutual exclusions.

**Current cards:** `COLDWAR_IRQ_iran_short_war` (92.0,19.0), `COLDWAR_IRQ_iran_sustained_war` (96.0,19.0), `COLDWAR_IRQ_iran_gulf_credit` (90.0,21.0), `COLDWAR_IRQ_iran_supplier_access` (98.0,21.0), `COLDWAR_IRQ_iran_operational_plan` (94.0,18.0).

### STR06 - Several finales are expensive ceremonies with identical payoff (medium)

Ten 49-day political finales share exactly +0.03 stability_factor and -0.02 political_power_factor despite very different political claims. Industrial Review and Social Service Compact require all three lower spurs but only unlock another review decision. This is a reward and pacing problem made conspicuous by identical bottom-card placement.

**Change:** Give milestone finales a distinctive enacted outcome (succession, enforceable settlement, institution or appropriately priced investment). Move routine review/reallocation decisions to the policy selection they actually review. Merge a review-only finale into its governing reform, or keep it with a material resulting national package; do not increase every stability value indiscriminately.

**Current cards:** `COLDWAR_IRQ_bakr_succession_plan` (19.0,11.0), `COLDWAR_IRQ_icp_socialist_republic` (53.0,10.0), `COLDWAR_IRQ_aziz_party_renewal` (59.0,11.0), `COLDWAR_IRQ_civic_mandate` (69.0,10.0), `COLDWAR_IRQ_royal_settlement` (76.0,11.0), `COLDWAR_IRQ_kdp_common_republic` (4.0,23.0), `COLDWAR_IRQ_puk_federal_mandate` (11.0,23.0), `COLDWAR_IRQ_dawa_government_review` (19.0,24.0), `COLDWAR_IRQ_sciri_iraqi_mandate` (28.0,24.0), `COLDWAR_IRQ_iip_government_mandate` (36.0,24.0), `COLDWAR_IRQ_industry_delivery_review` (52.0,23.0), `COLDWAR_IRQ_society_service_compact` (68.0,24.0).

### STR07 - Choice arms converge before players feel different programmes (medium)

Most choices retain distinct modifier variables, so they are not literally fake. But the graph rejoins after one delivery card, and the rest is usually the same three collectible projects. Baath National Front/Exclusive Party State even rejoins at Regional Congress without requiring its chosen optional delivery spur. The visible country trajectory quickly becomes identical.

**Change:** Deepen selected political forks rather than adding arbitrary binary choices to roads and hospitals. Guard priority versus general-staff priority should carry distinct procurement/readiness/support decisions and a route-specific milestone; they need not ban the historical existence of the other force. Bakr deputy choice should shape actual succession safeguards. National Front/monopoly should reach congress through the corresponding charter/screening delivery, with later labor/cabinet rights conditioned on the selected policy. Ordinary national development can remain shared.

**Current cards:** `COLDWAR_IRQ_saddam_guard` (26.0,6.0), `COLDWAR_IRQ_saddam_regular_army` (30.0,6.0), `COLDWAR_IRQ_saddam_guard_supply` (26.0,7.0), `COLDWAR_IRQ_saddam_staff_college` (30.0,7.0), `COLDWAR_IRQ_saddam_regional_role` (28.0,8.0), `COLDWAR_IRQ_bakr_contain_deputy` (18.0,6.0), `COLDWAR_IRQ_bakr_delegate` (20.0,6.0), `COLDWAR_IRQ_bakr_development` (19.0,8.0), `COLDWAR_IRQ_national_front` (12.0,3.0), `COLDWAR_IRQ_baath_monopoly` (14.0,3.0), `COLDWAR_IRQ_baath_congress` (13.0,4.0).

### STR08 - Constitutional models are independently selectable across overlapping active sections (medium)

All 46 exclusion pairs are internal to one section; none links constitutional state choices with party/leader governance. The starting Baath+Bakr+shared state programmes can be active simultaneously, and durable shared settlements remain after a party change. This permits a Civic Compact plus exclusive-party structures without a visible reconciliation of the constitutional promise.

**Change:** Audit specific contradictions, not all combinations: a civic compact can describe institutions without necessarily proving full democracy. Where policies really conflict, use one current constitutional-settlement contract and explicit paid revision that replaces incompatible live programme effects. Do not permanently mutually-exclude different parties entire trees: a later legitimate government must retain playable continuation. New cross-section focus exclusions need lifecycle/save review before implementation.

**Current cards:** `COLDWAR_IRQ_executive_state` (3.0,3.0), `COLDWAR_IRQ_civic_compact` (5.0,3.0), `COLDWAR_IRQ_national_front` (12.0,3.0), `COLDWAR_IRQ_baath_monopoly` (14.0,3.0), `COLDWAR_IRQ_saddam_personal_state` (26.0,3.0), `COLDWAR_IRQ_saddam_party_cabinet` (30.0,3.0), `COLDWAR_IRQ_civic_federal` (68.0,6.0), `COLDWAR_IRQ_civic_unitary` (70.0,6.0), `COLDWAR_IRQ_kdp_autonomy` (3.0,16.0), `COLDWAR_IRQ_kdp_federal_republic` (5.0,16.0).

### STR09 - Iran chapter makes both escalating claims compulsory (medium)

The Southern War Plan has two separate prerequisite blocks, requiring both Southern Command and Assess Tehran's Army. The latter comes only through The Arabistan Claim; therefore even a limited Shatt-frontier strategy must first claim Khuzestan. The graphic looks like two complementary intelligence tasks, but one arm embodies an escalated territorial objective.

**Change:** Move neutral Iranian force assessment to a shared prerequisite or combine it into the frontier dossier. Keep Shatt enforcement and Arabistan annexation as explicit distinct war aims. If a new true mutual pair is wanted, make limited frontier revision versus annexation/integration a deliberate war-aim choice, preserving the user-requested Khuzestan claim/core route on the expansive side. Define real limited-war settlement rewards before making it exclusive. Do not imply a Shatt-only goal can core the whole province.

**Current cards:** `COLDWAR_IRQ_iran_shatt_demand` (92.0,16.0), `COLDWAR_IRQ_iran_arabistan_claim` (96.0,16.0), `COLDWAR_IRQ_iran_southern_command` (92.0,17.0), `COLDWAR_IRQ_iran_tehran_assessment` (96.0,17.0), `COLDWAR_IRQ_iran_operational_plan` (94.0,18.0).

### STR10 - Repeated portraits flatten Saddam policy categories (low)

The same Saddam leadership image is used on six cards including staff training, Iranian Revolution and deterrence; this is visibly repetitive in the normal-scale render and weakens policy recognition. The portrait itself matches the supplied visual and should remain.

**Change:** Keep the portrait on the presidency and a genuine personal-leadership milestone. Reuse native thematic education/staff, diplomacy, Iranian political crisis and readiness icons for the other cards. This requires art-only changes, no modifier or layout change.

**Current cards:** `COLDWAR_IRQ_saddam_presidency` (28.0,2.0), `COLDWAR_IRQ_saddam_technocrats` (30.0,4.0), `COLDWAR_IRQ_saddam_staff_college` (30.0,7.0), `COLDWAR_IRQ_saddam_regional_role` (28.0,8.0), `COLDWAR_IRQ_saddam_iran_dossier` (26.0,9.0), `COLDWAR_IRQ_saddam_bounded_deterrence` (26.0,10.0).

### STR11 - Oil training duplicates its later operators card (medium)

Two different 35-day focuses, Train Iraqi Oil Engineers and Refinery Operators, have exactly the same persistent +2% efficiency-gain/+1% research pair. General country-wide research is also a weak label match for training a specific refining workforce.

**Change:** Merge operator training into the Baiji refining delivery and keep one meaningful trained-workforce milestone; alternatively keep both only after giving genuinely distinct, supported sector/technology outcomes and a combined cap. Do not merely relabel identical small rewards.

**Current cards:** `COLDWAR_IRQ_oil_technical_training` (45.0,17.0), `COLDWAR_IRQ_oil_operators` (45.0,21.0).

### STR12 - Debt focus title promises territory without a territorial effect (medium)

Credit from Territory, at (84,10), currently unlocks a Regional Debt Review subject to creditor consent. It has no territorial transfer, demand, claim, core or territorial loan collateral effect. The historical Kuwait coercion chain lives elsewhere.

**Change:** Rename this diplomatic card Regional Debt Settlement or Negotiations with Gulf Creditors. Keep coercive claims/war goals and occupation incentives in the explicit postwar Gulf crisis programme. Do not add territory as a hidden fix for an inaccurate title.

**Current cards:** `COLDWAR_IRQ_foreign_kuwait` (84.0,9.0), `COLDWAR_IRQ_foreign_debt_diplomacy` (84.0,10.0).

### STR13 - US Baghdad Accord and armed protection need a clear relationship (medium)

Baghdad Accord and Guarantee Self-Rule converge into an OR recovery card but are both collectible. This can mean sequential de facto protection followed by recognition, or genuinely alternative postwar commitments; the graph does not explain which. Current runtime allows a respected settlement as an eligibility alternative for some protection outcomes.

**Change:** Choose and state the intended policy. Prefer an exclusive CURRENT settlement stance: negotiated recognized autonomy with Baghdad versus externally protected de facto self-rule. Give each distinctive ongoing benefits, payer obligations and escalation risk; later switch by a real negotiated policy revision instead of a permanent focus lock. Retain independent Desert Storm 14-day access and humanitarian entry roots; do not make humanitarian aid require first provoking the uprising or a coalition contributor accepting a deal.

**Current cards:** `COLDWAR_USA_gulf_baghdad_accord` (30,7), `COLDWAR_USA_gulf_self_rule` (34,7), `COLDWAR_USA_gulf_recovery` (32,8).

### STR14 - Commercial Services has the wrong visual theme (low)

`COLDWAR_IRQ_industry_commercial_services` at (54,21) uses `welfare`: a large red heart, despite creating an offices building. Replace its art with the native `generic_office_construct` sprite. It is registered in main MD `interface/goals.gfx` at lines 5885-5886 and points to `gfx/interface/goals/00_economy/generic_office_construct.dds`; the actual texture was visually inspected and shows an office tower with construction tools. `industry_grid_management` (50,22) uses `crane_and_tower`; a native `national_grid` treatment would identify dispatch better. `industry_tax_service` (54,22) already uses `balance_buget` finance art and is not a factory-icon defect. Reusing appropriate MD art is normal; the problem is the specifically misleading heart on offices.

## Concrete oil layout proposal

Only STR04 has a fully specified local coordinate transform: keep oil_accounts, oil_nationalize, oil_renegotiate, oil_state_company and oil_concession_delivery fixed; add +1 to y for training itself and the twelve subsequent oil cards (thirteen moved cards total). Train Iraqi Oil Engineers moves from (45,17) to (45,18); Sovereign Accounts moves from (45,22) to (45,23). The oil footprint becomes x=42..48,y=15..23 and stays clear of the adjacent industry x=50..55 footprint. The logical change is intentional: training now follows the actually delivered chosen arrangement. A fresh faithful render and reachability/cost review are still required before implementing.

## What to retain

- The historically relevant alternate governments and actual party/office-holder gates for government programmes. Fix specifically misplaced opposition chapters rather than deleting parties.
- The 14-day US Desert Storm crisis entry, independent optional coalition and basing efforts, and separate humanitarian access. Do not hide crisis response behind a long generic tree.
- Real Gulf lender consent, expensive sustained war, actual debt, Khuzestan integration and Kuwait crisis systems. Merge duplicate unlock focuses without deleting those decisions or their costs.
- Shared infrastructure, literacy and ordinary development that a country can credibly pursue together. Do not invent permanent exclusivity between every useful pair of investments.
- Distinct national gains versus government-bound policy rewards, current policy revision, and save-safe earned receipts. New exclusivity must not make a later elected government permanently unplayable.

## Actual main-MD structural references

`00_generic.txt` has 158 focuses in the inspected source. GENERIC_political_games and GENERIC_the_state use separate prerequisite blocks to require both contributing reforms. The economy mixes complementary infrastructure branches with genuinely exclusive choices such as subsistence/commercialized agriculture. Its common choice spacing is 2 grid units (for example decentralization/centralization), with 1-row steps.

`05_russia.txt` has 806 focuses. Putin economics branches from a common spine into differently shaped and different-length state-corporatist/oligarchic programmes; SOV_state_corporatism, SOV_oligarchic_republic and SOV_combined_economic_system are the actual multiway economic alternatives, followed by further route-dependent developments. SOV_young_guard/reform_sovfed and SOV_putinism use meaningful AND joins. These examples justify varied programme footprints and real choice consequences, not copying Russian political institutions or imposing one universal focus count.

## Evidence and limits

Independently parsed current emitted code and compared all 426 coordinates, grouped prerequisites and exclusions against approved_iraq.json. The installed render report source hash for Iraq predates later writing/presentation edits, but its coordinates, groups, exclusions and every Iraqi/new-US card title still match current code/localization exactly. Inspected the full IRQ overview and native-scale Baath, Bakr, Saddam, Communist, KDP, oil, industry, defence and Iran-war images, plus the US chapter with existing defence neighbours. All are locked-state render approximations using native art/cards/font; connector routing and actual in-game hover/camera behavior were not verified. The cropped neighbouring cards at the image edges are preview crops, not a claimed native clipping bug.

Exact source hashes, IDs, existing coordinates, proposed oil coordinates and findings are in [structure.json](structure.json).

## Suggested next revision order

1. Fix governing/opposition contradictions and make the chosen oil implementation matter.
2. Rewrite the guard/general-staff and Front/monopoly forks as strong multistep commitments; recalibrate actual effects with main-MD reference examples.
3. Replace ceremonial finale rewards and remove two Iran support unlock-only cards by merging their decisions into the war plan.
4. Resolve war-aim and constitutional contracts, then add only meaningful new current-policy exclusions.
5. Adjust icon diversity and any remaining whitespace after the mechanics stop generating identical silhouettes.
