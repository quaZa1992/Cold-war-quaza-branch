# COLDWAR Iraq 1970: implementation

The audit revision is installed as `COLDWAR_IRQ_1970_focus`: 410 active Iraqi
focuses in 23 chapters, retaining all 426 IDs through 16 hidden, empty legacy
entries. Its coordinates, prerequisites, exclusions, durations and rewards
follow the approved 19 October audit. The existing USA tree receives 15
registered Gulf/northern Iraq IDs, 14 active, at x30–38; its original 214
focuses retain their existing definitions.
All new in-game localization is English. New content uses the `COLDWAR_` prefix.
See [the current implementation and checks](../audit_2026_10_19/IMPLEMENTATION.md)
for exact packages, current contracts, migration and actual test boundaries.

The January 1970 start uses Ahmed Hassan al-Bakr and seven situation cards.
The dated country history seeds ordinary national ideas directly, so their
starting attachment no longer depends on pressing Play or the daily callback.
Reforms select one native idea stage per burden; the six former dynamic
starting cards are detached from existing saves to prevent double application.
The literacy marker uses MD's actual education system rather than applying a
second research or education-cost penalty.
Earned party and leader programmes suspend when their exact government or
office-holder leaves, and restore on a qualifying return. Buildings, literacy,
resources, claims, money and cores are one-time deliveries. Rebuilding derived
programme values cannot repeat these rewards. Policy reviews select programmes
without rerunning original physical rewards. Positive policy stability is
capped at fifteen points; negative contributions and starting burdens remain.

Modifier-bearing focuses show native MD programme headings and coloured
numeric modifier tooltips. Starting-spirit reforms preview actual idea changes.
Availability lists the governing historical party, any required office-holder,
implemented prerequisite reforms and current agreements separately. Preview
blocks do not execute rewards; the guarded transaction remains the sole grant.

All 426 English focus descriptions now use national policy narrative modelled
on normal main MD 2000 examples. The two `flavour_*.json` files remain the base
editorial overrides; `audit_design.py` and `audit_rewards.py` apply the approved
revision without changing the frozen original catalogue. Paid-focus previews
use native signed treasury amounts, calculated
from current GDP until a quote exists and from that stored quote afterwards.
Decision unlocks and spirit changes use native tooltips, without per-focus
invoice/queue essays. Actual guarded payments and one-time delivery receipts
execute the current audited packages. Historical party names and icons reuse
the shared curated presentation, without invoking its installer.
See `MD_RUSSIA_2000_WRITING_REFERENCE.md` and the writing/presentation reports.

Duplicate predecessor-receipt checks are hidden in focus availability because
the native prerequisite graph already shows those edges. Pending-project
decisions retain readable delivery conditions. The shared presentation helper
also applies to the Greek, Cypriot and Vietnamese generators; its scan report
is `tools/focus_prerequisite_ui_report.json`. No gate or reward was removed.

An existing 1970 save is reconciled on its first daily tick after loading.
Successful delivery receipts restore missing programme/unlock metadata without
replaying money or assets. A completed focus without a delivery receipt enters
its pending-project decision instead of receiving unverified free rewards.
Fully restart HOI4 after installing the scripts and English localization.

National projects freeze their stated GDP quote once. Delivery checks funds,
government, implemented prerequisites, agreements, state ownership/control and
native building capacity before charging. A blocked delivery has its own
start-accessible retry decision. The queue overview never purchases all projects.

The Iranian campaign provides a Khuzestan claim and explicit war goal, two
operational approaches, paid offensives and occupation/integration choices.
Khuzestan requires 730 consecutive days of ownership/control, peace with Iran,
infrastructure 3, compliance 60 or higher, resistance below 15 and its 6%-GDP
invoice before receiving an Iraqi core. Other countries' cores remain.

Real war with Iran applies one replacing military-cost tier: army personnel
+100% / native equipment operating costs +50%, then +175% / +100% at 180 days,
then +250% / +150% at 365 days. The native equipment component includes deployed
land equipment and discounted stockpiles. Normal MD weekly accounting and
deficit borrowing remain the cash/debt charger. Paid temporary campaign
preparations and their remaining personnel obligations are additional costs.

An actual long war and substantial net new borrowing can produce The Price of
Victory: construction −30%, tax revenue −20%, stability −10 points, interest
+2 points and consumer-goods burden +20%. The consumer-goods number is a relative
MD tax-cost expectation modifier, not twenty percentage points of tax.

Kuwait, Saudi Arabia and the UAE receive their own private credit responses.
Accepted loans debit the actual lender, credit Iraq and record native debt and
the specific principal once. Repayment transfers real money. Native aggregate
repayments whose creditor is unknown conservatively retire Gulf principal first;
known authored non-Gulf transactions update the separate protected balance.
Kuwait forgiveness only cancels its surviving recorded principal. Other native
debt remains. The postwar crisis, creditor refusal/oil dispute, ultimatum,
conquest relief, bounded treasury seizure and paid stable integration form the
Kuwait route. Both Kuwaiti states can become Iraqi cores after the integration
conditions have actually been met. The rejected 1985 credit system is not a
provider for this 1970 package and remains gated to its separate scenario.

The USA can obtain its Iraq liberation goal through the 14-day Desert Storm
focus after an actual Iraqi attack on Kuwait. War declaration remains a player
action. Northern content uses recipient consent, actual cash and equipment,
native resistance on specified Kurdish cores, expensive Iraqi countermeasures,
a bounded uprising coordinator and a new Iraqi-overlord autonomy definition.
Northern Air Shield uses real interception/superiority and local-recipient
damage-reduction modifiers with personnel costs. It requires real consenting
access and forces; it does not implement a geographic flight prohibition.

Party organization uses MD's existing party arrays and outlooks. The important
Iraqi families occupy native slots 2,3,4,6,8,9,12,18,19,21,22,23. PUK uses native
nonaligned communist slot19; this is an explicit implementation mapping for its
previously unspecified slot. PUK and SCIRI require their actual formation.
Candidate survival after contingent historical repression needs earlier
protection. Known dead candidates cannot return through an ordinary refresh.
Where an identified historical portrait is unavailable, the native generic Arab
portrait is used as a placeholder. The supplied Saddam artwork is a focus badge.
The 35% literacy input is a proposed balance baseline, not a verified census
statistic; an existing literacy value is preserved. Iraq is enrolled in native
MD annual literacy updates without resetting its education progress.

## Reproduce and review

Run from the mod directory:

```text
python tools/iraq_1970/compile.py
python tools/iraq_1970/validate.py
python tools/iraq_1970/test_core.py
python tools/iraq_1970/test_starting_spirits.py
python tools/iraq_1970/test_presentation.py
python tools/iraq_1970/startup_patch.py
python tools/iraq_1970/gulf_module.py
python tools/iraq_1970/test_usa_module.py
python tools/iraq_1970/test_decisions_module.py
python tools/iraq_1970/render_installed.py
```

The compiler reads the immutable `tools/iraq_1970/approved_iraq.json` and the
reviewed provider modules. `manifest.json` records generated hashes and nine
narrow native adapters. Their first baseline copies live under
`tools/iraq_1970/integration_baseline`. Shared edits cover Iraq history/fallback,
native leader routing, party-name display, subparty callbacks, USA attachment
and the northern resistance90 coordinator guard. The old Iraq provider's
commented-out final brace was repaired as part of the necessary wrapper.

`VALIDATION_REPORT.json`, the component test reports and
`INSTALLED_RENDER_REPORT.json` distinguish static execution, source preservation
and visual checks. The PNGs use installed coordinates/art/native bitmap font;
their connector routing approximates the engine. `ENGINE_REPORT.json` records
an earlier isolated engine-loader attempt using a separate user profile.
`ENGINE_RUNTIME_REPORT.json` records a successful current-manifest native1970
startup, seven active starting cards, one real focus completion and government
programme departure/return without stacking. The test addon is isolated from
the user's playset. Native hover, long-term budget accrual, combat, save/reload,
AI and multiplayer acceptance still require live gameplay testing. Existing errors in
unrelated mod files are recorded separately, not silently included in a clean
whole-mod claim. These changes do not repair the rest of the mod.

See [USA implementation](USA_GULF_IMPLEMENTATION.md),
[verification and remaining engine limits](VERIFICATION.md),
[installed layout report](INSTALLED_RENDER_REPORT.json),
[Iran branch](IRQ_NATIVE_iran_war.png) and
[USA chapter with existing neighbours](USA_GULF_WITH_EXISTING_DEFENCE.png).
