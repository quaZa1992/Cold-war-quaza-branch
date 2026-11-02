# IMPERIA COLD WAR — Emitted diplomacy contracts and historical roster regression tests
"""Bounded source model. Does not emulate HOI4 event delivery, netcode or rendering."""
import copy
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/colonial_affairs'))
from test_runtime import Model, Scope, D, parse, first
from build import MEMBERS, PERMANENT, DEPARTING_1970, HELD_1971


def load(rel):
    return parse((ROOT/rel).read_text(encoding='utf-8-sig'))


def walk(rows):
    for row in rows:
        yield row
        if isinstance(row[2], list):
            yield from walk(row[2])


class DiplomacyModel(Model):
    def __init__(self):
        super().__init__()
        # IMPERIA COLD WAR — Model existing 1970 recognition cases without assigning UN membership.
        self.c = {t:Scope(t) for t in set(MEMBERS)|set('GER DDR CHI NKO VIE SWI KOR SVN QAT BHU FIJ UAE BIA ZIM'.split())}
        self.root = self.c['GER']
        self.requests = []
        self.api_calls = []
        for kind in ('effects', 'triggers'):
            getattr(self,kind).update((k,v) for k,o,v in load('common/scripted_'+kind+'/COLDWAR_diplomacy_1970.txt'))
            # IMPERIA COLD WAR — Load the actual recognition-catalogue providers.
            getattr(self,kind).update((k,v) for k,o,v in load('common/scripted_'+kind+'/ICW_recognition_picker_1970.txt'))
        self.effects['un_recog_setup_check'] = first(load('common/scripted_effects/01_international_systems_effects.txt'),'un_recog_setup_check')
        # IMPERIA COLD WAR — Exercise the native ledger-count branch; milestone news and PP rewards are outside this model.
        self.effects['recognition_grant_increment'] = first(load('common/scripted_effects/01_international_systems_effects.txt'),'recognition_grant_increment')[:2]
        # IMPERIA COLD WAR — Exercise the actual native eligibility provider and emitted dossier text.
        native_triggers = load('common/scripted_triggers/01_international_triggers.txt')
        for key in ('can_seek_permanent_unsc_seat','can_campaign_for_permanent_unsc_seat','is_on_un_sec_council'):
            self.triggers[key] = first(native_triggers,key)
        p5 = first(first(load('common/ideas/Organizations.txt'),'ideas'),'country')
        self.p5 = first(p5,'p5_member')

    def value(self, name, current, root, prev):
        if isinstance(name,str) and name.startswith('var:'):
            return self.scope(name,current,root,prev)
        return super().value(name,current,root,prev)

    def condition(self, rows, current, root=None, prev=None):
        root = root or current
        for k,o,v in rows:
            if k == 'is_in_array':
                obj,name = self.variable(v[0][0],current,root,prev)
                ok = self.value(v[0][2],current,root,prev) in obj.vars.get(name,[])
            elif k == 'has_civil_war':
                ok = ('_civil_war' in current.flags) == (v == 'yes')
            elif k == 'is_full_state':
                ok = ('non_state_actor' not in current.ideas) == (v == 'yes')
            elif k == 'country_exists':
                ok = self.scope(v,current,root,prev) in self.c.values()
            # IMPERIA COLD WAR — A stale country reference is not an existing country.
            elif k == 'exists':
                ok = (current in self.c.values()) == (v == 'yes')
            elif k == 'has_cosmetic_tag':
                ok = getattr(current, 'cosmetic', '') == v
            elif k == 'if':
                ok = not self.condition(first(v,'limit',[]),current,root,prev) or self.condition([r for r in v if r[0]!='limit'],current,root,prev)
            else:
                ok = super().condition([(k,o,v)],current,root,prev)
            if not ok:
                return False
        return True

    def execute(self, rows, current, root, prev):
        last_if = None
        for k,o,v in rows:
            if k == 'if':
                last_if = self.condition(first(v,'limit',[]),current,root,prev)
                if last_if:self.execute([r for r in v if r[0]!='limit'],current,root,prev)
            elif k == 'else_if':
                if last_if is False:
                    last_if = self.condition(first(v,'limit',[]),current,root,prev)
                    if last_if:self.execute([r for r in v if r[0]!='limit'],current,root,prev)
            elif k == 'else':
                if last_if is False:self.execute(v,current,root,prev)
                last_if = None
            elif k in ('add_to_array','remove_from_array'):
                obj,name = self.variable(v[0][0],current,root,prev)
                value = self.value(v[0][2],current,root,prev)
                values = obj.vars.setdefault(name,[])
                if k == 'add_to_array':values.append(value)
                else:values[:] = [item for item in values if item is not value]
            elif k == 'clear_array':
                obj,name = self.variable(v,current,root,prev);obj.vars[name] = []
            # IMPERIA COLD WAR — Interpret native explicit var/value subtraction for recognition counts.
            elif k == 'subtract_from_variable' and first(v,'var') is not None:
                super().execute([(k,o,[(first(v,'var'),'=',first(v,'value'))])],current,root,prev)
            # IMPERIA COLD WAR — Iterate the existing small catalogue, never an implicit world scan.
            elif k == 'for_each_scope_loop':
                obj,name = self.variable(first(v,'array'),current,root,prev)
                for target in list(obj.vars.get(name,[])):
                    self.execute([row for row in v if row[0]!='array'],target,root,current)
            # IMPERIA COLD WAR — Native recognition button meta-text uses opaque owner flags in these fixtures.
            elif k == 'meta_effect':
                self.execute(first(v,'text'),current,root,prev)
            elif k == 'every_collection_element':
                assert first(v,'input') == [('input','=','collection:un_general_assembly_members_collection')]
                for target in list(self.g.vars.get('UN_general_assembly',[])):
                    self.execute([row for row in v if row[0]!='input'],target,root,current)
            elif k == 'random_country':
                eligible = [c for c in self.c.values() if self.condition(first(v,'limit',[]),c,root,current)]
                if eligible:
                    self.execute([row for row in v if row[0]!='limit'],eligible[0],root,current)
            elif k in ('set_global_flag','clr_global_flag'):
                flag = first(v,'flag') if isinstance(v,list) else v
                self.g.flags.add(flag) if k == 'set_global_flag' else self.g.flags.discard(flag)
            elif k in ('add_ideas','remove_ideas'):
                exists = v in current.ideas
                current.ideas.add(v) if k=='add_ideas' else current.ideas.discard(v)
                if v=='p5_member' and exists != (k=='add_ideas'):
                    self.execute(first(self.p5,'on_add' if k=='add_ideas' else 'on_remove'),current,root,prev)
            elif k == 'update_sc_vote':
                self.requests.append((current.vars['sc_new_vote_type'],current.vars['sc_new_vote_nation'].id))
            elif k in ('country_event','news_event') and isinstance(v,str):
                self.events.append((v,current.id,dict(self.saved_targets)))
            # IMPERIA COLD WAR — Both native GUI invalidation providers remain outside the bounded model.
            elif k in ('recompute_un_2_3_number','recompute_un_sc_required_yes','international_systems_force_update','international_systems_update','COLDWAR_GER_1970_rv_sync_views','COLDWAR_GER_1970_rv_update_stage','COLDWAR_GER_1970_east_gui_refresh'):
                # Providers exist in native MD. Their queue math/UI is outside this model.
                self.api_calls.append(k)
            elif k == 'unlock_decision_tooltip':
                self.api_calls.append((k,v))
            else:
                super().execute([(k,o,v)],current,root,prev)


class Diplomacy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.template = DiplomacyModel()

    def setUp(self):self.m = copy.deepcopy(self.template)

    def test_january_roster_excludes_later_admissions_and_prc(self):
        for c in self.m.c.values():c.modifiers.add('united_nations_member')
        self.m.c['CHI'].ideas.add('p5_member')
        self.m.c['TAI'].ideas.update(('lacks_international_recognition','non_state_actor'))
        self.m.run('COLDWAR_UN_1970_initialize')
        members = self.m.g.vars['UN_general_assembly']
        self.assertEqual({c.id for c in members},set(MEMBERS))
        self.assertEqual(len(members),126)
        for tag in 'GER DDR CHI NKO VIE SWI KOR SVN QAT BHU FIJ UAE'.split():
            self.assertNotIn('united_nations_member',self.m.c[tag].modifiers)
        self.assertNotIn('non_state_actor',self.m.c['TAI'].ideas)

    def test_council_cohorts_and_native_veto_idea_agree(self):
        self.m.run('COLDWAR_UN_1970_initialize')
        self.assertEqual([c.id for c in self.m.g.vars['security_council_members']],DEPARTING_1970+HELD_1971+PERMANENT)
        self.assertEqual({c.id for c in self.m.g.vars['p5_sc_members']},set(PERMANENT))
        self.assertTrue(all('p5_member' in self.m.c[t].ideas for t in PERMANENT))
        self.assertNotIn('p5_member',self.m.c['CHI'].ideas)

    def test_soviet_republic_founders_keep_separate_assembly_seats(self):
        soviet=self.m.c['SOV']
        for tag in ('UKR','BLR'):
            self.m.c[tag].overlord=soviet
        for tag in ('KAZ','ARM'):
            self.m.c[tag]=Scope(tag,overlord=soviet)
        self.m.run('COLDWAR_UN_1970_initialize')
        members=self.m.g.vars['UN_general_assembly']
        self.assertEqual(len(members),126)
        for tag in ('SOV','UKR','BLR'):
            self.assertEqual(members.count(self.m.c[tag]),1)
            self.assertIn('united_nations_member',self.m.c[tag].modifiers)
        for tag in ('UKR','BLR'):
            self.assertIs(self.m.c[tag].overlord,soviet)
            self.assertNotIn(self.m.c[tag],self.m.g.vars['security_council_members'])
            self.assertNotIn(self.m.c[tag],self.m.g.vars['p5_sc_members'])
            self.assertNotIn('p5_member',self.m.c[tag].ideas)
        for tag in ('KAZ','ARM'):
            self.assertNotIn(self.m.c[tag],members)
            self.assertNotIn('united_nations_member',self.m.c[tag].modifiers)
        self.m.run('COLDWAR_UN_1970_initialize')
        for tag in ('SOV','UKR','BLR'):
            self.assertEqual(members.count(self.m.c[tag]),1)

    def test_soviet_republics_cast_their_own_native_assembly_votes(self):
        for tag in ('UKR','BLR'):
            self.m.c[tag].overlord=self.m.c['SOV']
        self.m.run('COLDWAR_UN_1970_initialize')
        events={first(v,'id'):v for k,o,v in load('events/UN_Voting_Events.txt') if k=='country_event'}
        options={first(v,'name'):v for k,o,v in events['UN.6'] if k=='option'}
        self.m.g.flags.add('current_ongoing_ga_vote')
        for tag,option,result in [('SOV','UN.6.a','yes'),('UKR','UN.6.b','no'),('BLR','UN.6.c','abstain')]:
            country=self.m.c[tag]
            effects=[row for row in options[option] if row[0] not in ('name','log','ai_chance')]
            self.m.execute(effects,country,country,None)
            self.assertEqual(self.m.g.vars['general_assembly_vote_'+result],[country])
        self.assertIs(self.m.c['UKR'].overlord,self.m.c['SOV'])
        self.assertIs(self.m.c['BLR'].overlord,self.m.c['SOV'])

    def test_roster_initialization_never_overwrites_later_player_admission(self):
        self.m.run('COLDWAR_UN_1970_initialize')
        self.m.g.vars['UN_general_assembly'].append(self.m.c['DDR'])
        self.m.run('COLDWAR_UN_1970_initialize')
        self.assertIn(self.m.c['DDR'],self.m.g.vars['UN_general_assembly'])

    def test_non_1970_setup_is_unchanged(self):
        self.m.scenario = False
        self.m.run('COLDWAR_UN_1970_initialize')
        self.assertFalse(self.m.g.flags)
        self.m.run('un_recog_setup_check',self.m.c['QAT'])
        self.assertIn(self.m.c['QAT'],self.m.g.vars['UN_general_assembly'])

    def test_released_nonmember_does_not_join_automatically(self):
        self.m.run('un_recog_setup_check',self.m.c['QAT'])
        self.assertNotIn('UN_general_assembly',self.m.g.vars)
        self.m.run('un_recog_setup_check',self.m.c['DDR'])
        self.assertIn(self.m.c['DDR'],self.m.g.vars['Unrecognised_States'])
        self.assertNotIn('lacks_international_recognition',self.m.c['DDR'].ideas)

    def test_native_recognition_buttons_allow_both_germanies_and_independent_withdrawal(self):
        gui = first(first(load('common/scripted_guis/00_missiles_scripted_guis.txt'),'scripted_gui'),'MD_UN_system_gui')
        triggers = first(gui,'triggers');effects = first(gui,'effects')
        actor = self.m.c['SWI'];actor.pp = D(100)
        for target in ('GER','DDR'):
            actor.vars['open_state'] = self.m.c[target]
            self.assertTrue(self.m.condition(first(triggers,'grant_recog_button_click_enabled'),actor))
            mutation = next(r for r in walk(first(effects,'grant_recog_button_click')) if r[0]=='add_to_array' and r[2]==[('recognised_countries','=','var:open_state')])
            self.m.execute([mutation],actor,actor,None)
            self.m.run('COLDWAR_Germany_recount_recognition',self.m.c[target])
        self.assertEqual([c.id for c in actor.vars['recognised_countries']],['GER','DDR'])
        self.assertTrue(self.m.condition(first(triggers,'rescind_recog_button_click_enabled'),actor))
        mutation = next(r for r in walk(first(effects,'rescind_recog_button_click')) if r[0]=='remove_from_array')
        self.m.execute([mutation],actor,actor,None)
        self.m.run('COLDWAR_Germany_recount_recognition',self.m.c['DDR'])
        self.assertEqual([c.id for c in actor.vars['recognised_countries']],['GER'])
        self.assertEqual(self.m.c['DDR'].vars['Granted_Recognition'],0)
        self.assertEqual(self.m.c['GER'].vars['Granted_Recognition'],1)

    def test_both_states_are_visible_in_the_native_country_picker(self):
        gui = first(first(load('common/scripted_guis/00_missiles_scripted_guis.txt'),'scripted_gui'),'international_state_unrecognized_countries_dynamic_lists')
        trigger = first(first(gui,'triggers'),'name_of_state_button_visible')
        actor = self.m.c['SWI']
        for target in ('GER','DDR'):
            actor.vars['v'] = self.m.c[target]
            self.assertTrue(self.m.condition(trigger,actor))

    # IMPERIA COLD WAR — Regress the complete recognition catalogue and actual German button transactions.
    def test_recognition_picker_includes_all_twelve_1970_cases_without_changing_membership_or_choices(self):
        self.m.run('COLDWAR_UN_1970_initialize')
        actor=self.m.c['SWI']
        ledger={tag:list(c.vars.get('recognised_countries',[])) for tag,c in self.m.c.items()}
        members=list(self.m.g.vars['UN_general_assembly'])
        modifiers={tag:set(c.modifiers) for tag,c in self.m.c.items()}
        for _ in range(2):self.m.run('ICW_refresh_recognition_candidates',actor)
        catalogue=self.m.g.vars['ICW_recognition_candidates']
        self.assertEqual({c.id for c in catalogue},set('GER DDR CHI TAI NKO KOR VIE SVN ISR MON BIA ZIM'.split()))
        self.assertEqual(len(catalogue),12)
        self.assertEqual(self.m.g.vars['UN_general_assembly'],members)
        self.assertEqual({tag:list(c.vars.get('recognised_countries',[])) for tag,c in self.m.c.items()},ledger)
        self.assertEqual({tag:set(c.modifiers) for tag,c in self.m.c.items()},modifiers)
        self.assertFalse(any('lacks_international_recognition' in c.ideas for c in catalogue))

    def test_recognition_picker_keeps_native_breakaways_and_deduplicates_them(self):
        abk=Scope('ABK');abk.ideas.add('lacks_international_recognition');self.m.c['ABK']=abk
        self.m.g.vars['Unrecognised_States']=[abk,abk,self.m.c['GER']]
        self.m.run('ICW_refresh_recognition_candidates',self.m.c['SWI'])
        catalogue=self.m.g.vars['ICW_recognition_candidates']
        self.assertEqual(sum(c is abk for c in catalogue),1)
        self.assertEqual(len(catalogue),13)
        self.assertEqual(self.m.g.vars['Unrecognised_States'],[abk,abk,self.m.c['GER']])

    def test_existing_saves_refresh_catalogue_when_the_recognition_tab_opens(self):
        actor=self.m.c['SWI'];actor.vars['open_state']=self.m.c['DDR']
        gui=first(load('common/scripted_guis/00_missiles_scripted_guis.txt'),'scripted_gui')
        button=next(first(first(v,'effects'),'un_state_recog_btn_click') for k,o,v in gui if isinstance(v,list) and first(first(v,'effects',[]),'un_state_recog_btn_click') is not None)
        self.m.execute(button,actor,actor,None)
        self.assertEqual(len(self.m.g.vars['ICW_recognition_candidates']),12)
        self.assertIs(actor.vars['open_state'],self.m.c['DDR'])
        self.assertEqual(actor.vars['var_open_MD_state_recog'],2)
        self.assertFalse(self.m.g.flags)

    def test_recognition_catalogue_does_not_add_future_or_absent_states(self):
        gone=self.m.c.pop('BIA')
        self.m.run('ICW_refresh_recognition_candidates',self.m.c['SWI'])
        self.assertNotIn(gone,self.m.g.vars['ICW_recognition_candidates'])
        self.assertNotIn(self.m.c['QAT'],self.m.g.vars['ICW_recognition_candidates'])
        actor=self.m.c['SWI'];actor.vars['v']=gone
        gui=first(first(load('common/scripted_guis/00_missiles_scripted_guis.txt'),'scripted_gui'),'international_state_unrecognized_countries_dynamic_lists')
        self.assertFalse(self.m.condition(first(first(gui,'triggers'),'name_of_state_button_visible'),actor))
        self.m.scenario=False
        self.m.run('ICW_refresh_recognition_candidates',actor)
        self.assertFalse(self.m.g.vars['ICW_recognition_candidates'])

    def test_newly_created_subject_registers_once_without_an_un_admission(self):
        bia=self.m.c['BIA']
        for _ in range(2):self.m.run('un_recog_setup_check',bia)
        self.assertEqual(self.m.g.vars['ICW_recognition_candidates'],[bia])
        self.assertNotIn('united_nations_member',bia.modifiers)
        self.assertNotIn('UN_general_assembly',self.m.g.vars)

    def test_full_native_buttons_recognise_both_germanies_and_rescind_only_one(self):
        gui=first(first(load('common/scripted_guis/00_missiles_scripted_guis.txt'),'scripted_gui'),'MD_UN_system_gui')
        effects=first(gui,'effects');actor=self.m.c['SWI'];actor.pp=D(100)
        for target in ('GER','DDR'):
            actor.vars['open_state']=self.m.c[target]
            self.m.execute(first(effects,'grant_recog_button_click'),actor,actor,None)
        self.assertEqual([c.id for c in actor.vars['recognised_countries']],['GER','DDR'])
        self.assertEqual(actor.pp,50)
        self.m.execute(first(effects,'grant_recog_button_click'),actor,actor,None)
        self.assertEqual(actor.pp,50)
        actor.vars['open_state']=self.m.c['GER']
        self.m.execute(first(effects,'rescind_recog_button_click'),actor,actor,None)
        # Native rescission requires 25 PP but has no deduction; this picker fix preserves that behavior.
        self.assertEqual(actor.pp,50)
        self.assertEqual(actor.vars['recognised_countries'],[self.m.c['DDR']])
        self.assertEqual(self.m.c['DDR'].vars['Granted_Recognition'],1)
        self.assertEqual(self.m.c['GER'].vars['Granted_Recognition'],0)
        self.assertFalse(self.m.g.vars.get('UN_general_assembly'))

    # IMPERIA COLD WAR — Both Korean states retain independent bilateral recognition in either order.
    def test_full_native_buttons_recognise_both_koreas_independently(self):
        gui=first(first(load('common/scripted_guis/00_missiles_scripted_guis.txt'),'scripted_gui'),'MD_UN_system_gui')
        effects=first(gui,'effects');triggers=first(gui,'triggers')
        for order in (('NKO','KOR'),('KOR','NKO')):
            for withdrawn in order:
                with self.subTest(order=order,withdrawn=withdrawn):
                    self.m=copy.deepcopy(self.template)
                    actor=self.m.c['SWI'];actor.pp=D(100)
                    for target in order:
                        actor.vars['open_state']=self.m.c[target]
                        self.assertTrue(self.m.condition(first(triggers,'grant_recog_button_click_enabled'),actor))
                        self.m.execute(first(effects,'grant_recog_button_click'),actor,actor,None)
                    self.assertEqual([c.id for c in actor.vars['recognised_countries']],list(order))
                    self.assertEqual(actor.pp,50)
                    self.assertFalse(self.m.condition(first(triggers,'grant_recog_button_click_enabled'),actor))
                    self.m.execute(first(effects,'grant_recog_button_click'),actor,actor,None)
                    self.assertEqual(actor.pp,50)
                    self.assertEqual(len(actor.vars['recognised_countries']),2)
                    actor.vars['open_state']=self.m.c[withdrawn]
                    self.assertTrue(self.m.condition(first(triggers,'rescind_recog_button_click_enabled'),actor))
                    self.m.execute(first(effects,'rescind_recog_button_click'),actor,actor,None)
                    retained=next(tag for tag in order if tag!=withdrawn)
                    self.assertEqual(actor.vars['recognised_countries'],[self.m.c[retained]])
                    self.assertEqual(self.m.c[withdrawn].vars['Granted_Recognition'],0)
                    self.assertEqual(self.m.c[retained].vars['Granted_Recognition'],1)
                    self.assertTrue(self.m.condition(first(triggers,'grant_recog_button_click_enabled'),actor))
                    self.m.execute(first(effects,'grant_recog_button_click'),actor,actor,None)
                    self.assertEqual({c.id for c in actor.vars['recognised_countries']},{'NKO','KOR'})
                    self.assertEqual(actor.pp,25)
                    self.assertFalse(self.m.g.vars.get('UN_general_assembly'))

    def test_all_additional_subjects_are_eligible_for_bilateral_recognition(self):
        gui=first(first(load('common/scripted_guis/00_missiles_scripted_guis.txt'),'scripted_gui'),'MD_UN_system_gui')
        trigger=first(first(gui,'triggers'),'grant_recog_button_click_enabled')
        actor=self.m.c['SWI'];actor.pp=D(25)
        self.m.c['TAI'].modifiers.add('united_nations_member')
        for target in 'CHI TAI NKO KOR VIE SVN ISR MON BIA ZIM'.split():
            actor.vars['open_state']=self.m.c[target]
            self.assertTrue(self.m.condition(trigger,actor),target)

    def test_recognition_grid_fits_its_native_entries_and_compact_labels(self):
        from pathlib import Path
        containers=[v for k,o,v in load('interface/MD_countrymissilesview.gui') if k=='guiTypes' for key,op,v in v if key=='containerWindowType']
        holder=next(v for v in containers if first(v,'name')=='"IS_unrecognized_states_container"')
        entry=next(v for v in containers if first(v,'name')=='"IS_states_to_recognize_list"')
        main=next(v for v in containers if first(v,'name')=='"MD_UN_system_window"')
        button=first(entry,'buttonType');grid=first(holder,'gridboxType')
        self.assertEqual(first(button,'buttonText'),'"[ICW_recognition_picker_name]"')
        self.assertEqual(first(grid,'max_slots_horizontal'),'2')
        self.assertLessEqual(int(first(first(button,'position'),'x'))+148,int(first(first(grid,'slotsize'),'width')))
        self.assertLessEqual(34,int(first(first(grid,'slotsize'),'height')))
        selected=next(v for k,o,v in main if k=='instantTextBoxType' and first(v,'name')=='"ir_nation_sel_disp"')
        self.assertLess(int(first(first(holder,'position'),'y'))+int(first(first(holder,'size'),'height')),int(first(first(selected,'position'),'y')))
        self.assertLessEqual(int(first(first(grid,'padding'),'top')),4)
        raw=(ROOT/'localisation/english/ICW_recognition_picker_1970_l_english.yml').read_bytes()
        self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
        font=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/gfx/fonts/hoi_16mbs.fnt')
        if font.exists():
            glyphs={};kernings={}
            for line in font.read_text(encoding='utf-8-sig').splitlines():
                row={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
                if line.startswith('char '):glyphs[row['id']]=row['xadvance']
                elif line.startswith('kerning '):kernings[row['first'],row['second']]=row['amount']
            for key,text in re.findall(r'^ (\w+): "(.*)"$',raw.decode('utf-8-sig'),re.M):
                if key.endswith('native_name'):continue
                label=re.sub(r'\[[^\]]+\]','',text).strip()
                width=sum(glyphs.get(ord(c),glyphs[63]) for c in label)+sum(kernings.get((ord(a),ord(b)),0) for a,b in zip(label,label[1:]))
                self.assertLessEqual(width+16+12,148,(label,width))

    # IMPERIA COLD WAR — Short labels preserve the native name after reunification or outside 1970.
    def test_compact_recognition_labels_route_to_the_selected_country(self):
        text=next(v for k,o,v in load('common/scripted_localisation/ICW_recognition_picker_1970.txt') if k=='defined_text')
        actor=self.m.c['SWI']
        def resolve(target):
            actor.vars['v']=self.m.c[target]
            return next(first(v,'localization_key') for k,o,v in text if k=='text' and self.m.condition(first(v,'trigger',[]),actor))
        self.assertEqual(resolve('GER'),'ICW_recognition_picker_west_germany')
        self.assertEqual(resolve('DDR'),'ICW_recognition_picker_east_germany')
        self.assertEqual(resolve('VIE'),'ICW_recognition_picker_north_vietnam')
        self.assertEqual(resolve('SVN'),'ICW_recognition_picker_south_vietnam')
        self.assertEqual(resolve('NKO'),'ICW_recognition_picker_north_korea')
        self.assertEqual(resolve('KOR'),'ICW_recognition_picker_south_korea')
        self.assertEqual(resolve('TAI'),'ICW_recognition_picker_roc')
        self.m.c['CHI'].cosmetic='CHI_PRC_1970'
        self.assertEqual(resolve('CHI'),'ICW_recognition_picker_prc')
        self.m.c.pop('DDR')
        self.assertEqual(resolve('GER'),'ICW_recognition_picker_native_name')
        self.m.scenario=False
        self.assertEqual(resolve('TAI'),'ICW_recognition_picker_native_name')

    def test_opening_january_does_not_rotate_the_historical_cohort(self):
        effect = first(load('common/scripted_effects/01_international_systems_effects.txt'),'update_security_council_peeps')
        guard = first(first(effect,'if'),'limit')
        self.assertFalse(self.m.condition(guard,self.m.root))
        self.m.date = '1971.1.1'
        self.assertTrue(self.m.condition(guard,self.m.root))
        self.m.date = '2000.1.1';self.m.scenario = False
        self.assertTrue(self.m.condition(guard,self.m.root))

    def test_ddr_campaign_exact_price_and_stale_native_order(self):
        for kind in ('effects','triggers'):
            self.m.__dict__[kind].update((k,v) for k,o,v in load('common/scripted_'+kind+'/COLDWAR_DDR_1970_relations.txt'))
        g,d = self.m.c['GER'],self.m.c['DDR'];p = 'COLDWAR_GER_1970'
        g.flags.update(('cwgg_initialized',p+'_initialized'));d.flags.add(p+'_ddr_initialized')
        d.pp = D(199)
        self.m.run(p+'_east_act_recognition_drive',d)
        self.assertEqual(d.pp,199);self.assertFalse(self.m.events)
        d.pp = D(200)
        self.m.run(p+'_east_act_recognition_drive',d)
        self.assertEqual(d.pp,0);self.assertEqual(len(self.m.events),1)
        self.m.run(p+'_east_act_recognition_drive',d)
        self.assertEqual(d.pp,0);self.assertEqual(len(self.m.events),1)
        d.pp = D(200) - 200  # Native engine already charged this stale order.
        self.m.run(p+'_east_native_recognition_drive',d)
        self.assertEqual(d.pp,200);self.assertEqual(len(self.m.events),1)

    def test_mutual_recognition_keeps_third_country_choices_and_is_idempotent(self):
        self.m.c['SWI'].vars['recognised_countries'] = [self.m.c['DDR'],self.m.c['GER']]
        for _ in range(2):self.m.run('COLDWAR_Germany_mutual_recognition')
        self.assertEqual(self.m.c['GER'].vars['recognised_countries'],[self.m.c['DDR']])
        self.assertEqual(self.m.c['DDR'].vars['recognised_countries'],[self.m.c['GER']])
        self.assertEqual(self.m.c['DDR'].vars['Granted_Recognition'],2)
        self.assertEqual(len(self.m.c['SWI'].vars['recognised_countries']),2)

    def test_joint_applications_queue_two_votes_without_granting_membership(self):
        self.m.run('COLDWAR_Germany_joint_un_applications')
        self.m.run('COLDWAR_Germany_joint_un_applications')
        self.assertEqual(self.m.requests,[(5,'GER'),(5,'DDR')])
        self.assertFalse(self.m.g.vars.get('UN_general_assembly'))
        self.assertNotIn('united_nations_member',self.m.c['DDR'].modifiers)

    def test_campaign_waits_for_recipients_and_shares_native_lock(self):
        d = self.m.c['DDR']
        self.m.run('COLDWAR_Germany_campaign_recognition',d)
        self.m.run('COLDWAR_Germany_campaign_recognition',d)
        self.assertEqual([e[0] for e in self.m.events],['recognition.17'])
        self.assertFalse(any(c.vars.get('recognised_countries') for c in self.m.c.values()))
        gui = first(first(load('common/scripted_guis/00_missiles_scripted_guis.txt'),'scripted_gui'),'MD_UN_system_gui')
        d.pp = D(500)
        self.assertFalse(self.m.condition(first(first(gui,'triggers'),'un_campaign_for_recog_button_click_enabled'),d))

    def test_player_text_has_ascii_minus_and_no_retired_points(self):
        for rel in ('localisation/english/COLDWAR_DDR_1970_relations_l_english.yml','localisation/english/COLDWAR_GER_1970_l_english.yml'):
            raw = (ROOT/rel).read_bytes();self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            lines = [line for line in raw.decode('utf-8-sig').splitlines() if not line.lstrip().startswith('#')]
            self.assertFalse(any(c in '\n'.join(lines) for c in ('\u2212','\u2013','\u2014')))
            self.assertFalse(re.search(r'(?<!\[)\?\d','\n'.join(lines)))
            self.assertNotIn('cwddr_recognition','\n'.join(lines))

    # IMPERIA COLD WAR — Membership, elected mandates and permanent-seat campaigning share native state.
    def test_permanent_seat_focus_unlocks_native_campaign_without_granting_a_seat(self):
        g = self.m.c['GER']
        tree = first(load('common/national_focus/COLDWAR_GER_1970_focus.txt'),'focus_tree')
        focus = next(v for k,o,v in tree if k=='focus' and first(v,'id')=='COLDWAR_GER_1970_permanent_seat')
        reward = first(focus,'completion_reward')
        self.assertFalse(self.m.condition(first(focus,'available'),g))
        self.m.execute(reward,g,g,None)
        self.assertFalse(self.m.api_calls)
        g.modifiers.add('united_nations_member')
        self.assertTrue(self.m.condition(first(focus,'available'),g))
        self.assertFalse(self.m.condition([('can_campaign_for_permanent_unsc_seat','=','yes')],g))
        g.focuses.add('COLDWAR_GER_1970_permanent_seat')
        self.assertTrue(self.m.condition([('can_campaign_for_permanent_unsc_seat','=','yes')],g))
        self.m.execute(reward,g,g,None)
        self.assertEqual(self.m.api_calls,[('unlock_decision_tooltip','UNSC_lobby_permanent_member'),('unlock_decision_tooltip','UNSC_submit_permanent_seat_application')])
        self.assertFalse(self.m.requests)
        self.assertNotIn('p5_member',g.ideas)
        self.assertFalse(self.m.events)
        g.modifiers.clear()
        self.assertFalse(self.m.condition([('can_campaign_for_permanent_unsc_seat','=','yes')],g))
        g.modifiers.add('united_nations_member');g.ideas.add('p5_member')
        self.assertFalse(self.m.condition([('can_campaign_for_permanent_unsc_seat','=','yes')],g))
        self.m.scenario=False;g.ideas.clear()
        self.assertFalse(self.m.condition([('can_campaign_for_permanent_unsc_seat','=','yes')],g))

    def test_native_lobbying_targets_the_actual_current_veto_holders(self):
        self.m.run('COLDWAR_UN_1970_initialize')
        category = first(load('common/decisions/un_voting_decisions.txt'),'UNSC_permanent_seat_campaign')
        decision = first(category,'UNSC_lobby_permanent_member')
        target_array = first(decision,'target_array')
        obj,key = self.m.variable(target_array,self.m.root,self.m.root,None)
        targets = {c.id for c in obj.vars[key]}
        self.assertIn('TAI',targets);self.assertNotIn('CHI',targets)

    def test_completed_joint_application_displays_actual_separate_memberships_and_mandates(self):
        texts = {first(v,'name'):v for k,o,v in load('common/scripted_localisation/COLDWAR_diplomacy_1970.txt')}
        def selected(name,actor):
            for k,o,v in texts[name]:
                if k=='text' and self.m.condition(first(v,'trigger',[]),actor):
                    return first(v,'localization_key')
            self.fail('Missing fallback '+name)
        pair = 'COLDWAR_Germany_UN_pair_status';g=self.m.c['GER'];d=self.m.c['DDR']
        g.vars['cwgg_vertrag_4']=D(1)
        self.assertEqual(selected(pair,d),'COLDWAR_Germany_UN_neither')
        g.modifiers.add('united_nations_member')
        self.assertEqual(selected(pair,d),'COLDWAR_Germany_UN_GER_only')
        d.modifiers.add('united_nations_member')
        self.assertEqual(selected(pair,g),'COLDWAR_Germany_UN_both')
        g.modifiers.clear()
        self.assertEqual(selected(pair,g),'COLDWAR_Germany_UN_DDR_only')
        self.assertEqual(selected('COLDWAR_DDR_UN_status',g),'COLDWAR_Germany_UN_assembly')
        self.m.g.vars['security_council_members']=[d]
        self.assertEqual(selected('COLDWAR_DDR_UN_status',g),'COLDWAR_Germany_UN_elected')
        self.m.g.vars['security_council_members']=[]
        self.assertEqual(selected('COLDWAR_DDR_UN_status',g),'COLDWAR_Germany_UN_assembly')
        self.m.g.vars['p5_sc_members']=[d]
        self.assertEqual(selected('COLDWAR_DDR_UN_status',g),'COLDWAR_Germany_UN_permanent')
        d.modifiers.clear()
        self.assertEqual(selected('COLDWAR_DDR_UN_status',g),'COLDWAR_Germany_UN_outside')
        for rel,name in [('COLDWAR_GER_1970_windows','RV_Treaty_4'),('COLDWAR_DDR_1970_relations','EGR_Treaty_4')]:
            rows=load('common/scripted_localisation/'+rel+'.txt')
            dt=next(v for k,o,v in rows if first(v,'name')==name)
            self.assertEqual(first(first(dt,'text'),'localization_key'),'COLDWAR_Germany_un_applications_status')

    def test_un_transaction_refresh_is_constant_scope_and_non_1970_inert(self):
        self.m.c['GER'].flags.add('cwgg_initialized')
        self.m.run('COLDWAR_Germany_un_status_changed',self.m.c['TAI'])
        self.assertEqual(self.m.api_calls,['COLDWAR_GER_1970_rv_sync_views'])
        self.m.scenario=False;self.m.api_calls.clear()
        self.m.run('COLDWAR_Germany_un_status_changed')
        self.assertFalse(self.m.api_calls)
        helper=self.m.effects['COLDWAR_Germany_un_status_changed']
        self.assertFalse(any(k in ('every_country','any_country','random_country') for k,o,v in walk(helper)))
        native=load('common/scripted_effects/01_international_systems_effects.txt')
        for key in ('update_security_council_peeps','clear_united_nations_member_state','unsc_promote_permanent_member'):
            self.assertTrue(any(k=='COLDWAR_Germany_un_status_changed' for k,o,v in walk(first(native,key))))
        event=next(v for k,o,v in load('events/International Recognition.txt') if k=='country_event' and first(v,'id')=='recognition.71')
        self.assertTrue(any(k=='COLDWAR_Germany_un_status_changed' for k,o,v in walk(first(event,'option'))))

    def test_un_focus_rewards_stop_if_membership_or_current_council_mandate_is_lost(self):
        g=self.m.c['GER'];g.flags.add('COLDWAR_GER_1970_unity_achieved')
        tree=first(load('common/national_focus/COLDWAR_GER_1970_focus.txt'),'focus_tree')
        for suffix in ('un_city_bonn','european_seat','namibia_contact_group','un_security_council','un_entry'):
            focus=next(v for k,o,v in tree if k=='focus' and first(v,'id')=='COLDWAR_GER_1970_'+suffix)
            self.assertFalse(self.m.condition(first(focus,'available'),g),suffix)
            self.m.execute(first(focus,'completion_reward'),g,g,None)
        self.assertFalse(self.m.events)
        self.assertFalse(self.m.api_calls)
        g.modifiers.add('united_nations_member')
        focus=next(v for k,o,v in tree if k=='focus' and first(v,'id')=='COLDWAR_GER_1970_namibia_contact_group')
        self.assertFalse(self.m.condition(first(focus,'available'),g))
        self.m.g.vars['security_council_members']=[g]
        self.assertTrue(self.m.condition(first(focus,'available'),g))
        self.m.g.vars['security_council_members']=[]
        self.m.execute(first(focus,'completion_reward'),g,g,None)
        self.assertFalse(self.m.api_calls)

    def test_queued_legacy_permanent_seat_acceptances_are_inert(self):
        events={first(v,'id'):v for k,o,v in load('events/COLDWAR_GER_1970_events.txt') if k=='country_event'}
        for base in (400,410,420,430,440):
            for offset in (0,1,2):
                event=events['COLDWAR_GDIP.'+str(base+offset)]
                self.assertEqual(first(event,'hidden'),'yes')
                option=first(event,'option')
                self.assertEqual({k for k,o,v in option},{'name','ai_chance','log'})
        # Stable identifiers preserve every subsequent foreign-policy transaction.
        self.assertEqual(first(events['COLDWAR_GDIP.450'],'title'),'COLDWAR_GDIP.450.t')

    def test_european_proposal_previews_both_parties_without_paying_and_rechecks_membership(self):
        g=self.m.c['GER']
        tree=first(load('common/national_focus/COLDWAR_GER_1970_focus.txt'),'focus_tree')
        focus=next(v for k,o,v in tree if k=='focus' and first(v,'id')=='COLDWAR_GER_1970_european_seat')
        preview=first(first(focus,'completion_reward'),'effect_tooltip')
        before=copy.deepcopy(g.vars)
        self.m.execute([('effect_tooltip','=',preview)],g,g,None)
        self.assertEqual(g.vars,before);self.assertFalse(self.m.events)
        deltas=[v[0] for k,o,v in walk(preview) if k=='add_to_variable']
        self.assertIn(('cwfo_west_europe','=','0.05'),deltas)
        self.assertIn(('cwfo_welt_support','=','0.04'),deltas)
        self.assertIsNotNone(first(first(preview,'FRA'),'add_opinion_modifier'))
        events={first(v,'id'):v for k,o,v in load('events/COLDWAR_GER_1970_events.txt') if k=='country_event'}
        option=[row for row in first(events['COLDWAR_GDIP.451'],'option') if row[0] not in ('name','ai_chance')]
        self.m.execute(option,g,g,None)
        self.assertNotIn('cwdip_euro_seat',g.flags)
        g.modifiers.add('united_nations_member')
        for _ in range(2):self.m.execute(option,g,g,None)
        self.assertEqual(g.vars['cwfo_west_europe'],D('0.05'))
        self.assertEqual(g.vars['cwfo_welt_support'],D('0.04'))
        self.assertIn('cwdip_euro_seat',g.flags)


if __name__ == '__main__':unittest.main(verbosity=2)
