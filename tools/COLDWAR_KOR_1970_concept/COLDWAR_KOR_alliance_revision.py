# IMPERIA CW — Cold War: bilateral delivery and the Korean-American programme.
"""User-requested gameplay revision; keep the original 298 IDs and the 300 cap."""
from copy import deepcopy
from pathlib import Path
import json

HERE=Path(__file__).parent
DOC=HERE.parents[1]/'docs/design/COLDWAR_KOR_1970'
P='COLDWAR_KOR_'
REVISION='USFK and reciprocal diplomacy, 25 October 2026'

def number(v):return f'{v:.5f}'.rstrip('0').rstrip('.')

def policy(node,mods,slot=None,condition=None):
    old=node['effects']['policies']
    slot=slot or (old[0]['slot'] if old else node['key'])
    prefix=node['id']+'_'+slot+'_'
    lines=[line for line in node['native_leaf_effects'].splitlines() if not line.startswith('set_variable = { '+prefix)]
    q=old[0]['qualified_slot'] if old else node['group']+':'+slot
    entry={'slot':slot,'qualified_slot':q,'modifiers':mods}
    if condition:entry['active_condition']='accepted '+condition
    node['effects']['policies']=[entry]
    node['native_leaf_effects']='\n'.join(lines+[f'set_variable = {{ {prefix+k} = {number(v)} }}' for k,v in mods.items()])

def offer(node,key):
    if not any(a.get('type')=='offer' and a.get('value')==key for a in node['effects']['actions']):node['effects']['actions'].append({'type':'offer','value':key})

def contract(data,key,recipient,kor,partner,cost=1,other_cost=1,weekly=.001,other_weekly=.001,days=1095,**extra):
    found=next((x for x in data['contracts'] if x['key']==key),None)
    c=found or {'id':P+key,'key':key,'recipient':recipient,'description':'','status':'Implemented bilateral agreement'}
    c.update(recipient=recipient,KOR_cost_bn=cost,KOR_weekly_bn=weekly,
        KOR_policy=[{'slot':key,'modifiers':kor}] if kor else [],
        recipient_effects={'treasury_change':-other_cost,'weekly_expense_bn':other_weekly,'policy':partner},duration_days=days)
    c.update(extra)
    c['revised_terms']=True
    if not found:data['contracts'].append(c)
    return c

def new_focus(template,key,label,description,xy,icon='diplomacy'):
    n=deepcopy(template)
    for field in ('native_bypass_body','bypass','start_replacements','temporary_effect','state_effects','conditional_completion'):
        n.pop(field,None)
    n.update(id=P+key,key=key,group='usfk',label=label,full_title=label,description=description,
        xy=list(xy),anchor=None,offset=list(xy),icon_family=icon,prerequisites=[],mutually_exclusive=[],ownership='national',
        native_leaf_effects='',native_gate_body='original_tag = KOR\nIMP_is_1970_scenario = yes\nis_subject = no',
        added_in_revision=3,history='research_us_forces_1970.md',requirements=[],condition_code=[])
    n['effects']={'policies':[],'cost':0,'weekly':0,'buildings':[],'one_time':{},'actions':[]}
    n['proposed_trigger']=P+'can_'+key
    return n

def load_design():
    d=json.loads((DOC/'COLDWAR_KOR_design.json').read_text(encoding='utf-8'))
    assert len(d['nodes'])==298
    by={n['key']:n for n in d['nodes']}
    # The diplomatic opening itself has concrete, reciprocal institutions.
    contract(d,'red_cross_channel','NKO',{'stability_factor':.025,'social_cost_multiplier_modifier':.025},
        {'stability_factor':.025,'social_cost_multiplier_modifier':.025},weekly=.0005,other_weekly=.0005)
    contract(d,'working_contacts','NKO',{'trade_opinion_factor':.05,'political_power_factor':.04,'bureaucracy_cost_multiplier_modifier':.04},
        {'trade_opinion_factor':.05,'political_power_factor':.04,'bureaucracy_cost_multiplier_modifier':.04})
    contract(d,'parallel_recognition','NKO',{'foreign_influence_defense_modifier':.06,'stability_factor':.03,'political_power_factor':-.04},
        {'foreign_influence_defense_modifier':.06,'stability_factor':.03,'political_power_factor':-.04},weekly=.0005,other_weekly=.0005,days=1825)
    contract(d,'sovereign_confederation','NKO',{'trade_opinion_factor':.05,'civilian_factories_productivity':.015,'bureaucracy_cost_multiplier_modifier':.06,'foreign_influence_defense_modifier':-.04},
        {'trade_opinion_factor':.05,'civilian_factories_productivity':.015,'bureaucracy_cost_multiplier_modifier':.06,'foreign_influence_defense_modifier':-.04},cost=2,other_cost=2,weekly=.002,other_weekly=.002,days=0)
    contract(d,'historical_claims_dialogue','JAP',{'stability_factor':.04,'bureaucracy_cost_multiplier_modifier':.03,'trade_opinion_factor':-.02},
        {'trade_opinion_factor':.03,'political_power_factor':-.03},weekly=0,other_weekly=0)
    contract(d,'independent_left_dialogue','NKO',{'political_power_factor':.06,'foreign_influence_defense_modifier':.03,'bureaucracy_cost_multiplier_modifier':.04},
        {'trade_opinion_factor':.04,'bureaucracy_cost_multiplier_modifier':.03},weekly=0,other_weekly=0)
    contract(d,'cultural_exchanges','NKO',{'trade_opinion_factor':.04,'research_speed_factor':.015,'foreign_influence_defense_modifier':-.025},
        {'trade_opinion_factor':.04,'research_speed_factor':.015,'foreign_influence_defense_modifier':-.025},weekly=.0005,other_weekly=.0005)
    contract(d,'border_notifications','NKO',{'army_org_factor':.025,'army_core_defence_factor':.03,'bureaucracy_cost_multiplier_modifier':.03},
        {'army_org_factor':.025,'army_core_defence_factor':.03,'bureaucracy_cost_multiplier_modifier':.03},weekly=.0005,other_weekly=.0005)
    contract(d,'korean_community_dialogue','NKO',{'stability_factor':.04,'civilian_factories_productivity':.025,'bureaucracy_cost_multiplier_modifier':.06,'foreign_influence_defense_modifier':-.04},
        {'stability_factor':.04,'civilian_factories_productivity':.025,'bureaucracy_cost_multiplier_modifier':.06,'foreign_influence_defense_modifier':-.04},cost=2,other_cost=2,weekly=.0015,other_weekly=.0015,days=1825)
    contract(d,'neutrality_guarantees','USA, NKO, SOV and CHI; all four must assent',
        {'foreign_influence_defense_modifier':.10,'trade_opinion_factor':.04,'army_attack_factor':-.05},
        {'trade_opinion_factor':.02,'bureaucracy_cost_multiplier_modifier':.015},cost=2,other_cost=1,weekly=.001,other_weekly=0,days=1825,non_aggression=True)
    # New follow-up negotiations for activities involving another government.
    contract(d,'japan_joint_training','JAP',{'research_speed_factor':.025,'civilian_factories_productivity':.025,'foreign_influence_defense_modifier':-.035},
        {'trade_opinion_factor':.03,'education_cost_multiplier_modifier':.02})
    contract(d,'gulf_project_access','SAU or IRQ',{'civilian_factories_productivity':.03,'trade_opinion_factor':.04,'foreign_influence_defense_modifier':-.03},
        {'production_speed_industrial_complex_factor':.025,'bureaucracy_cost_multiplier_modifier':.025},other_cost=0,other_weekly=0,
        selectable=True,recipient_income=1,recipient_weekly_income=.001)
    contract(d,'worker_rights_protocol','GER',{'stability_factor':.03,'trade_opinion_factor':.03,'social_cost_multiplier_modifier':.03},
        {'stability_factor':.02,'bureaucracy_cost_multiplier_modifier':.025},weekly=0,other_weekly=0)
    contract(d,'peninsula_liaison_office','NKO',{'trade_opinion_factor':.06,'army_org_factor':.02,'bureaucracy_cost_multiplier_modifier':.04,'foreign_influence_defense_modifier':-.02},
        {'trade_opinion_factor':.06,'army_org_factor':.02,'bureaucracy_cost_multiplier_modifier':.04,'foreign_influence_defense_modifier':-.02})
    contract(d,'korean_final_settlement','NKO',{'stability_factor':.05,'trade_opinion_factor':.04,'army_attack_factor':-.03,'bureaucracy_cost_multiplier_modifier':.03},
        {'stability_factor':.05,'trade_opinion_factor':.04,'army_attack_factor':-.03,'bureaucracy_cost_multiplier_modifier':.03},cost=2,other_cost=2,days=1825)
    for nkey,ckey in (('joint_technical_training','japan_joint_training'),('middle_east_bids','gulf_project_access'),
                     ('contract_worker_protection','worker_rights_protocol'),('peninsula_liaison_office','peninsula_liaison_office')):
        n=by[nkey];offer(n,ckey)
        n['effects']['policies'][0]['active_condition']='accepted '+ckey
    for nkey,ckey in (('japan_pragmatism','japan_technology_finance'),('nordpolitik','nordpolitik_recognition'),
                     ('pacific_exports','pacific_trade_contacts'),('civilian_exchange_priority','cultural_exchanges')):
        by[nkey]['effects']['policies'][0]['active_condition']='accepted '+ckey
    offer(by['korean_settlement'],'korean_final_settlement')
    by['korean_settlement']['effects']['actions']=[a for a in by['korean_settlement']['effects']['actions'] if a['value']!='conditional_peninsula_review']
    by['korean_settlement']['native_gate_body']+='\nOR = { has_country_flag = COLDWAR_KOR_confederal_secretariat_signed has_country_flag = COLDWAR_KOR_limited_trade_signed }'
    by['korean_settlement']['native_bypass_body']='original_tag = KOR IMP_is_1970_scenario = yes NOT = { OR = { has_country_flag = COLDWAR_KOR_confederal_secretariat_signed has_country_flag = COLDWAR_KOR_limited_trade_signed } } OR = { has_country_flag = COLDWAR_KOR_confederal_secretariat_refused has_country_flag = COLDWAR_KOR_confederal_secretariat_expired has_country_flag = COLDWAR_KOR_limited_trade_refused has_country_flag = COLDWAR_KOR_limited_trade_expired }'
    policy(by['korean_implementation_review'],{'trade_opinion_factor':.03,'foreign_influence_defense_modifier':.03,'bureaucracy_cost_multiplier_modifier':.04})
    # A fresh USFK programme: ten preserved IDs plus exactly two new focuses.
    contract(d,'us_garrison','USA',{'army_core_defence_factor':.06,'army_org_factor':.03,'foreign_influence_defense_modifier':-.08,'personnel_cost_multiplier_modifier':-.03,'bureaucracy_cost_multiplier_modifier':.03},
        {'army_org_factor':.015,'supply_consumption_factor':.02,'bureaucracy_cost_multiplier_modifier':.02},cost=2,other_cost=2,weekly=.002,other_weekly=.004,days=1825,usfk=True)
    contract(d,'us_drawdown','USA',{'foreign_influence_defense_modifier':.08,'production_speed_arms_factory_factor':.10,'army_org_factor':.03,'army_core_defence_factor':-.06,'personnel_cost_multiplier_modifier':.10},
        {'personnel_cost_multiplier_modifier':-.01,'bureaucracy_cost_multiplier_modifier':.01},cost=2,other_cost=1,weekly=.002,other_weekly=0,days=1825,usfk=True)
    contract(d,'us_combined_command','USA',{'planning_speed':.08,'army_org_factor':.04,'foreign_influence_defense_modifier':-.05,'bureaucracy_cost_multiplier_modifier':.04},
        {'army_org_factor':.02,'supply_consumption_factor':.015,'bureaucracy_cost_multiplier_modifier':.02},weekly=.002,other_weekly=.002,days=1825,usfk=True)
    contract(d,'combined_readiness_board','USA',{'army_org_factor':.03,'supply_consumption_factor':-.04,'bureaucracy_cost_multiplier_modifier':.04},
        {'army_org_factor':.015,'bureaucracy_cost_multiplier_modifier':.02},usfk=True)
    for c in d['contracts']:
        if 'recipient_income' in c:c['recipient_effects']['treasury_change']=c['recipient_income']
        if 'recipient_weekly_income' in c:c['recipient_effects']['weekly_income_bn']=c['recipient_weekly_income']
    root=new_focus(by['diplomatic_review'],'usfk_presence','US Forces Korea',
        'The American presence anchors deterrence on the peninsula, but its future rests on decisions taken in both capitals. A renewed stationing agreement would define facilities, consultation and support while preserving the Republic’s responsibility for its own defence.',[63,15])
    offer(root,'us_garrison');d['nodes'].append(root);by[root['key']]=root
    exercises=new_focus(by['diplomatic_review'],'combined_exercises','Combined Exercises',
        'Korean and American staffs must test plans against the demands of reinforcement and command. Field exercises sharpen combat readiness, while command-post drills concentrate on planning; both require an agreed schedule, trained personnel and the resources of two governments.',[63,20],'training')
    exercises['effects']['cost']=1
    exercises['native_leaf_effects']='set_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes'
    exercises['effects']['actions']=[{'type':'action','value':'open_usfk_exercises'}]
    policy(exercises,{'planning_speed':.04,'personnel_cost_multiplier_modifier':.03},slot='exercise_staff')
    d['nodes'].append(exercises);by[exercises['key']]=exercises
    d['groups'].append({'id':'usfk','label':'US Forces Korea','anchor':[63,15],'party':None,'icon':'army','history':'research_us_forces_1970.md','gate':'Reciprocal Korean-American agreements','ownership':'national','root':root['id']})
    positions={'alliance_bargain':[62,16],'strategic_autonomy':[64,16],'burden_sharing':[62,17],'diverse_partners':[64,17],
        'defence_quality':[63,18],'allied_procurement':[62,19],'domestic_defence_industry':[64,19],
        'licensed_maintenance':[62,20],'changwon_production':[64,20],
        'joint_readiness_audits':[63,22],'combined_exercises':[63,21]}
    for key,xy in positions.items():
        n=by[key];n['group']='usfk';n['xy']=xy;n['anchor']=root['id'];n['offset']=[xy[0]-63,xy[1]-15]
        if key in ('alliance_bargain','burden_sharing','combined_exercises','joint_readiness_audits'):
            n['requires_usfk_membership']=True
            n['native_gate_body']+='\nhas_idea = COLDWAR_KOR_usfk_member\nUSA = { has_idea = COLDWAR_KOR_usfk_member }'
    for key in ('alliance_bargain','strategic_autonomy'):by[key]['prerequisites']=[[root['id']]]
    by['defence_quality']['prerequisites']=[[P+'burden_sharing',P+'diverse_partners']]
    for key in ('allied_procurement','domestic_defence_industry'):by[key]['prerequisites']=[[P+'defence_quality']]
    exercises['prerequisites']=[[P+'licensed_maintenance',P+'changwon_production']]
    by['joint_readiness_audits']['prerequisites']=[[exercises['id']]]
    for key in ('reserve_army','professional_core'):by[key]['prerequisites']=[[P+'defence_logistics']]
    by['defence_quality']['label']='Arms Standards'
    by['vietnam_legacy']['prerequisites']=[[P+'diplomatic_review']]
    by['strategic_autonomy']['label']='Korean-Led Defence';by['strategic_autonomy'].pop('start_replacements',None)
    offer(by['strategic_autonomy'],'us_drawdown')
    by['strategic_autonomy']['native_gate_body']+='\nNOT = { has_country_flag = COLDWAR_KOR_us_garrison_pending }'
    by['alliance_bargain']['effects']['policies'][0]['active_condition']='accepted us_alliance_assurance'
    by['burden_sharing']['label']='Combined Command';offer(by['burden_sharing'],'us_combined_command')
    by['burden_sharing']['effects']['policies'][0]['active_condition']='accepted us_combined_command'
    n=by['joint_readiness_audits'];n['effects']['one_time']={};n['native_leaf_effects']=n['native_leaf_effects'].replace('army_experience = 15\n','')
    n['effects']['policies'][0]['active_condition']='accepted combined_readiness_board';offer(n,'combined_readiness_board')
    by['alliance_bargain']['label']='Retain US Forces'
    by['diverse_partners']['label']='Diversify Security Links'
    for key,family in {'usfk_presence':'army','alliance_bargain':'cooperation','strategic_autonomy':'army',
            'burden_sharing':'state','diverse_partners':'cooperation','defence_quality':'oversight',
            'allied_procurement':'research','domestic_defence_industry':'industry',
            'licensed_maintenance':'research','changwon_production':'industry'}.items():
        by[key]['icon_family']=family
    descriptions={
        'reciprocal_contacts':'Regular contact between officials can turn occasional exchanges into a working relationship. Both governments would fund permanent negotiating teams, accepting an administrative burden in return for steadier communication and a clearer route toward recognition and practical cooperation.',
        'red_cross_channel':'Separated families need more than public declarations of sympathy. A funded channel between the Korean Red Cross organizations would support humanitarian negotiations and provide officials able to carry them forward, while placing new obligations on each government’s welfare administration.',
        'sovereign_confederation':'A consultative framework could give the two Korean governments common institutions without dissolving their separate administrations. Shared work would improve commercial coordination, but the secretariat and political accommodation would demand resources and expose each government to influence from the other.',
        'two_governments':'Reciprocal recognition would acknowledge that practical cooperation must proceed between two established governments. The declaration could steady the political relationship and protect each administration’s room to govern, while provoking constituencies unwilling to accept a divided national authority.',
        'korean_settlement':'The earlier agreements have created a basis for a broader political settlement. Seoul can seek a common commitment to sustained cooperation, accepting restraints and administrative obligations in exchange for a more stable relationship across the peninsula.',
        'peninsula_liaison_office':'Permanent liaison offices would give the two governments a daily means of resolving disputes and supervising agreed work. Seoul must negotiate the offices’ authority and finance their operation, balancing more reliable communication against the influence and obligations that sustained contact brings.',
        'joint_technical_training':'Korean industrial development needs people able to adapt foreign methods to domestic production. A joint programme with Japanese institutions would bring engineers and workers into closer technical cooperation, while deepening dependence on an external partner and requiring resources from both sides.',
        'middle_east_bids':'Korean contractors seek a place in the Middle East’s expanding construction markets. Government negotiations can establish access and technical cooperation, but participating firms will depend on foreign authorities and must sustain the administrative and financial commitments of overseas work.',
        'contract_worker_protection':'Korean workers abroad depend on agreements that reach beyond the authority of Seoul’s labour administration. A protocol with West Germany would establish common responsibilities for their treatment and supervision, requiring both governments to support the institutions that enforce those standards.',
        'alliance_bargain':'American assurances can steady deterrence through a period of changing troop commitments. Seoul must secure Washington’s agreement to the relationship it seeks, accepting the financial and political demands of close cooperation rather than assuming that continued support is guaranteed.',
        'strategic_autonomy':'A stronger Korean command structure would give the Republic greater capacity to shape its own defence. Seoul can prepare those institutions while negotiating a reduction of the resident American presence; any agreed drawdown will bring additional responsibilities as well as greater freedom of action.',
        'burden_sharing':'A combined headquarters would turn alliance commitments into operational plans, supported by Korean facilities and reception arrangements. Shared command promises more coherent readiness, while binding national decisions more closely to an American partner and creating a lasting administrative obligation.',
        'joint_readiness_audits':'A standing bilateral board could examine the weaknesses revealed by combined training and reinforcement plans. Its work would improve logistics and command coordination, provided both military establishments commit personnel, funding and access to the review.',
        'defence_quality':'Korean procurement needs consistent standards for inspection, maintenance and industrial quality. A stronger purchasing authority would make production more reliable whether equipment is licensed abroad or developed at home, while increasing the administrative demands placed on suppliers and the defence ministry.',
    }
    for key,text in descriptions.items():by[key]['delivery_description']=text
    # Every new node uses the same native guard/offset receipt contract.
    for n in d['nodes']:
        n['native_completion_guard']=n['native_gate_body']+'\nNOT = { has_country_flag = '+n['id']+'_paid }'
    d['revision']=3;d['status']='IMPLEMENTED — user-requested USFK and diplomatic delivery revision'
    d['delivery_revision']=REVISION
    d['layout']['shortcuts'][5]['name']='Defence and US Forces Korea'
    # Compact the old foreign-policy spine after its alliance lane moved.
    for n in d['nodes']:
        if n['group']=='foreign' and n['xy'][1]>=3:
            n['xy'][1]-=2;n['offset'][1]-=2
        elif n['group']=='usfk':
            n['xy'][1]-=2
            if n['anchor'] is None:n['offset'][1]-=2
        elif n['group']=='defence' and n['xy'][1]>=7:
            n['xy'][1]-=3;n['offset'][1]-=3
    d['groups'][-1]['anchor']=[63,13]
    assert len(d['nodes'])==300 and len({n['id'] for n in d['nodes']})==300
    return d

def write_snapshot(data):
    (DOC/'COLDWAR_KOR_runtime_design.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
