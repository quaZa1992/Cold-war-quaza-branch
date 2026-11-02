IMPERIA COLD WAR

# Air Command implementation, 29 October 2026

The approved Air Command proposal is installed in the native MD doctrine system. There are now twelve grand doctrines and fifty-two subdoctrines. Five grands and fourteen subs are new. All seven inherited grands and thirty-eight inherited subs receive an immediate, persistent trade-off. New content includes thirty grand milestones, seventy subdoctrine rewards, nineteen original icons and concise historical English descriptions.

The original approved design files remain unchanged. Their hashes are pinned in `tools/air_doctrine_implementation_1970/baseline.json`. The design catalogue and value tables remain the historical rationale and approval record. `tools/air_doctrine_implementation_1970/installed_values.json` records the actual installed activation, every reward and the full mastered contribution, including the inherited side effects discovered during implementation.

## Added choices

| Track | New choices |
|---|---|
| Grand doctrine | Dispersed Air Defence; Selective Air Denial; Offensive Counter Air; Maritime Air Denial; Counterinsurgency Air Support |
| Training and Operations | Dispersed Servicing Teams; Adversary Air Training |
| Aircraft Design | Field Maintainable Designs; Rugged Attack Designs |
| Fighter Aircraft | Ambush Interception; Section Mutual Support |
| Multirole Aircraft | Low Level Penetration; Stand Off Strike Packages |
| Strike Aircraft | Forward Air Control; Sea Skimming Strike |
| Heavy Aircraft | Tactical Airlift Procedures; Maritime Search Coordination |
| Drone Warfare | Reconnaissance RPV Operations; Decoy RPV Operations |

The native system continues to provide six tracks per grand doctrine. Some grands repeat a track category, allowing different compatible specialisations. A subdoctrine cannot be selected twice. New grand choices cost 100 Air XP; subdoctrines cost 75. Each subdoctrine has five mastery rewards, with multiplier 6. Grand milestones follow completion of the corresponding native track.

## Historical and mechanical fit

Historical precedents include Swedish Bas 60/Bas 90 dispersal and field servicing, Finnish defensive priorities, North Vietnamese ground-controlled interception, Israeli counter-air and RPV operations, Argentine maritime attacks in 1982, Norwegian Orion patrols, Portuguese African air support, the Berlin Airlift, airborne controllers in Korea, Red Flag and section tactics such as the Thach Weave. Detailed source links and claim boundaries remain in the approved catalogue. The exact percentages are balance choices, not measured historical coefficients.

The five new grands emphasise distinct situations: recovering a dispersed home air force, denying selected enemy missions, preparing offensive counter-air packages, contesting the maritime approaches, or supporting a ground campaign with limited hostile air opposition. Their drawbacks concern operating range, alternative missions, fuel, specialist personnel or fighter performance. Existing powerful packages retain their approved positive ceilings and permanent weaknesses.

Personnel-cost modifiers use MD's existing weekly air-force budget stream. They are not aircraft purchase prices or a newly invented upkeep API. Manufacturing costs use scoped airframe `build_cost_ic`; fuel uses native fuel modifiers. No workforce-size penalty or generic research tax was introduced.

## Native integration corrections

- BVR, WVR and general fighter benefits cover the disjoint union of Light, Air Superiority, Multirole and Strike Fighters. Light, Air Superiority and Multirole categories include their carrier equivalents. Strike effects use the actual Light Strike and Carrier Light Strike unit scopes, excluding MD's future strike mothership that shares the broader Strike Fighter category. General CAS benefits and matching CAS drawbacks also cover gunships. Specialist unrelated units do not receive blanket fighter bonuses.
- The old `tech_air_damage_factor` uses were removed from the air branches. That modifier concerns static air defence against bombing, not suppression of enemy SAMs. SEAD's approved replacement gives multirole/strike air defence at activation and first reward, reaching +15% with the existing reward. It models package survivability rather than a new SAM-suppression simulation.
- Four old rewards would otherwise have become empty after removing that incorrect modifier. Existing legitimate defence gains were redistributed into those stages without raising their final totals: Stealth Designs, Electronic Warfare Designs, Heavy Gunships and CAS Operations.
- Local Airspace Defense's hidden -20% small-airframe manufacturing spirit was replaced by the approved doctrine-owned +10% interception-detection milestone. Its old hidden spirit is removed by migration.
- Eight additional inherited production ideas also escaped native doctrine-switch cleanup. Their existing manufacturing and personnel/detection/fuel effects are now direct rewards owned by their subdoctrines. These benefits were absent from the proposal's numeric extractor, so they are explicitly included in the installed-value record. Their upstream definitions in `Various.txt` remain untouched.
- Stealth Designs keeps its inherited -15% production reward on six original frames. Those frames start at +30% production cost, reaching the approved +15% net cost when the reward is mastered. Four other designated stealth frames retain +15%. The -10% range drawback persists. This prevents the old hidden discount from cancelling the intended final cost.
- All nine obsolete ideas are removed once from existing countries, including ideas left after earlier switches. Startup and daily fallback hooks select a valid country scope; after the global migration flag is set, the daily path performs only its flag check. There is no perpetual country scan.
- Drone-track mastery uses the actual UAV unit category. The previously omitted `kamikaze_drone` receives that existing category, so conventional, carrier and expendable UAVs receive the appropriate benefits, drawbacks and mastery eligibility. Transport aircraft that share MD's `suicide` equipment type do not qualify for that track.
- Modern UCAV, swarm and stealth options remain visible but require the actual corresponding technology or completed stealth project. The 1970 Japan tree no longer depends on an unreachable modern Article 9 focus; other starting-date behaviour and national constitutional spirits remain in their own systems.

## Historical reconnaissance RPVs

Two researchable, fixed, unarmed reconnaissance models provide a usable historical basis for the RPV specialisations: Early Recon RPVs (1964) and Tactical Recon RPVs (1978). These are generic programmes informed by Ryan and Israeli precedents, not named aircraft replicas with purported historical production prices.

The models use MD's existing UAV subtype and regular air-force accounting. They permit reconnaissance and training and have zero attack, bombing, naval attack and air-superiority stats. Research does not grant free aircraft. They must be produced and deployed. The 1978 programme requires the 1964 programme. The existing later drone research is not made dependent on these new programmes.

Both existing aircraft research folders receive native grid registrations in separate rows. The donor grid uses 70 x 70 slots, LEFT format and a 400 x 1000 extent. Original neighbouring GUI definitions and all unrelated equipment enums are preserved. Research titles fit the native 166-pixel label width. The two model IDs are registered in MD's equipment enum. RPV specialisations accept either historical reconnaissance programme or the appropriate later drone technology.

## Art and localisation

Nineteen transparent pictograms were generated with the built-in ImageGen tool using native MD air-doctrine references: blue-grey aircraft, black outlines and orange tactical accents. They are exported as native 64 x 64 BGRA32 DDS. Original masters, prompts, source paths, hashes and donor credits are retained. `tools/air_doctrine_implementation_1970/icon_review.png` shows every icon at native and enlarged size; it is an asset composition, not a live screenshot.

All player-facing additions are English. The 64 main descriptions and nineteen new doctrine names are measured with the actual inherited BMFont advances against the native selection and description fields. Subdoctrine stages have specific names and descriptions. Signed effects remain native numeric previews. Existing stat-colour correction is reused. Source/asset notices identify unknown original artists or separate permissions explicitly; no project label is painted onto runtime art.

## Verification record

Final result: **1,192 static checks passed; the final native run completed with zero failed fixture assertions and zero air-feature engine errors. All twelve grands and fifty-two unique completed subdoctrines passed. All fourteen installed runtime files match the final native-test overlay hashes.** The final private profile is `E:/HOI4_Mod_Tools/mdcoldwar/runtime/air_doctrine_1970/20261029_204011/profile`; the bounded run took 235.8 seconds.

Current machine-readable results are in `tools/air_doctrine_implementation_1970/implementation_result.json`, `validation.json`, `native_result.json` and `native_run_location.json`. The native runner uses private profiles and frozen scripts on E:, never follows asset junctions, retains complete logs and terminates only its own test process.

The first run established selection and mastery for the complete catalogue, then exposed missing equipment-enum and research-grid registrations and a startup-scope error. A later run caught non-native decimal spellings in redistributed rewards and was stopped deliberately. Those integration problems were corrected. The fixture was also corrected to inspect both closed RPV gates before granting the technology, rather than assuming a same-event technology reset. The final run and its exact fourteen-file overlay hashes are recorded separately, preserving the failed evidence.

Static verification covers approved cumulative values with documented adapters, every progression stage's surviving trade-off, nonempty rewards, absence of unowned idea grants, native number formatting, encoding, markers, text dimensions, icon references, register preservation and generator drift. The native fixture checks all twelve grands, all fifty-two completed subdoctrines, every grand's immediate penalty, switch cleanup, removal of legacy ideas, historical RPV availability and recognition of both equipment models. It also submits both models to native production-line creation.

These checks do not certify competitive multiplayer balance, multiplayer synchronisation, an actual pre-change save load, DLC-disabled behaviour or every live UI state. Engine warnings outside the feature are retained in full, rather than represented as a clean whole-mod error log. The attempted hidden-window capture was unreliable and activation timed out; no mouse click or text entry was sent. `tools/air_doctrine_implementation_1970/ui_inspection.json` records that boundary. See the current result record for the final run's status.
