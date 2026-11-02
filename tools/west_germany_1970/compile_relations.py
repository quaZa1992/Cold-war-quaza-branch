# IMPERIA COLD WAR — Bounded installation of German dossier and politics launchers
"""Render all sources in memory, install only the shared-dossier contract."""
from pathlib import Path
import hashlib
import json
import re
import compile as generator
from compile_security import spans,replace,parse,first

ROOT=Path(__file__).resolve().parents[2]
P='COLDWAR_GER_1970'
MARK='# IMPERIA COLD WAR — German dossier politics panel access\n'


def marked_replace(old,new,key,identity=None):
    a,b,body=spans(old,key,identity)[0]
    updated=replace(old,new,key,identity)
    if not old[:a].endswith(MARK):updated=updated[:a]+MARK+updated[a:]
    return updated


def main():
    captured={}
    generator.write=lambda root,rel,text,bom=False:captured.setdefault(rel,(text,bom)) and rel
    generator.build(str(ROOT),scripts_only=True)
    writes={};review={}
    for rel,(new,bom) in captured.items():
        if 'COLDWAR_DDR_1970_relations' in rel or rel.endswith(P+'_trust_cleanup.txt'):
            writes[rel]=(new,bom);continue
        target=ROOT/rel
        if rel==f'common/scripted_effects/{P}_windows_effects.txt':
            old=target.read_text(encoding='utf-8');result=old
            for key in (P+'_rv_gui_refresh',P+'_rv_gui_presentation',P+'_rv_climate'):
                if spans(result,key):result=marked_replace(result,new,key)
                else:result+='\n'+MARK+spans(new,key)[0][2]+'\n'
            review[rel]=['rv_gui_refresh','rv_gui_presentation','rv_climate']
        elif rel==f'events/{P}_events.txt':
            old=target.read_text(encoding='utf-8');result=marked_replace(old,new,'country_event',('id','COLDWAR_GGR.200'))
            review[rel]=['COLDWAR_GGR.200']
        elif rel==f'localisation/english/{P}_l_english.yml':
            old=target.read_text(encoding='utf-8-sig');result=old
            keys={'cwgg_rv_mo_'+str(i) for i in range(4)}|{'cwgg_rv_none_txt','cwgg_rv_topbar_tt','cwgg_sec_topbar_tt'}
            for key,value in re.findall(r'(?m)^ ([^:\s]+):0 (".*")$',new):
                if not (key.startswith('COLDWAR_GGR.200') or key in keys):continue
                pattern=r'(?m)^ '+re.escape(key)+r':0 ".*"$'
                if re.search(pattern,result):result=re.sub(pattern,lambda _:f' {key}:0 {value}',result)
                else:result+=f' {key}:0 {value}\n'
            review[rel]=['COLDWAR_GGR.200.*']+sorted(keys)
        elif rel==f'common/decisions/{P}_decisions.txt':
            import ddr_relations
            old=target.read_text(encoding='utf-8');result=old
            for key,row in ddr_relations.catalogue().items():
                result=marked_replace(result,new,row['id'])
            result=marked_replace(result,new,P+'_dec_ddr_crisis_course')
            review[rel]=list(ddr_relations.KEYS)+['crisis_course']
        elif rel==f'interface/{P}_windows.gui':
            old=target.read_text(encoding='utf-8');result=old
            names=('cwgg_rv_topbar_container','cwgg_sec_topbar_container')
            for name in names:result=marked_replace(result,new,'containerWindowType',('name',name))
            review[rel]=list(names)
        elif rel==f'common/scripted_guis/{P}_windows.txt':
            old=target.read_text(encoding='utf-8');result=old
            names=('cwgg_rv_topbar','cwgg_sec_topbar')
            for name in names:result=marked_replace(result,new,name)
            # IMPERIA COLD WAR — Replace the legacy undefined security-view trigger.
            result=result.replace(P+'_sec_active = yes','IMP_is_1970_scenario = yes has_country_flag = cwsec_initialized')
            review[rel]=list(names)
        elif rel==f'common/scripted_localisation/{P}_windows.txt':
            old=target.read_text(encoding='utf-8');result=old
            names=('RV_MoscowStance','RV_Bnd')
            for name in names:result=marked_replace(result,new,'defined_text',('name',name))
            review[rel]=list(names)
        elif rel==f'interface/{P}_windows.gfx':
            old=target.read_text(encoding='utf-8');result=old
            names=('GFX_cwgg_launcher_relations','GFX_cwgg_launcher_security')
            for name in names:
                ident=('name',name)
                if spans(result,'spriteType',ident):result=marked_replace(result,new,'spriteType',ident)
                else:
                    end=result.rfind('}')
                    result=result[:end]+MARK+spans(new,'spriteType',ident)[0][2]+'\n'+result[end:]
            review[rel]=list(names)
        else:continue
        if old!=result:writes[rel]=(result,bom)
    # Resolve every existing block before making any change.
    for rel,(text,bom) in writes.items():
        blob=text.encode('utf-8-sig' if bom else 'utf-8')
        target=ROOT/rel;target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists() or target.read_bytes()!=blob:target.write_bytes(blob)
    import ddr_relations
    artwork=ddr_relations.write_art(ROOT)
    import entry_ui
    assets=entry_ui.write_assets(ROOT)
    report=dict(project='IMPERIA COLD WAR',files=sorted(writes)+[artwork]+assets,blocks=review,sha256={r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in list(writes)+[artwork]+assets},engine_tested=False)
    Path(__file__).with_name('relations_integration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(files=len(writes),existing_blocks=sum(map(len,review.values())),engine_tested=False)))


if __name__=='__main__':main()
