# IMPERIA CW — Cold War: iraq 1970 — test audit transactions.
"""Fresh compiler-output transaction tests for the approved audit migration.

Native research, construction, literacy and politics calls are explicit recorded
API boundaries. The harness checks emitted authority/receipts/cash, not HOI4
research usability, budget simulation, UI rendering or multiplayer behavior.
"""
import json, math
from common import ROOT, P, parse, first, values
import compile as compiler
import audit_migration, decisions_module, runtime_design, starting_spirits
from audit_design import load_design, baseline
from test_audit_politics import PoliticsWorld


class GeneratedOutputs(dict):
    """Carry the exact data revision used to generate a bounded fixture."""
    design=None


def fresh_outputs(legacy=False):
    compiler.CONDITIONS.update(decisions_module.CONTRACTS)
    compiler.CONDITIONS.update(compiler.OWN_CONDITIONS)
    saved=(compiler.D,compiler.NODES,compiler.BY,compiler.GROUPS)
    try:
        if legacy:
            compiler.D=load_design(include_overhaul=False)
            compiler.NODES=compiler.D['nodes'];compiler.BY={n['id']:n for n in compiler.NODES}
            compiler.GROUPS={g['id']:g for g in compiler.D['groups']}
        compiler.OUTPUTS.clear()
        compiler.generate_focuses();compiler.generate_programmes();compiler.generate_queue()
        output=GeneratedOutputs(compiler.OUTPUTS);output.design=compiler.D
        return output
    finally:
        compiler.D,compiler.NODES,compiler.BY,compiler.GROUPS=saved


class AuditWorld(PoliticsWorld):
    def __init__(self, outputs):
        super().__init__()
        self.dynamic=set();self.assets=[];self.research=[];self.doctrine=[]
        self.completed=set();self.capacity={};self.design=getattr(outputs,'design',None) or load_design()
        self.nodes={n['key']:n for n in self.design['nodes']}
        self.old_nodes={n['key']:n for n in baseline()['nodes']}
        self.c['IRQ'].var.update(gdp_total=10,treasury=10,literacy_rate=.35)
        import reward_overhaul
        states={557,166,171,1141,1142,1123}
        states.update(s for n in self.design['nodes'] for s,k,cnt in reward_overhaul.building_specs(n))
        for sid in states:
            if str(sid) not in self.s:
                from test_usa_module import Scope
                self.s[str(sid)]=Scope(str(sid))
            self.capacity[str(sid)]=10
        for output in [runtime_design.generate(ROOT),starting_spirits.generate(ROOT),outputs]:
            for path,source in output.items():
                if path.startswith('common/scripted_effects/'):
                    self.effects.update({k:v for k,o,v in parse(source)})
                elif path.startswith('common/scripted_triggers/'):
                    self.triggers.update({k:v for k,o,v in parse(source)})
        # Real native law-step provider, not a no-op API stand-in.
        native_budget=parse((ROOT/'common/scripted_effects/00_budget_effects.txt').read_text(encoding='utf-8-sig'))
        self.effects['decrease_corruption']=first(native_budget,'decrease_corruption')
    def test(self,k,o,v,c,root,prev,source):
        if k=='has_completed_focus':return v in self.completed
        if k=='has_dynamic_modifier':return first(v,'modifier') in self.dynamic
        if k=='free_building_slots':
            _,op,count=next(row for row in v if row[0]=='size')
            return self.compare(self.capacity.get(c.key,0),op,float(count))
        return super().test(k,o,v,c,root,prev,source)
    def run(self,rows,c,root=None,prev=None,source=None):
        root=root or c;taken=False
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
                name,_,value=v[0];c.var[name]/=self.num(value,c);continue
            if k=='add_dynamic_modifier':self.dynamic.add(first(v,'modifier'));continue
            if k=='remove_dynamic_modifier':self.dynamic.discard(first(v,'modifier'));continue
            if k=='force_update_dynamic_modifier':continue
            if k=='swap_ideas':
                c.ideas.pop(first(v,'remove_idea'),None);c.ideas[first(v,'add_idea')]=None;continue
            if k=='add_building_construction':
                count=int(first(v,'level'));self.capacity[c.key]-=count
                self.assets.append((c.key,first(v,'type'),count));continue
            if k in ['army_experience','air_experience','navy_experience']:
                key=k.removesuffix('_experience')+'_xp';c.var[key]=c.var.get(key,0)+float(v);continue
            if k=='update_literacy_rate':
                c.var['literacy_rate']=max(0,min(1,c.var['literacy_rate']+c.var.get('LR_change',0)));continue
            if k=='add_tech_bonus':self.research.append(dict((a,d) for a,b,d in v));continue
            if k=='add_doctrine_cost_reduction':self.doctrine.append(dict((a,d) for a,b,d in v));continue
            super().run([(k,o,v)],c,root,prev,source)
    def parents(self,key):
        for group in self.nodes[key]['prerequisites']:
            self.c['IRQ'].flags[group[0]+'_implemented']=None
            self.completed.add(group[0])
    def legacy(self,*keys):
        c=self.c['IRQ']
        for key in keys:
            c.flags[P+key+'_implemented']=None;self.completed.add(P+key)
            share=self.old_nodes[key]['budget_gdp_share']
            if share:
                c.var[P+key+'_invoice']=c.var['gdp_total']*share
                c.flags[P+key+'_quoted']=None
        return c
    def call_irq(self,key):self.call(P+key,'IRQ')


def near(a,b):assert math.isclose(a,b,abs_tol=1e-8),(a,b)


def pending_child_quote_regressions(out):
    """Exercise pre-v1 and repaired-v1 commitments through emitted effects."""
    checks=[]
    def pending(c,key,amount):
        c.flags[P+key+'_quoted']=None;c.flags[P+key+'_pending']=None
        c.var[P+key+'_invoice']=amount
    def upgraded_v1(c,key,amount):
        c.flags[audit_migration.VERSION]=None
        c.flags[P+key+'_audit_upgrade_pending']=None
        c.flags[P+key+'_audit_upgrade_quoted']=None
        c.var[P+key+'_audit_upgrade_invoice']=amount

    # An unpaid0.5 invoice is a GDP10 commitment, never a0.5 cash credit.
    for already_v1 in [False,True]:
        w=AuditWorld(out);w.parents('industry_heavy');c=w.legacy('industry_heavy')
        pending(c,'industry_steel',.5);w.completed.add(P+'industry_steel')
        c.var.update(gdp_total=100,treasury=.5)
        if already_v1:
            c.flags.pop(P+'industry_steel_pending')
            upgraded_v1(c,'industry_heavy',4.8)
        w.call_irq('migrate_audit_revision')
        near(c.var[audit_migration.quote_basis_variable(w.nodes['industry_heavy'])],10)
        near(c.var[P+'industry_heavy_audit_upgrade_invoice'],.3)
        near(c.var[P+'industry_steel_invoice'],.5)
        near(c.var['treasury'],.5);assert not w.assets and not w.research
        assert not w.flag(c,P+'industry_steel_pending')
        assert w.flag(c,audit_migration.QUOTE_VERSION)
        category=dict((k,v) for k,o,v in parse(out['common/decisions/COLDWAR_IRQ_1970_pending.txt']))['COLDWAR_IRQ_pending_projects']
        decisions={k:v for k,o,v in category if isinstance(v,list)}
        decision=decisions[P+'industry_heavy_audit_upgrade_delivery']
        assert w.tests(first(decision,'visible'),c) and w.tests(first(decision,'available'),c)
        c.var['gdp_total']=1000
        w.call_irq('migrate_audit_revision');w.call_irq('quote_upgrade_industry_heavy')
        near(c.var[P+'industry_heavy_audit_upgrade_invoice'],.3)
        w.call_irq('upgrade_industry_heavy');w.call_irq('upgrade_industry_heavy')
        w.call_irq('migrate_audit_revision')
        near(c.var['treasury'],.2)
        assert w.assets==[('557','industrial_complex',1)] and len(w.research)==1
    checks.append('Pre-v1 and already-v1 Heavy/Steel commitments preserve GDP10, charge0.3 rather than4.8, remain affordable and deliver once')

    # No valid unspent quote means genuinely new work still uses current GDP.
    for quoted,amount in [(False,.5),(True,0),(True,-.5),(False,0)]:
        w=AuditWorld(out);w.parents('industry_heavy');c=w.legacy('industry_heavy')
        c.var['gdp_total']=20;c.var[P+'industry_steel_invoice']=amount
        if quoted:c.flags[P+'industry_steel_quoted']=None
        w.call_irq('migrate_audit_revision');w.call_irq('quote_upgrade_industry_heavy')
        near(c.var[P+'industry_heavy_audit_upgrade_invoice'],.8)
        near(c.var[audit_migration.quote_basis_variable(w.nodes['industry_heavy'])],0)
    checks.append('Absent, nonpositive and unflagged child invoices never replace current-GDP pricing for unquoted new work')

    # A valid existing v1 supplementary quote with no unpaid child is frozen.
    w=AuditWorld(out);w.parents('industry_heavy');c=w.legacy('industry_heavy')
    upgraded_v1(c,'industry_heavy',.8);c.var['gdp_total']=100
    w.call_irq('migrate_audit_revision');w.call_irq('quote_upgrade_industry_heavy')
    near(c.var[P+'industry_heavy_audit_upgrade_invoice'],.8)
    checks.append('Already-v1 legitimate frozen top-ups without eligible child commitments are unchanged')

    # Both retired rural invoices are commitments. Select the lowest implied
    # GDP regardless of which source supplies it; neither unpaid bill is credit.
    for already_v1 in [False,True]:
        for credit_gdp,wasit_gdp in [(30,10),(10,30)]:
            w=AuditWorld(out);w.parents('agri_cooperatives');c=w.legacy('agri_cooperatives')
            pending(c,'agri_cooperative_credit',credit_gdp*.025)
            pending(c,'agri_wasit',wasit_gdp*.03)
            c.var['gdp_total']=100
            if already_v1:
                c.flags.pop(P+'agri_cooperative_credit_pending');c.flags.pop(P+'agri_wasit_pending')
                upgraded_v1(c,'agri_cooperatives',4)
            w.call_irq('migrate_audit_revision')
            near(c.var[audit_migration.quote_basis_variable(w.nodes['agri_cooperatives'])],10)
            near(c.var[P+'agri_cooperatives_audit_upgrade_invoice'],.4)
            assert not w.assets
            w.call_irq('upgrade_agri_cooperatives');w.call_irq('upgrade_agri_cooperatives')
            near(c.var['treasury'],9.6)
            assert w.assets==[('1141','agriculture_district',1)]
    checks.append('Multiple rural commitments deterministically use the lowest implied historical GDP; unpaid credit/Wasit bills do not finance the district')

    for key,child,old_invoice,expected in [
        ('oil_diversification','oil_industrial_fund',.5,.1),
        ('oil_revenue_state','oil_export_terminals',.35,.35),
    ]:
        for already_v1 in [False,True]:
            w=AuditWorld(out);w.parents(key);c=w.legacy(key)
            pending(c,child,old_invoice);c.var['gdp_total']=100
            if already_v1:
                c.flags.pop(P+child+'_pending');upgraded_v1(c,key,4)
            w.call_irq('migrate_audit_revision')
            near(c.var[P+key+'_audit_upgrade_invoice'],expected)
            cash=c.var['treasury'];w.call_irq('upgrade_'+key);w.call_irq('upgrade_'+key)
            near(c.var['treasury'],cash-expected);assert len(w.assets)==1
    checks.append('Oil factory and export-infrastructure merges preserve child GDP10 while deducting only real paid parent investment')

    # Defensive old-save recovery can also retain an ordinary pending invoice;
    # it must not manufacture a badge, implementation, assets or payment.
    w=AuditWorld(out);w.parents('industry_heavy');c=w.c['IRQ']
    pending(c,'industry_heavy',5);pending(c,'industry_steel',.5)
    c.flags[audit_migration.VERSION]=None;c.var['gdp_total']=100
    w.call_irq('migrate_audit_revision')
    near(c.var[P+'industry_heavy_invoice'],.5)
    assert not w.flag(c,P+'industry_heavy_implemented') and not w.assets and not w.research
    near(c.var['treasury'],10)
    checks.append('An already-v1 ordinary pending replacement can recover the child price basis without claiming delivery or charging')

    w=AuditWorld(out);c=w.c['IRQ'];c.flags[P+'industry_heavy_package_earned']=None
    w.completed.add(P+'industry_heavy');pending(c,'industry_steel',.5)
    c.var['gdp_total']=100
    w.call_irq('migrate_audit_revision')
    assert not w.flag(c,P+'industry_heavy_audit_upgrade_pending')
    assert not w.flag(c,P+'industry_heavy_audit_upgrade_quoted')
    assert all(not w.flag(c,x['receipt']) for x in w.nodes['industry_heavy']['audit_delivery_components'])
    assert not w.assets and not w.research;near(c.var['treasury'],10)
    checks.append('Earned policy/badge plus an unpaid child never invents financed delivery or an upgrade receipt')

    # Even if old child metadata survives, already delivered work is final.
    w=AuditWorld(out);c=w.legacy('industry_heavy');pending(c,'industry_steel',.5)
    c.flags.pop(P+'industry_steel_pending');c.flags[audit_migration.VERSION]=None
    c.flags[P+'industry_heavy_audit_upgrade_quoted']=None
    c.var[P+'industry_heavy_audit_upgrade_invoice']=4.8
    for component in w.nodes['industry_heavy']['audit_delivery_components']:
        c.flags[component['receipt']]=None
    c.var.update(gdp_total=100,treasury=5.2)
    w.call_irq('migrate_audit_revision');w.call_irq('upgrade_industry_heavy')
    near(c.var[P+'industry_heavy_audit_upgrade_invoice'],4.8)
    near(c.var['treasury'],5.2);assert not w.assets and not w.research
    assert not w.flag(c,P+'industry_heavy_audit_upgrade_pending')
    checks.append('Completed-v1 component receipts preserve the settled invoice and never refund, replay assets or reopen work')
    return checks


def main():
    # Preserve the v2 transaction contract as a distinct compatibility fixture.
    # Current direct-reward transactions have their own v3 regression suite.
    out=fresh_outputs(legacy=True);checks=[]
    for path,source in out.items():
        if path.endswith('.txt'):parse(source)
    checks.append('Pure focus/programme/queue compiler outputs parse; tests never write loaded content')

    w=AuditWorld(out);w.parents('industry_heavy');c=w.c['IRQ']
    w.call_irq('apply_industry_heavy');near(c.var['treasury'],9.5)
    assert w.assets==[('557','industrial_complex',1)] and len(w.research)==1
    w.call_irq('apply_industry_heavy');w.call_irq('migrate_audit_revision')
    near(c.var['treasury'],9.5);assert len(w.assets)==len(w.research)==1
    checks.append('Fresh Heavy programme charges 5% GDP and delivers one factory/research bonus once')

    w=AuditWorld(out);w.parents('industry_heavy');c=w.legacy('industry_heavy','industry_steel')
    w.call_irq('migrate_audit_revision');assert w.flag(c,P+'industry_heavy_audit_upgrade_pending')
    near(c.var[audit_migration.quote_basis_variable(w.nodes['industry_heavy'])],0)
    w.call_irq('upgrade_industry_heavy');near(c.var['treasury'],10)
    assert not w.assets and len(w.research)==1
    w.call_irq('upgrade_industry_heavy');w.call_irq('migrate_audit_revision');assert not w.assets and len(w.research)==1
    checks.append('Legacy Heavy plus Steel credits the delivered factory and full old financing; only the new research is granted once')

    w=AuditWorld(out);w.parents('industry_heavy');c=w.legacy('industry_heavy')
    w.call_irq('migrate_audit_revision');w.call_irq('quote_upgrade_industry_heavy')
    near(c.var[P+'industry_heavy_audit_upgrade_invoice'],.3)
    c.var['gdp_total']=100;w.call_irq('quote_upgrade_industry_heavy');near(c.var[P+'industry_heavy_audit_upgrade_invoice'],.3)
    w.call_irq('upgrade_industry_heavy');near(c.var['treasury'],9.7)
    assert w.assets==[('557','industrial_complex',1)] and len(w.research)==1
    w.call_irq('upgrade_industry_heavy');near(c.var['treasury'],9.7)
    checks.append('Legacy Heavy-only pays the frozen 3%-GDP supplementary quote exactly once for its missing factory/research')

    w=AuditWorld(out);w.parents('industry_heavy');c=w.legacy('industry_heavy')
    c.var['gdp_total']=20
    w.call_irq('migrate_audit_revision');w.call_irq('quote_upgrade_industry_heavy')
    near(c.var[P+'industry_heavy_audit_upgrade_invoice'],.8)
    c.var['gdp_total']=100;w.call_irq('quote_upgrade_industry_heavy')
    near(c.var[P+'industry_heavy_audit_upgrade_invoice'],.8)
    w.call_irq('upgrade_industry_heavy');near(c.var['treasury'],9.2)
    checks.append('Growing GDP does not invent larger historical financing: GDP20 total1 minus actual paid0.2 equals frozen0.8')

    w=AuditWorld(out);w.parents('industry_heavy');c=w.legacy('industry_heavy')
    c.var.pop(P+'industry_heavy_invoice');c.flags.pop(P+'industry_heavy_quoted')
    w.call_irq('migrate_audit_revision');w.call_irq('quote_upgrade_industry_heavy')
    near(c.var[P+'industry_heavy_audit_upgrade_invoice'],.5)
    checks.append('Missing historical payment amount creates no fabricated treasury credit')

    for invalid in ['funds','owner','controller','capacity','zero_gdp','skip','campaign']:
        w=AuditWorld(out);w.parents('industry_heavy');c=w.legacy('industry_heavy');w.call_irq('migrate_audit_revision')
        if invalid=='funds':c.var['treasury']=.299
        if invalid=='owner':w.s['557'].owner='PER'
        if invalid=='controller':w.s['557'].controller='PER'
        if invalid=='capacity':w.capacity['557']=0
        if invalid=='zero_gdp':c.var['gdp_total']=0
        if invalid=='skip':c.flags['MD_skip_treasury_cost']=None
        if invalid=='campaign':w.scenario=False
        cash=c.var['treasury'];w.call_irq('upgrade_industry_heavy')
        near(c.var['treasury'],cash);assert not w.assets and not w.research
    checks.append('Supplementary factory delivery rejects insufficient cash, ownership/control/capacity failure, zero GDP, skip-cost and wrong scenario')

    w=AuditWorld(out);w.parents('baath_future');c=w.legacy('baath_future')
    w.call_irq('migrate_audit_revision');c.var['ruling_party']=22;cash=c.var['treasury']
    w.call_irq('upgrade_baath_future');near(c.var['treasury'],cash);assert not w.research
    c.var['ruling_party']=21;w.call_irq('upgrade_baath_future');assert len(w.research)==1
    checks.append('A party-bound supplementary research grant waits for the exact governing party, then delivers once')

    w=AuditWorld(out);w.parents('defence_staff_training');c=w.legacy('defence_staff_training')
    c.var['army_xp']=15;w.call_irq('migrate_audit_revision');w.call_irq('upgrade_defence_staff_training')
    near(c.var['army_xp'],35);assert len(w.doctrine)==1
    w.call_irq('upgrade_defence_staff_training');near(c.var['army_xp'],35);assert len(w.doctrine)==1
    checks.append('Historical 15 Staff Training XP receives only 20 additional XP and the new doctrine reduction once')

    w=AuditWorld(out);w.parents('society_mass_literacy');c=w.legacy('society_mass_literacy')
    c.var['literacy_rate']=.375;w.call_irq('migrate_audit_revision');w.call_irq('upgrade_society_mass_literacy')
    near(c.var['literacy_rate'],.41)
    w.call_irq('upgrade_society_mass_literacy');near(c.var['literacy_rate'],.41)
    checks.append('Historical 2.5-point literacy receipt receives only 3.5 additional percentage points once')

    w=AuditWorld(out);c=w.c['IRQ'];c.flags[P+'industry_heavy_package_earned']=None
    w.completed.add(P+'industry_heavy');w.call_irq('migrate_audit_revision')
    components=w.nodes['industry_heavy']['audit_delivery_components']
    assert all(not w.flag(c,x['receipt']) for x in components)
    assert not w.flag(c,P+'industry_heavy_audit_upgrade_pending')
    assert all(c.var.get(audit_migration.credit_variable(x),0)==0 for x in components)
    checks.append('Policy-earned flags and native focus badges alone never count as paid delivery credits')

    w=AuditWorld(out);c=w.legacy('north_talks','industry_heavy','defence_mixed_supply')
    c.flags[P+'runtime_metadata_repaired_v1']=None
    w.call_irq('migrate_audit_revision')
    for key in ['north_talks','industry_heavy','defence_mixed_supply']:
        for decision in w.nodes[key]['decisions']:
            assert w.flag(c,decision['id']+'_unlocked'),decision['id']
    assert not w.assets and not w.research
    checks.append('Version migration restores new and relocated decision unlocks even when the earlier metadata-repair version already ran')

    w=AuditWorld(out);c=w.legacy('saddam_guard');c.leader='Saddam Hussein'
    c.flags[P+'saddam_guard_package_earned']=None;c.flags[P+'policy_saddam_saddam_guard']=None
    c.flags[P+'policy_saddam_saddam_party_cabinet']=None
    w.call_irq('reconcile_programmes');near(c.var[P+'saddam_army_org_factor'],.03)
    near(c.var[P+'saddam_army_defence_factor'],.04)
    c.var['ruling_party']=22;w.call_irq('reconcile_programmes')
    near(c.var[P+'saddam_army_org_factor'],0);assert P+'saddam_programme' not in w.dynamic
    c.var['ruling_party']=21;w.call_irq('reconcile_programmes')
    near(c.var[P+'saddam_army_org_factor'],.03)
    e=w.open('army_priority_review');w.choose(e,'The Regular Army')
    near(c.var[P+'saddam_army_org_factor'],0)
    near(c.var[P+'saddam_army_morale_factor'],.06)
    near(c.var[P+'saddam_training_time_army_factor'],-.08)
    near(c.var[P+'saddam_army_personnel_cost_multiplier_modifier'],.04)
    assert not w.assets and not w.research and c.var.get('army_xp',0)==0
    checks.append('Actual programme consumer removes/restores the leader policy and replaces Guard with regular-army values without replay')

    # Original positive pending quote was 2% of GDP10. Its authorized new5%
    # total is rescaled once from that same historical base, never liveGDP100.
    w=AuditWorld(out);w.parents('industry_heavy');c=w.c['IRQ']
    c.var.update({P+'industry_heavy_invoice':.2,'gdp_total':100})
    c.flags[P+'industry_heavy_quoted']=None;c.flags[P+'industry_heavy_pending']=None
    w.completed.add(P+'industry_heavy');w.call_irq('migrate_audit_revision')
    near(c.var[P+'industry_heavy_invoice'],.5)
    w.call_irq('migrate_audit_revision');near(c.var[P+'industry_heavy_invoice'],.5)
    w.call_irq('apply_industry_heavy');near(c.var['treasury'],9.5)
    checks.append('Unpaid old quote rescales to the new bundle from the original GDP once, rather than charging the live GDP or underfunding new assets')

    checks.extend(pending_child_quote_regressions(out))

    print(json.dumps({'scope':'Executed fresh compiler and native API boundaries; no loaded writes or HOI4 runtime claim','passed':len(checks),'checks':checks},indent=2))


if __name__=='__main__':main()
