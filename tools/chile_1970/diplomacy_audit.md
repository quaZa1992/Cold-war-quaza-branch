IMPERIA COLD WAR — Chile 1970 Diplomacy Audit

Scope: `tools/chile_1970/diplomacy.py`, its emitted diplomacy blocks, and `tools/chile_1970/test_diplomacy.py`. The frozen input is `tools/chile_1970/approved_design.json`. No generated game files were installed by this audit.

## Changes

- `diplomacy.py` reads the frozen approved design directly, rather than the concept design copy.
- Acceptance previews now show both sides' named spirits, setup and weekly payment amounts, buildings and extra slots, research bonuses, and a display-only numeric tooltip row for each signed modifier. The modifier rows use the compiler's existing `COLDWAR_CHL_mod_<stat>_tt` native formatter labels. They are inside `effect_tooltip`; the real payment and reward transaction remains separate.
- World-daily cleanup now removes active spirits and weekly costs and clears orphaned pending, awaiting, and collective ratification flags when Chile does not exist. A global transition flag makes cleanup run once per absence period and resets when Chile exists again. Paid and signed receipts remain, so restored treaties do not repeat their setup transaction.
- Each bilateral or collective pair-clear trigger now explicitly requires every recipient country to exist, so daily suspension takes effect when a participant disappears. The world helper uses the native `clr_global_flag` effect.
- Notice events now use each agreement's actual title and short description. Their option shows the complete acceptance terms through display-only numeric preview effects; payment and consent still occur only through the recipient decision flow.
- Tests now examine all nine frozen agreements, per-recipient accept/refuse visibility and payout guards, numeric preview data, once-only transaction guards, each collective participant's Cartagena spirit, all ten Andean pairs, eight mirrored Imperia sanction arrays, event notices, and cleanup behavior.

## Checks performed

- `python -m unittest tools.chile_1970.test_diplomacy -v`: all 6 tests pass.
- `python -m py_compile tools/chile_1970/diplomacy.py tools/chile_1970/test_diplomacy.py`: passes.
- The Clausewitz AST parser parses all six emitted script files. The localisation starts with `l_english:` followed by the exact project marker; generated player-facing localisation contains no en or em dashes.
- The transaction's top-level guard checks the paid receipt, Chile and recipient existence, actual recipient approval, the live relation/member conditions, and the asset-capacity helper before any setup payment, slot, building, research, spirit, or signed receipt effect. There is no treasury-affordability condition.
- Bilateral accept/refuse decisions are scoped to their named recipient. Collective approval is four independent recipient decisions. Execution occurs once in Chile scope after all four distinct ratifications and rechecks every participant pair and membership condition.
- Both directions of war, native embargo, and all eight mirrored sanction-array directions are present in the pair-clear trigger. The Cuba threshold is presented as “Relations with Cuba exceed -25.”
- Specific agreement notices have the same full preview helper as their focus and recipient decision, and no notice option executes setup costs or grants assets.

## Limits

These checks establish generator output and static AST consistency, not live HOI4 parser acceptance or tooltip rendering. The numeric modifier rows use the Chile compiler's shared tooltip localization keys; the compiled game localization and rendered signs still need an engine inspection. Building ownership, control, state-cap, and shared-slot checks are emitted by `compile.py`'s `can_build_*` triggers and are called from diplomacy guards, but were not revalidated in a live game here. The parent compiler/staging integration and root world-daily call remain outside this module's ownership.
