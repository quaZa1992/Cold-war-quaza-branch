# IMPERIA COLD WAR — Execute emitted treaty AST with hostile transaction and lifecycle cases
"""A source-level semantic model. Native execution and multiplayer are separate checks."""
import copy,json,math,re
from pathlib import Path
from behavior_tests import Model,parser,ROOT,HERE


class TreatyModel(Model):
    def __init__(self):
        super().__init__();self.tags.update(FRA=6,ENG=7)
        for t in ('FRA','ENG'):self.v[t]={};self.a[t]={};self.flags[t]=set()
        self.stocks={t:{} for t in self.tags};self.ideas={t:set() for t in self.tags};self.events=[];self.news=[];self.targets={};self.opinions={};self.wars=set();self.missions={};self.volunteers={};self.dead=set()
        for t in self.tags:self.v[t].update(political_power=500,command_power=100,treasury=1000)
        for p in (ROOT/'common/scripted_effects').glob('ICW_superpower*.txt'):self.effects.update({k:b for k,o,b in parser.parse(p.read_text(encoding='utf-8'))})
        for p in (ROOT/'common/scripted_triggers').glob('ICW_superpower*.txt'):self.triggers.update({k:b for k,o,b in parser.parse(p.read_text(encoding='utf-8'))})
        # The shared regional spirit also belongs to the explicit Chinese contract.
        source=ROOT/'common/scripted_triggers/COLDWAR_USA_kissinger.txt'
        if source.exists():self.triggers.update({k:b for k,o,b in parser.parse(source.read_text(encoding='utf-8'))})
    def country(self,key,ctx):
        if key.startswith('event_target:'):return self.targets.get(key.split(':',1)[1])
        return super().country(key,ctx)
    def value(self,key,ctx):
        if isinstance(key,str) and key.startswith('num_equipment@'):return self.stocks[ctx[0]].get(key.split('@',1)[1],0)
        return super().value(key,ctx)
    def scalar(self,key,ctx):
        if str(key).startswith('var:'):return self.value(key[4:],ctx)
        if key in ('THIS','ROOT','PREV') or key in self.tags or str(key).startswith(('var:','event_target:')):
            c=self.country(key,ctx);return self.tags.get(c,0)
        return self.value(key,ctx)
    def predicate(self,k,o,b,ctx):
        if k=='exists':return (ctx[0] not in self.dead)==(b=='yes')
        if k=='country_exists':return b in self.tags and b not in self.dead
        if k=='has_idea':return b in self.ideas[ctx[0]]
        if k=='has_political_power':return self.compare(self.v[ctx[0]].get('political_power',0),float(b),o)
        if k=='is_in_array':
            f=dict((k,v) for k,o,v in b);owner,key=self.owner(f['array'],ctx)
            return self.scalar(f['value'],ctx) in self.a[owner].get(key,[])
        if k=='has_war_with':return (ctx[0],self.country(b,ctx)) in self.wars
        if k=='is_embargoing':return (ctx[0],self.country(b,ctx)) in getattr(self,'embargoes',set())
        if k=='has_game_rule':return True
        if k=='has_attache_from':return self.missions.get((self.country(b,ctx),ctx[0]),False)
        if k=='has_volunteers_amount_from':
            f=dict((k,v) for k,o,v in b);return self.volunteers.get((self.country(f['tag'],ctx),ctx[0]),0)>0
        if k in ('political_power','command_power'):return self.compare(self.v[ctx[0]].get(k,0),float(b),o)
        if k.startswith('event_target:'):
            tag=self.country(k,ctx);return tag is not None and self.test(b,(tag,ctx[0],ctx[2]))
        return super().predicate(k,o,b,ctx)
    def run(self,rows,ctx):
        previous=None
        for k,o,b in rows:
            if k in ('if','else_if','else'):
                if k=='if':previous=False
                take=not previous and (k=='else' or self.test(next(v for n,o,v in b if n=='limit'),ctx))
                if take:self.run([r for r in b if r[0]!='limit'],ctx);previous=True
                continue
            if k=='effect_tooltip':continue
            if k in self.effects:self.run(self.effects[k],ctx);continue
            if k in ('multiply_variable','divide_variable','multiply_temp_variable','divide_temp_variable'):
                key,op,val=b[0];owner,key=self.owner(key,ctx);key=self.index(key,ctx);table=self.temp if '_temp_' in k else self.v[owner];factor=self.value(val,ctx)
                table[key]=table.get(key,0)*factor if k.startswith('multiply') else table.get(key,0)/factor;continue
            if k in ('round_variable','round_temp_variable'):
                owner,key=self.owner(b,ctx);table=self.temp if '_temp_' in k else self.v[owner];table[key]=math.floor(table.get(key,0)+0.5);continue
            if k in ('clamp_variable','clamp_temp_variable'):
                f=dict((k,v) for k,o,v in b);owner,key=self.owner(f['var'],ctx);table=self.temp if '_temp_' in k else self.v[owner];table[key]=max(float(f.get('min',-math.inf)),min(float(f.get('max',math.inf)),table.get(key,0)));continue
            if k=='remove_from_array':
                f=dict((k,v) for k,o,v in b);owner,key=self.owner(f['array'],ctx);items=self.a[owner].get(key,[])
                if 'index' in f:items.pop(int(self.value(f['index'],ctx)))
                else:self.a[owner][key]=[v for v in items if v!=self.scalar(f['value'],ctx)]
                continue
            if k in ('add_ideas','remove_ideas'):
                if k=='add_ideas':self.ideas[ctx[0]].add(b)
                else:self.ideas[ctx[0]].discard(b)
                continue
            if k in ('add_political_power','add_command_power'):
                key='political_power' if k=='add_political_power' else 'command_power';self.v[ctx[0]][key]+=self.value(b,ctx);continue
            if k=='modify_treasury_effect':
                self.v[ctx[0]]['treasury']+=self.value('treasury_change',ctx);continue
            if k=='add_equipment_to_stockpile':
                f=dict((k,v) for k,o,v in b);q=self.value(f['amount'],ctx);self.stocks[ctx[0]][f['type']]=self.stocks[ctx[0]].get(f['type'],0)+q;assert self.stocks[ctx[0]][f['type']]>=0;continue
            if k in ('country_event','news_event'):
                f=dict((k,v) for k,o,v in b);(self.events if k=='country_event' else self.news).append((f['id'],ctx[0]));continue
            if k=='save_event_target_as':self.targets[b]=ctx[0];continue
            if k in ('add_opinion_modifier','remove_opinion_modifier'):
                f=dict((k,v) for k,o,v in b);key=(ctx[0],self.country(f['target'],ctx),f['modifier'])
                if k.startswith('add'):self.opinions[key]=1
                else:self.opinions.pop(key,None)
                continue
            if k=='recall_attache':self.missions.pop((ctx[0],self.country(b,ctx)),None);continue
            if k=='recall_volunteers_from':self.volunteers.pop((ctx[0],self.country(b,ctx)),None);continue
            if k in ('PREV','ROOT','THIS'):
                c=self.country(k,ctx);self.run(b,(c,ctx[0],ctx[2]));continue
            if k.startswith('event_target:'):
                c=self.country(k,ctx);assert c;self.run(b,(c,ctx[0],ctx[2]));continue
            super().run([(k,o,b)],ctx)


def main():
    checks=[]
    def check(test,label):assert test,label;checks.append(label)
    def prepared(n=5):
        m=TreatyModel();m.stocks['USA']['nuclear_missile_equipment_1']=100;m.stocks['SOV']['nuclear_missile_equipment_1']=200
        m.call(f'icwt_edit_{n}');return m
    m=prepared();m.call('icwt_send_5');rev=m.v['global']['icwt_p_revision']
    check(m.stocks['USA']['nuclear_missile_equipment_1']==100 and not m.ideas['USA'] and not m.news,'Sending an offer cannot retire equipment, grant spirits or announce signature')
    m.call('icwt_sign_5','SOV');check(not m.ideas['SOV'],'Unreviewed signature is rejected')
    m.call('icwt_review_5','SOV');m.call('icwt_sign_5','SOV')
    check(m.stocks['USA']['nuclear_missile_equipment_1']==75 and m.stocks['SOV']['nuclear_missile_equipment_1']==150,'Both exact frozen ICBM reserve reductions execute after real core consent')
    check(all('icwt_spirit_5' in m.ideas[t] for t in ('USA','SOV')),'Each core party receives the named treaty spirit')
    check(len(m.news)==1 and m.news[0][0]=='icwt.2005','One static treaty-specific international signing news is published')
    before=copy.deepcopy((m.stocks,m.ideas,m.news));m.call('icwt_sign_5','SOV');check(before==(m.stocks,m.ideas,m.news),'A repeated sign command cannot replay equipment retirement or news')
    m.call('icwt_leave_5','SOV');check('icwt_spirit_5' not in m.ideas['SOV'] and 'icwt_spirit_5' in m.ideas['USA'],'Withdrawal removes only the acting participant spirit')
    check(m.stocks['SOV']['nuclear_missile_equipment_1']==150,'Withdrawal does not restore retired equipment')
    before=len(m.news);m.call('icwt_leave_5','SOV');check(len(m.news)==before,'Repeated withdrawal cannot repeat an international announcement')
    m=prepared();m.call('icwt_send_5');m.stocks['USA']['nuclear_missile_equipment_1']=1;m.call('icwt_review_5','SOV');m.call('icwt_sign_5','SOV')
    check(not m.ideas['USA'] and not m.ideas['SOV'] and m.stocks['SOV']['nuclear_missile_equipment_1']==200,'A changed sender stockpile aborts the whole transaction before any participant retirement')
    check(not m.news and m.v['global']['icwt_pending']==5,'Failed preflight leaves a coherent unsigned pending paper')
    check(m.events[-1]==('icwt.500','SOV'),'Changed core stocks produce a clear recipient notice requiring revised terms')
    m=prepared();m.a['USA']['icwt_edit_invites']=[6];m.call('icwt_send_5');m.call('icwt_review_5','SOV');m.call('icwt_sign_5','SOV')
    check(not m.ideas['FRA'] and m.a['global']['icwt_5_members']==[1,2],'An unanswered optional invitation does not delay or silently join the core agreement')
    m.call('icwt_review_5','FRA');m.call('icwt_accept_invite_5','FRA');check('icwt_spirit_5' in m.ideas['FRA'] and m.a['global']['icwt_5_members']==[1,2,6],'Late accession requires the invited country review and approval')
    check(m.news[-1]==('icwt.2105','FRA'),'Accession announces the actual joining country through native event scope')
    before=len(m.news);m.call('icwt_accept_invite_5','FRA');check(len(m.news)==before,'An invitation receipt cannot be replayed after accession')
    m=prepared();m.a['USA']['icwt_edit_invites']=[6];m.call('icwt_send_5');m.call('icwt_review_5','FRA');old=m.v['FRA']['icwt_review_revision'];m.call('icwt_counteroffer','SOV');m.call('icwt_send_5','SOV')
    check(m.v['global']['icwt_p_revision']!=old,'A counteroffer receives a fresh immutable proposal revision')
    m.call('icwt_accept_invite_5','FRA');check(m.v['FRA'].get('icwt_accept_5',0)==0,'An old reviewed invitation cannot approve a revised paper')
    m=prepared(11);m.v['USA']['icwt_edit_reduction']=0;m.a['USA']['imp_fin_sanc_by_us']=[2];m.a['SOV']['imp_fin_sanc_on_us']=[1];m.call('icwt_send_11');m.call('icwt_review_11','SOV');m.call('icwt_sign_11','SOV')
    check(m.v['USA']['political_power']==465 and not m.a['USA']['imp_fin_sanc_by_us'] and not m.a['SOV']['imp_fin_sanc_on_us'],'Sanctions relief charges its real 35 PP once and removes both native mirrors')
    check(m.v['USA'].get('icwt_block_fin@SOV')==1,'The active selected sanctions protocol creates an enforceable bilateral moratorium')
    m.call('icwt_leave_11');check(m.v['USA'].get('icwt_block_fin@SOV')==0 and m.v['USA']['political_power']==465,'Withdrawal ends its moratorium without refunding completed relief')
    m=prepared(9);m.call('icwt_send_9');m.call('icwt_review_9','SOV');m.call('icwt_sign_9','SOV')
    check(m.v['USA']['icwt_investment@SOV']==1 and m.v['SOV']['icwt_investment@USA']==1,'Investment discounts apply only between current consenting signatories')
    check(not m.v['EGY'].get('icwt_investment@USA',0),'A non-signatory receives no investment discount')
    m.call('icwt_leave_9','SOV');check(m.v['USA']['icwt_investment@SOV']==0,'A departed counterparty loses bilateral investment benefits')
    m=prepared(8);m.v['USA']['icwt_edit_duration']=180;m.call('icwt_send_8');m.call('icwt_review_8','SOV');m.call('icwt_sign_8','SOV');m.v['global']['num_days']=181;m.call('icwt_weekly')
    check(not any('icwt_spirit_8' in m.ideas[t] for t in ('USA','SOV')) and m.a['global'].get('icwt_8_members',[])==[],'Finite treaty expiry removes all remaining membership spirits once')
    check(not any(k[2].startswith('icwt_') for k in m.opinions),'Expiry removes treaty-owned commercial opinion effects')
    m=prepared(5);before=copy.deepcopy((m.stocks,m.ideas,m.v,m.news));m.call('icwt_preview_selected');check(before==(m.stocks,m.ideas,m.v,m.news),'Native prospective effect wrapper has no gameplay transaction in the source model')
    m=prepared();m.call('icwt_send_5');before=copy.deepcopy(m.v['global']);m.call('icwt_send_8','SOV');check(m.v['global']==before,'A simultaneous second paper cannot replace the immutable pending proposal')
    m.call('icwt_review_5');m.call('icwt_sign_5');check(not m.ideas['USA'],'The proposer cannot supply the counterparty signature')
    m=prepared(11);m.a['USA']['imp_fin_sanc_by_us']=[2];m.a['SOV']['imp_fin_sanc_on_us']=[1];m.call('icwt_send_11');m.v['USA']['political_power']=1;m.call('icwt_review_11','SOV');m.call('icwt_sign_11','SOV')
    check(not m.ideas['USA'] and m.a['USA']['imp_fin_sanc_by_us']==[2] and m.v['USA']['political_power']==1,'Insufficient current sanction-lift funds abort both sides before any relief or charge')
    m=prepared(9);m.call('icwt_send_9');m.call('icwt_review_9','SOV');m.call('icwt_sign_9','SOV');m.run([('icwt_invite_active_9','=', 'yes')],('USA','ENG','USA'));m.call('icwt_review_9','ENG');m.call('icwt_accept_invite_9','ENG')
    check('icwt_spirit_9' in m.ideas['ENG'] and m.a['global']['icwt_9_members']==[1,2,7],'An additional government can review and join an already signed agreement')
    m=prepared(5);m.call('icwt_send_5');m.call('icwt_review_5','SOV');m.call('icwt_sign_5','SOV');m.call('icwt_edit_1');m.call('icwt_send_1');m.call('icwt_review_1','SOV');m.call('icwt_sign_1','SOV');m.call('icwt_edit_6');m.call('icwt_send_6');m.call('icwt_review_6','SOV');m.call('icwt_sign_6','SOV')
    m.stocks['USA']['nuclear_missile_equipment_1']=40;m.call('icwt_refresh')
    check('icwt_limit_broken_6' in m.flags['USA'] and 'icwt_limit_broken_1' not in m.flags['USA'],'Each overlapping missile ceiling is checked against its own actually signed reserve limit')
    m.call('icwt_leave_6');check('icwt_limit_broken_6' not in m.flags['USA'] and m.stocks['USA']['nuclear_missile_equipment_1']==40,'Leaving a ceiling neither destroys nor refunds missile equipment')
    m=prepared();m.v['USA'].update(icsd_tab=3,icwt_register=1)
    for n in range(1,13):m.v['USA'][f'icwt_receipt_{n}']=1
    m.v['USA']['icwt_register_offset']=8;m.call('icwt_display');check(m.a['USA']['icwt_rows']==[9,10,11,12],'The treaty register pages through all named instruments and the independent custom agreement')
    check(not m.v['USA'].get('icwt_show_member',0),'Former signatories do not display a currently granted treaty spirit')
    m=prepared(10);check(not m.test(m.triggers['icwt_edit_valid'],('USA','USA','USA')),'Regional terms require two actual valid own mission recipients before submission')
    m=prepared(5);m.call('icwt_send_5');m.call('icwt_review_5','SOV');m.call('icwt_sign_5','SOV');m.call('icwt_edit_9');m.call('icwt_send_9');m.call('icwt_review_9','SOV');m.call('icwt_sign_9','SOV');m.dead.add('SOV');m.call('icwt_weekly')
    check(m.a['global']['icwt_5_members']==[1] and m.a['global']['icwt_9_members']==[1] and not m.ideas['SOV'],'Disappeared participants lose membership and shared restraint without ending surviving participation')
    check(m.v['USA'].get('icwt_investment@SOV')==0 and m.v['SOV'].get('icwt_investment@USA')==0,'Annexation clears both bilateral investment caches before a possible country release')
    m=prepared(9);m.call('icwt_send_9');m.call('icwt_review_9','SOV');m.call('icwt_sign_9','SOV');m.wars.update({('USA','SOV'),('SOV','USA')});m.call('icwt_refresh')
    check(m.v['USA'].get('icwt_investment@SOV')==0 and m.v['global']['icwt_relief']==0,'War suspends economic partnership benefits and bilateral detente relief')
    report={'project':'IMPERIA COLD WAR','passed':len(checks),'checks':checks,'scope':'Emitted AST executed in a bounded semantic model. Not native-engine, timing or multiplayer evidence.'}
    (HERE/'treaty-behavior-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
