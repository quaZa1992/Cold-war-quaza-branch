# IMPERIA COLD WAR — Bounded Cyprus replacement and shared MD integration.
from pathlib import Path
import ast, json, re, sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from multiplayer_quality.native_compat import blocks

MARK='# IMPERIA COLD WAR — Compact Cyprus 1970 integration.\n'

def read(rel):return (ROOT/rel).read_text('utf-8-sig')
def write(rel,text):
 if not text.startswith('# IMPERIA COLD WAR'):text=MARK+text
 path=ROOT/rel
 if path.exists()and path.read_text('utf-8-sig')==text:return
 staged=path.with_name(path.name+'.cyprus-staged')
 staged.write_text(text,encoding='utf8',newline='\n')
 staged.replace(path)

def top_block(source,key):
 return next(n for n in blocks(source)if n['key']==key and n['parent']is None)

def add_inside(source,key,marker,body):
 begin=f'# IMPERIA COLD WAR — {marker} BEGIN';end=f'# IMPERIA COLD WAR — {marker} END'
 source=re.sub(re.escape(begin)+r'.*?'+re.escape(end)+r'\n?', '',source,flags=re.S)
 n=top_block(source,key)
 return source[:n['end']-1]+'\n'+begin+'\n'+body+'\n'+end+'\n'+source[n['end']-1:]

def attach_foreign_focuses(source,host):
 """Idempotent post-emission adapter used by both owning host generators."""
 from .foreign_focuses import HOSTS
 design=json.loads((HERE/'approved_design.json').read_text('utf8'))
 if host=='GRE':
  removals=[]
  for n in blocks(source):
   if n['key']not in('focus','shortcut'):continue
   body=source[n['open']+1:n['end']-1]
   ident=re.search(r'\b'+('id'if n['key']=='focus'else'name')+r'\s*=\s*(\S+)',body)
   if not ident:continue
   retired_target=n['key']=='shortcut'and re.search(r'\btarget\s*=\s*COLDWAR_GRE_1970_cyprus_\d+\b',body)
   if re.fullmatch(r'COLDWAR_GRE_1970_cyprus_\d+',ident[1])or retired_target or ident[1]in('COLDWAR_GRE_1970_shortcut_cyprus_crisis','COLDWAR_GRE_1970_shortcut_cyprus_outcome'):
    start=source.rfind('\n',0,n['open'])+1;removals.append((start,n['end']))
  for start,end in sorted(removals,reverse=True):source=source[:start]+source[end:]
  actors=[a for a in design['actor_focuses']if a['tag']=='GRE']
 else:actors=[a for a in design['actor_focuses']if a['tag']in('TUR','ENG')]
 body='\n'.join('shared_focus = '+a['id']for a in actors)
 for tag in sorted({a['tag']for a in actors}):
  first=next(a for a in actors if a['tag']==tag)
  body+='\nshortcut = { name = COLDWAR_CYP_R2_shortcut_'+tag.lower()+' target = '+first['id']+' scroll_wheel_factor = 0.8 }'
 return add_inside(source,'focus_tree','Cyprus guarantor imports',body)

def patch_owning_generators():
 # Greece keeps its complete non-Cyprus source design and reward revisions.
 assert 'prepare_greek_design' in read('tools/greece_1970/compile.py'),'Greek canonical retirement adapter is missing.'
 rel='Claude outputs/COLDWAR_GEN_generator/gen_focus.py';s=read(rel)
 if 'Compact Cyprus shared-focus imports'not in s:
  needle="    return _repair_grants('GENERIC1970',text)";assert needle in s
  s=s.replace(needle,"    # IMPERIA COLD WAR — Compact Cyprus shared-focus imports.\n    import sys\n    from pathlib import Path\n    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))\n    from cyprus_1970_rework.integration import attach_foreign_focuses\n    return attach_foreign_focuses(_repair_grants('GENERIC1970', text), 'GENERIC')",1)
  write(rel,s)
 # The obsolete large compiler can no longer resurrect its daily observer or decision menus.
 write('tools/cyprus_1970/compile.py',MARK+'''"""Retired large-tree entry point. Compile the approved compact replacement."""
from pathlib import Path
import runpy
import sys
target = Path(__file__).resolve().parents[1] / 'cyprus_1970_rework' / 'compile.py'
sys.path.insert(0, str(target.parent))
if '--check' not in sys.argv and '--install' not in sys.argv:
    sys.argv.append('--install')
runpy.run_path(str(target), run_name='__main__')
''')
 # Keep Cyprus's existing historical commander mapping, but schedule it through the new monthly owner.
 rel='tools/eastern_mediterranean_1970/compile.py';s=read(rel)
 needle="self.write(f'common/on_actions/COLDWAR_{tag}_1970_regional_on_actions.txt'"
 if '# CYP R2 MONTHLY ROSTER OWNER'not in s:
  pos=s.find(needle);assert pos>=0
  # Hook the central file writer rather than changing the unrelated Greek/Turkish roster loops.
  m=re.search(r'(?m)^    def write\(self,\s*(\w+),\s*(\w+)[^\n]*:',s);assert m
  relvar,textvar=m[1],m[2]
  s=s[:m.end()]+f"\n        # IMPERIA COLD WAR — CYP R2 MONTHLY ROSTER OWNER\n        if str({relvar}) == 'common/on_actions/COLDWAR_CYP_1970_regional_on_actions.txt':\n            {textvar} = '# IMPERIA COLD WAR — Cyprus roster is reconciled by the compact monthly owner.\\n'"+s[m.end():]
  write(rel,s)

def patch_native_entrypoints():
 rel='common/bookmarks/blitzkrieg.txt';s=read(rel)
 for old,new in [('republic_at_ten','republic'),('intercommunal_talks','talks'),('command_review','guard')]:
  s=s.replace('COLDWAR_CYP_1970_'+old,'COLDWAR_CYP_R2_'+new)
 write(rel,s)
 rel='history/countries/CYP - Cyprus.txt';s=read(rel).replace('COLDWAR_CYP_1970_initialize = yes','COLDWAR_CYP_R2_initialize = yes');write(rel,s)
 rel='common/scripted_effects/00_leader_setup_scripted_effects.txt';s=read(rel).replace('COLDWAR_CYP_1970_set_leader = yes','COLDWAR_CYP_R2_set_leader = yes');write(rel,s)
 # The existing tree ID intentionally remains stable, so fallback selection needs no redesign.
 rel='common/scripted_effects/00_money_system.txt';s=read(rel)
 for key,body in [
  ('calculate_additional_income_rate','COLDWAR_CYP_R2_calculate_weekly_streams = yes\nadd_to_variable = { additional_income_rate = COLDWAR_CYP_R2_weekly_income }'),
  ('calculate_additional_expense_rate','COLDWAR_CYP_R2_calculate_weekly_streams = yes\nadd_to_variable = { additional_expenses_rate = COLDWAR_CYP_R2_weekly_expenses }')]:
  s=add_inside(s,key,'Cyprus weekly '+('income'if'income'in key else'expenses'),body)
 write(rel,s)
 # Existing Imperia callbacks run after the native mirrored sanction arrays change.
 # Their scope is the target, ROOT is the sender. This is an event callback, not polling.
 rel='common/scripted_effects/mdcw_cold_war_effects.txt';s=read(rel)
 body='''if = { limit = {
 country_exists = CYP
 OR = { original_tag = CYP ROOT = { original_tag = CYP } }
 CYP = { has_country_flag = COLDWAR_CYP_R2_initialized }
 }
 CYP = { COLDWAR_CYP_R2_agreements_reconcile = yes }
}'''
 for key in('mdcw_cw_on_sanction_imposed','mdcw_cw_on_sanction_lifted'):
  s=add_inside(s,key,'Cyprus agreement sanction transition',body)
 write(rel,s)
 # Entry guards wrap the actual existing native helper bodies and retain all upstream integrations.
 rel='common/scripted_effects/01_NATO_effects.txt';s=read(rel)
 for key in('NATO_join','NATO_join_via_event'):
  n=top_block(s,key);body=s[n['open']+1:n['end']-1]
  if '# CYP R2 TEMPORARY SEPARATION GUARD'not in body:
   wrapped='\n# IMPERIA COLD WAR — CYP R2 TEMPORARY SEPARATION GUARD\nif = {\n limit = { COLDWAR_CYP_R2_nato_join_allowed = yes }\n'+body+'\n}\n'
   s=s[:n['open']+1]+wrapped+s[n['end']-1:]
 write(rel,s)
 # A direct idea grant must not restore a temporarily separated combatant before peace.
 rel='common/ideas/Factions.txt';s=read(rel)
 owner=next(n for n in blocks(s)if n['key']=='NATO_member')
 n=next(n for n in blocks(s)if n['key']=='on_add'and n['open']>owner['open']and n['end']<owner['end'])
 body=s[n['open']+1:n['end']-1]
 if '# CYP R2 MEMBERSHIP ENTRY GUARD'not in body:
  wrapped='\n# IMPERIA COLD WAR — CYP R2 MEMBERSHIP ENTRY GUARD\nif = { limit = { COLDWAR_CYP_R2_nato_join_allowed = yes }\n'+body+'\n} else = { NATO_leave = yes }\n'
  s=s[:n['open']+1]+wrapped+s[n['end']-1:]
 write(rel,s)

def retire_legacy():
 # Retain dynamic party names and all Northern Cyprus identities, never the old focus programmes.
 rel='localisation/english/COLDWAR_CYP_1970_l_english.yml';s=read(rel)
 rows=[]
 for line in s.splitlines():
  m=re.match(r'\s*(\w+):',line)
  if m and(m[1].startswith('COLDWAR_CYP_1970_party_')or m[1].startswith('COLDWAR_NCY_1970_')):
   # No invented Cypriot religious party organizations in dormant MD slots.
   if re.match(r'COLDWAR_CYP_1970_party_(8|9|10|11|12)(?:_|$)',m[1])and not m[1].endswith('_icon'):
    value='No organized party'if not m[1].endswith('_desc')else'No organized party represents this programme in Cyprus.'
    line=' '+m[1]+':0 '+json.dumps(value)
   rows.append(line)
 (ROOT/rel).write_text('l_english:\n# IMPERIA COLD WAR — Retained dated Cypriot and Turkish Cypriot party identities.\n'+'\n'.join(rows)+'\n',encoding='utf-8-sig')
 retired=['common/game_rules/COLDWAR_CYP_1970_rules.txt','common/on_actions/COLDWAR_CYP_1970_on_actions.txt',
  'common/scripted_effects/COLDWAR_CYP_1970_effects.txt','common/scripted_triggers/COLDWAR_CYP_1970_triggers.txt',
  'common/ideas/COLDWAR_CYP_1970_ideas.txt','common/dynamic_modifiers/COLDWAR_CYP_1970_modifiers.txt',
  'events/COLDWAR_CYP_1970_events.txt','common/decisions/COLDWAR_CYP_1970_decisions.txt',
  'common/decisions/categories/COLDWAR_CYP_1970_categories.txt','interface/COLDWAR_CYP_1970_ideas.gfx']
 for rel in retired:
  path=ROOT/rel
  assert path.resolve().is_relative_to(ROOT.resolve()),path
  if path.is_file():path.unlink()
 write('common/on_actions/COLDWAR_CYP_1970_regional_on_actions.txt',MARK+'# Regional commander updates are invoked by COLDWAR_CYP_R2_core_monthly.\n')
 return retired

def install(meta):
 if not(HERE/'backup.json').exists():raise RuntimeError('External pre-replacement archive must exist before installation.')
 patch_owning_generators()
 for host in('GRE','GENERIC'):
  rel='common/national_focus/'+('COLDWAR_GRE_1970_focus.txt'if host=='GRE'else'mdcw_1970_generic_focus.txt')
  write(rel,attach_foreign_focuses(read(rel),host))
 patch_native_entrypoints()
 from .greek_cleanup import retire_generated_cyprus
 retire_generated_cyprus(ROOT)
 retired=retire_legacy()
 return {'project':'IMPERIA COLD WAR','retired':retired,'foreign_imports':16,'monthly_only':True}
