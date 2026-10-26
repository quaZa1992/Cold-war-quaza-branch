# IMPERIA CW — Cold War: prohibit every AI raid at preparation and launch.
from pathlib import Path
import json
import re
from port import ROOT, AUDIT, MARKER, read, write
from adapt import blocks, modify

def enforce():
    counts={}
    for p in (ROOT/'common/raids').glob('*.txt'):
        def human_only(s):
            roots=blocks(s)
            if not roots or roots[0]['name']!='types':return s
            edits=[]; count=0
            for raid in roots[0]['children']:
                if raid['name'] is None:continue
                count+=1
                for obsolete in [n for n in raid['children'] if n['name']=='can_launch']:
                    clean=re.sub(r'#[^\n]*','',s[obsolete['open']:obsolete['close']])
                    assert re.fullmatch(r'\s*(is_ai\s*=\s*no\s*)+',clean)
                    edits.append((obsolete['start'],obsolete['end'],''))
                for field in ['available','launchable']:
                    nodes=[n for n in raid['children'] if n['name']==field]
                    if nodes:
                        n=nodes[0]; body=s[n['open']:n['close']]
                        body=re.sub(r'\n\t{3}# IMPERIA CW[^\n]*\n\t{3}# COLDWAR_AI_RAIDS_DISABLED\n?', '', body)
                        body=re.sub(r'(?m)^\t{3}is_ai\s*=\s*no\s*\n','',body)
                        body='\n\t\t\t'+MARKER+'\n\t\t\t# COLDWAR_AI_RAIDS_DISABLED\n\t\t\tis_ai = no\n'+body
                        edits.append((n['open'],n['close'],body))
                    else:
                        edits.append((raid['open'],raid['open'],'\n\t\t'+MARKER+'\n\t\t# COLDWAR_AI_RAIDS_DISABLED\n\t\t'+field+' = { is_ai = no }'))
            counts[p.name]=count
            for start,end,body in sorted(edits,reverse=True):s=s[:start]+body+s[end:]
            return s
        modify(p.relative_to(ROOT),human_only)
    write(AUDIT/'raid_policy.json',json.dumps(counts,indent=2))
    print('Human-only raid definitions:',sum(counts.values()),'in',len(counts),'files')

if __name__=='__main__':enforce()
