IMPERIA COLD WAR

# Cross-country building-capacity audit, 27 October 2026

The same hidden dependency on manual building permissions exists outside the repaired USA programmes. The read-only inventory examined 21 authored 1970 tree providers, direct queries, execution helpers, shared native grant helpers and associated delivery paths. A raw search found 629 nonshared-state queries without an explicit province in 78 files across the entire mod, including unused modern trees and ordinary investment systems. Those 629 matches are candidates, not 629 confirmed bugs.

`INVENTORY.json` records the complete source scan, active country-tree references, exact locations and native-helper chains. `FINDINGS.json` contains the reviewed country groups and exact focus IDs. Original game scripts, generators, approval inputs, party rules, prices and assets were not changed in this audit. No game was launched.

## Confirmed source-level coupling in scripted grants

| Country/provider | Reviewed affected focus/programme paths | Mechanism |
| --- | ---: | --- |
| Soviet Union |30 focuses|Native random-state helpers for infrastructure, reactors, renewables, fuel reserves and air defence. Their internal selectors use technology-limited free slots. |
| DDR |35 focuses|The same native helper chain, also including radar programmes. |
| Soviet republics shared tree |17 focuses|Infrastructure+1 in availability, prospective selection and actual execution.68 query sites across tree/reward providers. |
| Egypt |16 focuses|23 helper calls:17 infrastructure,4 renewable and 2 air-defence grants. Their ancestor chains do not establish the corresponding technologies. |
| Generic 1970 tree |37 focuses|Technology-dependent native selectors for scripted grants; the affected caller need not display the capacity requirement itself. |
| Israel |12 direct focuses|Instant infrastructure+1 after one extra shared slot; existing infrastructure 3 is below the physical cap 6. |
| Iraq |20 focus reward helpers|18 infrastructure and 2 fuel-silo programmes. Their component receipts and pending delivery keep failed grants before payment. |
| Cuba |2 focus/agreement paths|Havana port programme's silo and Soviet air-defence agreement's radar. Real recipient consent and delivery receipts remain necessary. |
| Syria |3 focuses|Euphrates Power, Mainline Upgrades and Connect Consumers. Instant renewables/infrastructure, with the same capacity condition repeated in delivery guards. |
| Libya |1 conditional focus reward|A Revolutionary Administration can complete while its internet-station component is skipped by the manual-construction query. |
| Greece |1 radar focus|The 1945 radar technology is absent from the inspected start setup; an undisclosed research dependency can block the promised installation. |

These are distinct source paths, not a claim that every alternative party branch is simultaneously available. Existing save technology can satisfy a query, and a genuinely full state must still block construction. The audited mechanism is the implicit technology limit for promised scripted assets, not a universal defect in `free_building_slots`.

For example, the shared infrastructure selector can return no eligible state when the relevant manually buildable level comes from 1985 or later, despite a physical cap 6. An instant grant can instead use the actual state building level and the complete grant quantity. Two- or three-state random grants usually give one level per selected state: their per-state physical ceiling remains cap minus 1, not cap minus the number of states.

Several shared native helpers place their own charge outside successful state selection. SOV/DDR and generic callers may suppress that flat charge and apply a separate GDP invoice. Therefore the defect can omit a promised asset while a policy fee and other real rewards still apply. It is inaccurate to call every such focus completely empty or to claim every caller pays the same native flat price. Four generic green-policy focuses explicitly skip the helper's$8.5 billion charge and apply their own 1.1%GDP policy invoice. The strategic-reserves and first-nuclear-station callers instead leave the native$3/$9 billion helper fees enabled.

## Different contracts requiring separate treatment

Israel has 18 additional funded project decisions with 19 infrastructure predicates. They wait 180 to 330 days, then grant buildings instantly. Both starting and delivering the project use the problematic capacity condition. Most grant+1; the two entrenchment-network projects grant+2 and need a physical cap minus 2 check. These are not ordinary construction-queue items.

Greece's `COLDWAR_GRE_1970_economy_18` and Vietnam's `COLDWAR_VIE_kiet_transport`, `COLDWAR_VIE_industry_roads`, `COLDWAR_VIE_farm_dykes` use `instant_build=no`. Their start-state infrastructure and missing manual technologies explain the source-level locks, but simply replacing the focus predicate may leave the native queued construction blocked. Vietnam's `COLDWAR_VIE_army_airdefence` similarly uses a normal air-defence queue with missing early unlocks. These need their own queue-aware correction and native verification.

Not confirmed as the same unintended defect:

- Japan already uses physical state-level limits. Its current reward revision adds explicit researched-technology conditions for specialised buildings. That is a separately authored research contract.
- France's examined national programmes contain no direct building constructions or these slot predicates.
- Germany's Gronau enrichment reward explicitly checks `nuclear_technology` and supplies a research-project fallback. Spain's nuclear investment confirmation explicitly requires `reactor1`. Egypt's El Dabaa reactor likewise explicitly requires `reactor1`; that focus is excluded from Egypt's 16 above.
- Ordinary shared building slots and exact province naval-base predicates remain appropriate to their scope. Cyprus's Famagusta harbour is a queued provincial project, not this independent-state-grant case.
- Air bases, fossil plants and civilian shelters have no corresponding `enable_building` provider in the inspected technology inventory. Their mere appearance in a nonshared-slot query is insufficient evidence of this same research-limit bug. This excludes the inspected UAE aviation hub, Iraqi/Cuban fossil programmes and Soviet shelter case from the confirmed technology-coupling group.

## Canonical repair points

The audit identifies these sources for a later authorised repair, without executing them:

- SOV/DDR/EGY: their `Claude outputs/COLDWAR_<TAG>_generator/cw_effects.py` or DDR`dg_effects.py` native building-helper dispatches. Use country-focus grant adapters rather than modifying every MD manual investment helper globally.
- Soviet republics: `tools/ssr_1970/compile.py`, `building_state_limit()`, shared by focus availability, preview selection and real reward selection.
- Israel: `tools/israel_1970/build_content.py`, `building_gate()`, and `policy_common.py`'s common funded-project validity predicate.
- Iraq: `tools/iraq_1970/compile.py`, capacity generation, plus `reward_overhaul.py` building components and their original credit/receipt guards.
- Cuba: `tools/cuba_1970/compile.py`, `economic_guard()`, and `diplomacy.py`'s offer/acceptance/radar project checks.
- Syria: generated guard content owned by `tools/syria_1970` and its current design/reward pipeline. The actual three focus IDs and all delivery copies are in `FINDINGS.json`.
- Generic 1970 and Libya: preserve original source attribution. The exact authoritative generator for these legacy tree sections was not established; do not invent one or rewrite an immutable approval record.

Every later correction must preserve actual ownership/control, province identity, funding contracts, both parties' consent where applicable, full building quantities, one-time receipts and additional same-state slots. Removing a visible condition without fixing the authoritative execution or delivery selector would leave the bug in place.

## Evidence and provenance

Three independent read-only reviews traced the assigned country groups. Detailed generic/IRQ/CUB observations and unchanged source hashes are also recorded in `../usa_capacity_20261027/OTHER_COUNTRIES_READONLY.md` and its JSON companion. The inventory and reviewed findings distinguish source-confirmed coupling from untested runtime outcomes. No existing-save hover, native queued-construction test or multiplayer test was performed.

All evidence is from the current local IMPERIA COLD WAR runtime, its canonical source files and installed Paradox scripting documentation. Existing MD/Paradox/project authorship remains as recorded in the original providers. Separate individual credits/licence or permissions are unknown where the existing notices do not establish them. No third-party image, font or other binary asset was copied. The project marker asserts no new rights.
