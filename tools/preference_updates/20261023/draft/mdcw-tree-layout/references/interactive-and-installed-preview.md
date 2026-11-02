# IMPERIA COLD WAR: interactive inspection and installed-output verification

Use this guidance for an interactive focus-tree concept or an installed-tree visual audit. Vietnam is a case study, not a required canvas size or engine certification.

## A focus inspector must support clicking every focus

Enes explicitly requested clicking rather than only dragging, all focuses inspectable, and a wider window. Make every focus open its details, including currently locked and mutually exclusive nodes; inspection is separate from gameplay eligibility. Show English title/description, party/leader/context gates, prerequisites, cost/duration, exact benefits and drawbacks, and one-time/temporary/programme ownership where the design supplies them.

For an offer requiring another country's acceptance, opening the focus must immediately show a complete "If they accept" section for each country: exact spirit names, every signed modifier, setup and recurring costs, buildings with slots, research and other rewards. Keep those terms visible for unsigned, pending, refused, suspended, locked and mutually exclusive focuses. Do not make acceptance, a second agreement button, an expanded history section or a separate recipient decision necessary to see the numbers. Verify an unaccepted offer and an ineligible focus; the prospective Effects must remain complete while the real reward remains unexecuted.

Distinguish a click from a drag using a movement threshold; release pointer capture and suppress the click only after an actual pan. Avoid a global pan handler or transparent connector overlay swallowing node clicks. Provide zoom/fit and a usable wider responsive viewport. A details panel should not cover the selected node or consume most of the tree's viewing space. Preserve the user's selected focus/government when updating the visualization where practical.

Verify representative clicks on nodes from every programme, including locked paths; a click must open details without shifting the canvas. Also check pan, zoom, fit, narrow screens and panel overflow. If browser interaction cannot be exercised, disclose that limitation; a static screenshot cannot prove click handling. A static export can accompany the interactive inspector, not replace requested interaction.

## Reconstruct what is installed

Independently parse emitted focus files, recursively resolve relative positions, preserve prerequisite groups and exclusivity, and resolve actual live sprite registrations and English titles. Compare with the current approved revision before reusing a prior concept render. Preserve earlier immutable snapshots and use a separate revision rather than overwriting their bindings. Verify declaration order too: the native engine requires relative anchors to be defined before their dependent focuses. Include the current starting party/leader state and relevant alternatives. Inactive fixed branches still require reserved space: availability does not prove the engine hides or rearranges them.

Measure title glyphs, protruding icon bounds, card bounds and connectors at normal scale. Overview images alone can conceal collisions. Vietnam's inspected UI used a 96×130 grid, a 165×128 focus container and a 147×20 title field; these are version-specific measurements, not universal constants. Render external routing/state shading as approximations and inspect actual generated images. Do not modify global fonts, titlebars or other trees to force a local fit.

## Native art and logical references

Resolve focus sprites, matching shine companions, dynamic programme icons, idea picture aliases, decision icons and category icons through their actual native conventions. A category's full sprite reference and an idea's `GFX_idea_<picture>` alias are different contracts; compare current MD precedents. Inspect the image, not only its filename.

When converting an approved icon, preserve decoded pixels, dimensions and alpha unless an art change was requested. Check actual DDS magic/header/pixel format and decoded output rather than trusting the extension. Existing usable TGA sources need not be gratuitously converted. Match shine masks and texture paths to the corresponding focus art.

Do not flag an established native logical effect alias as a missing file solely because no literal file with that extension exists. The inspected MD shine code uses `gfx/FX/buttonstate.lua` while the base game supplies `buttonstate.shader`; verify the native pattern and provider, then reserve actual shader behavior for an engine test.

## Review freshness

Record audited source hashes, resolved positions, inspected views, approximations and scope. After small final changes, use a bounded preservation/hash refresh: check affected semantics and reuse images only if geometry, displayed titles, art and shown reward text remain representative. Do not rerender a stable layout merely because comments changed. Do not label an old hash current, and do not convert a refresh into an unrequested whole-tree balance audit.

Example evidence: `tools/vietnam_1970/LAYOUT_REVIEW.md` and `LAYOUT_REVIEW.json`. Its external installed-tree images are faithful source reconstructions, not running-game screenshots. Discover current paths from the report; skill users without those optional artifacts must create their own evidence.

## Linked national-focus event presentation

When the requested national-focus work includes its events, inspect their actual native picture class and donor window. A registered wide news sprite is not a valid country-event picture. The inspected MD donor uses a 217 x 163 photo with a specific outer frame, an inset at (19, 6) of size 180 x 150 and adjacent answer buttons. Those dimensions are version-specific. Check the complete donor geometry, actual nontransparent photo bounds, frame pixels, texture transparency, title/description area and option-entry width/slots before claiming a proper fit. Do not change global GUI positions to hide an oversized country picture. `tools/cuba_1970/validate_event_art.py` is an optional project example, not a required installed dependency. A composite made from donor assets must be labelled a layout preview rather than a live screenshot.
