# IMPERIA COLD WAR — Approved Cyprus replacement snapshot and bounded external archive.
from pathlib import Path
import argparse, datetime, hashlib, json, zipfile

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
ARCHIVE_ROOT=Path('E:/MDColdWar_Backups/Codex_Test_Archives')

def freeze():
 source=ROOT/'docs/cyprus_1970_rework_20261027/concept.json'
 target=HERE/'approved_design.json'
 raw=source.read_bytes()
 if not target.exists():target.write_bytes(raw)
 data=json.loads(target.read_text('utf8'))
 assert data['project']=='IMPERIA COLD WAR' and len(data['focuses'])==100
 return hashlib.sha256(target.read_bytes()).hexdigest()

def archive():
 # Explicit regular-file inventory: no asset traversal, junction following or recursive moves.
 manifest=json.loads((ROOT/'tools/cyprus_1970/manifest.json').read_text('utf8'))
 targets=set(manifest['generated'])
 targets.update(json.loads((ROOT/'tools/cyprus_1970/integration.json').read_text('utf8')))
 targets.update(['common/on_actions/COLDWAR_CYP_1970_regional_on_actions.txt',
  'common/scripted_effects/COLDWAR_CYP_1970_regional_effects.txt',
  'common/scripted_effects/01_NATO_effects.txt','common/scripted_effects/00_money_system.txt',
  'common/ideas/Factions.txt','common/national_focus/COLDWAR_GRE_1970_focus.txt',
  'common/national_focus/turkey.txt','common/national_focus/05_britain.txt',
  'common/on_actions/CYP_on_actions.txt'])
 targets.update(['common/national_focus/mdcw_1970_generic_focus.txt','Claude outputs/COLDWAR_GEN_generator/gen_focus.py',
  'common/scripted_effects/imp_sanctions_effects.txt','common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt',
  'common/decisions/COLDWAR_GRE_1970_tree_decisions.txt','events/COLDWAR_GRE_1970_tree_events.txt'])
 for folder in ['tools/cyprus_1970','tools/greece_1970','tools/eastern_mediterranean_1970']:
  base=ROOT/folder
  if base.is_dir():
   targets.update(p.relative_to(ROOT).as_posix()for p in base.iterdir()
    if p.is_file()and not p.is_symlink()and p.suffix in('.py','.json','.md'))
 assert ARCHIVE_ROOT.as_posix()=='E:/MDColdWar_Backups/Codex_Test_Archives'
 ARCHIVE_ROOT.mkdir(parents=True,exist_ok=True)
 output=ARCHIVE_ROOT/('CYP_before_compact_rework_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.zip')
 hashes={}
 with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED)as z:
  for rel in sorted(targets):
   path=ROOT/rel
   if not path.is_file()or path.is_symlink():continue
   assert path.resolve().is_relative_to(ROOT.resolve()),path
   raw=path.read_bytes();hashes[rel]=hashlib.sha256(raw).hexdigest();z.writestr(rel,raw)
  z.writestr('IMPERIA_COLD_WAR_ARCHIVE.json',json.dumps({'project':'IMPERIA COLD WAR',
   'purpose':'Pre-replacement file backup. No assets or junctions traversed.','files':hashes},indent=2))
 report={'project':'IMPERIA COLD WAR','archive':output.as_posix(),'files':len(hashes),
  'archive_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'approved_design_sha256':freeze()}
 (HERE/'backup.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
 print(json.dumps(report))

def supplemental():
 """Preserve the existing archive record and add one explicitly named shared file."""
 output=ARCHIVE_ROOT/('CYP_sanctions_hook_before_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.zip')
 rel='common/scripted_effects/mdcw_cold_war_effects.txt'
 path=ROOT/rel
 assert path.resolve().is_relative_to(ROOT.resolve()) and not path.is_symlink()
 raw=path.read_bytes()
 with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED)as z:
  z.writestr(rel,raw)
 report={'project':'IMPERIA COLD WAR','purpose':'Supplemental original shared sanctions hook backup.','archive':output.as_posix(),'file':rel,'sha256':hashlib.sha256(raw).hexdigest()}
 (HERE/'supplemental_backup.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
 print(json.dumps(report))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--archive',action='store_true');parser.add_argument('--supplemental',action='store_true');args=parser.parse_args()
 if args.supplemental:supplemental()
 elif args.archive:archive()
 else:print(freeze())
