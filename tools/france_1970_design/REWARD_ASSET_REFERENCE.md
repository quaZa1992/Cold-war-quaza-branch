IMPERIA COLD WAR

# France 1970 reward asset reference

Read-only source reference for adding tangible rewards to the fixed 152-focus concept. No state history, concept, generator, or live game file was changed. Source of truth for 1970 France is this mod's `history/states` and `history/countries/FRA - France.txt`; MD's 2000 France tree is used only as a reward pattern. State and province IDs from its 2000 tree are not interchangeable with the 1970 map.

## Buildings and native construction progression

| Building | MD cap and shared slot behavior | Native enabling tech in current MD |
|---|---|---|
| `offices` | State cap 50; shares slots. No explicit building-enable tech found. | No `enable_building` entry found. |
| `internet_station` | State cap 11; no shared-slot flag. | `internet_1` enables level 1, tech start year 1975; `internet_2` level 2, 1990; then levels 3 to 11 in `internet_3` to `internet_11`, 2000 to 2080 in 10-year steps. |
| `agriculture_district` | State cap 10; shares slots. Each level contributes fuel and local supply modifiers in the building definition. No explicit enable tech found. | No `enable_building` entry found. |
| `rail_terminal` | State cap 5; no shared-slot flag. Each level adds state productivity, local supply and local slot-factor modifiers. | `railway_system_02` enables level 1, tech start year 1990; `_04` level 2, 2000; `_05` level 3, 2005; `_06` level 4, 2010; `_08` level 5, 2025. `_03` and `_07` do not grant terminal levels. |
| `radar_station` | State cap 6; no shared-slot flag. | `radar` enables level 6, tech start year 1945. |
| `fuel_silo` | State cap 5; explicitly `shares_slots = no`. | `fuel_silos` enables level 5, tech start year 1985. |
| `air_base` | State cap 10; no shared-slot flag. | No explicit building-enable tech found. |
| `dockyard` | State cap 20; shares slots; coastal states only. | No explicit building-enable tech found. |
| `infrastructure` | State cap 6; no shared-slot flag. | `railway_system_01` enables level 1, tech start year 1985; `_02` level 2, 1990; `_04` level 3, 2000; `_05` level 4, 2005; `_06` level 5, 2010. No separate level 6 enable was found in this series. |
| `naval_base` | Province cap 10; coastal provinces only; separate from state-level `dockyard`. | No explicit building-enable tech found. |

The tech `start_year` is the technology's base year, not a hard ban on earlier research. Existing state-history levels can predate their construction tech: for example, the 1970 files already set `infrastructure = 2` or `3` and include two `fuel_silo` levels, while the construction technologies begin in 1985. Treat the tech links as the native construction progression, not proof that a prebuilt 1970 level is invalid.

Source anchors: MD `common/buildings/00_buildings.txt:75-107,109-151,233-281,255-264,369-389,746-761`; MD `common/technologies/engineering.txt:3705-4880`; MD `common/technologies/industry.txt:2057-2080,7030-7355`.

## Metropolitan France at the 1970 start

The state files below set `owner = FRA` and `controller = FRA` in their `1970.1.1` block. `buildings_max_level_factor = 1.000` is recorded for each. Slot capacity is the state's category value in `common/state_category`; occupied slots count only built types whose MD definition sets `shares_slots = yes` among the initial stock. Free slots are the static category capacity minus that usage, before dynamic/global slot modifiers. The per-focus project rule still adds one shared slot per granted level, even for types that do not consume slots.

| State | Category slots | Used / free | Offices | Agriculture | Infrastructure | Air base | Radar | Fuel silo | Dockyard |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 54 Haute-de-France | 22 | 5 / 17 | 1 | 2 | 3 | 10 | 0 | 1 | 0 |
| 55 Normandie | 14 | 2 / 12 | 1 | 0 | 3 | 10 | 0 | 0 | 0 |
| 56 Ile de France | 33 | 11 / 22 | 3 | 1 | 3 | 5 | 0 | 0 | 0 |
| 57 Alsace-Lorraine | 14 | 2 / 12 | 1 | 0 | 3 | 5 | 0 | 0 | 0 |
| 58 Bourgogne | 10 | 1 / 9 | 0 | 1 | 3 | 2 | 0 | 0 | 0 |
| 59 Loire | 10 | 3 / 7 | 1 | 1 | 3 | 2 | 0 | 0 | 0 |
| 60 Aquitaine | 14 | 3 / 11 | 1 | 0 | 3 | 3 | 0 | 0 | 0 |
| 61 Midi Pyrenees | 14 | 2 / 12 | 1 | 0 | 3 | 2 | 0 | 0 | 0 |
| 62 Rhone-Alpes | 18 | 5 / 13 | 1 | 0 | 3 | 4 | 0 | 0 | 0 |
| 63 Provence | 18 | 5 / 13 | 1 | 0 | 3 | 10 | 2 | 0 | 0 |
| 64 Bretagne | 14 | 6 / 8 | 1 | 1 | 2 | 10 | 1 | 0 | 2 |
| 65 Corsica | 4 | 0 / 4 | 0 | 0 | 2 | 1 | 0 | 0 | 0 |

`internet_station` and `rail_terminal` are level 0 in all twelve metropolitan files. Shared-slot occupancy includes industrial complexes and arms factories as well as offices, agriculture districts, and dockyards. Non-shared initial assets such as air bases, infrastructure, radar, nuclear reactors, fuel silos, renewable infrastructure and provincial naval bases do not reduce these table's shared-slot headroom. State-category anchors: `common/state_category/state_01.txt:4` (4 slots), `state_03.txt:4` (10), `state_04.txt:4` (14), `state_05.txt:4` (18), `state_06.txt:4` (22), `state_09.txt:4` (33). State histories are `history/states/54-Haute-de-France.txt` through `65-Corsica.txt`.

### Good coastal and air-base locations

- **Normandie, state 55:** air base 10/10; naval base province 6449 at 5/10 and province 485 at 1/10. Category capacity 14, with 12 shared slots free. Province 6449 also contains a naval facility level 1.
- **Bretagne, state 64:** air base 10/10, dockyard 2/20, radar 1/6. Naval base provinces 3552 at 10/10, 6536 at 4/10, 9510 at 1/10, and 542 at 1/10. Category capacity 14, with 8 shared slots free. Provinces 6536, 9510, and 542 have port-level headroom.
- **Provence, state 63:** air base 10/10, radar 2/6. Naval base province 911 is 10/10 and province 11834 is 3/10. Category capacity 18, with 13 shared slots free. Province 11834 has port-level headroom.
- **Air-base levels below cap:** Paris, state 56, has air base 5/10 and 22 shared slots free. Aquitaine, state 60, has air base 3/10, naval base province 9737 at 3/10, and 11 shared slots free. These are useful alternatives when a reward must add air-base levels rather than grant an already-full base.

Avoid using **Bourgogne, state 58** for `dockyard` or `naval_base`: its 1970 state file has no coastal port building and the state is inland. It has 9 base shared slots free for offices or agriculture. The native dockyard and naval-base definitions both require coastal placement.

Every listed port province is inside the named state file's `provinces` list. All twelve states have FRA ownership and control on 1970-01-01, so no starting occupation exception was found. In later play, check current full state control before construction, then choose a port province from the target state's province list. State-level `dockyard` and province-level `naval_base` need separate scopes and caps. Main MD France donor focuses use `has_full_control_of_state` before the state construction transaction. Province-specific dynamic control behavior was not engine-tested.

Source anchors for levels, ownership/control and category: `history/states/54-Haute-de-France.txt:10-60`; `55-Normandie.txt:9-74`; `56-Ile de France.txt:10-69`; `57-Alsace-Lorraine.txt:10-68`; `58-Bourgogne.txt:6-42`; `59-Loire.txt:9-57`; `60-Aquitaine.txt:10-58`; `61-Midi Pyrenees.txt:9-49`; `62-Rhone-Alpes.txt:9-73`; `63-Provence.txt:6-69`; `64-Bretagne.txt:5-68`; `65-Corsica.txt:5-32`. The `provinces` list and corresponding province-level naval base entries are in the same ranges. Category slot counts are from `common/state_category/state_01.txt:4`, `state_03.txt:4`, `state_04.txt:4`, `state_05.txt:4`, `state_06.txt:4`, and `state_09.txt:4`.

## Internal faction levers in France

France's 1970 country history adds the native `industrial_conglomerates`, `labour_unions`, and `farmers` ideas and initializes their opinion variables from existing values or 50 if none exists. The available helpers are:

- `change_industrial_conglomerates_opinion = yes`
- `change_labour_unions_opinion = yes`
- `change_farmers_opinion = yes`

Set signed `temp_opinion` before calling a helper. Each helper requires its matching idea, clamps the opinion to 0-100, displays its native opinion tooltip and refreshes that faction's dynamic modifier. The shared `autocrats_opinion_change` doubles positive changes for the listed autocratic ruling currents; UDR's 1970 Western Conservatism does not meet that trigger, so use the normal signed amount. There is no separate CGT opinion variable or helper. The existing `labour_unions` faction is the native umbrella lever; project context treats CGT, CFDT and FO as distinct labour actors, not new parties. Use CGT in descriptions or choices without inventing a CGT faction ID.

Source anchors: `history/countries/FRA - France.txt:89-119`; `common/scripted_effects/00_internal_faction_effects.txt:1001-1021,1055-1074,1194-1218,1248-1267`; `tools/france_1970_design/README.md:38-39`.

## Main MD France reward patterns

- `FRA_modern_interest`, MD `common/national_focus/05_france.txt:1029-1074`: on full control of state 62, add 2 shared slots then 2 offices instantly; charge treasury 24. The AI also checks `can_staff_an_offices`.
- `FRA_wake_up`, `:3676-3721`: on full control of MD 2000 state 959, add 2 slots then 2 agriculture districts instantly; charge treasury 7.5. AI checks `can_staff_an_agriculture_district`.
- `FRA_stole_voter`, `:1474-1529`: two state-level civilian factories, each guarded by full control and paired with one extra slot; treasury cost 15.
- `FRA_reise_tertiary`, `:2248-2285`, and `FRA_nuclear_eu`, `:2165-2220`: use named office and reactor construction-speed modifiers as durable policy rewards rather than only flat factories.

These are reward-shape examples, not historical or state-ID templates. MD's 2000 France uses state 959 for Pays de la Loire; the 1970 mod uses a different metropolitan map. Use the 1970 IDs above, include one extra slot per granted level as the project requires, preserve state-control and building-capacity checks, and choose a native construction technology gate where the building is research-enabled. The native preview should show the actual named building or modifier, plus its treasury cost, not an explanatory substitute.

