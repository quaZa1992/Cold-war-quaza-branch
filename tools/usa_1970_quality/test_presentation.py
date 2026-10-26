# IMPERIA CW — Cold War: usa 1970 quality — test presentation.
"""Check that presentation wrappers preserve actual prerequisite logic."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from focus_prerequisite_ui import nodes
from presentation import hide_routing,patch_usa

def canon(rows):
    result=[]
    for n in rows:
        if n.key in ('hidden_trigger','custom_trigger_tooltip'):
            result.extend(canon([c for c in n.children() if c.key!='tooltip']))
        else:result.append((n.key,n.op,canon(n.children()) if isinstance(n.value,list) else n.value))
    return tuple(result)

class PresentationTests(unittest.TestCase):
    def test_internal_and_meaningful_mixed_or_stay_equivalent(self):
        before='original_tag = GRE\nIMP_is_1970_scenario = yes\nOR = { check_variable = { ruling_party = 1 } AND = { is_ai = no has_idea = member } }'
        after=hide_routing(before)
        self.assertEqual(canon(nodes(before)),canon(nodes(after)))
        self.assertIn('has_idea = member',after)
        self.assertNotIn('hidden_trigger = { has_idea',after)

    def test_ai_reservation_is_hidden_as_one_equivalent_rule(self):
        before='OR = { is_ai = no AND = { has_country_flag = COLDWAR_CYP_1970_dedicated_historical_ai NOT = { has_country_flag = COLDWAR_CYP_1970_human_seat_reserved } } }'
        after=hide_routing(before)
        self.assertTrue(after.startswith('hidden_trigger = { OR'))
        self.assertEqual(canon(nodes(before)),canon(nodes(after)))

    def test_meaningful_historical_dates_are_not_globally_hidden(self):
        before='date > 1970.12.26\nhas_idea = idea_gcc_member_state\nowns_state = 145'
        self.assertEqual(before,hide_routing(before))

    def test_nixon_terms_named_without_changing_rewards_or_deadline(self):
        before='focus_tree = { focus = { id = USA_1970_NIX_A0 available = { has_country_flag = USA_1970_nixon_presidency date < 1973.1.20 } completion_reward = { add_political_power = 50 add_stability = -0.01 } } }'
        after=patch_usa(before)
        self.assertIn('USA_1970_nixon_first_term_tt',after)
        self.assertEqual(canon(nodes(before)),canon(nodes(after)))

    def test_live_overlay_is_idempotent(self):
        path=Path(__file__).resolve().parents[2]/'common/national_focus/USA_1970.txt'
        text=path.read_text(encoding='utf-8')
        self.assertEqual(text,patch_usa(text))

if __name__=='__main__':unittest.main(verbosity=2)
