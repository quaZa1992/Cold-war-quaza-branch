# IMPERIA COLD WAR — Chile readable requirements without internal flag labels.
"""Keep technical predicates executable and suppress only their native display."""
from copy import deepcopy

LOGIC={'AND','OR','NOT','hidden_trigger'}
COUNTRY_SCOPES={'CHL','CUB','USA','SOV','JAP','ARG','PRU','BOL','COL','ECU','FRA','ROOT','FROM','PREV','THIS'}

def technical(row):
    key,op,value=row
    if key=='hidden_trigger':return True
    if key in ('date','tag','original_tag','is_dynamic_country'):return True
    if key in ('IMP_is_1970_scenario','COLDWAR_CHL_is_scenario'):return True
    if key in ('has_country_flag','has_global_flag','has_variable') and isinstance(value,str):
        return value.startswith('COLDWAR_CHL_')
    if key=='is_in_array' and isinstance(value,list):
        return any(k=='array' and str(v).startswith('imp_') for k,o,v in value)
    if key in LOGIC|COUNTRY_SCOPES and isinstance(value,list):
        return bool(value) and all(technical(child) for child in value)
    return False

def polish(rows):
    result=[]
    for row in rows:
        key,op,value=row
        if key=='hidden_trigger' or key in ('custom_trigger_tooltip','custom_override_tooltip'):
            result.append(deepcopy(row))
        elif technical(row):result.append(('hidden_trigger','=',[deepcopy(row)]))
        elif isinstance(value,list) and key in LOGIC|COUNTRY_SCOPES:
            result.append((key,op,polish(value)))
        else:result.append(deepcopy(row))
    return result

def polish_file(ast,scripted_triggers=False):
    if scripted_triggers:return [(k,o,polish(v) if isinstance(v,list) else v) for k,o,v in ast]
    def walk(rows):
        out=[]
        for k,o,v in rows:
            if isinstance(v,list):
                v=polish(v) if k in ('available','visible','allowed','trigger') else walk(v)
            out.append((k,o,v))
        return out
    return walk(ast)
