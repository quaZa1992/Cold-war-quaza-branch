"""Territorial projects, negotiated status and explicitly optional radical policy."""
from policy_common import SINAI,focus_id,ident,flag,has,scope

def build(api):
    def gated(key):return has(key)
    def done(key):return has('project_'+key+'_done')
    def clear(key):return 'clr_country_flag = '+ident(key)
    def call(key):return ident(key)+' = yes'
    def local(name,mods,state,gate='always = yes'):
        mid=api.state_modifier(name,name.replace('_',' ').title(),'An explicitly scoped territorial policy. It applies only under the stated controller and policy conditions.',mods,
            enable='is_controlled_by = ISR\nISR = { ISR70_is_scenario = yes '+gate+' }')
        return scope(state,'add_dynamic_modifier = { modifier = '+mid+' }')
    def nation(key,mods,code='',available='',text=''):
        iid=api.idea(key+'_idea',api.nodes[focus_id(key)]['label'],text or 'A distinct national policy programme with ongoing budget consequences.',mods)
        api.focus(key,'add_ideas = '+iid+'\n'+code,available=available,description=text)
        return iid
    def resistance(state,amount,rid,occupied='EGY',days=None):
        tip='ISR70_policy_resistance_'+str(rid)+'_tt';api.loc(tip,'Resistance target from this policy: '+f'{amount:+g}'+' percentage points.')
        return scope(state,f'remove_resistance_target = {rid}\nadd_resistance_target = {{ id = {rid} amount = {amount} occupied = {occupied} occupier = ISR tooltip = {tip}'+(f' days = {days}' if days else '')+' }')
    def project(key,state,buildings,share,days,mods=None,after='',available='',pp=0):
        unlock=api.project(key,state,buildings,share,days,mods=mods,after=after,available=available,political_cost=pp)
        api.focus(key,unlock,description=f'Fund the specified project through decisions. Reserve {share*100:g}% of GDP; delivery takes {days} days. Lost requirements refund the original reserved budget.')
    def for_target(code):
        return '\n'.join(f'if = {{ limit = {{ {has("target_"+str(s))} }} {code(s)} }}' for s in (208,209))
    def project_target(key,buildings,share,days,mods=None,after=None,available='',pp=0):
        unlocks=[]
        for s in (208,209):
            items=[{**b,'province':7107 if s==208 else 13207} if b['type']=='bunker' else b for b in buildings]
            unlocks.append(api.project(key+'_'+str(s),s,items,share,days,mods=mods,
                after=after(s) if after else '',available='\n'.join(x for x in (has('target_'+str(s)),f'{s} = {{ is_owned_by = PAL }}',available) if x),political_cost=pp,unlock=key))
        api.focus(key,'\n'.join(unlocks),description=f'One selected Palestinian-owned target: the West Bank or Gaza. Reserve {share*100:g}% of GDP for the chosen project; delivery takes {days} days. It is not a grant of ownership or a core.')
    def target_project_done(key):return 'OR = { '+done(key+'_208')+' '+done(key+'_209')+' }'

    # Survey once, then one target and one construction policy. A Palestinian
    # government retains its response; player selection cannot award its assent.
    survey=api.event(400,'Select the Settlement Project Area','Select one Palestinian-owned area currently controlled by Israel. All three settlement policies refer to this same project area.',[
        ('Review the West Bank.',flag('target_208'), '208 = { is_owned_by = PAL is_controlled_by = ISR }',2),
        ('Review Gaza.',flag('target_209'), '209 = { is_owned_by = PAL is_controlled_by = ISR }',1)],trigger='ISR70_is_scenario = yes')
    api.focus('land_survey',api.money(.001)+f'\ncountry_event = {{ id = {survey} days = 1 }}',
        available='OR = { 208 = { is_owned_by = PAL is_controlled_by = ISR } 209 = { is_owned_by = PAL is_controlled_by = ISR } }',
        description='Survey one controlled Palestinian-owned project area. The survey costs 0.1% of GDP; it neither changes ownership nor predetermines Palestinian consent.')
    api.focus('settlement_budget',flag('settlement_budget'),available='OR = { '+has('target_208')+' '+has('target_209')+' }',description='Choose the settlement project budget for the already selected area. Freeze, limited development and expansion are mutually exclusive; each has its own actual funding and Palestinian consequences.')
    pal_gate='original_tag = PAL\nIMP_is_1970_scenario = yes\nISR = { ISR70_is_scenario = yes }'
    freeze_accept=for_target(lambda s:resistance(s,-5,197000+s,'PAL'))
    freeze_event=api.event(401,'A Settlement Freeze Proposal','Israel proposes a binding freeze of new settlement projects and a local administrative agreement. Palestinian representatives may reject the terms.',[
        ('Accept the freeze and open administrative talks.','ISR = { '+flag('freeze_agreed')+'\n'+freeze_accept+' }\n'+api.opinion('settlement_freeze',15,'ISR'),'',3),
        ('Decline these terms.','ISR = { '+flag('freeze_declined')+' }','',2)],trigger=pal_gate)
    api.focus('freeze_new',api.pay_pp(75)+'\n'+flag('freeze_offer')+f'\nPAL = {{ country_event = {{ id = {freeze_event} days = 1 }} }}',
        available='PAL = { exists = yes } OR = { '+has('target_208')+' '+has('target_209')+' }',
        description='Pay 75 political power and offer a settlement freeze. Only an accepted offer reduces the local resistance target by 5 points. Rejection changes neither control nor rights.')
    api.decision('retry_freeze','Renew the Settlement Freeze Proposal','A rejected proposal can be renewed; Palestinian consent is still required.','freeze_new',
        'PAL = { exists = yes } NOT = { '+has('freeze_agreed')+' }',f'PAL = {{ country_event = {{ id = {freeze_event} days = 1 }} }}',cost=25,repeatable=True,cooldown=360)
    project_target('municipal_works',[{'type':'industrial_complex','levels':1},{'type':'infrastructure','levels':1}],.015,270,
        mods={'social_cost_multiplier_modifier':.02},after=lambda s:local('settlement_municipal_supply_'+str(s),{'local_supplies_for_controller':.10},s),available=has('freeze_agreed'))
    compact=api.event(402,'A Local Administrative Compact','Israel offers an administrative compact and a funded transfer for agreed civilian services. Acceptance leaves legal ownership unchanged.',[
        ('Accept the compact.','ISR = { '+flag('land_compact_agreed')+' }','',3),
        ('Decline the administrative terms.','ISR = { '+flag('land_compact_declined')+' }','',2)],trigger=pal_gate)
    api.focus('land_compact',f'PAL = {{ country_event = {{ id = {compact} days = 1 }} }}',available=target_project_done('municipal_works'),
        description='Open a separate administrative agreement. The transfer and reductions in garrison and administrative costs require actual Palestinian acceptance and implementation.')
    compact_idea=api.idea('land_compact','Local Administrative Compact','A funded local administrative compact reduces central administration costs.',{'bureaucracy_cost_multiplier_modifier':-.05})
    transfer='set_variable = { ISR70_policy_transfer = ISR70_policy_cost_0_0030 }\nPAL = { set_temp_variable = { treasury_change = ISR.ISR70_policy_transfer } modify_treasury_effect = yes }\nclear_variable = ISR70_policy_transfer'
    api.decision('implement_land_compact','Fund the Accepted Administrative Compact','Transfer 0.3% of GDP for Palestinian civilian services. Only implementation grants the administrative benefits.','land_compact',
        has('land_compact_agreed')+'\nPAL = { exists = yes }',api.money(.003)+'\n'+transfer+'\nadd_ideas = '+compact_idea+'\n'+for_target(lambda s:local('compact_garrison_'+str(s),{'required_garrison_factor':-.20},s)+'\n'+resistance(s,-5,198000+s,'PAL')))
    project_target('designated_sites',[{'type':'shared_slots','levels':1},{'type':'agriculture_district','levels':1}],.008,240,
        mods={'bureaucracy_cost_multiplier_modifier':.02},after=lambda s:'PAL = { '+api.opinion('designated_sites',-10,'ISR')+' }')
    project_target('settlement_services',[{'type':'infrastructure','levels':1}],.006,180,
        after=lambda s:local('limited_supply_'+str(s),{'local_supplies_for_controller':.15},s)+'\n'+resistance(s,5,199000+s,'PAL'),available=target_project_done('designated_sites'))
    project_target('settlement_ceiling',[{'type':'bunker','levels':1}],.004,180,
        after=lambda s:local('limited_garrison_'+str(s),{'required_garrison_factor':.05},s)+'\n'+flag('binding_settlement_ceiling'),available=target_project_done('settlement_services'))
    project_target('authorize_expansion',[{'type':'shared_slots','levels':3}],.003,90,
        mods={'bureaucracy_cost_multiplier_modifier':.02},after=lambda s:local('settlement_infra_'+str(s),{'state_production_speed_infrastructure_factor':.15},s)+'\nPAL = { '+api.opinion('settlement_expansion',-25,'ISR')+' }')
    project_target('settlement_package',[{'type':'agriculture_district','levels':1},{'type':'industrial_complex','levels':1}],.023,300,
        mods={'social_cost_multiplier_modifier':.03},available=target_project_done('authorize_expansion'))
    project_target('entrench_network',[{'type':'infrastructure','levels':2},{'type':'bunker','levels':2}],.009,240,
        mods={'bureaucracy_cost_multiplier_modifier':.03},after=lambda s:local('network_supply_'+str(s),{'local_supplies_for_controller':.25},s),available=target_project_done('settlement_package'))
    compensation=api.event(403,'Settlement Limits and Compensation','Israel offers a binding limit on new settlement expansion and a funded compensation arrangement. It cannot impose Palestinian agreement.',[
        ('Accept the limited compensation arrangement.','ISR = { '+flag('settlement_compensation_accepted')+' }','',2),
        ('Reject the proposed limit and compensation.','ISR = { '+flag('settlement_compensation_rejected')+' }','',3)],trigger=pal_gate)
    api.focus('settlement_compensation',api.pay_pp(75)+f'\nPAL = {{ country_event = {{ id = {compensation} days = 1 }} }}',
        available=target_project_done('entrench_network')+'\nPAL = { exists = yes }',
        description='Pay 75 political power to negotiate a binding expansion ceiling. PAL can reject. An accepted arrangement requires a separate 0.6% GDP transfer; then resistance target rises 3 points and garrison need rises 5%, rather than the unilateral penalties.')
    api.decision('fund_settlement_compensation','Implement the Accepted Settlement Limit','Pay the additional 0.6% GDP only after acceptance. Further expansion is barred by the agreement.','settlement_compensation',
        has('settlement_compensation_accepted')+'\nPAL = { exists = yes }',api.money(.006)+'\n'+flag('binding_settlement_ceiling')+'\n'+for_target(lambda s:local('compensated_garrison_'+str(s),{'required_garrison_factor':.05},s)+'\n'+resistance(s,3,200000+s,'PAL')))
    api.decision('retry_settlement_compensation','Renew the Settlement Limit Proposal','The new offer still requires PAL to agree.','settlement_compensation',
        'PAL = { exists = yes } NOT = { '+has('settlement_compensation_accepted')+' }',f'PAL = {{ country_event = {{ id = {compensation} days = 1 }} }}',cost=25,repeatable=True,cooldown=360)
    response=api.event(404,'Response to Unilateral Settlement Expansion','Israel has imposed the settlement network without an accepted agreement. Palestinian institutions choose how to respond.',[
        ('Seek external mediation.',api.opinion('unilateral_settlement',-20,'ISR'),'',3),
        ('Mobilize political opposition.',api.opinion('unilateral_settlement',-25,'ISR')+'\nadd_political_power = 25','',3)],trigger=pal_gate)
    api.focus('settlement_unilateral',api.pay_pp(50)+'\n'+flag('settlement_unilateral')+'\n'+for_target(lambda s:local('unilateral_garrison_'+str(s),{'required_garrison_factor':.15,'resistance_damage_to_garrison':.10},s)+'\n'+resistance(s,10,201000+s,'PAL'))+f'\nPAL = {{ country_event = {{ id = {response} days = 1 }} }}',
        available=target_project_done('entrench_network'),description='Impose the network unilaterally. Pay 50 political power; local resistance target rises 10 points, garrison need 15% and garrison damage 10%. PAL receives an actual response event; war is not declared automatically.')

    # A shared mandate is paid once across the territorial and Herut branches.
    mandate=api.effect('secure_greater_mandate','if = { limit = { NOT = { '+has('greater_mandate')+' } } add_political_power = -100 '+flag('greater_mandate')+' }')
    mandate_gate='OR = { '+has('greater_mandate')+' political_power > 99 }'
    hardliner='OR = { western_conservative_are_in_power = yes western_autocrats_are_in_power = yes nationalist_right_wing_populists_are_in_power = yes nationalist_monarchists_are_in_power = yes }'
    # Exact party APIs are taken from existing groups rather than invented names.
    parties={g['party']:g['trigger'] for g in api.data['groups'] if g['party'] is not None}
    hardliner='OR = { AND = { '+parties[1]+' = yes has_completed_focus = ISR70_p1_cb } AND = { '+parties[0]+' = yes has_completed_focus = ISR70_p0_cb } '+parties[21]+' = yes '+parties[22]+' = yes }'
    api.focus('gi_mandate',mandate+' = yes',available=mandate_gate+'\n'+hardliner+'\nNOT = { has_country_flag = ISR70_egypt_peace_signed }',description='Pay the shared 100-political-power territorial mandate once. A mandate already paid through Herut covers this focus; it grants neither ownership nor a declaration of war.')
    api.focus('gi_frontier_review',api.money(.002),description='Budget 0.2% of GDP to separate Sinai civilian development, coastal projects, and the later choice of legal status.')
    nation('gi_sinai_admin',{'bureaucracy_cost_multiplier_modifier':.03},api.money(.003)+'\n'+local('sinai_administration',{'state_production_speed_infrastructure_factor':.15},213),available='213 = { is_controlled_by = ISR }',text='Establish permanent Sinai administration at a cost of 0.3% of GDP. Local infrastructure builds 15% faster; bureaucracy costs rise 3%. Egyptian ownership remains until an actual territorial settlement.')
    project('gi_sinai_housing',213,[{'type':'shared_slots','levels':2},{'type':'infrastructure','levels':1}],.010,240)

    # Voluntary migration changes state population by equal and opposite amounts.
    def migration(key,target,total,years,cost,extra=''):
        installments=years*12;chunk=total//installments;last=total-chunk*(installments-1)
        active=ident(key+'_migration_active');count=ident(key+'_migration_steps');doneflag=ident(key+'_migration_done')
        idea=api.idea(key+'_services',api.nodes[focus_id(key)]['label'],'Temporary family services for a limited voluntary internal migration programme.',{'social_cost_multiplier_modifier':.02})
        api.focus(key,api.money(cost)+f'\nset_variable = {{ {count} = 0 }}\nset_country_flag = {active}\nadd_timed_idea = {{ idea = {idea} days = {years*365} }}\n'+extra,
            available=f'{target} = {{ is_controlled_by = ISR }}\n204 = {{ is_owned_by = ISR is_controlled_by = ISR state_population > {total} }}',
            description=f'Fund a voluntary internal movement of at most {total:,} people over {years} years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.')
        eventno=1100+len(api.data.get('policy_migrations',[]))
        step=f'''if = {{ limit = {{ has_country_flag = {active} }}
if = {{ limit = {{ {target} = {{ is_controlled_by = ISR }} 204 = {{ is_owned_by = ISR is_controlled_by = ISR state_population > {last} }} }}
if = {{ limit = {{ check_variable = {{ {count} < {installments-1} }} }}
204 = {{ add_manpower = {-chunk} }} {target} = {{ add_manpower = {chunk} }}
add_to_variable = {{ {count} = 1 }} country_event = {{ id = ISR70P.{eventno} days = 30 }}
}} else = {{ 204 = {{ add_manpower = {-last} }} {target} = {{ add_manpower = {last} }} set_country_flag = {doneflag} clr_country_flag = {active} }}
}} else = {{ clr_country_flag = {active} remove_ideas = {idea} }} }}'''
        api.event(eventno,'Voluntary Internal Migration','A limited, funded internal settlement cohort moves between the two named states.',[('Record this month.',step,'',1)],trigger='always = yes',hidden=True)
        # Schedule once after the focus has set the active flag.
        api.effects[ident('complete_'+key)]+=f'\ncountry_event = {{ id = ISR70P.{eventno} days = 30 }}'
        api.data.setdefault('policy_migrations',[]).append(dict(key=key,source=204,target=target,total=total,installments=installments,chunk=chunk,last=last))
    migration('gi_sinai_families',213,20000,5,.010,extra='')
    api.nodes[focus_id('gi_sinai_families')]['available']+='\n'+done('gi_sinai_housing')
    growth=api.idea('frontier_family_services','Frontier Family Services','A five-year national family-service programme; monthly_population is a growth-rate modifier, not a migration count.',{'monthly_population':.05,'health_cost_multiplier_modifier':.02})
    api.focus('gi_frontier_families',api.money(.004)+f'\nadd_timed_idea = {{ idea = {growth} days = 1825 }}',description='Fund 0.4% of GDP for a single five-year family-service idea: population-growth modifier +5%, healthcare costs +2%. It does not add 5% of the population each month and cannot stack with itself.')
    project('gi_sinai_economy',213,[{'type':'agriculture_district','levels':1},{'type':'industrial_complex','levels':1}],.018,300,available=done('gi_sinai_housing'))
    api.focus('gi_sinai_status',api.pay_pp(150)+'\n'+flag('sinai_sovereignty_settled'),available='213 = { is_owned_by = ISR is_controlled_by = ISR }',description='After an actual peace settlement has transferred Sinai, pay 150 political power for its sovereignty administration. This focus does not transfer the state or remove the Egyptian core.')
    claims=api.opinion('canal_claims',-40,'ISR')
    api.focus('gi_canal_claim',api.pay_pp(150)+f'\nadd_state_claim = {SINAI}\nEGY = {{ {claims} }}\nPAL = {{ '+api.opinion('regional_claims',-15,'ISR')+' }\nJOR = { '+api.opinion('regional_claims',-15,'ISR')+' }',
        available='NOT = { has_country_flag = ISR70_egypt_peace_signed }\nEGY = { exists = yes }',description='Pay 150 political power for a Sinai territorial claim. Relations with Egypt fall 40 and with PAL/Jordan 15. This neither changes ownership nor declares war.')
    api.decision('canal_wargoal','Prepare a Sinai War Goal','Authorize a distinct territorial war goal. Declaring war remains a separate player decision.','gi_canal_claim',
        f'EGY = {{ exists = yes controls_state = {SINAI} }} NOT = {{ has_war_with = EGY }} NOT = {{ has_country_flag = ISR70_egypt_peace_signed }}',
        f'create_wargoal = {{ type = take_state_focus target = EGY generator = {{ {SINAI} }} }}',cost=50)
    project('gi_canal_repair',SINAI,[{'type':'infrastructure','levels':1},{'type':'naval_base','levels':1,'province':10099}],.012,240,
        after=local('canal_repair_garrison',{'required_garrison_factor':.10},SINAI))
    migration('gi_canal_settlers',SINAI,15000,5,.012)
    api.nodes[focus_id('gi_canal_settlers')]['available']+='\n'+done('gi_canal_repair')
    project('gi_canal_industry',SINAI,[{'type':'shared_slots','levels':2},{'type':'industrial_complex','levels':1},{'type':'dockyard','levels':1}],.020,360,available=done('gi_canal_repair'))
    project('gi_canal_navigation',SINAI,[],.008,180,mods={'bureaucracy_cost_multiplier_modifier':.01},
        after=local('sinai_coastal_logistics',{'local_supplies_for_controller':.10},SINAI),
        available=done('gi_canal_repair'))
    api.focus('gi_canal_province',api.pay_pp(150)+'\n'+api.money(.003)+'\n'+flag('canal_province_constituted'),available=f'{SINAI} = {{ is_owned_by = ISR is_controlled_by = ISR }}',
        description='Constitute the Sinai province only after actual Israeli ownership and control. Pay 150 political power and 0.3% of GDP; bureaucracy costs rise 3%. No core is granted.')
    province_idea=api.idea('canal_province_admin','Sinai Provincial Administration','An annexed province requires a permanent civil administrative apparatus.',{'bureaucracy_cost_multiplier_modifier':.03})
    api.effects[ident('complete_gi_canal_province')]+='\nadd_ideas = '+province_idea

    build_status(api,nation,local,resistance,parties)
    build_radicals(api,nation,local,resistance,migration,parties,mandate,mandate_gate)
    finalize_factory_access(api)

    # A 1970 peace proposal cannot simultaneously leave a maximalist mandate
    # active, and its implementation must return the occupied Sinai.
    for name in ('territorial_maximalism','egypt_peace'):
        n=api.nodes['ISR70_'+name]
        if name=='egypt_peace':n['available']+='\nNOT = { '+has('greater_mandate')+' } NOT = { '+has('inalienable_land')+' } NOT = { '+has('herut_retention')+' }'
    for d in api.data['decisions']:
        if d['id']=='ISR70_decision_talks_egypt':d['available']+='\nNOT = { '+has('greater_mandate')+' }'
    api.decision('abandon_territorial_mandate','Abandon the Permanent Territorial Mandate','Pay 100 political power to abandon permanent territorial retention. Previous projects and civilian claims remain; an Egyptian agreement is still required before withdrawal.',
        'gi_mandate',has('greater_mandate'),clear('greater_mandate')+'\n'+clear('herut_retention'),cost=100,repeatable=True,cooldown=365)
    withdrawal=api.event(430,'An Israeli Territorial Withdrawal Proposal','Israel has abandoned its permanent-retention mandate and offers an actual return of the controlled Sinai. The agreement does not erase earlier civilian property or return claims.',[
        ('Accept the territorial return.','ISR = { set_country_flag = ISR70_egypt_peace_signed ISR70_implement_egypt_peace = yes }','',5),
        ('Reject these security terms.','ISR = { '+flag('withdrawal_rejected')+' }','',1)],
        trigger='original_tag = EGY IMP_is_1970_scenario = yes ISR = { NOT = { '+has('greater_mandate')+' } NOT = { '+has('inalienable_land')+' } }')
    api.decision('negotiate_withdrawal','Negotiate Sinai Withdrawal','After abandoning the mandate, negotiate an explicit return even if the original maximalist focus choice remains in the historical focus record. Egypt must accept; no other owner\'s territory is transferred.',
        'gi_mandate','EGY = { exists = yes } NOT = { '+has('greater_mandate')+' } NOT = { '+has('inalienable_land')+' } controls_state = 213',
        f'EGY = {{ country_event = {{ id = {withdrawal} days = 7 }} }}',cost=50,repeatable=True,cooldown=360)

def build_status(api,nation,local,resistance,parties):
    """Exclusive legal regimes, conditional cooperation and genuine consent."""
    def clear(k):return 'clr_country_flag = '+ident(k)
    c=SINAI
    available=f'{c} = {{ is_controlled_by = ISR NOT = {{ is_core_of = ISR }} }}'
    names=['equal_civil','occupation_special','kach_special']
    # Clear only status-bound effects. Buildings, voluntary population moves,
    # expulsion damage, and property claims survive a later legal reform.
    country_ideas=[];state_mods=[];regime_resistance=[202000,202001]
    def statusidea(key,label,mods):
        iid=api.idea(key,label,'A legal-status policy with explicit continuing costs. It is replaced, not stacked, when the legal regime changes.',mods);country_ideas.append(iid);return iid
    def statusmod(key,mods,regime):
        mid=api.state_modifier(key,key.replace('_',' ').title(),'A local status-bound modifier.',mods,
            enable='is_controlled_by = ISR ISR = { '+has(regime)+' }');state_mods.append(mid);return mid
    eq=statusidea('equal_status','Equal Civil Rights',{'social_cost_multiplier_modifier':.03})
    special=statusidea('special_status','Unequal Occupation Status',{'social_cost_multiplier_modifier':-.02,'police_cost_multiplier_modifier':.03})
    kach=statusidea('kach_status','Radical Unequal Status',{'police_cost_multiplier_modifier':.05})
    eq_council=statusidea('equal_council_admin','Civil Service Transition',{'bureaucracy_cost_multiplier_modifier':.02})
    delegated=statusidea('delegated_admin','Delegated Occupation Administration',{'bureaucracy_cost_multiplier_modifier':-.03,'corruption_cost_factor':.03})
    statute=statusidea('permanent_statute','Permanent Occupation Statute',{'police_cost_multiplier_modifier':.02,'stability_factor':-.02})
    eq_local=statusmod('equal_council_garrison',{'required_garrison_factor':-.05},'equal_civil')
    sp_local=statusmod('special_status_access',{'local_factories':.10,'required_garrison_factor':.15},'occupation_special')
    road_local=statusmod('occupation_roads',{'local_supplies_for_controller':.15,'required_garrison_factor':.05},'occupation_special')
    industry_local=statusmod('occupation_industry_garrison',{'required_garrison_factor':.05},'occupation_special')
    statute_local=statusmod('permanent_statute_access',{'local_factories':.05},'occupation_special')
    kach_local=statusmod('kach_status_access',{'local_factories':.10,'required_garrison_factor':.10},'kach_special')
    cleanup='\n'.join(clear(k) for k in names+['equal_since','low_resistance_since','local_status_accepted','egypt_status_accepted','council_agreed','delegated_agreed','delegated_admin_active','permanent_statute_active'])
    cleanup+='\n'+'\n'.join('remove_ideas = '+k for k in country_ideas)
    cleanup+='\n'+scope(c,'\n'.join('remove_dynamic_modifier = '+k for k in state_mods)+'\n'+'\n'.join('remove_resistance_target = '+str(k) for k in regime_resistance))
    # Later radical constitutional ideas are also status-bound and removable.
    cleanup+='\nremove_ideas = ISR70_policy_permanent_emergency\nremove_ideas = ISR70_policy_electoral_sunset\n'+scope(c,'remove_dynamic_modifier = ISR70_policy_emergency_access\nremove_dynamic_modifier = ISR70_policy_sunset_access')
    api.effect('clear_status',cleanup)
    mark_status=flag('status_chosen')+'\n'+clear('reform_equal_authorized')+'\n'+clear('reform_special_authorized')
    activate_equal=api.effect('activate_equal','ISR70_policy_clear_status = yes\n'+mark_status+'\n'+flag('equal_civil')+'\n'+flag('equal_since')+'\nadd_ideas = '+eq)
    activate_special=api.effect('activate_special','ISR70_policy_clear_status = yes\n'+mark_status+'\n'+flag('occupation_special')+'\nadd_ideas = '+special+'\n'+scope(c,'add_dynamic_modifier = { modifier = '+sp_local+' }')+'\n'+resistance(c,8,202000)+f'\nif = {{ limit = {{ {has("project_occ_security_roads_done")} }} {scope(c,"add_dynamic_modifier = { modifier = "+road_local+" }")} }}'+f'\nif = {{ limit = {{ {has("project_occ_occupation_industry_done")} }} {scope(c,"add_dynamic_modifier = { modifier = "+industry_local+" }")} }}')
    api.effect('activate_kach','ISR70_policy_clear_status = yes\n'+mark_status+'\n'+flag('kach_special')+'\nadd_ideas = '+kach+'\n'+scope(c,'add_dynamic_modifier = { modifier = '+kach_local+' }'))
    revoked=f'if = {{ limit = {{ {has("equal_civil")} }} '+resistance(c,5,202003,days=730)+' }\n'
    api.effects[activate_special]=revoked+api.effects[activate_special]
    api.effects[ident('activate_kach')]=revoked+api.effects[ident('activate_kach')]
    api.focus('gi_resident_status',api.pay_pp(50)+'\n'+flag('resident_status_review'),available=available,description='Pay 50 political power to open the actual choice of equal civil status or an unequal occupation statute. Settlement projects and party affiliation do not select the legal status automatically.')
    api.focus('gi_equal_status',api.pay_pp(100)+'\n'+activate_equal+' = yes',available=available+'\nNOT = { '+has('active_expulsion')+' }\nOR = { NOT = { '+has('status_chosen')+' } '+has('reform_equal_authorized')+' }',description='Equal legal rights and service entitlements cost 100 political power and +3% social spending. There is no immediate resistance, compliance, loyalty or sovereignty-consent bonus. A previously chosen unequal regime must first be repealed through the explicit reform decision.')
    api.focus('occ_special_status',api.pay_pp(50)+'\n'+activate_special+' = yes\nEGY = { '+api.opinion('unequal_canal_status',-15,'ISR')+' }\nPAL = { '+api.opinion('unequal_canal_status',-15,'ISR')+' }',available=available,
        description='Choose unequal occupation law. Existing local factory access rises 10 points, garrison needs rise 15%, police costs 3%, and resistance target 8 points; social spending falls 2%. The general and Kach statutes replace each other.')
    api.nodes[focus_id('occ_special_status')]['available']+='\nOR = { NOT = { '+has('status_chosen')+' } '+has('reform_special_authorized')+' }'
    council=api.event(410,'Local Civil Administration Talks','Municipal representatives from Sinai consider a practical administrative contract. Accepting administrative duties does not recognize Israeli sovereignty or bind every resident.',[
        ('The representatives accept a limited administrative contract.','ISR = { '+flag('council_agreed')+' }','',2),
        ('The representatives decline the contract.','ISR = { '+flag('council_declined')+' }','',5)],
        trigger='original_tag = EGY IMP_is_1970_scenario = yes ISR = { '+has('equal_civil')+' }')
    api.focus('gi_canal_councils',api.money(.008)+'\nadd_ideas = '+eq_council+f'\nEGY = {{ country_event = {{ id = {council} days = 7 }} }}',available=has('equal_civil')+'\nEGY = { exists = yes }',
        description='Fund civilian services at 0.8% of GDP and +2% bureaucracy costs. A separately accepted and implemented local contract reduces garrison needs only 5%. Rejection grants no bonus and does not repeal equal rights.')
    api.decision('implement_council','Implement the Accepted Council Contract','A limited administrative agreement reduces garrison duties only while it remains valid. It is not an endorsement of annexation.','gi_canal_councils',
        has('equal_civil')+'\n'+has('council_agreed')+f'\n{c} = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {eq_local} }} }} }}',scope(c,'add_dynamic_modifier = { modifier = '+eq_local+' }'),repeatable=True)
    api.decision('renew_council_talks','Renew Council Talks','An unsuccessful approach can be renewed after a year. No cooperation is presumed.','gi_canal_councils',
        has('equal_civil')+'\nEGY = { exists = yes } NOT = { '+has('council_agreed')+' }',f'EGY = {{ country_event = {{ id = {council} days = 7 }} }}',cost=25,repeatable=True,cooldown=360)
    property_event=api.event(411,'Property Claims and Return Arrangements','Claimants consider whether the offered restitution and return framework meets their concrete claims. A fund alone does not settle those claims.',[
        ('Accept and verify the agreed restitution.','ISR = { '+flag('property_claims_agreed')+' }','',2),
        ('The claims remain unresolved.','ISR = { '+flag('property_claims_unresolved')+' }','',3)],trigger='original_tag = EGY IMP_is_1970_scenario = yes ISR = { '+has('equal_civil')+' }')
    api.focus('gi_property_settlement',api.money(.007)+'\n'+flag('restitution_fund')+f'\nEGY = {{ country_event = {{ id = {property_event} days = 30 }} }}',available=has('equal_civil')+'\nEGY = { exists = yes }',
        description='Reserve at least 0.7% of GDP for restitution. Only fulfilled, agreed claims can lower resistance target by 2 points. Prior expulsion creates additional obligations; there is no automatic loyalty or compliance reward.')
    api.decision('fulfil_property_claims','Fulfil the Agreed Property and Return Terms','Resolve outstanding civilian claims before the small resistance effect is awarded. Previous forced displacement requires a further funded restitution step.','gi_property_settlement',
        has('equal_civil')+'\n'+has('property_claims_agreed')+'\nNOT = { '+has('active_expulsion')+' }\nOR = { NOT = { '+has('expulsion_damage')+' } '+has('additional_restitution_paid')+' }',
        flag('property_claims_fulfilled')+'\n'+resistance(c,-2,202002))
    api.decision('additional_restitution','Fund Additional Restitution after Forced Displacement','Pay an additional 0.7% of GDP toward the outstanding claims caused by the prior forced displacement. No people are erased from the population by this accounting step.','gi_property_settlement',
        has('equal_civil')+'\n'+has('expulsion_damage')+'\n'+has('property_claims_agreed'),api.money(.007)+'\n'+flag('additional_restitution_paid'))
    api.decision('renew_property_talks','Renew Property and Return Negotiations','The claimants retain a real right to refuse the proposed terms.','gi_property_settlement',
        has('equal_civil')+'\nEGY = { exists = yes } NOT = { '+has('property_claims_agreed')+' }',f'EGY = {{ country_event = {{ id = {property_event} days = 30 }} }}',cost=25,repeatable=True,cooldown=360)
    # A province's native compliance percentage never substitutes for a vote.
    long_gate=api.trigger('core_long_conditions',f'''{c} = {{ is_owned_by = ISR is_controlled_by = ISR compliance > 69 resistance < 10.001 }}
stability > 0.5999
has_country_flag = {{ flag = ISR70_policy_owned_since days > 3649 }}
has_country_flag = {{ flag = ISR70_policy_equal_since days > 1824 }}
has_country_flag = {{ flag = ISR70_policy_low_resistance_since days > 729 }}
{has('equal_civil')} {has('property_claims_fulfilled')}
NOT = {{ {has('active_expulsion')} }}''')
    long_tip=api.loc(long_gate+'_tt','Sinai has ten continuous years of Israeli ownership/control, five years of equal civil rights, and two years of resistance at most 10%. Stability is at least 60%, compliance at least 70%, agreed property/return obligations are fulfilled, and no forced displacement is active.')
    api.triggers[long_gate]='custom_trigger_tooltip = { tooltip = '+long_tip+' '+api.triggers[long_gate]+' }'
    consultation=api.event(412,'The Sinai Status Consultation','The district status process has reached its long-term review. Local civic representatives consider the proposed status separately from Egyptian sovereignty negotiations. Services and rights do not guarantee an affirmative result.',[
        ('The local consultation accepts the proposed status.','ISR = { '+flag('local_status_accepted')+' }', '',1),
        ('The consultation rejects integration.','ISR = { '+flag('local_status_rejected')+' }','',6)],trigger='original_tag = EGY IMP_is_1970_scenario = yes ISR = { '+long_gate+' = yes }')
    sovereignty=api.event(413,'A Proposed Sinai Sovereignty Settlement','Local assent alone does not settle Egypt\'s sovereign claim. The Egyptian government must separately accept or refuse the actual Sinai agreement.',[
        ('Accept the specific sovereignty settlement.','ISR = { '+flag('egypt_status_accepted')+' }','',1),
        ('Reject the permanent transfer of sovereignty.','ISR = { '+flag('egypt_status_rejected')+' }','',10)],trigger='original_tag = EGY IMP_is_1970_scenario = yes ISR = { '+has('local_status_accepted')+' }')
    api.focus('gi_core_review',api.pay_pp(100)+f'\nEGY = {{ country_event = {{ id = {consultation} days = 30 }} }}',available=long_gate+' = yes\nEGY = { exists = yes }',
        description='After ten years of real ownership and control and five years of equal rights, pay 100 political power to open a separate local status process. An affirmative result is not guaranteed; rejection leaves civil rights intact and grants no core.')
    api.decision('egypt_status_proposal','Negotiate the Egyptian Sovereignty Settlement','Local acceptance is required before Egypt is asked to settle the sovereignty issue. Egypt may refuse.','gi_core_review',
        long_gate+' = yes\n'+has('local_status_accepted')+'\nEGY = { exists = yes } NOT = { '+has('egypt_status_accepted')+' }',f'EGY = {{ country_event = {{ id = {sovereignty} days = 30 }} }}',repeatable=True,cooldown=360)
    api.decision('renew_status_consultation','Renew the Sinai Status Consultation','After an unsuccessful status process, new talks may be opened. Repeated proposals never guarantee assent.','gi_core_review',
        long_gate+' = yes\nEGY = { exists = yes } NOT = { '+has('local_status_accepted')+' }',f'EGY = {{ country_event = {{ id = {consultation} days = 30 }} }}',cost=50,repeatable=True,cooldown=720)
    api.focus('gi_canal_core',api.pay_pp(150)+'\n'+api.money(.005)+f'\n{c} = {{ add_core_of = ISR }}\n'+flag('canal_integrated'),
        available=long_gate+' = yes\n'+has('local_status_accepted')+'\n'+has('egypt_status_accepted'),
        description='Pay 150 political power and 0.5% of GDP only after real local and Egyptian status agreements. The core applies solely to Sinai; ordinary core effects replace native occupation mechanics. Egyptian cores and historic claims remain.')

    road_after=scope(c,'add_dynamic_modifier = { modifier = '+road_local+' }')
    api.project('occ_security_roads',c,[{'type':'infrastructure','levels':1}],.008,180,after=road_after,available=has('occupation_special'))
    api.focus('occ_security_roads','unlock_decision_tooltip = ISR70_policy_project_occ_security_roads',available=has('occupation_special'),description='Fund 0.8% of GDP for one infrastructure level after 180 days. Secured roads add 15% local supplies but also 5% garrison need under the unequal statute.')
    delegated_event=api.event(414,'Delegated Administration under Unequal Law','Local administrators consider a limited administrative contract. Refusal grants Israel no administrative savings and does not require a further repressive policy.',[
        ('Accept the limited duties.','ISR = { '+flag('delegated_agreed')+' }','',1),
        ('Decline the contract.','ISR = { '+flag('delegated_declined')+' }','',5)],trigger='original_tag = EGY IMP_is_1970_scenario = yes ISR = { '+has('occupation_special')+' }')
    api.focus('occ_delegated_administration',f'EGY = {{ country_event = {{ id = {delegated_event} days = 7 }} }}',available=has('occupation_special')+'\nEGY = { exists = yes }',description='Request a limited local administrative contract. Only acceptance followed by funding grants the 3% bureaucracy saving and 3% corruption surcharge; refusal is possible.')
    api.decision('fund_delegated_administration','Fund the Accepted Delegated Administration','Spend 0.2% of GDP to implement the accepted duties.','occ_delegated_administration',
        has('occupation_special')+'\n'+has('delegated_agreed')+'\nNOT = { '+has('delegated_admin_active')+' }',api.money(.002)+'\nadd_ideas = '+delegated+'\n'+flag('delegated_admin_active'),repeatable=True)
    api.project('occ_occupation_industry',c,[{'type':'shared_slots','levels':1},{'type':'industrial_complex','levels':1}],.010,270,after=scope(c,'add_dynamic_modifier = { modifier = '+industry_local+' }'),available=has('occupation_special'))
    api.focus('occ_occupation_industry','unlock_decision_tooltip = ISR70_policy_project_occ_occupation_industry',available=has('occupation_special'),description='Reserve 1.0% of GDP for one building slot and one factory on contractually acquired land. Delivery takes 270 days and adds 5% local garrison need. A local administrative refusal does not block this distinct project.')
    statute_code='add_ideas = '+statute+'\n'+flag('permanent_statute_active')+'\n'+scope(c,'add_dynamic_modifier = { modifier = '+statute_local+' }')+'\n'+resistance(c,4,202001)
    api.focus('occ_permanent_statute',api.pay_pp(100)+'\n'+statute_code,
        available=has('occupation_special'),description='Pay 100 political power to make the unequal statute permanent. Add 5 points of factory access, 2% police costs and 4 resistance-target points; stability falls 2 points. It remains an occupation, with no core.')
    api.decision('reenact_permanent_statute','Re-enact the Permanent Occupation Statute','Following a legal-status change, a permanent statute requires a new 100-political-power enactment. Its old costs and bonuses cannot stack.','occ_permanent_statute',
        has('occupation_special')+'\nNOT = { '+has('permanent_statute_active')+' }',statute_code,cost=100,repeatable=True,cooldown=365)
    # Repeatable explicit changes replace the regime, not completed focuses.
    not_core=f'{c} = {{ is_controlled_by = ISR NOT = {{ is_core_of = ISR }} }}'
    reform_equal=api.effect('prepare_equal_reform',f'if = {{ limit = {{ has_completed_focus = {focus_id("gi_equal_status")} }} {activate_equal} = yes }} else = {{ {flag("reform_equal_authorized")} }}')
    reform_special=api.effect('prepare_special_reform',f'if = {{ limit = {{ has_completed_focus = {focus_id("occ_special_status")} }} {activate_special} = yes }} else = {{ {flag("reform_special_authorized")} }}')
    api.decision('reform_equal','Replace the Special Statute with Equal Rights','Pay 100 political power to repeal unequal law. If the civil-status focus has not yet been completed, it becomes available with its own cost. Otherwise the civil regime is reinstated directly. Physical projects and historic claims remain; no cooperation bonus is granted.','gi_resident_status',
        not_core+'\nOR = { '+has('occupation_special')+' '+has('kach_special')+' } NOT = { '+has('active_expulsion')+' }',reform_equal+' = yes',cost=100,repeatable=True,cooldown=365)
    api.decision('reform_special','Replace the Civil Reform with an Unequal Statute','Pay 100 political power to revoke the civil reform. Its rights clock and gains end; prior spending is not refunded. Revocation adds 5 resistance-target points for two years.','gi_resident_status',
        not_core+'\n'+has('equal_civil'),reform_special+' = yes',cost=100,repeatable=True,cooldown=365)
    api.decision('withdraw_status_reform','Withdraw the Pending Status Reform','Withdraw the authorisation before the new law takes effect. The current regime remains; the 100-political-power authorisation cost is not refunded.','gi_resident_status',
        'OR = { '+has('reform_equal_authorized')+' '+has('reform_special_authorized')+' }',clear('reform_equal_authorized')+'\n'+clear('reform_special_authorized'),repeatable=True,cooldown=30)

    api.tick.append(f'''if = {{ limit = {{ {c} = {{ is_owned_by = ISR is_controlled_by = ISR }} }}
if = {{ limit = {{ NOT = {{ {has('owned_since')} }} }} {flag('owned_since')} }}
}} else = {{ {clear('owned_since')} {clear('low_resistance_since')} }}
if = {{ limit = {{ {has('equal_civil')} {c} = {{ is_owned_by = ISR is_controlled_by = ISR }} }}
if = {{ limit = {{ NOT = {{ {has('equal_since')} }} }} {flag('equal_since')} }}
}} else = {{ {clear('equal_since')} }}
if = {{ limit = {{ {has('equal_civil')} {c} = {{ is_owned_by = ISR is_controlled_by = ISR resistance < 10.001 }} }}
if = {{ limit = {{ NOT = {{ {has('low_resistance_since')} }} }} {flag('low_resistance_since')} }}
}} else = {{ {clear('low_resistance_since')} }}''')
    # Reconcile both directions: loss suspends spending, recapture restores it.
    # A regime change still explicitly clears the underlying active flags.
    conditions={eq:has('equal_civil'),special:has('occupation_special'),kach:has('kach_special'),
        eq_council:has('equal_civil')+' has_completed_focus = ISR70_gi_canal_councils',
        delegated:has('occupation_special')+' '+has('delegated_admin_active'),
        statute:has('occupation_special')+' '+has('permanent_statute_active')}
    for key,condition in conditions.items():
        api.tick.append(f'if = {{ limit = {{ {c} = {{ is_controlled_by = ISR }} {condition} }} if = {{ limit = {{ NOT = {{ has_idea = {key} }} }} add_ideas = {key} }} }} else = {{ remove_ideas = {key} }}')
    api.data['policy_status_rules']={'state':c,'exclusive_flags':names,'core_trigger':long_gate,'resistance_ids':regime_resistance,'cleanup_effect':ident('clear_status'),'keep_harm_flags':['expulsion_damage'],'reforms_repeatable':True}

def build_radicals(api,nation,local,resistance,migration,parties,mandate,mandate_gate):
    """Government access does not silently choose expulsions or suspend elections."""
    def government(slot):return parties[slot]+' = yes'
    anyparty='OR = { '+government(1)+' '+government(0)+' '+government(21)+' }'
    api.focus('rad_government',api.pay_pp(75),available=anyparty,description='Pay 75 political power for a radical territorial programme only while its actual party governs. This neither wins an election nor enacts any of the later choices automatically.')
    api.focus('rad_herut_mandate',mandate+' = yes',available=government(1)+'\nhas_completed_focus = ISR70_p1_cb\n'+mandate_gate,description='Herut/Gahal adopts the shared territorial mandate after choosing Indivisible Security Interests. Pay its 100-political-power cost once, credited against the Greater Israel entry.')
    nation('rad_herut_authority',{'bureaucracy_cost_multiplier_modifier':.02},api.money(.004)+'\n'+local('herut_territorial_building',{'state_production_speed_infrastructure_factor':.10},213,government(1)),available=government(1)+'\n213 = { is_controlled_by = ISR }',text='Budget 0.4% of GDP for a territorial authority: local infrastructure construction +10%, bureaucracy costs +2%, only under the programme government.')
    nation('rad_herut_preparation',{'personnel_cost_multiplier_modifier':.03},api.money(.005)+'\narmy_experience = 30\n'+local('herut_supplies',{'local_supplies_for_controller':.10},213,government(1)),available=government(1),text='Budget 0.5% of GDP and +3% personnel costs for 30 army experience and 10% local supply support in the controlled Sinai. It is preparation, not a declaration of war.')
    api.focus('rad_herut_retention',flag('herut_retention')+'\nEGY = { '+api.opinion('herut_retention',-20,'ISR')+' }\nUSA = { '+api.opinion('herut_retention_usa',-15,'ISR')+' }',available=government(1),description='Reject territorial withdrawal as an explicit Herut policy. Egyptian relations fall 20, American relations 15. A later peace requires repeal; the focus does not annex a state.')
    api.focus('rad_mafdal_council',api.pay_pp(50)+'\n'+flag('mafdal_council'),available=government(0)+'\nhas_completed_focus = ISR70_p0_cb',description='After choosing Religious Settlement Policy, pay 50 political power for the religious settlement programme. The later land and legal-binding choices remain separate decisions.')
    migration('rad_mafdal_settlers',213,10000,3,.008)
    api.nodes[focus_id('rad_mafdal_settlers')]['available']+='\n'+government(0)+'\n'+has('project_gi_sinai_housing_done')
    api.focus('rad_mafdal_land',api.money(.004)+'\n'+scope(213,'add_extra_state_shared_building_slots = 1')+'\n'+resistance(213,8,203000)+'\n'+flag('mafdal_expropriation'),
        available=government(0)+'\n213 = { is_controlled_by = ISR }',description='Choose compulsory land expropriation instead of negotiated purchase: spend 0.4% of GDP for one building slot; local resistance target rises 8 points and property claims remain.')
    purchase=api.event(420,'A Negotiated Land Purchase','Local owners consider a land contract. Refusal transfers no land and pays out no new building slot.',[
        ('Accept the purchase terms.','ISR = { '+flag('mafdal_purchase_accepted')+' }','',2),
        ('Decline the sale.','ISR = { '+flag('mafdal_purchase_rejected')+' }','',3)],trigger='original_tag = EGY IMP_is_1970_scenario = yes')
    api.focus('rad_mafdal_purchase',f'EGY = {{ country_event = {{ id = {purchase} days = 7 }} }}',available=government(0)+'\nEGY = { exists = yes }',description='Seek a voluntary land purchase. Only accepted terms unlock the 1.0%-GDP, 270-day project for the same building slot. No expropriation or automatic resistance rise follows refusal.')
    api.project('mafdal_purchase',213,[{'type':'shared_slots','levels':1}],.010,270,available=government(0)+'\n'+has('mafdal_purchase_accepted'),unlock='rad_mafdal_purchase')
    api.focus('rad_mafdal_lock','add_political_power = 50\nadd_stability = -0.03\n'+flag('inalienable_land'),available=government(0),description='Make settlement land politically inalienable. Gain 50 political power once; stability falls 3 points, and later withdrawal requires a separate repeal. The alternative is a reviewable lease system.')
    nation('rad_mafdal_review',{'internal_investments_money_cost_modifier':-.05},api.pay_pp(50)+'\n'+api.money(.003),available=government(0),text='Choose reviewable land leases and a registry instead of inalienability. Pay 50 political power and 0.3% of GDP; internal investment costs fall 5%, and territorial negotiations remain available.')
    land_delivered='OR = { '+has('mafdal_expropriation')+' '+has('project_mafdal_purchase_done')+' }'
    for key in ('rad_mafdal_lock','rad_mafdal_review'):api.nodes[focus_id(key)]['available']+='\n'+land_delivered
    api.focus('rad_kach_government',api.pay_pp(100)+'\n'+flag('kach_government')+'\nEGY = { '+api.opinion('kach_government',-25,'ISR')+' }\nPAL = { '+api.opinion('kach_government',-25,'ISR')+' }\nJOR = { '+api.opinion('kach_government',-25,'ISR')+' }',available=government(21),description='Pay 100 political power for the governing National Front/Kach programme. Before 1971 it uses the existing National Front presentation. Relations with Egypt, PAL and Jordan fall 25; taking office does not automatically expel residents.')
    api.nodes[focus_id('rad_kach_government')]['label']='National Front: Radical Government Programme'
    api.focus('rad_denial','ISR70_policy_activate_kach = yes',available=government(21)+f'\n{SINAI} = {{ is_controlled_by = ISR NOT = {{ is_core_of = ISR }} }}',description='Explicitly deny equal civil status in controlled, non-core Sinai: +10 points of occupied factory access, +10% garrison need and +5% police costs. This replaces the general unequal statute and blocks the civic core route while active.')
    api.focus('rad_no_expulsion',api.money(.005)+'\n'+flag('residents_retained'),available=government(21)+'\n'+has('kach_special'),description='Keep residents and their economic activity under unequal administration, with 0.5% of GDP for basic services. No seized-property slots or additional expulsion penalties are awarded; the underlying unequal legal regime remains.')
    harms=api.idea('expulsion_damage','Consequences of Forced Displacement','Civilian displacement, lost homes and unresolved property claims continue after a change of government.',{'stability_factor':-.08})
    harm_local=api.state_modifier('expulsion_garrison','Forced Displacement and Unresolved Claims','Civilian harm and ongoing conflict are not erased by a new government.',{'required_garrison_factor':.20},enable='is_controlled_by = ISR ISR = { '+has('expulsion_damage')+' NOT = { '+has('property_claims_fulfilled')+' } }')
    sanctions=api.event(421,'Forced Displacement in Sinai','Israel has ordered forced displacement of Arab residents. Civilian homes, property, livelihoods and return claims are affected. The government may impose a real trade embargo or issue diplomatic condemnation.',[
        ('Impose a trade embargo.','send_embargo = ISR\n'+api.opinion('expulsion_condemnation',-50,'ISR'),'',4),
        ('Condemn the policy diplomatically.',api.opinion('expulsion_condemnation',-50,'ISR'),'',3)],trigger='IMP_is_1970_scenario = yes NOT = { original_tag = ISR } ISR = { '+has('expulsion_damage')+' }')
    api.focus('rad_expulsion',api.pay_pp(200)+'\n'+flag('active_expulsion')+'\n'+flag('expulsion_damage')+'\nadd_ideas = '+harms+'\n'+scope(SINAI,'add_extra_state_shared_building_slots = 2\nadd_dynamic_modifier = { modifier = '+harm_local+' }')+'\n'+resistance(SINAI,25,203001)+f'\nEGY = {{ country_event = {{ id = {sanctions} days = 1 }} }}\nPAL = {{ country_event = {{ id = {sanctions} days = 1 }} }}\nJOR = {{ country_event = {{ id = {sanctions} days = 1 }} }}\nUSA = {{ country_event = {{ id = {sanctions} days = 1 }} }}',
        available=government(21)+'\n'+has('kach_special')+f'\n{SINAI} = {{ is_controlled_by = ISR }}',description='An explicitly chosen, abstract forced-displacement policy. Pay 200 political power; at most two seized-property slots, stability -8 points, local resistance target +25 points and garrison need +20%. Refugees and property claims persist; other states receive actual embargo choices. No expulsion quota, population deletion, or core reward.')
    permanent=api.idea('permanent_emergency','Permanent Territorial Emergency','An explicitly chosen constitutional emergency suspends elections and raises enforcement and personnel costs.',{'police_cost_multiplier_modifier':.10,'personnel_cost_multiplier_modifier':.10})
    sunset=api.idea('electoral_sunset','Security Powers with an Electoral Sunset','Security powers last for 365 days and preserve the existing electoral framework.',{'police_cost_multiplier_modifier':.03})
    per_local=api.state_modifier('emergency_access','Permanent Emergency Administration','Additional occupied factory access during the emergency regime.',{'local_factories':.05},enable='is_controlled_by = ISR ISR = { '+has('kach_special')+' has_idea = '+permanent+' }')
    sun_local=api.state_modifier('sunset_access','Temporary Security Mandate','Additional occupied factory access only during the temporary mandate.',{'local_factories':.02},enable='is_controlled_by = ISR ISR = { '+has('kach_special')+' has_idea = '+sunset+' }')
    api.focus('rad_permanent_emergency','add_ideas = '+permanent+'\n'+flag('policy_suspended_elections')+'\nset_politics = { ruling_party = nationalist elections_allowed = no }\n'+scope(SINAI,'add_dynamic_modifier = { modifier = '+per_local+' }'),
        available=government(21)+'\n'+has('kach_special'),description='Choose a permanent emergency explicitly. Suspend elections, gain 5 further points of occupied factory access, and pay +10% police and +10% personnel costs. Neither party membership nor the population-policy choice enacts this automatically.')
    api.focus('rad_limited_emergency',api.pay_pp(50)+f'\nadd_timed_idea = {{ idea = {sunset} days = 365 }}\n'+scope(SINAI,'add_dynamic_modifier = { modifier = '+sun_local+' }'),available=government(21)+'\n'+has('kach_special'),description='Pay 50 political power for 365 days of +2 occupied factory-access points and +3% police costs. Elections are preserved. Renewal requires another paid government decision; the alternative is permanent emergency.')
    api.decision('renew_security_sunset','Renew the Temporary Security Mandate','Renew a lapsed 365-day mandate without suspending elections.','rad_limited_emergency',government(21)+'\n'+has('kach_special')+'\nNOT = { has_idea = '+sunset+' }',f'add_timed_idea = {{ idea = {sunset} days = 365 }}',cost=50,repeatable=True,cooldown=365)
    api.decision('end_expulsion','End the Forced-Displacement Policy','End the active policy explicitly. Civilian claims, economic harm and outstanding return obligations remain; equal rights and restitution require their own reforms.','rad_expulsion',has('active_expulsion'),clear_flag('active_expulsion'),cost=50)
    api.decision('repeal_inalienable_land','Repeal the Inalienable-Land Statute','Repeal the legal barrier before a territorial return can be implemented. Prior expropriation claims remain.','rad_mafdal_lock',has('inalienable_land'),clear_flag('inalienable_land'),cost=100)
    restore=[]
    for outlook in ('democratic','communism','neutrality','nationalist'):
        slots=[g['trigger']+' = yes' for g in api.data['groups'] if g['party'] is not None and ('democratic' if g['party']<4 else 'communism' if g['party']<10 else 'neutrality' if g['party']<20 else 'nationalist')==outlook]
        restore.append('if = { limit = { OR = { '+' '.join(slots)+' } } set_politics = { ruling_party = '+outlook+' elections_allowed = yes } }')
    restore_id=api.effect('restore_policy_elections','\n'.join(restore)+'\n'+clear_flag('policy_suspended_elections')+'\nremove_ideas = '+permanent)
    api.decision('restore_emergency_elections','Restore Elections after the Territorial Emergency','End the policy-imposed suspension explicitly. This restores elections within the current governing outlook; it does not install a new party or erase civilian claims.','rad_permanent_emergency',
        has('policy_suspended_elections'),restore_id+' = yes',cost=75,repeatable=True,cooldown=365)
    api.decision('reenact_permanent_emergency','Re-enact the Permanent Territorial Emergency','A returning government must explicitly re-enact the territorial emergency after its earlier suspension ended.','rad_permanent_emergency',
        government(21)+'\n'+has('kach_special')+'\nNOT = { '+has('policy_suspended_elections')+' }',
        'add_ideas = '+permanent+'\n'+flag('policy_suspended_elections')+'\nset_politics = { ruling_party = nationalist elections_allowed = no }',cost=75,repeatable=True,cooldown=365)
    for key,slot in (('rad_herut_authority',1),('rad_herut_preparation',1),('rad_mafdal_review',0)):
        iid=ident(key+'_idea')
        api.tick.append(f'if = {{ limit = {{ has_completed_focus = {focus_id(key)} {government(slot)} }} if = {{ limit = {{ NOT = {{ has_idea = {iid} }} }} add_ideas = {iid} }} }} else = {{ remove_ideas = {iid} }}')
    api.tick.append('if = { limit = { NOT = { '+government(21)+' } } remove_ideas = '+permanent+' remove_ideas = '+sunset+' }')
    api.tick.append('if = { limit = { '+has('policy_suspended_elections')+' NOT = { '+government(21)+' } } '+clear_flag('policy_suspended_elections')+' }')
    api.tick.append('if = { limit = { '+has('property_claims_fulfilled')+' '+has('expulsion_damage')+' } remove_ideas = '+harms+' '+scope(SINAI,'remove_resistance_target = 203001\nremove_dynamic_modifier = '+harm_local)+' }')

def clear_flag(key):return 'clr_country_flag = '+ident(key)

def finalize_factory_access(api):
    """One aggregate state bonus, with a real ceiling on total factory access."""
    names=['special_status_access','permanent_statute_access','kach_status_access','emergency_access','sunset_access']
    for name in names:api.dynamic[ident(name)][0].pop('local_factories',None)
    for name in names:
        full=ident(name)
        if api.dynamic[full][0]:continue
        del api.dynamic[full]
        import re
        def strip(code):
            code=re.sub(r'add_dynamic_modifier\s*=\s*\{\s*modifier\s*=\s*'+re.escape(full)+r'\s*\}','',code)
            return re.sub(r'remove_dynamic_modifier\s*=\s*'+re.escape(full)+r'\b','',code)
        api.effects={k:strip(code) for k,code in api.effects.items()}
        api.decisions=[strip(code) for code in api.decisions]
    key=api.state_modifier('factory_access','Occupied Factory Access','Additional access to existing factories, limited by the remaining room below 100%. It is not factory output or newly created industry.',
        {'local_factories':'ISR70_policy_access_applied'},enable='is_controlled_by = ISR ISR = { OR = { '+has('occupation_special')+' '+has('kach_special')+' } }')
    code=f'''{SINAI} = {{
set_variable = {{ ISR70_policy_access_wanted = 0 }}
if = {{ limit = {{ ISR = {{ {has('occupation_special')} }} }} set_variable = {{ ISR70_policy_access_wanted = 0.10 }}
if = {{ limit = {{ ISR = {{ {has('permanent_statute_active')} }} }} add_to_variable = {{ ISR70_policy_access_wanted = 0.05 }} }} }}
if = {{ limit = {{ ISR = {{ {has('kach_special')} }} }} set_variable = {{ ISR70_policy_access_wanted = 0.10 }}
if = {{ limit = {{ ISR = {{ has_idea = ISR70_policy_permanent_emergency }} }} add_to_variable = {{ ISR70_policy_access_wanted = 0.05 }} }}
else_if = {{ limit = {{ ISR = {{ has_idea = ISR70_policy_electoral_sunset }} }} add_to_variable = {{ ISR70_policy_access_wanted = 0.02 }} }} }}
set_variable = {{ ISR70_policy_access_room = 1 }}
subtract_from_variable = {{ ISR70_policy_access_room = modifier@local_factories }}
if = {{ limit = {{ has_dynamic_modifier = {{ modifier = {key} }} }} add_to_variable = {{ ISR70_policy_access_room = ISR70_policy_access_applied }} }}
clamp_variable = {{ var = ISR70_policy_access_room min = 0 max = ISR70_policy_access_wanted }}
set_variable = {{ ISR70_policy_access_applied = ISR70_policy_access_room }}
if = {{ limit = {{ is_controlled_by = ISR check_variable = {{ ISR70_policy_access_wanted > 0 }} }}
add_dynamic_modifier = {{ modifier = {key} }} }} else = {{ remove_dynamic_modifier = {key} clear_variable = ISR70_policy_access_applied }}
}}'''
    api.effect('update_factory_access',code)
    api.effects[ident('clear_status')]+='\n'+scope(SINAI,'remove_dynamic_modifier = '+key+'\nclear_variable = ISR70_policy_access_applied')
    for name in ('activate_special','activate_kach','complete_occ_permanent_statute','complete_rad_permanent_emergency','complete_rad_limited_emergency'):
        api.effects[ident(name)]+='\nISR70_policy_update_factory_access = yes'
    api.tick.append('ISR70_policy_update_factory_access = yes')
    api.data['policy_factory_access']={'state':SINAI,'modifier':key,'max_total':1.0,'normal_requested':.10,'permanent_requested':.15,'temporary_radical_requested':.12,'variable':'ISR70_policy_access_applied'}
