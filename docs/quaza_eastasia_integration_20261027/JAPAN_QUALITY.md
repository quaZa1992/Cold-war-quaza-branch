IMPERIA COLD WAR

# Japan 1970 quality and implementation review

## Scope and evidence boundary

This note reviews the installed Japan national programme in `common/national_focus/COLDWAR_JAP_1970_focus.txt`, its reward providers, approved design and generated presentation. Japan has 425 focus IDs: 13 constitutional focuses, 212 national and economic focuses, 80 foreign-policy focuses, and five 24-focus party programmes. The 80 economic and 80 foreign-policy focuses are arranged in eight 10-focus sections each. The examples below are individual compatible choices. They are not added into a whole-tree total, because many are mutually exclusive or government-specific.

Technical findings are based on the current installed script and its source providers. Historical framing distinguishes claims inherited from references in `tools/japan_1970/approved_design.json` from the primary-source claims independently checked while writing this note. Proposed percentages, treasury amounts and game rewards are balance values, not historical measurements.

## Programme choices and representative scale

The opening makes Japan's postwar security settlement, civilian oversight, defence capacity and economic opportunity cost explicit. Later national programmes address the SDF, procurement, high-growth policy, pollution and public health, housing, labour, regional development, energy, infrastructure, credit, science and diplomacy. The party programmes are distinct policy packages for the LDP, DSP, JSP, JCP and Komeito. Each contains visible institutional priorities and three exclusive policy pairs with follow-ups. Exact MD party-in-power triggers gate party focus availability and execution; the other parties' branches remain visible.

| Choice or programme | Focus IDs | Representative effects and trade-off |
|---|---|---|
| Defence budget | `COLDWAR_JAP_1970_national_0_a_restrained_defence_budget` / `COLDWAR_JAP_1970_national_0_expand_defence_appropriations` | Both take 70 days. Restraint grants +3% stability factor at −3% military factory output. Expanded appropriations grant +4% military factory output at −3% stability factor. |
| Procurement model | `COLDWAR_JAP_1970_national_4_licensed_production` / `COLDWAR_JAP_1970_national_4_domestic_design_capacity` | Both are 70-day choices after procurement policy. Licensed production requires the existing Licensed Armaments Programme and grants +3% military factory output at −2% civilian-sector productivity. Domestic design capacity grants +3% research speed at −2% military factory output. Neither is a free upgrade to the other. |
| Pollution compliance | `COLDWAR_JAP_1970_national_5_strict_emissions_standards` / `COLDWAR_JAP_1970_national_5_negotiated_compliance` | Strict standards give +3% research speed at −3% military factory output. Negotiated compliance gives +3% civilian-sector productivity while increasing health spending by 4%. The paths prioritize industrial enforcement versus negotiated adjustment, with distinct ongoing costs. |
| Social insurance | `COLDWAR_JAP_1970_national_6_expand_public_insurance` / `COLDWAR_JAP_1970_national_6_control_medical_costs` | Expanded insurance gives +4% stability factor at +6% health spending. Cost control reduces health spending by 5% at −3% stability factor. |
| Public science or targeted grant | `COLDWAR_JAP_1970_national_10_public_laboratory_grants` / `COLDWAR_JAP_1970_national_10_specialist_research_teams` | Public laboratories provide +2% research speed at +2% education spending. Specialist teams spend $2 billion for one 25% industry-technology research bonus. The one-use bonus has a direct cash cost and a narrow target. |
| Constitutional referendum outcome | `COLDWAR_JAP_1970_article9_abolish` / `COLDWAR_JAP_1970_article9_confirm` | Both are 70-day outcomes after the debate, campaign and referendum chain. Abolition removes the starting Article 9 and Self-Defence spirit and adds a revised defence spirit: +5% army attack, +5% recruitable population factor, −7% stability factor and +10% army personnel expenditure; it also triggers separate US and Soviet responses. Confirmation retains the starting spirit, grants +50 political power and +3% stability factor for 730 days. The retained spirit itself carries −10% recruitable population factor and −5% army attack, alongside +5% stability factor. These are different constitutional settlements, not additive branches. |
| LDP industrial policy | `COLDWAR_JAP_1970_ldp_deep_fork1_a` / `COLDWAR_JAP_1970_ldp_deep_fork1_b` | The 35-day Strategic Industrial Guidance route grants +4% civilian-sector productivity at −2% office-sector productivity. Market Liberalisation grants +4% office-sector productivity at −3% stability factor. Each leads to its own follow-up and the LDP charter. |
| Other party programmes | DSP: `COLDWAR_JAP_1970_dsp_deep_fork0_a` / `COLDWAR_JAP_1970_dsp_deep_fork0_b`; JSP: `COLDWAR_JAP_1970_jsp_deep_fork0_a` / `COLDWAR_JAP_1970_jsp_deep_fork0_b`; JCP: `COLDWAR_JAP_1970_jcp_deep_fork0_a` / `COLDWAR_JAP_1970_jcp_deep_fork0_b`; Komeito: `COLDWAR_JAP_1970_komeito_deep_fork0_a` / `COLDWAR_JAP_1970_komeito_deep_fork0_b` | DSP chooses +4% stability with +4% social expenditure or +4% civilian productivity with −3% stability. The JSP chooses between +5% stability with −8% recruitable population or +4% army core defence with +4% social expenditure. The JCP chooses between +4% civilian productivity with +5% bureaucracy spending or +4% agricultural productivity with +3% social expenditure. Komeito chooses between +4% stability with +5% social expenditure or +4% stability with −3% civilian productivity. These examples remain party-bound, mutually exclusive routes, not a combined national bonus. |
| Seoul industrial cooperation | `COLDWAR_JAP_1970_seoul_industrial_cooperation` | South Korea may accept or refuse. Acceptance charges Japan $2 billion, gives South Korea a civilian factory in a state it selects and owns and controls, gives Japan +2% office-sector productivity for five years, and adds +20 mutual opinion. Refusal costs nothing. |
| Okinawa base consultation | `COLDWAR_JAP_1970_okinawa_base_compact` | The United States may accept or refuse. Acceptance charges Japan $3 billion and gives both +20 mutual opinion and +2% stability for five years. It does not change Okinawa ownership or American basing. |

These values are sampled from emitted focus effects and the matching approved design, not accumulated across incompatible paths. The constitutional outcome also has event-driven diplomatic consequences; focus completion does not itself change a treaty, base or nuclear policy.

## Effect mechanics and MD consumers

The national programme's custom modifier values are registered through Japan's dynamic-modifier definitions, and the corresponding keys are read by the focus rewards. The modifier audit records 41 used keys and traces them to definitions and consumers. Examples include factory and office productivity, research, energy use, health and education expenditure, military performance, and social or administrative costs. The growth and energy sections use `country_productivity_growth_modifier`, which is registered and read by MD's `00_productivity_effects` calculation. Electricity and fuel modifiers are checked against MD's energy definitions; treasury effects use the existing money-system effect and formatter. These are source-level consumer checks, not independent measurements of their long-run balance impact.

Construction effects retain separate scenario, state ownership/control and native capacity guards. A granted building level receives one shared state slot per level in the same state before construction, including infrastructure and fortification-style buildings; slot grants are inside the one-time transaction. Preview text is not used to bypass these actual guards.

No arbitrary focus year gate was found in the Japan tree. Constitutional progress is gated by the starting Article 9 spirit, staged political support and the final stability requirement, rather than a calendar date. This does not rewrite the scenario's actual dated leader succession or other historical country setup. The 730-day constitutional and five-year bilateral durations are effect durations, not focus start-date restrictions.

## Recipient consent and prospective previews

The Japan content contains 39 recipient-approved offer focuses with full native prospective numeric previews. The displayed terms remain visible while the focus is locked and before a response. The actual acceptance path still belongs to the recipient; only acceptance applies the listed transaction. The offer families cover direct bilateral proposals, Korean reconciliation and member-led multilateral invitations. Multiple-invite effects render one generic accepting-recipient reward block rather than implying that every country in a global scope receives the offer.

Four project offers use recipient-selected construction locations. Acceptance must resolve to a state the recipient owns and controls, with native capacity checked separately. The preview identifies the recipient-selected site rather than inventing a fixed state. Each project construction level includes its shared slot grant in the same guarded transaction. Offer dispatch, acceptance and refusal remain separate; previews are display-only.

The installed bilateral source has pending and unresolved checks around response execution, preventing repeated payment from a stale or duplicate response. On accepted terms that grant both signatories an agreement spirit, the event applies the matching named timed idea to both countries, generally for 1,825 days, and applies mutual opinion effects in both directions. The proposal's spending and construction can still be asymmetric where the displayed terms say so. These are timed agreements, not permanent spirits with a suspend-and-restore lifecycle. A separate daily recovery effect can redispatch a completed offer only when the recipient exists and has neither a pending nor resolved response; this recovery does not charge or award the agreement again. Static review covers consent and agreement code paths; it is not a guarantee against every multiplayer race or save migration.

## Historical basis and provenance

The design's recorded historical context supports policy subjects without presenting proposed modifiers as historical facts:

- Japan's 1960 Income Doubling Plan and the 1970 task of sustaining growth inform the high-growth and party-policy sections.
- Article 9 and its amendment procedure inform a staged Diet and referendum route. The design records the [House of Representatives' English constitution page](https://www.shugiin.go.jp/internet/itdb_english.nsf/html/statics/english/constitution_e.htm), the MOFA [Japan-US Security Treaty text](https://www.mofa.go.jp/region/n-america/us/q&a/ref/1.html) and Japan's [Three Non-Nuclear Principles](https://www.mofa.go.jp/policy/un/disarmament/nnp/).
- The 1970s pollution crisis and industrial remediation inform the pollution and public-health programmes. The design records Japan's [Ministry of Environment pollution history](https://www.env.go.jp/en/water/wq/wemj/history.html) and a [1976 pollution-control source](https://worldjpn.net/documents/texts/docs/19761029.O1J.html).
- The 1973 and 1979 oil shocks are later than the January 1970 start. The energy branches therefore frame diversification and conservation as future policy, not as crises already experienced at game start. The design records the existing oil-shock event and the IEA's [Japan 2021 Energy Policy Review](https://www.iea.org/reports/japan-2021).
- The Okinawa Reversion Agreement was signed in 1971 and took effect in 1972; it is a precedent for negotiated US consent, not for an automatic 1970 transfer. The recorded [Japan-China 1972 Joint Communique](https://www.mofa.go.jp/region/asia-paci/china/joint72.html), [Japan-USSR 1956 Joint Declaration background](https://www.mofa.go.jp/policy/q_a/faq11.html), [Japan-ROK 1965 Treaty on Basic Relations](https://www.mofa.go.jp/region/asia-paci/korea/treaty.html) and [1967 ASEAN Declaration](https://asean.org/the-asean-declaration-bangkok-declaration-bangkok-8-august-1967/) support negotiated status, unresolved territorial issues and voluntary regional engagement. The official [Cabinet Secretariat Okinawa timeline](https://www.cas.go.jp/jp/ryodo_eg/taiou/senkaku/senkaku02-02.html) records the 1971 signing and 1972 entry into force; the [MOFA treaty-history exhibit](https://www.mofa.go.jp/mofaj/annai/honsho/shiryo/page24_001761.html) records the ratification exchange and effective date.

These inherited references are listed in `tools/japan_1970/approved_design.json` evidence and rationale. This review independently checked the official Okinawa timeline, including the 17 June 1971 signing and 15 May 1972 entry into force; the official Japan-US Security Treaty, which provides for consultation and separately arranged facilities; the MOFA account that the 1956 Japan-Soviet declaration restored diplomatic relations while leaving peace-treaty and territorial questions for further negotiation; and the 1972 Japan-China communiqué, which formalized normalization and diplomatic relations. The approved design's URL labeled as the Okinawa Reversion Agreement actually opens the Japan-US Security Treaty, and its URL labeled as Japan-USSR Joint Declaration opens a pre-1855 territory-history page. This note replaces those two mismatched links above. Claims about the Income Doubling Plan, pollution precedents, energy policy, the Japan-ROK treaty and ASEAN founding are inherited from the approved design's source trail and were not independently rechecked here. Independently checked in the technical audit are installed focus gates, effect/provider references, transaction structure, source counts, and the presentation manifest. The earlier `tools/japan_1970/RUNTIME_REVIEW.md` records a native execution probe for representative recipient response, construction, payment, party-variable and constitutional paths; it does not show every focus or every lifecycle outcome was exercised in game.

## Layout and preview limits

The review renderer uses the measured Japan/MD presentation reference: 96 by 130 px focus-grid spacing, a 165 by 128 px item container, and an approximate 147 px name field. The native titlebar and resolved focus icons are used. Relative anchors and coordinates are parsed from the emitted graph. The freshly generated output comprises a full-tree overview and 32 section views. The static checker reports no card overlap, modeled exclusion or prerequisite obstruction, panel collision, title overflow, or guarded-payout change.

The image is a source-derived preview, not a live-game screenshot. Arial substitutes for the native game font; connector routing and initial availability are approximations. Static line-crossing checks cannot prove the engine's actual connector routing, tooltip layout, scroll/zoom behavior, or multiplayer presentation. The earlier native execution probe is gameplay evidence for selected paths, not graphical focus-tree validation.

## Reproducible checks

Successful bounded commands from the mod root:

```text
python tools/japan_1970/stage_focus_graph.py
Staged 425 graph nodes. 0 have no mapped reward; in-game behaviour remains unverified.

python tools/japan_1970/render_presentation.py
Rendered overview and 32 current branch views from 425 emitted focuses.

python tools/japan_1970/check_presentation.py
Presentation: 425 focuses; normalized 120 exact party-gate presentations and 23 guaranteed-slot equivalents; protected payouts, cards, exclusions, routes, panel and titles; 0 findings

python tools/japan_1970/check_live_install.py
Grammar checked 39 installed scripts; 0 findings
Presentation: 425 focuses; normalized 120 exact party-gate presentations and 23 guaranteed-slot equivalents; protected payouts, cards, exclusions, routes, panel and titles; 0 findings
Installed: 425 focus IDs, 425 reward helpers, 10 English localization files; 0 findings
```

The presentation comparison uses the immutable archived pre-polish Japan tree at `E:/HOI4_Mod_Tools/mdcoldwar/runtime/quaza_eastasia_20261027/donor/tools/japan_1970/staging/graph/before_polish_focus_tree.txt`. Its narrow normalizations equate exact-slot legacy tooltip wrappers with the corresponding native party trigger, and only discard an old free-slot availability check when the current focus preview guarantees enough shared slots before construction in the same state. Focus IDs, guarded payouts, other availability conditions and geometry diagnostics remain checked. These commands did not launch HOI4 or modify the installed country files.
