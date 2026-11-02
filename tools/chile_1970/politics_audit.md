IMPERIA COLD WAR — Chile 1970 Domestic Politics Audit

## Scope

This review covers the frozen approved input, `tools/chile_1970/politics.py`, its in-memory output mapping, and `tools/chile_1970/test_politics.py`. The module remains pure: importing it emits no runtime files.

## Implemented

- The September 1970 campaign event is available from 1 January through 3 September. The ballot reads the actual post-campaign native party array and counts each approved candidate ticket once. A simple majority is confirmed directly; otherwise Congress considers the plurality and a native coalition majority for the runner-up.
- Congressional coalition support is recalculated from `gov_coalition_array` and `party_pop_elect_array`. An unsuccessful alternative majority leaves the presidency unconfirmed and retries Congress after seven days.
- Inauguration runs from 3 November onward, without an artificial upper date. Native government changes and `update_set_politics` calls use `no_leader_change` guards. Leader routing preserves Frei before the 1970 ballot and routes actual ruling parties to available candidates.
- The 1988 plebiscite compares the approved native Yes and No party blocs. After a No result, the 1989 election counts eligible native candidate slots from `party_pop_elect_array`; ties remain unresolved. The handover installs the counted party and corresponding leader.
- Every event option now presents its material effects through `effect_tooltip` and rechecks its live scenario, party, focus, vote, and once-only conditions inside a guarded hidden transaction. Early civilian-transfer delays and congressional failure retain timed retries.
- Civic financial remedies show their numeric fees and package effects before selection, guard execution with the same availability conditions, and apply the approved 365-day restructuring burden and paid package. The funded public option records its $0.003 billion weekly expense for the active period. Stress-test re-entry becomes available after its 365-day receipt expires.
- Corrected temporary arithmetic, invalid clear-variable names, the stability trigger, native party slot ideologies, and verified Chile leader portraits.

## Checks

- `python -m unittest tools.chile_1970.test_politics -v`: 10 tests pass.
- `python -m py_compile tools/chile_1970/politics.py tools/chile_1970/test_politics.py`: passes.
- The Clausewitz AST parser parses every generated script. Portrait paths, approved event count, calendar guards, majority conditions, option previews, and transaction guards are checked in the tests.
- No HOI4 game was launched. The static checks establish generator output structure and source consistency; they do not establish live event rendering, engine parser acceptance, or save/reload behavior.
