# IMPERIA COLD WAR — File-by-file MD 2.0.3 adoption proposal.
"""Document the verified inventory and user choices; do not change runtime."""
from pathlib import Path
import csv
import gzip
import json
import re

from audit import ROOT,OUT,UP,PROJECT,emit

PRESERVE={
 'common/intelligence_agency_upgrades/intelligence_agency_upgrades.txt':'Keep completed passive-defence tracking for nuclear intelligence and the Cold War covert-action artwork; the MD native upgrade changes are already present.',
 'common/on_actions/MD_on_actions.txt':'Keep guest-worker updates, 1970 date guards and reserve-currency accounting observers; the MD queue callback removal is already present.',
 'common/scripted_diplomatic_actions/00_scripted_diplomatic_actions.txt':'Keep dossier correspondence receipts; obsolete MD offer filtering has already been removed.',
 'common/scripted_guis/00_missiles_scripted_guis.txt':'Keep Space Race, Cold War satellites and international-system changes. The obsolete satellite-reject handler is already absent; retain current balanced closing blocks.',
 'common/synchronized_dynamic_tokens/MD_tokens.txt':'Keep uranium, uranium-mine, energy and resource-toolbar tokens; MD removed queue/filter tokens are already absent.',
 'interface/alerts.gui':'Keep COMECON toolbar clearance; new MD native alert buttons are already present.',
 'interface/countrytechtreeview.gui':'Keep 1970 research branches, early equipment and custom positions. Native MD research-tab controls are already present.',
 'interface/countrytradeview.gui':'Keep nine-resource uranium geometry. New MD trade controls are already present.',
 'interface/general_stuff.gfx':'Keep nine-frame resource strips including uranium. New MD sprites are already present.',
 'interface/MD_countrymissilesview.gui':'Keep Space Race ledger and compact recognition list; obsolete MD satellite filter controls are already removed.',
 'localisation/english/MD_missiles_l_english.yml':'Keep Cold War GNSS benefit wording and legacy cleanup labels. The MD obsolete-filter text changes are already present.',
 'localisation/english/research_l_english.yml':'Keep current file: both new MD research-keyboard tooltip values already match exactly, including all local extra keys.'
}


def main():
    summary=json.loads((OUT/'inventory_summary.json').read_text(encoding='utf-8'))
    review=json.loads((OUT/'semantic_review.json').read_text(encoding='utf-8'))
    runtime={};preserve_runtime=0
    with gzip.open(OUT/'all_files.jsonl.gz','rt',encoding='utf-8') as stream:
        for r in map(json.loads,stream):
            if r['runtime'] and r['classification'] in ('cold_war_only_keep','cold_war_addition_keep'):preserve_runtime+=1
    for r in review['files']:
        path=r['path'];semantic=r['semantic']
        if path in PRESERVE:proposal=PRESERVE[path];action='KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT'
        elif semantic=='non_runtime_binary_reference':proposal='Exclude these two Cold War development previews found in the supplied MD folder; they are not a runtime update.';action='EXCLUDE_SOURCE_DEVELOPMENT_ARTIFACT'
        elif semantic=='deleted_upstream_local_empty_stub':proposal='Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled.';action='ASK_REMOVE_EMPTY_LEGACY_FILE'
        elif path=='descriptor.mod':proposal='Set version to 2.0.3; retain MD Cold War name, portable launcher identity and all custom replace paths.';action='ASK_UPDATE_METADATA_KEEP_IDENTITY'
        elif path=='Changelog.txt':proposal='Retain the earlier MD notes as historical reference in the audit, and adopt the supplied current upstream note with project provenance.';action='ASK_UPDATE_UPSTREAM_NOTE'
        elif path.startswith('descriptions/') or 'MD_frontend_l_' in path:
            proposal='Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity.';action='ASK_SYNC_EXISTING_VERSION_LABELS'
        else:proposal='Already contains the new MD content; keep current file.';action='ALREADY_PRESENT_KEEP'
        r.update(proposal=proposal,action=action)
        if r['runtime'] and (ROOT/path).is_file():
            b=(ROOT/path).read_bytes();runtime[path]=dict(sha256=r['cold_war_sha256'],bom=b.startswith(b'\xef\xbb\xbf'))
    emit(OUT/'adoption_plan.json',dict(project=PROJECT,status='AWAITING_USER_SOURCE_CHOICES',runtime_writes=0,
        baseline_verified_files=71,files=review['files'],runtime_preservation=runtime,
        protected_runtime_additions_or_changes=preserve_runtime,
        decisions=dict(recommended='Keep all current Cold War functionality and already integrated MD technical fixes; synchronize versions, clean twelve empty legacy files and exclude two source development previews.',
            conservative='Same feature-preserving result, but retain the twelve empty compatibility stubs. No legacy queue is restored.'),
        unperformed=['No active migration writes, native engine, save/reload or multiplayer tests.']))
    fields=['project','path','classification','semantic','baseline_verified','action','proposal']
    with (OUT/'decisions.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(review['files'])
    lines=['# IMPERIA COLD WAR: MD 2.0.3 update review','',
        'Status: read-only comparison completed. Source-adoption choices are pending. No loaded mod file has been changed by this task.','',
        '## Scope and evidence','',
        f"The supplied Workshop source contains {summary['sources']['new_md']['regular_files']:,} regular files; the current Cold War tree contains {summary['sources']['cold_war']['regular_files']:,}. All were read and hashed. The archived original MD inventory contains 79,721 files. Their union is {summary['union_files']:,} paths. There were no read errors, case collisions or final-scan source changes.", '',
        'The archive is the actual source inventory from the earlier migration, not an assumed ancestor. Its SHA256 and current Git HEAD are in inventory_summary.json. Every one of the 71 changed/deleted historical MD files has a recovered, hash-verified original. The research GUI ancestor was verified against the official v2.0.2 tag. The Workshop descriptor was recovered by reversing only its version literal and matching its exact archived raw hash.','',
        'Git metadata, private caches and the audit output/tool directories are explicitly excluded. Four asset-provider junctions are recorded without traversal. They are aliases rather than independent game assets. No regular runtime directory was excluded.','',
        '## What this installed MD update actually changes','',
        'There are 73 changed/additional/deleted source paths: 59 changed existing files, 12 deletions and two development PNG additions. Of these, 69 are runtime-directory paths. The installed source changes native UI controls and keyboard shortcuts for HOI4 1.19.4, research-tab tooltips, the native agency upgrade queue and obsolete offer filters. It also changes version labels. This delta contains no changed MD country focus tree, state history, map binary, economy formula or unit-technology definition. The technology-tag file differs in formatting only.','',
        'The two additional files are Cold War Egyptian preview PNGs under Claude outputs. They are documented source-folder development artifacts, not interpreted as a new upstream gameplay feature. The supplied folder is the user-selected source; it is not falsely certified as a byte-identical pristine GitHub release.','',
        'The public release is [v2.0.3](https://github.com/MillenniumDawn/Millennium-Dawn/releases/tag/v2.0.3). The release link confirms the release identity, while the local full-file hashes establish this comparison. The public Git tag descriptor still contains a developer 2.0.2 label; the supplied Workshop descriptor contains 2.0.3. Version strings alone are therefore not the merge baseline.','',
        '## Results and preservation','',
        'Twenty-three script/text files have exactly the same executable tokens as the new MD source after excluding comments and whitespace. Two localisation files already have all the same MD key values, including both research-tab tooltip strings. The full three-way probes returned 34 files with no additional executable changes, 22 clean metadata/text updates and three textual conflicts.','',
        'The three textual conflicts are: descriptor version plus the custom mod name; an already-removed satellite filter handler next to locally reformatted closing blocks; and research tooltip lines that are already identical except for a local comment. These do not justify replacing the shared Cold War files.','',
        f'{preserve_runtime:,} runtime files are additional or modified Cold War content outside the MD delta and are preserved. The remaining shared-file custom changes also stay: early research and equipment, nine-resource uranium trade/UI, Space Race, recognition presentation, nuclear-intelligence passive-defence receipts, dossier observers, guest workers, reserve-currency tracking and 1970 event guards. The separate SSR agency-creation blocker and its native parent window remain in place.','',
        'Existing MD auto-agency files are already comment-only stubs or an empty localisation header in the current Git commit. Removing these twelve empty files follows upstream cleanup without removing an active Cold War programme. Keeping them is an equally feature-preserving compatibility option. Reinstating the obsolete modded queue is not part of either proposal.','',
        '## Decisions for the user','',
        '| Area | Proposed source choice |','| --- | --- |',
        '| Native UI, shortcuts, queue and filters | Retain the MD 2.0.3 fixes already merged into our files. |',
        '| Research, uranium, Space Race, SSR, diplomacy and 1970 content | Retain Cold War implementations and additions. |',
        '| Descriptor and version labels | Update to 2.0.3, retain Cold War name and custom paths. |',
        '| Twelve obsolete empty agency files | Recommended: remove. Alternative: retain empty compatibility stubs. |',
        '| Two Egyptian preview PNGs in the supplied MD folder | Exclude from the update. |','',
        'The requested decision is whether to apply the recommended version-and-cleanup proposal, retain the twelve empty compatibility files, or select individual file exceptions. Nothing in the active mod has been replaced while this choice is pending.','',
        '## Complete changed-source file catalogue','',
        '| File | Classification and proposed action |','| --- | --- |']
    for r in review['files']:lines.append('| `'+r['path']+'` | '+r['action']+': '+r['proposal']+' |')
    lines+=['','## Artifacts and limits','',
        '- all_files.jsonl.gz: one record for every union path, with original/new/local hashes and classification.',
        '- inventory_summary.json: source coverage, exclusions, stable-scan evidence and area counts.',
        '- upstream_changes.json and upstream_delta.diff: all source changes and verified original-to-new textual hunks.',
        '- semantic_review.json and local_preservation.diff: full token/key comparison, dry-run merges and local feature differences.',
        '- decisions.csv and adoption_plan.json: per-file action catalogue and pending user choices.','',
        'This is source and merge-probe evidence. No HOI4 launch, save conversion, tooltip rendering, economy tick or multiplayer rehearsal has run for this update. A full engine feature audit is not claimed merely from hashing every file.','',
        '## Provenance','',
        'The audit tools and review narrative were authored for IMPERIA COLD WAR with Codex. Original source credit: Millennium Dawn contributors and existing Cold War/Imperia contributors. Source code excerpts in the two diff reports retain their original source identity; no artwork pixels are modified or copied into the active mod. Individual upstream authors and separate redistribution permissions are unknown where the inherited source does not identify them. Existing repository licence and notices remain authoritative; a project marker does not establish third-party ownership.']
    (OUT/'REVIEW.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(dict(project=PROJECT,status='AWAITING_USER_SOURCE_CHOICES',catalogued_source_changes=len(review['files']),protected_runtime_files=preserve_runtime,runtime_writes=0)))


if __name__=='__main__':main()
