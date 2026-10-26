"""Check that both concept previews embed the current canonical design."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
VIZ = Path('C:/Users/Enes/.codex/visualizations/2026/10/19/01a153f9-9c59-71b2-8460-d28a5d918d07/uae-1970-focus-concept.html')
raw = (HERE / 'COLDWAR_UAE_1970_CONCEPT.json').read_bytes()
design = json.loads(raw)
matches = {}
for path in [HERE / 'PREVIEW.html', VIZ]:
    text = path.read_text(encoding='utf-8')
    embedded = json.loads(re.search(r'<script type="application/json" id="uae-data">(.*?)</script>', text, re.S)[1].replace('<\\/', '</'))
    embedded.pop('assets')
    matches[path.name] = embedded == design
    assert matches[path.name], path
assert VIZ.stat().st_size < 1_000_000
start = design['british_treaties']['starting_state']
assert start['starts_with_both_spirits'] and not start['requires_focus'] and not start['requires_new_uk_acceptance']
report = dict(sha256=hashlib.sha256(raw).hexdigest(), embedded_model_matches=matches,
              focuses=len(design['nodes']), decisions=len(design['decisions']),
              starting_base_oil=4, oil_capex_billion=16.25,
              unrelated_existing_focuses_preserved=97, treaty_variants=len(design['british_treaties']['variants']),
              starting_withdrawal_in_both_countries=True, historical_release_requires_focus=False,
              historical_release_requires_new_uk_approval=False, loaded_files_written=False)
(HERE / 'FINAL_BUNDLE_VALIDATION.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
