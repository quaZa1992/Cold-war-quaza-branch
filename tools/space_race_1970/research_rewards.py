# IMPERIA CW — Cold War: one-use scientific spillover awards covering all technologies.
import ast
from functools import lru_cache
import re


@lru_cache(maxsize=1)
def scope(root):
    # Reuse the project's script reader without executing its unrelated validators.
    source=root/'tools/israel_1970/validate_content.py';tree=ast.parse(source.read_text(encoding='utf-8'));namespace={'re':re}
    exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'tokens','parse','values','first','walk'}],type_ignores=[]),str(source),'exec'),namespace)
    parse,first=namespace['parse'],namespace['first']
    declared=set()
    for file in sorted((root/'common/technology_tags').glob('*.txt')):
        for key,op,body in parse(file.read_text(encoding='utf-8-sig')):
            if key.lower()=='technology_categories':declared.update(v for k,op,v in body if k=='_bare')
    technologies={}
    for file in sorted((root/'common/technologies').glob('*.txt')):
        body=first(parse(file.read_text(encoding='utf-8-sig')),'technologies',[])
        for ident,op,tech in body:
            if isinstance(tech,list) and not ident.startswith('@'):
                technologies[ident]={v for k,op,v in first(tech,'categories',[]) if k=='_bare'}
    assert technologies,'No technologies found for the general research award'
    categories=set().union(*(tags&declared for tags in technologies.values()))
    # Explicit technology selectors also cover uncategorised technologies and
    # existing technologies whose categories are not declared by the mod.
    uncategorised={ident for ident,tags in technologies.items() if not tags&categories}
    selectors=' '.join('category = '+tag for tag in sorted(categories))+' '+' '.join('technology = '+ident for ident in sorted(uncategorised))
    return technologies,categories,uncategorised,selectors.strip()


def award(root,name,bonus):
    # A single native award contains all selectors and one shared use. Never
    # issue a separate bonus per category, which would multiply the reward.
    return f'add_tech_bonus = {{ name = {name} bonus = {bonus:.2f} uses = 1 {scope(root)[3]} }}\n'
