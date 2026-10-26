# Shared Iraqi reward overhaul: authored implementation data

19 October 2026. This agent authored **all158 active shared focuses** in `tools/iraq_1970/reward_overhaul_economy.json`: State18,Foreign18,Oil15,Industry13,Agriculture15,Society16,Defence17,War18,Iran28. This is the complete source-data change for the assigned chapters, not another list of audit suggestions. No existing generator, loaded game file or geometry was edited by this agent. The root agent owns compiler integration, migration and installation.

Final economic dataset SHA256: `5587a2d86672715a7df579d23aecf7eefbbd468fc35dc1f667b796ad9168b90b`.

Each focus record gives explicit final `modifiers`, `building`, `army_xp`, `instant`, `budget_gdp_share`, `days`, an individually written English `description`, a native `reference` and the design `rationale`. Modifier and instant lists replace their old lists. Existing special requirement/contract/territory and starting-spirit consumers are retained through integration; none is presumed satisfied by a research grant. All158descriptions were rewritten: zero old catalogue descriptions remain unchanged, and the source was scanned for mojibake.

## Original main MD references, actual rewards

The reviewed originals are under `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`, not the generated Cold War mod. These examples establish the direct reward grammar and useful scale, not permission to copy2000technology or another country's borders.

| Original focus | Days / actual direct reward / treasury cost |
|---|---|
| [IRQ_oil_fields_in_the_north](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iraq.txt:77) |70days;8oil166+4oil165+2fossilplants165; $16bn; bothstates owned/controlled. |
| [IRQ_farming_regulations](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iraq.txt:2042) |35days; four actual home states each+50state productivity; no direct treasury debit; Baath/ownership gates. The new dataset **does not copy an unguarded foreign-state mutation**: Survey now gives a country-owned agricultural-efficiency benefit. |
| [IRQ_brick_by_brick](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iraq.txt:2525) |70days; up to3owned-state infrastructure levels;2×50%Infrastructure research+2×25%Construction; $10.5bn. |
| [IRQ_restoration_of_hospitals](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iraq.txt:3703) | Up to3actual infrastructure levels for$10.5bn. It does not invent a hospital building or a mortality variable. |
| [IRQ_renovation_of_baiji_refinery](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iraq.txt:3604) | Oil5+five fuel silos167,$15bn. The new Iraqi package adapts this to **one** explicit silo, current capacity and a domestic technical programme. |
| [IRQ_ship_building_industry](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iraq.txt:1728) |50.33days; two actual dockyards through `two_random_dockyards`; the helper charges$15bn unless skipped. It is not a free helper to nest inside our invoice. |
| [PER_extraction_efforts_in_semnan](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iran.txt:1957) |50.4days;1infrastructure+8steel1149; $12bn; owned/controlledstate. |
| [PER_expand_industrial_towns_in_qazvin](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iran.txt:2007) |40.04days;2actual civilian factories405; $17.5bn. |
| [PER_expanding_the_power_grid](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iran.txt:2757) |40.04days;3fossilplants405; $6.75bn; real energy/fuel obligations follow. |
| [PER_tabriz_service_sector](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iran.txt:2803) |40.04days;2offices407; $24bn; this has a separate sector-tax/workforce outcome from factories. |
| [PER_prepare_the_army](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iran.txt:939) |50.05days;100ArmyXP+100NavyXP+100AirXP+100CommandPower; no direct treasury debit. The Iraqi overhaul grants smaller lessons at meaningful military milestones, not this entire prize at every node. |
| [PER_prepare_for_the_next_century](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_iran.txt:4742) |14days; three separate pools, each2×50%Industry/Civilian/Agriculture; no direct treasury debit. Agriculture-only targets are too late for an immediate1970reward, so they are not copied. |
| [SOV_military_education](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_russia.txt:13923) |21days;35ArmyXP+one actual officer-training law step;−15%mobilisation speed. The Iraqi general military programme retains conservative organisation values and uses explicit finite doctrine/training outcomes. |
| [SOV_aero_improvements](E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_russia.txt:13269) |21days;1×25%Aircraft,−10%air accidents,$3bn. The Iraqi air-maintenance focus now also delivers actual accident reduction, alongside its existing research/XP. |

The independent reference reviewer traced helper bodies. `one_office_construction` also adds a fossil plant and charges$12bn; random-arms helpers charge$7.5/$22.5bn. **None is called by this dataset.** Explicit structured assets are used with one external invoice.

## Complete programme changes

- **State:** executive effectiveness versus civilian capacity; productive provincial institutions versus councils; a security-state police commitment versus judicial investment confidence. Actual ministerial patronage and professional-command spirit improvements remain. Funded autonomy delivers1Nineveh infrastructure only after the actual agreement. StateCompact keeps its meaningful−6%Bureaucracy/+4%tax outcome. No additional corruption-law step competes with the political agent's civic reform.
- **Foreign:** direct domestic trade, technical preparation, industry/construction research and frontier infrastructure accompany diplomacy. Partner choice and nonalignment have different influence implications. Actual contracts, border recognition and loans still require recipient consent. Debt administration provides a small native rate adjustment; it grants no cash or principal cancellation.
- **Oil:** preserve Nationalisation/Concession and Revenue/Diversification. Ownership transition and negotiated foreign share remain real. FieldMaintenance grants one35%Industry use on **both** routes and removes the final6%technical IPC burden only on the nationalised route. Nationalisation retains its explicit90-day disrupted-marketing idea. Baiji and reserves gain actual fuel-silo capacity; native MD fossil-fuel efficiency replaces old vanilla `fuel_gain_factor` abstractions.
- **Industry:** keep Heavy/Light's factories and genuinely different production/construction benefits. Public finance supports revenue with a civilian commitment; credit finance accelerates construction at a real rate premium. Maintenance, machine tools, power and commercial offices each produce their own outcome. TaxService specialises in the real office sector rather than another universal tax modifier.
- **Agriculture:** existing actual districts remain. LargeIrrigation adds Wasit infrastructure and stronger farm productivity at a civilian-capacity cost; LocalIrrigation is faster and retains the DhiQar district follow-up. Storage/roads, extension/genetics, inspected waterworks and clinics have different technical/service effects. Existing rural-spirit stages and final removal remain separate, not double-counted as a new modifier.
- **Society:** real literacy gains, teacher capacity and finite specialist research. UniversalServices has long-term native productivity growth and a larger social commitment; TargetedServices preserves more civilian capacity, funds real Nineveh infrastructure and pays for a means-testing administration. PrimaryCare provides actual Maysan infrastructure and healthcare efficiency. Education costs are labelled as education costs, not another generic bureaucracy surcharge.
- **Defence:** Professional/Reserve and Soviet/Mixed remain different. Conservative organisation/recovery values are retained. Procurement, logistics, operating manuals, staff instruction, safe aircraft maintenance, dockyard practice and readiness have direct capability/XP/research outcomes. No equipment appears from a foreign country's stockpile without its agreement.
- **War/recovery:** meaningful contingency/authorisation lessons and repair capacity; military-output commitment versus protected civilian productivity. Procurement efficiency carries equipment expense; emergency accounting reduces actual equipment waste. Veterans retain experience at a social cost; civilian reconstruction and reintegration have productive outcomes. Refinancing/sanctions preparation adds direct expertise while leaving creditors and sanctions contracts in control of their own decisions.
- **Iran:** claims, actual war goal, operational choices, initial offensive windows, duration tests, occupation requirements and the final core remain. Former empty ledger/attrition nodes are shorter and give finite military lessons. Occupation has actual compliance and policing obligations. The large independent Gulf wage/equipment escalation, borrowing, PriceOfVictory and Kuwait chain are untouched.

## Counts and physical scope

Across the158assigned focuses, bureaucracy payloads fall66→15; Stability payloads24→8. The surviving negative stability, funded institutions, security costs and integration commitments have a specific function. This does not replace every discarded malus with another budget line.

All pre-existing structured building grants keep exactly their previous state/type/count. Nine new building-bearing focuses are explicit:

| Focus | New one-time asset |
|---|---|
| autonomy_guarantees |1infrastructure166 |
| foreign_border_delivery |1infrastructure1124 |
| oil_baiji |1fuel_silo167 |
| oil_reserve_policy |1fuel_silo171 |
| agri_large_irrigation |1infrastructure1141 |
| society_primary_care |1infrastructure1124 |
| society_priority_districts |1infrastructure166 |
| defence_logistics |1infrastructure167 |
| iran_forward_depots |1infrastructure167 |

No extra raw `add_building_construction` is hidden in `instant`. Root integration must guard **all** physical components for present ownership/control/capacity before any debit. Infrastructure and silos are nonshared with actual caps6/5; general shared-slot syntax is not sufficient. Existing once-only grants must be credited in v3; only new uses/assets or increased fees belong in an upgrade. The nationalisation timer is credited for existing implementations instead of punishing them again.

There are20finite technology pools/23uses across the158-focus catalogue, plus finite doctrine instruction. This is not23uses on a single eligible route and not23permanent global research bonuses. Actual early consumers were checked: electronics1965/1975; infantry1965/1970/1975; infrastructure1960/1967. Genetics is now usable through the current authored early technology file: `mdcw_industry_60s_70s.txt:86`geneticcode1966,`:103`recombinantDNA1973,`:120`sequencing1977. The old audit's “genetics starts1985” observation is superseded by these current consumers. No early Agriculture/FuelRefining/Excavation pool was copied blindly from the original2000trees.

## Compatible complete civilian routes

Full original/proposed node lists and exact arithmetic are in `reward_diversity_2026_10_19/OVERHAUL_ECONOMY_ROUTES.json`. They include all compatible side projects in Oil/Industry/Agriculture/Society. Prerequisite groups and mutual exclusions were checked directly against the current graph. Both routes stay in one country and require ownership/control, available construction capacity and actual funding. No foreign treaty acceptance or incompatible party is silently added.

- **A:** Nationalisation+Revenue; Light+PublicFinance; Cooperatives+LocalIrrigation; TeacherFirst+TargetedServices.47focuses; DhiQar,all rural milestones,power,offices,technicalcolleges andhousing included.
- **B:** Nationalisation+Diversification; Heavy+PublicFinance; Cooperatives+LargeIrrigation; MassLiteracy+UniversalServices.46focuses; DhiQar andPriorityDistricts excluded because they belong to unchosen branches.

| Chapter contributions before laws/starting ideas/party programmes | A old | A new | B old | B new |
|---|---:|---:|---:|---:|
| Bureaucracy expense multiplier |+52%|+10%|+43%|+8%|
| Social expense multiplier |+16%|+5%|+22%|+8%|
| Education expense multiplier |0|+10%|0|+10%|
| Health expense multiplier |0|−5%|0|−10%|
| General tax gain |+10%|+5%|+13%|+8%|
| Office-specific tax coefficient |0|+22%|0|+22%|
| Oil export-income multiplier |+28%|+34%|+7%|+13%|
| Factory efficiency growth |+15%|+26%|+15%|+26%|
| Max factory efficiency |+5%|+5%|+15%|+15%|
| Military factory output |−1%|−1%|+4%|+4%|
| Generic building speed |+10%|+11%|+10%|+11%|
| Infrastructure-specific building speed |0|+30%|0|+30%|
| Agriculture productivity coefficient |+23%|+39%|+24%|+42%|
| Relative consumer-goods factor |+1%|−3%|+5%|+5%|
| Global research |+7%|+5%|+2%|0|
| Native productivity-growth parameter |0|0|0|+.10|
| Fossil-power fuel consumption |0|−10%|0|−10%|
| Army fuel consumption |0|−4%|0|−4%|
| Positive programme stability, before cap |+6points|0|+8points|0|
| Physical building grants |9|12|8|12|
| Finite technology uses |6|11|6|11|
| Focus-days |1729|1645|1680|1624|
| Sum of quoted GDP shares* |87.5%|91%|89%|92%|

\*The shares span several years and changing quote dates. Their sum is not a single-year budget or a predicted cash total. The native asset price floor, exact frozen invoice and upgrade-cost credit remain compiler responsibilities. Old physical assets are never charged again just because the programme gains a new technical benefit.

The old+18%Bureaucracy from JulyState/Patronage remains on an unreformed starting government; these four chapters alone do not erase it. Thus A's explicit chapter+those two ideas changes+70→+28%, B+61→+26%, before other laws/modifiers. State reforms have their own rewards and conditions and are not smuggled into this comparison.

## Complete defence routes: organisation kept conservative

Both rows include all compatible defence side projects, including logistics,air/coastal maintenance,armaments andreadiness. They exclude the alternative root and alternative supplier branch. No Saddam/Bakr/other-party programme, temporary readiness/adviser idea or Iran-war bonus is counted.

| Direct defence programme | Professional+Soviet old→new | Reserve+Mixed old→new |
|---|---:|---:|
| Focuses/days |13/497→13/483|13/497→13/483|
| Organisation |+8%→+8%|−3%→−3%|
| Recovery |+3%→+3%|+14%→+14%|
| Army training time |+4%→+4%|0→+2%|
| Army personnel costs |+8%→+8%|+5%→+5%|
| Supply use |−13%→−15%|0→−2%|
| Bureaucracy |+11%→0|+13%→0|
| ArmyXP |105→140|85→130|

New maintenance depth includes−10%AirAccidents,+10%DockyardOutput,+3%ArmySpeed,+10%PlanningSpeed and,onlyonMixed,−3%Attrition/+2%TrainingTime. The Professional route retains its paid staff doctrine instruction and gains distinct domestic preparation before a Soviet offer. FiniteXP does not create divisions or give aircraft that Iraq does not own.

## Honest stacking risks and integration checks

1. **Agriculture has real impact.** A/B+39/+42%agriculture coefficients plus districts and inherited spirit relief are intentionally much stronger than the prior repetitive administrative chain. Additional compatible political agriculture programmes can raise them further. There is no invented silent cap. This is a priority balance check in an actual1970economy, particularly once both old rural penalties have been removed.
2. **Infrastructure has a visible pileup.** GrainStorage,RiverTalks andHousing each contribute10%infrastructure speed:30%in these full routes, before ForeignSyria/other parties. These are additive specialist capabilities, not30%general construction. If reduction is needed, consolidate one contributor into its actual asset rather than impose another bureaucracy bill.
3. **Office coefficients are sector-specific.** TaxService12%+MunicipalFinance10%=22%on the actual office income calculation. This does not mean22%more total national revenue. The reduction in generic tax gains is deliberate.
4. **Native fuel use is scoped.** Baiji+GridManagement combine to−10%on fossil plants' fuel use. They do not reduce all military fuel demand or generate oil. Separate military fuel discipline can stack on actual military operations and must be shown separately.
5. **Interest terms cannot cancel creditors.** ForeignDebtDiplomacy−.25pp andWarCreditBurden−.25pp can coexist after their own gates. CreditFinance+.25pp andDebtAccounts−.15pp belong to the credit branch. Native rate clamps remain; neither principal nor a player's consent is changed. PriceOfVictory's+2rate term and the massive independent Iran cost chain remain real.
6. **Research needs unused targets.** The pools have real1970consumers, but a player may already have researched some. Multiple categories in a pool are not independent bonuses. v3 must credit previously delivered uses by category/count and grant only genuinely additional uses, not reissue stronger versions of already consumed pools.
7. **XP is finite, not an alternative army.** The catalogue contains460ArmyXP across mutually incompatible branches and later war milestones; no player receives that at once. Complete defence routes earn140/130over483focus-days versus originalIran100in one50-dayfocus. The engine cap and actual template/doctrine spending still matter.
8. **Military stacking is bounded by choices, not new caps.** Shared StateOrg2+3,Professional8,SouthCommand4 andLongWarReserves4 remain their old values. Guard/Regular and other party programmes are separately selected; do not sum every leader. The new PeaceDividend deliberately trades some readiness−2%Org for civilian recovery. Active-war/emergency/occupation predicates must continue to suppress inappropriate programmes after a contract expires or circumstances change.
9. **Territorial rewards stay earned.** No country-wide compliance grant, new Khuzestan claim or extra core was copied. New compliance in399uses the existing territorial predicates; the finalcore still requires its actual control,peace and integration conditions. Primary MP acceptance events,decline paths andactual Kuwait obligations survive the reward rewrite.

The author ran JSON/schema/coverage checks, current-route prerequisite/exclusion assertions, existing-building equality checks, naming checks and text-encoding scans. An independent reviewer caught and corrected the unsafe Wasit effect and the missing nationalisation transition timer. This report does not certify emitted tooltips, saves, native economic balance or multiplayer behaviour; those require the root integration tests and a real game.
