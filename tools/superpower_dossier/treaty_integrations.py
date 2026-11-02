# IMPERIA COLD WAR — Narrow treaty integration into native sanctions and investment formulas
import re


def span(source,name):
    start=re.search(r'\b'+re.escape(name)+r'\s*=\s*\{',source).end();end=start;depth=1;quoted=False
    while depth:
        c=source[end]
        if c=='"':quoted=not quoted
        if not quoted:depth+=(c=='{')-(c=='}')
        end+=1
    return start,end-1


def strip(source):
    """Remove precisely this feature's two provider integrations for preservation checks."""
    for header in ('# IMPERIA COLD WAR — Native sanction actions with treaty moratorium guards\n',
                   '# IMPERIA COLD WAR — Bilateral treaty investment adjustments in native project formulas\n'):
        source=source.removeprefix(header)
    for typ,action in (('dip','diplo'),('fin','fin'),('eco','eco'),('mil','mil')):
        if 'imp_'+action+'_sanctions_impose' not in source:continue
        a,b=span(source,'imp_'+action+'_sanctions_impose');f=source[a:b]
        marker='\n\t\t\t# IMPERIA COLD WAR — Selected treaty sanction moratorium\n\t\t\ticwt_can_impose_'+typ+' = yes'
        if marker in f:
            f=f.replace(marker,'',1)
            c,d=span(f,'complete_effect');wrapped=f[c:d]
            i,j=span(wrapped,'if');inner=wrapped[i:j];u,v=span(inner,'limit')
            old=inner[v+1:].removesuffix('\n\t\t\t')
            f=f[:c]+old+f[d:];source=source[:a]+f+source[b:]
    source=re.sub(r'\n\t\t\t# IMPERIA COLD WAR — Maximum applicable bilateral treaty discount\n\t\t\ticwt_investment_cost_extra = yes','',source)
    source=re.sub(r'\n\t\t# IMPERIA COLD WAR — Maximum applicable bilateral treaty duration adjustment\n\t\ticwt_investment_duration_extra = yes','',source)
    return source


def patch(root):
    results=[]
    rel='common/scripted_diplomatic_actions/imp_sanctions_diplomatic_actions.txt'
    p=root/rel;before=p.read_text(encoding='utf-8-sig');s=before
    header='# IMPERIA COLD WAR — Native sanction actions with treaty moratorium guards\n'
    if not s.startswith(header):s=header+s
    for typ,action in (('dip','diplo'),('fin','fin'),('eco','eco'),('mil','mil')):
        a,b=span(s,'imp_'+action+'_sanctions_impose');fragment=s[a:b]
        guard='icwt_can_impose_'+typ+' = yes'
        if guard not in fragment:
            c,d=span(fragment,'selectable');fragment=fragment[:c]+'\n\t\t\t# IMPERIA COLD WAR — Selected treaty sanction moratorium\n\t\t\t'+guard+fragment[c:]
            c,d=span(fragment,'complete_effect');old=fragment[c:d]
            fragment=fragment[:c]+'\n\t\t\tif = { limit = { '+guard+' }'+old+'\n\t\t\t}\n\t\t'+fragment[d:]
            s=s[:a]+fragment+s[b:]
    if s!=before:
        assert p.read_text(encoding='utf-8-sig')==before,'Concurrent sanction edit: rebuild from current source'
        p.write_text(s,encoding='utf-8',newline='\n')
    results.append(rel)
    rel='common/scripted_effects/99_investment_scripted_effects.txt';p=root/rel;before=p.read_text(encoding='utf-8-sig');s=before
    header='# IMPERIA COLD WAR — Bilateral treaty investment adjustments in native project formulas\n'
    if not s.startswith(header):s=header+s
    for name,helper,anchor in (
        ('project_monetary_cost_calculation','icwt_investment_cost_extra','\n\t\t}\n\t}\n\tadd_to_temp_variable = { investments_cost_modifier'),
        ('precompute_state_construction_data','icwt_investment_duration_extra','\n\t\tadd_to_temp_variable = { receiving_investment_duration_temp = THIS.modifier@receiving_investment_duration_modifier }')):
        a,b=span(s,name);f=s[a:b]
        if helper+' = yes' not in f:
            assert anchor in f,(name,'complete native controller block changed')
            if name=='project_monetary_cost_calculation':f=f.replace(anchor,'\n\t\t\t# IMPERIA COLD WAR — Maximum applicable bilateral treaty discount\n\t\t\t'+helper+' = yes'+anchor,1)
            else:f=f.replace(anchor,'\n\t\t# IMPERIA COLD WAR — Maximum applicable bilateral treaty duration adjustment\n\t\t'+helper+' = yes'+anchor,1)
            s=s[:a]+f+s[b:]
    if s!=before:
        assert p.read_text(encoding='utf-8-sig')==before,'Concurrent investment edit: rebuild from current source'
        p.write_text(s,encoding='utf-8',newline='\n')
    results.append(rel)
    return results
