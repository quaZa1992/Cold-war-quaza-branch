# IMPERIA CW — Cold War: Korean bilateral agreement runtime generator.
"""Build the KOR 1970 consent-based foreign agreement subsystem.

The returned script files are not written here: the approved-tree orchestrator
owns emission and integration. Localisation values are English strings; its
writer is responsible for the project's UTF-8-BOM YAML convention.
"""

from __future__ import annotations

import re
from COLDWAR_KOR_presentation import agreement_terms, AGREEMENTS


PREFIX = "COLDWAR_KOR_"
SCRIPT_COMMENT = "# IMPERIA CW — Cold War: Korean bilateral agreement runtime."
SELECTABLE_KEYS = {"technology_licence", "security_partner_contacts", "alternative_finance_contacts", "nordpolitik_recognition", "gulf_project_access"}


def _q(v):
    return f"{v:.5f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def _tag_list(c):
    rec = c.get("recipient", "")
    known = ("KOR", "NKO", "USA", "JAP", "SOV", "CHI", "SVN", "GER", "SAU", "IRQ")
    return [t for t in known if re.search(rf"\b{t}\b", rec)]


def _partner_policy(c):
    # Partner-side receipt may be a simple policy or be explicitly absent.
    effects = c.get("recipient_effects", {})
    return effects.get("policy", {}) if isinstance(effects, dict) else {}


def _policy(c, side):
    records = c.get("KOR_policy", []) if side == "kor" else []
    merged = {}
    for row in records:
        merged.update(row.get("modifiers", {}))
    if side == "partner":
        merged.update(_partner_policy(c))
    return merged


def _agreement_active(c, side="kor", partner_tag=None):
    key, signed, tags = c["key"], c["signed"], c["tags"]
    if key in SELECTABLE_KEYS:
        if side == "kor" and partner_tag is None:
            return "OR = { " + " ".join(f"AND = {{ {_agreement_active(c, side, tag)} }}" for tag in tags) + " }"
        tag = partner_tag or tags[0]
        pair = f"KOR = {{ has_country_flag = COLDWAR_KOR_{key}_{tag}_signed is_subject = no }} {tag} = {{ has_country_flag = COLDWAR_KOR_{key}_{tag}_signed is_subject = no NOT = {{ has_war_with = KOR }} }}"
        if key == "northern_security_compact": pair += " KOR = { check_variable = { ruling_party = 4 } }"
        return pair+_term_guards(c,[tag])
    terms = [f"KOR = {{ has_country_flag = {signed} is_subject = no }}"]
    for tag in tags:
        terms.append(f"{tag} = {{ has_country_flag = {signed} is_subject = no NOT = {{ has_war_with = KOR }} }}")
    if key == "northern_security_compact": terms.append("KOR = { check_variable = { ruling_party = 4 } }")
    if c.get('usfk') and key not in ('us_garrison','us_drawdown'):terms.append('COLDWAR_KOR_usfk_cooperation_live = yes')
    return " ".join(terms)+_term_guards(c,tags)

def _term_guards(c,tags):
    if not c.get('revised_terms'):return ''
    return ' '+' '.join(tag+' = { has_country_flag = COLDWAR_KOR_'+c['key']+'_terms_v3 }' for tag in ['KOR']+list(tags))


def _recipient_pair_active(c, tag):
    if c["key"] in SELECTABLE_KEYS:
        receipt = f"COLDWAR_KOR_{c['key']}_{tag}_signed"
        return f"KOR = {{ has_country_flag = {receipt} is_subject = no NOT = {{ has_war_with = {tag} }} }} has_country_flag = {receipt} is_subject = no NOT = {{ has_war_with = KOR }}"+_term_guards(c,[tag])
    result = f"KOR = {{ has_country_flag = {c['signed']} is_subject = no NOT = {{ has_war_with = {tag} }} }} has_country_flag = {c['signed']} is_subject = no NOT = {{ has_war_with = KOR }}"
    if c["key"] == "northern_security_compact": result += " KOR = { check_variable = { ruling_party = 4 } }"
    if c.get('usfk') and c['key'] not in ('us_garrison','us_drawdown'):result+=' COLDWAR_KOR_usfk_cooperation_live = yes'
    return result+_term_guards(c,c['tags'])


def _modifier_name(c, side, partner_tag=None):
    suffix = f"_{partner_tag.lower()}" if partner_tag and (side == "partner" and c["key"] in SELECTABLE_KEYS or side == "kor" and c["key"] == "nordpolitik_recognition") else ""
    return f"COLDWAR_KOR_1970_foreign_{c['key']}_{side}{suffix}"


def _event_localisation(c, localised):
    key = c["key"]
    recipient = c["recipient"]
    purposes = {
        "red_cross_channel": "The two Korean Red Cross organizations propose a humanitarian liaison channel.",
        "family_reunions": "The two Korean governments consider arrangements for visits by separated families.",
        "military_hotline": "Military representatives propose a direct communications link for managing incidents.",
        "nonaggression_compact": "The Korean governments consider a reciprocal commitment against armed aggression.",
        "verified_restraint": "Both governments consider reciprocal verification of military restraint.",
        "working_contacts": "The two Korean governments propose regular official working contacts.",
        "sovereign_confederation": "The Korean governments consider a consultative framework that preserves separate governments and armed forces.",
        "confederal_secretariat": "The participating governments consider a permanent secretariat for their consultative framework.",
        "parallel_recognition": "The two Korean governments consider reciprocal declarations recognizing their separate administrations.",
        "limited_trade": "The Korean governments consider a limited programme of civilian trade.",
        "northern_security_compact": "The Southern revolutionary government proposes a military liaison arrangement with the North.",
        "independent_left_dialogue": "An independent Southern socialist government proposes talks while retaining its own institutions.",
        "technology_licence": "Seoul seeks a licensed industrial know-how agreement with a foreign supplier.",
        "allied_procurement_contract": "Seoul seeks access to allied procurement and maintenance services. Equipment purchases remain separate contracts.",
        "us_alliance_assurance": "Seoul and Washington consider renewed alliance liaison and defense assurances.",
        "security_partner_contacts": "Seoul proposes limited cooperation between military staffs.",
        "japan_technology_finance": "Seoul proposes technical and financial cooperation with Japanese partners. Historical claims remain a separate question.",
        "historical_claims_dialogue": "Seoul and Tokyo consider talks on historical claims and their political implications.",
        "alternative_finance_contacts": "Seoul seeks additional sources of foreign finance to reduce its concentration of creditors.",
        "nordpolitik_recognition": "Seoul proposes a bilateral diplomatic and commercial opening. Each government must make its own decision.",
        "pacific_trade_contacts": "Seoul proposes technical cooperation to expand access to Pacific export markets.",
        "revolutionary_recognition": "The Southern revolutionary cabinet seeks diplomatic recognition without an automatic alliance or aid commitment.",
        "neutrality_guarantees": "The participating governments consider a negotiated neutrality framework requiring every signatory’s assent.",
        "vietnam_withdrawal_settlement": "Seoul seeks an agreed settlement of its remaining Vietnam commitment and veterans’ obligations.",
        "cultural_exchanges": "The Korean governments consider a framework for limited civilian exchanges.",
        "cultural_visits": "The Korean governments consider a programme of cultural and educational visits.",
        "border_notifications": "The Korean governments consider advance notification arrangements for military incidents.",
        "border_notice_protocol": "The Korean governments consider a reciprocal incident-notification protocol.",
        "korean_community_dialogue": "The Korean governments consider a common-community agenda while retaining separate governments and armed forces.",
        "japan_joint_training": "Korean and Japanese institutions propose a joint technical-training programme for industrial workers and engineers.",
        "gulf_project_access": "Korean contractors seek an agreement covering access to construction work, technical cooperation and the obligations of participating firms.",
        "worker_rights_protocol": "Seoul and Bonn consider common standards for the protection of Korean contract workers and the administration of their employment.",
        "peninsula_liaison_office": "The two Korean governments consider permanent liaison offices to supervise accepted agreements and resolve practical disputes.",
        "korean_final_settlement": "The two governments consider a political settlement sustaining cooperation while retaining separate administrations and armed forces.",
        "us_garrison": "Seoul and Washington consider the facilities, responsibilities and consultation arrangements supporting the American presence in Korea.",
        "us_drawdown": "Seoul proposes a negotiated reduction of the resident American presence while preserving consultation and the possibility of agreed exercises.",
        "us_combined_command": "The allies consider a combined command structure linking operational planning with Korean host-nation support.",
        "combined_readiness_board": "The two military establishments propose a standing readiness board to assess combined plans, logistics and reinforcement requirements.",
    }
    localised[f"COLDWAR_KOR_foreign.{c['event_index']}.t"] = AGREEMENTS[key]
    localised[f"COLDWAR_KOR_foreign.{c['event_index']}.d"] = purposes[key]
    localised[f"COLDWAR_KOR_foreign.{c['event_index']}.option_a"] = "Accept the agreement"
    localised[f"COLDWAR_KOR_foreign.{c['event_index']}.option_b"] = "Decline the agreement"
    localised[f"COLDWAR_KOR_foreign.{c['event_index']}.option_c"] = "Close the Lapsed Proposal"
    localised[f"COLDWAR_KOR_{key}_offer_tt"] = agreement_terms(c,offer=True)
    localised[f"COLDWAR_KOR_foreign.{c['event_index']}.accepted_tt"] = agreement_terms(c,offer=False)
    if c.get("selector_index"):
        localised[f"COLDWAR_KOR_foreign.{c['selector_index']}.t"] = "Select a negotiating counterpart"
        localised[f"COLDWAR_KOR_foreign.{c['selector_index']}.d"] = "Choose which government will receive this proposal. No agreement or payment takes effect until that government accepts."
        localised[f"COLDWAR_KOR_foreign.{c['selector_index']}.option_cancel"] = "Defer the Approach"
        for tag in c["tags"]:
            localised[f"COLDWAR_KOR_foreign.{c['selector_index']}.option_{tag}"] = {"USA":"Approach the United States","JAP":"Approach Japan","GER":"Approach West Germany","SOV":"Approach the Soviet Union","CHI":"Approach China"}.get(tag, f"Approach {tag}")
    localised[f"COLDWAR_KOR_foreign.{c['reply_index']}.t"] = AGREEMENTS[key]+": Agreement Reached"
    localised[f"COLDWAR_KOR_foreign.{c['reply_index']}.d"] = "The negotiating governments have accepted the agreement. Its financial commitments and cooperative arrangements are now in force."
    localised[f"COLDWAR_KOR_foreign.{c['reply_index']}.option_a"] = "Return to the diplomatic programme"
    localised[f"COLDWAR_KOR_foreign.{c['expiry_index']}.t"] = "Agreement offer expired"
    localised[f"COLDWAR_KOR_foreign.{c['expiry_index']}.d"] = "The response period ended without a complete agreement. No payment or agreement effects were applied."
    localised[f"COLDWAR_KOR_foreign.{c['expiry_index']}.option_a"] = "Continue"
    for index,title,desc in (
        (c['refusal_index'],AGREEMENTS[key]+": Proposal Declined","The other government has declined the proposed terms. Our delegation will have to reconsider the political conditions before seeking a new round of negotiations."),
        (c['notice_index'],AGREEMENTS[key]+": Negotiations Lapsed","The proposed terms have not secured the required agreement within the response period. The delegation has closed this round of negotiations.")):
        localised[f'COLDWAR_KOR_foreign.{index}.t']=title
        localised[f'COLDWAR_KOR_foreign.{index}.d']=desc
        localised[f'COLDWAR_KOR_foreign.{index}.option_a']='Review Our Position'


def _trigger_tags(tags):
    return "\n".join(f"{t} = {{ exists = yes is_subject = no }}" for t in tags)


def _numeric_effects(tag, c, side, partner_tag=None, display=False):
    lines = [f"{tag} = {{"]
    delta = -c.get("KOR_cost_bn", 0) if side == "kor" else c.get("recipient_effects", {}).get("treasury_change", 0)
    if delta:
        lines += [f"\tset_temp_variable = {{ treasury_change = {_q(delta)} }}", "\tmodify_treasury_effect = yes"]
    policy = _policy(c, side)
    if policy:
        lines += [f"\tadd_ideas = COLDWAR_KOR_agreement_{c['key']}_{side}_preview"] if display else [f"\tadd_dynamic_modifier = {{ modifier = {_modifier_name(c, side, partner_tag)} }}"]
    if (c["key"] == "nonaggression_compact" or c.get('non_aggression')) and tag == "KOR":
        for target in c["tags"]:
            if target != tag:
                lines.append(f"\tdiplomatic_relation = {{ country = {target} relation = non_aggression_pact active = yes }}")
    if display and side=='kor' and c['key']=='sovereign_confederation':lines.append('\tadd_ideas = COLDWAR_KOR_confederal_member')
    if display and side=='kor' and c['key'] in ('us_garrison','us_drawdown'):lines.append('\tadd_ideas = COLDWAR_KOR_usfk_member')
    if display and side=='kor' and c['key']=='us_garrison':lines.append('\tgive_military_access = USA')
    lines.append("}")
    return lines


def _scripted_triggers(contracts):
    out = [SCRIPT_COMMENT, '''COLDWAR_KOR_usfk_cooperation_live = {
      KOR = { exists = yes IMP_is_1970_scenario = yes is_subject = no has_idea = COLDWAR_KOR_usfk_member NOT = { has_war_with = USA } }
      USA = { exists = yes is_subject = no has_idea = COLDWAR_KOR_usfk_member }
      OR = {
        AND = { KOR = { has_country_flag = COLDWAR_KOR_us_garrison_signed } USA = { has_country_flag = COLDWAR_KOR_us_garrison_signed } }
        AND = { KOR = { has_country_flag = COLDWAR_KOR_us_drawdown_signed } USA = { has_country_flag = COLDWAR_KOR_us_drawdown_signed } }
      }
    }''']
    for c in contracts:
        key = c["key"]
        tags = c["tags"]
        pending = c["pending"]
        signed = c["signed"]
        out.append(f"COLDWAR_KOR_can_send_{key} = {{")
        out += ["\ttag = KOR", "\toriginal_tag = KOR", "\tIMP_is_1970_scenario = yes", "\tis_subject = no"]
        if key in SELECTABLE_KEYS:
            out.append("\tOR = { " + " ".join(f"{t} = {{ exists = yes is_subject = no NOT = {{ has_war_with = KOR }} }}" for t in tags) + " }")
        else:
            out.append("\t" + _trigger_tags(tags).replace("\n", "\n\t"))
            for tag in tags: out.append(f"\tNOT = {{ {tag} = {{ has_war_with = KOR }} }}")
        if key == "nordpolitik_recognition":
            out.append("\tOR = { " + " ".join(f"NOT = {{ {t} = {{ has_country_flag = COLDWAR_KOR_{key}_{t}_signed }} }}" for t in tags) + " }")
        else:
            out.append(f"\tNOT = {{ has_country_flag = {signed} }}")
        out.append(f"\tNOT = {{ has_country_flag = {pending} }}")
        out.append(f"\tNOT = {{ has_country_flag = COLDWAR_KOR_{key}_cooldown }}")
        if key in {"working_contacts", "sovereign_confederation"}:
            out += ["\tNKO = { NOT = { has_country_flag = COLDWAR_NKO_korean_channel_pending } NOT = { has_country_flag = COLDWAR_NKO_foreign_korean_channel_confederation_offer_pending } }", "\tKOR = { NOT = { has_country_flag = COLDWAR_NKO_korean_channel_pending } NOT = { has_country_flag = COLDWAR_NKO_foreign_korean_channel_confederation_offer_pending } }"]
        if key == "confederal_secretariat":
            out += ["\thas_idea = COLDWAR_KOR_confederal_member", "\tNKO = { has_idea = COLDWAR_KOR_confederal_member }"]
        if key == "northern_security_compact": out.append("\tcheck_variable = { ruling_party = 4 }")
        if key == "vietnam_withdrawal_settlement": out.append("\thas_country_flag = COLDWAR_KOR_vietnam_commitment_active")
        if c.get('usfk') and key not in ('us_garrison','us_drawdown'):out.append('\tCOLDWAR_KOR_usfk_cooperation_live = yes')
        if key=='us_drawdown':out.append('\thas_country_flag = COLDWAR_KOR_strategic_autonomy_paid')
        out.append("}")
        out.append(f"COLDWAR_KOR_can_accept_{key} = {{")
        if c.get('revised_terms'):out.append(f'\tKOR = {{ has_country_flag = COLDWAR_KOR_{key}_offer_v3 }}')
        out.append("\tKOR = { original_tag = KOR IMP_is_1970_scenario = yes is_subject = no }")
        out.append(f"\tKOR = {{ check_variable = {{ var = COLDWAR_KOR_{key}_sender_party value = ruling_party compare = equals }} }}")
        out.append(f"\tKOR = {{ check_variable = {{ var = COLDWAR_KOR_{key}_sender_office_epoch value = COLDWAR_KOR_office_epoch compare = equals }} }}")
        if key not in SELECTABLE_KEYS:
            out.append("\t" + _trigger_tags(tags).replace("\n", "\n\t"))
            for tag in tags: out.append(f"\tNOT = {{ {tag} = {{ has_war_with = KOR }} }}")
        if key in {"working_contacts", "sovereign_confederation"}:
            out += ["\tNKO = { NOT = { has_country_flag = COLDWAR_NKO_korean_channel_pending } NOT = { has_country_flag = COLDWAR_NKO_foreign_korean_channel_confederation_offer_pending } }", "\tKOR = { NOT = { has_country_flag = COLDWAR_NKO_korean_channel_pending } NOT = { has_country_flag = COLDWAR_NKO_foreign_korean_channel_confederation_offer_pending } }"]
        out.append(f"\tKOR = {{ has_country_flag = {pending} has_country_flag = COLDWAR_KOR_{key}_offer_open }}")
        if key in SELECTABLE_KEYS:
            out.append("\tOR = { " + " ".join(f"AND = {{ tag = {t} {t} = {{ exists = yes is_subject = no NOT = {{ has_war_with = KOR }} }} KOR = {{ has_country_flag = COLDWAR_KOR_{key}_target_{t} }} {t} = {{ has_country_flag = {pending} has_country_flag = COLDWAR_KOR_{key}_offer_open NOT = {{ has_country_flag = COLDWAR_KOR_{key}_{t}_signed }} }} }}" for t in tags) + " }")
        else:
            for tag in tags: out.append(f"\t{tag} = {{ has_country_flag = {pending} has_country_flag = COLDWAR_KOR_{key}_offer_open NOT = {{ has_country_flag = {signed} }} }}")
            out.append("\tOR = { " + " ".join(f"AND = {{ tag = {tag} {tag} = {{ has_country_flag = {pending} has_country_flag = COLDWAR_KOR_{key}_offer_open }} }}" for tag in tags) + " }")
        out.append(f"\tNOT = {{ KOR = {{ has_country_flag = COLDWAR_KOR_{key}_cooldown }} }}")
        if key == "confederal_secretariat":
            out += ["\tKOR = { has_idea = COLDWAR_KOR_confederal_member }", "\tNKO = { has_idea = COLDWAR_KOR_confederal_member }"]
        if key == "northern_security_compact":
            out += ["\tKOR = { check_variable = { ruling_party = 4 } }"]
        if key == "vietnam_withdrawal_settlement":
            out.append("\tKOR = { has_country_flag = COLDWAR_KOR_vietnam_commitment_active }")
        if c.get('usfk') and key not in ('us_garrison','us_drawdown'):out.append('\tCOLDWAR_KOR_usfk_cooperation_live = yes')
        out.append("}")
        out.append(f"COLDWAR_KOR_can_refuse_{key} = {{ KOR = {{ has_country_flag = {pending} has_country_flag = COLDWAR_KOR_{key}_offer_open }}")
        if key in SELECTABLE_KEYS:
            out.append("\tOR = { " + " ".join(f"AND = {{ tag = {tag} KOR = {{ has_country_flag = COLDWAR_KOR_{key}_target_{tag} }} {tag} = {{ has_country_flag = {pending} has_country_flag = COLDWAR_KOR_{key}_offer_open }} }}" for tag in tags) + " }")
        else:
            out.append("\tOR = { " + " ".join(f"AND = {{ tag = {tag} {tag} = {{ has_country_flag = {pending} has_country_flag = COLDWAR_KOR_{key}_offer_open }} }}" for tag in tags) + " }")
        out.append("}")
    return "\n".join(out) + "\n"


def _scripted_effects(contracts):
    out = [SCRIPT_COMMENT]
    # One send effect per agreement. Partner selection is done by a genuine
    # player event, never by choosing the first extant country silently.
    for c in contracts:
        key, tags = c["key"], c["tags"]
        preview=_numeric_effects('KOR',c,'kor',display=True)
        if len(tags)==1:preview+=_numeric_effects(tags[0],c,'partner',display=True)
        out += [f'COLDWAR_KOR_preview_agreement_{key} = {{']+['\t'+x for x in preview]+['}']
        out.append(f"COLDWAR_KOR_send_{key} = {{")
        out.append("\tif = {")
        out.append(f"\t\tlimit = {{ COLDWAR_KOR_can_send_{key} = yes }}")
        if key in SELECTABLE_KEYS:
            out.append(f"\t\tKOR = {{ country_event = {{ id = COLDWAR_KOR_foreign.{c['selector_index']} }} }}")
            out.append("\t}")
            out.append("}")
            for tag in tags:
                out.append(f"COLDWAR_KOR_send_{key}_to_{tag} = {{")
                out.append(f"\tif = {{ limit = {{ COLDWAR_KOR_can_send_{key} = yes NOT = {{ {tag} = {{ has_country_flag = COLDWAR_KOR_{key}_{tag}_signed }} }} }}")
                out.append(f"\t\tKOR = {{ set_variable = {{ COLDWAR_KOR_{key}_sender_party = ruling_party }} set_variable = {{ COLDWAR_KOR_{key}_sender_office_epoch = COLDWAR_KOR_office_epoch }} clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} set_country_flag = {c['pending']} set_country_flag = {{ flag = COLDWAR_KOR_{key}_offer_open days = 60 }} set_country_flag = COLDWAR_KOR_{key}_target_{tag} set_country_flag = COLDWAR_KOR_{key}_assent_{tag} }}")
                out.append(f'\t\tKOR = {{ clr_country_flag = COLDWAR_KOR_{key}_refused clr_country_flag = COLDWAR_KOR_{key}_expired }}')
                if c.get('revised_terms'):out.append(f'\t\tKOR = {{ set_country_flag = COLDWAR_KOR_{key}_offer_v3 }}')
                out.append(f"\t\t{tag} = {{ clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} set_country_flag = {c['pending']} set_country_flag = {{ flag = COLDWAR_KOR_{key}_offer_open days = 60 }} country_event = {{ id = COLDWAR_KOR_foreign.{c['event_index']} }} }}")
                out.append(f"\t\tKOR = {{ country_event = {{ id = COLDWAR_KOR_foreign.{c['expiry_index']} days = 61 }} }}")
                out.append("\t}")
                out.append("}")
        else:
            clear_kor_assent = f"clr_country_flag = COLDWAR_KOR_{key}_assent_KOR " + " ".join(f"clr_country_flag = COLDWAR_KOR_{key}_assent_{tag}" for tag in tags)
            out.append(f"\t\tKOR = {{ set_variable = {{ COLDWAR_KOR_{key}_sender_party = ruling_party }} set_variable = {{ COLDWAR_KOR_{key}_sender_office_epoch = COLDWAR_KOR_office_epoch }} {clear_kor_assent} set_country_flag = {c['pending']} set_country_flag = {{ flag = COLDWAR_KOR_{key}_offer_open days = 60 }} }}")
            out.append(f'\t\tKOR = {{ clr_country_flag = COLDWAR_KOR_{key}_refused clr_country_flag = COLDWAR_KOR_{key}_expired }}')
            if c.get('revised_terms'):out.append(f'\t\tKOR = {{ set_country_flag = COLDWAR_KOR_{key}_offer_v3 }}')
            for tag in tags:
                out.append(f"\t\t{tag} = {{ clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} set_country_flag = {c['pending']} set_country_flag = {{ flag = COLDWAR_KOR_{key}_offer_open days = 60 }} country_event = {{ id = COLDWAR_KOR_foreign.{c['event_index']} }} }}")
            out.append(f"\t\tKOR = {{ country_event = {{ id = COLDWAR_KOR_foreign.{c['expiry_index']} days = 61 }} }}")
            out.append("\t}")
            out.append("}")
        # Consent is recorded first; agreement effects and all payments are
        # applied only once every named signer has assented.
        out.append(f"COLDWAR_KOR_accept_{key} = {{")
        out.append(f"\tif = {{ limit = {{ COLDWAR_KOR_can_accept_{key} = yes }}")
        for tag in tags:
            out.append(f"\t\tif = {{ limit = {{ tag = {tag} }} set_country_flag = COLDWAR_KOR_{key}_assent_{tag} }}")
        if key in SELECTABLE_KEYS:
            for tag in tags:
                target_signed = f"COLDWAR_KOR_{key}_{tag}_signed"
                out.append(f"\t\tif = {{ limit = {{ tag = {tag} KOR = {{ has_country_flag = COLDWAR_KOR_{key}_target_{tag} has_country_flag = COLDWAR_KOR_{key}_assent_{tag} }} }}")
                out.append(f"\t\t\tKOR = {{ set_country_flag = {c['signed']} set_country_flag = {target_signed} clr_country_flag = {c['pending']} clr_country_flag = COLDWAR_KOR_{key}_offer_open clr_country_flag = COLDWAR_KOR_{key}_target_{tag} }}")
                out.append(f"\t\t\tKOR = {{ clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} }}")
                out.append(f"\t\t\t{tag} = {{ set_country_flag = {c['signed']} set_country_flag = {target_signed} clr_country_flag = {c['pending']} clr_country_flag = COLDWAR_KOR_{key}_offer_open clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} }}")
                if c.get('revised_terms'):out.append(f'\t\t\tKOR = {{ set_country_flag = COLDWAR_KOR_{key}_terms_v3 }} {tag} = {{ set_country_flag = COLDWAR_KOR_{key}_terms_v3 }}')
                if c.get("duration_days", 0) and key != "nordpolitik_recognition":
                    out.append(f"\t\t\tKOR = {{ clr_country_flag = {c['signed']} set_country_flag = {{ flag = {c['signed']} days = {c['duration_days']} }} set_country_flag = {{ flag = {target_signed} days = {c['duration_days']} }} }}")
                    out.append(f"\t\t\t{tag} = {{ clr_country_flag = {c['signed']} set_country_flag = {{ flag = {c['signed']} days = {c['duration_days']} }} set_country_flag = {{ flag = {target_signed} days = {c['duration_days']} }} }}")
                elif c.get("duration_days", 0):
                    out.append(f"\t\t\tKOR = {{ clr_country_flag = {target_signed} set_country_flag = {{ flag = {target_signed} days = {c['duration_days']} }} }}")
                    out.append(f"\t\t\t{tag} = {{ clr_country_flag = {c['signed']} set_country_flag = {{ flag = {c['signed']} days = {c['duration_days']} }} clr_country_flag = {target_signed} set_country_flag = {{ flag = {target_signed} days = {c['duration_days']} }} }}")
                if key == "nordpolitik_recognition":
                    out.append(f"\t\t\tKOR = {{ add_dynamic_modifier = {{ modifier = {_modifier_name(c, 'kor', tag)} }} }}")
                    out.append(f"\t\t\t{tag} = {{ add_dynamic_modifier = {{ modifier = {_modifier_name(c, 'partner', tag)} }} }}")
                else:
                    out.extend("\t\t\t" + x for x in _numeric_effects("KOR", c, "kor"))
                    out.extend("\t\t\t" + x for x in _numeric_effects(tag, c, "partner", tag))
                out.append("\t\t\tKOR = { COLDWAR_KOR_refresh_programmes = yes }")
                out.append(f"\t\t\tKOR = {{ country_event = {{ id = COLDWAR_KOR_foreign.{c['reply_index']} }} }}")
                out.append("\t\t}")
        else:
            complete = " ".join([f"{t} = {{ has_country_flag = COLDWAR_KOR_{key}_assent_{t} }}" for t in tags])
            out.append(f"\t\tif = {{ limit = {{ {complete} }}")
            out.append(f"\t\t\tKOR = {{ set_country_flag = {c['signed']} clr_country_flag = {c['pending']} clr_country_flag = COLDWAR_KOR_{key}_offer_open clr_country_flag = COLDWAR_KOR_{key}_assent_KOR }}")
            for tag in tags: out.append(f"\t\t\t{tag} = {{ set_country_flag = {c['signed']} clr_country_flag = {c['pending']} clr_country_flag = COLDWAR_KOR_{key}_offer_open clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} }}")
            if c.get('revised_terms'):
                for tag in ['KOR']+tags:out.append(f'\t\t\t{tag} = {{ set_country_flag = COLDWAR_KOR_{key}_terms_v3 }}')
            if c.get("duration_days", 0):
                out.append(f"\t\t\tKOR = {{ clr_country_flag = {c['signed']} set_country_flag = {{ flag = {c['signed']} days = {c['duration_days']} }} }}")
                for tag in tags: out.append(f"\t\t\t{tag} = {{ clr_country_flag = {c['signed']} set_country_flag = {{ flag = {c['signed']} days = {c['duration_days']} }} }}")
            if key == "sovereign_confederation":
                out.append("\t\t\tKOR = { add_ideas = COLDWAR_KOR_confederal_member }")
                for tag in tags: out.append(f"\t\t\t{tag} = {{ add_ideas = COLDWAR_KOR_confederal_member }}")
            if key=='us_garrison':out.append('\t\t\tKOR = { COLDWAR_KOR_ratify_us_garrison = yes }')
            if key=='us_drawdown':out.append('\t\t\tKOR = { COLDWAR_KOR_ratify_us_drawdown = yes }')
            if key == "vietnam_withdrawal_settlement": out.append("\t\t\tKOR = { clr_country_flag = COLDWAR_KOR_vietnam_commitment_active }")
            out.extend("\t\t\t" + x for x in _numeric_effects("KOR", c, "kor"))
            for tag in tags: out.extend("\t\t\t" + x for x in _numeric_effects(tag, c, "partner"))
            out.append("\t\t\tKOR = { COLDWAR_KOR_refresh_programmes = yes }")
            out.append(f"\t\t\tKOR = {{ country_event = {{ id = COLDWAR_KOR_foreign.{c['reply_index']} }} }}")
            out.append("\t\t}")
        out.append("\t}")
        out.append("}")
        out.append(f"COLDWAR_KOR_refuse_{key} = {{")
        out.append(f"\tif = {{ limit = {{ COLDWAR_KOR_can_refuse_{key} = yes }}")
        out.append(f"\tKOR = {{ clr_country_flag = {c['pending']} clr_country_flag = COLDWAR_KOR_{key}_offer_open clr_country_flag = COLDWAR_KOR_{key}_assent_KOR set_country_flag = COLDWAR_KOR_{key}_refused set_country_flag = {{ flag = COLDWAR_KOR_{key}_cooldown days = 180 }} }}")
        for tag in tags:
            out.append(f"\tKOR = {{ clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} clr_country_flag = COLDWAR_KOR_{key}_target_{tag} }}")
        for tag in tags:
            out.append(f"\t{tag} = {{ clr_country_flag = {c['pending']} clr_country_flag = COLDWAR_KOR_{key}_offer_open clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} }}")
        out.append(f"\tKOR = {{ country_event = {{ id = COLDWAR_KOR_foreign.{c['refusal_index']} }} }}")
        out.append("\t}")
        out.append("}")
        out.append(f"COLDWAR_KOR_expire_{key} = {{")
        out.append(f"\tif = {{ limit = {{ has_country_flag = {c['pending']} NOT = {{ has_country_flag = COLDWAR_KOR_{key}_offer_open }} }}")
        out.append(f"\t\tclr_country_flag = {c['pending']}")
        out.append(f"\t\tclr_country_flag = COLDWAR_KOR_{key}_offer_open")
        out.append(f"\t\tset_country_flag = COLDWAR_KOR_{key}_expired")
        out.append(f"\t\tset_country_flag = {{ flag = COLDWAR_KOR_{key}_cooldown days = 180 }}")
        out.append(f"\t\tKOR = {{ clr_country_flag = COLDWAR_KOR_{key}_assent_KOR }}")
        for tag in tags:
            out.append(f"\t\tKOR = {{ clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} clr_country_flag = COLDWAR_KOR_{key}_target_{tag} }}")
        for tag in tags:
            out.append(f"\t\t{tag} = {{ clr_country_flag = {c['pending']} clr_country_flag = COLDWAR_KOR_{key}_offer_open clr_country_flag = COLDWAR_KOR_{key}_assent_{tag} }}")
        out.append(f'\t\tcountry_event = {{ id = COLDWAR_KOR_foreign.{c["notice_index"]} }}')
        out.append("\t}")
        out.append("}")

    # Central reader called from the two native budget calculators. The payer
    # and payee roles are explicit so ROOT never shifts a contract's direction.
    out.append("COLDWAR_KOR_contract_expenses = {")
    for c in contracts:
        key = c["key"]
        if c.get("KOR_weekly_bn", 0):
            if key in SELECTABLE_KEYS:
                active = "OR = { " + " ".join(f"AND = {{ { _agreement_active(c, 'kor', t) } }}" for t in c["tags"]) + " }"
                gate = f"tag = KOR {active}"
            else: gate = f"tag = KOR {_agreement_active(c)}"
            out += ["\tif = {", f"\t\tlimit = {{ {gate} }}", f"\t\tadd_to_variable = {{ additional_expenses_rate = {_q(c['KOR_weekly_bn'])} }}", "\t}"]
        weekly = c.get("recipient_effects", {}).get("weekly_expense_bn", 0)
        for tag in c["tags"]:
            if weekly:
                out += ["\tif = {", f"\t\tlimit = {{ tag = {tag} {_recipient_pair_active(c, tag)} }}", f"\t\tadd_to_variable = {{ additional_expenses_rate = {_q(weekly)} }}", "\t}"]
    out.append("\tCOLDWAR_KOR_usfk_exercise_expenses = yes")
    out.append("}")
    out.append("COLDWAR_KOR_contract_income = {")
    for c in contracts:
        income = c.get("recipient_effects", {}).get("weekly_income_bn", 0)
        if income:
            for tag in c["tags"]:
                out += ["\tif = {", f"\t\tlimit = {{ tag = {tag} {_recipient_pair_active(c, tag)} }}", f"\t\tadd_to_variable = {{ additional_income_rate = {_q(income)} }}", "\t}"]
    out.append("}")

    out.append("COLDWAR_KOR_contract_maintenance = {")
    out.append('\tKOR = { COLDWAR_KOR_upgrade_agreement_terms = yes }')
    for c in contracts:
        key = c["key"]
        # The live window closes on day60. A persistent pending receipt lets
        # daily maintenance recover even if an engine callback was missed.
        out.append(f"\tif = {{ limit = {{ KOR = {{ has_country_flag = {c['pending']} NOT = {{ has_country_flag = COLDWAR_KOR_{key}_offer_open }} }} }} KOR = {{ COLDWAR_KOR_expire_{key} = yes }} }}")
        if key in SELECTABLE_KEYS:
            for t in c["tags"]:
                ts = f"COLDWAR_KOR_{key}_{t}_signed"
                bad_pair = f"NOT = {{ {_agreement_active(c, 'kor', t)} }}"
                out.append(f"\tif = {{ limit = {{ KOR = {{ has_country_flag = {ts} }} {bad_pair} }}")
                out.append(f"\t\tKOR = {{ clr_country_flag = {ts} clr_country_flag = COLDWAR_KOR_{key}_target_{t} }}")
                out.append(f"\t\t{t} = {{ clr_country_flag = {ts} clr_country_flag = {c['signed']} }}")
                if _policy(c, "partner"): out.append(f"\t\t{t} = {{ remove_dynamic_modifier = {{ modifier = {_modifier_name(c, 'partner', t)} }} }}")
                if key == "nordpolitik_recognition" and _policy(c, "kor"):
                    out.append(f"\t\tKOR = {{ remove_dynamic_modifier = {{ modifier = {_modifier_name(c, 'kor', t)} }} }}")
                out.append("\t}")
            if key == "nordpolitik_recognition":
                any_pair = "OR = { " + " ".join(f"KOR = {{ has_country_flag = COLDWAR_KOR_{key}_{t}_signed }}" for t in c["tags"]) + " }"
                out.append(f"\tif = {{ limit = {{ KOR = {{ has_country_flag = {c['signed']} }} NOT = {{ {any_pair} }} }}")
                out.append(f"\t\tKOR = {{ clr_country_flag = {c['signed']} }}")
                out.append("\t}")
            else:
                active_pair = _agreement_active(c, "kor")
                out.append(f"\tif = {{ limit = {{ KOR = {{ has_country_flag = {c['signed']} }} NOT = {{ {active_pair} }} }}")
                out.append(f"\t\tKOR = {{ clr_country_flag = {c['signed']} remove_dynamic_modifier = {{ modifier = {_modifier_name(c, 'kor')} }} }}")
                out.append("\t}")
            continue
        invalid_terms = ["KOR = { exists = no }", "KOR = { is_subject = yes }"]
        for t in c["tags"]:
            invalid_terms.extend([f"{t} = {{ exists = no }}", f"{t} = {{ is_subject = yes }}", f"{t} = {{ has_war_with = KOR }}"])
        if key == "northern_security_compact": invalid_terms.append("NOT = { KOR = { check_variable = { ruling_party = 4 } } }")
        invalid = "OR = { " + " ".join(invalid_terms) + " }"
        out.append(f"\tif = {{ limit = {{ KOR = {{ has_country_flag = {c['signed']} }} {invalid} }}")
        out.append(f"\t\tKOR = {{ clr_country_flag = {c['signed']} }}")
        for t in c["tags"]:
            out.append(f"\t\t{t} = {{ clr_country_flag = {c['signed']} }}")
        for side, scope in [("kor", "KOR")]+[("partner", t) for t in c["tags"]]:
            if _policy(c, side):
                out.append(f"\t\t{scope} = {{ remove_dynamic_modifier = {{ modifier = {_modifier_name(c, side)} }} }}")
        if key == "sovereign_confederation":
            out.append("\t\tKOR = { remove_ideas = COLDWAR_KOR_confederal_member }")
            for t in c["tags"]: out.append(f"\t\t{t} = {{ remove_ideas = COLDWAR_KOR_confederal_member }}")
        out.append("\t}")
        # Timed contracts clear their signed receipt on natural expiry.
        if c.get("duration_days", 0):
            out.append(f"\tif = {{ limit = {{ KOR = {{ has_country_flag = {c['signed']} }} NOT = {{ {c['tags'][0]} = {{ has_country_flag = {c['signed']} }} }} }}")
            out.append(f"\t\tKOR = {{ clr_country_flag = {c['signed']} }}")
            for t in c["tags"]: out.append(f"\t\t{t} = {{ clr_country_flag = {c['signed']} }}")
            for side, scope in [("kor", "KOR")]+[("partner", t) for t in c["tags"]]:
                if _policy(c, side): out.append(f"\t\t{scope} = {{ remove_dynamic_modifier = {{ modifier = {_modifier_name(c, side)} }} }}")
            if key == "sovereign_confederation":
                out.append("\t\tKOR = { remove_ideas = COLDWAR_KOR_confederal_member }")
                for t in c["tags"]: out.append(f"\t\t{t} = {{ remove_ideas = COLDWAR_KOR_confederal_member }}")
            out.append("\t}")
    out.append("\tKOR = { COLDWAR_KOR_usfk_reconcile = yes }")
    out.append("}")
    # Grandfather only the genuine old two-country acceptance ledger. This adds
    # membership as a zero-stat receipt; legacy spending and modifiers stay with NKO.
    out += ["COLDWAR_KOR_grandfather_nko_framework = {", "\tif = {", "\t\tlimit = { NKO = { exists = yes has_country_flag = COLDWAR_NKO_korean_channel_confederation_offer_accepted } KOR = { exists = yes has_country_flag = COLDWAR_NKO_korean_channel_confederation_offer_accepted } }", "\t\tKOR = { add_ideas = COLDWAR_KOR_confederal_member }", "\t\tNKO = { add_ideas = COLDWAR_KOR_confederal_member }", "\t}", "}"]
    # Idempotent startup/monthly synchronization never replays payments.
    out += ["COLDWAR_KOR_foreign_initialize = {", "\tCOLDWAR_KOR_grandfather_nko_framework = yes", "\tCOLDWAR_KOR_foreign_refresh = yes", "}", "COLDWAR_KOR_foreign_refresh = {"]
    for c in contracts:
        entries = ([*(('kor', 'KOR', t) for t in c['tags']), *(('partner', t, t) for t in c['tags'])] if c["key"] == "nordpolitik_recognition" else [("kor", "KOR", None)] + [("partner", t, t if c["key"] in SELECTABLE_KEYS else None) for t in c["tags"]])
        for side, scope, partner_tag in entries:
            mod = _modifier_name(c, side, partner_tag)
            if _policy(c, side):
                active = _agreement_active(c, side, partner_tag)
                out += [f"\tif = {{ limit = {{ {active} {scope} = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {mod} }} }} }} }}", f"\t\t{scope} = {{ add_dynamic_modifier = {{ modifier = {mod} }} }}", "\t}"]
                out += [f"\tif = {{ limit = {{ NOT = {{ {active} }} {scope} = {{ has_dynamic_modifier = {{ modifier = {mod} }} }} }}", f"\t\t{scope} = {{ remove_dynamic_modifier = {{ modifier = {mod} }} }}", "\t}"]
    out.append("\tCOLDWAR_KOR_contract_maintenance = yes")
    out.append("}")
    return "\n".join(out) + "\n"


def _events(contracts, localised):
    out = [SCRIPT_COMMENT, "add_namespace = COLDWAR_KOR_foreign"]
    for c in contracts:
        idx, rep, exp = c["event_index"], c["reply_index"], c["expiry_index"]
        key = c["key"]
        if c.get("selector_index"):
            out += ["country_event = {", f"\tid = COLDWAR_KOR_foreign.{c['selector_index']}", "\tis_triggered_only = yes", f"\ttitle = COLDWAR_KOR_foreign.{c['selector_index']}.t", f"\tdesc = COLDWAR_KOR_foreign.{c['selector_index']}.d"]
            for tag in c["tags"]:
                out += ["\toption = {", f"\t\tname = COLDWAR_KOR_foreign.{c['selector_index']}.option_{tag}", f"\t\ttrigger = {{ {tag} = {{ exists = yes is_subject = no }} }}", f"\t\tCOLDWAR_KOR_send_{key}_to_{tag} = yes", "\t}"]
            out += [f"\toption = {{ name = COLDWAR_KOR_foreign.{c['selector_index']}.option_cancel }}", "}"]
        out += ["country_event = {", f"\tid = COLDWAR_KOR_foreign.{idx}", "\tis_triggered_only = yes", f"\ttitle = COLDWAR_KOR_foreign.{idx}.t", f"\tdesc = COLDWAR_KOR_foreign.{idx}.d", "\toption = {", f"\t\tname = COLDWAR_KOR_foreign.{idx}.option_a", f"\t\ttrigger = {{ COLDWAR_KOR_can_accept_{key} = yes }}", "\t\teffect_tooltip = {"]
        if key == "nordpolitik_recognition":
            for tag in c["tags"]:
                out.append(f"\t\t\tif = {{ limit = {{ tag = {tag} }}")
                out.extend("\t\t\t\t" + x for x in _numeric_effects("KOR", c, "kor", tag, display=True))
                out.extend("\t\t\t\t" + x for x in _numeric_effects("ROOT", c, "partner", tag, display=True))
                out.append("\t\t\t}")
        else:
            for line in _numeric_effects("KOR", c, "kor", display=True):
                out.append("\t\t\t" + line)
        if key in SELECTABLE_KEYS and key != "nordpolitik_recognition":
            for tag in c["tags"]:
                out.append(f"\t\t\tif = {{ limit = {{ tag = {tag} }}")
                out.extend("\t\t\t\t" + x for x in _numeric_effects("ROOT", c, "partner", tag, display=True))
                out.append("\t\t\t}")
        elif key not in SELECTABLE_KEYS:
            out.extend("\t\t\t" + x for x in _numeric_effects("ROOT", c, "partner", display=True))
        out += ["\t\t}", f"\t\tcustom_effect_tooltip = COLDWAR_KOR_foreign.{idx}.accepted_tt", f"\t\tCOLDWAR_KOR_accept_{key} = yes", "\t}", "\toption = {", f"\t\tname = COLDWAR_KOR_foreign.{idx}.option_b", f"\t\ttrigger = {{ COLDWAR_KOR_can_refuse_{key} = yes }}", f"\t\tCOLDWAR_KOR_refuse_{key} = yes", "\t}", f"\toption = {{ name = COLDWAR_KOR_foreign.{idx}.option_c trigger = {{ NOT = {{ OR = {{ COLDWAR_KOR_can_accept_{key} = yes COLDWAR_KOR_can_refuse_{key} = yes }} }} }} }}", "}"]
        out += ["country_event = {", f"\tid = COLDWAR_KOR_foreign.{rep}", "\tis_triggered_only = yes", f"\ttitle = COLDWAR_KOR_foreign.{rep}.t", f"\tdesc = COLDWAR_KOR_foreign.{rep}.d", "\toption = {", f"\t\tname = COLDWAR_KOR_foreign.{rep}.option_a", "\t}", "}"]
        out += ["country_event = {", f"\tid = COLDWAR_KOR_foreign.{exp}", "\tis_triggered_only = yes", "\thidden = yes", f"\ttrigger = {{ has_country_flag = {c['pending']} NOT = {{ has_country_flag = COLDWAR_KOR_{key}_offer_open }} }}", "\timmediate = {", f"\t\tCOLDWAR_KOR_expire_{key} = yes", "\t}", "}"]
        for result in (c['refusal_index'],c['notice_index']):
            out += ['country_event = {',f'\tid = COLDWAR_KOR_foreign.{result}','\tis_triggered_only = yes',f'\ttitle = COLDWAR_KOR_foreign.{result}.t',f'\tdesc = COLDWAR_KOR_foreign.{result}.d',f'\toption = {{ name = COLDWAR_KOR_foreign.{result}.option_a }}','}']
        _event_localisation(c, localised)
    localised['COLDWAR_KOR_foreign.700.t']='Renewing the Cooperation Agreements'
    localised['COLDWAR_KOR_foreign.700.d']='Our delegations have reviewed the practical obligations of earlier frameworks. New funding and operating arrangements must be submitted to the participating governments before they can take effect.'
    localised['COLDWAR_KOR_foreign.700.option_a']='Authorize Fresh Negotiations'
    out.append('country_event = { id = COLDWAR_KOR_foreign.700 is_triggered_only = yes title = COLDWAR_KOR_foreign.700.t desc = COLDWAR_KOR_foreign.700.d option = { name = COLDWAR_KOR_foreign.700.option_a } }')
    return "\n".join(out) + "\n"


def _modifiers(contracts, localised):
    out = [SCRIPT_COMMENT]
    for c in contracts:
        entries = ([*(('kor', tag) for tag in c['tags']), *(('partner', tag) for tag in c['tags'])] if c["key"] == "nordpolitik_recognition" else [("kor", None)] + ([("partner", tag) for tag in c["tags"]] if c["key"] in SELECTABLE_KEYS else [("partner", None)]))
        for side, partner_tag in entries:
            mods = _policy(c, side)
            if not mods:
                continue
            name = _modifier_name(c, side, partner_tag)
            suffix = f" ({partner_tag})" if partner_tag else ""
            localised[name] = f"Korean Agreement: {c['key'].replace('_', ' ').title()}{suffix}"
            active = _agreement_active(c, side, partner_tag)
            out += [f"{name} = {{", "\ticon = GFX_idea_economic_increase", f"\tenable = {{ {active} }}"]
            out.extend(f"\t{k} = {_q(v)}" for k, v in mods.items())
            out.append("}")
    return "\n".join(out) + "\n"


def _repeat_decisions(contracts, data, localised):
    """Free retry actions unlocked only by an already paid focus receipt."""
    owners = {}
    for node in data.get("nodes", []):
        for action in node.get("effects", {}).get("actions", []):
            if action.get("type") == "offer":
                owners.setdefault(action["value"], set()).add(node.get("key", ""))
    out = [SCRIPT_COMMENT]
    localised["COLDWAR_KOR_1970_foreign_category"] = "Bilateral Agreement Proposals"
    localised["COLDWAR_KOR_1970_foreign_category_desc"] = "Reopen an approved diplomatic proposal after a refusal or expiry. Sending the offer costs nothing; payment begins only after the counterpart signs."
    for c in contracts:
        key = c["key"]
        focus_keys = sorted(owners.get(key, ()))
        # Some approved contracts share a focus with alternate diplomatic routes.
        if not focus_keys:
            continue
        condition = "OR = { " + " ".join(f"has_country_flag = COLDWAR_KOR_{fk}_paid" for fk in focus_keys) + " }"
        decision_id = f"COLDWAR_KOR_repeat_{key}"
        out += [decision_id + " = {", "\ticon = GFX_decision_relation", "\tcost = 0", f"\tvisible = {{ {condition} }}", f"\tavailable = {{ COLDWAR_KOR_can_send_{key} = yes }}", "\tcomplete_effect = {", f"\t\tCOLDWAR_KOR_send_{key} = yes", "\t}", "\tai_will_do = { factor = 0 }", "}"]
        localised[decision_id] = f"Renew proposal: {key.replace('_', ' ').title()}"
        localised[decision_id + "_desc"] = "Send the proposal for a new response. No payment or agreement effect applies unless the counterpart accepts."
    return SCRIPT_COMMENT + "\nCOLDWAR_KOR_1970_foreign_category = {\n" + "\n".join("\t" + line for line in out[1:]) + "\n}\n"


def _preview_ideas(contracts,loc):
    out=[SCRIPT_COMMENT,'ideas = { country = {']
    loc['COLDWAR_KOR_usfk_member']='Korean-American Defence Cooperation'
    loc['COLDWAR_KOR_usfk_member_desc']='The two governments have ratified a framework for defence consultation, agreed training and the responsibilities of the American presence.'
    out += ['COLDWAR_KOR_usfk_member = { picture = COLDWAR_KOR_spirit_army allowed = { always = yes } removal_cost = -1 modifier = { } }']
    for c in contracts:
        for side in ('kor','partner'):
            mods=_policy(c,side)
            if not mods:continue
            id=f'COLDWAR_KOR_agreement_{c["key"]}_{side}_preview'
            loc[id]=AGREEMENTS[c['key']]
            loc[id+'_desc']='The ratified agreement defines the participating governments’ cooperation and commitments.'
            out.append(id+' = { picture = COLDWAR_KOR_spirit_diplomacy allowed = { always = yes } removal_cost = -1 modifier = { '+' '.join(k+' = '+_q(v) for k,v in mods.items())+' } }')
    return '\n'.join(out+['} }'])+'\n'


def _usfk_effects():
    return SCRIPT_COMMENT+'''\n
COLDWAR_KOR_ratify_us_garrison = {
 KOR = {
  add_ideas = COLDWAR_KOR_usfk_member
  if = { limit = { NOT = { USA = { has_military_access_to = KOR } } }
   give_military_access = USA
   set_country_flag = COLDWAR_KOR_usfk_access_granted
  }
 }
 USA = { add_ideas = COLDWAR_KOR_usfk_member }
}
COLDWAR_KOR_end_us_garrison = {
 KOR = {
  clr_country_flag = COLDWAR_KOR_us_garrison_signed
  remove_dynamic_modifier = { modifier = COLDWAR_KOR_1970_foreign_us_garrison_kor }
  if = { limit = { has_country_flag = COLDWAR_KOR_usfk_access_granted }
   USA = { diplomatic_relation = { country = KOR relation = military_access active = no } }
   clr_country_flag = COLDWAR_KOR_usfk_access_granted
  }
 }
 USA = { clr_country_flag = COLDWAR_KOR_us_garrison_signed remove_dynamic_modifier = { modifier = COLDWAR_KOR_1970_foreign_us_garrison_partner } }
}
COLDWAR_KOR_ratify_us_drawdown = {
 COLDWAR_KOR_usfk_exercise_abort = yes
 COLDWAR_KOR_end_us_garrison = yes
 KOR = { add_ideas = COLDWAR_KOR_usfk_member }
 USA = { add_ideas = COLDWAR_KOR_usfk_member }
}
COLDWAR_KOR_usfk_reconcile = {
 if = { limit = { KOR = { has_country_flag = COLDWAR_KOR_usfk_access_granted NOT = { has_country_flag = COLDWAR_KOR_us_garrison_signed } } }
  COLDWAR_KOR_end_us_garrison = yes
 }
 if = { limit = { OR = { KOR = { has_idea = COLDWAR_KOR_usfk_member } USA = { has_idea = COLDWAR_KOR_usfk_member } }
    NOT = { COLDWAR_KOR_usfk_cooperation_live = yes } }
  KOR = { remove_ideas = COLDWAR_KOR_usfk_member }
  USA = { remove_ideas = COLDWAR_KOR_usfk_member }
 }
}
'''

def _upgrade_terms(contracts):
    lines=[SCRIPT_COMMENT,'COLDWAR_KOR_upgrade_agreement_terms = {','if = { limit = { tag = KOR IMP_is_1970_scenario = yes NOT = { has_country_flag = COLDWAR_KOR_terms_review_complete } }','set_country_flag = COLDWAR_KOR_terms_review_complete']
    for c in contracts:
        if not c.get('revised_terms'):continue
        key=c['key'];sig=c['signed'];pending=c['pending'];terms=f'COLDWAR_KOR_{key}_terms_v3';offer=f'COLDWAR_KOR_{key}_offer_v3'
        lines.append(f'if = {{ limit = {{ OR = {{ AND = {{ has_country_flag = {sig} NOT = {{ has_country_flag = {terms} }} }} AND = {{ has_country_flag = {pending} NOT = {{ has_country_flag = {offer} }} }} }} }} set_country_flag = COLDWAR_KOR_terms_need_review')
        if key=='working_contacts':
            lines.append(f'if = {{ limit = {{ has_country_flag = {sig} NKO = {{ has_country_flag = {sig} }} }} set_country_flag = COLDWAR_KOR_legacy_working_contacts NKO = {{ set_country_flag = COLDWAR_KOR_legacy_working_contacts }} }}')
        for tag in ['KOR']+c['tags']:
            cleanup=f'clr_country_flag = {sig} clr_country_flag = {pending} clr_country_flag = COLDWAR_KOR_{key}_offer_open'
            cleanup+=' '+' '.join(f'clr_country_flag = COLDWAR_KOR_{key}_assent_{t} clr_country_flag = COLDWAR_KOR_{key}_target_{t}' for t in c['tags'])
            lines.append(tag+' = { '+cleanup+' }')
        lines.append('}')
    lines+=['if = { limit = { has_country_flag = COLDWAR_KOR_terms_need_review } clr_country_flag = COLDWAR_KOR_terms_need_review country_event = { id = COLDWAR_KOR_foreign.700 } }','}','}']
    return '\n'.join(lines)+'\n'


def build(data):
    """Return (repo-relative script files, English localization key/text)."""
    contracts = []
    next_e = 1
    for original in data.get("contracts", []):
        c = dict(original)
        key = c["key"]
        tags = _tag_list(c)
        if key == "nordpolitik_recognition":
            # This contract intentionally becomes two independent transactions.
            c["tags"] = ["SOV", "CHI"]
        elif key == "neutrality_guarantees":
            c["tags"] = ["USA", "NKO", "SOV", "CHI"]
        elif key == "vietnam_withdrawal_settlement":
            c["tags"] = ["SVN", "USA"]
        elif key in {"technology_licence", "security_partner_contacts"}:
            c["tags"] = ["JAP", "USA"]
        elif key == "alternative_finance_contacts":
            c["tags"] = ["USA", "GER"]
        elif key == 'gulf_project_access':
            c['tags']=['SAU','IRQ']
        else:
            c["tags"] = tags
        c["event_index"] = next_e
        c["reply_index"] = 100 + next_e
        c["expiry_index"] = 200 + next_e
        c['refusal_index']=400+next_e
        c['notice_index']=500+next_e
        c["selector_index"] = 300 + next_e if key in SELECTABLE_KEYS else None
        next_e += 1
        c["pending"] = f"COLDWAR_KOR_{key}_pending"
        c["signed"] = f"COLDWAR_KOR_{key}_signed"
        contracts.append(c)

    loc = {}
    files = {
        "common/scripted_effects/COLDWAR_KOR_1970_foreign.txt": _scripted_effects(contracts),
        "common/scripted_triggers/COLDWAR_KOR_1970_foreign.txt": _scripted_triggers(contracts),
        "events/COLDWAR_KOR_1970_foreign.txt": _events(contracts, loc),
        "common/dynamic_modifiers/COLDWAR_KOR_1970_foreign.txt": _modifiers(contracts, loc),
        'common/ideas/COLDWAR_KOR_1970_foreign_previews.txt': _preview_ideas(contracts,loc),
        'common/scripted_effects/COLDWAR_KOR_1970_usfk_agreements.txt': _usfk_effects(),
        'common/scripted_effects/COLDWAR_KOR_1970_terms_review.txt': _upgrade_terms(contracts),
        "common/decisions/COLDWAR_KOR_1970_foreign.txt": _repeat_decisions(contracts, data, loc),
        "common/decisions/categories/COLDWAR_KOR_1970_foreign.txt": "\n".join([SCRIPT_COMMENT, "COLDWAR_KOR_1970_foreign_category = {", "\ticon = GFX_decision_category_generic_foreign_policy", "\tallowed = { always = yes }", "\tvisible = { tag = KOR IMP_is_1970_scenario = yes is_subject = no }", "}"]) + "\n",
    }
    return files, loc
