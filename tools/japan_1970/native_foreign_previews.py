# IMPERIA COLD WAR — Native prospective effects for Japan 1970 foreign offers.
"""Build non-executing focus previews from the accepted transaction terms."""
import json
from pathlib import Path

from check_script_grammar import Entry, parse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / 'staging' / 'foreign'
HELPER_PREFIX = 'COLDWAR_JAP70_preview_acceptance_'


def _field(entries, key, default=None):
    return next((node.value for node in entries if node.key == key), default)


def _named(entries, key):
    return [node for node in entries if node.key == key and isinstance(node.value, list)]


def _event_acceptance(path, ident, event_id=None):
    tree = parse(path.read_text(encoding='utf-8'))
    for event in tree:
        if event.key != 'country_event' or not isinstance(event.value, list):
            continue
        if event_id is not None and _field(event.value, 'id') != event_id:
            continue
        for option in _named(event.value, 'option'):
            if _field(option.value, 'name') != ident:
                continue
            block = next((x.value for x in option.value
                          if x.key == 'effect_tooltip' and isinstance(x.value, list)), None)
            if block is None:
                raise ValueError(f'Missing acceptance preview block for {ident}')
            return block
    raise ValueError(f'Missing acceptance option {ident} in {path.name}')


def _project_acceptance(path, ident):
    tree = parse(path.read_text(encoding='utf-8'))
    for category in tree:
        if not isinstance(category.value, list):
            continue
        for decision in _named(category.value, ident):
            complete = next((n.value for n in decision.value
                             if n.key == 'complete_effect' and isinstance(n.value, list)), None)
            if complete is None:
                break
            preview = next((n.value for n in complete
                            if n.key == 'effect_tooltip' and isinstance(n.value, list)), None)
            if preview is None:
                raise ValueError(f'Missing completed-project preview for {ident}')
            return preview
    raise ValueError(f'Missing project decision {ident}')


def _expiry_days(nodes):
    for node in nodes:
        if node.key == 'country_event' and isinstance(node.value, list):
            days = _field(node.value, 'days')
            if days and str(days).isdigit():
                return int(days)
        if isinstance(node.value, list):
            found = _expiry_days(node.value)
            if found:
                return found
    return None


def _clean(nodes):
    """Remove bookkeeping and timers while exposing guarded reward terms."""
    result = []
    for node in nodes:
        if node.key in {'country_event', 'set_country_flag', 'clr_country_flag',
                        'log'}:
            continue
        if node.key == 'if' and isinstance(node.value, list):
            # Acceptance scripts guard only a repeatable dynamic-spirit add.
            # Preview its reward independently of the current active state.
            then = next((child.value for child in node.value
                         if child.key in {'limit', 'else'} and isinstance(child.value, list)), None)
            if then is None:
                then = [child for child in node.value if child.key not in {'limit', 'else'}]
            else:
                then = [child for child in node.value if child.key not in {'limit', 'else'}]
            result.extend(_clean(then))
            continue
        if isinstance(node.value, list):
            result.append(Entry(node.key, node.operator, _clean(node.value), node.line))
        else:
            result.append(node)
    return result


def _rewrite_targets(nodes, recipient):
    rewritten = []
    for node in nodes:
        value = node.value
        if node.key == 'target' and value == 'ROOT':
            value = recipient
        elif isinstance(value, list):
            value = _rewrite_targets(value, recipient)
        rewritten.append(Entry(node.key, node.operator, value, node.line))
    return rewritten


def _render(nodes, level=1):
    out = []
    pad = '\t' * level
    for node in nodes:
        if isinstance(node.value, list):
            out.append(f'{pad}{node.key} = {{')
            out.extend(_render(node.value, level + 1))
            out.append(f'{pad}}}')
        elif node.operator is None:
            out.append(f'{pad}{node.key}')
        else:
            out.append(f'{pad}{node.key} {node.operator} {node.value}')
    return out


def build_preview_source():
    """Return complete static helper source plus focus-to-helper coverage."""
    transactions = [json.loads(line) for line in
                    (OUT / 'bilateral_manifest.jsonl').read_text(encoding='utf-8').splitlines()
                    if line.strip()]
    bilateral = ROOT / 'events' / 'COLDWAR_JAP70_bilateral_events.txt'
    multilateral = ROOT / 'events' / 'COLDWAR_JAP70_multilateral_invitation_events.txt'
    projects = OUT / 'COLDWAR_JAP70_foreign_project_decisions.txt'
    lines = ['# IMPERIA COLD WAR — Non-executing Japan foreign-offer focus previews.']
    coverage = {}

    for transaction in transactions:
        focus = transaction['focus']
        helper = HELPER_PREFIX + focus
        if transaction.get('decision', '').endswith(('_site',)):
            raw = _project_acceptance(projects, transaction['decision'])
            expiry = _expiry_days(raw)
            recipient = transaction.get('recipient')
            if recipient:
                scope = recipient
            else:
                scope = 'random_country'
            recipient_effects = []
            japan_effects = []
            recipient_effects.append(Entry('unlock_decision_category_tooltip', '=',
                                           'COLDWAR_JAP70_foreign_projects_category', 1))
            site_heading_added = False
            for node in _clean(raw):
                if node.key == 'FROM' and isinstance(node.value, list):
                    state = _clean(node.value)
                    if not any(part.key == 'add_extra_state_shared_building_slots' for part in state):
                        state.insert(0, Entry('add_extra_state_shared_building_slots', '=', '1', node.line))
                    if not site_heading_added:
                        recipient_effects.append(Entry('custom_effect_tooltip', '=',
                                                       'COLDWAR_JAP70_foreign_recipient_selected_site_tt', node.line))
                        site_heading_added = True
                    recipient_effects.append(Entry('random_owned_state', '=', state, node.line))
                elif node.key == 'JAP' and isinstance(node.value, list):
                    japan_effects.extend(node.value)
                else:
                    recipient_effects.append(node)
            generic = recipient is None
            recipient_effects = _rewrite_targets(recipient_effects, 'JAP')
            japan_effects = _rewrite_targets(japan_effects, 'PREV' if generic else scope)
            if expiry and any(node.key == 'add_dynamic_modifier' for node in japan_effects):
                japan_effects.append(Entry('custom_effect_tooltip', '=',
                                           f'COLDWAR_JAP70_foreign_dynamic_duration_{expiry}_tt', 1))
            # Timed idea additions display their name in the native focus
            # preview. These extra numeric rows expose the exact modifier on
            # both signatories while keeping the real accepted effect intact.
            preview_rows = {
                'seoul_industrial_cooperation': ('COLDWAR_JAP70_seoul_package_recipient_tt', 'COLDWAR_JAP70_seoul_package_japan_tt'),
                'asean_infrastructure': (None, 'COLDWAR_JAP70_asean_package_japan_tt'),
                'mekong_development': ('COLDWAR_JAP70_mekong_package_recipient_tt', None),
                'indochina_reconstruction': ('COLDWAR_JAP70_indochina_package_recipient_tt', 'COLDWAR_JAP70_indochina_package_japan_tt'),
            }
            recipient_row, japan_row = preview_rows.get(focus, (None, None))
            if recipient_row:
                recipient_effects.append(Entry('custom_effect_tooltip', '=', recipient_row, 1))
            if japan_row:
                japan_effects.append(Entry('custom_effect_tooltip', '=', japan_row, 1))
            preview = [Entry('custom_effect_tooltip', '=', 'TT_IF_THEY_ACCEPT', 1)]
            if generic:
                preview.append(Entry('custom_effect_tooltip', '=',
                                     'COLDWAR_JAP70_foreign_accepting_country_tt', 1))
                recipient_effects.append(Entry('JAP', '=', japan_effects, 1))
                preview.append(Entry('random_country', '=', [
                    Entry('limit', '=', [Entry('NOT', '=', [Entry('tag', '=', 'JAP', 1)], 1)], 1),
                    *recipient_effects], 1))
            else:
                preview.append(Entry(scope, '=', recipient_effects, 1))
            if japan_effects and not generic:
                preview.append(Entry('JAP', '=', japan_effects, 1))
        elif transaction.get('recipients'):
            preview = [Entry('custom_effect_tooltip', '=', 'TT_IF_THEY_ACCEPT', 1)]
            for recipient in transaction['recipients']:
                event_id = transaction.get('events', [])[transaction['recipients'].index(recipient)]
                event_name = f'COLDWAR_JAP70_BIL_{focus}_accept'
                raw = _clean(_event_acceptance(bilateral, event_name, event_id))
                recipient_effects, japan_effects = [], []
                for node in raw:
                    if node.key == 'JAP' and isinstance(node.value, list):
                        japan_effects.extend(node.value)
                    else:
                        recipient_effects.append(node)
                preview.append(Entry(recipient, '=', _rewrite_targets(recipient_effects, 'JAP'), 1))
                if japan_effects:
                    preview.append(Entry('JAP', '=', _rewrite_targets(japan_effects, recipient), 1))
        elif transaction.get('decision', '').endswith('_invite'):
            event_name = f'COLDWAR_JAP70_ML_{focus}_accept'
            raw_original = _event_acceptance(multilateral, event_name)
            expiry = _expiry_days(raw_original)
            raw = _clean(raw_original)
            recipient_effects, japan_effects = [], []
            for node in raw:
                if node.key == 'JAP' and isinstance(node.value, list):
                    japan_effects.extend(node.value)
                else:
                    recipient_effects.append(node)
            japan_effects = _rewrite_targets(japan_effects, 'PREV')
            if expiry and any(node.key == 'add_dynamic_modifier' for node in japan_effects):
                japan_effects.append(Entry('custom_effect_tooltip', '=',
                                           f'COLDWAR_JAP70_foreign_dynamic_duration_{expiry}_tt', 1))
            preview = [Entry('custom_effect_tooltip', '=', 'TT_IF_THEY_ACCEPT', 1),
                       Entry('custom_effect_tooltip', '=',
                             'COLDWAR_JAP70_foreign_accepting_country_tt', 1),
                       Entry('random_country', '=', [
                           Entry('limit', '=', [Entry('NOT', '=', [Entry('tag', '=', 'JAP', 1)], 1)], 1),
                           *_rewrite_targets(recipient_effects, 'JAP'),
                           Entry('JAP', '=', japan_effects, 1)], 1)]
        else:
            event_id = transaction.get('event') or transaction.get('offer_event')
            if not event_id:
                raise ValueError(f'Missing acceptance event for {focus}')
            accept_name = f'COLDWAR_JAP70_BIL_{focus}_accept'
            raw = _clean(_event_acceptance(bilateral, accept_name, event_id))
            recipient = transaction['recipient']
            recipient_effects, japan_effects = [], []
            for node in raw:
                if node.key == 'JAP' and isinstance(node.value, list):
                    japan_effects.extend(node.value)
                else:
                    recipient_effects.append(node)
            if focus == 'china_trade_framework':
                terms = 'COLDWAR_JAP70_china_trade_terms_tt'
                recipient_effects.append(Entry('custom_effect_tooltip', '=', terms, 1))
                japan_effects.append(Entry('custom_effect_tooltip', '=', terms, 1))
            elif focus == 'china_technology_exchange':
                terms = 'COLDWAR_JAP70_china_technology_terms_tt'
                recipient_effects.append(Entry('custom_effect_tooltip', '=', terms, 1))
                japan_effects.append(Entry('custom_effect_tooltip', '=', terms, 1))
            preview = [Entry('custom_effect_tooltip', '=', 'TT_IF_THEY_ACCEPT', 1),
                       Entry(recipient, '=', _rewrite_targets(recipient_effects, 'JAP'), 1)]
            if japan_effects:
                preview.append(Entry('JAP', '=', _rewrite_targets(japan_effects, recipient), 1))

        lines.append(f'{helper} = {{')
        lines.extend(_render(preview, 1))
        lines.append('}')
        coverage[focus] = helper
    lines.append('')
    source = '\n'.join(lines)
    if 'every_country =' in source:
        raise ValueError('Prospective offer previews must not fan out across every country')
    return source, coverage


def write_preview_source():
    content, coverage = build_preview_source()
    target = OUT / 'scripted_effects' / 'COLDWAR_JAP70_native_foreign_previews.txt'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')
    return target, coverage
