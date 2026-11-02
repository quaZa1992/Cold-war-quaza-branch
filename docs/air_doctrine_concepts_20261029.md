IMPERIA COLD WAR

# Air Command: researched expansion and complete balance proposal

Design brief, 29 October 2026. Requested deliverable: researched concepts and concrete values for additional Grand Doctrines and subdoctrines, with appropriate drawbacks for every existing Air Command choice. **This is a proposal. No runtime doctrine, localisation or game asset is changed by this brief.**

The complete numerical catalogue is [Air Command values](air_doctrine_values_20261029.md). It contains every activation bonus, all thirty new grand milestones, all seventy new subdoctrine rewards, cumulative values and the complete forty-five-row inherited drawback schedule. The exact machine-readable fields and checks are in `tools/air_doctrine_design_1970/concept_values.json`.

## What the current system actually contains

- Seven Grand Doctrines, each costing **100 Air XP** and supplying six ordered track slots and six matching milestones.
- Thirty-eight existing subdoctrines, each costing **75 Air XP**, with five mastery rewards. A complete six-slot initial selection therefore costs **550 Air XP** before discounts or later replacements.
- Seven track types: **Training and Operations** (3 existing choices), **Aircraft Design** (7), **Heavy Aircraft** (6), **Multirole Aircraft** (5), **Strike Aircraft** (6), **Fighter Aircraft** (6), and **Drone Warfare** (5). A grand has six slots, so it cannot offer all seven different tracks at once. Some repeat a track.
- The default is **100 mastery per reward**, or **500 mastery** for a subdoctrine, with a **40 monthly cap** and a training contribution factor of **0.1**. Five hundred mastery takes at least 12.5 months at that cap, before any applicable engine exceptions; it is not an automatic scheduled duration.
- Air tracks use a manpower/equipment-contribution multiplier of 5, while most subdoctrines override theirs to 6 and Centralized Command uses 2. These are mastery-contribution parameters, not an XP purchase price or a directly linear time multiplier. The proposal standardises the normal subdoctrine override to **6**, including Centralized Command, to avoid an unexplained progression difference.

The current grand set is Local Airspace Defense, Strategic Destruction, Battlefield Support, Air Supremacy, Autonomous Air Operations, Mixed Role and Integrated Air Warfare. Most benefits are country-wide mission modifiers, unit-category stats or airframe equipment bonuses. Their scopes differ materially.

## Design rules

1. Every option has a visible initial drawback and at least one genuine disadvantage remaining after its own mastery. Existing rewards cannot silently turn the same advertised drawback into a net buff. A separate, independently selected doctrine may compensate at an opportunity cost.
2. Strong effects pay through an actual operating burden or tactical limitation: fuel, personnel, qualification rate, range, agility, protection, particular mission efficiency, or production cost. A positive cost is a debuff; a negative accident or experience-loss modifier is a buff.
3. The generalist provides useful breadth; a specialist must clearly outperform it in the chosen task. No single fighter or multirole branch should simultaneously offer the best combat, training, escort, range and affordability.
4. Country examples justify the concept, not national access restrictions. Geography, industry, fuel, aircrew depth, aircraft and the expected enemy determine suitability. Later historical examples do not mean every country has that equipment in 1970.
5. New player-facing names and historical descriptions are English. Costs and effects use real native modifiers, with the appropriate colour polarity. This design introduces no disguised recurring fee, workforce penalty or generic research tax.

## Five new Grand Doctrines

Values in this table are the **fully mastered contribution of the grand alone**. They do not already include selected subdoctrines. The catalogue also gives the on-selection values and the exact six milestone additions.

| Doctrine | Strategic identity | Principal completed benefits | Persistent drawbacks |
| --- | --- | --- | --- |
| **Dispersed Air Defence** | Sustain a smaller defensive air force after disruption to its bases | Interception efficiency +20%; air-base repair +50%; home air defence +10%; interception detection +10%; accident chance modifier -10%; wing XP loss modifier -10% | Air force personnel costs +12%; air range -10% |
| **Selective Air Denial** | Conserve a smaller fighter force and contest selected engagements | Interception efficiency +20%; interception detection +10%; eligible fighter attack +10% and defence +5%; home air defence +10%; wing XP loss modifier -15%; air fuel use -5% | Air-superiority mission efficiency -15%; escort efficiency -10% |
| **Offensive Counter Air** | Prepare coordinated attacks on the opponent's air infrastructure | Bombing targeting +20%; multirole/strike bombing stat +15%; escort efficiency +15%; mission XP +10%; mission efficiency +5% | Air fuel use +15%; home air defence -10% |
| **Maritime Air Denial** | Make a stronger fleet's sea approaches dangerous | Naval mission efficiency +25%; naval strike targeting +10%; naval strike attack +10%; naval-aircraft surface detection +15% and range +10%; port strike +10%; bad-weather penalty modifier -10% | CAS efficiency -15%; air-superiority mission efficiency -10% |
| **Counterinsurgency Air Support** | Sustain close support where hostile fighter power is limited | CAS efficiency +15%; ground-support combat modifier +10%; CAS/gunship ground attack +10%; CAS organisation damage +5%; mission XP +15%; air-base repair +25%; ground-attack modifier +5% | Air attack -10%; strategic bombing -20% |

**Historical fit:** Swedish wartime-base planning supports dispersal and mobile servicing, rather than a blanket industrial-damage shield. [Swedish Armed Forces air-base history](https://www.forsvarsmakten.se/siteassets/6-information-och-fakta/historia/vagbaserna/fortv-2007-1.pdf). Finnish defensive priorities and Vietnamese controlled attacks support conserving aircraft and choosing engagements. [General Heikki Nikunen](https://www.mannerheim.fi/13_erity/Nikumar.htm), [NDU Press](https://ndupress.ndu.edu/Media/News/News-Article-View/Article/2076617/adapting-to-disruption-aerial-combat-over-north-vietnam/).

Israeli airfield attacks in 1967 support the counter-air concept. Their result is not treated as a reusable automatic first-strike event. [US Air Force doctrinal history](https://www.dafhistory.af.mil/Portals/16/documents/Studies/101-150/AFD-090529-053.pdf). Argentina's 1982 operations support a maritime strategy with restricted reach and demanding flight profiles. [RAF Museum](https://www.rafmuseum.org.uk/research/research-enquiries/history-of-aviation-timeline/british-military-aviation/1982-2/). Portuguese African deployments and pilot preparation support a light tactical-support emphasis. [Portuguese Air Force](https://emfa.pt/unidade-18-base-aerea-n-5).

**Available tracks:**

| Grand | Slots, in milestone order |
| --- | --- |
| Dispersed Air Defence | Training and Operations; Aircraft Design; Fighter Aircraft; Fighter Aircraft; Multirole Aircraft; Strike Aircraft |
| Selective Air Denial | Training and Operations; Aircraft Design; Fighter Aircraft; Fighter Aircraft; Multirole Aircraft; Heavy Aircraft |
| Offensive Counter Air | Training and Operations; Aircraft Design; Fighter Aircraft; Multirole Aircraft; Strike Aircraft; Drone Warfare |
| Maritime Air Denial | Training and Operations; Aircraft Design; Fighter Aircraft; Multirole Aircraft; Strike Aircraft; Heavy Aircraft |
| Counterinsurgency Air Support | Training and Operations; Aircraft Design; Multirole Aircraft; Strike Aircraft; Heavy Aircraft; Drone Warfare |

This gives denial two fighter choices, maritime warfare both search and strike access, and counter-air a reconnaissance/decoy option without also granting every heavy-support choice.

## Fourteen additional subdoctrines

Each has five 100-mastery stages and costs 75 Air XP. Principal end values are condensed here; the catalogue retains every additional modifier and each stage. Drawbacks start on selection and persist.

| Track | New choice | Principal completed benefits | Persistent drawbacks |
| --- | --- | --- | --- |
| Training and Operations | **Dispersed Servicing Teams** | Air-base repair +40%; interception efficiency +10%; accident chance modifier -10% | Air force personnel costs +10%; escort efficiency -5% |
| Training and Operations | **Adversary Air Training** | Training XP +25%; wing XP loss modifier -20%; mission XP +10%; untrained-pilot penalty modifier -10%; ace effectiveness +5% | Air fuel use +10%; air force personnel costs +12% |
| Aircraft Design | **Field Maintainable Designs** | Specified tactical airframe production IC -5%; air force personnel costs -8%; accident chance modifier -15% | Maximum speed of those tactical airframes -5% |
| Aircraft Design | **Rugged Attack Designs** | CAS and gunship ground attack +15%, air defence +10%; accident chance modifier -10% | CAS/gunship maximum speed -5% and air attack -10% |
| Heavy Aircraft | **Tactical Airlift Procedures** | Transport airframe range +20%, fuel consumption -10%; organisation after paradropping +10%; accident chance modifier -10% | Air force personnel costs +10%; training XP -10% |
| Heavy Aircraft | **Maritime Search Coordination** | Maritime-aircraft surface and sub detection +20%, range +10% | Those aircraft's naval strike attack -10%; air force personnel costs +10% |
| Multirole Aircraft | **Low Level Penetration** | Multirole/strike air defence +15%, maximum speed +5%, ground attack +10% | Their range -15%, bombing stat -10%; accident chance modifier +15% |
| Multirole Aircraft | **Stand Off Strike Packages** | Multirole/strike bombing stat +20%, range +15%, defence +10%; bombing targeting +10% | CAS efficiency -15%; air force personnel costs +12% |
| Strike Aircraft | **Forward Air Control** | CAS efficiency +15%; CAS organisation damage +10%; mission XP +10% | Strategic bombing -15%; air force personnel costs +10% |
| Strike Aircraft | **Sea Skimming Strike** | Naval strike attack +25%, targeting +20%; maritime-aircraft defence +10% | Maritime-aircraft range -20%; accident chance modifier +15% |
| Fighter Aircraft | **Ambush Interception** | Interception efficiency +20%, interception detection +15%; eligible fighter attack +10% | Escort efficiency -15%; air-superiority mission efficiency -10% |
| Fighter Aircraft | **Section Mutual Support** | Eligible fighter air defence +15%; wing XP loss modifier -20%; escort efficiency +10% | Those fighters' air attack -5%; ace generation chance modifier -15% |
| Drone Warfare | **Reconnaissance RPV Operations** | Air-superiority detection +15%; interception detection +10%; bombing targeting +10% | UAV air defence -10%; air force personnel costs +10% |
| Drone Warfare | **Decoy RPV Operations** | Multirole/strike air defence +10%; bombing targeting +15%; escort efficiency +10% | UAV air defence -20%; air force personnel costs +8% |

**Why these are different:** Field maintenance improves the cost of operating tactical aircraft, whereas Adversary Air Training invests fuel and staff in more capable crews. Maritime Search sacrifices weapon employment to find contacts; Sea Skimming prioritises attacks within a shorter radius. Section Mutual Support preserves formations; BVR and WVR remain combat specialisations. Airlift is a transport doctrine, not a disguised universal supply buff.

**Historical anchors:** Red Flag began in 1975 to provide realistic combat preparation. [Nellis AFB](https://www.nellis.af.mil/About/Fact-Sheets/Display/Article/2605882/414th-combat-training-squadron-red-flag/). Norwegian Orion service from 1969 supplies the search/sensor precedent. [Institutional report to Parliament](https://forsvarsombudet.no/wp-content/uploads/2021/04/2009-Dokument-5-Ombudsmannsnemnda-for-Forsvarets-innberetning.pdf). Korean FAC/TACP cooperation supports Forward Air Control. [USAF Museum](https://www.nationalmuseum.af.mil/Visit/Museum-Exhibits/Fact-Sheets/Display/Article/196086/close-air-support-battering-from-above/).

The RAF's 1991 experience supports the benefits and risks of low-level attacks, and the separate value of deliberate designated strikes. [RAF Museum](https://www.rafmuseum.org.uk/research/research-enquiries/history-of-aviation-timeline/british-military-aviation/1991-2/). Thach's early-1940s mutual-support tactics support formation survival rather than extra lone-ace bonuses. [US Naval History and Heritage Command](https://www.history.navy.mil/content/history/nhhc/our-collections/photography/us-people/t/thach-john-s.html). Reconnaissance RPVs and the 1982 decoy role are distinct from modern armed-drone swarms. [US Army historical study](https://www.armyupress.army.mil/Portals/7/combat-studies-institute/csi-books/OP37.pdf), [contemporary Air University Review](https://www.airuniversity.af.edu/Portals/10/ASPJ/journals/1984_Vol35_No1-6/1984_Vol35_No6.pdf).

## Every inherited choice receives a drawback schedule

The catalogue includes **all 7 old grands and all 38 old subdoctrines**, grouped by their actual tracks. Nothing is omitted because it is modern, specialised, or duplicates another displayed name. Some examples demonstrate why the base and full-mastery columns differ:

| Existing choice | Proposed persistent result | Interpretation |
| --- | --- | --- |
| Centralized Command | Mission XP -10%; personnel costs +5% | Initial mission XP change is -25%, offset partly by its existing +15% reward |
| Aerial Refueling | Air fuel use +15%; personnel costs +8% | Initial fuel change is +25%, offset by the existing -10% reward |
| Drone Designs | Small and carrier UAV airframe defence -5%; medium UAV defence -15% | The -15% initial equipment change survives the existing +10% rewards where those apply |
| Heavy Gunship | Gunship air defence -10%; maximum speed -10% | Initial defence change is -35%, offset by its existing +25% progression |
| Skill-focused alternatives in the air system | Each receives its own mission, personnel, aircraft-performance or qualification trade-off | There is no invented general air-training-time modifier |

The numbers above remain separate native contributions. For example, a country-level attack factor and an airframe's attack stat cannot simply be added and called the final damage increase.

## Targeted correction of inherited outliers

Adding weak penalties while leaving every inherited peak unchanged would keep several old packages more attractive than the new specialists. The proposal therefore includes eight bounded positive end-state adjustments, fully listed in the catalogue:

- **Air Supremacy, fighter subdoctrine:** air attack +17.5% instead of +27.5%, agility +10% instead of +17.5%, escort +15% instead of +30%, superiority efficiency +10% instead of +20%. It remains the broad fighter specialist and gains a +15% production-IC drawback on its actual fighter airframes.
- **Light Fighters:** completed attack +17.5% instead of +27.5%, with shorter range and weaker defence.
- **BVR Combat:** eligible fighter attack +20%, superiority efficiency +10%, both detection modifiers +15%. Agility -7.5% and personnel costs +8% remain. Benefits and penalties must cover the same eligible fighter roles.
- **WVR Dogfighting:** eligible fighter agility +15% and defence +5%, with range -10% and training XP -15%. Its combat skills should not inexplicably apply only to Light Fighters.
- **Mixed Multirole:** a broad but moderate package. Attack/agility +7.5%, ground/bombing +10%, range/defence +5%, naval attack +5%, naval targeting +2.5%, alongside its new costs.
- **Strike Aircraft:** lean towards ground attack +17.5% and bombing +12.5%, with the proposed net -5% agility. Its remaining changed targets are specified in the catalogue.
- **Multirole Ops:** ground attack and bombing +12.5%, air attack +5%, air defence +7.5% for its two supported roles, retaining its range and staff burden.
- **Local Airspace Defense:** keep the home-defence/static-AA identity but reduce unrelated universal support benefits. Air-base repair +25%, fuel use -5%, training XP +15%, air XP +10%, untrained-pilot penalty and wing XP-loss modifiers -15%. Replace its hidden manufacturing spirit with a doctrine-owned +10% interception-detection milestone. The old hidden spirit must be removed safely during migration; it must not remain as a free manufacturing discount after switching doctrines.

These positive targets require a deliberate redistribution across the existing five rewards or six milestones. They are end-state specifications, not a claim that a finished runtime progression has already been authored. The new concepts already have complete stage-by-stage values.

## Native integration findings that must accompany implementation

1. **The old SEAD value does not implement enemy SAM suppression.** `tech_air_damage_factor` is documented and localised as a country/static-AA bombing-damage-reduction factor. Its negative use in several air branches cannot be advertised as protection against enemy SAMs. Remove the misleading uses. For SEAD, replace the initial -10% and first -5% with +5% multirole/strike air defence at selection and another +5% at the first reward. Together with its existing defence reward, those roles reach +15%. This models general package survivability and coordination, not a new suppression simulation or automatic removal of enemy AA units.
2. **The hidden manufacturing idea has no doctrine-switch removal in the searched runtime references.** Local Airspace Defense adds an idea granting -20% small-airframe production cost via a scripted effect. The idea only appears in its definition and grant, with no matching removal found. Doctrine-owned `equipment_bonus` effects have native cleanup support; unrestricted `add_ideas` does not provide that guarantee. The concept replaces this benefit rather than silently retaining an exploitable discount.
3. **Fighter categories are narrower than their names suggest.** Light Fighters, Air Superiority Fighters, Multirole Fighters and Strike Fighters use separate MD categories. `category_fighter` is not a reliable blanket for all four. BVR/WVR and general fighter teamwork should cover the intended four-role union once, including carrier equivalents where their native categories already include them. Dedicated CAS/gunships, transports, RPVs and fantasy heavy units are not automatically fighter-training beneficiaries.
4. **CAS and gunships need explicit role coverage.** The gunship has `category_gunship`, not the CAS category. Shared attack-survivability concepts target both disjoint scopes. Naval categories must include light, medium, large and carrier platforms when the concept is genuinely general maritime aviation.
5. **Drone mastery has a source-level classification collision.** Its equipment filter is `suicide`, while `med_transport`, `cv_med_transport` and `large_transport` also declare that type. This establishes a classification risk, not a measured live mastery result. Restrict the intended drone contribution to actual UAV units/categories and verify the native behaviour. Do not let transport flights become the convenient training route for a drone-only track.
6. **Reusable reconnaissance RPVs need a real reconnaissance role.** A 1960s/1980s reconnaissance doctrine must not quietly turn every drone into expendable strike ammunition. Check and separate reusable scout-capable designs from loitering munitions. Doctrine selection neither grants an airframe nor changes an unarmed aircraft into an operational UCAV.
7. **Modern inherited concepts stay identified as later capabilities.** Autonomous Air Operations, armed MALE employment, carrier UCAS and swarm integration must not be presented as established 1970 practice. All receive the specified costs, but their equipment access and descriptions need period-appropriate capability gates or explicit later content. Experimental armed RPV work is not evidence for a mature 1970 armed-drone force.
8. **Current Japan access conditions require a 1970 check.** All seven old grands reference a particular Japanese focus/BOP condition. That condition is recorded in the inventory. Do not copy a modern political dependency into the new global doctrines without checking the actual 1970 Japanese content. New historical examples are not nation locks.
9. **No fictional economy API:** the current `airforce_personnel_cost_multiplier_modifier` feeds the native weekly MD personnel budget channel, including the channel's existing weighted aircraft, AA and missile-site entries. It is not aircraft purchase cost. The global equipment-upkeep multiplier observed in this source does not supply an aircraft-only upkeep modifier. Aircraft manufacture instead uses correctly scoped `build_cost_ic`; fuel uses the real air-fuel modifier. Do not label personnel costs as maintenance or GDP percentages.
10. **No fake transport-capacity or air-training modifier:** the installed `transport_capacity` modifier concerns naval troop-convoy requirements, not aircraft payload. A separate general `training_time_air_factor` was not present in the inspected native modifier catalogue. The proposal uses transport airframe range/fuel, paradrop organisation and correctly named training-XP effects instead. It promises no unsupported percentage increase in flown supply tonnage.
11. **No reliability filler:** many current airframe archetypes already begin at or above nominal full reliability. Field Maintainable Designs uses accident, personnel and production-cost effects instead of assuming another reliability percentage would remain useful.

These are design and source findings. Only implementation and native tests can certify their complete lifecycle, colours, equipment mapping and save migration.

## Combination review

Three legal six-slot examples are calculated in the catalogue and JSON. They retain exact field scopes:

| Example | Resulting air-personnel cost contribution | Air fuel contribution | Why it is not free power |
| --- | --- | --- | --- |
| Defensive survival | +32% | 0% | Staff-heavy dispersion; range limits, lower individual attack and slower mixed-role training remain |
| Maritime denial | +10% | +8% | Superiority, CAS and escort limits remain; search configuration reduces the aircraft's naval-strike stat. The range penalty is offset by two other choices |
| Prepared counter-air | +60% | +25% | A deliberately expensive training, electronics, BVR, designation, FAC and RPV combination. Its bombing accuracy and coordinated operations require a substantial support establishment |

The totals refer to the native cost modifiers, not final money expenditure. They show why a small air arm might choose cheap field-maintainable designs, simple interceptors or selected engagements rather than trying to stack every expensive coordination layer. Independent branches can counter particular drawbacks by sacrificing another choice. Their costs and lost alternatives must be considered together.

These sums are not combat simulations and do not establish a multiplayer meta. Evaluation must compare actual aircraft designs, fuel, pilot experience, operating radius, enemy fighters/AA, mission selection and casualties. A +20% targeting or interception modifier is not a guaranteed +20% kill rate. Accident and XP-loss modifiers likewise act on their own underlying calculations.

## Deliverables and evidence boundary

- Five new grand concepts with thirty milestones, fourteen new subdoctrines with seventy rewards, and English historical descriptions.
- All forty-five inherited choices have exact proposed initial drawback changes and cumulative results after their existing progression.
- Eight targeted inherited positive-end-state adjustments, role coverage corrections and required semantic/lifecycle repairs are separately specified.
- The arithmetic audit passed **546 checks**, including all old/new penalty stages, complete category coverage, known country modifiers, costs and three legal example builds.
- `build_brief.py` hashes the eight inspected runtime inputs before and after generation. They remain unchanged. The checks validate this proposal's arithmetic and source correspondence; there has been no air-doctrine engine run, live UI inspection or multiplayer trial for this proposal.

Rebuild with `python tools/air_doctrine_design_1970/build_brief.py`. It writes only the concept catalogue and its JSON evidence. Actual runtime implementation would need matching native previews, progression redistribution, access guards, correct effect scopes, doctrine-switch cleanup, migration and appropriate native tests.

Historical sources are credited to their named authors or institutions in the catalogue. New design prose and balance numbers were authored for IMPERIA COLD WAR. Existing MD/Paradox scripts and assets retain their upstream rights; individual authors and separate redistribution permissions are unknown where not recorded. No image or third-party publication is copied into the repository by this proposal.
