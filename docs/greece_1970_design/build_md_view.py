"""Build the self-contained MD-style Greece 1970 focus-tree design preview."""
from pathlib import Path
from PIL import Image
import base64, io, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = json.loads((HERE / 'coldwar_greece_1970_design.json').read_text(encoding='utf-8'))
# Audit metadata remains in the authoritative design JSON. The inline preview
# needs the visible effects and code, without repeated unused audit strings.
for node in DATA['focuses']:
    for key in ('idea_definition', 'effect_mode', 'status', 'modifier_slot', 'execution_mode', 'required_completed_focus', 'required_active_idea', 'required_regime_flags'):
        node.pop(key, None)
    node['reward_code'] = node['reward_code'].replace('\n# Proposed adapter must also recheck actual implementation and slot ceilings before grants.', '')
DATA['routes'] = [{k: r[k] for k in ('key', 'title', 'party', 'leader', 'gate')} for r in DATA['routes']]
DATA.pop('regime_packages', None)

# All images are existing mod textures. Keep this preview deterministic and offline.
ICON_PATHS = {
    'junta': 'gfx/interface/goals/coldwar/Junta_Focus.dds',
    'constitution': 'gfx/interface/goals/00_politics/Focus_Parliament_Constitution.dds',
    'election': 'gfx/interface/goals/coldwar/Greek_election.dds',
    'industry': 'gfx/interface/goals/coldwar/Greece_industrilization_1.dds',
    'army': 'gfx/interface/goals/00_army/army_reform.dds',
    'navy': 'gfx/interface/goals/coldwar/GRE_navy_focus.dds',
    'air': 'gfx/interface/goals/coldwar/GRE_air_force_focus.dds',
    'cyprus': 'gfx/interface/goals/coldwar/Cyprus_question.tga',
    'electricity': 'gfx/interface/goals/00_science/electricity.dds',
    'money': 'gfx/interface/goals/00_economy/money.dds',
    'education': 'gfx/interface/goals/00_politics/education_reform.dds',
    'diplomacy': 'gfx/interface/goals/coldwar/Greece_resort_to_UN.dds',
    'social': 'gfx/interface/goals/00_ideology/social_democracy.dds',
    'communism': 'gfx/interface/goals/00_ideology/communism/communism.dds',
    'crown': 'gfx/interface/goals/coldwar/King_compromises_with_Junta.dds',
    'republic': 'gfx/interface/goals/greece/Democratic_Greece.dds',
    'training': 'gfx/interface/goals/00_army/soldiers/Generic_Infantry_Training.dds',
    'research': 'gfx/interface/goals/00_science/research.dds',
    'shipyard': 'gfx/interface/goals/00_navy/Damen_Shipyards.dds',
    'submarine': 'gfx/interface/goals/00_navy/Generic_Submarine1.dds',
    'signals': 'gfx/interface/goals/00_science/radio_communications.dds',
    'maritime': 'gfx/interface/goals/00_trade/maritime_trade.dds',
    'agriculture': 'gfx/interface/goals/00_economy/agriculture/Generic_Veggies.dds',
    'housing': 'gfx/interface/goals/israel_1970/generic_construct_public_housing.dds',
}
ASSETS, SOURCES = {}, {}
for key, rel in ICON_PATHS.items():
    path = ROOT / rel
    if not path.exists():
        raise FileNotFoundError(f'Missing existing preview icon: {path}')
    im = Image.open(path).convert('RGBA')
    out = io.BytesIO(); im.save(out, 'WEBP', lossless=True, method=6)
    ASSETS[key] = 'data:image/webp;base64,' + base64.b64encode(out.getvalue()).decode('ascii')
    SOURCES[key] = {'path': rel, 'width': im.width, 'height': im.height, 'format': 'WebP data URL'}

PITCH_X, PITCH_Y, PAD_X, PAD_Y = 90, 130, 380, 220
def choose_icon(node):
    title = node['title'].lower()
    if node.get('party') is not None and node.get('local_y') == 0:
        return node.get('icon') if node.get('icon') in ICON_PATHS else 'republic'
    rules = [
        (('submarine', 'undersea'), 'submarine'),
        (('shipyard', 'dockyard', 'shipbuilding', 'naval construction'), 'shipyard'),
        (('maritime', 'merchant fleet', 'shipping', 'seafarer'), 'maritime'),
        (('communication', 'signals', 'radio', 'radar', 'intelligence network'), 'signals'),
        (('research', 'science', 'technical', 'university', 'skills', 'academy'), 'research'),
        (('training', 'recruit', 'infantry school', 'officer school'), 'training'),
        (('agriculture', 'rural', 'irrigation', 'farm', 'agrarian'), 'agriculture'),
        (('housing', 'displaced', 'resettlement', 'returnee'), 'housing'),
    ]
    for words, icon in rules:
        if any(word in title for word in words):
            return icon
    if node.get('icon') not in ICON_PATHS:
        return 'republic'
    return node['icon']
for node in DATA['focuses']:
    node['world_x'] = PAD_X + node['x'] * PITCH_X
    node['world_y'] = PAD_Y + node['y'] * PITCH_Y
    node['icon'] = choose_icon(node)
DATA['view'] = {
    'pitch_x': PITCH_X, 'pitch_y': PITCH_Y, 'pad_x': PAD_X, 'pad_y': PAD_Y,
    'width': PAD_X * 2 + max(n['x'] for n in DATA['focuses']) * PITCH_X,
    'height': PAD_Y * 2 + max(n['y'] for n in DATA['focuses']) * PITCH_Y,
    'item_width': 165, 'item_height': 128,
    'opening_anchor': next(s['anchor'] for s in DATA['sections'] if s['id'] == 'opening'),
}
DATA['assets'] = ASSETS
encoded = json.dumps(DATA, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
template = (HERE / 'md-view.template.html').read_text(encoding='utf-8')
fragment = template.replace('__COLDWAR_DATA__', encoded)
if '__COLDWAR_DATA__' in fragment: raise ValueError('Data placeholder was not replaced')
(HERE / 'coldwar-greece-md-layout.html').write_text(fragment, encoding='utf-8')
copy = Path(r'C:\Users\Enes\.codex\visualizations\2026\10\16\01a1431d-4972-7a81-99ad-c3beb5089421\coldwar-greece-focus-tree.html')
copy.parent.mkdir(parents=True, exist_ok=True)
copy.write_text(fragment, encoding='utf-8')
(HERE / 'MD_VIEW_ASSETS.json').write_text(json.dumps({'assets': SOURCES, 'view': DATA['view']}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'focuses': len(DATA['focuses']), 'sections': len(DATA['sections']), 'asset_count': len(ASSETS), 'fragment_bytes': len(fragment.encode()), 'world': DATA['view']}))




