IMPERIA COLD WAR — DDR reward revision

# DDR reward review and implementation

## Scope and weak rewards

The loaded DDR tree contains 836 focus IDs. This reward-only revision preserves those IDs, coordinates, costs, prerequisites, exclusions, leader successions, party systems, inter-German diplomacy, security integrations, and the retired Soviet trust system. It does not run the legacy 821-focus generator or modify shared German relations, country history, or global economy files.

Several existing rewards were narrow or repetitive. Examples included `ind_refined_for_the_west`, which offered only 1% GDP and 5% resource-export revenue; `micro_computers_for_the_schools`, which offered a limited research bonus and 3% research speed; and multiple NVA foci that repeated small core defence, naval coordination, or experience modifiers. The revision gives important industry, household policy, technology, agriculture, energy, alternative party programmes, and NVA units distinct assets or targeted rewards with visible trade-offs.

## Coverage

The bounded overlay revises 49 existing focus rewards: 31 static policy, finite research, doctrine, or equipment outcomes, plus 18 paid asset programmes. The economic leadership alternatives differ in both capacity and cost. Ulbricht's NÖS investment and Kombinat autonomy reinforce productivity and enterprise coordination. Honecker's housing, wage, and consumer programmes improve household provision while costing more and adding social obligations. The alternative CDU, UCT, DBD, Green League, and defence-first routes have distinct industrial, rural, energy, and fiscal outcomes.

The paid packages cover chemical and civilian industry, planning offices, microelectronics, urban infrastructure, housing, lignite, nuclear power, renewables, agriculture districts, and NVA arms production. Asset bundles replace their original random paid project helpers with explicit DDR states. Each bundle adds a shared state slot for every building level before construction. It is gated by current GDP above zero, current ownership and control, whole-package native state capacity, and any specialist technology tier. No pre-existing free slot is required. The GDP price is calculated at completion from current GDP and charged once.

At the 1970 start value of $32B GDP, individual packages cost 0.74% to 4.70% of GDP. The sum of all 18 listed prices is 46.16% of starting GDP if every package were acquired; several represent alternative political or economic routes and are not all selectable in one run. Legacy project fees are included in the transaction price, and the old asset helpers and negative GDP charges cannot run separately. Original non-project effects, including opinions, spirits, party state, positive Treasury credits, and focus-specific system updates, remain inside the complete guarded transaction.

| Focus programme | GDP fraction | Approximate 1970 price | Complete asset package |
|---|---:|---:|---|
| `ulb_the_structure_determining_tasks` | 0.02880 | $0.9216B at DDR's $32B 1970 GDP | Saxony (44) industrial_complex +1; Saxony (44) synthetic_refinery +1; Saxony-Anhalt (972) industrial_complex +1; Saxony-Anhalt (972) synthetic_refinery +1 |
| `ulb_the_kombinat_as_economic_unit` | 0.03200 | $1.0240B at DDR's $32B 1970 GDP | Saxony (44) industrial_complex +4 |
| `ulb_cybernetics_and_the_plan` | 0.02560 | $0.8192B at DDR's $32B 1970 GDP | Saxony (44) offices +2 |
| `hon_pay_from_the_plan` | 0.01500 | $0.4800B at DDR's $32B 1970 GDP | Berlin (45) infrastructure +1; Mecklenburg (539) infrastructure +1; Saxony-Anhalt (972) infrastructure +1; Brandenburg (1079) infrastructure +1 |
| `hon_solve_the_housing_question` | 0.03100 | $0.9920B at DDR's $32B 1970 GDP | Saxony (44) industrial_complex +1; Saxony (44) infrastructure +1; Berlin (45) industrial_complex +1; Mecklenburg (539) infrastructure +1; Thuringia (545) infrastructure +1; Brandenburg (1079) infrastructure +1 |
| `hon_the_main_task_fulfilled` | 0.04700 | $1.5040B at DDR's $32B 1970 GDP | Saxony (44) industrial_complex +2; Saxony (44) infrastructure +1; Berlin (45) industrial_complex +2; Berlin (45) infrastructure +1; Thuringia (545) infrastructure +1; Saxony-Anhalt (972) infrastructure +1 |
| `cons_the_thousand_small_things` | 0.03200 | $1.0240B at DDR's $32B 1970 GDP | Saxony (44) industrial_complex +2; Berlin (45) industrial_complex +2 |
| `mit_the_microelectronics_resolution` | 0.02220 | $0.7104B at DDR's $32B 1970 GDP | Saxony (44) microchip_plant +2 |
| `spk_the_computing_centres` | 0.02560 | $0.8192B at DDR's $32B 1970 GDP | Saxony (44) offices +1; Berlin (45) offices +1 |
| `ind_plastics_from_schkopau` | 0.01280 | $0.4096B at DDR's $32B 1970 GDP | Saxony-Anhalt (972) synthetic_refinery +1 |
| `energy_brown_coal_from_lusatia` | 0.01350 | $0.4320B at DDR's $32B 1970 GDP | Brandenburg (1079) fossil_powerplant +2 |
| `energy_greifswald_nuclear_power_station` | 0.02960 | $0.9472B at DDR's $32B 1970 GDP | Mecklenburg (539) nuclear_reactor +2 |
| `gl_neither_coal_nor_atom` | 0.02710 | $0.8672B at DDR's $32B 1970 GDP | Thuringia (545) renewable_energy_infra +2 |
| `dbd_a_republic_of_villages` | 0.01600 | $0.5120B at DDR's $32B 1970 GDP | Brandenburg (1079) agriculture_district +4 |
| `hof_the_suhl_arsenal` | 0.03200 | $1.0240B at DDR's $32B 1970 GDP | Thuringia (545) arms_factory +4 |
| `cdu_a_christian_social_market` | 0.03200 | $1.0240B at DDR's $32B 1970 GDP | Saxony (44) industrial_complex +2; Berlin (45) industrial_complex +2 |
| `uct_the_mittelstand_republic` | 0.03200 | $1.0240B at DDR's $32B 1970 GDP | Saxony (44) industrial_complex +2; Thuringia (545) industrial_complex +2 |
| `dbd_the_village_programme` | 0.00740 | $0.2368B at DDR's $32B 1970 GDP | Mecklenburg (539) infrastructure +2 |

## Native mechanics and player preview

Each focus keeps its original meaningful availability rules and adds native GDP and asset capacity requirements. Party paths keep their original MD party-in-power triggers and remain visible. The runtime helper rechecks the same frozen base availability, GDP, ownership, control, state capacity, and specialist technology gates, then applies the complete residual old reward, current-GDP price, buildings, new rewards, and one-time receipt together.

Every transaction focus uses an unconditional native `effect_tooltip` containing the calculated GDP deduction, original non-project effects, exact slot and building levels, research and modifier rewards. The actual scripted effect call is under `hidden_effect`, so it adds no internal helper text to the visible effect list. Static focus additions use the same concrete native preview and execute once under the focus's frozen original availability trigger. Research and doctrine bonuses have finite uses. New awards have distinct localised names from retained research bonuses. Equipment-cost rebates are permanent and apply only to the listed families. The Soviet equipment focus keeps its existing infantry fighting vehicle research bonus while replacing the broad equipment discount with a 3% IC cost reduction on anti-tank and anti-air families.

No new separately scheduled monetary stream, affordability gate, workforce-size penalty, free equipment, uranium production, uranium mine, or free nuclear technology is added. Budget modifiers still affect the existing MD ledger: border troops now add police costs +2%, and the 40th Parachute Battalion adds army personnel costs +1%. The MiG-23 programme improves aircraft defence +3% with air accident risk +2%, alongside its retained air-to-air rewards. Existing approved Soviet procurement and production-licence agreements, their recipient decisions, and the trust/removal/security integrations are outside this overlay.

## Historical and mechanic references

Historical precedents and current MD examples are recorded in [HISTORICAL_AND_MD_REFERENCES.md](HISTORICAL_AND_MD_REFERENCES.md). They cover the 1963 New Economic System, Honecker's 1971 Unity of Economic and Social Policy, lignite dependence, LPG mechanisation, the later cost of microelectronics, and current finite research, doctrine, construction, and native building-cap patterns. The 7-day focus-point calibration means cost 4.3 takes about 30 days, cost 6 takes 42 days, cost 7 takes 49 days, and cost 10 takes 70 days.

## Rebuild footprint and verification boundary

The canonical source is `Claude outputs/COLDWAR_DDR_generator/design/ddr_reward_overlay_20261027.json`. It freezes original availability and completion rewards per target from the approved BEFORE snapshot, so the writer does not depend on reading the private archive during later rebuilds. The bounded writer is `tools/focus_quality_20261020/apply_ddr_reward_overlay.py`; `tools/focus_quality_20261020/apply_ddr.py` calls it after the existing retained quality post-process.

The DDR reward writer changes the loaded DDR focus file, its English focus localisation, and two DDR-scoped runtime files: `common/scripted_effects/COLDWAR_DDR_20261027_programmes.txt` and `common/scripted_triggers/COLDWAR_DDR_20261027_programmes.txt`. The existing shared building-grant repair module is also imported as a transitive dependency. Its integration emits or maintains five shared outputs: `localisation/english/COLDWAR_GRANT_capacity_l_english.yml`, `common/scripted_effects/COLDWAR_GRANT_native.txt`, `common/scripted_effects/COLDWAR_GRANT_programmes.txt`, `common/scripted_triggers/COLDWAR_GRANT_programmes.txt`, and `common/on_actions/COLDWAR_GRANT_programmes.txt`. The shared helper source is `tools/building_grants/grants.py`; it is owned by the broader building-grant integration, not this DDR overlay. The rebuild hook does not invoke `dg_build.py` or write broad `out/` outputs. It does not edit shared German relations, state history, the national economy, or security files. The 836 focus count and unique IDs were retained. Reapplication produced byte-identical output for all nine files in the bounded hook. The DDR focus, DDR runtime, and shared grant script files passed the project's Clausewitz parser. A live focus-hover review, full native game session, or multiplayer replay is not claimed by this source-level work.

## Parent final verification

The final combined source check passed. All 37 targeted native assertions and all 49 existing source-model regression tests passed. Both bounded canonical rebuilds produced byte-identical runtime files to the successful native fixture. One intermediate game launch crashed before fixture execution; its crash profile and report are retained separately. No crash cause or full multiplayer result is claimed. See [FINAL_CHECKS.json](FINAL_CHECKS.json) and [IMPLEMENTATION.md](IMPLEMENTATION.md).
