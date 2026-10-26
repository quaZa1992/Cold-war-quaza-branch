# IMPERIA CW — Cold War: GC equilibrium controls and graduated crisis penalties.
"""Bounded maintenance source; the old full equilibrium generator is absent.

Updates the existing GC category, three equilibrium effects and their English
tooltips. Does not regenerate bloc membership, assistance programmes or oil trade.
"""
from pathlib import Path
from decimal import Decimal
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/historical_politics_1970'))
from starting_identity import nodes, parse, first, walk
from script_ast import emit

HEADER = '# IMPERIA CW — Cold War: GC equilibrium controls and graduated crisis penalties.\n'
WORLD = 'common/scripted_effects/mdcw_cold_war_effects.txt'
LOC = 'localisation/english/mdcw_cold_war_l_english.yml'
GC = 'is_ai = no has_idea = imp_gc_nation has_global_flag = mdcw_cw_initialized'
FLAG = 'COLDWAR_gc_equilibrium_expanded'
P = 'COLDWAR_gc_cw_'


def block(name, code):
    return name + ' = {\n' + emit(parse(code), 1) + '\n}\n'


def protected(code):
    return 'if = { limit = { ' + GC + ' } ' + code + ' }'


def condition(body):
    test = first(first(body, 'limit', []), 'check_variable', [])
    return first(test, 'var'), first(test, 'value')


def adjust(rows, variable, amount, scaled):
    for index, (key, op, value) in enumerate(rows):
        if key in {'set_variable', 'add_to_variable'} and first(value, variable) is not None:
            if first(value, variable) == 'mdcw_cw_t_fx':
                for previous in range(index - 1, -1, -1):
                    if rows[previous][0] == 'set_temp_variable':
                        assert first(rows[previous][2], 'mdcw_cw_t_fx') is not None
                        rows[previous] = ('set_temp_variable', '=', [('mdcw_cw_t_fx', '=', amount)])
                        return
                raise AssertionError('Missing exposure-scaled coefficient: ' + variable)
            rows[index] = (key, op, [(variable, '=', amount)])
            return
    if scaled:
        rows.extend(parse(f'set_temp_variable = {{ mdcw_cw_t_fx = {amount} }} multiply_temp_variable = {{ mdcw_cw_t_fx = mdcw_cw_wm_exposure }} add_to_variable = {{ {variable} = mdcw_cw_t_fx }}'))
    else:
        rows.append(('add_to_variable', '=', [(variable, '=', amount)]))


def patch_effect(source, name, config):
    node = next(n for n in nodes(source) if n['key'] == name)
    body = node['value']
    applied = set()
    for key, op, branch in walk(body):
        if key not in {'if', 'else_if'} or not isinstance(branch, list):
            continue
        variable, tier = condition(branch)
        track = {'global.mdcw_cw_market': 'market', 'global.mdcw_cw_arms': 'arms',
                 'global.mdcw_cw_tension': 'tension', 'mdcw_cw_oil_crisis_ratio': 'oil'}.get(variable)
        if track is None or tier not in config[track]:
            continue
        for stat, amount in config[track][tier].items():
            adjust(branch, stat, amount, track == 'market')
        applied.add((track, tier))
    expected = {(track, tier) for track in (('oil',) if name.endswith('oil_crisis_tier') else ('market', 'arms', 'tension')) for tier in config[track]}
    assert applied == expected, ('Missing native tier', expected - applied)
    replacement = name + ' = {\n' + emit(body, 1) + '\n}'
    marker = '# IMPERIA CW — Cold War: penalties increase through every crisis stage.\n'
    if not source[:node['start']].endswith(marker):
        replacement = marker + replacement
    return source[:node['start']] + replacement + source[node['end']:]


def make_helpers():
    out = HEADER
    for track, minimum in (('market', 5), ('arms', 0)):
        out += block(P + 'apply_' + track, f'''
            set_variable = {{ global.{P}{track}_base = global.mdcw_cw_{track} }}
            add_to_variable = {{ global.mdcw_cw_{track} = global.{P}{track}_adjustment }}
            clamp_variable = {{ var = global.mdcw_cw_{track} min = {minimum} max = 100 }}
            round_variable = global.mdcw_cw_{track}
        ''') + '\n'
    out += block(P + 'refresh', '''
        mdcw_cw_update_world_situation = yes
        IMP_cold_war_recalculate_military_industrial_complex = yes
        imp_update_oil_price_display = yes
        every_country = {
            limit = { has_country_flag = mdcw_cw_initialized }
            set_temp_variable = { imp_oil_factor_t = global.imp_global_oil_price }
            mdcw_cw_oil_effective_price = yes
            set_variable = { mdcw_cw_oil_crisis_ratio = imp_oil_factor_t }
            divide_variable = { mdcw_cw_oil_crisis_ratio = 75 }
            if = { limit = { check_variable = { imp_oil_factor_t > 75 } }
                imp_calculate_oil_dynamic_modifiers_high = yes
            }
            else = { imp_calculate_oil_dynamic_modifiers_low = yes }
            mdcw_cw_update_oil_crisis_tier = yes
            if = { limit = { has_idea = defense_industry }
                set_variable = { IMP_military_industrial_complex_tension_bonus = global.IMP_military_industrial_complex_tension_bonus }
                set_variable = { IMP_military_industrial_complex_war_bonus = global.IMP_military_industrial_complex_war_bonus }
                set_variable = { IMP_military_industrial_complex_tax_bonus = global.IMP_military_industrial_complex_total_bonus }
                if = { limit = { NOT = { has_dynamic_modifier = { modifier = IMP_military_industrial_complex_dynamic_modifier } } }
                    add_dynamic_modifier = { modifier = IMP_military_industrial_complex_dynamic_modifier }
                }
            }
            mdcw_cw_update_world_market = yes
        }
        mdcw_cw_touch_gui = yes
    ''') + '\n'
    out += block(P + 'change_tension', protected('''
        set_temp_variable = { mdcw_cw_tension_delta = COLDWAR_gc_cw_delta }
        mdcw_cw_add_tension = yes
        COLDWAR_gc_cw_refresh = yes
    ''')) + '\n'
    out += block(P + 'reset_tension', protected('''
        set_variable = { global.mdcw_cw_tension = global.mdcw_cw_tension_baseline }
        clamp_variable = { var = global.mdcw_cw_tension min = 0 max = 100 }
        COLDWAR_gc_cw_refresh = yes
    ''')) + '\n'
    for track, minimum in (('market', 5), ('arms', 0)):
        out += block(P + 'change_' + track, protected(f'''
            if = {{ limit = {{ NOT = {{ has_variable = global.{P}{track}_base }} }}
                mdcw_cw_update_world_situation = yes
            }}
            set_temp_variable = {{ COLDWAR_gc_cw_target = global.mdcw_cw_{track} }}
            add_to_temp_variable = {{ COLDWAR_gc_cw_target = COLDWAR_gc_cw_delta }}
            clamp_temp_variable = {{ var = COLDWAR_gc_cw_target min = {minimum} max = 100 }}
            set_variable = {{ global.{P}{track}_adjustment = COLDWAR_gc_cw_target }}
            subtract_from_variable = {{ global.{P}{track}_adjustment = global.{P}{track}_base }}
            COLDWAR_gc_cw_refresh = yes
        ''')) + '\n'
        out += block(P + 'reset_' + track, protected(f'''
            set_variable = {{ global.{P}{track}_adjustment = 0 }}
            COLDWAR_gc_cw_refresh = yes
        ''')) + '\n'
    out += block(P + 'change_oil', protected('''
        if = { limit = { NOT = { has_variable = global.mdcw_cw_oil_level } }
            set_variable = { global.mdcw_cw_oil_level = 1 }
        }
        add_to_variable = { global.mdcw_cw_oil_level = COLDWAR_gc_cw_delta }
        clamp_variable = { var = global.mdcw_cw_oil_level min = 0.5 max = 12 }
        COLDWAR_gc_cw_refresh = yes
    ''')) + '\n'
    out += block(P + 'reset_oil', protected('''
        set_variable = { global.mdcw_cw_oil_level = 1 }
        COLDWAR_gc_cw_refresh = yes
    '''))
    return out


def make_decisions():
    entries = []
    loc = {}
    for action, visible, effect, label in (
            ('expand', 'NOT = { has_country_flag = ' + FLAG + ' }', 'set_country_flag = ' + FLAG, '§GShow Cold War Equilibrium Tools§!'),
            ('collapse', 'has_country_flag = ' + FLAG, 'clr_country_flag = ' + FLAG, '§RHide Cold War Equilibrium Tools§!')):
        name = P + action
        entries.append(block(name, f'icon = GFX_decision_imp_list cost = 0 visible = {{ {GC} {visible} }} available = {{ hidden_trigger = {{ {GC} }} }} complete_effect = {{ {protected(effect)} }} ai_will_do = {{ factor = 0 }}'))
        loc[name] = label
        loc[name + '_desc'] = ('§YInternational Situation§!\nCold War Tension: §Y[?global.mdcw_cw_tension|0] / 100§!\nMarket Confidence: §Y[?global.mdcw_cw_market|0] / 100§! (GC assessment: [?global.COLDWAR_gc_cw_market_adjustment|+0])\nArms Demand: §Y[?global.mdcw_cw_arms|0] / 100§! (GC assessment: [?global.COLDWAR_gc_cw_arms_adjustment|+0])\nOil producer price level: §Yx[?global.mdcw_cw_oil_level|2]§!\n\nMarket and arms assessments remain in force until revised or cleared. Diplomatic tension and producer prices continue their normal monthly movement.')
    for track, title, minimum, maximum, steps in (
            ('tension', 'Cold War Tension', 0, 100, ('5', '20')),
            ('market', 'Market Confidence', 5, 100, ('5', '20')),
            ('arms', 'Arms Demand', 0, 100, ('5', '20')),
            ('oil', 'Oil Producer Price Level', 0.5, 12, ('0.25', '1'))):
        variable = 'global.mdcw_cw_' + ('oil_level' if track == 'oil' else track)
        for sign, direction in ((1, 'raise'), (-1, 'lower')):
            for step in steps:
                delta = step if sign > 0 else '-' + step
                name = P + track + '_' + direction + '_' + step.replace('.', '_')
                comparison = '<' if sign > 0 else '>'
                bound = maximum if sign > 0 else minimum
                entries.append(block(name, f'''
                    icon = GFX_decision_imp_list cost = 0
                    visible = {{ {GC} has_country_flag = {FLAG} }}
                    available = {{ hidden_trigger = {{ {GC} }} custom_trigger_tooltip = {{ tooltip = {P}{track}_{direction}_allowed_tt check_variable = {{ {variable} {comparison} {bound} }} }} }}
                    complete_effect = {{
                        custom_effect_tooltip = {name}_tt
                        hidden_effect = {{
                            log = "[GetDateText]: [Root.GetName]: GC equilibrium adjustment {track} {delta}"
                            set_temp_variable = {{ COLDWAR_gc_cw_delta = {delta} }}
                            {P}change_{track} = yes
                        }}
                    }}
                    ai_will_do = {{ factor = 0 }}
                '''))
                signed = '+' + step if sign > 0 else '-' + step
                loc[name] = title + ': §Y' + signed + ('x' if track == 'oil' else ' points') + '§!'
                loc[name + '_desc'] = 'Revise the international situation following a ruling by the Game Controller.'
                loc[P + track + '_' + direction + '_allowed_tt'] = title + (' is below ' if sign > 0 else ' is above ') + ('x' if track == 'oil' else '') + str(bound) + '.'
                if track == 'oil':
                    loc[name + '_tt'] = 'Oil producer price level: §Y' + signed + '§! (limits: x0.50 to x12.00).\nPrices, oil-shock burdens and the international situation are updated.'
                else:
                    loc[name + '_tt'] = title + ': §Y' + signed + '§! points (limits: ' + str(minimum) + '-' + str(maximum) + ').\n' + ('Normal monthly diplomatic drift continues.' if track == 'tension' else 'This GC assessment remains in effect until revised or cleared; wars, sanctions and oil prices continue to influence the total.')
        name = P + track + '_reset'
        if track in {'market', 'arms'}:
            available = f'OR = {{ check_variable = {{ global.{P}{track}_adjustment > 0 }} check_variable = {{ global.{P}{track}_adjustment < 0 }} }}'
            label, effect = 'Clear GC ' + title + ' Assessment', 'Remove the GC assessment from ' + title + '. The value follows the prevailing international situation.'
        elif track == 'oil':
            available = 'NOT = { check_variable = { global.mdcw_cw_oil_level = 1 } }'
            label, effect = 'Return the Producer Price Level to x1', 'Oil producer price level: §Yx1.00§!. Existing national asking prices and embargoes remain in force.'
        else:
            available = 'has_variable = global.mdcw_cw_tension_baseline NOT = { check_variable = { global.mdcw_cw_tension = global.mdcw_cw_tension_baseline } }'
            label, effect = 'Return Tension to the Diplomatic Baseline', 'Cold War Tension: §Y[?global.mdcw_cw_tension_baseline|1]§! points. Sanctions continue to determine the diplomatic baseline.'
        entries.append(block(name, f'icon = GFX_decision_imp_list cost = 0 visible = {{ {GC} has_country_flag = {FLAG} }} available = {{ hidden_trigger = {{ {GC} }} custom_trigger_tooltip = {{ tooltip = {name}_allowed_tt {available} }} }} complete_effect = {{ custom_effect_tooltip = {name}_tt hidden_effect = {{ log = "[GetDateText]: [Root.GetName]: GC equilibrium reset {track}" {P}reset_{track} = yes }} }} ai_will_do = {{ factor = 0 }}'))
        loc[name], loc[name + '_desc'], loc[name + '_tt'] = label, 'Revise the international situation following a ruling by the Game Controller.', effect
        loc[name + '_allowed_tt'] = ('A GC ' + title + ' assessment is in force.' if track in {'market', 'arms'} else
                                     'The producer price level differs from x1.00.' if track == 'oil' else
                                     'Cold War Tension differs from the diplomatic baseline.')
    loc[P + 'assessment_empty'] = ''
    loc[P + 'market_assessment_line'] = '\n + International financial climate: §Y[?global.COLDWAR_gc_cw_market_adjustment|+0]§!'
    loc[P + 'arms_assessment_line'] = '\nInternational procurement climate: §Y[?global.COLDWAR_gc_cw_arms_adjustment|+0]§! points.'
    return HEADER + 'imp_gc_tools_decisions = {\n' + '\n'.join('\t' + line for entry in entries for line in entry.splitlines()) + '\n}\n', loc


def loc_line(key, value):
    return ' ' + key + ': ' + json.dumps(value, ensure_ascii=False).replace('\\u00a7', '§')


def validate_tooltip_values(config, texts):
    prefixes = {'market': 'mdcw_cw_market_fx_', 'arms': 'mdcw_cw_arms_fx_', 'tension': 'mdcw_cw_climate_fx_'}
    for track, prefix in prefixes.items():
        for index, tier in enumerate(reversed(list(config[track])), 1):
            text = texts[prefix + str(index)]
            for stat, amount in config[track][tier].items():
                number = Decimal(amount) * (1 if stat.endswith('_interest') else 100)
                visible = ('+' if number > 0 else '-') + format(abs(number).normalize(), 'f')
                if not stat.endswith('_interest'):
                    visible += '%'
                assert '§R' + visible + '§!' in text, ('Stale tier tooltip', track, tier, stat)
    oil = texts['mdcw_cw_oil_crisis_breakdown_tt']
    for tier, stats in config['oil'].items():
        line = next(line for line in oil.split('\n') if line.startswith('x' + tier + ':'))
        for amount in stats.values():
            number = Decimal(amount) * 100
            visible = ('+' if number > 0 else '-') + format(abs(number).normalize(), 'f') + '%'
            assert '§R' + visible + '§!' in line, ('Stale oil tooltip', tier, amount)


def render():
    config = json.loads((HERE / 'balance.json').read_text(encoding='utf-8'))
    source = (ROOT / WORLD).read_text(encoding='utf-8-sig')
    for name in ('mdcw_cw_update_world_market', 'mdcw_cw_update_oil_crisis_tier'):
        source = patch_effect(source, name, config)
    for track in ('market', 'arms'):
        anchor = 'round_variable = global.mdcw_cw_' + track
        call = P + 'apply_' + track + ' = yes'
        if call not in source:
            assert source.count(anchor) == 1
            source = source.replace(anchor, anchor + '\n\t' + HEADER.rstrip() + '\n\t' + call, 1)
    decisions, loc = make_decisions()
    outputs = {WORLD: source, 'common/scripted_effects/COLDWAR_gc_equilibrium_effects.txt': make_helpers(),
               'common/decisions/COLDWAR_gc_equilibrium_decisions.txt': decisions,
               'localisation/english/COLDWAR_gc_equilibrium_l_english.yml': 'l_english:\n ' + HEADER.rstrip() + '\n' + '\n'.join(loc_line(k, v) for k, v in loc.items()) + '\n'}
    outputs['common/on_actions/COLDWAR_gc_equilibrium_on_actions.txt'] = HEADER + block('on_actions', '''
        on_startup = { effect = {
            if = { limit = { has_global_flag = mdcw_cw_initialized country_exists = USA }
                USA = { COLDWAR_gc_cw_refresh = yes }
            }
        } }
    ''')
    texts = []
    for track in ('market', 'arms'):
        texts.append(block('defined_text', f'name = {P}{track}_assessment_L text = {{ trigger = {{ OR = {{ check_variable = {{ global.{P}{track}_adjustment > 0 }} check_variable = {{ global.{P}{track}_adjustment < 0 }} }} }} localization_key = {P}{track}_assessment_line }} text = {{ localization_key = {P}assessment_empty }}'))
    outputs['common/scripted_localisation/COLDWAR_gc_equilibrium.txt'] = HEADER + '\n'.join(texts)
    existing = (ROOT / LOC).read_text(encoding='utf-8-sig')
    changes = json.loads((HERE / 'tooltips.json').read_text(encoding='utf-8'))
    validate_tooltip_values(config, changes)
    for key, value in changes.items():
        pattern = re.compile(r'^\s*' + re.escape(key) + r':[^\n]*$', re.M)
        matches = list(pattern.finditer(existing))
        assert len(matches) == 1, key
        match = matches[0]
        # Only the authored localisation entry is replaced; neighbouring descriptions remain intact.
        prefix = existing[:match.start()]
        marker = '  ' + HEADER.rstrip() + '\n'
        replacement = loc_line(key, value).lstrip()
        if not prefix.endswith(marker):
            replacement = marker + '  ' + replacement
        else:
            replacement = '  ' + replacement
        existing = prefix + replacement + existing[match.end():]
    outputs[LOC] = existing
    return outputs


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--check', action='store_true')
    args = cli.parse_args()
    for relative, text in render().items():
        path = ROOT / relative
        raw = text.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8')
        if args.check:
            assert path.read_bytes() == raw, 'Output differs: ' + relative
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists() or path.read_bytes() != raw:
                path.write_bytes(raw)
    print('GC controls and every crisis stage synchronized with their English tooltips.')
