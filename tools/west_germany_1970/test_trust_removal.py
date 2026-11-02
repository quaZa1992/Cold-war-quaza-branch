# IMPERIA COLD WAR — Retired German score and save-cleanup regression
"""Execute installed cleanup/formulas; native game save loading is not emulated."""
import copy
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/colonial_affairs'))
from test_runtime import Model,Scope,D,parse,first
from trust_cleanup import P

RETIRED=('cwger_westbindung','cwddr_moscow_backing','COLDWAR_DDR_moscow_trust',
         'COLDWAR_DDR_trust_delta','DDR_state_trust','DDR_moscow_trust')


def load(rel):return parse((ROOT/rel).read_text(encoding='utf-8-sig'))


class Retirement(unittest.TestCase):
    def setUp(self):
        self.m=Model()
        self.w=self.m.c['GER']=Scope('GER');self.d=self.m.c['DDR']=Scope('DDR')
        self.m.root=self.w
        providers=load(f'common/scripted_effects/{P}_effects.txt')
        self.m.effects[P+'_update_modifiers']=first(providers,P+'_update_modifiers')
        self.m.effects.update((k,v) for k,o,v in load(f'common/scripted_effects/{P}_trust_cleanup.txt'))
        self.m.effects.update((k,v) for k,o,v in load('common/scripted_effects/99_DDR_1985_state_crisis_effects.txt'))

    def test_existing_scores_removed_without_resetting_political_inputs(self):
        self.w.flags.add(P+'_initialized')
        self.w.vars.update(cwger_westbindung=D(88),cwger_dm_ideo=D('.076'),cwger_security=D(62),cwger_rechtsstaat=D(60))
        self.d.vars.update({key:D(77) for key in RETIRED[1:]})
        self.d.vars.update(COLDWAR_DDR_course=D('-.4'),cwddr_sed_control=D(70),cwddr_hard_currency=D(42))
        self.d.modifiers.add('COLDWAR_DDR_socialist_camp')
        for country in (self.w,self.d):self.m.run(P+'_retired_trust_cleanup',country)
        for country in (self.w,self.d):
            self.assertFalse(set(RETIRED)&country.vars.keys())
            self.assertIn(P+'_retired_trust_cleaned',country.flags)
        self.assertEqual(self.w.vars.get('cwger_dm_ideo',D(0)),0)
        self.assertEqual(self.w.vars['cwger_security'],62)
        self.assertEqual(self.d.vars['COLDWAR_DDR_course'],D('-.4'))
        self.assertEqual(self.d.vars['cwddr_hard_currency'],42)
        self.assertEqual(self.d.modifiers,{'COLDWAR_DDR_socialist_camp'})
        before=copy.deepcopy((self.w.vars,self.d.vars,self.w.flags,self.d.flags))
        for country in (self.w,self.d):self.m.run(P+'_retired_trust_cleanup',country)
        self.assertEqual(before,(self.w.vars,self.d.vars,self.w.flags,self.d.flags))

    def test_fresh_or_dormant_legacy_state_is_not_initialized(self):
        self.m.run(P+'_retired_trust_cleanup',self.d)
        self.assertNotIn('DDR_state_crisis_system_enabled',self.d.flags)
        self.assertNotIn('DDR_sed_control',self.d.vars)
        self.assertNotIn(P+'_ddr_initialized',self.d.flags)

    def test_active_legacy_formulas_drop_trust_and_keep_independent_terms(self):
        self.d.flags.add('DDR_state_crisis_system_enabled')
        self.d.vars.update(DDR_state_trust=D(44),DDR_moscow_trust=D(78),
                           DDR_sed_control=D(86),DDR_nva_loyalty=D(76),
                           DDR_reform_pressure=D(34),DDR_emigration_pressure=D(46),
                           DDR_mass_protest_pressure=D(10),DDR_supply_pressure=D(56))
        self.m.run(P+'_retired_trust_cleanup',self.d)
        self.assertEqual(self.d.vars['DDR_state_crisis_stability_factor'],D(16)/2600)
        self.assertEqual(self.d.vars['DDR_state_crisis_communism_drift'],D(52)/2600)

    def test_startup_hook_handles_missing_country_without_a_recurring_scan(self):
        rows=first(load(f'common/on_actions/{P}_trust_cleanup.txt'),'on_actions')
        self.assertEqual([k for k,o,v in rows],['on_startup'])
        body=first(first(rows,'on_startup'),'effect')
        del self.m.c['GER']
        self.m.execute(body,self.d,self.d,self.d)
        self.assertIn(P+'_retired_trust_cleaned',self.d.flags)
        text=(ROOT/f'common/on_actions/{P}_trust_cleanup.txt').read_text(encoding='utf-8')
        self.assertNotIn('every_country',text)

    def test_cleanup_does_not_remove_unregistered_dynamic_modifiers(self):
        text=(ROOT/f'common/scripted_effects/{P}_trust_cleanup.txt').read_text(encoding='utf-8')
        self.assertNotIn('remove_dynamic_modifier',text)
        self.assertIn('clear_variable = COLDWAR_DDR_moscow_trust',text)
        self.assertIn('clear_variable = COLDWAR_DDR_trust_delta',text)

    def test_retired_scores_have_no_loaded_readers_or_writers(self):
        tokens=re.compile(r'\b(?:'+'|'.join(map(re.escape,RETIRED))+r')\b')
        violations=[]
        for folder in ('common','events','localisation/english'):
            for path in (ROOT/folder).rglob('*'):
                if path.suffix not in ('.txt','.gui','.gfx','.yml'):continue
                for n,line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1):
                    if not tokens.search(line) or line.lstrip().startswith('#'):continue
                    if path.name==P+'_trust_cleanup.txt' and line.strip().startswith('clear_variable ='):continue
                    violations.append(str(path.relative_to(ROOT))+':'+str(n)+': '+line.strip())
        self.assertEqual(violations,[])


if __name__=='__main__':unittest.main(verbosity=2)
