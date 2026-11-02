# IMPERIA COLD WAR — Israel V2 scenario bootstrap and legacy isolation.
"""Patch only this country's entry points, retaining native later scenarios."""
from pathlib import Path
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/israel_1970'))
from script_format import read

MARK='# IMPERIA COLD WAR — Israel V2 scenario and legacy integration.\n'


def B(key,body):return key+' = {\n'+body+'\n}'
def IF(guard,body,other=''):
    return B('if',B('limit',guard)+'\n'+body)+('\n'+B('else',other) if other else '')


def bounds(text,start):
    opening=text.index('{',start)
    depth=0
    for match in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',text[opening:]):
        token=match[0]
        if token=='{':depth+=1
        elif token=='}':
            depth-=1
            if not depth:return opening,opening+match.end()
    raise ValueError(('Unclosed native block',text[start:start+80]))


def top_blocks(text):
    pos=0
    while True:
        match=re.search(r'(?m)^([A-Za-z_][\w.]*)\s*=\s*\{',text[pos:])
        if not match:return
        start=pos+match.start()
        opening,end=bounds(text,start)
        yield match[1],start,opening,end
        pos=end


def guarded_legacy(path,names,initialize=False):
    text=(ROOT/path).read_text(encoding='utf-8-sig')
    changes=[]
    for key,start,opening,end in top_blocks(text):
        if key not in names:continue
        body=text[opening+1:end-1].strip()
        # Existing marked wrapper is unwrapped before regeneration, ensuring
        # repeated generation cannot nest another copy around the old body.
        begin='# ISR2 LEGACY BODY BEGIN'
        finish='# ISR2 LEGACY BODY END'
        if begin in body:
            body=body.split(begin,1)[1].split(finish,1)[0].strip()
        legacy=begin+'\n'+body+'\n'+finish
        replacement=(IF('ISR2_replaces_legacy = yes',IF('ISR2_is_scenario = yes',
            'set_global_flag = ISR2_legacy_replaced\nset_country_flag = ISR2_bootstrap_pending'),legacy)
                     if initialize and key=='ISR70_initialize' else IF('NOT = { ISR2_replaces_legacy = yes }',legacy))
        changes.append((opening+1,end-1,'\n'+replacement+'\n'))
    assert len(changes)==len(names),(path,names,len(changes))
    for a,b,new in reversed(changes):text=text[:a]+new+text[b:]
    if not text.startswith(MARK):text=MARK+text
    return text


def category_patch(path):
    text=(ROOT/path).read_text(encoding='utf-8-sig')
    changes=[]
    for key,start,opening,end in top_blocks(text):
        body=text[opening+1:end-1]
        visible=re.search(r'\bvisible\s*=\s*\{',body)
        if not visible:continue
        at=opening+1+visible.end()
        if 'ISR2_replaces_legacy' not in text[at:at+120]:
            changes.append((at,'\n\t\tNOT = { ISR2_replaces_legacy = yes } # ISR2 retires Israel\'s old decision menu\n'))
    for at,new in reversed(changes):text=text[:at]+new+text[at:]
    if not text.startswith(MARK):text=MARK+text
    return text


def party_restrictions_patch(text):
    """Remove excluded party values, never their unrelated array positions."""
    for key,start,opening,end in top_blocks(text):
        if key!='ISR70_restrict_party_slots':continue
        body=text[opening+1:end-1]
        for slot in (8,9,10,11):
            prior='remove_from_array = { gov_coalition_array = '+str(slot)+' }'
            replacement=IF('is_in_array = { array = gov_coalition_array value = '+str(slot)+' }',
                'remove_from_array = { array = gov_coalition_array value = '+str(slot)+' }')
            if prior in body:
                assert body.count(prior)==1
                body=body.replace(prior,replacement)
            else:
                assert replacement in body,('Changed native party-removal anchor',slot)
        return text[:opening+1]+body+text[end-1:]
    raise ValueError('Native Israel party restriction helper is missing')


def legacy_definitions():
    ideas=[];dynamic=[]
    path=ROOT/'common/ideas/ISR70_ideas.txt'
    for key,op,rows in read(path.read_text(encoding='utf-8-sig')):
        if key=='ideas':
            for kind,_,members in rows:
                if kind=='country':ideas += [name for name,_,value in members if isinstance(value,list) and name.startswith('ISR70_')]
    for path in sorted((ROOT/'common/dynamic_modifiers').glob('ISR70*.txt')):
        dynamic += [key for key,_,value in read(path.read_text(encoding='utf-8-sig')) if isinstance(value,list) and key.startswith('ISR70_')]
    return sorted(set(ideas)),sorted(set(dynamic))


def politics_patch(path,parties):
    text=(ROOT/path).read_text(encoding='utf-8-sig')
    changes=[]
    for key,start,opening,end in top_blocks(text):
        if key!='defined_text':continue
        body=text[opening+1:end-1]
        # Only actual native party NAME getters, never descriptions or icons.
        slots=set(int(x) for x in re.findall(r'localization_key\s*=\s*ISR70_party_(\d+)\s*(?=\}|#|\n)',body))
        if len(slots)!=1:continue
        slot=next(iter(slots))
        if slot not in parties:continue
        begin='# ISR2 PARTY NAME BEGIN'
        finish='# ISR2 PARTY NAME END'
        body=re.sub(re.escape(begin)+r'.*?'+re.escape(finish)+r'\s*','',body,flags=re.S)
        first=re.search(r'\btext\s*=\s*\{',body)
        if not first:continue
        new=begin+'\ntext = { trigger = { ISR2_is_scenario = yes } localization_key = ISR2_party_'+str(slot)+' }\n'+finish+'\n'
        body=body[:first.start()]+new+body[first.start():]
        changes.append((opening+1,end-1,body))
    for a,b,new in reversed(changes):text=text[:a]+new+text[b:]
    if not text.startswith(MARK):text=MARK+text
    return text


def integrate(data,modules):
    files={};loc={}
    # Retired, guarded script still refers to the old IDs. Keep those references
    # registered in an unselectable, effect-free compatibility tree. None of
    # these cards belongs to the live217-focus tree or grants old rewards.
    legacy=json.loads((ROOT/'tools/israel_1970/english_design.json').read_text(encoding='utf-8'))
    registry=['id = ISR2_legacy_focus_registry',
        'country = { base = 0 modifier = { add = -1000 always = yes } }','default = no']
    for index,node in enumerate(legacy['nodes']):
        registry.append(B('focus','id = '+node['id']+'\nicon = '+node['icon']+
            f'\nx = {(index%20)*3}\ny = {(index//20)*2}\ncost = 1\navailable = {{ always = no }}\ncompletion_reward = {{ }}'))
    files['common/national_focus/ISR2_legacy_focus_registry.txt']=MARK+B('focus_tree','\n'.join(registry))+'\n'
    ideas,dynamic=legacy_definitions()
    cleanup=[]
    cleanup += [IF('has_idea = '+key,'remove_ideas = '+key) for key in ideas]
    cleanup += [IF('has_dynamic_modifier = { modifier = '+key+' }','remove_dynamic_modifier = { modifier = '+key+' }') for key in dynamic]
    state_cleanup='\n'.join(IF('has_dynamic_modifier = { modifier = '+key+' }','remove_dynamic_modifier = { modifier = '+key+' }') for key in dynamic)
    migration=B('ISR2_retire_legacy_modifiers',IF('NOT = { has_country_flag = ISR2_legacy_retired }',
        '\n'.join(cleanup)+'\n'+B('every_controlled_state',state_cleanup)+'\nset_country_flag = ISR2_legacy_retired'))
    init=IF('NOT = { has_country_flag = ISR2_initialized }',
        IF('has_country_flag = ISR70_initialized','set_country_flag = ISR2_legacy_save')+'\n'+
        IF('NOT = { has_country_flag = ISR2_legacy_save }\ndate < 1970.1.2','set_variable = { election_threshold = 0.01 }')+'\n'+
        'set_country_flag = ISR2_enabled\nISR2_retire_legacy_modifiers = yes\n'+
        IF('NOT = { has_focus_tree = ISR70_focus }','load_focus_tree = ISR70_focus')+'\n'+
        '\n'.join(m['init'] for m in modules)+'\nISR70_restrict_party_slots = yes\nset_variable = { ISR70_leader_slot = ruling_party }\nset_country_flag = ISR2_initialized\nclr_country_flag = ISR2_bootstrap_pending')
    # Civil pressure is first measured raw, then the accepted bilateral relief
    # is reconciled, and only then is the effective Palestinian burden applied.
    refresh='\n'.join(['ISR2_legacy_refund_pending = yes','ISR2_territories_refresh = yes','ISR2_bilateral_reconcile = yes',
        'ISR2_territories_pressure_reconcile = yes','ISR2_domestic_refresh = yes','ISR2_core_refresh = yes'])
    daily='\n'.join(['ISR2_territories_daily = yes','ISR2_bilateral_daily = yes',
        'ISR2_territories_pressure_reconcile = yes','ISR2_domestic_daily = yes','ISR2_core_daily = yes'])
    daily+='\nISR70_restrict_party_slots = yes\n'+IF('NOT = { check_variable = { ISR70_leader_slot = ruling_party } }','ISR70_set_party_leader = yes')
    effects=MARK+migration+'\n\n'+B('ISR2_initialize',IF('ISR2_is_scenario = yes',
        'set_global_flag = ISR2_legacy_replaced\n'+init+'\nISR2_refresh = yes'))
    # History runs before native occupation objects are ready. Its compatibility
    # route records pending retirement only. Startup constructs the module, and
    # early budget/government callbacks cannot enter an unfinished refresh.
    effects+='\n\n'+B('ISR2_refresh',IF('ISR2_is_scenario = yes\nhas_country_flag = ISR2_initialized',refresh))
    effects+='\n\n'+B('ISR2_daily',IF('ISR2_is_scenario = yes',
        IF('NOT = { has_country_flag = ISR2_initialized }','ISR2_initialize = yes')+'\n'+daily))+'\n'
    files['common/scripted_effects/ISR2_integration_effects.txt']=effects
    files['common/scripted_triggers/ISR2_scenario_triggers.txt']=MARK+B('ISR2_is_scenario',
        'tag = ISR\noriginal_tag = ISR\nIMP_is_1970_scenario = yes')+'\n\n'+B('ISR2_replaces_legacy',
        'original_tag = ISR\nIMP_is_1970_scenario = yes')+'\n'
    files['common/on_actions/ISR2_on_actions.txt']=MARK+B('on_actions',
        B('on_startup',B('effect',B('ISR',IF('exists = yes\nISR2_is_scenario = yes','ISR2_initialize = yes'))))+'\n'+
        B('on_daily',B('effect',IF('ISR2_is_scenario = yes','ISR2_daily = yes')))+'\n'+
        B('on_government_change',B('effect',IF('ISR2_is_scenario = yes','ISR2_refresh = yes'))))+'\n'
    for path,names,initialize in [
        ('common/scripted_effects/ISR70_effects.txt',{'ISR70_initialize','ISR70_daily_update','ISR70_refresh_programmes'},True),
        ('common/scripted_effects/ISR70_policy_effects.txt',{'ISR70_policy_daily'},False)]:
        files[path]=guarded_legacy(path,names,initialize)
        if path.endswith('/ISR70_effects.txt'):
            files[path]=party_restrictions_patch(files[path])
    for path in sorted((ROOT/'common/decisions/categories').glob('ISR70*.txt')):
        files[path.relative_to(ROOT).as_posix()]=category_patch(path.relative_to(ROOT).as_posix())
    parties={g['party_slot']:g['gate'].removesuffix(' is in Power.') for g in data['groups'] if g.get('party_slot') is not None}
    for slot,name in parties.items():loc['ISR2_party_'+str(slot)]=name
    for path in ['common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt',
                 'common/scripted_localisation/IMP_1970_party_name_scripted_localisation.txt']:
        files[path]=politics_patch(path,parties)
    # Preserve the legacy compiler as a public compatibility entry point while
    # preventing a future rebuild from restoring the superseded399-focus tree.
    path='tools/israel_1970/build_content.py'
    text=(ROOT/path).read_text(encoding='utf-8-sig')
    prior='remove_from_array = {{ gov_coalition_array = {i} }}'
    replacement='if = {{ limit = {{ is_in_array = {{ array = gov_coalition_array value = {i} }} }} remove_from_array = {{ array = gov_coalition_array value = {i} }} }}'
    if prior in text:
        assert text.count(prior)==1
        text=text.replace(prior,replacement)
    else:
        assert replacement in text,'Changed legacy party-removal generator anchor'
    begin='# ISR2 COMPILER ROUTE BEGIN';end='# ISR2 COMPILER ROUTE END'
    text=re.sub(re.escape(begin)+r'.*?'+re.escape(end)+r'\n?','',text,flags=re.S)
    if not text.startswith(MARK):text=MARK+text
    # Insert after any required __future__ imports, before old module imports.
    route=(begin+'\nif __name__ == "__main__":\n'
        '    import runpy as _isr2_runpy\n'
        '    import sys as _isr2_sys\n'
        '    from pathlib import Path as _ISR2_Path\n'
        '    _isr2_sys.argv = [str(_ISR2_Path(__file__).resolve().parents[1] / "israel_v2/compile.py"), "--write"]\n'
        '    _isr2_runpy.run_path(_isr2_sys.argv[0], run_name="__main__")\n'
        '    raise SystemExit(0)\n'+end+'\n')
    # The inspected old emitter has no __future__ import.
    assert 'from __future__ import' not in text
    position=re.match(r'(?:(?:#[^\n]*\n)|(?:[ \t]*\n))*',text).end()
    text=text[:position]+route+text[position:]
    files[path]=text
    return dict(files=files,loc=loc)
