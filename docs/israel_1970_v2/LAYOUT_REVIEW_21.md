# IMPERIA COLD WAR: Israel Version 2.1 expanded layout review

Scope: the proposed 192-focus, nineteen-programme design, including eleven party programmes. Alignment and Gahal contain 23 focuses each; Mafdal contains nineteen. The preview remains explicitly labelled as a proposal. No loaded focus, GUI, script, localisation or history file was changed by this layout task.

## Verified sources

Revision: `2.1-expanded-20261028`. The data, fragment and standalone preview hashes were compared before and after the complete browser run. No source changed during verification. The inline fragment is 589,938 bytes.

| Input | SHA256 |
|---|---|
| `tools/israel_v2/design.json` | `de44ef3a56c962ee5def4b4b8c425a481e3a034a9fa05e72d276f7e1d26ce7ef` |
| `tools/israel_v2/fragment.html` | `ffcbf27487ada079c98b66eb13d921e28f480d44f6af3cf778f3659b5b2f04cd` |
| Standalone `preview.html` | `6874e77d84645e3ef2c4a2527aea620c41695a4684f67a39f53cb876269e3c7c` |
| Inline `israel-1970-v2.html` | `2c56e11b888623b372b818d591f90532731f4ddce200948766eb8828c3bdfd6e` |

The supplied MD 2.0.3 national-focus GUI was inspected directly: native container 165 x 128 pixels, grid 96 x 130 pixels, title field 147 x 20 pixels, font `hoi_16mbs`. The external proposal uses native artwork, 147 x 142 focus bounds, 82 x 178 preview units and Georgia as a font approximation. It is not an exact engine render.

## Downward continuation

The major programmes now visibly continue through many rows. The opening view retains a readable minimum 74% scale. `Continue downward` moves to the next off-screen row and shows the actual count of focuses below. The final movement is limited by the programme's bottom so several concluding rows remain visible. `Back to top` restores the opening view. Deep programmes call the toolbar action `Branch start` rather than promising a miniature whole-branch fit.

All focus cards remain in the same canvas. Overview titles have clear space above their clusters, and individual focus titles reappear if the overview is manually enlarged. Fresh initial selection is the substantive Gahal arbitration policy.

The first expanded run exposed an unnecessary six-pixel movement in the short reserve programme: an eight-pixel safety margin requested continuation although the card was visible. Aligning the test against the actual card/footer boundary with a two-pixel margin removed that false continuation. The complete suite was rerun and passed.

## Complete browser verification

`node tools/israel_v2/verify_preview.cjs` passed:

- 57 responsive views: all nineteen programmes at widths 320, 736 and 1024 pixels.
- 192 actual pointer inspections. Each inspector displayed the correct title and retained every supplied effect row.
- All 192 cards and 211 prerequisite edges retained in every branch view. No party-dependent hiding.
- Every native focus image loaded. No card collisions, connector/card intersections, off-row exclusive pairs or title overflows.
- Seven clear row-gap or vertical-gutter detours avoid unrelated cards without changing prerequisites.
- Actual pointer dragging moved the map independently of focus selection. Actual zoom buttons increased and restored scale.
- Every programme was followed to a fully visible final row. Return to its opening position passed whenever continuation was required.
- No overlapping or clipped overview labels. Starting conditions and the complete programme index remained present.

Measured downward navigation for the major parties:

| Width | Alignment | Gahal | Mafdal |
|---|---|---|---|
| 320 px | 4 jumps | 3 jumps | 3 jumps |
| 736 px | 2 jumps | 2 jumps | 2 jumps |
| 1024 px | 2 jumps | 2 jumps | 2 jumps |

Every entry above ended with the final row visible and a successful return to the top. Full results and hashes are in `browser_validation.json`. The older `display_refresh.json` is a bounded intermediate check and must not replace this full result.

## Visual review and limitations

The reviewer opened the fresh Gahal starting view, the deep Alignment, Gahal and Mafdal views, and the complete overview. The Gahal opening shows output and repair gains with treasury and stability costs. The lower programmes contain several visible rows and concrete projects or competing fiscal outcomes. Their complete right-hand continuation remains visible in the deep views.

Reviewed images: `preview-gahal.png`, `preview-alignment-deep.png`, `preview-gahal-deep.png`, `preview-mafdal-deep.png` and `preview-overview.png`. These are browser-rendered design previews, not HOI4 screenshots.

This establishes preview geometry, navigation, readable labels and supplied-effect visibility. It does not execute rewards, validate native modifier scopes, repair the existing game crash or establish multiplayer, save/reload or rehost stability.

Provenance: renderer, browser checks and this review were authored for IMPERIA COLD WAR with Codex. Existing native images were reused from project/MD/Imperia assets. Individual original authors or separate permissions remain unknown where inherited records do not identify them. Existing credits and licences continue to apply; see the root `IMPERIA_COLD_WAR_NOTICE.md` and current design provenance. No raster artwork was generated or retouched by this task.
