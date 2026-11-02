IMPERIA COLD WAR

# Brazil 1970 implementation

Installed in the loaded mod on 2 November 2026, following the user's instruction: "Implementiere alles nun ins Spiel. AAA Polish". The approved concept SHA-256 is `0b14031fbad84b84ad72a1599e47cf444a3b52523bcc26070c8f7fd94bc55875`. `approved_design.json` remains byte-identical to the approved concept. `APPROVAL.json` records authorization; `runtime_design.json` and `RUNTIME_CATALOGUE.md` describe the installed translation.

The subsequent Brazil-only polish is recorded in `POLISH.md` and `POLISH_CHECK.json`: 192 English refinements, complete party-formation previews and unchanged approved gameplay. The user owns further image work; no proposed event-photograph replacement was applied.

The authored tree contains 224 focuses in 18 sections: thirteen political programmes and five shared national sections. All 45 mutually exclusive pairs, coordinates, relative anchors, prerequisite groups and eight navigation shortcuts match the approval. Eight starting spirits, eight domestic events, fourteen recipient-approved standing agreements, two funded domestic decisions and the party formation/congress decisions are integrated. New player text is English only.

## Political integration

The January 1970 start retains Emilio Garrastazu Medici and the military ruling slot 22. ARENA is a distinct civilian identity in slot 1. MDB is the legal opposition in slot 2. Programmes cover the Armed Forces, ARENA/PDS, MDB/PMDB, restored historic PTB, later PTB, PDT, PT, PFL, PSDB, PCB, PCdoB, Lacerdists and PRN. The native 24-slot election model remains in use.

Party branches remain visible. Execution checks the actual ruling slot, registered identity and meaningful institutional opening. Registration and congress nomination do not appoint a president. Native elections and actual government changes route the corresponding leader through MD's ideology-group mapper. Genuine party reform permits the approved early alternative organisations; PFL and PSDB also require their real predecessor organisations and split authority. PRN retains its late-1989 formation requirement. Lacerda's posthumous continuation requires explicit successor authorization. Geisel and Figueiredo have dated military succession; other late succession rules are recorded in `politics.py`.

Earned party policy spirits and their appropriations suspend when that identity loses office and return when it governs again. Finite rewards, construction, research and setup charges never replay during reconciliation. Shared national reforms remain earned.

## Economy and cooperation

Prices use each payer's current internal MD `gdp_total`, through native `modify_treasury_effect`. A 0.65% price is `gdp_total * 0.0065`. Zero or negative treasury does not block own state spending. Existing native borrowing is retained. Invalid or zero GDP blocks a paid transaction.

Recurring appropriations use weekly MD units: current annual GDP percentage / 100 / 52. One hook in each native additional-expense/income aggregator adds the streams after the existing inflation adjustment. The native monetary tooltip includes their current totals in millions per week. Every budget literal has at most five fractional digits.

Every bilateral offer originates in its Brazilian focus. The recipient receives distinct Accept and Decline decisions and an agreement notice. Source focuses, recipient decisions and notices preview both countries' complete prospective costs, named spirits and signed modifiers, research, experience, building levels and additional slots. Previewing grants nothing. Failed or declined proposals charge nothing; renewal requires the already-completed source focus.

Both standing spirits require both countries to exist, peace with one another, no native embargo in either direction and none of the four mirrored Imperia sanction classes. Suspension stops both spirits and budget streams; valid conditions restore them without repeating one-time rewards. Dependent offers require their active parent agreement. There is no automatic expiry.

Itaipu includes separate own-GDP appropriations and an additional transfer: Brazil pays 0.08% of its current annual GDP / 52 and Paraguay receives the identical quote. This is RP project financing, not a historical royalty formula or physical electricity pricing. Hydropower and the domestic reactor start construction. Every building level gets one extra shared state slot before construction, including infrastructure and other nonshared buildings. Owner, controller, full-control and native level-cap checks are separate. Shared-slot buildings also pass a post-grant free-capacity check before fees or rewards; failed transactions roll back only their newly added slots.

Uranium feasibility work grants research only. Deposits and paid development remain in the existing Imperia investment system; no raw uranium or free mine is added.

## Native modifier corrections

The first engine run rejected two names that the concept's earlier source audit had incorrectly accepted. The immutable approval is retained, and `native_adjustments.py` records all nine translations at unchanged signed magnitudes:

| Approved concept key | Installed supported key | Actual scope |
| --- | --- | --- |
| `military_spending_cost_multiplier_modifier`, 2 occurrences | `personnel_cost_multiplier_modifier` | Military personnel costs, rather than all military expenditure |
| `inflation_gain_multiplier_modifier`, 7 occurrences | `inflation_cost_multiplier_modifier` | Inflation-related fiscal costs, rather than inflation-rate growth |

The relevant descriptions and installed catalogue use the narrower actual effects. These policies do not directly change the inflation rate. The consumers are MD's personnel-cost calculation and inflation-cost expense multipliers in `00_money_system.txt`. The validator now rejects unregistered and undocumented idea modifier keys, with native building-specific speed modifiers derived from the actual building registry.

## Presentation and sources

The MD Brazil, Russia, Generic and Germany reference measurements are in `docs/brazil_1970_concept/MD_REFERENCE_PROFILE.md`. The approved external renders retain their original proposal context. They are reconstructions, not screenshots of HOI4. `RUNTIME_CATALOGUE.md` supersedes their effect text for the native modifier corrections above.

All 224 focus icon references, 203 idea picture references and 22 event picture references resolve. The initial polish uses 83 distinct native focus symbols, with 87 normal/shine aliases including retained originals; eight starting and eighteen group spirit icons use native artwork. Nine event images preserve the complete existing MD 217 x 163 frame, alpha and 180 x 150 photo inset byte-for-byte. The full donor window and adjacent 300 x 47 option slots were inspected. Shared event GUI is unchanged.

Existing exact portraits are used where available. Unmatched historical people use the explicit neutral 156 x 210 silhouette. Prestes uses the installed Trial of Allegiance portrait only if that DLC is available, with the neutral fallback otherwise. No DLC image is copied. The tree does not require that DLC. Historical faces are not fabricated or replaced with other people's portraits.

Historical precedents and citations are recorded in `docs/brazil_1970_concept/HISTORICAL_RESEARCH.md`, `FINAL_HISTORICAL_REVIEW.md` and the leader reviews. They cover repression and AI-5, the Miracle and inequality, party reorganisation, Embrapa and frontier development, oil and credit vulnerability, Itaipu, regional river consultation, Argentine nuclear confidence, German nuclear cooperation and the other foreign programmes. Historical facts, alternative political outcomes and proposed numerical balance remain distinct. See `NOTICE.md` for attribution and permission limits.

## Verification

The isolated native fixture now contains 117 assertions, including registration preview non-execution checks. `NATIVE_RESULT.json` identifies the final tested run and result; `NATIVE_CHECKPOINTS.txt` records each assertion. Full profiles, logs and earlier runs stay on the user-approved D: drive. The helper intentionally terminates only its own process after completion. Its process exit code is not the fixture result; `native_pass` records the completed assertions and diagnostics.

The fixture checks the real 1970 tree, leader and eight spirits; zero/negative treasury charges and replay prevention; infrastructure and shared-slot factory rewards; native faction-opinion scaling; party registration, government mapping, leader changes and programme suspension/return; recipient consent and both GDP setup charges; weekly budget repricing and identical Itaipu transfers; all eight sanction-array directions; real embargoes from both countries; war, peace and restoration without setup replay. The Paraguay embargo test uses its own recipient event because native `break_embargo` uses ROOT as sender.

Independent emitted-source validation currently reports 9,936 assertions, zero errors. `compile.py --check` verifies deterministic emitted output. `PACKAGE_CHECK.json` checks current package hashes against the native run's frozen runtime scripts and recorded art references. The source validator preserves the exact approved graph and checks helper references, English keys, sprite references, registered modifiers, encoding, once-only guards and paired agreement rules. Independent reviews are `REVIEW_MECHANICS.md`, `LAYOUT_PARTY_REVIEW.md`, `ART_IMPLEMENTATION_REVIEW.md` and the follow-up reviews listed in `POLISH.md`.

The game fixture uses artificial GDP/treasury states in a private fresh start. It does not establish a full 1970-1990 balance campaign, every later succession, save/reload persistence or network multiplayer behavior. Desktop capture reached the isolated game, but a complete native focus scrolling and hover session was not captured. Static native-art branch renders and source-derived previews were reviewed; no live focus-hover screenshot is claimed. Unrelated pre-existing mod diagnostics remain outside this feature's scope.

## Files and rebuilding

`manifest.json` records the emitted scripts, English localisation, bounded shared integrations, installed model and catalogue. `art_manifest.json` and the art notices record the associated assets. `PACKAGE_CHECK.json` includes the art and generator hashes. No archive or native test profile is stored in the mod.

The canonical authoring modules are `core.py`, `diplomacy.py`, `politics.py`, its owned templates, `common.py`, `native_adjustments.py`, `integration.py`, `catalogue.py` and `art.py`. Run `compile.py`, then `validate.py`; use `compile.py --check` for drift checking. Art is built separately by `art.py`. Do not regenerate the archived concept or run another country's generator to rebuild Brazil.

Shared integrations are limited to Brazil's 1970 history/fallback route, the native party-name providers, the real party-change callback, leader dispatch, weekly monetary aggregation and the monetary breakdown localisation. The Brazil leader clause is outside Chile's generator-owned marker region. Script output uses UTF-8 without BOM; English localisation uses UTF-8 with BOM. Existing upstream attribution and other countries' code remain in their files.
