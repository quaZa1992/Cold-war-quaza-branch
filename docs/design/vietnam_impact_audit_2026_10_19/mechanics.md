# Vietnam impact audit: mechanics proposals

**Read-only, 19 October 2026. These are balancing/design proposals, not implemented changes.** Only mechanics.md and mechanics.json were written. The compiler was neither imported nor run; the installed307-focus tree was checked against the import-safe runtime design. No engine testing is claimed.

## Main findings

-298 of307 focuses take70 days;7 take35 days and2 take42 days. Forty-one campaign policy ideas still last180 days.
-The six old common branches need4,284 days in total along compatible paths; one old political programme adds about700. A20-year campaign then has only about6.3 years left for the three new war chapters. Chinh has157 historical days versus665 for the shortest installed end path.
-All16 building rewards queue ordinary construction. The three northern1970 states start with0 CIV/0 MIL. A queued factory is not available construction capacity. Native leasing and donor-paid investments exist, but require substantial real funding.
-The rice opening is only+1%bureaucracy and an unlock. Its imported-rice decision is actually+2 stability/+3%market transmission for$35m/180 days, not a food-production or grain-stock mechanic.
-The old foreign decision family blocks simultaneous Soviet aid,China trade,Paris and investment. Aircrew Training is tied to a dockyard. The focus named Investment Access is tied to political pluralism, although the native investment UI itself is not locked.
-Do not blanket-buff every node: six compatible common programmes can already add up to+31percentage-points to the bureaucracy expense multiplier before timed programmes/party costs. This is not+31%of the whole state budget. Stronger choice bundles should replace repeated tiny steps and repeated expenses.

## Fifteen concrete proposals

The full exact installed gates, previews, costs, lifecycles and reference source payloads are in mechanics.json. Numbers below are replacement proposals. Countrywide modifiers stay countrywide; no new virtual resources are introduced.

### M01 — Deliver the first reconstruction factory

**IST:**
- `COLDWAR_VIE_industry_root` (Survey the War Economy): 42 days; $0bn; bureaucracy expenses +1%; national-spirit recovery ['war_damage', 1]; unlock reconstruction. Persistent national programme.
- `COLDWAR_VIE_industry_machine` (Northeastern Industry): 70 days; $0.12bn; No direct modifier; one queued [524, 'industrial_complex']; instant_build=no. Persistent national programme.
- `COLDWAR_VIE_industry_goods` (Hanoi Workshops): 70 days; $0.1bn; No direct modifier; one queued [522, 'industrial_complex']; instant_build=no. Persistent national programme.
- `COLDWAR_VIE_industry_power` (Haiphong Power): 70 days; $0.1bn; No direct modifier; one queued [522, 'fossil_powerplant']; instant_build=no. Persistent national programme.

**Why change it:** All16 focus building projects queue construction; the northern1970 history starts with0 civilian and0 military factories. A queued factory or+5% construction speed creates no construction capacity by itself. Paid native alternatives are real but expensive and contingent.

**SOLL — proposal:**
- focus days: 70.
- placement: A common reconstruction focus after Survey the War Economy, before the workshop split.
- cash bn: 0.15.
- effects: `[{"effect": "add_building_construction", "state": 522, "type": "industrial_complex", "level": 1, "instant_build": true}]`.
- small downside: `{"bureaucracy_cost_multiplier_modifier": 0.02, "days": 365}`.
- lifecycle: One-time physical rehabilitation; persists across governments; one success stamp.
- interpretation: An explicitly proposed rehabilitation of prewar capacity, not a brand-new factory allegedly priced at$150m; no starting GDP, OOB or history buff..

**Gate/lifecycle:** Exact VIE1970 campaign; state522 owned/controlled; actual free shared slot; treasury>=0.15bn. Recheck inside the one-time transaction before charging.

**Units/scope:** One completed physical CIV. Ordinary staffing/consumer-goods rules still apply; test actual available construction in-engine. Keep the other15 projects as queued/native projects.

**Native amount/gate references:**
- `SOV_civilian_industrial_councils`: 49 days: one completed CIV plus5%construction. Communist/neutral-communist government, economy chain, not bankrupt; no explicit focus cash debit. Source: [05_russia.txt:13136](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:13136>).
- `TUR_economic_reforms`: 70 days/$45bn: six completed CIVs,2each in states159/160/934; Through Troubles prerequisite. Scale reference, not a VIE cost template. Source: [turkey.txt:37](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\turkey.txt:37>).

### M02 — Make heavy industry and balanced recovery different useful plans

**IST:**
- `COLDWAR_VIE_duan_heavy` (Heavy Industry First): 70 days; $0bn; military factory output +6%; agricultural productivity -5%. Exact leader and governing-party bound.
- `COLDWAR_VIE_duan_balanced` (Balanced Recovery): 70 days; $0bn; agricultural productivity +5%; military factory output -3%. Exact leader and governing-party bound.

**Why change it:** 70 days buys+6%MIL/−5%agriculture or+5%agriculture/−3%MIL, and the entire economic bonus disappears on Le Duan's departure. Military output is initially an increment on zero military factories while agriculture loses output immediately.

**SOLL — proposal:**
- focus days: 70.
- cash bn: 0.
- **Heavy industry and equipment:** military factory output +10%; production efficiency cap +5%; agricultural productivity -3%. Small downside: Agriculture productivity−3%.
- **Food and civilian recovery:** agricultural productivity +12%; building repair speed +5%; military factory output -2%. Small downside: Military factory output−2%.
- lifecycle: Adopt under Le Duan/party4. The institutional sector plan may survive normal same-party succession until replaced; personal-authority bonuses remain leader-bound..

**Gate/lifecycle:** Exact Communist Party4 and Le Duan for adoption; a later industrial plan replaces this sector policy, rather than stacking all former leaders' rewards.

**Units/scope:** National output/efficiency/repair fractions, not factory grants or direct GDP. Replacement bundles, not additions on top of the old values.

**Native amount/gate references:**
- `SOV_UVZ_expanding`: 35 days/$10bn:10%MIL output+10%efficiency cap plus equipment/R&D package; sanctions flag and not bankrupt. Source: [05_russia.txt:32602](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:32602>).
- `SOV_land_socialisation`: 49 days:12%agriculture,20%agriculture-tax modifier,21%bureaucracy expenses; western_social_democrats. Source: [05_russia.txt:27849](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:27849>).

### M03 — Deliver a Chinh outcome within the historical mandate

**IST:**
- `COLDWAR_VIE_chinh_root` (Reassess the Plan): 70 days; $0bn; research speed +2%; PP gain -3%; unlock plan_review. Exact leader and governing-party bound.
- `COLDWAR_VIE_chinh_orthodox` (Planning Discipline): 70 days; $0bn; PP gain +5%; signed productivity-growth factor -3%. Exact leader and governing-party bound.
- `COLDWAR_VIE_chinh_evidence` (Evidence before Dogma): 70 days; $0bn; signed productivity-growth factor +4%; PP gain -4%. Exact leader and governing-party bound.
- `COLDWAR_VIE_chinh_subsidy` (Retain the Subsidies): 70 days; $0bn; stability contribution +4%; social expenses +5%. Exact leader and governing-party bound.
- `COLDWAR_VIE_chinh_autonomy` (Enterprise Autonomy): 70 days; $0bn; signed productivity-growth factor +5%; stability contribution -3%. Exact leader and governing-party bound.

**Why change it:** His historical mandate is157 days; the installed shortest end path is665 days. The opening choices exchange small PP/growth factors. The later subsidy/autonomy choice is only+4 stability/+5%social cost versus+5%growth factor/−3 stability.

**SOLL — proposal:**
- sequence: A70-day reassessment then one70-day substantive institutional choice:140 days total. Move the choice to the opening. Later continuation requires a longer alternate mandate or inherited cabinet policy..
- cash bn: 0.03.
- **Guarantee essentials during reassessment:** stability contribution +6%; production efficiency cap +5%; social expenses +3%. Small downside: Social expenses+3%.
- **Enterprise accounting autonomy:** signed productivity-growth factor +12%; military factory output +5%; stability contribution -2%. Small downside: Stability contribution−2 points.

**Gate/lifecycle:** Actual Chinh and party4 for adoption. Preserve the institutional outcome under normal same-party succession; no early forced accession or reward replay.

**Units/scope:** Growth factor+12% is not+12%GDP and scales signed growth. Do not pretend the historical157-day leadership can complete a665-day branch.

**Native amount/gate references:**
- `SOV_first_two_year_plan`: 21 days:5%construction plus an1800 day plan idea. Communist government and SOV_has_fixed_the_economy. Source: [05_russia.txt:13061](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:13061>).
- `SOV_civilian_industrial_councils`: 49 days: one completed CIV plus5%construction. Communist/neutral-communist government, economy chain, not bankrupt; no explicit focus cash debit. Source: [05_russia.txt:13136](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:13136>).

### M04 — Differentiate households and productive cooperatives

**IST:**
- `COLDWAR_VIE_linh_contract` (Household Production): 70 days; $0bn; agricultural productivity +8%; PP gain -3%. Exact leader and governing-party bound.
- `COLDWAR_VIE_linh_coops` (Collective Production): 70 days; $0bn; agricultural productivity +4%; bureaucracy expenses +1.5%. Exact leader and governing-party bound.

**Why change it:** Current70-day alternatives are+8%agriculture/−3%PP versus+4%agriculture/+1.5%bureaucracy, with little distinct play identity and a weak cooperative side.

**SOLL — proposal:**
- focus days: 70.
- cash bn: 0.
- **Household contracts:** agricultural productivity +14%; signed productivity-growth factor +4%; PP gain -2%. Small downside: PP gain−2%.
- **Productive cooperative guarantees:** agricultural productivity +10%; stability contribution +4%; bureaucracy expenses +2%. Small downside: Bureaucracy expenses+2%.
- replacement: Replace existing choice rewards and consolidate nearby repeated agriculture increments; do not stack the new bundle with every old tool/market increment..

**Gate/lifecycle:** Exact Linh and party4 adoption; one continuing rural institutional plan per governing party. Built farms remain physical capital on party change.

**Units/scope:** Native national agricultural productivity, not grain tonnes or a new food meter. Israel's farmer-union focus/idea gives a district plus several sector modifiers; proposed VIE choice grants no building.

**Native amount/gate references:**
- `SOV_land_socialisation`: 49 days:12%agriculture,20%agriculture-tax modifier,21%bureaucracy expenses; western_social_democrats. Source: [05_russia.txt:27849](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:27849>).
- `ISR_agricultural_sector`: 42 days: completed agriculture district plus farmer-union upgrade; Labour or specified coalition government. Source: [05_israel.txt:1802](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:1802>).
- `ISR_farmer_union`: Native idea:7%agriculture productivity,8%agriculture-tax modifier,3%workers,8%foreign-influence defence,6%bureaucracy. Cancels when native coalition-policy validity ends. Source: [Israeli.txt:3011](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\ideas\Israeli.txt:3011>).

### M05 — Make gradual and rapid price reform both rewarding

**IST:**
- `COLDWAR_VIE_linh_gradual` (Sequence Price Reform): 70 days; $0bn; signed productivity-growth factor +3%; bureaucracy expenses +1.5%. Exact leader and governing-party bound.
- `COLDWAR_VIE_linh_shock` (End Blanket Subsidies): 70 days; $0bn; signed productivity-growth factor +6%; stability contribution -6%; unlock price_stabilisation. Exact leader and governing-party bound.
- `COLDWAR_VIE_linh_budget` (A Consumption Floor): 70 days; $0.05bn; stability contribution +3%; social expenses +3.5%. Exact leader and governing-party bound.
- `COLDWAR_VIE_linh_inflation` (Fiscal Stabilisation): 70 days; $0.03bn; signed productivity-growth factor -3%; bureaucracy expenses -5%; unlock price_stabilisation. Exact leader and governing-party bound.

**Why change it:** Gradual is+3%growth factor/+1.5%bureau. Shock is+6%growth factor/−6 stability for the personal programme; its fiscal follow-up removes3%growth factor. The political loss can dominate a small change to growth rather than GDP.

**SOLL — proposal:**
- focus days: 70.
- cash bn: 0.
- **Sequence reform and protect consumption:** signed productivity-growth factor +10%; stability contribution +3%; bureaucracy expenses +2%. Small downside: Bureaucracy expenses+2%.
- **End blanket subsidies with a transition:** signed productivity-growth factor +15%; bureaucracy expenses -4%. Small downside: Separate stability contribution−3 points for365 days.
- replacement: One reform policy family. Fiscal follow-up improves its stage rather than silently removing its advertised core benefit..

**Gate/lifecycle:** Exact Linh/party4 adoption. Use a native timed idea for the transition malus; no free timer reset on refresh.

**Units/scope:** Growth factors scale signed growth; expense savings concern only that budget component, not total government spending.

**Native amount/gate references:**
- `SOV_third_way`: 49 days:12%corporate-tax income,6%construction,10%bureaucracy; western_social_democrats. Source: [05_russia.txt:27818](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:27818>).
- `GER_more_healthcare_funding`: About50.05 days: permanent health-reforms idea, after the normal healthcare prerequisite. Source: [05_germany.txt:2883](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:2883>).
- `GER_idea_health_reforms`: Native idea:−8%healthcare expense and−5%social expense. Source: [German.txt:727](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\ideas\German.txt:727>).

### M06 — Separate political pluralism from foreign-capital policy

**IST:**
- `COLDWAR_VIE_linh_monopoly` (Party Monopoly): 70 days; $0bn; PP gain +5%; research speed -2%. Exact leader and governing-party bound.
- `COLDWAR_VIE_linh_pluralism` (Political Pluralism): 70 days; $0bn; research speed +3%; PP gain -5%; unlock political_dialogue. Exact leader and governing-party bound.
- `COLDWAR_VIE_linh_limited` (Screen Foreign Capital): 70 days; $0bn; globalism target +4 points; market transmission +4%; bureaucracy expenses +1%. Exact leader and governing-party bound.
- `COLDWAR_VIE_linh_guarantee` (Investment Access): 70 days; $0bn; globalism target +6 points; market transmission +6%; PP gain -3%. Exact leader and governing-party bound.

**Why change it:** Investment Access is behind Political Pluralism, but technically gives only+6 globalism target,+6%market transmission/−3%PP. Screen Foreign Capital gives+4target,+4%transmission/+1%bureau. Neither actually unlocks native MD FDI; its UI is already separately available.

**SOLL — proposal:**
- focus days: 70.
- **Party monopoly:** PP gain +10%; stability contribution +3%; research speed -2%. Small downside: Research speed−2%.
- **Negotiated political pluralism:** research speed +5%; stability contribution +3%; PP gain -3%. Small downside: PP gain−3%.
- capital placement: Move both economic approaches after Enterprise Accounts, independently of the political choice..
- **Screen strategic foreign capital:** military factory output +6%; sanction resistance +5%; bureaucracy expenses +2%. Small downside: Bureaucracy expenses+2%.
- **Open investment partnerships:** construction speed +8%; research speed +3%; market transmission +8%. Small downside: World-market transmission+8%, magnifying booms and shocks.

**Gate/lifecycle:** Exact party4 adoption with negotiated political alternatives. Native donor-paid investment remains possible under either political option; actual consent/funding/construction still required.

**Units/scope:** Globalism uses target points; market exposure is not guaranteed investment income. No unilateral foreign capital or invented access API.

**Native amount/gate references:**
- `SOV_soviet_academy_of_sciences`: 49 days: one office helper plus5%research. Communist/neutral-communist government and not bankrupt. Source: [05_russia.txt:13225](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:13225>).
- `GER_DAAD_Expand_Academic_exchange_service`: 45.5 days:2%CIV construction+2%office construction+2%research; democratic government and research-cooperation prerequisite. Source: [05_germany.txt:12878](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:12878>).
- `SOV_third_way`: 49 days:12%corporate-tax income,6%construction,10%bureaucracy; western_social_democrats. Source: [05_russia.txt:27818](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:27818>).

### M07 — Democratic Party: open procurement or accountable national enterprises

**IST:**
- `COLDWAR_VIE_dem_tender` (Open Public Tenders): 70 days; $0bn; bureaucracy expenses -5%; PP gain -3%; unlock project_audit. Governing-party bound.
- `COLDWAR_VIE_dem_champions` (National Enterprises): 70 days; $0bn; military factory output +4%; signed productivity-growth factor -2%. Governing-party bound.

**Why change it:** 70 days for−5%bureau/−3%PP versus+4%MIL/−2%growth factor is a small accounting choice versus output on potentially zero factories, not two equally useful development strategies.

**SOLL — proposal:**
- focus days: 70.
- cash bn: 0.
- **Competitive public procurement:** bureaucracy expenses -8%; signed productivity-growth factor +8%; PP gain -2%. Small downside: PP gain−2%.
- **Accountable national enterprises:** military factory output +10%; production efficiency cap +5%; bureaucracy expenses +2%. Small downside: Bureaucracy expenses+2%.
- lifecycle: Governing Democratic programme; deactivate on departure and restore earned values on a legitimate return without replaying one-time rewards..

**Gate/lifecycle:** Exact western_liberals party2 and democratic outlook. No invented party slot or leader.

**Units/scope:** National modifiers. Expense savings are a component multiplier; no instant cash windfall. Physical factories persist across parties.

**Native amount/gate references:**
- `GER_idea_health_reforms`: Native idea:−8%healthcare expense and−5%social expense. Source: [German.txt:727](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\ideas\German.txt:727>).
- `SOV_UVZ_expanding`: 35 days/$10bn:10%MIL output+10%efficiency cap plus equipment/R&D package; sanctions flag and not bankrupt. Source: [05_russia.txt:32602](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:32602>).

### M08 — Socialist Party: universal cohesion or rural targeting

**IST:**
- `COLDWAR_VIE_soc_universal` (Basic Services for All): 70 days; $0bn; stability contribution +4.5%; social expenses +6%. Governing-party bound.
- `COLDWAR_VIE_soc_target` (Target Rural Poverty): 70 days; $0bn; stability contribution +2%; social expenses +3%. Governing-party bound.

**Why change it:** Both70-day paths merely purchase stability:4.5 points for6%social expense versus2 points for3%. Rural targeting has no distinct rural or literacy outcome.

**SOLL — proposal:**
- focus days: 70.
- cash bn: 0.
- **Universal basic services:** stability contribution +6%; research speed +3%; social expenses +4%. Small downside: Social expenses+4%.
- **Rural poverty and literacy:** agricultural productivity +10%; research speed +2%; social expenses +2%. Small downside: Social expenses+2%.
- identity: Broad social cohesion versus faster food-sector recovery and literacy at lower continuing expense..

**Gate/lifecycle:** Exact western_social_democrats party3/democratic outlook. Keep the northern Socialist Party distinct from the southern Hoa Hao party. Exclusive replacement, not both packages.

**Units/scope:** Research/agriculture/stability are separate real native effects. stability_factor is a contribution, not an instantaneous add_stability event.

**Native amount/gate references:**
- `ISR_education_relief_plan`: 35 days:300 day education-relief idea; Labour/eligible coalition. Source: [05_israel.txt:2422](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:2422>).
- `ISR_edication_relief`: 300 day idea:5%research,7%education expense and expected_education_modifier−1. Modern education expectation is not proposed for VIE. Source: [Israeli.txt:3042](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\ideas\Israeli.txt:3042>).
- `ISR_agricultural_sector`: 42 days: completed agriculture district plus farmer-union upgrade; Labour or specified coalition government. Source: [05_israel.txt:1802](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:1802>).

### M09 — Give rice security and procurement actual economic content

**IST:**
- `COLDWAR_VIE_farm_root` (Secure the Rice Supply): 70 days; $0bn; bureaucracy expenses +1%; unlock food_emergency. Persistent national programme.
- `COLDWAR_VIE_farm_procure` (Raise Procurement): 70 days; $0bn; stability contribution +2%; agricultural productivity -3%. Persistent national programme.
- `COLDWAR_VIE_farm_plots` (Expand Plot Incentives): 70 days; $0bn; agricultural productivity +5%; PP gain -3%. Persistent national programme.

**Why change it:** The root gives only+1%bureau and an unlock after70 days. The$35m/180 day Rice Import decision gives only+2 stability/+3%market exposure: no agricultural productivity or grain stock. Procurement is+2 stability/−3%agriculture; plots+5%agriculture/−3%PP.

**SOLL — proposal:**
- focus days: 70.
- opening modifiers: agricultural productivity +6%; social expenses +1%.
- **Reliable state procurement:** stability contribution +4%; army supply consumption -5%; agricultural productivity -3%. Small downside: Agricultural productivity−3%.
- **Plot incentives:** agricultural productivity +10%; signed productivity-growth factor +4%; PP gain -2%. Small downside: PP gain−2%.
- rice decision: `{"cash_bn": 0.035, "days": 180, "modifiers": {"stability_factor": 0.04, "social_cost_multiplier_modifier": -0.03, "mdcw_cw_market_exposure": 0.03}, "description": "Temporary household and procurement relief; no grain resource spawned or structural rationing spirit erased."}`.

**Gate/lifecycle:** Common national food policy; native paid decision expiry and territorial project guards remain.

**Units/scope:** Imported supplies do not increase permanent crop yields. Proposed temporary import effects operate through real social expenses/stability, with market dependency as a small cost.

**Native amount/gate references:**
- `ISR_agricultural_protection_act`: 35 days: agricultural-protection idea, including3%bureaucracy/6%agriculture-tax modifier and4%foreign-influence defence; Labour or specified coalition government. Source: [05_israel.txt:1743](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:1743>).
- `ISR_agricultural_sector`: 42 days: completed agriculture district plus farmer-union upgrade; Labour or specified coalition government. Source: [05_israel.txt:1802](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:1802>).
- `ISR_farmer_union`: Native idea:7%agriculture productivity,8%agriculture-tax modifier,3%workers,8%foreign-influence defence,6%bureaucracy. Cancels when native coalition-policy validity ends. Source: [Israeli.txt:3011](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\ideas\Israeli.txt:3011>).
- `GER_idea_health_reforms`: Native idea:−8%healthcare expense and−5%social expense. Source: [German.txt:727](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\ideas\German.txt:727>).

### M10 — Make local defence and combined arms substantial doctrine choices

**IST:**
- `COLDWAR_VIE_army_local` (Local Defence): 70 days; $0bn; defence on Vietnamese cores +6%; military factory output -3%. Persistent national programme.
- `COLDWAR_VIE_army_combined` (Combined Arms): 70 days; $0bn; army organisation +5%; army supply consumption +6%. Persistent national programme.

**Why change it:** 70 days gives6%core defence/−3%MIL versus5%organisation/+6%supply. The combined-arms side pays a large entire-army supply cost for a modest gain, with no finite doctrine reward.

**SOLL — proposal:**
- focus days: 70.
- cash bn: 0.
- **Territorial defence:** defence on Vietnamese cores +10%; maximum entrenchment +2 points; maximum planning -3%. Small downside: Maximum planning−3%.
- **Combined-arms coordination:** army organisation +8%; maximum planning +5%; army supply consumption +3%. Small downside: Supply consumption+3%.
- each one time effect: `{"effect": "add_doctrine_cost_reduction", "category": "land_doctrine", "uses": 1, "cost_reduction": 0.25}`.

**Gate/lifecycle:** Existing common military branch; no forced doctrine selection, modern technology or equipment. One exclusive policy; do not replay finite discounts on party return.

**Units/scope:** Core defence on all Vietnamese cores; entrenchment across fronts; national supply use. Native Germany grants two50%discounts plus an idea inabout30 days; VIE proposal is deliberately smaller.

**Native amount/gate references:**
- `GER_Reform_Light_forces`: About30.1 days: two50%land-doctrine discounts and an idea replacement; European Anchor Army prerequisite. Source: [05_germany.txt:11667](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:11667>).
- `TUR_the_soldiers`: About50.05 days:one100%infantry research bonus plus one50%land-doctrine discount; Ground Force prerequisite. Source: [turkey.txt:3174](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\turkey.txt:3174>).
- `SOV_military_education`: 21 days:35 armyXP, officer-training increase and−15%mobilization-speed modifier. Communist/neutral-communist government. Source: [05_russia.txt:13923](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:13923>).

### M11 — Air training must not require a dockyard

**IST:**
- `COLDWAR_VIE_army_coast` (Coastal Approaches): 70 days; $0bn; bureaucracy expenses +1%; unlock coastal_patrol. Persistent national programme.
- `COLDWAR_VIE_army_aircrew` (Aircrew Training): 70 days; $0.04bn; research speed +2%; education expenses +3%. Persistent national programme.
- `COLDWAR_VIE_army_fleet` (Small-Fleet Repairs): 70 days; $0.1bn; No direct modifier; one queued [523, 'dockyard']; instant_build=no. Persistent national programme.

**Why change it:** Coastal Approaches gives only1%bureau/unlock after70 days. Aircrew Training is70 days/$40m for2%generic research/+3%education, but requires the exclusive fleet route and its queued dockyard.

**SOLL — proposal:**
- layout: Attach Aircrew Training to General Staff/shared preparation, not the dockyard; retain naval choices for naval content..
- coastal approaches: `{"focus_days": 70, "one_time_effects": [{"effect": "navy_experience", "value": 15}, {"effect": "add_doctrine_cost_reduction", "category": "naval_doctrine", "uses": 1, "cost_reduction": 0.25}], "small_downside": {"bureaucracy_cost_multiplier_modifier": 0.01}}`.
- aircrew: `{"focus_days": 70, "cash_bn": 0.04, "one_time_effects": [{"effect": "air_experience", "value": 25}, {"effect": "add_doctrine_cost_reduction", "category": "air_doctrine", "uses": 1, "cost_reduction": 0.25}], "small_downside": {"education_cost_multiplier_modifier": 0.02}}`.

**Gate/lifecycle:** No aircraft, ship, OOB or equipment grants. Trained cadres and finite doctrine support; ordinary units still require actual equipment production.

**Units/scope:** XP is a flat stock. Germany uses native air-doctrine reductions; Russian2001 reform gives25XP to each branch plus an idea reform for$5bn/21 days. No copy of its whole modern package.

**Native amount/gate references:**
- `GER_Capability_focus`: 42 days: two50%air-doctrine discounts; military prerequisite chain. Source: [05_germany.txt:7639](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:7639>).
- `SOV_2001_military_reforms`: 21 days/$5bn:25 armyXP+25airXP+25navalXP and army-spirit reform; normal prerequisite chain. Source: [05_russia.txt:22944](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:22944>).

### M12 — Fighting and negotiating must remain compatible

**IST:**
- `COLDWAR_VIE_unity_pressure` (Pressure at the Front): 70 days; $0bn; army organisation +4%; army supply consumption +4%. Persistent national programme.
- `COLDWAR_VIE_unity_paris` (The Paris Talks): 70 days; $0bn; bureaucracy expenses +1%; war-support contribution -3%; unlock paris_contacts. Persistent national programme.
- `COLDWAR_VIE_unity_aftermath` (After the Fighting): 70 days; $0bn; bureaucracy expenses +1.5%; social expenses +2%; unlock ceasefire_monitoring. Persistent national programme.

**Why change it:** Military pressure and Paris are exclusive. Paris gives1%bureau/−3war-support, then an accepted$15m session adds only2 stability/−3war-support for270 days. After the Fighting adds another1.5%bureau/2%social for70 days and an unlock.

**SOLL — proposal:**
- focus days: 70.
- exclusion: Keep exclusive command-resource postures if desired, but share access to the actual Paris decision so military pressure does not forbid negotiations..
- **Battlefield pressure:** army organisation +6%; maximum planning +3%; army supply consumption +3%. Small downside: Supply consumption+3%.
- **Negotiating mandate:** stability contribution +3%; defence on Vietnamese cores +3%; bureaucracy expenses +1%. Small downside: Bureaucracy expenses+1%.
- aftermath modifiers: building repair speed +10%; agricultural productivity +5%; bureaucracy expenses +1%.
- accepted session: `{"cash_bn": 0.015, "days": 365, "modifiers": {"stability_factor": 0.04, "war_support_factor": -0.02}}`.

**Gate/lifecycle:** Actual recipient consent; US obligations need separate US consent. Aftermath requires real cessation/recovery conditions. No focus badge ends war or transfers territory.

**Units/scope:** Native numeric event options preview real sender-scoped cost, duration and idea effects; short explanation in the event description. No hidden prose reward.

**Native amount/gate references:**
- `ISR_assam_ibrahims_mission`: 28 days, Egypt exists/no war/opinion>4: recipient event; accepted preview costs100PP and gives25 armyXP,15command power,one25%special-forces research bonus and one25%land-doctrine discount. Source: [05_israel.txt:13005](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:13005>).
- `GER_Suitable_Agriculture_programs`: 45.5 days: recipient-owned events for Colombia,Ethiopia,Vietnam; accepted preview includes an agriculture idea,two100%civilian research bonuses,actual influence/investment/debt consequences. Democratic German government. Source: [05_germany.txt:13690](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:13690>).

### M13 — Training should outlast its own focus chain

**IST:**
- `COLDWAR_VIE_guerrilla_lessons` (The Long War): 70 days; $0.01bn; No direct modifier; 1 uses of 15.0% land_doctrine XP discount; Unlock: Review the war method. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_guerrilla_training` (Small Unit Schools): 70 days; $0.015bn; No direct modifier; Small Unit Schools: land-doctrine XP cost -5%; army training time +3%; 180 days. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_guerrilla_staff` (Regional Staffs): 70 days; $0.02bn; No direct modifier; Regional Staffs: land-doctrine XP cost -7%; bureaucracy expenses +2%; 180 days. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_guerrilla_networks` (Army and Movement): 70 days; $0.02bn; No direct modifier; xp 10; Unlock: Select a campaign posture. Per-family timed; conditional permanent only where explicitly specified.

**Why change it:** The Long War is70 days/$10m for one15%doctrine discount/unlock. Schools:70 days/$15m for5%land-doctrine cost reduction but3%slower training for180 days. Staffs then replaces it with7%reduction/+2%bureau for180 days. The two-lane prerequisites consume much of the timers.

**SOLL — proposal:**
- focus days: 70.
- long war: `{"cash_bn": 0.01, "one_time_effects": [{"effect": "army_experience", "value": 20}, {"effect": "add_doctrine_cost_reduction", "category": "land_doctrine", "uses": 1, "cost_reduction": 0.25}]}`.
- schools: `{"cash_bn": 0.015, "one_time_effects": [{"effect": "army_experience", "value": 25}, {"effect": "add_doctrine_cost_reduction", "category": "land_doctrine", "uses": 1, "cost_reduction": 0.25}], "small_downside": {"education_cost_multiplier_modifier": 0.02, "days": 365}}`.
- staffs: `{"cash_bn": 0.02, "days": 365, "modifiers": {"land_doctrine_cost_factor": -0.1, "training_time_army_factor": -0.05, "bureaucracy_cost_multiplier_modifier": 0.02}}`.
- replacement: Replace old stages; renew only the timed policy, never one-time focusXP or finite discounts..

**Gate/lifecycle:** Common professional military lessons. Foreign revolutionary party support remains separately party4-gated. No forced modern MD guerrilla doctrine or mech_militia technology.

**Units/scope:** Native Israel35 day drill bundles30XP+one25%discount+idea with real peace/manpower/US gates and$2.75bn cost. Proposed VIE funding/force requirements remain its own scale.

**Native amount/gate references:**
- `ISR_sayeret_drill`: 35 days/$2.75bn/50command power:30 armyXP,one25%land-doctrine discount and drill idea. Peace,army manpower>120000,US exists/opinion>19,Major Non-NATO Ally,not bankrupt. Source: [05_israel.txt:32061](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:32061>).
- `TUR_the_soldiers`: About50.05 days:one100%infantry research bonus plus one50%land-doctrine discount; Ground Force prerequisite. Source: [turkey.txt:3174](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\turkey.txt:3174>).
- `GER_Reform_Light_forces`: About30.1 days: two50%land-doctrine discounts and an idea replacement; European Anchor Army prerequisite. Source: [05_germany.txt:11667](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:11667>).

### M14 — Earn China and Cambodia operating plans before the short campaigns

**IST:**
- `COLDWAR_VIE_china_survey` (Survey the Defences): 70 days; $0.02bn; No direct modifier; Frontier Readiness: maximum entrenchment +1 points; entrenchment speed +10%; 180 days. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_china_liaison` (A Northern Command): 70 days; $0.025bn; No direct modifier; Northern Command: maximum entrenchment +2 points; entrenchment speed +15%; defence on Vietnamese cores +3%; 180 days. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_china_hold` (Hold the Line): 70 days; $0.035bn; No direct modifier; Northern Defence: maximum entrenchment +3 points; entrenchment speed +20%; defence on Vietnamese cores +5%; maximum planning -3%; 180 days; forest/jungle defence 5.0%. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_china_depth` (Defence in Depth): 70 days; $0.04bn; No direct modifier; Defence in Depth: maximum entrenchment +5 points; entrenchment speed +25%; defence on Vietnamese cores +8%; maximum planning -5%; 180 days; forest/jungle defence 10.0%. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_china_counter` (A Limited Counterstroke): 70 days; $0.04bn; No direct modifier; Limited Counterstroke: army supply consumption +7%; military factory output -3%; attack against named opponent +6%; defence against named opponent +3% vs CHI; 180 days. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_china_objectives` (Bound the Objectives): 70 days; $0.045bn; No direct modifier; Bounded Counterstroke: army supply consumption +8%; military factory output -4%; attack against named opponent +8%; defence against named opponent +3% vs CHI; 180 days; Unlock: Offer a bounded ceasefire. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_china_crisis` (The Frontier Crisis): 35 days; $0.015bn; No direct modifier; xp 10; Unlock: Review the northern mandate. Per-family timed; conditional permanent only where explicitly specified.
- `COLDWAR_VIE_cambodia_capital` (Phnom Penh Objective): 70 days; $0.05bn; No direct modifier; Cambodian Offensive: army supply consumption +6%; military factory output -2%; attack against named opponent +14%; defence against named opponent +6% vs CBD; 240 days; Unlock: Review achieved campaign objectives. Per-family240-day wartime operating idea.

**Why change it:** Current defence is already strong and distinctive. Timing is weak:35 days for the crisis plus70 days for a war plan can exceed a short frontier war. Counterstroke pays7–8%army supply and3–4%MIL for6–8%CHI attack/3%CHI defence. Cambodia Capital likewise requires an actual CBD war throughout its70-day focus before the240-day offensive idea is delivered; a rapid offensive can finish first.

**SOLL — proposal:**
- preparation: Keep70 days to earn a selected plan before conflict without inventing hostility. An actual-war decision activates one initially prepaid earned term immediately; later renewals are paid. Actual peace cancels the operational bonus..
- defence: Preserve exact current Hold values: entrenchment3, speed20%,coredefence5%,forest/jungledefence5%,planning−3%; Depth5/25%/8%/10%/−5%. Proposed usable term365 days, still war-gated..
- counterstroke: `{"cash_bn": 0.04, "days": 365, "target": "CHI", "targeted_modifiers": {"attack_bonus_against": 0.08, "defense_bonus_against": 0.03}, "country_modifiers": {"max_planning_factor": 0.05, "supply_consumption_factor": 0.03}, "small_downside": "Supply+3%"}`.
- objectives: `{"cash_bn": 0.045, "days": 365, "target": "CHI", "targeted_modifiers": {"attack_bonus_against": 0.1, "defense_bonus_against": 0.03}, "country_modifiers": {"max_planning_factor": 0.05, "supply_consumption_factor": 0.04}, "small_downside": "Supply+4%; replaces counterstroke"}`.
- cambodia operation: `{"institution_days": 70, "activation": "A recipient-independent domestic operations decision during actual VIE-CBD war, after an earned intervention mandate; recheck cash at execution. No campaign bonus requires sitting in a70-day war focus.", "cash_bn": 0.05, "days": 240, "target": "CBD", "targeted_modifiers": {"attack_bonus_against": 0.14, "defense_bonus_against": 0.06}, "country_modifiers": {"supply_consumption_factor": 0.06, "industrial_capacity_factory": -0.02}, "values": "Retain the approved substantial Cambodia operation amounts; this is a timing/access fix, not another numerical buff."}`.

**Gate/lifecycle:** Actual CHI war for activation; no free regrant on daily ticks. Survey is ordinary preparedness. States523/524 are the true frontier;522 is rear-area delta.

**Units/scope:** max_dig_in is flat. Terrain applies against any opponent in that terrain while active; CHI targeted benefits apply across all fronts against CHI. No quantity buff to the approved defensive values.

**Native amount/gate references:**
- `GER_Reform_Light_forces`: About30.1 days: two50%land-doctrine discounts and an idea replacement; European Anchor Army prerequisite. Source: [05_germany.txt:11667](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:11667>).
- `SOV_first_two_year_plan`: 21 days:5%construction plus an1800 day plan idea. Communist government and SOV_has_fixed_the_economy. Source: [05_russia.txt:13061](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:13061>).
- `ISR_sayeret_drill`: 35 days/$2.75bn/50command power:30 armyXP,one25%land-doctrine discount and drill idea. Peace,army manpower>120000,US exists/opinion>19,Major Non-NATO Ally,not bankrupt. Source: [05_israel.txt:32061](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:32061>).

### M15 — Remove the blanket diplomatic lockout

**IST:**
- `COLDWAR_VIE_diplomacy_root` (Two Patrons): 70 days; $0bn; bureaucracy expenses +1%; unlock patron_contacts. Persistent national programme.
- `COLDWAR_VIE_diplomacy_moscow` (The Soviet Relationship): 70 days; $0bn; research speed +3%; globalism target -3 points; unlock soviet_offer. Persistent national programme.
- `COLDWAR_VIE_diplomacy_balance` (Balance the Patrons): 70 days; $0bn; sanction resistance +4%; bureaucracy expenses +2%; unlock chinese_offer. Persistent national programme.

**Why change it:** Moscow/Balance is3%research/−3 globalism target versus4%sanction resistance/+2%bureau. The foreign decision family additionally prevents concurrent Soviet aid, China trade, Paris and investment missions, although those are different activities.

**SOLL — proposal:**
- focus days: 70.
- **Soviet technical commitment:** research speed +5%; army supply consumption -3%; bureaucracy expenses +2%. Small downside: Bureaucracy+2%.
- **Balance two supply relationships:** agricultural productivity +8%; sanction resistance +6%; bureaucracy expenses +2%. Small downside: Bureaucracy+2%.
- families: Separate current donor technical programmes from diplomacy/settlement terms. Allow one Soviet and one Chinese programme plus an unrelated negotiation; retain native donor capacity, fees, consent, expiry and dependency burdens..
- agreements: `{"soviet": {"cash_bn": 0.04, "days": 365, "modifiers": {"research_speed_factor": 0.03, "bureaucracy_cost_multiplier_modifier": 0.015}}, "chinese": {"cash_bn": 0.035, "days": 365, "modifiers": {"supply_consumption_factor": -0.04, "bureaucracy_cost_multiplier_modifier": 0.01}}}`.

**Gate/lifecycle:** Keep exact earned-provider pairs. Soviet aid is donor initiated; only positive, active, unexpired donor-scoped p6/p7 counts as real received military aid. Accepted interest is not deliveries.

**Units/scope:** Sanction resistance mitigates existing sanctions only; supply benefits are national. Events show concrete numeric payer-scoped costs and native rewards, not a narrative approximation.

**Native amount/gate references:**
- `SOV_soviet_academy_of_sciences`: 49 days: one office helper plus5%research. Communist/neutral-communist government and not bankrupt. Source: [05_russia.txt:13225](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:13225>).
- `ISR_assam_ibrahims_mission`: 28 days, Egypt exists/no war/opinion>4: recipient event; accepted preview costs100PP and gives25 armyXP,15command power,one25%special-forces research bonus and one25%land-doctrine discount. Source: [05_israel.txt:13005](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:13005>).
- `GER_Suitable_Agriculture_programs`: 45.5 days: recipient-owned events for Colombia,Ethiopia,Vietnam; accepted preview includes an agriculture idea,two100%civilian research bonuses,actual influence/investment/debt consequences. Democratic German government. Source: [05_germany.txt:13690](<E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:13690>).

## Stacking, economy and cleanup constraints

- Bundles replace listed existing rewards and should consolidate adjacent repeated increments. They are not15simultaneous blanket buffs.
- Six common programmes coexist. Independent per-key structural maxima before spirits/timed programmes:research+23.5%,bureaucracy multiplier+31%,social-expense multiplier+25.5%. An active Democratic programme can add8.5%research; Socialist programme11%social expense. These are component multipliers,not whole-budget percentages; listed maxima need not share the same choices.
- Current source classification:95national-persistent,80party-bound,64exact-leader-bound focuses before the68campaign additions. Built capital and one-time training should survive leadership; personal authority should not. Continuing sector plans replace predecessors rather than stack all former leaders.
- At70 days per focus,roleplay identity should come from different sector outcomes and meaningful native decisions,not repeated+3%PP-versus−3%research swaps.
- Current Cambodia victory is already worthwhile:25 armyXP,two20%land-doctrine discounts,and a conditional friendly secure-southwest idea with6%agriculture,−3%supply,+2%bureau. Preserve actual victory/control/consent verification instead of inflating every branch.
- Currency is billions:0.01=$10m. max_dig_in is flat; other listed fractions require native tooltips. Agricultural productivity is not rice tonnes. Country growth-factor modifies signed growth,not GDP directly.
- Timed policy expiry/cancellation must not reset finite XP/discounts or construction. Daily synchronization restores only authorized earned programmes,never their original cash/reward transaction.
- Current AGENTS.md: agreement events use short explanations and concrete numeric native option effects in correct payer/recipient scopes.
- Engine checks remain necessary for actual available construction,short-war timing,terrain-technology cleanup,party/succession retention,offer acceptance/expiry and family replacement. No engine proof is claimed.

## Provider-to-consumer checks

- **agricolture_productivity_modifier**: National agriculture/GDP/tax multiplier; not food stock. definition: C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\modifier_definitions\money_modifier_definitions.txt:353; consumers: C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\scripted_effects\00_money_system.txt:408,544,5245,5941
- **country_productivity_growth_modifier**: Signed base growth multiplied by1+modifier;negative growth can reverse intuitive cost/benefit. definition: C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\modifier_definitions\money_modifier_definitions.txt:515; consumer: C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\scripted_effects\00_productivity_effects.txt:73–80,229–235
- **native_instant_factory**: Actual industrial_complex1 instant_build=yes; current VIE projects allinstant_build=no. provider: E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\scripted_effects\00_scripted_effects.txt:223–231
- **native_leasing**: Real offsiteCIV. First lease atGDP/capita.113 with no inflation uplift (inflation_on_leases=1) costs about0.100113bn per native budget week;not a cheap guaranteed bridge. provider: C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\scripted_guis\00_MD_economyview_scripted_guis.txt:916–925; consumer: C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\scripted_effects\00_money_system.txt:3663–3676
- **native_foreign_investment**: Donor-funded native project;recipient10%commissioning,baseCIV12bn donor/1.2bn recipient before modifiers;duration independent of VIE civilian count. provider: C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\scripted_effects\99_investment_scripted_effects.txt:9,100,162,309,428,489
- **native_SOV_variable_consumers**: Cited Russian variables map to native construction/research/agriculture/output/efficiency modifiers. provider: E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\dynamic_modifiers\99_SOV_dynamic_modifiers.txt:12,16,18,164,172–173,197–198
- **native_GER_variable_consumers**: DAAD variables map toCIV/officeconstruction/research. Heer cost variable maps to total personnel-cost multiplier. provider: E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\dynamic_modifiers\99_GER_dynamic_modifiers.txt:124–126,239

## What this audit does not assert

Native modern MD numbers are scale and coding references, not an instruction to copy modern factories,unit counts,coalitions,technology or cash prices into1970Vietnam. A restored civilian complex is a deliberate proposed change to the approved reward design, not a hidden start buff. Native leasing costs and any final available factory allocation still need an engine check.

The concrete proposal set includes separate Democratic Party and Socialist Party identities. Retained starting leaders,party slots,empty initial OOB and historical starting GDP are outside this audit change scope.
