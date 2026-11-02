IMPERIA COLD WAR

# Generic naval donor mechanics review

Read-only source audit, 25 October 2026. No gameplay file or generator output was changed. No native game or multiplayer test was performed.

## Donor and attribution

The donor is installed Millennium Dawn 2.0.2, game 1.19.*, workshop 2777392649, at `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649`. The local `00_generic.txt` has different whole-file content, but all 20 naval focus ASTs are equal to that original donor. Individual focus authors and separate redistribution permission are unknown in the inspected source. The naval-project file credits AngriestBird, Doolittle, DROID and TheGeneral. Existing code/art rights remain separate from project adaptations.

The source root is declared at (31, 0). The footprint retains that root and 19 relative-anchor nodes. It spans relative columns -5 through 4 and rows 0 through 5. Only aircraft carriers versus helicopter operators form an exclusion pair. Three external prerequisite IDs appear in five edges; an isolated copy must resolve them. Cost 10 means 70 nominal days, 7.1 approximately 50, and 5 means 35. Native completion rounding was not observed.

## Fundamental naval-project conclusion

`sp_naval_vessel_project` is a real, allowed naval-specialization project. It requires one naval breakthrough and 25 steel in its native project, and its normal facility helper costs 15 billion. The generic 20 does not grant that facility or a scientist. The 15% effect adds prototype progress; it is not a project completion or research unlock.

No 1970 history completion was found for USA, SOV, DDR, IRQ or UAE, nor a global 1970 scripted/on_action completion. USA/SOV/UAE complete the project only inside their 2000.1.1 history; DDR/IRQ have no matching completion. Retaining its focus gates is therefore a real gameplay prerequisite, not proof of immediate 1970 access. Removing a focus gate alone also does not remove the underlying historical hull technology allow gate, for example `mdcw_carrier_hull_1955` and `mdcw_destroyer_hull_1955`.

Composite production 1 starts in 1990. Stealth corvette/frigate projects require 2010 hulls, and stealth destroyer requires 2005 hull 3. These native providers exist, but their future output should not be granted as an immediate 1970 reward. Era-neutral replacement research can preserve the donor layout.

## Exact focus catalogue

| Donor focus | Cost | Prerequisites | Concrete reward bundle |
| --- | --- | --- | --- |
| `GENERIC_naval_reform` | 10 | Entry | 75 naval XP; 30 naval-folder mastery if a naval grand doctrine is selected; +15% prototype progress to the incomplete foundational naval project; maritime industry opinion +10. |
| `GENERIC_combined_military_defense_industries` | 10 | (dockyards) AND (refitting_the_military_industry) | Permanent Combined Defense Industries: military-factory productivity +10%, dockyard productivity +10%, military-industry tax modifier +10%, dockyard income tax modifier +10%. Defense and maritime opinions +5 each. One arms factory free because skip_payment=1. |
| `GENERIC_naval_bases` | 10 | (naval_reform) | One port level through native random-province construction, treasury -0.5 billion, maritime opinion +5. Donor grants no extra shared slot. |
| `GENERIC_submarines` | 10 | (naval_reform) | Two 50% CAT_submarines research bonuses. |
| `GENERIC_surface_ships` | 10 | (naval_reform) | Two 50% CAT_surface_ships research bonuses. |
| `GENERIC_dockyards` | 10 | (naval_bases) | One dockyard if fewer than15 total factories, otherwise two. Native helper charge7.5 or15 billion. Maritime opinion +5. |
| `GENERIC_nuclear_submarines` | 7.1 | (submarines) | Two 50% CAT_submarines research bonuses. +50 mastery for each matching selected escort_attack_subs, hunter_killer_subs or missile_boats subdoctrine. No nuclear ship or propulsion technology is granted. |
| `GENERIC_naval_doctrine_innovations` | 10 | (naval_reform) | 50 naval XP and50 naval-folder mastery. |
| `GENERIC_aircraft_carriers` | 10 | (surface_ships) AND (fighter_planes) | Two 50% CAT_aircraft_carriers research bonuses. |
| `GENERIC_light_helicopter_operators` | 10 | (surface_ships) AND (fighter_planes) | Two 50% CAT_helicopter_operators research bonuses. |
| `GENERIC_large_ship_drydocks` | 10 | (aircraft_carriers OR light_helicopter_operators) | One dockyard through native helper, normal7.5-billion charge. |
| `GENERIC_improved_repair_facilities` | 10 | (large_ship_drydocks) | repair_yard_focus for365days: repair_speed_factor +25%. |
| `GENERIC_vessel_production` | 5 | (nuclear_submarines) AND (dockyards) | naval_production_bonus4 for730days: industrial_capacity_dockyard +20%. Maritime opinion +5. |
| `GENERIC_composite_industrial_expansion` | 5 | (combined_military_defense_industries) AND (military_industry_investment_projects) | One composite plant through native helper, normal8.5-billion charge. Its tech/project path begins1990. |
| `GENERIC_weapon_conversion_packages` | 5 | (combined_military_defense_industries) AND (military_industry_investment_projects) | equipment_conversion_efforts_idea for730days: equipment conversion speed +15%, factory output +15%. |
| `GENERIC_naval_doctrine_expertise` | 10 | (naval_doctrine_innovations) | 25 naval XP and50 naval-folder mastery. |
| `GENERIC_convoy_and_freighter_production` | 10 | (naval_reform) | Permanent convoy_production_bonus: convoy equipment build cost -15%, instant=yes. |
| `GENERIC_establish_a_marine_corps` | 10 | (naval_doctrine_expertise) | Permanent establishing_a_marine_corps_idea: naval XP gain +5%, amphibious invasion +15%, extra marine supply grace48, marine special-forces contribution factor -5%. |
| `GENERIC_submarine_expansion_project` | 7.1 | (vessel_production) AND (naval_doctrine_expertise) | Two 50% CAT_submarines research bonuses and the same conditional +50 submarine-subdoctrine mastery as Nuclear Submarines. |
| `GENERIC_stealth_ships` | 10 | (surface_ships) AND (naval_doctrine_expertise) | Prototype progress +10% for each incomplete stealth corvette, frigate and destroyer project. No hull or completed special project is granted. |

## Actionable adaptation findings

### external_prerequisites

Five prerequisite references point to three focuses outside the20-node naval footprint. Copying only naval nodes leaves dangling or unreachable prerequisites. Preserve internal joins and the carrier/helicopter exclusion; replace the three external land/air prerequisites with reviewed existing country equivalents or explicitly documented internal naval prerequisites.

Source: `common/national_focus/00_generic.txt:4357,4673,4724,4865,4895`.

### foundation_1970

The foundation project is defined and allowed, but not precompleted in any inspected1970block for USA/SOV/DDR/IRQ/UAE. USA/SOV/UAE completions are inside2000.1.1 history; DDR/IRQ have none. No1970global scripted/on_action completion was found. The20-node donor does not build a naval research facility or scientist. A15% prototype-progress effect is not a completed-project/facility grant. Do not assume foundation completion at1970start. Ordinary native facility/research remains a possible route. If removing only national-focus project gates, retain and disclose that actual naval hull technologies still have this native allow gate. Any explicit historical baseline completion requires a separate intentional integration decision.

Source: `common/special_projects/projects/naval_projects.txt:3; history/countries/USA - USA.txt:981; common/technologies/mdcw_historical_air_naval.txt:135`.

### late_technology

Composite production1 starts1990. Stealth corvette/frigate project availability requires hull4 with start_year2010; stealth destroyer requires destroyer_hull3 start_year2005. These are native valid providers, not1970immediate content. Keep their geometry but replace rewards/titles with era-neutral maritime materials/engineering research. Do not silently complete modern stealth projects or grant2010hulls. Use existing real categories such as CAT_industry or CAT_naval_modules after choosing the intended subject.

Source: `common/technologies/industry.txt:8709; common/special_projects/projects/naval_projects.txt:64,116,168`.

### port_slot_and_transaction

The donor port focus grants no promised extra shared slot and charges0.5billion even when no eligible construction state exists. Port cap is10perprovince, not shared-state capacity. Recheck current owned/control/coast/actual port-province capacity and funds in execution. Add one extra state shared slot before one port level in that same guarded transaction. No include_locked field for the nonshared port class.

Source: `common/national_focus/00_generic.txt:4413; common/buildings/00_buildings.txt:269`.

### helper_delivery_and_price

Dockyard helpers bill7.5/15billion even if fewer eligible states are found; two_random_dockyards selects two distinct states with one level each. A country with one eligible coast may receive only one yard while paying15. Combined Defense Industries sets skip_payment=1 and its arms factory is therefore free. Composite helper bills8.5 and adds its slot after construction. Use locally guarded explicit construction instead of rewriting shared helpers. Reserve/check the entire promised amount and native capacity before any payment. Choose either donor fixed fees or a reviewed GDP-based adaptation, never both. Preserve the free arms-factory bundle unless changing it intentionally. Put every promised slot before construction.

Source: `common/scripted_effects/00_scripted_effects.txt:4,595,650,1185`.

### coastal_adaptation

Dockyard requirements are5submarine,4surface,8nuclear-submarine,11carrier and6helicopter/drydock/repair. Carrier requires major power; helicopter regional power; drydock/repair major power. These can close most of the copied branch for small coastal navies. Parent proposal is mechanically coherent:20nodes for USA/SOV and 15 for DDR/IRQ/UAE, omitting the three submarine nodes and two carrier/operator nodes. Rewire the retained drydock join and vessel-production parent explicitly after omissions; lower/remove major-status gates for adapted coastal facilities without changing the retained geometry.

Source: `common/national_focus/00_generic.txt:4450-4960`.

### mastery

add_mastery is a real current native effect and applies to active matching doctrine tracks. The selected-doctrine requirement is real and meaningful; conditional subdoctrine bonuses are not guaranteed threefold grants. Retain the real selected-naval-doctrine gate for doctrine mastery programmes, including execution. Preserve XP/use counts and actual matching filters. Do not advertise mastery as a free doctrine unlock or as guaranteed useful when no track exists.

Source: `common/scripted_triggers/00_doctrines_scripted_triggers.txt:126; installed effects_documentation.md:1477`.

### stacking

The donor gives substantial lasting/economic and730day bonuses. Existing national naval/industrial programmes remain active independently. Combined Defense Industries affects tax/GDP component productivity, while +20%dockyard output is a different native production modifier. These are not one interchangeable naval statistic. Prefer the existing donor idea IDs for faithful copies so a same-ID source cannot create a second parallel country clone. Audit additive country-variable bonuses and distinct same-stat ideas before increasing values. Keep durations365/730 and the permanent/temporary distinctions; no universal new cap or unsolicited workforce penalty.

Source: `common/ideas/generic_ideas.txt:535,588,1090,1146,1170,1207`.

## Existing country rewards and minimal copy

The parent proposes 20 nodes for USA/SOV and 15 for DDR/IRQ/UAE, omitting submarines, nuclear submarines, submarine expansion, carriers and helicopter operators in the coastal version. This keeps the recognizable shape while avoiding country-inappropriate capital/submarine paths. The retained drydock join and vessel-production prerequisites must be explicitly rerouted after omissions. Composite/stealth positions can retain era-neutral research outcomes. Keep the existing real category keys, native mastery filters and effect counts rather than inventing equipment aliases or free ships. The donor grants no completed vessel or stockpile package.

Current trees already contain independent naval programmes. Examples: USA `USA_1970_D6` changes its native navy damage/defense/repair variables; SOV `COLDWAR_SOV_the_navy_question`, `the_kiev_class` and `the_shipyards_of_the_north` include naval organization/range/output and research/yard rewards; DDR Baltic/Peene shipyards and naval NVA programmes add output/productivity; Iraq Ship Maintenance adds +10% dockyard output. See JSON for exact current source IDs, prerequisite groups, exclusions and signed contributions. No sum across incompatible political routes is asserted.

Reuse donor idea IDs for faithful same programmes where practical. Separate country clone IDs for identical ideas can introduce another stacking source. Permanent convoy/marine/combined-industry ideas and 365/730 day temporary ideas must remain distinct. The economic combined-industry productivity/tax modifiers are consumed in native GDP/tax calculations; they are not simply the same as naval production output. Do not advertise their four 10% rows as +40% GDP.

Native dockyard and arms-factory helpers bill 7.5 billion per single grant; two-yard helper bills 15. Combined Defense Industries explicitly waives the arms invoice. The composite helper bills 8.5 and places its shared slot after construction. If adopting current country-scaled yard fees instead, SOV/DDR source uses 0.008 GDP per yard and 0.016 for two; that is an explicit adaptation, not the unchanged donor fee. Never retain helper billing and add another invoice.

## Verification boundaries and hashes

The JSON preserves all 20 full availability/completion ASTs, exact prerequisite groups, eight findings, native documentation anchors, country stacking pointers and current source hashes. This establishes source mechanics and transitive references. Live 1970 hulls/project progression, timed-idea stacking, bonus consumption, transaction outcomes and multiplayer behavior remain unobserved.

| Source | SHA-256 |
| --- | --- |
| `common\national_focus\00_generic.txt` | `0fb010d416dcbf26cd73336a5b82300a2c35af038f7c664a501fef854cf4243e` |
| `localisation\english\MD_focus_GENERIC_l_english.yml` | `d982a49fb1c38a0a9c67b930c8bfbeab48851ff071bacad11a4f012593dfbd0d` |
| `descriptor.mod` | `f983a4178909871786ffcd7899952648373718f8cebcf03378cdca8cae35b025` |
| `common/ideas/generic_ideas.txt` | `ec379701a14a60feaaa13a7cd884f7a776becec8ba4453d929af6bd2d5f44326` |
| `common/scripted_effects/00_scripted_effects.txt` | `d0bacf977ad58bfa084f3d4e53ece1b89a28112238ed28324a178424a39b25af` |
| `common/scripted_triggers/00_scripted_triggers.txt` | `ddb35fbd1927a800f91a0480bc48b39e0ad33a094f43d549d732237b0befe209` |
| `common/scripted_triggers/00_doctrines_scripted_triggers.txt` | `aa260527bf1af37eff9d9659afb4f5231d761ecedf878efc007efca7ca154e78` |
| `common/special_projects/projects/naval_projects.txt` | `e58cc71b4df1d6ecd81aad2d8d36a30234e20b86f13f6f8c100e3d86fd109836` |
| `common/special_projects/projects/civilian_projects.txt` | `9a37af829e8b8c6f7706741f384f8a9543fd142ae7592a140203a945032059c5` |
| `common/technologies/naval.txt` | `a70891da3d9f086b6f7ce525d83ceb03d0c76ca2cddd6287511b06900506426d` |
| `common/technologies/industry.txt` | `43c94b4cc27a65683af4bcbe2f9afe1207fe90b43ff5746c068760b04eb9c859` |
| `common/technologies/mdcw_historical_air_naval.txt` | `008d9dfdae81ebd889c598e1c72189417ce0833b65f7b13519d22467e174d5f4` |
| `common/technology_tags/00_technology.txt` | `e55442ebd0bbb7478897d0ddddc3d7738ed8acd6432c892b6b7ed43304dd2611` |
| `common/units/equipment/MD_convoys.txt` | `d75201111e3edd820f960f82e95fed638df0eca3df44c659fcd178b83bf7838a` |
| `common/buildings/00_buildings.txt` | `cee577c4a89085e1745b2c38a7f5609346bd4b7407848d932b22078244bfb1be` |
| `common/modifier_definitions/money_modifier_definitions.txt` | `a416032e9ef73d93e48249255b8caa8857d320ba518b2192566a6cbcbd741ce8` |
| `common/scripted_effects/00_money_system.txt` | `cc89f09d19c5f70af31023c4d14f9c3ae36bf454803affdcb537fe839fd4e23f` |
| `common/national_focus/USA_1970.txt` | `8f494e3aa01c5882c79aa336e17d286c9f131cdeabcb651b654d9317875ec043` |
| `common/national_focus/COLDWAR_SOV_1970_focus.txt` | `2b0beb6dfd49ee5910d5bb35f963b5adcdeadcf29c145e7e87d85caba86b1c69` |
| `common/national_focus/COLDWAR_DDR_1970_focus.txt` | `58397c0c0f1f047e1cd804da58a16d70920bfbd6528295f68fb43c40792221d9` |
| `common/national_focus/COLDWAR_IRQ_1970_focus.txt` | `4e8c02d48fb8bd9b08ad23cbedd672c8f84f698530577aa82b4f2e6980b37b01` |
| `common/national_focus/COLDWAR_UAE_1970_focus.txt` | `9550d90f7306b170896d72db393749528b6450029263e35b4406cf20518ddd57` |
| `history/countries/USA - USA.txt` | `0342bda336b6bdfe2f63e217a145c548ff39c6d9d872348dabda104ed6f22d2d` |
| `history/countries/SOV - Russia.txt` | `ea6072a1933b0234d48116981a9e2513a787d549166cf58a458937c9157ed5b1` |
| `history/countries/DDR - East Germany.txt` | `2752381771a5ddc2cb4528eb05ef67b5edc88a7f71e75fd03def599af5c8ea3c` |
| `history/countries/IRQ - Iraq.txt` | `3d30a5d7b340d420ceda5a9e2643bacd4e7156d617e2897202c92ec4c84c2b9e` |
| `history/countries/UAE - United Arab Emirates.txt` | `db456b93b6f7bcabdcf32134798a5898f8d159e8579de05a171bca538c0416f8` |
