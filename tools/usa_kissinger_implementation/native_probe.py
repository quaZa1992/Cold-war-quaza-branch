# IMPERIA COLD WAR — Isolated Kissinger native smoke fixture on E:.
"""Freeze and test only a private profile. Never touch an existing HOI4 process.

The original USA probe supplies the proven hidden launcher and targeted-mask
loader. This adapter owns a fresh E: runtime, actual assets-only copy, KS fixture
and source manifest. Accelerated production-helper calls are not elapsed-year,
human approval, UI hover, save/reload or multiplayer evidence.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys

ROOT=Path(__file__).resolve().parents[2]
BASE=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/kissinger_20261028')
RUNS=BASE/'native'
ASSETS=BASE/'assets'
MARK='# IMPERIA COLD WAR — Isolated Kissinger native fixture.\n'
P='COLDWAR_USA_KS_'
STEM='COLDWAR_USA_kissinger'
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field
_spec=importlib.util.spec_from_file_location('ks_proven_native_driver',ROOT/'tools/usa_1970_expansion/native_probe.py')
driver=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(driver)
driver.OWN=RUNS;driver.ASSET_PROVIDER=ASSETS
SKIPPED=[]


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_private(path):
    path=Path(path).absolute()
    assert path.is_relative_to(BASE.absolute()),path
    for ancestor in (path,*path.parents):
        if ancestor==BASE.parent:break
        if ancestor.exists():assert not ancestor.is_symlink() and not ancestor.is_junction(),ancestor
    assert path.resolve().is_relative_to(BASE.resolve()),path
    return path


def write(path,text):
    path=check_private(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')


def safe_files(folder):
    """Never enumerate through a junction, symlink or other reparse directory."""
    folder=Path(folder)
    if folder.is_junction() or folder.is_symlink():
        SKIPPED.append(str(folder));return
    with os.scandir(folder) as entries:
        for entry in entries:
            information=entry.stat(follow_symlinks=False)
            if getattr(information,'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT:
                SKIPPED.append(entry.path);continue
            if entry.is_dir(follow_symlinks=False):yield from safe_files(Path(entry.path))
            elif entry.is_file(follow_symlinks=False):yield Path(entry.path),information


driver.files_in=safe_files


def assets():
    check_private(ASSETS);check_private(RUNS)
    result=driver.prepare_assets('kissinger_assets_20261028')
    result['skipped_reparse_paths']=sorted(set(SKIPPED))
    write(BASE/'ASSET_PREPARATION.json',json.dumps(result,indent=2)+'\n')
    return result


def source_files():
    for name in driver.RUNTIME:
        folder=ROOT/name
        if folder.is_dir():
            for path,_ in safe_files(folder):yield path
    yield ROOT/'descriptor.mod'


def plan():
    free=shutil.disk_usage('E:/').free
    return dict(project='IMPERIA COLD WAR',mode='read-only KS native preparation plan',
      private_root=str(BASE),assets_only_provider=str(ASSETS),runs=str(RUNS/'runs'),
      free_bytes=free,reserve_bytes=10*1024**3,
      uses_proven_launcher=str(ROOT/'tools/usa_1970_expansion/native_probe.py'),
      freeze_required_before_launch=True,existing_processes_never_stopped=True,
      junction_policy='Skip every reparse point and use robocopy /XJ. Never follow asset junctions.',
      planned_checks=['USA tree and all 41 KS focus references','Recipient offer, acceptance and duplicate protection','Native weekly expense/income consumer','Native field-division trigger and lasting stabilisation','Accelerated withdrawal, fading and recurrence','Bounded regional birth and finite cache acceptance','One real weekly update'],
      excluded=['Human recipient or AI acceptance choice','Hover rendering','Actual multi-year endurance','Save/reload and multiplayer'])


def block(key,body):
    if isinstance(body,list):body='\n'.join(body)
    return key+' = {\n'+body+'\n}'


def assertion(label,conditions):return driver.assertion('KS_'+label,conditions)


def fixture_calls(key,count):
    """Literal sequential source, with no assumed native loop construct."""
    assert count in (14,26,52,103,104,519)
    return '\n'.join(key+' = yes' for _ in range(count))


def inventory_checkpoint(stage):
    prefix='ICW_KS_NATIVE_'+stage
    return '\n'.join([
      'set_variable = { '+prefix+'_stock = num_equipment@infantry_weapons_type }',
      'set_variable = { '+prefix+'_field = num_equipment_in_armies@infantry_weapons_type }',
      'set_variable = { '+prefix+'_total = '+prefix+'_stock }',
      'add_to_variable = { '+prefix+'_total = '+prefix+'_field }',
      'log = "ICW_USA_NATIVE DIAG_CACHE_'+stage.upper()+' stock=[?'+prefix+'_stock] field=[?'+prefix+'_field] total=[?'+prefix+'_total]"'])


def diagnostic_boolean(label,conditions):
    return 'if = { limit = { '+conditions+' } log = "ICW_USA_NATIVE DIAG_'+label+'=yes" } else = { log = "ICW_USA_NATIVE DIAG_'+label+'=no" }'


def validate_fixture_ast(snapshot,events,on_actions):
    documentation=(driver.GAME/'documentation/effects_documentation.md').read_text(encoding='utf-8-sig')
    native=set(re.findall(r'^## ([a-z_][a-z_0-9]*)\s*$',documentation,re.M))
    helpers=set()
    for name in (STEM+'.txt','00_money_system.txt','00_budget_effects.txt'):
        helpers.update(n.key for n in nodes((snapshot/'common/scripted_effects'/name).read_text(encoding='utf-8-sig')))
    technologies=set()
    for path in (snapshot/'common/technologies').glob('*.txt'):
        for root in nodes(path.read_text(encoding='utf-8-sig')):
            if root.key=='technologies':technologies.update(n.key for n in root.children() if n.children())
    def tech_references(rows):
        for n in rows:
            if n.key=='has_tech':assert n.value in technologies,('Undefined fixture technology',n.value)
            tech_references(n.children())
    tech_references(nodes(events));tech_references(nodes(on_actions))
    def effect_rows(rows):
        for n in rows:
            key=n.key
            assert key!='while','Unsupported native fixture control block: while'
            if key in ('if','else_if'):
                effect_rows([x for x in n.children() if x.key!='limit'])
            elif key in ('else','hidden_effect','effect_tooltip') or key in ('USA','TUR','PER','SYR','KPI','KPS','ROOT','PREV') or str(key).isdigit():
                effect_rows(n.children())
            else:assert key in native or key in helpers,('Unknown native fixture effect/control',key)
    for event in nodes(events):
        for n in event.children():
            if n.key=='immediate':effect_rows(n.children())
    for root in nodes(on_actions):
        for hook in root.children():
            for n in hook.children():
                if n.key=='effect':effect_rows(n.children())


def decision_effect(snapshot,key):
    text=(snapshot/f'common/decisions/{STEM}.txt').read_text(encoding='utf-8-sig')
    for category in nodes(text):
        for decision in category.children():
            if decision.key!=key:continue
            effect=next(n for n in decision.children() if n.key=='complete_effect')
            return text[text.index('{',effect.start)+1:effect.end-1].strip()
    raise KeyError(key)


def fixture_sources(snapshot,focus_ids):
    # Every mutation below occurs in a fresh throwaway campaign. The two test
    # columns and the deleted starting units in state408 are explicit fixture
    # setup, not a production manpower/equipment grant or a real player action.
    first=[
      'log = "ICW_USA_NATIVE FIRST_HOUR"',
      assertion('TREE','has_focus_tree = USA_1970_focus'),
      assertion('SCENARIO','tag = USA IMP_is_1970_scenario = yes'),
      'set_variable = { treasury = 1000 }','set_variable = { gdp_total = 1000 }',P+'refresh_fiscal_usa = yes','clr_country_flag = MD_skip_treasury_cost',
      'add_equipment_to_stockpile = { type = infantry_weapons_1 amount = 5000 }',
      'set_variable = { ICW_KS_NATIVE_equipment_before = num_equipment@infantry_weapons_type }',
      P+'complete_covert = yes',
      assertion('NEGATIVE_SETUP','check_variable = { treasury = 999.995 }'),
      P+'complete_covert = yes',
      assertion('SETUP_ONCE','check_variable = { treasury = 999.995 }'),
      # Fixture-only nonzero native inflation proves the advertised nominal
      # transfer is appended after the MD inflation multiplier.
      'add_ideas = ICW_USA_NATIVE_inflation_probe',
      'set_variable = { ICW_KS_NATIVE_inflation_modifier = modifier@inflation_cost_multiplier_modifier }',
      assertion('NONZERO_NATIVE_INFLATION','check_variable = { ICW_KS_NATIVE_inflation_modifier > 0.5 }'),
      'set_variable = { ICW_KS_NATIVE_expense_before = '+P+'weekly_expense }',
      'calculate_additional_expense_rate = yes',
      'set_variable = { ICW_KS_NATIVE_native_expense_before = additional_expenses_rate }',
      P+'deal_irq_anatolia_offer = yes',
      assertion('TRANSIT_PENDING','has_country_flag = '+P+'deal_irq_anatolia_pending TUR = { has_country_flag = '+P+'deal_irq_anatolia_pending }'),
      assertion('PENDING_NO_SPIRITS','NOT = { has_idea = '+P+'deal_irq_anatolia_usa } TUR = { NOT = { has_idea = '+P+'deal_irq_anatolia_partner } }'),
      'TUR = { '+P+'deal_irq_anatolia_accept = yes }',
      assertion('ACTUAL_RECIPIENT_ACCEPTED',P+'deal_irq_anatolia_active = yes has_idea = '+P+'deal_irq_anatolia_usa TUR = { has_idea = '+P+'deal_irq_anatolia_partner }'),
      'TUR = { '+P+'deal_irq_anatolia_accept = yes }',
      assertion('DUPLICATE_ACCEPT_NO_SETUP','check_variable = { treasury = 999.995 }'),
      'calculate_additional_expense_rate = yes',
      'set_variable = { ICW_KS_NATIVE_native_expense_delta = additional_expenses_rate }',
      'subtract_from_variable = { ICW_KS_NATIVE_native_expense_delta = ICW_KS_NATIVE_native_expense_before }',
      assertion('NATIVE_WEEKLY_EXPENSE','check_variable = { ICW_KS_NATIVE_native_expense_delta > 0 } check_variable = { ICW_KS_NATIVE_native_expense_delta = 0.0004 }'),
      'TUR = { '+P+'calculate_streams = yes }',
      assertion('RECIPIENT_TRANSIT_INCOME','TUR = { check_variable = { '+P+'weekly_income > 0 } check_variable = { '+P+'weekly_income = 0.0004 } }'),
      'remove_ideas = ICW_USA_NATIVE_inflation_probe',
      'add_to_array = { array = imp_mil_sanc_by_us value = TUR }',P+'reconcile_deals = yes',
      assertion('SANCTION_SUSPENDS_PAIR','NOT = { has_idea = '+P+'deal_irq_anatolia_usa } TUR = { NOT = { has_idea = '+P+'deal_irq_anatolia_partner } }'),
      'remove_from_array = { array = imp_mil_sanc_by_us value = TUR }',P+'reconcile_deals = yes',
      assertion('RESTORE_PAIR',P+'deal_irq_anatolia_active = yes has_idea = '+P+'deal_irq_anatolia_usa TUR = { has_idea = '+P+'deal_irq_anatolia_partner }'),
      # Fixture prerequisite: deliberate breach is already authorised. This
      # does not claim the production political decision was clicked.
      'set_country_flag = '+P+'breach_per',P+'execute_irn_contacts = yes',P+'complete_irn_fund = yes',
      assertion('MATERIAL_COMMITTED','check_variable = { '+P+'cache_per = 1000 } check_variable = { '+P+'stage_per = 2 }'),
      'set_variable = { ICW_KS_NATIVE_equipment_delta = ICW_KS_NATIVE_equipment_before }',
      'subtract_from_variable = { ICW_KS_NATIVE_equipment_delta = num_equipment@infantry_weapons_type }',
      assertion('REAL_EQUIPMENT_DEBIT','check_variable = { ICW_KS_NATIVE_equipment_delta = 1000 }'),
      'PER = { set_variable = { treasury = 1000 } set_variable = { gdp_total = 100 } '+P+'refresh_host = yes clr_country_flag = MD_skip_treasury_cost delete_unit = { state = 408 disband = no }\n'
      'division_template = { name = "ICW KS Native Column" is_locked = yes regiments = { Militia_Bat = { x = 0 y = 0 } Militia_Bat = { x = 0 y = 1 } } }\n'
      '408 = { create_unit = { owner = PER count = 2 id = 197010281 division = "division_template = \\\"ICW KS Native Column\\\" start_experience_factor = 0.1 start_equipment_factor = 0 start_manpower_factor = 0" } }\n'
      +assertion('TWO_REAL_FIELD_DIVISIONS',P+'forces_per = yes 408 = { is_owned_and_controlled_by = PER is_fully_controlled_by = PER }')+'\n'+P+'per_security = yes\n'
      +assertion('SECURITY_FUNDED','has_country_flag = '+P+'security has_idea = '+P+'security_programme')+'\n'
      +fixture_calls(P+'tick_per',26)+'\n'
      +assertion('SUSTAINED_STABILISATION','check_variable = { '+P+'stabilisation > 90 } check_variable = { '+P+'unrest = 0 }')+'\n'
      'delete_unit = { division_template = "ICW KS Native Column" disband = no }\n'
      +decision_effect(snapshot,P+'per_end_programme')+'\n'
      +assertion('WITHDRAWN','NOT = { '+P+'forces_per = yes } NOT = { has_country_flag = '+P+'security }')+'\n'
      +fixture_calls(P+'tick_per',52)+'\n'
      +assertion('CALM_AFTER_WITHDRAWAL','check_variable = { '+P+'unrest = 0 } check_variable = { '+P+'stabilisation > 50 }')+'\n'
      +fixture_calls(P+'tick_per',104)+'\n'
      +assertion('RECURRENCE_AFTER_FADING','check_variable = { '+P+'unrest > 79 } check_variable = { '+P+'stabilisation = 0 }')+'\n}',
      P+'complete_irn_front = yes',
      assertion('ARMED_PROGRAMME','check_variable = { '+P+'stage_per = 3 } check_variable = { '+P+'cache_per > 1999 }'),
      'PER = { '+fixture_calls(P+'tick_per',14)+' }',
      assertion('MANUAL_WARNING_OPPORTUNITY','NOT = { country_exists = KPI } PER = { has_country_flag = '+P+'mobilisation_ready check_variable = { '+P+'qualifying_days > 29 } check_variable = { '+P+'warning_days > 44 } }'),
      # Invoke the real guarded birth separately from the passive weekly tick.
      # The USA decision also charges PP; this fixture tests its authoritative
      # host helper and does not claim that the decision UI was clicked.
      'PER = { '+P+'uprising_per = yes }',
      assertion('BOUNDED_BIRTH','country_exists = KPI 408 = { is_owned_and_controlled_by = KPI is_core_of = PER }'),
      assertion('OWN_ZERO_BALANCES','KPI = { check_variable = { treasury = 0 } check_variable = { debt = 0 } check_variable = { int_investments = 0 } has_variable = last_quarter_gdp_total }'),
      assertion('MINIMUM_REGIONAL_RESEARCH','KPI = { '+ ' '.join('has_tech = '+tech for tech in ('mdcw_infantry_weapons_1940','mdcw_util_vehicle_1940','mdcw_cnc_equipment_1940','mdcw_support_weapons_1940','mdcw_special_forces_1940','mdcw_camouflage_1940','mdcw_body_armor_1945','mdcw_anti_tank_1940'))+' OR = { AND = { has_dlc = "No Step Back" has_tech = mdcw_nsb_anti_air_1940 } AND = { NOT = { has_dlc = "No Step Back" } has_tech = mdcw_anti_air_1940 } } NOT = { has_tech = infantry_weapons_1 } }'),
      'KPI = { '+inventory_checkpoint('before')+'\nif = { limit = { has_tech = infantry_weapons_1 } log = "ICW_USA_NATIVE DIAG_CACHE_TECH infantry_weapons_1=yes" } else = { log = "ICW_USA_NATIVE DIAG_CACHE_TECH infantry_weapons_1=no" } }',
      assertion('NO_FREE_INITIAL_WEAPONS','KPI = { check_variable = { ICW_KS_NATIVE_before_total = 0 } NOT = { has_equipment = { convoy_1 > 0 } } }'),
      assertion('LOCAL_WAR','KPI = { has_war_with = PER }'),
      # Preserve the newly created actor for the real weekly startup check.
      # This fixture-only peace is not a production diplomacy outcome test.
      'KPI = { white_peace = PER }',
      'KPI = { '+decision_effect(snapshot,P+'per_liaison_kpi')+' }',
      assertion('PEACEFUL_LIAISON_SEPARATE_FROM_WAR','KPI = { has_country_flag = '+P+'partner_per NOT = { has_country_flag = '+P+'participate_per } }'),
      'log = "ICW_USA_NATIVE DIAG_CACHE_COMMITTED cache=[?'+P+'cache_per]"',
      'KPI = { '+decision_effect(snapshot,P+'per_cache_kpi')+' }',
      'KPI = { '+inventory_checkpoint('after')+'\nset_variable = { ICW_KS_NATIVE_delivery_delta = ICW_KS_NATIVE_after_total } subtract_from_variable = { ICW_KS_NATIVE_delivery_delta = ICW_KS_NATIVE_before_total } }',
      'log = "ICW_USA_NATIVE DIAG_CACHE_RECEIPT cache=[?'+P+'cache_per] delivered=[?'+P+'delivered_per_kpi]"',
      assertion('CACHE_DELIVERED','check_variable = { '+P+'cache_per = 0 } KPI = { check_variable = { ICW_KS_NATIVE_delivery_delta = 2000 } check_variable = { ICW_KS_NATIVE_after_total = 2000 } }'),
      assertion('CACHE_BUDGET_PAIR','has_idea = '+P+'aid_per_kpi_3_usa KPI = { has_idea = '+P+'aid_per_kpi_3_partner }'),
      'KPI = { '+decision_effect(snapshot,P+'per_cache_kpi')+' }',
      'KPI = { '+inventory_checkpoint('duplicate')+' }',
      assertion('CACHE_NOT_DUPLICATED','KPI = { check_variable = { ICW_KS_NATIVE_duplicate_total = ICW_KS_NATIVE_after_total } }'),
      # Failure-only private diagnostics. These one-unit trials never run in
      # a passing conservation case and cannot turn a failed assertion green.
      'KPI = { if = { limit = { check_variable = { ICW_KS_NATIVE_delivery_delta < 2000 } } add_equipment_to_stockpile = { type = infantry_weapons_1 amount = 1 } '+inventory_checkpoint('trial_unqualified')+'\nadd_equipment_to_stockpile = { type = infantry_weapons_1 amount = 1 producer = USA } '+inventory_checkpoint('trial_usa_producer')+' } }',
      'KPI = { if = { limit = { check_variable = { ICW_KS_NATIVE_before_field > 0 } } set_variable = { ICW_KS_NATIVE_refund_stock_before = num_equipment@infantry_weapons_type } delete_unit = { division_template = "Regional Defence Column" disband = yes } '+inventory_checkpoint('disband_refund')+'\nset_variable = { ICW_KS_NATIVE_refund_delta = ICW_KS_NATIVE_disband_refund_stock } subtract_from_variable = { ICW_KS_NATIVE_refund_delta = ICW_KS_NATIVE_refund_stock_before } log = "ICW_USA_NATIVE DIAG_COLUMN_REFUND actual_stock_delta=[?ICW_KS_NATIVE_refund_delta]" } }',
      'if = { limit = { KPI = { check_variable = { ICW_KS_NATIVE_before_field > 0 } } } country_event = { id = ICW_USA_NATIVE.2 hours = 1 } }',
      reconciliation_fixture(snapshot),
      'set_country_flag = ICW_USA_NATIVE_first_hour_done',
      'log = "ICW_USA_NATIVE FIRST_HOUR_COMPLETE"']
    for fid in focus_ids:
        first.insert(3,'if = { limit = { has_completed_focus = '+fid+' } log = "ICW_USA_NATIVE DIAG_FOCUS_COMPLETED '+fid+'" }')
    first.insert(3,'log = "ICW_USA_NATIVE KS_SOURCE_FOCUS_REFERENCES='+str(len(focus_ids))+'"')
    weekly=[
      'log = "ICW_USA_NATIVE FIRST_WEEK"',
      diagnostic_boolean('WEEKLY_AMBIENT_USA','tag = USA'),
      'USA = { '+diagnostic_boolean('WEEKLY_USA_SIGNED','has_country_flag = '+P+'deal_irq_anatolia_signed')+'\n'+diagnostic_boolean('WEEKLY_TRANSIT_RELATIONS',P+'deal_irq_anatolia_relations = yes')+'\n'+diagnostic_boolean('WEEKLY_BREACH_TUR','has_country_flag = '+P+'breach_tur')+' }',
      'TUR = { '+diagnostic_boolean('WEEKLY_TUR_SIGNED','has_country_flag = '+P+'deal_irq_anatolia_signed')+' }',
      assertion('STANDING_TRANSIT_AFTER_WEEK','USA = { '+P+'deal_irq_anatolia_active = yes has_idea = '+P+'deal_irq_anatolia_usa } TUR = { has_idea = '+P+'deal_irq_anatolia_partner }'),
      assertion('NEW_COUNTRY_WEEKLY_RECEIPT','KPI = { exists = yes has_variable = last_quarter_gdp_total NOT = { has_equipment = { convoy_1 > 0 } } }'),
      assertion('REPRESSION_EVENTS_DELIVERED','USA = { has_country_flag = '+P+'usa_report_syr } SYR = { has_country_flag = '+P+'host_report_syr }'),
      'set_country_flag = ICW_USA_NATIVE_complete',
      'log = "ICW_USA_NATIVE COMPLETE failures=[?ICW_USA_NATIVE_failures]"']
    delayed='KPI = { '+inventory_checkpoint('refund_one_hour')+'\nset_variable = { ICW_KS_NATIVE_refund_delayed_delta = ICW_KS_NATIVE_refund_one_hour_stock } subtract_from_variable = { ICW_KS_NATIVE_refund_delayed_delta = ICW_KS_NATIVE_refund_stock_before } log = "ICW_USA_NATIVE DIAG_COLUMN_REFUND_ONE_HOUR actual_stock_delta=[?ICW_KS_NATIVE_refund_delayed_delta]" }'
    events=MARK+'add_namespace = ICW_USA_NATIVE\n'+block('country_event',['id = ICW_USA_NATIVE.1','hidden = yes','is_triggered_only = yes',block('immediate',first)])+'\n'+block('country_event',['id = ICW_USA_NATIVE.2','hidden = yes','is_triggered_only = yes',block('immediate',delayed)])
    on_actions=MARK+block('on_actions',[
      block('on_startup',block('effect','log = "ICW_USA_NATIVE STARTUP"\nUSA = { country_event = { id = ICW_USA_NATIVE.1 hours = 1 } }')),
      block('on_weekly_USA',block('effect',block('if',[block('limit','has_country_flag = ICW_USA_NATIVE_first_hour_done NOT = { has_country_flag = ICW_USA_NATIVE_complete }'),'\n'.join(weekly)])))])
    return events,on_actions


def reconciliation_fixture(snapshot):
    """Independent Syrian case, separate from the Iranian 2,000-weapon test.

    Only the fixture seeds the opening diplomatic stage, GDP, reserve and test
    columns. Production guards, prices, population effect and reports are used.
    No date-skipping or injected completion receipts replace the weekly helper.
    """
    column='193 = { create_unit = { owner = SYR count = 2 id = 197010291 division = "division_template = \\\"ICW KS Reconciliation Column\\\" start_experience_factor = 0.1 start_equipment_factor = 0 start_manpower_factor = 0" } }'
    remove='delete_unit = { division_template = "ICW KS Reconciliation Column" disband = no }'
    return '\n'.join([
      'set_country_flag = '+P+'contact_syr','set_country_flag = '+P+'breach_syr',
      'set_variable = { '+P+'stage_syr = 3 }','set_variable = { '+P+'max_stage_syr = 3 }',P+'init_syr = yes',
      'SYR = { set_variable = { treasury = 1000 } set_variable = { gdp_total = 100 } clr_country_flag = MD_skip_treasury_cost '+P+'refresh_host = yes\n'
      'delete_unit = { state = 193 disband = no }\ndivision_template = { name = "ICW KS Reconciliation Column" is_locked = yes regiments = { Militia_Bat = { x = 0 y = 0 } Militia_Bat = { x = 0 y = 1 } } }\n'+column+'\n'
      'set_variable = { '+P+'unrest = 0 } set_variable = { '+P+'stabilisation = 80 }\n'+decision_effect(snapshot,P+'syr_autonomy')+'\n'+P+'syr_investment = yes\n'
      +fixture_calls(P+'tick_syr',519)+'\n'+P+'syr_consolidate = yes\n'
      +assertion('DECADE_NOT_EARLY','check_variable = { '+P+'qualifying_weeks = 519 } check_variable = { '+P+'reconciliation_weeks = 519 } NOT = { has_country_flag = '+P+'pacified } check_variable = { treasury = 998 }')+'\n'
      +P+'tick_syr = yes\n'+P+'syr_consolidate = yes\n'
      +assertion('DECADE_COMPACT','check_variable = { '+P+'qualifying_weeks = 520 } has_country_flag = '+P+'pacified has_idea = '+P+'consolidated_compact check_variable = { treasury = 988 }')+'\n'
      +P+'syr_consolidate = yes\n'+assertion('COMPACT_NO_DUPLICATE_COST','check_variable = { treasury = 988 }')+'\n'
      +fixture_calls(P+'tick_syr',52)+'\n'+assertion('COMPACT_NO_SPONTANEOUS_UNREST','check_variable = { '+P+'unrest = 0 } has_country_flag = '+P+'pacified')+'\n'
      # Separate fixture case: reset only this private test's completed clock,
      # not any production guard, and earn the shorter route from zero again.
      'clr_country_flag = '+P+'pacified remove_ideas = '+P+'consolidated_compact set_variable = { treasury = 1000 } set_variable = { '+P+'qualifying_weeks = 0 } '+P+'reconciliation_total = yes\n'
      +fixture_calls(P+'tick_syr',52)+'\n'+P+'syr_reform_rights_charter = yes\n'
      +fixture_calls(P+'tick_syr',52)+'\n'+P+'syr_reform_revenue = yes\n'
      +fixture_calls(P+'tick_syr',52)+'\n'+P+'syr_reform_integration = yes\n'
      +fixture_calls(P+'tick_syr',52)+'\n'+P+'syr_reform_reconstruction = yes\n'
      +assertion('FOUR_REFORMS_REAL_COST','check_variable = { treasury = 945 } check_variable = { '+P+'reform_credit = 208 }')+'\n'
      +fixture_calls(P+'tick_syr',103)+'\n'+P+'syr_consolidate = yes\n'
      +assertion('SIX_YEAR_ROUTE_NOT_EARLY','check_variable = { '+P+'qualifying_weeks = 311 } check_variable = { '+P+'reconciliation_weeks = 519 } NOT = { has_country_flag = '+P+'pacified } check_variable = { treasury = 945 }')+'\n'
      +P+'tick_syr = yes\n'+P+'syr_consolidate = yes\n'
      +assertion('SIX_YEAR_ROUTE_COMPLETES','check_variable = { '+P+'qualifying_weeks = 312 } has_country_flag = '+P+'pacified check_variable = { treasury = 935 }')+'\n}',
      P+'calculate_streams = yes\nset_variable = { ICW_KS_NATIVE_surge_expense_before = '+P+'weekly_expense }\nset_variable = { ICW_KS_NATIVE_surge_treasury_before = treasury }\nset_variable = { ICW_KS_NATIVE_surge_equipment_before = num_equipment@infantry_weapons_type }',
      P+'syr_intensify = yes',
      'set_variable = { ICW_KS_NATIVE_surge_treasury_delta = ICW_KS_NATIVE_surge_treasury_before } subtract_from_variable = { ICW_KS_NATIVE_surge_treasury_delta = treasury }\nset_variable = { ICW_KS_NATIVE_surge_equipment_delta = ICW_KS_NATIVE_surge_equipment_before } subtract_from_variable = { ICW_KS_NATIVE_surge_equipment_delta = num_equipment@infantry_weapons_type }',
      assertion('SURGE_REAL_PAYMENT','check_variable = { ICW_KS_NATIVE_surge_treasury_delta = 0.025 } check_variable = { ICW_KS_NATIVE_surge_equipment_delta = 1000 } check_variable = { '+P+'cache_syr = 1000 } SYR = { check_variable = { '+P+'pressure_weeks = 26 } }'),
      P+'calculate_streams = yes\nset_variable = { ICW_KS_NATIVE_surge_expense_delta = '+P+'weekly_expense } subtract_from_variable = { ICW_KS_NATIVE_surge_expense_delta = ICW_KS_NATIVE_surge_expense_before }',
      assertion('SURGE_WEEKLY_PRICE','check_variable = { ICW_KS_NATIVE_surge_expense_delta = 0.0025 }'),
      'SYR = { '+fixture_calls(P+'tick_syr',26)+'\n'+assertion('DEFENDED_COMPACT_HOLDS','has_country_flag = '+P+'pacified check_variable = { '+P+'unrest = 0 } check_variable = { '+P+'pressure_weeks = 0 }')+'\n'+remove+'\n'+decision_effect(snapshot,P+'syr_end_programme')+'\n}',
      P+'syr_intensify = yes\nSYR = { '+fixture_calls(P+'tick_syr',26)+' }',
      P+'syr_intensify = yes\nSYR = { '+fixture_calls(P+'tick_syr',26)+'\n'+assertion('NEGLECT_REOPENS_COMPACT','NOT = { has_country_flag = '+P+'pacified } check_variable = { '+P+'unrest > 79 }')+' }',
      assertion('REOPENING_IS_NOT_AUTOMATIC_BIRTH','NOT = { country_exists = KPS }'),
      'SYR = { '+column+'\n'+P+'syr_security = yes\n'+fixture_calls(P+'tick_syr',26)+'\n'+assertion('DEPLOYMENT_RESTORES_CONTROL','check_variable = { '+P+'unrest = 0 } NOT = { has_country_flag = '+P+'mobilisation_ready }')+'\n'
      # A new fictional massacre case is deliberately seeded only after the
      # separate containment assertions. Population is sampled immediately.
      +column+'\nset_variable = { '+P+'unrest = 100 }\n193 = { set_variable = { ICW_KS_NATIVE_population_before = state_population_k } }\n'+P+'syr_repression = yes\n'
      '193 = { set_variable = { ICW_KS_NATIVE_population_loss = ICW_KS_NATIVE_population_before } subtract_from_variable = { ICW_KS_NATIVE_population_loss = state_population_k } }\n'
      +assertion('CIVILIAN_POPULATION_ACTUALLY_REMOVED','193 = { check_variable = { ICW_KS_NATIVE_population_loss = 10 } } check_variable = { '+P+'civilian_losses = 10000 }')+'\n'
      +assertion('REPRESSION_HAS_POLITICAL_COST','has_idea = '+P+'repression_legacy check_variable = { '+P+'trauma_weeks = 156 } NOT = { '+P+'rights_syr = yes }')+'\n'
      +P+'syr_repression = yes\n193 = { set_variable = { ICW_KS_NATIVE_population_duplicate_loss = ICW_KS_NATIVE_population_before } subtract_from_variable = { ICW_KS_NATIVE_population_duplicate_loss = state_population_k } }\n'
      +assertion('CIVILIAN_LOSSES_NOT_DUPLICATED','193 = { check_variable = { ICW_KS_NATIVE_population_duplicate_loss = 10 } } check_variable = { '+P+'civilian_losses = 10000 }')+'\n}'])


def deterministic_events(snapshot,profile):
    relative=Path(f'events/{STEM}.txt');original=(snapshot/relative).read_text(encoding='utf-8')
    edits=[];count=0
    def shape(items):
        return [(n.key,n.op,shape(n.children()) if n.children() else n.value) for n in items if n.key!='ai_chance']
    for event in nodes(original):
        options=[n for n in event.children() if n.key=='option']
        for index,option in enumerate(options):
            weight=100 if index==len(options)-1 else 0
            old=[n for n in option.children() if n.key=='ai_chance']
            if old:
                for n in old:edits.append((n.start,n.end,'ai_chance = { factor = '+str(weight)+' }'))
            else:edits.append((option.end-1,option.end-1,'\nai_chance = { factor = '+str(weight)+' }\n'))
            count+=1
    changed=original
    for start,end,value in sorted(edits,reverse=True):changed=changed[:start]+value+changed[end:]
    assert shape(nodes(original))==shape(nodes(changed)),'Fixture altered non-AI event semantics'
    write(profile/'fixture'/relative,changed)
    return dict(project='IMPERIA COLD WAR',path=relative.as_posix(),source_sha256=digest(snapshot/relative),fixture_sha256=digest(profile/'fixture'/relative),option_weights_overridden=count,non_ai_ast_identical=True,purpose='AI review only; recipient production helpers called explicitly by the private fixture.')


def prepare(run_id,reuse_run_id=None):
    assert re.fullmatch(r'[A-Za-z0-9_-]{1,80}',run_id),run_id
    assert (ASSETS/'asset_manifest.json').is_file(),'Complete assets preparation first'
    report=ROOT/'docs/design/usa_kissinger_20261028/IMPLEMENTATION_VALIDATION_STATIC.json'
    model=ROOT/'docs/design/usa_kissinger_20261028/IMPLEMENTATION_VALIDATION_MODEL.json'
    validation=json.loads(report.read_text(encoding='utf-8'))
    behaviour=json.loads(model.read_text(encoding='utf-8'))
    validation_hash,model_hash,adapter_hash,launcher_hash=digest(report),digest(model),digest(__file__),digest(driver.__file__)
    assert validation['status']=='PASS' and behaviour['status']=='PASS','Current source/model checks must pass first'
    for relative,expected in validation['hashes'].items():
        assert digest(ROOT/relative)==expected,('Static validation is stale',relative)
    for relative,expected in behaviour['source_sha256'].items():
        assert digest(ROOT/relative)==expected,('Model validation is stale',relative)
    # The provider was copied before the final script freeze. Recheck every
    # task-owned sprite dependency and newborn flag against that exact copy.
    asset_manifest=json.loads((ASSETS/'asset_manifest.json').read_text(encoding='utf-8'))
    task_assets=set()
    def scan(items):
        for node in items:
            if node.key.lower() in ('texturefile','texturefile1','texturefile2'):
                task_assets.add(str(node.value).strip('"'))
            scan(node.children())
    scan(nodes((ROOT/f'interface/{STEM}.gfx').read_text(encoding='utf-8')))
    for tag in ('KPI','KPT','KPS'):
        for size in ('','medium/','small/'):
            task_assets.add('gfx/flags/'+size+tag+'.tga')
    for relative in sorted(task_assets):
        record=asset_manifest['assets'].get(relative)
        assert record and digest(ROOT/relative)==record['sha256']==digest(ASSETS/relative),('Task asset changed since provider preparation',relative)
    cache=None
    if reuse_run_id:
        assert re.fullmatch(r'[A-Za-z0-9_-]{1,80}',reuse_run_id) and reuse_run_id!=run_id
        cache=check_private(RUNS/'runs'/reuse_run_id/'snapshot')
        assert cache.is_dir(),'Requested private cache snapshot does not exist'
    run=check_private(RUNS/'runs'/run_id);run.mkdir(parents=True,exist_ok=False)
    snapshot,profile=run/'snapshot',run/'profile';snapshot.mkdir()
    sources=list(source_files());hashes={};original={}
    free=shutil.disk_usage(BASE).free
    total=sum(p.stat().st_size for p in sources)
    assert free>total+10*1024**3,'Insufficient E: free space for runtime snapshot and reserve'
    print(json.dumps(dict(project='IMPERIA COLD WAR',runtime_freeze_started=True,files=len(sources),bytes=total)),flush=True)
    copied=linked=0
    for index,source in enumerate(sources,1):
        relative=source.relative_to(ROOT);target=check_private(snapshot/relative)
        target.parent.mkdir(parents=True,exist_ok=True);before=digest(source)
        cached=check_private(cache/relative) if cache else None
        # Never modify any reused inode. Descriptors are deliberately separate
        # because profile_metadata rewrites their loader metadata below.
        if cached and relative.as_posix()!='descriptor.mod' and cached.is_file() and digest(cached)==before:
            os.link(cached,target);linked+=1
        else:
            shutil.copy2(source,target);copied+=1
        after=digest(target);assert before==after==digest(source),('Source changed while freezing',relative)
        hashes[relative.as_posix()]=after;original[relative.as_posix()]=before
        if index%3000==0:print(json.dumps(dict(project='IMPERIA COLD WAR',runtime_frozen_files=index)),flush=True)
    # Preserve original targeted masks and native/DLC inheritance. The live
    # working mod is not one of the enabled sources for this private campaign.
    masks=driver.profile_metadata(run,(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig'))
    hashes['descriptor.mod']=digest(snapshot/'descriptor.mod')
    tree=(snapshot/'common/national_focus/USA_1970.txt').read_text(encoding='utf-8-sig')
    focus_ids=[field(n.children(),'id') for t in nodes(tree) if t.key=='focus_tree' for n in t.children() if n.key=='focus' and str(field(n.children(),'id','')).startswith(P)]
    assert len(focus_ids)==len(set(focus_ids))==41
    events,on_actions=fixture_sources(snapshot,focus_ids)
    validate_fixture_ast(snapshot,events,on_actions)
    def check_fixture_numbers(rows):
        for node in rows:
            assert not (isinstance(node.value,str) and re.fullmatch(r'[+-]?\.\d+',node.value)),('Native fixture numeric literal lacks leading zero',node.key,node.value)
            check_fixture_numbers(node.children())
    check_fixture_numbers(nodes(events));check_fixture_numbers(nodes(on_actions))
    write(profile/'fixture/events/ICW_USA_NATIVE.txt',events)
    write(profile/'fixture/common/on_actions/zzzzzzzz_ICW_USA_NATIVE.txt',on_actions)
    write(profile/'fixture/common/ideas/ICW_USA_NATIVE.txt',MARK+'ideas = { country = { ICW_USA_NATIVE_inflation_probe = { picture = '+P+'consultations modifier = { inflation_cost_multiplier_modifier = 1.0 } } } }\n')
    override=deterministic_events(snapshot,profile)
    fixture={p.relative_to(profile).as_posix():digest(p) for p,_ in safe_files(profile/'fixture')}
    loaders={p.relative_to(profile).as_posix():digest(p) for p in [profile/'dlc_load.json',profile/'settings.txt',*sorted((profile/'mod').glob('*.mod'))]}
    for relative,expected in original.items():assert digest(ROOT/relative)==expected,('Source changed before final freeze',relative)
    # Recheck against the exact validated version, not merely whatever version
    # happened to be present when a late directory entry was copied.
    for relative,expected in validation['hashes'].items():
        assert digest(snapshot/relative)==expected==digest(ROOT/relative),('Validated runtime changed during freeze',relative)
    for relative,expected in behaviour['source_sha256'].items():
        assert digest(ROOT/relative)==expected,('Model input changed during freeze',relative)
    assert validation_hash==digest(report) and model_hash==digest(model),'Validation record changed during freeze'
    assert adapter_hash==digest(__file__) and launcher_hash==digest(driver.__file__),'Native fixture source changed during freeze'
    task_paths=[p.replace('\\','/') for p in validation['hashes']]
    task_paths+=['common/national_focus/USA_1970.txt','common/scripted_effects/00_money_system.txt','common/scripted_effects/COLDWAR_USA_gulf_effects.txt','common/scripted_triggers/COLDWAR_USA_gulf_triggers.txt','common/decisions/COLDWAR_USA_gulf_decisions.txt']
    freeze=dict(project='IMPERIA COLD WAR',feature='Kissinger statecraft native smoke',run_id=run_id,
      snapshot=str(snapshot),profile=str(profile),compiled_focuses=342,ks_focus_references=41,
      runtime_hashes=hashes,origin_runtime_hashes=original,fixture_hashes=fixture,loader_hashes=loaders,
      reused_private_snapshot=str(cache) if cache else None,reused_verified_hardlinks=linked,copied_source_files=copied,
      cache_policy='Reused only byte-identical private snapshot files. Changed files and descriptors copied independently; no existing inode overwritten.',
      isolated_asset_provider=str(ASSETS),asset_provider_manifest_sha256=digest(ASSETS/'asset_manifest.json'),asset_provider_descriptor_sha256=digest(ASSETS/'descriptor.mod'),
      task_asset_hashes={relative:asset_manifest['assets'][relative]['sha256'] for relative in sorted(task_assets)},
      asset_mode='Actual isolated E: asset copy and fully frozen runtime, no live-mod overlay',
      frozen_replace_paths=masks,fixture_event_overrides=[override],task_runtime_paths=sorted(set(task_paths)),
      metadata_only_differences={'descriptor.mod':dict(source_sha256=original['descriptor.mod'],snapshot_sha256=hashes['descriptor.mod'])},
      validation_sha256=validation_hash,model_sha256=model_hash,fixture_generator_sha256=adapter_hash,proven_launcher_sha256=launcher_hash,engine_sha256=digest(driver.GAME/'hoi4.exe'),
      skipped_reparse_paths=sorted(set(SKIPPED)),created_utc=datetime.now(timezone.utc).isoformat(),engine_launched=False,
      fixture_setup='Fresh private1970 campaign. Adds fixture-only USA weapons and a temporary native inflation modifier for the nominal-transfer assertion, removes only PER units in state408, creates two named zero-equipment fixture columns, later removes those columns, then restores peace after the real bounded KPI birth to preserve its real weekly startup check.',
      evidence_limits='Accelerated unchanged production-helper calls, direct recipient execution and one calendar week; not human/AI approval, hover, real multi-year endurance, save/reload or MP.')
    write(run/'freeze.json',json.dumps(freeze,indent=2)+'\n')
    write(run/'NOTICE.md','IMPERIA COLD WAR\n\nPrivate native fixture with byte-frozen runtime and copied assets. Original Paradox, Millennium Dawn and project authors retain their credits and terms; individual licences/permissions remain unknown where not identified. No source files or user profiles are modified. Fixture-only AI weights route events to Review; native production recipient helpers are called explicitly.\n')
    return dict(project='IMPERIA COLD WAR',prepared=str(run),freeze_sha256=digest(run/'freeze.json'),runtime_files=len(hashes),reused_verified_hardlinks=linked,copied_source_files=copied,ks_focus_references=41,engine_launched=False)


def verify_asset_payload():
    data=json.loads((ASSETS/'asset_manifest.json').read_text(encoding='utf-8'))
    check_private(ASSETS);skips=len(SKIPPED);inventory=[]
    for name in driver.ASSETS:
        inventory.extend(safe_files(ASSETS/name))
    assert len(SKIPPED)==skips,'Reparse point introduced into frozen asset provider'
    assert len(inventory)==len(data['assets']),'Frozen asset inventory changed'
    def verify(item):
        target,information=item;relative=target.relative_to(ASSETS).as_posix();record=data['assets'].get(relative)
        assert record and information.st_size==record['bytes'] and driver.digest(target)==record['sha256'],('Frozen asset changed',relative)
        return relative
    # Independent read-only hashes can run concurrently, as in the proven
    # asset preparation. Stream file contents in bounded chunks and report
    # progress without weakening the complete pre/post-launch inventory check.
    with ThreadPoolExecutor(max_workers=8) as executor:
        for count,_ in enumerate(executor.map(verify,inventory),1):
            if count%5000==0:print(json.dumps(dict(project='IMPERIA COLD WAR',asset_verification_files=count,asset_verification_total=len(inventory))),flush=True)
    return len(inventory)


def launch(run_id,freeze_sha256,duration,diagnostic_continue=False):
    assert re.fullmatch(r'[A-Za-z0-9_-]{1,80}',run_id),run_id
    run=check_private(RUNS/'runs'/run_id);freeze=json.loads((run/'freeze.json').read_text(encoding='utf-8'))
    assert digest(run/'freeze.json')==freeze_sha256,'Unreviewed freeze manifest'
    assert digest(__file__)==freeze['fixture_generator_sha256'],'Fixture adapter changed after preparation'
    assert digest(driver.__file__)==freeze['proven_launcher_sha256'],'Proven launcher changed after preparation'
    assert digest(driver.GAME/'hoi4.exe')==freeze['engine_sha256'],'Game executable changed after preparation'
    count=verify_asset_payload()
    print(json.dumps(dict(project='IMPERIA COLD WAR',frozen_asset_files_verified=count,launch_ready=True)),flush=True)
    result=driver.launch(run_id,freeze_sha256,duration,stop_on_failure=not diagnostic_continue)
    result.update(feature='Kissinger statecraft native smoke',accelerated_term_days=None,accelerated_term_expiry_observed=False,
      accelerated_regional_helper_cycles=True,actual_multi_year_endurance_tested=False,
      actual_365_day_endurance_tested=False,ks_focus_references=41,diagnostic_continue_after_failure=diagnostic_continue)
    try:result['frozen_assets_verified_after_launch']=verify_asset_payload()
    except Exception as exc:
        result['frozen_assets_verified_after_launch']=False
        result['asset_verification_failure']=str(exc)
        result['native_smoke_passed']=False
    write(run/'native_result.json',json.dumps(result,indent=2)+'\n')
    return result


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    modes=cli.add_mutually_exclusive_group(required=True)
    modes.add_argument('--plan',action='store_true');modes.add_argument('--prepare-assets',action='store_true')
    modes.add_argument('--prepare',action='store_true');modes.add_argument('--launch',action='store_true')
    cli.add_argument('--run-id',default=datetime.now(timezone.utc).strftime('ks_%Y%m%d_%H%M%S'))
    cli.add_argument('--freeze-sha256');cli.add_argument('--duration',type=int,default=900)
    cli.add_argument('--reuse-run-id',help='Reuse byte-verified unchanged private snapshot files in a NEW run; never mutate the old snapshot.')
    cli.add_argument('--diagnostic-continue',action='store_true',help='Keep failed status and collect the real weekly checkpoint after first-hour diagnostics.')
    args=cli.parse_args()
    if args.plan:result=plan()
    elif args.prepare_assets:result=assets()
    elif args.prepare:result=prepare(args.run_id,args.reuse_run_id)
    else:
        if not args.freeze_sha256:cli.error('--launch requires the reviewed --freeze-sha256')
        result=launch(args.run_id,args.freeze_sha256,args.duration,args.diagnostic_continue)
    if args.launch:
        summary={key:result.get(key) for key in ('project','run_id','native_smoke_passed','complete','elapsed_seconds','first_hour_observed','weekly_observed','failed_checks','task_diagnostic_lines','external_diagnostic_lines','frozen_assets_verified_after_launch')}
        summary.update(passed_checks=len(result.get('passed_checks',[])),full_result=str(RUNS/'runs'/args.run_id/'native_result.json'))
        print(json.dumps(summary,indent=2),flush=True)
    else:print(json.dumps(result,indent=2),flush=True)
    if args.launch and not result.get('native_smoke_passed'):raise SystemExit(1)


if __name__=='__main__':main()
