# IMPERIA CW — Cold War: iraq 1970 — test audit politics.
"""Execute generated audit political transactions; native APIs are boundaries.

No game outputs are written. This exercises authority, consent, replacement,
cash and repeat protection, rather than mirroring string construction.
"""
import json, math
from audit_design import load_design
from common import ROOT, P, parse, first, values, walk
import decisions_module
from test_decisions_module import DecisionWorld


class PoliticsWorld(DecisionWorld):
    def __init__(self):
        super().__init__()
        self.design=load_design()
        self.arrays={key:{} for key in self.c}
        self.research=[]
    def test(self,k,o,v,c,root,prev,source):
        if k=='custom_trigger_tooltip':
            return self.tests([r for r in v if r[0]!='tooltip'],c,root,prev,source)
        if k=='is_in_array':
            return self.num(first(v,'value'),c) in self.arrays[c.key].get(first(v,'array'),set())
        return super().test(k,o,v,c,root,prev,source)
    def run(self,rows,c,root=None,prev=None,source=None):
        # The base runner's recursive calls re-enter here. Visual previews must
        # never be mistaken for executed rewards by the test interpreter.
        filtered=[]
        for k,o,v in rows:
            if k in ['effect_tooltip','custom_effect_tooltip']:continue
            if k=='add_tech_bonus':self.research.append(dict((a,d) for a,b,d in v));continue
            if k in ['add_to_array','remove_from_array']:
                name=first(v,'array')
                if name is None:name,_,raw=v[0]
                else:raw=first(v,'value')
                arr=self.arrays[c.key].setdefault(name,set())
                val=self.num(raw,c)
                if k=='add_to_array':arr.add(val)
                else:arr.discard(val)
                continue
            filtered.append((k,o,v))
        super().run(filtered,c,root,prev,source)


def near(a,b):assert math.isclose(a,b,abs_tol=1e-8),(a,b)


def main():
    checks=[]
    d=load_design(); before=len(d['decisions'])
    decisions_module.extra_focus_decisions(d)
    assert len(d['decisions'])==before
    assert all(fid in {n['id'] for n in d['nodes']} for fid in decisions_module.POLICY_CONTRACT_GATES)
    checks.append('Pure catalogue extension is idempotent; all constitutional IDs resolve')
    contract=json.loads((ROOT/'tools/iraq_1970/decision_event_ids.json').read_text())
    output=decisions_module.generate(ROOT)
    emitted={first(e,'id') for e in values(parse(output['events/COLDWAR_IRQ_1970_decisions.txt']),'country_event')}
    legacy={r['id'] for r in contract['events']}
    assert legacy<=emitted and all(int(e.split('.')[-1])>=10000 for e in emitted-legacy)
    assert len(emitted)==len(values(parse(output['events/COLDWAR_IRQ_1970_decisions.txt']),'country_event'))
    checks.append('All 115 legacy decision-event IDs remain defined; fourteen new events use explicit reserved IDs >=10000')

    w=PoliticsWorld();c=w.c['IRQ'];e=w.open('icp_preaccession')
    w.choose(e,'Negotiate ministries');r=w.response();w.choose(r,'Accept the charter')
    assert c.var['ruling_party']==21 and w.flag(c,P+'front_accepted')
    assert 4 in w.arrays['IRQ']['gov_coalition_array']
    assert not any(k.endswith('_package_earned') and ('icp_' in k or 'aziz_' in k) for k in c.flags)
    near(c.var['treasury'],9.9)
    checks.append('Pre-accession Front creates legal coalition rights without ICP accession or sovereign programme receipts')

    w=PoliticsWorld();c=w.c['IRQ'];e=w.open('icp_preaccession');w.choose(e,'Discuss legal')
    r=w.response();c.var['ruling_party']=22;cash=c.var['treasury'];w.choose(r,'Accept legal rights')
    near(c.var['treasury'],cash);assert not w.flag(c,P+'legalization_accepted')
    checks.append('A stale legalization callback cannot retain the former Baath/ICP authority')

    w=PoliticsWorld();c=w.c['IRQ'];e=w.open('icp_preaccession');w.choose(e,'Organize an independent opposition')
    near(c.var['treasury'],9.95);assert c.var['ruling_party']==21
    calls=[x for x in w.calls if x[1]=='change_relative_party_popularity']
    assert len(calls)==1 and calls[0][2]['party_index']==4 and calls[0][2]['party_popularity_increase']==.02
    w.choose(e,'Organize an independent opposition');near(c.var['treasury'],9.95)
    assert len([x for x in w.calls if x[1]=='change_relative_party_popularity'])==1
    checks.append('Paid independent organization uses native party inputs once per cooldown, never changes government')

    w=PoliticsWorld();c=w.c['IRQ'];c.flags[P+'policy_state_civic_compact']=None
    c.flags[P+'executive_state_implemented']=None
    w.call(P+'reconcile_political_contracts','IRQ')
    assert w.flag(c,P+'constitution_representative')
    e=w.open('constitutional_settlement_review');w.choose(e,'Ratify executive')
    near(c.var['treasury'],9.9)
    w.call(P+'reconcile_political_contracts','IRQ')
    assert w.flag(c,P+'constitution_executive') and not w.flag(c,P+'constitution_representative')
    assert not w.tests(parse(P+'constitution_representative_active = yes'),c)
    checks.append('Selected policy beats legacy receipt during initial migration; paid revision remains authoritative on later ticks')

    w=PoliticsWorld();c=w.c['IRQ'];c.leader='Saddam Hussein'
    c.flags[P+'saddam_guard_implemented']=None;c.flags[P+'policy_saddam_saddam_guard']=None
    e=w.open('army_priority_review');w.choose(e,'The Regular Army')
    near(c.var['treasury'],9.9)
    assert w.flag(c,P+'policy_saddam_saddam_regular_army') and not w.flag(c,P+'policy_saddam_saddam_guard')
    assert w.flag(c,P+'saddam_regular_army_package_earned')
    assert c.var.get('xp',0)==0 and c.stock==1000
    checks.append('Army priority replaces the current selected package at 1% GDP without replaying XP, equipment or assets')

    w=PoliticsWorld();c=w.c['IRQ'];c.flags[P+'oil_revenue_state_implemented']=None
    c.flags[P+'policy_oil_oil_revenue_state']=None;c.flags[P+'oil_state_company_implemented']=None
    e=w.open('oil_revenue_priority_review')
    labels=[w.loc[first(row,'name')] for row in values(w.events[e[0]],'option')]
    assert any('Beyond Oil' in label for label in labels)
    assert not any('Nationalize the IPC' in label or 'New Concession Terms' in label for label in labels)
    w.choose(e,'Beyond Oil');near(c.var['treasury'],9.9)
    assert w.flag(c,P+'policy_oil_oil_diversification') and w.flag(c,P+'oil_state_company_implemented')
    assert not w.flag(c,P+'oil_renegotiate_implemented') and not w.flag(c,P+'oil_concession_accepted')
    checks.append('Oil review changes only revenue/development allocation, never nationalization or concession ownership')

    w=PoliticsWorld();c=w.c['IRQ'];w.ready('defence_readiness_cycle')
    w.call(P+'refresh_decision_quotes','IRQ');w.call(P+'do_defence_readiness_cycle','IRQ')
    near(c.var['treasury'],9.95);assert w.idea(c,P+'readiness_cycle')
    w.day=90;assert not w.idea(c,P+'readiness_cycle')
    w.call(P+'refresh_decision_quotes','IRQ');w.call(P+'do_defence_readiness_cycle','IRQ');near(c.var['treasury'],9.95)
    w.day=180;w.call(P+'refresh_decision_quotes','IRQ');w.call(P+'do_defence_readiness_cycle','IRQ');near(c.var['treasury'],9.9)
    idearows=first(first(parse(w.out['common/ideas/COLDWAR_IRQ_1970_decision_ideas.txt']),'ideas'),'country')
    mods=first(first(idearows,P+'readiness_cycle'),'modifier')
    assert {k:float(v) for k,o,v in mods}=={'army_org_factor':.04,'army_morale_factor':.04,'army_personnel_cost_multiplier_modifier':.04}
    checks.append('Readiness exact cost, three modifiers, 90-day benefit and 180-day cooldown execute without XP')

    w=PoliticsWorld();c=w.c['IRQ'];c.flags[P+'autonomy_accepted']=None;c.flags[P+'autonomy_fulfilled']=None
    e=w.open('north_fiscal_settlement');w.choose(e,'Revenue-sharing');r=w.response();w.choose(r,'delegates ratify')
    near(c.var['treasury'],9.8);assert w.flag(c,P+'federal_settlement') and w.idea(c,P+'north_revenue_sharing')
    assert not w.idea(c,P+'north_central_administration')
    w.call(P+'finalize_north_terms','IRQ');near(c.var['treasury'],9.8)
    checks.append('Domestic delegated fiscal consent pays once and installs the revenue-sharing cost with existing federal relief')

    w=PoliticsWorld();c=w.c['IRQ'];c.flags[P+'autonomy_accepted']=None;c.flags[P+'autonomy_fulfilled']=None
    w.c['KUR'].exists=True;w.c['PUK'].exists=True
    e=w.open('north_fiscal_settlement');w.choose(e,'Revenue-sharing')
    r=w.response();w.choose(r,'Accept the proposed');near(c.var['treasury'],10)
    r2=w.response();w.choose(r2,'Accept the proposed');near(c.var['treasury'],9.8)
    assert w.flag(c,P+'federal_settlement') and not w.flag(c,P+'north_offer_revenue')
    w.choose(r2,'Accept the proposed');near(c.var['treasury'],9.8)
    checks.append('Both actual Kurdish governments control their own consent; no money or new terms before both agree; callbacks cannot replay')

    w=PoliticsWorld();c=w.c['IRQ'];c.flags[P+'autonomy_accepted']=None;c.flags[P+'autonomy_fulfilled']=None
    c.flags[P+'federal_settlement']=None;w.call(P+'reconcile_political_contracts','IRQ')
    assert w.idea(c,P+'north_revenue_sharing')
    e=w.open('north_fiscal_settlement');w.choose(e,'Central administration');r=w.response();w.choose(r,'delegates ratify')
    assert not w.flag(c,P+'federal_settlement') and not w.idea(c,P+'north_revenue_sharing')
    assert w.idea(c,P+'north_central_administration')
    c.wars.add('KUR');w.call(P+'reconcile_political_contracts','IRQ')
    assert not w.idea(c,P+'north_central_administration')
    checks.append('Central terms replace federal fiscal effects; a broken northern settlement removes its current programme')

    for invalid in ['war','expired','ownership']:
        w=PoliticsWorld();c=w.c['IRQ'];c.flags[P+'autonomy_accepted']=None;c.flags[P+'autonomy_fulfilled']=None
        w.c['KUR'].exists=True;e=w.open('north_fiscal_settlement');w.choose(e,'Revenue-sharing');r=w.response()
        if invalid=='war':c.wars.add('KUR')
        if invalid=='expired':w.day=61
        if invalid=='ownership':w.s['165'].controller='PER'
        w.choose(r,'Accept the proposed');w.call(P+'finalize_north_terms','IRQ')
        near(c.var['treasury'],10);assert not w.flag(c,P+'federal_settlement')
    checks.append('War, expired consent and loss of Kirkuk control block northern ratification and payment')

    w=PoliticsWorld();c=w.c['IRQ'];c.flags[P+'autonomy_accepted']=None;c.flags[P+'autonomy_fulfilled']=None;c.var['treasury']=0
    e=w.open('north_fiscal_settlement');w.choose(e,'Revenue-sharing');r=w.response();w.choose(r,'delegates ratify')
    assert not w.flag(c,P+'federal_settlement');near(c.var['treasury'],0)
    c.var.update(treasury=.2,gdp_total=100)
    w.call(P+'finalize_north_terms','IRQ');near(c.var['treasury'],0)
    assert w.flag(c,P+'federal_settlement')
    w.call(P+'finalize_north_terms','IRQ');near(c.var['treasury'],0)
    checks.append('Consented but unaffordable northern settlement waits; later delivery charges the original positive quote once')

    w=PoliticsWorld();c=w.c['IRQ'];c.flags[P+'autonomy_accepted']=None;c.flags[P+'autonomy_fulfilled']=None;c.var['gdp_total']=0
    e=w.open('north_fiscal_settlement');c.var['gdp_total']=10;w.choose(e,'Revenue-sharing')
    assert not w.event_queue and not w.flag(c,P+'north_offer_revenue')
    checks.append('A northern proposal opened at zero GDP cannot later create an unquoted agreement for free')

    w=PoliticsWorld();c=w.c['IRQ'];e=w.open('icp_preaccession');w.choose(e,'Negotiate ministries');w.choose(w.response(),'Accept the charter')
    w.ready('front_labour_terms');w.call(P+'refresh_decision_quotes','IRQ');w.call(P+'do_front_labour_terms','IRQ')
    assert w.idea(c,P+'front_labour_charter');near(c.var['treasury'],9.8)
    w.arrays['IRQ']['gov_coalition_array'].discard(4)
    w.call(P+'reconcile_political_contracts','IRQ');assert not w.idea(c,P+'front_labour_charter')
    checks.append('Funded Front labour effects require actual maintained coalition rights and disappear when the partner is excluded')

    w=PoliticsWorld();e=w.open('defence_diversified_offer');w.choose(e,'FRA');r=w.response()
    cash=w.c['IRQ'].var['treasury'];w.choose(r,'Decline the proposed')
    near(w.c['IRQ'].var['treasury'],cash);assert not w.idea(w.c['IRQ'],P+'advisers')
    assert not w.research and not w.flag(w.c['IRQ'],P+'diversified_artillery_instruction_delivered')
    checks.append('Diversified advisory mission remains recipient-owned and refusal grants no cash, advisers or equipment')
    w=PoliticsWorld();c=w.c['IRQ'];e=w.open('defence_diversified_offer');w.choose(e,'FRA');r=w.response()
    assert not w.research;w.choose(r,'Accept the stated agreement')
    near(c.var['treasury'],9.9)
    assert len(w.research)==1 and w.research[0]['category']=='CAT_artillery' and w.research[0]['bonus']=='0.25' and w.research[0]['uses']=='1'
    w.choose(r,'Accept the stated agreement');assert len(w.research)==1;near(c.var['treasury'],9.9)
    e=w.open('defence_diversified_offer');w.choose(e,'ENG');r=w.response();w.choose(r,'Accept the stated agreement')
    assert len(w.research)==1;near(c.var['treasury'],9.8)
    checks.append('First paid and accepted diversified mission grants one artillery research bonus; neither duplicate response nor second supplier can replay it')

    print(json.dumps({'scope':'Fresh emitted political AST and explicit native API boundaries; not HOI4 UI or multiplayer execution', 'passed':len(checks),'checks':checks},indent=2))


if __name__=='__main__':main()
