# UAE and GCC event cost ledger

Read-only source inventory,2026-10-19. Covers all35 authored UAE dialogue
types and the3 common GCC dialogue types. Repeated immutable round IDs are
technical copies of these types, not additional narrative events or charges.
The amounts below describe current execution, not proposed changes. Native
HOI4 delivery/tooltips have not been tested.

## Reading the prices

- PP is charged once by the initiating decision. Its child popup, recipient
  popup, counterproposal and confirmation do **not** each charge that PP again.
  Recipients do not pay PP merely to answer. Declining does not refund the
  initiating PP. Focus-initiated offers have no separate decision PP charge.
- `S` is frozen scenario-start GDP: **$0.686bn**, or$686m. This is a game
  calibration baseline, not a newly asserted historical GDP estimate.
- `U` is the UAE's actual `gdp_total` when the offer is sent. Prices are frozen
  per offer. `R` is the receiving country's own GDP when its invitation is
  delivered. `UK` below means Britain; it is not the GDP symbol`U`.
- A current-GDP invoice changes with economic development; it is not always
  the starting-price example. At`U=S`:1%=**$6.86m**,2%=**$13.72m**,
  3%=**$20.58m**,5%=**$34.30m**,10%=**$68.60m**.
- Foreign cash transfers name their payee below. Programme expenditure without
  a named payee removes money from the funding treasury; it is not secretly a
  foreign grant. Native percentage spending modifiers are ongoing budget
  effects, not another fixed cash invoice.
- Cash moves only after the guarded acceptance/confirmation. An unsigned,
  rejected or expired agreement does not pay its contract invoice. Ordinary
  focus setup costs and prerequisite route investments are separate and are
  not charged again by these event options.

Sources: `diplomacy.py` family definitions, dispatch/acceptance effects and
domestic meetings; emitted decision`cost` fields; `revision.current_design()`;
the common GCC compiler/loaded events; native`idea_gcc_member_state`.

## Twelve domestic UAE/UK meeting types

Event IDs show the first immutable round. All PP belongs to the named
initiating decision, even if the player later chooses to maintain policy.

| Type / first event | Opening expense | Option expense and actual outcome | Cost/benefit assessment |
|---|---|---|---|
| Founders' Settlement`.110001` | UAE**35PP** | Cash0. Accepting stronger federal mandate unlocks that charter direction; accepting emirate guarantees unlocks the alternative. Refusal spends no cash and allows retry after180days. | A meaningful mandatory constitutional branch choice. The popup should identify the future focus permission; it does not immediately award the later focus's buffs. |
| Federal Dispute`.111001` | UAE**35PP** | Accepted mediation: UAE spends**3%S=$20.58m**, programme spending with no foreign payee. Clears the recorded crisis and removes the **remaining** Unequal Development stability penalty. Originally−6percentage points; after RAK accession it is−3points. Decline costs no cash. | A real paid remedy. Show its current marginal stability relief rather than promising a flat+6 regardless of earlier reform. |
| Crown and Property`.112001` | UAE**50PP** | Settlement: UAE spends**5%S=$34.30m** and removes Citizen Republic's **−6percentage-point stability contribution**. No separate crown country receives cash. Decline retains it and pays0cash. | Coherent compensation abstracted as domestic spending. Distinguish a continuing modifier remedy from an immediate flat stability grant. |
| Delegation of Federal Powers`.113001` | UAE**50PP** | Cash0. Acceptance sets the delegated-power flags and adds a modifier-free status idea. No actual constitutional, office, numerical or future-focus consumer was found. Decline leaves status unchanged. | **Poor present value / missing enacted effect.** The approved summary promises an active constitutional change; current execution records status only. See D4 in the diplomacy audit. |
| Federal Cabinet Bargain`.114001` | UAE**35PP** | Cash0. Accepts the negotiated cabinet; before7October1990 Rashid can occupy the prime-minister office if he is not himself president. Grants up to **3points relief** from remaining Fragmented Authority bureaucracy costs, but the active cabinet adds **+3% bureaucracy cost**. Presidency remains separate. | Primarily an office/constitutional bargain. The ongoing+3% can offset the full3-point relief; do not sell the relief alone as a net budget saving. If little penalty remains, the current net cost can be positive. |
| Sharjah Restoration Attempt`.115001` | UAE**25PP** | Negotiation: UAE spends**2%S=$13.72m** and gains **+3% stability factor for365days**. Security response: cash0, **+10ArmyXP**, **+5% army personnel costs for365days**. Either resolves the recorded attempt. | A meaningful funded settlement versus military response with a continuing cost. No foreign army is spawned and the national party is not replaced. |
| Release Reserve Principal`.116001` | UAE**15PP** | Withdraw all recorded principal, or one standard **5%S=$34.30m** deposit if covered. UAE treasury gains exactly the amount removed from its reserve ledger. Leave intact: cash0. | This is return of earlier savings, not new income or interest. A deposit previously cost another15PP and$34.30m; depositing then withdrawing therefore costs30PP overall. |
| Oil Downturn`.117001` | UAE**35PP** | Draw all recorded reserves as above; or cash0 and **−10% bureaucracy cost /−8% construction speed for365days**; or maintain current policy for no cash/effect. | Actual austerity trade-off or use of existing savings.35PP is still spent if the player selects no change. No synthetic oil-income bailout is granted. |
| Reopen Status Talks`.118001` | UAE**35PP** | Choosing protection sends`.1001`; choosing early handover sends`.2001`. **No extra PP or cash** for either child popup. Keeping the timetable costs no additional cash. | Optional diplomacy. The historical withdrawal itself does not require paying35PP or requesting freedom. |
| Amend Withdrawal Terms`.119001` | UAE**35PP** | Sends a360-day transition proposal`.18001` or protection proposal`.1001`; no additional PP/cash. Keeping current terms pays0cash. | A negotiation expense, not an independence purchase. UK consent is required to replace the timetable. |
| British Withdrawal Policy`.120001` | Britain**0PP**, cash0 | Sends continued protection`.16001` or earlier release`.17001`; child popups add no PP/cash. Continuing the timetable has no payment. | Correctly makes honouring the announced departure free. Renewed protection is an agreed alternative. |
| Invasion of Kuwait`.121001` | UAE**35PP** | Financial aid sends`.15001`: UAE will pay **3%U to Kuwait** only if Kuwait accepts. Transit`.19001` and deployment access`.20001`: cash0. Civil protection: UAE spends **1% of live GDP frozen when this menu opens** and gains **+3% stability factor for365days**. Maintain policy: cash0. | All alternatives use this **single35PP** opening charge. Aid money is a real transfer; access does not create troops, a faction or automatic war entry. |

## Twenty bilateral offer types

These are the first-stage recipient popups. The PP column describes the
originating route, not a fresh charge on the receiving government.

| Type / first event | Initiation PP already paid | Valid acceptance cash and actual result | Cost/benefit assessment |
|---|---|---|---|
| Renewing British Protection`.1001` | **0** from Renew Protection focus; or UAE**35** via Status Talks/Amendment menu | Cash0. Replaces scheduled departure with continuing British protection. Dependency keeps the UAE's **−10% political-power gain** spirit; review date does not itself release it. | Meaningful diplomatic/status choice. The direct focus takes70days; neither route buys independence. |
| Preparing British Handover`.2001` | **0** from Preparing the Handover focus; or UAE**35** via Status Talks | Cash0. UK may accept immediate release or agree practical cooperation while retaining the existing release date. Rejection does not cancel the historical timetable. | No fee is appropriate to this already announced withdrawal. Direct focus takes70days. |
| UK–UAE Friendship Treaty`.3001` | **0**, dispatched by the70-day friendship focus | Cash0. Accepted independent friendship activates that earned focus's **+3% research speed,+6% office productivity,+5% education costs**. No puppet/faction/automatic guarantee. | Real cooperation with a continuing education-budget cost. Those modifiers require the earned focus; signing a status flag alone is not a free duplicate grant. |
| British Development Co-Financing`.4001` | UAE**25PP** | Britain pays **$250m**; UAE receives **$250m** once under its accepted protection compact. | A substantial recipient benefit funded by the consenting UK treasury. At the start baseline this equals36.44%of UAE GDP, so the balance impact is large; it is not a historical grant amount established by this code. |
| Bahrain Federal Charter`.5001` | UAE**25PP** | Full participation or association each costs UAE **2%U** ($13.72m at baseline). Domestic preparation spending, **not a cash transfer to Bahrain**. Recipient gains the selected status. Both Bahrain and Qatar full acceptances together enable the Nine States focus's **+1 incoming investment capacity**. No annexation. | Individual acceptance is principally RP/constitutional preparation; the substantial capacity benefit requires **both** full signatures. Two baseline invitations total50PP+$27.44m. |
| Qatar Federal Charter`.6001` | UAE**25PP** | Same2%U preparation invoice and full/associate alternatives as Bahrain; Qatar keeps its territory and separate sovereignty. | Do not present association as the full-signature investment-capacity condition. UAE and recipient each retain control of their own country. |
| Arab Technical Cooperation`.7001` | UAE**25PP** | UAE spends **2%U**. No foreign cash payee. Both countries gain **+10productivity points per controlled state**; recipient has a730-day exchange cooldown. | Substantive technical aid, but partner benefit scales with the partner's number of controlled states while cost uses only small UAE GDP. Potentially generous aid to a large partner; not a10%percentage buff or temporary productivity grant. |
| Oil Concession Equity`.8001` | UAE**35PP** | UAE pays **10%U** ($68.60m at baseline) **to Britain**. Accepted State Participation programme gives UAE **+15% oil-export revenue multiplier,+6% bureaucracy cost**. | A real paid equity/administration trade-off. Payment is once; the native recurring modifier is not a guaranteed fixed dollar return. |
| Training Agreement`.9001` | UAE**25PP** | UAE spends **2%U**. No treasury payment to the partner. UAE gains **+15ArmyXP and−5% training time for730days**. | Real experience plus temporary benefit. The partner supplies agreed expertise; it is not forced to pay or supply troops. |
| Technical Exchange`.10001` | UAE**25PP** | UAE spends **2%U**, gains **+10productivity points per controlled UAE state**. Partner gets no cash/productivity reward from this variant; recipient cooldown730days. | Meaningful small-country productivity gain. Explicitly distinguish this one-sided training result from the Arab variant's two-country benefit. |
| Procurement Quotation`.11001` | UAE**25PP** | **No money or equipment moves when the seller quotes.** It proposes1,000existing1965 infantry-equipment units for$250m; actual transfer requires buyer confirmation`.90001`. | This MD equipment represents Rifle Squad packages, **not1,000literal individual rifles**. Assess price against those package units/native balance. Still a large36.44%of baseline UAE GDP. |
| Islands Settlement`.12001` | UAE**35PP** | Cash0. Accepted full arbitration creates mirrored status ideas/flags. A narrower Iranian access proposal opens`.80001`. Neither response transfers a state, oil or military access by itself. | **Weak mechanical incentive at present:** recorded RP status has no independent modifier or territorial result. This is deliberate arbitration/status, not a missing promised annexation. |
| Saudi Border Talks`.13001` | UAE**35PP** | Cash0. Adds the bilateral border-accord status ideas/flags. No state transfer, oil transfer or separate opinion modifier is executed. | **Weak mechanical incentive:**35PP for recorded recognition only. Do not claim an economic/treaty modifier that is absent. |
| Legacy UAE Gulf Charter`.14001` | UAE**50PP** | Every new participant pays **2% of its own frozen GDP**. Recipient pays2%R; UAE pays2%U only if not already a member. Each gains the native GCC membership idea. | Meaningful native bonuses, but duplicates the common charter UI and has weaker sovereignty/expulsion guards; see diplomacy audit D2. No repeated entry fee for an existing UAE member. |
| Financial Support for Kuwait`.15001` | **35PP already paid** for Kuwait menu; **0additional** | UAE pays **3%U** ($20.58m at baseline), Kuwait receives exactly that amount. | A real, recipient-approved aid transfer. No war entry or deployment purchased. |
| Britain Proposes Continued Protection`.16001` | Britain**0PP** via its policy menu | Cash0. UAE acceptance renews protection and retains the applicable dependency penalty instead of scheduled freedom. | Same substantive terms as protection offered from the UAE side; origin does not create a second payment. |
| Britain Offers Earlier Release`.17001` | Britain**0PP** via its policy menu | Cash0. UAE accepts immediate independence or refuses and retains the prior timetable. | Independence is not sold and refusal does not abolish the prior schedule. |
| Agreed Transition Date`.18001` | UAE**35PP already paid** for Amendment menu; **0additional** | Cash0. UK acceptance replaces the current timetable with a deadline **360days after the proposal was sent**. | The deadline is frozen at proposal, not reset when the recipient finally clicks. No payment and no fresh approval at the agreed handover date. |
| Kuwait Transit`.19001` | UAE**35PP already paid** for Kuwait menu; **0additional** | Cash0. UAE grants Kuwait military access through UAE territory after Kuwait agrees. | Useful access permission, not troops or automatic participation in a war. |
| Kuwait Deployment Access`.20001` | UAE**35PP already paid** for Kuwait menu; **0additional** | Cash0. Kuwait grants UAE military access. Existing forces and war decisions remain player-controlled. | No deployment fee or spawned contingent is secretly included. |

Native GCC membership currently gives **+10% political-power gain,+10% trade
opinion factor,+10% oil/aluminium/rubber/tungsten/steel/chromium resource
output**. It also registers the country in the real GCC member array. It does
not itself create a military faction or complete the common GCC focus branch.

## Three counterproposal/buyer-confirmation types

| Type / first event | Extra PP for this popup | Confirmation cash and result | Assessment |
|---|---|---|---|
| Britain's Friendship Counterproposal`.70001` | **0**; retains the original protection route's0or35PP charge | Cash0. UAE confirmation delivers immediate release and the agreed friendship status. Any friendship-focus productivity/research bonus still requires that focus to have been earned. Refusal preserves the existing release schedule. | A new consent step, not a second negotiation fee or automatic free completion of the friendship focus. |
| Iran's Abu Musa Counterproposal`.80001` | **0**; original islands decision already cost35PP | Cash0. UAE confirmation records **Abu Musa access talks only** in both countries. Tunbs dispute remains unresolved; no actual territorial or military-access transfer occurs. | Another RP agreement with a weak immediate mechanical reward. Its narrower scope must not be described as resolution of every island dispute. |
| Buyer Procurement Confirmation`.90001` | **0**; procurement request already cost25PP | Buy: **UAE−$250m / seller+$250m**, seller stock−1,000 / UAE stock+1,000 of the1965 Rifle Squad equipment type. Decline: no money or equipment transfer. | The actual purchase occurs here once, with live funds/stock checks. Price is per1,000MD equipment packages, not individual rifles. The stale-decline defect in audit D1 is a separate bug. |

## Three common GCC types

| Type | Opening expense | Actual cash/result | Assessment |
|---|---|---|---|
| A Gulf Cooperation Charter`COLDWAR_GCC_1970.<origin><round>` | Initiator**50PP once** | Each new participant pays **2% of its own GDP frozen when the offer is sent/delivered**. Existing initiating members pay no second entry contribution. Adds native membership, initializes minimum unity/dominant-member handling and makes the common member-only focus branch usable under its own conditions. | Same named entry ratio as the old UAE offer, now sovereign-only across all six founders. Entry is not the sum of both countries' GDP charged to one payer. |
| The Gulf Charter Is Agreed`COLDWAR_GCC_1970.1` | **0additional PP** | **0additional cash**. Notifies the sender after the recipient has signed and the actual entry invoices have already executed. | Never add another2%invoice for this informational popup. |
| The Charter Invitation Is Declined`COLDWAR_GCC_1970.2` | **0additional PP** | **0cash**. No admission, no entry contribution; initiating50PP remains spent. | Notification only; it does not remove an existing membership or apply a financial penalty. |

## Sensibility and clarity issues to retain in the user-facing review

1. **Delegation50PP has no enacted effect.** It is the clearest poor-benefit
   event; status text cannot substitute for the promised constitutional change.
2. **Islands/border agreements are RP status only.** Their35PP can be an
   administrative negotiation cost, but the player should know no numerical,
   territorial or actual-access outcome is delivered. Do not invent a hidden
   advantage to justify the price.
3. **Cabinet relief and burden must be shown together.** Up to3points of
   permanent bureaucracy relief is accompanied by+3%cabinet upkeep; the net
   budget effect is not automatically a saving. The office settlement is the
   main distinctive outcome.
4. **Large foreign benefits at small UAE prices:** Arab exchange grants a
   per-state gain to the partner while charging only2%of UAE GDP. Its effect
   can be much greater for a large country than for a Gulf microstate. This is
   an explicit balance concern, not a historical fact or a failing transfer.
5. **Procurement and UK co-financing are each$250m.** They are about36.44%of
   the starting game GDP. That is a substantial budget choice. Procurement
   must be assessed as Rifle Squad packages; calling them literal individual
   rifles badly misstates what the native equipment units represent.
6. **Frozen start GDP becomes less demanding later.** Court settlement,
   mediation and Sharjah negotiation retain$34.30m/$20.58m/$13.72m prices even
   after the economy expands. Current-GDP exchanges/equity/aid grow with the
   economy. This is current intentional implementation and should be visible.
7. **Some expense is only incurred if the player agrees.** Do not total both
   exclusive Sharjah options, all Kuwait choices, both reserve withdrawals,
   both charter settlements or accept+decline. Do not count each of128round
   copies as a fresh automatic fee. A voluntary later retry can incur its own
   new decision PP, but a child popup does not.
8. **The35PP Kuwait menu is a single selected response.** Sending financial
   aid, transit or deployment does not add a second35PP. Only the separate
   civil-protection choice immediately spends1%of the GDP quote made when
   that menu opened.

No values were changed by this ledger. Historical justification, repricing
and any implementation repair remain separate from this source inventory.
