# Independent Vietnam layout and MD registration review

Reviewed 18 October 2026. Result: **pass for the installed-file layout, graph, approved reward payload, and art-registration checks described below; no actionable findings in this scope.** No game launch or in-engine behavior is claimed. This reviewer did not import or execute the compiler and did not edit any loaded game file. Only this report, its JSON evidence, and external static preview artifacts were written.

## Source identity

`approved_design.json` retains the approved source SHA-256 `a75e577703dbfa708f5e7493539f46e5280628d1a1e940b3204a38d46082d3d2`, matching `manifest.json` and the approved external concept. All 239 approved focuses are present exactly once in `common/national_focus/COLDWAR_VIE_1970_focus.txt`.

The independent token parser and geometry resolver were written separately from `script_ast.py` and the compiler. Full per-focus, sprite, DDS and source-hash evidence is in [LAYOUT_REVIEW.json](LAYOUT_REVIEW.json). No audited focus/effect/GFX source changed while this pass was running.

## Exact graph, geometry and effects comparison

All 239 loaded focus IDs, emitted offsets, relative anchors, recursively resolved absolute positions, durations, prerequisite groups, reciprocal exclusions, English titles and filters match the approved design. There are no missing or cyclic anchors, graph cycles, asymmetric exclusions, or structurally unreachable focuses. Compatible-history enumeration preserves separate prerequisite blocks as AND and members within a block as OR; its largest node has eight valid alternative exclusive histories, with no enumeration cap.

Every loaded completion call matches the approved call, and each of the 239 authored effect helpers contains the exact approved raw reward payload. This verifies preservation of promised effects and registration, rather than proving every engine/API consumer or campaign outcome. The separate mechanics review owns runtime transactions and broader numerical balance.

Exact approved governing-party, leader and additional context conditions remain present after expanding the local `COLDWAR_VIE_is_1970` alias. The implementation intentionally strengthens execution protection:

- The common scenario alias additionally requires that VIE exists.
- Every prerequisite group also has a matching OR group of implemented-parent `*_reward_applied` flags, so an unpaid completed badge cannot substitute for an implemented policy.
- All 60 funded focuses use the exact required treasury amount; application helpers recheck the same live availability before applying the reward.
- All 16 building projects preserve their approved queued building, state, amount and cost. Capacity checks derive shared-slot behavior from the actual building definition. `include_locked = no` is retained for shared-slot industry, offices, agriculture and dockyards; it is omitted for non-shared fossil plants, infrastructure and anti-air. State ownership/control remains checked.

These are explicit implementation guards, not silent coordinate, reward, prerequisite or policy-choice changes. Their actual engine behavior still needs runtime testing.

The focus header retains the approved Le Duan initial camera target, all 15 valid shortcut targets with scroll factor 0.80, and continuous-focus position (5400,1700). All political programmes retain fixed simultaneous footprints; availability changes do not rely on unverified dynamic hiding.

## Native MD presentation and art closure

The installed tree uses native local relative anchors, short spines, compact/broad pairs and OR joins at the approved positions. Costs 3/5/7 preserve the approved 21/35/49-day durations and follow the measured Russia reference vocabulary. Filters, standard completion logging and helper calls follow native MD structure. The retained native GUI spacing is 96×130, the focus container 165×128 and the title field 147×20; no global GUI/font/titlebar modification was introduced. Git status for `nationalfocusview.gui`, `nationalfocusview.gfx` and `00_titlebar_styles.txt` is clean.

All 554 new sprite definitions are unique across the live interface registry:

- 239 focus sprites and their 239 native two-pass shine companions;
- 72 native `GFX_idea_<picture>` aliases covering starting-spirit stages, decision ideas and crisis ideas;
- four decision/category sprites, with both new categories resolving their registered icons.

All 15 dynamic programme icons also resolve. Every focus texture is pixel-for-pixel identical, including alpha, to its approved source. The three approved TGA sources remain direct references; 22 PNG sources received lossless DDS copies. Every copied DDS has the correct `DDS ` magic, 124-byte header, 32-byte pixel-format header, 32-bit RGBA data, expected dimensions and exact decoded pixel identity. No source art was resized or redrawn.

Each shine points to its matching approved texture and mask, uses the native additive ±90° scrolling pair at 0.75 seconds, and disables legacy lazy loading. The overlay texture resolves. The native logical `gfx/FX/buttonstate.lua` effect reference is the same one used in supplied MD `goals_shine.gfx`; the corresponding base-game shader `gfx/FX/buttonstate.shader` is present. Treating the native logical alias as a missing asset solely because no literal `.lua` file exists would also flag the supplied MD source. Actual alias/shader execution remains an engine check.

Idea picture aliases and direct full category sprite names match supplied MD conventions. Category precedent includes `00_corruption_category.txt`; foreign-policy filter precedent includes the supplied MD shared Korea and China/North Korea trees. Default titlebar styles remain inherited native unavailable/available/current/completed states.

## Actual installed-output visualization

After comparing installed source, an external preview was reconstructed from the parsed installed positions and resolved live texture registrations. It was not merely a rerender of proposed sprite paths.

The full installed tree and January 1970 state are 7736×3230. All 239 labels fit the native-width bitmap-font measurement. There are zero missing icons, icon/titlebar overlaps, or simulated connector intersections with unrelated cards. The complete overview and normal-scale industry sheet were visually inspected; the latter confirms separation of compact pairs, clear OR joins, legible labels and the approved queued-project reward wording. Le Duan and industry sheets were also generated from the installed output.

External artifacts:

- [Full installed tree](C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f32-41dc-74b3-baa1-8f6916e026ed/coldwar-vietnam-installed-native.png)
- [January 1970 state](C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f32-41dc-74b3-baa1-8f6916e026ed/coldwar-vietnam-installed-1970.png)
- [Installed industry detail](C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f32-41dc-74b3-baa1-8f6916e026ed/coldwar-vietnam-installed-industry.png)

The previews use native source icons/titlebars and installed bitmap label glyphs; external routing, background sampling, state shading, placement and annotations remain approximations. They do not establish real engine routing, hover/tooltips or shaders.

## Integration and remaining runtime limits

The direct VIE history load now selects `COLDWAR_VIE_1970_focus`; the central fallback dispatcher now exempts 1970 VIE, preventing old fallback calls from replacing the authored tree. Startup, daily and government/party observers are registered. The earlier read-only engine-options report documents the available game executable and baseline logs; no game was launched during this audit.

A real fresh-1970 engine session must still verify initial spirits/tree, every hover, party/leader departure and return, pending reward funding and recovery, construction queue results, recipient refusal/acceptance, exclusive decisions, succession and save/reload without repeated rewards. Static parsing and a clean external layout cannot replace those tests.
## Final bounded freshness snapshot

Snapshot: 18 October 2026 16:37:50 CEST (14:37:50 UTC). The compiler had completed final stable regeneration before this check.

A bounded preservation pass reconfirmed all 239 approved focus offsets/anchors, grouped prerequisites, exclusions, durations, displayed titles, completion calls and approved raw reward payloads. Drift findings: 0. All 239 focus English narrative descriptions are now present from the authored flavour source. The clearer immutable-input headers and politics metadata change source bytes without changing the approved tree. The additional exact VIE tag condition on foreign transaction availability belongs to the transaction review; it does not alter the focus geometry or reward payload.

Current focus, effect, GFX, compiler, flavour, manifest and English-localisation SHA-256 values are recorded in the JSON source_hashes field. The approved design hash remains unchanged. Sources remained byte-stable across this bounded check. The existing installed-output images remain representative because geometry, titles, reward payloads and approved artwork did not drift; no unnecessary rerender or broad audit was repeated.

Six genuine mojibake sequences in this report were normalized: four multiplication signs, the plus/minus sign and the degree sign. The corrected UTF-8 report has zero detected replacement/known mojibake sequences. Earlier static layout/art results retain their original scope; this refresh does not add any in-engine execution, tooltip, shader, save/reload or multiplayer test claim.
