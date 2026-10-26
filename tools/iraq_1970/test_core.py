# IMPERIA CW — Cold War: iraq 1970 — test core.
"""Fail-closed execution of the emitted IRQ reward/programme AST.

The harness covers transactions and derived caches. It deliberately does not
claim to simulate HOI4's UI, warfare, native economy or multiplayer networking.
"""
import json,math
from pathlib import Path
from common import *
from test_usa_module import Scope
from test_decisions_module import DecisionWorld
from audit_design import load_design

class IraqWorld(DecisionWorld):
    def __init__(self):
        super().__init__()
        for rel in ['common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt','common/scripted_effects/COLDWAR_IRQ_1970_programmes.txt','common/scripted_effects/COLDWAR_IRQ_1970_situations.txt','common/scripted_effects/COLDWAR_IRQ_1970_starting_spirits.txt','common/scripted_effects/COLDWAR_IRQ_1970_startup_patch.txt','common/scripted_effects/COLDWAR_IRQ_1970_audit_migration.txt','common/scripted_effects/COLDWAR_IRQ_1970_politics.txt']:
            self.effects.update({k:v for k,o,v in parse((ROOT/rel).read_text(encoding='utf-8-sig'))})
        dec={k:v for k,o,v in parse((ROOT/'common/scripted_effects/COLDWAR_IRQ_1970_decision_effects.txt').read_text(encoding='utf-8-sig'))}
        self.effects.update(dec)
        self.effects.update({k:v for k,o,v in parse((ROOT/'common/scripted_effects/COLDWAR_IRQ_1970_direct_rewards_v3.txt').read_text(encoding='utf-8-sig'))})
        # Contract reconciliation and authority are real emitted providers; only
        # native politics/research/economy calls retain recorded API boundaries.
        self.triggers.update({k:v for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_IRQ_1970_decision_triggers.txt').read_text(encoding='utf-8-sig'))})
        tr={k:v for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_IRQ_1970_triggers.txt').read_text(encoding='utf-8-sig'))}
        if P+'northern_settlement_active' in tr:self.triggers[P+'northern_settlement_active']=tr[P+'northern_settlement_active']
        ust={k:v for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_USA_gulf_triggers.txt').read_text(encoding='utf-8-sig'))}
        self.triggers['COLDWAR_USA_gulf_settlement_respected']=ust['COLDWAR_USA_gulf_settlement_respected']
        self.s.update({str(s):Scope(str(s)) for s in [557,171,167,165]})
        self.dynamic=set();self.deliveries=[];self.completed=set();self.c['IRQ'].var.update({'ruling_party':21.,'gdp_total':10.,'treasury':0.})
        self.c['IRQ'].leader='Ahmed Hassan al-Bakr';self.slot_count=1
    def test(self,k,o,v,c,root,prev,source):
        if k=='custom_trigger_tooltip':return self.tests([r for r in v if r[0]!='tooltip'],c,root,prev,source)
        if k=='has_dynamic_modifier':return first(v,'modifier') in self.dynamic
        if k=='COLDWAR_IRQ_northern_settlement_active':
            return self.tests(self.triggers[k],c,root,prev,source)==(v=='yes')
        if k=='has_country_leader':return getattr(c,'leader','')==str(first(v,'name')).strip('"')
        if k=='COLDWAR_IRQ_leader_bakr_in_office':return c.leader=='Ahmed Hassan al-Bakr'
        if k=='COLDWAR_IRQ_leader_saddam_in_office':return c.leader=='Saddam Hussein'
        if k=='COLDWAR_IRQ_leader_aziz_muhammad_in_office':return c.leader=='Aziz Muhammad'
        if k=='has_variable':return v in c.var
        if k=='has_completed_focus':return v in self.completed
        if k=='has_war':return bool(c.wars)==(v=='yes')
        if k=='free_building_slots':
            _,op,count=next(row for row in v if row[0]=='size')
            return self.compare(self.slot_count,op,float(count))
        return super().test(k,o,v,c,root,prev,source)
    def run(self,rows,c,root=None,prev=None,source=None):
        root=root or c
        # Preserve if/else chains by letting the parent handle whole structural
        # blocks, while this override handles the additional concrete effects.
        taken=False
        for k,o,v in rows:
            if k=='if':
                taken=self.tests(first(v,'limit',[]),c,root,prev,source)
                if taken:self.run([r for r in v if r[0]!='limit'],c,root,prev,source)
                continue
            if k=='else_if':
                if not taken and self.tests(first(v,'limit',[]),c,root,prev,source):
                    taken=True;self.run([r for r in v if r[0]!='limit'],c,root,prev,source)
                continue
            if k=='else':
                if not taken:self.run(v,c,root,prev,source)
                taken=True;continue
            taken=False
            if k=='divide_variable':
                name,_,val=v[0];c.var[name]/=self.num(val,c);continue
            if k=='add_dynamic_modifier':self.dynamic.add(first(v,'modifier'));continue
            if k=='remove_dynamic_modifier':self.dynamic.discard(first(v,'modifier'));continue
            if k=='force_update_dynamic_modifier':continue
            if k=='add_building_construction':self.slot_count-=int(first(v,'level'));self.deliveries.append((c.key,first(v,'type'),int(first(v,'level'))));continue
            if k=='army_experience':c.var['xp']=c.var.get('xp',0)+float(v);continue
            super().run([(k,o,v)],c,root,prev,source)
    def ready(self,key):
        n=next(n for n in DESIGN['nodes'] if n['key']==key)
        for ps in n['prerequisites']:
            self.c['IRQ'].flags[ps[0]+'_implemented']=None
            self.completed.add(ps[0])
    def call_irq(self,key):
        if key.startswith('apply_'):self.completed.add(P+key.removeprefix('apply_'))
        self.call(P+key,'IRQ')

DESIGN=load_design()
ACTIVE_NODES=[n for n in DESIGN['nodes'] if not n.get('audit_retired')]
assert len(ACTIVE_NODES)+len(DESIGN['retired_focuses'])==426
assert len(DESIGN['nodes'])==426
assert len({n['id'] for n in DESIGN['nodes']})==426
def check_close(a,b):assert math.isclose(a,b,abs_tol=1e-8),(a,b)
def main():
    passed=[]
    w=IraqWorld();w.ready('saddam_industry');w.c['IRQ'].leader='Saddam Hussein'
    w.call_irq('apply_saddam_industry');assert not w.deliveries;assert P+'saddam_industry_pending' in w.c['IRQ'].flags
    check_close(w.c['IRQ'].var[P+'saddam_industry_invoice'],.4)
    w.c['IRQ'].var['gdp_total']=100;w.c['IRQ'].var['treasury']=.4
    w.call_irq('apply_saddam_industry');check_close(w.c['IRQ'].var['treasury'],0);assert len(w.deliveries)==1
    w.call_irq('apply_saddam_industry');assert len(w.deliveries)==1;check_close(w.c['IRQ'].var['treasury'],0)
    passed.append('Frozen GDP invoice; unaffordable pending; exact-boundary delivery; no reward replay')
    for block in ['owner','controller','slots','party','leader','parent']:
        w=IraqWorld();w.ready('saddam_industry');w.c['IRQ'].leader='Saddam Hussein';w.c['IRQ'].var['treasury']=1
        if block in ('owner','controller'):setattr(w.s['557'],block,'PER')
        if block=='slots':w.slot_count=0
        if block=='party':w.c['IRQ'].var['ruling_party']=4
        if block=='leader':w.c['IRQ'].leader='Ahmed Hassan al-Bakr'
        if block=='parent':w.c['IRQ'].flags.clear()
        w.call_irq('apply_saddam_industry');assert not w.deliveries;check_close(w.c['IRQ'].var['treasury'],1)
    passed.append('Ownership, control, shared-slot capacity, exact party, leader and implemented-parent guards precede payment')
    w=IraqWorld();c=w.c['IRQ'];w.call_irq('apply_regional_command');base=c.var[P+'baath_political_power_factor'];check_close(base,.08)
    assert P+'baath_programme' in w.dynamic
    c.var['ruling_party']=4;w.call_irq('reconcile_programmes');check_close(c.var[P+'baath_political_power_factor'],0);assert P+'baath_programme' not in w.dynamic
    c.var['ruling_party']=21;w.call_irq('reconcile_programmes');check_close(c.var[P+'baath_political_power_factor'],base)
    w.call_irq('reconcile_programmes');check_close(c.var[P+'baath_political_power_factor'],base)
    passed.append('Party departure detaches programme, return restores earned values, repeated reconciliation does not stack')
    c.flags[P+'bakr_presidency_package_earned']=None
    w.call_irq('reconcile_programmes');check_close(c.var[P+'bakr_political_power_factor'],.06)
    c.leader='Saddam Hussein';w.call_irq('reconcile_programmes');check_close(c.var[P+'bakr_political_power_factor'],0);assert P+'bakr_programme' not in w.dynamic
    c.leader='Ahmed Hassan al-Bakr';w.call_irq('reconcile_programmes');assert P+'bakr_programme' in w.dynamic
    passed.append('A leader change inside Baath suspends only the former leader programme and restores it on a valid return')
    # Activate every earned slot to stress the positive cap while preserving all
    # authored negative contributions; the fixtures intentionally exceed normal
    # political reachability to test the arithmetic boundary itself.
    for n in ACTIVE_NODES:
        if not n['requires'] and not n.get('active_requires'):
            c.flags[n['id']+'_package_earned']=None
            if n['mutually_exclusive']:c.flags[P+'policy_'+n['group']+'_'+n['key']]=None
    w.call_irq('reconcile_programmes')
    pos=sum(c.var.get(P+g['id']+'_stability_positive',0) for g in DESIGN['groups']);neg=sum(c.var.get(P+g['id']+'_stability_negative',0) for g in DESIGN['groups'])
    net=sum(c.var.get(P+g['id']+'_stability_factor',0) for g in DESIGN['groups']);check_close(net,min(pos,.15)+neg)
    passed.append('Positive stability caps at15 points; every negative contribution remains uncapped')
    w=IraqWorld();c=w.c['IRQ'];w.call_irq('reconcile_situations');check_close(c.var[P+'spirit_patronage_army_org_factor'],-.05)
    c.flags[P+'professional_command_implemented']=None;c.flags[P+'ministerial_audit_implemented']=None
    w.call_irq('reconcile_situations');check_close(c.var[P+'spirit_patronage_army_org_factor'],0);check_close(c.var[P+'spirit_patronage_bureaucracy_cost_multiplier_modifier'],.07)
    w.call_irq('reconcile_situations');check_close(c.var[P+'spirit_patronage_bureaucracy_cost_multiplier_modifier'],.07)
    passed.append('Situation component replacement applies once without additive drift')
    w=IraqWorld();c=w.c['IRQ'];n=next(n for n in DESIGN['nodes'] if n['key']=='bakr_north')
    c.flags[n['id']+'_package_earned']=None
    # This leaf inherits both of the al-Bakr branch's selected policy choices.
    c.flags[P+'policy_bakr_bakr_collective']=None;c.flags[P+'policy_bakr_bakr_contain_deputy']=None
    c.flags[P+'autonomy_accepted']=None;c.flags[P+'autonomy_fulfilled']=None
    w.call_irq('reconcile_programmes');before=c.var[P+'bakr_police_cost_multiplier_modifier'];check_close(before,-.06)
    c.flags.pop(P+'autonomy_fulfilled');w.call_irq('reconcile_programmes');check_close(c.var[P+'bakr_police_cost_multiplier_modifier'],0)
    c.flags[P+'autonomy_fulfilled']=None;w.call_irq('reconcile_programmes');check_close(c.var[P+'bakr_police_cost_multiplier_modifier'],before)
    c.flags.pop(n['id']+'_package_earned');c.flags[P+'bakr_guarantees_package_earned']=None
    w.call_irq('reconcile_programmes');check_close(c.var[P+'bakr_army_personnel_cost_multiplier_modifier'],-.03)
    c.flags.pop(P+'policy_bakr_bakr_contain_deputy');c.flags[P+'policy_bakr_bakr_delegate']=None
    w.call_irq('reconcile_programmes');check_close(c.var[P+'bakr_army_personnel_cost_multiplier_modifier'],0)
    assert not w.deliveries
    passed.append('Guarantee withdrawal suspends treaty-dependent programme; restoration reactivates; revised ancestral policy suspends old descendants without physical replay')
    w=IraqWorld();w.ready('saddam_industry');w.c['IRQ'].leader='Saddam Hussein';w.c['IRQ'].var['treasury']=2
    w.c['IRQ'].flags['MD_skip_treasury_cost']=None;w.call_irq('apply_saddam_industry');assert not w.deliveries;check_close(w.c['IRQ'].var['treasury'],2)
    w=IraqWorld();w.ready('saddam_industry');w.c['IRQ'].leader='Saddam Hussein';w.c['IRQ'].var['treasury']=2;w.c['IRQ'].var['gdp_total']=0
    w.call_irq('apply_saddam_industry');assert not w.deliveries and P+'saddam_industry_quoted' not in w.c['IRQ'].flags
    passed.append('Native treasury-skip and missing/zero GDP cannot generate free projects or zero invoices')
    report={'scope':'Static emitted-AST transaction/cache tests; no HOI4 engine simulation','passed':len(passed),'checks':passed}
    Path(__file__).with_name('CORE_TEST_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
