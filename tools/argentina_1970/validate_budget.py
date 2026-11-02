# IMPERIA COLD WAR — Independent installed GDP cost contracts.
"""Check monetary preview/execution parity and price tiers from emitted ASTs."""
import hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,walk,values

def main():
    checks=[]
    def ck(ok,name):checks.append(dict(name=name,passed=bool(ok)))
    d=json.loads((HERE/'runtime_design.json').read_text(encoding='utf-8'))
    core=dict((k,v) for k,o,v in parse((ROOT/'common/scripted_effects/COLDWAR_ARG_1970_core.txt').read_text()))
    treaty=dict((k,v) for k,o,v in parse((ROOT/'common/scripted_effects/COLDWAR_ARG_1970_treaties.txt').read_text()))
    tr=dict((k,v) for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_ARG_1970_core.txt').read_text()))
    def invoices(rows):return [first(v,'treasury_change') for k,o,v in walk(rows) if k=='set_temp_variable' and first(v,'treasury_change') is not None]
    def weekly_quotes(rows):return [first(v,'COLDWAR_ARG_weekly_amount') for k,o,v in walk(rows) if k=='set_temp_variable' and first(v,'COLDWAR_ARG_weekly_amount') is not None]
    def check_fee(rows,amount,name):
        q=invoices(rows)
        if amount>0:
            ck(len(q)==1 and isinstance(q[0],list),name+' GDP invoice')
            if len(q)==1 and isinstance(q[0],list):ck(first(q[0],'value')=='gdp_total' and float(first(q[0],'multiply'))==-amount,name+' own GDP and rate')
        else:ck(not q,name+' no spending invoice')
    for n in d['nodes']:
        preview=core['COLDWAR_ARG_preview_focus_'+n['key']];actual=core['COLDWAR_ARG_complete_'+n['key']]
        ck(invoices(preview)==invoices(actual),n['id']+' preview/charge parity')
        check_fee(actual,n['money_gdp_share'],n['id'])
        if n['money_gdp_share'] or n['weekly_annual_gdp_share']:
            ck(any(k=='gdp_total' and op=='>' and v=='0' for k,op,v in walk(tr['COLDWAR_ARG_can_complete_'+n['key']])),n['id']+' valid GDP guard')
        if n['weekly_annual_gdp_share']:
            quotes=weekly_quotes(preview)
            ck(len(quotes)==1 and first(quotes[0],'value')=='gdp_total' and first(quotes[0],'divide')=='52' and float(first(quotes[0],'multiply'))==n['weekly_annual_gdp_share'],n['id']+' weekly preview annual conversion')
    for name in ('COLDWAR_ARG_refresh_programmes','COLDWAR_ARG_refresh_event_programmes'):
        rows=core[name];ck(not invoices(rows),name+' no setup replay')
        target='COLDWAR_ARG_programme_weekly' if name.endswith('refresh_programmes') else 'COLDWAR_ARG_event_weekly'
        ck(any(k=='set_variable' and first(v,target)=='0' for k,o,v in walk(rows)),name+' zeroed aggregate')
        ck(any(k=='multiply_variable' and first(v,target)=='gdp_total' for k,o,v in walk(rows)),name+' live GDP multiplier')
        ck(any(k=='divide_variable' and first(v,target)=='52' for k,o,v in walk(rows)),name+' weekly divisor')
    for a in d['agreements']:
        preview=treaty['COLDWAR_ARG_preview_'+a['id']];actual=treaty['COLDWAR_ARG_execute_treaty_'+a['id']]
        ck(invoices(preview)==invoices(actual),a['id']+' all prospective invoice parity')
        q=invoices(actual)
        ck(all(isinstance(v,list) for v in q),a['id']+' no flat setup invoice')
        ck(all(first(v,'value') in ('gdp_total','ARG.gdp_total') for v in q),a['id']+' explicit GDP basis')
        if a.get('transfer'):
            annual=a['transfer']['annual_arg_gdp_share']
            occurrences=[]
            for rel in ('common/scripted_effects/COLDWAR_ARG_1970_treaties.txt',):
                text=(ROOT/rel).read_text();occurrences=re.findall(r'value = ARG\.gdp_total multiply = '+str(annual)+r' divide = 52',text)
            ck(len(occurrences)>=4,a['id']+' matching transfer previews/debit/credit')
    for rel in ('common/scripted_effects/COLDWAR_ARG_1970_core.txt','common/scripted_effects/COLDWAR_ARG_1970_treaties.txt'):
        s=(ROOT/rel).read_text();ck(not re.search(r'(?<![\w.])-?\d+\.\d{6,}(?![\w.])',s),rel+' native budget literal precision')
    # A later layout-only request changes coordinates, preserving all financial rewards.
    approved=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'))
    keys=('id','anchor','prerequisites','excludes','days','cost','modifiers','buildings','research','xp','doctrine','wargoal')
    for before,after in zip(approved['nodes'],d['nodes']):ck(all(before[k]==after[k] for k in keys),after['id']+' preserved structure and material rewards')
    result=dict(project='IMPERIA COLD WAR',passed=all(c['passed'] for c in checks),checks=len(checks),failed=[c['name'] for c in checks if not c['passed']],boundary='Installed-source price contracts; native behavior is tested separately.')
    (HERE/'GDP_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result));return not result['passed']
if __name__=='__main__':raise SystemExit(main())
