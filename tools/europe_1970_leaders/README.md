IMPERIA COLD WAR: German leadership and Eastern portraits

Implemented in the working mod. West Germany has 44 country-person entries and East Germany has 46. Gysi, Bisky and Merkel share one portrait each across both countries: 87 distinct people and 95 party-specific choices.
The portrait pass installs 112 distinct people: 87 German figures and 25 existing SSR/Eastern Bloc/Soviet figures. 106 use AI restoration; 3 retain their previously approved original DDS textures unchanged. Three use their identified original period photographs after the image service rejected restoration: Björn Engholm, Günther Maleuda and Johannes Käbin.

Willy Brandt, Walter Ulbricht and Leonid Brezhnev use the exact original textures from commit 34fb12b2bfab7f33b4a4ba066baeaa770a123998. Their native bindings and save-compatible portrait aliases are restored byte-for-byte. approved_portraits.json pins the source hashes, and regeneration verifies and copies these approved inputs without image processing. Their small selector icons are derived from those original portraits.

## Player behaviour

- Free, repeatable native leadership selections appear for the actual governing party in the 1970 scenario. Historical terms, age and calendar death flags do not lock human selections.
- Selections are remembered per party. Existing West German CDU/CSU, FDP and SPD indices keep their native focus/event meanings. The late authoritarian National Directorate retains its existing route.
- East German personal SED profile flags follow the actual incumbent in the actual SED slot. Leaving that slot clears the personal profile; selecting a profile again restores it. Hoffmann and Keßler remain distinct. Earned focus-dependent leader traits are reapplied when the selected profile is recreated.
- Existing AI appointments and calendar succession, other bookmarks, party identities and hypothetical routes are retained. No new religious party slots, collective substitute people or military recruitment are added.
- The HOI4 portrait represents the selected political figure. Choosing Heinemann, Carstens, Weizsäcker, Herzog or Bergmann-Pohl does not implement a separate constitutional presidential office or historical term.
- Reconciliation uses startup and two country-specific monthly hooks, for GER and DDR. No new daily or weekly pulse and no recurring world-country scan are introduced.
- All new localisation is English. IDs and runtime files use the COLDWAR prefix.

## Integration and duplicate prevention

The central MD dispatcher, native German setters, historical pools and owning generators use narrow adapters in integration.py. The three existing West German candidate variables retain their first candidate indices. Modern Sheep menus are excluded from the 1970 scenario. Canonical GER, DDR and historical-pool writers retain the adapters on regeneration.
Eastern portraits replace existing bound DDS textures. In particular Brezhnev uses the existing SOV_Coldwar_Brezhnev.dds binding and existing Soviet leadership entry. This pass adds no second Brezhnev. The earlier USA/Soviet selection module remains at 41 USA and 52 Soviet candidates; its portrait icons were regenerated after these texture updates.

## Period sources and identity checks

Archival metadata and full captions take precedence over filenames and present-day Wikipedia thumbnails. Later opposition figures use period photographs from the 1980s or 1990s. Modern elderly photographs of Engholm, Rau, Lafontaine, Scharping and Schröder were replaced before installation. A filename containing 1992 proved to be a 2015 Stoiber photograph and was replaced by a 1981 Bundesarchiv source.
The Frey source is the politician, not the mathematician. Deckert is the politician, not the ski jumper. The Passau 1998 caption identifies Voigt as the second person from the left; the third is Distler. Wolf Biermann, the dissident songwriter, is distinct from Wolfgang Biermann, the Carl Zeiss industrial director. Aliyev uses a TASS photograph from 22 December 1972, replacing a later independence-era portrait.
Some original dates remain unknown: the reused Rasulov and Gapurov portraits and the historical Kochinyan image reproduced on a 2013 stamp. Kochinyan died in 1989; 2013 is the stamp issue, not a claim about the photographic sitting. Stehr's photograph with Castro is from the 1990s, with 1994 and 1996 recollections recorded as uncertain. No exact year is invented for these sources.
Source authors, reported licences, unknown permissions, modifications, input hashes and installed asset paths are recorded in [ASSET_NOTICE.md](ASSET_NOTICE.md), [ASSET_MANIFEST.json](ASSET_MANIFEST.json), sources.json and generated/*.json. Project identification does not establish third-party ownership.

## Historical references

- [Federal Chancellery: chancellors since 1949](https://www.bundeskanzler.de/bk-de/kanzleramt/bundeskanzler-seit-1949): Brandt, Schmidt, Kohl and Schröder, alongside the native Union/SPD alternatives.
- [Haus der Geschichte: 1990 chronology](https://www.hdg.de/lemo/jahreschronik/1990.html) and [Gysi biography](https://www.hdg.de/lemo/biografie/gregor-gysi.html): SED-PDS, opposition and democratic transition.
- [Federal government: de Maizière elected minister-president](https://www.bundesregierung.de/breg-de/schwerpunkte/deutsche-einheit/lothar-de-maizi%C3%A8re-wird-ministerpraesident-353994): the eastern CDU alternative.
- [Volkskammer primary proceedings](https://webarchiv.bundestag.de/volkskammer/dokumente/protokolle/1026.pdf): contemporary institutional and political identities.
- [ZEISS corporate history](https://www.zeiss.de/content/dam/Corporate/history/PDFs/schluesselereignisse_1989-2011.pdf): Wolfgang Biermann as industrial director, distinct from the songwriter.
- [Historical Lexicon of Bavaria: DKP](https://www.historisches-lexikon-bayerns.de/Lexikon/Deutsche_Kommunistische_Partei_%28DKP%29): Bachmann, Mies and Stehr.

## Verification

Current German bounded model: 1039 cases passed. It checks valid and invalid execution, repeat clicks, 1970/1999/2005 selections, party return, incumbent name aliases, retained West German indices, DDR profile cleanup, saved death flags, syntax, encoding, asset dimensions, adapter idempotence and full-build byte idempotence.
The USA/Soviet regression suite passed 1,024 model cases after icon regeneration. Its earlier restoration-method counts describe the original pass; the four Soviet portrait replacements in this pass have their updated provenance here.
These are source and bounded-model checks. The model stubs native MD politics, traits and dynamic-modifier refresh. HOI4 startup, native UI rendering, save/reload and live multiplayer were not tested by this pass. The contact sheets are composed from installed DDS textures and are not game screenshots.

Commands:

```text
python -X utf8 tools/europe_1970_leaders/catalogue.py
python -X utf8 tools/europe_1970_leaders/build.py
python -X utf8 tools/europe_1970_leaders/validate.py
python -X utf8 tools/superpower_1970_leaders/build.py
python -X utf8 tools/superpower_1970_leaders/validate.py
python -X utf8 tools/europe_1970_leaders/document.py
```

## German coverage

| Country | Figure | Native party slot(s) |
| --- | --- | --- |
| GER | Willy Brandt | 3 |
| GER | Helmut Schmidt | 3 |
| GER | Hans-Jochen Vogel | 3 |
| GER | Johannes Rau | 3 |
| GER | Oskar Lafontaine | 3 |
| GER | Björn Engholm | 3 |
| GER | Rudolf Scharping | 3 |
| GER | Gerhard Schröder | 3 |
| GER | Rainer Barzel | 1 |
| GER | Helmut Kohl | 1 |
| GER | Franz Josef Strauß | 1 |
| GER | Ernst Albrecht | 1 |
| GER | Lothar Späth | 1 |
| GER | Wolfgang Schäuble | 1 |
| GER | Kurt Georg Kiesinger | 1 |
| GER | Edmund Stoiber | 1 |
| GER | Theo Waigel | 1 |
| GER | Angela Merkel | 1 |
| GER | Karl Carstens | 1 |
| GER | Richard von Weizsäcker | 1 |
| GER | Roman Herzog | 1 |
| GER | Gustav Heinemann | 3 |
| GER | Walter Scheel | 2 |
| GER | Hans-Dietrich Genscher | 2 |
| GER | Otto Graf Lambsdorff | 2 |
| GER | Wolfgang Mischnick | 2 |
| GER | Martin Bangemann | 2 |
| GER | Klaus Kinkel | 2 |
| GER | Petra Kelly | 17 |
| GER | Joschka Fischer | 17 |
| GER | Jutta Ditfurth | 17 |
| GER | Antje Vollmer | 17 |
| GER | Kurt Bachmann | 4 |
| GER | Herbert Mies | 4 |
| GER | Heinz Stehr | 4 |
| GER | Gregor Gysi | 5 |
| GER | Lothar Bisky | 5 |
| GER | Franz Schönhuber | 20 |
| GER | Rolf Schlierer | 20 |
| GER | Adolf von Thadden | 21 |
| GER | Martin Mußgnug | 21 |
| GER | Günter Deckert | 21 |
| GER | Udo Voigt | 21 |
| GER | Gerhard Frey | 22 |
| DDR | Walter Ulbricht | 4 |
| DDR | Erich Honecker | 4 |
| DDR | Willi Stoph | 4 |
| DDR | Günter Mittag | 4 |
| DDR | Kurt Hager | 4 |
| DDR | Heinz Hoffmann | 4, 22 |
| DDR | Werner Lamberz | 4 |
| DDR | Werner Krolikowski | 4 |
| DDR | Egon Krenz | 4 |
| DDR | Hans Modrow | 4, 5 |
| DDR | Heinz Keßler | 4, 22 |
| DDR | Günter Schabowski | 4 |
| DDR | Horst Sindermann | 4 |
| DDR | Robert Havemann | 5 |
| DDR | Wolf Biermann | 5 |
| DDR | Gregor Gysi | 4, 5 |
| DDR | Lothar Bisky | 5 |
| DDR | Alfred Neumann | 6 |
| DDR | Erich Mielke | 7 |
| DDR | Alexander Schalck-Golodkowski | 0 |
| DDR | Gerald Götting | 1 |
| DDR | Lothar de Maizière | 1 |
| DDR | Rainer Eppelmann | 1, 14 |
| DDR | Angela Merkel | 1 |
| DDR | Sabine Bergmann-Pohl | 1 |
| DDR | Manfred Gerlach | 2 |
| DDR | Rainer Ortleb | 2 |
| DDR | Friedrich Ebert Jr. | 3 |
| DDR | Markus Meckel | 3 |
| DDR | Ibrahim Böhme | 3 |
| DDR | Stephan Hilsberg | 3 |
| DDR | Manfred Stolpe | 3 |
| DDR | Gerhard Schürer | 13 |
| DDR | Albrecht Schönherr | 14 |
| DDR | Joachim Gauck | 14 |
| DDR | Wolfgang Ullmann | 14 |
| DDR | Wolfgang Biermann | 15 |
| DDR | Reimar Gilsenbach | 17 |
| DDR | Bärbel Bohley | 17 |
| DDR | Jens Reich | 17 |
| DDR | Ernst Goldenbaum | 18 |
| DDR | Günther Maleuda | 18 |
| DDR | Wolfgang Harich | 19 |
| DDR | Lothar Bolz | 20 |
| DDR | Heinrich Homann | 20 |
| DDR | Louis Ferdinand, Prince of Prussia | 23 |

## Installed portrait reviews

![West Germany](GER_PORTRAIT_REVIEW.png)

![East Germany](DDR_PORTRAIT_REVIEW.png)

![SSR, Eastern Bloc and Soviet portraits](EAST_PORTRAIT_REVIEW.png)
