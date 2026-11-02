# IMPERIA COLD WAR — Lukashenko eligibility across native Belarus providers.
from pathlib import Path
import sys,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from superpower_1970_leaders.integration import body_patch,format_block
from superpower_1970_leaders.build import b,iff
P='COLDWAR_LUKASHENKO_'
HEADER='# IMPERIA COLD WAR — Lukashenko date gate and portrait integration.\n'

def wrap(text,name,test,effect):
    marker='# COLDWAR LUKASHENKO '+name
    if marker in text:return text
    return body_patch(text,name,lambda body:marker+'\n'+iff(test,effect,body.strip()))

def adapt(relative,text):
    relative=str(relative).replace('\\','/');original=text
    if relative=='common/scripted_effects/00_leader_setup_scripted_effects.txt' and '# COLDWAR LUKASHENKO EARLY ROUTE' not in text:
        anchor='# COLDWAR EU EARLY ROUTE\n\tif = {'
        assert anchor in text,'German dispatcher anchor changed'
        route='# COLDWAR LUKASHENKO EARLY ROUTE\n'+iff(P+'BLR_supported = yes',P+'BLR_set_leader = yes')+'\n\t# COLDWAR EU EARLY ROUTE\n\telse_if = {'
        text=text.replace(anchor,route,1)
    if relative=='common/scripted_effects/BLR_political_leaders.txt':
        text=wrap(text,'set_leader_BLR',P+'BLR_supported = yes',P+'BLR_set_leader = yes')
    if relative=='common/scripted_effects/mdcw_historical_native_pools.txt':
        text=wrap(text,'MDCW_HP_native_pool_BLR_6','original_tag = BLR\nIMP_is_1970_scenario = yes\nNOT = { '+P+'ready = yes }',P+'BLR_early_fallback = yes')
        # Reapply the remembered appearance after a legacy appointment, without recreating it.
        from historical_politics_1970.special_successors import _assignment_blocks,_one_string
        for start,o,end in reversed(list(_assignment_blocks(text,'create_country_leader'))):
            block=text[start:end]
            if _one_string(block,'name')!='Alexander Lukashenko':continue
            call=P+'apply_portrait = yes'
            if not text[end:].lstrip().startswith('hidden_effect = { '+call+' }'):text=text[:end]+'\nhidden_effect = { '+call+' }'+text[end:]
    if '# COLDWAR LUKASHENKO ' in text and '# IMPERIA COLD WAR — Lukashenko date gate and portrait integration.' not in text:
        text=text.replace('# COLDWAR LUKASHENKO ',HEADER+'# COLDWAR LUKASHENKO ',1)
    if text!=original:
        if not text.startswith('# IMPERIA COLD WAR — '):text=HEADER+text
        # Retain upstream text; mark the actual additions in the containers above.
    return text

def install(write):
    for relative in ('common/scripted_effects/00_leader_setup_scripted_effects.txt','common/scripted_effects/BLR_political_leaders.txt','common/scripted_effects/mdcw_historical_native_pools.txt'):
        path=ROOT/relative;old=path.read_text(encoding='utf-8-sig');write(relative,adapt(relative,old))
    relative='tools/historical_politics_1970/build.py';path=ROOT/relative;text=path.read_text(encoding='utf8')
    if 'import adapt as lukashenko_leadership' not in text:
        anchor='        text = superpower_leadership(path, text)';assert anchor in text
        text=text.replace(anchor,anchor+'\n        from lukashenko_1970.integration import adapt as lukashenko_leadership\n        text = lukashenko_leadership(path, text)',1)
    write(relative,text)
