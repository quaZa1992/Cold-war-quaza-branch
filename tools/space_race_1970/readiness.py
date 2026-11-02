# IMPERIA CW — Cold War: visible mission qualification and actual modifier accounting.
from mission_rules import REQUIREMENTS, qualified
from technology_integration import FAMILIES,PILOTS,description as technology_description,requirement_parts
from risk_rules import profile as risk_profile,findings as risk_findings


# IMPERIA COLD WAR — International operational cooperation.
def definitions(c):
    loc,cv,var=c['loc'],c['cv'],c['var'];programmes=c['PROGRAMMES'];ids=c['IDS'];out=''
    def define(name,entries,fallback):
        nonlocal out
        out+='defined_text = { name = '+name+'\n'+''.join('text = { trigger = { '+condition+' } localization_key = '+key+' }\n' for condition,key in entries)+'text = { localization_key = '+fallback+' } }\n'
    def receipt(name,condition,label):
        define(name,[(condition,loc(name+'_met','§GMET§!  '+label))],loc(name+'_missing','§RMISSING§!  '+label))
    def cap_key(capability):return capability.replace('-','_')
    for capability in sorted({k for p in programmes for k in p['capabilityRequirements']}):
        receipt('CW_SR_Check_'+cap_key(capability),'has_country_flag = cw_sr_cap_'+cap_key(capability),capability.replace('-',' ').title())
    all_groups=sorted({group for groups in REQUIREMENTS.values() for group in groups})
    groups={group:i for i,group in enumerate(all_groups,1)}
    for group,i in groups.items():
        label=' OR '.join(programmes[ids[item]-1]['name'] for item in group)
        history='OR = { '+' '.join('has_country_flag = cw_sr_heritage_'+str(ids[item]) for item in group)+' }'
        define('CW_SR_Qualification_'+str(i),[(history,loc('cw_sr_qualification_history_'+str(i),'§GMET§!  '+label+' (established before 1970)')),(qualified(group,ids),loc('cw_sr_qualification_met_'+str(i),'§GMET§!  '+label))],loc('cw_sr_qualification_missing_'+str(i),'§RMISSING§!  '+label))
    for family,count in FAMILIES.items():
        define('CW_SR_Known_'+family,[(cv('cw_sr_tech_'+family,'=',i),loc('cw_sr_known_'+family+str(i),family+' '+str((1975 if family=='KILLSAT' else 1955)+10*i))) for i in range(1,count+1)],loc('cw_sr_not_researched','Not researched'))
    loc('cw_sr_research_access_tt','Established national space administration or a completed national space project.')
    loc('cw_sr_weapons_access_tt','Qualified orbital reconnaissance and OLV 1975, or a completed space-weapons project.')
    selected=[];rewards=[];hardware=[];risks=[]
    for n,p in enumerate(programmes,1):
        receipt('CW_SR_Date_'+str(n),f'date > {p["minYear"]-1}.12.31','Programme available from '+str(p['minYear']))
        receipt('CW_SR_Tech_'+str(n),f'cw_sr_p{n}_technology = yes','Researched flight hardware (see Research & hardware)')
        research_lines=[]
        for j,(label,condition) in enumerate(requirement_parts(p),1):
            name=f'CW_SR_Tech_{n}_{j}';receipt(name,condition,label);research_lines.append('['+name+']')
        if not research_lines:research_lines=[technology_description(p)+'.']
        # IMPERIA COLD WAR — Qualified missions do not consume a new development place.
        qualified_hardware='OR = { '+' '.join(cv(var(n,'state'),'=',value) for value in [3,4,5,6])+f' has_country_flag = cw_sr_institution_{n}'+' }'
        capacity='OR = { '+cv('cw_sr_active','<',3)+' '+cv(var(n,'state'),'=',1)+' }'
        define('CW_SR_Capacity_'+str(n),[(qualified_hardware,loc('cw_sr_capacity_not_needed','§GMET§!  No additional development place required')),(capacity,loc('cw_sr_capacity_free','§GMET§!  Development capacity available (maximum 3 programmes)'))],loc('cw_sr_capacity_full','§RMISSING§!  Development capacity available (maximum 3 programmes)'))
        # IMPERIA COLD WAR — The treasury check uses the agreed national share.
        from crew import eligible as crew_eligible, funds as crew_funds
        # IMPERIA COLD WAR — Present the same signed operational launch gates.
        from cooperation import eligible as op_eligible, funds as op_funds
        receipt('CW_SR_Funds_'+str(n),op_funds(c,n,p) if op_eligible(p) else (crew_funds(c,n,p) if crew_eligible(p) else cv('treasury','>=',p['missionCostB'])),'National departure appropriation: see International operations' if op_eligible(p) else f'Mission appropriation: ${p["missionCostB"]:.2f}bn')
        if crew_eligible(p):receipt('CW_SR_Crew_'+str(n),f'cw_sr_p{n}_crew_ready = yes','Guest consent, joint training and contributions cleared')
        if op_eligible(p):receipt('CW_SR_Operations_'+str(n),f'cw_sr_p{n}_operations_ready = yes','Operational partner approval, qualification and funds cleared')
        receipt('CW_SR_Debt_'+str(n),cv(var(n,'arrears'),'<',.001),'No unpaid programme operating costs')
        receipt('CW_SR_Hardware_'+str(n),'OR = { '+' '.join(cv(var(n,'state'),'=',s) for s in [3,4,5])+' }','Hardware development and qualification completed')
        receipt('CW_SR_Review_'+str(n),cv(var(n,'im'),'<',.001),'No unresolved accident investigation')
        window=''
        if p.get('windowCycleMonths'):
            receipt('CW_SR_Window_'+str(n),cv('global.cw_sr_window_'+p['region'],'<',p['windowOpenMonths']),'Transfer opportunity open')
            window='\n[CW_SR_Window_'+str(n)+']'
        elif 'fixedWindowStartMonth' in p:
            receipt('CW_SR_Window_'+str(n),'date > 1984.11.30 date < 1985.1.1','December 1984 launch opportunity')
            window='\n[CW_SR_Window_'+str(n)+']'
        lines=['§HREQUIRED RESEARCH§!']+research_lines+['','§HNATIONAL CAPABILITIES§!','[CW_SR_Date_'+str(n)+']','[CW_SR_Capacity_'+str(n)+']']
        lines+=['[CW_SR_Check_'+cap_key(k)+']' for k in p['capabilityRequirements']]
        if not p['capabilityRequirements']:lines+=['No prior national capabilities required.']
        lines+=['','§HSUCCESSFUL PRECURSOR MISSIONS§!']
        if p['id'] in REQUIREMENTS:lines+=['[CW_SR_Qualification_'+str(groups[group])+']' for group in REQUIREMENTS[p['id']]]
        else:lines+=['No additional precursor flight required.']
        lines+=['','§HBEFORE MISSION AUTHORISATION§!','[CW_SR_Hardware_'+str(n)+']','[CW_SR_Funds_'+str(n)+']','[CW_SR_Debt_'+str(n)+']','[CW_SR_Review_'+str(n)+']'+window,'','Development can run alongside research and precursor flights.','Departure requires the research and successful qualifications.']
        # IMPERIA COLD WAR — Expose the real crew readiness gate.
        if crew_eligible(p):lines.insert(-2,'[CW_SR_Crew_'+str(n)+']')
        if op_eligible(p):lines.insert(-2,'[CW_SR_Operations_'+str(n)+']');lines.remove('Development can run alongside research and precursor flights.')
        key=loc('cw_sr_checklist_'+str(n),'\n'.join(lines));selected.append((cv('cw_sr_selected','=',n),key))
        r=p['rewardEffects']
        text=f'First success: §H+[?cw_sr_view_first_prestige|2] prestige§!, §H+{r["researchPoints"]} research data§!, §H+{r["politicalCapital"]} political power§!.\n'
        if r['researchPoints']>=4:text+='§H10% research bonus§! for one technology in any field.\n'
        if p['id'] in PILOTS:text+='One pilot satellite enters the existing orbital network, subject to capacity.\n'
        text+='\nAccepted capability: '+', '.join(k.replace('-',' ').title() for k in p['grants'])+'.\n\n[CW_SR_AwardState_'+str(n)+']'
        define('CW_SR_AwardState_'+str(n),[('has_country_flag = cw_sr_p'+str(n)+'_awarded',loc('cw_sr_award_received','First-success awards already received. Further missions provide limited prestige and flight experience.'))],loc('cw_sr_award_available','First-success awards remain available. Qualifying world firsts provide additional awards.'))
        # IMPERIA COLD WAR — Selected crew view supplies the actual national share.
        if crew_eligible(p) or op_eligible(p):text=f'National share: [?cw_sr_crew_host_percent|0]%.\nFirst success: §G+[?cw_sr_crew_host_prestige|2] prestige§!, §G+[?cw_sr_crew_host_science|2] research data§!, §G+[?cw_sr_crew_host_pp|2] political power§!.\n'+('§G[?cw_sr_crew_host_bonus|0]% research bonus§! for one technology in any field.\n' if r['researchPoints']>=4 else '')+'\n[CW_SR_AwardState_'+str(n)+']'
        rewards.append((cv('cw_sr_selected','=',n),loc('cw_sr_visible_rewards_'+str(n),text)))
        info='§HREQUIRED RESEARCH BEFORE DEPARTURE§!\n'+technology_description(p)+'.\n[CW_SR_Tech_'+str(n)+']\n\n§HNATIONAL HARDWARE GENERATIONS§!\n'+'\n'.join(label+': [CW_SR_Known_'+family+']' for family,label in [('OLV','Launch vehicles'),('GNSS','Navigation satellites'),('COMSAT','Communications satellites'),('SPYSAT','Observation satellites'),('KILLSAT','Anti-satellite systems')])+'\n\n§HTECHNOLOGY AND FLIGHT QUALIFICATION§!\nResearch unlocks hardware. Funded programmes and successful precursor missions establish operational qualification. Research alone provides no satellites or mission awards.\n\nEach launch-vehicle generation above the requirement adds +0.5 pp departure chance, up to +2 pp. Relevant satellite generations add +0.5 pp objective chance, up to +2 pp. Values are fixed at departure.\n\n'
        if p['id'] in PILOTS:info+='The first successful campaign commissions one pilot satellite through the national orbital network. Further launches, replacement, capacity and network operating charges remain under existing orbital management. Programme costs finance the pilot campaign; they do not grant a constellation.'
        else:info+='Satellite resources remain unchanged. Orbital observation, communications and navigation provide services without increasing raw-material production.'
        hardware.append((cv('cw_sr_selected','=',n),loc('cw_sr_hardware_'+str(n),info)))
        r=risk_profile(p)
        for kind,stage in [('partial',9),('failure',10),('catastrophic',11)]:
            launch_finding='A launch-vehicle propulsion, staging or guidance failure prevented orbital insertion.'
            define(f'CW_SR_Finding_{n}_{stage}',[(cv(var(n,'phase'),'=',0),loc(f'cw_sr_finding_launch_{n}_{stage}',launch_finding))],loc(f'cw_sr_finding_{n}_{stage}',risk_findings(p,kind)))
        risk_text='§HPRINCIPAL HAZARDS§!\n'+r['hazards']+'\n\n[CW_SR_RiskEstimate]\n'
        if not p.get('commissioningOnly'):
            risk_text+=f'\n§HCONTAINED FLIGHT ANOMALY§!\n[?cw_sr_view_risk_anomaly|2]% per departed flight; at most one.\nDelay: +{r["delay"]} days. Supplementary services: ${r["cost"]:.3f}bn.\nUnpaid invoices remain programme arrears. Recovery operations do not by themselves decide the final result.\n\n'
        risk_text+='§HUNSUCCESSFUL ATTEMPTS§!\nSafe launch abort: 1-month funded inspection.\nPartial results: 3-month funded review.\nMission failure: 6-month funded investigation.\nCatastrophe: 12-month funded investigation.\nReview funding is separate from a replacement mission.\nNo full rewards or flight qualification for an aborted or unsuccessful mission.\n\n[CW_SR_FrozenNote]'
        if p.get('commissioningOnly'):risk_text=risk_text.replace('Safe launch abort: 1-month funded inspection.\n','')
        risks.append((cv('cw_sr_selected','=',n),loc('cw_sr_risks_'+str(n),risk_text)))
    define('CW_SR_Selected_Checklist',selected,'cw_sr_checklist_47')
    define('CW_SR_VisibleRewards',rewards,'cw_sr_visible_rewards_47')
    define('CW_SR_Selected_Hardware',hardware,'cw_sr_hardware_47')
    define('CW_SR_Selected_Risks',risks,'cw_sr_risks_47')
    define('CW_SR_RiskEstimate',[(cv('cw_sr_view_state','=',4)+' '+cv('cw_sr_view_risk_recorded','=',0),loc('cw_sr_risk_legacy','This flight retains its original safety rules. No retrospective risk estimate is available.'))],loc('cw_sr_risk_estimate','§HESTIMATED EXPOSURE PER ATTEMPT§!\nCatastrophic hardware loss: [?cw_sr_view_risk_loss|2]%.\nCrew-loss probability: [?cw_sr_view_risk_crew|2]%.\nThese outcomes are already included in the full-success estimate.\nAny required crew return is part of the objective stage.'))
    define('CW_SR_NationalLeader',[('has_country_flag = cw_sr_leader',loc('cw_sr_national_leader_active','§GSpace leadership active§!\nMission objective chance: +2 percentage points.\nWeekly operating costs: -5%.'))],loc('cw_sr_national_leader_inactive','No space leadership bonus is active.\nBecome the sole prestige leader to receive +2 pp objective chance and -5% weekly operating costs.'))
    define('CW_SR_FrozenNote',[(cv('cw_sr_view_state','=',4),loc('cw_sr_frozen_note','Departure values are fixed for this mission. Later policy changes and new bonuses affect future missions.'))],loc('cw_sr_live_note','These are the current contributions used for this programme. Policy bonuses are earned through paid engineering work.'))
    define('CW_SR_ModifierTable',[(cv('cw_sr_view_state','=',4)+' '+cv('cw_sr_view_mod_recorded','=',0),loc('cw_sr_legacy_flight_modifiers','This mission departed before detailed qualification records were introduced. Its original departure probabilities remain in force.\n\nFinal departure: [?cw_sr_view_launch|2]%\nFinal objective: [?cw_sr_view_objective|2]%\nFull mission success: [?cw_sr_view_full|2]%'))],'cw_sr_modifier_table')
    loc('cw_sr_modifier_table','Departure / objective contributions in percentage points\n\nBase design: [?cw_sr_view_base_l|2]% / [?cw_sr_view_base_o|2]%\nPaid qualification: [?cw_sr_view_mod_paid_l|2] / [?cw_sr_view_mod_paid_o|2] pp\nOperating support: [?cw_sr_view_mod_support_l|2] / [?cw_sr_view_mod_support_o|2] pp\nFlight experience: [?cw_sr_view_mod_experience_l|2] / [?cw_sr_view_mod_experience_o|2] pp\nFunding disruption: [?cw_sr_view_mod_disruption_l|2] / [?cw_sr_view_mod_disruption_o|2] pp\nCorrective engineering: [?cw_sr_view_mod_corrective_l|2] / [?cw_sr_view_mod_corrective_o|2] pp\nResearch analysis: 0.00 / [?cw_sr_view_mod_analysis|2] pp\nSpace leadership: 0.00 / [?cw_sr_view_mod_leader|2] pp\n\n§HFinal departure: [?cw_sr_view_launch|2]%§!\n§HFinal objective: [?cw_sr_view_objective|2]%§!\n§GFull mission success: [?cw_sr_view_full|2]%§!\n\n[CW_SR_FrozenNote]\n\nProbabilities are limited to 2-99.5%. Ground commissioning has no departure risk. Full success requires both stages.')
    loc('cw_sr_national_effects','§HSPACE LEADERSHIP§!\n[CW_SR_Leader]\n\n[CW_SR_NationalLeader]\n\n§HRESEARCH ANALYSIS§!\nCurrent objective bonus: §H[?cw_sr_analysis_current|2] percentage points§!.\nEach research data point adds 0.02 pp, up to +2 pp.\n\n§HOPERATING EXPENDITURE§!\nCurrent weekly operating costs: §H$[?cw_sr_weekly_upkeep_m|2]m§!.\nThe leadership reduction is already included.\n\n§HDEVELOPMENT APPROACH§!\n[CW_SR_Selected_Policy]\n[CW_SR_PolicyEffects]\n\nPolicy changes affect future paid work. They do not grant an immediate chance increase or alter a mission already in flight.')
    define('CW_SR_PolicyEffects',[(cv('cw_sr_view_policy','=',p),loc('cw_sr_visible_policy_'+str(p),message)) for p,message in [(1,'Development cost +18%; calendar +18%.\nFull funded qualification: up to +2.5 pp departure and +4 pp objective.'),(2,'Development cost +25%; calendar -15%.\nFull funded qualification: up to -4.5 pp departure and -3.5 pp objective.'),(3,'Development cost -20%; calendar +35%.\nFull funded qualification: up to -2.5 pp departure and -2 pp objective.')]],loc('cw_sr_visible_policy_0','Standard development cost and calendar.\nNo additional policy contribution to mission probability.'))
    # Put the contribution into the same actual-component table as other modifiers.
    c['LOC']['cw_sr_modifier_table']=c['LOC']['cw_sr_modifier_table'].replace('Operating support:', 'Hardware generations: [?cw_sr_view_mod_technology_l|2] / [?cw_sr_view_mod_technology_o|2] pp\\nOperating support:')
    return out
