# IMPERIA COLD WAR — Native decision-only annual Union orders and human responsibility.
"""Narrow generator. Never rebuilds the Soviet tree or unrelated country content."""
from pathlib import Path
import hashlib
import json
import sys
from catalogue import FAMILIES, CHANNELS, CHANNEL_SOURCES, channels_for, TAGS, IDS, GROUPS, CONFLICTS, POLICIES, TEMPORARY_POLICIES, PERIOD, OUTCOME_DAYS, PROPOSAL_DAYS

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, emit, first

P = 'COLDWAR_ORD_'
MARKER = '# IMPERIA COLD WAR — Annual Union orders in the native Decisions menu.'
LOC = {}
OUTPUTS = []


def block(key, body):
    return key + ' = {\n' + body + '\n}\n'


def iff(condition, body, otherwise=''):
    return block('if', block('limit', condition) + body) + (block('else', otherwise) if otherwise else '')


def eq(name, value):
    return f'check_variable = {{ {name} = {value} }}'


def at_least(name, value):
    return f'check_variable = {{ var = {name} value = {value} compare = greater_than_or_equals }}'


def setv(name, value):
    return f'set_variable = {{ {name} = {value} }}\n'


def timed_flag(name,days):
    return f'set_country_flag = {{ flag = {name} value = 1 days = {days} }}\n'


def loc(key, text):
    LOC[key] = text
    return key


def write(relative, body, localisation=False):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if localisation:
        text = 'l_english:\n' + MARKER + '\n' + body
        encoding = 'utf-8-sig'
    else:
        text = MARKER + '\n' + emit(parse(body)) + '\n'
        encoding = 'utf-8'
    path.write_text(text, encoding=encoding)
    OUTPUTS.append(relative)


def scope_all(body):
    return '\n'.join(block(tag, iff('exists = yes', body)) for tag in ('SOV',) + TAGS)


def var(f, suffix):
    return P + f.key + '_' + suffix


def mission(f, kind='objective'):
    return P + kind + '_' + f.key


def state_is(f, value):
    return eq(var(f, 'state'), value)


def remove_mission(identifier):
    # Hidden MD missions are not reliably reported by has_active_mission. Native
    # removal is safe for an absent known ID and must precede a timer refresh.
    if identifier.startswith(P):return 'remove_mission = '+identifier+'\n'
    return iff('has_active_mission = ' + identifier, 'remove_mission = ' + identifier)


def family_scope(f):
    return eq(P + 'draft_family', IDS[f.key])


def proposal_review(f):
    return f'ROOT = {{ tag = SOV {P}actor = yes check_variable = {{ {P}review_target = PREV.id }} check_variable = {{ {P}review_serial_{f.key} = PREV.{var(f,"serial")} }} }}'


def return_review(f):
    return f'ROOT = {{ tag = SOV {P}actor = yes check_variable = {{ {P}return_target = PREV.id }} {eq(P+"return_family",IDS[f.key])} check_variable = {{ {P}return_serial = PREV.{var(f,"serial")} }} }}'


def free(f):
    return ' '.join(eq(P + key + '_state', 0) for key in sorted(CONFLICTS[f.key]))


def family_capacity(f):
    return 'any_owned_state = { is_coastal = yes is_owned_and_controlled_by = PREV } check_variable = { naval_factory_total > 0 }' if f.naval else 'always = yes'


def tally_building(f, suffix):
    result = ''
    for i, building in enumerate(f.buildings):
        value = var(f, suffix + str(i))
        result += setv(value, 0)
        result += block('every_owned_state', 'limit = { is_owned_and_controlled_by = PREV is_core_of = PREV }\n' + f'add_to_variable = {{ PREV.{value} = building_level@{building} }}')
    return result


def source_ready(f):
    if f.buildings:
        conditions = [at_least(var(f, 'current' + str(i)), var(f, 'target' + str(i))) for i in range(len(f.buildings))]
        return block('OR', '\n'.join(conditions))
    proof = at_least(f.counter, var(f, 'target')) if f.counter else 'has_country_flag = ' + var(f, 'certified')
    return block('OR', block('AND', eq(var(f, 'kind'), 1) + '\n' + proof) + block('AND', eq(var(f, 'kind'), 2) + '\n' + at_least(var(f, 'delivered'), var(f, 'quantity'))))


def outcome_id(f, success=True):
    return P + ('successful_' if success else 'unfulfilled_') + f.key


def effect_preview(f, quote=P + 'draft_cost', conditional_target=False, award_only=False):
    # Native numeric formatters inside a non-executing tooltip. No preview payment.
    success='\n'.join(f'add_timed_idea = {{ idea = {outcome_id(c)} days = {OUTCOME_DAYS} }}' for c in channels_for(f))
    failure='\n'.join(f'add_timed_idea = {{ idea = {outcome_id(c,False)} days = {OUTCOME_DAYS} }}' for c in channels_for(f))
    body = f'''custom_effect_tooltip = {P}assistance_heading
add_to_variable = {{ {P}preview = {quote} tooltip = {P}support_debit_tt }}
add_to_variable = {{ {P}preview = {quote} tooltip = {P}support_credit_tt }}
custom_effect_tooltip = {P}success_heading
{success}
custom_effect_tooltip = {P}failure_heading
{failure}
add_timed_idea = {{ idea = {P}shortfall days = {OUTCOME_DAYS} }}'''
    if award_only:body=f'custom_effect_tooltip = {P}success_heading\n'+success
    if conditional_target:
        body = iff(f'var:{P}draft_target = {{ {P}human_country = yes }}', body,
                   f'custom_effect_tooltip = {P}advisory_heading')
    return block('effect_tooltip', body)


def decision(key, title, description, visible, available, effects, preview='', targeted=False, category=None):
    identifier = P + key
    loc(identifier, title)
    loc(identifier + '_desc', description)
    target = ''
    if targeted:
        target = 'target_root_trigger = { always = yes }\ntargets = { ' + ' '.join(TAGS) + ' }\ntarget_non_existing = no\n'
        target += block('target_trigger', 'FROM = { exists = yes ' + P + 'republic = yes }')
    body = f'icon = GFX_decision_generic_factory\nallowed = {{ {P}tag = yes }}\nfire_only_once = no\n' + target
    body += block('visible', f'{P}actor = yes\n' + visible)
    requirement=None
    if key.startswith(('issue_','submit_')):requirement=('commission_ready','The selected republic can accept this commission without a conflicting annual reservation, and any required assistance can be financed.')
    elif key.startswith('approve_'):requirement=('proposal_ready','The submitted proposal remains current and the Soviet treasury can finance any agreed assistance.')
    elif key.startswith(('reject_','withdraw_')):requirement=('proposal_pending','The republican proposal is still awaiting confirmation.')
    elif key.startswith(('review_return_','certify_','decline_return_')):requirement=('return_current','A current production return awaits the Union commission.')
    elif key.startswith('return_'):requirement=('return_not_pending','No production return is already awaiting certification.')
    elif key.startswith('consign_'):requirement=('stock_available','Equipment is available for consignment to Soviet stores.')
    elif key=='decrease':requirement=('quantity_above_one','The proposed annual quantity exceeds one.')
    elif key in TEMPORARY_POLICIES:requirement=('mobilisation_ready','A binding annual commission is active and the previous mobilisation has ended.')
    advertised=available
    if requirement:advertised=block('custom_trigger_tooltip','tooltip = '+loc(P+'require_'+requirement[0],requirement[1])+'\n'+available)
    elif available in {'always = yes','always = no'}:advertised=block('hidden_trigger',available)
    body += block('available', block('hidden_trigger',P+'actor = yes') + advertised)
    body += block('complete_effect', preview + block('hidden_effect', iff(f'{P}actor = yes\n{visible}\n{available}', effects)))
    body += 'ai_will_do = { base = 0 }'
    return block(identifier, body)


def make_triggers():
    text = block(P + 'tag', 'OR = { ' + ' '.join('original_tag = ' + t for t in ('SOV',) + TAGS) + ' }')
    text += block(P + 'human_country', 'is_ai = no')
    text += block(P + 'republic', f'IMP_is_1970_scenario = yes\nexists = yes\nis_subject_of = SOV\nOR = {{ ' + ' '.join('tag = ' + t for t in TAGS) + ' }')
    text += block(P + 'member', f'IMP_is_1970_scenario = yes\nexists = yes\nOR = {{ tag = SOV {P}republic = yes }}')
    text += block(P + 'actor', f'{P}human_country = yes\n{P}member = yes\nhas_global_flag = {P}enabled')
    text += block(P + 'has_live_commission','OR = { '+' '.join(state_is(f,2) for f in FAMILIES)+' }')
    for f in FAMILIES:
        text += block(P + 'free_' + f.key, free(f))
        text += block(P + 'ready_' + f.key, f'{P}republic = yes\n{P}human_country = yes\n{state_is(f, 2)}\n' + source_ready(f))
    write('common/scripted_triggers/COLDWAR_UNION_orders.txt', text)


def make_ideas():
    bodies = ''
    for f in CHANNELS:
        for successful in (True, False):
            identifier = outcome_id(f, successful)
            prefix = 'Successful' if successful else 'Unfulfilled'
            loc(identifier, f'{prefix} Programme: {f.name}')
            loc(identifier + '_desc', ('The republics have fulfilled the Union commission for ' + f.name.lower() + '. Standardised orders and dependable schedules have reduced the cost of the next production series.' if f.equipment and successful else
                'The Union development programme has delivered its agreed capacity. The new installations and established working methods now support the republican economy.' if successful else
                'The annual commission for ' + f.name.lower() + ' has fallen short. Interrupted schedules and unfinished preparations are raising the cost of subsequent work.') + '\n\nThis programme lasts 180 days. Its Union benefits require continued membership. Standing shortfalls take priority while their own programme remains in force.')
            body = f'picture = COLDWAR_SSR_{f.art}\nallowed = {{ always = no }}\nallowed_civil_war = {{ always = yes }}\n'
            if f.equipment:
                gear = '\n'.join(block(eqid, f'build_cost_ic = {"-0.08" if successful else "0.08"}\ninstant = yes') for eqid in f.equipment)
                body += block('equipment_bonus', gear)
            elif successful:
                body += block('modifier', '\n'.join(f'{key} = {value:g}' for key, value in f.modifiers))
            bodies += block(identifier, body)
    bodies += block(P + 'shortfall', 'picture = COLDWAR_SSR_shortages\nallowed = { always = no }\nallowed_civil_war = { always = yes }\nmodifier = { consumer_goods_factor = 0.03 }')
    loc(P + 'shortfall', 'Unfulfilled Union Programmes')
    loc(P + 'shortfall_desc', 'Missed republican commissions have disrupted Union supply schedules. Factories and ministries must devote additional capacity to civilian provisioning while production is reorganised.\n\nConsumer Goods Factor: +3% for 180 days. Concurrent shortfalls do not multiply this burden.')
    for key,(flag,name,art,modifiers,description) in {**POLICIES,**TEMPORARY_POLICIES}.items():
        identifier=P+'policy_'+key
        loc(identifier,name);loc(identifier+'_desc',description+'\n\nThe programme requires continued Union membership.'+(' Its current commission lasts 180 days.' if key in TEMPORARY_POLICIES else ''))
        bodies+=block(identifier,f'picture = COLDWAR_SSR_{art}\nallowed = {{ always = no }}\nallowed_civil_war = {{ always = yes }}\n'+block('modifier','\n'.join(f'{k} = {v:g}' for k,v in modifiers.items())))
    write('common/ideas/COLDWAR_UNION_orders.txt', block('ideas', block('country', bodies)))


def hidden_mission(identifier, days, timeout):
    # Native MD cyber-operation pattern: disallowed for normal selection, but
    # explicitly activatable. visible = { always = no } blocks native activation.
    return block(identifier, f'''icon = GFX_decision_generic_factory
allowed = {{ always = no }}
activation = {{ always = no }}
available = {{ always = no }}
is_good = yes
selectable_mission = no
fire_only_once = no
days_mission_timeout = {days}
timeout_effect = {{ hidden_effect = {{ {timeout} }} }}
ai_will_do = {{ base = 0 }}''')


def make_family_effects(f):
    k = f.key
    s = var(f, 'state')
    eff = ''
    # Reserve atomically in the recipient scope. PREV is the draft's country.
    valid_kind = eq(P + 'draft_kind', 3) if f.buildings else ('OR = { ' + eq(P + 'draft_kind', 1) + (' ' + eq(P + 'draft_kind', 2) if f.delivery else '') + ' }')
    actor_guard = f'''PREV = {{ {P}actor = yes {family_scope(f)} {valid_kind}
{at_least(P + 'draft_quantity', 1)}
check_variable = {{ {P}draft_target = PREV.id }}
OR = {{ tag = SOV check_variable = {{ THIS.id = PREV.id }} }} }}'''
    reserve_guard = f'{P}republic = yes\n{P}free_{k} = yes\n{family_capacity(f)}\n{actor_guard}'
    copy = ''.join(setv(var(f, dst), 'PREV.' + P + src) for dst, src in (('quantity', 'draft_quantity'), ('fraction', 'draft_fraction'), ('kind', 'draft_kind')))
    copy += setv(var(f, 'origin'), 'PREV.id') + setv(var(f, 'delivered'), 0)
    copy += f'add_to_variable = {{ global.{P}next_serial = 1 }}\n' + setv(var(f,'serial'),'global.'+P+'next_serial')
    copy += setv(var(f,'cost'),'SOV.gdp_total') + f'multiply_variable = {{ {var(f,"cost")} = {var(f,"fraction")} }}\n'
    copy += f'clr_country_flag = {var(f, "certified")}\nclr_country_flag = {var(f, "return_pending")}\n'
    pending = setv(s, 1) + timed_flag(mission(f,'proposal'),PROPOSAL_DAYS) + f'activate_mission = {mission(f, "proposal")}'
    direct = f'{P}activate_{k} = yes'
    eff += block(P + 'reserve_' + k, iff(reserve_guard, copy + iff(eq(var(f, 'origin'), 'SOV.id'), direct, pending)))
    # Quote the approved fraction against current Soviet GDP at commitment.
    quote = setv(var(f, 'cost'), 'SOV.gdp_total') + f'multiply_variable = {{ {var(f, "cost")} = {var(f, "fraction")} }}\n'
    affordable = 'OR = { '+eq(var(f,'fraction'),0)+' SOV = { ' + at_least('treasury', 'PREV.' + var(f, 'cost')) + ' } }'
    eligibility = f'{P}republic = yes\n{family_capacity(f)}\nOR = {{ {state_is(f, 0)} {state_is(f, 1)} }}'
    pay = iff(at_least(var(f, 'cost'), '.00001'), f'''SOV = {{
set_temp_variable = {{ treasury_change = {{ value = PREV.{var(f, 'cost')} multiply = -1 }} }}
modify_treasury_effect = yes
}}
set_temp_variable = {{ treasury_change = {var(f, 'cost')} }}
modify_treasury_effect = yes''')
    start = pay + remove_mission(mission(f, 'proposal')) + f'clr_country_flag = {mission(f,"proposal")}\n' + setv(s, 2)
    start += timed_flag(mission(f,'window'),PERIOD) + f'activate_mission = {mission(f, "window")}\n'
    if f.buildings:
        start += tally_building(f, 'baseline')
        for i in range(len(f.buildings)):
            start += setv(var(f, 'target' + str(i)), var(f, 'baseline' + str(i)))
            start += f'add_to_variable = {{ {var(f, "target" + str(i))} = {var(f, "quantity")} }}\n'
    elif f.counter:
        start += setv(var(f, 'baseline'), f.counter) + setv(var(f, 'target'), f.counter)
        start += f'add_to_variable = {{ {var(f, "target")} = {var(f, "quantity")} }}\n'
    start += iff(P + 'human_country = yes', f'activate_mission = {mission(f)}', setv(s, 6))
    eff += block(P + 'activate_' + k, quote + iff(eligibility + '\n' + affordable, start))
    approve_guard = proposal_review(f)+f'\n{state_is(f, 1)}\n{P}human_country = yes\n{P}republic = yes'
    eff += block(P + 'approve_' + k, iff(approve_guard, f'{P}activate_{k} = yes'))
    reject_guard = f'{state_is(f, 1)}\nROOT = {{ {P}actor = yes }}\nOR = {{ {proposal_review(f)} ROOT = {{ NOT = {{ tag = SOV }} check_variable = {{ THIS.id = PREV.id }} }} }}'
    eff += block(P + 'reject_' + k, iff(reject_guard, setv(s, 0) + remove_mission(mission(f, 'proposal')) + f'clr_country_flag = {mission(f,"proposal")}\nclr_country_flag = {var(f, "return_pending")}'))
    # Neutralisation never rewrites a settled outcome and never opens a fresh year.
    eff += block(P + 'neutralise_' + k, iff(state_is(f, 2), setv(s, 5) + remove_mission(mission(f)) + f'clr_country_flag = {var(f, "return_pending")}'))
    ready = f'{P}ready_{k} = yes'
    success = setv(s, 3) + remove_mission(mission(f)) + f'clr_country_flag = {var(f, "return_pending")}\n'
    success += f'set_country_flag = {P}calendar_scored\nset_country_flag = {P}calendar_success\n'
    success += block('SOV', remove_mission(mission(f, 'success_clock')) + timed_flag(mission(f,'success_clock'),OUTCOME_DAYS) + f'activate_mission = {mission(f, "success_clock")}\n{P}outcome_changed_{k} = yes\n{P}tally_calendar = yes')
    eff += block(P + 'succeed_' + k, iff(ready, success))
    fail_guard = f'{state_is(f, 2)}\n{P}republic = yes\n{P}human_country = yes'
    failure = setv(s, 4) + remove_mission(mission(f)) + f'clr_country_flag = {var(f, "return_pending")}\n'
    failure += f'set_country_flag = {P}calendar_scored\nset_country_flag = {P}calendar_failed\n'
    failure += block('SOV', remove_mission(mission(f, 'failure_clock')) + timed_flag(mission(f,'failure_clock'),OUTCOME_DAYS) + f'activate_mission = {mission(f, "failure_clock")}\n{P}outcome_changed_{k} = yes\n' + remove_mission(P + 'shortfall_clock') + timed_flag(P+'shortfall_clock',OUTCOME_DAYS) + f'activate_mission = {P}shortfall_clock\n{P}sync_shortfall_all = yes\n{P}tally_calendar = yes')
    eff += block(P + 'fail_' + k, iff(fail_guard, failure, f'{P}neutralise_{k} = yes'))
    # The hidden annual clock closes the reservation, even after early fulfilment.
    close = iff(state_is(f, 2), f'{P}measure_{k} = yes\n' + iff(ready, f'{P}succeed_{k} = yes', f'{P}fail_{k} = yes'))
    close += remove_mission(mission(f)) + remove_mission(mission(f,'window')) + f'clr_country_flag = {mission(f,"window")}\n' + setv(s, 0) + f'clr_country_flag = {var(f, "return_pending")}\nclr_country_flag = {var(f, "certified")}'
    eff += block(P + 'close_' + k, iff(f'check_variable = {{ {s} > 0 }}',close))
    measure = tally_building(f, 'current') if f.buildings else ''
    if f.counter:
        measure += setv(var(f, 'produced'), f.counter) + f'subtract_from_variable = {{ {var(f, "produced")} = {var(f, "baseline")} }}\nclamp_variable = {{ var = {var(f, "produced")} min = 0 }}\n'
    eff += block(P + 'measure_' + k, measure or 'set_temp_variable = { COLDWAR_ORD_noop = 0 }')
    if f.delivery:
        equipment = f.equipment[0]
        delivery_guard = fail_guard + '\n' + eq(var(f, 'kind'), 2) + '\n' + at_least('num_equipment@' + equipment, '.00001')
        send = setv(var(f, 'consignment'), var(f, 'quantity')) + f'subtract_from_variable = {{ {var(f, "consignment")} = {var(f, "delivered")} }}\n'
        send += f'set_temp_variable = {{ {P}before_delivery = SOV.num_equipment@{equipment} }}\nsend_equipment = {{ type = {equipment} amount = {var(f, "consignment")} target = SOV }}\n'
        send += f'set_temp_variable = {{ {P}actual_delivery = SOV.num_equipment@{equipment} }}\nsubtract_from_temp_variable = {{ {P}actual_delivery = {P}before_delivery }}\nclamp_temp_variable = {{ var = {P}actual_delivery min = 0 max = {var(f, "consignment")} }}\n'
        send += f'add_to_variable = {{ {var(f, "delivered")} = {P}actual_delivery }}\n{P}succeed_{k} = yes'
        eff += block(P + 'deliver_' + k, iff(delivery_guard, send))
    if not f.buildings and not f.counter:
        cert_guard = fail_guard + '\n' + eq(var(f, 'kind'), 1) + '\n'+return_review(f)+'\nhas_country_flag = ' + var(f, 'return_pending')
        eff += block(P + 'certify_' + k, iff(cert_guard, f'set_country_flag = {var(f, "certified")}\n{P}succeed_{k} = yes'))
    # One live outcome per actual equipment target prevents broad/narrow stacking.
    all_sync = scope_all('\n'.join(f'{P}sync_{c.key} = yes' for c in channels_for(f)))
    eff += block(P + 'outcome_changed_' + k, all_sync)
    return eff


def make_channel_sync(f):
    sync_body = ''
    for idea in (outcome_id(f), outcome_id(f, False)):
        sync_body += iff('has_idea = ' + idea, 'remove_ideas = ' + idea)
    sync_body+=f'set_temp_variable = {{ {P}failure_remaining = 0 }}\nset_temp_variable = {{ {P}success_remaining = 0 }}\n'
    for source in CHANNEL_SOURCES[f.key]:
        for outcome in ('success','failure'):
            clock=mission(source,outcome+'_clock')
            remaining=P+outcome+'_remaining'
            read=f'set_temp_variable = {{ {P}candidate_remaining = SOV.days_mission_timeout@{clock} }}\n'
            read+=iff(at_least(P+'candidate_remaining',remaining),f'set_temp_variable = {{ {remaining} = {P}candidate_remaining }}')
            sync_body+=iff(f'SOV = {{ has_country_flag = {clock} }}',read)
    apply_failure=f'add_timed_idea = {{ idea = {outcome_id(f,False)} days = {P}failure_remaining }}'
    apply_success=f'add_timed_idea = {{ idea = {outcome_id(f)} days = {P}success_remaining }}'
    sync_body+=iff(P+'member = yes',iff(f'check_variable = {{ {P}failure_remaining > 0 }}',apply_failure,iff(f'check_variable = {{ {P}success_remaining > 0 }}',apply_success)))
    return block(P+'sync_'+f.key,sync_body)


def make_effects():
    text = ''
    text += block(P + 'refresh_draft', setv(P + 'draft_cost', 'SOV.gdp_total') + f'multiply_variable = {{ {P}draft_cost = {P}draft_fraction }}')
    # Explicit actor -> selected republic scope preserves PREV for the transaction.
    dispatch = ''
    for f in FAMILIES:
        dispatch += iff(family_scope(f), f'var:{P}draft_target = {{ {P}reserve_{f.key} = yes }}')
    text += block(P + 'commit_draft', iff(f'{P}actor = yes\nvar:{P}draft_target = {{ {P}republic = yes }}', dispatch))
    snapshot=''.join(setv(P+'review_serial_'+f.key,'PREV.'+var(f,'serial')) for f in FAMILIES)
    text+=block(P+'snapshot_proposals',iff(f'tag = SOV {P}actor = yes var:{P}review_target = {{ {P}republic = yes }}',f'var:{P}review_target = {{ SOV = {{ '+snapshot+' } }'))
    init = f'''if = {{ limit = {{ NOT = {{ has_country_flag = {P}initialised }} }}
set_country_flag = {P}initialised
{setv(P + 'draft_target', 'id')}
{setv(P + 'draft_family', IDS['mbt'])}
{setv(P + 'draft_kind', 1)}
{setv(P + 'draft_quantity', 300)}
{setv(P + 'draft_step', 100)}
{setv(P + 'draft_fraction', 0)}
{setv(P + 'draft_stage', 0)}
if = {{ limit = {{ tag = SOV }} {setv(P + 'draft_target', 'UKR.id')} }}
}}'''
    text += block(P + 'initialise_country', init)
    bootstrap = f'''if = {{ limit = {{ IMP_is_1970_scenario = yes exists = yes tag = SOV }}
set_global_flag = {P}enabled
{P}initialise_country = yes
if = {{ limit = {{ NOT = {{ has_country_flag = {P}legacy_migrated }} }}
set_country_flag = {P}legacy_migrated
{remove_mission('COLDWAR_UNI_union_plan')}
clr_global_flag = COLDWAR_UNI_year_running
clr_global_flag = COLDWAR_UNI_year_won
}}
{scope_all(P + 'initialise_country = yes ' + P + 'retire_legacy = yes')}
}}'''
    text += block(P + 'bootstrap', bootstrap)
    retired = f'if = {{ limit = {{ NOT = {{ has_country_flag = {P}legacy_migrated }} }}\nset_country_flag = {P}legacy_migrated\n'
    for prefix, keys in (('target', ('civ','arms','power','agri','roads','dock','oil','deliver','discipline','steel','cotton','virgin','orchards')), ('directive', ('civ','arms','power','nuclear','agri','roads','dock','deliver','komsomol'))):
        for key in keys:
            retired += remove_mission('COLDWAR_UNI_' + prefix + '_' + key)
        retired += 'clr_country_flag = COLDWAR_UNI_' + prefix + '_active\n'
    retired += 'clr_country_flag = COLDWAR_UNI_dir_pending\n}'
    text += block(P + 'retire_legacy', retired)
    sync_all = ''.join(f'{P}sync_{f.key} = yes\n' for f in CHANNELS) + P + 'sync_shortfall = yes'
    text += block(P + 'sync_all', sync_all)
    shortfall_sync = iff('has_idea = ' + P + 'shortfall', 'remove_ideas = ' + P + 'shortfall')
    shortfall_sync += iff(f'{P}member = yes SOV = {{ has_country_flag = {P}shortfall_clock }}',
        f'set_temp_variable = {{ {P}outcome_remaining = SOV.days_mission_timeout@{P}shortfall_clock }}\nadd_timed_idea = {{ idea = {P}shortfall days = {P}outcome_remaining }}')
    text += block(P + 'sync_shortfall', shortfall_sync)
    text += block(P + 'sync_shortfall_all', scope_all(P + 'sync_shortfall = yes'))
    policy_sync=''
    for key,(flag,name,art,modifiers,description) in POLICIES.items():
        idea=P+'policy_'+key
        enabled=f'{P}member = yes has_country_flag = {flag}'
        policy_sync+=iff(enabled,iff('NOT = { has_idea = '+idea+' }','add_ideas = '+idea),iff('has_idea = '+idea,'remove_ideas = '+idea))
    for key in TEMPORARY_POLICIES:
        idea=P+'policy_'+key;clock=P+'policy_clock_'+key
        enabled=f'{P}member = yes has_country_flag = {clock}'
        grant=f'set_temp_variable = {{ {P}policy_left = days_mission_timeout@{clock} }}\nadd_timed_idea = {{ idea = {idea} days = {P}policy_left }}'
        policy_sync+=iff(enabled,iff('NOT = { has_idea = '+idea+' }',grant),iff('has_idea = '+idea,'remove_ideas = '+idea))
    text+=block(P+'sync_policies',policy_sync)
    daily = f'{P}initialise_country = yes\n{P}retire_legacy = yes\n'
    daily+=P+'sync_policies = yes\n'
    daily += iff(P + 'human_country = yes', P + 'refresh_draft = yes')
    daily += iff(f'{P}member = yes NOT = {{ has_country_flag = {P}member_seen }}', f'set_country_flag = {P}member_seen\n{P}sync_all = yes')
    daily += iff(f'{P}member = no has_country_flag = {P}member_seen', f'clr_country_flag = {P}member_seen\n{P}sync_all = yes')
    for f in FAMILIES:
        k=f.key
        active = iff(f'OR = {{ {P}republic = no {P}human_country = no }}', f'{P}neutralise_{k} = yes')
        active += iff(f'{state_is(f,2)}', f'{P}measure_{k} = yes\n{P}succeed_{k} = yes')
        daily += iff(state_is(f,2), active)
        daily += iff(f'{state_is(f,1)} OR = {{ {P}republic = no {P}human_country = no }}', setv(var(f,'state'),0) + remove_mission(mission(f,'proposal')) + f'clr_country_flag = {mission(f,"proposal")}')
        daily += iff(state_is(f,1), setv(var(f,'cost'),'SOV.gdp_total') + f'multiply_variable = {{ {var(f,"cost")} = {var(f,"fraction")} }}')
        daily += iff(f'{state_is(f,1)} NOT = {{ has_country_flag = {mission(f,"proposal")} }}',setv(var(f,'state'),0)+remove_mission(mission(f,'proposal')))
        daily += iff(f'check_variable = {{ {var(f,"state")} > 1 }} NOT = {{ has_country_flag = {mission(f,"window")} }}',f'{P}close_{k} = yes')
    text += block(P + 'daily', iff('IMP_is_1970_scenario = yes has_global_flag = ' + P + 'enabled', daily))
    for f in FAMILIES:
        text += make_family_effects(f)
    for f in CHANNELS:
        text += make_channel_sync(f)
    # Calendar statistics consider actual settled human obligations, never AI fiction.
    tally = setv('global.COLDWAR_UNI_members',0) + setv('global.COLDWAR_UNI_fulfilled',0)
    for tag in TAGS:
        tally += block(tag, iff(f'exists = yes has_country_flag = {P}calendar_scored', 'add_to_variable = { global.COLDWAR_UNI_members = 1 }\n' + iff(f'has_country_flag = {P}calendar_success NOT = {{ has_country_flag = {P}calendar_failed }}','add_to_variable = { global.COLDWAR_UNI_fulfilled = 1 }')))
    tally += setv('global.COLDWAR_UNI_needed','global.COLDWAR_UNI_members')
    tally += 'multiply_variable = { global.COLDWAR_UNI_needed = 9 }\ndivide_variable = { global.COLDWAR_UNI_needed = 14 }\nadd_to_variable = { global.COLDWAR_UNI_needed = 0.49999 }\nround_variable = global.COLDWAR_UNI_needed\nclr_global_flag = COLDWAR_UNI_year_won\n'
    tally += iff('check_variable = { global.COLDWAR_UNI_members > 0 } ' + at_least('global.COLDWAR_UNI_fulfilled','global.COLDWAR_UNI_needed'),'set_global_flag = COLDWAR_UNI_year_won')
    text += block(P + 'tally_calendar', tally)
    settle = setv('global.COLDWAR_UNI_year_plan','global.COLDWAR_SOV_plan') + P + 'tally_calendar = yes\n'
    for k in ('members','fulfilled','needed'):
        settle += setv('global.COLDWAR_UNI_last_' + k, 'global.COLDWAR_UNI_' + k)
    settle += 'clr_global_flag = COLDWAR_UNI_last_won\n'
    win = 'set_global_flag = COLDWAR_UNI_last_won\n'
    for plan in range(9,14):
        win += iff(eq('global.COLDWAR_SOV_plan',plan),f'add_to_variable = {{ global.COLDWAR_UNI_good_years_{plan} = 1 }}')
    settle += iff('has_global_flag = COLDWAR_UNI_year_won',win)
    settle += iff('has_global_flag = COLDWAR_UNI_year_won',scope_all(iff(P+'member = yes','COLDWAR_UNI_add_union_buff = yes')))
    for tag in TAGS:
        settle += block(tag,'\n'.join('clr_country_flag = '+P+'calendar_'+name for name in ('scored','success','failed')))
    settle += P + 'tally_calendar = yes'
    text += block(P + 'settle_calendar',iff('has_global_flag = '+P+'enabled',settle))
    write('common/scripted_effects/COLDWAR_UNION_orders.txt', text)


def make_categories():
    text = ''
    for suffix,title,priority in (('prepare','Annual Union Orders',196),('submissions','Republican Submissions',195),('register','Annual Obligations',194)):
        key=P+suffix
        loc(key,title)
        if suffix=='prepare':
            description="The Union ministries coordinate republican commissions for the coming year. Moscow may issue a directive, while a republican council may submit its own proposal for confirmation.\n\nRepublic: §Y[COLDWAR_ORD_GetRecipient]§!\nCommission: §Y[COLDWAR_ORD_GetFamily]§!\nObligation: [COLDWAR_ORD_GetKind]\nAnnual quantity: §Y[?COLDWAR_ORD_draft_quantity|0]§!\nAccounting period: §Y365 days§!\nUnion assistance: §Y[?COLDWAR_ORD_draft_fraction|%3]§! of Soviet GDP\n\n[COLDWAR_ORD_GetMeasurement]"
        elif suffix=='submissions':
            description='Republican planning councils have submitted their commissions for Soviet confirmation. Approval commits the published quantity and assistance, then opens a full year of work. Unsigned proposals carry no production obligation.'
        else:
            description='The annual register records issued commissions and their remaining time. A fulfilled programme or shortfall lasts 180 days. AI administrations carry no punitive quota; an unfinished commission transferred to AI administration is closed neutrally.'
        loc(key+'_desc',description)
        text+=block(key,f'icon = GFX_decision_category_generic_economy\npriority = {priority}\nvisible_when_empty = yes\nallowed = {{ {P}tag = yes }}\nvisible = {{ {P}actor = yes }}')
    write('common/decisions/categories/COLDWAR_UNION_orders.txt',text)


def make_prepare_decisions():
    text=''
    def d(key,title,desc,stage,effect,available='always = yes',visible='',preview=''):
        return decision(key,title,desc,eq(P+'draft_stage',stage)+'\n'+visible,available,effect,preview)
    title='The planning council has prepared the next annual commission. Select its terms before it is entered in the Union register.'
    for key,name,stage in (('choose_republic','Choose the Republic',1),('choose_kind','Change the Obligation',2),('choose_family','Choose the Production Sector',3),('choose_quantity','Adjust the Annual Quantity',5),('choose_funding','Set Union Assistance',6)):
        text+=d(key,name,title,0,setv(P+'draft_stage',stage),visible='tag = SOV' if key=='choose_republic' else '')
    for i,tag in enumerate(TAGS):
        vis=f'tag = SOV {tag} = {{ {P}republic = yes OR = {{ {P}human_country = yes ROOT = {{ has_country_flag = {P}show_ai }} }} }}'
        text+=d('recipient_'+tag,f'Commission for [{tag}.GetNameDef]',title,1,setv(P+'draft_target',tag+'.id')+setv(P+'draft_stage',0),visible=vis)
    text+=d('toggle_ai','Show AI Advisory Programmes','AI administrations may receive development programmes without failure penalties.',1,iff('has_country_flag = '+P+'show_ai','clr_country_flag = '+P+'show_ai','set_country_flag = '+P+'show_ai'),visible='tag = SOV')
    for kind,name,desc in ((1,'Production Quota','New output is counted from the opening return. Narrow equipment classes require a certified production return.'),(2,'Delivery Order','The commission is fulfilled by actual consignments to Soviet stores. Existing reserves may be used.'),(3,'Construction Target','The republic must add the agreed capacity in territory it owns and controls.')):
        family='civilian' if kind==3 else 'mbt'
        effects=setv(P+'draft_kind',kind)+setv(P+'draft_family',IDS[family])+setv(P+'draft_quantity',1 if kind==3 else 300)+setv(P+'draft_stage',0)
        text+=d('kind_'+str(kind),name,desc,2,effects)
    for group,name in GROUPS.items():
        visibility=eq(P+'draft_kind',3) if group==6 else 'NOT = { '+eq(P+'draft_kind',3)+' }'
        text+=d('group_'+str(group),name,title,3,setv(P+'draft_group',group)+setv(P+'draft_stage',4),visible=visibility)
    for f in FAMILIES:
        vis=eq(P+'draft_group',f.group)
        if not f.delivery and not f.buildings:
            vis+=' NOT = { '+eq(P+'draft_kind',2)+' }'
        if f.naval:
            vis+=f' var:{P}draft_target = {{ {family_capacity(f)} }}'
        effect=setv(P+'draft_family',IDS[f.key])+setv(P+'draft_stage',0)
        text+=d('family_'+f.key,f.name,('Additional agricultural districts or civilian textile-processing capacity may fulfil this cotton programme.' if f.key=='cotton' else title),4,effect,visible=vis)
    for step in (1,10,100,1000):
        text+=d('step_'+str(step),'Quantity Adjustment: '+str(step),'The planning office revises the proposed annual quantity in the selected increment.',5,setv(P+'draft_step',step))
    text+=d('increase','Increase Quantity by [?COLDWAR_ORD_draft_step|0]',title,5,f'add_to_variable = {{ {P}draft_quantity = {P}draft_step }}\nclamp_variable = {{ var = {P}draft_quantity max = 1000000 }}')
    text+=d('decrease','Decrease Quantity by [?COLDWAR_ORD_draft_step|0]',title,5,f'subtract_from_variable = {{ {P}draft_quantity = {P}draft_step }}\nclamp_variable = {{ var = {P}draft_quantity min = 1 }}',available=f'check_variable = {{ {P}draft_quantity > 1 }}')
    for key,fraction,label in (('none',0,'No Financial Assistance'),('025',.00025,'0.025% of Soviet GDP'),('05',.0005,'0.05% of Soviet GDP'),('10',.001,'0.1% of Soviet GDP'),('20',.002,'0.2% of Soviet GDP')):
        text+=d('funding_'+key,label,'The Soviet treasury will advance the agreed share when the commission is confirmed.',6,setv(P+'draft_fraction',f'{fraction:.5f}')+setv(P+'draft_stage',0)+P+'refresh_draft = yes')
    text+=decision('back','Return to the Commission','Review the proposed terms before entering the annual register.',f'check_variable = {{ {P}draft_stage > 0 }}','always = yes',setv(P+'draft_stage',0)+P+'refresh_draft = yes')
    for f in FAMILIES:
        target=f'var:{P}draft_target = {{ {P}republic = yes {P}free_{f.key} = yes {family_capacity(f)} }}'
        vis=family_scope(f)+' '+eq(P+'draft_stage',0)
        description='Moscow enters the published commission in the Union register. A player republic is bound for a full year. An AI administration instead receives an advisory programme without punitive consequences.'
        availability=target+' OR = { '+eq(P+'draft_fraction',0)+' SOV = { '+at_least('treasury','ROOT.'+P+'draft_cost')+' } }'
        text+=decision('issue_'+f.key,'Issue Annual Order: '+f.name,description,vis+' tag = SOV',availability,P+'commit_draft = yes',effect_preview(f,conditional_target=True))
        text+=decision('submit_'+f.key,'Submit Annual Proposal: '+f.name,'The republican council offers this commission to the Soviet planning authorities. Confirmation is required before the annual obligation and financial assistance begin.',vis+' NOT = { tag = SOV }',target,P+'commit_draft = yes',effect_preview(f))
    write('common/decisions/COLDWAR_UNION_orders_prepare.txt',block(P+'prepare',text))


def make_submissions():
    text=''
    for tag in TAGS:
        condition=block(tag,'OR = { '+' '.join(state_is(f,1) for f in FAMILIES)+' }')
        visible='tag = SOV '+eq(P+'review_target',0)+' '+condition
        text+=decision('review_'+tag,f'Republican Submissions: [{tag}.GetNameDef]','The republican council awaits a decision on its proposed annual commissions.',visible,'always = yes',setv(P+'review_target',tag+'.id')+P+'snapshot_proposals = yes')
    text+=decision('review_back','Return to Republican Submissions','Review the submissions of another republican council.',f'tag = SOV check_variable = {{ {P}review_target > 0 }}','always = yes',setv(P+'review_target',0))
    text+=decision('review_refresh','Review the Latest Submitted Terms','The planning office brings the selected republic\'s latest proposals before the Union commission.',f'tag = SOV check_variable = {{ {P}review_target > 0 }}',f'var:{P}review_target = {{ {P}republic = yes }}',P+'snapshot_proposals = yes')
    for f in FAMILIES:
        target=f'FROM = {{ {state_is(f,1)} check_variable = {{ ROOT.{P}review_target = THIS.id }} }}'
        vis='tag = SOV '+target
        description=f'The republican council proposes [?FROM.{var(f,"quantity")}|0] {f.name.lower()} in 365 days. The approved Union assistance is [?FROM.{var(f,"fraction")}|%3] of Soviet GDP. The full year begins on confirmation.'
        quote='FROM.'+var(f,'cost')
        current=f'FROM = {{ {proposal_review(f)} }}'
        available=target+' '+current+' OR = { FROM = { '+eq(var(f,'fraction'),0)+' } SOV = { '+at_least('treasury','FROM.'+var(f,'cost'))+' } }'
        text+=decision('approve_'+f.key,'Approve [FROM.GetNameDef]: '+f.name,description,vis,available,f'FROM = {{ {P}approve_{f.key} = yes }}',effect_preview(f,quote),True)
        text+=decision('reject_'+f.key,'Reject [FROM.GetNameDef]: '+f.name,description,vis,target+' '+current,f'FROM = {{ {P}reject_{f.key} = yes }}',targeted=True)
        text+=decision('withdraw_'+f.key,'Withdraw Proposal: '+f.name,'The republican council withdraws its unsigned commission. No assistance has been transferred and no annual obligation has begun.',f'NOT = {{ tag = SOV }} {state_is(f,1)}',state_is(f,1),P+'reject_'+f.key+' = yes')
        if f.equipment and not f.counter:
            basic=f'{state_is(f,2)} {eq(var(f,"kind"),1)} has_country_flag = {var(f,"return_pending")} {P}human_country = yes'
            selection=f'set_variable = {{ {P}return_target = FROM.id }}\n'+setv(P+'return_family',IDS[f.key])+setv(P+'return_serial','FROM.'+var(f,'serial'))
            unselected=f'FROM = {{ {basic} NOT = {{ {return_review(f)} }} }}'
            text+=decision('review_return_'+f.key,'Examine [FROM.GetNameDef] Production Return: '+f.name,'The republican council has submitted its annual production return to the Union commission.',f'tag = SOV {unselected}',unselected,selection,targeted=True)
            active=f'FROM = {{ {basic} {return_review(f)} }}'
            text+=decision('certify_'+f.key,'Certify [FROM.GetNameDef] Production: '+f.name,'The republican production return is before the Union commission. Certification accepts the submitted annual output and authorises the successful programme.',f'tag = SOV {active}',active,f'FROM = {{ {P}certify_{f.key} = yes }}',effect_preview(f,'0',award_only=True),True)
            reject_effect=f'FROM = {{ if = {{ limit = {{ {active.removeprefix("FROM = {").removesuffix("}")} }} clr_country_flag = {var(f,"return_pending")} }} }}'
            text+=decision('decline_return_'+f.key,'Return [FROM.GetNameDef] Figures for Revision: '+f.name,'The commission declines to certify these figures. The republic may submit a revised return before the original annual deadline.',f'tag = SOV {active}',active,reject_effect,targeted=True)
    write('common/decisions/COLDWAR_UNION_orders_submissions.txt',block(P+'submissions',text))


def make_register():
    text=hidden_mission(P+'shortfall_clock',OUTCOME_DAYS,f'clr_country_flag = {P}shortfall_clock\n'+P+'sync_shortfall_all = yes')
    for key,(flag,name,art,modifiers,description) in TEMPORARY_POLICIES.items():
        clock=P+'policy_clock_'+key
        text+=hidden_mission(clock,OUTCOME_DAYS,f'clr_country_flag = {clock}\n'+P+'sync_policies = yes')
        visible=f'NOT = {{ tag = SOV }} has_country_flag = {flag}'
        available=f'{P}has_live_commission = yes NOT = {{ has_country_flag = {clock} }}'
        effect=timed_flag(clock,OUTCOME_DAYS)+f'activate_mission = {clock}\n{P}sync_policies = yes'
        if key=='overtime':effect='add_stability = -0.05\n'+effect
        preview=block('effect_tooltip',('add_stability = -0.05\n' if key=='overtime' else '')+f'add_timed_idea = {{ idea = {P}policy_{key} days = {OUTCOME_DAYS} }}')
        entry=decision(key,'Dispatch the Procurement Agents' if key=='procurement_agents' else 'Order Extra Production Shifts',description,visible,available,effect,preview)
        if key=='procurement_agents':entry=entry.replace('fire_only_once = no','fire_only_once = no\ncost = 25',1)
        text+=entry
    for f in FAMILIES:
        k=f.key
        text+=hidden_mission(mission(f,'proposal'),PROPOSAL_DAYS,iff(state_is(f,1),setv(var(f,'state'),0))+f'clr_country_flag = {mission(f,"proposal")}')
        text+=hidden_mission(mission(f,'window'),PERIOD,P+'close_'+k+' = yes')
        for clock in ('success_clock','failure_clock'):
            text+=hidden_mission(mission(f,clock),OUTCOME_DAYS,f'clr_country_flag = {mission(f,clock)}\n'+P+'outcome_changed_'+k+' = yes')
        identifier=mission(f)
        loc(identifier,f.name+': [?'+var(f,'quantity')+'|0]')
        progress=('[?'+var(f,'produced')+'|0] / [?'+var(f,'quantity')+'|0] newly produced' if f.counter else 'A certified return of the agreed new production is required.' if f.equipment else 'The agreed increase must be in owned, controlled core territory.')
        loc(identifier+'_desc',f'The annual commission for {f.name.lower()} has been entered in the Union register.\n\n{progress}\n\nDelivery consignments: [?'+var(f,'delivered')+'|0] / [?'+var(f,'quantity')+'|0].\nFinancial assistance: [?'+var(f,'fraction')+'|%3] of Soviet GDP.\n\nSuccess and shortfall programmes last 180 days. AI administration cancels punitive responsibility for an unfinished commission.')
        body=f'''icon = GFX_decision_generic_factory
allowed = {{ {P}tag = yes }} activation = {{ always = no }}
visible = {{ {P}republic = yes {state_is(f,2)} }}
available = {{ custom_trigger_tooltip = {{ tooltip = {P}require_fulfilled {P}ready_{k} = yes }} }} selectable_mission = no fire_only_once = no days_mission_timeout = {PERIOD}
cancel_trigger = {{ OR = {{ {P}republic = no {P}human_country = no }} }}
cancel_effect = {{ hidden_effect = {{ {P}neutralise_{k} = yes }} }}
complete_effect = {{ {effect_preview(f, var(f,'cost'))} hidden_effect = {{ {P}succeed_{k} = yes }} }}
timeout_effect = {{ hidden_effect = {{ {P}close_{k} = yes }} }} ai_will_do = {{ base = 0 }}'''
        text+=block(identifier,body)
        if f.delivery:
            stock=at_least('num_equipment@'+f.equipment[0],'.00001')
            text+=decision('consign_'+k,'Dispatch Consignment: '+f.name,'Send available equipment to Soviet stores against this annual delivery order. Several consignments may fulfil the same order; only equipment actually received is counted.',f'NOT = {{ tag = SOV }} {state_is(f,2)} {eq(var(f,"kind"),2)}',stock,P+'deliver_'+k+' = yes')
        if f.equipment and not f.counter:
            text+=decision('return_'+k,'Submit Production Return: '+f.name,'The republican council submits its new production figures for certification by the Union commission. Imported equipment and old reserves are not new production.',f'NOT = {{ tag = SOV }} {state_is(f,2)} {eq(var(f,"kind"),1)}',f'NOT = {{ has_country_flag = {var(f,"return_pending")} }}',f'set_country_flag = {var(f,"return_pending")}')
        view=f'FROM = {{ check_variable = {{ {var(f,"state")} > 0 }} check_variable = {{ ROOT.{P}draft_target = THIS.id }} }}'
        desc=f'Status: §Y[FROM.COLDWAR_ORD_GetRecord_{k}]§!.\nAnnual quantity: [?FROM.{var(f,"quantity")}|0].\nRemaining annual window: [?FROM.days_mission_timeout@{mission(f,"window")}|0] days.\nProduction: [?FROM.{var(f,"produced")}|0].\nDelivered: [?FROM.{var(f,"delivered")}|0].\n\nAI and neutral programmes have no punitive consequences.'
        text+=decision('inspect_'+k,'[FROM.GetNameDef]: '+f.name,desc,'tag = SOV '+view,'always = no','',targeted=True)
        closed='OR = { '+' '.join(state_is(f,s) for s in (3,4,5,6))+' }'
        desc2='The original annual commission remains recorded until its deadline.\n\nStatus: §Y[COLDWAR_ORD_GetRecord_'+k+']§!.\nRemaining annual window: [?days_mission_timeout@'+mission(f,'window')+'|0] days.'
        text+=decision('record_'+k,'Annual Record: '+f.name,desc2,'NOT = { tag = SOV } '+closed,'always = no','')
    write('common/decisions/COLDWAR_UNION_orders_register.txt',block(P+'register',text))


def defined(name, rows, fallback):
    body='name = '+name+'\n'
    for condition,key in rows:
        body+=block('text',block('trigger',condition)+'localization_key = '+key)
    body+=block('text','localization_key = '+fallback)
    return block('defined_text',body)


def make_localisation():
    rows=[]
    for tag in TAGS:
        rows.append((eq(P+'draft_target',tag+'.id'),loc(P+'country_'+tag,'['+tag+'.GetNameDef]')))
    text=defined(P+'GetRecipient',rows,loc(P+'select_recipient','Select a Union republic'))
    rows=[(family_scope(f),loc(P+'family_name_'+f.key,f.name)) for f in FAMILIES]
    text+=defined(P+'GetFamily',rows,loc(P+'select_family','Select a production sector'))
    rows=[(eq(P+'draft_kind',i),loc(P+'kind_name_'+str(i),name)) for i,name in ((1,'Production quota'),(2,'Delivery order'),(3,'Construction target'))]
    text+=defined(P+'GetKind',rows,P+'kind_name_1')
    measurement=[]
    for f in FAMILIES:
        wording=('Eligible building-level increase in owned and controlled core territory.' if f.buildings else 'New production is counted in the native equipment class from the opening baseline.' if f.counter else 'The Union commission must certify the republican return for this equipment class.')
        measurement.append((family_scope(f),loc(P+'measure_'+f.key,wording)))
    text+=defined(P+'GetMeasurement',[(eq(P+'draft_kind',2),loc(P+'measure_delivery','Actual equipment consignments received by the Soviet Union.'))]+measurement,P+'select_family')
    for f in FAMILIES:
        rows=[(state_is(f,i),loc(P+'record_status_'+str(i),label)) for i,label in ((1,'Awaiting confirmation'),(2,'In progress'),(3,'Fulfilled'),(4,'Unfulfilled'),(5,'Neutral commission'),(6,'AI advisory programme'))]
        text+=defined(P+'GetRecord_'+f.key,rows,loc(P+'record_status_0','No current commission'))
    write('common/scripted_localisation/COLDWAR_UNION_orders.txt',text)
    loc(P+'assistance_heading','§YOn commitment§!')
    loc(P+'success_heading','§YOn fulfilment: all Union members§!')
    loc(P+'failure_heading','§YOn failure: all Union members§!')
    loc(P+'collective_heading','§YOn annual collective fulfilment: all Union members§!')
    loc(P+'support_debit_tt','Soviet Treasury: $RIGHT|-=3$ billion')
    loc(P+'support_credit_tt','Republican Treasury: $RIGHT|+=3$ billion')
    loc(P+'advisory_heading','§YAI advisory programme§!')
    loc(P+'require_fulfilled','The annual commission has met its fulfilment requirement.')
    write('localisation/english/COLDWAR_UNION_orders_l_english.yml','\n'.join(' '+key+':0 '+json.dumps(value,ensure_ascii=False) for key,value in LOC.items())+'\n',True)


def make_on_actions():
    text=block('on_startup',block('effect','SOV = { '+P+'bootstrap = yes }'))
    for tag in ('SOV',)+TAGS:
        body=(P+'bootstrap = yes\n' if tag=='SOV' else '')+P+'daily = yes'
        text+=block('on_daily_'+tag,block('effect',block(tag,body)))
    text+=block('on_yearly',block('effect',block('SOV',P+'settle_calendar = yes')))
    for action in ('on_subject_free','on_release_as_free','on_release_as_puppet','on_puppet'):
        text+=block(action,block('effect','ROOT = { if = { limit = { '+P+'tag = yes } '+P+'daily = yes } }'))
    write('common/on_actions/COLDWAR_UNION_orders.txt',block('on_actions',text))


def make_tokens():
    tokens={P+'shortfall_clock'}|{P+'policy_clock_'+key for key in TEMPORARY_POLICIES}
    tokens.update(mission(f,kind) for f in FAMILIES for kind in ('objective','proposal','window','success_clock','failure_clock'))
    # The native parser resolves mission-time variable suffixes before decision
    # registration. Pre-register them identically on every multiplayer client.
    write('common/synchronized_dynamic_tokens/COLDWAR_UNION_orders.txt','\n'.join(sorted(tokens)))


def main():
    make_triggers()
    make_ideas()
    make_effects()
    make_categories()
    make_prepare_decisions()
    make_submissions()
    make_register()
    make_on_actions()
    make_tokens()
    make_localisation()
    import integration
    OUTPUTS.extend(integration.install(ROOT))
    manifest={'project':'IMPERIA COLD WAR','quota_days':PERIOD,'success_days':OUTCOME_DAYS,'failure_days':OUTCOME_DAYS,'proposal_days':PROPOSAL_DAYS,'families':len(FAMILIES),'republics':list(TAGS),'outputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in OUTPUTS}}
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k not in {'outputs','republics'}}))


if __name__=='__main__':
    main()
