# Egypt, January 1970: parties and personnel

All 24 Millennium Dawn subparty slots have Egyptian names, English/German
descriptions, registered icons and explicit leadership choices. Later parties
are deliberately retained at the user's request. Their 1970 leadership casting
is alternative history; it is labelled as such in the party descriptions.

Nasser starts with the Arab Socialist Union. The Socialist Popular Alliance
and Nation's Future Party are optional later-party formations using the existing
subparty slots, not additional indices in Millennium Dawn's 24-entry arrays.
Collective leaders have four purpose-made MD-style group portraits, created
from the existing `egypt_junta` / `egypt_salafis` portraits as visual references.
Their anonymous representatives are fictional, not claimed historical leaders.

Eight military characters are recruited at the start: Fawzi, Sadek, Shazly,
Gamasy, Mahmoud Fahmy, Ali Baghdady, Mohammed Ali Fahmy and Hosni Mubarak.
Ahmad Ismail Ali and Fouad Abou Zikry are optional reserve recalls. Strategic
army leadership uses the game's `field_marshal` role; this does not assert that
Fawzi or Sadek held the historical rank of field marshal in January 1970.

The existing empty starting armies, fleet and air wings remain unchanged.

Photographic edits were made with the built-in Imagegen tool. The base prompt:

> Mach dieses foto kolorisiert und als wäre es mit einem handy aufgenommen wurde.

Identity, clothing, pose and a portrait crop were additionally specified.
Photo dates vary; these are AI-restored game portraits, not documentary colour
photographs taken in January 1970. Fuad II uses a youth photograph from 1977
and an explicitly requested age reconstruction for the January 1970 depiction;
the user's later instruction retained this selected version. The subsequently
provided clipboard photo is retained as an unused reference.

`reference_photos/sources.json` and `party_logo_sources/sources.json` record
the source articles and image URLs. Egyptian Communist Party iconography uses
the existing generic hammer and sickle, rather than crediting a Syrian party
flag as an Egyptian logo. Personal leadership casting is in `roster.py`.

Final DDS assets live in `gfx/leaders/EGY/1970` and
`gfx/texticons/parties_icons/egypt/1970`. The edited PNG masters are in
`tools/egypt_1970/generated`. Emblems were resized from downloaded logo
references; Pillow was used only for layout, resizing and DDS conversion.

The four council images were revised with the built-in Imagegen tool after the
user asked for the HOI4/MD council style: dark painted group scenes, a meeting
table or collective leadership group, period clothing around 1970 and a
faction-appropriate banner. The shared prompt was:

> Bearbeite dieses vorhandene Millennium-Dawn-Ratsporträt als neues HOI4/MD-Spielporträt.
> Die Referenz ist das Editierziel und die verbindliche Stil- und Kompositionsvorlage.
> Behalte die Art des originalen MD-Gruppenporträts: vertikales 156:210-Seitenverhältnis,
> dunkle gedeckte Farben, leicht gemalte realistische Texturen, warmes gerichtetes Licht,
> natürliche plastische Gesichter, dunkle Bildränder und eine vollständig zusammenhängende Szene.
> Der Rat muss als Gruppe erkennbar sein, auch als kleines Spielporträt.
> Alle Köpfe bleiben innerhalb des Bildes. Fülle die gesamte Bildfläche ohne leere Kästen.
> Kein einzelnes vergrößertes Parteienlogo, keine Collage von freigestellten Köpfen,
> kein Text, keine Beschriftung, kein Rahmen, kein Wasserzeichen.

Faction details: the Shi'a reform council includes clerics and civilian jurists;
the guardians' council includes four clerics; the Ba'ath regional command
includes civilian officials and an officer before a pan-Arab banner; the Sinai
council includes three anonymous representatives in period civilian clothes.
The previous emblem-based preview is retained as `party_portraits_before_councils.png`.

Run from the repository root:

```powershell
python -X utf8 tools/egypt_1970/build_content.py
python -X utf8 tools/egypt_1970/validate_content.py
python -X utf8 tools/egypt_1970/preview_content.py
```

If the older Egypt focus compiler is run again, run this builder afterward.
Portrait mappings and the Nasser death flag are also patched into its sources.
Unrelated later focus-story leaders remain outside this January 1970 roster;
`focus_leader_inventory.json` inventories their current portrait coverage.

Validation checks actual files, traits, sprite registrations, all 24 leadership
branches, all 72 localisation routes, both localisation languages, reserve
status, the September succession connection, and the DDS image dimensions.
`validation.json` records the result. An in-game launch has not been performed.
