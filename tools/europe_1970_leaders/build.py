# IMPERIA COLD WAR — West and East German political leadership selections.
"""Native party candidates, without calendar locks, retaining authored German systems."""
from pathlib import Path
import sys,json,re,uuid,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from europe_1970_leaders.catalogue import PEOPLE
from superpower_1970_leaders.build import IDEO,TRIG,b,iff,incumbent,ident
from historical_politics_1970.special_successors import _assignment_blocks
from multiplayer_quality.native_compat import normalize
P='COLDWAR_EU_1970_'
HEADER='# IMPERIA COLD WAR — German leadership and Eastern portrait integration.\n'
WRITTEN=[]
PROFILES=['ulb','hon','sto','mit','hag','hof','lam','kro','kre','mod']
LEGACY={1:'cwger_cdu_leader',2:'cwger_fdp_leader',3:'cwger_spd_leader'}

def context(tag):return f'original_tag = {tag}\nexists = yes\nis_dynamic_country = no\nIMP_is_1970_scenario = yes'
def preference(tag,slot):return LEGACY[slot] if tag=='GER' and slot in LEGACY else P+tag+'_preference_'+str(slot)
def write(relative,content,bom=False):
    path=ROOT/relative;path.parent.mkdir(parents=True,exist_ok=True)
    if not relative.endswith('.json'):
        content=normalize(content,relative)
        if relative.endswith('.yml'):
            if not content.startswith('l_english:\n'+HEADER):content=content.replace('l_english:\n','l_english:\n'+HEADER,1)
        elif not content.startswith('# IMPERIA COLD WAR — '):content=HEADER+content
    raw=content.encode('utf-8-sig' if bom else 'utf8');old=path.read_bytes() if path.exists() else None
    if old!=raw:
        tmp=path.with_name(path.name+'.coldwar_eu_'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(raw)
        assert (path.read_bytes() if path.exists() else None)==old,'Concurrent edit: '+relative
        tmp.replace(path)
    WRITTEN.append(relative)

def rows():
    data={ident(p):dict(p,id=ident(p)) for p in PEOPLE}
    inventory=json.loads((HERE/'INVENTORY.json').read_text(encoding='utf8'))['people']
    for p in data.values():
        for r in inventory:
            if r['tag']==p['tag'] and r['name'] in [p['name'],*p['aliases']]:
                if r['runtime_name']!=p['name'] and r['runtime_name'] not in p['aliases']:p['aliases'].append(r['runtime_name'])
        p['portrait']='gfx/leaders/COLDWAR_europe_1970/'+p['key']+'.dds'
        p['icon']='gfx/interface/decisions/COLDWAR_europe_1970/'+p['key']+'.dds'
    return data

def portraits(data):
    from europe_1970_leaders.art import convert,sources as portrait_sources
    sources=portrait_sources()
    sprites=[]
    for p in data.values():
        s=sources[p['key']];method=convert(s,p['portrait'])
        dest=ROOT/p['icon'];dest.parent.mkdir(parents=True,exist_ok=True)
        ImageOps.fit(Image.open(ROOT/p['portrait']),(33,30),method=Image.Resampling.LANCZOS,centering=(.5,.1)).save(dest,format='DDS')
        sprites.append(b('spriteType',f'name = "GFX_{P}{p["id"]}"\ntexturefile = "{p["icon"]}"'))
        p.update(source=s,method=method)
    write('interface/COLDWAR_europe_1970_leaders.gfx',b('spriteTypes','\n\n'.join(sprites))+'\n')

def profile_refresh(p,slot):
    desired=p.get('profile') if slot==4 else None
    flags=['COLDWAR_DDR_first_sec_'+k for k in PROFILES]+['COLDWAR_DDR_kessler_leads']
    wanted=['COLDWAR_DDR_first_sec_'+desired] if desired else []
    if desired and p['key']=='heinz_kessler':wanted.append('COLDWAR_DDR_kessler_leads')
    check=b('OR','\n'.join('has_country_flag = '+f for f in flags if f not in wanted)+'\n'+'\n'.join('NOT = { has_country_flag = '+f+' }' for f in wanted))
    return iff(check,'COLDWAR_DDR_clear_first_sec = yes\n'+'\n'.join('set_country_flag = '+f for f in wanted)+'\nforce_update_dynamic_modifier = yes')

def earned_traits(p,slot):
    if p['tag']!='DDR' or slot!=4 or not p.get('profile'):return ''
    if p['key']=='heinz_kessler':return 'add_country_leader_trait = COLDWAR_DDR_hof_army_general'
    text=(ROOT/'common/scripted_effects/COLDWAR_DDR_1970_scripted_effects.txt').read_text(encoding='utf8')
    _,o,e=next(_assignment_blocks(text,'COLDWAR_DDR_install_first_sec_'+p['profile']))
    chunk=text[o+1:e-1]
    return '\n'.join(chunk[s:z] for s,a,z in _assignment_blocks(chunk,'if') if 'has_completed_focus' in chunk[s:z] and 'add_country_leader_trait' in chunk[s:z] and 'create_country_leader' not in chunk[s:z])

def appointment(p,slot):
    traits=[]
    if p['tag']=='GER':traits=['career_politician'] if slot in (1,2,3,17) else []
    create=b('create_country_leader',f'name = "{p["name"]}"\npicture = "{p["portrait"]}"\ndesc = {P}{p["id"]}_desc\nideology = {IDEO[slot]}'+ ('\ntraits = { '+' '.join(traits)+' }' if traits else ''))
    extra=earned_traits(p,slot)
    return iff('NOT = { '+incumbent(p)+' }','retire_country_leader = yes\n'+create+ ('\n'+extra if extra else ''))

def render(data):
    effects={};triggers={};categories=[];decisions=[];loc={}
    for tag in ('GER','DDR'):
        people=[p for p in data.values() if p['tag']==tag];slots=sorted({s for p in people for s in p['slots']})
        extra='\nNOT = { has_country_flag = COLDWAR_GER_1970_dark_regime }' if tag=='GER' else ''
        triggers[P+tag+'_supported']=context(tag)+'\nis_ai = no'+extra+'\n'+b('OR','\n'.join(f'check_variable = {{ ruling_party = {s} }}' for s in slots))
        branches=[];observers=[]
        for slot in slots:
            candidates=[p for p in people if slot in p['slots']];pref=preference(tag,slot)
            party=TRIG[slot]+'_are_in_power = yes';gate=context(tag)+'\nis_ai = no'+extra+'\n'+party
            apply=[];observe=[]
            for index,p in enumerate(candidates,1):
                if p.get('legacy_index') and tag=='GER' and slot in LEGACY:assert p['legacy_index']==index,(p,index)
                observed=f'set_variable = {{ {pref} = {index} }}'
                if tag=='DDR':observed+='\n'+profile_refresh(p,slot)
                observe.append(b('if' if index==1 else 'else_if',b('limit',incumbent(p))+'\n'+observed))
                apply.append(b('if' if index==1 else 'else_if',b('limit',f'check_variable = {{ {pref} = {index} }}')+'\n'+appointment(p,slot)))
                key=P+tag+'_choose_'+str(slot)+'_'+p['key']
                active=b('hidden_trigger',context(tag)+'\nis_ai = no'+extra)+'\n'+party+'\nNOT = { '+incumbent(p)+' }'
                run=f'set_variable = {{ {pref} = {index} }}\n'
                if tag=='DDR':run+='COLDWAR_DDR_clear_heirs = yes\nclr_country_flag = COLDWAR_DDR_ulb_retiring\nclr_country_flag = COLDWAR_DDR_cc_pending\n'
                run+=appointment(p,slot)+'\nset_correct_ideology_trait = yes\n'+P+tag+'_observe = yes'
                effects[key+'_effect']=iff(active,run)
                effects[P+'note_'+p['id']+'_'+str(slot)]=iff(context(tag)+'\nis_ai = no',f'set_variable = {{ {pref} = {index} }}\n'+iff(party,P+tag+'_observe = yes'))
                decisions.append((tag,slot,b(key,f'icon = GFX_{P}{p["id"]}\ncost = 0\nfire_only_once = no\ndays_re_enable = 0\n'+b('allowed','original_tag = '+tag)+'\n'+b('visible',gate)+'\n'+b('available',active)+'\n'+b('complete_effect',key+'_effect = yes')+'\nai_will_do = { factor = 0 }')))
                loc[key]='Select '+p['name'];loc[key+'_desc']=p['description'];loc[P+p['id']+'_desc']=p['description']
            if tag=='DDR':observe.append(b('else',profile_refresh(dict(key='none',profile=None),0)))
            apply.append(b('else',f'set_variable = {{ {pref} = 1 }}\n'+appointment(candidates[0],slot)))
            cycle=iff('check_variable = { MDCW_HP_native_retirement = 1 }\nNOT = { has_country_flag = do_not_retire }',f'add_to_variable = {{ {pref} = 1 }}\n'+iff(f'check_variable = {{ {pref} > {len(candidates)} }}',f'set_variable = {{ {pref} = 1 }}'))
            branches.append(b('if' if not branches else 'else_if',b('limit',party)+'\n'+cycle+'\n'+'\n'.join(apply)))
            observers.append(b('if' if not observers else 'else_if',b('limit',party)+'\n'+'\n'.join(observe)))
            cat=P+tag+'_candidates_'+str(slot)
            categories.append(b(cat,'icon = GFX_decision_category_generic_political_actions\npriority = 2000\n'+b('allowed','original_tag = '+tag)+'\n'+b('visible',gate)))
            loc[cat]='Leadership Candidates: [show_ruling_party]';loc[cat+'_desc']='Choose the political representative of the governing party. Candidates remain available throughout the campaign.'
        cleanup=''
        if tag=='DDR':
            cleanup=iff('NOT = { emerging_communist_state_are_in_power = yes }',profile_refresh(dict(key='none',profile=None),0))
            effects[P+'DDR_cleanup']=iff(context(tag)+'\nis_ai = no',cleanup)
        effects[P+tag+'_observe']=iff(context(tag)+'\nis_ai = no','\n'.join(observers)+'\n'+cleanup+f'\nset_variable = {{ {P}{tag}_observed_party = ruling_party }}')
        # Native West German focuses explicitly write the three existing index variables.
        # Adopting their outgoing incumbent here would overwrite the requested appointment.
        adopt=iff(f'check_variable = {{ {P}{tag}_observed_party = ruling_party }}',P+tag+'_observe = yes') if tag=='DDR' else ''
        effects[P+tag+'_set_leader']=iff(P+tag+'_supported = yes',adopt+'\nupdate_set_politics = yes\n'+'\n'.join(branches)+'\nset_correct_ideology_trait = yes\n'+P+tag+'_observe = yes')
    triggers[P+'supported']=b('OR',P+'GER_supported = yes\n'+P+'DDR_supported = yes')
    triggers[P+'human_ddr']=context('DDR')+'\nis_ai = no'
    pulse='\n'.join(b(tag,iff('exists = yes\nIMP_is_1970_scenario = yes',P+tag+'_observe = yes')) for tag in ('GER','DDR'))
    hooks=b('on_startup',b('effect',pulse))+'\n'+'\n'.join(b('on_monthly_'+tag,b('effect',iff(context(tag),P+tag+'_observe = yes'))) for tag in ('GER','DDR'))
    write('common/scripted_effects/COLDWAR_europe_1970_leaders.txt','\n\n'.join(b(k,v) for k,v in effects.items())+'\n')
    write('common/scripted_triggers/COLDWAR_europe_1970_leaders.txt','\n\n'.join(b(k,v) for k,v in triggers.items())+'\n')
    write('common/decisions/categories/COLDWAR_europe_1970_leaders.txt','\n\n'.join(categories)+'\n')
    write('common/decisions/COLDWAR_europe_1970_leaders.txt','\n\n'.join(b(P+tag+'_candidates_'+str(slot),'\n\n'.join(t for tg,s,t in decisions if tg==tag and s==slot)) for tag in ('GER','DDR') for slot in sorted({s for tg,s,t in decisions if tg==tag}))+'\n')
    write('common/on_actions/COLDWAR_europe_1970_leaders.txt',b('on_actions',hooks)+'\n')
    write('localisation/english/COLDWAR_europe_1970_leaders_l_english.yml','l_english:\n'+HEADER+'\n'.join(' '+k+':0 "'+v.replace('"',"'")+'"' for k,v in sorted(loc.items()))+'\n',True)

def main():
    from europe_1970_leaders.art import install_eastern,document
    install_eastern()
    data=rows();portraits(data);render(data)
    from europe_1970_leaders.integration import install
    install(data,write)
    document(data)
    write('tools/europe_1970_leaders/runtime_roster.json',json.dumps(dict(project='IMPERIA COLD WAR',calendar_eligibility=False,people=list(data.values())),ensure_ascii=False,indent=2)+'\n')
    (HERE/'runtime_files.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',files=sorted(set(WRITTEN))),indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(people=len(data),unique_people=len({p['key'] for p in PEOPLE}),choices=sum(len(p['slots']) for p in PEOPLE))))
if __name__=='__main__':main()
