IMPERIA COLD WAR

# Cyprus refusal war-goal review

## Finding

The native `create_wargoal` effect is documented for country scope, but the installed effect reference does not enumerate its arguments or offer an inline expiration field (`E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/effects_documentation.md:3311-3318`). Main-MD examples confirm these forms in use:

- Full Enosis: `create_wargoal = { type = annex_everything target = CYP }`. The type exists in [`common/wargoals/00_invasion.txt`](../../common/wargoals/00_invasion.txt:107) and a native event creates it in `events/yugoslavia_events.txt:43-49`.
- Southern Union: `create_wargoal = { type = take_state_focus target = CYP generator = { 145 } }`. `generator` state syntax is used by the Abu Musa decision (`common/decisions/COLDWAR_PER_Abu_Musa_1970.txt:52`) and by a main-MD focus (`common/national_focus/COLDWAR_EGY_1970_focus.txt:25494`). The native `take_state_focus` type has `expire = 730` days (`common/wargoals/00_invasion.txt:15-29`).

`annex_everything` has no `expire` value in its native definition (`common/wargoals/00_invasion.txt:107-127`), so the source does not establish a finite lifetime for it. Do not add `expire = N` inside `create_wargoal`: no installed documentation or example verifies that syntax. If a finite lifetime is required, define project-specific wargoal types with explicit `expire` values and validate them in game; otherwise disclose that the native annex goal has no verified expiry. The state goal's default 730-day expiry is long but finite.

## Required transaction boundary

Create the goal only from the explicit CYP refusal option belonging to the currently pending Enosis instance. The option must recheck the pending instance ID, route, CYP recipient, and refusal response, then consume one shared GRE receipt that prevents either Enosis route from issuing a second goal. Timeout, offer cancellation, another guarantor's refusal, or a stale event must not issue it. For `take_state_focus`, require state 145 still owned by CYP at issuance. For `annex_everything`, recheck the route's expected CYP territory (145 and 146) before issuance so the goal cannot silently expand to extra territory. The goal grants a claim to declare war; it must not automatically declare war.

## Keep the war paths separate

The existing `COLDWAR_CYP_R2_ACT_gre_escalate_apply` is specifically the Greek intervention against TUR on CYP's side: it snapshots and separates GRE/TUR from NATO, then uses `add_to_war = { targeted_alliance = CYP enemy = TUR }` (`common/scripted_effects/COLDWAR_CYP_R2_crisis.txt:361-400`). Its availability also requires TUR already at war with CYP (`common/scripted_triggers/COLDWAR_CYP_R2_crisis.txt:138-150`). It is not valid for the new GRE-against-CYP war.

Treat the refusal war as a separate conflict instance: GRE receives the goal and may later declare against CYP; TUR's possible intervention for CYP needs its own explicit response and `add_to_war` path after the actual GRE-CYP war begins. Snapshot NATO membership for only the countries whose positions this new conflict changes, before making any change. Do not reuse the old helper's GRE/TUR separation receipts or its restoration conditions: those currently key off the GRE-TUR and CYP-TUR peace pairs (`common/scripted_effects/COLDWAR_CYP_R2_crisis.txt:644-666,707-729`), which do not by themselves describe the new GRE-CYP conflict. Define cleanup against the actual war pairs of this separate instance, preserving NATO leadership and unrelated faction memberships.

## Verification limit

This is static source evidence. The wargoal parameter forms are established by native definitions and main-MD usage, but the new refusal route, exact expiration behavior in a live save, and three-party intervention/NATO lifecycle still need an engine scenario check.

## Final data recheck

The current `enosis.py` data resolves the design-level gaps above: each route limits issuance to the explicit CYP refusal for the matching live offer and government snapshot; both share `COLDWAR_GRE_R2_enosis_refusal_wargoal_issued`; timeout, cancellation, stale offers and other signatories' refusals are excluded. It assigns `annex_everything` to full union and `take_state_focus` with generator state 145 to southern union, in GRE scope against CYP. The data does not claim an inline expiry, and uses the native 730-day lifetime for the state goal. These match the source-supported forms.

The revised Turkish response is also separated: it joins CYP against GRE only after the actual GRE-CYP refusal war. Its NATO snapshot and restoration pairs are scoped to this conflict (GRE-CYP and GRE-TUR), rather than borrowing the old GRE-on-CYP-side-against-TUR helper. Both formerly identified design contradictions are resolved in the current concept data. Remaining checks are implementation and live-engine behavior: correct event-scope enforcement of the current-instance receipt, native faction handling while GRE and TUR oppose each other, peace-trigger restoration, and the native lifetime/availability of `annex_everything` in the refusal scenario.
