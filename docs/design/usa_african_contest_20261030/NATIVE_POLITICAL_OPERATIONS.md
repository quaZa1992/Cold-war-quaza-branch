IMPERIA COLD WAR: Global American political operations using native MD
====================================================================

User clarification: the United States should be able to provoke unrest and support Western-aligned uprisings worldwide, using meaningful MD mechanics rather than only paying friendly governments. This revises the current design and visualization. It does not install the new protest-financing decision or change native MD access.

Current custom content
----------------------

The Kurdish underground system already funds networks before statehood in Iraq, Iran, Turkey and Syria. Its finance operation adds 15 regional organisation and 5 unrest, subject to its campaign, route, funding, settlement and cooldown conditions. Those are regional Kurdish movements, not a generic worldwide Western-outlook rebellion.

The current Chilean programme applies Stability -3% and Police Cost +2%; it does not trigger a coup or change the government. The current Angolan agreement supports an actual UNITA country. The proposed African extension establishes earlier movement contacts and adds local political and military choices. Neither creates a global Western-opposition campaign by itself.

Native foundation
-----------------

| Action | Existing authority | Meaning |
| --- | --- | --- |
| Manipulate politics | `manipulate_politics_action` in `common/scripted_effects/00_influence_scripted_effects.txt`; human GUI guards in `common/scripted_guis/01_influence_scripted_guis.txt` | USA among the top three influencers with at least 30%, 100 PP at the ordinary cost, 28-day sender-target cooldown. The default action supports the target party slot corresponding to the sponsor's actual governing party. It spends 10 influence points. It does not select any arbitrary party. |
| Influence coup | `influence.44` then the sponsoring country's `influence.5` in `events/Influence.txt` | Largest influencer with at least 50%, more than 200 PP before initiation, different target outlook, not the sponsor's subject, native country protections and Western-features game rule. Confirmation costs 200 PP and adds 2 world-tension points. Native weights can produce a takeover, civil-war outcome or failure/exposure. The strongest local party in the sponsor's actual outlook is the coup candidate. |
| Native protests | `protest_strength`, `check_protest_trigger`, `MD_incoming_protest_movement`, `MD_incoming_revolt` | Pressure, warnings, government remedies, state resistance and eventual escalation already exist. A native protest civil war currently uses the incumbent outlook; funding unrest alone is not a promise of Western rebels. |
| Lend-lease | Existing diplomacy | Actual weapons and other equipment can support an existing Western-aligned armed partner through the ordinary offer and acceptance route. No virtual recipient, automatic American divisions or new rebel state is fabricated. |

The displayed 1.2-percentage-point manipulation example is the current unmodified formula, 0.08 multiplied by a clamped 0.15 factor. Real effects must continue using the native formula and party/outlook effects, not a fixed 1.2-point replacement. The corresponding-party-slot manipulation and strongest-party coup selection are distinct.

The separate `common/timed_activities/00_stage_coup.txt` definition's 1,000-weapon requirement is not the influence-coup GUI transaction. Do not silently combine those two entry points or charge the same political cost twice. Preserve the ordinary political cooldown and the same country-specific protections, including Eritrea's transitional authority.

New proposed US decision
-------------------------

**Finance Protest Organisers** is the one extra targeted action in this revision. It requires the existing Political Operations focus, a Western US government, an established local Western opposition with at least 10% outlook support, a top-three American influence share of at least 30%, and the absence of native protest-disable, protest-cooldown or political-protection conditions. The target must not have received this financing in the preceding 28 days.

Proposed one-time cost: **0.0005% of current US GDP and 50 PP**. Proposed effect: **+10 native protest strength, capped at 100**. This is a balance proposal, not an existing MD action. There is no new unrest meter, passive strength modifier, global daily scan, automatically activated revolt or forced warning reset. Native processing decides whether the pressure survives, triggers a warning or develops into resistance. Eligibility and funds must be rechecked at execution before any fee or target change.

A hostile government does not approve outside support for its opponents. It keeps its own influence defence, reforms, spending choices, native protest decisions and garrisons. A real future partner approves cooperative aid and contracts. These two forms of agency must not be confused.

Political workflow
------------------

Build influence, support the represented Western opposition and decide whether to fund unrest. When influence and local support warrant it, use the existing native coup process. Supply a Western front only if an actual partner emerges. A successful political takeover is also a valid native outcome; a Western civil war is not guaranteed.

Native-action arrows in the preview show this political workflow, not newly imposed focus prerequisites. Existing political manipulation, coups and lend-lease retain their own access. The proposed protest-financing decision is the new focus unlock. The Political Operations focus remains the native country entry rather than four ceremony focuses duplicating existing diplomacy.

Historical basis
----------------

American support to Chilean political parties, media and opposition organisations is a relevant precedent for political intervention, but neither all American clients nor all anti-communist movements were liberal democrats. The Western MD outlook is therefore explicit in this route, while the Angola and Kurdish programmes keep their own local actors and aims. [Office of the Historian: Chile](https://history.state.gov/milestones/1969-1976/allende), [US Senate Intelligence Committee: covert activities](https://www.intelligence.senate.gov/wp-content/uploads/2024/08/sites-default-files-94intelligence-activities-vii.pdf).

Verification
------------

The revised preview distinguishes native actions, proposed decisions and focuses. Its source-level interaction fixtures inspect all 36 entries and preserve all prospective values. A separate native-asset composition checks six views at wide and narrow diagram widths. Native engine, live browser and multiplayer behavior are not certified. No loaded game files or immutable approval snapshots change in this design revision.
