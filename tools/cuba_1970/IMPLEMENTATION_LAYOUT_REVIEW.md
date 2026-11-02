IMPERIA COLD WAR

# Cuba 1970 implementation and layout review

Status: the latest emitted focus tree passes 5,571 independent core checks and the bilateral package passes 1,364 checks. The closure audit finds 198 custom Cuba `has_completed_focus` references across loaded providers, all resolving to current focus IDs. The fresh two-profile native probe is pending, so this is not final engine signoff. No runtime or generator file was edited for this review.

## Approved graph and geometry

The immutable original design is pinned at SHA-256 `89a94cf53ea67e9183a0bd5e19e139e89d7664b0b6740893b2423a18a43d96d6`; the approved foreign redesign is pinned at `338a9d911ffd8ce1c01269d33a4087efbfa1989a60755690057696dc60699b7b`. The emitted tree contains all 120 approved focuses, including 25 foreign-policy focuses, 21 partner agreements and the unchanged 13-focus PCC/Fidel branch. The design records 11 merge actions releasing 12 focus slots. The foreign expansion uses those slots without removing the political alternatives.

The independent AST comparison resolves every focus ID, local coordinate, relative anchor, prerequisite group, duration, reward preview and reciprocal mutual-exclusion pair against the approved design. It finds 118 prerequisite edges and 27 reciprocal exclusive pairs. All 120 resolved positions are unique. The full tree occupies x=0..62 and y=0..24 on the native 96 by 130 pixel grid. The foreign subtree occupies x=34..62 and y=0..9, with Island Diplomacy at (48,0). Parallel contract tracks use four-cell horizontal spacing; this gives 384 pixels between card centers and a 219 pixel gap between 165 pixel cards. The longest approved focus title is 143 pixels, inside the native 147 pixel title field.

The close foreign and mission previews are legible and show no clipped labels or overlapping cards. The full-tree preview is intentionally at 15 percent and works as an overview rather than a reading view. Browser validation covers all 120 focus selections across 320, 736 and 1024 pixel viewport widths, with zoom and pan checks. The preview connector routing is orthogonal, but it is a concept renderer, so it cannot certify the final connector path drawn by HOI4 itself.

## Foreign-policy presentation

Partnered focuses keep the offers on the Cuban tree. Completing a Cuban offer focus issues a proposal to the named counterpart, where that country receives the acceptance and refusal decisions. The focus tooltip previews both countries' named spirits, every signed modifier, both setup costs and any one-time accepted term. For example, Soviet Assistance shows Technical Cooperation for Cuba and Cuban Technical Cooperation for the Soviet Union, Cuban setup cost -0.10 billion, Soviet setup cost -0.30 billion, and the two countries' modifier rows. Soviet Industrial Credits includes its Camagüey factory and the extra state building slot in the focus preview. Cayo Blanco Agreement previews the transfer of State 1252 to DDR and Cuba's retained core, as well as both payments and spirits.

The English focus descriptions use institutional and diplomatic language. They describe the policy bargain and historical context without exposing receipt flags, helper names, expiry implementation or other code workflow. The preview's concise “If they accept” heading introduces native effect rows rather than replacing them with prose. The cancellation, refusal, expiry and replay rules are enforced in the decisions and effects; they are not presented as effect-summary paragraphs.

This follows the source presentation patterns without copying their narrower mechanics. MD's `SOV_expand_trade_with_taiwan` in `05_russia.txt` at line 20577 combines a partner-specific availability check, reciprocal relations and influence, and a targeted decision unlock. Native Cuba's `CUB_coop_usa` at line 256 uses a visible party requirement and a mutual-exclusion pair, while `CUB_revolutionary_army` at line 318 joins either prior route. The new Cuba tree applies those patterns to recipient-approved treaties: partner-specific guards, separate recipient decisions, and genuine local exclusivity while allowing unrelated trade agreements to coexist.

## Agreement scope and lifecycle

The emitted offer effects run as Cuba and recheck the Cuban focus receipt, counterpart existence, matching pending/open/signature state, the bilateral peace condition and any deal-specific conditions before opening a 90-day offer. The recipient decisions verify the acting country and active proposal, then recheck Cuba's open proposal and relevant conditions. Signing stamps both countries' signature receipts and charges each setup cost once. One-time transfers, research, compensation, buildings and experience have durable grant receipts. Refusal and expiry clear the pending proposal without charge; reopening does not reopen a signed deal; termination clears the paired signatures without clearing the paid receipts.

Paired agreement spirits activate only when both signatures remain and both countries satisfy the peace, embargo and bilateral-sanctions checks. Signing is not blocked merely because sanctions remain, which allows the agreement to be signed while its benefits are suspended. Acceptance previews use display-only native effect tooltips; the actual charges and grants remain in the hidden effect. The 1,364-check validator confirms these actor scopes, costs, receipts, paired spirit values, sanction directions, recalculation calls, event references and English localization.

## Corrected integration details

The emitted Ethiopian eligibility guard, offer issuance, acceptance and reopening now use the exact native party predicates `emerging_communist_state_are_in_power`, `neutrality_neutral_communism_are_in_power` and `nationalist_military_junta_are_in_power` within ETH scope. The bilateral validator checks this at each provider. The all-provider closure check covers retained diplomacy/bilateral providers and decision visibility; it returns zero dangling custom focus references after removed-focus checks were converted to durable applied receipts.

The LIMITED agreement preview now shows the full American embargo spirit removed and the limited spirit added. Acceptance stamps the limited-easing receipt and calls the shared reconciler. Full settlement previews and removes both embargo spirits; acceptance stamps final settlement, clears limited easing and calls the reconciler. The reconciler restores only the intended burden for each status. The core validator also verifies each infrastructure grant's actual state-level `building_level@infrastructure < 6` gate, and confirms that the reward still adds one shared building slot before construction.

All 41 newly defined paired agreement spirits also cancel if either signatory no longer exists. This prevents a surviving partner spirit from applying modifiers after annexation; the validator requires the paired-signatory existence test on both the Cuban and counterpart spirit definitions.

## Evidence

- Approved graph and visual checks: `docs/design/cuba_foreign_1970/FOREIGN_POLICY_CONCEPT.json`, `VALIDATION.json`, `BROWSER_VALIDATION.json`, `PREVIEW_foreign.png`, `PREVIEW_missions.png` and `PREVIEW_context.png`.
- Emitted focus and script checks: `tools/cuba_1970/IMPLEMENTATION_VALIDATION.json` and `tools/cuba_1970/BILATERAL_VALIDATION.json`.
- Native source references: MD `05_russia.txt` line 20577 and `05_cuba.txt` lines 256 and 318.

## Final runtime verification

The installed 41 runtime/shared file hashes match `ENGINE_FOREIGN_BUILD_MANIFEST.json` after an identical repeat build. `FOREIGN_IMPLEMENTATION_VERIFICATION.json` records 209 executed and passed native assertions, the four embargo skips, the private 1972 scenario-routing override and verification of the 92-file backup. The 1970 sanction and war fixtures invoke the installed full daily-update helper. The native volunteer-modifier reader is tested directly.
