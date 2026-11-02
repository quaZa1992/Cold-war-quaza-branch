# IMPERIA COLD WAR — International operations and concurrent work orders.
"""Native flag cards, consent controls and clear national trade-offs."""
from PIL import Image, ImageDraw
from crew_ui import flag
from cooperation import eligible, ORDERS, ROLES, order


def controls(c,a):
    text,button,icon,tab=(a[k] for k in ['text','button','icon','tab'])
    cv,sv=c['cv'],c['sv'];view=tab(10);active=view+' '+cv('cw_sr_op_available','=',1);dashboard=view+' '+cv('cw_sr_op_available','=',0)
    outbound='OR = { '+' '.join(cv(order(w,'status'),'>',0) for w in ORDERS)+' }'
    button('cw_sr_control_operations',620,523,256,25,'International operations  >',sv('cw_sr_tab',10)+'clr_country_flag = cw_sr_partner_catalogue_cached\n',tab(8)+' '+cv('cw_sr_op_available','=',1),size=12)
    button('cw_sr_brief_operations',440,876,760,28,'Review our international work orders  >',sv('cw_sr_tab',10)+'clr_country_flag = cw_sr_partner_catalogue_cached\n',tab(2)+' '+outbound,size=12)
    button('cw_sr_crew_operations',792,999,410,23,'Operational partners & work orders  >',sv('cw_sr_tab',10)+'clr_country_flag = cw_sr_partner_catalogue_cached\n',tab(9),size=12)
    icon('cw_sr_op_background',0,264,'operations',active)
    icon('cw_sr_op_orders_background',0,264,'operations_orders',dashboard)
    text('cw_sr_op_heading',24,282,850,22,'FLIGHT OPERATIONS / INTERNATIONAL WORK PACKAGES',13,view)
    button('cw_sr_op_back',960,279,250,28,'< Mission Control',sv('cw_sr_tab',8),view,size=12)
    text('cw_sr_op_programme',24,326,1170,44,'[CW_SR_Selected_name]',23,active)
    text('cw_sr_op_orders_title',24,326,1050,44,'Our international work orders',23,dashboard)
    # IMPERIA COLD WAR — The operational selector shares the human partner list.
    button('cw_sr_op_candidate',24,380,728,90,'','cw_sr_crew_candidate_next = yes',active,cv('cw_sr_view_state','!=',4),size=13,tip='cw_sr_partner_selector_tt')
    flag(a,'cw_sr_op_candidate_flag',48,399,'cw_sr_crew_candidate',active+' '+cv('cw_sr_crew_candidate','>',0))
    icon('cw_sr_op_candidate_empty',48,399,'crew_empty_flag',active+' '+cv('cw_sr_crew_candidate','=',0))
    text('cw_sr_op_candidate_label',148,394,380,18,'PARTNER GOVERNMENT · [?cw_sr_partner_count|0] AVAILABLE',11,active)
    text('cw_sr_op_candidate_name',148,421,390,42,'[CW_SR_CrewCandidate]',19,active)
    text('cw_sr_op_candidate_next',556,420,175,24,'[CW_SR_PartnerCycle]',14,active)
    text('cw_sr_op_candidate_scope',24,471,728,15,'Only player-controlled countries at peace can receive invitations.',11,active)
    button('cw_sr_op_role',24,486,728,36,'Work package: [CW_SR_OpSelectedRole]  >','cw_sr_op_role_next = yes',active,cv('cw_sr_op_view_country','=',0)+' '+cv('cw_sr_view_state','!=',4),size=15)
    for r,(_,weeks,cost,detail) in ROLES.items():
        text(f'cw_sr_op_role_detail{r}',36,540,702,58,detail,16,active+' '+cv('cw_sr_op_view_role','=',r))
    text('cw_sr_op_partner_label',148,625,390,18,'CONTRACTED OPERATIONAL PARTNER',11,active)
    flag(a,'cw_sr_op_assigned_flag',48,651,'cw_sr_op_view_country',active+' '+cv('cw_sr_op_view_country','>',0))
    icon('cw_sr_op_assigned_empty',48,651,'crew_empty_flag',active+' '+cv('cw_sr_op_view_country','=',0))
    text('cw_sr_op_assigned_name',148,652,386,42,'[CW_SR_OpCountry]',19,active)
    text('cw_sr_op_status',148,700,548,26,'[CW_SR_OpStatus]',13,active)
    allowed='OR = { '+' '.join('AND = { '+cv('cw_sr_selected','=',n)+f' cw_sr_p{n}_op_invite_allowed = yes'+' }' for n,p in enumerate(c['PROGRAMMES'],1) if eligible(p))+' }'
    button('cw_sr_op_invite',548,651,182,30,'Propose work package','cw_sr_op_invite = yes',active+' '+cv('cw_sr_op_view_country','=',0),allowed,size=12,tip='cw_sr_op_invite_tt')
    button('cw_sr_op_remove',548,690,182,26,'Restore national delivery','cw_sr_op_remove = yes',active+' '+cv('cw_sr_op_view_country','>',0)+' '+cv('cw_sr_view_state','!=',4),size=11)
    text('cw_sr_op_requirements_title',44,774,668,20,'PARTNER QUALIFICATION',12,active)
    text('cw_sr_op_requirements',44,806,668,60,'[CW_SR_OpRequirements]',14,active)
    flag(a,'cw_sr_op_operator_flag',796,408,'THIS',active,True)
    text('cw_sr_op_return_title',796,395,300,18,'NATIONAL SHARE OF AVAILABLE AWARDS',12,active)
    text('cw_sr_op_return',1104,422,90,43,'§H[?cw_sr_crew_host_percent|0]%§!',29,active)
    text('cw_sr_op_return_brief',796,464,392,59,'Operational partner: 10% of available awards.\nAstronaut shares are deducted separately.\nNational delivery retains all operational honours.',13,active)
    text('cw_sr_op_bill_label',796,542,392,18,'NATIONAL DEPARTURE APPROPRIATION',11,active)
    text('cw_sr_op_bill',796,571,392,29,'§H$[?cw_sr_crew_host_cost|3]bn§!',23,active)
    text('cw_sr_op_bill_brief',796,611,392,27,'[CW_SR_OpFinance]',12,active)
    text('cw_sr_op_training_title',796,675,392,20,'PAID INTERFACE QUALIFICATION',12,active)
    text('cw_sr_op_training',796,711,392,82,'[?cw_sr_op_view_required|0] paid weeks · $[?cw_sr_op_view_weekly_m|2]m/week\nPartner flight allocation: $[?cw_sr_op_view_contribution|3]bn\n[CW_SR_OpFee]',14,active)
    text('cw_sr_op_terms',796,812,392,51,'Flight support is funded at departure.\nGovernment approval · Two work orders per country',12,active)
    text('cw_sr_op_unavailable',24,390,1170,52,'Support another country through funded instruments, tracking, mission operations or launch services.\nSelect a flight programme in the Orbital Atlas to propose a work package of our own.',16,dashboard)
    text('cw_sr_op_outbound_heading',24,876,1170,18,'OUR INTERNATIONAL COMMITMENTS · SEPARATE FROM ASTRONAUT TRAINING',11,active)
    for w in ORDERS:
        x=24+(w-1)*604
        flag(a,f'cw_sr_op_work{w}_flag',x+16,920,order(w,'host'),active+' '+cv(order(w,'status'),'>',0),True)
        text(f'cw_sr_op_work{w}_text',x+72,911,480,74,f'[CW_SR_OpWork{w}]',13,active)
        button(f'cw_sr_op_work{w}_withdraw',x+394,979,166,24,'Withdraw our work order',f'cw_sr_op_withdraw{w} = yes',active+' OR = { '+cv(order(w,'status'),'=',1)+' '+cv(order(w,'status'),'=',2)+' }',size=11)
        occupied=dashboard+' '+cv(order(w,'status'),'>',0);empty=dashboard+' '+cv(order(w,'status'),'=',0)
        flag(a,f'cw_sr_op_work{w}_large_flag',x+24,494,order(w,'host'),occupied)
        text(f'cw_sr_op_work{w}_label',x+124,488,410,19,f'WORK ORDER 0{w} · MISSION OPERATOR',11,dashboard)
        text(f'cw_sr_op_work{w}_host',x+124,520,410,48,f'[?{order(w,"host")}.GetName]',21,occupied)
        text(f'cw_sr_op_work{w}_large_role',x+24,594,530,30,f'[CW_SR_OpWorkRole{w}]',19,occupied)
        text(f'cw_sr_op_work{w}_large_programme',x+24,642,530,68,f'[CW_SR_OpWorkProgramme{w}]',17,occupied)
        text(f'cw_sr_op_work{w}_large_status',x+24,730,530,44,f'[CW_SR_OpWorkStatus{w}]',15,occupied)
        text(f'cw_sr_op_work{w}_large_terms',x+24,798,530,58,f'[CW_SR_OpWorkTerms{w}]',13,occupied)
        button(f'cw_sr_op_work{w}_large_withdraw',x+24,910,530,34,'Withdraw this work order',f'cw_sr_op_withdraw{w} = yes',occupied+' OR = { '+cv(order(w,'status'),'=',1)+' '+cv(order(w,'status'),'=',2)+' }',size=13)
        icon(f'cw_sr_op_work{w}_empty_flag',x+24,494,'crew_empty_flag',empty)
        text(f'cw_sr_op_work{w}_large_empty',x+124,520,410,48,'Available work order',21,empty)
        text(f'cw_sr_op_work{w}_large_empty_brief',x+24,642,530,108,'An invitation from another government reserves this place. Review the mission, required qualification and financial terms before accepting.',17,empty)
    text('cw_sr_op_orders_terms',24,988,1170,27,'Two operational commitments per country · Astronaut assignments remain separate · Flight allocations are paid at departure',13,dashboard)



def graphics(texture):
    im=Image.new('RGBA',(1240,760),'#111d25');d=ImageDraw.Draw(im)
    for x,y,w,h in [(24,610,728,126),(24,758,728,110),(776,380,440,268),(776,660,440,208),(24,902,580,108),(628,902,588,108)]:
        y-=264
        d.rounded_rectangle((x,y,x+w-1,y+h-1),radius=3,fill='#1b2a33',outline='#3c515a')
        d.rectangle((x+1,y+9,x+3,y+h-10),fill='#c4ac76' if x==776 else '#83afb7')
    texture('operations',im)
    im=Image.new('RGBA',(1240,760),'#111d25');d=ImageDraw.Draw(im)
    for x,w in [(24,580),(628,588)]:
        y=466-264
        d.rounded_rectangle((x,y,x+w-1,970-264),radius=3,fill='#1b2a33',outline='#3c515a')
        d.rectangle((x+1,y+10,x+3,960-264),fill='#83afb7')
        d.line((x+24,576-264,x+w-24,576-264),fill='#3c515a')
    texture('operations_orders',im)
