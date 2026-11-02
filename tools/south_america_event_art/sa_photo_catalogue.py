# IMPERIA COLD WAR — Chile, Brazil and Argentina restored event-photo catalogue.
"""Shared picture bindings. No gameplay or approval-design data is modified."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ASSET_DIR = 'gfx/event_pictures/COLDWAR_SOUTH_AMERICA_1970'
GFX = 'interface/COLDWAR_SOUTH_AMERICA_1970_photos.gfx'
PREFIX = 'GFX_ICW_SA_'

CHILE = dict(zip(
    ['election','congress','copper','transport','rupture','junta','repression','adjustment','banking','early_exit','plebiscite','handover','truth','andean'],
    ['chl_congress','chl_congress','chl_copper','chl_economy','chl_rupture','chl_junta','chl_repression','chl_finance','chl_finance','chl_handover','chl_plebiscite','chl_handover','chl_truth','shared_contract']))
BRAZIL = dict(zip(
    ['officer_council','constitution','party_reform','oil_shock','debt_crisis','us_rights','party_split','inflation_settlement','agreement_notice'],
    ['bra_officers','bra_constitution','bra_party','shared_oil','bra_debt','bra_rights','bra_split','bra_inflation','shared_contract']))
ARGENTINA = dict(zip(
    ['commanders','opening','popular_hour','peronism','labor','accountability','stabilization','privatization','liberalization','ownership','beagle','grain_pressure','islands_conference','naval_demonstration','war_outcome','campaign_inquiry'],
    ['arg_commanders','arg_opening','arg_opening','arg_labor','arg_labor','arg_accountability','arg_economy','arg_industry','arg_industry','arg_industry','arg_beagle','arg_grain','arg_islands','arg_navy','arg_islands','shared_contract']))
ARG_TREATIES = dict(zip(
    ['brazil_industry','brazil_atom','uruguay_navigation','bolivia_gas','beagle_peace','andean_passes','soviet_grain','soviet_academic','us_training','us_credit','french_aviation','spain_industry','cuba_health','peru_depots','uk_links','uk_leaseback','uk_services','madrid_consular','madrid_diplomatic','uk_sovereignty'],
    ['arg_industry','shared_nuclear','arg_grain','shared_oil','shared_treaty','shared_contract','arg_grain','shared_contract','arg_navy','shared_contract','shared_aviation','arg_industry','shared_medical','arg_navy','arg_islands','arg_islands','arg_islands','shared_contract','shared_contract','arg_islands']))

EVENT_ASSETS = {}
EVENT_ASSETS.update({'COLDWAR_CHL.'+str(i):a for i,a in enumerate(CHILE.values(),1)})
EVENT_ASSETS.update({'COLDWAR_CHL_DIP.'+str(i):a for i,a in enumerate(
    ['chl_copper','arg_industry','arg_grain','shared_medical','shared_treaty','arg_navy','arg_grain','arg_industry'],1)})
EVENT_ASSETS.update({'COLDWAR_CHL_DIP.'+str(i):'arg_industry' for i in range(20,24)})
EVENT_ASSETS.update({'COLDWAR_CHL_DIP.'+str(i):'shared_contract' for i in range(100,105)})
EVENT_ASSETS.update({'COLDWAR_BRA.'+str(i):a for i,a in enumerate(list(BRAZIL.values())[:8],1)})
EVENT_ASSETS.update({'COLDWAR_BRA_AGREEMENTS.'+str(i):a for i,a in enumerate(
    ['arg_navy','arg_industry','arg_grain','arg_industry','shared_contract','arg_grain','arg_industry','shared_medical','arg_grain','shared_nuclear','shared_nuclear','arg_industry','arg_grain','shared_aviation'],1)})
EVENT_ASSETS.update({'COLDWAR_ARG.'+str(i):a for i,a in enumerate(ARGENTINA.values(),1)})
EVENT_ASSETS.update({'COLDWAR_ARG_politics.1':'arg_labor','COLDWAR_ARG_politics.2':'arg_commanders'})
EVENT_ASSETS.update({'COLDWAR_ARG_TREATY.'+str(i):a for i,a in enumerate(ARG_TREATIES.values(),1)})

# Relative crop anchors keep faces in the native 180x150 photograph aperture.
CENTERS = {
    'arg_opening':(.5,0), 'arg_commanders':(.5,0), 'bra_party':(.5,0),
    'bra_inflation':(.5,0), 'bra_debt':(.5,.1), 'arg_economy':(.5,.15),
    'chl_congress':(.55,.6), 'chl_plebiscite':(.48,.85),
    'bra_constitution':(.63,.45), 'bra_officers':(.57,.5),
    'chl_repression':(.5,.45), 'arg_labor':(.5,.75),
    'shared_aviation':(.7,.5), 'arg_navy':(.33,.5),
}

def picture_for(event_id, fallback=None):
    asset = EVENT_ASSETS.get(event_id)
    if asset is None:
        if fallback is None: raise KeyError('Unmapped South American event '+str(event_id))
        return fallback
    return PREFIX+asset

def registry_text(keys=None):
    keys=sorted(set(EVENT_ASSETS.values()) if keys is None else keys)
    lines=['# IMPERIA COLD WAR — Restored South American country-event photographs.','spriteTypes = {']
    for key in keys:
        lines += ['\tspriteType = {',f'\t\tname = "{PREFIX+key}"',f'\t\ttexturefile = "{ASSET_DIR}/{key}.dds"','\t\tlegacy_lazy_load = no','\t}']
    return '\n'.join(lines+['}',''])
