IMPERIA COLD WAR

# France 1970 starting-spirit audit

## Scope and evidence

Read-only review of the approved `tools/france_1970_runtime/runtime_design.json`, SHA-256 `D7298667CAF36D1E0E3A1493FEFE77AC270C85C39DA8FF61E489AFAE94B451C7`. It contains eight starting spirits and eleven focus rewards that remove a spirit. Current focus costs are in weeks of 7 days; setup fees are shares of France's GDP. Prerequisite alternatives are OR choices within a group.

The current Jan 1970 baseline spirits are mixed in several cases. “The Fifth Republic,” “The Unfinished Settlement of Grenelle,” “Uneven Modernisation,” “A Narrow Route to Expertise,” “The Price of Independence,” “The Postcolonial Settlement,” and “After the 1969 Devaluation” each carry at least one useful effect alongside a cost. Treating all eight as simple debuffs would misstate the design.

## Spirit and removal map

| Starting spirit | Current effects | Current removal route and actual net outcome |
|---|---|---|
| The Fifth Republic | Political power +10%; bureaucracy cost +5%; stability -2%. | `public_service` (5 weeks, 0.08% GDP), then `executive` or `parliament` (7 weeks). Executive ends at PP +12%, bureaucracy +3%, stability -2%: relative to start, PP +2 points and bureaucracy cost -2, with stability unchanged. Parliamentary ends at stability +5%, PP -5%, bureaucracy -3%: relative to start, stability +7, PP -15, bureaucracy cost -8. These are different institutional bargains, not a pure debuff cleanup. |
| The Unfinished Settlement of Grenelle | Stability -4%; factory efficiency growth -5%; social cost +5%. | `public_service` → either `executive` or `parliament` → `contract` or `statute`: 19 weeks and 0.18% GDP including the initial service programme. Contract ends stability at 0%, efficiency growth +3%, social cost +8%. Statute ends stability at 0%, efficiency growth +6%, social cost 0% and police cost +4%. Both sides retain a distinct labour or industry faction trade-off. |
| Uneven Modernisation | Industrial-complex construction speed +5%; infrastructure construction speed -8%. | Sixth Plan (5 weeks, 0.08%) → Regional Links (7 weeks, 0.30%) → Industrial Champions or Regional Industry (7 weeks, 0.60%) → Industrial Balance (5 weeks): 24 weeks and 0.98% GDP. Removal also removes the +5% industrial-complex construction bonus; infrastructure construction changes from -8% to +3%. |
| Oil-Intensive Growth | Civilian energy use +8%. | High-Speed Rail or Regional Motorways (7 weeks, 0.60%) → Energy Choices (5 weeks, 0.05%) → Nuclear Expansion (7 weeks, 0.75%) or Diversified Energy (7 weeks, 0.60%) → Cut Oil Dependence (5 weeks). Before the final removal the branch has spent 19 weeks and 1.40% or 1.25% GDP, excluding the preceding transport-choice focus. The transport and energy choices also change energy use or generation, so the final effective level depends on the selected route. |
| A Narrow Route to Expertise | Research speed +3%; education cost +10%; factory efficiency growth -3%. | Sixth Plan (5 weeks, 0.08%) → Technical Colleges (7 weeks, 0.25%) or Mass Universities (7 weeks, 0.40%): 12 weeks and 0.33% or 0.48% GDP. Colleges end at efficiency growth +6%, education cost +5%, and remove the permanent +3% research speed in exchange for finite industry/electronics research bonuses. Universities end at research speed +4%, education cost +12%, remove the efficiency-growth penalty, and grant finite electronics/nuclear-research bonuses. Neither is an unqualified improvement. |
| The Price of Independence | War support +5%; equipment cost +5%. | Defence Priorities (5 weeks, 0.05% GDP and army XP) → Nuclear Deterrent or Balanced Forces (7 weeks). Nuclear Deterrent ends at war support +6%, equipment cost +8%, plus finite nuclear research; relative to start, war support improves by 1 point while equipment cost worsens by 3. Balanced Forces ends at army organisation +5%, equipment cost +3%, war support -2%; relative to start, equipment cost improves by 2 points and war support falls by 7. Both options preserve real trade-offs. |
| The Postcolonial Settlement | Stability -2%; bureaucracy cost +5%. | The path is not a quick side route: the same `public_service` and labour-settlement choice must be followed by Housing and Rights (7 weeks, 0.30% GDP, infrastructure in state 56), then Historical Recognition or Republican Amnesty (7 weeks), then Civic Settlement (5 weeks). Total: 38 weeks and 0.48% GDP. Recognition costs 50 PP and adds stability/social-cost effects; Amnesty grants 60 PP and war support but reduces stability. Civic Settlement removes the spirit and adds bureaucracy cost -2%. |
| After the 1969 Devaluation | Factory capacity +3%; general building construction speed -4%. | The spirit expires after 270 days and is not re-applied. It is deliberately mixed and historically timed; no removal focus is needed. Do not include it in a blanket “make debuffs harder to remove” pass. |

## Balance recommendation

The only removal that can happen after a single 7-week focus is the Fifth Republic reform choice, following the 5-week `public_service` focus. Its current terminal focus lasts 49 days; the full route from the start is 84 days and has a 0.08% GDP fee. If the intended role is a slower constitutional adjustment, make the first choice partial: add a distinct intermediate reform idea while preserving `COLDWAR_FRA2_presidency`. A later, meaningful accountability or parliamentary-capacity follow-through can then replace the starting spirit. Keep both executive and parliamentary routes distinct, disclose their final modifier totals, and ensure the intermediate idea is removed in the final transaction so modifiers do not stack twice. Do not use arbitrary calendar gating.

Do not broadly add time or fees to the Grenelle, regional, energy, education, or defence reliefs. Their existing routes already require funded programmes and have substantial continuing trade-offs. The postcolonial path already combines housing investment, a political choice and follow-through. The 270-day franc spirit is already temporary.

The history supports treating presidential authority and parliamentary checks as genuine institutional alternatives. The 1962 constitutional referendum established direct election of the president and was opposed by a majority of parliamentarians; see [Vie publique's account of the 1962 constitutional revision](https://www.vie-publique.fr/fiches/38016-la-revision-constitutionnelle-et-le-referendum-de-1962). Post-Grenelle interprofessional agreements on employment security and training followed in 1969 and 1970; see the [National Assembly's report on the employment-security and vocational-training agreements](https://www.assemblee-nationale.fr/14/rapports/r0847-tI.asp). These are historical precedents for gradual institutional follow-through, not evidence that the proposed focus values are historical measurements.

## Tooltip finding

The native “Modifies Republic and Society” heading is a valid heading. The screenshot's confusing appearance comes from previewing the starting spirit's removal and the replacement modifier together. That is not, by itself, a malformed removal effect. The real balance decision is whether the removal happens too early. A clearer tooltip should reserve that heading for the actual dynamic modifier deltas and show spirit removals, named spirits, assets and costs as their own concrete native effects.

## Source record

- `tools/france_1970_runtime/runtime_design.json`: approved 1970 design and all listed starting spirit, prerequisite, reward and GDP fee values; SHA-256 recorded above.
- `common/ideas/COLDWAR_FRA2_1970_ideas.txt`: compiled runtime spirit/modifier definitions. This audit does not claim a new native engine test.
- Historical sources linked above support the institutional precedents only. Numeric modifier values and route lengths are design data, not historical estimates.
