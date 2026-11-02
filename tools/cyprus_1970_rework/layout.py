# IMPERIA COLD WAR — Compact Cyprus focus positioning revision.
"""Geometry-only overlay. The approved gameplay snapshot remains immutable."""
from copy import deepcopy

ROOTS={
 'constitution':(4,0),'community':(12,0),'crisis':(20,0),
 'economy':(32,0),'defence':(44,0),'diplomacy':(52,0),
 'centre':(20,10),'liberal':(28,10),'akel':(36,10),
}
CONTINUOUS={'x':300,'y':2500}

def apply(design):
 d=deepcopy(design)
 origins={g['key']:(g['x'],g['y'])for g in d['groups']}
 for f in d['focuses']:
  ox,oy=origins[f['group']];nx,ny=ROOTS[f['group']]
  dx=f['x']-ox
  assert dx%3==0,(f['id'],dx)
  f['x']=nx+dx//3*2
  f['y']=ny+f['y']-oy
  if f['key']in('civilian_rule','geneva'):f['y']=6
 by={f['id']:f for f in d['focuses']}
 for f in d['focuses']:
  a=by[f['anchor']]if f['anchor']else{'x':0,'y':0}
  f['emitted_xy']=[f['x']-a['x'],f['y']-a['y']]
  if 'offset'in f:f['offset']=list(f['emitted_xy'])
 for g in d['groups']:g['x'],g['y']=ROOTS[g['key']]
 d['layout_revision']={'project':'IMPERIA COLD WAR','id':'compact_spacing_20261028','continuous_focus_position':CONTINUOUS}
 return d
