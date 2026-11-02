# IMPERIA COLD WAR — Preserve German selections across canonical native providers.
from pathlib import Path
import sys,json,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from historical_politics_1970.special_successors import _assignment_blocks,_one_string,_one_atom
from superpower_1970_leaders.integration import body_patch,format_block,guard_modern_menu
from europe_1970_leaders.build import P,HEADER,IDEO,b,iff

def data_default():
    path=HERE/'runtime_roster.json'
    return {r['id']:r for r in json.loads(path.read_text(encoding='utf8'))['people']} if path.exists() else {}

def creations(text,data):
    names={}
    for p in data.values():
        for n in [p['name'],*p['aliases']]:names.setdefault(n,[]).append(p)
    edits=[]
    for start,o,end in _assignment_blocks(text,'create_country_leader'):
        block=text[start:end];matches=names.get(_one_string(block,'name'))
        if not matches:continue
        p=matches[0]
        picture='picture = "'+p['portrait']+'"'
        if re.search(r'\bpicture\s*=\s*"[^"]*"',block):revised=re.sub(r'\bpicture\s*=\s*"[^"]*"',picture,block,count=1)
        else:revised=block[:block.index('{')+1]+' '+picture+block[block.index('{')+1:]
        ideology=_one_atom(block,'ideology')
        adjacent=re.match(r'(?:\s*hidden_effect\s*=\s*\{\s*COLDWAR_EU_1970_note_[^{}]*\})*',text[end:]).group()
        for candidate in matches:
            if ideology in IDEO and IDEO.index(ideology) in candidate['slots']:
                call=P+'note_'+candidate['id']+'_'+str(IDEO.index(ideology))+' = yes'
                if call not in adjacent:revised+='\nhidden_effect = { '+call+' }'
        edits.append((start,end,revised))
    for start,end,revised in reversed(edits):text=text[:start]+revised+text[end:]
    return text

def envelope(text,effect,test,run):
    marker='# COLDWAR EU '+effect+' BEGIN'
    if marker in text:return text
    return body_patch(text,effect,lambda body:marker+'\n'+iff(test,run,body.strip())+'\n# COLDWAR EU '+effect+' END')

CREATION_FILES={
 'common/scripted_effects/COLDWAR_GER_1970_effects.txt','common/national_focus/COLDWAR_GER_1970_focus.txt','events/COLDWAR_GER_1970_events.txt',
 'common/scripted_effects/COLDWAR_DDR_1970_scripted_effects.txt','common/national_focus/COLDWAR_DDR_1970_focus.txt','events/COLDWAR_DDR_1970_events.txt',
 'common/scripted_effects/mdcw_historical_special_successors.txt','common/scripted_effects/mdcw_historical_sov_egy_successors.txt',
 'common/scripted_effects/mdcw_historical_native_pools.txt',
}

def adapt(relative,text,data=None):
    relative=str(relative).replace('\\','/');data=data or data_default();original=text;changed_blocks=[]
    if relative=='common/scripted_effects/00_leader_setup_scripted_effects.txt':
        if '# COLDWAR EU EARLY ROUTE' not in text:
            def patch(body):
                anchor='# COLDWAR SP EARLY ROUTE\n\tif = {'
                assert anchor in body,'Native early route changed'
                route='# COLDWAR EU EARLY ROUTE\n'+iff(P+'supported = yes',iff('original_tag = GER',P+'GER_set_leader = yes',P+'DDR_set_leader = yes'))+'\n\t# COLDWAR SP EARLY ROUTE\n\telse_if = {'
                body=body.replace(anchor,route,1)
                return '# COLDWAR EU PROFILE CLEANUP\n'+P+'DDR_cleanup = yes\n'+body
            text=body_patch(text,'set_leader',patch)
        changed_blocks.append('set_leader')
    wrappers={
     'common/scripted_effects/COLDWAR_GER_1970_effects.txt':('COLDWAR_GER_1970_set_leader','GER'),
     'common/scripted_effects/GER_political_leaders.txt':('set_leader_GER','GER'),
     'common/scripted_effects/DDR_political_leaders.txt':('set_leader_DDR','DDR'),
    }
    if relative in wrappers:
        effect,tag=wrappers[relative]
        text=envelope(text,effect,P+tag+'_supported = yes',P+tag+'_set_leader = yes');changed_blocks.append(effect)
    if relative in CREATION_FILES and data:text=creations(text,data)
    if relative in ('history/countries/GER - Germany.txt','history/countries/DDR - East Germany.txt') and data:
        # Touch the 1970 date block only. Other bookmarks retain their portraits and leaders.
        text=body_patch(text,'1970.1.1',lambda body:creations(body,data))
    if relative=='common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt':
        for key in ('ulb','hof','lam'):
            effect='COLDWAR_DDR_alive_'+key;marker='# COLDWAR EU UNDATED '+key
            if marker not in text:text=body_patch(text,effect,lambda body,marker=marker:marker+'\n'+b('OR',P+'human_ddr = yes\n'+b('AND','NOT = { '+P+'human_ddr = yes }\n'+body.strip())))
            changed_blocks.append(effect)
    if re.fullmatch(r'common/decisions/(?:categories/)?imp_leader_ger_(?:spd|grune|fdp|cdu)_(?:decisions|cat)\.txt',relative):
        text=guard_modern_menu(text)
    for name in changed_blocks:
        for start,o,end in reversed(list(_assignment_blocks(text,name))):text=text[:start]+format_block(text[start:end])+text[end:]
    if text!=original and not text.startswith(HEADER):text=HEADER+text
    return text

def install(data,write):
    files=set(CREATION_FILES)|{
     'common/scripted_effects/00_leader_setup_scripted_effects.txt','common/scripted_effects/GER_political_leaders.txt',
     'common/scripted_effects/DDR_political_leaders.txt','common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt',
     'history/countries/GER - Germany.txt','history/countries/DDR - East Germany.txt',
    }
    files|={p.relative_to(ROOT).as_posix() for p in (ROOT/'common/scripted_effects').glob('mdcw*pool*.txt')}
    files|={'common/decisions/'+folder+'imp_leader_ger_'+party+'_'+suffix+'.txt' for folder,suffix in (('','decisions'),('categories/','cat')) for party in ('spd','grune','fdp','cdu')}
    for relative in sorted(files):
        path=ROOT/relative
        if not path.exists():continue
        old=path.read_text(encoding='utf-8-sig');new=adapt(relative,old,data)
        if new!=old or new.startswith(HEADER):write(relative,new)
    install_writers(write)

def install_writers(write):
    hooks=[
     ('tools/west_germany_1970/compile.py','def write(root, rel, text, bom=False):','    import sys\n    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))\n    from europe_1970_leaders.integration import adapt as europe_leadership\n    text = europe_leadership(rel, text)'),
     ('Claude outputs/COLDWAR_DDR_generator/dg_common.py','def write(path, text, bom=False):','    import sys\n    sys.path.insert(0, os.path.join(MOD, "tools"))\n    from europe_1970_leaders.integration import adapt as europe_leadership\n    text = europe_leadership(path, text)'),
     ('tools/historical_politics_1970/build.py','    def write(self, path, text):','        import sys\n        sys.path.insert(0, str(ROOT / "tools"))\n        from europe_1970_leaders.integration import adapt as europe_leadership\n        text = europe_leadership(path, text)'),
    ]
    for relative,anchor,hook in hooks:
        path=ROOT/relative;text=path.read_text(encoding='utf-8-sig')
        if 'import adapt as europe_leadership' not in text:
            assert anchor in text,relative;text=text.replace(anchor,anchor+'\n'+hook,1)
        write(relative,text)
