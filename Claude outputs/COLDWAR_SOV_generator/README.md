# COLDWAR_SOV_generator - Soviet Union 1970 (Cold War mod)

Generates every file of the Soviet 1970 focus tree and the Politburo of the Republics from the approved design
(`../COLDWAR_SOV_design`, visualised in `soviet_union_1970_focus_tree.html`). Edit the generator or the design, not the output.

Run (Python 3.10+):

    python cw_build.py        # writes ./out (same folder layout as the mod)
    python validate_sov.py    # static checks: braces, loc, references, sprites, ideas, modifiers, events, flags

Modules:
- cw_layout.py: loads the design and lays out the 836 foci on one canvas (tidy tree per section, sections stacked)
- cw_avail.py / cw_effects.py / cw_manual.py: convert the design's conditions and effects into MD-style code
- cw_focus.py: the focus tree file (MD 2000 focus style, log line in every reward)
- cw_sys_effects.py: init, money, factions, cohesion, Politburo balance, General Secretaries, seats, votes, proposals, kompromat
- cw_decisions.py: decision categories and decisions (Moscow and the republics)
- cw_events.py / cw_offers.py: events (Politburo, congresses, deaths, crises) and the 48 offers (the partner decides)
- cw_misc.py: ideas, dynamic modifiers, balance of power, opinion modifiers, traits, on_actions, scripted localisation
- desc/: English focus descriptions and icon choices (out_N.json, icons_N.json)

Index files are shared with `../COLDWAR_EGY_generator` (goal_sprites.json, idea_gfx.txt, repo_paths.json, our_*.txt).

## MD audit (17.10.2026)

- `audit/`: reports of the audit agents – structure of MD's 2000 Russia tree (`md_russia_structure.md`, maps), its focus effects and the
  rulebook (`md_russia_effects.md`, `md_effect_norms.json`), the Imperia / Cold War hooks (`imperia_coldwar_hooks.*`) and the agent
  instructions for the per-focus audit (`INSTRUCTIONS.md`).
- `overrides/<group>.json`: the per-focus edits of the audit (set/del/add effects, cost, extra availability, new ideas, tooltips,
  opinion modifiers). `cw_layout.py` applies them before anything else reads the design, then the review fixes (block
  "fixes from the independent review").
- Layout (layout probe 2, `audit/probe2/md_layout_probe.md`): MD style, wide and shallow (427 × 19). Every section hangs under
  its logical parent and all blocks start at the top. The trunk feeds the four direction foci on one bar, and each direction
  heads its outlook group. Every party tree hangs straight under its power focus. The General Secretary trees stand side by
  side under the Politburo plenum, and the economy, military, state and foreign sections sit side by side at row 0.
  20 cross-section prerequisites, previously only `available`, are real lines again (18 party roots, `cpsu`, `bre`).
  No prerequisite line runs through another focus.
- No date gates (17.10.2026): `cw_avail.atom` drops every "Datum ≥/<" condition of the design; a date alternative inside an
  OR is dropped too. `ALIVE` keeps only the death dates. The "Declare Sovereignty" decision no longer opens in 1985.
- Icons: `cw_focus.BANNED_ICONS` keeps photos out of the tree (`STALIN_PLAN.dds` 750 × 415, `ABMT_1.tga`); the next
  candidate of the icon list is used.
- Stand-ins (17.10.2026): `cw_effects.STANDIN`. When a General Secretary candidate has died (death events 90-97),
  a man of his camp carries his plenum focus and his tree: Kosygin → Ryzhkov, Podgorny → Kuznetsov, Suslov → Zimyanin,
  Andropov → Aliyev, Grechko → Ogarkov, Ustinov → Smirnov, Chernenko → Grishin. Trigger `COLDWAR_SOV_standin_<key>`
  (= not alive). `install_gensec_<key>` creates the stand-in, the death event keeps the candidacy, "Convene the Plenum"
  gets a stand-in variant, and the succession plenum (event 31) offers the stand-in of every dead candidate.
  Shelepin no longer leaves the Politburo in 1975 (that was a date gate, not a death).

## Union projects and the investment burden (18.10.2026)

- `cw_sys_effects.BUILD`: Moscow pays four times the old price for a Union project in a republic (civilian factory / power station 2 %,
  infrastructure / agriculture 1.5 %, military factory 3 % of its GDP). Used by the petition (event 29), approved proposals (events 20/22)
  and the plan project (event 25).
- Every project adds one burden to SOV (`COLDWAR_SOV_republic_burden`) for `BURDEN_DAYS` = 90 days (hidden event 30 lifts it):
  dynamic modifier `COLDWAR_SOV_republic_investment_modifier` "Investment in the Republics", Tax Cost Factor (Consumer Goods)
  +10 % per active burden (stacking), and the next project costs +50 % per active burden. The AI grants petitions only with no
  burden running (×0.4 at one, never at two or more).
- Event 29 uses the Politburo photo `GFX_report_event_COLDWAR_SOV_politburo_table` (MD frame 217 × 163); `cw_build.EVENT_PICTURES`
  writes `interface/COLDWAR_SOV_1970_event_pictures.gfx`, the DDS lives in `gfx/event_pictures/coldwar_1970/`.
- `cw_build.py`: the history patches are idempotent (the build also runs on the already patched mod file) and include the KGB at the start.

## The Union Plan (18.10.2026): missions of the republics, Moscow's judgement, the joint Union tree

Module `cw_union.py` (prefix `COLDWAR_UNI_`, event namespace `COLDWAR_UNI`, own files `COLDWAR_UNI_1970_*` and
`localisation/english/COLDWAR_UNI_1970_l_english.yml`). Concept: project doc `claude/mdcw_union_missions_concept.md`.

- **Cycle.** The January Politburo session (event `COLDWAR_SOV.10`, marker temp `COLDWAR_UNI_january`) calls
  `COLDWAR_UNI_january_session` from January 1971: settlement of the old year (`COLDWAR_UNI_settle_year`), then event
  `COLDWAR_UNI.1` 14 days later issues every republic's annual target (mission, 300-321 days, Moscow's plan priority x1.5)
  and Moscow's mission "Fulfil the Union Plan" (completes at 9 of 14 → "The Plan Is Fulfilled!" for Moscow and every fulfiller).
  With the joint focus "The Union Plan" a republic chooses in "Gosplan's Draft" (event 3): priority, its regional mission,
  Roads of the Union, Plan Deliveries, Party Discipline, or the Counter-Plan.
- **Failure.** Shortfall points by weight (UKR 3; BLR, KAZ, UZB 2; others 1), 180 days each, stacking (events 41/42):
  Moscow's dynamic modifier "Shortfalls in the Republics" = construction −2.5 %, political power −2.5 %,
  Tax Cost Factor (Consumer Goods) +1 % per point. News 30 to every member, judgement event 10 to Moscow (FROM = republic,
  15 days, default pardon). Levels: pardon, reprimand, requisition (25 % of civilian factories, 1-3, 60 days, Moscow gets
  them free), offices, levy 0.3 % GDP, slow construction, replacement by Politburo vote (type 5) or by decree,
  Gorbachev's khozraschet. Costs: `COLDWAR_UNI_judgement_cost` (cohesion, seat, protection, General Secretary rules).
- **Success.** Reward idea by family and tier (180 days), Moscow's "Deliveries from the Republics" (+1 %/point, 180 days).
- **Pripiski.** `report_overfulfilment` also fulfils a running mission; exposure (kompromat, KGB investigation, January audit
  with People's Control or Andropov) removes the reward, counts double, and Moscow judges (hidden event 45 fires news 31 and
  event 10 from the republic).
- **Joint tree** (`COLDWAR_UNI_1970_union_joint.txt`, 17 foci): attached with `shared_focus = COLDWAR_UNI_the_union_plan`
  in the Soviet tree (root 355/8, box `cw_focus.UNION_BOX` kept free) and, by an idempotent patch in `cw_build.py`, in
  `mdcw_1970_generic_focus` (root 240/0). Never ship the shared_focus line without the joint file (a missing shared focus crashes).
- **Validator** (`validate_sov.py` section 12): joint ids, attachment, membership trigger, positive member rewards, AI
  de-duplication, missions defined and activated, Union box free.

## Politburo votes by decision, leadership votes, readable tooltips (18.10.2026)

- **Who votes.** Every Politburo vote (`COLDWAR_SOV_start_vote`) is cast by the three republican seat holders. A human seat holder
  gets notice event `COLDWAR_SOV.11` and votes in the decision category "The Politburo Votes"
  (`COLDWAR_SOV_politburo_vote_category`, visible while `vote_running` and `in_vote`): "Vote in Favour" or "Vote Against"
  (weapon icon `GFX_decision_weapon_on_tabel_dont_use_as_goal_icon`). Not voting within the 10 days of the vote is an abstention.
  AI seat holders vote through `COLDWAR_SOV_ai_ballot`: always yes on a leadership change (type 3), no against their own cadre
  replacement, 67/33 on a replacement (type 5), else 91/9.
- **Leadership votes (type 3).** Moscow casts 3 votes in favour (the seven simulated Moscow members and the General Secretary's
  vote are not used), every republican seat 1. Only cast votes count (`global.COLDWAR_SOV_vote_rep_cast`): the change fails
  only if all three seats vote against. All other vote types keep the old weighting (seven Moscow members by balance and lean).
  Texts: scripted loc `COLDWAR_SOV_GetVoteLeanFull`, `COLDWAR_SOV_GetMoscowVote`, `COLDWAR_SOV_GetOwnVote`.
- **Readable tooltips.** `cw_names.py`: `ctt()` wraps every generated condition in `custom_trigger_tooltip` with an English text
  (Politburo balance, General Secretary, faction opinion, Union cohesion, Cold War tension, oil price level, party popularity);
  `add_name_loc()` gives every COLDWAR flag and variable a loc key (curated names in `FLAG_TEXT`/`VAR_TEXT`, families such as
  `*_unlocked`, programme variables named after their dynamic modifier). `cw_build.hide_var_ops` wraps plain variable
  bookkeeping in COLDWAR effects in `hidden_effect`.
- **Validator** section 13 (`tools/raw_tooltip_scan.py`, parser `tools/pdx.py`): error on any raw flag/variable name a player
  would see in a focus, decision or event tooltip.
- **External hooks.** The historical-politics tool (`tools/historical_politics_1970/sov_egy_successors.py`) hooks the manual
  retirement of the General Secretary into our succession vote (`MDCW_HP_SOV_*`, markers `# MDCW HP SOV ... BEGIN/END`).
  The hooks are part of the generator (`cw_sys_effects.HP_*`) so a rebuild keeps them; the validator accepts the `MDCW_HP_*`
  effects defined in `common/scripted_effects/mdcw_historical_*.txt`.

## The Politburo dossier (19.10.2026): a GUI in the decision category

Module `cw_pbgui.py`; art in `art/` (`pb_layout.py` shared coordinates, `politburo_art.py` paints the textures with Playwright/Chromium
and the fontsource fonts into `art/dds/`, `preview.py` renders a mock-up). `cw_build.py` copies `art/dds/*.dds` to
`gfx/interface/coldwar_politburo/`. Re-run `python3 art/politburo_art.py` only when the look or the layout changes.

- **One category for everybody.** "The Politburo of the CPSU" (`COLDWAR_SOV_politburo_cpsu_category`, `scripted_gui = COLDWAR_SOV_politburo_gui`)
  is shown to Moscow and to every Union republic. The former categories "Seats of the Republics", "The Republic and the Politburo"
  and "The Politburo Votes" are groups inside it now (`cw_decisions.MERGED`): their allowed/visible conditions move into each
  decision, so every country sees only its own decisions; the ballot comes first.
- **The file** (510 x 740, a Soviet dossier: red banner, typed form, pinned photos, rubber stamps):
  the General Secretary (portrait, office, name, designated heir, Politburo balance marker, Union cohesion and tier, next session,
  next Party Congress); the three republican members (portrait, flag, name, title; vote stamps FOR / AGAINST / ABSTAINED / AWAITING
  during a vote; VACANT for an empty seat); the ballot line (running vote or the last decision with ADOPTED / REJECTED);
  Socialist Emulation (growth, industry, output per head, Union Plan targets: leading republic, its value, our place);
  the Pride of the Union.
- **Live data.** Portraits come from scripted loc by leader name (`has_country_leader`), with a "no photograph" silhouette for
  unknown names; the balance marker is one of 21 sprites chosen from `COLDWAR_SOV_bop`. Seat slots (`global.COLDWAR_SOV_pb_seat_1..3`,
  sticky per republic) are updated by `COLDWAR_SOV_pb_update_seats` (take/leave seat, startup, monthly); the ranking by
  `COLDWAR_SOV_pb_update_board` (startup, monthly).
- **Pride of the Union.** See Socialist Emulation below (module `cw_emulation.py` since 20.10.2026).
- **Portraits** of Kosygin, Podgorny, Suslov, Shelepin, Grechko, Romanov, Kuznetsov and Grishin are now wired from
  `gfx/leaders/mdcw_historical_pool/` (leaders created by the tree get them too).
- **Validator** section 14: GUI elements vs scripted GUI, sprites, loc keys, shipped textures, background size.
  `tools/device_known_textures.txt` lists device textures the cloud mirror lacks.

## Socialist Emulation (20.10.2026): banners, honours, Moscow's favourite, pripiski, Spartakiad

Module `cw_emulation.py` (imported by `cw_pbgui.py`; its effects and scripted loc are written with the dossier's files). Multiplayer
rule: ideas, traits and political power reach a country only through an event in its own scope; the effects keep the books.
Tunable constants at the top (`INFL_*`, `FAVOUR_*`, `PRIDE_DAYS`, `SP_*`).

- **Table** (`COLDWAR_SOV_pb_update_board`, monthly via `COLDWAR_SOV_pb_monthly` from `on_monthly_SOV`): growth, industry, output per
  head, plan targets (the plan of temp `COLDWAR_SOV_pb_judge_plan`: the January judgement passes the plan of the judged year).
  A republic with `COLDWAR_SOV_pb_inflated` (pripiski) reports growth +1.5, factories and output per head x1.1; a disqualified one
  (`COLDWAR_SOV_pb_disqualified`, 365 days) is last everywhere and shows "disqualified" as its place.
- **Four Transferable Red Banners** (every third month, `COLDWAR_SOV_pb_award_banners`): to the leader of each column if its value is
  above 0; the holder keeps it on a tie. Gain events 162-165 (visible), loss 166-169 (hidden), rank refresh 179. Ideas
  `COLDWAR_SOV_banner_<k>` / `_2` (doubled after the Union focus Socialist Emulation, global flag `COLDWAR_UNI_emulation`):
  growth construction +5 %, industry factory output +3 %, output per head consumer goods -2 %, plan stability +3 % and PP +5 %.
  The old January banner of the Union plan (`COLDWAR_UNI_red_banner`) is gone; news 34 names the plan banner holder.
- **January judgement** (`COLDWAR_SOV_pb_award_pride`): lowest sum of the four ranks wins (Moscow's favourite -3, disqualified cannot
  win). Event 160 to the winner (`COLDWAR_SOV_pb_receive_pride`): Pride of the Union (stability +5 %, PP +10 %, construction +10 %,
  consumer goods -5 %, 365 days); a second title in a row: Hero of Socialist Labour instead (adds construction +15 %, factory
  output +5 %) and the leader trait `COLDWAR_SOV_gold_star`; three titles in one Five-Year Plan: the Order of Lenin (permanent,
  `cancel` when the republic leaves the Union). The worst (not the winner, not the favourite, not disqualified, more than 2 republics)
  gets event 161: Lagging Behind (stability -3 %, PP -5 %, 365 days, investigation chance +10). News 38 with all lines.
- **Moscow's favourite** (SOV decision `COLDWAR_SOV_pb_favour_republic`, 50 PP, one per 365 days, cohesion -1): event 176 to the
  republic (PP +25, flag `COLDWAR_SOV_pb_favoured`), which sends news 177 to Moscow and the other republics (opinion modifier
  `COLDWAR_SOV_moscows_favourite` -20 towards the favourite).
- **Pripiski** (`report_overfulfilment`): no public news any more; private event 16 and the flag `COLDWAR_SOV_pb_inflated`.
  Exposure (`COLDWAR_UNI_pripiski_exposed`, the proven branch of `COLDWAR_SOV_investigate_republic`) calls `COLDWAR_SOV_pb_disqualify`
  (hidden event 178 strips Pride, Hero, Order and banners and resets streak and titles).
- **Spartakiad of the Peoples of the USSR** (V 1971, VI 1975, VII 1979, VIII 1983, IX 1986): hidden SOV events 180-184 open the
  preparations 90 days before (news 170; AI republics roll 0-10 points), the republics' decisions `COLDWAR_SOV_pb_sp_train` (25 PP, +3),
  `_stadiums` (0.15 % of GDP, +4), `_special` (25 PP, +6, one in four caught: event 173 Doping Scandal); hidden events 185-189 hold the
  games: points + 2 x weight (`COLDWAR_UNI_weight_of`) + random 0-7; gold event 172 (Champions of the Spartakiad, 730 days), silver
  174 (+50 PP), bronze 175 (+25 PP), cohesion +2, news 171.
- **Dossier**: a banner per row (bright when the leader holds it, faded when it still hangs elsewhere; tooltip names the holder), and
  an honour roll: Pride (with "Hero of Socialist Labour" or "title withdrawn"), last place, Moscow's favourite, the Spartakiad line.
