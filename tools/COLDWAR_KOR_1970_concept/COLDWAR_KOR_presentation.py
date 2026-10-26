# IMPERIA CW — Cold War: South Korean release presentation and English prose.
"""Display-only adapters. Every predicate and executed reward is retained."""
import hashlib
import json
import re
from pathlib import Path

PARTIES = {
    '0': 'Democratic Republican Party', '1': 'New Democratic Party',
    '2': 'democratic reform movement', '3': 'Unification Socialist Party',
    '4': 'Revolutionary Party for Reunification', '5': 'student civic coalition',
    '7': 'security directorate', '19': 'independent Southern left',
    '22': 'Army and Democratic Justice Party',
}
COUNTRIES = {'KOR':'South Korea','NKO':'North Korea','USA':'the United States','JAP':'Japan','GER':'West Germany','SOV':'the Soviet Union','CHI':'China','SVN':'South Vietnam','SAU':'Saudi Arabia','IRQ':'Iraq'}
AGREEMENTS = {
    'red_cross_channel':'Red Cross Liaison', 'family_reunions':'Family Reunions',
    'military_hotline':'Military Hotline', 'nonaggression_compact':'Nonaggression Compact',
    'verified_restraint':'Reciprocal Military Restraint', 'working_contacts':'Inter-Korean Working Contacts',
    'sovereign_confederation':'Sovereign Korean Consultation', 'confederal_secretariat':'Korean Consultative Secretariat',
    'parallel_recognition':'Reciprocal Recognition', 'limited_trade':'Limited Inter-Korean Trade',
    'northern_security_compact':'Northern Security Liaison', 'independent_left_dialogue':'Independent Southern Dialogue',
    'technology_licence':'Industrial Licensing', 'allied_procurement_contract':'Allied Procurement',
    'us_alliance_assurance':'American Alliance Assurances', 'security_partner_contacts':'Military Staff Cooperation',
    'japan_technology_finance':'Japanese Technical Cooperation', 'historical_claims_dialogue':'Historical Claims Talks',
    'alternative_finance_contacts':'Alternative Foreign Finance', 'nordpolitik_recognition':'Nordpolitik Opening',
    'pacific_trade_contacts':'Pacific Export Cooperation', 'revolutionary_recognition':'Revolutionary Recognition',
    'neutrality_guarantees':'Negotiated Neutrality', 'vietnam_withdrawal_settlement':'Vietnam Withdrawal Settlement',
    'cultural_exchanges':'Cultural Exchange Framework', 'cultural_visits':'Cultural Visits',
    'border_notifications':'Military Notification Talks', 'border_notice_protocol':'Border Notification Protocol',
    'korean_community_dialogue':'Korean Community Dialogue',
    'japan_joint_training':'Korean-Japanese Technical Training', 'gulf_project_access':'Construction Market Access',
    'worker_rights_protocol':'Overseas Worker Protection', 'peninsula_liaison_office':'Permanent Korean Liaison',
    'korean_final_settlement':'Korean Cooperation Settlement', 'us_garrison':'American Stationing Agreement',
    'us_drawdown':'Negotiated American Drawdown', 'us_combined_command':'Combined Command Agreement',
    'combined_readiness_board':'Combined Readiness Board',
}

# Explicit opposites describe the whole condition; an absent receipt never
# implies that an offer was refused or that a country has already held a vote.
FLAG_TEXT = {
 'constitutional_crisis':('The presidential contest or a constitutional crisis has opened the question of revision.','No presidential contest or constitutional crisis has opened the question of revision.'),
 'constitution_yushin':('The Yushin Constitution is in force.','The Yushin Constitution is not in force.'),
 'constitution_controlled_fifth':('The controlled Fifth Republic constitution is in force.','The controlled Fifth Republic constitution is not in force.'),
 'constitutional_order':('Constitutional government has been established.','Constitutional government has not been established.'),
 'constitution_presidential':('The presidential constitution has been ratified.','The presidential constitution has not been ratified.'),
 'constitution_parliamentary':('The parliamentary constitution has been ratified.','The parliamentary constitution has not been ratified.'),
 'constitution_consensus':('The consensus constitution has been ratified.','The consensus constitution has not been ratified.'),
 'military_reconsolidation':('Military command has reasserted control.','Military command has not reasserted control.'),
 'opposition_constitutional_demand':('The opposition is demanding constitutional revision.','The opposition has not raised a demand for constitutional revision.'),
 'military_opening_authorized':('The military government has authorized a political opening.','The military government has not authorized a political opening.'),
 'transition_open':('A transition to civilian government is under way.','No transition to civilian government is under way.'),
 'talks_authorized':('Constitutional negotiations have been authorized.','Constitutional negotiations have not been authorized.'),
 'talks_retry_cooldown':('The §Y90-day§! interval before renewed negotiations is still in effect.','No waiting period prevents renewed constitutional negotiations.'),
 'charter_retry_cooldown':('The §Y90-day§! interval before resubmission is still in effect.','No waiting period prevents another charter ballot.'),
 'charter_rejected':('The previous constitutional draft was rejected.','No rejection of the constitutional draft is recorded.'),
 'charter_mandate':('The negotiating parties have agreed a constitutional mandate.','The negotiating parties have not agreed a constitutional mandate.'),
 'ballot_pending':('A constitutional ratification ballot is pending.','No constitutional ratification ballot is pending.'),
 'constitutional_ratification_passed':('The constitutional draft has passed ratification.','The constitutional draft has not passed ratification.'),
 'negotiating_commitment':('The government has committed to constitutional negotiations.','The government has not committed to constitutional negotiations.'),
 'electoral_opening':('A competitive electoral opening has been accepted.','A competitive electoral opening has not been accepted.'),
 'caretaker_installed':('A civilian caretaker administration is in office.','No civilian caretaker administration is in office.'),
 'civilian_succession_open':('A civilian succession has been authorized.','A civilian succession has not been authorized.'),
 'officer_council_contest':('An officer council is contesting the succession.','No officer council is contesting the succession.'),
 'historical_chun_transition':('Chun Doo-hwan’s military cabinet has been authorized.','Chun Doo-hwan’s military cabinet has not been authorized.'),
 'nationwide_martial_law':('Nationwide martial law is in force.','Nationwide martial law is not in force.'),
 'security_directorate_ratified':('An exceptional security caretaker has been authorized.','An exceptional security caretaker has not been authorized.'),
 'revolutionary_settlement':('The Southern revolutionary cabinet has been ratified.','The Southern revolutionary cabinet has not been ratified.'),
 'civic_legal_5':('Student civic organizations may participate legally.','Student civic organizations have not been legalized.'),
 'civic_legal_19':('Independent left organizations may participate legally.','Independent left organizations have not been legalized.'),
 'electoral_party_4_legal':('The Revolutionary Party for Reunification may contest elections.','The Revolutionary Party for Reunification may not contest elections.'),
 'electoral_party_22_legal':('The Democratic Justice Party may contest elections.','The Democratic Justice Party may not contest elections.'),
 'judicial_review':('The Constitutional Court has a legal mandate.','The Constitutional Court has no legal mandate.'),
 'court_appointments_implemented':('The court’s appointments have been funded.','The court’s appointments have not been funded.'),
 'court_implementation_pending':('The court is awaiting commissioning.','The court is not awaiting commissioning.'),
 'court_commissioning_delay':('The court’s §Y90-day§! commissioning period is still in effect.','No commissioning delay prevents the court from opening.'),
 'judicial_review_operational':('The Constitutional Court is operational.','The Constitutional Court is not operational.'),
 'intelligence_oversight':('Civilian intelligence oversight has been established.','Civilian intelligence oversight has not been established.'),
 'repression_cases_reviewed':('The review of political repression has been authorized.','The review of political repression has not been authorized.'),
 'direct_election_principle':('Direct presidential elections have been accepted in principle.','Direct presidential elections have not been accepted in principle.'),
 'djp_formed':('The Democratic Justice Party has been constituted.','The Democratic Justice Party has not been constituted.'),
 'ndrp_formed':('The New Democratic Republican Party has been constituted.','The New Democratic Republican Party has not been constituted.'),
 'djp_merger_authorized':('The DJP has authorized merger negotiations.','The DJP has not authorized merger negotiations.'),
 'ys_merger_authorized':('Kim Young-sam’s organization has authorized merger negotiations.','Kim Young-sam’s organization has not authorized merger negotiations.'),
 'ys_merger_pending':('Kim Young-sam’s organization is considering the merger proposal.','No merger proposal is awaiting Kim Young-sam’s organization.'),
 'ndrp_merger_authorized':('The NDRP has authorized merger negotiations.','The NDRP has not authorized merger negotiations.'),
 'conservative_merger_ratified':('The participating parties have ratified the conservative merger.','The participating parties have not ratified the conservative merger.'),
 'transition_1990_recorded':('The conservative merger proposal has been resolved.','The conservative merger proposal has not been resolved.'),
 'kjp_successor':('Kim Jong-pil has succeeded to the premiership or presidency.','Kim Jong-pil has not succeeded to national executive office.'),
 'lawful_election_completed':('An election under the ratified constitution has been resolved.','No election under the ratified constitution has been resolved.'),
 'vietnam_commitment_active':('Korean obligations in Vietnam remain unsettled.','Korean obligations in Vietnam have been settled or are no longer active.'),
 'civilian_control':('Civilian authority over military command has been established.','Civilian authority over military command has not been established.'),
 'civilian_appointments':('Military appointments are subject to civilian authority.','Military appointments are not subject to civilian authority.'),
 'court_event_queued':('The court’s commissioning decision is awaiting a response.','No court commissioning decision is awaiting a response.'),
 'democratic_safeguards':('Constitutional safeguards have been enacted.','Constitutional safeguards have not been enacted.'),
}
FLAG_TEXT.update({
 'usfk_exercise_pending':('A combined-exercise proposal is awaiting a response.','No combined-exercise proposal is awaiting a response.'),
 'usfk_exercise_running':('A combined exercise is in progress.','No combined exercise is in progress.'),
 'usfk_exercise_cooldown':('The interval before another exercise invitation is still in effect.','No waiting period prevents another exercise invitation.'),
 'usfk_exercise_offer_open':('The exercise proposal remains within its response period.','The exercise proposal has no open response period.'),
 'usfk_exercise_assent':('Washington has approved the exercise proposal.','Washington has not approved the exercise proposal.'),
 'usfk_exercise_training_open':('The agreed training period is under way.','The agreed training period is no longer under way.'),
 'legacy_working_contacts':('An existing working-level channel is recognized.','No existing working-level channel is recognized.'),
})

def money(amount):
    """MD budget amounts stay in billions; display small flows in millions."""
    amount=abs(float(amount))
    if amount < 1:return f'${amount*1000:g} million'
    return f'${amount:g} billion'

def term(days):
    if days and days % 365 == 0:return str(days//365)+' years' if days!=365 else '1 year'
    return str(days)+' days'

def agreement_terms(c,offer=True):
    """Use identical ledger amounts in compact, explicitly conditional text."""
    title=AGREEMENTS[c['key']];tags=c.get('tags',[])
    partners=', '.join(COUNTRIES.get(x,x) for x in tags)
    rows=[]
    if offer:
        rows.append('§YProposal: '+title+'§!')
        if c['key']=='nordpolitik_recognition':rows.append('Requires a separate agreement with each counterpart.')
        elif c.get('selector_index'):rows.append('Requires the selected partner’s acceptance.')
        else:rows.append('Requires agreement with '+partners+'.')
        rows.append('§YOn ratification:§!')
    else:
        rows.append('§YAgreement commitments§!')
        if len(tags)>1 and not c.get('selector_index'):rows.append('All participating governments must accept before these terms take effect.')
    weekly=c.get('KOR_weekly_bn',0);other_weekly=c.get('recipient_effects',{}).get('weekly_expense_bn',0)
    if weekly and weekly==other_weekly and len(tags)==1:
        rows.append('  Upkeep, each government: §R'+money(weekly)+'/week§!')
    else:
        if weekly:rows.append('  South Korean upkeep: §R'+money(weekly)+'/week§!')
        if other_weekly:
            payer=COUNTRIES.get(tags[0],tags[0]) if len(tags)==1 else 'Each counterpart'
            rows.append('  '+payer+' upkeep: §R'+money(other_weekly)+'/week§!')
    days=c.get('duration_days',0)
    if days:rows.append('  Duration: §Y'+term(days)+'§!')
    if c['key']=='working_contacts':rows.append('  Opens negotiations on recognition and Korean consultation.')
    if c['key']=='us_garrison':rows.append('  Authorizes American military access under the stationing agreement.')
    if c['key']=='us_drawdown':rows.append('  Replaces resident-force support with negotiated drawdown and visiting-force cooperation.')
    if c.get('recipient_effects',{}).get('treasury_change',0)<0 and c.get('selector_index'):
        rows.append('  The selected partner contributes §R'+money(c['recipient_effects']['treasury_change'])+'§! upon ratification.')
    return '\n'.join(rows)


class Presentation:
    def __init__(self,compiler):
        self.c=compiler;self.loc=compiler.loc;self.P='COLDWAR_KOR_'
        from script_ast import parse,emit,first
        self.parse=parse;self.emit=emit;self.first=first
        self.contracts={x['key']:x for x in compiler.d['contracts']}
        self.triggers={k:v for path,code in compiler.files.items() if path.startswith('common/scripted_triggers/') for k,o,v in parse(code)}
        self.sources={};self.flag_count=0;self.variable_count=0

    def tooltip(self,key,pair,predicate):
        self.loc[key],self.loc[key+'_NOT']=pair
        return ('custom_trigger_tooltip','=',[('tooltip','=',key),('not_tooltip','=',key+'_NOT')]+predicate)

    def flag_pair(self,flag):
        name=flag.removeprefix(self.P)
        if name in FLAG_TEXT:return FLAG_TEXT[name]
        candidates={'ys':'Kim Young-sam','dj':'Kim Dae-jung','kjp':'Kim Jong-pil','roh':'Roh Tae-woo','park':'Park Chung Hee','yun':'Yun Po-sun','chun':'Chun Doo-hwan'}
        if name.endswith('_nominated') and name[:-10] in candidates:
            who=candidates[name[:-10]];return (who+' is registered as a candidate.',who+' is not registered as a candidate.')
        if name.startswith('presidential_term_served_'):
            who=candidates[name.removeprefix('presidential_term_served_')]
            return (who+' has served a term under the one-term constitution.',who+' has not served a term under the one-term constitution.')
        for stem in ('charter_supporter_','charter_endorsement_pending_'):
            if name.startswith(stem):
                party=PARTIES[name.removeprefix(stem)]
                if stem=='charter_supporter_':return ('The '+party+' endorses the constitutional draft.','The '+party+' has not endorsed the constitutional draft.')
                return ('The '+party+' is considering the constitutional draft.','No endorsement request is awaiting the '+party+'.')
        if name.endswith('_paid') and flag[:-5] in self.c.nodes:
            label=self.c.nodes[flag[:-5]]['label']
            return ('Has completed §Y'+label+'§!.','Has not completed §Y'+label+'§!.')
        for key,title in sorted(AGREEMENTS.items(),key=lambda x:-len(x[0])):
            if not name.startswith(key+'_'):continue
            state=name[len(key)+1:];subject='The §Y'+title+'§! agreement'
            if state=='signed':return (subject+' is in force.',subject+' is not in force.')
            if state=='pending':return ('A §Y'+title+'§! proposal is awaiting a response.','No §Y'+title+'§! proposal is awaiting a response.')
            if state=='cooldown':return ('The waiting period for another §Y'+title+'§! proposal is still in effect.','No waiting period prevents another §Y'+title+'§! proposal.')
            if state=='offer_open':return ('The §Y'+title+'§! proposal remains within its §Y60-day§! response period.','The §Y'+title+'§! proposal has no open response period.')
            if state=='refused':return ('A refusal of the §Y'+title+'§! proposal is recorded.','No refusal of the §Y'+title+'§! proposal is recorded.')
            if state=='expired':return ('An expired §Y'+title+'§! proposal is recorded.','No expired §Y'+title+'§! proposal is recorded.')
            if state.endswith('_signed') and state[:-7] in COUNTRIES:
                who=COUNTRIES[state[:-7]];return (subject+' with '+who+' is in force.',subject+' with '+who+' is not in force.')
            for kind in ('target_','assent_'):
                if state.startswith(kind) and state[len(kind):] in COUNTRIES:
                    who=COUNTRIES[state[len(kind):]]
                    if kind=='target_':return ('The proposal is addressed to '+who+'.','The proposal is not addressed to '+who+'.')
                    return (who[0].upper()+who[1:]+' has accepted the proposal.',who[0].upper()+who[1:]+' has not accepted the proposal.')
        legacy={
            'COLDWAR_NKO_korean_channel_pending':'an inter-Korean liaison proposal',
            'COLDWAR_NKO_foreign_korean_channel_confederation_offer_pending':'a Northern consultative-framework proposal',
            'COLDWAR_NKO_korean_channel_accepted':'the Northern inter-Korean liaison agreement',
            'COLDWAR_NKO_korean_channel_confederation_offer_accepted':'the Northern consultative framework',
        }
        if flag in legacy:
            thing=legacy[flag]
            proposal=thing.removeprefix('an ').removeprefix('a ')
            return (proposal[0].upper()+proposal[1:]+' is awaiting resolution.','No '+proposal+' is awaiting resolution.') if flag.endswith('pending') else ('Acceptance of '+thing+' is recorded.','No acceptance of '+thing+' is recorded.')
        # Only a readable fallback for focus-only institutional milestones;
        # release validation separately inventories every decision condition.
        phrase=name.replace('_',' ')
        for suffix,positive,negative in (
            (' authorized',' has been authorized.',' has not been authorized.'),
            (' established',' has been established.',' has not been established.'),
            (' ratified',' has been ratified.',' has not been ratified.'),
            (' open',' is open.',' is not open.'),
            (' operational',' is operational.',' is not operational.'),
            (' pending',' is pending.',' is not pending.'),
        ):
            if phrase.endswith(suffix):
                subject=phrase[:-len(suffix)].capitalize();return subject+positive,subject+negative
        return ('The §Y'+phrase+'§! settlement is in effect.','The §Y'+phrase+'§! settlement is not in effect.')

    def trigger(self,rows,inline=False,trail=()):
        out=[]
        for k,o,v in rows:
            if inline and k in self.triggers and v in ('yes','no'):
                assert k not in trail,'Recursive presentation provider: '+k
                expanded=self.trigger(self.triggers[k],inline=True,trail=trail+(k,))
                out.extend(expanded if v=='yes' else [('NOT','=',expanded)]);continue
            if k=='hidden_trigger':out.append((k,o,v));continue
            if k=='custom_trigger_tooltip':
                predicate=[x for x in v if x[0] not in ('tooltip','not_tooltip')]
                out.extend(self.trigger(predicate,inline,trail));continue
            if k in ('tag','original_tag','IMP_is_1970_scenario') or (k=='has_country_flag' and v in (self.P+'initialized',self.P+'sync_running')):
                out.append(('hidden_trigger','=',[(k,o,v)]));continue
            if k=='has_country_flag' and v.startswith(('COLDWAR_KOR_','COLDWAR_NKO_')):
                self.flag_count+=1
                key=self.P+'require_'+v.removeprefix(self.P)+'_tt'
                out.append(self.tooltip(key,self.flag_pair(v),[(k,o,v)]));continue
            if k=='check_variable':
                var,compare,value=v[0] if len(v)==1 else (self.first(v,'var'),self.first(v,'compare'),self.first(v,'value'))
                pair=None
                if var=='ruling_party' and value in PARTIES:
                    party=PARTIES[value];pair=('The '+party+' leads the government.','The '+party+' does not lead the government.')
                elif var and var.startswith('party_banned_array^'):
                    party=PARTIES.get(var.split('^')[1],'required party');pair=('The '+party+' may participate legally.','The '+party+' is prohibited from political participation.')
                elif var and var.startswith('party_pop_array^'):
                    party=PARTIES.get(var.split('^')[1],'required party');pair=('The '+party+' has political support.','The '+party+' has no political support.')
                elif var==self.P+'charter_model':
                    if compare in ('>','greater_than') and value=='0':pair=('A constitutional draft has been selected.','No constitutional draft has been selected.')
                    elif compare in ('=','equals') and value in ('1','2','3'):
                        model={'1':'presidential','2':'parliamentary','3':'consensus'}[value]
                        pair=('The selected draft provides for a '+model+' republic.','The selected draft does not provide for a '+model+' republic.')
                elif var and ('_sender_party' in var or '_sender_office_epoch' in var):
                    pair=('The proposal retains the authority of its original government.','The government that issued this proposal is no longer in office.')
                elif var==self.P+'usfk_exercise_kind':
                    kind='field' if value=='1' else 'command-post'
                    pair=('The agreed programme is a '+kind+' exercise.','The agreed programme is not a '+kind+' exercise.')
                elif var and var.startswith(self.P+'slot_'):
                    out.append(('hidden_trigger','=',[(k,o,v)]));continue
                if pair:
                    self.variable_count+=1;digest=hashlib.sha256(repr(v).encode()).hexdigest()[:12]
                    out.append(self.tooltip(self.P+'condition_'+digest+'_tt',pair,[(k,o,v)]));continue
            if isinstance(v,list):out.append((k,o,self.trigger(v,inline,trail)))
            else:out.append((k,o,v))
        return out

    def prose(self):
        expected={n['id']+'_desc' for n in self.c.d['nodes']};seen=set()
        for source in ('COLDWAR_KOR_prose_politics.json','COLDWAR_KOR_prose_national.json'):
            entries=json.loads((Path(__file__).parent/source).read_text(encoding='utf-8'))
            for key,value in entries.items():
                if key.startswith('_'):continue
                assert key in expected and key not in seen,key
                seen.add(key);self.loc[key]=value
                stem=key[:-5]
                for suffix in ('_preview_desc','_programme_desc'):
                    if stem+suffix in self.loc:self.loc[stem+suffix]=value
        for n in self.c.d['nodes']:
            if n['id']+'_desc' not in seen or n.get('delivery_description'):
                key=n['id']+'_desc';self.loc[key]=n.get('delivery_description',n['description']);seen.add(key)
                for suffix in ('_preview_desc','_programme_desc'):
                    if n['id']+suffix in self.loc:self.loc[n['id']+suffix]=self.loc[key]
        assert seen==expected,'Incomplete editorial focus coverage'

    def material_effects(self,rows):
        out=[]
        native={'modify_treasury_effect','add_political_power','add_stability','add_war_support','army_experience','navy_experience','air_experience','add_timed_idea','add_ideas','remove_ideas','add_dynamic_modifier','remove_dynamic_modifier','country_event','news_event','diplomatic_relation','add_building_construction'}
        for k,o,v in rows:
            if k in native:out.append((k,o,v))
            elif k=='set_temp_variable' and self.first(v,'treasury_change') is not None:out.append((k,o,v))
            elif k in ('if','else_if','else'):
                effect=self.material_effects([x for x in v if x[0]!='limit'])
                if effect:
                    if k!='else':effect=[('limit','=',self.trigger(self.first(v,'limit',[])))]+effect
                    out.append((k,o,effect))
            elif k in COUNTRIES:
                effect=self.material_effects(v)
                if effect:out.append((k,o,effect))
        return out

    def decision_hint(self,key):
        hints={
            'legalize_civic_parties':'Legalizes the student civic and independent left organizations for political participation.',
            'reopen_constitutional_talks':'Authorizes a renewed constitutional opening under the military government.',
            'reopen_charter_ballot':'Submits the selected draft to a new §Y30-day§! ratification ballot.',
            'implement_constitutional_court':'Funds judicial appointments. Commissioning takes §Y90 days§!.',
            'review_repression_cases':'Begins the accountability settlement and replaces the martial-law legitimacy burden.',
            'authorize_djp_merger':'Authorizes the DJP delegation to negotiate the proposed merger.',
            'authorize_ys_merger':'Requests a separate decision from Kim Young-sam’s organization.',
            'authorize_ndrp_merger':'Authorizes the NDRP delegation to negotiate the proposed merger.',
            'open_conservative_merger':'Convenes the authorized delegations to accept or reject the merger.',
            'authorize_military_succession':'Appoints §YChun Doo-hwan§! and establishes an Army-led cabinet.',
            'ratify_revolutionary_settlement':'Ratifies the Southern revolutionary cabinet after its accession to government.',
            'form_democratic_justice_party':'Constitutes the DJP as an electoral organization.',
            'authorize_security_directorate':'Installs an exceptional §Ysecurity directorate§! and suspends elections.',
            'authorize_kjp_handover':'Transfers executive office to §YKim Jong-pil§! under the authorized civilian succession.',
            'northern_consultation_proposal':'Invites Seoul to decide whether to open reciprocal consultations.',
        }
        name=key.removeprefix(self.P)
        if name in hints:return hints[name]
        if name.startswith('usfk_exercise_invite_'):return 'Invites Washington to approve the proposed training programme. Both governments must authorize its launch.'
        candidates={'ys':'Kim Young-sam','dj':'Kim Dae-jung','roh':'Roh Tae-woo','kjp':'Kim Jong-pil'}
        if name.startswith('nominate_'):return 'Registers §Y'+candidates[name.removeprefix('nominate_')]+'§! as a candidate. The election determines who takes office.'
        if name.startswith('request_charter_endorsement_'):return 'Requests the party’s endorsement of the constitutional draft.'
        if name.startswith('withdraw_charter_endorsement_'):return 'Withdraws the party’s endorsement before the ballot is submitted.'
        if name.startswith('repeat_'):
            contract=name.removeprefix('repeat_');return 'Reopens negotiations on §Y'+AGREEMENTS[contract]+'§!. Financial commitments begin only after agreement.'
        raise ValueError('Unedited decision consequence: '+key)

    def decision(self,key,body):
        out=[]
        for k,o,v in body:
            if k in ('available','visible','allowed'):out.append((k,o,self.trigger(v,inline=True)))
            elif k=='complete_effect':
                preview=self.material_effects(v)
                hint=self.P+'decision_'+key.removeprefix(self.P)+'_effect_tt';self.loc[hint]=self.decision_hint(key)
                shown=([('effect_tooltip','=',preview)] if preview else [])+[('custom_effect_tooltip','=',hint)]
                out.append((k,o,shown+[('hidden_effect','=',v)]))
            else:out.append((k,o,v))
        return out

    def clean_options(self,body):
        """Retain the existing numeric preview, conceal only its real payout."""
        out=[]
        for k,o,v in body:
            if k=='option':
                option=[]
                for a,b,c in v:
                    if a=='trigger':option.append((a,b,self.trigger(c)))
                    elif a=='effect_tooltip':
                        preview=self.trim_preview(c)
                        if preview:option.append((a,b,preview))
                    elif a.startswith(self.P) and c=='yes':option.append(('hidden_effect','=',[(a,b,c)]))
                    elif a in ('set_country_flag','clr_country_flag','set_variable','set_temp_variable'):
                        if a=='set_temp_variable' and self.first(c,'treasury_change') is not None:option.append((a,b,c))
                        else:option.append(('hidden_effect','=',[(a,b,c)]))
                    else:option.append((a,b,c))
                out.append((k,o,option))
            else:out.append((k,o,v))
        return out

    def trim_preview(self,rows):
        result=[]
        for k,o,v in rows:
            if isinstance(v,list):
                v=self.trim_preview(v)
                if k in (*COUNTRIES,'ROOT','FROM','PREV') and not v:continue
                if k in ('if','else_if','else') and not any(x[0]!='limit' for x in v):continue
            result.append((k,o,v))
        return result

    def decision_prose(self):
        paragraphs={
            'legalize_civic_parties': 'Student associations and the independent left have long operated at the margins of an anticommunist political order. Legal recognition would bring these movements into public debate and electoral competition, while requiring the government to accept organizations it cannot direct from the ministries or security services.',
            'reopen_constitutional_talks': 'Military reconsolidation has restored command without settling the question of political legitimacy. The opposition continues to demand constitutional revision. Renewing negotiations would give the government a route out of confrontation, but the officers must accept that a civilian settlement will place limits on their authority.',
            'reopen_charter_ballot': 'The rejected draft has left the constitutional question unresolved. With a negotiating mandate still intact, the parties can return their chosen text to ratification. A renewed ballot will test whether concessions and political organization have produced a majority where the earlier bargain failed.',
            'implement_constitutional_court': 'Constitutional review requires more than a place in the new charter. Judges must be appointed, staff recruited and procedures established before the court can hear a case. Funding that work will give the settlement an institution capable of reviewing the exercise of state power.',
            'review_repression_cases': 'Emergency rule has left disputed prosecutions, broken careers and families seeking answers from the state. A formal review would open the record to scrutiny and begin an accountability settlement. Its findings may restore confidence in civilian institutions while exposing officials and security networks to an uncomfortable reckoning.',
            'authorize_djp_merger': 'The Democratic Justice Party must decide whether a broader conservative alignment can secure the political order beyond military rule. Authorizing its delegation opens negotiations with Kim Young-sam’s organization and Kim Jong-pil’s conservatives, whose constituencies will expect a voice in the resulting settlement.',
            'authorize_ys_merger': 'Kim Young-sam’s organization stands between continued opposition and a negotiated place in a broader conservative party. Its leaders must weigh access to government against the risk of dividing the democratic movement. A separate mandate is needed before its delegation can bargain with the DJP and NDRP.',
            'authorize_ndrp_merger': 'Kim Jong-pil’s New Democratic Republican Party brings an established conservative network to the proposed realignment. Its delegation must decide what terms would protect that organization within a larger governing party. Authorizing talks gives it a seat at the table without settling the final agreement.',
            'open_conservative_merger': 'The participating organizations have each authorized a delegation. Their leaders can now negotiate a common party, balancing access to government, leadership claims and the survival of local networks. Kim Dae-jung’s organization remains outside this conservative bargain.',
            'authorize_military_succession': 'An unsettled succession has opened the presidency to an officer council. Backing Chun Doo-hwan would place the cabinet under an Army-led political settlement, with the promise of command continuity and the burden of a disputed civilian mandate. The decision will shape the terms of any later opening.',
            'ratify_revolutionary_settlement': 'The revolutionary party has reached government, but its accession has not settled the organization of the Southern state. Ratifying a cabinet gives the new administration a common mandate. Replacing established authority will unsettle officials, employers and communities whose cooperation remains essential to governing.',
            'form_democratic_justice_party': 'An Army-led administration needs an organization capable of contesting elections and negotiating within civilian institutions. Constituting the Democratic Justice Party gives its supporters an electoral vehicle. Officers and party organizers must now decide how much independence that organization will enjoy from the command structure.',
            'authorize_security_directorate': 'A command crisis and severe instability have weakened the authority of ordinary government. An exceptional security directorate offers a coercive answer to the succession dispute, suspending electoral competition and concentrating responsibility in the security apparatus. Its initial order will carry a lasting question of legitimacy.',
            'authorize_kjp_handover': 'The authorized civilian succession gives Kim Jong-pil a route to executive office through the conservative organization he helped build. A negotiated handover would preserve administrative continuity while redistributing authority among party figures, ministers and the military networks accustomed to presidential direction.',
            'nominate_ys': 'Kim Young-sam offers a reform leadership rooted in parliamentary opposition and the struggle for civilian politics. Registering his candidacy places that claim before the electorate. His organization must still turn a reputation for resistance into a governing coalition capable of winning office.',
            'nominate_dj': 'Kim Dae-jung’s organization seeks to carry the democratic challenge into national government. His candidacy brings a distinct constituency and programme to the reform movement, but also renews the question of opposition unity. The campaign must reconcile those ambitions with the coalition needed to win office.',
            'nominate_roh': 'The Democratic Justice Party looks to Roh Tae-woo to carry its organization into direct electoral competition. His candidacy links a negotiated opening to the institutions of the outgoing military order. Winning civilian office will require support beyond the command networks on which that order rested.',
            'nominate_kjp': 'Kim Jong-pil’s conservative organization seeks a mandate of its own through the electoral process. His candidacy offers experience in party organization and government, while asking voters to distinguish civilian continuity from the military presidency that shaped the developmental state.',
            'northern_consultation_proposal': 'Regular contacts have made a formal invitation to Seoul possible. A sovereign consultative framework could give the two Korean governments a place to negotiate practical cooperation while retaining their separate administrations. The Southern government must first decide whether it is prepared to open those talks.',
        }
        for key,paragraph in paragraphs.items():self.loc[self.P+key+'_desc']=paragraph
        interests={
            'drp':('DRP','the conservative governing organization','executive continuity and the survival of its local organization'),
            'ndp':('NDP','the parliamentary opposition','competitive elections and an Assembly capable of checking the executive'),
            'two_kim_reform':('Reform Movement','the organizations of the Two Kims','civilian government and the leadership of the democratic coalition'),
            'usp':('USP','the Unification Socialist Party','lawful social-democratic participation and enforceable labour rights'),
            'rpr':('Revolutionary Party','the legalized Southern revolutionary organization','its place in the new political settlement and the peninsula question'),
            'student_civic':('Civic Coalition','the student civic coalition','freedom of association and safeguards against renewed emergency rule'),
            'independent_left':('Independent Left','the independent Southern left','political independence and a voice for organized labour'),
            'army_djp':('Army / DJP','the Army and DJP organization','command continuity and the boundaries of a civilian opening'),
        }
        for slug,(short,organization,interest) in interests.items():
            key=self.P+'request_charter_endorsement_'+slug
            self.loc[key]='Seek '+short+' Charter Endorsement'
            self.loc[key+'_desc']='The constitutional bargain must address '+interest+'. Asking '+organization+' to endorse the draft will establish whether it accepts the negotiated terms before the text is submitted to ratification.'
            key=self.P+'withdraw_charter_endorsement_'+slug
            self.loc[key]='Withdraw '+short+' Charter Endorsement'
            self.loc[key+'_desc']='Support from '+organization+' rests on the concessions made during negotiations over '+interest+'. Withdrawing its endorsement before the ballot would reopen that dispute and remove its support from the agreed constitutional text.'
        for key,title in AGREEMENTS.items():
            id=self.P+'repeat_'+key
            if id not in self.loc:continue
            self.loc[id]='Reopen '+title+' Talks'
            # Reuse the corresponding policy's edited narrative, rather than
            # pad every diplomatic decision with the same procedural paragraph.
            owners=[n for n in self.c.d['nodes'] if any(a.get('type')=='offer' and a.get('value')==key for a in n['effects']['actions'])]
            if owners:self.loc[id+'_desc']=self.loc[owners[0]['id']+'_desc']
        self.loc[self.P+'constitutional_decisions_desc']='The settlement of civilian authority depends on the constitution, the armed forces, the courts and the political organizations asked to accept the new rules.'
        self.loc[self.P+'1970_foreign_category_desc']='Korean diplomacy must turn strategic ambitions into agreements that other governments are willing to uphold. These negotiations cover security, trade and contacts across the divided peninsula.'
        self.loc[self.P+'northern_consultation_category_desc']='The two Korean governments can build institutions for consultation while retaining their own administrations. Practical cooperation depends on reciprocal commitments and the political willingness to sustain them.'
        # Keep ballot procedure in a concise tooltip; the event itself speaks
        # in the language of the institutions deciding the country's future.
        self.loc[self.P+'transition.30.d']='The negotiated charter has been put to the political organizations entitled to participate in ratification. Their recorded endorsements determine whether the draft commands a majority and whether the settlement can proceed to electoral administration.'
        self.loc[self.P+'transition.30.option_a']='Record the Ratification Result'
        self.loc[self.P+'owner_programme_tt']='Applies while this party or leader governs.'

    def focus_notes(self):
        hints={
            'resolve_command_challenge':'Opens a decision on the command dispute.',
            'submit_constitutional_ballot':'Begins a §Y30-day§! constitutional ballot. Ratification requires more than half of eligible parties’ combined support.',
            'configure_lawful_election':'Establishes electoral administration and opens the campaign under the ratified constitution.',
            'open_constitutional_dossier':'Opens the constitutional negotiation process.',
            'legal_civic_associations':'Legalizes student civic and independent left organizations.',
            'confirm_native_handover':'Confirms the transfer following a resolved constitutional election.',
            'constitutional_review_rules':'Establishes the court’s mandate. Funded appointments and commissioning are required before it opens.',
            'conservative_merger':'The coalition settlement takes effect after the participating parties ratify their agreement.',
            'yushin_institutions':'Enacts the Yushin constitutional settlement.',
            'constitutional_reform_commitment':'Commits the government to an electoral and constitutional opening.',
            'managed_succession':'Authorizes a managed succession within the conservative governing organization.',
            'open_succession':'Authorizes a civilian succession.',
            'restore_civil_liberties':'Establishes a commitment to civil liberties.',
            'parliamentary_republic':'Commits the party to a parliamentary republic.',
            'presidential_term_limits':'Commits the party to constitutional limits on the presidency.',
            'intelligence_oversight':'Authorizes civilian oversight of intelligence operations.',
            'political_prisoner_review':'Authorizes a review of political prisoners’ cases.',
            'confirm_constitutional_settlement':'Confirms the ratified constitutional settlement.',
            'nordpolitik_negotiations':'Authorizes negotiations with the Soviet Union and China.',
            'controlled_constitution':'Establishes the controlled Fifth Republic settlement.',
            'open_constitutional_negotiations':'Authorizes a negotiated political opening.',
            'accept_direct_election_principle':'Accepts direct presidential elections in principle.',
            'independent_union_law':'Recognizes lawful collective bargaining.',
            'socialist_international_contacts':'Authorizes contacts with international social-democratic organizations.',
            'civic_pluralism':'Commits the civic coalition to political pluralism.',
            'left_pluralism':'Commits the revolutionary government to a pluralist settlement.',
            'southern_ratification':'Records Southern approval of the negotiated settlement.',
            'civilian_transition_agreement':'Accepts the terms of a civilian transition.',
            'political_case_review':'Authorizes scrutiny of politically motivated cases.',
            'security_transition_terms':'Accepts negotiated terms for a transition from security rule.',
            'bind_electoral_succession':'Commits the administration to electoral succession.',
            'independent_repression_inquiry':'Authorizes an independent inquiry into political repression.',
            'register_charter_participants':'Registers the negotiating organizations for the constitutional settlement.',
            'preserve_case_records':'Preserves the records required for independent investigation.',
            'conditional_disclosure_compact':'Establishes conditional disclosure as the basis for the accountability bargain.',
            'ratify_negotiating_mandate':'Confirms the negotiating mandate for a constitutional draft.',
            'register_native_labor_faction':'Recognizes organized labour in the political settlement.',
            'prepare_local_autonomy_law':'Prepares the legal framework for local autonomy.',
            'constitutional_party_guarantees':'Records the civilian parties’ constitutional guarantees.',
            'inter_korean_channels':'Authorizes official inter-Korean contacts.',
            'extend_social_insurance':'Establishes the social-insurance framework.',
            'publish_treaty_obligations':'Authorizes publication of the country’s treaty obligations.',
            'sector_investment_priority':'Authorizes a review of industrial investment priorities.',
            'verify_korean_signatures':'Records the verification of both Korean governments’ signatures.',
            'existing_guest_worker_contracts':'Bilateral worker agreements and overseas placements determine remittance income.',
            'energy_project_options':'Energy development remains subject to its construction, supply and financing requirements.',
            'existing_civil_nuclear_projects':'Nuclear development requires research, funded construction, fuel and safeguards.',
            'existing_energy_purchase_options':'Energy imports require a funded supply agreement.',
        }
        for name,text in hints.items():self.loc[self.P+'action_'+name+'_tt']=text
        for n in self.c.d['nodes']:
            for policy in n['effects']['policies']:
                if n['effects']['weekly']:self.loc[n['id']+'_weekly_tt']='Policy upkeep: §R'+money(n['effects']['weekly'])+'/week§!'
                condition=policy.get('active_condition','')
                key=n['id']+'_conditional_tt'
                if not condition:continue
                if condition.startswith('accepted '):self.loc[key]='Requires an active §Y'+AGREEMENTS[condition[9:]]+'§! agreement.'
                elif n['key']=='independent_constitutional_court':self.loc[key]='Takes effect once the court is commissioned under constitutional government.'
                elif n['key']=='conservative_merger':self.loc[key]='Requires ratification by the participating party organizations.'
                else:self.loc[key]='Requires the constitutional settlement to remain in force.'

    def remove_empty_notes(self,rows):
        out=[]
        for k,o,v in rows:
            if k=='custom_effect_tooltip' and self.loc.get(v)=='Implements the associated institutional measures under their stated political and legal conditions.':continue
            out.append((k,o,self.remove_empty_notes(v) if isinstance(v,list) else v))
        return out

    def apply(self):
        self.prose()
        self.focus_notes()
        for path,code in self.c.files.items():
            if not path.endswith('.txt'):continue
            rows=self.parse(code)
            if path.startswith('common/scripted_triggers/'):
                rows=[(k,o,self.trigger(v)) for k,o,v in rows]
            elif path.startswith('common/decisions/') and '/categories/' not in path:
                rows=[(cat,o,[(key,p,self.decision(key,body)) for key,p,body in category]) for cat,o,category in rows]
            elif path.startswith('common/decisions/categories/'):
                rows=[(cat,o,[(k,p,self.trigger(v,inline=True) if k in ('visible','allowed','available') else v) for k,p,v in category]) for cat,o,category in rows]
            elif path.startswith('events/'):
                rows=[(k,o,self.clean_options(v) if k in ('country_event','news_event') else v) for k,o,v in rows]
            elif path.startswith('common/national_focus/'):
                rows=self.remove_empty_notes(rows)
            else:continue
            self.c.files[path]='# IMPERIA CW — Cold War: South Korean presentation.\n'+self.emit(rows)+'\n'
        self.decision_prose()
        # Existing focus wrappers reference the same keys. Replace their old
        # generic inverse text even if a focus alone was the original writer.
        for key in list(self.loc):
            if key.startswith(self.P+'require_') and key.endswith('_tt'):
                name=key[len(self.P+'require_'):-3]
                flag=name if name.startswith('COLDWAR_NKO_') else self.P+name
                self.loc[key],self.loc[key+'_NOT']=self.flag_pair(flag)
