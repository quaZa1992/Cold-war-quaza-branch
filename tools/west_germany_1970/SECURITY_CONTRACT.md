<!-- IMPERIA CW — Cold War: authoritative RAF integration and verification contract. -->

# One German RAF case

The German focus tree, federal security cabinet and shared **Security Affairs** file use the same native RAF variables. There is no second recruitment, prisoner or incident simulation in the shared file. `cwger_raf_cadre`, `cwger_raf_milieu`, `cwger_raf_gen`, `cwger_raf_prisoners`, the wanted cards and the native attack plans remain authoritative.

`security_contract.py` emits the common lifecycle, programme and custody providers. `../colonial_affairs/raf_programmes.json` supplies both interfaces with one programme catalogue. The old shared programme flag IDs are deliberately retained for existing saves.

| Focus | Programme available in both interfaces |
|---|---|
| BKA Expansion | Federal-State Case Coordination |
| Data Protection | Judicial Review of Security Measures |
| The Stammheim Trial | Independent Prison Medical Review |

These focuses retain their original rewards and graph position and add an explicit unlock receipt. Relevant security focuses refresh the same native case. Completed focuses are reconciled into receipts without replaying their construction, political-power or modifier rewards. An already paid legacy programme can finish its term; a new activation requires its focus. The reconciliation focus retains its existing OR prerequisite group.

All shared programme buttons call the native German actions. Payments, requirements and cooldowns are checked again inside the effect. Existing native actions, wanted-person access, protection details and prison-regime changes also recheck their native availability before changing anything. Dragnet searches require the existing doctrine unlock as well as BKA level 3.

## Runtime ownership

- `COLDWAR_GER_1970_raf_case_active` is the single lifecycle gate: initialized German 1970 system, 14 May 1970 or later, generation 1–3, no dissolution or shared settlement. January staging values remain stored for compatibility but do not recruit, conduct manhunts or plan attacks before formation. Non-RAF internal-security cases retain their existing behavior.
- `COLDWAR_GER_1970_monthly` invokes `security_external_monthly` exactly once before the native recruitment and security ticks. That helper applies reconciled foreign-aid growth and the two ongoing programme effects. The shared contact monthly hook does not grow the RAF.
- `security_refresh_threat` recomputes the derived left-wing threat without recruitment, arrest, attack or programme rolls. Focuses, aid deliveries and actions can refresh it immediately. Existing other left-wing organisations keep their contributions.
- `security_weekly_budget` recomputes a display/accounting total only. The existing `COLDWAR_COL_domestic_budget` adds that total once to the MD weekly expense path. Neither UI charges a second expense.
- Closure clears the three live programme flags, cached aid, attack plans and hostage ultimatum. Programme cooldowns survive. The daily reconciliation and immediate action guards prevent closed-case payments or recruitment.
- The German daily callback invokes the native refresh provider, updating formation dates, programme expiry and hostage countdowns. Full presentation arithmetic runs only for an open human cabinet; closed and AI windows remain asleep.
- `sec_reconcile_custody` marks excess current-generation custody cards as **No longer in custody** when aggregate prisoner counts fall, including German Autumn and Kinkel releases. It never fabricates prisoners or discards aggregate prisoners from previous generations. Closed cards use existing neutral portrait/badge frames.

Foreign assistance still requires an agency and a network strictly above 50% in the exact supported state. All four German contact regions share one 15-point RAF aid cap, existing package prices and disclosure risks. The shared file can open the native security cabinet directly. The cabinet's fourth tab also exposes the three common programmes and their additional weekly cost.

## Bounded build

From the mod root:

```powershell
python tools/west_germany_1970/compile_security.py
python tools/colonial_affairs/compile.py
python tools/west_germany_1970/test_security_contract.py
python tools/west_germany_1970/test_performance_gui.py
python tools/colonial_affairs/validate.py
python tools/colonial_affairs/test_runtime.py
```

`compile_security.py` renders the canonical German generator into memory, then replaces only security-owned blocks, related focus rewards/localisation and the German Autumn custody refresh. Unrelated live government, economy, foreign-policy and unity content is preserved. `security_integration.json` records changed files and inspected blocks. The full national compiler includes the same contract for future complete rebuilds.

`security_contract_tests.json` records installed-script lifecycle, accounting, focus, custody and stale-click tests. The GUI regression executes real lifecycle providers and checks open/closed/AI refresh behavior; it does not measure engine frame times. The historical policy precedents and authored numerical calibration are recorded in [MEASURES_HISTORY.md](../colonial_affairs/MEASURES_HISTORY.md). Native HOI4 loading, hover rendering, save/reload and multiplayer synchronization remain untested.
