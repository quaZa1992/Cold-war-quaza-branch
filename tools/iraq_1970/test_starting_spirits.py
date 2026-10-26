# IMPERIA CW — Cold War: iraq 1970 — test starting spirits.
"""Execute native starting-card/history helper AST and compare real idea values.

This catches missing history seeding and duplicate dynamic/static application.
It does not render HOI4's native interface.
"""
import json,math
from common import *
from test_core import IraqWorld,Scope

DATA=json.loads((ROOT/'tools/iraq_1970/approved_iraq.json').read_text(encoding='utf-8-sig'))
IDEAS={k:v for k,o,v in first(first(parse((ROOT/'common/ideas/COLDWAR_IRQ_1970_starting_ideas.txt').read_text(encoding='utf-8-sig')),'ideas'),'country')}
BASE=[s['id'] for s in DATA['starting_spirits']]
LEGACY=[s for s in BASE if s!=P+'spirit_literacy']
class StartingWorld(IraqWorld):
    def __init__(self):
        super().__init__();self.scenario=True;self.date='1970.1.1';self.c['ENG']=Scope('ENG')
        tr={k:v for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_IRQ_1970_decision_triggers.txt').read_text(encoding='utf-8-sig'))}
        for k in ['COLDWAR_IRQ_oil_concession_active','COLDWAR_IRQ_border_settlement_active']:self.triggers[k]=tr[k]
    def test(self,k,o,v,c,root,prev,source):
        if k=='COLDWAR_IRQ_campaign_active':return (c.key=='IRQ' and self.scenario)==(v=='yes')
        if k=='COLDWAR_IRQ_border_settlement_active':return self.tests(self.triggers[k],c,root,prev,source)==(v=='yes')
        if k=='original_tag':return c.key==v
        if k=='is_dynamic_country':return v=='no'
        if k=='date':return self.compare(tuple(map(int,self.date.split('.'))),o,tuple(map(int,v.split('.'))))
        if k=='country_exists':return v in self.c and self.c[v].exists
        return super().test(k,o,v,c,root,prev,source)
    def run(self,rows,c,root=None,prev=None,source=None):
        # Native add_ideas supports an ID list; handle it as one statement so
        # if/else chains in the parent interpreter keep their full semantics.
        expanded=[]
        for k,o,v in rows:
            if k=='add_ideas' and isinstance(v,list):expanded.extend((k,o,idea) for _,_,idea in v)
            else:expanded.append((k,o,v))
        super().run(expanded,c,root,prev,source)
    def modifiers(self):
        result={}
        for key in self.c['IRQ'].ideas:
            if key in IDEAS:
                for k,o,v in first(IDEAS[key],'modifier',[]):result[k]=result.get(k,0)+float(v)
        return result
    def family(self,base):return [k for k in self.c['IRQ'].ideas if k==base or k.startswith(base+'_')]
    def refresh(self):self.call_irq('reconcile_situations')

def eq(a,b):assert math.isclose(a,b,abs_tol=1e-8),(a,b)
def main():
    checks=[]
    history=parse((ROOT/'history/countries/IRQ - Iraq.txt').read_text(encoding='utf-8-sig'))
    jan=first(history,'1970.1.1');assert sum(k=='COLDWAR_IRQ_seed_starting_spirits' for k,o,v in walk(jan))==1
    w=StartingWorld();w.scenario=False;w.call_irq('seed_starting_spirits');assert all(w.idea(w.c['IRQ'],s) for s in BASE)
    assert len(w.c['IRQ'].ideas)==7;eq(w.c['IRQ'].var['literacy_rate'],.35)
    checks.append('Actual1970history calls seed once; seven ordinary idea cards and baseline literacy exist before campaign startup')
    before=dict(w.c['IRQ'].ideas);w.call_irq('seed_starting_spirits');assert before==w.c['IRQ'].ideas
    checks.append('Repeated historical initialization cannot stack cards or reset literacy')
    w=StartingWorld();w.c['IRQ'].var['literacy_rate']=.61;w.call_irq('seed_starting_spirits');eq(w.c['IRQ'].var['literacy_rate'],.61)
    w=StartingWorld();w.scenario=False;w.date='2000.1.1';w.call_irq('seed_starting_spirits');assert not w.c['IRQ'].ideas
    checks.append('Existing literacy preserved and later-start history does not acquire Cold War challenges')
    w=StartingWorld();w.call_irq('seed_starting_spirits');w.dynamic.update(LEGACY);w.refresh();assert not (w.dynamic & set(LEGACY))
    for spirit in DATA['starting_spirits']:
        assert len(w.family(spirit['id']))==1
    actual=w.modifiers();expected={}
    for s in DATA['starting_spirits']:
        for k,v in s['modifiers'].items():expected[k]=expected.get(k,0)+v
    for k,v in expected.items():eq(actual[k],v)
    checks.append('All approved initial modifiers applied by real static ideas exactly once; legacy dynamic copies detached')
    c=w.c['IRQ'];c.flags[P+'ministerial_audit_implemented']=None;w.refresh();eq(w.modifiers()['bureaucracy_cost_multiplier_modifier'],.15)
    c.flags[P+'professional_command_implemented']=None;w.refresh();eq(w.modifiers()['army_org_factor'],0);assert w.family(P+'spirit_patronage')==[P+'spirit_patronage_audited_command']
    before=dict(c.ideas);w.refresh();assert before==c.ideas
    checks.append('Patronage audit and command reform replace independent components without duplicate spirits or daily reinstall')
    c.flags[P+'autonomy_accepted']=None;c.flags[P+'autonomy_fulfilled']=None;w.refresh();assert w.family(P+'spirit_unsettled_north')==[P+'spirit_unsettled_north_autonomy']
    c.flags[P+'federal_settlement']=None;w.refresh();assert w.family(P+'spirit_unsettled_north')==[P+'spirit_unsettled_north_federal']
    c.wars.add('KUR');w.refresh();assert w.family(P+'spirit_unsettled_north')==[P+'spirit_unsettled_north']
    checks.append('Northern stages follow an actually respected settlement; war restores original burden')
    w=StartingWorld();w.call_irq('seed_starting_spirits');c=w.c['IRQ'];c.flags[P+'oil_state_company_implemented']=None;w.refresh();assert w.family(P+'spirit_ipc')==[P+'spirit_ipc_transition']
    c.flags[P+'oil_field_maintenance_implemented']=None;w.refresh();assert not w.family(P+'spirit_ipc')
    w=StartingWorld();w.call_irq('seed_starting_spirits');c=w.c['IRQ'];c.flags.update({P+'oil_concession_delivery_implemented':None,P+'oil_concession_accepted':None});w.c['ENG'].flags[P+'oil_concession_partner']=None;w.refresh();assert w.family(P+'spirit_ipc')==[P+'spirit_ipc_concession']
    c.wars.add('ENG');w.refresh();assert w.family(P+'spirit_ipc')==[P+'spirit_ipc']
    checks.append('Nationalization, paid maintenance and respected concession select exact native oil burdens; broken concession loses relief')
    w=StartingWorld();w.call_irq('seed_starting_spirits');c=w.c['IRQ']
    for key,ag,cg in [('agri_cooperative_credit',-.08,.03),('agri_extension',-.04,.03),('agri_distribution',-.04,.01)]:
        c.flags[P+key+'_implemented']=None;w.refresh();m=w.modifiers();eq(m['agricolture_productivity_modifier'],ag);eq(m['consumer_goods_factor'],cg);assert len(w.family(P+'spirit_rural'))==1
    c.flags[P+'agri_reform_delivery_implemented']=None;w.refresh();assert not w.family(P+'spirit_rural')
    checks.append('Each rural stage preserves the other component; delivered final reform removes the burden once')
    w=StartingWorld();w.call_irq('seed_starting_spirits');w.refresh();c=w.c['IRQ'];c.var['ruling_party']=4;w.refresh();assert not w.family(P+'spirit_july_state')
    c.var['ruling_party']=21;w.refresh();assert w.family(P+'spirit_july_state')==[P+'spirit_july_state']
    c.flags[P+'national_front_implemented']=None;w.refresh();assert not w.family(P+'spirit_july_state')
    checks.append('July State follows Baath government and its institutional replacement without removing unrelated challenges')
    report={'scope':'Executed generated static-idea/history/reconciliation AST; not native UI rendering','passed':len(checks),'checks':checks}
    (ROOT/'tools/iraq_1970/STARTING_SPIRITS_TEST_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
