# Iraq 1970: reward-impact audit

Read-only audit, 19 October 2026. No focus, modifier, history, localization or generator output was changed. Facts below come from the installed mod and installed main MD. Proposed values are tuning suggestions; the historical audit should validate their policy rationale.

## What the source actually contains

426 focuses; 340 with modifier payloads; 22 building focuses; 5 Army-XP focuses; 0 technology-bonus focuses; 0 doctrine-bonus focuses; 46 mutual-exclusion pairs. Bureaucracy appears in148focuses, Stability136, political-power gain88. These are catalogue counts, not a simultaneously playable route.

The first priority is to remove penalty-only filler, make specialist projects produce specialist rewards, and make existing forks meaningfully different. Adding more exclusive forks before fixing these rewards would repeat the same problem.

## Comparable main MD 2000 rewards

| Reference | Focus days | Actual material reward and cost | Gates / source |
|---|---:|---|---|
| `SOV_military_education` | 21 | 35 Army XP, one native officer-training-law upgrade, mobilization_speed variable -0.15; communist government. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:13923` |
| `SOV_aero_improvements` | 21 | 1x25% aircraft research,-10% air accidents, $3bn treasury cost; communist government and UAC prerequisite. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:13269` |
| `SOV_russian_laissez_faire` | 49 | +10% construction,+7% office tax income; oligarch political chain. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_russia.txt:1155` |
| `ISR_deliver_computers` | 35 | 1x25% IT research,$3bn cost; eligible coalition and large Knesset. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:2357` |
| `ISR_assam_ibrahims_mission` | 28 | On accepted cooperation: -100PP,+25ArmyXP,+15CommandPower,1x25%special-forces research,1x25%land doctrine cost reduction. Egypt opinion/existence/peace gates. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_israel.txt:13005` |
| `GER_modernise_mining_equipment` | 45.5 | 1x40%construction research,$10bn treasury cost. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:1976` |
| `GER_german_oilrig_designs` | 40.04 | 2civilian factories,2x50%excavation/refining research plus domestic-influence effect. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\05_germany.txt:180` |
| `TUR_industrial_research` | 40.04 | 2x50%industry research; industrial branch prerequisite. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\turkey.txt:1726` |
| `TUR_turkish_agriculture` | 40.04 | 1civilian factory and1x25%genetics research; agricultural branch prerequisite. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\turkey.txt:2221` |
| `TUR_the_soldiers` | 50.05 | 1x100%infantry research,1x50%land-doctrine cost reduction; ground-forces prerequisite. | `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\turkey.txt:3174` |

Costs use the native 7-days-per-cost-unit convention; fractional focus duration is listed as written rather than pretending to verify a native rounded completion date. These are actual API examples and numerical bounds, not prescriptions to give1970Iraq Germany’s factories or cash. A national `research_speed_factor` and a finite `add_tech_bonus` are different rewards. The Egypt case is an accepted-event preview, not an automatic grant.

## Eight priority findings

### M01 — Remove pure administrative penalties from focus progression (priority1)

**Confirmed:** defence_accounts is 21 days for +2% bureaucracy and no unlock. society_literacy_accounts is 35 days plus 0.5% GDP for +1% bureaucracy and no unlock. industry_survey is 21 days for +2% bureaucracy and a queue-inspection decision. These have no direct positive numerical reward.

**Proposed change:** Merge the survey and accounting steps into the following substantive project. If retained: defence_accounts grants 20 Army XP and removes its +2% bureaucracy; society_literacy_accounts grants one 25% CAT_industry research bonus, removes its +1% bureaucracy and retains 0.5% GDP payment; industry_survey is a 14-day free inspection/unlock, with no permanent malus. These are alternatives to consolidation, not cumulative grants.

**Exact focus IDs:** `COLDWAR_IRQ_defence_accounts`, `COLDWAR_IRQ_society_literacy_accounts`, `COLDWAR_IRQ_industry_survey`.

### M02 — Stop selling stability that the global cap discards (priority1)

**Confirmed:** Positive policy Stability is capped at +0.15 across all eligible programmes; negatives remain in full. Once the sum is already >=0.15, another purely positive Stability contribution changes its allocation but cannot increase the national sum. state_compact gives +0.03 Stability after 49 days and a constitutional review unlock. Many political end focuses also give only +0.03 Stability plus PP/cost modifiers.

**Proposed change:** Keep the cap. Replace late duplicated positive Stability with distinct institutional payoffs. state_compact: bureaucracy -0.06 and tax collection +0.04, no additional Stability, 49 days and unchanged review unlock. baath_future: keep +0.03 PP, replace +0.02 bureaucracy with one 25% CAT_industry bonus. bakr_succession_plan: keep political/transition function, replace +0.03 Stability with +25 command power only if a direct command-power consumer is useful; otherwise shorten to 21 days and retain its actual transition options. Do not manufacture another hidden global bonus cap.

**Exact focus IDs:** `COLDWAR_IRQ_state_compact`, `COLDWAR_IRQ_baath_future`, `COLDWAR_IRQ_bakr_succession_plan`, `COLDWAR_IRQ_saddam_legacy`.

### M03 — Replace global small research bonuses with useful specialist research rewards (priority1)

**Confirmed:** All 426 approved focus payloads together contain zero add_tech_bonus and zero add_doctrine_cost_reduction effects; 25 contain global research_speed_factor. Main MD explicitly uses specialist one-time research bonuses from 10% to 100%, often 25-50%, with 1-2 uses.

**Proposed change:** industry_machine_tools: replace +1% global research with two 35% CAT_industry uses; keep +3% efficiency cap and 2.5% GDP. society_technical_colleges: replace +3% global research with one 50% CAT_construction and one 25% CAT_industry use; keep +3% social expenditure and 3% GDP. defence_air_maintenance: replace +2% global research with one 35% CAT_aircraft use and 15 Air XP; retain +2% bureaucracy and 2.5% GDP. defence_staff_training: 15 -> 35 Army XP and one 25% land_doctrine cost reduction; retain existing +3% organisation,+4% training time and 2% GDP. Verify the downstream technology is visible/unresearched in the actual 1970 save; no free ahead-of-time bypass.

**Exact focus IDs:** `COLDWAR_IRQ_industry_machine_tools`, `COLDWAR_IRQ_society_technical_colleges`, `COLDWAR_IRQ_defence_air_maintenance`, `COLDWAR_IRQ_defence_staff_training`.

### M04 — Make headline exclusive options desirable before their subordinate foci (priority1)

**Confirmed:** 46 exclusive pairs already exist, but many compare +2-5% generic modifiers. industry_heavy is +3% efficiency cap/+2% consumer-goods factor; industry_light is +3% efficiency growth/-2% military factory output. defence_professional is +4% organisation/+6% personnel costs; defence_mass is +6% conscription_factor/-3% organisation. These are not necessarily strictly dominated because descendants and constraints differ, but their headline strategic differences are weak.

**Proposed change:** Use the six complete pairs below rather than increasing every minor reward. Show the branch-specific one-time payoff and enduring policy on the actual choice focus. Audit the complete reachable branch, not just its first node.

**Exact focus IDs:** `COLDWAR_IRQ_industry_heavy`, `COLDWAR_IRQ_industry_light`, `COLDWAR_IRQ_defence_professional`, `COLDWAR_IRQ_defence_mass`, `COLDWAR_IRQ_saddam_guard`, `COLDWAR_IRQ_saddam_regular_army`.

### M05 — Fix cost/reward tempo rather than simply giving every focus more buildings (priority2)

**Confirmed:** The entire Industry catalogue totals 34.5% GDP in frozen one-time invoices, agriculture 30%, oil 29%, society 28%, defence 29.5%. These totals include both mutually exclusive branches and are not a payable single-route bill. A building is granted only after its invoice, control and capacity checks pass. Some offers have additional distinct payments. Industry branch has 686 listed focus-days including alternatives.

**Proposed change:** Consolidate industry_quality and industry_maintenance into one 35-day 2% GDP package: +8% efficiency growth,+2% maximum efficiency,-1% military factory output,+2% bureaucracy. Replace the remaining node with the specialist training bonus in M03 or remove it with preserved existing-save receipts. For defence_readiness: keep the 49-day unlock only if it also gives one-time 25 Army XP. Change its recurring 2% GDP/90-day +3% organisation/+4% army costs cycle to a 0.5% GDP/90-day +8% organisation,+8% recovery,+4% army costs cycle with unchanged 180-day cooldown. No repeatable XP.

**Exact focus IDs:** `COLDWAR_IRQ_industry_quality`, `COLDWAR_IRQ_industry_maintenance`, `COLDWAR_IRQ_defence_readiness`.

### M06 — Give recurring bureaucracy taxes a specific purpose and a route to completion (priority2)

**Confirmed:** 148 of 426 focus payloads modify bureaucracy expenditure, overwhelmingly adding +1-6% as a generic downside. 88 modify PP and 136 Stability. The pattern makes very different ideologies feel mechanically similar and can leave reforms more administratively expensive without a visible service improvement. MD reader multiplies the bureaucracy spending array by 1 + modifier; it does not directly raise tax receipts or improve institutions.

**Proposed change:** Use a small number of explicit funded institutions instead of a new permanent bureaucracy malus on every step. Example: courts_budget becomes one 35-day 1.5% GDP package tax +0.05, bureaucracy +0.02. budget_accounts becomes tax +0.04 and bureaucracy -0.03, 0.5% GDP, replacing its PP -0.02. Preserve non-identical historical tradeoffs; do not stack this example with an unchanged final state_compact reward until whole-route totals are recalculated.

**Exact focus IDs:** `COLDWAR_IRQ_courts_budget`, `COLDWAR_IRQ_budget_accounts`, `COLDWAR_IRQ_baath_accounts`, `COLDWAR_IRQ_bakr_continuity`, `COLDWAR_IRQ_society_municipal_finance`.

### M07 — Do not mistake export and relative-cost modifiers for production or percentage points (priority2)

**Confirmed:** oil_export_multiplier_modifier feeds exported oil quantity times market price times additive export multiplier. It produces no benefit without actual oil exports, and creates neither resources nor infrastructure. consumer_goods_factor multiplies consumer_goods_expected_value; +0.02 is a 2% relative factor, not +2 percentage points of factories. army_personnel_cost_multiplier_modifier multiplies the army wage component, not every military expense or all national expenditure.

**Proposed change:** For an oil-export path, retain genuine exports as the main incentive but pair it with real infrastructure/refining research so embargoed Iraq has a meaningful alternative. Use the oil pair below. Preserve the existing exceptionally expensive actual Iran-war wage/equipment escalation; do not describe a +6% ordinary focus wage modifier as the mechanism that creates that crisis.

**Exact focus IDs:** `COLDWAR_IRQ_oil_revenue_state`, `COLDWAR_IRQ_oil_diversification`, `COLDWAR_IRQ_war_economy`, `COLDWAR_IRQ_agri_large_irrigation`.

### M08 — Keep strong territorial/crisis payoffs and improve decision-unlock staging (priority2)

**Confirmed:** The 1970 package already includes actual Khuzestan claim/war goal/core and Kuwait invasion/core/debt-crisis relief. US Gulf focuses intentionally unlock consent-dependent operations; they are not all empty numeric foci. Desert Storm grants its actual liberation war goal in 14 days. Northern air readiness already gives +15% interception,+10% air superiority efficiency,+15% air personnel costs for90days, and accepted recipient cover gives +25%CASdamage reduction/-20%enemy air-superiority effect/+5%army personnel costs.

**Proposed change:** Do not inflate these existing major prizes. In the US tree, merge contacts plus appeal if their separate completion only adds extra clicks before the same paid intervention. Make limited_war versus arm_front a visibly consequential commitment: limited_war may offer a consent-based 30-day actual war/ceasefire negotiation channel plus recipient-paid reconstruction; arm_front retains the actual weapons/underground budget and risks rebellion. No automatic peace, unwilling allies, free troops or remote air ban. Preserve all current genuine crisis and consent gates. Exact new diplomatic costs require the historical/MP review before implementation.

**Exact focus IDs:** `COLDWAR_IRQ_iran_final_ultimatum`, `COLDWAR_IRQ_iran_core_khuzestan`.

## Six concrete exclusive choices

Each row changes an existing pair; it does not require inventing six new political gates. Exact current values, existing prerequisite groups, costs, exclusions and replacement flags are preserved in the companion mechanics.json for review. Proposed values replace current bundles unless explicitly described as a follow-up. A recurring political programme remains conditional on its actual party/leader; buildings, XP, literacy and consumed research bonuses are durable, one-time outcomes.

### P1 — State heavy industry or consumer expansion

Heavy industry strengthens domestic military supply and long production runs; a consumer-led programme expands the civilian construction base. Neither branch receives both payoffs; keep industry_steel/consumers follow-ups only after checking total assets.

**Heavy Industry** (`COLDWAR_IRQ_industry_heavy`)

```json
{
  "days": 49,
  "budget_gdp_share": 0.03,
  "modifiers": {
    "production_factory_max_efficiency_factor": 0.1,
    "industrial_capacity_factory": 0.05,
    "consumer_goods_factor": 0.02
  },
  "tech_bonus": {
    "category": "CAT_industry",
    "bonus": 0.35,
    "uses": 1
  }
}
```

**Light Industry** (`COLDWAR_IRQ_industry_light`)

```json
{
  "days": 49,
  "budget_gdp_share": 0.04,
  "modifiers": {
    "production_speed_buildings_factor": 0.08,
    "bureaucracy_cost_multiplier_modifier": 0.02
  },
  "building": [
    166,
    "industrial_complex",
    1
  ]
}
```

### P2 — Professional cadre or national reserve

A smaller better-trained army versus deeper replacements and recovery. Conscription factor is a relative manpower modifier; do not label it fifteen percentage points of population.

**A Professional Core** (`COLDWAR_IRQ_defence_professional`)

```json
{
  "days": 35,
  "budget_gdp_share": 0.01,
  "modifiers": {
    "army_org_factor": 0.08,
    "training_time_army_factor": -0.1,
    "army_personnel_cost_multiplier_modifier": 0.06
  },
  "army_xp": 25
}
```

**A Mass Reserve Army** (`COLDWAR_IRQ_defence_mass`)

```json
{
  "days": 35,
  "budget_gdp_share": 0.01,
  "modifiers": {
    "conscription_factor": 0.15,
    "army_morale_factor": 0.08,
    "army_org_factor": -0.03
  },
  "army_xp": 25
}
```

### P3 — Guard-centered deterrence or a stronger regular army

The guard option concentrates expensive readiness; regular-army institutions improve sustained recovery and replacement training. These are explicitly national abstractions; this code does not restrict an org bonus to actual guard divisions.

**Presidential Guard** (`COLDWAR_IRQ_saddam_guard`)

```json
{
  "days": 35,
  "budget_gdp_share": 0.02,
  "modifiers": {
    "army_org_factor": 0.08,
    "army_defence_factor": 0.04,
    "army_personnel_cost_multiplier_modifier": 0.1
  }
}
```

**The Regular Army** (`COLDWAR_IRQ_saddam_regular_army`)

```json
{
  "days": 35,
  "budget_gdp_share": 0.02,
  "modifiers": {
    "army_org_factor": 0.04,
    "army_morale_factor": 0.1,
    "training_time_army_factor": -0.12,
    "army_personnel_cost_multiplier_modifier": 0.04
  }
}
```

### P4 — Rapid adult literacy or teacher-led technical education

Mass campaigns yield immediate broad basic skills; slower teacher formation supports research and technical training. Preserve native literacy penalties and thresholds, no duplicate literacy spirit penalty or auto-reset on party change.

**Mass Literacy** (`COLDWAR_IRQ_society_mass_literacy`)

```json
{
  "days": 35,
  "budget_gdp_share": 0.025,
  "modifiers": {
    "social_cost_multiplier_modifier": 0.03
  },
  "instant": [
    "set_temp_variable = { LR_change = 0.06 }",
    "update_literacy_rate = yes"
  ],
  "follow_up": "evening_classes remains +0.02 literacy, rather than also boosting every schooling focus"
}
```

**Train Teachers First** (`COLDWAR_IRQ_society_teacher_first`)

```json
{
  "days": 35,
  "budget_gdp_share": 0.025,
  "modifiers": {
    "research_speed_factor": 0.05,
    "social_cost_multiplier_modifier": 0.03
  },
  "tech_bonus": {
    "category": "CAT_industry",
    "bonus": 0.25,
    "uses": 1
  },
  "follow_up": "teacher_deployment remains +0.035 literacy"
}
```

### P5 — Export revenue now or diversify the economy

Oil receipts fund an immediate rentier model only while actual exports continue. Diversification purchases permanent non-oil capacity at a cash cost and foregoes some current export income. Do not claim exports create oil resources.

**An Oil Revenue State** (`COLDWAR_IRQ_oil_revenue_state`)

```json
{
  "days": 35,
  "budget_gdp_share": 0,
  "modifiers": {
    "oil_export_multiplier_modifier": 0.18,
    "tax_gain_multiplier_modifier": -0.03
  }
}
```

**Beyond Oil** (`COLDWAR_IRQ_oil_diversification`)

```json
{
  "days": 49,
  "budget_gdp_share": 0.04,
  "modifiers": {
    "production_speed_buildings_factor": 0.08,
    "oil_export_multiplier_modifier": -0.03
  },
  "building": [
    557,
    "industrial_complex",
    1
  ]
}
```

### P6 — Coalition institutions or party-state concentration

A coalition recruits specialists and productive expertise while requiring administrative coordination; concentrated party rule yields political capacity and ideological entrenchment with narrower research freedom. Keep the actual opposition/legalization consent system. These are balance abstractions, not claims that an authoritarian option is harmless.

**National Front** (`COLDWAR_IRQ_national_front`)

```json
{
  "days": 35,
  "budget_gdp_share": 0.01,
  "modifiers": {
    "production_factory_efficiency_gain_factor": 0.1,
    "research_speed_factor": 0.04,
    "bureaucracy_cost_multiplier_modifier": 0.03
  },
  "replace_current_stability_and_pp": true
}
```

**Exclusive Party State** (`COLDWAR_IRQ_baath_monopoly`)

```json
{
  "days": 35,
  "budget_gdp_share": 0,
  "modifiers": {
    "political_power_factor": 0.15,
    "drift_defence_factor": 0.15,
    "research_speed_factor": -0.03
  },
  "replace_current_stability_and_pp": true
}
```

## Native mechanics, scope and reader evidence

**Economic effects are not inferred from their names.** Bureaucracy adds to a national wage/spending factor; tax collection adds to relevant income multipliers; army personnel costs affect the actual army wage component; oil-export modifiers change revenue from actual exports; consumer_goods_factor scales the expected consumer-goods share. None is a flat treasury transfer or a direct state building grant.

- bureaucracy: `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\scripted_effects\00_money_system.txt:3267` — `value = 1 add = modifier@bureaucracy_cost_multiplier_modifier`
- tax: `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\scripted_effects\00_money_system.txt:406` — `add = modifier@tax_gain_multiplier_modifier`
- army_cost: `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\scripted_effects\00_money_system.txt:3140` — `army_personnel_cost_multiplier = { value = 1`
- oil_export: `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\scripted_effects\00_money_system.txt:4456` — `oil_export_multiplier = { value = resource_export_multiplier`
- consumer_goods: `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\scripted_effects\00_money_system.txt:4606` — `actual_consumer_goods_percent_display = {`
- agriculture: `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\scripted_effects\00_money_system.txt:389` — `value = modifier@agricolture_productivity_modifier`
- literacy: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\scripted_effects\00_education_effects.txt:166` — `update_literacy_rate = {`
- officer_law_provider: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\scripted_effects\00_military_effects.txt:309` — `increase_officer_training_level = {`
- industrial_research_1970_targets: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\technologies\mdcw_historical_industry.txt:26` — `categories = { CAT_civilian CAT_industry CAT_construction }`
- infantry_research_1970_targets: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\technologies\mdcw_early_infantry.txt:109` — `categories = { CAT_military CAT_infantry CAT_body_armor }`
- aircraft_research_1970_targets: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\technologies\mdcw_historical_air_naval.txt:22` — `categories = { CAT_military CAT_aircraft CAT_medium_aircraft }`
- artillery_research_1970_targets: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\technologies\mdcw_historical_land.txt:140` — `CAT_artillery`
- stability_cap: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\common\scripted_effects\COLDWAR_IRQ_1970_programmes.txt:7584` — `set_variable = { COLDWAR_IRQ_positive_stability = 0 }`
- programme_owner: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\tools\iraq_1970\common.py:41` — `def group_gate(key):`
- invoice: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\tools\iraq_1970\common.py:16` — `def invoice(key,share):`
- review_switch: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\tools\iraq_1970\decisions_module.py:110` — `def policy_menu(group):`
- readiness: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\tools\iraq_1970\decisions_module.py:320` — `register('defence_readiness_cycle'`
- us_unlock_provider: `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar\tools\iraq_1970\usa_module.py:769` — `def _focuses(data, out, loc)`

**Engine-owned modifiers:** organisation, recovery, training time, military output, construction speed, efficiency cap, research speed and relative conscription factor already occur in loaded IRQ programmes and/or the cited MD Russia code. The consumer is native HOI4, so a script search cannot independently prove its engine formula. Keep the exact registered native key, unit and national scope. A -10% training-time modifier is beneficial; +4% training time is slower training. A +15% conscription_factor is relative, not +15 percentage points of population.

**Research provider and consumers:** use native add_tech_bonus with a unique COLDWAR key and actual technology categories. The target1970extension has industry/construction, infantry, artillery and aircraft targets at the anchors above. Broader CAT_industry can be consumed by many technologies; specific category availability must be checked in the actual save before finalizing. Use add_doctrine_cost_reduction for land_doctrine, as in Israel/Turkey, rather than relabeling a technology bonus as doctrine. No automatic technology grant or ahead-of-time bypass is proposed.

**Physical project boundary:** native add_building_construction belongs in owned, controlled state scope; retain free-capacity checks and a single successful delivery receipt. Credit the selected branch only once. A policy-review decision changes selected programme flags; it must never repeat buildings, stockpiles, research, XP or literacy. Main MD random-factory helpers are references, not a reason to ignore Iraqi state capacity.

**Costs and net-route review:** invoice amounts are frozen from positive live GDP once; payment and rewards are deferred together when unaffordable or blocked. A focus finishing does not alone prove its package was paid and implemented. GDP percentages above are one-time treasury costs, distinct from recurring national spending. The summed catalogue invoice totals include exclusive alternatives and are not a real route affordability calculation. Test one1970start plus 1974/1980wartime budgets after choosing compatible paths; no current report proves those balances.

## What not to increase

Keep the Khuzestan and Kuwait territorial rewards and the genuine war-spending/debt crisis. They already have campaign-sized consequences. Keep US intervention player consent, real equipment and aircraft requirements, and the actual14-day Desert Storm war goal. Do not add a remote geographic no-fly ban or a national Iraqi -100%aircraft penalty. Strengthen the weak economic/political programme choices around these major objectives.

## Validation boundary

This audit reads the current frozen catalogue, compiler, runtime programmes, decision providers, native main MD rewards and formula consumers. It does not certify native tooltips, fresh balance, US/IRQ multiplayer decisions or a completed1970campaign. Source consistency and actual gameplay balance remain separate checks. Historical explanations in proposed pair rationales are design inferences awaiting the parallel historical audit.

## Addendum: compatible-route stacking check (19 October 2026)

These are two explicit compatible examples, not maxima and not totals over every tree. The prerequisite closure was calculated from the approved JSON, with every OR group choosing one reachable predecessor and every mutually exclusive opposite rejected. Only state, Baath, Saddam, shared Defence, War and Iran-war groups enter; no al-Bakr/officer/Communist/other government programmes are added. Saddam and Baath are actually governing. All listed focus packages are assumed implemented and their required current war conditions fulfilled. No policy respec, ally bonus, generic MD law, trait, technology or national spirit outside the explicitly named additions is silently counted.

Values below are **additive native modifier contributions**, not final division stats. Negative training time is faster. Positive personnel values increase the army wage component. The proposal is exactly P2/P3 above plus unchanged military follow-ups; the M05 readiness change is shown separately.

| Example route | Organisation current -> proposed | Recovery current -> proposed | Training time current -> proposed | Army personnel costs current -> proposed | Supply use current -> proposed | Army fuel current -> proposed |
|---|---:|---:|---:|---:|---:|---:|
| A: Peacetime Baath/Saddam professional army with Guard | +15% -> +24% | +3% -> +3% | +4% -> -6% | +25% -> +27% | -10% -> -10% | -4% -> -4% |
| B: Baath/Saddam regular-army long Iran war | +24% -> +28% | +6% -> +16% | +9% -> -18% | +64% -> +68% | -12% -> -12% | -4% -> -4% |

**Route A with the recurring readiness cycle active:** organisation +18% -> +32%; recovery +3% -> +11%; training time +4% -> -6%; army wage modifier +29% -> +31%. The default unresolved northern/frontier spirits add a further +15% army wage modifier to both versions: +44% -> +46%, provided neither situation has been settled. Patronage’s -5% organisation is already removed by professional_command; it is not subtracted again.

**Route B with the recurring readiness cycle active:** organisation +27% -> +36%; recovery +6% -> +24%; training time +9% -> -18%; army wage modifier +68% -> +72%. If this is a >=365-day actual Iran war with the default +15% northern/frontier wage burden and +12% attrition-bill wage burden, the +250% third war-spending tier adds on top: shown contributions total +345% -> +349% army wages (4.45 -> 4.49 times that component before other modifiers), not +345% national expenditure. Equipment costs and offensive supply/fuel burdens are separate; no temporary offensive or follow-up bill is included here. Therefore modest ordinary focus wage penalties do not balance a new huge combat stack by themselves.

**Risk:** P2+P3+the proposed readiness cycle accumulate too much generic organisation/recovery/training improvement. On route A the proposed +8% professional army, +8% Guard, +5% state command and +3% staff already produce +24% permanent organisation. Route B shifts training by 27 modifier points (+9% -> -18%) while potentially quadrupling recovery (+6% -> +24%) during readiness. These remain engine-supported values, but this audit does not recommend shipping all headline suggestions unchanged.

**Recommended resolution:** establish one explicit, visibly named army-organisation reform package for professional/Guard/regular approaches. Select/replace its base contribution instead of silently stacking separate +8% sources. For example, professional contributes +5% org; the Guard-selected variant replaces that +5% with +8% (a net +3%, not another +8%); the regular-army variant retains +5% org but adds recovery +6% and training -8%. Staff training keeps one-time XP/doctrine and its genuine existing training trade-off, but its +3% organisation is incorporated into that package rather than an extra lifetime bonus. State professional_command removes the patronage organisation penalty; its existing +3% extra organisation can also be folded into the same visible institutional package. A staffed headquarters is the same army, not three different armies. This is an explicit replacement/priority relationship with transparent tooltips, not a new hidden cap. Keep the national guard abstraction truthful.

**Readiness revision after the stacking check:** reduce the earlier M05 proposal to +4% organisation and +4% recovery for90days, +4% personnel cost, 0.5% GDP and unchanged180-day cooldown; or retain +8% readiness organisation only when it explicitly replaces the peacetime readiness part of the same package. Never add permanent combat modifiers to disguise a weak renewable contract. Recalculate the exact adopted slot configuration before implementation.

**Side-effect ownership:** original research/XP and durable physical projects stay once-only. A policy review/leadership return must never deliver them twice. The proposed priority slot changes how overlapping military institutions are represented, not the native war-cost escalation, player sovereignty or previous building receipts.

### Route A: exact prerequisite closure (37 focuses)

`COLDWAR_IRQ_arab_socialism`, `COLDWAR_IRQ_army_command_review`, `COLDWAR_IRQ_baath_accounts`, `COLDWAR_IRQ_baath_congress`, `COLDWAR_IRQ_baath_future`, `COLDWAR_IRQ_baath_monopoly`, `COLDWAR_IRQ_cadre_party`, `COLDWAR_IRQ_civil_register`, `COLDWAR_IRQ_defence_accounts`, `COLDWAR_IRQ_defence_air_maintenance`, `COLDWAR_IRQ_defence_fuel_discipline`, `COLDWAR_IRQ_defence_land_schools`, `COLDWAR_IRQ_defence_logistics`, `COLDWAR_IRQ_defence_procurement_board`, `COLDWAR_IRQ_defence_professional`, `COLDWAR_IRQ_defence_soviet_offer`, `COLDWAR_IRQ_defence_soviet_standard`, `COLDWAR_IRQ_defence_staff_training`, `COLDWAR_IRQ_enterprise_accounts`, `COLDWAR_IRQ_executive_state`, `COLDWAR_IRQ_ministerial_audit`, `COLDWAR_IRQ_party_schools`, `COLDWAR_IRQ_professional_command`, `COLDWAR_IRQ_provincial_agents`, `COLDWAR_IRQ_rcc_rules`, `COLDWAR_IRQ_regional_command`, `COLDWAR_IRQ_review_detentions`, `COLDWAR_IRQ_saddam_bounded_deterrence`, `COLDWAR_IRQ_saddam_guard`, `COLDWAR_IRQ_saddam_guard_supply`, `COLDWAR_IRQ_saddam_iran_dossier`, `COLDWAR_IRQ_saddam_party_cabinet`, `COLDWAR_IRQ_saddam_presidency`, `COLDWAR_IRQ_saddam_regional_role`, `COLDWAR_IRQ_saddam_social_contract`, `COLDWAR_IRQ_saddam_technocrats`, `COLDWAR_IRQ_security_priority`.

### Route B: exact prerequisite closure (58 focuses)

`COLDWAR_IRQ_arab_socialism`, `COLDWAR_IRQ_army_command_review`, `COLDWAR_IRQ_baath_accounts`, `COLDWAR_IRQ_baath_congress`, `COLDWAR_IRQ_baath_future`, `COLDWAR_IRQ_baath_monopoly`, `COLDWAR_IRQ_cadre_party`, `COLDWAR_IRQ_civil_register`, `COLDWAR_IRQ_defence_accounts`, `COLDWAR_IRQ_defence_air_maintenance`, `COLDWAR_IRQ_defence_fuel_discipline`, `COLDWAR_IRQ_defence_land_schools`, `COLDWAR_IRQ_defence_logistics`, `COLDWAR_IRQ_defence_procurement_board`, `COLDWAR_IRQ_defence_professional`, `COLDWAR_IRQ_defence_soviet_offer`, `COLDWAR_IRQ_defence_soviet_standard`, `COLDWAR_IRQ_defence_staff_training`, `COLDWAR_IRQ_enterprise_accounts`, `COLDWAR_IRQ_executive_state`, `COLDWAR_IRQ_iran_another_offensive`, `COLDWAR_IRQ_iran_arabistan_claim`, `COLDWAR_IRQ_iran_campaign_accounts`, `COLDWAR_IRQ_iran_final_ultimatum`, `COLDWAR_IRQ_iran_frontier`, `COLDWAR_IRQ_iran_launch_campaign`, `COLDWAR_IRQ_iran_long_war`, `COLDWAR_IRQ_iran_mobilisation_base`, `COLDWAR_IRQ_iran_no_easy_exit`, `COLDWAR_IRQ_iran_operational_plan`, `COLDWAR_IRQ_iran_shatt_demand`, `COLDWAR_IRQ_iran_southern_command`, `COLDWAR_IRQ_iran_sustained_war`, `COLDWAR_IRQ_iran_tehran_assessment`, `COLDWAR_IRQ_iran_war_contracts`, `COLDWAR_IRQ_iran_war_of_reserves`, `COLDWAR_IRQ_ministerial_audit`, `COLDWAR_IRQ_party_schools`, `COLDWAR_IRQ_professional_command`, `COLDWAR_IRQ_provincial_agents`, `COLDWAR_IRQ_rcc_rules`, `COLDWAR_IRQ_regional_command`, `COLDWAR_IRQ_review_detentions`, `COLDWAR_IRQ_saddam_bounded_deterrence`, `COLDWAR_IRQ_saddam_iran_dossier`, `COLDWAR_IRQ_saddam_party_cabinet`, `COLDWAR_IRQ_saddam_presidency`, `COLDWAR_IRQ_saddam_regional_role`, `COLDWAR_IRQ_saddam_regular_army`, `COLDWAR_IRQ_saddam_social_contract`, `COLDWAR_IRQ_saddam_staff_college`, `COLDWAR_IRQ_saddam_technocrats`, `COLDWAR_IRQ_security_priority`, `COLDWAR_IRQ_war_civil_continuity`, `COLDWAR_IRQ_war_contingency`, `COLDWAR_IRQ_war_deliberate_authority`, `COLDWAR_IRQ_war_economy`, `COLDWAR_IRQ_war_offensive_option`.

### Consolidated Heavy/Light proposal from the main audit

**Acceptable design shape:** Heavy + steel become one49-day package,5%GDP,one civilian factory in557,+10%efficiency cap,+5%military factory output,one35%industry research use,+2%relative consumer-goods factor. Light + consumers become one49-day package,4%GDP,one civilian factory in166,+8%construction,+2%bureaucracy. Move the existing follow-up factory into the headline package; do not award a second factory. Both branches grant one physical factory in total.

Relative to the current two-focus routes, Heavy falls from84days and7%GDP to49days and5%GDP; Light from84days and5.5%GDP to49days and4%GDP, while gaining stronger policy rewards. That is already a substantial combined tempo/cost buff. The extra1%GDP buys Heavy a specialised production/research package, whereas Light’s immediate construction multiplier strengthens the civilian build-up. +10%efficiency cap is not an instant+10%output increase; it pays back with sustained production and combines with+5%output. +2%CG is relative expected-goods scaling, usually a modest bill rather than two full factory-percentage points. These look like desirable distinct routes, subject to a native1970affordability and production-run check. They should replace the original separate Heavy/steel and Light/consumers grants, not stack with them. No additional factory or later same-project delivery may remain.

## Superseding military balance recommendation: conservative direct replacements

This is the final numerical recommendation for review and supersedes the stronger P2/P3 and readiness suggestions above. It uses the existing focus programme contributions directly; it does not add a bonus cap, abstract law or new priority-slot mechanism. All programme eligibility, exclusivity, one-time receipts and ordinary native effects remain explicit.

- Professional army: +8% organisation,+25ArmyXP,+6%army personnel costs,1%GDP; **no new training-time bonus**.
- National reserve: +15%relative conscription factor,+8%recovery,-3%organisation,+25ArmyXP,1%GDP.
- Guard: +3%organisation,+4%defence,+10%army personnel costs,2%GDP. This remains an explicitly national abstraction.
- Regular army: remove its previous+4%organisation; instead +6%recovery,-8%training time,+4%army personnel costs,2%GDP.
- Staff training: remove its previous+3%organisation; grant35ArmyXP and one25%land_doctrine cost reduction; keep+4%training time and2%GDP.
- State organisation rewards remain unchanged.
- Renewable readiness: +4%organisation,+4%recovery,+4%army personnel costs for90days,0.5%GDP,180-daycooldown. No repeatable XP or research.

| Exact compatible route | Organisation | Recovery | Training time | Army personnel cost |
|---|---:|---:|---:|---:|
| A | +16% | +3% | +4% | +27% |
| A + readiness | +20% | +7% | +4% | +31% |
| B | +21% | +12% | -4% | +68% |
| B + readiness | +25% | +16% | -4% | +72% |

The37-focus routeA and58-focus routeB closures above were reused unchanged, so these numbers do not mix exclusive Guard/regular branches, incompatible parties or short/long Iran plans. Personnel totals still exclude the separately described starting situation and actual war-escalation ideas. Specialist experience/doctrine rewards are one-time benefits and are not added to recurring organisation totals.

**Assessment:** plausible, audit-ready replacement for the earlier excessive stacks. RouteA gains one organisation modifier point before readiness instead of nine; RouteB loses three organisation points but obtains six recovery points and improves training by thirteen points, creating a distinct regular-army payoff. Staff training offers real XP/doctrine without another permanent organisation layer. This is source-arithmetic clearance, not an engine/campaign-balance certification. Native tooltip, affordability and representative combat tests remain implementation checks.
