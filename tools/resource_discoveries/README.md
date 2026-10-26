# IMPERIA CW — Cold War: Resource discovery lottery

The two original monthly branches remain: weight 5 for peaceful human countries
without Developed Economy and internal GDP below 1,000; weight 5 for peaceful human
countries with Resource Extraction Mandate, regardless of development level; weight 90
for no discovery. The global counter must exceed 40. Coastal and capital states
remain excluded. The counter still resets when the owner claims a discovery.

<!-- IMPERIA COLD WAR: Mandate eligibility explicitly includes developed economies. -->
The mandate can be selected by developed economies as well. Its discovery branch
has no GDP or development-level restriction. The normal branch retains both gates;
neither route guarantees a discovery. Selection costs and the four-year commitment
remain unchanged.

Discovery amounts no longer use that counter. A successful draw selects one of five
mineral/fuel resource categories with equal weights, plus rubber with the same
weight where suitable. Sizes then have weights 65/30/5 and multipliers 1/2/3:

| Resource | Small | Medium | Large |
|---|---:|---:|---:|
| Oil | 16 | 32 | 48 |
| Steel | 12 | 24 | 36 |
| Aluminium | 8 | 16 | 24 |
| Technology Metals | 8 | 16 | 24 |
| Precious Metals | 4 | 8 | 12 |
| Rubber | 8 | 16 | 24 |

Rubber eligibility uses an existing rubber deposit or the bounded regional list in
`balance.json`: tropical production areas in Asia, Africa and the Americas. This
is a coarse gameplay suitability check, not a claim that every province in those
regions is agronomically suitable. The report describes new rubber-growing land,
not an underground rubber deposit. Microchips, composites and the separate uranium
mine system are excluded.

Type and quantity are stored on the selected state before the major news event.
An unanswered result excludes only that state from another selection, preserving
its result. Owner confirmation adds the selected resource once and clears its
pending flag. Observer options do not award anything. Stored type and quantity
remain for news display. An already-open old-save event with no prepared result
rolls a bounded result when claimed. Quantities never depend on a delayed click or
another country's counter reset. Existing native resource modifiers can affect the
final displayed output after the base addition.

No new recurring hooks or country/state loops are added. Two small weighted draws
run only after a successful original monthly selection. Standard resource expansion
decisions, payments, original news artwork and resource-rights diplomacy remain.

Run `python tools/resource_discoveries/build.py` to regenerate the two owned helper
files, or `--check` to check synchronization. Run
`python tools/resource_discoveries/test_discoveries.py` for emitted-script tests.
The test interpreter fails on unsupported authored commands. Native event rendering,
save/load and multiplayer synchronization still require an HOI4 engine session.
