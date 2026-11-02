IMPERIA COLD WAR

# USA 1970 fiscal follow-through

Decision record: after this audit, the user explicitly selected keeping the existing services and accepting the deficit. The selected implementation is the tax-only correction, with no healthcare-class change, law downgrade or other retrenchment. This document retains the second-stage audit and unselected alternatives as evidence. Corporate 20 restores construction but creates a severe deficit with the inherited service and military bills; that is an accepted trade-off, not a balanced-budget claim.

## What the original fiscal observation does and does not establish

The retained engine log records weekly income 69.25320, corporate tax 49.76320, household tax 14.13042, other income 5.35958, expenses 54.85895 and a surplus of 14.39425 at corporate 48 and household 24. Internal GDP is 3941.76292 in year-2000 prices, with 208.19219 million people. The era helper explicitly stores internal GDP, costs and money on that price basis; the displayed 1970 GDP is divided by 3.4. Thus a weekly deficit must be multiplied by 52 and compared with internal GDP when reporting an annual GDP share. Confusing displayed GDP and internal money would add another factor-of-3.4 error.

Crucially, `common/scripted_effects/mdcw_communist_struggle_startup_effects.txt:114` seeds sanctions, refreshes state values, then applies each GDP profile and logs its budget. The final `IMP_sanctions_refresh_world` call follows the budget logs. The old log therefore is not a steady post-sanctions fiscal observation. The earlier -14.63428/week tax20 calculation was explicitly conditional on unchanged other readers; it understates the budget problem if the screenshot's sanctions blowback is applied afterwards.

The screenshot's +35.5% blowback consumer-goods factor implies `p = .355/.6`. Its corporate-tax effect is `-.35*p = -.20708333`, or -20.708333 percentage points of the corporate-income modifier. Under the known native USA tax-code contribution of +2%, the corresponding income-factor ratio is `(1.02-.20708333)/1.02 = .79697712`. This ratio is conditional on there being no other live corporate-income modifier. It is not correct to blindly multiply all income by .79291667. The source's productivity-growth channel also matters over time; it is not a one-time reduction of starting productivity. The current save's exact whole modifier set is not available to this source audit.

## Expense trace

| Weekly expense | Native observation or bounded derivation | Source |
| --- | ---: | --- |
| Defence | 9.52178 observed | `00_money_system.txt:2707`, industry plus personnel/equipment and capability costs |
| Bureaucracy | 5.46262 observed | population, cost modifiers and standard ladder level 3 |
| Education | 4.70827 observed | population, research slots/facilities and education ladder level 3 |
| Healthcare | 7.46301 observed | population, cost modifiers and health ladder 4.4 |
| Social spending | 12.79760 observed | population, cost modifiers and social ladder 4 |
| Police | 4.68953 derived | population 2081.9219 units, standard ladder 1.6, cost factor 1+.15+.14 |
| Remaining costs | 10.21614 residual | all infrastructure, interest and remaining native additional streams preserved |
| Total | 54.85895 observed | native `update_display` aggregates categories once |

The residual is deliberately not relabelled as entirely infrastructure. State-history aggregation independently resolves 65 USA-owned states at January 1970: 100 civilian factories, 62 military factories, 18 dockyards, 46 offices, 42 agricultural districts, 33 reactors, 21 renewable levels, 159 infrastructure levels, 242 air-base levels, 15 radar levels, 5 anti-air levels, 14 fuel-silo levels and 1 stronghold. Fossil plants are rebuilt by the demand-based startup helper and cannot be read from their deliberately zeroed history entries. Reactor/renewable and static infrastructure upkeep alone explain approximately 7.52 of the residual before fossil plants, interest and other streams. No live export of the residual's final subvariables was retained.

The welfare bill does not currently include a high-unemployment surcharge. Although the earlier log shows 30.5% unused workforce, the 1970 helper adds 35 percentage points to the unemployment threshold. The source resets the high-unemployment contribution and clamps it to zero below that threshold. The native spending ladders and weekly category accumulation were traced without finding a confirmed duplicate payment. Reducing the displayed cost by deleting an arbitrary category would conceal a real bill.

## Missing healthcare institution and historical limits

The USA 1970 initializer adds Basic Hospital Subsidies (`health_03`) but no healthcare-privatisation law. Native USA 2000 explicitly selects `fully_privatized_healthcare` while retaining the same hospital law, primary/secondary education law and basic pension law. Native Fully Privatized Healthcare has health costs -35%, healthcare-sector tax income -40% and healthcare workforce requirements -15%. Partially Privatized Healthcare instead supplies -15%, -20% and -8%. These are actual native effects, not a free income source.

The native Fully Privatized label is an MD abstraction, not a claim that the United States had no Medicare or Medicaid. [CMS's 2003 statistical tables](https://cms.hhs.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/CMS-Statistics-Reference-Booklet/Downloads/2003CMSStatistics.pdf), Table 37, show private sources financing 64.8% of personal healthcare in 1970, versus 57.0% in 2000. [HHS's historical financing review](https://aspe.hhs.gov/reports/long-term-growth-medical-expenditures-public-private-0) separately reports private funding at 62% of total national health expenditure in 1970. These definitions differ. They support a predominantly private financing class, not the deletion of public hospital support.

The missing class is a defensible institutional correction. With the current +18% healthcare cost factor, the native -35 percentage-point class reduces the observed 7.46301 health bill by about 2.21360/week, while lowering healthcare-sector receipts and labour demand. This is too small to fix the whole tax20 budget. Downgrading `health_03` to Basic Health Clinics or `social_03` to Minimal Pensions is a real retrenchment policy. Medicare hospital insurance covered roughly 20.1 million people in 1970 according to the [CDC/CMS historical table](https://www.cdc.gov/nchs/data/hus/2010/140.pdf). Such a downgrade should not be presented as an unambiguous historical correction.

## Two feasible native policy alternatives

These alternatives show a fundable direction with visible sacrifices. Neither has been installed as the historical default. Both preserve education03, policing02, all sanctions, Vietnam burdens, existing money stocks and all other recurring expenses. Both set household tax 31, retain the ordinary tax stability cost and one additional service-expectation step, and use native Fully Privatized Healthcare, Basic Civil Service Administration (`bureau_02`), Basic Health Clinics (`health_02`) and Minimal Pensions (`social_02`).

| Alternative | Corporate / household tax | Military budget | Construction lower bound | Conditional weekly balance | Annual deficit / internal GDP |
| --- | --- | --- | ---: | ---: | ---: |
| Investment and retrenchment, new start | 20 / 31 | Medium (`defence_03`) | 20 | -0.64917 | 0.86% |
| Same, preserving old 42/48 tax reduction | 17.5 / 31 | Medium | 30 | -2.63178 | 3.47% |
| Funded strategic commitment, new start | 23 / 31 | Sizeable (`defence_04`) | 8 | -0.15717 | 0.21% |
| Same, preserving old 42/48 tax reduction | 20.125 / 31 | Sizeable | 19 | -2.43717 | 3.22% |

The construction calculation removes the old hospital law's -1% consumer-goods factor, so its multiplier is `1.62/.99`. Upward rounding of demand produces the whole-factory lower bound. The budget model applies the conditional post-blowback income ratio and deliberately reserves the entire assumed upper-bound rate48 health-sector income of 2/week, scaled with tax and sanctions, rather than counting all its previous income after privatisation and the hospital cut. The resulting figures are cautious estimates, not engine-tested bounds on a changing economy.

The native military model separates the industry portion from the remainder of the observed 9.52178 bill. At the observed GDP per capita and 80 military/naval factories, the source industry formula gives approximately 4.91937/week. The empty-OOB startup's remaining 4.60241 is treated as personnel affected by the native mobilisation multiplier. Fixed equipment cost is assumed zero for this deliberately empty-force opening. Future forces, stored equipment or capability costs can invalidate that assumption. Health workforce/GDP, military productivity, further market changes, protests, growth and the later interest path are not fully simulated. The model retains the entire 10.21614 residual unchanged rather than treating it as savings.

The lower-tax old-save variants retain a meaningful extra deficit. At 120 initial cash, a deficit near 2.5/week gives roughly a year of reserves rather than eight weeks, and annual debt accumulation around 3% to 3.5% of the current internal GDP before growth and interest changes. Ordinary native borrowing and its fee continue. This is a manageable policy challenge, not a claim of permanent solvency. A player can choose more revenue at the expense of construction or restore services once the revenue base supports them.

The real native trade-offs are substantial. Bureau03 to02 loses 0.25 daily political power while improving construction speed by 5 percentage points. The hospital and pension reductions each lose 0.05 daily political power and 3 percentage points of stability; the hospital cut additionally loses recovery, productivity-growth and casualty-support benefits. Household24 to31 loses another 7 percentage points of tax stability. Medium rather than Large military spending sacrifices 22 percentage points of maximum efficiency and dockyard output, 30 points of military/dockyard productivity and 15 points of recruitable-population factor, while freeing 3 workforce points and recovering 10 stability points. Sizeable rather than Large sacrifices half those military deltas and frees 1.5 workforce points. The JSON includes every exact signed native-law delta.

These packages are credible alternate fiscal policies, not evidence that the historical United States funded only clinics or abandoned substantial Social Security. The historical hospital and pension institutions should remain available, visible and restorable. Selecting a package in a player-facing flow would need full native numeric previews and real law changes. Automatically applying the retrenchment package would be a separate design decision, not a verified parser fix.

## Delivery and remaining evidence

`tools/usa_1970_expansion/fiscal_options.py` creates only the analysis JSON. It changes no loaded runtime policy. The selected `economy.py` remains the limited tax20/old42-to17.5 correction, with its funding cost explicitly accepted. The independent review confirmed that its native guards and migration are safe, while separately identifying the sustainability limit. No HOI4 process was launched or controlled, and the player's campaign was not touched.
