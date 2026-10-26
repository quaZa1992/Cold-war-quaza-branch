# IMPERIA CW — Cold War: berlin landmarks — clear city corridor.
"""Suppress decorative city blocks in a local buffer around the approved wall.

Patch only indexed pixel bytes in cities.bmp, preserving its original V4 header,
palette and all other pixels. Province/terrain maps and landmark assets are never
modified. An unassigned city-style index generates no decorative house group.
"""
from pathlib import Path
import hashlib
import json
import math
import re
import struct

import numpy as np
from PIL import Image

from pdx import read, meshes

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONFIG = json.loads((HERE/'config.json').read_text())
CITY_MAP = ROOT/'map/cities.bmp'
EMPTY_INDEX = 3  # Already present in this map, with no city_group assignment.
HOUSE_RADIUS = 1.309592
PIXEL_RADIUS = math.sqrt(.5)
EXTRA_MARGIN = .02


def sha(data):
    return hashlib.sha256(data).hexdigest()


def protected_assets():
    paths = list((ROOT/'gfx/models/buildings/landmarks').glob('landmark_berlin_*.mesh'))
    paths += list((ROOT/'gfx/models/buildings/landmarks').glob('mdcw_berlin_landmarks_*.dds'))
    paths += [ROOT/name for name in ['map/provinces.bmp','map/terrain.bmp',
              'map/buildings.txt','gfx/entities/mdcw_berlin_landmarks.asset']]
    return {str(path.relative_to(ROOT)):sha(path.read_bytes()) for path in paths}


def distance_to_edges(points, edges):
    distance = np.full(len(points), np.inf)
    for start,end in edges:
        delta = end-start
        length2 = delta@delta
        t = np.clip((points-start)@delta/length2,0,1) if length2 else np.zeros(len(points))
        distance = np.minimum(distance,np.linalg.norm(points-start-t[:,None]*delta,axis=1))
    return distance


def polygon_distance(points, polygon):
    edges = list(zip(polygon,np.roll(polygon,-1,axis=0)))
    distance = distance_to_edges(points,edges)
    inside = np.zeros(len(points),dtype=bool)
    for a,b in edges:
        if abs(b[1]-a[1])<1e-12:continue
        crosses = (a[1]>points[:,1]) != (b[1]>points[:,1])
        cross_x = a[0]+(points[:,1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
        inside ^= crosses & (points[:,0]<cross_x)
    distance[inside] = 0
    return distance


def wall_footprint():
    route = np.array(CONFIG['wall_world'],dtype=float)
    directions = np.diff(route,axis=0)
    directions /= np.linalg.norm(directions,axis=1)[:,None]
    normals = np.c_[-directions[:,1],directions[:,0]]
    miters = [normals[0]]
    for a,b in zip(normals,normals[1:]):
        miter = a+b;miter /= np.linalg.norm(miter)
        miters.append(miter/(miter@b))
    miters = np.array(miters+[normals[-1]])
    polygon = np.vstack([route+miters*.0025,(route+miters*.50)[::-1]])
    # Include any watchtower, coping or light overhang beyond the ground ribbon.
    wall = next(meshes(read(ROOT/'gfx/models/buildings/landmarks/landmark_berlin_wall.mesh')))[1]
    vertices = wall.prop('p').value.reshape(-1,3)[:,[0,2]]+CONFIG['wall_anchor']
    overhang = float(polygon_distance(vertices,polygon).max())
    return polygon,overhang


def main():
    protected = protected_assets()
    original = CITY_MAP.read_bytes()
    report_path = HERE/'city_clearance_report.json'
    prior = json.loads(report_path.read_text()) if report_path.exists() else {}
    assert original[:2]==b'BM'
    offset = struct.unpack_from('<I',original,10)[0]
    width,height = struct.unpack_from('<ii',original,18)
    bits = struct.unpack_from('<H',original,28)[0]
    compression = struct.unpack_from('<I',original,30)[0]
    assert bits==8 and compression==0 and width>0 and height>0
    stride = (width+3)//4*4
    assert offset+stride*height<=len(original)
    city_text = (ROOT/'map/cities.txt').read_text()
    assigned = {int(index) for index in re.findall(r'color_index\s*=\s*(\d+)',city_text)}
    assert EMPTY_INDEX not in assigned
    assert EMPTY_INDEX in np.asarray(Image.open(CITY_MAP)), 'Use an existing unassigned style index'

    polygon,overhang = wall_footprint()
    clearance = HOUSE_RADIUS+PIXEL_RADIUS+EXTRA_MARGIN+overhang
    low = np.floor(polygon.min(0)-clearance-1).astype(int)
    high = np.ceil(polygon.max(0)+clearance+1).astype(int)
    xs = np.arange(max(0,low[0]),min(width,high[0])+1)
    ys = np.arange(max(0,height-high[1]-1),min(height-1,height-low[1])+1)
    yy,xx = np.meshgrid(ys,xs,indexing='ij')
    centers = np.c_[xx.ravel()+.5,height-yy.ravel()-.5]
    distances = polygon_distance(centers,polygon)
    selected = distances<=clearance
    x,y = xx.ravel()[selected],yy.ravel()[selected]
    indices = offset+(height-1-y)*stride+x
    result = bytearray(original)
    array = np.frombuffer(result,dtype=np.uint8)
    selected_indices = set(map(int,indices))
    restored = []
    retained = []
    # Restore only pixels previously cleared by this tool, and only if they
    # still contain its blank style. Other map edits remain untouched.
    for change in prior.get('changes',[]):
        index = offset+(height-1-change['y'])*stride+change['x']
        if array[index]!=EMPTY_INDEX:continue
        if index in selected_indices:
            retained.append(change)
        else:
            assert change['from'] in assigned
            array[index] = change['from']
            restored.append(change)
    previous = array[indices].copy()
    changed = previous!=EMPTY_INDEX
    array[indices] = EMPTY_INDEX
    assert bytes(result[:offset])==original[:offset], 'BMP header or palette changed'
    actual_changes = np.flatnonzero(np.frombuffer(original,dtype=np.uint8)!=array)
    restored_indices = {offset+(height-1-e['y'])*stride+e['x'] for e in restored}
    assert set(actual_changes)==set(indices[changed])|restored_indices, 'Unexpected pixels modified'
    assert set(previous[changed]).issubset(assigned), 'Unassigned non-house pixels would be overwritten'
    # Prove every pixel cell that can hold a block within reach of the wall has
    # no house-group assignment after the edit, including large rotated roofs.
    assert (array[indices]==EMPTY_INDEX).all()
    backup = HERE/'runtime/cities_before_wall_clearance.bmp'
    backup.parent.mkdir(exist_ok=True)
    if not backup.exists():backup.write_bytes(original)
    CITY_MAP.write_bytes(result)
    with Image.open(CITY_MAP) as image:
        assert image.mode=='P' and image.size==(width,height)
        image.verify()
    assert protected_assets()==protected, 'An approved map/model asset changed'

    new_changes = [{'x':int(cx),'y':int(cy),'from':int(value),'to':EMPTY_INDEX}
                   for cx,cy,value in zip(x[changed],y[changed],previous[changed])]
    active_changes = retained+new_changes

    report = {
        'status':'PASS',
        'source':'map/cities.bmp',
        'width':width,'height':height,'pixel_offset':offset,
        'unchanged_header_palette_sha256':sha(original[:offset]),
        'before_sha256':sha(original),'after_sha256':sha(result),
        'empty_city_style_index':EMPTY_INDEX,
        'assigned_house_style_indices':sorted(assigned),
        'house_maximum_radius':HOUSE_RADIUS,'pixel_half_diagonal':PIXEL_RADIUS,
        'wall_overhang':overhang,'additional_margin':EXTRA_MARGIN,
        'clearance_from_wall_footprint':clearance,
        'corridor_pixel_count':len(indices),'changed_pixel_count':len(active_changes),
        'newly_cleared_this_run':int(changed.sum()),
        'restored_this_run':len(restored),'restored_pixels':restored,
        'modified_this_run':len(actual_changes),
        'previous_indices':sorted({e['from'] for e in active_changes}),
        'changes':active_changes,
        'approved_assets_unchanged':protected,
        'backup':str(backup.relative_to(HERE)),
        'reload':'cityreload or restart HOI4; no new state history needed',
        'scope':'Local decorative-house mask; model shapes, borders and terrain unchanged. In-game visual confirmation remains necessary.'
    }
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS: {len(restored)} city pixels restored, {len(active_changes)} remain clear; BMP header/palette and approved assets unchanged.')


if __name__=='__main__':main()
