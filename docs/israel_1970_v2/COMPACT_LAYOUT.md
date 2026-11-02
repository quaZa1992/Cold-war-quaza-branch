# IMPERIA COLD WAR: Israel 2.2 compact native layout

Scope: native implementation of the approved Version 2.2 catalogue. The approved `tools/israel_v2/design.json` remains immutable. The previous proposal previews and their review records are preserved. This report covers geometry; the implementation's mechanics and engine checks require separate evidence.

## Source and conversion

Approved catalogue SHA256: `aa480fcaf2c1609d7d8531164978a3d2dc0023728331775261f26eae09962706`.

The current native `interface/nationalfocusview.gui` was inspected in full for focus, symbol, title and link geometry:

| Element | Native measurement |
|---|---|
| Grid step | 96 x 130 pixels |
| Focus container | 165 x 128 pixels |
| Symbol centre within container | (87.5, 20) |
| Title | (15, 58), 147 x 20 pixels, `hoi_16mbs` |
| Title background | (5, 40), 164 x 50 pixels, visible through (169, 90) |
| Prerequisite link anchors | parent (80, 64), child (80, 0) |
| Safe normalized symbol canvas | 112 x 72 pixels |

The safe symbol occupies x31.5..143.5 and y-16..56, leaving two pixels before native title text. The complete visible symbol/title-background union is x5..169 and y-16..90. The background's four-pixel overhang beyond the 165-pixel container is included in collision and programme-footprint checks. Artwork must be proportionally fitted with transparent padding rather than stretched. Native focus fonts, titlebars and the shared GUI are unchanged.

All three base-game background donors were inspected, rather than inferring their size from the text box: `focus_unavailable_bg.dds`, `focus_can_start_bg.dds` and `focus_completed_bg.dds` are 164 x 50 with full alpha bounds. The external reconstruction embeds lossless viewing copies at their actual native size. `runtime-titlebar-donors.png` and its provenance record preserve the inspected sources and hashes. The browser's Georgia label rendering remains an approximation of native `hoi_16mbs`; it does not modify a shared game font or GUI.

Current main-MD `00_generic.txt` and `05_russia.txt` were also parsed. Generic contains 158 direct focuses and Russia contains 806. Sampled root, fan and join layouts use one-row steps and two-column card separation, including native relative anchors. These are reference measurements rather than a universal country-tree size.

## Arrangement

`tools/israel_v2/runtime_layout.py` exposes `arrange(data) -> deepcopied data` and `audit(data)`. The function has no file I/O. It changes only `xy`, group origins and the pixel-conversion metadata. Full semantic comparison, input immutability and repeated-call idempotence pass.

The arrangement uses compact national bands, keeps Territories and Mafdal adjacent for their real visible cross-programme prerequisite, and fills free pockets with smaller party programmes. The major parties retain their complete downward continuation. Their branch footprint is reserved even when that party does not govern.

Long connections were cleared by moving individual cards within their programmes. Examples include the reserve exercise/call-up pocket, interleaved controlled and foreign settlement columns, the separate ending-funding row, the early Gahal health bill, and shifted industrial and communal follow-ups. These edits retain all prerequisite groups and exclusions exactly. No visible prerequisite became an availability gate.

On the unchanged 213-focus catalogue, independent checks pass for all 244 prerequisite connections:

- No overlap between any full 165 x 128 focus containers.
- No overlap between normalized art/title bounds.
- No overlap between complete programme footprints, including clearance.
- Every prerequisite descends and every exclusive alternative remains on its choice row.
- No connection in the native-anchor orthogonal approximation crosses another focus's visible art or title.

The native card bounds are 3525 x 5198 pixels. Rendering the approved coordinates on that same native grid would occupy 6117 x 7018 pixels. The compact arrangement reduces width by 42.37%, height by 25.93% and bounding area by 57.32%. This comparison isolates coordinate compaction rather than counting the old browser's taller conversion as a layout improvement.

The separately authorized real financing focuses `ISR2_financing_usa`, `ISR2_financing_ger` and `ISR2_financing_rom` occupy a compact final capital row at local (-3,6), (0,6) and (3,6). Lower programme bands move down one native row to retain clear full footprints. The additionally authorized `ISR2_security_emergency` supplies the actual paid cabinet authorisation behind the approved RP-emergency gate. Its local (-5,3) position fills free space in the reserve programme without widening the group. The actual extended 217-focus, 245-connection data passes the same coordinate-only semantic and geometry checks. Its native bounds are 3525 x 5328 pixels. Complete programme footprints retain clearance around the full native title backgrounds. Native emitted-code reconstruction, rendered checks and engine checks remain separate steps.

## Art findings and evidence limits

The earlier proposal used thumbnails, not original texture dimensions. The native source audit found large canvases: `agricultural_banks` 200 x 100, `democratic_socialism` 153 x 170, `focus_public_housing` 166 x 95 and `industrial_subsidies` 150 x 150. Alpha bounds distinguish padding from real art: agricultural banks has only an 86 x 90 visible area, whereas democratic socialism fills its large canvas. This is an intrinsic symbol/title issue, not something fixed by separating programme roots. The implementation compiler is responsible for normalized ISR2 sprites or suitable existing native donors; this layout reserves the safe normalized dimensions.

The mechanical packaging stage is now implemented as `runtime_art.build(data)`. The immutable catalogue contains 86 distinct assigned motifs. All 86 complete source registrations and original textures resolve. The in-memory build returns 86 native DDS copies, 86 per-asset provenance records, a combined base/shine GFX file and a notice. It also returns exact normalized PNG pixels for the future source-derived preview. Each motif is alpha-cropped, proportionally downscaled only where necessary and centred on a 112 x 72 transparent canvas with at least two transparent border pixels. No motif is repainted, source asset overwritten or catalogue field changed.

Two independent build calls returned identical files. All 86 outputs decode as 112 x 72 RGBA and preserve the normalized pixels exactly through native uncompressed DDS encoding. All 172 base/shine registrations are unique, and every DDS has a matching source/output hash and modification record. These checks emitted no loaded asset file. Caller emission and native rendering remain separate steps.

The domestic emitter's state-institution enable guard uses an explicit `204 = { ... }` state scope. This follows the independent finding that a state-attached dynamic modifier with `scope = ISR` evaluates its enable guard from the country context. Bare country-context `is_owned_by` or `is_controlled_by` statements are not used.

The unsupported shelter building and unspecified country-level casualty modifier have concrete native replacements: one Tel Aviv urban shared slot, a named civil-defence institution, and a focus-granted medical-protocol custom technology. The technology follows `common/technologies/custom_tech.txt:KOR_celltrion_tech` and gives +10% casualty trickleback specifically to `combat_service_support_company` and `helicopter_combat_service_support`. The focus preview names both unit groups and their values. This is a disclosed scope adaptation, not a general casualty bonus or an additional invented repair modifier. The 0.01%-GDP weekly establishment remains.

`test_runtime_domestic.py` passes twenty-two source-driven fiscal and lifecycle regressions, including the emitted real bilateral pool-consumption and early-loan-repayment bodies. These cover quote purity, bounded envelopes, exclusive matching programmes, current ownership/capacity/capital rechecks, one-time slots/factories, anonymous versus named debt and creditor payment, coupon consumption, reserve replacement/release/expiry, political costs and the real cabinet-authorisation cooldown. Native-load findings also have targeted regressions: political-power/stability requirements use actual native trigger names, including their exact payment boundaries; negative Treasury and debt quotes use sequential temporary assignment and multiplication. All six timed country-flag dictionaries explicitly set `value = 1`. The bounded model now treats an omitted dictionary value as zero and inactive, correcting an earlier false assumption. The 181/182-day exercise, 69/70-day call-up and 179/180-day cabinet cooldown boundaries are checked. Removing the explicit values from an in-memory payload makes all four targeted flag/expiry regressions fail as expected. The bounded interpreter models the inspected native Treasury/debt variable consumers; it does not constitute a HOI4 gameplay test.

The routed-line audit uses the inspected native link anchors and a three-segment orthogonal join. It checks the visible symbol/title union separately from the full container's empty lower area. The game's internal connector router is not controlled by these coordinates. Native rendering, multiway exclusion decoration, hover behaviour, camera shortcuts and continuous-focus-panel placement remain engine-check items. No running-game test is claimed here.

Provenance: the coordinate arrangement and checks were authored for IMPERIA COLD WAR with Codex. Existing native images retain their inherited project/MD/Imperia attribution. Individual authors or separate asset licences remain unknown where inherited records do not identify them. See `IMPERIA_COLD_WAR_NOTICE.md`. No artwork was generated or repainted by this layout work.
