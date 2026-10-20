"""Compact MD-style branch blocks with relative anchors, shared with the preview."""

COMMON = {
 'state': {'january_1970':(0,0),'knesset':(0,1),'unity_cabinet':(-2,2),'narrow_cabinet':(2,2),'civil_service':(0,3),'oversight':(0,4),'local_councils':(-3,4),'central_planning':(3,4),'basic_laws':(0,5)},
 'economy': {'economic_plan':(0,0),'water':(-6,1),'negev_agriculture':(-5,2),'water_maintenance':(-8,2),'haifa_industry':(0,1),'tel_aviv_offices':(6,1),'negev_roads':(-5,3),'power_grid':(0,2),'exports':(6,2),'import_substitution':(-2,2),'export_specialization':(2,2),'diaspora_bonds':(6,3),'investment_scrutiny':(6,4),'civil_electronics':(0,4),'technion':(0,5),'sme_credit':(6,5),'civil_plant':(0,6),'fiscal_review':(6,6),'steady_budget':(5,7),'development_budget':(7,7)},
 'society': {'social_contract':(0,0),'vocational':(-5,1),'development_towns':(-5,2),'absorption_reform':(-5,3),'arab_citizens':(0,1),'equal_local_services':(-1,2),'local_autonomy':(1,2),'religion_state':(5,1),'religious_compromise':(4,2),'civil_marriage':(6,2),'national_service':(5,3),'volunteer_service':(4,4),'service_expansion':(6,4),'universities':(-7,2),'public_health':(-3,3)},
 'defense': {'staff':(0,0),'reserve_system':(-9,1),'defensive_depth':(-11,2),'maneuver':(-9,2),'armour_programme':(-3,1),'survivability':(-4,2),'armour_mobility':(-2,2),'imi':(-3,3),'artillery':(-7,2),'engineers':(-7,3),'special_forces':(-7,4),'air_staff':(5,1),'foreign_aircraft':(4,2),'local_aircraft':(6,2),'air_maintenance':(5,3),'airfield':(5,4),'air_defense':(8,2),'naval_staff':(12,1),'missile_boats':(11,2),'submarines':(13,2),'shipyards':(12,3),'intelligence':(0,5),'intelligence_analysis':(-2,6),'intelligence_operations':(2,6),'civil_defense':(-15,2),'preparedness':(-10,5)},
 'diplomacy': {'foreign_policy':(0,0),'us_channel':(-9,1),'us_security':(-10,2),'us_civil':(-8,2),'france_channel':(-4,1),'european_trade':(-4,2),'soviet_channel':(0,1),'soviet_dialogue':(0,2),'independent_diplomacy':(5,1),'africa_contacts':(4,2),'jordan_backchannel':(10,1),'iran_contacts':(14,1),'oil_security':(14,2),'nuclear_policy':(7,2),'keep_ambiguity':(6,3),'nuclear_transparency':(8,3)},
 'territories': {'suez':(0,0),'limited_attrition':(-2,1),'deep_raids':(2,1),'rogers':(0,2),'ceasefire':(-2,3),'armed_stalemate':(2,3),'territorial_policy':(0,4),'all_on':(-5,5),'territorial_maximalism':(-2,5),'regional_compromise':(5,5),'sinai_negotiation':(-6,6),'westbank_autonomy':(-3,6),'golan_review':(3,7),'gaza_services':(6,7),'egypt_peace':(-6,7),'regional_normalization':(-5,8),'territory_administration':(0,6),'annexation_review':(0,7)},
}
EXTRA = {'alignment_balance':(-6,2),'golda_labour':(-7,3),'golda_manager':(-5,3),'golda_panthers':(-6,4),'golda_housing':(-6,5),'golda_succession':(0,5),'rabin_cabinet':(-1,6),'peres_cabinet':(1,6),'gahal_identity':(-6,2),'gahal_coalition':(-7,3),'likud_foundation':(-5,3)}

# Policy branches extend below the established tree in two compact rows. Each
# branch has its own local coordinate system, so its ODER lanes remain local.
POLICY_ORIGINS = {
 'policy_citizens':(4,26),'policy_settlements':(44,26),'policy_finance':(84,26),
 'policy_greater':(4,42),'policy_occupation':(44,42),'policy_radicals':(84,42),
}

# Match Russia's use of independent thematic roots and offsets from local
# anchors. Party programmes occupy two tiers rather than one 457-column strip.
ORIGINS={
 'state':(34,0),'economy':(13,1),'society':(59,1),
 'diplomacy':(83,1),'defense':(110,1),'territories':(110,9),
 'party_3':(9,10),'party_1':(21,10),'party_0':(11,17),'party_2':(19,17),
 'party_4':(32,7),'party_5':(40,7),'party_6':(32,12),'party_7':(40,12),
 'party_12':(49,7),'party_13':(57,7),'party_14':(65,7),'party_15':(73,7),
 'party_16':(49,12),'party_17':(57,12),'party_18':(65,12),'party_19':(73,12),
 'party_20':(82,7),'party_21':(90,7),'party_22':(82,12),'party_23':(90,12),
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
    return {'revision':6,'x_unit':80,'y_unit':190,'node_width':148,'node_height':160,'icons':{},'coordinate_system':'Resolved MD coordinates. Policy branches are compact local blocks below the original tree; within-block ODER prerequisites stay visible and cross-block requirements remain availability gates.'}
