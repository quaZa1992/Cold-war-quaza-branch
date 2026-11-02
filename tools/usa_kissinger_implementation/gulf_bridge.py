# IMPERIA COLD WAR — One continuing northern-Iraq authority behind legacy Gulf IDs.
from .shared import *
import re
import sys
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field

def replace_roots(text,replacements):
    edits=[]
    for n in nodes(text):
        if n.key in replacements:edits.append((n.start,n.end,b(n.key,replacements.pop(n.key))))
    assert not replacements,('Missing owned Gulf helper',replacements.keys())
    for start,end,value in sorted(edits,reverse=True):text=text[:start]+value+text[end:]
    return text

def patch_legacy_focus(text):
    roots=nodes(text);tree=next((n for n in roots if n.key=='focus_tree'),None)
    candidates=tree.children() if tree else roots
    arm=next((n for n in candidates if n.key=='focus' and field(n.children(),'id')=='COLDWAR_USA_gulf_arm_front'),None)
    if not arm:return text
    reward=next(n for n in arm.children() if n.key=='completion_reward')
    body=P+'legacy_irq_preview = yes\n'+b('hidden_effect','set_country_flag = COLDWAR_USA_gulf_programme_arm_front\n'+P+'legacy_irq_start = yes\n'+guard(noflag('legacy_gulf_paid'),setflag('legacy_gulf_pending')))
    return text[:reward.start]+b('completion_reward',body)+text[reward.end:]

def patch_outputs(source):
    result=dict(source)
    path='common/scripted_effects/COLDWAR_USA_gulf_effects.txt';text=result[path]
    original={n.key:text[n.start:n.end] for n in nodes(text)}
    def body(key):
        raw=original[key];return raw[raw.index('{')+1:raw.rfind('}')].strip()
    replacement={
      'COLDWAR_USA_gulf_initial_underground':P+'legacy_irq_start = yes',
      'COLDWAR_USA_gulf_usa_daily':P+'migrate_irq = yes\n'+body('COLDWAR_USA_gulf_usa_daily'),
      'COLDWAR_USA_gulf_irq_daily':'COLDWAR_USA_gulf_observe_kuwait_crisis = yes\n'+P+'migrate_irq = yes\n'+guard(noflag('tracked'),body('COLDWAR_USA_gulf_irq_daily')),
      'COLDWAR_USA_gulf_start_security':'USA = { '+P+'init_irq = yes }\n'+P+'refresh_host = yes\n'+P+'irq_security = yes',
      'COLDWAR_USA_gulf_start_major_operation':'USA = { '+P+'init_irq = yes }\n'+P+'refresh_host = yes\n'+P+'irq_security = yes'}
    result[path]=replace_roots(text,replacement)
    # The old Gulf military/relief/settlement paths remain. Only the replaced
    # underground invoices and 30-day security packages leave the old menu.
    retired={
      'COLDWAR_USA_gulf_arms_offer','COLDWAR_USA_gulf_renew_arms','COLDWAR_USA_gulf_underground','COLDWAR_USA_gulf_sustain_underground',
      'COLDWAR_USA_gulf_end_support','COLDWAR_USA_gulf_writeoff_cache','COLDWAR_USA_gulf_cache_offer_KUR','COLDWAR_USA_gulf_cache_offer_PUK',
      'COLDWAR_IRQ_northern_security','COLDWAR_IRQ_northern_major_operation','COLDWAR_IRQ_northern_withdraw_security',
      *('COLDWAR_USA_gulf_expand_'+str(s) for s in HOSTS['irq']['states'])}
    path='common/decisions/COLDWAR_USA_gulf_decisions.txt';text=result[path];edits=[]
    for cat in nodes(text):
        for n in cat.children():
            if n.key not in retired:continue
            vis=next(x for x in n.children() if x.key=='visible')
            old=text[vis.start:vis.end];oldbody=old[old.index('{')+1:old.rfind('}')]
            edits.append((vis.start,vis.end,b('visible',oldbody+'\nNOT = { IRQ = { '+flag('tracked')+' } }')))
    for start,end,value in sorted(edits,reverse=True):text=text[:start]+value+text[end:]
    result[path]=text
    # A popup queued in an older save must not execute its retired invoice or
    # equipment grant after migration. Keep the native Decline/Review options.
    path='events/COLDWAR_USA_gulf_events.txt';text=result[path];edits=[]
    for ev in nodes(text):
        if ev.key!='country_event' or field(ev.children(),'id') not in {'COLDWAR_USA_gulf_events.21','COLDWAR_USA_gulf_events.22','COLDWAR_USA_gulf_events.23'}:continue
        for opt in (n for n in ev.children() if n.key=='option'):
            actions=[n for n in opt.children() if n.key not in {'name','trigger','ai_chance'}]
            if not actions:continue
            if not any(n.key in {'if','modify_treasury_effect','add_equipment_to_stockpile','add_timed_idea'} for n in actions):continue
            first,last=actions[0].start,actions[-1].end
            edits.append((first,last,guard('NOT = { IRQ = { '+flag('tracked')+' } }',text[first:last])))
    for start,end,value in sorted(edits,reverse=True):text=text[:start]+value+text[end:]
    result[path]=text
    fragment='tools/iraq_1970/staged/USA_GULF_FOCUS_FRAGMENT.txt'
    result[fragment]=patch_legacy_focus(result[fragment])
    # No Gulf helper can restore the retired 90-day aid budget after migration.
    # Relief and air-protection budgets still retain their own approved terms.
    return result
