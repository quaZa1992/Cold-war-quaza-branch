# IMPERIA CW — Cold War: warsaw landmarks — build.
"""Rebuild native Blender sources, PDX exports, icons and verification renders."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

from PIL import Image
import icons
import materials

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/berlin_landmarks'))
from pdx import read, meshes


def city_preview_textures():
    report = json.loads((HERE/'city_style_report.json').read_text())
    target = HERE/'city_style_runtime'; target.mkdir(exist_ok=True)
    for entry in report['chosen_meshes'].values():
        mesh_path = ROOT/'gfx/models/buildings'/entry['mesh']
        _, mesh = next(meshes(read(mesh_path)))
        filename = mesh.nodes('material')[0].prop('diff').value[0].rstrip(b'\0').decode()
        matches = [path for path in ROOT.glob('gfx/models/buildings/**/*.dds') if path.name.lower() == filename.lower()]
        assert matches, f'Missing city texture {filename}'
        texture = Image.open(matches[0]).convert('RGBA')
        texture.save(target/(mesh_path.stem+'.png'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    config = json.loads((HERE/'config.json').read_text())
    parser.add_argument('--blender', type=Path, default=Path(config['blender']))
    args = parser.parse_args()
    assert args.blender.is_file(), f'Blender not found: {args.blender}'
    materials.create()
    runtime = HERE/'runtime'; runtime.mkdir(exist_ok=True)
    environment = os.environ.copy()
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    environment['BLENDER_USER_CONFIG'] = str(runtime)
    def blender(script):
        subprocess.run([str(args.blender), '--background', '--factory-startup',
                        '--python-exit-code', '1', '--python', str(HERE/script)],
                       cwd=ROOT, env=environment, check=True,
                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    blender('blender_palace.py')
    icons.create()
    city_preview_textures()
    blender('render_city_style.py')
    blender('blender_verify_export.py')
    subprocess.run([sys.executable, str(HERE/'validate.py')], cwd=ROOT, check=True)
