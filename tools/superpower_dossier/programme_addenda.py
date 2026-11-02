# IMPERIA COLD WAR — Reviewed programme addenda without replaying treaty concessions
"""Reuse the native treaty paper for bilateral programme amendments to standing accords."""
from treaties import FIELDS,TREATIES
from programmes import PROGRAMMES

def extend(ef,tr,events,loc):
    def get(rows,name):return next(x for x in rows if x.startswith(name+' = {')).split('\n',1)[1].rsplit('\n}',1)[0]
    def put(rows,name,body):
        assert body.count('{')==body.count('}'),name
        rows[:]=[x for x in rows if not x.startswith(name+' = {')]
        rows.append(name+' = {\n'+body+'\n}')
    def effect(name,body):put(ef,name,body)
    def trigger(name,body):put(tr,name,body)
    # A programme has its own accepted revision. Original material-protocol receipts stay intact.
    for pid,p in PROGRAMMES.items():
        n=p['slot']
        active=get(tr,f'icwt_programme_{pid}_active').replace(f'icwt_programme_{pid}_receipt = global.icwt_{n}_revision',f'icwt_programme_{pid}_receipt = global.icwt_{n}_programme_revision')
        trigger(f'icwt_programme_{pid}_active',active)
    pay=get(ef,'icwt_programme_pay_setup')
    for pid,p in PROGRAMMES.items():pay=pay.replace(f'icwt_programme_{pid}_receipt = global.icwt_{p["slot"]}_revision',f'icwt_programme_{pid}_receipt = global.icwt_{p["slot"]}_programme_revision')
    effect('icwt_programme_pay_setup',pay)
    for n in range(1,len(TREATIES)+1):
        category=TREATIES[n-1][4]
        index=[i for i,t in enumerate(TREATIES,1) if t[4]==category].index(n)
        navigation=f'set_variable = {{ icwt_category = {category} }} set_variable = {{ icwt_page = {index//4} }}'
        for action in ('select','edit','review'):
            current=get(ef,f'icwt_{action}_{n}')
            current=current.replace(f'set_variable = {{ icwt_template = {n} }}',f'set_variable = {{ icwt_template = {n} }} {navigation}',1)
            effect(f'icwt_{action}_{n}',current)
        # Ordinary treaty creation always leaves amendment mode explicitly.
        effect(f'icwt_edit_{n}',get(ef,f'icwt_edit_{n}').replace('set_variable = { icwt_template = ', 'clear_variable = icwt_edit_addendum clear_variable = icwt_edit_base_revision\nset_variable = { icwt_template = ',1))
        send=get(ef,f'icwt_send_{n}').replace(f'add_to_variable = {{ global.icwt_sequence = 1 }}',f'clear_variable = global.icwt_p_addendum clear_variable = global.icwt_p_base_revision\nadd_to_variable = {{ global.icwt_sequence = 1 }}',1)
        effect(f'icwt_send_{n}',send)
        sign=get(ef,f'icwt_sign_{n}').replace(f'set_variable = {{ global.icwt_{n}_revision = global.icwt_p_revision }}',f'set_variable = {{ global.icwt_{n}_revision = global.icwt_p_revision }}\nset_variable = {{ global.icwt_{n}_programme_revision = global.icwt_p_revision }}',1)
        effect(f'icwt_sign_{n}',sign)
    # All material fields are immutable in an addendum, including the original term.
    validity=[]
    for pid,p in PROGRAMMES.items():
        n=p['slot']
        base=f'''USA = {{ has_country_flag = icwt_member_{n} }} SOV = {{ has_country_flag = icwt_member_{n} }}
OR = {{ check_variable = {{ global.icwt_{n}_end = 0 }} check_variable = {{ global.num_days < global.icwt_{n}_end }} }}'''
        equal='\n'.join(f'check_variable = {{ icwt_edit_{f} = global.icwt_{n}_{f} }}' for f in FIELDS if f!='programme')
        validity.append(f'''AND = {{ check_variable = {{ icwt_template = {n} }} {base}
check_variable = {{ icwt_edit_base_revision = global.icwt_{n}_revision }}
NOT = {{ check_variable = {{ icwt_edit_programme = global.icwt_{n}_programme }} }}
{equal}
}}''')
        category=TREATIES[n-1][4]
        effect(f'icwt_edit_addendum_{n}',f'''if = {{ limit = {{ icwt_core = yes NOT = {{ icwt_pending = yes }} {base} }}
set_variable = {{ icwt_template = {n} }} set_variable = {{ icwt_category = {category} }} set_variable = {{ icwt_page = 0 }} set_variable = {{ icsd_tab = 2 }} set_variable = {{ icwt_screen = 1 }} set_variable = {{ icwt_edit_addendum = 1 }}
set_variable = {{ icwt_edit_base_revision = global.icwt_{n}_revision }} clear_variable = icwt_review_revision clear_array = icwt_edit_invites
'''+ '\n'.join(f'set_variable = {{ icwt_edit_{f} = global.icwt_{n}_{f} }}' for f in FIELDS)+'''
icwt_display = yes icwt_touch = yes
}''')
        send=f'''if = {{ limit = {{ icwt_core = yes NOT = {{ icwt_pending = yes }} icwt_edit_valid = yes check_variable = {{ icwt_template = {n} }} check_variable = {{ icwt_edit_addendum = 1 }} }}
add_to_variable = {{ global.icwt_sequence = 1 }} set_variable = {{ global.icwt_pending = {n} }} set_variable = {{ global.icwt_p_revision = global.icwt_sequence }} set_variable = {{ global.icwt_p_author = THIS.id }}
set_variable = {{ global.icwt_p_addendum = 1 }} set_variable = {{ global.icwt_p_base_revision = icwt_edit_base_revision }}
'''+ '\n'.join(f'set_variable = {{ global.icwt_p_{f} = icwt_edit_{f} }}' for f in FIELDS)+f'''
clear_array = global.icwt_p_invites icwt_clear_reviews = yes
if = {{ limit = {{ tag = USA }} SOV = {{ country_event = {{ id = icwt.{n} }} }} }} else = {{ USA = {{ country_event = {{ id = icwt.{n} }} }} }}
set_variable = {{ icwt_screen = 3 }} icwt_touch_core = yes
}}'''
        effect(f'icwt_send_addendum_{n}',send)
        original=get(ef,f'icwt_send_{n}')
        effect(f'icwt_send_{n}',f'if = {{ limit = {{ check_variable = {{ icwt_edit_addendum = 1 }} }} icwt_send_addendum_{n} = yes }} else = {{\n{original}\n}}')
        pending_equal='\n'.join(f'check_variable = {{ global.icwt_p_{f} = global.icwt_{n}_{f} }}' for f in FIELDS if f!='programme')
        trigger(f'icwt_addendum_{n}_current',f'''check_variable = {{ global.icwt_pending = {n} }} check_variable = {{ global.icwt_p_addendum = 1 }}
check_variable = {{ global.icwt_p_base_revision = global.icwt_{n}_revision }} {base}
NOT = {{ check_variable = {{ global.icwt_p_programme = global.icwt_{n}_programme }} }}
{pending_equal}''')
        effect(f'icwt_sign_addendum_{n}',f'''if = {{ limit = {{ icwt_core = yes icwt_addendum_{n}_current = yes
icwt_reviewed_{n} = yes check_variable = {{ icwt_review_revision = global.icwt_p_revision }} NOT = {{ check_variable = {{ global.icwt_p_author = THIS.id }} }} }}
set_variable = {{ global.icwt_preflight = 1 }}
if = {{ limit = {{ NOT = {{ icwt_programme_pending_valid = yes }} }} set_variable = {{ global.icwt_preflight = 0 }} }}
if = {{ limit = {{ check_variable = {{ global.icwt_p_programme > 0 }} }}
 if = {{ limit = {{ NOT = {{ icwt_programme_relations = yes }} }} set_variable = {{ global.icwt_preflight = 0 }} }}
 USA = {{ icwt_programme_quote_setup = yes if = {{ limit = {{ NOT = {{ icwt_programme_setup_affordable = yes }} }} set_variable = {{ global.icwt_preflight = 0 }} }} }}
 SOV = {{ icwt_programme_quote_setup = yes if = {{ limit = {{ NOT = {{ icwt_programme_setup_affordable = yes }} }} set_variable = {{ global.icwt_preflight = 0 }} }} }}
}}
if = {{ limit = {{ check_variable = {{ global.icwt_preflight = 1 }} }}
set_variable = {{ global.icwt_{n}_programme = global.icwt_p_programme }} set_variable = {{ global.icwt_{n}_programme_revision = global.icwt_p_revision }}
USA = {{ icwt_programme_pay_setup = yes }} SOV = {{ icwt_programme_pay_setup = yes }}
clear_variable = global.icwt_pending icwt_clear_reviews = yes icwt_refresh = yes
news_event = {{ id = icwt.{2300+n} }}
set_variable = {{ icsd_tab = 3 }} set_variable = {{ icwt_register = 1 }} set_variable = {{ icwt_template = {n} }} icwt_touch_core = yes
}} else = {{ icwt_clear_reviews = yes country_event = {{ id = icwt.500 }} }}
}}''')
        original=get(ef,f'icwt_sign_{n}')
        effect(f'icwt_sign_{n}',f'if = {{ limit = {{ check_variable = {{ global.icwt_p_addendum = 1 }} }} icwt_sign_addendum_{n} = yes }} else = {{\n{original}\n}}')
        loc(f'icwt_news_addendum_{n}', 'American-Soviet programme terms agreed')
        events.append(f'news_event = {{ id = icwt.{2300+n} title = icwt_news_addendum_{n} desc = icwt_news_addendum_desc picture = GFX_icwt_news is_triggered_only = yes major = yes option = {{ name = icwt_news_ack }} }}')
        # Focus initiative prepares a real addendum only if both governments still participate.
        initiative=get(ef,f'icwt_initiative_{n}')
        old=f'}} else_if = {{ limit = {{ check_variable = {{ global.icwt_{n}_members^num > 0 }} }}'
        new=f'}} else_if = {{ limit = {{ {base} }} icwt_edit_addendum_{n} = yes set_variable = {{ icwt_edit_programme = {pid} }} }} else_if = {{ limit = {{ check_variable = {{ global.icwt_{n}_members^num > 0 }} }}'
        assert old in initiative,n
        effect(f'icwt_initiative_{n}',initiative.replace(old,new,1))
    trigger('icwt_edit_addendum_valid','OR = { NOT = { check_variable = { icwt_edit_addendum = 1 } } AND = { icwt_programme_relations = yes OR = {\n'+'\n'.join(validity)+'\n} } }')
    trigger('icwt_edit_valid',get(tr,'icwt_edit_valid')+'\nicwt_edit_addendum_valid = yes')
    # Withdrawals and expiry invalidate an outstanding addendum, without ending the standing treaty themselves.
    cleanup='if = { limit = { icwt_pending = yes check_variable = { global.icwt_p_addendum = 1 } NOT = { OR = { '+' '.join(f'icwt_addendum_{p["slot"]}_current = yes' for p in PROGRAMMES.values())+' } } } clear_variable = global.icwt_pending icwt_clear_reviews = yes icwt_touch_core = yes }'
    effect('icwt_programme_pending_cleanup',cleanup)
    effect('icwt_refresh',get(ef,'icwt_refresh')+'\nicwt_programme_pending_cleanup = yes')
    loc('icwt_news_addendum_desc','Washington and Moscow have signed a programme addendum to their standing agreement. The original treaty commitments and term remain in force. The programme follows its newly accepted funding and cooperation terms.')
    loc('icwt_amend_programme','Amend programme')
