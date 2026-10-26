# Cold War adapter: post-Soviet Buran preservation

The native Millennium Dawn mission `SOV_buran_hangar` previously activated whenever the original tag was SOV and the preservation storyline had not finished. It had no start-bookmark or calendar gate. Its 862-day timeout therefore ran in the January 1970 campaign, too. An unfunded timeout called `russia.304`; accepting that event removed 5 percentage points of stability and 100 political power, then dispatched `russia.3044` six hours later. The post-Soviet hangar collapse was thus transplanted into the early 1970s.

The entire bounded preservation family is unavailable in a campaign whose actual start date is 1 January 1970. This uses the existing `IMP_is_1970_scenario` provider, which checks the bookmark start date, so advancing the calendar never re-enables this story in that campaign. Modern starts retain the original requirements, fees, random outcomes, rewards and timing.

## Changed content

- Six native decisions: `SOV_buran_hangar`, `SOV_begin_funding`, `SOV_dissassemble_the_shuttle`, `SOV_build_hangar`, `SOV_make_repairs_at_temp_hangar`, `SOV_announce_full_restoration`.
- Nine native events: `russia.200`, `.300`, `.301`, `.302`, `.3022`, `.303`, `.3033`, `.304`, `.3044`.
- Loaded source anchors: `common/decisions/Russia.txt:5586`, `events/Russia.txt:7929`, `events/Russia.txt:7954`.

The mission cannot activate in 1970; a previously active mission cancels without a cancellation reward or penalty. All existing mission/decision completion and timeout effects independently check the scenario before executing, including already-running programmes in old saves. All nine events have an entry trigger; every effectful event option independently checks the scenario, so an already-open old collapse event cannot remove stability or political power, grant preservation rewards, set preservation receipts or dispatch another news event after the update. An already-rendered popup cannot be removed retrospectively by changing script files.

The native MD files have no local generator. `buran.py` is the canonical, idempotent adapter for those two files; rerun it after refreshing native MD content. It preserves BOM and newline format. It does not rebuild the Soviet focus generator or overwrite other events.

## Adjacent mission and event audit

All five timed missions in the native `common/decisions/Russia.txt` were inspected:

| Mission | Entry requirement | Finding |
| --- | --- | --- |
| Buran hangar | Original SOV tag and unfinished story | Confirmed automatic anachronism; fixed with the entire associated family. |
| 500 Days ticker | `SOV_capitalism_in_500_days` completed | Modern national-focus programme; not an automatic tag-only startup story. Unchanged. |
| National Projects ticker | `SOV_npp` completed | Modern national-focus programme; not an automatic tag-only startup story. Unchanged. |
| Centre to Regions ticker | `SOV_from_center_to_regions` completed | Modern national-focus programme; not an automatic tag-only startup story. Unchanged. |
| Reunification mission | Explicit activation by paid country-specific talks; then self-refires | Political gameplay after a deliberate action, not automatic historical flavour news. Unchanged. |

The additional MTTH-bearing native Russian corporate-scandal events require modern corporation focuses and are triggered-only; they do not reproduce the tag-only Buran startup defect. Native general news collections use political/event callers rather than this Buran mission and were not globally disabled. This is a bounded caller-chain and neighbouring-mission audit, not a claim that every MD event has been reviewed.

The custom `COLDWAR_SOV.4` event (`events/COLDWAR_SOV_1970_events.txt:59`) is an alternate Soviet lunar landing, authored by `Claude outputs/COLDWAR_SOV_generator/cw_events.py`. It reuses a Buran picture but contains no call to the native Buran family. Its gameplay was retained; artwork is a separate issue.

## Validation

Run `python tools/modern_news_1970/test_buran.py`.

The 45 source/AST checks cover all six decisions, nine event entry gates, effectful options, cancellation without penalties, guarded legacy timeouts and courses, and idempotent installation. Projecting the new scenario guards away for a modern campaign yields exactly the original full-file AST from Git HEAD in both files; this also checks that unrelated political content remains unchanged. No live HOI4 save or popup was exercised.
