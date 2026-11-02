IMPERIA COLD WAR: USA focus calendar restrictions

24 October 2026. Bounded implementation support for the user's explicit instruction to remove arbitrary focus time restrictions. The new module and tests do not write loaded runtime files, launch the game, change the main compiler or modify immutable design/source records.

## Result and exact scope

`tools/usa_1970_expansion/focus_dates.py` supplies pure in-memory compiler hooks. The reviewed input tree has 281 focuses and SHA256 `cde668bd4b711a14a7cfe07f63c8fbe6c492d50b313ec3f0034430a29783d380`.

- Remove 64 date comparisons from ordinary focus availability, including the Nixon programme's 20 January 1973 cutoff and the D0/D1/D2 opening dates.
- Remove the matching 64 date comparisons from 53 real execution/retry helpers: 51 legacy ready helpers and the two reworked domestic force-model helpers. Updating only the visible tree would leave those execution vetoes in place.
- Detach 30 paid programme entries from historical election-result prerequisites. Their exact native governing-party requirements remain; all subsequent policy prerequisites and choices remain.
- Preserve all 14 automatic election-result cards byte-for-byte. Their `always = no`, dated bypass windows and opposite-result tests stay intact. Future victories do not automatically complete in 1970.
- Preserve costs, rewards, coordinates, exclusions, buildings, control/capacity, receipts, law, Congress, membership, peace and consent conditions. No reward or balance amount changes.

All 267 ordinary focuses have no remaining availability date comparison after the in-memory transformation. An independent transitive walk through 377 reachable scripted-trigger providers found zero remaining calendar comparisons after applying the corresponding ready-helper transformation. Before transformation, every dated reachable scripted trigger belonged to one of those 53 known ready helpers. No additional shared MD helper needs rewriting for this current source.

Complete per-focus and per-helper records, input hashes, in-memory transformed hashes and immutable-record hashes are in `implementation_support_focus_dates.json`. The transformed hashes identify a proposal in memory, not an installed build.

## Why election receipts require separate handling

The existing zero-cost victory cards are historical records, not selectable party policies. Their availability is always false and their bypass requires the appropriate inauguration window and actual party. Removing their dates would assert every Republican victory in 1970 when the Republicans govern, or the equivalent Democratic victories after a party switch. That would change election history rather than merely unlock policy.

Ordinary programmes now depend on the actual governing party and their real policy chain. Only direct prerequisite groups consisting entirely of historical victory receipts are removed. Current source has no mixed receipt/policy OR group. The hook deliberately refuses such a future group rather than silently changing its meaning. The result preserves policy-to-policy AND/OR dependencies while leaving election records separate. Coordinates remain unchanged, so the old result-to-entry arrows disappear; no layout movement or new unlock focus is introduced.

Common enacted-law focuses retain their existing policy-chain prerequisites. A government cannot obtain them simply because a date restriction was removed. Active party-programme cleanup and one-time completion receipts are unaffected.

## Genuine chronology retained

The existing `USA_1970_nixon_presidency` flag remains the actual Nixon requirement. The first-term cutoff is removed, so a continuing Nixon presidency can pursue its programme after 20 January 1973. Losing the presidency still fails the condition.

Pentagon Papers, `USA_1970_NIX_A5`, retains the real `USA_1970_pentagon_papers_published` state. Its previous extra release-date threshold and date-only fallback are removed. In particular, `OR = { publication flag date fallback }` becomes the actual publication requirement, rather than `always = yes`. The historical publication event stays scheduled by `USA_1970_initialize` at `common/scripted_effects/USA_1970_scripted_effects.txt:39`; `events/USA_1970_nixon_events.txt:21` remains the flag provider. Thus this event response still follows its event, not an arbitrary independent focus timer.

`USA_1970_set_scenario_leader` at `common/scripted_effects/USA_1970_scripted_effects.txt:243` retains its dated leader selection. Existing election events, event scheduling, leader identity changes, agreement mandates and their real duration/cooldown flags are not touched by the hooks. No broad search-and-delete is applied to calendar predicates elsewhere in the country.

## Integration hooks

Import the module from the canonical coordinator. The coordinator retains all write ownership and native formatting/encoding handling.

1. After constructing the complete tree, call `tree = focus_dates.patch_focus_tree(tree)`.
2. Before emitting the legacy trigger dictionary, call `triggers = focus_dates.patch_trigger_bodies(triggers)`. This changes only `COLDWAR_USA_legacy_ready_*` and `COLDWAR_USA_dom_ready_*` bodies.
3. For the domestic module's emitted trigger text, call `focus_dates.patch_ready_triggers(text)` on `common/scripted_triggers/COLDWAR_USA_1970_programmes.txt`. This is necessary because `domestic.py:355` restores frozen original availability to the D1/D2 real ready guards. That original chronology remains in the immutable inventory but must be removed from emitted execution conditions under the user's new instruction.
4. Before writing the original English provider, call `loc = focus_dates.patch_english_localisation(loc)`.

Alternatively, pass the four target text records to `patch_outputs(mapping)`. Other paths are returned unchanged. This wrapper does not read, write or launch anything. `patch_trigger_bodies` is also available for canonical dictionary generation before a file exists. No change to domestic/agreement setup payments, migration or reconciliation is required.

Two English overrides correct obsolete restrictions:

| Key | New text |
| --- | --- |
| `USA_1970_nixon_first_term_tt` | `Nixon is President.` |
| `USA_1970_nixon_shortcut` | `Nixon Administration` |

Historical Act names and their descriptions retain their names. No current English focus description states an additional enforced opening date after these two requirement/navigation corrections.

## Native MD reference and source review

The actual main MD donor is version 2.0.2 at `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`. Its `common/national_focus/05_usa.txt:374` administration entry separates ordinary focus availability and automatic bypass, with the native exact-party trigger at line 391. The current user instruction overrides its calendar policy for selectable US programmes; it does not authorize replacing native election results or government succession.

The existing native party providers in `common/scripted_triggers/01_political_triggers.txt:176` and `:183` check `ruling_party` slots 1 and 2 and supply the normal MD party-name tooltips. The hook retains those providers rather than inventing party labels or using broad outlook conditions. It adds the same native trigger only if a receipt-independent programme entry did not already contain it.

The legacy compiler copies frozen focus availability into real ready conditions at `tools/usa_1970_expansion/compile.py:158`. The domestic compiler does so independently at `domestic.py:355`. Both are covered. Actual completion and recovery decisions call those ready helpers; no separate date comparison was found in their real effects or decision execution. The existing Nixon diplomacy sender helpers have no independent date veto. All reachable custom availability helpers, including new spec providers and membership checks, were included in the transitive trigger inventory.

## Verification and evidence limits

`python tools/usa_1970_expansion/test_focus_dates.py` passes 12 tests. Tests read the loaded source and never invoke a compiler or game process. They cover all 281 IDs, all 14 unchanged election cards, ordinary graph/effect/cost/coordinate preservation, party entry gating in 1970, D0, Nixon after the former cutoff, actual Pentagon Papers publication, force law/Congress conditions, real ready helpers, retry receipt/party guards, empty boolean/tooltip groups, mixed prerequisite refusal, idempotence, English text and unchanged leader/event chronology. File writes are explicitly blocked during the pure output-hook test.

These source/model checks do not prove a native focus click, current-save UI refresh or multiplayer synchronization. The parent must integrate and validate the emitted result. No running game was disturbed by this task.
