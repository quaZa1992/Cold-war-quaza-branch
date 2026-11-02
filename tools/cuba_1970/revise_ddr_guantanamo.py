# IMPERIA COLD WAR — Requested independent island diplomacy and defensive works.
"""Create the authorized revision from the immutable foreign-policy concept."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT/'docs/design/cuba_foreign_1970/FOREIGN_POLICY_CONCEPT.json'
data = json.loads(BASE.read_text(encoding='utf8'))
by = {n['key']: n for n in data['nodes']}


def merge(source, targets):
    donor = by[source]
    for key in targets:
        n = by[key]
        for k,v in donor['modifiers'].items():
            n['modifiers'][k] = round(n['modifiers'].get(k, 0)+v, 5)
        n['effects'] += deepcopy(donor['effects'])
        n['days'] += donor['days']; n['cost'] += donor['cost']
        n.setdefault('consolidated_from', []).append(source)
        n['prerequisites'] = [p for p in n['prerequisites'] if donor['id'] not in p]
    data['nodes'].remove(donor)
    data['merges'].append(dict(source=source, targets=targets, days=donor['days'], effects=donor['effects'], modifiers=donor['modifiers']))


merge('harvest_accounts', ['finish_zafra','restore_sectors'])
merge('health_workforce', ['medical_brigades','retain_doctors'])
by['finish_zafra']['lifetime'] = 'Harvest mobilisation until 26 July 1970; public accounts and transport remain national institutions.'
for n in data['nodes']:
    if n['anchor'] in ('COLDWAR_CUB_harvest_accounts','COLDWAR_CUB_health_workforce'):
        n['anchor'] = None

# The two island routes are independent entry choices, beside Soviet diplomacy.
# Berlin and Havana becomes a substantive continuation of either accepted route.
positions = {
    'foreign_soviet':(36,0), 'foreign_cmea':(34,2), 'foreign_specialisation':(34,3),
    'foreign_sov_commodity':(38,2), 'foreign_sov_industry':(42,2),
    'foreign_symbolic':(44,0), 'foreign_cession':(48,0), 'foreign_ddr':(46,2),
    'foreign_diplomacy':(56,0), 'foreign_mex_fuel':(54,2), 'foreign_mex_agro':(58,2),
    'foreign_spr_nickel':(62,2), 'foreign_spr_training':(66,2),
    'foreign_can_rail':(62,4), 'foreign_can_fisheries':(66,4),
    'foreign_interests':(54,4), 'foreign_limited':(52,5), 'foreign_settlement':(56,5),
    'foreign_caribbean':(62,5), 'foreign_algeria':(70,5),
    'foreign_overseas':(64,6), 'foreign_advisers':(62,7), 'foreign_expeditionary':(66,7),
    'foreign_angola':(62,9), 'foreign_ethiopia':(66,9),
    'coastal_patrols':(32,1), 'civil_military_pact':(32,3),
}
for key, xy in positions.items():
    by[key]['xy'] = list(xy)
for key in ('foreign_soviet','foreign_symbolic','foreign_cession'):
    by[key]['prerequisites'] = []
by['foreign_ddr']['prerequisites'] = [['COLDWAR_CUB_foreign_symbolic','COLDWAR_CUB_foreign_cession']]
by['foreign_ddr']['required_agreements_any'] = ['foreign_symbolic','foreign_cession']
by['foreign_ddr']['description'] = 'A ratified island agreement gives Havana and East Berlin a basis for practical cooperation. An industrial training commission can turn the friendship gesture or negotiated access protocol into sustained work between Cuban enterprises and East German technical institutions.'
by['foreign_cession']['accepted_effects'].append(dict(kind='rename_state',state=1252,name='Ernst Thälmann Island'))

# The existing US consent route remains a short, clearly named blockade path.
by['foreign_interests']['native_title'] = by['foreign_interests']['title'] = 'Talks with Washington'
by['foreign_limited']['native_title'] = by['foreign_limited']['title'] = 'Ease the Trade Blockade'
by['foreign_settlement']['native_title'] = by['foreign_settlement']['title'] = 'Settle Claims and Embargo'
by['foreign_settlement']['native_title'] = 'End the Blockade'
by['foreign_settlement']['description'] = 'A comprehensive settlement requires Washington to accept compensation terms and the removal of its remaining restrictions. Cuba can regain commercial access while accepting a costly claims payment and greater exposure to American economic influence. The agreement leaves Cuba\'s government and the status of Guantánamo outside its terms.'


def agreement(key,title,xy,icon,cub,other,costs,spirit,effects,description):
    n = deepcopy(by['foreign_ddr'])
    n.update(id='COLDWAR_CUB_'+key,key=key,title=title,native_title=title,xy=list(xy),anchor=None,local_xy=[0,0],
             prerequisites=[['COLDWAR_CUB_foreign_ddr']],required_agreements_all=['foreign_ddr'],
             required_agreements_any=[],cost=7,days=49,icon=icon,cub_modifiers=cub,partner_modifiers=other,
             setup_costs=costs,spirit=spirit,accepted_effects=effects,receipt=[],description=description,
             historical_status='Historical cooperation precedent; negotiated project effects are balance abstractions.',
             sources=['tools/cuba_1970/GUANTANAMO_DDR_RESEARCH.md'],requirements=['A ratified Berlin and Havana agreement'])
    n['effects'] = []; n['modifiers'] = {}; n['mutually_exclusive'] = []
    data['nodes'].append(n); by[key] = n


agreement('foreign_ddr_industry','Citrus for Machinery',(44,4),'sugartobaccocuba',
          {'agriculture_district_income_tax_modifier':.06,'resource_export_multiplier_modifier':.04,'foreign_influence_defense_modifier':-.03},
          {'civilian_factories_productivity':.03,'resource_export_multiplier_modifier':.04,'bureaucracy_cost_multiplier_modifier':.02},
          [.45,.25],'Cuban-GDR Citrus Protocol',
          [dict(kind='building',state=855,building='agriculture_district',levels=1,extra_slots=1)],
          'Cuban citrus can supply an East German market in return for irrigation and processing machinery. A joint project expands agricultural capacity, while delivery standards, packaging and dependence on a concentrated buyer require lasting commitments from both governments.')
agreement('foreign_ddr_science','Industrial Training',(48,4),'free_higher_education',
          {'research_speed_factor':.03,'civilian_factories_productivity':.03,'education_cost_multiplier_modifier':.04},
          {'research_speed_factor':.01,'resource_export_multiplier_modifier':.04,'education_cost_multiplier_modifier':.03},
          [.20,.15],'Cuban-GDR Technical Training',
          [dict(kind='research',country='CUB',category='CAT_industry',bonus=.25,uses=1),
           dict(kind='research',country='DDR',category='CAT_electronics',bonus=.25,uses=1)],
          'Industrial placements and joint maintenance teams can make imported machinery more useful. Cuba gains trained technicians and East Germany gains service contracts and practical experience. Training capacity, language instruction and compatible technical standards require a continuing education budget on both sides.')

# Existing defence focuses become a localized, paid engineering sequence.
# Preserve the old naval training and civil-military effects as part of it.
forts = {
    'coastal_patrols':('Guantánamo Perimeter',[
        dict(kind='treasury',amount=-.20),
        dict(kind='building',state=855,building='bunker',level=2,province=7590),
        dict(kind='building',state=855,building='coastal_bunker',level=1,province=7590)],
        'The Guantánamo boundary already has opposing posts, patrols and controlled access. Reinforced positions, protected observation points and coastal approaches can limit an incursion without crossing the base boundary. Construction absorbs funds and does not settle the dispute over the American base.'),
    'civil_military_pact':('Coastal Strongpoints',[
        dict(kind='treasury',amount=-.45),
        dict(kind='building',state=855,building='bunker',level=1,province=9603),
        dict(kind='building',state=855,building='coastal_bunker',level=1,province=9603),
        dict(kind='building',state=855,building='coastal_bunker',level=1,province=7590)],
        'Santiago and the Cuban approaches to Guantánamo need connected local defenses rather than an island-wide fortress belt. Coastal observation, protected firing positions and coordination with the FAR strengthen resistance to a landing. Sustained military priorities also narrow the discretion of civilian institutions.'),
}
for key,(title,extra,description) in forts.items():
    n=by[key]; n['title']=n['native_title']=title; n['description']=description
    n['additional_effects']=extra; n['effects']+=deepcopy(extra); n['cost']+=3; n['days']+=21
    n['prerequisites']=[['COLDWAR_CUB_far_reorganisation' if key=='coastal_patrols' else 'COLDWAR_CUB_coastal_patrols']]
    n['sources']=['tools/cuba_1970/GUANTANAMO_DDR_RESEARCH.md']

# Recalculate native relative offsets only after every absolute position is fixed.
ids={n['id']:n for n in data['nodes']}
for n in data['nodes']:
    if n['group']=='foreign':
        anchor = None if not n['prerequisites'] else 'COLDWAR_CUB_foreign_symbolic' if n['key'].startswith('foreign_ddr') else 'COLDWAR_CUB_foreign_soviet' if n['key'] in ('foreign_cmea','foreign_specialisation','foreign_sov_commodity','foreign_sov_industry') else 'COLDWAR_CUB_foreign_diplomacy'
        n['anchor']=anchor
    if n['anchor'] not in ids:n['anchor']=None
    n['local_xy']=[n['xy'][i]-ids[n['anchor']]['xy'][i] for i in (0,1)] if n['anchor'] else [0,0]
for g in data['groups']:
    g['nodes']=[n['id'] for n in data['nodes'] if n['group']==g['id']]
    g['root']=ids[g['nodes'][0]]['xy']
data['project']='IMPERIA COLD WAR'
data['revision']='Independent island diplomacy, reciprocal DDR projects and Guantanamo defensive works'
data['parent_concept_sha256']=hashlib.sha256(BASE.read_bytes()).hexdigest()
assert len(data['nodes'])==120
out=HERE/'revision_design.json';out.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8')
approval={'project':'IMPERIA COLD WAR','approved_design':out.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'parent_concept_sha256':data['parent_concept_sha256'],'authorization':'User requests independent DDR/island branch, additional reciprocal partnerships, US-consented blockade removal, MD event pictures and historically grounded Guantanamo land/coastal forts.','backup':'rollback_backups/cuba_ddr_guantanamo_20261023_211847','focuses':120}
(HERE/'revision_approval.json').write_text(json.dumps(approval,indent=2)+'\n',encoding='utf8')
print(json.dumps({'focuses':len(data['nodes']),'foreign':sum(n['group']=='foreign' for n in data['nodes']),'agreements':sum(bool(n.get('partner')) for n in data['nodes'])}))
