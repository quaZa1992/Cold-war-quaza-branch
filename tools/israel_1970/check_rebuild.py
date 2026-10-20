"""Assert that recompilation preserves generated assets and integration edits."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
files=manifest['generated']+list(manifest['party_icons'].values())+list(manifest.get('focus_art',{}).values())+[
 'history/countries/ISR - Israel.txt',
 'common/scripted_effects/IMP_1970_world_politics_effects.txt',
 'common/scripted_effects/mdcw_1970_focus_tree_effects.txt',
 'common/scripted_effects/ISR_political_leaders.txt',
 'common/on_actions/99_ISR_on_actions.txt',
 'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt',
 'common/scripted_localisation/IMP_1970_party_name_scripted_localisation.txt',
 'tools/israel_1970/manifest.json',
 'tools/israel_1970/design_source.json',
 'tools/israel_1970/english_design.json',
]
def snapshot():return {rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in files}
before=snapshot()
subprocess.run([sys.executable,str(HERE/'build_content.py')],cwd=ROOT,check=True)
changed=[rel for rel,digest in snapshot().items() if digest!=before[rel]]
assert not changed,'Rebuild changed files: '+', '.join(changed)
print(f'PASS: {len(files)} generated, asset and integration files unchanged by rebuild.')
