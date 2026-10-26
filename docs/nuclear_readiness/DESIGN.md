# Nuclear readiness and crisis diplomacy

Historical grounding and balance record for the 1970 multiplayer scenario.

The revised Strategic Command emblem, instrument-panel design, native text layout and visual verification are documented in [the interface art-direction record](interface/ART_DIRECTION.md).

## Historical precedents

- **Cuban crisis, 1962:** the 12 November Executive Committee record distinguishes SAC at DEFCON 2 from other forces at DEFCON 3. McNamara explicitly links prolonged alert to spare-parts consumption and discusses standing down as an observable signal to Moscow. This supports separate national readiness, recurring costs, cumulative fatigue and deliberate de-escalation. Source: [FRUS 1961–1963, XI, document 170](https://history.state.gov/historicaldocuments/frus1961-63v11/d170).
- **Middle East crisis, 24–25 October 1973:** the contemporary NSC/JCS memorandum records the relationship between Soviet intervention warnings, force alerts and diplomatic exchanges. This supports a confrontation between identified governments, a counter-alert, allied consultation and direct communications. Source: [FRUS 1969–1976, XXV, document 269](https://history.state.gov/historicaldocuments/frus1969-76v25/d269).
- **Dispersal in 1962:** the US Air Force historical account records dispersal and increased bomber/missile alert. The mod represents this through a bounded protected share of stored missiles rather than claiming a literal location or an actual SSBN patrol. Source: [Air Force Historical Support Division, Cuban Missile Crisis](https://www.afhistory.af.mil/FAQs/Fact-Sheets/Article/458954/1962-cuban-missile-crisis/).

All numerical budgets, percentages, intelligence thresholds and timers below are gameplay estimates, not historical expenditure or weapon-performance measurements.

## Player decisions and institutional trade-offs

| Readiness | Operational stock allocation | Dispersed stock protected from counterforce loss | Weekly cost multiplier | Fatigue per day |
|---|---:|---:|---:|---:|
| Routine Deterrence | 15% | 10% | 1 | −2 |
| Increased Vigilance | 30% | 15% | 1.15 | −2 |
| Reinforced Readiness | 50% | 25% | 1.4 | +0.25 |
| Strategic Alert | 75% | 40% | 1.8 | +1 |
| Maximum Readiness | 100% | 50% | 2.5 | +2 |

Orders cost 25 political power. Raising readiness takes two days per level; the previous posture remains operative during preparations. A reduction is immediate. Confirmed incoming nuclear use releases an agreed stand-down and orders emergency maximum readiness with a one-day preparation period; it never launches a weapon.

The weekly readiness base is $0.002 billion plus $0.00001 billion per stored nuclear missile. Readiness, fatigue, the established GDP/c wage scale and inflation multiply that base. At 100 fatigue, strategic-force costs increase by 50% and stability is reduced by five percentage points. These costs enter the existing Defence Budget once; GUI refreshes calculate rates without transferring treasury funds.

Civil defence costs 25 political power, takes three days, and reduces remaining population losses by 20% after shelters. It diverts labour: −3% construction speed and factory output. Weekly funding starts with mobilisation, at $0.002 billion plus 0.002% of GDP, adjusted for inflation. Release removes its cost and penalties.

The reserve protects actual stored missiles from added counterforce losses. A tactical/state/strategic hit removes 5/15/40% of the exposed stock, once per raid, not once per affected state. It does not create missiles, replace lost weapons, or make buildings or population immune. Existing strike damage and fallout continue independently.

## Multiplayer diplomacy

- Nuclear readiness and warning access follow actual ownership of either nuclear missile archetype, for every country, including subjects. Nuclear-status laws and country tags do not grant or restrict warning access. An empty arsenal disables it; employment laws continue to govern actual launches. The diplomatic menu derives uppercase title and hover-description keys for all eight actions, with static hover descriptions that do not require event or country text contexts.
- A formal warning costs 50 political power, adds five Cold War tension and two world tension, and creates one reciprocal confrontation for 90 days. Both countries are locked to that counterpart until closure. A 90-day pair cooldown prevents repeated warning cycles.
- The recipient may issue one counter-alert for 25 political power, adding three Cold War tension and one world tension. A completed readiness level of at least Reinforced Readiness and an actual nuclear stockpile are required.
- Direct communications and mutual stand-down are native diplomatic offers, each costing 15 political power. Consent belongs to the recipient. Offers expire after 14 days; unanswered or rejected offers retain a 21-day sender cooldown. An accepted communications channel permits an immediate mutual stand-down proposal. Pair identifiers, counterpart identity, deadlines, proposal type and both countries' nuclear-use revisions are checked on acceptance.
- A mutual stand-down returns both forces to routine readiness, cancels orders and commits both for 30 days. It removes only that confrontation's actual Cold War tension contribution, normally five or eight points, rising to at most 18 with both final ultimatums. Contributions are measured after the 100-point clamp, so a warning at maximum tension cannot generate a free reduction later. Actual-use tension is excluded. It gives no political-power reward. World tension already caused remains subject to the normal game system.
- Only the original issuer can withdraw its warning. Withdrawal returns that state's forces to routine readiness and commits it for 14 days; Cold War tension falls by up to two points, capped by the actual contribution. Expiry applies the same bounded reduction and leaves both national military postures under player control. The recipient can independently lower its readiness and propose an agreed resolution.
- Allied consultations cost 20 political power and inform allied human governments, once per 30 days. They neither order allied forces nor bind allied players to war.
- An assessment costs 10 political power and has a 14-day cooldown. Below 35% air intelligence, readiness is unconfirmed unless public or allied liaison applies. At 35%, or through liaison/a public confrontation, only a broad band is reported. At 65%, the exact readiness level is confirmed. Discovery of a concealed strategic/maximum alert adds one Cold War tension, at most once per target per 30 days.
- New features never order automatic launches. The existing human-only raid guards are preserved as the first preparation/launch checks. Older US/Soviet automatic nuclear decisions are excluded from this scenario. The existing employment laws are checked again at launch. Retaliation is attributed to the actual nuclear aggressor rather than an unrestricted historical victim marker.

The strategic command panel uses English institutional language and numeric effect tooltips. Historical sources, implementation records and verification fixtures are confined to development files and never inserted into normal player descriptions.

The [first-use procedure](FIRST_USE.md) adds a 100-political-power final ultimatum at Maximum Readiness. After 72 hours, a seven-day, target-bound release window permits native nuclear operations without a preceding declaration of war. The first resolved operation opens hostilities. Revocation and negotiated stand-down remain available, with separate own/foreign status in Strategic Command. National employment doctrines, human-only raid guards and normal equipment requirements remain operative.

## Event photographs

All 21 visible nuclear readiness events use 12 themed archival photographs: strategic command, civil defence, missile warning, bomber counter-alert, hotline communications, arms-control agreement, diplomatic venue, situation briefing, security consultation, nuclear detonation, blast aftermath and aerial intelligence. Eleven monochrome sources were individually colourised using built-in ImageGen; the SALT agreement image retains its original colour. These are illustrative archival subjects for all countries, and restored colours are interpretive.

Each picture uses the existing native MD 217 × 163 frame with a proportionally fitted 180 × 150 inset. The exporter verifies unchanged outer-frame pixels, colour content, and exact decoded DDS/PNG equality. All 21 event bindings resolve to 12 unique registered textures; the hidden timer event has no picture. The complete set, provenance, licensing and source/master/output hashes are in [the event-art record](event_art/CREDITS.md); prompts are retained in `tools/nuclear_readiness/art/prompts.json`. Event localisation promotes saved country targets by their names, without the effect-script `event_target:` prefix.

## Verification — 26 October 2026

The 41 strict AST tests execute the authored effects for crossed warnings, independent simultaneous crises, expired and invalidated offers, recipient/issuer authority, capped and fractional tension, preparation, costs, fatigue, civil defence, dispersed stocks, attributed retaliation and the full first-use procedure. Arsenal-based warning access is exercised for five country tags, both missile archetypes, missing nuclear-status laws and a subject government; nuclear status without weapons does not enable a warning. Integration checks cover runtime guards, one hit callback per raid outcome, four peacetime-operation handlers per raid type, native-budget aggregation, encoding, numeric precision, generated references and all eight native diplomatic title/description pairs.

A fresh HOI4 1.19.3 test campaign passed 16 native checkpoints: actual equipment counts, readiness lead time, tactical eligibility, reciprocal crisis creation, bilateral hotline, mutual stand-down with both timed flags, civil defence preparation, counterforce protection, ultimatum context, the initial launch block, the scheduled native hourly callback, the 72-step boundary, the seven-day release window, war opening, attacker attribution and one-time consequences. The controlled 1,000-missile stockpile produced the expected $0.012 billion routine weekly budget; a maximum-readiness reserve left 800 missiles after the specified counterforce hit. No readiness/escalation-module errors were reported in the final run, including country-name promotions. The native record is `tools/nuclear_readiness/engine_report.json`.

The command panel was inspected in the running game for all five named levels, current/operational/dispersed stocks, weekly costs, fatigue, civil protection, the correctly named crisis counterpart and English text. The final native run includes the corrected implicit diplomatic-title keys, arsenal-based eligibility and event target-name promotions. All eight diplomatic hover descriptions are checked to avoid context-dependent placeholders. The saved source hashes are the report-time snapshot rather than a claim that every visible interaction was exercised at that exact revision.

This is not a two-client multiplayer or network/OOS test. The native fixture calls diplomatic and raid-resolution helpers directly; it does not establish human-to-human notification delivery on a network, nor does it execute every nuclear raid outcome in live combat. The hourly callback executes on the native clock; the remaining countdown boundary is then exercised through the native timer helper. Existing errors in unrelated mod systems are outside this verification. The test campaign is unsaved; temporary runtime fixtures are removed after the owned process is stopped.
