# IMPERIA CW — Cold War: merge reviewed complete hunks against the MD ancestor.
"""Complete hunks keep paired structural insertions/deletions atomic.

The original checkout is retained in docs/.../before. A conflict is written to
the audit folder and never installed in the game files.
"""
from pathlib import Path
import difflib,json,subprocess,tempfile
from port import ROOT,BASE,SOURCE,AUDIT,SHARED,MARKER,read,write
from adapt import blocks,block

SKIP={'common/buildings/00_buildings.txt','common/special_projects/projects/naval_projects.txt','common/special_projects/projects/nuclear_projects.txt','common/units/equipment/MD_ballistic_missiles.txt','common/units/equipment/MD_nuclear_missiles.txt','localisation/english/MD_money_l_english.yml','localisation/english/replace/replaced_from_vanilla_buildings_l_english.yml'}

def main():
    reports=[]
    for rel in SHARED:
        if rel in SKIP:continue
        base=read(BASE/rel).splitlines(keepends=True);source=read(SOURCE/rel).splitlines(keepends=True)
        old=read(AUDIT/'before'/rel) if (AUDIT/'before'/rel).exists() else read(ROOT/rel)
        patches=[]
        for group in difflib.SequenceMatcher(None,base,source,autojunk=False).get_grouped_opcodes(3):
            new=''.join(''.join(source[a:b]) for tag,i,j,a,b in group if tag!='equal')
            if not any(k in new.lower() for k in ['uranium','enrichment','imp_raid_','imp_ai_raid_','imp_nuclear_','imp_ai_wants_nukes']):continue
            if rel.endswith('99_investment_scripted_effects.txt') and group[0][1]==0:continue
            if rel.endswith('00_money_system.txt') and 'nuclear_forces_cost' in new:continue
            i=group[0][1];j=group[-1][2];a=group[0][3];b=group[-1][4]
            patches.append((i,j,source[a:b]))
        desired=base[:]
        for i,j,new in reversed(patches):desired[i:j]=new
        with tempfile.TemporaryDirectory(dir=AUDIT) as td:
            paths=[Path(td)/n for n in ['current.txt','base.txt','selected.txt']]
            for path,txt in zip(paths,[old,''.join(base),''.join(desired)]):write(path,txt)
            result=subprocess.run(['git','merge-file','-p',*map(str,paths)],capture_output=True)
        merged=result.stdout.decode('utf-8')
        if result.returncode:
            path=AUDIT/'conflicts'/rel;write(path,merged)
            print('MANUAL',rel,result.returncode);reports.append({'file':rel,'conflict':True});continue
        # Mark modified regions while keeping the existing file's prose/code.
        before=old.splitlines();after=merged.splitlines();inserts=[]
        for tag,i,j,a,b in difflib.SequenceMatcher(None,before,after,autojunk=False).get_opcodes():
            if tag!='equal' and a<b:inserts.append(a)
        for a in reversed(inserts):
            indent=after[a][:len(after[a])-len(after[a].lstrip())]
            after.insert(a,indent+MARKER)
        write(AUDIT/'staged'/rel,'\n'.join(after)+'\n')
        reports.append({'file':rel,'hunks':len(patches),'conflict':False})
    write(AUDIT/'merge_report.json',json.dumps(reports,indent=2))
    print('Merged:',sum(not r['conflict'] for r in reports),'Conflicts:',sum(r['conflict'] for r in reports))

if __name__=='__main__':main()
