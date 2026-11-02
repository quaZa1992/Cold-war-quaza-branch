# IMPERIA CW — Cold War: researched hardware, flight qualification and native satellites.
import re
from pathlib import Path

# COLDWAR 2025-cut: MD research tiers from 2025 on are removed (OLV/GNSS/COMSAT/SPYSAT 7-12, KILLSAT 5-10).
FAMILIES={'OLV':6,'GNSS':6,'COMSAT':6,'SPYSAT':6,'KILLSAT':4}
PARTNER={'ariel-science','aryabhata','isis-science','anik-communications','san-marco','sirio','azur-science','symphonie','ans-astronomy','interkosmos-instruments','mkf6-imaging','interkosmos-cosmonaut','intersputnik-terminal'}
# Ground acceptance needs no orbital launcher. The first purchased launch is
# financed inside its own partnership campaign, without a domestic OLV receipt.
SUBORBITAL={'foreign-launch-partnership'}
LAUNCH_TIERS={'modular-station':2,'reusable-shuttle':2,'energia-buran':3,'orbital-depot':2,'lunar-orbit-station':2,'lunar-outpost':2,'se-l2-observatory':2,'grand-tour':2,'deep-space-habitat':2,'mars-heavy-edl':2,'mars-sample-return':2,'mars-crewed-landing':3}
PAYLOADS={'meo-navigation':'GNSS','geo-comsat':'COMSAT','heo-comsat':'COMSAT','reconnaissance':'SPYSAT','almaz':'SPYSAT','anik-communications':'COMSAT','sirio':'COMSAT','symphonie':'COMSAT','intersputnik-terminal':'COMSAT','mkf6-imaging':'SPYSAT'}
# A completed pilot campaign commissions one physical satellite, not a constellation.
PILOTS={'meo-navigation':'GNSS','geo-comsat':'COMSAT','heo-comsat':'COMSAT','reconnaissance':'SPYSAT','anik-communications':'COMSAT','sirio':'COMSAT','symphonie':'COMSAT'}
BASES={'GNSS':120,'COMSAT':140,'SPYSAT':160}
HISTORICAL_TECH={'USA':('OLV1','GNSS1','COMSAT1','SPYSAT1'),'SOV':('OLV1','GNSS1','COMSAT1','SPYSAT1'),'FRA':('OLV1',),'ENG':('COMSAT1',)}


def rules(p):
    minimum=0 if p['id'] in SUBORBITAL or p.get('commissioningOnly') else LAUNCH_TIERS.get(p['id'],1)
    return minimum,PAYLOADS.get(p['id']),p['id'] in PARTNER


def tech(family,minimum=1):
    return 'OR = { '+' '.join(f'has_tech = {family}{i}' for i in range(minimum,FAMILIES[family]+1))+' }'


# IMPERIA COLD WAR — Foreign carriage requires a named, qualified human provider.
def provider_name(p):
    return 'cw_sr_provider_'+p['id'].replace('-','_')


def requirement_parts(p):
    minimum,payload,partner=rules(p);parts=[]
    if p['id']=='foreign-launch-partnership':parts.append(('Signed and qualified foreign launch provider',provider_name(p)+' = yes'))
    if minimum:
        launch=tech('OLV',minimum)
        if partner:launch='OR = { '+launch+' '+provider_name(p)+' = yes }'
        parts.append((f'OLV {1965+(minimum-1)*10} or later'+(' OR signed qualified launch provider' if partner else ''),launch))
    if payload:parts.append((payload+' 1965 or later',tech(payload)))
    return parts


def requirement(p):
    return ' '.join(condition for label,condition in requirement_parts(p)) or 'always = yes'


def description(p):
    minimum,payload,partner=rules(p);items=[]
    if minimum:items.append(f'OLV {1965+(minimum-1)*10}'+(' or a signed qualified launch provider' if partner else ''))
    if payload:items.append(payload+' 1965')
    return ', '.join(items) or ('Signed, funded and qualified foreign launch provider required' if p['id']=='foreign-launch-partnership' else 'Ground acceptance; no orbital-launch research required')


def build(c):
    sv,av,cv,block_if,effect,write,guard=(c[k] for k in ['sv','av','cv','block_if','effect','write','guard'])
    triggers='';effects=''
    for family,count in FAMILIES.items():
        body=sv('cw_sr_tech_'+family,0)
        for tier in range(1,count+1):body+=block_if(f'has_tech = {family}{tier}',sv('cw_sr_tech_'+family,tier))
        effects+=effect('cw_sr_scan_'+family,body)
    historical=''
    for tag,entries in HISTORICAL_TECH.items():
        historical+=block_if('original_tag = '+tag,''.join(block_if('NOT = { has_tech = '+item+' }','set_technology = { '+item+' = 1 popup = no }\n') for item in entries))
    scan=block_if('NOT = { has_country_flag = cw_sr_hardware_history }',historical+'set_country_flag = cw_sr_hardware_history\n')+''.join('cw_sr_scan_'+f+' = yes\n' for f in FAMILIES)
    scan+=sv('var_GNSS_civ_local_resources_factor',0)+sv('var_GNSS_civ_local_resources_factor_base',0)
    effects+=effect('cw_sr_technology_refresh',block_if(guard(),scan))
    for n,p in enumerate(c['PROGRAMMES'],1):
        triggers+=effect(f'cw_sr_p{n}_technology',requirement(p))
        minimum,payload,partner=rules(p)
        body=sv(f'cw_sr_p{n}_mod_technology_l',0)+sv(f'cw_sr_p{n}_mod_technology_o',0)
        if minimum:
            # IMPERIA COLD WAR — Borrowed launch research remains with the provider.
            generation=f'cw_sr_p{n}_launch_generation'
            body+=sv(generation,'cw_sr_tech_OLV')
            if partner:
                scan=''.join(block_if(f'has_tech = OLV{tier}',sv('PREV.'+generation,tier)) for tier in range(1,FAMILIES['OLV']+1))  # COLDWAR 2025-cut: follow the remaining OLV tiers
                body+=block_if(provider_name(p)+' = yes',f'var:cw_sr_p{n}_op_country = {{\n'+scan+'}\n')
            body+=sv(f'cw_sr_p{n}_mod_technology_l',generation)+av(f'cw_sr_p{n}_mod_technology_l',-minimum)+f'multiply_variable = {{ cw_sr_p{n}_mod_technology_l = 0.5 }}\n'+c['clamp'](f'cw_sr_p{n}_mod_technology_l',0,2)
        if payload:
            body+=sv(f'cw_sr_p{n}_mod_technology_o','cw_sr_tech_'+payload)+av(f'cw_sr_p{n}_mod_technology_o',-1)+f'multiply_variable = {{ cw_sr_p{n}_mod_technology_o = 0.5 }}\n'+c['clamp'](f'cw_sr_p{n}_mod_technology_o',0,2)
        if p['id'] in PILOTS:
            family=PILOTS[p['id']];body+=sv(f'cw_sr_p{n}_native_model','cw_sr_tech_'+family)+av(f'cw_sr_p{n}_native_model',BASES[family])
        effects+=effect(f'cw_sr_p{n}_technology_odds',body)
        if p['id'] in PILOTS:
            # The donor API owns orbit limits, older-model replacement, ownership,
            # target references and family totals. Preserve the player's launch queue.
            # IMPERIA COLD WAR — Accept native delivery only after the target-model count rises.
            native_family={'GNSS':'GNSS','COMSAT':'COM','SPYSAT':'SPY'}[PILOTS[p['id']]]
            index=f'cw_sr_p{n}_native_index';before=f'cw_sr_p{n}_native_before';counter=f'{native_family}_satellite_array^{index}'
            pilot=sv(index,f'cw_sr_p{n}_native_model')+av(index,-BASES[PILOTS[p['id']]]-1)+sv(before,counter)
            pilot+='clear_array = cw_sr_saved_payload\nfor_each_loop = { array = payload_array value = cw_sr_saved_item add_to_array = { cw_sr_saved_payload = cw_sr_saved_item } }\n'
            pilot+=sv('cw_sr_saved_orbit','var_orbit')+'clear_array = payload_array\n'+f'add_to_array = {{ payload_array = cw_sr_p{n}_native_model }}\nadd_satellite_from_payload = yes\nclear_array = payload_array\nfor_each_loop = {{ array = cw_sr_saved_payload value = cw_sr_restore_item add_to_array = {{ payload_array = cw_sr_restore_item }} }}\nclear_array = cw_sr_saved_payload\n'+sv('var_orbit','cw_sr_saved_orbit')+block_if(cv(counter,'>',before),f'set_country_flag = cw_sr_p{n}_native_commissioned\n')
            condition=guard()+f' NOT = {{ has_country_flag = cw_sr_p{n}_native_commissioned }} '+cv(f'cw_sr_p{n}_native_model','>',BASES[PILOTS[p['id']]])+' '+cv(f'cw_sr_p{n}_native_model','<=',BASES[PILOTS[p['id']]]+12)
            effects+=effect(f'cw_sr_p{n}_native_pilot',block_if(condition,pilot))
    write('common/scripted_triggers/COLDWAR_space_race_technology.txt',triggers)
    write('common/scripted_effects/COLDWAR_space_race_technology.txt',effects)


def apply_shared():
    from integrate import ROOT,save,span
    mark='# IMPERIA CW — Cold War: integrated space research without satellite resource production.'
    changed=[]
    path='common/scripted_triggers/00_special_projects_triggers.txt';source=(ROOT/path).read_text(encoding='utf-8-sig')
    for name,legacy,condition,tooltip in [
        ('has_completed_space_program','sp_space_program','has_country_flag = cw_sr_cap_space_administration','cw_sr_research_access_tt'),
        ('has_completed_space_weapons','sp_space_weapons','has_country_flag = cw_sr_cap_orbital_reconnaissance '+tech('OLV',2),'cw_sr_weapons_access_tt')]:
        begin,end,brace=span(source,name)
        modern='AND = { is_ai = no IMP_is_1970_scenario = yes '+condition+' }'
        old='AND = { NOT = { AND = { is_ai = no IMP_is_1970_scenario = yes } } is_special_project_completed = sp:'+legacy+' }'
        # IMPERIA COLD WAR — Retain the quarantine gate when regenerating native access routes.
        code=name+' = {\n# IMPERIA COLD WAR — GC emergency space quarantine.\nhidden_trigger = { NOT = { has_global_flag = cw_sr_emergency_disabled } }\n custom_trigger_tooltip = { tooltip = '+tooltip+' OR = { '+modern+' '+old+' } } }'
        if source[begin:end].strip()!=code:source=source[:begin]+'\n'+mark+'\n'+code+source[end:]
    save(path,source);changed.append(path)
    # Remove the obsolete extraction calculations, including treaty accumulation
    # and the selected-system preview. Keep all adjacent non-resource mechanics.
    path='common/scripted_effects/00_missiles_scripted_effects.txt';source=(ROOT/path).read_text(encoding='utf-8-sig')
    for name in ['calculate_GNSS_civ_gui_vars','add_access_GNSS_civ_vars','GNSS_civ_button_update']:
        begin,end,brace=span(source,name);body=source[begin:end]
        if name=='calculate_GNSS_civ_gui_vars':
            pat=r'set_variable\s*=\s*\{\s*var_GNSS_civ_local_resources_factor_base\s*=\s*\{'
            match=re.search(pat,body)
            if match:
                left=match.start();opening=body.index('{',left);depth=1;i=opening+1
                while depth:
                    if body[i]=='{':depth+=1
                    elif body[i]=='}':depth-=1
                    i+=1
                body=body[:left]+mark+'\n\tset_variable = { var_GNSS_civ_local_resources_factor_base = 0 }'+body[i:]
        else:
            body=re.sub(r'(set_variable\s*=\s*\{\s*var_GNSS_civ_local_resources_factor\s*=\s*)[^{}]+(?=\})',r'\g<1>0 ',body)
            body=re.sub(r'\s*add_to_variable = \{ ROOT\.var_GNSS_civ_local_resources_factor = THIS\.var_GNSS_civ_local_resources_factor_base \}', '\n\t\t\t\t'+mark,body)
            body=re.sub(r'\s*clamp_variable = \{ var = ROOT\.var_GNSS_civ_local_resources_factor max = global\.GNSS_civ_local_resources_factor_max_array\^temp_GNSS_civ_access_system_highest_idx \}', '\n\t\t\t'+mark,body)
            if mark not in body:body=body[:body.index('{')+1]+'\n\t'+mark+body[body.index('{')+1:]
        source=source[:begin]+body+source[end:]
    save(path,source);changed.append(path)
    path='common/scripted_effects/00_missiles_models.txt';source=(ROOT/path).read_text(encoding='utf-8-sig')
    source=re.sub(r'(?m)^(\s*)add_to_array = \{ global\.GNSS_civ_local_resources_factor_(min|max)_array = [\d.]+ \}',lambda m:m[1]+mark+'\n'+m[1]+'add_to_array = { global.GNSS_civ_local_resources_factor_'+m[2]+'_array = 0 }',source) if mark not in source else source
    save(path,source);changed.append(path)
    path='localisation/english/MD_missiles_l_english.yml';source=(ROOT/path).read_text(encoding='utf-8-sig')
    for key in ['SPACE_AUTO_NET_GNSS_TT','GNSS_CIV_STATS_TT_DELAYED','GNSS_CIV_EFFECTS_TEXT','GNSS_CIV_EFFECTS_MIN','GNSS_CIV_EFFECTS_MAX']:
        match=re.search(r'(?m)^ '+key+r':[^\n]*',source);assert match,key
        line=match[0].replace('construction speed and resource extraction','construction and infrastructure speed').replace('\\nResource Gain Efficiency','').replace('Infrastructure construction speed','Infrastructure speed')
        line=re.sub(r'\\n\[\?global\.GNSS_civ_local_resources_factor_(min|max)_array\^i\|G1%\]','',line)
        if line!=match[0]:source=source[:match.start()]+' '+mark+'\n'+line+source[match.end():]
    target=ROOT/path
    if target.read_text(encoding='utf-8-sig')!=source:
        tmp=target.with_suffix('.yml.cw_sr_tmp');tmp.write_text(source,encoding='utf-8-sig',newline='\n');tmp.replace(target)
    changed.append(path)
    return changed
