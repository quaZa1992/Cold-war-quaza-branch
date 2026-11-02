# IMPERIA COLD WAR — Regression checks for readable Chile requirements.
import itertools
from pathlib import Path
import sys
import unittest
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from chile_presentation import polish, polish_file
from script_ast import parse, first

def unwrap(rows):
    out=[]
    for k,o,v in rows:
        if k=='hidden_trigger':out.extend(unwrap(v))
        else:out.append((k,o,unwrap(v) if isinstance(v,list) else v))
    return out

def evaluate(rows,flags):
    for k,o,v in rows:
        if k in ('hidden_trigger','AND'):
            if not evaluate(v,flags):return False
        elif k=='OR':
            if not any(evaluate([r],flags) for r in v):return False
        elif k=='NOT':
            if evaluate(v,flags):return False
        elif k=='has_country_flag':
            if v not in flags:return False
        else:raise AssertionError(k)
    return True

def visible(rows):
    for k,o,v in rows:
        if k in ('hidden_trigger','custom_trigger_tooltip','custom_override_tooltip'):continue
        yield k,o,v
        if isinstance(v,list):yield from visible(v)

class PresentationTests(unittest.TestCase):
    def test_wrapping_keeps_predicates_and_boolean_results(self):
        rows=parse('NOT = { OR = { has_country_flag = COLDWAR_CHL_a has_country_flag = COLDWAR_CHL_b } } has_country_flag = COLDWAR_CHL_c')
        revised=polish(rows)
        self.assertEqual(unwrap(revised),rows)
        self.assertEqual(revised[0][0],'hidden_trigger')
        for bits in itertools.product((False,True),repeat=3):
            flags={f'COLDWAR_CHL_{k}' for k,b in zip('abc',bits) if b}
            self.assertEqual(evaluate(rows,flags),evaluate(revised,flags))
    def test_effects_and_complete_reward_bodies_are_unchanged(self):
        source=parse('focus = { available = { NOT = { has_country_flag = COLDWAR_CHL_paid } } completion_reward = { effect_tooltip = { set_temp_variable = { treasury_change = -0.05 } modify_treasury_effect = yes } hidden_effect = { if = { limit = { NOT = { has_country_flag = COLDWAR_CHL_paid } } add_building_construction = { type = industrial_complex level = 1 } } } } }')
        self.assertEqual(unwrap(polish_file(source)),unwrap(source))
        self.assertEqual(first(first(polish_file(source),'focus'),'completion_reward'),first(first(source,'focus'),'completion_reward'))
    def test_emitted_trigger_labels_do_not_expose_internal_receipts(self):
        for path in (HERE/'stage/common/scripted_triggers').glob('COLDWAR_CHL*.txt'):
            for name,o,rows in parse(path.read_text(encoding='utf-8')):
                for key,op,value in visible(rows):
                    if key in ('has_country_flag','has_global_flag'):
                        self.assertFalse(str(value).startswith('COLDWAR_CHL_'),(name,value))
        path=HERE/'stage/common/scripted_triggers/COLDWAR_CHL_1970_diplomacy.txt'
        cuba=first(parse(path.read_text(encoding='utf-8')),'COLDWAR_CHL_can_offer_cuba_clinics')
        self.assertTrue(any(k=='country_exists' and v=='CUB' for k,o,v in cuba))
        labels=[first(v,'tooltip') for k,o,v in cuba if k=='custom_trigger_tooltip']
        self.assertIn('COLDWAR_CHL_dip_cuba_clinics_relations_tt',labels)
        self.assertIn('COLDWAR_CHL_cuba_relations_tt',labels)

if __name__=='__main__':unittest.main()
