IMPERIA COLD WAR

# Installed generic naval adaptations, 25 October 2026

The requested native generic naval chapter is integrated into the active 1970 USA, Soviet, DDR, Iraqi and Emirati national trees. There are 85 new focuses. Existing country programmes and their strategic exclusions remain available through their original routes.

| Country | New focuses | Installed direct focuses | Adaptation |
| --- | ---: | ---: | --- |
| USA |20|301|Fleet modernisation, undersea warfare, fleet carriers or sea-control ships, shipbuilding and Fleet Marine Force support |
| Soviet Union |20|856|Gorshkov-era construction, undersea forces, helicopter or aircraft-carrying ships, arsenals and naval infantry support |
| DDR |15|836|Volksmarine patrol/escort forces, Baltic yards, communications, repairs and landing support |
| Iraq |15|441|Umm Qasr, Basrah coastal yards, Gulf patrol craft, seamanship and naval support workshops |
| UAE |15|129|Abu Dhabi Sea Wing, coastal patrols, emirate maritime yards and training before federal naval unification |

USA has 300 visible cards because its pre-existing deprecated Gulf contact receipt stays hidden. Soviet direct-focus counts exclude separately registered Union shared focuses. Each new root connects to actual existing country focuses; a native Naval Development shortcut targets the new root. Layout evidence includes both the chapter and existing neighbouring country cards.

## What was copied and changed

The source is the 20-focus descendant closure of `GENERIC_naval_reform` in the installed Millennium Dawn 2.0.2 `common/national_focus/00_generic.txt`, supported HOI 4 version 1.19.*. Relative geometry, native icons, most costs and native reward magnitudes are retained. Country-specific identifiers prevent one country's programme from satisfying another country's receipts.

USA/SOV retain the aircraft-carrier versus helicopter-operator exclusion. The three coastal versions omit submarines, nuclear submarines, submarine expansion and both carrier paths. Their surface research is limited to real patrol-boat/corvette categories, and their drydock/production links are rerouted so no missing predecessor makes the branch impossible. The existing USA naval-priority and Soviet/DDR strategic exclusions are preserved. The new general construction chapter does not pay out a previously excluded old programme.

External generic fighter and military-industry prerequisites are replaced with relevant local naval prerequisites. A 1970 focus grants research coupons rather than a completed 1990 composite factory or progress toward 2010 stealth prototypes. The root's 15% special-project progress becomes one 50% naval-module research coupon; the materials study gives one 50% industry coupon and one 50% naval-engine coupon; the sensor study gives two 50% naval-electronics coupons. No special project or technology is automatically completed. Actual native hull/project technology requirements remain unchanged.

Most focus costs retain donor 10/5/7.1 values. UAE keeps the established user preference of 70 days per focus, including the donor's shorter follow-ups. Native meaningful coastal, yard-count, power-status and selected-doctrine requirements remain. Internal scenario, quotation and replay checks are hidden. Visible construction requirements show actual capacity; funded projects also show treasury against a five-decimal native quotation. UAE retains its existing deficit-finance policy. Search filters preserve donor categories and add NAVY; AI spending has a high-deficit guard on paid construction.

## Rewards and construction

Six native ideas are adapted per country. Their actual modifier payloads match the generic source:

| Programme | Duration | Native payload |
| --- | --- | --- |
| Combined military/maritime suppliers |Permanent|Military-factory productivity+10%, dockyard productivity+10%, military-industry tax modifier+10%, dockyard-income tax modifier+10% |
| Arsenal/equipment conversion |730 days|Equipment conversion+15%, military factory output+15% |
| Merchant shipping |Permanent|Convoy production cost-15% |
| Repair facilities |365 days|Repair speed+25% |
| Vessel production |730 days|Dockyard output+20% |
| Marine/landing/boarding support |Permanent|Navy experience gain+5%, amphibious invasion+15%, marine supply grace+48 hours, marine special-forces contribution factor-5% |

These are distinct native statistics. Economic productivity/tax modifiers are not interchangeable with ship production output. Military factory output and general repair speed have their full native scope, including eligible assets outside the navy. Their descriptions use shared military supply and industrial institutions rather than promise a nonexistent ship-refit modifier. These new ideas add to compatible existing national programmes; existing country bonuses are not replaced or silently capped. There is no second copy of the new programme within one country, and expired timed rewards cannot be refreshed by replaying its completed focus.

USA/SOV port construction costs $0.5 billion, each dockyard $7.5 billion. Their main expansion grants two yards atomically in one eligible state; the later drydock grants one. DDR/IRQ/UAE port construction costs 0.2% of current GDP, a yard 0.8% of GDP, and each yard focus grants one. These are gameplay prices adapted from native costs and country scale, not claimed historical invoices. The donor's free shared arms factory remains free and explicit in its native preview. No new monetary weekly stream is introduced.

Every building level grants one extra same-state shared building slot immediately before construction. The same execution branch checks real owner/controller, province control for ports, native building caps and existing capacity, then charges exactly once. USA/SOV/DDR/IRQ also require full treasury coverage. UAE preserves its separately authorised country-wide deficit policy: only its explicit profile flag removes the affordability veto, while the full invoice is still deducted once even from a negative treasury. Positive GDP and quotation, actual ownership/control, capacity and the MD payment-state guard remain mandatory. A stray opt-in on another tag cannot remove its affordability check.

The first eligible named target receives the complete package. A blocked focus payout stays pending without a charge; the country-specific daily hook retries it against current conditions. Full prospective asset effects remain visible even while blocked, but preview calls execute no rewards. Daily hooks are restricted to the five actual tags, without a recurring global-country search.

Two existing coastal predecessor grants were also repaired: Iraq's coastal dockyard and the Emirati Dubai harbour project. Seven existing preview/execution copies now include the missing slot inside their original transaction/credit guards. Canonical templates are repaired too. Previously completed receipts receive no retrospective free construction. See `PREDECESSOR_SLOT_PROOF.json` for the bounded preservation evidence.

## Historical basis and limits

For the USA, the Navy's own history records Zumwalt's 1970 force-planning priorities and high/low construction debate. This supports selectable carrier/sea-control investment, escort numbers and lifecycle support. A sea-control-ship focus represents a proposed alternative, not an already deployed 1970 vessel. [NHHC, US Navy Capstone Strategies and Concepts 1970-1980](https://www.history.navy.mil/research/library/online-reading-room/title-list-alphabetically/u/us-navy-capstone-strategies-concepts-1970-1980.html), [NHHC, Admiral Elmo R. Zumwalt Jr.](https://www.history.navy.mil/browse-by-topic/people/chiefs-of-naval-operations/admiral-elmo-r--zumwalt-jr-.html).

`SOV_DDR_RESEARCH.md` records the real Gorshkov-era fleet and Warsaw Pact coastal-modernisation context, the actual existing national programmes and exact archival-access limits. `IRQ_UAE_RESEARCH.md` records Iraq's limited coastal role and the Abu Dhabi Sea Wing 1967, Abu Dhabi Navy 1971 and federal UAE Navy 1976 institutional sequence. The UAE root deliberately names the Sea Wing. No modern national navy, foreign operational consent or historical fleet size is invented to fill the generic slots.

Shared supplier productivity, merchant support, repairs and operational training model the institutional advantages of each programme. Their magnitudes remain native donor gameplay values, not historical estimates. Carrier size, yard investment, prerequisites, temporary versus permanent rewards and mutually exclusive carrier choices supply the inherited opportunity costs. This copy does not create a new foreign agreement, war, faction, ship formation or OOB.

## Verification and remaining native checks

`VALIDATION.json` checks actual emitted country trees/runtime against canonical source, 85 IDs, complete prerequisite groups, symmetric exclusions, providers, native 147 pixel title widths, encoding and all new cards against every existing country card. `BUILD_CHECKS.json` and `CHECK_LOG.txt` record scoped rebuild stability and naval asset/lifecycle/emitter tests, 12 USA calendar tests, 18 Gulf-access preservation tests and the existing UAE revision checks. Exact current test counts are recorded from the runner output. The naval tests include funded retries in four countries and full once-only Emirati invoices despite a negative treasury. Existing USA integration validation now expects 301 focuses. Legacy Soviet/DDR validators also recognise the new totals and naval localisation, but their broad output-folder validators were not run against stale generated folders.

`IMPLEMENTATION_MECHANICS_REVIEW.md/.json` independently reviews actual transactions, 30 donor-equivalent idea payloads, quote races, parent/exclusion guards, 15 timed expiries and public/runtime readiness. `INDEPENDENT_FLAVOUR_REVIEW.md/.json` and `DATA_PROSE_AND_HOOK_REVIEW.md/.json` document prose, glyph and image inspection. Pure Soviet/DDR emitter tests preserve all original focus blocks and tree semantics after removing exactly the naval block; ordinary writes are blocked. IRQ/UAE hooks are inspected without executing broad builders over active unrelated work.

Both USA and Iraqi AST formatters discard comments. Their canonical integration therefore formats ordinary country content first, then inserts the marked naval chapter. The Iraqi `code()` path also strips an existing marked chapter before formatting, so an in-memory standalone streamlining pass can retain it without duplicate IDs or lost ownership markers. Its pure writer is tested against the real native formatter without running the broad Iraqi build.

`installed/` contains native-asset source compositions and a five-country overview, not live screenshots. Renderer connector routing is approximate; a few long cross-row links pass behind icons in the compositor. No native engine routing defect was established from that approximation. A live game check should confirm links, locked/unlocked numeric tooltips, correct port/yard placement, changing quotations, save/load after pending completion and timed expiry. A two-client MP rehearsal remains outstanding. No current native game or multiplayer test is claimed.

## Provenance

Original generic script donor SHA-256: `c3f2e55df976b712e423fa906afd18b9e638c838d1cb34a13fb80bfa2ea82ac5`. Source: existing Millennium Dawn team content, Steam Workshop 2777392649, locally installed version 2.0.2. The actual source file is unchanged. Individual generic chapter authors and a separate applicable redistribution licence/permission were not established, so those are explicitly unknown. Existing Millennium Dawn and Paradox Interactive authorship and notices remain applicable; the project marker does not grant third-party rights.

Country adaptation, bounded emitters and source-model evidence are IMPERIA COLD WAR modifications. Existing native sprites, source textures, frames and bitmap fonts are referenced unchanged. No new binary game art was created or edited. Preview transformations and asset-source hashes are recorded in `installed/LAYOUT_EVIDENCE.json`; its companion `NOTICE.md` identifies the local-review compositions and unknown separate permissions. Historical sources are linked original paraphrases; their photographs, scans and prose were not redistributed.
