IMPERIA COLD WAR

# France 1970 starting-spirit recovery revision

## Scope

This revision stages three remedies that were previously immediate or complete at their first terminal focus. It leaves the other five permanent starting spirits, the 270-day franc spirit, the focus count, and all focus costs and rewards unchanged. The approved design JSON remains immutable. `starting_spirit_revision.py` returns a deep-copied overlay for the runtime compiler.

## Recovery paths

| Existing path | First transition | Later state |
|---|---|---|
| `executive` or `parliament` | Replaces The Fifth Republic with **Unsettled Institutional Balance**: stability -2%, bureaucracy cost +4%. The starting political-power +10% ends. Existing focus rewards remain unchanged. | **Civic Settlement** removes the residual at the end of its funded housing and reconciliation path. Its description now includes rebuilding trust in constitutional institutions. |
| `technical_colleges` or `mass_universities` | Replaces A Narrow Route to Expertise with permanent **Higher Education Expansion Pressures**: education cost +4%, factory efficiency growth -1%. | No timed expiry or extra follow-up. Existing focus rewards remain unchanged. |
| `nuclear_scale` or `diverse_energy` | Replaces Oil-Intensive Growth (+8% civilian energy use) with **Reduced but Persistent Oil Dependence** (+6%). | The existing guarded `oil_resilience` focus replaces it with permanent **Persistent Oil Dependence** (+3%). The actual reactor or funded-diversification condition is unchanged. |

These are persistent national ideas, not party programme modifiers. A party change cannot suspend or replay them. Scripted transitions check that the source idea is present; each focus retains its existing earned-focus guard. Native `swap_ideas` effects appear in the focus effect preview. No new fee, wait, focus, asset, research, experience, opinion or decision is introduced.

## Existing-save reconciliation

A new one-time migration flag, `COLDWAR_FRA2_starting_spirit_revision_20261029_migrated`, is separate from the retained focus-earned receipts and the existing party-revision migration. It runs only for FRA in the 1970 scenario and changes ideas only.

- An earned `executive` or `parliament` receipt adds Unsettled Institutional Balance if `civic_settlement` has not been earned. An earned Civic Settlement remains fully resolved.
- An earned Technical Colleges or Mass Universities receipt adds Higher Education Expansion Pressures once.
- Earned Nuclear Expansion or Diversified Energy without an earned Oil Resilience receipt maps the old oil spirit to the +6% intermediate stage.
- An earned Oil Resilience receipt maps the old cleared result to the new +3% residual once. The old focus receipt remains intact; no GDP, building, research, experience, opinion or other focus reward is replayed.

The migration does not add any stage idea to a save without the corresponding earned receipt. Repeated sync calls are blocked by the migration flag. New post-revision oil transitions also write `COLDWAR_FRA2_recovery_applied_<focus>` receipts, separate from the legacy `COLDWAR_FRA2_earned_<focus>` receipts.

## Historical framing

The institutional path treats the balance of presidential and parliamentary authority as a continuing political settlement. The 1962 referendum established direct presidential election and faced opposition from most parliamentarians; [Vie publique's constitutional history](https://www.vie-publique.fr/fiches/38016-la-revision-constitutionnelle-et-le-referendum-de-1962) supports that institutional tension. The numbers above are game-balance proposals, not historical measurements.

The education and oil ideas represent adjustment costs and enduring import exposure after policy investment; their exact percentages are balance choices. The proposal does not claim that historical France faced these exact costs or that its actual nuclear programme eliminated dependence on petroleum.

## Source and verification limits

- `runtime_design.json` supplies the original spirits, focus routes, native guards and unchanged rewards.
- `starting_spirit_revision.py` provides the reviewable overlay; `core.py` emits stage ideas, transitions and migration source text.
- This report records source-level design and migration semantics only. The root-owned compiler and native fixture are still required to verify the composed output; no live-game test is claimed here.
