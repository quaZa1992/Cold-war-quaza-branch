"""Compile/test only actual available assets in a temporary workspace copy."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INPUTS = [
    'common/characters/TUR.txt', 'common/characters/GRE.txt', 'common/characters/CYP.txt',
    'common/scripted_effects/00_leader_setup_scripted_effects.txt',
    'common/scripted_effects/IMP_1970_world_politics_effects.txt',
    'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt',
    'history/countries/GRE - Greece.txt', 'history/countries/TUR - Turkey.txt',
    'localisation/english/0_political_system_l_english.yml',
    'tools/cyprus_1970/north/assets.json', 'tools/cyprus_1970/validate.py',
    'tools/eastern_mediterranean_1970/compile.py',
    'tools/eastern_mediterranean_1970/validate_runtime.py',
]


def main():
    with tempfile.TemporaryDirectory(prefix='isolated_runtime_', dir=HERE) as directory:
        target = Path(directory).resolve()
        # Verify the exact recursive-cleanup target before copying any files.
        assert target.parent == HERE.resolve() and ROOT.resolve() in target.parents
        def copy(relative):
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        for relative in INPUTS:
            copy(relative)
        later_history = {}
        for relative in ('history/countries/GRE - Greece.txt', 'history/countries/TUR - Turkey.txt'):
            later_history[relative] = (target / relative).read_text(encoding='utf-8-sig').partition('2000.1.1 = {')[2]
        north = json.loads((ROOT / 'tools/cyprus_1970/north/assets.json').read_text(encoding='utf-8'))['assets']
        copy(north['generic']['portrait'])
        for tag in ('TUR', 'GRE', 'CYP'):
            relative = f'tools/eastern_mediterranean_1970/{tag}/assets.json'
            if (ROOT / relative).is_file():
                copy(relative)
                for asset in json.loads((ROOT / relative).read_text(encoding='utf-8'))['assets'].values():
                    copy(asset['portrait'])
                    copy(asset['small'])
            if tag != 'CYP':
                copy(f'gfx/leaders/{tag}/1970/COLDWAR_{tag}_1970_institution.dds')
        for script in ('compile.py', 'validate_runtime.py'):
            process = subprocess.run([sys.executable, '-X', 'utf8', str(target / 'tools/eastern_mediterranean_1970' / script)],
                capture_output=True, text=True, encoding='utf-8')
            print(process.stdout.strip())
            if process.returncode:
                print(process.stderr)
                raise SystemExit(process.returncode)
        for relative, original in later_history.items():
            assert (target / relative).read_text(encoding='utf-8-sig').partition('2000.1.1 = {')[2] == original, relative
        print('PASS: temporary fixture used only actual completed portraits; production runtime unchanged.')


if __name__ == '__main__':
    main()
