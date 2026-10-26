# IMPERIA CW — Cold War: currency balance — validate.
"""Validate actual currency drawbacks, their consumers and scoped changes."""
from pathlib import Path
import copy,hashlib,json,math,re,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/israel_1970'))
from script_format import read
from balance_manifest import reverse_if_recorded


def one(block,key):
    found=[v for k,o,v in block if k==key and o=='=']
    assert len(found)==1,(key,len(found))
    return found[0]
def walk(block):
    for k,o,v in block:
        yield k,o,v
        if isinstance(v,list):yield from walk(v)
def normalize(block):
    return [(k,o,normalize(v) if isinstance(v,list) else float(v)
             if isinstance(v,str) and re.fullmatch(r'-?\d+(?:\.\d+)?',v) else v) for k,o,v in block]
def parse(path):return read((ROOT/path).read_text(encoding='utf-8-sig'))
def sha(data):return hashlib.sha256(data).hexdigest()


def main():
    checks=[]
    def check(condition,label):
        assert condition,label
        checks.append(label)
    baseline=json.loads((HERE/'baseline.json').read_text())
    changes=json.loads((HERE/'changes.json').read_text())['files']
    policy=json.loads((HERE/'policy.json').read_text())
    old={}
    for name,record in baseline['before'].items():
        old[name]=reverse_if_recorded(name,(ROOT/name).read_bytes())
        check(sha(old[name])==record['sha256'],f'Exact authorized reverse-byte proof: {name}')
    for name,digest in baseline['protected'].items():
        current=(ROOT/name).read_bytes()
        check(sha(current)==digest,f'Protected asset unchanged: {name}')
    path='common/ideas/AA_law_expanded_economics.txt'
    laws=one(one(parse(path),'ideas'),'reserve_currency')
    previous=one(one(read(old[path].decode('utf-8-sig')),'ideas'),'reserve_currency')
    ids=[k for k,o,v in laws if isinstance(v,list)]
    check(ids==[k for k,o,v in previous if isinstance(v,list)],'Every currency ID and order retained')
    check(set(ids)==set(policy['added'])|set(policy['retained']),'Every currency has a specified drawback')
    for name in ids:
        before=one(previous,name);current=one(laws,name)
        check([v for v in current if v[0]!='modifier']==[v for v in before if v[0]!='modifier'],
              f'{name}: adoption, cleanup, date gates, icons and AI unchanged')
        expected=copy.deepcopy(one(before,'modifier'))
        if name=='ddr_mark':expected=[entry for entry in expected if entry[0]!='custom_modifier_tooltip']
        for key,value in policy['added'].get(name,{}).items():expected.append((key,'=',str(value)))
        check(sorted(normalize(one(current,'modifier')),key=lambda entry:entry[0])==
              sorted(normalize(expected),key=lambda entry:entry[0]),f'{name}: only approved modifier changes')
        downside=policy['added'].get(name,policy['retained'].get(name))
        entries=list(walk(one(current,'modifier')))
        for key,value in downside.items():
            matches=[float(v) for k,o,v in entries if k==key]
            check(matches==[value],f'{name}: {key} drawback applied once')
    # Registered custom modifiers have the correct sign, units and consumers.
    providers={}
    for name in ['money_modifier_definitions.txt','influence_modifier_definitions.txt','modifier_definitions.txt']:
        providers.update({k:v for k,o,v in parse('common/modifier_definitions/'+name) if isinstance(v,list)})
    for key,bad,unit in [('receiving_investment_cost_modifier','bad','percentage'),
                         ('foreign_influence_defense_modifier','good','percentage'),
                         ('interest_rate_multiplier_modifier','bad','number')]:
        check(one(providers[key],'color_type')==bad and one(providers[key],'value_type')==unit,
              f'{key}: registered sign and display units')
    investment=one(parse('common/scripted_effects/99_investment_scripted_effects.txt'),'project_monetary_cost_calculation')
    check(('add_to_temp_variable','=',[('investments_cost_modifier','=','THIS.modifier@receiving_investment_cost_modifier')])
          in list(walk(investment)),'Inbound-investment drawback is consumed as target-country project cost')
    check(math.isclose(100*(1+float(one(one(one(laws,'ddr_mark'),'modifier'),'receiving_investment_cost_modifier'))),110),
          'Ostmark adds ten percent of base cost to incoming investment projects')
    interest=one(parse('common/scripted_effects/00_money_system.txt'),'calculate_interest_rate')
    check(('add','=','modifier@interest_rate_multiplier_modifier') in list(walk(interest)),
          'Interest adjustments are additive percentage points in the native money pass')
    ddr=one(one(laws,'ddr_mark'),'modifier')
    check(sum(k=='interest_rate_multiplier_modifier' for k,o,v in walk(ddr))==1
          and not any(k=='custom_modifier_tooltip' for k,o,v in ddr),
          'Ostmark has one interest adjustment and no repeated explanatory modifier line')
    check(float(one(ddr,'political_power_gain'))==.05 and float(one(ddr,'stability_factor'))==.02
          and float(one(ddr,'interest_rate_multiplier_modifier'))==-.5,'All Ostmark benefits retained')
    for language in ['english','german']:
        raw=(ROOT/f'localisation/{language}/mdcw_ddr_currency_l_{language}.yml').read_bytes()
        source=raw.decode('utf-8-sig')
        check(raw.startswith(b'\xef\xbb\xbf') and ' ddr_mark: "Mark der DDR (Ostmark)"' in source
              and 'ddr_mark_interest_scope_tt' not in source,f'{language}: Ostmark flair name, BOM and clean tooltip')
    source=(ROOT/'localisation/english/replace/replaced_from_vanilla_modifiers_l_english.yml').read_text(encoding='utf-8-sig')
    label=re.findall(r'^ interest_rate_multiplier_modifier: "(.*)"$',source,re.M)
    check(len(label)==1 and '(percentage points)' in label[0],'English interest-rate label states percentage-point units')
    report={'status':'PASS','checks':checks,'policy':policy,
            'scope':'Static currency effects, consumers, exact preservation and localization; no in-game test.'}
    (HERE/'validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS: All {len(ids)} currency laws have drawbacks; {len(checks)} checks passed.')


if __name__=='__main__':main()
