# COLDWAR_IRQ — Iran: Road to War

18 October 2026. Approval concept only. Adds 30 focuses, eight decisions and seven proposed campaign ideas to the existing Iraqi concept. Nothing is installed in loaded game directories. All values are balance proposals; source support does not establish live budget or combat balance.

## Territorial demand and historical setting

The claim is on **Khuzestan, state399**, called Arabistan in Iraqi nationalist rhetoric. This is a disputed Iraqi demand, not a declaration that the province was rightfully Iraqi or that its population supported annexation. The Shatt al-Arab dispute is represented separately. The existing1970 state file makes Iran owner/controller, contains11base oil, and gives PER/ARA cores; Iraq has no core. Its dated1970 building overrides must be read instead of advertising the larger2000 economy.

The river dispute was already acute in1969: Iran repudiated the1937 treaty and challenged Iraqi inspection/navigation demands. This permits a1970 escalation path without pretending that Iran had already experienced its1979 revolution. [Contemporary INR analysis,22April1969](https://history.state.gov/historicaldocuments/frus1969-76ve04/d12).

The1975 Algiers agreement exchanged Iranian withdrawal of support for Iraqi Kurds for a boundary settlement in the river. A player can pursue a tactical settlement and later repudiate it, but must relinquish its actual reciprocal benefits. [INR retrospective,1976](https://history.state.gov/historicaldocuments/frus1969-76v27/d306). Claims to Arabistan and the later decision to attack appear in the [US Army historical account](https://webdoc.sub.gwdg.de/ebook/p/2005/CMH_2/www.army.mil/cmh-pg/books/www/www1.htm).

Baghdad had reasons to consider military action feasible: oil finance, an expanded army and a perception that Iranian revolutionary turmoil offered an opening. It also had shortages of skills and reliance on imported support. Those strengths and limits motivate funded command, spares, industry and an optional crisis-intelligence decision. [National Intelligence Estimate,21June1979](https://history.state.gov/historicaldocuments/frus1977-80v18/d137). Iranian revolutionary pressure and Iraqi counter-subversion are documented, but neither Iraqi Shia disloyalty nor Iranian Arab cooperation is automatic. [CIA assessment,March1980](https://history.state.gov/historicaldocuments/frus1977-80v11p1/d205).

## Exact position and progression

The new sector root is **(94,15)**, right of the existing war sector. Its full footprint is x90..98,y15..30. Earlier396focus coordinates, IDs, rewards and prerequisites are preserved. The continuous panel moves below the enlarged tree to(0,4300), and a ninth native-style shortcut targets the new root. The browser opens this sector for inspection; the proposed1970 game still begins with al-Bakr.

The two upper lanes assert the river policy and grant the Khuzestan claim, then develop command and intelligence. Their AND-join leads to the operational plan. The central exclusive fork selects **A Short Sharp War** or **Prepare a Long War**. Forward logistics or mobilization contracts lead through an OR-join to **The Final Ultimatum**. Gulf credit and external suppliers are optional side spurs: another player's refusal cannot veto the claim, war goal or attack.

After actual war participation, **The Campaign Ledger** remains completable in peace. A quick victory therefore does not lock the province's administration behind restarting a war. **Secure Khuzestan** leads to funded oil infrastructure, local administration and **Arabistan Secured** after a real peace settlement. **Fight Through Attrition** leads to reserves, renewed offensives and **Victory at Any Cost**. Neither route forces a ceasefire or Iranian surrender. Players may still negotiate through normal diplomacy.

## Why the Iraqi player might attack

**The Arabistan Claim** grants `add_state_claim = 399` and five percentage points of war support. **The Final Ultimatum** grants a180day `take_state_focus` war goal against PER with `generator = { 399 }`, alongside native threat generation. It does not ask Iran for permission or transfer the province. The player declares war through normal diplomacy.

The short-war plan allows a once-only paid opening spirit: **+8%attack against PER, +15%planning speed for90days**. It costs a frozen2%GDP invoice and75PP, and increases supply use8% and army fuel use10%. The sustained plan instead offers **+5%attack against PER, +10%planning for120days**, with supply+5% and fuel+6%; its funded industry and war-production programme provide greater replacement capacity. Targeted attack works against PER forces anywhere; planning, supply and fuel effects are country-wide. Both openings create **+8%army personnel expenditure for180days**, including after an early peace.

Preparation can provide command cohesion, supply organization, fuel discipline, real army experience and one paid military factory on the sustained lane. Optional Gulf credit remains a real loan with a consenting creditor and repayment. No focus invents divisions, ammunition, air superiority or an Iranian military collapse.

The territorial prize is actual access to the province's existing oil, port and land through native conquest/occupation/peace mechanics. No duplicated11oil grant is issued. After ownership and control, a paid infrastructure level and infrastructure3 qualify a **national oil export revenue multiplier+10%, bureaucracy expenditure+6%** programme. This is an additive national export multiplier, not10%extra provincial production or a guaranteed income increase. Occupation, damage, price and embargo rules remain. Civil administration gives five percentage points of local compliance once, without a core. Actual territorial success and peace qualify100PP plus a conditional regional-influence programme.

## Alternate-history core integration

After Arabistan Secured, A Provincial Settlement leads to the reciprocal Equal Citizenship/Central State Rule choice, then an OR join into An Iraqi Province at(92,30). Civic integration costs4%GDP and grants12compliance points once, with bureaucracy+6%/social expenditure+4%. Central integration costs2.5%GDP and grants6points once, with ideology drift defence+8%, bureaucracy+3% and stability-3points. Both policies keep their costs while Iraq owns and controls399, including after coring. The initial settlement costs2%GDP with administrative/political costs.

The final70dayfocus charges a frozen6%GDP invoice and executes `399 = { add_core_of = IRQ }` once. It requires Iraq to own and control the non-core state continuously for730days, peace withIran, infrastructure>=3, compliance>=60 and resistance<15. The hold timer starts on actual acquisition/control rather than focus completion, resets on losing ownership/control, and survives peace and party changes. Compliance/resistance qualify delivery; they are not subsequently used to remove the earned core or its programmes. Existing PER/ARA cores remain; no additional resource/population grant accompanies it.

These thresholds and the core outcome are explicitly alternate-history balance proposals. Native syntax is evidenced by MD`common/decisions/Iraq.txt:37-39,110-112` (state-scoped Iraqi core), MD`common/decisions/Thailand.txt:1074-1080` (0-100compliance/resistance), and this checkout's `common/scripted_effects/ISR70_policy_effects.txt:1128-1141` plus `common/scripted_triggers/ISR70_policy_triggers.txt:7-9` (continuous ownership clock). The observer additionally needs actual `on_state_control_changed` and authoritative peace/transfer calls so brief losses cannot evade reset. No engine runtime test is claimed.

## Long-war risk and lifecycle

The first observed Iraq–Iran war opens a30day activation window. It expires permanently even if the player missed preparation. Neither a new government, save/reload, a second war nor reconciliation resets the first-war/consumed flags. Operational ideas cancel at peace and retain their original timed expiry; fixed-duration bills remain payable.

After180continuous war days, an automatic burden adds **supply use+8%, army personnel expenditure+12%, stability−4points** until peace, regardless of completed focuses. After90days, a renewed offensive may be funded for3%GDP and100PP: +5%attack against PER for60days, supply/fuel+12%, plus a90day+12%personnel bill. It has a180day cooldown, cannot overlap an opening or another renewed bonus/bill, and may coexist with remaining initial mobilization obligations. Continued mobilization can increase output further at explicit civilian, personnel and stability costs.

`COLDWAR_IRQ_IRAN_CAMPAIGN_SPECIMEN.txt` gives the new observer proposal: actual-war flags, first-window expiry,180day attrition, guarded peace cleanup and executable requests to the concept's new reconciler. War transitions refresh once per observer call. Earned territorial packages cause guarded daily reevaluation of current control, ownership and infrastructure. Claims, buildings, compliance, cash and war support never replay during refresh. `active_requires` expresses current programme qualification separately from one-time completion gates. It does not substitute for earned/selected-package checks.

Implementation still needs real daily/war/peace/load hooks, the paid decision wrappers, settlement-provider synchronization, offered credit/supply contracts, native tooltips and engine tests. The specimen declares these as new integration, not pre-existing MD APIs. No HOI4 or multiplayer test has been claimed.

## Native mechanic evidence

Paths marked MD refer to `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`; other paths refer to this checkout.

| Mechanic | Source evidence |
|---|---|
| Correct territory and1970 overrides | `history/states/399-Khuzestan.txt:2–5,46–47,80–98` |
| Claim399 | MD`common/national_focus/05_syria.txt:11613` |
| State-targeted conquest goal | MD`common/national_focus/05_china.txt:12331–12335` |
| Effect-level war-goal expiry | MD`common/national_focus/05_poland.txt:4698–4701` |
| Native threat helper/type2 | MD`common/national_focus/01_EU_USoE_shared.txt:1118`; `common/scripted_effects/00_scripted_effects.txt:2604` |
| PER-targeted attack | `common/ideas/Iraqi.txt:1697–1703` |
| Planning, supply and personnel expenditure | `common/ideas/Iraqi.txt:1237,988,1388–1390` |
| Army fuel | MD`common/ideas/05_china.txt:1591` |
| Timed idea and peace cancellation | MD`common/decisions/00_antarctica_decisions.txt:64`; MD`common/ideas/arab_spirits.txt:732–745` |
| Flag-age trigger | `common/decisions/05_CHI_decisions.txt:4487` |
| Oil export and bureaucracy consumers | `common/scripted_effects/00_money_system.txt:4503–4527,3300–3312` |
| Non-core/compliance resource access | MD`common/modifiers/00_static_modifiers.txt:185–200` |
| Undamaged infrastructure resource factor | `common/defines/MD_defines.lua:285` |
| Compliance percentage points | MD`common/national_focus/05_china.txt:399–409` |
| Infrastructure reward pattern | MD`common/national_focus/05_iraq.txt:2555–2567` |

Independent historical research, a separate modifier/mechanics review and a separate geometry/render review informed this revision. Current review fingerprints and actual browser results are recorded beside the concept; previous reviews retain their original revision boundary.
