# IMPERIA CW — Cold War: visible mission qualification and actual modifier accounting.
from mission_rules import REQUIREMENTS, qualified


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
    selected=[];rewards=[]
    for n,p in enumerate(programmes,1):
        receipt('CW_SR_Date_'+str(n),f'date > {p["minYear"]-1}.12.31','Programme available from '+str(p['minYear']))
        receipt('CW_SR_Capacity_'+str(n),'OR = { '+cv('cw_sr_active','<',3)+' '+cv(var(n,'state'),'=',1)+' }','Development capacity available (maximum 3 programmes)')
        receipt('CW_SR_Funds_'+str(n),cv('treasury','>=',p['missionCostB']),f'Mission appropriation: ${p["missionCostB"]:.2f}bn')
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
        lines=['§HNATIONAL CAPABILITIES§!','[CW_SR_Date_'+str(n)+']','[CW_SR_Capacity_'+str(n)+']']
        lines+=['[CW_SR_Check_'+cap_key(k)+']' for k in p['capabilityRequirements']]
        if not p['capabilityRequirements']:lines+=['No prior national capabilities required.']
        lines+=['','§HSUCCESSFUL PRECURSOR MISSIONS§!']
        if p['id'] in REQUIREMENTS:lines+=['[CW_SR_Qualification_'+str(groups[group])+']' for group in REQUIREMENTS[p['id']]]
        else:lines+=['No additional precursor flight required.']
        lines+=['','§HBEFORE MISSION AUTHORISATION§!','[CW_SR_Hardware_'+str(n)+']','[CW_SR_Funds_'+str(n)+']','[CW_SR_Debt_'+str(n)+']','[CW_SR_Review_'+str(n)+']'+window,'','Development may proceed before precursor flights finish.','Only a fully successful mission provides flight qualification.']
        key=loc('cw_sr_checklist_'+str(n),'\n'.join(lines));selected.append((cv('cw_sr_selected','=',n),key))
        r=p['rewardEffects']
        text=f'First success: §H+{p["prestige"]} prestige§!, §H+{r["researchPoints"]} research data§!, §H+{r["politicalCapital"]} political power§!.\n'
        if r['researchPoints']>=4:text+='§H10% research bonus§! for one technology in any field.\n'
        text+='\nAccepted capability: '+', '.join(k.replace('-',' ').title() for k in p['grants'])+'.\n\n[CW_SR_AwardState_'+str(n)+']'
        define('CW_SR_AwardState_'+str(n),[('has_country_flag = cw_sr_p'+str(n)+'_awarded',loc('cw_sr_award_received','First-success awards already received. Further missions provide limited prestige and flight experience.'))],loc('cw_sr_award_available','First-success awards remain available. Qualifying world firsts provide additional awards.'))
        rewards.append((cv('cw_sr_selected','=',n),loc('cw_sr_visible_rewards_'+str(n),text)))
    define('CW_SR_Selected_Checklist',selected,'cw_sr_checklist_47')
    define('CW_SR_VisibleRewards',rewards,'cw_sr_visible_rewards_47')
    define('CW_SR_NationalLeader',[('has_country_flag = cw_sr_leader',loc('cw_sr_national_leader_active','§GSpace leadership active§!\nMission objective chance: +2 percentage points.\nWeekly operating costs: -5%.'))],loc('cw_sr_national_leader_inactive','No space leadership bonus is active.\nBecome the sole prestige leader to receive +2 pp objective chance and -5% weekly operating costs.'))
    define('CW_SR_FrozenNote',[(cv('cw_sr_view_state','=',4),loc('cw_sr_frozen_note','Departure values are fixed for this mission. Later policy changes and new bonuses affect future missions.'))],loc('cw_sr_live_note','These are the current contributions used for this programme. Policy bonuses are earned through paid engineering work.'))
    define('CW_SR_ModifierTable',[(cv('cw_sr_view_state','=',4)+' '+cv('cw_sr_view_mod_recorded','=',0),loc('cw_sr_legacy_flight_modifiers','This mission departed before detailed qualification records were introduced. Its original departure probabilities remain in force.\n\nFinal departure: [?cw_sr_view_launch|2]%\nFinal objective: [?cw_sr_view_objective|2]%\nFull mission success: [?cw_sr_view_full|2]%'))],'cw_sr_modifier_table')
    loc('cw_sr_modifier_table','Departure / objective contributions in percentage points\n\nBase design: [?cw_sr_view_base_l|2]% / [?cw_sr_view_base_o|2]%\nPaid qualification: [?cw_sr_view_mod_paid_l|2] / [?cw_sr_view_mod_paid_o|2] pp\nOperating support: [?cw_sr_view_mod_support_l|2] / [?cw_sr_view_mod_support_o|2] pp\nFlight experience: [?cw_sr_view_mod_experience_l|2] / [?cw_sr_view_mod_experience_o|2] pp\nFunding disruption: [?cw_sr_view_mod_disruption_l|2] / [?cw_sr_view_mod_disruption_o|2] pp\nCorrective engineering: [?cw_sr_view_mod_corrective_l|2] / [?cw_sr_view_mod_corrective_o|2] pp\nResearch analysis: 0.00 / [?cw_sr_view_mod_analysis|2] pp\nSpace leadership: 0.00 / [?cw_sr_view_mod_leader|2] pp\n\n§HFinal departure: [?cw_sr_view_launch|2]%§!\n§HFinal objective: [?cw_sr_view_objective|2]%§!\n§GFull mission success: [?cw_sr_view_full|2]%§!\n\n[CW_SR_FrozenNote]\n\nProbabilities are limited to 2-99.5%. Ground commissioning has no departure risk. Full success requires both stages.')
    loc('cw_sr_national_effects','§HSPACE LEADERSHIP§!\n[CW_SR_Leader]\n\n[CW_SR_NationalLeader]\n\n§HRESEARCH ANALYSIS§!\nCurrent objective bonus: §H[?cw_sr_analysis_current|2] percentage points§!.\nEach research data point adds 0.02 pp, up to +2 pp.\n\n§HOPERATING EXPENDITURE§!\nCurrent weekly operating costs: §H$[?cw_sr_weekly_upkeep_m|2]m§!.\nThe leadership reduction is already included.\n\n§HDEVELOPMENT APPROACH§!\n[CW_SR_Selected_Policy]\n[CW_SR_PolicyEffects]\n\nPolicy changes affect future paid work. They do not grant an immediate chance increase or alter a mission already in flight.')
    define('CW_SR_PolicyEffects',[(cv('cw_sr_view_policy','=',p),loc('cw_sr_visible_policy_'+str(p),message)) for p,message in [(1,'Development cost +18%; calendar +18%.\nFull funded qualification: up to +2.5 pp departure and +4 pp objective.'),(2,'Development cost +25%; calendar -15%.\nFull funded qualification: up to -4.5 pp departure and -3.5 pp objective.'),(3,'Development cost -20%; calendar +35%.\nFull funded qualification: up to -2.5 pp departure and -2 pp objective.')]],loc('cw_sr_visible_policy_0','Standard development cost and calendar.\nNo additional policy contribution to mission probability.'))
    return out
