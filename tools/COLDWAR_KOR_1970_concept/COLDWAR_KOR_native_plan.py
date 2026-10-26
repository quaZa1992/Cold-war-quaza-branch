# IMPERIA CW — Cold War: declared native-code recipes for the uninstalled concept.
"""Keep existing engine/MD APIs distinct from new Korean content definitions."""
import re
P='COLDWAR_KOR_'

def declare(d):
    for index,c in enumerate(d['contracts'],1):
        c['recipient_event']='COLDWAR_KOR_foreign.'+str(index)
        c['proposer_reply_event']='COLDWAR_KOR_foreign.'+str(100+index)
        c['provider_ids']={kind:P+kind+'_'+c['key'] for kind in ('send','can_accept','accept','refuse','expire')}
        c['state_flags']={kind:P+c['key']+'_'+kind for kind in ('pending','signed','refused','expired')}
        c['ownership']='national agreement; continues across ordinary government changes' if c['key']!='northern_security_compact' else 'requires actual RPR government; terminate charges/benefits when that condition ends'
        c['payer_scopes']='Use explicit KOR scope for Korean payments/benefits and explicit recipient tag for its effects. Recipient event ROOT must never be mistaken for the Korean payer.'
        if c['key']=='sovereign_confederation':
            c['KOR_on_accept']={'add_ideas':P+'confederal_member'}
            c['recipient_effects']['add_ideas']=P+'confederal_member'
            c['membership_cleanup']='Remove membership idea in both countries on agreed dissolution or bilateral war. No passive stats belong to this membership receipt.'
        if c['key']=='confederal_secretariat':
            c['membership_requirements']={'KOR':'has_idea = '+P+'confederal_member','NKO':'has_idea = '+P+'confederal_member'}
            c['acceptance']+=' Both countries must still hold the actual confederal membership idea.'
    d['new_membership_ideas']={P+'confederal_member':{
      'label':'Korean Consultative Framework','modifiers':{},
      'grant':'Both countries, atomically, only on a signed sovereign framework or verified grandfathered legacy acceptance',
      'cleanup':'Both countries on dissolution/war; no unilateral founding focus grants it'}}
    d['NKO_compatibility_adapter']={
      'existing_sources':['common/scripted_effects/COLDWAR_NKO_1970_foreign.txt:831-909','common/decisions/COLDWAR_NKO_1970_foreign.txt:238-248','common/dynamic_modifiers/COLDWAR_NKO_1970_foreign.txt:80-98'],
      'existing_acceptance':'COLDWAR_NKO_korean_channel_confederation_offer_accepted must be present in both countries, not merely the offer-earned flag.',
      'old_to_new':'Grandfather genuinely signed existing channels/frameworks into the shared ledger and add the zero-stat membership receipt. Preserve their already accepted native payments, modifiers and upkeep; no recharge, free refund or duplicated KOR bonus.',
      'new_to_old':'NKO send/eligibility checks read shared pending/signature/membership OR genuine legacy acceptance. Do not manufacture the old acceptance flag on a new deal, because it can activate legacy reward consumers without their negotiated payment.',
      'new_project':'A new secretariat or civilian-trade project requires a separate accepted numeric contract; it is additional scope, not a second award for the existing framework.',
      'scope':'These are proposed narrowly scoped integration changes; no existing NKO agreement is altered during this concept phase.'}
    d['actions']['conditional_review']={
      'ids':['conditional_peninsula_review'],
      'design':'If secretariat or civilian trade signed, reveal joint ratification. Otherwise if conclusively refused/expired, add_political_power = 25; no membership, treaty or unification reward.'}
    d['actions']['party_guarantees']={
      'ids':['constitutional_party_guarantees'],
      'design':'Set civilian-party-settlement receipt and keep competitive-party rights in native politics; numerical benefit and cost are the associated focus policy, with no hidden grant.'}
    d['party_migration']['additional_router_fix']='Existing common/scripted_effects/KOR_political_leaders.txt installs Kim Jong-pil under ruling_party=14. The proposed 1970 router must route him through actual DRP/NDRP slot0 and preserve NACF slot14; do not copy the modern slot14 office gate.'
    d['political_entry_routes']=[
      {'id':P+'legalize_civic_parties','kind':'new domestic decision and government response','scope':'KOR only',
       'available':'Competitive civilian constitution OR a negotiated civilian opening; no nationwide martial law; existing lawful governing player authorizes legalization',
       'cost':'50 political power; 90d political adjustment: political power gain -5%',
       'effect':'Record legal participation for student civic slot5 and independent left slot19. No automatic popularity or appointment. Actual native election/coalition result must put the party in office before its programme opens.'},
      {'id':P+'ratify_revolutionary_transition','kind':'new response to a native revolutionary/electoral transition','scope':'KOR only',
       'available':'A native resolved regime transition has actually selected slot4; or a legalized slot4 party wins through the existing political system. An underground network or Northern offer alone is insufficient.',
       'cost':'90d transition burden: stability -8%, factory output -5%; no industrial or diplomatic gift',
       'effect':'Set revolutionary-settlement receipt, use native change_ruling_party_effect with target4 only after the actual transition; dispatch a historical Southern revolutionary cabinet from the new 1970 pool. Northern material support still requires a signed contract.'},
      {'id':P+'ratify_security_directorate','kind':'new exceptional emergency-cabinet decision','scope':'KOR only',
       'available':'Unresolved presidential succession crisis; stability below30%; current government explicitly accepts a security caretaker; no existing civilian settlement ratification',
       'cost':'100 political power; stability -5%; 180d caretaker burden: trade opinion -5%, police expenses +5%',
       'effect':'Set security-directorate receipt. Use native change_ruling_party_effect target7, elections disabled, existing actual support unchanged; create/select the new KCIA caretaker pool in the 1970 router. Party-array slot7 now actually governs. This is labelled alternate history and cannot trigger from coalition backing alone.'},
      {'id':P+'native_party_accession','kind':'existing native election/coalition result plus new KOR leader dispatcher',
       'scope':'KOR only','available':'Real native political result for slots0,1,2,3 or22',
       'cost':'Native politics costs; no duplicate accession fee',
       'effect':'Use current change_ruling_party_effect inputs; update actual incumbent and exact-party programmes. Preserve completed national development and party vote totals.'},
    ]
    native_party_code='''# Existing MD API; target and election settings supplied by the resolved political result.
set_temp_variable = { rul_party_temp = TARGET_SLOT }
set_temp_variable = { disable_elections = ELECTIONS_DISABLED }
change_ruling_party_effect = yes
# This existing helper calls set_leader; the NEW COLDWAR_KOR_1970_set_leader
# early dispatcher must therefore exist before integration. Never call the
# unmodified modern KOR pool and hope it chooses the proposed 1970 incumbent.'''
    d['native_party_change_recipe']=native_party_code
    d['new_helpers']={
      P+'1970_set_leader':'New early country dispatcher inside set_leader. Respects actual selection, never rerolls Park at initialization. Pools: Park/KJP0, NDP1, both reform Kims2 with separate incumbent, Kim Chul3, RPR4, civic5, security7, independent left19, Chun/Roh22. Choi interim office gets its actual caretaker state before an election; it does not pretend to be a normal party victory.',
      P+'refresh_programmes':'New idempotent recomputation: reset sums, select latest earned policy per qualified slot, include only current actual owner and constitutional settlement, include signed active contract modifiers, update dynamic modifier once. No treasury, buildings, XP or PP writes.',
      P+'calculate_weekly_cost':'New single aggregation of active expense_commitment slots and accepted contract charges. Native calculate_additional_expense_rate calls this and adds its result to additional_expenses_rate; accepted recipient income uses a matching additional_income_rate reader. Never subtract cash directly on a monthly or GUI refresh.',
      P+'sync_politics':'New KOR hook from native exact-party change helper, KOR office dispatcher and on-load/monthly failsafe; calls refresh, does not set party or office itself.',
      P+'offer_dispatch':'New bounded offer sender with per-pair pending lock,60d deadline, sender office/country snapshot and no payment. Recipient options show each exact payer and benefit.',
      P+'offer_accept':'New revalidated transaction; charge and grant once, mark signed membership or relation and ledger receipt, clear pending, notify proposer. Existing NKO-side offers map to the same ledger.',
      P+'offer_refuse':'New final refusal/expiry receipt with no charge or agreement modifier; clear pending and start180d renegotiation cooldown; treaty-only follow-ups bypass without reward.',
    }
    d['new_helpers'][P+'refresh_programmes']+=' Explicitly remove inactive party/leader dynamic modifiers, retain earned variables and re-add only the returning active owner’s modifier. Enable guards are a second safeguard; the hook must detect exact-party changes within the same broad outlook.'
    if d.get('transition_maintenance_recipe'):
        d['new_helpers'][P+'sync_politics']+=' Also run the declared transition_maintenance_recipe to resume already funded court commissioning after constitutional restoration; never charge or appoint a ruler there.'
    d['rights_followup_decision']={
      'id':P+'review_repression_cases','availability':'Competitive civilian settlement, independent court or oversight, no nationwide martial law',
      'cost':'75 political power and $1bn once','effect':'Adjudicate cases and compensate victims. Reduce national martial-law legitimacy scar from stability -8%, trade opinion -5%, police expenses +8% to stability -3%, bureaucracy expenses +4%; no historical memory erasure.',
      'historicity':'Earlier independent accountability is alternate history; the1995–96 trials are not claimed to occur before1990.'}
    sources={
      'drp':['https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_i500300','https://www.adb.org/publications/saemaul-undong-movement-republic-korea'],
      'ndp':['https://theme.archives.go.kr/next/vote/outline/lineOut01.do'],
      'reform':['https://contents.history.go.kr/front/hm/view.do?levelId=hm_151_0060'],
      'army':['https://theme.archives.go.kr/next/vote/outline/lineOut01.do','https://encykorea.aks.ac.kr/Article/E0042141'],
      'usp':['https://encykorea.aks.ac.kr/Article/E0075798'],
      'minjung':['https://press.umich.edu/Books/R/Revisiting-Minjung','https://contents.history.go.kr/front/hm/view.do?levelId=hm_160_0020&tabId=01&treeId=020308'],
      'rpr':['research_history.md — underground revolutionary organizations; full governing route is alternate history'],
      'security':['research_history.md — KCIA institutions and1979 crisis; governing directorate is alternate history'],
      'economy':['https://www.kdi.re.kr/eng/research/reportView?pub_no=99','https://documents1.worldbank.org/curated/en/477601468914114162/pdf/Analysis-synthesis-and-recommendations.pdf'],
      'defence':['https://history.state.gov/historicaldocuments/frus1969-76v19p1/d58'],
      'foreign':['https://history.state.gov/historicaldocuments/frus1969-76v19p1/d157','https://www.odakorea.go.kr/kor/cont/ContShow?cont_seq=25'],
      'korea':['https://peacemaker.un.org/en/node/9000','https://theme.archives.go.kr/next/unikorea/seven/seven01.do'],
      'kjp':['research_history.md — Kim Jong-pil/NDRP and1990 coalition; presidential office is alternate history'],
      'transition':['research_democratic_transition_expansion.md','https://www.law.go.kr/lsInfoP.do?lsiSeq=61603&viewCls=engLsInfoR','https://museum.nec.go.kr/eng/eexh/eexh_1987_12_16.html'],
    }
    for g in d['groups']:g['historical_sources']=sources[g['id']]
    for n in d['nodes']:n['historical_sources']=sources[n['group']]
    d['gate_definitions']={}
    byid={n['id']:n for n in d['nodes']}
    for n in d['nodes']:
        base=['original_tag = KOR','IMP_is_1970_scenario = yes','is_subject = no']
        group=n['group'];owner=n['ownership'];slot=None
        if group=='minjung' and owner!='national':slot=5 if owner=='party:5' else 19
        else:
            g=next(g for g in d['groups'] if g['id']==group);slot=g['party']
        if slot is not None:base.append(f'check_variable = {{ ruling_party = {slot} }}')
        if owner.startswith('leader:'):base.append('has_country_leader = { name = "'+owner[7:]+'" ruling_only = yes }')
        if group=='security':base.append('has_country_flag = '+P+'security_directorate_ratified')
        if group=='rpr':base.append('has_country_flag = '+P+'revolutionary_settlement')
        if group=='minjung' and slot is not None:base.append('has_country_flag = '+P+'civic_legal_'+str(slot))
        if n['key']=='yushin':base.append('has_country_flag = '+P+'constitutional_crisis')
        if n['key'] in ('emergency_decrees','dynastic_presidency'):
            base.append('has_country_flag = '+P+'constitution_yushin')
        if n['key']=='press_consolidation':base.append('has_country_flag = '+P+'constitution_controlled_fifth')
        if n['key']=='roh_nordpolitik':base.append('has_elections = yes')
        base.extend(n.get('condition_code',[]))
        for a in n['effects']['actions']:
            if a['type']=='condition' and a['value'].startswith('accepted '):
                condition=a['value'][9:]
                if ' OR ' in condition:
                    base.append('OR = { '+' '.join('has_country_flag = '+P+c+'_signed' for c in condition.split(' OR '))+' }')
                else:base.append('has_country_flag = '+P+condition+'_signed')
        if n['key']=='confederal_secretariat':
            base += ['has_idea = '+P+'confederal_member','NKO = { has_idea = '+P+'confederal_member }']
        for b in n['effects']['buildings']:
            base.append(str(b['state'])+' = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = '+b['type']+' size > '+str(b['level']-1)+' include_locked = no } }')
        # Native bypass is independent of completion/reward guards. A recorded
        # refusal cannot satisfy the signed-treaty reward condition.
        bypass=n.get('bypass',{})
        if isinstance(bypass,dict) and bypass.get('native_pattern'):
            import re
            contract=re.search(P+r'(\w+)_refused',bypass['native_pattern']).group(1)
            senders=[x['id'] for x in d['nodes'] if any(a['type']=='offer' and a['value']==contract for a in x['effects']['actions'])]
            assert senders,(n['id'],contract,'missing dispatch')
            dispatch='OR = { '+' '.join('has_completed_focus = '+x for x in senders)+' }'
            n['native_bypass_body']='\n'.join(['original_tag = KOR','IMP_is_1970_scenario = yes',dispatch,
              'NOT = { has_country_flag = '+P+contract+'_signed }',bypass['native_pattern']])
        n['proposed_trigger']=P+'can_'+n['key']
        n['native_gate_body']='\n'.join(base)
        n['native_completion_guard']=n['native_gate_body']+'\nNOT = { has_country_flag = '+n['id']+'_paid }'
        # Native code below represents proposed NEW content definitions, not an
        # assertion that any COLDWAR_KOR helper is already installed.
        d['gate_definitions'][n['proposed_trigger']]={'status':'NEW proposed scripted trigger','body':n['native_gate_body'],'additional_conditions':n.get('requirements',[])}
        leaf=[]
        if n['effects']['cost']:
            leaf+=['set_temp_variable = { treasury_change = -'+str(n['effects']['cost']).removesuffix('.0')+' }','modify_treasury_effect = yes']
        for b in n['effects']['buildings']:
            leaf += [str(b['state'])+' = { add_building_construction = { type = '+b['type']+' level = '+str(b['level'])+' instant_build = yes } }']
        for kind,value in n['effects']['one_time'].items():
            k={'xp':'army_experience','pp_once':'add_political_power','stability':'add_stability','war_support':'add_war_support'}[kind]
            leaf.append(k+' = '+str(value).removesuffix('.0'))
        for policy in n['effects']['policies']:
            prefix=n['id']+'_'+policy['slot']
            for key,value in policy['modifiers'].items():leaf.append('set_variable = { '+prefix+'_'+key+' = '+str(value)+' }')
        leaf.extend(n.get('state_effects',[]))
        if n.get('temporary_effect'):
            t=n['temporary_effect'];leaf.append('add_timed_idea = { idea = '+t['id']+' days = '+str(t['days'])+' }')
        n['native_leaf_effects']='\n'.join(leaf)
        n['native_reward_design_note']='Policy records above need the declared latest-slot selector and mapped dynamic modifier. Writing a variable alone does not apply a modifier. New action/contract handlers are separately declared; their names are not existing MD APIs.'
        if any('civilian_factories_productivity' in p['modifiers'] for p in n['effects']['policies']):
            n['economic_effect_note']='Civilian industry productivity changes the civilian-industrial tax base and its contribution to GDP. The national result depends on industry and employment; it is not a military-production bonus.'
    d['native_examples']={
      'nonaggression_accept':'diplomatic_relation = { country = NKO relation = non_aggression_pact active = yes }',
      'national_policy_dynamic':'COLDWAR_KOR_national_programme = { enable = { original_tag = KOR IMP_is_1970_scenario = yes } civilian_factories_productivity = COLDWAR_KOR_active_civ_productivity stability_factor = COLDWAR_KOR_active_stab }',
      'park_programme_dynamic':'COLDWAR_KOR_park_programme = { enable = { original_tag = KOR check_variable = { ruling_party = 0 } has_country_leader = { name = "Park Chung Hee" ruling_only = yes } } political_power_factor = COLDWAR_KOR_park_pp stability_factor = COLDWAR_KOR_park_stab }',
      'modifier_refresh':'add_dynamic_modifier = { modifier = COLDWAR_KOR_park_programme }\nforce_update_dynamic_modifier = yes',
      'weekly_reader_addition':'COLDWAR_KOR_calculate_weekly_cost = yes\nadd_to_variable = { additional_expenses_rate = COLDWAR_KOR_weekly_cost }',
    }
    d['native_api_evidence']={
      'change_ruling_party_effect':'common/scripted_effects/00_MD_politicsview_scripted_effects.txt:1980-2085; inputs rul_party_temp, disable_elections; optional col_one..col_five and change_leader_temp',
      'money':'common/scripted_effects/00_budget_effects.txt:1484-1498; modify_treasury_effect requires treasury_change in billions',
      'diplomatic_relation':'HOI4 documentation/effects_documentation.md:3564; MD common/national_focus/05_russia.txt:18890-18893 uses non_aggression_pact',
      'construction':'HOI4 documentation/effects_documentation.md:839; native KOR paid projects; state scope plus current slots/ownership checked twice',
      'dynamic':'HOI4 documentation/effects_documentation.md:4372; target generic/VIE/SOV ownership patterns',
    }
    return d
