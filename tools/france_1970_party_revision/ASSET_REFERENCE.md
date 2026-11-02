IMPERIA COLD WAR

# France 1970 party partnerships: verified asset locations

Design reference only. The state IDs, owner/controller, state category, and listed building levels come from the current local `history/states` files. Each listed state has an explicit `1970.1.1` owner and controller override matching the intended partner. The building totals below count existing buildings whose current `common/buildings/00_buildings.txt` definition says `shares_slots = yes`; they are static-history calculations, not a live-game measurement. The target building definitions cap both `industrial_complex` and `offices` at 50 levels per state. Runtime acceptance must still recheck state ownership, control, full control, building level caps, state slots, and partner eligibility before either side pays or receives an asset.

The project rule for grants remains: add one shared state building slot per granted building level before adding a shared-slot building. That slot grant belongs inside the same one-time guarded transaction. Adding a slot to infrastructure, land forts, or coastal forts is also required by the project rule, even though those types do not consume shared slots.

| Partner | Intended target | Verified state | Target building | Existing shared-slot buildings | Category slots | Static headroom | Sources |
|---|---|---:|---|---:|---:|---:|---|
| SOV | Kazan / Tatarstan machine-tool compact | 661, Tartarstan | industrial complex | 4 (3 industry, 1 arms) | 14 | 10 | [state file](../../history/states/661-Tartarstan.txt:2), [Kazan province marker](../../history/states/661-Tartarstan.txt:47), [category](../../common/state_category/state_04.txt:3) |
| SOV | Moscow office | 652, Moscow | offices | 23 (16 industry, 3 arms, 4 offices) | 33 | 10 | [state file](../../history/states/652-Moscow.txt:2), [category](../../common/state_category/state_09.txt:3) |
| USA | California electronics office | 811, California | offices | 29 potential (10 industry, 5 arms, 2 dockyards, 5 offices, 6 agriculture, 1 DLC-gated naval headquarters) | 51 | 22 conservative (23 without the DLC building) | [state file](../../history/states/811-California.txt:2), [category](../../common/state_category/state_14.txt:3) |
| ENG | Southern England / London office | 13, Greater London | offices | 10 (4 industry, 5 offices, 1 agriculture) | 26 | 16 | [state file](../../history/states/13-Greater%20London.txt:2), [category](../../common/state_category/state_07.txt:3) |
| ITA | Emilia-Romagna cooperative office | 265, Romagna | offices | 6 (4 industry, 2 offices) | 18 | 12 | [state file](../../history/states/265-Romagna.txt:2), [Bologna province](../../history/states/265-Romagna.txt:8), [category](../../common/state_category/state_05.txt:3) |
| ALG | Capital-area civilian factory | 386, Algérois | industrial complex | 4 (2 industry, 1 office, 1 agriculture) | 22 | 18 | [state file](../../history/states/386-Algerois.txt:2), [category](../../common/state_category/state_06.txt:3) |
| ALG | Oran civilian factory | 387, Oranais | industrial complex | 1 (1 industry) | 22 | 21 | [state file](../../history/states/387-Oranais.txt:2), [Oran province](../../history/states/387-Oranais.txt:19), [category](../../common/state_category/state_06.txt:3) |

The 1970 overrides are explicit at: Tatarstan [54-56](../../history/states/661-Tartarstan.txt:54), Moscow [40-43](../../history/states/652-Moscow.txt:40), California [133-136](../../history/states/811-California.txt:133), Greater London [53-56](../../history/states/13-Greater%20London.txt:53), Romagna [68-71](../../history/states/265-Romagna.txt:68), Algérois [41-44](../../history/states/386-Algerois.txt:41), and Oranais [50-53](../../history/states/387-Oranais.txt:50). Each override sets the named state owner and controller to its partner tag. Static state capacity comes from the linked category definitions; all listed buildings consume shared slots in the current local definitions. The proposal should choose at most one recipient asset per state in any one transaction. Algérois and Oranais are separate alternatives and should not both be awarded by a single Algeria agreement unless the approved design explicitly calls for two distinct sites.

### Site naming and source limits

- State 661 is named `Tartarstan`, not Kazan. Its province 6338 has the local `terrain_kazan` modifier, which supports describing the site as Kazan/Tatarstan.
- State 265 is named `Romagna`, not Emilia-Romagna. The file identifies Bologna (province 304) as its victory-point center. Use “Romagna” for the verified state name and “Emilia-Romagna” only as a broader regional description.
- State 386 is `Algérois` and includes Algiers province 1145. State 387 is `Oranais` and includes Oran province 7132.
- Existing ordinary building levels are read from the state history building blocks. The dated 1970 blocks explicitly establish owner/controller, but do not restate ordinary factory/office levels. Treat the slot counts as a pre-start source estimate and recheck the loaded 1970 state before execution.
- A proposal’s slot grant makes one additional slot available per granted level, but it does not waive native per-building caps, full-control checks, changed ownership, or a transaction-wide preflight of both countries before charging either side.

### Partner country tags

| Country requested | Current tag | Source |
|---|---|---|
| Soviet Union / Russia | `SOV` | [country tags](../../common/country_tags/00_countries.txt:49) |
| United States | `USA` | [country tags](../../common/country_tags/00_countries.txt:142) |
| United Kingdom | `ENG` | [country tags](../../common/country_tags/00_countries.txt:13) |
| Italy | `ITA` | [country tags](../../common/country_tags/00_countries.txt:29) |
| Algeria | `ALG` | [country tags](../../common/country_tags/00_countries.txt:185) |
| Austria | `AUS` | [country tags](../../common/country_tags/00_countries.txt:4) |
| Argentina | `ARG` | [country tags](../../common/country_tags/00_countries.txt:163) |
| Yugoslavia | No current country tag `YUG` is registered. Current Serbia uses `SER`; its history file applies the cosmetic tag `YUG_Coldwar_Communism`. Use `SER` only if the intended participant is the current Serbia country object. | [country tags](../../common/country_tags/00_countries.txt), [Serbia history](../../history/countries/SER%20-%20Serbia.txt:12) |
