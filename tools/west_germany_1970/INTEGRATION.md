<!-- IMPERIA CW — Cold War: selective quaZa West German content import. -->

# West Germany import

Source: [quaZa's Cold War branch](https://github.com/quaZa1992/Cold-war-quaza-branch), commit `e45483ffc603835c8f44db1e2f9975cbc13fba85`.
The exact 18 dedicated runtime/localisation paths and focus differences are listed in `import_report.json`.

The 417 source focuses retain their IDs, coordinates, relative anchors, costs, prerequisite groups, mutual exclusions, bypasses and icons. Shared country routing, startup hooks, art assets and currency registration are installed separately. This source package never writes the shared historical-currency sprite registry.

## Existing parties remain authoritative

The import does not install source party names, localisations, party icons, popularity arrays, historical identity, coalition or registry entries. The existing `tools/party_registry_1970/data/GER.json` remains unchanged; its recorded pre-import SHA-256 is in the import report.

The incoming FDP references are adapted from source slot 16 to the current native FDP slot 2. CDU 1, SPD 3, DKP 4 and NPD 21 keep their matching existing slots. Source PDS 5, Greens 17, REP 20 and DVU 22 do **not** exist in the current roster: those slots currently represent SDS, Deutscher Naturschutzring, Bund der Vertriebenen and Bundeswehr. Their source-specific party popularity rewards are omitted, and no imported leader or coalition formation is applied to these unrelated organisations.

`roster.py` reads the existing registry at compilation and emits meaningful English party-existence requirements. The Greens parliamentary entry and red-green formation entry are unavailable while that party is absent. Green-government requirements on `red_green_federal`, `eco_tax`, `atomkonsens`, `bielefeld_congress`, and the Green alternatives in `no_deployment`, `emergency_laws_review`, `three_percent` and the abortion-law event are guarded as one conjunction. An unavailable Green alternative does not block a valid SPD/FDP alternative. Source founding events `COLDWAR_GER.93` (Greens) and `.94` (REP) are gated rather than renaming existing parties. PDS/REP/DVU rewards never go to an unrelated current slot. All availability deltas are listed in the report.

The imported `setup_politics` and `assert_1969_coalition` helpers are intentionally inert compatibility IDs. Initialization and queued intro/repair paths cannot reset the native parties. Parliamentary calculations use a private 24-slot cache: the last native election result if available, otherwise current native party shares. They never rewrite the native arrays or coalition. Unhandled ruling-party slots use the existing native `set_leader_GER` provider. DDR initialization adds bilateral simulation state without resetting existing DDR politics or leadership.

## Migration compatibility

The already approved Overseas Labour Ministry remains authoritative for guest workers: real state population, recipient consent, payment, receiving-country cooldown, permanent resident costs, origin ledgers, returns and the $3 billion weekly remittance cap.

The incoming recruitment focuses activate the existing human receiving programme and prepare its normal partner list. They grant no automatic population, military manpower, population growth, private sender income or second diaspora stock. Source preliminary international agreements remain political understandings; each actual recruitment transfer requires a normal Ministry agreement. Recruitment-stop policies suspend native recruitment; reopening policies clear that suspension. No new monthly all-country remittance loop is installed; the legacy helper and dynamic modifiers remain inert compatibility identifiers.

The deportation decree and return-premium focus direct the player to community return management. No military manpower or population disappears merely from choosing the focus/decree. Existing residents and their native public-service costs continue until the normal authorised return is completed. Source thematic political, diplomatic and economic rewards are otherwise retained.

German resettlers from the GDR use bounded state-to-state population transactions rather than military manpower. Source monthly quantities of 600/1,500/3,000/6,000, open-border 30,000, exit-wave option 15,000 and exodus option 20,000 are preserved. Both a controlled origin state with sufficient population and a controlled destination are validated before either mutation. A positive origin military-reserve artefact is compensated; the transaction does not grant military manpower, guest-worker diaspora stock or the native delayed-refugee integration pool, which would otherwise duplicate population later. The private arrival counter advances only on a completed transfer. The Exodus acceptance charges its original 0.1% GDP reception cost and applies its unity/exit-pressure consequences only after the 20,000-person transaction succeeds; queued requests with missing or occupied states have no reception charge or arrival rewards.

All incoming `COLDWAR_DDR.N` events and references are namespaced `COLDWAR_GER_DDR.N` to avoid the existing authored DDR chain. Existing `COLDWAR_DDR_1970` focus/effect IDs are unchanged.

## Regeneration and verification

`python tools/west_germany_1970/compile.py <output>` defaults to the 18 dedicated text outputs only. Use a staging output and compare before copying. `--assets` explicitly enables the package's optional art generation; neither mode overwrites the shared historical-currency registry. `integration/apply.py` has no politics-reset injection and writes native script files without BOM; it fails on changed shared-file anchors rather than guessing.

Checks completed after integration:

- Strict native script parsing and static references: 417 focuses, 360 events, 64 ideas and 4,396 English keys, zero errors or warnings.
- 1,093 executable regression assertions, including all seven population-transfer quantities, missing/occupied/insufficient states, population conservation, military-reserve compensation, registry preservation and uniqueness against all live event IDs.
- Independent review of all 17 focus-availability differences and reward differences: only party compatibility, the namespace fix and guest-worker bridges differ from source.
- A second scripts-only build reproduces all 18 installed outputs byte-for-byte; custom headers and script/localisation BOM rules pass.

A new-game HOI4 runtime/UI smoke test remains necessary; static checks and the script harness do not exercise the engine renderer or multiplayer scheduling.
