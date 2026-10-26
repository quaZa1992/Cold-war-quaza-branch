# IMPERIA CW — Cold War: focus quality 20261020 — finalize report.
"""Run the approved quality-pass checks and publish their bounded evidence."""
from pathlib import Path
import hashlib
import html
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/tree_quality_audit_20261020'

CASES = [
    ('SDE-01', 'Soviet financial units', 'Interest rewards now use percentage points: banks -0.25 pp; Open Gates -0.10 pp. Runtime, tooltip and design preview agree.'),
    ('SDE-02', 'DDR internal factions', 'Military-industry effects target the initialized industrial_conglomerates faction. Procurement faction changes occur only after actual settlement.'),
    ('SDE-03', 'DDR debt repayment', 'Pay and retire the smaller of 3% GDP or remaining debt. No new borrowing or unfunded reward. A funded, once-only settlement grants -0.25 pp interest for 730 days, +8% sanction resistance and the stated political effects.'),
    ('SDE-04', 'Egyptian programme gates', '46 repeated debate/accounting connectors merged; six distinct shared historical or constitutional entries retained. Original reward guards and prerequisite alternatives preserved. Party roots remain at their original row.'),
    ('SDE-05', 'DDR political narratives', 'Seven priority political, financial and procurement descriptions now explain their programmes in English; canonical design, page and live text match.'),
    ('SDE-06', 'DDR Soviet procurement', 'The import route requests 90 real Soviet stock tanks for 1% frozen DDR GDP. Assembly requires an actual Soviet licence, costs 1.6% GDP, and grants two military factories plus 3% military factory productivity only on settlement. Soviet consent, stock, designs, cash and capacity are rechecked. No future tank technology is unlocked.'),
    ('GIIL-01', 'Libyan capstone', 'The 70-day capstone always calls native healthcare advancement, including its 150 PP maximum-tier fallback. It also grants +3% stability and -5% healthcare costs for 730 days.'),
    ('GIIL-02', 'Iraqi prisoner review', 'Only living unresolved cases inside their rescue windows remain actionable. One 30 PP session and a frozen 0.5% GDP invoice; invalidated sessions refund PP once without charging cash or applying the negotiation penalty.'),
    ('GIIL-03', 'Libyan descriptions', '67 descriptions rewritten as historical programmes instead of raw effect catalogues or implementation metadata.'),
    ('GIIL-04', 'Israeli descriptions', '20 party finales and 80 follow-through entries receive individual English narratives. Existing rewards and disabled-path safeguards retained.'),
    ('GCVU-01', 'Greek, Cypriot and US descriptions', '821 curated English descriptions: 313 Greece, 295 Cyprus and 213 USA. The 16 existing US Gulf additions are preserved.'),
    ('GCVU-02', 'Greek military connectors', 'The air opening grants 25 Air XP instead of repeated PP. Its radar follow-up costs 0.25% GDP and builds only with funding and capacity. The empty navy connector is bypassed and its successor requirements rewired.'),
    ('GCVU-03', 'Cypriot incumbent entry', 'Makarios administrative programme is directly reachable: 35 days, +3% stability factor and -5% bureaucracy costs for 0.25% GDP, once and only for the correct governing party.'),
    ('GCVU-04', 'Focus requirements UI', 'Internal routing, scenario and redundant receipt checks hidden while real guards remain. Meaningful party and membership requirements stay visible; Nixon presidency and the 20 January 1973 deadline are named.'),
    ('GEN-01', 'Generic two-office projects', 'Eleven projects deliver two office/power-plant phases, including in a single-state country. Each completed phase is charged once; unavailable phases stay pending. Existing net prices are preserved and the separate infrastructure invoice remains separate. No periodic global callback added.'),
    ('GEN-02', 'Generic military narratives', '64 individual descriptions: 58 army, navy and air entries plus six R&D precursors. Existing military rewards and the 70-day Air Cavalry research programme retained.'),
]

COMMANDS = [
    'tools/focus_quality_20261020/test_transactions.py',
    'tools/focus_quality_20261020/test_canonical_sources.py',
    'tools/focus_quality_20261020/test_generic_narratives.py',
    'tools/egypt_1970/test_quality_merges_20261020.py',
    'tools/iraq_1970/test_quality_review_20261020.py',
    'tools/iraq_1970/test_decisions_module.py',
    'tools/israel_1970/validate_rewards.py',
    'tools/israel_1970/validate_content.py',
    'tools/greece_1970/validate.py',
    'tools/greece_1970/test_quality.py',
    'tools/cyprus_1970/validate.py',
    'tools/cyprus_1970/test_transactions.py',
    'tools/usa_1970_quality/test_presentation.py',
]


def main():
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    checks = []
    log = []
    for script in COMMANDS:
        result = subprocess.run([sys.executable, '-W', 'ignore::ResourceWarning', script], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', env=env)
        output = result.stdout + result.stderr
        checks.append({'command': 'python ' + script, 'passed': result.returncode == 0,
                       'exit_code': result.returncode, 'output': output})
        log.append('COMMAND: python ' + script + '\n' + output)
        print(('PASS ' if result.returncode == 0 else 'FAIL ') + script, flush=True)
    # Hash the actual live focus inputs independently of the earlier audit snapshot.
    active = ['COLDWAR_DDR_1970_focus.txt', 'COLDWAR_SOV_1970_focus.txt',
              'COLDWAR_EGY_1970_focus.txt', 'mdcw_1970_generic_focus.txt']
    active += [p.name for p in (ROOT/'common/national_focus').glob('*')
               if p.suffix == '.txt' and any(x in p.name.lower() for x in ('libya_1970', 'isr70', 'cyp_1970', 'gre_1970', 'usa_1970', 'gen_1970'))]
    hashes = {str(Path('common/national_focus')/name): hashlib.sha256(
        (ROOT/'common/national_focus'/name).read_bytes()).hexdigest() for name in sorted(set(active))}
    report = {
        'date': '2026-10-20', 'status': 'implemented; source checks passed' if all(c['passed'] for c in checks) else 'CHECK FAILURE',
        'scope': 'The 16 approved findings from the focus-quality audit, not certification of every focus or modifier in the mod.',
        'cases': [{'id': ident, 'title': title, 'status': 'implemented', 'change': change} for ident, title, change in CASES],
        'checks': checks, 'live_focus_sha256': hashes,
        'canonical_sources': ['Claude outputs/COLDWAR_DDR_generator', 'Claude outputs/COLDWAR_SOV_generator',
                              'Claude outputs/COLDWAR_EGY_generator', 'Claude outputs/COLDWAR_GEN_generator',
                              'tools/iraq_1970', 'tools/israel_1970', 'tools/greece_1970', 'tools/cyprus_1970',
                              'tools/usa_1970_quality', 'libya: hand-authored live files'],
        'source_visual_review': 'Egypt and Greece full-tree and neighbor previews inspected using native GUI spacing, icons, title plates and bitmap font. Source previews approximate engine connector routing and text wrapping.',
        'reviews': ['Independent cross-owner mechanic and narrative reviews; discovered skip-cost, zero-GDP, frozen-quote and root-row cases corrected before final checks.'],
        'performance': 'New DDR and generic project logic is transaction/decision-driven; no new periodic global callback. This does not replace a multiplayer performance measurement.',
        'limits': [
            'No HOI4 engine, live tooltip, save/reload or multiplayer execution performed. Native stock transfer, production licence and construction calls have explicit modeled boundaries in AST tests.',
            'Full changes should be tested on a new 1970 start. Previously completed focus rewards and removed Egyptian connectors are not retroactively migrated or regranted in old saves.',
            'Retired Greek and Cypriot connector IDs remain hidden bypassed compatibility markers, not a guarantee of general old-save compatibility.',
            'Original USA generator named in its historical header is absent; the maintained overlay is documented in the live header.',
            'Deferred general event-art work and unrelated simultaneous changes were left outside this pass.',
        ],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'implementation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (OUT/'implementation_tests.log').write_text('\n\n'.join(log), encoding='utf-8')
    esc = html.escape
    rows = ''.join('<tr><td>'+esc(c['id'])+'</td><td><strong>'+esc(c['title'])+'</strong><br>'+esc(c['change'])+'</td></tr>' for c in report['cases'])
    tests = ''.join('<li>'+('PASS' if c['passed'] else 'FAIL')+' · <code>'+esc(c['command'])+'</code></li>' for c in checks)
    page = '<!doctype html><html lang="en"><meta charset="utf-8"><title>Focus quality implementation · 20 October 2026</title><style>body{background:#111820;color:#e5eaf0;font:16px/1.6 system-ui;margin:0}main{max-width:1100px;margin:auto;padding:32px}a{color:#a6d9e9}td{vertical-align:top;padding:16px;border-bottom:1px solid #354453}td:first-child{white-space:nowrap;color:#a6d9e9}code{font-size:.85em}h2{margin-top:36px}strong{color:white}</style><main><h1>Focus quality: implementation</h1><p>20 October 2026 · '+esc(report['status'])+'</p><p>'+esc(report['scope'])+'</p><table>'+rows+'</table><h2>Verification</h2><ul>'+tests+'</ul><p>'+esc(report['source_visual_review'])+'</p><p>'+esc(report['performance'])+'</p><h2>Practical limits</h2><ul>'+''.join('<li>'+esc(x)+'</li>' for x in report['limits'])+'</ul><p><a href="implementation.json">Machine-readable details and source hashes</a> · <a href="implementation_tests.log">Full test output</a> · <a href="review.html">Original audit</a></p><p><a href="previews/EGY_ASU_TP_neighbors.png">Egypt preview</a> · <a href="previews/GRE_navy_air_neighbors.png">Greece preview</a></p></main></html>'
    (OUT/'implementation.html').write_text(page, encoding='utf-8')
    original = OUT/'review.html'
    text = original.read_text(encoding='utf-8')
    if 'id="implementation-update"' not in text:
        text = text.replace('<main>', '<main><div class="intro" id="implementation-update"><strong>Implementation update, 20 October 2026:</strong> The 16 approved findings were addressed after this historical audit. <a href="implementation.html">Read changes, verification and remaining runtime limits.</a></div>', 1)
        original.write_text(text, encoding='utf-8')
    raise SystemExit(0 if all(c['passed'] for c in checks) else 1)


if __name__ == '__main__':
    main()
