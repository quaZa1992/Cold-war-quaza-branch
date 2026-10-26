# Spanish Sahara: January 1970 ownership and local unrest

<!-- IMPERIA CW — Cold War: historical basis and state modifier balance. -->

Spain administered the whole territory of Spanish Sahara in January 1970. The modern MD division between Tifariti (372) and Western Sahara (373) does not represent a Spanish–Moroccan administrative division in 1970. Both states therefore start owned and controlled by SPR, with the existing SHA cores retained. Spain receives no cores. Morocco retains a territorial claim rather than a core in the 1970 snapshot. This is a scenario representation of contested sovereignty, not a statement that Spain possessed internationally recognised sovereignty over the territory.

Primary sources:

- [UN General Assembly resolution 2711 (XXV), 14 December 1970](https://www.refworld.org/legal/resolution/unga/1970/en/6988): identifies Spain as administering power, reaffirms Sahrawi self-determination, regrets the bloodshed of June 1970, and calls for conditions permitting a free referendum. This supports political mobilisation and contested administration in the 1970 setting; it does not establish an already ongoing large guerrilla war in January.
- [US intelligence memorandum, Spanish Sahara, 6 September 1974, FRUS document 87](https://history.state.gov/historicaldocuments/frus1969-76ve09p1/d87): describes the Spanish governor-general and military administration, the advisory Yemaa created in 1967, Moroccan and Mauritanian claims, and the different histories of Tarfaya (returned in 1958) and Ifni (1969). These separate territories must not be confused with Tifariti. Its discussion of growing independence movements concerns a later phase and is not copied wholesale into January 1970.

## Implemented balance

Both states receive the same **Sahrawi Political Mobilisation** state modifier: construction speed −10%, resource gain −10%, and local recruitable population −20%. These are authored gameplay values, not measured historical percentages. They represent administrative friction, disrupted cooperation with extractive projects, and limited recruitment legitimacy. They are deliberately milder than native MD's `ENG_resistance_against_westminster` state modifier (resources −15%, local manpower −20%, supply −30%, controller attrition +10%, plus productivity effects). No battle damage, automatic armed rebellion, forced war, or countrywide Spanish penalty is introduced.

The modifier is attached directly in the dated state-history blocks, following native MD state-history `add_dynamic_modifier` usage. All three keys are engine-native state modifiers, documented in the installed HOI4 `documentation/modifiers_documentation.html`; MD uses them in state modifiers such as `ENG_overseas_territory`, `ENG_resistance_against_westminster`, and `GLOBAL_azer_resistance_modifier`. No custom numerical consumer is required.

Activation depends on the 1970 state flag and absence of SHA control. Sahrawi control disables the penalties; renewed foreign control restores them. This represents the unresolved colonial question rather than an automatic historical outcome. Existing Spanish diplomatic protocol focuses do not erase it merely by agreeing to further talks.

Explicit 2000 state-history snapshots restore the native MD owners (SHA in 372, MOR in 373), Moroccan cores and the absence of this modifier. Those snapshots affect later scenario creation; they do not transfer territory on reaching the year 2000 in a 1970 campaign. Existing manpower, buildings, resources and province lists are retained.

State-history ownership changes require a fresh scenario to appear. Source validation is separate from testing the modifier's native display and activation in a running HOI4 game.
