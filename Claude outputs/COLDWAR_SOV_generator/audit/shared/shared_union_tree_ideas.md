# Shared Union Tree: Design Brainstorm (17.10.2026)

**Status:** brainstorm only. Nothing here is approved or implemented.
**Text:** in-game names are in English. IDs use the proposed prefix `COLDWAR_UNI_` (see question 9).

**Checked before writing:**
- the SOV generator (`/home/claude/sovgen`: `cw_sys_effects.py`, `cw_events.py`, `cw_decisions.py`) and the SOV design (`/home/claude/sov/d_*.py`)
- the project docs: SOV implementation, coding playbook, generic 1970 tree
- MD 2.0.2's shared and joint trees in the mod: `gulf_shared.txt`, `Commonwealth_shared.txt`, `03_benelux_shared.txt`, `06_MERCOSUR_shared.txt`, `06_czehcoslavakia_shared.txt`

**Status tags used throughout:**
- **[OK]**: standard HOI4/MD, already used in our code
- **[MD-PROVEN, TEST]**: MD uses it, but we must confirm the exact behaviour in game
- **[VERIFY]**: probably works, not yet seen in our code
- **[UNSURE]**: avoid it, or build a fallback

---

## 0. In one paragraph

The shared tree is the economic side of the Union. The Politburo of the Republics already decides who sits, votes and proposes. This tree decides who builds, delivers, over-reports and pays.

- **Spine:** a per-republic plan ledger.
  - The Five-Year Plan sets a quota. The republic bargains over it at plan start.
  - The republic's foci, decisions and real construction fill the ledger.
  - At the January session that opens the next plan, the ledger is settled. Pripiski are audited first, then rewards are paid.
- **Content:** Union megaprojects (BAM, Urengoy–Pomary–Uzhgorod, the Central Asian energy ring, Siberian rivers and others). Any republic can co-fund them. They pay out only on completion, and only if at least N republics took part.
- **Presentation:** socialist competition. The Transferable Red Banner, the ranking in Pravda and the inspection of the last place are all read off the same ledger.
- **Shared commons:** several republics' gains build up risks that all of them pay for: Aral strain from cotton, the RBMK count for the reactor accident.
- **Endgame:** khozraschet for the republics, the Union Treaty with a 9+1 threshold, and the Economic Community. These are offers only.

---

## 1. Rules this design keeps

1. **Multiplayer safety.**
   - No focus forces war, alliance, bases, territory, annexation or release on another country.
   - Whatever touches another country is an offer, answered in that country's own event. This is the existing dispatcher pattern (events 100–147, notices 900/901).
   - Cooperation pays on acceptance or on completion, never in advance.
   - Joint foci (see §2) carry only harmless rewards for members.
2. **Oil price / OPEC stays player-only.** Oil and gas foci change production, `oil_export_multiplier_modifier`, or treasury scaled by the read-only `global.mdcw_cw_oil_ratio`. They never change the price or the equilibrium.
3. **No parallel systems.** Existing hooks are reused (§3). New state is limited to:
   - the per-republic ledger (or its status-only variant)
   - the progress variables of the megaprojects
   - two shared risk counters, which only feed existing flags (`COLDWAR_SOV_aral_disaster`, `COLDWAR_SOV_rbmk`)
4. **No date gates in `available`** (Enes, 17.10.2026).
   - Plan blocks open on `global.COLDWAR_SOV_plan`.
   - The endgame opens on cohesion and flags.
   - Historical disasters (Chernobyl, Spitak) stay events and may use dates, like the death events.
5. **MD budget.**
   - Costs 2/3/5/7; 1 point ≈ one typical MD line.
   - Buildings are always paid, through MD helpers with `skip_payment` plus a GDP share.
   - Downsides appear where they follow logically. Stability is at most +6 % outside capstones.
6. **Conflict with the 15.10 rule.** The Politburo design says "no per-republic loyalty meters; RP happens on Discord". A plan ledger is an economic number, not loyalty, but it is a per-republic counter. → Question 1. A status-only variant is described in §4-A.

---

## 2. Toolbox: what HOI4 and MD 2.0.2 give us

| Mechanic | Use here | Status |
|---|---|---|
| `shared_focus = { … }`, included per tree with `shared_focus = <root id>` | Every country completes its own copy. Main mechanic of the tree. | [OK]: MD Gulf, Commonwealth, EU; MD Russia includes 3 |
| `offset = { x y trigger = { original_tag = X } }` | One branch definition fits the SOV tree (427 wide) and the SSR host tree at different positions | [OK]: MD `gulf_shared.txt` |
| `allow_branch` by tag group | Slavic, Baltic, Caucasus, Central Asia, KAZ, MLV and Moscow sub-branches | [OK] for static tag lists. [UNSURE] how often dynamic `allow_branch` is re-checked → put subject status in `available`, not `allow_branch` |
| "One completes for all" (GCC pattern) | The first completer sets a global flag; the others `bypass` | [OK]: MD `gulf_shared.txt` |
| `joint_focus` (Saadabad type) | Keys: `joint_trigger` (who takes part), `completion_reward` (all), `completion_reward_joint_originator`, `completion_reward_joint_member`, `select_effect` (MD sets an "in progress" global flag so the AI does not start it twice), `text_icon` style. **Plan capstones only.** | [MD-PROVEN, TEST]: Benelux, Mercosur, Czechoslovakia. To test: does a member need the prerequisites? Does it interrupt the member's running focus? Does it work between overlord and subject without a faction? |
| Global variables, arrays, `every_country`, `for_each_scope_loop`, `var:` scopes | Ledger, project progress, contributor lists | [OK]: Politburo system |
| Offers as events with timeout | Every bilateral interaction | [OK]: dispatchers 100–147 |
| Politburo vote engine `COLDWAR_SOV_start_vote` | Megaproject launches, vetoes | [OK]. New vote subjects need scripted-loc lines |
| Missions (`days_mission_timeout`, `timeout_effect`) | Storming at plan end, project deadlines | [OK]: vanilla, used in MD |
| Dynamic modifiers fed by variables | `COLDWAR_SOV_gosplan_modifier`, `COLDWAR_SOV_union_modifier` (SOV); new `COLDWAR_UNI_republic_plan_modifier` (republics) | [OK] |
| Focus cost that depends on game state | e.g. cheaper if it matches the plan priority | **Not supported** (cost is static) → reward multipliers instead |
| Overlapping coordinates for foci that tag groups hide from each other | Compact layout: all six group sub-branches use the same slot, since each country sees one | [VERIFY]: hidden branches are not drawn |
| `[?var]` in focus descriptions | Show fulfilment % in the focus tooltip | [OK] in events and decisions. [VERIFY] for focus descriptions |
| `num_of_civilian_factories` / `num_of_military_factories` read into variables | "Real output" = factories built during the plan | [VERIFY] the token; the fallback is plan points only |
| `custom_cost_trigger` / `custom_cost_text` on decisions | Dynamic costs (sovereignty-parade discount) | [VERIFY]. The fallback is a variable threshold in `available` |
| Special-project progress from a republic's focus | Baikonur / Energia contribution | [VERIFY] in MD 2.0.2 |
| `set_autonomy` to `autonomy_soviet_republic_1985` in 1970 | Union Treaty signers | [VERIFY]: needs `SOV_1985_soviet_republic_autonomies_enabled` on SOV |
| `add_offsite_building` (country scope) | "All-Union enterprises" run from Moscow | [VERIFY] how they are removed again |
| Full ranking of 14 republics | Pravda table | [UNSURE]: possible with loops but costly → only top and bottom (max/min loop) plus a list in scripted loc |

**Joint foci and multiplayer.** A joint focus applies effects in other players' trees when the originator completes it. Safe use:
- only as the plan capstone, after every member has opted in through its own shared foci
- member rewards only positive and small
- no costs, no flags that change the members' options

If the test shows that a joint focus hijacks a member's running focus, fall back to a shared capstone with a global-threshold `available`.

---

## 3. Existing hooks to reuse

| Need | Existing hook |
|---|---|
| Which plan is running | `global.COLDWAR_SOV_plan` (8 → 9/10/11/12, set by event 10 in the January session of 1971/76/81/86) |
| Plan start | `COLDWAR_SOV_start_plan`: hook the ledger settlement of the old plan and the quota draft of the new plan here |
| Plan priority | Ideas `COLDWAR_SOV_plan_group_a / _group_b / _armaments / _agriculture` on SOV, set by decision + vote type 2. Republic foci that match it pay ×1.5 plan points |
| Free Union project | Event 25 (seat holders, plan start), `COLDWAR_SOV_build_union_project`, `prop_building` 1–5. Extend it to Red Banner holders and over-fulfillers |
| Union cohesion | `COLDWAR_SOV_union_cohesion` (0–100), `COLDWAR_SOV_change_union_cohesion` (temp `cohesion_delta`), four tier modifiers, event 44 below 15 |
| Money | `COLDWAR_SOV_pay_gdp_share`, `_receive_gdp_share`, `_transfer_gdp_share` (temp `COLDWAR_SOV_gdp_share`, `COLDWAR_SOV_transfer_target`) |
| Buildings | `one_random_industrial_complex`, `one_random_infrastructure`, `one_random_fossil_fuel_powerplant`, `one_random_agriculture_district`, `one_random_arms_factory` (+ `skip_payment`) |
| Pripiski | Decision `report_overfulfilment` (+50 PP, corruption, flag `COLDWAR_SOV_pripiski`, `pripiski_plan`), news 16, `COLDWAR_SOV_investigate_republic` (chance 15 % + 5 %/corruption level + 25 % pripiski ± Andropov/barons) |
| Relief / shortfall | Ideas `COLDWAR_SOV_plan_relief` / `COLDWAR_SOV_plan_shortfall` (proposal type 2) |
| Statuses | Seat, Patron in Moscow, In Disgrace, Slanderer, Defying the Politburo, cadre protection, Declaration of Sovereignty |
| National path | Popular Front, Declare Sovereignty (cohesion < 55), Referendum (event 24 → 61), Federation Council (news 28) |
| Shared disasters | Event 45 (RBMK accident, MTTH, flag `COLDWAR_SOV_rbmk`), event 46 (Dying Sea, flag `COLDWAR_SOV_aral_disaster`) |
| SOV megaproject foci (do not duplicate) | `avtovaz_the_zhiguli`, `kamaz_the_kama_truck_works`, `the_baikal_amur_mainline`, `bam_open_to_traffic`, `urengoy`, `the_tyumen_complex`, `kuzbass_and_ekibastuz`, `the_unified_energy_system`, `rbmk_reactors` / `vver_reactors`, `atoms_for_the_republics`, `the_great_siberian_dams`, `virgin_lands_renewal`, `white_gold`, `irrigate_the_desert` / `save_the_aral_sea`, `turn_the_siberian_rivers`, `the_food_programme`, `energia_buran`, `the_cotton_affair`, `the_baltic_question`, `and_the_large_scale_experiment`, `computing_centres_of_the_republics`, `the_soyuz_pipeline` (Comecon offer) |

**Rule against double rewards.**
- SOV's own focus keeps SOV's reward. The shared tree adds the republics' share and the joint completion bonus.
- SOV-only shared foci are gated with `available = { has_completed_focus = COLDWAR_SOV_<x> }`, not `prerequisite`, because a prerequisite pointing to a focus that is missing from the SSR trees breaks them.

---

## 4. Core loop proposals

### A. The Plan Ledger: quotas and fulfilment %

**Idea:** Gosplan gives every republic a quota in plan points. Points come in during the plan. The plan closes at the January session that opens the next one.

**State:**
- country variables `COLDWAR_UNI_quota`, `COLDWAR_UNI_output` (real), `COLDWAR_UNI_reported` (real + padding) and `COLDWAR_UNI_fulfil` (%)
- `global.COLDWAR_UNI_union_fulfil`

**Quota tiers** (plan points over 5 years):
| Tier | Points |
|---|---|
| Low | 8 |
| Standard | 12 |
| Taut | 16 |
| Counter-plan | +4 on top |

**Point sources:**
- plan foci: 2–4 each, ×1.5 if they match SOV's plan priority
- megaproject contributions: +2
- decisions: Storming, Tolkachi
- [VERIFY] real construction: +1 per civilian or military factory gained since the plan started, from a snapshot taken in `COLDWAR_SOV_start_plan`
- pripiski: +3 reported, 0 real

**Settlement** (in `COLDWAR_SOV_start_plan`, before the new plan):
1. **Audit.** Every republic with `COLDWAR_SOV_pripiski` rolls `COLDWAR_SOV_investigate_republic`, but only if SOV has an audit flag (People's Control focus, Andropov's discipline, Romanov's iron discipline).
   - If exposed: `reported = output`, existing disgrace effects, cohesion −1.
2. **Bands on `reported`:**

| Band | Name | Effects |
|---|---|---|
| < 80 % | Plan Failed | Timed idea `COLDWAR_UNI_plan_failed` (2 years: PP −10 %, stability −3 %). The republic may ask for Plan Relief (existing). |
| 80–99 % | Nearly fulfilled | Nothing. |
| 100–109 % | Plan Fulfilled | +1 line on `COLDWAR_UNI_republic_plan_modifier`, +50 PP. |
| ≥ 110 % | Over-Fulfilled | +2 lines, a Union-project ticket (event 25 even without a seat), Red Banner candidate. |

3. **Ratchet ("planning from the achieved level").** Over-fulfilling raises the next plan's base quota by one tier. The counter-play is the decision "Keep Reserves in Hand": report only 101 %, give up the over-fulfilment band and keep the old tier.
4. **SOV** is paid by union fulfilment, the average of the republics plus an RSFSR term from SOV's own plan foci, weight ×3:
   - ≥ 100 %: gosplan modifier line + cohesion +3
   - < 85 %: `COLDWAR_SOV_plan_shortfall` + cohesion −3

**News:** "The Results of the Ninth Five-Year Plan", one line per republic. Same pattern as `[UKR.COLDWAR_SOV_GetVoteLine]`.

**AI floor:** AI republics get +2 points per year (hidden), so an AI-heavy game does not drag the union average down.

**Status-only variant (keeps the 15.10 rule):**
- No numbers. Every completed plan focus of the running plan sets a flag. Counting the flags gives three statuses: *Behind the Plan* (0–1), *On Plan* (2–3), *Over-Fulfilled* (4+).
- The status shows in the vote lines and the news. Pripiski raise the status by one.
- Same settlement, less code, coarser.

**Pros:**
- One number drives everything: rewards, ranking, audits, the SOV result.
- Historically exact: quota, ratchet, pripiski, storming.

**Cons:**
- A new per-republic counter (question 1).
- The settlement code is the biggest new script.

### B. Socialist Competition: Red Banner and ranking

**Idea:** Republics join the all-Union socialist competition (*sotsialisticheskoe sorevnovanie*). At each January session the leader in output relative to quota gets the **Transferable Red Banner of the Central Committee**:
- timed idea, 1 year: stability +3 %, construction +5 %
- the next Union project ticket

The last place receives a **People's Control inspection** event, where the republic chooses:
- **Open the books:** lose pripiski padding, safe.
- **Stonewall:** 50 PP, audit chance +15 %.
- **"The inspectors are our guests":** corruption +1, audit chance −10 %. This is the Uzbek/Azerbaijani way.

**Challenges.** A republic may challenge another to a one-plan duel (offer). Winner: Banner points and +25 PP. Loser: −25 PP. Declining costs nothing.

**SOV side:** "Award the Banner" ceremonies give cohesion +1 if at least 3 republics compete.

**Pros:**
- Ideal for multiplayer: visible, competitive, cheap to understand.

**Cons:**
- Needs a measurable score, so it is either built on A or reduced to counting completed foci.
- Can feel like a minigame if A is missing.

### C. Gosplan Bargaining: quota against investment

**Idea:** At plan start every republic receives the event **"The Draft Plan from Gosplan"** (10-day timeout → accept):
1. **Accept the targets:** standard tier.
2. **Argue the targets down:** −1 tier, −50 PP, flag *Under Scrutiny* (audit chance +15 % for this plan).
3. **Ask for capital investment:** +1 tier. This sends a request to SOV, which decides in its own event:
   - **Approve:** SOV pays 0.3 % of its GDP to the republic at that moment, through `COLDWAR_SOV_transfer_gdp_share`. The republic is bound to the higher tier.
   - **Refuse:** the tier goes back to standard.
4. **Adopt a counter-plan** (*vstrechny plan*): +1 tier, rewards ×1.5 at settlement; failure brings *Broken Pledge*.

**SOV levers:**
- Once per plan, the decision **"A Taut Plan" / "A Realistic Plan"**: all quotas +1 tier with SOV's reward ×1.25, or no change.
- A targeted decision **"Revise the Quota of [FROM]"**: an offer the republic can refuse, at a cost of −1 cohesion.

**Pros:**
- Pure negotiation, ideal for a multiplayer group that plays out the politics on Discord.
- Reuses the investment money helper.

**Cons:**
- Meaningless without A, because tiers need settling.
- One more event per republic per plan (14 × 4 over the game, fine).

### D. The Union Projects Pool: megaprojects funded together

**Idea:** SOV launches a megaproject, through its own existing focus plus a Politburo vote for the contested ones (Siberian rivers, Ignalina unit 3, Daugavpils HPP). This opens a contribution focus in every republic's shared tree.

**Contributions:**
- GDP share 0.1–0.3 %, Komsomol brigades (manpower) or PP
- added to `global.COLDWAR_UNI_proj_<key>` (0–100)
- the contributor is added to `global.COLDWAR_UNI_proj_<key>_members`

**Completion:** progress ≥ 100 **and** at least N members (2–6 depending on the project) fire a completion event for all members.
- The host gets the main asset.
- Every member gets a share: dynamic line, opinion, +2 plan points.
- SOV gets its union effect and cohesion.

**Cancellation:** if SOV shelves a project (decision, cohesion −2), contributors get 50 % back.

**Pros:**
- The richest content. Historically the Union really ran on "all-Union shock constructions" with republican sponsors.
- Natural cooperation between players.

**Cons:**
- Needs AI contribution logic (treasury, historical weight).
- Many projects means many variables (fine).

### E. (Smaller alternative) Inter-republican deliveries

**Idea:** Bilateral supply contracts as offers:
- Belarusian tractors for Kazakh grain
- Turkmen gas for Ukrainian pipe
- Estonian oil-shale power for Latvia

Both sides pay a little and get a dynamic line while the contract runs.

**Ending a contract:** a decision, available from plan XII on ("the war of deliveries" of 1990–91).
- Both lose the bonus.
- The breaker gets *Unreliable Supplier* (opinion, −1 cohesion).
- No malus is ever imposed on the partner beyond losing the deal it agreed to.

**Pros:**
- Republic-to-republic play without Moscow.

**Cons:**
- Pure bilateral, so it does not touch the plan unless linked to A (+1 point per running contract).

### Recommendation

**A + C as the spine, D as the content, B as the presentation, E as an optional XII-era add-on.**

- If the author keeps the no-meters rule, use A in its status-only variant. B then ranks by status plus completed foci, and C changes the status thresholds instead of the tiers.
- All four touch only existing global systems:
  - plan variable
  - priority ideas
  - event 25
  - cohesion
  - pripiski
  - votes
  - GDP-share money

---

## 5. Five-Year Plan branches

Each block hangs from the trunk, not from the previous plan, so a republic that joins late starts at the running plan.

**Gating:** plan foci are `available` only while `global.COLDWAR_SOV_plan` = their plan. Afterwards they cannot be taken. There is no bypass, so no free completion.

**Republic types:**
- Slavic core: UKR, BLR
- Baltics: EST, LAT, LIT
- Caucasus: ARM, AZE, GEO
- Central Asia: UZB, TAJ, KYR, TRK
- KAZ
- MLV

Moscow (SOV only) has its own sub-branch.

### IX Five-Year Plan, 1971–75: "The Plan of the People's Welfare"

**Frame:**
- Adopted at the XXIV Congress (1971).
- The first plan in which Group B (consumer goods) was planned to grow faster than Group A. It missed that.
- AvtoVAZ in full production, KamAZ under construction.
- Non-Black-Earth programme (1974), BAM decision (1974).
- The 1972 harvest failure.
- The Union's 50th jubilee (Dec 1972): every union republic received the new Order of Friendship of Peoples.

**Union-wide foci (all republics and SOV):**
- **Directives of the Ninth Plan** (root of the block, quota event of loop C)
- **Fifty Years of the Union**
  - Republic: cohesion +1, idea "Order of Friendship of Peoples" (stability +2 %).
  - SOV: news, cohesion +2 once.
- **Socialist Obligations** (enter the competition, B)
- **The Harvest Battle.** Send combine operators and students to the harvest.
  - Contribution: manpower and PP.
  - Agrarian republics (KAZ, UKR, MLV) receive points; senders get +1 point.
  - Ties in with SOV's "The Harvest of 1972".

| Group | Gives | Gets |
|---|---|---|
| Slavic core | UKR **Donbass and Kryvbas** (coal and iron: Group A points ×1.5 with Group A priority). BLR **The Assembly Shop of the Union** (MAZ/BelAZ/MTZ: unlocks the delivery contract "Tractors for the Virgin Lands" with KAZ). BLR **Soligorsk Potash** (fertiliser: +1 point to every agrarian republic that signs the fertiliser contract) | Civ/arms factory (paid), opinion, plan points |
| Baltics | **The Soviet West** consumer branch: LAT **VEF and RAF** (radios, minibuses: Group B ×1.5). EST **Narva Oil Shale** (power plant; contract "Power for the North-West" with SOV). LAT **Ventspils Oil Terminal** (export infrastructure; oil ratio read only) | Consumer-goods relief, trade opinion, power |
| Caucasus | AZE **Oil from the Sea: Neft Daşları** (resource and infrastructure, not price). GEO **The Abasha Experiment** (agrarian incentive pay: agriculture line, corruption risk). ARM **The Yerevan Computer Institute** (research line, link to SOV "Computing Centres of the Republics") | Research, oil output, agriculture |
| Central Asia | UZB **Six Million Tons of White Gold** (example 4). TAJ **Nurek Dam** (power; first unit 1972, completed 1980). TRK **Shatlyk Gas** (gas export to the Centre, SOV export line). Group **The Hungry Steppe** (irrigation: agriculture district, Aral strain +1) | Big agrarian points, power, money, at the cost of the Aral |
| KAZ | **The Billion Poods** (Virgin Lands grain: points ×1.5 with Food priority). **Temirtau: the Kazakh Magnitka** (steel). **Leninsk: Baikonur's City** (supply town; link to SOV space foci) | Grain, steel, space link |
| MLV | **The Garden of the Union** (fruit, wine, tobacco: Group B points). **Agro-Industrial Integration** (Bodiul's inter-farm associations, promoted as a model: agriculture and production-efficiency line). **The Moldavian GRES** (power exported to the Balkans: contract offer to BUL/ROM, who decide) | Agriculture, power exports |
| Moscow (SOV) | **Gosplan Sets the Quotas** (unlocks loop C levers). **Capital Investments for the Republics** (SOV pays 0.5 % GDP once; every republic below 80 % at that moment gets a building, `skip_payment`). **KamAZ: Builders from Every Republic** (opens project D "KamAZ") | Gosplan lines, cohesion |

**Capstone (joint, when `global.COLDWAR_UNI_union_fulfil` ≥ 95 %):** **The Ninth Plan Fulfilled**
- all members: +25 PP and +1 stability
- the originator (SOV or the top republic): +50 PP

### X Five-Year Plan, 1976–80: "The Plan of Efficiency and Quality"

**Frame:**
- XXV Congress; the State Quality Mark; the Shchekino method.
- Atommash, Sayano-Shushenskaya, Kansk-Achinsk.
- BAM at full pace; KamAZ's first trucks (1976).
- The 1977 Constitution (Art. 72, the right to secede) and the 1978 republican constitutions. The Georgian language protest of 14 April 1978 kept Georgian as state language.
- The 1980 Olympics: sailing in Tallinn; football in Kyiv, Minsk and Leningrad.

**Union-wide foci:**
- **Directives of the Tenth Plan**
- **The State Quality Mark.** Plan points count ×1.2 for a year; consumer goods +1 % (higher standards cost).
- **Republican Constitutions.** Republic chooses one:
  - "Our Language in the Constitution": stability +3 %, cohesion −1, party pop of the national party +2.
  - "The Union Text": cohesion +1, PP +25.
- **The Olympic Year.** SOV focus "Olympic Venues in the Republics" sends offers to EST, UKR and BLR. They accept and pay a small GDP share; they receive infrastructure, stability and opinion.

| Group | Gives | Gets |
|---|---|---|
| Slavic core | UKR **Atoms for Ukraine: Chernobyl and the South** (RBMK: `global.COLDWAR_UNI_rbmk_units` +1). UKR **Yuzhmash** (only with the defence priority: arms factory, points ×1.5). BLR **Novopolotsk and Mozyr** (refineries on the Druzhba line) | Energy, defence points, the reactor risk |
| Baltics | EST **The Olympic Regatta** (if the venue offer was accepted: hotel, TV tower, infrastructure, stability). LAT **Trains from Riga** (Riga Wagon Works: infrastructure exports, +2 points to any republic that orders through a contract). LIT **Ignalina** (RBMK-1500: power, `rbmk_units` +1; contract to export power to BLR and LAT) | Showcase, power, the reactor risk |
| Caucasus | GEO **The Inguri Dam** (271 m arch dam spanning Georgia proper and Abkhazia: power, megaproject D with contributors). ARM **Metsamor** (NPP in an earthquake zone: power, sets flag `seismic_risk`, which makes Spitak worse later). AZE **Aliyev's Industrial Drive** (consumer plants, deep-water platform yard; Azerbaijan's reports were famously glowing: the pripiski decision is +1 point cheaper in PP) | Power, consumer industry |
| Central Asia | KYR **Toktogul** (Naryn dam; upstream water power, key for the water-sharing offer in XII). TAJ **TadAZ: Aluminium from Nurek Power** (needs `nurek` completed or a power contract with KYR: aluminium resource). TRK **Dauletabad Gas** and **The Karakum Canal Extended** (Aral strain +1). UZB **Navoi and Muruntau Gold** (treasury, scaled modestly) | Resources, irrigation, money |
| KAZ | **Ekibastuz: Coal for the Grid** (power, opens project D "Ekibastuz–Centre"). **Mangyshlak and Tengiz** (oil field, discovered 1979; output only) | Energy and oil output |
| MLV | **Agro-Industrial Complexes** (follows integration: production efficiency). **Wine for the Union** (consumer line; exposed to the 1985 anti-alcohol campaign later) | Consumer and agrarian points |
| Moscow (SOV) | **Atommash** (reactor vessel plant; offers reactor kits to UKR, LIT, ARM, who accept and pay). **Komsomol Shock Construction: BAM** (opens project D BAM, example 10). **The People's Control** (unlocks audits at settlement and the targeted decision "Send the Inspectors to [FROM]", an event to the republic with the three choices of loop B) | Audit power, energy, cohesion |

**Capstone (joint):** **Efficiency and Quality**, at ≥ 95 % union fulfilment and at least one Quality Mark focus in 7 republics.

### XI Five-Year Plan, 1981–85: "The Plan of Intensification"

**Frame:**
- The Food Programme (May 1982 plenum).
- Urengoy–Pomary–Uzhgorod (1982–84), built despite the 1982 Western pipeline sanctions.
- Andropov's discipline campaign (1983).
- The Large-Scale Economic Experiment (1984). It ran in Union ministries plus three republican ones: Ukrainian light industry, Belarusian food industry, Lithuanian local industry.
- The cotton affair investigations (from 1983).
- BAM's golden link (1984) and the Ekibastuz 1150 kV line.

**Union-wide foci:**
- **Directives of the Eleventh Plan**
- **The Food Programme in the Republics.** With SOV's Food priority, agrarian points ×1.5. Every republic chooses:
  - "Feed the Cities": food production line.
  - "Feed Ourselves First": stability, −1 point.
- **Discipline at the Workplace.** Available while SOV has the Andropov discipline flag.
  - Production efficiency line.
  - The republic's pripiski are audited at once, using the existing cotton-affair hook.
- **The Large-Scale Economic Experiment.** Joint, threshold 3 republics; historically UKR, BLR and LIT, but any 3 can take part.
  - Participants: "Enterprise Autonomy" line (production efficiency +, consumer goods −).
  - SOV: Gosplan line. It unlocks the XII khozraschet branch early.
- **Urengoy–Pomary–Uzhgorod** (contribution, example 5).

| Group | Gives | Gets |
|---|---|---|
| Slavic core | UKR **The Western End: Uzhgorod** (host of the pipeline: transit line once the project completes). BLR **The Food Industry Experiment** (joins the experiment threshold) | Transit income, reform lines |
| Baltics | LIT **Local Industry on Khozraschet** (joins the experiment). EST **Phosphorite for the Food Programme**: fertiliser, points ×1.5 with Food. It sets the flag `phosphorite_mines`, which drives the 1987 "Phosphorite War" protest in XII. LIT **Mažeikiai Refinery** (1980: refinery). LIT **The Klaipėda–Mukran Ferry** (1986: offer to the GDR player, who decides: trade opinion for both) | Fertiliser, ports, a delayed protest |
| Caucasus | GEO **The Tsekhoviki** (shadow workshops; illegal consumer production). Choose: <br>• "Look the Other Way": consumer goods −2 %, treasury +, corruption +1, audit chance +20 %. <br>• "Shevardnadze's Clean Hands": corruption −1, stability −2 %. <br>ARM **The Arpa–Sevan Tunnel** (1981: rescue Lake Sevan; agriculture, stability). AZE **A Call to Moscow**: if the existing promotion event moved Aliyev to Moscow, Azerbaijan gets Patron in Moscow and a project ticket | Consumer goods vs corruption, ecology |
| Central Asia | UZB **The Cotton Affair: Open the Books or Close Ranks** (only with pripiski or at least 2 cotton foci). <br>• Open: lose the padded points, corruption −2, cohesion +1, the First Secretary is replaced. <br>• Close ranks: +25 PP, cadre protection if a seat holder; the next audit chance +30 %. <br>TAJ **Rogun** (megaproject: needs 2 contributors). TRK **Gas for the Centre** (Central Asia–Centre pipeline: SOV export line). Group **Siberian Water for Central Asia**: lobby focus. It puts SOV's "Turn the Siberian Rivers" to a Politburo vote, where republican votes count. If it passes, project D "Sibaral" opens | Cotton money vs exposure, the river question |
| KAZ | **Ekibastuz–Centre: The 1150 kV Line** (project D host). **Kazakh Grain for the Food Programme** | Energy and grain |
| MLV | **The Garden Feeds the Union** (Food Programme deliveries: points, a contract with SOV) | Agrarian points |
| Moscow (SOV) | **The Food Programme Commission** (unlocks the Food delivery contracts). **Andropov's Inspectors** (with the discipline flag: audits cost 25 instead of 50 PP). **Answer the Pipeline Sanctions** (if a Western player sanctioned SOV through the Imperia sanctions, contributors get "Pipe from Our Own Mills": build speed). | Food, audits |

**Capstone (joint):** **Intensification**, at ≥ 90 % union fulfilment and with the pipeline completed.

### XII Five-Year Plan, 1986–90: "Acceleration" → perestroika

**Frame:**
- Uskorenie; the anti-alcohol campaign (May 1985). Vineyards were cut down in Moldova, Georgia, Armenia and Azerbaijan.
- Chernobyl (26 April 1986). Liquidators came from every republic; Belarus received most of the fallout.
- The Siberian river diversion was stopped (Aug 1986).
- Gospriyomka (1987), the Law on State Enterprise (1987), the Law on Cooperatives (1988).
- IME, "Self-Managing Estonia" (Sept 1987).
- Environmental protest movements:
  - the Phosphorite War (1987)
  - Daugavpils HPP stopped (1987)
  - Nevada–Semipalatinsk (1989)
  - Ignalina unit 3 halted
  - Metsamor closed (1989)
- The Spitak earthquake (7 Dec 1988).
- The Union law on the economic independence of the three Baltic republics (27 Nov 1989).
- Republican khozraschet (1990).

**Union-wide foci:**
- **Directives of the Twelfth Plan**
- **Acceleration.** Production speed +5 % and points ×1.2; at settlement, a stability −2 % hangover.
- **The Dry Law in the Republics.** Choose:
  - "Uproot the Vineyards": wine republics lose their wine line; cohesion +1.
  - "Spare Our Vines": keep the line; a pripiski-like flag (audit chance +15 %).
- **Gospriyomka: State Acceptance.** Real output only: pripiski padding no longer counts this plan; points from real construction ×1.5.
- **The Liquidators** (after event 45; solidarity, see §7).
- **Republican Khozraschet** (the bridge to §8).

| Group | Gives | Gets |
|---|---|---|
| Slavic core | UKR **After Chernobyl** (if the accident hit: the zone, a stability choice, contributions from liquidators). BLR **The Gomel Zone** (the same for Belarus: health cost, donor offers) | Solidarity, recovery |
| Baltics | EST **Self-Managing Estonia (IME)** (example 7). EST **The Phosphorite War** (needs `phosphorite_mines`: national party +5 %, cohesion −2, stability +2 %; ends the fertiliser line). LAT **Stop the Daugavpils Dam** (ecology: the same pattern). LIT **No Third Unit at Ignalina** (offer to SOV: approve → `rbmk_units` −1; refuse → national party +5 %) | National mobilisation, the khozraschet path |
| Caucasus | ARM **Rebuild Spitak** (receiver side, example 8). ARM **Close Metsamor** (power −, stability +, `rbmk`/`seismic` risk ended). GEO **The Inguri Completed** (if the project finished: power, +2 points). AZE and ARM get no Karabakh foci here (they stay in the SOV tree) | Recovery, ecology |
| Central Asia | Group **The Water Accord** (upstream KYR/TAJ ↔ downstream UZB/KAZ/TRK: summer releases for cotton against energy or money; offer, both decide). UZB **The Aral Reckoning** (with Aral strain ≥ 4: health cost, stability −; choice "Less Cotton": points −, strain −2). Group **Rehabilitate the Cadres**: reverses "In Disgrace" from the cotton affair. Historically, the Gdlyan–Ivanov investigations themselves became a scandal | Water, ecology, cadres |
| KAZ | **Zheltoqsan** (if SOV replaced the First Secretary through the existing promotion or kompromat paths: stability −, national party +). **Nevada–Semipalatinsk** (petition to SOV: close the test site; SOV decides; accept → cohesion +3, SOV the_military −) | National movement |
| MLV | **The Language of the Republic** (1989 language law: national party +5, cohesion −2, stability +2 %). **Spare the Vineyards** (see Dry Law) | National path |
| Moscow (SOV) | **The Law on State Enterprise** (Gosplan line, ledger quotas −1 tier for everyone: "orders, not targets"). **Republican Cost Accounting** (sends the khozraschet offer, §8). **Stop the River Reversal** (cancels Sibaral; CA republics lose the project, contributors refunded 50 %; Friends of Baikal +) | Reform lines, endgame entry |

**Capstone (joint):** **The Twelfth Plan Fulfilled** (≥ 90 %), or a shared non-joint focus **The Plan Collapses** (< 70 %): every republic chooses "Ration and Endure" or "Our Goods Stay Here" (opens the delivery-war decisions of E).

**Ambitious option: alt-history XIII Five-Year Plan (1991–95).** It opens only if cohesion ≥ 40 and the Union Treaty is signed (§8). It is a "Union of Sovereign States" plan with voluntary quotas.

---

## 6. Megaproject catalogue (loop D)

| Project | Plan | SOV hook focus | Host | Contributors / N | Completion reward | Risk / downside |
|---|---|---|---|---|---|---|
| KamAZ | IX | `kamaz_the_kama_truck_works` | SOV | any / 4 brigades | SOV truck line; contributors "KamAZ Trucks" (infrastructure build speed) | Brigade manpower away for 1 year |
| Virgin Lands harvest brigades | IX–XI (yearly) | `virgin_lands_renewal` | KAZ | UKR, BLR, Baltics / 2 | KAZ grain points, senders +1 point, opinion | Senders' production −2 % during harvest month |
| BAM | IX–XI | `the_baikal_amur_mainline`, `bam_open_to_traffic` | SOV | any / 6 | Golden Link: SOV supply line; members get a station named after the republic (news) + PP + cohesion | Permafrost overrun event: SOV pays more or contributors may withdraw (refund 50 %) |
| Nurek and the Vakhsh cascade | IX–X | — | TAJ | UZB, TRK (downstream) / 1 | Power for TAJ; members get a power contract | Rogun follows |
| Inguri dam | X | — | GEO | ARM, AZE / 1 | Power, Caucasus grid line | Abkhazian tension flavour event |
| Kursk Magnetic Anomaly / OEMK | X | `steel_cities` | SOV | UKR, BLR / 2 | Steel resource for SOV, members a steel contract | — |
| Atoms for the republics (RBMK) | X | `rbmk_reactors`, `atoms_for_the_republics` | UKR, LIT, (ARM) | — | Power per host | `global.COLDWAR_UNI_rbmk_units` +1 each → MTTH of event 45 shortened ×0.85 per unit [VERIFY: MTTH modifier on a global variable] |
| Urengoy–Pomary–Uzhgorod | XI | `urengoy` | SOV + UKR | any / 3 incl. UKR | SOV gas export line; UKR transit; members energy | Sanctions by Western players remain their own choice |
| Ekibastuz–Centre 1150 kV | XI | `kuzbass_and_ekibastuz`, `the_unified_energy_system` | KAZ + SOV | / 2 | Unified grid line for KAZ and SOV | — |
| Central Asian energy ring | X–XI | — | TAJ, KYR, KAZ | needs Nurek + Toktogul + Ekibastuz (3 hosts) | "Unified Energy System of Central Asia": power and stability for all 5 CA republics | Upstream/downstream water quarrel (XII accord) |
| Sibaral (Siberian rivers) | XI–XII | `turn_the_siberian_rivers` + Politburo vote | SOV | UZB, KAZ, TRK, TAJ, KYR / 3 | Irrigation for CA, Aral strain −3 | Greens and Russian nationalists (party pop), cohesion −2 in Slavic and Baltic republics' news; SOV can stop it (XII) |
| Baikonur and Energia | XI–XII | `energia_buran` | KAZ | UKR (Yuzhmash), any / 2 | Special-project progress [VERIFY]; KAZ "Leninsk" line | Expensive |
| Baltic gateway: Muuga, Ventspils, Klaipėda | XI–XII | — | EST, LAT, LIT | / 2 of 3 hosts | Trade line for the Baltics, SOV export line | Raises "Soviet West" visibility (national pop +1) |
| Spitak reconstruction | XII (event) | — | ARM | all / 5 donors | ARM buildings and stability, donors cohesion | — |
| Chernobyl liquidation | XII (event 45) | — | UKR / BLR | all / 4 | Zone recovery for hosts, donors "Liquidators" honour | Donor manpower and health cost |

**Funding model.**
- SOV pays the launch: 0.5–1.0 % of its GDP, in its own focus or decision.
- Contributors pay 0.1–0.3 % of their GDP or a brigade (500–3,000 manpower, returned after 365 days by a delayed event).
- Everything is paid at contribution. Rewards come only at completion.

---

## 7. Interactions between players

| # | Interaction | Who → who | How | Downside that makes sense |
|---|---|---|---|---|
| 1 | Draft quota | SOV (Gosplan) → each republic | Event at plan start (loop C) | Arguing down: −50 PP and Under Scrutiny |
| 2 | Investment request | Republic → SOV | Offer; SOV pays at approval | Republic bound to a higher tier (ratchet) |
| 3 | Revise a quota | SOV → republic | Targeted decision, offer | SOV −1 cohesion if refused; republic −PP if accepted under protest |
| 4 | Plan relief | Republic → SOV | Existing proposal type 2 | SOV `plan_shortfall` |
| 5 | Socialist competition challenge | Republic → republic | Offer, duel for one plan | Loser −25 PP; declining free |
| 6 | Delivery contract | Republic ↔ republic, or with SOV | Offer, runs until ended | Breaking: both lose the line; the breaker gets *Unreliable Supplier* |
| 7 | Megaproject contribution | Anyone → project | Shared focus, global progress, threshold N | Money or manpower spent even if the project stalls (50 % refund only if SOV cancels) |
| 8 | Komsomol brigades | Republic → host | Decision or focus, manpower out, back after 1 year | Production −2 % while away |
| 9 | Audit (People's Control) | SOV → republic | Targeted decision → republic event (open / stonewall / guests) | SOV −PP; cohesion −1 if nothing is found |
| 10 | Kompromat on plan fraud | Republic → SOV about another seat holder | Existing kompromat, +25 % with pripiski | Existing Slanderer status |
| 11 | Politburo veto on megaprojects | SOV launch → vote | `COLDWAR_SOV_start_vote` with new subjects | Failed vote: project shelved; overriding the vote: Defying the Politburo |
| 12 | Site bargaining | Seat holder → SOV | Extension of event 25: the seat holder can bid to host the next Union plant (aluminium, refinery) | A seat holder who wins may lose the next congress seat vote (opinion of the others) |
| 13 | Cadre exchange | Republic ↔ republic / SOV | Offer "Send Specialists": the sender pays PP and a little manpower; the receiver gets research or construction speed | The sender's national party −1 (brain drain), the receiver's national party +1 (newcomers) |
| 14 | Water accord | Upstream (KYR, TAJ) ↔ downstream (UZB, KAZ, TRK) | Offer each summer or once per plan: releases for cotton against energy or money | Refusal: downstream −points, upstream +power |
| 15 | Disaster solidarity | Any → stricken republic | Shared focus "Send Aid": the receiver accepts per donor | The donor pays at acceptance |
| 16 | Joint capstone | All members | Joint focus at threshold | None (rewards only) |
| 17 | Patron networks | Existing patronage event 23 | Unchanged; the ledger adds "client's project counts +1 point for the patron" | — |

---

## 8. Endgame branch: "A New Union?" (offers only)

**Gating:** `global.COLDWAR_SOV_plan` ≥ 12, **or** cohesion < 50, **or** the Federation Council flag. There is no date gate.

| Focus / step | Who | Mechanics | Historical anchor |
|---|---|---|---|
| **Republican Cost Accounting** | SOV sends; every republic decides | Accept → idea *Republican Khozraschet*: tax +5 %, stability +2 %, no more free event-25 projects, no plan relief. SOV: tax −1 % per signer (union modifier), cohesion +2 per signer | Regional khozraschet, 1989–90 |
| **The Economic Independence of the Republic** | Republic (Baltics first; others once 1 Baltic signer exists) | Offer to SOV: approve → stronger khozraschet line; refuse → national party +5 %, cohesion −2 | IME 1987; Union law of 27 Nov 1989 |
| **The Parade of Sovereignties** | Hook on the existing "Declare Sovereignty" decision | `global.COLDWAR_UNI_sovereign_count` +1 per declaration. The threshold `global.COLDWAR_UNI_sovereignty_threshold` = 55 + 5 × count (variable-vs-variable check), so each declaration makes the next easier. Nothing is applied to other players | 1988–90 |
| **The 500 Days** | SOV focus | Offers an economic union to all republics. Full reward (SOV Gosplan lines, cohesion floor) only with ≥ 8 signers; otherwise a half reward | Shatalin–Yavlinsky, Aug–Sept 1990 |
| **The Union Referendum** | SOV focus | Each republic chooses in its own event: hold it (cohesion +2, stability −1) or boycott (national party +3). The result news counts the boycotts | 17 March 1991; 6 republics boycotted |
| **Draft the Union Treaty** → **Sign the Union Treaty** | SOV offers; each republic decides | Signer: *Sovereign Republic of the Union* (stability +5 %, PP +10 %), cohesion +3. At ≥ 9 signers: SOV capstone **The Union of Sovereign States** (cohesion floor 40, union modifier lines, unlocks the alt-hist XIII plan). With fewer: *The Treaty Fails* (cohesion −5). Non-signers keep the existing referendum path; nothing is forced | Novo-Ogaryovo "9+1", 23 April 1991 |
| **The Economic Community** | Any republic, also independent ones, and SOV | Multi-offer: signers get a trade line and opinion; ≥ 6 signers → "Single Economic Space" line for all | Treaty on the Economic Community, Alma-Ata, 18 Oct 1991 (8 republics) |
| **Regional associations** | Baltic Council (EST, LAT, LIT); Central Asian cooperation (5 CA republics) | Offers inside the group; signers get group lines. No military content, no alliance | Baltic Council 1990; Alma-Ata meeting of CA leaders, June 1990 |
| **The Inter-Republican Economic Committee** | SOV, after a failed treaty | Coordination offer to every republic: a consultative body with small trade lines; SOV gets cohesion decay −1/month halved | Committee of 1991 |

The endgame works for independent ex-republics as well. Its `available` checks `original_tag` groups, not subject status.

---

## 9. Layout, size and cost

```
row 0  [The Plan and the Union] ---------------------------------------------------------- trunk
          |                 |               |               |               |              |
       [Socialist       [IX block]      [X block]       [XI block]     [XII block]     [A New Union?]
        Competition]        |                                                           (endgame)
        (6 foci)   Directives (2-3)                                                       (12-14 foci)
                     /     |       \
          union-wide   GROUP SLOT    project
          (3 foci)     (one of 6 groups or Moscow,     contributions
                        same x, hidden by allow_branch) (2-4 foci)
                           |
                     [Plan capstone, joint]
```

- **Plan blocks** stand side by side under the trunk; they do not chain. Each block is about 9 columns wide:
  - union-wide column
  - group slot (2–3 columns)
  - project column
- **Group slot trick** [VERIFY]: the six republic-type sub-branches and the Moscow sub-branch share the same coordinates. Each country sees exactly one of them. This keeps the width at about 9 instead of about 40 columns per plan. If overlapping is refused, use `offset` per group so each host sees its group at the same place.
- **Total width:** about 60–70 columns, 8–9 rows (MD style: wide and shallow; every block at row 0/1).
- **Placement:**
  - SOV: at the right end of `COLDWAR_SOV_1970_focus` (x ≈ 430+), with an 11th shortcut "The Union Plan".
  - SSRs: `offset` into the host tree (question 2).

**Focus count (rough):**

| Block | Defined | Visible to one SSR | Visible to SOV |
|---|---|---|---|
| Trunk | 3 | 3 | 3 |
| Socialist competition | 6 | 5 | 3 |
| Per plan: directives 1 + union-wide 3–4 + group foci (6 groups × 3–4, Moscow 3–4) + projects 3 + capstone 1 | ≈ 32 | ≈ 11 | ≈ 11 |
| × 4 plans | ≈ 128 | ≈ 44 | ≈ 44 |
| Megaproject launches (SOV) | 8 | 0 | 8 |
| Endgame | 14 | 9 | 7 |
| **Total** | **≈ 160** | **≈ 60** | **≈ 65** |

**Costs (MD 2/3/5/7; 1 cost = 7 days):**
- trunk and directives: 2
- union-wide and most republic foci: 3
- big builds and contributions: 5
- capstones and treaties: 7

A republic's visible plan block (about 11 foci, average cost 3.5) takes about 270 days of a 1,825-day plan, roughly 15 %. SSR players keep most of their focus time for their own tree.

**Search filters:** `FOCUS_FILTER_UNION_PLAN` (new), plus the standard `FOCUS_FILTER_ECONOMY`, `FOCUS_FILTER_INDUSTRY` and `FOCUS_FILTER_POLITICAL`.

**Files (if approved):**
- `common/national_focus/COLDWAR_UNI_1970_shared.txt`
- `common/scripted_effects/COLDWAR_UNI_1970_scripted_effects.txt` (ledger, settlement, projects)
- events namespace `COLDWAR_UNI`
- a decision category "The Republic and the Plan" (SSR)
- additions to the existing SOV "Five-Year Plans" category
- `localisation/english/COLDWAR_UNI_1970_l_english.yml`

These would be generated, like SOV (extend `sovgen` or create a sibling generator).

---

## 10. Ten example foci

The effects are written in plain words. "Republic" means any union republic completing its own copy; "SOV" means the Soviet Union's copy.

### 1. The Plan and the Union
- **ID:** `COLDWAR_UNI_the_plan_and_the_union` · **Cost:** 2 · **Block:** trunk, row 0
- **Prerequisites:** none (shared root). **Allow branch:** SOV or one of the 14 SSR tags (static).
- **Available:** SOV, or `COLDWAR_SOV_is_union_republic = yes`; global flag `COLDWAR_SOV_politburo_system`.
- **Effects:**
  - Republic:
    - opens the decision category "The Republic and the Plan" (Storming, Keep Reserves in Hand, Send Specialists, contracts)
    - adds an empty `COLDWAR_UNI_republic_plan_modifier`
    - sets the standard quota tier for the running plan
    - +25 PP
  - SOV:
    - adds the ledger decisions to the existing "Five-Year Plans" category
    - first completion only (global flag): cohesion +1
- **AI:** base 100; always the first shared focus.

### 2. Directives of the Ninth Plan
- **ID:** `COLDWAR_UNI_ix_directives` · **Cost:** 2 · **Prerequisites:** focus 1.
- **Available:** `global.COLDWAR_SOV_plan = 9`; union republic or SOV.
- **Effects:**
  - Republic:
    - receives "The Draft Plan from Gosplan" (loop C) if it has not yet answered this plan
    - +1 plan point
    - tooltip: points ×1.5 for foci matching SOV's priority, read from the `COLDWAR_SOV_plan_*` idea on SOV
  - SOV:
    - unlocks "A Taut Plan / A Realistic Plan" (once per plan)
    - unlocks "Revise the Quota of [FROM]"
- **AI:** base 50; +50 while the plan is running.

### 3. The Counter-Plan
- **ID:** `COLDWAR_UNI_the_counter_plan` · **Cost:** 3 · **Prerequisites:** the running plan's directives (OR across the four blocks).
- **Available:**
  - union republic
  - no `COLDWAR_SOV_plan_relief`
  - not *Under Scrutiny* this plan
  - stability ≥ 50 %
- **Effects:**
  - Now:
    - quota +1 tier for the running plan
    - dynamic line "Socialist Obligations": production speed +5 % and consumer goods +2 % until the settlement (the effort has a cost)
  - At settlement:
    - fulfilled: rewards ×1.5, +2 Red Banner points
    - missed: *Broken Pledge* (1 year: PP −10 %) and cohesion −1
- **AI:** base 5; ×0 below 60 % stability or if the treasury < 0; ×2 for KAZ, AZE and UZB with `is_historical_focus_on` (they loved pledges).

### 4. Six Million Tons of White Gold
- **ID:** `COLDWAR_UNI_white_gold` · **Cost:** 5 · **Allow branch:** UZB, TAJ, TRK, KYR (KAZ: own "Cotton of the South" variant).
- **Prerequisites:** IX or X directives.
- **Available:** union republic; not `COLDWAR_SOV_aral_disaster` already set.
- **Effects:**
  - an agriculture district (MD helper, paid)
  - dynamic line: agriculture productivity +5 %, tax +2 %
  - +3 plan points (×1.5 with Group B, because textiles count)
  - downside: `global.COLDWAR_UNI_aral_strain` +1, stability −1 % (schools and students sent to the harvest)
  - tooltip: when Aral strain reaches 4, SOV gets `COLDWAR_SOV_aral_disaster` (event 46), and every republic that took a cotton or irrigation focus gets *The Dying Sea* (health cost +5 %, stability −2 %, until "Less Cotton" or Sibaral is completed)
- **AI:** base 10; ×3 UZB historical; ×0.3 if strain ≥ 3 and SOV has `save_the_aral_sea`.

### 5. Urengoy–Pomary–Uzhgorod
- **ID:** `COLDWAR_UNI_urengoy_pomary_uzhgorod` · **Cost:** 5 · **Prerequisites:** XI directives.
- **Available:**
  - global flag `COLDWAR_UNI_proj_pipeline_open`, set by SOV's launch decision, which needs `COLDWAR_SOV_urengoy`
  - project not finished
  - this country not yet a member
- **Effects:**
  - Republic:
    - pays 0.25 % of its GDP (UKR as host pays 0.15 %)
    - progress +25 (UKR +35)
    - joins `global.COLDWAR_UNI_proj_pipeline_members`
    - +2 plan points
  - SOV: pays 0.5 % of its GDP; progress +30.
  - Completion (progress ≥ 100 and ≥ 3 members including UKR) fires the event "Gas Flows to Europe" for all members:
    - members: energy line and opinion
    - UKR: transit line (tax +2 %)
    - SOV: gas export line, scaled by the oil ratio (read only)
  - Nothing is paid out before completion.
- **AI:** base 5; ×0 if treasury < 1 % GDP; ×3 for UKR.

### 6. The Transferable Red Banner
- **ID:** `COLDWAR_UNI_the_red_banner` · **Cost:** 3 · **Block:** socialist competition · **Prerequisites:** focus 1.
- **Available:** union republic or SOV.
- **Effects:**
  - Republic:
    - joins `global.COLDWAR_UNI_competitors`
    - unlocks the "Challenge [FROM] to Socialist Competition" decision
    - +10 PP
    - tooltip: at each January session, the competitor with the best output relative to quota gets the Red Banner (1 year: stability +3 %, construction +5 %, next Union project ticket); the last place gets a People's Control inspection
  - SOV:
    - unlocks the award ceremony news
    - cohesion +1 per ceremony while at least 3 republics compete
- **AI:** base 10; ×2 if ledger fulfilment ≥ 100 %.

### 7. Self-Managing Estonia (generic name "A Self-Managing Republic" for LAT and LIT)
- **ID:** `COLDWAR_UNI_self_managing_republic` · **Cost:** 5 · **Allow branch:** EST, LAT, LIT.
- **Prerequisites:** XII directives. LAT and LIT need EST's completion or the global flag `COLDWAR_UNI_ime_approved`.
- **Available:** union republic, and one of these on SOV: cohesion < 70, Politburo balance ≤ 0, or a reform flag (`deepen_the_kosygin_reform` / Gorbachev path).
- **Effects:**
  - Sends an offer to SOV. Nothing is paid now.
  - SOV approves:
    - the republic gets *Republican Khozraschet* (tax +5 %, stability +2 %, consumer goods −2 %; no free event-25 projects, no plan relief)
    - SOV: tax −1 % on the union modifier, cohesion +3, global flag `COLDWAR_UNI_ime_approved`, which opens the offer for every other republic
  - SOV refuses: the republic's national party +5 %, cohesion −2. The republic may raise it again after 365 days.
- **AI:** republic base 10 (EST ×3 historical). SOV AI approves if `COLDWAR_SOV_bop` < 0.

### 8. Friendship of Peoples: Rebuild Spitak
- **ID:** `COLDWAR_UNI_rebuild_spitak` (donor); ARM sees `COLDWAR_UNI_accept_the_unions_help` · **Cost:** 3.
- **Prerequisites:** XII directives.
- **Available:**
  - global flag `COLDWAR_UNI_spitak`, set by the earthquake event (Dec 1988, or by MTTH in an alt-history game)
  - the donor is a union republic or SOV, not ARM
- **Effects:**
  - Donor: offer to ARM, "[FROM] sends builders and money".
  - ARM accepts:
    - the donor pays 0.2 % of its GDP and builds one civilian factory or infrastructure level in ARM through `skip_payment`
    - ARM: stability +1 %
    - the donor: cohesion +1 and opinion
  - ARM refuses: nothing is paid. This allows the Karabakh-era politics.
  - At ≥ 5 donors: shared news "The Union Stands Together" (cohesion +5 once).
  - If ARM took **Metsamor** in X: ARM's damage doubles (flag `seismic_risk`).
- **AI:** donors base 20; ×0 for AZE while the Karabakh dispute flag is set.

### 9. Draft the Union Treaty / Sign the Union Treaty
- **IDs:** `COLDWAR_UNI_draft_the_union_treaty` (SOV, cost 7) and `COLDWAR_UNI_sign_the_union_treaty` (republic, cost 3).
- **Prerequisites:** endgame entry focus "A New Union?".
- **Available:**
  - SOV: plan ≥ 12, or cohesion < 50, or the Federation Council flag.
  - Republic: the global flag `COLDWAR_UNI_treaty_drafted`, no Declaration of Independence.
- **Effects:**
  - SOV:
    - news "The Union Treaty"
    - sets the draft flag
    - −50 PP
    - the balance shifts 0.05 toward the reformers
  - Republic (its own focus = its own consent):
    - *Sovereign Republic of the Union* (stability +5 %, PP +10 %)
    - cohesion +3
    - joins `global.COLDWAR_UNI_treaty_signers`
  - At 9 signers, SOV's capstone **The Union of Sovereign States** opens:
    - cohesion floor 40
    - union modifier lines
    - the alt-hist XIII plan
  - Without 9 signers after 365 days: *The Treaty Fails* (cohesion −5).
  - Non-signers lose nothing and keep their own national path.
- **AI:** republics sign if cohesion ≥ 25 and they are not Baltic (Baltics ×0.1); GEO, ARM and MLV ×0.3 (historical boycott).

### 10. Komsomol Shock Construction: BAM
- **ID:** `COLDWAR_UNI_komsomol_bam` · **Cost:** 3 · **Prerequisites:** X directives (or IX if the BAM project is already open).
- **Available:**
  - global flag `COLDWAR_UNI_proj_bam_open`, set by SOV's `the_baikal_amur_mainline`
  - manpower ≥ 5,000
  - not yet a member
- **Effects:**
  - Republic:
    - −2,000 manpower, returned after 365 days by a delayed event
    - BAM progress +10
    - joins the members
    - +2 plan points
    - "Komsomol Pass" line: production −2 % for 1 year (the young workers are away)
  - At ≥ 6 members and SOV's `bam_open_to_traffic`, the event "The Golden Link" fires for all members:
    - each gets a station settlement named in the news
    - +50 PP
    - cohesion +1
    - SOV gets its existing BAM supply effect
- **AI:** base 10; ×2 for UKR, BLR and the Baltics with `is_historical_focus_on`; ×0 below 10,000 manpower.

**Mentioned but not written out:** the Moscow foci (Gosplan Sets the Quotas, The People's Control), the Large-Scale Economic Experiment (joint, threshold 3), The Water Accord (upstream/downstream offer), The Phosphorite War (delayed protest), and The Dry Law in the Republics.

---

## 11. Mechanics confidence summary

- **[OK]:**
  - shared foci with offsets and `allow_branch` by tag
  - global variables and arrays
  - offers and events
  - GDP-share payments, building helpers with `skip_payment`
  - dynamic modifiers on variables
  - missions
  - delayed events (brigades coming back)
  - the vote engine with new subjects
  - news lines per republic through scripted loc
- **[MD-PROVEN, TEST]:** `joint_focus` capstones. Test member behaviour: prerequisites, running focus, overlord/subject, `completion_reward_joint_member`. Fallback: a shared capstone with a global-threshold `available`.
- **[VERIFY]:**
  - overlapping coordinates for groups hidden by `allow_branch`
  - `[?var]` in focus descriptions
  - reading factory counts into variables (real output)
  - MTTH factor driven by a global counter (RBMK)
  - `custom_cost_trigger` (the threshold-variable fallback is planned)
  - special-project progress from a republic's focus
  - `set_autonomy` to the 1985 Soviet republic autonomy in 1970
  - `add_offsite_building` removal
- **[UNSURE] / avoided:**
  - dynamic focus costs (not possible → multipliers)
  - dynamic `allow_branch` (→ `available`)
  - a full sorted ranking of 14 republics (→ top and bottom only)
  - AI coordination in thresholds (→ AI weights plus a hidden AI floor)

---

## 12. Open questions for the author

1. **Ledger or statuses?** A per-republic plan number (fulfilment %) is new state and touches the 15.10 rule "no per-republic meters". Full ledger, or the status-only variant?
2. **Where do SSR players get the branch?** Today they load the generic 1970 tree (349 foci). Option (a): include the shared branch there, with `allow_branch` for the 14 tags. Option (b): a small dedicated `COLDWAR_SSR_1970_focus` tree.
3. **Joint foci.** Is it acceptable that a joint capstone completes in other players' trees (rewards only), or should it be shared foci and global thresholds only?
4. **Event 25.** Should the free Union project stay seat-only, or also go to Red Banner holders and over-fulfillers?
5. **Funding split.** For megaprojects, does Moscow carry most of the cost (e.g. 50–70 %), or should the republics pay the larger part?
6. **Audits.** Should SOV be able to inspect any republic at any time (People's Control decision), or only under the Andropov/Romanov flags as today?
7. **AI pripiski.** The Politburo design says the AI never reports pripiski. Keep that, or let AI UZB/AZE pad historically?
8. **Union Treaty.** Should signing change the autonomy level (needs the 1985 autonomy in 1970), or only add ideas?
9. **Prefix.** Is `COLDWAR_UNI_` fine, and should the tree be generated by `sovgen` or by its own generator?
10. **Alt-history XIII plan.** Include a XIII plan (1991–95) for a surviving Union, or end at XII?
11. **Delivery war.** Should the 1990–91 decisions to end contracts (loop E) exist at all, or does that feel like griefing even though they only end consented deals?

---

## Appendix: historical anchors used

**Five-Year Plans:** IX 1971–75 (XXIV Congress 1971), X 1976–80 (XXV), XI 1981–85 (XXVI), XII 1986–90 (XXVII).

**Plants, dams and pipelines:**
- AvtoVAZ: first Zhiguli in 1970. KamAZ: first truck in Feb 1976.
- BAM: decree 1974, golden link 1984.
- Nurek: first unit 1972, completed 1980. Toktogul: mid/late 1970s. Inguri: from 1978, completed 1987. Rogun: begun 1976.
- Ignalina: unit 1 in 1983, unit 3 halted 1988. Chernobyl: unit 1 in 1977, accident 26.04.1986. Metsamor: 1976/1980, closed 1989.
- Urengoy–Pomary–Uzhgorod: 1982–84; Western sanctions 1981–82. Orenburg "Soyuz": 1975–78/79.
- Ekibastuz GRES-1 and the 1150 kV line: 1980s. Tengiz: discovered 1979. TadAZ: 1975. Mažeikiai: 1980. Muuga: 1986. Klaipėda–Mukran: 1986.

**Programmes, laws and events:**
- Order of Friendship of Peoples: created Dec 1972; the union republics were among the first holders.
- Non-Black-Earth programme: 1974. Food Programme: May 1982.
- Large-Scale Economic Experiment: 1984. Ministries named in §5 XI.
- Cotton affair: investigations from 1983 (Gdlyan–Ivanov).
- Georgian language protest: 14.04.1978.
- Anti-alcohol campaign: May 1985.
- Siberian river diversion cancelled: Aug 1986.
- IME: Sept 1987. Phosphorite War: 1987. Daugavpils HPP stopped: 1987. Nevada–Semipalatinsk: 1989.
- Spitak: 07.12.1988.
- Union law on Baltic economic independence: 27.11.1989.
- 500 Days: 1990.
- Union referendum: 17.03.1991. Novo-Ogaryovo: 23.04.1991.
- Treaty on the Economic Community: 18.10.1991.

**Leaders:**
- Shelest / Shcherbytsky (UKR)
- Masherov (BLR, †1980)
- Kunaev (KAZ, until Dec 1986)
- Rashidov (UZB, †1983)
- Aliyev (AZE, 1969–82)
- Shevardnadze (GEO, 1972–85)
- Bodiul (MLV, until 1980)

Approximate where marked; check the details again before writing loc text.
