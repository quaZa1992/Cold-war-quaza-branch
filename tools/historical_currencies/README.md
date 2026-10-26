# Historical currency presentation

This documents the presentation pass. A later user-authorized balance pass in
`tools/currency_balance/` adds drawbacks to currencies, including the Deutsche
Mark, and renames the DDR Mark to `Mark der DDR (Ostmark)`. Its exact edits are
reversed before the presentation-stage preservation audit. The balance validator
checks the actual current effects; the original presentation baseline stays intact.

This change targets the Cold War currency UI in English. The Deutsche Mark,
DDR Mark effects, every reserve currency ID, all reserve-network calculations,
all other law modifiers, and the existing Euro/Real/Bitcoin date gates are
preserved.

- `russia_rouble` displays **Soviet Rouble** before 1992 and **Russian Rouble**
  afterwards. Its Cold War description distinguishes Soviet cash roubles from
  the transferable rouble used for Comecon accounting.
- `gulden` displays **Dutch Guilder**. Before 1999 it is available without either
  modern restoration focus; the existing focus requirements still apply later,
  and eurozone membership still excludes it.
- `swiss_frank` displays **Swiss Franc**.
- `chinese_yuan` displays **Chinese Yuan**, with a Cold War description of state
  foreign-exchange controls. The previous modern description remains available
  for later scenarios. The 1999 text boundary selects the Cold War versus modern
  scenario wording; it does not represent a claim of a monetary reform in 1999.

The Soviet Rouble and Dutch Guilder use separate new 72x64 uncompressed BGRA DDS
textures, matching the existing currency-icon format and transparent canvas.
The Soviet artwork uses a stylized period emblem rather than the modern ruble
sign; the guilder keeps its florin symbol and bronze field with a clean rim.
The original source textures and their sprite definitions remain intact.

Idea pictures are static assets. The newly assigned Soviet-style rouble icon
is the Cold War presentation of this shared law, including if a campaign is
continued beyond 1991. The name and description have later-period branches;
the preserved original modern icon is not switched automatically by date.

## Asset pipeline

The built-in `image_gen` tool produced the two transparent masters. Full prompts
are in [generation.json](generation.json). `source/` contains their unmodified
PNG outputs and unchanged original texture conversions used as references.
`build_icons.py` only fits the art to the native icon footprint and encodes DDS;
it does not repaint the artwork. Near-invisible generation noise below alpha5
is ignored when measuring outer padding, and original RGBA pixels inside the
measured crop are retained. The masters remain byte-identical to tool output.

```powershell
python tools/historical_currencies/build_icons.py
python tools/historical_currencies/validate.py
python tools/ddr_currency/validate.py
```

`changes.json` records the exact authorized edits to existing game files.
Reversing them must recreate the hashes in `baseline.json`. The DDR validator
also reverses these later known changes before checking its original baseline;
its baseline itself has not been rewritten. The historical validator compares
every law's original AST, including the Deutsche Mark and DDR Mark, and allows
only the two new picture assignments and the historical guilder date branch.

These checks establish source consistency and native asset format, not an
in-game test. Restart HOI4 and load an existing save; no new campaign or currency
re-adoption is needed for the presentation changes.

## Historical references

- [Bank of Russia, approval of the modern ruble sign on 11 December 2013](https://cbr.ru/press/PR/?file=131211_121051rubl4.htm).
- [Contemporary APuZ study of the Comecon currency system, 1986](https://www.bpb.de/shop/zeitschriften/apuz/archiv/533656/das-waehrungssystem-der-rgw-laender/).
