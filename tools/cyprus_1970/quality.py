# IMPERIA CW — Cold War: cyprus 1970 — quality.
"""Approved incumbent-entry and administration corrections,20 October2026."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def revise(data):
    by={n['key']:n for n in data['focuses']}
    # Automatic compatibility receipt preserves old save/focus references.
    by['p1_mandate'].update(days=0,focus_cost=0,quality_marker=True,local_x=1,local_y=0)
    by['p1_mandate']['x']=by['p1_organisation']['x']+1
    by['p1_mandate']['y']=0
    n=by['p1_organisation']
    n['y']=0
    n['local_y']=0
    n['focus_cost']=5
    n['modifiers']['bureaucracy_cost_multiplier_modifier']=-.05
    n['treasury_cost_gdp_percent']=.25
    n['prerequisite_groups']=[]
    return data

def narrative(node):
    return json.loads((HERE/'narrative.json').read_text(encoding='utf-8'))[node['key']]
