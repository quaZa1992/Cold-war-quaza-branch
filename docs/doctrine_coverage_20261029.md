IMPERIA COLD WAR

# Land doctrine coverage and immediate trade-offs

User revision, 29 October 2026. This supersedes the affected unit scopes and activation values in the earlier concept and trade-off reports. The approved original concept and prior engine evidence remain historical records.

## Foot formations and specialist troops

Forest Envelopment now applies its forest modifiers to all Foot Infantry category members and the dismounted Ranger Battalion, Air Assault Battalion and Ranger Reconnaissance Company. This includes light infantry, militia, foot paratroopers, marines, marine commandos and Special Forces. Every eligible unit receives the forest bonus once: initially +10 percentage points of forest attack and movement, finally +20 attack, +20 movement and +10 defence. Its -10% maximum planning trade-off remains.

The same missing specialist coverage is corrected wherever a land doctrine grants Foot Infantry bonuses, including Assault Breaching, Key Zone Defence, Guided Anti Armour Integration and the older operational/dedicated variants. Territorial Defence's identical light-infantry and militia terrain blocks are combined and extended to the same foot formations. Existing explicitly mounted formations and deliberately militia-specific bonuses retain their roles. Vehicle-mounted special forces and the rotorcraft support attachment do not gain a foot-movement bonus merely because they carry a special-forces category.

Mission Rehearsal now grants **+5% maximum planning immediately**, retaining its existing +5% planning speed. The later +10% maximum planning reward remains, giving +15% after mastery. Training and personnel costs remain in place.

## All artillery types

General land-doctrine artillery attack bonuses now use the registered native unit-category modifier `modifier_army_sub_unit_category_artillery_attack_factor`, with the English label **All Artillery Attack**. The common MD Artillery category includes towed guns, self-propelled artillery, MLRS, their light/regimental and support-battery variants, and air-assault artillery. MLRS need explicit category coverage because their native unit type is `rocket`, rather than `artillery`.

This replaces the narrower modifier instead of adding a second overlapping attack bonus. Values and unlock timing remain the same. Counterfire Coordination's existing category-wide defensive reward also remains. Native MD category membership is preserved, including its forward-observer/pathfinder support member and optional special-unit artillery. No new unit category or equipment requirement is invented. The modifier's identifier is also registered in `common/synchronized_dynamic_tokens/mdcw_doctrine_tokens.txt` for deterministic script-variable access.

## Grand doctrines

All fourteen land Grand Doctrines now have an immediate drawback that remains a drawback throughout their own progression. The table gives their own fully mastered penalties, before other independent choices or national modifiers.

| Grand doctrine | Persistent drawbacks |
| --- | --- |
| Combined Arms | Supply consumption +8%; training time +10% |
| Shock And Awe | Army fuel consumption +15%; out-of-supply penalties +10% |
| Defence In Depth | Attack movement speed -10%; organisation loss while moving +10% |
| Mission Command | Training time +15%; army personnel costs +8% |
| Battlefield Support | Army speed -5%; supply consumption +15%, including its existing +10% milestone |
| Guerrilla Warfare | Breakthrough -10%; maximum planning -15%; its existing +10% upkeep attrition milestone remains |
| Deep Operation | Initiative -5%, existing |
| Active Defense | Breakthrough -10%; attack movement speed -5% |
| AirLand Battle | Army fuel consumption +5%, existing |
| People's War | Armour attack -10%; maximum planning -10% |
| Total Defence | Non-core attack -5%, existing |
| Fanatical Struggle | Experience loss +10%; coordination -5%, existing |
| Deliberate Firepower | Planning speed -10%; supply consumption +12%; army speed -5%, existing |
| Mobile Raiding Warfare | Out-of-supply penalties +15%; maximum planning -10%; army defence -5%, existing |

Battlefield Support previously borrowed Mission Command's description key. It now has its own historical support-command description and its own numeric costs.

## Existing subdoctrines in all six land tracks

The audit covers all **45 older subdoctrine entries and all 12 expansion entries**, across Structure, Operational Theory, Dedicated Doctrine, Training, Leadership and Technology. Operational/dedicated twins are audited individually. Existing drawbacks are retained rather than indiscriminately adding a second penalty to every choice.

- **Skill School:** training time rises from +10% to +15%, with +5% supply consumption immediately. Its existing progression adds +14% personnel costs by full mastery. Technical proficiency remains strong, but courses and live-fire training consume time and supplies.
- **Officer Training:** +10% training time immediately. Its existing first mastery reward adds another +10%, leaving +20% at full mastery. Existing personnel and promotion costs remain.
- Other old choices already have costs such as fuel demand, equipment upkeep, slower training, lower armour attack, planning limits, stability loss, or reduced offensive mobility. Those are checked from activation through every reward, rather than looking only for a minus sign. A positive cost modifier is also a real debuff.

`coverage_validation.json` records each entry's actual drawbacks at every stage. This is an audit of the six land strategy tracks shown by the user. It does not rebalance the separate air, navy, equipment or special-forces doctrine folders.

## Stat colours

The installed base-game English `stats_l_english.yml` defines `STAT_MODIFIER_VALUE` as `$VALUE|=G0%$`, forcing generic unit-stat modifiers green even when negative. A bounded English replacement changes this to the native signed formatter `$VALUE|=+0%$`: negative soft attack and breakthrough are red, positive values green.

Country modifier definitions and inverse-stat formatters, including `STAT_MODIFIER_DIFF_NEG` and the supply-consumption formatter, are untouched. This is a shared native unit-stat formatting correction, not a prose overlay or duplicated effect tooltip. A new game launch is required to load this localisation and the new category modifier reliably.

## Historical rationale and rights

The exact numbers are game-balance choices. The sources support the institutional and tactical trade-offs, not measured percentage effects.

- **Command and training:** [US Army, The Development and Training of the South Vietnamese Army, 1950-1972](https://history.army.mil/portals/143/Images/Publications/catalog/90-10-1.pdf), especially the 1968-1972 school and instructor discussion, documents the demands of expanding branch schools and leadership education. [Army University Press, NCO professional development](https://www.armyupress.army.mil/Books/Browse-Books/iBooks-and-EPUBs/NCO-Primer/) covers wartime leadership shortages and the 1971 NCO education system. Longer courses, personnel expense and training supplies are balance abstractions of institutional investment.
- **Forward defence and offensive limits:** [US Army, AirLand Battle emerges](https://www.army.mil/article/266846/) explains the criticisms of the 1976 doctrine's defensive and first-battle emphasis and the later move toward depth and counterattack. Active Defense's offensive trade-offs draw on that distinction.
- **Support commands:** [CASCOM history, Logistics Center 1973-1990](https://cascom.army.mil/about/history/) records the integrated organisation of logistics concepts, units, careers and exercises. The movement and supply penalties represent the burden of the chosen support structure.
- **Rapid dominance:** Harlan Ullman's [NDU PRISM account](https://ndupress.ndu.edu/Portals/68/Documents/prism/prism_2-1/prism_2-1.pdf), pages 79 onward, dates the formal concept to the 1996 NDU publication. The inherited name is retained and the description makes its later date explicit. Fuel and supply exposure describe this game's high-tempo interpretation, rather than a claim that the original concept was simply a fuel-intensive land assault.
- **Irregular versus regular warfare:** [Military Review, US Tactics in Vietnam](https://www.armyupress.army.mil/Portals/7/military-review/Archives/English/50th-Anniversary/50th-Bradford/us-tactics-in-vietnam.pdf) distinguishes guerrilla activity from mobile and positional warfare. [Military Review, CORDS](https://www.armyupress.army.mil/Journals/Military-Review/English-Edition-Archives/COIN-Reader-1/Andrade-Willbanks-MA-2006/) distinguishes local guerrillas from substantial regular main forces. The game penalties describe the selected irregular or dispersed force emphasis, not an assertion that Chinese or Vietnamese regular armies could never conduct large offensives.
- The earlier approved concept and trade-off report retain the Finnish, Austrian, Swedish, Egyptian and southern African precedents. Broadening dismounted training to comparable foot specialists is a game-design inference from shared battlefield roles.

New prose, integration code and balance values were authored for this project. Existing MD/Paradox code and localisation retain their upstream authorship. Individual upstream authors and separate redistribution permissions remain unknown where not identified in existing notices. No artwork, font or third-party document is copied or changed in this revision.

## Verification

The immutable semantic input is `tools/doctrine_expansion_1970/scope_baseline_20261029.json`. An independent AST transformation checks the exact authorised changes while preserving identities, access, costs, reward order and every unrelated value. Generator checks are idempotent. Encoding, localisation collisions, description sizes and current numeric acceptance values are also checked.

Source results: **1,189/1,189 coverage checks** and **295/295 integration checks** passed. Coverage checks all 71 land entries at activation and every progression stage, specialist parity without duplicate foot bonuses, all artillery variants, synchronised token registration, early Mission Rehearsal planning, and the sign-dependent colour format. Native engine results are recorded separately after the isolated run. Single-client loading and source proofs do not certify multiplayer balance or save/rehost behaviour.

The first private engine attempt reached its five-minute loading limit before startup events. While parsing the probe's modifier observation, it reported the missing synchronised token. That diagnostic prompted the production registration above; the complete unsuccessful result remains in `native_result_coverage_attempt_1.json` and its E: profile. The corrected run uses a fresh profile, a longer loading allowance, the verified immutable scripts and a separately hashed fixture copy of the new synchronised-token file. The original snapshot is not edited. The user ended Computer Use with Escape during loading, so no further UI inputs are issued and no live tooltip-colour inspection is claimed.

The corrected run **passed**, reaching **2 January 1970 at 16:00** after **285.3 seconds**. Its fresh profile is `E:/HOI4_Mod_Tools/mdcoldwar/runtime/doctrine_expansion_1970/20261029_192928/profile/`. All fourteen immediate grand-penalty observations passed. The original twenty-four mastery slot checks and three additional school checks passed, covering twenty-one distinct subdoctrines. The schools' immediate training-time delta was +0.30 as expected. The actual category-wide artillery modifier fell by exactly 0.30 on a grand/track replacement, and the raiding supply-gap penalty fell by 0.15. The Territorial Defence exclusion remained effective.

There were no diagnostics referencing the affected doctrine files, category modifier, token registration or probe. This does not certify unrelated mod files. All eighteen affected runtime inputs match the installed source hashes, accounting explicitly for the single new token file loaded from the fixture overlay. `coverage_revision_evidence.json` records the exact correspondence and successful markers; `native_result.json` retains the complete current native result. No multiplayer, save/rehost or live-tooltip-colour claim is made.
