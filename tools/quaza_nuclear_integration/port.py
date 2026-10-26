# IMPERIA CW — Cold War: selective quaZa uranium and raid integration.
"""Apply only the reviewed feature delta, retaining local Cold War changes.

The installed main MD is the common ancestor. Every applied file is backed up
outside the runtime directories. Ambiguous edits fail closed for manual review.
"""
from pathlib import Path
import difflib
import hashlib
import json
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
BASE = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
SOURCE = Path('E:/SteamLibrary/steamapps/workshop/content/394360/3818306694')
AUDIT = ROOT / 'docs/quaza_nuclear_integration'
MARKER = '# IMPERIA CW — Cold War: quaZa uranium supply chain and raid integration.'

SHARED = '''common/resources/00_resources.txt
common/buildings/00_buildings.txt
common/scripted_effects/!_energy_effects.txt
common/scripted_effects/00_money_system.txt
common/scripted_effects/00_resource_storage_effects.txt
common/scripted_effects/99_AI_investment_scripted_effects.txt
common/scripted_effects/99_investment_scripted_effects.txt
common/scripted_effects/BI_dynamic_topbar_effects.txt
common/scripted_guis/00_resource_storage_gui.txt
common/scripted_guis/01_investment_scripted_gui.txt
common/scripted_localisation/00_investment_scripted_localisation.txt
common/scripted_localisation/00_resource_storage_scripted_localisation.txt
common/scripted_triggers/00_investment_scripted_triggers.txt
common/synchronized_dynamic_tokens/MD_tokens.txt
common/technologies/industry.txt
common/special_projects/projects/naval_projects.txt
common/special_projects/projects/nuclear_projects.txt
common/units/equipment/MD_ballistic_missiles.txt
common/units/equipment/MD_nuclear_missiles.txt
common/units/equipment/modules/MD_ship_modules.txt
interface/countryproductionlineview.gui
interface/countrystateview.gfx
interface/countrytradeview.gui
interface/general_stuff.gfx
interface/MD_countryeconomyview.gui
interface/MD_dynamic_topbar.gfx
interface/MD_investments.gui
interface/resource_storage.gui
interface/military_raids/MD_military_raids.gfx
events/investments_events.txt
localisation/english/0_energy_l_english.yml
localisation/english/MD_money_l_english.yml
localisation/english/MD_dynamic_topbar_l_english.yml
localisation/english/replace/replaced_from_vanilla_buildings_l_english.yml
common/raids/air_raids.txt
common/raids/cruise_missile_strike.txt
common/raids/naval_raids.txt
common/raids/drone_strike_raids.txt
common/raids/special_forces_raids.txt'''.splitlines()

DEDICATED = '''common/ai_strategy/imp_nuclear_ai.txt
common/dynamic_modifiers/imp_nuclear_programme_dynamic_modifiers.txt
common/dynamic_modifiers/imp_uranium_dynamic_modifiers.txt
common/map_modes/imp_uranium_map_mode.txt
common/modifier_definitions/imp_uranium_modifier_definitions.txt
common/on_actions/zzzzzz_imp_nuclear_programme_on_actions.txt
common/on_actions/zzzzzz_imp_uranium_on_actions.txt
common/scripted_effects/imp_nuclear_ai_effects.txt
common/scripted_effects/imp_uranium_effects.txt
common/scripted_triggers/imp_nuclear_ai_triggers.txt
common/scripted_triggers/imp_raid_triggers.txt
interface/imp_uranium.gfx
localisation/english/imp_nuclear_programme_l_english.yml
localisation/english/imp_uranium_l_english.yml'''.splitlines()

def read(path):
    return path.read_text(encoding='utf-8-sig')

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    data=text.encode('utf-8-sig' if path.suffix == '.yml' else 'utf-8')
    for attempt in range(20):
        try:
            path.write_bytes(data)
            return
        except OSError as error:
            if error.errno not in (13,22) or attempt==19:raise
            time.sleep(0.15)

def backup(rel):
    path = ROOT / rel
    dest = AUDIT / 'before' / rel
    if path.exists() and not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(path.read_bytes())

def selected(rel, old, new):
    text = '\n'.join(new)
    # Uranium-specific resource costs only; retain local equipment balance and
    # do not introduce the unrelated modern Burevestnik variant.
    if 'units/equipment/' in rel:
        return 'uranium' in text and 'imp_sov_burestnevik' not in text
    if rel == 'common/scripted_effects/00_money_system.txt':
        return 'uranium' in text and 'nuclear_forces_cost' not in text
    if rel == 'localisation/english/MD_money_l_english.yml':
        return 'uranium' in text
    if rel.endswith('replaced_from_vanilla_buildings_l_english.yml'):
        return 'uranium' in text
    return any(k in text.lower() for k in ['uranium', 'enrichment', 'imp_raid_', 'imp_ai_raid_', 'imp_nuclear_'])

def candidates(lines, snippet):
    return [i for i in range(len(lines)-len(snippet)+1) if lines[i:i+len(snippet)] == snippet]

def locate(current, base, i, j):
    # Match the old region with stable surrounding lines; shorten independently
    # because Cold War frequently inserts guards just before the edited region.
    for context in range(6, 0, -1):
        for left, right in [(context,context),(context,0),(0,context)]:
            start, end = max(0,i-left), min(len(base),j+right)
            hits = candidates(current, base[start:end])
            if len(hits) == 1:
                pos = hits[0] + i-start
                return pos
    return None

def main():
    apply = '--apply' in sys.argv
    report = []
    for rel in SHARED:
        base, source, current = read(BASE/rel).splitlines(), read(SOURCE/rel).splitlines(), read(ROOT/rel).splitlines()
        changes = []
        for tag,i,j,a,b in difflib.SequenceMatcher(None,base,source,autojunk=False).get_opcodes():
            if tag == 'equal' or not selected(rel,base[i:j],source[a:b]):
                continue
            pos = locate(current,base,i,j)
            if pos is None:
                changes.append({'status':'manual','base_line':i+1,'old':base[i:j],'new':source[a:b]})
                continue
            indent = re.match(r'\s*',source[a] if a < b else base[i]).group()
            replacement = [indent+MARKER] + source[a:b]
            current[pos:pos+j-i] = replacement
            changes.append({'status':'applied','base_line':i+1,'new_lines':b-a})
        if changes:
            if apply:
                backup(rel)
                write(ROOT/rel,'\n'.join(current)+'\n')
            report.append({'file':rel,'changes':changes})
    if apply:
        for rel in DEDICATED:
            p=Path(rel)
            dest=p.with_name('COLDWAR_quaza_'+p.name)
            assert not (ROOT/dest).exists(), dest
            write(ROOT/dest, MARKER+'\n# Adapted from quaZa Feature Test, workshop 3818306694.\n'+read(SOURCE/rel))
            report.append({'file':dest.as_posix(),'copied_from':rel})
    AUDIT.mkdir(parents=True,exist_ok=True)
    write(AUDIT/('port_report.json' if apply else 'dry_run.json'),json.dumps(report,indent=2,ensure_ascii=False))
    print('Files:',len(report),'Applied changes:',sum(c['status']=='applied' for r in report for c in r.get('changes',[])))
    for r in report:
        for c in r.get('changes',[]):
            if c['status']=='manual':print('MANUAL',r['file'],c['base_line'],'old:',repr('\n'.join(c['old'])[:100]),'new:',repr('\n'.join(c['new'])[:160]))

if __name__ == '__main__':main()
