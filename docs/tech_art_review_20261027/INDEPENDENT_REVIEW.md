# IMPERIA COLD WAR — Independent technology and focus-art review

## Scope and result

Read-only source review of the installed DPRK, South Korea, and Japan reward changes, their actual Millennium Dawn building unlock providers, the emitted focus/decision guards, and the assigned focus artwork. The reward gates align with the active `enable_building` providers in the inspected sources. I found one clear art mismatch in the assignment map: `COLDWAR_NKO_chondo_cooperative_irrigation` is assigned the hydroelectric dam image although its text and asset reward are agricultural irrigation. No other unambiguous mismatch remained in the reviewed assignments. The parent was informed and is correcting that mapping.

## Construction unlock semantics

`common/technologies/engineering.txt` encodes microchip capacity directly as `enable_building = { building = microchip_plant level = 1/2/3 }` on `microchip_production_1/2/3` (around lines 1323, 1638, 1674). Each `level` is the state building-level ceiling enabled by that technology. The levels are sequentially researched along the microchip technology path; the gate uses the highest researched enabled tier available to the recipient. The values are therefore cumulative capacity ceilings, not separate one-off building grants.

The common helper in `tools/reward_rework_20261027/building_technology.py:18-58` reads all active technology files for nine special building types, then emits a recipient technology check together with a state-level headroom check. The latter compares the existing state level with `enabled maximum - awarded levels + 1`, so the full award must fit beneath the actual researched ceiling. It intentionally returns no extra condition for ordinary building types. I found no project source support for a generic `max_building_level` trigger/modifier; the inspected implementation uses the documented/current `building_level@<type>` state dynamic value, and the MD technology records are the authoritative unlock provider.

Japan's `COLDWAR_JAP_1970_microelectronics_capacity` grants two plants. Its visible requirement asks for `microchip_production_2` or `_3`; its state predicate allows tier 2 only when current plant level is below 1, or tier 3 when below 2 (`common/national_focus/COLDWAR_JAP_1970_focus.txt:5730-5764`). This is the correct amount-aware condition: two plants fit at 0 under tier 2, and at 0 or 1 under tier 3. Requiring tier 3 in all cases would be stricter than the native cap requires. The execution helper has the same restriction (`common/scripted_effects/COLDWAR_JAP_1970_national_economy.txt:2565-2579`), while the focus still exposes the prospective reward in its `effect_tooltip`.

Japan's one-level rail-terminal awards use the recipient's researched rail-terminal ceiling and current state level. Japan's foreign-project decisions also check technology on the recipient (`ROOT`) and state capacity on the selected recipient state in both availability and transaction paths (`tools/japan_1970/build_diplomatic_runtime.py:50-80`; emitted decisions in `common/decisions/COLDWAR_JAP70_foreign_project_decisions.txt`). This matches the recipient-approved construction model.

The Korea runtime builder applies the common technology/state guard in both eligibility and execution. The emitted gates include synthetic-refinery capacity for heavy chemical works, `radar` for the six-level radar station award, and `air_defense` or the appropriate SAM technology for anti-air capacity (`tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime.py:177`; `common/scripted_triggers/COLDWAR_KOR_1970_focus.txt:4250, 4950, 4980`).

The North Korea compiler and agreement candidate-site checks use the same technology/state capacity predicate for special building rewards (`tools/north_korea_1970/compile.py`, `tools/north_korea_1970/agreements.py`). Ownership and control are separately checked at the selected NKO state. The locked reward remains present in the preview tooltip; the technology/capacity gate protects eligibility and execution, not prospective presentation.

Across the affected-country reward sources, the active special types requiring technology are `microchip_plant`, `nuclear_reactor`, `renewable_energy_infra`, `fuel_silo`, `synthetic_refinery`, `internet_station`, `rail_terminal`, `anti_air_building`, and `radar_station`. `fossil_powerplant` has no active `enable_building` provider in the inspected MD technology files; matching technology occurrences concern production modifiers. It should not receive an invented technology gate. No other missing gate or preview-removal issue was found in the reviewed emitted sources. These are static source conclusions; they do not establish engine tooltip rendering or live campaign scope evaluation.

## Artwork review

The candidate contact sheet at `docs/tech_art_review_20261027/ICON_CANDIDATES.png` was inspected against the theme images and focus titles. The one clear issue in `tools/reward_rework_20261027/focus_art.json:139` is:

- `COLDWAR_NKO_chondo_cooperative_irrigation` → `hydroelectric`: the focus title and description concern shared irrigation, and its reward builds an `agriculture_district` (`common/national_focus/COLDWAR_NKO_1970_focus.txt:7085-7113`). The `FocusHydroelectricDams.dds` motif depicts power dams, so the `agriculture` theme is a closer match.

The remaining assignments inspected have direct or reasonable title-to-motif matches, including Korea's cooperative industry → industry, Japan's article 9 → constitution/parliament, Japan's rail/electricity/nuclear/electronics lines, and North Korea's hydro-power and electric-grid focuses. `COLDWAR_NKO_electric_traction` → electric grid and Japan's communications grid → microelectronics are broad rather than exact motifs, but are not clear errors from the supplied art. Asset provenance and attribution are not independently re-audited here.

## Limits

This review read source and the supplied candidate sheet only. No generator was run, no gameplay files were edited, and no claim is made about native campaign behavior or final runtime hashes. Parent's separate native test and any subsequent art-only update remain distinct evidence.


## Integration resolution and evidence boundary

The irrigation image is corrected to agriculture. Thirteen additional South Korean assignments replace generic industry images for technical education, research, social bargaining, housing, finance and energy; the root inspected their refreshed emitted-coordinate view. The current total is 159 focuses. The earlier wording about native accumulation is a source inference: the implementation explicitly enforces a researched technology's declared level, while the installed native documentation does not independently define accumulation semantics. The radar technology enables six levels; the reviewed Korean focus grants one level. Native test outcomes are recorded separately in ENGINE_REPORT.json.
