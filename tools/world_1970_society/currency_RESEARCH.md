IMPERIA COLD WAR

# Currency assignments for 1 January 1970

This is internal historical provenance, not player-facing localisation. The dataset is `currency.json`. It covers 397 country-history tags. Four records have no proposed value and must remain untouched pending the user's decision: ADS, ALN, C01 and ZOM. No country history or runtime provider is changed by this research package.

The existing MD law does several jobs at once. Some choices represent an external reserve/settlement orientation; its own issuers also use the same slot for their national money. France, Italy and East Germany have dedicated domestic choices. Consequently a historical assignment cannot be interpreted as either a census of domestic legal tender or an exact national reserve portfolio. This work preserves the current system as requested.

## Evidence and interpretation

The contemporary IMF [survey of exchange rates at the beginning of 1970](https://www.elibrary.imf.org/abstract/journals/022/0007/004/article-A003-en.xml) and [Annual Report 1970](https://www.elibrary.imf.org/display/book/9781616351823/ch002.xml) provide the system-wide dollar/sterling context. They do not prove that an individual country's entire reserve portfolio was in dollars. The general USD assignments are conservative model choices for convertible external settlement, not individually observed 100 percent dollar portfolios. Each such record identifies that uncertainty internally.

The [Bank of England OV44 archive catalogue](https://www.bankofengland.co.uk/calmview/Record.aspx?id=OV44&src=CalmView.Catalog) enumerates the countries and currency authorities involved in sterling guarantee arrangements. Its [1969 report](https://www.bankofengland.co.uk/-/media/boe/files/annual-report/1969/boe-1969.pdf) explains the reserve commitments. These support actual sterling dependence even where local people used rupees, dinars, shillings or domestic dollars. The [RBA 1969 report](https://www.rba.gov.au/publications/annual-reports/rba/1969/res-bank-policy.html) supplies direct Australian evidence. Australia's sterling commitment was substantial but was not necessarily a majority of every reserve definition.

Burma is a deliberate exception to a simple formal-area lookup. It left the Sterling Area in 1966, but country-supplied [IMF settlement data](https://www.elibrary.imf.org/view/journals/024/1969/003/article-A001-en.xml) show sterling still dominating its regional settlements in 1967. Its GBP assignment is a near-date settlement proxy, not a claim that formal membership continued.

The [IMF account of the 1969 franc devaluation](https://www.elibrary.imf.org/display/book/9781451971477/ch022.xml) identifies the African operations-account partners, overseas franc currencies and North African exceptions. The current `french_franc` law is France-only. There is no native CFA, CFP or general French settlement-area choice. The research therefore records the real franc relationship and proposes the existing generic local-law option where no applicable named option exists. This does not mean these countries lacked reserves. Assigning USD merely because the native list lacks CFA would incorrectly give the United States the reserve-network benefit for French monetary arrangements. No new laws or recurring logic are proposed.

The [IBEC institutional chronology](https://ibec.int/ru/about/general/) identifies its original members and the 1964 transferable-rouble system. Original CMEA members and the USSR territorial monetary area use native `russia_rouble`, except the existing dedicated DDR domestic Mark. Cuba, North Korea and North Vietnam are explicitly recorded as bilateral socialist-clearing proxies, not original IBEC members. Cuba entered IBEC in 1974 and Vietnam in 1977. The native law merges nonconvertible domestic roubles, transferable-rouble accounts and bilateral clearing; this source data does not pretend they were identical monetary instruments.

The [Bank of China history](https://www.boc.cn/en/aboutboc/ab7/200809/t20080926_1601854.html) specifically says renminbi was not exported as a circulating reserve in this period. `chinese_yuan` is limited to the PRC domestic monetary area and its territorial releasables. It is not spread to foreign states as if modern RMB internationalisation had happened in 1970.

## Dates and territory traps checked

- Brazil used cruzeiro novo on 1 January 1970. The [BCB monetary standards](https://www.bcb.gov.br/ingles/museu-espacos/ASynthesisBrazilianMonetaryStandards.pdf) date its renaming to May 1970. The [real began in 1994](https://www.bcb.gov.br/en/monetarypolicy/realplan). No Brazilian real is assigned.
- Qatar-Dubai riyal and Bahraini dinar predate the [UAE's 1973 dirham](https://centralbank.ae/en/about/about-cbuae/our-history/). The 1970 external orientation remains sterling; the future domestic dirham law is not backdated.
- [Djibouti's franc](https://banque-centrale.dj/historique-du-franc-djibouti/) was dollar-linked from 1949, unlike CFA francs. It receives USD despite French sovereignty in 1970.
- [Okinawa used actual US-dollar legal tender from 1958 to 1972](https://www.archives.pref.okinawa.jp/news/that_day/4578). Native Japanese state ownership must not backdate the yen.
- [PNG used Australian dollars before the kina](https://www.bankpng.gov.pg/currency). Its record uses the inherited Australian reserve relationship, not current capital-owner text as historical proof.
- Yugoslav successor territories inherit a [dinar and convertible-settlement baseline](https://www.bsi.si/sl/statistika/devizni-tecaji/zgodovina-deviznih-tecajev-1945-1998), not a Soviet-bloc currency based solely on socialism.
- Soviet republics and later breakaway tags use 1970 Soviet territorial monetary arrangements. This does not claim they were independent reserve authorities.
- GLC is an American Great Lakes union, capital Michigan. It is not an African Great Lakes state.
- OMG has a misleading native name, Outer Mongolia, but capital/state 556 is Inner Mongolia. MON represents independent Mongolia.
- SAZ's placeholder capital in Balochistan is not South Azerbaijan. Its East Azerbaijan core supports the Iranian baseline.
- TLS has a placeholder Scottish capital, while its Shirvan core is in the Azerbaijan SSR. Its monetary baseline is Soviet.
- Tuareg cores span multiple monetary areas. The predominant Mali/franc-area baseline is a modelling decision, not a historical Tuareg central bank.

The auxiliary `currency_capital_baselines.json` records local native geography for review. It is not an external historical source and is not trusted blindly where it conflicts with primary historical evidence or the tag's actual cores.

## Native integration constraints

All proposed law IDs resolve against the inventory and current local definitions. The builder rejects euro, bitcoin, Brazilian real and advanced yuan-internationalisation variants for this start date. It enforces the France-only, Italy-only, DDR-only and Switzerland/Liechtenstein restrictions.

Native rouble purchase availability requires SOV or faction membership. It has no cancellation rule that removes historical initialization from a later releasable. An initial historical law should not fabricate diplomatic faction membership merely to satisfy the purchase interface.

`no_foreign_reserve` must mirror native `on_add`, not be reinterpreted independently:

| Native choice | Variable |
| --- | ---: |
| USD, DEM, GBP, RUB, JPY, CHF, NLG, CNY | 0, including their home issuers |
| generic domestic, DDR Mark, French franc, Italian lira | 1 |

This variable changes MD's debt FX calculation. It is not a historical measurement of foreign reserves and cannot be set to 1 for every sovereign country merely because that country issued its own money.

No exact reserve shares or uncalibrated `currency_strength` values have been fabricated. Retain existing explicit values and the native startup default when a country lacks one. Official fixed exchange quotations, especially the Soviet accounting rate, are not equivalent to MD's dimensionless strength index.

## Provenance

Historical sources, authors, dates, URLs, limitations and access dates are recorded in the JSON source registry. Original source licences are unknown unless governed by an existing local notice. Research uses paraphrases and links rather than republishing source text or artwork. Dataset and builder modifications: original IMPERIA COLD WAR research and implementation preparation. Original MD code remains under its existing notices and attribution. See `IMPERIA_COLD_WAR_NOTICE.md`.
