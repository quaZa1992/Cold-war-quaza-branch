# IMPERIA COLD WAR: project contract learned from the user's requests

Maintained authoring preferences, not blanket authorization. The current request wins. Keep country-specific choices country-specific; research-tree corrections are not national-focus geometry rules.

## Recurring requirements

| Concern | Apply this decision |
|---|---|
| Target | January 1970 Cold War multiplayer roleplay. Main MD/Imperia is a separate product; its individual audit decisions do not automatically apply here. |
| Base | Current MD architecture and supported APIs; preserve approved Cold War/Imperia additions and balance. |
| Language | All new in-game text in English. Communicate with Enes in German unless asked otherwise. |
| Design | Full spatial tree and effects first. A list is not a tree visualization. Respect an explicit approval boundary. Quality takes priority over focus count; a small country can have a compact tree. |
| Look | Native MD grammar, especially Generic/Russia 2000 and applicable Germany party branches. No invented font, giant gaps, arbitrary stretched grid or generic boxes substituting for the focus presentation. |
| Politics | Distinct programmes for relevant parties/leaders, with internal choices. Outlooks and exact governing subparties are different things. Historical starting leader, ruling subparty and country identity belong in dated history; inspect later native callbacks for overwrites instead of using startup patches as the source of truth. |
| Party visibility and requirements | Keep all party trees visible and inspectable; only execution and party programmes depend on governing. Do not hide them with party-dependent `allow_branch`. Reuse native MD exact-party `*_are_in_power` checks and their registered party-name tooltips, rather than invented "Governing political current" text or outlook/coalition substitutes. Use the actual party name instead of a present/future name joined by an arrow. |
| Gates | No extra 'over-focus' to unlock the already-ruling party. Avoid unnecessary date locks; retain genuine succession/event requirements. For newly authored focuses, use native MD cost deductions without adding a Treasury prerequisite by default. Preserve an existing explicitly approved funding contract unless the user changes it; removing an affordability gate must also remove its hidden application/retry veto. |
| Rewards | Calibrate values, costs, modifiers and reward bundles using comparable normal MD 2000-era focuses from Russia, Israel, Germany, Turkey and other relevant countries. Check units, duration and gates, then fit the target country and 1970 scenario. Rejected filler included 1% stability/10 PP or tiny construction gains as an entire programme. This preference does not authorize blanket numerical buffs. |
| Trade-offs | Both historically grounded exclusive options should be attractive enough that the player would like both. Give them distinct substantial benefits and a plausible modest drawback or opportunity cost. Audit the whole reachable programme and its stacking; strengthen existing choices before adding more. Shared ordinary development stays shared. Preserve serious historical starting problems rather than making every policy harmless. |
| Descriptions and effects | Learn and apply normal MD 2000-era conventions using suitable examples from Russia, Israel, Germany, Turkey and other relevant countries: specific national narrative and clear native effects with real values, costs and named outcomes. Reject raw design instructions, filler, placeholder localisation and developer bookkeeping in place of finished content. Review emitted prose and effects together; substantial rewrites receive an independent comparison. Word removal or a reference citation alone is insufficient. Hidden helpers need accurate previews. Duplicate graph-predecessor checks stay hidden; extra conditions remain visible. |
| Spirits | Relevant starting challenges, visible improvement and intentional party-bound cleanup. Avoid unconditional lists removing spirits a country never had. |
| Effect fields | Show only concrete native costs, signed modifiers, research/experience, named spirit changes and decision unlocks. No custom explanatory paragraphs about ownership, consent, expiry or internal handling; place needed context in descriptions or visible requirements. Native numeric formatters and standard MD headings are appropriate. Apply this across all focuses, decisions, event options and previews. |
| Acceptance previews | Every recipient-approved focus always shows both countries' complete prospective "If they accept" Effects with exact spirit modifiers, costs and other rewards, even before acceptance or while currently ineligible. Spirit names and later decision references alone do not suffice. Preview visibility is separate from execution and consent. |
| Cuban bilateral offers | Cuba chooses the concrete offer through separate national focuses. Only the recipient RP country receives the acceptance or refusal decision; do not replace the Cuban focus choice with a Cuban offer decision menu. |
| Code identification | Begin custom files with the exact `IMPERIA COLD WAR` marker in the format's valid comment syntax, after a mandatory language/header block only when required. Shared MD files identify the custom integration and retain upstream attribution; custom blocks stay marked. Update canonical generators too. JSON uses a schema-compatible project field; binary/rigid formats use companion provenance. |
| Building grants | One extra shared state building slot per granted building level, before construction in the same state and one-time guard. This explicitly includes province forts. Check actual owner, control, province and native capacity separately. |
| Costs and glyphs | Weekly MD monetary units; budget literals at most five fractional digits. English player text and previews contain no en/em dashes. Native numeric formatters must render signed values correctly. |
| Standing Cuban agreements | Distinct Cuban offer focuses; real recipient responses; indefinite paired spirits conditional on both countries existing, peace, and no bilateral native embargo or any of the four mirrored Imperia sanction classes. Restore without replaying fees/assets; active membership/parent spirits gate dependent content. |
| Event photographs | Use the actual MD country-event frame and correct viewport, not an arbitrary registered sprite or wide news art. Inspect decoded art, topic/date, transparency and the full adjacent answer-button layout. See the Cuba lessons for the measured donor and workflow. |
| Art | Inspect existing appropriate Cold War/MD icons. Resolve the actual texture: national spirits use appropriate idea artwork, not a focus medallion renamed with an idea alias. Texture existence is not semantic suitability. Show material art choices when requested. |
| Review | Economical agents for native MD comparison, inventory, layout and independent correctness. Give tasks meaningful names and inspect their findings. |
| Evidence | Static QA, rendered preview and engine test are different. Never call an observed hover crash fixed merely because unrelated warnings disappeared. |

## Failures to avoid

- Showing only additions, leaving neighbours out of the preview, then creating overlaps or vast empty zones.
- Preview and installed output using different coordinates, prerequisites, effects or generation sources.
- Treating a tooltip, localization entry, unconsumed variable or custom modifier registration as an executable benefit.
- Copying a state/equipment/subunit field into a country idea; confusing flat numbers, percentages, percentage points and tick frequency.
- Giving 'party support' to the wrong MD slot or pairing the wrong outlook with a subparty.
- Adding ceremony/unlock focuses despite the required party already governing.
- Copying another country's state IDs or leader/party/portrait references. Valid IDs can still point to the wrong geography after map changes.
- Inventing a new menu, fee, leadership system, virtual supply source or parallel EU system instead of integrating into existing MD systems.
- Replaying one-time rewards during refresh/load or retaining an old government's temporary programme without intent.
- Reporting catalogue totals as installed distinct people/assets or including held content as complete.
- Hiding every prospective reward number behind a currently false treaty/party condition while leaving its heading visible. Preview future terms; keep real consent and activation in the execution path.
- Assuming modern resources/buildings belong in1970, or deleting the traditional economy while depicting a difficult start.

## Scoped examples

- **Spain:** user requested viable Falange/continuity and Bourbon alternatives, including economic/military continuation. Party programmes follow actual governing party; authoritarian entry has the relevant outlook gate. This is not every country's transition template.
- **Israel:** no Shia/Salafist paths were requested. User wanted genuine internal policy choices, office development, corrected Sinai geography and less generous easy integration rewards. Do not generalize its policy balance to other countries.
- **North Vietnam:** the user approved the visual concept before implementation, requested all focus cards to be clickable and a wider inspector, and then asked to retain the implementation lessons in these skills. The historical/alternate roster and January 1970 constraints remain Vietnam-specific; see `vietnam-integration.md`.
- **Soviet Union:** January 1970 constraints should be hard but manageable, with credible leader/party variation. Preserve Politburo/succession systems rather than replacing them with a new menu.
- **Greece/Cyprus:** programme funding and consent contracts are specific to their systems. A focus concerning another player's territory is not a shortcut around diplomacy or the recipient's response.

- **UAE / Trucial States:** the user explicitly replaced the initial North Vietnam mention with UAE. Keep the protected1970 opening, dated withdrawal, independence-only transition and focus-driven federal proclamation distinct. Start with low oil, no metals/composites and real maritime livelihoods; development changes their relative importance. The +200% tree-growth cap and exact maritime/oil values are scoped to UAE; see [the correction record](uae-1970-lessons.md).

## Scenario boundaries

Initial research and starting armies/equipment were deferred, the 1985 start removed, and future research limited with specific exceptions. A focus task does not authorize rebuilding those starts, enabling deleted modules or reactivating archived chains. Recheck the current task and data before reusing old rewards.

Historical starting leaders stay unless explicitly changed. Additional politicians integrate with existing country systems. Current successor-list ordering is not a universal national-focus rule.

Resolve routine technical choices from actual MD analogues and existing approvals. Ask only when uncertainty changes gameplay, history, selected imagery or an approved design, giving a concrete understandable consequence. Do not re-ask permission for authorized work or quietly invent values for unresolved cases.

## Cuba correction record

The current Cuba conversation explicitly reiterated exact file-start branding and asked that all learned expectations be retained in these skills. [Cuba implementation lessons](cuba-implementation-lessons.md) records the reusable contracts and separates them from Cuba-only choices: the 120-focus ceiling, 13-focus Fidel programme, an island STATE rather than a country, independent DDR diplomacy, negotiated blockade relief, localized Cuban defences and alternative operating costs for medical/overseas programmes. These examples do not authorize unrelated changes or impose Cuban history on other trees.
