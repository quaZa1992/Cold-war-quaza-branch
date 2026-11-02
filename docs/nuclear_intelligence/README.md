# IMPERIA COLD WAR — Nuclear intelligence

Implemented for the shared nuclear system in all bookmarks. Every country keeps its own confidential assessment. Reports are informational country events; there are no automatic public announcements, sanctions, treasury charges, wars or ally-wide disclosures.

## Monthly chances

| Observer | Enrichment expansion | Bomb/warhead research |
| --- | ---: | ---: |
| Neighbour | 15% | 10% |
| Named or MD great power | 25% | 20% |
| Network 50–69% | 30% | 25% |
| Network 70–89% | 40% | 40% |
| Network 90–100% | 55% | 55% |

Named powers are USA, SOV, ENG, FRA and CHI. `great_power` and `super_power` extend the list; temporary wartime `is_major` does not. Only the highest category applies. Distant agency countries need at least 50% network strength in the programme country. A neighbour or great power does not need an agency for diplomatic/industrial reporting.

One observer/programme pair gets at most one roll per monthly sweep. Unresolved military work takes priority over enrichment. The first successful roll gives a moderate-confidence report; a later independent monthly success corroborates it. Enrichment and weapons assessments are separate. A weapons report never certifies a usable device or arsenal.

Medium defence multiplies enrichment chances by 0.85 and weapons chances by 0.8. Strong defence uses 0.75 and 0.6. National modifier thresholds are 1.25 and 2.5 `intelligence_agency_defense`. Completed passive-defence levels 2–3 also qualify as medium, level 4 as strong. Only completed upgrades count; the existing automation's queued-upgrade array is deliberately ignored. Full passive defence in an older save is recognised through the native completed-upgrade trigger. Partial upgrades completed before installing this feature are not reconstructible from that trigger and are recognised when the next passive-defence level completes, or when the native aggregate already reaches a threshold.

## Construction and lifecycle

No new build menu or decision is required. A native engine probe established that `free_building_slots` ignores queued levels, while `can_construct_building` rejects a second queued enrichment level. For this building's one-level, non-shared state slot, an empty unlocked slot with free capacity that fails the native construction check identifies a queued build. This is evaluated only in owned, controlled states of relevant nuclear countries, monthly.

New queues open an expansion revision. Completion refreshes a 180-day trace without opening a duplicate revision. Ordinary completion outside the queue detector is caught as a raw-level increase. The initial civil project's granted plant explicitly records a receipt and its state baseline. Existing history is baselined at startup; damage and repair use unchanged raw levels, and ownership changes baseline inherited infrastructure instead of announcing new construction. A cancelled queue keeps its already-created 180-day trace. Once the trace expires, existing capacity remains discoverable at one-quarter of the expansion rate.

Live military research refreshes a 365-day trace. Completion is hooked directly into both projects. After research stops, the trace has half the research rate; after that, the permanent research record retains one-quarter rates. Existing saves with completed nuclear projects acquire a research record on the first monthly sweep. Public nuclear status suppresses redundant weapons reports.

A new expansion resets only that revision's two-step assessment. Permanent knowledge of an enrichment capability remains. Corroboration allows the observing country to see concealed enrichment raid targets. Public nuclear powers remain valid raid targets. The native human-only raid guards remain intact. Nuclear AI threat assessment now requires its own weapons-intelligence flag before treating a secret foreign project as a proliferation threat.

## Performance

- One global candidate-cache rebuild per monthly pulse, guarded by a one-day global flag.
- The cache contains existing great powers and countries with agencies.
- Only relevant nuclear countries inspect their own controlled states, once monthly; no added daily/weekly checks or global state sweeps.
- Observers in the cache are checked once per programme; neighbours absent from the cache are processed separately.
- Known assessments skip random rolls. A 20-day per-pair receipt prevents duplicate calls during one monthly pulse.
- Sparse targeted variables/flags hold pair knowledge. There is no country-by-country matrix or daily report queue.

For P relevant programmes, A cached agency/power countries and S owned states in those programmes, work is approximately O(countries + P*A + S + neighbours) per month. This is a structural bound, not a measured FPS or multiplayer benchmark.

## Events and art

| ID | Report | Artwork |
| --- | --- | --- |
| COLDWAR_NI.1 | Nuclear Fuel Activity in [country] | Colourised historical industrial construction photograph |
| COLDWAR_NI.2 | Enrichment Activity Corroborated | Same colourised construction photograph |
| COLDWAR_NI.3 | Possible Nuclear Weapons Programme | Colourised historical research laboratory photograph |
| COLDWAR_NI.4 | Nuclear Weapons Development Corroborated | Same colourised laboratory photograph |

Existing quiet capacity uses alternate enrichment descriptions instead of claiming a current expansion. The artwork consists of locally saved colourised derivatives of the base game's `report_event_generic_construction_site.dds` and `report_event_generic_research_lab.dds`. Built-in Imagegen performed the colourisation; the full prompts and source register are in `art/colorisation.json`, with selected PNG masters alongside. The source photographs remain available in the base game. Colours are plausible reconstructions, not documented original colours.

`python tools/nuclear_intelligence/export_color_art.py` packages the colour masters as uncompressed RGBA DDS at the native 210x176 and 209x176 sizes and preserves the source alpha masks exactly. The two local sprites reference these DDS files. `python tools/nuclear_intelligence/preview.py` refreshes the gallery from the actual exported art and production localisation. No explosion or modern centrifuge photograph is used to illustrate an unconfirmed programme.

`preview/events.html` and `preview/events.png` show the production English localisation with Iran as an example source. They are layout previews, not native game screenshots.

## Historical basis

The probabilities and defence thresholds are gameplay choices, not historical measured detection rates.

- [US Embassy Islamabad telegram, 19 December 1978](https://nsarchive.gwu.edu/document/24463-u-s-embassy-pakistan-telegram-12497-state-department-discussion-french-official): observations and photographs of the Kahuta construction site circulated among French, Australian and US diplomats. Supports construction-stage discovery outside a deep spy network.
- [Rusk memorandum to Kennedy, 30 January 1961](https://history.state.gov/historicaldocuments/frus1961-63v17/d5): reports of Dimona construction prompted inquiries, proposed visits and continuing intelligence observation. Supports a persistent dossier and the separation of facility discovery from proven weapons intent.
- [AEC intelligence assessment, 9 December 1960](https://nsarchive.gwu.edu/document/32660-document-3-atomic-energy-commission-aec-intelligence-report-israeli-reactor-site): competing interpretations of the reactor complex and uncertainty over its purpose support qualified, confidence-based event wording.

## Validation

Run `python tools/nuclear_intelligence/test_runtime.py` for the feature's emitted-script tests, and `python tools/quaza_nuclear_integration/test_integration.py` for the uranium, costs, project, raid and encoding regression suite.

`python tools/nuclear_intelligence/probe.py` creates an isolated, task-owned game profile and loads the current mod. It checks real native defence arithmetic, live construction detection, observer-cache reuse, report source scoping, private pair variables and the monthly sweep. It writes `native_probe.json`. The normal launcher playset and player saves are untouched. The probe terminates its own game process after the checkpoints finish. It is not a long-running campaign or multiplayer test.

Current verification: **18 feature tests and 21 uranium integration tests passed**. The native 1970 probe passed all seven required checkpoints, all four report-source checks and the private-knowledge check, with no errors attributed to this feature. Its process exit code of 1 records intentional termination after completion, not a failed checkpoint. Unrelated existing mod errors remain outside this report. Agency creation was unavailable in the isolated profile, so the native probe directly exercised national modifiers and the completed-level input; the four actual upgrade completion hooks are covered by the emitted-script tests.
