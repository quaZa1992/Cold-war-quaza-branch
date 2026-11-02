IMPERIA COLD WAR — Greece 1970 Replacement Tree Native MD Reference

# Scope

Concept-only layout research for a proposed 100-focus Greece tree. The native reference files were sampled directly from the local Millennium Dawn checkout. No loaded Greece, shared-focus, GUI, generator, localization, or runtime file was changed. The report does not make historical claims about Greece or validate the proposed policy content.

# Reference snapshot

- Main MD root: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`.
- `common/national_focus/05_israel.txt`: 667 focus blocks, SHA-256 `be0d4bc91e52fa877443826f4d9d8d5d2e007f614f7ed5b54d5d9db4de9da91c`.
- `common/national_focus/05_russia.txt`: 806 focus blocks, SHA-256 `db03d72e1fdbc239076eba9f7e9259e1791e909eab425186304cd6b14858b602`.
- `interface/nationalfocusview.gui`: SHA-256 `5ea0ab2ae2115fc2e146043031dd08b72a603aace2ed66060d701f1296dbb53d`.
- Local Greece tree: `common/national_focus/COLDWAR_GRE_1970_focus.txt`, 293 current focus blocks. There are nine separately imported Greek guarantor focus nodes; keep their host integration stable.

# What native geometry shows

The focus GUI defines a **96 by 130 pixel** `focus_spacing` pitch and a **165 by 128 pixel** `national_focus_item` window (`nationalfocusview.gui:536-539, 663-669`). The focus title starts at `(15,58)` in `hoi_16mbs` (`:577-580`). Connectors use `link_spacing=(16,16)`, `link_begin=(80,64)`, and `link_end=(80,0)` (`:671-685`). The item-window size is an outer GUI window measure; spacing alone does not guarantee that icons, names, glows, or connector segments read cleanly.

Measured reference examples (all grid positions resolved from the emitted relative offsets):

- Israel uses a root at `(95,0)` (`05_israel.txt:47-52`), then a separated first-level policy root at `(125,1)` from relative `(30,1)` (`:66-76`). A later stable anchor at `(140,2)` fans into a one-step spine and a tight three-way alternative at `x=138,140,142`, row 4 (`:117-127, 445-455, 482-493, 522-533, 562-573`). This shows both wide sector spacing and compact, deliberate choice spacing in one native tree.
- Russia 2000 places the main root at `(62,0)` (`05_russia.txt:51-56`), a political-policy branch at `(75,1)` (`:81-91, 108-118`), and a policy spine at `(75,2)` (`:155-165`). Two early arms at `(74,4)` and `(76,4)` rejoin at `(75,5)` with separate prerequisites (`:319-329, 351-362, 388-399`). Three competing economic models sit on the same row at `(74,8)`, `(76,8)`, `(78,8)` (`:552-564, 600-612, 649-661`).
- The examples show small ±1/±2 fans for local alternatives, straight single-column spines, and enough separation for separate sections. Larger offsets are used where branches form their own major areas; they should not be copied just to imitate a large country.

# 100-focus geometry proposal

Use a compact planning envelope of about **28 columns by 21 rows**, with five visibly separate political roots and a few shared domains. The coordinate envelope is an initial sketch rather than an engine constraint; actual titles, icons, prerequisites and native routing can expand it.

| Zone | Proposed roots (grid) | Rows | Composition |
|---|---:|---:|---|
| Shared constitutional opening | `(12,0)` | 0-3 | One short common spine with the necessary constitutional fork. Avoid adding a positioning-only focus. |
| Shared policy pillars | `(0,5)`, `(8,5)`, `(16,5)`, `(24,5)` | 5-8 | Parallel institutions, diplomacy, economy, and armed forces; avoid unnecessary cross-locking between domains. |
| Political routes | `(0,10)`, `(6,10)`, `(12,10)`, `(18,10)`, `(24,10)` | 10-17 | Independent centrist, right, social-democratic, left, and junta/monarchy routes. Keep every party route visible; show actual party requirements natively and gate execution/rewards. |
| Shared conclusion | `(12,18)` | 18-20 | Place only true shared joins or late common choices here. |

Prefer relative child offsets in the `-2..+2` range and one-row vertical progression for short local branches. A wider row is appropriate for the five route anchors or an explicit multi-way choice. Declare all absolute roots before any relative descendants: the engine can reject a relative anchor declared later even when its resolved coordinates are mathematically correct. Preserve prerequisites as grouped logic: blocks are AND; multiple `focus` fields within one block are OR. Do not convert real prerequisites into visual-only connectors.

# Existing Greek actor-module constraint

The generated Greek guarantor module has nine Greek focus nodes (`gre_officers`, `gre_treaty`, `gre_network`, `gre_consult`, `gre_withdraw`, `gre_coup`, `gre_response`, `gre_volunteers`, `gre_escalate`). `tools/cyprus_1970_rework/foreign_focuses.py:20-34` attaches them to `COLDWAR_GRE_1970_focus` around existing `COLDWAR_GRE_1970_foreign_0` at `(224,0)`, with module base `(264,0)`. The current tree has 293 focus blocks before those imported nodes. Keep this module and its coordinates stable under this concept-only pass, reserve its full footprint, and verify its actual connector/prerequisite interaction after a proposed replacement tree is emitted. The compact sketch ends well to the left of that anchor, so a future implementation may need either deliberate continuity/navigation or a separately approved rebase; this profile does not move it.

# Reward and style cues

- Political decisions use native party triggers and modifier interfaces. `SOV_putin` combines a visible party availability check, modifier/PP changes, and a relative party popularity adjustment (`05_russia.txt:122-145`).
- Economic programmes use native named spirits, treasury transaction helpers, and decision unlock tooltips (`SOV_stabilisation_fund`, `:297-305`).
- Military/research rewards can be direct and legible: the nuclear-plant focus gives one reactor and a single-use 50% research bonus (`SOV_gen_3_nuclear_plants`, `:499-508`). Israel’s personnel focus spends command power and treasury while swapping a named idea (`ISR_extend_standing_period`, `05_israel.txt:27061-27069`).
- Diplomatic offers place the named recipient event and a full numeric `If They Accept` tooltip in the focus reward preview, then apply bilateral influence/opinion effects (`ISR_befriend_south_africa`, `05_israel.txt:301-323`).
- Building rewards are shown through real construction effects/helpers; inspect the full state, slot and ownership semantics before using any example. Israel’s Tel Aviv focus calls its state construction helper and adjusts business opinion (`ISR_tel_aviv_priority`, `05_israel.txt:28117-28121`).
- Focus costs are explicitly authored per node where needed: e.g. 5 for `ISR_extend_standing_period` (`05_israel.txt:27053`) and 9 for `ISR_tel_aviv_priority` (`:28106`). These are examples only, not a new Greece-wide duration rule.

# Neutral icon candidates

`MD_REFERENCE_PROFILE.json` includes 35 candidate texture records with dimensions and hashes from the existing local native-icon catalogue. The contact sheet at [native-icon-candidates.png](native-icon-candidates.png) was generated from the resolved source textures and visually inspected; the earlier Cyprus card sheet was also reviewed as a cross-check. The shortlist favors neutral parliamentary, civil-service, negotiation, production, infrastructure, and military imagery, not country flags or portraits. It excludes Cyprus-specific custom emblems. Re-open the full-resolution texture and verify its registered sprite/shine pair before any implementation; local credit and permission metadata are unknown.

# Limits

This is a native-source layout profile, not an emitted-tree layout audit. No new Greece concept JSON, focus coordinates, connector render, localization, or engine-loaded tree was reviewed. The coordinate envelope and icon picks are proposals, not approval to replace the tree.

See `MD_REFERENCE_PROFILE.json` for the complete source hashes, sampled coordinates, GUI measurements, icon texture IDs and file hashes.
