# IMPERIA COLD WAR — Stable project identification for owned Cuba files and integrations.
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
MARK='IMPERIA COLD WAR'
SHARED={
    'history/countries/CUB - Cuba.txt':'Custom Cuba 1970 scenario integration; upstream Millennium Dawn history retained.',
    'common/scripted_effects/CUB_political_leaders.txt':'Custom Cuba 1970 leader integration; upstream Millennium Dawn content retained.',
    'common/scripted_effects/mdcw_1970_focus_tree_effects.txt':'Cold War 1970 focus-tree routing, including the custom Cuba integration.',
    'common/scripted_effects/mdcw_diaspora_migration_effects.txt':'Cold War diaspora integration, including the custom Cuba return observer.',
}


def project_comment(line,prefix='#'):
    if MARK in line:
        detail=line.split(MARK,1)[1].lstrip(' \u2014:')
    elif 'IMPERIA CW' in line:
        detail=line.split('IMPERIA CW',1)[1].lstrip(' \u2014:')
        detail=detail.removeprefix('Cold War:').strip()
    else:
        return None
    return prefix+' '+MARK+' \u2014 '+detail


def stamp(text,feature,localisation=False,prefix='#'):
    lines=text.splitlines()
    if localisation:
        assert lines and lines[0]=='l_english:','Keep the required language header first'
        index=1
    else:
        index=1 if lines and lines[0].startswith('#!') else 0
    marker=prefix+' '+MARK+' \u2014 '+feature
    if len(lines)>index and (updated:=project_comment(lines[index],prefix)):
        lines[index]=updated
    else:
        lines.insert(index,marker)
    return '\n'.join(lines)+'\n'


def main():
    manifest=json.loads((ROOT/'tools/cuba_1970/integration_manifest.json').read_text())
    paths={e['path'] for e in manifest['owned']}|set(SHARED)
    changed=[]
    for rel in sorted(paths):
        p=ROOT/rel;old=p.read_text(encoding='utf-8-sig')
        feature=SHARED.get(rel,'Cuba 1970: '+p.stem.removeprefix('COLDWAR_CUB_1970').strip('_')+'.')
        new=stamp(old,feature,p.suffix=='.yml')
        if new!=old or (p.suffix!='.yml' and p.read_bytes().startswith(b'\xef\xbb\xbf')):
            p.write_text(new,encoding='utf-8-sig' if p.suffix=='.yml' else 'utf-8',newline='\n');changed.append(rel)
    print(json.dumps({'project':MARK,'headers_updated':len(changed)}))


if __name__=='__main__':main()
