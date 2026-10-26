# IMPERIA CW — Cold War: independent emitted-core transaction and programme fixtures.
"""Exercise emitted script transactions. Fail on unsupported script, not silently.

Native MD treasury and construction primitives are bounded ledger operations here;
this verifies source contracts and is not an engine or multiplayer certification.
"""
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import json
import compile as compiler
from script_ast import parse,first,walk

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
D=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'))
C=compiler.Compiler(D);FILES=C.build()
E={k:v for k,o,v in parse(FILES['common/scripted_effects/COLDWAR_SPR_v2_focus_rewards.txt'])}
T={k:v for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_SPR_v2_politics.txt').read_text(encoding='utf-8'))}
E['increase_education_budget']=next(v for k,o,v in parse((ROOT/'common/scripted_effects/00_budget_effects.txt').read_text(encoding='utf-8')) if k=='increase_education_budget')

class Fixture:
    def __init__(self,node=None):
        self.flags={'COLDWAR_SPR_v2_core_initialized','COLDWAR_SPR_franco_departed','COLDWAR_SPR_legal_representative'}
        self.vars=defaultdict(float,treasury=100,ruling_party=22)
        self.ideas=set();self.dyn=set();self.completed=set();self.scope=None;self.elections=True
        self.states=defaultdict(lambda:{'controlled':True,'owned':True,'coastal':True,'buildings':defaultdict(int),'slots':0})
        self.tx=defaultdict(float);self.bonuses=[]
        if node:
            gid=node['group'];self.vars['ruling_party']=compiler.POLITICAL_GROUPS and {'continuity':22,'falange':21,'crown':23,'ucd':1,'ap_pp':1,'cds':2,'psoe':3,'pce_iu':4}.get(gid,22)
            if gid in ['ucd','ap_pp']:self.flags.add('COLDWAR_SPR_mandate_'+gid)
            for clause in node['prerequisites']:self.flags.add(compiler.applied(clause[0]))
            if node['gate'].get('authoritarian_legal_settlement'):
                self.flags.discard('COLDWAR_SPR_legal_representative');self.flags.add('COLDWAR_SPR_legal_authoritarian');self.elections=False
            if node['gate'].get('actual_membership_spirit'):self.ideas.add(node['gate']['actual_membership_spirit'])
    def value(self,x):
        try:return float(x)
        except (ValueError,TypeError):return self.vars[x]
    def condition(self,rows):
        for k,op,v in rows:
            if k=='tooltip':continue
            if k in ['AND','hidden_trigger','custom_trigger_tooltip']:result=self.condition(v)
            elif k=='OR':result=any(self.condition([r]) for r in v)
            elif k=='NOT':result=not self.condition(v)
            elif k in T:result=self.condition(T[k])==(v=='yes')
            elif k in ['tag','original_tag']:result=v=='SPR'
            elif k=='is_dynamic_country':result=v=='no'
            elif k=='IMP_is_1970_scenario':result=v=='yes'
            elif k=='has_country_flag':result=v in self.flags
            elif k=='has_completed_focus':result=v in self.completed
            elif k=='has_idea':result=v in self.ideas
            elif k=='has_elections':result=self.elections==(v=='yes')
            elif k=='has_country_leader':result=False
            elif k=='has_dynamic_modifier':result=first(v,'modifier') in self.dyn
            elif k=='check_variable':
                if first(v,'var'):
                    a=self.value(first(v,'var'));b=self.value(first(v,'value'));compare=first(v,'compare')
                    result={'greater_than_or_equals':a>=b,'less_than':a<b,'equals':a==b}[compare]
                else:
                    a,o,b=v[0];a=self.value(a);b=self.value(b);result={'=':a==b,'>':a>b,'<':a<b,'>=':a>=b,'<=':a<=b}[o]
            elif k.isdigit():
                before=self.scope;self.scope=int(k);result=self.condition(v);self.scope=before
            elif k=='is_owned_and_controlled_by':result=self.states[self.scope]['owned'] and self.states[self.scope]['controlled']
            elif k=='is_coastal':result=self.states[self.scope]['coastal']==(v=='yes')
            elif k in C.buildings:
                a=self.states[self.scope]['buildings'][k];b=float(v);result={'<':a<b,'>':a>b,'=':a==b}[op]
            elif k=='date':result=False
            else:raise AssertionError('Unsupported condition '+k)
            if not result:return False
        return True
    def run(self,rows):
        previous=False
        for k,op,v in rows:
            if k in ['if','else_if','else']:
                take=(k=='if' or not previous) and (k=='else' or self.condition(first(v,'limit',[])))
                if k=='if':previous=False
                if take:self.run([r for r in v if r[0]!='limit']);previous=True
                continue
            previous=False
            if k in E:self.run(E[k])
            elif k in ['set_variable','set_temp_variable','add_to_variable']:
                name,_,amount=v[0];amount=self.value(amount)
                if k=='add_to_variable':self.vars[name]+=amount
                else:self.vars[name]=amount
            elif k=='set_country_flag':self.flags.add(v)
            elif k=='add_ideas':self.ideas.add(v)
            elif k=='remove_ideas':self.ideas.discard(v)
            elif k=='swap_ideas':self.ideas.discard(first(v,'remove_idea'));self.ideas.add(first(v,'add_idea'))
            elif k=='add_dynamic_modifier':self.dyn.add(first(v,'modifier'))
            elif k=='remove_dynamic_modifier':self.dyn.discard(first(v,'modifier'))
            elif k=='modify_treasury_effect':
                self.vars['treasury']+=self.vars['treasury_change'];self.tx['cash']+=self.vars['treasury_change']
            elif k in ['add_political_power','add_stability','army_experience','air_experience','navy_experience']:
                self.tx[k]+=float(v)
            elif k in ['add_tech_bonus','add_doctrine_cost_reduction']:self.bonuses.append((k,deepcopy(v)))
            elif k.isdigit():
                before=self.scope;self.scope=int(k);self.run(v);self.scope=before
            elif k=='add_extra_state_shared_building_slots':self.states[self.scope]['slots']+=int(v);self.tx['slots']+=int(v)
            elif k=='add_building_construction':
                kind=first(v,'type');amount=int(first(v,'level'));state=self.states[self.scope]
                if first(first(C.buildings[kind],'level_cap',[]),'shares_slots')=='yes':
                    assert state['slots']>=amount,'Shared construction has no slot grant'
                    state['slots']-=amount
                state['buildings'][kind]+=amount;self.tx['buildings']+=amount
            elif k=='force_update_dynamic_modifier':pass
            else:raise AssertionError('Unsupported effect '+k)
    def complete(self,node):self.run(E['COLDWAR_SPR_complete_'+compiler.slug(node['id'])])
    def sync(self):self.run(E['COLDWAR_SPR_sync_programmes'])
    def snapshot(self):return dict(self.tx),deepcopy(self.bonuses),self.vars['treasury']

def main():
    results=[]
    asset_nodes=[n for n in D['nodes'] if any(e['type']=='building' for e in n['effects'])]
    for node in asset_nodes:
        debit=-sum(e['amount'] for e in node['effects'] if e['type']=='treasury')
        f=Fixture(node);f.vars['treasury']=debit-.00001;f.complete(node)
        assert compiler.applied(node['id']) not in f.flags and not f.tx
        f.vars['treasury']=debit;f.complete(node)
        assert compiler.applied(node['id']) in f.flags and abs(f.vars['treasury'])<1e-8
        expected=sum(e['amount'] for e in node['effects'] if e['type']=='building')
        assert f.tx['buildings']==expected
        before=f.snapshot();f.complete(node);f.sync();assert f.snapshot()==before
        # Every target must remain both owned and controlled at execution.
        for asset in [e for e in node['effects'] if e['type']=='building']:
            for state_key in ['owned','controlled']:
                g=Fixture(node);g.states[asset['state']][state_key]=False;g.complete(node)
                assert compiler.applied(node['id']) not in g.flags and not g.tx
            g=Fixture(node);maximum=int(first(first(C.buildings[asset['building']],'level_cap',[]),'state_max',50))
            g.states[asset['state']]['buildings'][asset['building']]=maximum-asset['amount']+1;g.complete(node)
            assert compiler.applied(node['id']) not in g.flags and not g.tx
    results.append(f'{len(asset_nodes)} asset transactions: exact/low funds, ownership/control, cap headroom, slot grants and once-only replay')
    # Actual cabinet authority deactivates earned policies, then restores only those earned.
    n=C.nodes['COLDWAR_SPR_council_secretariat'];f=Fixture(n);f.complete(n)
    variable=compiler.backing('continuity','political_power_factor');assert f.vars[variable]==.1
    before=f.snapshot();f.vars['ruling_party']=3;f.sync();assert f.vars[variable]==0 and compiler.programme('continuity') not in f.dyn
    f.vars['ruling_party']=22;f.sync();assert f.vars[variable]==.1 and f.snapshot()==before
    assert all(f.vars[compiler.backing(g,'political_power_factor')]==0 for g in compiler.POLITICAL_GROUPS if g!='continuity')
    # Shared conservative outlook cannot mix UCD and AP/PP mandates.
    for group in ['ucd','ap_pp']:
        node=next(n for n in D['nodes'] if n['group']==group and any(e['type']=='modifier' for e in n['effects']))
        f=Fixture(node);f.complete(node);f.flags.discard('COLDWAR_SPR_mandate_'+group);f.flags.add('COLDWAR_SPR_mandate_'+('ap_pp' if group=='ucd' else 'ucd'));f.sync()
        assert all(f.vars[compiler.backing(group,e['key'])]==0 for e in node['effects'] if e['type']=='modifier')
    results.append('Actual cabinet departure/return and UCD/AP exclusive mandates restore earned modifiers without reward replay')
    # One earned labour policy converts between the current legal packages; they never stack.
    f=Fixture();f.flags.add(compiler.applied('COLDWAR_SPR_official_labour'));f.sync()
    assert abs(f.vars[compiler.backing('territorial','social_cost_multiplier_modifier')]-.08)<1e-9
    f.flags.discard('COLDWAR_SPR_legal_representative');f.flags.add('COLDWAR_SPR_legal_authoritarian');f.elections=False;f.sync()
    assert abs(f.vars[compiler.backing('territorial','social_cost_multiplier_modifier')]-.06)<1e-9
    f.flags.add(compiler.applied('COLDWAR_SPR_free_unions'));f.sync();assert abs(f.vars[compiler.backing('territorial','civilian_factories_productivity')]-.08)<1e-9
    results.append('Labour conversion follows current legal settlement and cannot double-stack even with both receipts')
    # Current treaty membership guards availability, completion and active earned modifiers.
    n=C.nodes['COLDWAR_SPR_nato_standards'];f=Fixture(n);f.ideas.clear();f.complete(n);assert not f.tx and compiler.applied(n['id']) not in f.flags
    f.ideas.add('NATO_member');f.complete(n);before=f.snapshot();f.ideas.clear();f.sync();assert f.vars[compiler.backing('foreign','supply_consumption_factor')]==0
    f.ideas.add('NATO_member');f.sync();assert f.vars[compiler.backing('foreign','supply_consumption_factor')]==-.05 and f.snapshot()==before
    n=C.nodes['COLDWAR_SPR_nonbloc_doctrine'];f=Fixture(n);f.complete(n);before=f.snapshot();f.ideas.add('NATO_member');f.sync();assert f.vars[compiler.backing('foreign','supply_consumption_factor')]==0
    assert f.snapshot()==before
    results.append('NATO member/nonmember conditional rewards and modifier removal never replay XP or treasury')
    # A delayed Spanish receipt cannot substitute for genuine current native EC membership.
    n=C.nodes['COLDWAR_SPR_community_standards'];f=Fixture(n);f.complete(n)
    assert compiler.applied(n['id']) not in f.flags
    f.ideas.add('EU_member');f.complete(n);before=f.snapshot()
    assert f.vars[compiler.backing('foreign','civilian_factories_productivity')]==.10
    f.ideas.remove('EU_member');f.sync()
    assert 'COLDWAR_SPR_eec_membership' in f.ideas and f.vars[compiler.backing('foreign','civilian_factories_productivity')]==0
    f.ideas.add('EU_member');f.sync()
    assert f.vars[compiler.backing('foreign','civilian_factories_productivity')]==.10 and f.snapshot()==before
    results.append('EC rewards require both the accepted Spanish accession receipt and actual native membership, including a stale-receipt gap')
    # Education executes the actual native helper; its endpoint 150 PP must remain unreachable.
    n=C.nodes['COLDWAR_SPR_technical_universities']
    for existing in ['edu_01','edu_04','edu_05',None]:
        f=Fixture(n)
        if existing:f.ideas.add(existing)
        f.complete(n);assert f.tx['add_political_power']==0 and len(f.bonuses)==1
        if existing=='edu_01':assert 'edu_02' in f.ideas
        if existing=='edu_04':assert 'edu_05' in f.ideas
    results.append('Native education helper: lower levels advance, maximum/unknown skip 150 PP fallback')
    # A badge stranded by a funding race retries only the originally undelivered transaction.
    n=C.nodes['COLDWAR_SPR_regional_employment'];f=Fixture(n);f.completed.add(n['id']);f.vars['treasury']=0
    f.run(E['COLDWAR_SPR_retry_completed_focuses']);assert not f.tx
    f.vars['treasury']=2.2;f.run(E['COLDWAR_SPR_retry_completed_focuses']);assert f.tx['buildings']==1 and abs(f.vars['treasury'])<1e-8
    before=f.snapshot();f.run(E['COLDWAR_SPR_retry_completed_focuses']);assert f.snapshot()==before
    results.append('Funding-race badge retries once after affordability recovers')
    # Compare installed focus preview literals and native delivery against immutable reward rows.
    tree=first(parse(FILES['common/national_focus/COLDWAR_SPR_1970_focus.txt']),'focus_tree')
    focuses={first(v,'id'):v for k,o,v in tree if k=='focus'}
    for n in D['nodes']:
        reward=first(focuses[n['id']],'completion_reward');preview=first(reward,'effect_tooltip')
        for e in n['effects']:
            if e['type']=='modifier' and n['id'] not in compiler.LEGAL_FOCI:
                found=[v for k,o,v in walk(preview) if k=='add_to_variable' and first(v,compiler.backing(n['group'],e['key'])) is not None]
                assert any(abs(float(first(v,compiler.backing(n['group'],e['key'])))-e['amount'])<1e-8 for v in found)
            if e['type']=='decision':assert e['id']+'_effect' in str(E['COLDWAR_SPR_complete_'+compiler.slug(n['id'])])
    results.append('All 231 focus previews expose approved modifier deltas and custom-effect delivery IDs')
    report={'status':'passed','asset_focuses':len(asset_nodes),'focuses':len(D['nodes']),'checks':results,'unknown_commands':'fail closed','engine_tested':False}
    (HERE/'core_tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
