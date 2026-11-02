IMPERIA COLD WAR

# Independent concept review: corrected USA expansion

Reviewed on 24 October 2026. Review scope: `build_proposal.py`, its emitted `proposal.json`, relevant current US diplomacy/law/history files and the project skill contracts. This is a design review, not a native implementation or multiplayer test.

Reviewed proposal SHA-256: `f524a00e9ab934872d748994b5de1ac89608a791de6cf6b28b0d7c55b142cfa8`.

Review refreshed after bounded final changes: the four 1980 choice entries and their four follow-ups moved to rows 33 and 34; the foreign-policy footprint was tightened to columns 10 through 19 following a separate overlap review; all 13 reworked focuses now preserve their existing focus cost multiplied by seven as the displayed duration. Rewards, quoted bilateral terms, requirements, exclusions and the agreement lifecycle are unchanged by these final adjustments. The substantive findings below therefore remain applicable. This refresh verifies the catalogue changes and timing preservation; it does not claim native or rendered geometry validation.

The corrected concept is suitable for player review. It contains 13 reworked and 52 new focuses, including 16 recipient-approved programmes. The projected full-tree count is 281. These counts describe the design data, not newly installed game content.

## Findings corrected in the reviewed catalogue

| Finding | Corrected result |
| --- | --- |
| South Vietnam recipient was provisional | The advisory mission explicitly targets SVN. VIE remains North Vietnam. |
| Foreign doctrine changed undisclosed partner bills | Offers now have fixed setup and weekly terms. Each doctrine grants its own package instead of modifying quoted payments. |
| Energy audit showed a temporary penalty inside a standing spirit | `Retrofit Adjustment` is explicitly listed for 730 days. The standing energy-efficiency gains are separate. |
| Bilateral continuations depended on missed first-term Nixon focuses | Japan, South Vietnam, China and Soviet exchange now have OR entry through permanent foreign-policy focuses. Old focus completion is optional, and an old refusal does not permanently veto a fresh offer. |
| Recruitment reform could omit the real native law change | Volunteer and draft law consequences are explicitly distinguished from the small additional programme spirits. The design no longer treats recruitment reform as only an organisation bonus. |
| Restoration rules did not fully specify renegotiation | Persistent country-and-agreement-family receipts survive termination and renegotiation. Buildings, research bonuses and experience cannot be farmed by reopening. Formal exercise renewal remains a separately priced programme. |
| Bahrain facility partnership had only a prose conflict with cession | The new node explicitly excludes `COLDWAR_USA_bahrain_base_request`, requires no signed cession and has a reciprocal exclusion in the rewiring data. |
| Rogers talks inherited a two-country peace condition | The three-party mandate now checks USA-Egypt and USA-Israel relations. Egyptian-Israeli war or sanctions do not themselves prevent talks. Both recipients must accept before any participant receives the package. |

The main diplomatic contracts preserve human authority. They do not impose a government, faction, war, peace settlement, border change, recognition decision or resource delivery. Partner follow-ups require new acceptance. Government changes can deactivate party programmes without automatically cancelling a state treaty. Standing agreements have no fixed expiry; temporary deadlines run from final acceptance and continue during suspension.

## Balance and historical assessment

The proposals make different kinds of rewards attractive: actual industrial capacity, production retention, limited research and doctrine bonuses, professional training, logistics, sector efficiency and funded institutional cooperation. The industrial, civil, energy and military choices have different benefits and costs instead of repeating tiny PP/stability gifts. Ordinary complementary development remains shared. China opening and Soviet detente remain compatible.

The German forward-defence and sustainment settlements give both countries a reason to negotiate either option. The USA trades forward readiness against local support and personnel relief; Germany trades immediate military readiness against industrial and logistical capacity. The nominally equal US flat net running bill does not make the total economic cost equal, because personnel and equipment multipliers also matter.

A theoretical overlap of the 15 compatible offer packages, choosing either German variant, costs the USA $77.00 billion in setup expenditure. Gross flat weekly expenses are $0.19 billion with the forward-defence variant and $0.04 billion in matched German/Saudi income, leaving $0.15 billion/week net. Choosing German sustainment changes the gross composition but has the same flat net. This is an upper-envelope catalogue sum across different unlock dates and durations. It is not a prediction of a normal campaign or a total fiscal burden: native personnel, equipment, tax and other costs are additional.

Historical boundaries are handled appropriately: the Auto Pact expands an existing 1965 relationship; Okinawa state 618 is already Japanese in the current map and base state 827 is separate; Saudi institutional cooperation is a 1974 continuation or an explicitly early negotiated alternative; the Moscow science package does not claim to implement SALT. Rogers talks do not silently enforce the historical ceasefire or a later peace settlement.

The Mexican programme can now be sourced more firmly than its provisional technical note suggests. The [Mexican Ministry of Economy account](https://www.economia-snci.gob.mx/sic_php/pages/importa/abc_maquiladora.php) dates the policy to 20 May 1965 and identifies Ciudad Juarez in 1966 and Nogales in 1968. A [contemporary 1971 Congressional Record account](https://www.congress.gov/92/crecb/1971/11/04/GPO-CRECB-1971-pt30-3-3.pdf) describes the original border programme and temporary duty-free component imports for export assembly. These substantiate industrial integration, training and fiscal trade-offs. The exact bilateral focus package remains proposed balance.

## Checks performed and remaining limits

Read-only catalogue checks passed for unique IDs, SVN routing, the explicitly timed retrofit row, later-president entry alternatives, Bahrain exclusion, the Rogers relation exception, symmetric exclusions between concept nodes, named effects for the USA and partners, and at most five fractional digits in quoted flat weekly amounts. The final refresh additionally checked all 13 reworked durations against the current inventory's cost multiplied by seven, and the 1980 additions at rows 33 and 34. There are 65 unique concept nodes and 16 offer nodes in the reviewed output.

The native NATO membership provider exists as `NATO_member` in `common/ideas/Factions.txt:5`. Exact party predicates exist in `common/scripted_triggers/01_political_triggers.txt:176` and `:183`. These are verified implementation anchors. The catalogue's generic membership wording must eventually map to the real idea in both availability and reward execution, including member-only entry nodes.

Before implementation can be called complete, the following remain necessary:

- Reconcile each reworked package with existing US dynamic helpers, starting burdens, native army laws, party programmes and recipient events. A new named package must replace the same old benefit rather than add a duplicate layer.
- Verify exact MD modifier consumers and technology/doctrine categories. Proposed values are not proof of registered APIs, and global country modifiers may only approximate a sector-specific policy.
- Integrate flat recurring payments into actual native weekly income and expense consumers. Match each transfer at both ends and avoid copying the existing Gulf daily high-precision deductions.
- Select actual owned, controlled eligible states/provinces and native construction capacity. Grant the promised extra slot before every building level in the same one-time transaction.
- Implement the quoted offer lifetime, replay receipts, parent dependencies, cancellation and suspension contract. Show identical complete signed terms in focus, recipient option and inspector even when eligibility is false.
- Test actual event arrival, atomic three-party acceptance, funds/debt policy, weekly boundaries, co-op/repeated input, refusal, sanctions, expiry, parent failure, save/reload and genuine network rehost.

No native game load, hover, budget execution, construction, save migration or multiplayer behavior was observed in this review. No runtime scripts were changed. The design review supports the direction and the concrete corrections above; it does not certify final numerical balance or engine behavior.
