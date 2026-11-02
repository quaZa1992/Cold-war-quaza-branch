IMPERIA COLD WAR

# Brazil-only presentation polish

The 2 November 2026 polish is confined to Brazil's focus tree and its own events, political decisions and English localisation. `POLISH_CHECK.json` compares the installed output with the compact pre-polish baseline: no non-Brazil runtime file changed, all 224 focus gameplay records are identical, and no existing execution helper changed. Coordinates, prerequisites, exclusions, focus titles, durations, rewards and GDP prices remain unchanged.

## Player-facing changes

The compiler applies 192 reviewed English replacements from `english_polish.json`. Cabinet events, their fifteen policy spirits, fourteen foreign proposal notices, congress decisions and selected national programmes now use specific institutional language. Oil shocks refer to actual surging world prices rather than asserting that the event is the historical 1973 shock. The US military dispute does not assume a particular US president. Text distinguishes inflation-related fiscal costs from a direct change in the inflation rate. Rapid Competition describes productive efficiency and political resistance, matching its real modifiers.

Party descriptions distinguish ARENA and military command; MDB, PMDB and PSDB; the restored historic PTB, Ivete Vargas's PTB and PDT; and the Lacerdist movement from the PRN. Formation dates are not asserted as current facts where the approved early reform can create a genuine alternative sequence. PRN retains its actual late formation gate. No new chronological barrier was added.

The Party Reorganisation event now previews the registration decisions it opens. Its limited-opening option also shows the conditional PCB and PCdoB routes after the same 1984 threshold used by execution. The labourist split previews the actual one-time party support and outlook changes from registering PTB and PDT. All eleven formation decisions show both native +1% support effects and the relevant congress decision access. Registration already completed does not promise another formation reward.

These additions use native numeric effects and decision unlocks. Thirteen new display helpers are called only through `effect_tooltip`; real party registration remains behind the original guarded hidden effects. The existing government, nomination, formation and programme execution helpers are unchanged.

## Graphics ownership

An initial art-selection pass assigned appropriate existing native symbols to 185 focuses, giving the tree 83 distinct symbols. The project keeps 87 normal/shine aliases so archived references remain valid. No new focus artwork was generated. `focus_art_polish.json` records this selection and its sources; `docs/brazil_1970_concept/FOCUS_ART_PROVENANCE.md` records the independent mapping and footprint review.

The user subsequently reserved further image work. No proposed event-photograph replacement was applied, and no further image or graphic assignment was changed after that instruction. Future image work belongs to the user. The nine existing event images retain their prior donors, frames and alpha pixels.

`docs/brazil_1970_concept/EVENT_ART_POLISH_REVIEW.png` is an inspection contact sheet of the existing nine event textures, not a replacement asset or an archival-photo claim. Source paths and provenance limits remain those in `art_manifest.json`, `art.py` and `NOTICE.md`. No external photograph was downloaded or introduced.

## Verification

The emitted-source validator reports 9,936 assertions with zero errors. It now also verifies the real registration amounts against both native preview rows, every decision-unlock reference, the split event's two formation previews and unchanged approved gameplay. `compile.py --check` verifies deterministic output. `polish_check.py` establishes the Brazil-only file boundary and unchanged existing execution helpers.

The native fixture contains 117 assertions, including three new checks that registration previews do not grant party support, change outlook support or register an organisation. See `NATIVE_RESULT.json` for the final isolated run and `NATIVE_CHECKPOINTS.txt` for its exact assertion log. Frozen source and referenced-art hashes are checked by `package_report.py`. Private profiles and engine logs remain under the user-approved `D:/HOI4_Mod_Tools/mdcoldwar/runtime/brazil_1970/` path.

Independent reviews are `NEW_POLISH_MECHANICS_REVIEW.md`, `docs/brazil_1970_concept/ENGLISH_POLISH_REVIEW.md` and `FOCUS_ART_PROVENANCE.md`. The native fixture is an artificial fresh-start scenario. It does not establish full live focus-hover rendering, save/reload behavior, every later succession or network multiplayer balance. No complete focus-hover screenshot session is claimed.

## Authoring

`presentation.py` applies the English and native-symbol selections to the runtime model without changing the approval. `politics_presentation.py` supplies display helpers and wraps existing formation transactions. The loaded files remain generated by `compile.py`; the immutable `approved_design.json` is unchanged. Read `README.md` for the original implementation, numerical modifier translations and source records.
