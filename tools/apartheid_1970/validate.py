# IMPERIA COLD WAR — Source-driven apartheid state and diplomacy regression checks.
"""Exercise emitted effects, not a second copy of the implementation logic."""
from pathlib import Path
from decimal import Decimal as D
import copy
import itertools
import importlib.util
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,walk
P='COLDWAR_AP_'
AGRI=P+'commercial_agriculture_productivity'
EXPECTED={
 'political':{'stability_factor':'-.30','bureaucracy_cost_multiplier_modifier':'.25','police_cost_multiplier_modifier':'1','expected_police_modifier':'3'},
 'services':{'social_cost_multiplier_modifier':'-.50','health_cost_multiplier_modifier':'-.75','education_cost_multiplier_modifier':'-.75','expected_welfare_modifier':'3','expected_healthcare_modifier':'3','expected_education_modifier':'3'},
 'labour':{'receiving_investment_cost_modifier':'-.20','production_speed_buildings_factor':'.10','offices_worker_requirement_modifier':'.10',AGRI:'.25'},
 'military':{'personnel_cost_multiplier_modifier':'.50','expected_mil_modifier':'3'},
 'population':{'migration_rate_value_factor':'.25','monthly_population':'.50'},
}


class Country:
    def __init__(self,tag,continent='africa',subject=None):
        self.tag=tag;self.continent=continent;self.subject=subject;self.alive=True
        self.variables={};self.flags=set();self.modifiers=set();self.opinions={};self.wars=set()


class Engine:
    """Small effect interpreter for this feature's source/model checks only."""
    def __init__(self,countries,scenario=True):
        self.countries={c.tag:c for c in countries};self.global_flags=set();self.scenario=scenario
        self.effects=dict((k,v) for k,o,v in parse((ROOT/'common/scripted_effects/COLDWAR_AP_1970.txt').read_text(encoding='utf-8')))
        self.triggers=dict((k,v) for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_AP_1970.txt').read_text(encoding='utf-8')))
        self.definitions=first(parse((ROOT/'common/opinion_modifiers/COLDWAR_AP_1970.txt').read_text(encoding='utf-8')),'opinion_modifiers')
        self.opinion_values={k:D(first(v,'value')) for k,o,v in self.definitions}
        self.calls=[]

    def ref(self,text,current,previous,root,source):
        if text in ('THIS','ROOT','PREV','FROM'):return {'THIS':current,'ROOT':root,'PREV':previous,'FROM':source}[text]
        return self.countries.get(text)

    def value(self,text,current):
        try:return D(text)
        except Exception:
            if '.' in text:
                tag,var=text.split('.',1);return self.countries[tag].variables.get(var,D(0))
            return current.variables.get(text,D(0))

    def condition(self,rows,current,previous=None,root=None,source=None):
        root=root or current
        result=[]
        for key,op,value in rows:
            if key in ('AND','hidden_trigger'):answer=self.condition(value,current,previous,root,source)
            elif key=='OR':answer=any(self.condition([row],current,previous,root,source) for row in value)
            elif key=='NOT':answer=not self.condition(value,current,previous,root,source)
            elif key=='always':answer=value=='yes'
            elif key=='IMP_is_1970_scenario':answer=self.scenario
            elif key in self.triggers:answer=self.condition(self.triggers[key],current,previous,root,source)
            elif key=='check_variable':
                name,cmp,wanted=value[0];left=self.value(name,current);right=self.value(wanted,current)
                answer={'=':left==right,'>':left>right,'<':left<right,'>=':left>=right,'<=':left<=right}[cmp]
            elif key=='tag':
                other=self.ref(value,current,previous,root,source);answer=current.tag==(other.tag if other else value)
            elif key=='has_country_flag':answer=value in current.flags
            elif key=='has_global_flag':answer=value in self.global_flags
            elif key=='country_exists':answer=value in self.countries and self.countries[value].alive
            elif key=='exists':answer=current.alive==(value=='yes')
            elif key=='is_subject_of':answer=current.subject==value
            elif key=='is_subject':answer=(current.subject is not None)==(value=='yes')
            elif key=='has_war_with':
                other=self.ref(value,current,previous,root,source);answer=other is not None and other.tag in current.wars
            elif key=='capital_scope':answer=self.condition(value,current,previous,root,source)
            elif key=='is_on_continent':answer=current.continent==value
            elif key=='has_dynamic_modifier':answer=first(value,'modifier') in current.modifiers
            elif key=='if':
                answer=not self.condition(first(value,'limit'),current,previous,root,source) or self.condition([r for r in value if r[0]!='limit'],current,previous,root,source)
            elif key in self.countries or key in ('ROOT','THIS','FROM','PREV'):
                other=self.ref(key,current,previous,root,source)
                answer=other is not None and self.condition(value,other,current,root,source)
            else:raise AssertionError('Unmodelled trigger '+key)
            result.append(answer)
        return all(result)

    def execute(self,rows,current,previous=None,root=None,source=None):
        root=root or current
        for key,op,value in rows:
            if key in ('limit','effect_tooltip','unlock_decision_tooltip','custom_effect_tooltip'):continue
            if key=='if':
                if self.condition(first(value,'limit'),current,previous,root,source):self.execute(value,current,previous,root,source)
            elif key=='hidden_effect':self.execute(value,current,previous,root,source)
            elif key in self.effects:self.execute(self.effects[key],current,previous,root,source)
            elif key in ('set_variable','add_to_variable','multiply_variable'):
                name,_,number=value[0];amount=self.value(number,current)
                old=current.variables.get(name,D(0))
                current.variables[name]={'set_variable':amount,'add_to_variable':old+amount,'multiply_variable':old*amount}[key]
            elif key=='clamp_variable':
                name=first(value,'var');current.variables[name]=min(D(first(value,'max')),max(D(first(value,'min')),current.variables.get(name,D(0))))
            elif key=='set_country_flag':current.flags.add(value if isinstance(value,str) else first(value,'flag'))
            elif key=='clr_country_flag':current.flags.discard(value)
            elif key=='set_global_flag':self.global_flags.add(value)
            elif key=='add_dynamic_modifier':current.modifiers.add(first(value,'modifier'))
            elif key=='remove_dynamic_modifier':current.modifiers.discard(first(value,'modifier'))
            elif key in ('force_update_dynamic_modifier','ingame_update_setup'):self.calls.append((current.tag,key))
            elif key=='every_country':
                for other in self.countries.values():
                    if other.alive and self.condition(first(value,'limit',[]),other,current,root,source):self.execute(value,other,current,root,source)
            elif key in ('add_opinion_modifier','remove_opinion_modifier'):
                target=self.ref(first(value,'target'),current,previous,root,source)
                if target:
                    pair=(target.tag,first(value,'modifier'))
                    if key=='add_opinion_modifier':current.opinions[pair]=self.opinion_values[pair[1]]
                    else:current.opinions.pop(pair,None)
            elif key in self.countries or key in ('ROOT','THIS','FROM','PREV'):
                other=self.ref(key,current,previous,root,source)
                if other:self.execute(value,other,current,root,source)
            else:raise AssertionError('Unmodelled effect '+key)

    def run(self,key,tag='SAF',source=None):
        self.execute(self.effects[key],self.countries[tag],source=self.countries.get(source))


def check_vectors():
    c=Country('SAF');c.flags.add(P+'initialized');e=Engine([c]);count=0
    for combination in itertools.product(range(5),repeat=5):
        for domain,tier in zip(EXPECTED,combination):c.variables[P+domain]=D(tier)
        e.run(P+'refresh')
        for domain,tier in zip(EXPECTED,combination):
            for key,base in EXPECTED[domain].items():assert c.variables[P+key]==D(base)*tier/4,(domain,tier,key)
        assert (P+'spirit' in c.modifiers)==(sum(combination)>0)
        snapshot=copy.deepcopy((c.variables,c.modifiers));e.run(P+'refresh')
        assert snapshot==(c.variables,c.modifiers),'Refresh compounds existing contributions'
        count+=1
    return count


def check_diplomacy():
    tags=[Country(t) for t in ('SAF','ZIM','MLW','BOT','LES','SWA','ZAM','AGL','SUD','NAM')]+[Country('POR','europe'),Country('USA','north_america')]
    e=Engine(tags);startup=first(first(parse((ROOT/'common/on_actions/zzzzzzzzz_COLDWAR_AP_1970.txt').read_text(encoding='utf-8')),'on_actions'),'on_startup')
    e.execute(first(startup,'effect'),e.countries['USA'])
    assert P+'initialized' in e.countries['SAF'].flags and P+'initialized' in e.countries['ZIM'].flags
    assert P+'initialized' not in e.countries['NAM'].flags,'Independent Namibia incorrectly receives apartheid'
    for target in ('MLW','BOT','LES','SWA','ZAM','SUD','USA'):
        assert e.countries[target].opinions[('SAF',P+'SAF_world_trade_4')]==-20
    for target in ('MLW','ZIM','SUD','USA'):
        assert not any(k[0]=='SAF' and 'SAF_regional' in k[1] for k in e.countries[target].opinions),target
    for target in ('BOT','LES','SWA'):
        assert e.countries[target].opinions[('SAF',P+'SAF_regional_diplomatic_4')]==-50
        assert ('SAF',P+'SAF_regional_trade_4') not in e.countries[target].opinions
    for target in ('ZAM','AGL'):
        for kind in ('trade','diplomatic'):
            assert e.countries[target].opinions[('SAF',P+'SAF_regional_'+kind+'_4')]==-50
            assert e.countries['SAF'].opinions[(target,P+'SAF_regional_'+kind+'_4')]==-50
    e.countries['AGL'].subject='POR';e.run(P+'relations_SAF')
    assert ('SAF',P+'SAF_regional_trade_4') not in e.countries['AGL'].opinions
    e.countries['AGL'].subject=None;e.run(P+'relations_SAF')
    assert ('SAF',P+'SAF_regional_trade_4') in e.countries['AGL'].opinions
    before=copy.deepcopy([c.opinions for c in e.countries.values()]);e.run(P+'relations_SAF')
    assert before==[c.opinions for c in e.countries.values()],'Opinion refresh stacks copies'
    # Render source-driven decision effects using recipient ROOT, the scope in
    # which a careless ROOT-based diplomatic refresh usually breaks.
    decisions=first(parse((ROOT/'common/decisions/COLDWAR_AP_1970.txt').read_text(encoding='utf-8')),P+'policy_category')
    accept=first(first(decisions,P+'accept_SAF'),'complete_effect')
    saf=e.countries['SAF'];zam=e.countries['ZAM']
    saf.variables[P+'political']=D(2);e.run(P+'refresh');zam.flags.add(P+'pending_SAF')
    e.execute(accept,zam)
    assert P+'normalised_SAF' in zam.flags and P+'pending_SAF' not in zam.flags
    assert not any(k[0]=='SAF' and 'SAF_regional' in k[1] for k in zam.opinions)
    assert ('SAF',P+'SAF_world_trade_2') in zam.opinions
    before=copy.deepcopy((zam.flags,zam.opinions,saf.opinions));e.execute(accept,zam)
    assert before==(zam.flags,zam.opinions,saf.opinions),'Duplicate acceptance changes settlement'
    saf.variables[P+'political']=D(4);e.run(P+'refresh')
    assert zam.opinions[('SAF',P+'SAF_regional_trade_4')]==-50,'Backtracking fails to suspend normalisation'
    saf.variables[P+'political']=D(2);e.run(P+'refresh')
    assert ('SAF',P+'SAF_regional_trade_2') not in zam.opinions
    saf.wars.add('ZAM');zam.wars.add('SAF');e.run(P+'refresh')
    assert zam.opinions[('SAF',P+'SAF_regional_trade_2')]==-25
    saf.wars.clear();zam.wars.clear();e.run(P+'refresh')
    assert ('SAF',P+'SAF_regional_trade_2') not in zam.opinions
    # A dead sender retains variables and flags, but can no longer ratify.
    zam.flags.add(P+'pending_SAF');saf.alive=False
    assert not e.condition(first(first(decisions,P+'accept_SAF'),'available'),zam)
    saf.alive=True;zam.flags.discard(P+'pending_SAF')
    # The feature's persisted state survives a source-model save/rehost cycle.
    before=copy.deepcopy([(c.variables,c.flags,c.opinions,c.modifiers) for c in e.countries.values()])
    restored=Engine(copy.deepcopy(list(e.countries.values())))
    restored.global_flags=copy.deepcopy(e.global_flags);restored.run(P+'refresh')
    assert before==[(c.variables,c.flags,c.opinions,c.modifiers) for c in restored.countries.values()]
    for domain in EXPECTED:saf.variables[P+domain]=D(0)
    e.run(P+'refresh')
    assert not any('SAF_' in key[1] for c in e.countries.values() for key in c.opinions),'Abolition leaves stale opinion tiers'
    return e


def check_transitions():
    c=Country('SAF');e=Engine([c]);e.run(P+'initialize')
    decisions=first(parse((ROOT/'common/decisions/COLDWAR_AP_1970.txt').read_text(encoding='utf-8')),P+'policy_category')
    for domain in EXPECTED:
        row=first(decisions,P+'reduce_'+domain);effect=first(row,'complete_effect')
        for tier in (4,3,2,1):
            c.flags.discard(P+domain+'_cooldown');c.variables[P+domain]=D(tier);e.run(P+'refresh')
            before=dict(c.variables);e.execute(effect,c)
            for key,base in EXPECTED[domain].items():assert c.variables[P+key]-before[P+key]==-D(base)/4
            after=copy.deepcopy(c.variables);e.execute(effect,c)
            assert after==c.variables,'Decision can execute twice during its cooldown'
        c.flags.discard(P+domain+'_cooldown');c.variables[P+domain]=D(0);e.execute(effect,c)
        assert c.variables[P+domain]==0
        restore=first(first(decisions,P+'restore_'+domain),'complete_effect')
        e.execute(restore,c);assert c.variables[P+domain]==1
    assert e.calls[-2][1]=='force_update_dynamic_modifier' and e.calls[-1][1]=='ingame_update_setup'
    modern=Engine([Country('SAF')],scenario=False);modern.run(P+'initialize')
    assert not modern.countries['SAF'].variables,'Feature leaks into another start date'
    nam=Country('NAM',subject='SAF');parent=Country('SAF');release=Engine([parent,nam])
    release.run(P+'initialize');release.run(P+'initialize','NAM');nam.subject=None
    branch=first(first(parse((ROOT/'common/national_focus/COLDWAR_AP_1970_shared.txt').read_text(encoding='utf-8')),'shared_focus'),'allow_branch')
    assert release.condition(branch,nam),'Initialized NAM loses its branch after independence'


def structural():
    manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    paths=manifest['outputs']+['common/scripted_effects/00_money_system.txt','common/national_focus/mdcw_1970_generic_focus.txt']
    parsed={}
    for relative in paths:
        payload=(ROOT/relative).read_bytes()
        if relative.endswith('.yml'):
            assert payload.startswith(b'\xef\xbb\xbfl_english:\n')
            text=payload.decode('utf-8-sig');assert text.splitlines()[1].startswith('# IMPERIA COLD WAR')
            keys=re.findall(r'^ ([^\s:]+):',text,re.M);assert len(keys)==len(set(keys))
            assert '\\\\n' not in text,'Double-escaped localisation newline'
            for line in text.splitlines():
                if line.startswith(' '):assert '\u2013' not in line and '\u2014' not in line
        else:
            assert not payload.startswith(b'\xef\xbb\xbf'),relative
            text=payload.decode('utf-8');assert text.startswith('# IMPERIA COLD WAR'),relative
            parsed[relative]=parse(text)
    tags=set()
    for path in (ROOT/'common/country_tags').glob('*.txt'):
        tags.update(re.findall(r'^\s*([A-Z][A-Z0-9]{2})\s*=',path.read_text(encoding='utf-8-sig'),re.M))
    for relative,tree in parsed.items():
        if 'COLDWAR_AP' not in relative:continue
        for key,op,value in walk(tree):
            if key in ('tag','is_subject_of','country_exists') and isinstance(value,str) and re.fullmatch('[A-Z][A-Z0-9]{2}',value):
                assert value in tags,(relative,'unknown tag',value)
    dm=first(parsed['common/dynamic_modifiers/COLDWAR_AP_1970.txt'],P+'spirit')
    for domain in EXPECTED:
        for key in EXPECTED[domain]:assert first(dm,key)==P+key
    money=(ROOT/'common/scripted_effects/00_money_system.txt').read_text(encoding='utf-8')
    assert money.count('add = modifier@'+AGRI)==2,'Commercial modifier missing or leaking into other sectors'
    focus=parsed['common/national_focus/COLDWAR_AP_1970_shared.txt']
    assert sum(k=='shared_focus' for k,o,v in focus)==5
    category=first(parsed['common/decisions/categories/COLDWAR_AP_1970.txt'],P+'policy_category')
    assert first(category,'icon') in (ROOT/'interface/MD_decisions.gfx').read_text(encoding='utf-8-sig')
    for key,op,value in walk(parsed['common/decisions/COLDWAR_AP_1970.txt']):
        if key=='effect_tooltip':assert not any(k=='hidden_effect' for k,o,v in walk(value))
    spec=importlib.util.spec_from_file_location('apartheid_compiler',HERE/'compile.py')
    compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    assert compiler.patch_money(money)==money
    generic=(ROOT/'common/national_focus/mdcw_1970_generic_focus.txt').read_text(encoding='utf-8')
    assert compiler.patch_generic(generic)==generic
    # The generic's canonical generator preserves the loaded header, which
    # contains this attachment, rather than rebuilding an unrelated header.
    owner=(ROOT/'Claude outputs/COLDWAR_GEN_generator/gen_focus.py').read_text(encoding='utf-8')
    assert "header_text(loaded['header'])" in owner
    return len(paths)


if __name__=='__main__':
    files=structural();vectors=check_vectors();check_transitions();check_diplomacy()
    report={'project':'IMPERIA COLD WAR','parsed_files':files,'policy_vectors':vectors,'checks':['exact user base and all 3125 tier combinations','idempotent refresh and zero-state removal','decision replay guards and reversals','1970-only initialization','literal worldwide and mirrored regional opinions','Malawi and SACU exceptions','colonial status changes','recipient-root acceptance and duplicate delivery','rollback and war suspension','abolition cleanup','UTF-8/BOM and localisation escapes','idempotent integration patches'],'evidence':'Source/parser and effect-model checks. No native engine or multiplayer run.'}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
