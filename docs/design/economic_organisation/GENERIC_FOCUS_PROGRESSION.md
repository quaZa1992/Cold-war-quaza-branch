IMPERIA COLD WAR: Generic focus economic organisation progression

30 October 2026. The user requested that the generic tree's existing economic paths progressively change the actual Planned Economy / Market Economy system. This integration uses `icw_econ_position`, its existing -100/+100 limits, seven institutional tiers, national spirits and GUI marker. It does not add another slider, decision menu or recurring scan. Existing focus rewards, prerequisites, costs, coordinates, exclusions and availability remain intact.

## Focus steps

| Path | Focus | Change |
|---|---|---:|
| Market | Market Liberalisation | +10 |
| Market | Attract Foreign Investors | +5 |
| Market | Open the Stock Exchange | +10 |
| Market | Simplify the Tax Code | +5 |
| Market | Export Processing Zones | +10 |
| Market | Economic Miracle | +10 |
| Mixed | The Mixed Economy | Up to 20 towards zero |
| Mixed | Indicative Planning | Up to 20 towards zero |
| Mixed | National Champions | Up to 20 towards zero |
| Mixed | Social Partnership | Up to 20 towards zero |
| Mixed | Pension Fund Investments | Up to 20 towards zero |
| Mixed | Planned Prosperity | Up to 20 towards zero |
| Planning | Central Planning | -10 |
| Planning | Nationalise Key Industries | -15 |
| Planning | State Planning Committee | -10 |
| Planning | Collectivise Agriculture | -10 |
| Planning | Socialist Industrialisation | -15 |

These are balance choices using the existing system's manual 5/10/15-point reforms as the numerical reference (`tools/economic_organisation/catalogue.py`, `REFORMS`). The market programme totals +50 and the planning programme -60 before endpoint clamps. Five required mixed-economy focuses can bring either endpoint to zero, with an optional sixth step stopping at zero. The mixed route moves in either direction and never crosses its target. Common debt relief and agricultural development remain neutral: those policies do not inherently determine the ownership and coordination model of the entire economy. No historical claim or new policy narrative is introduced by these numerical links.

## Integration and boundaries

`tools/economic_organisation/focus_integration.py` owns the focus mapping, a source-preserving idempotent patch and two emitted providers. The current loaded tree is patched directly. The canonical generic generator calls the same patch and emits the same providers; the missing older base generator mentioned in the inherited file header is not recreated or run. No broad tree rebuild is performed.

Each completion shows its actual signed, capped `Economic Organisation` change through the native variable-effect numeric formatter. The existing tier, spirit, marker, globalisation equilibrium and economic readers refresh immediately. Each focus's new movement has its own one-time receipt. Loading an existing save does not retroactively reapply previously completed focuses.

An active timed reform keeps its duration and relative movement. Its queued target is rebased by the actual focus change and clamped. Market high-water marks prevent focus progress from being sold again after a reversal. Focus progress itself grants no sale money. Pending privatisation proceeds can only retain or decrease their frozen original quote in proportion to still-unsold points; they are never repriced upward using later GDP. A pending overlord offer invalidated by the new economic position is cleared, not automatically accepted. Existing manual-reform consent and cooldown rules are unchanged. Domestic focus availability is unchanged.

## Verification

`python tools/economic_organisation/test_focus_integration.py` exercises all 17 focus steps at every integer position, all three complete programmes, near-zero mixed movement, repeated invocation, uninitialised countries, concurrent reforms, capped/frozen privatisation proceeds, repeat-sale prevention and stale subject offers. It evaluates the emitted scripts through the existing strict economic-system model. These source/model checks do not establish live engine rendering, a game save/reload or live multiplayer behaviour. No computer-use actions or game launch are part of this change.
