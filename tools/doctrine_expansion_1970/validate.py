# IMPERIA COLD WAR — Approved doctrine values and native integration validation.
"""Check the installed content against approved end states and selection rules."""
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/multiplayer_quality'))
from audit import parse
from build import GRAND_PATH, SUB_PATH, LOC_PATH, GFX_PATH, TRIGGERS
from balance_revision import LEGACY, LEGACY_TEXT, REVISION
from coverage_revision import FOOT, ARTILLERY
from coverage_revision import TEXT as COVERAGE_TEXT
from validate_coverage import normalise_coverage, canonical

# Acceptance totals transcribed independently from the user-approved concept.
# Dotted paths retain unit, category and terrain scope instead of mixing them.
EXPECTED = {
 'mdcw_deliberate_firepower': {
  'army_artillery_attack_factor': '.2', 'max_planning_factor': '.15', 'army_speed_factor': '-.05',
  'supply_consumption_factor': '.1', 'planning_speed': '.1', 'coordination_bonus': '.1',
  'breakthrough_factor': '.05', 'army_infantry_defence_factor': '.05', 'army_org_regain': '.05'},
 'mdcw_mobile_raiding_warfare': {
  'army_speed_factor': '.1', 'recon_factor': '.1', 'max_planning_factor': '-.1', 'army_defence_factor': '-.05',
  'org_loss_when_moving': '-.2', 'no_supply_grace': '48', 'coordination_bonus': '.1', 'army_org_regain': '.1',
  **{f'{unit}.{stat}': '.1' for unit in ('Mot_Inf_Bat', 'Hvy_Mot_Inf_Bat', 'Mech_Inf_Bat', 'Arm_Inf_Bat') for stat in ('soft_attack', 'breakthrough')}},
 'mdcw_cohesive_unit_rotation': {
  'army_org_factor': '.1', 'experience_loss_factor': '-.25', 'army_personnel_cost_multiplier_modifier': '.1',
  'training_time_army_factor': '.1', 'army_strength_factor': '.05', 'army_org_regain': '.15', 'coordination_bonus': '.05', 'land_reinforce_rate': '.02'},
 'mdcw_integrated_support_commands': {
  'supply_consumption_factor': '-.15', 'coordination_bonus': '.05', 'army_personnel_cost_multiplier_modifier': '.08',
  'army_speed_factor': '-.05', 'army_strength_factor': '.1', 'combat_service_support_company.reliability_factor': '.03', 'army_org_regain': '.1'},
 'mdcw_forest_envelopment': {
  'L_Inf_Bat.forest.attack': '.2', 'L_Inf_Bat.forest.movement': '.2', 'L_Inf_Bat.forest.defence': '.1',
  'max_planning_factor': '-.1', 'recon_factor': '.1', 'org_loss_when_moving': '-.15', 'land_night_attack': '.1', 'initiative_factor': '.1'},
 'mdcw_heliborne_reaction_forces': {
  'L_Air_assault_Bat.soft_attack': '.1', 'army_fuel_consumption_factor': '.1', 'equipment_cost_multiplier_modifier': '.05',
  'L_Air_assault_Bat.max_organisation': '5', 'L_Air_assault_Bat.breakthrough': '.15',
  **{f'L_Air_assault_Bat.{terrain}.movement': '.1' for terrain in ('forest', 'hills', 'jungle')},
  'recon_factor': '.1', 'coordination_bonus': '.05', 'initiative_factor': '.1', 'org_loss_when_moving': '-.1'},
 'mdcw_assault_breaching': {
  **{f'{unit}.{key}': value for unit in ('category_foot_inf', 'Mot_Inf_Bat', 'Hvy_Mot_Inf_Bat', 'Mech_Inf_Bat', 'Arm_Inf_Bat')
     for key, value in {'fort.attack': '.2', 'river.attack': '.15', 'breakthrough': '.1'}.items()},
  'supply_consumption_factor': '.1', 'training_time_army_factor': '.1', 'planning_speed': '.1',
  'coordination_bonus': '.1', 'planning_decay_rate_factor': '-.1'},
 'mdcw_key_zone_defence': {
  'dig_in_speed_factor': '.2', 'army_attack_speed_factor': '-.1', 'supply_consumption_factor': '.05', 'max_dig_in': '3',
  'category_foot_inf.hills.defence': '.15', 'category_foot_inf.mountain.defence': '.15', 'recon_factor_while_entrenched': '.15',
  'category_foot_inf.fort.defence': '.4', 'category_foot_inf.river.defence': '.2', 'org_loss_at_low_org_factor': '-.1'},
 'mdcw_coastal_denial': {
  'amphibious_invasion_defence': '.25', 'breakthrough_factor': '-.05', 'equipment_cost_multiplier_modifier': '.05',
  'dig_in_speed_factor': '.1', 'coastal_bunker_effectiveness_factor': '.15', 'land_reinforce_rate': '.02', 'army_infantry_defence_factor': '.05'},
 'mdcw_opposing_force_exercises': {
  'experience_gain_army_unit_factor': '.25', 'training_time_army_factor': '.15', 'army_personnel_cost_multiplier_modifier': '.05',
  'coordination_bonus': '.1', 'experience_loss_factor': '-.15', 'land_night_attack': '.1', 'army_org_factor': '.05'},
 'mdcw_mission_rehearsal': {
  'planning_speed': '.15', 'training_time_army_factor': '.15', 'army_personnel_cost_multiplier_modifier': '.075',
  'category_special_forces.max_organisation': '5', 'max_planning_factor': '.1', 'land_night_attack': '.1', 'category_special_forces.breakthrough': '.1'},
 'mdcw_institutional_combat_learning': {
  'experience_gain_army_factor': '.25', 'training_time_army_factor': '.1', 'army_personnel_cost_multiplier_modifier': '.05',
  'experience_gain_army_unit_factor': '.1', 'experience_loss_factor': '-.1', 'max_planning_factor': '.05', 'army_org_regain': '.1',
  'operational_theory_track_mastery_gain_factor': '.1'},
 'mdcw_guided_anti_armour_integration': {
  **{f'{unit}.{stat}': value for unit in ('AT_company', 'Mot_AT_company')
     for stat, value in {'hard_attack': '.3', 'ap_attack': '.25', 'soft_attack': '-.1'}.items()},
  'equipment_cost_multiplier_modifier': '.05', 'category_foot_inf.hard_attack': '.1', 'category_foot_inf.ap_attack': '.05', 'recon_factor': '.1'},
 'mdcw_counterfire_coordination': {
  'army_artillery_attack_factor': '.2', 'supply_consumption_factor': '.1', 'equipment_cost_multiplier_modifier': '.05',
  'recon_factor': '.2', 'category_artillery.defense': '.15', 'coordination_bonus': '.1', 'planning_speed': '.1'},
}

# IMPERIA COLD WAR — Current acceptance totals for the user's stronger trade-offs.
# Preserve the original contract above; this explicit revision changes only penalties.
for _ident, _changes in {
 'mdcw_deliberate_firepower': {'planning_speed': '-.1', 'supply_consumption_factor': '.12'},
 'mdcw_mobile_raiding_warfare': {'out_of_supply_factor': '.15'},
 'mdcw_heliborne_reaction_forces': {'army_fuel_consumption_factor': '.15', 'L_Air_assault_Bat.fort.attack': '-.15'},
 'mdcw_key_zone_defence': {'org_loss_when_moving': '.15', 'supply_consumption_factor': '.08'},
 'mdcw_guided_anti_armour_integration': {'equipment_cost_multiplier_modifier': '.08',
   'AT_company.soft_attack': '-.15', 'AT_company.breakthrough': '-.15',
   'Mot_AT_company.soft_attack': '-.15', 'Mot_AT_company.breakthrough': '-.15'},
 'mdcw_counterfire_coordination': {'army_intel_to_others': '10', 'supply_consumption_factor': '.15'},
}.items():
    EXPECTED[_ident].update(_changes)

LEGACY_END = {
 'battalion_combat_teams': {'max_planning_factor': '-.15', 'supply_consumption_factor': '.08'},
 'decentralized_command': {'max_planning_factor': '-.05', 'planning_decay_rate_factor': '.05'},
 'common_technology_army': {'army_intel_to_others': '5'},
 'mdcw_maskirovka': {'initiative_factor': '-.1', 'planning_speed': '-.1'},
 'mdcw_cadre_reserve_system': {'army_org_factor': '-.05', 'experience_loss_factor': '.05'},
 'mdcw_radio_electronic_combat': {'equipment_cost_multiplier_modifier': '.08', 'army_intel_to_others': '10'},
}

# IMPERIA COLD WAR — Revised unit scope and early planning acceptance contract.
for _ident, _values in EXPECTED.items():
    if _ident == 'mdcw_forest_envelopment':
        for _key in list(_values):
            if _key.startswith('L_Inf_Bat.'):
                _values[_key.replace('L_Inf_Bat.', 'category_foot_inf.', 1)] = _values.pop(_key)
    for _key in list(_values):
        if _key.startswith('category_foot_inf.'):
            for _scope in FOOT[1:]:
                _values[_key.replace('category_foot_inf.', _scope + '.', 1)] = _values[_key]
    if 'army_artillery_attack_factor' in _values:
        _values[ARTILLERY] = _values.pop('army_artillery_attack_factor')
EXPECTED['mdcw_mission_rehearsal']['max_planning_factor'] = '.15'

META = {'folder', 'track', 'name', 'description', 'icon', 'xp_cost', 'xp_type', 'available', 'visible', 'ai_will_do', 'tracks', 'milestones', 'rewards'}


def first(rows, key):
    return next(value for name, _, value in rows if name == key)


def flatten(rows, prefix=()):
    result = defaultdict(Decimal)
    for key, _, value in rows:
        path = (*prefix, key)
        if isinstance(value, list):
            for nested, amount in flatten(value, path).items():
                result[nested] += amount
        else:
            result['.'.join(path)] += Decimal(value)
    return result


def totals(body):
    result = flatten([(key, op, value) for key, op, value in body if key not in META])
    progression = next((value for key, _, value in body if key in {'rewards', 'milestones'}), [])
    for _, _, effects in progression:
        for key, value in flatten(effects).items():
            result[key] += value
    return dict(result)


def evaluate(rows, owned):
    """Evaluate the actual native availability AST for the identity guard cases."""
    def entry(key, value):
        if key == 'NOT':
            return not evaluate(value, owned)
        if key == 'OR':
            return any(entry(k, v) for k, _, v in value)
        if key == 'AND':
            return evaluate(value, owned)
        if key == 'has_doctrine':
            return value in owned
        raise AssertionError(f'Unexpected availability trigger {key}')
    return all(entry(key, value) for key, _, value in rows)


def main():
    checks, errors = [], []
    def check(name, condition, detail=None):
        checks.append({'check': name, 'passed': bool(condition), 'detail': detail})
        if not condition:
            errors.append(name)
    runtime_paths = [GRAND_PATH, SUB_PATH, LOC_PATH, GFX_PATH, *LEGACY, *LEGACY_TEXT, TRIGGERS]
    ast = {}
    for relative in runtime_paths:
        path = ROOT / relative
        raw = path.read_bytes()
        source = raw.decode('utf-8-sig')
        check('encoding:' + relative, raw.startswith(b'\xef\xbb\xbf') == relative.endswith('.yml'))
        check('project_marker:' + relative, source.splitlines()[1 if relative.endswith('.yml') else 0].startswith('# IMPERIA COLD WAR —'))
        if path.suffix != '.yml':
            ast[relative] = parse(source)
    grands, subs = dict((k, v) for k, _, v in ast[GRAND_PATH]), dict((k, v) for k, _, v in ast[SUB_PATH])
    installed = {**grands, **subs}
    check('approved_ids', set(installed) == set(EXPECTED))
    actual_totals = {}
    for relative, changed in LEGACY.items():
        baseline = subprocess.run(['git', 'show', 'HEAD:' + relative], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        original = {key: body for key, _, body in parse(baseline)}
        current = {key: body for key, _, body in ast[relative]}
        check('legacy_identity_preservation:' + relative, set(original) == set(current))
        for ident, body in current.items():
            if ident not in changed:
                check('legacy_preserved_except_authorised_coverage:' + ident,
                      canonical(body) == canonical(normalise_coverage(original[ident], ident)))
                continue
            ignored = set(changed[ident])
            check('legacy_bonuses_rewards_and_guards_unchanged:' + ident,
                  canonical([(k, o, v) for k, o, v in body if k not in ignored]) ==
                  canonical([(k, o, v) for k, o, v in normalise_coverage(original[ident], ident) if k not in ignored]))
            actual = totals(body)
            actual_totals[ident] = {name: str(value) for name, value in actual.items()}
            check('persistent_legacy_penalties:' + ident,
                  all(actual[name] == Decimal(value) for name, value in LEGACY_END[ident].items()),
                  {name: str(actual[name]) for name in LEGACY_END[ident]})
    for key, body in installed.items():
        actual = totals(body)
        expected = {name: Decimal(value) for name, value in EXPECTED[key].items()}
        check('approved_end_values:' + key, actual == expected,
              {name: str(value) for name, value in actual.items()})
        actual_totals[key] = {name: str(value) for name, value in actual.items()}
        check('xp_cost:' + key, first(body, 'xp_cost') == ('100' if key in grands else '75') and first(body, 'xp_type') == 'army')
        check('no_side_effect_grants:' + key, 'effect =' not in str(body) and not any(name.startswith('add_') for name in actual))
        check('no_workforce_penalty:' + key, not any('workforce' in name or 'conscription' in name for name in actual))
        if key in subs:
            rewards = first(body, 'rewards')
            check('five_rewards:' + key, len(rewards) == 5)
            check('no_duplicate_self:' + key, not evaluate(first(body, 'available'), {key}))
            check('open_access:' + key, evaluate(first(body, 'available'), set()))
            if key != 'mdcw_key_zone_defence':
                check('no_new_grand_or_country_lock:' + key, len(first(body, 'available')) == 1)
        else:
            tracks = [value for _, _, value in first(body, 'tracks')]
            check('six_matching_milestones:' + key, len(tracks) == len(first(body, 'milestones')) == 6)
    check('category_distribution', Counter(first(body, 'track') for body in subs.values()) ==
          Counter({'structure_doctrine': 2, 'operational_theory': 2, 'dedicated_doctrine': 3, 'training': 2, 'leadership': 1, 'technology': 2}))
    key_available = first(subs['mdcw_key_zone_defence'], 'available')
    for territorial in ('mdcw_territorial_defence', 'dedicated_mdcw_territorial_defence'):
        check('key_zone_excludes:' + territorial, not evaluate(key_available, {territorial}))
    shared = ast[TRIGGERS]
    territorial_guard = first(shared, 'does_not_have_mdcw_territorial_defence_doctrine')
    check('territorial_excludes_key_zone', not evaluate(territorial_guard, {'mdcw_total_defence', 'mdcw_key_zone_defence'}))
    check('territorial_retains_parent', evaluate(territorial_guard, {'mdcw_total_defence'}) and not evaluate(territorial_guard, set()))
    baseline = subprocess.run(['git', 'show', 'HEAD:' + TRIGGERS], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    stripped = [(key, op, [(k, o, v) for k, o, v in value if not (k == 'NOT' and v == [('has_doctrine', '=', 'mdcw_key_zone_defence')])])
                if key == 'does_not_have_mdcw_territorial_defence_doctrine' else (key, op, value) for key, op, value in shared]
    check('unrelated_native_triggers_preserved', stripped == parse(baseline))
    loc_source = (ROOT / LOC_PATH).read_text(encoding='utf-8-sig')
    loc_entries = re.findall(r'^ ([A-Za-z0-9_]+):0 "((?:\\.|[^"\\])*)"$', loc_source, re.M)
    loc = dict(loc_entries)
    check('no_duplicate_localisation', len(loc) == len(loc_entries))
    check('english_marker_and_punctuation', loc_source.startswith('l_english:\n# IMPERIA COLD WAR —') and all('\u2013' not in value and '\u2014' not in value for value in loc.values()))
    used_loc = []
    for key, body in installed.items():
        used_loc += [first(body, 'name'), first(body, 'description')]
        for reward, _, _ in next((value for name, _, value in body if name == 'rewards'), []):
            used_loc += [key + '_' + reward, key + '_' + reward + '_desc']
    check('all_names_and_descriptions_localised', set(used_loc) == set(loc), {'expected': len(used_loc), 'actual': len(loc)})
    # Measure the actual inherited BMFont advances against the complete native
    # selection-row and description-field dimensions, rather than character counts.
    def font_metrics(name):
        candidates = [ROOT / 'gfx/fonts' / (name + '.fnt'),
                      Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/gfx/fonts') / (name + '.fnt')]
        path = next(path for path in candidates if path.is_file())
        text = path.read_text(encoding='utf-8-sig')
        advances = {int(code): int(width) for code, width in re.findall(r'^char id=(\d+).*?xadvance=(-?\d+)', text, re.M)}
        line_height = int(re.search(r'^common lineHeight=(\d+)', text, re.M).group(1))
        return advances, line_height
    def wrapped_lines(text, advances, width):
        lines = ['']
        for word in text.split():
            candidate = (lines[-1] + ' ' + word).strip()
            if sum(advances.get(ord(char), 9) for char in candidate) > width and lines[-1]:
                lines.append(word)
            else:
                lines[-1] = candidate
        return lines
    layout = {}
    for key, body in installed.items():
        record = {}
        for field, font, width, height in [('name', 'hoi_20bs', 140, 50), ('description', 'hoi_18mbs', 460, 80)]:
            advances, line_height = font_metrics(font)
            lines = wrapped_lines(loc[first(body, field)], advances, width)
            record[field] = {'font': font, 'lines': lines, 'height': len(lines) * line_height, 'limit': height}
            check('native_text_field_fit:' + key + ':' + field,
                  len(lines) * line_height <= height and all(sum(advances.get(ord(c), 9) for c in line) <= width for line in lines), record[field])
        layout[key] = record
    (HERE / 'text_layout.json').write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'native_fields': layout}, indent=2) + '\n', encoding='utf-8')
    all_legacy_text = {path: dict(entries) for path, entries in LEGACY_TEXT.items()}
    for path, entries in COVERAGE_TEXT.items():
        all_legacy_text.setdefault(path, {}).update(entries)
    for relative, replacements in all_legacy_text.items():
        source = (ROOT / relative).read_text(encoding='utf-8-sig')
        for key, text in replacements.items():
            advances, line_height = font_metrics('hoi_18mbs')
            lines = wrapped_lines(text, advances, 460)
            check('legacy_description_fit:' + key, len(lines) * line_height <= 80, lines)
            check('legacy_description_installed:' + key, text in source and '\u2013' not in text and '\u2014' not in text)
    local_occurrences = Counter()
    wanted_loc = set(loc)
    for path in (ROOT / 'localisation/english').rglob('*.yml'):
        for candidate in re.findall(r'^\s*([A-Za-z0-9_]+):\d*\s', path.read_text(encoding='utf-8-sig', errors='replace'), re.M):
            if candidate in wanted_loc:
                local_occurrences[candidate] += 1
    check('no_collisions_with_existing_english_keys', all(local_occurrences[key] == 1 for key in loc))
    all_tags = set()
    for path in (ROOT / 'common/country_tags').glob('*.txt'):
        all_tags.update(re.findall(r'^\s*([A-Z0-9]{3})\s*=', path.read_text(encoding='utf-8-sig'), re.M))
    gfx = first(ast[GFX_PATH], 'spriteTypes')
    sprites = {first(body, 'name').strip('"'): first(body, 'texturefile').strip('"') for _, _, body in gfx}
    sprite_occurrences = Counter()
    for path in (ROOT / 'interface').rglob('*.gfx'):
        for candidate in re.findall(r'\bname\s*=\s*"([^"\r\n]+)"', path.read_text(encoding='utf-8-sig', errors='replace')):
            if candidate in sprites:
                sprite_occurrences[candidate] += 1
    check('no_collisions_with_existing_sprites', all(sprite_occurrences[key] == 1 for key in sprites))
    manifest = json.loads((HERE / 'icon_manifest.json').read_text(encoding='utf-8'))
    check('fourteen_unique_icons', len(sprites) == len(manifest['assets']) == 14)
    for key, body in installed.items():
        sprite = first(body, 'icon')
        check('sprite_reference:' + key, sprite in sprites)
        texture = ROOT / sprites[sprite]
        raw = texture.read_bytes()
        check('native_dds:' + key, raw[:4] == b'DDS ' and struct.unpack_from('<II', raw, 12) == (64, 64) and
              struct.unpack_from('<4I', raw, 92) == (0xFF0000, 0xFF00, 0xFF, 0xFF000000))
        image = Image.open(texture).convert('RGBA')
        alpha = image.getchannel('A')
        check('transparent_readable_icon:' + key, alpha.getextrema()[0] == 0 and sum(v > 64 for v in alpha.tobytes()) > 200)
        tags = [value for _, _, conditions in first(body, 'ai_will_do') if isinstance(conditions, list)
                for _, _, group in conditions if isinstance(group, list)
                for name, _, value in group if name == 'original_tag']
        check('valid_ai_country_tags:' + key, set(tags) <= all_tags)
    check('no_long_fixed_point_literals', not re.search(r'(?<![\w.])-?\d+\.\d{6,}', '\n'.join((ROOT / p).read_text(encoding='utf-8-sig') for p in runtime_paths[:-1])))
    generator = subprocess.run([sys.executable, str(HERE / 'build.py'), '--check'], cwd=ROOT, capture_output=True, text=True)
    check('generator_matches_runtime', generator.returncode == 0, generator.stdout.strip())
    report = {'project': 'IMPERIA COLD WAR', 'revision': REVISION, 'scope': 'source, revised approved values, unchanged legacy rewards, native references, selection truth tables and asset storage',
              'grand_doctrines': len(grands), 'subdoctrines': len(subs), 'mastery_rewards': 60,
              'checks': checks, 'failed': errors, 'end_values': actual_totals,
              'source_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in runtime_paths},
              'live_engine_or_multiplayer_claim': False}
    (HERE / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'checks': len(checks), 'passed': len(checks) - len(errors), 'failed': errors}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
