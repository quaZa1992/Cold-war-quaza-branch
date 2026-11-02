IMPERIA COLD WAR

# France 1970 party revision layout review

## Inputs and result

The review covers the compiled French national focus tree after the approved party revision and current balance overlay. Approved snapshot SHA-256: `5159aaad0f0b13bbf3ef38e2d374be05fcb907a5df6386c8b2e933520b278419`. Compiled runtime design SHA-256: `d7298667caf36d1e0e3a1493fefe77ac270c85c39da8ff61e489afae94b451c7`. Current compile manifest SHA-256: `d953d828cf1fce04a0fa9a9d963f9b80898ef40cffb0e44005a26f255bd03403`. English localisation now has 1,013 keys (`4b4c6ce2fdb17353f438267f8a7efa7a3d7cc246498bd0e3048c180652a6a9fb` for the emitted file). The current inline preview is `C:\Users\Enes\.codex\visualizations\2026\10\28\01a183df-ceae-74b3-b1f4-d519f043ee74\france-cold-war.html` (SHA-256 `0b434dab9c9326a9af3e8c50d4ad2e1a1dde3dc469164423b41999199bb171d8`, 999321 bytes, below the 1,000,000-byte limit).

The emitted tree contains 156 focuses across 14 sections and 35 recipient-approved offers. Its footprint is x=4..103, y=0..13. It has 142 prerequisite groups, 183 prerequisite edges and 47 mutually exclusive pairs.

## Geometry and native presentation

The local preview uses the emitted coordinates and anchors on a 96 by 130 pixel stride, with 165 by 128 pixel focus hitboxes, 164 by 50 native titlebars and a 147 pixel label-width target. Static checks found no duplicate coordinates, same-row focus-card collisions or prerequisite connectors crossing unrelated focus hitboxes. The preview renders all 156 focus nodes, including party branches while another party is selected in the government control.

Browser QA covered all 14 section views at widths 320, 736 and 1024 pixels: 42 fit views, zero clipped focuses, zero title overflows, zero broken images and no script errors. Pan, zoom and the native-scale control work. All 35 offer inspectors show both parties and the full concrete effects rows; bilateral peace, sanctions and state/province ownership, control and native building-level capacity requirements are visible.

The preview uses 36 focus textures from emitted aliases plus the current MD native focus titlebars. DDS images were converted to lossless PNG without scaling.

## Scope limits

This is an independent static geometry and browser-presentation review of emitted data, not a game engine test. The title-width measurement uses Arial 15px in Chromium and approximates the game font. The preview does not establish that the tree has been loaded or clicked inside HOI4.

## Final compile refresh

The final compile changed the manifest and raised the localisation count from 1,011 to 1,013. The focus preview fragment is byte-identical to the previously reviewed version (`0b434dab9c9326a9af3e8c50d4ad2e1a1dde3dc469164423b41999199bb171d8`), and `runtime_design.json` retains the same SHA-256. The compiler now uses a native temporary variable in the GDP helper and fixes the FN send acceptance-date guard. Those code-path changes are not represented in the focus inspector. The corrected acceptance-date guard changes eligibility for the recipient’s acceptance decision and still requires engine-level validation. The earlier browser QA remains applicable because the preview payload is unchanged.

A fresh screenshot of Shared Components shows the current -5% Equipment Cost Multiplier and -8% Production Efficiency Growth effects: `screenshots/france-shared-components.png`.
