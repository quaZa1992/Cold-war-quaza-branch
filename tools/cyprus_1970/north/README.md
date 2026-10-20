# Cyprus party names and the Turkish Cypriot roster

Implemented on 16 October 2026. English game localisation only. New runtime
identifiers use `COLDWAR_NCY_1970_`; party names use each country's own prefix.

## Political display

`../politics.py` overrides name, description and emblem for all 24 native MD
political slots for **each** of CYP and NCY. This preserves the established
outlook/subparty indices and the existing Cyprus programme conditions. It does
not recalculate popularity or create 24 supposedly historical parties. Minor
unattested slots have explicitly alternate political-current names and native
generic outlook emblems. No modern party logo is silently reused.

The full mapping and its conditions are in `../party_catalog.json`. Important
dated names are Eniaion → DISY, the presidential coalition → Democratic
Alignment → DIKO, the original EDEK → socialist EDEK, pre-party Turkish Cypriot
opposition → CTP, communal executive → UBP, independent social democrats → TKP,
and TMT → GKK. Historical Halkçı Parti is not misidentified as the 2016 Halkın
Partisi, and the 2007 TDP name is not used for TKP. Halkçı Parti is not assigned
to the liberal slot merely to fill it.

The display date is a historical naming convention, not a forced election,
government programme or proclamation of statehood. MD's political slots are
gameplay groupings: the presidential coalition using index1 does not imply that
Makarios headed a Western-aligned formal party.

## People and activation

`roster.json` lists **23 people**:

| Role | People |
| --- | --- |
| Political leadership and advisors | Fazıl Küçük, Rauf Denktaş, Ahmet Mithat Berberoğlu, Özker Özgür, Alpay Durduran, İsmail Bozkurt, Mustafa Akıncı, Nejat Konuk, Osman Örek, Mustafa Çağatay, Derviş Eroğlu |
| TMT Bayraktars | Rüştü Kazandağ, Süleyman Eyüpoğlu, Arif Eryılmaz, Çetin Başar |
| GKK commanders | Hayri Ündül, Atilla Erdoğan, Kemal Yavuz, Hikmet Köksal, Y. Selçuk Saka, Bilgi Büyükünal, Ali Yalçın, Erdoğan Dirik |

There is no independent NCY in the January 1970 setup. Initialization requires
an actually existing original NCY in the 1970 scenario. Startup handles an
already existing country; its country-scoped daily pulse handles a later
release. No release, recognition, state transfer, war, unit creation or foreign
political decision is performed by this roster.

Political figures are recruitable advisors; MD's separate leader dispatcher
creates the contemporary representative for the ruling subparty. Küçük/Denktaş
are not replaced by the successive prime ministers or UBP party chairs. CTP
and TKP use their contemporary leadership sequences. Remaining alternate
political currents receive a generic administration rather than a modern
Erhürman, Özersay or Arıklı.

The central MD dispatcher intercepts NCY1970 **before** its modern leader-kill
logic. Recruitment flags prevent duplicate daily recruitment. Modern Sezai
Öztürk and Secme Akın characters are retired only if actually present.

A date change makes a cost-free **Convene a Leadership Review** decision
available to a human player when a newer representative exists for the current
political current. The player may adopt that representative or retain their
incumbent. The atomic effect rechecks country, era, human control and the
unapplied leadership epoch. It changes no party popularity, election schedule
or country reward. It cannot be replayed within the same epoch. Changing the
ruling subparty uses its contemporary representative through the normal MD
dispatcher. A calendar date alone never changes the player's ruling party.

TMT officers are the Turkish officers commanding **local** Turkish Cypriot
forces. They are not Turkey's 1974 invasion-corps commanders. GKK command is
available only from its formation on 1 August 1976. Army command and advisor
roles use native MD character syntax. Their skill values are balance choices,
not historical measurements. Political advisors cost75 PP, military chiefs
cost100 PP. Their modest traits grant +3% political power, +3% domestic
influence defence, or −3% bureaucracy costs; army chiefs use MD's existing
`army_chief_organizational_1`. Benefits require the normal advisor appointment.

Stable country/era eligibility is in `allowed`; current existence, dates and
the current-leader exclusion are in `available`. An already recruited military
character can remain in the army for roleplay, but cannot be newly appointed
chief outside the authored eligibility window. A new late-release country does
not receive obsolete TMT chiefs. Later GKK veterans can be retained; no script
automatically appoints, retires or changes a human's army command.

## Portraits and provenance

Native exports are156×210 RGBA DDS, with38×51 small versions. `assets.json`
records source files, original URLs, status, crop boxes and SHA256 hashes.
`portrait_preview.png` shows the actual exported files and labels placeholders.

All **23 named people** now have individual photo-based portraits restored with
built-in image_gen. There are **zero unrelated generic faces, zero raw native
leader portraits and zero untreated official-photo cards** in this Cold War
roster. Revision2 replaces the six placeholder faces, the two native portraits
and all eight untreated GKK photographs. The original seven restored portraits
remain. The exact requested prompt is **“Kolorisiere es und mache das wie ein
handyfoto”**; complete prompts, original source selections and selected PNG
masters are retained in `generation.json` and `masters/v2`.

Every portrait has the same restrained medium-grey photographic background,
natural colour and period appearance. These are AI restorations based on real
photographs, not original colour archival images. Source resolution limits what
can be established about tiny details. A source-unseen face is never supplied
from an unrelated native portrait. `build_north_assets.py` now fails when a
named person has no restored photo record; there is no automatic native or
generic-person fallback.

The four TMT identities come from a directly labelled photographic plate, with
additional university-source corroboration. The correct Kazandağ is the
middle-row centre portrait; Eyüpoğlu middle-row right; Eryılmaz bottom-row left;
Başar bottom-row centre. Eryılmaz retains his actual downward head angle. The
plate and coordinates are in
`references/v2/BAYRAKTAR_PORTRAIT_SOURCES.md`.

Denktaş uses a historical Anadolu Agency photograph published by TRT. Akıncı
uses the **young man on his1975–1990 memoir's cover**, not the elderly man beside
the cover. Eroğlu uses the explicitly identified family photograph captioned
approximately half a century before its2019 publication, around1969. Bozkurt's
identity is cross-checked against the explicitly named1990 election portrait
in the Turkish Historical Society archive, with an office photograph explicitly
dated1985 in Nail Tan's firsthand account. The latter is a lower-resolution
appearance reference. These dates are recorded honestly: not every photograph
was taken in1970, and the restored art is not a claim to an otherwise unknown
exact1970 photograph. GKK faces come from the official commander archive; exact photographic capture
years are not asserted. Their shoulder ranks are adapted to the documented GKK
command rank: Tuğgeneral, except Atilla Erdoğan as Tümgeneral. These are period
reconstructions, not evidence of when a particular original portrait was taken.

Özgür, Durduran and Konuk remain individually matched to the labelled headshots
on printed page4 of the14June1979 Politika newspaper. Durduran is additionally
cross-checked against the labelled right-hand headshot on page3 of the
14May1985 Cumhuriyet. Eight GKK source photos are individually matched to the
official commander archive and **all eight have now been restored**, including
background replacement and removal of white source-card frames and blocky
artifacts.

Anonymous collective administrations use a neutral Cyprus island plaque,
without a human face; it is an institutional illustration rather than an
invented historical leader. The former generic-person preview tile is removed.
All historical named characters retain their own unique portraits. The old
rejected asset catalog/contact sheet is preserved only as explicitly
`v1_superseded` review history and is not used by the game or current preview.

## Historical evidence and uncertainty

Institutional and contemporary sources used for names, dates and images:

- [Cyprus Parliament: DIKO history](https://www.parliament.cy/easyconsole.cfm/id/250): Democratic Alignment announced12May1976, Democratic Party name adopted4December1976.
- [DISY's own history](https://disy.org.cy/40-xp-v-a-n-u-2/): founding4July1976.
- [EDEK's own history](https://www.edek.org.cy/Content/2/Ιστορια-Ιδρυση-ΕΔΕΚ):1969 declaration,3May1970 founding congress, socialist terminology added at the April1974 second congress. The display changes1May because a day was not established.
- [CTP founder remembrance](https://cumhuriyetciturkpartisi.org/4-nisan-2020-ctpnin-kurucu-genel-baskani-ahmet-mithat-berberoglu-aniliyor/) and [50th anniversary](https://cumhuriyetciturkpartisi.org/26-aralik-2020-ctp-50-yasinda/):27December1970 founding, Berberoğlu1970–1976, Özgür1976–1996. The precise31October1976 chairmanship boundary is a secondary chronology detail.
- [UBP's own history](https://ubp.org.tr/tarihce/):11October1975 founding and the separate succession of party chairs; [Örek biography and portrait](https://ubp.org.tr/team/osman-nuri-orek/), [Çağatay biography and portrait](https://ubp.org.tr/team/mustafa-cagatay/), [Eroğlu biography](https://ubp.org.tr/team/dervis-eroglu/).
- [TKP/TDP institutional history](https://www.tdpkibris.org/tarihce/): TKP18March1976, Durduran, Bozkurt1983–1987, Akıncı1987 onwards. The exact6November1983 Durduran boundary is supported by the contemporary Cumhuriyet account below. The1987 transition uses a year boundary, not a claimed appointment day.
- [Atatürk Research Institution: Denktaş](https://ayk.gov.tr/ataturk-uluslararasi-baris-odulu-sahipleri/rauf-raif-denktas-kuzey-kibris-turk-cumhuriyeti-kurucu-cumhurbaskani/) and [Atatürk Encyclopaedia](https://ataturkansiklopedisi.gov.tr/detay/8174/Rauf-Raif-Denktaş-(1924-2012)): election16February1973, oath/accession28February1973. The latter date is used for executive leadership.
- [GKK history](https://www.guvkk.gov.ct.tr/Sayfa/Tarihce) and [official commanders with individual photographs](https://www.guvkk.gov.ct.tr/Sayfa/Komutanlarimiz): formation1August1976 and the eight command tenures. Subsequent availability uses the documented starting **year**;1January is a gameplay boundary, not an asserted exact handover date.
- [Anıtkabir journal94](https://www.anitkabir.com.tr/Files/Dergi/Anitkabir-Dergi-94.pdf), İsmail Bozkurt's first-person account, printedp32/PDFp34: identifies Arif Eryılmaz as Bayraktar and staff colonel in July1974. [Turkish Red Crescent archival volume](https://kizilayakademi.org.tr/wp-content/uploads/2021/10/00191283_kizilay-belgeleri-isiginda-kibris-baris-harekati-1974-profdr.pdf), p82, also identifies Eryılmaz.
- The four TMT turnover **months** are secondary chronology, [DARGEB](https://dargeb.com/turk-mukavemet-teskilati/), which itself cites Wikipedia. This is not independent primary confirmation. They are represented as approximate first-of-month availability boundaries: August1970, July1972, September1974. They must not be quoted as proven appointment days.
- [Politika14June1979](https://filedn.eu/lpwTKmJuSKCLNjzDCWvh2dm/politika-gazetesi/1979-06-14.pdf), printedp4: labelled Özgür/Konuk/Durduran portraits; [Cumhuriyet14May1985](https://egazete.cumhuriyet.com.tr/Archive/CUMHURIYET/GAZETE_ARSIVI/1985/5/14/827F4F8E-9DF4-4D52-8A32-5D9CB160786D_3241180.pdf), p3: Durduran portrait and political chronology.
- [Küçük Bundesarchiv photograph](https://upload.wikimedia.org/wikipedia/commons/8/89/Bundesarchiv_B_145_Bild-F014934-0068,_Fazil_Kutschuk.jpg),1961; [Berberoğlu CTP portrait](https://cumhuriyetciturkpartisi.org/wp-content/uploads/2024/01/1efa9c53e8b155b72bbbc4619982b2ae.jpg); [Özgür supporting historical photograph](https://kibristarih.com/kisiler/ozker-ozgur/), younger mustached man on the left.

## Rebuild and checks

From the mod root:

```powershell
python tools/cyprus_1970/build_north_assets.py
python tools/cyprus_1970/compile.py
python tools/cyprus_1970/validate.py
python tools/cyprus_1970/test_transactions.py
python tools/cyprus_1970/test_north.py
```

The eight additional checks exercise the emitted AST, including absent NCY,
wrong tag/era, initial and late release, exact party-date boundaries, TMT/GKK
recruitment, idempotent initialization, optional human succession, advisor
eligibility, every political display hook and every DDS size. They do not claim
HOI4 loading, in-game rendering or multiplayer synchronization has been tested.

## Revision2 additional image sources

- [Labelled TMT photo plate, Veryansın TV17February2024](https://www.veryansintv.com/tmtnin-ilk-bayraktari-albay-riza-vuruskani-aniyoruz) and [original image](https://cdn.veryansintv.com/2024/02/WhatsApp-Image-2024-02-17-at-13.01.13.jpeg).
- [Fırat University original repository](https://hdl.handle.net/11508/16205), Ayhan Cankut,2006 **master's thesis**189636, printedp101/PDFp122, Resim6. Attribution: Ayhan Cankut, personal photographs, Kıbrıs Türk Mücahitler Derneği. The primary universityPDF is retained, not a broken web mirror.
- [Denktaş historical Anadolu Agency image published by TRT](https://www.trthaber.com/haber/gundem/kibris-turk-halkinin-varolus-mucadelesinin-sembolu-rauf-denktas-546702.html). The article's publication date is not the photograph's capture date.
- [Akıncı memoir announcement and historical cover](https://www.yeniduzen.com/mustafa-akincinin-siyasi-anilarini-kaleme-aldigi-yasandigi-gibinin-ilk-cildi-yayimla-170967h.htm), [memoir bibliographic record](https://isikkitabevi.net/kitap/store.php?id=306150).
- [Eroğlu identified family photograph, Kıbrıs Postası10March2019](https://www.kibrispostasi.com/c1-KIBRIS_POSTASI_GAZETESI/j147/a34363-pazarlik10032019), caption “Yarım Asır Önce”; approximately1969, not an exact-dated1970 image.
- [Bozkurt, Turnalar80, original KIBATEK publisherPDF](https://www.kibatek.org.tr/wp-content/uploads/2026/02/80.-.-SAYI-PDF.pdf), Nail Tan, printedp4/PDFp6: firsthand account explicitly dating the office photograph1985. [TTK Archive Bulletin29](https://www.ttk.gov.tr/wp-content/uploads/2023/07/Arsiv-Bulteni-28.07.2023-2.pdf), printedp29/PDFp37, photograph21: clearly named election-poster identity reference for the22April1990 election. Full evidence and dating limits are in `references/v2/bozkurt_verified_sources_v2.json`.

The current portrait-only contact sheet is `portrait_preview_v2.png`. The asset
regression check is `portrait_revision2_validation.json`:23 unique photo-based
named portraits, zero raw native/official-card or unrelated-face fallbacks,
48 stable large/small DDS files. Uniform rank correction prompts are retained
alongside the original restoration prompts. Exact military insignia in the
low-resolution sources cannot establish a photograph's capture year.
