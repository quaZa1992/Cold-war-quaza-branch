# IMPERIA COLD WAR — Political leadership provenance and delivery documentation.
from pathlib import Path
from html import unescape
import json
import re

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]


def clean(value):return re.sub(r'<[^>]+>','',unescape(str(value or 'unknown'))).replace('|','/').replace('\n',' ')


def main():
    roster=json.loads((HERE/'runtime_roster.json').read_text(encoding='utf-8'))['people']
    records=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((HERE/'generated').glob('*.json')) if not p.stem.endswith('_error')]
    # Records contain their own project key; retain the original exact generation prompts.
    (HERE/'generation.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',portraits=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    notice=['IMPERIA COLD WAR: USA and Soviet political portrait provenance','',
        'These are game assets. AI restorations are interpretations of identified photographs, not untouched archival photographs.',
        'Requested restoration instruction: "Kolorisiere das Bild und mache es qualitativ wie ein Handyfoto."',
        'Each generated master and its full identity-preservation prompt is recorded in generation.json. Original source photographs remain in references/.',
        'Technical modifications: portrait crop, resize to 156 x 210 DDS, and native Sheep-style 33 x 30 decision icon crop. Existing portraits retain their original large texture.',
        'Original authors and licence information below are retained when known. Unknown means unverified. Project markers establish neither ownership nor permission.',
        'See the repository IMPERIA_COLD_WAR_NOTICE.md. Commons metadata, file pages, and source-specific credits are retained in sources.json and runtime_roster.json.',
        '', '| Person | Runtime portrait | Treatment | Source and credit | Licence or permission |', '|---|---|---|---|---|']
    for r in roster:
        s=r['source'];url=s.get('actual_download_url') or s.get('source_page') or s.get('source_url') or s.get('portrait')
        author=s.get('source_author') or s.get('provenance',{}).get('source_author') or 'Original MD contributors; individual artist unknown'
        licence=s.get('licence') or s.get('provenance',{}).get('licence') or 'unknown'
        notice.append('| '+r['name']+' | `'+r['portrait']+'` | '+r['method']+' | '+clean(url)+'; '+clean(author)+' | '+clean(licence)+' |')
    (HERE/'ASSET_NOTICE.md').write_text('\n'.join(notice)+'\n',encoding='utf-8')
    for folder in ('gfx/leaders/COLDWAR_superpower_1970','gfx/interface/decisions/COLDWAR_superpower_1970'):
        (ROOT/folder/'ASSET_NOTICE.md').write_text('IMPERIA COLD WAR: USA and Soviet political portrait assets\n\nFull source, author, licence, modification and generation records: tools/superpower_1970_leaders/ASSET_NOTICE.md, sources.json and generation.json. Unknown rights remain unknown.\n',encoding='utf-8')
    readme='''IMPERIA COLD WAR: USA and Soviet political candidate selections

The 1970 campaign has 41 US and 53 Soviet or later Russian political representatives, covering every individually named representative created by the existing 1970 USA and Soviet tree providers. Collective governments retain their existing institutional representation. No new religious party paths are added.

The roster covers presidents, general secretaries, the Soviet tree's existing stand-ins, major US primary challengers, communist and libertarian alternatives, democratic Soviet opposition, and Russian political rivals through the end of 1999. Putin's 1999 state-administrative alternative is a political representative, separate from the existing 1975 KGB operative feature. Some path governments, including exile and restoration options, are explicitly hypothetical. Choosing a representative does not enact that government's wider programme.

Human players use native, repeatable, zero-cost Sheep-style party candidate decisions with individual portrait icons. Their current native ruling-party trigger gates both availability and execution. A representative's selection is remembered separately within each affiliation. All earlier choices retain their policy without term, age, retirement-date or death-date windows. At the user's explicit request, Alexander Lukashenko is the sole date exception: visible but disabled before 1990, with a young default portrait and a separate 1990s appearance option. See tools/lukashenko_1970/README.md. The AI's authored historical selection and calendar remain available through the original providers. Other bookmarks use their original menus.

The dispatcher restores each party's remembered candidate when it takes power. A real legacy focus, election or Politburo appointment records its explicit candidate before the party-change dispatcher runs. Selecting a politician calls no focus reward, construction transaction or investment setup. Existing USA programme reconciliation remains with its owner. Soviet general-secretary flags and dynamic-modifier refresh follow the actual chosen person; non-CPSU governments and CPSU candidates without a personal path clear the former personal programme flags.

Human Soviet calendar-death triggers and already open calendar-death options cannot force a selected leader out of office. Existing political events and deliberate Politburo appointments remain meaningful. The existing retirement control cycles the applicable candidate pool. New recurring observation uses only on_monthly_USA and on_monthly_SOV, plus two fixed country scopes on startup. There is no new daily or weekly scan and no world-country scan.

The existing native 2000 candidate decisions are guarded at execution as well as visibility in a 1970 campaign. The original source bodies are retained for their bookmark. Narrow adapters are installed in the Soviet generator's writer, the USA expansion writer and the historical politics writer. The approved focus design inputs and all tree positions are retained. The Greek replacement-tree concept is outside this change.

Research and identity records are in catalogue.py, catalogue.json and sources.json. All 33 individually named Soviet 1970 representatives and all ten existing US 1970 presidential appointments were cross-checked against the actual loaded focus/effect providers. Later candidates represent documented political currents, not claims that they held office in January 1970.

Historical reference points:

- [FEC official 1996 election records](https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/federal-elections-1996/): Clinton, Dole, Perot, Browne, Nader and the distinction between a general-election nominee and primary alternatives.
- [Dole Institute presidential and Bush collection](https://dolearchives.ku.edu/research/topic/president-ghw-bush): Republican leadership and succession alternatives.
- [Reagan Library remarks about Jack Kemp](https://www.reaganlibrary.gov/archives/speech/remarks-dinner-honoring-representative-jack-f-kemp-new-york): Kemp's contemporary political position.
- [Senator Sanders's official biography](https://www.sanders.senate.gov/about-bernie/): Burlington and the 1990 House election, distinct from his later presidential campaigns.
- [AIP Sakharov exhibit](https://history.aip.org/exhibits/sakharov/perestroika.html): Sakharov's 1989 parliamentary and democratic-opposition role.
- [Sakharov Foundation on the 1989 Congress](https://sakharovfoundation.org/news/anniversary-a-watershed-moment-soviet-history/): Sakharov, Sobchak and the reform opposition.
- [Contemporary US presidential statement, 31 December 1999](https://www.presidency.ucsb.edu/documents/statement-the-resignation-president-boris-yeltsin-russia): the Yeltsin-to-Putin transfer at the end of the covered period.
- [Novocherkassk Tragedy Foundation photograph reproduced by Meduza](https://meduza.io/en/feature/2017/11/23/the-novocherkassk-massacre): the identified photograph of Pyotr Petrovich Siuda. He is not the modern Polish sociologist Piotr Siuda.

58 source-photo restorations use the requested prompt. Seven rejected restorations retain their identified original photographs: Edmund Muskie, Alexander Shelepin, Dzhermen Gvishiani, Barry Goldwater, David Bergland, Ed Clark and Henry M. Jackson. 29 runtime portraits reuse existing bound textures. Lukashenko's restored user-supplied image is produced by tools/lukashenko_1970; the other 28 are the original reused set. The rejection records are retained; no substitute faces were invented.

Build: `python tools/superpower_1970_leaders/catalogue.py`, then `python tools/superpower_1970_leaders/build.py`.
Validate: `python tools/superpower_1970_leaders/validate.py`.
Document assets: `python tools/superpower_1970_leaders/document.py`.

VALIDATION.json records current hashes, parser/encoding/reference checks, bounded model cases and regeneration idempotence. The model stubs native MD politics, traits and existing programme reconciliation. It is not an engine or live multiplayer test. Native UI rendering, calendar/save/reload and a multiplayer rehearsal still require the game.
'''
    lukashenko_year=json.loads((HERE.parent/'lukashenko_1970/config.json').read_text(encoding='utf8'))['available_from'].split('.')[0]
    readme=readme.replace('visible but disabled before 1990','visible but disabled before '+lukashenko_year)
    (HERE/'README.md').write_text(readme,encoding='utf-8')


if __name__=='__main__':main()
