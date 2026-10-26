# IMPERIA CW — Cold War: North Korea screenshot amendments and successor programme.
"""Apply authorized amendments to the preserved v2 approval snapshot."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
import json

ROOT=Path(__file__).resolve().parents[2]
APPROVED=ROOT/'docs/COLDWAR_NKO_1970_concept/v2/COLDWAR_NKO_v2_design.json'
CURRENT=Path(__file__).with_name('current_design.json')

def raised(value):
    return float((Decimal(str(value))*Decimal('1.25')).quantize(Decimal('.00001'),rounding=ROUND_HALF_UP))

DESCRIPTIONS={
 'soviet_industry':'Negotiate Soviet machinery deliveries, power engineering and technical training. Soviet access can relieve industrial bottlenecks, while increasing our dependence on imported equipment and advisers.',
 'china_border':'Restore regular agricultural exchange and supply arrangements along the Chinese frontier. Reliable deliveries would ease domestic shortages, at the cost of border administration and a greater reliance on Beijing.',
 'korean_channel':'Open reciprocal contacts, commercial exchanges and family visits across the peninsula. Both governments would gain a channel for cooperation while accepting the political risks of sustained contact.',
 'civil_atomic':'Negotiate Soviet assistance for civilian reactor research and engineering. Technical cooperation would strengthen the power programme while bringing additional training, supervision and diplomatic obligations.',
 'gdr_machinery':'Seek East German machine tools, industrial standards and specialist training. Better production methods would improve factory performance, while tying more of our industry to imported components.',
 'bulgarian_engineering':'Arrange engineering and agricultural exchanges with Bulgaria. Shared expertise would improve production and farm inputs, with continuing demands on technical staff and public budgets.',
 'romanian_exchange':'Expand industrial and commercial exchanges with Romania. Cooperation would diversify our external connections while requiring export commitments and administrative support.',
 'egyptian_technical':'Develop scientific, industrial and military training exchanges with Egypt. Reciprocal technical missions would broaden specialist experience while drawing skilled personnel away from domestic duties.',
 'japan_fisheries':'Negotiate practical arrangements for fisheries and commercial contact with Japan. Access to equipment and trade would ease civilian shortages, while creating sensitive obligations over revenue and supervision.',
}
UPGRADE_DESCRIPTIONS={
 'soviet_training':'Expand specialist placements and industrial training under the Soviet protocol. Greater expertise would come with a larger commitment of instructors, facilities and foreign technical influence.',
 'border_trade':'Establish regular trading arrangements at agreed border crossings. More dependable commerce would support supplies and revenue, while requiring additional customs and policing capacity.',
 'confederation_offer':'Propose a confederal framework while retaining separate administrations. The arrangement depends on the other Korean government accepting reciprocal economic and political obligations.',
 'npt_offer':'Extend civilian nuclear cooperation under international safeguards. Wider technical access would require inspection commitments and continuing supervision of the research programme.',
 'gdr_training':'Extend East German training and industrial cooperation to additional production lines. Higher efficiency would require more technical exchanges and sustained commitments to imported standards.',
 'bulgarian_agrobiology':'Expand joint agricultural research and engineering exchanges. Improved yields and farm practices would require additional training and public support.',
 'romanian_trade':'Broaden the exchange programme through regular commercial commitments. Increased trade would require further export allocations and administrative capacity.',
 'egyptian_missions':'Extend the exchange programme through longer technical and training missions. Additional experience would require greater spending on specialist personnel and education.',
 'japan_ports':'Broaden commercial arrangements through fisheries and port access. More reliable civilian trade would require additional policing and careful management of external commitments.',
}

def load():
    d=json.loads(APPROVED.read_text(encoding='utf-8'))
    for node in d['nodes']:
        node['cost_gdp_share']=raised(node['cost_gdp_share'])
        # A constitutional policy may be pursued ahead of its historical date.
        # Keep the actual leader/party/predecessor guards shown to the player.
        if node['key']=='presidency':
            node['eligibility_notes']=[g for g in node['eligibility_notes'] if 'COLDWAR_NKO_early_constitution' not in g]
        for extra in node['extra']:
            if extra['kind']=='debt':extra['principal_gdp_share']=raised(extra['principal_gdp_share'])
    for a in d['agreements']:
        a['description']=DESCRIPTIONS[a['key']]
        for side in ('nko','recipient'):a[side]['setup_gdp_share']=raised(a[side]['setup_gdp_share'])
        for u in a['upgrades']:
            u['setup_nko_gdp_share']=raised(u['setup_nko_gdp_share'])
            u['setup_recipient_gdp_share']=raised(u['setup_recipient_gdp_share'])
            u['description']=UPGRADE_DESCRIPTIONS.get(u['key'],'Expand the existing programme through additional reciprocal commitments and specialist exchanges.')
    for incident in d['incidents']:
        for c in incident.get('choices',[]):
            if 'cost_gdp_share' in c:c['cost_gdp_share']=raised(c['cost_gdp_share'])
        if 'mitigation_cost_gdp_share' in incident:incident['mitigation_cost_gdp_share']=raised(incident['mitigation_cost_gdp_share'])
    for n in d['nodes']:
        offer=next((e for e in n['extra'] if e['kind']=='agreement'),None)
        if offer:
            a=next(a for a in d['agreements'] if a['key']==offer['agreement'])
            n['description']=a['description'] if offer['stage']=='base' else next(u['description'] for u in a['upgrades'] if u['key']==offer['stage'])
    base=next(n for n in d['nodes'] if n['key']=='jongil_settlement')
    def add(key,title,x,y,pre,mods,cost,icon,description,mutex=()):
        n=deepcopy(base)
        n.update(id='COLDWAR_NKO_'+key,key=key,title=title,long_title=title,
          x=x,y=y,dx=x-64,dy=y-17,anchor='COLDWAR_NKO_jongil_authority',
          prerequisites=[['COLDWAR_NKO_'+p for p in pre]],mutex=['COLDWAR_NKO_'+p for p in mutex],
          cost=5,days=35,cost_gdp_share=cost,modifiers=mods,icon=icon,description=description,
          labels={},effects=[],historical_status='Early Kim Jong Il rule; historical constraints and alternative policy responses')
        d['nodes'].append(n)
    add('jongil_supply_commission','Supply Commission',64,20,['jongil_settlement'],
      {'supply_consumption_factor':-.04,'social_cost_multiplier_modifier':.04},.005,'NKO_food',
      'Coordinate food stocks, transport and emergency procurement after the loss of subsidized supplies. Central supervision can reduce waste, but relief purchases will place a heavier burden on the state budget.')
    add('jongil_distribution','Public Distribution',62,21,['jongil_supply_commission'],
      {'agricolture_productivity_modifier':.06,'stability_factor':.04,'social_cost_multiplier_modifier':.06,'tax_gain_multiplier_modifier':-.03},.0075,'NKO_food',
      'Protect priority rations and channel scarce fertilizer and fuel through the public distribution system. This can support farm output and social control, while requiring subsidies and leaving fewer resources for taxable exchange.',('jongil_local_markets',))
    add('jongil_local_markets','Tolerate Local Markets',66,21,['jongil_supply_commission'],
      {'productivity_growth_modifier':.04,'tax_gain_multiplier_modifier':.04,'political_power_factor':-.04,'police_cost_multiplier_modifier':.04},.005,'trade',
      'Allow regulated local exchange and household production to supplement official supplies. New commerce can improve livelihoods and revenue, while weakening central direction and demanding closer supervision.',('jongil_distribution',))
    add('jongil_priority_inputs','Priority Farm Inputs',62,22,['jongil_distribution'],
      {'agricolture_productivity_modifier':.08,'supply_consumption_factor':-.03,'production_speed_industrial_complex_factor':-.04,'social_cost_multiplier_modifier':.04},.00625,'NKO_food',
      'Reserve transport, spare parts and fuel for cultivation and irrigation. More dependable farm inputs would protect the harvest, while delaying civilian industrial investment and sustaining expensive state deliveries.')
    add('jongil_barter_channels','Barter Channels',66,22,['jongil_local_markets'],
      {'trade_opinion_factor':.08,'resource_export_multiplier_modifier':.04,'foreign_influence_defense_modifier':-.04,'bureaucracy_cost_multiplier_modifier':.03},.00438,'trade',
      'Permit supervised barter and commercial procurement where foreign exchange is scarce. Wider trading channels can secure essential inputs, while allocating more exports abroad and exposing officials to outside influence.')
    add('jongil_industrial_repair','Industrial Repairs',64,23,['jongil_priority_inputs','jongil_barter_channels'],
      {'industrial_capacity_factory':.06,'production_factory_efficiency_gain_factor':.05,'non_electric_fuel_consumption_modifier':.06},.01,'economic_civil_industry',
      'Repair idle machinery and restore dependable supplies of components to priority factories. Recovered output will increase demand for fuel before newer, more efficient equipment can be introduced.')
    add('jongil_kpa_priority','Prioritize the KPA',62,24,['jongil_industrial_repair'],
      {'army_org_factor':.08,'supply_consumption_factor':-.04,'army_personnel_cost_multiplier_modifier':.06,'production_speed_industrial_complex_factor':-.06},.0075,'NKO_defence',
      'Give the armed forces first claim on dependable supplies, trained personnel and transport. Better readiness strengthens the leadership’s military foundation, while higher personnel costs and delayed civilian construction deepen the defence burden.',('jongil_civilian_recovery',))
    add('jongil_civilian_recovery','Fund Civilian Recovery',66,24,['jongil_industrial_repair'],
      {'productivity_growth_modifier':.06,'agricolture_productivity_modifier':.06,'army_personnel_cost_multiplier_modifier':-.05,'army_org_factor':-.05},.0075,'economic_civil_industry',
      'Redirect resources from military establishments toward farms and civilian production. Lower personnel commitments and renewed investment can support recovery, at the cost of immediate military organization and readiness.',('jongil_kpa_priority',))
    add('jongil_recovery_accounts','Recovery Accounts',64,25,['jongil_kpa_priority','jongil_civilian_recovery'],
      {'production_factory_max_efficiency_factor':.05,'research_speed_factor':.025,'bureaucracy_cost_multiplier_modifier':.04},.005,'parliament_box',
      'Require ministries and enterprises to account for procurement, repaired capacity and technical training. Consistent records can sustain industrial recovery, but maintaining them requires a larger administrative establishment.')
    # Narrative and numerical previews are emitted from current data, not stale
    # effect strings embedded in the immutable approval snapshot.
    for n in d['nodes']:n.pop('effects',None)
    d['status']='IMPLEMENTED — screenshot amendments authorized by the user'
    d['amendments']={'one_off_price_multiplier':1.25,'proposal_reuse_days':180,'added_focuses':9,'weekly_commitments_changed':False,'presidency_historical_date_gate_removed':True}
    from expansion import extend
    extend(d)
    return d
