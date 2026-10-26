# USA: Bahrain Naval Base

Implemented 18 October 2026 for the 1970 scenario.

- One 35-day focus, `COLDWAR_USA_bahrain_base_request`, at (18, 5) in `common/national_focus/USA_1970.txt`.
- Requires any one of the existing three Middle East policy focuses, F7/F8/F9. Their mutually exclusive choices and all existing rewards are unchanged.
- The USA sends a proposal to Bahrain. The focus itself does not transfer territory.
- Bahrain's human player chooses; an AI Bahrain uses relative acceptance/refusal weights 65/35, adjusted by its opinion of the USA and common faction membership.
- Acceptance transfers ownership of **state 624 only** to the USA. This is a state cession using MD's `transfer_state`, not merely military access or a cosmetic lease. Bahrain's remaining territory and existing cores are not altered by this code.
- Refusal leaves the territory unchanged and adds **-25 US opinion of Bahrain for 730 days**. It does not add a reciprocal Bahraini opinion penalty.
- Both answers send an English notification to the USA. If the proposal becomes invalid, talks close without a transfer or refusal penalty.

## Guards and integration

Only the actual USA and BHR tags participate. Both countries track this offer separately from other diplomatic systems. Acceptance and refusal recheck current flags, ownership, full control and peace between the parties when applying the answer. Duplicate request calls do not replace an open or resolved offer. Delayed/duplicate responses cannot grant the territory a second time.

The native `GCC_expel_us_interests` focus and the existing USA-collapse event can subsequently return state 624 to Bahrain; those existing routes are preserved. There is no periodic ownership enforcement, automatic acceptance, new fee, recurring payment or separate diplomatic menu.

The USA tree header names `tools/generate_usa_1970_focus_tree.py`, but that generator is absent from this checkout. The new focus is explicitly marked as an authored extension in the installed file. Any external future generator must retain this addition. The previous tree can be reconstructed byte-for-byte by removing the added focus block.

## Files

- `common/national_focus/USA_1970.txt`
- `common/scripted_triggers/COLDWAR_USA_bahrain_base_triggers.txt`
- `common/scripted_effects/COLDWAR_USA_bahrain_base_effects.txt`
- `events/COLDWAR_USA_bahrain_base_events.txt`
- `common/opinion_modifiers/COLDWAR_USA_bahrain_base_opinion.txt`
- `localisation/english/COLDWAR_USA_bahrain_base_l_english.yml`

## Verification and limits

Independent source review covered scopes, recipient consent, event/localisation/art references, state transfer, opinion direction, pending flags and invalid-response handling. A strict focused AST model passed nine transaction cases: acceptance, refusal, changed owner, changed controller, war, repeated acceptance, repeated request, missing Bahrain and missing USA. The model does not establish engine `FROM` binding, event timing or actual state/core behavior.

The installed tree has 214 unique focus IDs and coordinate pairs. The new title measures 113 pixels in the actual `hoi_16mbs` font, within the native 147-pixel title field. Full-tree and branch previews use installed coordinates, native icons and font; they were independently inspected without visible overlap. Reconstructed connectors are approximate. No live HOI4 test was performed.

Native reference patterns: current MD and Cold War USA diplomacy events for recipient-owned offers and reply notifications; `COLDWAR_SOV_offer_soyuz_pipeline` for country-event sender/recipient scopes; MD `transfer_state` for state cession; timed opinion entries in `common/opinion_modifiers/China.txt`; focus spacing and title dimensions in `interface/nationalfocusview.gui`.
