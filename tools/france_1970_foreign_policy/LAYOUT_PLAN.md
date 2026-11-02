IMPERIA COLD WAR

# France foreign policy expansion: layout and concept review

## Scope and sources

This is a layout-only proposal for the next France foreign-policy extension. It preserves all 176 existing IDs, positions, grouped prerequisites, exclusions and offer terms. No runtime or generator files were changed. The current runtime tree is SHA-256 `57b479c47dafef3d83917931994617bf08c1467d8a00175aa28da957a7518628`.

The installed shared foreign-policy entry is `diplomatic_review` at (78,8), followed by `community_entry` at (78,11). Existing partnerships and regional focuses remain in place: `algeria_energy` (84,9), `algeria_training` (84,10), `senegal_civil` (88,10), `senegal_defence` (92,10), and `community_entry` (78,11). Their emitted source blocks are in [COLDWAR_FRA2_1970_focus.txt](../../common/national_focus/COLDWAR_FRA2_1970_focus.txt:5653), including `community_entry` at line 6270. These existing offers must not be duplicated.

Native reference checkout: Workshop 2777392649, installed but separately versioned build identifier unknown. France `05_france.txt` SHA-256 `b42f3b83177902c99d4eb860831674cc5d2c2318155eba2306ae4a5ed8f0d3ae`; Russia `05_russia.txt` SHA-256 `db03d72e1fdbc239076eba9f7e9259e1791e909eab425186304cd6b14858b602`. France has 381 focuses in four sections; its Francosphere branch has 40 focuses and begins at `(146,0)`. Examples include `FRA_francosphere` at line 17477, `FRA_the_levant_problem` at 17542, `FRA_intervention_in_africa` at 18414, and `FRA_francafrique` at 19095. The Francosphere layout gives a single stable entry, close alternatives, and deeper regional paths. Russia has 806 focuses, six roots and a resolved x=0..235/y=0..26 span; its long foreign-policy branches use distinct side footprints, showing that visual clusters can remain separate while sharing a host tree. See `tools/france_1970_design/donor_profile.json` for the full read-only measurements.

Main MD's repeated relative y increment is one grid row. The current France runtime bounds are x=4..103, y=0..13. The native card geometry is 165 x 128 px with a 96 x 130 px grid stride; alternatives should therefore retain at least two x units between cards, and preferably four for separate offer choices. The proposal stays inside the present x bounds and adds height below the existing tree.

## Proposed footprint

Keep the funded `Foreign Trade` entry at `(94,9)`, requiring `diplomatic_review` at `(78,8)`. Its connector ends above the Jaguar/Atlantic Training exclusion bar on row 9. Put the four chapter entries in a compact 2x2 tile around the existing diplomacy area. The two upper chapters start at row 14; the two lower chapters start at row 19:

| Chapter | Entry | Pair columns | Offer rows |
|---|---:|---|---|
| Africa Networks | (68,14) | (64,66) and (70,72) | y=15,17 |
| Arab Contracts and Mediterranean | (88,14) | (84,86) and (90,92) | y=15,17 |
| Africa Security and Development | (68,19) | (64,66) and (70,72) | y=20,22 |
| Global Technical Partnerships | (88,19) | (84,86) and (90,92) | y=20,22 |

Each offer row has four focus cards: two adjacent mutually exclusive pairs. The pair columns are two grid units apart; the two pairs sit on either side of the chapter centre. Each chapter has two offer rows and eight agreements.

Each chapter has eight distinct recipient-approved offer focuses: two mutually exclusive pairs on each listed row. Preserve every proposal prerequisite group and do not make one signed agreement a prerequisite for an unrelated offer. The current 35 offers remain unchanged.

The planned total remains 37 new focuses: one funded entry, four chapter entries, and 32 offer focuses forming 16 new exclusive pairs. That gives 213 total focuses and 67 recipient-approved agreements. New coordinates span x=64..94 and y=9..22; whole-tree bounds become x=4..103 and y=0..22. Four native shortcuts to the chapter entries will make the lower tree navigable from the current opening viewport; retain the Partnerships by Consent shortcut to the common diplomatic root. The existing focus groups remain visible under every government.

## Connector and collision review

The direct `diplomatic_review` to `(94,9)` route ends above the Jaguar/Atlantic Training exclusion bar at row 9. The outer x=94 spine remains 27 px from the right edge of existing `senegal_defence` at x=92,y=10. New chapter cards stay below the old tree's row-13 card bounds. Entry connectors meet the two upper chapters at the top of row 14 and the lower pair at row 19. The lower bus is below the top tiles' final row-17 cards, leaving 132 px before lower entry cards begin.

Within each chapter, the centre stem falls between the two offer pairs. The 165 px native card width leaves a 27 px gap inside each two-grid-unit mutual-exclusion pair; the pair-to-pair centre gap is eight grid units. Offer rows are two rows apart, leaving 132 px between their card bounds. All four groups stay around x=64..92 instead of stretching across the full tree. Static geometry simulation found no card overlaps, connector-card hits, connector crossings, or exclusion-bar crossings; final browser preview and in-game rendering remain pending the regenerated design and installation.

## Layout decisions still tied to content

- Preserve the shared foreign-service gate, then let the four chapter entries express distinct policy programmes. Do not create the same four deals under each party.
- Place recipient-approved bilateral terms directly on their offer focuses. Keep the two offers in each pair inspectable together and make only their actual alternative choices mutually exclusive.
- Keep later precedents gated by their verified dates and political conditions. Layout does not authorize a 1970 start to receive later agreements as completed facts.
- The 2x2 chapter tiles are a geometry proposal. If research changes offer grouping or prerequisite logic, keep chapters distinct and use only lanes that preserve prerequisite meaning and clear existing choices.

## Current concept preview

The current source design is SHA-256 `7bd27bfa457cda2c8443a4252150ed806396a5cc7adb4353a3e5ddaad0f3785f`. The pre-install concept preview opens on the African Networks tile at normal fit scale, with the Niger Concession inspector selected. Its optional Foreign Policy Area view shows the 37 new focuses; the full 213-focus tree remains available as another view. Browser QA passed 57 fit views at widths 320, 736 and 1024 px, with zero native-title-width overflows and zero geometry collisions. The exact checks and hashes are in [PREVIEW_QA.json](PREVIEW_QA.json); the Africa, Arab and complete-area screenshots are in `screenshots/`.

This remains a browser preview using current registered MD textures and an orthogonal connector approximation. It is not an emitted game build or HOI4 screenshot; native engine rendering remains pending installation and in-game inspection.

## Unverified

The concept data records the 37 new IDs, chapters, offer partners, rewards, costs and historical references; this file remains a geometry review. No game UI or native connector render was available for this planning pass.
