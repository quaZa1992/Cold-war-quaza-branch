IMPERIA COLD WAR

# Korea and Japan: technology requirements and focus artwork

User-requested follow-up to the reward revision, 27 October 2026. This revision adds real construction-technology requirements and more suitable Cold War focus artwork. Reward amounts, programme costs, parties, leaders, focus IDs, coordinates, prerequisite groups and exclusions are preserved.

## Technology requirements

Seventeen domestic focuses and three Japanese recipient-selected projects now check the relevant researched capability before construction. The same conditions protect availability and the complete paid transaction, including its receipt. Missing technology cannot consume money, grant part of a package or mark it paid. Locked focuses retain their full prospective native Effects.

The common generator reads the installed MD `enable_building` entries for nine specialised types: microchip plants, reactors, renewable infrastructure, fuel silos, synthetic refineries, communications stations, rail terminals, air defence and radar. It checks the country receiving the building and enough room for the whole award under a researched technology's declared level. Ordinary factories and fossil power plants receive no invented research prerequisite.

Japan's microelectronics investment grants two plant levels. The former tier-1 requirement did not cover that package. It now requires either:

- `microchip_production_2`, with no existing plant in the target state; or
- `microchip_production_3`, with at most one existing plant in that state.

These are the three active microchip unlock tiers in the current technology files. A larger generic building `state_max` does not waive this programme requirement. This explicitly enforced policy follows the declared technology levels; the native documentation does not independently specify the accumulation semantics of `enable_building`.

Other examples include `reactor1` for reactors, `fuel_silos` for renewable infrastructure and fuel storage, `radar` for radar stations, and the actual DLC-compatible air-defence/SAM technologies. A Japanese-financed foreign rail project checks the recipient's rail technology and selected state's existing level. Japan's technology cannot substitute for the recipient's capability. Offers remain inspectable and recipients retain their actual decision and site selection.

## Focus artwork

159 focus assignments use 30 visually inspected themes from `gfx/interface/goals/coldwar`: 50 DPRK, 55 South Korean and 54 Japanese focuses. Examples include steelmaking, electronics, railways, agriculture, research funding, technical education, shipyards and nuclear engineering. Bespoke party/leader imagery outside the explicit assignments is retained. The independent review's irrigation/dam mismatch has been corrected to agricultural artwork.

`focus_art.json` is the explicit per-focus catalogue. The three country writers read it, and the ordered installer emits a shared sprite file with native animated shine companions. Existing binary artwork is unchanged. National-spirit artwork is unaffected.

Current emitted-coordinate views, using native artwork, titlebars and bitmap glyphs:

- [DPRK industrial choices](NKO_industry_icons.png)
- [South Korean industry](KOR_industry_icons.png)
- [Japanese technology](JAP_technology_icons.png)
- [Japanese energy](JAP_energy_icons.png)

These are source-derived previews. Connector routing and title wrapping approximate the engine; they are not game screenshots.

## Final verification

All 37 targeted native assertions pass, including the missing-tech fixture, tier-1 rejection without charges/assets/receipt, tier-2 eligibility from zero, researched-tier headroom, actual paid construction, replay protection and Japanese party deactivation/restoration. No relevant country/probe or selected-art diagnostic was found. All 117 tested runtime files reproduce byte for byte through the complete ordered generator run. The tracked-source whitespace check passes.

## Reproduction and evidence

Install through `python -B tools/reward_rework_20261027/apply.py`. Private staged files and backups stay on E:. Then run `check_tech_art.py` in that directory for emitted-source, reference, encoding, graph, technology/transaction closure and sprite checks. `render_art_review.py` refreshes the views. `tech_art_probe.py` runs the isolated native fixture and writes this dossier's engine evidence without overwriting the previous reward revision's native report.

- `SOURCE_CHECKS.json` and `VALIDATION.json`: all 1,085 focus graphs and durations unchanged; registered native/custom APIs and live equipment/research providers checked.
- `TECH_ART_CHECKS.json`: actual availability and paid-helper trigger closure for the 17 specialised building focuses, recipient-site checks for three projects, all 159 art assignments and sprite/shine texture references.
- Country validators: NKO's 1,185 modeled transaction/lifecycle cases; KOR's installed 300-focus runtime checks; JAP's installed 425-helper, 39-script and native-presentation consistency checks.
- `PRESERVATION.json`: ten shared/history integration files unchanged.
- `ENGINE_REPORT.json`: final native result and exact input hashes. `ENGINE_ATTEMPT_1.json` retains the first launch crash before any assertion ran. `ENGINE_ATTEMPT_2.json` records a test-fixture error: native `set_technology = 0` did not revoke the researched starting technology. The corrected private profile withholds those initial Japanese tech entries, then researches tiers during the probe. Live country history is unchanged. Neither attempt is classified as a final successful test or assigned an unsupported crash cause.
- `REBUILD.json` and `FINAL_CHECKS.json`: final regeneration, whitespace and evidence summary.

Native assertions remain a targeted single-client fixture. They do not establish manual hover readability, full-campaign balance, save/rehost or multiplayer/OOS behavior. No commit or push is part of this revision.

## Provenance

The country baseline derives from the previously reviewed quaZa integration, pinned at `7bef99f058f5796788feb839c617407171141c1d`. Artwork is reused from the existing project Cold War folder; the original individual authors, separate source and redistribution permission remain unknown where not documented by existing notices. No ownership claim is made. `ICON_CANDIDATES.json`, the additional contact sheet and the explicit catalogue record the selected source paths and visual inspection. Native MD/HOI4 frames, bitmap fonts and shader assets retain their upstream rights. See `IMPERIA_COLD_WAR_NOTICE.md`.
