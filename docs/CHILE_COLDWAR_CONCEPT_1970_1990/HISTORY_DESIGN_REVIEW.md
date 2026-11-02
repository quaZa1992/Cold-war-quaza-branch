IMPERIA COLD WAR
# Chile 1970-1990 design: historical review

**Scope:** Historical and institutional review of `COLDWAR_CHL_design.json`. Reviewed its 184 focus nodes across 11 political programmes, seven starting/conditional spirits, 13 events and nine proposed agreements. This review proposes corrections only; it makes no design-catalogue or runtime edits. Money values in the concept are game-balance terms, not historical treaty prices or reported programme budgets.

## Correct as represented

- January 1970 starts under Eduardo Frei Montalva and the PDC; Allende, Alessandri and Tomic are the three candidates. The 1970 election and congressional-ratification events appropriately avoid immediate accession and keep the actual outcome/leader route conditional.
- The concept distinguishes the Allende-led Socialist path from the Communist and Radical coalition partners, and gives the congressional/cross-party route a meaningful constitutional alternative.
- The military route is not active at the January start. Its entry requires a real military transfer, and Pinochet-specific command requires him to be the actual leader. These are sound safeguards against putting Pinochet in office early.
- It presents copper as a fiscal/export exposure, not a copper mine or raw-resource-production claim. The concept metadata correctly says the modifier is a broad `resource_export_multiplier_modifier` proxy. Keep this limitation explicit in any tooltip/design handoff: the reward affects aggregate resource-export revenue, not copper tonnage or a copper-specific national resource.
- Bilateral contracts are generally marked with the right epistemic status. US terms, exact Soviet projects, Japan port equipment, the Chile-Cuba health exchange, the Peru protocol, Bolivia port improvements and French technical programme are all labeled proposed/alternate terms. The 1984 Chile-Argentina settlement and 1969 Cartagena framework are real precedents, while their exact reciprocal project terms and game costs are identified as proposals. Preserve that distinction; none of the numbers is a historical dollar amount.

## Required historical corrections

1. **Do not present MIR as a normal parliamentary governing programme.** MIR was outside the UP coalition and rejected the parliamentary road, although it accommodated Allende and worked alongside parts of the government. The current nine-focus “MIR and the Revolutionary Left” branch reads like an ordinary party-in-power alternative, with paths to a plural congress and a governing state. Retain it only as an explicitly counterfactual extra-parliamentary rupture route, with an actual revolutionary seizure/coalition condition and the resulting civil conflict, rights and legitimacy costs. If the concept does not model that rupture, remove the ruling-party programme and retain MIR as a smaller influence/mobilization event chain.

2. **Re-scope the Gremialist programme.** The Movimiento Gremialista began as a university movement in 1967, not as a national governing party in 1970. It became an influential regime collaborator after the coup. The UDI movement was organized in 1983 and registered as a legal party in 1988-89. A nine-focus party-in-power programme with no date or post-coup prerequisite makes the movement a free-standing 1970 electoral government. Recast it as a movement/influence route tied to the post-1973 regime and its institutional design, or as a post-1983 UDI/late-transition route. Do not call it a 1970 party or equate its later legal organization with the old National Party.

3. **Reduce the minor-party footprint.** PR, DR and PADENA currently have 11, 8 and 7 focuses respectively (26 total). The PR was a substantial historic party and UP partner; DR was a 1969 split that backed Alessandri and later had a modest CODE role; PADENA backed Tomic, recorded 1.9% in 1969, joined CODE in 1972 and won no 1973 seats. Keep a combined 10-12-focus parliamentary programme across PR/DR/PADENA, with PR carrying most of the depth and shorter, distinct minority choices for DR and PADENA. Their parties must gain office through an actual election/coalition change or an expressly labeled counterfactual event, not a no-cost focus switch.

4. **Keep the National Party within its real political window.** PN is a valid 1970 civilian conservative route. After the coup it publicly backed the Junta and relinquished direct political power; it attempted to reorganize in 1983, but its separate identity disappeared into Renovación Nacional in 1987. The post-1983/1987 conservative landscape included the UDI movement and RN, with UDI registered as a party in 1988-89. If the 1989-90 transition offers a civilian-right continuation, represent those successor formations through an explicitly alternate successor route; do not imply an automatic PN resurrection or use “Gremial” as a synonym for PN/UDI.

5. **Clarify Pinochet’s leadership sequence in the junta event.** Pinochet was the senior Army commander and chaired/led the junta from the September 11, 1973 coup. He assumed executive power as Supreme Chief of the Nation in June 1974 and the formal title President of the Republic in December 1974. The current “Presidency of the Junta” choice to “Concentrate the presidency under Pinochet” can suggest he was not the junta leader until that later choice. Keep the initial coup as a junta of the armed services and Carabineros, chaired by Pinochet; model June/December 1974 as the subsequent concentration and formalization of executive power. A “constitutionalist military leadership” belongs to the pre-coup settlement counterfactual, not as an actual 1973 junta faction. The current `actual national leader` check is useful but does not express these different offices/dates.

6. **Make repression an unavoidable part of the actual coup route.** The `event_rupture` coup option says only that military transfer activates the military branch; repression is then an optional event response or a later `National Security State` choice. That permits a clean Pinochet Chicago/reform/early-exit playthrough without recording the actual destruction of civilian institutions or ensuing detention, torture, killings and exile. Couple the actual coup route to dissolution of Congress and immediate repression/institutional rupture, then let `National Security State` deepen coercion and resistance. A civilian transition can end ongoing coercion, but it must inherit the documented human and institutional consequences. The full reparations/prosecution option should not simply erase every negative legacy spirit; separate the end of active repression from a persistent social, exile and accountability legacy. The existing limited-accountability spirit is a useful start, but the full-remedy route also needs to preserve unrecoverable harms.

7. **Add dates or accurate pre-reform framing for the Mapuche focus.** `Mapuche Land Guarantees` is available without a date even though its supporting statutory landmark, Law 17.729 and the Institute of Indigenous Development, dates to September 1972. Require the post-1972 legislative context or rename/reframe it as an earlier preparatory land/community policy with its own historical source. Do not grant the 1972 law in a January 1970 completion.

8. **Respect policy dates in the Pinochet economy branch.** “The Chicago Programme” can follow the coup immediately, although the rapid liberalization programme began in 1975. Either make it a dated 1975 choice or call an earlier focus economic planning/preparation and reserve the named policy effects for 1975 onward. Private pension capitalization is explicitly the 1980 pension law, effective in 1981; date it accordingly. The 1980 Constitution was approved under a heavily questioned plebiscite process, whereas the 1988 continuation vote used restored electoral rolls and formal scrutiny. Keep the credible 1988 plebiscite event tied to that later procedure and date; do not let it substitute for the 1980 constitutional vote.

9. **Enforce the Andean Pact's actual withdrawal.** Chile joined the 1969 Cartagena Agreement, then withdrew in 1976. A continuing membership spirit and its member-only focuses/offer can currently persist through the whole 1990 scenario unless another system removes it. Add the 1976 withdrawal/renegotiation decision: actual-history play exits membership, while continued membership must be a negotiated alternate route. Make the Andean agreement and industrial focus unavailable after withdrawal.

## Agreement provenance audit

| Offer | Historical precedent | Exact offer terms in this design |
|---|---|---|
| USA copper | Frei-era “Chileanization” and US mine participation are real. | The reciprocal engineering/compensation contract is correctly identified as proposed RP terms. Keep it available only with actual recipient consent; avoid describing it as an executed historic US-Chile deal. |
| Soviet machinery | Allende visited Moscow in 1972 and Soviet credits/supplier aid were extended. | Specific machinery project, price and state asset are proposed. Do not imply Moscow covered Chile's full external financing need. |
| Japan copper/ports | Japan was among diversified trade partners. | This long-term copper-for-port-equipment pact is correctly marked alternate history. |
| Cuba clinics | Castro's 1971 visit and restored diplomatic relations are precedent. | The named medical exchange and costs are proposed. Retain the diplomatic-relations requirement; it prevents the offer preceding restoration of relations. |
| Argentina/Beagle | Papal mediation (1979 onward) and the 1984 treaty are established. | The exact economic cooperation terms are proposed. Keep any offer after mediation/settlement steps, not as a completed 1970 agreement. |
| Peru maritime | Regional/Andean diplomacy is context. | This protocol is correctly labeled alternate history. |
| Bolivia transit | The 1904 treaty guarantees transit access, and later negotiations are real. | Expanded bonded handling/facilities are proposed. The “no sovereignty transfer or corridor” limit is historically important; retain it. |
| France technical | European diversification is context. | The named bilateral programme is correctly labeled alternate history. |
| Andean industrial protocol | The Cartagena framework and Chile's membership until 1976 are real. | Protocol terms, costs and specific industrial rewards are proposals. Require actual multi-country ratification and membership, and apply the 1976 exit rule above. |

## Direct source references

- Biblioteca del Congreso Nacional de Chile (BCN), UP history: identifies MIR as outside UP and distinguishes moderates/radicals: https://www.bcn.cl/historiapolitica/partidos_politicos/wiki/Unidad_Popular
- US FRUS, 1970-73 assessment of MIR: describes its rejection of parliamentary socialism and accommodation with Allende: https://history.state.gov/historicaldocuments/frus1969-76ve16/d116
- BCN, UDI and Gremialismo history: movement origins in 1967, regime role, UDI movement organization in 1983 and party registration in 1988-89: https://www.bcn.cl/historiapolitica/partidos_politicos/wiki/Partido_Uni%C3%B3n_Dem%C3%B3crata_Independiente
- BCN, Democracia Radical: formation, Alessandri support, CODE role and parliamentary scale: https://www.bcn.cl/historiapolitica/partidos_politicos/wiki/Partido_Democracia_Radical
- BCN, PADENA: 1969 result, Tomic support, 1972 CODE membership and 1973 loss of legal status: https://www.bcn.cl/historiapolitica/partidos_politicos/wiki/Partido_Democr%C3%A1tico_Nacional
- BCN, Partido Nacional: post-coup stance, 1983 reorganization attempt and disappearance into RN in 1987: https://www.bcn.cl/historiapolitica/partidos_politicos/wiki/Partido_Nacional
- BCN, coup and institutional break: Congress dissolved and left parties prohibited: https://www.bcn.cl/historiapolitica/elecciones/detalle_eleccion?handle=10221.1%2F63137
- BCN, Pinochet biography: executive power in June 1974 and formal presidential title in December 1974: https://www.bcn.cl/historiapolitica/resenas_parlamentarias/wiki/Augusto_Pinochet_Ugarte
- Memoria Chilena, Pinochet appointment sequence and Decree Law 527/806: https://www.memoriachilena.gob.cl/602/w3-article-92413.html
- BCN, 1980 constitutional plebiscite and its process limitations: https://www.bcn.cl/historiapolitica/elecciones/detalle_eleccion?handle=10221.1%2F63186
- Ley Chile, Decree Law 3,500 pension reform and 1981 effective date: https://bcn.cl/3m6sg
- Andean Community chronology, Chilean withdrawal in 1976: https://www.comunidadandina.org/quienes-somos/cronologia/
- Biblioteca del Congreso Nacional de Chile, 1988 plebiscite official summary and transition: https://www.bcn.cl/historiapolitica/elecciones/detalle_eleccion?handle=10221.1%2F63196&periodo=1973-1990
- Tribunal Calificador de Elecciones, certified 1988 result: https://tricel.cl/wp-content/uploads/2020/11/SENTENCIA-PLEBISCITO-1988.pdf
- Chile Law 17.729 (1972), indigenous lands and Indigenous Development Institute: https://bcn.cl/3ajf7
- UN Treaty Series, 1984 Chile-Argentina Treaty of Peace and Friendship: https://treaties.un.org/Pages/showDetails.aspx?objid=08000002800d4d04

**Review boundary:** This is a historical design review, not validation of native effects, focus syntax, leader-array implementation or GUI. It did not change the design JSON or runtime files.
