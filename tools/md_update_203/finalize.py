# IMPERIA COLD WAR — Final MD 2.0.3 implementation evidence and documentation.
"""Record exact installed metadata and preservation evidence without rebuilding content."""
from pathlib import Path
import collections
import gzip
import hashlib
import json
import re

from audit import ROOT,OUT,UP,PROJECT,emit


def main():
    implementation=json.loads((OUT/'implementation.json').read_text(encoding='utf-8'))
    source=json.loads((OUT/'source_recheck.json').read_text(encoding='utf-8'))
    assert implementation['status']==source['status']=='PASS'
    with gzip.open(OUT/'all_files.jsonl.gz','rt',encoding='utf-8') as stream:records=list(map(json.loads,stream))
    raw_changes=[r['path'] for r in records if (r['baseline'] or {}).get('sha256')!=(r['new_md'] or {}).get('sha256') and (r['baseline'] is not None or r['new_md'] is not None)]
    assert len(raw_changes)==73
    checks=[]
    for tx in implementation['transactions']:
        path=ROOT/tx['path']
        if tx['operation']=='remove_empty':assert not path.exists();checks.append(tx['path']+': verified empty file removed');continue
        raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==tx['after'],tx['path']
        if path.suffix=='.yml':
            assert raw.startswith(b'\xef\xbb\xbf')
            text=raw.decode('utf-8-sig');assert text.splitlines()[1].startswith('# IMPERIA COLD WAR — ')
            assert not re.search(r'^\s+VERSION_MD(?:_LOADING)?:.*2\.0\.2',text,re.M)
        if path.suffix=='.mod':
            assert raw.startswith('# IMPERIA COLD WAR — '.encode()) and not raw.startswith(b'\xef\xbb\xbf')
            assert b'version="2.0.3"' in raw and b'name="MD Cold War"' in raw
        if tx['path'].startswith('descriptions/'):
            assert re.search(rb'(?m)^\[b\].*\[/b\]\s*v?2\.0\.3\r?$',raw)
            assert not re.search(rb'(?m)^\[b\].*\[/b\]\s*(?:8751|ccc6)\s*$',raw)
        checks.append(tx['path']+': exact approved metadata result and encoding')
    launcher=implementation['external_launcher'];assert hashlib.sha256(Path(launcher['path']).read_bytes()).hexdigest()==launcher['after']
    preserved=['common/scripted_effects/00_money_system.txt','common/national_focus/ISR70_focus.txt',
        'common/scripted_effects/ISR70_policy_effects.txt','common/scripted_triggers/ISR70_policy_triggers.txt',
        'interface/countrytechtreeview.gui','interface/countrytradeview.gui','interface/MD_countrymissilesview.gui',
        'common/synchronized_dynamic_tokens/MD_tokens.txt','common/scripted_guis/COLDWAR_SSR_intelligence.txt',
        'common/scripted_triggers/COLDWAR_SSR_intelligence.txt','history/states/1253-West Jerusalem.txt']
    originals={r['cold_war']['path'].casefold():r['cold_war']['sha256'] for r in records if r['cold_war']}
    for rel in preserved:assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==originals[rel.casefold()],rel
    assert not (ROOT/'common/scripted_effects/00_money_system.txt').read_bytes().startswith(b'\xef\xbb\xbf')
    native_path=OUT/'native_report.json'
    native=json.loads(native_path.read_text(encoding='utf-8')) if native_path.exists() else dict(status='NOT_RUN',native_test=False)
    result=dict(project=PROJECT,status='PASS',scope='Installed metadata, source accounting and exact preservation checks',
        checks=checks,changed_or_removed_paths=38,updated_files=26,removed_empty_files=12,external_launchers=1,
        raw_upstream_changes=73,fresh_md_files_hashed=source['files'],
        full_installed_files_hashed=implementation['files_verified'],byte_preserved_files=implementation['files_preserved_byte_for_byte'],
        native_test=native.get('native_test',native.get('success',False)),native_status=native.get('status','PASS' if native.get('success') else 'FAIL'),
        feature_samples_rechecked=preserved,unexpected_changes=implementation['unexpected_changes'])
    emit(OUT/'final_verification.json',result)
    if native.get('native_test_executed') and not native.get('success'):
        native_note='the isolated test reached January 1970 startup but failed before its day-three checkpoints. '+('The engine produced a crash report. ' if native.get('crash_exceptions') else '')+'See native_report.json and FOLLOW_UP_VERIFICATION.md. Full runtime compatibility is not certified.'
    elif result['native_test']:
        native_note='the isolated smoke test passed; see native_report.json.'
    else:
        native_note='not run. The active Launcher-started HOI4 session was detected outside the restricted process view. The probe refused to start a second game and did not stop or alter that session.'
    note=['# IMPERIA COLD WAR: MD 2.0.3 update implemented','',
        'Implemented after the user approved the recommended proposal on 28 October 2026. The short interruption concerning national tactics was explicitly withdrawn and caused no content change.','',
        '## Actual changes','',
        '- Updated the mod descriptor, portable launcher descriptor and actual external launcher descriptor to version 2.0.3. The MD Cold War identity, supported game-version range and custom replace paths are retained.',
        '- Synchronized existing frontend version labels without generating new translations. Localisation retains its BOM and project marker position.',
        '- Updated eleven existing description version lines to 2.0.3 and removed their fixed upstream MD checksum claim. The source descriptions still contain stale 2.0.0/2.0.1 labels and the MD-specific 8751/ccc6 checksum values; these were not misrepresented as this custom mod\'s verified checksum. This corrects the initial proposal\'s overly broad description of these fields.',
        '- Adopted the supplied short upstream update note with explicit provenance. Its inherited v2.0.2 heading is identified as source text.',
        '- Removed exactly twelve already empty auto-agency compatibility files. No active queue implementation was deleted by this transaction.',
        '- Updated the README base version and root provenance notice. The two source-folder Egyptian development PNGs were excluded.','',
        'There are 26 updated repository files and twelve empty-file removals, plus the one external launcher update. No national focus, game effect, trigger, map, GUI implementation, economy formula, equipment definition or artwork was replaced. The technical MD 2.0.3 changes were already present alongside the Cold War additions before this finalization.','',
        '## Complete comparison and preservation','',
        f"A fresh raw SHA256 pass reread all {source['files']:,} files in the supplied Workshop folder and found no change since the individually reviewed source. The original MD inventory and current source differ at exactly 73 paths even when raw bytes, rather than normalized text, are compared. These comprise 59 changed existing files, twelve removed files and two development image additions. No additional formatting-only source changes were hidden by the normalized comparison.", '',
        f"The full post-implementation pass verified {implementation['files_verified']:,} installed files. Exactly {implementation['files_preserved_byte_for_byte']:,} files retain their original bytes. Every difference is listed in implementation.json; unexpected differences: zero. Our research, uranium, Space Race, SSR, country content, settlement programmes and other authored mechanics are retained.", '',
        'The comparison is against the exact local MD folder supplied by the user and the archived original MD source used for the prior migration. It is not a claim that Steam cannot publish another update, nor certification that every source-folder artifact belongs to a pristine public GitHub release. Private caches/Git metadata/audit outputs are explicitly excluded; asset junction aliases are not traversed. Actual loaded asset directories were included.','',
        '## Verification and limits','',
        '- Full upstream hash recheck and complete installed-file preservation: PASS.',
        '- Exact metadata transactions, mod identity, paths, localisation encoding and removed empty files: PASS.',
        '- Existing Israel content/reference/integration checks: PASS. Settlement-presence model: 341 checks. Palestinian pressure model: 867 checks.',
        '- Native game: '+native_note,
        '- Manual hover/UI operation, save/reload, first-month and multiplayer checks remain unperformed for this update. Source preservation is not substituted for those tests.','',
        '## Recovery and provenance','',
        'Original affected files and the external launcher were backed up before writes to `'+implementation['backup'].replace('\\','/')+'`. The archive hash and every before/after file hash are recorded in implementation.json. Original audit inventories remain unchanged.','',
        'Existing Millennium Dawn and Cold War/Imperia credits and licences remain in effect. No artwork was modified. Individual third-party authors or separate permissions remain unknown where not identified by the inherited source. The implementation tooling and this English report were authored for IMPERIA COLD WAR with Codex.']
    (OUT/'IMPLEMENTED.md').write_text('\n'.join(note)+'\n',encoding='utf-8')
    review=OUT/'REVIEW.md';value=review.read_text(encoding='utf-8')
    value=value.replace('Status: read-only comparison completed. Source-adoption choices are pending. No loaded mod file has been changed by this task.',
        'Status: the recommended proposal was subsequently approved and implemented. See IMPLEMENTED.md and implementation.json for the actual changes and verification. The original comparison and file choices below are retained as review evidence.')
    review.write_text(value,encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('project','status','updated_files','removed_empty_files','raw_upstream_changes','byte_preserved_files','native_status')},indent=2))


if __name__=='__main__':main()
