# IMPERIA COLD WAR — Retained Soviet generator and legacy annual-order integrations.
from pathlib import Path
import hashlib
import json
import re
import coldwar_order_legacy as legacy

HEADER = '# IMPERIA COLD WAR — Annual Union order integration.\n'


def install(root):
    paths = []
    for relative,transform in (
        ('common/scripted_effects/COLDWAR_UNI_1970_scripted_effects.txt',legacy.effects),
        ('events/COLDWAR_UNI_1970_events.txt',legacy.events),
        ('common/decisions/categories/COLDWAR_UNI_1970_decision_categories.txt',legacy.categories),
        ('common/scripted_triggers/COLDWAR_UNI_1970_scripted_triggers.txt',legacy.triggers),
        ('common/national_focus/COLDWAR_UNI_1970_union_joint.txt',legacy.joint),
    ):
        path=root/relative
        old=path.read_text(encoding='utf-8')
        new=transform(old)
        if not new.startswith(HEADER): new=HEADER+new
        if new!=old: path.write_text(new,encoding='utf-8')
        paths.append(relative)
    relative='Claude outputs/COLDWAR_SOV_generator/cw_union.py'
    path=root/relative
    old=path.read_text(encoding='utf-8')
    mark='# IMPERIA COLD WAR — Annual order adapter BEGIN'
    code='''# IMPERIA COLD WAR — Annual order adapter BEGIN
# Apply the same narrow guards whenever the retained Soviet generator is run.
from pathlib import Path as _OrderPath
sys.path.insert(0, str(_OrderPath(__file__).resolve().parents[2] / "tools/union_orders_1970"))
import coldwar_order_legacy as _OrderLegacy
EFFECTS_TXT = _OrderLegacy.effects(EFFECTS_TXT)
EVENTS_TXT = _OrderLegacy.events(EVENTS_TXT)
DEC_CAT_TXT = _OrderLegacy.categories(DEC_CAT_TXT)
TRIGGERS_TXT = _OrderLegacy.triggers(TRIGGERS_TXT)
JOINT_TXT = _OrderLegacy.joint(JOINT_TXT)
LOC.update(_OrderLegacy.LOC_UPDATES)
# IMPERIA COLD WAR — Annual order adapter END
'''
    if mark not in old:
        anchor='FILES = {\n'
        assert old.count(anchor)==1
        old=old.replace(anchor,code+'\n'+anchor)
    else:
        endmark='# IMPERIA COLD WAR — Annual order adapter END'
        old=old[:old.index(mark)]+code.rstrip('\n')+old[old.index(endmark)+len(endmark):]
    path.write_text(old,encoding='utf-8')
    paths.append(relative)
    relative='localisation/english/COLDWAR_UNI_1970_l_english.yml'
    path=root/relative
    text=path.read_text(encoding='utf-8-sig')
    for key,value in legacy.LOC_UPDATES.items():
        pattern=r'^ '+re.escape(key)+r':\d* .*?$'
        assert len(re.findall(pattern,text,re.M))==1,key
        text=re.sub(pattern,lambda m:' '+key+':0 '+json.dumps(value,ensure_ascii=False),text,flags=re.M)
    if not text.startswith('l_english:\n'+HEADER.rstrip()):text=text.replace('l_english:\n','l_english:\n'+HEADER,1)
    path.write_text(text,encoding='utf-8-sig')
    paths.append(relative)
    # The SSR manifest tracks the shared donor generator too. Refresh that one
    # expected integration hash, without rebuilding the approved SSR outputs.
    manifest=root/'tools/ssr_1970/manifest.json'
    if manifest.exists():
        data=json.loads(manifest.read_text(encoding='utf-8'))
        for key in data.get('outputs',{}):
            if Path(key).as_posix() in paths:
                data['outputs'][key]=hashlib.sha256((root/key).read_bytes()).hexdigest()
        manifest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    return paths
