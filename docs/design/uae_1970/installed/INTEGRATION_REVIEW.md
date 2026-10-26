# UAE 1970 installed integration review

Review scope: the first complete 33-output installation of the approved 107-focus / 40-decision catalogue, followed by bounded refreshes of corrections. This review reads the emitted Clausewitz files and their providers; it is not an HOI4 engine or multiplayer test.

Final verdict: all three identified integration findings are closed in the current installation. No high-value source-level integration finding remains open after the bounded final refresh. All 33 loaded-output hashes match the final manifest.

Reviewed manifest SHA-256: `d599b5a28f55e65be2f766f64a5a692109e45d0679b4b11f79c2e06dfd0ad0da`.

Reviewed contract-event source SHA-256: `94a1550c95e43e6b308e7585da76400208b98b8dc770e73425b38df61d613c77`.

Final bounded metadata refresh: primary foreign refusal guards now also require the sender's recorded partner ID to equal the responding recipient's `ROOT.id`, matching the acceptance identity check. The refresh verified that condition in all 2,560 primary refusal events and rechecked the 33 manifest output hashes. Effects, interfaces, nonces and the preceding integration conclusions are unchanged.

## Findings and correction status

1. **Starting GDP calibration order — corrected and verified in emitted source.** The first installation installed the six dynamic starting difficulties through a separate `on_startup` registration. Native GDP directly reads office and civilian productivity and workforce fulfilment, so freezing the historical accounting adjustment before those difficulties become active could change the starting GDP afterward. The installed `COLDWAR_UAE_startup_pre_economy` now explicitly calls `COLDWAR_UAE_refresh_programmes` immediately after the guarded oil bootstrap, before returning to native startup. This changes no rewards, does not reapply resource grants, and does not reset GDP on later loads. Source evidence: `00_money_system.txt` around lines 5921–5938; `IMP_1970_gdp_scripted_effects.txt` around lines 1828–1834; the explicit early UAE hook in `00_on_actions.txt`.

2. **Stale domestic negotiations — corrected and verified in emitted source.** The first installed Mediate, Court Settlement and Sharjah event acceptances did not consistently recheck the current governing party and earned focus. A player could open the meeting under an eligible government, change party and then complete the old settlement. Court Settlement belongs to the constitutional programme, Mediate and Sharjah to the monarchy programme. The refreshed installation uses non-reused domestic meeting rounds, pending lifetimes, consume-before-action guards, and current government/unlock/crisis checks. An independent structural pass checked all 1,536 domestic meeting events: each actionable option repeats its current eligibility in the executable guard and consumes its meeting-pending state before performing the action. The diplomacy AST suite additionally exercises stale settlement rejection.

3. **A second Council-expiry provider — corrected and verified in emitted source.** The native UAE branch in `IMP_1970_world_politics_effects.txt` could recreate the Council with `expire = "1971.12.2"` after the country-history provider had created a non-expiring Council. Name-based synchronization would not distinguish those instances. The installed `COLDWAR UAE WORLD COUNCIL` marker contains the Council creation without an expiry. A specific regression assertion covers this provider as well as the history and authored provider; all other world profiles remain unchanged.

## Verified integration contracts

### Native campaign and politics

- The campaign predicate uses the persistent 1970 start-date trigger, UAE original tag and dynamic-country exclusion. A later campaign year does not lose the authored tree or its providers.
- UAE history loads `COLDWAR_UAE_1970_focus` for the authored campaign; the fallback dispatcher explicitly excludes it. The later country-history portion beginning in 2000 is preserved.
- The global leader dispatcher routes the approved UAE native subparties before the generic leader kill and modern country-provider dispatch. The native UAE provider is also guarded for direct calls.
- The actual MD subparty callback synchronizes leadership and refreshes the programme ledger. This covers changes between parties inside the same outlook, which an outlook-change on-action alone would miss.
- The pre-federation Council has no 1971 character expiry. Only the independent federation transaction sets both formation aliases and creates the default Zayed presidency. Maktoum and the negotiated Rashid premiership appear as separate status offices. Government changes suspend the negotiated cabinet and its matching active cost while preserving the permanent settlement credit.

### Starting economy and durable rewards

- The existing canonical state resources are Dubai 7 and Abu Dhabi 40. The early once-only bootstrap subtracts 6 and 37 before native money setup and the historical GDP adjustment, leaving the approved 1/3 raw oil start. Existing calibrated saves, later starts and dynamic countries do not receive resource resets.
- Native historical GDP calibration retains the UAE target of $0.686 billion and its existing once-only flag. The UAE decision-price anchor is separately frozen once; it is not a recurring GDP override.
- Focus completion has an executable eligibility/affordability guard and once-earned marker. The refresh routine only recalculates current modifiers. It does not replay treasury transfers, oil, construction queues, productivity, experience or foreign offers.
- Political contributions use exact governing-party predicates. Positive political stability is capped separately; negative contributions remain. Starting penalties are rebuilt from original components plus earned relief, with strongest credits within a shared stage family and a zero floor.
- The broad charter investment contribution requires both accepted Bahrain/Qatar settlements. Oil participation revenue requires an accepted equity agreement. Neither offer alone activates the conditional reward.

### British timetable and spirits

- The native historical world-politics setup immediately initializes the British record after it establishes the ENG–UAE subject relationship. Daily initialization is a guarded fallback rather than a reset.
- The baseline release helper requires actual British subject status, an active schedule and its due date. It requires no focus completion, fresh UAE petition or new UK approval. Pending/refused offers do not pause the historical schedule.
- The historical deadline uses the literal 1 December 1971 scenario date. Negotiated 360-day schedules use the verified native `global.date + 8.64` convention, also used by existing native 360-day investment contracts.
- The paired starting/scheduled/protection spirits are mutually selected by the same UAE record. Exactly one corresponding UAE idea supplies the treaty-dependence −10% political-power contribution; the root dynamic-spirit generator excludes a duplicate carrier.
- The release effect ends the actual British subject relationship, records delivery and removes subject-only programme conditions. A still-protected Council does not become a president merely because the historical date passes.

### Recipient-owned transactions and temporary programmes

- Foreign agreements are recipient events with explicit per-family round IDs, sender pending state, recipient identity and repeat guards. Acceptance rechecks current live conditions and funds; refusal does not transfer money. The independent final structural pass checked all 2,560 foreign response events and 128 buyer-confirmation events; all foreign acceptances repeat their displayed guards in executable code. All 896 British-context response events additionally bind the offer to the current treaty nonce, invalidating proposals after a different agreement changes the treaty record.
- The final refresh additionally checked all 128 British friendship-counterproposal confirmations and all 128 Iranian narrower-access confirmations. Both require the current UAE authority, the original earned unlock, matching live offer round, pending state and the counterpart's still-current quoted response; their executable conditions match the option conditions and consume pending state before action. British counter-confirmation also rechecks actual British subject status, the due-date limit and the current treaty nonce. The Iranian alternative requires Iran to exist and remain at peace with the UAE, and preserves the separate Tunbs dispute. Neither foreign counterproposal binds the UAE before its own confirmation.
- British policy offers now share a UAE/UK policy lock across the protection, release, date-amendment and friendship families. Expired owner rounds are closed by the observer, and nonce changes invalidate superseded popups. The founders' settlement decision has an enabled AI weight; its immutable domestic rounds prevent an old popup from switching already accepted exclusive charter terms.
- British co-financing debits Britain by $0.25 billion and credits the UAE by the same amount. Oil equity and Kuwait support debit the UAE and credit the stated foreign recipient. GCC entry separately charges each joining government's treasury.
- Procurement first obtains a seller quotation, then a distinct UAE buyer confirmation. The buyer's $0.25 billion debit and seller credit occur with the 1,000-unit stock transfer after another stock/funds/round check. Duplicate completion is stopped by consuming the pending offer.
- Bahrain/Qatar acceptance records the negotiated political settlement without annexing states. Islands and Saudi talks record their agreed issues without guessed state/resource transfers. Transit and deployment access require the recipient and create no automatic war entry.
- Paid courses freeze their invoice when started and recheck current government, money and project conditions on completion. Temporary benefits and their disadvantages share the same timed dynamic-modifier carrier; government-bound carriers use the same enable condition for their positive and negative components.
- The Dirham bridge uses the native currency-law category and domestic-currency consumer. It gives no extra reserve-network or exchange bonus and does not restore itself over a later native currency choice on load.

## Validation limits

`test_politics.py` executes the emitted political provider AST and native-boundary contracts, including one-time oil, pre-kill routing, Council continuity in both history and the native world profile, distinct offices, exact-party providers, return/reload preservation, historical death dates, recognition, the convention, currency replacement and byte-stable shared patches. Final validation records 82,479 static checks with zero errors; focus runtime records 10 passing scenarios, politics 11 and diplomacy 19. Layout validation covers 107 focuses with zero overlaps. The independent event pass above examines the installed 4,480-event source, rather than only the generator catalogue, and verifies every manifest output hash. These checks do not establish actual HOI4 tooltip rendering, engine scheduling, initial displayed GDP, queued construction behaviour or multiplayer event delivery. Those remain engine checks.
