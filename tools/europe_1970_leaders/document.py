# IMPERIA COLD WAR — German leadership coverage and period portrait documentation.
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]

def main():
    roster=json.loads((HERE/'runtime_roster.json').read_text(encoding='utf8'))['people']
    assets=json.loads((HERE/'ASSET_MANIFEST.json').read_text(encoding='utf8'))['assets']
    report=json.loads((HERE/'VALIDATION.json').read_text(encoding='utf8'))
    preserved=sum(a['source'].get('status')=='approved_original' for a in assets)
    restored=sum('rejected' not in a['modifications'] and a['source'].get('status')!='approved_original' for a in assets)
    lines=['IMPERIA COLD WAR: German leadership and Eastern portraits','',
        'Implemented in the working mod. West Germany has 44 country-person entries and East Germany has 46. Gysi, Bisky and Merkel share one portrait each across both countries: 87 distinct people and 95 party-specific choices.',
        f'The portrait pass installs {len(assets)} distinct people: 87 German figures and 25 existing SSR/Eastern Bloc/Soviet figures. {restored} use AI restoration; {preserved} retain their previously approved original DDS textures unchanged. Three use their identified original period photographs after the image service rejected restoration: Björn Engholm, Günther Maleuda and Johannes Käbin.','',
        'Willy Brandt, Walter Ulbricht and Leonid Brezhnev use the exact original textures from commit 34fb12b2bfab7f33b4a4ba066baeaa770a123998. Their native bindings and save-compatible portrait aliases are restored byte-for-byte. approved_portraits.json pins the source hashes, and regeneration verifies and copies these approved inputs without image processing. Their small selector icons are derived from those original portraits.','',
        '## Player behaviour','',
        '- Free, repeatable native leadership selections appear for the actual governing party in the 1970 scenario. Historical terms, age and calendar death flags do not lock human selections.',
        '- Selections are remembered per party. Existing West German CDU/CSU, FDP and SPD indices keep their native focus/event meanings. The late authoritarian National Directorate retains its existing route.',
        '- East German personal SED profile flags follow the actual incumbent in the actual SED slot. Leaving that slot clears the personal profile; selecting a profile again restores it. Hoffmann and Keßler remain distinct. Earned focus-dependent leader traits are reapplied when the selected profile is recreated.',
        '- Existing AI appointments and calendar succession, other bookmarks, party identities and hypothetical routes are retained. No new religious party slots, collective substitute people or military recruitment are added.',
        '- The HOI4 portrait represents the selected political figure. Choosing Heinemann, Carstens, Weizsäcker, Herzog or Bergmann-Pohl does not implement a separate constitutional presidential office or historical term.',
        '- Reconciliation uses startup and two country-specific monthly hooks, for GER and DDR. No new daily or weekly pulse and no recurring world-country scan are introduced.',
        '- All new localisation is English. IDs and runtime files use the COLDWAR prefix.','',
        '## Integration and duplicate prevention','',
        'The central MD dispatcher, native German setters, historical pools and owning generators use narrow adapters in integration.py. The three existing West German candidate variables retain their first candidate indices. Modern Sheep menus are excluded from the 1970 scenario. Canonical GER, DDR and historical-pool writers retain the adapters on regeneration.',
        'Eastern portraits replace existing bound DDS textures. In particular Brezhnev uses the existing SOV_Coldwar_Brezhnev.dds binding and existing Soviet leadership entry. This pass adds no second Brezhnev. The earlier USA/Soviet selection module remains at 41 USA and 52 Soviet candidates; its portrait icons were regenerated after these texture updates.','',
        '## Period sources and identity checks','',
        'Archival metadata and full captions take precedence over filenames and present-day Wikipedia thumbnails. Later opposition figures use period photographs from the 1980s or 1990s. Modern elderly photographs of Engholm, Rau, Lafontaine, Scharping and Schröder were replaced before installation. A filename containing 1992 proved to be a 2015 Stoiber photograph and was replaced by a 1981 Bundesarchiv source.',
        'The Frey source is the politician, not the mathematician. Deckert is the politician, not the ski jumper. The Passau 1998 caption identifies Voigt as the second person from the left; the third is Distler. Wolf Biermann, the dissident songwriter, is distinct from Wolfgang Biermann, the Carl Zeiss industrial director. Aliyev uses a TASS photograph from 22 December 1972, replacing a later independence-era portrait.',
        'Some original dates remain unknown: the reused Rasulov and Gapurov portraits and the historical Kochinyan image reproduced on a 2013 stamp. Kochinyan died in 1989; 2013 is the stamp issue, not a claim about the photographic sitting. Stehr\'s photograph with Castro is from the 1990s, with 1994 and 1996 recollections recorded as uncertain. No exact year is invented for these sources.',
        'Source authors, reported licences, unknown permissions, modifications, input hashes and installed asset paths are recorded in [ASSET_NOTICE.md](ASSET_NOTICE.md), [ASSET_MANIFEST.json](ASSET_MANIFEST.json), sources.json and generated/*.json. Project identification does not establish third-party ownership.','',
        '## Historical references','',
        '- [Federal Chancellery: chancellors since 1949](https://www.bundeskanzler.de/bk-de/kanzleramt/bundeskanzler-seit-1949): Brandt, Schmidt, Kohl and Schröder, alongside the native Union/SPD alternatives.',
        '- [Haus der Geschichte: 1990 chronology](https://www.hdg.de/lemo/jahreschronik/1990.html) and [Gysi biography](https://www.hdg.de/lemo/biografie/gregor-gysi.html): SED-PDS, opposition and democratic transition.',
        '- [Federal government: de Maizière elected minister-president](https://www.bundesregierung.de/breg-de/schwerpunkte/deutsche-einheit/lothar-de-maizi%C3%A8re-wird-ministerpraesident-353994): the eastern CDU alternative.',
        '- [Volkskammer primary proceedings](https://webarchiv.bundestag.de/volkskammer/dokumente/protokolle/1026.pdf): contemporary institutional and political identities.',
        '- [ZEISS corporate history](https://www.zeiss.de/content/dam/Corporate/history/PDFs/schluesselereignisse_1989-2011.pdf): Wolfgang Biermann as industrial director, distinct from the songwriter.',
        '- [Historical Lexicon of Bavaria: DKP](https://www.historisches-lexikon-bayerns.de/Lexikon/Deutsche_Kommunistische_Partei_%28DKP%29): Bachmann, Mies and Stehr.','',
        '## Verification','',
        f'Current German bounded model: {report["bounded_model_cases"]} cases passed. It checks valid and invalid execution, repeat clicks, 1970/1999/2005 selections, party return, incumbent name aliases, retained West German indices, DDR profile cleanup, saved death flags, syntax, encoding, asset dimensions, adapter idempotence and full-build byte idempotence.',
        'The USA/Soviet regression suite passed 1,024 model cases after icon regeneration. Its earlier restoration-method counts describe the original pass; the four Soviet portrait replacements in this pass have their updated provenance here.',
        'These are source and bounded-model checks. The model stubs native MD politics, traits and dynamic-modifier refresh. HOI4 startup, native UI rendering, save/reload and live multiplayer were not tested by this pass. The contact sheets are composed from installed DDS textures and are not game screenshots.','',
        'Commands:','',
        '```text','python -X utf8 tools/europe_1970_leaders/catalogue.py','python -X utf8 tools/europe_1970_leaders/build.py','python -X utf8 tools/europe_1970_leaders/validate.py','python -X utf8 tools/superpower_1970_leaders/build.py','python -X utf8 tools/superpower_1970_leaders/validate.py','python -X utf8 tools/europe_1970_leaders/document.py','```','',
        '## German coverage','', '| Country | Figure | Native party slot(s) |','| --- | --- | --- |']
    lines.extend('| '+p['tag']+' | '+p['name']+' | '+', '.join(map(str,p['slots']))+' |' for p in roster)
    lines+=['','## Installed portrait reviews','','![West Germany](GER_PORTRAIT_REVIEW.png)','','![East Germany](DDR_PORTRAIT_REVIEW.png)','','![SSR, Eastern Bloc and Soviet portraits](EAST_PORTRAIT_REVIEW.png)','']
    (HERE/'README.md').write_text('\n'.join(lines),encoding='utf8')
    p=ROOT/'IMPERIA_COLD_WAR_NOTICE.md';text=p.read_text(encoding='utf8')
    entry='<!-- IMPERIA COLD WAR — German leadership and Eastern period portraits. -->'
    if entry not in text:
        text+='\n'+entry+'\n- German candidate selections and 112 period portrait assets: [module and verification](tools/europe_1970_leaders/README.md), [individual photo credits, licences and unknown permissions](tools/europe_1970_leaders/ASSET_NOTICE.md), and [exact installed asset hashes](tools/europe_1970_leaders/ASSET_MANIFEST.json). Existing Eastern leader bindings, including Brezhnev, are reused. AI restoration does not establish ownership of original photographs.\n'
        p.write_text(text,encoding='utf8')
    print('Documentation written for',len(roster),'country-person records and',len(assets),'portrait assets')

if __name__=='__main__':main()
