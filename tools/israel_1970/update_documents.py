# IMPERIA COLD WAR — Israel 1970 generated design documentation.
"""Keep the design report and code export aligned with the compiled module."""
from pathlib import Path
import html
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DOC=ROOT/'docs/israel_1970_design'
data=json.loads((HERE/'english_design.json').read_text(encoding='utf-8'))
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
report=['# IMPERIA COLD WAR: Israel 1970 Implemented Focus Tree','',
        f"{len(data['nodes'])} focuses, {manifest['total_decisions']} decisions, {manifest['events']} events, twenty political families and thirty-seven named party/list variants. All new game localisation is English.", '',
        'The compact layout uses relative-position anchors as in the MD Russia tree. Each political family starts directly when its exact party governs. The twelve outlook unlocks and twenty government-mandate focuses have been removed. No party entry requires a focus or a foundation flag. Internal policy choices remain connected within their branches. Shared achievements survive changes of government; party programme modifiers apply only while that party governs.','',
        'The 27 October 2026 revision adds distinct institutional rewards, stronger civilian productivity and diaspora finance, a shared workforce route capped at +15%, and three bounded settlement extensions. Ceasefire talks are player-initiated and territorial administration opens independently of military outcomes. See REWORK_20261027.md for history, numerical routes, provenance and validation limits.','',
        'The corrected settlement-presence extension separates unilateral footholds under foreign control from controlled-state construction, with regional occupation costs. The affected controller receives production, stability and budget penalties without a consent decision or payment. An existing Palestine also receives bounded West Bank/Gaza institutional and commercial pressure from actual settlement programmes, with selected funded compensation relief. See UNILATERAL_SETTLEMENTS.md, PRESENCE_AND_OCCUPATION.md and PALESTINIAN_PRESSURE.md for conditions, numeric terms, period sources and verification limits.','',
        'The retained outlooks are Western, Emerging, Non-Aligned and Nationalist. There are no Shiite or Salafist paths, foundations, campaigns or government programmes. Their four native slots are disabled for the 1970 Israel scenario.','',
        'Golda Meir and the Alignment lead the January 1970 coalition. Religious Zionist and Orthodox parliamentary parties retain their own programmes. Later named parties require their dated or explicitly alternative foundations. Generic MD symbols and portraits are used when period assets are absent.','',
        '## Starting Spirits','']
for spirit in data['starting_spirits'].values():
    report+=['### '+spirit['label'],'',spirit['treatment'],'',', '.join(f'`{k}`: {v:+g}' for k,v in spirit['modifiers'].items()),'']
for group in data['groups']:
    report+=['## '+group['label'],'',group['description'],'']
    for node in (n for n in data['nodes'] if n['group']==group['id']):
        report+=['### '+node['label'],'',f"`{node['id']}` | x={node['xy'][0]}, y={node['xy'][1]} | {node['days']} days",'']
        parents=[' OR '.join(row) for row in node['prerequisites']]
        report+=['Prerequisites: '+(' AND '.join('('+p+')' for p in parents) or 'Entry focus')+'.','']
        if node['mutually_exclusive']:report+=['Exclusive with: '+', '.join(node['mutually_exclusive'])+'.','']
        report+=['Artwork: `'+node.get('art_source','')+'`.','',node['description'],'']
        report+=['- '+line for line in node.get('reward_summary',[])]+['']
        report+=['```hoi4',node['completion_reward_code'],'```','']
report+=['## Validation','',
         'Run `python tools/israel_1970/build_content.py` followed by `python tools/israel_1970/validate_content.py`. Static validation covers references, syntax, assets, party restrictions, programme routes, treasury reservations, negotiations and scenario integration. It does not replace an HOI4 engine test.','']
(DOC/'DESIGN.md').write_text('\n'.join(report),encoding='utf-8')
exports=['# IMPERIA COLD WAR — Israel 1970 emitted script reference.']
for rel in manifest['generated']:
    if rel.endswith('.txt'):exports+=['# ===== '+rel+' =====\n'+(ROOT/rel).read_text(encoding='utf-8-sig')]
(DOC/'md_style_code_drafts.txt').write_text('\n\n'.join(exports),encoding='utf-8')
# render_preview.py owns the compact inspector data and readable conditions.
# Its output is wrapped separately; never infer a schema from an older preview.
# These four unused icons were created by this module before the scope correction.
asset_root=(ROOT/'gfx/texticons/parties_icons/israel/1970').resolve()
for idx in (8,9,10,11):
    asset=(asset_root/f'party_{idx}.dds').resolve()
    assert asset.parent==asset_root and asset_root.is_relative_to(ROOT.resolve())
    asset.unlink(missing_ok=True)
print('Updated English report and live code export; removed four unused module icons.')
