IMPERIA COLD WAR: Israel V2 native content compiler

The approved 213-focus catalogue in `design.json` is immutable. The native compiler extends it with three recipient-approved project-financing focuses and one paid cabinet emergency authorisation. The resulting live tree has 217 focuses in 19 programmes and retains the existing runtime tree ID `ISR70_focus`.

Installed on 29 October 2026. All 216 artifacts match a fresh build and the canonical inputs of the final native fixture. The 102 source/model tests and 29 native fixture assertions passed. The overall native report remains failed solely because twelve unrelated France/USA root files changed while its immutable snapshot and fixture stayed unchanged. See `docs/israel_1970_v2/IMPLEMENTATION.md` for the scoped review, exact installation receipt and unrun engine/multiplayer coverage.

## Build and verification

Run from the mod root:

```powershell
python tools/israel_v2/compile.py
python tools/israel_v2/validate_runtime.py
python tools/israel_v2/compile.py --write
python tools/israel_v2/validate_runtime.py --installed
```

The first command builds in memory and writes compact documentation only. `--write` installs the returned game payload. Every focus has one runtime action owner. Shared MD money and political-localisation files are read fresh and patched at specific marked entry points. Existing unrelated country work must remain intact. Rebuilding is deterministic and idempotent.

The original `validate.py`, `render.py` and proposal reports describe the approval phase. Their preservation assertions are not the runtime contract after installation. Do not edit the approved snapshot or replace its hashes to turn an old assertion green. Use `validate_runtime.py`, the seven `test_runtime_*.py` suites and the separate native probe for the implementation.

The old `tools/israel_1970/build_content.py` command routes to this compiler after installation. An unselectable, effect-free compatibility registry retains the 399 old focus IDs for guarded legacy-script references. These are not playable additional focuses. Delayed old Israel callbacks are retired, known unfinished paid reservations are refunded exactly once, and the separate Egyptian canal callback is preserved. Completed old assets and debt are retained. Migration of old focus progress is not implemented; begin a new 1970 campaign for the replacement tree.

## Runtime responsibilities

| Module | Responsibility |
|---|---|
| `runtime_core.py` | 153 generic policy, industry, research and military actions; national programme aggregates and native numeric previews |
| `runtime_domestic.py` | 13 restricted funding, procurement, reserve and home-front actions |
| `runtime_bilateral.py` | 18 recipient-approved country-event offers, actual project capital, equipment orders, loans and investor claim credits |
| `runtime_territories.py` | 33 controlled and foreign settlement actions, four occupation profiles, host costs and Palestinian pressure |
| `runtime_money.py` | Native weekly budget consumers and protection against anonymous repayment of named bilateral principal |
| `runtime_legacy.py` | Old callback isolation, exact paid-reservation refunds and the four corrected old state-enable scopes |
| `runtime_integration.py` | Scenario bootstrap, native party names, legacy entry points and compatibility registry |
| `runtime_layout.py`, `runtime_titles.py`, `runtime_art.py` | Compact native geometry, short readable labels and proportionally fitted existing artwork |
| `runtime_preview.py` | Reconstruction of the actual emitted focus code for the interactive inspector |

All new choices originate in focuses. Bilateral offers require the actual recipient's acceptance through a country event. Unilateral settlement programmes do not ask the host or Palestine for permission. There is no new Decision menu, automatic war, border transfer or core grant.

The three compatible workforce reforms add five percent each, with fifteen percent in total and no negative workforce-size modifier. Financial support uses actual Treasury/debt transactions or restricted funding. The United States, West Germany and Romania may each subscribe two percent of quoted Israeli GDP from real available funds. Israel receives restricted project capital; the payer receives the corresponding native investment asset. No invented private-capital account or guaranteed dividend is used.

The home-front programme uses native medical-support unit technology because the proposed shelter building has no valid MD provider. The four religious-workers projects are paid cooperative contracts under the actual native governing-party check; they do not invent separate cabinet representation. Both adaptations are explicit runtime overlays and leave the approval catalogue unchanged.

## Evidence and sources

Source/model results are recorded in `docs/israel_1970_v2/runtime_test_runs.json` and `runtime_validation.json`. Native execution has its own report under the private E: run directory, linked by the implementation report. A browser reconstruction is not a game screenshot. Source/model tests do not prove native rendering, save/reload or multiplayer stability.

The isolated native probe must be explicitly prepared and run. It refuses any existing HOI4 process, freezes source hashes, overlays the compiled payload without installing it, and stops only the process it created. Profiles and complete logs belong under `E:/HOI4_Mod_Tools/mdcoldwar/runtime/israel_v2`. Read `docs/israel_1970_v2/NATIVE_PROBE_PLAN.md` for the artificial transaction fixtures and remaining coverage limits.

Historical precedents and policy trade-offs are recorded in `docs/israel_1970_v2/POLICY_EXPANSION_RESEARCH.md`, `FOCUS_ONLY_CONTENT_REVIEW.md` and the module implementation records. Proposed balance numbers are game design, not historical economic measurements. Existing MD artwork retains its original rights; each generated DDS has a companion provenance record. See `IMPERIA_COLD_WAR_NOTICE.md`.
