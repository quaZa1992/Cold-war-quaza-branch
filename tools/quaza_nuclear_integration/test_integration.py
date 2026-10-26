# IMPERIA CW — Cold War: uranium arithmetic, conservation and integration checks.
import collections,hashlib,json,re,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Claude outputs/COLDWAR_SOV_generator/tools'))
import pdx
from port import ROOT,SOURCE,AUDIT,read
from adapt import block,blocks
from repair_coverage import gui

class Model:
    """Execute the actual uranium/budget effects against controlled inputs."""
    def __init__(self):
        self.vars={};self.resource=0;self.deposit=True;self.projects=set()
        self.effects={}
        for rel in ['common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt',
                    'common/scripted_effects/COLDWAR_nuclear_development_budget.txt']:
            self.effects.update({k:v for k,op,v,line in pdx.parse(read(ROOT/rel))[0] if isinstance(v,list)})
        self.vars['@imp_uranium_per_enrichment_facility']=25
        self.vars['@math_expressions_max']=100000000
    def value(self,x):
        if isinstance(x,list):
            val=0
            for k,op,v,line in x:
                if k=='value':val=self.value(v)
                elif k=='add':val+=self.value(v)
                elif k=='subtract':val-=self.value(v)
                elif k=='multiply':val*=self.value(v)
                elif k=='divide':val/=self.value(v)
                elif k=='clamp':val=max(self.value(pdx.get(v,'min',-1e30)),min(self.value(pdx.get(v,'max',1e30)),val))
                else:raise AssertionError(k)
            return val
        try:return float(x)
        except (ValueError,TypeError):return self.vars.get(x,0)
    def condition(self,items):
        conditions=[]
        for k,op,v,line in items:
            if k=='check_variable':
                a,cmp,b,_=v[0];a=self.value(a);b=self.value(b)
                conditions.append({'=':a==b,'>':a>b,'<':a<b,'>=':a>=b,'<=':a<=b}[cmp])
            elif k=='NOT':conditions.append(not self.condition(v))
            elif k=='OR':conditions.append(any(self.condition([item]) for item in v))
            elif k=='AND':conditions.append(self.condition(v))
            elif k=='has_dynamic_modifier':conditions.append(self.deposit)
            elif k=='has_variable':conditions.append(v in self.vars)
            elif k=='is_special_project_being_researched':conditions.append(v in self.projects)
            else:raise AssertionError(k)
        return all(conditions)
    def run(self,items):
        chain=False
        for k,op,v,line in items:
            if k in ['if','else_if','else']:
                if k=='if':chain=False
                if not chain and (k=='else' or self.condition(pdx.get(v,'limit'))):
                    chain=True;self.run([item for item in v if item[0]!='limit'])
            elif k in ['set_variable','set_temp_variable','multiply_variable','add_to_variable','add_to_temp_variable','subtract_from_variable']:
                name,_,amount,_=v[0];amount=self.value(amount)
                if k.startswith('set_'):self.vars[name]=amount
                elif k=='multiply_variable':self.vars[name]=self.value(name)*amount
                elif k in ['add_to_variable','add_to_temp_variable']:self.vars[name]=self.value(name)+amount
                else:self.vars[name]=self.value(name)-amount
            elif k=='round_variable':self.vars[v]=round(self.value(v))
            elif k=='add_resource':self.resource+=self.value(pdx.get(v,'amount'))
            elif k in self.effects:self.run(self.effects[k])
            else:raise AssertionError(k)
    def call(self,name):self.run(self.effects[name])

class Integration(unittest.TestCase):
    def test_development_budget_rates_and_lifecycle(self):
        # Match the engine's five-place fixed-point precision when converting the source budgets.
        bomb=int(8/52*100000)/100000;warhead=int(5/52*100000)/100000
        helper=read(ROOT/'common/scripted_effects/COLDWAR_nuclear_development_budget.txt')
        self.assertNotRegex(helper,r'\b\d+\.\d{6,}\b')
        for projects,weekly in [(set(),0),({'sp:sp_nuclear_bomb'},bomb),
                                ({'sp:sp_nuclear_warhead_program'},warhead),
                                ({'sp:sp_nuclear_bomb','sp:sp_nuclear_warhead_program'},bomb+warhead)]:
            for gdpc,multiplier in [(0,0.4),(9,0.4),(36,1),(72,1.2)]:
                for inflation in [1,1.35]:
                    with self.subTest(projects=projects,gdpc=gdpc,inflation=inflation):
                        m=Model();m.projects=projects
                        m.vars.update(gdp_per_capita=gdpc,inflation_multiplier=inflation)
                        for _ in range(5):
                            m.call('COLDWAR_calculate_nuclear_development_budget')
                            self.assertAlmostEqual(m.vars['COLDWAR_nuclear_development_weekly_cost'],weekly*multiplier*inflation)
                        m.projects=set();m.call('COLDWAR_calculate_nuclear_development_budget')
                        self.assertEqual(m.vars['COLDWAR_nuclear_development_weekly_cost'],0)
    def test_development_budget_enters_native_treasury_once(self):
        s=read(ROOT/'common/scripted_effects/00_money_system.txt');n=block(s,'update_military_rate')
        body=pdx.parse(s[n['open']:n['close']])[0]
        tail=body[-2:]
        self.assertEqual(tail[0][:3],('COLDWAR_calculate_nuclear_development_budget','=','yes'))
        self.assertEqual(s[n['start']:n['end']].count('add = COLDWAR_nuclear_development_weekly_cost'),1)
        m=Model();m.vars.update(gdp_per_capita=36,inflation_multiplier=1,
                              defence_breakdown_cyber=0.1,**{'array_defence_spend^def_index':1})
        m.projects={'sp:sp_nuclear_bomb'}
        for _ in range(5):m.run(tail);self.assertAlmostEqual(m.vars['defence_gain'],1.1+0.15384)
        n=block(s,'update_display');display=pdx.parse(s[n['open']:n['close']])[0]
        # Execute the production aggregation and net-income statements, omitting unrelated debt/UI logic.
        selected=[item for item in display if item[0]=='set_variable' and item[2][0][0] in ['display_expense','display_income','treasury_rate']]
        self.assertEqual(len(selected),3)
        m.vars.update(tax_gain=2,infra_gain=0.022)
        m.run(selected);self.assertAlmostEqual(m.vars['treasury_rate'],2-1.1-0.15384-0.022)
        m.projects=set();m.run(tail);m.run(selected)
        self.assertAlmostEqual(m.vars['treasury_rate'],2-1.1-0.022)
        hooks=read(ROOT/'common/on_actions/MD_on_actions.txt')
        n=block(hooks,'on_weekly');weekly=hooks[n['start']:n['end']]
        self.assertEqual(weekly.count('add_to_variable = { treasury = treasury_rate_gain }'),1)
        helper=read(ROOT/'common/scripted_effects/COLDWAR_nuclear_development_budget.txt')
        self.assertNotIn('modify_treasury_effect',helper)
        self.assertNotIn('treasury =',helper)
    def test_mine_cost_and_maintenance_chain(self):
        s=read(ROOT/'common/buildings/00_buildings.txt');n=block(s,'uranium_mine')
        mine=pdx.parse(s[n['open']:n['close']])[0]
        self.assertEqual(pdx.get(mine,'base_cost'),'32000')
        self.assertEqual(pdx.get(mine,'per_level_extra_cost'),'4000')
        s=read(ROOT/'common/scripted_effects/00_money_system.txt');n=block(s,'update_infra_rate')
        body=pdx.parse(s[n['open']:n['close']])[0]
        costs=[item for item in body if item[0]=='set_variable' and item[2][0][0] in ['uranium_mine_infra_expense','infra_gain']]
        self.assertEqual(len(costs),2)
        m=Model();m.vars.update(uranium_mine_total=3,common_money_modifier=1.2,infra_size_scaling=0.8)
        # GDP/size factors are taken directly from the production expression.
        n=block(s,'uranium_mine_infra_expense');part=s[n['start']:n['end']]
        self.assertIn('multiply = 0.022',part)
        m.run(costs)
        self.assertEqual(m.vars['infra_gain'],m.vars['uranium_mine_infra_expense'])
        self.assertAlmostEqual(m.vars['uranium_mine_infra_expense'],3*0.022*1.2*0.8)
    def test_uranium_weekly_work_is_bounded_and_enrichment_is_gated(self):
        hooks=read(ROOT/'common/on_actions/COLDWAR_quaza_zzzzzz_imp_uranium_on_actions.txt')
        self.assertNotIn('on_daily',hooks);self.assertNotIn('on_hourly',hooks)
        s=read(ROOT/'common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt');n=block(s,'imp_uranium_update_mines')
        part=s[n['start']:n['end']]
        self.assertEqual(part.count('every_owned_state'),1)
        self.assertNotIn('every_collection',part)
        self.assertNotIn('uranium_mine_output_total',s)
        self.assertIn('has_country_flag = COLDWAR_uranium_has_mining_district',part)
        s=read(ROOT/'common/on_actions/COLDWAR_quaza_zzzzzz_imp_nuclear_programme_on_actions.txt')
        n=block(s,'on_weekly');body=pdx.parse(s[n['open']:n['close']])[0]
        effect=pdx.get(body,'effect');self.assertEqual(len(effect),1)
        gate=effect[0];self.assertEqual(gate[0],'if')
        conditions=pdx.get(pdx.get(gate[2],'limit'),'OR')
        self.assertEqual({item[2] for item in conditions if item[0]=='is_special_project_being_researched'},
                         {'sp:sp_nuclear_bomb','sp:sp_nuclear_warhead_program'})
        self.assertTrue(any(item[0]=='has_dynamic_modifier' for item in conditions))
        self.assertIn(('COLDWAR_refresh_enrichment_count','=','yes'),[item[:3] for item in gate[2]])
    def test_enrichment_shortages_execute_actual_effect(self):
        for net,expected in [(-75,0),(-50,0),(-25,175),(0,350),(20,350)]:
            with self.subTest(net=net):
                m=Model();m.vars.update(total_enrichment_facilities=2,total_nuclear_reactor_fuel_production=350)
                m.vars['resource@uranium']=net;m.call('imp_uranium_enrichment_supply')
                self.assertEqual(m.vars['total_nuclear_reactor_fuel_production'],expected)
    def test_mine_conservation_damage_repair_loss_and_rebalance(self):
        m=Model();m.vars.update(imp_uranium_per_level=6,imp_uranium_mine_slots=2,imp_uranium_levels_applied=0)
        for working,expected in [(2,12),(2,12),(1,6),(0,0),(2,12)]:
            m.vars['non_damaged_building_level@uranium_mine']=working
            m.call('imp_uranium_count_mine_levels');m.call('imp_uranium_sync_mine_output')
            self.assertEqual(m.resource,expected)
        m.deposit=False;m.call('imp_uranium_sync_mine_output');self.assertEqual(m.resource,0)
        m.deposit=True;m.call('imp_uranium_sync_mine_output');self.assertEqual(m.resource,12)
        m.vars['imp_uranium_per_level']=9;m.call('imp_uranium_sync_mine_output');self.assertEqual(m.resource,18)
        for _ in range(30):m.call('imp_uranium_sync_mine_output')
        self.assertEqual(m.resource,18)
    def test_all_raids_block_ai_at_prepare_and_launch(self):
        count=0
        for p in (ROOT/'common/raids').glob('*.txt'):
            s=read(p)
            for root in blocks(s):
                if root['name']!='types':continue
                for raid in root['children']:
                    count+=1
                    self.assertNotIn('can_launch',[n['name'] for n in raid['children']],p.name)
                    for name in ['available','launchable']:
                        nodes=[n for n in raid['children'] if n['name']==name]
                        self.assertEqual(len(nodes),1,(p.name,raid['name'],name))
                        content=pdx.parse(s[nodes[0]['open']:nodes[0]['close']])[0]
                        self.assertEqual(content[0][:3],('is_ai','=','no'),(p.name,raid['name'],name))
        self.assertEqual(count,50)
    def test_no_duplicate_buildings_or_projects(self):
        for directory,container in [('common/buildings','buildings'),('common/special_projects/projects',None)]:
            ids=[]
            for p in (ROOT/directory).glob('*.txt'):
                nodes=blocks(read(p))
                if container:nodes=[x for n in nodes if n['name']==container for x in n['children']]
                ids.extend(n['name'] for n in nodes if n['name'])
            duplicate=[k for k,v in collections.Counter(ids).items() if v>1]
            self.assertFalse(duplicate,duplicate)
    def test_correct_torpedo_and_warhead_costs(self):
        s=read(ROOT/'common/special_projects/projects/naval_projects.txt')
        for name in ['sp_medium_naval_nuclear_engines','sp_nuclear_torpedoes']:
            n=block(s,name);self.assertIn('uranium',s[n['start']:n['end']])
        n=block(s,'sp_anti_torpedo_module');self.assertNotIn('uranium',s[n['start']:n['end']])
        s=read(ROOT/'common/special_projects/projects/nuclear_projects.txt')
        for name in ['sp_nuclear_bomb','sp_nuclear_warhead_program']:
            n=block(s,name);part=s[n['start']:n['end']]
            self.assertIn('undamaged_enrichment_facilities > 2',part)
            self.assertIn('uranium',part)
            self.assertEqual(sum(x['name']=='resource_cost' for x in n['children']),1)
    def test_encoding_and_braces_in_changed_runtime_files(self):
        paths={ROOT/p.relative_to(AUDIT/'before') for p in (AUDIT/'before').rglob('*') if p.is_file()}
        paths.update(ROOT/p.relative_to(AUDIT/'performance_before') for p in (AUDIT/'performance_before').rglob('*') if p.is_file())
        paths.update(ROOT/p.relative_to(AUDIT/'coverage_before') for p in (AUDIT/'coverage_before').rglob('*') if p.is_file())
        paths.update(ROOT/p.relative_to(AUDIT/'geology_before') for p in (AUDIT/'geology_before').rglob('*') if p.is_file())
        paths.update(p for d in ['common','interface','localisation/english'] for p in (ROOT/d).rglob('COLDWAR_quaza_*') if p.is_file())
        paths.add(ROOT/'common/scripted_effects/COLDWAR_nuclear_development_budget.txt')
        paths.add(ROOT/'interface/COLDWAR_nuclear_project_icons.gfx')
        for p in paths:
            if p.suffix not in ['.txt','.gui','.gfx','.yml']:continue
            data=p.read_bytes();self.assertTrue(data)
            if p.suffix=='.yml':self.assertTrue(data.startswith(b'\xef\xbb\xbf'),p)
            else:
                self.assertFalse(data.startswith(b'\xef\xbb\xbf'),p)
                blocks(data.decode('utf-8'))
            self.assertNotRegex(data.decode('utf-8-sig'),r'(?m)^(<<<<<<<|=======|>>>>>>>)')
    def test_icon_frames_keep_shelter_and_add_uranium(self):
        from PIL import Image,ImageChops
        for name in ['building_icon_strip.dds','building_icon_without_bg_strip.dds']:
            rel='gfx/interface/buildings/'+name
            original=Image.open(AUDIT/'before'/rel).convert('RGBA');current=Image.open(ROOT/rel).convert('RGBA')
            self.assertEqual(current.size,(1840,46));self.assertIsNone(ImageChops.difference(original,current.crop((0,0,1794,46))).getbbox())
        s=read(ROOT/'common/buildings/mdcw_imperia_shelters.txt');self.assertIn('icon_frame = 39',s)
        s=read(ROOT/'common/buildings/00_buildings.txt')
        n=block(s,'uranium_mine');self.assertIn('icon_frame = 40',s[n['start']:n['end']])
    def test_investment_progress_has_one_delivery_branch(self):
        s=read(ROOT/'common/scripted_effects/99_investment_scripted_effects.txt');n=block(s,'add_finished_buildings');part=s[n['start']:n['end']]
        self.assertEqual(part.count('type = industrial_complex level = 1'),1)
        self.assertEqual(part.count('type = uranium_mine level = 1'),1)
        self.assertEqual(part.count('ROOT.project_monetary_cost^ROOT.project = var_cost'),1)
        self.assertIn('mdcw_imp_segment_reward',part)
    def test_existing_investment_prices_preserved(self):
        rel='common/scripted_effects/99_investment_scripted_effects.txt'
        old=read(AUDIT/'before'/rel);now=read(ROOT/rel)
        a=block(old,'init_investment_system');b=block(now,'init_investment_system')
        for assignment in re.findall(r'set_variable\s*=\s*\{\s*([^{}]+?)\s*\}',old[a['start']:a['end']]):
            self.assertIn(assignment,now[b['start']:b['end']])
    def test_uranium_investment_icon_and_grid(self):
        s=read(ROOT/'interface/MD_investments.gui')
        mine=re.search(r'name = "select_uranium_mine_button"(.*?)position',s,re.S)
        self.assertIsNotNone(mine);self.assertIn('frame = 40',mine[1])
        self.assertIn('name = "uranium_mine"\n                position = { x = 224 y = 42 }',s)
        self.assertIn('name = "mil"\n                position = { x = 32 y = 3 }',s)
    def test_all_starting_uranium_requires_development(self):
        for p in (ROOT/'history/states').glob('*.txt'):
            s=read(p)
            self.assertFalse(re.search(r'\buranium\s*=\s*[1-9]\d*',s),p.name)
            self.assertFalse(re.search(r'\buranium_mine\s*=\s*[1-9]\d*',s),p.name)
        s=read(ROOT/'common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt')
        n=block(s,'COLDWAR_uranium_setup_1970_deposits');part=s[n['start']:n['end']]
        register=json.loads(read(AUDIT/'uranium_1970_research.json'))
        self.assertEqual(len(re.findall(r'imp_uranium_add_deposit = yes',part)),len(register['deposits']))
        self.assertNotIn('add_resource',part)
        self.assertNotIn('add_building_construction',part)
    def test_1970_geological_register_and_generated_capacities(self):
        register=json.loads(read(AUDIT/'uranium_1970_research.json'))
        balance=json.loads(read(AUDIT/'coldwar_balance.json'))
        self.assertEqual(register['knowledge_cutoff'],'1970-01-01')
        s=read(ROOT/'common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt')
        n=block(s,'COLDWAR_uranium_setup_1970_deposits');part=s[n['open']:n['close']]
        parsed=pdx.parse(part)[0]
        states={int(k):v for k,op,v,line in parsed}
        expected={row['state_id']:row for row in register['deposits']}
        self.assertEqual(set(states),set(expected))
        self.assertEqual(len(expected),len(register['deposits']))
        self.assertNotIn(785,states) # Crow Butte was discovered in 1980.
        self.assertIn(714,states) # Aksu-Stepnogorsk belongs to the northern state on this map.
        self.assertNotIn(716,states) # Do not duplicate the moved northern Kazakh capacity.
        self.assertTrue({745,884,747,756,717}.issubset(states))
        self.assertNotIn('imp_uranium_deposit_kt',part)
        state_ids={int(re.match(r'\d+',p.name)[0]) for p in (ROOT/'history/states').glob('*.txt')}
        for state,row in expected.items():
            self.assertIn(state,state_ids)
            self.assertLessEqual(row['known_by_year'],1969)
            self.assertTrue(row['districts'])
            self.assertTrue(row['sources'])
            self.assertTrue(all(url.startswith('https://') for url in row['sources']))
            self.assertIn(row['slots'],[1,2,3])
            self.assertIn(row['output_per_level'],[3,4,6,9,12])
            assignments={v[0][0]:int(v[0][2]) for k,op,v,line in states[state] if k=='set_variable'}
            self.assertEqual(assignments,{'imp_uranium_mine_slots':row['slots'],'imp_uranium_per_level':row['output_per_level']})
            self.assertEqual(balance['deposits'][str(state)],{'mine_slots':row['slots'],'output_per_level':row['output_per_level']})
        self.assertEqual(balance['starting_resources'],{})
        self.assertEqual(expected[717]['slots'],1) # Only the early southern Kazakh prospects.
        self.assertEqual(expected[756]['output_per_level'],6) # No later giant Athabasca discoveries.
    def test_uranium_map_reports_capacity_without_unsupported_tonnage(self):
        s=read(ROOT/'common/map_modes/COLDWAR_quaza_imp_uranium_map_mode.txt')
        self.assertNotIn('imp_uranium_deposit_kt',s)
        self.assertEqual(len(re.findall('check_variable = { imp_uranium_per_level',s)),4)
        self.assertIn('update_daily = no',s)
        loc=read(ROOT/'localisation/english/COLDWAR_quaza_imp_uranium_l_english.yml')
        tooltip=next(line for line in loc.splitlines() if line.lstrip().startswith('imp_uranium_deposit_map_mode_tooltip_delayed:'))
        self.assertNotIn('deposit_kt',tooltip)
        self.assertIn('imp_uranium_mine_slots',tooltip)
        self.assertIn('imp_uranium_per_level',tooltip)
        self.assertIn('imp_uranium_mine_levels',tooltip)
    def test_special_project_card_rows_and_native_bomb_art(self):
        s=read(ROOT/'interface/special_projects/facility.gui')
        n=gui(s,'projects_entry');card=s[n['open']:n['close']]
        def fields(name):
            node=gui(card,name)
            return pdx.parse(card[node['open']:node['close']])[0]
        def position(name):
            p=pdx.get(fields(name),'position')
            return int(pdx.get(p,'x')),int(pdx.get(p,'y'))
        rows=['project_name','project_name_default','project_type','project_time','scientist_info']
        bounds=[]
        cost_x=position('breakthrough_cost_tab')[0]
        for name in rows:
            f=fields(name);x,y=position(name)
            bounds.append((y,y+int(pdx.get(f,'maxHeight'))))
            self.assertEqual(x,225)
            self.assertLessEqual(x+int(pdx.get(f,'maxWidth')),cost_x)
        for prev,nxt in zip(bounds,bounds[1:]):self.assertLessEqual(prev[1],nxt[0])
        speed_x,speed_y=position('research_speed_window')
        self.assertLessEqual(225+int(pdx.get(fields('project_name'),'maxWidth')),speed_x)
        self.assertLessEqual(speed_y+25*float(pdx.get(fields('research_speed_icon'),'scale')),bounds[1][0])
        self.assertLessEqual(speed_x+30+40,511)
        projects=read(ROOT/'common/special_projects/projects/nuclear_projects.txt')
        n=block(projects,'sp_nuclear_bomb')
        name=pdx.get(pdx.parse(projects[n['open']:n['close']])[0],'icon')
        self.assertEqual(name,'GFX_COLDWAR_sp_nuclear_bomb')
        gfx=read(ROOT/'interface/COLDWAR_nuclear_project_icons.gfx')
        self.assertEqual(gfx.count('name = "'+name+'"'),1)
        art=re.search(r'texturefile\s*=\s*"([^"]+)"',gfx)[1]
        from PIL import Image
        native=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')/art
        self.assertTrue(native.is_file(),art)
        with Image.open(native) as image:self.assertEqual(image.size,(161,98))
    def test_donor_uranium_layout_geometry_is_complete(self):
        def body(s,name):
            n=gui(s,name);return s[n['open']:n['close']]
        def geometry(s,name,keys):
            p=pdx.parse(body(s,name))[0]
            def canonical(v):
                return [(k,op,canonical(x)) for k,op,x,line in v] if isinstance(v,list) else v
            return {k:canonical(pdx.get(p,k)) for k in keys}
        rel='interface/countrytradeview.gui';a=read(ROOT/rel);b=read(SOURCE/rel)
        self.assertEqual(geometry(body(a,'resources'),'resources_grid',['size','slotsize','max_slots']),
                         geometry(body(b,'resources'),'resources_grid',['size','slotsize','max_slots']))
        for name,keys in [('background',['scale']),('icon',['position'])]:
            self.assertEqual(geometry(body(a,'resources_filter_entry'),name,keys),
                             geometry(body(b,'resources_filter_entry'),name,keys))
        rel='interface/countryproductionlineview.gui';a=body(read(ROOT/rel),'resource_strip_item');b=body(read(SOURCE/rel),'resource_strip_item')
        for name,keys in [('icon',['position']),('value',['position','maxWidth'])]:
            self.assertEqual(geometry(a,name,keys),geometry(b,name,keys))
        self.assertEqual(pdx.get(pdx.get(pdx.parse(a)[0],'size'),'width'),'57')
        self.assertNotIn('resource_item_background',a)
        rel='interface/MD_countryeconomyview.gui';a=body(read(ROOT/rel),'MD_tradeview_market_prices');b=body(read(SOURCE/rel),'MD_tradeview_market_prices')
        for name in ['fossil_fuels','light_metals','rubber','technology_metals','steel','precious_metals','microchips','advanced_composities','uranium']:
            self.assertEqual(geometry(a,name,['position']),geometry(b,name,['position']),name)
        rel='interface/countrystateview.gui';a=read(ROOT/rel);b=read(SOURCE/rel)
        for name,keys in [('countrystateview',['position','show_position','size']),('state_building_bg',['size']),
                          ('shared_slot_building_bg',['position']),('state_shared_slot_building_entries',['position']),
                          ('state_resources',['position']),('province_info_window',['position'])]:
            self.assertEqual(geometry(a,name,keys),geometry(b,name,keys),name)
    def test_core_donor_effect_and_trigger_definitions_are_present(self):
        for rel in ['common/scripted_effects/imp_uranium_effects.txt','common/scripted_effects/imp_nuclear_ai_effects.txt',
                    'common/scripted_triggers/imp_nuclear_ai_triggers.txt','common/scripted_triggers/imp_raid_triggers.txt']:
            source=pdx.parse(read(SOURCE/rel))[0]
            p=ROOT/Path(rel).parent/('COLDWAR_quaza_'+Path(rel).name)
            installed={k for k,op,v,line in pdx.parse(read(p))[0] if isinstance(v,list)}
            expected={k for k,op,v,line in source if isinstance(v,list)}
            self.assertTrue(expected.issubset(installed),(rel,expected-installed))
    def test_uranium_assets_resolve_to_the_donor_art(self):
        import hashlib
        from PIL import Image
        for rel in ['gfx/interface/resources_strip.dds','gfx/interface/missing_resources_strip.dds',
                    'gfx/interface/tradeview/trade_resources_bg.dds',
                    'gfx/interface/state_modifiers/imp_uranium_deposit.dds',
                    'gfx/interface/mapmode/md_map_modes/imp_uranium_deposit_map_mode_deselected.dds',
                    'gfx/interface/mapmode/md_map_modes/imp_uranium_deposit_map_mode_selected.dds',
                    'gfx/interface/topbar/dynamic_topbar/topbar_uranium.dds',
                    'gfx/interface/military_raids/map_icons/raid_enrichment_facility_strike.dds']:
            self.assertEqual(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),hashlib.sha256((SOURCE/rel).read_bytes()).hexdigest(),rel)
        strip=Image.open(ROOT/'gfx/interface/resources_strip.dds')
        self.assertEqual(strip.size,(243,27))
        self.assertIsNotNone(strip.convert('RGBA').crop((216,0,243,27)).getbbox())

if __name__=='__main__':unittest.main(verbosity=2)
