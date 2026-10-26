<!-- IMPERIA CW — Cold War: independent Spain V2 political-provider source review. -->
# Independent political integration review

Reviewed the generated V2 politics effects, triggers, events and on-actions
against `politics.py`, its roster, `compile.py`, native leader routing,
`change_ruling_party_effect`, the actual political GUI retirement action and
`events/MD_Elections.txt`. This is a source review, not a HOI4 runtime test.

## Refreshed disposition

All four findings below are resolved in the refreshed provider source. Ordinary
Franco dispatch now has an explicit preservation branch independent of the
retirement-protection flag. Rejected reform has a free reconvening decision.
Political questions have current pending/generation predicates in their displayed
and executable options, with harmless lapsed choices and mandate invalidation.
The election observer renews the mandate only after the real native campaign and
coalition flags clear. A follow-up issue found during this refresh—government
change after the constituent ratification event opens—is also fixed by reissuing
ratification to the incumbent cabinet of the already-elected assembly.

Independent focused execution of the current generated effect source confirms:
ordinary 1972 Franco dispatch preserves him; a missing-name UCD return recreates
Suárez; a missing-name AP/PP return in 1992 recreates Aznar; government change
during open constituent ratification updates the ratification authority and
queues the current cabinet's question. These fixtures deliberately do not model
engine GUI scheduling or character objects.

Old identical event windows may answer the currently reopened identical question
while its current pending receipt is valid. The implementation does not provide a
separate immutable event-local proposal nonce, and this report does not claim
stronger stale-window isolation than the source implements.

## Corrected findings retained as an audit record

1. **P1 — Ordinary dispatch can kill Franco without installing a successor.**
   `common/scripted_triggers/COLDWAR_SPR_v2_politics.txt:46` makes
   `COLDWAR_SPR_keep_current_incumbent` require `do_not_retire` even for Franco.
   An ordinary `COLDWAR_SPR_dispatch_leader` callback before 20 November 1975,
   with native-retirement context zero and that flag absent, reaches its
   `kill_country_leader` branch at
   `common/scripted_effects/COLDWAR_SPR_v2_politics.txt:619`. The next setter
   (`:449`) checks `COLDWAR_SPR_franco_in_office` again. Franco's name was just
   removed, the one-day expiry fallback is false before November 1975, and the
   Falange provider also fails because departure is still false. The next daily
   observer then treats the missing leader as departure. A harmless native
   dispatch must preserve Franco; explicit native retirement context must still
   conduct the real departure. This is independent of any parser test.

2. **P1 — Rejecting the initial reform permanently blocks its route.**
   The parliamentary-settlement focus is exclusive with both other initial
   settlements. Its `COLDWAR_SPR_political_reform_effect` (`effects:294`) records
   its delivered receipt once. Both rejection options in events .10/.11
   (`events/COLDWAR_SPR_v2_politics.txt:37` and `:45`) only clear reform progress.
   There is no reform-retry decision. Constitutional revision requires
   `settlement_recorded` (`triggers:44`), which is first set only by actually
   enacting a legal package. A player who returns this first agreement for
   negotiation can therefore neither retry reform nor choose the excluded legal
   settlements. Add an actionable retry preserving the approved transaction
   costs, or make returning the agreement actually schedule continued talks.

3. **P1 — Delayed political answers are not bound to the initiating mandate.**
   The events .11 (60-day referendum), .14 (60-day revision), .16 (180-day
   republican vote), .20 (UCD/AP mandate) and .30 (Carlist agreement) neither
   capture the initiating government generation nor recheck it in their
   executable option effects. Examples: .14 (`events:56`) can enact the previous
   cabinet's requested constitutional revision after a government change; an
   already-open .20 (`events:87`) can change the UCD/AP identity after its original
   cabinet loses office; .30 stamps the *current* generation rather than proving
   the one that requested/purchased the talks. A top-level event trigger or an
   option visibility trigger is insufficient for an event left open while state
   changes. Snapshot the party/identity and government generation on request,
   require a live pending receipt, recheck in executable effects and clear
   obsolete transactions. Preserve an explicit harmless lapsed option.

4. **P2 — New-mandate bookkeeping runs at election campaign start.**
   V2 `on_new_term_election` (`common/on_actions/COLDWAR_SPR_v2_politics.txt:15`)
   increments the government generation, removes Carlist agreements and requests
   a conservative mandate immediately. Native
   `common/on_actions/00_on_actions.txt:120` uses this hook to launch
   `MD4_election_campaign.0`, whose campaign begins only when its option is
   selected (`events/MD_Elections.txt:1289`). Thus the old cabinet receives a new
   generation and loses negotiated support before votes or coalition formation.
   Same-party *wins* should still renew the mandate, but only after observing
   real election/coalition completion or a proper native result hook.

The findings were sent to both the root and the political provider's author
before this report was written. Re-read regenerated output after corrections;
line numbers above identify the reviewed pre-correction output snapshot.

## Contracts verified in source

* The shared early route in `00_leader_setup_scripted_effects.txt:58` calls the
  Spanish dispatcher before the generic dispatcher can destroy the incumbent.
  `SPR_political_leaders.txt:4` also routes the 1970 wrapper there. Other starts
  retain their native branch.
* Actual native GUI retirement at
  `00_MD_politicsview_scripted_guis.txt:1085` sets
  `MDCW_HP_native_retirement = 1`, calls `set_leader`, then clears it. The V2
  dispatcher explicitly observes this context. That real retirement route must
  remain distinct from the ordinary callback identified in finding 1.
* The 20 November 1975 engine expiry gap is explicitly handled by an incumbency
  flag and a one-day date fallback. The hard daily upper-bound departure check
  does not depend on Franco's name still being active. This is a sound source
  contract once ordinary dispatch is corrected.
* UCD and AP/PP share native slot 1 and have exclusive mandate flags; all other
  programme families use the real `ruling_party` slot. There is no replacement
  party-popularity or national-election system. Core focus availability and
  programme synchronization call these actual predicates.
* Per-family leader ordinals persist across opposition and same-outlook return.
  The provider can recreate the current known ordinal without consulting the
  just-retired leader's name. Ordinal advancement is specifically tied to actual
  native-retirement context, not every political callback. The current source
  supports same-outlook UCD/AP return; its UI execution still needs an engine
  check, including choosing a different conservative mandate.
* Party legalization clears the real native `partyall_banned` and
  `generic_election_killswitch` flags and resets `party_banned_array` slots 0–23.
  The loop bound matches native `set_partyall_allowed` in
  `00_MD_politicsview_scripted_effects.txt:2162`. It does not invent an unsupported
  all-slots ban or parallel party model.
* The constituent observer uses the actual native `elections_in_progress` and
  `coalition_forming` flags. Native election outcomes clear the former and
  coalition results clear the latter. Waiting for both is appropriate; the
  premature *generation* update is the separate finding above.
* Current Carlist predicates require actual current party and government
  generation, correctly preventing a previously concluded agreement from
  remaining active after a new cabinet. Its request/acceptance transaction still
  needs the stale-answer correction in finding 3.

## Final integration requirements

The root completed retirement and compilation during review. A subsequent source
check confirmed 231 loaded focus definitions, no duplicate custom Spanish
scripted-effect names and no old `COLDWAR_SPR_politics.txt` effects file. The
latest follow-up correction to constituent ratification must be included in the
root's final compile; it was briefly newer in provider source than loaded effects
while its author was finishing the change.

After fixes, verify a fresh 1970 start, ordinary dispatch while Franco rules,
native retirement, engine expiry, returning UCD/AP from another native party,
same-party election renewal, rejected/retried reform, campaign and coalition
completion, stale delayed answers, save/reload and actual focus hovers in HOI4.
