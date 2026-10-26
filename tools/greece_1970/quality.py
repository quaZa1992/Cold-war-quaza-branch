# IMPERIA CW — Cold War: greece 1970 — quality.
"""Approved 20 October focus-quality corrections; no global MD helpers changed."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def revise(data):
    p=data['prefix'];by={n['key']:n for n in data['focuses']}
    by['air_0'].update(political_power=0,xp=['air',25])
    by['air_1'].update(political_power=0,treasury_cost_gdp_percent=.25,
                       radar_project=True)
    # Keep the old ID as an automatic compatibility marker for existing saves;
    # no selectable49-day ceremony and no repeat20PP grant remain.
    by['navy_17'].update(days=0,focus_cost=0,political_power=0,quality_marker=True)
    return data

def narrative(node):
    descriptions=json.loads((HERE/'narrative.json').read_text(encoding='utf-8'))
    return descriptions[node['key']]
