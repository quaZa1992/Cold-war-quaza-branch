---
name: mdcw-tree-layout
description: Position, visualize, compact, and audit HOI4 Millennium Dawn Cold War national focus trees in native MD style, including relative anchors, connectors, branch footprints, icons, labels, and camera navigation. Use for national-focus layout work, not research-tree GUI positioning.
metadata:
  project: IMPERIA COLD WAR
---

# IMPERIA COLD WAR: Native national-focus layout

Make the whole tree read like current MD Generic/Russia focus trees, with coherent sections and readable alternatives. Do not impose research-GUI layout conventions on national focuses. Read [layout-method.md](references/layout-method.md) for geometry, visual QA and local references.

Use the owner-selected Soviet 1970 implementation as a case study for clustered sections, leader-programme fans, navigation and shared/joint-focus space. Its wide canvas is not a required size. Enes explicitly prioritizes quality over quantity: a compact small-country tree is acceptable. Match native spacing and readable choices without adding focus nodes merely to imitate a large country's size or symmetry. The reference distinguishes old graph images from current installed positions.

## Preserve scope

Spacing/aesthetic work preserves rewards, costs, IDs, logical prerequisite groups, exclusions, availability, AI and localization meaning. Compare their semantic representation before/after. Disclose logical corrections separately and respect existing authorization; do not change gameplay just to simplify lines.

An explicitly supplied fixture or review copy is the target instead of the live mod. With partial inputs, resolve and report only what can be established; list missing neighbours, textures, labels, offsets or renderer bounds as unverified. Do not claim full-tree or rendered QA from a partial coordinate review.

When approval is reserved, keep the proposed layout outside loaded files until accepted. Implement an already approved layout without another confirmation round.

Party branches remain visible and inspectable outside government unless the user explicitly requests hiding. Use exact-party availability/completion and modifier-activation checks; do not add party-dependent `allow_branch`. Reserve the complete footprint of inactive branches and include them in the starting-government overview. A preview that shows all parties cannot validate an installed tree that hides them. Reuse the actual registered party names and native MD requirement display, and check live labels for unsupported glyphs; do not combine current and future party names with arrows.

## Measure, resolve, compose

1. Inspect main MD `00_generic.txt`, `05_russia.txt`, the target country and focus GUI/GFX. Sample spines, choices, joins, section gaps and typography. Record measured spacing instead of inventing universal pixel sizes.
2. Read the whole affected tree, shared focuses, relative anchors, conditional offsets and existing neighbours. Locate its canonical generator. An isolated image of additions is insufficient.
3. Recursively resolve emitted `x`/`y` and `relative_position_id` into absolute grid coordinates. Report missing/cyclic anchors. Also verify each anchor is declared earlier than every focus using it: HOI4 rejected a forward relative anchor even though recursive coordinate resolution produced the intended position. Evaluate conditional offsets and loaded content as separate layout states.
4. Arrange coherent sections around stable anchors. Keep straight spines, deliberate choice rows and merges between their inputs. Reserve the entire subtree footprint. Avoid dead zones and arbitrary stretching while retaining clear section separation.
5. Preserve prerequisite groups: multiple blocks are AND; multiple `focus` fields within one block are OR. Connectors do not replace political gates. Mutually exclusive cards can remain visible together and must not overlap.
6. Place initial camera, shortcuts and continuous focuses intentionally. Use structural anchors without adding ceremony focuses merely for positioning.

## Preview the actual output

Use one coordinate/condition model for generation and preview, then independently parse emitted code to compare it. Check current file hashes/positions before reusing an old 'new layout' image. Show full-tree overview and normal-scale branch views with neighbours, actual icons, English titles and connections. A hand-arranged graph with different coordinates is not a substitute. A graph-only overview proves relationships, not card/icon/title rendering.

Show the starting government and relevant party/leader/layout variants. List unverified conditional states. Match native typography, background, titlebars and unavailable/available/current/completed treatment. Label preview approximations. Do not change global fonts, icon sizes or GUI to hide crowding.

Visually inspect actual renders, including agent-produced images. Check card/icon/title overlap, line-through-card collisions, crossings, clipping, excessive whitespace, awkward diagonals and unclear joins. Node-center distances alone are insufficient. Reuse appropriate MD/Cold War art. Inspect the resolved texture class as well as its name: a national-spirit proof must show actual idea artwork, not a focus medallion hidden behind an idea-named sprite alias.

For interactive concepts, clickable inspectors, native art closure or refreshed installed-output evidence, read [interactive-and-installed-preview.md](references/interactive-and-installed-preview.md). Enes expects every focus, including locked paths, to be inspectable by click in a usable wide viewport. Recipient-approved focuses must expose both countries' complete numeric "If they accept" outcomes directly in the focus inspector regardless of acceptance or current eligibility.

## Verify and hand off

- Compare design, emitted files and preview IDs, resolved coordinates and prerequisite groups.
- Run applicable geometry/structural tools after checking their write behaviour. Country-specific thresholds are not universal engine limits.
- For substantial work, have a separate reviewer inspect overview and normal-scale views plus coordinates. Request concrete issue IDs/positions, not a generic approval.
- Where available, inspect the tree in HOI4: zoom, scroll, hover, shortcuts and conditional branches. Simulated connectors do not prove engine routing.
- Report what moved, gameplay preserved, layout states and visual findings checked, and any engine-only gaps. Preserve the user's approval boundary and existing systems.
