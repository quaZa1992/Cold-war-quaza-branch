# IMPERIA COLD WAR — European Communities 1970 membership integration.
"""MD's EU is switched off in the 1970 scenario (GAME_RULE_eu_disabled) and replaced by the
European Communities system (COLDWAR_EC). Nobody holds MD's EU_member idea there, so every
membership condition of the approved French design reads the EC membership trigger instead.
Applied after the frozen snapshots like the other revisions; the approved JSON inputs stay unchanged."""
import json

NATIVE = 'has_idea = EU_member'
EC = 'COLDWAR_EC_is_member = yes'


def _swap(value):
    if isinstance(value, str):
        return value.replace(NATIVE, EC)
    if isinstance(value, list):
        return [_swap(v) for v in value]
    if isinstance(value, dict):
        return {k: _swap(v) for k, v in value.items()}
    return value


def apply_ec_membership_revision(design):
    out = _swap(design)
    assert 'EU_member' not in json.dumps(out, ensure_ascii=False), 'An MD EU membership reference remains.'
    out['ec_membership_revision'] = {
        'project': 'IMPERIA COLD WAR',
        'replaced': NATIVE,
        'with': EC,
        'reason': 'MD EU is disabled in 1970; membership of the European Communities comes from the COLDWAR_EC system.',
    }
    return out
