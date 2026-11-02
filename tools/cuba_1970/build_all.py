# IMPERIA COLD WAR — reproducible assembly of the approved Cuba programme.
"""Generated providers and narrow integrations; hand-authored history is preserved."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    # IMPERIA COLD WAR — Normalize hand-authored headers before taking preservation hashes.
    subprocess.run([sys.executable, '-B', str(HERE/'file_headers.py')], cwd=ROOT, check=True)
    # IMPERIA COLD WAR — Register and export MD-framed pictures before compiling events.
    subprocess.run([sys.executable, '-B', str(HERE/'event_art.py')], cwd=ROOT, check=True)
    manual = sorted(p for folder in ['events', 'common/ideas', 'common/scripted_effects', 'common/opinion_modifiers', 'common/on_actions', 'localisation/english']
                    for p in (ROOT/folder).glob('COLDWAR_CUB_1970_history*'))
    preserved = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in manual}
    for name in ['compile.py', 'foreign_contracts.py', 'integration.py', 'file_headers.py', 'validate.py', 'validate_bilateral.py', 'validate_generic_navy.py']:
        subprocess.run([sys.executable, '-B', str(HERE/name)], cwd=ROOT, check=True)
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == digest for p, digest in preserved.items()), 'A hand-authored history provider changed during the build'
    paths = sorted(set(p for folder in ['common/national_focus', 'common/ideas', 'common/dynamic_modifiers', 'common/scripted_effects',
                                        'common/scripted_triggers', 'common/on_actions', 'common/decisions', 'common/decisions/categories',
                                        'common/opinion_modifiers', 'events', 'interface', 'localisation/english']
                       for p in (ROOT/folder).glob('COLDWAR_CUB_1970*')))
    shared = ['history/countries/CUB - Cuba.txt', 'common/scripted_effects/CUB_political_leaders.txt',
              'common/scripted_effects/mdcw_1970_focus_tree_effects.txt', 'common/scripted_effects/mdcw_diaspora_migration_effects.txt']
    record = dict(project='IMPERIA COLD WAR', owned=[dict(path=str(p.relative_to(ROOT)).replace('\\', '/'), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],
                  shared_integrations=[dict(path=p, sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in shared],
                  binary_assets=[dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                                 for p in sorted((ROOT/'gfx/event_pictures/COLDWAR_CUB_1970').glob('*.dds'))],
                  hand_authored_preserved=preserved)
    (HERE/'integration_manifest.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(owned_runtime_files=len(paths), shared_integrations=len(shared), manual_history_preserved=len(preserved))))


if __name__ == '__main__':
    main()
