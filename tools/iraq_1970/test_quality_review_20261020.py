# IMPERIA CW — Cold War: iraq 1970 — test quality review 20261020.
"""Execute the approved finite review contract and capped Libya reward.

Tests use emitted/installed script AST. Native engine semantics are bounded
explicitly; this is not a HOI4 or multiplayer runtime test.
"""
from datetime import date
import json
from pathlib import Path
import re
import sys

from common import ROOT, P, parse, first, values
from test_decisions_module import DecisionWorld
from prison_review import CASES, ELIGIBLE, PENDING


class QualityWorld(DecisionWorld):
    pass


def main():
    checks=[]
    def done(message):checks.append(message)
    w=QualityWorld();w.ready('prison_review');c=w.c['IRQ']
    trigger=w.triggers[ELIGIBLE]
    for year,month,day,expected in [(1970,1,1,True),(1971,11,28,True),(1972,12,31,True),(1973,1,1,False)]:
        w.date=date(year,month,day)
        assert w.tests(trigger,c,c,None,None)==expected
    done('Review reaches remaining living cases within exact deadlines and expires at1973-01-01')
    w.date=date(1970,1,1)
    c.flags[P+'dukhayl_dead']=None;c.flags[P+'rikabi_dead']=None
    assert not w.tests(trigger,c,c,None,None)
    c.flags.clear()
    for _,_,settled in CASES:c.flags[P+settled]=None
    assert not w.tests(trigger,c,c,None,None)
    done('Dead or fully settled cases cannot keep a paid review available')

    # Select the actual native decision completion payload after its30PP cost.
    w=QualityWorld();w.ready('prison_review');c=w.c['IRQ'];c.var['political_power']=70
    ast=parse(w.out['common/decisions/COLDWAR_IRQ_1970_decisions.txt'])
    decision=first(first(ast,P+'1970_decisions'),P+'decision_prison_review')
    complete=first(decision,'complete_effect')
    w.run(complete,c)
    assert w.flag(c,PENDING)
    assert not w.tests(first(decision,'available'),c,c,None,None)
    shown=w.show(*reversed(w.event_queue.pop()))
    w.date=date(1973,1,1);cash=c.var['treasury']
    w.choose(shown,'Release and rehabilitate') # deliberately bypass option visibility
    assert c.var['treasury']==cash and c.var['political_power']==100
    assert not w.idea(c,P+'negotiation_cost') and not w.flag(c,PENDING)
    w.choose(shown,'Release and rehabilitate');w.choose(shown,'Close the conference')
    assert c.var['political_power']==100 and c.var['treasury']==cash
    done('An expired open event refunds exactly30PP, charges no cash/malus and cannot replay the refund')

    w=QualityWorld();e=w.open('prison_review');c=w.c['IRQ'];c.flags[P+'dukhayl_dead']=None;c.flags[P+'rikabi_dead']=None
    w.choose(e,'Retain detention')
    assert c.var['political_power']==30 and c.var['treasury']==10 and not c.ideas
    done('Deaths while the menu is open invalidate both paid and retention branches')

    w=QualityWorld();e=w.open('prison_review');c=w.c['IRQ'];c.flags.pop(P+'review_detentions_implemented')
    w.choose(e,'Close the conference')
    assert c.var['political_power']==30 and not w.flag(c,PENDING)
    done('Loss of programme authority releases the session and refunds its native fee')

    w=QualityWorld();e=w.open('prison_review');c=w.c['IRQ'];c.var['gdp_total']=100
    w.choose(e,'Release and rehabilitate')
    assert abs(c.var['treasury']-9.95)<1e-9 and c.var.get('political_power',0)==0
    assert all(w.flag(c,P+settled) for _,_,settled in CASES)
    assert w.idea(c,P+'negotiation_cost') and not w.flag(c,PENDING)
    assert not w.tests(w.triggers[ELIGIBLE],c,c,None,None)
    w.choose(e,'Release and rehabilitate')
    assert abs(c.var['treasury']-9.95)<1e-9 and c.var.get('political_power',0)==0
    done('Successful review pays the frozen0.5%GDP invoice once and settles only eligible actual cases')

    w=QualityWorld();w.ready('prison_review');c=w.c['IRQ'];w.date=date(1973,1,1);c.flags[PENDING]=None
    w.call(P+'do_prison_review','IRQ')
    assert c.var['political_power']==30 and not w.event_queue
    done('Eligibility lost between decision click and callback refunds before opening the menu')

    w=QualityWorld();w.ready('prison_review');c=w.c['IRQ']
    c.flags[P+'D_prison_review_quoted']=None
    c.var[P+'D_prison_review_invoice']=.00001
    w.run(complete,c);shown=w.show(*reversed(w.event_queue.pop()))
    assert abs(c.var[P+'D_prison_review_invoice']-.05)<1e-9
    w.choose(shown,'Close the conference')
    assert not w.flag(c,PENDING) and c.var.get('political_power',0)==0
    assert P+'D_prison_review_invoice' not in c.var
    done('A new native review discards legacy stale quotes; voluntary closing clears the session without fabricating a refund')

    # Compare installed contracts with the freshly generated canonical module.
    for path,key in [
        ('common/scripted_effects/COLDWAR_IRQ_1970_decision_effects.txt',P+'do_prison_review'),
        ('common/scripted_effects/COLDWAR_IRQ_1970_decision_effects.txt',P+'cancel_prison_review'),
        ('common/scripted_triggers/COLDWAR_IRQ_1970_decision_triggers.txt',ELIGIBLE)]:
        assert first(parse((ROOT/path).read_text(encoding='utf-8')),key)==first(parse(w.out[path]),key)
    path='events/COLDWAR_IRQ_1970_decisions.txt'
    extract=lambda text:next(v for v in values(parse(text),'country_event') if first(v,'id')=='COLDWAR_IRQ_decision_events.139')
    assert extract((ROOT/path).read_text(encoding='utf-8'))==extract(w.out[path])
    installed=first(first(parse((ROOT/'common/decisions/COLDWAR_IRQ_1970_decisions.txt').read_text(encoding='utf-8')),P+'1970_decisions'),P+'decision_prison_review')
    assert installed==decision
    done('Installed decision, event, eligibility and refund helpers exactly match canonical generated AST')

    focus=next(v for v in values(first(parse((ROOT/'common/national_focus/libya_1970.txt').read_text(encoding='utf-8')),'focus_tree'),'focus') if first(v,'id')=='LBA_1970_the_revolution_delivers')
    reward=first(focus,'completion_reward')
    budget=first(parse((ROOT/'common/scripted_effects/00_budget_effects.txt').read_text(encoding='utf-8')),'increase_healthcare_budget')
    for start,end,pp in [('health_03','health_04',0),('health_06','health_06',150)]:
        w=QualityWorld();c=w.c['IRQ'];c.ideas[start]=None;w.effects['increase_healthcare_budget']=budget
        w.run([r for r in reward if r[0]!='log'],c)
        assert end in c.ideas and c.var.get('political_power',0)==pp
        assert abs(c.var['stability']-.03)<1e-9
        assert c.ideas['LBA_1970_public_health_administration']==730
    idea=first(first(first(parse((ROOT/'common/ideas/LBA_1970_ideas.txt').read_text(encoding='utf-8')),'ideas'),'country'),'LBA_1970_public_health_administration')
    assert first(first(idea,'modifier'),'health_cost_multiplier_modifier')=='-0.05'
    done('Libya capstone advances native healthcare or grants its150PP fallback; both paths gain3pp stability and730day5%cost saving')

    sys.path.insert(0,str(ROOT/'tools/israel_1970'))
    from programme_narrative import NARRATIVE
    from revised_rewards import SPECS
    loc=(ROOT/'localisation/english/ISR70_l_english.yml').read_text(encoding='utf-8-sig')
    for key,(label,desc) in NARRATIVE.items():
        assert ' ISR70_'+key+':0 '+json.dumps(label,ensure_ascii=False) in loc
        assert ' ISR70_'+key+'_desc:0 '+json.dumps(desc,ensure_ascii=False) in loc
        assert key in SPECS
    assert len({d for _,d in NARRATIVE.values()})==100
    lba=(ROOT/'localisation/english/LBA_1970_l_english.yml').read_text(encoding='utf-8-sig')
    assert not re.search(r'_desc:0 "Effects?:',lba)
    assert not re.search(r'_desc:0 ".*\bstates? \d',lba)
    done('100 unique Israeli programme narratives match installed names/descriptions; Libya has no remaining effect-catalogue descriptions or raw state IDs')
    for path in [ROOT/'common/national_focus/libya_1970.txt',ROOT/'common/ideas/LBA_1970_ideas.txt',ROOT/'common/decisions/COLDWAR_IRQ_1970_decisions.txt',ROOT/'common/scripted_effects/COLDWAR_IRQ_1970_decision_effects.txt',ROOT/'common/scripted_triggers/COLDWAR_IRQ_1970_decision_triggers.txt',ROOT/'events/COLDWAR_IRQ_1970_decisions.txt']:
        assert not path.read_bytes().startswith(b'\xef\xbb\xbf');parse(path.read_text(encoding='utf-8'))
    for path in [ROOT/'localisation/english/LBA_1970_l_english.yml',ROOT/'localisation/english/ISR70_l_english.yml',ROOT/'localisation/english/COLDWAR_IRQ_1970_decisions_l_english.yml']:
        assert path.read_bytes().startswith(b'\xef\xbb\xbf')
    done('All changed live scripts parse without BOM; English localisation retains UTF8BOM')
    print(json.dumps({'passed':len(checks),'checks':checks,'limits':'Static AST execution; no HOI4 engine or multiplayer test'},indent=2))


if __name__=='__main__':main()
