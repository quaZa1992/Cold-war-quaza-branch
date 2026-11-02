# IMPERIA COLD WAR — Independent installed Air Command content verification.
from collections import defaultdict,Counter
from decimal import Decimal
from pathlib import Path
import json,re,sys,hashlib
import build
from PIL import Image

ROOT,HERE=build.ROOT,build.HERE
D=Decimal
META=build.META|{'instant'}

def flat(rows,prefix=''):
    result=defaultdict(D)
    for key,_,value in rows:
        if key in META: continue
        path=prefix+key
        if isinstance(value,list):
            for k,v in flat(value,path+'.').items(): result[k]+=v
        else:
            try: result[path]+=D(str(value))
            except Exception: pass
    return dict(result)

def total(body):
    values=defaultdict(D,flat(body))
    for _,_,stage in build.get(body,'rewards',build.get(body,'milestones',[])):
        for key,value in flat(stage).items(): values[key]+=value
    return dict(values)

def font(name):
    path=next(p for p in [ROOT/'gfx/fonts'/f'{name}.fnt',Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/gfx/fonts')/f'{name}.fnt'] if p.is_file())
    text=path.read_text(encoding='utf-8-sig')
    return {int(c):int(w) for c,w in re.findall(r'^char id=(\d+).*?xadvance=(-?\d+)',text,re.M)},int(re.search(r'^common lineHeight=(\d+)',text,re.M)[1])

def wrap(text,adv,width):
    lines=['']
    for word in text.split():
        new=(lines[-1]+' '+word).strip()
        if sum(adv.get(ord(c),9) for c in new)>width and lines[-1]: lines.append(word)
        else: lines[-1]=new
    return lines

def main():
    checks=[]
    def check(name,good,detail=None): checks.append(dict(name=name,passed=bool(good),detail=detail))
    approved=json.loads((ROOT/'tools/air_doctrine_design_1970/concept_values.json').read_text(encoding='utf-8'))
    installed={}; kinds={}
    for path in [build.OLD_GRAND,build.NEW_GRAND,build.OLD_SUB,build.NEW_SUB]:
        raw=(ROOT/path).read_bytes(); source=raw.decode('utf-8-sig')
        check('encoding:'+path,not raw.startswith(b'\xef\xbb\xbf'))
        check('marker:'+path,source.startswith(build.MARKER))
        for ident,_,body in build.parse(source):
            check('unique_id:'+ident,ident not in installed)
            installed[ident]=body; kinds[ident]='grand' if build.get(body,'folder') else build.get(body,'track')
    check('inventory_count',len(installed)==64)
    for item in [*approved['existing_inventory'],*approved['new_concepts']]:
        ident=item['id']; body=installed[ident]
        expected={k:D(str(v)) for k,v in item.get('draft_final',item['final']).items() if k!='tech_air_damage_factor' and D(str(v))!=0}
        # Native role coverage adapters explicitly required by the approved brief.
        for key in list(expected):
            if key.startswith('category_fighter.'):
                value=expected.pop(key)
                for role in build.FIGHTERS: expected[key.replace('category_fighter',role)]=value
        if ident in {'air_battlefield_support','integrated_air_warfare','cas_aircraft_operations'}:
            for key,value in list(expected.items()):
                if key.startswith('category_CAS.'): expected[key.replace('category_CAS.','gunship.')]=value
        if ident=='wvr_dogfighting_doctrine':
            for role in build.FIGHTERS: expected[role+'.maximum_speed']=expected['category_light_fighter.maximum_speed']
        if ident=='local_airspace_defense': expected['air_interception_detect_factor']=D('.10')
        # Eight inherited manufacturing ideas were side effects omitted by the
        # proposal's numeric extractor. Preserve them as owned native rewards.
        native_ideas=build.integration_baseline()['native_ideas']
        original=next((b for k,_,b in build.parse(json.loads((HERE/'baseline.json').read_text(encoding='utf-8'))['sources'][build.OLD_SUB]['text']) if k==ident),None)
        if original is not None:
            for _,_,stage in build.get(original,'rewards',[]):
                idea=build.get(build.get(stage,'effect',[]),'add_ideas')
                if idea is None: continue
                for key,_,value in native_ideas[idea]:
                    more=flat([(key,'=',value)]) if key=='equipment_bonus' else flat(value) if key=='modifier' else {}
                    for path,amount in more.items():
                        if idea=='stealth_aircraft_design_hidden_spirit' and path.endswith('.build_cost_ic'): continue
                        expected[path]=expected.get(path,D(0))+amount
        for path in list(expected):
            if path.startswith('category_Strike_fighter.'):
                amount=expected.pop(path)
                for unit in ('light_strike','cv_light_strike'): expected[path.replace('category_Strike_fighter',unit)]=amount
        actual={k:v for k,v in total(body).items() if v!=0}
        check('approved_final:'+ident,actual==expected,{'expected':{k:str(v) for k,v in expected.items()},'actual':{k:str(v) for k,v in actual.items()}} if actual!=expected else None)
        progression=build.get(body,'rewards',build.get(body,'milestones',[]))
        check('progression_count:'+ident,len(progression)==(6 if kinds[ident]=='grand' else 5))
        check('no_empty_rewards:'+ident,all(bool(v) for _,_,v in progression))
        check('no_unowned_reward_effects:'+ident,all(build.get(v,'effect') is None for _,_,v in progression))
        check('cost:'+ident,build.get(body,'xp_type')=='air' and build.get(body,'xp_cost')==('100' if kinds[ident]=='grand' else '75'))
        if kinds[ident]!='grand':
            check('mastery_6:'+ident,build.get(build.get(body,'mastery'),'multiplier')=='6')
            check('self_exclusion:'+ident,('NOT','=',[('has_doctrine','=',ident)]) in build.get(body,'available'))
        penalty_keys=(item.get('activation_deltas') or {k:v for k,v in item['activation'].items() if (float(v)<0 and not any(s in k for s in ['accident','xp_loss','cost','fuel'])) or (float(v)>0 and any(s in k for s in ['personnel_cost','accidents']))})
        penalty_keys=dict(penalty_keys)
        for path in list(penalty_keys):
            if path.startswith('category_Strike_fighter.'):
                amount=penalty_keys.pop(path)
                for unit in ('light_strike','cv_light_strike'): penalty_keys[path.replace('category_Strike_fighter',unit)]=amount
        # Persistent signs are checked against the exact approved penalties at every stage.
        cumulative=defaultdict(D,flat(body)); stage_count=0
        for stage in [None,*[v for _,_,v in progression]]:
            if stage is not None:
                for k,v in flat(stage).items(): cumulative[k]+=v
            surviving=[k for k,v in penalty_keys.items() if cumulative[k]*D(str(v))>0]
            check('persistent_tradeoff:'+ident+':'+str(stage_count),bool(surviving),surviving)
            stage_count+=1
    locpath=ROOT/build.LOC; raw=locpath.read_bytes()
    check('localisation_bom',raw.startswith(b'\xef\xbb\xbf'))
    source=raw.decode('utf-8-sig')
    check('localisation_marker',source.startswith('l_english:\n'+build.MARKER))
    pairs=re.findall(r'^\s*([\w]+):\d+\s+(".*")\s*$',source,re.M)
    loc={k:json.loads(v) for k,v in pairs}
    check('unique_localisation',len(loc)==len(pairs))
    adv,lineheight=font('hoi_20bs')
    for year in (1964,1978):
        label=loc['mdcw_rpv_'+str(year)]
        check('research_label_fit:'+str(year),sum(adv.get(ord(c),9) for c in label)<=166,label)
    check('english_punctuation',all('\u2013' not in v and '\u2014' not in v for v in loc.values()))
    layout={}
    # All new names and all 64 historical main descriptions use real native font advances.
    for ident,body in installed.items():
        fields=['description']+(['name'] if ident.startswith('mdcw_') else [])
        layout[ident]={}
        for field in fields:
            text=loc.get(build.get(body,field)); check('localised:'+ident+':'+field,text is not None)
            if text is None: continue
            width,height,name=(140,50,'hoi_20bs') if field=='name' else (460,80,'hoi_18mbs')
            adv,lineheight=font(name); lines=wrap(text,adv,width)
            detail={'lines':lines,'height':len(lines)*lineheight,'limit':height,'width':width}
            layout[ident][field]=detail
            check('native_text_fit:'+ident+':'+field,len(lines)*lineheight<=height and all(sum(adv.get(ord(c),9) for c in line)<=width for line in lines),detail)
        for key,_,_ in build.get(body,'rewards',[]):
            if ident.startswith('mdcw_'):
                check('reward_loc:'+ident+':'+key,ident+'_'+key in loc and ident+'_'+key+'_desc' in loc)
    gfx=build.parse((ROOT/build.GFX).read_text(encoding='utf-8'))
    sprites={build.get(v,'name').strip('"'):build.get(v,'texturefile').strip('"') for _,_,v in build.get(gfx,'spriteTypes')}
    for item in [*build.GRANDS,*build.SUBS]:
        path=ROOT/sprites[build.get(installed[item['id']],'icon')]
        image=Image.open(path).convert('RGBA')
        check('icon:'+item['id'],image.size==(64,64) and image.getchannel('A').getextrema()==(0,255))
    track=build.parse((ROOT/build.TRACK).read_text(encoding='utf-8'))
    mastery=build.get(build.get(track,'drone_warfare'),'mastery')
    check('uav_mastery_not_transport',build.get(mastery,'equipment') is None and build.get(mastery,'categories')==[('_bare','=','category_Air_UAV')])
    for relative,expected in build.outputs().items():
        check('generator_drift:'+relative,(ROOT/relative).read_bytes()==expected.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8'))
        if not relative.endswith('.yml'):
            check('native_number_format:'+relative,re.search(r'=\s*[+-]?\.\d',expected) is None)
    integration=build.integration_baseline()
    enum=(ROOT/build.ENUM).read_text(encoding='utf-8')
    enum_header='# IMPERIA COLD WAR — Air Command equipment enum integration; native MD entries retained.\n'
    enum_block='\t# IMPERIA COLD WAR — Historical reconnaissance RPV models.\n\tmdcw_recon_rpv_1964_model\n\tmdcw_recon_rpv_1978_model\n'
    check('unrelated_enum_preserved',enum.removeprefix(enum_header).replace(enum_block,'')==integration['script_enums_original'])
    gui=(ROOT/build.GUI).read_text(encoding='utf-8')
    cleaned=re.sub(r'\n\s*# IMPERIA COLD WAR RPV ROW BEGIN\n.*?# IMPERIA COLD WAR RPV ROW END\n','\n',gui,flags=re.S)
    cleaned=cleaned.removeprefix('# IMPERIA COLD WAR — Historical RPV research rows; native MD GUI retained.\n')
    check('unrelated_gui_semantics_preserved',build.parse(cleaned)==build.parse(integration['research_gui_original']))
    check('native_idea_source_unchanged',hashlib.sha256((ROOT/integration['native_ideas_source']).read_bytes()).hexdigest()==integration['native_ideas_sha256'])
    check('research_grid_registrations',gui.count('name = "mdcw_rpv_1964_tree"')==2 and gui.count('name = "mdcw_rpv_1978_tree"')==2)
    compiled='\n'.join((ROOT/p).read_text(encoding='utf-8') for p in [build.OLD_GRAND,build.OLD_SUB])
    check('no_wrong_static_aa_modifier','tech_air_damage_factor' not in compiled)
    check('no_hidden_idea_grants','add_ideas' not in compiled)
    check('native_enum_models',all(enum.count('\n\tmdcw_recon_rpv_'+str(y)+'_model\n')==1 for y in (1964,1978)))
    units_source=(ROOT/build.UNITS).read_text(encoding='utf-8')
    original_units=build.parse(integration['air_units_original'])
    current_units=build.parse(units_source)
    units=build.get(current_units,'sub_units')
    uavs=[k for k,_,body in units if ('_bare','=','category_Air_UAV') in build.get(body,'categories',[])]
    check('uav_category_complete',set(uavs)=={'drone','cv_drone','kamikaze_drone'},uavs)
    kamikaze=build.get(units,'kamikaze_drone')
    categories=build.get(kamikaze,'categories')
    categories.remove(('_bare','=','category_Air_UAV'))
    check('unrelated_air_units_preserved',current_units==original_units)
    check('fighter_mothership_excluded','category_Strike_fighter' not in compiled and 'category_fighter' not in compiled)
    report={'project':'IMPERIA COLD WAR','checks':checks,'passed':sum(c['passed'] for c in checks),'failed':[c for c in checks if not c['passed']], 'limits':['Static checks do not establish multiplayer balance or native UI rendering.']}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (HERE/'text_layout.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','fields':layout},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'failed':report['failed']},indent=2))
    raise SystemExit(bool(report['failed']))

if __name__=='__main__': main()
