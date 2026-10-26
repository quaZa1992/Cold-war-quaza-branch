# Cold War GCC shared branch

The existing national trees remain the host. Fourteen adapted MD shared focuses
are attached to the 1970 generic tree (Saudi Arabia, Kuwait, Bahrain, Qatar and
Oman) and the UAE tree. The branch uses the original MD relative positions,
prerequisite grouping, icons and durations, with two shorter consultations.
The UAE branch is shifted clear of its national content. The shortcut opens it.

## Historical scope

The six states signed the historical GCC charter on 25 May 1981. Early founding
by two willing independent states is an explicitly alternative development.
British-protected countries must first become independent; the UAE must also
establish its federation through its national tree. Membership requires an
accepted invitation. All fourteen council focuses, including A Gulf Council,
require the actual native `idea_gcc_member_state` spirit and sovereignty.
Charter invitations are independently available to eligible sovereign founders
before the member-only entry focus, so joining never requires already being a
member. The entry focus no longer advertises that existing decision as a reward.

Focus availability keeps internal scenario, host and delivered-parent checks in
`hidden_trigger`; visible requirements show the membership spirit and independence.
The real prerequisite graph is unchanged. Actual reward helpers use the same
membership requirement, so losing the spirit before completion prevents delivery.

Included subjects are economic agreements, regional trade, technical exchange,
investment, payments, roads, defence consultation, Peninsula Shield, officer
exchanges, staff liaison, procurement, contingency planning and council meetings.
The modern customs union, common currency, automatic alliance, foreign hegemony,
puppet demands and annexation paths are omitted. No focus creates units,
guarantees another state's intervention or transfers another player's resources.

The native membership spirit and GCC interface remain available. Native modern
shared-focus completion flags are deliberately never set: they activate automatic
faction and late-accession effects unsuitable for these agreed institutions.
The native modern bloc arms package is hidden only in the 1970 scenario: its
later event would otherwise charge the leading member $25 billion without that
government accepting the purchase. Ordinary native council decisions remain.

## Costs and persistence

Each policy charges the completing country's current annual GDP, between 0.25%
and 2% depending on the institution. Amounts appear through MD's treasury effect.
Focus affordability is not a prerequisite: normal MD borrowing remains possible.
An invitation instead freezes each new signatory's own entry contribution at 2%
of its GDP. Acceptance requires the matching live proposal and sufficient funds.
Existing members do not pay entry again. Invitations cost the sender 50 PP.

Policy modifiers are national and carry administrative, energy or military
personnel costs where applicable. One-time expenditure and training are recorded
once. Loss of sovereignty or membership suspends ongoing contributions and
research exchange; returning restores earned programmes without replaying costs,
experience or grants. Population growth, initial resources and the UAE's paid
development progression are unchanged.

Run `python tools/gcc_1970/compile.py` to regenerate the branch. The UAE attachment
also belongs to `tools/uae_1970/compile.py`; the generic attachment is a bounded
marked splice because its advertised generator is absent in this checkout.

## Primary historical references

- [GCC foundation and charter](https://www.gcc-sg.org/en/AboutUs/Pages/default.aspx)
- [British statement on the Gulf, December 1971](https://api.parliament.uk/historic-hansard/commons/1971/dec/06/the-gulf)
- [GCC economic integration chronology](https://www.gcc-sg.org/en/MediaCenter/DigitalLibrary/Documents/3331355824160.pdf)
- [GCC military cooperation chronology](https://www.gcc-sg.org/ar/JointGulf/Cooperation/MilitaryCooperation/Pages/default.aspx)

Automated checks interpret the emitted script subset and validate references.
They do not substitute for HOI4's loader, native tooltips, save/reload or a live
multiplayer acceptance test.
# UAE focus-only admission integration

The UAE national diplomacy focus uses `COLDWAR_GCC_UAE_can_petition`,
`COLDWAR_GCC_UAE_petition` and the nonexecuting native
`COLDWAR_GCC_UAE_petition_preview`. The helper sends its proposal to Saudi
Arabia, which must actually accept. It supports both an initial charter and
admission when Saudi Arabia already belongs. Only new members pay their own
frozen 2% GDP entry contribution; current members do not pay again. The preview
uses `TT_IF_THEY_ACCEPT` and native numeric money/membership effects.

The common charter decision is hidden for UAE only. The other five founders
retain their existing decision mechanism. Every focus in the shared GCC branch,
including its root, still requires the actual membership spirit.

`test_integration.py` now includes ten groups, including existing-member Saudi
admission, refusal, duplicate/concurrent proposals, native entry-price previews
and invalid sovereign/war/expulsion contexts. Native engine execution remains
outside the interpreter's evidence.

The native GCC membership array is reconciled against actual sovereign member
status for each of the six founders, including native puppet/free hooks. The
1970 startup no longer seeds unsigned states; modern starts retain the original
six-member seed. Existing nonfounder entries are preserved. Tests execute the
real native startup fragment, idea callbacks and exercise-invitation loop.

