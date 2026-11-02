# IMPERIA COLD WAR — Narrow retirement guards for the former automatic Union missions.
"""Pure text adapters used by the live installer and retained Soviet generator."""
import re
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'vietnam_1970'))

MARK = '# IMPERIA COLD WAR — Annual order retirement guard'
OFF = 'NOT = { has_global_flag = COLDWAR_ORD_enabled }'
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[^\s{}#"]+')


def closing(text, opening):
    depth = 0
    for match in TOKEN.finditer(text, opening):
        token = match.group()
        if token == '{': depth += 1
        elif token == '}':
            depth -= 1
            if depth == 0: return match.start()
    raise ValueError('Unclosed native block')


def wrap(text, name, human=False, alternative=''):
    found = re.search(r'^' + re.escape(name) + r'\s*=\s*\{', text, re.M)
    if not found: raise ValueError('Missing legacy effect: ' + name)
    start = text.index('{', found.start()) + 1
    end = closing(text, start - 1)
    body = text[start:end]
    if MARK in body[:250]: return text
    condition = OFF + (' is_ai = no' if human else '')
    replacement = '\n\t' + MARK + '\n\tif = { limit = { ' + condition + ' }\n' + body + '\n\t}\n'
    if alternative: replacement += '\telse = { ' + alternative + ' }\n'
    return text[:start] + replacement + text[end:]


def effects(text):
    for name in ('issue_annual_target', 'switch_target', 'start_target', 'start_directive', 'ai_floor', 'ai_floor_directive', 'union_plan_won', 'settle_year'):
        text = wrap(text, 'COLDWAR_UNI_' + name)
    for name in ('target_done', 'directive_done', 'target_failed', 'directive_failed', 'add_shortfall', 'pripiski_exposed'):
        text = wrap(text, 'COLDWAR_UNI_' + name, human=True)
    text=wrap(text, 'COLDWAR_UNI_january_session', alternative='COLDWAR_ORD_tally_calendar = yes')
    name='COLDWAR_UNI_add_union_buff'
    found=re.search(r'^'+name+r'\s*=\s*\{',text,re.M)
    start=text.index('{',found.start())+1;end=closing(text,start-1);body=text[start:end]
    if MARK+': aggregate duration' not in body[:250]:
        shorter=re.sub(r'\bdays = 365\b','days = 180',body)
        text=text[:start]+'\n'+MARK+': aggregate duration\nif = { limit = { has_global_flag = COLDWAR_ORD_enabled } '+shorter+' } else = { '+body+' }\n'+text[end:]
    return re.sub(r'[ \t]+(?=\n|$)', '', text)


LOC_UPDATES = {
    'COLDWAR_UNI_the_union_plan_desc': 'Moscow and the republican councils coordinate annual commissions through the Union register. Directives and republican proposals share a full year of work, while production returns and real consignments establish the result.',
    'COLDWAR_UNI_gosplan_directives_desc': 'A permanent commissioning staff gives the Union ministries a dependable means of coordinating enterprise schedules. Standardisation improves production at the cost of a larger administrative establishment.',
    'COLDWAR_UNI_peoples_control_desc': 'Committees of control reconcile enterprise accounts and republican production returns. Regular inspection can recover public revenue, but it requires officials, offices and sustained administrative expenditure.',
    'COLDWAR_UNI_party_control_commission_desc': 'The control commission enforces the centre\'s decisions across ministries and republican administrations. Its growing authority strengthens central direction while provoking resentment among officials and enterprise directors.',
    'COLDWAR_UNI_the_tolkachi_desc': 'Procurement agents know which enterprise has a spare machine, a missing cable or a wagon waiting in a siding. Their informal networks can keep republican commissions moving, at a considerable administrative cost.',
    'COLDWAR_UNI_storming_the_plan_desc': 'Factories can add night and weekend shifts when an annual commission falls behind. The increased output competes with construction for transport and materials, and places a strain on workers.',
    'COLDWAR_UNI_counter_plan_desc': 'Enterprise collectives promise higher operating standards and longer production series. The counter-plan raises attainable efficiency while demanding more power from the republican grid.',
    'COLDWAR_UNI_directives_9_tt': 'Annual collective fulfilment also grants the Ninth Plan programme for 180 days.',
    'COLDWAR_UNI_directives_10_tt': 'Annual collective fulfilment also grants the Tenth Plan programme for 180 days.',
    'COLDWAR_UNI_directives_11_tt': 'Annual collective fulfilment also grants the Eleventh Plan programme for 180 days.',
    'COLDWAR_UNI_directives_12_tt': 'Annual collective fulfilment also grants the Twelfth Plan programme for 180 days.',
}


def joint(text):
    mark=MARK+': joint policies'
    if mark in text:return text
    from script_ast import parse,emit,first
    rows=parse(text)
    policy_focus={'gosplan_directives':('directive_staff','originator'),'peoples_control':('production_audit','originator'),'party_control_commission':('control_commission','originator'),'counter_plan':('counter_plan','all')}
    remove={'COLDWAR_UNI_draft_unlock_tt','COLDWAR_UNI_cheap_directives_tt','COLDWAR_UNI_peoples_control_tt','COLDWAR_UNI_party_control_tt','COLDWAR_UNI_tolkachi_unlock_tt','COLDWAR_UNI_storming_unlock_tt','COLDWAR_UNI_counter_unlock_tt'}
    for k,o,focus in rows:
        if k!='joint_focus':continue
        identifier=first(focus,'id','').removeprefix('COLDWAR_UNI_')
        for i,(key,operator,body) in enumerate(focus):
            if key.startswith('completion_reward'):
                body[:]=[r for r in body if not(r[0]=='custom_effect_tooltip' and (r[2] in remove or r[2] in {'COLDWAR_UNI_directives_'+str(n)+'_tt' for n in range(9,13)}))]
                body.extend(parse('hidden_effect = { COLDWAR_ORD_sync_policies = yes }'))
        if identifier in policy_focus:
            policy,who=policy_focus[identifier]
            field='completion_reward_joint_originator' if who=='originator' else 'completion_reward'
            target=first(focus,field)
            target.extend(parse('effect_tooltip = { add_ideas = COLDWAR_ORD_policy_'+policy+' }'))
        if identifier in {'the_tolkachi','storming_the_plan'}:
            decision='procurement_agents' if identifier=='the_tolkachi' else 'overtime'
            first(focus,'completion_reward').extend(parse('unlock_decision_tooltip = COLDWAR_ORD_'+decision))
        if identifier.startswith('directives_'):
            n=identifier.rsplit('_',1)[1]
            first(focus,'completion_reward_joint_originator').extend(parse('effect_tooltip = { custom_effect_tooltip = COLDWAR_ORD_collective_heading add_timed_idea = { idea = COLDWAR_UNI_plan_fulfilled_'+n+' days = 180 } }'))
    header=text[:text.index('joint_focus')]
    result=header+mark+'\n'+emit(rows)+'\n'
    # Preserve the SSR generator's marked offset rather than allowing its next
    # narrow integration pass to insert a second identical conditional offset.
    for k,o,focus in rows:
        if k!='joint_focus' or first(focus,'id')!='COLDWAR_UNI_the_union_plan':continue
        for key,op,value in focus:
            if key=='offset' and 'COLDWAR_SSR_1970_focus' in str(value):
                serialised=emit([(key,op,value)],1)
                wrapped='\t# IMPERIA COLD WAR — SSR Union Plan position BEGIN\n'+serialised+'\n\t# IMPERIA COLD WAR — SSR Union Plan position END'
                assert result.count(serialised)==1
                result=result.replace(serialised,wrapped,1)
    return result


def triggers(text):
    for name,modern in (('COLDWAR_UNI_is_republic','COLDWAR_ORD_republic'),('COLDWAR_UNI_is_member','COLDWAR_ORD_member')):
        found=re.search(r'^'+name+r'\s*=\s*\{',text,re.M)
        start=text.index('{',found.start())+1;end=closing(text,start-1);body=text[start:end]
        if MARK+': membership' in body[:250]:continue
        replacement='\n'+MARK+': membership\nOR = { AND = { has_global_flag = COLDWAR_ORD_enabled '+modern+' = yes } AND = { '+OFF+' '+body+' } }\n'
        text=text[:start]+replacement+text[end:]
    return re.sub(r'[ \t]+(?=\n|$)', '', text)


def events(text):
    # Keep 41-44: these expire previously settled historical effects. They cannot
    # grant a new order penalty and must not leave old debits permanently active.
    if MARK + ': events' in text: return text
    from script_ast import parse, emit
    rows = parse(text)
    metadata = {'name', 'trigger', 'ai_chance', 'highlight', 'default', 'original_recipient_only', 'show_sound', 'goto', 'custom_cost_trigger', 'custom_cost_text'}
    for kind, op, value in rows:
        if kind not in {'country_event', 'news_event'} or not isinstance(value, list): continue
        identifier = next((v for k,o,v in value if k == 'id'), '')
        number = int(identifier.rsplit('.',1)[1])
        if number in {41,42,43,44}: continue
        trigger = next((v for k,o,v in value if k == 'trigger'), None)
        if trigger is None: value.append(('trigger', '=', parse(OFF)))
        else: trigger.extend(parse(OFF))
        for i,(key,operator,body) in enumerate(value):
            if key == 'immediate': value[i] = (key,operator,parse('if = { limit = { '+OFF+' } '+emit(body)+' }'))
            elif key == 'option':
                kept = [r for r in body if r[0] in metadata]
                mutations = [r for r in body if r[0] not in metadata]
                if mutations: kept.extend(parse('if = { limit = { '+OFF+' } '+emit(mutations)+' }'))
                value[i] = (key,operator,kept)
    # Retain the complete original file-start attribution/provenance comments.
    header = text[:text.index('add_namespace')]
    return header + MARK + ': events\n' + emit(rows) + '\n'


def categories(text):
    if MARK + ': category' in text: return text
    pattern = r'(\bvisible\s*=\s*\{)'
    assert len(re.findall(pattern,text)) == 1
    return re.sub(pattern, r'\1\n\t\t'+MARK+': category\n\t\t'+OFF, text, count=1)
