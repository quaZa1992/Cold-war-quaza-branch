# KOR 1970 concept graph — final preview review

## Scope and current artifact set

Reviewed the current 206-focus, 13-group `COLDWAR_KOR_design.json` (SHA-256 `57ECA6801E65786484E1790051433D901D69A733B328261039F1A7C5DA844ED0`) and the rebuilt normal-scale detail images for DRP, Two Kims, North Korea, and KJP, plus the current entire-tree overview and art contact sheet. All six preview files below were generated on 2026-10-24 at 18:52; these are the files inspected in this pass. No source or game files were changed.

- `COLDWAR_KOR_DRP_detail.png` — 266,752 bytes; SHA-256 `53540B63D67C52F29BC87AF1D91C67241FC07032C0EB221E6A35396257C77686`
- `COLDWAR_KOR_Two_Kims_detail.png` — 161,884 bytes; SHA-256 `7DC78522012C2B741195B3948093D401067109D0AC15577819188382AC227E06`
- `COLDWAR_KOR_North_Korea_detail.png` — 192,879 bytes; SHA-256 `3BCDDE9F440B946296FF5D99C2416B5AA8A4E06A2A11C89322666D0643EC2C1C`
- `COLDWAR_KOR_Kim_Jong_pil_detail.png` — 152,716 bytes; SHA-256 `08892E88093FFC4D351018994304AF49F8FC42872D289880809424AF8DD8F654`
- `COLDWAR_KOR_entire_tree.png` — 635,607 bytes; SHA-256 `15DA75F8F3698A9B4CE713DC1CA1A77F6DF62BE2B9BEEB8BD6109274C8D7CD4F`
- `COLDWAR_KOR_art_contact_sheet.png` — 330,536 bytes; SHA-256 `8D5647B39B30AED2443F7246E5069F19A080E1B1AF616FB80EFBACA462651F10`

The PNGs identify themselves as concept previews: native grid/art are used, but font, symbol placement, and connector routing approximate the engine.

## Geometry and graph checks

The current JSON contains 206 focus nodes in 13 groups and exactly 8 shortcut targets. Independent static checks found 0 bad anchor offsets, missing prerequisite or exclusion references, nonreciprocal exclusions, duplicate grid cells, or card-box intersections at the matching native GUI dimensions. All 206 foci are structurally reachable using OR within one prerequisite block and AND across multiple blocks; the design has no cross-group prerequisite edges. This does not establish party/leader gate satisfiability in a live scenario.

The graph occupies x=3..73 and y=0..25. With focus spacing 96x130 and card size 165x128, its nominal outer card bounds are about 6,885x3,378px before artwork/connector extents. Compact fork arms are two grid columns apart (192px): cards leave about 27px between edges, and 147px name fields leave 45px. The DRP, Two Kims, North Korea, and KJP details show these gaps clearly. The added KJP programme at `(45,18)` is collision-free and now has its own normal-scale detail image.

The orange mutually exclusive connectors now stop in the open gap between endpoint cards in all four inspected details. The previous preview issue where they ran through icon centers is not present in these current files. Gray prerequisite fan/merge connectors do not visibly cross unrelated cards in these branches; the Two Kims merge spans a wide empty area but routes cleanly into the central join.

All visible node names fit the preview's configured 147x20 field in the four detail images. Prior ellipses are gone from examples such as Yushin Constitution, Civilian Conservatism, Kim Young-sam, Kim Dae-jung, Sovereign Confederation, and their continuations. The section captions also fit inside the detail canvases now.

## Current art and remaining styling observations

The current contact sheet contains distinct topic families for constitutional/state administration, parliament, labour, student politics, revolutionary politics, intelligence, industry, roads, research, nuclear power, elections, welfare, policing, cooperation, housing, and energy. The previous modern NIS-style badge and skeleton-like revolution art are absent. The full overview reads as distinct thematic routes, and the DRP/economy/defence/KJP icon choices mostly reinforce their policy subjects.

Some repeated symbols remain in the branch details: the Two Kims' Kim Young-sam finance route reuses the chart/cube symbol across several choices, and the Korea branch uses the peninsula map throughout its Korean-question spine. These are not layout collisions; they are recognizable thematic reuse. The contact sheet and normal-scale details show no sprites touching adjacent focus cards or labels.

Navigation now fits the native GUI shortcut grid's eight vertical slots (`interface/nationalfocusview.gui:370-384`), and the initial show position targets `COLDWAR_KOR_developmental_state`. The eight shortcuts go to DRP, NDP, Two Kims, Army/DJP, national development, defence, foreign policy, and the Korean question. USP, Students/independent Marxists, RPR, KCIA, and KJP do not receive shortcuts, so those lower/alternate routes still require panning from the camera or another destination; this is a deliberate capacity tradeoff to decide, not overflow.

## Verification limits

This pass verifies the current PNGs and static geometry only. Actual HOI4 title fonts and clipping, focus-icon alignment, shortcut interaction, initial viewport behavior, and Clausewitz's native connector routing remain unverified in game. The current screenshots make no visible card/art collisions, but the renderer still labels its connector paths approximate, so engine routing should be checked before claiming exact native presentation.

## Native comparison

The 192px fork separation matches donor South Korea's measured `KOR_p8_poseidon` / `KOR_c295` spacing. Target focus card and text bounds are defined in `interface/nationalfocusview.gui:446-493,573-585`; current donor and target GUI/GFX geometry is recorded in `md_reference_layout.md`. Russia's native tree demonstrates an initial camera plus section shortcuts (`common/national_focus/05_russia.txt:10-49`); the current concept now provides both within the target GUI's eight-slot shortcut limit.

