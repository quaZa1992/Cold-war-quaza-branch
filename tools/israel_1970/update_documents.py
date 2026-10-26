# IMPERIA CW — Cold War: israel 1970 — update documents.
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
report=['# Israel 1970: Implemented Focus Tree','',
        f"{len(data['nodes'])} focuses, {manifest['total_decisions']} decisions, {manifest['events']} events, twenty political families and thirty-seven named party/list variants. All new game localisation is English.", '',
        'The compact layout uses relative-position anchors as in the MD Russia tree. Each political family starts directly when its exact party governs. The twelve outlook unlocks and twenty government-mandate focuses have been removed. No party entry requires a focus or a foundation flag. Internal policy choices remain connected within their branches. Shared achievements survive changes of government; party programme modifiers apply only while that party governs.','',
        'Rewards were rewritten individually in revision 2. Party policies combine visible MD-style modifier changes with buildings, research, experience, interest-group approval and real constitutional choices. Descriptions contain narrative text; the game shows rewards through completion-effect tooltips. There is no generic 65/35 modifier split.','',
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
exports=[]
for rel in manifest['generated']:
    if rel.endswith('.txt'):exports+=['# ===== '+rel+' =====\n'+(ROOT/rel).read_text(encoding='utf-8-sig')]
(DOC/'md_style_code_drafts.txt').write_text('\n\n'.join(exports),encoding='utf-8')
# Keep the existing standalone preview's embedded design synchronized without
# depending on the visualization output directory of the chat that created it.
preview=DOC/'preview.html'
if preview.exists():
    source=preview.read_text(encoding='utf-8')
    iframe=re.search(r'data-srcdoc="([^"]*)"',source)
    assert iframe,'Missing standalone preview iframe'
    fragment=html.unescape(iframe[1])
    pattern=r'(<script type="application/json" id="isr70-data">)(.*?)(</script>)'
    payload=re.search(pattern,fragment,re.S)
    assert payload,'Missing embedded focus design'
    previous=json.loads(payload[2])
    current={key:data[key] for key in previous}
    for key in ('nodes','groups'):
        fields=previous[key][0].keys()
        current[key]=[{field:item[field] for field in fields} for item in data[key]]
    encoded=json.dumps(current,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    fragment=re.sub(pattern,lambda match:match[1]+encoded+match[3],fragment,count=1,flags=re.S)
    source=source[:iframe.start(1)]+html.escape(fragment,quote=True)+source[iframe.end(1):]
    preview.write_text(source,encoding='utf-8')
# These four unused icons were created by this module before the scope correction.
asset_root=(ROOT/'gfx/texticons/parties_icons/israel/1970').resolve()
for idx in (8,9,10,11):
    asset=(asset_root/f'party_{idx}.dds').resolve()
    assert asset.parent==asset_root and asset_root.is_relative_to(ROOT.resolve())
    asset.unlink(missing_ok=True)
print('Updated English report and live code export; removed four unused module icons.')
