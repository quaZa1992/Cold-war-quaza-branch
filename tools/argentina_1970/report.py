# IMPERIA COLD WAR — Argentina implementation and validation record.
"""Write a compact current implementation record from installed validation receipts."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def main():
    d=json.loads((HERE/'runtime_design.json').read_text(encoding='utf-8'))
    source=json.loads((HERE/'VALIDATION.json').read_text())
    costs=json.loads((HERE/'GDP_VALIDATION.json').read_text())
    layout=json.loads((HERE/'LAYOUT_VALIDATION.json').read_text())
    native=json.loads((HERE/'NATIVE_RESULT.json').read_text())
    manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    groups=[g['title'] for g in d['groups'] if g['party'] is not None]
    unique_exclusions={tuple(sorted((n['id'],x))) for n in d['nodes'] for x in n['excludes']}
    text=f'''IMPERIA COLD WAR

# Argentina 1970: installed national programme

The national programme and its subsequently requested compact layout are implemented in the loaded mod. Start a new January 1970 Argentina campaign for the intended starting situation and progression. The historical starting leader is Juan Carlos Ongania and the ruling party is the Argentine Armed Forces. All player-facing additions are English.

## Content

- {len(d['nodes'])} focuses across {len(d['groups'])} sections, with {len(unique_exclusions)} mutually exclusive pairs.
- {len(groups)} party programmes, visible regardless of the governing party. Actual MD ruling-party and leader checks control execution and programme benefits/costs.
- Six starting national spirits, domestic industrial and military development, civilian election and succession content, and a dedicated South Atlantic section.
- Twenty focus-originated bilateral offers with recipient acceptance/refusal decisions. Each prospective focus reward shows both sides' concrete costs, modifiers, weekly flows, research, buildings and building slots before acceptance.
- Sixteen national content events, two additional political identity/succession events and twenty bilateral notification events.
- Eight native focus shortcuts, compact relative-anchor positions, and the approved prerequisite groups and exclusion relations.

## Compact layout revision

The layout-only request reduces the focus bounds from x=2..222, y=0..36 to x=2..100, y=0..23. Including full native card footprints, it is {layout['width_reduction_percent']}% narrower, {layout['height_reduction_percent']}% shorter and occupies {layout['area_reduction_percent']}% less bounding area. All 299 focuses remain, with their exact IDs, durations, GDP prices, rewards, political checks, prerequisite groups and exclusions preserved. The immutable original approval remains unchanged.

Eight paired political columns keep related programmes nearby. Three national columns place diplomacy below institutions, CNEA below the economy, and the South Atlantic below defence. Native grid spacing, cards, fonts and global GUI are unchanged. Local branch geometry uses single native rows and closer forks; two crowded four-card rows have dedicated lanes. The 770 x 380 continuous-focus panel now occupies a clear pocket below the political programmes instead of extending the old canvas.

The independent emitted-coordinate check covers {layout['prerequisite_links']} prerequisite links, all complete card rectangles and the continuous-focus pocket. It found {len(layout['card_overlaps'])} card overlaps and {len(layout['preview_connector_intersections'])} unrelated-card cuts in the orthogonal browser routing approximation. See [compact_layout_review.md](compact_layout_review.md) for independent visual review. Browser routing is an approximation; it does not establish exact in-game connector rendering.

## Falklands

`COLDWAR_ARG_rosario_plan`, Plan Operation Rosario, gives a real native `take_state_focus` war goal against Britain for state 26, expiring after 730 days. It costs 0.4% of live Argentine GDP and requires British ownership/control and bilateral peace. Declaration remains the player's diplomatic action. The branch also contains peaceful negotiating and joint-services alternatives, wartime mobilization and post-war restoration content.

## GDP-relative financing revision

The follow-up request replaces flat spending with shares of live native GDP. MD's January-1970 Argentine baseline is approximately 107.38543 billion internal GDP, displayed as 31.58395 billion historical 1970 dollars. Use the internal economic variable for native treasury calculations; dividing by the scenario price factor of 3.4 gives the historical display equivalent. These rates are game-balance appropriations, not estimates of historical programme budgets.

| Programme scale | One-time GDP share | Internal treasury amount at start | Historical display equivalent |
| --- | ---: | ---: | ---: |
| Routine reform | 0.2% | 0.21477 billion | 0.06317 billion |
| Substantial programme | 0.4% | 0.42954 billion | 0.12634 billion |
| Major national measure | 0.6% | 0.64431 billion | 0.18950 billion |
| Capital investment | 1.0% | 1.07385 billion | 0.31584 billion |
| Exceptional programme | 1.5% | 1.61078 billion | 0.47376 billion |

The sovereign islands settlement is the exceptional 2% Argentine GDP transaction, including compensation of 1.5% Argentine GDP paid to Britain. Britain's administrative setup charge is separately 0.2% of British GDP. The sponsored uranium mine costs 1% of live Argentine GDP at construction. The approved one-time asset-sale proceeds remain a fixed +3 native treasury units; this cost revision does not increase sale rewards.

Domestic running budgets range from 0.05% to 0.15% of annual GDP for the existing focus programmes, paid as native weekly expenses. Funded war mobilization uses 0.2% annual GDP while the war is active. Rates are recalculated from current GDP and retain the existing owner, duration and treaty activation conditions. Agreement operating budgets use each signatory's own GDP. The Bolivian gas transfer is 0.1% of Argentine GDP annually; the Soviet grain transfer is 0.3% annually. Each transfer has an identical payer debit and recipient credit, with separate own operating costs.

The cost revision leaves focus durations, geometry, political requirements, non-monetary rewards, modifiers and the Falklands war goal unchanged. Existing completion receipts are preserved; rebuilding costs does not replay paid setup rewards. A current [runtime preview](runtime-preview.html) shows the same revised costs, including both signatories and editable GDP estimates.

## Institutions and agreements

Earned party/leader programmes are reconstructed from completion receipts and current office ownership. Leaving office removes their active modifiers and weekly expenditure. Returning restores the earned programme without repeating one-time payments, construction or research. Authoritarian policy predicates require the party that owns that policy to still govern. Civilian handover requires an actually formed civilian constitutional government, so an election won by the military cannot clear the junta settlement.

Native MD elections and coalition resolution remain in place. The integration records the actual governing party only after election and coalition formation finish. It does not install the largest party as a substitute for MD's coalition result. Repeated handovers have separate election receipts and cannot charge twice for the same result.

Standing agreements have no spirit expiry. Both countries must exist, remain at peace with one another and impose no bilateral native embargo or any mirrored diplomatic, financial, economic or military Imperia sanction. Parent agreements require their actual active spirits. Pair reconciliation restores parents before dependents and runs even after Argentina disappears. It runs on the integrated major change hooks and once daily; monetary-flow guards use the current agreement conditions. Suspension/restoration never repeats setup fees, buildings, research or territorial transfers.

Every building level includes one additional shared state building slot before construction, inside the same one-time payout. Ownership/control, native capacity and the existing uranium deposit system are checked separately. Own state expenditure uses MD's treasury/debt path and requires no positive cash balance.

## Implementation clarifications

'''+''.join('- '+x+'\n' for x in d['implementation_adjustments'])+f'''
- Late leadership continuity uses the historical date boundaries and explicitly counterfactual collective offices recorded in [implementation_leaders.md](implementation_leaders.md). No historical person is newly installed after the relevant roster death boundary. An unchanged alternate-history incumbent is not automatically killed by the router.
- Event pictures reuse MD artwork in the current 217 x 163 frame with the original outer frame and alpha pixels. Stock illustrations are not represented as documentary Argentine photographs. Credits and unknown permissions are recorded in [implementation_art_notice.md](implementation_art_notice.md).

## Verification

- Installed-source validation: **{'PASS' if source['passed'] else 'FAIL'}**, {source['checks']} checks. This covers approval hash, installed hashes, BOM policy, references, localisation, sprites, portraits, registered leader ideologies, event namespaces, focus coordinates, prerequisite groups, exclusions and reward-preview separation.
- GDP price-contract validation: **{'PASS' if costs['passed'] else 'FAIL'}**, {costs['checks']} checks of invoices, preview/payment parity, own-GDP bases, weekly conversion and preserved non-monetary rewards.
- Compact layout validation: **{'PASS' if layout['passed'] else 'FAIL'}**, {layout['checks']} checks of semantic preservation, unchanged non-focus runtime providers, parsed coordinates, card/connector footprints and the continuous-focus pocket.
- Independent emitted-code mechanics review: [runtime_mechanics_final_review.md](runtime_mechanics_final_review.md).
- Independent layout and browser-preview review: [runtime_layout_final_review.md](runtime_layout_final_review.md). The browser preview is an approximation, not an HOI4 screenshot.
- Isolated native HOI4 transaction fixture: **{'PASS' if native['native_pass'] else 'NOT PASSED'}**, {native['passed']}/{native['expected']} checkpoints. Status: `{native['status']}`. Feature-specific diagnostics: {len(native['feature_diagnostics'])}. Raw provider hash changes during run: {len(native['frozen_source_drift'])}; native script-body changes: {len(native.get('runtime_semantic_drift',native['frozen_source_drift']))}. Concurrent Chile integration header comments were retained, with the exact parsed bodies compared against the frozen providers. The original private run record retains its raw hash-drift result; the repository result records the subsequent semantic review.
- Private profile: `{native['run']}`. The user explicitly authorized D: for this run because the prescribed E: drive was unavailable. Full logs and private scenario inputs stay outside the mod.

The native fixture uses controlled party slots, balances, embargo/sanction links and acceptance inputs. It checks actual runtime helpers, starting spirits, the Rosario war goal, party departure/return, payments from zero/negative treasury, one-time construction, twenty contract transactions, weekly aggregate contributions, paired suspension/restoration, coalition-resolution gates and annexation cleanup. These assertions do not constitute a human multiplayer session or prove every tooltip's exact rendering. A complete election campaign, an elapsed weekly budget tick, human in-game hover/navigation, a saved-campaign reload and simultaneous multiplayer interactions remain unperformed. Existing unrelated mod diagnostics were retained in the private error log and are not counted as Argentina feature errors.

## Rebuild and records

- Generator: `tools/argentina_1970/compile.py --install`.
- Source audit: `tools/argentina_1970/validate.py`.
- GDP price-contract audit: `tools/argentina_1970/validate_budget.py`; see [gdp_cost_audit.md](gdp_cost_audit.md) for the independent source review.
- Compact geometry and semantic audit: `tools/argentina_1970/validate_layout.py`; canonical layout is `tools/argentina_1970/layout.py`.
- Native fixture: `tools/argentina_1970/native_probe.py`; its default profile root remains on E:. D: is an explicit run override.
- Immutable approved input SHA-256: `{manifest['approved_sha256']}`. The original approved input remains unchanged.
- {len(manifest['files'])} generated or narrowly integrated script/localisation files are hash-recorded in `tools/argentina_1970/manifest.json`. Art assets have their own companion provenance record.
'''
    (ROOT/'docs/design/COLDWAR_ARG_1970/IMPLEMENTATION.md').write_text(text,encoding='utf-8',newline='\n')
    print(json.dumps(dict(project='IMPERIA COLD WAR',report='docs/design/COLDWAR_ARG_1970/IMPLEMENTATION.md',native_pass=native['native_pass'])))
if __name__=='__main__':main()
