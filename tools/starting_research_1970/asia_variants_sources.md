IMPERIA COLD WAR

# Asia and Middle East: historical equipment design provenance

Cutoff: 1 January 1970. Region includes Turkey and excludes the former Soviet republics, Cyprus and Northern Cyprus. The companion strict JSON is the maintained design input. This record describes evidence and representation limits; it is not a complete order of battle or an equipment inventory.

Research and native module mapping: Codex for the IMPERIA COLD WAR project. Historical facts are referenced to the originating institutions and authors at the linked pages. Copyright, authorship and licences remain with the original sources. Reuse permission is unknown unless a source states otherwise. No source photographs, diagrams or substantial passages were copied into the mod, and no ownership of third-party work is claimed.

## Method and cutoff

The JSON records model families known in service before the cutoff, their original design producer, bounded entry dates, contemporary physical fittings and local operators. A date ending 31 December bounds evidence stated only to a year; it does not assert a known acceptance ceremony on that day. Different national entry dates are explained in the model notes. A date on an order or a prototype does not establish operational delivery. Later sources are used only when they explicitly identify an earlier event, production series, artifact or service episode.

The package is representative. It provides documented core families across land, air and naval equipment while deliberately leaving uncertain fleets or specific gun models unassigned. Country arrays cover all 97 regional history tags. Empty arrays mean that this pass has no independently evidenced design package for that tag. They do not assert a population had no rifles or vehicles. Hypothetical releases receive no invented national tank, aircraft, shipyard or missile programme. Colonial and leased territories do not automatically receive the entire force of a foreign garrison.

Imported equipment is an operator's historical service design. Its original producer is recorded separately from licensed local manufacture. The compiler may unlock the minimal existing bare family and exact historical service components before creating the design; this does not transfer the producer's entire industrial, electronics or strategic research programme. No army, fleet, stockpile, air wing, carrier air group, warhead or completed special project is created.

## Native equipment mapping limits

Final physical audit: MiG-21, J-7 and Mirage III now use the native delta-wing module. Aircraft gun subslots use the project's neutral historical machine-gun, 20 mm, 30 mm or mixed-cannon modules. The original 83.4 mm Centurion gun uses the nearest historical 75/85 mm band. Type 61, Centurion, Sho't and Patton designs use the native Cast Turret module; its internal `tank_soviet_turret` identifier does not imply Soviet origin. Original engines and armour materials are retained.

- T-54/Type 59/Vijayanta/Sho't use the native 100/105 mm gun category. They do not use the later 115/120/125 mm category. Original 90 mm Pattons and Type 61 use the added narrow 90 mm module. M47 retains its original petrol engine, and Israeli Sho't retains the Meteor petrol engine at this cutoff. M47M and Sho't Kal later diesel conversions are excluded.
- AMX-13 and M41 use MD's recon/light-tank role chassis, with the compatible light suspension and `Rec_tank_0` legacy fallback. The AMX-13's actual oscillating turret and mechanical revolver magazines are recorded. No M41D or AMX-13 SM1 rebuild is supplied.
- M113 uses an original petrol, aluminium, machine-gun APC fit. Type 60 and Type 63 APCs remain their own early diesel troop-carrier families. MD's amphibious-chassis identifier is its APC equipment family and does not claim every represented vehicle is a literal amphibious tank.
- The M42 is optical twin-40 mm SPAA with no radar. Towed M101/M114 remain native static models with no fabricated tank-designer slots. The M-46 uses the existing heavier artillery family to distinguish the 130 mm long-range gun from a 105 mm light howitzer.
- Rifles, trucks and liaison 4x4s are static native families with no modern accessory, armour or special-forces upgrades. Type 56 SKS and AK models are distinct. ROK's M1 baseline is retained despite more modern weapons in particular overseas formations. Singapore gets the already issued M16 family, not a later date for M16S1 series production.
- MiG-21/F-104/Mirage III use the second-generation 1955 light family. F-4 uses the 1960 medium family. F-4D has no internal cannon; early F-4E retains its cannon. Ordinary gun-only Sabres, Hunters and J-5s do not gain radar missiles merely because another national aircraft carried them.
- Aircraft stores are conventional unguided bombs, original guns and specifically documented early IR/SARH missile families. H-6's conventional native bomb bay adds no H-6D/K missile or tanker system. Operational Marut Mk.1 keeps non-afterburning Orpheus engines and subsonic performance, excluding experimental reheat and Egyptian engine trials. The T-28 retains a piston engine; the A-37 is a subsonic twin-jet attack aircraft.
- Utility helicopters use `mdcw_utility_helicopter_1955_modular` for NSB and the static 1955 utility family without NSB. The native medium helicopter category is the smallest compatible with an unarmed transport layout, even for physically light Bell 206/Alouette aircraft. The original Mi-4 piston engine is distinguished from the turbines in Alouette/UH-1/Whirlwind Mk.10/Bell 206. No 1985 attack-helicopter chassis is used.
- Conventional diesel submarines are not nuclear boats. Only already commissioned conventional families are represented: Oshio, Kalvari/Foxtrot, Hangor/Daphne, Ghazi/Tench Fleet Snorkel, Turkish Balao, Indonesian Whiskey, Chinese Type 033 and Israeli T class. No Uzushio/Ming/Type 214 or later submarine conversion is added.
- Surface ships retain early gun, steam machinery, conventional radar/analogue director and ASW fits. Amatsukaze's Tartar installation uses the narrow early naval SAM family; later ASROC bundles are omitted. Anshan excludes its later anti-ship missile conversion. Original Type 12 Talwar is not the missile frigate class introduced decades later. Vikrant's deck does not create embarked aircraft.

`module_exceptions` documents the source and actual historical hardware behind coarse native first-generation modules whose tree dates do not match their earlier physical introduction. These are bounded conventional materials, mechanical engines, analog directors, early radar and transport layouts. They do not permit ERA, composite armour, laser rangefinders, thermal sights, CIWS, proximity ammunition or later guided weapons.

## Important dated checks

- Japan's Howa manufacturer page dates Type 64 adoption to 1964 and specifies its original 7.62 mm, gas-operated, twenty-round configuration. AWEIL dates Ishapore 7.62 mm regular production to 1964-65. Chinese defence sources identify both Type 56 rifle families as 1956 designs, with Vietnamese use independently documented in 1967-68 US Army history and a dated September 1968 captured-weapon photograph.
- CINCPAC Command History 1969 distinguishes North Korea's AK-47 manufacture from South Korea's still prevalent M1 rifle/carbine. The 1962 Iran aid memorandum identifies existing M1 stocks; future planned programme quantities are not treated as deliveries. German parliamentary records date Turkey's G3 licence to 1967; a physically marked POF artifact establishes Pakistani 1967 manufacture. Nepal's FAL adoption in 1960 is explicitly stated by Small Arms Survey, with later M16 acquisition kept separate.
- FAW dates the first CA10 to July 1956; the BJ212 manufacturer dates production approval to 1966. AVNL's factory history and Nissan's corporate history place the Indian Jonga programme in 1969; the Shaktiman entry is confined to AVNL's documented 1969 MAN collaboration. Mitsubishi and Toyota manufacturer histories establish the earlier licensed Jeep family and its Japanese institutional operator context.
- Indian Gnat combat in September 1965 is recorded contemporaneously in the government's Yojana magazine. The 1964 Indian parliamentary debate explicitly identifies Mi-4s already in the inventory. Marut's delivery pilot reports a March 1967 flight in his logbook, preceding the documented April 1967 squadron formation.
- June 1964 JCS and January 1965 Bangkok records explicitly count Lao and Thai T-28s already available. The USAF's official history places VNAF A-37 conversion in November 1968 and three squadrons by May 1969. Chinese SASTIND/AVIC records H-5 certification and batch production in April 1967; later special conversions are excluded.
- Pakistan Navy History Cell places Hangor commissioning on 1 December 1969. A January 1970 commissioning claim from derivative lists was rejected. Other exact navy entry dates are retained in each family record. Japan's Oshio is the commissioned 1965 boat, not the 1971 Uzushio class.

## Deliberate exclusions and unresolved completeness

The manifest excludes later F-4EJ production in Japan, Singapore Hunters delivered in 1970, Taiwanese M48s first acquired after the cutoff, later Sino-Pakistani F-6 delivery assumptions, later Chinese anti-ship/strategic programmes, modern Iranian F-14/Chieftain holdings, Israeli later diesel/ERA conversions and every undocumented hypothetical national package. M101/M114 assignments initially considered for India, Thailand, the Philippines and Turkey were removed where this pass lacked exact model-and-date evidence. No Abbot is assigned to India without a reliable pre-cutoff operator delivery record. No SP artillery model is invented to fill a checklist.

Native stats are coarse family approximations. Calibre, suspension, helicopter size and piston-engine performance cannot always be encoded exactly with existing modules. The recorded physical configuration takes priority over a superficially matching modern family. Static checks establish IDs, slots, compatibility, DLC routing and dates; actual live designer acceptance, balance and multiplayer/save-load behavior still require native game verification.

## Model and source index

Each row links the historical evidence used for that exact family. Additional operator and component explanations remain in the JSON notes. The source institutions retain their original authorship; unidentified individual authors and reuse licences are unknown.

| Model ID | Service bound | Original producer | Sources |
| --- | --- | --- | --- |
| `as_t54` | 1969-12-31 | SOV | [source 1](https://www.cia.gov/readingroom/docs/DOC_0000014188.pdf), [source 2](https://history.state.gov//historicaldocuments/frus1969-76ve07/d327), [source 3](https://mcoecbamcoepwprd01.blob.core.usgovcloudapi.net/library/CavalryArmorJournal/1960s/1968Jul-Dec.pdf) |
| `as_type59` | 1959-10-01 | CHI | [source 1](https://www.mod.gov.cn/gfbw/tp_214132/jskj/4827567_3.html), [source 2](https://www.sastind.gov.cn/history/n152/n6760142/n6760146/n6760161/c6807606/content.html) |
| `as_type61` | 1961-04-30 | JAP | [source 1](https://www.mod.go.jp/gsdf/nae/7d/tk_history.html), [source 2](https://www.mhi.com/company/overview/outline/pdf/2008_all.pdf) |
| `as_vijayanta` | 1966-12-31 | ENG | [source 1](https://avnl.co.in/index.php/milestone), [source 2](https://avnl.co.in/files/avnl_documents/AVNL_Complete2.pdf) |
| `as_centurion20` | 1965-09-30 | ENG | [source 1](https://publications.gc.ca/collections/collection_2024/mdn-dnd/d12/D12-11-5-8-eng.pdf), [source 2](https://tankmuseum.org/tank-nuts/tank-collection/m47?tpage=2), [source 3](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_shot_meteor` | 1969-12-31 | ENG | [source 1](https://spokesperson.blob.core.windows.net/digital/tanks-slider/index.html) |
| `as_m47` | 1967-06-30 | USA | [source 1](https://tankmuseum.org/tank-nuts/tank-collection/m47?tpage=2), [source 2](https://history.state.gov/historicaldocuments/frus1958-60v12/d237), [source 3](https://armyhistory.org/the-m48-patton-main-battle-tank/), [source 4](https://dergipark.org.tr/en/download/issue-full-file/81836), [source 5](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_m48a1` | 1966-12-31 | USA | [source 1](https://armyhistory.org/the-m48-patton-main-battle-tank/), [source 2](https://artsandculture.google.com/asset/delivery-of-u-s-m48-tanks-for-rok-military-modernization-the-bureau-of-public-information/wwGTWxiJ7bFH8g?hl=ko), [source 3](https://dergipark.org.tr/en/download/issue-full-file/81836), [source 4](https://spokesperson.blob.core.windows.net/digital/tanks-slider/index.html) |
| `as_amx1375` | 1969-08-09 | FRA | [source 1](https://tankmuseum.org/tank-nuts/tank-collection/amx-13), [source 2](https://www.army.gov.sg/our-forces/formations/armour/), [source 3](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_m41a3` | 1965-12-31 | USA | [source 1](https://history.army.mil/Portals/143/Images/Publications/Publication%20By%20Title%20Images/M%20Pdf/CMH_Pub_90-17-1.pdf), [source 2](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_m113` | 1964-12-31 | USA | [source 1](https://history.army.mil/Portals/143/Images/Publications/Publication%20By%20Title%20Images/M%20Pdf/CMH_Pub_90-17-1.pdf), [source 2](https://dergipark.org.tr/en/download/issue-full-file/81836), [source 3](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_type60apc` | 1960-12-31 | JAP | [source 1](https://www.mhi.com/company/overview/outline/pdf/2008_all.pdf), [source 2](https://www.mod.go.jp/gsdf/nae/7d/tk_history.html) |
| `as_m101` | 1969-12-31 | USA | [source 1](https://history.army.mil/Portals/143/Images/Publications/Publication%20By%20Title%20Images/M%20Pdf/CMH_Pub_90-17-1.pdf), [source 2](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf), [source 3](https://dl.ndl.go.jp/view/prepareDownload?contentNo=8&itemId=info%3Andljp%2Fpid%2F11043385), [source 4](https://www.govinfo.gov/content/pkg/GPO-CRECB-1971-pt32/pdf/GPO-CRECB-1971-pt32-1-3.pdf), [source 5](https://www.marines.mil/portals/1/Publications/U.S.%20Marine%20Operations%20in%20Korea%201950-1953%20Vol%205_Operations%20in%20West%20Korea%20%20PCN%2019000264000.pdf?ver=2017-04-26-105935-777) |
| `as_m114` | 1969-12-31 | USA | [source 1](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf), [source 2](https://dl.ndl.go.jp/view/prepareDownload?contentNo=8&itemId=info%3Andljp%2Fpid%2F11043385), [source 3](https://www.govinfo.gov/content/pkg/GPO-CRECB-1971-pt32/pdf/GPO-CRECB-1971-pt32-1-3.pdf), [source 4](https://ndlsearch.ndl.go.jp/books/R100000002-I034001384) |
| `as_m46` | 1968-03-07 | SOV | [source 1](https://www.intelligence.gov/assets/documents/tet-documents/dia/DlAISUP-67-68%20ARMOR%2C%20ARTILLERY%2C%20AND%20AIRBORNE%20THREAT%20AGAINST%20SOUTH%20VIETNAM.pdf) |
| `as_mig17` | 1968-07-31 | SOV | [source 1](https://www.cia.gov/readingroom/docs/DOC_0000233051.pdf) |
| `as_j5` | 1956-12-31 | CHI | [source 1](https://www.cia.gov/readingroom/docs/DOC_0000233051.pdf), [source 2](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_j6` | 1965-12-31 | CHI | [source 1](https://www.cia.gov/readingroom/docs/DOC_0000233051.pdf), [source 2](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_mig21f` | 1968-07-31 | SOV | [source 1](https://www.cia.gov/readingroom/docs/DOC_0000233051.pdf), [source 2](https://history.state.gov//historicaldocuments/frus1969-76ve07/d327) |
| `as_mig21pfm` | 1969-03-28 | SOV | [source 1](https://www.history.navy.mil/about-us/leadership/director/directors-corner/h-grams/h-gram-029/h-029-2.html), [source 2](https://www.cia.gov/readingroom/docs/DOC_0000233051.pdf) |
| `as_mig21fl` | 1967-12-31 | SOV | [source 1](https://hal-india.co.in/our-history), [source 2](https://hal-india.co.in/production-unit-details/aircraft-manufacturing-division-nasik) |
| `as_f86f` | 1969-12-31 | USA | [source 1](https://www.mod.go.jp/asdf/miho/about/tenjiki/index.html), [source 2](https://www.pafmuseum.com.pk/history/), [source 3](https://www.mnd.gov.tw/File/36873), [source 4](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_cac_sabre` | 1969-12-31 | AST | [source 1](https://repositori.parlimen.gov.my/bitstream/123456789/3540/49/DR-19031971.pdf) |
| `as_f104j` | 1962-03-31 | USA | [source 1](https://www.mod.go.jp/asdf/miho/about/tenjiki/index.html) |
| `as_f104a` | 1968-12-31 | USA | [source 1](https://www.pafmuseum.com.pk/history/), [source 2](https://www.mnd.gov.tw/File/36873), [source 3](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_f104g` | 1964-08-10 | USA | [source 1](https://www.guvkk.gov.ct.tr/Anitlar/Ucak), [source 2](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_f5a` | 1969-12-31 | USA | [source 1](https://www.rocafa.edu.tw/english/tour/index-1.asp?Parser=13%2C18%2C144%2C485%2C%2C%2C349%2C%2C%2C%2C2), [source 2](https://kookbang.dema.mil.kr/newsWeb/20170828/1/BBSMSTR_000000010232/view.do), [source 3](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf), [source 4](https://www.govinfo.gov/content/pkg/GOVPUB-D301-PURL-gpo125295/pdf/GOVPUB-D301-PURL-gpo125295.pdf) |
| `as_f4d` | 1969-08-29 | USA | [source 1](https://kookbang.dema.mil.kr/newsWeb/20170828/1/BBSMSTR_000000010232/view.do), [source 2](https://history.state.gov//historicaldocuments/frus1964-68v22/d322) |
| `as_f4e` | 1969-09-30 | USA | [source 1](https://media.defense.gov/2010/Oct/12/2001309632/-1/-1/0/AFD-101012-038.pdf), [source 2](https://history.state.gov/historicaldocuments/frus1964-68v20/d306) |
| `as_mirage3cj` | 1967-06-30 | FRA | [source 1](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf), [source 2](https://history.state.gov/historicaldocuments/frus1964-68v18/d402) |
| `as_mirage3e` | 1969-12-31 | FRA | [source 1](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf), [source 2](https://www.pafmuseum.com.pk/history/), [source 3](https://secondtonone.com.pk/wp-content/uploads/2023/07/Second-to-none-3rd-Magazine-July-2020.pdf) |
| `as_hunter` | 1967-12-31 | ENG | [source 1](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf), [source 2](https://history.state.gov/historicaldocuments/frus1964-68v18/d402) |
| `as_lightning` | 1969-12-31 | ENG | [source 1](https://agda.ae/en/archives/TNA/FCO/8/664) |
| `as_jetprovost` | 1959-12-31 | ENG | [source 1](https://airforce.lk/news.php?news=5095), [source 2](https://www.airforce.lk/history_pages.php?pages=air_attack) |
| `as_alouette3` | 1969-09-30 | FRA | [source 1](https://www.rsaf.gov.sg/about-us/history/history-of-the-rsaf/1968-nov-first-helicopter/), [source 2](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_uh1b_jp` | 1963-08-31 | USA | [source 1](https://www.subaru.co.jp/csr/report/pdf/2010/all.pdf) |
| `as_whirlwind10` | 1966-12-31 | ENG | [source 1](https://www.pelitabrunei.gov.bn/Arkib%20Dokumen/2021/Pelita%20Brunei%2028062021.pdf) |
| `as_bell206` | 1968-12-31 | USA | [source 1](https://www.pelitabrunei.gov.bn/Arkib%20Dokumen/1996/PB%2024%20April%201996.pdf) |
| `as_oshio` | 1965-03-31 | JAP | [source 1](https://www.mod.go.jp/msdf/sbf/history/history.html), [source 2](https://www.mod.go.jp/atla/research/dts2012/R2-2p.pdf) |
| `as_kalvari` | 1967-12-08 | SOV | [source 1](https://www.pib.gov.in/newsite/PrintRelease.aspx?lang=2&reg=48&relid=174299) |
| `as_hangor` | 1969-12-01 | FRA | [source 1](https://www.paknavy.gov.pk/English%20NN%20DEC%20MP.PDF), [source 2](https://www.app.com.pk/domestic/navy-war-college-celebrates-53rd-hangor-day/) |
| `as_ghazi` | 1964-06-01 | USA | [source 1](https://www.history.navy.mil/research/histories/ship-histories/danfs/d/diablo.html), [source 2](https://www.pafmuseum.com.pk/history/) |
| `as_balao` | 1960-03-18 | USA | [source 1](https://www.history.navy.mil/research/histories/ship-histories/danfs/m/mapiro.html) |
| `as_pasopati` | 1962-01-29 | SOV | [source 1](https://www.tnial.mil.id/assets/majalah/PDF-20200724-163349.pdf), [source 2](https://repositori.kemendikdasmen.go.id/26873/1/Katalog%20museum%20NAsional%20Jilid%202.pdf) |
| `as_type033` | 1965-12-31 | CHI | [source 1](https://navy.mnd.gov.tw/mediaroom/Paper_Info.aspx?AID=222&ID=30211), [source 2](https://www.mnd.gov.tw/File/16004) |
| `as_tclass` | 1968-12-31 | ENG | [source 1](https://archives.mod.gov.il/sites/English/Exhibitions/Pages/DAKAR.aspx), [source 2](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf), [source 3](https://www.cna.org/archive/CNA_Files/pdf/d0026727.a1.pdf) |
| `as_harukaze` | 1956-04-30 | JAP | [source 1](https://www.mhi.com/jp/company/overview/museum/nagasaki) |
| `as_amatsukaze` | 1965-02-28 | JAP | [source 1](https://www.mhi.com/jp/company/overview/museum/nagasaki), [source 2](https://www.usni.org/magazines/proceedings/1967/november/japan-present-and-potential-military-power), [source 3](https://www.usni.org/magazines/proceedings/1967/may/professional-notes-notebook-and-progress) |
| `as_anshan` | 1954-12-31 | SOV | [source 1](https://paper.people.com.cn/rmzk/html/2018-11/09/content_1891666.htm) |
| `as_shahjahan` | 1958-12-16 | ENG | [source 1](https://www.paknavy.gov.pk/English%20NN%20DEC%20MP.PDF) |
| `as_talwar` | 1960-04-26 | ENG | [source 1](https://twitter.com/indiannavy/status/1651082075628511235), [source 2](https://inexartificers.com/public/uploads/ebooks/Ebook_1_07-01-2019_11_39_25.pdf), [source 3](https://navalinstitute.com.au/wp-content/uploads/2014/04/headmark-003-Feb-1976.pdf) |
| `as_vikrant` | 1961-03-04 | ENG | [source 1](https://www.pib.gov.in/newsite/erelcontent.aspx?lang=2&reg=48&relid=98029) |
| `as_il28` | 1968-07-31 | SOV | [source 1](https://www.cia.gov/readingroom/docs/DOC_0000233051.pdf) |
| `as_canberra` | 1957-09-01 | ENG | [source 1](https://www.pib.gov.in/newsite/PrintRelease.aspx?lang=2&reg=48&relid=170404) |
| `as_b57` | 1959-11-30 | USA | [source 1](https://www.pafmuseum.com.pk/history/), [source 2](https://secondtonone.com.pk/wp-content/uploads/2021/04/1st-magazine-Second-to-none-Magazine-1st_compressed.pdf) |
| `as_h6` | 1969-12-31 | CHI | [source 1](https://www.comac.cc/fujian/dzzz/202508_134.pdf), [source 2](https://rfb.ln.gov.cn/rfb/rfzs/2CA92A392EA24DFC9A15A1C3FB6250DE/index.shtml), [source 3](https://www.cia.gov/readingroom/docs/DOC_0000233051.pdf) |
| `as_c130` | 1965-12-31 | USA | [source 1](https://tni-au.mil.id/tentang-kami/detail-sejarah/sikorsky-s-58t-twinpac-hadiah-persahabatan), [source 2](https://secondtonone.com.pk/wp-content/uploads/2021/04/1st-magazine-Second-to-none-Magazine-1st_compressed.pdf), [source 3](https://www.lockheed-martin.com/en-sa/news/lockheed-martin-celebrates-60-years-of-partnership-with-the-kingdom-of-saudi-arabia.html), [source 4](https://www.lockheedmartin.com/en-us/products/c130/history.html), [source 5](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_m42` | 1969-12-31 | USA | [source 1](https://webpac.tad.gov.tw/ebook/A20009393.pdf), [source 2](https://www.mod.go.jp/gsdf/nae/2d/kuniwomamoru/soubihin/souki/87jisoukousyakikannhou.htm), [source 3](https://armyhistory.org/duster-m42-self-propelled-anti-aircraft-gun/) |
| `as_type63apc` | 1969-12-31 | CHI | [source 1](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201976.pdf) |
| `as_j7` | 1966-11-30 | CHI | [source 1](https://www.mod.gov.cn/gfbw/gfjy_index/js_214151/4859875.html), [source 2](https://gdb.xlgl.gov.cn/rfb/rfzl/zsbl/2024011714533993420/index.html) |
| `as_cambodian_j5` | 1968-01-04 | CHI | [source 1](https://web.stanford.edu/group/tomzgroup/pmwiki/uploads/1806-1968-01-05-PQ-a-OEP.pdf), [source 2](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_strikemaster` | 1968-12-31 | ENG | [source 1](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf), [source 2](https://mod.gov.om/Home/RAFO) |
| `as_sye_provost` | 1968-12-31 | ENG | [source 1](https://www.sipri.org/sites/default/files/SIPRI%20Yearbook%201968%E2%80%9369.pdf) |
| `as_type64_rifle` | 1964-12-31 | JAP | [source 1](https://www.howa.co.jp/products/firer/defense/product03.html) |
| `as_1a1_slr` | 1965-12-31 | BEL | [source 1](https://www.aweil.in/units-division?lang=en) |
| `as_type56_sks` | 1956-12-31 | CHI | [source 1](https://www.mod.gov.cn/gfbw/gfjy_index/js_214151/4861522_4.html), [source 2](https://www.xinhuanet.com/mil/2015-10/29/c_128371155.htm), [source 3](https://history.army.mil/Portals/143/Images/Publications/Publication%20By%20Title%20Images/C%20Pdf/combat-staying-the-course.pdf) |
| `as_type56_ak` | 1956-12-31 | CHI | [source 1](https://www.xinhuanet.com/mil/2015-10/29/c_128371155.htm), [source 2](https://history.army.mil/Portals/143/Images/Publications/Publication%20By%20Title%20Images/C%20Pdf/combat-staying-the-course.pdf), [source 3](https://www.awm.gov.au/collection/C320541) |
| `as_ak47_nk` | 1969-12-31 | SOV | [source 1](https://nautilus.org/wp-content/uploads/2012/01/c_sixtyninevol2.pdf), [source 2](https://history.state.gov/historicaldocuments/frus1969-76v19p1/d34) |
| `as_m1_garand` | 1969-12-31 | USA | [source 1](https://nautilus.org/wp-content/uploads/2012/01/c_sixtyninevol2.pdf), [source 2](https://history.state.gov/historicaldocuments/frus1961-63v17/d248) |
| `as_m16` | 1968-12-31 | USA | [source 1](https://www.nas.gov.sg/archivesonline/data/pdfdoc/MINDEF_19991029002_1.pdf), [source 2](https://www.govinfo.gov/content/pkg/CHRG-90shrg77668/pdf/CHRG-90shrg77668.pdf), [source 3](https://history.army.mil/portals/143/Images/Publications/catalog/90-15-1.pdf) |
| `as_g3` | 1967-12-31 | GER | [source 1](https://dserver.bundestag.de/btd/17/022/1702207.pdf), [source 2](https://oka.gov.tr/assets/upload/dosyalar/72corum-savunma-sanayi-raporu_v2.pdf), [source 3](https://collectorssource.ca/product/39927/) |
| `as_t57` | 1968-12-31 | USA | [source 1](https://gpwd.mnd.gov.tw/filectrl/%E5%9C%8B%E9%98%B2%E7%A7%91%E6%8A%80_%E5%A4%A7%E5%AD%B8%E6%9A%A8%E5%9C%A8%E8%81%B7%E6%95%99%E8%82%B2%E6%8E%88%E8%AA%B2%E5%8F%83%E8%80%839_1.pdf), [source 2](https://ahonline.drnh.gov.tw/index.php?act=Archive%2Fsearch%2FeyJxdWVyeSI6W3siZmllbGQiOiJfYWxsIiwidmFsdWUiOiIwMDUtMDEwMjAyLTAwMDMzLTAxMiJ9XX0%3D) |
| `as_ca10` | 1956-12-31 | CHI | [source 1](https://www.fawtrucks-global.com/EN/COMPANY%20NEWS/535.html), [source 2](https://museum.cmes.org/machinery/search/detail/a916a94aa22e427f8496ad4e37a28cd0) |
| `as_bj212` | 1966-12-31 | CHI | [source 1](https://www.212.com.cn/pinpailishi.html) |
| `as_jonga` | 1969-12-31 | JAP | [source 1](https://www.avnl.co.in/vehicle-factory-jabalpur), [source 2](https://www.nissan-global.com/EN/COMPANY/90ANNIVERSARY/) |
| `as_shaktiman` | 1969-12-31 | GER | [source 1](https://www.avnl.co.in/vehicle-factory-jabalpur) |
| `as_mitsubishi_jeep` | 1953-12-31 | USA | [source 1](https://www.mitsubishi-motors.com/en/company/history/car/), [source 2](https://global.toyota/en/mobility/toyota-brand/features/landcruiser/history/evolution/heavy-duty.html), [source 3](https://www.mitsubishi-motors.com/en/newsroom/stories/pajero_development1/index.html) |
| `as_h5` | 1967-12-31 | CHI | [source 1](https://www.sastind.gov.cn/n10086205/n10086403/c10445060/content.html) |
| `as_gnat` | 1965-09-04 | ENG | [source 1](https://www.publicationsdivision.nic.in/journals/Journalarchives/Yojana/Yojana-English/1965/September/Yojana_1965_September_pdf.pdf), [source 2](https://eparlib.sansad.in/bitstream/123456789/62684/1/14_Defence_17.pdf) |
| `as_marut` | 1967-04-01 | RAJ | [source 1](https://www.vayuaerospace.in/Issue/202404031155582676.pdf), [source 2](https://www.publicationsdivision.nic.in/journals/Journalarchives/Yojana/Yojana-English/1965/September/Yojana_1965_September_pdf.pdf), [source 3](https://www.hindustantimes.com/india-news/60-years-of-marut-a-fighter-jet-that-proved-its-worth-in-1971-war-101624129770008.html/) |
| `as_t28d` | 1964-06-27 | USA | [source 1](https://history.state.gov//historicaldocuments/frus1964-68v28/d102), [source 2](https://history.state.gov/historicaldocuments/frus1964-68v28/d160), [source 3](https://www.nationalmuseum.af.mil/Visit/Museum-Exhibits/Fact-Sheets/Display/Article/196029/north-american-t-28b-trojan/) |
| `as_a37b` | 1969-05-31 | USA | [source 1](https://media.defense.gov/2017/Mar/28/2001722972/-1/-1/0/07-ILL_HIST_CH20-BACK_%28PAGES309-383%29.PDF), [source 2](https://www.govinfo.gov/content/pkg/GOVPUB-D301-PURL-gpo126022/pdf/GOVPUB-D301-PURL-gpo126022.pdf) |
| `as_mi4` | 1964-03-21 | SOV | [source 1](https://eparlib.sansad.in/bitstream/123456789/54543/1/lsd_03_07_21-03-1964.pdf) |
| `as_nepal_fal` | 1960-12-31 | BEL | [source 1](https://www.smallarmssurvey.org/sites/default/files/resources/Small-Arms-Survey-2003-Chapter-03-EN.pdf) |

## Country package index

| History tag | Documented design families |
| --- | --- |
| ACE | No independently evidenced package in this pass |
| AFG | `as_t54`, `as_mig17`, `as_mig21f`, `as_il28` |
| ALA | No independently evidenced package in this pass |
| AQY | No independently evidenced package in this pass |
| ARA | No independently evidenced package in this pass |
| ARK | No independently evidenced package in this pass |
| BAN | No independently evidenced package in this pass |
| BDA | No independently evidenced package in this pass |
| BHR | No independently evidenced package in this pass |
| BHU | No independently evidenced package in this pass |
| BLC | No independently evidenced package in this pass |
| BNG | No independently evidenced package in this pass |
| BRM | `as_f86f` |
| BRU | `as_whirlwind10`, `as_bell206` |
| CBD | `as_cambodian_j5` |
| CHI | `as_type59`, `as_j5`, `as_j6`, `as_type033`, `as_anshan`, `as_h6`, `as_type63apc`, `as_j7`, `as_type56_sks`, `as_type56_ak`, `as_ca10`, `as_bj212`, `as_h5` |
| CHS | No independently evidenced package in this pass |
| DRU | No independently evidenced package in this pass |
| ETK | No independently evidenced package in this pass |
| FSA | No independently evidenced package in this pass |
| HAM | No independently evidenced package in this pass |
| HAZ | No independently evidenced package in this pass |
| HEJ | No independently evidenced package in this pass |
| HEZ | No independently evidenced package in this pass |
| HKG | No independently evidenced package in this pass |
| HOU | No independently evidenced package in this pass |
| HRM | No independently evidenced package in this pass |
| IEK | No independently evidenced package in this pass |
| IKR | No independently evidenced package in this pass |
| IND | `as_amx1375`, `as_mig21f`, `as_pasopati`, `as_c130` |
| IRQ | `as_t54`, `as_mig17`, `as_mig21f`, `as_hunter`, `as_il28` |
| ISI | No independently evidenced package in this pass |
| ISR | `as_shot_meteor`, `as_m48a1`, `as_amx1375`, `as_f4e`, `as_mirage3cj`, `as_tclass` |
| JAP | `as_type61`, `as_type60apc`, `as_m101`, `as_m114`, `as_f86f`, `as_f104j`, `as_uh1b_jp`, `as_oshio`, `as_harukaze`, `as_amatsukaze`, `as_m42`, `as_type64_rifle`, `as_mitsubishi_jeep` |
| JOR | `as_m47`, `as_f104a`, `as_hunter` |
| KAC | No independently evidenced package in this pass |
| KAM | No independently evidenced package in this pass |
| KAR | No independently evidenced package in this pass |
| KAS | No independently evidenced package in this pass |
| KHA | No independently evidenced package in this pass |
| KOR | `as_m48a1`, `as_m101`, `as_m114`, `as_f86f`, `as_f5a`, `as_f4d`, `as_m1_garand` |
| KPI | No independently evidenced package in this pass |
| KPS | No independently evidenced package in this pass |
| KPT | No independently evidenced package in this pass |
| KUR | No independently evidenced package in this pass |
| KUW | `as_hunter`, `as_lightning` |
| LAD | No independently evidenced package in this pass |
| LAO | `as_t28d` |
| LEB | `as_mirage3e`, `as_hunter`, `as_alouette3` |
| LOR | No independently evidenced package in this pass |
| MAC | No independently evidenced package in this pass |
| MAN | No independently evidenced package in this pass |
| MAY | `as_cac_sabre` |
| MEG | No independently evidenced package in this pass |
| MLD | No independently evidenced package in this pass |
| MON | `as_t34_85`, `as_mig15bis` |
| NEJ | No independently evidenced package in this pass |
| NEP | `as_nepal_fal` |
| NHN | No independently evidenced package in this pass |
| NKO | `as_mig17`, `as_mig21pfm`, `as_t54`, `as_il28`, `as_ak47_nk` |
| NPM | No independently evidenced package in this pass |
| NUS | No independently evidenced package in this pass |
| OMA | `as_strikemaster` |
| OMG | No independently evidenced package in this pass |
| PAK | `as_m47`, `as_m48a1`, `as_m113`, `as_m101`, `as_m114`, `as_f86f`, `as_f104a`, `as_mirage3e`, `as_hangor`, `as_ghazi`, `as_shahjahan`, `as_b57`, `as_c130`, `as_g3` |
| PAL | No independently evidenced package in this pass |
| PER | `as_m47`, `as_f86f`, `as_f5a`, `as_f4d`, `as_c130`, `as_m1_garand` |
| PHI | `as_f86f`, `as_f5a` |
| PKK | No independently evidenced package in this pass |
| PUK | No independently evidenced package in this pass |
| QAT | No independently evidenced package in this pass |
| QTF | No independently evidenced package in this pass |
| RAJ | `as_vijayanta`, `as_centurion20`, `as_amx1375`, `as_mig21fl`, `as_alouette3`, `as_kalvari`, `as_talwar`, `as_vikrant`, `as_canberra`, `as_1a1_slr`, `as_jonga`, `as_shaktiman`, `as_gnat`, `as_marut`, `as_mi4` |
| ROJ | No independently evidenced package in this pass |
| RYU | No independently evidenced package in this pass |
| SAU | `as_lightning`, `as_c130` |
| SAZ | No independently evidenced package in this pass |
| SHN | No independently evidenced package in this pass |
| SIA | `as_m41a3`, `as_f5a`, `as_t28d` |
| SIK | No independently evidenced package in this pass |
| SIN | `as_amx1375`, `as_alouette3`, `as_m16` |
| SRI | `as_jetprovost` |
| SVN | `as_m41a3`, `as_m113`, `as_m101`, `as_m114`, `as_f5a`, `as_m16`, `as_a37b` |
| SYE | `as_sye_provost`, `as_mig17` |
| SYR | `as_t54`, `as_mig17`, `as_mig21f` |
| TAB | No independently evidenced package in this pass |
| TAI | `as_m41a3`, `as_f86f`, `as_f104a`, `as_f5a`, `as_m42`, `as_t57` |
| TAL | No independently evidenced package in this pass |
| TIB | No independently evidenced package in this pass |
| TIM | No independently evidenced package in this pass |
| TML | No independently evidenced package in this pass |
| TTP | No independently evidenced package in this pass |
| TUR | `as_m47`, `as_m48a1`, `as_m113`, `as_f104g`, `as_f5a`, `as_balao`, `as_c130`, `as_g3` |
| UAE | No independently evidenced package in this pass |
| VIE | `as_m46`, `as_mig17`, `as_mig21f`, `as_type56_sks`, `as_type56_ak` |
| WAA | No independently evidenced package in this pass |
| YEM | `as_t34_85`, `as_mig17` |


## Native MD mobility and protection calibration

The original land designs now use explicit native `tank_nsb_armor_upgrade` and `tank_nsb_engine_upgrade` levels. These are balance-scale choices within the existing MD designer. An armor level adds 7.5% aggregate game armor and costs speed and reliability; an engine level adds 3.5% game speed and costs reliability, fuel and IC. Neither level is a millimetre or horsepower conversion. Chassis, turret, engine and armor modules also contribute to the final result. Real specifications remain in each model's `historical_specs`, with an explicit `native_calibration` rationale.

Shared family levels are T-54/Type 59 armor 1 / engine 1, Meteor Centurion 2 / 0, original petrol M47/M48 3 / 6, T-34-85 1 / 2, M41 1 / 3 and AMX-13 0 / 3. The higher petrol Patton engine level compensates for the native first-generation petrol module's lower initial speed than the diesel module. It does not install a later engine. Existing MD historical variants supply conservative comparison anchors, including Centurion armor 2, T-55 armor 1 and early Leopard armor 1. Existing fallback models use their separate coarse legacy equipment scale; NSB upgrade identifiers are not copied into that unrelated scale.

Physical reference evidence added for this calibration:

- [Saumur T-54 museum record](https://museedesblindes.fr/les_chars/t54/) records the original 520 PS, 36 tonne, 50 km/h family and 200 mm maximum armor reference. Those physical dimensions are not a direct game-armor formula.
- [JGSDF Seventh Division equipment table](https://www.mod.go.jp/gsdf/nae/7d/siryoukan.html) gives Type 61 at approximately 35 tonnes, 570 PS and 45 km/h. Armor 1 / engine 0 is a conservative comparison; no exact thickness is invented from the official table's missing numerical armor data.
- [Taiwan Armour School engine study](https://www.mnd.gov.tw/File/13360), page 7, identifies the original Type 59 12150 diesel at 520 hp. Later 580 hp Type 69 and turbocharged successor engines remain excluded.
- [Bovington's M47 restoration history](https://tankmuseum.org/article/history-of-the-m47) gives the original 810 hp AV-1790 petrol, 46 tonnes and 30 mph, with 4 inch hull/turret fronts and a 4.5 inch gun shield.
- [First Division Museum M48 record](https://www.fdmuseum.org/exhibit/m48-patton-tank/) distinguishes early petrol tanks from the later diesel M48A3. Its original-engine technical table gives 810 hp and 28 mph. Its family-wide overview is not treated as proof of an exact M48A1 maximum armor thickness or local diesel refit.
- [Bendigo RSL's own Australian Mk5/1](https://bendigorsl.com.au/centurion-tank/) identifies its 83.4 mm gun, 650 bhp Meteor Mk4B, 54 tonnes, 35 km/h and 152 mm maximum cast-turret armor. These are specific to that Australian example; its exact weight and protection are not silently copied onto every Centurion mark.
- [Swiss Centurion owner's technical sheet](https://centurion-verein.ch/wp-content/uploads/2023/11/Centurion-Datasheet.pdf) corroborates the original Meteor family's 35 km/h mobility. It is used only for the shared mobility band where a different operator's mark is represented.
- [Contemporary US Army ARMOR, January-February 1953](https://www.benning.army.mil/armor/eARMOR/content/issues/1953/JAN_FEB/1953JanuaryFebruary.pdf) describes the original Walker Bulldog's 500 hp engine and road speed exceeding 40 mph. No later Brazilian diesel or 90 mm upgrade is fitted.
- [Saumur T-34-85 record](https://museedesblindes.fr/les_chars/t34_85/) gives 500 PS, 32 tonnes and 55 km/h for the original family. Museum maximum armor figures differ between examples; no exact maximum thickness is asserted for the Cuban tank.

Vijayanta remains a clearly marked conservative armor 1 / engine 1 baseline. The manufacturer establishes the original Vickers family and period. Exact numerical protection and mobility have not been established from accessible primary material in this pass, so no unsupported precision or later Bison conversion is added. The shared native bands provide differentiated starting designs, while their final combat values remain an MD game abstraction requiring native inspection and playtesting.


## Additional real-state coverage

Mongolia receives the original T-34-85 and a conservative MiG-15 gun-fighter family. The [Spanish Air Ministry's November 1968 force survey](https://publicaciones.defensa.gob.es/media/downloadable/files/links/r/a/raa_336.pdf), printed page 877, lists Mongolian T-34s and six MiG-15 combat aircraft. Its two-column OCR interleaves North Korean equipment with the Mongolian section; the 800 tank total and PT-76/T-54/T-55 list belong to North Korea and are not treated as a Mongolian inventory. The [US Air Force Museum MiG-15bis](https://www.nationalmuseum.af.mil/Visit/Museum-Exhibits/Fact-Sheets/Display/Article/196115/mikoyan-gurevich-mig-15bis/) supplies the representative swept-wing, single non-afterburning turbojet and 23/37 mm cannon fit. The source inventory does not establish an individual Mongolian subvariant or serial. Soviet aircraft and tanks stationed in Mongolia do not become Mongolian-owned equipment. Later MiG-21 deliveries and modern tank packages remain excluded; the T-54 acquisition date was not independently established from accessible primary material in this pass.

North Yemen receives the original T-34-85 and MiG-17 family. [DIA's June 21, 1963 memorandum](https://history.state.gov/historicaldocuments/frus1961-63v18/d278) explicitly describes T-34 shipments under the 1956 agreement and warns that much equipment deteriorated in storage. The design entry establishes available historical hardware, with no assertion that every tank was operational or present in a starting unit. A [June 1967 US diplomatic report](https://history.state.gov/historicaldocuments/frus1964-68v19/d266) identifies MiG-17 aircraft in Yemen; Egyptian assistance and airframes in theatre do not establish an independent Yemeni production industry. A [contemporary December 4, 1969 intelligence note](https://history.state.gov/historicaldocuments/frus1969-76v24/d176) directly identifies South Yemen's MiG-17s, Arab pilots and Soviet training assistance, so that existing family is also added to South Yemen. MiG-21 and uncertain T-54 assumptions remain excluded from these added packages.
