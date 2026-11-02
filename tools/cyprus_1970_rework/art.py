# IMPERIA COLD WAR — Cyprus focus icon selection and native sprite registration.
"""Country-local focus artwork. Gameplay and layout remain unchanged."""
from copy import deepcopy
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PREFIX='GFX_COLDWAR_CYP_R2_art_'
HEADER='# IMPERIA COLD WAR — Cyprus 1970 focus artwork.\n'
CUSTOM={
 'republic':'republic','new_compact':'republic','rights':'republic',
 'passage':'peace','movement':'peace','safeguards':'peace','geneva':'peace',
 'guard':'guard','cypriot_command':'guard','civilian_rule':'guard',
}

def native_copy(texture):
 return 'gfx/interface/goals/coldwar_cyprus_r2/native/'+Path(texture).stem.lower()+'_'+hashlib.sha256(texture.encode()).hexdigest()[:8]+'.dds'

def selections(design):
 choices=json.loads((HERE/'native_icon_choices.json').read_text('utf8'))
 choices=choices.get('focuses',choices)
 result={}
 for f in design['focuses']:
  item=dict(choices[f['key']])
  if f['key']in CUSTOM:
   key=CUSTOM[f['key']]
   item={'texture':'gfx/interface/goals/coldwar_cyprus_r2/'+key+'.dds','reason':'Generated Cyprus '+key+' emblem.','custom':True}
  else:
   item['source_texture']=item['texture'];item['texture']=native_copy(item['texture'])
  assert (ROOT/item['texture']).is_file(),item['texture']
  item['sprite']=PREFIX+Path(item['texture']).stem.lower()
  result[f['key']]=item
 return result

def apply(design):
 d=deepcopy(design);art=selections(d)
 for f in d['focuses']:
  f['sprite']=art[f['key']]['sprite'];f['icon']=art[f['key']]['texture']
 d['focus_art']=art
 return d

def build(design):
 unique={v['sprite']:v['texture']for v in design['focus_art'].values()}
 # Identical basenames from separate source folders must never silently collide.
 for sprite,path in unique.items():
  assert all(v['texture']==path for v in design['focus_art'].values()if v['sprite']==sprite),sprite
 plain=[HEADER,'spriteTypes = {'];shine=[HEADER,'spriteTypes = {']
 for sprite,path in sorted(unique.items()):
  plain+=['\tspriteType = {',f'\t\tname = "{sprite}"',f'\t\ttexturefile = "{path}"','\t}']
  shine+=['\tspriteType = {',f'\t\tname = "{sprite}_shine"',f'\t\ttexturefile = "{path}"','\t\teffectFile = "gfx/FX/buttonstate.lua"']
  for rotation in(-90,90):
   shine+=['\t\tanimation = {',f'\t\t\tanimationmaskfile = "{path}"','\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',f'\t\t\tanimationrotation = {rotation}.0','\t\t\tanimationlooping = no','\t\t\tanimationtime = 0.75','\t\t\tanimationdelay = 0','\t\t\tanimationblendmode = "add"','\t\t\tanimationtype = "scrolling"','\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }','\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }','\t\t}']
  shine+=['\t\tlegacy_lazy_load = no','\t}']
 plain.append('}');shine.append('}')
 return {'files':{'interface/COLDWAR_CYP_R2_focus_icons.gfx':'\n'.join(plain)+'\n','interface/COLDWAR_CYP_R2_focus_shine.gfx':'\n'.join(shine)+'\n'},'loc':{},'meta':{'project':'IMPERIA COLD WAR','distinct_icons':len(unique),'custom_focuses':len(CUSTOM),'textures':unique}}
