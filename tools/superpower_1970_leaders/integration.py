# IMPERIA COLD WAR — Preserve political candidate selections across native providers.
"""Idempotent adapters for the canonical Soviet, USA and historical-pool writers."""
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from historical_politics_1970.special_successors import _assignment_blocks, _block_end, _one_string, _one_atom

P = 'COLDWAR_SP_1970_'
MARK = '# IMPERIA COLD WAR — USA and Soviet political leadership integration.\n'


def b(k, body):
    return k+' = {\n'+'\n'.join('\t'+s if s else '' for s in body.splitlines())+'\n}'


def wrapped(test, body):
    return b('if', b('limit', test)+'\n'+body)


def format_block(text):
    """Indent an edited container, preserving statements, comments and quoted braces."""
    depth=0; lines=[]
    for raw in text.splitlines():
        line=raw.strip()
        if not line:
            lines.append('');continue
        code=re.sub(r'"(?:\\.|[^"\\])*"','""',line).split('#',1)[0]
        leading=1 if code.startswith('}') else 0
        lines.append('\t'*max(0,depth-leading)+line)
        depth+=code.count('{')-code.count('}')
        assert depth>=0,line
    assert depth==0
    return '\n'.join(lines)


def body_patch(text, name, transform, first_only=False):
    hits = list(_assignment_blocks(text, name))
    if first_only: hits=hits[:1]
    assert len(hits)==1, (name,len(hits))
    _,o,e=hits[0]
    return text[:o+1]+'\n'+transform(text[o+1:e-1]).strip('\n')+'\n'+text[e-1:]


def portrait_map():
    path=HERE/'runtime_roster.json'
    if path.exists():
        return {r['id']:r for r in json.loads(path.read_text(encoding='utf-8'))['people']}
    return {}


def native_creations(text, data):
    names={n:r for r in data.values() for n in [r['name'],*r.get('aliases',[])]}
    from superpower_1970_leaders.build import IDEO
    replacements=[]
    for start,o,end in _assignment_blocks(text,'create_country_leader'):
        block=text[start:end]; name=_one_string(block,'name'); row=names.get(name)
        if not row: continue
        picture='picture = "'+row['portrait']+'"'
        if re.search(r'\bpicture\s*=\s*"[^"]*"',block):
            revised=re.sub(r'\bpicture\s*=\s*"[^"]*"',picture,block,count=1)
        else:
            revised=block[:block.index('{')+1]+' '+picture+block[block.index('{')+1:]
        ideology=_one_atom(block,'ideology')
        if ideology in IDEO and IDEO.index(ideology) in row['slots']:
            slot=IDEO.index(ideology)
            call=P+'note_'+row['id']+'_'+str(slot)+' = yes'
            # Every actual legacy appointment records its own preference before any party dispatcher.
            tail=text[end:end+len(call)+120]
            if call not in tail:
                revised+='\nhidden_effect = { '+call+' }'
        replacements.append((start,end,revised))
    for start,end,revised in reversed(replacements): text=text[:start]+revised+text[end:]
    lines=text.splitlines(keepends=True)
    for i,line in enumerate(lines):
        if i and line.lstrip().startswith('hidden_effect = { '+P+'note_'):
            indent=re.match(r'[\t ]*',lines[i-1])[0]
            lines[i]=indent+line.lstrip()
    return ''.join(lines)


def envelope(text, effect, test, run):
    if '# COLDWAR SP '+effect+' BEGIN' in text: return text
    def patch(body):
        return '# COLDWAR SP '+effect+' BEGIN\n'+wrapped(test,run)+'\n'+b('else',body.strip())+'\n# COLDWAR SP '+effect+' END'
    return body_patch(text,effect,patch)


def guard_modern_menu(text):
    # The pre-existing 2000 candidate menus retain their effects and traits in that bookmark.
    # Guard execution as well as visibility, because an old UI request can arrive after a switch.
    changes=[]
    for key in ('visible','available'):
        for start,o,end in _assignment_blocks(text,key):
            if 'NOT = { IMP_is_1970_scenario = yes }' not in text[o:end]:
                changes.append((o+1,o+1,'\n\tNOT = { IMP_is_1970_scenario = yes }'))
    for start,o,end in _assignment_blocks(text,'complete_effect'):
        body=text[o+1:end-1]
        if '# COLDWAR SP MODERN EXECUTION' not in body:
            changes.append((o+1,end-1,'\n# COLDWAR SP MODERN EXECUTION\n'+wrapped('NOT = { IMP_is_1970_scenario = yes }',body.strip())+'\n'))
    for start,end,revised in sorted(changes,reverse=True): text=text[:start]+revised+text[end:]
    return text


def adapt(relative,text,data=None):
    """Transform only known runtime providers; safe for generated output directories."""
    relative=str(relative).replace('\\','/')
    data=data or portrait_map()
    original=text
    if relative=='common/scripted_effects/00_leader_setup_scripted_effects.txt':
        if '# COLDWAR SP EARLY ROUTE' not in text:
            anchor='# MDCW SOVIET RETIREMENT ROUTE BEGIN\n\tif = {'
            assert anchor in text, 'Native Soviet retirement anchor changed'
            route='# COLDWAR SP EARLY ROUTE\n'+wrapped(P+'supported = yes',
                wrapped('original_tag = USA',P+'USA_set_leader = yes')+'\n'+b('else',P+'SOV_set_leader = yes'))+'\n\t'
            text=text.replace(anchor,route+'# MDCW SOVIET RETIREMENT ROUTE BEGIN\n\telse_if = {',1)
    if relative in ('common/scripted_effects/USA_political_leaders.txt','common/scripted_effects/SOV_political_leaders.txt'):
        tag=Path(relative).name[:3]
        text=envelope(text,'set_leader_'+tag,P+tag+'_supported = yes',P+tag+'_set_leader = yes')
    if relative=='common/scripted_effects/USA_1970_scripted_effects.txt':
        text=envelope(text,'USA_1970_set_scenario_leader',P+'USA_supported = yes',P+'USA_set_leader = yes')
    creation_files={
        'common/scripted_effects/USA_political_leaders.txt', 'common/scripted_effects/SOV_political_leaders.txt',
        'common/scripted_effects/USA_1970_scripted_effects.txt','common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt',
        'common/national_focus/USA_1970.txt','common/national_focus/COLDWAR_SOV_1970_focus.txt',
        'events/USA_1970_events.txt','events/COLDWAR_SOV_1970_events.txt',
        'common/scripted_effects/mdcw_historical_special_successors.txt',
        'common/scripted_effects/mdcw_historical_sov_egy_successors.txt'}
    if relative in creation_files and data:
        text=native_creations(text,data)
    if relative=='common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt':
        from superpower_1970_leaders.catalogue import PEOPLE
        for key in ('bre','kos','pod','sus','and','gre','ust','che'):
            effect='COLDWAR_SOV_alive_'+key
            if '# COLDWAR SP UNDATED '+key in text: continue
            alt=next((r for r in PEOPLE if r['tag']=='SOV' and r.get('profile')==key and r.get('standin')),None)
            human=P+'human_sov = yes'
            if alt: human+='\nNOT = { has_country_leader = { name = "'+alt['name']+'" ruling_only = yes } }'
            def change(body,key=key,human=human):
                return '# COLDWAR SP UNDATED '+key+'\n'+b('OR',b('AND',human)+'\n'+b('AND','NOT = { '+P+'human_sov = yes }\n'+body.strip()))
            text=body_patch(text,effect,change)
    if relative=='events/COLDWAR_SOV_1970_events.txt':
        edits=[]
        for start,o,end in _assignment_blocks(text,'country_event'):
            chunk=text[start:end]
            if not re.search(r'\bid\s*=\s*COLDWAR_SOV\.9[0-7](?!\d)',chunk): continue
            if '# COLDWAR SP DEATH GUARD' in chunk: continue
            chunk=body_patch(chunk,'trigger',lambda body:'# COLDWAR SP DEATH GUARD\nNOT = { '+P+'human_sov = yes }\n'+body.strip(), first_only=True)
            chunk=body_patch(chunk,'immediate',lambda body:wrapped('NOT = { '+P+'human_sov = yes }',body.strip()))
            # Recheck a queued option at execution, independently of its visible trigger.
            opt_changes=[]
            for st,op,en in _assignment_blocks(chunk,'option'):
                option=chunk[st:en]
                for statement in ('COLDWAR_SOV_succession = yes',):
                    option=option.replace(statement,wrapped('NOT = { '+P+'human_sov = yes }',statement))
                option=re.sub(r'(?m)^(\s*)(clr_country_flag\s*=\s*COLDWAR_SOV_gensec_\w+)',
                    lambda m:m[1]+wrapped('NOT = { '+P+'human_sov = yes }',m[2]),option)
                opt_changes.append((st,en,option))
            for st,en,revised in reversed(opt_changes): chunk=chunk[:st]+revised+chunk[en:]
            edits.append((start,end,chunk))
        for start,end,revised in reversed(edits): text=text[:start]+format_block(revised)+text[end:]
        # Also repair the second option of events already emitted by the first adapter revision.
        # It contained an inline flag clear and must recheck the human calendar guard too.
        text=re.sub(r'if\s*=\s*\{\s*limit\s*=\s*\{\s*has_country_flag\s*=\s*(COLDWAR_SOV_gensec_\w+)\s*\}\s*clr_country_flag\s*=\s*\1\s*\}',
            lambda m:'if = { limit = { has_country_flag = '+m[1]+' NOT = { '+P+'human_sov = yes } } clr_country_flag = '+m[1]+' }',text)
        for start,o,end in reversed(list(_assignment_blocks(text,'country_event'))):
            chunk=text[start:end]
            if '# COLDWAR SP DEATH GUARD' in chunk:text=text[:start]+format_block(chunk)+text[end:]
    if re.fullmatch(r'common/decisions/(?:categories/)?imp_leader_(?:usa_rep|usa_dem|sov_cprf)_(?:decisions|cat)\.txt',relative):
        text=guard_modern_menu(text)
    # Format only containers changed by this integration.
    names=[]
    if relative=='common/scripted_effects/00_leader_setup_scripted_effects.txt':names=['set_leader']
    if relative in ('common/scripted_effects/USA_political_leaders.txt','common/scripted_effects/SOV_political_leaders.txt'):
        names=['set_leader_'+Path(relative).name[:3]]
    if relative=='common/scripted_effects/USA_1970_scripted_effects.txt':names=['USA_1970_set_scenario_leader']
    if relative=='common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt':
        names=['COLDWAR_SOV_alive_'+key for key in ('bre','kos','pod','sus','and','gre','ust','che')]
    for name in names:
        for start,o,end in reversed(list(_assignment_blocks(text,name))):text=text[:start]+format_block(text[start:end])+text[end:]
    if text!=original and not text.startswith(MARK): text=MARK+text
    return text


def install(data,write):
    paths=['common/scripted_effects/00_leader_setup_scripted_effects.txt',
        'common/scripted_effects/USA_political_leaders.txt','common/scripted_effects/SOV_political_leaders.txt',
        'common/scripted_effects/USA_1970_scripted_effects.txt','common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt',
        'common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt',
        'common/national_focus/USA_1970.txt','common/national_focus/COLDWAR_SOV_1970_focus.txt',
        'events/USA_1970_events.txt','events/COLDWAR_SOV_1970_events.txt']
    paths += ['common/decisions/'+folder+'imp_leader_'+key+'_'+suffix+'.txt'
        for folder,suffix in (('','decisions'),('categories/','cat')) for key in ('usa_rep','usa_dem','sov_cprf')]
    # Include the real generated historical-pool effect names without relying on guessed filenames.
    paths += [p.relative_to(ROOT).as_posix() for p in (ROOT/'common/scripted_effects').glob('mdcw*successor*.txt')]
    for relative in paths:
        path=ROOT/relative
        if path.exists():
            old=path.read_text(encoding='utf-8-sig'); new=adapt(relative,old,data)
            if new!=old or new.startswith(MARK): write(relative,new)
    install_writers(write)


def install_writers(write):
    # Narrow writer adapters ensure regeneration does not undo the reviewed integration.
    providers=[('Claude outputs/COLDWAR_SOV_generator/cw_common.py',
        '    text = native_compatibility(text, path)',
        '    from superpower_1970_leaders.integration import adapt as superpower_leadership\n    text = superpower_leadership(path, text)'),
        ('tools/usa_1970_expansion/compile.py','    text=revised',
        '    from superpower_1970_leaders.integration import adapt as superpower_leadership\n    text=superpower_leadership(relative,revised)'),
        ('tools/historical_politics_1970/build.py','    def write(self, path, text):',
        '        import sys\n        sys.path.insert(0, str(ROOT / "tools"))\n        from superpower_1970_leaders.integration import adapt as superpower_leadership\n        text = superpower_leadership(path, text)')]
    for relative,anchor,hook in providers:
        path=ROOT/relative; content=path.read_text(encoding='utf-8-sig')
        if 'import adapt as superpower_leadership' in content:
            if relative=='tools/historical_politics_1970/build.py':
                old='    def write(self, path, text):\n        from superpower_1970_leaders.integration import adapt as superpower_leadership'
                new='    def write(self, path, text):\n        import sys\n        sys.path.insert(0, str(ROOT / "tools"))\n        from superpower_1970_leaders.integration import adapt as superpower_leadership'
                content=content.replace(old,new,1)
            write(relative,content)
            continue
        assert anchor in content, relative
        if relative.endswith('build.py'):
            content=content.replace(anchor,anchor+'\n'+hook,1)
        elif relative.endswith('compile.py'):
            content=content.replace(anchor,hook,1)
        else:
            content=content.replace(anchor,anchor+'\n'+hook,1)
        write(relative,MARK+content if not content.startswith(MARK) else content)
