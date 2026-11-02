# IMPERIA COLD WAR — COMECON authoritative contract lifecycle
from build import *

def each(s,body):return f'for_each_scope_loop = {{ array = global.cc_members {body} }}'
def participants(s,body):
    return f'if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase > 0 }} }} for_each_scope_loop = {{ array = global.cc_{s}_payers {body} }} }} else = {{ '+each(s,f'if = {{ limit = {{ cc_{s}_participant = yes }} {body} }}')+' }'
def recipients(s,body):return f'for_each_scope_loop = {{ array = global.cc_{s}_receivers {body} }}'
def refresh(s):return recipients(s,'cc_refresh_country = yes')

def compile_mechanics(out):
    startup=[f'if = {{ limit = {{ NOT = {{ has_global_flag = cc_initialized }} date < 1992.1.1 country_exists = SOV }} set_global_flag = cc_initialized set_variable = {{ global.cc_dirty = 1 }} add_to_array = {{ global.cc_union_hosts = SOV }}']
    for tag in FOUNDERS:
        startup.append(f'{tag} = {{ if = {{ limit = {{ exists = yes }} add_ideas = cc_member add_to_array = {{ global.cc_members = THIS }} add_to_array = {{ global.cc_hosts = THIS }} }} }}')
    for tag in SSRS:
        startup.append(f'{tag} = {{ if = {{ limit = {{ COLDWAR_SOV_is_union_republic = yes }} add_to_array = {{ global.cc_hosts = THIS }} add_to_array = {{ global.cc_union_hosts = THIS }} }} }}')
    startup.append('cc_update_authority = yes')
    for s in range(1,5):
        startup += [var(f'global.cc_{s}_host','HUN.id'),var(f'global.cc_{s}_union','SOV.id'),var(f'global.cc_{s}_owner','HUN.id'),var(f'global.cc_{s}_offer',1),var(f'global.cc_{s}_tier',1),var(f'global.cc_{s}_revision',1)]
        startup.append(f'SOV = {{ set_variable = {{ cc_{s}_host_index = 1 }} }}')
        startup.append(f'if = {{ limit = {{ NOT = {{ check_variable = {{ global.cc_chair = 0 }} }} }} var:global.cc_chair = {{ set_variable = {{ cc_{s}_share = 100 }} }} }}')
    startup += ['every_country = { capital_scope = { '+ ' '.join(f'set_variable = {{ PREV.cc_{s}_site1 = THIS.id }}' for s in range(1,5))+' } }','cc_rebuild_hub_sites = yes set_global_flag = cc_safety_v2','} cc_update_authority = yes cc_migrate_safety = yes']
    for s in range(1,5):startup.append(f'if = {{ limit = {{ has_global_flag = cc_initialized }} cc_{s}_rebuild = yes }}')
    startup.append('cc_election_initialize = yes')
    out.append(block('cc_initialize','\n'.join(startup)))
    out.append(block('cc_sync_members','''CUB = { if = { limit = { has_idea = COLDWAR_CUB_cmea_member NOT = { is_in_array = { global.cc_members = THIS } } } add_to_array = { global.cc_members = THIS } add_to_array = { global.cc_hosts = THIS } cc_touch = yes } }'''))
    on=[MARK+' one organisation clock, human authority and passive AI recipients','on_actions = { on_startup = { effect = { SOV = { cc_initialize = yes } } }',
       'on_weekly = { effect = { if = { limit = { NOT = { cc_clock_alive = yes } cc_member_country = yes } cc_update_authority = yes } if = { limit = { check_variable = { THIS.id = global.cc_clock } } cc_update_authority = yes cc_sync_members = yes clr_global_flag = cc_clock_absent']
    for s in range(1,5):on.append(f'if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase > 1 }} check_variable = {{ global.cc_{s}_phase < 4 }} }} cc_{s}_check_operating = yes }}')
    on.append('} else_if = { limit = { has_global_flag = cc_initialized NOT = { cc_clock_alive = yes } NOT = { has_global_flag = cc_clock_absent } OR = { '+' '.join(f'has_country_flag = cc_{s}_beneficiary' for s in range(1,5))+' } } set_global_flag = cc_clock_absent '+' '.join(f'set_variable = {{ global.cc_{s}_operating = 0 }} set_variable = {{ global.cc_{s}_valid = 0 }} {refresh(s)}' for s in range(1,5))+' cc_touch = yes } } } on_daily = { effect = { if = { limit = { NOT = { has_global_flag = cc_safety_v2 } OR = { tag = SOV cc_human_member = yes } } cc_initialize = yes } if = { limit = { check_variable = { THIS.id = global.cc_clock } has_global_flag = cc_initialized } cc_election_tick = yes')
    for s in range(1,5):on.append(f'cc_{s}_guard_controllers = yes cc_{s}_daily = yes')
    on.append('} } } }');write('common/on_actions/zzzzzzzz_ICW_COMECON.txt','\n'.join(on))
    for s in range(1,5):
        train_index=next(i for i,(p,o) in enumerate(OFFERS,1) if o['kind']=='equipment')
        stock=[var(f'global.cc_{s}_train_need',0),recipients(s,var(f'cc_{s}_train_quota',0))]
        for t in range(1,4):
            stock.append(choose(f'global.cc_{s}_tier',t,participants(s,f'''if = {{ limit = {{ NOT = {{ check_variable = {{ THIS.id = global.cc_{s}_owner }} }} }}
set_variable = {{ cc_{s}_train_quota = cc_{s}_share }} divide_variable = {{ cc_{s}_train_quota = 5 }} multiply_variable = {{ cc_{s}_train_quota = {t} }}
add_to_variable = {{ global.cc_{s}_train_need = cc_{s}_train_quota }}
var:cc_{s}_recipient = {{ set_variable = {{ cc_{s}_train_quota = PREV.cc_{s}_train_quota }} }} }}''')))
        stock += [var(f'global.cc_{s}_train_negative',f'global.cc_{s}_train_need'),f'multiply_variable = {{ global.cc_{s}_train_negative = -1 }}',var(f'global.cc_{s}_train_threshold',f'global.cc_{s}_train_need'),f'subtract_from_variable = {{ global.cc_{s}_train_threshold = 1 }}',f'var:global.cc_{s}_host = {{ if = {{ limit = {{ NOT = {{ has_equipment = {{ mdcw_steam_train_equipment_1940 > global.cc_{s}_train_threshold }} }} }} add_to_variable = {{ global.cc_{s}_invalid = 1 }} }} }}']
        out.append(block(f'cc_{s}_check_train_stock',choose(f'global.cc_{s}_offer',train_index,'\n'.join(stock))))
        calc=[var(f'global.cc_{s}_coverage',0),var(f'global.cc_{s}_participants',0),var(f'global.cc_{s}_founding',0),var(f'global.cc_{s}_owner',f'global.cc_{s}_host'),
          f'clear_array = global.cc_{s}_receivers clear_array = global.cc_{s}_parties',
          f'var:global.cc_{s}_host = {{ if = {{ limit = {{ COLDWAR_SOV_is_union_republic = yes }} set_variable = {{ global.cc_{s}_owner = SOV.id }} }} }}',
          each(s,f'''set_variable = {{ cc_{s}_recipient = THIS.id }}
if = {{ limit = {{ tag = SOV }} set_variable = {{ cc_{s}_recipient = global.cc_{s}_union }} if = {{ limit = {{ check_variable = {{ global.cc_{s}_owner = SOV.id }} }} set_variable = {{ cc_{s}_recipient = global.cc_{s}_host }} }} }}
if = {{ limit = {{ cc_{s}_participant = yes }} add_to_variable = {{ global.cc_{s}_coverage = cc_{s}_share }} add_to_variable = {{ global.cc_{s}_participants = 1 }} add_to_array = {{ global.cc_{s}_parties = THIS }}
var:cc_{s}_recipient = {{ if = {{ limit = {{ NOT = {{ is_in_array = {{ array = global.cc_{s}_receivers value = THIS }} }} }} add_to_array = {{ global.cc_{s}_receivers = THIS }} }} }} }}'''),
          f'var:global.cc_{s}_host = {{ if = {{ limit = {{ cc_access = yes NOT = {{ is_in_array = {{ array = global.cc_{s}_receivers value = THIS }} }} }} add_to_array = {{ global.cc_{s}_receivers = THIS }} }} }}',
          recipients(s,f'if = {{ limit = {{ NOT = {{ is_in_array = {{ array = global.cc_{s}_parties value = THIS }} }} }} add_to_array = {{ global.cc_{s}_parties = THIS }} }}'),
          var(f'global.cc_{s}_receiver_count',f'global.cc_{s}_receivers^num')]
        for i,(p,o) in enumerate(OFFERS,1):
            for t in range(3):
                days=180 if DATA['catalogue'][p].get('campaign') else 90
                base=(o.get('base') or DATA['catalogue'][p]['cost'])[t]/1000
                same=o['kind']=='shared' or o.get('all') or o.get('includeHost')
                body=[var(f'global.cc_{s}_days',days),var(f'global.cc_{s}_campaign',int(days==180)),var(f'global.cc_{s}_base',base),var(f'global.cc_{s}_extra',o['extra'][t]/1000),var(f'global.cc_{s}_recipients',f'global.cc_{s}_receiver_count')]
                body.append(var(f'global.cc_{s}_project',PROJECTS.index(p)+1))
                if DATA['catalogue'][p].get('institution'):body.append(f'if = {{ limit = {{ NOT = {{ has_global_flag = cc_founded_{p} }} }} set_variable = {{ global.cc_{s}_founding = 1 }} }}')
                if not same:body.append(f'subtract_from_variable = {{ global.cc_{s}_recipients = 1 }}')
                body += [f'clamp_variable = {{ var = global.cc_{s}_recipients min = 0 max = 32 }}',var(f'global.cc_{s}_cost',f'global.cc_{s}_recipients'),f'multiply_variable = {{ global.cc_{s}_cost = global.cc_{s}_extra }} add_to_variable = {{ global.cc_{s}_cost = global.cc_{s}_base }}',var(f'global.cc_{s}_weekly',f'global.cc_{s}_cost'),f'multiply_variable = {{ global.cc_{s}_weekly = 7 }} divide_variable = {{ global.cc_{s}_weekly = global.cc_{s}_days }}']
                calc.append(choose(f'global.cc_{s}_offer',i,choose(f'global.cc_{s}_tier',t+1,' '.join(body))))
        calc.append(each(s,f'''set_variable = {{ cc_{s}_weekly = global.cc_{s}_weekly }} multiply_variable = {{ cc_{s}_weekly = cc_{s}_share }} divide_variable = {{ cc_{s}_weekly = 100 }} set_variable = {{ cc_{s}_weekly_negative = cc_{s}_weekly }} multiply_variable = {{ cc_{s}_weekly_negative = -1 }}'''))
        calc.append(each(s,f'set_variable = {{ cc_{s}_quoted_share = global.cc_{s}_cost }} multiply_variable = {{ cc_{s}_quoted_share = cc_{s}_share }} divide_variable = {{ cc_{s}_quoted_share = 100 }}'))
        out.append(block(f'cc_{s}_rebuild',f'if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase = 0 }} }} '+'\n'.join(calc)+f' }} cc_{s}_check_readiness = yes cc_{s}_check_train_stock = yes cc_{s}_prepare_cards = yes cc_touch = yes'))
        # No money or approvals are changed by rebuilding display data.
        out.append(block(f'cc_{s}_revise',f'add_to_variable = {{ global.cc_{s}_revision = 1 }} cc_{s}_rebuild = yes'))
        # All pairs are checked in both directions, including the mirrored sanction arrays.
        arrays=[f'imp_{kind}_sanc_{direction}' for kind in ('dip','fin','eco','mil') for direction in ('on_us','by_us')]
        pair='NOT = { has_war_with = event_target:cc_counterpart } NOT = { is_embargoing = event_target:cc_counterpart } '
        pair+=' '.join('NOT = { is_in_array = { array = '+a+' value = event_target:cc_counterpart } }' for a in arrays)
        validation=[var(f'global.cc_{s}_valid',1),participants(s,f'''if = {{ limit = {{ NOT = {{ cc_member_country = yes cc_{s}_allocation_valid = yes }} }} set_variable = {{ global.cc_{s}_valid = 0 }} }}
if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase < 3 }} NOT = {{ cc_human_member = yes }} }} set_variable = {{ global.cc_{s}_valid = 0 }} }}
if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase > 0 }} check_variable = {{ global.cc_{s}_phase < 3 }} NOT = {{ cc_{s}_signed = yes }} }} set_variable = {{ global.cc_{s}_valid = 0 }} }}'''),
          recipients(s,f'''if = {{ limit = {{ NOT = {{ cc_access = yes cc_{s}_target_operating = yes }} }} set_variable = {{ global.cc_{s}_valid = 0 }} }}
if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase > 0 }} NOT = {{ cc_{s}_receiver_consent = yes }} }} set_variable = {{ global.cc_{s}_valid = 0 }} }}'''),
          f'for_each_scope_loop = {{ array = global.cc_{s}_parties save_event_target_as = cc_counterpart for_each_scope_loop = {{ array = global.cc_{s}_parties if = {{ limit = {{ NOT = {{ {pair} }} }} set_variable = {{ global.cc_{s}_valid = 0 }} }} }} }}']
        out.append(block(f'cc_{s}_validate_partners','\n'.join(validation)))
        operating=f'''cc_{s}_validate_partners = yes
if = {{ limit = {{ check_variable = {{ global.cc_{s}_valid = 0 }} }} set_variable = {{ global.cc_{s}_operating = 0 }} }}
else_if = {{ limit = {{ OR = {{ check_variable = {{ global.cc_{s}_phase = 3 }} AND = {{ check_variable = {{ global.cc_{s}_campaign = 1 }} check_variable = {{ global.cc_{s}_period_left > 0 }} }} }} }} set_variable = {{ global.cc_{s}_operating = 1 }} }}
else = {{ set_variable = {{ global.cc_{s}_operating = 0 }} }}
{refresh(s)} cc_touch = yes'''
        out.append(block(f'cc_{s}_check_operating',operating))
        # Compute every invoice before charging any payer. The final invoice settles exact remaining liability.
        prepay=[f'cc_{s}_validate_partners = yes',var(f'global.cc_{s}_period',f'global.cc_{s}_remaining'),f'clamp_variable = {{ var = global.cc_{s}_period min = 0 max = 7 }}']
        prepay.append(participants(s,f'''set_variable = {{ cc_{s}_invoice = cc_{s}_weekly }}
if = {{ limit = {{ check_variable = {{ global.cc_{s}_remaining < 8 }} }} set_variable = {{ cc_{s}_invoice = cc_{s}_liability }} subtract_from_variable = {{ cc_{s}_invoice = cc_{s}_paid }} }}
if = {{ limit = {{ OR = {{ has_country_flag = MD_skip_treasury_cost check_variable = {{ treasury < cc_{s}_invoice }} }} }} set_variable = {{ global.cc_{s}_valid = 0 }} }}'''))
        prepay.append(f'''if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase = 2 }} check_variable = {{ global.cc_{s}_valid = 1 }} check_variable = {{ global.cc_{s}_period > 0 }} check_variable = {{ global.cc_{s}_period_left = 0 }} }}
{participants(s,f'set_temp_variable = {{ treasury_change = cc_{s}_invoice }} multiply_temp_variable = {{ treasury_change = -1 }} modify_treasury_effect = yes add_to_variable = {{ cc_{s}_paid = cc_{s}_invoice }}')}
set_variable = {{ global.cc_{s}_period_left = global.cc_{s}_period }}
{''.join(choose(f'global.cc_{s}_offer',i,f'if = {{ limit = {{ NOT = {{ has_global_flag = cc_founded_{p} }} }} set_global_flag = cc_founded_{p} }}') for i,(p,o) in enumerate(OFFERS,1) if DATA['catalogue'][p].get('institution'))}
}} cc_{s}_check_operating = yes''')
        out.append(block(f'cc_{s}_prepay','\n'.join(prepay)))
        start=f'''if = {{ limit = {{ cc_human_member = yes }} cc_update_authority = yes cc_{s}_rebuild = yes
if = {{ limit = {{ cc_{s}_can_ratify = yes }} cc_{s}_validate_partners = yes
if = {{ limit = {{ check_variable = {{ global.cc_{s}_valid = 1 }} }}
set_variable = {{ global.cc_{s}_phase = 2 }} set_variable = {{ global.cc_{s}_remaining = global.cc_{s}_days }} set_variable = {{ global.cc_{s}_period_left = 0 }}
{participants(s,f'set_variable = {{ cc_{s}_liability = global.cc_{s}_cost }} multiply_variable = {{ cc_{s}_liability = cc_{s}_share }} divide_variable = {{ cc_{s}_liability = 100 }} set_variable = {{ cc_{s}_paid = 0 }}')}
{recipients(s,f'set_country_flag = cc_{s}_beneficiary')}
cc_{s}_prepay = yes }} }} }}'''
        out.append(block(f'cc_{s}_ratify',start))
        # Completion uses a fresh full asset check before any participant receives an asset.
        delivery=[f'if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase = 2 }} check_variable = {{ global.cc_{s}_remaining = 0 }} }}',f'cc_{s}_rebuild = yes cc_{s}_validate_partners = yes',
          f'if = {{ limit = {{ check_variable = {{ global.cc_{s}_valid = 1 }} check_variable = {{ global.cc_{s}_invalid = 0 }} }}']
        deliveries=[]
        for i,(p,o) in enumerate(OFFERS,1):
            if DATA['catalogue'][p].get('campaign'):continue
            for t in range(3):
                hb=assets(s,p,o,t,True);pb=assets(s,p,o,t,False)
                body=f'if = {{ limit = {{ {cv("THIS.id","=",f"global.cc_{s}_host")} }} {hb} }} else = {{ {pb} }}'
                deliveries.append(choose(f'global.cc_{s}_offer',i,choose(f'global.cc_{s}_tier',t+1,body)))
        delivery.append(recipients(s,f'if = {{ limit = {{ NOT = {{ check_variable = {{ cc_{s}_delivered_revision = global.cc_{s}_revision }} }} }} '+'\n'.join(deliveries)+f' set_variable = {{ cc_{s}_delivered_revision = global.cc_{s}_revision }} }}'))
        delivery += [f'''if = {{ limit = {{ check_variable = {{ global.cc_{s}_campaign = 1 }} }} set_variable = {{ global.cc_{s}_phase = 4 }} set_variable = {{ global.cc_{s}_operating = 0 }} }}
else = {{ set_variable = {{ global.cc_{s}_phase = 3 }} set_variable = {{ global.cc_{s}_remaining = 90 }} set_variable = {{ global.cc_{s}_operating = 1 }} }}
{refresh(s)} cc_touch = yes''','} }']
        out.append(block(f'cc_{s}_complete','\n'.join(delivery)))
        daily=f'''if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase = 2 }} check_variable = {{ global.cc_{s}_valid = 1 }} check_variable = {{ global.cc_{s}_period_left > 0 }} }}
subtract_from_variable = {{ global.cc_{s}_period_left = 1 }} subtract_from_variable = {{ global.cc_{s}_remaining = 1 }}
if = {{ limit = {{ check_variable = {{ global.cc_{s}_remaining = 0 }} }} cc_{s}_complete = yes }}
else_if = {{ limit = {{ check_variable = {{ global.cc_{s}_period_left = 0 }} }} cc_{s}_prepay = yes }} }}
else_if = {{ limit = {{ check_variable = {{ global.cc_{s}_phase = 3 }} check_variable = {{ global.cc_{s}_valid = 1 }} }}
subtract_from_variable = {{ global.cc_{s}_remaining = 1 }}
if = {{ limit = {{ check_variable = {{ global.cc_{s}_remaining < 1 }} }} set_variable = {{ global.cc_{s}_phase = 4 }} set_variable = {{ global.cc_{s}_operating = 0 }} {refresh(s)} cc_touch = yes }} }}'''
        out.append(block(f'cc_{s}_daily',daily))
        out.append(block(f'cc_{s}_resume',f'if = {{ limit = {{ cc_secretariat = yes check_variable = {{ global.cc_{s}_phase = 2 }} check_variable = {{ global.cc_{s}_period_left = 0 }} }} cc_{s}_prepay = yes if = {{ limit = {{ check_variable = {{ global.cc_{s}_remaining = 0 }} }} cc_{s}_complete = yes }} }}'))
        out.append(block(f'cc_{s}_reset',f'''if = {{ limit = {{ cc_secretariat = yes OR = {{ check_variable = {{ global.cc_{s}_phase = 0 }} check_variable = {{ global.cc_{s}_phase = 4 }} }} }}
{recipients(s,f'clr_country_flag = cc_{s}_beneficiary cc_refresh_country = yes')}
set_variable = {{ global.cc_{s}_phase = 0 }} set_variable = {{ global.cc_{s}_remaining = 0 }} set_variable = {{ global.cc_{s}_operating = 0 }} cc_{s}_revise = yes }}'''))
    from governance import compile_governance
    compile_governance(out)
    compile_decisions()

def compile_decisions():
    from actions import compile_decisions as emit
    emit()
