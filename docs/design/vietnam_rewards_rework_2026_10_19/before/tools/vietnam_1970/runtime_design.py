"""Explicit runtime corrections without rewriting the immutable approval input."""
import json,re
from pathlib import Path

HERE=Path(__file__).resolve().parent
CAMBODIA_OFFERS={'COLDWAR_VIE_decision_cambodia','COLDWAR_VIE_decision_withdrawal'}

def _apply_focus_timing(design):
    timing=json.loads((HERE/'focus_timing.json').read_text(encoding='utf-8'))
    assert timing['default_days']==70
    for node in design['nodes']:
        node['days']=timing['exceptions'].get(node['id'],{}).get('days',timing['default_days'])
        assert node['days'] in (35,42,70)
    return design

def load_design():
    design=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'))
    for decision in design['decisions']:
        if decision['id'] not in CAMBODIA_OFFERS:
            continue
        # The native registry is authoritative: CBD is Cambodia, CAM Cameroon.
        assert decision['target']=='CAM'
        for key,value in list(decision.items()):
            if isinstance(value,str):decision[key]=re.sub(r'\bCAM\b','CBD',value)
    return _apply_focus_timing(design)


def load_campaign_design():
    """Apply the later user correction; preserve the original approval snapshot."""
    design=json.loads((HERE/'approved_campaigns.json').read_text(encoding='utf-8'))
    override=json.loads((HERE/'campaign_defence_overrides.json').read_text(encoding='utf-8'))
    expected={'COLDWAR_VIE_china_'+suffix for suffix in ('survey','liaison','hold','depth')}
    assert override['schema']==1 and set(override['policies'])==expected
    for node in design['nodes']:
        patch=override['policies'].get(node['id'])
        if patch is None:continue
        assert set(patch)<= {'description','conditions','modifiers','terrain_training'}
        node['description']=patch['description']
        node['conditions']=node['availability_code']=patch['conditions']
        policy=next(e for e in node['effects'] if e['type']=='idea')
        policy['modifiers']=patch['modifiers'].copy()
        policy['target']=None;policy['targeted_modifiers']={}
        terrain=patch.get('terrain_training')
        if terrain:node['terrain_training']=terrain.copy()
        modifiers='\n'.join(f'    {k} = {v}' for k,v in policy['modifiers'].items())
        if terrain:modifiers+='\n    custom_modifier_tooltip = '+node['id']+'_terrain_tt'
        node['idea_definitions']=node['id']+'_policy = {\n  picture = national_defenders\n  modifier = {\n'+modifiers+'\n  }\n}'
    for decision in design['decisions']:
        if decision['id']=='COLDWAR_VIE_china_decision_renew_readiness':
            decision['cost_risk']=override['renewal_cost_risk']
    for node in design['nodes']:
        for decision in node['decisions']:
            if decision['id']=='COLDWAR_VIE_china_decision_renew_readiness':
                decision['cost_risk']=override['renewal_cost_risk']
    return _apply_focus_timing(design)
