# Vietnamese military campaign expansion

The approved expansion adds 68 focuses to the existing national tree: guerrilla warfare and postwar security, Cambodia, and China. The complete tree has 307 focuses. The two limited Cambodian settlement continuations preserve an exit that does not require occupation. The military intervention route retains its distinct victory rewards.

## Defensive content against China

The later user correction replaces generic opponent bonuses and recurring economic penalties in four defensive postures with fieldworks, homeland defence and genuine terrain defence:

| Posture | Maximum entrenchment | Entrenchment speed | Defence on Vietnamese cores | Army defence in forest and jungle |
| --- | --- | --- | --- | --- |
| Survey the Defences | 1 additional level | 10% | | |
| A Northern Command | 2 additional levels | 15% | 3% | |
| Hold the Line | 3 additional levels | 20% | 5% | 5% |
| Defence in Depth | 5 additional levels | 25% | 8% | 10% |

The first two are preparation before war. Hold and Depth require an actual Chinese war. They retain 3 and 5 percentage points less maximum offensive planning respectively. These four postures add no supply consumption, bureaucracy or factory-output penalty. Their existing funding, duration, renewal and family-replacement rules remain. Offensive alternatives retain their own operating costs.

Entrenchment affects Vietnamese formations on every front; core defence applies on Vietnamese core territory. Terrain defence applies to the national army in forest/jungle against any opponent while the corresponding posture is active. It is implemented through native hidden terrain-training technologies, granted with the timed idea and removed with it. The engine's Italian timed-terrain pattern supplies the removal contract, while MD supplies the actual `category_army` forest/jungle defence syntax. A daily observer reconciles active ideas and their technologies without restoring expired policies or replaying payment. The directly adjacent northern states are 523 and 524; state 522 is the rear-area Red River Delta.

## Why intervention in Cambodia is worthwhile

The offensive preparation against Cambodia reaches 14% attack and 6% defence for 240 days, with 6% additional supply consumption and 2% lower military factory output. An actual secured military victory earns 25 army experience and two 20% land-doctrine discounts. A war goal does not declare a war or install a puppet.

After a real victory and a lawful friendly Cambodian settlement, **A Secured Southwest** can provide 6% agricultural productivity, 3% lower supply consumption and 2% additional bureaucracy expenses while its continuing security conditions hold. Agriculture is the actual native national agriculture calculation, not an immediate GDP/food grant or a southern-state-only effect. Its southern-control and partner conditions remain required.

Partner readiness can reduce the real continuing intervention burden. Verified land withdrawal ends the separate funded occupation/deployment policies; an actual remaining native advisory mission retains its lighter commitment burden until that mission genuinely ends. Sending an invitation, taking Phnom Penh or clicking a focus alone does not satisfy every obligation. The limited border agreement does not award the regime-change victory package or the friendly-partner dividend.

The victory review opens the friendly-partner continuation. The limited route instead requires its own verified settlement without a continuing Vietnamese occupation. The terminal regional focus requires an accepted regional conference. Accepted talks never make peace or withdraw divisions automatically.

## Runtime ownership

`approved_campaigns.json` is the immutable approved review snapshot, including the original concept-only status. Its SHA-256 is `ddce90a402e021c24693adf1eb61c3c92eab2cd49f2c2b0005de8a9f25e4e7d3`. It supplies IDs, positions, grouped prerequisites, exclusions, timing, descriptions and proposed effect values. `campaigns.py` compiles its integration into dedicated campaign ideas, effects, triggers, decisions, events and observers. `compile.py` appends the focus blocks and shortcuts to the existing tree and owns shared English localization and art registration.

The original 239-focus approval file is preserved. `runtime_design.py` records the deliberate correction of the two older Cambodian invitations: **CBD is Cambodia; CAM is Cameroon**. Guards, dispatch and recipient responses must all agree with that correction. The later defensive-policy correction is separately recorded in `campaign_defence_overrides.json`; its four effects and renewal explanation override the older campaign snapshot without changing that snapshot or the graph. The manifest records the override hash.

The new islands begin at (52,13), (60,13) and (68,13), with limited-settlement continuations at (56,20) and (56,22). Existing focus positions and the initial camera remain unchanged. The continuous panel moves to the verified empty lower-left gutter at (50,1750).

The later `focus_timing.json` policy sets the whole Vietnam tree to a 70-day standard, retaining only nine short survey, review, crisis and verification tasks at 35 or 42 days. Both immutable approval snapshots retain their original timings for provenance. Technical scenario gates remain hidden; actual Treasury requirements display their exact amount and current balance through native custom trigger tooltips.

## Contracts to preserve

- Display the promised effects independently from current execution guards. Actual rewards are funded, checked and stamped once. A preview must not pay or grant anything.
- Replace only the relevant policy family. Expired paid programmes do not return free, and initialization/refresh does not repeat XP, doctrine discounts or cash transactions.
- Track actual war participation, capitulation/control and lawful postwar outcomes. A peace-hook comment is not evidence that ROOT won a war.
- Distinguish actual native donor assistance from a diplomatic request or expression of interest. Native military offers originate with the donor; incoming type 6/7 support is verified on donor-scoped active programme data.
- Verify the intended current recipient, actual funds, eligibility and expiry when accepting any proposal. A consultation does not force another country's peace, units, government or territory.
- Ordinary occupation resistance/compliance is for real non-core occupation. It is not a generic insurgency model for Vietnamese-controlled cores, and it does not spawn NLF/FULRO units.
- Country occupation modifiers affect all qualifying Vietnamese occupations. Productivity-growth factors scale the actual signed growth calculation; they are not an unconditional penalty in every economic state.
- Keep all new English text readable, hide technical scenario checks, localize internal requirements, and use native small national-spirit art separately from focus icons.

Run the main compiler and validators, legacy transaction/political suites, and the independent campaign validator/transaction suite before delivering changes. Source checks and limited AST execution are not HOI4 engine or multiplayer tests. New hover, war, objective, assistance, withdrawal and save/reload checks still require a running game.

## Native providers inspected

- Main MD `common/ideas/generic_ideas.txt` and `Russian.txt`: native `targeted_modifier` with `attack_bonus_against` and `defense_bonus_against`.
- Main MD `common/ideas/arab_spirits.txt` and `Singapore.txt`: flat maximum entrenchment, entrenchment-speed factors and core defence. `max_dig_in` is a number of levels; the two factors use fractions displayed as percentages.
- Main MD `common/technologies/custom_tech.txt`: `category_army` with `forest`/`jungle` and `defence`. Base game `common/ideas/italy.txt` and its national focus file: a hidden terrain technology is enabled with a timed idea and set to zero in that idea's `on_remove`.
- Main MD `common/national_focus/05_afghanistan.txt` and doctrine documentation: army experience and finite land doctrine cost reductions. These grants do not select a grand doctrine or unlock modern militia automatically.
- Main MD `common/scripted_effects/00_budget_effects.txt` and money modifier definitions: treasury transactions, agricultural productivity and recurring national expense modifiers.
- This mod's `common/scripted_effects/mdcw_cold_war_effects.txt`: actual donor scoped type 6/7 state, size and expiry; donor initiated paid assistance; political support; overview refresh.
- Main MD investment GUI and `00_money_dynamic_modifiers.txt`: paid state rebuilding and its occupation limits. Campaign shortcuts give instructions and expose existing controls; the actual native investment retains its payment and timer.
- Installed engine trigger documentation: `num_divisions_in_states`, `controls_province`, ownership/control and military access checks. Cambodian states are 511 through 514; Phnom Penh is province 7376 in state 514.

These are source-level API checks. They do not replace running-game verification of engine behaviour or multiplayer balance.
