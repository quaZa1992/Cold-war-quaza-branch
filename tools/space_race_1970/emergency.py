# IMPERIA COLD WAR — GC campaign-wide emergency space quarantine.
"""Persist the kill switch in saves and stop work before touching any arrays.

No normal economy, missile, nuclear or state-building system is shut down.
Completed research and spent budgets are history, not reversible transactions.
"""
import ast
from functools import lru_cache
import re
from integrate import ROOT, span, save

FLAG='cw_sr_emergency_disabled'
ENABLED='NOT = { has_global_flag = '+FLAG+' }'
MARK='# IMPERIA COLD WAR — GC emergency space quarantine.'
PREFIX='cw_sr_gc_'
EXEMPT={'cw_sr_touch','cw_sr_retire_antarctica'}


@lru_cache(maxsize=1)
def reader():
    tree=ast.parse((ROOT/'tools/israel_1970/validate_content.py').read_text(encoding='utf-8'))
    ns={'re':re}
    exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'tokens','parse','values','first','walk'}],type_ignores=[]),'space_quarantine_reader','exec'),ns)
    return ns['parse'],ns['first']


def quarantine(body):
    return MARK+'\nif = { limit = { '+ENABLED+' }\n'+body.rstrip()+'\n}\n'


def node_span(source,name):
    match=re.search(r'(?<![\w])'+re.escape(name)+r'\s*=\s*\{',source)
    assert match,'Missing block '+name
    begin,end,brace=span(source[match.start():],name)
    return begin+match.start(),end+match.start(),brace+match.start()


def wrap_effect(source,name,otherwise=''):
    begin,end,brace=node_span(source,name)
    if MARK in source[brace+1:brace+160]:
        block=re.sub(r'(?m)^[ \t]+$', '',source[begin:end])
        return source[:begin]+block+source[end:]
    body=source[brace+1:end-1].rstrip()
    code=source[begin:brace+1]+'\n'+quarantine(body)
    if otherwise:code+='else = { '+otherwise+' }\n'
    return source[:begin]+code+'}'+source[end:]


def gate_block(source,name):
    begin,end,brace=span(source,name)
    if MARK in source[brace+1:brace+160]:return source
    return source[:brace+1]+'\n'+MARK+'\n'+ENABLED+'\n'+source[brace+1:]


def generated(c):
    """Single-pass guards keep a complete rebuild linear in generated size."""
    guarded=[];event_count=0
    for relative in list(c['OUTPUTS']):
        if not relative.endswith('.txt'):continue
        source=(ROOT/relative).read_text(encoding='utf-8')
        if '/scripted_effects/' in relative or '/scripted_triggers/' in relative:
            nodes=list(re.finditer(r'(?m)^(cw_sr_\w+)\s*=\s*\{',source))
            parts=[source[:nodes[0].start()]] if nodes else [source]
            for i,node in enumerate(nodes):
                stop=nodes[i+1].start() if i+1<len(nodes) else len(source)
                segment=source[node.start():stop];name=node[1];brace=segment.index('{');close=segment.rfind('}')
                if '/scripted_effects/' in relative and name not in EXEMPT and not name.startswith(PREFIX):
                    segment=segment[:brace+1]+'\n'+quarantine(segment[brace+1:close])+'}'+segment[close+1:];guarded.append(name)
                elif '/scripted_triggers/' in relative:
                    segment=segment[:brace+1]+'\n'+MARK+'\n'+ENABLED+'\n'+segment[brace+1:]
                parts.append(segment)
            source=''.join(parts)
        elif relative.startswith('events/'):
            pattern=r'(?m)^(country_event|news_event)\s*=\s*\{\s*id\s*=\s*[\w.]+'
            def gate_event(match):
                nonlocal event_count
                event_count+=1
                return match[0]+'\n'+MARK+'\ntrigger = { '+ENABLED+' }\n'
            source=re.sub(pattern,gate_event,source)
        elif relative=='common/on_actions/COLDWAR_space_race_on_actions.txt':
            for action in ['on_startup','on_daily','on_weekly']:
                begin,end,_=span(source,action);block=source[begin:end]
                block=wrap_effect(block,'effect');source=source[:begin]+block+source[end:]
        else:continue
        save(relative,source)
    return guarded,event_count


def shared():
    """Patch complete native blocks, preserving upstream credits and neighbours."""
    parse,first=reader();changed=[];native=[];guis=[]
    relative='common/scripted_effects/00_missiles_scripted_effects.txt'
    source=(ROOT/relative).read_text(encoding='utf-8')
    # Mixed inventory inheritance, nuclear fuel and missile-site configuration
    # must remain available to the ordinary military/economy systems.
    excluded={'update_missile_satellite_inventory','nuclear_reactor_fuel_consumption','add_missile_building_level','setup_missile_configuration_effect'}
    for name,_,body in parse(source):
        if not isinstance(body,list) or name.startswith('@') or name in excluded:continue
        source=wrap_effect(source,name);native.append(name)
    addition='add_dynamic_modifier = { modifier = satellite_system }'
    begin,end,_=span(source,'setup_missile_configuration_effect');block=source[begin:end]
    if MARK not in block:
        assert addition in block
        block=block.replace(addition,MARK+'\nif = { limit = { '+ENABLED+' } '+addition+' }')
        source=source[:begin]+block+source[end:]
    save(relative,source);changed.append(relative)
    relative='common/scripted_effects/00_space_automation_effects.txt'
    source=(ROOT/relative).read_text(encoding='utf-8')
    for name,_,body in parse(source):
        if not isinstance(body,list) or name.startswith('@'):continue
        source=wrap_effect(source,name,'set_variable = { space_prod_expense = 0 }' if name in ['space_prod_weekly_calc','space_prod_weekly_expense','space_prod_weekly_bill'] else '')
        native.append(name)
    save(relative,source);changed.append(relative)
    relative='common/scripted_effects/01_international_systems_effects.txt'
    source=(ROOT/relative).read_text(encoding='utf-8');source=wrap_effect(source,'full_satellite_system_access');save(relative,source);changed.append(relative);native.append('full_satellite_system_access')
    relative='common/scripted_triggers/00_special_projects_triggers.txt'
    source=(ROOT/relative).read_text(encoding='utf-8')
    for name in ['has_completed_space_program','has_completed_space_weapons']:source=gate_block(source,name)
    save(relative,source);changed.append(relative)
    relative='common/decisions/00_missile_decisions.txt';source=(ROOT/relative).read_text(encoding='utf-8')
    for i in range(10,15):
        name=f'missile_construction_{i}';begin,end,_=span(source,name);block=source[begin:end]
        block=wrap_effect(block,'timeout_effect')
        if 'cancel_trigger' in block:
            left,right,brace=node_span(block,'cancel_trigger')
            existing=block[brace+1:right-1]
            if FLAG not in existing:block=block[:brace+1]+'\n'+MARK+'\nOR = { has_global_flag = '+FLAG+' AND = { '+existing+' } }\n'+block[right-1:]
        else:
            brace=block.index('{');block=block[:brace+1]+'\n'+MARK+'\ncancel_trigger = { has_global_flag = '+FLAG+' }\n'+block[brace+1:]
        source=source[:begin]+block+source[end:]
    save(relative,source);changed.append(relative)
    relative='common/dynamic_modifiers/05_missiles_modifiers.txt';source=(ROOT/relative).read_text(encoding='utf-8')
    begin,end,brace=span(source,'satellite_system')
    if MARK not in source[begin:end]:source=source[:brace+1]+'\n'+MARK+'\nremove_trigger = { has_global_flag = '+FLAG+' }\n'+source[brace+1:]
    save(relative,source);changed.append(relative)
    relative='common/scripted_guis/00_missiles_scripted_guis.txt';source=(ROOT/relative).read_text(encoding='utf-8')
    for name,_,body in first(parse(source),'scripted_gui'):
        visible=first(body,'visible',[])
        # All native orbital production, launch, network, target-selection and
        # access windows have this donor route. Audit the whole GUI, not keywords
        # in isolated callback hunks.
        begin,end,_=span(source,name);block=source[begin:end]
        raw_visible=block[span(block,'visible')[0]:span(block,'visible')[1]] if visible else ''
        orbital=('var_open_MD_space_gui' in raw_visible or 'open_MD_select_satellite_system_window' in raw_visible)
        if orbital:
            block=gate_block(block,'visible');guis.append(name)
            for callback,_,effect_body in first(body,'effects',[]):block=wrap_effect(block,callback)
        # Preserve the shared military menu and its non-orbital ledgers.
        if name=='MD_missiles_gui':
            if any(k=='icon_space_gui_ledger_visible' for k,_,v in first(body,'triggers',[])):
                left,right,_=span(block,'icon_space_gui_ledger_visible');block=block[:left]+block[right:]
            for callback in ['space_gui_ledger_button_click','antarctica_gui_ledger_button_click']:block=wrap_effect(block,callback)
            for widget in ['space_gui_ledger_button','icon_ledger_btn_1','antarctica_gui_ledger_button','icon_antarctica_gui_ledger']:
                key=widget+'_visible'
                if any(k==key for k,_,v in first(body,'triggers',[])):block=gate_block(block,key)
                else:
                    _,_,brace=span(block,'triggers');block=block[:brace+1]+'\n'+MARK+'\n'+key+' = { '+ENABLED+' }\n'+block[brace+1:]
            block=gate_block(block,'antarctica_gui_ledger_button_click_enabled')
        source=source[:begin]+block+source[end:]
    save(relative,source);changed.append(relative)
    # Native delayed satellite GUI events must not re-open or refresh the network.
    relative='events/missiles_events.txt';source=(ROOT/relative).read_text(encoding='utf-8')
    for name,_,body in parse(source):
        if name not in ['country_event','news_event'] or first(body,'id') not in ['satellites.9','satellites.10']:continue
        ident=first(body,'id');match=re.search(r'(?m)^country_event\s*=\s*\{\s*id\s*=\s*'+re.escape(ident)+r'\b',source)
        assert match;tail=source[match.start():];begin,end,_=span(tail,'country_event');block=wrap_effect(tail[begin:end],'immediate');source=source[:match.start()+begin]+block+tail[end:]
    save(relative,source);changed.append(relative)
    return changed,native,guis


def build(c):
    sv,cv,block_if,effect=(c[k] for k in ['sv','cv','block_if','effect'])
    cleanup=''
    for flag in ['cw_sr_open','cw_sr_policy_open','cw_sr_requirements_open','cw_sr_leader','cw_sr_ranked','cw_sr_crew_invitation_open','cw_sr_op_invitation_open','open_MD_select_satellite_system_window','open_MD_satellite_orbit_country_selection','open_MD_space_gui','rods_search_target','space_auto_active']+[f'space_auto_line_{i}' for i in range(10,15)]:cleanup+='clr_country_flag = '+flag+'\n'
    for key in ['var_open_MD_space_gui','var_open_MD_antarctica_gui','var_open_MD_missiles_gui_ledger_4','var_open_MD_missiles_gui_ledger_5','cw_sr_active','cw_sr_demand','cw_sr_flights','cw_sr_weekly_upkeep_m','cw_sr_week_spent','space_prod_expense','cw_sr_crew_pending_prestige','cw_sr_crew_pending_science','cw_sr_crew_pending_pp','cw_sr_op_pending_prestige','cw_sr_op_pending_science','cw_sr_op_pending_pp']:
        cleanup+=sv(key,0)
    for key in ['host','programme','slot','status','weeks','expires','serial']:cleanup+=sv('cw_sr_crew_'+key,0)
    from cooperation import ORDERS,order,field
    from crew import slots,field as seat
    for w in ORDERS:
        for key in ['host','programme','role','status','weeks','expires','serial','contribution','fee','required','weekly_m']:cleanup+=sv(order(w,key),0)
    for n,p in enumerate(c['PROGRAMMES'],1):
        cleanup+=f'clr_country_flag = cw_sr_p{n}_deployed\n'+sv(f'cw_sr_p{n}_crew_recorded',0)
        for s in slots(p):
            for key in ['country','status']:cleanup+=sv(seat(n,s,key),0)
        for key in ['country','status','recorded']:cleanup+=sv(field(n,key),0)
        for prefix in ['cw_sr_crew_pending_','cw_sr_op_pending_']:cleanup+=f'clr_country_flag = {prefix}cw_sr_p{n}_name\n'
    for m,_ in enumerate(c['DATA']['milestones'],1):
        for prefix in ['cw_sr_crew_pending_','cw_sr_op_pending_']:cleanup+=f'clr_country_flag = {prefix}cw_sr_milestone_{m}\n'
    for i in range(10,15):cleanup+=block_if(f'has_active_mission = missile_construction_{i}',f'remove_mission = missile_construction_{i}\n')
    cleanup+=block_if('has_dynamic_modifier = satellite_system','remove_dynamic_modifier = { modifier = satellite_system }\n')+'cw_sr_retire_antarctica = yes\n'
    fx=effect('cw_sr_gc_quarantine_country',block_if('has_global_flag = '+FLAG,cleanup))
    auth='is_ai = no has_idea = imp_gc_nation '+ENABLED
    body='set_global_flag = '+FLAG+'\nevery_country = { cw_sr_gc_quarantine_country = yes }\n'
    for i in [1,2,3]:body+=block_if(f'has_event_target = cw_sr_rank{i}',f'clear_global_event_target = cw_sr_rank{i}\n')+sv(f'global.cw_sr_score{i}',0)
    body+=sv('global.cw_sr_ties',0)+'cw_sr_touch = yes\ninternational_systems_update = yes\n'
    fx+=effect('cw_sr_gc_emergency_shutdown',block_if(auth,body))
    c['write']('common/scripted_effects/COLDWAR_space_race_emergency.txt',fx)
    decision='''imp_gc_tools_decisions = {
    cw_sr_gc_emergency_shutdown_decision = {
        icon = GFX_decision_imp_list
        cost = 0
        fire_only_once = no
        visible = { is_ai = no has_idea = imp_gc_nation has_country_flag = imp_gc_tools_show_perf_decisions }
        available = { hidden_trigger = { is_ai = no has_idea = imp_gc_nation } custom_trigger_tooltip = { tooltip = cw_sr_gc_operations_enabled NOT = { has_global_flag = cw_sr_emergency_disabled } } }
        complete_effect = { hidden_effect = { cw_sr_gc_emergency_shutdown = yes } }
        ai_will_do = { factor = 0 }
    }
}
'''
    c['write']('common/decisions/COLDWAR_space_race_emergency.txt',decision)
    # The quarantine is deliberately one-way for this save. Re-enabling partial
    # manifests, expired events and cancelled production would not be a safe fix.
    c['loc']('cw_sr_gc_operations_enabled','Space operations are enabled')
    c['loc']('cw_sr_gc_emergency_shutdown_decision','Emergency: Disable Space Operations Worldwide')
    c['loc']('cw_sr_gc_emergency_shutdown_decision_desc','Use only if space activity threatens campaign stability. The Game Controller immediately closes Space Race and orbital services worldwide for the remainder of this campaign.\n\nSpace production and international work orders are cancelled. Programme activity, new mission outcomes, space payments and satellite service bonuses stop. Existing research, historical records, spent funds and ordinary military systems are retained.\n\nThis shutdown persists after saving, loading and player changes. It cannot be reversed through the decision menu.')
    return shared()
