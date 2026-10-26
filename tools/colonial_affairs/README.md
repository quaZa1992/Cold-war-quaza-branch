# Colonial Affairs — shared 1970 colonial administration

<!-- IMPERIA CW — Cold War: approved shared colonial administration and cabinet dossier. -->

The approved cabinet-file design is implemented as native decision-category scripted GUIs. Colonial powers use **Colonial Affairs**. Foreign players use **Resistance Contacts**, or open the regional file from the selected state. A native intelligence agency and a network **strictly above 50% in that exact state** are required for visibility and every transaction. Native occupation resistance is also eligible outside the historical colonial registry. Existing deliveries expire normally after network access is lost; further payments are blocked.

**Internal Security Cases** replaces the former IRA seven-slider simulation and its separate interface. Northern Ireland has a new regional organisation record. RAF contact files appear from **14 May 1970** in authored West German/West Berlin regions when the existing German RAF system is active. Aid feeds that existing cadre, sympathiser and attack-planning model. Its German security window remains the sole countermeasure interface; no second RAF incident or budget simulation is added. The new IRA uses regional strength, police appropriations and incidents; it does not turn core territory into a military occupation. Each has an emblem in the shared file. The IRA donor emblem is retained; other distinct archive badges are stylised identifiers, not purported reproductions of historical arms.

Colonial standing budgets are doubled against the initial implementation. Contested and armed administrations maintain resistance floors where native occupation resistance exists, with only rare, paid, temporary relaxation. A disclosure roll follows actual successful foreign aid: **10% political, 25% funding, 40% arms**. Disclosure notifies the responsible government and broadcasts a major news event using event-local sponsor and region identities; covert success does not automatically incur a public diplomatic penalty.

The registry covers **44 administrations, 94 map states and ten historical powers**: Australia, Denmark, France, the Netherlands, New Zealand, Portugal, South Africa, Spain, the United Kingdom and the United States. Associated territories, protectorates and integral overseas departments retain their existing status and receive no fabricated liberation war. Explicit historical and map limitations are documented in [HISTORY.md](HISTORY.md); this feature does not silently redraw the scenario.

## Rebuild and verification

```powershell
python tools/colonial_affairs/compile.py
python tools/colonial_affairs/validate.py
python tools/colonial_affairs/test_runtime.py
```

`compile.py --no-art` rebuilds runtime scripts and merges existing UI localisation without redrawing DDS assets. Canonical sources are `registry.json`, `runtime.py`, `contacts.py`, `retire_ira.py` and `ui.py`. Full UI rebuild uses Pillow and local Windows fonts. No global fonts or Soviet donor files are modified. Script files are UTF-8 without BOM; English localisation uses UTF-8 with BOM.

The compiler owns its named Colonial Affairs outputs, two bounded money/Sahara integrations, and the authorised old IRA retirement. `retired_ira/` preserves original custom sources outside game-loading folders. Unrelated British political institutions and the British national focus graph remain. Remaining historical focus/event rewards consume the new Northern Ireland organisation strength; old foreign-action duplicates, the two obsolete Libyan IRA delivery focuses, and the old countermeasure UI are removed. Legacy modifier/idea identifiers have inert migration definitions so old saves can remove them without restoring their effects. Other feature generators must not restore the retired modules.

`manifest.json`, `validation.json`, `runtime_tests.json` and `ui_geometry_review.json` record source/model checks. `ui_preview/` contains composites rendered from parsed native GUI coordinates. These are approximate previews, not screenshots of a running HOI4 session.

## Runtime

See [RUNTIME.md](RUNTIME.md) for exact policy multipliers, local modifiers, resistance stages, aid prices, cleanup and provider contracts. Recurring budgets use the existing MD weekly expense account. Grants and funding use the actual treasury effect; arms consume MD infantry and command-and-control equipment. Foreign resistance assistance has a shared 15-point maximum per affected state and blocked payments at the cap.

The daily observer initializes existing 1970 saves lazily, but a **fresh January 1970 campaign is the intended complete start**. In particular, state-history ownership corrections are not retroactively imposed on existing saves. Startup receipts prevent reopening a save from decrementing a second policy/concern day through this feature's startup callback.

No native HOI4 load, hover, save/reload or multiplayer synchronization test has been performed. First engine checks should cover the 510×740 category envelope, adjacent state-view controls, portrait/flag fallback, an exact-cost aid package, a petition left open beyond its expiry, partial independence and the weekly economy breakdown. The source model deliberately does not simulate native occupation evolution, AI decisions or networking.

## Recorded limits

- Papua/New Guinea's mainland and Diego Garcia have pre-existing map/status mismatches; the registry records them explicitly instead of imposing a new ownership settlement.
- One grouped administration simultaneously divided between unrelated foreign powers currently follows one administrator and only counts its retained eligible states. Normal native independence, protected-state independence and a complete foreign takeover are covered.
- Numerical budgets are authored gameplay values, not claims about historical annual accounts. Performance and financial balance still require a running campaign check.
