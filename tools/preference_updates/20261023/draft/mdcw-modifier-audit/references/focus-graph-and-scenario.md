# Focus graph, references, and 1970-scenario reachability

## Follow every live reference

For each reviewed focus, start with its ID, `available`, prerequisites, exclusions, and completion effect. Follow calls until the resulting effect is understood. A focus is not audited when its own block looks valid but a called effect, trigger, idea, event option, or condition is missing or inactive.

Check these linked resources from the actual script:

- Focus prerequisites, mutually exclusive focuses, relative-position anchors, country/date/party gates, and callbacks.
- Every `country_event` or `state_event` ID and relevant option; check option conditions, costs, accepted/rejected branches, follow-up events, scopes, and retry or refund behavior.
- Referenced scripted effects and triggers, ideas, dynamic modifiers, flags and variables. For any stateful feature, trace where state is set, read, reset, and removed.
- Focus icon/sprite name through an interface sprite registration to an existing texture file; focus name and description localization, plus all visible tooltip keys in English localization.
- Equipment bonus names and equipment targets, research categories used by real technologies, and doctrine-cost categories used by the intended doctrine tree.

Use exact keys and paths. Search all relevant scripts and localization, not only the focus file. Transitive references that leave the tree—especially an event option or common cleanup effect—are part of the audit.

## Check transitions and cleanup

For rewards whose availability follows a governing party, ideology, coalition, or temporary status, inspect the transition path in both directions. Verify that the feature is granted only to the intended current holder, that a departing party's dynamic idea is removed or recomputed when appropriate, and that a returning party can be handled without stale or duplicate state. Check what should persist: one-time construction, completed historical choices, and permanent claims may intentionally survive even when a timed or party-specific modifier does not.

Do not introduce an automatic reset merely because the government changes. Establish ownership and intended persistence from the existing feature design and current MD lifecycle. If no cleanup path can be proven from source, report the gap instead of inventing a mechanic.

## Verify the actual 1970 route

A globally valid focus can still be inaccessible in the requested campaign. Establish the real 1970 starting tag, party/government, relevant variables and flags, tree loader or scenario dispatcher, and any legacy-tree guard. Multiple `prerequisite` blocks are AND; multiple `focus` fields inside one block are OR. Thus `{A,B}` plus `{C}` means `(A OR B) AND C`. Include `available` conditions, not just the graph edges, and test whether mutually exclusive histories can actually satisfy the combined requirement.

Follow scenario setup through events and decisions when the tree's first playable route depends on them. Check date gates against formation/leadership history and confirm that starting values do not bypass or deadlock the intended branches. If a later-year branch is supposed to be unavailable at campaign start, verify that the gate is attached to the route rather than merely present in localization.

The local `tools/israel_1970/validate_design.py` illustrates graph checks for missing nodes, asymmetric exclusions, grouped prerequisite reachability and mutually exclusive policy combinations. `tools/israel_1970/validate_content.py` demonstrates transitive checks for ideas, dynamic modifiers, events, localization keys, sprites/assets, flags, and 1970 history/dispatcher integration. `tools/israel_1970/validate_policy.py` models budget reservation/refund and state transitions, while `validate_policy_map.py` checks project-specific territorial references. Read and adapt only the checks relevant to the tree being audited.

## State the confidence boundary

Static checks can establish that IDs resolve, the route graph reaches a node under modeled conditions, and source code preserves the expected state transitions. They cannot prove that the game engine loads the focus tree, that every scope resolves as intended at runtime, that tooltips render correctly, or that a save migrates cleanly. Report separately any required parser/load, tooltip, campaign-start, transition, or save test. Never write “works guaranteed” from static validation alone.

## Soviet examples: authority and cooperative outcomes

`cw_focus.py`'s `plenum_focus` separates candidature from installation through existing Politburo decisions/events; leader programmes read actual office flags. Audit all three states. Do not give every country a Politburo or treat a candidature as having taken office.

For an offer, follow proposer helper -> receiver event -> accept/refuse -> payer/beneficiary effects -> proposer reply -> completion/pending cleanup. Pipeline event `COLDWAR_SOV.118` charges its payer on acceptance, guards a one-time Soviet reward and replies through `.900`/`.901`. Check retries, absent recipients, changed ownership/government and delayed replies against the actual contract. Sending a proposal is not executing the project.

`COLDWAR_UNI_1970_union_joint.txt` has member conditions, conditional host offset and initiator/member reward blocks. Audit each eligibility/reward scope; ensure shared root, attachments, referenced joint focuses and providers are loaded together. Distinguish supported joint-focus blocks from ordinary syntax; do not flatten member effects into repeated originator grants.

For decision unlocks, prove category visibility and usable actions, not only the flag/tooltip. Soviet planning/grain decisions illustrate start conditions, costs and expiry; their exact values remain country-specific.
