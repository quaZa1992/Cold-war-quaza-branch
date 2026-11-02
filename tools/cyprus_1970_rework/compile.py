# IMPERIA COLD WAR — Compile and install the approved compact Cyprus replacement.
"""Pure generation by default. --install performs the archived, bounded integration."""
from pathlib import Path
import argparse, hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse
from multiplayer_quality.native_compat import normalize
from cyprus_1970_rework import core, agreements, crisis, foreign_focuses, layout, art
from cyprus_1970_rework.integration import install

HEADER='# IMPERIA COLD WAR — Compact Cyprus runtime wiring.\n\n'
P='COLDWAR_CYP_R2_'

def wiring(design,agreement_meta):
 """One cheap monthly dispatch; native weekly bookkeeping only reads cached eligibility."""
 loc={P+'shortcut_gre':'Cyprus: Greece',P+'shortcut_tur':'Cyprus: Turkey',P+'shortcut_eng':'Cyprus: United Kingdom'}
 helpers={
  P+'calculate_weekly_streams':f'''{P}core_weekly_streams = yes
{P}agreements_weekly_streams = yes
{P}crisis_weekly_streams = yes
set_variable = {{ {P}weekly_income = {P}deal_weekly_income }}
set_variable = {{ {P}weekly_expenses = {P}core_weekly_expenses }}
add_to_variable = {{ {P}weekly_expenses = {P}deal_weekly_expenses }}
add_to_variable = {{ {P}weekly_expenses = {P}crisis_weekly_expenses }}''',
  P+'monthly':f'''{P}core_monthly = yes
{P}agreements_clear_expired_offers = yes
{P}agreements_reconcile = yes
{P}crisis_monthly = yes''',
  P+'relationship_changed':f'''if = {{ limit = {{ country_exists = CYP CYP = {{ has_country_flag = {P}initialized }} }}
 CYP = {{ {P}agreements_reconcile = yes {P}crisis_reconcile = yes {P}refresh_programmes = yes }}
}}
else = {{ {P}missing_cyprus_cleanup = yes {P}crisis_reconcile = yes }}''',
 }
 cleanup=[]
 for key,deal in design['offers'].items():
  for tag in deal['recipients']:
   cleanup.append(f'{tag} = {{ if = {{ limit = {{ exists = yes }} remove_ideas = {P}{key}_{tag.lower()} clr_country_flag = {P}{key}_active }} }}')
 helpers[P+'missing_cyprus_cleanup']='if = { limit = { NOT = { country_exists = CYP } }\n'+'\n'.join(cleanup)+'\n}'
 # Hooks explicitly target the named actors, not a recurring every-country relationship scan.
 on=f'''on_actions = {{
 on_startup = {{ effect = {{
  if = {{ limit = {{ country_exists = CYP }} CYP = {{ {P}initialize = yes {P}monthly = yes }} }}
 }} }}
 on_monthly = {{ effect = {{
  if = {{ limit = {{ original_tag = CYP IMP_is_1970_scenario = yes }} {P}monthly = yes }}
  if = {{ limit = {{ original_tag = USA IMP_is_1970_scenario = yes NOT = {{ country_exists = CYP }} }} {P}relationship_changed = yes }}
 }} }}
 on_war_relation_added = {{ effect = {{
  if = {{ limit = {{ OR = {{ original_tag = CYP original_tag = GRE original_tag = TUR FROM = {{ OR = {{ original_tag = CYP original_tag = GRE original_tag = TUR }} }} }} }} {P}relationship_changed = yes }}
 }} }}
 on_peaceconference_ended = {{ effect = {{ {P}relationship_changed = yes }} }}
 on_annex = {{ effect = {{ {P}relationship_changed = yes }} }}
 on_puppet = {{ effect = {{ {P}relationship_changed = yes }} }}
 on_subject_free = {{ effect = {{ {P}relationship_changed = yes }} }}
}}
'''
 files={'common/scripted_effects/COLDWAR_CYP_R2_wiring.txt':HEADER+'\n\n'.join(core.block(k,v)for k,v in helpers.items())+'\n',
  'common/on_actions/zzzzzz_COLDWAR_CYP_R2_on_actions.txt':HEADER+on}
 return {'files':files,'loc':loc,'meta':{'periodic':'monthly','weekly':'native money arithmetic only','archive':'tools/cyprus_1970_rework/backup.json'}}

def generate():
 design=json.loads((HERE/'approved_design.json').read_text('utf8'))
 design=layout.apply(design)
 design=art.apply(design)
 a=agreements.build(design)
 design['core_event_picture']=a['meta']['core_event_picture']
 parts=[('agreements',a),('art',art.build(design)),('core',core.build(design)),('crisis',crisis.build(design)),('foreign_focuses',foreign_focuses.build(design)),('wiring',wiring(design,a['meta']))]
 files={};loc={};meta={}
 for name,result in parts:
  meta[name]=result['meta']
  for rel,text in result['files'].items():
   if rel in files:raise ValueError('Duplicate runtime file '+rel)
   files[rel]=normalize(text,rel)
  for key,value in result['loc'].items():
   if key in loc and loc[key]!=value:raise ValueError('Conflicting localisation '+key+': '+repr((loc[key],value)))
   loc[key]=value
 files['localisation/english/COLDWAR_CYP_R2_l_english.yml']='l_english:\n# IMPERIA COLD WAR — Compact Cyprus 1970 replacement.\n'+'\n'.join(' '+key+':0 '+json.dumps(value,ensure_ascii=False)for key,value in sorted(loc.items()))+'\n'
 definitions=set();calls=set()
 for rel,text in files.items():
  if rel.endswith(('.txt','.gfx','.gui')):
   parse(text)
   if not text.startswith('# IMPERIA COLD WAR'):raise ValueError('Missing marker '+rel)
  if rel.startswith(('common/scripted_effects/','common/scripted_triggers/')):
   definitions.update(re.findall(r'(?m)^\s*(COLDWAR_CYP_R2_\w+)\s*=\s*\{',text))
  if rel.endswith('.txt'):calls.update(re.findall(r'\b(COLDWAR_CYP_R2_\w+)\s*=\s*yes\b',text))
 unresolved=sorted(calls-definitions)
 if unresolved:raise ValueError('Unresolved Cyprus helpers: '+', '.join(unresolved))
 text=files['common/national_focus/COLDWAR_CYP_1970_focus.txt']
 count=len(re.findall(r'\bid\s*=\s*COLDWAR_CYP_R2_',text));assert count==100,count
 for rel,text in files.items():
  for key in re.findall(r'\b(?:custom_effect_tooltip|title|desc|name)\s*=\s*(COLDWAR_CYP_R2_[A-Za-z0-9_.]+)',text):
   if key not in loc and not key.endswith('_focus'):raise ValueError('Missing English key '+key+' in '+rel)
 return design,files,loc,meta

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
 design,files,loc,meta=generate()
 report={'project':'IMPERIA COLD WAR','focuses':100,'foreign_focuses':16,'generated_files':list(files),'localisation_keys':len(loc),
  'approved_design_sha256':hashlib.sha256((HERE/'approved_design.json').read_bytes()).hexdigest(),'script_parse':'passed','installed':False,'engine_tested':False,'meta':meta}
 if args.install:
  if not(HERE/'backup.json').exists():raise RuntimeError('External archive required before replacement.')
  for rel,text in files.items():
   path=ROOT/rel;path.parent.mkdir(parents=True,exist_ok=True)
   if path.exists()and path.read_text('utf-8-sig')==text:continue
   staged=path.with_name(path.name+'.cyprus-staged')
   staged.write_text(text,encoding='utf-8-sig'if rel.endswith('.yml')else'utf8',newline='\n')
   staged.replace(path)
  report['integration']=install(meta)
  report['installed']=True
 destination=HERE/('manifest.json'if args.install else 'GENERATION_CHECK.json')
 destination.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps({k:report[k]for k in('focuses','foreign_focuses','localisation_keys','script_parse','installed')}))

if __name__=='__main__':main()
