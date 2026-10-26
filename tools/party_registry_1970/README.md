# COLDWAR | 1970 party registry

Source of the politics-screen party names, descriptions and icons for the 1970 start.

* `data/<TAG>.json` – one file per country, the 24 MD ideology slots (name, English name, native name,
  abbreviation, ideology, two-paragraph description, optional MD icon, optional later period with `from`).
* `logo_icons.json` – fetched party logos (`TAG|slot|period` -> sprite in
  `gfx/texticons/parties_icons/1970_registry/`, declared in `interface/mdcw_1970_party_registry.gfx`).
* `generate.py` – writes `common/scripted_localisation/mdcw_historical_parties.txt` and
  `localisation/english/mdcw_1970_party_registry_l_english.yml`.

Display follows Millennium Dawn: `(ABBR) - English name`; catchy factions (catchy = true) show the native label.
Description header: `(Ideology) - English name (Language: native name, ABBR)`.

Hand-authored regional entries stay untouched: registry lines marked `# COLDWAR` and
`# COLDWAR ... BEGIN/END` blocks are carried over on every run (DDR, VIE, IRQ, UAE).

Run from the mod root: `python tools/party_registry_1970/generate.py --root .`
