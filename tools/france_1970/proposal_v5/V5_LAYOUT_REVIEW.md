IMPERIA COLD WAR

# V5 layout review

## Scope and reference

Review of latest `proposal_v5/proposal.json` (260 nodes, 13 groups, 50 offers), `preview_template.html`, and final images `v5-gaullist-foreign.png` and `v5-national-all.png`. I read the `mdcw-tree-layout` skill and `layout-method.md`; geometry was compared to installed MD's `common/national_focus/00_generic.txt` and `05_russia.txt` conventions. This is a browser-rendered proposal; native HOI4 connectors and loaded focus routing are still untested.

## Structural checks

- All 260 node IDs are unique; no duplicate `(x,y)` coordinates were found. All 50 offer nodes are included in those 260 nodes.
- All relative anchors, prerequisite IDs, and exclusion IDs resolve. Exclusion pairs are reciprocal. A static prerequisite walk from the 13 group entries reaches all nodes, interpreting each inner prerequisite array as an OR group and separate arrays as AND groups. This establishes graph reachability only; exact-party gates and game-level satisfaction remain engine checks.
- The party columns retain a 30-grid stride and overall x span 2–372. At 1024 px, the supplied renders show no card-to-card overlap in the viewed Gaullist foreign branch or National full group; long offer titles wrap to three lines and remain legible. The 13-column tree is panoramic, but latest layout metadata now includes an opening camera at `COLDWAR_FRA_progress_contracts` and shortcuts to all 13 group entries. These improve navigation in the proposal; native shortcut syntax and opening position still require game verification.
- The Gaullist foreign image exposes one genuine visual inefficiency: `COLDWAR_FRA_v5_gaullist_sov_05` sits at `[38,1]` and depends directly on `progress_contracts` at `[16,0]`. Its long horizontal connector spans nearly the full rendered canvas above the military branch. It misses other cards, so it is not a functional collision, but placing this shared diplomatic offer closer to its parent (while preserving the direct prerequisite) would shorten the line. Check for a non-overlapping slot before moving it.
- In `v5-national-all.png`, the lowest foreign-offer row is separated by a large empty vertical band from its parent bus; the long drops to the Romanian and German offers are visible but do not cross cards. Consider moving the low offer row upward if the country column permits. The visible political, military, and offer titles are legible at the supplied scale; no clipping is evident at the shown 1024-wide render.

## Connector and semantic risks

- **Armament OR buses are clear in the supplied preview.** The proposal now places personnel preparations and the OR-merge into the arms allocation deliberately; the visible line model uses a horizontal bus rather than the diagonal X I flagged in the earlier coordinate-only review. This resolves that visual concern in the preview. Keep the bus semantics and exclusion marks when translating to native focus prerequisites, then verify actual HOI4 routing.
- Alternative prerequisite groups remain important to preserve. Examples include `gaullist_renewal` after `industrial_participation` or `national_champions`, and `orderly_alternation` after `executive_programme_office` or `minority_constitutional_referral`. In the visualized tree, these OR joins read as shared routes rather than accidental double requirements.
- The updated military spine uses rows 1–4 and offers rows 1/4/6. The Gaullist foreign preview shows the two exclusive armament choices, follow-ups, and offers without card overlap; the National full preview shows the political branch and bilateral offers together, with no obvious title collision. The bottom offer bus does create the long drops noted above. PNG geometry is evidence for this renderer only, not proof of native line routing.

## Render checks still needed

The supplied browser preview has a 1024-wide normal-scale rendering and includes controls for fit/readable scale and navigation; the two requested full renders were checked visually. Root-reported browser checks cover all 260 nodes, 290 prerequisite edges, 100 spirit sides, and responsive widths 736/360 with no JavaScript errors or card overlap. I have not independently rerun that browser suite. The HTML uses its own connector renderer, so native HOI4 path routing, in-game camera behavior, exact shortcut integration and all-pairs full-tree overlap remain unverified. Before installation, check the long Gaullist root-to-Soviet connector and bottom offer drops in the native focus screen.
