# IMPERIA CW — Cold War: uae 1970 — focus delivery.
"""Foreign consent delivered by focuses; no domestic course or extra PP fee.

The diplomatic compiler owns executable providers and native price previews.
This module owns only the explicit focus-to-offer routing and fixed partners.
Domestic programme benefits/costs belong to the normal focus ledger.
"""
from copy import deepcopy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = 'COLDWAR_UAE_'
DECISIONS = frozenset({'oil_restraint', 'reserve_deposit', 'reserve_withdraw'})
FOCUS_OFFERS = {
    'nine_states': ('bahrain', 'qatar'),
    'arab_solidarity': ('arab_exchange',),
    'state_participation': ('participation',),
    'air_coastal_shield': ('procurement',),
    'security_contracts': ('training_offer',),
    'technical_exchange': ('exchange_offer',),
    'enduring_protection': ('british_cofinance',),
    'kuwait_support': ('kuwait_support',),
    'kuwait_transit': ('kuwait_transit',),
    'kuwait_deployment': ('kuwait_deployment',),
}
OFFER_TARGETS = {
    'bahrain': 'BHR', 'qatar': 'QAT', 'arab_exchange': 'EGY',
    'participation': 'ENG', 'procurement': 'ENG', 'training_offer': 'ENG',
    'exchange_offer': 'SOV', 'british_cofinance': 'ENG',
    'kuwait_support': 'KUW', 'kuwait_transit': 'KUW', 'kuwait_deployment': 'KUW',
}
OFFER_FOCUSES = {offer: focus for focus, offers in FOCUS_OFFERS.items() for offer in offers}


def focus_action(key: str, preview: bool = False) -> str:
    """Return native calls for a full focus ID, focus suffix or offer key.

    Unknown/non-diplomatic focuses intentionally return no additional action.
    Actual calls request one non-replayed delivery. Preview calls are always
    nonexecuting, native conditional prices and the actual negotiated effects.
    """
    key = key.removeprefix(P)
    offers = FOCUS_OFFERS.get(key, (key,) if key in OFFER_TARGETS else ())
    stem = 'focus_preview_' if preview else 'focus_'
    return '\n'.join(P + stem + offer + ' = yes' for offer in offers)


def focus_available(key: str) -> str:
    """Partner validity only; no treasury, programme receipt or party veto.

    An already issued/accepted offer satisfies its side of the focus and is
    never duplicated merely because the government completes this programme.
    The host compiler may put these bookkeeping predicates in hidden_trigger.
    """
    key = key.removeprefix(P)
    offers = FOCUS_OFFERS.get(key, (key,) if key in OFFER_TARGETS else ())
    return '\n'.join(P + 'focus_partner_' + offer + '_available = yes' for offer in offers)


def programme_specs(data: dict) -> dict[str, dict]:
    """Retain canonical offer metadata after loaded decisions shrink to three."""
    original = json.loads((HERE / 'approved_design.json').read_text(encoding='utf-8'))
    result = {d['id'].removeprefix(P + 'decision_'): deepcopy(d) for d in original['decisions']}
    result.update({d['id'].removeprefix(P + 'decision_'): deepcopy(d) for d in data.get('decisions', [])})
    return result
