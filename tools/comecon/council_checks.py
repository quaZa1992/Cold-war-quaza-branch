# IMPERIA COLD WAR — COMECON electoral and catalogue source invariants
from build import ROOT


def run(check,trees):
    def walk(body):
        for k,o,v in body:
            yield k,o,v
            if isinstance(v,list):yield from walk(v)
    def has(body,key,value=None):return any(k==key and (value is None or v==value) for k,o,v in walk(body))
    effects={k:v for k,o,v in trees['common/scripted_effects/ICW_COMECON.txt']}
    triggers={k:v for k,o,v in trees['common/scripted_triggers/ICW_COMECON.txt']}
    check(has(triggers['cc_ballot_can_vote'],'cc_human_member','yes') and 'global.cc_ballot_register' in str(triggers['cc_ballot_can_vote']),'electoral franchise uses actual represented full members and the opening register')
    check(has(triggers['cc_member_country'],'COLDWAR_SOV_is_union_republic','yes') and has(triggers['cc_member_country'],'NOT'),'Union republics retain their shared Soviet Council representation')
    check(has(effects['cc_update_authority'],'cc_chair_alive','yes') and has(effects['cc_update_authority'],'NOT'),'an eligible elected chair survives normal authority refresh')
    check(has(effects['cc_update_authority'],'global.cc_chair','global.cc_ballot_winner'),'temporary representation cannot erase the saved elected mandate')
    check(has(effects['cc_ballot_begin'],'global.cc_ballot_year','global.year') and has(effects['cc_ballot_begin'],'global.cc_ballot_days_left','15'),'ballot opens once per calendar year with fifteen full days')
    check('global.cc_ballot_start_day' in str(effects['cc_election_tick']) and has(effects['cc_election_tick'],'global.cc_ballot_days_left','global.num_days'),'deadline reads elapsed native game days')
    cast=str(effects['cc_ballot_cast'])
    check('cc_ballot_can_vote' in cast and 'cc_ballot_view_round' in cast and 'cc_ballot_proposal_valid' in cast,'casting repeats eligibility, sealed-ballot and current-issue guards')
    check(has(effects['cc_ballot_cast'],'cc_ballot_target','cc_ballot_proposed'),'a proposed flag enters the sealed ballot only inside the guarded cast')
    count=str(effects['cc_ballot_count']);resolve=str(effects['cc_ballot_resolve'])
    check('cc_human_member' in count and 'cc_ballot_receipt' in count and 'cc_ballot_target_valid' in count,'the count discards unrepresented voters and invalid candidates')
    check('cc_human_member' in resolve and 'cc_ballot_best' in resolve and "'>'" in resolve,'resolution selects the greatest tally and uses captured succession order for ties')
    for name in ('cc_ballot_begin','cc_ballot_cast','cc_ballot_resolve','cc_election_tick','cc_agenda_submit'):
        code=str(effects[name])
        check(not any(k in code for k in ('modify_treasury','treasury_change','_share','add_building_construction','_vote_revision')),name+': changes neither capital terms nor project signatures and assets')
    office=trees['common/scripted_effects/ICW_COMECON_office_view.txt']
    check(not any(k in str(office) for k in ('modify_treasury','treasury_change','cc_ballot_receipt','cc_ballot_target','_vote_revision')), 'office and catalogue display refreshes cannot cast, debit or sign')
    for s in range(1,5):
        for suffix in ('prepare_catalogue','prepare_agenda'):
            code=str(effects[f'cc_{s}_{suffix}'])
            check(f'cc_{s}_editable' in code and 'cc_view_slot' in code,f'file {s}: {suffix} requires the chair, an unsigned draft and its literal file')
        check('cc_agenda_selected_revision' in str(effects[f'cc_{s}_prepare_agenda']),f'file {s}: a changed referral cannot replace the selected proposal silently')
    source=(ROOT/'tools/comecon/council_ui.py').read_text(encoding='utf-8')
    check('max_slots_horizontal = 4' in source and '622,152,76,153' in source,'eight candidate cards occupy exactly two bounded rows')
    check('cc_ballot_chosen_flag' in source and '[?v.GetFlag]' in source,'selected ballot preserves the live country flag over the disabled ballot button')
    # Text metrics use the installed local fonts, rather than character-count estimates.
    from validate import parse
    import re
    text=(ROOT/'localisation/english/ICW_COMECON_l_english.yml').read_text(encoding='utf-8-sig')
    rewards=re.findall(r'^ cc_cat_(?:host|partner)_\d+_\d+:0 "(.*)"$',text,re.M)
    check(len(rewards)==264 and all(len(t.split('\\n'))*17<=100 for t in rewards),'all 264 catalogue reward columns fit before the national service rows')
    check('AI' not in text[text.index(' cc_ballot_rules:'):text.index(' cc_ballot_rules:')+1500] and 'multiplayer' not in text[text.index(' cc_ballot_rules:'):text.index(' cc_ballot_rules:')+1500].lower(),'electoral instructions use institutional language')
