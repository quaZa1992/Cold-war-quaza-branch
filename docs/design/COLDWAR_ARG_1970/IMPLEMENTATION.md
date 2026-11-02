IMPERIA COLD WAR

# Argentina 1970: installed national programme

The national programme and its subsequently requested compact layout are implemented in the loaded mod. Start a new January 1970 Argentina campaign for the intended starting situation and progression. The historical starting leader is Juan Carlos Ongania and the ruling party is the Argentine Armed Forces. All player-facing additions are English.

## Content

- 299 focuses across 22 sections, with 67 mutually exclusive pairs.
- 16 party programmes, visible regardless of the governing party. Actual MD ruling-party and leader checks control execution and programme benefits/costs.
- Six starting national spirits, domestic industrial and military development, civilian election and succession content, and a dedicated South Atlantic section.
- Twenty focus-originated bilateral offers with recipient acceptance/refusal decisions. Each prospective focus reward shows both sides' concrete costs, modifiers, weekly flows, research, buildings and building slots before acceptance.
- Sixteen national content events, two additional political identity/succession events and twenty bilateral notification events.
- Eight native focus shortcuts, compact relative-anchor positions, and the approved prerequisite groups and exclusion relations.

## Compact layout revision

The layout-only request reduces the focus bounds from x=2..222, y=0..36 to x=2..100, y=0..23. Including full native card footprints, it is 55.02% narrower, 35.15% shorter and occupies 70.83% less bounding area. All 299 focuses remain, with their exact IDs, durations, GDP prices, rewards, political checks, prerequisite groups and exclusions preserved. The immutable original approval remains unchanged.

Eight paired political columns keep related programmes nearby. Three national columns place diplomacy below institutions, CNEA below the economy, and the South Atlantic below defence. Native grid spacing, cards, fonts and global GUI are unchanged. Local branch geometry uses single native rows and closer forks; two crowded four-card rows have dedicated lanes. The 770 x 380 continuous-focus panel now occupies a clear pocket below the political programmes instead of extending the old canvas.

The independent emitted-coordinate check covers 342 prerequisite links, all complete card rectangles and the continuous-focus pocket. It found 0 card overlaps and 0 unrelated-card cuts in the orthogonal browser routing approximation. See [compact_layout_review.md](compact_layout_review.md) for independent visual review. Browser routing is an approximation; it does not establish exact in-game connector rendering.

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

- The sponsored uranium mine costs 1% of live Argentine GDP, charged in its construction decision with the native capacity/ownership/slot grant transaction.
- Constitutional-election preparation does not remove the regime spirit before the elected government actually takes office.
- Independent party labor settlements remove the superseded wage-restraint spirit so its stated remedy is reachable.

- Late leadership continuity uses the historical date boundaries and explicitly counterfactual collective offices recorded in [implementation_leaders.md](implementation_leaders.md). No historical person is newly installed after the relevant roster death boundary. An unchanged alternate-history incumbent is not automatically killed by the router.
- Event pictures reuse MD artwork in the current 217 x 163 frame with the original outer frame and alpha pixels. Stock illustrations are not represented as documentary Argentine photographs. Credits and unknown permissions are recorded in [implementation_art_notice.md](implementation_art_notice.md).

## Verification

- Installed-source validation: **PASS**, 8168 checks. This covers approval hash, installed hashes, BOM policy, references, localisation, sprites, portraits, registered leader ideologies, event namespaces, focus coordinates, prerequisite groups, exclusions and reward-preview separation.
- GDP price-contract validation: **PASS**, 1641 checks of invoices, preview/payment parity, own-GDP bases, weekly conversion and preserved non-monetary rewards.
- Compact layout validation: **PASS**, 672 checks of semantic preservation, unchanged non-focus runtime providers, parsed coordinates, card/connector footprints and the continuous-focus pocket.
- Independent emitted-code mechanics review: [runtime_mechanics_final_review.md](runtime_mechanics_final_review.md).
- Independent layout and browser-preview review: [runtime_layout_final_review.md](runtime_layout_final_review.md). The browser preview is an approximation, not an HOI4 screenshot.
- Isolated native HOI4 transaction fixture: **PASS**, 237/237 checkpoints. Status: `fixture_complete`. Feature-specific diagnostics: 0. Raw provider hash changes during run: 2; native script-body changes: 0. Concurrent Chile integration header comments were retained, with the exact parsed bodies compared against the frozen providers. The original private run record retains its raw hash-drift result; the repository result records the subsequent semantic review.
- Private profile: `D:\HOI4_Mod_Tools\mdcoldwar\runtime\argentina_1970\20261101_191504_751195`. The user explicitly authorized D: for this run because the prescribed E: drive was unavailable. Full logs and private scenario inputs stay outside the mod.

The native fixture uses controlled party slots, balances, embargo/sanction links and acceptance inputs. It checks actual runtime helpers, starting spirits, the Rosario war goal, party departure/return, payments from zero/negative treasury, one-time construction, twenty contract transactions, weekly aggregate contributions, paired suspension/restoration, coalition-resolution gates and annexation cleanup. These assertions do not constitute a human multiplayer session or prove every tooltip's exact rendering. A complete election campaign, an elapsed weekly budget tick, human in-game hover/navigation, a saved-campaign reload and simultaneous multiplayer interactions remain unperformed. Existing unrelated mod diagnostics were retained in the private error log and are not counted as Argentina feature errors.

## Rebuild and records

- Generator: `tools/argentina_1970/compile.py --install`.
- Source audit: `tools/argentina_1970/validate.py`.
- GDP price-contract audit: `tools/argentina_1970/validate_budget.py`; see [gdp_cost_audit.md](gdp_cost_audit.md) for the independent source review.
- Compact geometry and semantic audit: `tools/argentina_1970/validate_layout.py`; canonical layout is `tools/argentina_1970/layout.py`.
- Native fixture: `tools/argentina_1970/native_probe.py`; its default profile root remains on E:. D: is an explicit run override.
- Immutable approved input SHA-256: `bbfa7337ba2677c7f3939a09e1aa3b456caad8966dbf8d03369d262483006012`. The original approved input remains unchanged.
- 28 generated or narrowly integrated script/localisation files are hash-recorded in `tools/argentina_1970/manifest.json`. Art assets have their own companion provenance record.
