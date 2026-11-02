IMPERIA COLD WAR
# Universal SSR focus programme: approval concept

Revision 2: 25 October 2026. This is an unapproved design and interactive concept. It installs no focus tree, idea, event, decision, localisation or history patch.

The common programme requires **actual recognised SSR status only**. It has no communist-party, outlook or Soviet-government requirement. If the Union changes political direction but remains intact, its republics retain all common SSR content. The January 1970 First Secretaries remain the historical starting leadership, rather than a permanent condition on later government.

## One tree, national modules

The proposed `COLDWAR_SSR_1970_focus` is a single universal tree for UKR, BLR, MLV, EST, LAT, LIT, GEO, ARM, AZE, KAZ, UZB, TRK, KYR and TAJ. Its common core is defined once. Regional, specialisation and political modules use country-namespaced focus IDs. Static country selection chooses the relevant republic's political and regional modules; **no party-dependent `allow_branch` hides political alternatives**. Per-country views contain 262 to 312 new focuses, including 162 SSR focuses, plus the 17 existing Union Plan focuses. All 14 republics receive all nine identical specialisation alternatives. Historical production profiles confer no eligibility restriction or different reward.

The RSFSR was also a Union republic. In this scenario the SOV country represents the Union centre and already has its own substantial tree. This proposal preserves that architecture. It does not equate ASSRs with Union republics or replace SOV's existing content.

| Chapter | Absolute root | Focuses | Eligibility |
|---|---:|---:|---|
| Republican Administration | (8, 0) | 15 | SSR status |
| Republican Economy | (20, 0) | 16 | SSR status |
| Society and Institutions | (32, 0) | 14 | SSR status |
| Union Defence Contribution | (44, 0) | 14 | SSR status |
| Regional Priorities | (56, 0) | 4 | SSR status; correct republic |
| Existing Union Plan | (70, 0) | 17 existing | Existing Union Plan participation rules |
| Nine Union specialisations | (6 + 10 x programme index, 14) | 11 each, 99 total | SSR status; one primary programme |
| Sovereignty and Statehood | (8, 26) | 11 | Actual independence |
| Economic Transition | (20, 26) | 14 | Actual independence |
| Independent Defence | (32, 26) | 9 | Actual independence |
| Independent Foreign Policy | (44, 26) | 9 | Actual independence; suitable recipients for offers |
| Political programmes | (6 + 12 x programme index, 39) | Country-specific | Actual independence and exact governing party |

Ordinary two-way choices use native offsets of two or three columns and one-row steps; wider diplomatic footprints have their own reserved lanes. Independent chapters can be started without completing any SSR focus. A successful unilateral independence transition can activate them; Soviet permission is not a permanent domestic-content requirement. The existing political, succession and independence systems continue to decide who governs and whether a country is actually free.

`DESIGN.json` is the exact position/effect/requirement catalogue. Every focus records grouped prerequisites, reciprocal exclusions, native-grid coordinates, earlier relative anchors, cost, duration, modifier keys, setup costs and any assets. `FOCUS_CATALOGUE.md` is its complete readable counterpart. Ordinary cost 5 is 35 nominal days; larger projects use cost 7 or 10. The engine's inspected `FOCUS_POINT_DAYS` is 7.

The initial camera targets `COLDWAR_SSR_secretariat`. Sector and aftermath shortcuts are recorded in the manifest. Continuous focuses reserve a 770 x 380 pixel window at (6100, 650), below the shared Union cluster. To reuse the existing joint tree, its new host needs a native conditional offset (-285, -8) from the current (355, 8) root. Existing SOV (355, 8) and generic (240, 0) host positions remain separate. This is a proposed generator integration, not an applied edit.

## Historical opening and policy choices

The January 1970 institutional basis is the 1936 Soviet Constitution as amended. The 1977 Constitution is a later comparison. Union authority over planning, foreign trade and defence explains the common republican administration and economic programme. The 1944 legal provision for republican military formations did not create functioning sovereign armies in these republics. [1936 Constitution](https://seventeenmoments.web.illinois.edu/1936-2/stalin-constitution/stalin-constitution-texts/the-stalin-constitution/), [UN Yearbook on Human Rights, republican constitutions](https://digitallibrary.un.org/record/860913/files/1947-E.pdf).

Each republic starts with four common proposed spirits and one regional constraint:

| Common spirit | Initial modifiers | Main response |
|---|---|---|
| Plan Targets and Shortages | Military production efficiency cap -10%; civilian industry productivity -10% | Enterprise accounting, then investment settlement; independent industrial conversion also repairs an unresolved legacy |
| Republican Patronage Networks | Political power gain -10%; bureaucracy expenditure +8% | Professional audit or administrative discipline; independent judicial/executive reform can address an unresolved network |
| Soviet Social Guarantees | Stability +8%; social expenditure +10% | Service Settlement retains stability and lowers the expenditure modifier to +6% |
| Union Technical Network | Research speed +5%; supply consumption -5% | Requires continuing SSR status and operating links; independent cooperation must be negotiated |

Regional profiles cover industrial imbalance in Ukraine, Union orders in Belarus and Latvia, processing and agriculture in Moldova, Estonia's oil-shale costs, Lithuania's competing farm/factory needs, Georgian informal networks, Armenian imported inputs, ageing Azerbaijani equipment, Kazakh environmental burdens, Uzbek cotton/water dependence, Turkmen irrigation, Kyrgyz seasonal water/energy exchange and uneven Tajik investment. Regional Standards halves the specific constraint; it does not erase its historical legacy. Exact country values are balance proposals in the inspector.

Major SSR alternatives include central versus republican appointments, professional audits versus administrative discipline, Union military orders versus local reinvestment, industrial combines versus consumer supply, output incentives versus quality standards, new generation versus energy conservation, technical institutes versus vocational skills, collective-farm machinery versus household supply, and specialised Union orders versus pre-transition diversification. Both sides retain useful outcomes and a concrete fiscal, political, military or resource trade-off.

The economic choices draw on the 1965 reform debate over enterprise autonomy, incentives, quality and the limits imposed by the ministries. They are adaptable institutions, not a claim that every republic implemented every branch. [CIA contemporary assessment, NIE 11-5-67](https://www.cia.gov/readingroom/docs/DOC_0000272916.pdf), [CIA retrospective study of Soviet economic reform](https://www.cia.gov/resources/csi/static/Watching-the-Bear-2-Chap2-TheEconomy.pdf).

## Independence is a difficult transition

Actual independence suspends ordinary Union-dependent policy programmes and the Union Technical Network. The selected primary specialisation instead becomes an independent industrial or institutional legacy: each beneficial modifier and equipment bonus retains 20%, each adverse modifier retains 75%, and the weekly allocation falls to half its former GDP share, rounded to five decimals. These are balance proposals. National construction, earned experience, research bonuses and completed institutional reforms survive in full. Social guarantees and unreformed national problems remain. Early independence is fully playable: the independent branches can resolve inherited planning/patronage problems and improve an unreformed regional constraint without requiring inaccessible SSR focuses.

Three new spirits model interrupted production, payments, public administration and command responsibilities. The unscaled base is:

| Transition spirit | Base modifiers |
|---|---|
| Fractured Supply Chains | Military factory output -15%; civilian industry productivity -15%; construction speed -10% |
| Unsettled State Accounts | Tax revenue -15%; bureaucracy expenditure +15%; political power gain -10% |
| Unsettled Defence Administration | Division organisation -12%; training time +10%; army personnel expenditure +10% |

Country-specific severity factors are explicit in `rules.py`, rather than historical statistical estimates. Two supply preparations can each reduce the inherited supply liability by 25%. Civil registers and defence records can each reduce their own liability by 25%. A genuinely negotiated and operating transition applies a further 0.6 multiplier. The inspector shows exact country numbers for abrupt, prepared, and prepared-plus-negotiated separation.

Each liability has three distinct recovery receipts. One repair leaves two thirds of its initial penalty, two leave one third, three remove it. Receipts count independently of order. Five-decimal rounding is reconciled at removal. Union Supply Contracts adds a separate Unconverted Union Orders burden after independence: tax revenue -4% and civilian productivity -5%. Either export conversion or domestic supplier reconstruction removes it. Neither a timer nor an automatic civil war replaces player policy.

The historical precedent is the breakdown of contracts and payment arrangements, input shortages and loss of budget/price transfers, with large differences among republics. Those effects do not prove an identical 1970 counterfactual or inevitable conflict. [IMF, transition output decline](https://www.elibrary.imf.org/view/IMF084/05300-9781557755186/05300-9781557755186/ch02.xml), [IMF, Baltic stabilisation](https://www.elibrary.imf.org/view/book/9781557755193/ch01.xml).

## Political aftermath

Every selected country-specific political programme remains visible. Execution and programme activation require the actual registered governing organisation through the native exact-slot `*_are_in_power` trigger. Departure suspends that programme; return restores its earned modifiers without reissuing cash, buildings, research bonuses or experience. A party gets one accumulated dynamic programme, rather than a separate national spirit for every focus.

The roster distinguishes existing parties, exile authorities and underground organisations from alternate-history coalitions built around cultural, labour, religious or regional institutions. Writers' unions and ministries are not presented as legal opposition parties in 1970. Later counterparts such as Rukh, the Baltic fronts, Birlik, Erk or the Islamic Renaissance Party do not appear prematurely as established parties. Their eventual names can follow a genuine political formation or a documented alternate-history transition, without a redundant focus to unlock an already governing party.

The Ukrainian UPR centre, UHVR, URDP, OUN-M and OUN-B have separate dispositions. OUN-M's cooperative and commercial coalition and OUN-B's cadre-state alternative have different ownership choices, effects and costs; their historical liabilities are not converted into free superiority. Armenia distinguishes ARF security/diaspora mobilisation, Democratic Liberal commercial institutions, Hunchak labour/diaspora institutions and the National United Party. Georgian social democracy gets elected municipalities and cooperative follow-through. Lithuania retains a separate state-continuity route. Central Asian civic and conservative alternatives are explicitly counterfactual governing coalitions where the historical organisation was informal. Only Tajikistan has the selected optional civic religious programme; no Salafi or Shia filler is added.

All 69 programmes have an institutional identity and two country-specific signature focuses. The 55 non-communist organisations also have their own exclusive economic alternatives and associated follow-through. Constitutional authority and fiscal/social provision supply further exclusive choices. Anti-communist organisations have an optional archive-opening focus: it transfers 15% of current communist-party support to the actual governing organisation, with public-administration costs. This is a relative support transfer, not a ban, forced election or automatic government change. Public and market charters determine which national enterprise-settlement methods the government can execute. Government changes suspend a party programme and its charter; they do not reset settled enterprises or the national reform deadline.

## Universal specialisations

The roots at row 14 form one nine-way mutually exclusive selection. Each branch has eleven visible focuses and eight focuses on any completed route: entry, paid works, technical education, one of two directions and its follow-up, common coordination, one of two administrative settlements, then consolidation. All republics can select every programme. Maritime projects require an owned, controlled legal coast; Caspian access supports regional naval activity and does not guarantee access through the Volga-Don route. Extraction requires actual existing non-uranium production; the alternative processing direction can use imported materials.

| Programme | Internal industrial or institutional choice | Historical examples, not country locks |
|---|---|---|
| Aviation and Aircraft | Aircraft production or air-service schools | Ukrainian aircraft industry; Tbilisi; Tashkent |
| Armour Production | Advanced armour or lower-cost serial tanks | Kharkiv's tank works |
| Artillery and Ordnance | Precision ordnance or lower-cost mass production | Motovilikha, Russian SFSR |
| Ground Forces and Logistics | Professional cadres or mass reserve schools | Tashkent command training; Union depots |
| Maritime Industry and Fleet | Shipbuilding or coastal fleet services | Mykolaiv combat yards; Baltic merchant and repair facilities |
| Agriculture and Food | Intensive specialisation or crop diversification | Kazakh grain; Uzbek cotton; Moldovan horticulture |
| Civilian Industry | Capital goods or consumer manufacturing | Minsk and Chisinau machinery |
| Resources and Processing | Existing extraction or materials processing | Azerbaijani oil; Turkmen gas; Kazakh minerals |
| Electronics and Research | Defence electronics or civilian applications | Armenian Nairi; Lithuanian Ruta; Latvian VEF |

Weapon-related programmes retain their existing output, efficiency-cap and shipyard bonuses. They also have equipment-specific baseline production-cost reductions, so both internal routes receive a useful specialist cost advantage. The aircraft programme names the actual MD equipment classes rather than the internal generic airframe wording. The preview reads those English names directly from the current native localisation.

| Programme | Specific baseline production cost | Manufacturing or quality choice, including baseline |
|---|---|---|
| Aviation | -5% for the seven named light fighter, light multirole, light CAS, air-superiority, multirole, CAS and heavy-lift families | Aircraft Production: -15% for those families; Air Service Schools retains -5% |
| Armour | Main Battle Tank -6% | Advanced Armour: net -1%, armour +10%, reliability +8%; Serial Tank Production: -18%, armour -4% |
| Artillery | Artillery, Self-Propelled Artillery and MLRS -8% | Precision Ordnance: net -2%, soft attack +10%; Volume Production: -22%, reliability -4% |
| Ground service | Small Arms and Utility Vehicle -5% | Both professional and reserve-service routes retain these reductions |
| Maritime | Patrol Boat, Corvette and Frigate -5% | Shipbuilding Orders: -15%, reliability +5%; Coastal Fleet Service retains -5% |
| Electronics | C&C Equipment -4% | Defence Electronics: -14%, reliability +5%; Civilian Electronics retains -4% |

The listed percentages are this programme's summed contribution, before other national modifiers. Quality premiums remain separate positive cost contributions. On independence discounts retain 20% while those premiums retain 75%, so the quality routes can become more expensive than the unmodified baseline. This is an intended loss of Union supply advantages, not an unadvertised persistent discount. Every component remains visible in its focus; the Specialisations comparison shows compatible-route totals. The costs use `equipment_bonus` with `build_cost_ic`, not generic factory output. The native continuous-air-production idea provides the explicit class-list pattern, including separate base and duplicate archetypes. Designer/non-designer variant refresh, idea removal and actual native cost stacking still require an engine test.

Historical examples appear as a short final reference in descriptions. They never auto-select a role, confer a starting plant, or restrict another republic from investing in the same field. Scope-specific equipment bonuses belong to removable programme spirits so independence can weaken them. Global military output and efficiency effects retain their actual broad scope in the numeric preview. Research and buildings remain one-time national gains.

## GDP prices, market opening and restructuring

All new setup fees, settlement proceeds and recurring allocations are fractions of the paying or receiving country's GDP. Setup transactions use current GDP at execution; weekly allocations use current GDP each weekly calculation. No fixed-dollar charge remains. New works generally cost 1.5% of GDP for a factory or dockyard and 0.9% for infrastructure in the specialisation branches; administrative and technical programmes use smaller shares. These are campaign-balance proposals, not historical budgets. Source evidence for the native GDP arithmetic and weekly reader is recorded in `research_mechanics_v2.md`.

The independent economic chapter offers three mutually exclusive national courses:

| Course | One-time cost | 730-day productive programme | 730-day fiscal/social programme | Separate persistent restructuring burden |
|---|---:|---|---|---|
| Shock Therapy | 0.40% GDP | Productivity growth +1.200; civilian construction +15%; civilian productivity +8% | Tax revenue -25%; stability -8%; social expenditure +10% | Consumer goods factor +18% |
| Gradual Transition | 0.30% GDP | Productivity growth +0.400; civilian construction +5%; civilian productivity +5% | Tax revenue -8%; stability +4%; social expenditure +6% | Consumer goods factor +9%; weekly allocation 0.005% GDP |
| Directed Reconstruction | 0.50% GDP | Productivity growth +0.300; civilian productivity +8%; military-factory construction +8% | Stability +5%; social expenditure +10%; construction -4% | Consumer goods factor +6%; weekly allocation 0.015% GDP |

The first actual sovereign course starts the two-year deadline once. A party switch, re-entry, second secession or save/load cannot restart it. Native productivity growth is a raw monthly input: +1.200 gives approximately +0.6 state productivity points per neutral monthly pass, rather than 120% annual growth. Catch-up and other native multipliers change the outcome. The early benefit represents new-entry and reallocation potential alongside severe immediate disruption; it is not a claim of positive measured post-Soviet output in the first two years.

Six finite enterprise sectors can each be settled once. One national project runs at a time, followed by a 30-day interval. Every method removes one sixth of the course's original consumer-goods burden. Corporate-tax-based consumer goods are a relative factor, not percentage points of all factories.

| Method | Fee | Proceeds | Other effects per sector | Duration |
|---|---:|---:|---|---:|
| Competitive Sale | 0.05% GDP | 0.15% GDP | Civilian productivity +1%; corporate tax revenue -1%; CIVs preserved | 60 days |
| Worker Buyout | 0.12% GDP | 0.03% GDP | Civilian productivity +0.5%; stability +1%; CIVs preserved | 90 days |
| Close the Combine | 0.03% GDP | 0.08% GDP | Administration expenditure -1%; stability -1%; civilian factory -1 | 45 days |
| Public Retooling | 0.20% GDP | None | Civilian productivity +1.5%; tax revenue +1%; administration expenditure +1%; CIVs preserved | 120 days |

A sale models a finite ownership settlement through a charter and national accounts; MD has no native public/private pool for individual CIV levels. Factory loss therefore belongs to actual closure. Closure requires an eligible owned and controlled core state with at least two civilian factories at execution. Six sales provide a finite net 0.60% GDP across their quoted shares; changing government cannot reopen lots. Exact costs, proceeds, consumer-goods relief and capacity loss are visible before choosing. State binding and atomic runtime receipts still require implementation and testing.

## Multiplayer agreements

Concrete foreign-policy focuses offer clearing, technical cooperation, a border commission, defence training, energy transit and shared-basin cooperation. Moldova's unionist programme also has a Romanian cultural convention, without automatic annexation. Their terms are separate and fully numeric in the focus inspector, including both countries' named spirits, every modifier, setup price and weekly programme budget. Locked or politically ineligible focuses remain inspectable.

The focus's completion event selects one eligible named RP partner. The actual recipient gets Accept/Refuse decisions. Acceptance rechecks both countries, meaningful geography/capability requirements and restrictions, then charges setup fees once. Refusal charges neither side. Training and neutrality are independent of whether a border partner happens to be available.

Signatures have no expiry. The active pair requires both states to exist, bilateral peace, no native embargo and no diplomatic, financial, economic or military Imperia sanctions in either direction. Suspension preserves the signature and stops that pair's benefits and dedicated expenses. Restoration does not replay setup fees or national assets. Shared recipient programmes do not multiply their national modifiers across republics; any already active programme must be reflected in the actual marginal acceptance preview. Either signatory can terminate.

Water commissions use actual basins and the later 1992 Almaty agreement as a precedent, not an organisation available automatically in 1970. Energy conventions improve administration and cooperation; they do not conjure resources or pipelines. [ICWC, Almaty agreement](https://secretariat-mkvk.org/?lang=en&page_id=4221), [ICWC agreement texts](https://cawater-info.net/library/icwc-agreem_e.htm).

## MD mechanics and remaining implementation work

Main MD `00_generic.txt` and `05_russia.txt` supply the structural/reward references. Their native relative anchors, reciprocal exclusions and AND/OR prerequisite grammar are retained. The preview uses real inherited focus art, native titlebars and the installed `hoi_16mbs` glyph atlas. It approximates connector routing and chapter labels. Shared Union cards use concise preview titles where their existing labels exceed the native title width; no live localisation is changed.

`civilian_factories_productivity` is MD's civilian economic productivity modifier, read by civilian tax and GDP calculations. `industrial_capacity_factory` and the production efficiency cap are military-production modifiers. Social, administrative and personnel cost modifiers change the corresponding native expenditure formula; they do not themselves raise a law or service tier. A separate weekly treaty stream is another explicit expense, not a second subject subsidy.

Building projects grant exactly one extra shared slot per building level, first, in the same owned and controlled state and one-time transaction. This includes infrastructure. **The final deterministic project-to-state binding and live capacity behaviour remain implementation work**; the concept currently specifies an eligible owned and controlled core state. No third country's territory or resources are granted. Custom project prices deliberately differ from modern MD's 2000-era fixed charges and need campaign calibration against the actual 1970 economy.

The evidence is source inspection, concept graph checks and local browser QA. It is not an emitted-game-script, live tooltip, save/load or multiplayer rehearsal test. `DESIGN_AUDIT.json` records route feasibility, geometry and status-only SSR checks. `BROWSER_CHECKS.json` records all country inspectors, party/status states and viewport checks. Full source/research notes and independent reviews live under `tools/ssr_concept/`. Review snapshots can predate the final small corrections; the generated design/audit hashes identify the delivered revision.

Historical facts, plausible alternatives and numerical balance are separate. The percentages, prices, focus lengths and recovery coefficients are proposals for approval. Implementation waits for the user's approval of this concept.
