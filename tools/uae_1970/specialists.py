# IMPERIA COLD WAR — Research-only specialist scarcity and small-country trade-offs.
"""Apply the 25 October user revision without modifying the approved snapshot."""
import json

P = 'COLDWAR_UAE_'
SCARCITY = P + 'scarce_specialists'
RESEARCH = 'research_speed_factor'
WORKFORCE = 'total_workforce_modifier'


def _relief(node, value):
    """Keep catalogue mirrors aligned with the actual research-only remedy."""
    for field in ('starting_changes', 'spirit_changes'):
        old = next(c for c in node[field] if c['spirit'] == SCARCITY)
        change = dict(old, component=RESEARCH, operation='set', value=value)
        node[field] = [c for c in node[field] if c['spirit'] != SCARCITY] + [change]
    marker = '# PROPOSED persistent starting-spirit operations'
    head = node['effect_body'].split(marker, 1)[0].rstrip()
    node['effect_body'] = head + '\n' + marker + ':\n' + json.dumps(node['spirit_changes'], indent=2)


def apply_revision(data):
    by = {n['id'].removeprefix(P): n for n in data['nodes']}
    spirit = next(s for s in data['starting_spirits'] if s['id'] == SCARCITY)
    spirit['modifiers'] = {RESEARCH: -0.15}
    spirit['treatment'] = 'Training or specialist recruitment reduces the research penalty; Technical Institutes removes the remaining penalty.'

    for key in ('national_training', 'foreign_specialists'):
        _relief(by[key], -0.10)
        by[key]['reward_summary'] = [
            'Reduce the Scarce Specialists research penalty by 5 percentage points.',
            *[s for s in by[key]['reward_summary'] if 'Scarce Specialists' not in s],
        ]
    _relief(by['technical_institutes'], 0)
    by['technical_institutes']['reward_summary'] = [
        'Remove the remaining Scarce Specialists research penalty.',
        *[s for s in by['technical_institutes']['reward_summary']
          if 'Scarce Specialists' not in s and 'specialist workforce penalty' not in s],
    ]

    descriptions = {
        'citizen_ballot': (
            'Citizens need a durable stake in the new constitutional order. '
            'Building representative institutions can strengthen support for reform, '
            'while drawing scarce administrative and technical expertise away from research.'
        ),
        'citizen_dividend': (
            'Concentrating social entitlements on citizens builds a national constituency for reform. '
            'Prioritising immediate household support leaves fewer resources for scientific institutions.'
        ),
    }
    for key, description in descriptions.items():
        node = by[key]
        old = node['modifiers'].pop(WORKFORCE)
        assert old == -0.03 and RESEARCH not in node['modifiers'], key
        node['modifiers'][RESEARCH] = -0.03
        node['description'] = description
        node['effect_body'] = node['effect_body'].replace(node['id'] + '_' + WORKFORCE, node['id'] + '_' + RESEARCH)
        node['reward_summary'] = [s for s in node['reward_summary'] if 'workforce' not in s.lower()]
        node['reward_summary'].append('Research speed: -3%.')

    assert all(n['modifiers'].get(WORKFORCE, 0) >= 0 for n in data['nodes'])
    assert all(s['modifiers'].get(WORKFORCE, 0) >= 0 for s in data['starting_spirits'])
    return data
