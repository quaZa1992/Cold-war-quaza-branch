# Vietnam: focus structure and decision audit

Read-only review of the loaded 307-focus tree, 19 October 2026. Only this report and `layout.json` were written. The JSON contains all 307 current cards, resolved coordinates, actual prerequisite groups, exclusions, visible English text and source links.

## Assessment

The graph uses native MD anchoring and exclusion syntax correctly. No asymmetric exclusions, missing prerequisites, structurally incompatible histories or source-bound card collisions were found. The design problem is opportunity cost and repeated progression: fourteen nearly identical ten-row programmes, three compulsory campaign preambles, and temporary operating policies embedded in long focus chains. Preserve the requested seventy-day standard for substantive national institutions; merge procedural cards and put urgent, short-lived operations into actual gated paid decisions.

The current tree has 298 focuses at 70 days, seven at 35 and two at 42; eighteen roots and eighteen shortcuts. Nine political programmes are independently gated by their actual party or communist incumbent. The civic outlook cards are not required to unlock them.

## Current main MD comparison

| Reference | Focuses | Most common nominal durations | AND joins | Nodes with exclusions | Resolved grid bounds |
|---|---:|---|---:|---:|---|
| 00_generic.txt | 158 | 70 days × 103, 55.02 days × 29, 60.2 days × 10, 35 days × 9 | 27 | 29 | [-13, 0, 51, 10] |
| 05_russia.txt | 806 | 21 days × 314, 35 days × 216, 49 days × 168, 14 days × 76 | 169 | 85 | [0, 0, 235, 26] |
| Current Vietnam | 307 | 70 days × 298; 35 × 7; 42 × 2 | 3 | 106 | [1,0,78,26] |

Russia is wider than Vietnam, so raw width is not a native-style defect. Its cadence and branch footprints vary substantially. Its 35-day state-corporatism / oligarchic-republic / combined-economy choice at (78,8)/(74,8)/(76,8) consumes prior verdicts and changes distinct institutions, corruption and interest-group relations. Generic centralisation/decentralisation at (0,2)/(2,2) is a symmetric institutional fork. Vietnam copies that syntax but repeats essentially one three-diamond topology across unrelated subjects. The seventy-day rule was requested by the user; the recommendation is fewer procedural steps, not a blanket return to Russia's shorter focus costs.

- `GENERIC_centralization` [0, 2]: [00_generic.txt:641](<E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/00_generic.txt:641>)
- `GENERIC_decentralization` [2, 2]: [00_generic.txt:604](<E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/00_generic.txt:604>)
- `GENERIC_the_west` [-6.5, 3]: [00_generic.txt:687](<E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/00_generic.txt:687>)
- `SOV_state_corporatism` [78, 8]: [05_russia.txt:553](<E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_russia.txt:553>)
- `SOV_oligarchic_republic` [74, 8]: [05_russia.txt:601](<E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_russia.txt:601>)
- `SOV_combined_economic_system` [76, 8]: [05_russia.txt:650](<E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_russia.txt:650>)

## Findings

### L01 · Chinh's ten-step programme cannot fit the default historical mandate (high)

**Evidence:** The shortest compatible route to the handover costs 665 nominal focus-days across ten completed focuses. The installed historical observer installs Chinh on 14 July 1986 and Linh on 18 December: 157 days. All Chinh focuses require Chinh personally, cancel when invalid and cannot continue under Linh.

**Implication:** Only two seventy-day focuses fit the default historical window; its handover capstone is inaccessible in that window.

An early alternate Chinh mandate can last longer. This is not a claim that every alternate history blocks his tree.

Affected cards: `COLDWAR_VIE_chinh_root` (20,0); `COLDWAR_VIE_chinh_documents` (20,3); `COLDWAR_VIE_chinh_handover` (20,9).

Sources: [COLDWAR_VIE_1970_focus.txt:1456](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:1456>), [COLDWAR_VIE_1970_focus.txt:1679](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:1679>), [COLDWAR_VIE_1970_focus.txt:2142](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:2142>).

### L02 · All campaign forks are behind forced dual-lane introductions (high)

**Evidence:** These are the only three multiple-block AND joins in the entire tree. Each requires a root, both two-focus lanes and the central join. Their minimum costs are respectively 420/385/385 focus-days and 0.095/0.100/0.100 billion in contributions.

**Implication:** The first operational choice appears after more than a year of uninterrupted selections. The parallel-looking introductions are both compulsory.

These are structural lower bounds before war/party/treasury waiting and other national priorities.

Affected cards: `COLDWAR_VIE_guerrilla_networks` (52,16); `COLDWAR_VIE_cambodia_mandate` (60,16); `COLDWAR_VIE_china_crisis` (68,16).

Sources: [COLDWAR_VIE_1970_focus.txt:11015](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:11015>), [COLDWAR_VIE_1970_focus.txt:11729](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:11729>), [COLDWAR_VIE_1970_focus.txt:12469](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:12469>).

### L03 · The wartime defence and offensive bonuses arrive after lengthy war-only research (high)

**Evidence:** Even with all earlier institutions prepared, China Crisis needs 35 days during actual CHI war before Hold can begin its 70 days. Hold's defensive bonus therefore arrives no earlier than 105 days into that response; Depth requires another 70. Phnom Penh Objective likewise needs 70 days of actual CBD war. cancel_if_invalid=yes and continue_if_invalid=no are emitted.

**Implication:** A short real war can finish before the intended campaign bonus is granted. A focus-day standard designed for national institutions has become a reaction delay on operational orders.

The script arithmetic is confirmed. Historical short-offensive dates are contextual and should be supplied by the historical research audit; no war duration or engine cancellation was simulated.

Affected cards: `COLDWAR_VIE_china_crisis` (68,16); `COLDWAR_VIE_china_hold` (67,17); `COLDWAR_VIE_china_depth` (67,18); `COLDWAR_VIE_cambodia_capital` (61,18).

Sources: [COLDWAR_VIE_1970_focus.txt:12469](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:12469>), [COLDWAR_VIE_1970_focus.txt:12503](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:12503>), [COLDWAR_VIE_1970_focus.txt:12567](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:12567>), [COLDWAR_VIE_1970_focus.txt:11866](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:11866>).

### L04 · Paid temporary policies expire while unlocking their own next layer (high)

**Evidence:** The two guerrilla preparation lanes grant 180-day policies. Local replaces Cadres within liaison; Staff replaces Training within training. The lane completed first must wait at least three further seventy-day completions before Networks: its latest policy is expired by then. Survey, Command, Hold and Depth also replace one china_posture family rather than accumulating.

**Implication:** Focus cards read like permanent institutional development, but several are paid replacement programmes whose useful window is consumed by the next focus chain.

Replacement is intentional and correctly guarded; this is a pacing and presentation mismatch, not a claim of stacking bugs.

Affected cards: `COLDWAR_VIE_guerrilla_cadres` (50,14); `COLDWAR_VIE_guerrilla_local` (50,15); `COLDWAR_VIE_guerrilla_training` (54,14); `COLDWAR_VIE_guerrilla_staff` (54,15); `COLDWAR_VIE_china_survey` (70,14); `COLDWAR_VIE_china_liaison` (70,15); `COLDWAR_VIE_china_hold` (67,17); `COLDWAR_VIE_china_depth` (67,18).

Sources: [COLDWAR_VIE_1970_focus.txt:10894](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:10894>), [COLDWAR_VIE_1970_focus.txt:10955](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:10955>), [COLDWAR_VIE_1970_focus.txt:10925](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:10925>), [COLDWAR_VIE_1970_focus.txt:10985](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:10985>).

### L05 · Cambodia's limited route still points into a victory-only continuation (high)

**Evidence:** Aftermath has Monitor OR Capital as focus prerequisites, but its live gate requires a real won Cambodian campaign. A limited peaceful route must instead use the separate x56 bypass and verified terms before the regional continuation.

**Implication:** The central connector promises a continuation that the intended limited outcome normally cannot take.

The bypass already prevents a total dead end. Do not award military victory merely to repair a drawing.

Affected cards: `COLDWAR_VIE_cambodia_monitor` (59,18); `COLDWAR_VIE_cambodia_aftermath` (60,19); `COLDWAR_VIE_cambodia_border_settlement` (56,20); `COLDWAR_VIE_cambodia_limited_commitment` (56,22); `COLDWAR_VIE_cambodia_talks` (60,25).

Sources: [COLDWAR_VIE_1970_focus.txt:11834](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:11834>), [COLDWAR_VIE_1970_focus.txt:11898](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:11898>), [COLDWAR_VIE_1970_focus.txt:13036](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:13036>), [COLDWAR_VIE_1970_focus.txt:13068](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:13068>).

### L06 · Permanent locks sometimes separate complementary activities (medium)

**Evidence:** Front pressure excludes Paris talks; mobilisation excludes a diplomatic opening. Aircrew Training has only the Fleet parent, while Coastal Defence permanently excludes Fleet.

**Implication:** Coercive diplomacy is prohibited and a coastal-defence choice unexpectedly forbids pilot training. These are unnecessary policy restrictions rather than asymmetric syntax.

Affected cards: `COLDWAR_VIE_unity_pressure` (34,14); `COLDWAR_VIE_unity_paris` (38,14); `COLDWAR_VIE_china_mobilise` (67,23); `COLDWAR_VIE_china_opening` (69,23); `COLDWAR_VIE_army_coastal` (26,20); `COLDWAR_VIE_army_fleet` (30,20); `COLDWAR_VIE_army_aircrew` (30,21).

Sources: [COLDWAR_VIE_1970_focus.txt:9423](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:9423>), [COLDWAR_VIE_1970_focus.txt:9464](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:9464>), [COLDWAR_VIE_1970_focus.txt:12833](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:12833>), [COLDWAR_VIE_1970_focus.txt:12865](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:12865>).

### L07 · Fourteen different subjects share one sixteen-node template (medium)

**Evidence:** Nine political islands and five common branches each contain sixteen nodes over ten rows, three binary exclusive pairs and repeated OR reconvergence. A selected terminal route normally takes ten focuses. Alternating one/two-column offsets changes the silhouette slightly but not the repeated grammar.

**Implication:** Distinct leaders, institutions, civilian sectors and military services read as interchangeable ten-step checklists.

Native Russia is also very wide. Width and a grid are not intrinsically incorrect MD style.

Affected cards: `COLDWAR_VIE_duan_root` (12,0); `COLDWAR_VIE_chinh_root` (20,0); `COLDWAR_VIE_linh_root` (28,0); `COLDWAR_VIE_kiet_root` (36,0); `COLDWAR_VIE_front_root` (44,0); `COLDWAR_VIE_dem_root` (52,0); `COLDWAR_VIE_soc_root` (60,0); `COLDWAR_VIE_nat_root` (68,0); `COLDWAR_VIE_junta_root` (76,0); `COLDWAR_VIE_industry_root` (12,13); `COLDWAR_VIE_farm_root` (20,13); `COLDWAR_VIE_army_root` (28,13); `COLDWAR_VIE_unity_root` (36,13); `COLDWAR_VIE_diplomacy_root` (44,13).

Sources: [COLDWAR_VIE_1970_focus.txt:734](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:734>), [COLDWAR_VIE_1970_focus.txt:1456](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:1456>), [COLDWAR_VIE_1970_focus.txt:2188](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:2188>), [COLDWAR_VIE_1970_focus.txt:2925](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:2925>).

### L08 · Outlook advocacy looks like ideology selection but unlocks no party tree (medium)

**Evidence:** All four outlook cards follow the civic root, have no mutual exclusions and can be completed sequentially. Exact-party/leader roots are independently gated and require none of those cards.

**Implication:** The drawing invites an ideology-branch interpretation while the reward is a popularity/outlook intervention. Adding another mandatory outlook-unlock ceremony would worsen the issue.

Permanent outlook exclusivity would conflict with the requested multiplayer party departure/return system; advocacy should be moved to decisions rather than made a permanent ideological prison.

Affected cards: `COLDWAR_VIE_state_root` (4,0); `COLDWAR_VIE_state_emerging` (1,1); `COLDWAR_VIE_state_western` (3,1); `COLDWAR_VIE_state_neutral` (5,1); `COLDWAR_VIE_state_national` (7,1); `COLDWAR_VIE_duan_root` (12,0); `COLDWAR_VIE_dem_root` (52,0).

Sources: [COLDWAR_VIE_1970_focus.txt:30](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:30>), [COLDWAR_VIE_1970_focus.txt:64](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:64>), [COLDWAR_VIE_1970_focus.txt:107](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:107>), [COLDWAR_VIE_1970_focus.txt:158](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:158>).

### L09 · The civilian transition is a three-card preparation ceremony (medium)

**Evidence:** The three successive seventy-day cards all require the military-junta government. They grant programme modifiers and unlock flags; the civilian decision is a funded timed idea. Actual native political transfer remains separate.

**Implication:** The labels promise a regime-level outcome while the tree remains under the old government's gate throughout.

Do not repair this with a forced coup, automatic election winner or invented historical leader. Use a real player-owned native transition contract.

Affected cards: `COLDWAR_VIE_junta_transition` (78,7); `COLDWAR_VIE_junta_assembly` (78,8); `COLDWAR_VIE_junta_mandate` (76,9).

Sources: [COLDWAR_VIE_1970_focus.txt:7036](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:7036>), [COLDWAR_VIE_1970_focus.txt:7123](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:7123>), [COLDWAR_VIE_1970_focus.txt:7171](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:7171>).

### L10 · Orderly islands have too little thematic hierarchy (medium)

**Evidence:** Political roots are at x12,20,...76 with the same ten-row height. The junta root is 6144 grid pixels right of the initial Duan root. Eighteen branch shortcuts already exist. The repeated grid is stronger than the thematic distinction between short-lived incumbents and permanent national systems.

**Implication:** Shorten and differentiate leadership footprints, retain shortcuts and reserve space for genuine institutional forks. Do not compress titlebars onto adjacent columns.

Source-bound overlap and structural checks are separate from native rendering; no game screenshot or conditional-hide refresh was tested.

Affected cards: `COLDWAR_VIE_duan_root` (12,0); `COLDWAR_VIE_chinh_root` (20,0); `COLDWAR_VIE_linh_root` (28,0); `COLDWAR_VIE_junta_root` (76,0).

Sources: [COLDWAR_VIE_1970_focus.txt:734](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:734>), [COLDWAR_VIE_1970_focus.txt:1456](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:1456>), [COLDWAR_VIE_1970_focus.txt:2188](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:2188>), [COLDWAR_VIE_1970_focus.txt:6509](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/COLDWAR_VIE_1970_focus.txt:6509>).

Additional actual-script anchors:

- Historical Linh handover: [COLDWAR_VIE_1970_politics.txt:74](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/COLDWAR_VIE_1970_politics.txt:74>)
- Historical Chinh handover: [COLDWAR_VIE_1970_politics.txt:78](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/COLDWAR_VIE_1970_politics.txt:78>)
- Liaison policy replacement: [COLDWAR_VIE_campaign_effects.txt:18](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/COLDWAR_VIE_campaign_effects.txt:18>)
- Training policy replacement: [COLDWAR_VIE_campaign_effects.txt:26](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/COLDWAR_VIE_campaign_effects.txt:26>)
- Actual military victory gate: [COLDWAR_VIE_campaign_triggers.txt:194](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/COLDWAR_VIE_campaign_triggers.txt:194>)
- Civilian transition programme effect: [COLDWAR_VIE_1970_effects.txt:10930](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/COLDWAR_VIE_1970_effects.txt:10930>)

## Minimum focus-day commitments

These are compatible structural lower bounds, including every compulsory AND lane and one member of each OR group. They exclude financing/war/party waiting, other national priorities and external focus duration modifiers.

| Target | Position | Minimum completed focuses | Nominal days | Compatible histories |
|---|---|---:|---:|---:|
| `COLDWAR_VIE_state_charter` | [4, 9] | 9 | 630 | 16 |
| `COLDWAR_VIE_duan_legacy` | [12, 9] | 10 | 700 | 8 |
| `COLDWAR_VIE_chinh_handover` | [20, 9] | 10 | 665 | 8 |
| `COLDWAR_VIE_linh_survival` | [28, 9] | 10 | 700 | 8 |
| `COLDWAR_VIE_industry_recovery` | [12, 22] | 10 | 672 | 8 |
| `COLDWAR_VIE_army_postwar` | [28, 22] | 10 | 672 | 8 |
| `COLDWAR_VIE_guerrilla_networks` | [52, 16] | 6 | 420 | 1 |
| `COLDWAR_VIE_guerrilla_aftermath` | [52, 26] | 16 | 1050 | 8 |
| `COLDWAR_VIE_cambodia_mandate` | [60, 16] | 6 | 385 | 1 |
| `COLDWAR_VIE_cambodia_limits` | [60, 26] | 12 | 805 | 9 |
| `COLDWAR_VIE_china_crisis` | [68, 16] | 6 | 385 | 1 |
| `COLDWAR_VIE_china_hold` | [67, 17] | 7 | 455 | 1 |
| `COLDWAR_VIE_china_security` | [68, 26] | 16 | 1050 | 8 |

## Ten concrete changes for review

These are proposals, not approved implementation. Outer prerequisite groups below are AND; multiple IDs within one group are OR. Any removed card needs explicit handling for existing completion/reward flags.

### R01 · Make Chinh a two-focus congress mandate

**Change:** Keep the root plus one substantive exclusive seventy-day mandate. Move hearings, drafting and subsidy review into decision/event options. Remove the handover as a ten-step capstone; native succession remains authoritative.

**Benefit:** A 140-day route fits the 157-day historical window. An early alternate mandate can open additional decisions rather than another identical full tree.

**Preserve:** Remembered progress, genuine native succession and the distinction between personal active modifiers and lasting reforms.

Current anchors: `COLDWAR_VIE_chinh_root` (20,0); `COLDWAR_VIE_chinh_orthodox` (19,1); `COLDWAR_VIE_chinh_evidence` (21,1); `COLDWAR_VIE_chinh_documents` (20,3); `COLDWAR_VIE_chinh_rectify` (20,6); `COLDWAR_VIE_chinh_handover` (20,9).

### R02 · Move four outlook advocacy cards out of the focus spine

**Change:** Keep After Ho Chi Minh as the civic root. Make outlook advocacy native political decisions. Connect Cadres and Mass Organisation directly to state_root. Keep exact-party roots independent.

**Benefit:** Four ceremonial cards disappear; the shortest civic route loses seventy days without preventing future party changes.

**Preserve:** Party programme departure/reactivation follows actual power, not a permanently selected outlook focus.

Current anchors: `COLDWAR_VIE_state_emerging` (1,1); `COLDWAR_VIE_state_western` (3,1); `COLDWAR_VIE_state_neutral` (5,1); `COLDWAR_VIE_state_national` (7,1); `COLDWAR_VIE_state_cadres` (2,3); `COLDWAR_VIE_state_mass` (6,3).

Proposed prerequisites:

```json
{
  "COLDWAR_VIE_state_cadres": [
    [
      "COLDWAR_VIE_state_root"
    ]
  ],
  "COLDWAR_VIE_state_mass": [
    [
      "COLDWAR_VIE_state_root"
    ]
  ]
}
```

### R03 · Make guerrilla preparation a genuine institutional choice

**Change:** Use political organisation versus professional small-unit schools as the first institutional fork. Move Local/Staff upgrades to paid programme decisions. Networks takes one OR group rather than requiring both lanes.

**Benefit:** A three-focus entrance costs 210 days before the operational choice, rather than 420. A later voluntary integration project can reward players who fund both capabilities.

**Preserve:** No fabricated units or universal rebellion. Rebalance programme terms and migrate old prerequisite flags together.

Current anchors: `COLDWAR_VIE_guerrilla_cadres` (50,14); `COLDWAR_VIE_guerrilla_training` (54,14); `COLDWAR_VIE_guerrilla_local` (50,15); `COLDWAR_VIE_guerrilla_staff` (54,15); `COLDWAR_VIE_guerrilla_networks` (52,16).

Proposed prerequisites:

```json
{
  "COLDWAR_VIE_guerrilla_networks": [
    [
      "COLDWAR_VIE_guerrilla_cadres",
      "COLDWAR_VIE_guerrilla_training"
    ]
  ]
}
```

Proposed exclusive pairs:

```json
[
  [
    "COLDWAR_VIE_guerrilla_cadres",
    "COLDWAR_VIE_guerrilla_training"
  ]
]
```

### R04 · Prepare Chinese defence before war and activate it during the real campaign

**Change:** Keep seventy-day defensive institutions and contingency planning available before war. Leave talks/rights optional. Crisis needs Northern Command, not both lanes. A gated paid war decision/event activates the chosen 180-day operational posture when an actual war begins; a long focus is not the sole way to issue an urgent order.

**Benefit:** Removes 140 mandatory preparation days and avoids waiting 105 days into a short war for the first defence bonus without breaking the seventy-day focus standard.

**Preserve:** Actual CHI combat gates, the user-approved entrenchment/core/forest/jungle values, family replacement, cost, expiry and hidden-tech cleanup.

Current anchors: `COLDWAR_VIE_china_talks` (66,14); `COLDWAR_VIE_china_citizens` (66,15); `COLDWAR_VIE_china_survey` (70,14); `COLDWAR_VIE_china_liaison` (70,15); `COLDWAR_VIE_china_crisis` (68,16); `COLDWAR_VIE_china_hold` (67,17); `COLDWAR_VIE_china_counter` (69,17); `COLDWAR_VIE_china_depth` (67,18).

Proposed prerequisites:

```json
{
  "COLDWAR_VIE_china_crisis": [
    [
      "COLDWAR_VIE_china_liaison"
    ]
  ]
}
```

### R05 · Give Cambodia separate diplomacy and military entrances

**Change:** Let commission requests start from the question/logistics institution without first needing Cambodian war or a hostile war goal. Make civilian protection optional. Merge frontier/command preparation. Mandate accepts real military preparation OR a genuinely accepted limited-security framework. Prepare an operational plan in a seventy-day focus, then activate its timed campaign effects with a real-war decision.

**Benefit:** Avoids a 385-day two-lane toll and lets diplomacy begin before a hostile crisis. The capital-campaign bonus need not wait seventy actual war days.

**Preserve:** A regime-change war goal still requires grave actual hostility. A commission never awards military victory, annexation or automatic peace.

Current anchors: `COLDWAR_VIE_cambodia_question` (60,13); `COLDWAR_VIE_cambodia_frontier` (58,14); `COLDWAR_VIE_cambodia_civilians` (62,14); `COLDWAR_VIE_cambodia_staff` (58,15); `COLDWAR_VIE_cambodia_channel` (62,15); `COLDWAR_VIE_cambodia_mandate` (60,16); `COLDWAR_VIE_cambodia_capital` (61,18).

### R06 · Clean up the limited Cambodia bypass

**Change:** Remove Monitor from the victory-node prerequisite. Merge Sovereign Border and Limited Commitment into one implementation focus; keep the actual limited review as a paid decision. Join the regional process from that verified limited node.

**Benefit:** One misleading connector and a repeated seventy-day/0.020-billion step disappear.

**Preserve:** Actual peace, no occupation, reciprocal drawdown, current terms and the separate limited verification. Saved flags need migration.

Current anchors: `COLDWAR_VIE_cambodia_monitor` (59,18); `COLDWAR_VIE_cambodia_aftermath` (60,19); `COLDWAR_VIE_cambodia_border_settlement` (56,20); `COLDWAR_VIE_cambodia_limited_commitment` (56,22); `COLDWAR_VIE_cambodia_talks` (60,25).

Proposed prerequisites:

```json
{
  "COLDWAR_VIE_cambodia_aftermath": [
    [
      "COLDWAR_VIE_cambodia_capital"
    ]
  ],
  "COLDWAR_VIE_cambodia_talks": [
    [
      "COLDWAR_VIE_cambodia_restore",
      "COLDWAR_VIE_cambodia_verify",
      "COLDWAR_VIE_cambodia_border_settlement"
    ]
  ]
}
```

### R07 · Remove the paid Long Commitment acknowledgement

**Change:** The burden already follows actual occupation/native assistance. Remove the compulsory seventy-day/0.020-billion acknowledgement; offer exit policy after either administration branch.

**Benefit:** The player pays and waits for a policy, rather than for acknowledgement that the commitment exists.

**Preserve:** Offers remove no burden; verified withdrawal and actual mission termination stay authoritative.

Current anchors: `COLDWAR_VIE_cambodia_train` (58,21); `COLDWAR_VIE_cambodia_dry` (62,21); `COLDWAR_VIE_cambodia_burden` (60,22); `COLDWAR_VIE_cambodia_stay` (59,23); `COLDWAR_VIE_cambodia_leave` (61,23).

Proposed prerequisites:

```json
{
  "COLDWAR_VIE_cambodia_stay": [
    [
      "COLDWAR_VIE_cambodia_train",
      "COLDWAR_VIE_cambodia_dry"
    ]
  ],
  "COLDWAR_VIE_cambodia_leave": [
    [
      "COLDWAR_VIE_cambodia_train",
      "COLDWAR_VIE_cambodia_dry"
    ]
  ]
}
```

### R08 · Do not permanently exclude diplomacy from military readiness

**Change:** Remove Pressure/Paris and Mobilisation/Opening permanent exclusions. Separate negotiation and military-programme families. Retain real force-structure incompatibilities and recipient consent.

**Benefit:** Supports fighting and negotiating, refusal and revised terms in multiplayer.

**Preserve:** Removing a focus lock alone is insufficient if the supposedly parallel ideas still silently replace one shared family.

Current anchors: `COLDWAR_VIE_unity_pressure` (34,14); `COLDWAR_VIE_unity_paris` (38,14); `COLDWAR_VIE_china_mobilise` (67,23); `COLDWAR_VIE_china_opening` (69,23); `COLDWAR_VIE_china_standdown` (69,24).

Remove exclusive pairs:

```json
[
  [
    "COLDWAR_VIE_unity_pressure",
    "COLDWAR_VIE_unity_paris"
  ],
  [
    "COLDWAR_VIE_china_mobilise",
    "COLDWAR_VIE_china_opening"
  ]
]
```

### R09 · Detach Aircrew Training from the fleet choice

**Change:** Connect Aircrew Training to the shared service institution or an independent air branch. Reserve Coastal/Fleet exclusivity for naval force structure.

**Benefit:** A coastal doctrine no longer forbids unrelated pilot training.

**Preserve:** Dockyards remain funded queued construction; no free aircraft or units.

Current anchors: `COLDWAR_VIE_army_coast` (28,19); `COLDWAR_VIE_army_coastal` (26,20); `COLDWAR_VIE_army_fleet` (30,20); `COLDWAR_VIE_army_aircrew` (30,21).

Proposed prerequisites:

```json
{
  "COLDWAR_VIE_army_aircrew": [
    [
      "COLDWAR_VIE_army_coast"
    ]
  ]
}
```

### R10 · Replace the civilian-handover ceremony with a real transition contract

**Change:** Keep one mandate-setting focus, then negotiate the constituent timetable through native political events and decisions. Merge Assembly/Regular Mandate into that settlement rather than requiring another 140 days under the old government gate.

**Benefit:** The selected route changes permitted governing arrangements and lasting civic guarantees rather than merely unlocking another generic timed administration idea.

**Preserve:** No forced election winner or invented coup leader. Constitutional guarantees owned by the national settlement must not disappear merely because the old junta programme deactivates.

Current anchors: `COLDWAR_VIE_junta_transition` (78,7); `COLDWAR_VIE_junta_assembly` (78,8); `COLDWAR_VIE_junta_mandate` (76,9).

## Six substantive new choice contracts

These replace mismatched or cosmetic forks instead of adding twelve compulsory toll cards. Each side has a credible benefit, a cost and different follow-up decisions. They must be exclusive in both directions. Positions reuse existing slots after the associated changes; this is not a rendered replacement tree. Exact numeric balance and APIs require the separate mechanics review. Agreement events must show agreed costs/rewards numerically in native option effects and keep English descriptions short.

### C01 · The congress inherits a concrete economic mandate

| Route | Proposed ID / slot | Advantage | Cost |
|---|---|---|---|
| Secure the Consumption Floor | `COLDWAR_VIE_chinh_stabilisation_mandate` [19, 1] | Protect rations, wages and administrative continuity. | Higher funded support burden and slower price adjustment. |
| Release the Enterprises | `COLDWAR_VIE_chinh_enterprise_mandate` [21, 1] | Retained earnings and local procurement experiments. | Temporary price/stability disruption and a smaller guaranteed consumption floor. |

**Path contract:** Root plus choice is 140 days; hearings and handover are decisions/native succession. The congress settlement persists beyond Chinh, while his personal programme still follows office.

**Different follow-up decisions:** A finite emergency subsidy budget with actual paid tranches. / Choose which real pilot programmes receive scarce funds.

Replace: `COLDWAR_VIE_chinh_orthodox`, `COLDWAR_VIE_chinh_evidence`.

### C02 · Le Duan allocates scarce national effort

| Route | Proposed ID / slot | Advantage | Cost |
|---|---|---|---|
| Rebuild the North First | `COLDWAR_VIE_duan_northern_reconstruction_mandate` [10, 1] | Commit the next programme to repair capacity and civilian output. | Reduced operational mobilisation commitment during reconstruction. |
| Sustain the Southern Effort | `COLDWAR_VIE_duan_southern_campaign_mandate` [14, 1] | Protect military readiness and resources allocated to the real southern effort. | Delayed civilian repair and consumption commitments. |

**Path contract:** Rename the introductory mandate accordingly. Both routes may negotiate. Exclusive national allocation, not willingness to talk, is the incompatibility; later integration follows a real outcome.

**Different follow-up decisions:** Choose actual paid northern construction/investment projects. / Choose a bounded real-war support programme without free units.

Replace: `COLDWAR_VIE_duan_offensive`, `COLDWAR_VIE_duan_patient`.

### C03 · Renovation deals with the cadre network

| Route | Proposed ID / slot | Advantage | Cost |
|---|---|---|---|
| Negotiate a Cadre Compact | `COLDWAR_VIE_linh_protect_cadre_compact` [26, 7] | Preserve administrative continuity and provincial cooperation. | Retained patronage costs and slower managerial accountability. |
| Give the Auditors Authority | `COLDWAR_VIE_linh_independent_inspections` [30, 7] | Reduce protected procurement and managerial abuses. | Funded inspections and temporary political cohesion costs. |

**Path contract:** Both are party-led reform paths with different personnel and programme consequences. Constitutional pluralism is a separately negotiated governing transition rather than a generic research-bonus card.

**Different follow-up decisions:** Negotiate performance obligations with native personnel institutions. / Choose an audit target and accept a finite backlash, not an invented universal purge.

Replace: `COLDWAR_VIE_linh_monopoly`, `COLDWAR_VIE_linh_pluralism`.

### C04 · A constitutional government settles wartime property claims

| Route | Proposed ID / slot | Advantage | Cost |
|---|---|---|---|
| A Restitution Commission | `COLDWAR_VIE_dem_restitution_commission` [50, 7] | Credible individual claims and civil property guarantees. | Slow administrative resolution and disputes with current beneficiaries. |
| A Compensation Fund | `COLDWAR_VIE_dem_compensation_fund` [54, 7] | Settle claims without indiscriminate eviction or production disruption. | A defined treasury contribution and longer public payment burden. |

**Path contract:** Move foreign alignment to diplomacy. The settlement method creates different domestic obligations; it does not automatically transfer population, provinces or factories.

**Different follow-up decisions:** Fund case-by-case claims and choose protections for current households. / Select an actually funded tranche with concrete numeric event effects.

Replace: `COLDWAR_VIE_dem_west`, `COLDWAR_VIE_dem_neutral`.

### C05 · A military government chooses a credible civilian exit

| Route | Proposed ID / slot | Advantage | Cost |
|---|---|---|---|
| Set a Constituent Deadline | `COLDWAR_VIE_junta_constituent_deadline` [77, 8] | A clear and rapid civilian constitutional mandate. | Immediate uncertainty and reduced military appointment control. |
| A Phased Civilian Cabinet | `COLDWAR_VIE_junta_phased_civilian_cabinet` [79, 8] | Administrative/security continuity during a staged transfer. | Longer transition costs and weaker immediate civilian legitimacy. |

**Path contract:** Retain the existing permanent-council route. Within the chosen civilian-transition path, these are two viable transfer mechanisms with different obligations. The accepted result must reach the actual native political system, not only a timed buff.

**Different follow-up decisions:** Negotiate actual native election/assembly guarantees with the player retaining political choice. / Fund milestones and permit reviewed failure or renegotiation.

Replace: `COLDWAR_VIE_junta_assembly`, `COLDWAR_VIE_junta_mandate`.

### C06 · The frontier army chooses an enduring force structure

| Route | Proposed ID / slot | Advantage | Cost |
|---|---|---|---|
| A Fortified Border Zone | `COLDWAR_VIE_china_static_frontier_zone` [67, 23] | Prepared positions, entrenchment and homeland defence. | Lower offensive flexibility and higher fixed personnel commitments. |
| A Rotational Frontier Army | `COLDWAR_VIE_china_rotational_frontier_army` [69, 23] | Rest, training cycles and a mobile reserve. | Lower maximum prepared defence and repeated rotation costs. |

**Path contract:** Diplomacy remains independently available with actual consent. Permanent institutional design differs from temporary operating programmes; retain expiry and family ownership, with no new CHI-only scalar defence needed.

**Different follow-up decisions:** Fund defensive renewals; terrain training follows the active paid idea. / Choose funded schedules while retaining readiness during talks.

Replace: `COLDWAR_VIE_china_mobilise`, `COLDWAR_VIE_china_opening`.

## Geometry, preservation and uncertainty

A fresh comparison of native source icon alpha bounds and the 164-pixel titlebars found zero card overlaps. The grid is 96 × 130. Political roots are eight columns apart; the junta root is 6144 grid pixels right of the initial Duan root. Retain all eighteen shortcuts. Differentiate short-lived leader footprints, permanent national services and optional operating programmes rather than repeating the same height and gutter everywhere. Do not compact an exclusive pair onto adjacent columns where titlebars overlap.

All 53 existing exclusion pairs are symmetric. Meaningful forks such as actual unification/coexistence, friendly Cambodian partner/direct occupation, and defensive hold/limited counterstroke should remain distinct. The loaded graph is structurally satisfiable; this says nothing about whether every live political or war condition will occur in a normal campaign.

- No compiler or runtime/test runner was executed. Only layout.md and layout.json in this review directory were written.
- Loaded focus AST, actual localization, actual effects/triggers and current main MD references are the evidence. Immutable design JSON identifies group membership, never final modifier values.
- Nominal focus-days equal cost times seven, before external duration modifiers, treasury/party/war waiting and other priorities. Structural histories enforce focus grouping and exclusions, not every live condition.
- Source geometry is not a native screenshot. Connector routing, clipping, hide/refresh behaviour, save behaviour and multiplayer balance remain untested.
- The six pairs are replacement concepts, not twelve new mandatory cards. Their slot positions reuse removed forks after redesign and are not a rendered proposed tree. Exact modifier values/APIs need separate mechanics review.
- Event implementation must show agreed costs/rewards as concrete numeric native option effects, with short English descriptions.
