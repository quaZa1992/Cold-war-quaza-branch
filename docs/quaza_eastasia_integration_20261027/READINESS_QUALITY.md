# IMPERIA COLD WAR - Nuclear Readiness quality review

## Scope and evidence

This review covers the installed Nuclear Readiness scripts and their generator under `tools/nuclear_readiness/`, the native nuclear raid and money-system integrations, and the currently emitted player interfaces. It is a source review of the 1970 scenario. It does not certify multiplayer synchronization or live game performance.

The readiness regression suite reports 41 tests passed with zero failures or errors. Its only omitted test, `test_generation_is_deterministic`, calls the artwork writer; generator/output parity was checked separately without writes. These are source-level assertions, not native-game proof. The prior standalone readiness native report at [`engine_report.json`](../../tools/nuclear_readiness/engine_report.json) records 16 scenario assertions passed in a single-player fixture. That run is not proof for the current combined East Asia import. The combined East Asia fixture stopped with a native `C0000005` crash after six startup tree and leader assertions, and had logged invalid DDS texture payloads for the NKO memorial and funeral news assets. The assets have since been converted to DXT5 with one mip; the combined rerun subsequently passed all 26 native assertions with zero targeted diagnostics. Treat those evidence classes separately.

## Historical fit and design

The 1970 start aligns with both deterrence and arms-control diplomacy. The SALT talks formally opened in November 1969, and a July 1970 U.S. decision memorandum instructed its delegation to pursue verifiable numerical limits on strategic systems. The Non-Proliferation Treaty entered into force on 5 March 1970. Those precedents support a mechanic that gives leaders warning, intelligence assessments, allied consultation, reciprocal communication and an escalation ladder, rather than making nuclear use automatic. NATO had adopted flexible response in 1967, a strategy that retained conventional and nuclear responses across an escalation spectrum. The five readiness levels and their percentages are gameplay abstractions; they should not be read as historical DEFCON levels or literal percentages of real arsenals.

Sources: [U.S. Office of the Historian, SALT I and II](https://history.state.gov/milestones/1969-1976/salt), [U.S. National Security Decision Memorandum 691, 9 July 1970](https://history.state.gov/historicaldocuments/frus1969-76v32/d94), [United Nations Treaty Collection, NPT entry into force](https://treaties.un.org/pages/showDetails.aspx?objid=08000002801d56c5), and [U.S. discussion of NATO flexible response](https://history.state.gov/historicaldocuments/frus1981-88v01/d91).

## Mechanics and balance

### Readiness, authority and nuclear use

The system enables only in the 1970 scenario with the required Götterdämmerung DLC. A country counts as a nuclear power only while it has at least one `nuclear_missile_equipment` or `nuclear_ballistic_missile_equipment` in stock and has not capitulated ([scenario and DLC gate](../../common/scripted_triggers/COLDWAR_nuclear_readiness.txt:2), [stockpile provider](../../common/scripted_triggers/COLDWAR_nuclear_readiness.txt:3), [raid gates](../../common/scripted_triggers/COLDWAR_nuclear_escalation.txt:70)). Readiness is initialized at Routine Deterrence, level 5. Each order costs 25 PP; moving toward a more alert level takes two days per level step, so maximum readiness from level 5 takes eight days. Returning to a less alert level applies immediately ([order effect](../../common/scripted_effects/COLDWAR_nuclear_readiness.txt:162)).

| Level | Ready share | Protected reserve share | Cost factor | Fatigue change per day |
| --- | ---: | ---: | ---: | ---: |
| 5, Routine Deterrence | 15% | 10% | 1.00 | -2/day |
| 4, Increased Vigilance | 30% | 15% | 1.15 | -2/day |
| 3, Reinforced Readiness | 50% | 25% | 1.40 | 0.25 |
| 2, Strategic Alert | 75% | 40% | 1.80 | 1 |
| 1, Maximum Readiness | 100% | 50% | 2.50 | 2 |

Fatigue is clamped from 0 to 100. Its derived value is `-0.0005 x fatigue` and is read by the `stability_factor` on `COLDWAR_nr_strategic_forces`, reaching -0.05 at the cap ([dynamic modifier](../../common/dynamic_modifiers/COLDWAR_nuclear_readiness.txt:2)). Tactical launch availability begins below level 4 with at least one ready weapon; state attacks begin below level 3 with more than 19 ready weapons; strategic attacks require level 1 and more than 199 ready weapons ([readiness triggers](../../common/scripted_triggers/COLDWAR_nuclear_readiness.txt:93)). The native raid files still require their stockpile and doctrine checks, then recheck the integrated readiness gate in launchable phase. Each native hit routes once to the readiness recorder ([tactical raid example](../../common/raids/nuclear_raids.txt:182), [recorder](../../common/scripted_effects/COLDWAR_nuclear_readiness.txt:821)).

Peacetime first use is human controlled: the initiator must be a human, a non-subject with the offensive `nuclear_power_off` idea and either full first use or tactical-first-use/strategic-retaliation doctrine. The initiating state must be at maximum readiness, outside stand-down, and target an independent state outside its faction with no non-aggression pact. Preparation is restricted to that target; release authorization starts only after the 72-hour ultimatum and lasts 168 hours unless revoked or cancelled. The same pair is subject to a 90-day cooldown after use. Native raid launch still requires the target and doctrine gates ([policy and context](../../common/scripted_triggers/COLDWAR_nuclear_escalation.txt:2), [launch conditions](../../common/scripted_triggers/COLDWAR_nuclear_escalation.txt:77)). In an existing war, native doctrine can authorize attacks without this peacetime release path.

The diplomacy is not an automatic agreement transaction. Warnings cost 50 PP and need no acceptance; counters cost 25 PP. Hotlines and stand-down offers cost 15 PP, require recipient acceptance, remain open for 14 days, use a 21-day sender cooldown, and are invalidated if either side's strike revision changes. Withdrawal is free. The first-use posture blocks AI initiators; the exposed native raid consumers are `is_able_to_use_nuclear_strikes`, `is_able_to_use_nuclear_strikes_tac`, plus the built-in `nuclear_power_off` and first-use doctrine checks. Recipient-side AI acceptance remains an engine behavior to observe in the combined game test ([diplomatic actions](../../common/scripted_diplomatic_actions/COLDWAR_nuclear_readiness.txt:2), [offer receipts](../../common/scripted_effects/COLDWAR_nuclear_readiness.txt:410)).

### Monetary units and player-visible costs

All rates are expressed as billions of dollars per week and are added once to MD's weekly `defence_gain`, then carried into `display_expense` and `treasury_rate` ([MD economy integration](../../common/scripted_effects/00_money_system.txt:3335), [weekly expense aggregation](../../common/scripted_effects/00_money_system.txt:4684), [treasury rate](../../common/scripted_effects/00_money_system.txt:4749)). This matches the project's other weekly monetary streams, including nuclear development upkeep, rather than charging each time the GUI refreshes.

The source formula is:

- Strategic forces: `((0.00001 x total missile stock) + 0.002) x readiness factor x fatigue factor x GDP/c factor x inflation multiplier`.
- Civil defence: `(0.00002 x GDP + 0.002) x inflation multiplier` while preparing or active.

GDP/c is scaled by `GDP per capita / 36`, clamped to 0.4-1.2. Inflation is clamped to 0.01-100. Fatigue raises force upkeep by 0.5% per fatigue point. For a 1,000-weapon arsenal at GDP/c 36 and inflation 1, level 5 costs $0.012B/week; level 1 costs $0.030B/week before fatigue. At $1,000B GDP, civil defence costs $0.022B/week. The source test's native probe recorded the $0.012B/week 1,000-stock level-5 case. For comparison in the same MD budget, the current NKO nuclear development provider charges $0.15384B/week for bomb research and $0.09615B/week for warhead research before its GDP/c and inflation scaling ([development provider](../../common/scripted_effects/COLDWAR_nuclear_development_budget.txt:1)).

Civil-defence mobilisation costs 25 PP, takes three days to prepare, then continues until the player stops it or capitulation ends it. While active it reduces factory construction speed and industrial capacity by 3% and reduces the native casualty-rate input by 20% in the two nuclear casualty callbacks ([effect and budget](../../common/scripted_effects/COLDWAR_nuclear_readiness.txt:110), [modifier](../../common/dynamic_modifiers/COLDWAR_nuclear_readiness.txt:7), [native casualty callbacks](../../common/scripted_effects/mdcw_imperia_nuclear_effects.txt:15)). There is an explicit stop control. No auto-expiry means players need to monitor its recurring expense.

### Counterforce, pollution and sanctions

A recorded hit removes part of the victim's exposed stock: the effect multiplies the raid's 5%, 15% or 40% counterforce fraction by the portion outside the reserve share, rounds losses by missile type, and refreshes readiness. A source and native scenario assertion check that a 1,000-stock victim with a 50% reserve retains 800 after a 40% strategic counterforce fraction. The raid's ordinary native population, infrastructure and contamination effects remain in force. Civil defence only scales the casualty-rate input; it does not remove contamination, restore buildings or blunt other nuclear raid effects.

Peacetime first use that successfully opens a war applies -5 percentage points stability, +20 global Cold War tension when that system is initialized, +10 named threat, a 365-day aggressor flag, and condemnation opinion from all countries. It does not itself add an economic sanction. Existing sanction systems remain separate. The actual pollution, national sanctions and downstream country-specific reactions require native gameplay observation; the source does not establish that civil defence contains those effects ([first-use resolution](../../common/scripted_effects/COLDWAR_nuclear_escalation.txt:170)).

## Save, multiplayer and performance

State is stored per country: readiness, order, transition days, fatigue, civil-defence days, opponent, initiator, crisis serial and strike revisions. The reciprocal pair trigger checks that the other country exists, has not capitulated, points back to the same participant and has the same serial. A new hit increments the revision, so pending diplomatic offers and first-use authority are invalidated when the stockpile state changes. The one-time init flag supplies defaults; the hourly ultimatum event advances the 72-hour clock in two-hour increments. Source checks cover repeated offers, invalid pairs and hour timing, but a rehosted multiplayer save has not yet been demonstrated.

The daily on_action is country-scoped. It runs the readiness lifecycle for countries with missile stock or a saved `COLDWAR_nr_initialized` flag. Each eligible country recalculates stock, readiness shares, costs, fatigue and first-use validity; it has no all-state loop. The 72-hour timer uses 36 scheduled two-hour events per active initiator. A warning/ultimatum sends notifications to other human countries with one campaign-wide country iteration at crisis start, not every day. These are source operation bounds, not measured frame time or OOS evidence.

**Low-severity performance finding:** The free `COLDWAR_nr_open_command` decision has no nuclear-stock availability guard. Any human in the enabled scenario can open the interface, causing `COLDWAR_nr_init` to set the permanent initialized flag. The daily hook then continues to run for that country even if it has no weapons, because the hook admits every initialized country ([open decision](../../common/decisions/COLDWAR_nuclear_readiness.txt:2), [daily hook](../../common/on_actions/COLDWAR_nuclear_readiness.txt:3)). Gate opening or first initialization on `COLDWAR_nr_nuclear_power`, or explicitly clear initialization when a country has no active readiness state, to avoid a needless per-day loop for non-nuclear users. This does not affect core nuclear-country behavior.

A save loaded with the DLC or scenario condition disabled is an unresolved lifecycle edge. The on_action no longer ticks once `COLDWAR_nr_enabled` is false, so active dynamic modifiers and stored crisis state may not receive their usual cleanup. No test here proves the behavior of changing DLC availability across saves; keep the gate conditions stable for an active campaign and include that case in a future save/rehost rehearsal.

## Weaponless assessment correction

The assessment now starts at unknown/zero and only reads a target's readiness level inside a `PREV = { COLDWAR_nr_nuclear_power = yes }` guard. A target with no missile stock therefore receives an unknown-confidence report instead of a guessed level, and cannot trigger the hidden-readiness tension penalty. The assessment event may still report that the available evidence is insufficient, which matches its localisation. The source regression is [`test_weaponless_target_does_not_receive_a_nuclear_readiness_assessment`](../../tools/nuclear_readiness/test_readiness.py:321), and the emitting behavior is in [`COLDWAR_nr_assess_prev`](../../common/scripted_effects/COLDWAR_nuclear_readiness.txt:749).

## Checks and remaining proof

The reported 41 source checks and the older standalone 16-condition native report are separate from the current combined East Asia native fixture. The combined fixture's first attempt ended in an actual `C0000005` crash after six startup identity/tree checks, with invalid texture payload diagnostics for the newly imported NKO memorial and news images. The corrected DXT5/mip-1 assets passed the combined rerun: 26 native assertions, zero targeted diagnostics and no crash. This proves the specified startup, succession and readiness helper paths, not manual event UI, live pollution interactions or cross-feature save state.

Even after a successful single-client run, OOS and RP stability remain untested. The remaining proof is a two-client session covering simultaneous warnings, accept/reject races, a raid during a pending offer, both sides' stand-down, a save/rehost during the 72-hour countdown, a nuclear strike in an existing war, and scenario/DLC save continuity.
