# IMPERIA COLD WAR — Complete land doctrine unit coverage and visible trade-offs.
"""User-authorised 29 October revision; preserve existing rewards and access."""
from copy import deepcopy
from pathlib import Path
import re

REVISION = '20261029_complete_land_coverage'
MARKER = '# IMPERIA COLD WAR — Land doctrine coverage and immediate trade-offs.'
FOOT = ('category_foot_inf', 'L_Ranger_Bat', 'L_Air_assault_Bat', 'L_Ranger_Recce_Comp')
ARTILLERY = 'modifier_army_sub_unit_category_artillery_attack_factor'
UNIT_MODIFIERS = 'common/units/unit_modifiers/unit_modifiers.txt'
SYNC_PATH = 'common/synchronized_dynamic_tokens/mdcw_doctrine_tokens.txt'
COLOUR_PATH = 'localisation/english/replace/mdcw_doctrine_stat_colours_l_english.yml'
GRAND_FILES = ('common/doctrines/grand_doctrines/land_doctrine.txt',
               'common/doctrines/grand_doctrines/mdcw_cold_war_land_doctrines.txt')
SUB_FILES = tuple('common/doctrines/subdoctrines/land/' + name for name in (
    'land_doctrines_combat.txt', 'land_doctrines_dedicated.txt', 'land_doctrines_supporting.txt',
    'mdcw_cold_war_free_subdoctrines.txt', 'mdcw_cold_war_operational_subdoctrines.txt',
    'mdcw_cold_war_dedicated_subdoctrines.txt'))

# Activation values, with the previous value as a concurrent-edit guard.
PENALTIES = {
 'combined_arms': {'supply_consumption_factor': (None, .08), 'training_time_army_factor': (None, .10)},
 'shock_and_awe': {'army_fuel_consumption_factor': (None, .15), 'out_of_supply_factor': (None, .10)},
 'defence_in_depth': {'army_attack_speed_factor': (None, -.10), 'org_loss_when_moving': (None, .10)},
 'mission_command': {'training_time_army_factor': (None, .15), 'army_personnel_cost_multiplier_modifier': (None, .08)},
 'battlefield_support': {'army_speed_factor': (None, -.05), 'supply_consumption_factor': (None, .05)},
 'guerrilla_warfare': {'breakthrough_factor': (None, -.10), 'max_planning_factor': (None, -.15)},
 'mdcw_active_defense': {'breakthrough_factor': (None, -.10), 'army_attack_speed_factor': (None, -.05)},
 'mdcw_peoples_war': {'army_armor_attack_factor': (None, -.10), 'max_planning_factor': (None, -.10)},
 'skill_school_focus': {'training_time_army_factor': (.10, .15), 'supply_consumption_factor': (None, .05)},
 'officer_training_focus': {'training_time_army_factor': (None, .10)},
}

TEXT = {
 'localisation/english/MD_doctrines_ncns_l_english.yml': {
  'GRAND_DOCTRINE_COMBINED_ARMS_DESC': 'Combined-arms armies of the Second World War and Cold War integrated infantry, armour, artillery and support. Coordinated formations gain flexibility, but joint training takes longer and their supporting services consume more supplies.',
  'GRAND_DOCTRINE_SHOCK_AND_AWE_DESC': 'Rapid-dominance ideas formalised in 1996 drew on the concentrated force seen in 1991. High tempo disrupts the opponent, but consumes more fuel and makes an advance vulnerable once its supply reserve runs out.',
  'GRAND_DOCTRINE_DEFENCE_IN_DEPTH_DESC': 'Soviet defensive belts at Kursk in 1943 combined obstacles, successive positions and reserves. Layered defence absorbs an attack, but moving prepared defenders disrupts cohesion and slows offensive movement.',
  'GRAND_DOCTRINE_MISSION_COMMAND_DESC': 'German Auftragstaktik and later NATO practice delegated action within a clear intent. Capable subordinate leaders improve command, but their education takes longer and sustaining a professional command cadre increases personnel costs.',
  'GRAND_DOCTRINE_BATTLEFIELD_SUPPORT_DESC': 'Cold War support commands coordinated distribution, transport, repair and evacuation. Strong support sustains the fighting force, but a larger logistical train needs more supplies and slows movement.',
  'GRAND_DOCTRINE_GUERRILLA_WARFARE_DESC': 'Vietnamese and other Cold War guerrillas used dispersed units, local knowledge and captured stores. Irregular forces sustain resistance, but have less capacity for prepared offensives and frontal breakthroughs.',
  'SUBDOCTRINE_TRAINING_SKILLS_DESC': 'Cold War branch schools trained specialists in weapons, engineering and small-unit tactics. Technical proficiency and coordinated fire improve, but longer courses delay deployment and live-fire training raises supply demand.',
  'SUBDOCTRINE_LEADERSHIP_OFFICER_DESC': 'Cold War officer academies and staff colleges built professional command teams. Planning and coordination improve, but longer initial schooling delays deployment; later specialisation adds personnel and promotion costs.',
 },
 'localisation/english/mdcw_cold_war_doctrines_l_english.yml': {
  'GRAND_DOCTRINE_MDCW_ACTIVE_DEFENSE_DESC': 'The US Army in 1976 emphasised winning the first battle through forward anti-tank defence and lateral concentration. Strong defensive fire trades away offensive movement and breakthrough capacity for sustained exploitation.',
  'GRAND_DOCTRINE_MDCW_PEOPLES_WAR_DESC': 'Chinese and Vietnamese protracted-war concepts combined local resistance, militia and regular forces. Dispersed preparation sustains a national struggle, but limits elaborate battle plans and armoured offensive proficiency.',
 },
}


def apply_expansion(items):
    for item in items:
        if item['id'] == 'mdcw_forest_envelopment':
            for effects in [item['effects'], *[r['effects'] for r in item['rewards']]]:
                if 'L_Inf_Bat' in effects:
                    effects['category_foot_inf'] = effects.pop('L_Inf_Bat')
            item['description'] = ('Finnish motti operations isolated road-bound columns through forest movement, also in summer campaigns in 1941 to 1944. '
                                   'Foot infantry and dismounted specialists gain local mobility and surprise, with less central battle preparation.')
            for stage in item['rewards']:
                stage['description'] = stage['description'].replace('Light infantry', 'Foot troops').replace('light infantry', 'foot troops')
        if item['id'] == 'mdcw_mission_rehearsal':
            item['effects']['max_planning_factor'] = .05
        def widen(effects):
            if 'category_foot_inf' in effects:
                for scope in FOOT[1:]:
                    assert scope not in effects
                    effects[scope] = deepcopy(effects['category_foot_inf'])
            if 'army_artillery_attack_factor' in effects:
                effects[ARTILLERY] = effects.pop('army_artillery_attack_factor')
        widen(item['effects'])
        for stage in item.get('rewards', []):
            widen(stage['effects'])
        for _, effects in item.get('milestones', []):
            widen(effects)


def brace_end(source, opening):
    depth = 0
    for match in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]', source[opening:]):
        if match[0] == '{':
            depth += 1
        elif match[0] == '}':
            depth -= 1
            if depth == 0:
                return opening + match.end()
    raise ValueError('Unclosed script block')


def activation_patch(source, ident, changes):
    from balance_revision import block_span
    from decimal import Decimal
    start, end = block_span(source, ident)
    block = source[start:end]
    cut = re.search(r'\n\t(?:rewards|milestones)\s*=\s*\{', block).start()
    prefix, tail = block[:cut], block[cut:]
    for key, (before, after) in changes.items():
        pattern = re.compile(r'(?m)^(\t' + re.escape(key) + r'\s*=\s*)(-?\d+(?:\.\d+)?)([^\r\n]*)$')
        match = pattern.search(prefix)
        if match:
            assert Decimal(match[2]) in {Decimal(str(v)) for v in (before, after) if v is not None}, (ident, key, match[2])
            prefix = prefix[:match.start(2)] + str(after) + prefix[match.end(2):]
        else:
            assert before is None, (ident, key)
            prefix = prefix.rstrip() + '\n\t' + MARKER + '\n\t' + key + ' = ' + str(after) + '\n'
    return source[:start] + prefix + tail + source[end:]


def widen_foot_source(source):
    """Clone only missing sibling scopes. Existing foot-category members never overlap."""
    edits = []
    for match in re.finditer(r'(?m)^(\t+)category_foot_inf\s*=\s*\{', source):
        indent = match[1]
        end = brace_end(source, source.index('{', match.start()))
        # Siblings extend to the first closing brace at the parent indentation.
        parent_end = re.search(r'(?m)^' + re.escape(indent[:-1]) + r'}', source[end:])
        upper = end + parent_end.start() if parent_end else len(source)
        parent_start = 0
        for previous in re.finditer(r'(?m)^' + re.escape(indent[:-1]) + r'[^\t\r\n].*?\{', source[:match.start()]):
            parent_start = previous.end()
        siblings = source[parent_start:upper]
        block = source[match.start():end]
        additions = []
        for scope in FOOT[1:]:
            if not re.search(r'(?m)^' + re.escape(indent + scope) + r'\s*=\s*\{', siblings):
                additions.append(block.replace(indent + 'category_foot_inf', indent + scope, 1))
        if additions:
            edits.append((end, '\n' + indent + MARKER + '\n' + '\n'.join(additions)))
    for end, text in reversed(edits):
        source = source[:end] + text + source[end:]
    return source


def integrate_text(source, replacements):
    for key, text in replacements.items():
        pattern = re.compile(r'(?m)^( ' + re.escape(key) + r':(?:0)? )"(?:\\.|[^"\\])*"$')
        source, count = pattern.subn(lambda m: m[1] + '"' + text + '"', source)
        if not count:
            assert key == 'GRAND_DOCTRINE_BATTLEFIELD_SUPPORT_DESC', key
            source += ' ' + key + ':0 "' + text + '"\n'
        else:
            assert count == 1, key
    lines = source.splitlines()
    if lines[1] != MARKER:
        lines.insert(1, MARKER)
    return '\n'.join(lines) + '\n'


def outputs(root, pending):
    result = {}
    for relative in (*GRAND_FILES, *SUB_FILES):
        source = pending.get(relative, (root / relative).read_text(encoding='utf-8-sig'))
        for ident, changes in PENALTIES.items():
            if re.search(r'(?m)^' + re.escape(ident) + r'\s*=\s*\{', source):
                source = activation_patch(source, ident, changes)
        if relative == GRAND_FILES[0]:
            # Battlefield Support previously reused Mission Command's description.
            from balance_revision import block_span
            start, end = block_span(source, 'battlefield_support')
            block = source[start:end].replace('description = GRAND_DOCTRINE_MISSION_COMMAND_DESC',
                                             'description = GRAND_DOCTRINE_BATTLEFIELD_SUPPORT_DESC')
            source = source[:start] + block + source[end:]
        if 'mdcw_cold_war_' in relative and 'subdoctrines' in relative:
            # Territorial fieldcraft belongs to all foot troops, including specialists.
            pattern = re.compile(r'(?m)^(\t+)L_Inf_Bat = \{\n(.*?)^\1}\n\1Militia_Bat = \{\n\2^\1}', re.S | re.M)
            source = pattern.sub(lambda m: m[1] + 'category_foot_inf = {\n' + m[2] + m[1] + '}', source)
        source = widen_foot_source(source)
        source = re.sub(r'\barmy_artillery_attack_factor(?=\s*=)', ARTILLERY, source)
        if not source.startswith(MARKER):
            source = MARKER + '\n# Native MD content and existing attribution retained; integrations are marked below.\n' + source
        result[relative] = source
    for relative, replacements in TEXT.items():
        result[relative] = integrate_text(pending.get(relative, (root / relative).read_text(encoding='utf-8-sig')), replacements)
    relative = UNIT_MODIFIERS
    source = (root / relative).read_text(encoding='utf-8-sig')
    if ARTILLERY not in source:
        source = source.rstrip()[:-1].rstrip() + '\n\t' + MARKER + '\n\t' + ARTILLERY + '\n}\n'
    if not source.startswith(MARKER):
        source = MARKER + '\n# Native MD unit modifiers retained.\n' + source
    result[relative] = source
    # The inherited STAT_MODIFIER_VALUE uses hard-coded G, even for negative stats.
    # Country modifiers and inverse cost/stat formatters retain their own polarity.
    result[COLOUR_PATH] = ('l_english:\n' + MARKER + '\n'
                          ' STAT_MODIFIER_VALUE:0 "$VALUE|=+0%$"\n'
                          ' modifier_army_sub_unit_category_artillery_attack_factor:0 "All Artillery Attack"\n')
    result[SYNC_PATH] = MARKER + '\n' + ARTILLERY + '\n'
    return result
