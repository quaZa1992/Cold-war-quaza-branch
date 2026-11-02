IMPERIA COLD WAR: European and Soviet historical equipment variants for 1 January 1970

Original historical synthesis and native-MD design mapping prepared for this project. No photographs, technical drawings, source prose or external game data are reproduced. Source authors retain their rights; source licence/permission is unknown unless the source expressly specifies otherwise. JSON contains only names, historical facts, original design choices and references.

Coverage: 132 country/releasable tags, 212 shared representative models. Empty packages deliberately avoid creating an autonomous1970 military programme for later Soviet/Yugoslav/European releases, microstates, or jurisdictions without a coherent documented national package. These designs do not assert inventory quantities, operational readiness or domestic massproduction. Imported equipment retains the original designer nation.

The cutoff is strict: actual service/delivery before1970, not merely first flight, order, licensed-production agreement or later fleet status. service_by is a conservative calendar-year upper bound, not an invented exact commissioning day. The resulting design catalogue is representative, not an exhaustive serial/subvariant inventory.

Native abstraction limits: calibre classes, suspension families, aircraft-size classes and naval gun categories are coarse. Notes identify approximations. Original engines, conventional armour, loading method and original sensors are retained where the available modules permit. No universal laser/thermal sight, ERA, composite armour, modern guided shell, digital control, MIO bonus or full producer research package is copied from2000history.

Designer availability: NSB modular ground/helicopter designs have fixed-model fallbacks; BBA modular fixed-wing designs have legacy fallbacks. The compiler must unlock an actually operated bare chassis/airframe/hull before its modular variant, because allow_without_tech alone does not create required bare-hull ordering. Towed artillery/infantry/utility equipment remains native static equipment.

Native runtime correction: primary aircraft modules override the equipment role. The manifest uses actual MD CAS, interceptor, carrier, maritime-patrol and transport derivatives matching that primary module, rather than selecting only a compatible slot layout. Prefix-correct copies of the existing early airframes allow MD_x_plane_airframes.txt to generate its real role derivatives, preserving the donors' historical numerical values and slots. The service bundle unlocks the exact derived role and its bare frame before creation. See role_frames_notice.md for source attribution and the native diagnostic basis.

Specific corrected donor errors: Shilka uses early23mm systems and impact ammunition, not1985autocannon/proximity ammunition. Abbot is manually loaded105mm. AMX13F3 is an open manually loaded155mm installation with original petrol power. Chieftain has conventional steel armour, while T64A alone among these models receives documented composite armour and an autoloader. M47/M48 retain90mm, rather than being silently upgunned to105mm.

Naval exceptions: only the actual sixteen-tube Resolution/Project667A ballistic boats use nominal1975subVLS/ammunition modules as a physicaltube/capacity abstraction. module_exceptions records dated evidence and does not authorize1975research or future missiles. EarlySAM modules on Volna/Seaslug/Masurca/Tartar ships denote earlynavalairdefence function, not an American Terrierexport. No missileboat is inflated to a corvette/frigate, and no Exocet/Harpoon/SeaWolf/SeaSparrowlaterrefit is copied. Moskva has a1967service exception to the coarse native1970helicopterhull label.

Known omitted families: many minesweepers, coastal patrol boats, fast attack boats, monitors, dedicated reconnaissance and maritime-patrol subvariants cannot be represented faithfully by the available hull and airframe modules. The manifest leaves these unmodeled. Finnish Turunmaa is omitted because no early gun battery fits the corvette mandatory slot. Its hull is not enlarged to a frigate. French Etendard IVM and F8E(FN), British Phantom FG1 and Buccaneer S2 use actual carrier-capable frames; no land-only airframe is presented as carrier-compatible.

National limits: no BelgianMirage5 before1971; no AustrianSaab105 beforeJuly1970; no DanishDraken beforelater1970; no FinnishDraken before1972 or Mi8 before1973; no SpanishF5/AMX30 beforelater1970; no Marder1971, Viggen1971, RomanianIAR3161971, T72, T80, M80IFV, Gazelle, Mi24 or post1969 navalrefit. DDRBMP1 trials before1970 are not treated as a normal operational fleet. ItalianLeopard1 delivery began afterthecutoff.

Dutch Leopard1 inclusion has a narrow dated basis: the Netherlands Institute of Military History records the first manufacturer handover in late1969. The shared original Leopard1 model therefore belongs in the Dutch January1970 design catalogue. This does not establish that all468 ordered tanks had arrived, a fully equipped operational fleet, or the later Leopard1V configuration. Primary source: https://www.nimh.nl/onderwerpen/d/de-leopard-1

Sources and reasoning

- weg: https://cgsc.contentdm.oclc.org/digital/api/collection/p4013coll11/id/2089/download
- t64: https://115ombr.mil.gov.ua/t-64/
- bmp: https://www.army.mil/article-amp/220341/ria_self_guided_tour_bmp_1_armored_personnel_carrier
- m113: https://armyhistory.org/m113-armored-personnel-carrier/
- ot64: https://www.mo.gov.cz/scripts/detail.php?id=6042
- pbv: https://www.arsenalen.se/fordonsregister/pansarbandvagn-pbv-302/
- strv: https://www.saab.com/newsroom/stories/2019/may/artillery-pieces-and-combat-vehicles
- cent: https://collectie.nmm.nl/nl/collectie/detail/270881/
- chieftain: https://ejercito.defensa.gob.es/en/unidades/Madrid/muma/Noticias/2014/CHIEFTAIN.html
- m47: https://tankmuseum.org/article/m47
- fv432: https://tankmuseum.org/tank-nuts/tank-collection/bulldog
- amx13: https://www.servicehistorique.sga.defense.gouv.fr/es/node/46264
- amx30: https://www.senat.fr/rap/1967-1968/i1967_1968_0016_03_36.pdf
- leopard: https://www.bundeswehr.de/de/ausruestung-technik-bundeswehr/kampfpanzer-leopard-versionen-bundeswehr
- mig17: https://www.nationalmuseum.af.mil/Visit/Museum-Exhibits/Fact-Sheets/Display/Article/196057/mikoyan-gurevich-mig-17f/
- mig21: https://www.aftc.af.mil/News/On-This-Day-in-Test-History/Article-Display-Test-History/Article/2458475/january-23-1968-flight-test-center-examines-soviet-mig-21/
- phantom: https://www.raf.mod.uk/what-we-do/our-history/air-historical-branch/regional-studies-post-coldwar-narratives/developments-in-air-defence-1945-1970/
- vulcan: https://www.rafmuseum.org.uk/research/collections/avro-vulcan-b2/
- wessex: https://www.rafmuseum.org.uk/research/collections/westland-wessex-hc2/
- seaking: https://www.royalnavy.mod.uk/news/2016/february/19/120219-life-saving-sea-king-to-go-on-public-display
- navyuk: https://hansard.parliament.uk/Commons/1963-03-11/debates/a9449801-d866-430b-a230-8ed5f76ead93/NavyEstimates1963%E2%80%9364
- polaris: https://www.gov.uk/government/publications/the-uks-nuclear-deterrent-what-you-need-to-know/the-uks-nuclear-deterrent-the-national-endeavour-explained
- italianavy: https://www.marina.difesa.it/noi-siamo-la-marina/pilastro-operativo/mezzi/mezzi-storici/Pagine/ABCD/andrea_doria_incrociatore.aspx
- nlnavy: https://www.defensie.nl/defensieonderdelen/koninklijke-marine/eenheden/schepen/zr-ms-van-speijk
- marina: https://www.marina.difesa.it/media-cultura/editoria/marivista/Documents/supplementi/Supplemento_Settembre_2022.pdf
- mirage: https://www.dassault-aviation.com/en/passion/aircraft/military-dassault-aircraft/mirage-iii/
- mirage4: https://www.dassault-aviation.com/en/passion/aircraft/military-dassault-aircraft/mirage-iv/
- saabhistory: https://www.saab.com/about/company-in-brief/history
- luftwaffe: https://www.bundeswehr.de/en/about-bundeswehr/history/history-german-air-force
- alouette: https://www.museehelico-alat.com/visite-virtuelle/alouette-ii-artouste
- alouette3: https://www.airbus.com/en/newsroom/stories/2019-02-the-60th-anniversary-of-the-alouette-iii
- mi8: https://muzeumlotnictwa.pl/en/exhibits/mil-mi-8-2/
- nf5: https://www.erfgoednlr.nl/pdf/75_years_NLR_deel_1.pdf
- an2: https://www.museumofflight.org/Exhibits-and-Events/Aircraft/antonov-2-colt
- raf69: https://www.rafmuseum.org.uk/research/research-enquiries/history-of-aviation-timeline/british-military-aviation/1969-2/
- sovsurface: https://www.usni.org/magazines/proceedings/1969/july/pictorial-soviet-surface-combatants
- sovsubs: https://www.usni.org/magazines/proceedings/1971/august/pictorial-soviet-submarine-force
- kashin: https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/Other/K-61315.html
- resolution: https://www.royalnavy.mod.uk/news/2017/june/22/170622-submarine-console-is-given-a-new-lease-of-life
- dolfijn: https://www.defensie.nl/defensieonderdelen/koninklijke-marine/eenheden/schepen/zr-ms-dolfijn
- impavido: https://www.marina.difesa.it/noi-siamo-la-marina/pilastro-operativo/mezzi/mezzi-storici/Pagine/EFGHI/impavido02.aspx
- clemenceau: https://www.servicehistorique.sga.defense.gouv.fr/ark/954925
- frnavy: https://www.senat.fr/rap/1965-1966/i1965_1966_0034_05.pdf
- etendard: https://www.dassault-aviation.com/en/passion/aircraft/military-dassault-aircraft/etendard/
- f8fn: https://www.irsem.fr/storage/file_manager_files/2025/03/1-tomes-bonnet-v8.pdf
- ak: https://kalashnikov.media/birthday/
- g3: https://www.hkdefense.us/corporate/history.html
- l1a1: https://www.rmg.co.uk/collections/objects/rmgc-object-252104
- stgw: https://www.sigsauer.swiss/de/ueber-uns.php
- rk62: https://www.sako.global/article/sako-history-highlights-by-year
- vz58: https://acr.mo.gov.cz/assets/sa58.pdf
- bm59: https://www.indaginibalistiche.it/utlities/manuali/beretta_bm59_IT_EN_FR_DE.pdf
- m59: https://muzej-policije.gov.hr/zbirke-30/zbirka-oruzja/podzbirka-vatreno-oruzje/vojnicke-puske/200?big=1
- ireair: https://www.military.ie/en/public-information/defence-forces-museums/defence-forces-history/history-of-the-air-corps/
- garand: https://marinehist.dk/orlogsbib/f/folkogvaern/1951-FogV.pdf
- fal: https://fnbrowninggroup.com/app/uploads/2025/09/250924_HerstalGroup_HabillageUsine_Timeline_V1-1.pdf
- cetme: https://artsandculture.google.com/asset/cetme-model-c-assault-rifle-oviedo-factory-of-weapons/vQFf6rTFRjHKGg?hl=en
- unimog: https://www.hasmer.mercedes-benz-trucks.com/int/en/experience/heritage/unimog-1956-1965-complete-programme.html
- landrover: https://www.lrheritagecollection.org.uk/the-collection/series-ii/
- jastreb: https://www.muzejvazduhoplovstva.mod.gov.rs/eng/289/j-21-jastreb-289
- galeb: https://www.muzejvazduhoplovstva.mod.gov.rs/eng/248/soko-g-2-galeb-248
- m60austria: https://www.bmlv.gv.at/cms/artikel.php?ID=2203
- austriahowitzer: https://www.parlament.gv.at/dokument/XVIII/III/146/imfname_547596.pdf
- hamburg: https://www.zerstoerer-hamburg.de/hamburg/klasse
- pederskram: https://navalhistory.dk/_pdfFiler/StillingsBeretning.pdf
- kobben: https://www.forsvarshistoriskmuseum.no/utstillinger/museumsubaten-utstein
- delfinen: https://springeren-maritimt.dk/en/submarine-springeren/
- type205: https://www.marinemuseum.de/2021_unsere-staendigen-ausstellungen/2021_u-10/
- lutjens: https://www.marinemuseum.de/50-jahre-moelders/
- albacora: https://cultura.marinha.pt/pt/museumarinha_web/multimedia_web/Paginas/efemeride-submarinho-albacora-lancado-agua-13out20.aspx
- joaobelo: https://www.marinha.pt/conteudos_externos/Revista_Armada/PDF/2003/RA2003.pdf
- heroj: https://www.brodosplit.hr/hr/brodogradnja/vojni-program/
- dedalo: https://armada.defensa.gob.es/archivo/mardigitalrevistas/cuadernosihcn/77cuaderno/cm77.pdf
- moskva: https://www.history.navy.mil/our-collections/photography/numerical-list-of-images/nhhc-series/nh-series/USN-1134000/USN-1134890.html
- s75: https://www.nationalmuseum.af.mil/Visit/Museum-Exhibits/Fact-Sheets/Display/Article/196037/sa-2-surface-to-air-missile/
- hawk: https://history.redstone.army.mil/miss-hawk.html
- bloodhound: https://api.parliament.uk/historic-hansard/written-answers/1987/may/05/bloodhound
- nikedate: https://history.redstone.army.mil/ihist-vigil.html
- denmarksam: https://www.forsvaret.dk/da/organisation/flyvevaabnet/air-defence-wing/historie/
- germansam: https://zms.bundeswehr.de/de/mediathek/zmsbw-aktuelle-karte-luftverteidigung-5509524
- swedishsam: https://fht.nu/Dokument/Flygvapnet/flyg_publ_dok_strilsystemdokument.pdf
- koln: https://www.fregatte-koeln.de/Haupt-Koeln/haupt-englisch.htm
- valiant: https://thedockyard.co.uk/news/warship-wednesday-hms-valiant-the-first-nuclear-submarine-to-be-refitted-and-refuelled-at-chatham/

Country packages

- ABK (Abkhazia): No independent historical variant package assigned.
- ADJ (Adjara): No independent historical variant package assigned.
- ADO (Andorra): No independent historical variant package assigned.
- ADY (Adygea): No independent historical variant package assigned.
- ALB (Albania): Type 56, AK-47, GAZ-69, T-34-85, T-54B, Type 59, BTR-152, 122mm M-30, RPG-2, 57mm S-60, MiG-17F, MiG-21F-13, Shenyang J-6, Antonov An-2, Mil Mi-4, Project 613 Whiskey
- ALT (Altai): No independent historical variant package assigned.
- ARM (Armenia): No independent historical variant package assigned.
- AUS (Austria): FN FAL, Unimog 404S, M47 Patton, M60A1, AMX-13/75, Saurer 4K 4FA, M109 155mm, 105mm M101A1, Bofors 40mm L/70, Saab J 29F Tunnan, SE.3130 Alouette II, Bell 47G, Carl Gustaf m/48
- AZE (Azerbaijan): No independent historical variant package assigned.
- BAY (Bavaria): No independent historical variant package assigned.
- BEL (Belgium): FN FAL, Land Rover Series IIA, Leopard 1, M47 Patton, M75 APC, AMX-VCI, M109 155mm, 105mm M101A1, 155mm M114, M20 Super Bazooka, Bofors 40mm L/70, F-104G Starfighter, F-84F Thunderstreak, Fairchild C-119G, SE.3130 Alouette II, MIM-23A Basic HAWK, MIM-14 Nike Hercules
- BLR (Belarus): No independent historical variant package assigned.
- BOS (Bosnia): No independent historical variant package assigned.
- BRY (Buryatia): No independent historical variant package assigned.
- BSH (Bashkiria): No independent historical variant package assigned.
- BUL (Bulgaria): AKM, GAZ-69, ZIL-157, T-34-85, T-54B, T-55A, BTR-60PB, BTR-152, BRDM-2, PT-76B, 122mm D-30, 152mm D-20, 130mm M-46, 122mm M-30, BM-21 Grad, ZSU-57-2, RPG-2, RPG-7, 57mm S-60, ZU-23-2, MiG-17F, MiG-19S, MiG-21F-13, Ilyushin Il-14, Antonov An-2, Mil Mi-4, Mil Mi-8T, Project 50 Riga, Project 613 Whiskey, S-75 Dvina
- CAT (Catalonia): No independent historical variant package assigned.
- CHE (Chechnya): No independent historical variant package assigned.
- CHU (Chuvashia): No independent historical variant package assigned.
- CKK (Chukotka): No independent historical variant package assigned.
- CNR (Canary Islands): No independent historical variant package assigned.
- CRE (Crete): No independent historical variant package assigned.
- CRM (Crimea): No independent historical variant package assigned.
- CRO (Croatia): No independent historical variant package assigned.
- CSB (Central Siberia): No independent historical variant package assigned.
- CYP (Cyprus): 7.62mm samopal vz.58, T-34-85, BTR-152, Ordnance QF 25-pounder, M20 Super Bazooka
- CZE (Czech Republic): 7.62mm samopal vz.58, GAZ-69, T-34-85, T-54B, T-55A, OT-64A SKOT, OT-62 TOPAS, BRDM-2, PT-76B, 122mm D-30, 152mm D-20, 130mm M-46, 122mm M-30, RPG-2, RPG-7, 57mm S-60, ZU-23-2, MiG-17F, MiG-21F-13, MiG-21PFM, Aero L-29 Delfin, Ilyushin Il-14, Antonov An-2, Mil Mi-4, Mil Mi-8T, S-75 Dvina
- DAG (Dagestan): No independent historical variant package assigned.
- DDR (East Germany): AKM, GAZ-69, ZIL-157, T-34-85, T-54B, T-55A, BTR-60PB, BTR-152, BTR-50PK, BRDM-2, PT-76B, 122mm D-30, 152mm D-20, 130mm M-46, BM-21 Grad, ZSU-23-4 Shilka, ZSU-57-2, RPG-2, RPG-7, 57mm S-60, ZU-23-2, MiG-17F, MiG-21F-13, MiG-21PFM, Ilyushin Il-14, Antonov An-2, Mil Mi-4, Mil Mi-8T, Project 50 Riga, S-75 Dvina
- DEN (Denmark): M1 Garand, Land Rover Series IIA, Centurion Mk 5/2, M113, M109 155mm, 105mm M101A1, 155mm M114, Carl Gustaf m/48, Bofors 40mm L/70, F-104G Starfighter, F-100D Super Sabre, Douglas C-54 Skymaster, SA.3160 Alouette III, Peder Skram class, Delfinen class, MIM-23A Basic HAWK, MIM-14 Nike Hercules
- DON (Don): No independent historical variant package assigned.
- DPR (Donetsk People's Republic): No independent historical variant package assigned.
- DRP (Dnipro People's Republic): No independent historical variant package assigned.
- ENG (United Kingdom): L1A1 SLR, Land Rover Series IIA, Centurion Mk 5/2, Chieftain Mk 2, FV432 Mk 2, FV601 Saladin, Daimler Ferret, FV433 Abbot, M109 155mm, Ordnance QF 25-pounder, 105mm L5 Pack Howitzer, Carl Gustaf m/48, Bofors 40mm L/70, English Electric Lightning F.6, Phantom FG.1, Harrier GR.1, Hunter FGA.9, Buccaneer S.2, Canberra B.6, Avro Vulcan B.2, Hercules C.1 (C-130K), Westland Wessex HC.2, Westland Scout AH.1, Westland Sea King HAS.1, Leander class, County class, Daring class, Audacious class, Oberon class, Valiant class, Resolution class, Bloodhound Mk II
- ESB (Eastern Siberia): No independent historical variant package assigned.
- EST (Estonia): No independent historical variant package assigned.
- EUU (EU): No independent historical variant package assigned.
- FAO (Faroe Islands): No independent historical variant package assigned.
- FAR (Far Eastern Republic): No independent historical variant package assigned.
- FIN (Finland): Valmet RK 62, AK-47, GAZ-69, T-34-85, T-54B, T-55A, Comet Mk I, BTR-50PK, PT-76B, 122mm D-30, 130mm M-46, 122mm M-30, Carl Gustaf m/48, 57mm S-60, ZU-23-2, MiG-21F-13, Folland Gnat F.1, Douglas C-47 Dakota, Mil Mi-4, Bell 47G, Hameenmaa class
- FLN (Flanders): No independent historical variant package assigned.
- FRA (France): MAS 49/56, AMX-30B, AMX-13/75, AMX-13/90, AMX-VCI, Panhard AML 60, Panhard AML 90, Panhard EBR 75, AMX-13 F3, AMX-13 DCA, 105mm Modele 1950, 155mm M114, M20 Super Bazooka, Bofors 40mm L/70, Mirage IIIC, Mirage IIIE, Mirage IVA, Nord N.2501 Noratlas, Transall C-160, SE.3130 Alouette II, SA.3160 Alouette III, SA.330B Puma, Clemenceau class, Suffren class, T 47 Surcouf class, Commandant Riviere class, Daphne class, Etendard IVM, F-8E(FN) Crusader, MIM-23A Basic HAWK
- FYR (Macedonia): No independent historical variant package assigned.
- GAL (Galicia): No independent historical variant package assigned.
- GEO (Georgia): No independent historical variant package assigned.
- GER (Germany): Heckler & Koch G3, Unimog 404S, Leopard 1, M48A2 Patton, Schutzenpanzer lang HS 30, M113A1, M109G, M42 Duster, 105mm M101A1, 155mm M114, M20 Super Bazooka, Bofors 40mm L/70, F-104G Starfighter, Fiat G.91R/3, Nord N.2501 Noratlas, Transall C-160, Bell UH-1D Iroquois, SE.3130 Alouette II, Hamburg class, Lutjens class, Koln class, Type 205, MIM-23A Basic HAWK, MIM-14 Nike Hercules
- GGZ (Gagauzia): No independent historical variant package assigned.
- GOR (Gorskaya Republic): No independent historical variant package assigned.
- GRE (Greece): M1 Garand, Land Rover Series IIA, M47 Patton, M48A1 Patton, M113, M52 105mm, M42 Duster, 105mm M101A1, 155mm M114, M20 Super Bazooka, Bofors 40mm L/70, F-104G Starfighter, Northrop F-5A Freedom Fighter, F-84F Thunderstreak, Douglas C-47 Dakota, Bell 47G, Fletcher class, Balao class, MIM-23A Basic HAWK, MIM-14 Nike Hercules
- GRN (Greenland): No independent historical variant package assigned.
- HLS (Holy See): No independent historical variant package assigned.
- HOL (Holland): FN FAL, Land Rover Series IIA, Leopard 1, Centurion Mk 5/2, AMX-13/75, DAF YP-408, AMX-VCI, M109 155mm, 105mm M101A1, 155mm M114, M20 Super Bazooka, Bofors 40mm L/70, F-104G Starfighter, F-84F Thunderstreak, Canadair NF-5A, Douglas C-47 Dakota, SA.3160 Alouette III, Friesland class, Van Speijk class, Dolfijn class, MIM-23A Basic HAWK, MIM-14 Nike Hercules
- HPR (Harkov): No independent historical variant package assigned.
- HUN (Hungary): AKM-63, GAZ-69, T-34-85, T-54B, T-55A, BTR-60PB, 122mm D-30, 122mm M-30, RPG-2, RPG-7, 57mm S-60, ZU-23-2, MiG-17F, MiG-21F-13, Antonov An-2, Mil Mi-4, Mil Mi-8T, S-75 Dvina
- HZG (Herzegovinian): No independent historical variant package assigned.
- ICE (Iceland): No independent historical variant package assigned.
- ING (Ingushetia): No independent historical variant package assigned.
- IOM (Isle of Mann): No independent historical variant package assigned.
- IRE (Ireland): FN FAL, Land Rover Series IIA, Comet Mk I, FV601 Saladin, Daimler Ferret, Panhard AML 60, Panhard AML 90, Ordnance QF 25-pounder, Carl Gustaf m/48, Bofors 40mm L/70, Vampire T.55, SA.3160 Alouette III
- ITA (Italy): Beretta BM59, Unimog 404S, M47 Patton, M60A1, M113, M113A1, M109 155mm, M7B2 Priest, 105mm M101A1, 155mm M114, 105mm L5 Pack Howitzer, M20 Super Bazooka, Bofors 40mm L/70, F-104G Starfighter, Fiat G.91R/1, Canadair Sabre Mk.4 (F-86E(M)), Fairchild C-119G, Douglas C-47 Dakota, Bell UH-1B Iroquois, Bell UH-1D Iroquois, Bell 47G, Impavido class, Andrea Doria class, Carlo Bergamini class, Enrico Toti class, MIM-23A Basic HAWK, MIM-14 Nike Hercules
- KAE (Karelia): No independent historical variant package assigned.
- KAZ (Kazakhstan): No independent historical variant package assigned.
- KBK (Kabardino Balkaria): No independent historical variant package assigned.
- KCC (Karachay Cherkessia): No independent historical variant package assigned.
- KHM (Khanty-Mansi): No independent historical variant package assigned.
- KHS (Khakassia): No independent historical variant package assigned.
- KLM (Kalmykia): No independent historical variant package assigned.
- KOM (Komi): No independent historical variant package assigned.
- KOS (Kosovo): No independent historical variant package assigned.
- KRP (Karakalpakstan): No independent historical variant package assigned.
- KSH (Kashubia): No independent historical variant package assigned.
- KUB (Kuban Republic): No independent historical variant package assigned.
- KYR (Kyrgyzstan): No independent historical variant package assigned.
- LAG (Latgale): No independent historical variant package assigned.
- LAT (Latvia): No independent historical variant package assigned.
- LIC (Liechenstein): No independent historical variant package assigned.
- LIT (Lithuania): No independent historical variant package assigned.
- LPR (Lugansk People's Republic): No independent historical variant package assigned.
- LUX (Luxemburg): FN FAL, Land Rover Series IIA, M20 Super Bazooka
- MEL (Mari El): No independent historical variant package assigned.
- MLR (Malorossiya): No independent historical variant package assigned.
- MLT (Malta): L1A1 SLR, Land Rover Series IIA, Bofors 40mm L/70
- MLV (Moldova): No independent historical variant package assigned.
- MNC (Monaco): No independent historical variant package assigned.
- MNT (Montenegro): No independent historical variant package assigned.
- MOV (Mordovia): No independent historical variant package assigned.
- NAV (Basque Country): No independent historical variant package assigned.
- NCY (Northern Cyprus): No independent historical variant package assigned.
- NEE (Nenets): No independent historical variant package assigned.
- NIR (Northern Ireland): No independent historical variant package assigned.
- NKR (Artsakh): No independent historical variant package assigned.
- NOV (Novorossiya): No independent historical variant package assigned.
- NRY (Norway): Heckler & Koch G3, Land Rover Series IIA, M48A2 Patton, M113, M109 155mm, 105mm M101A1, 155mm M114, Carl Gustaf m/48, Bofors 40mm L/70, F-104G Starfighter, Northrop F-5A Freedom Fighter, Fairchild C-119G, C-130H Hercules, Bell UH-1B Iroquois, Oslo class, Kobben class, M1 Garand, MIM-14 Nike Hercules
- OPR (Odessa): No independent historical variant package assigned.
- PMR (Transnistria): No independent historical variant package assigned.
- POL (Poland): AKM, GAZ-69, ZIL-157, T-34-85, T-54B, T-55A, OT-64A SKOT, OT-62 TOPAS, BRDM-2, PT-76B, 122mm D-30, 152mm D-20, 130mm M-46, 122mm M-30, BM-21 Grad, ZSU-23-4 Shilka, ZSU-57-2, RPG-2, RPG-7, 57mm S-60, ZU-23-2, MiG-17F, MiG-21F-13, MiG-21PFM, Lim-6bis, Antonov An-2, Ilyushin Il-14, Mil Mi-2, Mil Mi-4, Mil Mi-8T, Project 30bis Skory, Project 613 Whiskey, S-75 Dvina
- POR (Portugal): Heckler & Koch G3, Land Rover Series IIA, M47 Patton, Daimler Ferret, Panhard AML 60, Panhard AML 90, 105mm M101A1, 155mm M114, Ordnance QF 25-pounder, M20 Super Bazooka, Bofors 40mm L/70, Fiat G.91R/4, F-86F Sabre, Nord N.2501 Noratlas, Douglas C-47 Dakota, SA.3160 Alouette III, SA.330B Puma, Joao Belo class, Albacora class
- ROM (Romania): PM md.63, GAZ-69, T-34-85, T-55A, BTR-60PB, 152mm D-20, 130mm M-46, 122mm M-30, RPG-2, RPG-7, 57mm S-60, ZU-23-2, MiG-17F, MiG-19S, MiG-21F-13, Ilyushin Il-14, Antonov An-2, Mil Mi-4, Mil Mi-8T, S-75 Dvina
- RSK (Republika Srpska): No independent historical variant package assigned.
- RUS (Lokot Republic): No independent historical variant package assigned.
- SAR (Sardinia): No independent historical variant package assigned.
- SCL (Padania): No independent historical variant package assigned.
- SCO (Scotland): No independent historical variant package assigned.
- SER (Serbia): Zastava M59/66, GAZ-69, T-34-85, T-55A, M47 Patton, M-60 armoured personnel carrier, BTR-50PK, M7B2 Priest, 105mm M101A1, 155mm M114, 122mm M-30, 130mm M-46, RPG-2, M20 Super Bazooka, Bofors 40mm L/70, MiG-21F-13, Canadair Sabre Mk.4 (F-86E(M)), F-84F Thunderstreak, Soko G-2 Galeb, Soko J-21 Jastreb, Douglas C-47 Dakota, Mil Mi-4, Mil Mi-8T, Heroj class, Mil Mi-2
- SEU (South-Eastern Ukrainian Autonomous Republic): No independent historical variant package assigned.
- SIB (Siberian Republic): No independent historical variant package assigned.
- SIL (Silesia): No independent historical variant package assigned.
- SLO (Slovakia): No independent historical variant package assigned.
- SLV (Slovenia): No independent historical variant package assigned.
- SMA (San Marino): No independent historical variant package assigned.
- SOO (South Ossetia): No independent historical variant package assigned.
- SOV (Russia): AKM, AK-47, GAZ-69, ZIL-157, T-34-85, T-54B, T-55A, T-62, T-64A, BMP-1, BTR-60PB, BTR-152, BTR-50PK, BRDM-2, PT-76B, 122mm D-30, 152mm D-20, 130mm M-46, 122mm M-30, BM-21 Grad, ZSU-23-4 Shilka, ZSU-57-2, RPG-2, RPG-7, 57mm S-60, ZU-23-2, 9K32 Strela-2, MiG-17F, MiG-19S, MiG-21F-13, MiG-21PFM, Su-7B, Tu-128, Tu-16, Tu-95M, Antonov An-12, Ilyushin Il-14, Antonov An-2, Mil Mi-4, Mil Mi-8T, Mil Mi-2, Project 61 Kashin, Project 56 Kotlin, Project 159 Petya, Project 68bis Sverdlov, Project 1123 Moskva, Project 641 Foxtrot, Project 613 Whiskey, Project 633 Romeo, Project 671 Victor I, Project 667A Yankee I, S-75 Dvina
- SPA (Andalusia): No independent historical variant package assigned.
- SPR (Spain): CETME Modelo C, Land Rover Series IIA, M47 Patton, M48A1 Patton, M113, M7B2 Priest, M37 105mm, 105mm M101A1, 155mm M114, M20 Super Bazooka, Bofors 40mm L/70, F-104G Starfighter, F-86F Sabre, Hispano HA-200 Saeta, Douglas C-47 Dakota, Douglas C-54 Skymaster, Bell UH-1B Iroquois, SA.3160 Alouette III, Fletcher class, Balao class, Dedalo (ex-USS Cabot)
- SWE (Sweden): Automatkarbin 4, Land Rover Series IIA, Centurion Mk 5/2, Stridsvagn 103A, Stridsvagn 74, Pansarbandvagn 302, Bandkanon 1A, Carl Gustaf m/48, Bofors 40mm L/70, Saab J 35F Draken, Saab A 32A Lansen, Saab J 29F Tunnan, Lockheed C-130E Hercules, SE.3130 Alouette II, Ostergotland class, Draken class, MIM-23A Basic HAWK, Bloodhound Mk II
- SWI (Switzerland): Sturmgewehr 57, Unimog 404S, Centurion Mk 5/2, Panzer 61, AMX-13/75, M113, 105mm M101A1, Bofors 40mm L/70, Hunter Mk.58, Mirage IIIS, SE.3130 Alouette II, SA.3160 Alouette III, Bloodhound Mk II
- TAJ (Tajikistan): No independent historical variant package assigned.
- TAT (Tatarstan): No independent historical variant package assigned.
- TLS (Talishstan): No independent historical variant package assigned.
- TRA (Transylvania): No independent historical variant package assigned.
- TRK (Turkmenistan): No independent historical variant package assigned.
- TUV (Tuva): No independent historical variant package assigned.
- UDM (Udmurtia): No independent historical variant package assigned.
- UKR (Ukraine): No independent historical variant package assigned.
- URA (Ural Republic): No independent historical variant package assigned.
- UZB (Uzbekistan): No independent historical variant package assigned.
- VOJ (Vojvodina): No independent historical variant package assigned.
- VTB (Vitebsk): No independent historical variant package assigned.
- WAS (Wales): No independent historical variant package assigned.
- WLC (Wallachia): No independent historical variant package assigned.
- YAK (Yakutia): No independent historical variant package assigned.
- YAM (Yamalo-Nenets): No independent historical variant package assigned.

Evidence status: officialoperator/manufacturer/museum/archival sources establish key dates and physical configuration. USArmyWEG and contemporaryprofessional naval observation supply comparative system details. Countryimport and licensedproduction context should be read with europe_sources.md and the countryprofiles. A shared design is not evidence that every recipient manufactured it. Uncertain peripheral subvariants are omitted.

Native armour and engine calibration

The source figures describe the physical vehicle. Native game armour and movement are abstract combat statistics, so70mm is not entered as70 game armour or seven arbitrary upgrades. The original MD donor bands provide anchors: Leopard1 armour1, T55 armour1, Centurion armour2 and Chieftain armour6. The source-backed mobility order distinguishes the fast, lightly protected Leopard/AMX30 from slower heavy Centurion/Chieftain and intermediate Patton/T54/T55.

Native tank_nsb_engine_upgrade adds3.5% movement speed per level, with1.5% reliability loss,0.3 IC cost and0.25 fuel consumption. Native tank_nsb_armor_upgrade adds7.5% armour per level, with2.5% speed loss,2% reliability loss,0.2 IC cost,0.25 breakthrough and0.1 defence. These are original MD trade-offs, not free historical bonuses. Petrol1 contributes speed7 while diesel1 contributes speed9, which explains the higher petrol-Patton engine levels. No gun upgrade, MIO or experience bonus is added.

Leopard1 specifically records the Bundeswehr original105mm L7A3,830PS/610kW,40tonnes and65km/h; Bovington records70mm armour. The model retains a cast turret, optical fire control and manual loading. It excludes postcutoff A1 stabilization, later thermal optics and later ammunition/armour upgrades. Engine5 and armour1 are relative native calibration choices. The exact physical numbers are retained independently in historical_specs.

Model | NSB armour | NSB engine
--- | ---: | ---:
Leopard 1 | 1 | 5
AMX-30B | 2 | 5
T-54B | 1 | 1
T-55A | 1 | 1
T-62 | 2 | 1
T-64A | 2 | 3
Centurion Mk 5/2 | 2 | 0
Chieftain Mk 2 | 6 | 0
M47 Patton | 3 | 6
M48A2 Patton | 3 | 6
M48A1 Patton | 3 | 6
M60A1 | 3 | 1
T-34-85 | 1 | 2
Type 59 | 1 | 1
AMX-13/75 | 0 | 3
AMX-13/90 | 0 | 3
Panzer 61 | 2 | 2
Stridsvagn 103A | 2 | 1
Stridsvagn 74 | 1 | 1
Comet Mk I | 1 | 1
FV601 Saladin | 1 | 2
Daimler Ferret | 0 | 1
BTR-152 | 0 | 2

T55A uses the same1955 medium chassis baseline as T54/T55. Its NBC protection improvement does not justify the higher base armour of the native1965 chassis. The physical100mm hull-front record and shared armour1/engine1 calibration remain unchanged.

Original Mk112 eight-cell ASROC box launchers use the dedicated early ASW module, with Navy1960photographic and NTIS1969technical provenance. They are not vertical launch systems and grant no nuclear warhead effect.
