# UAE 1970 corrections: decisions to retain

These lessons were recorded from Enes's corrections in the UAE / Trucial States conversation on 19 October 2026. They are project guidance, not permission to alter another country's approved mechanics. Current user instructions and the approved design control; recheck version-sensitive source details in the current checkout rather than treating this snapshot as permanent proof. Buggy current output does not override the user's design. The initial North Vietnam mention was explicitly withdrawn.

## Reusable lessons

### Put the historical start in history and follow its consumers

The selection menu, first loaded frame and later tick must agree on country name, leader, portrait, outlook and exact governing subparty. Define the starting government/identity in dated history. A portrait alone does not prove a valid country leader. Trace native leader pools/setters, puppet political matching and cosmetic callbacks when they overwrite that history; do not repair each symptom with another unconditional `on_startup` assignment. If the faulty callback is shared, audit other affected countries with bounded1970 guards and preserve later bookmarks.

Use MD's actual subparty mapping. A pro-Western ruling house is not automatically in the Nationalist outlook: the corrected UAE start uses `Western_Autocracy`, slot0. Its separate `Monarchist`, slot23 alternative is not the historical opening. Do not generalize either mapping to every monarchy.

### Model an announced transition before inventing a request

Research what was already decided at the scenario date. In the approved UAE model Britain's1968 withdrawal announcement is already represented by matching UK/UAE starting spirits. A focus does not need to petition for that existing historical timetable. A new petition may negotiate an earlier handover or alternative terms; rejection does not cancel the existing schedule. Keep the historical treaty-protection relationship distinct from arbitrary later puppeting.

Separate subject cooperation, actual independence and national formation. British liaison/loyal-protection content must work while genuinely subject to Britain. `A Coast in Transition` requires full independence, including from other overlords. The later `Proclaim the Union` focus alone forms/names the United Arab Emirates and creates the federal offices. Reaching a date, ending British protection or acknowledging withdrawal does not silently perform that focus. Native cosmetics must preserve Trucial States until formation.

### A cost is not automatically an availability condition

For newly authored national focuses, follow the user's preference for native MD cost deductions without inventing a Treasury prerequisite. Existing approved funding systems are not automatically rewritten. In UAE the user explicitly removed the check from every focus, including hidden `can_apply` and retry paths; keeping a hidden veto would permit completion without the promised reward. Keep the full native cost and once-only receipt. Confirm what the actual MD treasury provider and existing debt system do with a negative balance instead of inventing a loan mechanic or promising no borrowing. This change did not remove decision funding checks or a foreign recipient's consent/funds contract.

### Prospective reward numbers must remain visible

The reported `Shared Administration` hover displayed a cost and `Modifies ... by:` with no values. Its non-executing preview tested the current treaty status, suppressing all numbers before acceptance. Advertise the prospective native signed rows even while a party/treaty requirement is currently false; enforce real eligibility/consent in actual application and ongoing activation. Use native `TT_IF_THEY_ACCEPT` where terms depend on recipient acceptance. Retain conditional arithmetic for actual marginal caps, already-earned relief and dated appointments. Do not replace missing effects with a paragraph of custom explanation.

Check the full emitted hover structure in eligible and ineligible states, not just whether localisation keys exist. The specific regression must show+8% office productivity and-5% bureaucracy costs before acceptance, while granting neither ongoing contribution until the compact is accepted. A parser/model is not an observed game hover.

### Spirits need lore and the right class of artwork

Describe the country's circumstances, institutions and tensions in English. Do not expose instructions to the player, flags, ownership bookkeeping or implementation notes as national-spirit lore. Put numeric agreement costs/rewards in native event-option effects. For a national spirit, resolve its sprite through to the actual native `gfx/interface/ideas/` texture and inspect it; naming a focus texture `GFX_idea_...` does not make it idea artwork. Inspect semantic suitability as well as file existence. The UAE maritime spirit uses native `GFX_idea_maritime_industry`.

### Give the initial economy a past and make development change it

Do not inherit modern-era resources or buildings merely because the base MD state history has them. A deliberately difficult start still needs historically grounded income sources. Represent UAE fishing, dhow commerce and the legacy of pearling; pearling was already in decline by1970, so this is not a new pearl boom. Trace sector effects into actual GDP/tax/welfare readers rather than inventing a fish resource or unsupported cash tick.

If oil/industrial development displaces traditional livelihoods, recompute only the named legacy sources from earned development receipts. Preserve unrelated commerce/industrial benefits. Use a retained original share, not repeated multiplication of an already-reduced total. Order of investment, later party changes and refresh must not restore the old bonus or replay rewards. Prospective oil rewards must show both the gain and the actual signed loss of existing coastal contributions. Reducing a negative cost modifier towards zero is a positive expense delta.

### Make caps cover the intended whole programme

A request to cap the total tree bonus cannot be satisfied by capping each focus separately. Aggregate compatible contributions into one owned pool, clamp its live value and preview the actual marginal benefit near/at the cap. Check all providers, including alternate paths and abnormal combined receipts. Keep an explicitly tree-scoped cap separate from unrelated native migration, GDP and law systems. A growth modifier is not an immediate population grant.

## UAE-specific accepted balance snapshot

These are approved gameplay values in MD units, not historical construction invoices or universal targets:

- January1970: four base oil, Abu Dhabi3/Dubai1; no starting aluminium/light metals, steel or composite plants in either state. Paid later development must not be erased by repeated initialisation.
- Four oil-capacity focuses cost$0.75/$2.50/$5.00/$8.00bn and add8/10/15/10 base oil. Native costs remain; no focus Treasury prerequisite.
- Starting `Pearls, Fishing and Dhows`: primary productivity+10%, office productivity+3%, social cost multiplier-5%, country productivity-growth modifier-5%.
- `Pearls and Fishing`, $0.10bn: primary productivity+10%, office productivity+6%, social cost multiplier-2% before oil expansion.
- `Fishing Harbours`, $0.15bn: primary productivity+10%, social cost multiplier-3%; harbour construction+15%, bureaucracy cost+3%, energy use+2%. It removes the inherited-5% productivity-growth penalty.
- Every delivered oil phase reduces the original maritime productivity/social relief by20 percentage points of its original share:100/80/60/40/20%. Apply this only to the starting maritime source and those two coastal focuses. Harbour construction/admin/energy, other commerce and the inherited-growth remedy are unscaled. With both coastal focuses, maritime totals go from+30% primary/+9% offices/-10% social to+6%/+1.8%/-2% after all four oil phases.
- `social_cost_multiplier_modifier` affects MD's core population/law-based social bill. It does not reduce a separate flat guest-worker welfare supplement added afterwards. Recheck the live reader before promising an outcome.
- All UAE focus-tree monthly population-growth bonuses share a hard+200% (`2.0`) pool cap. The normal compatible citizen/workforce routes supply+160%/+200%. This cap does not redefine every native demographic modifier.
- The starting scenario retains Sharjah/UAE administration of Abu Musa and Iran's claim; later withdrawal/crisis content is distinct. Verify current province/state geometry before changing it. Optional Iranian operations require player-controlled decisions and real timed native effects, not automatic war/annexation.

## Local evidence to recheck

Resolve the live workspace first; these are source pointers, not permanent proof:

- `tools/uae_1970/revision.py`, `development.py`, `compile.py`, `presentation.py`, `maritime.py`, `politics.py`, `economy_start.py`, `flavour.py`.
- `test_revision.py` for direct/transitive focus gates; `test_maritime.py` and `test_presentation.py` for decline, order, signed previews and caps; `test_politics.py` for start/callback identity; diplomacy tests for unchanged recipient contracts.
- `docs/audits/COLDWAR_UAE_MARITIME_OIL_REVIEW.md` and `docs/design/uae_1970/installed/` for independent source/visual evidence. An older report may describe superseded affordability or unscaled bonuses; check its revision notice.

The recorded checks establish source/model consistency. Live HOI4 load, hover, save and multiplayer behavior were not established by those checks.
