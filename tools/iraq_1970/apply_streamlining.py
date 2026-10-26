# IMPERIA CW — Cold War: scoped installation of focus-owned reforms.
"""Never invokes broad integration, art generation, or other-country generators."""
from pathlib import Path
import hashlib,json,sys,zipfile
from common import ROOT,P,parse,first,walk,locline

HERE=Path(__file__).resolve().parent
REPORT=ROOT/'docs/design/iraq_1970/decision_streamlining_2026_10_21'
BASELINE=HERE/'decision_streamlining_baseline.json'

def original_shares():
 if not BASELINE.exists():raise RuntimeError('Run apply_streamlining.py --prepare before generation')
 return json.loads(BASELINE.read_text(encoding='utf-8'))['shares']

def prepare():
 if BASELINE.exists():return
 REPORT.mkdir(parents=True,exist_ok=True)
 path=ROOT/'common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt'
 shares={}
 for k,o,b in parse(path.read_text(encoding='utf-8-sig')):
  if not k.startswith(P+'apply_') or not isinstance(b,list):continue
  key=k.removeprefix(P+'apply_');var=P+key+'_invoice'
  shares[key]=next((float(first(v,var)) for a,op,v in walk(b) if a=='multiply_variable' and isinstance(v,list) and first(v,var) is not None),0)
 assert len(shares)==426,len(shares)
 targets=[]
 for folder in ['common/national_focus','common/scripted_effects','common/scripted_triggers','common/decisions','common/decisions/categories','common/dynamic_modifiers','events','localisation/english']:
  for p in (ROOT/folder).glob('*COLDWAR_IRQ*'):
   if p.is_file():targets.append(p)
 targets += [ROOT/'common/decisions/COLDWAR_USA_gulf_decisions.txt',ROOT/'common/national_focus/USA_1970.txt']
 hashes={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in targets}
 with zipfile.ZipFile(REPORT/'before.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in targets:z.write(p,str(p.relative_to(ROOT)))
 BASELINE.write_text(json.dumps({'feature':'IMPERIA CW — Cold War: decision streamlining original costs','shares':shares,'hashes':hashes},indent=2)+'\n',encoding='utf-8')

def merged_localisation(old,updates):
 import re
 for k,v in updates.items():
  row=locline(k,v);pattern=r'(?m)^\s*'+re.escape(k)+r':\d*\s+".*"\s*$'
  if re.search(pattern,old):old=re.sub(pattern,lambda _:row,old)
  else:old+='\n'+row
 return old+'\n' if not old.endswith('\n') else old

def generate():
 import compile as c
 import decisions_module,decision_streamlining,presentation,reward_overhaul
 c.CONDITIONS.update(decisions_module.CONTRACTS);c.CONDITIONS.update(c.OWN_CONDITIONS)
 c.generate_focuses();c.generate_programmes();c.generate_queue()
 for rel,text in decisions_module.generate(ROOT).items():
  # Art and ideas have no semantic change and remain owned by their existing files.
  if rel in ['interface/COLDWAR_IRQ_1970_decision_ideas.gfx']:continue
  c.OUTPUTS[rel]=text if rel.endswith('.yml') else c.HEADER+c.format_code(text)
 c.LOC.update(presentation.build_loc());c.LOC.update(c.BONUS_LOCALISATION);c.LOC.update(reward_overhaul.BONUS_LOCALISATION)
 locpath='localisation/english/COLDWAR_IRQ_1970_focus_l_english.yml'
 c.OUTPUTS[locpath]=merged_localisation((ROOT/locpath).read_text(encoding='utf-8-sig'),c.LOC)
 for rel in ['common/decisions/COLDWAR_USA_gulf_decisions.txt','common/national_focus/USA_1970.txt']:
  c.OUTPUTS[rel]=(ROOT/rel).read_text(encoding='utf-8-sig')
 outputs,report=decision_streamlining.transform(c.OUTPUTS,c.D,c.eligible,c.capacity,original_shares(),c.CONDITIONS)
 return outputs,c.D,report

def main():
 prepare()
 if '--prepare' in sys.argv:print('Prepared scoped original-cost snapshot and compressed backup.');return
 outputs,data,report=generate()
 REPORT.mkdir(parents=True,exist_ok=True)
 # IMPERIA CW — Cold War: do not overwrite work from another active chat.
 manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
 snapshot=json.loads(BASELINE.read_text(encoding='utf-8'))
 expected=manifest['generated'] if manifest.get('decision_streamlining_revision')==data['decision_streamlining_revision'] else snapshot['hashes']
 for rel in outputs:
  p=ROOT/rel
  actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
  if rel in expected and actual!=expected[rel]:raise RuntimeError('Source changed since snapshot; inspect before installation: '+rel)
 changed=[]
 for rel,text in outputs.items():
  p=ROOT/rel;blob=text.lstrip('\ufeff').encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8')
  if p.exists() and p.read_bytes()==blob:continue
  if not '--dry-run' in sys.argv:
   p.parent.mkdir(parents=True,exist_ok=True);temporary=p.with_name(p.name+'.coldwar_tmp');temporary.write_bytes(blob);temporary.replace(p)
  changed.append(rel)
 previous=json.loads((REPORT/'IMPLEMENTATION_REPORT.json').read_text(encoding='utf-8')) if (REPORT/'IMPLEMENTATION_REPORT.json').exists() else {}
 report['changed_files']=sorted(set(changed)|set(previous.get('changed_files',[]))) if manifest.get('decision_streamlining_revision')==data['decision_streamlining_revision'] else changed
 report['written_files_this_run']=changed;report['dry_run']='--dry-run' in sys.argv
 report['gameplay_tested']=False
 (REPORT/'IMPLEMENTATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 if '--dry-run' not in sys.argv:
  (HERE/'current_design.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
  # Preserve the manifest's unrelated art/adapters and update the scoped files.
  manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
  for rel in outputs:manifest['generated'][rel]=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
  manifest['decision_streamlining_revision']=data['decision_streamlining_revision']
  (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items() if k not in ['retained_events','retained_effects']},indent=2))

if __name__=='__main__':main()
