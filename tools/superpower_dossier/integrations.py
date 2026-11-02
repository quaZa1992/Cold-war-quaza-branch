# IMPERIA COLD WAR — Passive source integrations without alternate transactions
import re

MARK = '# IMPERIA COLD WAR — Superpower dossier correspondence observer integration\n'
BEGIN = '# IMPERIA COLD WAR — Dossier observer BEGIN'
END = '# IMPERIA COLD WAR — Dossier observer END'


def closing(source, start):
    depth, quoted, comment, escaped = 1, False, False, False
    for i in range(start,len(source)):
        c=source[i]
        if comment:
            if c=='\n':comment=False
            continue
        if c=='#' and not quoted:comment=True;continue
        if c=='"' and not escaped:quoted=not quoted
        if not quoted:
            depth+=(c=='{')-(c=='}')
            if not depth:return i
        escaped=(c=='\\' and not escaped)
    raise ValueError('Unclosed provider block')


def strip(source):
    source=source.removeprefix(MARK)
    source=re.sub(r'\n\t\t\t# IMPERIA COLD WAR — Read-only correspondence receipt\n\t\t\ticsd_note_(?:trade|money)_(?:sent|accepted|declined) = yes','',source)
    return re.sub(r'\n[ \t]*'+re.escape(BEGIN)+r'\n.*?'+re.escape(END)+r'\n','',source,flags=re.S)


def patch(root):
    rel='common/scripted_effects/00_influence_scripted_effects.txt'
    p=root/rel;before=p.read_text(encoding='utf-8-sig');source=before
    for effect,callback in (('manipulate_politics_action','icsd_note_politics'),('mp_economic_aid_transfer','icsd_note_economic_aid')):
        m=re.search(r'^'+effect+r'\s*=\s*\{',source,re.M);assert m,effect
        end=closing(source,m.end())
        if callback+' = yes' not in source[m.end():end]:
            source=source[:end]+f'\n\t{BEGIN}\n\t{callback} = yes\n\t{END}\n'+source[end:]
    if not source.startswith(MARK):source=MARK+source
    assert strip(source)==strip(before), 'Observer patch altered influence gameplay'
    assert p.read_text(encoding='utf-8-sig')==before,'Concurrent provider edit'
    if source != before:
        p.write_text(source,encoding='utf-8',newline='\n')
    rel2='events/Influence.txt';p=root/rel2;before=p.read_text(encoding='utf-8-sig');source=before
    if 'icsd_note_gdp_aid = yes' not in source:
        start=source.index('name = News_influence.0.a')
        credit='add_to_variable = { treasury = temp_amount_gift_sum }'
        at=source.index(credit,start)+len(credit)
        assert at<source.index('name = News_influence.0.b'), 'GDP aid acceptance path changed'
        source=source[:at]+f'\n\t\t{BEGIN}\n\t\ticsd_note_gdp_aid = yes\n\t\t{END}\n'+source[at:]
    if not source.startswith(MARK):source=MARK+source
    assert strip(source)==strip(before),'Observer patch altered GDP aid gameplay'
    assert p.read_text(encoding='utf-8-sig')==before,'Concurrent provider edit'
    if source != before:
        p.write_text(source,encoding='utf-8',newline='\n')
    return [rel,rel2]
