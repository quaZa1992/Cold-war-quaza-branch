# IMPERIA COLD WAR

## Independent intervention graph and actor layout review

Read-only review of the current generated `concept.json`, `tools/cyprus_1970_concept/intervention.py`, and `preview.html`. No source or runtime edits made. Layout observations refer to the concept preview, not native focus-tree coordinates in a live game.

### Layout

- **Greece response fork: well centered and separated.** In `intervention.py:59-74`, `gre_response` is at `(5,4)` and its exclusive children `gre_volunteers` and `gre_escalate` are at `(2,5)` and `(8,5)`. The child midpoint is x=5, directly under the root. `preview.html:67` renders these as a vertical focus prerequisite connector and a horizontal dashed exclusive pair. At the current 146 px card width, the 145 px row spacing leaves 50 px between card bounds. The earlier Greek module ends at y=2, so y=4 leaves an empty row at y=3; this is visually clear separation, though the final native attachment must reserve that vertical footprint.
- **Turkey fork: correct three-way layout.** The `tur_consult` root is `(4,0)`; `tur_terms`, `tur_operation`, and `tur_abstain` are `(0,1)`, `(4,1)`, and `(8,1)` in `intervention.py:33-56`. All three are children of the root and pairwise exclusive. The middle operation sits directly below the root, with negotiation and refusal on either side. No actor-preview coordinate collision is apparent.
- **Greece response root needs a hard runtime availability gate.** It has no focus prerequisite (`pre=[]`, line 60); its displayed requirement says an actual Turkey-Cyprus war is active. Ensure native focus availability checks the real current CYP-TUR war and country survival/independence. A description or graph edge alone does not prevent a player from taking it early.

### Former blocking graph defect: resolved in regenerated data

The prior version gave the combined `intervention` node outgoing edges to both `greek_choice` and `army_warning`, and gave `civilian_control` a direct edge to `greek_choice`. Those links have been corrected.

- `intervention.py:152` now branches to `turkish_operation` or `army_warning`.
- `late_intervention` also points to the shared `turkish_operation` outcome. That outcome alone points to `greek_choice` (`:162-166`).
- `civilian_control` is now terminal with `next=[]` and explicitly says it closes the coup chain without war (`:158-159`).
- The Greek response and direct-war focus now declare native availability requirements for existing CYP/TUR, active TUR-CYP war, and the current intervention receipt (`:179-186`). The response remains a visual root with no focus prerequisite, so that runtime availability check is essential.
- I checked current `concept.json`: every crisis node appears once in `crisis_layers`; no duplicate or omitted keys were found. The updated layers place the Turkish operation outcome before the Greek choice.

The generic renderer still draws each listed `next` edge as a plain arrow (`preview.html:70`). With explicit outcome nodes and the conditional text, the remaining arrows represent available branches and no longer imply Greek support after a no-war civilian-control result.

### Other graph/API notes

- `crisis_layers` now includes `turkish_operation` and `late_intervention` once each (`intervention.py:175-177`). The earlier concern that the actual-operation outcome was missing from the layout is resolved.
- Preserve the once-per-crisis receipt across the Turkish operation focus and the separate crisis `intervene` decision. Both presently advertise the same operation and bonus; without one shared runtime receipt, a refusal followed by a later authorization could duplicate the setup payment, war declaration, or refresh the 180-day bonus. The concept says the receipt is one-time and reversals cannot refresh it (`intervention.py:44-46`, `:99-104`), so implementation should share that guard.
- Turkish operation bonuses currently read Navy organization +15%, naval invasion preparation +50%, amphibious invasion attack +15%, planning speed +30%, and maximum planning +20% for 180 days (`intervention.py:5-7`, `:37-46`). The preview makes these legible as meaningful benefits; they must remain conditional on actual intervention, end at related peace or 180 days, and not recur if the crisis path changes.

## Disposition

The former concrete graph defect is resolved in the current data: only the actual Turkish operation outcome leads to the Greek choice, and civilian control ends without war. Actor coordinates remain internally coherent. No remaining concrete graph defect was found in this read-only recheck. Native attachment, native title wrapping, live focus availability, and rendered-browser appearance have not been verified in-game; the new native availability fields and shared receipt still need correct implementation.
