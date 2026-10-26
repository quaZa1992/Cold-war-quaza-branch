# Gulf start portraits and Bahrain ownership, 18 October 2026

State 624 belongs to Bahrain (BHR), both owner and controller, in a new 1970 start. A separate 2000 history snapshot restores native USA ownership for that bookmark. Dated history blocks do not schedule transfers during an ongoing 1970 campaign.

Six starting leader images were individually restored using the built-in image tool with the user prompt: **Kolorisiere das Bild und mach es wie ein Handyfoto qualitativ.** The full per-image prompts, source links, dates, credits and hashes are in `gulf_start_1970_portraits_20261018.json`. The final assets use the existing portrait compiler format: 156 x 210, uncompressed 32-bit RGBA DDS, alpha fully opaque.

The UAE image depicts a historical council meeting, not a single monarch or a claim to show every ruler. The whole group is fit into the portrait tile without cropping the participants.

## Historical references and image credits

- **BHR: Isa bin Salman Al Khalifa** — 1967-04-05. [U.S. Naval Historical Center / Naval History and Heritage Command](https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/NH-98000/NH-98005.html). U.S. federal government photograph, public domain in the United States; downloaded from ibiblio mirror. Source record lists low PNG, medium JPEG, high TIFF.
  Final asset: `gfx/leaders/BHR/BHR_Coldwar_Isa_bin_Salman_Al_Khalifa.dds`.
- **KUW: Sabah Al-Salim Al-Sabah** — 1965. [Kuwaiti Archive, Amiri Diwan](https://commons.wikimedia.org/wiki/File:Sheikh_Sabah_Al-Salem.png). Commons labels PD-Kuwait (expired photographic term in Kuwait).
  Final asset: `gfx/leaders/KUW/KUW_Coldwar_Sabah_Al_Salim_Al_Sabah.dds`.
- **OMA: Said bin Taimur** — 1958-01-01, per source metadata. [Unknown photographer / Col. David Smiley, as attributed by Commons; crop CzarJobKhaya](https://commons.wikimedia.org/wiki/File:Said_bin_Taimur_(cropped).png). CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/ ; edited derivative retains CC BY-SA 4.0.
  Final asset: `gfx/leaders/OMA/OMA_Coldwar_Said_bin_Taimur.dds`.
- **QAT: Ahmad bin Ali Al Thani** — Undated historical official portrait; capture year not established. Ruler 1960-1972; died 1977.. [Amiri Diwan, Qatar](https://www.diwan.gov.qa/about-qatar/qatars-rulers/sheikh-ahmad-bin-ali-al-thani). Official source photograph, no free license established; Wikipedia source is marked non-free. AI colorization/restoration does not establish public-domain status.
  Final asset: `gfx/leaders/QAT/QAT_Coldwar_Ahmad_bin_Ali_Al_Thani.dds`.
- **SAU: Faisal bin Abdulaziz Al Saud** — 1971-05-27. [Robert L. Knudsen / Executive Office of the President; NARA NAID 194360; crop WikiJunkie](https://commons.wikimedia.org/wiki/File:King_Faisal_of_Saudi_Arabia_in_1971_(cropped).jpg). U.S. federal government photograph, public domain in the United States.
  Final asset: `gfx/leaders/SAU/SAU_Coldwar_Faisal_bin_Abdulaziz_Al_Saud.dds`.
- **UAE: Trucial States Council** — circa 1969. [Noor Ali Photographer](https://commons.wikimedia.org/wiki/File:Group-photo-TSC-meeting-1969.jpg). Commons marks public domain under UAE Federal Law No. 7 of 2002; page also says U.S. public-domain tag should be included, while its hidden categories indicate PD-old missing SDC copyright status.
  Final asset: `gfx/leaders/UAE/UAE_Coldwar_Trucial_States_Council.dds`.

All six earlier DDS files already existed; the prior missing-portrait symptom was not traced conclusively to absent files or broken picture references. The restored files replace those assets at their existing paths. The first Saudi and Trucial native-pool entries now match the authored 1970 starters (Faisal and the Trucial States Council). Oman and Qatar had a separate proven source-routing mismatch: their historical leader pools used party 13, while their authored 1970 starters use Monarchist/23 and Kingdom/10. The historical leader records, runtime pool dispatch, counter synchronization and portrait ideologies now match those existing start profiles. Country history and political start values were preserved. The outdated sole-Khalid retirement restriction was removed after Faisal became an approved pool candidate, matching the existing generator logic. The initial suspected party-index mismatch was disproven: those values belonged to the separate 2000 history blocks, and those files were restored byte-for-byte.

## Validation boundary

Asset dimensions, decoding, opaque alpha, hashes, state-history snapshots, source/runtime identities and path bindings are checked locally. No HOI4 launch or visible in-game portrait rendering was performed by the agent. A complete game restart and new 1970 campaign are required to confirm the observed display issue is resolved.
