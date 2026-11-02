# IMPERIA COLD WAR — Execute treaty programme and addendum transactions from emitted AST
"""Bounded semantic fixtures. Native fixed-point, display and multiplayer require separate checks."""
import copy
import json
import math
from test_treaties import TreatyModel,ROOT,HERE,parser

class ProgrammeModel(TreatyModel):
    def __init__(self):
        super().__init__()
        self.embargoes=set();self.external_chinese=False
        self.v['USA']['gdp_total']=1000;self.v['SOV']['gdp_total']=400
        self.v['global']['num_days']=100
    def predicate(self,k,o,b,ctx):
        if k=='is_embargoing':return (ctx[0],self.country(b,ctx)) in self.embargoes
        # This suite isolates the Soviet programme. China's own emitted-AST suite covers its contract.
        if k=='COLDWAR_USA_KS_td_regional_active':return self.external_chinese
        return super().predicate(k,o,b,ctx)
def main():
    checks=[]
    def check(condition,label):assert condition,label;checks.append(label)
    def near(a,b):return math.isclose(a,b,abs_tol=1e-8)
    def sign(m,n,tag='SOV'):
        m.call(f'icwt_send_{n}','USA');m.call(f'icwt_review_{n}',tag);m.call(f'icwt_sign_{n}',tag)
    def ready(n,pid):
        m=ProgrammeModel();m.flags['USA'].add(f'icwt_programme_{pid}_unlocked');m.call(f'icwt_edit_{n}');m.v['USA']['icwt_edit_programme']=pid;return m
    m=ready(9,1);before=copy.deepcopy((m.v,m.ideas,m.stocks,m.flags));m.call('icwt_focus_preview_9')
    check(before==(m.v,m.ideas,m.stocks,m.flags),'A locked prospective focus preview cannot pay, sign or grant programme effects')
    m.call('icwt_send_9');m.call('icwt_sign_9','SOV')
    check(m.v['USA']['treasury']==1000 and not m.ideas['USA'],'Sending and unreviewed signature cannot activate or charge a programme')
    m.v['USA']['gdp_total']=2000;m.call('icwt_review_9','SOV');m.call('icwt_sign_9','SOV')
    check(near(m.v['USA']['treasury'],999.994) and near(m.v['SOV']['treasury'],999.9988),'Both setup charges use the frozen percentage of actual current GDP at signature')
    check(all(f'icwt_programme_1_{side}' in m.ideas[tag] for tag,side in [('USA','usa'),('SOV','sov')]),'Both approved scientific spirits activate after actual joint signature')
    m.call('icwt_programme_fiscal');m.call('icwt_programme_fiscal','SOV')
    check(near(m.v['USA']['icwt_weekly_expense'],.0004) and near(m.v['SOV']['icwt_weekly_expense'],.00008),'Scientific funding is live current-GDP expense in weekly MD billions for each actual payer')
    paid=copy.deepcopy([m.v[t]['treasury'] for t in ('USA','SOV')]);m.call('icwt_programme_fiscal');m.call('icwt_sign_9','SOV')
    check(near(m.v['USA']['icwt_weekly_expense'],.0004) and paid==[m.v[t]['treasury'] for t in ('USA','SOV')],'Repeated fiscal calculation and signature cannot accumulate costs or replay setup payment')
    for condition in ('war','embargo','sanction'):
        if condition=='war':m.wars.add(('USA','SOV'))
        if condition=='embargo':m.embargoes.add(('SOV','USA'))
        if condition=='sanction':m.a['SOV']['imp_mil_sanc_by_us']=[1]
        m.call('icwt_programme_fiscal');m.call('icwt_programme_fiscal','SOV')
        check(all(f'icwt_programme_1_{side}' not in m.ideas[tag] for tag,side in [('USA','usa'),('SOV','sov')]) and m.v['USA']['icwt_weekly_expense']==0 and m.v['SOV']['icwt_weekly_expense']==0,condition+' suspends both scientific spirits and all linked weekly funding')
        m.wars.clear();m.embargoes.clear();m.a['SOV']['imp_mil_sanc_by_us']=[];m.call('icwt_programme_fiscal')
    check(paid==[m.v[t]['treasury'] for t in ('USA','SOV')],'Restoring normal bilateral relations does not repeat setup charges')
    for owner,other_id in [('USA',2),('SOV',1)]:
        for kind in ('dip','fin','eco','mil'):
            for direction in ('on','by'):
                key=f'imp_{kind}_sanc_{direction}_us';m.a[owner][key]=[other_id]
                m.call('icwt_programme_fiscal');m.call('icwt_programme_fiscal','SOV')
                check(m.v['USA']['icwt_weekly_expense']==0 and m.v['SOV']['icwt_weekly_expense']==0 and 'icwt_programme_1_usa' not in m.ideas['USA'] and 'icwt_programme_1_sov' not in m.ideas['SOV'],f'{owner} {kind} sanction mirror {direction} suspends both benefits and both funding streams')
                m.a[owner][key]=[];m.call('icwt_programme_fiscal')
    m.call('icwt_leave_9','SOV');m.call('icwt_programme_fiscal')
    check(not m.v['USA']['icwt_weekly_expense'] and 'icwt_programme_1_usa' not in m.ideas['USA'] and 'icwt_spirit_9' in m.ideas['USA'],'Partner withdrawal ends the bilateral programme while preserving remaining treaty participation')
    m=ready(1,3);m.v['USA']['icwt_edit_reduction']=25;m.stocks['USA']['nuclear_missile_equipment_1']=100;m.stocks['SOV']['nuclear_missile_equipment_1']=200;m.v['SOV']['treasury']=0
    sign(m,1)
    check(m.stocks['USA']['nuclear_missile_equipment_1']==100 and m.stocks['SOV']['nuclear_missile_equipment_1']==200 and m.v['USA']['treasury']==1000 and not m.ideas['USA'],'Insufficient partner treasury aborts all charges, stockpile retirement and membership atomically')
    check(m.v['global']['icwt_pending']==1,'An unaffordable programme remains a coherent unsigned paper')
    # Material treaty first, then a separately reviewed programme addendum.
    m=ProgrammeModel();m.call('icwt_edit_1');m.v['USA']['icwt_edit_reduction']=25;m.v['USA']['icwt_edit_duration']=365;m.a['USA']['icwt_edit_invites']=[6]
    m.stocks['USA']['nuclear_missile_equipment_1']=100;m.stocks['SOV']['nuclear_missile_equipment_1']=200;sign(m,1)
    m.call('icwt_review_1','FRA');m.call('icwt_accept_invite_1','FRA')
    material=copy.deepcopy((m.stocks,m.a['global']['icwt_1_members'],m.v['global']['icwt_1_revision'],m.v['global']['icwt_1_end'],[m.v[t]['icwt_receipt_1'] for t in ('USA','SOV','FRA')]))
    m.flags['USA'].add('icwt_programme_3_unlocked');m.call('icwt_edit_addendum_1');m.v['USA']['icwt_edit_programme']=3;m.call('icwt_send_1')
    check(m.v['global']['icwt_p_addendum']==1 and m.v['global']['icwt_p_programme']==3,'An active treaty receives a distinct immutable programme paper requiring new consent')
    m.call('icwt_sign_1','SOV');check('icwt_programme_3_usa' not in m.ideas['USA'],'A standing treaty is not consent to its unsigned programme addendum')
    m.call('icwt_review_1','SOV');m.call('icwt_sign_1','SOV')
    check(material==(m.stocks,m.a['global']['icwt_1_members'],m.v['global']['icwt_1_revision'],m.v['global']['icwt_1_end'],[m.v[t]['icwt_receipt_1'] for t in ('USA','SOV','FRA')]),'Addendum preserves every retired asset, original term, core and optional member, original revision and material receipt')
    check(near(m.v['USA']['treasury'],999.995) and near(m.v['SOV']['treasury'],999.998) and 'icwt_programme_3_usa' in m.ideas['USA'],'Only the new programme setup charges execute after addendum signature')
    check(not any('icwt_programme' in idea for idea in m.ideas['FRA']),'An optional third-party signatory never silently joins the bilateral programme')
    paid=copy.deepcopy([m.v[t]['treasury'] for t in ('USA','SOV')]);m.call('icwt_sign_1','SOV');m.call('icwt_programme_fiscal')
    check(paid==[m.v[t]['treasury'] for t in ('USA','SOV')],'A repeated addendum signature cannot replay its setup cost')
    m.call('icwt_edit_addendum_1');m.call('icwt_send_1')
    check(m.v['global'].get('icwt_pending',0)==0,'Identical already signed programme terms cannot be reattached and charged again')
    # Explicit removal is a separately signed addendum, not a silent editor change.
    m.v['USA']['icwt_edit_programme']=0;m.call('icwt_send_1');m.call('icwt_review_1','SOV');m.call('icwt_display','SOV')
    check(m.v['SOV']['icwt_show_programme']==0 and m.v['SOV']['icwt_show_addendum']==1,'Review shows the proposed removal instead of the old standing programme')
    m.call('icwt_sign_1','SOV');m.call('icwt_programme_fiscal')
    check('icwt_programme_3_usa' not in m.ideas['USA'] and 'icwt_programme_3_sov' not in m.ideas['SOV'] and not m.v['USA']['icwt_weekly_expense'] and paid==[m.v[t]['treasury'] for t in ('USA','SOV')],'Mutually approved removal ends both benefits and funding without refunding or charging setup again')
    m.call('icwt_edit_addendum_1');m.v['USA']['icwt_edit_programme']=3;m.v['USA']['icwt_edit_reduction']=100;m.call('icwt_send_1')
    check(not m.v['global'].get('icwt_pending',0),'An addendum cannot alter the original material protocols')
    m.call('icwt_edit_addendum_1');m.v['USA']['icwt_edit_programme']=3;m.call('icwt_send_1');m.call('icwt_counteroffer','SOV');m.call('icwt_cycle_programme','SOV');m.call('icwt_send_1','SOV')
    check(m.v['global'].get('icwt_pending',0)==0 and 'icwt_spirit_1' in m.ideas['USA'],'A counteroffer removing an unsigned proposed clause cannot masquerade as changed standing terms')
    m.call('icwt_edit_addendum_1');m.v['USA']['icwt_edit_programme']=3;m.call('icwt_send_1');m.call('icwt_cancel_pending','SOV')
    check('icwt_spirit_1' in m.ideas['USA'] and m.stocks['USA']['nuclear_missile_equipment_1']==75,'Refusing a programme addendum preserves the standing treaty and completed concessions')
    m.call('icwt_edit_addendum_1');m.v['USA']['icwt_edit_programme']=3;m.call('icwt_send_1');m.v['global']['num_days']=465;m.call('icwt_refresh')
    check(not m.v['global'].get('icwt_pending',0),'Expiry invalidates the outstanding addendum before stale signature')
    # Regional transfer uses exactly the same US GDP quote on both sides.
    m=ready(10,4);m.v['SOV']['treasury']=-100;m.v['USA']['icwt_edit_usa_target']=3;m.v['USA']['icwt_edit_sov_target']=4;sign(m,10);m.call('icwt_programme_fiscal');m.call('icwt_programme_fiscal','SOV')
    check(m.v['SOV']['treasury']==-100 and 'icwt_programme_4_sov' in m.ideas['SOV'],'A recipient with no setup payment can accept funded cooperation despite its existing treasury deficit')
    check(near(m.v['USA']['icwt_weekly_expense'],.0005) and near(m.v['SOV']['icwt_weekly_income'],.0005),'Regional assistance charges and credits the same current US-GDP weekly amount')
    # Continuing restraint follows the actual selected mission types and actual named recipient.
    for mode in (1,2,3):
        case=ready(10,4);case.v['USA'].update(icwt_edit_regional=mode,icwt_edit_usa_target=3,icwt_edit_sov_target=4);sign(case,10)
        paid=copy.deepcopy([case.v[tag]['treasury'] for tag in ('USA','SOV')]);announcements=copy.deepcopy(case.news)
        for actor,target in [('USA','EGY'),('SOV','ISR')]:
            for kind in ('attache','volunteers'):
                if kind=='attache':case.missions[actor,target]=True
                else:case.volunteers[actor,target]=3
                covered=mode==3 or mode==(1 if kind=='attache' else 2)
                case.call('icwt_programme_fiscal');case.call('icwt_programme_fiscal','SOV')
                paused=case.v['USA']['icwt_weekly_expense']==0 and case.v['SOV']['icwt_weekly_income']==0 and 'icwt_programme_4_usa' not in case.ideas['USA'] and 'icwt_programme_4_sov' not in case.ideas['SOV']
                active=near(case.v['USA']['icwt_weekly_expense'],.0005) and near(case.v['SOV']['icwt_weekly_income'],.0005) and 'icwt_programme_4_usa' in case.ideas['USA'] and 'icwt_programme_4_sov' in case.ideas['SOV']
                retained=case.missions.get((actor,target),False) if kind=='attache' else case.volunteers.get((actor,target),0)==3
                check((paused if covered else active) and retained and case.news==announcements,f'Protocol {mode}, {actor} {kind}: only a covered renewed deployment pauses both programme spirits and funding, without recalling it or announcing sanctions')
                case.missions.pop((actor,target),None);case.volunteers.pop((actor,target),None)
                case.call('icwt_programme_fiscal');case.call('icwt_programme_fiscal','SOV')
                check(near(case.v['USA']['icwt_weekly_expense'],.0005) and near(case.v['SOV']['icwt_weekly_income'],.0005) and paid==[case.v[tag]['treasury'] for tag in ('USA','SOV')],f'Protocol {mode}, {actor} {kind}: mission withdrawal restores the same matched funding without repeating setup costs')
        for side,target_id,target in [('usa',3,'EGY'),('sov',4,'ISR')]:
            key='icwt_10_'+side+'_target'
            case.v['global'][key]=0;case.call('icwt_programme_fiscal');case.call('icwt_programme_fiscal','SOV')
            check(case.v['USA']['icwt_weekly_expense']==0 and case.v['SOV']['icwt_weekly_income']==0,f'Protocol {mode}: missing {side} recipient suspends funding rather than masquerading as zero missions')
            case.v['global'][key]=target_id;case.dead.add(target);case.call('icwt_programme_fiscal');case.call('icwt_programme_fiscal','SOV')
            check(case.v['USA']['icwt_weekly_expense']==0 and case.v['SOV']['icwt_weekly_income']==0,f'Protocol {mode}: disappeared {side} recipient suspends funding')
            case.dead.remove(target);case.call('icwt_programme_fiscal');case.call('icwt_programme_fiscal','SOV')
            check(near(case.v['USA']['icwt_weekly_expense'],.0005) and near(case.v['SOV']['icwt_weekly_income'],.0005) and paid==[case.v[tag]['treasury'] for tag in ('USA','SOV')],f'Protocol {mode}: restored {side} recipient resumes funding without a new payment or recall')
    bare=ProgrammeModel();bare.call('icwt_edit_10');bare.v['USA'].update(icwt_edit_usa_target=3,icwt_edit_sov_target=4)
    bare.volunteers['USA','EGY']=2;bare.volunteers['SOV','ISR']=2;bare.wars.add(('EGY','ISR'));sign(bare,10)
    bare.volunteers['SOV','ISR']=4;bare.call('icwt_refresh')
    check(all('icwt_spirit_10' in bare.ideas[tag] for tag in ('USA','SOV')) and bare.volunteers['SOV','ISR']==4 and ('EGY','ISR') in bare.wars,'The bare Regional Stand-down remains a one-time recall: renewed deployments do not end its treaty or the local war')
    ideas=parser.parse((ROOT/'common/ideas/ICW_superpower_treaties.txt').read_text(encoding='utf-8'))
    country=next(body for key,op,outer in ideas if key=='ideas' for key,op,body in outer if key=='country')
    programmes=[body for key,op,body in country if key.startswith('icwt_programme_')]
    check(len(programmes)==8 and all(('allowed_civil_war','=',[('always','=','no')]) in body for body in programmes),'All eight new paired programme spirits explicitly prohibit inheritance by civil-war breakaways')
    # Existing tension relief has an exact prospective row, with no second runtime reward.
    for label,tension,relief,initialised,joint,addendum,expected in [
        ('new instrument',50,0,True,False,False,-1),
        ('five-point cap',50,5,True,False,False,0),
        ('zero tension',0,0,True,False,False,0),
        ('remaining tension clamp',.5,0,True,False,False,-.5),
        ('existing joint instrument',50,0,True,True,False,0),
        ('programme addendum',50,0,True,False,True,0),
        ('uninitialised system',50,0,False,False,False,0),
    ]:
        preview=ProgrammeModel();preview.v['global'].update(mdcw_cw_tension=tension,icwt_relief=relief)
        if initialised:preview.flags['global'].add('mdcw_cw_initialized')
        if joint:
            preview.a['global']['icwt_9_members']=[1,2]
            for tag in ('USA','SOV'):preview.flags[tag].add('icwt_member_9')
        if addendum:preview.v['global'].update(icwt_pending=9,icwt_p_addendum=1)
        preview.call('icwt_tension_terms_9')
        check(near(preview.v['USA'].get('icwt_preview_tension',0),expected) and preview.v['global']['mdcw_cw_tension']==tension,f'{label}: prospective treaty tension row is bounded and never changes actual Cold War tension')
    preview=ProgrammeModel();preview.flags['global'].add('mdcw_cw_initialized');preview.v['global']['mdcw_cw_tension']=50
    state=copy.deepcopy((preview.v,preview.flags,preview.ideas,preview.stocks));preview.call('icwt_focus_preview_9')
    check(state==(preview.v,preview.flags,preview.ideas,preview.stocks),'A focus preview containing treaty relief remains non-executing for actual tension, treasury, spirits and assets')
    m.external_chinese=True;m.call('icwt_leave_10','SOV')
    check('icwt_programme_4_usa' in m.ideas['USA'] and 'icwt_programme_4_sov' not in m.ideas['SOV'],'Shared American regional spirit survives Soviet withdrawal while the separate Chinese contract remains active')
    report={'project':'IMPERIA COLD WAR','passed':len(checks),'checks':checks,'scope':'Actual emitted treaty AST, bounded state and fiscal fixtures. Chinese contract activation is an explicit external fixture here. Not native fixed-point, display, timing or multiplayer evidence.'}
    (HERE/'programme-behavior-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
