# IMPERIA CW — Cold War: approved Spanish development and diplomatic transactions.
"""Emit isolated V2 agreements; no shared MD files are changed.

Native API evidence and the approved EC integration adaptation are recorded in
agreements_native_contracts.md. The root compiler calls build(root, design).
"""
from __future__ import annotations
import json
from pathlib import Path

HEADER = '# IMPERIA CW — Cold War: Spain V2 development and negotiated agreements.\n'
P = 'COLDWAR_SPR_'


def money(amount):
    return f'set_temp_variable = {{ treasury_change = {amount:g} }}\nmodify_treasury_effect = yes'


def funds(amount):
    return f'check_variable = {{ var = treasury value = {amount:g} compare = greater_than_or_equals }}'


def unlock(slug):
    return P + 'unlock_' + slug


def applied(slug):
    return f'has_country_flag = {P}applied_{slug}'


def build(root, design):
    root = Path(root)
    effects, triggers, decisions, events, ideas = [], [], [], ['add_namespace = COLDWAR_SPR_v2_agreements'], []
    loc, previews = {}, {}
    sources = {}
    for node in design['nodes']:
        if node['group'] in ('development', 'military', 'foreign'):
            for effect in node['effects']:
                if effect['type'] == 'decision':
                    sources[effect['id'].removeprefix(P)] = node

    def L(key, value):
        loc[key] = value
        return key

    def E(name, body):
        effects.append(f'{name} = {{\n{body}\n}}')

    def T(name, body):
        triggers.append(f'{name} = {{\n{body}\n}}')

    def D(name, body):
        decisions.append(f'{name} = {{\nicon = obtain_foreign_investment\ncost = 0\n{body}\nai_will_do = {{ factor = 1 }}\n}}')

    def I(name, title, mods, description=''):
        ideas.append(f'{name} = {{ picture = generic_economy allowed = {{ always = no }} removal_cost = -1 modifier = {{ {mods} }} }}')
        L(name, title)
        L(name + '_desc', description)

    def preview(slug, code):
        key = P + slug + '_terms'
        previews[P + slug] = code
        return key

    # Effects called by completion rewards do not transact on behalf of recipients.
    for slug, node in sources.items():
        if slug in ('energy_crisis_protocol','industrial_adjustment','equipment_licensing'):
            tooltip = P+('licensing_tt' if slug == 'equipment_licensing' else slug+'_tt')
            E(P + slug + '_effect', f'custom_effect_tooltip = {tooltip}\nhidden_effect = {{ set_country_flag = {unlock(slug)} }}')
        else:
            E(P + slug + '_effect', f'unlock_decision_tooltip = {P}{slug}\nhidden_effect = {{ set_country_flag = {unlock(slug)} }}')
        L(P + slug, node['title'])
        L(P + slug + '_desc', node['description'])

    T(P + 'has_operating_nuclear_generation', '''custom_trigger_tooltip = {
tooltip = COLDWAR_SPR_operating_generation_tt
check_variable = { nuclear_energy_generation > 0 }
NOT = { has_country_flag = disable_nuclear_power_plant_flag }
NOT = { has_idea = non_nuclear_power }
any_owned_state = { is_controlled_by = ROOT nuclear_reactor > 0 }
}''')
    L(P + 'operating_generation_tt', 'An owned and controlled nuclear reactor is producing electricity.')
    L(P + 'agreements_category', 'Spanish Development and Agreements')
    L(P + 'agreements_category_desc', 'Fund national projects and negotiate commercial, defence and constitutional agreements with the governments concerned.')

    # The native investment API computes the live price and duration at the selected
    # site. The actual project runs through MD's project decisions and completion.
    spanish_states = '86 87 88 89 90 91 92 93 94 95 96 97 98 944 968 1040 1041 1042'
    investment = {
        'nuclear_investment': (13, 'nuclear_reactor', 'has_tech = reactor1 country_can_build_nuclear_reactors = yes', 14.4),
        'conventional_investment': (12, 'fossil_powerplant', '', 5.2),
        'uranium_investment': (15, 'uranium_mine', '', 6),
    }
    L(P + 'native_project_terms', 'Prepare one paid investment project. Confirm the current price and construction period before committing funds.')
    L(P + 'project_confirm', 'Authorise the investment')
    L(P + 'project_cancel', 'Defer construction')
    for index, (slug, (kind, building, gate, price)) in enumerate(investment.items(), 1):
        extra = 'imp_uranium_investment_one_level_available = yes' if kind == 15 else f'free_building_slots = {{ building = {building} size > 0 include_locked = no }}'
        eligible = f'is_owned_by = SPR is_controlled_by = SPR NOT = {{ is_in_array = {{ projects_in_state = SPR.id }} }} {extra}'
        T(P + slug + '_site_valid', eligible)
        # State scope PREV is restored deliberately, as required by update_gui.
        prepare = f'''set_variable = {{ project_building_type^-1 = {kind} }}
set_variable = {{ project_build_amount^-1 = 1 }}
set_variable = {{ investments_state_target = FROM.id }}
set_variable = {{ investments_nation_target = SPR.id }}
FROM = {{ SPR = {{ update_gui = yes }} }}
set_variable = {{ {P}v2_project_quote = project_monetary_cost^-1 }}
set_variable = {{ {P}v2_project_quoted_days = project_total_construction_duration_display^-1 }}
country_event = {{ id = COLDWAR_SPR_v2_agreements.{index} }}'''
        D(P + slug, f'''state_target = yes
on_map_mode = map_and_decisions_view
targets = {{ {('90' if kind == 15 else spanish_states)} }}
visible = {{ has_country_flag = {unlock(slug)} }}
target_trigger = {{ FROM = {{ {P}{slug}_site_valid = yes }} }}
available = {{ {applied(sources[slug]['id'].removeprefix(P))} {gate}
NOT = {{ has_active_mission = bankruptcy_incoming_collapse }}
NOT = {{ has_active_mission = cheap_loan_from_the_imf_mission }}
NOT = {{ has_country_flag = {P}project_confirmation_pending }} }}
complete_effect = {{ hidden_effect = {{ set_country_flag = {{ flag = {P}project_confirmation_pending days = 1 }} {prepare} }} custom_effect_tooltip = {P}native_project_terms }}''')
        valid = f'''tag = SPR IMP_is_1970_scenario = yes has_country_flag = {unlock(slug)} {applied(sources[slug]['id'].removeprefix(P))} {gate}
has_country_flag = {P}project_confirmation_pending
check_variable = {{ project_building_type^-1 = {kind} }}
check_variable = {{ project_build_amount^-1 = 1 }}
any_state = {{ state = SPR.investments_state_target {P}{slug}_site_valid = yes }}
has_available_treasury_investment = yes
NOT = {{ has_active_mission = bankruptcy_incoming_collapse }}
NOT = {{ has_active_mission = cheap_loan_from_the_imf_mission }}
check_variable = {{ active_projects < 15 }}'''
        T(P + slug + '_can_confirm', valid)
        # Recompute live costs before charging; confirmation cannot freeze obsolete
        # modifiers. Native project allocation precedes its debit.
        confirm = f'''if = {{ limit = {{ {P}{slug}_can_confirm = yes }}
random_state = {{ limit = {{ state = SPR.investments_state_target }} SPR = {{ update_gui = yes }} }}
if = {{ limit = {{ {P}{slug}_can_confirm = yes check_variable = {{ project_monetary_cost^-1 = {P}v2_project_quote }} check_variable = {{ project_total_construction_duration_display^-1 = {P}v2_project_quoted_days }} }} start_project_two = yes }}
else = {{ country_event = {{ id = COLDWAR_SPR_v2_agreements.1003 hours = 1 }} }}
}}
clr_country_flag = {P}project_confirmation_pending'''
        E(P + slug + '_confirm', confirm)
        events.append(f'''country_event = {{ id = COLDWAR_SPR_v2_agreements.{index}
title = {P}project_{kind}_title desc = {P}project_{kind}_desc picture = GFX_report_event_generic_economic_reform is_triggered_only = yes
option = {{ name = {P}project_confirm trigger = {{ {P}{slug}_can_confirm = yes }} custom_effect_tooltip = {P}project_price_tt hidden_effect = {{ {P}{slug}_confirm = yes }} }}
option = {{ name = {P}project_cancel clr_country_flag = {P}project_confirmation_pending }}
}}''')
        L(P + f'project_{kind}_title', {'nuclear_reactor':'A Reactor Investment','fossil_powerplant':'Conventional Generating Capacity','uranium_mine':'Develop the Salamanca Deposits'}[building])
        L(P + f'project_{kind}_desc', 'The ministry has prepared a site-specific proposal. The price reflects the current investment terms; construction will follow the normal project timetable.')
        preview(slug, f'custom_effect_tooltip = {P}native_project_terms')
    L(P + 'project_price_tt', 'Treasury: §R-$[?project_monetary_cost^-1|2] billion§!\nConstruction period: §Y[?project_total_construction_duration_display^-1|0] days§!\nOne paid project; normal energy, employment and fuel requirements apply.')

    # Energy accounts is a usable project entry rather than a permanent fake bonus.
    D(P + 'energy_accounts', f'''visible = {{ has_country_flag = {unlock('energy_accounts')} }}
available = {{ {applied('energy_balance')} }}
complete_effect = {{ country_event = {{ id = COLDWAR_SPR_v2_agreements.10 }} }}''')
    events.append(f'''country_event = {{ id = COLDWAR_SPR_v2_agreements.10 title = {P}energy_accounts desc = {P}energy_accounts_report picture = GFX_report_event_generic_economic_reform is_triggered_only = yes
option = {{ name = {P}review_accounts custom_effect_tooltip = {P}energy_accounts_values }} }}''')
    L(P + 'energy_accounts_report', 'The energy ministry reports current electricity output and fuel needs. New generating capacity must be funded and supplied throughout its operation.')
    L(P + 'review_accounts', 'Review the national balance')
    L(P + 'energy_accounts_values', 'Electricity balance: §Y[?energy_balance|2]§!\nNuclear generation: §Y[?nuclear_energy_generation|2]§!\nReactor fuel consumption: §Y[?nuclear_fuel_consumption|2] per week§!')
    preview('energy_accounts', f'custom_effect_tooltip = {P}native_project_terms')

    # Survey only: the existing 1970 deposit system already identifies Salamanca.
    # Reassert deposit capacity, never production or a finished mine.
    survey = f'''if = {{ limit = {{ 90 = {{ is_owned_by = SPR is_controlled_by = SPR }} NOT = {{ has_country_flag = {P}v2_survey_complete }} }}
90 = {{ imp_uranium_add_deposit = yes set_variable = {{ imp_uranium_mine_slots = 2 }} set_variable = {{ imp_uranium_per_level = 4 }} imp_uranium_sync_mine_slots = yes }}
set_country_flag = {P}v2_survey_complete }}'''
    effects = [e if not e.startswith(P+'uranium_investment_effect =') else e[:-1] + '\nhidden_effect = { ' + survey + ' }\n}' for e in effects]

    # Crisis observers apply shocks at their historical windows, never at startup.
    I(P + 'v2_oil_shock', 'Energy Supply Adjustment', 'civilian_factories_productivity = -0.10 offices_productivity = -0.05', 'Imported-energy disruption is forcing firms to adjust production and services.')
    I(P + 'v2_industrial_shock', 'Industrial Adjustment', 'civilian_factories_productivity = -0.10 social_cost_multiplier_modifier = 0.10', 'Industrial reconversion is reducing output while displaced workers require support.')
    I(P + 'v2_funded_adjustment', 'Funded Industrial Adjustment', 'civilian_factories_productivity = -0.05 social_cost_multiplier_modifier = 0.10', 'The reconversion fund cushions the productivity loss while maintaining support for displaced workers.')
    T(P + 'reserve_facility_owned', 'any_owned_state = { is_controlled_by = ROOT fuel_silo > 0 }')
    for slug in ('energy_crisis_protocol', 'industrial_adjustment'):
        preview(slug, f'custom_effect_tooltip = {P}{slug}_tt')
    L(P + 'energy_crisis_protocol_tt', 'Later supply adjustment: civilian productivity §R-10%§! and office productivity §R-5%§! for §Y90 days§! instead of §Y180§!, while an owned reserve facility remains operational. The 1973 shock is unaffected.')
    L(P + 'industrial_adjustment_tt', '1980s industrial adjustment: civilian productivity §R-5%§! instead of §R-10%§! for §Y365 days§!. Social expenditure remains §R+10%§!.')

    # Conscription uses each real law's native conditions and price, copied from the
    # current provider at build time so doctrine/institution restrictions survive.
    military = (root / 'common/ideas/AA_law_military_ideas.txt').read_text(encoding='utf-8-sig')
    def block(text, label):
        import re
        match = re.search(r'\b'+re.escape(label)+r'\s*=\s*\{', text)
        if not match:
            raise ValueError(label)
        pos, depth = match.end(), 1
        begin = pos
        while depth:
            if text[pos] == '{': depth += 1
            elif text[pos] == '}': depth -= 1
            pos += 1
        return text[begin:pos-1]
    law_steps = [('no_military','volunteer_army'), ('volunteer_army','partial_draft_army'), ('partial_draft_army','draft_army')]
    alternatives = []
    for before, after in law_steps:
        law_available = block(block(military, after), 'available')
        alternatives.append(f'AND = {{ has_idea = {before} {law_available} }}')
    T(P + 'reserve_law_available', 'OR = {\n'+'\n'.join(alternatives)+'\n}')
    D(P + 'reserve_law', f'''visible = {{ has_country_flag = {unlock('reserve_law')} NOT = {{ has_country_flag = {P}v2_reserve_law_used }} }}
available = {{ {P}reserve_law_available = yes }}
custom_cost_trigger = {{ has_political_power > 149 }} custom_cost_text = {P}law_cost
complete_effect = {{ if = {{ limit = {{ {P}reserve_law_available = yes has_political_power > 149 }} add_political_power = -150 increase_conscription_effect = yes set_country_flag = {P}v2_reserve_law_used }} }}''')
    L(P + 'law_cost', '£pol_power  §Y150§!')
    L(P + 'reserve_law_tt', 'Permit the next conscription law at its normal §Y150 Political Power§! cost and legal requirements. Enactment remains optional.')
    preview('reserve_law', f'custom_effect_tooltip = {P}reserve_law_tt')
    L(P + 'licensing_report', 'The procurement service can arrange production of foreign designs through bilateral contracts. The exporter determines which equipment it is willing to license, and the agreement retains its normal industrial cost.')
    L(P + 'licensing_option', 'Prepare a bilateral procurement request')
    L(P + 'licensing_tt', 'Use §YDiplomacy → Request Licence Production§! to select the exporter and equipment. The exporter must accept; normal civilian-industry licence costs apply.')
    preview('equipment_licensing', f'custom_effect_tooltip = {P}licensing_tt')

    # Each target owns the answer. All fixed terms are transacted only in the
    # acceptance option, after both countries, funds and current eligibility pass.
    agreements = {
        'us_bases_offer': dict(targets=['USA'], title='The Spanish Facilities Agreement', desc='Madrid proposes a temporary facilities agreement. The terms provide a single payment in return for agreed military access.', payer=1.5, mode='access'),
        'limited_access': dict(targets=['USA'], title='Restricted Spanish Facilities', desc='Madrid proposes a limited, temporary access arrangement without a facilities payment.', mode='access'),
        'bilateral_training': dict(targets=['USA','ENG','FRA'], title='Joint Exercises with Spain', desc='The Spanish services propose a funded bilateral exercise to improve staff coordination.', both=.3, mode='training'),
        'mediterranean_offer': dict(targets=['ITA','FRA','POR'], title='Mediterranean Commercial Cooperation', desc='Spain proposes reciprocal commercial services and a joint contribution to their development.', both=.5, mode='commerce'),
        'european_trade_offer': dict(targets=['FRA','GER','ITA','BEL','HOL','LUX'], title='Spanish Trade Negotiations', desc='Spain requests a regular trade-adjustment channel with the Communities. The arrangement confers no membership or financial obligation.', mode='trade'),
        'eec_application': dict(targets=['FRA','GER','ITA','BEL','HOL','LUX','ENG','IRE','DEN','GRE','POR'], title='Spain and the European Communities', desc='Spain requests assent to its candidacy. Legal adjustment and the normal Community admission requirements remain necessary.', mode='eec'),
        'sahara_conference': dict(targets=['MOR','MAU','ALG','SHA'], title='A Conference on the Sahara', desc='Spain invites the interested governments to a conference on Saharan self-determination and the future administration of the territory.', mode='conference'),
        'sahara_transition_offer': dict(targets=['MOR','MAU','ALG','SHA'], title='A Supervised Saharan Transition', desc='Spain proposes an agreed transition to Saharan self-government. A final settlement will require the participating governments to confirm their assent.', mode='transition'),
        'sahara_presence_offer': dict(targets=['MOR','MAU','ALG','SHA'], title='An Interim Saharan Administration', desc='Spain proposes a temporary continuation of its existing administration, subject to a review after 720 days.', mode='presence'),
        'maghreb_commerce': dict(targets=['MOR','ALG','TUN','MAU'], title='Maghreb Commercial Cooperation', desc='Spain proposes reciprocal commercial services with a funded contribution from both governments.', both=.5, mode='commerce'),
        'iberoamerican_credit': dict(targets=['ARG','BRA','CHL','BOL','COL','ECU','PAR','PRU','URG','VEN','MEX','CUB','DOM','GUA','HON','NIC','COS','PAN','ELS'], title='Spanish Development Credit', desc='Madrid offers a development bond at face value. The borrower receives the principal and accepts a matching obligation to Spain.', lender=2, mode='loan'),
    }
    L(P + 'accept', 'Accept the proposed terms')
    L(P + 'refuse', 'Decline the proposal')
    L(P + 'lapsed', 'The proposal can no longer be concluded')
    L(P + 'proposal_sent', 'Submit these terms for the recipient government’s approval. The offer remains open for §Y90 days§!.')
    I(P + 'v2_commercial_project', 'Spanish Commercial Cooperation', 'offices_productivity = 0.05', 'A funded commercial-services agreement supports offices for the duration of the project.')
    I(P + 'v2_sahara_interim', 'Interim Saharan Administration', '', 'Participating governments have accepted an interim Spanish administration, subject to review after 720 days.')
    refresh = []
    for number, (slug, terms) in enumerate(agreements.items(), 100):
        mode = terms['mode']
        focus = sources[slug]['id'].removeprefix(P)
        stem = P + 'v2_' + slug
        target_gate = 'has_idea = EU_member' if mode in ('eec','trade') else 'OR = { ' + ' '.join('tag = '+tag for tag in terms['targets'])+' }'
        sender_gate = f'tag = SPR IMP_is_1970_scenario = yes is_subject = no {applied(focus)} has_country_flag = {unlock(slug)}'
        if mode == 'eec': sender_gate += f' has_government = democratic has_elections = yes has_country_flag = {P}v2_ec_legal_ready NOT = {{ has_idea = EU_member }}'
        if mode in ('transition','presence'):
            sender_gate += f' {P}v2_sahara_conference_all_consented = yes'
        if mode in ('training','loan','access'):
            sender_gate += f' NOT = {{ has_country_flag = {stem}_concluded }}'
        own_gate = funds(terms['both']) if 'both' in terms else (funds(terms['lender']) if 'lender' in terms else '')
        rec_gate = funds(terms.get('both',terms.get('payer',0))) if 'both' in terms or 'payer' in terms else ''
        T(stem + '_sender_live', sender_gate + '\n' + own_gate)
        T(stem + '_accept_live', f'''exists = yes {target_gate} NOT = {{ has_war_with = SPR }} {rec_gate}
SPR = {{ exists = yes {stem}_sender_live = yes has_country_flag = {stem}_pending@ROOT NOT = {{ has_country_flag = {stem}_accepted@ROOT }} }}''')
        send = f'''if = {{ limit = {{ {stem}_sender_live = yes FROM = {{ exists = yes {target_gate} NOT = {{ has_war_with = SPR }} }} NOT = {{ has_country_flag = {stem}_pending@FROM }} NOT = {{ has_country_flag = {stem}_accepted@FROM }} }}
set_country_flag = {{ flag = {stem}_pending@FROM days = 90 }}
set_country_flag = {stem}_awaiting@FROM
FROM = {{ country_event = {{ id = COLDWAR_SPR_v2_agreements.{number} hours = 1 }} }} }}'''
        E(stem + '_send', send)
        D(P + slug, f'''{'target_array = global.EU_member' if mode in ('eec','trade') else 'targets = { '+ ' '.join(terms['targets'])+' }'}
visible = {{ has_country_flag = {unlock(slug)} }}
target_trigger = {{ FROM = {{ exists = yes {target_gate} NOT = {{ has_war_with = SPR }} }} NOT = {{ has_country_flag = {stem}_accepted@FROM }} }}
available = {{ {stem}_sender_live = yes NOT = {{ has_country_flag = {stem}_pending@FROM }} }}
complete_effect = {{ custom_effect_tooltip = {P}proposal_sent hidden_effect = {{ {stem}_send = yes }} }}''')
        result = [f'hidden_effect = {{ SPR = {{ set_country_flag = {stem}_accepted@ROOT clr_country_flag = {stem}_pending@ROOT clr_country_flag = {stem}_awaiting@ROOT }} }}']
        preview_code = ''
        if 'both' in terms:
            result += [money(terms['both']*-1), 'SPR = { '+money(terms['both']*-1)+' }']
        if mode == 'access':
            if 'payer' in terms:
                result += [money(-terms['payer']), 'SPR = { '+money(terms['payer'])+' }']
            result += [f'''if = {{ limit = {{ NOT = {{ has_military_access_to = SPR }} }}
diplomatic_relation = {{ country = SPR relation = military_access active = yes }}
SPR = {{ set_country_flag = {stem}_created_access }} }}
SPR = {{ set_country_flag = {stem}_concluded set_country_flag = {{ flag = {stem}_access_live days = 720 }} }}''']
            L(stem+'_tt', ('US Treasury: §R-$1.50 billion§!\nSpanish Treasury: §G+$1.50 billion§!\n' if 'payer' in terms else '')+'United States receives military access to Spain for §Y720 days§!, subject to continued peace. The agreement creates no alliance.')
        elif mode == 'training':
            result += ['army_experience = 20 air_experience = 10', f'SPR = {{ army_experience = 20 air_experience = 10 set_country_flag = {stem}_concluded }}']
            L(stem+'_tt', 'Each government: Treasury §R-$0.30 billion§!, §G+20 Army Experience§! and §G+10 Air Experience§!.')
        elif mode == 'commerce':
            result += [f'add_timed_idea = {{ idea = {P}v2_commercial_project days = 720 }}', f'SPR = {{ add_timed_idea = {{ idea = {P}v2_commercial_project days = 720 }} }}']
            L(stem+'_tt', 'Each government: Treasury §R-$0.50 billion§!; office productivity §G+5%§! for §Y720 days§!. Concurrent agreements do not stack the productivity bonus.')
        elif mode == 'loan':
            result += [money(2), 'SPR = { '+money(-2)+f' add_to_variable = {{ given_bonds@ROOT = 2 }} calculate_new_bonds_held = yes set_country_flag = {stem}_concluded }}', 'calculate_new_bonds_owed = yes']
            L(stem+'_tt', 'Spanish Treasury: §R-$2.00 billion§!\nBorrower Treasury: §G+$2.00 billion§!\nBond obligation to Spain: §Y$2.00 billion§! at face value. Repayment uses the normal bilateral bond settlement.')
        elif mode == 'eec':
            result += [f'SPR = {{ {P}v2_ec_update_candidate = yes }}']
            L(stem+'_tt', 'Recognise Spain’s candidacy. Every current Community member must assent before Spain receives candidate status. Admission retains the normal §Y50 Political Power§!, Europeanism, peace and legal requirements.')
        elif mode == 'presence':
            result += [f'SPR = {{ {P}v2_sahara_update = yes }}']
            L(stem+'_tt', 'Approve an interim administration of the territory Spain currently owns for §Y720 days§!. All conference participants must accept; no territorial transfer or new core is granted.')
        elif mode == 'transition':
            L(stem+'_tt', 'Accept a Saharan transition protocol and a non-aggression agreement with Spain. Finalisation requires every existing conference participant’s assent. Any territorial handover remains a separate agreement by the current owner.')
        elif mode == 'conference':
            L(stem+'_tt', 'Join the Saharan conference. Participation grants no territory, claim, core, military access or financial payment.')
        else:
            L(stem+'_tt', 'Establish a bilateral trade-adjustment channel. No membership, subsidy or compulsory market access is granted.')
        E(stem + '_accept', f'if = {{ limit = {{ hidden_trigger = {{ {stem}_accept_live = yes }} }}\n'+'\n'.join(result)+'\n}')
        events.append(f'''country_event = {{ id = COLDWAR_SPR_v2_agreements.{number} title = {stem}_title desc = {stem}_desc picture = GFX_report_event_generic_diplomacy is_triggered_only = yes
option = {{ name = {P}accept trigger = {{ {stem}_accept_live = yes }} custom_effect_tooltip = {stem}_tt {stem}_accept = yes }}
option = {{ name = {P}refuse trigger = {{ SPR = {{ has_country_flag = {stem}_pending@ROOT }} }} SPR = {{ clr_country_flag = {stem}_pending@ROOT clr_country_flag = {stem}_awaiting@ROOT country_event = {{ id = COLDWAR_SPR_v2_agreements.1001 hours = 1 }} }} }}
option = {{ name = {P}lapsed trigger = {{ NOT = {{ {stem}_accept_live = yes }} }} SPR = {{ clr_country_flag = {stem}_pending@ROOT clr_country_flag = {stem}_awaiting@ROOT }} }}
}}''')
        L(stem+'_title',terms['title']); L(stem+'_desc',terms['desc'])
        prospective = f'custom_effect_tooltip = {stem}_tt'
        if 'both' in terms:
            partner = terms['targets'][0]
            native = money(-terms['both'])
            if mode == 'training': native += '\narmy_experience = 20 air_experience = 10'
            if mode == 'commerce': native += f'\nadd_timed_idea = {{ idea = {P}v2_commercial_project days = 720 }}'
            prospective = native + f'\n{partner} = {{ {native} }}\n' + prospective
        elif 'payer' in terms:
            prospective = money(terms['payer']) + '\nUSA = { '+money(-terms['payer'])+' }\n' + prospective
        elif mode == 'loan':
            prospective = money(-2)+'\nARG = { '+money(2)+' }\n'+prospective
        preview(slug, prospective)
        refresh.append(f'''every_other_country = {{ limit = {{ SPR = {{ has_country_flag = {stem}_awaiting@PREV NOT = {{ has_country_flag = {stem}_pending@PREV }} }} }}
SPR = {{ clr_country_flag = {stem}_awaiting@PREV country_event = {{ id = COLDWAR_SPR_v2_agreements.1002 hours = 1 }} }} }}''')
        if mode == 'access':
            refresh.append(f'''if = {{ limit = {{ has_country_flag = {stem}_created_access OR = {{ NOT = {{ has_country_flag = {stem}_access_live }} has_war_with = USA NOT = {{ USA = {{ exists = yes }} }} }} }}
if = {{ limit = {{ NOT = {{ has_idea = NATO_member }} }} USA = {{ diplomatic_relation = {{ country = SPR relation = military_access active = no }} }} }}
clr_country_flag = {stem}_created_access }}''')

    # No nationality, agenda or global EU activation is invented: native candidate
    # state and the existing EU_apply_for_membership perform the real admission.
    E(P+'v2_ec_update_candidate', f'''if = {{ limit = {{ tag = SPR has_country_flag = {P}v2_ec_legal_ready has_government = democratic has_elections = yes
any_other_country = {{ has_idea = EU_member }}
NOT = {{ any_other_country = {{ has_idea = EU_member OR = {{ has_war_with = SPR NOT = {{ SPR = {{ has_country_flag = {P}v2_eec_application_accepted@PREV }} }} }} }} }} }}
set_country_flag = EU_candidate set_country_flag = {P}v2_ec_consent_complete set_eu_candidate_europeanism_floor = yes }}''')
    D(P+'v2_ec_legal_adjustment', f'''visible = {{ has_country_flag = {unlock('eec_application')} NOT = {{ has_country_flag = {P}v2_ec_legal_ready }} }}
available = {{ has_government = democratic has_elections = yes {applied('european_application')} }}
days_remove = 70 cancel_trigger = {{ OR = {{ NOT = {{ has_government = democratic }} NOT = {{ has_elections = yes }} }} }}
remove_effect = {{ if = {{ limit = {{ has_government = democratic has_elections = yes }} set_country_flag = {P}v2_ec_legal_ready {P}v2_ec_update_candidate = yes }} }}''')
    L(P+'v2_ec_legal_adjustment','Community Legal Adjustment')
    L(P+'v2_ec_legal_adjustment_desc','Parliament and the ministries must reconcile commercial law and administrative obligations before presenting a complete accession application.')
    # The membership receipt is provided by the root's approved-spirit compiler.
    refresh += [f'''{P}v2_ec_update_candidate = yes
if = {{ limit = {{ has_idea = EU_member has_country_flag = {P}v2_ec_consent_complete has_country_flag = {P}v2_ec_legal_ready NOT = {{ has_idea = {P}eec_membership }} }} add_ideas = {P}eec_membership }}
if = {{ limit = {{ has_idea = {P}eec_membership NOT = {{ has_idea = EU_member }} }} remove_ideas = {P}eec_membership }}''']
    # Native NATO.14 is owned by the alliance leader. Shared event guards use this
    # live transaction trigger for Spanish applicants only.
    T(P+'v2_nato_offer_live', f'''tag = SPR IMP_is_1970_scenario = yes
{applied('atlantic_application')} has_government = democratic has_elections = yes can_join_NATO = yes
has_country_flag = {P}v2_nato_pending NOT = {{ has_idea = NATO_member }}
any_other_country = {{ has_idea = NATO_member is_faction_leader = yes NOT = {{ has_war_with = SPR }} }}''')
    D(P+'nato_application', f'''visible = {{ has_country_flag = {unlock('nato_application')} NOT = {{ has_idea = NATO_member }} }}
available = {{ {applied('atlantic_application')} has_government = democratic has_elections = yes can_join_NATO = yes
any_other_country = {{ has_idea = NATO_member is_faction_leader = yes }} NOT = {{ has_country_flag = {P}v2_nato_retry }} }}
complete_effect = {{ if = {{ limit = {{ has_government = democratic has_elections = yes can_join_NATO = yes }} clr_country_flag = {P}v2_nato_leader_approved clear_variable = {P}v2_nato_sponsor set_country_flag = {{ flag = {P}v2_nato_pending days = 90 }} NATO_join_via_event = yes set_country_flag = {{ flag = {P}v2_nato_retry days = 90 }} }} }}''')
    L(P+'nato_application_tt','Request admission through the NATO member-led voting procedure. Actual admission requires alliance approval; no membership is granted by the application.')
    preview('nato_application',f'custom_effect_tooltip = {P}nato_application_tt')

    # The approved map may already be under another participant's administration.
    # Protocols therefore never require Spanish ownership or dispose of its land.
    parties = ['MOR','MAU','ALG','SHA']
    def all_consented(slug):
        stem = P+'v2_'+slug
        return '\n'.join(f'if = {{ limit = {{ {tag} = {{ exists = yes }} }} {tag} = {{ NOT = {{ has_war_with = SPR }} }} has_country_flag = {stem}_accepted@{tag} }}' for tag in parties)
    T(P+'v2_sahara_conference_all_consented', all_consented('sahara_conference'))
    for slug in ('sahara_transition_offer','sahara_presence_offer'):
        T(P+'v2_'+slug+'_all_consented', all_consented('sahara_conference')+'\n'+all_consented(slug))
    E(P+'v2_sahara_update', f'''if = {{ limit = {{ {P}v2_sahara_presence_offer_all_consented = yes NOT = {{ has_country_flag = {P}v2_sahara_interim_started }} }}
set_country_flag = {P}v2_sahara_interim_started set_country_flag = {{ flag = {P}v2_sahara_interim_live days = 720 }} add_timed_idea = {{ idea = {P}v2_sahara_interim days = 720 }} }}''')
    pacts = '\n'.join(f'if = {{ limit = {{ {tag} = {{ exists = yes }} }} diplomatic_relation = {{ country = {tag} relation = non_aggression_pact active = yes }} }}' for tag in parties)
    D(P+'v2_sahara_settlement', f'''visible = {{ has_country_flag = {unlock('sahara_transition_offer')} NOT = {{ has_country_flag = {P}v2_sahara_settled }} }}
available = {{ {P}v2_sahara_transition_offer_all_consented = yes }}
complete_effect = {{ if = {{ limit = {{ {P}v2_sahara_transition_offer_all_consented = yes }} {pacts} set_country_flag = {P}v2_sahara_settled }} }}''')
    L(P+'v2_sahara_settlement','Conclude the Saharan Transition')
    L(P+'v2_sahara_settlement_desc','Conclude the accepted transition protocol and establish non-aggression agreements between Spain and every participating government. Territorial administration remains subject to a separate agreement by its current owner.')
    D(P+'v2_review_sahara_administration', f'''visible = {{ has_country_flag = {P}v2_sahara_interim_started NOT = {{ has_country_flag = {P}v2_sahara_interim_live }} }}
complete_effect = {{ clr_country_flag = {P}v2_sahara_interim_started
every_other_country = {{ SPR = {{ clr_country_flag = {P}v2_sahara_presence_offer_accepted@PREV }} }} }}''')
    L(P+'v2_review_sahara_administration','Review the Interim Administration')
    L(P+'v2_review_sahara_administration_desc','The 720-day interim protocol has expired. Reopen negotiations so that every participant can consider renewed terms for a further period.')
    refresh += [f'{P}v2_sahara_update = yes']
    for num, suffix, title, desc in [(1001,'declined','A Proposal Declined','The other government has declined the proposed terms. No payment or agreement has been concluded.'),(1002,'expired','A Proposal Has Expired','A diplomatic proposal has reached the end of its acceptance period. Fresh terms may now be submitted.'),(1003,'quote_changed','Investment Terms Have Changed','The project price, timetable or eligibility changed before authorisation. No funds were committed. The ministry can prepare a fresh proposal.')]:
        events.append(f'country_event = {{ id = COLDWAR_SPR_v2_agreements.{num} title = {P}{suffix}_title desc = {P}{suffix}_desc picture = GFX_report_event_generic_diplomacy is_triggered_only = yes option = {{ name = {P}noted }} }}')
        L(P+suffix+'_title',title);L(P+suffix+'_desc',desc)
    L(P+'noted','Take note')
    # Date observers are one-shot and skip windows in late saves. The later energy
    # adjustment is separately observed, so the 1973 shock cannot be retro-mitigated.
    refresh += [f'''if = {{ limit = {{ date > 1973.10.15 date < 1974.1.1 NOT = {{ has_country_flag = {P}v2_oil1973_seen }} }} set_country_flag = {P}v2_oil1973_seen add_timed_idea = {{ idea = {P}v2_oil_shock days = 180 }} }}
if = {{ limit = {{ date > 1979.7.1 date < 1980.1.1 NOT = {{ has_country_flag = {P}v2_oil1979_seen }} }} set_country_flag = {P}v2_oil1979_seen
if = {{ limit = {{ {applied('crisis_planning')} has_country_flag = {unlock('energy_crisis_protocol')} {P}reserve_facility_owned = yes }} add_timed_idea = {{ idea = {P}v2_oil_shock days = 90 }} }}
else = {{ add_timed_idea = {{ idea = {P}v2_oil_shock days = 180 }} }} }}
if = {{ limit = {{ date > 1981.1.1 date < 1982.1.1 NOT = {{ has_country_flag = {P}v2_industrial1981_seen }} }} set_country_flag = {P}v2_industrial1981_seen
if = {{ limit = {{ {applied('reconversion_fund')} has_country_flag = {unlock('industrial_adjustment')} }} add_timed_idea = {{ idea = {P}v2_funded_adjustment days = 365 }} }}
else = {{ add_timed_idea = {{ idea = {P}v2_industrial_shock days = 365 }} }} }}''']
    E(P+'initialize_agreements',f'if = {{ limit = {{ tag = SPR IMP_is_1970_scenario = yes NOT = {{ has_country_flag = {P}v2_agreements_initialized }} }} set_country_flag = {P}v2_agreements_initialized }}')
    E(P+'refresh_agreements','if = { limit = { tag = SPR IMP_is_1970_scenario = yes }\n'+'\n'.join(refresh)+'\n}')

    # Idempotent, narrowly scoped native NATO integration. An invitation in a late
    # start or a non-Spanish request keeps its original availability.
    nato_path = 'events/NATO_system.txt'
    nato = (root/nato_path).read_text(encoding='utf-8-sig')
    for option, scope in [('NATO.14.a','FROM'),('NATO.9.a','THIS')]:
        marker = '# IMPERIA CW — Cold War: Spain V2 live NATO consent ('+option+').'
        if marker not in nato:
            condition = (f'FROM = {{ {P}v2_nato_offer_live = yes NOT = {{ has_country_flag = {P}v2_nato_leader_approved }} }} has_idea = NATO_member is_faction_leader = yes NOT = {{ has_war_with = SPR }}' if scope == 'FROM' else f'{P}v2_nato_offer_live = yes has_country_flag = {P}v2_nato_leader_approved check_variable = {{ {P}v2_nato_sponsor = FROM.id }} FROM = {{ has_idea = NATO_member is_faction_leader = yes NOT = {{ has_war_with = SPR }} }}')
            guard = f'\n\t\t{marker}\n\t\ttrigger = {{ OR = {{ NOT = {{ {scope} = {{ tag = SPR IMP_is_1970_scenario = yes }} }} AND = {{ {condition} }} }} }}'
            needle = 'name = '+option
            assert nato.count(needle) == 1
            nato = nato.replace(needle,needle+guard)
    # Execute-time guards are necessary even if an already-open event displayed
    # its accept option before eligibility changed.
    leader_marker = '# IMPERIA CW — Cold War: Spain V2 NATO leader transaction.'
    if leader_marker not in nato:
        old = 'add_political_power = 25\n\t\tFROM = { country_event = { id = NATO.9 hours = 6 } }'
        assert nato.count(old) == 1
        new = f'''{leader_marker}
        if = {{ limit = {{ OR = {{ NOT = {{ FROM = {{ tag = SPR IMP_is_1970_scenario = yes }} }} AND = {{
          FROM = {{ {P}v2_nato_offer_live = yes NOT = {{ has_country_flag = {P}v2_nato_leader_approved }} }}
          has_idea = NATO_member is_faction_leader = yes NOT = {{ has_war_with = SPR }}
        }} }} }}
          add_political_power = 25
          FROM = {{ if = {{ limit = {{ tag = SPR IMP_is_1970_scenario = yes }} set_country_flag = {P}v2_nato_leader_approved set_variable = {{ {P}v2_nato_sponsor = ROOT.id }} }} country_event = {{ id = NATO.9 hours = 6 }} }}
        }}'''
        nato = nato.replace(old,new)
    applicant_marker = '# IMPERIA CW — Cold War: Spain V2 NATO applicant transaction.'
    if applicant_marker not in nato:
        old = 'set_country_flag = has_joined_NATO_by_event\n\t\tNATO_join = yes\n\t\thidden_effect = { USA = { country_event = NATO.10 } }'
        assert nato.count(old) == 1
        new = f'''{applicant_marker}
        if = {{ limit = {{ OR = {{ NOT = {{ AND = {{ tag = SPR IMP_is_1970_scenario = yes }} }} AND = {{
          {P}v2_nato_offer_live = yes has_country_flag = {P}v2_nato_leader_approved
          check_variable = {{ {P}v2_nato_sponsor = FROM.id }}
          FROM = {{ has_idea = NATO_member is_faction_leader = yes NOT = {{ has_war_with = SPR }} }}
        }} }} }}
          set_country_flag = has_joined_NATO_by_event NATO_join = yes
          if = {{ limit = {{ tag = SPR IMP_is_1970_scenario = yes }} clr_country_flag = {P}v2_nato_pending clr_country_flag = {P}v2_nato_leader_approved }}
          hidden_effect = {{ USA = {{ country_event = NATO.10 }} }}
        }}'''
        nato = nato.replace(old,new)
    # Every focus effect has a prospective preview with exact terms even before its
    # live treaty and recipient guards become true.
    for slug in sources:
        assert P+slug in previews, slug
    outputs = {
        'common/scripted_effects/COLDWAR_SPR_v2_agreements.txt': HEADER+'\n\n'.join(effects)+'\n',
        'common/scripted_triggers/COLDWAR_SPR_v2_agreements.txt': HEADER+'\n\n'.join(triggers)+'\n',
        'common/decisions/COLDWAR_SPR_v2_agreements.txt': HEADER+P+'agreements_category = {\n'+'\n\n'.join(decisions)+'\n}\n',
        'common/decisions/categories/COLDWAR_SPR_v2_agreements.txt': HEADER+P+'agreements_category = { icon = generic_foreign_policy allowed = { tag = SPR } visible = { IMP_is_1970_scenario = yes } }\n',
        'common/ideas/COLDWAR_SPR_v2_agreements.txt': HEADER+'ideas = { country = {\n'+'\n'.join(ideas)+'\n} }\n',
        'events/COLDWAR_SPR_v2_agreements.txt': HEADER+'\n\n'.join(events)+'\n',
        'tools/spain_1970_v2/agreements_previews.json': json.dumps(previews,indent=2,ensure_ascii=False)+'\n',
        nato_path: nato,
    }
    localisation = '\ufeffl_english:\n '+HEADER.replace('\n','\n ')
    localisation += '\n'.join(' '+key+':0 '+json.dumps(value,ensure_ascii=False) for key,value in loc.items())+'\n'
    outputs['localisation/english/COLDWAR_SPR_v2_agreements_l_english.yml'] = localisation.encode('utf-8')
    for path in list(outputs):
        if path.startswith('events/COLDWAR_SPR'):
            outputs[path] = outputs[path].replace('GFX_report_event_generic_economic_reform','GFX_report_event_european_business').replace('GFX_report_event_generic_factory','GFX_report_event_european_business').replace('GFX_report_event_generic_diplomacy','GFX_report_event_generic_political_crisis')
        # IMPERIA CW — Cold War: Keep generated agreement scripts free of trailing whitespace.
        if path in ['common/decisions/COLDWAR_SPR_v2_agreements.txt', 'common/scripted_triggers/COLDWAR_SPR_v2_agreements.txt']:
            outputs[path] = '\n'.join(line.rstrip() for line in outputs[path].splitlines()) + '\n'
    return outputs


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[2]
    design = json.loads((Path(__file__).parent/'approved_design.json').read_text(encoding='utf-8-sig'))
    for relpath, data in build(root,design).items():
        path = root/relpath
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data if isinstance(data,bytes) else data.encode('utf-8'))
