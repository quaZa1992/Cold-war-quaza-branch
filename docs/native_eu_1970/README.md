# 1970 European Communities inside the native MD interface

> **Removed at the user's request.** This implementation is archived and no longer loaded. The [main MD EU restoration record](../main_md_eu_restore/README.md) describes the current active state. Its generators and validators were archived and removed as well.

The Cold War adaptation now extends the original Millennium Dawn EU implementation. It uses the existing office, state-information, Parliament, Council and fiscal screens. `interface/eu.gui` and `interface/eu.gfx` remain byte-identical to the reviewed original MD files. No replacement GUI, page hierarchy or parallel legislative docket is loaded.

All new in-game localisation is English. The original Workshop installation is a read-only reference.

## Where to find the features

1. Open the usual European interface, using the existing top-bar button or **Shift+I**.
2. The existing **Parliament** reform list contains the 53 original MD proposals and 118 added historical/alternative rows. Locked rows explain prerequisites. New proposals cost 200 PP once in Parliament. Their subsequent Council submission adds no second proposal charge.
3. The existing Parliament **Support/Oppose** controls cast the player's national delegation vote. Approved proposals enter the original Council queue.
4. Use the existing **Council** Support/Reject controls to vote. Approved acts enter the original enacted-law list and apply their real effects.
5. In **Common Budget**, the original contribution and spending controls prepare a draft. The original side panel switches between national contributions and distributions. Hover its country rows or the total-budget heading for enacted assessments, actual payments, category funding, cumulative records and the common reserve.
6. In **Offices**, nominate the Commission or Assembly president with the existing office buttons. The nomination opens an office ballot in the existing Council window. The rotating Council chair is assigned administratively for approximately six months.
7. Existing European decision categories contain national applications, Schengen participation, funded regional/research requests, physical infrastructure projects and EIB capital, borrowing and repayment actions.

One human can inspect everything and prepare a budget draft. Opening political proceedings requires at least **two human member countries**. Each human first confirms a national delegation through the mandate event. AI countries retain economic membership and display delegations but cast no political vote.

## Historical start and selectable development

The native `EU_member` idea and `global.EU_member` array remain canonical. The 1970 start initializes Belgium, West Germany, France, Italy, Luxembourg and the Netherlands. Their appointed delegations total 142 seats. Membership carries a modest political administration cost, trade goodwill and stability, with no ideology drift or compensating membership spirit.

The original proposal arrays, missions and dispatchers carry own resources, EPC, the European Council, direct elections, regional development, Werner cooperation, the currency snake, EMS, the Single European Act, Maastricht, Amsterdam, Nice, staged Schengen, research/Euratom, energy solidarity and alternative intergovernmental/political-union paths.

The European Union name is a **separate selectable act** after Maastricht. It updates the existing title, membership label and institutional country name. Its cosmetic flags reuse the original EU artwork unchanged.

Eight enlargement frameworks authorise candidacies. An individual accession vote then requires a live national application, peace, an independent eligible government and human approval. All 88 non-founder countries in the original MD availability collection have individual admission rows, preserving internal, microstate and extended eastern possibilities. Framework approval alone grants no membership. Admission grants no territory, faction leadership or NATO transfer. Withdrawal cooldowns and fresh approval apply on re-entry.

National seat allocations feed the original 24-party arrays. Adopted institutional settlements, rather than the calendar, choose the allocation profile. Actual membership determines the total. Verified historical combinations are:

| Membership and adopted settlement | Seats |
| --- | ---: |
| Founding Six | 142 |
| Add UK, Denmark and Ireland, appointed delegations | 198 |
| Direct elections, nine members | 410 |
| Add Greece | 434 |
| Add Spain and Portugal | 518 |
| Edinburgh settlement, twelve members | 567 |
| Add Austria, Finland and Sweden | 626 |
| Nice allocation, twenty-five members | 732 |
| Lisbon allocation, twenty-eight members | 751 |

Unlisted alternative states receive capped population-based game allocations. These are explicit gameplay approximations rather than claimed historical quotas. Original modern agendas remain available behind historical prerequisites. The original federal endgame requires explicit unanimous human approval and cannot annex a newly joined human country outside that ballot.

## Player voting in the native procedure

The flow remains `EU_potential_votes` → native Parliament mission → `EU_council_votes` → native Council mission → `EU_passed_votes`.

Electorates, national seats and Council weights freeze when a ballot opens. AI party popularity and lobbying do not produce legislative support. Late joins affect the next ballot; disconnects do not shrink the existing denominator or create consent. A missing response cannot ratify a treaty. Native timers close incomplete ballots.

Before Maastricht, the Council uses the historical weight model: at least 12/17 of frozen weight and two thirds of frozen countries. With all six founding governments human, this gives 12 weighted votes and four countries. Later ordinary proceedings use MD's population/state double majority, normalized to the frozen human electorate. Treaties, accession and major constitutional proposals require unanimity. Office elections use a majority of frozen human countries.

These are multiplayer RP rules built into MD's existing procedure, not an exact simulation of every historical treaty's legislative competences. The Assembly stage remains part of the native workflow before direct elections.

## Money, benefits and obligations

Amounts use MD billions. The initial common assessment is 0.25% of aggregate member GDP, allocated through the founding contribution key. Own resources switches the assessment basis to GDP shares. The original four spending headings remain adjustable; the starting shares are Growth 15%, CAP/Natural 75%, External 2% and Administration 8%.

Budget999 commits spending shares. Financial-framework998 commits contribution rates. Each uses the other side's last enacted snapshot, so concurrent or rejected drafts cannot change actual funding.

Weekly clearing collects only available national cash, funds grants from actual common liquidity and retains unused funds in the common reserve. Both contributions and grants use annual amounts divided by 52. The existing national weekly budget remains the sole recurring treasury settlement; nominal transfers are booked after domestic inflation to avoid overcharging. GUI recalculation never transfers cash.

Existing fiscal tooltips distinguish proposed amounts from enacted obligations and actual cash flows. They show last-week payments, shortfalls, category receipts, net transfers and cumulative contributions/grants. Agricultural productivity, regional construction, research and energy effects depend on actual funding and fall with underfunding. Policy obligations have explicit continuing political costs and no party-popularity effects. National treasury receipts proxy economic programme/procurement flows in MD's economy; they are not an exact tax-accounting model.

A regional infrastructure project costs 0.05 bn national cash plus 0.05 bn common cash and creates one real infrastructure level in an eligible owned, controlled state, at most once per country per year. EIB subscription transfers actual capital into a separate bank balance sheet. Loans transfer existing bank cash, create matching principal liabilities and charge 2% annual interest. Withdrawal preserves the loan and cumulative records while removing current Community benefits.

## Verification and loading

The scripts have passed content, voting, finance, complete native-flow, core and cross-file checks. These execute actual scripted actions and thresholds using bounded test interpreters. They cover all 88 admissions, complete Parliament/Council enactment, seat growth, inflation, shortages, 52-week cash conservation, EIB claims, exits and draft isolation. Native interface bytes, GUI component/list bindings, reviewed Workshop files and unrelated local work are checked separately.

The newest rendering and a live multiplayer session have **not** been tested in the game engine. Fully restart HOI4 and start a **new 1970 campaign**. Existing CWEC saves and campaigns initialized under the restored modern MD startup are not migrated.

Run `python tools/native_eu_1970/integrate.py` to apply the idempotent native adapters, followed by the `validate_*.py` scripts in that directory. The original pre-extension native files are preserved in `native_before_extension.zip`, with hashes in `baseline.json`. The separate earlier CWEC rollback backup remains archived under `docs/europe_1970_audit`.

## Historical references

- [European Parliament historical background](https://www.europarl.europa.eu/factsheets/en/sheet/11/the-european-parliament-historical-background): appointed Assembly, direct elections and successive seat totals.
- [European Parliament historical archives](https://historicalarchives.europarl.europa.eu/home/fonds/parliamentary-activities.html): appointed national delegations and direct elections from 1979.
- [European Parliament seat-allocation report](https://www.europarl.europa.eu/doceo/document/AFCO-PR-502178_EN.pdf?redirect=): the 732-seat national allocation.
- [European Parliament 2014 seat distribution](https://www.europarl.europa.eu/news/en/press-room/20130610IPR11414/valet-2014-fordelning-av-mandat-mellan-de-28-eu-landerna): the 751-seat allocation.
- [Council history of the EU budget](https://www.consilium.europa.eu/fr/eu-budget-story/): the own-resources settlement and development of parliamentary budget powers.
- [Council presidency history](https://www.consilium.europa.eu/en/council-eu/presidency-council-eu/timeline-presidencies-of-the-council-of-the-eu/): rotating six-month presidencies.
