# IMPERIA CW — Cold War: focus-owned Syrian institutions and essential RP choices.
"""Pure design/output transforms; never writes loaded files."""
from pathlib import Path
from copy import deepcopy
import json,re
from build_content import FORMAT

HERE=Path(__file__).resolve().parent
P='COLDWAR_SYR_'
REVISION='focus_owned_20261021'
MIGRATION=P+'migrate_streamlining_20261021'
HEADER='# IMPERIA CW — Cold War: Syrian focus-owned reforms and essential agreements.\n'
AUTO={'soviet_training','development_credit','friendship_treaty','gulf_project','pipeline','federation','golan','joint_plan','lebanon','iran_oil','funded_project','iraq_transit','gulf_finance','war_egypt','war_warning','war_mediation'}
KEEP={'succession_crisis','kurdish_coalition','drought','unrest_mediation','security_response','national_pact','governing_mandate',
      'choose_conservative_leader','choose_communist_leader','choose_nasserist_leader','choose_brotherhood_leader',
      'form_political_bureau','form_saadeddin_leadership','form_safwan_leadership','form_faisal_faction','withdraw_rights_coalition',
      'regional_withdrawal','authorize_mission','hard_currency','war_window','war_goal_armistice','war_credit','war_demobilize','war_appropriation'}

def parse(source):return FORMAT.read(source)
def first(rows,key,default=None):return next((v for k,o,v in rows if k==key),default)
def values(rows,key):return [v for k,o,v in rows if k==key]
def walk(rows):
    for row in rows:
        yield row
        if isinstance(row[2],list):yield from walk(row[2])
def emit(rows):
    return '\n'.join(k if o is None else k+' '+o+' '+('{\n'+emit(v)+'\n}' if isinstance(v,list) else str(v)) for k,o,v in rows)
def block(key,code):return key+' = {\n'+code+'\n}\n'
def flag(key):return 'has_country_flag = '+P+key
def setflag(key):return 'set_country_flag = '+P+key
def timed(key,days):return f'add_timed_idea = {{ idea = {P+key} days = {days} }}'
def short(d):return d['id'].removeprefix(P+'decision_')

# Funded by the existing focus appropriation; no new hard Treasury gate or
# second service invoice is introduced. Legacy conversion only restores flags.
LOCAL={
 'opening_military':('Secures an officer compact for the negotiated Corrective programme.','if = { limit = { NOT = { check_variable = { COLDWAR_SYR_officer_backing > 1 } } } set_variable = { COLDWAR_SYR_officer_backing = 2 } }',''),
 'opening_civilian':('Enacts the civilian command compact while preserving the incumbent presidency and governing mandate.','set_country_flag = COLDWAR_SYR_cabinet_consent\nset_country_flag = COLDWAR_SYR_dual_command_resolved',''),
 'opening_corrective':('Ratifies the officer–cabinet transfer agreement. The Transitional People’s Council focus appoints the acting president.','set_country_flag = COLDWAR_SYR_cabinet_consent\nset_country_flag = COLDWAR_SYR_dual_command_resolved\nset_country_flag = COLDWAR_SYR_corrective_transition',''),
 'industry_03':('Completes the public-enterprise investigations required for procurement reform.','set_variable = { COLDWAR_SYR_enterprise_audits = 3 }\nset_country_flag = COLDWAR_SYR_enterprise_audits_completed',timed('politics_enterprise_audit',90)),
 'fiscal_02':('Completes the contract investigations required for procurement reform.','set_variable = { COLDWAR_SYR_enterprise_audits = 3 }\nset_country_flag = COLDWAR_SYR_enterprise_audits_completed',''),
 'agriculture_06':('Funds reservoir resettlement and clears the community-settlement requirement for the Tabqa works.','set_country_flag = COLDWAR_SYR_reservoir_resettlement_completed',timed('politics_resettlement_burden',180)),
 'agriculture_10':('Completes the funded irrigation and drainage trials required for water-management reform.','set_variable = { COLDWAR_SYR_irrigation_trials = 3 }\nset_country_flag = COLDWAR_SYR_irrigation_trials_completed',''),
 'citizenship_01':('Enacts the land-tenure review and reopens the citizenship registers.','set_country_flag = COLDWAR_SYR_land_settlement_decided\nset_country_flag = COLDWAR_SYR_tenure_review\nset_country_flag = COLDWAR_SYR_reopen_citizenship_review',''),
 'citizenship_02':('Enacts the restrictive settlement policy. Political exclusion and its domestic crisis remain real costs.','set_country_flag = COLDWAR_SYR_land_settlement_decided\nset_country_flag = COLDWAR_SYR_discriminatory_settlement\nset_country_flag = COLDWAR_SYR_internal_crisis','add_ideas = COLDWAR_SYR_politics_exclusion\n'+timed('politics_security_control',180)),
 'citizenship_03':('Completes citizenship appeals, implements their decisions and ends the discriminatory settlement restrictions.','set_country_flag = COLDWAR_SYR_appeals_commission_open\nset_variable = { COLDWAR_SYR_citizenship_stages = 3 }\nset_country_flag = COLDWAR_SYR_citizenship_review_completed\nclr_country_flag = COLDWAR_SYR_discriminatory_settlement\nremove_ideas = COLDWAR_SYR_politics_exclusion',''),
 'citizenship_04':('Completes the register examination and opens a controlled appeals process.','set_country_flag = COLDWAR_SYR_appeals_commission_open\nset_variable = { COLDWAR_SYR_citizenship_stages = 3 }\nset_country_flag = COLDWAR_SYR_citizenship_review_completed',''),
 'citizenship_09':('Ends discriminatory settlement restrictions and arbitrary land seizures.','clr_country_flag = COLDWAR_SYR_discriminatory_settlement\nremove_ideas = COLDWAR_SYR_politics_exclusion',''),
 'qudsi_06':('Reopens the registers and implements a completed citizenship appeals programme.','set_country_flag = COLDWAR_SYR_reopen_citizenship_review\nset_country_flag = COLDWAR_SYR_appeals_commission_open\nset_variable = { COLDWAR_SYR_citizenship_stages = 3 }\nset_country_flag = COLDWAR_SYR_citizenship_review_completed\nclr_country_flag = COLDWAR_SYR_discriminatory_settlement\nremove_ideas = COLDWAR_SYR_politics_exclusion',''),
 'rifaat_03':('Enacts the guard-command settlement.','clr_country_flag = COLDWAR_SYR_rival_guard_commands\nset_country_flag = COLDWAR_SYR_guard_settlement',''),
 'parliament_05':('Ratifies legal opposition and competitive elections through the national constitutional pact.','COLDWAR_SYR_accept_national_pact = yes',timed('politics_transition_burden',180)),
 'military_council_09':('Ratifies the civilian constitution and permits competitive elections. The electorate determines the next government.','COLDWAR_SYR_accept_national_pact = yes\nset_country_flag = COLDWAR_SYR_military_transfer_agreed',timed('politics_command_disruption',180)),
 'limited_war_entry':('Enacts the Golan staff appropriation for one year.','set_country_flag = COLDWAR_SYR_war_budget_submitted','set_temp_variable = { treasury_change = gdp_total }\nmultiply_temp_variable = { treasury_change = -0.0075 }\nmodify_treasury_effect = yes\nset_country_flag = { flag = COLDWAR_SYR_operations_funded days = 365 }'),
 'limited_war_reserves':('Establishes trained reserve formations with continuing personnel commitments.','',''),
 'limited_war_depots':('Establishes permanent forward supply services with continuing personnel commitments.','',''),
 'limited_war_sustainment':('Establishes forward medical services with continuing healthcare commitments.','',''),
 'fiscal_13':('Activates the funded household-relief programme for 180 days.','','remove_ideas = COLDWAR_SYR_politics_restraint\n'+timed('politics_targeted_relief',180)),
 'fiscal_14':('Enacts subsidy restraint for 180 days.','','remove_ideas = COLDWAR_SYR_politics_targeted_relief\n'+timed('politics_restraint',180)),
 'limited_war_appropriation':('Authorises the funded Golan operations programme.','set_country_flag = COLDWAR_SYR_operational_mandate\nclr_country_flag = COLDWAR_SYR_defensive_brief','set_country_flag = { flag = COLDWAR_SYR_operations_funded days = 365 }'),
 'limited_war_review':('Completes the campaign review. Withdrawal remains a deliberate wartime decision.','set_country_flag = COLDWAR_SYR_campaign_review_completed',''),
}

def augment(data,baseline):
    from politics import material_option_preview
    patches=json.loads((HERE/'streamlining_rewards.json').read_text(encoding='utf-8'))
    for n in data['nodes']:
        n['streamline_previous_modifiers']=deepcopy(baseline['nodes'][n['id']]['modifiers'])
        patch=patches.get(n['id'])
        if patch:
            n['modifiers']=deepcopy(patch['modifiers']);n['description']=patch['description'];n['streamlining_reference']=patch['reference']
            n['one_time']+=deepcopy(patch.get('one_time',[]))
        k=n['id'].removeprefix(P)
        # The formerly separate $2bn officer bargain is the focus's own charge.
        if k=='opening_military':n['treasury_cost_bn']=2
        # Preparations must survive the long staff branch. Replace short-lived
        # click packages with real standing services and their recurring burdens.
        standing={
          'limited_war_reserves':{'conscription_factor':.025,'army_org_factor':.04,'army_personnel_cost_multiplier_modifier':.035,'industrial_capacity_factory':-.03},
          'limited_war_depots':{'supply_consumption_factor':-.05,'army_fuel_consumption_factor':-.025,'army_personnel_cost_multiplier_modifier':.02},
          'limited_war_sustainment':{'army_fuel_consumption_factor':-.02,'army_morale_factor':.04,'army_org_factor':.02,'health_cost_multiplier_modifier':.04},
        }
        if k in standing:n['modifiers']=standing[k]
        descriptions={
          'limited_war_reserves': 'Reserve districts must be able to assemble trained formations rather than produce impressive lists of names. Permanent training cadres, maintained equipment and prepared assembly points will improve readiness well beyond a single exercise. These units will require continuing pay, while their mobilisation obligations draw skilled workers away from industrial production.',
          'limited_war_depots': 'Dispersed depots need more than a temporary allocation of stores. Trained distribution teams, maintained transport and accountable stock records can reduce the waste of fuel and supplies throughout the army. Those savings depend on retaining experienced personnel and paying for a standing supply service after the first preparations are complete.',
          'limited_war_sustainment': 'The forward echelons must be able to recover their wounded and return exhausted formations to service. Military clinics, trained orderlies and coordinated transport can support that endurance while reducing wasteful fuel movements. Maintaining this capability creates a continuing healthcare commitment that the national budget must carry alongside the army’s readiness.',
        }
        if k in descriptions:n['description']=descriptions[k]
        if k in LOCAL:
            text,permanent,temporary=LOCAL[k]
            n['focus_owned_effect']=permanent+'\n'+temporary
            n['focus_owned_preview']='custom_effect_tooltip = '+n['id']+'_enactment_tt\n'+material_option_preview(permanent+'\n'+temporary)
            n['focus_owned_text']=text
            if k=='limited_war_entry':n['available']+='\nhidden_trigger = { check_variable = { gdp_total > 0 } }'
        # Replace confirmations, retaining the actual Golan war-goal helper.
        for item in n['one_time']:
            item['code']=re.sub(r'country_event\s*=\s*\{\s*id\s*=\s*COLDWAR_SYR_WAR\.(?:1|2|3|10)\s+days\s*=\s*1\s*\}','',item['code'])
        n['one_time']=[item for item in n['one_time'] if item['code'].strip()]
        n['streamline_changed']=bool(patch or k in LOCAL)
    for d in data['decisions']:d['streamlining_mode']='automatic_offer' if short(d) in AUTO else 'retained' if short(d) in KEEP or short(d).startswith(('campaign_','coalition_')) else 'removed'
    data['streamlining_revision']=REVISION

def option_payload(option):
    return [r for r in option if r[0] not in ['name','trigger','ai_chance','custom_effect_tooltip','effect_tooltip']]

def transform(outputs,data):
    result=dict(outputs);loc={};by={n['id']:n for n in data['nodes']}
    def output(path,rows):result[path]=HEADER+FORMAT.format_script(emit(rows))
    def L(key,value):loc[key]=value
    event_paths=['events/COLDWAR_SYR_politics_events.txt','events/COLDWAR_SYR_foreign_events.txt']
    event_asts={p:parse(result[p]) for p in event_paths}
    events={first(v,'id'):v for ast in event_asts.values() for v in values(ast,'country_event')}
    decision_paths=['common/decisions/COLDWAR_SYR_politics_decisions.txt','common/decisions/COLDWAR_SYR_foreign_decisions.txt']
    asts={p:parse(result[p]) for p in decision_paths}
    definitions={k:v for a in asts.values() for _,_,cat in a if isinstance(cat,list) for k,_,v in cat if isinstance(v,list)}
    before_count=len(definitions)
    original_decisions={d['id']:d for d in data['decisions']}
    helpers=[]
    def strip_dispatch_receipt(rows,ident):
        result=[]
        for k,o,v in rows:
            if k in ['has_country_flag','set_country_flag'] and v==ident+'_completed':continue
            nested=strip_dispatch_receipt(v,ident) if isinstance(v,list) else v
            if isinstance(nested,list) and (not nested or k=='custom_trigger_tooltip' and all(a=='tooltip' for a,_,_ in nested)):continue
            result.append((k,o,nested))
        return result
    def helper(name,gate,code):
        helpers.extend(parse(block(P+name,block('if',block('limit',gate)+code))))
        return P+name+' = yes'
    # Reuse original live success guards and original recipient dispatch; the old
    # preparation failure/refund branch must never mint PP from a free focus.
    offer_calls={};retry_options=[];retry_gates=[]
    for name in sorted(AUTO):
        ident=P+'decision_'+name;d=definitions[ident]
        expiry=first(d,'remove_effect',[])
        success=first(expiry,'if')
        assert success is not None,('Missing guarded offer',ident)
        gate=strip_dispatch_receipt(first(success,'limit',[]),ident)
        actual=strip_dispatch_receipt([r for r in success if r[0]!='limit'],ident)
        if name=='friendship_treaty':gate+=parse('NOT = { has_country_flag = COLDWAR_SYR_friendship_treaty }')
        call=helper('offer_'+name,emit(gate),'COLDWAR_SYR_update_operation_costs = yes\n'+emit(actual))
        offer_calls[ident]=call
        retry_options.append(('option','=',[('name','=',P+'retry_'+name),('trigger','=',gate),('hidden_effect','=',parse(call))]))
        retry_gates.append(('AND','=',gate))
        label=original_decisions[ident]['label'];L(P+'retry_'+name,label)
        L(P+'offer_'+name+'_tt','Opens negotiations: '+label+'. The other government decides whether to accept.')
    # Effects tied to successful focus delivery are not replayed by refresh.
    rewards_path='common/scripted_effects/COLDWAR_SYR_focus_rewards.txt'
    rewards=parse(result[rewards_path])
    for n in data['nodes']:
        offers=[offer_calls[d['id']] for d in data['decisions'] if d['id'] in offer_calls and (d.get('unlock')==n['id'] or n['id'] in d.get('unlock_any',[]))]
        if offers:
            first(first(rewards,n['id']+'_implement'),'if').extend(parse('\n'.join(offers)))
        if n.get('focus_owned_text'):L(n['id']+'_enactment_tt',n['focus_owned_text'])
    output(rewards_path,rewards)
    # Direct Front institution; both eligible historical partners are invited
    # into the existing domestic coalition, without replacing its leading party.
    front=[]
    for slot in [4,13]:
        front.append(block('if',block('limit',f'check_variable = {{ party_pop_array^{slot} > 0.04999 }} NOT = {{ is_in_array = {{ gov_coalition_array = {slot} }} }}')+f'set_variable = {{ party_banned_array^{slot} = 0 }}\nset_temp_variable = {{ add_col_one = {slot} }}\nadd_coalition_members_effect = yes'))
    frontcall=helper('enact_front','original_tag = SYR IMP_is_1970_scenario = yes check_variable = { ruling_party = 7 }','\n'.join(front)+'\nupdate_dirty_politicsview_expanded = yes')
    first(first(rewards,P+'baath_02_implement'),'if').extend(parse(frontcall));output(rewards_path,rewards)
    L(P+'baath_02_enactment_tt','Admits the Communist and Arab Socialist Union parties to the governing Front if each has at least 5% support. The Baath retains government.')
    by[P+'baath_02']['focus_owned_preview']='custom_effect_tooltip = '+P+'baath_02_enactment_tt'
    # Menu-free domestic crisis mediation; the decision keeps its real timing/cost.
    inline_events={
        'COLDWAR_SYR_POL.8':option_payload(values(events['COLDWAR_SYR_POL.8'],'option')[0]),
        'COLDWAR_SYR_WAR.9':[],
        'COLDWAR_SYR_WAR.14':parse('clr_country_flag = COLDWAR_SYR_training_request_pending'),
        'COLDWAR_SYR_WAR.12':parse('COLDWAR_SYR_clear_campaign_effects = yes'),
    }
    # The Egyptian player already accepted a Syrian request; execute the promised
    # Syrian contribution through its original checks instead of a second popup.
    ev=events['COLDWAR_SYR_WAR.5']
    funding=next(o for o in values(ev,'option') if any(k=='modify_treasury_effect' for k,_,_ in walk(option_payload(o))))
    inline_events['COLDWAR_SYR_WAR.5']=first(ev,'immediate',[])+[('if','=',[('limit','=',first(funding,'trigger',[]))]+option_payload(funding))]
    # Operational doctrine is already chosen by mutually exclusive focuses.
    window=[]
    for option in values(events['COLDWAR_SYR_WAR.6'],'option'):
        if not any(k=='add_timed_idea' for k,_,_ in walk(option_payload(option))):continue
        window.append(('if','=',[('limit','=',first(option,'trigger',[]))]+option_payload(option)))
    inline_events['COLDWAR_SYR_WAR.6']=window
    def inline(rows):
        result=[]
        for k,o,v in rows:
            if k=='country_event' and isinstance(v,list) and first(v,'id') in inline_events:result.extend(deepcopy(inline_events[first(v,'id')]))
            else:result.append((k,o,inline(v) if isinstance(v,list) else v))
        return result
    # Keep only real choices. Campaigns and coalition talks each get one shared
    # entry; individual options retain the authority of their original outlook.
    polcat=first(asts[decision_paths[0]],P+'politics_category')
    for kind,start in [('campaign',20),('coalition',24)]:
        names=[P+'decision_'+kind+'_'+x for x in ['western','emerging','nonaligned','nationalist']]
        guards=[];options=[]
        for index,name in enumerate(names):
            d=definitions[name];gate=first(d,'available',[]);guards.append(('AND','=',gate))
            for option in values(events[f'COLDWAR_SYR_POL.{start+index}'],'option'):
                if not any(k in ['change_relative_party_popularity','add_coalition_members_effect'] for k,_,_ in walk(option)):continue
                option=deepcopy(option)
                trigger=first(option,'trigger')
                if trigger is None:option.append(('trigger','=',deepcopy(gate)))
                else:trigger.extend(deepcopy(gate))
                options.append(('option','=',option))
        number=90 if kind=='campaign' else 91;eid=f'COLDWAR_SYR_POL.{number}'
        events[eid]=[('id','=',eid),('title','=',eid+'.t'),('desc','=',eid+'.d'),('is_triggered_only','=','yes'),('trigger','=',parse('original_tag = SYR IMP_is_1970_scenario = yes'))]+options+[('option','=',[('name','=',P+'close_consultations')])]
        event_asts[event_paths[0]].append(('country_event','=',events[eid]))
        d=deepcopy(definitions[names[0]])
        d[:]=[(k,o,[('OR','=',deepcopy(guards))] if k in ['visible','available'] else parse('country_event = { id = '+eid+' days = 1 }') if k=='remove_effect' else v) for k,o,v in d]
        canonical=P+'decision_'+kind+'_politics';polcat.append((canonical,'=',d));KEEP.add(kind+'_politics')
        L(canonical,'Organize a Political Campaign' if kind=='campaign' else 'Negotiate Cabinet Representation')
        L(canonical+'_desc','Support a legal party through its funded organising campaign.' if kind=='campaign' else 'Agree cabinet representation with a legal party holding at least 5% support. The incumbent retains government.')
        L(eid+'.t','Political Organising' if kind=='campaign' else 'Cabinet Representation')
        L(eid+'.d','The cabinet must select the political organisation it intends to support. Only parties with the required legal standing can participate.')
    for a in asts.values():
        for _,_,category in a:
            if isinstance(category,list):category[:]=[(k,o,v) for k,o,v in category if k.removeprefix(P+'decision_') in KEEP or k.startswith(P+'counterparty_') or k in ['COLDWAR_SYR_lebanon_revoke','COLDWAR_SYR_iraq_pipeline_withdraw']]
    # Preserve the recipient-owned withdrawal entries by their real namespace.
    original_counter=first(parse(outputs[decision_paths[1]]),P+'counterparty_dossier',[])
    for i,(k,o,v) in enumerate(asts[decision_paths[1]]):
        if k==P+'counterparty_dossier':asts[decision_paths[1]][i]=(k,o,original_counter)
    retry_id=P+'decision_reopen_negotiations';retry_event='COLDWAR_SYR_FOREIGN.90'
    retry=[('icon','=','GFX_decision_generic_political_discourse'),('cost','=','0'),('visible','=',[('OR','=',retry_gates)]),('available','=',parse('original_tag = SYR IMP_is_1970_scenario = yes')),('complete_effect','=',parse('country_event = { id = '+retry_event+' }'))]
    first(asts[decision_paths[1]],P+'foreign_dossier').append((retry_id,'=',retry))
    retrybody=[('id','=',retry_event),('title','=',retry_event+'.t'),('desc','=',retry_event+'.d'),('is_triggered_only','=','yes'),('trigger','=',parse('original_tag = SYR IMP_is_1970_scenario = yes'))]+retry_options+[('option','=',[('name','=',P+'close_consultations')])]
    event_asts[event_paths[1]].append(('country_event','=',retrybody));events[retry_event]=retrybody
    L(retry_id,'Reopen Diplomatic Negotiations');L(retry_id+'_desc','Return to an unresolved offer. Every commitment still requires the other government’s response; reopening consultations charges no political fee.')
    L(retry_event+'.t','Outstanding Diplomatic Proposals');L(retry_event+'.d','The foreign ministry can renew a proposal when circumstances permit. Each government retains control of its response.')
    L(P+'close_consultations','Close the consultations.')
    for path,ast in asts.items():output(path,inline(ast))
    # A campaign may start years after staff training or resume after an
    # armistice. One real budget decision renews expired funding and authorises
    # a valid campaign, crediting any still-live appropriation automatically.
    foreign_cat=first(asts[decision_paths[1]],P+'foreign_dossier')
    budget=first(foreign_cat,P+'decision_war_appropriation')
    authority='original_tag = SYR IMP_is_1970_scenario = yes\n'+flag('limited_war_entry_implemented')+'\nCOLDWAR_SYR_campaign_is_valid = yes\nNOT = { '+flag('operational_mandate')+' }\ncheck_variable = { gdp_total > 0 }'
    debit='set_temp_variable = { treasury_change = gdp_total }\nmultiply_temp_variable = { treasury_change = -0.0075 }\nmodify_treasury_effect = yes'
    action=block('if',block('limit','NOT = { '+flag('operations_funded')+' }')+debit+'\nset_country_flag = { flag = COLDWAR_SYR_operations_funded days = 365 }')+setflag('operational_mandate')
    budget_preview='custom_effect_tooltip = COLDWAR_SYR_renew_budget_tt\n'+block('effect_tooltip',block('if',block('limit',block('hidden_trigger','NOT = { '+flag('operations_funded')+' }'))+debit))
    budget_actual=block('hidden_effect',block('if',block('limit',authority)+action)+block('else','add_political_power = '+str(first(budget,'cost'))))
    for index,(k,o,v) in enumerate(budget):
        if k=='available':budget[index]=(k,o,parse(block('hidden_trigger','original_tag = SYR IMP_is_1970_scenario = yes\n'+flag('limited_war_entry_implemented')+'\ncheck_variable = { gdp_total > 0 }')+block('custom_trigger_tooltip','tooltip = COLDWAR_SYR_operational_cabinet_requirement_tt\nCOLDWAR_SYR_campaign_is_valid = yes\nNOT = { '+flag('operational_mandate')+' }')))
        elif k=='visible':budget[index]=(k,o,parse(flag('limited_war_entry_implemented')))
        elif k=='remove_effect':budget[index]=(k,o,parse(budget_preview+budget_actual))
    L(P+'decision_war_appropriation','Convene the Operational Cabinet')
    L(P+'decision_war_appropriation_desc','Activate a valid Golan campaign under the prepared staff programme. A still-valid appropriation is credited; renewing an expired budget costs 0.75% of current annual GDP. This authorization does not declare war.')
    L(P+'renew_budget_tt','Authorises the operational mandate. Renews the budget for one year if it has expired; an existing funded appropriation is not charged again.')
    L(P+'operational_cabinet_requirement_tt','The Golan objective remains unresolved, a war or war goal against Israel is active, and the operational mandate has not yet been authorised.')
    L(P+'operational_cabinet_requirement_tt_NOT','The Golan objective, war status or existing operational mandate prevents a new cabinet authorisation.')
    output(decision_paths[1],inline(asts[decision_paths[1]]))
    # Normal focus and deferred-delivery tooltips advertise only extant actions.
    retained={k for ast in asts.values() for _,_,cat in ast if isinstance(cat,list) for k,_,v in cat if isinstance(v,list)}
    def previews(rows):
        result=[]
        for k,o,v in rows:
            if k=='unlock_decision_tooltip' and v not in retained:
                name=v.removeprefix(P+'decision_')
                if name in AUTO:result.append(('custom_effect_tooltip','=',P+'offer_'+name+'_tt'))
                elif name.startswith(('campaign_','coalition_')):result.append((k,o,P+'decision_'+name.split('_')[0]+'_politics'))
                continue
            result.append((k,o,previews(v) if isinstance(v,list) else v))
        return result
    for path in ['common/national_focus/COLDWAR_SYR_1970_focus.txt','common/decisions/COLDWAR_SYR_deferred_projects.txt',rewards_path]:output(path,previews(inline(parse(result[path]))))
    # Front's institution is appended after compilation, with an explicit preview.
    for path in ['common/national_focus/COLDWAR_SYR_1970_focus.txt','common/decisions/COLDWAR_SYR_deferred_projects.txt']:
        ast=parse(result[path])
        for k,o,v in walk(ast):
            if k=='focus' and isinstance(v,list) and first(v,'id')==P+'baath_02':first(first(v,'completion_reward'),'effect_tooltip').append(('custom_effect_tooltip','=',P+'baath_02_enactment_tt'))
            if k==P+'baath_02_resume':first(first(v,'complete_effect'),'effect_tooltip').append(('custom_effect_tooltip','=',P+'baath_02_enactment_tt'))
        output(path,ast)
    # Once-only saved-variable deltas. No construction, training, cash, foreign
    # dispatch, timed programme or leader installation occurs during recovery.
    migration=[]
    for n in data['nodes']:
        if not n.get('streamline_changed'):continue
        old=n['streamline_previous_modifiers'];new=n['modifiers'];body=[]
        for mod in sorted(old.keys()|new.keys()):
            diff=round(new.get(mod,0)-old.get(mod,0),5)
            if diff:body.append(f'add_to_variable = {{ {n["owner"]}_{mod} = {diff:g} }}')
        # Safe completed domestic work is credited. Political office/mandate,
        # timed campaign activation and fresh coalition choices are not replayed.
        key=n['id'].removeprefix(P)
        if key in LOCAL and key not in ['limited_war_entry','limited_war_appropriation','citizenship_02']:
            body.append(LOCAL[key][1])
        if key=='baath_02':body.append(block('if',block('limit','check_variable = { ruling_party = 7 }')+frontcall))
        replaced={'limited_war_reserves':'war_reserve_readiness','limited_war_depots':'war_supply_preparation','limited_war_sustainment':'war_medical_service'}
        if key in replaced:body.append('remove_ideas = '+P+replaced[key])
        body.append('set_country_flag = '+n['id']+'_streamlined_20261021')
        migration.append(block('if',block('limit','has_country_flag = '+n['id']+'_implemented\nNOT = { has_country_flag = '+n['id']+'_streamlined_20261021 }')+'\n'.join(body)))
    # Formerly empty entry groups can acquire newly introduced keys in old saves.
    initialize=[]
    for var in sorted({n['owner']+'_'+m for n in data['nodes'] for m in n['modifiers']}):initialize.append(block('if',block('limit','NOT = { has_variable = '+var+' }')+'set_variable = { '+var+' = 0 }'))
    helpers.extend(parse(block(MIGRATION,block('if',block('limit','original_tag = SYR IMP_is_1970_scenario = yes')+'\n'.join(initialize+migration)))))
    output('common/scripted_effects/COLDWAR_SYR_focus_owned_reforms.txt',helpers)
    # Expiry callbacks do their actual cleanup invisibly; event menus with only
    # acknowledgements are not a player decision.
    hidden=0
    for path,ast in event_asts.items():
        for event in values(ast,'country_event'):
            eid=first(event,'id');opts=values(event,'option')
            is_expiry=eid.startswith('COLDWAR_SYR_FOREIGN.') and int(eid.split('.')[1])>=100
            if (is_expiry or eid in ['COLDWAR_SYR_WAR.11','COLDWAR_SYR_POL.11','COLDWAR_SYR_POL.12']) and opts:
                action=option_payload(opts[0]);event[:]=[r for r in event if r[0] not in ['option','hidden']]
                event.append(('hidden','=','yes'));immediate=first(event,'immediate')
                if immediate is None:event.append(('immediate','=',action))
                else:immediate.extend(action)
                event.append(('option','=',[('name','=',P+'close_consultations')]))
                hidden+=1
        event_asts[path]=inline(ast)
    # Remove every unreachable event after following the retained callback graph.
    all_events={first(v,'id'):v for a in event_asts.values() for v in values(a,'country_event')}
    def refs(rows):return {first(v,'id') for k,_,v in walk(rows) if k=='country_event' and isinstance(v,list) and first(v,'id') in all_events}
    roots=[]
    for path,source in result.items():
        if path.endswith('.txt') and path not in event_paths:roots+=parse(source)
    keep=refs(roots);queue=list(keep)
    while queue:
        more=refs(all_events[queue.pop()])-keep;keep|=more;queue+=list(more)
    for path,ast in event_asts.items():output(path,[r for r in ast if r[0]!='country_event' or first(r[2],'id') in keep])
    # Generated metadata is used by the faithful preview too. Index only actual
    # installed actions, including consolidated ones, never deleted catalogue IDs.
    data['removed_decisions']=[d['id'] for d in data['decisions'] if d['streamlining_mode']=='removed']
    native_loc={}
    for path,source in result.items():
        if path.endswith('.yml'):
            for ident,text in re.findall(r'^\s*([^\s:]+):\d*\s+(".*")\s*$',source,re.M):native_loc[ident]=json.loads(text)
    native_loc.update(loc)
    current=[]
    for ast in asts.values():
        for _,_,category in ast:
            if not isinstance(category,list):continue
            for ident,_,body in category:
                if not isinstance(body,list):continue
                metadata=deepcopy(original_decisions.get(ident,{'id':ident,'unlock':'START'}))
                metadata.update(label=native_loc.get(ident,ident),effects=native_loc.get(ident+'_desc',''),note='',political_power_cost=int(first(body,'cost','0')),duration_days=int(first(body,'days_remove','0')),cooldown_days=int(first(body,'days_re_enable','0')),repeatable=True,streamlining_mode='retained')
                if ident in [P+'decision_campaign_politics',P+'decision_coalition_politics']:
                    kind='campaign' if 'campaign_' in ident else 'coalition'
                    metadata['unlock_any']=[d['unlock'] for d in original_decisions.values() if short(d).startswith(kind+'_')]
                if ident==retry_id:metadata['unlock_any']=list(dict.fromkeys(d['unlock'] for d in original_decisions.values() if short(d) in AUTO))
                current.append(metadata)
    data['decisions']=current
    labels={'agricolture_productivity_modifier':'Agricultural Productivity','civilian_factories_productivity':'Civilian Factory Productivity','offices_productivity':'Office Productivity','industrial_capacity_factory':'Military Factory Output','production_factory_efficiency_gain_factor':'Production Efficiency Growth','max_dig_in':'Maximum Entrenchment','army_morale_factor':'Army Recovery Rate','army_personnel_cost_multiplier_modifier':'Army Personnel Expenditure','health_cost_multiplier_modifier':'Healthcare Expenditure','social_cost_multiplier_modifier':'Social Expenditure','education_cost_multiplier_modifier':'Education Expenditure','bureaucracy_cost_multiplier_modifier':'Administrative Expenditure','tax_gain_multiplier_modifier':'Tax Revenue','agriculture_district_income_tax_modifier':'Agricultural Tax Revenue','foreign_influence_defense_modifier':'Foreign Influence Defence','equipment_upgrade_xp_cost':'Equipment Upgrade Experience Cost'}
    changed_mods=set(json.loads((HERE/'streamlining_rewards.json').read_text(encoding='utf-8')))|{P+x for x in ['limited_war_reserves','limited_war_depots','limited_war_sustainment']}
    for n in data['nodes']:
        if n['id'] in changed_mods:
            rows=[]
            for mod,value in n['modifiers'].items():
                caption=labels.get(mod,mod.removesuffix('_modifier').removesuffix('_factor').replace('_',' ').title())
                amount=value if mod in ['max_dig_in','political_power_gain','interest_rate_multiplier_modifier'] else value*100
                unit=' percentage points' if mod=='interest_rate_multiplier_modifier' else '' if mod in ['max_dig_in','political_power_gain'] else '%'
                rows.append(caption+': '+f'{amount:+g}'+unit)
            rows+=[item['summary'] for item in n['one_time']]
        else:
            rows=[s for s in n['reward_summary'] if not s.startswith(('Unlocks decision:','One-time treasury cost:','Event:')) and 'Convenes the new Syrian War Cabinet event' not in s and 'Opens campaign review:' not in s and 'Records the funded campaign mandate' not in s]
        if n['treasury_cost_bn']:rows.append(f'One-time Treasury Cost: ${n["treasury_cost_bn"]:g} billion.')
        if n.get('focus_owned_text'):rows.append(n['focus_owned_text'])
        if n['id']==P+'limited_war_entry':rows.append('Operations appropriation: 0.75% of current annual GDP, once.')
        for d in original_decisions.values():
            if d.get('unlock')!=n['id'] and n['id'] not in d.get('unlock_any',[]):continue
            if short(d) in AUTO:rows.append('Diplomatic proposal: '+d['label'])
            elif d['id'] in retained:rows.append('Decision: '+native_loc.get(d['id'],d['label']))
            elif short(d).startswith(('campaign_','coalition_')):rows.append('Decision: '+native_loc[P+'decision_'+short(d).split('_')[0]+'_politics'])
        n['reward_summary']=list(dict.fromkeys(rows))
        n['decision_unlocks']=[] # populated from the actual compiled preview below
    focus_ast=first(parse(result['common/national_focus/COLDWAR_SYR_1970_focus.txt']),'focus_tree')
    for f in values(focus_ast,'focus'):by[first(f,'id')]['decision_unlocks']=[v for k,_,v in walk(first(f,'completion_reward',[])) if k=='unlock_decision_tooltip']
    # Update existing names in their owning file; duplicate localisation keys
    # otherwise leave the loaded title dependent on file ordering.
    additions=dict(loc)
    for path,source in list(result.items()):
        if not path.endswith('.yml'):continue
        existing=set(re.findall(r'^\s*([^\s:]+):\d*\s+"',source,re.M))
        for ident in existing & additions.keys():
            source=re.sub(r'(?m)^\s*'+re.escape(ident)+r':\d*\s+".*"\s*$',lambda _: ' '+ident+':0 '+json.dumps(loc[ident],ensure_ascii=False),source)
            del additions[ident]
        result[path]=source
    result['localisation/english/COLDWAR_SYR_focus_owned_reforms_l_english.yml']='l_english:\n'+HEADER+'\n'.join(' '+k+':0 '+json.dumps(v,ensure_ascii=False) for k,v in additions.items())+'\n'
    return result,{'decisions_before_including_counterparties':before_count,'decisions_after_including_counterparties':sum(len(v) for a in asts.values() for _,_,v in a if isinstance(v,list)),'events_before':len(events)-3,'events_after':len(keep),'hidden_cleanup_events':sum(first(all_events[k],'hidden')=='yes' for k in keep),'retained_events':sorted(keep),'automatic_offers':sorted(AUTO),'revised_reward_focuses':len(json.loads((HERE/'streamlining_rewards.json').read_text(encoding='utf-8')))+3,'focus_count':len(data['nodes'])}
