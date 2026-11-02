IMPERIA COLD WAR

# Strong doctrine trade offs

Revision authorised by the user on 28 October 2026: stronger and more varied drawbacks for the strongest land-doctrine packages. Twelve concepts are revised: six expansion choices and six existing choices. Positive rewards, mastery progression, XP costs, icons, access and the remaining choices are preserved. The initial concept remains unchanged as the original approved design record; this revision supersedes its affected penalty values.

## Fully mastered penalties

These are contributions from the specified choice after all its own rewards. Country, unit and terrain scopes remain separate. Other independently selected doctrines can compensate at an opportunity cost; the same doctrine's mastery no longer removes its listed weakness.

| Choice | Persistent penalties after full mastery | Intended tactical cost |
| --- | --- | --- |
| Deliberate Firepower | Planning speed -10%; supply consumption +12%; army speed -5% | Assembling ammunition and registered fire plans takes time. An improvised offensive is harder. Previously its final planning speed was +10%. |
| Mobile Raiding Warfare | Out-of-supply penalties +15%; maximum planning -10%; army defence -5% | Short raids retain their supply grace, but remaining beyond the carried reserve is dangerous. No supplies are secretly removed. |
| Heliborne Reaction Forces | Army fuel consumption +15%; equipment upkeep +5%; Air Assault Infantry fort-attack modifier -15 percentage points | Small helicopter-borne groups have limited heavy assault support for frontal attacks on prepared positions. |
| Key Zone Defence | Organisation loss while moving +15%; attack movement speed -10%; supply consumption +8% | Formations organised around prepared positions lose cohesion when forced to relocate. Their fortified defence remains strong. |
| Guided Anti Armour Integration | AT-company soft-attack modifier -15%; AT-company breakthrough modifier -15%; equipment upkeep +8% | Specialist missile positions sacrifice offensive flexibility and fire against soft targets. The penalties target both AT_company and Mot_AT_company. |
| Counterfire Coordination | Army intel to others +10 modifier points; supply consumption +15%; equipment upkeep +5% | Radar and radio emissions reveal information, while the fire-control network requires sustained supply. No selective enemy counterbattery strike is invented. |
| Battalion Combat Teams | Maximum planning -15%; supply consumption +8% | Numerous self-contained teams duplicate supporting functions and have less capacity for deep preparation. |
| Decentralized Command | Maximum planning -5%; planning decay +5%; training time +10% | Local initiative remains strong, but a single prolonged coordinated plan is harder to sustain. Base penalties include -15% maximum planning and +20% planning decay before its existing rewards. |
| Maskirovka | Initiative -10%; planning speed -10% | Concealment and restricted information delay preparation and local decisions. Its existing +5% initiative reward reduces the initial -15% penalty without cancelling it. |
| Cadre and Reserve System | Organisation -5%; experience loss +5% | Rapid expansion and lower standing cost no longer produce a fully mastered free quality increase. Its existing refresher reward improves the initial penalties from -10% organisation and +15% experience loss. |
| Radio-Electronic Combat | Army intel to others +10 modifier points; equipment upkeep +8% | Active emitters can themselves be detected. Encryption benefits remain, but they are a different mechanic from the army-information exposure modifier. |
| Common Tech Army | Army intel to others +5 modifier points | Common radio procedures remain recognisable. Existing security rewards reduce activation exposure from +15 to +5 rather than changing it into a net concealment bonus. |

The change focuses on combinations with broad rewards or unusually strong specialist effects. Forest Envelopment, Coastal Denial, training schools and the other narrower packages receive no automatic additional penalty. In particular, a small country is not penalised merely for adopting an appropriate specialised method.

## Military basis and abstraction

The historical origins recorded in the original concept still apply. The additional costs represent tactical constraints, not historical measurements of effectiveness. Percentages are balance decisions. No claim is made that real armies suffered exactly these numerical losses.

- **Emissions and deception:** Department of the Army, [FM 100-5 Operations, 1 July 1976, chapters 7 and 9](https://djvu.online/file/nR23FTznxzkg9), describes battlefield preparation for deception, the detectability of emitters and the particular exposure of jammers. This is the period manual mirrored by the linked service. The modifier mapping is an abstraction; it does not simulate a radar automatically receiving a counterbattery strike.
- **Sustainment and operational reach:** the same manual's combat-service-support chapter treats fuel, ammunition and repair as requirements for sustained operations. The [critical archival study of Operation Hooper](https://scientiamilitaria.journals.ac.za/pub/article/download/1095/1100/) records practical limits of South African mobility through intelligence, minefields, equipment and logistics. The new supply-gap penalty is an inference for gameplay rather than a directly measured historical effect.
- **Reserve cohesion:** contemporary CIA assessments distinguish ready and cadre formations and estimate a need for training after mobilisation. [1983 assessment, indexed passage on cadre divisions](https://www.cia.gov/readingroom/docs/1983-08-01a.pdf). The direct document request redirected to the reading-room index during this review; the narrower indexed passage, rather than an invented document quotation or success rate, informed the rationale. The penalty applies to the game's generic reserve organisation, not a claim that every national reserve system was equally ineffective.
- **Heliborne limits:** the [U.S. Defence POW/MIA Accounting Agency's Lam Son 719 history](https://dpaa-mil.sites.crmforce.mil/dpaaFamWebInLamSon) documents the interaction of landing areas, weather, terrain, air defence and support. A weaker prepared-fort assault stat represents the limitations of the chosen light reaction-force method. It is not a new anti-aircraft loss formula.
- **Prepared key zones:** [Austrian defence ministry account of Spannocchi's concept](https://www.bmlv.gv.at/cms/artikel.php?ID=8668) identifies fixed key zones, barriers and prepared positions. Increased reorganisation friction when leaving them is a balance inference.

Source authors and their existing rights remain separate. Only short paraphrases and links are used; no new source imagery is copied. Separate rights for the external texts or media are unknown unless established in their original notices.

## Implementation

`tools/doctrine_expansion_1970/balance_revision.py` owns the explicit revision. The existing generator applies its expansion overrides and bounded patches to the six legacy choices. Legacy patches accept the original or already revised activation value, refuse unexpected competing values and leave each reward block and unrelated doctrine intact. Regeneration and `--check` include these integrations.

`validate.py` retains its initial acceptance matrix and applies an explicit revised end-state matrix. Legacy rewards, positive stats and selection guards are compared with the pre-existing repository source. Descriptions identify the new trade-offs in concise English and are measured against the native description field. All effects remain native numeric modifiers. There are no new recurring script loops, event transactions or workforce penalties.

The initial 214-check and native reports are retained as `validation_initial_20261028.json` and `native_result_initial_20261028.json`. Current validation and the fresh native run are recorded separately in the current report files. The original native snapshot also remains on E:.

## Verification results

- **275 of 275 source checks passed.** Coverage includes revised cumulative values, persistent own-mastery penalties, legacy reward/guard preservation, generator parity, encoding and all changed description-field sizes.
- A separate comparison with the initial native snapshot confirms that all twelve new subdoctrine reward blocks and both six-milestone grand progressions are unchanged. Their sixty rewards and twelve milestones retain the original contents. `balance_preservation.json` records the comparison and every before/after modifier change across the twelve affected choices.
- The corrected native run completed on **2 January 1970 at 15:00**, after 167.6 seconds, in a fresh private profile under `E:/HOI4_Mod_Tools/mdcoldwar/runtime/doctrine_expansion_1970/20261028_184931/`. It reused the immutable `20261028_184133/snapshot` only after verifying that all ten affected runtime-file hashes still matched.
- All **24 mastery slot checks covering 18 distinct subdoctrines** passed, including the twelve expansion options and six revised legacy choices. The actual Territorial Defence conflict guard also passed.
- The native out-of-supply modifier fell by exactly **0.15** when the raiding doctrine was replaced. The old USA fixture's artillery modifier fell from **0.30 to 0.00** when changing doctrines, removing the grand's +20% and Radio-Electronic Combat's +10% together with the old tracks.
- No error-log entries naming any affected doctrine file, fixture or tested ID were found. This does not claim the rest of the mod has no unrelated diagnostics.

The first revised test retained the initial fixture's +0.20 artillery-cleanup expectation despite adding Radio-Electronic Combat to that fixture. Its observed +0.30 removal was correct. That obsolete test expectation was corrected, and the fresh-profile repeat passed. The first result is preserved as `native_result_tradeoff_attempt_1.json`; it was not relabelled as passing or overwritten on E:.

`native_result.json`, `validation.json` and `balance_revision_evidence.json` hold the current compact results. No multiplayer, save/rehost or live-tooltip rendering certification is implied. The tests establish native loading, assignment, mastery, the observed modifier cleanup and source correspondence.
