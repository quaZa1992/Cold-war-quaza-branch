# COLDWAR North Vietnam: independent implementation mechanics audit

Read-only source audit on 18 October 2026. Only this report was written by the auditor inside the repository; no generated content, compiler, politics integration or broader generator was changed.

**Result: no unresolved source-level mechanics blocker found in the inspected final emission.** This establishes source consistency and traced behavior. HOI4 parsing/loading, rendered tooltips, native UI interactions and save behavior have not been tested by this audit.

## Approved design and executable output

The canonical `approved_design.json` retains SHA-256 `a75e577703dbfa708f5e7493539f46e5280628d1a1e940b3204a38d46082d3d2`.

An independent AST comparison of the loaded files established:

- All 239 focus IDs, emitted coordinates, grouped prerequisites and mutually exclusive IDs match approval.
- Each of the 239 reward helpers contains exactly the approved raw reward AST, followed by the applied stamp and pending cleanup. Funding, implemented-parent and territory/capacity guards wrap those effects; they do not silently replace approved rewards.
- All 16 physical projects queue construction with `instant_build = no`. No instant focus factory grant was introduced.
- All 15 dynamic programmes map the approved modifier keys onto the correct group-specific backing variables.
- All 72 country ideas use ordinary MD idea-picture names with corresponding registered `GFX_idea_...` sprites. The 554 focus/shine/idea/decision sprites resolve to existing texture files.
- All 359 inspected `COLDWAR_VIE_` scripted trigger/effect definitions cover the boolean helper calls made by the inspected VIE focus, idea, dynamic-modifier, event, decision and on-action files. No unresolved political initializer/update call remains.

These checks were performed independently against actual loaded-path files rather than accepting the compiler's own pass count as proof. The compiler validator's current report separately records 7,097 checks and no errors; it is also a static check, not engine validation.

## Native syntax and scope

The compiler correctly adapts the review-only files for actual loading:

- Decision category metadata is emitted in `common/decisions/categories/COLDWAR_VIE_1970_categories.txt`; decision bodies live under category wrappers in their ordinary decision file. The earlier combined review-copy form was not copied verbatim.
- Idea `picture` uses the unprefixed idea key, backed by `GFX_idea_<key>`. Dynamic modifier `icon` and focus `icon` use registered sprite names directly.
- Timed ideas use native `cancel = { NOT = { <eligible trigger> = yes } }`, supported by existing MD country ideas. Losing eligibility cancels benefits and linked drawbacks together; returning does not recreate expired or cancelled timed funding.
- `add_dynamic_modifier = { modifier = ... }` and `force_update_dynamic_modifier = yes` are supported by installed engine documentation in country/state scope. The forced refresh does not re-execute focus rewards.
- `free_building_slots` is a state trigger for available construction levels, including nonshared state buildings. The compiler reads each real building's `level_cap.shares_slots` and includes `include_locked` only for shared-slot buildings. Infrastructure and fossil power do not incorrectly inherit a shared-slot-only parameter.
- Treasury guards use native `check_variable` comparison with `compare = greater_than_or_equals`; the visible money helper uses actual MD `treasury_change` in billions. Variable-delta tooltips use native arithmetic `$RIGHT` values.

Primary local engine evidence: `documentation/effects_documentation.html` entries for `add_building_construction`, `add_dynamic_modifier` and `force_update_dynamic_modifier`; `documentation/triggers_documentation.html` entry for `free_building_slots`. Native MD/CW coding patterns and actual custom-modifier readers are documented in the earlier source audit.

## Lifecycle and scenario integration

`history/countries/VIE - Vietnam.txt:8` loads the dedicated tree. Its initialization call at `:18`, the startup hook, and the country-scoped daily update provide the scenario setup/restoration path. `mdcw_1970_focus_tree_effects.txt:17` excludes VIE from the generic fallback. The later 2000 start is outside the historical block changed by the compiler.

`COLDWAR_VIE_is_1970` checks original tag, existence and the actual 1970 start date. The existing `IMP_is_1970_scenario` tests `has_start_date`, so programme availability does not accidentally expire when the campaign crosses into the 1980s.

`COLDWAR_VIE_initialize` is idempotent. It initializes starting ideas/stage variables and programme values once. `COLDWAR_VIE_sync_programmes` checks implemented roots and exact governing party/leader before attaching a programme; it removes only stale VIE programme modifiers and preserves backing values. It never calls application helpers. Government/ruling-party hooks and the native MD subparty callback in `00_MD_politicsview_scripted_effects.txt:2051` invoke sync, with the daily observer covering leadership changes/restoration.

Focus availability and helper completion additionally require the appropriate implemented parent reward flags. A completed but unfunded focus therefore cannot unlock a whole chain of unimplemented reforms. Deferred retries call the same guarded helper with zero PP cost; the one-time applied flag prevents cash, experience, recovery or buildings from replaying.

### Final political-provider and succession audit

The installed identity integration was separately reviewed after its final expiry-gap correction. `00_leader_setup_scripted_effects.txt:10` calls the native counter synchronizer before its ordinary leader removal; the VIE portion delegates to `COLDWAR_VIE_1970_sync_leader_counter` (`COLDWAR_VIE_1970_politics.txt:24`). The native retirement button sets `MDCW_HP_native_retirement = 1` only around `set_leader`, then clears it (`00_MD_politicsview_scripted_guis.txt:1078`). `set_leader_VIE` delegates the six approved 1970 slots to the dedicated provider and retains its modern fallback outside those slots/scenario. Normal party return restores the remembered person without advancing the counter; only explicit native retirement advances it, and `do_not_retire` prevents that advance. The four communist names exactly match the focus gates. The 18 historical-registry name/description/icon entries are guarded VIE/1970 overrides and resolve through the existing native party-name registry, preserving other countries and later starts.

The daily observer (`COLDWAR_VIE_1970_politics.txt:220`) now synchronizes recognized current leaders before using remembered incumbency. This prevents Le Duan's history expiry on 10 July 1986 from destroying the 14 July succession route if the engine removes his name or substitutes a fallback. Delayed catch-up checks the latest due successor first: after 18 December 1986, stale historical Duan/Chinh memory installs Linh once, rather than creating and killing two successive leaders on one tick. Explicit alternate retirement mandates survive congress dates; deceased Duan/Chinh cannot be resurrected by the rotation, and a prolonged alternate Chinh mandate ends on his historical death in September 1988. Known later human choices take precedence over stale memory. Democratic/Socialist named providers and explicitly alternate collective providers retain their approved party-family identities.

I reran `python -B tools/vietnam_1970/test_politics.py`: all 14 AST/native-workflow scenarios passed, covering initialization idempotence, the pre-kill counter chain, ordinary party return, `do_not_retire`, explicit retirement, socialist reentry, July expiry/fallback, single-install December catch-up, alternate mandates, and other-country/later-start/dynamic-tag scope. This models the authored script sequencing and asserts the relevant native source contract; it does not simulate the actual game's leader-expiry implementation or prove rendered portraits/party labels in the engine. No additional source-level political blocker was found.

## Recurring and diplomatic decisions

The 48 programmes use exact earned provider-focus flags plus their current government/leader gates. A shared decision cannot rely on an unearned common-provider branch. All same-family ideas are excluded at availability and implementation, giving at most one active economy, civic, security and foreign programme.

All 13 foreign offers:

- Recheck sender eligibility, current pending flag, family capacity, recipient existence and available treasury before implementation.
- Restrict acceptance to the intended recipient tag and the current offer.
- Debit VIE only after successful acceptance and attach the approved timed idea once.
- Clear pending/awaiting state on completion, rejection or expiry; feedback is delivered separately.
- Use a 90-day pending lifetime. A stale event cannot later charge treasury without a current pending offer.
- Do not force equipment, land, faction membership, sanctions removal or peace. Existing MD/Imperia diplomacy remains authoritative.

This is a consented domestic consultation/technical programme, not a fabricated transfer from the foreign player's economy. Actual foreign construction or financial aid remains a separate native transaction.

## Future crises

The three approved direct policy consequences—price adjustment, unified southern administration and coercive political screening—remain in the exact approved raw rewards, with their own timed idea definitions. Unified administration checks peace and VIE ownership/control of all three southern states.

The three former integration contracts now have real observers:

- Flood: one configured 1971 window, northern state ownership/control, and a one-time seen flag. It is absent on 1970.1.1 and does not backfire into a later saved game.
- China war: a real `has_war_with = CHI` condition; temporary border pressure renews while the war continues and cancels at peace. No war declaration is generated.
- Patron supply: begins watching only after accepted cooperation. Loss of the actual cooperation idea, patron existence or a recorded communist patron's later government transition can trigger the shock once.

The initial compiler shocked an accepted relationship with an **already noncommunist** SOV/CHI as if its government had just fallen. This finding was corrected: acceptance now records `COLDWAR_VIE_communist_patron_SOV/CHI` only when the patron is communist at acceptance, and the government-loss condition requires that recorded marker. This preserves valid alternate diplomatic relationships.

## Construction from zero starting civilians

The approved starting northern states have zero civilian factories. Queueing buildings alone does not invent construction capacity. No extra starting factory, GDP, equipment or OOB was added by this implementation.

Two existing paid native routes are source-traced:

1. **Economy → economic projects → Leasing → Civilian Complexes +** executes `add_offsite_building = { type = industrial_complex level = 1 }` in `00_MD_economyview_scripted_guis.txt:916`. It charges recurring native lease expenses (`00_money_system.txt:3664`–3673), does not add GDP/corporate income, and can later be reversed. It needs no initial civilian factory or peace condition. It is a manual human-player action, not automatic free aid.
2. **Donor selects a VIE state → Investment → Civilian Industry/Infrastructure/Agriculture → offer → VIE acceptance.** Native `99_investment_scripted_effects.txt:428` calculates a separate timed project assuming construction capacity independently of VIE's civilian count. On expiry, `complete_project:553` calls `add_finished_buildings` to install the real finished building. Donor treasury, VIE's 10% co-payment, native limits and donor influence apply. Actual active investment cost arrays, rather than stale building-header prices, determine the cost.

The existing Imperia **Transfer Funds** diplomatic action (`imp_money_transfer_diplomatic_actions.txt:38`–39) can finance agreed co-payments or leases with a real sender debit, recipient credit and acceptance. This does not require a new focus-only capital system. Merchant trade is a contingent campaign source of capacity; no guaranteed export-customer bootstrap was assumed. The owned-state temporary infrastructure investment is a policy modifier, not proof of a completed physical road.

## Runtime verification still required

Run a 1970 VIE campaign and inspect the engine error log; starting tree/spirits; conditional reward tooltips while underfunded, under another party and after implementation; actual lease and native investment UI; government and leader departure/return; exact decision caps/cancellation; pending focus retry; foreign acceptance/refusal/expiry; flood, China-war and patron transitions; then save/reload.

These are the confidence limits of static source review. They do not imply an additional source-level blocker, and no claim of engine or multiplayer balance testing is made.
