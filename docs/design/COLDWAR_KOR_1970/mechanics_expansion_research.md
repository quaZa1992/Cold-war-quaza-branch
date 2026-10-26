# South Korea 1970–1990: mechanics research for concept expansion

**Research only.** This report maps the current 206-node design to installed MD/Imperia mechanics and recommends areas for a substantial design expansion. It does not change the design, implement providers, or authorize loaded-mod edits. Source anchors refer to the current checkout and should be rechecked when implementation begins.

## Findings at a glance

The codebase already has native mechanics for changing the actual ruling party and election status, party popularity, coalition composition, country stability, literacy and education spending, labor-faction opinion, weekly money accounting, regional building construction, reactor-safety targets, and recipient-consent diplomacy. Use those systems where they fit.

I found no general native “political legitimacy,” judicial independence, press freedom, or civilian-control-of-the-military modifier or meter. Similar words in focus text or a custom modifier registration would not provide those outcomes. Treat these as institutional states that need explicit KOR-specific flags/ideas, action/transition providers, guards, and removal/repeal rules—or express only the supported consequences (elections, party access, stability, costs, etc.) and avoid claiming a metric the game does not calculate.

The most important structural corrections for the expansion are:

1. Build a playable, event-resolved 1979–87 military-to-civilian transition. The present tree has Chun/Fifth Republic, liberalization, and direct-election nodes, but a substantial political handover must connect actual crisis outcomes to office, elections, and opposition access.
2. Separate durable national institutions from party/leader programmes. An independent court, lawful unions, election rights, or press protections should survive a normal cabinet change until an explicit rollback, while a party’s economic programme may deactivate when it leaves office.
3. Turn material “requirements” from prose into executable guards. The current civil-nuclear gate is a clear example: its requirement says “native safeguards, technology and projects,” while its exact proposed gate only tests KOR/scenario/subject status.
4. Add a whole-tree stacking ledger. The replacement rule limits a named policy slot; it does not limit totals across numerous different slots and independent national policies.
5. Make industrial, rural, urban, labor, education, defense, and diplomacy choices change their intended system. A shared stability or productivity percentage alone cannot carry all those meanings.

## 1. Politics, legitimacy, and transition

### Existing political APIs

`common/scripted_effects/00_MD_politicsview_scripted_effects.txt:136–155` provides `add_ruling_outlook_popularity` and `modify_election_threshold`. The latter accepts `threshold_change`, updates `election_threshold`, clamps it to 0–0.10, and refreshes the politics view. It is a threshold rule; it is not a legitimacy meter or a guaranteed victory.

`change_ruling_party_effect` is the native office transition primitive (`common/scripted_effects/00_MD_politicsview_scripted_effects.txt:1980–2076`). Its documented temp inputs are `rul_party_temp`, optional `col_one` through `col_five`, `change_leader_temp`, and `disable_elections`. It changes the actual `ruling_party`, rebuilds the coalition array, sets `elections_allowed`, updates coalition strength, calls `set_leader`, and invokes relevant native integration hooks. For KOR this is the right primitive for an actual handover, but the new KOR transition dispatcher/flags and sync hooks remain proposed providers. A party popularity change, focus completion, or coalition member is not the same as an office transition.

The native concepts are separate:

- **Government identity:** actual `ruling_party`, elected/appointed leader, election status, and coalition array.
- **Political support:** outlook/party popularity and its effect on elections.
- **Political performance:** standard `stability_factor`, `political_power_factor` / `political_power_gain`, and other supported modifiers. Do not label political power as legitimacy.
- **Institutional legitimacy:** no general reader was found that calculates this as a country score. A KOR “legitimacy” consequence would need a new stateful system and consumer, or should be expressed as named, supported outcomes rather than a fabricated stat.

### Transition design recommendation

Treat the military-to-democratic sequence as an actual transition spine that unlocks branches, not as a regular set of Chun focuses. Preserve entry by the scenario’s real date and political outcome: Park’s end of office, Choi Kyu-hah’s interim role, the military seizure, Gwangju/repression, and the 1987 direct-election settlement need distinct receipts or existing native events that can be checked. Then connect the direct-election guarantee to the actual election/party change through `change_ruling_party_effect`; do not select an opposition incumbent automatically when the declaration is accepted.

The political branch then needs to remain available to successful civilian opposition governments. Current KOR NDP/reform programmes are gated by actual party slots, which is good, but the design must identify how a real transition places them in office and supplies the correct incumbent. The 1970 registry and current native pools do not already represent the full later 1980s party map; the previous mechanics review documents that migration as proposed, not implemented.

### No generic court, press, or civil-command stat

The current native `has_repressive_government` / `has_not_repressive_government` scripted triggers (`common/scripted_triggers/01_political_reform_triggers.txt:3–63`) check for a set of named censorship/closed-country ideas. This is a useful eligibility gate but does not grant press freedom, remove KOR repression, or create graduated levels by itself. No generic judicial independence, constitutional compliance, press freedom, or civilian-command modifier was found in modifier definitions or common scripted APIs.

For the expanded court/oversight/press programme:

- Define discrete national institutional states (for example, independent review authorized, emergency powers narrowed, civilian appointment authority, legal press protections) with explicit receipts and exact transition/rollback actions. Avoid presenting `stability_factor` or `trade_opinion_factor` as a court or press mechanic.
- Gate dependent choices on those receipts at availability and completion. A path prerequisite documents history, but a live institutional requirement should be tested in the exact guard.
- If a receipt removes or downgrades existing censorship ideas, enumerate the supported KOR starting ideas and define the exact removal/swap path. A generic repression trigger only tests their presence.
- Keep a party’s governance programme separate from the national institution it enacted. Government changes should deactivate the former where intended but should not silently abolish the latter.

The existing `constitutional_court` focus currently proposes stability/political-power/bureaucracy modifiers and a one-time cost; its effect catalogue does not itself establish a judicial review system. Likewise, `civilian_security` lists an oversight action but its current numeric policy alone cannot make intelligence agencies answerable to elected authorities. These are good subjects for a new institutional provider, not evidence of an existing API.

## 2. Labor relations and social compact

`change_labour_unions_opinion` is a real MD scripted effect (`common/scripted_effects/00_internal_faction_effects.txt:1245–1266`). It takes the signed `temp_opinion` value, updates `labour_unions_opinion`, clamps to 0–100 using registered country modifiers, shows an opinion tooltip, and refreshes the labor-union dynamic effect. **It only runs its body if the country has the `labour_unions` idea.** The KOR 1970 history block (`history/countries/KOR - Korea.txt:5–56`) does not grant that idea or set an education-budget idea. `edu_04` appears later, under the 2000.1.1 history block at line 735, and must not be used as proof of the 1970 state. No other 1970 initialization provider was verified in this research, so the effective 1970 education-budget and labor-faction starting state remain unresolved until the scenario initialization chain is traced. Therefore the existing labor effect is not a plug-and-play provider for KOR's proposed independent-union policy. The expansion should use an explicit KOR native faction-registration provider with an already-present check, initialize only when absent, and preserve existing opinion; do not call blind `increase_education_budget` or labor-opinion effects.

The native education/labor/economy systems can support a real bargain: show the wage/productivity choice, its actual recurrent expense and productivity/workforce outcomes, and how labor-faction opinion changes following enacted policy. Do not use an opinion delta alone to imply independent union legalization. Add historical political hooks for labor organization and repression as relevant, while keeping a legal left cabinet distinct from labor being influential under another party.

## 3. Education, skills, and research

KOR's effective 1970 education-budget idea has not been established. `edu_04` occurs in the later `2000.1.1` block of `history/countries/KOR - Korea.txt:722–740`; the actual 1970 block at `:5–56` does not set an education budget. The existing `increase_education_budget` family in `common/scripted_effects/00_budget_effects.txt:374–467` swaps among `edu_01` through `edu_05`; a call on the maximum level can fall through to a political-power grant instead of raising spending further. Trace the 1970 scenario initializer first, then decide whether and how to integrate that existing budget system. A budget-level change is not a direct literacy or technology grant.

The education subsystem also has a measured literacy path:

- `literacy_rate_education_modifier` is registered country-scoped as a percentage (`common/modifier_definitions/modifier_definitions.txt:70–77`).
- `EDU_check_education_spending` (`common/scripted_effects/00_education_effects.txt:134–146`) samples a literacy change between the modifier minus 0.05 and the modifier, then stores it.
- `update_literacy_rate_event` and `update_literacy_rate` (`:148–180`) apply and clamp literacy to 0.01–1. They refresh `education_dynamic_modifier` and recalculate agriculture math where the country is classified as agrarian.
- `education_dynamic_modifier` maps literacy into research speed, education expense, productivity growth, office productivity, and uneducated-worker agriculture effects (`common/dynamic_modifiers/00_MD_dynamic_modifiers.txt:168–176`).

For expansion, distinguish education budget, actual literacy progress, technical-college/skills policy, and targeted research. Do not translate “education” into an unverified flat research buff. A focus that grants a technology bonus must use a category actually used by technologies; doctrine reductions are a separate API. Check current definitions before selecting category tokens.

## 4. Rural development, urban services, and regional investment

The prior mechanics review traced `agricolture_productivity_modifier` to country-level agriculture tax, rural-worker GDP, and productive agriculture calculations (`common/modifier_definitions/money_modifier_definitions.txt:353–359`; `common/scripted_effects/00_money_system.txt:412–420, 5344, 6055`). It is a national agriculture productivity input, not a per-province yield, irrigation, or building level. The current DRP rural choices use this global modifier, so they should not be described as geographically targeted village production unless they also add actual regional development.

State construction is the grounded way to make an urban/rural or regional project geographically specific: use a state-scoped building effect with owned/controlled state, building-type, capacity, geography and atomic-cost checks. The previous report identifies KOR states 604–608, but historical state files are not proof of effective free capacity after scenario initialization. Prefer one or a few consequence-bearing project choices over stat-only “balanced development.”

Make “rural development” and “urban services” measurably different. Rural productivity, education, local infrastructure, clinic/service access and farmer income distribution are not the same mechanic. Existing code can represent agriculture productivity and state buildings; it does not supply a per-state service or regional-equity score. Any claimed service/inequality measure needs an explicit new reader or should be modeled by concrete state investments and limited, explained national effects.

## 5. Civilian industry and sector choices

The latest concept correctly replaces civilian-economic output claims with `civilian_factories_productivity`, whose MD readers are actual and country-scoped (`money_modifier_definitions/money_modifier_definitions.txt:381–386`; `common/scripted_effects/00_money_system.txt:469, 6027`). It changes the civilian-factory tax component and civilian-factory GDP contribution, not all national GDP and not HOI4 production-line output. Its label is “Civilian industry productivity”; include the tooltip caveat already added in the concept.

For production construction, distinguish:

- `production_speed_industrial_complex_factor`: speed of building industrial complexes, not their output.
- `production_speed_buildings_factor`: construction speed for the specified building category in the host API; confirm the exact target when composing dynamic modifiers.
- `industrial_capacity_factory` / `production_factory_max_efficiency_factor`: military production capacity/production-efficiency fields. The prior review correctly confines them to defense-focused content.
- `civilian_factories_productivity`: Imperia civilian tax/GDP calculation, never substitute it for civilian factory game output.

Heavy-chemical, steel, machinery, shipbuilding, or export clusters should be differentiated with actual construction in suitable Korean states, relevant existing technology bonus categories, and source-traced labor/finance effects. A new “steel productivity” percentage would need a registered definition and consumer; do not infer it from the sector’s label. For any `add_tech_bonus`, inspect the current technology tree for actual technologies in that category. For `add_equipment_bonus`, confirm that the target equipment type/name exists. Use `add_doctrine_cost_reduction` only for an actual doctrine category.

## 6. Professional defense, conscription, and civilian authority

Existing national modifier fields support conventional defense trade-offs: army attack/defense, core defense, organization, morale, training time, supply consumption, conscription, equipment production and costs. They represent military performance/manpower/cost, not professionalization or the constitutional subordination of officers. The current concept’s “professional core,” “reserve army,” “career NCOs,” and “retire political officers” need a clear chain from chosen institution to supported modifiers and from national military changes to the political transition state.

Recommended architecture:

- Separate force structure (reserve versus paid professional core) from command governance (civilian appointment, military withdrawal from politics) and training/doctrine (NCOs, combined arms, logistics). Each category should have non-duplicative outcomes and visible cost.
- Keep defense readiness and conscription effects nationally persistent if they are national forces; keep a party’s alliance or command philosophy party-bound only if it is meant to deactivate on a change of government.
- Use actual transition receipts and incumbent conditions for army-led programmes. For civilian control, introduce a new constitutional/command receipt and require the actual military-to-civilian transition before the democratic branch counts as accessible. Standard army modifiers alone cannot prove civilian control.
- Continue to use existing doctrines/technology categories after checking the current tree rather than filling the new branch with generic combat buffs.

## 7. Civil nuclear safeguards and energy

The existing Cold War nuclear subsystem offers a particularly strong integration target:

- `mdcw_nuclear_safety_target` is a country-scoped numeric target (`common/modifier_definitions/COLDWAR_nuclear_power_modifier_definitions.txt:1–8`).
- `COLDWAR_nuc_player_programme` is limited to human-controlled countries with reactors (`common/scripted_triggers/COLDWAR_nuclear_power_triggers.txt:14–18`).
- `COLDWAR_nuc_update_safety` sets target 40, adds the modifier, applies the selected regime adjustment, clamps to 0–100, and moves safety by at most two points monthly (`common/scripted_effects/COLDWAR_nuclear_power_effects.txt:106–154`). The rigorous regime adds 15 safety target and upkeep +40% while output falls 3%; the minimal regime subtracts 20 safety and cuts upkeep 30% while output rises 3% (`:106–123`).
- Development and fuel/reprocessing project costs are already collected in the shared weekly budget (`common/scripted_effects/COLDWAR_nuclear_development_budget.txt:1–38`). The wider nuclear subsystem owns real projects, technology, reactor safety, fuel and accident consequences; nuclear flags or a focus name are not substitutes.

The existing KOR `civil_nuclear` node is not yet mechanically gated to that scope: its prose requirement says “native safeguards, technology and projects,” but the current exact native gate is only original tag KOR, the 1970 scenario, and independence (`COLDWAR_KOR_design.json`, node `COLDWAR_KOR_civil_nuclear`, gate/requirements near the corresponding node record). On expansion, change the specification so the exact start and completion conditions prove an eligible development level, required technology, safety/project availability, and no free reactor/uranium grant. Distinguish civilian power projects from enrichment/weapons projects; use the shared native weekly cost reader and current paid-project action. Do not grant state-history uranium output or built uranium mines.

## 8. Inter-Korean diplomacy and consent

KOR should integrate with the extant NKO-owned Korean channel/confederation flow rather than invent a unilateral KOR agreement API. Current NKO scripted effects include send/accept/refuse/expiry and recipient-pair lifecycle (`common/scripted_effects/COLDWAR_NKO_1970_foreign.txt:626–909`); the prior report traces existing NKO acceptance flags and required bilateral membership handling. In expansions, every contract must state initiator, recipient, payer, beneficiary, duration, expiry/termination, and acceptance receipt. KOR focus completion can unlock an offer but cannot stand in for recipient consent. Historical talks should have explicit initiative/offer/acceptance milestones; a focus should not jump from contact to reunification, annexation, or shared institutions.

## 9. The 206-node design: expansion-specific structural audit

### Access to democratic and institutional content

The design’s NDP, reform, USP and civic focuses are gated on actual party slot/leader states (see `COLDWAR_KOR_design.json` `gate_definitions` and node guards). The political entry route now provides civic legalization, revolutionary ratification, and an exceptional security caretaker, but those do not by themselves model the historical Park succession and military seizure that separates 1970 politics from Chun’s office. The national-tree skill’s historical review already flags the need to bind Fifth Republic/liberalization to the real 1979–80 transitions and the June 1987 settlement. Expansion should make this playable before increasing the size of downstream policy branches.

In particular, focus content such as independent unions and the legal civic cabinet cannot become available merely because slot 3 or 5 has popularity or is present in a coalition. The exact legal settlement and actual appointment/election should be checked in the KOR political system; otherwise the branch is unreachable or claims an institutional outcome without authorizing it.

### Requirements that are currently prose

The focus catalogue has a mixture of actual `native_gate_body`/`native_completion_guard` and plain-language `requirements`. The civil-nuclear mismatch above is confirmed. The next expansion review should classify every prose requirement as either (a) narrative/tooltip only, (b) covered by a predecessor whose receipt persists, or (c) a live exact trigger requirement. For (c), define it in both availability and completion guards. Examples include lawful union status, direct-election settlement, civilian control, signed contracts, state capacity, reactor safeguards, and project stage. A focus preview/tooltip must state meaningful prerequisites, and the guard must enforce them.

### Aggregate caps and distinct trade-offs

The current `rules.lifecycle` says latest earned level replaces the value in each owner-qualified policy slot. This solves duplicate replacement within one slot but has no global cap or interaction table for simultaneously active values across many slots (starting spirits, national policies, party programmes, defense policies, and signed contracts). Before adding up to the user’s 300-focus ceiling, produce a compatible-path stacking table for at least stability, political power, civilian-factory productivity, agriculture productivity, construction speed, debt/interest, labor/workforce, and military output/efficiency. Calculate the strongest compatible full route including start replacement and accepted contract effects. Use intentional domain caps or slot design after comparing actual KOR baseline and MD/Imperia formulas; do not add arbitrary clamps without that balance pass.

The old concept often expresses consequential institutional/civic themes via stable `stability_factor`, `political_power_factor`, research speed or civilian productivity. These can be valid secondary outcomes, but repeated generic percentages will flatten choices. The expanded tree should grant at least one system-specific change per important programme, then use modifiers as consequences. Examples: actual election rights/office change for democratization; enacted oversight/appointment rule for civilian command; legal status/union response for labor; actual school-budget and literacy flow for education; actual state projects for regional investment; reactor project/safety pathway for civil nuclear; consent-based terms for inter-Korean diplomacy.

### Durable national reforms versus party programmes

The current lifecycle model should be refined before adding reforms. Classify each reward as:

1. **National problem/reform state** — persists across routine party changes after enactment; is explicitly repealed, suspended, or amended by a later action. Court independence, legal publication rights, an enacted union law, election rules, and completed state projects normally belong here.
2. **Party/leader programme** — active only while the actual party/office holder governs. Industrial-credit strategy, governing-party negotiations, current labor bargain, or a president’s executive method may belong here.
3. **Temporary burden or timed commitment** — remains for a defined duration or until a project/contract ends.
4. **One-time outcome** — treasury, PP, a building, research grant, or transfer that must never replay during refresh or government return.

Do not store durable constitutional reforms in a party slot that disappears automatically when that party leaves office. Conversely, do not let a former government’s price/benefit programme remain active indefinitely if it is intended to be a live executive policy. The previous mechanics report already describes owner-qualified refresh; this expansion needs an explicit receipt/repeal model for institutional laws alongside it.

### Scale and focus-count budget

The current concept contains 206 nodes across 13 groups. The requested 300-node ceiling leaves room for up to 94 additional nodes, but the expansion should reserve a substantial part of that capacity for the actual transitions and durable institutions before appending parallel sub-branches. Prefer linked bundles: an entry outcome, two or more meaningful policy choices, and consequences/follow-up actions. Avoid one-focus treatment of each requested topic unless the focus participates in a coherent path. Use the tree preview and layout review for footprint and joins after the concept is approved.

## 10. Native versus new-provider checklist

| Requested outcome | Existing supported substrate | New KOR content/provider still needed |
|---|---|---|
| Democratic handover | `change_ruling_party_effect`, coalition arrays, elections allowed, real party popularity and `set_leader` | Dated transition decision/events and exact outcome receipts; KOR leader/party migration and refresh hook |
| Political performance | `stability_factor`, political power fields, popularity, election threshold | If a single legitimacy score is desired, its new variable, formula, UI, clamps and consumer |
| Independent court / press / civilian command | Existing named censorship-state triggers; general political system can gate lawful governance | Enacted law/oversight/civilian-command status and repeal/rollback behavior; no native single modifier found |
| Labor unions | `change_labour_unions_opinion` when `labour_unions` exists; labor-union dynamic modifier | KOR initialization/integration because history starts `edu_04`, not `labour_unions`; actual legalization/representation transition |
| Literacy/technical skills | `edu_01`–`edu_05`, literacy variable/effects/dynamic modifier | Korean focus/decision route, guarded status/cost preview, any chosen actual tech categories |
| Agriculture/civilian development | Agriculture and civilian-factory tax/GDP reader modifiers; real state-building API | Correct geography, effective 1970 capacity checks and explicit distribution/service model if claimed |
| Defense/professionalism | Native military modifiers, conscription/training/costs, doctrine/research APIs | Civilian command transition/receipt; Korean force-structure choices and appropriate ownership/cleanup |
| Civil nuclear | Reactor safety target/regime, project technologies, weekly project budget, nuclear safety/upkeep effects | KOR exact gate wiring, eligible funded project path, no-free-uranium compliance |
| North–South agreements | NKO-owned offer, recipient choice, acceptance and cleanup | Shared contract ledger/adapter and separately scoped terms for each pair/signatory |

## Source anchors

- Political change/coalition/election control: `common/scripted_effects/00_MD_politicsview_scripted_effects.txt:136–155, 1980–2076`.
- Repression eligibility, not a press-freedom effect: `common/scripted_triggers/01_political_reform_triggers.txt:3–63`.
- Labor opinion provider and `has_idea = labour_unions` prerequisite: `common/scripted_effects/00_internal_faction_effects.txt:1245–1266`; labor bounds in `common/modifier_definitions/internal_factions_modifier_definitions.txt:333–349`.
- KOR 1970 history: `history/countries/KOR - Korea.txt:5–56` has no education-budget or labour-union idea; `edu_04` at `:722–740` is in the later 2000.1.1 block. Verify any scenario-time education/faction setup before assigning a baseline. Education-budget steps: `common/scripted_effects/00_budget_effects.txt:374–467`.
- Literacy updates and education dynamic modifier: `common/scripted_effects/00_education_effects.txt:134–180`; `common/dynamic_modifiers/00_MD_dynamic_modifiers.txt:168–176`.
- Agriculture and civilian industry exact definitions/readers: `common/modifier_definitions/money_modifier_definitions.txt:353–386`; `common/scripted_effects/00_money_system.txt:412–420, 469, 5344, 6027, 6055`.
- Nuclear player/safety target: `common/modifier_definitions/COLDWAR_nuclear_power_modifier_definitions.txt:1–8`; `common/scripted_triggers/COLDWAR_nuclear_power_triggers.txt:14–18`; `common/scripted_effects/COLDWAR_nuclear_power_effects.txt:89–154`; `common/decisions/COLDWAR_nuclear_power_decisions.txt:4–85`.
- Funded nuclear special projects/week-price reader: `common/scripted_effects/COLDWAR_nuclear_development_budget.txt:1–38`; native weekly account is in `common/scripted_effects/00_money_system.txt:3665–3681`.
- KOR native design currently requiring a civil-nuclear guard correction: `docs/design/COLDWAR_KOR_1970/COLDWAR_KOR_design.json`, node `COLDWAR_KOR_civil_nuclear` (requirements versus `native_gate_body`).
- NKO recipient-consent flow: `common/scripted_effects/COLDWAR_NKO_1970_foreign.txt:626–909`; the earlier `mechanics_concept_review.md` and `mechanics_feasibility.md` document legacy acceptance and KOR integration boundaries.
- Current concept size and lifecycle rules: `docs/design/COLDWAR_KOR_1970/COLDWAR_KOR_design.json` (`nodes`, `rules`, `party_migration`). Historical transition and labor/party-system gaps: `docs/design/COLDWAR_KOR_1970/historical_concept_review.md` and `research_history.md`.

Static source inspection confirms the named effects and calculation paths above, not runtime integration, parser acceptance, save migration, or final balance. Those checks belong to a later approved implementation review.
