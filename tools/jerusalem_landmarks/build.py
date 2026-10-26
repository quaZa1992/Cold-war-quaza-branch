# IMPERIA CW — Cold War: jerusalem landmarks — build.
"""Rebuild Western Wall's native Blender source, exports, icons and checks."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

import icons
import materials

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    config = json.loads((HERE/'config.json').read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', type=Path, default=Path(config['blender']))
    args = parser.parse_args()
    if not args.blender.is_file():
        parser.error(f'Blender not found: {args.blender}')
    materials.create()
    runtime = HERE/'runtime'
    runtime.mkdir(exist_ok=True)
    environment = os.environ.copy()
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    environment['BLENDER_USER_CONFIG'] = str(runtime)

    def blender(script):
        subprocess.run(
            [str(args.blender), '--background', '--factory-startup',
             '--python-exit-code', '1', '--python', str(HERE/script)],
            cwd=ROOT, env=environment, check=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )

    blender('blender_western_wall.py')
    icons.create()
    blender('blender_verify_export.py')
    subprocess.run([sys.executable, str(HERE/'validate.py')],
                   cwd=ROOT, env=environment, check=True)


if __name__ == '__main__':
    main()
