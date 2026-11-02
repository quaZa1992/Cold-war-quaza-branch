IMPERIA COLD WAR

# Six-country monetary and startup audit

The secondary review changes source linkage and internal rationales only. The proposed law choices remain Iraq USD, Egypt USD, Syria USD, Libya GBP, Turkey USD and Saudi Arabia USD. No history or runtime source was edited by this research agent.

| Country | Primary evidence near the starting date | Consequence for the existing native slot |
| --- | --- | --- |
| Iraq | [CBI institutional history](https://www.cbi.iq/page/39) dates its dollar link to 1959. [BoE OV23/25](https://www.bankofengland.co.uk/CalmView/Record.aspx?id=OV23%2F25&src=CalmView.Catalog) records departure from the Sterling Area on 23 June 1959. [World Bank Report419a-IRQ](https://documents1.worldbank.org/curated/en/888911468283504398/pdf/multi-page.pdf), Table3.5, separates 1969 gold, IMF and foreign-exchange assets. | Keep USD for convertible external settlement. Neither an old sterling history nor Soviet loans imply a 1970 sterling guarantee or transferable-rouble regime. The table's USD reporting units are not reserve-denomination proof. |
| Egypt | [World Bank EMA-29a](https://documents1.worldbank.org/curated/en/167311468025735892/pdf/multi-page.pdf), based on a May-June1970 mission, describes 1969 reserve scarcity, Arab transfers, Western bank credits and large bilateral-clearing liabilities. | Keep USD as the convertible-settlement component of a mixed system. Do not claim a dollar-only reserve portfolio or equate Soviet military aid with exclusive rouble reserves. |
| Syria | [IMF, Dual Markets: The Case of the Syrian Arab Republic](https://www.elibrary.imf.org/view/journals/024/1975/002/article-A006-en.xml) describes the 1969-1970 official/parallel USD exchange markets and April1970 FX budget. | Keep USD as the convertible intervention/settlement component. Soviet support coexisted with it. Later liberalisation is not a starting condition. |
| Libya | [CBL exchange chronology](https://cbl.gov.ly/en/exchange-rate-policy/) records sterling parity in1952 and non-devaluation in1967; [BoE guarantee archive](https://www.bankofengland.co.uk/calmview/Record.aspx?id=OV44&src=CalmView.Catalog) independently establishes the reserve commitment. | Keep GBP. This follows actual reserve relationships, not merely domestic currency name or political sympathy after the1969 revolution. |
| Turkey | [OECD Economic Survey Turkey1970](https://www.oecd.org/content/dam/oecd/en/publications/reports/1970/12/oecd-economic-surveys-turkey-1970_g1g16e57/eco_surveys-tur-1970-en.pdf), pp22-24, gives the official9TL/USD parity since1960 and its pre-reform multiple rates. | Keep USD external orientation. Do not backdate the August1970 devaluation to January. |
| Saudi Arabia | [FRUS VolumeXXIV Document141](https://history.state.gov/historicaldocuments/frus1969-76v24/d141) discusses dollar reserves/deposits in contemporary1970 reporting. [IMF country study1974](https://www.elibrary.imf.org/view/journals/024/1974/002/article-A001-en.xml) provides the retrospective SAMA balance-sheet context. | Keep USD. No exact1970 reserve share is claimed; later1974 financial arrangements are not backdated. |

No quoted exchange rate is used as `currency_strength`. Native strength is a dimensionless economic index, not a historical nominal currency quotation.

## Startup providers checked

| Provider | Location at audit time | Currency result |
| --- | --- | --- |
| `COLDWAR_EGY_initialize_1970` | `common/scripted_effects/COLDWAR_EGY_1970_scripted_effects.txt:7`, called from EGY history:50 | Adds laws/factions/spirits, no reserve-law or strength mutation. |
| `COLDWAR_SYR_initial_profile`, `COLDWAR_SYR_politics_init` | `common/scripted_effects/COLDWAR_SYR_politics_effects.txt:5`, :29; initial profile called from SYR history:46 | Political state changes, no reserve-law or strength mutation. |
| `LBA_1970_initialize_system` | `common/scripted_effects/LBA_1970_scripted_effects.txt:136`, called from LBA history:54 | Supplies missing spending/political laws, no currency mutation. |
| `SAU_startup.1` | `events/SAU_events.txt:5`; SAU history:91 | Its history invocation belongs to2000, not the1970 snapshot. |
| `set_law_vars` | `common/scripted_effects/00_law_attitudes.txt:5` | No currency or `no_foreign_reserve` initialization. Explicit history value remains necessary because history ideas do not execute native `on_add`. |
| `currency_startup` | `common/scripted_effects/00_currency_effects.txt:54` | Fills missing strength/base with the native default and updates issuer flags. Special DDR/GER handling exists; no default currency overwrite for the six countries above. |
| Global reserve recount | `common/on_actions/00_on_actions.txt:1734` | Counts the history-law choices before the country economy pass. This reinforces using the existing flow, with no new recurring scan. |
| Country startup economy pass | `common/on_actions/00_on_actions.txt:1831` | Calls `currency_startup` before `ingame_update_setup`. |
| AI faction join/leave currency hooks | `common/on_actions/MD_on_actions.txt:1423` and :1473 | Joining a CHI/SOV/RUS/JAP/ENG-led faction can change currency; leaving can change it to USD. This is existing gameplay, not a proposed new updater. |
| `IMP_1970_setup_global_alignment_internal` | `common/scripted_effects/IMP_1970_world_politics_effects.txt:1205`; public wrapper:1387 | Initial NATO is USA-led, the Arab command EGY-led. Neither leader triggers the listed join auto-switches, so the six seeds are not changed by those initial joins. |

Source authors, access dates, licences and limitations are recorded in `currency.json`. Local source locations refer to the audited shared-workspace version and may move when the parent integrates history blocks.
