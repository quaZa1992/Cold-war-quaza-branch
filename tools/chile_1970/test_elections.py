# IMPERIA COLD WAR — Independent emitted presidential ballot arithmetic checks.
"""Execute the small native arithmetic subset used by the emitted 1970 count.

This is a source-model check, not an HOI4 interpreter or engine test.
"""
import itertools
import random
import sys
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import first, parse
P='COLDWAR_CHL_'

class Ballot:
    def __init__(self,array):self.vars={f'party_pop_array^{i}':v for i,v in enumerate(array)};self.flags=set()
    def value(self,key):
        try:return float(key)
        except ValueError:return self.vars.get(key,0)
    def condition(self,rows):
        for k,op,v in rows:
            if k=='check_variable':
                for a,comparison,b in v:
                    left,right=self.value(a),self.value(b)
                    if not {'=':left==right,'>':left>right,'<':left<right,'>=':left>=right,'<=':left<=right}[comparison]:return False
            elif k=='NOT':
                if self.condition(v):return False
            elif k=='has_country_flag':
                if v not in self.flags:return False
            else:raise AssertionError('Unsupported test predicate '+k)
        return True
    def run(self,rows):
        taken=False
        for k,op,v in rows:
            if k in ('if','else_if'):
                eligible=(k=='if' or not taken) and self.condition(first(v,'limit',[]))
                if k=='if':taken=False
                if eligible:self.run([r for r in v if r[0]!='limit']);taken=True
            elif k=='else':
                if not taken:self.run(v)
                taken=True
            elif k in ('set_variable','set_temp_variable','add_to_temp_variable','divide_temp_variable'):
                self.assert_pair(v)
                name,_,amount=v[0];amount=self.value(amount)
                if k.startswith('set_'):self.vars[name]=amount
                elif k=='add_to_temp_variable':self.vars[name]=self.vars.get(name,0)+amount
                else:self.vars[name]/=amount
            elif k=='set_country_flag':self.flags.add(v)
            elif k=='hold_elections':pass  # External MD array refresh. This model tests the following raw-support tally only.
            else:raise AssertionError('Unsupported test effect '+k)
    @staticmethod
    def assert_pair(rows):assert len(rows)==1,rows

class EmittedElectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source=(ROOT/'common/scripted_effects/COLDWAR_CHL_1970_politics.txt').read_text(encoding='utf-8')
        # Test the arithmetic inside the guarded transaction. Political eligibility
        # and replay protection are exercised independently in test_transition.py.
        transaction=first(first(parse(source),P+'election_count'),'if')
        cls.ballot=[row for row in transaction if row[0]!='limit']
    def assert_result(self,array):
        sums={1:array[1]+array[20],2:array[2]+array[14],18:sum(array[i] for i in (18,4,3,19))}
        ordered=sorted(sums,key=lambda k:(-sums[k],(1,2,18).index(k)))
        model=Ballot(array);model.run(self.ballot)
        if sum(sums.values())==0:
            self.assertNotIn(P+'election_ballot_counted',model.flags);return
        self.assertEqual(model.vars[P+'election_winner_slot'],ordered[0])
        self.assertEqual(model.vars[P+'election_runner_up_slot'],ordered[1])
        share=sums[ordered[0]]/sum(sums.values())
        self.assertAlmostEqual(model.vars[P+'election_winner_share'],share)
        self.assertEqual(P+'election_ratified' in model.flags,share>0.5)
        self.assertEqual(model.vars[P+'election_confirmed_slot'],ordered[0] if share>0.5 else -1)
    def test_all_candidate_rankings_majorities_and_ties(self):
        for weights in itertools.permutations((.4,.35,.25)):
            array=[0.0]*24
            for slot,value in zip((1,2,18),weights):array[slot]=value
            self.assert_result(array)
        for weights in ((.5,.25,.25),(.51,.3,.19),(.1,.2,.7),(0,0,0),(.3,.3,.3)):
            array=[0.0]*24
            for slot,value in zip((1,2,18),weights):array[slot]=value
            self.assert_result(array)
    def test_coalition_shares_are_counted_once_and_unregistered_tickets_are_excluded(self):
        generator=random.Random(1970)
        for _ in range(100):self.assert_result([generator.random() for _ in range(24)])

if __name__=='__main__':unittest.main()
