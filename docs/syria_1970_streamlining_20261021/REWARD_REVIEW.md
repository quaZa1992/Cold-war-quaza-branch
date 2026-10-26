# Syria 1970: reward diversification review

IMPERIA CW — Cold War. Source inspection and bounded reward recommendations, 21 October 2026. This document does not certify HOI4 execution or multiplayer balance.

## Owned changes

`tools/syria_1970/streamlining_rewards.json` contains exactly 22 focus overrides. Each provides a complete replacement modifier dictionary, an English country-specific description and a numerical/reference note. Only the staff college adds a `one_time` item. The consumer must append that item; existing physical grants, treasury costs, durations, focus IDs, coordinates, prerequisites, exclusions and live access conditions are preserved.

No loaded game files or generator scripts were edited by the reward reviewer. Root integration owns migration and installation.

## Reasons for the changes

The installed pre-change manifest has 184 focuses using bureaucracy costs, 131 using political-power modifiers and 109 using stability. Several exclusive alternatives differ only in small generic values. The inland/coastal infrastructure fork and Soviet/diversified diplomacy fork have identical modifier dictionaries. Aleppo textiles and domestic medicines incorrectly use the military-factory-output modifier as their principal industrial benefit.

Summing national programme modifiers after choosing a maximum value from each mutually exclusive pair produces an upper bound of +132.6% bureaucracy spending and +48 percentage points of stability. This is a long-campaign arithmetic bound, not proof that all diplomatic, war and political access conditions can hold together. Party and leader programmes were not added to that bound. The source refresh does not impose a separate reward cap.

The changes replace selected generic increments with civilian productivity, investment administration, training, repair, fuel, equipment spending, agricultural receipts and naval roles. They do not increase every focus or erase the seven historical starting problems.

## The 22 changes

Percentages below are modifier magnitudes. `max_dig_in` is a flat entrenchment value. The interest, tax, investment and spending modifiers retain their native MD meanings.

| Focus suffix | Main outcome | Continuing drawback or opportunity cost |
| --- | --- | --- |
| `baath_01` | Mobilization +8%; command-point gain +5% | Research speed −2%; excludes the Front |
| `baath_02` | Civilian productivity +5% | Social costs +2%; political power −1%; excludes vanguard |
| `hafez_01` | Civilian productivity +6%; investment duration −8% | Tax receipts −2%; existing market exposure +2% |
| `hafez_02` | Army organization +4%; command-point gain +8% | Army personnel costs +4%; research −1% |
| `industry_01` | Civilian productivity +5%; factory efficiency gain +5% | Social costs +2%; excludes workshop route |
| `industry_02` | Civilian-factory construction +7%; office productivity +4% | Tax receipts −2%; existing market exposure +2% |
| `industry_06` | Civilian productivity +6%, replacing military output | Social costs +2% |
| `industry_08` | Health costs −3% | Education costs +2% |
| `industry_11` | Civilian productivity +4%; health costs −2%; existing factory retained | Education costs +1%; existing paid construction |
| `army_03` | Planning +8%; one 25% land-doctrine cost reduction | Education costs +2% |
| `army_06` | Attrition −5%; industrial repair +10% | Equipment costs +2%; does not magically replenish a stockpile |
| `army_07` | Army training time −5%; recovery +3% | Army personnel costs +2% |
| `army_09` | Army speed +3%; planning +8% | Army fuel use +4%; excludes defensive belts |
| `army_10` | Entrenchment speed +15%; maximum entrenchment +2 | Construction speed −1%; excludes mobile reserves |
| `infrastructure_01` | Infrastructure construction +8%; supply use −3% | Social costs +2%; excludes coastal concentration |
| `infrastructure_02` | Office productivity +6%; civilian productivity +3% | Receiving-investment cost +2%; excludes inland priority |
| `great_powers_01` | Army training time −5%; equipment-design XP cost −10% | Foreign-influence defence −3%; new aid still requires consent |
| `great_powers_02` | Licensed production +10%; investment duration −10% | Supply use +2%; licences/investments still require actual agreements |
| `agriculture_13` | Agriculture productivity +5%; agriculture tax receipts +4% | Social costs +3%; excludes food priority |
| `agriculture_14` | Agriculture productivity +4%; social costs −4% | Tax receipts −1%; excludes cotton priority |
| `navy_01` | Naval positioning +5%; coordination +3% | Navy fuel use +2%; excludes escort priority |
| `navy_02` | Convoy escort efficiency +10%; naval speed +3% | Navy fuel use +3%; excludes coastal denial |

## Native MD reference profile

All references were read in `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus`. Native focus cost is measured in focus points; nominal days are cost × 7. No other country's state IDs or modern political conditions are copied.

| Source focus | Native cost | Values used as calibration |
| --- | ---: | --- |
| `SOV_academy`, `05_russia.txt` | 3 / 21 days | Mobilization +5%; planning +5%; training time −10%; terrain penalty reduction +10%; Communist-government gate |
| `SYR_military_reform`, `05_syria.txt` | 5 / 35 days | Army, navy and air experience +15 each; native Syrian-content gate |
| `SYR_guerrilla_warfare`, `05_syria.txt` | 10 / 70 days | One 50% `land_doctrine` cost reduction; exclusive doctrine route |
| `SYR_decentralised_tactics`, `05_syria.txt` | 10 / 70 days | One 50% `land_doctrine` cost reduction; competing exclusive doctrine route |
| `PER_rials_behind_red_tape`, `05_iran.txt` | 7.2 / 50.4 days | Civilian productivity +5%; political power +5%; bureaucracy costs −2% |
| `PER_utilize_workers_house`, `05_iran.txt` | 7.2 / 50.4 days | Factory efficiency gain +10%; health costs −5%; social costs −5%; governing-Shia-party gate |
| `PER_control_tax_evasion`, `05_iran.txt` | 5.72 / 40.04 days | Agriculture tax receipts +5%; population tax receipts +2.5%; interest multiplier −15% |
| `SOV_roscosmos_intel`, `05_russia.txt` | 3 / 21 days | Naval coordination +5%; positioning +5%; land planning and recon +5% each |
| `PER_irgc_marines`, `05_iran.txt` | 5.72 / 40.04 days | Convoy escort efficiency +10%; convoy retreat speed +10%; invasion preparation −15%; governing-Shia-party gate |

The Syrian adaptation deliberately grants one 25% doctrine reduction instead of copying the modern Syrian 50% reward. The medicine sequence together reduces health costs by 5%. Training reductions from the NCO schools and Soviet standardization together reach −10%, matching the single Russian academy reference; none of these focuses grants foreign specialists without an agreement.

## Readers, scope and stacking limits

- `civilian_factories_productivity`, `offices_productivity`, agriculture tax receipts and equipment/personnel costs have real readers in `common/scripted_effects/00_money_system.txt`. Civilian productivity changes both the civilian economy and the associated native GDP calculation; it is not military factory output.
- `receiving_investment_duration_modifier` is consumed in `99_investment_scripted_effects.txt`. A negative value shortens an accepted investment; it does not create one. `receiving_investment_cost_modifier` retains its native project-cost meaning.
- `foreign_influence_modifier` is an outbound benefit in `00_influence_scripted_effects.txt`. The Soviet-route burden therefore uses **foreign_influence_defense_modifier −3%**, reducing Syria's resistance to foreign influence. A positive outbound modifier would not represent dependency.
- `mdcw_cw_market_exposure` already has a consumer in `mdcw_cold_war_effects.txt`; the existing merchant/workshop exposure is preserved.
- `army_morale_factor` is the native recovery-rate modifier. `max_dig_in = 2` is flat maximum entrenchment. Repair, escort, planning and training modifiers are documented in the local engine `modifiers_documentation.md`; numerical adaptations here are balance choices, not quotations of another focus.
- All improved national modifiers can coexist where their routes and conditions permit. Within these 22 overrides, the largest civilian-productivity route is **+18% national**, plus **+5% Ba'ath Front** and **+6% Hafez merchant** if the corresponding current authorities permit them: **+29% across those three layers**. This is a conservative arithmetic bound, not a complete campaign simulation. Private workshops choose a different, mutually exclusive industrial package and cannot be added to the state-enterprise total.
- This overlay introduces only **+5% factory efficiency gain**, through state-enterprise rehabilitation. No efficiency-gain modifier existed in the baseline Syrian programme, so the overlay does not build a route around an already saturated efficiency-gain cap.
- The staff college and mobile reserves add at most +16% planning together. Mobile reserves exclude the defensive-entrenchment fork. The two new training reductions total −10%. Medicine health savings total −5%. The largest office-productivity addition is +10% from private workshops and coastal concentration.
- These are **budget bounds**, not new runtime clamps. No arbitrary Syria-wide cap or global economy modification is introduced. Existing timed operational packages and their real war/fuel/personnel expenses must still be included in root's complete route tests.

## Required integration safeguards

Syria accumulates programme variables when each focus is implemented. It does not derive them afresh from completed focus receipts during every refresh. Existing saves therefore require a once-only modifier-delta migration for already implemented focuses, including zero-initialization for newly introduced keys. Do not rerun focus implementation or the existing entry-reward migration to achieve this.

The staff-college doctrine instruction must have a once-only delivery receipt. Root should define whether already completed staff colleges receive this new instruction as a compatibility supplement; programme refresh, office departure/return and duplicate delivery must never grant another use.

Preserve actual party, leader and coalition eligibility. Durable national gains stay national; Ba'ath and Hafez modifiers detach when their exact authority is absent and can return without replaying one-time grants. Prospective tooltips should show native numeric benefits and drawbacks even while the route is locked. No new geometric changes or forced foreign agreements are included.

## Separate source defect surfaced during review

`foreign.py` currently implements a pipeline transfer of $0.004 billion per 30 days with `treasury > 0.003999`. Updated project instructions require weekly recurring costs and at most five fractional digits in budget literals. Root should convert this contract to matching weekly payer/recipient transfers, approximately $0.00093 billion per week, preserve consent/termination and update all option/display values. This review does not change that script.

## Verification performed by the reviewer

The JSON parses, has 22 unique focus IDs present in the current manifest, preserves each focus's existing object-level cost/building/duration fields by omission, contains only native/locally defined modifier keys and adds exactly one named doctrine instruction. Reference values were checked against current main-MD source. No loaded outputs, real HOI4 execution, live hovers, save/reload or multiplayer synchronization were tested by this authoring subtask.
