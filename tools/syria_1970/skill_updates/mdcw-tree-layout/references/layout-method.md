# Native geometry and aesthetic review

## Sources and reference profile

Use the recipient's actual target checkout (TARGET_ROOT) and main MD reference (MD_ROOT). The following original-machine paths are examples, not required dependencies. If they do not exist, use the paths given in the current task or resolve the relevant workspace; do not assume another user's installation is available. A supplied fixture/review copy remains the audit boundary.

Target: `<TARGET_ROOT>`.
Main MD: `<MD_ROOT>`.
Verify both; rediscover moved files with `rg --files`. Generic is currently `common/national_focus/00_generic.txt`, Russia `05_russia.txt`. Record the source/version of your reference profile.

Sample coherent spines, paired/multi-way alternatives, joins, long titles and section boundaries. Record minimum/typical offsets and subtree extents rather than assuming one pair defines the entire style. A large country may remain wide; compact means purposeful spacing, not a fixed canvas for every country.

## Coordinate model

```text
resolve(f):
  no relative_position_id => p = (f.x, f.y)
  otherwise              => p = resolve(anchor) + (f.x, f.y)
  apply only offsets active in this layout state
```

Detect missing anchors and recursive cycles first. Anchors need not be prerequisites. If design anchor is `(10,2)` and child `(12,5)`, emit child offsets `(2,3)` with its anchor ID, not `(12,5)` again. Stable section roots reduce drift when moving a block.

Grid units are not pixels. Derive any preview conversion and label/card bounds from the target UI/reference and record approximations. Never reuse a research-tree conversion for focus geometry.

## Logic and drawing

```text
prerequisite = { focus = A focus = B }
prerequisite = { focus = C }
```

Means `(A OR B) AND C`. Retain grouped data in preview and emitter. Reachability requires a satisfiable history: an AND-join requiring mutually exclusive parents is broken even when each parent is individually reachable.

`available` adds eligibility without drawing a connector. It is not a decision's `visible` field. Verify actual MD/engine focus patterns for conditional loading/hiding rather than copying decision syntax.

Some project designs put cross-section gates in `available` to avoid long lines; others deliberately draw them. Do not universally convert between them. Preserve approved semantics and readable eligibility. Reciprocal `mutually_exclusive` links represent real choice; they do not hide losing cards or permit overlapping positions.

## Preview data

Maintain a review manifest with ID/group, absolute coordinate, emitted offset/anchor, prerequisite groups, exclusions/eligibility, layout conditions, actual sprite and English title, card/icon/title bounds, camera/shortcuts/continuous/shared content, and linked conditions/effects/costs. Record source identifiers/hashes and rendering approximations.

Normal-scale views matter as much as overview. Use genuine focus icons/titlebars rather than large replacement rectangles. If exact fonts cannot be used externally, state the approximation; never alter live fonts to match the preview. Evaluate start government plus relevant party/leader branches, shared content and conditional offsets. Test all content that can be visible simultaneously.

## Investigate reportedly missing focuses

Compare the affected screenshot section with the approved design and emitted IDs, resolved coordinates, prerequisite groups, visibility and actual rewards. A total focus count cannot establish that a particular branch is complete. Small organizing sections may intentionally unlock decisions rather than grant passive modifiers; expose those real unlocks instead of adding filler focuses or invented buffs. Preserve approved gaps and grouping unless a layout change is authorized.

Measure the active `interface/nationalfocusview.gui` as well as the art. In the Syrian repair reference, native MD used a 96 by 130 grid, a 165 by 128 item container and a 147 by 20 name field with `hoi_16mbs`; the preview used 165 by 112 visible-art bounds. Those measurements describe that installation, not a universal engine constant. Label connector and visible-bounds approximations; a browser preview does not prove millimetre-identical engine rendering.

## Geometry and visual review

1. Compare intended IDs/anchors and generated positions with preview data.
2. Check complete cards, protruding icons, titles and state frames, including across adjacent rows. Same-row center separation is insufficient.
3. Simulate native-style connector routing; flag unrelated card intersections and needless long joins/crossings. Routing remains approximate until engine-checked.
4. Keep sensible forks and merges. Do not accept backward or near-horizontal diagonals merely because they connect.
5. Check entire subtree bounding boxes; root spacing alone does not protect expanding branches.
6. Compare density and whitespace with the measured reference without enforcing a universal density quota.
7. Inspect initial viewport, shortcuts, extremes, bottom edge, shared content and continuous focuses for clipping and unreasonable opening scroll distances.
8. Inspect textures at intended size in relevant states. Right filenames do not prove appropriate content/transparency.

Report focus IDs, coordinates and images for real issues. Separate functional collision, readability and aesthetic preference. A graph image cannot prove exact engine geometry.

## Existing tools to adapt

- `tools/israel_1970/validate_layout.py`: independently resolves emitted anchors, compares code/design coordinates and grouped prerequisites, and simulates connectors. Hardcoded inputs, density and same-row spacing checks are country-specific and do not cover every cross-row/title collision.
- `tools/greece_1970/layout.py`, `LAYOUT.md`: section anchors, native filters, satisfiable histories and connector checks. Its broad layout is not mandatory for small countries.
- `docs/cyprus_1970_design/LAYOUT_REVIEW.md`: subtree footprints, genuine alternatives and opening viewport.
- `Claude outputs/COLDWAR_SOV_generator/cw_focus.py`: relative offsets, icon registration and initial-view patterns. Read the generator README before running it.
- `common/national_focus/00_titlebar_styles.txt`: native focus states. `tools/israel_1970/focus_art.py` illustrates optional matching shine; do not add a glow by default.

Read inputs/side effects before running tools; these are not automatic validators for other countries. For pure layout work compare before/after semantic data excluding only approved position/navigation fields. Rewards, gates and prerequisite groups stay equal.

## Compact review record

```text
Scope: exact supplied tree/files, full tree or partial fixture
Reference: MD version/files and measurements, or unavailable
Positions: ID | anchor | emitted x/y | resolved x/y | evaluated condition
Changes: ID | old position | proposed position | purpose
Semantics: rewards/costs/gates/prerequisite groups/exclusions unchanged, or exact exceptions
Visual QA: image/view checked, measured bounds, concrete collision IDs
Separate defects: gameplay or asset issues observed but not changed by layout task
Unverified: missing input/state/render/engine checks
```

## Soviet 1970 case study

The owner selected the implemented Soviet tree as an additional project benchmark. Inspect `Claude outputs/COLDWAR_SOV_generator/cw_layout.py`, `cw_focus.py`, the emitted SOV focus file and attached `COLDWAR_UNI_1970_union_joint.txt`. Learn coherent outlook/party clusters, leader-programme fans, parallel policy domains and intentional navigation. Clusters are produced by geometry; section comments or colours in an audit image are not in-game UI bands.

The emitter subtracts each section anchor from its resolved design coordinates. It also looks for real cross-section prerequisites that can be drawn clearly instead of retaining an invisible eligibility link. Adapt only with logical equivalence, grouped requirements and readable routes; do not universally replace `available` conditions by lines.

The Union subtree reserves its full footprint, and the continuous panel searches for free space outside it. Its conditional host offset places the same joint tree differently in Soviet and generic hosts. Check every host's full subtree and panel bounds. The inspected root positions `(93,0)` for Soviet entry and `(355,8)` for Union are snapshot evidence, not coordinates to copy elsewhere. Likewise the generator's cell-to-panel conversion and pocket dimensions are local implementation choices, not universal UI constants.

The inspected audit PNGs are older than current output and are point/line graphs. Use them to understand earlier arrangements, not as exact live geometry or proof that icons/titles fit. Compare source hashes and resolved coordinates, then produce a current card-level preview. Native icon reuse and shine registration still require inspecting real textures at target size; reject oversized photographs even if registered as sprites.

Reference shortcuts and initial view make a large tree navigable, but eleven Soviet shortcuts or its broad aspect ratio are not quotas. Fit navigation and whitespace to the new country's actual content.
