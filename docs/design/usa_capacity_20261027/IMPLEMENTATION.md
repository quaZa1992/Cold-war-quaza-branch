IMPERIA COLD WAR

# USA focus building-capacity correction, 27 October 2026

The reported focus is `USA_1970_1976_dem_2_a_national_energy_effort`. Its legacy capacity and execution guards asked `free_building_slots` whether Texas 800, Colorado 804 and California 811 could manually construct renewable energy. That query includes technology-unlocked construction levels. The 1970 country setup does not grant `fuel_silos`; the similarly named entry in USA history belongs to 2000. The tech enables renewable construction up to 20 and has a 1985 tech year. A manual permission result of 0 therefore does not establish that the states physically contain 20 renewable levels.

The canonical `usa_building_capacity.py` now checks independent state building grants against the loaded physical state cap using `building_level@<type> <= state_max - granted_levels`. The screenshot's three one-level grants each require an existing level at most 19. Infrastructure uses its actual six-level cap, including the two-level condition of at most 4. Fossil power, nuclear plants and fuel silos use their own current definitions. Shared-slot and exact province-building queries retain their existing native predicates.

The public requirements and real execution/retry guards use the same capacity logic. Six English requirement entries display the number of additional levels and the physical state limit. There is no raw dynamic-variable name or incorrect 'Can build 0 more' manual-construction requirement for these independent state grants.

The independent source review verified 70 correctly bounded physical-cap wrappers and 203 unchanged shared/province slot queries across the targeted USA providers. After normalising only the intended capacity replacement, the remaining trigger AST is unchanged. Ownership, control, party, scenario and once-only receipts remain. The national tree and reward effects are unchanged: one extra same-state shared slot before each plant, the original buildings, modifiers and $25.5 billion invoice. The Democratic Party requirement of this particular programme remains a real condition.

`CHECKS.json` records eight dedicated capacity regressions, fifteen domestic regressions, the installed USA integration validator and a byte-identical canonical rebuild. The regression model explicitly distinguishes manual tech entitlement 0 from physical building room; the previous permissive free-slot model did not establish that distinction. Exact-limit cases, all three state targets, lost ownership/control, multi-level grants, party/receipt preservation, province-specific ports and complete English providers are covered.

## Native evidence boundary

The single-launch A/B fixture has 33 assertions prepared in `tools/usa_1970_expansion/capacity_native_probe.py`. Its frozen baseline, addon and profile are on `E:/HOI4_Mod_Tools/mdcoldwar/runtime/usa_capacity_20261027`, outside the mod. It compares the real baseline with the candidate predicate and tests full grants, the original invoice, repetition and a full state. A separate diagnostic toggles the technology only inside the private fixture.

No native probe was launched: an elevated inventory found an existing ordinary user HOI4 process. Its process, playset and saves were left untouched. `NATIVE_PENDING.json` records this and explicitly reports zero newly created engine processes. The current fix has source/model verification and independent review, without a live hover, existing-save load, debt-tick, queued-construction or multiplayer claim. `building_level@...` is a documented existing-level accessor; it is not advertised as a native queued-level reservation API.

The running game must load the changed scripts on restart. No country history, tech unlock, dated election receipt, construction price or reward amount is changed by this correction.

## Source and provenance

Providers: current `common/buildings/00_buildings.txt` (renewable cap 20, infrastructure cap 6), `common/technologies/industry.txt` (`fuel_silos` unlock), `history/countries/USA - USA.txt` (separate 1970/2000 blocks), and installed Paradox documentation `dynamic_variables_documentation.md` state `building_level` plus `triggers_documentation.md` entries `check_variable` and `free_building_slots`. Current MD economic and raid scripts independently read the same dynamic building-level accessor.

This is an IMPERIA COLD WAR script correction to existing project/MD content. Original individual authors and separate applicable third-party permissions are unknown where existing notices do not identify them; the project marker establishes no new rights. No art, font, state-history asset or binary is added or edited. Compact diagnostic hashes are in `CHECKS.json`; the retained private baseline stays on E:.
