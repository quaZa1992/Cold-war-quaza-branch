# IMPERIA COLD WAR — Oversupply price, cooldown and global dispatch regression checks.
"""Execute the installed oil ASTs in a bounded model. No game or MP session is launched."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal
import json,sys,hashlib,unittest,re,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from guest_workers import validate as V

FX='common/scripted_effects/imp_oil_prices_scripted_effects.txt'
HOOK='common/on_actions/zzzzzz_imp_oil_prices_on_actions.txt'
EVENTS='events/imp_oil_events.txt'
LOC='localisation/english/imp_oil_price_l_english.yml'
EFFECTS={k:v for k,o,v in V.parse((ROOT/FX).read_text(encoding='utf8'))}
H=V.first(V.parse((ROOT/HOOK).read_text(encoding='utf8')),'on_actions')
MONTHLY=next(v for k,o,v in H if k=='on_monthly_LIC' and any(kk=='imp_random_global_oil_event' for kk,oo,vv in V.walk(v)))
TABLE=V.first(EFFECTS['imp_random_global_oil_event'],'random_list')
OVERSUPPLY=next((k,v) for k,o,v in TABLE if any(kk=='COLDWAR_oil_oversupply_shock' for kk,oo,vv in v))
BASELINE=json.loads((HERE/'OVERSUPPLY_BASELINE.json').read_text(encoding='utf8'))
D=V.D

def digest(tree):return hashlib.sha256(json.dumps(tree,ensure_ascii=False).encode()).hexdigest()

class OilModel(V.ScriptMachine):
    def __init__(self,price='75'):
        super().__init__(EFFECTS,{})
        self.global_scope=V.Country('GLOBAL');self.countries={tag:V.Country(tag) for tag in ('LIC','USA','SOV','SAU')}
        self.root=self.current=self.countries['LIC'];self.origin=self.countries['USA'];self.previous=self.root
        self.global_scope.variables.update(imp_global_oil_price=D(price),imp_global_oil_price_equilibrium=D(75),imp_oil_price_base_unit=D('.024'),mdcw_cw_oil_level=D(1),mdcw_cw_cpi=D(1),mdcw_cw_oil_embargo_world_multiplier=D(1))
        self.draws=0
    def scope(self,name):
        if name.lower()=='global':return self.global_scope
        return super().scope(name)
    def test(self,body):
        for k,o,v in body:
            if k=='has_global_flag':answer=v in self.global_scope.flags
            elif k=='has_variable':
                scope,name=self.resolve_variable(v);answer=name in scope.variables or name in scope.temporary
            else:answer=super().test([(k,o,v)])
            if not answer:return False
        return True
    def weight(self,key,body):
        result=D(key)
        for k,o,v in body:
            if k=='modifier' and self.test([row for row in v if row[0]!='factor']):result*=D(V.first(v,'factor'))
        return result
    def execute(self,body):
        pending=[]
        for k,o,v in body:
            if k not in ('set_global_flag','random_list'):
                pending.append((k,o,v));continue
            if pending:super().execute(pending);pending=[]
            if k=='set_global_flag':
                flag=v if isinstance(v,str) else V.first(v,'flag')
                self.global_scope.flags[flag]=D(0) if isinstance(v,str) else D(V.first(v,'days','0'))
                self.global_scope.flag_started[flag]=self.now
            else:
                self.draws+=1
                # Force the oversupply branch to test the actual dispatcher and its guards.
                # This is deterministic branch coverage, not an engine RNG simulation.
                candidate=next((body for weight,op,body in v if any(key=='COLDWAR_oil_oversupply_shock' for key,op,value in body)),None)
                assert candidate is not None
                assert self.weight(OVERSUPPLY[0],candidate)>0,'Attempted to select an excluded branch'
                self.execute([row for row in candidate if row[0]!='modifier'])
        if pending:super().execute(pending)
    def elapse(self,days):
        self.now+=D(days)
        for flag,ttl in list(self.global_scope.flags.items()):
            if ttl>0 and self.now-self.global_scope.flag_started[flag]>=ttl:
                self.global_scope.flags.pop(flag);self.global_scope.flag_started.pop(flag)

class OversupplyChecks(unittest.TestCase):
    def test_price_drop_is_one_percent_and_preserves_equilibrium_and_policies(self):
        for price in ('15','15.1','30','50','75','135','200'):
            with self.subTest(price=price):
                m=OilModel(price);before=dict(m.global_scope.variables);m.call('COLDWAR_oil_oversupply_shock')
                expected=max(D(15),D(price)*D('.99'))
                self.assertEqual(m.get('global.imp_global_oil_price'),expected)
                self.assertGreaterEqual(expected,D(price)*D('.99'))
                for key in ('imp_global_oil_price_equilibrium','mdcw_cw_oil_level','mdcw_cw_cpi','mdcw_cw_oil_embargo_world_multiplier'):self.assertEqual(m.get('global.'+key),before[key])
                self.assertEqual(m.get('global.imp_oil_price_display'),expected*D('.024'))
                self.assertEqual(len(m.queue),1)
    def test_display_scales_with_opec_cpi_and_embargo_without_amplifying_percentage(self):
        m=OilModel('30');m.global_scope.variables.update(mdcw_cw_oil_level=D(4),mdcw_cw_cpi=D('1.5'),mdcw_cw_oil_embargo_world_multiplier=D('1.2'))
        m.call('imp_update_oil_price_display');before=m.get('global.imp_oil_price_display');m.call('COLDWAR_oil_oversupply_shock')
        self.assertEqual(m.get('global.imp_oil_price_display'),before*D('.99'))
    def test_repeat_direct_calls_and_other_countries_cannot_stack_the_price_drop(self):
        m=OilModel();m.call('COLDWAR_oil_oversupply_shock');before=deepcopy(m.global_scope.variables)
        for scope in m.countries.values():
            m.in_scope(scope,lambda:m.call('COLDWAR_oil_oversupply_shock'))
        self.assertEqual(m.global_scope.variables,before);self.assertEqual(len(m.queue),1)
    def test_cooldown_survives_global_state_reload_and_expires_after_730_days(self):
        m=OilModel();m.call('COLDWAR_oil_oversupply_shock')
        saved=deepcopy(m.global_scope);resumed=OilModel();resumed.global_scope=saved
        resumed.elapse(729);before=resumed.get('global.imp_global_oil_price');resumed.call('COLDWAR_oil_oversupply_shock');self.assertEqual(resumed.get('global.imp_global_oil_price'),before)
        resumed.elapse(1);resumed.call('COLDWAR_oil_oversupply_shock');self.assertEqual(resumed.get('global.imp_global_oil_price'),before*D('.99'))
    def test_draw_weight_is_halved_and_zero_while_the_specific_cooldown_is_active(self):
        m=OilModel();weight=m.weight(*OVERSUPPLY);total=sum(m.weight(k,v) for k,o,v in TABLE)
        self.assertEqual(weight,D(BASELINE['baseline_weight'])/2);self.assertEqual(total,D(185))
        self.assertLess(weight/total,D(BASELINE['baseline_weight'])/D(BASELINE['baseline_total_weight']))
        m.call('COLDWAR_oil_oversupply_shock');self.assertEqual(m.weight(*OVERSUPPLY),0)
        m.elapse(730);self.assertEqual(m.weight(*OVERSUPPLY),weight)
    def test_existing_global_monthly_dispatch_runs_once_across_repeated_country_invocations(self):
        m=OilModel();body=V.first(MONTHLY,'effect');m.execute(body)
        self.assertEqual(m.draws,1);self.assertEqual(m.get('global.imp_global_oil_price'),D('74.25'))
        for scope in m.countries.values():m.in_scope(scope,lambda:m.execute(body))
        self.assertEqual(m.draws,1);self.assertEqual(len(m.queue),1)
        m.elapse(232);self.assertNotIn('imp_oil_random_event_done',m.global_scope.flags)
        self.assertEqual(m.weight(*OVERSUPPLY),0)
    def test_broadcast_event_buttons_have_no_second_global_price_effect(self):
        tree=V.parse((ROOT/EVENTS).read_text(encoding='utf-8-sig'));event=next(v for k,o,v in tree if k=='country_event' and V.first(v,'id')=='imp_oil.21')
        self.assertEqual(digest(event),BASELINE['news_event_sha256'])
        for option in V.values(event,'option'):self.assertFalse([r for r in option if r[0] not in ('name','ai_chance','trigger')])
    def test_all_other_random_branches_and_shared_war_gc_spike_math_are_unchanged(self):
        for key,sha in BASELINE['preserved_effects'].items():self.assertEqual(digest(EFFECTS[key]),sha,key)
        remaining=[dict(weight=k,sha256=digest(v)) for k,o,v in TABLE if (k,v)!=OVERSUPPLY]
        self.assertEqual(remaining,BASELINE['preserved_random_branches'])
        self.assertEqual(digest(V.parse((ROOT/HOOK).read_text(encoding='utf8'))),BASELINE['scheduler_sha256'])
        m=OilModel();m.current.temporary['oil_cost_multiplier_t']=D('.3');m.call('imp_spike_oil_price');self.assertEqual(m.get('global.imp_global_oil_price'),D('97.5'))
    def test_weekly_market_recovery_still_uses_the_existing_equilibrium(self):
        m=OilModel();m.call('COLDWAR_oil_oversupply_shock');body=EFFECTS['imp_weekly_oil_price_change']
        end=next(i for i,(k,o,v) in enumerate(body) if k=='if' and any(kk=='every_country' for kk,oo,vv in V.walk(v)))
        for _ in range(16):m.execute(body[:end])
        self.assertLess(D(75)-m.get('global.imp_global_oil_price'),D('.25'))
        self.assertEqual(m.get('global.imp_global_oil_price_equilibrium'),D(75))
    def test_no_new_recurring_hooks_or_country_scans_and_correct_encoding(self):
        helper=EFFECTS['COLDWAR_oil_oversupply_shock']
        self.assertFalse(any(k in ('every_country','every_possible_country','for_each_scope_loop','while_loop_effect','for_loop_effect') for k,o,v in V.walk(helper)))
        self.assertFalse((ROOT/FX).read_bytes().startswith(b'\xef\xbb\xbf'))
        self.assertTrue((ROOT/LOC).read_bytes().startswith(b'\xef\xbb\xbf'))
        self.assertTrue((ROOT/FX).read_text(encoding='utf8').startswith('# IMPERIA COLD WAR — '))
        self.assertTrue((ROOT/LOC).read_text(encoding='utf-8-sig').splitlines()[1].startswith('# IMPERIA COLD WAR — '))

def main():
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(OversupplyChecks)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():raise SystemExit(1)
    regression=[sys.executable,'-X','utf8',str(ROOT/'tools/cold_war_gc/test_controls.py'),'GCEquilibriumTests.test_oil_buttons_apply_real_prices_and_reset_crisis_burdens','GCEquilibriumTests.test_manual_refresh_does_not_advance_monthly_or_weekly_simulation']
    run=subprocess.run(regression,cwd=ROOT,capture_output=True,text=True,encoding='utf8');print(run.stdout+run.stderr)
    if run.returncode:raise SystemExit(run.returncode)
    report=dict(project='IMPERIA COLD WAR',result='PASS',focused_tests=result.testsRun,shared_oil_gc_tests=2,old_draw_probability='0.15',new_unlocked_draw_probability=str(D(15)/D(185)),new_price_multiplier='.99',own_cooldown_days=730,general_draw_cooldown_days=232,native_engine_tested=False,live_multiplayer_tested=False,boundary='Executed real script ASTs; simulated expiring global flags and forced branch selection. No engine RNG or live save/rehost claim.',regression_command=regression,regression_exit_code=run.returncode,source_hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in (FX,HOOK,EVENTS,LOC)})
    (HERE/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k!='source_hashes'},indent=2))

if __name__=='__main__':main()
