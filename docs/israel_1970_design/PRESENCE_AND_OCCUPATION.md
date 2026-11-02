# IMPERIA COLD WAR: Settlement presence and the cost of occupation

Historical prototype record. The foreign-presence agreement terms in this file
were superseded on 28 October 2026 by `UNILATERAL_SETTLEMENTS.md`: the host no
longer grants permission, receives money or earns positive settlement rewards.
The occupation profiles and controlled construction described below remain.

Implemented on 27 October 2026 after the earlier tree rework. That version
had 399 focuses, 198 decisions and 77 events. The added ten focuses form two
independent programmes. Their numerical effects are balance proposals, not
historically measured percentages.

The subsequent Palestinian-country consequences, two regional tiers and funded
compensation relief are recorded in `PALESTINIAN_PRESSURE.md`. They apply only
to an existing Palestine with actual West Bank or Gaza settlement activity.

## A benefit linked to a state outside Israeli control

Four distinct focuses offer civilian settlement holdings and a marketing compact
in the West Bank, Gaza, Sinai or Golan. The actual government owning and controlling
the area receives acceptance, refusal and termination decisions. Israel's offer
does not move a border, grant a core, change control or create population. A state
with different owners and controllers cannot conclude this compact until its
authority is resolved. Political party or historical diplomatic dates do not
select another RP country's answer.

The state displays **Israeli Civilian Settlement Presence**, linked to Israel's
national **Israeli Settlement Holdings** programme for that particular area.
This extra national programme supplies the Israeli benefit when Israel is not
the controller; an ordinary state modifier alone would benefit the controller.

| Recipient | Prospective terms per state |
| --- | --- |
| Israel | Office productivity +4%, agricultural productivity +3%, social costs +1%, bureaucracy costs +1% |
| Host government | Agricultural productivity +2%, bureaucracy costs +1% |
| Named state | Infrastructure construction speed +10% |
| Capital | Israel transfers 1% of its annual GDP to the accepting host, once per state |

The amount is quoted at the proposal and transferred only when the real host
accepts and Israel can cover the same amount. A refusal transfers nothing. A
duplicate acceptance cannot charge or pay again. Previously paid capital is
retained if the agreement is later renegotiated: the new capital payment is zero.
The focus and host acceptance tooltip always show both countries' full prospective
numeric terms, including when locked or not yet accepted. These displays contain
no fiscal provider or real modifier grant.

Both governments can terminate an agreement. War, either country's embargo,
any of the four mirrored Imperia sanction classes, Israeli control, a different
host or divided ownership/control suspend the benefits. Restoration reactivates
the programmes without another transfer. The saved host's exact identity is
checked again during acceptance, refusal and termination, including after country
destruction/recreation. Refusal can be followed by a new Israeli proposal.

This is a negotiated alternative-history RP option. Research found no accepted
1967-1973 agreement establishing this exact Israeli civilian-presence arrangement
under restored Palestinian, Egyptian or Syrian sovereignty. It adapts period
cooperative, property, marketing and cross-border economic institutions into a
player-controlled diplomatic choice.

## A separate programme under Israeli control

Four additional regional focuses unlock funded construction in the named state.
Each project costs 1.5% of annual GDP and 25 political power, takes 270 days and
grants:

- One agricultural district, one infrastructure level and one land-fort level.
- Three shared building slots before construction.
- Local supplies for Israel +10%, paired with local garrison requirement +10%.

The project requires actual Israeli control, the appropriate legal owner,
staffing, state capacity and control/capacity of its actual fort province. A
binding freeze or settlement ceiling prevents construction in the selected
Palestinian project area, including if it is enacted during an outstanding
project. Failed delivery refunds the stored reservation exactly. Buildings
remain in their state on later withdrawal. These projects complement the earlier
limited, expansive and compensated settlement routes; they do not unlock a core.

## Starting regional occupation burdens

The current January 1970 map has Palestinian ownership of states 208/209,
Egyptian ownership of 213 and Syrian ownership of 587, with Israeli control and
no Israeli core. Each receives a separate **Military Administration** state
modifier and a separate Israeli **Administration and Security Budget** modifier.

| State | Starting resistance / compliance | Added target | Garrison need | Garrison damage | Local factory access | Local supply |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| West Bank | 18 / 25 | +15 points | +40% | +20% | -15 points | No change |
| Gaza | 25 / 15 | +25 points | +60% | +35% | -20 points | No change |
| Sinai | 8 / 30 | +5 points | +20% | No change | -10 points | -12% |
| Golan | 10 / 20 | +8 points | +25% | No change | -10 points | -5% |

| Israeli weekly budget component | West Bank | Gaza | Sinai | Golan | All four controlled |
| --- | ---: | ---: | ---: | ---: | ---: |
| Police cost modifier | +5% | +8% | +2% | +2% | +17% |
| Bureaucracy cost modifier | +3% | +4% | +3% | +2% | +12% |
| Personnel cost modifier | +2% | +3% | +8% | +5% | +18% |

These are additive modifiers to the native weekly MD spending components, not
percentages of total GDP or flat cash charges. Native garrison manpower,
equipment losses and resistance thresholds operate in addition. Gaza emphasises
internal security; Sinai and Golan emphasise frontier personnel and supply.

Actual resistance and compliance are set only during the first reconciliation,
before February 1970. The generic engine history defaults would otherwise start
at zero resistance and 70 compliance, obscuring much of the occupation burden.
The new values are never reset daily. Existing later saves keep their earned
resistance/compliance; they receive only the applicable profiles and costs.
Later uprisings follow native conditions, not a new dated event sequence.

Control loss disables the local modifier and removes Israel's country budget
modifier. Recapture restores the modifier without resetting resistance, repeating
a fee or granting assets. Unilateral annexation of a non-core state does not
remove these costs. Genuine core integration through the existing guarded system
does end the non-core profile. Existing municipal agreements and practical
administrative programmes remain ways to reduce individual burdens.

The existing Israeli cores in East Jerusalem and West Jerusalem are retained.
Their map/core treatment was not changed or overridden with forced resistance.
No additional workforce-size bonus or penalty was introduced; the earlier shared
workforce programme remains capped at +15% in total.

## Historical and native references

- [ICRC, June 1968](https://international-review.icrc.org/articles/application-geneva-conventions-particularly-fourth-territory-occupied-israel):
  contemporary delegations and civilian-protection work across the West Bank,
  Gaza-Sinai and Golan. This establishes distinct administrative settings.
- [ICRC report, September 1970](https://tile.loc.gov/storage-services/service/ll/llmlp/65002328_RC_Sep-1970/65002328_RC_Sep-1970.pdf):
  period civilian relief and public-service needs, including Gaza-Sinai and Golan.
- [IDF institutional account of the War of Attrition](https://www.idf.il/en/mini-sites/wars-and-operations/the-war-of-attrition/):
  the military-front and security context. This is a conflict participant's
  institutional account, not a neutral measurement of civilian attitudes.
- [FRUS, 2 March 1971](https://history.state.gov/historicaldocuments/frus1969-76v23/d214):
  discussed arrangements and guarantees as alternatives to territorial retention.
  It does not establish acceptance of the new civilian compact.
- [Bank of Israel, Annual Report 1972, chapter IX](https://www.boi.org.il/media/ti3nzv2j/pe_9.pdf):
  period economic and employment links with the administered areas. These support
  economic interdependence, not a new automatic workforce reward.

Native scope and unit evidence comes from the installed HOI4 documentation and
current MD occupation laws. `resistance_target = 0.15` is a 15-point target
increase; `set_resistance = 18` sets strength to 18 points. Country police,
bureaucracy and personnel modifiers are read by the native budget calculations.

MD's custom economy already counts population and raw building levels of all
controlled states. Therefore a local factory-access penalty alone does not
establish a matching reduction in MD GDP/taxes. The extra country spending is a
real additional fiscal burden; this revision does not claim to rewrite that
global economic accounting model.

## Validation and provenance

`validate_presence.py` passed 581 emitted-AST model and structural checks, covering
real host scope, frozen capital, duplicate and stale responses, refusal, funds,
war/embargo/sanction suspension, restoration, dead countries, occupation seeding,
control/core changes, project slots and refunds. Existing content, reward, layout,
policy and reference checks also pass. The full tree has 399 positions and 440
visible prerequisite connectors. Browser results are recorded separately in
`preview_validation.json`. Source/model tests do not establish native tooltip,
save/reload, economy-cache or multiplayer/rehost behaviour; no HOI4 live test ran.

New code and English narrative were authored for this project with Codex. Existing
Millennium Dawn/Cold War icons are reused without pixel edits. Credit belongs to
the existing contributors; individual original artists and separate asset
licences/redistribution permissions are unknown. No new visible country event or
event picture was added; the four new project callbacks are hidden. Preview PNGs
are browser-rendered compositions, not live game screenshots.
