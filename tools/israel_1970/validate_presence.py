# IMPERIA COLD WAR — Settlement presence and occupation regression checks.
"""Evaluate emitted, bounded transactions; this is not a native engine test.

Country/state scope, PREV, global event targets, receipts, displayed-only effects
and the native budget-provider deltas have explicit fixture adapters. Native
staffing/capacity and dynamic enable outcomes are exercised as predicate inputs.
Unsupported executed commands or guards fail instead of being assumed valid.
"""
from pathlib import Path
import copy
import hashlib
import json
import re
from script_format import read

ROOT=Path(__file__).resolve().parents[2]
SOURCES=['tools/israel_1970/english_design.json','common/scripted_effects/ISR70_policy_effects.txt',
         'common/scripted_triggers/ISR70_policy_triggers.txt','common/dynamic_modifiers/ISR70_policy_dynamic_modifiers.txt',
         'common/decisions/ISR70_presence_responses.txt','events/ISR70_policy_events.txt',
         'history/states/207-Jerusalem.txt','history/states/1253-West Jerusalem.txt',
         'common/national_focus/ISR70_focus.txt','common/decisions/ISR70_policy_decisions.txt',
         'common/decisions/categories/ISR70_presence_responses.txt']
TEXT={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in SOURCES}
DATA=json.loads(TEXT[SOURCES[0]])
ERRORS=[]
CHECKS=[]


def scalar(block,key,default=None):
    return next((v for k,o,v in block if k==key and not isinstance(v,list)),default)


def child(block,key,default=None):
    return next((v for k,o,v in block if k==key and isinstance(v,list)),default)


def walk(block):
    for k,o,v in block:
        yield k,o,v
        if isinstance(v,list):yield from walk(v)


def blocks(path):
    return {k:v for k,o,v in read(TEXT[path]) if isinstance(v,list)}


EFFECTS=blocks(SOURCES[1]);TRIGGERS=blocks(SOURCES[2]);DYNAMIC=blocks(SOURCES[3])
RESPONSES={k:v for k,o,v in child(read(TEXT[SOURCES[4]]),'ISR70_presence_responses') if isinstance(v,list)}
EVENTS={scalar(v,'id'):v for k,o,v in read(TEXT[SOURCES[5]]) if k=='country_event'}
FOCUSES={scalar(v,'id'):v for k,o,v in child(read(TEXT[SOURCES[8]]),'focus_tree') if k=='focus'}
DECISIONS={k:v for k,o,v in child(read(TEXT[SOURCES[9]]),'ISR70_policy_category') if isinstance(v,list)}


def check(ok,label):
    CHECKS.append(label)
    if not ok:ERRORS.append(label)


class World:
    def __init__(self):
        self.countries={tag:dict(exists=True,vars={'treasury':1000.,'gdp_total':100.,'debt':0.},flags=set(),
                                dynamic={},arrays={},dirty=0,ideas=set(),bankrupt=False,
                                focuses={n['id'] for n in DATA['nodes']}) for tag in ('ISR','PAL','EGY','SYR','USA')}
        self.states={s:dict(owner=owner,controller='ISR',cores={owner},resistance=0.,compliance=70.,
                            dynamic={},capacity=True,full=True,slots=0,buildings={},has_resistance=True)
                     for s,owner in ((208,'PAL'),(209,'PAL'),(213,'EGY'),(587,'SYR'))}
        for state in (207,1253):
            self.states[state]=dict(owner='ISR',controller='ISR',cores={'ISR','PAL'},resistance=0.,compliance=70.,
                                    dynamic={},capacity=True,full=True,slots=0,buildings={},has_resistance=False)
        self.targets={};self.wars=set();self.embargoes=set();self.date='1970.1.1';self.staff=True
        self.events=[];self.scenario=True

    def resolve(self,token,stack):
        if token=='PREV':return stack[-2] if len(stack)>1 else None
        if token in ('THIS','ROOT'):return stack[-1] if token=='THIS' else stack[0]
        if token.startswith('event_target:'):return self.targets.get(token.split(':',1)[1])
        if token in self.countries:return token
        if token.isdigit() and int(token) in self.states:return int(token)
        return None

    def object(self,ctx):
        return self.states[ctx] if isinstance(ctx,int) else self.countries[ctx]

    def number(self,token,ctx):
        try:return float(token)
        except (ValueError,TypeError):
            if token.startswith('building_level@'):
                assert isinstance(ctx,int),ctx
                return self.states[ctx]['buildings'].get(token.split('@',1)[1],0)
            if '.' in token and token.split('.',1)[0] in self.countries:
                tag,name=token.split('.',1);return self.countries[tag]['vars'][name]
            return self.object(ctx)['vars'][token]

    def condition(self,block,stack,mode='AND'):
        ctx=stack[-1]
        if ctx is None:return False
        out=[]
        for k,o,v in block:
            if k.startswith('#') or k=='tooltip':continue
            obj=self.object(ctx)
            if k in ('AND','hidden_trigger','custom_trigger_tooltip'):ok=self.condition(v,stack)
            elif k=='OR':ok=self.condition(v,stack,'OR')
            elif k=='NOT':ok=not self.condition(v,stack)
            elif k in TRIGGERS:ok=self.condition(TRIGGERS[k],stack)==(v=='yes')
            elif k=='ISR70_is_scenario':ok=ctx=='ISR' and self.scenario==(v=='yes')
            elif k=='IMP_is_1970_scenario':ok=self.scenario==(v=='yes')
            elif k=='tag':ok=ctx==self.resolve(v,stack)
            elif k=='always':ok=v=='yes'
            elif k=='exists':ok=obj['exists']==(v=='yes')
            elif k=='has_country_flag':ok=v in obj['flags']
            elif k=='has_completed_focus':ok=v in obj['focuses']
            elif k=='has_variable':ok=v in obj['vars']
            elif k=='has_idea':ok=v in obj['ideas']
            elif k=='has_active_mission':
                assert v=='bankruptcy_incoming_collapse',v
                ok=obj['bankrupt']
            elif k=='has_event_target':ok=v in self.targets
            elif k=='country_exists':
                target=self.resolve(v,stack);ok=target in self.countries and self.countries[target]['exists']
            elif k=='has_war_with':ok=frozenset((ctx,self.resolve(v,stack))) in self.wars
            elif k=='is_embargoing':ok=(ctx,self.resolve(v,stack)) in self.embargoes
            elif k=='is_in_array':ok=self.resolve(scalar(v,'value'),stack) in obj['arrays'].get(scalar(v,'array'),set())
            elif k=='owns_state':ok=self.states[int(v)]['owner']==ctx
            elif k=='controls_state':ok=self.states[int(v)]['controller']==ctx
            elif k=='is_owned_by':ok=obj['owner']==self.resolve(v,stack)
            elif k=='is_controlled_by':ok=obj['controller']==self.resolve(v,stack)
            elif k=='is_core_of':ok=self.resolve(v,stack) in obj['cores']
            elif k=='has_dynamic_modifier':ok=scalar(v,'modifier') in obj['dynamic']
            elif k=='has_resistance':ok=obj['has_resistance']==(v=='yes')
            elif k=='has_full_control_of_state':ok=self.states[int(v)]['full']
            elif k=='free_building_slots':ok=obj['capacity']
            elif k.startswith('can_staff_'):ok=self.staff
            elif k=='date':
                a=tuple(map(int,self.date.split('.')));b=tuple(map(int,v.split('.')))
                ok={'<':a<b,'>':a>b,'=':a==b}[o]
            elif k=='check_variable':
                if scalar(v,'var'):
                    a=self.number(scalar(v,'var'),ctx);b=self.number(scalar(v,'value'),ctx)
                    cmp=scalar(v,'compare');ok={'greater_than':a>b,'greater_than_or_equals':a>=b,
                                               'less_than':a<b,'less_than_or_equals':a<=b,'equals':a==b}[cmp]
                else:
                    terms=[x for x in v if not x[0].startswith('#')];assert len(terms)==1,terms
                    name,op,val=terms[0];a=self.number(name,ctx);b=self.number(val,ctx)
                    ok={'>':a>b,'<':a<b,'=':a==b}[op]
            elif k in ('owner','controller'):
                ok=self.condition(v,stack+[obj[k]])
            elif k.isdigit() or k in self.countries or k.startswith('event_target:'):
                ok=self.condition(v,stack+[self.resolve(k,stack)])
            else:raise ValueError('Unsupported executed condition: '+k)
            out.append(ok)
            if mode=='AND' and not ok:return False
            if mode=='OR' and ok:return True
        return all(out) if mode=='AND' else any(out)

    def execute(self,block,stack=None):
        stack=['ISR'] if stack is None else stack
        ctx=stack[-1]
        if ctx is None:return
        obj=self.object(ctx);branch=None
        for k,o,v in block:
            if k.startswith('#') or k in ('custom_effect_tooltip','unlock_decision_tooltip','log'):continue
            if k=='effect_tooltip':continue
            if k in ('if','else_if'):
                allowed=(k=='if' or branch is False) and self.condition(child(v,'limit',[]),stack)
                branch=bool(allowed) or (branch if k=='else_if' else False)
                if allowed:self.execute([(a,b,c) for a,b,c in v if a!='limit'],stack)
                continue
            if k=='else':
                if branch is False:self.execute(v,stack)
                branch=None;continue
            branch=None
            if k=='hidden_effect':self.execute(v,stack)
            elif k in EFFECTS:self.execute(EFFECTS[k],stack)
            elif k in ('owner','controller'):self.execute(v,stack+[obj[k]])
            elif k.isdigit() or k in self.countries or k.startswith('event_target:'):
                self.execute(v,stack+[self.resolve(k,stack)])
            elif k in ('set_variable','set_temp_variable','multiply_variable','multiply_temp_variable','add_to_variable'):
                terms=[x for x in v if x[0]!='tooltip'];assert len(terms)==1,terms
                name,_,val=terms[0];value=self.number(val,ctx)
                if k.startswith('multiply'):obj['vars'][name]*=value
                elif k=='add_to_variable':obj['vars'][name]=obj['vars'].get(name,0)+value
                else:obj['vars'][name]=value
            elif k=='clear_variable':obj['vars'].pop(v,None)
            elif k=='set_country_flag':obj['flags'].add(v)
            elif k=='clr_country_flag':obj['flags'].discard(v)
            elif k=='save_global_event_target_as':self.targets[v]=ctx
            elif k=='modify_treasury_effect':obj['vars']['treasury']+=obj['vars']['treasury_change'];obj['dirty']+=1
            elif k=='update_money_dirty_variable':obj['dirty']+=1
            elif k=='add_dynamic_modifier':obj['dynamic'][scalar(v,'modifier')]=scalar(v,'scope')
            elif k=='remove_dynamic_modifier':obj['dynamic'].pop(scalar(v,'modifier'),None)
            elif k=='add_ideas':obj['ideas'].add(v)
            elif k=='set_resistance':obj['resistance']=float(v)
            elif k=='set_compliance':obj['compliance']=float(v)
            elif k=='start_resistance':obj['has_resistance']=True
            elif k=='country_event':self.events.append((ctx,scalar(v,'id'),int(scalar(v,'days'))))
            elif k=='add_extra_state_shared_building_slots':obj['slots']+=int(v)
            elif k=='add_building_construction':
                kind=scalar(v,'type');obj['buildings'][kind]=obj['buildings'].get(kind,0)+int(scalar(v,'level'))
            else:raise ValueError('Unsupported executed effect: '+k)

    def balances(self):return {k:v['vars']['treasury'] for k,v in self.countries.items()}

    def enabled(self,ctx,name):
        return name in self.object(ctx)['dynamic'] and self.condition(child(DYNAMIC[name],'enable',[]),[ctx])


def snapshot(world):return copy.deepcopy(world.__dict__)


def main():
    presence=DATA['settlement_presence'];occupation=DATA['occupation_profiles']
    check(len(presence['contracts'])==4 and presence['recipient_decisions']==0 and not RESPONSES,
          'Four unilateral programmes and zero host response decisions')
    check(presence.get('unilateral') is True and presence.get('host_receives_capital') is False,
          'Metadata specifies unilateral funding without host capital transfers')
    check(abs(presence['capital_share']-.01)<1e-8,'Initial unilateral funding is exactly 1% of GDP')
    category=child(read(TEXT[SOURCES[10]]),'ISR70_presence_responses')
    check(not World().condition(child(category,'visible',[]),['PAL']),'Legacy host response category is disabled')
    for c in presence['contracts']:
        state=c['state'];host={208:'PAL',209:'PAL',213:'EGY',587:'SYR'}[state]
        def bare():
            w=World();w.states[state]['controller']=host;return w
        def established():
            w=bare();w.execute(EFFECTS[c['offer']]);return w
        w=established()
        check(w.countries['ISR']['vars']['treasury']==999 and all(country['vars']['treasury']==1000 for tag,country in w.countries.items() if tag!='ISR'),
              str(state)+': establishment spends 1% once in Israel and transfers nothing to any host')
        check(c['paid'] in w.countries['ISR']['flags'] and c['active'] in w.countries['ISR']['flags'],str(state)+': paid and active receipts are recorded')
        check(w.targets.get(c['host_target'])==host and w.enabled('ISR',c['israel_modifier']) and w.enabled(host,c['host_modifier']) and w.enabled(state,c['state_modifier']),
              str(state)+': live effects target the actual foreign controller')
        check(c['host_pending'] not in w.countries[host]['flags'] and c['host_signed'] not in w.countries[host]['flags'],str(state)+': establishment creates no host acceptance flags')
        w.countries['ISR']['vars']['gdp_total']=500;before=snapshot(w);w.execute(EFFECTS[c['offer']])
        check(snapshot(w)==before,str(state)+': duplicate establishment cannot spend again after GDP changes')
        check(c['host_modifiers']=={'agricolture_productivity_modifier':-.03,'bureaucracy_cost_multiplier_modifier':.025,'police_cost_multiplier_modifier':.02,'stability_factor':-.01},
              str(state)+': affected controller receives only the four specified disadvantages')
        check(c['state_modifiers']=={'state_production_speed_infrastructure_factor':-.10,'local_factories':-.05,'local_supplies_for_controller':-.05},
              str(state)+': local encroachment has the exact three specified disadvantages')
        for action in (c['accept'],c['cancel'],c['offer']):
            before=snapshot(w);w.execute(EFFECTS[action],[host])
            check(snapshot(w)==before,str(state)+': non-Israeli legacy/helper execution is inert: '+action)
        for invalid in ('poor','bankrupt','israel_dead','host_dead','israel_control','zero_gdp'):
            trial=bare()
            if invalid=='poor':trial.countries['ISR']['vars']['treasury']=0
            if invalid=='bankrupt':trial.countries['ISR']['bankrupt']=True
            if invalid=='israel_dead':trial.countries['ISR']['exists']=False
            if invalid=='host_dead':trial.countries[host]['exists']=False
            if invalid=='israel_control':trial.states[state]['controller']='ISR'
            if invalid=='zero_gdp':trial.countries['ISR']['vars']['gdp_total']=0
            money=trial.balances();trial.execute(EFFECTS[c['offer']])
            check(trial.balances()==money and c['paid'] not in trial.countries['ISR']['flags'] and c['active'] not in trial.countries['ISR']['flags'],
                  str(state)+': invalid '+invalid+' establishment does not fund or activate the programme')
        for regime in ['war','embargo_isr','embargo_host']+[f'sanction_{tag}_{kind}_{direction}' for tag in ('ISR',host) for kind in ('dip','fin','eco','mil') for direction in ('on','by')]:
            trial=copy.deepcopy(w)
            if regime=='war':trial.wars.add(frozenset(('ISR',host)))
            elif regime=='embargo_isr':trial.embargoes.add(('ISR',host))
            elif regime=='embargo_host':trial.embargoes.add((host,'ISR'))
            else:
                _,tag,kind,direction=regime.split('_');other=host if tag=='ISR' else 'ISR'
                trial.countries[tag]['arrays'].setdefault(f'imp_{kind}_sanc_{direction}_us',set()).add(other)
            money=trial.balances();trial.execute(EFFECTS['ISR70_policy_reconcile_presence'])
            check(trial.enabled('ISR',c['israel_modifier']) and trial.enabled(host,c['host_modifier']) and trial.balances()==money,
                  str(state)+': '+regime+' gives the affected government no permission veto')
        # Ownership is distinct from effective control. The controller receives
        # costs; the former target is cleaned without a new payment.
        trial=copy.deepcopy(w);money=trial.balances();trial.states[state]['controller']='USA'
        check(not trial.enabled(host,c['host_modifier']),str(state)+': old controller burden disables immediately')
        trial.execute(EFFECTS['ISR70_policy_reconcile_presence'])
        check(c['host_modifier'] not in trial.countries[host]['dynamic'] and trial.enabled('USA',c['host_modifier']) and trial.targets[c['host_target']]=='USA' and trial.balances()==money,
              str(state)+': controller change moves the burden and cleans old target without repayment')
        trial.states[state]['owner']='ISR';trial.execute(EFFECTS['ISR70_policy_reconcile_presence'])
        check(trial.enabled('USA',c['host_modifier']) and trial.enabled('ISR',c['israel_modifier']),str(state)+': Israeli legal ownership does not substitute for military control')
        if state==208:
            # A former/dead-country cycle can leave a disabled modifier already
            # registered on PAL. Returning control must dirty its budget even
            # though has_dynamic_modifier prevents another add call.
            trial=copy.deepcopy(w);trial.states[state]['controller']='USA'
            trial.targets[c['host_target']]='USA'
            trial.countries['USA']['dynamic'][c['host_modifier']]=None
            check(c['host_modifier'] in trial.countries['PAL']['dynamic'] and not trial.enabled('PAL',c['host_modifier']),
                  '208: returning-controller fixture starts with a disabled existing PAL burden')
            trial.states[state]['controller']='PAL'
            dirty=trial.countries['PAL']['dirty'];money=trial.balances()
            trial.execute(EFFECTS['ISR70_policy_reconcile_presence'])
            check(trial.countries['PAL']['dirty']>dirty and trial.targets[c['host_target']]=='PAL'
                  and trial.enabled('PAL',c['host_modifier']) and trial.balances()==money,
                  '208: returning PAL controller dirties its existing burden without repeating capital')
        for absent in ('israel_control','host_dead','israel_dead'):
            trial=copy.deepcopy(w);money=trial.balances()
            if absent=='israel_control':trial.states[state]['controller']='ISR'
            if absent=='host_dead':trial.countries[host]['exists']=False
            if absent=='israel_dead':trial.countries['ISR']['exists']=False
            check(not trial.enabled('ISR',c['israel_modifier']) and not trial.enabled(state,c['state_modifier']),str(state)+': '+absent+' immediately disables foreign-route effects')
            trial.execute(EFFECTS['ISR70_policy_reconcile_presence'])
            check(c['israel_modifier'] not in trial.countries['ISR']['dynamic'] and trial.balances()==money,str(state)+': '+absent+' suspends without cash replay')
            trial.states[state]['controller']=host;trial.countries[host]['exists']=True;trial.countries['ISR']['exists']=True
            trial.execute(EFFECTS['ISR70_policy_reconcile_presence'])
            check(trial.enabled('ISR',c['israel_modifier']) and trial.enabled(host,c['host_modifier']) and trial.balances()==money,
                  str(state)+': '+absent+' restoration resumes without repayment')
        money=w.balances();w.execute(EFFECTS[c['cancel']]);check(not w.enabled('ISR',c['israel_modifier']) and w.balances()==money,str(state)+': Israel can end funding without a refund')
        w.execute(EFFECTS[c['offer']]);check(w.countries['ISR']['vars'][c['quote']]==0 and w.balances()==money and w.enabled('ISR',c['israel_modifier']),str(state)+': previously funded holdings re-establish at zero capital')
        # Old paid agreements migrate their receipts and active state without
        # rerunning a transaction. Pending unpaid offers remain unfunded.
        for prior in ('paid_active','unpaid_pending'):
            trial=bare();trial.targets[c['host_target']]=host;trial.countries['ISR']['flags'].add(c['pending'])
            trial.countries[host]['flags'].update((c['host_pending'],c['host_signed']))
            if prior=='paid_active':
                trial.countries['ISR']['flags'].update((c['paid'],c['active']))
                trial.countries['ISR']['dynamic'][c['israel_modifier']]=None;trial.countries[host]['dynamic'][c['host_modifier']]=None
            money=trial.balances();trial.execute(EFFECTS['ISR70_policy_reconcile_presence'])
            check(c['migration'] in trial.countries['ISR']['flags'] and c['pending'] not in trial.countries['ISR']['flags'] and not ({c['host_pending'],c['host_signed']} & trial.countries[host]['flags']) and trial.balances()==money,
                  str(state)+': '+prior+' migration removes former consent flags without payment')
            check(trial.enabled('ISR',c['israel_modifier'])==(prior=='paid_active'),str(state)+': '+prior+' migration preserves paid activation only')
            if prior=='paid_active':check(trial.countries['ISR']['dirty']>0 and trial.countries[host]['dirty']>0,str(state)+': changed legacy modifier fields dirty both budgets once')
            before=snapshot(trial);trial.execute(EFFECTS['ISR70_policy_reconcile_presence'])
            check(snapshot(trial)==before,str(state)+': '+prior+' migration and stable reconciliation are idempotent')
        # Execute actual emitted focus and decision wrappers, not just helpers.
        focus=child(FOCUSES[c['focus']],'completion_reward');trial=bare();trial.execute(focus)
        check(trial.countries['ISR']['vars']['treasury']==999 and trial.enabled('ISR',c['israel_modifier']),str(state)+': actual national focus establishes the unilateral programme')
        renew=DECISIONS[f'ISR70_policy_decision_renew_presence_{state}'];end=DECISIONS[f'ISR70_policy_decision_end_presence_{state}']
        trial.execute(child(end,'complete_effect'));money=trial.balances();trial.execute(child(renew,'complete_effect'))
        check(trial.balances()==money and trial.enabled('ISR',c['israel_modifier']),str(state)+': actual funding-end and re-establish decisions preserve the paid receipt')
        trial=bare();trial.execute(EFFECTS['ISR70_policy_refresh_costs']);trial.execute(child(renew,'complete_effect'))
        check(trial.countries['ISR']['vars']['treasury']==999 and trial.enabled('ISR',c['israel_modifier']),str(state)+': actual re-establishment decision can fund an unfunded completed route')
        preview=read(c['preview']);forbidden={'modify_treasury_effect','modify_debt_effect','add_dynamic_modifier','add_ideas','add_building_construction','transfer_state','set_state_controller','add_manpower','set_country_flag'}
        check(not any(k in forbidden or k in EFFECTS for k,o,v in walk(preview)),str(state)+': prospective unilateral display contains no runtime providers or grants')
        trial=bare();before=snapshot(trial);trial.execute(preview)
        check(snapshot(trial)==before,str(state)+': display wrapper cannot establish or charge the programme')

    helper=EFFECTS[occupation['reconcile_effect']]
    world=World();world.execute(helper)
    for p in occupation['profiles']:
        state=p['state'];obj=world.states[state]
        check((obj['resistance'],obj['compliance'])==(p['initial_resistance'],p['initial_compliance']),str(state)+': January occupation values seeded')
        check(world.enabled(state,p['state_modifier']) and world.enabled('ISR',p['country_modifier']),str(state)+': state and country burdens enabled')
        check(obj['dynamic'][p['state_modifier']]=='ISR',str(state)+': state burden explicitly scoped to Israel')
        obj['resistance']=43;obj['compliance']=51
    dirty=world.countries['ISR']['dirty'];world.execute(helper)
    check(world.countries['ISR']['dirty']==dirty,'Unchanged occupation composition does not dirty the budget again')
    check(all(world.states[p['state']]['resistance']==43 and world.states[p['state']]['compliance']==51 for p in occupation['profiles']),
          'Daily occupation reconciliation does not reset earned resistance/compliance')
    for p in occupation['profiles']:
        for failure in ('control','core'):
            trial=copy.deepcopy(world);obj=trial.states[p['state']]
            if failure=='control':obj['controller']='USA'
            else:obj['cores'].add('ISR')
            check(not trial.enabled(p['state'],p['state_modifier']) and not trial.enabled('ISR',p['country_modifier']),str(p['state'])+': '+failure+' immediately disables occupation burdens')
            trial.execute(helper)
            check(p['country_modifier'] not in trial.countries['ISR']['dynamic'],str(p['state'])+': '+failure+' removes national cost modifier')
            obj['controller']='ISR';obj['cores'].discard('ISR');trial.execute(helper)
            check(trial.enabled('ISR',p['country_modifier']) and obj['resistance']==43 and obj['compliance']==51,
                  str(p['state'])+': '+failure+' recovery restores costs without resetting progress')
    late=World();late.date='1970.2.1';late.execute(helper)
    check(all(late.states[p['state']]['resistance']==0 and late.states[p['state']]['compliance']==70 for p in occupation['profiles']),
          'Late-save first reconciliation preserves existing resistance and compliance')
    skipped=World();skipped.states[208]['controller']='PAL';skipped.states[209]['cores'].add('ISR');skipped.execute(helper)
    check(skipped.states[208]['resistance']==0 and skipped.states[209]['resistance']==0,
          'Initial seed excludes foreign-controlled states and existing Israeli cores')
    skipped.states[208]['controller']='ISR';skipped.states[209]['cores'].discard('ISR');skipped.date='1970.1.2';skipped.execute(helper)
    check(skipped.states[208]['resistance']==0 and skipped.states[209]['resistance']==0,
          'Later January control/core changes do not replay initial seed')
    for state in (207,1253):
        check(world.states[state]==World().states[state],str(state)+': Jerusalem core and state values remain untouched')
        history=child(child(read(TEXT[SOURCES[6 if state==207 else 7]]),'state'),'history')
        check(('add_core_of','=','ISR') in history,str(state)+': actual state history retains Israeli core')
    profile_keys={k for p in occupation['profiles'] for m in ('state_modifiers','country_modifiers') for k in p[m]}
    check(not any('workforce' in k or 'tax' in k for k in profile_keys),'Occupation profiles introduce no workforce or tax penalties')
    check(not any(k in ('every_country','every_state','every_owned_state','every_controlled_state') for k,o,v in walk(helper)),
          'Occupation reconciliation has four bounded states and no world enumeration')

    for p in [p for p in DATA['policy_expansion']['projects'] if p['key'].startswith('controlled_')]:
        state=p['states'][0];game=World();game.execute(EFFECTS['ISR70_policy_refresh_costs'])
        start=EFFECTS['ISR70_policy_start_'+p['key']];callback=child(EVENTS[p['callback']],'immediate')
        game.execute(start);game.execute(callback)
        check(game.states[state]['slots']==3 and game.states[state]['buildings']=={'agriculture_district':1,'infrastructure':1,'bunker':1},
              p['key']+': actual controlled-state callback grants three levels with three slots')
        before=snapshot(game);game.execute(callback);game.execute(start)
        check(snapshot(game)==before,p['key']+': controlled-state buildings cannot replay')
        for key,o,value in walk(callback):
            if key==str(state) and isinstance(value,list) and any(k=='add_building_construction' for k,o,v in value):
                credit=0
                for k,o,v in value:
                    if k=='add_extra_state_shared_building_slots':credit+=int(v)
                    if k=='add_building_construction':credit-=int(scalar(v,'level'));check(credit>=0,p['key']+': slots precede each building')
        if state in (208,209):
            for freeze in ('ISR70_policy_freeze_agreed','ISR70_policy_binding_settlement_ceiling'):
                game=World();game.countries['ISR']['flags'].update(('ISR70_policy_target_'+str(state),freeze))
                game.execute(EFFECTS['ISR70_policy_refresh_costs']);before=snapshot(game);game.execute(start)
                check(snapshot(game)==before,p['key']+': selected-area '+freeze+' blocks construction start')
                game=World();game.execute(EFFECTS['ISR70_policy_refresh_costs']);game.execute(start)
                game.countries['ISR']['flags'].update(('ISR70_policy_target_'+str(state),freeze))
                game.countries['ISR']['vars']['gdp_total']=500;game.execute(EFFECTS['ISR70_policy_refresh_costs']);game.execute(callback)
                check(game.countries['ISR']['vars']['treasury']==1000 and game.states[state]['buildings']=={} and p['done'] not in game.countries['ISR']['flags'],
                      p['key']+': a newly accepted '+freeze+' refunds the original reservation without construction')
        for failure in ('lost_control','capacity','staff','infrastructure_ceiling'):
            game=World();game.execute(EFFECTS['ISR70_policy_refresh_costs']);game.execute(start)
            if failure=='lost_control':game.states[state]['controller']='USA'
            if failure=='capacity':game.states[state]['capacity']=False
            if failure=='staff':game.staff=False
            if failure=='infrastructure_ceiling':game.states[state]['buildings']['infrastructure']=6
            assets=copy.deepcopy(game.states[state]['buildings'])
            game.countries['ISR']['vars']['gdp_total']=500;game.execute(EFFECTS['ISR70_policy_refresh_costs']);game.execute(callback)
            check(game.countries['ISR']['vars']['treasury']==1000 and game.states[state]['buildings']==assets and p['done'] not in game.countries['ISR']['flags'],
                  p['key']+': '+failure+' at delivery refunds the original quote without assets')


if __name__=='__main__':
    try:main()
    except Exception as exc:ERRORS.append(type(exc).__name__+': '+str(exc))
    report=dict(project='IMPERIA COLD WAR',status='FAIL' if ERRORS else 'PASS',checks=len(CHECKS),errors=ERRORS,
        passed=[c for c in CHECKS if c not in ERRORS],source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES},
        method='Emitted AST evaluation with multi-country/state scopes, PREV and global event-target fixtures, plus structural guard checks.',
        limitations=['No native HOI4, save, multiplayer, UI or tooltip-rendering execution.',
            'Native money providers are fixture delta adapters; economy and recurring interest are not simulated.',
            'Native staffing and building capacity are explicit fixture predicates; scope adapters are a bounded interpretation, not an engine emulator.',
            'Dynamic modifier enable blocks are evaluated by this model, not the native cache or scheduler.'],runtime_test=False)
    (ROOT/'docs/israel_1970_design/presence_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('passed','source_sha256')},indent=2));raise SystemExit(bool(ERRORS))
