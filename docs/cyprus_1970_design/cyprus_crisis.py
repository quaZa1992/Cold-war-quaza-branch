"""Research-led road to the1974 war. All events/adapters remain design contracts."""

def add_crisis(section,focus,either,exclusive,spirit):
    spirit('armed_enosis_opposition','The Armed Enosis Underground',
           {'stability_factor':-.03,'political_power_factor':-.05},
           note='January1970: the National Front and other armed opponents challenge Makarios. This is not EOKA B before its1971 formation and is not a penalty for Greek Cypriot ethnicity. Civilian security reform, disarmament or an explicit regime change determine its later course.')
    section('road_to_war','The Road to the Cyprus War',(6,14),
            'A broken constitutional partnership is the background; Greek military influence, armed opposition and the1974 coup are distinct escalation mechanisms. Turkey and other players choose their own responses. Peace is possible.')
    nodes=[]
    def f(key,title,xy,parents=(),pressure=0,**opts):
        node=focus('war_'+key,title,'road_to_war',xy,['war_'+p for p in parents],**opts)
        node['coup_pressure_delta']=pressure
        node['crisis_content']=True;nodes.append(node)
        return node
    def join(node,*parents):return either(node,*['war_'+p for p in parents])
    def x(a,b):exclusive('war_'+a,'war_'+b)

    f('pressures','A Republic between Armed Patrons',(0,0),days=10,
      note='The armed underground and divided chain of command are visible starting problems. Initialise coup pressure45 once; communal tension remains a DIFFERENT track. Pressure is a balance variable, not a historical percentage chance.')
    f('underground','Investigate the Armed Underground',(0,1),['pressures'],cost=.5,days=35,
      note='The8March1970 attempt on Makarios is a conditional historical event; contemporary reports did not establish every perpetrator. No EOKA B label before1971, no automatic foreign-policy conversion.')
    f('civilian_guard','Assert Civilian Authority over the Guard',(-4,2),['underground'],cost=1,pressure=-10,
      event='war_civilian_command',note='Begin replacing divided command with accountable institutions. Request withdrawal/reassignment of outside officers through an actual Greek response; training expertise is not silently replaced.')
    f('mainland_command','Retain the Mainland Command Structure',(4,2),['underground'],pressure=10,
      mods={'foreign_influence_defense_modifier':-.04},note='Keep expertise and political dependence. Existing retained-officer organisation rewards are not granted a second time.')
    x('civilian_guard','mainland_command')
    f('domestic_security','Build an Accountable Domestic Security Chain',(-4,3),['civilian_guard'],cost=1,pressure=-15,
      note='Professionalise police and guard command without suppressing an ethnic population. Reduce underground influence only if disarmament/command outcomes are implemented.')
    f('junta_links','Bind the Officer Corps to the Greek Junta',(4,3),['mainland_command'],pressure=15,
      event='war_junta_patronage',requires='A military junta actually governs Greece and agrees to sponsor the network.',
      note='Not every Greek government or officer supports a coup. If Greece democratises or refuses, no sponsor flag or donated weapons appear.')
    join(f('command_dispute','The Greek–Cypriot Command Dispute',(0,5),days=35,
           note='Makarios\'2July1974 letter demanding removal of mainland officers is a historical milestone if the unresolved command dispute still exists; an earlier settlement can avert that confrontation.'),'domestic_security','junta_links')
    f('officer_agreement','Negotiate an Officer Withdrawal',(-4,6),['command_dispute'],cost=.5,pressure=-10,event='war_officer_withdrawal',
      note='Greece can accept, negotiate or refuse. Removing officers by decree does not itself remove a clandestine armed network; provide a command transition.')
    f('plot','Organise against the Presidency',(4,6),['command_dispute'],cost=.5,pressure=15,event='war_coup_preparation',
      requires='A formed pro-Enosis opposition/sponsor network; a current president cannot organise a coup against himself as a free reform.',
      note='For a Makarios player this is an opposition/foreign-sponsored threat handled by events. A hardline political route or an explicitly authorised sponsored plot may advance it.')
    x('officer_agreement','plot')
    f('loyal_guard','A Guard Loyal to the Republic',(-4,7),['officer_agreement'],cost=1,pressure=-15,
      requires='An implemented command transition and withdrawal/retirement agreement; not merely an unanswered letter.',
      note='Conditional removal of the armed-underground pressure spirit after sustained lawful disarmament. Existing divided-command reforms use the same one-time ledger.')
    f('putsch','Commit to the Putsch',(4,7),['plot'],days=10,pressure=10,event='war_coup_resolution',
      requires='Actual sponsor/plot organisation, vulnerable command and date>=1971 for EOKA B stage; historical schedule15July1974 only while the required conditions survive.',
      note='Resolve coup success, failure and constitutional resistance. Sampson is installed only after a successful historical-style coup; Makarios escape/succession is an event outcome, not a guaranteed assassination.')

    # An externally triggered coup or severe renewed violence can open this
    # conditional root even if the CYP player never chose a plotting focus.
    f('guarantors','The Guarantors Respond',(0,10),days=10,event='war_guarantor_consultation',
      requires='Successful unconstitutional coup OR unilateral Enosis OR independently verified grave renewed communal violence; a routine unresolved constitutional dispute alone is insufficient.',
      note='Turkey considers guarantees, security and diplomacy; Greece and Britain have independent responses. A CYP focus cannot select a Turkish declaration of war.')
    f('conference','Seek a Joint Guarantor Conference',(-4,11),['guarantors'],cost=.5,event='war_joint_guarantor_offer',
      note='Historic Turkish approaches to Britain are represented as genuine proposals. Joint action is not assured; a refusal does not mean Britain has accepted unilateral territorial partition.')
    f('defy','Reject the Guarantor Ultimatum',(4,11),['guarantors'],tension=10,event='war_ultimatum_refusal',
      note='A confrontational government can reject terms. Turkey still chooses mediation, an ultimatum, limited intervention or a broader operation; no compulsory war.')
    x('conference','defy')
    f('restore','Restore Constitutional Government',(-4,12),['conference'],cost=.5,event='war_constitutional_restoration',
      note='A coup regime can step down, or resistance can restore constitutional authority. This removes the coup pretext only after real restoration; civilian harms and other disputes remain.')
    f('prepare_intervention','Prepare for Foreign Intervention',(4,12),['defy'],cost=1,
      mods={'army_defence_factor':.03},duration=180,event='war_turkish_intervention_choice',
      note='Temporary defensive preparation, not the right to dictate another player\'s military action. Combat requires valid OOBs, transports, landing technology, bases and supply; the current scenario deliberately defers those forces.')
    f('july_ceasefire','Answer the July Ceasefire Appeal',(0,14),days=10,event='war_july_ceasefire',
      requires='A real first-phase intervention/combat outcome or an explicitly labelled abstract crisis phase. First historical landing20July; initial ceasefire22July1974.',
      note='No instant transfer of all state146. A ceasefire flag alone cannot stop engine combat; the scenario needs a tested stop-combat/ownership-preserving adapter. Do not invoke the generic MD territorial ceasefire or720-day white-peace path blindly.')
    f('geneva','Negotiate a Settlement at Geneva',(-4,15),['july_ceasefire'],cost=.5,event='war_geneva_negotiation',
      note='Separate30July first-Geneva arrangements from the8–14August second conference. Require real negotiations and accept/refuse choices; the first ceasefire is not final ownership or1983 independence.')
    f('remobilise','Refuse Terms and Remobilise',(4,15),['july_ceasefire'],cost=1,event='war_remobilisation',
      note='A party can reject the proposed settlement, but the second Turkish offensive remains a Turkish decision. Disputes over constitutional models, troop positions and security can sustain a crisis.')
    x('geneva','remobilise')
    join(f('august','The August Decision',(0,17),days=10,event='war_august_decision',
           requires='First phase completed; no accepted and implemented final settlement; diplomacy failed or an agreed deadline expires.',
           note='Historical second offensive14–16August1974 is distinct from the20July landing. No automatic second war after a durable accepted agreement.'),'geneva','remobilise')
    f('monitored_settlement','Accept a Monitored Political Settlement',(-4,18),['august'],cost=.5,event='war_final_settlement',
      note='Both communities and applicable external parties decide. Any agreed demarcation and withdrawal follows actual terms; no unconsented annexation or property extinguishment.')
    f('military_settlement','Fight for a Military Settlement',(4,18),['august'],cost=1,event='war_second_phase_combat',
      requires='The relevant sovereign player actually chooses renewed combat; ceasefire/truce adapter permits it; military readiness exists.',
      note='War outcomes, occupation, atrocities, missing persons and displacement are tracked separately from victory. Capturing a state never grants a productivity, manpower or tax bonus for expelling civilians.')
    x('monitored_settlement','military_settlement')
    # Reactive actor choices run on the crisis clock, not the focus clock.
    # The focus records the event outcome; one guarded payload owns all effects.
    reactive={'putsch','guarantors','conference','defy','restore','prepare_intervention',
              'july_ceasefire','geneva','remobilise','august','monitored_settlement','military_settlement'}
    for node in nodes:
        if node['key'][4:] in reactive:
            node['execution_mode']='event_milestone'
            node['note']+=' Fast actor-response milestone: events or short decisions resolve this choice independently of the displayed focus duration. Record it with complete_national_focus only after the result is applied once; do not duplicate payment, pressure changes or dispatch.'
    return {
      'sources':['WAR_HISTORY.md','WAR_MECHANICS.md'],
      'pressure_variable':'COLDWAR_CYP_1970_coup_pressure','starting_coup_pressure':45,
      'causal_chain':['1963constitutional rupture and civilian harms','uneven normalisation by1969–70',
                     '1970NationalFront/armed underground','1971EOKAB and Greek-junta links',
                     'unresolved military-command dispute','conditional15July1974 coup',
                     'Turkish/Greek/British decisions','20July first landing','22July ceasefire',
                     'Geneva negotiations','conditional14August second offensive','postwar humanitarian/political outcomes'],
      'war_is_avoidable':True,
      'selected_phase_model':'Current-map design: explicitly abstract the limited July foothold and negotiation phase without whole-state transfer or a pretend engine ceasefire. A later real engine offensive remains gated by actual force/readiness setup; final territory follows real results or accepted terms.',
      'reaction_clock':'Preparation focuses use their displayed duration. Reactive milestones are resolved by actor events/short decisions on the crisis clock, then recorded once using the real complete_national_focus effect. Never block the July20 response behind a35-day focus.',
      'payload_rule':'Each crisis instance has one outcome-applied ledger. The actor event owns costs and effects; focus completion only records the result. No invented reward=no parameter and no duplicate rewards or ultimata.',
      'engine_limits':['TUR and CYP1970 OOBs are deliberately empty; no functioning invasion is claimed.',
                       'States145 and146 each contain only one province; a July Kyrenia beachhead cannot be represented as control of all146.',
                       'NCY has cores on145/146/812; blind release risks the wrong territory.',
                       'Generic MD ceasefire/whitepeace may transfer ownership and impose720-day truce; use a bespoke tested adapter.'],
      'phase_rules':['No war simply because Turkish Cypriots exist.',
                     'Coup pressure and communal tension are independent bounded tracks.',
                     'No compulsory1974 war if causes have been addressed; historical dates are conditional milestones.',
                     'The Turkish player retains its intervention decision; the CYP player retains its response.',
                     'No sovereignty transfer, mass population change or free modern units on the first-landing event.']}
