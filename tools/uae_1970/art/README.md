# Colourised rulers photograph

The user supplied the black-and-white photograph and requested a colourised
version for the events. Created with the built-in ImageGen tool, edit mode,
opaque background, on19October2026. The second, less polished interpretation
was selected after the first pass changed facial details too strongly.
Colours are an artistic interpretation of the supplied monochrome image.

Source: `source/COLDWAR_UAE_rulers_original.png`.
Selected full-size master: `source/COLDWAR_UAE_rulers_colour_master.png`.
Runtime: `gfx/event_pictures/COLDWAR_UAE/COLDWAR_UAE_rulers_colour.dds`.
Sprite: `GFX_COLDWAR_UAE_rulers_meeting_colour`.

The original seven-person composition is fitted proportionally inside native
MD's217x163country-event picture size, using top/bottom matte rather than
cropping people or stretching them. FFmpeg resamples the ImageGen master;
`export_event_picture.py` packages those pixels into lossless RGBA32DDS.
The PNG and decoded DDS are byte-identical. Re-export with:

```powershell
python tools/uae_1970/export_event_picture.py
```

Routing is deliberately limited to rulers/federation subjects: Bahrain and Qatar federal charters and common charter proposals originating
from UAE. Redundant domestic meetings were subsequently retired by the user.
256 UAE instances and32common
instances receive the photo. Other countries' GCC proposals, oil downturns,
arms purchases and unrelated events retain their existing illustration.

Canonical ownership: `event_pictures.uae_picture` is called by the diplomacy
generator; `art.build` emits the dedicated registry; the GCC generator chooses
this sprite only for its UAE origin. The bounded `event_pictures.py` installer
can update existing outputs without rebuilding other modules. It verifies
that every non-picture byte of the event scripts remains unchanged.

## Selected final ImageGen prompt

> COLORIZATION ONLY, not restoration or recreation. Edit target is this exact
> attached archival black-and-white photograph of seven men. Keep its original
> monochrome photograph's grain, low resolution, softness, uneven exposure,
> facial detail, all silhouettes and exact composition completely intact.
> Treat the source luminance as locked and add restrained translucent color
> over it. Do NOT synthesize new faces, sharpen faces, smooth skin, make anyone
> younger, invent costume embroidery, move hands or change garments. Crucial:
> the THIRD man from the LEFT is older and wears dark-rimmed eyeglasses; keep
> his glasses and face exactly as photographed. Preserve each other man's
> exact expression and age, all seven original head positions, the original
> hands and cropped edges. Retain the original speckled photographic grain
> throughout, even where it reduces prettiness. Only color existing source
> areas: white/ivory headcloth and robes, black headbands and dark robes, muted
> brown and taupe outer robes, subdued subtle warm gold trim ONLY where already
> present, naturally muted tan skin, restrained warm beige and dusty
> reddish-brown room, muted carpet. Low saturation, faded archival color film
> palette. Keep original aspect ratio and framing with no crop, no invented
> detail, no added text or border. The result must look like the SAME old
> photograph colorized, not a new ultra-clear digital portrait of different
> people.

Tool input: the user-supplied original local PNG, not a recreated reference.
Selected generated file: `exec-fa5f1cd6-8dd0-434c-abf7-a3c8a6f24e1c.png`.
The original and selected master are retained in this workspace.

## Trucial States Council flag

The pre-federation cosmetic now uses the Council banner rather than the modern
UAE flag. The modern flag was first raised on 2 December1971; the Council's
red/white banner and green seven-point star represent the collective coast in
the1970 scenario. This does not imply that each emirate abandoned its own flag.

Vendored vector: `source/COLDWAR_UAE_trucial_council.svg`, public-domain artwork
by Svyatoslav, simplified by Alkari:
https://commons.wikimedia.org/wiki/File:Flag_of_the_Trucial_States_(1968%E2%80%931971).svg

Historical context: https://www.crwflags.com/fotw/flags/ae_tsc.html and
https://www.mohamedbinzayed.ae/en/latest-news-listing/2026/02/UAE-President-attends-reunion-of-individuals-present-during-founding-of-the-Union
The exact geometry is the identified source illustration, not a primary
government specification verified by this project.

`flags.py` exports the vector deterministically to the engine's82×52,41×26 and
10×7 flag textures, with supersampled edges. All six outlook filename variants
share the same historical Council banner. `Proclaim the Union` drops this
cosmetic; the existing native UAE flag then applies. No modern UAE flag file
is replaced. The compile manifest owns all18 exports.
