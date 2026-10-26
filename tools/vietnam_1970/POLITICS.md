# COLDWAR VIE 1970 political integration

The approved political identity and succession additions use the existing MD/Imperia party and retirement workflow. These files do not create a second leader menu or change the approved focus geometry or rewards.

## Public hooks

| Helper | Caller and purpose |
|---|---|
| `COLDWAR_VIE_1970_initialize_politics` | Main VIE one-time initializer. Records the existing historical chief, preserves starting government/popularity/coalition and refreshes native names. |
| `COLDWAR_VIE_1970_update_politics` | Main VIE daily observer. Refreshes known incumbency, handles due historical succession and the 1976 party-name change. |
| `COLDWAR_VIE_1970_sync_leader_counter` | The VIE block in native `MDCW_HP_sync_native_counter`, before the old leader is killed. Records the current person and keeps the legacy counter aligned. |
| `COLDWAR_VIE_1970_set_leader` | Approved-slot branch of native `set_leader_VIE`; also delegated by the VIE historical native pool. Installs the current candidate, then calls `COLDWAR_VIE_sync_programmes`. |

The main compiler owns the initializer/daily calls and the generated `COLDWAR_VIE_sync_programmes` helper. The dedicated politics file is hand-authored and is not a compiler output.

## Roster and identity

| Existing MD slot | Era-specific identity | Leadership |
|---|---|---|
| 0 | Vietnamese Nationalist Party / VNQDD | Proposed collective Nationalist Return Committee |
| 2 | Democratic Party of Vietnam | Nghiem Xuan Yem |
| 3 | Socialist Party of Vietnam | Nguyen Xien; native retirement can select Hoang Minh Giam |
| 4 | Workers' Party of Vietnam, renamed Communist Party of Vietnam after the December 1976 congress | Le Duan → Truong Chinh → Nguyen Van Linh; Vo Van Kiet is an explicitly alternate party-chief mandate |
| 19 | Vietnam Fatherland Front | Proposed collective Fatherland Front Presidium |
| 22 | Provisional Military Council | Proposed collective; no real officer is assigned a fictitious historical coup |

Yem, Xien and Giam are real historical Front-allied politicians. Their independent liberal/pluralist governing roles are alternate transformations, not descriptions of a historical anti-communist opposition. The Socialist Party is distinct from the southern Hoa Hao Democratic Socialist Party. Kiet was historically a practical local/national government administrator and never national General Secretary. Collective governments use institutional emblems rather than unrelated faces.

Sources: [Yem, institutional biography](https://daidoanket.vn/ky-su-nghiem-xuan-yem-tong-thu-ky-dang-dan-chu-thanh-vien-quan-trong-cua-mat-tran-10078504.html), [Xien, official Nghe An biography](https://baonghean.vn/giao-su-nguyen-xien-mot-nguoi-vinh-loi-lac-10261254.html), [Giam, Foreign Ministry biography](https://www.mofa.gov.vn/vi/bng_vietnam/nr050225105543/nr050225105648/nr050302090431/ns050302093534/view), [Chinh, official party biography](https://en.daihoidang.vn/nhan-su/truong-chinh-1094.html), [official congress chronology](https://en.daihoidang.vn/lich-su.html).

## Succession, expiry and player choice

The current communist incumbent ordinal is persistent: 0 Duan, 1 Chinh, 2 Linh, 3 Kiet. It is distinct from a new selection menu; native retirement advances it and sets the alternate-succession flag. `do_not_retire` preserves the person. Returning to the party reuses the remembered incumbent rather than advancing automatically.

The historical line installs Chinh on 14 July 1986 and Linh on 18 December 1986 using native `set_leader`. The observer first synchronizes any known current chief. It then uses remembered incumbency, **not a required surviving `has_country_leader = Le Duan` name**, because history gives Duan an expiry of 10 July. Thus engine expiry, a temporarily missing leader or an engine-generated fallback cannot strand the historical succession after the four-day gap.

Delayed historical catch-up checks the latest due successor first. A first observer tick after 18 December with stale Duan/Chinh incumbency installs Linh once, without creating Chinh and killing him immediately. Repeated ticks and saved-state reloads do not repeat installation.

The historical observer requires a remembered incumbent and slot 4 in government. It does not replace another governing party. A known later human choice synchronizes memory before eligibility is evaluated. Manual alternate mandates survive the December 1986 congress: early Chinh can remain until his historical death on 30 September 1988, while Linh and Kiet remain selected. Dead Duan/Chinh are skipped on new selections; current expired/missing alternates are also replaced at their death/succession boundaries. The political routes do not script unrequested popularity changes, election winners or automatic dissolution of an independently governing alternative party in 1988.

## Reproducible verification

Run from the mod root:

```powershell
python tools/vietnam_1970/test_politics.py
```

The test writes no files. It parses and executes the installed helper bodies plus the actual VIE country provider through an intentionally limited AST interpreter. It models the observed native ordering `counter synchronization → outgoing leader removal → country provider`, and independently asserts that source-order contract in the global dispatcher. Unsupported authored statements fail instead of silently passing.

Fourteen scenarios cover:

- Historical start preservation and idempotent initialization.
- Early retirement, all four CPV candidates and the native legacy counter.
- `do_not_retire`.
- Party departure/return with remembered incumbency.
- Socialist secondary leadership and return.
- Exact July/December 1986 date boundaries.
- Duan expiring during the four-day gap, including an engine fallback name.
- One-install December catch-up, repeated ticks and saved-state copying.
- Known later human choices with stale remembered data.
- A prolonged alternate Chinh mandate and expiry at his death.
- All three collective providers.
- Non-1970 scenarios, other original tags and dynamic countries; modern VIE liberal fallback remains Do Hoang Diem.
- Native source integration and supported script comparison operators.

All 14 passed after the expiry revision. This is a script-level integration check, not an HOI4 engine/UI or multiplayer session. The main content validator separately checks focus content. Engine checks still need native retirement UI, party changes, portraits and save/reload.

## Maintaining the manual providers safely

Do not run the broad historical-politics generators to rebuild this country. They own many unrelated countries and would overwrite existing country-specific integrations. `tools/vietnam_1970/compile.py` owns focus/effect outputs but must leave the dedicated politics, portraits and manual provider patches intact.

If a broad historical regeneration is deliberately authorized later, first preserve the current affected files outside the loaded mod and inspect its proposed diff. Reapply only the following VIE integrations, then run this test and the main validator:

1. In `VIE_political_leaders.txt`, put the 1970/non-dynamic slot 0/2/3/4/19/22 delegation ahead of the retained modern body. Do not replace the modern contents with a new country-wide roster.
2. The body of `MDCW_HP_native_pool_VIE_4` delegates to `COLDWAR_VIE_1970_set_leader = yes`. The VIE slot-4 block inside `MDCW_HP_sync_native_counter` delegates to `COLDWAR_VIE_1970_sync_leader_counter = yes`. Preserve every other country's block.
3. In each of the six native historical party registry families below, insert the VIE rule immediately after its `name = MDCW_HP_<family>` and corresponding `_desc` / `_icon` names. This is 18 first-match rules. Preserve other countries' lookup rules.

| Family | Slot |
|---|---|
| `Western_Autocracy` | 0 |
| `liberalism` | 2 |
| `socialism` | 3 |
| `communist_state` | 4 |
| `Neutral_Communism` | 19 |
| `Nat_Autocracy` | 22 |

Rule template, using the matching slot and optional suffix:

```text
text = { trigger = { original_tag = VIE IMP_is_1970_scenario = yes } localization_key = COLDWAR_VIE_1970_party_<slot><suffix> } # COLDWAR VIE 1970
```

The existing registry is ahead of vanilla names in the politics UI, so merely adding a localization key without these consumer rules is insufficient. The generic trait and native election/coalition systems remain authoritative.

## Complete subtask file list

Hand-authored code, localization and provider changes:

```text
common/scripted_effects/COLDWAR_VIE_1970_politics.txt
common/scripted_effects/VIE_political_leaders.txt
common/scripted_effects/mdcw_historical_native_pools.txt
common/scripted_localisation/COLDWAR_VIE_1970_politics.txt
common/scripted_localisation/mdcw_historical_parties.txt
localisation/english/COLDWAR_VIE_1970_politics_l_english.yml
interface/COLDWAR_VIE_1970_portraits.gfx
```

Assets and provenance:

```text
gfx/leaders/VIE/1970/COLDWAR_VIE_1970_truong_chinh.dds
gfx/leaders/VIE/1970/COLDWAR_VIE_1970_nghiem_xuan_yem.dds
gfx/leaders/VIE/1970/COLDWAR_VIE_1970_nguyen_xien.dds
gfx/leaders/VIE/1970/COLDWAR_VIE_1970_hoang_minh_giam.dds
gfx/leaders/VIE/1970/COLDWAR_VIE_1970_portrait_sources.json
```

Verification and documentation:

```text
tools/vietnam_1970/test_politics.py
tools/vietnam_1970/POLITICS.md
```

The four new portraits are 210 × 279 DDS DXT5. Original identified Chinh/Giam photographs underwent size/format normalization. Yem/Xien used identity-preserving built-in image editing to reframe the verified historical photographs, followed by engine conversion. They are source-derived portraits rather than untouched archival originals; the JSON records URLs, processing and prompts. Existing Duan/Linh/Kiet portrait files are reused unchanged. There are ten leader/emblem references and twenty unique English localization keys.
