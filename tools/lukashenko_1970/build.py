# IMPERIA COLD WAR — Dated Lukashenko choices and remembered portrait variants.
"""Native selector integration for Belarus and the Soviet Union. No new polling."""
from pathlib import Path
from datetime import date,timedelta
import json,sys,re,uuid,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from superpower_1970_leaders.build import b,iff,IDEO,TRIG,incumbent
P='COLDWAR_LUKASHENKO_'
HEADER='# IMPERIA COLD WAR — Dated Lukashenko selection and portrait wardrobe.\n'
NAME='Alexander Lukashenko'
ALIASES=('Aleksandr Lukashenko','Alyaksandr Lukashenka')
CONFIG=json.loads((HERE/'config.json').read_text(encoding='utf8'))
YOUNG='gfx/leaders/COLDWAR_lukashenko/young.dds'
NINETIES='gfx/leaders/COLDWAR_lukashenko/90s.dds'
MASHEROV='gfx/Leaders/BLR/BLR_Coldwar_Pyotr_Masherov.dds'
FILES=[]

def available_from(value):
    d=date(*map(int,value.split('.')))-timedelta(days=1)
    return f'date > {d.year}.{d.month}.{d.day}'
def context():
    return 'IMP_is_1970_scenario = yes\nexists = yes\nis_dynamic_country = no\nis_ai = no\n'+b('OR','original_tag = SOV\noriginal_tag = BLR')
def leader():return incumbent(dict(name=NAME,aliases=ALIASES))
def blr_context():return 'original_tag = BLR\nexists = yes\nis_dynamic_country = no\nIMP_is_1970_scenario = yes\nis_ai = no'

def write(relative,text,bom=False):
    if not relative.endswith('.json'):
        if relative.endswith('.yml'):
            if not text.startswith('l_english:\n# IMPERIA COLD WAR — '):text=text.replace('l_english:\n','l_english:\n'+HEADER,1)
        elif not text.startswith('# IMPERIA COLD WAR — '):text=HEADER+text
    path=ROOT/relative;path.parent.mkdir(parents=True,exist_ok=True);raw=text.encode('utf-8-sig' if bom else 'utf8')
    old=path.read_bytes() if path.exists() else None
    if old!=raw:
        temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temporary.write_bytes(raw)
        assert (path.read_bytes() if path.exists() else None)==old,relative
        temporary.replace(path)
    FILES.append(relative)

def assets():
    sprites=[];records=[];review=Image.new('RGB',(680,470),'#20272b');draw=ImageDraw.Draw(review)
    for index,(key,path,crop) in enumerate([('young',YOUNG,None),('90s',NINETIES,(.10,.0,.55,.81))]):
        meta=json.loads((HERE/('source_'+key+'.json')).read_text(encoding='utf8'));source=HERE/meta['master'];im=Image.open(source).convert('RGBA')
        if crop:im=im.crop(tuple(round(v*im.size[i%2]) for i,v in enumerate(crop)))
        dest=ROOT/path;dest.parent.mkdir(parents=True,exist_ok=True)
        ImageOps.fit(im,(156,210),method=Image.Resampling.LANCZOS,centering=(.5,.12)).save(dest,format='DDS')
        icon='gfx/interface/decisions/COLDWAR_lukashenko/'+key+'.dds';dest=ROOT/icon;dest.parent.mkdir(parents=True,exist_ok=True)
        ImageOps.fit(Image.open(ROOT/path),(33,30),method=Image.Resampling.LANCZOS,centering=(.5,.12)).save(dest,format='DDS')
        sprites.extend([b('spriteType',f'name = "GFX_{P}{key}_portrait"\ntexturefile = "{path}"'),b('spriteType',f'name = "GFX_{P}{key}_icon"\ntexturefile = "{icon}"')])
        review.paste(Image.open(ROOT/path).convert('RGB').resize((312,420)),(index*340,0));draw.text((index*340+10,435),'Lukashenko '+('Young' if key=='young' else '90s'),fill='white')
        records.append(dict(project='IMPERIA COLD WAR',variant=key,source=meta,path=path,icon=icon,master_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),portrait_sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),technical_crop=crop))
    # Masherov is an existing Belarusian incumbent, not a newly invented fallback.
    assert (ROOT/MASHEROV).exists()
    icon='gfx/interface/decisions/COLDWAR_lukashenko/masherov.dds';dest=ROOT/icon;dest.parent.mkdir(parents=True,exist_ok=True)
    ImageOps.fit(Image.open(ROOT/MASHEROV),(33,30),method=Image.Resampling.LANCZOS,centering=(.5,.12)).save(dest,format='DDS')
    sprites.append(b('spriteType',f'name = "GFX_{P}masherov_icon"\ntexturefile = "{icon}"'))
    write('interface/COLDWAR_lukashenko_1970.gfx',b('spriteTypes','\n\n'.join(sprites))+'\n')
    write('tools/lukashenko_1970/ASSET_MANIFEST.json',json.dumps(dict(project='IMPERIA COLD WAR',portraits=records),ensure_ascii=False,indent=2)+'\n')
    review.save(HERE/'PORTRAIT_REVIEW.png')

def person(name,key):return dict(name=name,key=key,aliases=ALIASES if key=='lukashenko' else ())
def appointment(name,key,slot):
    picture=YOUNG if key=='lukashenko' else MASHEROV
    creation=b('create_country_leader',f'name = "{name}"\npicture = "{picture}"\ndesc = {P}{key}_desc\nideology = {IDEO[slot]}\ntraits = {{ }}')
    return iff('NOT = { '+incumbent(person(name,key))+' }','retire_country_leader = yes\n'+creation)+(('\n'+P+'apply_portrait = yes') if key=='lukashenko' else '')

def wardrobe_decisions(gate,suffix,loc):
    rows=[]
    for key,nineties in [('young',False),('90s',True)]:
        active=P+'ready = yes\n'+(('has_country_flag = '+P+'portrait_90s') if not nineties else 'NOT = { has_country_flag = '+P+'portrait_90s }\n'+P+'portrait_90s_ready = yes')
        decision=P+suffix+'_portrait_'+key
        rows.append(b(decision,f'icon = GFX_{P}{key}_icon\ncost = 0\nfire_only_once = no\ndays_re_enable = 0\n'+b('allowed',b('OR','original_tag = SOV\noriginal_tag = BLR'))+'\n'+b('visible',gate+'\n'+leader())+'\n'+b('available',active)+'\n'+b('complete_effect',P+'set_portrait_'+key+' = yes')+'\nai_will_do = { factor = 0 }'))
        loc[decision]='Lukashenko 90s' if nineties else 'Lukashenko: Young'
        loc[decision+'_desc']='Use the restored 1990s portrait of Alexander Lukashenko.' if nineties else 'Use the restored uniform portrait of the young Alexander Lukashenko.'
    return '\n\n'.join(rows)

def render():
    effects={};triggers={P+'ready':available_from(CONFIG['available_from']),P+'portrait_90s_ready':available_from(CONFIG['portrait_90s_from']),P+'BLR_supported':blr_context()+'\n'+b('OR','check_variable = { ruling_party = 4 }\ncheck_variable = { ruling_party = 6 }')}
    effects[P+'apply_portrait']=iff(context()+'\n'+P+'ready = yes\n'+leader(),iff('has_country_flag = '+P+'portrait_90s\n'+P+'portrait_90s_ready = yes','set_country_leader_portrait = { portrait = GFX_'+P+'90s_portrait }','set_country_leader_portrait = { portrait = GFX_'+P+'young_portrait }'))
    for key in ('young','90s'):
        gate=context()+'\n'+P+'ready = yes\n'+leader()
        if key=='90s':gate+='\n'+P+'portrait_90s_ready = yes'
        effects[P+'set_portrait_'+key]=iff(gate,('set_country_flag' if key=='90s' else 'clr_country_flag')+' = '+P+'portrait_90s\n'+P+'apply_portrait = yes')
    branch=[];observers=[];categories=[];decisions=[];loc={P+'lukashenko_desc':'Belarusian Soviet political organizer and agricultural administrator, later a parliamentary deputy and advocate of state-led economic policy. His appointment to Union leadership is an alternative political outcome.',P+'masherov_desc':'First Secretary of the Communist Party of Byelorussia and a leading figure of the republic\'s Soviet administration.',P+'portrait_young':'Lukashenko: Young',P+'portrait_90s':'Lukashenko 90s',P+'portrait_young_desc':'Use the restored uniform portrait of the young Alexander Lukashenko.',P+'portrait_90s_desc':'Use the restored 1990s portrait of Alexander Lukashenko.'}
    for slot in (4,6):
        party=TRIG[slot]+'_are_in_power = yes';gate=blr_context()+'\n'+party;pref=P+'BLR_preference_'+str(slot);cat=P+'BLR_candidates_'+str(slot)
        choose=[];observe=[]
        for index,(name,key) in enumerate([('Pyotr Masherov','masherov'),(NAME,'lukashenko')],1):
            ready='\n'+P+'ready = yes' if key=='lukashenko' else ''
            active=b('hidden_trigger',blr_context())+'\n'+party+ready+'\nNOT = { '+incumbent(person(name,key))+' }'
            command=P+'BLR_choose_'+str(slot)+'_'+key
            effects[command]=iff(active,f'set_variable = {{ {pref} = {index} }}\n'+appointment(name,key,slot)+'\nset_correct_ideology_trait = yes')
            choose.append(b('if' if not choose else 'else_if',b('limit',f'check_variable = {{ {pref} = {index} }}'+ready)+'\n'+appointment(name,key,slot)))
            observe.append(b('if' if not observe else 'else_if',b('limit',incumbent(person(name,key))+ready)+'\n'+f'set_variable = {{ {pref} = {index} }}'))
            decisions.append((cat,b(command,f'icon = GFX_{P}{"young" if key=="lukashenko" else key}_icon\ncost = 0\nfire_only_once = no\ndays_re_enable = 0\n'+b('allowed','original_tag = BLR')+'\n'+b('visible',gate)+'\n'+b('available',active)+'\n'+b('complete_effect',command+' = yes')+'\nai_will_do = { factor = 0 }')))
            loc[command]='Select '+name;loc[command+'_desc']=loc[P+key+'_desc']+(' Available from '+CONFIG['available_from'].split('.')[0]+'.' if key=='lukashenko' else '')
        choose.append(b('else',f'set_variable = {{ {pref} = 1 }}\n'+appointment('Pyotr Masherov','masherov',slot)))
        cycle=iff('check_variable = { MDCW_HP_native_retirement = 1 }\nNOT = { has_country_flag = do_not_retire }',f'add_to_variable = {{ {pref} = 1 }}\n'+iff(f'check_variable = {{ {pref} > 2 }}\n',f'set_variable = {{ {pref} = 1 }}'))
        branch.append(b('if' if not branch else 'else_if',b('limit',party)+'\n'+cycle+'\n'+'\n'.join(choose)))
        observers.append(b('if' if not observers else 'else_if',b('limit',party)+'\n'+'\n'.join(observe)))
        categories.append(b(cat,'icon = GFX_decision_category_generic_political_actions\npriority = 2000\n'+b('allowed','original_tag = BLR')+'\n'+b('visible',gate)))
        loc[cat]='Leadership Candidates: [show_ruling_party]';loc[cat+'_desc']='Choose the political representative of the governing party. Alexander Lukashenko becomes available in '+CONFIG['available_from'].split('.')[0]+'.'
    effects[P+'BLR_set_leader']=iff(P+'BLR_supported = yes','update_set_politics = yes\n'+'\n'.join(branch)+'\nset_correct_ideology_trait = yes')
    effects[P+'BLR_observe']=iff(P+'BLR_supported = yes',iff('NOT = { '+P+'ready = yes }\n'+leader(),P+'BLR_set_leader = yes')+'\n'+'\n'.join(observers))
    # AI and legacy routes may also enter the old Belarusian slot-six pool.
    effects[P+'BLR_early_fallback']=iff('original_tag = BLR\nIMP_is_1970_scenario = yes\nNOT = { '+P+'ready = yes }',appointment('Pyotr Masherov','masherov',6)+'\nset_correct_ideology_trait = yes')
    for cat in [P+'BLR_candidates_4',P+'BLR_candidates_6']:
        slot=int(cat[-1]);decisions.append((cat,wardrobe_decisions(blr_context()+'\n'+TRIG[slot]+'_are_in_power = yes','BLR_'+str(slot),loc)))
    write('common/scripted_effects/COLDWAR_lukashenko_1970.txt','\n\n'.join(b(k,v) for k,v in effects.items())+'\n')
    write('common/scripted_triggers/COLDWAR_lukashenko_1970.txt','\n\n'.join(b(k,v) for k,v in triggers.items())+'\n')
    write('common/decisions/categories/COLDWAR_lukashenko_1970.txt','\n\n'.join(categories)+'\n')
    write('common/decisions/COLDWAR_lukashenko_1970.txt','\n\n'.join(b(cat,'\n\n'.join(body for c,body in decisions if c==cat)) for cat in dict.fromkeys(c for c,d in decisions))+'\n')
    hooks=b('on_startup',b('effect',b('BLR',P+'BLR_observe = yes')))+'\n'+b('on_monthly_BLR',b('effect',P+'BLR_observe = yes'))
    write('common/on_actions/COLDWAR_lukashenko_1970.txt',b('on_actions',hooks)+'\n')
    write('localisation/english/COLDWAR_lukashenko_1970_l_english.yml','l_english:\n'+HEADER+'\n'.join(' '+k+':0 "'+v.replace('"',"'")+'"' for k,v in sorted(loc.items()))+'\n',True)

def main():
    FILES.clear()
    assets();render()
    from lukashenko_1970.integration import install
    install(write)
    write('tools/lukashenko_1970/runtime_files.json',json.dumps(dict(project='IMPERIA COLD WAR',files=sorted(set(FILES))),indent=2)+'\n')
    print('Lukashenko selector and two portrait variants built. Available from '+CONFIG['available_from'])

if __name__=='__main__':main()
