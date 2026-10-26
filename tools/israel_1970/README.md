# Israel 1970 implementation

The generated `ISR70` module contains 389 focuses, 161 decisions, sixty-seven events,
twenty political families and thirty-seven named party/list variants. New
localisation is English only, with a UTF-8 BOM. The seven starting spirits are
applied once for the January 1970 campaign.

The focus layout uses compact thematic blocks and MD relative-position anchors.
Party programmes occupy two compact tiers. All 32 political unlock focuses have
been removed. Each party's institutional root requires only its exact governing
party, with no prerequisite focus or foundation flag. Political organization
decisions are accessible without an outlook focus or the Knesset focus.
Cross-block focus
requirements remain in `available`, avoiding long lines through other branches.
Resolved script positions match the layout data and preview.
Government programmes are separate dynamic modifiers, enabled and restored only
for the governing MD party slot. Changes of government do not reset the tree.

Revision 2 replaces every focus reward. `revised_rewards.py` is the authored
reward and artwork source; the original 65/35 modifier split is no longer used.
Political choices now combine distinct institutions, research bonuses, state
construction, experience, interest-group approval and constitutional effects.
Descriptions contain narrative text. Rewards, costs and unlocks appear through
the normal completion-effect tooltips rather than duplicate description lists.
Programme changes use the same visible `add_to_variable` tooltips as MD Russia,
including MD's actual labels, sign colors and units.

Focus graphics come from existing Cold War and Israeli assets, including the
period Herut, Mapai, Mapam and Hapoel HaMizrachi emblems. Each selected texture was
reviewed on contact sheets; filenames that concealed foreign flags or modern
politicians were rejected. PNG sources have lossless DDS copies, and all focus
sprites have MD completion-shine registrations. Spirits use matching artwork.

Existing 1970 saves synchronize completed focus programme modifiers and spirits
once. Immediate rewards such as new factories, money and research are not
retroactively reissued. A new 1970 campaign receives the complete new rewards.

The initial political distribution is a model of the 1969 political families,
not a claim that the MD slots correspond exactly to individual electoral lists.
The Alignment leads a coalition with Gahal, Mafdal, the Independent Liberals and
the Arab municipal-list family. Mapam is initially part of the Alignment.

Period names are separate from later foundations. Likud, Hadash and Shas have
their own formation steps. Other named successor lists use dated presentation
decisions. Party-family progress survives these changes. Noam is represented in
the religious-Zionist family, not as the founder of a monarchy. Israel has no
Shiite or Salafist branches, foundations, campaigns or government programmes.
The four native MD slots remain in the framework's fixed arrays but are disabled
for Israel in the 1970 scenario. The four retained outlooks are Western, Emerging,
Non-Aligned and Nationalist.

Fifty-seven registered text icons use existing MD artwork. Generic ideological
symbols represent early parties or alternative movements where MD has no period
party logo; native Israeli logos are used for corresponding later formations.
They are not presented as reconstructed historical logos. Several period leader
candidates use an existing generic portrait; Golda Meir uses the period asset.

Projects reserve their quoted budget when selected and deliver after their stated
duration. A project that loses its state or other required conditions refunds
that exact reservation. One-time completion flags prevent repeated factory grants.
Debt repayments debit and retire the same capped amount. Bilateral agreements
require the other country's response, and rejected proposals can be retried.
Territorial implementation checks both legal owner and controller; it creates
no automatic ownership or cores from a claim. The new Sinai-integration route
has its own much stricter consent and time conditions. Starting armies, fleets
and air wings remain deferred.

## Policy expansion (approved design revision 5)

The 77-focus proposal is compiled by `policy_common.py`, `policy_domestic.py`
and `policy_territories.py` from `policy_design.json`. Three existing citizenship
focuses retain their IDs, giving 74 net additions. The six compact new blocks
cover citizenship, settlement projects, finance, Sinai development and expansion,
occupation status and optional radical government programmes. Local government
can coexist with either citizenship policy; the two access policies exclude
each other. Office workforce/productivity and financing values retain the
approved proposal, including equal treasury/debt entries for the bond facility.

Country effects are separate from state effects. Project budgets are reserved
once, delivery checks the original conditions and failed delivery refunds the
exact reservation. Shared-slot checks cover the whole multi-building package.
The three voluntary internal migration cohorts have independent caps, hidden
monthly callbacks, and exactly matching source/target population changes.

The legal regimes are exclusive through runtime conditions, rather than
irreversible focus exclusions that would deadlock later paid reforms. Reforms
replace status-bound modifiers and reset civil-rights deadlines; already built
assets, actual population and civilian/property claims remain. A pending first
reform can be withdrawn before the other focus enacts it. Country costs and
local effects suspend/restore together on control loss and recapture. Government
programme costs are similarly reconciled when the relevant party enters/leaves.
Factory access uses one aggregate state modifier with a real 100% total cap;
it is not factory output or a new building grant.

Equal rights grant no automatic resistance/compliance/loyalty bonus. Only an
implemented council contract can lower local garrison need by 5%; fulfilled
restitution can lower resistance target by 2 points. The optional Sinai core
requires ten continuous years of ownership/control, five years of equal rights,
two years of low resistance, minimum stability/compliance, fulfilled claims,
and separate accepted local and Egyptian status agreements. Both proposals can
be rejected and retried. Rights persist without a core. Radical population and
constitutional choices are explicit alternatives; the forced-displacement
option records enduring civilian claims and sends actual foreign embargo
response events. It does not delete a population count or award a core.

The user-corrected territorial target is existing Sinai state 213. Both the
civilian and coastal development tracks, all three voluntary migration cohorts,
occupation regimes and the optional core refer to Sinai. The three independent
cohorts move at most 45,000 people (20,000 + 15,000 + 10,000), matched by the same
population subtraction from Tel Aviv; they create no national population.
Legacy `gi_canal_*` identifiers remain stable, with updated Sinai labels/effects.
`policy_map.py` restores the superseded state-214 split, removes only its owned
state/category files, and returns canal port models to state 214. No new state
boundary or population allocation is used. `policy_world.py` keeps the actual
canal's 213/214 shore checks and closed-canal revenue gate; Egypt can fund a
separate reopening. Sinai coastal logistics grants local supplies and incurs
administrative costs; it does not reopen the canal or generate canal revenue.

Static checks and browser rendering do not establish engine/save compatibility.
Existing
saves remove the two superseded citizenship modifier ideas once; instant
historical rewards are neither reissued nor retrospectively revoked.

The history, world-politics dispatcher, party getters and leader dispatch are
integrated with the new module. The legacy Israel weekly/monthly mechanics are
excluded only from the 1970 scenario. The fallback tree loader protects the new
tree only for that scenario.

## Build and validate

```powershell
python tools/israel_1970/build_content.py
python tools/israel_1970/validate_content.py
python tools/israel_1970/validate_layout.py
python tools/israel_1970/validate_rewards.py
python tools/israel_1970/validate_policy.py
python tools/israel_1970/validate_policy_map.py
python tools/israel_1970/audit_md_patterns.py
python tools/israel_1970/check_rebuild.py
```

`design_source.json` preserves the original English input. `direct_access.py`
removes the obsolete political gates on every build; `revised_rewards.py`
authors the live rewards and artwork. `design_tree.py` is a compatibility entry
point for the current compiler and report updater. It cannot restore the old
unlock chain or the superseded German design preview.

Static validation covers Clausewitz block structure, focus prerequisites and
exclusions, referenced helpers, events, ideas, dynamic modifiers, party getters,
icon registrations and DDS files, English localisation, budget reservation,
negotiation retries and scenario integration. It is not an HOI4 engine test.
Layout validation also resolves anchors in the generated focus script and checks
all positions and prerequisite connectors against the preview data. Missing or
cyclic anchors, prerequisite lines running upward and preview connectors crossing
unrelated focus cards are rejected. Revision 5 clears the six obstructed preview
connections in the economy, defense and territorial branches, and groups
intelligence below the General Staff. The territorial block starts one row lower
to leave room between sections. The preview geometry does not establish the
engine's exact line routing.
`update_documents.py` also refreshes the standalone preview's embedded design.
The MD layout and reward reviews are saved in
`docs/israel_1970_design/MD_LAYOUT_REVIEW.md` and `MD_REWARD_REVIEW.md`.

The October 15 engine log identified unsupported `>=` operators as the cause
of missing focus branches. Building capacity now uses MD's `size > N-1` form;
treasury and mandate thresholds use explicit `check_variable` fields with
`compare = greater_than_or_equals`. The validator rejects compound comparison
tokens and checks these regression cases. The unsupported country modifier
`reliability_factor` was replaced by MD's `army_armor_defence_factor` (+10%).
The corrected build still requires an in-game reload/restart to verify loading.

The 14:26:12 hover crash dump also shows a null ideology-group object while the
engine builds the "Politics will change:" tooltip. The captured text includes
"Return to Parliamentary Government" beside the Mizrahi municipal branch.
Eleven visible election effects omitted `ruling_party`. Each now explicitly
supplies its party's existing outlook (`communism`, `neutrality`, or
`nationalist`); its governing-party condition is unchanged. Validation rejects
missing groups and mismatched party/outlook pairs. This repair was checked
against the crash dump and generated scripts, without restarting the game.
