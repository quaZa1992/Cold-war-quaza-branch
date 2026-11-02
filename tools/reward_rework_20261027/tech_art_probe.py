# IMPERIA COLD WAR — Native technology-gated construction verification.
"""Extend the reward fixture without overwriting its historical evidence."""
from pathlib import Path
import time
import re

import engine_probe as probe
from script_ast import parse, first, emit

ROOT = Path(__file__).resolve().parents[2]
probe.REPORT = ROOT / 'docs/tech_art_review_20261027'
probe.PROFILE = Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/tech_art_review_20261027/native') / time.strftime('%Y%m%d_%H%M%S')
original_fixture = probe.fixture
original_write = probe.write


def write(relative, text):
    original_write(relative, text)
    if relative == 'fixture/events/COLDWAR_RW_probe.txt':
        # Native set_technology=0 does not revoke the researched start tech.
        # Withhold these three entries only in the private history override.
        history = (ROOT / 'history/countries/JAP - Japan.txt').read_text(encoding='utf-8')
        history = re.sub(r'(?m)^\s*microchip_production_[123]\s*=\s*1[^\n]*\n', '', history)
        original_write('fixture/history/countries/JAP - Japan.txt', probe.MARK + history)


def fixture():
    source, triggers = original_fixture()
    rows = parse(source)
    for key, operator, event in rows:
        if key != 'country_event' or first(event, 'id') != 'COLDWAR_RW_probe.3':
            continue
        code = emit(first(event, 'immediate'))
        # The actual installed microchip technologies unlock at most level 3.
        # Keep the same aggregate-cap boundary test at that researched ceiling.
        code = code.replace('set_technology = { microchip_production_1 = 1 }',
                            '')
        code = code.replace('level = 4', 'level = 2').replace('level = 3', 'level = 1')
        code = code.replace('building_level@microchip_plant = 4', 'building_level@microchip_plant = 2')
        anchor = '615 = {\n\tset_variable = { COLDWAR_RW_before_zero_gdp'
        assert anchor in code, 'Native fixture anchor changed'
        preparation = '615 = { add_extra_state_shared_building_slots = 80 set_building_level = { type = microchip_plant level = 0 } }\n'
        preparation += probe.check('JAP_missing_chip_technology_fixture',
                                   'NOT = { has_tech = microchip_production_1 } NOT = { has_tech = microchip_production_2 } NOT = { has_tech = microchip_production_3 }')
        preparation += probe.check('JAP_missing_technology_blocks_project', 'NOT = { COLDWAR_RW_can_JAP = yes }')
        no_award = 'NOT = { has_country_flag = COLDWAR_JAP_1970_microelectronics_capacity_receipt } 615 = { check_variable = { building_level@microchip_plant = 0 } } ' + probe.amount_is('treasury', 0)
        preparation += 'COLDWAR_JAP_1970_microelectronics_capacity_apply = yes\n'
        preparation += probe.check('JAP_missing_technology_no_charge_assets_or_receipt', no_award)
        preparation += 'set_technology = { microchip_production_1 = 1 }\n'
        preparation += probe.check('JAP_first_chip_tier_cannot_fund_two_levels', 'NOT = { COLDWAR_RW_can_JAP = yes }')
        preparation += 'COLDWAR_JAP_1970_microelectronics_capacity_apply = yes\n'
        preparation += probe.check('JAP_insufficient_tier_no_charge_assets_or_receipt', no_award)
        preparation += 'set_technology = { microchip_production_2 = 1 }\n'
        preparation += probe.check('JAP_second_chip_tier_allows_two_levels_from_zero', 'COLDWAR_RW_can_JAP = yes')
        preparation += 'set_technology = { microchip_production_3 = 1 }\n'
        code = code.replace(anchor, preparation + anchor, 1)
        immediate = first(event, 'immediate')
        immediate[:] = parse(code)
    return probe.MARK + emit(rows), triggers


probe.fixture = fixture
probe.write = write


def finalise_report():
    import json
    from focus_art import catalogue
    path = probe.REPORT / 'ENGINE_REPORT.json'
    report = json.loads(path.read_text(encoding='utf-8'))
    errors = (Path(report['profile']) / 'logs/error.log').read_text(encoding='utf-8-sig', errors='replace')
    records = re.split(r'(?=\[\d{2}:\d{2}:\d{2}\]\[)', errors)
    assets = {Path(texture).name.lower() for texture in catalogue()['themes'].values()}
    art_errors = [record.strip() for record in records
                  if 'coldwar_eastasia' in record.lower() or any(name in record.lower() for name in assets)]
    report['art_relevant_errors'] = art_errors
    report['fixture_technology_setup'] = 'Private JAP history override omits the three starting microchip technologies. The event asserts absence, then researches tiers 1, 2 and 3 in sequence. Live country history is unchanged.'
    report['success'] = report['success'] and not art_errors
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    probe.main()
    finalise_report()
