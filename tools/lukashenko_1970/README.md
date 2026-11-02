IMPERIA COLD WAR: Alexander Lukashenko selection and portrait wardrobe

Implemented for human Belarus (BLR) and Soviet Union (SOV) players in the 1970 scenario. Alexander Lukashenko is visible in the native governing-party selector before 1977, but disabled until 1977.1.1. Selection and execution both check the date and actual governing party. Once available, he has no term or death-date expiry. Other existing candidates retain their undated policy.

The first supplied photo, restored in colour, is his default portrait and candidate icon. The same menu gains free, repeatable `Lukashenko: Young` and `Lukashenko 90s` appearance options while he is the incumbent. The latter is available from 1990.1.1. Appearance is remembered per country through another leader, party changes and reappointment. It is cosmetic: native `set_country_leader_portrait` changes the picture without retiring or recreating the leader, changing traits, or granting programme rewards.

The two native affiliations are communist (slot 4) and Eastern-aligned conservative (slot 6), consistent with the existing Belarusian Lukashenko slot. The Soviet appointment is an alternate-history RP choice, not a claim that he headed the USSR. Belarus reuses its existing Pyotr Masherov as an immediately available alternative. This prevents the old slot-six pool from installing Lukashenko early, for both human and AI countries, without inventing another person. Actual party names still come from MD's native party system.

Historical basis: the [official biographical timeline](https://president.gov.by/en/president/biography) records political-instructor service in 1975-1977 and 1980-1982, early Komsomol/administrative work from 1977, and election to the BSSR Supreme Council in 1990. The [full biography](https://president.gov.by/en/president/biography/full) dates his national political career to 1990. The user selected his first political function in 1977 as the availability basis, at year-level granularity. National parliamentary activity and the 1990s portrait remain associated with 1990. The two photographs are user supplied; their exact original sitting dates are unknown.

Existing native paths, 2000 bookmarks and party identities remain with their original providers. The Soviet catalogue gains one person and two party choices: 53 Soviet figures and 111 USA/Soviet party choices in total. No duplicate character definition, general, military unit, new party, focus or national spirit is created. This pass does not implement a broader Belarusian tree rework.

Integration covers the central dispatcher, Belarusian native setter, legacy Belarusian pool, Soviet selector generator and historical-pool writer. The legacy pool has a real execution guard, so the disabled choice cannot be bypassed through that path. New periodic work is limited to one country-specific monthly Belarus hook. No new daily/weekly pulse, random draw or world scan is introduced. Portrait updates run on explicit appearance changes and appointments.

Validation: 126 focused model cases passed, including visibility before the date, year boundaries, direct execution guards, invalid countries/parties/scenarios, AI legacy fallback, repeat selection, portrait-only changes, party return, unique decision IDs, asset dimensions and byte-idempotent generation. The updated USA/Soviet regression suite passed 1,042 model cases. These are source/model checks; native HOI4 startup, UI, save/reload and live multiplayer were not tested. Native portrait-effect syntax was checked against the installed vanilla `common/national_focus/india_goe.txt` and the mod's `mdcw_gulf_1970_portraits.txt`.

Build and verify:

```text
python -X utf8 tools/lukashenko_1970/build.py
python -X utf8 tools/superpower_1970_leaders/catalogue.py
python -X utf8 tools/superpower_1970_leaders/build.py
python -X utf8 tools/lukashenko_1970/validate.py
python -X utf8 tools/superpower_1970_leaders/validate.py
python -X utf8 tools/lukashenko_1970/document.py
```

Runtime file list: `runtime_files.json`. Checks and source hashes: `VALIDATION.json`. Images and rights: [ASSET_NOTICE.md](ASSET_NOTICE.md) and `ASSET_MANIFEST.json`. The availability year is stored in `config.json`; rebuild both generators after changing it.

![Installed portrait textures](PORTRAIT_REVIEW.png)
