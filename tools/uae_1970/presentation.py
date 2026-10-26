# IMPERIA CW — Cold War: uae 1970 — presentation.
"""Native MD focus-effect presentation, with no imported compiler or file writes.

Returned snippets belong INSIDE the compiler's existing effect_tooltip block.
They describe hypothetical rewards; actual guarded transactions remain owned by
compile.py. Temporary arithmetic follows main MD's UK/GDP preview pattern.
"""
from __future__ import annotations
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import re
from development import POPULATION_GROWTH_CAP
from maritime import OIL_PHASES, MARITIME_FOCUSES, SCALED_MODIFIERS, scale_effect, scaled_value

ROOT = Path(__file__).resolve().parents[2]
MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
P = 'COLDWAR_UAE_'
POLITICAL = {'monarchy', 'constitutional', 'arab', 'left', 'islah'}
FLAG_LABELS = {
    P+'broad_charter_accepted': 'Broad federal settlement accepted',
    P+'oil_participation_accepted': 'Oil participation agreement accepted',
    P+'friendship_accepted': 'Anglo-Emirati friendship treaty accepted',
    P+'protection_accepted': 'Renewed British protection compact accepted',
    P+'federation_established': 'The federation has been established',
    P+'islah_organised': 'Al Islah has been legally recognised',
}


def _block(key, body):
    return key + ' = {\n' + '\n'.join('\t'+line if line else '' for line in body.strip().splitlines()) + '\n}'


def _suffix(node):
    return node['id'].removeprefix(P)


def _done(node):
    return P+'done_'+_suffix(node)


def _runtime(condition):
    return condition.replace('nationalist_monarchists_are_in_power = yes', P+'monarchy_government = yes')


@lru_cache(maxsize=1)
def _localisation():
    native, labels = {}, {}
    paths = [GAME/'localisation/english/modifiers_l_english.yml',
             MD/'localisation/english/MD_dm_modifiers_l_english.yml',
             ROOT/'localisation/english/MD_dm_modifiers_l_english.yml',
             ROOT/'localisation/english/replace/replaced_from_vanilla_modifiers_l_english.yml']
    for path in paths:
        if path.exists():
            entries = dict(re.findall(r'(?m)^\s*([^\s:#]+):(?:\d+)?\s*"([^\r\n]*)"', path.read_text(encoding='utf-8-sig')))
            native.update(entries)
            labels.update(entries)
    # Custom Imperia labels have native registered modifiers but may not have
    # their own variable-effect formatter. Reuse their real name when needed.
    for path in sorted((ROOT/'localisation/english').glob('*.yml')):
        if not path.name.startswith('COLDWAR_UAE_'):
            labels.update(dict(re.findall(r'(?m)^\s*([^\s:#]+):(?:\d+)?\s*"([^\r\n]*)"', path.read_text(encoding='utf-8-sig'))))
    return native, labels


def native_tooltip_keys():
    """Existing native formatter inventory, for integration validators."""
    return frozenset(key for key in _localisation()[0] if key.endswith('_tt'))


def native_tooltip_key(modifier, data, loc):
    """Prefer MD/vanilla's exact formatter; register only missing fallbacks."""
    native, labels = _localisation()
    key = modifier+'_tt'
    if key in native:
        return key
    candidates = [modifier, 'MODIFIER_'+modifier.upper(), 'modifier_'+modifier]
    label_key = next((name for name in candidates if name in labels), None)
    if label_key:
        aliases = [key for key, text in native.items() if key.endswith('_tt')
                   and '$'+label_key+'$' in text and '$RIGHT|' in text]
        if len(aliases) == 1:
            return aliases[0]
    if modifier not in data['modifier_labels']:
        raise ValueError('Unreviewed modifier formatter: '+modifier)
    label, unit = data['modifier_labels'][modifier]
    label = '$'+label_key+'$' if label_key else label
    expense = any(part in modifier for part in ('cost_', 'energy_use', 'supply_consumption',
                   'training_time', 'worker_requirement', 'interest_rate'))
    colour = '-=' if expense else '+='
    formatter = '%1' if unit in {'percent', 'fraction_pp'} else '0' if unit == 'integer' else '2'
    fallback = P+'tt_'+modifier
    loc[fallback] = label+': $RIGHT|'+colour+formatter+'$'
    return fallback


def _condition(condition, loc):
    result = _runtime(condition).strip()
    for flag, text in FLAG_LABELS.items():
        if 'has_country_flag = '+flag in result:
            key = flag+'_tt'
            loc[key] = text
            result = result.replace('has_country_flag = '+flag,
                                    'custom_trigger_tooltip = { tooltip = '+key+' has_country_flag = '+flag+' }')
    return result


def _heading(modifier):
    return 'custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = '+modifier+' }'


def _set(variable, value):
    return f'set_temp_variable = {{ {variable} = {value:g} }}' if isinstance(value, (float, int)) else f'set_temp_variable = {{ {variable} = {value} }}'


def _delta_line(variable, value, modifier, data, loc):
    return f'add_to_variable = {{ {variable} = {value} tooltip = {native_tooltip_key(modifier, data, loc)} }}'


def _component_setup(node, data, spirit, modifier):
    """Exact before/after mirrors programme_outputs' persistent spirit maths."""
    base = spirit['modifiers'][modifier]
    stem = P+'preview_'+spirit['id'].removeprefix(P)+'_'+modifier
    before, after, delta = stem+'_before', stem+'_after', stem+'_delta'
    rows = [_set(before, base), _set(after, base)]
    families = defaultdict(list)
    for candidate in data['nodes']:
        for change in candidate.get('spirit_changes', []):
            if change['spirit'] == spirit['id'] and change['component'] == modifier:
                relief = abs(base-change['value']) if change['operation'] == 'set' else abs(change['value'])
                families[change['family']].append((relief, candidate))
    for number, (family, members) in enumerate(families.items()):
        current, future = stem+f'_credit_{number}', stem+f'_future_credit_{number}'
        rows += [_set(current, 0), _set(future, 0)]
        for relief, candidate in sorted(members, key=lambda row: (row[0], _suffix(row[1]))):
            earned = 'has_country_flag = '+_done(candidate)
            rows.append(_block('if', 'limit = { '+earned+' }\n'+_set(current, relief)))
            guard = 'always = yes' if candidate['id'] == node['id'] else earned
            rows.append(_block('if', 'limit = { '+guard+' }\n'+_set(future, relief)))
        operation = 'subtract_from_temp_variable' if base > 0 else 'add_to_temp_variable'
        rows += [f'{operation} = {{ {before} = {current} }}', f'{operation} = {{ {after} = {future} }}']
    if spirit['id'] == P+'unequal_development' and modifier == 'stability_factor':
        rows.append(_block('if', 'limit = { has_country_flag = '+P+'mediate_settled }\n'+_set(before, 0)+'\n'+_set(after, 0)))
    if spirit['id'] == P+'fragmented_authority' and modifier == 'bureaucracy_cost_multiplier_modifier':
        rows.append(_block('if', 'limit = { has_country_flag = '+P+'cabinet_settled }\n'+
            f'subtract_from_temp_variable = {{ {before} = 0.03 }}\nsubtract_from_temp_variable = {{ {after} = 0.03 }}'))
        if _suffix(node) == 'rulers_compact':
            rows.append(_block('if', 'limit = { NOT = { has_country_flag = '+P+'cabinet_settled } }\n'+
                f'subtract_from_temp_variable = {{ {after} = 0.03 }}'))
    clamp = 'min' if base > 0 else 'max'
    rows += [f'clamp_temp_variable = {{ var = {before} {clamp} = 0 }}',
             f'clamp_temp_variable = {{ var = {after} {clamp} = 0 }}']
    if spirit['id'] == P+'maritime_livelihoods' and modifier in SCALED_MODIFIERS:
        current_scale, future_scale = stem+'_current_share', stem+'_future_share'
        rows += [scale_effect(current_scale, temporary=True),
                 scale_effect(future_scale, temporary=True, prospective=_suffix(node)),
                 f'multiply_temp_variable = {{ {before} = {current_scale} }}',
                 f'multiply_temp_variable = {{ {after} = {future_scale} }}']
    rows += [_set(delta, after), f'subtract_from_temp_variable = {{ {delta} = {before} }}']
    return rows, before, after, delta


def spirit_change_preview(node, data, loc):
    """Named native current-to-post deltas, with strongest-family/clamp rules."""
    affected = defaultdict(list)
    for change in node.get('spirit_changes', []):
        if change['component'] not in affected[change['spirit']]:
            affected[change['spirit']].append(change['component'])
    rows = []
    for spirit_id, modifiers in affected.items():
        spirit = next(s for s in data['starting_spirits'] if s['id'] == spirit_id)
        setup, deltas, post = [], {}, {}
        # All components are needed to truthfully preview full spirit removal.
        for modifier in spirit['modifiers']:
            code, _, after, delta = _component_setup(node, data, spirit, modifier)
            setup += code
            deltas[modifier], post[modifier] = delta, after
        rows += setup + [_heading(spirit_id)]
        for modifier in modifiers:
            rows.append(_delta_line(P+'preview_display', deltas[modifier], modifier, data, loc))
        condition = 'has_dynamic_modifier = { modifier = '+spirit_id+' }\n'+ '\n'.join(
            f'check_variable = {{ var = {variable} value = 0 compare = equals }}' for variable in post.values())
        rows.append(_block('if', _block('limit', condition)+'\nremove_dynamic_modifier = { modifier = '+spirit_id+' }'))
    return '\n'.join(rows)


def _stability_delta(node, data):
    """Cap only positive contributions exactly as the programme reconciler."""
    before, after, delta = (P+'preview_positive_stability_'+tail for tail in ('before', 'after', 'delta'))
    rows = [_set(before, 0)]
    for candidate in data['nodes']:
        value = candidate['modifiers'].get('stability_factor', 0)
        if candidate['group'] != node['group'] or value <= 0:
            continue
        guard = ['has_country_flag = '+_done(candidate), _runtime(candidate['active_condition'])]
        if candidate['temporary_days']:
            guard.append('has_country_flag = '+P+'temporary_'+_suffix(candidate))
        rows.append(_block('if', _block('limit', '\n'.join(guard))+
                           f'\nadd_to_temp_variable = {{ {before} = {value:g} }}'))
    rows += [_set(after, before)]
    rows.append(_block('if', 'limit = { NOT = { has_country_flag = '+_done(node)+' } }\n'+
                       f'add_to_temp_variable = {{ {after} = {node["modifiers"]["stability_factor"]:g} }}'))
    rows += [f'clamp_temp_variable = {{ var = {before} max = 0.15 }}',
             f'clamp_temp_variable = {{ var = {after} max = 0.15 }}',
             _set(delta, after), f'subtract_from_temp_variable = {{ {delta} = {before} }}']
    return rows, delta


def _population_delta(node, data):
    """Native numeric preview of the additional growth within the total cap."""
    before, after, delta = (P+'preview_population_'+tail for tail in ('before', 'after', 'delta'))
    rows = [_set(before, 0)]
    for candidate in data['nodes']:
        value = candidate['modifiers'].get('monthly_population', 0)
        if not value:
            continue
        guards = ['has_country_flag = '+_done(candidate), _runtime(candidate['active_condition'])]
        if candidate['temporary_days']:
            guards.append('has_country_flag = '+P+'temporary_'+_suffix(candidate))
        rows.append(_block('if', _block('limit', '\n'.join(guards))+f'\nadd_to_temp_variable = {{ {before} = {value:g} }}'))
    rows.append(_set(after, before))
    rows.append(_block('if', 'limit = { NOT = { has_country_flag = '+_done(node)+' } }\n'+
                       f'add_to_temp_variable = {{ {after} = {node["modifiers"]["monthly_population"]:g} }}'))
    rows += [f'clamp_temp_variable = {{ var = {before} max = {POPULATION_GROWTH_CAP:g} }}',
             f'clamp_temp_variable = {{ var = {after} max = {POPULATION_GROWTH_CAP:g} }}',
             _set(delta, after), f'subtract_from_temp_variable = {{ {delta} = {before} }}']
    return rows, delta


def programme_preview(node, data, loc):
    main = node['modifiers']
    extra = [(c['condition'], {k: v for k, v in c['modifiers'].items() if k not in main})
             for c in node.get('conditional_contributions', [])]
    if not main and not any(modifiers for _, modifiers in extra):
        return ''
    body, setup = [], []
    coastal = _suffix(node) in MARITIME_FOCUSES
    coastal_scale = P+'preview_maritime_share'
    if coastal:
        setup.append(scale_effect(coastal_scale, temporary=True))
    for modifier, value in main.items():
        if coastal and modifier in SCALED_MODIFIERS:
            amount = P+'preview_maritime_'+modifier
            setup.append(scaled_value(amount, value, coastal_scale))
            body.append(_delta_line(P+node['group']+'_'+modifier, amount, modifier, data, loc))
        elif node['group'] in POLITICAL and modifier == 'stability_factor' and value > 0:
            calculation, delta = _stability_delta(node, data)
            setup += calculation
            body.append(_delta_line(P+node['group']+'_'+modifier, delta, modifier, data, loc))
        elif modifier == 'monthly_population':
            calculation, delta = _population_delta(node, data)
            setup += calculation
            body.append(_delta_line(P+node['group']+'_'+modifier, delta, modifier, data, loc))
        else:
            effect = _delta_line(P+node['group']+'_'+modifier, f'{value:g}', modifier, data, loc)
            if _suffix(node) == 'citizen_republic' and modifier == 'stability_factor' and value < 0:
                effect = _block('if', 'limit = { NOT = { has_country_flag = '+P+'court_settled } }\n'+effect)
            body.append(effect)
    for condition, modifiers in extra:
        if modifiers:
            values = '\n'.join(_delta_line(P+node['group']+'_'+k, f'{v:g}', k, data, loc) for k, v in modifiers.items())
            # Preview prospective agreement terms even before acceptance, as
            # in native MD. Real delivery remains in the guarded reconciler.
            body.append('custom_effect_tooltip = TT_IF_THEY_ACCEPT\n'+values)
    if node['temporary_days']:
        key = P+'presentation_duration_'+_suffix(node)
        loc[key] = 'Duration: §Y'+str(node['temporary_days'])+' days§!'
        body.append('custom_effect_tooltip = '+key)
    terms = ['custom_effect_tooltip = TT_IF_THEY_ACCEPT'] if _suffix(node) in {'british_friendship', 'state_participation'} else []
    # available already presents the government/status prerequisites. Wrapping
    # advertised numbers in their current truth value produces empty hovers.
    return '\n'.join(setup+terms+[_heading(P+node['group']+'_programme')]+body)


def maritime_oil_preview(node, data, loc):
    """Native marginal losses on existing coastal sources, never future grants."""
    if _suffix(node) not in OIL_PHASES:
        return ''
    spirit = next(s for s in data['starting_spirits'] if s['id'] == P+'maritime_livelihoods')
    rows, changes = [], []
    for modifier in SCALED_MODIFIERS:
        setup, _, _, delta = _component_setup(node, data, spirit, modifier)
        rows += setup
        changes.append(_delta_line(P+'preview_display', delta, modifier, data, loc))
    rows += [_heading(spirit['id'])] + changes
    current, future, change = (P+'preview_maritime_share_'+suffix for suffix in ('before', 'after', 'delta'))
    rows += [scale_effect(current, temporary=True),
             scale_effect(future, temporary=True, prospective=_suffix(node)),
             _set(change, future), f'subtract_from_temp_variable = {{ {change} = {current} }}']
    coastal_nodes = [n for n in data['nodes'] if _suffix(n) in MARITIME_FOCUSES]
    earned = 'OR = { '+ ' '.join('has_country_flag = '+_done(n) for n in coastal_nodes)+' }'
    commerce, commerce_changes = [], []
    for modifier in SCALED_MODIFIERS:
        amount = P+'preview_maritime_existing_'+modifier
        commerce.append(_set(amount, 0))
        for coastal in coastal_nodes:
            value = coastal['modifiers'].get(modifier, 0)
            if value:
                condition = 'has_country_flag = '+_done(coastal)+'\n'+_runtime(coastal['active_condition'])
                commerce.append(_block('if', _block('limit', condition)+'\n'+
                    f'add_to_temp_variable = {{ {amount} = {value:g} }}'))
        commerce.append(f'multiply_temp_variable = {{ {amount} = {change} }}')
        commerce_changes.append(_delta_line(P+'preview_display', amount, modifier, data, loc))
    rows.append(_block('if', 'limit = { '+earned+' }\n'+'\n'.join(
        commerce+[_heading(P+'commerce_programme')]+commerce_changes)))
    return '\n'.join(rows)


def special_preview(node, data, loc):
    key = _suffix(node)
    if key == 'rulers_compact':
        spirit = next(s for s in data['starting_spirits'] if s['id'] == P+'fragmented_authority')
        setup, remaining, deltas = [], {}, {}
        for modifier in spirit['modifiers']:
            code, _, after, delta = _component_setup(node, data, spirit, modifier)
            setup += code
            remaining[modifier], deltas[modifier] = after, delta
        rows = setup + [_heading(spirit['id']), _delta_line(spirit['id']+'_bureaucracy_cost_multiplier_modifier', deltas['bureaucracy_cost_multiplier_modifier'],
                'bureaucracy_cost_multiplier_modifier', data, loc)]
        cleared = 'has_dynamic_modifier = { modifier = '+spirit['id']+' }\n'+'\n'.join(
            f'check_variable = {{ var = {variable} value = 0 compare = equals }}' for variable in remaining.values())
        rows.append(_block('if', _block('limit', cleared)+'\nremove_dynamic_modifier = { modifier = '+spirit['id']+' }'))
        rows.append(_block('if', 'limit = { date < 1990.10.7 NOT = { has_country_flag = '+P+'rashid_president } }\n'+
                    'add_ideas = '+P+'prime_minister_rashid'))
        return '\n'.join(rows)
    if key == 'sovereign_union':
        tooltip = P+'unlock_proclamation_tt'
        loc[tooltip] = 'Unlocks §Y$COLDWAR_UAE_proclaim_federation$§!.'
        return 'custom_effect_tooltip = '+tooltip
    if key == 'proclaim_federation':
        return 'drop_cosmetic_tag = yes\n'+_federal_office_preview()
    if key == 'dirham':
        return 'add_ideas = COLDWAR_UAE_dirham_currency'
    offers = {'renew_protection': (1001, ''),
              'british_friendship': (3001, 'NOT = { has_country_flag = COLDWAR_UAE_friendship_accepted }')}
    if key in offers:
        ident, condition = offers[key]
        event = 'ENG = { country_event = { id = COLDWAR_UAE_1970_contracts.'+str(ident)+' } }'
        return _block('if', 'limit = { '+condition+' }\n'+event) if condition else event
    return ''


def _federal_office_preview():
    """Native appointment effects, matching the existing dated office provider."""
    def leader(name, picture):
        body = []
        for keyword, ideology, trait in [('if', 'Western_Autocracy', 'western_Western_Autocracy'),
                                         ('else', 'Monarchist', 'nationalist_Monarchist')]:
            guard = 'limit = { check_variable = { ruling_party = 0 } }\n' if keyword == 'if' else ''
            body.append(_block(keyword, guard+_block('create_country_leader',
                f'name = "{name}"\npicture = "{picture}"\nideology = {ideology}\ntraits = {{ king {trait} }}')))
        return '\n'.join(body)
    # Actual formation resets president to0; dated native succession then
    # replaces an expired office holder. Rashid's alternate presidency is not
    # selected by the formation transaction and is therefore not advertised.
    appointments = _block('if', 'limit = { date > 2022.5.12 }\n'+
        leader('Mohammed bin Zayed Al Nahyan', 'gfx/leaders/UAE/mohammed_bin_zayed_al_nahyan.dds'))
    appointments += '\n'+_block('else_if', 'limit = { date > 2004.11.1 }\n'+
        leader('Khalifa bin Zayed Al Nahyan', 'gfx/leaders/UAE/khalifa_bin_zayed_al_nahyan.dds'))
    appointments += '\n'+_block('else', leader('Zayed bin Sultan Al Nahyan', 'gfx/leaders/UAE/zayed_bin_sultan_al_nahyan.dds'))
    cabinet = _block('if', 'limit = { has_country_flag = '+P+'cabinet_settled date < 1990.10.7 }\n'+
                     'add_ideas = '+P+'prime_minister_rashid')
    cabinet += '\n'+_block('else_if', 'limit = { date < 2006.1.4 }\nadd_ideas = '+P+'prime_minister_maktoum')
    return _block('if', 'limit = { '+P+'monarchy_government = yes }\n'+appointments+'\n'+cabinet)
