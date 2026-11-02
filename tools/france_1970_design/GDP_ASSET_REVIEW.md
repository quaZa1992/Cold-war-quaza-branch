IMPERIA COLD WAR

# France 1970 GDP reward asset review

Bounded, read-only check of the current `concept.json` and `reward_revision.py` against the mod's 1970 state history and current MD building definitions. Reviewed concept SHA-256: `4f57a4c6e3d13eba6b7ec4129cb81fd8b9a2a645e9fac10c5ebf8d36588c18b5`. I could not find `newreward_revision.py`; the matching current revision script is `tools/france_1970_design/reward_revision.py`. No concept, generator, or live game files were changed.

## Result

The current snapshot contains 43 building rows when counting 40 French national/decision assets and 3 recipient-side offer assets. Every row has `slots = amount = 1`, `slots_before_construction = true`, and `once = true`. This includes the reactor funding decision and all foreign assets. `build_design.py:15-18` defines those fields for assets; `reward_revision.py:121-138` normalizes the full node, offer, and decision set and specifies one guarded transaction for the GDP debit, slot grant, and building. The proposed convention gives an extra slot even to infrastructure, internet stations, naval bases, reactors, and other buildings that do not use shared slots.

The audited 1970 locations have enough native level and shared-slot capacity for the complete one-time reward set, including accumulation across different governing-party programmes. The current municipal France revision costs 0.45% of France's current GDP and builds one office and one agriculture district in state 60. This leaves Aquitaine infrastructure at three possible added levels in total: regional links and motorways add two to its starting level 3, for 5 / 6. No proposed `air_base` level targets a full base. The defined state ownership/control and capacity checks remain transaction requirements for implementation, not runtime behavior verified by this report.

## French assets and cumulative capacity

The free-slot figures below are the static 1970 category headroom from `REWARD_ASSET_REFERENCE.md`, before dynamic slot modifiers. “Rows” counts every one-time asset that can target the state, even if party changes are needed to reach it. Each row grants one shared slot, so the project rewards have sufficient slot capacity wherever a shared building consumes one. For non-shared buildings, the required extra slot remains available afterward.

| State | Initial shared slots used / free | Possible reward rows | Tightest native level check |
|---|---:|---:|---|
| 54 Haute-de-France | 5 / 17 | 3 | arms factory cap 35; industrial complex cap 50 |
| 55 Normandie | 2 / 12 | 5 | naval base province 6449: 5 to 6 / 10; other state buildings well below cap |
| 56 Ile de France | 11 / 22 | 5 | infrastructure 3 to 5 / 6; internet stations 0 to 2 / 11 |
| 57 Alsace-Lorraine | 2 / 12 | 2 | industrial complex cap 50 |
| 58 Bourgogne | 1 / 9 | 1 | industrial complex cap 50 |
| 59 Loire | 3 / 7 | 5 | infrastructure 3 to 5 / 6; nuclear reactor starts at 3, then 4 / 20 |
| 60 Aquitaine | 3 / 11 | 6 | infrastructure 3 to 5 / 6; offices 1 to 3 / 50; agriculture districts 0 to 2 / 10 |
| 61 Midi Pyrenees | 2 / 12 | 2 | industrial complex cap 50 |
| 62 Rhone-Alpes | 5 / 13 | 5 | internet station 0 to 1 / 11; infrastructure 3 to 4 / 6 |
| 63 Provence | 5 / 13 | 3 | province 11834 naval base 3 to 5 / 10 |
| 64 Bretagne | 6 / 8 | 3 | dockyards 2 to 4 / 20; province 6536 naval base 4 to 5 / 10 |

Counts include the three UDR NATO assets and shared-tree assets that can be earned in different party cycles. The native maximum for `infrastructure` is 6 (`common/buildings/00_buildings.txt:75-84`). State 60 remains below cap at infrastructure level 5 after the current reward set; the native capacity guard still protects against other construction. State 56 and 59 infrastructure also remain below cap after all listed compatible awards. No additional `rail_terminal` is in the revision. The TGV reward is an infrastructure level in state 62 and finite `CAT_infrastructure` research progress, not a rail terminal or an untracked research slot.

State anchors: `history/states/54-Haute-de-France.txt:10-60`; `55-Normandie.txt:9-74`; `56-Ile de France.txt:10-69`; `57-Alsace-Lorraine.txt:10-68`; `58-Bourgogne.txt:6-42`; `59-Loire.txt:9-57`; `60-Aquitaine.txt:10-58`; `61-Midi Pyrenees.txt:9-49`; `62-Rhone-Alpes.txt:9-73`; `63-Provence.txt:6-69`; `64-Bretagne.txt:5-68`. Slot category capacities and starting shared-slot calculations are detailed in `REWARD_ASSET_REFERENCE.md`.

### Ports and other special buildings

- Bretagne state 64 starts with 2 dockyards. The ocean fleet and NATO sea priority can add two, for 4 / 20. Their one extra slot per level exactly covers dockyards' shared-slot use. Naval base province 6536 starts at 4 / 10 and can receive one more through the UDR NATO fleet-support focus.
- Provence state 63 province 11834 starts at 3 / 10 and can receive one level from regional industry and one from maritime escorts, reaching 5 / 10. These are province buildings, not state dockyards.
- Normandie state 55 province 6449 starts at 5 / 10 and receives one level from logistics, reaching 6 / 10.
- Bretagne is coastal, Normandie is coastal, and Provence is coastal. The selected ports occur in those states' province lists. MD definitions require coastal placement for both `dockyard` and `naval_base`; a state-level control check plus the specified province/cap check is appropriate.
- No reward adds an air base. This avoids adding levels to full 10/10 air bases such as states 54, 55, 63 and 64.
- France's internet station rewards are in states 56 and 62, each starting at zero. MD caps the building at 11. Both the French telecom programme and the Symphonie route carry an `internet_1` requirement; Symphonie also requires Germany's `internet_1`. The first-level native technology starts in 1975. No rail terminal is awarded.
- The nuclear decision targets state 59, which starts with 3 nuclear reactors; its cap is 20. Its source condition calls for actual reactor technology. It must retain the separately specified state-control, capacity and once-only debit guard.

## Recipient-side foreign assets

The three recipient assets are all in 1970 German-controlled territory and stay on the recipient side of the offer: Airbus industrial complex in Hamburg (state 1080), plus Symphonie internet station and Rhine industrial complex in Baden-Wurttemberg (state 42). These correspond to 3 rows in addition to France's 40.

| Germany state | Start owner/controller | Category slots | Initial shared use / free | Proposed assets and native headroom |
|---|---|---:|---:|---|
| 1080 Hamburg | GER / GER | 10 | 4 / 6 | Airbus adds one industrial complex; current 2, cap 50. One project slot covers its shared-slot use. |
| 42 Baden-Wurttemberg | GER / GER | 33 | 13 / 20 | Symphonie adds one internet station (current 0, cap 11); Rhine adds one industrial complex (current 7, cap 50). Both agreements together still fit; the internet station does not consume a shared slot, and its project slot remains free. |

Germany state 1080 source: `history/states/1080-Hamburg.txt:5-46`; state 42 source: `history/states/42-Baden-Wurttemberg.txt:5-58`. MD limits industrial complexes to 50 per state and internet stations to 11 (`common/buildings/00_buildings.txt:43-51,93-102`). Both state histories place the target inside Germany's ownership and control in the 1970 setup. At acceptance, ownership and control must be rechecked in the recipient's country scope before either signatory pays or receives any finite asset; a changed owner/controller should fail that side's whole agreement transaction.

## Current preview spot-check

Opened the generated `PREVIEW.html` in local Chrome with Playwright and inspected the three requested effects in the rendered inspector. This is browser UI verification only, not a HOI4 engine test.

- **Airbus Partnership:** both acceptance sides display their own Treasury cost of -0.5% of current GDP. For each country the +1 shared building slot row appears immediately before its +1 Civilian Factory row: Midi Pyrenees (61) for France and Hamburg (1080) for Germany. No browser page errors occurred.
- **Maritime Escorts:** the inspector displays Treasury -0.35% of current GDP, then Provence +1 shared building slot immediately before Marseille / province 11834 +1 Naval Base.
- **Rhine Field Exercises:** the inspector shows France Weekly Programme Expense `(0.03% of current GDP) ÷ 52` and Germany `(0.02% of current GDP) ÷ 52`. This is the intended asymmetric allocation, with each stream based on that signatory's own current GDP.

## Implementation handoff

All state/category level values in the report are based on current static history, not a live-game save. The concept's `transaction` field and generator normalization specify the intended once-only guard but do not establish that the runtime scripts exist or have passed engine validation. Keep the full-control, current owner, coastal target province, native level-capacity and shared-slot checks separate, and place the slot grant before each construction in the same atomic transaction as the single payer-specific GDP cost. Preserve the French and recipient GDP bases independently for each offer.
