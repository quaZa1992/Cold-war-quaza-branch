"""Publish a complete explicit revision from the three reviewed catalogues."""
from pathlib import Path
import hashlib,json
from decisions import normalized as decision_rewards

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];P='COLDWAR_VIE_'

def main():
    common=json.loads((HERE/'common.json').read_text(encoding='utf-8'))
    political=json.loads((HERE/'politics.json').read_text(encoding='utf-8'))
    campaign=json.loads((HERE/'campaigns.json').read_text(encoding='utf-8'))
    approved=json.loads((ROOT/'tools/vietnam_1970/approved_design.json').read_text(encoding='utf-8'))
    old={n['id']:n for n in approved['nodes']}
    patches=common['patches'].copy()
    bonus_categories={'I':'CAT_industry','C':'CAT_construction','E':'CAT_electronics','W':'CAT_infantry_weapons'}
    for group,rows in political['rows'].items():
        for suffix,short,reward,role,why in rows:
            key=P+group+'_'+suffix;assert key in old,key
            finite=[]
            for token in reward.split():
                code=token[0];value=int(token[1:])
                if code=='X':finite.append(dict(type='army_xp',amount=value))
                elif code=='D':finite.append(dict(type='doctrine_bonus',cost_reduction=value/100,uses=1,category='land_doctrine'))
                else:finite.append(dict(type='research_bonus',bonus=value/100,uses=1,category=bonus_categories[code]))
            patches.append(dict(id=key,group=group,modifiers={political['shorthand'][k]:v for k,v in short.items()},rewards=finite,role=role,why_player_wants_it=why,lifecycle=old[key]['lifecycle']))
    by={q['id']:q for q in patches}
    # These are precise costs of the chosen priority, not generic penalties on all cards.
    costs={
        'duan_patient':{'max_planning_factor':-.03},'duan_heavy':{'agricolture_productivity_modifier':-.02},'duan_balanced':{'industrial_capacity_factory':-.02},
        'duan_transform':{'bureaucracy_cost_multiplier_modifier':.02},'duan_gradual':{'production_speed_buildings_factor':-.02},
        'chinh_autonomy':{'stability_factor':-.02},'chinh_experts':{'education_cost_multiplier_modifier':.015},
        'linh_contract':{'bureaucracy_cost_multiplier_modifier':.015},'linh_coops':{'education_cost_multiplier_modifier':.01},'linh_gradual':{'bureaucracy_cost_multiplier_modifier':.015},'linh_monopoly':{'research_speed_factor':-.01},
        'kiet_local':{'stability_factor':-.01},'kiet_national':{'bureaucracy_cost_multiplier_modifier':.02},'kiet_treasury':{'bureaucracy_cost_multiplier_modifier':.02},'kiet_domestic':{'research_speed_factor':-.01},'kiet_exports':{'mdcw_cw_market_exposure':.04},
        'front_councils':{'bureaucracy_cost_multiplier_modifier':.02},'front_experts':{'education_cost_multiplier_modifier':.01},'front_cooperative':{'bureaucracy_cost_multiplier_modifier':.015},'front_households':{'political_power_factor':-.02},'front_reconcile':{'war_support_factor':-.02},'front_vanguard':{'research_speed_factor':-.01},
        'dem_courts':{'production_speed_buildings_factor':-.02},'dem_executive':{'stability_factor':-.02},'dem_champions':{'bureaucracy_cost_multiplier_modifier':.02},'dem_tender':{'political_power_factor':-.02},'dem_neutral':{'education_cost_multiplier_modifier':.01},'dem_west':{'mdcw_cw_market_exposure':.03},
        'soc_tripartite':{'bureaucracy_cost_multiplier_modifier':.015},'soc_mixed':{'mdcw_cw_market_exposure':.025},
        'nat_constitution':{'war_support_factor':-.02},'nat_president':{'stability_factor':-.015},'nat_protection':{'production_speed_buildings_factor':-.02},'nat_commerce':{'mdcw_cw_market_exposure':.03},'nat_autonomy':{'education_cost_multiplier_modifier':.015},'nat_guarantee':{'mdcw_cw_market_exposure':.03},
        'junta_defence':{'production_speed_industrial_complex_factor':-.02},'junta_recovery':{'industrial_capacity_factory':-.02},'junta_transition':{'war_support_factor':-.02},
        'unity_united':{'social_cost_multiplier_modifier':.02}}
    for suffix,mods in costs.items():by[P+suffix]['modifiers'].update(mods)
    by[P+'kiet_enterprise']['modifiers']={'production_speed_industrial_complex_factor':.08,'bureaucracy_cost_multiplier_modifier':-.02,'corporate_tax_income_multiplier_modifier':-.03}
    by[P+'kiet_enterprise']['why_player_wants_it']='Retained earnings fund faster enterprise investment and reduce central processing, at the cost of current corporate-tax collection.'
    by[P+'duan_heavy']['modifiers'].update(industrial_capacity_factory=.08,production_factory_max_efficiency_factor=.05)
    by[P+'duan_heavy']['rewards'].append(dict(type='research_bonus',bonus=.5,uses=1,category='CAT_industry'))
    by[P+'duan_balanced']['modifiers'].update(agricolture_productivity_modifier=.10,production_speed_buildings_factor=.06)
    by[P+'dem_rights']['modifiers']={'political_power_factor':.15,'bureaucracy_cost_multiplier_modifier':-.04,'stability_factor':.03}
    by[P+'dem_rights']['rewards']=[]
    by[P+'dem_rights']['why_player_wants_it']='Organised professional and civic associations improve legislative capacity and public oversight. Legal freedom does not create an unexplained electronics research grant.'
    descriptions={
        'linh_contract':'Direct the next agrarian renovation allocation towards household delivery contracts, accountable purchasing and the right to retain additional surplus. Cooperatives may still provide services, but this programme puts the new administrative effort behind household responsibility.',
        'linh_coops':'Direct the next agrarian renovation allocation towards shared equipment, technical staff and cooperative infrastructure. Household production continues, but the new funding strengthens common services and collective management rather than enlarging the household-contract programme.',
        'duan_offensive':'Concentrate the next staff, reserve-equipment and training allocation on a regular offensive. The main force gains the cohesion needed for a decisive campaign, while its supply commitment grows. Negotiations and local defence continue alongside this priority.',
        'duan_patient':'Concentrate the next staff and training allocation on staying power, protected routes and territorial defence. The army can sustain pressure with fewer supply demands, while a rapid offensive receives less planning attention. This course does not close the negotiating channel.',
        'duan_heavy':'Reserve the next industrial allocation for machine-building, armament workshops and the technical knowledge needed to sustain them. More of the scarce capital stays in heavy production, leaving less for immediate agricultural improvement.',
        'duan_balanced':'Direct the next reconstruction allocation towards food production and civilian works. Recovery must be visible in fields and ordinary workshops, even though the same investment cannot simultaneously expand the military production programme.',
        'kiet_enterprise':'Allow enterprises to reinvest a larger share of operating earnings and remove unnecessary central processing. Their investment programme can move faster, but current tax receipts fall as more resources remain inside the firms.',
        'kiet_treasury':'Pool the next development allocation in the national treasury for coordinated infrastructure and priority works. Central direction can connect projects that individual enterprises cannot finance, at the expense of additional administration.',
        'front_councils':'Give elected workplace representatives the leading role in allocating the next industrial management programme. Their knowledge can improve cooperation and civilian production, while consultation requires more administrative work. Technical specialists retain their ordinary advisory roles.',
        'front_experts':'Give the next industrial management allocation to a specialist technical cabinet and its project staff. Construction and technical review can move more quickly, while maintaining qualified personnel requires a larger education commitment. Workplace representation remains part of ordinary administration.',
        'front_nonaligned':'Independent socialism needs productive competence as well as diplomatic declarations. Establish an industrial adaptation service for machinery and technical manuals, and connect it to a homeland-defence programme that can function without surrendering control to a patron.',
        'dem_rights':'Protect civic and professional associations so that citizens can organise, challenge waste and contribute to legislation. Their capacity strengthens constitutional government and public oversight, rather than turning political liberty into a substitute for laboratories or equipment.',
    }
    for suffix,text in descriptions.items():by[P+suffix]['description']=text
    by[P+'chinh_schools']['description']='District officials must be able to turn a national programme into budgets, supplies and working enterprises. Assign the next training allocation to practical administration and industrial management in the Party school network, while the specialist advisory staff receives no matching expansion.'
    by[P+'chinh_experts']['description']='The plan needs a specialist staff able to trace shortages through accounts, transport and prices. Assign the next training allocation to an economic and technical review team, while district Party schools continue without an equivalent expansion.'
    by[P+'linh_limited']['description']='Screen projects against the machinery, repairs and operating needs of domestic enterprises. Investment can proceed under continued Party rule; the question is how to use limited administrative capacity, not whether political pluralism is required for foreign capital.'
    by[P+'linh_guarantee']['description']='Develop predictable approvals, project infrastructure and operating guarantees for investment partnerships. State oversight remains in place, while the programme commits more of the investment administration to supporting wider commercial access.'
    for suffix in ('linh_limited','linh_guarantee'):by[P+suffix]['prerequisites']=[[P+'linh_monopoly',P+'linh_pluralism']]
    by[P+'linh_limited']['modifiers'].update(production_speed_industrial_complex_factor=.04,corporate_tax_income_multiplier_modifier=.04,imp_sanction_resistance=.08,bureaucracy_cost_multiplier_modifier=.01)
    by[P+'linh_guarantee']['modifiers']['mdcw_cw_market_exposure']=.04
    # Both economic approaches remain available under either political settlement.
    for suffix in ('linh_monopoly','linh_pluralism'):
        by[P+suffix]['why_player_wants_it']+=' Capital-policy training remains independent of the constitutional choice.'
    original_campaign=json.loads((ROOT/'tools/vietnam_1970/approved_campaigns.json').read_text(encoding='utf-8'))
    oldc={n['id']:n for n in original_campaign['nodes']}
    cp=[]
    for row in campaign['patches']:
        key=row['focus_id'];proposal=row['proposed'];effects=[];patch=dict(id=key,group=oldc[key]['group'],cash=proposal['cash_bn'],why_player_wants_it=row['why_player_wants_it'])
        for pol in proposal['policies']:
            original=next((e for e in oldc[key]['effects'] if e['type']=='idea'),None)
            assert len(proposal['policies'])==1
            effects.append(dict(type='idea',title=original['title'] if original else row['title_en'],family=pol['family'],modifiers=pol['modifiers'],duration=pol['duration_days'],target=pol['target'],targeted_modifiers=pol['targeted_modifiers']))
            patch['policy_lifetime']=pol['lifetime']
            patch['policy_activation_mode']=pol['activation']
            patch['reserve_first_term']=pol['duration_days'] is not None
            mode=pol['activation']
            if mode.startswith('prepared_'):
                patch['activation']='prepared_war_plan'
                patch['war_target']='CHI' if 'chi_' in mode else 'CBD' if 'cbd_' in mode else None
                if patch['war_target'] is None:patch['activation']='prepared_any_war_plan'
        for e in proposal['typed_effects']:
            kind=e['type']
            if kind=='army_xp':effects.append(dict(type='xp',value=e['value']))
            elif kind=='doctrine':effects.append(dict(type='doctrine',uses=e['uses'],value=e['cost_reduction'],category=e['category']))
            elif kind=='research':effects.append(dict(type='research',uses=e['uses'],bonus=e['bonus'],category=e['category']))
            elif kind in ('unlock','wargoal'):effects.append({k:v for k,v in e.items() if k not in ('once_only','effect')})
            else:raise ValueError(e)
        patch['effects']=effects
        # Keep existing national narrative except where its event timing is revised.
        if key==P+'china_crisis':patch.update(label='Approve Frontier Plans',description='A frontier confrontation may leave little time for deliberation. Agree the command arrangements and political limits before the crisis begins, so that prepared defensive or counteroffensive plans can be used when a real war demands them.')
        cp.append(patch)
    assert len(patches)==239 and len(by)==239 and set(by)==set(old)
    assert len(cp)==68 and {p['id'] for p in cp}==set(oldc)
    data=dict(schema=1,revision='whole_tree_rewards_20261019',focuses=patches,campaigns=cp,new_exclusive_sets=common['new_exclusive_sets']+[[P+'linh_limited',P+'linh_guarantee']],
        decisions=decision_rewards(),
        sources={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['common.json','politics.json','campaigns.json','history_review.md']},
        contract=['Absolute per-focus replacement contributions, never old plus new.','Finite money, factory, XP and research transactions are once stamped.','Institutions and paid operational terms have different persistence.','No starting history, army, technology or sovereign transfer is granted.'])
    dest=ROOT/'tools/vietnam_1970/reward_rework.json';dest.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(original=len(patches),campaign=len(cp),new_exclusive_pairs=len(common['new_exclusive_sets']),revision=data['revision'])))

if __name__=='__main__':main()
