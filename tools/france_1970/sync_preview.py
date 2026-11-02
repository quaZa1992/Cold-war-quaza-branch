# IMPERIA COLD WAR — Synchronize the existing France inspector with installed content.
"""Refresh data without running archived concept generators or altering approved input."""
import copy
import hashlib
import json
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
PREVIEW=Path('C:/Users/Enes/.codex/visualizations/2026/10/23/01a16840-34d5-7e60-8c3d-134a5e042a6a/coldwar_france_politics/coldwar-france-politics.html')
D=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'))
policy=json.loads((HERE/'offer_policy.json').read_text(encoding='utf-8'))
text=PREVIEW.read_text(encoding='utf-8')
pattern=r'(<script[^>]*id="ef-data"[^>]*>)(.*?)(</script>)'
match=re.search(pattern,text,re.S)
assert match, 'Missing existing preview data payload'
data=json.loads(match.group(2))
fields={k for n in data['nodes'] for k in n}
data['nodes']=[{k:copy.deepcopy(v) for k,v in n.items() if k in fields} for n in D['nodes']]
data['residual_spirits']=copy.deepcopy(D['residual_spirits'])
data['spirits']=copy.deepcopy(D['spirits'])
data['status']='Implemented; native engine render untested'
data['offer_policy']=policy
data['offers']=copy.deepcopy(D['offers'])
for offer in data['offers']:
    if offer['duration_days']:
        offer['duration_days']=None
        offer['kind']='permanent_compact'
        offer['lifecycle']['government_change']='Accepted spirits survive government changes; pending quotes retain their government checks.'
        offer['lifecycle']['termination']='Withdrawal, bilateral war, bilateral Imperia sanctions, lost sovereignty or a missing signatory ends both spirits.'
        offer['lifecycle']['renegotiation']='No scheduled expiry. A terminated compact requires fresh consent and its approved setup charges.'
    else:
        offer['kind']='finite_research_exchange'
data['offer_rules']={'lifecycle_override':policy,'research_exchanges':'Approved finite awards and durable receipts retained.'}
payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')
text=text[:match.start(2)]+payload+text[match.end(2):]
text=text.replace('<!-- IMPERIA CW — Cold War: France policy structure and visible numeric effects. -->','<!-- IMPERIA COLD WAR — France installed tree and native numeric effects. -->')
assert 'Awaiting approval before game implementation' not in text
assert len(text.encode('utf-8'))<1_000_000
PREVIEW.write_text(text,encoding='utf-8',newline='\n')
report={'project':'IMPERIA COLD WAR','preview':str(PREVIEW),'sha256':hashlib.sha256(PREVIEW.read_bytes()).hexdigest(),'focuses':len(data['nodes']),'groups':len(data['groups']),'offers':len(data['offers']),'source':'approved_design.json plus offer_policy.json; rendered script model, not HOI4 screenshot'}
(HERE/'PREVIEW_SYNC.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
