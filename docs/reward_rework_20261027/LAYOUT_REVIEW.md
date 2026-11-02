IMPERIA COLD WAR

# Three-tree layout preservation review

Date: 27 October 2026  
Scope: read-only comparison of the installed NKO, KOR and JAP focus-tree source files against the frozen pre-reward runtime copies at `E:/HOI4_Mod_Tools/mdcoldwar/runtime/reward_rework_20261027/before/common/national_focus/`. The native probe was still running during this review.

## Source comparison

I parsed both the frozen focus-tree files and current installed files and compared each focus's ID, local `x` and `y`, relative anchor, focus cost, icon, every separate prerequisite block with its inner OR group, and every mutual-exclusion group. I also compared the tree ID, initial-show position, continuous-focus position, and every shortcut target and label.

| Tree | Frozen/current focus count | IDs added or missing | Graph-field differences | Root presentation differences |
|---|---:|---:|---:|---:|
| NKO | 360 / 360 | 0 | 0 | 0 |
| KOR | 300 / 300 | 0 | 0 | 0 |
| JAP | 425 / 425 | 0 | 0 | 0 |
| **Total** | **1,085 / 1,085** | **0** | **0** | **0** |

The comparison used the frozen runtime focus files, rather than relying only on `GRAPH_BEFORE.json`, because parsing the native source preserves the grouping of multiple prerequisite blocks. No focus geometry, predecessor grouping, exclusions, icon, focus duration, initial camera, continuous-focus position, or shortcut was changed by the installed reward integration.

## Native presentation and labels

All three trees remain in their existing native Millennium Dawn focus-tree source files. The reward overlays do not add focus nodes or change any focus label, so they introduce no new focus-card title widths or focus-count-driven layout changes. KOR's existing 300-focus presentation retains its prior shortcut targets and initial camera. NKO retains 360 focus nodes and Japan retains 425.

Native MD source geometry and rendered in-game appearance are separate checks. This review establishes source-field equality only. It does not claim a game screenshot, UI hover-wrap result, engine launch, or native multiplayer layout pass; the independent native probe was still in progress.
