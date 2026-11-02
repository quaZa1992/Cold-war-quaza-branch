# IMPERIA COLD WAR — Brazil installed effect catalogue from the runtime model.
from common import *

def catalogue(d):
    by={n['key']:n for n in d['nodes']};groups={g['id']:g for g in d['groups']}
    def rows(es):
        result=[]
        for e in es:
            kind=e['kind']
            if kind=='modifier':
                key=e['key'];v=e['value'];amount=(('+' if v>=0 else '')+num(v)+' percentage points') if key=='interest_rate_multiplier_modifier' else ('+' if v>=0 else '')+num(v*100)+'%'
                s=d['labels'][key]+': '+amount
            elif kind=='treasury_gdp':s='Treasury: '+num(e['percent'])+'% of payer current GDP, once'
            elif kind=='weekly_gdp_expense':s='Weekly expense: '+num(e['annual_gdp_percent'])+'% of payer current annual GDP / 52'
            elif kind=='weekly_transfer':s='Weekly '+e['direction']+': '+num(e['annual_gdp_percent'])+'% of Brazil current annual GDP / 52'
            elif kind=='building':s=d['state_names'].get(str(e['state']),d['state_names'].get(e['state'],str(e['state'])))+': +'+str(e['slots'])+' shared slots, then +'+str(e['amount'])+' '+d['building_labels'][e['building']]+(' construction' if e.get('instant') is False else ' completed')
            elif kind=='research':s=d['category_labels'].get(e['category'],e['category'])+' research bonus: +'+num(e['bonus']*100)+'%, '+str(e['uses'])+' use(s)'
            elif kind=='experience':s=e['service'].title()+' experience: +'+str(e['amount'])
            elif kind=='faction_opinion':s=e['faction'].replace('_',' ').title()+' opinion: '+('+' if e['value']>=0 else '')+num(e['value'])+' points, if that native faction is active'
            elif kind=='remove_spirit':s='Remove '+e['spirit']
            elif kind=='unlock_decision':s='Unlock decision '+e['id']
            elif kind=='event':s='Event: '+e['id']
            elif kind=='suspend_agreement':s='Terminate agreement '+e['agreement']+' and remove both spirits'
            else:raise ValueError(e)
            result.append('- '+s)
        return result
    out=['IMPERIA COLD WAR','','# Brazil 1970 installed effects','','Generated from the installed runtime model. Spatial approval remains immutable. Modifier translations are recorded in `native_adjustments.py` and `runtime_design.json`. These rows describe authored effects; native engine results are recorded separately.','','## Starting spirits','']
    for s in d['starting_spirits']:out+=['### '+s['title'],'',s['description'],'']+rows(s['effects'])+['']
    for g in d['groups']:
        out+=['## '+g.get('title',g.get('name',g['id'])),'']
        for n in d['nodes']:
            if n['group']!=g['id']:continue
            out+=['### '+n['title'],'','`'+n['id']+'`, grid ('+str(n['x'])+', '+str(n['y'])+'), focus cost '+num(n['cost'])+'.',n['description'],'']
            if n['prerequisites']:out+=['Prerequisites: '+' AND '.join('('+' OR '.join(by[k]['title'] for k in p)+')' for p in n['prerequisites'])+'.','']
            if n['exclusions']:out+=['Mutually exclusive with: '+', '.join(by[k]['title'] for k in n['exclusions'])+'.','']
            if groups[n['group']]['slot'] is not None:out+=['Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.','']
            out+=rows(n['effects'])+['']
            if n.get('offer'):
                o=n['offer'];out+=['Recipient: '+o['partner_name']+'. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.','']
                for side in ('brazil','recipient'):out+=['**'+o[side]['name']+'**','']+rows(o[side]['effects'])+['']
    out+=['## Domestic decisions','']
    for de in d['decisions']:out+=['### '+de['title'],'']+rows(de['effects'])+['']
    out+=['## Domestic events','']
    for e in d['events']:
        out+=['### '+e['title'],'',e['description'],'','Lifetime: '+e['lifetime']+'.','']
        for op in e['options']:out+=['**'+op['title']+'**','']+rows(op['effects'])+['']
    return '\n'.join(out)+'\n'
