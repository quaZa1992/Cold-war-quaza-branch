# IMPERIA CW — Cold War: berlin landmarks — blender reexport.
"""Re-export the saved editable Blender sources without repeating renders."""
from pathlib import Path
import hashlib
import json
import sys
import bpy

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import blender_landmarks as build

bie=build.exporter()
for source,model,shape in [('tv_tower.blend','landmark_berlin_tv_tower','mdcw_berlin_tv_tower'),
                           ('berlin_wall.blend','landmark_berlin_wall','landmark_berlin_wall')]:
    bpy.ops.wm.open_mainfile(filepath=str(build.SOURCE/source))
    if source=='berlin_wall.blend':
        for obj in bpy.context.scene.objects:
            if obj.type!='MESH':continue
            for modifier in list(obj.modifiers):
                if modifier.type=='BEVEL':
                    if obj.name in ['Mauer_Westseite','Mauer_Hinterland']:
                        obj.modifiers.remove(modifier)
                        continue
                    group=obj.vertex_groups.get('Exposed_concrete_edges') or obj.vertex_groups.new(name='Exposed_concrete_edges')
                    indices=[vertex.index for vertex in obj.data.vertices if vertex.co.z>.001]
                    group.add(indices,1.0,'REPLACE')
                    modifier.limit_method='VGROUP';modifier.vertex_group=group.name
        bpy.context.preferences.filepaths.save_version=0
        bpy.ops.wm.save_as_mainfile(filepath=str(build.SOURCE/source))
    objects=[obj for obj in bpy.context.scene.objects if obj.type=='MESH' and
             any(mat is not None and 'shader' in mat for mat in obj.data.materials)]
    build.export_objects(objects,model+'.mesh',shape,bie)
    build.export_objects(objects,model+'_destroyed.mesh',shape,bie)
path=HERE/'blender_export.json'
manifest=json.loads(path.read_text())
for source in manifest['sources']:
    source['sha256']=hashlib.sha256((HERE/source['path']).read_bytes()).hexdigest()
manifest['exported_files']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in build.OUT.glob('landmark_berlin_*.mesh')}
path.write_text(json.dumps(manifest,indent=2)+'\n')
print('BLENDER_REEXPORT_COMPLETE')
