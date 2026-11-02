# IMPERIA COLD WAR — Argentina 1970 restored historical event photographs.
"""Keep event and agreement art stable across bounded national-tree rebuilds."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'south_america_event_art'))
from sa_photo_catalogue import ARGENTINA, ARG_TREATIES, PREFIX, ASSET_DIR, GFX
from sa_photo_export import build_assets

GFX_REL='interface/COLDWAR_ARG_1970_eventpictures.gfx'
EVENT_IMAGE=ARGENTINA
AGREEMENT_IMAGE=ARG_TREATIES

def build(root,design):
    root=Path(root)
    manifest=build_assets(root)
    events={str(e['key']):PREFIX+ARGENTINA[str(e['key'])] for e in design.get('events',[])}
    agreements={str(a['id']):PREFIX+ARG_TREATIES[str(a['id'])] for a in design.get('agreements',[])}
    # Retain old sprite names for existing popups and external references.
    aliases={'GFX_COLDWAR_ARG_1970_event_'+k:v for k,v in ARGENTINA.items()}
    aliases.update({'GFX_COLDWAR_ARG_1970_contract_'+k:v for k,v in ARG_TREATIES.items()})
    aliases.update({'GFX_COLDWAR_ARG_1970_photo_'+k:v for k,v in {
        'political_council':'arg_opening','industrial_works':'arg_industry',
        'grain_silos':'arg_grain','treaty_signing':'shared_contract',
        'south_atlantic_map':'arg_islands','argentine_flag':'arg_islands','naval_carrier':'arg_navy'}.items()})
    lines=['# IMPERIA COLD WAR — Argentina restored event-photo compatibility aliases.','spriteTypes = {']
    for alias,asset in aliases.items():
        lines += ['\tspriteType = {',f'\t\tname = "{alias}"',f'\t\ttexturefile = "{ASSET_DIR}/{asset}.dds"','\t}']
    (root/GFX_REL).write_text('\n'.join(lines+['}','']),encoding='utf-8',newline='\n')
    notice='IMPERIA COLD WAR\n\nArgentina now uses the restored historical photo catalogue. See tools/south_america_event_art/ASSET_NOTICE.md for individual credits, licences, unknown permissions, AI restoration prompts and modifications. The current review is docs/event_art_review/south_america_1970/manifest.json. Earlier seven-image MD contact sheets are superseded. The preview is donor-composed, not a live HOI4 screenshot.\n'
    (root/'docs/design/COLDWAR_ARG_1970/implementation_art_notice.md').write_text(notice,encoding='utf-8')
    return {'outputs':[GFX_REL,GFX]+[a['output'] for a in manifest['assets']],
            'event_picture_map':events,'agreement_picture_map':agreements,'assets':manifest['assets']}
