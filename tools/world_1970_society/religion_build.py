# IMPERIA COLD WAR — Auditable 1970 cultural religion mapping
"""Build original native-law mappings. Raw research datasets are not redistributed."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
inventory = json.loads((ROOT / 'inventory.json').read_text(encoding='utf-8'))
countries = {r['tag']: r for r in inventory['countries']}
records = {}
sources = {
    'wrp1970': {
        'title': 'World Religion Dataset, version 1.1: 1970 observations',
        'url': 'https://correlatesofwar.org/data-sets/world-religion-data/',
        'data_url': 'https://correlatesofwar.org/wp-content/uploads/WRP_national.csv',
        'author': 'Zeev Maoz and Errol A. Henderson', 'published': '2013',
        'accessed': '2026-10-23',
        'citation': 'Maoz, Zeev, and Errol A. Henderson. 2013. The World Religion Dataset, 1945-2010: Logic, Estimates, and Trends. International Interactions 39:265-291.',
        'licence': 'COW terms restrict commercial use and raw dataset redistribution. No raw dataset is included. These are original coarse native-game classifications, not copied numerical demographic tables.',
        'terms_url': 'https://correlatesofwar.org/data-sets/',
        'limitations': 'Retrospective estimates, sometimes interpolated. 1970 is an annual observation, not a census conducted on 1 January. National rows do not independently establish regional religious proportions.'
    },
    'wrp_codebook': {
        'title': 'World Religion Project: Codebook, version 1.1',
        'url': 'https://correlatesofwar.org/wp-content/uploads/wrp-codebook-bibliography.pdf',
        'author': 'Zeev Maoz and Errol A. Henderson', 'published': '2013', 'accessed': '2026-10-23',
        'licence': 'COW dataset terms; documentation is cited, not redistributed.',
        'limitations': 'Describes category reconciliation, imputation, and dual religious affiliation.'
    },
    'un1971': {
        'title': 'Demographic Yearbook 1971, table 17: Population by religion, pp. 510-514',
        'url': 'https://unstats.un.org/unsd/demographic/products/dyb/dybsets/1971%20DYB.pdf',
        'author': 'United Nations Statistical Office; contributing national statistical offices',
        'published': '1972', 'accessed': '2026-10-23',
        'licence': 'United Nations publication. Reuse licence not established; only original qualitative classifications are retained, no raw PDF or census table.',
        'limitations': 'Censuses span 1962-1971; census categories can absorb syncretic traditions. Nigeria1963 census is explicitly flagged as believed overenumerated.'
    },
    'un1973': {
        'title': 'Demographic Yearbook 1973, table 31: Population by religion, pp. 486-489',
        'url': 'https://unstats.un.org/unsd/demographic/products/dyb/dybsets/1973%20DYB.pdf',
        'author': 'United Nations Statistical Office; contributing national statistical offices',
        'published': '1974', 'accessed': '2026-10-23',
        'licence': 'United Nations publication. Reuse licence not established; only original qualitative classifications are retained, no raw PDF or census table.',
        'limitations': '1965-1973 censuses used as period evidence, not as exact observations on the scenario day.'
    },
    'india1971': {
        'title': 'Religion, Series-1, Census of India 1971',
        'url': 'https://censusindia.gov.in/nada/index.php/catalog/31626',
        'author': 'A. Chandra Sekhar; Registrar General and Census Commissioner, India',
        'published': '1972', 'accessed': '2026-10-23',
        'licence': 'Rights: Office of the Registrar General, India. No tables reproduced.',
        'limitations': '1971 census used as nearest period evidence. Current regional borders and later ethnic political organizations are not projected back as governments.'
    },
    'meghalaya1971': {
        'title': 'Statistical Abstract of Meghalaya 1978, table 1.25: religion 1961-1971',
        'url': 'https://des.megplanning.gov.in/documents/Abstract-1978.pdf',
        'author': 'Directorate of Economics and Statistics, Government of Meghalaya; Census of India1971',
        'published': '1978', 'accessed': '2026-10-23',
        'licence': 'Government publication; reuse licence unknown. No table reproduced.',
        'limitations': 'Christianity was a plurality in1971, with substantial indigenous and Hindu traditions; a modern Christian supermajority is not backdated.'
    },
    'srilanka1971': {
        'title': 'Census of Population and Housing1971, religion variable',
        'url': 'https://nada.statistics.gov.lk/index.php/catalog/228/variable/V122',
        'author': 'Department of Census and Statistics, Sri Lanka',
        'published': '1971 census; catalogue2023', 'accessed': '2026-10-23',
        'licence': 'Reuse licence unknown. No microdata or tables redistributed.',
        'limitations': 'Catalogue warns microdata case counts are not population summaries; used to validate native categories alongside WRP1970.'
    },
    'soviet_study': {
        'title': 'Soviet Union: A Country Study, religions and nationalities chapters',
        'url': 'https://www.loc.gov/item/90025756/',
        'text_url': 'https://www.marines.mil/Portals/1/Publications/Soviet%20Union%20Study_3.pdf',
        'author': 'Raymond E. Zickel, editor; Federal Research Division, Library of Congress',
        'published': '1991, research completed May1989', 'accessed': '2026-10-23',
        'licence': 'Library of Congress states text and graphics public domain except separately credited protected photographs. No images reused.',
        'limitations': 'Retrospective institutional and ethnocultural context, not a1970 regional religious census. Regional mappings are marked inference or proxy.'
    },
    'indian_ocean_study': {
        'title': 'Indian Ocean: Five Island Countries, historical religion chapters',
        'url': 'https://www.loc.gov/item/95016570/',
        'author': 'Helen Chapin Metz, editor; Federal Research Division, Library of Congress',
        'published': '1995, research completed August1994', 'accessed': '2026-10-23',
        'licence': 'Library of Congress states text and graphics public domain except separately credited protected photographs. No images reused.',
        'limitations': 'Historical continuity evidence, not a same-day1970 enumeration. Original coarse mappings only.'
    },
    'bahrain1970': {
        'title': 'Report of the Personal Representative of the Secretary-General, Bahrain background, paragraph20',
        'url': 'https://digitallibrary.un.org/record/604851/files/S_SUPP_1970_2--%5EOR_SC_1970_2%5E-EN.pdf',
        'author': 'United Nations Secretary-General and his Personal Representative',
        'published': '1970', 'accessed': '2026-10-23',
        'licence': 'United Nations official record; reuse licence unknown. No report text reproduced.',
        'limitations': 'Reports about half Bahraini Muslims Shia and the remainder mostly Sunni. Does not warrant importing modern demographic claims into1970.'
    },
    'kachin_history': {
        'title': 'Being and Becoming Kachin: Histories Beyond the State, chapter8 Virtue',
        'url': 'https://academic.oup.com/british-academy-scholarship-online/book/28495/chapter-abstract/229992842',
        'author': 'Mandy Sadan', 'published': '2013', 'accessed': '2026-10-23',
        'licence': 'British Academy/Oxford University Press copyright. Only an original short mapping rationale retained.',
        'limitations': 'Original historical research explicitly challenges a pre-late1970s Christian majority; pluralist avoids backdating later conversion.'
    },
    'timor_church_history': {
        'title': 'Interview with Cardinal Virgilio do Carmo da Silva: The wounds have been healed through forgiveness',
        'url': 'https://fides.org/en/news/75387',
        'author': 'Agenzia Fides; Cardinal Virgilio do Carmo da Silva',
        'published': '2024', 'accessed': '2026-10-23',
        'licence': 'Catholic mission news agency; reuse licence unknown. No quotation or image reproduced.',
        'limitations': 'Primary institutional oral-history testimony explicitly identifies the large growth of Catholic affiliation after1975. Used for historical direction, not an exact1970 headcount.'
    },
    'eritrea_continuity': {
        'title': 'Eritrea: Facts and Figures, religious historical background',
        'url': 'https://home.eritreaembassy.ch/discover-eritrea/fact-and-figures',
        'author': 'Embassy of the State of Eritrea, Switzerland',
        'published': 'Undated', 'accessed': '2026-10-23',
        'licence': 'Reuse licence unknown. Original coarse mapping only.',
        'limitations': 'Current official description used for long-standing Christian/Muslim geography, not to assert an exact1970 ratio.'
    },
    'native_md': {
        'title': 'Native Millennium Dawn religion idea definitions, localisation and classification scripts',
        'url': None,
        'paths': ['common/ideas/AA_law_religion.txt', 'localisation/english/MD_ideas_l_english.yml', 'common/scripted_effects/00_religion_effects.txt', 'common/scripted_effects/00_country_classification_arrays.txt'],
        'author': 'Millennium Dawn contributors; exact per-block authors unknown',
        'published': 'Workspace version at research date', 'accessed': '2026-10-23',
        'licence': 'Retain existing project/upstream notices. This record does not establish ownership.',
        'limitations': 'One mutually exclusive religion slot; Western Christian combines Catholics and Protestants, Buddhist combines traditions. No generic Sikh, indigenous, Taoist, Confucian, Druze, Alawite or secular law exists.'
    },
    'territorial_proxy': {
        'title': 'IMPERIA COLD WAR authored territorial-release mapping policy',
        'url': None, 'author': 'IMPERIA COLD WAR research pass', 'published': '2026-10-23', 'accessed': '2026-10-23',
        'licence': 'Original project research notes. Underlying cited sources retain their own terms.',
        'limitations': 'An explicitly identified design inference from1970 territory or historical cultural institutions, not an independent religious census and not a claim that a later organization existed in1970.'
    },
    'pending_tag_review': {
        'title': 'IMPERIA COLD WAR native nonhistorical tag evidence, pending user review',
        'url': None, 'author': 'Existing upstream/custom tag definitions; exact authors unknown',
        'published': 'Workspace version at research date', 'accessed': '2026-10-23',
        'paths': ['history/countries/ALN - Alien.txt', 'history/countries/ZOM - Zombies.txt', 'history/countries/C01 - Custom_01.txt', 'history/countries/ADS - Aegist.txt', 'localisation/english/countries_l_english.yml'],
        'licence': 'Retain existing upstream notices; per-file permission unknown.',
        'limitations': 'No religion is assigned to these four tags. A later release state or real later organization is not classified as fictional merely because it did not exist in1970.'
    }
}

def add(tags, idea, rationale, source_ids, confidence='medium', status='territorial_proxy', limitations=None):
    for tag in tags.split():
        assert tag in countries, tag
        assert tag not in records, ('duplicate', tag)
        records[tag] = {
            'name': countries[tag]['name'], 'idea': idea,
            'rationale': re.sub(r'(?<=[A-Za-z])(?=(?:19|20)[0-9]{2})|(?<=[0-9])(?=[A-Za-z])', ' ', rationale.format(name=countries[tag]['name'])),
            'source_ids': source_ids,
            'confidence': confidence, 'status': status,
            'limitations': limitations or 'Native law is a coarse cultural-institutional mapping, not a claim of universal adherence or an official state religion.'
        }

# Original classifications based on the direct1970 WRP state observations.
direct_christian = '''USA CAN CUB HAI DOM JAM TRI BAR MEX GUA HON ELS NIC COS PAN COL VEN ECU PRU BRA BOL PAR CHL ARG URG ENG IRE HOL BEL LUX FRA SWI SPR POR GER DDR POL AUS HUN CZE ITA MLT FIN SWE NRY DEN ICE EGU GAB CNG DRC UGA KEN BUR RWA ZAM MLW SAF LES SWA PHI AST NZL'''
add(direct_christian, 'christian', 'The1970 national evidence places Western Christian traditions at the centre of {name} religious life; Catholics and Protestants share MD\'s Western Christian law.', ['wrp1970', 'native_md'], 'high', 'direct_1970_national')
add('GRE CYP BUL ROM', 'orthodox_christian', 'Eastern Orthodox Christianity is the dominant historical Christian tradition of {name}; this is distinct from MD\'s Western Christian category.', ['wrp1970', 'native_md'], 'high', 'direct_1970_national')
add('AFG ALG GAM GUI MAU MOR NGR MAL TUN LBA SUD TUR EGY SYR JOR SAU KUW QAT UAE PAK IND MAY MLD SOM SYE', 'sunni', 'The1970 evidence supports Sunni Islam as the principal religious tradition of {name}; minority communities and secular government policy are not erased by this one-slot mapping.', ['wrp1970', 'native_md'], 'high', 'direct_1970_national')
add('PER IRQ YEM', 'shia', 'Shia traditions form the principal cultural religious baseline in {name}; the ruler\'s personal affiliation does not replace the population\'s tradition.', ['wrp1970', 'native_md'], 'high', 'direct_1970_national', 'Native shia groups distinct Shia schools, including Zaydi Islam in North Yemen; it does not imply Twelver clerical government or post1979 Iranian policy.')
add('BRM CBD LAO SIA SVN', 'buddism', 'The1970 evidence supports Buddhist traditions as the principal religious cultural baseline of {name}.', ['wrp1970', 'native_md'], 'high', 'direct_1970_national')
add('RAJ NEP', 'hindu', 'Hindu traditions provide the majority cultural religious baseline of {name} around1970; minority religions and constitutional secularism remain separate questions.', ['wrp1970', 'india1971', 'native_md'], 'high', 'direct_1970_national')
add('ISR', 'judaism', 'The1970 Israeli religious-cultural baseline is Jewish, with Muslim, Christian and Druze minorities.', ['wrp1970', 'native_md'], 'high', 'direct_1970_national')
add('JAP', 'shinto', 'Shinto institutions and rites are central to Japan\'s cultural religious landscape alongside overlapping Buddhist practice; the base native law is retained.', ['wrp1970', 'wrp_codebook', 'native_md'], 'high', 'direct_1970_national', 'Shinto and Buddhism overlap. This does not restore wartime State Shinto and does not use the later focus-upgraded shinto2 spirit.')
add('OMA', 'ibadi', 'Ibadi Islam is the distinctive Omani historical religious institution; a generic Sunni label would obscure that context.', ['wrp1970', 'native_md'], 'high', 'direct_1970_national', 'Oman also contains large Sunni communities; the one native slot represents the historical Omani religious institution, not a uniform national population.')
add('SEN', 'sufi_islam', 'Sufi brotherhoods are central to Senegal\'s Sunni Muslim religious institutions and public life around1970.', ['wrp1970', 'native_md'], 'high', 'direct_1970_national', 'Sufi is a practice and institutional tradition within Sunni Islam, not a separate exclusive denomination. Native MD treats it as a separate law and does not include it in the sunni classification array.')
add('SRI', 'buddism', 'Period national evidence and the1971 census support a Buddhist majority, alongside Hindu, Muslim and Christian communities.', ['wrp1970', 'srilanka1971', 'native_md'], 'high', 'direct_1970_national')
add('ETH', 'eastern_church_eth', 'The Ethiopian Orthodox Tewahedo Church is the historical state-linked Christian institution in1970 Ethiopia.', ['wrp1970', 'native_md'], 'medium', 'direct_1970_national', 'Oriental Orthodoxy is not Eastern Orthodoxy. The country-specific native Ethiopian law is used; the country also includes large Muslim and indigenous populations and Eritrea in1970.')
add('NIG', 'fifty_fifty_divide', 'Nigeria\'s1970 cultural landscape contains two comparably large Christian and Muslim blocs and substantial indigenous traditions; neither a single Christian nor Sunni law fits.', ['wrp1970', 'un1971', 'native_md'], 'medium', 'direct_1970_national', 'Native Fifty Fifty Divide approximates the Christian/Muslim institutional split. It is not an exact50/50 census claim and understates indigenous traditions. The1963 census was disputed; no NIG focus-upgraded majority spirit is granted.')
add('LEB', 'religious_divide', 'Lebanon\'s confessional republic rests on substantial Christian, Sunni, Shia and Druze communities; one predominant religious law would conceal that structure.', ['wrp1970', 'native_md'], 'medium', 'direct_1970_national', 'Religious Divide is a native abstraction for a confessional power-sharing society, not a claim of two equally sized religions or inevitability of the1975 war.')
add('BHR', 'pluralist', 'The UN\'s1970 Bahrain background describes a near split between Shia and Sunni Bahraini Muslims; the later ruling dynasty is not used to relabel the population Sunni.', ['bahrain1970', 'wrp1970', 'native_md'], 'medium', 'direct_period_source', 'Native MD has no general mixed Sunni/Shia law. Pluralist is the least specific fit; no modern70-percent Shia figure is backdated.')
add('ALB', 'pluralist', 'Albania retains Sunni/Bektashi, Orthodox and Catholic historical communities under the1967 official anti-religious campaign; native cultural religion cannot be equated to a later country-specific atheist reward.', ['wrp1970', 'native_md'], 'medium', 'direct_1970_national')
add('BEN BFA CDI LIB SIE CAM CAR BOT MAD TNZ MRT GUY FIJ', 'pluralist', '{name} has substantial combinations of indigenous, Christian, Muslim or Hindu traditions in period evidence; the native single-denomination choices would conceal the mixed landscape.', ['wrp1970', 'native_md'], 'medium', 'direct_1970_national', 'MD has no generic indigenous-tradition law. Pluralist is an approximation of religious diversity and syncretism, not a modern constitutional or interfaith-policy claim.')
add('CHI TAI KOR NKO VIE SIN', 'pluralist', '{name} combines substantial folk, ancestral, Buddhist, Confucian, Christian or nonreligious traditions; no single native religion accurately covers the1970 landscape.', ['wrp1970', 'wrp_codebook', 'native_md'], 'medium', 'direct_1970_national', 'State repression or atheism does not make all citizens atheists. Native cheondo is a particular Korean movement, not a generic Korean belief system. No modern church growth is backdated.')
add('SOV', 'pluralist', 'The USSR in1970 contains Orthodox, Muslim, Catholic, Jewish, Buddhist and nonreligious populations; the whole union is not reduced to ethnic Russian Orthodoxy.', ['wrp1970', 'soviet_study', 'native_md'], 'medium', 'direct_1970_national', 'Native law represents union-wide cultural diversity, not the official Marxist-Leninist policy. Orthodox Christianity remains the largest Christian institution; no focus-upgraded church spirit is granted.')
add('MON', 'buddism', 'Tibetan Buddhist institutions remain Mongolia\'s distinctive historical religious tradition despite severe communist suppression and widespread nonreligion by1970.', ['wrp1970', 'native_md'], 'medium', 'cultural_institution_inference', 'A cultural-institutional mapping, not a claim that most Mongolians actively professed Buddhism in1970. Native MD has no general secular cultural law.')
add('ZIM', 'pluralist', 'Period evidence shows substantial Christian and indigenous traditions across Rhodesia\'s whole population, not only the white settler population.', ['wrp1970', 'un1971', 'native_md'], 'medium', 'direct_1970_national')

# Period census evidence for territories not in the direct WRP1970 state sample.
add('BAH STH SOL NAU VAN PAP TON SAM KIR TUL', 'christian', 'Period UN census tables identify Christian traditions as the principal affiliation of {name}; this applies to the territory before any later independence.', ['un1971', 'native_md'], 'high', 'direct_period_territorial')
add('SEY', 'christian', 'The1971 census identifies overwhelmingly Christian affiliation in the Seychelles, consistent with the colonial-era religious landscape.', ['un1973', 'indian_ocean_study', 'native_md'], 'high', 'direct_period_territorial')
add('MAC', 'buddism', 'Macau\'s1970 census records Buddhism as the predominant affiliation; Portuguese administration does not justify assigning a Catholic majority.', ['un1973', 'native_md'], 'high', 'direct_period_territorial', 'Census Buddhist affiliation may include Chinese folk practice. The native category is broad and does not measure intensity of belief.')
add('BRU', 'sunni', 'Brunei\'s1971 census and its historical Malay Islamic institutions support Sunni Islam, with substantial Buddhist and indigenous minorities.', ['un1971', 'native_md'], 'high', 'direct_period_territorial')
add('PAL', 'sunni', 'The1967 Gaza census and broader Palestinian cultural baseline support Sunni Islam; Christian Palestinians remain a significant historic minority.', ['un1971', 'native_md'], 'high', 'direct_period_territorial')
add('ZAN', 'sunni', 'The1967 Zanzibar census supports a predominantly Muslim island population, distinct from the mixed mainland Tanzanian baseline.', ['un1971', 'native_md'], 'high', 'direct_period_territorial')
add('SHA', 'sunni', 'The1970 Spanish Sahara census identifies Islam as the predominant Sahrawi cultural tradition; Spanish settler Christians do not determine the release baseline.', ['un1973', 'native_md'], 'high', 'direct_period_territorial')
add('SUR', 'pluralist', 'The1964 Suriname census shows substantial Christian, Hindu and Muslim communities, making a plural native law the best period fit.', ['un1971', 'native_md'], 'high', 'direct_period_territorial')

# European regional releases: territorial baseline, not later separatist ideology.
add('ADO BAY CAT CNR FLN GAL HLS HZG IOM LIC MNC NAV SAR SCL SCO SMA SPA WAS', 'christian', '{name} inherits the surrounding territory\'s Catholic or Protestant institutions around1970; later separatist identity does not create a new religion.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('CHA GAH TOG', 'pluralist', 'Period evidence places substantial indigenous, Christian and Muslim communities in {name}; no single native tradition adequately represents the whole population.', ['wrp1970', 'native_md'], 'medium', 'direct_1970_national')
add('CRO SLO SLV SIL KSH LAG LAT LIT EST', 'christian', '{name}\'s1970 territory has long-standing Catholic or Protestant institutions. Communist secularization is represented separately from this cultural baseline.', ['wrp1970', 'soviet_study', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'National successor-state observations are not silently treated as1970 regional census counts. One category compresses local Orthodox and nonreligious communities.')
add('BLR UKR MLV PMR MNT RSK FYR CRE GGZ WLC VTB', 'orthodox_christian', '{name} uses its1970 territorial Eastern Orthodox institutional baseline, without projecting later independence or wartime movements back into1970.', ['wrp1970', 'soviet_study', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('SER', 'pluralist', 'The SER tag represents all Yugoslavia in1970, with Orthodox, Catholic, Muslim and nonreligious populations; a Serbia-only Orthodox baseline would misrepresent the federation.', ['wrp1970', 'native_md'], 'high', 'direct_1970_national', 'MD has separate Western and Orthodox Christian laws and no single Yugoslav confessional law. Pluralist is the best whole-federation mapping; successor-state boundaries are not substituted for1970 Yugoslavia.')
add('BOS VOJ TRA', 'pluralist', '{name}\'s1970 territory contains substantial communities from different Orthodox, Catholic, Protestant or Muslim traditions; a uniform denominational law would hide that diversity.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('KOS NCY', 'sunni', '{name} uses the Sunni Muslim cultural baseline of the relevant Albanian or Turkish-Cypriot communities in1970, not the institutions of a later release government.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('NIR', 'christian', 'Both principal Northern Irish confessional communities around1970 are Western Christian, Protestant and Catholic; MD\'s native law combines them.', ['wrp1970', 'native_md'], 'high', 'territorial_proxy', 'Western Christian does not erase the Troubles. A Christian/Muslim divide law would be inaccurate for a Protestant/Catholic conflict.')
add('FAO GRN', 'christian', 'Lutheran Christian institutions provide the established cultural religious baseline in {name} around1970, alongside local inherited traditions.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('EUU', 'christian', 'For the counterfactual unified-European country slot, the1970 European Community members\' Catholic and Protestant cultural baseline maps to Western Christian.', ['wrp1970', 'territorial_proxy', 'native_md'], 'low', 'counterfactual_territorial_aggregate', 'The European Communities were real institutions, not a sovereign country with one religious law. This is an authored aggregate for a country tag, not an actual1970 national religious observation.')

# Soviet territorial releases: actual ethnocultural context, no post-Soviet national rewards.
add('ARM NKR', 'eastern_church_arm', 'Armenian Apostolic Christianity is the distinctive historical religious institution of {name}\'s Armenian cultural territory.', ['soviet_study', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'Oriental Orthodoxy is distinct from Eastern Orthodoxy. The native Armenian base law is used without granting pagan or church reform focus rewards; no1970 regional census is claimed.')
add('GEO', 'orthodox_christian', 'The Georgian Orthodox Church supplies the historical cultural institutional baseline despite Soviet restrictions.', ['soviet_study', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('ABK SOO', 'pluralist', '{name} combines Orthodox Christian, Muslim or indigenous customary traditions; modern national religious revival spirits are not backdated.', ['soviet_study', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy', 'Reliable1970 self-reported regional religion figures were not obtained. The generic plural law avoids claiming universal Orthodoxy or importing1980s organized Assianism.')
add('ADJ', 'sunni', 'The Adjarian Muslim historical cultural tradition is predominantly Sunni, while Soviet settlement and neighboring Georgian Orthodox traditions make the territory mixed.', ['soviet_study', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy', 'No1970 regional religious census was obtained. This is an inference from historical Adjarian identity, not a claim based on modern Georgian census results.')
add('AZE SAZ ARA LOR TAB QTF HAZ TLS', 'shia', '{name}\'s historical1970 territorial communities belong principally to Shia traditions; later Islamist parties or revolutionary institutions are not used as the baseline.', ['wrp1970', 'soviet_study', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'Territorial cultural inference. Local Sunni or other minorities are compressed by the single native law; no precise1970 regional share is claimed.')
add('CHE ING DAG TAT BSH KAZ KYR TAJ TRK UZB KRP', 'sunni', '{name}\'s historical Muslim communities are principally Sunni; Soviet repression and the presence of Christian or nonreligious residents are separate from this inherited cultural institution.', ['soviet_study', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'Country release law emphasizes the titular territory\'s Muslim cultural institution. In mixed Soviet regions it does not claim every resident or an absolute majority was observant Sunni.')
add('ADY KBK KCC GOR', 'pluralist', '{name}\'s North Caucasian1970 territory contains Sunni Muslim and Orthodox Christian populations, with secular and customary traditions; one exclusive religion is too narrow.', ['soviet_study', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy')
add('BRY KLM TUV', 'buddism', 'Tibetan Buddhist institutions are a distinctive inherited tradition of the titular {name} communities, despite Soviet repression and a substantial Russian settler population.', ['soviet_study', 'territorial_proxy', 'native_md'], 'medium', 'cultural_institution_inference', 'This is the titular territory\'s institutional tradition, not an assertion that practising Buddhists were an absolute1970 population majority. No post-Soviet revival reward is granted.')
add('ALT YAK MEL', 'pluralist', '{name}\'s1970 cultural landscape includes indigenous customary traditions alongside Orthodox Christian and nonreligious residents; the native menu lacks the relevant indigenous tradition.', ['soviet_study', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy')
add('CHU MOV UDM KOM KAE', 'orthodox_christian', '{name}\'s1970 territory has a substantial Eastern Orthodox Christian historical institutional baseline alongside indigenous and nonreligious communities.', ['soviet_study', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('KHM KHS NEE CKK YAM', 'pluralist', '{name} has important indigenous customary traditions and Christian or nonreligious communities in its1970 territorial population; a single specific native religion would misstate this mix.', ['soviet_study', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy', 'The native game has no generic Siberian indigenous religion category. Pluralist is an approximation; no census denomination percentages are asserted.')
add('CRM DON DPR DRP ESB FAR HPR KUB LPR MLR NOV OPR RUS SEU SIB URA CSB', 'orthodox_christian', 'For this later or counterfactual political release, {name} uses the Eastern Orthodox historical institutional baseline of its1970 Russian or Ukrainian territory.', ['soviet_study', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'The later organization or republic is not asserted to have existed in1970. Its modern ideology does not replace the pre-existing cultural religious tradition; no upgraded national church idea is granted.')

# American and Caribbean territories and regional releases.
add('ASK CAL CAS CSA FLA GLC IDH KAN NEN NYK TEX UDT USB VMT WVA QUE PTR', 'christian', '{name}\'s1970 North American territorial cultural baseline is predominantly Western Christian, with Catholic and Protestant traditions combined in the native slot.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'A later political release or organization does not imply a different1970 religion. Deseret\'s Latter-day Saint tradition is compressed into native Western Christian because no distinct native law exists.')
add('HWI LKT', 'pluralist', '{name} retains significant indigenous or Asian religious traditions alongside Christian communities; its1970 cultural territory is not reduced to the mainland US average.', ['wrp1970', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy')
add('ANT BLZ DMI GRA NLA STK STL STV', 'christian', '{name} uses the historically established Catholic and Protestant cultural institutions of its Caribbean or Central American territory around1970, before later independence where applicable.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('FGU PAT RGD SPL SUL TAM YUC SLA TRC ZAP', 'christian', '{name}\'s1970 Latin American territorial baseline is predominantly Catholic within native Western Christian; later armed or regional movements do not establish a different population religion.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'Indigenous and Afro-American practices can coexist with formal Christian affiliation. This category does not endorse or backdate any later organization.')

# African territories and later movement tags.
add('AGL CAB UNI NAM SAO VER', 'christian', '{name} uses the long-established Christian institutional tradition of its1970 territory, with substantial customary practices retained outside the coarse native category.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'For movement tags this represents territory and communities, not an organization already in power. No independent1970 regional enumeration is claimed.')
add('GUB MOZ SSU', 'pluralist', 'The1970 territory of {name} contains substantial indigenous religious practice alongside Christian or Muslim communities; current national religious proportions are not projected backward.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'For Southern Sudan, modern Christian-majority estimates are not treated as1970 census evidence. Native MD lacks a generic indigenous law.')
add('DJI', 'sunni', 'Sunni Islam is the longstanding principal tradition among Somali and Afar communities in the French Territory of the Afars and the Issas in1970.', ['wrp1970', 'territorial_proxy', 'native_md'], 'high', 'territorial_proxy')
add('COM ANJ MTE', 'sunni', '{name} inherits the longstanding Sunni Islamic cultural institutions of the Comorian islands before later independent or French territorial arrangements.', ['indian_ocean_study', 'territorial_proxy', 'native_md'], 'high', 'territorial_proxy')
add('ERI', 'pluralist', 'Eritrea\'s longstanding Christian highland and Muslim lowland/coastal communities require a mixed cultural baseline within1970 Ethiopia.', ['wrp1970', 'eritrea_continuity', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'The modern official description corroborates historic geography; no exact1970 split is claimed. A distinct Eritrean church separate from the Ethiopian church is not backdated to1970.')
add('DAR CSM LGN TIE TUA', 'sunni', '{name} uses the historically established Sunni Muslim institutions of its Sahelian or Saharan communities around1970.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'Territorial inference rather than an independent1970 survey. Sufi practice can be prominent within this Sunni baseline.')
add('CYR FEZ GNA GNC HOR TRP', 'sunni', '{name} uses Libya\'s established Sunni Muslim territorial baseline in1970; later rival governments are not treated as existing scenario governments.', ['wrp1970', 'territorial_proxy', 'native_md'], 'high', 'territorial_proxy')
add('JUB PUN SHB SML SNA SWS AIA', 'sunni', '{name} uses the Somali territory\'s predominantly Sunni Muslim cultural baseline around1970, rather than the ideology of a later armed organization.', ['wrp1970', 'territorial_proxy', 'native_md'], 'high', 'territorial_proxy')
add('BIA', 'christian', 'The1970 Biafran/Igbo territorial baseline has strong Catholic and Protestant Christian institutions, with indigenous traditions also present.', ['wrp1970', 'un1971', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('BAL SEL', 'pluralist', '{name} uses the Central African territory\'s1970 combination of customary, Christian and Muslim communities; a later militia\'s label does not define all residents.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('AFR LUR', 'pluralist', '{name} uses its Sierra Leonean or Liberian1970 territory\'s mixed indigenous, Muslim and Christian religious landscape, not later rebel branding.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('FNC', 'pluralist', 'The northern Ivorian territorial baseline includes substantial Muslim and indigenous traditions; the later Forces Nouvelles organization is not backdated.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('MLC RCD', 'christian', '{name} inherits the Congo territory\'s established Christian institutional baseline around1970; the later movement is not asserted to exist at the scenario date.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')

# Asian territorial releases and later organization tags.
add('BAN BLC BNG ETK KAS ACE', 'sunni', '{name} uses the Sunni Muslim cultural institutions of the relevant1970 territory; independence or later militant organization dates do not change that baseline.', ['wrp1970', 'india1971', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('AQY HAM HEJ ISI NEJ NUS FSA TAL TTP IEK IKR KUR PKK PUK ROJ BDA KBY', 'sunni', '{name} uses the Sunni Muslim cultural baseline of its1970 territorial population, without importing the state religion or policies of a later movement.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'A territorial proxy for later political or armed tags. Kurdish secular party ideology is not equated with an atheist population; minority traditions are compressed by the native single slot.')
add('HEZ HOU', 'shia', '{name} uses the inherited Shia cultural baseline of its Lebanese Shia or northern Yemeni Zaydi territorial community, not a later organization\'s existence in1970.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'The native shia category combines distinct schools. This grants neither post1979 Iranian institutions nor modern movement rewards.')
add('ALA DRU HRM', 'pluralist', '{name}\'s1970 territory includes religious traditions or mixed communities that MD\'s Sunni/Twelver Shia binary cannot faithfully identify.', ['wrp1970', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy', 'MD has no general Alawite or Druze law. Alawites and Druze are not relabelled ordinary Twelver Shia; Hormuz is treated cautiously as a mixed Gulf/Iranian coastal territory.')
add('HKG', 'pluralist', '{name} combines Chinese folk, ancestral, Taoist, Buddhist, Christian and nonreligious practice in its1970 territorial population.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('RYU', 'pluralist', 'Okinawa\'s1970 religious landscape combines Ryukyuan ancestral/customary rites and Japanese Buddhist or Shinto institutions under US administration.', ['wrp1970', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy', 'Native MD lacks a Ryukyuan religion. US administration until1972 does not justify importing mainland American Christianity or uniform mainland Shinto.')
add('ARK NHN SHN TIB BHU', 'buddism', '{name} uses its longstanding Buddhist cultural institutions around1970; the native category covers both Theravada and Tibetan Buddhist traditions.', ['wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('OMG', 'pluralist', 'This tag\'s territorial anchor is Inner Mongolia, whose1970 cultural landscape includes Tibetan Buddhist, Mongolian customary, Han Chinese and nonreligious traditions.', ['wrp1970', 'soviet_study', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy', 'The tag name Outer Mongolia conflicts with its Inner Mongolian territorial anchor. It is not copied from independent Mongolia and does not assert a1970 religious census.')
add('KAC', 'pluralist', 'Kachin communities around1970 include customary spirit traditions, Christianity and Buddhism; historical research cautions against backdating a later Christian majority.', ['kachin_history', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy')
add('CHS KAR WAA', 'pluralist', '{name}\'s1970 communities include important indigenous customary practice alongside Christian or Buddhist institutions; modern conversion patterns are not backdated wholesale.', ['wrp1970', 'kachin_history', 'territorial_proxy', 'native_md'], 'low', 'territorial_proxy', 'No independent1970 regional census was obtained. Native MD lacks the relevant indigenous religion and compresses heterogeneous hill communities into one law.')
add('KAM MAN NPM TML', 'hindu', '{name} uses its1970 territorial Hindu cultural baseline, rather than the ideology of a later movement.', ['india1971', 'wrp1970', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'No claim that all inhabitants share one religion. For Tamil Eelam, Christian and Muslim Tamils remain separate minorities within the native approximation.')
add('KHA LAD MEG SIK', 'pluralist', '{name}\'s1970 territory includes large Sikh, Buddhist, Muslim, Hindu, Christian or indigenous communities which are not faithfully represented by one available denominational law.', ['india1971', 'meghalaya1971', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'Punjab\'s Sikh tradition has no native Sikh law; Ladakh is Buddhist/Muslim; Sikkim has Hindu and Buddhist populations; Meghalaya1971 is Christian/indigenous/Hindu. Pluralist is a native-menu mapping, not an exact demographic measurement.')
add('TIM', 'pluralist', 'Portuguese Timor around1970 combines indigenous customary religion with Catholic institutions; the much larger Catholic affiliation after1975 is not projected backward.', ['timor_church_history', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'Historical church testimony supports substantial post1975 conversion. Reliable1970 religious census counts were not obtained; modern Catholic supermajority statistics would be anachronistic.')
add('MAR MIC PAU', 'christian', '{name} inherits long-established Protestant and Catholic missionary institutions in the1970 Trust Territory of the Pacific Islands.', ['un1971', 'territorial_proxy', 'native_md'], 'medium', 'territorial_proxy', 'The UN table supplies nearby Pacific period context, not a separate1970 enumeration for each island group. Local customary traditions are not measured by the one native slot.')

if __name__ == '__main__':
    pending = {
        'ALN': 'Fantasy alien tag. Native history disables the economy and grants EH_chimera_units and EH_the_unstoppable_army_idea; no historical population religion exists.',
        'ZOM': 'Fantasy zombie tag. Native history grants Zombie and zombietech and disables the economy; no historical population religion exists.',
        'C01': 'Generic utility country slot. The history file explicitly labels itself a utility tag; its arbitrary capital does not establish a historical population.',
        'ADS': 'Authored Albionis state tag. File name Aegist routes through Aegis.txt, while native localisation names all ideological forms Albionis; this does not establish a real1970 country.'
    }
    for tag, reason in pending.items():
        assert tag not in records
        records[tag] = {
            'name': countries[tag]['name'], 'idea': None,
            'rationale': reason, 'source_ids': ['pending_tag_review'],
            'confidence': 'unassigned', 'status': 'awaiting_user_decision',
            'limitations': 'User requested these tags be shown before any changes. Do not implement a religion assignment for this record.'
        }
    assert set(records) == set(countries)
    valid = set(inventory['native_ideas']['religion'])
    assert all(x['idea'] is None or x['idea'] in valid for x in records.values())
    assert all(x['source_ids'] and all(s in sources for s in x['source_ids']) for x in records.values())
    document = {
        'project': 'IMPERIA COLD WAR', 'date': '1970.1.1',
        'scope': '397 country history tags reviewed;393 religion assignments;4 nonhistorical/utility tags deliberately unassigned pending user review.',
        'mapping_policy': [
            'Native religion is treated as a coarse cultural and institutional slot, not the government\'s religion policy or a universal personal belief.',
            'Catholic and Protestant traditions map to christian; Eastern Orthodox to orthodox_christian; Oriental Armenian and Ethiopian churches use their base native country-specific ideas.',
            'No national focus-upgraded religion idea is granted. Communist government alone does not justify a state-atheist reward spirit.',
            'Pluralist is used when indigenous/folk/syncretic or large mixed traditions lack a faithful single native category; it is not a claim of a modern tolerance policy.',
            'Later real organizations use their1970 territorial communities rather than present-day organizational ideology; their existence in1970 is not asserted.',
            'Direct1970 national rows, nearby period territorial censuses, cultural-institutional interpretations and territorial proxies are distinguished in status and confidence.',
            'Fictional and utility tags ALN,ZOM,C01,ADS remain idea:null pending user decision. No fallback is implemented.',
            'Raw WRP CSV and UN PDFs were consulted privately and are not included or redistributed. This file contains original coarse classifications and original rationale.'
        ],
        'sources': sources,
        'records': dict(sorted(records.items()))
    }
    (ROOT / 'religion.json').write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Reviewed', len(records), 'tags:', sum(x['idea'] is not None for x in records.values()), 'assigned;', len(pending), 'pending user review.')
