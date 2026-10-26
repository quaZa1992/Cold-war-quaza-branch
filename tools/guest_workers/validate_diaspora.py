# IMPERIA CW — Cold War: Guest Worker Administration
"""Execute the authored diaspora scripts and inspect native UI/budget wiring.

Uses the existing strict script interpreter. This does not emulate HOI4 rendering,
RNG or its closed-source manpower recalculation. Observed reserve artifacts are
injected explicitly; no assertion here is an in-game performance benchmark.
"""
from copy import deepcopy
import json
from pathlib import Path
import re
import struct
import sys

import validate as V

D, first, values, walk, check = V.D, V.first, V.values, V.walk, V.check
ROOT = V.ROOT


def load():
    effects = {}
    for path in [ROOT/'common/scripted_effects/mdcw_guest_workers_effects.txt',
                 *sorted((ROOT/'common/scripted_effects').glob('mdcw_diaspora*.txt'))]:
        effects.update({k:v for k,_,v in V.read_script(path.relative_to(ROOT).as_posix())})
    triggers = {}
    # IMPERIA CW — Cold War: include generated Ministry transaction guards.
    for name in ('mdcw_guest_workers_triggers', 'mdcw_guest_workers_ai_triggers', 'mdcw_diaspora_triggers', 'mdcw_diaspora_dashboard_triggers', 'mdcw_diaspora_policy_triggers'):
        triggers.update({k:v for k,_,v in V.read_script('common/scripted_triggers/'+name+'.txt')})
    events = {}
    for name in ('mdcw_guest_workers_events', 'mdcw_diaspora_events', 'mdcw_diaspora_policy_events'):
        events.update({first(v,'id'):v for k,_,v in V.read_script('events/'+name+'.txt') if k=='country_event'})
    return effects,triggers,events


def fixture(data, amount=100, population=20_000_000):
    m=V.ScriptMachine(*data)
    m.root.states[0].population=D(population)
    m.root.variables.update(gdp_total=D(200), population_total=D(population)/100000,
                            mdcw_gw_guest_workers_k=D(0),mdcw_gw_net_emigration_k=-D(amount))
    m.origin.variables.update(gw_abroad_k=D(amount),mdcw_gw_remittance_pool_m=D(400),mdcw_gw_net_emigration_k=D(amount))
    m.call('mdcw_gw_ledger_initialize')
    m.root.variables['gw_selected_origin']=D(2)
    m.root.temporary['gw_lookup_origin']=D(2)
    m.call('mdcw_gw_ensure_origin')
    m.execute([('set_variable','=', [('gw_stock^gw_index','=',str(amount))])])
    m.call('mdcw_gw_recount_ledger')
    m.call('mdcw_gw_update_resident_costs')
    # IMPERIA CW — Cold War: Management fixtures represent recent arrivals in an
    # established migration year. Dedicated policy tests exercise eligible returns.
    m.root.variables['gw_return_basis^0']=D(0)
    return m


def core(m):
    return deepcopy([(c.tag,c.variables,c.political_power,c.military_manpower,c.stability,
                      [(s.population,s.owner,s.controller) for s in c.states]) for c in m.countries.values()])


def resources(m):
    """Economic resources and coverage; selection/preview/dirty caches may refresh."""
    return deepcopy([(c.tag,c.variables.get('treasury'),c.political_power,c.military_manpower,
                      c.stability,[(k,v) for k,v in c.variables.items() if k.startswith(
                          ('gw_stock^','gw_registered^','gw_housed^','gw_protected^'))],
                      [(s.population,s.owner,s.controller) for s in c.states]) for c in m.countries.values()])


def close_tests(data):
    ideas=first(V.read_script('common/ideas/mdcw_guest_workers_ideas.txt'),'ideas',[])
    receiving=first(first(ideas,'imp_national_ideas_2',[]),'mdcw_ni_guest_worker_recruitment_programme',[])
    gate=first(receiving,'allowed_to_remove',[])
    m=fixture(data)
    check(not m.test(gate),'Positive-stock recipient is removable immediately')
    m.advance_days(1460)
    check(not m.test(gate),'Four years makes retained residents removable')
    m.root.variables['mdcw_gw_guest_workers_k']=D(0)
    check(m.test(gate),'Zero-stock recipient cannot be removed')
    for flag in ('gw_project_active','gw_return_active','mdcw_gw_request_pending','mdcw_gw_offer_pending','mdcw_gw_offer_window_open'):
        m.root.flags[flag]=D(0)
        check(not m.test(gate),'Removal bypasses active transaction: '+flag)
        m.root.flags.pop(flag)


def project_tests(data):
    # Preview and actual charges must agree across small groups and both CG caps.
    for amount in (25, 50, 100, 1000, 2000, 20000):
        for choice, fee, cg, cap in ((1, '.030', '.01', '.15'), (2, '.050', '.02', '.25'),
                                    (3, '.040', '.01', '.15')):
            sample = fixture(data, amount)
            sample.root.variables['gw_project_choice'] = D(choice)
            sample.call('mdcw_gw_prepare_project')
            expected_cash = D(amount) / 100 * D(fee)
            expected_cg = min(D(amount) / 100 * D(cg), D(cap))
            check(sample.get('gw_project_preview_weekly') == expected_cash
                  and sample.get('gw_project_preview_consumer') == expected_cg,
                  'Integration preview does not scale with untreated cohort size or the CG cap')
            sample.call('mdcw_gw_start_project')
            check(sample.get('gw_project_weekly') == expected_cash
                  and sample.get('gw_project_consumer') == expected_cg,
                  'Actual integration cost differs from the confirmed scaled price')
    for choice,pp,fee,cg,coverage in ((1,75,'.030','.01','registered'),(2,100,'.050','.02','housed'),(3,100,'.040','.01','protected')):
        m=fixture(data,1000)
        m.root.variables['gw_project_choice']=D(choice)
        before=m.root.political_power
        m.call('mdcw_gw_start_project')
        check(m.root.political_power==before-pp and m.root.variables['gw_project_covered_k']==1000,
              f'Project {choice}: wrong coverage or PP charge')
        check(m.root.variables['gw_project_weekly']==D(fee)*10 and m.root.variables['gw_project_consumer']==D(cg)*10,
              f'Project {choice}: wrong recurring expense or Consumer Goods')
        before=resources(m)
        m.call('mdcw_gw_start_project')
        check(resources(m)==before,f'Project {choice}: duplicate activation changes resources')
        # Additional arrivals during the365-day project are deliberately uncovered.
        m.root.variables['mdcw_gw_last_arrival_k']=D(100)
        m.root.states[0].population+=100000
        m.call('mdcw_gw_record_agreement')
        check(m.in_scope(m.origin,lambda:m.array_values('gw_hosts'))==[D(1)],
              'Origin does not retain a sparse list of actual receiving countries')
        m.advance_days(364)
        check(m.get(f'gw_{coverage}^0')==0 and 'gw_project_active' in m.root.flags,
              f'Project {choice}: benefit arrives before completion')
        m.advance_days(1)
        check(m.get('gw_stock^0')==1100 and m.get(f'gw_{coverage}^0')==1000,
              f'Project {choice}: late arrivals receive free integration')
        check(m.root.variables['gw_project_weekly']==0 and m.root.variables['gw_project_consumer']==0
              and 'gw_project_active' not in m.root.flags,
              f'Project {choice}: expense/Consumer Goods persist after completion')
        m.call('mdcw_gw_prepare_project')
        check(m.root.variables['gw_project_preview_k']==100,
              f'Project {choice}: a repeated programme treats already covered residents')
    m=fixture(data,1000)
    check(abs(m.root.variables['gw_welfare_weekly']-D(200)/52*D('.05')*D('.5'))<D('1e-18'),
          'Welfare does not equal weekly GDP equivalent times resident share times0.50')
    check(m.root.variables['mdcw_gw_health_cost']==D('.5')
          and m.root.variables['mdcw_gw_bureaucracy_cost']==D('1'),
          'Five-percent population example has wrong Healthcare/Administration surcharges')
    for name in ('registered','housed','protected'):
        m.root.variables[f'gw_{name}^0']=D(1000)
    m.call('mdcw_gw_recount_ledger');m.call('mdcw_gw_update_resident_costs')
    check(m.root.variables['mdcw_gw_health_cost']==D('.4')
          and m.root.variables['mdcw_gw_bureaucracy_cost']==D('.7')
          and abs(m.root.variables['gw_welfare_weekly']-D(200)/52*D('.05')*D('.5')*D('.6'))<D('1e-18'),
          'Completed programmes do not apply the agreed20/30/40-percent targeted relief')
    before=core(m);m.root.variables['gw_project_choice']=D(1);before=core(m)
    m.call('mdcw_gw_start_project')
    # Preview variables may refresh, but no paid project can start at full coverage.
    check('gw_project_active' not in m.root.flags and m.root.political_power==1000,
          'Fully covered origin can buy/stack the same benefit again')


def return_tests(data):
    for amount in (25,50,100,D('24.999'),D('.001')):
        for two_states in (False,True):
            m=fixture(data,100)
            if two_states:
                m.root.states=[V.State(population=D(60000),owner='A',controller='A'),
                               V.State(population=D(60001),owner='A',controller='A')]
            m.root.variables['gw_return_choice_k']=D(amount)
            before_pop=sum(s.population for c in m.countries.values() for s in c.states)
            host_before=sum(s.population for s in m.root.states)
            home_before=sum(s.population for s in m.origin.states)
            before_pp,before_cash=m.root.political_power,m.root.variables['treasury']
            # Explicitly inject the recorded engine reserve artifact on the first withdrawal.
            injected=[D(9219)]
            def artifact(model,state,delta):
                if delta<0 and state.owner=='A' and injected:
                    m.root.military_manpower+=injected.pop()
            m.state_population_hook=artifact
            m.call('mdcw_gw_start_return')
            check(m.root.variables['gw_stock^0']==100 and sum(s.population for s in m.root.states)==host_before,
                  'Preparation immediately moves residents')
            check(m.root.variables['treasury']==before_cash-D(amount)/100*5
                  and m.root.political_power==before_pp-D(amount),
                  'Return preparation does not charge the quoted amount once')
            # Duplicate invocation must not take another deposit or queue another return.
            before=resources(m);queued=len(m.queue);m.call('mdcw_gw_start_return')
            check(resources(m)==before and len(m.queue)==queued,'Duplicate return takes another deposit')
            m.advance_days(89)
            check(sum(s.population for s in m.root.states)==host_before,'Return happens before day90')
            m.advance_days(1)
            check(sum(s.population for s in m.root.states)==host_before-D(amount)*1000
                  and sum(s.population for s in m.origin.states)==home_before+D(amount)*1000
                  and sum(s.population for c in m.countries.values() for s in c.states)==before_pop,
                  f'Return {amount}, split={two_states}: POP is lost, created or moved to the wrong country')
            check(m.root.military_manpower==250000,'Repatriation creates an exporter reserve windfall')
            check(m.get('gw_stock^0')==100-D(amount)
                  and m.origin.variables['gw_abroad_k']==100-D(amount)
                  and m.origin.variables['mdcw_gw_remittance_pool_m']==D(400)*(1-D(amount)/100),
                  'Return ledger or proportional origin remittances are incorrect')
            if amount==100 and two_states:
                check(m.root.variables['gw_return_source_count']==2,'Two-source return did not use two actual states')
            before=core(m);m.call('mdcw_gw_execute_return')
            check(core(m)==before,'Replayed completion returns or refunds a second time')
            # Acknowledging the receipt must be read-only.
            notice=next(e for e in m.open_events if e[1]=='mdcw_diaspora.41')
            m.choose(notice,0)
            check(core(m)==before,'Return receipt acknowledgment repeats its population effects')
            if amount==25:
                m.root.variables['gw_return_choice_k']=D(50)
                m.call('mdcw_gw_start_return')
                check(m.root.variables['gw_return_receipt_k']==25 and m.root.variables['gw_return_k']==50,
                      'Starting another return overwrites the previous completed receipt')
    for failure in ('host_war','origin_war','origin_absent','no_source','no_destination','source_control','lost_stock'):
        m=fixture(data)
        m.root.variables['gw_return_choice_k']=D(100)
        before_cash,before_pp=m.root.variables['treasury'],m.root.political_power
        m.call('mdcw_gw_start_return')
        if failure=='host_war':m.root.peace=False
        elif failure=='origin_war':m.origin.peace=False
        elif failure=='origin_absent':m.origin.exists=False
        elif failure=='no_source':m.root.states.clear()
        elif failure=='no_destination':m.origin.states.clear()
        elif failure=='source_control':m.root.states[0].controller='B'
        elif failure=='lost_stock':m.root.variables['gw_stock^0']=D(50)
        before_pop=sum(s.population for c in m.countries.values() for s in c.states)
        m.advance_days(90)
        check(m.root.variables['treasury']==before_cash and m.root.political_power==before_pp
              and 'gw_return_active' not in m.root.flags
              and sum(s.population for c in m.countries.values() for s in c.states)==before_pop,
              'Invalid return fails its atomic refund: '+failure)
    # Odd headcount, two-state final return: rounded integer source1 + remainder source2.
    m=fixture(data,D('99.999'))
    m.root.states=[V.State(population=D(50000),owner='A',controller='A'),
                   V.State(population=D(49999),owner='A',controller='A')]
    m.root.variables['gw_return_choice_k']=D('99.999')
    total=sum(s.population for c in m.countries.values() for s in c.states)
    m.call('mdcw_gw_start_return');m.advance_days(90)
    check(m.get('gw_stock^0')==0 and sum(s.population for c in m.countries.values() for s in c.states)==total,
          'Odd final headcount creates/destroys fractional people or cannot close the ledger')


def diplomacy_tests(data):
    m=fixture(data)
    sender,host=m.origin,m.root
    m.event_context((m.now,'',sender,host,{}),lambda:m.call('mdcw_gw_start_outreach'))
    check(sender.variables['treasury']==D('99.5') and m.get('gw_outreach^0')==1,
          'Outreach charges the wrong country or records no bilateral link')
    m.root.temporary['tag_index']=D(2);m.root.temporary['influence_change']=D(0)
    m.call('mdcw_gw_apply_diaspora_influence')
    check(m.get('influence_change')==D('.1'),'Normal outreach gives wrong influence effectiveness')
    m.root.variables['gw_protected^0']=D(100)
    m.root.temporary['influence_change']=D(0)
    m.call('mdcw_gw_apply_diaspora_influence')
    check(m.get('influence_change')==D('.05'),'Labour integration does not halve outreach effectiveness')
    m.advance_days(180)
    check(m.get('gw_outreach^0')==0,'Outreach persists beyond180 days')
    # Employer abuse: the ignored complaint reaches the real origin; its veto
    # blocks future recruitment, and the explicit resume decision lifts it.
    m=fixture(data)
    event=(m.now,'mdcw_diaspora.61',m.root,m.root,{})
    m.choose(event,1);m.advance_days(1)
    notice=next(e for e in m.open_events if e[1]=='mdcw_diaspora.62')
    check(notice[2] is m.origin and notice[3] is m.root,'Complaint reaches the wrong origin or names the wrong host')
    m.choose(notice,0)
    check(not m.test(m.triggers['mdcw_gw_pair_not_suspended']),'Origin suspension does not block recruitment')
    m.in_scope(m.origin,lambda:m.execute([('remove_from_array','=',[('gw_suspended_hosts','=','ROOT.id')])]))
    check(m.test(m.triggers['mdcw_gw_pair_not_suspended']),'Lifting the suspension does not restore recruitment')
    # Legacy registration never fabricates POP, grants rewards or guesses a flag.
    m=V.ScriptMachine(*data);m.root.variables['mdcw_gw_guest_workers_k']=D(50)
    m.origin.variables['mdcw_gw_net_emigration_k']=D(50)
    m.in_scope(m.origin,lambda:m.call('mdcw_gw_ledger_initialize'))
    m.call('mdcw_gw_ledger_initialize')
    check(m.root.variables['gw_unrecorded_k']==50 and m.get('gw_origins^num')==0,
          'Legacy origins are invented instead of explicitly marked unknown')
    pop=sum(s.population for c in m.countries.values() for s in c.states)
    money=[c.variables['treasury'] for c in m.countries.values()]
    m.call('mdcw_gw_register_legacy_origin')
    check(m.get('gw_stock^0')==50 and m.root.variables['gw_unrecorded_k']==0
          and m.root.variables['mdcw_gw_guest_workers_k']==50
          and m.origin.variables['gw_abroad_k']==50
          and sum(s.population for c in m.countries.values() for s in c.states)==pop
          and [c.variables['treasury'] for c in m.countries.values()]==money,
          'Legacy identification changes actual population, cash or total retained stock')


def annexation_tests(data):
    for own_origin in (False,True):
        m=fixture(data)
        defeated=V.Country('C');defeated.states=[V.State(owner='A',controller='A')]
        m.countries['C']=defeated
        def seed():
            m.call('mdcw_gw_ledger_initialize')
            m.current.temporary['gw_lookup_origin']=D(1 if own_origin else 2)
            m.call('mdcw_gw_ensure_origin')
            for field,amount in [('stock',50),('registered',25),('housed',10),('protected',20)]:
                m.execute([('set_variable','=',[(f'gw_{field}^gw_index','=',str(amount))])])
            m.call('mdcw_gw_recount_ledger')
        m.in_scope(defeated,seed)
        if own_origin:
            m.root.variables.update(gw_abroad_k=D(50),mdcw_gw_remittance_pool_m=D(200),mdcw_gw_net_emigration_k=D(-50))
        else:m.origin.variables['gw_abroad_k']=D(150)
        pop=sum(s.population for c in m.countries.values() for s in c.states)
        m.event_context((m.now,'',m.root,defeated,{}),lambda:m.call('mdcw_gw_absorb_annexed_ledger'))
        check(m.root.variables['mdcw_gw_guest_workers_k']==(100 if own_origin else 150)
              and defeated.variables['mdcw_gw_guest_workers_k']==0
              and sum(s.population for c in m.countries.values() for s in c.states)==pop,
              'Annexation duplicates/deletes residents or physical population')
        check(m.root.variables['mdcw_gw_net_emigration_k']==(-100 if own_origin else -150),
              'Annexation leaves a stale net-emigration/remittance baseline')
        if own_origin:
            check(m.root.variables['gw_abroad_k']==0 and m.root.variables['mdcw_gw_remittance_pool_m']==0,
                  'Citizens returning through annexation remain foreign residents or continue remitting')
        else:
            check(m.get('gw_registered^0')==25 and m.get('gw_housed^0')==10 and m.get('gw_protected^0')==20,
                  'Annexation loses completed integration coverage')
        before=resources(m)
        m.event_context((m.now,'',m.root,defeated,{}),lambda:m.call('mdcw_gw_absorb_annexed_ledger'))
        check(resources(m)==before,'Repeated annexation duplicates cohorts or integration')


def ui_and_wiring(data):
    effects,triggers,events=data
    gui=first(V.read_script('interface/mdcw_diaspora.gui'),'guiTypes',[])
    window=first(gui,'containerWindowType',[])
    controls={first(v,'name').strip('"'):v for k,_,v in window if isinstance(v,list) and first(v,'name')}
    script=first(first(V.read_script('common/scripted_guis/mdcw_diaspora_gui.txt'),'scripted_gui',[]),'mdcw_gw_dashboard',[])
    check(first(script,'context_type')=='decision_category' and first(script,'dirty')=='gw_ui_dirty',
          'Dashboard is not a native dirty-cached decision-category GUI')
    sprites=first(V.read_script('interface/mdcw_diaspora.gfx'),'spriteTypes',[])
    for _,_,definition in sprites:
        texture=ROOT/first(definition,'texturefile').strip('"')
        check(texture.is_file(),'Missing dossier texture: '+str(texture))
        if texture.is_file():
            raw=texture.read_bytes();height,width=struct.unpack_from('<II',raw,12)
            frames=int(first(definition,'noOfFrames','1'))
            check(raw[:4]==b'DDS ' and raw[84:88]==b'\0'*4 and width%frames==0
                  and len(raw)==128+width*height*4,
                  'GUI texture does not use complete native RGBA frames: '+str(texture))
    for name,_,body in first(script,'effects',[]):
        check(name.removesuffix('_click') in controls,'Click handler has no actual UI control: '+name)
    for row in range(1,5):
        check(f'gw_row{row}_flag' in controls and f'gw_row{row}_name' in controls,'Missing flag row')
    check(not any('state' in name.lower() for name in controls),'Unrequested residence-state tracking appears in the UI')
    loc={}
    for path in (ROOT/'localisation/english').glob('mdcw_*guest*english.yml'):
        loc.update({k:json.loads(v) for k,v in re.findall(r'^ (\S+):\d+ (".*")$',path.read_text(encoding='utf-8-sig'),re.M)})
    for path in (ROOT/'localisation/english').glob('mdcw_diaspora*english.yml'):
        loc.update({k:json.loads(v) for k,v in re.findall(r'^ (\S+):\d+ (".*")$',path.read_text(encoding='utf-8-sig'),re.M)})
    for nodes in [window,script,*events.values()]:
        for key,_,value in walk(nodes):
            if key in {'text','buttonText','pdx_tooltip','title','desc','name','custom_effect_tooltip'} and isinstance(value,str):
                value=value.strip('"')
                if value.startswith(('gw_','mdcw_diaspora.')) and value not in controls:
                    check(value in loc,'Missing player-facing localisation: '+value)
            if key.startswith('mdcw_gw_') and value=='yes':
                check(key in effects or key in triggers,'Undefined native UI/event helper: '+key)
    # Exercise the actual generated UI click chain, including safe expired dialogs.
    m=fixture(data);clicks=dict((k,v) for k,_,v in first(script,'effects',[]))
    enabled=dict((k,v) for k,_,v in first(script,'triggers',[]))
    m.execute(clicks['gw_register_click'])
    m.advance_days(0)
    check(not m.test(enabled['gw_housing_click_enabled']),'A second management dialog can overwrite the first')
    offer=next(e for e in m.open_events if e[1]=='mdcw_diaspora.11')
    m.advance_days(8)
    options=values(events['mdcw_diaspora.11'],'option')
    check(m.test(first(options[0],'trigger',[])),
          'Funding disappears after seven days while the confirmation popup is still open')
    m.advance_days(6)
    check(not m.test(first(options[0],'trigger',[])),'Expired accept-first management popup can still spend resources')
    before=resources(m)
    m.execute(first(options[0],'hidden_effect',[]))
    check(resources(m)==before and 'gw_project_active' not in m.root.flags,
          'A stale native timeout bypasses the project effect guard')
    m.choose(offer,1)
    check('gw_dialog_window' not in m.root.flags,'Cancel leaves the management UI locked')
    m.execute(clicks['gw_register_click'])
    m.advance_days(0)
    offer=[e for e in m.open_events if e[1]=='mdcw_diaspora.11'][-1]
    m.choose(offer,0)
    check(m.root.political_power==925 and 'gw_project_active' in m.root.flags,
          'Actual flag-row/UI/event chain does not start one paid programme')
    expired=fixture(data)
    expired.execute(clicks['gw_return_100_click']);expired.advance_days(8)
    before=resources(expired)
    expired.execute(first(values(events['mdcw_diaspora.30'],'option')[0],'hidden_effect',[]))
    check(resources(expired)==before and 'gw_return_active' not in expired.root.flags,
          'A stale native timeout bypasses the return confirmation guard')
    # Pagination should list all origin groups without a fixed donor cap.
    m=fixture(data)
    for i in range(3,12):
        m.root.temporary['gw_lookup_origin']=D(i);m.call('mdcw_gw_ensure_origin')
        m.execute([('set_variable','=',[('gw_stock^gw_index','=','25')])])
    m.call('mdcw_gw_recount_ledger')
    seen=[]
    for page in range(3):
        for row in range(1,5):
            if m.root.variables[f'gw_row{row}_k']>0:seen.append(m.root.variables[f'gw_row{row}_origin'])
        if page<2:m.execute(clicks['gw_next_click'])
    check(len(seen)==10 and len(set(seen))==10,'Paged dashboard loses or duplicates origins')
    money=V.read_script('common/scripted_effects/00_money_system.txt')
    social=first(money,'update_social_rate',[])
    check(sum(k=='add' and v=='gw_welfare_weekly' for k,_,v in walk(social))==1,
          'Welfare charge is absent or duplicated in native spending-law previews')
    expenses=first(money,'calculate_additional_expense_rate',[])
    check(sum(k=='add_to_variable' and first(v,'additional_expenses_rate')=='gw_project_weekly' for k,_,v in walk(expenses))==1,
          'Project expense does not enter the native weekly budget exactly once')
    # Budget closure must remain constant work even with many origin groups.
    forbidden={'every_country','every_state','every_owned_state','for_each_loop','for_each_scope_loop','random_owned_state','while_loop_effect'}
    for helper in ('mdcw_gw_calculate_diaspora_costs','mdcw_gw_update_cost_receipt'):
        check(not {k for k,_,v in walk(effects[helper])}&forbidden,'Recurring budget calculation scans state/country/origin lists: '+helper)
    check(not list((ROOT/'common/scripted_effects').glob('*diaspora*state*')),'Unexpected per-state diaspora matrix')


def confirmation_dialog_tests(data):
    effects, triggers, events = data
    script = first(first(V.read_script('common/scripted_guis/mdcw_diaspora_gui.txt'), 'scripted_gui', []), 'mdcw_gw_dashboard', [])
    clicks = dict((k,v) for k,_,v in first(script, 'effects', []))
    sloc = V.read_script('common/scripted_localisation/mdcw_diaspora_scripted_localisation.txt')
    status = next(b for k,_,b in sloc if k == 'defined_text' and first(b, 'name') == 'mdcw_gw_project_readiness')
    def reason(m):
        return next(first(b, 'localization_key') for b in values(status, 'text')
                    if m.test(first(b, 'trigger', [])))
    for kind, choice, eid, fee in [('register',1,11,75),('housing',2,12,100),('protect',3,13,100)]:
        for pp in (fee-1, fee, fee+50):
            m = fixture(data)
            m.root.political_power = D(pp)
            m.execute(clicks[f'gw_{kind}_click'])
            # Simulate stale GUI caches; native popup initialisation must restore
            # its locked origin and event-specific project type before triggers.
            m.root.variables['gw_selected_origin'] = D(-1)
            m.root.variables['gw_selected_stock_k'] = D(0)
            m.root.variables['gw_project_preview_k'] = D(0)
            m.root.variables['gw_project_choice'] = D(99)
            m.advance_days(0)
            popup = next(e for e in m.open_events if e[1] == f'mdcw_diaspora.{eid}')
            option = values(events[f'mdcw_diaspora.{eid}'], 'option')[0]
            check(m.get('gw_project_choice') == choice and m.get('gw_project_preview_k') == 100,
                  'Native integration event retains a stale selection/type/empty preview')
            check(m.test(first(option,'trigger',[])) == (pp >= fee),
                  'The funding option is missing despite eligible residents and exact PP payment')
            check(reason(m) == ('gw_project_ready' if pp >= fee else 'gw_project_blocked_pp'),
                  'An unaffordable project does not explain its exact PP prerequisite')
            if pp >= fee:
                m.choose(popup, 0)
                check(m.get('gw_project_type') == choice and m.root.political_power == pp-fee
                      and m.get('gw_project_covered_k') == 100,
                      'The actual UI/event confirmation does not start the selected programme exactly once')
            else:
                before = resources(m)
                m.execute(first(option, 'hidden_effect', []))
                check(resources(m) == before and 'gw_project_active' not in m.root.flags,
                      'A hidden/unaffordable confirmation still starts or charges a programme')
    m = fixture(data)
    m.root.variables['gw_housed^0'] = D(100)
    m.execute(clicks['gw_housing_click']); m.advance_days(0)
    check(reason(m) == 'gw_project_blocked_covered',
          'A fully treated group has no explanation for the missing funding option')


def political_reaction_tests(data):
    effects, triggers, events = data
    body = next(b for k, _, b in walk(effects['mdcw_gw_quarterly_review']) if k == 'random_list')
    incidents = [b for _, _, b in body if isinstance(b, list)
                 and any(k == 'country_event' for k, _, _ in b)]
    check(len(incidents) == 2, 'Quarterly review lacks separate abuse and political incidents')
    campaign = next(b for b in incidents if any(k == 'country_event' and first(v, 'id') == 'mdcw_diaspora.63'
                                               for k, _, v in b))
    branch = [node for node in campaign if node[0] != 'modifier']
    for amount in (25, 100, 1000, 20000):
        for option in (0, 1):
            m = fixture(data, amount)
            m.root.ideas.add('mdcw_gw_immigration_backlash')
            stability = m.root.stability
            m.execute(branch)
            m.advance_days(0)
            bill = min(max(D(amount) / 100 * D('.1'), D('.1')), D(5))
            check(m.get('gw_campaign_response_cash') == bill,
                  'Political response invoice fails to scale or respect its bounds')
            popup = next(e for e in m.open_events if e[1] == 'mdcw_diaspora.63')
            check(popup[2] is m.root, 'Nationalist backlash event is sent to the origin country')
            m.choose(popup, option)
            if option == 0:
                check(m.root.variables['treasury'] == D(100) - bill
                      and m.root.political_power == D(975)
                      and 'mdcw_gw_immigration_backlash' not in m.root.ideas
                      and m.root.stability == stability + D('.005'),
                      'Mediation has an incorrect bill, PP charge or backlash removal')
            else:
                check(m.root.variables['treasury'] == D(100)
                      and m.root.political_power == D(1000)
                      and m.root.stability == stability - D('.01')
                      and m.root.timed_ideas.get('mdcw_gw_immigration_backlash') == D(180),
                      'Ignoring agitation duplicates money or fails to set a bounded backlash')
            check('gw_incident_open' not in m.root.flags
                  and m.root.flags.get('gw_incident_cooldown') == D(365),
                  'A political response leaves a stuck popup or removes the annual incident limit')
            # Existing yearly cap must suppress either incident; no new periodic system.
            delivered = len(m.delivered)
            m.call('mdcw_gw_quarterly_review')
            m.advance_days(0)
            check(len(m.delivered) == delivered, 'Another incident bypasses the shared annual limit')
            check(m.origin.variables['treasury'] == D(100)
                  and not m.origin.timed_ideas,
                  'Recipient politics modify the sending country')
    ideas = V.read_script('common/ideas/mdcw_guest_workers_ideas.txt')
    backlash = next(b for k, _, b in walk(ideas) if k == 'mdcw_gw_immigration_backlash')
    check(first(first(backlash, 'modifier', []), 'nationalist_drift') == '0.02',
          'Nationalist reaction does not use the native +0.02 drift modifier')


def main():
    data=load()
    for test in (close_tests,project_tests,return_tests,diplomacy_tests,annexation_tests,ui_and_wiring,confirmation_dialog_tests,political_reaction_tests):
        try:test(data)
        except Exception as error:
            check(False,test.__name__+': '+str(error))
            import traceback
            traceback.print_exc()
    if V.ISSUES:
        print('FAIL: diaspora mechanics / native UI integration')
        for issue in V.ISSUES:print(' - '+issue)
        return 1
    print(f'PASS: diaspora transactions, integration, diplomacy and native UI wiring ({V.CHECKS} checks)')
    return 0


if __name__=='__main__':sys.exit(main())
