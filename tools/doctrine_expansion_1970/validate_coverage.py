# IMPERIA COLD WAR — All-stage doctrine penalties, foot coverage and artillery regression checks.
"""Compare actual installed ASTs with the immutable pre-revision semantic input."""
from collections import defaultdict
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/multiplayer_quality'))
from audit import parse

FOOT_EXTRA = ('L_Ranger_Bat', 'L_Air_assault_Bat', 'L_Ranger_Recce_Comp')
ART = 'modifier_army_sub_unit_category_artillery_attack_factor'
# Independent acceptance values, not imported from the emitting generator.
CHANGES = {
 'combined_arms': {'supply_consumption_factor': '.08', 'training_time_army_factor': '.1'},
 'shock_and_awe': {'army_fuel_consumption_factor': '.15', 'out_of_supply_factor': '.1'},
 'defence_in_depth': {'army_attack_speed_factor': '-.1', 'org_loss_when_moving': '.1'},
 'mission_command': {'training_time_army_factor': '.15', 'army_personnel_cost_multiplier_modifier': '.08'},
 'battlefield_support': {'army_speed_factor': '-.05', 'supply_consumption_factor': '.05'},
 'guerrilla_warfare': {'breakthrough_factor': '-.1', 'max_planning_factor': '-.15'},
 'mdcw_active_defense': {'breakthrough_factor': '-.1', 'army_attack_speed_factor': '-.05'},
 'mdcw_peoples_war': {'army_armor_attack_factor': '-.1', 'max_planning_factor': '-.1'},
 'skill_school_focus': {'training_time_army_factor': '.15', 'supply_consumption_factor': '.05'},
 'officer_training_focus': {'training_time_army_factor': '.1'},
 'mdcw_mission_rehearsal': {'max_planning_factor': '.05'},
}
META = {'folder', 'track', 'name', 'description', 'icon', 'xp_cost', 'xp_type', 'available',
        'visible', 'ai_will_do', 'tracks', 'milestones', 'rewards', 'effect', 'enable_tactic', 'mastery'}
BAD_HIGH = {'supply_consumption_factor', 'army_fuel_consumption_factor', 'equipment_cost_multiplier_modifier',
            'army_personnel_cost_multiplier_modifier', 'training_time_army_factor', 'out_of_supply_factor',
            'experience_loss_factor', 'org_loss_when_moving', 'planning_decay_rate_factor', 'attrition',
            'unit_upkeep_attrition_factor', 'army_intel_to_others', 'promote_cost_factor', 'combat_width'}
BAD_LOW = {'max_planning_factor', 'initiative_factor', 'army_org_factor', 'army_speed_factor',
           'army_attack_speed_factor', 'army_armor_attack_factor', 'army_defence_factor', 'army_non_core_attack_factor',
           'breakthrough_factor', 'land_reinforce_rate', 'army_morale_factor', 'max_fuel_factor',
           'equipment_capture_factor', 'casualty_trickleback', 'max_dig_in_factor', 'unit_medal_effectiveness',
           'army_strength_factor', 'skill_bonus_factor', 'planning_speed', 'soft_attack', 'breakthrough', 'attack', 'stability_factor'}


def normalise_coverage(rows, ident):
    """Independent expected AST transformation. No emitted strings or patch code reused."""
    def walk(entries):
        entries = deepcopy(entries)
        if ident == 'mdcw_forest_envelopment':
            entries = [('category_foot_inf' if k == 'L_Inf_Bat' else k, op, v) for k, op, v in entries]
        if ident in ('mdcw_territorial_defence', 'dedicated_mdcw_territorial_defence'):
            small = next((v for k, _, v in entries if k == 'L_Inf_Bat'), None)
            militia = next((v for k, _, v in entries if k == 'Militia_Bat'), None)
            if small is not None and small == militia:
                entries = [('category_foot_inf' if k == 'L_Inf_Bat' else k, op, v)
                           for k, op, v in entries if k != 'Militia_Bat']
        out = []
        names = {k for k, _, _ in entries}
        for k, op, v in entries:
            v = walk(v) if isinstance(v, list) else v
            out.append((ART if k == 'army_artillery_attack_factor' else k, op, v))
            if k == 'category_foot_inf':
                out.extend((scope, '=', deepcopy(v)) for scope in FOOT_EXTRA if scope not in names)
        return out
    result = walk(rows)
    for key, value in CHANGES.get(ident, {}).items():
        index = next((i for i, (k, _, _) in enumerate(result) if k == key), None)
        if index is None:
            index = next(i for i, (k, _, _) in enumerate(result) if k in {'rewards', 'milestones'})
            result.insert(index, (key, '=', value))
        else:
            result[index] = (key, '=', value)
    if ident == 'battlefield_support':
        result = [(k, op, 'GRAND_DOCTRINE_BATTLEFIELD_SUPPORT_DESC' if k == 'description' else v) for k, op, v in result]
    return result


def canonical(rows):
    result = []
    for k, op, value in rows:
        if isinstance(value, list):
            if k in {'milestones', 'rewards', 'tracks'}:
                value = [(a, b, canonical(c) if isinstance(c, list) else c) for a, b, c in value]
            else:
                value = canonical(value)
        else:
            try:
                value = str(Decimal(value).normalize())
            except Exception:
                pass
        result.append((k, op, value))
    return sorted(result, key=lambda row: json.dumps(row))


def numbers(rows, prefix=''):
    out = defaultdict(Decimal)
    for k, _, v in rows:
        if k in META:
            continue
        if isinstance(v, list):
            for name, value in numbers(v, prefix + k + '.').items():
                out[name] += value
        else:
            try:
                out[prefix + k] += Decimal(v)
            except Exception:
                pass
    return out


def stages(body):
    current = numbers(body)
    yield dict(current)
    for _, _, stage in next((v for k, _, v in body if k in {'rewards', 'milestones'}), []):
        for key, value in numbers(stage).items():
            current[key] += value
        yield dict(current)


def harmful(values):
    return {key: str(value) for key, value in values.items()
            if (key.rsplit('.', 1)[-1] in BAD_HIGH and value > 0) or
               (key.rsplit('.', 1)[-1] in BAD_LOW and value < 0)}


def main():
    checks = []
    def check(name, condition, detail=None):
        checks.append({'check': name, 'passed': bool(condition), 'detail': detail})
    baseline = json.loads((HERE / 'scope_baseline_20261029.json').read_text(encoding='utf-8'))
    installed, counts, paths = {}, defaultdict(int), []
    for relative, record in baseline['files'].items():
        path = ROOT / relative
        paths.append(relative)
        raw = path.read_bytes()
        source = raw.decode('utf-8-sig')
        check('encoding_marker:' + relative, not raw.startswith(b'\xef\xbb\xbf') and source.startswith('# IMPERIA COLD WAR —'))
        previous = {k: v for k, _, v in record['ast']}
        current = {k: v for k, _, v in parse(source)}
        check('identities_preserved:' + relative, current.keys() == previous.keys())
        for ident, body in current.items():
            installed[ident] = body
            expected = normalise_coverage(previous[ident], ident)
            check('only_authorised_semantic_changes:' + ident, canonical(body) == canonical(expected))
            track = next((v for k, _, v in body if k == 'track'), 'grand')
            counts[track] += 1
            for level, values in enumerate(stages(body)):
                check('permanent_penalty:' + ident + ':' + str(level), bool(harmful(values)), harmful(values))
    check('complete_land_inventory', sum(counts.values()) == 71 and counts['grand'] == 14 and counts['structure_doctrine'] == 5,
          dict(counts))
    # Resolve actual native categories rather than assuming that all SF are foot units.
    units = {}
    for path in (ROOT / 'common/units').glob('*.txt'):
        for _, _, group in parse(path.read_text(encoding='utf-8-sig')):
            if not isinstance(group, list):
                continue
            for ident, _, body in group:
                if isinstance(body, list):
                    cats = next((v for k, _, v in body if k == 'categories'), [])
                    units[ident] = {v for _, _, v in cats}
    foot = {name for name, cats in units.items() if 'category_foot_inf' in cats} | set(FOOT_EXTRA)
    forest = installed['mdcw_forest_envelopment']
    forest_values = list(stages(forest))
    for unit in sorted(foot):
        scopes = ['category_foot_inf'] if 'category_foot_inf' in units[unit] else []
        scopes += [unit] if unit in FOOT_EXTRA else []
        for level, values in enumerate(forest_values):
            attack = sum((values.get(scope + '.forest.attack', Decimal(0)) for scope in scopes), Decimal(0))
            movement = sum((values.get(scope + '.forest.movement', Decimal(0)) for scope in scopes), Decimal(0))
            check('forest_exact_once:' + unit + ':' + str(level),
                  attack == Decimal('.1' if level < 2 else '.2') and movement == Decimal('.1' if level < 5 else '.2'))
    for excluded in ('Mot_Air_Inf_Bat', 'Mech_Air_Inf_Bat', 'Arm_Air_Inf_Bat', 'Light_L_Air_assault_Bat'):
        check('no_foot_bonus_for_vehicle_or_rotor_unit:' + excluded, excluded not in foot)
    for ident, body in installed.items():
        for level, values in enumerate(stages(body)):
            for key, value in values.items():
                if key.startswith('category_foot_inf.'):
                    for unit in FOOT_EXTRA:
                        check('specialist_foot_parity:' + ident + ':' + str(level) + ':' + unit + ':' + key,
                              values.get(unit + key[len('category_foot_inf'):]) == value)
    all_arty = sorted(name for name, cats in units.items() if 'category_artillery' in cats)
    for name in ('Arty_Bat', 'SP_Arty_Bat', 'SP_R_arty_Bat', 'Light_SP_Arty_Bat', 'Light_SP_R_arty_Bat',
                 'Arty_Battery', 'SP_arty_battery', 'SP_R_arty_battery', 'air_assault_arty_Bat', 'air_assault_arty_battery'):
        check('all_artillery_types:' + name, name in all_arty)
    for ident, body in installed.items():
        check('no_narrow_generic_artillery_bonus:' + ident, 'army_artillery_attack_factor' not in json.dumps(body))
    registration = (ROOT / 'common/units/unit_modifiers/unit_modifiers.txt').read_text(encoding='utf-8')
    check('native_category_modifier_registered_once', len(re.findall(r'^\s*' + ART + r'\s*$', registration, re.M)) == 1)
    sync_path = 'common/synchronized_dynamic_tokens/mdcw_doctrine_tokens.txt'
    sync = (ROOT / sync_path).read_bytes()
    check('category_modifier_token_synchronised', sync.decode('utf-8').splitlines() ==
          ['# IMPERIA COLD WAR — Land doctrine coverage and immediate trade-offs.', ART])
    check('sync_token_script_encoding', not sync.startswith(b'\xef\xbb\xbf'))
    colour_path = ROOT / 'localisation/english/replace/mdcw_doctrine_stat_colours_l_english.yml'
    colour = colour_path.read_text(encoding='utf-8-sig')
    check('signed_colour_formatter', 'STAT_MODIFIER_VALUE:0 "$VALUE|=+0%$"' in colour and '|=G' not in colour)
    check('inverse_colour_formatters_preserved', not re.search(r'^ STAT_(?:MODIFIER_DIFF_NEG|ARMY_SUPPLY_CONSUMPTION_MOD_VALUE):', colour, re.M))
    check('colour_override_bom_marker', colour_path.read_bytes().startswith(b'\xef\xbb\xbf') and colour.splitlines()[1].startswith('# IMPERIA COLD WAR —'))
    rehearsal = installed['mdcw_mission_rehearsal']
    check('mission_rehearsal_immediate_planning', numbers(rehearsal)['max_planning_factor'] == Decimal('.05'))
    check('mission_rehearsal_final_planning', list(stages(rehearsal))[-1]['max_planning_factor'] == Decimal('.15'))
    paths += ['common/units/unit_modifiers/unit_modifiers.txt', colour_path.relative_to(ROOT).as_posix(), sync_path]
    report = {'project': 'IMPERIA COLD WAR', 'revision': '20261029_complete_land_coverage',
              'inventory': dict(counts), 'foot_units': sorted(foot), 'all_artillery_category_members': all_arty,
              'checks': checks, 'failed': [c['check'] for c in checks if not c['passed']],
              'fully_mastered_penalties': {k: harmful(list(stages(v))[-1]) for k, v in installed.items()},
              'source_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
              'native_ui_or_multiplayer_claim': False}
    (HERE / 'coverage_validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'checks': len(checks), 'passed': sum(c['passed'] for c in checks), 'failed': report['failed']}, indent=2))
    raise SystemExit(bool(report['failed']))


if __name__ == '__main__':
    main()
