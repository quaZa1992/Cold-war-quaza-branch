# Project contract learned from the user's requests

Maintained authoring preferences, not blanket authorization. The current request wins. Keep country-specific choices country-specific; research-tree corrections are not national-focus geometry rules.

## Recurring requirements

| Concern | Apply this decision |
|---|---|
| Target | January 1970 Cold War multiplayer roleplay. Main MD/Imperia is a separate product; its individual audit decisions do not automatically apply here. |
| Base | Current MD architecture and supported APIs; preserve approved Cold War/Imperia additions and balance. |
| Language | All new in-game text in English. Communicate in the language requested by the current user. |
| Design | Full spatial tree and effects first. A list is not a tree visualization. Respect an explicit approval boundary. |
| Look | Native MD grammar, especially Generic/Russia 2000 and applicable Germany party branches. No invented font, giant gaps, arbitrary stretched grid or generic boxes substituting for the focus presentation. |
| Politics | Distinct programmes for relevant parties/leaders, with internal choices. Outlooks and exact governing subparties are different things. |
| Gates | No extra 'over-focus' to unlock the already-ruling party. Avoid unnecessary date locks; retain genuine succession/event requirements. |
| Rewards | Meaningful, contextual effects at a comparable MD scale. Rejected filler included 1% stability/10 PP or tiny construction gains as an entire programme. This is not authorization for blanket numerical buffs. |
| Trade-offs | Costs/disadvantages where plausible, not attached mechanically to every focus. Avoid cosmetic alternatives with one universally superior outcome. |
| Monetary costs | Across all countries, price paid focus, decision and event actions within $1.000-$10.000 billion according to their importance and the strength of their benefits. Own spending may overdraw the treasury through native MD borrowing. |
| Tooltips | Normal completion effects show the real rewards. No artificial 'Completion Reward' paragraph appended to narrative descriptions. Hidden helpers need accurate localized previews. |
| Spirits | Relevant starting challenges, visible improvement and intentional party-bound cleanup. Avoid unconditional lists removing spirits a country never had. |
| Art | Inspect existing appropriate Cold War/MD icons. Texture existence is not semantic suitability. Show material art choices when requested. |
| Review | Economical agents for native MD comparison, inventory, layout and independent correctness. Give tasks meaningful names and inspect their findings. |
| Evidence | Static QA, rendered preview and engine test are different. Never call an observed hover crash fixed merely because unrelated warnings disappeared. |

For monetary cost calibration, use the lower end for limited actions and the upper end for major programmes or strong, broad or lasting buffs. Consider benefit duration, repeatability and associated burdens when choosing the amount. MD treasury effect arguments are already in billions: this range means values 1-10, not 1000-10000. Updating this rule alone does not authorize repricing existing content; retain the borrowing mechanics described in [runtime-presentation.md](runtime-presentation.md#state-expenditure-and-borrowing-all-countries).

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

## Scoped examples

- **Spain:** user requested viable Falange/continuity and Bourbon alternatives, including economic/military continuation. Party programmes follow actual governing party; authoritarian entry has the relevant outlook gate. This is not every country's transition template.
- **Israel:** no Shia/Salafist paths were requested. User wanted genuine internal policy choices, office development, corrected Sinai geography and less generous easy integration rewards. Do not generalize its policy balance to other countries.
- **Soviet Union:** January 1970 constraints should be hard but manageable, with credible leader/party variation. Preserve Politburo/succession systems rather than replacing them with a new menu.
- **Greece/Cyprus:** programme funding and consent contracts are specific to their systems. A focus concerning another player's territory is not a shortcut around diplomacy or the recipient's response.

## Scenario boundaries

Initial research and starting armies/equipment were deferred, the 1985 start removed, and future research limited with specific exceptions. A focus task does not authorize rebuilding those starts, enabling deleted modules or reactivating archived chains. Recheck the current task and data before reusing old rewards.

Historical starting leaders stay unless explicitly changed. Additional politicians integrate with existing country systems. Current successor-list ordering is not a universal national-focus rule.

Resolve routine technical choices from actual MD analogues and existing approvals. Ask only when uncertainty changes gameplay, history, selected imagery or an approved design, giving a concrete understandable consequence. Do not re-ask permission for authorized work or quietly invent values for unresolved cases.
