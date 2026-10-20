# Greece 1970 runtime tree

The saved 313-focus design in `docs/greece_1970_design/coldwar_greece_1970_design.json`
is installed as `COLDWAR_GRE_1970_focus`. `layout.py` replaces the original
stacked layout and 60 prerequisite groups with sectors and parallel branches
based on the original MD Russia 2000 tree. All 313 focus IDs, exclusions and
durations are retained. See `LAYOUT.md` for the exact structural comparison.
The original HTML preview remains an archive of the earlier design.

`rewards.py` completes or differentiates 88 focus rewards which were missing
effects or used identical generic packages. This includes 19 targeted research
bonuses, state-local rural development, industrial output, productivity growth,
tax collection, dockyard output, army logistics and aircraft maintenance.
There are 31 country modifier types, plus state development modifiers. Every
paid programme now has a concrete gameplay outcome. The funded economic models
for the seven governments share a replacement slot; switching government never
stacks all models. A returning eligible government can restore its own funded
permanent policies without replaying payments or one-time rewards.

`rewards_review.json` records each changed reward and `layout_review.json`
records structural changes and geometry checks. Explicit effect tooltips show
the actual programme modifiers, duration and research bonuses before selection.

Rebuild and check from the mod directory:

```powershell
python -X utf8 tools/greece_1970/compile.py
python -X utf8 tools/greece_1970/validate.py
```

`compile.py` generates the files listed in `manifest.json`. Two small integration
edits are maintained outside the generator: Greek country history loads this
tree in the 1970 snapshot, and `mdcw_load_1970_fallback_tree` exempts Greece.
The existing eastern Mediterranean roster still supplies leaders and portraits.
Later-start country history is retained.

Domestic agreements and elections supply the factual gates which existed only
as contracts in the preview. All three initial regime paths work; a later exit
from lasting military rule, retained military tutelage or a hardline reversal
can join the shared civilian transition. A refused agreement can be revisited
through decisions. A lasting junta is a playable outcome. A failed restoration
referendum returns the country to a parliamentary republic.

Election options record the actual winner agreed in multiplayer. AI weights the
existing MD party support. Native election notifications renew the current
mandate; an unelected party change invalidates it. ND and PASOK names and leader
availability continue to use the existing dated regional/native politics system.

Foreign proposals send a named country its own accept/refuse/revise/defer event.
Proposals to multiple guarantors require all named consents. Replies expire after
90 days; silence is recorded separately from refusal. Cyprus offers record the
current native crisis instance, so a reply to an earlier crisis cannot authorise
a new one. Covert sponsorship can increase existing Cypriot coup pressure only
after Cypriot acceptance; the existing Cyprus system controls any subsequent
actual coup or Turkish response. No Greek focus starts a war, annexes Cyprus,
grants EEC membership, or automatically concludes a foreign settlement.

Funding is checked again at implementation. Unfunded completed programmes expose
retry decisions and block their ordinary descendants until implemented. One-time
flags prevent duplicate payment, XP, PP, stability or queued construction.
The current selection is recorded per modifier slot; reconciliation cannot
reactivate every historical policy. Timed programmes are never recreated after
expiry. State development penalties apply only to the three specified owned
rural states and are removed by the corresponding regional reform.

The credit line debits the US lender and credits Greek treasury and debt by the
same frozen amount (2% of Greek GDP at first dispatch). Temporary revenue measures
reverse only their actual native tax increase after expiry. Oil penalties require
an observed oil-price shock; they do not start in January 1970. Aegean licensing
disputes can be explicitly authorised as an alternate-history dossier decision.

Localisation is English only, as specified by the design. Existing mod textures
are reused for focus and idea icons, with the vanilla shine overlay.

`validation.json` records syntax/reference checks and 26 state-machine scenarios,
including five civilian transitions, party governments, repayment guards,
construction capacity, diplomacy, crisis-instance invalidation and the 2000
scenario guard, paid productivity/research, local programme suspension,
corruption floors and restoration of government programmes. These are
script-level tests, not HOI4 engine tests. Final
in-game layout, AI pacing and multiplayer behaviour still need a fresh 1970
campaign check.
