IMPERIA COLD WAR

# Kissinger implementation: independent layout and owner inventory

Independent read-only planning and emitted-code review, 2026-10-28. The user
approved the Kissinger concept for implementation. This reviewer has changed
no mod runtime, generator, image, localisation or approval file. Outputs are
this review document and the separately authorised source-preview artifacts
in the conversation's visualization directory. The recorded baseline below
supports the final emitted-code comparison near the end of this document.

## Recorded preimplementation host

`common/national_focus/USA_1970.txt` still has SHA256
`5d18bafd4d1c972115cb2f7cd9395e6694de33ab8a8b6209fc6f82c777c1f32b`.
It contains 301 direct IDs, 300 visible cards, nine shortcuts, no shared-focus or
joint-focus import and no conditional focus offsets. The hidden legacy Gulf
Contacts receipt accounts for the one invisible ID. Current direct focus bounds
are x=-33..38 and y=0..58. Fractional x positions exist, so coordinate resolution
must use floats rather than integer-only parsing.

The naval adaptation contains twenty nodes. Its direct root is
`COLDWAR_NAVY_USA_naval_reform` at28,16; the other nodes use relative offsets from
that earlier root. Its canonical profile is
`tools/naval_adaptation_1970/profiles/USA.json`. The main defence pocket is around
x21..25, y1..12; naval additions are around x23..32, y16..21. The fifteen-ID Gulf
pocket remains x30..38, y0..7, with fourteen visible cards. No Gulf move is needed
to make physical space for the forty-one new cards.

Leave the original initial camera0,0, continuous-focus panel(-3200,1800) and
naval anchor intact. They do not intersect the new right-hand footprint.

## Canonical insertion point and semantics

The USA owner is `tools/usa_1970_expansion/compile.py`. Its build_tree currently
finishes in this order: original presentation, Gulf-owner replacement,
calendar presentation, then `naval_adapter.integrate_tree('USA', text)`. Insert
the new canonical module after those steps and before returning the final tree.
The writer's date pass must remain idempotent and preserve the new marked block.
Do not run the broad country generation merely to add these focuses.

The Gulf owner remains `tools/iraq_1970/usa_module.py`, reached through
`tools/usa_1970_expansion/gulf_revision.py`. Preserve all fifteen Gulf IDs,
including the hidden legacy Contacts receipt, and its real access, relief and
settlement contracts. Desert Storm, Desert Shield and Coalition Mandate remain
independent crisis entries. Early Kurdish funding must not become a mandatory
prerequisite for responding to an Iraqi attack on Kuwait.

For position anchoring, the new doctrine can reference the earlier
`USA_1970_F0` at14,1 with relative offsets41,-1, placing it at55,0. This is only a
position anchor. The approved doctrine has no focus prerequisite; do not add an
unapproved mandatory completion of the old foreign-policy root. Every remaining
new focus can anchor to the earlier doctrine by subtracting55,0 from its desired
world coordinate. The approved data order already declares parents before their
children; preserve that ordering and independently recheck it after emission.

## Compact actual coordinate recommendation

All forty-one approved world coordinates are currently unique and clear of the
301 existing cards under the inspected165x128 native container and96x130 grid.
The nearest possible old/new x gap is three grid columns,288 pixels, before
considering their different rows.

Six small coordinate overrides improve native connector safety and compactness.
Place Clients and Political Alternatives on the same row3 as THE KURDS, because
all three descend from Deniable Pressure. Their old row4 placements allow a
normal midpoint connector to pass the intervening Kurdish hub. Move their
single descendants to row4. Keep these theatre columns outside the Kurdish
fan, then bring the right edge from87 to81. This changes no prerequisite,
exclusion, cost, reward or political requirement. Other approved positions are
unchanged. The JSON below is the complete suggested mapping, not emitted code.

```json
{
  "project": "IMPERIA COLD WAR",
  "phase": "Read-only implementation layout recommendation; final emitted-code review pending",
  "root": {
    "id": "COLDWAR_USA_KS_doctrine",
    "world": [
      55,
      0
    ],
    "relative_position_id": "USA_1970_F0",
    "relative_xy": [
      41,
      -1
    ],
    "new_prerequisite_on_anchor": false
  },
  "child_relative_position_id": "COLDWAR_USA_KS_doctrine",
  "child_relative_rule": "Subtract [55,0] from each world coordinate. Declare doctrine before every child.",
  "positions": {
    "COLDWAR_USA_KS_doctrine": [
      55,
      0
    ],
    "COLDWAR_USA_KS_limited": [
      53,
      1
    ],
    "COLDWAR_USA_KS_expanded": [
      57,
      1
    ],
    "COLDWAR_USA_KS_triangular": [
      43,
      2
    ],
    "COLDWAR_USA_KS_covert": [
      55,
      2
    ],
    "COLDWAR_USA_KS_guarantees": [
      81,
      2
    ],
    "COLDWAR_USA_KS_beijing": [
      41,
      3
    ],
    "COLDWAR_USA_KS_moscow": [
      45,
      3
    ],
    "COLDWAR_USA_KS_clients": [
      73,
      3
    ],
    "COLDWAR_USA_KS_angola": [
      73,
      4
    ],
    "COLDWAR_USA_KS_political": [
      77,
      3
    ],
    "COLDWAR_USA_KS_chile": [
      77,
      4
    ],
    "COLDWAR_USA_KS_shuttle": [
      81,
      3
    ],
    "COLDWAR_USA_KS_kurds": [
      55,
      3
    ],
    "COLDWAR_USA_KS_irq_contacts": [
      43,
      5
    ],
    "COLDWAR_USA_KS_irq_transit": [
      41,
      6
    ],
    "COLDWAR_USA_KS_irq_anatolia": [
      45,
      6
    ],
    "COLDWAR_USA_KS_irq_fund": [
      43,
      7
    ],
    "COLDWAR_USA_KS_irq_autonomy": [
      41,
      8
    ],
    "COLDWAR_USA_KS_irq_front": [
      45,
      8
    ],
    "COLDWAR_USA_KS_irq_settlement": [
      41,
      9
    ],
    "COLDWAR_USA_KS_irq_independence": [
      45,
      9
    ],
    "COLDWAR_USA_KS_irn_dossier": [
      51,
      5
    ],
    "COLDWAR_USA_KS_irn_contacts": [
      51,
      6
    ],
    "COLDWAR_USA_KS_irn_fund": [
      51,
      7
    ],
    "COLDWAR_USA_KS_irn_rights": [
      49,
      8
    ],
    "COLDWAR_USA_KS_irn_front": [
      53,
      8
    ],
    "COLDWAR_USA_KS_irn_claim": [
      53,
      9
    ],
    "COLDWAR_USA_KS_tur_dossier": [
      59,
      5
    ],
    "COLDWAR_USA_KS_tur_alliance": [
      57,
      6
    ],
    "COLDWAR_USA_KS_tur_breach": [
      61,
      6
    ],
    "COLDWAR_USA_KS_tur_networks": [
      61,
      7
    ],
    "COLDWAR_USA_KS_tur_rights": [
      59,
      8
    ],
    "COLDWAR_USA_KS_tur_front": [
      63,
      8
    ],
    "COLDWAR_USA_KS_tur_claim": [
      63,
      9
    ],
    "COLDWAR_USA_KS_syr_contacts": [
      67,
      5
    ],
    "COLDWAR_USA_KS_syr_voice": [
      67,
      6
    ],
    "COLDWAR_USA_KS_syr_organisation": [
      67,
      7
    ],
    "COLDWAR_USA_KS_syr_rights": [
      65,
      8
    ],
    "COLDWAR_USA_KS_syr_front": [
      69,
      8
    ],
    "COLDWAR_USA_KS_syr_claim": [
      69,
      9
    ]
  }
}
```

The native source compositor places an approximately90-pixel symbol around
x+87.5,y+20 and the164x50 bar atx+5,y+40. It must include the protruding symbol
above the nominal origin when checking actual bounds. With90-pixel new icons,
a one-row130-pixel step leaves approximately15 pixels between complete visible
symbol/bar footprints. Two-column peer steps leave27 pixels between165-pixel
containers. Final art bounds and engine routing still require actual render
inspection, not just point-distance checks.

## Native caption and art strategy

The native title field is147x20 using hoi_16mbs. Twelve approved descriptive
titles exceed147 pixels in the actual installed bitmap font. Do not enlarge
fonts or titlebars to hide clipping. Keep their political descriptions and use
these concise map captions, all measured with the installed font atlas:

| Focus suffix | Suggested native caption | Width, pixels |
| --- | --- | ---: |
| irq_settlement | Guarantee Autonomy | 127 |
| irq_independence | A Separate Kurdistan | 125 |
| irn_contacts | Zagros Networks | 99 |
| irn_fund | Mountain Committees | 132 |
| irn_front | Challenge Tehran | 102 |
| irn_claim | A Kurdish Claim | 93 |
| tur_networks | Southeastern Contacts | 135 |
| tur_rights | Regional Rights Talks | 127 |
| tur_front | An Armed Alternative | 130 |
| tur_claim | A Separate State | 101 |
| syr_rights | Citizenship and Rights | 131 |
| syr_claim | Northern Authority | 115 |

The root and other twenty-eight new names fit the native147-pixel field. Use
`tools/iraq_1970_concept/native_font.py` only as a read-only measurement helper;
its title shortening is not permission to change approved descriptions.

Use the twelve approved generated medallions as actual focus-class textures at
approximately90x90, with alpha preserved and a valid native DDS/TGA encoding.
Register literal sprite names and verify their resolved files and dimensions.
Retain the normal default_style titlebars from00_titlebar_styles.txt and their
existing unavailable/available/current/completed states. No global GUI or font
change is justified. The atlas is concept artwork until those registrations,
textures and native render references exist; preserve its recorded generation
provenance and create no visible watermark.

## Navigation and existing programme integration

The actual shortcut_grid ininterface/nationalfocusview.gui declares one column
and eight vertical slots; the current USA source already declares nine
shortcuts. This is a measured capacity concern, not proof of what the native
engine currently clips. Do not blindly append six more country bookmarks or
change the global GUI. A bounded option is to retarget the existing Foreign
Policy shortcut to the new doctrine and retain Gulf access separately. The
Kurdish chapter is then reachable from the visible doctrine branch. Record any
navigation retarget explicitly and inspect the actual engine when possible.

Existing related content includesNIX_F1 Beijing Backchannel(6,1),NIX_F4 The
President in Beijing(6,2),NIX_F5 The Moscow Summit(8,2),F5 Triangular Diplomacy
(14,3),USA_X_china(10,13) andUSA_X_soviet_exchange. The new forty-one focuses
remain the approved count, but their strategic institutions must not
accidentally re-award an existing trade/scientific agreement's setup assets or
create a second incompatible receipt for the same contract.

The current canonical manifest hardcodes301 total IDs, and the old installed
renderer asserts300 visible cards. With exactly the forty-one approved additions
and no new hidden cards, the expected counts become342 registered and341
visible. Update derived metadata from the actual final tree or verify the added
set before changing expected counts. Do not present the old300-card render as
current. The new source reconstruction should include normal-scale Kissinger,
all four country branches and the old Gulf/naval/foreign neighbours, plus a
whole-tree overview. The existing source renderer's static routing remains an
approximation until checked inside HOI4.

## Independent emitted-code review: completed

No remaining geometry blocker was found within the bounded focus-layout and
native-panel scope after the owner corrected the initially oversized textures.
The later native-log follow-up below identified shine registration and a
shortcut number-token issue that the initial static check did not establish.
The following findings concern current emitted files, rather than only the
approved concept:

- The actual USA tree has342 unique direct focus IDs:301 existing and41 new.
  There are341 visible focuses and the same hidden legacy Gulf receipt. New
  resolved bounds arex41..81,y0..9; old bounds remainx-33..38,y0..58. All relative
  references resolve to earlier declarations. No165x128 native node-card bounds
  overlap between new nodes, or between a new node and any existing node.
- All41 new prerequisite groups exactly match the implementation's immutable
  approval snapshot. Their AND/OR structure is preserved, every prerequisite
  and exclusion resolves, exclusions are reciprocal, the graph is acyclic,
  and each node has at least one structurally reachable ancestor combination
  consistent with those exclusions. Runtime diplomatic and military gates
  require their separate gameplay review.
- The three old Desert Shield, Desert Storm and Coalition entries remain
  independent roots. No Kurdish funding prerequisite was attached to Kuwait
  intervention. The doctrine remains an independent entry at55,0. Four country
  tops remain at43,5;51,5;59,5;67,5, under the Kurdish hub at55,3.
- There is one intentional effect integration among the301 existing focuses:
  `COLDWAR_USA_gulf_arm_front` now routes its completion reward through
  `COLDWAR_USA_KS_legacy_irq_preview` and `COLDWAR_USA_KS_legacy_irq_start`.
  The shared Iraqi authority replaces the parallel legacy underground start.
  Its existing36,2 position, ID, native icon, Open Northern Channels prerequisite
  and Limited War exclusion remain. The other300 existing focus ASTs are
  preserved. This is an authorised reward integration, so a claim that all301
  full focus ASTs remained unchanged from the preimplementation tree would be
  incorrect.
- Every new emitted caption was measured against the actual `hoi_16mbs` bitmap
  font and fits the147px native name box. The maximum is142px for `Arm the
  Mountain Front`. All twelve proposed native caption shortenings are emitted.
  Existing titlebar styles, global fonts and global focus-item geometry are
  reused. Main orthogonal branch corridors avoid intervening cards under the
  inspected source layout; native connector rendering still needs an engine
  view.
- The existing sixth USA shortcut, `USA_1970_foreign_shortcut`, now targets
  `COLDWAR_USA_KS_doctrine`. Its native Foreign Policy caption and slot remain.
  The independent Gulf shortcut still targets Desert Storm, and the existing
  naval shortcut remains. No additional shortcut or global eight-slot change
  was introduced. The USA tree already had nine shortcuts before this change;
  the new branch does not increase that inherited count.
- Pure calls to `patch_tree` on the emitted tree are byte-idempotent, including
  a second repeated call. A read-only canonical USA `build_tree` reconstruction
  matches all342 current focus ASTs, including the intended Arm the Mountain
  Front reward integration. The owning staged Gulf fragment also receives
  `gulf_bridge.patch_legacy_focus`, preserving the change through the canonical
  rebuild. The pre-existing naval shortcut now uses parser-safe `0.8`, and the
  entire canonical USA `build_tree` output equals the installed tree byte for
  byte. The earlier static inference that `.8` would be equivalent was wrong
  for the native engine, as the follow-up log below established. This reviewer
  did not execute a runtime writer, compiler main, asset emitter or game run.
- All twelve actual new DDS files decode as90x90 RGBA with transparency. The
  generator and provenance record both preserve that90px extraction. All twelve
  sprite declarations resolve, and the ten sprites currently referenced by new
  focus nodes resolve. Gulf art sprites10/11 are registered and available while
  the old Gulf focuses retain their existing native art. The source atlas hash
  remains`df158e35ad6f3f852d35347e2e0742181d83b543c2fba2b5291327592ba21623`.
- All twelve images were visually inspected at native size. Six representative
  emitted focus cards were also composed in memory with the actual164x50 native
  unavailable titlebar and native bitmap-font raster. The Kissinger portrait,
  country medallions, longest tested caption and neighbouring rows fit the
  normal icon/title geometry. This was a donor-composed source reconstruction,
  not a game screenshot. The final source-preview artifacts described below
  were then written outside the mod with the owner's explicit authorisation.
- The four emitted decision-category controllers, windows and categories have
  exact matching references. Each root is493x112 at5,0; all text and the240x16
  progressbar remain within it. Each bar and numerical readout use the correct
  fixed host scope:IRQ/PER/TUR/SYR. Dynamic legacy/warning text uses the same
  host scopes. All headings and status variants fit their native text boxes;
  the widest status is340px of469, and `Unrest: 100/100` is93px of221.
- The emitted GFX is the inspected neutral native autonomy/NKO progress donor,
  with100 steps and the existing progress effect path. Its use through an
  `iconType.spriteType` field also has existing native MD progressbar examples.
  The cache rounds the authoritative0..100 theatre unrest into the frame
  variable; the controllers have host-qualified dirty variables and no GUI
  actions or effects. Displayed legacy and warning changes are included in the
  cached invalidation check. The complete current category-header/description
  donor remains unchanged by these custom windows.
- The one bar deliberately represents whole-theatre unrest, matching the user's
  later simplification. It does not claim that every Iraqi state has its own
  visible meter. The source birth requirement is separate from that display:
  Iraq uses two actually held eligible states and the other hosts use their
  selected local state. Numeric counterplay, consent, payout and uprising
  correctness remain the gameplay review's responsibility.
- Reviewed script/GUI/GFX files are UTF-8 without BOM and begin with the exact
  project marker. The English localisation has its required BOM and marker
  below `l_english:`. Native event artwork is referenced unchanged through
  `GFX_political_deal`; its provider texture decodes at217x163. No new event
  frame, event-option geometry or global country-decision geometry is supplied
  by this integration.

The final inspected tree hash is
`dd0210b28f0577bccb6ef525bc59cd6c288a02fc521bd243dd5f920ee84713bd`.
The current Kissinger English localisation hash is
`8611b2cf53bdac05660fd07c54ffb4add6980ce24db359cf4e9bd1691f5b1f58`.
The panel GUI hash is
`746a4bdea9be0018046c0cca128ac3c8142da3a4f27e314ddeb3990665dc84a6`;
its GFX hash is
`8ca11139ea85271690e75ee3282013007ef4c58a6916d7ac1bf5637babd27fb2`;
the controller hash is
`d7fbf4d85892de36b9e8ada802338d39f00845174025bb3818332701be09d625`.

Native camera/connector views, focus and decision hover previews, category
stacking at different UI scales, zero/maximum bar rendering, switching between
USA and host views, host annexation, save/reload and multiplayer rehearsal were
not performed. Full numerical mechanics, historical identity and multiplayer
stress evidence are separate review responsibilities. Source closure and a
donor-composed preview do not establish those runtime results.

## Native art-API and parser follow-up

An existing native run, rather than boilerplate convention, establishes an
actual shine-registration warning for all41 new focuses. The inspected log is
`E:/HOI4_Mod_Tools/mdcoldwar/runtime/france_1970/20261028_213341_298325/profile/logs/error.log`,
SHA256`033987e8071a74aaebe182ebbdbfce634ed3422d5139b358187a7030a0c35de0`.
Lines707..747, timestamp22:34:57, contain one `Missing icon shine for focus`
warning for each KS focus. This confirms that the current engine expects
the shine sprite lookup for warning-free focus registration. It does not
establish a fatal load failure or prove that a base icon becomes invisible.
The precise selected/completed fallback behaviour was not observed.

The complete native donor at `interface/goals_shine.gfx` lines12514..12547
registers `army_reform_shine` with the same texture as `army_reform`,
`effectfile = "gfx/FX/buttonstate.lua"`, two native scrolling/add animations
masked by that same texture, and `legacy_lazy_load = no`. Both animations use
`gfx/interface/goals/shine_overlay.dds`, rotations-90/+90, no looping,0.75s,
delay0, offset0,0 and scale1,1. That overlay exists unchanged in the base game
at87x88. Each of the twelve KS base goal sprites can receive a corresponding
`_shine` declaration copied from this complete donor, changing only its name,
texture path and both mask paths. No DDS modification is necessary. The GUI's
separate highlight/continuous glows do not provide evidence of an automatic
replacement for this engine lookup.

The same log's line706 explicitly reports `Malformed token: .8` for the USA
naval shortcut near line9541. This supersedes the initial static inference of
numeric equivalence. The canonical USA builder already emits `0.8`; the
installed shortcut must use that parser-safe spelling consistently.

The owner subsequently fixed both confirmed issues in source and in the
owning generator. Independent reinspection verifies twelve paired `_shine`
declarations with the same90px DDS as texture and both masks, the native
buttonstate shader and all donor animation settings. The emitted GFX equals
the owning generator's output byte for byte. During that correction, only the
inherited shortcut's number token changed in the tree; all focus ASTs and
geometry remained identical to the preceding reviewed version. The current
hashes, including the subsequent requirement-presentation refresh, are above.
The canonical main USA tree now matches byte for byte and KS patching remains
idempotent. This establishes source resolution; a subsequent native run must
still establish warning-free loading and selected/completed rendering.

## Installed branch source previews

Six final previews were generated with the existing
`tools/iraq_1970/render_installed.py` helper imported without running its main
or any country compiler. The wrapper reads the actual341 visible nodes and
current sprite/localisation registries. It preserves installed world positions,
native96x130 grid,90px medallions,164x50 native titlebars and147px bitmap-font
captions. Country-detail views retain native pixel scale; only the full
overview is reduced from4080x1425 to2600x908. All six saved images were opened
and visually checked. Names, medallions and cards remain legible without card
collisions in the normal-scale details. Header labels explicitly state source
composition, approximate links and no engine test.

Artifact directory:
`C:/Users/Enes/.codex/visualizations/2026/10/24/01a16eeb-40d0-7851-80fa-70784386712c/usa-kissinger-installed-20261028`.

- `USA_KISSINGER_INSTALLED_OVERVIEW.png`: the complete41-focus branch at its
  actual installed coordinates.
- `USA_KISSINGER_IRAQ_NATIVE_SOURCE.png`,
  `USA_KISSINGER_IRAN_NATIVE_SOURCE.png`,
  `USA_KISSINGER_TURKEY_NATIVE_SOURCE.png`,
  `USA_KISSINGER_SYRIA_NATIVE_SOURCE.png`: bounded normal-scale country routes.
- `USA_GULF_IRAQ_CONTEXT_NATIVE_SOURCE.png`: the retained old Gulf pocket and
  the new Iraqi branch in their real neighbouring positions.

The directory also contains `layout_evidence.json`, `NOTICE.md` and the small
read-only `render_source_preview.py` wrapper. These record exact source hashes,
credits, unknown separate redistribution permissions and composition details.
They are source-composed previews, not screenshots. No image-generation tool,
gameplay effect, native test run, save mutation, texture repaint or mod-file
write occurred during this preview step.

The later source refresh introduced requirement-presentation wrappers and
expanded documented payment comparisons, while retaining all focus IDs,
coordinates, icons, captions, prerequisite groups and exclusions. This reviewer
compared the41 current layout/graph records against the preceding saved source
evidence and found no differences. Actual NATO membership checks remain in the
relations trigger. The pure canonical main USA build still equals the current
installed tree byte for byte, and KS patching remains byte-idempotent.

All six previews were regenerated against the final tree and localisation
hashes recorded above. Every resulting PNG is byte-identical to its preceding
version, confirming that these changes do not alter the rendered source layout.
The refreshed `layout_evidence.json` now explicitly includes both relevant USA
localisation input hashes and individual preview hashes. This is visual and
source-reproducibility evidence; native execution of the amended payment gates
is outside this bounded layout review.

The final wording-only localisation refresh makes the recognition requirement
explicitly say `independent` and the Iraqi territorial requirement explicitly
say `owns and fully controls`. Every one of the41 emitted focus captions still
matches the saved preview metadata. Only the locale input hash was refreshed;
the six PNGs were not regenerated for these two requirement-text changes.
Their previously established byte-equality and recorded image hashes remain
valid. Tree and GFX hashes are unchanged.

The owner also applied the same bounded one-character `.8` to `0.8` naval
shortcut normalisation to
`common/national_focus/COLDWAR_IRQ_1970_focus.txt`,
`common/national_focus/COLDWAR_SOV_1970_focus.txt` and
`common/national_focus/COLDWAR_UAE_1970_focus.txt`. Each current
`COLDWAR_NAVY_<TAG>_shortcut` was independently read and uses `0.8`.
The owning `tools/naval_adaptation_1970/naval_adapter.py` already emits that
spelling. These parser corrections do not introduce focus, programme or
geometry changes and are separate from the Kissinger visual footprint.

## Provenance

Measurements come from the current target USA tree, its canonical owners, the
installed HOI4 focus GUI and bitmap font, and the approved DESIGN.json. Native
Paradox, Millennium Dawn and project attribution remains in those providers and
IMPERIA_COLD_WAR_NOTICE.md. Artwork provenance remains inART_PROVENANCE.json.
Separate original author credit or redistribution permission is unknown where
not established by those notices. No native or runtime binary asset was copied
or altered by this reviewer; only the authorised composed preview images were
written outside the mod.

## Native regional-contest decision-category panel

The small Iraqi PMF donor was inspected in full: `interface/Iraq_civil_war.gui`
lines333..363, `common/scripted_guis/99_IRQ_scripted_guis.txt` lines3..11,
`common/decisions/categories/99_IRQ_decision_categories.txt` lines106..117,
and both referenced declarations in `interface/MD_scripted_gui.gfx`. Its
`context_type = decision_category`, host-qualified `dirty` and progress-property
binding are suitable patterns. Its visual assets are not suitable for a general
Kurdish contest: the404x36 PMF fill contains a militia emblem, while the alternate
PER404x36 fill contains the Iranian flag. Both were decoded and visually
inspected. The PER frame is neutral420x52, but the donor's declared50x60 root
does not contain its visible420px bar/frame and110px readout. Do not reproduce
that overflow.

The safer compact donor is the complete North Korean naval-buildup progress
chain: `interface/MD_NKO_guis.gui` lines196..277,
`common/scripted_guis/99_NKO_scripted_guis.txt` lines31..46, and
`interface/MD_scripted_gui.gfx` lines124..132. Its native progressbar uses plain
blue/tan chevrons without country or organisation insignia. Both source textures
were decoded and visually inspected; each is181x16 and the donor deliberately
sizes its progressbar240x16. This is a real `progressbartype`, not an indexed
sprite atlas. Its declared `steps = 100` supports a cached value clamped0..100;
do not add1 as one would for a one-based sprite sheet.

Register one custom-named GFX declaration that reuses the native texture paths:

```text
progressbartype = {
    name = "GFX_COLDWAR_USA_KS_regional_progress"
    textureFile1 = "gfx/interface/autonomy/subject_progress_bar_long.dds"
    textureFile2 = "gfx/interface/autonomy/subject_progress_bar_long_bg.dds"
    size = { x = 240 y = 16 }
    effectFile = "gfx/FX/progress.lua"
    steps = 100
}
```

The current target `interface/countrydecisionview.gui` was inspected through the
complete category-header and category-description blocks. Its decision grid is
520px wide; its description container is514px atx5, and the collapse controls
occupy the separate header. Do not change that global donor. A per-host panel
can use this bounded geometry with the donor's existing fonts:

| Element | Local position | Maximum extent | Native font |
| --- | --- | --- | --- |
| Root container |5,0|493x112|none|
| Title or route-status line |12,4|469x22|hoi_18b|
| Neutral progressbar |12,34|240x16|none|
| Numeric unrest and threshold |260,32|221x20|hoi_16mbs|
| Organisation and warning timers |12,58|469x20|hoi_16mbs|
| Regional values or status |12,82|469x20|hoi_16mbs|

All children fit inside the493x112 root: its absolute extent isx5..498,y0..112.
Use the real container height so native decisions can follow below it, and
leave room beneath the final20px line. There is no need for a second background
or a scaled PMF frame. Keep all actions in the native decisions beneath the
panel, with no GUI effects, click handlers or hidden economy transactions.

Use four distinct windows/controllers bound from the corresponding native
categories, with explicit host references `IRQ`, `PER`, `TUR`, `SYR`. The Iran
tag is `PER`, verified from current country-history files. For example, the IRQ
controller binds `properties.<unique_icon_name>.frame = IRQ.<cached_unrest>` and
`dirty = IRQ.<gui_revision>`; its numeric localisation must use the same IRQ
scope even when the viewer is USA. Increment the revision only when a displayed
value, pending-offer state, accepted-route state or status flag changes. The
bar's cached source is clamped0..100 by gameplay update code; the GUI must not
compute or own authoritative unrest, timers, costs or diplomatic consent.

Name the exact aggregate shown by a single bar. A maximum, average or selected
region is not itself proof of the two-region uprising condition. Show hot-region
count and the actual organisation/warning timers separately, with the full
region breakdown available on hover if it cannot fit the one native text row.
Status text must distinguish an unsigned/suspended channel from a delivered
programme. Native zero, maximum, fractional rounding, acceptance/suspension,
host annexation, save/reload and switching between attacker/host views remain
required engine checks. These donor/source measurements are not evidence of a
live screenshot or successful multiplayer run.

The native progress effect path is supplied by the installed game's engine
assets; it was referenced by both donor declarations but was not exposed as a
loose file at the inspected base-game path. This does not justify shipping a
replacement shader. Native texture author credit/licence beyond existing
Paradox/MD notices is unknown. No donor texture or runtime file was changed by
this review.
