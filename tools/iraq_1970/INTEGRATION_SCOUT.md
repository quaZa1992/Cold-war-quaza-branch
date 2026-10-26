# COLDWAR IRQ/USA implementation integration scout

18 October 2026. Read-only inspection before the approved implementation. No loaded file, generator or game state was changed by this reviewer. The paths and hashes describe this snapshot; the implementing agents may subsequently change them. Applied the national-tree/layout skills and the project-contract, source-map and Vietnam integration references.

## USA host and safe chapter placement

The live1970 host is **`common/national_focus/USA_1970.txt`**, tree ID **`USA_1970_focus`**. `history/countries/USA - USA.txt:8` explicitly loads it. Its country selector uses `original_tag`/tag USA plus the persistent1970 scenario predicate. The source comment names `tools/generate_usa_1970_focus_tree.py`, but that generator is absent from the current `tools` inventory; do not invoke a guessed broad generator.

Independently parsed all214 local focuses and resolved their anchors. The host has no current shared-focus imports and no conditional node offsets. Complete center bounds are **x−33…25,y0…58**. Its Nixon/institutional chapters occupy the upper rows; election branches continue down to1996/y58. Appending below an apparent early presidency would collide with later elections. For example, translating the new chapter by(0,20) creates nine card collisions.

**Recommended approved chapter translation: (+30,0).** Preserve all15 concept positions relative to that translation:

| Entry | Installed position |
|---|---|
| Desert Shield | (30,0) |
| Desert Storm | (34,0) |
| Coalition Mandate | (38,0) |
| Northern Access | (30,4) |
| Provide Comfort | (34,4) |
| Northern Air Shield | (36,5) |
| Northern Recovery | (32,8) |

This reserves x30…38,y0…8. All existing214 icons were resolved through their real registrations/textures; none was missing. The widest inspected old icon is110px. Actual old full-icon/titlebar bounds versus the new native art/titlebar rectangles yield **zero cross-chapter collisions**. The rightmost existing defence titles at x25 end at2569px; the first new x30 titlebar begins at2885px, a316px section gap. Existing/new orthogonal connectors occupy separate x bands. The continuous panel at(1200,1100) lies far left of the new block. This checks all current USA host neighbours, rather than only its nearest root. Existing internal USA layout defects, if any, were not redesigned.

Native shared imports are supported: `common/national_focus/gulf_shared.txt` defines top-level `shared_focus` blocks; `00_generic.txt:12` imports `GCC_the_gcc`. The Union/Benelux modules demonstrate separately maintained imported chapters. If using shared focuses for USA, preserve/import **all five independent roots** listed above. Importing only Desert Storm cannot be assumed to include the disconnected Shield/Coalition/relief/access entries. Shared descendants can retain a stable `relative_position_id` anchor at Desert Storm(34,0); independent roots can reference that anchor for positioning without adding political prerequisites. Native descendant import closure must still be checked in the emitted host and in HOI4. A narrow generated-marker append of15 local focus blocks is another safe integration mechanism. Do not add a mandatory Desert Storm prerequisite to humanitarian relief merely to simplify import closure.

USA is already protected from `mdcw_load_1970_fallback_tree`; its history loads the authored host. The new module should join this host, not replace it with a second USA tree or reset presidential progress. Add a native shortcut targeting the actual new Storm root.

## Iraq startup/fallback protection

`history/countries/IRQ - Iraq.txt:8` currently loads **`mdcw_1970_generic_focus`**. Its January1970 block seeds `IMP_1970_profile_national_fascist`, the Baath cosmetic tag and **Ahmed Hassan al-Bakr**, with expiry1979.7.16. Preserve its deferred OOBs, GDP/productivity and starting leader when changing the tree loader and adding country initialization.

**Critical shared edit:** `common/scripted_effects/mdcw_1970_focus_tree_effects.txt:4`, `mdcw_load_1970_fallback_tree`, protects USA/SPR/LBA/EGY/SOV/CYP/ISR/GRE/VIE but **not IRQ**. Add the authored1970 Iraq exemption, following the country+scenario form used for VIE. Otherwise modern `events/Iraq.txt` calls at3501,3699,3936,6044,6517,6700,6956 and7152 can replace the new tree/reset its progress. Changing history alone is insufficient.

The authoritative persistent scenario predicate is `common/scripted_triggers/IMP_cold_war_scenario_triggers.txt:1`, **`IMP_is_1970_scenario`**:

```text
has_start_date > 1969.12.31
has_start_date < 1970.1.2
```

It remains true when a1970 campaign reaches the1980s/1990s. `common/on_actions/00_IMP_cold_war_scenario_on_actions.txt` also sets `IMP_SCENARIO_1970`, but a current-calendar-year gate is inappropriate for programme lifetime. Later starts must retain their native fallback.

## Authoritative MD subparty and leader callbacks

**Exact subparty change entry:** `common/scripted_effects/00_MD_politicsview_scripted_effects.txt:1979`, **`change_ruling_party_effect`**. Inputs include `rul_party_temp`, coalition parameters, `change_leader_temp` and `disable_elections`. It sets `ruling_party`, coalitions, outlook/elections and calls **`set_leader`**. The hidden tail already refreshes country programmes, including `COLDWAR_VIE_sync_programmes`. Add the narrow IRQ1970 refresh there; `on_government_change` alone misses subparty changes within the same outlook. Do not create a second party-selection menu or set only `set_politics` while leaving MD's `ruling_party` inconsistent.

**Global leader dispatcher:** `common/scripted_effects/00_leader_setup_scripted_effects.txt:9`, **`set_leader`**. Before the generic dispatcher kills the incumbent, it calls `MDCW_HP_sync_native_counter`, then special retirement synchronization. CYP/NCY/TUR/GRE already use early1970 country delegations before the generic kill/meta-effect branch. The generic branch invokes `set_leader_[original_tag]`, whose Iraq provider is **`common/scripted_effects/IRQ_political_leaders.txt:1`, `set_leader_IRQ`**.

**Current IRQ historical pool is insufficient:** only governing slot21 routes into `MDCW_HP_native_pool_IRQ_21` (`mdcw_historical_native_pools.txt:6241`), cycling al-Bakr→Saddam→Tariq Aziz→al-Bakr. Its current counter synchronization begins at15995. This is a retirement pool, not a valid dated1979 succession controller; it can resurrect al-Bakr after expiry and the global kill can erase the person before a later callback reads them. Preserve current recognized incumbency before removal, retain memory during expiry gaps, choose the latest due successor on delayed catch-up, and distinguish explicit native retirement from routine refresh/party return. Respect `do_not_retire` and `MDCW_HP_native_retirement`.

The important wrapper is `MDCW_HP_sync_native_counter` at13554: it runs only when `IMP_is_1970_scenario` **and `MDCW_HP_has_native_pool`** qualify. The latter trigger (`common/scripted_triggers/mdcw_historical_native_pools.txt:142`) currently includes IRQ **only for slot21**. Inserting IRQ memory/sync solely inside that old wrapper misses ICP4 and all newly implemented alternatives. An early IRQ1970 branch in global `set_leader`, like the existing CYP/GRE route, can preserve the person before generic deletion and delegate to the country provider. The narrow `set_leader_IRQ`1970 delegation should also be guarded, with modern content retained outside scope. Vietnam's code illustrates the lifecycle pitfalls; its exact slots and dates are not Iraq defaults.

## Party slots, leader identity and name consumers

The historical start sets **`ruling_party=21`**, broad outlook nationalist, coalition slot22. The native profile is in `IMP_1970_world_politics_effects.txt:170`. Existing historical party display already identifies **Baath21, ICP4 and KDP6**. It is therefore incorrect to borrow the modern Iraq provider's ICP19 or modern slot6 Dawa leader wholesale:

- `IRQ_political_leaders.txt` slot6 creates Ibrahim al-Jaafari/Nouri al-Maliki, although the1970 registry calls slot6 KDP.
- Slot19 creates Raid Jahid Fahmi; there is no1970 ICP4/Aziz Muhammad provider in this file.
- Slots2/3/8/11/12/20 contain later figures, and slot21's modern fallback is al-Douri. These are not a completed1970 roster.
- The modern monarchist slot23 has Ra'ad bin Zeid and can inform asset reuse, but the new constitutional programme/eligibility still needs explicit integration.

The concept's existing mechanics/history report maps approved/candidate alternatives at `docs/design/iraq_1970/MECHANICS_AND_HISTORY.md:37–50`, including KDP6, proposed Dawa8 and later SCIRI9. Reuse that approved mapping work and native `01_political_triggers.txt`; do not invent another party array or silently make all emerging parties the same programme.

**Visible party name routing:** `common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt:261` delegates `show_ruling_party` into **`MDCW_HP_ruling_party`**; family-name/description/icon consumers similarly route into **`common/scripted_localisation/mdcw_historical_parties.txt`**. Existing IRQ English entries are in `localisation/english/mdcw_historical_politics_1970_l_english.yml:1055` (ICP4),1175(KDP6),1502(Baath21). The starting-party fallback is separately `IMP_1970_party_name_scripted_localisation.txt:73` / `IMP_1970_has_historical_ruling_party`.

Adding unused English names will not change that UI. Update the current native registry with guarded IRQ1970 entries or country delegation, following VIE's existing first-choice entries for names/descriptions/icons. Preserve other countries and later starts. Exact party and current leader gates should activate earned programmes and remove/re-add only their live modifiers; a refresh must not replay one-time construction/cash/core grants.

## Initial source fingerprints and remaining audit

| Baseline file | SHA-256 |
|---|---|
| `common/national_focus/USA_1970.txt` | `0be13b91dcfdee071ed2045c7e2c87bcf8c94c124171888e30b85d50063d1dbc` |
| `history/countries/IRQ - Iraq.txt` | `906bb30eddbdecf7990ed5c651125863df5dd4e8cc0e42bd6176fd9746623636` |
| `common/scripted_effects/IRQ_political_leaders.txt` | `ab5efe637d598b66fef2ed22e7144bea621d64271b515f286896e2655f0ddc43` |
| `common/scripted_effects/mdcw_1970_focus_tree_effects.txt` | `6af86136ea93de0be490f9107e52401cdc2317c84841c59088563f67d2fffe40` |
| `common/scripted_effects/00_leader_setup_scripted_effects.txt` | `7a4bc251d98c8abc84d9b4d321f39ce825ee01100e078a3c3956407f557c6312` |
| `common/scripted_effects/00_MD_politicsview_scripted_effects.txt` | `b7ee0f667df9d39fe0979927dd8ffbb0e5378844552ad1208bd07761a4f692fc` |

Next independent review must parse the actual emitted Iraq tree and USA attachment, resolve every shared/relative anchor and evaluated offset, compare approved IDs/grouped logic/art, inspect current full/native-size renders and report final hashes. This scout does not certify the forthcoming compiled effects, dynamic-state cleanup, transaction idempotence, imported shared-focus closure or HOI4 behavior.
