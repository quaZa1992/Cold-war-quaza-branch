IMPERIA COLD WAR

# Independent Gulf player revision review, 25 October 2026

This review covers the installed Gulf chapter, its canonical generators, Iraqi counterplay, prospective effects and historical framing. No gameplay file was edited and no game was launched by this reviewer. The machine-readable companion records exact source hashes, source locations, model results and the inspected image.

The financing defect and the multiplayer race involving an already existing peaceful Kurdish player are corrected and independently retested. No confirmed unresolved defect remains in this bounded scope. Current-revision native and multiplayer tests remain pending.

## Installed scope and visual result

The USA tree SHA-256 is `8f494e3aa01c5882c79aa336e17d286c9f131cdeabcb651b654d9317875ec043`. It registers 281 IDs and displays 280 cards. The Gulf chapter retains its 15 registered IDs, with 14 visible cards. The obsolete `COLDWAR_USA_gulf_contacts` remains hidden and inert for save identity. Its old completion receipt can bypass the replacement entry focus without charging for the obsolete step.

Final emitted Gulf effect SHA-256: `11dd93ea17455c1a970f7548cbfb54ce454686beb0dbffee2cad397059312b5c`. Final trigger SHA-256: `dae7cd943b4525a752706dc336888938aeb849e10fc57154e625c2c653c5af99`. The companion JSON also hashes the generator, preview module, all nine runtime outputs, immutable catalogue, research record, image and layout evidence.

The inspected image is [USA_GULF.png](../../usa_1970_expansion_20261024/installed/USA_GULF.png). It uses actual installed cards, bitmap font, icons and resolved 96 x 130 coordinates. It is a source composition, not a native screenshot. Connector bends and locked-state treatment approximate the engine.

All 14 visible captions are legible. Their maximum native font advance is 143 pixels against a 147-pixel title area. No missing artwork, cropped caption or card/icon overlap was found. An independent component-bounding-box check also found zero intersections between any Gulf card and the other 266 USA focuses. The renderer reports no conditional coordinate offsets. The hidden contact card does not leave an empty mandatory step.

The policy fork clearly separates **A Limited War** and **Arm the Front**. Northern Access and Provide Comfort remain independent entry roots. Northern Safe Haven and Northern Air Shield require both access and relief branches. Baghdad Accord and Guarantee Self-Rule support paid, consented policy revisions rather than an irreversible ideological split. These distinctions are coherent with the actual prerequisites and exclusion blocks.

## Iraqi counterplay and native mechanics

The overlay in `tools/iraq_1970/gulf_counterplay.py` replaces the old pooled force and global security veto. It checks Iraqi divisions separately in states 164, 633, 630 and 1078. Each state must be owned and controlled by Iraq and have the relevant Kurdish core; the PUK state additionally requires the movement to have formed.

| Paid operation | Upfront invoice | National overhead for 90 days | Local requirement | One delivery per state and paid operation | Maintained local resistance target |
| --- | --- | --- | --- | --- | --- |
| Emergency Security Appropriation | 2% of current annual GDP | Army personnel +35%; equipment upkeep +20% | 2 actual Iraqi divisions for 30 consecutive observed days | Resistance -15 points | -20 points |
| Major Northern Operation | 4% of current annual GDP | Army personnel +60%; equipment upkeep +35% | 3 actual Iraqi divisions for 30 consecutive observed days | Resistance -25 points | -35 points |

The real helper recalculates its invoice from current Iraqi GDP, checks positive GDP and actual Treasury coverage, rejects the native Treasury-skip flag and pays through `modify_treasury_effect`. It increments one operation receipt after payment. Availability's daily quote is presentation data; it is not an authority for an unaffordable transaction.

Readiness is state-local. Repeated observer calls on the same model day cannot accelerate it. Troop withdrawal, loss of ownership or loss of control resets local readiness and removes the maintained target at the next observer. Returning troops must prepare again; the state receipt prevents another immediate resistance reduction during the same paid operation. The foreign mobilisation pulse independently checks the actual local troops, readiness and delivered receipt. Merely owning the national idea cannot stop all four states' pulses.

The 90-day overhead survives troop withdrawal. Iraq can explicitly end the operation's ideas, but the original cooldown and sunk invoice remain. Expiry or withdrawal does not reverse a resistance reduction already delivered. Migration conservatively retains old delivered reductions without another charge or delivery. An old undelivered preparation starts the new local readiness assessment without silently treating a former pooled force as four prepared local forces.

The actual MD economy reads both overhead modifier classes in `common/scripted_effects/00_money_system.txt:3217`. They therefore feed personnel and equipment costs rather than representing a separate hidden flat bill. Native installed documentation confirms `num_divisions_in_states` is a country trigger with a state list and count, and resistance-target effects use state scope. The generated code observes those scopes.

The uprising observer still needs at least two tracked states at 80% resistance, a real military opening and committed arms. It requires 30 qualifying days, then issues a 45-day warning. A local operation can reduce resistance sufficiently to interrupt those conditions; the warning clears after 15 days below its continuation conditions. An independent test with a paid idea but no local troops reached the uprising on day 75. There is no national-idea shortcut that freezes the warning.

## Kuwait crisis, access and recipient agency

The live Kuwait-war trigger does not depend solely on the special invasion focus or aggression receipt. Actual Iraq-Kuwait war, Iraqi occupation or annexation, and Iraqi subjection of Kuwait can establish the unresolved crisis. An independent, peaceful Kuwait owning and controlling both relevant states closes it despite an old aggression flag. A real military commitment followed by liberation records one finite 180-day postwar opening; an unoccupied diplomatic settlement does not invent a military defeat or refresh the window daily.

Desert Storm bypasses its redundant war-goal step if the USA is already at war with Iraq. Open Northern Channels has one native OR prerequisite group containing Desert Shield, Desert Storm and Coalition Mandate. This keeps the opposition channel reachable through any of the three roots. Its availability still needs an actual crisis or military opening and unresolved northern grievances. These are causal state checks, not arbitrary calendar locks.

Iran now receives its own host event, `COLDWAR_USA_gulf_events.14`, through Request Northern Access from PER. Iran's player accepts or refuses. On a valid first acceptance the USA pays $0.5 billion once and receives actual military and air-base access. Iran receives no invented matching Treasury grant. Repeat consent does not replay the invoice. Decline, missing pending offer, wrong recipient, USA disappearance, host war or insufficient funds grant no access and charge nothing.

An underground supply route requires a separately consenting Iran or Turkey and live American military access. Distant French basing alone cannot create that border route. Iran is the documented historical precedent; Turkey is a selectable RP alternative. Loss of the border route stops the underground subsidy on the funding observer without refunding or deleting weapons already committed. These checks represent the cooperating border government; they do not calculate a province-by-province logistics corridor.

## Findings and repairs

**GULF-HOST-OR, P1, fixed and independently retested.** The first host-payment OR originally treated `NOT MD_skip_treasury_cost` and Treasury coverage as separate alternatives. With $0.499 billion, a pending Iranian access offer accepted at $0.5 billion drove the USA to -$0.001 billion and granted access. Both request availability and the real acceptance gate now use a paid receipt OR an AND containing all first-payment requirements. The same $0.499 counterexample now leaves money, access and payment receipts unchanged. A generated regression also covers insufficient funds and the Treasury-skip flag across all ten host acceptance alternatives.

**GULF-EARLY-CHRONOLOGY-TEXT, P3, fixed.** Arm the Front formerly described the 1972-75 programme as an already past policy. That was misleading if players created an early Kuwait crisis in the date-free 1970 scenario. Its installed description now proposes clandestine aid through a cooperating border government without assuming those later events already happened.

**GULF-EXISTING-ACTOR-RACE, P1, fixed and independently retested.** The original uprising helper could transfer strongholds and declare war for a peaceful human KUR/PUK that appeared after the initial underground package. State eligibility now requires absent-tag creation, an actual Iraq war or explicit coordination by an independent local actor. The execution helper recounts at least two eligible hot states before marking the uprising as fired. A temporary new-tag receipt permits the second state transfer after the first creates that country, and is cleared afterward. War and unit creation additionally require the actor's own controlled rebel stronghold. Six independent cases cover a peaceful human actor in state 630, explicit independent opt-in, an existing Iraq war, a subject's unauthorized opt-in, only one hot state and a newly created actor receiving both prepared states. Peaceful non-participants receive no territory, unit or forced war; failed eligibility does not consume the uprising receipt. Repeated execution creates no extra column.

## Prospective effects and presentation

The preview generator shows unconditional, non-executing native effect sections. Named countries and complete numeric terms remain present before signatures and while requirements are locked. The revised Arm the Front preview separately shows the real underground preparation costs, recurring budget and later recorded-cache handover. Each prospective local construction alternative shows its own $0.2 billion cost, one extra shared slot and one infrastructure level. It does not display four buildings as a single one-state purchase.

Limited-war relief has the real $0.020 billion weekly rate against standard relief's $0.025 billion. The armed alternative retains the real $0.25 billion setup, 1,000-weapon commitment and $0.050 billion weekly support. Relief, safe-haven logistics, national air readiness and recipient-approved air cover retain distinct control, funding, basing and consent conditions. No preview variable becomes a real programme provider or transaction.

All nine installed Gulf runtime outputs compare semantically with fresh canonical generation, and the fifteen installed Gulf focus blocks match the direct pure overlay. The 266 other focus blocks are preserved. The immutable proposal hash remains `bdbec679bbe773ec793cba69f68fc5d37f83e2730548c459f055f02a2975fd34`.

The new Iranian event uses unchanged `GFX_political_deal`, inspected at 217 x 163 pixels. The live donor's standard country window is 581 x 427; its lower section is 581 x 206, picture origin (5,5), and adjacent option grid origin (215,-1), width 300 with 47-pixel vertical slots. The Iranian event has three possible options, including the staging alternative which requires its own pending offer. This reuses the existing donor geometry; it does not establish live tooltip fit or native popup ordering.

## Historical fit and evidence limits

The detailed primary-source record is [PLAYER_REVISION_RESEARCH_20261025.md](PLAYER_REVISION_RESEARCH_20261025.md). The implemented description and policy split respect its principal distinctions:

- Financial and material support began in July 1972 and used Iran; Iran's 1975 withdrawal of assistance could cut the supply route. This is a precedent for the armed alternative, not proof of an American-organized initial uprising in 1991. [FRUS 254](https://history.state.gov/historicaldocuments/frus1969-76v27/d254), [FRUS 289](https://history.state.gov/historicaldocuments/frus1969-76v27/d289)
- Bush's 15 February 1991 appeal encouraged Iraqi political action. His 3 April statement declined intervention in the internal civil war. Limited war without an initial rebel arms guarantee is therefore a real historical choice. [15 February remarks](https://www.bush41library.gov/digital-research-room/finding-aid/public-papers/remarks-raytheon-missile-systems-plant-employees), [3 April exchange](https://www.bush41library.gov/digital-research-room/finding-aid/public-papers/question-and-answer-session-reporters-hobe-sound)
- Desert Shield's defensive deployment preceded the conditional force authorization in Resolution 678. April refugee relief and protected camps were a further development, not an automatic consequence of a February appeal. Resolution 688 does not itself create Kurdish independence or an explicit no-fly zone. [Resolution 678](https://www.refworld.org/legal/resolution/unsc/1990/en/8997), [Resolution 688](https://www.refworld.org/legal/resolution/unsc/1991/en/113183), [16 April announcement](https://www.bush41library.gov/digital-research-room/finding-aid/public-papers/remarks-assistance-iraqi-refugees-and-news)

Final independently executed checks: 47 bounded unittest cases, 20 legacy fiscal cases, 14 native-treasury regression cases and 15 additional edge cases, totaling 96. The final nine runtime outputs and installed focus overlay were compared again after the actor-race repair was emitted. Existing harness report writes were intercepted in memory and Python bytecode writes disabled. These models do not simulate combat, actual resistance growth, native update ordering, graphical clipping, save loading or multiplayer synchronisation. Earlier native arithmetic/flag probes calibrate selected inputs only. A current-revision native and multiplayer run is still required.
