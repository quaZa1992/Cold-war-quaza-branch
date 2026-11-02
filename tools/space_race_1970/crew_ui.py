# IMPERIA COLD WAR — Native country flags and an institutional flight manifest.
"""Presentation only. Native GetFlag follows the country's current identity.

The masked flag donors are the same as MD's EU and international-system views;
the flags themselves are never copied into a generated texture atlas.
"""
from PIL import Image,ImageDraw
import math


def flag(a,name,x,y,target,condition='',small=False):
    sprite='GFX_cw_sr_flag_'+('small' if small else 'medium')
    if not any(f'name = "{sprite}"' in s for s in a['sprites']):
        overlay='flag_overlay_small.dds' if small else 'flag_overlay.dds'
        mask='shield_small_mask.tga' if small else 'shield_medium_mask.tga'
        a['sprites'].append(f'maskedShieldType = {{ name = "{sprite}" textureFile1 = "gfx/interface/{overlay}" textureFile2 = "gfx/interface/{mask}" effectFile = "gfx/FX/maskedflag.lua" }}\n')
    a['widgets'].append(f'iconType = {{ name = "{name}" position = {{ x = {x} y = {y} }} spriteType = "{sprite}" alwaysTransparent = yes }}\n')
    a['properties'].append(f'{name} = {{ image = "[?{target}.GetFlag]" }}\n')
    if condition:a['triggers'].append(f'{name}_visible = {{ {condition} }}\n')


# IMPERIA COLD WAR — International operational cooperation.
def controls(c,a):
    text,button,icon,tab=(a[k] for k in ['text','button','icon','tab'])
    cv,sv=(c[k] for k in ['cv','sv'])
    from crew import slots
    available=cv('cw_sr_crew_available','=',1);crew=tab(9)
    assignment=tab(2)+' '+cv('cw_sr_crew_status','>',0)
    flag(a,'cw_sr_crew_our_flag',440,909,'cw_sr_crew_host',assignment,True)
    text('cw_sr_crew_our_delegation',496,903,704,65,'OUR ASTRONAUT DELEGATION · [?cw_sr_crew_host.GetName]\nTraining credited: [?cw_sr_crew_weeks|0]/26 weeks · $2.00m/week',13,assignment)
    button('cw_sr_crew_our_withdraw',440,976,760,28,'Withdraw our astronaut delegation','cw_sr_crew_withdraw = yes',assignment,'OR = { '+cv('cw_sr_crew_status','=',1)+' '+cv('cw_sr_crew_status','=',2)+' }',size=12)
    button('cw_sr_control_crew',354,523,256,25,'Astronaut crew  >',sv('cw_sr_tab',9)+'clr_country_flag = cw_sr_partner_catalogue_cached\n',tab(8)+' '+available,size=12)
    icon('cw_sr_crew_background',0,238,'crew_manifest',crew)
    text('cw_sr_crew_heading',24,252,850,23,'FLIGHT OPERATIONS / CREW MANIFEST',13,crew)
    button('cw_sr_crew_back',960,249,250,28,'< Mission Control',sv('cw_sr_tab',8),crew,size=12)
    text('cw_sr_crew_mission',24,292,1170,54,'[CW_SR_Selected_name]',23,crew)
    flag(a,'cw_sr_crew_operator_flag',48,386,'THIS',crew)
    text('cw_sr_crew_operator_label',148,372,490,18,'MISSION OPERATOR · COMMAND AUTHORITY',11,crew)
    text('cw_sr_crew_commander',148,397,480,29,'[ROOT.GetName]',21,crew)
    text('cw_sr_crew_national',148,436,540,22,'National crew: [?cw_sr_crew_host_seats|0] / [?cw_sr_crew_total|0] · Commander included',13,crew)
    # The entire country card advances the selection; the transparent flag and
    # name retain the same click target as its explicit next-country affordance.
    # IMPERIA COLD WAR — Explicit player-only discovery, including empty SP lobbies.
    button('cw_sr_crew_partner',24,484,728,94,'','cw_sr_crew_candidate_next = yes',crew,cv('cw_sr_view_state','!=',4),size=13,tip='cw_sr_partner_selector_tt')
    flag(a,'cw_sr_crew_candidate_flag',48,505,'cw_sr_crew_candidate',crew+' '+cv('cw_sr_crew_candidate','>',0))
    icon('cw_sr_crew_candidate_empty',48,505,'crew_empty_flag',crew+' '+cv('cw_sr_crew_candidate','=',0))
    text('cw_sr_crew_partner_label',148,499,380,18,'PARTNER GOVERNMENT · [?cw_sr_partner_count|0] AVAILABLE',11,crew)
    text('cw_sr_crew_partner_name',148,526,390,47,'[CW_SR_CrewCandidate]',19,crew)
    text('cw_sr_crew_partner_next',556,522,175,24,'[CW_SR_PartnerCycle]',14,crew)
    text('cw_sr_crew_partner_scope',24,579,728,15,'Only player-controlled countries at peace can receive invitations.',11,crew)
    for s in [1,2]:
        visible=crew+' '+cv('cw_sr_crew_total','>',s);y=594+(s-1)*144
        flag(a,f'cw_sr_crew_guest{s}_flag',48,y+40,f'cw_sr_crew_flag_guest{s}',visible)
        text(f'cw_sr_crew_guest{s}_heading',148,y+18,380,18,f'RESEARCH ASTRONAUT / PLACE 0{s}',11,visible)
        text(f'cw_sr_crew_guest{s}_name',148,y+43,374,28,f'[CW_SR_CrewGuest{s}]',21,visible)
        icon(f'cw_sr_crew_guest{s}_badge',142,y+78,'crew_badge',visible)
        a['properties'].append(f'cw_sr_crew_guest{s}_badge = {{ frame = cw_sr_crew_badge{s} }}\n')
        text(f'cw_sr_crew_guest{s}_state',154,y+84,356,28,f'[CW_SR_CrewStatus{s}]',12,visible)
        enabled='OR = { '+' '.join('AND = { '+cv('cw_sr_selected','=',n)+f' cw_sr_p{n}_crew_invite{s}_allowed = yes'+' }' for n,p in enumerate(c['PROGRAMMES'],1) if s in slots(p))+' }'
        button(f'cw_sr_crew_guest{s}_choose',548,y+38,182,30,'Invite selected country',sv('cw_sr_crew_edit_slot',s)+'cw_sr_crew_invite = yes',visible+' '+cv(f'cw_sr_crew_view_guest{s}','=',0),enabled,size=12)
        button(f'cw_sr_crew_guest{s}_clear',548,y+80,182,26,'Restore national crew',sv('cw_sr_crew_edit_slot',s)+'cw_sr_crew_remove = yes',visible+' '+cv(f'cw_sr_crew_view_guest{s}','>',0)+' '+cv('cw_sr_view_state','!=',4),cv('cw_sr_view_state','!=',4),size=12)
        text(f'cw_sr_crew_guest{s}_share',548,y+17,182,18,'Guest award share: 20%',11,visible+' '+cv(f'cw_sr_crew_view_guest{s}','>',0))
    limited=crew+' '+cv('cw_sr_crew_total','=',2)
    icon('cw_sr_crew_capacity_symbol',48,776,'crew_empty_flag',limited)
    text('cw_sr_crew_capacity_title',148,758,560,20,'CREW CAPACITY',12,limited)
    text('cw_sr_crew_capacity_brief',148,791,560,51,'Two-seat spacecraft\nCommander and one research astronaut place.',16,limited)
    # Two short briefs replace the previous dense full-width rules paragraph.
    text('cw_sr_crew_training_title',44,903,332,18,'JOINT TRAINING',12,crew)
    text('cw_sr_crew_training_terms',44,931,332,65,'Initial course: 26 paid weeks\nQualified refresher: 6 paid weeks\nAppropriation: $2.00m / week',13,crew)
    text('cw_sr_crew_terms_title',400,903,328,18,'FLIGHT AGREEMENT',12,crew)
    text('cw_sr_crew_terms',400,931,328,65,'Guest contribution: 15% of flight bill\nGuest return: 20% of available awards\nGovernment approval required',13,crew)
    text('cw_sr_crew_share_title',796,374,392,24,'EXPEDITION RETURN',15,crew)
    flag(a,'cw_sr_crew_share_flag',796,410,'THIS',crew,True)
    text('cw_sr_crew_share_country',850,408,240,47,'[ROOT.GetName]',16,crew)
    text('cw_sr_crew_share',1100,402,94,43,'§H[?cw_sr_crew_host_percent|0]%§!',29,crew)
    icon('cw_sr_crew_share_bar',796,461,'crew_share_bar',crew)
    a['properties'].append('cw_sr_crew_share_bar = { frame = cw_sr_crew_share_frame }\n')
    text('cw_sr_crew_share_key',796,480,392,19,'§HNational [?cw_sr_crew_host_percent|0]%§!     §TPartners [?cw_sr_crew_partner_percent|0]%§!',12,crew)
    text('cw_sr_crew_rewards_heading',796,520,392,20,'FIRST ACCEPTED PROGRAMME',12,crew)
    for i,(label,key) in enumerate([('Space prestige','prestige'),('Research data','science'),('Political power','pp')]):
        text('cw_sr_crew_reward_label_'+key,796,556+i*34,288,23,label,14,crew)
        text('cw_sr_crew_reward_'+key,1094,552+i*34,100,26,'§G+[?cw_sr_crew_host_'+key+'|2]§!',17,crew)
    text('cw_sr_crew_research',796,672,392,50,'[CW_SR_CrewResearchReward]',14,crew)
    text('cw_sr_crew_reward_state',796,740,392,64,'[CW_SR_CrewAwardState]',13,crew)
    text('cw_sr_crew_cost_label',796,820,240,18,'NATIONAL DEPARTURE BILL',11,crew)
    text('cw_sr_crew_cost',1040,814,154,29,'§H$[?cw_sr_crew_host_cost|3]bn§!',21,crew)
    text('cw_sr_crew_contributions',796,848,392,18,'[CW_SR_CombinedFinance]',12,crew)
    text('cw_sr_crew_tradeoff_title',796,903,392,18,'NATIONAL OR JOINT EXPEDITION',12,crew)
    text('cw_sr_crew_tradeoff',796,931,392,65,'National delivery retains all honours.\nPartners share costs and available awards.\nAssignments are fixed at departure.',13,crew)


# IMPERIA COLD WAR — International operational cooperation.
def graphics(texture):
    """Original code-native chrome. No country flag or photo is baked in."""
    im=Image.new('RGBA',(1240,786),'#111d25');d=ImageDraw.Draw(im)
    for y in range(116):
        shade=22-int(y/14);d.line((0,y,1239,y),fill=(shade,shade+12,shade+19,255))
    def card(x,y,w,h,accent='#576e76'):
        y-=238
        d.rounded_rectangle((x,y,x+w-1,y+h-1),radius=3,fill='#1b2a33',outline='#3c515a')
        d.line((x+2,y+2,x+w-3,y+2),fill='#2e424c')
        d.rectangle((x+1,y+9,x+3,y+h-10),fill=accent)
    card(24,354,728,116,'#c4ac76');card(24,594,728,130,'#83afb7');card(24,738,728,130,'#83afb7')
    card(24,886,728,116);card(776,354,440,516,'#c4ac76');card(776,886,440,116)
    d.line((796,572,1196,572),fill='#3c515a') # local y = absolute 810
    # A small engraved helmet in the operator card supplies a visual role cue.
    hx,hy=694,158
    d.arc((hx-17,hy-10,hx+17,hy+23),180,360,fill='#728e94',width=2)
    d.rounded_rectangle((hx-15,hy+1,hx+15,hy+20),radius=7,outline='#91a7a9',width=2)
    d.line((hx-18,hy+23,hx+18,hy+23),fill='#c4ac76',width=2)
    d.line((hx-12,hy+27,hx+12,hy+27),fill='#728e94')
    texture('crew_manifest',im)
    badge=Image.new('RGBA',(380*5,30),(0,0,0,0));d=ImageDraw.Draw(badge)
    for i,(bg,line) in enumerate([('#24343c','#637c83'),('#3b3529','#c3ac77'),('#203a45','#85b4be'),('#263b32','#91b295'),('#2b333e','#8798a8')]):
        d.rounded_rectangle((i*380,0,(i+1)*380-1,29),radius=3,fill=bg)
        d.rectangle((i*380,5,i*380+2,24),fill=line)
    texture('crew_badge',badge,5)
    bar=Image.new('RGBA',(392*6,8),'#253b46');d=ImageDraw.Draw(bar)
    for i,fraction in enumerate([1,.9,.8,.7,.6,.5]):
        start=i*392;boundary=start+round(392*fraction)
        d.rectangle((start,0,boundary-1,7),fill='#c4ac76')
        if fraction<1:
            d.rectangle((boundary,0,start+391,7),fill='#85b4be');d.line((boundary,0,boundary,7),fill='#15232b')
        if fraction==.6:d.line((start+round(392*.8),0,start+round(392*.8),7),fill='#15232b')
    texture('crew_share_bar',bar,6)
    empty=Image.new('RGBA',(82,52),'#14222b');d=ImageDraw.Draw(empty)
    d.rectangle((0,0,81,51),outline='#506b75')
    for angle in range(0,360,90):
        a=math.radians(angle);d.line((41+math.cos(a)*13,26+math.sin(a)*13,41+math.cos(a)*19,26+math.sin(a)*19),fill='#77919a')
    d.ellipse((27,12,55,40),outline='#77919a');d.ellipse((38,23,44,29),fill='#c4ac76')
    texture('crew_empty_flag',empty)
