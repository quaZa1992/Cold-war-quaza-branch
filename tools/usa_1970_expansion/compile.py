# IMPERIA COLD WAR — USA and Soviet political leadership integration.
# IMPERIA COLD WAR — Canonical USA 1970 expansion integration.
"""Compile the approved USA expansion and bounded native integrations.

The historical USA tree generator is absent. A one-time, hashed source record
preserves that authored tree; the two content modules own only their files.
Shared MD files receive small marked integrations against their current text.
"""
from __future__ import annotations
from collections import defaultdict
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import textwrap

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
DOC=ROOT/'docs/design/usa_1970_expansion_20261024'
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field
from usa_building_capacity import capacity_trigger, capacity_localisation
import focus_dates
import gulf_revision
from naval_adaptation_1970 import naval_adapter
from usa_kissinger_implementation import compile as kissinger

MARKER='# IMPERIA COLD WAR — USA 1970 national programmes and negotiated partnerships.\n'
APPROVED_SHA='f524a00e9ab934872d748994b5de1ac89608a791de6cf6b28b0d7c55b142cfa8'
BASELINE_SHA='479d4979b1b7574ac8f58e2943505ddc432de1e563429c837e276d0e585c8da8'
TREE='common/national_focus/USA_1970.txt'
LOCALE='localisation/english/USA_1970_focus_l_english.yml'
OWNED_SOURCE=[TREE,LOCALE,'tools/usa_1970_quality/narrative.json',
    'common/scripted_effects/USA_1970_scripted_effects.txt',
    'events/USA_1970_events.txt','events/USA_1970_nixon_diplomacy_events.txt',
    'common/scripted_effects/USA_1970_nixon_diplomacy_effects.txt']
RETIRED_SENDERS={
    'USA_1970_send_atlantic_bargain_offers','USA_1970_send_triangular_diplomacy_offers',
    'USA_1970_send_middle_east_trade_offers','USA_1970_send_israel_security_offer',
    'USA_1970_send_broker_offers','USA_1970_send_maritime_basing_offers',
    'USA_1970_send_north_american_trade_offers','USA_1970_send_globalization_offers'}

def digest(data):return hashlib.sha256(data).hexdigest()
def kissinger_manifest():
    return dict(new_focuses=41,regional_campaigns=['IRQ','PER','TUR','SYR'],standing_focus_offers=10,
        canonical_source='tools/usa_kissinger_implementation/compile.py',approved_sha256=kissinger.APPROVED_SHA,
        gulf_bridge='tools/usa_kissinger_implementation/gulf_bridge.py',
        owned_outputs=sorted(kissinger.outputs()),
        documentation='tools/usa_kissinger_implementation/README.md')
def read_json(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def dec(value):return format(Decimal(str(value)).normalize(),'f')
def indent(s,n=1):return textwrap.indent(s.strip(),'\t'*n)
def block(key,body):return key+' = {\n'+indent(body)+'\n}'
def pretty_script(text):
    rows=nodes(text)
    def shape(items):return [(n.key,n.op,shape(n.children()) if isinstance(n.value,list) else n.value) for n in items]
    def render(n,depth=0):
        prefix='\t'*depth
        if n.key=='_bare':return prefix+str(n.value)
        lead=n.key+' '+n.op+' '
        if not isinstance(n.value,list):return prefix+lead+str(n.value)
        children=n.children()
        if not children:return prefix+lead+'{ }'
        if all(not isinstance(c.value,list) for c in children):
            flat=' '.join(str(c.value) if c.key=='_bare' else c.key+' '+c.op+' '+str(c.value) for c in children)
            if len(flat)<105:return prefix+lead+'{ '+flat+' }'
        return prefix+lead+'{\n'+'\n'.join(render(c,depth+1) for c in children)+'\n'+prefix+'}'
    result=text[:rows[0].start]+'\n\n'.join(render(n) for n in rows)+'\n'
    assert shape(rows)==shape(nodes(result)),'Formatting altered script semantics'
    return result
def write(relative,text,bom=False):
    # Current player revisions layer over, rather than rewrite, the immutable
    # approval catalogue. Real election-result chronology remains intact.
    revised=focus_dates.patch_outputs({relative:text})[relative]
    if revised!=text and relative.endswith('.txt'):
        revised=pretty_script(revised)
    from superpower_1970_leaders.integration import adapt as superpower_leadership
    text=superpower_leadership(relative,revised)
    path=ROOT/relative;path.parent.mkdir(parents=True,exist_ok=True)
    data=text.encode('utf-8-sig' if bom else 'utf-8')
    if path.exists() and path.read_bytes()==data:return False
    path.write_bytes(data);return True

def source_snapshot():
    path=HERE/'source_snapshot.json'
    if path.exists():return read_json(path)
    assert digest((ROOT/TREE).read_bytes())==BASELINE_SHA,'USA source changed before the approved integration baseline was captured'
    records={rel:dict(sha256=digest((ROOT/rel).read_bytes()),text=(ROOT/rel).read_text(encoding='utf-8-sig')) for rel in OWNED_SOURCE}
    data=dict(project='IMPERIA COLD WAR',purpose='Immutable pre-implementation authored USA source; attribution and original comments retained.',files=records)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data

def field_text(raw,key):
    root=nodes(raw)[0]
    n=next((n for n in root.children() if n.key==key),None)
    if not n:return ''
    return raw[n.start:n.end]

def field_body(raw,key):
    text=field_text(raw,key)
    return text[text.index('{')+1:text.rfind('}')].strip() if '{' in text else ''

def set_fields(raw,updates):
    root=nodes(raw)[0];edits=[];seen=set()
    for n in root.children():
        if n.key not in updates:continue
        value=updates[n.key]
        replacement='' if n.key in seen or value is None else value
        seen.add(n.key);edits.append((n.start,n.end,replacement))
    missing='\n'.join('\t\t'+v.replace('\n','\n\t\t') for k,v in updates.items() if k not in seen and v is not None)
    if missing:edits.append((root.end-1,root.end-1,'\n'+missing+'\n\t'))
    for a,b,new in sorted(edits,reverse=True):raw=raw[:a]+new+raw[b:]
    return raw

def remove_calls(text,keys):
    edits=[]
    def visit(rows):
        for n in rows:
            if n.key in keys:edits.append((n.start,n.end,''))
            else:visit(n.children())
    visit(nodes(text))
    for a,b,new in sorted(edits,reverse=True):text=text[:a]+new+text[b:]
    return text

def helper_delta(helper,amount):
    return f'set_temp_variable = {{ temp_change = {dec(amount)} }}\n{helper} = yes'

def load_specs():
    domestic=read_json(HERE/'domestic_focus_specs.json')
    diplomatic=read_json(HERE/'agreements/focus_specs.json')
    early=read_json(HERE/'early_cooperation/focus_specs.json')
    result={}
    for data in (domestic,diplomatic):
        items=data.get('focuses',data.get('focus_specs',data.get('nodes',[])))
        if isinstance(items,dict):items=[dict(id=k,**v) for k,v in items.items()]
        for n in items:
            assert n['id'] not in result,n['id'];result[n['id']]=n
    for fid,spec in early['focuses'].items():
        assert fid not in result,fid
        result[fid]=spec
    return result,domestic.get('hooks',{}),diplomatic.get('hooks',{}),early

def build_tree(snapshot,specs,proposal):
    original=snapshot['files'][TREE]['text']
    inv=read_json(DOC/'current_inventory.json');baseline={n['id']:n for n in inv['focuses']}
    elections=read_json(DOC/'implementation_support_elections.json')['nodes'];election_map={n['id']:n for n in elections}
    bld=read_json(DOC/'building_slot_repairs.json')
    bld_rows=bld['missing_slot_focuses']+bld.get('existing_slot_focuses_also_requiring_transaction_review',[])
    buildings={n['id']:n for n in bld_rows}
    # The dated audit retains the old proposed trigger strings as evidence.
    # Generate runtime predicates from current native building definitions.
    def capacities(group):
        return [block(str(group['state']),capacity_trigger(kind,int(amount)))
                for kind,amount in group['levels_by_type'].items()]
    proposed={n['id']:n for n in proposal['nodes']};rewire={n['focus']:n for n in proposal['rewiring']}
    effects={};triggers={};updates=[];receipts=[];party_bundles=[];report=[]

    root=next(n for n in nodes(original) if n.key=='focus_tree')
    for focus in root.children():
        if focus.key!='focus':continue
        fid=field(focus.children(),'id');raw=original[focus.start:focus.end]
        if str(fid).startswith(gulf_revision.PREFIX):
            # The Gulf owner supplies its complete live guards, consent and
            # counterplay. Generic wrappers must not revive its retired card
            # or retain obsolete availability inside a second transaction.
            report.append(dict(id=fid,reworked=True,owner='tools/iraq_1970/usa_module.py'))
            continue
        data=baseline[fid];changes={};extra=[];election=election_map.get(fid)
        if fid=='USA_1970_F4':extra.append('has_idea = NATO_member')
        if fid in specs:
            s=specs[fid]
            changes['completion_reward']=block('completion_reward',s['completion_reward'])
            if s.get('available'):extra.append(s['available'])
        elif float(data['cost'])!=0:
            reward=field_body(raw,'completion_reward')
            reward=remove_calls(reward,RETIRED_SENDERS)
            receipt='COLDWAR_USA_legacy_done_'+fid.removeprefix('USA_1970_')
            receipts.append((fid,receipt))
            conditions=['tag = USA','IMP_is_1970_scenario = yes',f'NOT = {{ has_country_flag = {receipt} }}']
            if fid=='USA_1970_F4':conditions.append('has_idea = NATO_member')
            # Availability is rechecked when executing, not only by the UI.
            availability=field_body(raw,'available')
            if availability:conditions.append(availability)
            if election and election.get('execution_gate'):conditions.append(election['execution_gate']+' = yes')
            if fid in buildings:
                asset=buildings[fid]
                for group in asset['state_groups']:
                    conditions.append(group['aggregate_owner_control'])
                    conditions.extend(capacities(group))
                # Keep every pre-existing slot command, add only missing ones.
                # Source offsets are refreshed after dispatcher removal.
                if asset['missing_slots']:
                    grants=list(re.finditer(r'\badd_building_construction\s*=\s*\{',reward))
                    for m in reversed(grants):
                        reward=reward[:m.start()]+'add_extra_state_shared_building_slots = 1\n'+reward[m.start():]
                extra.append('COLDWAR_USA_legacy_capacity_'+fid+' = yes')
                triggers['COLDWAR_USA_legacy_capacity_'+fid]='\n'.join(condition for group in asset['state_groups'] for condition in [group['aggregate_owner_control']]+capacities(group))
            if election and election['suspend_helper_bundle_on_party_loss']:
                # The earned national assets remain. Only this source's signed
                # discretionary helper contributions follow the current party.
                active='COLDWAR_USA_legacy_active_'+fid
                reward+='\nset_country_flag = '+active
                party_bundles.append((election,active,receipt))
            helper='COLDWAR_USA_legacy_complete_'+fid
            pending='COLDWAR_USA_legacy_pending_'+fid.removeprefix('USA_1970_')
            ready='COLDWAR_USA_legacy_ready_'+fid
            triggers[ready]='\n'.join(conditions)
            effects[helper]=block('if',block('limit','tag = USA\nIMP_is_1970_scenario = yes\nNOT = { has_country_flag = '+receipt+' }')+'\nset_country_flag = '+pending+'\n'+block('if',block('limit',ready+' = yes')+'\n'+reward+'\nset_country_flag = '+receipt+'\nclr_country_flag = '+pending))
            preview=remove_calls(reward,{'log','set_country_flag','clr_country_flag'})
            changes['completion_reward']=block('completion_reward',block('effect_tooltip',preview)+'\n'+block('hidden_effect',helper+' = yes'))
        if election and election.get('execution_gate'):extra.append(election['execution_gate']+' = yes')
        # Historical election windows still govern the automatic receipt, but
        # do not conceal its entire programme from later governments.
        allow=field_body(raw,'allow_branch')
        if allow:
            if election and election['classification']=='persistent_election_receipt':
                changes['bypass']=block('bypass',field_body(raw,'bypass')+'\n'+block('hidden_trigger',allow))
            else:extra.append(block('hidden_trigger',allow))
            changes['allow_branch']=None
        if fid in rewire:
            rw=rewire[fid]
            if 'prerequisites' in rw:changes['prerequisite']='\n'.join(block('prerequisite','\n'.join('focus = '+p for p in row)) for row in rw['prerequisites'])
            if rw.get('remove_exclusion'):changes['mutually_exclusive']=None
            if rw.get('add_exclusion'):changes['mutually_exclusive']=block('mutually_exclusive','\n'.join('focus = '+p for p in data['mutually_exclusive']+rw['add_exclusion']))
        if extra:
            available='' if specs.get(fid,{}).get('replace_legacy_available') else field_body(raw,'available')
            changes['available']=block('available','\n'.join([available]+extra))
        if float(data['cost'])!=0:changes['cancel_if_invalid']='cancel_if_invalid = yes'
        if changes:
            raw=set_fields(raw,changes)
            updates.append((focus.start,focus.end,raw))
        report.append(dict(id=fid,reworked=fid in specs,party=election.get('party') if election else None,buildings_guarded=fid in buildings and fid not in specs))

    text=original
    for a,b,new in sorted(updates,reverse=True):text=text[:a]+new+text[b:]
    additions=[]
    for n in proposal['nodes']:
        if n['id'] in baseline:continue
        s=specs[n['id']]
        available='hidden_trigger = { tag = USA IMP_is_1970_scenario = yes }\n'+s.get('available','')
        prereqs='\n'.join(block('prerequisite','\n'.join('focus = '+p for p in row)) for row in s.get('prerequisites',n['prerequisites']))
        exclusions=block('mutually_exclusive','\n'.join('focus = '+p for p in n['mutually_exclusive'])) if n['mutually_exclusive'] else ''
        kind=n['module'];filters=['FOCUS_FILTER_POLITICAL']
        if kind in ('Industry','Civil priorities','Energy','Election priorities','Americas'):filters=['FOCUS_FILTER_ECONOMY']
        if kind in ('Force structure','Army doctrine'):filters=['FOCUS_FILTER_ARMY']
        if kind=='Naval priorities':filters=['FOCUS_FILTER_NAVY']
        if 'offer' in n:filters=['FOCUS_FILTER_FOREIGN_POLICY']
        body=f"id = {n['id']}\nicon = {s.get('icon','diplomatic_treaty')}\nx = {n['xy'][0]}\ny = {n['xy'][1]}\ncost = {s.get('cost',dec(Decimal(n['days'])/7))}\n"
        body+='\n'.join(x for x in [prereqs,exclusions,block('available',available),'cancel_if_invalid = yes',block('search_filters',' '.join(filters)),block('completion_reward',s['completion_reward']),block('ai_will_do','factor = 3\nmodifier = { factor = 0 is_ai = yes ai_has_high_deficit = yes }')] if x)
        additions.append(block('focus',body))
    tree_node=next(n for n in nodes(text) if n.key=='focus_tree')
    text=text[:tree_node.end-1]+'\n\t# IMPERIA COLD WAR — Approved USA programme and recipient-controlled agreement expansion.\n'+indent('\n\n'.join(additions))+'\n'+text[tree_node.end-1:]
    first_tree=text.index('focus_tree =')
    text=MARKER+'# Canonical generator: tools/usa_1970_expansion/compile.py\n# Authored 229-focus baseline retained in tools/usa_1970_expansion/source_snapshot.json.\n# Earlier narrative overlay: tools/usa_1970_quality/apply.py; Gulf content: tools/iraq_1970/usa_module.py.\n\n'+text[first_tree:]
    text=re.sub(r'\n[\t ]*\n(?:[\t ]*\n)+','\n\n',text)
    quality_spec=importlib.util.spec_from_file_location('usa_quality_presentation',ROOT/'tools/usa_1970_quality/presentation.py')
    quality=importlib.util.module_from_spec(quality_spec);quality_spec.loader.exec_module(quality)
    text=quality.patch_usa(text)
    text=set_fields(text,{'reset_on_civilwar':'reset_on_civilwar = no','continuous_focus_position':'continuous_focus_position = { x = -3200 y = 1800 }'})
    text=pretty_script(text)
    text=pretty_script(gulf_revision.patch_tree(text))
    # Apply the calendar revision before inserting the marked naval block.
    # The writer's idempotent date pass must not reformat away its markers.
    text=pretty_script(focus_dates.patch_focus_tree(text))
    text=naval_adapter.integrate_tree('USA',text)
    text=kissinger.patch_tree(text)
    return text,effects,triggers,receipts,party_bundles,report

def lifecycle(effects,receipts,bundles,early):
    migration=[];sync=[]
    for fid,receipt in receipts:
        migration.append(block('if',block('limit','has_completed_focus = '+fid)+'\nset_country_flag = '+receipt))
    for item,active,receipt in bundles:
        deltas=item['party_bound_helper_deltas'];gate=item['execution_gate']+' = yes'
        enable='\n'.join(helper_delta(d['helper'],d['amount']) for d in deltas)+'\nset_country_flag = '+active
        disable='\n'.join(helper_delta(d['helper'],-Decimal(d['amount'])) for d in deltas)+'\nclr_country_flag = '+active
        # Existing saves contain these source deltas even if that party has
        # already left office. Mark the old contribution before reconciling it.
        migration.append(block('if',block('limit','has_completed_focus = '+item['id'])+'\nset_country_flag = '+active))
        sync.append(block('if',block('limit','has_country_flag = '+receipt)+'\n'+block('if',block('limit',gate+'\nNOT = { has_country_flag = '+active+' }')+'\n'+enable)+'\n'+block('else_if',block('limit','NOT = { '+gate+' }\nhas_country_flag = '+active)+'\n'+disable)))
    effects['COLDWAR_USA_legacy_reconcile_party_programmes']='\n'.join(sync)
    # These three roots now offer new, consent-owned programmes. Remove only
    # their exact old unbounded helper deltas on pre-revision saves. Historic
    # cash/PP/assets are never replayed or refunded; pending old packages paid
    # nothing and therefore have no modifier bundle to reverse.
    from source_audit import providers
    bridge=providers()
    original={n['id']:n for n in read_json(DOC/'current_inventory.json')['focuses']}
    reversals=[]
    for fid in early['legacy_replaced']:
        temp=None;undo=[]
        for command,_,value in original[fid]['completion_reward']:
            if command=='set_temp_variable' and value[0][0]=='temp_change':temp=Decimal(value[0][2])
            elif command in bridge:
                assert temp is not None,(fid,command)
                undo.append('add_to_variable = { '+bridge[command]['variable']+' = '+dec(-temp)+' }')
        suffix=fid.removeprefix('USA_1970_')
        paid='COLDWAR_USA_legacy_done_'+suffix
        pending='COLDWAR_USA_legacy_pending_'+suffix
        auth='COLDWAR_USA_early_alliances_authorised' if fid=='USA_1970_NIX_F3' else 'COLDWAR_USA_early_root_'+('israel' if fid=='USA_1970_F7' else 'trade')+'_authorised'
        gate=f'has_completed_focus = {fid}\nNOT = {{ has_country_flag = {auth} }}\nOR = {{ has_country_flag = {paid} NOT = {{ has_country_flag = {pending} }} }}'
        reversals.append(block('if',block('limit',gate)+'\n'+'\n'.join(undo)))
        reversals.append('clr_country_flag = '+pending)
    effects['COLDWAR_USA_early_legacy_bundle_migrate']=block('if',block('limit','tag = USA\nIMP_is_1970_scenario = yes\nNOT = { has_country_flag = COLDWAR_USA_early_legacy_bundles_migrated }')+'\n'+'\n'.join(reversals)+'\nset_country_flag = COLDWAR_USA_early_legacy_bundles_migrated\nforce_update_dynamic_modifier = yes')
    effects['COLDWAR_USA_expansion_initialize']=block('if',block('limit','tag = USA\nIMP_is_1970_scenario = yes\nhas_country_flag = USA_1970_systems_initialized')+'\nCOLDWAR_USA_gulf_recalculate_prorated_costs = yes\n'+block('if',block('limit','NOT = { has_country_flag = COLDWAR_USA_expansion_initialized }')+'\n'+ '\n'.join(migration)+'\nset_country_flag = COLDWAR_USA_expansion_initialized')+'\nCOLDWAR_USA_early_legacy_bundle_migrate = yes\nCOLDWAR_USA_dom_initialize = yes\nCOLDWAR_USA_early_initialize = yes\nCOLDWAR_USA_agreements_initialize = yes\nCOLDWAR_USA_legacy_reconcile_party_programmes = yes')
    effects['COLDWAR_USA_expansion_reconcile']='COLDWAR_USA_expansion_initialize = yes\nCOLDWAR_USA_dom_reconcile = yes\nCOLDWAR_USA_legacy_reconcile_party_programmes = yes\nCOLDWAR_USA_early_reconcile_all = yes\nCOLDWAR_USA_agreements_reconcile_all = yes'
    return effects

def insert_marked(text,marker,body,anchor,where='after'):
    start='# IMPERIA COLD WAR — '+marker+' BEGIN';end='# IMPERIA COLD WAR — '+marker+' END'
    text=re.sub(r'(?m)^[\t ]*'+re.escape(start)+r'.*?^[\t ]*'+re.escape(end)+r'\n?', '',text,flags=re.S)
    assert anchor in text,('Missing integration anchor',marker)
    value=start+'\n'+body.strip()+'\n'+end+'\n'
    pos=text.index(anchor)+(len(anchor) if where=='after' else 0)
    return text[:pos]+value+text[pos:]

def integrate_shared_files(snapshot):
    changed=[]
    rel='common/scripted_effects/00_money_system.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    income='\tCOLDWAR_USA_agreements_calculate_weekly_streams = yes\n\tadd_to_variable = { additional_income_rate = COLDWAR_USA_agreements_weekly_income }\n\tCOLDWAR_USA_early_calculate_weekly_streams = yes\n\tadd_to_variable = { additional_income_rate = COLDWAR_USA_early_weekly_income }'
    expense='\tCOLDWAR_USA_agreements_calculate_weekly_streams = yes\n\tadd_to_variable = { additional_expenses_rate = COLDWAR_USA_agreements_weekly_expense }\n\tCOLDWAR_USA_early_calculate_weekly_streams = yes\n\tadd_to_variable = { additional_expenses_rate = COLDWAR_USA_early_weekly_expense }\n\tCOLDWAR_USA_dom_add_expense_rate = yes'
    text=insert_marked(text,'USA signed weekly income',income,'calculate_additional_income_rate = {\n\tset_variable = { additional_income_rate = 0 }\n')
    text=insert_marked(text,'USA signed weekly expenses',expense,'\tadd_to_variable = { additional_expenses_rate = gw_dp_retention_weekly }\n')
    if not text.startswith('# IMPERIA COLD WAR'):text=MARKER+text
    if write(rel,text):changed.append(rel)
    # Authoritative native US subparty callback. This is outside every
    # successor branch and therefore also handles third parties and returns.
    rel='common/scripted_effects/USA_political_leaders.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    start='# IMPERIA COLD WAR — USA programme party synchronisation BEGIN';end='# IMPERIA COLD WAR — USA programme party synchronisation END'
    text=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n?','',text,flags=re.S)
    r=next(n for n in nodes(text) if n.key=='set_leader_USA')
    body=start+'\nif = { limit = { tag = USA IMP_is_1970_scenario = yes has_country_flag = USA_1970_systems_initialized } COLDWAR_USA_expansion_reconcile = yes }\n'+end+'\n'
    text=text[:r.end-1]+body+text[r.end-1:]
    if not text.startswith(MARKER):text=MARKER+text
    if write(rel,text):changed.append(rel)
    # Standard native admissions and departures are the real membership-change
    # transaction boundary. Only this country is offered/reconciled here; no
    # daily world membership scan or new designation is introduced.
    rel='common/scripted_effects/01_NATO_effects.txt'
    text=(ROOT/rel).read_text(encoding='utf-8-sig')
    for name in ('NATO_join','NATO_leave','NATO_major_non_nato_ally_join','NATO_major_non_nato_ally_leave'):
        start='# IMPERIA COLD WAR — USA readiness membership '+name+' BEGIN'
        end='# IMPERIA COLD WAR — USA readiness membership '+name+' END'
        text=re.sub(r'(?m)^[\t ]*'+re.escape(start)+r'.*?^[\t ]*'+re.escape(end)+r'\n?','',text,flags=re.S)
        fx=next(n for n in nodes(text) if n.key==name)
        hook='if = { limit = { IMP_is_1970_scenario = yes country_exists = USA } COLDWAR_USA_early_membership_changed = yes USA = { COLDWAR_USA_early_reconcile_all = yes COLDWAR_USA_agreements_reconcile_all = yes } }'
        snippet='\n\t'+start+'\n\t'+block('hidden_effect',hook).replace('\n','\n\t')+'\n\t'+end+'\n'
        text=text[:fx.end-1].rstrip()+snippet+text[fx.end-1:]
    notice='# IMPERIA COLD WAR — USA readiness offers integrated into native NATO and MNNA membership effects.\n'
    if not text.startswith(notice):text=notice+text
    if write(rel,text):changed.append(rel)
    # Some native events grant membership directly rather than calling the
    # standard admission effects. The actual idea callback covers those paths
    # without polling the world. Initialization guards avoid history reentry.
    for rel,idea in (('common/ideas/Factions.txt','NATO_member'),('common/ideas/united_states.txt','Major_Non_NATO_Ally')):
        text=(ROOT/rel).read_text(encoding='utf-8-sig')
        start='# IMPERIA COLD WAR — USA readiness direct membership '+idea+' BEGIN'
        end='# IMPERIA COLD WAR — USA readiness direct membership '+idea+' END'
        text=re.sub(r'(?m)^[\t ]*'+re.escape(start)+r'.*?^[\t ]*'+re.escape(end)+r'\n?','',text,flags=re.S)
        def descendants(items):
            for item in items:
                yield item
                yield from descendants(item.children())
        target=next(n for n in descendants(nodes(text)) if n.key==idea)
        callback=next((n for n in target.children() if n.key=='on_add'),None)
        hook='if = { limit = { country_exists = USA USA = { IMP_is_1970_scenario = yes has_country_flag = USA_1970_systems_initialized has_country_flag = COLDWAR_USA_expansion_initialized } } COLDWAR_USA_early_membership_changed = yes USA = { COLDWAR_USA_agreements_reconcile_all = yes } }'
        addition=start+'\n'+block('hidden_effect',hook)+'\n'+end+'\n'
        if callback:
            pos=callback.end-1
            addition=textwrap.indent(addition,'\t'*4)
            text=text[:pos].rstrip()+'\n'+addition+'\t'*3+text[pos:]
        else:
            # Include the whole added callback in the marker, making repeated
            # integration replace it without accumulating empty on_add blocks.
            pos=target.end-1
            addition=start+'\n'+block('on_add',block('hidden_effect',hook))+'\n'+end+'\n'
            addition=textwrap.indent(addition,'\t'*3)
            text=text[:pos].rstrip()+'\n'+addition+'\t'*2+text[pos:]
        notice='# IMPERIA COLD WAR — USA readiness offers integrated into native membership idea callbacks.\n'
        if not text.startswith(notice):text=notice+text
        if write(rel,text):changed.append(rel)
    return changed

def integrate_legacy_diplomacy(snapshot):
    changed=[]
    rel='common/scripted_effects/USA_1970_scripted_effects.txt';text=snapshot['files'][rel]['text']
    # Old general menus no longer dispatch material packages alongside the
    # individual approved focus offers. Keep logical aliases for save/event
    # compatibility, but make those obsolete dispatchers harmless.
    edits=[]
    for n in nodes(text):
        if n.key in RETIRED_SENDERS:edits.append((n.start,n.end,block(n.key,'# Replaced by concrete focus-owned recipient mandates.')))
    for a,b,new in sorted(edits,reverse=True):text=text[:a]+new+text[b:]
    # This call stays inside the original once-only fresh-start initializer.
    # Migration is deliberately scheduled after history initialization instead
    # of running from the reentrant leader/programme reconciliation callback.
    initializer=next(n for n in nodes(text) if n.key=='USA_1970_initialize_systems')
    def fiscal_nodes(rows):
        for node in rows:
            yield node
            yield from fiscal_nodes(node.children())
    fiscal=[n for n in fiscal_nodes(initializer.children()) if n.key=='set_variable' and field(n.children(),'corporate_tax_rate')=='48']
    assert len(fiscal)==1,'Exactly one legacy fresh-start corporate tax assignment'
    item=fiscal[0]
    text=text[:item.start]+'COLDWAR_USA_1970_economy_initialize = yes'+text[item.end:]
    text=MARKER+text if not text.startswith(MARKER) else text
    if write(rel,text):changed.append(rel)
    # The retained Nixon contacts remain genuine invitations. Their focus
    # tooltips now expose the actual recipient and sender option outcomes,
    # rather than a prose promise or an event title in place of the numbers.
    events=snapshot['files']['events/USA_1970_nixon_diplomacy_events.txt']['text']
    event_map={field(ev.children(),'id'):ev for ev in nodes(events) if ev.key=='country_event'}
    previews={}
    ignored={'name','ai_chance','trigger','country_event','log','set_country_flag','clr_country_flag'}
    def option_outcomes(number,tag):
        option=next(n for n in event_map['USA_1970_nixon_dip.'+str(number)].children() if n.key=='option')
        recipient=[];sender=[]
        for child in option.children():
            if child.key in ignored:continue
            raw=events[child.start:child.end]
            raw=remove_calls(raw,ignored)
            if child.key=='FROM':sender.append(raw[raw.index('{')+1:raw.rfind('}')])
            else:recipient.append(raw)
        def refs(value):
            return re.sub(r'\bROOT\b',tag,re.sub(r'\bPREV\b',tag,re.sub(r'\bFROM\b','USA',value)))
        return '\n'.join([block(tag,refs('\n'.join(recipient))),block('USA',refs('\n'.join(sender)))])
    channels={'china_backchannel':[(1,'CHI')],'salt_channel':[(2,'SOV')],'beijing_summit':[(3,'CHI')],'moscow_summit':[(4,'SOV')],'okinawa_reversion':[(5,'JAP')],'arvn_assistance':[(6,'SVN')],'vietnam_settlement_invitations':[(7,'VIE'),(8,'SVN')]}
    for key,pairs in channels.items():
        previews['COLDWAR_USA_legacy_preview_'+key]=block('effect_tooltip','custom_effect_tooltip = COLDWAR_USA_agreements_if_accept_tt\n'+'\n'.join(option_outcomes(num,tag) for num,tag in pairs))
    rel='common/scripted_effects/USA_1970_nixon_diplomacy_effects.txt';text=snapshot['files'][rel]['text'];edits=[]
    for n in nodes(text):
        for key in channels:
            if n.key=='USA_1970_nixon_send_'+key+'_offer' or n.key=='USA_1970_nixon_send_'+key:
                raw=text[n.start:n.end]
                raw=re.sub(r'custom_effect_tooltip\s*=\s*[^\s{}]+','COLDWAR_USA_legacy_preview_'+key+' = yes',raw,count=1)
                edits.append((n.start,n.end,raw))
    for a,b,new in sorted(edits,reverse=True):text=text[:a]+new+text[b:]
    if write(rel,MARKER+text):changed.append(rel)
    write('common/scripted_effects/COLDWAR_USA_1970_legacy_previews.txt',pretty_script(MARKER+'\n\n'.join(block(k,v) for k,v in previews.items())+'\n'))
    # Preserve the national funding decisions which follow the old diplomatic
    # channels. A real active new agreement is an alternative to an old save's
    # historical receipt; it is never faked as an already-paid old package.
    receipt_alternatives={
        'USA_1970_israel_package_completed': [('has_idea','COLDWAR_USA_agreements_israel_usa'),('has_idea','COLDWAR_USA_early_israel_usa')],
        'USA_1970_broker_partner_found': [('has_idea','COLDWAR_USA_agreements_rogers_usa')],
        'USA_1970_arab_compact_applied': [('has_idea','COLDWAR_USA_agreements_saudi_usa')],
        'USA_1970_middle_east_security_path': [('has_completed_focus','USA_1970_F7')]}
    for rel in ('common/decisions/USA_1970_policy_decisions.txt','common/decisions/categories/USA_1970_policy_decision_categories.txt','common/scripted_effects/USA_1970_policy_decision_effects.txt','common/scripted_triggers/USA_1970_policy_decision_triggers.txt'):
        text=(ROOT/rel).read_text(encoding='utf-8-sig');edits=[]
        def visit(items):
            for n in items:
                if n.key=='OR' and any(c.key=='has_country_flag' and c.value in receipt_alternatives for c in n.children()):
                    existing={(c.key,c.value) for c in n.children() if not isinstance(c.value,list)}
                    additions={pair for c in n.children() if c.key=='has_country_flag' for pair in receipt_alternatives.get(c.value,[])}-existing
                    if additions:
                        raw=text[n.start:n.end];pos=raw.rfind('}')
                        extra='\n# IMPERIA COLD WAR — Accepted partnership and focus continuity.\n'+'\n'.join(k+' = '+v for k,v in sorted(additions))+'\n'
                        edits.append((n.start,n.end,raw[:pos]+extra+raw[pos:]))
                    continue
                if n.key=='has_country_flag' and n.value in receipt_alternatives:
                    extra=' '.join(k+' = '+v for k,v in receipt_alternatives[n.value])
                    edits.append((n.start,n.end,'OR = { has_country_flag = '+n.value+' '+extra+' }'))
                else:visit(n.children())
        visit(nodes(text))
        for a,b,new in sorted(edits,reverse=True):text=text[:a]+new+text[b:]
        if edits:
            if not text.startswith(MARKER):text=MARKER+text
            if write(rel,text):changed.append(rel)
    # Previously queued general offers close without a payment. Their event
    # IDs/localisation stay valid for old saves. Historical Nixon channels
    # remain distinct diplomatic contacts, not a second industrial treaty.
    rel='events/USA_1970_events.txt';text=snapshot['files'][rel]['text'];edits=[]
    retired={'USA_1970.'+str(x) for x in (100,101,110,111,120,121,130,131,140,141,150,151,160,170,171)}
    for ev in nodes(text):
        if ev.key=='country_event' and field(ev.children(),'id')=='USA_1970.10':
            # The survival outcome retains the actual Nixon presidency. Ford's
            # resignation outcome and the crisis chronology remain unchanged.
            option=next(n for n in ev.children() if n.key=='option' and field(n.children(),'name')=='USA_1970.10.b')
            assert any(n.key=='create_country_leader' and field(n.children(),'name')=='"Richard Nixon"' for n in option.children())
            flag=next(n for n in option.children() if n.key=='clr_country_flag' and n.value=='USA_1970_nixon_presidency')
            edits.append((flag.start,flag.end,'set_country_flag = USA_1970_nixon_presidency'))
        if ev.key!='country_event' or field(ev.children(),'id') not in retired:continue
        fid=field(ev.children(),'id')
        new=block('country_event',f'id = {fid}\nhidden = yes\nis_triggered_only = yes\n'+block('immediate','set_country_flag = COLDWAR_USA_legacy_offer_closed'))
        edits.append((ev.start,ev.end,new))
    for a,b,new in sorted(edits,reverse=True):text=text[:a]+new+text[b:]
    if write(rel,MARKER+text):changed.append(rel)
    # Two legacy Bahrain country events used a wide news photograph. Reuse
    # the actual framed MD agreement photo; its source pixels stay untouched.
    rel='events/COLDWAR_USA_bahrain_base_events.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    text=text.replace('GFX_news_usa_nsa_bahrain','GFX_political_deal')
    if not text.startswith(MARKER):text=MARKER+text
    if write(rel,text):changed.append(rel)
    rel='common/scripted_effects/COLDWAR_USA_bahrain_base_effects.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    helper=next((n for n in nodes(text) if n.key=='COLDWAR_USA_request_bahrain_base'),None)
    if helper:
        raw=text[helper.start:helper.end]
        accept=block('effect_tooltip','custom_effect_tooltip = COLDWAR_USA_bahrain_base_accept_tt\nBHR = { USA = { transfer_state = 624 } }')
        refuse=block('effect_tooltip','custom_effect_tooltip = COLDWAR_USA_bahrain_base_refuse_tt\nUSA = { add_opinion_modifier = { target = BHR modifier = COLDWAR_USA_bahrain_base_refused_opinion } }')
        raw=block('COLDWAR_USA_request_bahrain_base',accept+'\n'+refuse+'\n'+block('hidden_effect',field_body(raw,'hidden_effect')))
        text=text[:helper.start]+raw+text[helper.end:]
        if not text.startswith(MARKER):text=MARKER+text
        if write(rel,pretty_script(text)):changed.append(rel)
    rel='common/scripted_triggers/COLDWAR_USA_bahrain_base_triggers.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig');edits=[]
    guard='NOT = { has_country_flag = COLDWAR_USA_agreements_bahrain_signed }\nNOT = { has_country_flag = COLDWAR_USA_agreements_bahrain_offer_open }'
    for n in nodes(text):
        if n.key not in ('COLDWAR_USA_bahrain_base_can_request','COLDWAR_USA_bahrain_base_can_accept'):continue
        raw=text[n.start:n.end]
        if 'COLDWAR_USA_agreements_bahrain_signed' in raw:continue
        extra=guard if n.key.endswith('can_request') else block('USA',guard)
        raw=raw[:raw.rfind('}')]+'\n'+extra+'\n}'
        edits.append((n.start,n.end,raw))
    for a,b,new in sorted(edits,reverse=True):text=text[:a]+new+text[b:]
    if not text.startswith(MARKER):text=MARKER+text
    if write(rel,pretty_script(text)):changed.append(rel)
    return changed

def legacy_enactments(snapshot,effects,receipts):
    inv={n['id']:n for n in read_json(DOC/'current_inventory.json')['focuses']}
    decisions=[];loc={}
    for fid,receipt in receipts:
        suffix=fid.removeprefix('USA_1970_');pending='COLDWAR_USA_legacy_pending_'+suffix
        ready='COLDWAR_USA_legacy_ready_'+fid;key='COLDWAR_USA_legacy_enact_'+suffix
        source=effects['COLDWAR_USA_legacy_complete_'+fid]
        # The same native prospective bundle is shown by the focus and the
        # narrowly visible recovery authorisation. Neither preview executes.
        focus=next(n for n in nodes(snapshot['files'][TREE]['text'])[0].children() if n.key=='focus' and field(n.children(),'id')==fid)
        raw=snapshot['files'][TREE]['text'][focus.start:focus.end]
        # The emitted helper itself owns the asset and fee transaction. For a
        # retry, a purely native tooltip shows the approved old reward with
        # its additional slot grants; lifecycle/receipt flags remain hidden.
        reward=field_body(raw,'completion_reward');reward=remove_calls(reward,RETIRED_SENDERS|{'log','set_country_flag','clr_country_flag'})
        if 'add_extra_state_shared_building_slots' not in reward:
            reward=re.sub(r'\badd_building_construction\s*=\s*\{','add_extra_state_shared_building_slots = 1\nadd_building_construction = {',reward)
        body='icon = GFX_decision_generic_political_discourse\ncost = 0\n'+block('visible','tag = USA\nIMP_is_1970_scenario = yes\nhas_country_flag = '+pending+'\nNOT = { has_country_flag = '+receipt+' }')+'\n'+block('available',ready+' = yes')+'\n'+block('complete_effect',block('effect_tooltip',reward)+'\n'+block('hidden_effect','COLDWAR_USA_legacy_complete_'+fid+' = yes'))+'\nai_will_do = { factor = 1 }'
        decisions.append(block(key,body));loc[key]='Enact '+inv[fid]['name'];loc[key+'_desc']='The national programme has been authorised. Its measures can take effect when the required political support and territorial conditions are in place.'
    cat='COLDWAR_USA_legacy_enactment_category';loc[cat]='National Programme Authorisations';loc[cat+'_desc']='Carry authorised national measures into effect as their political and territorial requirements are met.'
    pending_any='OR = { '+' '.join('has_country_flag = COLDWAR_USA_legacy_pending_'+fid.removeprefix('USA_1970_') for fid,_ in receipts)+' }'
    cattext=MARKER+block(cat,'icon = GFX_decision_category_usa_congress\n'+block('allowed','original_tag = USA')+'\n'+block('visible','tag = USA\nIMP_is_1970_scenario = yes\n'+pending_any))+'\n'
    write('common/decisions/categories/COLDWAR_USA_1970_expansion.txt',cattext)
    write('common/decisions/COLDWAR_USA_1970_expansion.txt',pretty_script(MARKER+block(cat,'\n\n'.join(decisions))+'\n'))
    ltext='l_english:\n'+MARKER+'\n'.join(' '+k+':0 '+json.dumps(v,ensure_ascii=False) for k,v in loc.items())+'\n'
    write('localisation/english/COLDWAR_USA_1970_expansion_l_english.yml',ltext,True)

def on_actions():
    return MARKER+block('on_actions',
        block('on_startup',block('effect','USA = { if = { limit = { tag = USA IMP_is_1970_scenario = yes } COLDWAR_USA_1970_economy_migrate = yes COLDWAR_USA_expansion_reconcile = yes } }'))+'\n'+
        block('on_daily_USA',block('effect','if = { limit = { tag = USA IMP_is_1970_scenario = yes } COLDWAR_USA_1970_economy_migrate = yes COLDWAR_USA_expansion_reconcile = yes }'))+'\n'+
        block('on_weekly_USA',block('effect','if = { limit = { tag = USA IMP_is_1970_scenario = yes } COLDWAR_USA_expansion_reconcile = yes }'))+'\n'+
        block('on_war_relation_added',block('effect','if = { limit = { country_exists = USA USA = { IMP_is_1970_scenario = yes has_country_flag = COLDWAR_USA_expansion_initialized } } USA = { COLDWAR_USA_early_reconcile_all = yes COLDWAR_USA_agreements_reconcile_all = yes } }'))
    )+'\n'

def main():
    approved=(DOC/'proposal.json').read_bytes();assert digest(approved)==APPROVED_SHA,'Approved proposal changed'
    snapshot=source_snapshot()
    if '--skip-content' not in sys.argv:
        for module in ('domestic.py','early_cooperation.py','agreements.py','economy.py'):
            subprocess.run([sys.executable,str(HERE/module)],cwd=ROOT,check=True)
    specs,dom_hooks,dip_hooks,early=load_specs();proposal=json.loads(approved)
    expected={n['id'] for n in proposal['nodes']}|set(early['focuses'])
    assert set(specs)==expected,('Missing/extra focus specs',set(specs)^expected)
    tree,effects,triggers,receipts,bundles,report=build_tree(snapshot,specs,proposal)
    effects=lifecycle(effects,receipts,bundles,early)
    triggers=focus_dates.patch_trigger_bodies(triggers)
    legacy_enactments(snapshot,effects,receipts)
    changed=[]
    if '--skip-content' not in sys.argv:
        changed+=gulf_revision.emit(write,pretty_script)
        for path,content in naval_adapter.runtime_outputs().items():
            if write(path,content,path.endswith('.yml')):changed.append(path)
    for rel,text,bom in [
        (TREE,tree,False),
        ('common/scripted_effects/COLDWAR_USA_1970_expansion.txt',pretty_script(MARKER+'\n\n'.join(block(k,v) for k,v in effects.items())+'\n'),False),
        ('common/scripted_triggers/COLDWAR_USA_1970_expansion.txt',pretty_script(MARKER+'\n\n'.join(block(k,v) for k,v in triggers.items())+'\n'),False),
        ('common/on_actions/COLDWAR_USA_1970_expansion.txt',on_actions(),False)]:
        if write(rel,text,bom):changed.append(rel)
    # The existing localisation provider remains authoritative for the 13
    # reworked IDs. Updating the original overlay prevents later regression.
    loc=snapshot['files'][LOCALE]['text'];narrative=json.loads(snapshot['files']['tools/usa_1970_quality/narrative.json']['text'])
    for n in proposal['nodes']:
        if not n.get('replaces'):continue
        s=specs[n['id']]
        for key,value in [(n['id'],s['name']),(n['id']+'_desc',s['description'])]:
            line=' '+key+':0 '+json.dumps(value,ensure_ascii=False)
            pattern=r'(?m)^\s*'+re.escape(key)+r':\d*\s*".*"\s*$'
            assert re.search(pattern,loc),key;loc=re.sub(pattern,lambda m:line,loc,count=1)
        if n['id'] in narrative:narrative[n['id']]=s['description']
    for fid,s in early['focuses'].items():
        for key,value in ((fid,s['name']),(fid+'_desc',s['description'])):
            pattern=r'(?m)^\s*'+re.escape(key)+r':\d*\s*".*"\s*$'
            assert re.search(pattern,loc),key
            loc=re.sub(pattern,lambda m:' '+key+':0 '+json.dumps(value,ensure_ascii=False),loc,count=1)
        narrative[fid]=s['description']
    # Older inherited captions receive the same bounded native-width cleanup.
    # Only their short map label changes; their full description is preserved.
    captions=read_json(HERE/'focus_titles.json')['titles']
    for key,value in captions.items():
        pattern=r'(?m)^\s*'+re.escape(key)+r':\d*\s*".*"\s*$'
        if re.search(pattern,loc):loc=re.sub(pattern,lambda m:' '+key+':0 '+json.dumps(value,ensure_ascii=False),loc,count=1)
    if not loc.splitlines()[1].startswith('# IMPERIA COLD WAR'):
        loc=loc.replace('l_english:\n','l_english:\n'+MARKER,1)
    if write(LOCALE,loc,True):changed.append(LOCALE)
    if write('tools/usa_1970_quality/narrative.json',json.dumps(dict(project='IMPERIA COLD WAR',descriptions=narrative),ensure_ascii=False,indent=2)+'\n'):changed.append('tools/usa_1970_quality/narrative.json')
    changed+=integrate_shared_files(snapshot)
    changed+=integrate_legacy_diplomacy(snapshot)
    changed+=kissinger.emit_runtime()
    changed+=kissinger.integrate_money()
    installed_count=sum(n.key=='focus' for n in next(n for n in nodes(tree) if n.key=='focus_tree').children())
    manifest=dict(project='IMPERIA COLD WAR',approved_sha256=APPROVED_SHA,focuses=installed_count,naval_adaptation_focuses=20,programme_nodes=len(specs),offers=29,bilateral_contract_families=30,base_expansion_offers=19,kissinger=kissinger_manifest(),baseline_sha256=BASELINE_SHA,player_revision='Date-free programmes, consent-owned cooperation, retained services with deficit, Gulf counterplay, adapted generic naval development and Kissinger statecraft',early_cooperation_hooks=early['hooks'],
        gulf=dict(registered_ids=15,visible_focuses=14,canonical_source='tools/iraq_1970/usa_module.py',integration='tools/usa_1970_expansion/gulf_revision.py',owned_outputs=sorted(p for p in gulf_revision.outputs() if not p.startswith('common/autonomous_states/'))),
        domestic_hooks=dom_hooks,agreement_hooks=dip_hooks,owned_outputs=sorted(set(OWNED_SOURCE+[TREE,'common/scripted_effects/COLDWAR_USA_1970_expansion.txt','common/scripted_triggers/COLDWAR_USA_1970_expansion.txt','common/on_actions/COLDWAR_USA_1970_expansion.txt','common/decisions/COLDWAR_USA_1970_expansion.txt','common/decisions/categories/COLDWAR_USA_1970_expansion.txt','localisation/english/COLDWAR_USA_1970_expansion_l_english.yml','localisation/english/COLDWAR_USA_1970_building_capacity_l_english.yml'])),
        legacy_receipts=len(receipts),party_bundles=len(bundles),focus_integration=report,
        evidence='Generated and source checked. Native, visual, calendar and multiplayer evidence are recorded separately.')
    write('tools/usa_1970_expansion/manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    # Building-grant requirements share one English provider. Read the just
    # emitted owned triggers so every actual quantity has exactly one key.
    capacity_sources=[p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/scripted_triggers').glob('COLDWAR_USA_1970_*.txt')]
    capacity_path='localisation/english/COLDWAR_USA_1970_building_capacity_l_english.yml'
    if write(capacity_path,capacity_localisation(capacity_sources),True):changed.append(capacity_path)
    print(json.dumps(dict(changed=changed,focuses=installed_count,legacy_receipts=len(receipts),party_bundles=len(bundles)),indent=2))

if __name__=='__main__':main()
