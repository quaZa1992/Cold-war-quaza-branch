# Layout probe 2: MD 2000 Russia positioning rules, diagnosis of COLDWAR_SOV_1970, re-layout

Inputs: `05_russia.txt` (MD, 806 foci) and the sandbox generator `/home/claude/sovgen_layout` (836 foci, 50 sections).
Grid: 1 column = 96 px, 1 row = 130 px. "Gap" always means the distance between the nearest foci of two neighbours in one row. MD never puts two foci of a row closer than 2.

Scripts in this folder:
- `md_probe.py`: MD metrics. Output in `md_probe.txt` and `md_probe.json`.
- `cw_probe.py`: the same metrics for our tree. Run it as `SB=<sandbox> python3 cw_probe.py before|after`. Output in `probe_*.txt` and `cw_probe_*.json`.
- `cw_load_sb.py`: a copy of `../cw_load.py` that takes the sandbox path.
- `colprof.py`: the column profile metric.
- `render_probe2.py`: draws maps the same way as `../render.py`.
- `ascii_md.py`: an ASCII map of MD.

Maps:
- `sov_layout_before.png` and `sov_layout_after.png`.
- `sov_layout_after_politics.png` (party area, x 0-104) and `sov_layout_before_politics.png`.
- `sov_layout_after_politburo.png` (x 100-215).

---

## 1. MD 2000 Russia: positioning rules (measured)

### 1.1 Canvas and blocks
The canvas is **236 x 27**, aspect 6.45:1 in pixels. Fill is 12.6% of the grid cells.

| block, left to right | x | rows | w x h | foci | fill (2-col pitch) | foci per row |
|---|---|---|---|---|---|---|
| Zyuganov | 0-17 | 1-16 | 18x16 | 67 | 0.44 | 1,5,8,9,4,6,6,3,2,5,2,3,6,4,2,1 |
| Westernism | 16-54 | 1-15 | 39x15 | 105 | 0.35 | 1,2,2,3,3,4,5,10,16,12,18,15,6,4,4 |
| New Russia | 36-59 | 1-10 | 24x10 | 44 | 0.35 | 1,4,6,10,8,3,3,4,3,2 |
| Subjects | 58-67 | 1-3 | 10x3 | 8 | 0.48 | 1,4,3 |
| KOB (tucked) | 60-68 | 4-14 | 9x11 | 23 | 0.42 | 1,2,2,3,3,2,2,2,2,3,1 |
| Putin (ruling) | 63-86 | 1-26 | 24x26 | 110 | 0.34 | narrow top (1-3 per row for 9 rows), 5-10 per row in rows 11-24 |
| Zhirinovsky | 83-119 | 1-14 | 37x14 | 117 | 0.44 | 1,4,8,9,9,14,13,13,9,10,9,10,6,2 |
| Nazbols | 119-129 | 1-12 | 11x12 | 29 | 0.40 | |
| Economy | 131-189 | 0-8 | 59x9 | 129 | 0.48 | 1,17,23,21,21,17,15,11,3 |
| Military reform | 183-203 | 0-18 | 21x19 | 86 | 0.41 | |
| Security | 199-209 | 0-5 | 11x6 | 18 | 0.50 | |
| PMC | 210-214 | 0-4 | 5x5 | 9 | 0.60 | |
| Foreign | 215-235 | 0-8 | 21x9 | 60 | 0.61 | 1,2,6,4,8,9,10,10,10 |

### 1.2 Rules

**R1, parent centring.**
- Of the 284 parents with 2 or more children one row down, 149 (52%) stand exactly over the midpoint of their first and last child, and 80% are within 1 column of it.
- For pairs the share is 116/185 exact and 151/185 within 1 column. Wide fans are not centred: the economy root sits at 0.35 of its bar and Yeltsin at 0.46.
- Of the 350 single children, 183 are straight below their parent (dx 0) and 296 are within 1 column.

**R2, hinges: a long bar with sub-blocks side by side.** Every block hangs from a hinge focus through one horizontal bar at dy 1.
- **Yeltsin** has 7 children on one bar (x 10-122, span 112). Sub-block widths are 18, 39, 23, 10, 23, 37 and 11. Their depths are 16, 15, 6, 3, 26, 14 and 12. The gaps between sub-blocks are 2, 3, 2, 6, 2 and 2.
- **Economy root** has 17 children on one bar (span 54, pitch 2-3). Each chain is 1-11 wide and 1-8 deep, with gaps of 2 throughout.
- **Zhirinovsky** has 4 sub-blocks, 7, 8, 3 and 22 wide and 13, 11, 4 and 13 deep, with gaps of 2, 3 and 4.
- **Westernism "Convention"** uses a *hinge row* rather than a single hinge focus. Three parents stand in row 5: reconcile_cprf_2 at x 24, foster_multi_party_democracy at 27 and ostracize_cprf at 30. Four party roots stand in row 6: PARNAS at 18, SPS at 24, Yabloko at 35 and A Just Russia at 47. Each party root has an OR group (reconcile or ostracize) plus an AND parent (foster). All lines have dy 1, so the OR and AND lines share the 5.5 channel and cannot cross a focus.
- The gap between sub-blocks is **2 columns** (most common value), sometimes 3-4. The gap between top-level blocks has a minimum of 2 and a median of 7.

**R3, tops and depths.**
- Every independent root is at row 0, and every party leader is at row 1 under the trunk bar, so all block tops align at row 0 or 1. The bottoms are ragged, from 3 to 26 rows.
- Depths alternate rather than being sorted. Left to right they run 16, 15, 10, 3 (+KOB), 26, 14, 12, then 9, 19, 6, 5, 9.
- Blocks are packed by **row contour**, not by bounding box. Bounding boxes overlap by up to 18 columns: Westernism's lower sub-parties run on under the shallow New Russia, and the economy and military overlap by 6.

**R4, roots gated by `available` or `allow_branch` are tucked into free space.**
- 12 foci have no prerequisite. 6 of them are roots at row 0: Yeltsin, economy, military reform, security, PMC and foreign.
- KOB (`allow_branch`) is at (64,4). It sits one row under the 3-row Subjects block, next to Putin's column (gap 2).
- Five small available-gated roots sit beside their related focus at the same height or one row lower: referendum_start, russia_good and usr at row 7 under New Russia, oligarchs_democracy at row 9 in Putin's block, and western_russia at row 18.

**R5, the ruling party is next to the trunk.**
- Subjects (shallow, 3 rows) is straight below Yeltsin.
- Putin is the next block (dx +13 from Yeltsin). It is the deepest column in the tree, 24 wide by 26 rows: a sequential story with mutually exclusive triples.
- Opposition parties sit to the left; Zhirinovsky and Limonov sit to the right, followed by the domains.

**R6, mutually exclusive groups.**
- There are 40 groups: 35 pairs and 5 triples.
- **All 40 are on one row, and none has another focus between the partners.** The spacing between partners is dx 2 (25), 4 (11) or 6 (4), rarely 3, 3.5, 2.5 or 8.
- 37 of the 40 share a parent one row up, and that parent is centred over the group in 21.

**R7, long lines.**
- There are 1,200 lines. 92% have dy 1 (1,100); 95 have dy 2 and 2 have dy 3.
- Line lengths: |dx| <= 2 for 79%, >= 6 for 102 lines, >= 10 for 42 and >= 20 for 12.
- The 12 lines with |dx| >= 20 are all hinge bars or OR lines:
  - Yeltsin's bar: dx 60, 52, 35 and 31.
  - The economy root's fan: dx 35, 28 and 21.
  - OR lines from the party-victory foci into foreign policy: dx 30, 26, 26 and 22, all at dy 2.
  - Foster to A Just Russia: dx 20.
- No long line drops vertically through the tree. Long means horizontal, in the channel under the parent.

**R8, row use and shape.**
- Blocks are 0.34-0.61 full at a 2-column pitch.
- Average empty rows above the first focus of a column: 2.9. Interior vertical holes of 3 or more rows: 152 cells in 32 of 118 column pairs.

**R9, other ways MD keeps blocks together.**
- OR groups: 100 in total. In 89 the parents are on one row, and in 77 the child stands between the parents. The spread between parents is 2 (44) or 4 (24).
- Staggered fans: the 7 Subjects referenda alternate between rows 2 and 3 at a 1-2 column pitch.
- `relative_position_id`: party leaders are relative to Yeltsin (-52 to +60) and the economy root at +90. The other domain roots are absolute.
- The continuous-focus pocket sits under the shallow economy block, 75% of the way across.

### 1.3 Sketches (MD coordinates)

```
(1) Trunk hinge: one parent, one bar, party blocks side by side, tops on row 1, gaps 2-6
row 0                                          Yeltsin(62)
      +----------------+----------------------+-----+------+-----------------+-----------------------------+
row 1 Zyuganov(10)     Westernism(27)       NewRus(49) Subj(62) Putin(75)   Zhirinovsky(93)            Nazbols(122)
      18w x16          39w x15              23w x6-10  10w x3   24w x26     37w x14                    11w x12
```
```
(2) Hinge row (Westernism "Convention"): three parents on one row, party columns one row below, all lines dy 1
row 5               reconcile(24)  foster(27)  ostracize(30)
          ..........:......+.......+...........:......................................   (OR dashed + AND solid, 5.5 channel)
row 6   PARNAS(18)       SPS(24)              Yabloko(35)                    A Just Russia(47)
        5 wide           5 wide               14 wide                        13 wide      (gap 2; 7-10 rows deep)
```
```
(3) Domain fan (economy): one root, 17 short chains on one bar, pitch 2-3, 9 rows in all
row 0                         Economy(152)
      +--+--+--+--+--+--+--+--+---+--+--+--+--+--+--+--+
row 1 c  c  c  c  c  c  c  c  c   c  c  c  c  c  c  c  c      chains 1-8 deep, 1-11 wide, gap 2
```
```
(4) Tucked root (KOB, allow_branch) under a shallow block, staggered fan above it
row 1              Subjects(62)
row 2   Ural(58) KhMAO(60)      Bashk(64) Tatar(66)
row 3          Kuban(61) Crimea(63)          Chechnya(67)
row 4                       [KOB](64)                         <- no line; column x 60-68, rows 4-14, gap 2 to Putin
row 5                  Loyal(63)  Militar(65)
```
```
(5) Mutually exclusive: same row, adjacent, parent centred one row up
        P                 P
      +-+-+           +---+---+
      A x B           A   B   C        dx 2 / 2 (also 4, 6); never a foreign focus between A and C
```

---

## 2. Diagnosis of our tree (before)

Before: 327 x 31, aspect 7.8:1, fill 8.2%. Sections were tidy trees, stacked in tiers inside 6 blocks. Each line below is "section key: what is wrong", measured against the MD rules.

**Floating islands.** 43 roots without a prerequisite sit below row 0 (MD: 6).
- Outlook second roots: `em` em_the_leading_role_of_the_party, `we` we_a_democratic_union, `na` na_neither..., `nt` nt_russia_first. All four sit at row 6 inside the outlook band with no line.
- `cpsu` is at row 3, *above* its logical parent power_the_cpsu (dx 16, dy -3).
- `bre` is 3 rows under ple_the_politburo with no line.
- `kos`, `pod`, `sus` and `she` are at row 3, 35-70 columns from their candidacies.
- `and`, `gre`, `ust`, `gro`, `che` and `gor` are at row 16, 15 rows under their candidacies, dx 1-51.
- `wc`, `ns`, `kv`, `sd`, `nts`, `gt`, `lnl`, `rd`, `rp` and `cnr` are at row 10, dy 2 and dx 2-18 from their power focus.
- `chr`, `uds`, `fel`, `fob`, `smc`, `usr`, `com` and `rom` are at rows 20-21, dy 12-13.
- Domain sections: `agr` and `en` at row 13, `sci` at 19, `str` and `navy` at 8, `kgb` at 7, `soc` at 13, `chi` and `tw` at 11.

**Vertical stacking of unrelated sections.** There are 31 pairs (`cw_probe` counts a section stacked under another with which it has no logical link, direct or through other sections).
- General Secretary tier 2 under tier 1: `and`/`gre` under `bre`; `gre`/`ust`/`gro` under `kos`; `gro`/`che` under `pod`; `che`/`gor` under `sus`; `gor` under `she`.
- Party tier 2 under tier 1: `chr` under `sd`, `uds` under `nts`, `fel` under `gt`, `fob`/`smc` under `lnl`, `usr` under `rd`, `com` under `rp`, `rom` under `cnr`.
- Domains: `agr`/`en`/`sci` under `eco`, `sci` under `agr`/`en`, `str`/`navy` under `army`, `kgb`/`soc` under `union`, `soc` under `kgb`, `chi`/`tw` under `bloc`, `tw` under `det`.
- Count: 10 General Secretary pairs, 8 party pairs and 13 domain pairs.

**Ragged tops.** Sections start at 12 different rows: 0, 3, 6, 7, 8, 10, 11, 13, 16, 19, 20 and 21.

**Empty areas.**
- Interior vertical holes (3 or more empty rows between two foci of a column): **1,149 cells in 130 of 151 column pairs**. MD has 152 cells in 32.
- The holes are between the tiers: General Secretary rows 12-15, party rows 19-20, and the economy, state and foreign tiers.
- Gaps between sections in a row: median 10, 59% of them 10 or more (MD blocks: median 7).

**Long dotted links** (`available` only, no line).
- There are 49, with median dx 7 and max 70, median dy 4 and max 15. 38 of them are longer than 10 steps.
- Worst: `ple_she` to `she` dx 70; `ple_sus` to `sus` dx 59; `ple_gor` to `gor` dx 51, dy 15.

**Long lines that do not follow MD.**
- `pol` dir_* to the outlooks: 4 parents each draw a bar at y 4.5 across x 5-88. The bars lie on top of one another, so the player cannot see which direction feeds which outlook. All drops are dy 2.
- In MD a long bar always comes from one parent with dy 1.

**Hinges missing.** The power_* foci of each outlook stand at a 2-column pitch (`na`: 7 foci in 13 columns), while their party trees are spread over 30-60 columns. The hinge row does not sit over its sub-blocks.

**Unchanged and fine.** All 95 mutually exclusive groups are on one row and adjacent. Line conflicts: 0. No two foci of a row are closer than 2.

---

## 3. What I changed, and why (only `cw_layout.py`, from "section layout" to the end)

1. **`layout_section` is now a contour tidy tree** (R1, R3).
   - A parent is centred over its first and last child.
   - Sub-trees are packed by row contour with gap 2.
   - Each node chooses between the sibling order and its mirror (mirroring keeps mutually exclusive partners adjacent) to keep the sub-tree narrow and its deepest foci under the parent. This straightens story columns the way MD's are.
   - `VIRT[p]` now reserves the column under the parent down to its deepest line, and the parent stands on that column. The `section_conflicts` / `VIRT` loop is unchanged.
   - A new `_settle()` moves a child 1-3 columns aside inside its section when one of its lines would cross a focus. It keeps 2 columns to the other foci of the row and never jumps over one, so the global `fix_child_columns()` now has nothing left to do (it moved 34 foci before).
   - Total section width: 674 before, 509 after.
2. **Row-contour helpers** `_c_add`, `_c_merge` and `_c_offset`. `_contour()` covers both foci and line channels: a bar under its parent, the drop columns, and the `_xav` groups about to become lines. `_pack()` places parts left to right as far left as their contours allow, never left of the previous part, so blocks interleave like MD's without anything sliding under another block.
3. **Politics** (`_outlook_group`, `_trunk`; R2, R5, MD sketches 1 and 2).
   - whither_the_union hangs the four `dir_*` foci on **one bar** (dy 1).
   - Each direction stands over its own outlook group, followed by the outlook tops (M+-1, or M-2/M/M+2 for `na`), the merge focus M, and the **power_* foci as a hinge row** (row 7).
   - **Every party tree hangs straight below its power focus** (row 8), side by side with gap 2.
   - The outlook's second root (government already in power) closes the hinge row on the right. Its OR lines to the party roots run in the 7.5 channel, exactly like MD's Westernism Convention.
   - `cpsu` hangs under power_the_cpsu.
   - Groups run nt | na | we | em with gap 4. The trunk stands right of `em`, next to the Politburo.
   - The trunk keeps the design order and stays **mirrored** (`MIRROR` kept). `_trunk()` also checks that whither faces the outlooks and stands 2 columns clear of the doctrine branch, so the two bars at 3.5 never merge.
   - The direction foci left the trunk's cluster. This replaces the 4 stacked bars with one bar.
4. **Politburo** (R2, R5). `ple_the_politburo` hangs the 10 candidacies on one bar.
   - Each General Secretary tree stands straight below its candidacy (dx 0, dy 1, row 2), all 11 on one row.
   - Order: kos, pod, sus and she (the 1970 colleagues), then **bre in the middle**, straight below ple_the_politburo, then and, gre, ust, gro, che and gor. The bar runs 49 columns left and 53 right, like Yeltsin at 0.46.
   - The design deliberately keeps the candidacy-to-tree links as flags ("however he came to power"), so those links stay unlined.
5. **Domains** (R3, R4). Every section root is at row 0, side by side with gap 2: economy (eco, agr, en, sci), military (army, str, navy), state (union, kgb, soc) and foreign (bloc, det, chi, tw). There are 4 columns between blocks.
   - The sub-sections have no cross-section link (`_xav` is empty; they are gated only by `has_completed_focus = the_collective_leadership` in `available`), so a drawn fan under the domain root is impossible. MD's equivalent for independent roots is row 0 side by side (reform | security | PMC | foreign).
6. **`link_cross_prerequisites()`** runs after `layout()` and applies the allowed exception. A section root's `_xav` group becomes a `prerequisite` when every member stands in the row straight above it, or straight above in its column, and the new lines cross no focus.
   - **20 groups were converted (39 lines):** the 18 party roots and `cpsu`, each OR {power_X, outlook second root} with dy 1 and the power focus at dx 0, and `bre` {ple_the_politburo}, a straight vertical with dy 2 whose row-1 cell is empty.
   - The condition is identical. A structural diff of the focus files shows that, apart from these 20 groups and x/y/`relative_position_id`/`continuous_focus_position`, nothing differs. All other files in `out/` are byte-identical.
7. `fix_child_columns()` is kept. Its candidate shifts are now +-1..3, and it will not place a focus closer than 2 columns to another focus of the row (MD has no 1-column neighbours).
8. `_boxes()` fills `SEC_ORIGIN` (bounding box of each section; boxes may now interleave, so the box-overlap assert became a focus-overlap assert), `BLOCK_X`, `BLOCK_BOTTOM` and `BLOCK_IDS`. It runs again after the fixer, and `WIDTH`/`HEIGHT` are recomputed at the end.
9. Constants:
   - `OPP` is now (outlook, [party sections incl. cpsu]), `GS_T1`/`GS_T2` form one row, and `DOMAINS` gives one row per domain. `GAP` = 2, `OUTLOOK_GAP` = 4, `BLOCK_GAP` = 4.
   - The tier constants were removed. `ANCHOR`, `SEC_ORIGIN`, `BLOCK_X`, `BLOCK_BOTTOM`, `WIDTH`, `HEIGHT`, `MIRROR` and `MOVED` still exist.
   - `layout()` can be called again.

The new outlook group, as built:
```
row 3  ...-----------------------------------------------------------+ whither_the_union (trunk)
row 4                          dir_the_leading_role
row 5                     new_type      komsomol
row 6                          workers_state
       +-----------+-----------+------------+
row 7  pow_cpsu    pow_councils  pow_iron   pow_komsomol          leading_role   (second root, no prerequisite)
       :...........:.............:..........:.....................:  +--+      OR {power_X, leading_role}, 7.5 channel
row 8  cpsu        wc            ns         kv              emulation  control
       (party trees straight below their power focus, gap 2, rows 8-18)
```

---

## 4. Metrics: MD, before, after

| metric | MD Russia | before | after |
|---|---|---|---|
| canvas (cols x rows) | 236 x 27 | 327 x 31 | **427 x 19** |
| aspect (px) / fill | 6.45:1 / 12.6% | 7.8:1 / 8.2% | 16.6:1 / 10.3% |
| roots without prerequisite / of them below row 0 | 12 / 6 | 50 / 43 | **30 / 14** (4 outlook second roots in their hinge row, 10 GS roots straight under their candidacy) |
| dotted (`available`-only) links: n, median dx/dy, max dx/dy | - | 49, 7/4, 70/15 | **10, 0/1, 0/1** |
| sections stacked under an unrelated section | 0 | 31 | **0** |
| distinct top rows of sections | 0/1 (+KOB 4) | 12 | 4 (0 roots, 2 GS, 5 outlooks, 8 parties: one per hinge level) |
| interior vertical holes (cells / column pairs) | 152 / 32 | 1149 / 130 | **114 / 28** |
| gap between neighbouring sections/blocks in a row: min / median / share >= 10 | 2 / 7 / 34% (blocks) | 2 / 10 / 59% | 2 / 5 / 26% |
| lines: n, dy 1, dx <= 2 | 1200, 92%, 79% | 983, 94%, 73% | 1022, 95%, 82% |
| lines dx >= 20 / max dx | 12 / 60 | 8 / 69 | 15 / 84 (whither to dir_the_russian_idea; ple bar max 53) |
| parent centred (exact / within 1) | 52% / 80% | 92% / 97% | 88% / 95% |
| mutually exclusive groups on one row and adjacent | 40/40 | 95/95 | 95/95 (dx 2: 100 of 109 spacings) |
| same-row neighbours closer than 2 | 0 | 0 | 0 |
| `line_conflicts()` | - | 0 | **0** (global fixer moves: 34 before, 0 after) |
| `validate_sov.py` | - | 0 errors, 8 warnings | 0 errors, 8 warnings (same warnings) |

Foci per row in each block after the re-layout:
- **Politics** (x 0-101, rows 0-18): 1,2,1,2,6,11,4,23,27,43,21,37,23,25,20,24,15,9,3.
- **Politburo** (x 102-212, rows 0-14): 1,10,11,33,29,44,36,32,18,20,15,14,7,4,1.
- **Economy**: 0-11 rows. **Military**: 0-6. **State**: 0-5. **Foreign**: 0-9.

The continuous-focus pocket is now at grid (325, 8), under the state block, 76% of the way across (MD: 75%). The 10 shortcuts still point at `ANCHOR`s.

---

## 5. Open points and levers

- **Width.** At 427 columns the canvas is 1.8 times MD's width; MD fits in 27 rows. The rules "side by side, no unrelated stacking" put all 50 sections on one row. Even after the contour compaction the sections sum to 509 columns of tree width, while our trees are only 5-13 rows deep (MD's Putin is 26).
  - Narrower gaps change little: `BLOCK_GAP` = `OUTLOOK_GAP` = 2 gives 414.
  - The real lever is MD's own R4 tucking: small domain sections such as `soc`, `kgb`, `str` or `navy` could sit under a shallow neighbour. That is stacking, which this brief forbids, so it was not applied.
- **Politics roof.** Rows 0-3 above the outlook groups are empty except for the whither bar at 3.5. The trunk's stem (collective_leadership, lenin_centenary, 24th congress, whither, rows 0-3) is fixed by the design's prerequisite chain. MD's roof is one row, because Yeltsin heads the parties directly.
- **Unlined roots that remain.** The 10 General Secretary roots are flag-gated by design, so drawing a line would change gameplay; they stand straight below their candidacy. The 4 outlook second roots have no prerequisite at all. The domain section roots are gated by `available` only.
- The check covers lines through foci only, not lines crossing lines. Some General Secretary trees have long internal secondary-prerequisite lines from the design (for example in `kos` and `sus`); they existed before too.
- The line-conflict model is conservative: it checks both the parent column and the child column. The layout has not been checked in game.
- The sandbox `README.md` still says "328 x 31". It was not edited, because only `cw_layout.py` was to change.
