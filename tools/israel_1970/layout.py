# IMPERIA COLD WAR — Israel 1970 national programme layout.
"""Native focus clusters: national institutions, political families and policy.

Positions are authored once here and consumed by both the game compiler and the
interactive preview. This module changes geometry only; the original grouped
prerequisites, exclusive choices and government gates remain intact.
"""

COMMON = {
 'state': {'january_1970':(0,0),'knesset':(0,1),'unity_cabinet':(-3,2),'narrow_cabinet':(3,2),'civil_service':(0,3),'oversight':(0,4),'local_councils':(-4,4),'central_planning':(4,4),'basic_laws':(0,5)},
 'economy': {'economic_plan':(0,0),'water':(-7,1),'negev_agriculture':(-6,2),'water_maintenance':(-9,2),'haifa_industry':(0,1),'tel_aviv_offices':(7,1),'negev_roads':(-6,3),'power_grid':(0,2),'exports':(7,2),'import_substitution':(-2,2),'export_specialization':(2,2),'diaspora_bonds':(7,3),'investment_scrutiny':(7,4),'civil_electronics':(0,3),'technion':(0,4),'sme_credit':(7,5),'civil_plant':(0,5),'fiscal_review':(7,6),'steady_budget':(6,7),'development_budget':(8,7)},
 'society': {'social_contract':(0,0),'vocational':(-4,1),'development_towns':(-4,2),'absorption_reform':(-4,3),'arab_citizens':(0,1),'equal_local_services':(-1,2),'local_autonomy':(1,2),'religion_state':(4,1),'religious_compromise':(3,2),'civil_marriage':(5,2),'national_service':(4,3),'volunteer_service':(3,4),'service_expansion':(5,4),'universities':(-7,2),'public_health':(-1,3)},
 'defense': {'staff':(0,0),'reserve_system':(-12,1),'defensive_depth':(-14,2),'maneuver':(-12,2),'armour_programme':(-2,1),'survivability':(-3,2),'armour_mobility':(-1,2),'imi':(-2,3),'artillery':(-6,2),'engineers':(-6,3),'special_forces':(-6,4),'air_staff':(7,1),'foreign_aircraft':(6,2),'local_aircraft':(8,2),'air_maintenance':(7,3),'airfield':(7,4),'air_defense':(-9,2),'naval_staff':(14,1),'missile_boats':(13,2),'submarines':(15,2),'shipyards':(14,3),'intelligence':(0,5),'intelligence_analysis':(-3,6),'intelligence_operations':(3,6),'civil_defense':(-17,2),'preparedness':(-12,4)},
 'diplomacy': {'foreign_policy':(0,0),'us_channel':(-10,1),'us_security':(-11,2),'us_civil':(-9,2),'france_channel':(-5,1),'european_trade':(-5,2),'soviet_channel':(0,1),'soviet_dialogue':(0,2),'independent_diplomacy':(5,1),'africa_contacts':(4,2),'jordan_backchannel':(10,1),'iran_contacts':(14,1),'oil_security':(14,2),'nuclear_policy':(7,2),'keep_ambiguity':(6,3),'nuclear_transparency':(8,3)},
 'territories': {'suez':(-10,0),'limited_attrition':(-15,1),'deep_raids':(-11,1),'rogers':(-7,1),'ceasefire':(-7,2),'armed_stalemate':(-13,2),'territorial_policy':(4,0),'all_on':(0,1),'territorial_maximalism':(4,1),'regional_compromise':(10,1),'sinai_negotiation':(0,2),'westbank_autonomy':(3,2),'golan_review':(13,1),'gaza_services':(16,1),'egypt_peace':(0,3),'regional_normalization':(2,4),'territory_administration':(6,2),'annexation_review':(6,3)},
}
EXTRA = {'alignment_balance':(-6,2),'golda_labour':(-7,3),'golda_manager':(-5,3),'golda_panthers':(-6,4),'golda_housing':(-6,5),'golda_succession':(0,5),'rabin_cabinet':(-1,6),'peres_cabinet':(1,6),'gahal_identity':(-6,2),'gahal_coalition':(-7,3),'likud_foundation':(-5,3)}

# A single policy terrace follows the political families. Read left to right:
# citizenship, development finance, settlements, Sinai, civil status and the
# radical alternatives. Keep the authored policy lanes and their visible forks.
POLICY_ORIGINS = {
 'policy_citizens':(12,26),'policy_finance':(39,26),
 'policy_settlements':(67,26),'policy_greater':(92,26),
 'policy_occupation':(110,26),'policy_radicals':(135,26),
 'policy_presence':(67,36),
}

# National branches occupy the upper terrace. The Knesset anchors the centre,
# social and economic programmes lie to its left, military and foreign policy
# to its right. Four political families below them remain inspectable together.
# Larger Alignment and Gahal footprints receive their own western-family space.
ORIGINS={
 'state':(53,0),'economy':(15,0),'society':(37,0),
 'defense':(83,0),'diplomacy':(121,0),'territories':(121,7),
 'party_3':(14,10),'party_1':(29,10),
 'party_0':(12,18),'party_2':(25,18),
 'party_4':(44,10),'party_5':(55,10),
 'party_6':(44,17),'party_7':(55,17),
 'party_12':(71,10),'party_13':(82,10),
 'party_14':(93,10),'party_15':(104,10),
 'party_16':(71,17),'party_17':(82,17),
 'party_18':(93,17),'party_19':(104,17),
 'party_20':(119,18),'party_21':(130,18),
 'party_22':(119,22),'party_23':(130,22),
 **POLICY_ORIGINS,
}


def _policy_fallback(nodes):
    """Give unannotated policy nodes a safe, deterministic downward layout.

    Authors should provide ``policy_local_xy`` for the intended route layout;
    this fallback keeps incremental design edits collision-free until then.
    Alternatives sharing a ``choice_group`` are placed beside one another.
    """
    by_id={n['id']:n for n in nodes}
    positions={}
    grouped={}
    for n in nodes:
        if n.get('choice_group'):
            grouped.setdefault(n['choice_group'],[]).append(n)
    handled=set()
    for n in nodes:
        if n['id'] in handled:continue
        choice=n.get('choice_group')
        cluster=grouped.get(choice,[n]) if choice else [n]
        inner_parents=[p for member in cluster for row in member.get('prerequisites',[]) for p in row if p in by_id]
        y=max((positions[p][1] for p in inner_parents),default=-1)+1
        # A normal focus continues from its first in-group prerequisite. A root
        # gets a fresh lane; alternatives share a row with two units of padding.
        if choice:
            count=len(cluster)
            xs=[i*2-(count-1) for i in range(count)]
            occupied={tuple(xy) for xy in positions.values()}
            while any((x,y) in occupied for x in xs):xs=[x+2 for x in xs]
            for member,x in zip(cluster,xs):
                positions[member['id']]=[x,y];handled.add(member['id'])
        else:
            parents=[p for row in n.get('prerequisites',[]) for p in row if p in positions]
            x=positions[parents[0]][0] if parents else 0
            occupied={tuple(xy) for xy in positions.values()}
            while (x,y) in occupied:x+=2
            positions[n['id']]=[x,y];handled.add(n['id'])
    return positions


def apply_layout(nodes, groups, root):
    policy_groups={g['id'] for g in groups if g['id'].startswith('policy_')}
    fallback={group:_policy_fallback([n for n in nodes if n['group']==group]) for group in policy_groups}
    for n in nodes:
        key=n['id'].removeprefix('ISR70_')
        if n['group'] in COMMON:n['local_xy']=list(COMMON[n['group']][key])
        elif key in EXTRA:n['local_xy']=[EXTRA[key][0],EXTRA[key][1]-1]
        elif n['group'] in policy_groups:
            local=n.get('policy_local_xy')
            n['local_xy']=list(local if local is not None else fallback[n['group']][n['id']])
        else:
            suffix=key.split('_',1)[1]
            n['local_xy']=list({'institution':(0,0),'ea':(-3,1),'eb':(-1,1),'ca':(1,1),'cb':(3,1),'ea_deepen':(-3,2),'eb_deepen':(-1,2),'ca_deepen':(1,2),'cb_deepen':(3,2),'finish':(0,3)}[suffix])
    for g in groups:
        assert g['id'] in ORIGINS,('No compact layout defined for group',g['id'])
        g['layout_origin']=list(ORIGINS[g['id']])
    groupmap={g['id']:g for g in groups}
    for n in nodes:
        origin=groupmap[n['group']]['layout_origin']
        n['xy']=[origin[0]+n['local_xy'][0],origin[1]+n['local_xy'][1]]
    # Logical prerequisites are preserved in metadata. Cross-block gates are
    # expressed through available/has_completed_focus so long lines do not cut
    # across unrelated programmes. Same-block ODER links stay visible.
    by_id={n['id']:n for n in nodes}
    anchors={g['id']:next(n['id'] for n in nodes if n['group']==g['id']) for g in groups}
    for n in nodes:
        n['visual_prerequisites']=[];n['availability_prerequisites']=[]
        for row in n['prerequisites']:
            target=n['visual_prerequisites'] if all(by_id[p]['group']==n['group'] for p in row) else n['availability_prerequisites']
            target.append(row)
        anchor=anchors[n['group']]
        if n['id']==anchor:anchor='ISR70_january_1970'
        if n['id']==anchor:
            n['relative_position_id']=None;n['script_xy']=list(n['xy'])
        else:
            n['relative_position_id']=anchor
            n['script_xy']=[n['xy'][axis]-by_id[anchor]['xy'][axis] for axis in (0,1)]
    return {'revision':10,'x_unit':80,'y_unit':190,'node_width':148,'node_height':160,'icons':{},'initial_show_position':[53,0],'continuous_focus_position':[0,2900],'coordinate_system':'Resolved MD coordinates. National institutions form the upper terrace; party families occupy the middle; six policy programmes form the lower terrace, with external associations and controlled-state development stacked beneath them. Within-block OR prerequisites stay visible and cross-block requirements remain availability gates.'}
