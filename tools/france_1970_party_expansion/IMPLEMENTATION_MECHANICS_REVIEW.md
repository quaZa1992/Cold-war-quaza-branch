IMPERIA COLD WAR

# France 1970 party expansion implementation review

## Reviewed inputs and scope

This review covers the compiled implementation of the approved expansion proposal, SHA-256 `c8e6ab3933bf72a14b043c3a92d846826f3d1937f902efc7cc3d0dd64364c055`. The compiled design has 176 focuses and retains 35 recipient-approved offers. Twenty focuses were added; the existing Regional Conversion Fund gained an alternate parent requirement. This review did not edit runtime generators or emitted game files.

Reviewed hashes:

- Compiled design: `57b479c47dafef3d83917931994617bf08c1467d8a00175aa28da957a7518628`
- Core generator: `46d7f97c157962371d96eb945c31a8d61e23124a2b44cf254ca9d277bca71bc6`
- France focus script: `25668f30f1cc830d8a62edea9e7def613813ee665f27f0df79cf35436d7e6843`
- France effects script: `d3a39192c708b8171a6f7d33b99c9c4ce808eb96b743c36654ae42747f1d8894`
- France triggers script: `e84b66171ceb9ee5fc89deddb87aa172af87b4a04a262a189e7956a6fa7e4e47`
- France domestic decisions: `6b862fcc455c6bad95ba09e8334a54673baabfcd14bdfdcfb631a6d2934290e4`
- France English localisation: `3116b2291f907c0deeedcd0b1769684179d1ed150ec78e75f28270760e367601`
- Diplomatic generator after the cost-preview repair: `6e05b5d07d65bc34db547c50bab679283ab2c9d8e27b45da922a3985e954c2c3`

## Findings

The 20 added focus rewards are wired through guarded completion providers. The exact native ruling-party requirement stays visible. Scenario, replay and positive-GDP checks stay inside hidden availability; state ownership, control and full control for both buildings and standalone slot grants are shown through a visible named asset requirement tooltip. Physical building capacity remains a separate guard. The completion provider repeats the transaction guards. The native Effects preview is separate from execution.

All 32 added building levels have 32 shared slots granted within their one-time construction helpers. The five additional standalone slots are site preparation and are separate from those building levels. The new asset helpers resolve uniquely; ownership, control, full control and native building capacity remain separate checks. The two recently moved infrastructure projects target Auvergne (state 962) and Pays de la Loire (state 959), respectively, and are checked against their current state IDs and infrastructure caps.

The Regional Conversion Fund remains the same one-time transaction. The before/after proposal records show unchanged effects: its 0.40% own-GDP setup debit, one Hauts-de-France civilian factory and one CAT_industry bonus. The existing Public Bank Credit prerequisite now has the alternative of Conversion Boards. The emitted decision checks either completed focus, current PS party power, state control, native factory capacity, positive GDP and its completion receipt before payment and construction.

The CID save migration is receipt-based and one-time. It clears stale Right/CID modifier pool values, rebuilds the current pools from existing earned focus receipts, and preserves those receipts. It does not replay the focuses' Treasury fees, assets, research or other finite rewards. The dedicated migration detaches the stale Right dynamic modifier once; normal programme sync restores Right only when a surviving Right/FN focus receipt supports it. The CID pool has its own party and date conditions, so it suspends on government change and ends when the CID identity is replaced on 5 October 1972.

The authored source was executed through a restricted AST model. It passed the old-CID receipt rebuild, migration replay, a CID-only old save with a stale Right spirit, government leave/return, and the 1972-10-05 CID-off/FN-Right-on case. The checker rejects unmodelled migration or sync effects and disallows Treasury, construction, research and other finite effects in these migration paths. See [IMPLEMENTATION_CHECKS.json](IMPLEMENTATION_CHECKS.json).

The cost-preview repair keeps one native Treasury row for each setup debit and adds a separate display-only quote for each side's weekly GDP expense, converted to millions and formatted to two decimals. The check covers all 70 country-side previews, confirms 105 preview call sites are inside `effect_tooltip`, and verifies all 144 non-preview diplomacy providers retain their prior hashes. It reports zero issues in [COST_DISPLAY_CHECKS.json](../france_1970_runtime/COST_DISPLAY_CHECKS.json).

The compiled source validator reports zero issues across 176 focuses, 35 offers and 1,023 English localisation keys. The root also reports a clean compile check. These checks establish source structure and a restricted AST model, not native rendering or live game behavior.

## Limits

No HOI4 engine or native tooltip session was run for this expansion. The migration model does not load a real save and cannot establish engine timing, native dynamic-modifier refresh behavior, live treasury presentation, or multiplayer/rehost behavior. Those remain outside this source review.
