IMPERIA COLD WAR

# France follow-up corrections, 29 October 2026

These changes follow the user's live screenshots and later balance instructions. They supersede the earlier 437-assertion build where their content differs. The immutable original and party-revision approvals remain intact; the later instructions are implemented as narrow overlays and generator corrections.

## Native group opinion and effect headings

The erroneous faction-opinion preview formatted an absolute value of -5 as a fractional percentage and displayed -500%. Actual execution already passed -5 to MD's opinion helper. Focus previews now call the same native helper with `temp_opinion`, using MD's own faction labels, point formatting, current opinion and native adjustments. The three custom percentage opinion formatter keys are retired. All 27 authored opinion effects retain their intended point values.

National-spirit changes, costs, assets, research and opinion now appear before the programme-modifier heading. The native 'Modifies' heading covers only the actual dynamic-modifier deltas. Removing a spirit and adding programme changes is valid script, but the previous blanket heading obscured which values belonged to which operation.

## Starting difficulties

- Executive Safeguards and Parliamentary Checks replace the original presidency with Unsettled Institutional Balance: stability -2% and bureaucracy costs +4%. The original +10% political-power benefit ends. The residual clears only at the existing, longer funded Civic Settlement chain.
- Technical Colleges and Mass Universities leave Higher Education Expansion Pressures: education costs +4% and production efficiency growth -1%, with no automatic expiry.
- Nuclear Expansion or Diversified Energy reduces the original +8% civilian energy demand to +6%. Oil Resilience requires its actual prior energy programme and improves the burden to a permanent +3%, rather than erasing exposure.
- The other funded national remedies retain their existing trade-offs. The mixed franc stabilisation spirit retains its 270-day duration.

`starting_spirit_revision.py` defines the four replacement ideas and eight transition effects. The migration maps existing earned receipts to the new ongoing burdens once, including already-completed Oil Resilience. It replays no fees, buildings, research or experience. The native focus guards require the actual source spirit before a new transition executes. `STARTING_SPIRIT_AUDIT.md` records the original routes and net effects; `STARTING_SPIRIT_REVISION.md` records the changed rules.

## Investment instead of repeated productivity rewards

`asset_reward_revision.py` changes 20 domestic focuses. Twenty-two positive productivity/efficiency modifier entries are replaced, mainly with six civilian factories and sixteen offices. The tree now contains 91 one-level building grants, all with one additional shared slot before construction. Every added site uses current owner, control and physical-capacity checks. Setup fees use the paying country's current GDP; all other retained rewards and drawbacks remain explicit.

Positive domestic modifier entry counts change as follows: country productivity growth 2 to 1; civilian factory productivity 7 to 0; office productivity 7 to 2; production efficiency growth 10 to 1. The remaining entries belong to the Sixth Plan, the two financial-policy programmes, and Technical Colleges. The 35 bilateral packages remain unchanged by this asset overlay. This count refers to domestic focus rewards, not all signatories' treaty modifiers.

Previously completed focuses do not replay new finite assets or invoices. A new programme-rebuild version applies current continuing modifiers from earned receipts once. This is a balance update to current programmes, not a retroactive award of the new investment sites. The new asset amounts, GDP shares and state labels were independently reviewed in `ASSET_REWARD_REVIEW.md`.

## Intelligence display

The shared agency repetition sprite declared two frames while the current 1.19.4 game texture is 96 by 32 pixels and contains three 32 by 32 status frames. The wrong slicing can expose fragments of adjacent green/amber symbols. `interface/countryintelligenceagencyview.gfx` now declares three frames. This is shared interface metadata; it changes neither country upgrades nor queue/cost mechanics.

`tools/md_update_203/fix_agency_repetition_frames.py --check` verifies the complete sprite, native texture dimensions, agency references and unchanged GUI geometry. Its repair is idempotent. `INTELLIGENCE_SCREEN_AUDIT.md` records source evidence and limits. Existing game/MD artwork is unchanged; original artists and separate permissions remain unknown where inherited files do not identify them.

## NATO concept only

No NATO membership changes were installed. The proposed approach retains the real `NATO_member` ID and effects, with a French historical presentation or separate command-status indicator. Copying it to a new ID would not satisfy MD's literal membership checks or automatically duplicate membership-array callbacks. Country-context name/description rendering would need a native UI check before adopting that cosmetic approach. Historical reference: [NATO, France and NATO](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/france-and-nato).

## Current verification boundary

The current compiler comparison, scoped source/encoding/reference validator, 96 emitted-AST recovery-state cases plus 96 replay checks, agency frame check, and full browser preview checks pass. Browser checks include all 156 focuses, 35 bilateral inspectors, 42 responsive section views and the changed spirit/asset panels. They reconstruct emitted data and are not native game hovers.

The new isolated native fixture was prepared on E: but was not launched because its safety guard detected an already-running HOI4 process. The earlier 437/437 native result remains historical evidence for the previous build, not a full native certificate for these later changes. Computer Use also reported 'Computer Use was not approved to use hoi4', so the opened game's live intelligence screen and focus hovers were not inspected. No player process or save was stopped or changed. Save/reload and live multiplayer remain untested.
