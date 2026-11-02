# IMPERIA COLD WAR — Research-backed 1970 currency-slot assignments.
"""Build reviewable research data only. Never modifies country histories."""
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
inventory = json.loads((HERE / 'inventory.json').read_text(encoding='utf-8'))
geography = json.loads((HERE / 'currency_capital_baselines.json').read_text(encoding='utf-8'))['countries']


def source(title, author, url, date, supports, limitation=''):
    return dict(title=title, author=author, url=url, publication_date=date,
                accessed='2026-10-23', supports=supports, limitation=limitation,
                licence='Unknown. Linked and paraphrased; no third-party text or artwork reproduced.')


sources = {
    'IMF_1970_RATES': source('Exchange Rates at the Beginning of 1970', 'Jozef Swidrowski, International Monetary Fund',
        'https://www.elibrary.imf.org/abstract/journals/022/0007/004/article-A003-en.xml', '1970-12-01',
        'Contemporaneous survey of the system in operation at the beginning of 1970, including European Monetary Agreement countries, dollar intervention and multiple exchange rates.',
        'Parities and settlement arrangements do not establish an exact national reserve portfolio. USD assignments outside documented blocs remain model abstractions.'),
    'IMF_1970_LIQUIDITY': source('International Monetary Fund Annual Report 1970, Chapter 2: Developments in International Liquidity', 'International Monetary Fund',
        'https://www.elibrary.imf.org/display/book/9781616351823/ch002.xml', '1970-09-01',
        'Dollar and sterling reserve holdings, 1969 growth of sterling balances and the 1968 guarantees.',
        'Aggregated international evidence, not currency-by-currency portfolios for every country.'),
    'IMF_1969_ASIA': source('Existing International Banking and Credit Facilities in the ECAFE Region, especially Table 2 and choice-of-currency discussion', 'International Monetary Fund, IMF Staff Papers 1969 Issue 003',
        'https://www.elibrary.imf.org/view/journals/024/1969/003/article-A001-en.xml', '1969',
        'Country-supplied settlement observations: sterling predominated in Burma and India; USD predominated in Japan, Korea, Philippines, Thailand and South Vietnam; non-sterling countries generally preferred USD.',
        'Intraregional settlement data from 1966-1968 are a near-date proxy, not official reserve percentages on 1970-01-01.'),
    'BOE_OV44': source('Archive OV44: Overseas Department, Sterling and Sterling Area Policy', 'Bank of England Archive',
        'https://www.bankofengland.co.uk/calmview/Record.aspx?id=OV44&src=CalmView.Catalog', 'Archival records 1966-1974; catalogue undated',
        'Catalogue identifies the territorial and national participants in the 1968 sterling guarantee arrangements, including Caribbean, Asian, African and Gulf participants.',
        'Catalogue includes subsequent extensions, e.g. Bangladesh. For 1970 Bangladesh is assigned the East Pakistan baseline, not an independent agreement.'),
    'BOE_1969': source('Annual Report and Accounts 1969', 'Bank of England',
        'https://www.bankofengland.co.uk/-/media/boe/files/annual-report/1969/boe-1969.pdf', '1969',
        'Countries agreed minimum sterling shares in exchange for dollar-value guarantees; this is genuine reserve dependence, not simply a sterling exchange-rate peg.'),
    'BOE_1974': source('Overseas Sterling Balances 1963-1973', 'Bank of England, Quarterly Bulletin 1974 Q2',
        'https://www.bankofengland.co.uk/-/media/boe/files/quarterly-bulletin/1974/overseas-sterling-balances-1963-1973.pdf', '1974-06',
        'Retrospective account of the September 1968 to May 1972 sterling arrangements and reserve accumulation.'),
    'RBA_1969': source('Reserve Bank Policy in 1968/69', 'Reserve Bank of Australia, Annual Report 1969',
        'https://www.rba.gov.au/publications/annual-reports/rba/1969/res-bank-policy.html', '1969',
        'Australia agreed an approximately 45 percent aim and 40 percent minimum sterling holding, under a specially defined reserve measure.',
        'Supports a meaningful sterling commitment, not a claim that sterling was necessarily more than half of every reserve definition.'),
    'IMF_FRANC_1969': source('The International Monetary Fund 1966-1971, Chapter 22: Adjustments in Rates for French Franc and Deutsche Mark (1969)', 'International Monetary Fund',
        'https://www.elibrary.imf.org/display/book/9781451971477/ch022.xml', '1996-02-29',
        'Names the 14 African operations-account partners, French overseas monetary areas, and Algeria/Morocco/Tunisia exceptions at the August 1969 franc devaluation.',
        'Native french_franc is France-only and lacks a franc-area reserve network. These countries receive an explicit generic fallback, not a fictitious dollar linkage.'),
    'IBEC_1963': source('General information and institutional chronology', 'International Bank for Economic Co-operation',
        'https://ibec.int/ru/about/general/', 'Undated institutional history',
        'Original 1963 members: Bulgaria, Hungary, GDR, Mongolia, Poland, Romania, USSR and Czechoslovakia. Transferable-rouble settlements began 1964. Cuba joined 1974 and Vietnam 1977.',
        'A transferable rouble was an accounting unit and differed from the domestic Soviet rouble. Native russia_rouble collapses those distinctions.'),
    'CBR_1961': source('History of the Bank of Russia, 1960 and 1961 chronology', 'Bank of Russia',
        'https://cbr.ru/about_br/history/', 'Undated institutional history',
        'Gosbank was the USSR-wide issue and settlement centre; the 1961 reform established the Soviet monetary unit used during 1970.',
        'The official 0.90 rouble/USD quotation is not a market valuation and must not be inserted as MD currency_strength.'),
    'BOC_RMB_1968': source('RMB Denominated Settlement Attempted to Maintain Foreign Exchange Value (1968-1976)', 'Bank of China',
        'https://www.boc.cn/en/aboutboc/ab7/200809/t20080926_1601854.html', '2008-09-26',
        'PRC foreign trade used chiefly sterling in capitalist markets and rouble accounting with socialist partners. RMB invoicing trials began 1968 but RMB was not exported as a circulating reserve.',
        'chinese_yuan is retained only as the PRC domestic accounting-unit exception, including its 1970 territorial monetary areas. No foreign client is assigned a modern international RMB reserve system.'),
    'SAFE_70YEARS': source("China's Foreign Exchange Administration Reform over the Past Seven Decades", 'Pan Gongsheng, State Administration of Foreign Exchange',
        'https://www.safe.gov.cn/en/2019/0930/1574.html', '2019-09-30',
        'Pre-reform RMB was a planning/accounting instrument; Soviet loans were repaid in 1964; external borrowing and FDI were very limited.'),
    'IMF_ALBANIA': source('Albania, Chapters II-III: Pre-Reform Economic System and Economic Performance', 'International Monetary Fund',
        'https://www.elibrary.imf.org/display/book/9781557752666/ch003.xml', '1992',
        'Albanian foreign exchange monopoly, Chinese loans largely denominated in roubles and the break with China in 1978.',
        'A rouble-denominated Chinese credit must not be mistaken for actual Soviet control or an international yuan-reserve law.'),
    'FRUS_CUBA_1964': source('Foreign Relations of the United States 1964-1968, Volume XXXII, Document 226', 'United States Department of State, Office of the Historian',
        'https://history.state.gov/historicaldocuments/frus1964-68v32/d226', '1964',
        'Contemporaneous record of Soviet-Cuban trade and credit support, alongside smaller convertible-currency reserves.',
        'Cuban rouble choice is a bilateral Soviet settlement abstraction, not a claim of 1970 CMEA/IBEC membership.'),
    'NIKH_DPRK_1970': source('North Korean foreign trade structure, 1970-1985', 'National Institute of Korean History, Korean History Database',
        'https://db.history.go.kr/diachronic/level.do?levelId=kn_027_0080_0040_0020', 'Undated institutional historical publication',
        'Official South Korean historical compilation reports Soviet Union 50.3 percent and communist countries 83.6 percent of DPRK trade in 1970.',
        'Trade destination is only a proxy for clearing orientation, not measured reserve composition or CMEA membership.'),
    'SLO_DINAR_HISTORY': source('History of exchange rates 1945-1998', 'Banka Slovenije',
        'https://www.bsi.si/sl/statistika/devizni-tecaji/zgodovina-deviznih-tecajev-1945-1998', 'Undated institutional historical series',
        'Yugoslav dinar Bretton Woods dollar/gold parity and 1966 redenomination. SFR Yugoslavia was not in the transferable-rouble monetary bloc.',
        'USD is an external convertible-settlement abstraction; Yugoslav citizens paid dinars, not dollars.'),
    'QCB_CURRENCY': source('History of Banknotes', 'Qatar Central Bank',
        'https://www.qcb.gov.qa/en/Pages/HistoryOfBanknotes.aspx', 'Undated institutional history',
        'Qatar-Dubai riyal began 1966; separate Qatari riyal and UAE dirham belong to 1973.'),
    'CBUAE_HISTORY': source('Our History, 1973 Currency Board entry', 'Central Bank of the United Arab Emirates',
        'https://centralbank.ae/en/about/about-cbuae/our-history/', 'Undated institutional history',
        'Dirham replaced Bahraini dinar and Qatar-Dubai riyal in 1973. No UAE dirham is backdated to January 1970.'),
    'BNM_HISTORY': source('Significant milestones in the Malaysian Foreign Exchange Market', 'Bank Negara Malaysia',
        'https://www.bnm.gov.my/web/guest/significant-milestones-in-the-malaysian-foreign-exchange-market', 'Undated institutional history',
        '1967 Malaysian dollar issue and 1968-1970 sterling intervention quotations; also demonstrates why a peg and reserve portfolio must be distinguished.'),
    'LIE_1924': source('100 Jahre Schweizer Franken feierlich gewuerdigt', 'Government of Liechtenstein',
        'https://medienportal.regierung.li/medienportal-medium/16182/231910/0/medienmitteilung', '2024-04-11',
        'Swiss franc adopted as legal currency in Liechtenstein in April 1924, preceding the 1980 treaty.'),
    'RBA_PNG_1975': source('Annual Report 1975: Papua New Guinea', 'Reserve Bank of Australia',
        'https://www.rba.gov.au/publications/annual-reports/rba/1975/papua-new-guinea.html', '1975',
        'PNG and Australia shared a monetary area; kina introduced in April 1975, replacing Australian dollar by January 1976.',
        'GBP is an inherited Australian external-reserve commitment proxy because no AUD law exists; it is not PNG domestic legal tender.'),
    'BPNG_CURRENCY': source('Currency: History of Exchange in PNG', 'Bank of Papua New Guinea',
        'https://www.bankpng.gov.pg/currency', 'Undated institutional history',
        'Australian dollar preceded 1975 kina; traditional exchange media also persisted.'),
    'OKINAWA_1958': source('September 16, 1958: Legal currency changes from B-yen to dollar', 'Okinawa Prefectural Archives',
        'https://www.archives.pref.okinawa.jp/news/that_day/4578', 'Undated archival history',
        'US dollar was legal tender from September 1958 until the May 1972 reversion to Japan.'),
    'BCD_1949': source('Historique du Franc Djibouti', 'Banque Centrale de Djibouti',
        'https://banque-centrale.dj/historique-du-franc-djibouti/', 'Undated institutional history',
        'Djibouti franc established 1949 with dollar-based parity, distinct from the French CFA-franc arrangements.'),
    'WB_NEPAL_1969': source('Nepal economic report, Table 3.7 International Reserves', 'World Bank; table source Nepal Rastra Bank',
        'https://documents1.worldbank.org/curated/en/209051468291043046/pdf/multi0page.pdf', 'Historical report includes 1969-1979 series',
        '1969 reserves included a substantial Indian-rupee component and non-rupee foreign exchange.',
        'A USD external-settlement fallback does not claim all holdings were dollars. Indian rupee is absent from native currency choices.'),
    'WB_BURMA_1966': source('Economic Committee Papers: Burma, IDA Operations', 'World Bank Group Archives, folder 30275795',
        'https://thedocs.worldbank.org/en/doc/088040125349920022-0560011966/original/WorldBankGroupArchivesfolder30275795.pdf', '1966',
        'Burma left the Sterling Area in October 1966; subsequent strong sterling use must not be labelled formal continued membership.'),
    'SARB_HISTORY': source('History and chronology', 'South African Reserve Bank',
        'https://www.sarb.co.za/en/home/about-us/history', 'Undated institutional history',
        'Rand introduced 1961. USD in this dataset means external convertible reserve/settlement alignment, not domestic dollarisation.'),
    'BCB_REAL_1994': source('The Real Plan', 'Banco Central do Brasil',
        'https://www.bcb.gov.br/en/monetarypolicy/realplan', 'Undated institutional history',
        'Brazilian real began July 1994 and is anachronistic for the 1970 slot.'),
    'BCB_STANDARDS': source('A Synthesis of Brazilian Monetary Standards', 'Museum of Money, Banco Central do Brasil',
        'https://www.bcb.gov.br/ingles/museu-espacos/ASynthesisBrazilianMonetaryStandards.pdf', '2007-05',
        'On January 1, 1970 Brazil used the cruzeiro novo, whose name reverted to cruzeiro in May 1970.'),
    'CBVS_1971': source('Jaarverslag 1971', 'Centrale Bank van Suriname',
        'https://www.cbvs.sr/images/content/annual-reports/Jaarverslag%201971.pdf', '1971',
        'Surinamese guilder was a distinct unit with its own gold/dollar parity, not automatically the Netherlands guilder.',
        '1971 account describes a later parity change; used to avoid conflating currencies, not to backdate the change.'),
    'CBI_HISTORY': source('History of the Central Bank of Iraq', 'Central Bank of Iraq',
        'https://www.cbi.iq/page/39', 'Undated institutional history',
        'The central bank dates the move from the sterling link to a USD2.80-per-dinar link to1959, followed by banking nationalisation in1964.',
        'This establishes an institutional exchange anchor, not a precise1969 currency breakdown of the reserve portfolio.'),
    'BOE_IRAQ_1959': source('OV23/25: Iraq financial relations with the UK', 'Bank of England Archive',
        'https://www.bankofengland.co.uk/CalmView/Record.aspx?id=OV23%2F25&src=CalmView.Catalog', '1959-06-01 to1959-07-29',
        'Contemporary records identify Iraq departure from the Sterling Area on23June1959.'),
    'WB_IRAQ_1974': source('Current Economic Position and Prospects of Iraq, Report419a-IRQ, Table3.5', 'O. Maiss and A. Zaman, World Bank; reserve table from CBI and IMF',
        'https://documents1.worldbank.org/curated/en/888911468283504398/pdf/multi-page.pdf', '1974-10-09',
        'Historical1969 reserve table separates gold, IMF position and foreign exchange, with no bilateral-agreement assets reported in that year.',
        'Foreign-exchange values are expressed in USD, not classified wholly as USD-denominated holdings. Later1972 debt composition must not be backdated.'),
    'WB_EGY_1971': source('Current Economic Position and Prospects of the United Arab Republic, ReportEMA-29a', 'World Bank mission led by A. Karaosmanoglu',
        'https://documents1.worldbank.org/curated/en/167311468025735892/pdf/multi-page.pdf', '1971-06-09',
        'Mission ofMay-June1970 documents1969 foreign reserves, Arab hard-currency assistance, commercial-bank borrowing and bilateral-clearing deficits.',
        'USD option represents only convertible settlement within a mixed system. Neither Soviet aid nor dollar-reporting units prove an exclusive reserve currency.'),
    'IMF_SYR_DUAL': source('Dual Markets: The Case of the Syrian Arab Republic', 'International Monetary Fund, IMF Staff Papers1975 Issue002',
        'https://www.elibrary.imf.org/view/journals/024/1975/002/article-A006-en.xml', '1975',
        'Country-specific account of1969-1970 official/parallel dollar exchange markets and theApril1970 foreign-exchange budget.',
        'Dollar intervention is a settlement proxy, not a verified dollar-only portfolio. The1971 liberalisation and1973 unification are not starting conditions.'),
    'CBL_EXCHANGE_HISTORY': source('Exchange Rate Policy: historical chronology', 'Central Bank of Libya',
        'https://cbl.gov.ly/en/exchange-rate-policy/', 'Undated institutional history',
        'Libyan pound was established at sterling parity in1952. Libya did not follow sterling devaluation in1967; a later explicit USD peg dates to1973.',
        'Sterling reserve alignment is supported separately by actual Bank of England guarantee records, not inferred solely from an exchange peg.'),
    'OECD_TUR_1970': source('OECD Economic Surveys: Turkey1970, December, pp22-24', 'Organisation for Economic Co-operation and Development',
        'https://www.oecd.org/content/dam/oecd/en/publications/reports/1970/12/oecd-economic-surveys-turkey-1970_g1g16e57/eco_surveys-tur-1970-en.pdf', '1970-12',
        'Contemporaneous survey records official9TL/USD parity since1960 and multiple rates before theAugust1970 reform.',
        'The August1970 devaluation and later rates are not backdated. An exchange anchor does not establish a reserve-asset share.'),
    'FRUS_SAU_1970': source('FRUS1969-1976 VolumeXXIV Document141: Telegram from Embassy in Saudi Arabia', 'United States Embassy Jidda; Department of State Office of the Historian',
        'https://history.state.gov/historicaldocuments/frus1969-76v24/d141', '1970-05',
        'Contemporary diplomatic reporting discusses the risk of Arab conversion of dollar reserves and moving deposits out of the United States.',
        'Evidence of an existing dollar-financial channel, not a complete SAMA portfolio. Later1974 US-Saudi arrangements are not backdated.'),
    'IMF_SAU_1974': source('The Economy and Finances of Saudi Arabia', 'International Monetary Fund, IMF Staff Papers1974 Issue002',
        'https://www.elibrary.imf.org/view/journals/024/1974/002/article-A001-en.xml', '1974',
        'Retrospective country account documents SAMA foreign-exchange assets,1968-1969 reserve declines and1960 riyal parity.',
        '1973 reserve-composition percentages are not inserted as1970 data.'),
    'NATIVE_DEFINITIONS': dict(title='Current MD reserve_currency law and issuer definitions', author='Millennium Dawn upstream and IMPERIA COLD WAR contributors',
        paths=['common/ideas/AA_law_expanded_economics.txt', 'common/ideas/COLDWAR_FRF_ITL_currencies.txt',
               'common/scripted_effects/00_currency_effects.txt', 'common/scripted_triggers/00_economic_triggers.txt'],
        accessed='2026-10-23', licence='See upstream notices and IMPERIA_COLD_WAR_NOTICE.md. Original author for each block not fully identified.',
        supports='Native law IDs, availability and on_add no_foreign_reserve behaviour. Local runtime authority, not historical evidence.'),
}

# Current native map sometimes gives a releasable a placeholder capital.
parent_overrides = {'SAZ': 'PER', 'TLS': 'AZE', 'PAP': 'AST', 'RYU': 'USA', 'TUA': 'MAL'}
ussr = set('ARM AZE BLR EST GEO KAZ KYR LAT LIT MLV TAJ TRK UKR UZB SOV'.split())
sterling = set('ANT AST BAH BAN BAR BHR BLZ BOT BRM BRU CYP DMI ENG FIJ GAH GAM GRA GUY HKG ICE IRE JAM JOR KEN KIR KUW LBA LES MAY MLD MLT MLW MRT NAU NIG NZL OMA PAK PAP QAT RAJ SAM SEY SIE SIN SOL SRI STH STK STL STV SYE TNZ TON TRI TUL UAE UGA VAN ZAM'.split())
franc = set('ALG BEN BFA CAM CAR CDI CHA CNG COM FGU GAB MAD MAL MAU MNC MOR MTE NGR SEN TOG TUN ANJ'.split())
clearing = set('BUL CZE HUN MON POL ROM CUB NKO VIE'.split())
fictional = set('ADS ALN C01 ZOM'.split())
de_facto = set('BIA ZIM'.split())
non_sovereign_active = ussr - {'SOV'} | set('BHR BRU PAL QAT UAE'.split())
records = {}

for country in inventory['countries']:
    tag, name = country['tag'], country['name']
    parent = parent_overrides.get(tag, geography[tag].get('owner') or tag)
    area = 'SOV' if parent in ussr else parent
    status = 'historical_state'
    if tag in fictional:
        status = 'fictional_or_technical_fallback'
    elif tag in de_facto:
        status = 'historical_de_facto_state'
    elif not country['active_1970'] or tag in non_sovereign_active:
        status = 'territorial_1970_baseline_for_later_or_separate_tag'

    idea, confidence, ids = 'us_dollar', 'medium_model_proxy', ['IMF_1970_RATES', 'IMF_1970_LIQUIDITY']
    rationale = ('USD represents convertible external reserve and settlement orientation within the 1970 dollar-centred system. '
                 'This does not replace the domestic currency and is not a verified all-dollar reserve portfolio.')
    if tag in fictional:
        idea, confidence, ids = 'no_foreign_reserve', 'technical_not_historical', []
        rationale = 'No historical 1970 sovereign monetary authority exists for this fictional or utility tag. Use the neutral native fallback, not an invented reserve claim.'
    elif tag == 'FRA':
        idea, confidence, ids = 'french_franc', 'high_domestic_law_exception', ['IMF_FRANC_1969']
        rationale = 'France-only native domestic franc law retained. France had gold and foreign reserves; native no_foreign_reserve=1 is a mechanical domestic-law flag, not evidence of no foreign assets.'
    elif tag == 'ITA':
        idea, confidence, ids = 'italian_lira', 'high_domestic_law_exception', ['IMF_1970_RATES']
        rationale = 'Italy-only native domestic lira law retained. Native no_foreign_reserve=1 is the existing domestic-law convention, not a claim that Italy held no dollars or gold.'
    elif tag == 'DDR':
        idea, confidence, ids = 'ddr_mark', 'high_domestic_law_exception', ['IBEC_1963']
        rationale = 'Native DDR domestic Mark law retained. DDR also participated in transferable-rouble clearing, but the one native slot cannot display both. The domestic Mark was not a convertible reserve.'
    elif tag == 'HOL':
        idea, confidence, ids = 'gulden', 'high_domestic_law_exception', ['IMF_1970_RATES']
        rationale = 'Native Netherlands guilder issuing-country law retained. The Netherlands still held international reserve assets; this is the native domestic-currency exception.'
    elif tag in {'SWI', 'LIC'}:
        idea, confidence, ids = 'swiss_frank', 'high_domestic_law_exception', ['LIE_1924', 'IMF_1970_RATES']
        rationale = 'Swiss franc domestic monetary area. Liechtenstein had used the Swiss franc since 1924; this does not backdate the later 1980 formal treaty.'
    elif area == 'GER':
        idea, confidence, ids = 'deutsche_mark', 'high_domestic_law_exception', ['IMF_1970_RATES', 'IMF_FRANC_1969']
        rationale = 'Federal German Deutsche Mark monetary area, including territorial releasables. Native domestic/issuer exception; not a claim that West Germany kept its reserves in its own liability.'
    elif tag == 'JAP':
        idea, confidence, ids = 'japanese_yen', 'high_domestic_law_exception', ['IMF_1970_RATES', 'IMF_1969_ASIA']
        rationale = 'Native Japanese yen issuing-country law retained. Japanese external settlement was heavily dollar-based; the native one-slot system uses the domestic currency for its own issuer.'
    elif area == 'CHI':
        idea, confidence, ids = 'chinese_yuan', 'high_domestic_law_exception', ['BOC_RMB_1968', 'SAFE_70YEARS']
        rationale = 'PRC domestic renminbi accounting area. It is not an internationally convertible yuan-reserve network in 1970. Do not assign the later yuan internationalisation variants.'
        if tag == 'OMG':
            rationale += ' Native tag name says Outer Mongolia, but capital556 and actual territory are Inner Mongolia in the PRC; independent Mongolia is MON.'
    elif area == 'SOV' or area in clearing:
        idea, confidence, ids = 'russia_rouble', 'high_clearing_proxy', ['CBR_1961', 'IBEC_1963']
        rationale = 'Soviet domestic monetary area or original CMEA transferable-rouble clearing orientation. Native russia_rouble combines domestic roubles and the separate clearing accounting unit.'
        if area == 'CUB':
            confidence, ids = 'medium_bilateral_proxy', ['FRUS_CUBA_1964', 'IBEC_1963']
            rationale = 'Soviet bilateral trade and credit settlement alignment. Cuba was not yet an IBEC member in January 1970; the native rouble law is a bilateral-clearing proxy, not evidence of CMEA reserve holdings.'
        elif area == 'NKO':
            confidence, ids = 'medium_bilateral_proxy', ['NIKH_DPRK_1970', 'IBEC_1963']
            rationale = 'Soviet-oriented bilateral socialist clearing proxy, supported by the USSR share of 1970 trade. North Korea was not an IBEC member; actual reserve composition is not verified.'
        elif area == 'VIE':
            confidence, ids = 'low_bilateral_proxy', ['IBEC_1963', 'BOC_RMB_1968']
            rationale = 'North Vietnamese socialist bilateral-clearing proxy, not a freely convertible reserve holding. Soviet and Chinese support coexisted; Vietnam did not enter IBEC until1977. No claim of an exclusive Soviet reserve portfolio.'
    elif tag in sterling or area in sterling:
        idea, confidence, ids = 'british_pound', 'high_reserve_or_settlement_alignment', ['BOE_OV44', 'BOE_1969', 'BOE_1974']
        rationale = 'Documented sterling-area reserve commitment or inherited territorial monetary arrangement around 1970. GBP represents reserve/settlement dependence, not necessarily domestic legal tender or an all-sterling portfolio.'
        if area == 'BRM':
            ids, confidence = ['IMF_1969_ASIA', 'WB_BURMA_1966'], 'medium_recent_settlement_proxy'
            rationale = 'Burma left the formal Sterling Area in October1966. Country-supplied 1967 settlement data nevertheless show strong sterling use, retained as a near-date settlement proxy; no formal 1970 membership is claimed.'
        elif tag in {'AST', 'PAP', 'NAU'}:
            ids, confidence = ['RBA_1969', 'RBA_PNG_1975', 'BPNG_CURRENCY'], 'medium_reserve_commitment_proxy'
            rationale = 'Australian/Pacific monetary baseline with a substantial binding Australian sterling-reserve commitment. No AUD option exists. GBP is external reserve orientation, not a claim that Australian or PNG citizens paid in sterling in 1970.'
        elif tag in {'QAT', 'UAE', 'BHR'}:
            ids += ['QCB_CURRENCY', 'CBUAE_HISTORY']
            rationale += ' The 1973 UAE dirham and independent Qatari riyal are not backdated; the Qatar-Dubai riyal/Bahraini dinar arrangements preceded them.'
        elif area == 'MAY':
            ids += ['BNM_HISTORY']
        elif area == 'RAJ':
            ids += ['IMF_1969_ASIA']
            rationale += ' India also held gold and dollars and operated bilateral clearing arrangements. This is the one-slot sterling-commitment abstraction, not uniform reserve composition.'
        elif tag == 'BAN':
            rationale += ' Bangladesh was East Pakistan in January1970. This baseline inherits Pakistan rather than inventing a separate Bangladeshi reserve authority.'
    elif tag in franc or area in franc or area == 'FRA':
        idea, confidence, ids = 'no_foreign_reserve', 'explicit_native_option_gap', ['IMF_FRANC_1969']
        rationale = 'French-franc area, local franc or operations-account baseline. Native french_franc is France-only and no CFA/CFP or French settlement reserve law exists. Generic native fallback avoids falsely paying a USD reserve-network bonus. It does not mean zero foreign reserves.'
        if area in {'ALG', 'MOR', 'TUN'}:
            rationale += ' Unlike operations-account partners, Algeria, Morocco and Tunisia did not follow the 1969 French devaluation; their distinct national arrangements are not claimed to be identical to CFA membership.'
    elif area in {'ITA', 'HLS', 'SMA'} or tag in {'ADO', 'BHU', 'BIA', 'ALB', 'ZIM'}:
        idea, confidence, ids = 'no_foreign_reserve', 'explicit_native_option_gap', ['IMF_1970_RATES']
        rationale = 'The applicable local monetary arrangement has no matching native foreign-reserve option. Generic fallback avoids inventing foreign reserve dependence; it does not establish an absence of international assets.'
        if tag == 'ALB':
            ids = ['IMF_ALBANIA']
            rationale = 'Autonomous Albanian lek and state foreign-exchange monopoly with Chinese bilateral credits. Neither Soviet reserve-network membership nor international yuan reserves is accurate; Chinese rouble-denominated credit is not Soviet issuance.'
        elif tag == 'BIA':
            confidence = 'low_wartime_fallback'
            rationale = 'Biafra remained a blockaded de facto state on January1,1970 with its own wartime pound. Its name alone does not prove participation in British sterling guarantees. Native neutral fallback avoids that unsupported claim.'
        elif tag == 'ZIM':
            confidence = 'medium_sanctioned_fallback'
            rationale = 'UDI Rhodesia operated its own pound in January1970 under sanctions; Rhodesian dollar arrived later in1970. A native neutral domestic fallback avoids falsely claiming access to ordinary British reserve guarantees.'
        elif tag == 'BHU':
            rationale = 'Bhutan used Indian rupees before its later ngultrum. No INR option exists; a local fallback avoids inventing British or US reserve-network membership.'
        elif tag == 'ADO':
            rationale = 'Andorra used French francs and Spanish pesetas. No dual-currency law exists and France-only french_franc cannot be assigned here; native fallback does not imply a nonexistent Andorran currency or zero foreign assets.'
    elif area == 'SER':
        ids = ['SLO_DINAR_HISTORY', 'IMF_1970_RATES']
        rationale = 'SFR Yugoslav dinar monetary baseline and convertible external dollar/gold settlement. Yugoslavia was nonaligned; do not confuse a socialist government with Soviet transferable-rouble membership.'

    # Specific external-settlement exceptions to territorial parent inheritance.
    if tag == 'DJI':
        idea, confidence, ids = 'us_dollar', 'high_currency_backing_proxy', ['BCD_1949']
        rationale = 'French Afars and Issas used the dollar-linked Djibouti franc created in1949, rather than the CFA franc. Native USD represents the underlying external anchor.'
    elif tag == 'RYU':
        idea, confidence, ids = 'us_dollar', 'high_legal_tender', ['OKINAWA_1958']
        rationale = 'US-administered Ryukyu/Okinawa used US dollars as legal tender from1958 until Japanese reversion in1972. Native JAP ownership must not backdate the yen.'
    elif tag in {'NLA', 'SUR'}:
        idea, confidence, ids = 'us_dollar', 'medium_external_settlement_proxy', ['IMF_1970_RATES', 'CBVS_1971']
        rationale = 'Distinct Antillean/Surinamese guilder arrangement, not the Netherlands guilder. USD is an external convertible-settlement fallback; no Antillean or Surinamese guilder law exists.'
    elif tag in {'NEP', 'NPM'}:
        idea, confidence, ids = 'us_dollar', 'medium_external_settlement_proxy', ['WB_NEPAL_1969', 'IMF_1970_RATES']
        rationale = 'Nepal held Indian rupees as well as other foreign exchange. No INR law exists; USD represents the convertible external component, not Nepalese domestic currency, sterling membership or an all-dollar portfolio.'
    elif tag in {'SAF', 'NAM', 'SWA'}:
        idea, confidence, ids = 'us_dollar', 'medium_external_settlement_proxy', ['SARB_HISTORY', 'IMF_1970_RATES']
        rationale = 'Rand monetary area with gold and convertible external assets. No rand law exists; USD is an external-settlement proxy, not domestic dollarisation. Botswana/Lesotho have separate documented sterling reserve commitments.'
    elif tag in {'BRA', 'SPL', 'SUL'}:
        idea, confidence, ids = 'us_dollar', 'medium_external_settlement_proxy', ['BCB_REAL_1994', 'BCB_STANDARDS', 'IMF_1970_RATES']
        rationale = 'Brazil used cruzeiro novo on January1,1970. Native brazilian_real would backdate1994. USD represents external reserve/settlement orientation without inventing a new law.'

    if tag == 'EUU':
        status = 'territorial_1970_baseline_for_later_or_separate_tag'
        rationale = 'A later European union tag receives the Belgian/Western European territorial convertible-settlement baseline. No sovereign EU reserve authority or euro existed in January 1970; this does not invent one.'

    # Country-specific secondary audit. Choice remains unchanged; stronger provenance.
    country_reviews = {
        'IRQ': (['CBI_HISTORY', 'BOE_IRAQ_1959', 'WB_IRAQ_1974'],
                'Iraq left the Sterling Area in1959 and its central bank records a dollar exchange link from that year. Gold and convertible reserves coexisted. USD remains the convertible-settlement choice; Soviet loans do not make Iraq an original transferable-rouble member.'),
        'EGY': (['WB_EGY_1971'],
                'Egypt operated a mixed system: scarce convertible foreign exchange, Arab financial transfers, European commercial-bank borrowing and large bilateral-clearing liabilities. USD represents the convertible component. Soviet military support does not establish exclusive rouble reserves.'),
        'SYR': (['IMF_SYR_DUAL'],
                'Syrian official and parallel foreign-exchange markets used dollar intervention quotations in1969-1970 alongside exchange controls. USD represents convertible-market settlement; Baathist rule and Soviet aid do not by themselves establish transferable-rouble membership.'),
        'LBA': (['CBL_EXCHANGE_HISTORY'],
                'Libya retained a domestic pound, had actual sterling reserve-guarantee arrangements, and did not follow the1967 sterling devaluation. GBP represents the reserve relationship, not a claim that a new dollar peg from1973 already applied.'),
        'TUR': (['OECD_TUR_1970'],
                'Turkey used a dollar-anchored, controlled and multiple-rate exchange system at the start of1970. USD represents external convertible settlement. The August1970 devaluation is not a January starting value.'),
        'SAU': (['FRUS_SAU_1970', 'IMF_SAU_1974'],
                'SAMA held substantial convertible foreign assets; contemporary1970 reporting specifically discusses dollar reserves and deposits. USD represents that channel. No later1974 petrodollar arrangement or exact reserve percentage is backdated.'),
    }
    if tag in country_reviews:
        new_ids, rationale = country_reviews[tag]
        ids += new_ids

    if status.startswith('territorial'):
        rationale = f'1970 territorial monetary baseline for {name}, using {parent}; not a claim that this tag had an independent reserve authority. ' + rationale
    if tag in parent_overrides:
        rationale += f' Geographic correction: use {parent} baseline rather than the current history capital owner {geography[tag].get("owner")}; see currency_capital_baselines.json and recorded exceptions.'
    if tag == 'TUA':
        rationale += ' Tuareg cores cross several monetary areas. Mali/franc-area is the documented majority-core fallback, not a claim of a single historical Tuareg reserve bank.'

    records[tag] = dict(name=name, history_path=country['path'], reserve_currency=idea,
                        no_foreign_reserve=int(idea in {'no_foreign_reserve', 'ddr_mark', 'french_franc', 'italian_lira'}),
                        currency_strength_action='retain_existing_else_native_startup_default',
                        status=status, territorial_baseline=parent, confidence=confidence,
                        rationale=rationale, source_ids=ids + ['NATIVE_DEFINITIONS'])
    if tag in fictional:
        records[tag].update(reserve_currency=None, no_foreign_reserve=None,
                            status='pending_user_decision_no_history_changes_authorized',
                            confidence='not_applicable',
                            recommended_action='leave_current_history_unchanged',
                            rationale='Show this fictional/technical tag to the user first. No new 1970 currency value is proposed or authorized.')

assert set(records) == {c['tag'] for c in inventory['countries']}
assert len(records) == 397
for tag, r in records.items():
    if r['status'] == 'pending_user_decision_no_history_changes_authorized':
        assert r['reserve_currency'] is None and r['no_foreign_reserve'] is None
        continue
    assert r['reserve_currency'] in inventory['native_ideas']['reserve_currency']
    assert r['reserve_currency'] not in {'euro', 'bitcoin', 'brazilian_real', 'chinese_yuan_2', 'chinese_yuan_3'}
    assert r['reserve_currency'] != 'french_franc' or tag == 'FRA'
    assert r['reserve_currency'] != 'italian_lira' or tag == 'ITA'
    assert r['reserve_currency'] != 'ddr_mark' or tag == 'DDR'
    assert r['reserve_currency'] != 'swiss_frank' or tag in {'SWI', 'LIC'}
    assert all(s in sources for s in r['source_ids'])

output = dict(project='IMPERIA COLD WAR', feature='1970 native reserve-currency-slot research',
              effective_date='1970.1.1',
              interpretation='One native law is a reserve/settlement-alignment abstraction with existing domestic-currency exceptions. It is not a literal reserve portfolio or debt-denomination ledger.',
              numeric_policy='Do not fabricate reserve percentages or currency_strength. Preserve existing calibrated values and rely on native startup default if absent.',
              no_foreign_reserve_policy='Match the native on_add value. All issuer-network laws set0, including their home issuers. Generic, DDR, FRF and ITL domestic laws set1. This is an engine variable, not a claim about actual foreign assets.',
              allowed_checks=dict(forbidden_1970_laws=['euro', 'bitcoin', 'brazilian_real', 'chinese_yuan_2', 'chinese_yuan_3'],
                                  tag_restrictions={'french_franc':['FRA'],'italian_lira':['ITA'],'ddr_mark':['DDR'],'swiss_frank':['SWI','LIC']},
                                  russia_rouble='Native available requires SOV/faction membership when purchasing. Historical initialization can grant this non-cancelling law to historically rouble-using releasables without inventing a new diplomatic faction.',
                                  all397_native_ideas_resolve=True),
              pending_tags=sorted(fictional),
              source_registry=sources, counts=dict(Counter(r['reserve_currency'] or 'pending_user_decision' for r in records.values())), records=records)
(HERE / 'currency.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps(output['counts'], indent=2))
print(f'{len(records)} currency assignments written; live history unchanged.')
