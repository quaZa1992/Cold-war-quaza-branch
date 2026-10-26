# IMPERIA CW — Cold War: focused source-level Spanish acceptance transactions.
"""Evaluate emitted acceptance effects; does not model the HOI4 scheduler or UI."""
from copy import deepcopy
from pathlib import Path
import json
from agreements import build, P
from script_ast import parse, first

ROOT = Path(__file__).resolve().parents[2]
DESIGN = json.loads((Path(__file__).parent/'approved_design.json').read_text(encoding='utf-8-sig'))
OUT = build(ROOT, DESIGN)
EFFECTS = {k:v for k,_,v in parse(OUT['common/scripted_effects/COLDWAR_SPR_v2_agreements.txt'])}
TRIGGERS = {k:v for k,_,v in parse(OUT['common/scripted_triggers/COLDWAR_SPR_v2_agreements.txt'])}


class Model:
    def __init__(self, slug, recipient, focus):
        self.slug, self.recipient = slug, recipient
        self.stem = P+'v2_'+slug
        self.countries = {t:dict(flags=set(),vars={'treasury':10},ideas=set(),xp={},relations=set()) for t in ['SPR',recipient]}
        self.countries['SPR']['flags'].update({P+'applied_'+focus, P+'unlock_'+slug, self.stem+'_pending@'+recipient})
        self.temp = {}

    def scope(self, name, ctx):
        return {'ROOT':self.recipient,'THIS':ctx[0],'PREV':ctx[1],'FROM':'SPR'}.get(name,name)

    def dynamic(self, name, ctx):
        if '@' in name:
            left, right = name.split('@')
            return left+'@'+self.scope(right,ctx)
        return name

    def value(self, text, ctx):
        try: return float(text)
        except (ValueError,TypeError): pass
        return self.countries[ctx[0]]['vars'].get(self.dynamic(text,ctx),0)

    def trigger(self, rows, ctx):
        checks=[]
        for key,op,val in rows:
            nation=self.countries[ctx[0]]
            if key in TRIGGERS: result=self.trigger(TRIGGERS[key],ctx)
            elif key in self.countries or key in ('ROOT','THIS','PREV','FROM'):
                result=self.trigger(val,(self.scope(key,ctx),ctx[0]))
            elif key in ('AND','hidden_trigger'): result=self.trigger(val,ctx)
            elif key=='OR': result=any(self.trigger([row],ctx) for row in val)
            elif key=='NOT': result=not self.trigger(val,ctx)
            elif key=='tag': result=ctx[0]==val
            elif key=='IMP_is_1970_scenario': result=True
            elif key=='exists': result=(ctx[0] in self.countries)==(val=='yes')
            elif key=='is_subject': result=val=='no'
            elif key=='has_war_with': result=False
            elif key=='has_country_flag': result=self.dynamic(val,ctx) in nation['flags']
            elif key=='has_idea': result=val in nation['ideas']
            elif key=='has_military_access_to': result=False
            elif key=='check_variable':
                if first(val,'var'):
                    left=self.value(first(val,'var'),ctx);right=self.value(first(val,'value'),ctx)
                    comparison=first(val,'compare','equals')
                    result={'greater_than_or_equals':left>=right,'less_than_or_equals':left<=right,'equals':left==right}[comparison]
                else:
                    name,comparison,target=val[0];left=self.value(name,ctx);right=self.value(target,ctx)
                    result={'=':left==right,'>':left>right,'<':left<right}[comparison]
            else: raise AssertionError('Unsupported trigger '+key)
            checks.append(result)
        return all(checks)

    def effects(self, rows, ctx):
        for key,_,val in rows:
            nation=self.countries[ctx[0]]
            if key in EFFECTS: self.effects(EFFECTS[key],ctx)
            elif key in self.countries or key in ('ROOT','THIS','PREV','FROM'):
                self.effects(val,(self.scope(key,ctx),ctx[0]))
            elif key=='if':
                if self.trigger(first(val,'limit'),ctx): self.effects([row for row in val if row[0]!='limit'],ctx)
            elif key=='hidden_effect': self.effects(val,ctx)
            elif key=='set_country_flag': nation['flags'].add(self.dynamic(val if isinstance(val,str) else first(val,'flag'),ctx))
            elif key=='clr_country_flag': nation['flags'].discard(self.dynamic(val,ctx))
            elif key=='set_temp_variable': self.temp[val[0][0]]=self.value(val[0][2],ctx)
            elif key=='modify_treasury_effect': nation['vars']['treasury']+=self.temp['treasury_change']
            elif key in ('army_experience','air_experience'): nation['xp'][key]=nation['xp'].get(key,0)+float(val)
            elif key=='add_timed_idea': nation['ideas'].add(first(val,'idea'))
            elif key=='diplomatic_relation': nation['relations'].add((first(val,'country'),first(val,'relation'),first(val,'active')))
            elif key=='add_to_variable':
                name,_,amount=val[0];name=self.dynamic(name,ctx)
                nation['vars'][name]=nation['vars'].get(name,0)+self.value(amount,ctx)
            elif key in ('calculate_new_bonds_held','calculate_new_bonds_owed'):
                # Native aggregate readers are checked structurally below; the
                # actual bilateral ledger written by the source is modelled.
                pass
            else: raise AssertionError('Unsupported effect '+key)

    def accept(self): self.effects(EFFECTS[self.stem+'_accept'],(self.recipient,'SPR'))


def main():
    checks=0
    for slug, recipient, focus, paid, receive, xp in [
        ('bilateral_training','USA','atlantic_contacts',.3,-.3,20),
        ('mediterranean_offer','ITA','mediterranean_contacts',.5,-.5,0),
        ('maghreb_commerce','MOR','maghreb_dialogue',.5,-.5,0),
        ('iberoamerican_credit','ARG','iberoamerican_links',2,2,0),
    ]:
        base=Model(slug,recipient,focus)
        good=deepcopy(base);good.accept()
        assert abs(good.countries['SPR']['vars']['treasury']-(10-paid))<.00001
        assert abs(good.countries[recipient]['vars']['treasury']-(10+receive))<.00001
        if xp: assert good.countries[recipient]['xp']['army_experience']==xp
        if slug=='iberoamerican_credit': assert good.countries['SPR']['vars']['given_bonds@ARG']==2
        snapshot=deepcopy(good.countries);good.accept();assert good.countries==snapshot
        checks+=1
        wrong=Model(slug,'GER',focus);before=deepcopy(wrong.countries);wrong.accept();assert wrong.countries==before
        checks+=1
        # Boundary: exact funds are accepted, one unit below are not.
        equal=deepcopy(base);equal.countries['SPR']['vars']['treasury']=paid;equal.accept()
        assert equal.countries['SPR']['vars']['treasury']==0
        checks+=1
        for failure in ('sender_funds','recipient_funds','expired','lost_focus','already_accepted'):
            bad=deepcopy(base)
            if failure=='sender_funds': bad.countries['SPR']['vars']['treasury']=paid-.01
            elif failure=='recipient_funds':
                if slug=='iberoamerican_credit': continue
                bad.countries[recipient]['vars']['treasury']=paid-.01
            elif failure=='expired': bad.countries['SPR']['flags'].discard(bad.stem+'_pending@'+recipient)
            elif failure=='lost_focus': bad.countries['SPR']['flags'].discard(P+'applied_'+focus)
            else: bad.countries['SPR']['flags'].add(bad.stem+'_accepted@'+recipient)
            before=deepcopy(bad.countries);bad.accept();assert bad.countries==before,(slug,failure)
            checks+=1
    for treasury, succeeds in [(1.5,True),(1.49,False)]:
        bases=Model('us_bases_offer','USA','us_negotiation')
        bases.countries['USA']['vars']['treasury']=treasury
        bases.countries['SPR']['vars']['treasury']=0
        before=deepcopy(bases.countries);bases.accept()
        if succeeds:
            assert bases.countries['USA']['vars']['treasury']==0
            assert bases.countries['SPR']['vars']['treasury']==1.5
            assert ('SPR','military_access','yes') in bases.countries['USA']['relations']
            after=deepcopy(bases.countries);bases.accept();assert bases.countries==after
        else: assert bases.countries==before
        checks+=1
    # Rebuild stability, encoding, references and scoped native patch presence.
    for name, content in OUT.items():
        if name.endswith('.txt'): parse(content)
        if name.endswith('.yml'): assert content.startswith(b'\xef\xbb\xbfl_english:')
    nato=OUT['events/NATO_system.txt']
    assert nato.count('Spain V2')==4
    assert 'COLDWAR_SPR_v2_nato_sponsor = FROM.id' in nato
    assert 'COLDWAR_SPR_v2_nato_leader_approved' in nato
    assert set(json.loads(OUT['tools/spain_1970_v2/agreements_previews.json']))=={P+s for s in [e['id'].removeprefix(P) for n in DESIGN['nodes'] if n['group'] in ('development','military','foreign') for e in n['effects'] if e['type']=='decision']}
    print(json.dumps({'source_transaction_cases':checks,'parse':'pass','encoding':'pass','engine':'not run'}))


if __name__=='__main__': main()
