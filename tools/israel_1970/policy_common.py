"""Compiler support for the approved 1970 policy expansion.

Focus metadata belongs to the ordinary compiler. Decisions, timers and local
status effects are emitted separately so rebuilding cannot silently drop them.
"""
from pathlib import Path
import copy,json,re

PREFIX='ISR70_policy_'
FOCUS_ALIASES={'citizen_review':'arab_citizens','equal_services':'equal_local_services','municipal_self':'local_autonomy'}
SINAI=213
CANAL=214

def focus_id(key): return 'ISR70_'+FOCUS_ALIASES.get(key,key)
def ident(key): return key if key.startswith(PREFIX) else PREFIX+key
def flag(key): return 'set_country_flag = '+ident(key)
def has(key): return 'has_country_flag = '+ident(key)
def scope(state,code): return str(state)+' = {\n'+code+'\n}'

class PolicyCompiler:
    def __init__(self,data,root,art):
        self.data,self.root,self.art=data,root,art
        self.design=json.loads((Path(__file__).parent/'policy_design.json').read_text(encoding='utf-8'))
        self.effects={};self.triggers={};self.dynamic={};self.events=[];self.decisions=[];self.localisation={}
        self.tick=[];self.costs=set();self.focus_specs={};self.projects=[]
        self.opinions={}
        self.nodes={n['id']:n for n in data['nodes']}
        self._add_nodes()

    def _add_nodes(self):
        labels={'citizens':'Citizenship and Municipal Development','settlements':'Settlement Projects and Palestinian Relations',
                'finance':'Development Finance and Office Networks','greater':'Greater Israel: Sinai Development and Integration',
                'occupation':'Civil Rights and Occupation Status','radicals':'Radical Territorial Programmes'}
        roots={'citizens':'social_contract','settlements':'territory_administration','finance':'diaspora_bonds',
               'greater':'territorial_maximalism','occupation':'gi_frontier_review'}
        old_nodes=copy.deepcopy(self.nodes)
        def add(raw,branch,parents,xy):
            fid=focus_id(raw['id']);art=old_nodes['ISR70_'+raw['art']]
            n=copy.deepcopy(old_nodes.get(fid,old_nodes['ISR70_january_1970']))
            n.update(id=fid,group='policy_'+branch['id'],label=raw['name'],prerequisites=parents,
                mutually_exclusive=[],days=raw['days'],modifiers={},reward='',available='',duration_days=None,
                description='A specific programme of '+raw['name'].lower()+'. Its costs and actual conditions are shown in the completion effects.',
                note='',icon=art['icon'],art_source=art['art_source'],policy_extension=True,
                policy_key=raw['id'],policy_local_xy=xy,reward_revision=3,policy_summary=[])
            if raw.get('choice_group'):n['choice_group']=raw['choice_group']
            self.art[n['icon']]=n['art_source']
            self.nodes[fid]=n
            self.data['nodes']=[v for v in self.data['nodes'] if v['id']!=fid]+[n]
            return n
        for b in self.design['branches']:
            self.data['groups'].append(dict(id='policy_'+b['id'],label=labels[b['id']],description=labels[b['id']]+'. Each policy retains its own conditions and consequences.',outlook=None,party=None,trigger=None,history='Approved alternative-history policy expansion.'))
            previous=[]
            for i,raw in enumerate(b['common']):
                parents=[[focus_id(previous[-1])]] if previous else ([[focus_id(roots[b['id']])]] if b['id'] in roots else [])
                add(raw,b,parents,[0,i]);previous.append(raw['id'])
            for lane,path in enumerate(b['paths']):
                x=(lane-(len(b['paths'])-1)/2)*8
                stages=[]
                for raw in path['nodes']:
                    if raw.get('choice_group') and stages and stages[-1][0].get('choice_group')==raw['choice_group']:stages[-1].append(raw)
                    else:stages.append([raw])
                parents=[[focus_id(previous[-1])]]
                for index,stage in enumerate(stages):
                    for option,raw in enumerate(stage):
                        n=add(raw,b,parents,[int(x+(option-(len(stage)-1)/2)*4),len(b['common'])+1+index])
                        if len(stage)>1:n['mutually_exclusive']=[focus_id(other['id']) for other in stage if other!=raw]
                    parents=[[focus_id(raw['id']) for raw in stage]]
            # Legal regimes are exclusive at runtime but explicitly reversible.
            # Permanent focus exclusions would deadlock the promised reform.
            if b['id']=='occupation':
                for key in ('gi_equal_status','occ_special_status'):self.nodes[focus_id(key)]['policy_mutable_choice']=True
            if b['id']=='citizens':self._exclude('equal_services','preferential_allocations')
            if b['id'] in ('settlements','finance'):
                first=[p['nodes'][0]['id'] for p in b['paths']]
                for a in first:
                    for c in first:
                        if a!=c:self._exclude(a,c)
        self.data['policy_expansion']={'revision':5,'target_state':SINAI,'canal_state':CANAL,'focuses':77,'focus_aliases':FOCUS_ALIASES}
        self.tick.append('if = { limit = { NOT = { has_country_flag = ISR70_policy_migrated } } remove_ideas = ISR70_equal_local_services_idea remove_ideas = ISR70_local_autonomy_idea set_country_flag = ISR70_policy_migrated }')

    def _exclude(self,a,b):
        a,b=focus_id(a),focus_id(b)
        for left,right in ((a,b),(b,a)):
            if right not in self.nodes[left]['mutually_exclusive']:self.nodes[left]['mutually_exclusive'].append(right)

    def loc(self,key,text):
        assert key not in self.localisation or self.localisation[key]==text,('duplicate policy localisation',key)
        self.localisation[key]=text
        return key
    def flag_label(self,full):
        short=full.removeprefix(PREFIX)
        known={'equal_civil':'Equal civil rights are in force in Sinai.',
            'occupation_special':'The general unequal occupation statute is active.',
            'kach_special':'The radical unequal occupation statute is active.',
            'greater_mandate':'A paid permanent-territory mandate is active.',
            'target_208':'The West Bank is the selected project area.',
            'target_209':'Gaza is the selected project area.',
            'property_claims_fulfilled':'Agreed property, restitution and return obligations have been fulfilled.',
            'property_claims_agreed':'The claimants have accepted the proposed property settlement.',
            'local_status_accepted':'The separate local status process has accepted integration.',
            'egypt_status_accepted':'Egypt has accepted the sovereignty agreement.',
            'active_expulsion':'A forced-displacement policy is active.',
            'expulsion_damage':'Outstanding consequences of forced displacement remain.',
            'council_agreed':'Local representatives have accepted a limited administrative contract.',
            'delegated_agreed':'Local representatives have accepted the delegated administration.',
            'status_chosen':'An initial legal status has already been chosen.',
            'reform_equal_authorized':'The paid reform authorizes the equal-rights focus.',
            'reform_special_authorized':'The paid reform authorizes the unequal-statute focus.'}
        if short in known:return known[short]
        if short.startswith('project_') and short.endswith('_done'):
            project=short[len('project_'):-len('_done')]
            for suffix in ('_208','_209'):project=project.removesuffix(suffix)
            node=self.nodes.get(focus_id(project))
            if node:return 'The funded project "'+node['label']+'" has actually been delivered.'
        return short.replace('_',' ').capitalize()+'.'
    def readable(self,code):
        def replace(match):
            full=match[1];tip=full+'_condition_tt';self.loc(tip,self.flag_label(full))
            return 'custom_trigger_tooltip = { tooltip = '+tip+' has_country_flag = '+full+' }'
        return re.sub(r'\bhas_country_flag\s*=\s*(ISR70_policy_\w+)\b',replace,code)
    def effect(self,name,code):
        key=ident(name);assert key not in self.effects,key;self.effects[key]=code;return key
    def trigger(self,name,code):
        key=ident(name);assert key not in self.triggers,key;self.triggers[key]=code;return key
    def idea(self,name,label,description,mods,duration=None):
        key=ident(name)
        self.data['idea_definitions'][key.removeprefix('ISR70_')]={'label':label,'treatment':description,'modifiers':mods,'picture':'ISR70_spirit_generic_union_agreement'}
        return key
    def state_modifier(self,name,label,description,mods,enable='always = yes'):
        key=ident(name);assert key not in self.dynamic,key
        self.dynamic[key]=(mods,enable);self.loc(key,label);self.loc(key+'_desc',description)
        return key
    def opinion(self,name,value,target,days=1825):
        key=ident(name);self.opinions[key]=(value,days);self.loc(key,name.replace('_',' ').title())
        return f'add_opinion_modifier = {{ target = {target} modifier = {key} }}'
    def money(self,share):
        share=float(share);self.costs.add(share)
        return f'{PREFIX}pay_{self.cost_token(share)} = yes'
    @staticmethod
    def cost_token(share):return f'{share:.4f}'.replace('.','_')
    @staticmethod
    def pay_pp(amount):return f'add_political_power = {-amount:g}'
    def _gates(self,code):
        gates=[]
        for token in sorted(set(re.findall(PREFIX+r'pay_(\d+_\d+) = yes',code))):gates.append(PREFIX+'afford_'+token+' = yes')
        amounts=[float(x) for x in re.findall(r'add_political_power = -([\d.]+)',code)]
        if amounts:gates.append(f'political_power > {sum(amounts)-1:g}')
        return '\n'.join(gates)
    def focus(self,key,code,available='',description='',summary=None):
        n=self.nodes[focus_id(key)]
        helper=self.effect('complete_'+key,code or 'custom_effect_tooltip = ISR70_policy_project_unlock_tt')
        n['reward']=helper+' = yes'
        n['available']='\n'.join(x for x in (available,self._gates(code)) if x)
        if description:n['description']=description;n['note']=description
        n['policy_summary']=summary if isinstance(summary,list) else [summary or description or 'Opens the specified policy programme; costs and actual consequences are shown in its completion tooltip.']
        n['policy_effect']=helper
        self.focus_specs[key]=n
        return helper
    def event(self,number,title,description,options,trigger='ISR70_is_scenario = yes',**extra):
        key='ISR70P.'+str(number);self.loc(key+'.t',title);self.loc(key+'.d',description)
        parts=['country_event = {',f'id = {key}',f'title = {key}.t',f'desc = {key}.d','picture = GFX_israeli_government_event','is_triggered_only = yes','trigger = { '+trigger+' }']
        if extra.get('hidden'):
            assert len(options)==1 and not options[0][2],('Hidden callback must have exactly one unconditional action',key)
            parts+=['hidden = yes','immediate = {',options[0][1],'}','}']
            self.events.append('\n'.join(parts));return key
        for i,(label,code,gate,weight) in enumerate(options):
            opt=key+'.'+chr(97+i);self.loc(opt,label)
            gates='\n'.join(x for x in (gate,self._gates(code)) if x)
            parts+=['option = {','name = '+opt,'ai_chance = { base = '+str(weight)+' }']
            if gates:parts+=['trigger = { '+self.readable(gates)+' }']
            parts += [code,'}']
        parts+=['}'];self.events.append('\n'.join(parts));return key
    def decision(self,key,label,description,unlock,available,code,cost=0,days=0,repeatable=False,**extra):
        did=ident('decision_'+key);self.loc(did,label);self.loc(did+'_desc',description)
        visible='ISR70_is_scenario = yes'
        if unlock:visible+='\nhas_completed_focus = '+focus_id(unlock)
        done=ident(key+'_done')
        if not repeatable:visible+='\nNOT = { has_country_flag = '+done+' }'
        gate='\n'.join(x for x in (available,self._gates(code)) if x)
        reward=code+('' if repeatable else '\nset_country_flag = '+done)
        # Non-project decisions complete immediately; projects have a dedicated
        # reservation and completion event, never days_remove budget races.
        assert not days,('Use project for delayed delivery',key)
        body=f'{did} = {{\nicon = generic_political_actions\ncost = {cost}\nvisible = {{ {visible} }}\navailable = {{ {self.readable(gate)} }}\ncomplete_effect = {{ {reward} }}\ndays_re_enable = {extra.get("cooldown",90)}\nai_will_do = {{ factor = {extra.get("ai",1)} }}\n}}'
        self.decisions.append(body);return did

    def project(self,key,target,buildings,share,days,mods=None,after='',available='',political_cost=0,unlock=None,**extra):
        """Reserve once, deliver after real days, recheck and refund exactly."""
        unlock=unlock or key;self.costs.add(float(share));token=self.cost_token(share)
        done=ident('project_'+key+'_done');active=ident('project_'+key+'_active');paid=ident('project_'+key+'_paid')
        did=ident('project_'+key);effect=ident('start_'+key)
        targets=[int(t) for t in (target if isinstance(target,list) else [target])]
        guards=[f'{t} = {{ is_controlled_by = ISR }}' for t in targets]+[available]
        guards += [f'{t} = {{ is_owned_by = ISR }}' for t in targets if t in (204,205,206,207)]
        staff={'industrial_complex':'can_staff_an_industrial_complex','arms_factory':'can_staff_an_arms_industry','offices':'can_staff_an_offices','agriculture_district':'can_staff_an_agriculture_district','dockyard':'can_staff_an_dockyard'}
        commands={t:[] for t in targets}
        for b in buildings:
            target=int(b.get('state',targets[0]));assert target in targets,(key,target,targets)
            kind=b.get('type',b.get('kind'));levels=b.get('levels',b.get('level',1))
            if kind=='shared_slots':commands[target].append(f'add_extra_state_shared_building_slots = {levels}');continue
            if kind in staff:guards.append(staff[kind]+' = yes')
            if kind=='dockyard':guards.append(f'{target} = {{ is_coastal = yes }}')
            if kind in staff and not any(v.get('type')=='shared_slots' for v in buildings):
                guards.append(f'{target} = {{ free_building_slots = {{ building = {kind} size > {levels-1} }} }}')
            elif kind not in ('bunker','naval_base'):
                guards.append(f'{target} = {{ free_building_slots = {{ building = {kind} size > {levels-1} }} }}')
            province=b.get('province')
            if kind in ('bunker','naval_base'):
                assert province,('Province building requires province',key,kind)
                guards.append(f'has_full_control_of_state = {target}')
                guards.append(f'{target} = {{ free_building_slots = {{ building = {kind} size > {levels-1} province = {province} }} }}')
            commands[target].append('add_building_construction = { type = '+kind+f' level = {levels} instant_build = yes'+(f' province = {{ id = {province} }}' if province else '')+' }')
        guards=[g for g in guards if g];valid='\n'.join(dict.fromkeys(guards))
        for t in targets:
            added=sum(b.get('levels',1) for b in buildings if int(b.get('state',targets[0]))==t and b['type']=='shared_slots')
            needed=sum(b.get('levels',1) for b in buildings if int(b.get('state',targets[0]))==t and b['type'] in staff)-added
            if needed>0:valid+=f'\n{t} = {{ free_building_slots = {{ building = industrial_complex size > {needed-1} }} }}'
        success='\n'.join(scope(t,'\n'.join(cmds)) for t,cmds in commands.items())+'\n'+after+'\nset_country_flag = '+done
        if mods:
            iid=self.idea('project_'+key+'_idea',self.nodes[focus_id(unlock)]['label'],'An implemented, funded development programme.',mods)
            success+='\nadd_ideas = '+iid
            if targets[0] in (208,209):
                ongoing=' '.join(f'{t} = {{ is_controlled_by = ISR is_owned_by = PAL }}' for t in targets)
                self.tick.append(f'if = {{ limit = {{ has_country_flag = {done} {ongoing} }} if = {{ limit = {{ NOT = {{ has_idea = {iid} }} }} add_ideas = {iid} }} }} else = {{ remove_ideas = {iid} }}')
        number=1000+len(self.projects)
        # A triggered-only completion callback with no trigger cannot vanish
        # before refunding a project whose political/control conditions failed.
        callback=f'if = {{ limit = {{ has_country_flag = {active} }} if = {{ limit = {{ {valid} }} {success} }}\nelse = {{ set_temp_variable = {{ treasury_change = {paid} }} modify_treasury_effect = yes }}\nclear_variable = {paid}\nclr_country_flag = {active} }}'
        event=self.event(number,'Development Project Completed','The reserved development project has reached its delivery date. If its requirements no longer hold, its original reservation is returned.',[('Review the project.',callback,'',1)],trigger='always = yes',hidden=True)
        start=f'set_variable = {{ {paid} = {PREFIX}cost_{token} }}\n{self.money(share)}\nset_country_flag = {active}\ncountry_event = {{ id = {event} days = {days} }}'
        self.effect('start_'+key,start)
        self.loc(did,self.nodes[focus_id(unlock)]['label']+': Fund the Project')
        building_names={'shared_slots':'building slots','industrial_complex':'civilian factories','arms_factory':'military factories','offices':'office levels','agriculture_district':'agricultural districts','infrastructure':'infrastructure levels','bunker':'land fort levels','naval_base':'naval base levels','dockyard':'naval dockyards'}
        state_names={204:'Tel Aviv',205:'Haifa',206:'the Negev',208:'the West Bank',209:'Gaza',SINAI:'Sinai',CANAL:'Suez and the Eastern Nile Delta'}
        delivery='; '.join('+'+str(b.get('levels',1))+' '+building_names[b['type']]+' in '+state_names.get(int(b.get('state',targets[0])),str(b.get('state',targets[0]))) for b in buildings) or 'the specified clearance and operating works'
        from player_rewards import LABELS
        continuing='; '.join(LABELS.get(k,k.replace('_',' ').title())+': '+f'{v*100:+g}%' for k,v in (mods or {}).items())
        local_lines=[]
        for modifier in sorted(set(re.findall(r'add_dynamic_modifier\s*=\s*\{\s*modifier\s*=\s*(\w+)',after))):
            for k,v in self.dynamic[modifier][0].items():
                if isinstance(v,(int,float)):local_lines.append(LABELS.get(k,k.replace('_',' ').title())+': '+f'{v*100:+g}%')
        for amount in re.findall(r'add_resistance_target\s*=\s*\{[^{}]*?amount\s*=\s*(-?[\d.]+)',after):local_lines.append('Local resistance target: '+f'{float(amount):+g}'+' points')
        for modifier in sorted(set(re.findall(r'add_opinion_modifier\s*=\s*\{[^{}]*?modifier\s*=\s*(\w+)',after))):
            if modifier in self.opinions:local_lines.append('Relations toward Israel: '+f'{self.opinions[modifier][0]:+g}'+' points')
        local_text='; '.join(dict.fromkeys(local_lines))
        project_text=f'Reserve {share*100:g}% of annual GDP at selection. Delivery after {days} days: {delivery}.'+(' Continuing effects: '+continuing+'.' if continuing else '')+(' Local policy effects: '+local_text+'.' if local_text else '')+' Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.'
        self.loc(did+'_desc',project_text)
        delivery_tt=self.loc(did+'_delivery_tt',f'After {days} days: {delivery}.'+(' '+continuing if continuing else '')+(' '+local_text if local_text else ''))
        visible=f'has_completed_focus = {focus_id(unlock)} NOT = {{ has_country_flag = {done} }}'
        gate=f'NOT = {{ has_country_flag = {active} }}\n{PREFIX}afford_{token} = yes\n{valid}'
        self.decisions.append(f'{did} = {{ icon = generic_construction cost = {political_cost} visible = {{ {visible} }} available = {{ {self.readable(gate)} }} complete_effect = {{ custom_effect_tooltip = {delivery_tt} {effect} = yes }} days_re_enable = 1 ai_will_do = {{ factor = 1 }} }}')
        self.projects.append({'key':key,'unlock':unlock,'states':targets,'buildings':buildings,'mods':mods or {},'days':days,'share':share,'guard':valid,'callback':event,'paid':paid,'done':done,'delivery_summary':project_text})
        return 'unlock_decision_tooltip = '+did

    def emit(self,write,loc):
        from policy_map import apply as apply_canal_map
        from policy_world import patch as patch_canal_world
        self.data['policy_expansion']['map']=apply_canal_map(self.root,write,loc)
        patch_canal_world(self,write)
        for share in sorted(self.costs):
            token=self.cost_token(share);var=PREFIX+'cost_'+token
            self.triggers[PREFIX+'afford_'+token]=f'has_variable = gdp_total check_variable = {{ gdp_total > 0 }} has_variable = {var} check_variable = {{ var = treasury value = {var} compare = greater_than_or_equals }} NOT = {{ has_active_mission = bankruptcy_incoming_collapse }}'
            tip=self.loc(PREFIX+'afford_'+token+'_tt',f'The treasury can cover {share*100:g}% of annual GDP, with no pending bankruptcy collapse.')
            self.triggers[PREFIX+'afford_'+token]='custom_trigger_tooltip = { tooltip = '+tip+' '+self.triggers[PREFIX+'afford_'+token]+' }'
            self.effects[PREFIX+'pay_'+token]=f'set_temp_variable = {{ treasury_change = {var} }} multiply_temp_variable = {{ treasury_change = -1 }} modify_treasury_effect = yes'
        refresh='\n'.join(f'set_variable = {{ {PREFIX}cost_{self.cost_token(s)} = gdp_total }}\nmultiply_variable = {{ {PREFIX}cost_{self.cost_token(s)} = {s:g} }}' for s in sorted(self.costs))
        self.effects[PREFIX+'refresh_costs']=refresh
        self.effects[PREFIX+'daily']=PREFIX+'refresh_costs = yes\n'+'\n'.join(self.tick)
        self.loc('ISR70_policy_project_unlock_tt','The funded project is available in decisions. Its budget and delivery time are shown there.')
        self.loc('ISR70_policy_category','Israeli Development and Territorial Policy')
        self.loc('ISR70_policy_category_desc','Fund concrete projects, negotiate with the affected governments, and choose the legal and constitutional rules applied by the Israeli administration.')
        for k,v in self.localisation.items():loc(k,v)
        header='# Generated from tools/israel_1970/policy_design.json and policy compiler.\n'
        write('common/scripted_effects/ISR70_policy_effects.txt',header+'\n\n'.join(k+' = {\n'+v+'\n}' for k,v in self.effects.items())+'\n')
        write('common/scripted_triggers/ISR70_policy_triggers.txt',header+'\n\n'.join(k+' = {\n'+v+'\n}' for k,v in self.triggers.items())+'\n')
        write('common/dynamic_modifiers/ISR70_policy_dynamic_modifiers.txt',header+'\n\n'.join(k+' = {\nicon = GFX_idea_political_establishment\nenable = { '+gate+' }\n'+'\n'.join(m+' = '+str(v) for m,v in mods.items())+'\n}' for k,(mods,gate) in self.dynamic.items())+'\n')
        write('common/decisions/categories/ISR70_policy_category.txt',header+'ISR70_policy_category = { icon = generic_political_actions allowed = { original_tag = ISR } visible = { ISR70_is_scenario = yes } }\n')
        write('common/decisions/ISR70_policy_decisions.txt',header+'ISR70_policy_category = {\n'+'\n\n'.join(self.decisions)+'\n}\n')
        if hasattr(self,'egypt_decisions'):
            write('common/decisions/categories/ISR70_policy_egypt_category.txt',header+'ISR70_policy_egypt_canal_category = { icon = generic_political_actions allowed = { original_tag = EGY } visible = { IMP_is_1970_scenario = yes } }\n')
            write('common/decisions/ISR70_policy_egypt_decisions.txt',header+self.egypt_decisions+'\n')
        write('events/ISR70_policy_events.txt',header+'add_namespace = ISR70P\n\n'+'\n\n'.join(self.events)+'\n')
        write('common/on_actions/ISR70_policy_on_actions.txt',header+'on_actions = { on_startup = { effect = { ISR = { if = { limit = { ISR70_is_scenario = yes } ISR70_policy_daily = yes } } } } on_daily = { effect = { if = { limit = { ISR70_is_scenario = yes } ISR70_policy_daily = yes } } } }\n')
        write('common/opinion_modifiers/ISR70_policy_opinion_modifiers.txt',header+'opinion_modifiers = {\n'+'\n'.join(k+' = { value = '+str(v)+' days = '+str(days)+' }' for k,(v,days) in self.opinions.items())+'\n}\n')
        self.data['policy_expansion'].update(projects=self.projects,events=len(self.events),decisions=len(self.decisions),effects=len(self.effects),triggers=len(self.triggers))

def install(data,root,art):
    api=PolicyCompiler(data,root,art)
    from policy_domestic import build as domestic
    from policy_territories import build as territories
    domestic(api);territories(api)
    from policy_world import register as register_world
    register_world(api)
    for project in api.projects:api.nodes[focus_id(project['unlock'])]['policy_summary'].append(project['delivery_summary'])
    expected={n['id'] for b in api.design['branches'] for n in b['common']+[v for p in b['paths'] for v in p['nodes']]}
    assert expected==api.focus_specs.keys(),('Missing policy focus implementations',expected-api.focus_specs.keys())
    return api
