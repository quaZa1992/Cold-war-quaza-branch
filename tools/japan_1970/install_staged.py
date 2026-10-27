# IMPERIA CW — Cold War: Japan 1970 staged-content installer.
"""Install reviewed fragments without touching existing shared scripts.

The caller must separately integrate the 1970 Japan history and fallback tree.
Run without --apply for a read-only destination check.
"""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
stage = Path(__file__).resolve().parent / 'staging'
foreign = stage / 'foreign'
targets = [
    (stage / 'graph/focus_tree.txt', 'common/national_focus/COLDWAR_JAP_1970_focus.txt'),
    (stage / 'graph/focus_l_english.yml', 'localisation/english/COLDWAR_JAP_1970_focus_l_english.yml'),
    (stage / 'national_economy_focus_effects_scripted_effects.txt', 'common/scripted_effects/COLDWAR_JAP_1970_national_economy.txt'),
    (stage / 'national_economy_focus_effects_dynamic_modifiers.txt', 'common/dynamic_modifiers/COLDWAR_JAP_1970_national_economy.txt'),
    (stage / 'national_economy_focus_effects_l_english.yml', 'localisation/english/COLDWAR_JAP_1970_national_economy_l_english.yml'),
    (stage / 'constitution/effects.txt', 'common/scripted_effects/COLDWAR_JAP_1970_constitution_rewards.txt'),
    (stage / 'constitution/ideas.txt', 'common/ideas/COLDWAR_JAP_1970_constitution_climate.txt'),
    (stage / 'constitution/localisation.yml', 'localisation/english/COLDWAR_JAP_1970_constitution_climate_l_english.yml'),
    (stage / 'COLDWAR_JAP_1970_okinawa_idea.txt', 'common/ideas/COLDWAR_JAP_1970_okinawa.txt'),
    (stage / 'COLDWAR_JAP_1970_okinawa_l_english.yml', 'localisation/english/COLDWAR_JAP_1970_okinawa_l_english.yml'),
]
for name in ('bilateral_effects', 'foreign_effects', 'multilateral_invitation_effects', 'multilateral_project_effects'):
    filename = f'COLDWAR_JAP70_{name}.txt'
    targets.append((foreign / filename, 'common/scripted_effects/' + filename))
for name in ('bilateral_events', 'multilateral_invitation_events'):
    filename = f'COLDWAR_JAP70_{name}.txt'
    targets.append((foreign / filename, 'events/' + filename))
for name in ('bilateral_ideas', 'foreign_ideas', 'multilateral_invitation_ideas'):
    filename = f'COLDWAR_JAP70_{name}.txt'
    targets.append((foreign / filename, 'common/ideas/' + filename))
for name in ('dynamic_modifiers', 'multilateral_invitation_dynamic_modifiers', 'project_dynamic_modifiers'):
    filename = f'COLDWAR_JAP70_{name}.txt'
    targets.append((foreign / filename, 'common/dynamic_modifiers/' + filename))
for name in ('bilateral_opinion_modifiers', 'multilateral_invitation_opinions'):
    filename = f'COLDWAR_JAP70_{name}.txt'
    targets.append((foreign / filename, 'common/opinion_modifiers/' + filename))
for name in ('foreign_project_decisions', 'multilateral_invitation_decisions'):
    filename = f'COLDWAR_JAP70_{name}.txt'
    targets.append((foreign / filename, 'common/decisions/' + filename))
for filename in ('COLDWAR_JAP70_foreign_projects_category.txt', 'COLDWAR_JAP70_multilateral_invites_category.txt'):
    targets.append((foreign / 'categories' / filename, 'common/decisions/categories/' + filename))
for name in ('bilateral', 'foreign', 'multilateral_invitation', 'diplomatic_reports'):
    filename = f'COLDWAR_JAP70_{name}_l_english.yml'
    targets.append((foreign / filename, 'localisation/english/' + filename))
targets += [
    (foreign/'scripted_effects/COLDWAR_JAP70_diplomatic_reports.txt','common/scripted_effects/COLDWAR_JAP70_diplomatic_reports.txt'),
    (foreign/'events/COLDWAR_JAP70_diplomatic_reports.txt','events/COLDWAR_JAP70_diplomatic_reports.txt'),
    (foreign/'COLDWAR_JAP70_diplomatic_recovery.txt','common/on_actions/COLDWAR_JAP70_diplomatic_recovery.txt'),
]

missing = [str(src) for src, _ in targets if not src.is_file()]
collisions = [dest for _, dest in targets if (root / dest).exists()]
if missing or collisions:
    for item in missing:
        print('Missing source:', item)
    for item in collisions:
        print('Existing destination:', item)
    raise SystemExit(1)
if '--apply' in sys.argv:
    for src, dest in targets:
        (root / dest).write_bytes(src.read_bytes())
    print(f'Installed {len(targets)} new files; shared history and fallback still require integration.')
else:
    print(f'{len(targets)} staged files have new, available destinations; no files installed.')
