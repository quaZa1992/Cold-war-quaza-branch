# IMPERIA CW — Cold War: uae 1970 — event catalogue.
"""Read-only extraction of every installed UAE/GCC event for review.

Writes only audit artefacts and a conversation preview, never loaded mod files.
The preview displays real localisation and source; it is not an engine render.
"""
from pathlib import Path
import base64
import collections
import gzip
import hashlib
import io
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values

EVENT_FILES = ['events/COLDWAR_UAE_1970_contracts.txt', 'events/COLDWAR_GCC_1970.txt']
VIS = Path('C:/Users/Enes/.codex/visualizations/2026/10/19/01a153f9-9c59-71b2-8460-d28a5d918d07')


def pretty(rows, level=0):
    lines = []
    for k, op, v in rows:
        if isinstance(v, list):
            lines.append('  '*level + f'{k} {op} {{')
            lines.extend(pretty(v, level+1).splitlines())
            lines.append('  '*level + '}')
        else:
            lines.append('  '*level + f'{k} {op} {v}')
    return '\n'.join(lines)


def main():
    loc = {}
    loc_paths = list((ROOT/'localisation/english').glob('COLDWAR_UAE_1970*.yml')) + [ROOT/'localisation/english/COLDWAR_GCC_1970_l_english.yml']
    for path in loc_paths:
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            match = re.fullmatch(r'\s*(\S+):\d*\s+"((?:[^"\\]|\\.)*)"\s*', line)
            if match:
                loc[match[1]] = match[2].replace('\\n','\n').replace('\\"','"').replace('\\\\','\\')
    resolve = lambda key: loc.get(str(key), str(key))
    events, groups = [], collections.OrderedDict()
    for relative in EVENT_FILES:
        text = (ROOT/relative).read_text(encoding='utf-8-sig')
        lines = {m[1]: text.count('\n',0,m.start())+1 for m in re.finditer(r'(?m)^\s*id\s*=\s*(\S+)\s*$',text)}
        for kind, op, body in parse(text):
            if kind not in {'country_event','news_event'}:
                continue
            eid = first(body,'id')
            title, desc = resolve(first(body,'title')), resolve(first(body,'desc'))
            opts = []
            for opt in values(body,'option'):
                actions = [r for r in opt if r[0] not in {'name','trigger','ai_chance'}]
                opts.append({'name':resolve(first(opt,'name')), 'condition':pretty(first(opt,'trigger') or []),
                             'effects':actions, 'source':pretty(actions)})
            event = {'id':eid, 'title':title, 'description':desc, 'picture':first(body,'picture'),
                     'file':relative, 'line':lines[eid], 'options':opts,
                     'immediate':pretty(first(body,'immediate') or []), 'source':pretty([(kind,op,body)])}
            idx = len(events)
            events.append(event)
            group_key = (relative,title,desc,tuple(o['name'] for o in opts))
            groups.setdefault(group_key,[]).append(idx)
    grouped = [{'title':key[1], 'file':key[0], 'events':ids} for key,ids in groups.items()]
    image_data = {}
    from PIL import Image
    gfx_text = '\n'.join((ROOT/p).read_text(encoding='utf-8-sig') for p in
                         ['interface/MD_eventpictures.gfx','interface/COLDWAR_UAE_1970_eventpictures.gfx'])
    for picture in {e['picture'] for e in events}:
        match = re.search(r'name\s*=\s*"'+re.escape(picture)+r'"\s+texturefile\s*=\s*"([^"]+)"',gfx_text,re.I)
        if not match:
            raise AssertionError('Picture unresolved: '+picture)
        img = Image.open(ROOT/match[1].replace('\\','/')).convert('RGB')
        stream = io.BytesIO()
        img.save(stream, format='JPEG', quality=85)
        image_data[picture] = 'data:image/jpeg;base64,'+base64.b64encode(stream.getvalue()).decode()
    payload = {'events':events,'groups':grouped,'images':image_data}
    report = {'event_ids':len(events),'preview_groups':len(grouped),
              'unique_titles':len({e['title'] for e in events}),
              'files':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in EVENT_FILES},
              'pictures':sorted(image_data), 'native_engine_render':False,
              'groups':[{'title':g['title'],'variants':len(g['events']), 'first_id':events[g['events'][0]]['id']} for g in grouped]}
    (HERE/'EVENT_CATALOGUE.json').write_text(json.dumps(report,indent=2)+'\n')
    # Repeated immutable event rounds compress well. Every exact event, source,
    # condition and option remains available; no selected rounds are omitted.
    packed = base64.b64encode(gzip.compress(json.dumps(payload,separators=(',',':')).encode(),mtime=0)).decode()
    template = (HERE/'event_catalogue_template.html').read_text(encoding='utf-8')
    fragment = template.replace('__EVENT_DATA_GZIP__',packed)
    output = VIS/'uae-gcc-events.html'
    output.write_text(fragment,encoding='utf-8')
    assert output.stat().st_size < 1_000_000, output.stat().st_size
    print(json.dumps({'events':len(events),'groups':len(grouped),'unique_titles':report['unique_titles'],
                      'bytes':output.stat().st_size,'path':str(output), 'pictures':report['pictures']}))


if __name__ == '__main__':
    main()
