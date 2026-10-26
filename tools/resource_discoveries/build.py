# IMPERIA CW — Cold War: Generate the bounded discovery roll and single-use native resource receipt.
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HEADER = '# IMPERIA CW — Cold War: Fixed resource discoveries; preserve Imperia eligibility and monthly cadence.\n'


def outputs(data):
    trigger = HEADER + 'COLDWAR_resource_rubber_region = {\n\tOR = {\n'
    trigger += '\t\thas_resources_amount = { resource = rubber amount > 0 }\n'
    for region, label in data['rubber_regions'].items():
        trigger += f'\t\tregion = {region} # {label}\n'
    trigger += '\t}\n}\n'
    code = HEADER
    code += '# State scope. Freeze the type and amount before publishing the news.\n'
    code += 'COLDWAR_resource_discovery_roll = {\n\trandom_list = {\n'
    for resource in data['resources']:
        code += '\t\t100 = {\n'
        if resource['resource'] == 'rubber':
            code += '\t\t\tmodifier = { factor = 0 NOT = { COLDWAR_resource_rubber_region = yes } }\n'
        code += f'\t\t\tset_variable = {{ COLDWAR_discovery_type = {resource["id"]} }}\n'
        code += f'\t\t\tset_variable = {{ COLDWAR_discovery_amount = {resource["small"]} }}\n\t\t}}\n'
    code += '\t}\n\trandom_list = {\n'
    for size in data['sizes']:
        code += f'\t\t{size["weight"]} = {{\n'
        code += f'\t\t\tset_variable = {{ COLDWAR_discovery_size = {size["multiplier"]} }}\n'
        code += f'\t\t\tmultiply_variable = {{ COLDWAR_discovery_amount = {size["multiplier"]} }}\n\t\t}}\n'
    code += '\t}\n\tset_state_flag = COLDWAR_resource_discovery_pending\n}\n\n'
    code += '# State scope. Retain the selected result after claiming so observers still see the report.\n'
    code += 'COLDWAR_resource_discovery_claim = {\n'
    code += '\t# An already-open event from an older save has no prepared result.\n'
    code += '\thidden_effect = {\n\t\tif = {\n\t\t\tlimit = { NOT = { has_variable = COLDWAR_discovery_type } }\n'
    code += '\t\t\tCOLDWAR_resource_discovery_roll = yes\n\t\t}\n\t}\n'
    code += '\tif = {\n\t\tlimit = { hidden_trigger = { has_state_flag = COLDWAR_resource_discovery_pending } }\n'
    for resource in data['resources']:
        code += '\t\t' + ('if' if resource['id'] == 1 else 'else_if') + ' = {\n'
        code += f'\t\t\tlimit = {{ hidden_trigger = {{ check_variable = {{ COLDWAR_discovery_type = {resource["id"]} }} }} }}\n'
        code += f'\t\t\tadd_resource = {{ type = {resource["resource"]} amount = COLDWAR_discovery_amount }}\n\t\t}}\n'
    code += '\t\thidden_effect = {\n\t\t\tclr_state_flag = COLDWAR_resource_discovery_pending\n'
    code += '\t\t\tset_variable = { global.resource_spawner_counter = 0 }\n\t\t}\n\t}\n}\n'
    return {'common/scripted_triggers/COLDWAR_resource_discoveries.txt': trigger,
            'common/scripted_effects/COLDWAR_resource_discoveries.txt': code}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.loads((HERE / 'balance.json').read_text(encoding='utf-8'))
    for rel, text in outputs(data).items():
        path = ROOT / rel
        blob = text.encode('utf-8')
        if args.check:
            assert path.read_bytes() == blob, rel + ' needs regeneration'
        elif not path.exists() or path.read_bytes() != blob:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
    print('Fixed discovery sizes and regional rubber eligibility synchronized.')


if __name__ == '__main__':
    main()
