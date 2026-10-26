# Native1970 country selection and starting identities

The historical incumbent, engine outlook, MD party subtype, party support and historical cosmetic now live directly in each country's dated1970 history. Their display does not depend on an on-start repair event. Only the `IMP_1970_historical_politics` runtime flag is scenario-guarded, because earlier history is also read when selecting a later bookmark.

This repair reuses existing authored leaders, portraits, election dates and expiry dates. It creates no countries, transfers no states and changes no deferred military setup or focus reward.

## Coverage and preserved content

| Inventory | Result |
|---|---|
| Country history files inspected |397|
| Tags owning states on1970-01-01|163|
| Existing authored1970 identities |164, including potential Northern Cyprus|
| Identities repaired by this tool |163:162 active tags plus Northern Cyprus|
| UAE identity |Delegated to `tools/uae_1970/politics.py`|
| Dormant/future files without an authored1970 incumbent |233 left untouched|

The machine-readable companion `1970_starting_identity.json` lists all397 files, individual historical providers, native party slots and before/after/later-history signatures. Each original2000 history tail is retained byte-for-byte by this transformation. All nonidentity country initialization, research, labour ideas, relationships and empty OOB assignments remain in place.

The owned snapshots preserve the authored profile's numeric values rather than substituting one general political distribution.162 initialize the native24-slot MD arrays directly. Lebanon is the single bounded exception: its newly supplied clear/resize/support/coalition leaves are guarded by the1970 scenario inside history, because its native2000 block has no political array reset. Its already authored direct incumbent, broad politics, popularities and ruling subtype remain available for country selection. Gulf character-based incumbents are recruited before `set_politics`, then promoted after their party input exists. Fresh unmarked inputs are tested in addition to already-installed markers.

## Bounded startup protections

The native Gulf government-change cleanup dropped authored historical cosmetics while assigning `dynamic_flag`. Its additional exclusion now requires the1970 scenario, the exact original country, the exact historical cosmetic and its engine government: Saudi Arabia's `SAU_KSA_1985` under Salafist government, Muscat's `OMA_MUSCAT_1970` under Nationalist government and Jordan's `JOR_AUTH` under the corrected Western government. UAE retains its separately owned pre-federation exclusion. This is not a permanent exemption for every government of these countries.

Initial UK subject creation is enclosed by the temporary global flag `COLDWAR_1970_initial_treaty_setup`, cleared immediately after the existing five-subject setup. The matching exemption for Bahrain, Qatar, Brunei and Tonga requires this flag, the1970 scenario, a nondynamic original country, actual subjection to the UK and the UK as the intended overlord. UAE's existing treaty-specific exemption remains separate. Ordinary later puppeting still uses MD's original political matcher.

Only four promoted historical cosmetics lack a native later restoration: `DDR_DDR`, `SAM_WESTERN_SAMOA_1970`, `SVN_REPUBLIC_1970` and `SYE_SOUTH_YEMEN_1970`. Their own country histories now include a marked1999-12-31 compatibility boundary before the unchanged native2000 block. It drops only that unchanged historical cosmetic and only outside the1970 scenario. The boundary is a setup safeguard, not a claimed renaming date, an independence action or a running-campaign event. Samoa therefore keeps Western Samoa in the1970 preview and its native default name in a2000 start.

## Explicit Western dynasty corrections

`native_monarchy_alignment.json` is the keyed correction source. It does not infer a political family from the existence of a monarch.

| Country |Native/history basis|Result|
|---|---|---|
|Bahrain|Main MD2000 Bahrain uses slot0 and `Western_Autocracy` for its ruling house.|Existing Al Khalifa incumbents and approved dynastic successors move23→0.|
|Jordan|Main MD2000 Jordan uses slot0 and `Western_Autocracy`.|Existing Hashemite monarchs move23→0; existing court officials remain in their authored slots.|
|Kuwait|Main MD2000 Kuwait uses slot0 and `Western_Autocracy`.|Existing Al Sabah incumbents and approved dynastic successors move23→0.|
|Iran|An explicitly historical1970 adaptation, supported by the1969 US diplomatic assessment of the Shah's control and Iran's Western security orientation.|Only the existing Pahlavi dynasty party and Mohammad Reza Pahlavi move23→0.|

The Iran classification is an inference from historical evidence mapped onto an existing MD family. It is not presented as a native2000 Shah template. The source is [FRUS, January30,1969, document2](https://history.state.gov/historicaldocuments/frus1969-76ve04/d2). The Shah's authored history expiry remains1979-02-11. Revolutionary alternatives, their native counters and Iran's modern fallback are preserved.

For these four starting distributions, the existing slot0 and23 support is exchanged:0.05 and0.54 become0.54 and0.05. The corresponding broad Western and Nationalist outlooks become61 and11. Every other party value and outlook is unchanged; no additional support is created. Sovereigns retain the native `king` trait and Western ideology trait. Named court officials do not automatically receive `king`.

Party catalogues, native presentation branches, English descriptions/icons, character roles, historical leader pools, counter synchronization, native setter routing and sole-candidate retirement checks are updated together. Unapproved portraits remain excluded. The pool adapter preserves each native modern setter fallback and unrelated country pools.

Saudi Kingdom10 remains intact. Oman, Qatar, Brunei, Morocco and constitutional monarchies are not indiscriminately moved to Western0; their differing existing assignments and elected governments are retained. UAE's approved dynasty programmes and ruler lifecycle remain owned by its national compiler.

## Canonical tools and verification

- `tools/historical_politics_1970/starting_identity.py`: native history transformation, guarded historical flag, recruitment order, cosmetic compatibility and callback markers.
- `native_monarchy_alignment.json` and `monarchy_alignment.py`: narrowly keyed catalogue corrections, applied by both `build.load_catalog` and `curate.py`.
- `apply_monarchy_alignment.py`: bounded history/data/presentation/profile/character migration; preserves existing script BOM and uniform line endings.
- `monarchy_runtime.py`: selected native pool/counter/setter/retirement regeneration, without a broad runtime build.

The repair can be reviewed with `starting_identity.py --history`; installing its own history outputs uses `--history --install`. `apply_monarchy_alignment.py --install` applies the corresponding selected presentation/provider leaves. `monarchy_runtime.build(load_catalog())` returns the bounded runtime output dictionary. Shared callback/profile writes must be coordinated with the UAE compiler, which reads the latest files and preserves these markers.

Verification completed on the emitted source:

| Check |Result|
|---|---|
|`test_starting_identity.py`|3045 checks; all active tags covered, direct incumbents, party arrays, portraits, later tails, scenario-false flag execution, fresh-input recruitment and all four modern cosmetic safeguards.|
|`test_lebanon_identity.py`|34 checks; fresh and migrated array guard, identical1970 distribution, preserved direct preview, absent new arrays in modern history, unchanged existing-array sentinels and all five actual native fallback limits.|
|`test_monarchy_alignment.py`|154 checks; numeric conservation, catalogue/provider/character consistency, party display at1970/1990/1999 and reproducible bounded outputs.|
|`test_monarchy_runtime.py`|43 checks; native counters, protection rollback, fallback, preserved alternatives, modern setter preservation and regeneration.|
|`tools/gulf_1970/validate.py`|103 checks after replacing obsolete UAE assumptions.|
|`tools/gulf_1970/validate_region_starters.py`|403 checks after replacing obsolete UAE assumptions.|

These are source and AST checks, not a claim of a fresh HOI4 playthrough. The selection screen and runtime portraits/names still require an engine confirmation. Lebanon's preexisting2000 history has no complete modern political seed. Its native tail and existing fallback behavior are preserved: the additional1970 arrays do not execute in a modern start, while its preexisting raw preview fields remain unchanged. No modern ruler or government is invented.
