# North Korea 1970 implementation

The user approved implementation of `docs/COLDWAR_NKO_1970_concept/v2/COLDWAR_NKO_v2_design.json`, then authorized the screenshot fixes and a substantial expansion, explicitly waiving the earlier focus-count limit. The installed design now has **360 focuses**, including dedicated Chinese and Soviet programmes. `design.py` applies the authorized amendments without changing the original approval snapshot. `current_design.json` is the complete exported design used by the emitted-source validator and independent review. The current status is recorded in `docs/COLDWAR_NKO_1970_concept/IMPLEMENTATION.md`.

From the mod root, using Python with Pillow:

```powershell
python tools/north_korea_1970/compile.py
python tools/north_korea_1970/validate.py --check-rebuild
python tools/north_korea_1970/succession.py --check
python tools/north_korea_1970/preview.py
```

`compile.py` emits 360 focuses, their guards, rewards, programme modifiers, domestic adapters and English localisation. `expansion.py` owns the 162-focus national extension and imports the disjoint political, defence and patron modules. `agreements.py` emits the 15 reciprocal agreements, recipient decisions, paired modifiers, feedback and weekly expenses. `succession.py` emits the historical transfer/news event and converts the approved restoration to the native 410×164 BC3 news texture. It does not generate a new photograph. `preview.py` renders the emitted tree with native title glyphs and art into `docs/COLDWAR_NKO_1970_concept/expansion/`; it does not launch HOI4 or claim exact connector routing.

The compiler also applies six narrow shared integrations: NKO history, the central MD party-change callback, the native additional-expense calculation, Imperia sanction reconciliation, the generic-tree fallback exemption, and the native flat army-experience tooltip formatter. These patches preserve surrounding content and line endings. The manifest records every installed output and its SHA-256 digest. Rebuilding should produce the same bytes.

Game scripts use UTF-8 without BOM. Localisation uses UTF-8 with one BOM. The formatter/parser imported from `tools/vietnam_1970/script_ast.py` handles this emitter's script subset; importing it does not rebuild Vietnam.

The source validator compares the emitted graph and modifiers with the current model and checks preservation of the approval snapshot's dependencies, rewards and relative structure. It checks every node's satisfiable prerequisites/exclusions, card bounds, helper/event/localisation references, decision icons, textures, decimal precision and shared-hook uniqueness. Its 1,149 transaction/lifecycle cases exercise all 162 new executors, party return, required agreement spirits, consent, suspension and replay prevention against the native money/building interfaces. It is **not the HOI4 parser or campaign engine**. It does not establish multiplayer synchronization, native tooltip layout, automatic debt timing or save/load callback timing. Do not treat old game logs as a test of these newly emitted files.

Keep one-time payments and construction in receipt-guarded executors. Refresh helpers may only reconcile already-earned programmes and outstanding offers; they must never repeat an accepted contract's initial reward. Preserve both signatories' acceptance receipts when sanctions or war suspend cooperation.
