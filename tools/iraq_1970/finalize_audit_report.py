# IMPERIA CW — Cold War: iraq 1970 — finalize audit report.
"""Pin final installed evidence; does not certify untested engine behaviour."""
from pathlib import Path
import hashlib,json,subprocess,sys
from common import ROOT

HERE=Path(__file__).resolve().parent
OUT=ROOT/'docs/design/iraq_1970/audit_2026_10_19'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    manifest=read(HERE/'manifest.json')
    files={**manifest['generated'],**{a['path']:a['sha256'] for a in manifest['adapters']}}
    assert all(sha(ROOT/p)==h for p,h in files.items()), 'Installed outputs changed; inspect concurrent work before regeneration.'
    before=sha(HERE/'manifest.json')
    result=subprocess.run([sys.executable,str(HERE/'compile.py')],cwd=ROOT,text=True,capture_output=True,check=True)
    assert sha(HERE/'manifest.json')==before, 'Compiler manifest is not reproducible.'
    assert all(sha(ROOT/p)==h for p,h in files.items()), 'Compiler output is not reproducible.'
    (HERE/'REPRODUCIBILITY_REPORT.json').write_text(json.dumps({'byte_identical_regeneration':True,'manifest_sha256':before,'generated':len(manifest['generated']),'adapters':len(manifest['adapters'])},indent=2)+'\n',encoding='utf-8')
    validation=read(HERE/'VALIDATION_REPORT.json')
    browser=read(ROOT/'docs/design/iraq_1970/implementation/INSTALLED_VIEWER_BROWSER_REPORT.json')
    viewer=read(HERE/'staged/INSTALLED_VIEWER_REPORT.json')
    post_review=read(OUT/'POST_REVIEW_INSTALLED_TESTS.json')
    assert not validation['missing_references'] and not browser['errors']
    assert post_review['success'] and post_review['manifest_sha256']==before
    assert all(sha(ROOT/p)==h for p,h in viewer['source_hashes'].items())
    starts=read(OUT/'implementation_start_snapshot.json')
    changed={p:{'start':h,'current':sha(ROOT/p)} for p,h in starts.items() if (ROOT/p).exists() and sha(ROOT/p)!=h}
    report={
      'revision':manifest['audit_revision'],
      'manifest_sha256':before,'approved_original_sha256':manifest['approved_sha256'],
      'generated_files':len(manifest['generated']),'scoped_adapters':len(manifest['adapters']),
      'all_installed_hashes_match':True,'byte_identical_regeneration':True,
      'counts':{'irq_registered':426,'irq_active':410,'irq_legacy':16,'usa_original_preserved':validation['usa_existing_preserved'],'usa_added_registered':15,'usa_added_active':14,'usa_total_active':228},
      'test_families':{'reward_data':15,'structure_graph':13,'fresh_transactions':22,'politics':18,'new_usa_transactions':21,'prior_usa_transactions':17,'us_review_counterexamples':14,'concession_feasibility':6,'core':8,'prior_decisions':15,'starting_spirits':9,'presentation':9,'metadata_recovery':10,'gulf_checks':75},
      'test_scope':'Source/data/strict emitted-AST checks with explicit native API boundaries. Counts are scenario families, not a full HOI4 emulator.',
      'validation':validation,'browser':browser,'viewer':viewer,'post_review_installed_counterexamples':post_review,
      'engine_full_latest_attempt':read(HERE/'ENGINE_RUNTIME_REPORT.json'),
      'engine_targeted_latest_attempt':read(HERE/'ENGINE_ASSET_REPORT.json'),
      'earlier_native_observation':{'manifest_sha256':'ff7b7cb8c64877b27bd1a79826995eb497b9c7cd5d008067a2fb95f79da71eca','scope':'Observed tool result at14:35:52, targeted actual asset fixture before later presentation/shared-history updates; not final whole-mod certification.','target_state_factory_before':1,'target_state_factory_after':2,'synthetic_gdp_bn':10,'treasury_start_bn':1000,'paid_invoice_bn':.5,'repeat_payment_and_asset_replay':False,'completed':True},
      'native_limit':'No new native engine attempt was performed for post-review v2. A targeted native factory/payment check succeeded on an earlier manifest. Subsequent pre-v2 full-start and targeted repetitions terminated before their checkpoints, and one early targeted attempt remained blocked by startup conditions. Current campaign startup, real old-save load, long-term budgets/combat and multiplayer are not certified; the previous crash cause is unassigned.',
      'skill_install':read(HERE/'skill_updates/IMPACT_INSTALL_VERIFICATION.json'),
      'changed_since_implementation_start':changed,
      'shared_work_preserved':'Shared party presentation and a concurrent Iraqi history reformat/army-deferral edit were preserved. The pure Iraqi party adapter emits all36 curated keys exactly. No whole-workspace unchanged claim is made.',
      'test_import_correction':'The USA harness now appends the shared AST directory. A first discovery imported Vietnam compile by module-name collision and regenerated its current sources; this was not an intended content change. No speculative revert of concurrent Vietnamese work was performed.',
      'conditional_design_boundary':'No new Shatt-only bilateral war/peace contract was promised as finished by the approved audit; neutral assessment/shared preparation implemented, territorial ultimatum/core retains its express claim.',
      'installed_hashes':files,
      'source_hashes':{p.name:sha(p) for p in HERE.glob('*.py')},
    }
    (OUT/'IMPLEMENTATION_CHECKS.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'manifest_sha256':before,'generated':len(manifest['generated']),'adapters':len(manifest['adapters']),'reproducible':True,'references':validation['missing_references'],'browser_errors':browser['errors'],'native_final_certified':False},indent=2))

if __name__=='__main__':main()
