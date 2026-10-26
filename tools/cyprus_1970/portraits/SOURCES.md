# Cyprus leader portraits: sources and treatment

Five individual historical-photo-based portraits were installed on2026-10-16. They replace the generic art for the named leaders already implemented in the Cyprus tree. Makarios III and Glafkos Clerides retain their existing portraits.

User prompt, preserved verbatim in every generation:

> Kolorisiere es und mache das wie ein handyfoto

Built-in `image_gen` performed the creative restoration and colour treatment. The prompt was supplemented with identity preservation, historical clothing, natural skin texture, full-head framing and a neutral background suitable for small game portraits. Full individual prompts are in [generation.json](generation.json). The resulting images are AI-restored game illustrations based on historical photographs, rather than untouched documentary photographs. Colours and recovered detail can be inferred by the model.

| Leader | Historical reference | Image used / provenance |
|---|---|---|
| Vassos Lyssarides | [Cyprus Broadcasting Corporation, Digital Herodotus, panel photograph](https://digital-herodotus.eu/archive/photo-archive/photo/115/) | Panel dated30May1975; far-left participant is the edit target. [Cyprus University of Technology, George Lanitis Photographic Archive](https://athena.cut.ac.cy/s/georgelanitis/item/304135),1980s close-up, provides supporting facial detail. Saved as `references/lyssarides_panel_1975.jpg` and `references/lyssarides_1980s.jpg`. The2011 elderly Commons photograph was deliberately not used. |
| Ezekias Papaioannou | [Photograph file description](https://en.wikipedia.org/wiki/File:Ezekias.jpg), [identifying article](https://en.wikipedia.org/wiki/Ezekias_Papaioannou) | Original low-resolution portrait served by [Wikimedia](https://upload.wikimedia.org/wikipedia/en/7/78/Ezekias.jpg), saved as `references/papaioannou.jpg`. Date/photographer not established. No Commons free-license claim is made for this local English-Wikipedia image. |
| Georgios Grivas | [Dutch National Archives / ANEFO portrait on Commons](https://commons.wikimedia.org/wiki/File:Georgios_Grivas_1967.jpg) |20November1967; inventory920-8717, unknown photographer. Source page specifies CC0. Saved as `references/grivas.jpg`. Preserve the recognisable moustache, bald head and knitted zip sweater. |
| Nikos Sampson | [Newsbomb historical article](https://www.newsbomb.gr/kypros/story/1664727/kypros-51-xronia-meta-to-praksikopima-kata-tou-makariou-i-proti-fasi-tou-olethrou) | The caption identifies Nikos Sampson and credits EUROKINISSI. [Selected source image](https://img.bbmd.gr/img/900/max/90/2025/07/15/259381.jpg), saved as `references/sampson.jpg`. No open reuse license established. |
| Spyros Kyprianou | [Bernard Gotfryd photograph, Library of Congress](https://www.loc.gov/item/2020735976/), [Commons crop and source metadata](https://commons.wikimedia.org/wiki/File:Spyros_Kyprianou_UN_(cropped).jpg) |24May1978, United Nations, New York. Commons records no known copyright restrictions for the Gotfryd collection. Saved as `references/kyprianou.jpg`. This source is already in colour; treatment restores its colour and detail. |

The source descriptions and credits remain attached to the source photographs; this manifest does not declare a new license for them. No watermark or attribution text was removed from a photograph by the export script.

## Installed files

All five game textures are uncompressed RGBA DDS,156×210pixels, under `gfx/leaders/CYP/1970/`:

- `COLDWAR_CYP_1970_Vassos_Lyssarides.dds`
- `COLDWAR_CYP_1970_Ezekias_Papaioannou.dds`
- `COLDWAR_CYP_1970_Georgios_Grivas.dds`
- `COLDWAR_CYP_1970_Nikos_Sampson.dds`
- `COLDWAR_CYP_1970_Spyros_Kyprianou.dds`

Full-resolution PNG masters are preserved in `masters/`; `assets.json` records project paths and texture checksums. `portrait_preview.png` displays the actual exported DDSs at native size. To repeat format export without regenerating the images, run `python tools/cyprus_1970/build_portraits.py`; masters inside the repository are preferred over the original generation paths.

The runtime generator assigns portraits in every named governing/succession variant, including Sampson's three ideology slots, Grivas's death transition and Kyprianou's post-Makarios succession. A one-time `COLDWAR_CYP_1970_portraits_v1` migration refreshes an already initialized Cyprus leader on the next daily tick. No political programme is reset and no project reward is replayed. The existing generic fallback remains only for unnamed minor alternate administrations.

Static validation checks every named leader's exact portrait assignment, all nine generated leader/succession variants and the DDS dimensions. The five exported images were visually inspected as a contact sheet. An actual in-game graphics reload has not been tested.
