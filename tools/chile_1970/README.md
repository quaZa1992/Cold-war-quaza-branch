IMPERIA COLD WAR

# Chile 1970 national programme

The approved 184-focus design is frozen in `approved_design.json`. The approval snapshot and the original concept viewer remain unchanged. The user subsequently authorized installation. This folder contains the bounded compiler, domestic politics and treaty modules, independent emitted-script checks and an optional isolated native probe.

The current user-requested revision is applied by `current_design.py`: `cost_revision.py` calibrates all monetary fields to the measured 1970 GDP, `layout_revision.py` packs the tree into three bands, and `chile_presentation.py` hides technical predicates while retaining their execution. `political_revision.py` and `politics.py` add the player-directed military transition without elections. The revision inputs are hashed in the installation manifest. See `FOLLOWUP_20261031.md` and `PINOCHET_ROUTE_20261101.md` in the design documentation directory.

Run from the mod root using an available Python 3 interpreter:

```text
python tools/chile_1970/compile.py --install
python tools/chile_1970/validate.py --installed
python -m unittest tools.chile_1970.test_diplomacy tools.chile_1970.test_politics tools.chile_1970.test_elections tools.chile_1970.test_costs tools.chile_1970.test_presentation tools.chile_1970.test_transition -v
python tools/chile_1970/preview.py
```

Without `--install`, the compiler writes its review output under `stage`. The manifest identifies which output is current. Do not run the original concept generator as an implementation build. It owns earlier review materials rather than the installed scripts.

The compiler changes only its Chile outputs and six marked integration blocks: Chile's 1970 history, the Chile leader route, the shared early leader dispatcher, historical retirement eligibility, the native party setter and weekly additional expenses. It does not regenerate other countries or modify shared UI or artwork.

Own expenditure uses MD's native treasury effect and permits borrowing. Party programmes retain earned receipts and variables while their dynamic modifier and recurring fee follow the actual ruling party. One-time buildings, research and fees are never part of a programme refresh. Standing agreements use recipient consent and preserve setup receipts while both sides' benefits and recurring fees suspend and restore together.

See `docs/CHILE_COLDWAR_CONCEPT_1970_1990/IMPLEMENTATION.md` for scope, policy precedents, deviations and final verification. Original research and design audits in that directory retain their historical concept-only status. The implementation record supersedes that status without rewriting the approval snapshot.

The user explicitly chose to omit the native HOI4 test because the required E: runtime drive was unavailable. Do not redirect the native probe to another drive without authorization. No native profile was prepared and no engine verification is claimed.

`Chile: Political Transition` contains `Secure the Officer Corps`: 100 political power and 90 days of preparation. The existing constitutional crisis then offers civilian guarantees or military takeover; the existing junta event selects collective authority or Augusto Pinochet. The route requires civilian, independent Chile with Santiago owned and controlled, no civil war and no capitulation. It does not require an election, Allende, low stability or the 1973 crisis window. A coup permanently supersedes the old 1970 ballot chain, including already-open events and ratified candidates. Cancellation permits a new paid preparation after conditions recover; a completed constitutional settlement cannot be replayed.
