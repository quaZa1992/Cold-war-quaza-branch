# IMPERIA COLD WAR — Reproducible Codex skill metadata and upstream attribution.
"""Refresh packaging metadata without rewriting authored skill instructions."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SKILLS = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
MARKER = '# IMPERIA COLD WAR — '

# name, UI title, short UI description, upstream skill names, domain references
CATALOGUE = [
    ('mdcw-leaders', 'Cold War Leaders', 'Historical 1970 commanders and advisers', ['add-leader'], ['content-guidelines', 'oob-variants-reference']),
    ('mdcw-economy-streams', 'Cold War Fiscal Streams', 'Weekly income, expenses and fiscal transactions', ['additional-income'], ['dynamic-modifier-tooltips', 'energy-power-balance', 'md-custom-modifiers']),
    ('mdcw-edge-case-review', 'Cold War Edge Cases', 'Scope, timing, replay and multiplayer failure cases', ['adversarial-review'], ['bug-patterns', 'known-false-positives', 'scripting-edge-cases', 'hoi4-data-structures']),
    ('mdcw-quality-audit', 'Cold War Quality Audit', 'Mechanics quality, performance and MP evidence', ['audit'], ['agent-conventions', 'bug-patterns', 'performance-patterns', 'regression-test-scope', 'un-system-reference']),
    ('mdcw-changelog', 'Cold War Changelog', 'Verified English changelog and release notes', ['changelog'], ['localisation-rules']),
    ('mdcw-github-workflow', 'Cold War GitHub Workflow', 'Scoped issue fixes, draft PRs and requested closures', ['fix-issue', 'open-pr', 'close-issue'], ['agent-conventions']),
    ('mdcw-content-review', 'Cold War Content Review', 'Historical fit, rewards and native MD presentation', ['content-review'], ['content-guidelines', 'idea-reference', 'mio-reference', 'focus-tree-reference']),
    ('mdcw-country-ai', 'Cold War Country AI', '1970 AI paths, crisis cures and human RP agency', ['country-ai-path'], ['ai-strategy-reference', 'ai-equipment-reference', 'oob-variants-reference']),
    ('mdcw-dev-diaries', 'Cold War Dev Diaries', 'English development diaries with accurate media', ['dev-diary-mdx'], ['localisation-rules']),
    ('mdcw-lifecycle-check', 'Cold War Readiness', 'Country integration and 1970 readiness checks', ['lifecycle-check'], ['content-guidelines', 'entity-system', 'formable-reference']),
    ('mdcw-tick-profiler', 'Cold War Tick Workload', 'Trace recurring script work and native timing limits', ['md-tick-profiler'], ['performance-patterns']),
    ('mdcw-namelists', 'Cold War Unit Names', 'Historical formation, ship and squadron name lists', ['new-namelist'], ['namelist-reference', 'oob-variants-reference']),
    ('mdcw-party-names', 'Cold War Party Identity', '1970 parties, native slots and identity transitions', ['party-names'], ['party-loc-reference', 'localisation-rules']),
    ('mdcw-rework-brief', 'Cold War Rework Briefs', 'Researched country and mechanic design briefs', ['rework-brief'], ['content-guidelines']),
    ('mdcw-search-filters', 'Cold War Focus Filters', 'Focus search tags and actual spending AI guards', ['search-filter-check'], ['search-filters']),
    ('mdcw-localisation', 'Cold War English Text', 'English localisation, dynamic text and spirit paths', ['spirit-removal-desc'], ['localisation-rules', 'loc-smoke-checklist', 'typo-watchlist', 'party-loc-reference']),
    ('mdcw-standardize', 'Cold War Standardization', 'Format specified scripts while preserving semantics', ['standardize'], ['refactor-checklist', 'simplification-patterns']),
    ('mdcw-test-plan', 'Cold War MP Test Plans', 'Concrete 1970 playthrough and multiplayer rehearsals', ['test-plan'], ['debug-commands', 'regression-test-scope']),
    ('mdcw-maintain-skills', 'Cold War Skill Maintenance', 'Maintain scoped skills from verified project lessons', ['update-claude'], ['agent-conventions', 'documentation-references']),
    ('mdcw-validate', 'Cold War Validation', 'Available checks and complete diagnostic artifacts', ['validate', 'warnings'], ['validation-pipeline', 'validator-check-notes', 'known-false-positives']),
    ('mdcw-events-decisions', 'Cold War Events and Deals', 'Event routing, decisions and recipient-approved deals', [], ['event-reference', 'decision-reference', 'diplomatic-action-reference', 'faction-rules', 'un-system-reference']),
    ('mdcw-scripted-gui', 'Cold War Native GUI', 'Native minigame interfaces, scope and click safety', [], ['scripted-gui-rules', 'scripted-gui-patterns', 'meta-effect-patterns', 'map-mode-reference']),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    inventory = json.loads((HERE / 'upstream_inventory.json').read_text(encoding='utf-8'))
    commit = inventory['commit']
    blobs = {entry['path']: entry for entry in inventory['entries']}
    generator = SKILLS / '.system/skill-creator/scripts/generate_openai_yaml.py'
    environment = dict(os.environ)
    environment['PYTHONUTF8'] = '1'
    # Existing, locally recorded PyYAML dependency; no package install is needed.
    yaml_dependency = ROOT / 'tools/preference_updates/20261023/validator_dependencies'
    environment['PYTHONPATH'] = str(yaml_dependency) + os.pathsep + environment.get('PYTHONPATH', '')
    mapping = []
    for name, title, short, upstream, docs in CATALOGUE:
        folder = HERE / 'skills' / name
        assert (folder / 'SKILL.md').is_file(), name
        sources = [f'.claude/skills/{skill}/SKILL.md' for skill in upstream]
        sources += [f'.claude/docs/{doc}.md' for doc in docs]
        if name == 'mdcw-country-ai':
            sources += ['.claude/skills/country-ai-path/references/audit.md', '.claude/skills/country-ai-path/references/write.md']
        if name == 'mdcw-tick-profiler':
            sources += ['.claude/skills/md-tick-profiler/references/reading-the-flamegraph.md']
        if name == 'mdcw-events-decisions':
            sources.append('.claude/agents/event-builder.md')
        if name == 'mdcw-quality-audit':
            sources += [entry['path'] for entry in inventory['entries'] if entry['path'].startswith('.claude/agents/')]
        source_lines = []
        for path in sorted(set(sources)):
            assert path in blobs, path
            source_lines.append(f'- [{path}](https://github.com/MillenniumDawn/Millennium-Dawn/blob/{commit}/{path}), SHA-256 `{blobs[path]["sha256"]}`.')
        notice = (
            f'# IMPERIA COLD WAR — {title} source and adaptation\n\n'
            f'Source: MillenniumDawn/Millennium-Dawn, commit `{commit}`, retrieved 24 October 2026. '
            'Credit: the Millennium Dawn contributors. Individual authors of these instruction files are unknown in the reviewed snapshot.\n\n'
            f'Upstream repository licence: [CC BY-SA 4.0](https://github.com/MillenniumDawn/Millennium-Dawn/blob/{commit}/LICENSE). '
            'This adapted instructional text is also offered under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). '
            'No endorsement is implied. This applies to this skill, not the mod, third-party game assets or unrelated installed skills.\n\n'
            'Adapted for Codex, January 1970, Cold War multiplayer RP, the actual local toolchain and the current IMPERIA COLD WAR project standards. '
            'Claude tool/model declarations, automatic agent dispatch, upstream repository publication defaults and conflicting modern scenario rules are not imported. '
            'New wording and project-specific corrections were prepared with Codex assistance for Enes.\n\n'
            'Reviewed sources:\n\n' + '\n'.join(source_lines) + '\n'
        )
        references = folder / 'references'
        references.mkdir(exist_ok=True)
        (references / 'source.md').write_text(notice, encoding='utf-8', newline='\n')
        result = subprocess.run([
            sys.executable, '-X', 'utf8', str(generator), str(folder),
            '--interface', f'display_name={title}',
            '--interface', f'short_description={short}',
            '--interface', f'default_prompt=Use ${name} for the specified IMPERIA COLD WAR 1970 task, following current project standards.',
        ], env=environment, capture_output=True, text=True, encoding='utf-8')
        if result.returncode:
            raise RuntimeError(name + ': ' + result.stdout + result.stderr)
        ui = folder / 'agents/openai.yaml'
        ui.write_text(MARKER + title + ' discovery metadata.\n' + ui.read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
        mapping.append({'skill': name, 'upstream_skills': upstream, 'upstream_sources': sorted(set(sources)), 'kind': 'new'})

    # Small update to the existing skill, preserving every other installed resource.
    name = 'mdcw-national-trees'
    update = HERE / 'updates' / name
    update.mkdir(parents=True, exist_ok=True)
    installed = SKILLS / name / 'SKILL.md'
    text = installed.read_text(encoding='utf-8')
    original_title = '# IMPERIA COLD WAR: National focus authoring'
    replacement = MARKER + 'National focus authoring'
    assert text.count(original_title) == 1 or text.count(replacement) == 1
    text = text.replace(original_title, replacement, 1)
    pointer = '\nFor a specifically requested new-tree scaffold, read [1970 scaffolding](references/md-upstream-scaffolding.md). It adapts upstream MD setup to this project without imposing modern filenames, placeholders or unrelated branch approval.\n'
    if 'references/md-upstream-scaffolding.md' not in text:
        anchor = '\n## Establish the assignment\n'
        assert text.count(anchor) == 1
        text = text.replace(anchor, pointer + anchor, 1)
    (update / 'SKILL.md').write_text(text, encoding='utf-8', newline='\n')
    mapping.append({'skill': name, 'upstream_skills': ['new-focus'], 'upstream_sources': ['.claude/skills/new-focus/SKILL.md', '.claude/docs/focus-tree-reference.md'], 'kind': 'update'})

    files = []
    for parent, kind in [(HERE / 'skills', 'new'), (HERE / 'updates', 'update')]:
        for source in sorted(parent.rglob('*')):
            if not source.is_file():
                continue
            relative = source.relative_to(parent)
            destination = SKILLS / relative
            files.append({'source': source.relative_to(HERE).as_posix(), 'path': relative.as_posix(), 'kind': kind,
                          'before_sha256': digest(destination) if destination.exists() else None,
                          'after_sha256': digest(source)})
    manifest = {'project': 'IMPERIA COLD WAR', 'upstream_commit': commit, 'destination': str(SKILLS.resolve()),
                'skills': mapping, 'files': files}
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'new_skills': len(CATALOGUE), 'updated_skills': 1, 'files': len(files), 'commit': commit}))


if __name__ == '__main__':
    main()
