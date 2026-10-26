# Qatar: 1970 historical identity repair

The reported country panel had a Western government but no named civilian
leader. The installed dated history and recruited character still used
`Kingdom` (MD subparty10). Its historical native selector also handled only
subparty10. MD's normal `set_leader` removes the current leader before asking
the country selector for its replacement; the Qatar selector had no Western0
replacement. A valid portrait texture therefore did not establish a valid
active leader for the displayed outlook.

The bounded owner is `qatar_identity.py --install`. The dated1970 history,
character role, promotion, native ruler pool, counter sync and party display
now agree on `Western_Autocracy`, Western Outlook, subparty0. This is the
1970 British-protected ruling-house adaptation, not a claim that main MD's
modern Qatar belongs to that family. The actual named ruler remains Ahmad bin
Ali Al Thani with the previously reviewed portrait. The existing character
expiry22February1972 is retained. No automatic coup or new succession event
was added; approved native retirement behaviour remains available.

Primary ruler evidence:

- [Amiri Diwan: Ahmad bin Ali Al Thani,1960–1972](https://www.diwan.gov.qa/about-qatar/qatars-rulers/sheikh-ahmad-bin-ali-al-thani?sc_lang=en)
- [Amiri Diwan: Khalifa bin Hamad, accession22February1972](https://www.diwan.gov.qa/en/about-qatar/qatars-rulers/sheikh-khalifa-bin-hamad-al-thani)

The adapter changes Qatar branches only in shared loaded files, keeps the
modern native country-selector fallback, and preserves the2000 history tail.
It adds no startup identity replacement, forced daily government restoration
or change to Saudi Arabia or Oman. `monarchy_alignment.apply_country` and
`starting_identity.normalise_native_seed` apply the same bounded mapping so
later canonical generation does not reintroduce the mismatch.

Verification:

- `test_qatar_identity.py`:205 assertions, including actual dated recruitment,
  matching role/government/subparty, existing expiry, resolved portrait,
  actual native replacement bodies, unchanged modern fallback, unchanged
  non-Qatar catalogue entries and byte-stable bounded regeneration.
- `test_starting_identity.py`:3,045 checks,397country files,163active identities.
- `test_monarchy_alignment.py`:154 checks; existing four-country adapter stays
  reproducible.
- `test_monarchy_runtime.py`:43 checks; existing other-country pools retained.
- No live HOI4 menu or start was inspected. A fresh1970start after restarting
  HOI4 is the remaining engine check.

An initial import accidentally selected Vietnam's validation module because
the shared AST helper prepended its directory. That module ran its30,444
passing assertions and refreshed only `tools/vietnam_1970/validation.json`;
its source contains no loaded-game output writes. The adapter now restores
its own module directory's precedence before loading the party formatter.
