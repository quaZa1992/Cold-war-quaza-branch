# IMPERIA COLD WAR — Isolated Israel V2 native loading and transaction probe.
"""Explicit preparation/run only. Importing this module performs no I/O.

The private fixture overlays compile.build() before installation. It never
changes the user's saves, launcher playsets, installed sources or running game.
Only the process created by --run may be stopped. Every archive/profile/log is
under E:/HOI4_Mod_Tools/mdcoldwar/runtime/israel_v2/<timestamp>.
"""
from pathlib import Path,PurePosixPath
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
RUNTIME=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/israel_v2')
MARK='# IMPERIA COLD WAR — Private Israel V2 native probe fixture.\n'
PREFIX='ICW_ISR2_NATIVE'
SNAPSHOT_DIRS=('common','events','history','interface','localisation','map','portraits')
LINKED_ASSETS=('gfx','music','sound')
TRACE_FUNCTIONS={
    'ISR70_initialize','ISR2_initialize','ISR2_refresh','ISR2_retire_legacy_modifiers','ISR2_legacy_refund_pending',
    'ISR2_bilateral_init','ISR2_bilateral_reconcile','ISR2_domestic_init','ISR2_domestic_refresh',
    'ISR2_territories_init','ISR2_territories_refresh','ISR2_territories_pressure_reconcile',
    'ISR2_core_init','ISR2_core_refresh','calculate_additional_income_rate','calculate_additional_expense_rate',
    'calculate_interest_rate','update_money_dirty_variable'}


def sha(value):return hashlib.sha256(value).hexdigest()
def B(key,body):return key+' = {\n'+body+'\n}'
def IF(guard,body,other=''):return B('if',B('limit',guard)+'\n'+body)+('\n'+B('else',other) if other else '')
def V(key,value):return 'set_variable = { '+key+' = '+str(value)+' }'


def assert_private(path):
    base=RUNTIME.resolve();resolved=path.resolve()
    if resolved==base or not resolved.is_relative_to(base):
        raise ValueError('Expected a child of the private Israel V2 runtime directory: '+str(path))
    return resolved


def destination(base,relative):
    key=PurePosixPath(str(relative).replace('\\','/'))
    if key.is_absolute() or '..' in key.parts or ':' in str(key):raise ValueError('Unsafe relative fixture path: '+str(relative))
    result=base.joinpath(*key.parts)
    if not result.resolve().is_relative_to(base.resolve()):raise ValueError('Fixture path leaves its private root')
    return result


def write(base,relative,value):
    target=destination(base,relative);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(value if isinstance(value,bytes) else value.encode('utf-8'))
    return target


def dump(path,value):
    path.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))


def progress(phase,**values):
    print(json.dumps(dict(project='IMPERIA COLD WAR',phase=phase,**values)),flush=True)


def copy_tree(source,target,hashes,last_progress):
    # Inspect the entry itself. Never recurse through a junction or symlink.
    metadata=source.stat(follow_symlinks=False)
    if getattr(metadata,'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT or source.is_symlink():
        raise ValueError('Refusing to traverse reparse point: '+str(source))
    target.mkdir(parents=True,exist_ok=True)
    with os.scandir(source) as entries:
        for entry in entries:
            src=Path(entry.path);meta=entry.stat(follow_symlinks=False)
            if getattr(meta,'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT or entry.is_symlink():
                raise ValueError('Refusing to traverse reparse point: '+str(src))
            dest=target/entry.name
            if entry.is_dir(follow_symlinks=False):copy_tree(src,dest,hashes,last_progress)
            elif entry.is_file(follow_symlinks=False):
                before=sha(src.read_bytes());shutil.copy2(src,dest)
                if sha(dest.read_bytes())!=before or sha(src.read_bytes())!=before:
                    raise ValueError('Source changed while freezing: '+str(src))
                hashes[src.relative_to(ROOT).as_posix()]=before
            if time.monotonic()-last_progress[0]>=20:
                last_progress[0]=time.monotonic();progress('snapshot',frozen_files=len(hashes),current_directory=str(source))


def inventory_tree(source,hashes,last_progress):
    metadata=source.stat(follow_symlinks=False)
    if getattr(metadata,'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT or source.is_symlink():
        raise ValueError('Refusing to traverse reparse point: '+str(source))
    with os.scandir(source) as entries:
        for entry in entries:
            src=Path(entry.path);meta=entry.stat(follow_symlinks=False)
            if getattr(meta,'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT or entry.is_symlink():
                raise ValueError('Refusing to traverse reparse point: '+str(src))
            if entry.is_dir(follow_symlinks=False):inventory_tree(src,hashes,last_progress)
            elif entry.is_file(follow_symlinks=False):hashes[src.relative_to(ROOT).as_posix()]=sha(src.read_bytes())
            if time.monotonic()-last_progress[0]>=20:
                last_progress[0]=time.monotonic();progress('source_inventory',hashed_files=len(hashes))


def uncovered_base_changes(current,frozen,overrides):
    changed={key for key,value in current.items() if frozen.get(key)!=value}
    changed.update(key for key in frozen if key not in current)
    return sorted(changed-set(overrides))


def freeze_base_delta(current,frozen,overrides,root=ROOT):
    """Read exact current base text bytes, never mutate the reused snapshot.

    Canonical runtime overrides remain a separate owner. A removed native file
    cannot be represented by a normal higher-priority mod, so reuse refuses it.
    """
    removed=sorted(set(frozen)-set(current))
    if removed:raise ValueError(('Removed base inputs require a fresh full snapshot',removed))
    result={}
    allowed={'.txt','.yml','.gui','.gfx','.asset','.csv','.json','.lua'}
    reserved={'events/ICW_ISR2_NATIVE.txt','common/on_actions/zzzzzzzz_ICW_ISR2_NATIVE.txt'}
    for relative in uncovered_base_changes(current,frozen,overrides):
        key=PurePosixPath(relative)
        if key.is_absolute() or '..' in key.parts or ':' in relative or not key.parts or key.parts[0] not in SNAPSHOT_DIRS or key.suffix.lower() not in allowed or relative in reserved:
            raise ValueError(('Unsupported base delta path requires a fresh full snapshot',relative))
        source=root
        for part in key.parts:
            source=source/part;metadata=source.stat(follow_symlinks=False)
            if getattr(metadata,'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT or source.is_symlink():
                raise ValueError('Refusing base delta reparse point: '+str(source))
        raw=source.read_bytes()
        if sha(raw)!=current[relative]:raise ValueError(('Base delta changed during preparation',relative))
        try:raw.decode('utf-8-sig')
        except UnicodeDecodeError as error:raise ValueError(('Non-UTF8 base delta requires a fresh full snapshot',relative)) from error
        if b'\0' in raw:raise ValueError(('Binary base delta requires a fresh full snapshot',relative))
        result[relative]=raw
    return result


def hidden_startup():
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    return startup


def existing_games():
    result=subprocess.run(['powershell','-NoProfile','-Command',
        'Get-Process hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],
        capture_output=True,text=True,startupinfo=hidden_startup(),creationflags=subprocess.CREATE_NO_WINDOW)
    return [int(value) for value in result.stdout.split() if value.isdigit()]


def _read_script(text):
    # This is the same parser the canonical compiler uses, imported only on an
    # explicit preparation request, never as an import-time side effect.
    import sys
    sys.path.insert(0,str(ROOT/'tools/israel_1970'))
    from script_format import read
    return read(text)


def _field(rows,name):return next((v for k,_,v in rows if k==name),None)
def _walk(rows):
    for key,op,value in rows:
        yield key,op,value
        if isinstance(value,list):yield from _walk(value)


def action_call(payload,focus):
    action=payload['actions'][focus]['reward'].strip()
    rows=_read_script(action)
    if len(rows)!=1 or rows[0][1:]!=('=','yes'):raise ValueError(('Expected actual emitted reward helper',focus,action))
    return action


def offer_route(payload,focus):
    call=action_call(payload,focus);helper=_read_script(call)[0][0]
    effects=dict((k,v)for k,_,v in _read_script(payload['files']['common/scripted_effects/ISR2_bilateral_effects.txt'].decode('utf-8')))
    events=[v for k,_,v in _walk(effects[helper]) if k=='country_event']
    if len(events)!=1:raise ValueError(('Expected one real recipient event',focus))
    event_id=_field(events[0],'id')
    definitions=_read_script(payload['files']['events/ISR2_bilateral_events.txt'].decode('utf-8'))
    event=next(v for k,_,v in definitions if k=='country_event' and _field(v,'id')==event_id)
    options=[v for k,_,v in event if k=='option' and _field(v,'name')=='ISR2_bilateral_accept']
    actual=_field(options[0],'hidden_effect')
    if not actual:raise ValueError(('Missing actual guarded recipient acceptance',event_id))
    def serialize(rows):return '\n'.join(B(k,serialize(v)) if isinstance(v,list) else k+' '+op+' '+v for k,op,v in rows)
    return dict(event_id=event_id,acceptance=serialize(actual),offer_helper=helper)


def verify_slot_source(payload):
    """Static source assertion, separate from native actual building checks."""
    from runtime_money import bounds
    script=payload['files']['common/scripted_effects/ISR2_core_effects.txt'].decode('utf-8')
    helper=_read_script(action_call(payload,'ISR2_bonds_plant'))[0][0]
    start,end=bounds(script,helper);rows=_read_script(script[start:end])
    result=[]
    for state in ('205','206'):
        found=[v for k,_,v in _walk(rows) if k==state and isinstance(v,list) and any(x[0]=='add_building_construction' for x in v)]
        if len(found)!=1:raise ValueError(('Expected one asset transaction per state',state))
        commands=found[0]
        slot=next((i for i,x in enumerate(commands) if x[0]=='add_extra_state_shared_building_slots'),None)
        construction=[(i,_field(v,'level'))for i,(k,_,v)in enumerate(commands)if k=='add_building_construction']
        if slot is None or int(commands[slot][2])!=sum(int(level) for _,level in construction) or any(i<slot for i,_ in construction):
            raise ValueError(('Missing same-transaction slots before actual construction',state))
        result.append(dict(state=int(state),slots=int(commands[slot][2]),levels=sum(int(level)for _,level in construction),status='PASS_SOURCE'))
    return result


def instrument_recipient_events(text):
    # Add only logging to the actual country-event immediate blocks. There are
    # no automatic acceptance or eligibility changes in this instrumentation.
    from runtime_integration import top_blocks
    edits=[];routes=[]
    for key,start,opening,end in top_blocks(text):
        if key!='country_event':continue
        body=text[opening+1:end-1]
        ident=re.search(r'\bid\s*=\s*(ISR2_bilateral\.\d+)',body)[1]
        if re.search(r'\bimmediate\s*=',body):raise ValueError('Recheck native event instrumentation: existing immediate')
        log=B('immediate','log = "'+PREFIX+' ARRIVAL '+ident+' tag=[THIS.GetTag]"')
        edits.append((opening+1,'\n'+log+'\n'));routes.append(ident)
    for at,value in reversed(edits):text=text[:at]+value+text[at:]
    return text,routes


def instrument_startup_calls(files):
    """Only add scoped logs at real helper entry/exit and occupation seeding.

    This deliberately does not alter a guard, reorder a call, skip an effect or
    invoke a helper which the ordinary payload would not already execute.
    """
    from runtime_integration import top_blocks
    result=dict(files);receipts={}
    for path,raw in files.items():
        if not path.startswith('common/scripted_effects/') or not path.endswith('.txt'):continue
        text=raw.decode('utf-8');edits=[];names=[]
        for name,start,opening,end in top_blocks(text):
            if name not in TRACE_FUNCTIONS:continue
            def message(direction):
                command='log = "'+PREFIX+' TRACE '+direction+' '+name+' tag=[THIS.GetTag] date=[GetDateText]"'
                return IF('ISR2_is_scenario = yes',command)+'\n'
            edits += [(opening+1,'\n'+message('ENTER')),(end-1,'\n'+message('EXIT'))]
            names.append(name)
            if name=='ISR2_territories_init':
                body=text[opening+1:end-1]
                for match in re.finditer(r'(?m)^[ \t]*(start_resistance|set_resistance|set_compliance)\s*=\s*[^\n]+',body):
                    at=opening+1+match.start();finish=opening+1+match.end()
                    statement=match[0].strip().replace('"','')
                    edits += [(at,'log = "'+PREFIX+' TRACE BEFORE '+statement+'"\n'),
                              (finish,'\nlog = "'+PREFIX+' TRACE AFTER '+statement+'"')]
        if not edits:continue
        for at,value in sorted(edits,reverse=True):text=text[:at]+value+text[at:]
        result[path]=text.encode('utf-8')
        receipts[path]=dict(source_sha256=sha(raw),instrumented_sha256=sha(result[path]),functions=names)
    if not {'ISR2_initialize','ISR2_refresh'}.issubset({n for record in receipts.values() for n in record['functions']}):
        raise ValueError('Trace did not find actual root bootstrap/refresh providers')
    return result,receipts


def baseline_fixture():
    """Control fixture: frozen base only, no compiled Israel V2 overrides."""
    checks=dict(baseline_scenario_1970='IMP_is_1970_scenario = yes date > 1969.12.31 date < 1970.2.1',
        baseline_israel_tree='has_focus_tree = ISR70_focus',baseline_native_gdp='check_variable = { gdp_total > 0 }')
    assertions='\n'.join(IF(trigger,'log = "'+PREFIX+' PASS '+name+'"','log = "'+PREFIX+' FAIL '+name+'"')for name,trigger in checks.items())
    event=MARK+'add_namespace = '+PREFIX+'\n'+B('country_event','id = '+PREFIX+'.1\nhidden = yes\nis_triggered_only = yes\n'+B('immediate',
        'log = "'+PREFIX+' PHASE BASELINE_CONTROL_CURRENT_BASE_NO_COMPILED_OVERRIDES"\n'+assertions+'\nlog = "'+PREFIX+' COMPLETE BASELINE_CONTROL date=[GetDateText]"'))+'\n'
    onactions=MARK+B('on_actions',B('on_startup',B('effect','log = "'+PREFIX+' BASELINE_STARTUP"\n'+B('ISR',
        IF('exists = yes','country_event = { id = '+PREFIX+'.1 days = 1 }')))))+'\n'
    return dict(events=event,onactions=onactions,checks=list(checks),event_arrival=None,slot_source=[],
        limitations=['Baseline control uses the selected immutable snapshot plus exact-byte fresh base-text deltas, with no newly compiled Israel V2 overrides.',
            'This profile tests only control startup and native baseline GDP/tree, not Israel V2 mechanics.',
            'It must run separately and sequentially from other HOI4 profiles; no existing process is stopped.'])


def financial_diagnostics(stage):
    prefix='log = "'+PREFIX+' DIAG '+stage+' '
    rows=[prefix+'ECON gdp=[?gdp_total] treasury=[?treasury] debt=[?debt] pool=[?ISR2_private_available] ruling=[?ruling_party]"',
        prefix+'CAPITAL paid=[?ISR2_private_paid] required=[?ISR2_private_required] USA=[?ISR2_private_paid_USA] GER=[?ISR2_private_paid_GER] ROM=[?ISR2_private_paid_ROM]"',
        prefix+'FIFO oldest=[?ISR2_private_oldest_days] index=[?ISR2_private_oldest_index] take=[?ISR2_private_take]"',
        prefix+'YANAI used=[?ISR2_territories_yanai_used] quote=[?ISR2_territories_yanai_quote] reserve=[?ISR2_territories_yanai_reserve] state1=[?ISR2_territories_yanai_state_1]"',
        prefix+'PROJECT quote=[?ISR2_territories_project_quote] price=[?ISR2_territories_project_price] tier208=[?ISR2_territories_tiers_208]"']
    for label,condition in [
        ('YANAI_RECEIPT','has_country_flag = ISR2_territories_done_labor_yanai'),
        ('YANAI_TERM','has_country_flag = ISR2_territories_yanai_term'),
        ('ALIGNMENT_GATE','western_social_democrats_are_in_power = yes'),
        ('COVER_CAP','check_variable = { ISR2_territories_yanai_used < 2 }'),
        ('NAHAL_RECEIPT','has_country_flag = ISR2_territories_done_controlled_sites'),
        ('NAHAL_COOLDOWN','has_country_flag = ISR2_territories_cooldown_controlled_sites')]:
        rows.append(IF(condition,prefix+label+' YES"',prefix+label+' NO"'))
    # The readiness diagnostic temporarily supplies the exact prospective input
    # and restores it before the real action. It consumes no money or capital.
    rows += [V('ICW_ISR2_diag_saved_required','ISR2_private_required'),
        V('ISR2_private_required','{ value = gdp_total multiply = 0.005 }'),
        prefix+'DIAG_ONLY_QUOTE_005 required=[?ISR2_private_required]"',
        IF('ISR2_private_ready = yes',prefix+'PRIVATE_READY_005 YES"',prefix+'PRIVATE_READY_005 NO"'),
        V('ISR2_private_required','ICW_ISR2_diag_saved_required')]
    return '\n'.join(rows)


def fixture(payload):
    checks={}
    def check(name,trigger):
        if name in checks:raise ValueError('Duplicate check '+name)
        checks[name]=trigger
        return IF(trigger,'log = "'+PREFIX+' PASS '+name+'"','log = "'+PREFIX+' FAIL '+name+'"')
    def equal(var,expected):return 'check_variable = { var = '+var+' value = '+str(expected)+' compare = equals }'
    def expected(key,base,amount):return V(key,'{ value = '+base+' add = '+str(amount)+' }')
    finance=offer_route(payload,'ISR2_financing_usa');delivery=offer_route(payload,'ISR2_irrigation_exports')
    workforce_ids=[n['id'] for n in payload['data']['nodes'] if any(e.get('native_key')=='total_workforce_modifier' for e in n['effects'])]
    if len(workforce_ids)!=3:raise ValueError('Expected exactly three actual workforce action helpers')
    base=[check('scenario_1970','date > 1969.12.31 date < 1970.2.1 ISR2_is_scenario = yes'),
        check('initialized_tree','has_country_flag = ISR2_initialized has_focus_tree = ISR70_focus'),
        check('golda_and_alignment','has_country_leader = { name = "Golda Meir" ruling_only = yes } check_variable = { ruling_party = 3 }'),
        check('one_percent_threshold',equal('election_threshold','.01')),
        check('native_positive_gdp','has_variable = gdp_total check_variable = { gdp_total > 0 }'),
        check('four_starting_spirits',' '.join('has_idea = ISR2_start_'+s for s in ('citizen_army','histadrut','absorption','import_economy')))]
    for state in (208,209,213,587):
        base.append(check('occupation_'+str(state)+'_country_budget',f'has_dynamic_modifier = {{ modifier = ISR2_territories_occupation_{state}_budget }}'))
        base.append(check('occupation_'+str(state)+'_state_ISR_scope',f'{state} = {{ has_dynamic_modifier = {{ modifier = ISR2_territories_occupation_{state}_local scope = ISR }} }}'))
        diagnostic=[B('owner',f'log = "{PREFIX} DIAG OCCUPATION_{state} OWNER=[THIS.GetTag]"'),
                    B('controller',f'log = "{PREFIX} DIAG OCCUPATION_{state} CONTROLLER=[THIS.GetTag]"')]
        for name,condition in [('CORE_ISR','is_core_of = ISR'),('OWNER_ISR','is_owned_by = ISR'),('CONTROLLER_ISR','is_controlled_by = ISR'),
            ('UNSCOPED_QUERY',f'has_dynamic_modifier = {{ modifier = ISR2_territories_occupation_{state}_local }}')]:
            diagnostic.append(IF(condition,f'log = "{PREFIX} DIAG OCCUPATION_{state} {name} YES"',f'log = "{PREFIX} DIAG OCCUPATION_{state} {name} NO"'))
        base.append(B(str(state),'\n'.join(diagnostic)))
    base += [V('ICW_ISR2_workforce_before','modifier@total_workforce_modifier'),
        'log = "'+PREFIX+' PHASE BASELINE_UNMODIFIED gdp=[?gdp_total] treasury=[?treasury] workforce=[?ICW_ISR2_workforce_before]"',
        *(action_call(payload,f) for f in workforce_ids),'force_update_dynamic_modifier = yes',
        'country_event = { id = '+PREFIX+'.2 days = 1 }']
    second=[V('ICW_ISR2_workforce_delta','{ value = modifier@total_workforce_modifier subtract = ICW_ISR2_workforce_before }'),
        check('three_paid_workforce_actions',' '.join('has_country_flag = ISR2_core_done_'+f[5:] for f in workforce_ids)),
        check('native_workforce_plus_fifteen','check_variable = { ICW_ISR2_workforce_delta > .14999 } check_variable = { ICW_ISR2_workforce_delta < .15001 }'),
        action_call(payload,'ISR2_irrigation_exports'),
        'country_event = { id = '+PREFIX+'.3 days = 2 }']
    # Numerical transaction cases start only after the native baseline checks.
    # Saved values remain in this private unsaved fixture and are logged.
    tx=['log = "'+PREFIX+' PHASE EXPLICIT_TRANSACTION_FIXTURES"',
        V('ICW_ISR2_saved_gdp','gdp_total'),V('ICW_ISR2_saved_treasury','treasury'),V('ICW_ISR2_saved_debt','debt'),
        V('gdp_total',10),V('treasury',100),V('debt',10),
        B('USA',V('ICW_ISR2_saved_treasury','treasury')+'\n'+V('ICW_ISR2_saved_portfolio','int_investments')+'\n'+V('treasury',50)+'\n'+V('int_investments',5)),
        'log = "'+PREFIX+' FIXTURE_SAVED gdp=[?ICW_ISR2_saved_gdp] treasury=[?ICW_ISR2_saved_treasury] debt=[?ICW_ISR2_saved_debt]"',
        action_call(payload,'ISR2_bond_drive'),
        check('bond_cash_and_matching_debt',equal('treasury','100.8')+' '+equal('debt','10.8'))]
    for state in (205,206):tx.append(B(str(state),expected('ICW_ISR2_expected_civ','building_level@industrial_complex',1)))
    tx += [action_call(payload,'ISR2_bonds_plant'),
        check('paid_civil_factory_transaction',equal('treasury','100.5')),
        V('ICW_ISR2_civ_replay_cash','treasury'),action_call(payload,'ISR2_bonds_plant'),
        check('civil_factory_replay_has_no_charge',equal('treasury','ICW_ISR2_civ_replay_cash')),
        action_call(payload,'ISR2_financing_usa'),
        check('actual_financing_offer_pending','has_country_flag = ISR2_b_financing_usa_pending USA = { has_country_flag = ISR2_b_financing_usa_pending }'),
        B('USA',finance['acceptance']),
        check('actual_partner_cash_asset_escrow',B('USA',equal('treasury','49.8')+' '+equal('int_investments','5.2'))+' '+equal('ISR2_private_available','.2')+' '+equal('treasury','100.5')),
        B('USA',finance['acceptance']),
        check('financial_acceptance_replay_changes_nothing',B('USA',equal('treasury','49.8')+' '+equal('int_investments','5.2'))+' '+equal('ISR2_private_available','.2')),
        financial_diagnostics('BEFORE_YANAI'),action_call(payload,'ISR2_labor_yanai'),financial_diagnostics('AFTER_YANAI')]
    for building,level in (('agriculture_district',1),('infrastructure',1)):
        tx.append(B('208',expected('ICW_ISR2_expected_'+building,'building_level@'+building,level)))
    tx += [financial_diagnostics('BEFORE_NAHAL_FIRST'),action_call(payload,'ISR2_controlled_sites'),financial_diagnostics('AFTER_NAHAL_FIRST'),
        check('real_private_capital_consumed',equal('ISR2_private_available','.15')+' '+equal('ISR2_private_paid','.05')+' '+equal('ISR2_territories_yanai_used',1)),
        check('public_cofinancing_paid_once',equal('treasury','100.38')),
        V('ICW_ISR2_site_replay_cash','treasury'),financial_diagnostics('BEFORE_NAHAL_DUPLICATE'),action_call(payload,'ISR2_controlled_sites'),financial_diagnostics('AFTER_NAHAL_DUPLICATE'),
        check('site_replay_changes_no_cash_or_capital',equal('treasury','ICW_ISR2_site_replay_cash')+' '+equal('ISR2_private_available','.15')+' '+equal('ISR2_territories_tiers_208',1)),
        'country_event = { id = '+PREFIX+'.4 days = 1 }']
    assets=[check('real_two_civs_once',' '.join(B(str(s),equal('building_level@industrial_complex','ICW_ISR2_expected_civ'))for s in (205,206))),
        check('real_cofinanced_state_assets','208 = { '+equal('building_level@agriculture_district','ICW_ISR2_expected_agriculture_district')+' '+equal('building_level@infrastructure','ICW_ISR2_expected_infrastructure')+' }'),
        'country_event = { id = '+PREFIX+'.5 days = 4 }']
    finish=[check('ten_day_runtime_alive','ISR2_is_scenario = yes has_country_flag = ISR2_initialized check_variable = { gdp_total > 0 }'),
        'log = "'+PREFIX+' COMPLETE date=[GetDateText]"']
    events=[MARK+'add_namespace = '+PREFIX]
    for i,body in enumerate((base,second,tx,assets,finish),1):
        events.append(B('country_event','id = '+PREFIX+'.'+str(i)+'\nhidden = yes\nis_triggered_only = yes\n'+B('trigger','ISR2_is_scenario = yes')+'\n'+B('immediate','\n'.join(body))))
    onactions=MARK+B('on_actions',B('on_startup',B('effect','log = "'+PREFIX+' STARTUP"\n'+B('ISR',
        IF('exists = yes\nISR2_is_scenario = yes','country_event = { id = '+PREFIX+'.1 days = 2 }')))))+'\n'
    return dict(events='\n\n'.join(events)+'\n',onactions=onactions,checks=list(checks),
        event_arrival=dict(id=delivery['event_id'],tag='ETH'),finance=finance,
        workforce_actions=workforce_ids,slot_source=verify_slot_source(payload),
        limitations=['Workforce uses real starting values and paid emitted helpers; it bypasses focus time/prerequisite gameplay.',
            'Exact cashflow cases explicitly set saved isolated GDP/Treasury/portfolio values after the native baseline.',
            'US acceptance is scripted through the actual emitted recipient-option body; no human UI consent was tested.',
            'The separate Ethiopian offer measures actual country-event arrival with logging-only instrumentation.',
            'Building levels are checked natively; matching slot grants are asserted from their exact emitted source.',
            'Soviet loan, two-year expiry, manual UI, saves/reloads and multiplayer remain UNRUN.'])


def prepare(reuse_snapshot=None,variant='smoke'):
    if os.name!='nt':raise RuntimeError('This native profile preparer requires Windows')
    if variant not in ('smoke','trace','baseline'):raise ValueError('Unknown probe variant')
    if variant=='baseline' and reuse_snapshot is None:raise ValueError('Baseline control requires an explicitly selected immutable frozen snapshot')
    import sys
    sys.path.insert(0,str(ROOT/'tools/israel_v2'))
    from compile import build
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    run=RUNTIME/stamp;assert_private(run);run.mkdir(parents=True,exist_ok=False)
    snapshot,profile=run/'snapshot',run/'profile';hashes={};snapshot_hashes={};last=[time.monotonic()];parent_run=None
    progress('prepare',run=str(run),variant=variant,reuse_snapshot=str(reuse_snapshot) if reuse_snapshot else None)
    if reuse_snapshot is None:
        for name in SNAPSHOT_DIRS:copy_tree(ROOT/name,snapshot/name,hashes,last)
        descriptor=(ROOT/'descriptor.mod').read_bytes();write(snapshot,'descriptor.mod',descriptor);hashes['descriptor.mod']=sha(descriptor)
        snapshot_hashes=dict(hashes)
        for name in LINKED_ASSETS:
            source=ROOT/name;target=snapshot/name
            if not source.is_dir() or target.exists():raise ValueError('Invalid known asset junction '+name)
            subprocess.run(['cmd.exe','/c','mklink','/J',str(target),str(source)],check=True,capture_output=True,
                startupinfo=hidden_startup(),creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        parent_run=assert_private(Path(reuse_snapshot))
        parent=json.loads((parent_run/'probe_manifest.json').read_text(encoding='utf-8'))
        snapshot=assert_private(Path(parent['snapshot']))
        snapshot_hashes=parent.get('snapshot_hashes',parent['source_hashes'])
        changed=drift(snapshot,snapshot_hashes)
        if changed:raise ValueError(('Immutable parent snapshot drift; refusing reuse',changed))
        descriptor=(snapshot/'descriptor.mod').read_bytes()
        for name in SNAPSHOT_DIRS:inventory_tree(ROOT/name,hashes,last)
        hashes['descriptor.mod']=sha((ROOT/'descriptor.mod').read_bytes())
    generator_inputs=set()
    for folder in ('tools/israel_v2','tools/israel_1970'):
        for pattern in ('*.py','*.json'):generator_inputs.update((ROOT/folder).glob(pattern))
    generator_inputs.add(ROOT/'tools/focus_prerequisite_ui.py')
    generator_hashes={p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in sorted(generator_inputs)}
    # Compile only after freezing native inputs, then reject a changed source.
    # This prevents a fresh snapshot silently carrying an older compiled patch.
    payload=build() if variant!='baseline' else dict(files={})
    probe=fixture(payload) if variant!='baseline' else baseline_fixture()
    base_delta=freeze_base_delta(hashes,snapshot_hashes,payload['files']) if parent_run is not None else {}
    changed=drift(ROOT,hashes)+drift(ROOT,generator_hashes)
    if changed:raise ValueError(('Source changed while compiling the frozen fixture',changed))
    progress('compiled_fixture',files=len(payload['files']),fresh_base_delta_files=len(base_delta),checks=len(probe['checks']))
    # All new outputs, including gfx, go into the real fixture directory. The
    # base snapshot's asset junction is never a destination of write().
    fixture_root=profile/'fixture';payload_hashes={};trace_receipts={}
    for relative,value in base_delta.items():write(fixture_root,relative,value)
    override_files=payload['files']
    if variant=='trace':override_files,trace_receipts=instrument_startup_calls(override_files)
    for relative,value in override_files.items():
        target=write(fixture_root,relative,value);payload_hashes[relative]=sha(target.read_bytes())
    events_path='events/ISR2_bilateral_events.txt'
    event_receipt=None
    if variant!='baseline':
        native=payload['files'][events_path].decode('utf-8')
        instrumented,arrival_ids=instrument_recipient_events(native)
        write(fixture_root,events_path,instrumented)
        event_receipt=dict(source_sha256=sha(native.encode('utf-8')),fixture_sha256=sha(instrumented.encode('utf-8')),event_ids=arrival_ids)
    write(fixture_root,'events/ICW_ISR2_NATIVE.txt',probe['events'])
    write(fixture_root,'common/on_actions/zzzzzzzz_ICW_ISR2_NATIVE.txt',probe['onactions'])
    base_descriptor=descriptor.decode('utf-8-sig')
    base_name=re.search(r'(?m)^name\s*=\s*"([^"]+)"',base_descriptor)[1]
    base_descriptor=re.sub(r'(?m)^path\s*=.*\n?','',base_descriptor)
    write(profile,'mod/base.mod',base_descriptor+'\npath="'+snapshot.as_posix()+'"\n')
    addon=MARK+'name="IMPERIA Israel V2 Native Probe"\ndependencies={ "'+base_name+'" }\npath="'+fixture_root.as_posix()+'"\n'
    write(profile,'mod/probe.mod',addon);write(fixture_root,'descriptor.mod',addon)
    write(profile,'dlc_load.json',json.dumps(dict(enabled_mods=['mod/base.mod','mod/probe.mod'],disabled_dlcs=[])))
    write(profile,'settings.txt',MARK+'language="l_english"\ngraphics={size={x=1024 y=720} fullScreen=no borderless=no}\nmaster_volume=0\n')
    fixture_files=list(base_delta)+list(payload_hashes)+['events/ICW_ISR2_NATIVE.txt','common/on_actions/zzzzzzzz_ICW_ISR2_NATIVE.txt','descriptor.mod']
    controls=['mod/base.mod','mod/probe.mod','dlc_load.json','settings.txt']
    manifest=dict(project='IMPERIA COLD WAR',status='PREPARED_NOT_RUN',variant=variant,run=str(run),snapshot=str(snapshot),profile=str(profile),
        immutable_parent_run=str(parent_run) if parent_run else None,snapshot_hashes=snapshot_hashes,
        source_root=str(ROOT),source_hashes=hashes,generator_hashes=generator_hashes,payload_hashes=payload_hashes,
        fresh_base_delta_hashes={relative:sha(value) for relative,value in base_delta.items()},
        canonical_payload_hashes={relative:sha(value) for relative,value in payload['files'].items()},startup_trace_receipts=trace_receipts,
        fixture_hashes={relative:sha(destination(fixture_root,relative).read_bytes()) for relative in fixture_files},
        profile_control_hashes={relative:sha(destination(profile,relative).read_bytes()) for relative in controls},
        diagnostic_file_names=sorted({PurePosixPath(relative).name for relative in list(payload_hashes)+list(base_delta) if PurePosixPath(relative).suffix in ('.txt','.gui','.gfx')}),
        instrumented_events=event_receipt,
        checks=probe['checks'],event_arrival=probe['event_arrival'],slot_source=probe['slot_source'],
        fixture_phases=probe['limitations'],native_gameplay_tested=False,linked_assets=list(LINKED_ASSETS))
    dump(run/'probe_manifest.json',manifest)
    optional=['actual_recipient_event_arrival','soviet_loan_native'] if variant!='baseline' else []
    report=dict(project='IMPERIA COLD WAR',status='PREPARED_NOT_RUN',variant=variant,native_test_executed=False,passed=[],failed=[],unrun=probe['checks']+optional,run=str(run))
    dump(run/'native_report.json',report);progress('prepared',run=str(run),frozen_files=len(hashes),checks=len(probe['checks']))
    return run


def drift(base,hashes):
    changed=[];last=time.monotonic()
    for count,(relative,digest) in enumerate(hashes.items(),1):
        path=destination(base,relative)
        if not path.is_file() or sha(path.read_bytes())!=digest:changed.append(relative)
        if time.monotonic()-last>=20:
            last=time.monotonic();progress('hash_check',root=str(base),checked=count,total=len(hashes))
    return changed


def run_probe(run,timeout=900):
    run=assert_private(run)
    manifest=json.loads((run/'probe_manifest.json').read_text(encoding='utf-8'))
    if manifest['status']!='PREPARED_NOT_RUN':raise ValueError('Use a fresh explicitly prepared probe directory')
    if existing_games():
        report=dict(project='IMPERIA COLD WAR',status='NOT_RUN_EXISTING_HOI4',native_test_executed=False,active_process_ids=existing_games(),unrun=manifest['checks'])
        dump(run/'native_report.json',report);progress('refused_existing_game',report=report);return 2
    source_drift=drift(ROOT,manifest['source_hashes']);generator_drift=drift(ROOT,manifest['generator_hashes'])
    snapshot=Path(manifest['snapshot']);profile=Path(manifest['profile']);fixture_root=profile/'fixture'
    if profile!=run/'profile' or not assert_private(profile).is_relative_to(run):raise ValueError('Prepared manifest names a different private profile')
    parent_run=manifest.get('immutable_parent_run')
    if parent_run:
        parent_run=assert_private(Path(parent_run))
        parent=json.loads((parent_run/'probe_manifest.json').read_text(encoding='utf-8'))
        if snapshot!=Path(parent['snapshot']):raise ValueError('Reused snapshot differs from its immutable parent receipt')
        assert_private(snapshot)
    elif snapshot!=run/'snapshot' or not assert_private(snapshot).is_relative_to(run):raise ValueError('Prepared snapshot leaves this private run')
    snapshot_hashes=manifest.get('snapshot_hashes',manifest['source_hashes'])
    snapshot_drift=drift(snapshot,snapshot_hashes);fixture_drift=drift(fixture_root,manifest['fixture_hashes'])
    controls_drift=drift(profile,manifest['profile_control_hashes'])
    if source_drift or generator_drift or snapshot_drift or fixture_drift or controls_drift:
        report=dict(project='IMPERIA COLD WAR',status='NOT_RUN_PREPARED_INPUT_DRIFT',native_test_executed=False,
            source_drift=source_drift,generator_drift=generator_drift,snapshot_drift=snapshot_drift,fixture_drift=fixture_drift,profile_control_drift=controls_drift,unrun=manifest['checks'])
        dump(run/'native_report.json',report);progress('refused_drift',report=report);return 2
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(profile),'-start_tag=ISR','-start_speed=3','-hands_off']
    if existing_games():
        report=dict(project='IMPERIA COLD WAR',status='NOT_RUN_EXISTING_HOI4_BEFORE_LAUNCH',native_test_executed=False,unrun=manifest['checks'])
        dump(run/'native_report.json',report);progress('refused_existing_game',report=report);return 2
    started=time.monotonic()
    try:process=subprocess.Popen(args,cwd=GAME,startupinfo=hidden_startup(),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except OSError as error:
        report=dict(project='IMPERIA COLD WAR',status='NOT_RUN_LAUNCH_FAILED',native_test_executed=False,error=str(error),unrun=manifest['checks'])
        dump(run/'native_report.json',report);progress('launch_failed',report=report);return 2
    manifest['status']='RUN_STARTED';manifest['pid']=process.pid;dump(run/'probe_manifest.json',manifest)
    progress('native_start',pid=process.pid,profile=str(profile));log='';last_progress=started;stopped=False
    try:
        while process.poll() is None and time.monotonic()-started<timeout:
            time.sleep(1)
            game_log=profile/'logs/game.log';log=game_log.read_text(encoding='utf-8-sig',errors='replace') if game_log.exists() else ''
            if PREFIX+' COMPLETE' in log:break
            if time.monotonic()-last_progress>=20:
                last_progress=time.monotonic();progress('native_wait',elapsed_seconds=int(time.monotonic()-started),startup_seen=PREFIX+' STARTUP' in log or PREFIX+' BASELINE_STARTUP' in log)
    finally:
        stopped=process.poll() is None
        if stopped:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    game_log=profile/'logs/game.log';log=game_log.read_text(encoding='utf-8-sig',errors='replace') if game_log.exists() else log
    error_log=profile/'logs/error.log';errors=error_log.read_text(encoding='utf-8-sig',errors='replace') if error_log.exists() else ''
    passed=[name for name in manifest['checks'] if PREFIX+' PASS '+name in log]
    failed=[name for name in manifest['checks'] if PREFIX+' FAIL '+name in log]
    arrival=manifest['event_arrival'];arrival_seen=bool(arrival and PREFIX+' ARRIVAL '+arrival['id']+' tag='+arrival['tag'] in log)
    if arrival_seen:passed.append('actual_recipient_event_arrival')
    unrun=[name for name in manifest['checks'] if name not in passed+failed]
    if arrival and not arrival_seen:unrun.append('actual_recipient_event_arrival')
    if manifest.get('variant','smoke')!='baseline':unrun.append('soviet_loan_native')
    crashes=sorted((profile/'crashes').glob('*/exception.txt')) if (profile/'crashes').exists() else []
    diagnostic_names=manifest['diagnostic_file_names']
    relevant=[line for line in errors.splitlines() if re.search(r'ISR2_|ICW_ISR2_NATIVE',line) or any(name in line for name in diagnostic_names)]
    source_drift=drift(ROOT,manifest['source_hashes']);generator_drift=drift(ROOT,manifest['generator_hashes'])
    snapshot_drift=drift(snapshot,snapshot_hashes);fixture_drift=drift(fixture_root,manifest['fixture_hashes'])
    # HOI4 may legitimately rewrite this private profile's settings/dlc state;
    # record that separately. Immutable fixture scripts must remain identical.
    controls_drift=drift(profile,manifest['profile_control_hashes'])
    completed=PREFIX+' COMPLETE' in log
    failed_exit=not stopped and process.returncode!=0
    success=completed and not(failed or crashes or failed_exit or relevant or source_drift or generator_drift or snapshot_drift or fixture_drift or [x for x in unrun if x!='soviet_loan_native'])
    status=('PASS_BASELINE_CONTROL' if manifest.get('variant')=='baseline' else 'PASS_SMOKE') if success else 'FAIL_ENGINE_CRASH_OR_EXIT' if crashes or failed_exit else 'FAIL_INCOMPLETE_OR_DIAGNOSTICS'
    version=GAME/'launcher-settings.json'
    report=dict(project='IMPERIA COLD WAR',status=status,variant=manifest.get('variant','smoke'),native_test_executed=True,native_test=success,success=success,
        israel_v2_runtime_tested=success and manifest.get('variant')!='baseline',immutable_parent_run=manifest.get('immutable_parent_run'),
        passed=passed,failed=failed,unrun=unrun,complete_checkpoint=completed,actual_recipient_event_arrival=arrival_seen,
        profile=str(profile),snapshot=str(snapshot),fixture=str(fixture_root),game_log=str(game_log),full_error_log=str(error_log),
        total_error_log_lines=len(errors.splitlines()),relevant_errors=relevant,crash_exceptions=[str(p)for p in crashes],
        source_drift=source_drift,generator_drift=generator_drift,snapshot_drift=snapshot_drift,fixture_drift=fixture_drift,private_profile_control_changes=controls_drift,
        elapsed_seconds=round(time.monotonic()-started,1),returncode=process.returncode,stopped_own_pid=process.pid if stopped else None,
        engine_version=json.loads(version.read_text(encoding='utf-8-sig')).get('rawVersion') if version.exists() else 'unknown',
        checkpoints=[line for line in log.splitlines() if PREFIX in line],limitations=manifest['fixture_phases'])
    dump(run/'native_report.json',report);progress('native_result',status=status,passed=len(passed),failed=failed,unrun=unrun,full_error_log=str(error_log))
    return 0 if success else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prepare',action='store_true',help='Freeze source and compile a private E: fixture; do not launch HOI4')
    group.add_argument('--prepare-from',type=Path,metavar='PRIOR_RUN',help='Prepare a new private profile reusing a verified immutable earlier snapshot')
    group.add_argument('--run',type=Path,metavar='PREPARED_DIRECTORY',help='Explicitly launch only this already prepared private fixture')
    parser.add_argument('--reuse-snapshot',type=Path,metavar='PRIOR_RUN',help='Verify and reuse an earlier immutable frozen base without copying it')
    parser.add_argument('--variant',choices=('smoke','trace','baseline'),default='smoke')
    parser.add_argument('--timeout',type=int,default=900)
    args=parser.parse_args()
    if args.prepare or args.prepare_from:
        if args.prepare_from and args.reuse_snapshot:parser.error('Choose one snapshot reuse argument')
        prepare(args.prepare_from or args.reuse_snapshot,args.variant);return 0
    if args.reuse_snapshot is not None or args.variant!='smoke':parser.error('Snapshot/variant selection is a preparation option only')
    return run_probe(args.run,args.timeout)


if __name__=='__main__':raise SystemExit(main())
