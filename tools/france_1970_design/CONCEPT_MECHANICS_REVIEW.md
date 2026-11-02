# IMPERIA COLD WAR

# France 1970 concept mechanics review

**Reviewed input:** `concept.json`, revision FRA2 concept 1, 134 focus nodes, 3 explicit decision definitions. SHA-256: `04a12f6f1d2a3f4e500e6f848cac5fb1eab3c083d664642a6e09a88cca3060c2`. Last modified 2026-10-28 20:27 local time. This is a source-level review of the current design data and Millennium Dawn source. No game launch, parser validation, or runtime test was performed. No builder or loaded mod file was changed for this review.

## Refresh findings

- Final bounded refresh: the titles shortened for interface fit preserve `full_title`; navigation metadata was added. No numerical effects changed since the prior review. The source data still has 134 nodes and 15 recipient offers.
- The Iran offer is now differentiated from Algeria's. France receives +6% energy gain with a -2% foreign influence modifier for 0.0035b/week; Algeria's France side is +4% energy gain at 0.004b/week. Iran's recipient receives +5% civilian factory productivity at 0.0015b/week, while Algeria's recipient gets +4% civilian productivity and +2% bureaucracy cost at 0.002b/week. Setup remains 0.20b for France and 0.10b for the recipient. Algeria retains its valuable technical institutes follow-up. The previous dominance issue is resolved.
- Senegal civil and defence offers now both branch directly from Diplomatic Review, with no unrelated energy treaty prerequisite. The EEC entry also branches from Diplomatic Review and retains `has_idea = EU_member`. Algerian Technical Institutes continues to require the Algeria Energy agreement focus and both countries' active agreement spirits.
- Party requirements are present on all nodes in all nine party groups: each node's `conditions` contains the group's exact native trigger with `= yes`. The generator helper also injects that condition (`build_design.py:28-34`). Party branches stay visible because gating is on focus requirements, not branch visibility. This is a source/data check, not an emitted-tree test.
- The shared defence Jaguar doctrine requires the actual active French Jaguar agreement spirit. The Soviet friendship focus requires the actual active Franco-Soviet science spirit. EU institution nodes use `has_idea = EU_member`; France receives this through the 1970 EC-6 startup when the EU system is enabled (`common/scripted_effects/99_eu_scripted_effects.txt:716-724`; `common/scripted_effects/COLDWAR_EC_1970_effects.txt:44-49`).
- The concept now has exactly three explicit decision definitions: Energy Contingency Planning, Fund the First Approved Reactor Project, and Community Enlargement and Institutional Negotiations. Recipient responses remain explicit decision unlocks on their originating proposal focus; the data does not rely on unbacked generalized menu claims.
- Starting stability is -0.08 total: Fifth Republic -0.02, Grenelle -0.04, Postcolonial Settlement -0.02. The eighth starting spirit, After the 1969 Devaluation, lasts 270 days and gives +3% factory output with -4% building construction speed. This temporary opening modifier expires and does not return.

## Current route ceilings

I enumerated mutually exclusive choices and prerequisite closure within each group, then summed each modifier's independently highest reachable value across institutions, shared economy, defence, diplomacy, and one party branch. This is a static concept ceiling: different maxima for a route can come from different policy choices and should not be read as one simultaneously attainable package. It excludes treaty spirits and is not a game simulation.

| Party route | Stability max | Social expense multiplier max | Bureaucracy expense multiplier max | Factory efficiency growth max | Political power factor max |
| --- | ---: | ---: | ---: | ---: | ---: |
| UDR | +0.30 | +0.29 | +0.21 | +0.32 | +0.18 |
| RI | +0.28 | +0.33 | +0.14 | +0.21 | +0.09 |
| Centre | +0.33 | +0.35 | +0.22 | +0.21 | +0.23 |
| Radical | +0.27 | +0.35 | +0.19 | +0.21 | +0.09 |
| PS | +0.32 | +0.37 | +0.31 | +0.25 | +0.22 |
| PCF | +0.36 | +0.35 | +0.28 | +0.26 | +0.24 |
| PSU | +0.32 | +0.36 | +0.24 | +0.29 | +0.09 |
| Ecology | +0.25 | +0.33 | +0.24 | +0.21 | +0.12 |
| National Right | +0.19 | +0.32 | +0.19 | +0.16 | +0.22 |

Positive `social_cost_multiplier_modifier` and `bureaucracy_cost_multiplier_modifier` values increase those expenses under MD's formula; they are costs, not bonuses. The revised UDR and PCF choice values reduce their independent stability ceilings, while PCF remains highest at +0.36. Review these upper bounds alongside native starting spirits and agreements before implementation. The calculations assume optional conditions can become true and do not model political timing or opposing starting effects.

## Effects, categories, and assets

The concept uses `training_time_army_factor` and the real research categories `CAT_armor`, `CAT_electronics`, `CAT_industry`, `CAT_nuclear_reactors`, and `CAT_aircraft`. These categories are registered and used by current MD technology data. The requested modifier palette is recorded in `verified_effects.json`, including separate reactor construction (`production_speed_nuclear_reactor_factor`) and reactor generation (`nuclear_energy_generation_modifier`) keys. The latter is applied by `common/scripted_effects/!_energy_effects.txt:474-499` and defined in `common/modifier_definitions/energy_modifier_definitions.txt:122-127`; the concept does not currently claim either as a focus reward.

`police_cost_multiplier_modifier` is now recorded in `verified_effects.json` with its bill multiplier semantics and evidence. It is valid in MD. Donor evidence is `common/modifier_definitions/money_modifier_definitions.txt:58`; the France ideas use it at `common/ideas/05_france.txt:1139` and `:2105`.

Current building placements use one extra shared slot per level in the same state: industrial complexes in 54 Hauts-de-France and 55 Normandie, infrastructure in 62 Rhone-Alpes, arms factory in 55 Normandie, dockyard in 64 Bretagne, and the decision-funded reactor in 59 Loire. These IDs and names match current country/state history. Runtime effects still need the same-transaction one-time guard and separate ownership, control, and capacity checks.

## Agreement costs and integration boundary

The 15 proposal records contain named partners, separate French and recipient spirits, complete prospective effects, acceptance fees, and weekly expenses on both sides. Focus nodes unlock recipient-owned response decisions and do not duplicate acceptance fees. Across one accepted option in each of eight families, maximum French recurring cost is 0.025b/week and maximum recipient recurring cost is 0.018b/week. Maximum French setup outlay is 1.15b across families; recipient outlay can reach 0.77b. Rhine's 0.25b for each signatory includes 0.10b setup plus a 0.15b project contribution.

`additional_expenses_rate` is a rebuilt native aggregate, not persistent storage. The France precedent stores `FRA_nepad_sponsor_weekly_cost` and adds it into the aggregate in `common/scripted_effects/00_money_system.txt:4431-4435`. A France-specific consumer plus acceptance, suspension, restoration, and removal integration is still needed. Treaty rules correctly specify suspension for mutual war, native embargo, and four mirrored Imperia sanction classes, with restoration that does not replay setup or finite assets. These are design requirements, not active France runtime behavior.

The final browser review was reported by the integrator as passing 134 focus clicks, 15 offer previews, 39 width-fit views, and 3 width checks with zero errors and titles at or below 147 pixels. I did not independently reproduce that UI review. Native game tooltip rendering and gameplay remain unverified.
