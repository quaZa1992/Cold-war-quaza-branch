IMPERIA COLD WAR

# Worldwide January 1970 research and historical equipment

Current equipment repair: all 163 historical aircraft use native MD BBA production frames and have exact native designer GUI registrations. All 30 transport-helicopter records now use fixed native `transport_helicopter_1`, matching MD 2000 UH-1/Mi-8/Z-5 prefabs. The AH-1G uses native modular `heavy_tank_chassis_0`. In total, 281 primary type mappings were corrected across the 488 models and 1,004 assignments. [Native MD design audit](native_md_design_audit.json) compares them with 1,435 retained MD 2000 prefabs. New 1970 games are required.

All 15 research folders now have a consistent mouse-wheel factor and a continuous native tiled canvas. The aircraft header has 21 five-year labels, including 1960, and additional top clearance. All 144 existing research grids are retained; only the aircraft content receives a common vertical offset. [Repair report](prerequisite_repair_report.json), [GUI source validation](gui_validation.json).

Computer Use was stopped by physical Escape during the isolated loading screen. No further Computer Use calls or inputs were issued. Only the private test process was closed, after its exact PID and private profile were checked. The current designer UI and repaired research viewport remain visually unverified. Native startup/first-hour assertions did not complete. The report must not be treated as a native pass.

This directory maintains the starting knowledge and representative equipment designs for all **400 country-history tags**, with **1 January 1970** as the cutoff. The tags include sovereign countries, dependent territories, conditional releases and later entities. Each research profile states that distinction and records evidence, confidence and exclusions. Country coverage does not imply that 400 independent research establishments existed.

Start with [COUNTRY_OVERVIEW.md](COUNTRY_OVERVIEW.md) to find a country, or [MODEL_INDEX.md](MODEL_INDEX.md) to inspect the named designs, fitted modules, native upgrade levels, operators and historical specifications. The regional JSON files are the maintained inputs. Generated manifests and history additions are reproducible outputs.

## Historical method

The reference date is the beginning of January 1970. A contract, prototype flight, public demonstration or delivery later in 1970 does not establish service at the cutoff. Dates ending 31 December bound evidence stated only to a year; they are not invented acceptance ceremonies. Later publications can establish earlier service when they explicitly identify the earlier event. Shared designs retain separate local-operator evidence in their notes and provenance records.

Evidence distinguishes indigenous development and manufacture from licensed production, maintenance, imported equipment operation and foreign forces stationed locally. Uncertainty receives a conservative local baseline and an explicit confidence assessment. Hypothetical releases do not receive an invented independent nuclear, aerospace, missile, tank or shipbuilding industry. An empty named-design list means that this pass has no separately evidenced package, rather than establishing that a population or military possessed no basic arms.

Research is divided into 22 domains:

| Area | Profile domains |
| --- | --- |
| Civil capacity | `construction`, `machinery`, `grid`, `computing` |
| Infantry and support | `infantry`, `support`, `communications`, `vehicles`, `camouflage`, `special_forces`, `night_vision`, `body_armor` |
| Ground weapons | `anti_tank`, `anti_air`, `artillery`, `armor` |
| Air | `jet_light`, `jet_medium`, `aircraft_modules`, `helicopter` |
| Naval | `naval_surface`, `naval_submarine` |

A domain value is a ceiling in the corresponding existing technology chain. Zero means no grant from that domain. Exact `add_techs` and `remove_techs` handle exceptions; the compiler resolves hard prerequisites and the active DLC branch. A ceiling is not an assertion that every technology with that calendar year was known. No universal package of all 1970 technologies is granted.

The inherited MD tree is coarse. Some historical technologies bundle several capabilities, retain later names or represent multiple equipment generations. Those limitations are documented rather than treated as precise national milestones. For example, MiG-21 and Mirage III belong to the native second-generation light-jet branch; generic gun-based air defence does not establish MANPADS knowledge. Naval nuclear propulsion is not inferred from an ordinary diesel submarine. A research reactor does not automatically establish a commercial power-reactor family, an enrichment plant, a weapon or a completed special project. Missing native families, including the absent BWR branch, are not replaced by unrelated reactor technologies.

## Equipment and native MD values

Design records use native equipment families, slots, modules and upgrade fields. Original producers and local operators are recorded separately. Imported designs receive only the evidence-backed bare equipment and exact fitted component knowledge needed for their historical configuration. The compiler supplies those prerequisites before creating the variant, including separate DLC-specific component bundles. Designer-specific components follow their active branch. Shared static guns and transports can receive their exact bare type through a common service bundle when the ordinary research unlock does not cover every DLC configuration in which the same design is created. This can repeat an already available bare-type unlock in one configuration, with no additional equipment or effect. An imported tank does not grant the supplier's complete research, electronics or industrial package.

Modular land designs use the No Step Back branch, and modular aircraft use By Blood Alone. Where a faithful fixed equipment family exists, an explicit legacy fallback preserves the same broad historical role. Early T-54, Centurion and Patton families can use the existing 1955 medium-tank fallback; light AMX-13/M41 families use the reconnaissance family. Missing faithful alternatives are disclosed. Rifles, utility vehicles and towed artillery remain native fixed equipment. They have no invented module designer, self-propelled chassis or autoloader. The naval records use the mod's existing ship equipment framework and legal slots.

Aircraft now use MD's registered first-production `_1` frames and native primary-weapon role selection, rather than extra historical airframe copies. The nine extra role bases and their generated derivatives are retired. The custom modular utility-helicopter frame is removed. Three fixed early attack-aircraft fallback definitions remain exclusively available through non-BBA service bundles, preserving older aircraft roles when that designer DLC is absent. Active BBA designs never use those fixed fallbacks. Native fixed infantry, trucks and towed artillery retain their earlier Cold War research tiers within the existing MD categories. The medium native aircraft primary slot now accepts MD's existing cargo module so its already registered transport role can use one propeller engine for An-2. Its biplane geometry, very low engine power and payload remain limits of the native MD module granularity. P-3B uses a four-propeller maritime-patrol frame, first ASW payload and first MAD tier, with an evidenced pre1970 sensor exception.

Physical specifications and game values have different purposes. `historical_specs` records sourced calibre, power, road speed, mass, material and protection where available. Installed modules provide the closest legal native representation. Native gun bands, common chassis and imperfect suspension categories remain disclosed approximations. Missing numerical specifications are left unknown rather than filled with invented precision.

Relative protection and mobility use native MD upgrade logic. `tank_nsb_armor_upgrade` adds 7.5% aggregate game armor per level with native speed, reliability and cost trade-offs; `tank_nsb_engine_upgrade` adds 3.5% game speed with reliability, fuel and cost trade-offs. Levels are neither millimetres of plate nor horsepower units. A common level also has different results on different chassis and module combinations. Original MD historical variants provide restrained comparison anchors. For example, the early Leopard 1 uses its 105 mm gun, original diesel and steel protection with armor level 1 and engine level 5, preserving its mobility emphasis without fitting Leopard 1A5 fire control or later armor. See the model index and regional records for each design's sources and mapping rationale.

The result uses MD's existing combat-value abstractions. It does not claim that a native armor number is a literal historical penetration or protection measurement. MIOs, design teams, experience premiums and future modernization packages are not copied from later native history examples. These changes create research and available design definitions. They do not change army, air-force or fleet OOB quantities, spawn deployed equipment, or add stockpile quantities.

## Maintained inputs and sources

| Region | Research input | Research evidence | Equipment input | Equipment evidence |
| --- | --- | --- | --- | --- |
| Europe and former USSR | [Profiles](europe_profiles.json) | [Sources](europe_sources.md) | [Variants](europe_variants.json) | [Sources](europe_variants_sources.md) |
| Asia, Middle East and Turkey | [Profiles](asia_profiles.json) | [Sources](asia_sources.md) | [Variants](asia_variants.json) | [Sources](asia_variants_sources.md) |
| Africa | [Profiles](africa_profiles.json) | [Sources](africa_sources.md) | [Variants](africa_variants.json) | [Sources](africa_variants_sources.md) |
| Americas and Oceania | [Profiles, including USA](americas_oceania_profiles.json) | [Sources](americas_oceania_sources.md) | [Variants, excluding USA](americas_oceania_variants.json) | [Sources](americas_oceania_variants_sources.md) |
| USA equipment | Same Americas research profile | Same research register | [USA variants](usa_variants.json) | [USA sources](usa_variants_sources.md) |

[NOTICE.md](NOTICE.md) records authorship, inherited MD attribution and known licensing limits. Historical manufacturers and linked institutions retain their rights. Sources are evidence, not a transfer of copyright or permission to reuse their images. The project identifier establishes no ownership of third-party material. See also [the project notice](../../IMPERIA_COLD_WAR_NOTICE.md).

## Build and review

Run these commands from the mod root. Catalogs describe the available native identifiers and compatibility rules; inclusion in a catalog does not grant a technology to a country.

```powershell
python tools/starting_research_1970/catalog.py
python tools/starting_research_1970/equipment_catalog.py
python tools/starting_research_1970/component_compat.py --check
python tools/starting_research_1970/role_frames.py --check
python tools/starting_research_1970/gui_repair.py --check
python tools/starting_research_1970/validate_gui_repair.py
python tools/starting_research_1970/variants.py
python tools/starting_research_1970/build.py
python tools/starting_research_1970/validate.py --preview
python tools/starting_research_1970/validate_variants.py --data-only
python tools/starting_research_1970/validate_variants.py --preview
python tools/starting_research_1970/review_catalog.py
python tools/starting_research_1970/country_overview.py
```

`build.py` previews the compiled selections without installing the generated country-history changes. `variants.py` refreshes the generated variant manifest; `--apply-support` is its explicit support-definition write mode. The regional inputs remain authoritative if a generated manifest predates an edit. Do not manually repair a generated history block instead of its maintained input or generator.

The integration sequence, after the inputs and compatibility changes have been reviewed, is:

```powershell
python tools/starting_research_1970/native_md_designs.py --capture
python tools/starting_research_1970/native_md_designs.py --apply
python tools/starting_research_1970/component_compat.py --apply
python tools/starting_research_1970/role_frames.py --apply
python tools/starting_research_1970/catalog.py
python tools/starting_research_1970/equipment_catalog.py
python tools/starting_research_1970/variants.py
python tools/starting_research_1970/build.py --apply
python tools/starting_research_1970/build.py --check
python tools/starting_research_1970/validate.py
python tools/starting_research_1970/validate_variants.py
python tools/starting_research_1970/audit_native_md_designs.py
python tools/starting_research_1970/review_catalog.py
python tools/starting_research_1970/country_overview.py
```

The builder checks the captured original archive, preserves unrelated country-history semantics and later dated blocks, and confines the starting assignments to the scenario guards. Its guarded initialization does not repeatedly reset earned research or recreate variants during play. The independent validators check source definitions, hard prerequisites, DLC alternatives, fitted slots, physical-family assertions, cutoff dates, initialization and preservation of unrelated history. Static DLC coverage includes all eight combinations of the three scenario branches, or 3,200 country cases.

## Validation status and native checks

Current static results are recorded in [validation.json](validation.json) and [variant_validation.json](variant_validation.json). Read their `mode`, timestamp, input hashes, status and diagnostics together. A data-only pass covers the inputs; it does not establish that the current rendered or installed history passes. A preview pass does not establish a native engine result. Reports must be refreshed after material input or compiler changes.

The installed equipment checks pass for 488 models and 1,004 assignments in all 400 histories and 3,200 DLC cases. The native designer routing audit also passes. The research validator reports two preservation differences from its immutable original archive: concurrent GER and DDR leadership/portrait integration outside this feature. Those changes were retained; no prerequisite, DLC, future-tech or ordering errors were reported. The two original-baseline assertions remain failures in `validation.json`, rather than being silently waived. This is not a claim that every whole-repository check passes.

The current native attempt is interrupted and incomplete. Its frozen snapshot and full logs are retained at `E:/HOI4_Mod_Tools/mdcoldwar/runtime/starting_research_1970/20261030_212448`. It reached initial scenario loading but did not reach the research fixture or designer inspection before Computer Use was stopped. Zero matched feature-parser messages in that partial log do not prove that the designer or complete initialization works. A later legacy-branch compiler correction also means that this snapshot is not the exact final source revision.

The partial engine log retains the existing native `weap_buff_transport` optional category message separately from feature-matched diagnostics. Full diagnostics remain on E:. The test process return code records deliberate termination after the user stopped inspection; it is not presented as a game crash.

Private runtime data belongs under `E:/HOI4_Mod_Tools/mdcoldwar/runtime`; retained archives belong under `E:/MDColdWar_Backups/Codex_Test_Archives`. Asset junctions must not be recursively enumerated or copied.

```powershell
python tools/starting_research_1970/native_probe.py --prepare
python tools/starting_research_1970/native_probe.py --run --duration 480
```

A complete native verification still requires a fresh final-source snapshot, first-hour assertions and direct inspection of representative aircraft, tank, artillery, ship and helicopter designs. Save/reload and live multiplayer have not been tested. Record these separately from deterministic source checks.