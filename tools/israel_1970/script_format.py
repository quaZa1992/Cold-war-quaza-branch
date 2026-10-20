"""Format generated Clausewitz blocks with MD tabs and compact simple clauses."""
import re

PATTERN=r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|>=|<=|!=|=|<|>|[^\s{}<>=!#"]+'

def read(source):
    tokens=[m[0] for m in re.finditer(PATTERN,source)]
    assert not any(t in ('>=','<=','!=') for t in tokens),'Unsupported compound comparison'
    cursor=0
    def block(nested=False):
        nonlocal cursor
        result=[]
        while cursor<len(tokens):
            key=tokens[cursor];cursor+=1
            if key=='}':
                assert nested,'Unexpected closing brace'
                return result
            if key.startswith('#'):result.append((key,None,None));continue
            if cursor<len(tokens) and tokens[cursor] in ('=','>','<'):
                op=tokens[cursor];cursor+=1
                value=tokens[cursor];cursor+=1
                if value=='{':value=block(True)
                result.append((key,op,value))
            else:result.append((key,None,''))
        assert not nested,'Unclosed block'
        return result
    return block()

def format_script(source):
    def render(items,depth=0):
        lines=[]
        for key,op,value in items:
            pad='\t'*depth
            if op is None:lines.append(pad+key);continue
            head=key+' '+op+' '
            if isinstance(value,list):
                simple=all(not isinstance(v,list) and not k.startswith('#') for k,o,v in value)
                inner=' '.join(k+' '+o+' '+v if o else k for k,o,v in value) if simple else ''
                limit=180 if key in ('add_to_variable','custom_effect_tooltip','add_tech_bonus') else 100
                if simple and len(head+inner)<limit and depth>0 and key!='shortcut':
                    lines.append(pad+head+'{ '+inner+' }')
                else:
                    if depth==1 and key in ('focus','shortcut'):lines.append('')
                    if depth==2 and key in ('available','search_filters','completion_reward','ai_will_do'):lines.append('')
                    lines.append(pad+head+'{')
                    lines.extend(render(value,depth+1))
                    lines.append(pad+'}')
            else:lines.append(pad+head+value)
        return lines
    return re.sub(r'\n{3,}','\n\n','\n'.join(render(read(source))))+'\n'
