# IMPERIA CW — Cold War: cyprus 1970 — integrate.
"""Small idempotent era-scoped edits to existing history and MD dispatchers."""
import re

def body_span(text,name):
    m=re.search(r'(?m)^'+re.escape(name)+r'\s*=\s*\{',text)
    assert m,name
    start=m.end();depth=1
    for token in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',text[start:]):
        if token[0]=='{':depth+=1
        elif token[0]=='}':
            depth-=1
            if depth==0:return start,start+token.start()
    raise ValueError('Unclosed '+name)

def integrate(c):
    root=c.ROOT;p=c.P
    changed=[]
    def update(rel,fn):
        path=root/rel;text=path.read_text(encoding='utf-8-sig');new=fn(text)
        if new!=text:path.write_text(new,encoding='utf-8')
        changed.append(rel)
    def history(text):
        early,sep,late=text.partition('2000.1.1 = {')
        early=early.replace('load_focus_tree = mdcw_1970_generic_focus','load_focus_tree = '+p+'focus')
        early=early.replace('expire = "1977.8.3"','expire = "2000.1.1"')
        early=re.sub(r'gfx/leaders/CYP/CYP_Coldwar_Makarios_III\.dds','gfx/leaders/CYP/1970/COLDWAR_CYP_1970_makarios.dds',early,flags=re.IGNORECASE)
        if p+'initialize = yes' not in early:
            early=re.sub(r'(create_country_leader = \{ name = "Makarios III"[^\n]+\}\n)',r'\1\t\t'+p+'initialize = yes\n',early,count=1)
        return early+sep+late
    update('history/countries/CYP - Cyprus.txt',history)
    def fallback(text):
        if p+'focus' in text:return text
        anchor='\t\t\t\t\toriginal_tag = EGY # COLDWAR | own 1970 tree'
        assert anchor in text
        return text.replace(anchor,anchor+'\n\t\t\t\t\tAND = { original_tag = CYP IMP_is_1970_scenario = yes } # '+p+'focus',1)
    update('common/scripted_effects/mdcw_1970_focus_tree_effects.txt',fallback)
    def leader(text):
        a,b=body_span(text,'set_leader')
        if p+'set_leader = yes' in text[a:b]:
            body=re.sub(r'(?m)^[\t ]+$','',text[a:b])
            if 'COLDWAR_NCY_1970_set_leader = yes' not in body:
                body=body.replace('\telse = {','\telse_if = {\n\t\tlimit = { original_tag = NCY IMP_is_1970_scenario = yes }\n\t\tCOLDWAR_NCY_1970_set_leader = yes\n\t}\n\telse = {',1)
            return text[:a]+body+text[b:]
        old=text[a:b].strip('\n')
        replacement='\n\t# IMPERIA CW — Cold War: cyprus 1970 generated content.\n\t# COLDWAR | Protect the current 1970 president before the modern dispatcher kills him.\n'
        replacement+='\tif = {\n\t\tlimit = { original_tag = CYP IMP_is_1970_scenario = yes }\n\t\t'+p+'set_leader = yes\n\t}\n'
        replacement+='\telse_if = {\n\t\tlimit = { original_tag = NCY IMP_is_1970_scenario = yes }\n\t\tCOLDWAR_NCY_1970_set_leader = yes\n\t}\n\telse = {\n'
        replacement+='\n'.join('\t'+line if line.strip() else '' for line in old.splitlines())+'\n\t}\n'
        return text[:a]+replacement+text[b:]
    update('common/scripted_effects/00_leader_setup_scripted_effects.txt',leader)
    def modern_tick(text):
        if '# COLDWAR | Modern Cyprus events' in text:return re.sub(r'(?m)^[\t ]+$','',text)
        # Only the effect body of this existing country-specific pulse is wrapped.
        oa,ob=body_span(text,'on_actions');inner=text[oa:ob]
        m=re.search(r'(?m)^\s*on_weekly_CYP\s*=\s*\{',inner)
        assert m
        # effect is the first effect in this small file.
        em=re.search(r'\beffect\s*=\s*\{',text)
        start=em.end();depth=1;end=None
        for t in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',text[start:]):
            if t[0]=='{':depth+=1
            elif t[0]=='}':
                depth-=1
                if not depth:end=start+t.start();break
        assert end
        old='\n'.join('\t'+line if line.strip() else '' for line in text[start:end].splitlines())
        return text[:start]+'\n\t\t\t# IMPERIA CW — Cold War: cyprus 1970 generated content.\n\t\t\t# COLDWAR | Modern Cyprus events remain outside the 1970 campaign.\n\t\t\tif = {\n\t\t\t\tlimit = { NOT = { IMP_is_1970_scenario = yes } }\n'+old+'\n\t\t\t}\n\t\t'+text[end:]
    update('common/on_actions/CYP_on_actions.txt',modern_tick)
    def modern_decisions(text):
        marker='# COLDWAR | Modern EU/gas decisions'
        if marker in text:return text
        # Guard every decision's immutable tag eligibility, retaining later starts.
        return marker+' are unavailable in the 1970 campaign.\n'+text.replace('allowed = { original_tag = CYP }','allowed = { original_tag = CYP NOT = { IMP_is_1970_scenario = yes } }')
    update('common/decisions/CYP_decisions.txt',modern_decisions)
    def other_modern_category(text):
        a,b=body_span(text,'CYP_NCY_diplomatic_category')
        body=text[a:b]
        if 'COLDWAR | 1970 uses its own diplomatic dossier' not in body:
            body=body.replace('allowed = {','allowed = {\n\t\t# COLDWAR | 1970 uses its own diplomatic dossier.\n\t\tNOT = { IMP_is_1970_scenario = yes }',1)
        return text[:a]+body+text[b:]
    update('common/decisions/categories/99_GRE_decision_categories.txt',other_modern_category)
    def party_loc(text):
        from politics import integrate_party_names
        return integrate_party_names(c,text)
    update('common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt',party_loc)
    c.write('tools/cyprus_1970/integration.json',__import__('json').dumps(changed,indent=2)+'\n')
