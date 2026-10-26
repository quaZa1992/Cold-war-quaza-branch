# DDR currency

The reserve-currency law `ddr_mark` displays **Mark der DDR (Ostmark)** in both
German and English, retaining the German name for flavor. The historical
abbreviation is **M**. The name
Mark der Deutschen Demokratischen Republik took effect on 1 January 1968;
the previous MDN name belongs to 1964–1967. See the
[Deutsche Bundesbank currency-history table, PDF page 58](https://www.bundesbank.de/resource/blob/689202/130de3af5c6f92221c1c6e1a1c81e2d1/mL/metadaten-data.pdf).
The historical **M** abbreviation is documented in the
[December 1967 ordinance, published on 3 December](https://www.nd-archiv.de/ausgabe/1967-12-03)
and in the [1974 DDR law-gazette facsimile](https://www.gvoon.de/art/dokumente/1974/gesetzblatt-gbl-ddr-teil-1-1974/pdf/gesetzblatt-gbl-ddr-teil-1-1974-seite_580.pdf).

## Game integration

The currency is appended to the existing reserve-currency law category, keeping
all existing keys and their order. It retains the generic domestic-currency law's
+0.05 political power per day and domestic-debt treatment, and adds +2 percentage
points of stability and -0.5 percentage points to the interest rate. Its drawback
is +10% of base cost for incoming foreign-investment projects. These are
gameplay balance values rather than measured historical effects. There are no
international reserve issuer, adoption-network, trade or research bonuses.
The mod's generic currency strength, inflation and income calculations continue
to apply.

The native MD `interest_rate_multiplier_modifier` is added to the interest rate
in percentage points despite its name: -0.5 changes 5% to 4.5%, subject to the
existing 0.8% minimum and 50% maximum. This system has one modeled national debt
balance, without separate domestic and foreign-currency loan ledgers. The bonus
therefore applies to that entire balance, matching the other currency laws.
The English interest-rate label explicitly uses percentage points. The old
additional explanatory tooltip repeated the same half-point benefit; it has
been removed, so the native modifier appears once. Removing the currency removes
its stability and interest modifiers automatically; existing saves get the new
static law modifiers after restarting and loading, without resetting the
one-time initialization flag or later player currency choices.

New campaigns initialize the currency through `currency_startup`. Existing DDR
saves migrate once on the next weekly pulse, after restarting the game. The
existing save can be loaded normally; allow up to seven in-game days for the
one-time migration. A new campaign is not required. The
historical initialization window is 1 January 1968 through 30 June 1990. A
country flag prevents the migration from overwriting later player choices.
The own-currency trigger protects DDR AI against faction-driven switches to
foreign currencies and against choosing the generic domestic law again.

Run `python tools/ddr_currency/validate.py` from the mod root. The read-only
validator checks syntax, historical date boundaries, migration transitions,
AI protection, localisation and icon format/transparency. It also removes the
three exact insertions in memory and checks their original file hashes, proving
that every pre-existing byte and currency key was preserved. It writes
`validation_report.json`; this is static validation, not an in-game test.

## Icon

The DDR Mark icon uses the supplied coin's hammer, compass and wheat emblem,
adapted through image generation to the mod's existing currency art: raised
silver rim, a recessed coloured field, and highlights from the upper left.
The approved master must already have a transparent background.
The built-in `image_gen` tool produced the master; the complete prompt and
reference list are recorded in [generation.json](generation.json). The user's
original coin is preserved in `source/ddr_coin_reference.png`.

`build_icon.py <approved-generated.png>` preserves the master under
`source/ddr_mark_generated.png` and packages it as
`gfx/interface/ideas/laws/currency_ddr_mark.dds`.
The native icon is 72×64 pixels, with a proportionally fitted subject inside
the existing rouble icon's 58×60 pixel footprint. The DDS contains a single
uncompressed A8R8G8B8 frame and one mip level, matching existing currency icons.
The packaging script does not repaint or remove a background.

The script also records the master and texture hashes in `asset_manifest.json`
and writes native-size, enlarged, and comparison PNG previews. Currency icons
shown for comparison are read unchanged from the game assets.
