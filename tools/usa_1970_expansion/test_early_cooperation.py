# IMPERIA COLD WAR — Early cooperation generated-AST regression model.
"""Test emitted source transactions, not native UI, scope delivery or network play."""
from __future__ import annotations

import ast
import copy
from decimal import Decimal
import importlib.util
import inspect
import json
from pathlib import Path
import re
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('early_cooperation_module',HERE/'early_cooperation.py')
early=importlib.util.module_from_spec(spec);spec.loader.exec_module(early)
api=early.load_api();P=early.P;ROOT=early.ROOT
ns=early.parser();parse,first,walk=ns['parse'],ns['first'],ns['walk']


def model_class():
 functions=dict((k,v) for k,_,v in parse((ROOT/f'common/scripted_effects/{early.STEM}.txt').read_text()))
 triggers=dict((k,v) for k,_,v in parse((ROOT/f'common/scripted_triggers/{early.STEM}.txt').read_text()))
 nested=ast.parse(inspect.getsource(api.exercise_model)).body[0]
 klass=next(n for n in nested.body if isinstance(n,ast.ClassDef) and n.name=='Model')
 nodes=early.base_nodes(api)
 scope=dict(Decimal=Decimal,copy=copy,re=re,first=first,walk=walk,functions=functions,triggers=triggers,nodes=nodes,
  P=P,BUILDINGS={},PARENTS={},catalogue={n['suffix']:n for n in nodes},building_definitions=api.building_definitions,ROOT=ROOT)
 exec(compile(ast.Module(body=[klass],type_ignores=[]),str(HERE/'agreements.py'),'exec'),scope)
 Base=scope['Model']

 class Model(Base):
  def __init__(self):
   super().__init__();self.stack=[];self.root=None;self.triggers=triggers
   for tag in ('ENG','GER','SPA','SOV'):
    self.countries[tag]=dict(tag=tag,vars={'treasury':Decimal(1000)},flags={},ideas=set(),wars=set(),embargo=set(),arrays={},grants=[])
   for tag,c in self.countries.items():
    c['focuses']=set()
    c['ideas']={'NATO_member'} if tag in ('USA','CAN','ENG','GER') else set()

  def target(self,name):
   if name=='ROOT':return self.root
   if name=='PREV':return self.stack[-2] if len(self.stack)>1 else None
   if name=='THIS':return self.stack[-1] if self.stack else None
   return super().target(name)

  def country_value(self,value):
   target=self.target(value)
   return target['tag'] if target and 'tag' in target else value

  def condition(self,conditions,scope):
   push=not self.stack or self.stack[-1] is not scope
   if push:self.stack.append(scope)
   try:
    for key,op,value in conditions:
     if key=='exists':ok=(scope.get('tag') in self.countries)==(value=='yes')
     elif key=='is_in_array':ok=self.country_value(first(value,'value')) in scope['arrays'].get(first(value,'array'),set())
     elif key=='has_war_with':ok=self.country_value(value) in scope['wars']
     elif key=='is_embargoing':ok=self.country_value(value) in scope['embargo']
     elif key=='has_completed_focus':ok=value in scope['focuses']
     elif key=='check_variable' and not first(value,'var'):
      ident,sign,right=value[0];left=scope['vars'].get(ident,Decimal(0));right=Decimal(right)
      assert sign in ('>','<','=');ok=left>right if sign=='>' else left<right if sign=='<' else left==right
     else:ok=super().condition([(key,op,value)],scope)
     if not ok:return False
    return True
   finally:
    if push:self.stack.pop()

  def execute(self,statements,scope):
   push=not self.stack or self.stack[-1] is not scope
   if push:self.stack.append(scope)
   try:
    branch=False
    for key,op,value in statements:
     if key=='if':
      branch=self.condition(first(value,'limit',[]),scope)
      if branch:self.execute([x for x in value if x[0]!='limit'],scope)
     elif key=='else_if':
      if not branch and self.condition(first(value,'limit',[]),scope):self.execute([x for x in value if x[0]!='limit'],scope);branch=True
     elif key=='else':
      if not branch:self.execute(value,scope)
      branch=True
     elif key in ('every_country','for_each_scope_loop'):
      targets=list(self.countries) if key=='every_country' else sorted(scope['arrays'].get(first(value,'array'),set()))
      for tag in targets:
       if tag not in self.countries:continue
       target=self.countries[tag]
       if self.condition(first(value,'limit',[]),target):self.execute([x for x in value if x[0] not in ('limit','array')],target)
     elif key in ('add_to_array','remove_from_array'):
      array=scope['arrays'].setdefault(first(value,'array'),set());tag=self.country_value(first(value,'value'))
      array.add(tag) if key=='add_to_array' else array.discard(tag)
     else:super().execute([(key,op,value)],scope)
   finally:
    if push:self.stack.pop()

  def call(self,name,tag='USA'):
   self.root=self.countries[tag];assert not self.stack
   self.execute(functions[name],self.root)

  def early_accept(self,s,tag):self.call(f'{P}_accept_{s}_{tag.lower()}',tag)
  def root_focus(self,name):self.call(f'{P}_complete_root_{name}')
  def ally_accept(self,tag):self.call(P+'_alliance_accept',tag)
  def streams(self):
   for tag in self.countries:self.call(P+'_calculate_weekly_streams',tag)
  def reconcile(self):self.call(P+'_reconcile_all')

 return Model


class EarlyCooperationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  early.build();cls.Model=model_class()

 def m(self):return self.Model()

 def alliance(self):
  m=self.m();m.countries['USA']['flags']['USA_1970_nixon_presidency']=None;m.root_focus('alliances');return m

 def test_roots_offer_without_spirits_or_setup_fees(self):
  m=self.m();cash={t:c['vars']['treasury'] for t,c in m.countries.items()}
  m.root_focus('israel');m.root_focus('trade')
  self.assertIn(P+'_israel_offer_pending',m.countries['ISR']['flags'])
  self.assertIn(P+'_canada_offer_pending',m.countries['CAN']['flags'])
  self.assertIn(P+'_mexico_offer_pending',m.countries['MEX']['flags'])
  self.assertFalse(any(i.startswith(P+'_') for c in m.countries.values() for i in c['ideas']))
  self.assertEqual(cash,{t:c['vars']['treasury'] for t,c in m.countries.items()})

 def test_israeli_consent_pair_and_distinct_weekly_cost(self):
  m=self.m();m.root_focus('israel');m.early_accept('israel','ISR');m.streams()
  self.assertIn(P+'_israel_usa',m.countries['USA']['ideas']);self.assertIn(P+'_israel_isr',m.countries['ISR']['ideas'])
  self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],Decimal('.01'))
  self.assertEqual(m.countries['USA']['vars']['treasury'],1000)

 def test_canada_and_mexico_approve_independently(self):
  m=self.m();m.root_focus('trade');m.early_accept('canada','CAN');m.streams()
  self.assertNotIn(P+'_mexico_mex',m.countries['MEX']['ideas']);self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],Decimal('.005'))
  m.early_accept('mexico','MEX');m.streams();self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],Decimal('.01'))

 def test_genuine_nixon_guard_and_any_later_native_member(self):
  m=self.m();m.call(P+'_initialize');m.root_focus('alliances');self.assertFalse(m.events)
  m.countries['USA']['focuses'].add('USA_1970_NIX_F3');m.call(P+'_initialize')
  self.assertNotIn(P+'_alliances_authorised',m.countries['USA']['flags']);self.assertFalse(m.events)
  m.countries['USA']['flags']['USA_1970_nixon_presidency']=None;m.countries['USA']['ideas'].discard('NATO_member');m.root_focus('alliances');m.call(P+'_initialize')
  self.assertNotIn(P+'_alliances_authorised',m.countries['USA']['flags']);self.assertFalse(m.events)
  m.countries['USA']['ideas'].add('NATO_member')
  m.countries['USA']['flags']['USA_1970_nixon_presidency']=None;m.root_focus('alliances')
  self.assertIn(P+'_alliance_pending',m.countries['ENG']['flags']);self.assertNotIn(P+'_alliance_pending',m.countries['SPA']['flags'])
  m.countries['SPA']['ideas'].add('NATO_member');m.call(P+'_membership_changed','SPA');self.assertIn(P+'_alliance_pending',m.countries['SPA']['flags'])
  m.countries['SOV']['ideas'].add('Major_Non_NATO_Ally');m.call(P+'_membership_changed','SOV');self.assertIn(P+'_alliance_pending',m.countries['SOV']['flags'])
  self.assertEqual(m.countries['SOV']['ideas'],{'Major_Non_NATO_Ally'})

 def test_single_capped_usa_spirit_and_coupon(self):
  m=self.alliance();m.ally_accept('ENG');m.ally_accept('GER');m.streams()
  self.assertEqual(sum(i==early.ALLY_USA_ID for i in m.countries['USA']['ideas']),1)
  self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],Decimal('.01'))
  self.assertEqual(m.countries['USA']['vars'][P+'_alliance_weekly_expense'],Decimal('.01'))
  self.assertEqual(len(m.countries['USA']['grants']),1)
  before=copy.deepcopy((m.countries,m.events));m.ally_accept('ENG');self.assertEqual(before,(m.countries,m.events))

 def test_membership_suspension_and_restoration_do_not_replay(self):
  m=self.alliance();m.ally_accept('ENG');grants=copy.deepcopy(m.countries['ENG']['grants'])
  m.countries['ENG']['ideas'].discard('NATO_member');m.reconcile();m.streams()
  self.assertNotIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas']);self.assertNotIn(early.ALLY_USA_ID,m.countries['USA']['ideas']);self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],0)
  m.countries['ENG']['ideas'].add('Major_Non_NATO_Ally');m.reconcile();m.streams()
  self.assertIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas']);self.assertEqual(grants,m.countries['ENG']['grants']);self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],Decimal('.005'))
  # A real member blocked at first dispatch remains in the bounded candidate
  # list and receives its first proposal when restrictions clear.
  queued=self.m();queued.countries['USA']['flags']['USA_1970_nixon_presidency']=None;queued.countries['ENG']['embargo'].add('USA');queued.root_focus('alliances')
  self.assertNotIn(P+'_alliance_pending',queued.countries['ENG']['flags']);self.assertIn('ENG',queued.countries['USA']['arrays'][P+'_alliance_offered'])
  queued.countries['ENG']['embargo'].clear();queued.reconcile();self.assertIn(P+'_alliance_pending',queued.countries['ENG']['flags'])

 def test_every_mirrored_sanction_class_suspends_both_sides(self):
  m=self.alliance();m.ally_accept('ENG')
  for holder,other in [('USA','ENG'),('ENG','USA')]:
   for kind in ('dip','fin','eco','mil'):
    for direction in ('on','by'):
     key=f'imp_{kind}_sanc_{direction}_us';m.countries[holder]['arrays'][key]={other};m.reconcile();m.streams()
     self.assertNotIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas']);self.assertNotIn(early.ALLY_USA_ID,m.countries['USA']['ideas']);self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],0)
     m.countries[holder]['arrays'][key]=set();m.reconcile();self.assertIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas'])

 def test_bilateral_war_and_embargo_guard_acceptance_and_standing(self):
  for holder,other in [('USA','ENG'),('ENG','USA')]:
   for relation in ('wars','embargo'):
    with self.subTest(holder=holder,relation=relation):
     m=self.alliance();m.countries[holder][relation].add(other)
     m.ally_accept('ENG');m.streams()
     self.assertNotIn(P+'_alliance_signed',m.countries['ENG']['flags'])
     self.assertNotIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas'])
     self.assertNotIn(early.ALLY_USA_ID,m.countries['USA']['ideas'])
     self.assertFalse(m.countries['ENG']['grants']);self.assertFalse(m.countries['USA']['grants'])
     self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],0)
     m.countries[holder][relation].clear();m.ally_accept('ENG');m.streams()
     self.assertIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas'])
     grants={t:copy.deepcopy(m.countries[t]['grants']) for t in ('USA','ENG')}
     m.countries[holder][relation].add(other);m.reconcile();m.streams()
     self.assertNotIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas'])
     self.assertNotIn(early.ALLY_USA_ID,m.countries['USA']['ideas'])
     self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],0)
     m.countries[holder][relation].clear();m.reconcile();m.streams()
     self.assertIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas'])
     self.assertIn(early.ALLY_USA_ID,m.countries['USA']['ideas'])
     self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],Decimal('.005'))
     self.assertEqual(grants,{t:m.countries[t]['grants'] for t in ('USA','ENG')})

 def test_refusal_cooldown_and_pending_expiry(self):
  m=self.alliance();m.call(P+'_alliance_decline','ENG');self.assertFalse(m.condition(m.triggers[P+'_alliance_can_offer'],m.countries['ENG']))
  m.tick(90);m.call(P+'_alliance_send_to_recipient','ENG');self.assertIn(P+'_alliance_pending',m.countries['ENG']['flags'])
  m.tick(90);m.ally_accept('ENG');self.assertNotIn(P+'_alliance_signed',m.countries['ENG']['flags']);self.assertFalse(m.countries['ENG']['grants'])

 def test_sender_can_end_one_partner_while_other_continues(self):
  m=self.alliance();m.ally_accept('ENG');m.ally_accept('GER')
  m.root=m.countries['USA'];m.execute(parse('ENG = { '+P+'_alliance_end = yes }'),m.countries['USA']);m.streams()
  self.assertNotIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas']);self.assertIn(early.ALLY_PARTNER_ID,m.countries['GER']['ideas']);self.assertIn(early.ALLY_USA_ID,m.countries['USA']['ideas'])
  self.assertIn(P+'_alliance_sender_blocked',m.countries['ENG']['flags']);self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],Decimal('.005'))

 def test_recipient_can_terminate_after_sponsor_disappears(self):
  m=self.alliance();m.ally_accept('ENG');del m.countries['USA'];m.call(P+'_alliance_end','ENG')
  self.assertNotIn(early.ALLY_PARTNER_ID,m.countries['ENG']['ideas']);self.assertNotIn(P+'_alliance_signed',m.countries['ENG']['flags'])

 def test_old_save_authorises_offers_without_material_grants(self):
  m=self.m();m.countries['USA']['focuses'].update(early.ROOTS);m.call(P+'_initialize')
  self.assertIn(P+'_alliance_pending',m.countries['ENG']['flags']);self.assertIn(P+'_canada_offer_pending',m.countries['CAN']['flags'])
  self.assertFalse(any(i.startswith(P+'_') for c in m.countries.values() for i in c['ideas']));self.assertTrue(all(not c['grants'] for c in m.countries.values()))
  before=copy.deepcopy((m.countries,m.events));m.call(P+'_initialize');self.assertEqual(before,(m.countries,m.events))

 def test_weekly_calculation_is_pure_repeatable_and_deficit_compatible(self):
  m=self.alliance();m.ally_accept('ENG');m.countries['USA']['vars']['treasury']=Decimal(0);m.streams()
  self.assertEqual(m.countries['USA']['vars']['treasury'],0);self.assertEqual(m.countries['USA']['vars'][P+'_weekly_expense'],Decimal('.005'))
  before=copy.deepcopy((m.countries,m.events));m.streams();self.assertEqual(before,(m.countries,m.events))

 def test_mis_scoped_roots_and_full_previews(self):
  m=self.m();before=copy.deepcopy(m.countries);m.call(P+'_complete_root_trade','CAN');self.assertEqual(before,m.countries)
  m.call(P+'_preview_root_trade');m.call(P+'_preview_root_israel');m.call(P+'_preview_root_alliances');self.assertEqual(before,m.countries)
  specs=json.loads((early.OUT/'focus_specs.json').read_text())
  self.assertTrue(specs['focuses']['USA_1970_F7']['replace_legacy_available']);self.assertNotIn('enbo_',specs['focuses']['USA_1970_F7']['available'])
  self.assertEqual(specs['followups']['USA_X_israel']['runtime_guard'],P+'_active_israel = yes')
  source=(ROOT/f'common/scripted_effects/{early.STEM}.txt').read_text();effects=dict((k,v) for k,_,v in parse(source))
  template=effects[P+'_alliance_preview'];self.assertFalse(any(k in ('if','every_country') for k,_,v in walk(template)))
  self.assertTrue(any(k=='add_ideas' and v==early.ALLY_PARTNER_ID for k,_,v in walk(template)))
  self.assertTrue(any(k=='add_to_variable' and first(v,'tooltip')==P+'_weekly_expense_tt' for k,_,v in walk(template)))


if __name__=='__main__':
 unittest.main(verbosity=2)
