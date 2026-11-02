# Lessons from the implemented Soviet 1970 tree

Inspected 2026-10-18: emitted `common/national_focus/COLDWAR_SOV_1970_focus.txt` has 836 local focuses plus an attached Union joint-focus file. This is an architectural case study selected by the owner, not a required size or full correctness certification. No Soviet generator, validator or game test was run for this skill update.

Paths below are relative to TARGET_ROOT. They are discovery anchors; reread current code before adapting. Recipients without this mod can use the workflow but must establish equivalent providers in their target.

## Coherent layers and playable continuation

Institutional politics, outlooks/parties, leader programmes, economy, armed forces, internal state/Union and foreign policy form interacting programmes rather than unrelated PP gifts. Reforms have follow-up decisions and address actual starting problems.

For another country, map starting constraints -> institutions -> relevant political alternatives -> economic/military/diplomatic continuation. Approved alternatives need playable continuation beyond accession. Do not invent a Politburo or every ideology just to fill a coverage map.

Evidence: emitted sector roots, `cw_focus.py` (`SHORTCUTS`, `focus_file`) in `Claude outputs/COLDWAR_SOV_generator`; emitted `COLDWAR_SOV_gosplan_directives` opens planning decisions while granting a planning effect, and `cw_decisions.py` supplies the choices and expiry. Inspect both unlock and usable action.

## Classify the ownership of every gain

The implementation distinguishes permanent accumulated sector variables; party programmes gated by the actual governing party; leader programmes that additionally require the matching office-holder flag; timed ideas/burdens; and one-time outcomes such as construction or a signed agreement.

The lesson is ownership, not the five Soviet sector names. Leadership changes should preserve permanent national development while deactivating an old leader's programme where intended. Retaining earned variables can support later return. Check actual transitions and which effect becomes active again.

Evidence: `common/dynamic_modifiers/COLDWAR_SOV_1970_dynamic_modifiers.txt` (sectors from line 6, programmes from 183); `COLDWAR_SOV_clear_gensec` and `COLDWAR_SOV_install_gensec_*` in emitted scripted effects clear/set office flags and refresh modifiers.

## Match reward, purpose and cost

The audit records a verdict and precise override per focus. The emitted food programme changes agricultural outcomes, funds construction and removes an existing agricultural problem. Gosplan directives opens a real planning system. These are better patterns than attaching the same stability gift to unrelated titles.

For each material programme record policy goal, supported MD effects, payer/beneficiary, cost/duration, one-time/accumulating ownership, follow-up and competing route. Compare with similar current MD focuses and the target country's economy. Soviet cost tiers, reward scores and numerical ceilings remain that tree's review heuristics.

Evidence: emitted `COLDWAR_SOV_the_food_programme` near lines 26769-26800 and `COLDWAR_SOV_gosplan_directives` near 24604-24627; generator `overrides/*.json` and the compiler applying them. Recheck current final values.

## Keep truthful tooltips beside execution

The dynamic reward idiom is: ensure modifier exists -> show native change heading -> change exact mapped variable with localized per-stat tooltip -> refresh. Programme and permanent-sector variants share this form. Prove the custom modifier's consumer separately; a generated variable is not enough.

Refresh dependent Cold War/Imperia systems only when initialized and avoid redundant calls where one is sufficient. Do not execute an effect twice to obtain a preview. Evidence: `cw_effects.py` (`dyn_change`, `compile_effect` kinds `dyn`/`prog`), emitted Lenin centenary near lines 120-132, corresponding dynamic mapping.

## Separate candidature, authority and programme

Existing Politburo decisions/events resolve candidature and actual installation; programme eligibility reads the current office-holder flag. Becoming a candidate does not mean taking office. Alternative candidatures are not permanently exclusive merely because one person rules at a time.

Use each country's existing political system. A real accession/institutional decision is useful; a ceremonial focus merely unlocking the already-ruling party is not. Preserve exact prerequisite groups and party gates. Do not transplant Soviet voting, successor dates or flags elsewhere.

Evidence: `cw_focus.py` (`plenum_focus`), `cw_avail.py`, emitted candidate focuses and installation effects. Inspect the entire entry route, including existing outlook conditions.

## Complete the cooperative response contract

Offer helpers send a proposal; the receiver accepts/refuses and reports the result. The pipeline event charges its payer on acceptance and protects a one-time Soviet benefit with a signature flag. Trace proposed -> accepted/refused/expired where applicable -> actual outcome -> sender feedback -> pending cleanup. Verify re-entry, multiple targets and delayed replies instead of assuming one event is enough.

Joint focuses distinguish initiator/member rewards. State who may initiate, participate and receive each effect, following the native MD pattern and protecting simultaneous initiation. Do not add joint mechanics to an ordinary domestic reform.

Evidence: `cw_offers.py`, emitted offer helpers and `events/COLDWAR_SOV_1970_events.txt` (pipeline `.118`, replies `.900`/`.901`); `common/national_focus/COLDWAR_UNI_1970_union_joint.txt` and its membership trigger/provider.

## Trace design through review into loaded files

Use design DSL -> audit overrides -> layout/availability/effect compiler -> staged output -> installed files. `cw_layout.py` applies per-focus changes before compilation. Inspect representative rewards per relevant family, expanding to full coverage when requested or justified by findings.

Do not import build modules just to inspect them. `cw_build.py` deletes/rebuilds `out` and stages patches to shared history, generic focus and other files; installing them can overwrite later integrations. Establish output targets and compare loaded files before rebuilding/installing.

Some design prose still says 'not yet game code'; graph PNGs also predate the current coordinates. Use installed code to describe the current implementation. Graphs alone do not verify title/icon geometry or engine rendering.

## Transfer deliberately

Keep thematic depth, meaningful choices, explicit state ownership, real follow-ups, guarded refresh, consent and inspectable generation. Keep Soviet cohesion, SSR seats, Politburo, the particular 90-day project burden, Union missions and 836-focus size country-specific. New countries still need their own evidence, balance and current authorization.
