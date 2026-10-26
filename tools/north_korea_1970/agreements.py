# IMPERIA CW — Cold War: North Korea 1970 negotiated foreign agreements.
"""Generate isolated recipient-decided NKO 1970 bilateral agreement support."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


P = "COLDWAR_NKO_foreign_"
LOC = "COLDWAR_NKO_foreign_"
HEADER = "# IMPERIA CW — Cold War: North Korea 1970 bilateral agreements.\n"
PARTNER_LABELS = {
    "SOV": "the Soviet Union",
    "CHI": "China",
    "KOR": "South Korea",
    "DDR": "East Germany",
    "BUL": "Bulgaria",
    "ROM": "Romania",
    "EGY": "Egypt",
    "JAP": "Japan",
}
SPIRIT_DESCRIPTIONS = {
 'soviet_industry':('Soviet machinery, power engineering and training support North Korean production. Continued access brings technical dependence and a stronger Soviet presence.','Machinery exports and technical placements strengthen Soviet commercial and political influence. Training commitments add to education costs.'),
 'china_border':('Agricultural deliveries and organized border supplies support domestic production and logistics. Revenue concessions and reliance on China limit the freedom of the programme.','Border exchanges improve commerce and customs revenue. Regular cooperation requires additional administrative capacity.'),
 'korean_channel':('Regular exchanges support civilian commerce and stable contacts across the peninsula. Political accommodation constrains the military confrontation.','Regular exchanges support civilian commerce and stable contacts across the peninsula. Political accommodation constrains the military confrontation.'),
 'civil_atomic':('Reactor research, power engineering and specialist training strengthen the civilian nuclear programme. Supervision and education commitments accompany technical access.','Reactor engineering and specialist exchanges support scientific cooperation and external influence. Training and supervision require continuing resources.'),
 'gdr_machinery':('Machine tools, industrial standards and specialist exchanges improve production. Imported components and technical commitments add to the cost of cooperation.','Industrial cooperation supports machinery exports and technical influence. Specialist exchanges require continued education and administrative support.'),
 'bulgarian_engineering':('Engineering and agricultural exchanges improve technical expertise and farm production. Training and public support remain continuing obligations.','Engineering and agricultural exchanges develop technical cooperation. Education and administrative commitments accompany the programme.'),
 'romanian_exchange':('Industrial and commercial exchanges diversify external procurement. Export allocations and administrative commitments sustain the arrangement.','Reciprocal trade and industrial exchanges support commerce and technical contacts. The programme requires export and administrative commitments.'),
 'egyptian_technical':('Technical missions and training improve specialist experience. Personnel and education commitments place additional demands on the state.','Scientific and technical exchanges support specialist training and equipment cooperation. Education commitments draw on public resources.'),
 'japan_fisheries':('Fisheries equipment and commercial contact support civilian production. Revenue concessions and closer supervision accompany the arrangement.','Fisheries and commercial arrangements support trade with the DPRK. Supervision and administrative commitments remain part of the programme.'),
}
MOD_LABELS = {
    "productivity_growth_modifier": "Monthly Productivity Growth",
    "production_factory_max_efficiency_factor": "Production Efficiency Cap",
    "production_factory_efficiency_gain_factor": "Production Efficiency Growth",
    "fossil_pp_energy_generation_modifier": "Fossil Power Generation",
    "agricolture_productivity_modifier": "Agricultural Productivity",
    "supply_consumption_factor": "Supply Consumption",
    "foreign_influence_defense_modifier": "Foreign Influence Defense",
    "foreign_influence_modifier": "Foreign Influence",
    "army_personnel_cost_multiplier_modifier": "Army Personnel Costs",
    "tax_gain_multiplier_modifier": "Tax Revenue Multiplier",
    "stability_factor": "Stability",
    "trade_opinion_factor": "Trade Deal Opinion",
    "army_attack_factor": "Army Attack",
    "bureaucracy_cost_multiplier_modifier": "Bureaucracy Cost Multiplier",
    "research_speed_factor": "Research Speed",
    "education_cost_multiplier_modifier": "Education Cost Multiplier",
    "nuclear_energy_generation_modifier": "Nuclear Power Generation",
    "industrial_capacity_factory": "Factory Output",
    "corporate_tax_income_multiplier_modifier": "Corporate Tax Revenue Multiplier",
    "resource_export_multiplier_modifier": "Resource Export Multiplier",
    "experience_gain_army": "Army Experience Gain",
    "equipment_cost_multiplier_modifier": "Equipment Cost Multiplier",
    "agricolture_productivity_modifier": "Agricultural Productivity",
    "police_cost_multiplier_modifier": "Police Cost Multiplier",
}


def num(value: float) -> str:
    """Keep scripted decimal literals short and native-parser friendly."""
    value = float(value)
    result = f"{value:.5f}".rstrip("0").rstrip(".")
    return result or "0"


def percent(value: float) -> str:
    value = float(value) * 100
    return f"{value:+g}%"


def pct_share(value: float) -> str:
    value = float(value) * 100
    return f"{value:.5f}".rstrip("0").rstrip(".") + "%"


def indent(text: str, amount: int = 1) -> str:
    prefix = "\t" * amount
    return "\n".join(prefix + line if line else "" for line in text.splitlines())


def modifier_lines(mods: dict[str, float]) -> str:
    return "\n".join(f"{key} = {num(value)}" for key, value in mods.items())


def effect_tooltip_lines(mods: dict[str, float]) -> list[str]:
    lines = []
    for key, value in mods.items():
        label = MOD_LABELS[key]
        amount=f'{value:+g}' if key in ('productivity_growth_modifier','experience_gain_army') else percent(value)
        if key=='experience_gain_army':label='Daily Army Experience Gain'
        lines.append(f"{label}: {amount}")
    return lines


def setup_line(name: str, share: float) -> str:
    return f"{name} pays once: {pct_share(share)} of its GDP at submission."


def weekly_line(name: str, share: float) -> str:
    return f"{name} weekly commitment: {pct_share(float(share) / 52)} of current GDP."


def combined_modifiers(base: dict[str, float], upgrade: dict[str, float]) -> dict[str, float]:
    combined = dict(base)
    for key, value in upgrade.items():
        combined[key] = combined.get(key, 0) + value
    return {key: value for key, value in combined.items() if value}


def names(agreement: dict) -> list[tuple[str, dict, str]]:
    result = [(agreement["key"] + "_base", agreement, "base")]
    for upgrade in agreement.get("upgrades", []):
        result.append((upgrade["key"], upgrade, upgrade["key"]))
    return result


def receipt(agreement: dict, stage: str) -> str:
    if stage == "base":
        return agreement["receipts"]["accepted"]
    upgrade = next(up for up in agreement["upgrades"] if up["key"] == stage)
    return upgrade["receipt"]


def pending_flag(agreement: dict, stage: str) -> str:
    if stage == "base":
        return agreement["receipts"]["pending"]
    return f"COLDWAR_NKO_foreign_{agreement['key']}_{stage}_pending"


def initial_grant_flag(agreement: dict) -> str:
    return agreement["receipts"]["initial_grant"]


def is_receipted(flag: str) -> str:
    return f"has_country_flag = {flag}"


def clear_sanctions_in_scope(tag: str, other: str) -> str:
    rows = []
    for cls in ("dip", "fin", "eco", "mil"):
        for direction in ("by_us", "on_us"):
            rows.append(
                "NOT = { is_in_array = { array = "
                f"imp_{cls}_sanc_{direction} value = {other} }} }}"
            )
    return f"{tag} = {{\n" + indent("\n".join(rows), 1) + "\n}"


def pair_clear_trigger(agreement: dict) -> str:
    partner = agreement["partner"]
    return "\n".join(
        [
            "NKO = { exists = yes }",
            f"{partner} = {{ exists = yes }}",
            f"NOT = {{ NKO = {{ has_war_with = {partner} }} }}",
            clear_sanctions_in_scope("NKO", partner),
            clear_sanctions_in_scope(partner, "NKO"),
        ]
    )


def pair_active_trigger(agreement: dict, stage: str) -> str:
    accepted = receipt(agreement, stage)
    rows = [
        f"NKO = {{ exists = yes {is_receipted(accepted)} }}",
        f"{agreement['partner']} = {{ exists = yes {is_receipted(accepted)} }}",
        f"{P}{agreement['key']}_pair_clear = yes",
    ]
    if stage != "base":
        base = agreement["receipts"]["accepted"]
        rows.extend(
            [
                f"NKO = {{ {is_receipted(base)} }}",
                f"{agreement['partner']} = {{ {is_receipted(base)} }}",
            ]
        )
        if stage == 'npt_offer':rows.append('NKO = { has_country_flag = COLDWAR_NKO_safeguards_valid }')
    else:
        # An accepted upgrade replaces the base policy spirit, but the original
        # agreement and its annual commitments remain in force.
        for upgrade in agreement.get("upgrades", []):
            rows.append(f"NOT = {{ {P}{agreement['key']}_pair_active_{upgrade['key']} = yes }}")
    return "\n".join(rows)


def pair_signed_trigger(agreement: dict) -> str:
    accepted = agreement["receipts"]["accepted"]
    return "\n".join(
        [
            f"NKO = {{ exists = yes {is_receipted(accepted)} }}",
            f"{agreement['partner']} = {{ exists = yes {is_receipted(accepted)} }}",
            f"{P}{agreement['key']}_pair_clear = yes",
        ]
    )


def gen(root: Path, design: dict) -> dict[str, str]:
    agreements = design["agreements"]
    loc: dict[str, str] = {}
    effects: list[str] = []
    triggers: list[str] = []
    dynamic: list[str] = []
    decisions: list[str] = []
    events=['add_namespace = COLDWAR_NKO_foreign']
    stage_index=0

    def L(key: str, value: str) -> str:
        if key in loc and loc[key] != value:
            raise ValueError(f"duplicate localization key with different values: {key}")
        loc[key] = value
        return key

    def E(name: str, body: str) -> None:
        effects.append(f"{name} = {{\n{indent(body)}\n}}")

    def T(name: str, body: str) -> None:
        triggers.append(f"{name} = {{\n{indent(body)}\n}}")

    def DM(name: str, display: str, body: str, active: str, description: str) -> None:
        L(name, display)
        L(name + "_desc", description)
        dynamic.append(
            f"{name} = {{\n"
            f"\ticon = GFX_idea_economic_increase\n"
            f"\tenable = {{ {active} = yes }}\n"
            f"{indent(body)}\n"
            f"}}"
        )

    L("COLDWAR_NKO_1970_foreign", "Bilateral Agreements")
    L("COLDWAR_NKO_1970_foreign_desc", "Negotiate reciprocal programmes with the Democratic People’s Republic of Korea. Each proposal requires the other government’s consent.")
    L("COLDWAR_NKO_foreign_offer_conditions", "The partner country must exist. The recipient decides whether to accept within 90 days.")
    L("COLDWAR_NKO_foreign_accept_conditions", "Both countries must exist and be at peace, with no bilateral diplomatic, financial, economic or military sanctions in either direction.")
    L("COLDWAR_NKO_foreign_no_cost_on_decline", "Decline without charge. A new submission remains subject to the 180-day interval.")
    L("COLDWAR_NKO_foreign_resubmit_desc", "Submit a fresh 90-day proposal using current GDP quotes. No payment is made until the recipient accepts.")
    L("COLDWAR_NKO_foreign_resubmit_title", "Renew the proposal")
    L("COLDWAR_NKO_foreign_resubmit_sent", "The proposal has been resubmitted for 90 days.")
    L("COLDWAR_NKO_foreign_invalidated", "The proposal is no longer available. No payment was made; the sender may submit it again.")
    L("COLDWAR_NKO_foreign_partner_requirement", "The other government must exist and remain at peace with the DPRK without bilateral sanctions.")
    L('COLDWAR_NKO_foreign_ready_tt','The proposal is open, both countries are at peace and no bilateral sanctions are in force.')
    L('COLDWAR_NKO_foreign_ready_tt_NOT','A valid open proposal, peaceful relations and the absence of bilateral sanctions are required.')
    L('COLDWAR_NKO_foreign_resend_ready_tt','Both countries can reopen this proposal under the current diplomatic conditions.')
    L('COLDWAR_NKO_foreign_resend_ready_tt_NOT','The proposal cannot currently be reopened.')
    L('COLDWAR_NKO_foreign_cooldown_tt','At least §Y180 days§! have passed since the previous proposal.')
    L('COLDWAR_NKO_foreign_cooldown_tt_NOT','A new proposal must wait §Y180 days§! after the previous submission.')
    L('COLDWAR_NKO_foreign_if_accepted_tt','§YUpon acceptance:§!')
    L('COLDWAR_NKO_foreign_weekly_commitment_tt','Weekly commitment: §R$[?COLDWAR_NKO_foreign_weekly_preview|3] billion§!.')

    # Every contract has a single symmetric availability predicate. It is used by
    # both endpoint modifiers and by the weekly fee reconciliation.
    for agreement in agreements:
        key, partner = agreement["key"], agreement["partner"]
        T(f"{P}{key}_pair_clear", pair_clear_trigger(agreement))
        T(f"{P}{key}_pair_signed_active", pair_signed_trigger(agreement))
        for stage_id, stage_data, stage_kind in names(agreement):
            active_name = f"{P}{key}_pair_active_{stage_kind}"
            T(active_name, pair_active_trigger(agreement, stage_kind))
            public_key = key if stage_kind == "base" else stage_kind
            T(
                f"COLDWAR_NKO_{public_key}_active",
                f"{P}{key}_pair_signed_active = yes" if stage_kind == "base" else f"{active_name} = yes",
            )

    # Acceptance/offer triggers and persistent endpoint modifiers.
    for agreement in agreements:
        key, partner = agreement["key"], agreement["partner"]
        partner_name = PARTNER_LABELS[partner]
        base_receipt = agreement["receipts"]["accepted"]
        base_pending = pending_flag(agreement, "base")
        pair_clear = f"{P}{key}_pair_clear"

        for stage_id, stage_data, stage_kind in names(agreement):
            stage_index+=1
            newsbase=stage_index*4
            if stage_kind == "base":
                changes_nko = agreement["nko"]["modifiers"]
                changes_partner = agreement["recipient"]["modifiers"]
                setup_nko = agreement["nko"]["setup_gdp_share"]
                setup_partner = agreement["recipient"]["setup_gdp_share"]
                title = agreement["title"]
                stage_receipt = base_receipt
                stage_pending = base_pending
                base_stage = True
            else:
                up = next(u for u in agreement["upgrades"] if u["key"] == stage_kind)
                changes_nko = combined_modifiers(agreement["nko"]["modifiers"], up["nko"])
                changes_partner = combined_modifiers(agreement["recipient"]["modifiers"], up["recipient"])
                setup_nko = up["setup_nko_gdp_share"]
                setup_partner = up["setup_recipient_gdp_share"]
                title = up["title"]
                stage_receipt = up["receipt"]
                stage_pending = pending_flag(agreement, stage_kind)
                base_stage = False

            active_name = f"{P}{key}_pair_active_{stage_kind}"
            dm_nko = f"COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_nko"
            dm_partner = f"COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_partner"
            stage_description=agreement['description'] if base_stage else stage_data['description']
            spirit_nko,spirit_partner=agreement.get('spirit_descriptions',SPIRIT_DESCRIPTIONS.get(key,()))
            prefix='Expanded cooperation extends these commitments. ' if not base_stage else ''
            DM(dm_nko, title, modifier_lines(changes_nko), active_name,prefix+spirit_nko)
            DM(dm_partner, title, modifier_lines(changes_partner), active_name,prefix+spirit_partner)

            sender_live = f"{P}{key}_{stage_kind}_send_live"
            accept_live = f"{P}{key}_{stage_kind}_accept_live"
            cooldown=f'{P}cooldown_{key}_{stage_kind}'
            if base_stage:
                T(sender_live, f"""tag = NKO IMP_is_1970_scenario = yes
{partner} = {{ exists = yes }}
{pair_clear} = yes
NOT = {{ has_country_flag = {stage_receipt} }}
NOT = {{ has_country_flag = {stage_pending} }}
NOT = {{ has_country_flag = {cooldown} }}
NOT = {{ {partner} = {{ has_country_flag = {stage_pending} }} }}
check_variable = {{ gdp_total > 0 }} {partner} = {{ check_variable = {{ gdp_total > 0 }} }}""")
                valid_extra = f"{pair_clear} = yes"
                if agreement.get("buildings"):
                    valid_extra += f"\n{P}{key}_building_site_valid = yes"
                    T(f"{P}{key}_building_site_valid", "OR = {\n" + indent("\n".join(
                        f"{sid} = {{ is_owned_by = NKO is_controlled_by = NKO industrial_complex < 50 }}"
                        for sid in agreement["buildings"][0]["state_ids"]
                    )) + "\n}")
            else:
                T(sender_live, f"""tag = NKO IMP_is_1970_scenario = yes
NKO = {{ has_country_flag = {base_receipt} }} {partner} = {{ exists = yes has_country_flag = {base_receipt} }}
{P}{key}_pair_signed_active = yes
NOT = {{ has_country_flag = {stage_receipt} }}
NOT = {{ has_country_flag = {stage_pending} }}
NOT = {{ has_country_flag = {cooldown} }}
NOT = {{ {partner} = {{ has_country_flag = {stage_pending} }} }}
check_variable = {{ gdp_total > 0 }} {partner} = {{ check_variable = {{ gdp_total > 0 }} }}""")
                valid_extra = f"{P}{key}_pair_signed_active = yes"
            accept_partner_guard = f"exists = yes has_country_flag = {stage_pending} NOT = {{ has_country_flag = {stage_receipt} }}"
            accept_nko_guard = f"exists = yes IMP_is_1970_scenario = yes has_country_flag = {stage_pending} NOT = {{ has_country_flag = {stage_receipt} }}"
            if not base_stage:
                accept_nko_guard += f" has_country_flag = {base_receipt}"
                accept_partner_guard += f" has_country_flag = {base_receipt}"
            accept_nko_guard += f" {pair_clear} = yes"
            if stage_kind == 'npt_offer':accept_nko_guard += ' has_country_flag = COLDWAR_NKO_safeguards_valid'
            if stage_kind == 'confederation_offer':accept_partner_guard += ' is_subject = no'
            if agreement.get("buildings") and base_stage:
                accept_nko_guard += f" {P}{key}_building_site_valid = yes"
            T(accept_live, f"""tag = {partner}
exists = yes
has_country_flag = {stage_pending}
NOT = {{ has_country_flag = {stage_receipt} }}
NKO = {{ {accept_nko_guard} }}
{partner} = {{ {accept_partner_guard} }}
NKO = {{ check_variable = {{ {P}quote_{key}_{stage_kind}_nko > 0 }} }}
check_variable = {{ {P}quote_{key}_{stage_kind}_partner > 0 }}""")

            # Build one or two endpoint rewards, but never repeat an accepted
            # receipt or an initial grant during refresh.
            send_body = f"""if = {{
limit = {{ {sender_live} = yes }}
set_temp_variable = {{ {P}quote_temp = gdp_total }}
multiply_temp_variable = {{ {P}quote_temp = {num(setup_nko)} }}
set_variable = {{ {P}quote_{key}_{stage_kind}_nko = {P}quote_temp }}
{partner} = {{
set_temp_variable = {{ {P}quote_temp = gdp_total }}
multiply_temp_variable = {{ {P}quote_temp = {num(setup_partner)} }}
set_variable = {{ {P}quote_{key}_{stage_kind}_partner = {P}quote_temp }}
set_variable = {{ {P}quote_{key}_{stage_kind}_nko = NKO.{P}quote_{key}_{stage_kind}_nko }}
set_country_flag = {{ flag = {stage_pending} days = 90 }}
country_event = {{ id = COLDWAR_NKO_foreign.{newsbase} }}
}}
set_country_flag = {{ flag = {stage_pending} days = 90 }}
set_country_flag = {{ flag = {cooldown} value = 1 days = 180 }}
set_country_flag = {P}sent_{key}_{stage_kind}
clr_country_flag = {P}resubmit_{key}_{stage_kind}
clr_country_flag = {P}closure_notified_{key}_{stage_kind}
}}
else_if = {{ limit = {{ NOT = {{ has_country_flag = {stage_pending} }} NOT = {{ has_country_flag = {stage_receipt} }} }} set_country_flag = {P}resubmit_{key}_{stage_kind} }}"""
            E(f"{P}send_{key}_{stage_kind}", send_body)

            # Native material previews keep units, colors and sign conventions.
            # Proposal previews use current GDP; recipient previews use saved quotes.
            focus_tooltip = f"COLDWAR_NKO_foreign_offer_{key}_{stage_kind}_terms"
            L(focus_tooltip,f'Propose §Y{title}§! to [{partner}.GetNameDef]. A reply is due within §Y90 days§!; payment follows acceptance.')
            building_tt=None
            if base_stage and agreement.get('buildings'):
                b=agreement['buildings'][0];regions=' or '.join(design['state_names'][str(s)] for s in b['state_ids'])
                building_tt=L(f'{P}{key}_building_tt',f'Add §G{b["levels"]}§! Civilian Factory and §G{b["slots"]}§! Building Slot in {regions}.')
            def material(saved):
                chunks=[]
                for tag,side,share,dm in [('NKO','nko',setup_nko,dm_nko),(partner,'recipient',setup_partner,dm_partner)]:
                    quote=f'{P}quote_{key}_{stage_kind}_'+('nko' if side=='nko' else 'partner')
                    money=f'set_temp_variable = {{ treasury_change = {quote if saved else "gdp_total"} }} multiply_temp_variable = {{ treasury_change = {"-1" if saved else num(-share)} }} modify_treasury_effect = yes'
                    old=f'remove_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_base_'+('nko' if side=='nko' else 'partner')+' }' if not base_stage else ''
                    annual=agreement[side]['annual_commitment_gdp_share']
                    weekly=f'set_temp_variable = {{ {P}weekly_preview = gdp_total }} multiply_temp_variable = {{ {P}weekly_preview = {num(annual)} }} divide_temp_variable = {{ {P}weekly_preview = 52 }} custom_effect_tooltip = COLDWAR_NKO_foreign_weekly_commitment_tt'
                    building=f'custom_effect_tooltip = {building_tt}' if tag=='NKO' and building_tt else ''
                    chunks.append(f'{tag} = {{ {money} {old} add_dynamic_modifier = {{ modifier = {dm} }} {weekly} {building} }}')
                return '\n'.join(chunks)
            preview_id=f'{P}preview_{key}_{stage_kind}'
            terms_id=f'{P}terms_{key}_{stage_kind}'
            E(preview_id,f'custom_effect_tooltip = {focus_tooltip}\ncustom_effect_tooltip = COLDWAR_NKO_foreign_if_accepted_tt\n'+material(False))
            E(terms_id,material(True))
            for offset,body,option in [
                (0,stage_description,'Review the proposal.'),
                (1,'Both governments have approved this programme. The agreed reciprocal commitments are now in force.','Proceed with the agreement.'),
                (2,'The other government has declined this programme. No funds have been transferred.','Keep the channels open.'),
                (3,'The proposal has closed without an agreement. New terms may be submitted when diplomatic conditions permit.','Reconsider the proposal.')]:
                eid=f'COLDWAR_NKO_foreign.{newsbase+offset}'
                L(eid+'.t',title);L(eid+'.d',body);L(eid+'.option_a',option)
                note=('effect_tooltip = { '+terms_id+' = yes }') if offset==0 else ''
                events.append(f'country_event = {{ id = {eid} title = {eid}.t desc = {eid}.d is_triggered_only = yes option = {{ name = {eid}.option_a {note} }} }}')
            offer_suffix = f"{key}_base" if base_stage else stage_kind
            E(f"COLDWAR_NKO_offer_{offer_suffix}", f"""custom_effect_tooltip = {focus_tooltip}
hidden_effect = {{ {P}send_{key}_{stage_kind} = yes }}""")

            # Recipient decision can accept or decline. There are no treasury
            # checks: both signed GDP quotes are charged through MD's native helper.
            stage_title_key = f"COLDWAR_NKO_foreign_{key}_{stage_kind}_title"
            L(stage_title_key, f"{agreement['title']} — {title}" if not base_stage else agreement["title"])
            accept_key = f"COLDWAR_NKO_foreign_accept_{key}_{stage_kind}"
            decline_key = f"COLDWAR_NKO_foreign_decline_{key}_{stage_kind}"
            decision_desc = stage_description
            L(accept_key, "Accept " + title)
            L(accept_key + "_desc", decision_desc)
            L(decline_key, "Decline " + title)
            L(decline_key + "_desc", "No payment is made. The DPRK may submit a fresh proposal after refusal or expiry.")

            accept_initial_grant = (
                f"set_country_flag = {initial_grant_flag(agreement)}\n"
                if base_stage
                else ""
            )
            accept_nko_initial_grant = (
                f"NKO = {{ set_country_flag = {initial_grant_flag(agreement)} }}"
                if base_stage
                else ""
            )
            accept_effect = f"""if = {{ limit = {{ {accept_live} = yes }}
hidden_effect = {{
NKO = {{ set_country_flag = {stage_receipt} clr_country_flag = {stage_pending} }}
{partner} = {{ set_country_flag = {stage_receipt} clr_country_flag = {stage_pending} }}
set_country_flag = {stage_receipt}
clr_country_flag = {stage_pending}
NKO = {{ clr_country_flag = {P}resubmit_{key}_{stage_kind} }}
{partner} = {{ set_temp_variable = {{ treasury_change = {P}quote_{key}_{stage_kind}_partner }} multiply_temp_variable = {{ treasury_change = -1 }} modify_treasury_effect = yes }}
NKO = {{ set_temp_variable = {{ treasury_change = {P}quote_{key}_{stage_kind}_nko }} multiply_temp_variable = {{ treasury_change = -1 }} modify_treasury_effect = yes }}
                {('if = { limit = { NKO = { NOT = { has_country_flag = '+initial_grant_flag(agreement)+' } } } '+_building_grant(agreement)+' NKO = { set_country_flag = '+initial_grant_flag(agreement)+' } '+partner+' = { set_country_flag = '+initial_grant_flag(agreement)+' } }') if base_stage else ''}
NKO = {{ if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {dm_nko} }} }} }} add_dynamic_modifier = {{ modifier = {dm_nko} }} }} }}
{partner} = {{ if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {dm_partner} }} }} }} add_dynamic_modifier = {{ modifier = {dm_partner} }} }} }}
NKO = {{ {P}refresh = yes }}
NKO = {{ country_event = {{ id = COLDWAR_NKO_foreign.{newsbase+1} }} }}
}}
}}"""
            E(f"{P}accept_{key}_{stage_kind}", accept_effect)
            E(f"{P}decline_{key}_{stage_kind}", f"""if = {{ limit = {{ tag = {partner} has_country_flag = {stage_pending} NKO = {{ has_country_flag = {stage_pending} }} }}
NKO = {{ clr_country_flag = {stage_pending} clr_country_flag = {P}sent_{key}_{stage_kind} set_country_flag = {P}resubmit_{key}_{stage_kind} country_event = {{ id = COLDWAR_NKO_foreign.{newsbase+2} }} }}
clr_country_flag = {stage_pending}
}}""")

            # Sender retry remains available after an explicit refusal. Expiry is
            # detected by the shared daily refresh below when the timed pending
            # flag has elapsed.
            resubmit_key = f"COLDWAR_NKO_foreign_resubmit_{key}_{stage_kind}"
            L(resubmit_key, "Renew " + title)
            L(resubmit_key + "_desc", stage_description+' A new submission is possible 180 days after the previous proposal.')
            accept_id=f"COLDWAR_NKO_foreign_recipient_accept_{key}_{stage_kind}"
            decline_id=f"COLDWAR_NKO_foreign_recipient_decline_{key}_{stage_kind}"
            L(accept_id,"Accept "+title);L(accept_id+"_desc",decision_desc)
            L(decline_id,"Decline "+title);L(decline_id+"_desc","Decline the proposal without charge.")
            native_preview=terms_id+' = yes'
            decisions.append(f"""COLDWAR_NKO_foreign_resubmit_{key}_{stage_kind} = {{
	icon = GFX_decision_relation
	cost = 0
	days_re_enable = 180
	visible = {{ tag = NKO has_country_flag = {P}resubmit_{key}_{stage_kind} }}
	available = {{ custom_trigger_tooltip = {{ tooltip = COLDWAR_NKO_foreign_resend_ready_tt {sender_live} = yes }} custom_trigger_tooltip = {{ tooltip = COLDWAR_NKO_foreign_cooldown_tt NOT = {{ has_country_flag = {cooldown} }} }} }}
	complete_effect = {{ effect_tooltip = {{ {preview_id} = yes }} hidden_effect = {{ {P}send_{key}_{stage_kind} = yes }} }}
	ai_will_do = {{ factor = 0 }}
}}""")

            decisions.append(f"""COLDWAR_NKO_foreign_recipient_accept_{key}_{stage_kind} = {{
	icon = GFX_decision_relation
	cost = 0
	visible = {{ tag = {partner} has_country_flag = {stage_pending} }}
	available = {{ custom_trigger_tooltip = {{ tooltip = COLDWAR_NKO_foreign_ready_tt {accept_live} = yes }} }}
	complete_effect = {{ effect_tooltip = {{ {native_preview} }} hidden_effect = {{ {P}accept_{key}_{stage_kind} = yes }} }}
	ai_will_do = {{ factor = 0 }}
}}""")
            decisions.append(f"""COLDWAR_NKO_foreign_recipient_decline_{key}_{stage_kind} = {{
	icon = GFX_decision_relation
	cost = 0
	visible = {{ tag = {partner} has_country_flag = {stage_pending} }}
	complete_effect = {{ custom_effect_tooltip = COLDWAR_NKO_foreign_no_cost_on_decline hidden_effect = {{ {P}decline_{key}_{stage_kind} = yes }} }}
	ai_will_do = {{ factor = 0 }}
}}""")

    # A single refresh is called by the parent NKO daily hook and immediately
    # after decisions. It only reattaches already-earned persistent modifiers,
    # repairs expired pending offers, and publishes each country's weekly GDP
    # share. It never pays or repeats a project grant.
    refresh = [
        "if = {",
        "limit = { tag = NKO IMP_is_1970_scenario = yes }",
    ]
    stage_index=0
    for agreement in agreements:
        key, partner = agreement["key"], agreement["partner"]
        accepted = agreement["receipts"]["accepted"]
        pending = pending_flag(agreement, "base")
        for stage_id, stage_data, stage_kind in names(agreement):
            stage_index+=1
            newsbase=stage_index*4
            stage_pending = pending_flag(agreement, stage_kind)
            stage_receipt = receipt(agreement, stage_kind)
            refresh.append(
                f"if = {{ limit = {{ has_country_flag = {P}sent_{key}_{stage_kind} NOT = {{ has_country_flag = {stage_pending} }} NOT = {{ has_country_flag = {stage_receipt} }} }} set_country_flag = {P}resubmit_{key}_{stage_kind} {partner} = {{ clr_country_flag = {stage_pending} }} }}"
            )
            refresh.append(f'''if = {{ limit = {{ has_country_flag = {P}resubmit_{key}_{stage_kind} has_country_flag = {P}sent_{key}_{stage_kind} NOT = {{ has_country_flag = {P}closure_notified_{key}_{stage_kind} }} }}
              set_country_flag = {P}closure_notified_{key}_{stage_kind} country_event = {{ id = COLDWAR_NKO_foreign.{newsbase+3} }} }}''')
            refresh.append(
                f"if = {{ limit = {{ has_country_flag = {stage_pending} NOT = {{ {P}{key}_pair_clear = yes }} NOT = {{ has_country_flag = {stage_receipt} }} }} clr_country_flag = {stage_pending} set_country_flag = {P}resubmit_{key}_{stage_kind} {partner} = {{ clr_country_flag = {stage_pending} }} }}"
            )
        refresh.extend(
            [
                f"if = {{ limit = {{ {P}{key}_pair_active_base = yes }}",
                f"NKO = {{ if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_base_nko }} }} }} add_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_base_nko }} }} }}",
                f"{partner} = {{ if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_base_partner }} }} }} add_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_base_partner }} }} }}",
                "}",
            ]
        )
        refresh.append(f'''if = {{ limit = {{ NOT = {{ {P}{key}_pair_active_base = yes }} }}
          NKO = {{ if = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_base_nko }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_base_nko }} }} }}
          {partner} = {{ if = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_base_partner }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_base_partner }} }} }} }}''')
        for stage_id, stage_data, stage_kind in names(agreement):
            if stage_kind == "base":
                continue
            ureceipt = receipt(agreement, stage_kind)
            refresh.extend(
                [
                    f"if = {{ limit = {{ {P}{key}_pair_active_{stage_kind} = yes }}",
                    f"NKO = {{ if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_nko }} }} }} add_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_nko }} }} }}",
                    f"{partner} = {{ if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_partner }} }} }} add_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_partner }} }} }}",
                    "}",
                ]
            )
            refresh.append(f'''if = {{ limit = {{ NOT = {{ {P}{key}_pair_active_{stage_kind} = yes }} }}
              NKO = {{ if = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_nko }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_nko }} }} }}
              {partner} = {{ if = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_partner }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_NKO_1970_foreign_{key}_{stage_kind}_partner }} }} }} }}''')
        if key in ('soviet_industry','china_border'):
            refresh.append(f'''if = {{ limit = {{ {P}{key}_pair_signed_active = yes }} set_country_flag = {P}{key}_supply_was_active }}
            else = {{ if = {{ limit = {{ has_country_flag = {P}{key}_supply_was_active }} clr_country_flag = {P}{key}_supply_was_active
              if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_patron_disruption }} }} }} add_dynamic_modifier = {{ modifier = COLDWAR_NKO_patron_disruption days = 365 }} }} }} }}''')
    refresh.append('COLDWAR_NKO_refresh_programmes = yes')
    refresh.append("}")
    E(P + "refresh", "\n".join(refresh))

    # Parent inserts this into MD's weekly expense calculation. It is called in
    # each country's own scope and adds current GDP × annual commitment / 52.
    # The base agreement's payment continues after an upgrade; only its spirit
    # is replaced by the upgraded policy spirit.
    weekly_expenses = []
    for agreement in agreements:
        key, partner = agreement["key"], agreement["partner"]
        for tag, annual_share in (
            ("NKO", agreement["nko"]["annual_commitment_gdp_share"]),
            (partner, agreement["recipient"]["annual_commitment_gdp_share"]),
        ):
            weekly_expenses.append(
                f"if = {{ limit = {{ tag = {tag} {P}{key}_pair_clear = yes NKO = {{ has_country_flag = {agreement['receipts']['accepted']} }} {partner} = {{ has_country_flag = {agreement['receipts']['accepted']} }} }} "
                f"set_temp_variable = {{ {P}weekly_expense_temp = gdp_total }} "
                f"multiply_temp_variable = {{ {P}weekly_expense_temp = {num(annual_share)} }} "
                f"divide_temp_variable = {{ {P}weekly_expense_temp = 52 }} "
                f"add_to_variable = {{ additional_expenses_rate = {P}weekly_expense_temp }} }}"
            )
    E(P + "add_weekly_expenses", "\n".join(weekly_expenses))

    # Decision tree body is shared by NKO retry decisions and recipient decisions.
    decision_file = (
        HEADER
        + "COLDWAR_NKO_1970_foreign = {\n"
        + indent("\n\n".join(decisions))
        + "\n}\n"
    )
    decision_categories = (
        HEADER
        + "COLDWAR_NKO_1970_foreign = { icon = generic_foreign_policy allowed = { always = yes } visible = { IMP_is_1970_scenario = yes OR = { tag = NKO "+' '.join('has_country_flag = '+pending_flag(a,kind) for a in agreements for _,_,kind in names(a))+" } } }\n"
    )
    effect_file = HEADER + "\n\n".join(effects) + "\n"
    trigger_file = HEADER + "\n\n".join(triggers) + "\n"
    dynamic_file = HEADER + "\n\n".join(dynamic) + "\n"
    localisation = "l_english:\n# IMPERIA CW — Cold War: North Korea 1970 bilateral agreements.\n"
    localisation += "".join(f" {key}:0 \"{value.replace(chr(34), chr(39))}\"\n" for key, value in loc.items())
    return {
        "common/scripted_effects/COLDWAR_NKO_1970_foreign.txt": effect_file,
        "common/scripted_triggers/COLDWAR_NKO_1970_foreign.txt": trigger_file,
        "common/dynamic_modifiers/COLDWAR_NKO_1970_foreign.txt": dynamic_file,
        "common/decisions/COLDWAR_NKO_1970_foreign.txt": decision_file,
        "common/decisions/categories/COLDWAR_NKO_1970_foreign.txt": decision_categories,
        "events/COLDWAR_NKO_1970_foreign_events.txt":HEADER+'\n'.join(events)+'\n',
        "localisation/english/COLDWAR_NKO_1970_foreign_l_english.yml": localisation,
    }

    # Kept as a method to make the one-time Soviet building grant explicit in
    # generated code and guarded by the actual NKO ownership/level trigger.


def _building_grant(agreement: dict) -> str:
    if not agreement.get("buildings"):
        return ""
    building = agreement["buildings"][0]
    sid_list = building["state_ids"]
    clauses = []
    for index, sid in enumerate(sid_list):
        prefix = "if" if index == 0 else "else_if"
        clauses.append(
            f"{prefix} = {{ limit = {{ {sid} = {{ is_owned_by = NKO is_controlled_by = NKO industrial_complex < 50 }} }} "
            f"{sid} = {{ add_extra_state_shared_building_slots = {building['slots']} add_building_construction = {{ type = {building['type']} level = {building['levels']} instant_build = yes }} }} }}"
        )
    return "NKO = {\n" + indent("\n".join(clauses)) + "\n}"


def build(root: Path, design: dict) -> list[Path]:
    import sys
    sys.path.insert(0,str(Path(root)/'tools/vietnam_1970'))
    from script_ast import format_code
    root = Path(root)
    outputs = gen(root, design)
    paths = []
    for relative, text in outputs.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        encoding = "utf-8-sig" if relative.endswith(".yml") else "utf-8"
        if not relative.endswith('.yml'):text=HEADER+format_code(text)
        blob=text.lstrip('\ufeff').encode(encoding)
        if not path.exists() or path.read_bytes()!=blob:path.write_bytes(blob)
        paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--design",
        type=Path,
        default=Path("tools/north_korea_1970/current_design.json"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    design_path = args.design if args.design.is_absolute() else root / args.design
    design = json.loads(design_path.read_text(encoding="utf-8"))
    for path in build(root, design):
        print(path)


if __name__ == "__main__":
    main()
