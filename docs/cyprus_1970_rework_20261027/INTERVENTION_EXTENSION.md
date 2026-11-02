IMPERIA COLD WAR: Turkish intervention, army crisis and Greek escalation

Concept extension requested 27 October 2026. Not implemented in the loaded mod. The 100 Cyprus focuses stay intact. Supporting guarantor focuses now include a Turkish intervention/refusal fork and a Greek volunteer/direct-war fork.

## Player-visible intervention terms

### Cyprus Intervention Forces

- Cyprus Intervention Forces (180 days)
- Navy organization +15%
- Naval invasion preparation speed +50%
- Amphibious invasion attack +15%
- Planning speed +30%
- Maximum planning +20%

### Angry General Staff

- Angry General Staff (180 days)
- Stability -10%
- Army organization -10%
- Political power gain -15%

### Command Reorganization

- Command Reorganization (90 days)
- Army organization -5%
- Political power gain -5%

### Cyprus Volunteer Mission

- Cyprus Volunteer Mission (while the Cyprus mission remains eligible)
- Volunteer division limit +2
- Minimum army size for volunteers -100%
- World tension requirement for volunteers -100%
- Political power gain -5%

Turkey pays 75 political power and 0.5% of its own current GDP once on authorizing intervention, with 0.005% GDP per week while the expedition is active. The military bonus has an absolute 180-day expiry and ends earlier at related peace. Calling the operation through a later army-crisis response cannot renew an already used bonus.

## Refusal and civilian control

Only this campaign crisis, after a real constitutional rupture and failed guarantor consultation. Resolved security terms cancel the countdown and military plot. No pressure merely for an ordinary peaceful disagreement.
Refuse Intervention starts the army crisis immediately. Inaction or failed negotiations starts it when the 30-day deadline expires. A successful real settlement avoids it.
No daily drift or random daily coup roll. Pressure starts at 70, each of two once-only measures removes 25, the day 30 memorandum adds 15, and day 60 resolves the disclosed thresholds.
At day 60: pressure>=60 installs the dated native military-junta government; pressure 36..59 produces a defeated plot and stability -5%; pressure<=35 with the two control measures defeats the plot. A takeover does not automatically declare another war.

This is the sole authorized native decision-menu exception. It appears only for the active Turkish army crisis, contains four finite actions, and disappears at resolution. The rest of the Cyprus concept uses focus choices and foreign response events.

### Reassign Exposed Commanders

Angry General Staff crisis active. Not already used. Civilian government remains.

- Political power -50
- Treasury -0.25% of current Turkish GDP
- Military pressure -25

### Secure a Parliamentary Mandate

Angry General Staff crisis active. Not already used. Civilian government remains.

- Political power -75
- Military pressure -25

### Reassert Civilian Authority

Both control measures are completed. Military pressure at most 35. The coup has not succeeded.

- Political power -75
- Treasury -0.25% of current Turkish GDP
- Remove Angry General Staff
- Command Reorganization (90 days)
- Army organization -5%
- Political power gain -5%

### Authorize the Cyprus Operation

The same Cyprus security crisis remains unresolved. Turkey has not intervened in this crisis and is not already at war with Cyprus.

- Political power -75
- Treasury -0.5% of current Turkish GDP
- Remove Angry General Staff
- Turkey declares war on Cyprus
- Expense +0.005% of Turkish GDP per week while the intervention is active
- Cyprus Intervention Forces (180 days)
- Navy organization +15%
- Naval invasion preparation speed +50%
- Amphibious invasion attack +15%
- Planning speed +30%
- Maximum planning +20%

At pressure 70, the two once-only measures lower pressure to 20. If the day 30 memorandum has already happened, they lower 85 to 35. Both meet the stated civilian-control threshold. No actions by day 60 leave 85 and cause the coup. The two control measures cost 125 PP and 0.25% GDP; immediate civilian settlement adds 75 PP and 0.25% GDP. Both are alternatives to an expedition and its continuing expense.

Success or failure is disclosed rather than an unexplained random percentage. A resolved Cyprus security settlement cancels the external-crisis trigger; a genuine peaceful solution is not treated as ordinary inaction. A cabinet change alone cannot erase a pending army confrontation. A successful military takeover uses the actual dated native Turkish party/leader roster, whose exact selection still requires implementation review.

## Greek intervention and NATO

Greek volunteers require Cyprus acceptance via the real diplomatic volunteer action. Permission modifiers reduce native thresholds and increase capacity, but do not create units or certify deployment. Global can_send_volunteers rules are not overwritten. The wartime mission pauses when its eligibility fails and expires with the relevant Cyprus war; native volunteer return behavior still needs an engine check.

Direct Greek entry costs 100 PP and 0.5% Greek GDP. It uses the native add_to_war shape with targeted_alliance=CYP and enemy=TUR after shared NATO_leave effects. It creates co-belligerency with Cyprus rather than forcing Cyprus into a new faction. Full NATO exit is only triggered by this direct-war branch, not initial Turkish intervention or volunteer assistance.

Before either exit, snapshot GRE and TUR memberships separately, the current NATO faction, and the one-shot conflict instance. Remove through the native NATO_leave helper before war entry; do not just remove the idea or manually alter global.nato_members. This prevents the normal Article 5 script from seeing Turkey as a current member attacked by a newly nonmember Greece. NATO_leave already owns array, access, opinion, technology-sharing and leadership cleanup.

Automatic return requires both GRE-TUR peace and CYP-TUR peace. Unrelated wars need not end. Use NATO_join for prior members only, with an actual living NATO leader, independence, no conflicting faction, and no war against current NATO members. A missing/dead country or incompatible faction retains a pending receipt; retries are monthly rather than daily. Snapshotting both before either removal prevents sequential-state errors. Never restore a country that was outside NATO before the crisis.

The temporary-separation receipt also blocks early re-admission through NATO_join, NATO_join_via_eventandstale accession responses while the relevant war remains active. A different NATO accession path must not put one participant back inside the Alliance mid-war and create a fresh Article 5 cascade. The same small guard belongs at the native membership entry transaction, with a targeted direct-idea callback fallback if needed; those shared integration edits are still unimplemented.

The requested default is automatic return of both 1970 members. Exceptional later player changes can make native faction entry impossible; those are disclosed pending-state cases rather than silently forced diplomacy. Full immediate automatic restoration after every possible external-state mutation is not proven by source inspection.

The native left_nato opinion penalty is -20 and is not explicitly removed by NATO_join. The concept retains this diplomatic consequence and shows it for both countries at departure; full membership returns, but diplomatic confidence is not silently reset. The pre-existing +30 NATO member opinion is removed/reapplied by the native helpers. No custom diplomatic penalty is stacked.

## Scheduling and evidence

One-shot crisis events at 30,60 and 180 days. Flags/instance receipts discard stale events. Existing monthly fallback only; no new daily or weekly relationship observer.
All deadlines are relative to army-crisis activation, not the original consultation date. Explicit refusal activates immediately; no-action or failed diplomacy activates after the 30-day intervention window. Any successful intervention, accepted security resolution or completed civilian-control settlement marks the army-crisis instance closed before removing the spirit. All pending 30/60/180-day outcomes require the same still-active instance and therefore become no-ops. The original 180-day intervention expiry receipt is separate and cannot be restarted.

Actual entry and peace/settlement effects call the targeted reconciliation immediately. Native peace-conference hooks and a monthly fixed-tag fallback finish restoration when ordinary peace delivery is not observed. One-shot delayed events at 30/60/180 days are finite deadlines, not recurring daily polling. Recheck the crisis instance before every payment, decision completion and scheduled outcome. Native weekly money bookkeeping reads only cached expedition/mission expense; no relationship scan is added.

Source checks: common/scripted_effects/01_NATO_effects.txt(NATO_leave, NATO_join); common/ideas/Factions.txt(NATO_memberarray hooks); common/on_actions/MD_NATO_on_actions.txt(Article 5 andadd_to_war); common/scripted_triggers/00_NATO_scripted_triggers.txt(can_join_NATO). See RESEARCH_NATO_RUNTIME.md and REVIEW_INTERVENTION_MECHANICS.md for exact references and remaining native-action limits.

Historical distinction: Greece left integrated military command in 1974 but remained an Alliance member; it returned to integrated command in 1980. The requested simultaneous full exits and automatic returns, along with a refusal-triggered Turkish coup chain, are RP alternate history and balance proposals. See RESEARCH_INTERVENTION.md for FRUS, UNFICYPandNATO sources.

Static data checks and browser review do not establish in-game faction transitions, actual volunteers, event arrival, coup leaders, naval battle behavior or live multiplayer performance.
