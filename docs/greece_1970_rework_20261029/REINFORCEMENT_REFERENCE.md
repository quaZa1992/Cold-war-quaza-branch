IMPERIA COLD WAR

# Greek reinforcements for Cyprus: native mechanics reference

Read-only source audit for a proposed Greek focus that supplies Cyprus with two real infantry divisions. No runtime or history files were changed.

## 1970 force and template baseline

- Greece and Cyprus both load `mdcw_1970_empty_land` in the 1970 setup. The OOB is explicitly `units = { }`; the country histories also say starting armies and equipment are deferred. See `history/countries/GRE - Greece.txt:39-59`, `history/countries/CYP - Cyprus.txt:44-62`, and `history/units/mdcw_1970_empty_land.txt:1-3`. Neither country has a ready 1970 division template in its start OOB.
- The shared 1970 infantry research helper gives both tags the 1940 infantry, CNC, light anti-tank, and anti-air profiles. GRE and CYP profile definitions are `common/scripted_effects/mdcw_1970_infantry_research_effects.txt:2242-2267,3736-3761`; the date-gated dispatcher is at `:11347-11455`. Anti-air uses `mdcw_nsb_anti_air_1940` with No Step Back, otherwise `mdcw_anti_air_1940`.
- A valid light-infantry line battalion exists: `L_Inf_Bat` is active, 3 combat width, 200 manpower, and needs 200 `infantry_weapons_type`, 20 `L_AT_Equipment`, 20 `AA_Equipment`, and 20 `cnc_equipment_type` (`common/units/MD_land_units.txt:179-219`).
- The corresponding 1970 model family includes `mdcw_infantry_weapons_1940` (`common/units/equipment/MD_infantry_equipment.txt:48`), `mdcw_anti_tank_1940` (`.../MD_anti_tank.txt:50`), `mdcw_anti_air_1940` (`.../MD_anti_air.txt:46`), and `mdcw_cnc_equipment_1940` (`.../MD_electronic_equipment.txt:40`). These are the equipment-family members behind the archetype needs above; the battalion template should price the archetypes in the table, not an additional model copy.

For a compact custom 1970 template, use six `L_Inf_Bat` line battalions and no support companies per division. That is 18 width and 1,200 manpower per division. Two divisions require exactly:

| Resource | Per division | Two divisions |
|---|---:|---:|
| Manpower | 1,200 | 2,400 |
| Infantry weapons (`infantry_weapons_type`) | 1,200 | 2,400 |
| Light anti-tank (`L_AT_Equipment`) | 120 | 240 |
| Anti-air (`AA_Equipment`) | 120 | 240 |
| CNC equipment (`cnc_equipment_type`) | 120 | 240 |

These figures are the exact template needs for full strength, before any reinforcement buffer. Do not add artillery, trucks, or support equipment to the displayed cost unless those battalions or companies are actually added to the template.

## Native effects and routing

- `division_template = { ... }` defines a template in the current country; `create_unit` creates divisions in a state scope and supports `owner`, `prioritize_location`, and `count`. The installed game effect reference is `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/effects_documentation.md:3278-3310`; local MD examples are `events/Abkhazia.txt:37-50`, `events/05_armenia.txt:6965-6985`, and `events/00_arab_spring.txt:399-457`.
- Scope the template and unit creation through Cyprus so Cyprus owns the new units and template. Cyprus controls both 1970 states 145 and 146; state 145 contains Nicosia province 11984, and state 146 contains Famagusta province 7193 (`history/states/145-Cyprus.txt:38-53`, `history/states/146-Northern Cyprus.txt:35-52`). A state-scope spawn in either location works before a war when CYP still owns and controls the state. Existing MD uses `random_owned_controlled_state` plus a full-control guard (`events/05_armenia.txt:6975-6985`). Do not spawn in British state 812.
- `send_equipment` transfers a quantity from the current country stockpile to a target and removes it from the source. Native documentation is `.../documentation/effects_documentation.md:6550-6557`; MD uses it with `type = infantry_weapons_type` and a target in `events/05_bulgaria.txt:276-292`. Generic archetype types cover current models. By contrast, `add_equipment_to_stockpile` with a negative amount removes stock from the current country (`.../documentation/effects_documentation.md:1252-1266`); do not both send a full package and separately debit the same full package.
- `add_manpower` accepts a negative value; MD examples include `events/00_arab_spring.txt:210,237,261`, and the installed effect documentation defines country and state scopes at `.../documentation/effects_documentation.md:1468-1473`. Guard the exact `GRE` reserve before subtracting 2,400.

## Transaction recommendation and limits

For a one-focus immediate spawn, use one guarded, one-time transaction: validate Greece has at least 2,400 manpower and the four equipment quantities above; validate Cyprus exists and still owns and controls a spawn state; define the template in CYP scope; then debit the Greek manpower and equipment exactly once and create two CYP-owned units in state 145 or 146. Keep the existing volunteer and direct-war focuses separate. The reinforcement receipt must prevent repeat claims.

There is no direct troop-transfer effect in this source set. `transfer_troops = yes` appears as an `annex_country` option (`events/00_arab_spring.txt:420`), which is not suitable for this sovereign aid offer. More importantly, the native `create_unit` documentation describes OOB-style unit creation but does not specify whether the unit's `start_equipment_factor` consumes the current stockpile. Mod examples also create units with a start equipment factor independently of `send_equipment`. Therefore, static source inspection cannot certify that sending equipment to Cyprus and then using `create_unit` avoids duplicate weapons. Use one accounting model only: either debit the Greek stockpile as the cost for the generated CYP units, or transfer stock to Cyprus and let its normal deployment/recruitment consume that stock. Confirm any direct create-and-transfer combination in the live engine before claiming exact physical transfer.

The 1970 histories contain no `add_equipment_to_stockpile` setup for GRE or CYP, and both initial land OOBs are empty. Research unlocks equipment types but does not create inventory. Thus the proposed focus can be immediately available only if Greece has a sufficient actual reserve from another startup source; none was found in the audited Greek/Cypriot history files. Otherwise gate it until Greece has produced or acquired the exact quantities. A reserve-only startup grant could make the focus immediately usable without activating starting armies, but would need explicit design approval and should be accounted for as a separate initial grant.

## Final concept data check

The generated Greek concept contains 100 focuses, with 14 in its Cyprus group. `reinforce_guard` is a 7-day focus with no predecessor or exclusion; the volunteer and direct-entry routes remain mutually exclusive with each other and independent of this focus. Its recipient offer is explicitly a one-time `unit_transfer` to CYP. The offer displays Greece's complete manpower and equipment debit and Cyprus's two full-strength divisions in the focus preview. The standalone preview renderer handles the `units` effect and routes the embedded offer through the same two-sided agreement renderer.

The offer's four equipment archetypes and 2,400 manpower match the two six-battalion templates. It requires the real Greek reserves and a CYP-owned, CYP-controlled deployment state, preferring provinces 11984 and 7193 in states 145 and 146. It rejects British state 812, checks consent and conditions again at acceptance, and says to abort before charging if no valid spawn location remains. This is a one-off transfer with no standing spirit or recurring polling.

The native source documentation verifies template/unit creation and stockpile debit effects, but does not establish that generated units can be supplied from a different country's stock without changing CYP stockpile, nor that creation preserves the donated model tiers. The documented `create_unit` interface accepts a division template and start factors; it does not expose a donor-country equipment parameter. The offer therefore still needs an engine fixture that proves the Greek equipment debit materially supplies the two units, as well as GRE's exact losses, CYP's unchanged free manpower and stockpile, full unit strength, and the intended model tiers. Merely observing both a Greek debit and two equipped CYP units would not prove physical conservation if the units draw from Cyprus or receive equipment through an implicit start factor. The explicit debit plus CYP unit generation avoids an intentional second `send_equipment` transfer, but do not claim actual equipment provenance, model-tier preservation, or stock conservation until the fixture demonstrates all three.
