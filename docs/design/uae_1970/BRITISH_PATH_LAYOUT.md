# COLDWAR UAE: British protection and independence layout review

Reviewed 19 October 2026. Scope: the nine-focus British programme, preserved national-tree neighbours, six treaty-status preview states, paired UK/UAE national-spirit cards, current canonical/embedded data, and native art. All work remains in the approval concept; no loaded game files were changed.

**Verdict: no blocking layout or presentation defect remains.** The British programme occupies the previously empty left side of the opening tier and can be inspected alongside the existing federation programme. Negotiating status and actually becoming independent are visibly distinct.

## Snapshot and preservation

- Canonical `COLDWAR_UAE_1970_CONCEPT.json` final SHA-256: `adfed639db46226ba8ade823af9474fb31bce4ffaea48c1a68c4d78cf9686f3d`.
- 107 focuses, 40 decisions, 12 groups, 24 reciprocal exclusive pairs, 39 distinct native focus icon types.
- Complete grid bounds: x−6…37, y0…24. The additional width is on the left; the oil/development, society and defence tiers retain their coordinates.
- Independently recomputed the 14-field hashes for all 97 unchanged existing focuses against `BRITISH_PRESERVATION_BASELINE.json`: all match. The separately authorised change is `COLDWAR_UAE_sovereign_union`, now displayed as British Withdrawal and requiring actual independence. Its coordinates remain (5,5).
- The canonical model and embedded `PREVIEW.html` model agree, including nodes, groups and the bilateral treaty model.
- Final bounded refresh: the starting UAE treaty card now reuses the actual starting `COLDWAR_UAE_treaty_dependence` spirit ID instead of naming a duplicate idea. This metadata change preserves the reviewed focus nodes, groups, geometry, labels and art. The final file hash and canonical/embedded nodes/groups equality were rechecked; no layout rerun was needed.

## Native programme geometry

| Focus | Absolute position | Prerequisites / choice | Native sprite |
|---|---|---|---|
| The Protected Coast | (−3,0) | Entry | `align_to_britain` |
| Renew the Protection | (−5,1) | Protected Coast; exclusive with Petition for Freedom | `align_to_britain` |
| Petition for Freedom | (−1,1) | Protected Coast; exclusive with Renew the Protection | `treaty3` |
| Shared Administration | (−5,2) | Renewal OR petition; active compact and British status gate | `government_beu` |
| An Orderly Handover | (−1,2) | Renewal OR petition; actual independence gate | `accept_treaty` |
| British Training Teams | (−6,3) | Shared Administration; exclusive with commercial partnership | `military_mission` |
| Commercial Partnership | (−4,3) | Shared Administration; exclusive with training teams | `liberalization` |
| A Friendship Treaty | (−1,3) | Orderly Handover; independent treaty gate | `treaty2` |
| An Enduring Compact | (−5,4) | Training OR commercial partnership | `align_to_britain3` |

The new footprint is x−6…−1/y0…4. The nearest federation cards start at x3, leaving four grid units between the closest same-tier card centres. The British training/commercial pair uses the native two-unit rhythm; the initial policy pair has four-unit separation for its two continuations. Its capstone is centred between the training/commercial inputs.

The OR bridge below the first policy choice supports either subsequent diplomatic history: an initial petitioner can continue under an accepted protection compact, and an initially loyal country can later negotiate release. Static focus exclusions do not have to be undone to inspect or use the appropriate continuation. Availability/status gates carry that distinction; the drawing does not falsely promise that both sovereign states are active at once.

No long connector is drawn through the federation subtree. British Withdrawal in the existing national programme checks actual `is_subject = no` plus founding consent, rather than treating a petition, a future treaty date or loss of British-overlord status alone as independence.

## Visual closure

Opened `BRANCH_british.png` at native scale, the browser British view with federation neighbours, the refreshed full overview, and the paired signed-handover/continued-protection national-spirit screenshots.

- Every negative-x card and connector is inside the native proof-sheet bounds; the leftmost training card and rightmost handover/friendship cards are fully visible.
- British and federation group headings remain separate. No card, icon, title, exclusive mark or connection overlaps its neighbour.
- Independent full-concept route testing against actual icon-alpha rectangles plus native titlebar rectangles found zero unrelated visible-card intersections.
- The new English labels measure117–142 pixels with the actual `hoi_16mbs` glyph metrics. Commercial Partnership is the widest at142, within the147-pixel native field. No missing glyph or title clipping was observed.
- The native Union Jack/handshake sprites are appropriate to the British relationship; generic document, accepted-agreement, administration, training and commercial icons identify the functions. No laptop-based treaty art or unrelated country's flag was introduced.
- The full overview now shows all 12 groups, with the British opening clearly to the left of federation and the retained lower tiers. The addition does not force a change to the national tree's vertical extent.

The first-visit HTML state was initially still the federation root. This was corrected: the current viewer initializes `current='british'` and selects `COLDWAR_UAE_treaty_coast`, while the existing state-restoration mechanism can preserve a returning user's selection. This makes the new British opening the initial review camera. Native engine camera/shortcuts remain future implementation work.

## Treaty-status and national-spirit presentation

The viewer separates the governing-party choice from diplomatic status. Its six status views are British protection, a signed future handover, renewed protection, released independence, independent friendship, and another country's subject. This avoids making an outlook selector stand in for actual sovereignty.

The paired national-spirit screenshots show two aligned country cards with the same accepted agreement, status and date, followed by role-specific obligations. The signed handover shows 1 December 1971 in both cards and explicitly says the UAE remains a subject until that date. Continued protection instead shows a review date and says there is no fixed independence date; review expiry is not rendered as automatic release. The independent-state friendship is separately identified. Another overlord produces no stale British agreement cards.

At the inspected 1400-pixel view, headings, 80-pixel icons, date fields and obligations wrap without overlap. `BRITISH_BROWSER_VALIDATION.json` reports zero errors at 320/736/1024/1400 widths, all six status cases, matching UK/UAE dates, and actual-independence gating. The 320/1024 checks were exercised by the root agent's browser validation, not independently re-operated in this review. Responsive CSS uses a one-column card layout when two 300-pixel columns will not fit.

Run-together date/number prose noticed during the first screenshot pass was corrected in current canonical/embedded treaty text, including the protection-review example. These text-only changes preserve the reviewed card geometry.

## Limits and approval boundary

The preview demonstrates the proposed focus structure, named effects, conditions and bilateral national-spirit presentation. It does not execute diplomatic offers, advance the game date or prove native event delivery. Exact-party/status changes, accepted-date maturity, mirrored spirit replacement, one-time UK-scoped release, save recovery and leader continuity remain mechanics/implementation checks. Current focus availability in the browser is an explanatory approximation of the selected treaty state, not full world-state eligibility.

The prior whole-tree and oil layout reviews remain applicable to their preserved content. This report supersedes their whole-concept hash/counts and records the authorised federation-status presentation change. The user has requested visualization before implementation; the British branch and treaty spirits remain outside loaded focus/history/event/idea/localisation/GFX/on-action paths until approval.
