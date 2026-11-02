IMPERIA COLD WAR

# Brazil 1970 emitted art reference review

The generated Brazil focus, idea, and event references all resolve to existing sprites and image files in the current mod checkout.

| Reference set | Emitted references | Unique keys | Result |
| --- | ---: | ---: | --- |
| National focus icons | 224 | 23 | Every `COLDWAR_BRA_focus_<key>` alias and matching `_shine` alias resolves to an existing native goals texture. |
| Idea pictures | 203 | 26 | All 8 starting spirit pictures and 18 focus group pictures resolve through the standard `GFX_idea_` sprite prefix to 128 x 128 DDS assets. |
| Event pictures | 22 | 9 | Eight Brazil event pictures and the shared agreement notice resolve to native framed images. All are 217 x 163 and byte-identical to their declared donors. |

The detailed report records every source file and line number, picture key, resolved sprite, texture path, image dimensions, and asset SHA-256 in [ART_IMPLEMENTATION_REVIEW.json](ART_IMPLEMENTATION_REVIEW.json). Its source design hash is recorded there as well.

## Native event window comparison

The full `EventWindow` block in `interface/eventwindow.gui` matches the Millennium Dawn workshop donor byte-for-byte. The matching block hash is `ee2b21507195b64455534d95835ee85d6f615f8a67b187d99aacece4f9d00a99`. This block contains the existing picture placement, clip, and the adjacent option grid. The separate `EventWindow_News` block has project changes, but the country event window and its options were not changed.

The inspected country event window is 581 x 427. The lower container begins at y=221 and is 581 x 206. The picture is placed at local x=5, y=5 and displays the existing 217 x 163 framed donor art; the photo aperture is 180 x 150 at x=19, y=6. The picture clip is at local x=-3, y=35. The adjacent option grid is at x=215, y=-1, size 300 x 30, with 300 x 47 option slots and one column. Its block is identical to the upstream MD donor.

No missing aliases or missing image files were found. This is a static reference and pixel-source audit, not a live-game screenshot or in-engine rendering test.
