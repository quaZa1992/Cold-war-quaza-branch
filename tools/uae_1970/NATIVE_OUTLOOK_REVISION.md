# UAE native outlook integration revision

The user requested that the historical pro-Western ruling houses use Millennium Dawn's actual Western outlook and correct subparty. This revision changes the generated integration, while the immutable approved focus catalogue remains unchanged: SHA-256 `23e89bc7f0a02f4df337248bcfa67d139ec8fc910c414978a3f5ef5913158272`.

## Exact main MD references

Reference checkout: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`.

| Reference | Native mapping | Evidence |
|---|---|---|
| UAE, Zayed | Western outlook `democratic`; `Western_Autocracy`, slot 0 | `history/countries/UAE - United Arab Emirates.txt`: party array 296, leader ideology 315, `king` and `western_Western_Autocracy` traits 317–318 |
| Bahrain | `Western_Autocracy`, slot 0 | `history/countries/BHR - Bahrain.txt`: party array 289, leader ideology 310, native trait 313 |
| Jordan | `Western_Autocracy`, slot 0 | `history/countries/JOR - Jordan.txt`: party array 207, governing slot 216, leader ideology 229 |
| Saudi Arabia | Salafist outlook `fascism`; `Kingdom`, slot 10 | `history/countries/SAU - Saudi Arabia.txt`: governing slot 496, leader ideology 511, `king` and `salafist_Kingdom` traits 513–514 |
| United Kingdom, Tony Blair | Western outlook `democratic`; `socialism`, slot 3 | `history/countries/ENG - United Kingdom.txt`: broad outlook 2497, governing slot 2515, name/ideology 2521–2523 |

`common/ideologies/00_ideologies.txt` places `Western_Autocracy` inside `democratic` and `Monarchist` inside `nationalist`. The native leader traits are respectively `western_Western_Autocracy` and `nationalist_Monarchist` (`common/country_leader/00_traits.txt`, lines 21 and 156). The separate native `king` trait describes a monarch's position and has no modifiers. A constitutional monarchy does not automatically use the autocratic subparty: its elected government keeps its actual subtype. Saudi Arabia is intentionally distinct from the Western autocracies.

These sources establish the game's classification. They do not claim that Western outlook is a parliamentary democracy or that every hereditary monarchy belongs to the same outlook.

## Authored UAE runtime mapping

| Slot | Role | Ideology | Starting support |
|---|---|---|---:|
| 0 | Historical ruling houses | `Western_Autocracy` | 54% |
| 23 | Explicit alternate sovereigntist ruling houses | `Monarchist` | 5% |

Only the old slots 0 and 23 exchange their support. The other subparty values remain unchanged. Broad outlook totals consequently become Western 61%, Emerging 4%, Salafist 2%, Non-aligned 22%, Nationalist 11%. Both arrays sum to 100%.

The direct 1970 country-history snapshot provides the Council, native ideology trait and portrait without a startup or scenario-preview predicate. A dedicated `COLDWAR_UAE_apply_starting_politics` provider makes the same correction in the UAE-only world startup branch, preventing the former generic nationalist profile from undoing it. The Council still lasts until actual federal formation. Later country history remains unchanged.

Slots 0 and 23 use the same institutional ruling-house programme through `COLDWAR_UAE_monarchy_government`; the compiler's runtime gate integration substitutes this helper for the immutable catalogue's former nationalist-only condition. Physical rewards, values, coordinates, exclusions and earned-progress bookkeeping remain unchanged. The catalogue contains no explicit party-popularity support reward needing remapping.

The Council and historical presidential roster keep their identities, portraits, separate cabinet offices, retirement selection and dated successors. Each provider creates the actual governing native subtype and its trait. Named hereditary rulers also receive the native `king` trait; the collective Council receives only its outlook trait. Resynchronization checks native ideology traits as well as names, so changing between slots 0 and 23 cannot leave the same officeholder in the wrong subtype. It does not replay focus rewards.

The historical party registry now supplies names, descriptions and icons for all nine supported slots, including the new historical slot 0 before generic fallbacks. Its inline icons are explicitly mapped and checked against `interface/MD_texticons.gfx` and the existing `gfx/texticons` DDS files. The Communist State icon is case-sensitive: `GFX_generic_Communist_State_small`, not a lowercase derivation from the ideology name. The authored UAE dispatcher remains before native leader removal and modern/native-pool dispatch. The legacy historical slot-23 pool is retained but cannot override the authored provider in this campaign. No global party index or ideology definition is changed.

## Initial British treaty setup guard

The existing native puppet-alignment wrapper continues to preserve UAE domestic politics while qualifying British treaty protection is active. A separate initial-setup exemption covers Bahrain, Qatar, Brunei and Tonga only when all these conditions hold:

- The 1970 scenario and original, non-dynamic country apply.
- The global `COLDWAR_1970_initial_treaty_setup` flag is active around the existing initial British subject sequence.
- Britain is both the actual subject overlord and the intended party-matching target.

Clearing the setup flag restores the ordinary native party-matching behavior for those four countries. Other subjects and overlords are unaffected. The other agent owns the world setup flag bracket and historical Gulf cosmetic guard; this module preserves those markers when rebuilding.

## Verification

`python -B tools/uae_1970/test_politics.py` passes 18 regression groups. These execute the generated political AST around native API boundaries, covering direct history identity, the separate world profile, exact native traits, same-name changes between the two dynastic subtypes, succession and retirement, programme government predicates, registry priority, treaty exemption boundaries, unrelated countries/later starts, parsing and rebuild stability. The unchanged approval hash is checked separately. The broader focus/runtime checks are run by the root compiler owner after its gate update.

No HOI4 engine, live country-selection, save/reload or multiplayer test is claimed. Existing-save migration is not an implemented target; an existing slot-23 government remains a supported alternate government rather than being forcibly changed during a tick.
