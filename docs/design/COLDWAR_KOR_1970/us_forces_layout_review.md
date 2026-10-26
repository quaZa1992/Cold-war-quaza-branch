# South Korean USFK branch — revised layout review

## Scope and layout basis

Read-only structural proposal for the 298-focus, 14-group 1970 KOR concept, updated for the explicitly authorized branch reorganization. Reviewed the canonical design JSON and current defence/foreign layouts. Coordinates below are absolute native-grid cells on the project's measured 96×130 pitch and 165×128 card bounds. Keep every existing ID; add exactly two new IDs, for a final total of 300. Keep the current eight shortcuts.

The current design has two explicit US-facing focuses, `COLDWAR_KOR_alliance_bargain` and `COLDWAR_KOR_burden_sharing`. The proposal moves those and seven compatible existing focuses into an actual USFK programme, with bilateral exercises and alternative policy tracks. The moved readiness/materials focuses should be rewritten as mutually agreed US–ROK policy as needed; do not imply a focus can directly order a US deployment. Keep any real US force commitment behind the bilateral agreement/consent system.

## Compact programme footprint

Place the programme directly below the foreign-policy section in a clear 3-column footprint, x=62..64/y=15..21. It is below `public_treaty_process` at (63,13), and no current foreign card occupies y=14..21. The nearest KJP cells are x=53..55/y=20..27; at least seven grid columns separate their centers from this programme, so there is no card collision or connector crossing into KJP.

| Focus | Proposed absolute cell | Proposed role and prerequisite repair |
|---|---:|---|
| `COLDWAR_KOR_usfk_presence` (new) | (63,15) | Programme entry/root; do not draw a long connector back through the foreign section. Make alliance eligibility a real availability guard if required. |
| `COLDWAR_KOR_alliance_bargain` | (62,16) | Renew the alliance / request continued presence; prerequisite becomes the new root. Preserve its existing contract dispatch and consent lifecycle. |
| `COLDWAR_KOR_strategic_autonomy` | (64,16) | Negotiate a drawdown / greater autonomy; prerequisite becomes the new root. Preserve the ID and existing alternative relationship with Alliance Bargain. |
| `COLDWAR_KOR_burden_sharing` | (62,17) | Agreed host-nation support; keep under Alliance Bargain. |
| `COLDWAR_KOR_diverse_partners` | (64,17) | Broaden security partnerships; keep under Strategic Autonomy. |
| `COLDWAR_KOR_allied_procurement` | (62,18) | Alliance-standard facilities/equipment option; prerequisite can be either burden-sharing or diverse partners (one OR group). |
| `COLDWAR_KOR_domestic_defence_industry` | (64,18) | Domestic investment alternative; use the same OR prerequisite and retain its existing reciprocal exclusion with Allied Procurement. |
| `COLDWAR_KOR_licensed_maintenance` | (62,19) | Sustain imported systems; keep under Allied Procurement. |
| `COLDWAR_KOR_changwon_production` | (64,19) | Domestic sustainment/production; keep under Domestic Defence Industry. |
| `COLDWAR_KOR_rok_us_combined_exercises` (new) | (63,20) | Bilateral exercise programme; prerequisite may be either maintenance/production path, since both are beneath the procurement choice. |
| `COLDWAR_KOR_joint_readiness_audits` | (63,21) | Final mutual readiness review; redirect its current three defence-training prerequisites to the new Combined Exercises focus. Reframe the audit as reciprocal ROK–US planning. |

The existing first choice already has reciprocal exclusion between Alliance Bargain and Strategic Autonomy. Retain it. Allied Procurement and Domestic Defence Industry are also an existing reciprocal choice; retain it. Burden Sharing and Diverse Partners are not presently mutually exclusive: leave that relationship unchanged unless the content owner wants a second hard choice. The later procurement pair is reachable from either policy, so the tree does not force one burden-sharing strategy.

This layout has a root, a diplomatic commitment choice, a host-support/partner branch, a concrete alliance-systems versus domestic-investment choice, sustainment, exercises, and an audit. The new focus IDs are the only new nodes; no focus is deleted or duplicated.

## Dependency changes to preserve both host branches

1. Reparent Alliance Bargain and Strategic Autonomy from `COLDWAR_KOR_diplomatic_review` to the new USFK root. This makes the lower cluster locally connected and avoids diagonal lines through the existing foreign-policy cards.
2. Preserve the current edges from Alliance Bargain to Burden Sharing and from Strategic Autonomy to Diverse Partners.
3. Reparent Allied Procurement and Domestic Defence Industry from `COLDWAR_KOR_defence_logistics` to one OR prerequisite group containing Burden Sharing and Diverse Partners. Their existing reciprocal exclusion remains the visible policy choice.
4. Preserve Allied Procurement → Licensed Maintenance and Domestic Defence Industry → Changwon Production. The moved pair no longer feeds the old local Defence Quality focus.
5. Redirect `COLDWAR_KOR_joint_readiness_audits` from Aircrew Training / Escort Staff / Fire Direction to the new Combined Exercises focus. Those three existing ROK training focuses remain in the national-defence section as meaningful terminal specializations.
6. Preserve all other defence prerequisite edges and the complete national-defence spine. Specifically, keep the original Defence Quality node at (54,6) and reparent it locally to `COLDWAR_KOR_defence_logistics` (or another existing local defence prerequisite) because its two procurement parents have moved. It continues to unlock Reserve Army / Professional Core, Civil Defence Training / Career NCO Corps, Joint Staff, service priorities, and the Yulgok follow-up. This avoids a long connector back from the new USFK programme into the old defence section.
7. The moved Burden Sharing and Diverse Partners nodes currently feed Vietnam Legacy. To keep the foreign branch local and reachable, reparent `COLDWAR_KOR_vietnam_legacy` to `COLDWAR_KOR_diplomatic_review`. It remains at (63,3), followed by the complete Japan/market/overseas-contract chain. Its content concerns the legacy deployment and veterans' obligations, which can be handled independently of the new USFK agreement. Do not leave a connector from the moved lower nodes back to Vietnam Legacy.

The relocated procurement/sustainment identities belong to the USFK programme, while the local Defence Quality focus becomes a national industrial/readiness audit with a local prerequisite. Parent implementation should update reward semantics to match those revised institutional roles, preserve costs/receipts, and maintain independent native guards.

## Geometry, caps, and verification notes

- New cluster bounds: x=62..64, y=15..21. All cells unique.
- The nearest existing foreign card is at (63,13); the cluster begins two rows below it. Its vertical spine and paired choice rows use native-spacing-compatible cells.
- Nearest KJP cards are at x=53..55, y=20..27; the seven-column-or-greater center separation prevents item-box overlap and connector intersection.
- Existing focuses preserved: 298/298. New focuses: 2. Final total: exactly 300.
- Existing shortcuts preserved: 8/8.
- Main defence programme remains in its original defence area; only the US-cooperation equipment options and final readiness audit move. Redirecting Defence Quality locally prevents the moved equipment branch from cutting across the national-defence spine.
- Browser connectors remain an approximation. Verify actual Clausewitz connector routing, agreement/consent conditions, reachability, and effect meaning in game after implementation.

