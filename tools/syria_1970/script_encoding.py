# IMPERIA CW — Cold War: Syria 1970 content imported from quaZa.
"""Keep changed engine scripts plain UTF-8; localization retains its own BOM."""
from pathlib import Path
import json
import shutil


def normalize(root):
    root = Path(root)
    here = root/'tools/syria_1970'
    paths = {
        'history/countries/SYR - Syria.txt',
        'common/scripted_effects/00_leader_setup_scripted_effects.txt',
        'common/scripted_effects/00_MD_politicsview_scripted_effects.txt',
        'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt',
        'common/scripted_effects/IMP_1970_world_politics_effects.txt',
        'common/scripted_effects/mdcw_1970_focus_tree_effects.txt',
    }
    report = json.loads((here/'retirement_report.json').read_text(encoding='utf-8'))
    paths.update(report['retired_foreign_focus_conditions'])
    paths.update(json.loads((here/'retirement_awards_report.json').read_text(encoding='utf-8')))
    paths.update(p.relative_to(root).as_posix() for folder in ('common', 'events') for p in (root/folder).rglob('COLDWAR_SYR*.txt'))
    history_path = here/'encoding_repairs.json'
    repaired = json.loads(history_path.read_text(encoding='utf-8')) if history_path.exists() else []
    for relative in sorted(paths):
        path = root/relative
        payload = path.read_bytes()
        if b'\xef\xbb\xbf' not in payload:
            continue
        backup = here/'encoding_backups'/relative
        if not backup.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup)
        path.write_text(payload.decode('utf-8').replace('\ufeff', ''), encoding='utf-8', newline='\n')
        if relative not in repaired:
            repaired.append(relative)
    history_path.write_text(json.dumps(repaired, indent=2)+'\n', encoding='utf-8')
    return repaired
