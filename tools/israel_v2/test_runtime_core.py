# IMPERIA COLD WAR — Independent emitted-core transaction and preview checks.
"""Inspect the actual pure compiler payload and execute its core effect AST.

This is a bounded source interpreter, not an engine/MP test. Native technology,
doctrine, faction and corruption commands are recorded as calls. Native state
selection uses a deterministic fixture instead of the engine RNG. Shared-slot
unlock rules and native queues are approximated by explicit built/queued caps.
"""
from copy import deepcopy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import unittest
import sys

import compile as native_compile
from runtime_titles import apply as concise_titles
from runtime_territories import build as territory_build
from test_runtime_domestic import Runtime, parse, one, DOMESTIC, BILATERAL


PAYLOAD = native_compile.build()
DATA = PAYLOAD['data']
CORE = {key: value for key, value in PAYLOAD['actions'].items()
        if value['reward'].startswith('ISR2_core_commit_')}
NODES = {n['id']: n for n in DATA['nodes']}
GROUPS = {g['id']: g for g in DATA['groups']}
TERRITORIAL = territory_build(DATA)
ASSET_LABELS = {'Civilian Factory', 'Military Factory', 'Office District',
                'Agricultural District', 'Infrastructure', 'Land Fort', 'Land Forts'}


class CoreRuntime(Runtime):
    def __init__(self):
        self.native_calls, self.ideas = [], set()
        self.callbacks = {}
        super().__init__(DOMESTIC, BILATERAL)
        for path, source in PAYLOAD['files'].items():
            if not (path.startswith('common/scripted_effects/ISR2_core_') or path.startswith('common/scripted_triggers/ISR2_core_')):
                continue
            if isinstance(source, bytes): source = source.decode('utf-8-sig')
            if path.startswith('common/scripted_effects/ISR2_core_'):
                self.effects.update({k:v for k,o,v in parse(source)})
            if path.startswith('common/scripted_triggers/ISR2_core_'):
                self.triggers.update({k:v for k,o,v in parse(source)})
        for state in ('1253','213'):
            self.states[state] = dict(owner='ISR' if state=='1253' else 'EGY', controller='ISR', slots=5, factories=0)
        for state, record in self.states.items():
            record.update(levels={}, queued={}, core=state!='213')
        self.vars['ISR']['ruling_party'] = Decimal(15)
        self.run('ISR2_core_init')

    def value(self, raw, ctx='ISR'):
        if isinstance(raw,str) and raw.startswith('building_level@') and ctx in self.states:
            return Decimal(self.states[ctx]['levels'].get(raw.split('@',1)[1],0))
        return super().value(raw,ctx)

    def test(self, rows, ctx='ISR', mode='AND'):
        transformed=[]
        for key,op,val in rows:
            result=None
            if key in {g['runtime_party_trigger'] for g in GROUPS.values() if g.get('runtime_party_trigger')}:
                result=key in self.party
            elif key in self.states and isinstance(val,list):result=self.test(val,key)
            elif key=='owner' and ctx in self.states:result=self.test(val,self.states[ctx]['owner'])
            elif key=='exists':result=ctx in ('ISR','EGY','SOV','USA','GER','ROM') and val=='yes'
            elif key=='is_core_of': result=self.states[ctx]['core'] and val=='ISR'
            elif key=='any_owned_state': result=any(s['owner']=='ISR' and self.test(val,state) for state,s in self.states.items())
            elif key=='any_controlled_state': result=any(s['controller']=='ISR' and self.test(val,state) for state,s in self.states.items())
            elif key=='any_state': result=any(self.test(val,state) for state in self.states)
            elif key=='controls_province': result=val=='1155' and self.states['213']['controller']=='ISR'
            elif key=='free_building_slots':
                kind=one(val,'building');cap={'infrastructure':6,'agriculture_district':10,'bunker':7}.get(kind,50)
                available=cap-self.states[ctx]['levels'].get(kind,0)-self.states[ctx]['queued'].get(kind,0)
                threshold=int(next(v for k,o,v in val if k=='size'))
                result=available>threshold
            elif key=='is_in_array': result=one(val,'array')=='gov_coalition_array' and one(val,'value')=='15'
            elif key=='has_idea': result=val in self.ideas
            if result is not None:
                alias='TEST_NATIVE_TRIGGER_'+str(len(self.overrides));self.overrides[alias]=result
                transformed.append((alias,'=','yes'))
            else:transformed.append((key,op,val))
        return super().test(transformed,ctx,mode)

    def _native(self, key, val, ctx):
        if key in self.states and isinstance(val,list):self.execute(val,key)
        elif key=='multiply_temp_variable':
            name,op,raw=val[0];self.temp[ctx][name]=self.value(name,ctx)*self.value(raw,ctx)
        elif key=='add_ideas':self.ideas.add(val)
        elif key=='remove_ideas':self.ideas.discard(val)
        elif key=='add_building_construction':
            kind=one(val,'type');levels=int(one(val,'level'))
            self.states[ctx]['levels'][kind]=self.states[ctx]['levels'].get(kind,0)+levels
            self.native_calls.append((key,ctx,kind,levels))
        elif key=='random_owned_state':
            conditions=one(val,'limit',[])
            choices=[state for state,s in sorted(self.states.items()) if s['owner']=='ISR' and self.test(conditions,state)]
            if choices:self.execute([row for row in val if row[0]!='limit'],choices[0])
        else:self.native_calls.append((key,ctx,deepcopy(val)))

    def execute(self, rows, ctx='ISR'):
        transformed=[]
        stubs={'add_ideas','remove_ideas','add_building_construction','random_owned_state',
               'add_tech_bonus','add_doctrine_cost_reduction','decrease_corruption','multiply_temp_variable'}
        for key,op,val in rows:
            if key in stubs or (key.startswith('change_') and key.endswith('_opinion')) or (key in self.states and isinstance(val,list)):
                alias='TEST_NATIVE_EFFECT_'+str(len(self.callbacks))
                self.callbacks[alias]=(key,deepcopy(val),ctx)
                self.effects[alias]=None
                transformed.append((alias,'=','yes'))
            else:transformed.append((key,op,val))
        return super().execute(transformed,ctx)

    def run(self,name,ctx='ISR'):
        if name in self.callbacks:
            return self._native(*self.callbacks[name])
        return super().run(name,ctx)

    def complete(self,fid):
        self.completed.add(fid)
        self.run('ISR2_core_commit_'+fid[5:])

    def govern(self,fid):
        self.party.clear()
        trigger=GROUPS[NODES[fid]['group']].get('runtime_party_trigger')
        if trigger:self.party.add(trigger)

    def advance(self,days):
        # Native timed-country-flags expire in the engine, not in core refresh.
        for ctx in self.flags:
            for flag,remaining in list(self.flags[ctx].items()):
                if remaining is not None:
                    if remaining<=days:self.flags[ctx].pop(flag)
                    else:self.flags[ctx][flag]-=days
        self.run('ISR2_core_daily')


class CoreTransactions(unittest.TestCase):
    def setUp(self):self.r=CoreRuntime()
    def variables(self):return self.r.vars['ISR']

    def test_actual153_generic_owners_exclude_every_special_action(self):
        self.assertEqual(len(CORE),153)
        special=set(DOMESTIC['actions'])|set(BILATERAL['actions'])|set(TERRITORIAL['actions'])
        self.assertEqual(len(special),64)
        self.assertEqual(set(CORE) & special,set())
        self.assertEqual(set(CORE),{n['id'] for n in DATA['nodes'] if n['runtime_action']['reward'].startswith('ISR2_core_commit_')})

    def test_concise_native_titles_preserve_all_mechanics_and_original_names(self):
        shortened=concise_titles(DATA)
        for original,edited in zip(DATA['nodes'],shortened['nodes']):
            self.assertLessEqual(len(edited['label']),25)
            self.assertEqual(edited['full_label'],original.get('full_label',original['label']))
            self.assertEqual({k:v for k,v in original.items() if k not in ('label','full_label')},
                             {k:v for k,v in edited.items() if k not in ('label','full_label')})
        self.assertEqual(concise_titles(shortened),shortened)

    def test_all_generated_asset_transactions_are_once_only_with_matching_slots(self):
        checked=0
        for fid in CORE:
            n=NODES[fid]
            levels=sum(int(Decimal(e['value'].replace('+',''))) for e in n['effects']
                if ': ' in e['label'] and e['label'].rsplit(': ',1)[1] in ASSET_LABELS)
            if not levels:continue
            checked+=1;r=CoreRuntime();r.govern(fid)
            slots=sum(s['slots'] for s in r.states.values());r.complete(fid)
            self.assertIn('ISR2_core_done_'+fid[5:],r.flags['ISR'],fid)
            actual=sum(sum(s['levels'].values()) for s in r.states.values())
            self.assertEqual(actual,levels,fid)
            self.assertEqual(sum(s['slots'] for s in r.states.values())-slots,levels,fid)
            before=deepcopy(r.states);treasury=r.vars['ISR']['treasury'];calls=len(r.native_calls)
            r.complete(fid)
            self.assertEqual(before,r.states,fid);self.assertEqual(treasury,r.vars['ISR']['treasury'],fid)
            self.assertEqual(calls,len(r.native_calls),fid)
            self.assertIn(fid,r.completed,fid)
        self.assertGreater(checked,20)

    def test_slots_precede_construction_inside_each_actual_native_state_block(self):
        for fid in CORE:
            rows=self.r.effects['ISR2_core_commit_'+fid[5:]]
            def inspect(block):
                for key,op,val in block:
                    if isinstance(val,list):
                        builds=[int(one(v,'level')) for k,o,v in val if k=='add_building_construction']
                        if builds:
                            self.assertEqual(int(one(val,'add_extra_state_shared_building_slots')),sum(builds),fid)
                            keys=[k for k,o,v in val]
                            self.assertLess(keys.index('add_extra_state_shared_building_slots'),keys.index('add_building_construction'),fid)
                        inspect(val)
            inspect(rows)

    def test_late_control_loss_and_queued_capacity_reopen_without_assets_or_charge(self):
        fid='ISR2_bonds_plant'
        for failure in ('control','queued'):
            r=CoreRuntime();r.govern(fid)
            if failure=='control':r.states['205']['controller']='EGY'
            else:r.states['205']['levels']['industrial_complex']=49;r.states['205']['queued']['industrial_complex']=1
            before=deepcopy(r.states);treasury=r.vars['ISR']['treasury'];r.complete(fid)
            self.assertNotIn(fid,r.completed);self.assertNotIn('ISR2_core_done_bonds_plant',r.flags['ISR'])
            self.assertEqual(before,r.states);self.assertEqual(treasury,r.vars['ISR']['treasury'])

    def test_workforce_route_is_exactly_fifteen_percent_and_never_replays(self):
        for fid in ('ISR2_ulpan_jobs','ISR2_ort_workshops','ISR2_daycare_shifts'):self.r.complete(fid)
        self.assertEqual(self.variables()['ISR2_absorption_total_workforce_modifier'],Decimal('.15'))
        cash=self.variables()['treasury']
        for fid in ('ISR2_ulpan_jobs','ISR2_ort_workshops','ISR2_daycare_shifts'):self.r.complete(fid)
        self.assertEqual(self.variables()['ISR2_absorption_total_workforce_modifier'],Decimal('.15'));self.assertEqual(cash,self.variables()['treasury'])

    def test_detention_review_requires_actual_controlled_non_core_territory(self):
        fid='ISR2_haolam_detention_review';self.r.govern(fid)
        self.r.states['213']['controller']='EGY';cash=self.variables()['treasury'];self.r.complete(fid)
        self.assertNotIn(fid,self.r.completed);self.assertNotIn('ISR2_core_done_haolam_detention_review',self.r.flags['ISR'])
        self.assertEqual(cash,self.variables()['treasury'])
        self.r.states['213']['controller']='ISR';self.r.complete(fid)
        self.assertIn('ISR2_core_done_haolam_detention_review',self.r.flags['ISR'])

    def test_absorption_start_penalties_are_removed_without_second_positive_relief(self):
        self.assertIn('ISR2_start_absorption',self.r.ideas);self.r.complete('ISR2_settled_skills')
        self.assertNotIn('ISR2_start_absorption',self.r.ideas)
        self.assertEqual(self.variables()['ISR2_absorption_research_speed_factor'],0)
        self.assertEqual(self.variables()['ISR2_absorption_social_cost_multiplier_modifier'],0)

    def test_party_departure_return_and_term_expiry_preserve_receipts(self):
        fid='ISR2_wage_bonds';self.r.govern(fid);self.r.complete(fid)
        value='ISR2_alignment_industrial_capacity_factory';cash=self.variables()['treasury']
        self.assertEqual(self.variables()[value],Decimal('.08'))
        self.r.party.clear();self.r.run('ISR2_core_refresh');self.assertEqual(self.variables()[value],0)
        self.r.govern(fid);self.r.run('ISR2_core_refresh');self.assertEqual(self.variables()[value],Decimal('.08'))
        self.assertEqual(cash,self.variables()['treasury']);debt=self.variables()['debt']
        self.r.advance(365);self.assertEqual(self.variables()[value],0)
        self.assertIn('ISR2_core_done_wage_bonds',self.r.flags['ISR'])
        self.r.advance(6);self.assertNotIn(fid,self.r.completed)
        self.r.complete(fid);self.assertEqual(self.variables()[value],Decimal('.08'));self.assertGreater(self.variables()['debt'],debt)

    def test_focus_specific_pure_quotes_cannot_consume_envelopes_or_coupons(self):
        self.variables()['ISR2_domestic_absorption_balance']=Decimal('.4')
        self.r.flags['ISR']['ISR2_domestic_tank_coupon']=None
        balances={k:v for k,v in self.variables().items() if 'balance' in k};cash=self.variables()['treasury']
        self.r.run('ISR2_refresh_core_quotes');self.r.run('ISR2_refresh_core_quotes')
        self.assertEqual(self.variables()['ISR2_preview_net_tal_tank'],Decimal('.11'))
        self.assertEqual(self.variables()['ISR2_preview_net_nesher'],Decimal('.18'))
        self.assertEqual(self.variables()['ISR2_preview_net_ulpan_jobs'],0)
        self.assertEqual(balances,{k:v for k,v in self.variables().items() if 'balance' in k});self.assertEqual(cash,self.variables()['treasury'])
        self.assertIn('ISR2_domestic_tank_coupon',self.r.flags['ISR'])

    def test_every_preview_is_nonexecuting_and_each_modifier_has_a_native_formatter(self):
        native=PAYLOAD['files']['common/national_focus/ISR70_focus.txt'].decode('utf-8')
        tree=one(parse(native),'focus_tree')
        focuses={one(row,'id'):row for key,op,row in tree if key=='focus'}
        count=0
        for fid,action in CORE.items():
            completion=one(focuses[fid],'completion_reward');self.assertIsNotNone(one(completion,'effect_tooltip'),fid)
            def check(rows):
                nonlocal count
                for key,op,value in rows:
                    if key=='add_to_variable':
                        self.assertIsNotNone(one(value,'tooltip'),fid);count+=1
                    if isinstance(value,list) and key!='add_to_variable':check(value)
            check(parse(action['preview']))
        self.assertGreater(count,100)


if __name__=='__main__':
    program=unittest.main(verbosity=2,exit=False)
    result=program.result
    source_files=('runtime_core.py','compile.py','runtime_domestic.py','runtime_titles.py','test_runtime_core.py')
    report=dict(project='IMPERIA COLD WAR',status='PASS' if result.wasSuccessful() else 'FAIL',
        test_count=result.testsRun,complete_suite=result.testsRun==11,
        generic_actions=len(CORE),special_actions_excluded=64,
        building_focuses=sum(any(': ' in e['label'] and e['label'].rsplit(': ',1)[1] in ASSET_LABELS for e in NODES[fid]['effects']) for fid in CORE),
        source_sha256={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest() for name in source_files},
        emitted_core_sha256=hashlib.sha256(PAYLOAD['files']['common/scripted_effects/ISR2_core_effects.txt']).hexdigest(),
        failures=[(str(test),detail) for test,detail in result.failures],
        errors=[(str(test),detail) for test,detail in result.errors],
        engine_test=False,
        limits=['Bounded source interpreter; no native engine, MP, save/reload or rehost evidence.',
                'Native research/doctrine/faction/corruption effects are recorded calls.',
                'State selection is deterministic; capacity and native queues use explicit fixture approximations.'])
    output=Path(__file__).resolve().parents[2]/'docs/israel_1970_v2/core_ast_validation.json'
    output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    sys.exit(0 if result.wasSuccessful() else 1)
