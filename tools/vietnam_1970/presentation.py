# IMPERIA CW — Cold War: vietnam 1970 — presentation.
"""English presentation corrections; no changes to approved gameplay values."""
import re

PROGRAMME_NAMES = {
    'state': 'National Institutions',
    'duan': 'Revolution and Reunification',
    'chinh': 'Doctrine and Reassessment',
    'linh': 'Doi Moi',
    'kiet': 'Practical Government',
    'front': 'Independent Front Socialism',
    'dem': 'Constitutional Government',
    'soc': 'A Pluralist Left',
    'nat': 'Nationalist Republicanism',
    'junta': 'Military Government',
    'industry': 'Reconstruction and Industry',
    'farm': 'Agriculture and Food Supply',
    'army': "People's Armed Forces",
    'unity': 'National Reunification',
    'diplomacy': 'Foreign Relations',
}

def clean_ui(text):
    text = text.replace('An explicitly alternate pre-1990 opening.', 'An alternative early diplomatic opening.')
    text = text.replace('A temporary adjustment programme; no automatic Soviet collapse or backdated 1991 event.',
                        'A temporary adjustment to a disruption in patron support.')
    text = text.replace('In January 1970 Le Duan', 'Le Duan')
    text = text.replace('historical 1986 chief succession', 'historical leadership succession')
    text = text.replace('historical 1970 coup', 'historical coup')
    # Preserve native format expressions and localization references. Their minus
    # control character determines value colour; it is not visible punctuation.
    parts = re.split(r'(\$[^$]+\$)', text)
    for i in range(0, len(parts), 2):
        value = re.sub(r'\s*[\u2013\u2014]\s*', ', ', parts[i])
        value = re.sub(r'[-\u2010\u2011\u2012\u2212]', ' ', value)
        parts[i] = re.sub(r' {2,}', ' ', value)
    return ''.join(parts)
