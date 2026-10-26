# COLDWAR UAE — starting withdrawal correction: mechanics audit

19 October 2026. Bounded concept review. This document supersedes the new-independence-request requirement in `BRITISH_PATH_MECHANICS.md`; its native API and subject-status evidence remains applicable. No generator or loaded gameplay file was edited by this reviewer.

**Required outcome:** both ENG and UAE begin January 1970 with a visible British Withdrawal Announced spirit and an already active historical withdrawal schedule. The default release is independent of focus completion, a new Emirati petition, a fresh UK acceptance, government/opinion changes, or unanswered diplomatic popups. Only a mutually accepted replacement can change that schedule.

## Historical input and exact date presentation

The companion `STARTING_WITHDRAWAL_CORRECTION_HISTORY.md` verifies the January 1968 announcement of withdrawal by the end of 1971, and the later actual termination of special relations on 1 December 1971. The scenario may execute on that historical date, but must label it **Historical scenario handover: 1 December 1971** alongside **Announced timetable: by the end of 1971**. It must not claim that the exact day was a newly signed bilateral date in January 1970. Federal proclamation is a separate act after actual independence.

The starting record therefore has origin `initial policy`, not `accepted player amendment`. Mirrored national spirits explain the same existing commitment from the two countries' perspectives; they do not invent a new signed independence treaty or additional financial, basing or military obligations.

## Bounded changes to the existing architecture

| Element | Required correction | Preserved behavior |
|---|---|---|
| Initial bilateral state | Initialize one current withdrawal schedule and both starting spirits once in the 1970 setup | Actual native British subject relationship continues until execution |
| `COLDWAR_UAE_petition_independence` | Retain ID/position; rename **Prepare the Handover**. Any offer concerns earlier release or practical handover terms | Mutual exclusion with Renew the Protection and existing geometry |
| Default release consumer | Accept the current initial-policy schedule as well as an accepted replacement; no focus, offer or fresh approval prerequisite | One guarded UK-scoped `end_puppet = UAE` leaf, current nonce/date checks, no duplicate execution |
| Renewed protection | Replace the original schedule only after both countries accept the same current proposal before execution | Existing native puppet costs and accepted protection programmes |
| Pending/refused/expired talks | Leave original schedule and due date unchanged | Retry cooldown and stale-popup protection apply to optional talks only |
| Main British Withdrawal / federation focus | Continue to require `is_subject = no` plus founders' consent | No release effect inside the focus; independent handover is not held hostage to federal formation |
| Spirit lifecycle | Replace both withdrawal spirits together on actual release or mutually accepted renewal | No duplicate Treaty Dependence modifier; subject-only programme contributions stop on actual release |

Change every provider and override: initial node declaration, later offer-dispatch loop, later reward-summary overwrite, status-talk decision, UK policy decision, treaty-amendment eligibility, programme rules and preview text. Updating only the initial node declaration is insufficient because the generator later overwrites its rewards and dispatch metadata.

## Startup and delivery contract

Initialization is a new proposed COLDWAR integration, not an existing native MD helper. Run after the scenario's initial ENG–UAE subject relation exists, guarded by native 1970 scenario status, actual relation, and a persistent initialization flag. Set the initial schedule ID/origin/nonce/due state and mirror the starting spirits only once. A load observer restores missing display state from the current saved record, rather than resetting that record or its date. Initialization must not overwrite a fulfilled release or an already accepted replacement.

The existing scenario creates the subject relation in `common/scripted_effects/IMP_1970_world_politics_effects.txt:1226–1232`. Its global alignment wrapper at 1348–1356 already prevents repeat initial alignment. Do not call the internal world setup on reload or treaty refresh: that would re-create subject relations and unrelated world state.

Use one authoritative due handler for the initial schedule, accepted earlier release and accepted later amendments. A daily country observer plus load catch-up and an optional scheduled wake-up should all reach the same idempotent consumer. Timed-idea expiration alone does not execute independence. Fixed historical maturity uses native `NOT = { date < 1971.12.1 }`; relative accepted terms can use the already traced native `global.date` convention, with a copied 360-day term adding 8.64 and displaying `GetDateStringNoHourLong`.

At delivery, require both countries to exist, actual `UAE = { is_subject_of = ENG }`, a current active schedule and its matching origin/nonce/date. Initial-policy origin must be valid without an accepted-offer flag. A renewed compact that validly replaced the schedule invalidates the old scheduled callback. Silence and refusal do not create such a replacement.

The existing native release leaf remains:

```text
# In ENG scope, only after the current schedule is due:
end_puppet = UAE
```

Installed game `documentation/effects_documentation.md:3662–3670` defines this as ending the current country's subject relation. The subject trigger is native (`triggers_documentation.md:6285–6293`). After actual release, consume the schedule, record fulfillment and actual execution date, stop subject-only contributions, and update both spirits. No new cash, XP, units, resource grants or formation reward is paid by this lifecycle operation.

If already independent, close stale schedule/display state without a second reward. If transferred to another overlord or annexed, invalidate the stale British delivery rather than freeing the country from an unrelated master. The main focus tests **`is_subject = no`**, not merely `NOT is_subject_of = ENG` (native trigger documentation:6276–6284).

## Amendment race and consent rules

An optional early-release offer or handover discussion can be refused while the default historical withdrawal remains fully active. The 180-day retry limit governs a new offer, never the baseline schedule. An accepted handover detail that does not change sovereignty/date also leaves the baseline intact.

A valid renewed-protection acceptance replaces the current schedule and mirrored spirits atomically, with a new nonce. Require actual British subject status and an unexecuted current record when accepting. Once the default due date has arrived, a stale offer must not retroactively postpone release: execute or recognize the due baseline before accepting an incompatible late renewal. After actual independence, any new subject relationship would require a different explicit agreement; friendship alone creates none.

The renewal's review date remains a review date rather than automatic independence. Conversely, a current release deadline remains binding through subsequent government/opinion changes. Neither party receives a new unilateral veto at maturity.

## Acceptance checks for the emitted revision

1. New 1970 game, no British focus or decision selected: both spirits appear and the default schedule executes once on its due date.
2. Prepare the Handover completed, earlier-release request refused or ignored: baseline date and automatic release remain unchanged.
3. Renew the Protection completed, no UK acceptance: same baseline result; no loyal programme activation merely for sending the proposal.
4. Valid bilateral renewal before maturity: original callback becomes stale; continued protection and both replacement spirits persist under the accepted terms.
5. Saved/reloaded before or after maturity: no date reset, duplicated release, re-puppeting, cash or permanent-gain replay.
6. UK government/opinion changes: no fresh approval needed for the unchanged baseline.
7. UAE already free or under another overlord: cleanup/current-status handling is safe; the federation focus still requires actual full independence.
8. Release completed without any federation focus: actual independence holds, founders' institutional choices remain separate, and the expired Council character does not itself form or release the country.
9. Stale renewal popup accepted after due date or after a newer agreement: nonce/date/status guards prevent retroactive postponement or overwrite.
10. All unrelated focus/effect records and the low-oil investment programme match the prior preservation baseline.

## Preserve the dependency contribution when the display changes

The emitted starting spirit retains `political_power_factor = -0.10` under the exact active condition `is_subject_of = ENG`. Its treatment explicitly reuses the existing `COLDWAR_UAE_treaty_dependence` ID and replaces its visible terms after an accepted compact. The final `british_treaties.spirit_implementation` now also explicitly requires preserving this contribution exactly once throughout continued British subject status, including renewed protection. Removing the initial displayed withdrawal idea must not silently erase the penalty; adding a compact must not duplicate it.

Implementation must either retain/relabel the existing mechanical carrier or move the same contribution atomically to the compact's carrier. A separate relation-conditioned dynamic modifier is also valid if only one provider remains. The initial and replacement treaty displays may differ; their underlying actual-subject condition remains authoritative. Deactivate the contribution on actual British release or a different actual overlord, rather than on focus completion, signed renewal or the main federal proclamation.

## Optional route after missing all opening focuses

Automatic release already leaves the main federation focus reachable independently of the British branch. The earlier optional Orderly Handover route required one of the opening policy focuses, whose root and choices were subject-only. A player doing no British focus before release could therefore have missed the optional handover/friendship programme. The final emitted correction resolves this edge case.

The final fallback bypasses only the non-exclusive Protected Coast root after actual `is_subject = no`, with an explicit no-fee/no-reward contract, and allows the player to choose Prepare the Handover voluntarily after independence. Its native availability is `OR = { is_subject_of = ENG is_subject = no }`, which excludes subjects of other overlords. The effect body sends an early-handover offer only inside `if = { limit = { is_subject_of = ENG } ... }`; after independence it prepares domestic handover work without asking for release again. Renew the Protection remains subject-only. Neither exclusive choice is bypassed or automatically selected. Native MD uses an independent-status focus bypass in `common/national_focus/05_libya.txt:12590–12591`.

This preserves access to optional programme rewards without making baseline release or the main federation gate depend on that preparation. The existing Orderly Handover prerequisite accepts either voluntarily completed policy choice; its actual-independence condition then opens the follow-up and later friendship offer.

## Emitted-model review status

**Final verdict: passed the bounded starting-withdrawal correction review.** The final canonical model and both preview data models agree; no blocking mechanics issue remains in this concept revision.

- Canonical JSON: `23e89bc7f0a02f4df337248bcfa67d139ec8fc910c414978a3f5ef5913158272`.
- 107 focuses / 40 decisions. All 97 unrelated focus records match `BRITISH_PRESERVATION_BASELINE.json` exactly under its recorded field set.
- `starting_state` explicitly requires no focus or new UK acceptance, records the 1968 origin, starts both spirits, initializes once and names 1 December 1971 as the historical scenario execution.
- Prepare the Handover retains its ID and geometry, dispatches `early_handover`, and explicitly preserves the original schedule on refusal or silence.
- The release consumer accepts the current starting schedule or mutually accepted replacement, checks actual British subject status and uses the native UK-scoped release leaf. Late renewal cannot postpone an already due baseline.
- The main focus still requires actual independence and founders' consent; no British focus prerequisite or second release effect was introduced.
- Both embedded preview models equal the canonical JSON after removing their preview-only assets. Final preview hashes: `a78734fbd3c7b86f279a7ff53bddf121e65f2f76741359ac53fff04a6bb78641` (repository) and `00c6d885082e58fa2159f17cb36667c07861bab7ff783ac9103d19c95f302a46` (inline).
- The missed-opening-focus fallback and the single dependency-penalty carrier are explicitly represented as described above. The root bypass grants nothing and neither exclusive choice is automatically selected.
- Amend the Withdrawal Terms now explicitly accepts the starting schedule or an accepted replacement; it requires no new signed treaty before the baseline can be discussed. Orderly Handover now describes release through the existing schedule or accepted earlier release.

The main formation reward still says a pending or refused UK request is insufficient. In context this is a true actual-status reminder, not a request prerequisite: its only diplomatic condition is actual `is_subject = no`, and normal historical release explicitly requires no request. The retained `petition_independence` ID is an intentional compatibility identifier; its title, dispatch kind, effect wrapper and reward text all implement preparation/optional early handover.

These checks establish source/model consistency, not installation or engine execution. New bootstrap, schedule, synchronization and nonce consumers remain explicitly proposed COLDWAR integration work.
