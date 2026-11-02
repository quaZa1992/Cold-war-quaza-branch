# IMPERIA COLD WAR — Rejected native construction-permission diagnostic.
"""DIAGNOSTIC ONLY: rejected construction-permission candidate for E: probes.

The hidden off-grid shape follows MD special_project_tech_smart_grid. No MD
research technology, statistics or equipment is granted by these providers.
No runtime generator imports this module. Nothing here writes mod providers.
"""
from __future__ import annotations

MARK = '# IMPERIA COLD WAR — Programme construction entitlements.\n'
KINDS = {'infrastructure': ('public_works', 'Public Works Construction Standard', 6),
         'anti_air_building': ('air_defence', 'Air Defence Construction Standard', 5)}
def technology_id(kind: str, level: int) -> str:
    stem, _, ceiling = KINDS[kind]
    assert 1 <= level <= ceiling
    return f'COLDWAR_QUEUE_{stem}_{level}'


def permission_outputs() -> dict[str, str]:
    """Private native-fixture text only. Never install these in the live mod."""
    code = MARK + 'technologies = {\n'
    loc = 'l_english:\n' + MARK
    for kind, (_, label, ceiling) in KINDS.items():
        for level in range(1, ceiling + 1):
            key = technology_id(kind, level)
            code += (f'\t{key} = {{\n\t\tallow = {{ always = no }}\n'
                     f'\t\tenable_building = {{ building = {kind} level = {level} }}\n'
                     '\t\tresearch_cost = 1\n\t\tstart_year = 1970\n'
                     '\t\tai_will_do = { factor = 0 }\n\t}\n')
            loc += f' {key}:0 "{label} {level}"\n'
            institution = 'public works' if kind == 'infrastructure' else 'national air defence'
            loc += (f' {key}_desc:0 "National {institution} construction standards '
                    f'authorise building up to level {level}."\n')
    code += '}\n'
    return {'common/technologies/COLDWAR_QUEUE_construction.txt': code,
            'localisation/english/COLDWAR_QUEUE_construction_l_english.yml': loc}
