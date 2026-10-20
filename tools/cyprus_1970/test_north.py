"""Focused dated-party and dormant-roster checks against emitted native scripts.

This small interpreter models only commands reached by these fixtures. It does
not emulate the game, native election logic, character rendering or MP sync.
"""
import json
import re
import unittest
from collections import defaultdict
from PIL import Image
from validate import ROOT, HERE, parse, first, vals, walk

N='COLDWAR_NCY_1970_'


def unquote(value):
    return json.loads(value) if value.startswith('"') else value


class RosterFixture:
    def __init__(self,tag='NCY',exists=True,date='1970.1.1',party=1,scenario=True):
        self.tag=tag;self.exists=exists;self.date=date;self.scenario=scenario;self.ai=False
        self.v=defaultdict(float,{'ruling_party':party});self.f=set();self.chars=set()
        self.leader=None;self.created=0
        self.effects={k:v for k,op,v in parse((ROOT/'common/scripted_effects/COLDWAR_NCY_1970_effects.txt').read_text(encoding='utf-8'))}

    def number(self,s):
        try:return float(s)
        except ValueError:return self.v[s]

    def term(self,k,op,v):
        if k in ('AND','OR','NOT'):
            results=[self.term(a,b,c) for a,b,c in v]
            return all(results) if k=='AND' else any(results) if k=='OR' else not any(results)
        if k=='date':
            a=tuple(map(int,self.date.split('.')));b=tuple(map(int,v.split('.')))
            return a<b if op=='<' else a>b if op=='>' else a==b
        if k=='original_tag':return v==self.tag
        if k=='exists':return self.exists==(v=='yes')
        if k=='IMP_is_1970_scenario':return self.scenario==(v=='yes')
        if k=='is_ai':return self.ai==(v=='yes')
        if k=='has_country_flag':return v in self.f
        if k=='has_variable':return v in self.v
        if k=='has_character':return v in self.chars
        if k=='has_country_leader':return unquote(first(v,'name'))==self.leader
        if k=='check_variable':
            name,cmp,value=v[0];a=self.number(name);b=self.number(value)
            return a==b if cmp=='=' else a>b if cmp=='>' else a<b
        raise AssertionError('Unmodelled trigger '+k)

    def test(self,ast):return all(self.term(k,op,v) for k,op,v in ast)

    def run(self,ast):
        matched=False
        for k,op,v in ast:
            if k in ('if','else_if'):
                execute=(k=='if' or not matched) and self.test(first(v,'limit',[]))
                if k=='if':matched=False
                if execute:
                    matched=True;self.run([x for x in v if x[0]!='limit'])
            elif k=='else':
                if not matched:self.run(v)
                matched=True
            elif k in self.effects:self.run(self.effects[k])
            elif k=='set_variable':
                name,_,value=v[0];self.v[name]=self.number(value)
            elif k=='set_country_flag':self.f.add(v)
            elif k=='recruit_character':
                assert v not in self.chars,'Duplicate recruitment '+v
                self.chars.add(v)
            elif k=='retire_character':self.chars.remove(v)
            elif k=='create_country_leader':self.leader=unquote(first(v,'name'));self.created+=1
            elif k=='update_set_politics':pass # Native political-system side effects are not emulated.
            elif k=='IMP_1970_profile_democratic_conservative':self.v['ruling_party']=1
            else:raise AssertionError('Unmodelled effect '+k)

    def call(self,key):self.run(self.effects[N+key])


class NorthTests(unittest.TestCase):
    def test_absent_country_wrong_tag_and_modern_start_remain_untouched(self):
        for fixture in (RosterFixture(exists=False),RosterFixture(tag='TUR'),RosterFixture(scenario=False)):
            fixture.call('initialize');fixture.call('refresh_roster');fixture.call('set_leader')
            self.assertEqual(fixture.chars,set());self.assertEqual(fixture.created,0);self.assertEqual(fixture.f,set())

    def test_new_country_initializes_once_and_never_recruits_future_officers(self):
        r=RosterFixture();r.chars.update({'NCY_sezai_ozturk','NCY_secme_akin'})
        r.call('daily_tick');r.call('daily_tick')
        self.assertEqual(r.created,1);self.assertEqual(r.leader,'Fazıl Küçük')
        self.assertIn(N+'kazandag',r.chars)
        self.assertFalse(any(N+'gkk_' in c for c in r.chars))
        self.assertNotIn(N+'eyupoglu',r.chars);self.assertNotIn(N+'berberoglu',r.chars)
        self.assertNotIn('NCY_sezai_ozturk',r.chars);self.assertNotIn('NCY_secme_akin',r.chars)

    def test_local_military_dates_and_late_country_creation(self):
        for date,expected in [('1970.7.31','kazandag'),('1970.8.1','eyupoglu'),
                              ('1972.7.1','eryilmaz'),('1974.9.1','basar'),('1976.8.1','gkk_1976')]:
            r=RosterFixture(date=date);r.call('daily_tick')
            military={c for c in r.chars if any(t in c for t in ('kazandag','eyupoglu','eryilmaz','basar','gkk_'))}
            self.assertEqual(military,{N+expected},date)
        r=RosterFixture(date='1976.7.31');r.call('daily_tick')
        self.assertNotIn(N+'gkk_1976',r.chars)
        r.date='1976.8.1';r.call('daily_tick');self.assertIn(N+'gkk_1976',r.chars)

    def test_calendar_turnover_is_an_optional_atomic_human_action(self):
        r=RosterFixture();r.call('daily_tick');r.date='1973.2.28';r.call('daily_tick')
        self.assertEqual(r.leader,'Fazıl Küçük')
        self.assertNotEqual(r.v[N+'leader_epoch'],r.v[N+'current_epoch'])
        r.ai=True;r.call('select_contemporary_leadership');self.assertEqual(r.created,1)
        r.ai=False;r.call('select_contemporary_leadership');self.assertEqual(r.leader,'Rauf Denktaş')
        r.call('select_contemporary_leadership');r.call('daily_tick');self.assertEqual(r.created,2)
        self.assertEqual(r.v['ruling_party'],1)

    def test_party_switch_uses_contemporary_representative_without_calendar_election(self):
        for date,party,name in [('1970.12.26',3,'Democratic Opposition Council'),
                               ('1970.12.27',3,'Ahmet Mithat Berberoğlu'),
                               ('1976.10.31',3,'Özker Özgür'),('1976.3.18',18,'Alpay Durduran'),
                               ('1983.11.6',18,'İsmail Bozkurt'),('1987.1.1',18,'Mustafa Akıncı')]:
            r=RosterFixture(date=date,party=party);r.call('daily_tick')
            self.assertEqual(r.leader,name);self.assertEqual(r.v['ruling_party'],party)
        r=RosterFixture(date='1980.1.1');r.call('daily_tick');r.v['ruling_party']=3;r.call('daily_tick')
        self.assertEqual(r.leader,'Özker Özgür');self.assertEqual(r.created,2)

    def test_advisors_have_dynamic_availability_and_valid_portraits(self):
        tree=parse((ROOT/'common/characters/COLDWAR_NCY_1970_characters.txt').read_text(encoding='utf-8'))
        chars=first(tree,'characters');self.assertEqual(len(chars),23)
        for key,op,body in chars:
            advisor=first(body,'advisor');allowed=first(advisor,'allowed');available=first(advisor,'available')
            self.assertEqual({k for k,op,v in allowed},{'original_tag','IMP_is_1970_scenario'})
            self.assertTrue(any(k=='date' for k,op,v in available))
            if not first(body,'corps_commander'):
                self.assertTrue(any(k=='ruling_only' and v=='yes' for k,op,v in walk(available)))
        assets=json.loads((HERE/'north/assets.json').read_text(encoding='utf-8'))['assets']
        for key,a in assets.items():
            for field,dim in [('portrait',(156,210)),('small',(38,51))]:
                with Image.open(ROOT/a[field]) as im:self.assertEqual(im.size,dim);self.assertEqual(im.format,'DDS')
        self.assertEqual(sum(a['status']=='image_gen_restored_historical_reference' for a in assets.values()),23)
        self.assertEqual(assets['generic']['status'],'collective_institution_emblem')
        self.assertFalse(any(a['status'] in ('generic_placeholder','existing_native_portrait','official_colour_photo') for a in assets.values()))
        named=[a['sha256'] for k,a in assets.items() if k!='generic']
        self.assertEqual(len(set(named)),23,'Historical people share a portrait')

    def test_all_party_slots_and_historical_name_boundaries(self):
        from politics import IDEOLOGIES
        tree=parse((ROOT/'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt').read_text(encoding='utf-8'))
        definitions={first(d,'name'):d for k,op,d in tree if k=='defined_text'}
        loc=dict((k,json.loads(v)) for k,v in re.findall(r'^ (\S+):0 (".*")$',
            (ROOT/'localisation/english/COLDWAR_CYP_1970_l_english.yml').read_text(encoding='utf-8-sig'),re.M))
        def label(tag,index,date,suffix=''):
            r=RosterFixture(tag=tag,date=date)
            for row in vals(definitions[IDEOLOGIES[index]+'_L'+suffix],'text'):
                key=first(row,'localization_key')
                if key and key.startswith('COLDWAR_'+tag+'_1970_party_') and r.test(first(row,'trigger',[])):
                    return loc[key]
            raise AssertionError((tag,index,date,suffix))
        for tag in ('CYP','NCY'):
            for index in range(24):
                for suffix in ('','_desc','_icon'):self.assertTrue(label(tag,index,'1970.1.1',suffix))
        for tag,index,before,on,old,new in [('NCY',3,'1970.12.26','1970.12.27','Democratic Opposition','CTP'),
            ('NCY',1,'1975.10.10','1975.10.11','Communal Administration','UBP'),
            ('NCY',18,'1976.3.17','1976.3.18','Independents','TKP'),
            ('NCY',22,'1976.7.31','1976.8.1','TMT','GKK'),
            ('CYP',2,'1976.7.3','1976.7.4','Eniaion','DISY'),
            ('CYP',1,'1976.12.3','1976.12.4','Democratic Alignment','DIKO')]:
            self.assertIn(old,label(tag,index,before));self.assertIn(new,label(tag,index,on))

    def test_no_formation_war_or_territorial_payload_and_dispatch_intercepts_modern_kill(self):
        ast=parse((ROOT/'common/scripted_effects/COLDWAR_NCY_1970_effects.txt').read_text(encoding='utf-8'))
        keys={k for k,op,v in walk(ast)}
        self.assertFalse(keys & {'release','release_puppet','transfer_state','declare_war_on','load_oob','create_unit','set_politics','set_popularities'})
        central=(ROOT/'common/scripted_effects/00_leader_setup_scripted_effects.txt').read_text(encoding='utf-8')
        self.assertLess(central.index(N+'set_leader = yes'),central.index('kill_country_leader = yes'))


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(NorthTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    (HERE/'north/validation.json').write_text(json.dumps({'passed':result.wasSuccessful(),
        'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'party_slots':48,'people':23,'in_game_test_performed':False},indent=2)+'\n',encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
