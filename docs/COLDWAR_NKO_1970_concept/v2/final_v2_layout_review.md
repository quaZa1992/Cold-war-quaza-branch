# DPRK 1970 concept v2 — final layout and localization review

## Scope and result

Reviewed the review-only v2 design (`COLDWAR_NKO_v2_design.json`, 189 focuses in 14 sections), the rendered `branch_foreign.png`, `branch_diplomacy.png`, and `branch_jongil.png`, and the preview’s connector/title implementation. No design, generator, localization, or game files were changed.

The three branches have sound card-level geometry. All relative anchors in the design resolve to their stated absolute coordinates. An independent check using the reference bounds of 165×128 px cards, 147×20 px name fields, and a 96×130 px grid found zero card overlaps, zero title-field overlaps, and zero unrelated-card intersections along prerequisite paths under the preview’s orthogonal router. The 33 mutual exclusions are reciprocal. The images show clear branch separation and no obvious connector-through-card collision. These are static checks of the supplied preview model, not a claim of in-engine routing.

Two titles exceed the installed game font’s native 147 px name field, and one foreign-diplomacy join currently has OR semantics that may understate the intended programme. Five foreign-programme descriptions are also repeated verbatim and should be made partner-specific before localization is finalized.

## Native title measurements

Measured every focus title using character advances from the installed base-game font `Hearts of Iron IV/gfx/fonts/hoi_16mbs.fnt`. All 189 titles have supported glyphs. Exactly two exceed the 147 px native focus-name field:

| Focus | Current title | Width | Suggested title | Width |
|---|---|---:|---|---:|
| `COLDWAR_NKO_technical_exchange` | Technical Exchange Council | 160 px | Technical Exchange | 114 px |
| `COLDWAR_NKO_jongil_authority` | The Successor’s Authority | 153 px | Succession Authority | 125 px |

The foreign branch image visibly truncates the first title to “Technical Exchange Co…”. The Jong Il title looks intact in the browser image because the preview title field is wider than the native field. Keep the full concept wording in any inspector subtitle if desired, but use the shortened strings for the in-game labels. The widest remaining title is `Community Associations` at exactly 147 px; it technically fits, with no spare width.

The preview stylesheet uses a 164 px-wide, 50 px-high title span with browser text and ellipsis (`preview_v2_template.html:33`), while the native target field is 147×20 px with `hoi_16mbs`. The preview is useful for layout and icon review but does not prove native title fit; the font measurements above are the relevant check.

## Localization corrections

The focus descriptions are generally concise English narrative and keep reward values and implementation details out of ordinary prose. I found no focus description mentioning flags, script variables, triggers, tooltips, or code-level country routing. Keep `requirements`, `eligibility_notes`, `succession_guard`, and other design metadata out of player-facing localization; they are specification/tooltip material, not focus descriptions.

Five focus descriptions repeat exactly:

| Focuses | Current repeated description | Recommendation |
|---|---|---|
| `COLDWAR_NKO_gdr_training`, `COLDWAR_NKO_bulgarian_agrobiology`, `COLDWAR_NKO_romanian_trade` | “Propose a further programme of specialist exchange and reliable deliveries under the existing agreement.” | Name the actual follow-up: machine-tool standards and plant training for the GDR; agronomy or field trials for Bulgaria; reciprocal industrial and agricultural schedules for Romania. |
| `COLDWAR_NKO_egyptian_missions`, `COLDWAR_NKO_japan_ports` | “Propose broader technical and commercial arrangements through the established bilateral channel.” | Describe Egyptian technical/maintenance missions separately from the limited fisheries and port-access negotiations with Japan. |

These descriptions are not implementation-heavy, but identical copy blurs the partner-specific stakes and gives each focus less identity than its title. Keep each to one short sentence and leave prices, requirements, and effects in the native tooltip.

## Prerequisites, choices, and routes

In the design representation, each prerequisite array is one OR group; separate arrays are ANDed. The preview displays this rule at `preview_v2_template.html:92` and draws every parent in the OR group at lines 112–115.

The Korean policy fork is correctly represented as a three-way choice: `COLDWAR_NKO_detente` at `(40,4)`, `COLDWAR_NKO_coercion` at `(44,4)`, and `COLDWAR_NKO_war_line` at `(48,4)` are pairwise mutually exclusive. Each is available from `COLDWAR_NKO_external_balance` at `(44,3)`. The row is well-spaced, and the preview draws exclusion links only between adjacent alternatives, avoiding a line through the middle card. The war route continues down the right side through `(48,9)` without colliding with the left détente route or the center pressure/export route. The merge at `COLDWAR_NKO_external_resilience` `(42,9)` is an OR between the civilian-export and military-mission alternatives; that is satisfiable and consistent with their mutual exclusion.

One semantic join needs an explicit decision: `COLDWAR_NKO_technical_exchange` at `(68,3)` has a single OR group containing `gdr_training`, `bulgarian_agrobiology`, and `romanian_trade`. It therefore unlocks after any one of the three follow-up programmes, even though its title and description read like a coordinating body for several partners. If the council is meant to consolidate all three programmes, encode three singleton prerequisite groups (AND). If one partner is intentionally sufficient, keep the OR group and narrow its title/description to a single-partner technical channel. Either choice leaves the present connector geometry intact.

`COLDWAR_NKO_external_balance` at `(44,3)` has a separate semantic concern: its one OR group accepts Soviet placements, Chinese border trade, or Chongryon commercial offices individually, while its title and description promise a diversified policy in which Moscow and Beijing remain mixable. If the intent is genuinely to keep both patron channels open, require `soviet_training` AND `border_trade` using separate singleton groups; leave the diaspora office as an optional parallel branch. If one channel is meant to suffice, rename it to a narrower title such as “Maintain Foreign Contacts” and describe the limited basis for the next policy fork. The current 3-way Korean strategy fork remains reachable under either interpretation.

Other visible OR joins are coherent with alternatives: `COLDWAR_NKO_recognition` accepts either confederation talks or armed bargaining; `COLDWAR_NKO_external_resilience` accepts either civilian or military exports; and `COLDWAR_NKO_jongil_settlement` accepts either side of the mutually exclusive party-centre/cabinet choice. Do not turn these into AND requirements: their alternatives are not simultaneously reachable by design.

The foreign section is geometrically clean: root `COLDWAR_NKO_foreign_missions` `(68,0)`, three partner starts at `(64,1)`, `(68,1)`, `(72,1)`, their parallel follow-ups at y=2, the technical join at `(68,3)`, and the Egypt/Japan pair through y=5. These rows leave clear gaps for the preview’s orthogonal paths. One structural point is intentionality rather than a collision: `foreign_missions` has no prerequisite from `COLDWAR_NKO_independent_diplomacy` or another existing diplomacy focus, so the whole 12-focus programme is a separate, immediately available root. Keep that if early, parallel diplomatic capacity is intended; otherwise add a real parent edge and review its cross-section route.

The Jong Il footprint is compact and clear: root `(64,17)`, pair `(62,18)` / `(66,18)`, and OR join `(64,19)`. The two policy cards are mutually exclusive and the join remains reachable through either. The title overrun noted above is the only concrete visual defect in this branch image.

## Renderer limits and checked artifacts

Reviewed images: `branch_foreign.png`, `branch_diplomacy.png`, and `branch_jongil.png`. The independent geometry check confirmed anchor/delta consistency, no focus-card or name-field overlaps, reciprocal mutexes, and no unrelated-card intersections in the supplied preview router. The design’s structural validation also reports 189 nodes, 212 prerequisite edges, 33 exclusions, and no structural errors.

The preview is generated for review and is not installed. Its connector drawing is an orthogonal approximation in `preview_v2_template.html:112–115`; it is not an HOI4 runtime render. The supplied branch images use browser typography and wider title fields than the game, so the native font check was performed separately. No claim is made here about full-tree camera behavior, unprovided variants, live GUI rendering, or in-game connector routing.

## Corrected current snapshot — 23 October 2026

Rechecked the regenerated 189-focus design and the refreshed foreign and Jong Il branch images. All 189 titles have supported glyphs and now fit the 147 px native field; the widest is `Community Associations` at exactly 147 px. `Technical Exchange` and `Succession Authority` render in the updated branch images without clipping. There are no exact duplicate focus descriptions in the current data.

The two joins called out above now match their stated intent: `External Channels` describes one-channel cooperation and intentionally accepts any one of its three partner routes; `Technical Exchange` intentionally accepts any one partner route and now requires an active GDR, Bulgarian, or Romanian agreement. The OR semantics therefore no longer contradict the focus wording. Relative anchors still resolve, and the current design retains zero card overlaps, zero title-field overlaps, and reciprocal exclusions. The reviewed layouts did not change, so the earlier connector-route check remains applicable.

No design-level blocker remains in the checked titles, repeated copy, branch geometry, or prerequisite semantics. Engine-only behavior remains unverified because this preview is review-only and is not installed or tested in HOI4. No DOM automation package was available in the local Node environment, so browser interaction was not independently simulated.
