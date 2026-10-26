# Focus-tree layout audit: MD 2000 Russia vs. COLDWAR_SOV_1970

Inputs: `05_russia.txt` (MD, 806 foci, `russia_focus`) and `COLDWAR_SOV_1970_focus.txt` (ours, 836 foci, 50 sections from `cw_layout`).
Scripts (all in `/home/claude/audit/`): `pdx.py` (brace-matched parser, `#` comments stripped, `relative_position_id` chains resolved), `md_load.py`/`md_analyze.py` (MD branches and statistics, output `md_stats.json`), `cw_load.py`/`cw_analyze.py` (our tree, output `cw_stats.json`), `render.py` (PNG maps), `plan_layout.py` (the new layout, output `layout_plan.json` and `plan_positions.json`).
Maps: `md_russia_layout.png`, `sov_current_layout.png`, and `sov_proposed_layout.png` (the plan below, drawn the same way).
Grid assumption: 1 x unit = 96 px and 1 y unit = 130 px (HOI4 focus spacing). The maps are drawn at that pixel aspect.

---

## 1. MD Russia structure

How branches were found. A branch is either a top-level root at y=0 or a child of the trunk root `SOV_reign_of_yeltsin`, plus everything below it. Each focus is assigned through its nearest-in-x prerequisite. Foci without a prerequisite are assigned through `relative_position_id`. The result matches the `#Start of ...` comment headers and the per-party `search_filters`. Placement: **all independent roots are at y=0, and everything is side by side. No branch is ever stacked below another branch.**

| # (left to right) | Branch root | English name | foci | x | y | rows | sibling gap (mode) | mutually exclusive pairs (all on one row / dx) | filter | main costs |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SOV_zyuganov | Gennadiy Zyuganov (CPRF) | 67 | 0-17 | 1-16 | 16 | 2 | 5 (dx 3,4,6) | RUSSIA_CPRF | 3 (48), 2 (11) |
| 2 | SOV_path_of_western | Path of Westernism (liberal parties) | 105 | 16-54 | 1-15 | 15 | 2 | 8 (dx 2,4,6,8) | RUSSIA_JUST/YABLO/SPS/PARNAS | 7 (68), 5 (23) |
| 3 | SOV_new_russia | New Russia | 44 | 36-59 | 1-10 | 10 | 2 | 5 (dx 2,4,6) | RUSSIA_YABLO | 3 (24) |
| 4 | SOV_subjects | Subjects of the Federation | 8 | 58-67 | 1-3 | 3 | 2 | 3 (dx 2) | RUSSIA_SUBJECT | 4 |
| 5 | SOV_kob_party_start | Conceptual Party Unity (KOB; root without prerequisite, `allow_branch`) | 23 | 60-68 | 4-14 | 11 | 2 | 0 | RUSSIA_SHIZO | 5 |
| - | SOV_reign_of_yeltsin | The Reign of Boris Yeltsin (**trunk root**, cost 1) | 1 | 62 | 0 | 1 | - | - | RUSSIA_UNITED | 1 |
| 6 | SOV_putin | Vladimir Putin (United Russia) | 110 | 63-86 | 1-26 | 26 | 2 | 13 (dx 2,4,6) | RUSSIA_UNITED | 5 (68), 7 (28) |
| 7 | SOV_zhirinovsky | Vladimir Zhirinovsky (LDPR) | 117 | 83-119 | 1-14 | 14 | 2 | 6 (dx 2,4) | RUSSIA_LDPR | 3 (80), 2 (28) |
| 8 | SOV_nazbols | Russia Is Everything (Limonov) | 29 | 119-129 | 1-12 | 12 | 2 | 1 (dx 2) | RUSSIA_NAZBOLS | 3 (19) |
| 9 | SOV_economic_russian | The Russian Economy | 129 | 131-189 | 0-8 | 9 | 2 | 3 (dx 2,4) | RUSSIA_ECONOMY | 3 (56), 5 (47) |
| 10 | SOV_groznyy_offensive | Groznyy Offensive (military reform) | 86 | 183-203 | 0-18 | 19 | 2 | 0 | RUSSIA_ARMY | 3 (57), 5 (25) |
| 11 | SOV_safe_russia | Security of the Country (FSB/MVD) | 18 | 199-209 | 0-5 | 6 | 2 | 0 | RUSSIA_ARMY | 3 |
| 12 | SOV_slavic_corps | Solve the Issue with the Slavic Corps (PMC) | 9 | 210-214 | 0-4 | 5 | 2 | 0 | PMC_WAGNER | 2 |
| 13 | SOV_withdraw_from_the_sco | Withdraw from the SCO (foreign policy) | 60 | 215-235 | 0-8 | 9 | 2 | 6 (dx 2,4) | RUSSIA_JUST... | 7 (48) |

**Left-to-right order:** opposition parties (CPRF, liberals, New Russia), then Subjects and KOB, then the **trunk root**, then the ruling party (Putin), Zhirinovsky, Limonov, **economy**, **military** (reform, security services, PMC), and **foreign** policy at the far right. Politics takes x 0-129 (55% of the width, 504 foci = 63%). Economy takes 131-189, military 183-214 and foreign 215-235.

**Gaps between neighbouring branches.** In the same row, the nearest foci of two neighbouring branches are **2 columns** apart, the same as siblings (5 between economy and military). Bounding boxes interleave: Westernism and New Russia overlap by 18 columns, but on different rows. Branches are separated by their structure, not by empty space.

### 2. Political structure

- **One trunk, every party hangs from it.** Yeltsin (62,0) has 7 children at y=1, joined by one long bar: Zyuganov x10, Westernism 27, New Russia 49, Subjects 62, Putin 75, Zhirinovsky 93, Nazbols 122. The longest lines in the tree are these (dx up to 60, dy 1). Each party is a **column block directly under the trunk**: 18, 39, 24, 10, 24, 37 and 11 columns wide, 3 to 26 rows deep. No party block sits below another. KOB, a root gated by `allow_branch`, is tucked into the free gap between Subjects and Putin (rows 4-14).
- **Sub-parties are side by side under a shared hinge focus.** Westernism has trunk rows 1-5: Pragmatic and Idealism are mutually exclusive at dx 2, then Respect and Decommunize at dx 4. Then comes "Convention for a Democratic Russia" (row 5), with **4 party columns at row 6**: PARNAS 16-20 (5 wide), SPS 22-26 (5), Yabloko 28-41 (14, which splits into Navalny and Yavlinsky, mutually exclusive at dx 8) and A Just Russia 42-54 (13). Each column is 7-10 rows deep, with 2-column gaps between columns. Zhirinovsky has 4 sub-blocks at row 2: Bumaga 83-89, Arrest 90-97 and Coopt 96-98 (mutually exclusive, dx 4), and Irredentism 98-119.
- **Ruling party = one deep column next to the trunk.** Putin is 24 wide by 26 deep, a sequential story with mutually exclusive triples at rows 8 and 15.
- **Mutually exclusive choices are always on the same row and adjacent.** All 50 pairs are on the same row: dx 2 (25 pairs), 4 (14), 6 (6), 3/8/2.5/3.5 (5).
- **Economy is one wide fan.** One root (cost 3, placed +90 from Yeltsin with no prerequisite) has 17 children at y=1, spaced 2-3 (x 131-189), only 9 rows deep. The sector chains under it are 2-5 rows long.
- **Military is several roots side by side at y=0:** reform (a column 21 wide by 19 deep), security services (11 by 6) and PMC (5 by 5). Foreign policy is a dense grid (21 by 9, sibling gaps 2-3).

---

## 3. Conventions with numbers

| Item | MD Russia | COLDWAR_SOV (current) |
|---|---|---|
| Canvas | x 0-235, y 0-26 (**236 x 27**), 22,656 x 3,510 px, aspect 6.5:1 | 150 x 126 used (130 allotted), 14,400 x 16,900 px, aspect 0.85:1 |
| Fill (foci per grid cell) | 12.6% | 4.3% (32 rows completely empty) |
| Foci without a prerequisite | 12: 6 roots at y=0, KOB at y=4, 5 mid-tree foci gated by `available` | **50** (every section root; only the outlook tops have lines) |
| `relative_position_id` | 800/806 foci. Only the 6 top-level roots are absolute. 71 anchors (branch root for 261 foci, a direct prerequisite for 162). x offsets within +/-3 for 73%. Party leaders are relative to Yeltsin (-52, -35, -13, +13, +31, +60) | 786/836. **50 absolute anchors** (one per section root). Offsets up to +/-20 |
| Sibling gap | 2 (mode in every branch), sometimes 3-4 | 2 (tidy tree, `2 focus units per column`) |
| Gap between branches/sections | 2 columns per row (5 between economy and military) | 4 extra columns (`SECGAP`) plus band centring, so 6 to 30+ columns of empty space |
| Prerequisite lines | 1,200 lines. dy=1 for 92%, dx <= 2 for 79%, dx >= 6 for 8.5%, max dx 60 (the trunk bar). 12 cross-branch. 100 OR groups | 983 lines. dy=1 for 94%, dx <= 2 for 73%, dx >= 6 for 9%, max dx 33. 9 cross-section (pol dir_ to outlooks, dy 4). 96 OR groups |
| Links that are only `available` (no line) | Party gating via `available` on 90% of foci, but every party still hangs from the trunk with a line | 49 links (party and General Secretary roots): **median dy 44 rows, max 58; median dx 24, max 67** |
| Lines that run through foci | 18 "below parent" (deliberate fan: child at dy 2, dx 1 beside a direct child), only 6 "above child" | 0 "below parent", **81 "above child"** |
| Mutually exclusive | 50 pairs, all on the same row, dx 2/4/6 | 124 pairs, all on the same row, dx 2 (69)/4 (32)/3 (13): same convention |
| Costs | 3 (39%), 5 (27%), 7 (21%), 2 (9%), 1 (2%). Top-level roots 1, party leader foci 2, military mostly 3, foreign mostly 7, deeper rows (8-11) shift to 7 | **5 for 70%**, 3 (18%), 7 (11%), 10 (5 foci) |
| `available` / `bypass` / `allow_branch` | 724 / 95 / 2 (KOB root, one military focus) | 584 / 1 / 0 |
| `ai_will_do` | `base = 1` plus modifiers for 82%. Start foci get large bases (Yeltsin 1000, security 1000, one military 2000) | `base = 3` plus `factor 0.1` if historical (63%), `base = 10` historical (30%), `base = 0` (6%) |
| `search_filters` | One custom filter per branch (RUSSIA_CPRF/UNITED/LDPR/NAZBOLS/YABLO/SPS/PARNAS/JUST/SHIZO/SUBJECT/ECONOMY/ARMY, PMC_WAGNER), plus INDUSTRY/EXPENDITURE as secondary tags | Generic only (POLITICAL 424, INTERNAL_FACTION 167, STABILITY 137, INFLUENCE 128, MILITARY_LAWS 108, ...) |
| Shortcuts | **6**: military root, economy root, and the 4 party leaders (Zhirinovsky, Putin, Zyuganov, Westernism) | **50** (one per section) |
| `initial_show_position` | `{ x = 2 y = 0 }` (left edge) | `{ focus = the_collective_leadership }` |
| `continuous_focus_position` | `{ x = 17000 y = 1000 }` px, about grid (177, 7.7): an empty pocket under the right half of the economy, 75% across the canvas | `{ x = 8544 y = 100 }`, about grid (89, 0.8), right of the pol root |

---

## 4. Problems in the COLDWAR_SOV layout

(See `sov_current_layout.png`. Pink dotted lines are the `available`-only logical links.)

1. **The canvas is turned on its side.** It is 150 by 126, made of 7 group bands stacked vertically (pol 0-14, CPSU and General Secretaries 15-49, parties 53-75, economy 79-91, military 95-101, state 106-111, foreign 116-125). MD is 236 by 27, with every domain root at y=0. 32 rows are completely empty, and the fill is 4.3% against MD's 12.6%.
2. **The domain trees are far from the start.** The player starts at pol (row 0) and has to scroll about **79 rows (10,300 px) down to reach the economy**, 95 rows to the military and 116 rows to foreign policy. In MD these are roots at y=0, one shortcut away to the right.
3. **Party trees sit 43-58 rows below their outlook.** The 18 party roots are in rows 53 and 66, while their outlook (`power_*` and `*_leading_role` foci) is in rows 8-10. The order does not follow the outlook either: na's parties are split between the right end of row 53 (gt, lnl, rd, fel) and the left of row 66 (fob, smc, usr). The links cross the whole canvas (dx up to 63). MD hangs every party block directly under the trunk, side by side.
4. **General Secretary trees are detached from the Politburo.** ple is a compact block 20 wide by 2 deep at rows 15-16. Its 10 candidacy foci sit up to 67 columns from their trees (ple_the_politburo to bre dx 67, ple_ust to ust dx 62, ple_gre to gre dx 49). The trees fill rows 22-49 in two centred rows (8 + 3), and the second row (gro, che, gor) floats in the middle.
5. **50 isolated roots.** Every section starts without a line. In MD, only the domain roots and KOB do.
6. **The dir_ to outlook bar is long and drops 4 rows.** It is a 67-column bar at y 4.5 (x 40-107) from 4 different parents, each line falling 4 rows (dy 4). In MD the long bar comes from one parent and has dy 1.
7. **The outlook bands are spread for nothing.** em, we, na and nt are centred over the whole 150-column width with large gaps. Their bottom part (`*_leading_role/democratic_union/...` root) stands unlined beside the lined top part.
8. **Band centring makes rows irregular.** For example, General Secretary row 1 spans x 0-149 while row 2 spans 54-95, party row 2 spans 35-114, and economy, military, state and foreign are each centred on their own. Sections that belong together (eco, agr, en, sci) are no closer to each other than unrelated ones.
9. **81 prerequisite lines drop through other foci on the child side.** These are tidy-tree artefacts in det (11), bre (9), eco (8), sus (5), army/pod/she (4) and others, for example `deepen_the_kosygin_reform` to `the_ninth_five_year_plan` passing through `enterprise_self_financing` and `legalise_the_cooperatives`. HOI4 bends the line just under the parent and drops at the child's x. MD's own layout follows that rule: it has 18 deliberate "below parent" fans but only 6 "above child" conflicts. `cw_layout.section_conflicts()` only reserves the parent column (VIRT), so this side is unchecked. This does not depend on section placement.
10. **50 shortcuts against MD's 6.** The shortcut bar becomes a list of every section.
11. **Smaller convention gaps** (not layout): 70% of foci cost 5 (MD spreads 3/5/7 by branch type). There are no per-branch search filters, and almost no `bypass`.

---

## 5. New layout plan (MD style)

Machine-readable form: `layout_plan.json`. It covers all 50 `cw_layout.ORDER` keys, the bounding boxes do not overlap (checked), and all 836 positions are unique. The generator is `plan_layout.py`. It derives every number from `cw_layout.LAY`, so it can be re-run when a section changes size. Per-focus result: `plan_positions.json`. Picture: `sov_proposed_layout.png`.

**Canvas: 372 x 31 grid units** (35,712 x 4,030 px, aspect 8.9:1, MD 6.5:1). Deepest row 30, so it stays within the 32-row target. Fill is 7.2%.

### Left-to-right order (blocks)
1. **Outlooks and party trees, x 0-119.** Groups from left to right: **nt | na | we | em**. Each outlook sits at rows 6-8, centred over its own party columns. The party trees form tier 1 from row 10 and tier 2 one free row below the deeper tree of tier 1.
2. **pol trunk** at x 88-103, rows 0-5, **mirrored** (local x becomes w-2-x) so the 4 dir_ foci sit on its left. It stands over the we|em boundary. dir_the_leading_role drops right into em (dx 3 and 8). The other three run left through the empty strip of rows 0-5 to we (dx 21-26), na (46-56) and nt (79-84). All 4 lines have dy 2. A search places pol so that no dir_ focus, and no pol focus in rows 3-5, stands in the column of an outlook focus.
3. **CPSU, Politburo and General Secretaries, x 126-223.** ple sits at rows 0-1, with ple_the_politburo directly above Brezhnev's root (same x 143, dy 3, so the design's line can be restored as a straight vertical). Tier 1 (row 3) is cpsu, bre, kos, pod, sus, she: the shared party tree plus the 1970 Politburo. Tier 2 (row 16) is and, gre, ust, gro, che, gor: the men who enter the Politburo between 1973 and 1980. em's party columns end at 119 and cpsu starts at 126, so em, CPSU and the Politburo are adjacent. This mirrors MD's trunk, then ruling party.
4. **Economy, x 230-265:** eco (row 0), then agr and en (row 13), then sci (row 19).
5. **Military, x 272-301:** army (row 0), then str and navy (row 8).
6. **State and Union, x 308-333:** union (row 0), then kgb (row 7), then soc (row 13).
7. **Foreign, x 340-371:** bloc and det (row 0), then chi and tw (row 11). bloc (Warsaw Pact and COMECON) is next to the military.

This is MD's sequence: opposition parties, then trunk, then ruling party, then economy, then military and security, then foreign. Politics takes 60% of the width for 68% of the foci (MD: 55% and 63%).

### Rules (numbers)
- Sections keep their tidy-tree layout and offsets. Only the anchor (`cw_layout.ANCHOR[key]`) moves, to origin plus its local position. The box is (x, y, w, h) with `w` from LAY, which already includes the 2-column right margin.
- Gaps: siblings 2 (unchanged); between sections of a tier, w plus 2 extra (nearest foci 4 apart); between outlook groups, 4 extra (6 apart); between blocks, 6 extra (8 apart); 1 free row between tiers.
- Every block root is at **row 0**, except the outlooks, which are at row 6 under the trunk. A block has at most 3 tiers, and each tier is centred in the block width. The deepest block is the political one, as with MD's Putin.
- Rows: pol 0-5, outlooks 6-8, party tier 1 from 10, party tier 2 from 20 or 21 (all end by row 30). ple 0-1, General Secretary tier 1 3-14, tier 2 16-28.
- Party and General Secretary roots stay gated by `available` with no lines. The link is now spatial: logical-link dy falls from a median of 44 to **4** (maximum 58 to 15), and dx from a median of 24 to **8**. The largest remaining dx is 78 (`ple_she` to `she`), because ple stays compact.
- No new line conflicts: the 9 cross-section lines are clear. The 81 internal "above child" conflicts remain until `section_conflicts()` also checks the child column.

### Section table (grid units; x_end and y_end inclusive, box includes the 2-column margin)

| block | key | section | foci | x | y | w x h | tier |
|---|---|---|---|---|---|---|---|
| 1 | pol | Die kollektive Führung | 14 | 88-103 | 0-5 | 16x6 | trunk (mirrored) |
| 1 | nt | Outlook: Nationalist | 11 | 3-16 | 6-8 | 14x3 | outlook |
| 1 | na | Outlook: Non-Aligned | 15 | 30-51 | 6-8 | 22x3 | outlook |
| 1 | we | Outlook: Western | 11 | 65-78 | 6-8 | 14x3 | outlook |
| 1 | em | Outlook: Emerging | 11 | 96-109 | 6-8 | 14x3 | outlook |
| 1 | rp | The Russian Party (20) | 13 | 1-10 | 10-18 | 10x9 | parties 1 |
| 1 | cnr | Committee of National Rebirth (21) | 7 | 13-18 | 10-14 | 6x5 | parties 1 |
| 1 | com | Council of Marshals (22) | 13 | 0-9 | 20-28 | 10x9 | parties 2 |
| 1 | rom | House of Romanov (23) | 10 | 12-19 | 20-26 | 8x7 | parties 2 |
| 1 | gt | Gosplan Technocracy (13) | 13 | 24-33 | 10-18 | 10x9 | parties 1 |
| 1 | lnl | Live Not by Lies (14) | 13 | 36-45 | 10-18 | 10x9 | parties 1 |
| 1 | rd | The Red Directors (15) | 13 | 48-57 | 10-18 | 10x9 | parties 1 |
| 1 | fel | Free Enterprise League (16) | 9 | 24-29 | 20-26 | 6x7 | parties 2 |
| 1 | fob | Friends of Baikal (17) | 10 | 32-39 | 20-26 | 8x7 | parties 2 |
| 1 | smc | Socialist Market Commonwealth (18) | 12 | 42-49 | 20-28 | 8x9 | parties 2 |
| 1 | usr | Union of Sovereign Republics (19) | 9 | 52-57 | 20-26 | 6x7 | parties 2 |
| 1 | sd | Systems Directorate (0) | 14 | 62-71 | 10-18 | 10x9 | parties 1 |
| 1 | nts | People's Labour Union (1) | 13 | 74-81 | 10-19 | 8x10 | parties 1 |
| 1 | chr | Committee for Human Rights (2) | 15 | 62-71 | 21-30 | 10x10 | parties 2 |
| 1 | uds | Union of Democratic Socialists (3) | 13 | 74-81 | 21-30 | 8x10 | parties 2 |
| 1 | wc | Free Councils of Labour (5) | 17 | 86-95 | 10-20 | 10x11 | parties 1 |
| 1 | ns | Neo-Stalinist Platform (6) | 17 | 98-107 | 10-20 | 10x11 | parties 1 |
| 1 | kv | Komsomol Vanguard (7) | 17 | 110-119 | 10-20 | 10x11 | parties 1 |
| 2 | ple | Das Politbüro: Machtwechsel | 11 | 134-153 | 0-1 | 20x2 | plenum |
| 2 | cpsu | KPdSU: Partei Lenins | 7 | 126-129 | 3-7 | 4x5 | General Secretaries 1 |
| 2 | bre | Breschnew | 40 | 132-157 | 3-11 | 26x9 | General Secretaries 1 |
| 2 | kos | Kossygin | 30 | 160-179 | 3-14 | 20x12 | General Secretaries 1 |
| 2 | pod | Podgorny | 21 | 182-191 | 3-12 | 10x10 | General Secretaries 1 |
| 2 | sus | Suslow | 24 | 194-207 | 3-13 | 14x11 | General Secretaries 1 |
| 2 | she | Schelepin | 23 | 210-223 | 3-12 | 14x10 | General Secretaries 1 |
| 2 | and | Andropow | 23 | 134-145 | 16-26 | 12x11 | General Secretaries 2 |
| 2 | gre | Gretschko | 21 | 148-161 | 16-24 | 14x9 | General Secretaries 2 |
| 2 | ust | Ustinow | 23 | 164-175 | 16-25 | 12x10 | General Secretaries 2 |
| 2 | gro | Romanow | 18 | 178-187 | 16-24 | 10x9 | General Secretaries 2 |
| 2 | che | Tschernenko | 17 | 190-201 | 16-26 | 12x11 | General Secretaries 2 |
| 2 | gor | Gorbatschow | 24 | 204-215 | 16-28 | 12x13 | General Secretaries 2 |
| 3 | eco | Gosplan & Fünfjahrpläne | 39 | 231-264 | 0-11 | 34x12 | A |
| 3 | agr | Landwirtschaft & Getreide | 18 | 230-245 | 13-17 | 16x5 | B |
| 3 | en | Energie, Sibirien & BAM | 15 | 248-265 | 13-17 | 18x5 | B |
| 3 | sci | Wissenschaft & Kosmos | 17 | 240-255 | 19-25 | 16x7 | C |
| 4 | army | Sowjetarmee | 22 | 275-298 | 0-6 | 24x7 | A |
| 4 | str | Strategische Kräfte & Luftverteidigung | 14 | 272-285 | 8-12 | 14x5 | B |
| 4 | navy | Hochseeflotte | 15 | 288-301 | 8-13 | 14x6 | B |
| 5 | union | Die Union der Republiken | 23 | 308-333 | 0-5 | 26x6 | A |
| 5 | kgb | KGB & innere Sicherheit | 16 | 312-329 | 7-11 | 18x5 | B |
| 5 | soc | Sowjetgesellschaft | 15 | 313-328 | 13-16 | 16x4 | C |
| 6 | bloc | Warschauer Pakt & RGW | 19 | 340-357 | 0-5 | 18x6 | A |
| 6 | det | Entspannung & der Westen | 16 | 360-371 | 0-9 | 12x10 | A |
| 6 | chi | Die chinesische Frage | 16 | 340-353 | 11-17 | 14x7 | B |
| 6 | tw | Dritte Welt & Internationalismus | 19 | 356-371 | 11-17 | 16x7 | B |

### Header
- **Shortcuts: 10 instead of 50.** politics goes to the_collective_leadership (92,0); politburo to ple_the_politburo (143,0); outlook_em, we, na and nt to the outlook top foci (row 6); economy to gosplan_directives (243,0); military to the_soviet_army (289,0); state to the_union_of_republics (322,0); foreign to the_socialist_commonwealth (348,0).
- **initial_show_position:** keep `focus = COLDWAR_SOV_the_collective_leadership`. The view then opens on pol, em and the start of the CPSU/Politburo block (bre is 51 columns to the right).
- **continuous_focus_position = { x = 26112 y = 2080 }.** That is grid (272, 16), a free pocket of at least 6x6 below the military block, 73% across the canvas, like MD's pocket at 75% in its domain area.

### Generator changes (in order)
1. In `cw_layout.layout()`, replace the band stacking with `SEC_ORIGIN[k] = (x, y)` from `layout_plan.json`, or port `plan_layout.py`, which computes the same numbers from LAY. Apply `mirror` to pol (local x becomes w-2-x).
2. In the `cw_focus` header, apply the new `continuous_focus_position` and the 10 shortcuts, and drop the other 40 shortcut localisations.
3. Optional, to match MD: chain the anchors. Keep only the 6 block anchor sections absolute (pol, ple, eco, army, union, bloc) and make every other section anchor `relative_position_id` to its block anchor.
4. Optional: make `ple_the_politburo` a real prerequisite of Brezhnev's root again (now a straight line).
5. Separately: extend `section_conflicts()` to the child column, which fixes the 81 lines that run through foci.
6. Width levers if 372 columns feel too wide: compact the widest tidy trees internally (eco 34, bre 26, union 26, army 24, kos/ple 20), or tighten the gaps (they are parameters in `plan_layout.py` RULES). With section/group/block extras of 0/2/2 the canvas is 318 x 31. With 0/0/0, which is MD's packing (nearest foci of neighbouring sections 2 apart), it is 302 x 31. No new line conflicts appear in either case. Depth is not the limit: politics already uses rows 0-30.
