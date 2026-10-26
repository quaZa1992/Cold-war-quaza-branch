# January 1970 uranium districts and project-card correction

The start profile now contains **57 surveyed development districts**, selected against a strict **1 January 1970** knowledge cutoff. The [source register](uranium_1970_research.json) records the districts, the year by which they were known, direct historical sources, qualifications and 21 later-discovery exclusions. The register is not a claim to cover every uranium occurrence worldwide.

Every state still starts with **zero raw uranium and no built uranium mines**. This is the requested development rule; historical uranium mining certainly existed in 1970. Known districts permit construction and investment, and only working mines add production. Existing mine construction, investment, upkeep and power costs remain connected.

## Principal changes

| Area | January 1970 treatment |
| --- | --- |
| Nebraska | Removed from the starting survey profile. Crow Butte was discovered in 1980. |
| Saskatchewan | Reduced to two levels producing six units each. Beaverlodge and Rabbit Lake support the profile; later Key Lake, Cigar Lake and McArthur River discoveries do not. |
| Northern Territory | Rum Jungle and Ranger remain. Ranger was discovered in 1969; Nabarlek and Koongarra discoveries during 1970 are outside the cutoff. |
| South Australia | Added a small band for Beverley and older Radium Hill/Mount Painter districts. Olympic Dam and Honeymoon do not justify starting capacity. |
| Kazakhstan | Southern sandstone capacity reduced to one level producing four units, based on early prospects. The northern Aksu-Stepnogorsk group was moved from state 716 to state 714 after checking the actual province map. Southeastern Kurday/Kolzhat prospects add a separate small band in state 719. |
| Namibia and Niger | Retained known prospects with smaller bands. Later mine opening dates do not invalidate discoveries already known before 1970. |
| Brazil | Added a small Poços de Caldas band in Minas Gerais. Later Caetité and Itataia discoveries are excluded. |
| Argentina | Added the earlier Don Otto/Los Berthos and Schlagintweit districts; reduced Patagonia to the earlier Los Adobes prospect. |
| Older workings | Small bands in Katanga, Lower Silesia, Sughd and the Northwestern Territories represent alternative redevelopment or reprocessing in known historical districts. Their sources do not prove commercially viable remaining reserves in January 1970. Sughd has a particularly strong depletion qualification. |

Mine levels and resource output are **gameplay capacity bands**, not historical reserve tonnages. The deposit map now shows those actual construction and production values. Unsupported estimates in thousands of tonnes were removed from the 1970 initializer and map tooltip. The later-scenario compatibility table remains separate.

Primary examples: [Cameco's Crow Butte history](https://www.camecoresources.com/business/crow-butte), [Geoscience Australia's discovery chronology](https://webmap.ga.gov.au/pdf/RR0030.pdf), [South Australia's geological authority](https://www.energymining.sa.gov.au/industry/minerals-and-mining/mineral-commodities/uranium), [Volkovgeology's archival chronology](https://www.vg.kz/en/company/history/), and [the Brazilian CNEN history hosted by US DOE](https://www.energy.gov/sites/default/files/2018/10/f57/Mezrahi-Legacy-Uranium-Sites-Brazil.pdf). Each register row contains its own sources.

## Project card

The inherited MD layout placed the country-specific and generic project names at the same vertical coordinate. The card now uses separate title, generic-name, category, time and scientist rows. Text widths stop before the breakthrough-cost column; the research-speed panel clears both titles.

The fission project also uses a unique local sprite registration for the existing native bomb illustration. The original national project names remain intact. No new generated artwork or project-category change was needed.

## Verification and use

- **21 integration tests passed:** generated data/register agreement, date and state-ID guards, zero starting uranium/mines, map values, card geometry, native artwork resolution, encoding, actual economic arithmetic, mine damage/repair, supply shortages and all 50 human-only raid guards.
- The generator updates only the 1970 deposit initializer and balance record. It grants no resources or buildings and adds no recurring scans.
- Rebuild the profile with `python tools/quaza_nuclear_integration/build_1970_deposits.py`; run checks with `python tools/quaza_nuclear_integration/test_integration.py`.
- These latest changes have **not been visually verified in the game**. The previous interrupted native run does not verify this revision.
- **Start a new campaign** for the revised surveyed districts and zero-production histories. Existing saves retain their saved deposits and resources; no automatic save migration was added.
