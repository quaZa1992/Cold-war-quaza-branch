# IMPERIA COLD WAR: Karelia and Mali uranium deposits

The 24 October 2026 request adds LOW mining capacity in Karelia and HIGH capacity at documented Malian uranium sites. These are geographic and balance additions to the existing mine system. They give no raw uranium, completed mines, money or construction. Normal construction, investment, maintenance, damage and resource reconciliation continue to determine production.

| Current state | Geological locations | Requested band | Maximum mine levels | Base uranium per working level | Maximum base output |
| --- | --- | --- | --- | --- | --- |
| 1128, Karelia | Srednyaya Padma / Zaonezhye and Karku / northeastern Lake Ladoga | LOW | 1 | 3 | 3 |
| 1164, Gao | Samit / Tilemsi-Gao basin | HIGH | 3 | 9 | 27 |
| 1166, Kayes | Falea / Kenieba and the associated Loulo occurrence | HIGH | 3 | 9 | 27 |

HIGH and LOW describe the requested game balance. They are not ore grades, historical production or reserve estimates. In particular, Samit's reported geological resource is substantially smaller than Falea's. Giving both the requested HIGH band does not assert equivalent deposits. Multiple sites within one state share the listed capacity; they do not grant additional copies. Kidal / Adrar des Iforas is an exploration province rather than an additional individually established deposit in this change.

The state allocation uses the current province membership and map, rather than modern administrative subdivisions. Karelia state 1128 contains the Petrozavodsk, Kondopoga and Sortavala districts. Western Malian sites belong to Kayes state 1166; Samit lies northeast of Gao in state 1164. These are regional allocations on the stylised game map, not mine-coordinate overlays. No provinces, borders, owners or state histories are changed.

Historical chronology remains separate from campaign access. Srednyaya Padma was discovered in 1985, Karku in 1989 and Falea in 1977. The exact discovery years of Samit and Loulo were not established in the consulted sources. Samit is explicitly documented in the French Senate's 2013 Mali report. Earlier recognition of regional potential is not treated as discovery of a specific deposit. These three added states are therefore recorded in `rp_geographic_additions`, separately from the 57 districts supported by the existing January 1970 knowledge cutoff.

`build_1970_deposits.py` emits the dated district block and the additional Karelia/Mali block from the same research register. A separate, persistent startup flag applies the new block once in both new and loaded campaigns without rerunning the original global deposit table. The existing startup reconciliation then opens the correct number of mine levels. The deposit helper only initializes missing output bookkeeping; reapplication does not erase mine output already accounted for. Existing mine costs and weekly accounting are reused.

Sources, authors and rights:

- [IAEA URAM 2018: Uranium deposits of the Karelian-Kola province](https://conferences.iaea.org/event/146/contributions/5315/), Elena Afanasyeva, Russian Geological Research Institute: geological districts and ore types. Copyright remains with the authors/publisher; separate reuse permission is unknown. Only facts are paraphrased.
- [Institute of Geology, Karelian Research Centre: geological route 3](https://miningroads.igkrc.ru/route3.html), materials credited to P. V. Medvedev, D. V. Rychanchik, O. B. Lavrov and K. V. Shekov, 2017: Srednyaya Padma location and 1985 discovery. Separate reuse licence or permission is unknown. No text or imagery is copied.
- [National Library of the Republic of Karelia: 2014 anniversary calendar](https://library.karelia.ru/kalendar2014/html/ukazatel5.html), citing V. V. Shchiptsov's entry in the Karelia encyclopedia: Karku's 1989 discovery near the village in Pitkyaranta district. Separate reuse licence or permission is unknown.
- [IAEA URAM 2018: Falea](https://conferences.iaea.org/event/146/contributions/5232/), Jerome Randabel, GoviEx: Falea geology and 1977 discovery. The indexed abstract was consulted; direct retrieval was unavailable. Separate reuse licence or permission is unknown.
- [Denison Mines 2014 annual information filing](https://www.sec.gov/Archives/edgar/data/1063259/000106299315001288/exhibit99-1.htm), Denison Mines, filed with the US SEC in 2015: western Mali location and Cogema exploration in the 1970s. Separate reuse licence or permission is unknown.
- [Embassy of Mali in Japan: Mining and Hydrocarbons](https://www.ambamali-jp.org/eng/investment/mining/), Embassy of the Republic of Mali: Falea/Loulo in Kayes and Samit northeast of Gao. The source retains copyright; separate reuse permission is unknown. Its inconsistent oxide notation is not reproduced or used for game quantities.
- [French Senate: Mali, comment gagner la paix?](https://www.senat.fr/rap/r12-513/r12-51310.html), Senate report 513, 2013: Samit uranium resources in the Tilemsi basin. Individual section author and separate reuse licence are unknown.
- [IAEA TECDOC 1843, World Distribution of Uranium Deposits, 2016 edition](https://www-pub.iaea.org/MTCD/Publications/PDF/TE1843_web.pdf), IAEA, 2018: separate Falea and Samit entries, with very different resource bands. No report content or map imagery is bundled; separate reuse permission is unknown.

Runtime implementation credit remains quaZa's Feature Test, Workshop 3818306694, adapted through the existing Cold War integration. Underlying Millennium Dawn and Hearts of Iron IV rights remain with their respective authors. Separate redistribution licences for the inherited implementation are unknown. This change adds source records, generated deposit assignments and one guarded startup call; it adds no third-party artwork.

Verification on 24 October 2026: all 23 integration tests passed, including zero starting resources/mines, generated state capacities, the separate startup guard and repeated-application resource conservation. A native-engine game session was not run for this change.
