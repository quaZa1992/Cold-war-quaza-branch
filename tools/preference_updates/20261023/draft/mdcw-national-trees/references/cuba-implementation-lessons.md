# IMPERIA COLD WAR: Cuba implementation and event-picture lessons

Use this reference for recipient-approved national focuses, standing agreements, building grants, event pictures, or a continuation of the Cuba tree. These are explicit user preferences and demonstrated failures from the October 2026 Cuba work. Keep Cuba's history and focus limit scoped to Cuba; the current request and live code take precedence over these snapshots.

## Project identity and native presentation

- Begin custom code with `# IMPERIA COLD WAR — <feature>`, using the format's valid comment syntax. Put it on the first line where grammar permits. A required language header, shebang or skill frontmatter keeps its position; place the marker immediately after it. Localisation keeps `l_english:` first and the project comment next. Scripts are UTF-8 without BOM; localisation is UTF-8 with BOM. Update the generator and emitted file together. The old `IMPERIA CW` abbreviation is not the requested marker.
- In a modified upstream MD file, identify the custom integration at the top, preserve upstream credits, and continue marking the actual custom blocks. The marker identifies additions, not ownership of MD code or photographs. Strict JSON uses a project field within its existing schema; binary and rigid data formats use companion provenance rather than invalid inserted text. Do not rewrite an immutable approved snapshot merely to add branding.
- New game text is English. The user rejects en/em dashes in player text and previews. The em dash in the required code comment is not player-facing text. Use native numeric formatters and supported glyphs; a minus sign displaying as `?` is a defect.
- Effects must look "naked": concrete native costs, signed modifiers, named spirits, buildings, slots, research, experience and decision unlocks. Put political context in descriptions and meaningful conditions in requirements. A custom paragraph must not substitute for actual effects.

## Recipient consent and standing agreements

Cuba's choice belongs in separate Cuban national focuses. The RP partner receives the actual acceptance/refusal event or decision; a Cuban offer-selection decision menu does not satisfy this design. Trace the real `country_event` dispatch, tag, pending state and response handler. A pending flag alone does not establish delivery. An unrelated notice with only a review button does not establish a working acceptance flow.

Every offer focus must always expose both countries' complete prospective "If they accept" effects: exact spirit names, every signed modifier, setup and recurring costs, construction with slots, research categories/uses and other rewards. The focus, recipient decision, event option and preview inspector must agree. Those numbers remain visible while locked, excluded, unsigned, refused or suspended. Previewing must execute no transaction.

For the approved standing Cuban deals, both signatures have no expiry. Both spirits require both countries to exist, bilateral peace and no native embargo or Imperia diplomatic, financial, economic or military sanction in either direction. Check both incoming/outgoing and mirrored sanction records. Third-country sanctions do not themselves invalidate this bilateral relationship. Suspend both spirits together, preserve signatures, and restore them when restrictions clear without replaying setup fees, buildings, research or experience. Either signatory can terminate. A missing partner must not leave a clickable termination action that does nothing.

Subsequent member-only or parent-dependent agreements require the actual active membership/parent spirit in availability, execution and recipient acceptance. Include the entry focus of a member-only branch. Keep founding/admission reachable before that branch. Reconciliation suspends dependent paired spirits if their required parent stops and restores them when appropriate. Preserve genuine logical prerequisites: multiple prerequisite blocks are AND, multiple focus entries in one block are OR.

## Buildings, budgets and native execution

- Grant one extra shared state building slot per granted building level, including infrastructure, land forts and coastal forts. Put slots before construction in the same state and same once-only transaction. Province forts do not consume shared slots, but the additional slots are an explicit user requirement, not a reason to omit them.
- Check actual current ownership/control and native building capacity, including the exact province for province buildings. Capacity checks and slot rewards are separate concerns. Derive caps from current MD definitions instead of imposing a remembered universal limit. In the inspected build, both fort types had province cap 7 and the native `any_province_building_level` comparison required `<` or `>`, not `=`.
- Keep recurring monetary costs in weekly MD units. Budget literals have at most five fractional digits. Do not introduce focus Treasury affordability gates by default; retain the approved cost contract and actual native deductions.
- Research preview and execution must use the same source label, category, bonus and uses. Passing no node to a shared helper once mislabeled new bilateral research as the Soviet air-defence reward. Check emitted transactions and localization uniqueness rather than trusting the catalogue.
- Keep earned national assets separate from party-bound programmes. Party departure disables the latter and return restores them without charging or granting assets again. Use the actual native party-in-power predicate; keep every party branch visible and inspectable.

## Event photographs must fit the actual MD frame

The user explicitly requires MD's framed event photographs. An existing/registered sprite is not sufficient. In the inspected MD version, country-event pictures are 217 x 163 RGBA, with a 180 x 150 photo inset at (19, 6). The exact frame reference is main MD `gfx/event_pictures/generic/elections/political_deal.dds`. Re-read the current donor before reuse; these are version-specific measurements.

Broad 397 x 153 or 400 x 150 news images overflowed the country-event slot and could cover answer buttons. A 217 x 163 image with a different old black border also did not satisfy the requested exact frame. Use appropriate already framed art or the existing native asset-packaging workflow. Preserve proportions and original outer frame/alpha pixels, and inspect the resulting DDS. Do not resize the global event window or move its buttons to accommodate one bad image.

Audit the complete `EventWindow` donor and adjacent `event_picture`, `event_pic_clip`, `options_grid`, slot size and option-entry texture, not only the picture coordinates. The inspected picture position was (5, 5) and option grid (215, -1) within the bottom window. Check actual nontransparent bounds against the options and container. Check every visible event, including retained reply events that originally lacked a picture. Topic, date, flag and people must fit the event: a Cuban constitution cover visibly dated 2019 was unsuitable for the Cold War setting.

The Cuba exporter is `tools/cuba_1970/event_art.py`; the independent geometry/pixel check is `validate_event_art.py`. Existing MD photographs are mechanically packaged with FFmpeg and a lossless native DDS container; creative image changes follow the applicable image workflow. Retain asset credits and unknown permissions explicitly. A donor-composed preview is not a live HOI4 screenshot.

## Cuba-specific design boundaries

- Keep religious and party alternatives relevant to the country. Do not invent Salafi/Shia paths for Cuba or another non-Muslim country merely to fill MD outlook slots.
- The approved ceiling is 120 focuses, retaining the 13-focus Fidel programme and credible party alternatives. This is not every country's quota. Merge accounting/review filler when needed while conserving costs, days, rewards, source receipts and intended lifetimes.
- Cayo Blanco del Sur is an independently transferable HOI4 STATE, not a new country. Its state/province identifiers and map colours must be rediscovered from current files. The historical symbolic dedication renames the Cuban island; genuine territorial cession is alternate history and requires the DDR player's consent. The accepted cession must also rename it, retain the Cuban core and avoid automatic bases or a new DDR core.
- The island route is independent beside Soviet assistance. Practical DDR partnerships follow a ratified island agreement and benefit both parties. Do not invent a dependency on Soviet assistance merely to anchor the layout.
- Cuba needs an explicit USA-consented route to ease or remove its actual embargo-burden spirits, including agreed real restrictions and compensation. A focus must not remove US restrictions unilaterally or change Guantánamo ownership as an incidental reward.
- Research localized Guantánamo posts, patrols and coastal readiness before adding defences. Verify map adjacency and ownership: construction belongs on Cuban territory, not the US base. Nationwide territorial mobilization and shelters are distinct later institutions, not evidence of a continuous 1970 fortress belt.
- The user specifically rejected available-workforce penalties for Overseas Forces and medical programmes. Use justified military operating, supply, training, health or education costs instead. Volunteer assistance changes real supported deployment requirements/capacity and does not create free divisions or waive recipient consent.

## Evidence and maintenance

Follow the canonical generator and current approved revision. Declare every `relative_position_id` anchor before its dependent focus; recursive coordinate resolution alone missed an actual HOI4 load error. Keep a stable anchor-first order and detect cycles.

Distinguish code/reference checks, rendered geometry, actual event arrival, native transaction execution, manual hovers, save/load and multiplayer. Native lifecycle tests can preserve their evidential value after a comment-only or picture-only change if the relevant gameplay representation is compared and the presentation change is disclosed. Do not label old raw hashes current or rerun a whole campaign solely to validate a comment. Preserve known-good backups and limit writes to the feature being changed.

Current discovery pointers, not permanent certificates: `tools/cuba_1970/README.md`, `cuba_runtime_design.py`, `foreign_contracts.py`, `EVENT_FRAME_VERIFICATION.json`, `REVISION_IMPLEMENTATION_VERIFICATION.json`, `GUANTANAMO_DDR_RESEARCH.md`, and `tools/cayo_blanco_del_sur/README.md`.
