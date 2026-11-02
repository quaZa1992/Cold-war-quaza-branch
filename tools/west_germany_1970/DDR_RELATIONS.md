IMPERIA COLD WAR — Shared inner-German dossier implementation contract

# Bonn and East Berlin

Current consent, espionage, recognition and settlement corrections are recorded in [BALANCE_IMPLEMENTATION.md](BALANCE_IMPLEMENTATION.md).

Both German players have two 20×20 launchers in the politics panel beside faction membership, at (424,248) and (446,248). The flags-and-bridge icon opens **Inner-German Relations**. The shield-and-file icon opens BRD **Internal Security** or DDR **Domestic Affairs**. These compact bounds also clear the native faction-dismantle control. East Berlin also has an **Inner-German Relations** decision category with an opener. Its Council of Ministers file has five tabs: Situation, Crisis, Levers, Treaties and Domestic. See [entry_ui_preview/PLACEMENT_AUDIT.md](entry_ui_preview/PLACEMENT_AUDIT.md) for the full adjacent native-control bounds.

The two perspectives read the same GER-owned climate, pressure, escalation stage, treaty progress, border snapshot and initiative pools. Each player owns their window selection, open flag, geometry cache and dirty counter. No gameplay variables are mirrored onto DDR.

The DDR controls sixteen policy actions: ten bilateral/military measures and six domestic measures. Two additional shared providers handle proposing Unity talks and reviewing the current Unity chapter. The existing national decisions and the new buttons call the same transactional bodies. Original prices and numerical policy effects are retained, with explicit political prerequisites added to SED-specific measures. Historical precedents and the limits of the numerical calibration are recorded in [DDR_RELATIONS_HISTORY.md](DDR_RELATIONS_HISTORY.md).

| Ownership | Authoritative state |
|---|---|
| GER | Bilateral `cwgg_*` climate, crises, treaties, initiative, readiness, border strength and Unity negotiations |
| DDR | Existing `cwddr_*` currency shortage, opposition, recognition and control pressures |
| Native DDR national tree | Independent `COLDWAR_DDR_course`, its course BOP, leadership and government; player-chosen politics remain native |
| Each human viewer | Own tab, open flag, dirty counter and presentation coordinates |

## Two-player historical sandbox

GER and DDR remain separate player-controlled countries. The old GER-owned Honecker appointment, DDR leader/Wende stage proxies, scheduled Wall opening, automatic collapse and one-sided unity fast track are retired. Legacy queued GER-to-DDR event IDs resolve to hidden no-effect events. The migration removes only obsolete proxy variables and flags; it does not infer a government, leader, ideology or border outcome for either player. Native DDR calendar mortality events are restricted to AI-controlled DDR, and their effects have a second AI guard. Human DDR leadership is chosen through its own politics.

The shared BRD/DDR bridge reads the native DDR border ladder's current state for border-opening availability. It does not replay a historical transition or grant an opening from a date, proxy stage or foreign event. German unity, the border and the treaty community therefore follow current policies and the bilateral process.

## Payments and player consent

GUI actions recheck the actual DDR country, scenario, counterpart existence, initialization, completed Unity, political prerequisites, initiative, political power and shared cooldown. A GUI action pays its DDR political-power cost once. A native decision keeps its original displayed engine cost; its wrapper rechecks non-price requirements and refunds that engine cost if the order has become invalid. Both paths apply the same body and local cooldown. The Unity proposal separates readiness from affordability so an exact 100-PP native payment is not rejected after the engine has deducted it.

The five crisis choices use one DDR-local 30-day instruction lock, shared with the existing crisis event. Choosing an instruction does not spend initiative; the two-month round resolution alone charges one initiative for escalation, Moscow or a counter-offer. Calling Moscow requires an existing USSR and does not confer Soviet consent or intervention. The event has a no-change option so a delayed prompt can always close safely. The DDR sees Bonn's last resolved stance; its current pending stance remains undisclosed.

Either country may initiate each of the nine bilateral treaties. The initiator pays 25 political power and 2 of its own initiative; treaty-specific climate, stage, predecessor and policy requirements still apply. After negotiation, both sides give explicit consent through their own guarded response. A ready or deferred proposal stays locked against a new start until it is accepted, refused or explicitly lapsed; there is no timeout acceptance. The GUI does not ratify for either country.

Unity talks remain a separate negotiated process. Neither focus requests nor legacy queued events auto-annex DDR or manufacture Soviet/Four-Power consent. The cooperative confederation flag and idea are available only after Treaty 9 has valid bilateral standing; this records cooperation while preserving DDR's independence, faction membership and government. It does not make DDR a subject. The native DDR tree remains the route for DDR political choices.

SED border/security and socialist-reform measures require the actual native `COLDWAR_DDR_sed_governs` trigger. A party change therefore disables those actions. The national DDR course no longer contributes to the bilateral monthly climate. Moscow Trust, the 1985 state/Moscow trust meters, Western Integration points and Moscow's Guarantee points are retired, including their derived contributions, rewards, thresholds and displays. Actual diplomatic relations, treaties, faction membership and player consent remain separate gameplay conditions.

War requires an explicit war path and current country/faction conditions. The DDR attack path checks actual Soviet-faction membership; a human-controlled Soviet Union is never added automatically. A false-alarm event does not declare war. During an active war, Bonn's armistice proposal is sent to DDR through the recipient event `COLDWAR_GGR.260`, where the DDR player accepts or rejects it.

## Performance and lifecycle

The bilateral simulation still has one `on_monthly_GER` owner. Independent DDR national economic callbacks remain; trust callbacks are removed. Opening or repainting the DDR file performs no border division count, world scan, random roll, recruitment, economic calculation or monthly simulation. It consumes the current shared border snapshot; the existing GER simulation and its established refresh callers maintain that snapshot.

GER's refresh also invalidates the DDR perspective. DDR actions update the shared state and use a presentation-only refresh for both viewers. Full presentation arithmetic is gated by an open human window. A small DDR daily callback runs only while a human's DDR file is open, updating current eligibility and expiry without running the minigame. Missing Bonn or completed Unity disable bilateral transactions while domestic policies remain accessible; a cooperative confederation keeps bilateral play available. Launchers do not depend on the hidden economy bar, the other German state's existence or the current crisis. Each scripted GUI uses its own country dirty counter and disables AI evaluation.

`compile_sandbox.py` renders canonical sources in memory, then applies only the bounded German sandbox nodes and files. It preserves unrelated live focus, government, economy, security and Unity code; it is not a full live-tree compile. Use `--dry-run` to review the proposed bounded install. Scripts use UTF-8 without BOM; English localisation uses UTF-8 with BOM.

```powershell
python tools/west_germany_1970/compile_sandbox.py --dry-run
python tools/west_germany_1970/test_ddr_relations.py
python tools/west_germany_1970/test_sandbox_history.py
python tools/west_germany_1970/test_performance_gui.py
python tools/west_germany_1970/validate.py . .
python tools/west_germany_1970/preview_ddr_relations.py
```

The installed-script model covers exact-price payments, refunds, cross-interface cooldowns, one-time policies, party changes, crisis selection/resolution, real Unity consent routing, shared view updates, missing countries, terminal states, independent national course, both DDR launcher routes and the transitive absence of extra scans/ticks in DDR presentation. Preview PNGs use installed GUI coordinates and DDS assets with approximate fonts and sample values. Their missing vanilla close-button sprite is a renderer limitation. Native HOI4 load, tooltips, save/reload, multiplayer synchronization and frame times have not been tested.

One startup-only, country-guarded migration clears the retired trust/alignment variables and trust-tier modifiers in existing German saves and refreshes independent derived modifiers. It does not run a daily migration or initialize the dormant legacy crisis system. Other stored pressures and political state remain. Engine-owned decision cooldowns or one-time decisions taken before this integration cannot be inferred retroactively into the shared receipt flags; those receipts are authoritative for subsequent activations. Native save migration remains untested in HOI4.

## Next DDR features — proposals, not installed content

The best next step is to give East Berlin more bargaining power through the existing dossier. Keep the native DDR political tree authoritative and give cooperation between two independent German states substantial follow-through. These proposals are design recommendations; no new rewards, costs or policy systems below have been installed.

| Priority | Proposed addition | Benefit and trade-off | Existing implementation anchor |
|---|---|---|---|
| 1 | DDR-authored economic packages and counter-offers | DDR offers limited travel, exchange or transit concessions for financing; Bonn may accept, refuse or return one of a few fixed counter-offers. Financing eases the shortage but entails debt/service or agreed policy concessions; Bonn pays a real cost. | Existing `ddr_ask_credit`, `ddr_goodwill`, exchange/transit actions and guarded treaty recipient flow. Imperia's `imp_money_transfer` already requires recipient acceptance and actually debits the sender and credits the recipient. A loan also needs an explicit debt/service contract; a gift or a shortage-meter reduction must not be labelled a loan. |
| 2 | Standing DDR travel/transit policies | Convert related one-off gestures into a small set of deliberate, reversible policies: strict exchange/control, limited family visits, or wider travel. Strict controls favor currency extraction and coercive capacity while worsening contact and political pressure; opening favors contact at a cost to control and administrative resources. | Native `COLDWAR_DDR_ladder_border_*` ideas and actual policy triggers; preserve earned national reforms and replace active policy forms rather than stacking duplicates. Do not clear the entire border regime for a minor family-visit concession. |
| 3 | Dialogue alongside security operations | A SED government may negotiate with church/civic representatives instead of ordering another sweep. Accommodation can reduce immediate confrontation but consumes resources and limits coercive control; repression can produce publicity and solidarity that strengthen the opposition. Neither choice schedules a government collapse. | Existing `stasi_sweep`, `reform_course` and native DDR church/party branches. Use actual governing-party predicates and suitable institutional text; avoid a second automatic political-course-to-climate score. |
| 4 | DDR-led security and durable two-state cooperation | DDR can propose an armistice or reciprocal alert reduction, and both countries can maintain transit, cultural or infrastructure cooperation while remaining separate states. Joint benefits carry agreed payments and commitments, with explicit withdrawal consequences. | Existing NVA alert controls, consent events, nine-treaty progression and cooperative confederation. Reuse the GER-owned record and both country views. Any future construction must grant one shared slot per building level in the same state. |

The economic-package proposal has a direct historical precedent. The Bundesarchiv's *DDR im Blick* edition describes the 1983 bank credit, federal guarantee and accompanying DDR concessions over border processing, minimum exchange for children, mines and self-firing devices. Those precedents justify a negotiated exchange; they do not prescribe a game amount or an automatic dated outcome. [DDR im Blick, introduction to 1983](https://www.ddr-im-blick.de/jahrgaenge/jahrgang-1983/report/einleitung-1983/)

Dialogue and repression also need distinct consequences. The Bundesarchiv documents how the 1987 Umweltbibliothek raid increased publicity and solidarity, damaged the regime's reputation, and ended with releases following public pressure and church-state negotiations. This supports a risk of backlash and a negotiated alternative, not a guaranteed success or forced 1989 sequence. [Bundesarchiv, Umweltbibliothek](https://www.bundesarchiv.de/themen-entdecken/online-entdecken/themenbeitraege/die-umweltbibliothek/)

For implementation, use fixed small offer packages in Treaties, the existing Domestic/Levers tabs for policies, and one existing monthly owner for recurring costs. Do not add new daily world scans, trust meters, a parallel currency system or a second border-policy stack. Amounts, weekly service costs and cooldowns require a separate numerical design before implementation. The current `cwddr_hard_currency` field measures shortage, not cash received; actual financing must use native treasury/debt effects. Existing non-SED governments need their own appropriate descriptions and available actions.
