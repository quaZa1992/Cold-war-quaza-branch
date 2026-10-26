# IMPERIA CW — Cold War: retire the old IRA interface and seven-slider simulation.
"""Preserve unrelated British politics; translate remaining focus/event rewards.

Original custom files are retained outside game-loading folders for provenance.
The adapters below consume existing political focus rewards through the new
regional organisation strength. They do not define any old IRA variables.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/spain_1970_v2'))
from script_ast import parse, emit, first

OLD = {
    'ENG_ira_militancy': 1, 'ENG_ira_support': .25,
    'ENG_ira_foreign_funding': .25, 'ENG_ira_security_pressure': -.25,
    'ENG_ira_peace_progress': -.5, 'ENG_ira_intelligence_penetration': -.25,
    'ENG_ira_loyalist_tension': .25,
}
REMOVED = {
    'ENG_1985_ira_mechanic', 'ENG_1985_ira_foreign_support',
    'ENG_1985_ira_apply_state_modifier', 'ENG_1985_ira_monthly_update',
    'ENG_ira_troubles_state_modifier', 'ENG_ira_static_modifier',
    'ENG_deploy_extra_police_presence',
    'LBA_1970_ship_arms_to_ira', 'LBA_1985_ship_arms_to_ira',
    'LBA_1985_fund_ira_networks', 'LBA_1985_intelligence_to_ira',
    'LBA_1985_scale_back_ira_support',
}
DEDICATED = [
    'common/scripted_guis/ENG_1985_ira_foreign_support_gui.txt',
    'common/scripted_guis/ENG_1985_ira_gui.txt',
    'common/scripted_localisation/ENG_1985_ira_scripted_localisation.txt',
    'common/decisions/ENG_1985_ira_counter_decisions.txt',
    'common/scripted_effects/mdcw_1970_consumed_ira_clamp.txt',
    'interface/ENG_1985_ira_gui.gui', 'interface/ENG_1985_ira_state_actions.gui',
    'events/ENG_1985_Troubles.txt',
    'localisation/english/ENG_1985_ira_foreign_support_l_english.yml',
]


def translated(rows, initialising=False):
    result=[]
    for k,op,v in rows:
        if k=='_bare' and v=='ENG_ulster_flashpoint':continue
        if k in ('add_ideas','remove_ideas') and v=='ENG_ulster_flashpoint':continue
        if k=='has_idea' and v=='ENG_ulster_flashpoint':
            result.append(('COLDWAR_COL_ira_active','=','yes'));continue
        if k=='ENG_ulster_flashpoint' and isinstance(v,list):
            result.append((k,op,[('allowed','=',[('always','=','no')]),('modifier','=',[])]));continue
        if k=='custom_effect_tooltip' and v=='ENG_1985_setup_ira_mechanic_tt':
            result.append((k,op,'COLDWAR_COL_british_domestic_setup_tt'));continue
        if k in ('ENG_1985_ira_apply_state_modifier','ENG_1985_ira_monthly_update'):
            continue
        if k=='ENG_1985_ira_clamp_values':
            result.append(('17','=',[('clamp_variable','=',[('var','=','COLDWAR_COL_cells'),('min','=','25'),('max','=','90')]),('COLDWAR_COL_apply_domestic','=','yes')]))
            continue
        if k=='country_event' and isinstance(v,list) and str(first(v,'id','')).startswith('eng_troubles.'):
            continue
        if k in ('add_dynamic_modifier','remove_dynamic_modifier','has_dynamic_modifier') and isinstance(v,list) and first(v,'modifier') in ('ENG_ira_troubles_state_modifier','ENG_ira_static_modifier'):
            if k=='has_dynamic_modifier': result.append(('COLDWAR_COL_domestic_contact','=','yes'))
            continue
        if k in ('set_country_flag','clr_country_flag','has_country_flag'):
            flag=first(v,'flag') if isinstance(v,list) else v
            if flag=='ENG_1985_ira_mechanic_active':
                if k=='has_country_flag':result.append(('COLDWAR_COL_ira_active','=','yes'))
                continue
            if flag=='ENG_1985_ira_mechanic_resolved':
                result.append((k,op,'COLDWAR_COL_ira_settlement'));continue
            if str(flag).startswith(('ENG_1985_ira_state_initialised','ENG_1985_ira_startup_grace')):continue
        if k in ('set_variable','add_to_variable','subtract_from_variable','multiply_variable','clamp_variable','check_variable') and isinstance(v,list):
            var=first(v,'var') or (v[0][0] if v else '')
            if var in OLD:
                if initialising or k in ('set_variable','multiply_variable','clamp_variable'):continue
                if k=='check_variable':
                    inner=[('var','=','COLDWAR_COL_cells') if key=='var' else ('COLDWAR_COL_cells',o,value) if key==var else (key,o,value) for key,o,value in v]
                    result.append(('17','=',[(k,op,inner)]));continue
                try:
                    value=float(v[0][2])*OLD[var]*(-1 if k=='subtract_from_variable' else 1)
                except ValueError:
                    continue
                result.append(('17','=',[('add_to_variable','=',[('COLDWAR_COL_cells','=',f'{value:.5f}'.rstrip('0').rstrip('.') or '0')])]))
                continue
        if isinstance(v,list):v=translated(v,initialising)
        if k=='ENG_1985_setup_ira_mechanic':k='COLDWAR_COL_setup_british_domestic_systems'
        result.append((k,op,v))
    return result


def spans(text):
    """Return real brace blocks, ignoring braces in comments/quoted strings."""
    tokens=list(re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[^\s{}=#]+|=',text))
    stack=[];out=[]
    for i,t in enumerate(tokens):
        if t[0]=='{':
            key=tokens[i-2][0] if i>1 and tokens[i-1][0]=='=' else ''
            start=tokens[i-2].start() if key else t.start()
            stack.append((key,start,len(stack)))
        elif t[0]=='}':
            key,start,depth=stack.pop();out.append((key,start,t.end(),depth))
    return out


def run(root=ROOT):
    archive=root/'tools/colonial_affairs/retired_ira'
    changed=[]
    def backup(path):
        target=archive/path.relative_to(root)
        if not target.exists():target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes())
    for rel in DEDICATED:
        path=root/rel
        if path.exists():backup(path);path.unlink();changed.append(rel)
    paths=[p for folder in ('common','events') for p in (root/folder).rglob('*.txt') if 'COLDWAR_colonial' not in p.name]
    for path in paths:
        original=path.read_bytes();text=original.decode('utf-8-sig')
        if not re.search(r'ENG_ulster_flashpoint|ENG_ira_|ENG_1985_(?:ira_|setup_ira)|LBA_(?:cultivate_ira_channels|ship_semtex_to_belfast)|LBA_(?:1970|1985)_(?:ship_arms_to_ira|fund_ira_networks|intelligence_to_ira|scale_back_ira_support)',text):continue
        candidates=[]
        for key,start,end,depth in spans(text):
            if path.parent.name=='national_focus':unit=key=='focus'
            elif path.parent.name=='decisions':unit=depth==1
            elif path.parent.name=='categories':unit=depth==0
            elif path.parent.name=='ideas':unit=key=='ENG_ulster_flashpoint'
            else:unit=depth==0
            if not unit:continue
            body=text[start:end]
            if not re.search(r'ENG_ulster_flashpoint|ENG_ira_|ENG_1985_(?:ira_|setup_ira)|LBA_(?:cultivate_ira_channels|ship_semtex_to_belfast)|LBA_(?:1970|1985)_(?:ship_arms_to_ira|fund_ira_networks|intelligence_to_ira|scale_back_ira_support)',body):continue
            old_libya_focus=key=='focus' and first(parse(body)[0][2],'id') in ('LBA_cultivate_ira_channels','LBA_ship_semtex_to_belfast')
            if key in REMOVED or old_libya_focus:replacement=''
            else:
                ast=parse(body)
                replacement=emit(translated(ast,initialising=key=='ENG_1985_setup_ira_mechanic'))
                if replacement==emit(ast):continue
            candidates.append((start,end,'# IMPERIA CW — Cold War: old IRA simulation replaced by the shared regional case.\n'+replacement))
        if not candidates:continue
        backup(path)
        for start,end,replacement in sorted(candidates,reverse=True):text=text[:start]+replacement+text[end:]
        path.write_bytes((text.rstrip()+'\n').encode('utf-8'));changed.append(path.relative_to(root).as_posix())
    return changed


if __name__=='__main__':
    print('\n'.join(run()))
