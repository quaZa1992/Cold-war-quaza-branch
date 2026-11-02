IMPERIA COLD WAR

# Kissinger foreign-policy concept: independent history and mechanics review

Design-only review, 2026-10-28. No loaded script, country history, focus tree,
modifier, approval snapshot or asset was changed by this review. Proposed new
campaign behaviour remains unimplemented and has not been tested in HOI4.

## Historical boundaries

Kissinger begins this scenario as National Security Adviser, the office he held
from January 1969. His Secretary of State appointment belongs to September 1973.
A 1970 portrait should depict the middle-aged, dark-haired Kissinger with his
characteristic spectacles, rather than the elderly public figure of later years.
The NSC and its covert-action review machinery provide a sound institutional
entry for a programme that can continue under later administrations. The
303 Committee became the 40 Committee on 17 February 1970. A general NSC review
entry avoids giving a January start a prematurely named institution.
Sources: [State Department biography](https://history.state.gov/departmenthistory/people/kissinger-henry-a),
[FRUS covert-action machinery](https://history.state.gov/historicaldocuments/frus1969-76v06/actionsstatement),
[Nixon Library NSC structure](https://www.nixonlibrary.gov/national-security-council-structure-and-functions).

| Country | Historical starting relationship and actors | Design classification |
| --- | --- | --- |
| Iraq | Iraqi Kurdish aid through Iran is a documented Nixon-Kissinger policy from 1972. Barzani's organisation is the appropriate early counterpart. | Historical core route, with alternative escalation beyond the actual policy. |
| Iran | The Shah's Iran was a close American regional partner and the conduit for aid into Iraq. The PDKI existed from 1945, but a US campaign against the Shah is not the historical default. | Partner/transit route by default. Hostile campaign requires a visible break with Tehran or a different regional alignment. |
| Turkey | NATO member since 1952. A US programme deliberately sponsoring revolt against this ally is an alternative policy with substantial alliance consequences. | Counterfactual hostile route. Cultural or diplomatic advocacy must remain distinct from arming an insurgency. |
| Syria | Diplomatic relations were severed in 1967 and restored in 1974. Early Kurdish political organisations existed, but modern PYD/YPG/SDF institutions do not belong in 1970. | Plausible alternative covert pressure, not a claimed historical Kissinger Kurdish programme. Retain a diplomatic accommodation alternative. |

Sources: [FRUS Kurdish assistance proposal](https://history.state.gov/historicaldocuments/frus1969-76ve04/d321),
[FRUS Iran/Iraq volume preface](https://history.state.gov/historicaldocuments/frus1969-76ve04/preface),
[NATO Turkish accession history](https://www.nato.int/cps/en/natohq/declassified_191048.htm),
[State Department Syrian diplomatic history](https://history.state.gov/countries/syria),
[PDKI organisational history](https://pdki.org/english/about/).

The most directly relevant primary document is Kissinger's April 1974 memorandum:
aid was intended to strengthen the Kurds' negotiating position and keep the Iraqi
government occupied internally, restricting its scope for regional adventures.
It supports a costly strategic-diversion game rather than a guaranteed American
button that creates a loyal independent country. All US aid was channelled
through Iran; its withdrawal after the March 1975 Algiers agreement contributed
to the resistance's collapse.
Sources: [FRUS memorandum 246](https://history.state.gov/historicaldocuments/frus1969-76v27/d246),
[CIA termination memorandum](https://history.state.gov/historicaldocuments/frus1969-76v27/d289).

Historical budget precision matters. The 1972 proposal specified approximately
$3 million in annual cash and $2 million in ordnance, excluding transportation.
The existing game's $0.05 billion/week is a balance amount, not that historical
budget. If used in a preview, label it as an existing gameplay benchmark. A
literal historical annual cash conversion would round to $0.00006 billion/week
under the project's five-decimal rule, rather than a long fixed-point literal.

Do not introduce the PKK in a 1970 start: it was established in 1978. PYD was
formed in 2003, YPG emerged in 2012, and SDF was created in 2015. The PUK was
founded in 1975; its predecessors or Talabani-associated networks are not an
already established PUK state in 1970. Current runtime already has a
`puk_formed` condition that must survive any redesign.
Sources: [US NCTC PKK history](https://archive.dni.gov/nctc/terrorist_groups/pkk.html),
[USIP report, Kurdish-group chronology](https://www.govinfo.gov/content/pkg/GOVPUB-Y3_P31-PURL-gpo126197/pdf/GOVPUB-Y3_P31-PURL-gpo126197.pdf),
[PUK founding history](https://pukmedia.org/EN/Details/81645).

## Existing reusable Iraq implementation

Authoritative sources are `tools/iraq_1970/usa_module.py` and the bounded USA
integration in `tools/usa_1970_expansion/gulf_revision.py`. The latter replaces
the fifteen existing Gulf IDs while preserving other US focus blocks. The
current old graph still places appeal, contacts and the arms choice below
Desert Storm. The requested design can move covert contacts into an earlier
institutional foreign-policy section without making Kuwait intervention depend
on those contacts.

The existing system already supplies:

- Four bounded northern Iraqi states: 164, 633, 630 and 1078. Their source files
  identify Iraqi Kurdistan, Dohuk, Sulaymaniyah and Halabjah. These are not a
  ready-made cross-border map or a warrant to claim every mixed-population area.
- Real Iranian or Turkish frontier consent plus military access for clandestine
  support. Distant basing alone does not supply the underground. Local playable
  governments accept their own assistance terms.
- A $0.25 billion setup package and 1,000 actual infantry weapons committed to
  a recorded cache, followed by a 90-day support commitment at $0.05 billion/week.
- Iraqi security decisions with a one-time 2% or 4% GDP invoice and a 90-day
  overhead package. Small/large operations add +35%/+60% army personnel costs
  and +20%/+35% equipment upkeep respectively.
- At least two actual Iraqi divisions in the northern state set for 30 days
  before the funded security reduction. This is a division-count test, not
  proof of local combat strength, equipment sufficiency or supply weighting.
- Two tracked states at resistance 80 or above, a military opening, a remaining
  cache and 30 qualifying days before a 45-day warning period. Fifteen days
  below the conditions reset the accumulated crisis. The warning is not the
  whole campaign length.
- Political settlement, accepted self-government and a separate external
  protection alternative. A respected settlement resolves the grievance and
  turns off the hostile programme.
- Kuwait-war access that also recognizes annexation, occupation and Iraqi
  subordination of Kuwait. Its US liberation wargoal does not automatically
  declare war and is not conditional on finishing the Kurdish branch.

These are source observations. Reuse the owner and preserve existing receipts,
cash/equipment accounting, host acceptance, troop presence, warning and
settlement contracts. A new system should not run alongside this system and
double-charge, double-seed resistance or duplicate a rebellion.

## Mechanic vocabulary verified in the checkout

| Modifier/effect | Provider and actual consumer | Correct proposed use |
| --- | --- | --- |
| `foreign_influence_modifier` | `common/modifier_definitions/influence_modifier_definitions.txt`; read in `common/scripted_effects/00_influence_scripted_effects.txt` | American diplomatic/influence capability. Does not automatically add insurgent strength. |
| `foreign_influence_defense_modifier` | Same provider and reader | Foreign political-pressure resistance. Does not automatically suppress a scripted regional campaign. |
| `army_personnel_cost_multiplier_modifier` | `money_modifier_definitions.txt`; `00_money_system.txt` around 3235 | Funded military-overhead burden on the country actually maintaining troops. |
| `equipment_cost_multiplier_modifier` | Same money provider and reader around 3239 | Increased equipment operating costs, not equipment destruction or a one-time weapons transfer. |
| `bureaucracy_cost_multiplier_modifier` | Same money provider; bureaucracy computation around 3367 | Administrative programme costs, not a substitute for every foreign-policy trade-off. |
| `police_cost_multiplier_modifier` | Same money provider; reader around 3397 | Appropriate for a funded domestic security programme. |
| `encryption_factor`, `decryption_factor` | Installed native modifier documentation | Cryptology rewards. They are not generic covert-action success or local intelligence-network gauges. |
| `agency_upgrade_time` | Installed native modifier documentation | Agency upgrade speed. A negative value is faster; do not present it as insurgent combat strength. |
| `additional_expenses_rate`, `additional_income_rate` | Existing MD recurring-money accumulators and US agreements integration | Weekly budget streams. The amount must be added once per relevant calculation and cease with the programme. |

Existing concrete spirit bundles provide useful native presentation examples:
`COLDWAR_USA_gulf_northern_air_readiness`,
`COLDWAR_KUR_coalition_air_cover`, `COLDWAR_KUR_us_advisers`,
`COLDWAR_USA_gulf_security_small`, `COLDWAR_USA_gulf_security_major`,
`COLDWAR_USA_gulf_recognised_budget` and
`COLDWAR_USA_gulf_recognised_development` in
`common/ideas/COLDWAR_USA_gulf_ideas.txt`. These combine real capability,
continuing costs and conditional operation. They are not permission to give
permanent free combat buffs or duplicate their effects.

## Cross-country multiplayer design recommendations

1. Maintain separate host/state/faction campaign ledgers. The four country tabs
   share a ruleset, not one global Kurdish allegiance or one global revolt bar.
   Do not reuse an existing Iraq-player `KUR` or `PUK` tag as the new rebel state
   in Turkey, Iran or Syria. A multi-country actor/release design needs its own
   explicit ownership and playable-tag review before implementation.
2. Show a funded early-contact stage, a materially stronger arms commitment and
   an explicit public escalation. The target gets meaningful warning and can
   spend on real deployment, administration, negotiations or local development.
   Discovery, parliamentary objections and loss of access provide American
   counter-costs. A proposed organisation/exposure gauge is new script work;
   the native influence modifiers do not implement it automatically.
3. Preserve local political agency. Existing Kurdish players accept their own
   offers and choose between a negotiated settlement and independence. A
   nonexisting country is represented by an underground movement, not a treasury
   that receives cash or equipment before it exists. An independent state is an
   alternative successful outcome, not the historical mandatory 1991 reward.
4. Iran and Turkey require visible strategic forks: sustain the partner, pressure
   the partner or break with it. Targeting a NATO ally is not an ordinary cheap
   operation. Show the actual `NATO_member` condition where relevant. A crisis
   can let allies choose their response; do not silently expel another human
   government from NATO or confiscate its forces.
5. Gulf escalation stays independent: Iraqi aggression against Kuwait opens
   Desert Shield, coalition diplomacy, ultimatum and Desert Storm. Defeat and
   diminished control create an opportunity for a Kurdish rising. A player may
   have invested in contacts before the Kuwait war, but those investments are
   not required to defend Kuwait.
6. Both nonviolent leverage and armed commitment need attractive endings.
   Negotiated autonomy offers lower future military costs and a durable local
   budget, while armed self-government provides stronger local security at
   greater US expense and diplomatic risk. Do not make one choice a bundle of
   penalties or force independence where a respected settlement was accepted.
7. Restrict recurring work to active campaigns and their known states. Do not
   add daily worldwide scans for all four potential targets. Generalizing native
   resistance into new cores, new occupied identities or new playable tags is
   not a cosmetic copy and needs separate native/save/multiplayer verification.

The numbers above describe existing Iraq gameplay or explicitly identified
historical budgets. New regional coefficients, operation costs and success
curves are balancing proposals until specified and tested. Source-level support
for a modifier does not prove that a new four-country minigame works in engine.

## Provenance

Sources are the current local IMPERIA COLD WAR providers, installed Paradox
documentation and the linked primary government/archive records. Party-owned
history is identified as such. This note adds design analysis only and copies
no images or other binary assets. Original authorship and permissions remain
under the original notices and `IMPERIA_COLD_WAR_NOTICE.md`; individual credits
or licences are unknown where those notices do not identify them.
