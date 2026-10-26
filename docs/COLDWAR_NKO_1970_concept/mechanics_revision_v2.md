# NKO 1970 concept — mechanics revision v2

This note records source-checked mechanics and concrete concept corrections for the next NKO design revision. It does not edit the concept JSON, generator, or loaded game files. All paths and line numbers refer to the current target checkout unless marked donor.

## Decisive corrections

- Artillery uses `army_artillery_attack_factor` and `army_artillery_defence_factor`; do not use `army_attack_factor` to represent an artillery-specific benefit. These exact keys appear in MD ideas (`common/ideas/05_netherlands.txt:433-434`) and army leader traits (`common/unit_leader/01_army_leader_traits.txt:1551,1567`). The current Artillery Concentration reward uses broad `army_attack_factor = 0.06`; replace it with `army_artillery_attack_factor = 0.06` (or split a smaller amount across attack and defence).
- A building level and its slot belong in the same state scope: apply `add_extra_state_shared_building_slots = N` for the number of granted levels, then add those levels with `add_building_construction`. MD does both in one state in `common/scripted_effects/00_internal_investment_automation_effects.txt:76-88` and `common/scripted_effects/00_scripted_effects.txt:8-10`.
- Cash costs should be a proportion of the payer’s current `gdp_total`. A native focus pattern is `set_temp_variable = { treasury_change = { value = gdp_total multiply = -0.005 } }` followed by `modify_treasury_effect = yes` (`common/national_focus/00_generic.txt:625,1999`). The treasury/debt system uses billion-dollar cash units (`common/scripted_effects/00_economic_system_utilities.txt:253-274`); the multiplier is dimensionless, so `.005` charges 0.5% of GDP. Do not store one fixed $1–8.5 billion amount as the cost for every NKO.
- A sender focus may open an external offer, but acceptance must be a decision in the recipient’s decision category. The native Spain V2 arrangement currently uses a sender-targeted decision and a recipient reply event (`common/decisions/COLDWAR_SPR_v2_agreements.txt:91-120`, `events/COLDWAR_SPR_v2_agreements.txt:25-40`); the recipient-decision UI requested for this concept needs a different acceptance surface.
- Each accepted external agreement grants a paired, perpetual modifier—one on each country. Both copies must test the same shared agreement receipts, no mutual war, and no direct Imperia sanctions in either direction. Do not grant one side’s spirit from a recipient decision and omit the partner.
- Add a dedicated NKO route against KOR. The supported native focus form is `will_lead_to_war_with = KOR` plus a completion reward `create_wargoal = { type = annex_everything target = KOR }`, both used in `common/national_focus/03_china_north_korea_joint.txt:1985,2018-2020`. This grants a wargoal; it does not declare war automatically.

## Military modifier audit: all 20 current defence focuses

The keys below exist in current MD providers. “Specific” describes the target of the bonus; broad operational modifiers remain suitable where the focus actually concerns the whole force.

| Focus | Current modifier evidence | Mechanics revision |
|---|---|---|
| Lessons of 1969 | `experience_gain_army` and personnel cost | Supported; it is an army-wide staff/training effect. |
| The Fortress State | `army_core_defence_factor`, supply, broad attack and productivity | Supported. Its broad `army_attack_factor` penalty can remain if the intended trade-off applies to the whole army; use artillery-specific modifiers only if the text singles out artillery. |
| A Mobile Field Army | `army_org_factor`, planning, equipment cost, `army_fuel_consumption_factor` | Supported. If the promise is specifically motorized-infantry combat, use the registered subunit keys `modifier_army_sub_unit_Mot_Inf_Bat_attack_factor` / `_defence_factor`, not an invented `army_motorized_attack_factor`. |
| Worker-Peasant Guards | Core defence, training time, productivity | Supported. If the named militia/infantry formations should fight better, `army_infantry_defence_factor` is native (e.g. `common/unit_leader/01_army_leader_traits.txt:1226`). |
| General Staff College | Planning, army experience, education cost | Supported; `experience_gain_army` and `max_planning_factor` are broad operational effects. |
| Reorganize Command | Army organization and bureaucracy cost | Supported; national army-wide effect. |
| Artillery Concentration | Currently `army_attack_factor = 0.06` | **Correct the benefit** to `army_artillery_attack_factor = 0.06`. Native paired attack/defence usage is shown in `common/ideas/05_netherlands.txt:433-434`. Its supply and equipment costs may remain. |
| Air Defence Commands | `air_mission_efficiency` and equipment cost | Use `air_interception_detect_factor` for interception readiness/detection (native examples: `common/ideas/Algerian.txt:2504-2540`); use `air_detection` only for broad air detection (e.g. `common/ideas/05_netherlands.txt:432`). `air_defence_factor` is the aircraft's `AircraftDefense` stat and does not mean land AA strength or interception efficiency. |
| Coastal Denial | Naval organization and equipment cost | Supported as a fleet-wide benefit. If it promises a particular class, use native class modifiers such as `navy_screen_defence_factor`, `navy_submarine_attack_factor`, or `navy_anti_air_attack_factor`; MD uses these in `common/ideas/05_france.txt:19-20` and `common/ideas/Algerian.txt:3859`. |
| Special Operations | Special-forces cap, personnel cost, army organization | Supported. The cap expands capacity, not special-forces combat stats. For an actual unit benefit, use registered `modifier_army_sub_unit_Special_Forces_attack_factor` / `_defence_factor`, present in `common/units/unit_modifiers/unit_modifiers.txt:56-59` and used in `common/ideas/05_france.txt:346-347`. |
| Ammunition Standards | Production efficiency cap and efficiency growth | Supported factory-production effects, not a unit attack bonus. The text should promise manufacturing reliability/capacity, or add a supported artillery category effect if combat improvement is intended. |
| Air Warning Network | Radar building | The building is supported; add one shared building slot in the radar’s selected state for each radar level. |
| Naval Workshops | Dockyard building | The building is supported; add one shared building slot in that same coastal state for each dockyard level. |
| Reconnaissance Plan | Planning and personnel cost | Supported army-wide planning effect. |
| Joint Logistics | Supply consumption and bureaucracy cost | Supported army-wide supply effect. |
| Workshop Conversion | Civilian/military factory construction speed and equipment cost | Supported economy/construction effects; it does not directly improve unit combat. |
| Arsenal Priority | Industrial output, industrial construction, electricity use | Supported industrial effects; distinguish factory output from unit attack in the text. |
| A Maintained Reserve | Organization and personnel cost | Supported army-wide readiness/maintenance effects. |
| Military Institutes | Research and education cost | Supported research/training-institution effects. |
| Readiness Inspections | Organization and `training_time_factor = 0.04` | The key is supported, but a positive time factor lengthens training. If this is a penalty, disclose it; if it is intended to speed readiness, use a small negative value. |

Native unit-specific national keys include `army_artillery_attack_factor` / `army_artillery_defence_factor`, `army_infantry_attack_factor` / `_defence_factor`, and `army_armor_attack_factor` / `_defence_factor` (see the Netherlands ideas, Chinese leader traits, and French ideas cited above). The target separately registers subunit keys in `common/units/unit_modifiers/unit_modifiers.txt:21-26,56-59`; examples include `modifier_army_sub_unit_L_Inf_Bat_attack_factor`, `modifier_army_sub_unit_Mot_Inf_Bat_attack_factor`, and the special-forces pair. Their idea usage is verifiable in `common/ideas/united_states.txt:1088-1107,1369-1383`. The registered subunit list has no artillery subunit modifier, so use the national `army_artillery_*` keys for artillery rather than inventing `modifier_army_sub_unit_artillery_*`.

The 20 current modifiers are syntactically represented by existing MD sources, but this static audit does not prove final in-game tooltips or combat calculations. The clear content defect is Artillery Concentration’s broad attack key; other combat-specific alternatives above depend on the intended prose.

## GDP-based costs and equal building slots

MD uses `gdp_total` directly to compute focus cash costs and posts those costs through the normal Treasury helper. Examples in `common/national_focus/00_generic.txt` include 0.1% (`:2019`), 0.5% (`:625,1999`), 0.7% (`:3294,3337`), 1.5% (`:247`), and 3% (`:2155`) of GDP. These establish a live API and a usable scale, not an instruction to price each NKO focus at the maximum.

Suggested starting price bands for the concept, charged once on completion:

- Small advisory, research, or administrative programme: 0.1–0.3% of payer GDP.
- Normal institutional or military programme: 0.3–0.75% of payer GDP.
- Major physical project: 0.75–2% of payer GDP per level; 3% is a high-end one-off ceiling, not a routine price.

These bands keep concept focus costs within the scale of existing GDP-multiplier focus rewards while allowing buildings to remain more expensive than policy choices. Calibrate each against the 1970 GDP and the combined cost of reachable routes. Offer prices must be quoted from the payer’s GDP when sent and stored for recipient acceptance, so the sender and recipient see and pay the same amount even if GDP changes before the decision is clicked. Each country transfer should charge its payer, not the NKO focus owner by default.

For one level in a state, the concept implementation shape is:

```hoi4
state = {
    # candidate-state ownership/control and room checks go here
    add_extra_state_shared_building_slots = 1
    add_building_construction = {
        type = industrial_complex
        level = 1
        instant_build = yes
    }
}
```

For N granted levels, add N shared slots and N building levels in the **same selected state**. Verify ownership, control, building cap, and construction capacity at reward time. The `add_building_construction` shape and slot pairing are native (`common/scripted_effects/00_scripted_effects.txt:8-10,29-30`); the exact per-focus selector remains a new helper.

For a normal one-time GDP charge, do not add an affordability gate: the existing weekly `automated_debt_taker` covers a negative Treasury (`common/scripted_effects/00_economic_system_utilities.txt:29-40`; invoked at `common/on_actions/MD_on_actions.txt:170`). A separately negotiated foreign loan must be separately recorded as principal and cash proceeds. Acceptance of the NKO 7.5% GDP-equivalent machinery quote should credit the quoted cash principal, add the same principal to debt, then debit the full project price once. This leaves the project cash-neutral only when the quoted principal equals its quoted project price. Repayment must debit at most `min(outstanding principal, available Treasury)` and reduce debt by exactly that amount.

## External offers: recipient decisions, paired perpetual spirits

MD has a standard decision category and ordinary `visible` / `available` / `complete_effect` decisions (e.g. `common/decisions/05_north_korea.txt:1-30` and `common/decisions/categories/COLDWAR_SPR_v2_agreements.txt:2`). Spain V2 provides a robust sender-side offer lifecycle: targeted offers set pending flags with 90-day expiry, acceptance triggers recheck liveness and records an accepted receipt (`common/decisions/COLDWAR_SPR_v2_agreements.txt:91-120`, `common/scripted_effects/COLDWAR_SPR_v2_agreements.txt:133-180`). Its current recipient response is an event, so retain its receipt/expiry safeguards but show NKO, SOV, CHI, and KOR acceptance/refusal as decisions visible in the recipient’s own decision tab.

Concrete decision shape for each incoming NKO offer:

```hoi4
COLDWAR_NKO_recipient_agreements = {
    icon = generic_foreign_policy
    allowed = { OR = { tag = SOV tag = CHI tag = KOR } }
    visible = { IMP_is_1970_scenario = yes }
}

COLDWAR_NKO_accept_offer_from_nko = {
    icon = generic_foreign_policy
    cost = 0
    visible = { has_country_flag = COLDWAR_NKO_offer_from_NKO_pending }
    available = {
        NKO = { exists = yes NOT = { has_war_with = ROOT } }
        COLDWAR_NKO_pair_unsanctioned_with_NKO = yes
    }
    complete_effect = { COLDWAR_NKO_accept_offer_from_recipient = yes }
    ai_will_do = { factor = 0 }
}
```

Define a matching refusal decision that clears pending receipts without charging or granting anything. The acceptance helper must, in one guarded transaction: verify sender and recipient still exist, the pending offer has not expired or already been accepted, the countries are not at war, and no relevant bilateral sanction is active; clear both pending flags; set the durable accepted-agreement flag on both tags; then attach the paired spirits. Keep the saved offer quote on the sender and display the same amount to the recipient.

Use two dynamic-modifier definitions (one per tag) or equivalent paired permanent ideas. Each side checks the same bilateral contract and the same status gates. Example conditions for NKO’s side with SOV are:

```hoi4
enable = {
    original_tag = NKO
    has_country_flag = COLDWAR_NKO_sov_agreement
    SOV = {
        exists = yes
        has_country_flag = COLDWAR_NKO_sov_agreement
        NOT = { has_war_with = NKO }
        NOT = { is_in_array = { array = imp_dip_sanc_by_us value = NKO } }
        NOT = { is_in_array = { array = imp_fin_sanc_by_us value = NKO } }
        NOT = { is_in_array = { array = imp_eco_sanc_by_us value = NKO } }
        NOT = { is_in_array = { array = imp_mil_sanc_by_us value = NKO } }
    }
    NOT = { is_in_array = { array = imp_dip_sanc_by_us value = SOV } }
    NOT = { is_in_array = { array = imp_fin_sanc_by_us value = SOV } }
    NOT = { is_in_array = { array = imp_eco_sanc_by_us value = SOV } }
    NOT = { is_in_array = { array = imp_mil_sanc_by_us value = SOV } }
}
```

This checks all four direct Imperia sanction classes in both directions. The sanction arrays’ semantics and reciprocal writes are defined by `common/scripted_effects/IMP_sanctions_support_effects.txt:5-50`: `imp_*_sanc_by_us` lists targets sanctioned by the current country, while `imp_*_sanc_on_us` lists countries sanctioning it. Mirror the accepted receipt and dynamic-modifier definition on SOV, reversing the NKO/SOV array tests. Repeat the same paired pattern separately for CHI and KOR; do not use one unilateral generic spirit for all partners.

The accepted receipt remains permanent. The modifier itself becomes inactive on either mutual war or direct sanctions and can return when both conditions clear. Add a bilateral refresh helper and call it on both tags when war starts/ends and when an Imperia sanction is imposed/lifted. The sanctions add/lift effects expose the exact array mutation points (`IMP_sanctions_support_effects.txt:5-50`; removal examples in `common/scripted_effects/COLDWAR_GER_1970_effects.txt:694-731`). `COLDWAR_SPR_v2` also has an agreement refresh effect (`common/scripted_effects/COLDWAR_SPR_v2_agreements.txt:329+`). This refresh contract must force the paired modifier update at both endpoints; a one-sided update can leave a stale spirit in multiplayer. Monthly reconciliation is a useful backstop, not a replacement for agreement/war/sanction callbacks.

## War route against KOR

Add a separately named focus with an explicit military route and player-facing war consequence. Native shape:

```hoi4
will_lead_to_war_with = KOR
completion_reward = {
    if = {
        limit = { country_exists = KOR NOT = { has_war_with = KOR } }
        create_wargoal = { type = annex_everything target = KOR }
    }
}
```

The existing joint Korea focus already declares `will_lead_to_war_with = KOR` and creates the exact wargoal (`common/national_focus/03_china_north_korea_joint.txt:1985-2020`). If the intended route is limited territorial revision rather than regime elimination, use a native state-specific take-state wargoal instead of promising annexation; do not silently switch the meaning. A KOR agreement’s paired spirit is disabled by the mutual-war gate from the first day of hostilities, and must not reactivate until the war and sanctions gates both clear.

## Verification boundary

Every modifier and scripted effect named above has a target-source provider/use example. These checks establish source-backed syntax and data flow only. The recipient decision window, paired modifier deactivation/reactivation, building slot result, GDP quote tooltip, and wargoal behavior still require implementation and an in-game 1970 validation pass.
