# IMPERIA CW — Cold War: iraq 1970 — test audit usa.
"""Focused emitted-AST checks for the approved 19 October US revision.

Reuses the strict transaction harness. This is not an HOI4 UI/battle emulator.
Generation remains in memory and no loaded game output is written.
"""
from pathlib import Path
import hashlib
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, values, walk
from usa_module import generate, P
from test_usa_module import World


class PolicyWorld(World):
    def test(self,k,o,v,c,root,prev,source):
        if k == 'has_deployed_air_force_size':
            _,op,amount=v[0]
            return self.compare(c.var.get('deployed_air',1),op,float(amount))
        if k == 'has_completed_focus': return v in c.flags.get('_completed',set())
        if k == 'has_variable': return v in c.var
        return super().test(k,o,v,c,root,prev,source)

    def run(self,rows,c,root=None,prev=None,source=None):
        # Tooltips are non-executing. Native goal arguments are validated before
        # recording their invocation; the engine's goal rules are not emulated.
        executable=[]
        for k,o,v in rows:
            if k in ('effect_tooltip','custom_effect_tooltip','unlock_decision_tooltip'):
                continue
            if k=='hidden_effect': executable.extend(v)
            elif k=='create_wargoal':
                assert first(v,'type')=='liberate_wargoal' and first(v,'target')=='IRQ'
                assert float(first(v,'expire'))==60
                executable.append(('set_country_flag','=','TEST_native_wargoal_invoked'))
            else: executable.append((k,o,v))
        return super().run(executable,c,root,prev,source)


def local(w,tag='KUR',sid='164'):
    w.c[tag].exists=True
    w.s[sid].owner=w.s[sid].controller=tag
    return w.c[tag]


def recognised(w):
    k=local(w);k.subject='IRQ';k.flags[P+'accord_consent']=None
    w.c['IRQ'].flags.update({'COLDWAR_IRQ_autonomy_accepted':None,'COLDWAR_IRQ_autonomy_fulfilled':None})
    w.c['IRQ'].wars.clear();k.wars.clear()


def external_offer(w):
    local(w)
    w.c['TUR'].flags[P+'fresh_north_consent']=None
    w.c['IRQ'].flags[P+'northern_emergency']=None
    w.call(P+'request_external_policy')


def main():
    before=hashlib.sha256((ROOT/'common/national_focus/USA_1970.txt').read_bytes()).hexdigest()
    live=first(parse((ROOT/'common/national_focus/USA_1970.txt').read_text(encoding='utf-8-sig')),'focus_tree')
    baseline=first(parse((ROOT/'tools/iraq_1970/integration_baseline/common/national_focus/USA_1970.txt').read_text(encoding='utf-8-sig')),'focus_tree')
    old=[f for f in values(live,'focus') if not first(f,'id').startswith(P)]
    assert len(old)==214 and old==values(baseline,'focus')
    out=generate(ROOT);assert out==generate(ROOT)
    for path,body in out.items():
        if path.endswith('.txt'):parse(body)
    checks=[]
    def done(name):checks.append(name)
    foci=values(parse(out['tools/iraq_1970/staged/USA_GULF_FOCUS_FRAGMENT.txt']),'focus')
    fs={first(f,'id'):f for f in foci}
    assert len(fs)==15 and sum(bool(first(f,'allow_branch')) for f in foci)==1
    assert first(first(fs[P+'contacts'],'allow_branch'),'always')=='no'
    assert float(first(fs[P+'desert_storm'],'cost'))==2
    assert not values(fs[P+'comfort'],'prerequisite') and not values(fs[P+'northern_access'],'prerequisite')
    assert not values(fs[P+'baghdad_accord'],'mutually_exclusive') and not values(fs[P+'self_rule'],'mutually_exclusive')
    assert [values(p,'focus') for p in values(fs[P+'self_rule'],'prerequisite')]==[[P+'assembly']]
    assert float(first(fs[P+'appeal'],'cost'))==3
    done('214 originalUSA focuses unchanged;15 registered IDs,14 visible, merged21-day channels,14-day Storm and independent relief roots')
    w=PolicyWorld(out);recognised(w);cash=w.c['USA'].var['treasury']
    w.call(P+'request_accord_policy')
    assert w.c['USA'].var[P+'current_settlement_policy']==1
    assert w.idea(w.c['IRQ'],P+'recognised_budget') and w.idea(w.c['KUR'],P+'recognised_development')
    assert w.c['USA'].var['treasury']==cash
    w.tick();assert math.isclose(w.c['USA'].var['treasury'],cash-.025/7)
    done('accepted existing legal autonomy receives one current recognised programme; true daily$.025bn/week bill')
    snapshot=(w.c['USA'].stock,w.c['KUR'].stock,w.c['KUR'].var['treasury'],w.s['164'].infrastructure)
    w.call(P+'commit_recognised_policy');w.call(P+'reconcile_settlement_policy')
    assert snapshot==(w.c['USA'].stock,w.c['KUR'].stock,w.c['KUR'].var['treasury'],w.s['164'].infrastructure)
    assert w.c['USA'].var[P+'accord_days']==89
    done('repeat reconciliation/commit does not renew a term or replay assets, treasury grants or equipment')
    w.c['USA'].var['treasury']=0;w.tick()
    assert not w.idea(w.c['IRQ'],P+'recognised_budget') and not w.idea(w.c['KUR'],P+'recognised_development')
    assert w.c['USA'].var[P+'accord_days']==0
    done('recognised insolvency removes all own programme effects on the same tick')
    w=PolicyWorld(out);local(w);w.call(P+'request_accord_policy')
    assert w.flag(w.c['USA'],P+'settlement_policy_offer')
    assert w.c['USA'].var.get(P+'current_settlement_policy',0)==0
    assert not w.c['KUR'].subject
    done('a request cannot turn refusal or an unfinished Baghdad negotiation into recognised autonomy')
    w=PolicyWorld(out);external_offer(w)
    assert w.c['USA'].var.get(P+'current_settlement_policy',0)==0
    assert w.flag(w.c['KUR'],P+'protection_offer')
    w.accept(52)
    assert w.c['USA'].var[P+'current_settlement_policy']==2
    assert w.idea(w.c['KUR'],P+'external_guarantee')
    assert w.idea(w.c['USA'],P+'northern_air_readiness')
    assert not w.c['KUR'].subject and not w.c['USA'].wars
    cash=w.c['USA'].var['treasury'];w.tick()
    assert math.isclose(cash-w.c['USA'].var['treasury'],.05/7)
    done('recipient accepts external commitment, normal air preparation retained, protection bill charged once only')
    w=PolicyWorld(out);external_offer(w);w.accept(52,option=1)
    assert w.c['USA'].var.get(P+'current_settlement_policy',0)==0
    assert not w.idea(w.c['KUR'],P+'external_guarantee') and w.c['USA'].var['treasury']==10
    done('local protection refusal leaves money, territory, status and programme unchanged')
    w=PolicyWorld(out);local(w,'PUK','1078');external_offer(w);w.accept(52)
    assert w.c['USA'].var.get(P+'current_settlement_policy',0)==0
    w.accept(52,'PUK');assert w.c['USA'].var[P+'current_settlement_policy']==2
    assert w.idea(w.c['KUR'],P+'external_guarantee') and w.idea(w.c['PUK'],P+'external_guarantee')
    done('both eligible local governments must independently consent')
    w=PolicyWorld(out);local(w);w.c['TUR'].flags[P+'fresh_north_consent']=None;w.c['USA'].var['deployed_air']=0
    w.call(P+'request_external_policy');assert not w.flag(w.c['USA'],P+'settlement_policy_offer')
    w.c['USA'].var['deployed_air']=1;w.c['TUR'].flags.pop(P+'fresh_north_consent')
    w.call(P+'request_external_policy');assert not w.flag(w.c['USA'],P+'settlement_policy_offer')
    done('external policy cannot bypass actual air deployment or fresh consent from a valid host')
    w=PolicyWorld(out);external_offer(w);w.accept(52)
    recognised(w);cash=w.c['USA'].var['treasury'];w.call(P+'request_accord_policy')
    assert w.c['USA'].var[P+'current_settlement_policy']==1 and math.isclose(cash-w.c['USA'].var['treasury'],.25)
    assert not w.idea(w.c['USA'],P+'northern_air_readiness') and not w.idea(w.c['KUR'],P+'external_guarantee')
    assert w.idea(w.c['IRQ'],P+'recognised_budget') and w.c['USA'].var[P+'protection_days']==0
    w.call(P+'commit_recognised_policy');assert math.isclose(cash-w.c['USA'].var['treasury'],.25)
    done('paid$.25bn revision changes current stance once and immediately replaces incompatible air/protection effects')
    w=PolicyWorld(out);external_offer(w);w.accept(52);w.call(P+'withdraw_settlement_policy')
    assert w.c['USA'].var[P+'last_settlement_policy']==2
    recognised(w);cash=w.c['USA'].var['treasury'];w.call(P+'request_accord_policy')
    assert math.isclose(cash-w.c['USA'].var['treasury'],.25)
    done('withdrawal cannot erase the previous policy and evade a revision invoice')
    w=PolicyWorld(out);local(w).subject='IRQ';local(w,'PUK','1078')
    w.call(P+'request_accord_policy');w.accept(30,'IRQ');w.accept(31,'KUR')
    assert math.isclose(w.c['IRQ'].var['treasury'],10)
    w.accept(31,'PUK');assert w.c['PUK'].subject=='IRQ'
    assert math.isclose(w.c['IRQ'].var['treasury'],9.8)
    w.tick();assert w.c['USA'].var[P+'current_settlement_policy']==1
    w.accept(31,'PUK');assert math.isclose(w.c['IRQ'].var['treasury'],9.8)
    done('mixed existingIRQ-autonomy and independentPUK can both ratify; Iraq pays its native2%GDP contribution once')
    w=PolicyWorld(out);local(w);w.call(P+'request_accord_policy');w.accept(30,'IRQ',option=1)
    assert not w.flag(w.c['USA'],P+'settlement_policy_offer') and w.c['USA'].var['treasury']==10
    done('Baghdad refusal immediately closes the pendingUS request without charging the revision invoice')
    w=PolicyWorld(out);recognised(w);w.c['USA'].var[P+'last_settlement_policy']=2;w.c['USA'].var['treasury']=.25
    w.call(P+'request_accord_policy');assert w.c['USA'].var.get(P+'current_settlement_policy',0)==0
    assert w.c['USA'].var['treasury']==.25
    w.c['USA'].var['treasury']=.25+.025/7+1e-7;w.tick()
    assert w.c['USA'].var[P+'current_settlement_policy']==1
    assert math.isclose(w.c['USA'].var['treasury'],1e-7,abs_tol=1e-9)
    w.tick()
    assert not w.idea(w.c['IRQ'],P+'recognised_budget')
    done('revision and first funded day checked together; fee-only balance fails, funded day pays once then insolvency expires')
    w=PolicyWorld(out);external_offer(w);w.accept(52);w.c['USA'].access.clear();w.tick()
    assert not w.idea(w.c['KUR'],P+'external_guarantee') and w.c['USA'].var[P+'protection_days']==0
    done('lost access removes protection benefit and closes its recurring budget')
    w=PolicyWorld(out);external_offer(w);w.accept(52);cash=w.c['USA'].var['treasury']
    w.call(P+'escalate_protection');assert w.c['USA'].var['treasury']==cash
    w.c['KUR'].wars.add('IRQ');w.c['IRQ'].wars.add('KUR')
    w.call(P+'escalate_protection');assert math.isclose(w.c['USA'].var['treasury'],cash-.5)
    assert w.flag(w.c['USA'],'TEST_native_wargoal_invoked') and not w.c['USA'].wars
    w.call(P+'escalate_protection');assert math.isclose(w.c['USA'].var['treasury'],cash-.5)
    done('one paid60-day intervention goal requires actual protected-party fighting; never automatic war')
    w=PolicyWorld(out);w.c['USA'].var[P+'relief_days']=90;w.c['IRQ'].flags[P+'northern_emergency']=None
    cash=w.c['USA'].var['treasury'];w.tick();assert math.isclose(cash-w.c['USA'].var['treasury'],.025/7)
    w.c['USA'].flags[P+'programme_limited_war']=None;cash=w.c['USA'].var['treasury'];w.tick()
    assert math.isclose(cash-w.c['USA'].var['treasury'],.02/7)
    done('limited-war choice has actual reduced humanitarian upkeep; armed programme keeps its separate real support costs')
    dec=first(parse(out['common/decisions/COLDWAR_USA_gulf_decisions.txt']),P+'category')
    definitions={k for k,_,v in dec}
    links=[v for f in foci for k,_,v in walk(f) if k=='unlock_decision_tooltip']
    assert set(links)<=definitions, set(links)-definitions
    for name in ('revise_accord','revise_external','escalate_protection'):
        assert float(first(first(dec,P+name),'cost'))==100
    assert 'country_event = { id = COLDWAR_USA_gulf_events.30' not in str(values(w.events[P+'events.43'],'option')[0])
    done('revision/escalation decisions have native100PP cost; notification options do not bypass the paid decisions')
    w=PolicyWorld(out);external_offer(w);w.accept(52)
    w.run(first(first(dec,P+'decline_protection'),'complete_effect'),w.c['KUR'])
    assert w.c['USA'].var[P+'current_settlement_policy']==0
    assert w.c['USA'].var[P+'last_settlement_policy']==2
    assert not w.idea(w.c['KUR'],P+'external_guarantee') and not w.idea(w.c['USA'],P+'northern_air_readiness')
    assert not w.c['KUR'].subject
    done('local government can withdraw its consent; no territorial/status changes or revision-fee reset')
    w=PolicyWorld(out);external_offer(w);cash=w.c['USA'].var['treasury']
    w.run(first(first(dec,P+'cancel_policy_offer'),'complete_effect'),w.c['USA'])
    w.accept(52)
    assert not w.flag(w.c['USA'],P+'settlement_policy_offer') and w.c['USA'].var['treasury']==cash
    assert w.c['USA'].var[P+'current_settlement_policy']==0
    done('pending offers can be cancelled; stale recipient acceptance cannot charge money or activate a stance')
    w=PolicyWorld(out);w.c['USA'].flags.update({P+'relief_initial_paid':None,P+'programme_limited_war':None});w.c['IRQ'].flags[P+'northern_emergency']=None
    w.c['USA'].var['treasury']=.02/7
    relief=first(dec,P+'refugees')
    assert w.tests(first(relief,'available'),w.c['USA'])
    w.run(first(relief,'complete_effect'),w.c['USA']);assert w.c['USA'].var[P+'relief_days']==90
    w.c['USA'].flags.pop(P+'relief_initial_paid');w.c['USA'].var['treasury']=.5
    assert not w.tests(first(relief,'available'),w.c['USA'])
    done('limited-relief decision uses its actual lower daily price; initial mobilisation must also fund the first operating day')
    assert before==hashlib.sha256((ROOT/'common/national_focus/USA_1970.txt').read_bytes()).hexdigest()
    report={'scope':'Read-only generation + strict bounded emitted-AST execution; not an engine/UI test','passed':len(checks),'checks':checks,'registered_focuses':15,'active_focuses':14,'original_usa_loaded_file_unchanged_sha256':before,'positions':{i:[first(f,'x'),first(f,'y')] for i,f in fs.items()}}
    dest=ROOT/'docs/design/iraq_1970/audit_2026_10_19/US_IMPLEMENTATION_TESTS.json';dest.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
