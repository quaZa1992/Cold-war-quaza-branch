from pathlib import Path
from check_highrisk import parse
import json,hashlib,difflib
out=Path(__file__).parent; base=out.parent
target=Path('C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdimperia_md202_review')
old=Path('E:/SteamLibrary/steamapps/workshop/content/394360/3464169624')
native=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
m=json.loads((base/'shared_modifier_readers_manifest.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
comments={m['files'][0]['path']:b'\t# Imperia: civilian GNSS resource-extraction bonus removed',m['files'][1]['path']:b'\t# Imperia: remaining scripted Western-sanctions effects disabled (Imperia uses its own sanctions system)'}
rows=[]
for f in m['files']:
    b=Path(f['backup']).read_bytes(); a=(target/f['path']).read_bytes(); nl=b'\r\n' if b'\r\n' in b else b'\n'
    expected=nl.join(('\t'+k+' = '+v).encode() for k,v in f['restored_assignments'].items())
    original=comments[f['path']]
    checks={'before_hash':sha(b)==f['before_sha256'],'after_hash':sha(a)==f['after_sha256'],'only_one_comment_replaced_remainder_bytes_exact':b.count(original)==1 and b.replace(original,expected)==a}
    e1,err1=parse(Path(f['backup'])); e2,err2=parse(target/f['path']); checks['target_balanced']=not err2
    norm=lambda e:{k:v for k,v in e.items() if k!='line'}
    serialized=lambda ee:[json.dumps(norm(e),sort_keys=True) for e in ee]
    sm=difflib.SequenceMatcher(a=serialized(e1),b=serialized(e2),autojunk=False)
    changes=[{'op':op,'before':e1[i:j],'after':e2[k:l]} for op,i,j,k,l in sm.get_opcodes() if op!='equal']
    added=[e for c in changes for e in c['after']]
    checks['ast_only_six_assignments_added']=len(changes)==1 and changes[0]['op']=='insert' and len(added)==6 and {e['key']:e['value'] for e in added}==f['restored_assignments'] and all(e['parents']==[f['provider']] and not e['block'] for e in added)
    checks['no_duplicate_reader_in_provider']=all(len([e for e in e2 if e['key']==k and e['parents']==[f['provider']]])==1 for k in f['restored_assignments'])
    witnesses={}
    for label,root in [('old',old),('native',native)]:
        pp=root/f['path']; ee=parse(pp)[0]; raw=pp.read_bytes().splitlines()
        relevant=[e for e in ee if e['parents']==[f['provider']] and e['key'] in f['restored_assignments']]
        checks[label+'_six_active_scope_value_assignments_identical']=len(relevant)==6 and {e['key']:e['value'] for e in relevant}==f['restored_assignments']
        restored_lines=[line for line in a.splitlines() if line in expected.splitlines()]
        checks[label+'_six_exact_active_source_lines_identical']=len(restored_lines)==6 and all(raw.count(line)==1 for line in restored_lines)
        witnesses[label]=[{'file':str(pp),'line':e['line'],'key':e['key'],'value':e['value']} for e in relevant]
    rows.append({'file':f['path'],'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL','assignment_changes':changes,'source_witnesses':witnesses})
guards={p:sha(Path(p).read_bytes())==h for p,h in m['source_sha256_guards'].items()}
result={'status':'PASS' if all(r['status']=='PASS' for r in rows) and all(guards.values()) else 'FAIL','manifest':str(base/'shared_modifier_readers_manifest.json'),'files':rows,'source_sha256_guards':guards,'engine_test_performed':False,'meaning':'Exact remainder-byte and active-assignment QA of six GNSS and six SOV readers; no gameplay or balance certification.'}
(out/'shared_modifier_readers_FINAL_QA.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'files':[{'file':r['file'],'checks':r['checks']} for r in rows]},indent=2))
