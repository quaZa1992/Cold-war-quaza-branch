# IMPERIA CW — Cold War: skill updates — install.
"""Install the user's explicitly requested MD writing-skill corrections."""
from pathlib import Path
import hashlib,json,argparse

BASE=Path('C:/Users/Enes/.codex/skills').resolve()
ALLOWED={'mdcw-national-trees/SKILL.md',
         'mdcw-national-trees/references/project-contract.md',
         'mdcw-national-trees/references/russia-2000-presentation.md',
         'mdcw-modifier-audit/SKILL.md'}
parser=argparse.ArgumentParser();bundle=parser.add_mutually_exclusive_group()
bundle.add_argument('--clarification',action='store_true');bundle.add_argument('--reference-pool',action='store_true');bundle.add_argument('--impact',action='store_true');args=parser.parse_args()
if args.reference_pool:ALLOWED.add('mdcw-national-trees/references/source-map.md')
source='reference_pool_updates.json' if args.reference_pool else 'clarification_updates.json' if args.clarification else 'updates.json'
if args.impact:
    ALLOWED={'mdcw-national-trees/SKILL.md','mdcw-national-trees/references/project-contract.md','mdcw-modifier-audit/SKILL.md'}
    source='impact_updates.json'
updates=json.loads(Path(__file__).with_name(source).read_text(encoding='utf-8'))
assert {u['relative'] for u in updates}==ALLOWED
for u in updates:
    path=(BASE/u['relative']).resolve()
    assert path.is_relative_to(BASE)
    actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    assert actual==u['before_sha256'],('Skill changed since preparation',path)
for u in updates:
    path=BASE/u['relative']
    path.write_text(u['after'],encoding='utf-8',newline='\n')
    print('Updated '+str(path))
