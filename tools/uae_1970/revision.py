# IMPERIA CW — Cold War: uae 1970 — revision.
"""Explicit user revisions layered over the immutable original UAE approval.

The October 19 correction separates independence, constitutional preparation,
and proclamation, and makes the protected-state opening usable without funding.
"""
from copy import deepcopy
import json
from pathlib import Path
from development import apply_revision
from streamline import apply_revision as streamline_revision
from focus_only import apply_revision as focus_only_revision

HERE = Path(__file__).resolve().parent
P = 'COLDWAR_UAE_'


def current_design():
    data = json.loads((HERE / 'approved_design.json').read_text(encoding='utf-8'))
    by = {n['id'].removeprefix(P): n for n in data['nodes']}
    by['council']['available'] = 'is_subject = no'
    by['council']['description'] = (
        "British protection has ended, leaving the rulers responsible for the coast's external affairs and defence. "
        "Their separate courts and administrations must now decide how much authority to entrust to a common government."
    )
    by['treaty_coast']['treasury_cost_billion'] = 0
    by['treaty_coast']['available'] = 'is_subject_of = ENG'
    by['treaty_coast']['effect_body'] = 'COLDWAR_UAE_refresh_programmes = yes'
    by['treaty_coast']['reward_summary'] = [
        'Bureaucracy spending multiplier: -5% while under British protection.',
        'Unlocks the existing withdrawal and treaty-amendment talks.',
    ]
    by['sovereign_union']['description'] = (
        "The end of Britain's special treaty responsibilities leaves the coast to conduct its own foreign affairs and defence. "
        "The rulers can put their agreed constitutional settlement into effect and prepare to proclaim their union."
    )
    by['sovereign_union']['reward_summary'] = ['Opens the proclamation of the federation after actual independence.']
    by['sovereign_union']['effect_body'] = '# Independence acknowledged; the following focus proclaims the federation.'
    node = deepcopy(by['sovereign_union'])
    node.update(
        id=P + 'proclaim_federation', title='Proclaim the Union',
        narrative_title='Proclaim the Union', xy=[5, 6], days=21, cost=3.0,
        prerequisites=[[P + 'sovereign_union']], mutually_exclusive=[],
        icon='national_unity',
        description=(
            "The rulers have agreed how their emirates will share authority, and British protection has ended. "
            "Proclaiming the United Arab Emirates gives the settlement a common name and establishes its federal offices. "
            "A federation must now reconcile the interests of the ruling houses with the responsibilities of an independent state."
        ),
        reward_summary=['Forms the United Arab Emirates and establishes the federal presidency.'],
        effect_body='COLDWAR_UAE_form_federation = yes',
    )
    data['nodes'].insert(data['nodes'].index(by['sovereign_union']) + 1, node)
    for key in ['rak_accession', 'federal_council']:
        by[key]['prerequisites'] = [[P + 'proclaim_federation']]
        by[key]['xy'][1] = 7
    by['dirham']['xy'][1] = 8
    data = apply_revision(data)
    # User-requested military trade-off: slower organisation recovery instead
    # of reducing the recruitable-population pool. Keep the workforce benefit.
    expatriates = next(s for s in data['starting_spirits'] if s['id'] == P+'expatriate_workforce')
    expatriates['modifiers'].pop('conscription_factor')
    expatriates['modifiers']['army_morale_factor'] = -0.20
    data['modifier_labels']['army_morale_factor'] = ['Division Recovery Rate', 'percent']
    # Explicit user revision: every UAE national focus takes seventy days,
    # including the later federation/industrial additions. Keep this last so
    # earlier development overlays cannot restore their former durations.
    for focus in data['nodes']:
        focus.update(days=70, cost=10.0)
    return focus_only_revision(streamline_revision(data))
