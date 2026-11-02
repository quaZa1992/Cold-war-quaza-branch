# IMPERIA COLD WAR — Chile 1970 diplomacy emitted-script tests.
"""Evaluate generated recipient and transaction guards using the project's Clausewitz AST."""
import sys
import json
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, values
sys.path.insert(0,str(HERE))
from diplomacy import build, SOURCE, varid, focus_key, participants, is_collective, idea_id, n
from current_design import load_design

class Scope:
    def __init__(self,tag, flags=None, ideas=None):
        self.tag=tag;self.flags=set(flags or ());self.ideas=set(ideas or ())

class World:
    def __init__(self):
        self.countries={};self.exists=set();self.relations={};self.arrays={};self.true_triggers=set();self.opinions={};self.defs={}
    def scope(self,tag):return self.countries.get(tag,Scope(tag))

def evaluate(rows,world,current):
    """Evaluate the emitted guard subset against explicit country and relation state."""
    if not isinstance(rows,list):return True
    for key,op,val in rows:
        if key=='_bare':continue
        if isinstance(val,list):
            if key=='NOT':
                if evaluate(val,world,current):return False
            elif key=='OR':
                if not any(evaluate([r],world,current) for r in val):return False
            elif key=='AND':
                if not evaluate(val,world,current):return False
            elif key in world.countries or key in ('CHL','USA','SOV','JAP','CUB','ARG','PRU','BOL','COL','ECU','FRA'):
                if not evaluate(val,world,key):return False
            elif key=='custom_trigger_tooltip':
                if not evaluate([r for r in val if r[0]!='tooltip'],world,current):return False
            elif key=='has_opinion':
                data={k:v for k,o,v in val if k!='_bare'}
                score=world.opinions.get((current,data.get('target')),0)
                if not compare(score,data.get('value'),data.get('>=' if '>=' in data else '>' )):return False
            elif key=='is_in_array':
                data={k:v for k,o,v in val if k!='_bare'}
                arr=data.get('array'); target=data.get('value')
                if target not in world.arrays.get((current,arr),set()):return False
            else:
                if not evaluate(val,world,current):return False
            continue
        if key=='tag' and current!=val:return False
        if key=='has_country_flag' and val not in world.scope(current).flags:return False
        if key=='has_idea' and val not in world.scope(current).ideas:return False
        if key=='country_exists' and val not in world.exists:return False
        if key=='has_war_with' and not world.relations.get(tuple(sorted((current,val))),{}).get('war',False):return False
        if key=='is_embargoing' and not world.relations.get((current,val),{}).get('embargo',False):return False
        if key=='COLDWAR_CHL_is_scenario' and val=='yes' and 'scenario' not in world.true_triggers:return False
        if key.startswith('COLDWAR_CHL_can_build_') and val=='yes' and key not in world.true_triggers:return False
        if key.startswith('COLDWAR_CHL_dip_') and key.endswith('_clear') and val=='yes':
            definition=world.defs.get(key)
            if definition is None or not evaluate(definition,world,current):return False
        if key in ('value',) and op in ('>','>=','<','<='):
            continue
        if key=='always' and val=='no':return False
    return True

def compare(left,right,op):
    if right is None:return False
    try:right=float(right);left=float(left)
    except (TypeError,ValueError):return False
    return {'>':left>right,'>=':left>=right,'<':left<right,'<=':left<=right,'=':left==right}.get(op,False)

def block(rows,name):
    if rows is None:return None
    for key,op,val in rows:
        if key==name and isinstance(val,list):return val
        if isinstance(val,list):
            found=block(val,name)
            if found is not None:return found
    return None

def all_block(rows,name):return [v for k,o,v in rows if k==name and isinstance(v,list)]

def walk(rows):
    for key,op,val in rows or []:
        yield key,op,val
        if isinstance(val,list):yield from walk(val)

def has(rows,key,value):
    return any(k==key and v==value for k,op,v in walk(rows))

def make_world(tags):
    w=World();w.exists=set(tags)
    for t in tags:w.countries[t]=Scope(t)
    for i,x in enumerate(tags):
        for y in tags[i+1:]:w.relations[tuple(sorted((x,y)))]= {'war':False}
    return w

def add_clear_definitions(w,trigger_text):
    ast=parse(trigger_text)
    for key,op,val in ast:
        if key.endswith('_clear') and isinstance(val,list):w.defs[key]=val

class DiplomacyEmittedGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=build()
        cls.effects=parse(cls.out['common/scripted_effects/COLDWAR_CHL_1970_diplomacy.txt'])
        cls.triggers=parse(cls.out['common/scripted_triggers/COLDWAR_CHL_1970_diplomacy.txt'])
        cls.decisions=parse(cls.out['common/decisions/COLDWAR_CHL_1970_diplomacy.txt'])
        cls.events=parse(cls.out['events/COLDWAR_CHL_1970_diplomacy.txt'])
        add_clear_definitions(cls.world,cls.out['common/scripted_triggers/COLDWAR_CHL_1970_diplomacy.txt']) if hasattr(cls,'world') else None

    def setUp(self):
        tags=['CHL','USA','SOV','JAP','CUB','ARG','PRU','BOL','COL','ECU','FRA']
        self.world=make_world(tags);add_clear_definitions(self.world,self.out['common/scripted_triggers/COLDWAR_CHL_1970_diplomacy.txt'])
        self.world.true_triggers.add('scenario')
        for tag in ('CHL','BOL','COL','ECU','PRU'):
            self.world.scope(tag).ideas.add('COLDWAR_CHL_cartagena_member')

    def test_frozen_agreement_and_api_coverage(self):
        import json
        data=load_design(SOURCE)
        self.assertEqual(SOURCE.name,'approved_design.json')
        self.assertEqual(sum(not is_collective(a) for a in data['agreements']),8)
        self.assertEqual(sum(is_collective(a) for a in data['agreements']),1)
        for a in data['agreements']:
            k=focus_key(a)
            preview=block(self.effects,'COLDWAR_CHL_preview_'+k)
            self.assertIsNotNone(preview)
            self.assertIsNotNone(block(self.effects,'COLDWAR_CHL_offer_'+k))
            can_offer=block(self.triggers,'COLDWAR_CHL_can_offer_'+k)
            self.assertIsNotNone(can_offer)
            clear=block(self.triggers,'COLDWAR_CHL_dip_'+varid(a)+'_clear')
            for tag in participants(a)[1:]:
                self.assertTrue(has(clear,'country_exists',tag),tag)
            self.assertIn('effect_tooltip',str(preview))
            sides=[('CHL',a['chile'])]
            if is_collective(a):
                sides += [(t,{**a['recipient'],'spirit':a['recipient_spirits'][t]}) for t in participants(a)[1:]]
            else:
                sides += [(a['partner'],a['recipient'])]
            for tag,side in sides:
                # The acceptance preview visibly names each country's exact spirit
                # and its payment amount, independently of offer/acceptance guards.
                self.assertIn(idea_id(a,tag),str(preview))
                if side.get('setup',0): self.assertTrue(has(preview,'treasury_change',n(-side['setup'])))
                self.assertTrue(has(preview,idea_id(a,tag)+'_weekly_payment',n(-round(side['weekly']*1000,5))))
                for stat,value in side.get('modifiers',{}).items():
                    numeric=f'COLDWAR_CHL_dip_preview_{varid(a)}_{tag.lower()}_{stat}'
                    self.assertTrue(has(preview,numeric,str(value)),numeric)
                    self.assertTrue(has(preview,'tooltip',f'COLDWAR_CHL_mod_{stat}_tt'),stat)
            txn=block(self.effects,'COLDWAR_CHL_dip_execute_'+varid(a))
            txn_if=block(txn,'if')
            txn_guard=block(txn_if,'limit')
            txn_body=[(key,op,value) for key,op,value in txn_if if key!='limit']
            self.assertIn('COLDWAR_CHL_dip_'+varid(a)+'_paid',str(txn_guard))
            for t in participants(a)[1:]:
                self.assertTrue(any(key=='country_exists' and value==t for key,op,value in walk(txn_guard)),t)
            self.assertIn('modify_treasury_effect',str(txn_body))
            self.assertNotIn('has_treasury',str(txn_guard))
            for side in [a['chile'],a['recipient']]:
                if side.get('setup',0): self.assertTrue(has(txn_body,'treasury_change',n(-side['setup'])))
            for building in a.get('buildings',[]):
                self.assertTrue(has(preview,'add_extra_state_shared_building_slots',str(building['levels'])))
                self.assertTrue(has(preview,'type',building['type']))
                self.assertTrue(has(txn_body,'add_extra_state_shared_building_slots',str(building['levels'])))
                self.assertTrue(has(txn_body,'type',building['type']))
            for research in a.get('research',[]):
                for rows in (preview,txn_body):
                    self.assertTrue(has(rows,'category',research['category']))
                    self.assertTrue(has(rows,'bonus',str(research['bonus'])))
                    self.assertTrue(has(rows,'uses',str(research['uses'])))
            # Each deal has its own focus key. The collective deal has one
            # recipient decision per named country, never a comma-delimited tag.
            if is_collective(a):
                for t in participants(a)[1:]:
                    self.assertIn(f'COLDWAR_CHL_DIP_accept_{varid(a)}_{t.lower()}',str(self.out['common/decisions/COLDWAR_CHL_1970_diplomacy.txt']))
                    self.assertIn(f'COLDWAR_CHL_DIP_refuse_{varid(a)}_{t.lower()}',str(self.out['common/decisions/COLDWAR_CHL_1970_diplomacy.txt']))
            else:
                self.assertIn(f'tag = {a["partner"]}',str(self.out['common/decisions/COLDWAR_CHL_1970_diplomacy.txt']))
        self.assertIsNotNone(block(self.effects,'COLDWAR_CHL_diplomacy_world_daily'))

    def test_each_named_recipient_controls_both_votes_and_preview_is_not_runtime_payout(self):
        import json
        data=load_design(SOURCE)
        decision_text=self.out['common/decisions/COLDWAR_CHL_1970_diplomacy.txt']
        effect_text=self.out['common/scripted_effects/COLDWAR_CHL_1970_diplomacy.txt']
        for a in data['agreements']:
            k=varid(a)
            recipients=participants(a)[1:]
            self.world.scope('CHL').flags.update({f'COLDWAR_CHL_dip_{k}_pending',f'COLDWAR_CHL_dip_{k}_awaiting'})
            for tag in recipients:
                self.world.scope(tag).flags.add(f'COLDWAR_CHL_dip_{k}_pending')
                suffix='_'+tag.lower() if is_collective(a) else ''
                for action in ('accept','refuse'):
                    key=f'COLDWAR_CHL_DIP_{action}_{k}{suffix}'
                    dec=block(self.decisions,key)
                    self.assertIsNotNone(dec,key)
                    self.assertTrue(evaluate(block(dec,'visible'),self.world,tag),key)
                    self.assertFalse(evaluate(block(dec,'visible'),self.world,'MEX'),key)
                helper=f'COLDWAR_CHL_dip_accept_{k}{suffix}'
                helper_guard=block(block(self.effects,helper),'if')
                self.assertTrue(any(key=='tag' and value==tag for key,op,value in walk(block(helper_guard,'limit'))),helper)
            preview=block(self.effects,'COLDWAR_CHL_preview_'+focus_key(a))
            # Display-only preview contains no transaction receipt or asset guard.
            self.assertNotIn(f'COLDWAR_CHL_dip_{k}_paid',str(preview))
            self.assertNotIn('can_build_',str(preview))
            self.assertNotIn(f'COLDWAR_CHL_dip_execute_{k}',str(preview))

    def test_notice_event_has_agreement_terms_as_numeric_preview_only(self):
        import json
        data=load_design(SOURCE)
        event_rows=[value for key,op,value in self.events if key=='country_event' and isinstance(value,list)]
        loc_text=self.out['localisation/english/COLDWAR_CHL_1970_diplomacy_l_english.yml']
        for i,a in enumerate([x for x in data['agreements'] if not is_collective(x)],1):
            cases=[case for case in event_rows if has(case,'id',f'COLDWAR_CHL_DIP.{i}')]
            self.assertEqual(len(cases),1)
            self.assertIn(f'COLDWAR_CHL_DIP.{i}.t:0 "{a["title"]}"',loc_text)
            self.assertIn(f'COLDWAR_CHL_DIP.{i}.d:0 "{a["description"]}"',loc_text)
            option=block(cases[0],'option')
            self.assertIn('COLDWAR_CHL_preview_'+focus_key(a),str(block(option,'effect_tooltip')))
            self.assertNotIn('modify_treasury_effect',str(option))
            self.assertNotIn('add_ideas',str(option))
        a=next(x for x in data['agreements'] if is_collective(x))
        for i,tag in enumerate(participants(a)[1:],20):
            cases=[case for case in event_rows if has(case,'id',f'COLDWAR_CHL_DIP.{i}')]
            self.assertEqual(len(cases),1,tag)
            self.assertIn(f'COLDWAR_CHL_DIP.{i}.t:0 "{a["title"]}"',loc_text)
            self.assertIn(f'COLDWAR_CHL_DIP.{i}.d:0 "{a["description"]}"',loc_text)
            option=block(cases[0],'option')
            self.assertIn('COLDWAR_CHL_preview_'+focus_key(a),str(block(option,'effect_tooltip')))
            self.assertNotIn('modify_treasury_effect',str(option))

    def test_bilateral_vote_is_recipient_scoped_and_transaction_is_once_guarded(self):
        a=next(x for x in load_design(SOURCE)['agreements'] if varid(x)=='usa_mines')
        k=varid(a);pending='COLDWAR_CHL_dip_'+k+'_pending';awaiting='COLDWAR_CHL_dip_'+k+'_awaiting'
        self.world.scope('CHL').flags.update({pending,awaiting})
        self.world.scope('USA').flags.add(pending)
        self.world.true_triggers.update({'COLDWAR_CHL_can_build_468_industrial_complex_1'})
        decision=block(self.decisions,'COLDWAR_CHL_DIP_accept_'+k)
        visible=block(decision,'visible');available=block(decision,'available')
        self.assertTrue(evaluate(visible,self.world,'USA'))
        self.assertFalse(evaluate(visible,self.world,'MEX'))
        self.assertTrue(evaluate(available,self.world,'USA'))
        self.world.relations[('CHL','USA')]['war']=True
        self.assertFalse(evaluate(available,self.world,'USA'))
        self.world.relations[('CHL','USA')]['war']=False
        helper=block(self.effects,'COLDWAR_CHL_dip_accept_'+k)
        helper_if=block(helper,'if');helper_limit=block(helper_if,'limit')
        self.assertTrue(evaluate(helper_limit,self.world,'USA'))
        self.assertFalse(evaluate(helper_limit,self.world,'MEX'))
        txn=block(self.effects,'COLDWAR_CHL_dip_execute_'+k);txn_if=block(txn,'if');txn_limit=block(txn_if,'limit')
        self.assertTrue(evaluate(txn_limit,self.world,'CHL'))
        self.world.scope('CHL').flags.add('COLDWAR_CHL_dip_'+k+'_paid')
        self.assertFalse(evaluate(txn_limit,self.world,'CHL'))
        completion=block(decision,'complete_effect')
        self.assertIsNotNone(block(completion,'effect_tooltip'))
        self.assertIsNotNone(block(completion,'hidden_effect'))

    def test_andes_requires_four_distinct_real_votes_and_rechecks_all_pairs(self):
        k='andean_protocol';pending=f'COLDWAR_CHL_dip_{k}_pending';awaiting=f'COLDWAR_CHL_dip_{k}_awaiting'
        chl=self.world.scope('CHL');chl.flags.update({pending,awaiting})
        self.world.scope('BOL').flags.add(pending)
        accept=block(self.effects,f'COLDWAR_CHL_dip_accept_{k}_bol')
        guard=block(block(accept,'if'),'limit')
        self.assertTrue(evaluate(guard,self.world,'BOL'))
        self.assertFalse(evaluate(guard,self.world,'COL'))
        for t in ('bol','col','ecu'):
            chl.flags.add(f'COLDWAR_CHL_dip_{k}_ratified_{t}')
        txn=block(self.effects,f'COLDWAR_CHL_dip_execute_{k}')
        txn_guard=block(block(txn,'if'),'limit')
        self.assertFalse(evaluate(txn_guard,self.world,'CHL'))
        chl.flags.add(f'COLDWAR_CHL_dip_{k}_ratified_pru')
        self.assertTrue(evaluate(txn_guard,self.world,'CHL'))
        clear=block(self.triggers,'COLDWAR_CHL_dip_andean_protocol_clear')
        for tag in ('CHL','BOL','COL','ECU','PRU'):
            self.assertTrue(any(key==tag and any(k=='has_idea' and v=='COLDWAR_CHL_cartagena_member' for k,o,v in walk(value)) for key,op,value in clear),tag)
        for tag in ('BOL','COL','ECU','PRU'):
            self.assertTrue(has(clear,'country_exists',tag),tag)
        pairs=[('CHL','BOL'),('CHL','COL'),('CHL','ECU'),('CHL','PRU'),('BOL','COL'),('BOL','ECU'),('BOL','PRU'),('COL','ECU'),('COL','PRU'),('ECU','PRU')]
        for x,y in pairs:
            self.assertTrue(any(key==x and any(k=='has_war_with' and v==y for k,o,v in walk(value)) for key,op,value in clear),(x,y))
        clear_text=str(clear)
        for sanction in ('imp_dip_sanc_on_us','imp_dip_sanc_by_us','imp_fin_sanc_on_us','imp_fin_sanc_by_us','imp_eco_sanc_on_us','imp_eco_sanc_by_us','imp_mil_sanc_on_us','imp_mil_sanc_by_us'):
            self.assertTrue(has(clear,'array',sanction))
        self.world.arrays[('CHL','imp_mil_sanc_on_us')]={'PRU'}
        self.assertFalse(evaluate(txn_guard,self.world,'CHL'))
        self.world.arrays.clear()
        self.world.scope('ECU').ideas.clear()
        self.assertFalse(evaluate(txn_guard,self.world,'CHL'))
        self.assertIn('country_event = { id = COLDWAR_CHL_DIP.104 }',self.out['common/scripted_effects/COLDWAR_CHL_1970_diplomacy.txt'])

    def test_expiry_is_one_shot_and_world_cleanup_keeps_receipts(self):
        k='usa_mines';awaiting=f'COLDWAR_CHL_dip_{k}_awaiting';pending=f'COLDWAR_CHL_dip_{k}_pending';receipt=f'COLDWAR_CHL_dip_{k}_receipt'
        chl=self.world.scope('CHL');chl.flags.update({awaiting,receipt})
        daily=block(self.effects,'COLDWAR_CHL_diplomacy_daily')
        expired=next(v for name,op,v in walk(daily) if name=='if' and isinstance(v,list) and awaiting in str(block(v,'limit')))
        limit=block(expired,'limit')
        self.world.true_triggers.add('scenario')
        self.assertTrue(evaluate(limit,self.world,'CHL'))
        chl.flags.add(pending);self.assertFalse(evaluate(limit,self.world,'CHL'))
        chl.flags.remove(pending);chl.flags.add(f'COLDWAR_CHL_dip_{k}_cooldown');self.assertFalse(evaluate(limit,self.world,'CHL'))
        world=block(self.effects,'COLDWAR_CHL_diplomacy_world_daily')
        text=str(world)
        self.assertIn('COLDWAR_CHL_dip_usa_mines_chl',text)
        self.assertIn('COLDWAR_CHL_diplomacy_weekly',text)
        self.assertNotIn('COLDWAR_CHL_dip_usa_mines_receipt',text)
        self.assertIn('COLDWAR_CHL_diplomacy_chl_absent_cleaned',text)
        self.assertTrue(any(key=='clr_country_flag' and value=='COLDWAR_CHL_dip_usa_mines_pending' for key,op,value in walk(world)))

if __name__=='__main__': unittest.main()
