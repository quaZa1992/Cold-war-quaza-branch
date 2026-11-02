IMPERIA COLD WAR: Jerusalem split integration

Viltsu's source is pinned at `972ca21aba34849ad8543654c11546b6c1aa2d4f` in `Imperia-MD/mdcoldwar`, branch `Split-Jerusalem`. The integration base is `2d08dc687d26b9258921870f81d9107446665da0`. Source credit, changes, findings and evidence are recorded in [the audit](../../docs/audits/jerusalem_split_20261027/REPORT.md).

Run from the repository root:

```powershell
python -B -X utf8 tools/jerusalem_split/integrate.py
python -B -X utf8 tools/jerusalem_split/validate.py
python -B -X utf8 tools/jerusalem_split/integrate.py --apply
python -B -X utf8 tools/jerusalem_split/validate.py --live
python -B -X utf8 tools/jerusalem_split/test_canal_migration.py
```

The builder derives 16 loaded outputs from pinned Git inputs and the actual Git LFS bitmap. It refuses unrelated changes to any output, retains the original backup on E:, and permits a subsequent rebuild only from its recorded installed hashes. It does not merge the entire branch, change the Git index, commit or push. New state 1253 and province 16538 leave Cayo Blanco del Sur's 1252/16537 intact. The installed COMECON rail-hub catalogues include both city sectors and their new rail link; their owning generator already discovers states and railways dynamically.

Original input backups are under `E:/MDColdWar_Backups/Codex_Test_Archives/jerusalem_split_20261027`. No archive or repeated engine snapshot belongs in the mod directory. The native probe uses a new unique directory under `E:/HOI4_Mod_Tools/mdcoldwar/runtime/jerusalem_split`, freezes scripts and the full map, and never traverses asset junctions while copying. It refuses to launch while another HOI4 process is running. Its temporary territorial transfers affect only that isolated campaign.

The four canal migration tests create and remove only small fixtures under the ignored `.fixtures` directory. The actual Israel generator is not run against the live repository. The real obsolete Suez file is required before its former numeric ID can be migrated; an independent occupant causes a refusal before any writes.

The builder is a guarded integration overlay, not a universal merge engine. A future upstream map, country-history, economy or peace-plan update requires reviewing and updating its pinned inputs before rebuilding. In particular, do not bypass its guards after regenerating the 1970 economy. The existing calibrated population total and productivity are deliberately retained; the sector allocation is approximate and documented in the audit.

Map and state-count changes require a fresh campaign and the same mod build on every multiplayer client. Save migration and live multiplayer have not been tested.
