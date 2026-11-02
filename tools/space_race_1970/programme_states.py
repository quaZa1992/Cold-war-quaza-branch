# IMPERIA COLD WAR — Genuine programme states, visible labels and restrained status strips.
# IMPERIA COLD WAR — International operational cooperation.
def build(c):
    cv,sv,var,block_if,effect,loc=(c[k] for k in ['cv','sv','var','block_if','effect','loc']);defs='';refresh=''
    for n,p in enumerate(c['PROGRAMMES'],1):
        state=var(n,'state');inst=f'has_country_flag = cw_sr_institution_{n}';award=f'has_country_flag = cw_sr_p{n}_awarded'
        complete='§HCOMPLETED§! · Operational' if p.get('commissioningOnly') else '§HCOMPLETED§! · New mission requirements pending'
        entries=[(inst,'§gESTABLISHED BEFORE 1970§!',4),(cv(state,'=',4),'§TMISSION IN FLIGHT§!',3),(cv(state,'=',6),'§RINVESTIGATION§! · Funded review required',5),(cv(state,'=',1),'§TDEVELOPMENT§! · [?'+var(n,'work')+'|0]%',3),(cv(state,'=',2),'§gSUSPENDED§! · Development retained',1),(cv(state,'=',7),'§gCANCELLED§! · Restart requires funding',1)]
        if p.get('commissioningOnly'):entries += [(award+f' has_country_flag = cw_sr_p{n}_deployed',complete,4),(award,'§gCOMPLETED§! · Operations suspended',4)]
        else:entries += [(f'cw_sr_p{n}_launch_allowed = yes '+award,'§GREADY§! · Repeat mission available',2),(award,complete,4)]
        entries += [(f'cw_sr_p{n}_launch_allowed = yes','§GREADY FOR MISSION§!',2),(cv(state,'=',3),'§HQUALIFIED§! · Departure requirements pending',6),(f'has_country_flag = cw_sr_heritage_{n} cw_sr_p{n}_start_allowed = yes','§HFLIGHT HERITAGE§! · New campaign available',4),(f'has_country_flag = cw_sr_heritage_{n}','§HFLIGHT HERITAGE§! · Campaign requirements pending',4),(f'cw_sr_p{n}_start_allowed = yes','§GAVAILABLE§! · Development can begin',2)]
        # IMPERIA COLD WAR — Guest participation is distinct from independent qualification.
        entries.insert(6,(f'has_country_flag = cw_sr_guest_p{n}_completed NOT = {{ '+cv(state,'>',0)+' } NOT = { '+award+' }','§TJOINT FLIGHT COMPLETED§! · Guest crew',3))
        # IMPERIA COLD WAR — A work package establishes a joint record, not domestic qualification.
        entries.insert(7,(f'has_country_flag = cw_sr_op_p{n}_completed NOT = {{ '+cv(state,'>',0)+' } NOT = { '+award+' }','§TJOINT MISSION COMPLETED§! · Operational partner',3))
        texts=[];frame=sv(var(n,'ui_frame'),1)
        # Reverse conditions so the first displayed status also wins the strip.
        for i,(condition,label,index) in reversed(list(enumerate(entries))):frame+=block_if(condition,sv(var(n,'ui_frame'),index))
        for i,(condition,label,index) in enumerate(entries):texts.append('text = { trigger = { '+condition+' } localization_key = '+loc(f'cw_sr_state_{n}_{i}',label)+' }\n')
        defs+='defined_text = { name = CW_SR_ProgrammeState_'+str(n)+'\n'+''.join(texts)+'text = { localization_key = '+loc('cw_sr_programme_locked','§gLOCKED§! · Requirements not met')+' } }\n'
        refresh+=frame
        loc(f'cw_sr_p{n}_row',p['name']+'\n[CW_SR_ProgrammeState_'+str(n)+']')
    defs+='defined_text = { name = CW_SR_AtlasPhase\n'+''.join('text = { trigger = { '+cv('cw_sr_selected','=',n)+f' has_country_flag = cw_sr_institution_{n}'+' } localization_key = '+loc('cw_sr_institution_phase','Established before 1970')+' }\n' for n in range(1,85))+'text = { localization_key = '+loc('cw_sr_standard_phase','[CW_SR_Selected_Status]')+' } }\n'
    c['write']('common/scripted_effects/COLDWAR_space_race_states.txt',effect('cw_sr_programme_states_refresh',refresh))
    return defs
