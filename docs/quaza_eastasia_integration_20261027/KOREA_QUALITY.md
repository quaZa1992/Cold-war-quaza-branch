IMPERIA COLD WAR

# Korea branch quality and mechanics

Scope: North and South Korean focus rewards, selected bilateral programmes, their MD modifier consumers, 1970 reachability, and current source-model checks. This is a source review, not a claim of comprehensive balance or multiplayer stability. Japan is covered separately in `JAPAN_QUALITY.md`.

## North Korea

The 360-focus tree presents institutional alternatives with different outputs and costs. The starting spirits encode real constraints rather than workforce penalties: *Monolithic Ideological System* gives political power +0.10 and stability +0.06, while research is -0.05 and bureaucracy costs +0.08; *Extended Seven-Year Plan* applies productivity growth -0.12, factory efficiency gain -0.10 and bureaucracy cost +0.08. The focus remedies and investment routes can address these bottlenecks.

A representative political choice is the WPK path: *Monolithic Discipline* gives political power +0.16 and stability +0.08, but research -0.06 and bureaucracy cost +0.10. Its exclusive *Collective Deliberation* alternative gives research +0.07 and productivity +0.06, at stability -0.06 and bureaucracy cost +0.08. Neither option is universally dominant: one favors political control, the other productive and technical capacity.

The food and industrial routes also differentiate priorities. *Public Distribution* costs 0.75% of current GDP once for agriculture +0.06 and stability +0.04, with social expenditure +0.06 and tax multiplier -0.03. *Tolerate Local Markets* costs 0.50% GDP for productivity +0.04 and tax multiplier +0.04, while political power falls by 0.04 and police cost rises by 0.04. Separately, *Prioritize the KPA* and *Fund Civilian Recovery* each cost 0.75% GDP: the former adds army organisation +0.08 and reduces supply use by 0.04, but raises personnel costs by 0.06 and slows industrial construction by 0.06; the latter adds productivity and agriculture +0.06 each, lowers personnel costs by 0.05, and reduces army organisation by 0.05.

Costs and magnitudes are grounded in native consumers, not just tooltip strings. `tools/north_korea_1970/compile.py` gates focus spending on positive `gdp_total` and emits MD treasury effects and dynamic modifiers. `tools/north_korea_1970/agreements.py` quotes current GDP and converts annual commitments to weekly units; the installed economy hook calls the NKO weekly expense path from `common/scripted_effects/00_money_system.txt`. For example, the Soviet industrial contract charges North Korea 1.25% of current GDP at setup and an annual commitment of 0.15% GDP, paid weekly; the Soviet side pays 0.025% GDP setup and 0.02% annually. It grants an industrial complex and distinct productivity, efficiency and energy effects, while foreign influence defense falls for North Korea. Values are saved at offer/commitment boundaries and require recipient consent; suspension and restoration are separate from setup payment.

## South Korea

The canonical loader expands the approved 298-node base design with two revision-3 focuses (`usfk_presence` and `combined_exercises`), producing 300 emitted focuses. Fixed MD treasury costs distinguish domestic programmes from NKO's GDP-share budget model. For instance, *Village Grants* costs $3 million weekly for agricultural productivity +0.12 and political power +0.04, but stability -0.03. *Village Elections* costs $2 million weekly for agricultural productivity +0.09 and stability +0.05, at political power -0.05 and bureaucracy cost +0.03. *Connect the Provinces* costs $2 billion once and adds one infrastructure level to each of states 606 and 607, with one shared slot per level; execution checks state ownership/control and available native capacity. *Advanced Exports* costs $2 billion once, reduces building workforce requirement by 3% and raises civilian factory productivity by 0.04, while education costs rise by 0.04. None of these uses a negative available-workforce-size penalty.

The USFK options are materially different bargains. The five-year Garrison agreement charges Korea $2 billion setup plus $2 million weekly, and the United States $2 billion setup plus $4 million weekly. Korea receives core defense +0.06, army organisation +0.03 and personnel costs -0.03, while foreign influence defense falls by 0.08 and bureaucracy costs rise by 0.03. The five-year Drawdown costs Korea the same setup and weekly amount, but the United States pays $1 billion setup with no recurring fee. Korea gains foreign influence defense +0.08 and arms production speed +0.10, at core defense -0.06 and personnel costs +0.10. Combined Command instead costs each side $1 billion setup and $2 million weekly; Korea gains planning speed +0.08 and army organisation +0.04, with foreign influence defense -0.05. These trade-offs make the offers distinct and leave agreement activation dependent on acceptance.

The native consumer chain is in the emitted focus/effect and decision files, the KOR dynamic modifiers and `common/scripted_effects/00_money_system.txt`: contract income/expense hooks and the programme weekly-cost helper apply costs only to signed or active agreements/programmes. Preview terms now include both parties' prospective numeric outcomes before agreement, without activating or charging either side. The party branches remain inspectable and use exact native party-in-power requirements for execution. Focus routes tied to Park Chung-hee, Kim Young-sam, Kim Dae-jung, Chun Doo-hwan, Roh Tae-woo and Kim Jong-pil use actual leader identity checks. These are leader-based historical gates, not merely focus calendar locks.

KOR politics events `.100` through `.114` retain their original date and trigger conditions but now use a bounded daily dispatcher with a two-day queued receipt and separate delivery receipt. If the event is dropped after its gate changes, the queue expires and permits a later retry; once delivered, a human's unanswered event cannot be duplicated. AI and human option authority and one-time outcome receipts remain in the options. This is an explicit next-day scheduling rule, not stochastic MTTH behavior.

## Verification and limits

The installed KOR validator passed with 300 focuses and 104 sprite records. The KOR bounded runtime scenario suite passed 24 named cases, including building-slot grants, construction guards, offer/replay behavior, and the event-dispatch retry/delivery cases. These establish modeled source invariants only. Tree parsing, native trigger/effect source checks and the selected modifier readers do not prove live tooltip rendering, save/rehost behavior or multi-client OOS stability.

The final native engine probe passed all 26 assertions with zero targeted diagnostics, as recorded with exact scope in [ENGINE_REPORT.json](ENGINE_REPORT.json). NKO's installed validator passed 1,150 modeled transaction/lifecycle cases. These are separate evidence levels; the native fixture is a single client, with no live raid combat or save/rehost proof.

## Sources

- NKO: `tools/north_korea_1970/current_design.json`, `compile.py`, `agreements.py`, and emitted `common/scripted_effects/COLDWAR_NKO_1970_*.txt`.
- KOR: `tools/COLDWAR_KOR_1970_concept/approved_design.json`, `COLDWAR_KOR_runtime.py`, `COLDWAR_KOR_runtime_foreign.py`, `COLDWAR_KOR_runtime_politics.py`, `COLDWAR_KOR_runtime_validate.py`, and `COLDWAR_KOR_runtime_scenarios.py`.
- Consumers: `common/scripted_effects/00_money_system.txt`, KOR/NKO dynamic modifier and scripted-effect files, and `history/countries/KOR - Korea.txt`.
- Integration and validation scope: `INTEGRATION.json`, `VALIDATION.json`, and `ENGINE_REPORT.json` in this directory.

