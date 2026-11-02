IMPERIA COLD WAR

# Intelligence Agency screen source audit

## Finding

**P2 visual defect, source correction applied.** The project declared two frames for `GFX_agency_upgrade_repetition_icon`, while the installed HOI4 1.19.4.1 definition and 96 by 32 native DDS use three horizontal 32 by 32 states. The upgrade entry selects frame 1. The two-frame override split the atlas into 48 pixel slices, crossing the green and amber states and matching the reported tiny dots/rectangles.

I changed the project declaration to three frames. The screenshot remains a 153 by 83 crop; live rendering could not be verified.

## Source comparison

- Current project: [countryintelligenceagencyview.gfx](../../interface/countryintelligenceagencyview.gfx:87). `GFX_agency_upgrade_repetition_icon` uses `cont_focus_check_icon_small.dds` with `noOfFrames = 2` at lines 87 to 89.
- Installed game 1.19.4.1: `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/interface/countryintelligenceagencyview.gfx:88`. It declares `noOfFrames = 3` at line 90. `system.log:226` identifies the loaded version as Operation Postern v1.19.4.1.99a5 (2c90).
- Current main MD workshop donor GFX is byte-identical to the project GFX and carries the same two-frame declaration. The project GUI is identical to the donor apart from the project marker comment.
- The base-game DDS is 96 by 32 pixels and has three side-by-side status images. There is no project override for this texture.

The smallest proposed correction is changing only the project GFX frame count from two to three. Keep the GUI’s `frame = 1`, scale and layout unchanged until a live screenshot confirms any remaining issue.

## Entry and surrounding layout

The popup is 1092 pixels wide and clamped to 789 pixels high. Each branch row is 1040 by 140 pixels, with a 125 pixel upgrade scroller and 205 by 150 grid slots. Each upgrade card is 200 by 115 pixels. Its repetition box begins at x=37, y=63, uses a 100 by 20 area and 2 pixel spacing. Each repeated icon slot is 11 by 21 pixels; its image is scaled to 0.7 and requests frame 1. These positions match the installed game GUI.

The native queue badge is separate: it is hidden by default, 30 by 30 pixels at x=105, y=-18, with clipping disabled and a numbered circle background. Its fields match the native queue layout. There is no progressbar inside `upgrade_entry`; the `upgrade_progressbar` belongs to the Operatives panel. The reported green markers are therefore tied to the repetition sprite, not that progressbar.

## Industrial Espionage data

`upgrade_blueprint_stealing`, localized as Industrial Espionage, has three upgrade levels. Each level adds `operation_steal_tech_outcome = 0.15`; completion charges 10 treasury and adds 2 intelligence-community opinion. Its complete block is identical to the current MD workshop donor. I found no France-only cost, progress or queue setting in this definition.

The relevant icon `agency_steal_blueprints.dds` is 68 by 68 pixels. The card button texture is 164 by 50 pixels. Neither is the repeated green dot texture.

## Scope

This audit used the user-provided screenshot, installed source and assets only. Computer-use access was denied for this task and was not retried or bypassed. No game files were edited. I did not reproduce the interface in game, so the exact rendering and gameplay cost timing remain unverified.

## Applied correction and update owner

`interface/countryintelligenceagencyview.gfx:87-90` now declares `noOfFrames = 3` and marks the custom line. A scoped file-start comment identifies this integration. A revert-to-donor comparison confirmed every other GFX byte is unchanged. The GUI and `upgrade_blueprint_stealing` cost/effect block were not modified.

After a future MD interface sync, run `python tools/md_update_203/fix_agency_repetition_frames.py --repair`, then `python tools/md_update_203/fix_agency_repetition_frames.py --check`. The check-only default rejects frame count 2 and scans all project GUI files for unexpected references. A temporary copy of the current MD donor GFX passed the 2-to-3 repair, second-run no-op and check sequence. Current validation also confirms the 96 by 32 DDS, one GUI reference, and unchanged native geometry for the popup, branch entry, upgrade card and repetition icon.

The green-dot source is repaired, but live UI rendering remains unverified because computer-use access was denied.
