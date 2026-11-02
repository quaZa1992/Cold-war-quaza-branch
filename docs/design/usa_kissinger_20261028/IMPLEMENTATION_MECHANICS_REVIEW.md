IMPERIA COLD WAR

# Kissinger implementation: independent mechanics reference review

Reference review started 2026-10-28. This reviewer owns this note only. No
gameplay provider, country, state, approval, binary asset or test profile is
changed by this review. A final emitted-code review will be appended when the
implementation owner supplies its completed output.

## Review boundary and approved model

The requested implementation is the complete Kissinger design in `DESIGN.json`,
including the revised simple campaign in `SIMPLE_CAMPAIGN_REVIEW.json`. Its
visible interface has one regional unrest bar, three defender policies and a
mobilisation warning. Funded troop deployment and investment accumulate lasting
stabilisation. Withdrawal removes immediate troop pressure but does not erase
the accumulated reserve; unmaintained gains decay gradually. Funding is a
standing weekly commitment rather than an automatically expiring 90-day purchase.
The reserve and coefficients are project design values, not native modifiers.

## Safe country identity and geography

The implementation owner selected three unused static authority tags. The
current tag declarations contain no KPT, KPI or KPS; KIR is already Kiribati and
must not be used. Static new histories avoid copying a human Kurdish player's
treasury, flags, technology or leadership into another theatre.

| Host | New authority | Sole initial eligible state | Verified source details |
| --- | --- | ---: | --- |
| TUR | KPT | 162 | `162-Turkish Kurdistan.txt`: owner TUR, explicit 1970 owner/controller TUR; includes Diyarbakir 4512, Hakkari 1463, Batman 12387 and Siirt 10497. |
| PER | KPI | 408 | `408-Kordestan.txt`: owner PER, explicit 1970 owner/controller PER; includes Sanandaj 16216, Saqqez 4943 and Marivan 14313. |
| SYR | KPS | 193 | `193-Hasakah.txt`: owner SYR, explicit 1970 owner/controller SYR; includes Qamishli 1549 and Hasakah 3129. This is a mixed Jazira administrative area, not an exclusively Kurdish state. |

The Syrian case must be named and described as a contested Jazira regional
authority. No ethnic claim to all eastern Syria follows from it. The current
map contains no separate small Afrin or Kobani state. Do not transfer 566 Aleppo
or 191 North Raqqa to approximate those towns. Their ownership, cities and
population would exceed the reviewed local movement. Similarly, Iranian state
979 includes Urmia and Miyandoab as well as Mahabad; it is excluded. Iranian
1139 Kermanshah and Turkish 935 Van remain outside the selected minimal scope.

Before each actual uprising, recheck the original host's ownership AND control,
the active armed mobilisation, final warning, funded commitment and available
rebel identity. Add the new authority's core only to the one rising state at
birth; retain the original host core. Do not call `release` on KUR/PUK and do
not enumerate all their cores. Iraq retains its separate bounded KUR/PUK
geography, formation and real recipient-consent rules.

The documented `transfer_state` effect runs in COUNTRY scope and sets both
owner and controller. Thus `KPI = { transfer_state = 408 }` is the supported
bounded owner/controller transfer once all uprising conditions have succeeded.
`set_capital = { state = 408 }` then uses an actually owned state. Existing Iraqi
donor code uses the same bounded transfer model.

`start_civil_war` is documented with explicit states and separate army/navy/air
ratios, but it also divides national forces and stockpiles. It is inappropriate
as a shortcut for these small locally funded authorities. `create_dynamic_country`
is documented and present in MD donors, but its `copy_tag` inherits unspecified
country data and dynamic identity. A static new authority is easier to audit
and does not risk copying an existing human player.

## Minimal own-country initialisation

`civil_war_replication_effect` in `00_scripted_effects.txt` explicitly copies
`PREV.treasury` and political/influence configuration. It must not be used.
The broader `ingame_startup_nations_effect` is also not neutral: it may inherit
PREV technology and GDP-convergence settings, while its fresh-nation branch
grants starting utility equipment, including a baseline 100 convoys. Neither
belongs in an unqualified new rebel spawn.

The following is a candidate for a newly created KPI AFTER the state transfer,
core assignment and own history/law setup. Replace only tag/state/receipt for
KPT and KPS. It uses existing MD helpers and actual native party slot 18,
`neutrality` outlook with `neutral_Social` subideology. This is an institutional
regional administration, not a claim that an invented famous leader held office.
Do not call it again after real aid has arrived.

```text
KPI = {
    if = {
        limit = {
            exists = yes
            408 = { is_owned_and_controlled_by = KPI }
            has_country_flag = COLDWAR_USA_kissinger_new_authority
            NOT = { has_country_flag = COLDWAR_USA_kissinger_authority_initialised }
        }
        set_capital = { state = 408 }
        set_variable = { treasury = 0 }
        set_variable = { debt = 0 }
        set_variable = { int_investments = 0 }
        set_variable = { nation_to_copy_from = 0 }
        set_variable = { corporate_tax_rate = 20 }
        set_variable = { population_tax_rate = 20 }
        set_variable = { domestic_influence_amount = 100 }
        set_popularities = { neutrality = 100 }
        set_politics = { ruling_party = neutrality elections_allowed = no }
        start_politics_input = yes
        set_variable = { party_pop_array^18 = 1 }
        set_variable = { ruling_party = 18 }
        startup_politics = yes
        setup_employment_variables = yes
        set_law_vars = yes
        currency_startup = yes
        ingame_update_setup = yes
        set_variable = { last_quarter_gdp_total = gdp_total }
        set_variable = { last_quarter_gdpc_total = gdp_per_capita }
        set_country_flag = COLDWAR_USA_kissinger_authority_initialised
    }
}
```

Required surrounding setup: own country definition with Kurdish donor graphical
cultures `middle_eastern_gfx` and `middle_eastern_2d`; own zero-cash/debt history;
empty land/naval/air OOBs; appropriate basic 1970 technology; explicit modest law
ideas and currency. Do not set a borrowed national treasury or give the region
an arbitrary GDP balance. GDP must subsequently reflect actual controlled
population, buildings and productivity. The tax values above are the existing
MD employment-helper defaults, not a newly researched regional tax programme.

`setup_employment_variables` reads `nation_to_copy_from`; zero ensures the own
default branch. `start_politics_input` sizes and clears the native 24-slot party
arrays, and `startup_politics` consumes the authored native slot. `set_law_vars`
is appropriate once after initial history laws. Do not use it repeatedly after
budget policy changes. `ingame_update_setup` refreshes state aggregates before
income/expense calculations and performs no direct treasury grant. Initial aid
must arrive after this once-only zero initialisation, not before it.

The native weekly action calls the broader startup helper if
`last_quarter_gdp_total` is missing. Therefore the narrow helper must set that
receipt during birth, rather than waiting for a later weekly economic refresh.
Otherwise the generic fresh-country branch can still grant its starter convoy
stockpile. The collections used by the economy are native
`game:all_countries` and `game:scope` with `controlled_states`; no manual country
registration is required for those two collections. Controlled-state productivity
and the 1970 GDP anchor travel with the actual state and are recomputed for the
new owner. After the first own-state refresh, set `gdpc_converging_var` to the
authority's own `gdp_per_capita`, matching the existing 1970 GDP setup convention.
For a playable authority's own UI, the audited non-copying helpers also include
`init_auto_influence_array`, `ingame_init_investment_system`,
`research_slot_init_for_country` and `setup_init_factions`. The latter consumes
only the authority's own ideas. These are explicit additional lifecycle choices,
not evidence that the short fiscal candidate initialises every MD subsystem.

For a minimal two-battalion column, `Militia_Bat` requires 150 men per battalion
in `common/units/MD_land_units.txt`, hence 300 men in total. The native creation
effect supports an OOB division string, explicit owner and a controlled spawn
location. Existing Iranian donors use `start_manpower_factor`; use a zero-manpower,
zero-equipment initial shell if the implementation intends normal reinforcement
from the new country's actual core manpower and funded cache. Do not inject
300 free manpower or copy host formations. The exact empty-unit survival and
reinforcement transition require a native observation before claiming it works.
The docs do not establish whether a full-strength `create_unit` independently
debits manpower, so do not both assume that debit and script another debit.

## Native military, money and consent scopes

`num_divisions_in_states` is a COUNTRY trigger with `count`, `states`, and
optional `types`/`exclude`. It counts divisions; it is not a strength, equipment
or supply weighted measure. The existing Iraqi donor uses `count > 1` on its
four-state set and a sustained deployment counter. The new theatre must count
the defending host's units in its own selected state, not US troops or another
target's units.

Equipment is native COUNTRY stockpile accounting:
`add_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 }`
debits the actual sponsor. A positive amount belongs to the actual new recipient
only after birth, once, from a finite previously debited cache. Native docs
allow an amount variable. The cache is not equipment already owned by an absent
country. Do not clone a 1,000-item cache for every theatre from one debit.

Native `modify_treasury_effect` uses the country in scope and the temporary
`treasury_change`. Therefore a host defence invoice belongs inside the original
host country, while US support belongs inside USA; temporary-value evaluation
and a scope hop must preserve that payer. Standing costs use the weekly MD
accumulators and must stop with the actual suspended programme. Do not implement
the same commitment with both a daily debit and a weekly expense stream.

Transit/basing governments and existing local Kurdish players accept their own
offers. The defending host does not consent to covert pressure against itself.
Hostile operations against Iran or Turkey retain their explicit alternative
foreign-policy gates and diplomatic consequences. Iraq's existing northern
settlement must continue to suppress grievance rather than silently restarting
the older and newer systems against the same state.

## Existing framed event picture and full donor window

`GFX_political_deal`, registered in `interface/MD_eventpictures.gfx`, resolves to
`gfx/event_pictures/generic/elections/political_deal.dds`. The loaded asset is
byte-identical to main MD, 217 x 163 RGBA, SHA256
`ad09f566f836ec2f5fae2906818fbca58df1dfe723ca5233ec7aa5d858f8f62c`.
Its already available reference PNG at
`tools/event_art/source/MD_country_event_frame_reference.png` is pixel-identical.
Visual inspection shows a parliamentary/council negotiating scene, suitable for
institutional approval or agreement events. It is not an arms-action photograph.
No new bitmap or composition is necessary for that use.

The inspected main-MD `EventWindow` is 581 x 427. Its bottom window is at y221,
height206; `event_picture` is x5/y5. The adjacent options grid is x215/y-1 with
width300, nominal height30 and 300 x 47 slots, one slot horizontally. The native
asset alpha bounding box is x14/y2 through x204/y162; the visible picture ends
at x209 after placement, before the options at x215. The 180 x 150 photo inset
at x19/y6 and all outer-frame pixels remain unchanged. This is a donor-window
and asset inspection, not a live screenshot of a new Kissinger event.

## Native MD references inspected

Main MD descriptor currently declares 2.0.3; target supports HOI4 1.19.*.
References below are mechanical/presentation comparisons, not political
templates or unconditional examples to copy.

- Russia `SOV_empower_siloviki`, cost5, exact-party and security-institution
  requirements: native dynamic-modifier heading, +5% intelligence network gain,
  +5% root-out-resistance effectiveness, +6% foreign-influence defence and a
  separate land-defence supplement. The actual dynamic modifier maps those
  variables to their native keys. Its English description explains the security
  officers' institutional role. Use this heading/numeric grammar, not a prose
  replacement for executable effects.
- Israel `ISR_intelligence_sharing_jordan`, cost2: existing Jordan, peace and
  Jordanian opinion above24; real recipient event `israel_economy.137` has
  accept/refuse options, an actual recipient $10 billion payment and a named
  intelligence-protection spirit. `ISR_covert_ties`, cost4, sends that event to
  eligible Gulf partners. The focus description explains the diplomatic purpose.
  Its old tooltip is not a full prospective numeric contract and must not be
  copied as compliant with current Imperia requirements. Its spirit also places
  custom MD influence-defence keys under `targeted_modifier`; do not assume that
  works against a named country without tracing a target-aware consumer.
- Turkey's mutually exclusive `TUR_close_kurdish_medias` and
  `TUR_sponsor_kurdish_medias`, cost7.15 each, sit at x-1/x1,y1 under the same
  media parent. They change the modern `TUR_PKK_strength` variable by -5/+2.
  The accommodation description promises peaceful coexistence, while the visible
  immediate strength change is +2. This is a useful warning to inspect follow-up
  consumers and time horizons instead of trusting a focus name. Do not port the
  modern PKK institution into 1970 or equate its variable with the new campaign.

## Initial canonical-source review

Reviewed the initial `tools/usa_kissinger_implementation/shared.py`, `deals.py`
and `regional.py` draft independently before emission. Only in-memory builder
output was inspected; no gameplay files were emitted or changed by this reviewer.
The first two builders produced 65 effects, 66 triggers, 22 ideas, 89 decisions
and four categories. Generated effect and trigger brace counts were balanced.
This is a structural smoke check, not an engine parse or behavioural test.

Confirmed findings sent to the implementation owner for correction:

1. The immediate weekly security reduction was gated only by the policy flag,
   while only reserve growth required the two actual divisions. Withdrawing the
   force therefore retained an unearned direct -3 unrest/week. Gate the direct
   deployment reduction by actual field presence; retain previously earned
   stabilisation as approved.
2. Weekly rising eligibility and final birth guards checked stage and cache but
   did not revalidate the funded route. Saved high unrest could produce a rising
   after transit or funding suspended. Recheck funded access, armed mobilisation,
   respected settlement and the completed qualifying/warning counters at birth.
3. Cache acceptance cleared the outstanding USA cache, while rising eligibility
   required that same cache to exceed 999. An existing consenting Kurdish player
   who actually received its weapons could therefore disable the supported
   rising. Distinguish outstanding, delivered and committed material, with no
   repeated equipment grant, or use actual eligible recipient stocks plus a
   delivery receipt.
4. The draft birth helper used scalar `set_capital = 408` and equivalents.
   Current native effect documentation supplies the structured country effect
   `set_capital = { state = 408 remember_old_capital = no }`. Use that verified
   form. The checkout's effect/event donors do not provide a scalar example.
5. USA and the host could terminate a standing rights agreement; the existing
   local Kurdish participant had no decision to withdraw its accepted consent.
   Provide local withdrawal and reconciliation for multiplayer agency.

The owner had already identified incomplete own-country initialization, new
Iraqi identity initialization, the frozen security-budget availability quote and
the old Iraqi donor bridge. Those unfinished portions were not treated as new
findings. In this initial draft, the new Iraqi transfer covered KUR's three
reviewed northern states only; PUK's bounded 1078 path and existing formation
conditions still require review when that bridge is complete.

The bilateral draft correctly evaluates partner relations within USA, puts
recipient acceptance in the named recipient, gates both actual spirit grants
behind the accepted signature and present relations, and uses scope-specific
weekly payer rows. A single cache delivery executes in the actual recipient,
then clears the common outstanding cache; simultaneous recipient clicks are
protected by the execution-time cache check. These findings do not establish
final suspension/renewal, settlement or engine behaviour before completed output.

## Emitted-code review: first completed output

The reviewer inspected the loaded `COLDWAR_USA_kissinger` effects, triggers,
decisions, events, on-actions, new country definitions/history and both actual
native money integration hooks. The canonical compiler, focus content and Gulf
bridge were also compared with their output. There are 41 approved new focus
IDs within the 342-focus USA tree. The owner reports no native run yet.

The earlier direct-security, current-funded-mobilisation, delivered-cache,
structured-capital and local-settlement-withdrawal findings are corrected in
this output. Actual birth uses the complete mobilisation trigger and both
completed counter thresholds. KPT/KPI/KPS add and transfer only 162/408/193,
respectively, after checking original host owner and controller; they never
copy KUR or PUK. Newborn cash/debt/investments are explicitly zero and the narrow
helper sets the native receipt that avoids free starter utility assets. Iraq
retains the separate PUK formation test and bounded 1078 branch. Current human
KUR/PUK identities are not passed through zero initialization.

The native income and expense providers each call the new stream calculator
once and add the appropriate accumulator once. The calculator resets both
accumulators before computing them. Bilateral transit income has a matching
USA expense. Regional payees are held in one per-theatre array, cleared before
the accepted recipient is added, so only one local payee receives that common
weekly subsidy. Cache delivery debits no second shipment: it grants only the
already-debited outstanding cache, increments the delivered receipt and clears
the outstanding balance in the same execution guard. The new material trigger
can use that delivered receipt. Mirrored native embargo/sanction checks govern
the actual subsidy. These are source-level findings, not observed bank balances.

The following remaining issues were sent to the owner promptly and require
correction or an explicit reviewed resolution before this reviewer can approve
the emitted mechanics:

- New KUR birth accepts any two held KUR-region states but unconditionally sets
  capital and spawns in 164. If only 633 and 630 are held, 164 is outside the
  transferred territory. Select an actually transferred, owned and controlled
  bounded state, or require 164 before using it.
- The KUR uprising block automatically sets `recognition_requested` even on an
  existing human KUR. Participation in a revolt is distinct from requesting US
  recognition. Automatic request belongs only to a genuinely new local identity;
  preserve the existing player's request decision.
- Cache acceptance now enrolls a recipient in a continuing subsidy, but the
  acceptance preview shows equipment only. Show the recipient's exact weekly
  income and matching USA payment there. The armed-front focus also needs the
  complete prospective recipient material and subsidy under its acceptance
  heading, alongside the already shown USA costs.
- Save migration stops old Iraqi security processing without removing or
  converting an existing `security_small`/`security_major` spirit. That leaves
  its +35%/+60% personnel and +20%/+35% equipment costs while its old local
  reductions cease, and a new security policy can add further costs. Convert an
  already-paid operation once without another setup invoice, retire its old
  spirits/owned target entries and preserve a bounded earned reserve as justified
  by its old sustained-deployment receipt. Likewise capture accepted legacy
  `support_kur`/`support_puk` participation/payee identity before clearing the old
  support budget, rather than retaining an unassigned paid stage.
- The three non-Iraqi defenders have no reachable negotiations response after
  the US armed-front focus completes: their rights focus is mutually exclusive
  and shuttle mediation expressly forbids a completed front. This contradicts
  the warning's available negotiation remedy and the approved three-response
  model. A host-initiated rights proposal or reachable post-escalation mediation
  must preserve real local-player consent and remain available during warning.

Agreement previews include both named spirits and signed native modifier rows
outside active-state checks. Local settlement refusal ends the proposal through
the USA-owned agreement helper; local withdrawal ends the standing agreement
without requiring host approval. The distinction between state transfer,
recipient equipment acceptance, continued support and recognition remains
auditable in the separate effects. Empty-column survival and reinforcement,
actual native scope evaluation, complete country lifecycle and multiplayer
transactions still require engine observations. A static parser or custom
emitted-script model cannot establish those claims.

## Final closure recheck

All five blockers from the preceding emitted-output pass are resolved in the
rechecked source and installed providers:

- New KUR selects the first actually owned and controlled state among
  164, 633 and 630 for its capital and column. Its automatic recognition request
  is confined to the genuinely new-actor branch. Existing players retain their
  separate request decision and are never initialized again by that branch.
- `aid.py` now exposes both prospective country spirits, the matching USA
  expense and recipient income, exact outstanding equipment and any separately
  recorded legacy cash escrow. Material assistance, political liaison and
  uprising participation have separate recipient receipts and withdrawal
  decisions. Finite cache acceptance does not silently grant uprising consent.
- One-time migration converts already-paid legacy security into the new policy
  without another setup invoice, removes both retired upkeep spirits and owned
  security targets, and preserves a capped 15-point reserve when the old
  sustained-deployment receipt justifies it. Legacy accepted payee and delivered
  material receipts are retained; its real $0.05 billion/week contract remains
  distinguishable from new lower-cost political programmes. Queued old 21/22/23
  event grants cannot execute after migration. Deferred forced-resistance cleanup
  retries without cancelling an unrelated active MD protest.
- Every host now owns a paid regional settlement response regardless of the US
  armed-focus choice. It has the exact setup invoice, weekly budget and actual
  named spirit, and requires existing relevant local players to accept. Local
  refusal or withdrawal can end that arrangement. It can suppress mobilisation
  during the warning instead of depending on Washington choosing its rights
  branch.
- Passive weekly ticks only complete the warning and mark readiness. The USA
  must choose a separate mobilisation decision. Actual birth still rechecks
  current funded access, material, unrest, settled rights, qualifying/warning
  counters and eligible territory before any transfer or war.

Two narrow follow-ups were sent to the owner during this closure pass:

1. The optional PUK 1078 transfer needs the same native
   `is_fully_controlled_by = IRQ` guard already present on the three KUR-state
   transfers and the three new-theatre states. A majority state controller must
   not take over a third country's still-held province through `transfer_state`.
2. `tur_networks` and `syr_voice` debit no weapons and add no new cache. Their
   paired focus preview must therefore use current cache only, rather than the
   material helper's default current-cache-plus-1,000. The genuinely weapon-funded
   focuses should retain the additional 1,000 in their prospective preview.

The owner reports an independent static validation pass and 25 emitted-AST
tests. This reviewer did not rerun those tests or treat the custom interpreter as
HOI4 evidence. A native fixture is being prepared outside the repository on E:;
no native assertion result is inferred here. The reviewer supplied current
native documentation for state/template-filtered `delete_unit`, the separate
country `num_equipment` and `num_equipment_in_armies` tokens, and exact
`has_equipment` stockpile bounds to that fixture's owner. The loaded MD money
provider treats `num_equipment@...` as its stockpile term, so fielded equipment
must not be subtracted from it when evaluating the probe.

## Bounded audit closure

Re-read the final emitted effects provider, SHA256
`756e118217bceeeff2943d860100a304a07ad7b283438cb4f3abaf3c9900e721`.
Both narrow follow-ups are closed. The optional PUK branch now requires state
1078 to be owned, controlled and fully controlled by Iraq before its transfer.
The two political-only previews, `preview_tur_networks` and `preview_syr_voice`,
now show only their actual USA setup/weekly costs and decision unlocks. They no
longer promise equipment or recipient-country material offers. The separate
weapon-funded programmes retain their real paired material previews.

No confirmed blocker remains within this bounded source/reference audit.
This closes the independent mechanics review, not a claim of native gameplay
or multiplayer validation. The fresh native smoke fixture and its 32 proposed
assertions are still being prepared by the implementation/validation owners;
their results are not inferred or certified by this note.

## Final English content and manual review

Applied `mdcw-content-review` and `mdcw-localisation`, including their content
contract and text/spirit references. Read the emitted English descriptions with
their actual reward bundles and representative regional decision effects. This
is a prose/content correspondence review; it does not certify live hover layout.

| Representative content | Review conclusion |
| --- | --- |
| Limited Commitments / Expanded Mandates | Meaningful alternatives: 50 PP, two campaigns, +10% decryption and +5% influence defence versus 75 PP, four campaigns, +10% foreign influence, -10% agency upgrade time and +3% bureaucracy cost. Descriptions explain concentration and exposure; neither option is a simple inferior copy. |
| Beijing, Moscow and Iranian transit | The political descriptions fit confidential consultation, arms control and transit. Each prospective bundle shows both real country spirits, exact signed modifiers and actual weekly payer/recipient balance before acceptance. The transit host bears +1% bureaucracy alongside its revenue and encryption benefit. |
| Iraq | The historical aid route is identified through Iran; political autonomy, armed assistance and recognition remain distinct. The text promises a response window and local political agency, rather than guaranteed US-controlled independence. Recognition has its explicit 180-day foreign-influence cost. |
| Iran and Turkey | The Iranian dossier identifies the Shah as the opening partner and requires confrontation; the Turkish dossier identifies the NATO alliance. Hostile routes are presented as deliberate alternatives, with credibility and opinion costs, rather than falsely described historical Kurdish operations. |
| Syria | Contacts refer to contemporary local political representatives, not PYD/YPG/SDF. The new authority and manual acknowledge the bounded mixed Jazira area; they do not claim all eastern Syria or all residents as separatist. |
| Regional defence | Security, investment and negotiated rights explain different institutional responses. Their previews show real setup bills, weekly costs and signed upkeep/spirit modifiers. Withdrawal prose correctly preserves earned calm while ending the direct deployment benefit. |

The representative descriptions use political and institutional language. Sampled
Effects contain concrete signed costs, named spirits, equipment, capacity and
decision unlocks, with short acceptance headings and numeric formatters. They do
not replace those numbers with paragraphs about providers, receipt bookkeeping,
debugging or implementation. The general MD comparisons recorded earlier remain
appropriate: Russia's institutional description plus signed modifier grammar,
Israel's recipient-owned offers, and Turkey's visible policy alternatives. The
new paired previews deliberately exceed the old MD spirit-name-only previews.

Standing policy, assistance, consultation, security, investment and rights
spirits have no unadvertised automatic 90-day expiry in this system. Credibility
and disputed-recognition spirits are explicitly 180-day costs. Chilean political
finance oversight suppresses the hostile pressure for a year, while the foreign
programme can survive. Its description was corrected to state that temporary
remedy and possible later rebuilding; the emitted English localisation SHA256 is
`4c06dfd209c640d9a9460a0c73404941d85924f9af126102032cb56f5764fff4`.

The final module README matches the reviewed geopolitical boundaries, actual
territory, finite material aid, independent Kuwait intervention, three defender
responses and source/native evidence limits. It does not promise a separate
battlefield-defeat unrest accelerator. Its two/four-campaign statement initially
exposed a legacy wartime bypass; the owner corrected the real guard instead of
documenting an exception. `legacy_irq_ready` now requires an existing Iraqi
commitment or an available campaign slot, and `legacy_irq_start` recounts before
its execution guard. The Kuwait war-goal path is unaffected.

Final exact provider hashes re-read for this closure:

- Effects: `27d37422e4a2405aed40c282f0b79a014c3fbe055d03d64a27ebfbd95b7bc891`.
- Triggers: `a0dde17ccefdd757ea13213a9881b37bce86bfc6f14a6d44f3f77e65b8ad1399`.
- Money system: `f43ada2f9ae864ffb0c2a5c9249cf8ab7bde037bd179d04076c80c590716b6b2`.

The new expense contribution is now added exactly once at the end of the
native additional-expense provider, after its global inflation multiplication.
The income hook remains separately counted once. This preserves the stated
nominal weekly contract rather than inflating only the donor's side. No
confirmed content/manual correspondence blocker remains in this bounded pass.
Native fixture assertions, live event/tooltip rendering and multiplayer behaviour
remain the responsibility of the separate validation run.

## Frozen-run presentation spotcheck

Read-only follow-up while the owner's native fixture was running. No generator,
runtime or running profile was changed by this reviewer. The inspected examples
were Beijing, Iraqi funding and settlement, Turkish regional rights and Turkish
recognition, with their expanded `available` trigger chains.

Confirmed safe presentation: `usa_actor` already encloses its actual country,
scenario and treasury-skip conditions in `hidden_trigger`; the focus's additional
outer hidden wrapper is harmless. Native country-existence, war, embargo,
territorial control and actual NATO-membership requirements are meaningful and
must remain understandable. Unused localisation helpers alone are not defects.

Confirmed presentation work for a subsequent owner-controlled emission:

- `deal_*_can_offer` repeats `tag = USA` and `IMP_is_1970_scenario` outside the
  hidden actor wrapper. The installed native English trigger catalogue contains
  explicit country-is and game-initially-started date strings. Hide these routing
  conditions in the visible offer chain while preserving their execution checks.
- Enclose the full `stage > 0 OR slot_available` condition in the existing
  meaningful capacity tooltip. Wrapping only `slot_available` leaves the existing
  commitment half without a corresponding player-facing explanation.
- Present the Iraqi accepted framework through a concise visible acceptance
  requirement. It is actual Iraqi consent, not a redundant receipt for completing
  the earlier US autonomy focus. Preserve the old respected-settlement alternative.
- Present Turkish governmental cooperation or regional contacts as one meaningful
  political-channel requirement. `contact_tur` is not safely interchangeable with
  a prerequisite focus: the focus can be completed while enactment is pending.
- Enclose each full recognition condition in a meaningful requirement describing
  an independent regional authority, relevant controlled territory and its actual
  request. The existing recognition helper can be used, with independence stated
  explicitly. Do not simply hide the local player's recognition request.
- Give existing local liaison/partner consent and mirrored sanction tests clear
  semantic requirements instead of exposing their internal flag/array structure.
  Actual active membership spirits and substantive relations requirements should
  still be visible; a generic availability sentence must not erase them.

Native documentation proves `hidden_trigger` suppresses its tooltip and
`custom_trigger_tooltip` is an AND condition with an overridden tooltip. It does
not establish how every unlocalised flag or bare variable renders in a normal
non-debug build. This reviewer therefore does not claim a live raw-name leak
from source alone. The concrete issue is that the meaningful consent/request
conditions have no authored display wrapper, while internal routing has explicit
native display text. Debug-only visibility, fallback suppression and missing
labels must not be conflated.

Relevant main-MD donors support the distinction: Israel's visible
`ISR_big_size_knesset` flag has its own political English localisation; Turkey
wraps its meaningful `hizmet_power > 0.59` threshold in `TUR_we_need_60`, and hides
an internal `TUR_rise_of_osman` condition. These are presentation precedents,
not evidence that a release-mode Kissinger hover has been inspected. Native
hover verification and equivalent-condition checks should follow any later
presentation-only emission.

## Presentation closure

Rechecked the owner-emitted display fixes. Internal offer routing and bookkeeping
are hidden. Complete capacity, framework consent, Turkish contacts, local partner,
recognition, Syrian crisis and accepted supply-route predicates now have authored
native requirement wrappers. Their actual guards remain intact. The recognition
label explicitly requires an independent authority, and the northern-territory
label explicitly requires Iraqi ownership as well as full control.

The Iraqi mobilisation decision now also previews/checks the same two fully
controlled, Iraqi-owned KUR-region states required by actual execution, avoiding
a paid selection that could have had no territorial result. Treasury equality
uses the documented expanded `compare = greater_than_or_equals` form rather than
the rejected short inclusive syntax. No runtime or profile changes were made by
this reviewer while the native fixture was running.

Final source hashes for this presentation closure:

- Effects: `6d01283988e88e46f19fae4d9284cfc714175e002aa0c9240ad180a5aa555f03`.
- Triggers: `7efd2a10e8289c2ccbc4549c9b4d194875a6e1f7f3d7d547f567489d58859010`.
- USA tree: `dd0210b28f0577bccb6ef525bc59cd6c288a02fc521bd243dd5f920ee84713bd`.
- English localisation: `8611b2cf53bdac05660fd07c54ffb4add6980ce24db359cf4e9bd1691f5b1f58`.

No confirmed source-level mechanics, prose or presentation-contract blocker
remains in the reviewed scope. This is not a claim that every release-mode hover
has been observed, and it does not certify native test or multiplayer results.

## Native-guided minimum-research finding

The owner reported that native run 2308 passed the exercised stabilisation,
withdrawal, recurrence, warning, KPI birth, zero-ledger and local-war checks.
Its 2,000-weapon cache delivery assertion failed despite the paired budget and
cache-clear receipts passing. This reviewer did not independently run that
fixture. A native equipment A/B diagnostic is pending, so equipment delivery
is not marked successful on the strength of source/model tests.

The resulting source audit confirms a separate startup defect: the existing
`mdcw_apply_1970_infantry_research` dispatcher at line 11347 is restricted to
January 1, 1970 and enumerates known `original_tag` values. KPI, KPT and KPS have
no dispatch branches. Thus calling it from their histories grants no research;
calling it at any later birth is also ineffective. Its applied flag can still
be set after the unrecognised-tag pass. The earlier review's generic minimum
research assumption is superseded by this complete dispatcher inspection.

The proposed correction is approved within this bounded review: use an explicit
owned minimum-research helper in the three new histories and genuine-new-actor
startup, without the date/tag dispatch or any technology inheritance. Fully
read KUR and PUK profiles, at lines 5448 and 7834, contain the same eight-tech
1940-1945 baseline:

`mdcw_infantry_weapons_1940`, `mdcw_util_vehicle_1940`,
`mdcw_cnc_equipment_1940`, `mdcw_support_weapons_1940`,
`mdcw_special_forces_1940`, `mdcw_camouflage_1940`,
`mdcw_body_armor_1945` and `mdcw_anti_tank_1940`.

They then select exactly one anti-air technology: `mdcw_nsb_anti_air_1940` with
No Step Back, otherwise `mdcw_anti_air_1940`. Preserve `popup = no`. The complete
definitions in `mdcw_early_infantry.txt` unlock early equipment/subunits and
modest baseline modifiers; none grants a stockpile, factories or 1965 research.
The early rifle technology expressly enables the militia battalion used by the
local column. This is a researched donor baseline, not permission to grant the
1965 `infantry_weapons_1` technology merely to conceal an aid-delivery defect.
The helper remains confined to genuinely new identities and must not reset an
existing player's political or research state.

The equipment issue is a separate native question. Current effect documentation
for `add_equipment_to_stockpile` explicitly supports optional `producer = USA`;
`creator` is not the documented parameter for this effect. A producer change
should be made only after the native A/B identifies the actual cause. A recorded
cache balance, zeroed delivery receipt or funded recipient spirit alone is not
proof that any usable rifles reached the recipient stockpile.

## Minimum-research and native producer closure

Independently read diagnostic run 2328's actual native `game.log` at
`E:/HOI4_Mod_Tools/mdcoldwar/runtime/kissinger_20261028/native/runs/ks_diag_20261028_2328/profile/logs/game.log`.
Lines 1853-1866 establish the equipment defect and its bounded remedy:

- The newborn initially had zero stockpiled and zero fielded rifles and no
  `infantry_weapons_1` research.
- Its recorded cache was 2,000. Original delivery cleared that cache and recorded
  2,000 delivered, but actual stockpiled and fielded rifles remained zero.
- An unqualified constant one-rifle addition still left both actual counts zero.
- The otherwise equivalent constant addition with `producer = USA` produced
  exactly one stockpiled rifle and zero fielded rifles.

This proves the old native positive-addition failure and the producer-qualified
one-item remedy. It does not, by itself, establish a passing final production
2,000-item transaction or full weekly lifecycle. The diagnostic run is not
classified as an overall native PASS.

Re-read the corrected emitted providers:

- Effects SHA256:
  `88a7257db2ef5ad328d8887b4c91b4557ae2d37c073183f655f1dde304303033`.
- Decisions SHA256:
  `642e67ea360638eab0370fb9373005544e1d45b34d1446f7519c637acf61bace`.

All five actual recipient cache transactions, KUR, PUK, KPI, KPT and KPS, now
specify the documented `producer = USA`. All 22 positive material-preview grants
in the owned effect provider use the same producer. Actual negative US stockpile
debits and the finite cache/delivered receipts remain in their original guarded
transactions; no second debit or free replacement shipment was introduced.

The emitted undated `COLDWAR_USA_KS_regional_research` helper contains exactly
the approved eight early technologies and the mutually exclusive DLC anti-air
choice. Each new country history and the genuine-new-actor initialization calls
that helper instead of the ineffective dated dispatcher. It grants neither
1965 rifle research nor equipment and does not copy an existing country's
politics, technology or armed forces. The earlier startup finding is therefore
closed in source. The separate fresh final native run and its 34 proposed checks
remain pending; no additional content or runtime mutation was performed by this
reviewer.

## Standing-policy AI closure

Applied `mdcw-country-ai` and its AI-path verification reference to the narrow
standing-policy correction. The old diagnostic's real weekly checkpoint had
lost its transit agreement. Source inspection found unrestricted positive AI
weights on cancellation and termination decisions, so a signed agreement could
be voluntarily ended almost immediately after acceptance. This is distinct
from native suspension under an actual war, embargo or sanction.

Re-read current decisions SHA256
`4c9e424a0803072cbbae2e748dcdc81d0bff93bedc92d06bb68029498576f38d`.
Unsigned proposal cancellation, standing agreement termination, local liaison
withdrawal, uprising stand-down, rights withdrawal, host policy ending and Chile
funding termination now have zero AI weight. The human decisions remain present.
American suspension has zero AI weight and resumption has weight one. Initial
acceptance/refusal choices retain their authored weights, including the separate
local settlement and Iraqi framework choices; recipient consent is not bypassed.

Each of the eight host security/investment decisions retains base factor two,
with a multiplicative zero when the other spending programme is already active.
The decision's own active-policy availability guard prevents buying it again.
The native `bankruptcy_incoming_collapse` mission adds a separate AI zero weight;
the actual provider is `common/decisions/bankruptcy_decisions.txt:888`, with the
same mission guard already used by MD's spending decisions. This is an AI
selection rule, not a new human affordability or crisis prohibition.

Canonical AST comparison with the retained 2328 decision snapshot was identical
after excluding `ai_will_do` and the separately reviewed equipment-producer
qualification. Thus no human visibility, availability, fees, payment execution,
recipient consent or transaction effect changed in this narrow AI correction.
The owning generators contain the same policy. It closes immediate discretionary
cancellation and repeated paid security/investment switching, not the broader
question of adaptive long-term AI strategy or fiscal optimisation. The fresh
native weekly checkpoint and 34-check smoke remain separate validation evidence.

## Final newborn-equipment scope and first-hour evidence

Re-read final effects SHA256
`f4f86628453f6a3216df14db760e9cb21bee5d9cf4c4d20c1bf16ec908e5bd28`.
Exactly seven `set_equipment_fraction = 0` calls follow the new local column:
three alternative KUR capital locations, one PUK location and one each for KPI,
KPT and KPS. Each call explicitly re-enters the named rebel COUNTRY scope.
The KUR/PUK paths are inside their genuine-new-actor receipts, set only when the
country did not exist before transfer. The other three uprising effects require
their distinct authority not to exist. An existing human country cannot enter
these initialization, column-creation or equipment-clearing branches. The clear
does not run during later aid acceptance or weekly reconciliation.

Current native effect documentation at `set_equipment_fraction`, line 6913,
specifies COUNTRY scope and an equipment factor. The complete existing
`imp_gc_perf_clear_ai_equipment` donor likewise applies zero in country scope.
This supports the explicit recipient scoping; it is not permission to clear
the defending host or a pre-existing regional player's armed forces.

Independently read the actual first-hour log from
`E:/HOI4_Mod_Tools/mdcoldwar/runtime/kissinger_20261028/native/runs/ks_final_20261029_0017/profile/logs/game.log`.
Lines 1853-1865 show minimum-research PASS, initial rifle stockpile/fielded/total
all zero, the committed 2,000-rifle cache, actual post-delivery stockpile 2,000
with fielded zero, cache zero with delivered receipt 2,000, and a duplicate
attempt still leaving exactly 2,000 actual rifles. Both cache delivery and
non-duplication assertions pass. No first-hour FAIL label was present in the
reviewed log, and no owned-namespace parser diagnostic was found in its error
log at this checkpoint.

This closes the reviewed startup/equipment source issue and establishes the
exercised native first-hour delivery result. The real weekly checkpoint remains
pending here. Accelerated helper calls, one authority's native birth and a
passing first hour do not establish multiplayer, save/reload, every theatre's
birth or years of uninterrupted play. No runtime file was changed by this
reviewer.

## Status and provenance

All findings above are current source, native documentation, asset metadata or
explicitly identified visual donor inspection. No new-country birth, state
transfer, manpower reinforcement, bilateral arrival, save/reload or multiplayer
test was performed by this reviewer. Final emitted-code findings remain pending.
Original MD/Paradox authorship and licence notices remain in their providers;
no third-party image was copied or modified. Missing individual authorship or
permission details remain unknown under `IMPERIA_COLD_WAR_NOTICE.md`.
