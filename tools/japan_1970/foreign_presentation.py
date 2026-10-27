# IMPERIA CW — Cold War: conditional Japan diplomatic reward presentation.
"""Display the existing agreements without implying an immediate focus payout."""
import re
from pathlib import Path
from presentation import field
from check_script_grammar import parse

NAMES = {'USA': 'the United States', 'CHI': 'China', 'SOV': 'the Soviet Union',
         'TAI': 'Taiwan', 'KOR': 'South Korea', 'NKO': 'North Korea'}
LABELS = {'stability_factor': 'Stability', 'offices_productivity': 'Office productivity',
          'research_speed_factor': 'Research speed', 'navy_org_factor': 'Naval organisation'}
SOURCE = Path(__file__).resolve().parent / 'staging' / 'foreign'
OPINION_DAYS = {}
for filename in ('COLDWAR_JAP70_bilateral_opinion_modifiers.txt', 'COLDWAR_JAP70_multilateral_invitation_opinions.txt'):
    for modifier in parse((SOURCE / filename).read_text(encoding='utf-8'))[0].value:
        OPINION_DAYS[modifier.key] = int(field(modifier.value, 'days', '0'))


def opinion_line(ident):
    key = f'COLDWAR_JAP70_opinion_{ident}'
    if ident == 'korea_reconciliation_offer':
        key += '_KOR'
    days = OPINION_DAYS[key]
    duration = f' for §Y{days // 365} years§!' if days else ''
    return f'  Mutual opinion: §G+20§!{duration}'


def cost_line(cost, payer='Japan'):
    return f'  {payer} — Treasury: §R−${cost:.3f} billion§!'


def offer_tooltip(record, transaction):
    ident = record['focus']
    body = record['preview_body']
    cost_match = re.search(r'\$(\d+\.\d+) billion', body)
    if not cost_match:
        raise ValueError('Missing agreement cost: ' + ident)
    cost = float(cost_match.group(1))
    years = 3 if ident == 'coast_guard_exchange' else 5
    if ident in {'seoul_industrial_cooperation', 'asean_infrastructure',
                 'mekong_development', 'indochina_reconstruction'}:
        partners = {
            'seoul_industrial_cooperation': 'South Korea',
            'asean_infrastructure': 'current ASEAN members',
            'mekong_development': 'governments in Indochina and Burma',
            'indochina_reconstruction': 'governments in Indochina, Burma, Malaya, the Sunda Islands, Borneo and the Philippines',
        }
        building = 'Civilian Factory' if ident in {'seoul_industrial_cooperation', 'indochina_reconstruction'} else 'Infrastructure'
        lines = [f'Offer development financing to §Y{partners[ident]}§!.',
                 'The recipient chooses an eligible state it owns and controls.',
                 '§YFor each completed project:§!', cost_line(cost),
                 f'  Selected state — {building}: §G+1§!']
        if ident in {'seoul_industrial_cooperation', 'asean_infrastructure'}:
            lines.append('  Japan — Office productivity: §G+2%§! for §Y5 years§!')
        if ident != 'asean_infrastructure':
            lines.append(opinion_line(ident))
        return '\n'.join(lines)
    if transaction.get('decision', '').endswith('_invite'):
        if ident.startswith('asean_'):
            partners = 'current ASEAN members'
        elif ident == 'lng_contracts':
            partners = 'oil-producing countries'
        elif ident == 'developing_market_access':
            partners = 'countries with GDP per capita below $20,000'
        elif ident == 'global_science_exchange':
            partners = 'governments worldwide'
        elif ident == 'search_rescue_protocol':
            partners = 'coastal countries'
        else:
            partners = 'East Asia, Southeast Asia, Australia and New Zealand'
        lines = [f'Unlock diplomatic invitations to §Y{partners}§!.',
                 '§YFor each accepted invitation:§!',
                 cost_line(cost, 'Each signatory' if ident == 'global_science_exchange' else 'Japan')]
        if ident == 'asean_training':
            lines += [f'  Recipient — Research speed: §G+2%§! for §Y{years} years§!',
                      f'  Mutual opinion: §G+20§! for §Y{years} years§!']
        else:
            modifier = ('Research speed' if ident == 'global_science_exchange' else
                        'Office productivity' if ident in {'asean_trade_rules', 'lng_contracts', 'developing_market_access'} else 'Stability')
            lines += [f'  Both signatories, for §Y{years} years§!:',
                      f'    {modifier}: §G+2%§!', '    Mutual opinion: §G+20§!']
        return '\n'.join(lines)
    if transaction.get('recipients'):
        lines = ['Send separate proposals to §YNorth Korea§! and §YSouth Korea§!.',
                 '§YFor each accepted proposal:§!', cost_line(cost)]
    else:
        lines = [f'Send a proposal to §Y{NAMES[transaction["recipient"]]}§!.',
                 '§YIf accepted:§!', cost_line(cost)]
    modifier = transaction.get('modifier', '').split('=')[0]
    if modifier:
        lines.append(f'  Both signatories — {LABELS[modifier]}: §G+2%§! for §Y5 years§!')
    lines.append(opinion_line(ident))
    return '\n'.join(lines)
