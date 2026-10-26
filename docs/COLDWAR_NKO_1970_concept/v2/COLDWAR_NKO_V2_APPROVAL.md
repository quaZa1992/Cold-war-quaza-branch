# COLDWAR — North Korea: revision 2 for approval

**189 focuses · 14 sections · 29 mutually exclusive choice groups · six starting national spirits.**

This is the revised design and visualization. No focus tree, history, event, decision, spirit, game localization or economy script has been installed or changed by this work. Implementation waits for the user's approval.

- [Full spatial overview](COLDWAR_NKO_1970_overview.png)
- [Every focus, modifier, GDP price, agreement and historical precedent](COLDWAR_NKO_V2_REVIEW.md)
- [Canonical positions and structured effects](COLDWAR_NKO_v2_design.json)
- [Foreign Diplomacy](branch_foreign.png), [patrons and the Korean war route](branch_diplomacy.png), [Kim Jong Il's leadership](branch_jongil.png)
- [Global news preview](COLDWAR_NKO_1994_news_preview.png)
- [Color-restored funeral image](assets/COLDWAR_NKO_1994_funeral_colorized.png), [source, restoration prompt and built-in tool report](assets/IMAGE_PROVENANCE.md)

The interactive preview's Section selector opens readable individual branches. Select a focus to inspect its narrative, requirements, costs and effects. Bilateral offer focuses show both countries' packages, the recipient's decisions and the shared suspension of spirits and weekly contributions. Government and leadership selections show the conditional programmes; Starting spirits and World news open their respective previews.

## Changes to approve

All new cash costs derive from GDP. Each party pays its own GDP-based setup quote only on acceptance; ongoing contributions are weekly, calculated from current GDP. A machinery loan records its original cash principal, spends the proceeds once and removes its risk premium after full repayment.

Every building level grants one extra building slot in the same selected state. The ten building reward records include nine focus rewards and one accepted Soviet cooperation project. Ownership, control, coastline and building-level caps remain real requirements.

Artillery programmes improve Artillery Attack, with a separate registered MD modifier for rocket artillery. Militia, mechanized infantry, special forces, air defence and coastal programmes likewise use relevant MD effects.

Foreign Diplomacy adds five new partner programmes. Across all sections there are nine base bilateral agreements with eight partner countries, plus nine recipient-approved upgrade offers. Signed spirits have no expiry or party requirement. Mutual war or any direct diplomatic, financial, economic or military sanction in either direction suspends both copies and their weekly fees. Restoration never repeats a building, cash or research grant. Declined or expired offers may be resubmitted through sender decisions.

The Korean policy fork offers peaceful exchange, armistice pressure or armed reunification. The military route awards a war goal against South Korea. The player chooses whether to declare war.

Kim Il Sung's death on 8 July 1994 creates one global news event. Kim Jong Il takes over only if the Kim regime is incumbent; alternative governments remain. A compact subsequent branch offers party-led consolidation or a stronger cabinet. The photograph depicts the funeral later in July and is labeled as an AI color restoration.

## Verification

- [Independent layout and English localization review](final_v2_layout_review.md): all 189 titles fit the native 147 px field; no checked card or simulated connector collisions.
- [Independent mechanics review](final_v2_mechanics_review.md): GDP pricing, building-slot pairs, specialist military modifiers, bilateral lifecycle and leadership guards checked against MD/Imperia sources.
- [Independent historical review](final_v2_history_review.md): 1970 conditions, party distinctions, diplomatic precedents and succession reviewed. Its starting-spirit terminology correction has been applied.
- [Structural validation](structural_validation_v2.json): 189 nodes, 212 prerequisite edges, 33 reciprocal exclusion pairs, no structural errors.

The previews use native MD artwork and measured card/grid geometry. JavaScript syntax and static renders were checked. Browser and HOI4 runtime behavior, multiplayer balancing and save/load reconciliation remain implementation checks after approval.
