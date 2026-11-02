IMPERIA COLD WAR: Implemented USA 1970 expansion

Latest follow-up: [Kuwait-war access and local Iraqi counterplay](../iraq_1970/usa_gulf/PLAYER_REVISION_IMPLEMENTATION_20261025.md) supersedes the earlier Gulf runtime hashes and generic-wrapper count in this dated report. The 15 Gulf IDs now use their owning generator directly, with 14 visible cards; the retired contact receipt is hidden.

24 October 2026, with the requested screenshot corrections completed on 25 October. Implemented following the user's approval of the researched proposal and visual design. Earlier inventories preserve the pre-expansion state. [Player revision](PLAYER_REVISION_20261025.md) records the removed calendar barriers, upgraded early agreements and explicitly accepted tax-cut deficit.

Construction follow-up: the user's live screenshots exposed an invalid shared-slot parameter on independent buildings. The current correction removes `include_locked = no` from 79 infrastructure, energy, silo and port checks across four runtime files. The building class is now read from the actual loaded definitions. Ownership, control, caps, grant quantities, costs and receipts are unchanged. `CAPACITY_FIX.json` records the exact old/new hashes and proves these runtime differences consist only of removing that parameter. The earlier native agreement run did not exercise this case; the capacity correction has source/model coverage and still needs confirmation after restarting the game.

## Installed content

The USA tree now contains **281 focuses**, up from 229. The original approved 65 authored packages consist of 13 revised existing rewards and 52 additional focuses. The screenshot revision replaces another three original rewards, bringing the authored total to **68 packages: 16 existing focuses and 52 additions**. There are now **19 offer focuses and 20 contract families**, because North American Trade sends independent Canadian and Mexican proposals. All original focus IDs remain present.

The domestic expansion adds industrial tools and workforce training, commercial research and redevelopment, alternative reactor and efficiency programmes, military establishments and specialised force development, naval choices, civil-rights implementation and deeper 1972/1980 party priorities. Mutually exclusive choices retain useful advantages with explicit, smaller institutional or fiscal costs. Continuations replace a family's cumulative spirit tier instead of stacking multiple copies of the same programme.

Later party programmes remain visible under either government. Ninety-two original partisan focuses require the actual native Republican or Democratic party in power at execution. Forty-four original ongoing programme bundles and the corresponding new partisan spirits deactivate and restore with the actual governing party. Enduring institutions, enacted measures, historical election receipts and earned physical assets persist. A party change never repeats setup payments, construction or research grants.

## Recipient-approved foreign policy

The 16 advanced offers cover the two alternative German defence arrangements, Canadian industrial cooperation, British research, Japanese cooperation, South Vietnamese assistance, Chinese commercial exchange, Soviet scientific exchange, Bahraini facilities, Israeli procurement, Saudi cooperation, Mexican development, Rogers mediation, Atlantic research, Canadian retooling and Pacific maintenance. Three existing roots now add Israeli security aid, two independent North American trade partnerships and a readiness offer for actual NATO or major non-NATO allies. These standing programmes require real recipient acceptance. Active early Israeli, Canadian and Mexican pairs are required before their paid industrial follow-ups. Each partner counts once toward the legacy partnership network across both tiers.

Offers originate from their distinct US focuses. The named recipient receives an event and accept/refuse decisions. Completing the focus and sending an offer grants neither country's programme spirit and performs no setup transaction. The final valid recipient acceptance activates the agreed package. Rogers mediation requires both Egyptian and Israeli approval before activating the three participants.

Standing agreements have no automatic spirit expiry. Time-limited programmes use fixed calendar terms of 180, 365 or 730 days as specified. Suspension does not extend their calendar. Renewal requires renewed consent. Both parties can terminate their agreement. Pending offers expire after 90 days, with retry safeguards.

Both countries' existence, bilateral peace, native embargoes and all four mirrored Imperia sanction classes determine activation. Parent-dependent programmes require their actual active parent spirit; NATO content requires actual membership. Loss of these conditions removes both sides' programme benefits and recurring streams. Restoration never repeats setup fees or assets. Shared family receipts also prevent farming rewards by switching German variants or signing again.

Initial and renewal previews show both countries' complete prospective numeric effects, exact spirit modifiers, setup and weekly costs, slots, buildings and research rewards. They remain available before signing and while execution is blocked. Preview helpers do not mutate gameplay state. Internal routing and transaction receipts remain hidden, while meaningful membership and relation requirements are visible.

## Cleanup and integration

- Retired the superseded generic USA offer senders and queued counteroffer rewards, preserving their identifiers and historical receipts. Existing Nixon diplomacy remains available with complete native prospective previews. Old payments are not replayed to install new treaties.
- Wrapped 199 remaining original nonzero reward packages in one-time transactions. Ownership, control, capacity and current political requirements are checked again on execution. If a completed focus cannot validly enact its package, it leaves a recoverable entitlement and a narrowly visible enactment decision without charging for missing assets. The three replaced early roots instead use their own recipient-approved transactions and exact old-save delta migration.
- Added matching shared building slots before every targeted original construction level, including infrastructure. The 51 original construction focuses contain 135 construction commands. Actual building ceilings and usable state space remain separate guards.
- Integrated matched treaty income/expense into the real native weekly consumers exactly once. Fixed nominal payments enter after generic expense inflation. The active reactor programme contributes its actual 0.03 weekly expense. Calculation helpers reset their accumulators and do not charge setup costs.
- Replaced unsafe long Gulf daily-budget literals with short weekly values and native division by seven. Existing cadence and weekly budgets are preserved.
- Corrected 47 older Gulf offer, delivery and cooldown flag setters to use an explicit native value. The engine A/B test confirmed that the omitted value failed a normal flag-presence check in this build. Other targeted legacy USA, Nixon and Bahrain files were independently checked for the same omission.
- Kept ordinary event artwork inside the actual MD country-event frame. Corrected the older Bahrain events' broad news image to an unchanged framed donor. The sovereign-facilities treaty and territorial-cession alternative cannot both transact.
- Cleaned the generated tree and helpers with syntax-preserving formatting. Script files use UTF-8 without BOM; English localisation uses UTF-8 with BOM. All 281 captions fit the measured native 147-pixel bitmap width. Artwork, full descriptions and agreement names remain separately sourced.

## Verification

The current scoped source run passed **4,194 assertions across 46 parsed runtime files**, with no scoped warnings. It checks 281 focuses, 68 authored packages, 19 offer focuses, 92 partisan gates, modifier providers, previews, legacy routing, real money consumers, construction slots/guards and native caption widths. It rejects the shared-slot-only parameter on independent state and province buildings. Shared native idea providers are parsed for their membership callbacks; their unrelated existing modifier sets are outside the USA audit.

Native loading exposed an unsupported `has_building` trigger in the new domestic capacity guards. It was replaced in the canonical generator with the documented state dynamic value `building_level@<type>` and an amount-aware native comparison. A regression check now rejects the unsupported trigger, and boundary cases verify two-level grants against the real building definitions while retaining the separate slot requirement.

The current revision passed **15 domestic, 12 focus-date, 15 economy, 14 early-cooperation and 11 integrated regression tests**, plus **36 advanced-agreement emitted-AST model cases**. They cover the reported capacity failure, true current-party requirements, once-only tax migration, old root deltas, real membership callbacks, consent, costs, sanctions, parents, expiry and duplicate prevention. Both transaction models reject the invalid building-class parameter. The previously completed presentation suite passed five tests and the targeted Gulf harnesses passed 34 checks. Repeated compilation produced no changed gameplay files.

The installed views use the actual current MD assets and bitmap font. Independent inspection found no card/title/icon overlaps or missing artwork in the full tree and detailed branches. Some long connectors pass behind intervening cards in the reconstruction; native connector routing and hover behavior remain engine observations. Very wide labels may have a small decorative outline overhang in the reconstruction, distinct from measured glyph advance.

The isolated native-engine run before the screenshot revisions **passed 92 checks with zero failures**. It reached the first hour, the shortened programme's actual calendar expiry and the first weekly update on 5 January 1970. Both the frozen runtime and fixture remained unchanged. Its 41 runtime/localisation hashes matched the installed validated files at that freeze. The full compiler was rerun before that freeze and produced no changed integration output. Those checks covered agreement transactions and shared-slot Canadian construction, not the subsequent capacity, calendar, early-cooperation or tax revisions. Those current changes have not been retested in the engine.

The native checks verify Canadian pending consent without spirits, payments or construction; actual recipient-helper acceptance; the exact US 6 and Canadian 4 setup deductions; one factory grant; duplicate-call protection; all 16 combinations of sanction holder/class/direction; restoration without repeated fees/assets; the British paired programme and weekly expense; pure repeated native budget calculations; and the actual 0.03 reactor expense contribution. The standing Canadian agreement remained active after the shortened British agreement ended.

The engine A/B diagnostic recorded `has_country_flag = no` immediately after an omitted-value timed setter and `yes` after the equivalent explicit-value setter. Actual native weekly-to-daily Gulf division produced 0.00714, 0.00357 and 0.00285. These observations drove the canonical flag and fixed-point regression checks.

Final freeze SHA256: `b180be15873a3ee95c46d49c6afa5e22892a1ba028e60bbb6cabe3e9c7178a42`. The last refresh changed only the four validated Gulf files on the already passing frozen world baseline. Unrelated live changes from other chats were not imported into that test. The run took 638 seconds and stopped only its own game process after completing its checks.

The native diagnostic filter found **zero lines associated with the targeted files or fixture**. The complete log contains **1,044 external diagnostic lines**, retained for separate work; this result is not a claim that the whole mod has no diagnostics. The raw result, full game/error logs, complete engine logs, exact fixture and loader sources, prior attempts and retention record are under `tools/usa_1970_expansion/native_probe/runs/usa_final_20261024/`. The copied 7.48 GB asset provider and other temporary bulk test directories are pruned after archiving; their manifests/hashes and a compressed full asset manifest remain.

The fixture changes only six Canadian/British event AI weights to select Review and appends a logging event that proves the override loaded. All original event guards, option effects, previews and pictures remain unchanged. Acceptance calls the real production recipient helpers directly. The one-year British term is shortened to one day only inside the fixture, then observed through the normal daily reconciliation. This establishes native transaction and calendar behavior, not human acceptance clicks or a full unaccelerated term.

Live human recipient acceptance, multiplayer synchronization, save/reload migration and a complete unaccelerated long-term campaign remain distinct manual rehearsals. The implementation includes guards and migration checks for those cases; they are not represented as completed network tests.

## Reproduction and visual evidence

See `tools/usa_1970_expansion/README.md` for the compiler, scoped checks and native probe workflow. `source_snapshot.json` is the immutable pre-expansion source; `proposal.json` is the immutable approved design. The pinned proposal SHA256 is `f524a00e9ab934872d748994b5de1ac89608a791de6cf6b28b0d7c55b142cfa8`.

- [Full installed tree](installed/USA_FULL_INSTALLED.png)
- [Foreign policy](installed/USA_FOREIGN.png)
- [Energy and industry](installed/USA_ENERGY_INDUSTRY.png)
- [Defence](installed/USA_DEFENCE.png)
- [1972 priorities](installed/USA_1972_PRIORITIES.png)
- [1980 priorities](installed/USA_1980_PRIORITIES.png)

These are source-derived reconstructions, not live game screenshots. Their notices retain the source/asset attribution and explicitly identify unknown individual artwork licences. No commit, push or unrelated country cleanup is included in this work.
