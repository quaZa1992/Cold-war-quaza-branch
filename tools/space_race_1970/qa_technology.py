# IMPERIA COLD WAR — qa technology validation.
import json
from pathlib import Path
import re
import validate as V
from mission_rules import REQUIREMENTS
from technology_integration import FAMILIES,HISTORICAL_TECH,PILOTS,rules,requirement_parts


def run():
    ids={p['id']:i for i,p in enumerate(V.DATA['programmes'],1)}
    shared={k:v for k,op,v in V.parse((V.ROOT/'common/scripted_triggers/00_special_projects_triggers.txt').read_text(encoding='utf-8'))}
    m=V.Machine(('SAU',));m.init()
    V.check(not m.test(shared['has_completed_space_program']),'Unestablished country can research orbital hardware')
    V.check(m.test(V.TRIGGERS['cw_sr_p47_start_allowed']),'Commission cannot be developed without space technology')
    m.call('cw_sr_p47_success');V.check(m.test(shared['has_completed_space_program']),'Established commission did not unlock first research nodes')
    V.check(not m.c.technologies,'Commission granted free advanced research')
    # Both modern research and legacy project paths remain scenario-specific.
    m.c.ai=True;V.check(not m.test(shared['has_completed_space_program']),'AI inherited player-only access route')
    m.c.projects.add('sp:sp_space_program');V.check(m.test(shared['has_completed_space_program']),'Legacy AI project route broken')
    m.c.ai=False;m.is_1970=False;m.c.projects.clear();V.check(not m.test(shared['has_completed_space_program']),'1970 commission bypass leaked into later scenarios')
    m.c.projects.add('sp:sp_space_program');V.check(m.test(shared['has_completed_space_program']),'Later-scenario legacy route broken')
    # Every mapped programme needs its actual hardware before departure, but may
    # develop while that hardware is being researched.
    for n,p in enumerate(V.DATA['programmes'],1):
        minimum,payload,partner=rules(p)
        if not minimum and not payload:continue
        t=V.Machine(('SAU','USA'));t.init();t.date=f'{max(1995,p["minYear"])}.12.1';t.g.update(cw_sr_window_mars=V.D(0),cw_sr_window_venus=V.D(0))
        if 'fixedWindowStartMonth' in p:t.date='1984.12.1'
        t.c.flags.update('cw_sr_cap_'+k.replace('-','_') for k in p['capabilityRequirements'])
        for group in REQUIREMENTS.get(p['id'],[]):t.c.flags.add('cw_sr_p'+str(ids[group[0]])+'_awarded')
        V.check(t.test(V.TRIGGERS[f'cw_sr_p{n}_start_allowed']),'Research prevents otherwise valid parallel development: '+p['id'])
        # Contracted access legitimately substitutes a domestic launch technology.
        if partner:t.c.flags.discard('cw_sr_cap_contracted_orbital_access');t.c.flags.discard('cw_sr_cap_interkosmos_cooperation')
        t.put(f'cw_sr_p{n}_state',3)
        V.check(not t.test(V.TRIGGERS[f'cw_sr_p{n}_technology']),p['id']+' ignores missing hardware research')
        old=t.get('treasury');t.call(f'cw_sr_p{n}_launch');V.check(t.get('treasury')==old and not t.events,p['id']+' bypasses actual launch gate')
        if minimum:t.c.technologies.add('OLV'+str(minimum))
        if payload:t.c.technologies.add(payload+'1')
        V.check(t.test(V.TRIGGERS[f'cw_sr_p{n}_technology']),p['id']+' rejects minimum researched hardware')
        # Each payload family is mandatory independently of researched launchers.
        if payload:
            t.c.technologies.discard(payload+'1');old=t.get('treasury');t.call(f'cw_sr_p{n}_launch')
            V.check(t.get('treasury')==old and not t.rolls and not t.events,p['id']+' launched with missing payload research')
            t.c.technologies.add(payload+'1')
        if minimum>1:
            t.c.technologies.discard('OLV'+str(minimum));t.c.technologies.add('OLV'+str(minimum-1))
            V.check(not t.test(V.TRIGGERS[f'cw_sr_p{n}_technology']),p['id']+' accepts an obsolete launch-vehicle generation')
            t.c.technologies.discard('OLV'+str(minimum-1));t.c.technologies.add('OLV'+str(minimum))
        if partner and minimum:
            t.c.technologies.discard('OLV'+str(minimum));t.c.flags.add('cw_sr_cap_contracted_orbital_access')
            V.check(not t.test(V.TRIGGERS[f'cw_sr_p{n}_technology']),p['id']+' uses an abstract access receipt without a real provider')
            from qa_cooperation import qualify
            t.c=t.countries['USA'];t.init();qualify(t,'USA');t.c=t.countries['SAU']
            t.put('cw_sr_selected',n);t.put(f'cw_sr_p{n}_op_role',4);t.put('cw_sr_crew_candidate',t.country_ids['USA']);t.call(f'cw_sr_p{n}_op_invite')
            t.c=t.countries['USA'];t.call(f'cw_sr_op_accept_{n}')
            for _ in range(26):t.call('cw_sr_op_weekly')
            t.c=t.countries['SAU'];V.check(t.test(V.TRIGGERS[f'cw_sr_p{n}_technology']),p['id']+' rejects a signed and qualified human launch provider')
    # IMPERIA COLD WAR — The named provider supplies carriage, never free OLV research.
    from qa_crew import setup as ready_contract
    from qa_cooperation import invite as work_invite
    t,p=ready_contract(57);work_invite(t,57,4);t.c.technologies={x for x in t.c.technologies if not x.startswith('OLV')};t.call('cw_sr_p57_odds')
    V.check(t.test(V.TRIGGERS['cw_sr_p57_technology']) and t.get('cw_sr_p57_mod_technology_l')==2,'Qualified foreign vehicle did not supply the actual launcher generation')
    # COLDWAR 2025-cut: OLV6/COMSAT6 are the highest remaining research tiers.
    t.countries['DDR'].technologies.discard('OLV6');t.countries['DDR'].technologies.add('OLV1');t.call('cw_sr_p57_odds');V.check(t.get('cw_sr_p57_mod_technology_l')==0,'Borrowed launch chance used the client launcher or stale provider generation')
    t.countries['DDR'].technologies.add('OLV6');t.call('cw_sr_p57_odds');t.rolls.append(0);t.call('cw_sr_p57_launch');V.check(t.get('cw_sr_p57_state')==4 and not any(x.startswith('OLV') for x in t.c.technologies),'Contract failed departure or transferred provider research')
    frozen=t.get('cw_sr_p57_lp');t.countries['DDR'].technologies.clear();t.call('cw_sr_p57_odds');V.check(t.get('cw_sr_p57_lp')==frozen,'Provider changes retroactively rerolled an inflight mission')
    t,p=ready_contract(50);V.check(not t.test(V.TRIGGERS['cw_sr_p50_technology']),'Purchased foreign launch bypassed a real provider with domestic research alone');work_invite(t,50,4);V.check(t.test(V.TRIGGERS['cw_sr_p50_technology']),'Purchased foreign launch rejects an actual qualified provider')
    # The displayed checklist must use the same actual per-component conditions.
    defined={V.first(v,'name'):v for file,body in V.ASTS.items() if '/scripted_localisation/' in file for key,op,v in body if key=='defined_text'}
    for n,p in enumerate(V.DATA['programmes'],1):
        for j,(label,condition) in enumerate(requirement_parts(p),1):
            check=defined[f'CW_SR_Tech_{n}_{j}'];shown=V.first(V.first(check,'text'),'trigger')
            V.check(shown==V.parse(condition),'Visible research requirement differs from the actual launch rule')
    # 1965 baselines do not seed later generations, hardware stocks or prestige.
    for tag,expected in HISTORICAL_TECH.items():
        t=V.Machine((tag,));t.init();V.check(t.c.technologies==set(expected),'Incorrect historical research baseline '+tag)
        V.check(t.get('cw_sr_prestige')==__import__('historical_standings').BASES.get(tag,0) and not t.c.arrays,'History granted campaign awards or satellites')
    # Pilot payload is the generation qualified at departure. Preserve the old
    # native launch queue and orbit selection; further successes cannot farm units.
    t=V.Machine(('SAU',));t.init();p=V.DATA['programmes'][5]
    t.c.flags.update('cw_sr_cap_'+k.replace('-','_') for k in p['capabilityRequirements']);t.c.technologies.update(['OLV1','COMSAT2']);t.put('cw_sr_p6_state',3)
    t.c.arrays['payload_array']=[V.D(121),V.D(161),V.D(1001)];t.put('var_orbit',3);t.rolls.append(0);t.call('cw_sr_p6_launch')
    V.check(t.get('cw_sr_p6_native_model')==142 and t.get('cw_sr_p6_state')==4,'Pilot did not freeze its researched payload')
    t.c.technologies.add('COMSAT3');t.call('cw_sr_refresh');t.call('cw_sr_p6_success')
    V.check(t.c.arrays['orbit_array']==[V.D(142)] and t.get('COM_satellite_array^1')==1,'Pilot used a new generation or failed to enter the native network')
    V.check(t.c.arrays['payload_array']==[V.D(121),V.D(161),V.D(1001)] and t.get('var_orbit')==3,'Pilot handover destroyed the player launch queue or orbit selection')
    for _ in range(12):t.call('cw_sr_p6_success')
    V.check(len(t.c.arrays['orbit_array'])==1,'Repeat success spawned more native satellites')
    full=V.Machine(('SAU',));full.init();full.c.technologies.update(['OLV1','COMSAT1']);full.put('cw_sr_p6_native_model',141);full.c.arrays['orbit_array']=[V.D(141)]*1000;full.c.arrays['payload_array']=[V.D(161)];full.call('cw_sr_p6_native_pilot')
    V.check(len(full.c.arrays['orbit_array'])==1000 and full.c.arrays['payload_array']==[V.D(161)],'Full native family capacity was bypassed or discarded the launch queue')
    # IMPERIA COLD WAR — A rejected native handover must remain eligible for delivery.
    V.check('cw_sr_p6_native_commissioned' not in full.c.flags,'Rejected pilot handover was marked commissioned')
    full.c.arrays['orbit_array'].pop();full.put('COM_satellite_array^0',999);full.c.flags.add('cw_sr_p6_awarded');full.call('cw_sr_p6_success')
    V.check(len(full.c.arrays['orbit_array'])==1000 and full.get('COM_satellite_array^0')==1000,'A later accepted mission could not finish its pilot handover')
    V.check('cw_sr_p6_native_commissioned' in full.c.flags and full.c.arrays['payload_array']==[V.D(161)],'Successful retry lost its receipt or the queued native payloads')
    full.call('cw_sr_p6_success');V.check(len(full.c.arrays['orbit_array'])==1000,'Pilot retry produced a duplicate satellite')
    V.check(t.get('var_GNSS_civ_local_resources_factor')==0,'Technology refresh restored resource yields')
    t.put('cw_sr_selected',6);t.put('cw_sr_p6_state',3);t.c.technologies.update(['OLV6','COMSAT6']);t.call('cw_sr_refresh')
    V.check(t.get('cw_sr_view_mod_technology_l')==2 and t.get('cw_sr_view_mod_technology_o')==2,'Hardware contribution is not capped at +2 pp per stage')
    # KILLSAT uses a qualified reconnaissance programme, not a free research receipt.
    k=V.Machine(('SAU',));k.init();k.c.technologies.add('OLV2');V.check(not k.test(shared['has_completed_space_weapons']),'OLV research alone unlocked space weapons')
    k.c.flags.add('cw_sr_cap_orbital_reconnaissance');V.check(k.test(shared['has_completed_space_weapons']),'Reconnaissance plus OLV did not unlock native space-weapons research')
    # Inspect complete native donors, including the capacity API and adjacent GUI.
    effects=V.parse((V.ROOT/'common/scripted_effects/00_missiles_scripted_effects.txt').read_text(encoding='utf-8'));native=dict((key,body) for key,op,body in effects)
    V.check(any(key=='reserve_satellite_capacity' for key,op,v in V.walk(native['add_satellite_from_payload'])),'Pilot donor no longer enforces orbital capacity')
    modifiers=V.parse((V.ROOT/'common/dynamic_modifiers/05_missiles_modifiers.txt').read_text(encoding='utf-8'))
    V.check(not any('resource' in key.lower() for key,op,v in V.walk(V.first(modifiers,'satellite_system'))),'Satellite dynamic modifier grants resources')
    for name in ['calculate_GNSS_civ_gui_vars','add_access_GNSS_civ_vars','GNSS_civ_button_update']:
        for key,op,value in V.walk(native[name]):
            if 'local_resources_factor' in key:V.check(value=='0','Nonzero GNSS resource calculation survived in '+name)
    models=V.parse((V.ROOT/'common/scripted_effects/00_missiles_models.txt').read_text(encoding='utf-8'));limits=[]
    for key,op,v in V.walk(models):
        if 'GNSS_civ_local_resources_factor_' in key:limits.append(v)
    V.check(len(limits)==24 and set(limits)=={'0'},'GNSS resource model limits were restored')
    loc=(V.ROOT/'localisation/english/MD_missiles_l_english.yml').read_text(encoding='utf-8-sig')
    for key in ['SPACE_AUTO_NET_GNSS_TT','GNSS_CIV_STATS_TT_DELAYED','GNSS_CIV_EFFECTS_TEXT','GNSS_CIV_EFFECTS_MIN','GNSS_CIV_EFFECTS_MAX']:
        line=next(line for line in loc.splitlines() if line.startswith(' '+key+':'))
        V.check('resource' not in line.lower(),'Resource benefit remains in satellite tooltip '+key)
    gui=V.parse((V.ROOT/'interface/MD_countrymissilesview.gui').read_text(encoding='utf-8'))
    donors={V.first(v,'name').strip('"'):v for key,op,v in V.walk(gui) if key=='containerWindowType' and V.first(v,'name') in ['"GNSS_civ_systems_entry"','"GNSS_mil_systems_entry"','"COM_mil_systems_entry"']}
    for name,body in donors.items():
        V.check(V.first(body,'clipping')=='no','Native donor now clips its existing satellite columns')
    civ=donors['GNSS_civ_systems_entry'];columns={V.first(v,'name').strip('"'):v for key,op,v in civ if key.lower()=='instanttextboxtype'}
    for label,x,w in [('text',145,300),('min',355,70),('max',405,70)]:
        col=columns['GNSS_civ_effects_'+label];V.check(V.first(V.first(col,'position'),'x')==str(x) and V.first(col,'maxWidth')==str(w),'GNSS donor or adjacent column moved')
    report={'project':'IMPERIA COLD WAR','checks':V.CHECKS,'status':'passed','programmes':84,'pilot_programmes':len(PILOTS),'research_families':list(FAMILIES),'resource_production':0,'native_api':'adapter contract modeled; full orbit/ASAT runtime requires live testing','in_game_tested':False}
    Path(__file__).with_name('technology_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':run()
