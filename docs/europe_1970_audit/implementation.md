> **Archived CWEC material.** The custom system was removed on 18 October 2026. [Native MD restoration status](native_restore.md) supersedes the implementation claims below.

# European Communities 1970 — implementation and operation

The 1970 campaign now uses an isolated `CWEC_*` ruleset connected to MD's canonical `EU_member` status and native weekly economy. New in-game text is English only. The research and design documents in this directory remain background material; this file describes what the code actually implements.

## Start and interface

Start a **new 1970 campaign** with the European Union system enabled. France, West Germany (`GER`), Italy, Belgium, the Netherlands and Luxembourg form the European Communities. The assembly has 142 seats and the Council starts with 4/4/4/2/2/1 weights. The chair rotates every 26 weekly ticks.

Use the existing European interface button or **Shift+I**. Opening explicitly selects Members using native-style country page flags. Its seven tabs are:

- **Members:** actual members, national seats, Council weights, GDP, human/AI status and the rotating chair. Hover a country for its annual assessment and payment ledger.
- **Assembly:** the full assembly, human delegations, frozen ballot representation and mandate confirmations.
- **Budget:** funded cash, reserves, allocations, arrears and persistent national payment ledgers. Hover the national ledger for project location/progress, sector effects and EIB accounts.
- **Ballot:** proposal, procedure, remaining time, participant list and Yes/No/Abstain controls.
- **Ledger:** the last 52 campaign weeks, showing actual contributions, CAP/research payments, completed works, administration and closing/current cash. Hover a row for project cofinance and escrow.
- **Treaties:** all 51 policy, budget, treaty and accession proposals, with descriptions, costs, procedures, native prerequisite checks and direct Submit controls. A second list records enacted acts. Locked proposals remain visible with their reason.
- **Projects:** 14 direct national actions for grants/construction, EIB accounts, arrears, implementation, Schengen, accession applications and withdrawal. Button tooltips show the actual decision rules and costs.

The country ledger retains former members. The weekly journal traces money through the common pool and programmes; it does not attribute each grant to a fictional individual donor.

## Player authority and adoption

Political proposals are opened directly in **Treaties**; **Decisions → European Communities** remains an alternative entry point. Both use the same docket and law/finance application code. The GUI adapter revalidates actual decision eligibility and pays 35 PP, or 50 PP for admission, only after the docket successfully opens. At least **two human member countries** are required to open a political docket; the catalogue and explanatory status remain visible with one player.

Every docket freezes its human countries, Council weights and national seats at opening. AI members remain contributors and programme beneficiaries, but have no political ballot, veto, ratification or party-popularity contribution. Hotjoining a different country affects the next docket. Disconnecting does not delete an already cast vote or lower the denominator. A withdrawn country cannot cast further ballots; the frozen denominator remains until that docket closes.

Each stage has four weekly ticks. Ordinary Council decisions require at least two thirds participation, two thirds of frozen Council weight voting Yes, and more than half of frozen countries voting Yes. Treaties require every frozen human member to approve, followed by explicit unanimous national ratification. Missing replies and abstentions cannot ratify a treaty. Timeout closes an incomplete docket as failed.

Before parliamentary reform, the assembly is consultative. The direct-election settlement grants parliamentary consent over common budgets; Maastricht extends binding parliamentary consent to ordinary legislation. Parliamentary consent requires a majority of frozen human seats and the same country participation quorum. The ratification stage remains separate.

Direct elections use **human national delegation confirmation**, with a new cycle after approximately 260 weekly ticks once the previous confirmation has finished. This is an RP representation system; national party popularity and AI elections do not allocate the legislative votes.

## Selectable historical and alternative paths

The catalogue includes own resources, a regional development fund, Euratom/civil research, direct elections, the Single European Act, Maastricht, monetary cooperation, political union of sovereign states, environmental legislation and democratic compliance review.

Historical dates are displayed as references. Players may agree an alternative timetable when the legal prerequisites are satisfied. Accession is available for 30 named countries, including the historical 1973, 1981, 1986 and 1995 enlargement countries, later eastern candidates and alternatives such as Norway, Switzerland and Turkey. A human applicant must explicitly request negotiations; the final admission rechecks existence, independence, peace, parliamentary eligibility and consent. Accession grants no territory or faction leadership.

Seat profiles are enacted rather than switched automatically by date. Actual membership determines the total:

| Profile and membership | Seats |
| --- | ---: |
| 1970 founding six | 142 |
| Add UK, Denmark and Ireland before direct-election reform | 198 |
| 1979 profile, nine members | 410 |
| Add Greece | 434 |
| Add Spain and Portugal | 518 |
| 1994 profile, twelve members | 567 |
| Add Austria, Finland and Sweden | 626 |

Alternative members receive explicit national allocations or a small fallback allocation. Only actual human delegations enter parliamentary ballot denominators. Civil-war splinters do not receive another national delegation while the original member exists; a victorious replacement retains its original country's profile.

Schengen has separate agreement, convention and implementation treaties, followed by national participation. Human members explicitly opt in. AI economic participation follows historical cohorts after player adoption; the UK, Ireland and Cyprus are not automatically enrolled. A player's explicit opt-in survives a later change to AI control. Participation can be left separately from Community membership.

The **European Union name** can be adopted alone. Maastricht also adopts that name and grants the additional parliamentary powers. Political union preserves national governments as playable states. The modern MD annexation, unified fleet/army and automatic faction-transfer paths are outside this ruleset.

Monetary cooperation preserves national currencies. It narrows the native monthly currency movement band to -0.5%/+1%, before any gold/silver parity correction, and adds a trade-opinion benefit with a political-power cost. A modern euro currency is not automatically introduced.

## What the common budget actually does

All amounts use MD **billions**. The initial annual assessment is calibrated to **0.25% of aggregate member GDP**, with the 1970 founding contribution keys. The own-resources settlement changes the assessment basis to GDP shares. Separately ratified contribution settlements permit 0.15%, 0.25% and 0.35%.

This is an explicit game-economy approximation: customs duties, agricultural levies and VAT resources are not individually extracted from separate customs accounts. The assessment rate is a balance parameter, not a claim to reproduce every historical budget figure.

The initial allocation is CAP 70%, research/Euratom 20%, administration 10%. Three selectable budget settlements offer agriculture, cohesion and research priorities. A changed allocation affects **new receipts**; it does not rewrite previous transfers or spend committed funds twice. Regional funds remain reserved until the regional programme is authorized.

The weekly flow is:

1. Prepare funded awards from the opening reserves. The first week has no fabricated starting grant pool.
2. Compute national assessments and cap current contributions to available liquidity, rechecking after project matching funds. Unpaid assessments become arrears.
3. Add contribution expenses and earmarked programme income/expenditure to MD's normal `treasury_rate` calculation.
4. After native weekly treasury accrual, record the same actual contribution as a common-fund receipt, once per country/week.
5. Record funded CAP/research payments and programme spending, then update reserves, effects, national ledgers and the weekly journal.

UI refreshes and recalculation do not settle cash. New receipts are usable for the next preparation cycle. Rounding remainders stay in disclosed administration reserves; payment preparation is capped to funded balances.

The common-fund accounting identity is:

`cash = settled contributions + net national project cofinance - programme payments - full project procurement - administration`

`cash = CAP reserve + regional reserve + research reserve + administration reserve + project escrow`

CAP and research transfers are **earmarked pass-through receipts**, paired with national programme expenditure. They are not disposable treasury gifts. Real funded CAP payments increase native agricultural productivity; real research payments support a capped research-speed effect. These effects decay without continued funding. The expanded research programme raises the research support ceiling. Regional envelopes favour lower GDP per capita and consider population.

Infrastructure contracts use the existing MD price: **3.50 billion**, including **2.625 billion Community grant and 0.875 billion national match**, with 52 weekly ticks of construction. An eligible owned and controlled state below infrastructure level 6 is selected and displayed. Both shares must be funded before construction begins. Completing the contract adds one real infrastructure level and consumes escrow. Losing control, withdrawal or a filled building cap cancels the contract and reverses the unspent funding. Non-compliance pauses construction. No investment-portfolio asset is manufactured for a public grant.

Administration consumes real cash. Holding an office does not receive the administration budget as a national subsidy.

## Compliance and national consequences

Adopted common legislation applies to members within the agreed competencies. Relevant implementation decisions give human governments 26 weeks to implement a new law. AI economic administration follows adopted law without an AI political vote. A new treaty does not erase existing non-compliance.

Single-market rules provide productivity-growth/trade benefits with coordination and recurring administration costs. Environmental rules trade administration costs for a stability benefit. Maastricht adds parliamentary powers and coordination benefits with political and financial costs. Non-compliance removes relevant benefits, blocks programme eligibility and, after democratic oversight is authorized, adds an institutional stability penalty. National implementation restores eligibility; no compliance action transfers territory or imposes a regime.

Withdrawal takes 180 days and leaves a three-year readmission cooldown. Historical payments and arrears remain in the ledger.

## Separate EIB balance sheet

In **Community Finance and EIB Accounts**, members can subscribe real national cash as bank equity. The EIB begins without fictional liquidity. A development loan is paid only from subscribed bank liquidity, booked as a bank receivable and a national official-creditor liability.

A contract is 0.10 billion, with approximately five years of principal repayment and 3% annual interest using native weekly-interest scaling. Payments are real national expenses and actual bank receipts. Remaining principal can be repaid early. Withdrawal does not erase the loan; a destroyed borrower produces a disclosed write-off.

EIB liabilities are deliberately separate from the generic market-debt variable, following the mod's official-creditor pattern. They are shown in the Community finance tooltip and are not also charged native market interest or erased by automatic market-debt repayment. The normal MD market-debt display remains the market-debt account.

## Files and repeatable checks

New gameplay files use `CWEC_*`. Native integration is limited to the EU initializer/member hooks, legacy political result guards, monthly/weekly hooks, national income/expense and currency calculation, the existing launcher/legacy visibility, and two English status strings. `tools/europe_1970/integrate.py` makes these surgical edits idempotently and preserves unrelated workspace edits.

Regenerate content only when changing its data source:

```powershell
python tools/europe_1970/content/generate_content.py
python tools/europe_1970/content/generate_proposal_ui.py
python tools/europe_1970/generate_interface_actions.py
python tools/europe_1970/generate_seats.py
python tools/europe_1970/write_localisation.py
python tools/europe_1970/integrate.py
```

Validation:

```powershell
python tools/europe_1970/validate.py
python tools/europe_1970/validate_voting.py
python tools/europe_1970/validate_integration.py
python tools/europe_1970/validate_ui.py
python tools/europe_1970/validate_membership.py
python tools/europe_1970/validate_proposal_ui.py
python tools/europe_1970/validate_interface_actions.py
python tools/europe_1970/check_original_md_reference.py
```

The checks cover financial conservation, duplicate settlement, rounding at small payment amounts, projects, withdrawals, annexations, bank accounting, actual-script voting thresholds/stages/controller changes, seat profiles, English BOM/localisation references and byte-idempotent native integration.

**HOI4 engine execution, visual inspection, save/load and a real multiplayer/OOS test have not been performed.** Runtime validation should use a new 1970 game with two human founding members, one AI member receiving payments, an applicant, a budget change and a funded project. Check the engine error log, UI layout, a save/reload during ratification, disconnect/rejoin, and weekly native/shared cash changes. Existing modern-EU saves are not a supported migration target.

## UI and membership correction

The user's real engine log exposed five unregistered page types. Pages are now top-level GUI types attached through their own scripted controllers, with independent visibility gates and controls bound to the controller that owns them. A regression test reproduces the original nested-window failure and checks that only one of the five pages can be shown.

Membership now directly grants its real baseline: 5% trade opinion and 1% stability, with a 3% political-power coordination cost. It has no ideology drift. The obsolete visible compensation modifier is disabled and removed; no start year appears in its fallback title. The separate Community Programmes modifier exists only while a funded programme or enacted policy has a real nonzero effect.

Existing CWEC campaigns repair these obsolete modifiers and refresh institutional data when the European interface is opened, at startup and during monthly maintenance. Repair does not reset money, proceedings, funded projects or the payment journal. The scalar dynamic-modifier removal syntax reported by the engine is corrected to its native parameter-block form.

The revised UI and effects require a full game restart to reload their definitions. The Computer Use inspection was stopped by the user before the revised definitions could be loaded and visually verified. The earlier game logs are evidence of the original defect, not proof of a successful run of the correction.

## Original MD system guard and direct interactions

The original reference is `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`, read-only. The dedicated original-system agent has reviewed the proposal, list-scope, page, finance and action adapters against native MD. Its detailed mapping is in `original_md_compatibility.md`; `original_md_reference_manifest.json` fingerprints 21 reference files. The normal reference-check command only reads the installation and warns if the reference changes. Updating the manifest is a separate explicit operation, never a write into the original mod.

The recorded 1970 startup confirms six members, 142 seats, one human member and GDP 2216.15916. The blank page was not evidence that these institutional data were missing. The previous UI had no explicit default page and exposed no direct proposal list. The flag-based default, two new action pages and adopted-act list address those concrete gaps.

Annual national assessments are now computed as a pure preview before the first weekly settlement. Paid balances remain zero until a real payment; an empty journal explains this rather than showing unexplained emptiness. National UI actions are generated from the actual decision eligibility and effects, including the same political costs. Withdrawal uses a shared 180-day event so the direct UI has the same notice period as the decision.

This integrates the selected 1970/RP paths. Modern AI party-vote machinery, post-1970 office campaigns, OMT/ECB interventions and military/annexation endgames are not silently re-enabled. The original comparison explicitly records which modern features do not yet have a separate historical implementation.
