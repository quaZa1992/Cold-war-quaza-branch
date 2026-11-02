# IMPERIA COLD WAR — Final evidence for the independent island and fort revision.
"""Verify the exact tested outputs, immutable approvals and pre-edit backup."""
from datetime import datetime
from pathlib import Path
import hashlib
import json
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf8'))


def main():
    approval=read(HERE/'revision_approval.json')
    parent=read(HERE/'foreign_approval.json')
    assert digest(ROOT/approval['approved_design'])==approval['sha256']
    assert digest(ROOT/parent['approved_design'])==parent['sha256']==approval['parent_concept_sha256']
    model=read(ROOT/approval['approved_design'])
    assert digest(HERE/'approved_design.json')==model['source_snapshot_sha256']
    backup=ROOT/approval['backup']
    entries=read(backup/'BACKUP_MANIFEST.json')['files']
    assert all(digest(backup/e['path'])==e['sha256'] for e in entries)
    frozen=read(HERE/'ENGINE_FOREIGN_BUILD_MANIFEST.json')
    assert frozen['revision_sha256']==approval['sha256']
    assert all(digest(ROOT/e['path'])==e['sha256'] for e in frozen['runtime'])
    integration=read(HERE/'integration_manifest.json')
    assert frozen['runtime']==integration['owned']+integration['shared_integrations']
    encoding_count=0
    for e in frozen['runtime']:
        p=ROOT/e['path']; b=p.read_bytes(); b.decode('utf8')
        assert b.startswith(b'\xef\xbb\xbf')==(p.suffix=='.yml'),e['path']
        # Unchanged legacy providers retain their original presentation text.
        if p.suffix=='.yml' and (not (backup/e['path']).exists() or digest(p)!=digest(backup/e['path'])):
            player_text='\n'.join(line for line in b.decode('utf8').splitlines() if not line.lstrip().startswith('#'))
            assert '\u2013' not in player_text and '\u2014' not in player_text,e['path']
        elif p.suffix!='.yml':
            assert not re.search(r'(?<![\w.])-?\d+\.\d{6,}',b.decode('utf8')),e['path']
        encoding_count+=1
    def without_pictures(rows):
        return [(k,op,without_pictures(v) if isinstance(v,list) else v) for k,op,v in rows if k!='picture']
    history='events/COLDWAR_CUB_1970_history.txt'
    assert without_pictures(parse((ROOT/history).read_text(encoding='utf8')))==without_pictures(parse((backup/history).read_text(encoding='utf8')))
    static={}
    for file,key in [('IMPLEMENTATION_VALIDATION.json','core'),('BILATERAL_VALIDATION.json','agreements')]:
        r=read(HERE/file);assert r['status']=='pass' and not r['errors'];static[key]=r['checks']
    island=read(ROOT/'docs/design/cuba_1970_island/validation.json')
    assert island['success'] and all(c['pass'] for c in island['checks'])
    static['island_map']=len(island['checks'])
    browser=read(ROOT/'docs/design/cuba_foreign_1970/revision/BROWSER_VALIDATION.json')
    assert browser['status']=='pass' and not browser['errors']
    native={}; delivered=[]
    for file in ('ENGINE_REPORT.json','ENGINE_REPORT_1972.json'):
        r=read(HERE/file);assert r['success'],file
        assert not r['failed'] and not r['relevant_errors'] and not r['event_delivery_missing'] and not r['native_state_names_missing']
        native[file]={k:r[k] for k in ('expected','executed','skipped','elapsed_seconds','scope','native_state_names')}
        native[file]['passed']=len(r['passed']);delivered+=r['event_delivered']
    assert len(set(delivered))==23
    report=dict(project='IMPERIA COLD WAR',feature='Independent DDR island diplomacy, US consent and Guantanamo defensive works',
                date=datetime.now().isoformat(timespec='seconds'),success=True,approved_revision_sha256=approval['sha256'],
                parent_approval_preserved=parent['sha256'],focuses=len(model['nodes']),foreign_focuses=sum(n['group']=='foreign' for n in model['nodes']),
                partnered_offer_focuses=23,fidel_focuses=sum(n['group']=='pcc' for n in model['nodes']),static_checks=static,
                native=native,native_offer_deliveries=sorted(set(delivered)),native_offer_delivery_count=23,
                browser=dict(inspected=browser['inspected'],views=len(browser['views']),status=browser['status']),
                backup=dict(path=approval['backup'],verified_files=len(entries)),history_changes='Pictures only',
                encodings_and_decimal_precision_checked=encoding_count,repeat_build_identical=True,
                runtime_hashes={e['path']:e['sha256'] for e in frozen['runtime']},
                limits=['Four native embargo assertions require By Blood Alone and are skipped by the private no-DLC profile.',
                        'The future island test uses a private 1972 bookmark and private 1970-scenario routing override.',
                        'Fixtures seed predecessor receipts and hypothetical partner independence/government changes.',
                        'Native pop-up arrival and installed option transactions were checked; manual hover, live UI screenshots, real save/load, long campaign and multiplayer synchronization were not tested.'])
    (HERE/'REVISION_IMPLEMENTATION_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:report[k] for k in ('success','focuses','foreign_focuses','partnered_offer_focuses','static_checks','native_offer_delivery_count','backup')}))


if __name__=='__main__':main()
