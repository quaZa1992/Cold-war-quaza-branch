# IMPERIA COLD WAR — USA scripted grants versus technology construction limits.
"""Focused source regressions. Native execution is recorded separately on E:."""
from pathlib import Path
import re
import sys
import unittest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'tools'))
from usa_building_capacity import capacity_trigger,capacity_localisation,building_definitions
from focus_prerequisite_ui import nodes,field

FOCUS='USA_1970_1976_dem_2_a_national_energy_effort'

def walk(rows):
    for n in rows:
        yield n
        yield from walk(n.children())

class CapacityContext:
    def __init__(self):
        self.party=2
        self.states={str(s):dict(owner='USA',controller='USA',levels={'renewable_energy_infra':0,'infrastructure':3},slots=0,manual_max=0) for s in (800,804,811)}

    def check(self,rows,state=None):
        def one(n):
            if n.key in self.states:return self.check(n.children(),self.states[n.key])
            if n.key in ('AND','hidden_trigger'):return self.check(n.children(),state)
            if n.key=='OR':return any(self.check([c],state) for c in n.children())
            if n.key=='NOT':return not self.check(n.children(),state)
            if n.key=='custom_trigger_tooltip':return self.check([c for c in n.children() if c.key!='tooltip'],state)
            if n.key=='is_owned_and_controlled_by':return state['owner']==state['controller']==n.value
            if n.key=='western_liberals_are_in_power':return self.party==2
            if n.key=='check_variable':
                variable=field(n.children(),'var');assert variable.startswith('building_level@')
                assert field(n.children(),'compare')=='less_than_or_equals'
                return state['levels'].get(variable.split('@',1)[1],0)<=int(field(n.children(),'value'))
            if n.key=='free_building_slots':
                # Deliberately distinguish manual tech entitlement from the
                # building's physical cap. The previous model conflated them.
                b=field(n.children(),'building')
                return state['manual_max']-state['levels'].get(b,0)>int(field(n.children(),'size'))
            raise AssertionError(('Unmodelled condition',n.key,n.value))
        return all(one(n) for n in rows)

class BuildingCapacityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=ROOT/'common/scripted_triggers/COLDWAR_USA_1970_expansion.txt'
        cls.triggers={n.key:n for n in nodes(path.read_text(encoding='utf-8-sig'))}
        cls.energy=cls.triggers['COLDWAR_USA_legacy_capacity_'+FOCUS].children()

    def test_screenshot_three_states_allow_grant_without_manual_unlock_or_shared_slots(self):
        m=CapacityContext()
        self.assertTrue(m.check(self.energy))
        self.assertFalse(m.check(nodes('free_building_slots = { building = renewable_energy_infra size > 0 }'),m.states['800']))
        for state in m.states.values():
            state['levels']['renewable_energy_infra']=19
        self.assertTrue(m.check(self.energy))

    def test_any_one_full_state_blocks_complete_three_state_package(self):
        for sid in ('800','804','811'):
            with self.subTest(state=sid):
                m=CapacityContext();m.states[sid]['levels']['renewable_energy_infra']=20
                self.assertFalse(m.check(self.energy))

    def test_actual_ownership_and_control_still_required(self):
        for sid in ('800','804','811'):
            for key in ('owner','controller'):
                with self.subTest(state=sid,key=key):
                    m=CapacityContext();m.states[sid][key]='GER';self.assertFalse(m.check(self.energy))

    def test_party_and_one_time_receipt_remain_in_authoritative_ready(self):
        r=self.triggers['COLDWAR_USA_legacy_ready_'+FOCUS]
        self.assertIn('western_liberals_are_in_power',[n.key for n in r.children()])
        self.assertTrue(any(n.key=='has_country_flag' and n.value=='COLDWAR_USA_legacy_done_'+FOCUS.removeprefix('USA_1970_') for n in walk(r.children())))
        m=CapacityContext();party=next(n for n in r.children() if n.key=='western_liberals_are_in_power')
        self.assertTrue(m.check([party]));m.party=1;self.assertFalse(m.check([party]))

    def test_independent_caps_use_all_granted_levels(self):
        for b in ('renewable_energy_infra','fossil_powerplant','nuclear_reactor','infrastructure','fuel_silo'):
            for count in (1,2):
                with self.subTest(building=b,count=count):
                    limit=int(building_definitions()[b]['state_max'])
                    state=CapacityContext().states['800'];state['levels'][b]=limit-count
                    body=nodes(capacity_trigger(b,count));m=CapacityContext()
                    self.assertTrue(m.check(body,state));state['levels'][b]+=1;self.assertFalse(m.check(body,state))

    def test_shared_slots_and_exact_port_province_keep_native_queries(self):
        shared=nodes(capacity_trigger('dockyard',2))[0]
        self.assertEqual(shared.key,'free_building_slots');self.assertEqual(field(shared.children(),'include_locked'),'no')
        port=nodes(capacity_trigger('naval_base',1,10337))[0]
        self.assertEqual(port.key,'free_building_slots');self.assertEqual(field(port.children(),'province'),'10337')
        self.assertIsNone(field(port.children(),'include_locked'))
        with self.assertRaises(AssertionError):capacity_trigger('naval_base')

    def test_generated_usa_providers_never_query_manual_slots_for_independent_state_grants(self):
        paths=[ROOT/'common/scripted_triggers'/('COLDWAR_USA_1970_'+k+'.txt') for k in ('expansion','programmes','agreements')]
        for path in paths:
            for n in walk(nodes(path.read_text(encoding='utf-8-sig'))):
                if n.key=='free_building_slots':
                    b=field(n.children(),'building')
                    self.assertTrue(building_definitions()[b]['shares_slots'] or field(n.children(),'province'),(path,b))

    def test_all_visible_capacity_keys_have_one_canonical_english_provider(self):
        sources=[p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/scripted_triggers').glob('COLDWAR_USA_1970_*.txt')]
        path=ROOT/'localisation/english/COLDWAR_USA_1970_building_capacity_l_english.yml'
        self.assertTrue(path.read_bytes().startswith(b'\xef\xbb\xbf'))
        text=path.read_text(encoding='utf-8-sig');self.assertEqual(text,capacity_localisation(sources))
        keys=re.findall(r'^ (\w+):0 ',text,re.M);self.assertEqual(len(keys),len(set(keys)))
        self.assertIn('COLDWAR_USA_building_capacity_renewable_energy_infra_1_tt',keys)

if __name__=='__main__':unittest.main(verbosity=2)
