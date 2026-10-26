# IMPERIA CW — Cold War: iraq 1970 concept — iran war.
"""COLDWAR_IRQ: proposed Iran escalation content; no live files are written here."""
import re

# Relative to the sector root (94,15); connections use the same model as the specimen.
GEOMETRY = [
    (0,0,[]), (-2,1,[[0]]), (2,1,[[0]]),
    (-2,2,[[1]]), (2,2,[[2]]), (0,3,[[3],[4]]),
    (-2,4,[[5]]), (2,4,[[5]]), (-2,5,[[6]]), (2,5,[[7]]),
    (-4,6,[[8]]), (-2,6,[[8]]), (2,6,[[9]]), (4,6,[[9]]),
    (0,7,[[11,12]]), (-2,8,[[14]]), (2,8,[[14]]), (0,9,[[15,16]]),
    (-2,10,[[17]]), (2,10,[[17]]),
    (-4,11,[[18]]), (-2,11,[[18]]), (2,11,[[19]]), (4,11,[[19]]),
    (-2,12,[[20],[21]]), (2,12,[[22],[23]]),
    (-2,13,[[24]]), (-4,14,[[26]]), (0,14,[[26]]), (-2,15,[[27,28]]),
]
EXCLUSIONS = {6:[7],7:[6],27:[28],28:[27]}

IDEAS = {
    'COLDWAR_IRQ_iran_opening_offensive': dict(
        label='The Southern Offensive',
        description='Prepared attacks against Iranian forces have a short operational window. Fuel and supply costs affect the entire Iraqi army. Peace ends the advantage; it never restarts.',
        modifier=dict(planning_speed=.15,supply_consumption_factor=.08,army_fuel_consumption_factor=.10),
        targeted_modifier=dict(tag='PER',attack_bonus_against=.08),cancel_peace=True,days=90),
    'COLDWAR_IRQ_iran_sustained_offensive': dict(
        label='A Prepared Iranian Campaign',
        description='A larger reserve supports a longer opening operation, with a smaller attack advantage and continuing logistical costs.',
        modifier=dict(planning_speed=.10,supply_consumption_factor=.05,army_fuel_consumption_factor=.06),
        targeted_modifier=dict(tag='PER',attack_bonus_against=.05),cancel_peace=True,days=120),
    'COLDWAR_IRQ_iran_mobilization_bill': dict(
        label='The Mobilization Bill',
        description='Personnel and transport obligations remain payable even if the initial campaign ends early.',
        modifier=dict(army_personnel_cost_multiplier_modifier=.08),days=180),
    'COLDWAR_IRQ_iran_disarray_assessment': dict(
        label='Intelligence on Iranian Disarray',
        description='A funded assessment of an actual Iranian political crisis accelerates planning. It does not weaken Iranian units or guarantee local cooperation.',
        modifier=dict(planning_speed=.10),days=120),
    'COLDWAR_IRQ_iran_attrition_bill': dict(
        label='A War Beyond the First Campaign',
        description='After 180 continuous days at war with Iran, replacement, transport and political burdens grow. This burden ends at peace.',
        modifier=dict(supply_consumption_factor=.08,army_personnel_cost_multiplier_modifier=.12,stability_factor=-.04),cancel_peace=True),
    'COLDWAR_IRQ_iran_followup_offensive': dict(
        label='A Renewed Southern Offensive',
        description='Another paid offensive offers a smaller advantage against Iran, at higher logistical strain. It cannot overlap the opening or another renewed offensive.',
        modifier=dict(supply_consumption_factor=.12,army_fuel_consumption_factor=.12),
        targeted_modifier=dict(tag='PER',attack_bonus_against=.05),cancel_peace=True,days=60),
    'COLDWAR_IRQ_iran_followup_bill': dict(
        label='Replacement and Transport Contracts',
        description='The renewed offensive leaves ninety days of personnel obligations, including after an early peace.',
        modifier=dict(army_personnel_cost_multiplier_modifier=.12),days=90),
}

def populate(G,I,M,D):
    def prose(s):
        return re.sub(r'(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])|(?<=%)(?=[A-Za-z])',' ',s)
    def e(key,title,story,**kw):
        if kw.get('outcomes'):kw['outcomes']=[prose(s) for s in kw['outcomes']]
        if kw.get('historic'):kw['historic']=prose(kw['historic'])
        return I(key,prose(title),prose(story),**kw)
    def d(key,title,cost,days,summary,**kw): return D(key,prose(title),cost,days,prose(summary),**kw)
    claim_conditions=['Iran owns Khuzestan; Iraq is independent, outside Irans faction and not at war with Iran']
    campaign='National campaign programme. Claims and paid buildings persist; war, territorial and timed packages have their own current eligibility. No party switch replays deliveries.'
    opening=d('iran_opening','Launch the Khuzestan Offensive',75,0,
        'Once per campaign history, after the offensive focus and within the first30days of the first Iraqi-Iranian war. Pay a frozen2%GDP invoice. Short-war plan: +8%attack against PER, +15%planning speed, +8%supply use and +10%army fuel use for90days. Sustained plan: +5%attack against PER, +10%planning speed, +5%supply use and +6%army fuel use for120days. Both create a180day +8%army personnel bill that survives early peace. Attack is PER-targeted; planning and logistical effects are country-wide. No automatic declaration.',
        budget_gdp_share=.02,repeatable=False,
        eligibility='has_war_with = PER; earned iran_launch_campaign; first-war window open; no COLDWAR_IRQ_iran_opening_used flag; invoice affordable',
        effect_code='''# NEW transaction/window integration: apply only after all eligibility and frozen-invoice checks pass.
# Native payload; the shared consumed flag is permanent and never cleared on peace or a party change.
if = {
 limit = { has_country_flag = COLDWAR_IRQ_iran_short_war_implemented }
 add_timed_idea = { idea = COLDWAR_IRQ_iran_opening_offensive days = 90 }
}
else = { add_timed_idea = { idea = COLDWAR_IRQ_iran_sustained_offensive days = 120 } }
add_timed_idea = { idea = COLDWAR_IRQ_iran_mobilization_bill days = 180 }
set_country_flag = COLDWAR_IRQ_iran_opening_used
clr_country_flag = COLDWAR_IRQ_iran_campaign_window_open''')
    G('iran_war','Iran: Road to War','shared',None,'tag = IRQ',campaign,[
        e('iran_frontier','The Iranian Frontier','The1969river dispute is a live1970crisis. Prepare a coercive policy toward Iran while Iraqi state capacity is still limited.',cost=3,m=M(pp=.03,admin=.02),icon='army_reform',historic='Historical river crisis1969; this campaign is a player choice',
          decisions=[d('iran_frontier_review','Review the Eastern Balance',25,30,'Expose actual Iranian stability, war status, owned Khuzestan and the Iraqi northern burden. Never manufacture an Iranian revolution or a loyal Arab uprising.')]),
        e('iran_shatt_demand','Enforce the Shatt Claim','Assert Baghdad\'s demand for river control. If a border agreement was actually signed, later repudiation must end its reciprocal benefits.',cost=3,m=M(pp=.04,st=-.02),icon='army_reform',
          outcomes=['A hardline river policy; no free ownership of either riverbank. A signed settlement must be repudiated before the ultimatum.'],
          decisions=[d('iran_revoke_settlement','Repudiate the Border Settlement',75,0,'Available only for an actual live Iran border settlement. Clear that agreement and its reciprocal benefits, restore the unresolved-river burden and notify Iran. This is a unilateral hostile act; Iran cannot veto its repudiation. It does not create a second claim or force war.',proposed_provider='COLDWAR_IRQ_revoke_actual_iran_settlement')]),
        e('iran_arabistan_claim','The Arabistan Claim','Publicly demand Khuzestan, described as Arabistan by Iraqi nationalists. The population is not automatically Iraqi, loyal or consenting.',cost=3,requires=claim_conditions,icon='oil_production2',
          instant=['add_state_claim = 399','add_war_support = 0.05'],
          outcomes=['Gain a CLAIM on Khuzestan (state399), plus5percentage points of war support. No core, ownership transfer, resources or local uprising.'],historic='Historical disputed Iraqi demand; Khuzestan is Iranian in January1970'),
        e('iran_southern_command','Rebuild Southern Command','Professional command and river-crossing exercises create a force capable of attempting a southern offensive.',cash=.02,xp=20,m=M(org=.04,milcost=.04),icon='army_reform'),
        e('iran_tehran_assessment',"Assess Tehran's Army",'Reconnaissance separates Iranian capabilities from Iraqi expectations. Revolutionary weakness is an opportunity only when it actually exists.',cost=3,cash=.005,icon='government_beu',
          decisions=[d('iran_disarray','Exploit Iranian Disarray',50,0,'Once only; Iran must actually have civil war or stability below40%. Cost1%frozenGDP. Planning speed +10%for120days. This optional opportunity is not needed to obtain the war goal.',budget_gdp_share=.01,repeatable=False,
            eligibility='country_exists = PER; PER = { OR = { has_civil_war = yes has_stability < 0.40 } }; NOT = { has_country_flag = COLDWAR_IRQ_iran_disarray_used }',
            effect_code='# After the common once-only paid transaction:\nadd_timed_idea = { idea = COLDWAR_IRQ_iran_disarray_assessment days = 120 }\nset_country_flag = COLDWAR_IRQ_iran_disarray_used')]),
        e('iran_operational_plan','The Southern War Plan','Combine command preparation and intelligence into a costed campaign plan. Iranian fragmentation is a possibility, not a victory condition.',cash=.015,m=M(supply=-.05,admin=.03),icon='focus_generic_supply_line'),
        e('iran_short_war','A Short Sharp War','Concentrate the prepared force for a rapid attempt to break into Khuzestan. If the opening fails, the initial advantage will be gone.',icon='army_reform',
          instant=['set_country_flag = COLDWAR_IRQ_iran_short_plan'],outcomes=['Select the90day opening profile: +8%attack against PER and +15%planning speed; +8%supply and +10%fuel consumption during it. Paid activation is unlocked later. Exclusive with the sustained-war plan.']),
        e('iran_sustained_war','Prepare a Long War','Sacrifice civilian priorities for a deeper reserve and a longer, less concentrated opening operation.',m=M(out=.08,eff=.04,research=-.03,milcost=.06),active_requires=['Actual active war against Iran'],icon='crane_and_tower',
          instant=['set_country_flag = COLDWAR_IRQ_iran_sustained_plan'],outcomes=['Select the120day opening profile: +5%attack against PER and +10%planning speed; +5%supply and +6%fuel consumption during it. Paid activation is unlocked later. Production package activates only during war with Iran.']),
        e('iran_fuel_spares','Fuel and Spares','A funded reserve and maintenance programme improves army fuel discipline. Imports and storage require administrators.',cash=.03,xp=10,m=M(fuel=-.06,admin=.03),icon='focus_generic_supply_line'),
        e('iran_mobilisation_base','Build the War Reserve','Fund one military factory in Salahuddin as the physical base of a sustained campaign.',cash=.05,build=(167,'arms_factory',1),cost=7,m=M(milcost=.03),icon='crane_and_tower'),
        e('iran_gulf_credit','Seek Gulf Backing','Seek external finance against the perceived Iranian threat. The attack route remains open if the Gulf refuses.',cost=3,icon='diplomatic_treaty',
          decisions=[d('iran_gulf_credit','Request Gulf War Credit',60,90,'Select a real Gulf creditor. Terms, amount, Iraqi debt, repayment and creditor treasury debit require recipient acceptance. Refusal cannot block the ultimatum. No free oil, loans or divisions.',proposed_provider='COLDWAR_IRQ_offer_actual_gulf_war_credit')]),
        e('iran_forward_depots','Forward Supply Depots','Pay for transport coordination and supply organization before committing the army.',cash=.025,m=M(supply=-.05,admin=.04),icon='focus_generic_supply_line'),
        e('iran_war_contracts','Mobilise War Contracts','Prepared production contracts accelerate replacement at the cost of civilian taxation and priorities.',cash=.025,m=M(eff=.05,tax=-.03),active_requires=['Actual active war against Iran'],icon='crane_and_tower'),
        e('iran_supplier_access','Secure Foreign Spares','Seek maintenance and purchase arrangements with actual suppliers, keeping the route independent of their answer.',cost=3,icon='diplomatic_treaty',
          decisions=[d('iran_supplier','Negotiate a Wartime Supply Contract',60,60,'Choose a current eligible arms supplier and actual equipment. Acceptance, treasury, availability and delivery use native trade/arms systems. No free equipment or Soviet commitment is assumed.',proposed_provider='COLDWAR_IRQ_offer_actual_wartime_supply_contract')]),
        e('iran_final_ultimatum','The Final Ultimatum','Demand the claimed province and prepare to enforce the demand. The focus grants a concrete conquest war goal; the Iraqi player chooses the declaration.',cost=3,requires=claim_conditions+['Iraq holds the Khuzestan claim; no live accepted Iran border settlement'],icon='army_reform',
          instant=['set_temp_variable = { wargoal_on = PER }','set_temp_variable = { wargoal_type = 2 }','add_threat_from_wargoal_effect = yes','create_wargoal = { type = take_state_focus target = PER generator = { 399 } expire = 180 }'],
          outcomes=['Conquest war goal against Iran for Khuzestan (399), expiring after180days. Native world-tension and declaration rules apply. Iranian refusal is not a prerequisite; no imposed peace or ownership transfer.']),
        e('iran_launch_campaign','Execute the War Plan','Complete this preparation before declaring war, then activate the one-use offensive within its real campaign window.',cost=3,icon='army_reform',decisions=[opening],
          outcomes=['Unlock Launch the Khuzestan Offensive: a paid, one-use PER-targeted opening bonus. If the first30days are missed, the opportunity expires permanently.']),
        e('iran_home_front','Mobilise the Nation','Pay to sustain recruitment, services and public mobilization. Domestic coercion does not erase Iraqi political divisions.',cash=.02,m=M(st=-.03,social=.04),active_requires=['Actual active war against Iran'],icon='government_beu',
          instant=['add_war_support = 0.06'],outcomes=['One-time +6percentage points of war support. This does not make Iraqi Shia disloyal or Iranian Arabs loyal by default.']),
        e('iran_campaign_accounts','The Campaign Ledger','A campaign can be won, prolonged or lost. After180continuous days against Iran, an automatic attrition burden raises supply use by8%, army personnel costs by12% and reduces stability by4points until peace.',cost=3,cash=.005,requires=['Recorded Iraqi-Iranian war participation'],icon='balance_buget',
          outcomes=['The long-war burden is an automatic campaign rule, independent of whether this focus is completed. Opening bonuses expire; the mobilization bill remains payable for its full180days.']),
        e('iran_secure_khuzestan','Secure Khuzestan','A controlled province needs roads, a functioning administration and forces. Capture is not legal ownership and does not make the population a core.',cash=.015,requires=['Iraq controls Khuzestan'],m=M(st=.03,admin=.04),active_requires=['Iraq controls Khuzestan'],icon='government_beu',
          outcomes=['Existing oil and ports become a real strategic prize through native occupation, infrastructure and eventual peace terms; no duplicate resource grant.']),
        e('iran_long_war','Fight Through Attrition','If Iran does not collapse, commit to another campaign rather than receiving an automatic ceasefire.',cost=3,requires=['Iraq has fought Iran continuously for at least90days'],icon='army_reform',
          outcomes=['Open the sustained-war continuation. Khuzestan can still be captured later; no focus forces peace or Iranian surrender.']),
        e('iran_oil_rehabilitation','Khuzestan Oilworks','After Iraq legally owns and controls the province, fund one infrastructure level. National export administration improves only after the province also reaches infrastructure3.',cash=.04,build=(399,'infrastructure',1),cost=7,requires=['Iraq owns and controls Khuzestan'],m=M(oil=.10,admin=.06),active_requires=['Iraq owns and controls Khuzestan with infrastructure at least3'],icon='oil_production2',
          outcomes=['Conditional NATIONAL oil export revenue multiplier +10%; bureaucracy expenditure +6%. This is not10%more provincial output or guaranteed total income. Native oil price, occupation, damage and embargo limits remain. If this project only raises infrastructure1 to2, build the final level normally before the programme activates.']),
        e('iran_civil_administration','Administer Arabistan','Recruit and fund a civilian administration rather than promising an effortless annexation. The core status of Khuzestan does not change.',cash=.025,requires=['Iraq owns and controls Khuzestan; it remains a non-core'],m=M(admin=.05),active_requires=['Iraq owns and controls Khuzestan'],icon='government_beu',
          instant=['399 = { add_compliance = 5 }'],outcomes=['One-time +5percentage points of local compliance; existing occupation mechanics and their costs continue.']),
        e('iran_war_of_reserves','An Army of Reserves','Mobilize a deeper pool and maintain trained units at the expense of specialists and the civilian budget.',cash=.025,m=M(org=.04,man=.05,milcost=.12,research=-.03),requires=['Actual active war against Iran'],active_requires=['Actual active war against Iran'],icon='army_reform'),
        e('iran_another_offensive','Prepare Another Blow','Further offensives must be supplied, paid and scheduled. They do not reset the opening campaign.',cost=3,requires=['Actual active war against Iran'],icon='focus_generic_supply_line',
          decisions=[d('iran_followup','Fund a Renewed Offensive',100,0,'After the opening has ended and at least90days of actual war. Pay a frozen3%GDP invoice; +5%attack against PER for60days, with +12%supply and +12%army fuel use. A separate +12%army personnel bill lasts90days even after peace.180day cooldown; no overlapping opening/follow-up bonus or previous follow-up bill. Earlier mobilization bills may still be payable.',budget_gdp_share=.03,repeatable=True,cooldown=180,
            eligibility='has_war_with = PER;90continuous war days; NOT any opening/followup idea or followup bill; frozen invoice affordable',
            effect_code='# After the common eligible, non-overlapping paid transaction:\nadd_timed_idea = { idea = COLDWAR_IRQ_iran_followup_offensive days = 60 }\nadd_timed_idea = { idea = COLDWAR_IRQ_iran_followup_bill days = 90 }')]),
        e('iran_regional_power','Arabistan Secured','A successful war and actual peace settlement can deliver territory, ports, existing oil and a stronger regional position. Iran is not automatically puppeted or disarmed.',cost=7,requires=['Iraq owns and controls Khuzestan and is at peace with Iran'],m=M(influence=.08,admin=.03),active_requires=['Iraq owns and controls Khuzestan'],icon='oil_production2',
          instant=['add_political_power = 100'],outcomes=['One-time +100political power after real territorial success and peace. Foreign influence +8% and bureaucracy cost +3% remain conditional on holding the province.']),
        e('iran_no_easy_exit','Victory at Any Cost','Escalate the industrial commitment if the war lasts. The state gains replacement output by displacing civilian consumption and exhausting legitimacy.',cost=7,cash=.04,requires=['Iraq has fought Iran continuously for at least180days'],m=M(out=.10,cg=.05,milcost=.15,st=-.05),active_requires=['Actual active war against Iran'],icon='crane_and_tower',
          decisions=[d('iran_war_aims','Revise the War Aims',80,30,'Choose continued prosecution, a new offensive or a limited negotiated offer. Iran may refuse settlement; no forced peace, claim removal or free debt relief. Ending the war suspends emergency bonuses and attrition, while fixed-duration bills still expire on their original dates.')]),
        e('iran_provincial_settlement','A Provincial Settlement','Begin the political and administrative integration of conquered Khuzestan. A durable Iraqi province needs functioning institutions and a sustained hold beyond the military campaign.',cost=7,cash=.02,m=M(admin=.02,pp=-.02),requires=['Iraq owns and controls Khuzestan and is at peace with Iran'],active_requires=['Iraq owns and controls Khuzestan'],icon='focus_generic_court',historic='Alternate-history integration programme; not a historical Iraqi core',
          outcomes=['Begins the integration continuation. The730day ownership/control clock starts when Iraq actually acquires and controls the state, even before this focus. Losing ownership or control resets that clock.']),
        e('iran_equal_citizenship','Equal Citizenship','Fund equal citizenship, local access to public services and protected Arabic and Persian use in provincial administration. Wider inclusion has a continuing administrative and social-service bill.',cost=7,cash=.04,m=M(admin=.06,social=.04),requires=['Iraq owns and controls Khuzestan; it remains a non-core'],active_requires=['Iraq owns and controls Khuzestan'],icon='focus_generic_court',historic='Alternate-history civic integration choice',
          instant=['399 = { add_compliance = 12 }'],outcomes=['One-time +12percentage points of local compliance. Bureaucracy expenditure +6% and social expenditure +4% while Iraq owns and controls the state, including after coring. Exclusive with Central State Rule.']),
        e('iran_central_administration','Central State Rule','Standardize provincial appointments and administration under Baghdad. A cheaper centralized settlement narrows local participation and creates political friction.',cost=7,cash=.025,m=M(admin=.03,dd=.08,st=-.03),requires=['Iraq owns and controls Khuzestan; it remains a non-core'],active_requires=['Iraq owns and controls Khuzestan'],icon='government_beu',historic='Alternate-history centralized integration choice',
          instant=['399 = { add_compliance = 6 }'],outcomes=['One-time +6percentage points of local compliance; ideology drift defence +8%, bureaucracy expenditure +3% and stability -3points while Iraq owns and controls the province, including after coring. Exclusive with Equal Citizenship.']),
        e('iran_core_khuzestan','An Iraqi Province','Complete the institutional integration of Khuzestan after a sustained hold, sufficient compliance, low resistance and funded infrastructure. This is an explicit alternate-history gameplay outcome.',cost=10,cash=.06,requires=['Khuzestan is eligible for Iraqi core integration'],icon='government_beu',historic='Alternate-history core reward; thresholds are balance proposals',
          instant=['399 = { add_core_of = IRQ }'],outcomes=['Khuzestan (399) becomes an Iraqi CORE once. Requires730continuous days of Iraqi ownership AND control, peace with Iran, infrastructure at least3, compliance at least60%, resistance below15%, and the frozen6%GDP invoice. Both provincial policies can reach this focus. Existing PER/ARA cores remain; no additional oil, population, manpower or buildings are spawned. The earned Iraqi core persists through government changes and later territorial loss; selected administrative costs remain conditional on holding the province.']),
    ],icon='army_reform',note='Historical disputed territorial demand plus explicit attack route and alternate-history core integration. Native claim, add_core_of, take_state_focus, timed PER-targeted ideas, treasury and occupation effects; campaign-window/holding-clock hooks, offers and reconciliation are proposed integration. No forced peaceful military capstone.',geometry=GEOMETRY,exclusions=EXCLUSIONS)

def idea_specimen():
    lines=['# COLDWAR_IRQ CONCEPT ONLY: new ideas, not registered in the live mod.','ideas = {','\tcountry = {']
    for key,idea in IDEAS.items():
        lines += ['\t\t'+key+' = {','\t\t\tpicture = army_good_officer']
        if idea.get('cancel_peace'):lines += ['\t\t\tcancel = { NOT = { has_war_with = PER } }']
        lines += ['\t\t\tmodifier = {']+[f'\t\t\t\t{k} = {v:g}' for k,v in idea['modifier'].items()]+['\t\t\t}']
        if idea.get('targeted_modifier'):
            lines += ['\t\t\ttargeted_modifier = {']+[f'\t\t\t\t{k} = {v}' for k,v in idea['targeted_modifier'].items()]+['\t\t\t}']
        lines += ['\t\t}']
    return '\n'.join(lines+['\t}','}'])+'\n'

def campaign_specimen():
    return '# IMPERIA CW — Cold War: iraq 1970 concept generated content.\n# COLDWAR_IRQ CONCEPT ONLY. New daily/on-war/peace observer; not a native MD helper.\n# Called in IRQ scope on actual war transitions, daily and on load; never inferred from focus completion.\n# A missing current-war flag is initialized conservatively on a legacy save; elapsed days are not invented.\nCOLDWAR_IRQ_update_iran_campaign = {\n # Observe actual ownership/control from first acquisition, independently of party or completed focuses.\n # Also call on_state_control_changed and authoritative peace/transfer pipelines to catch brief losses.\n if = {\n  limit = { 399 = { is_owned_and_controlled_by = IRQ } }\n  if = {\n   limit = { NOT = { has_country_flag = COLDWAR_IRQ_khuzestan_hold_since } }\n   set_country_flag = COLDWAR_IRQ_khuzestan_hold_since\n  }\n }\n else = { clr_country_flag = COLDWAR_IRQ_khuzestan_hold_since }\n if = {\n  limit = { has_war_with = PER }\n  if = {\n   limit = { NOT = { has_country_flag = COLDWAR_IRQ_iran_current_war_start } }\n   set_country_flag = COLDWAR_IRQ_iran_current_war_start\n   set_country_flag = COLDWAR_IRQ_iran_programme_refresh_needed\n  }\n  if = {\n   limit = { NOT = { has_country_flag = COLDWAR_IRQ_iran_first_war_seen } }\n   set_country_flag = COLDWAR_IRQ_iran_first_war_seen\n   set_country_flag = COLDWAR_IRQ_iran_campaign_window_open\n  }\n  if = {\n   limit = { has_country_flag = { flag = COLDWAR_IRQ_iran_first_war_seen days > 29 } }\n   clr_country_flag = COLDWAR_IRQ_iran_campaign_window_open\n  }\n  if = {\n   limit = {\n    has_country_flag = { flag = COLDWAR_IRQ_iran_current_war_start days > 179 }\n    NOT = { has_idea = COLDWAR_IRQ_iran_attrition_bill }\n   }\n   add_ideas = COLDWAR_IRQ_iran_attrition_bill\n  }\n }\n else = {\n  if = {\n   limit = { has_country_flag = COLDWAR_IRQ_iran_current_war_start }\n   clr_country_flag = COLDWAR_IRQ_iran_current_war_start\n   set_country_flag = COLDWAR_IRQ_iran_programme_refresh_needed\n  }\n  clr_country_flag = COLDWAR_IRQ_iran_campaign_window_open\n  if = { limit = { has_idea = COLDWAR_IRQ_iran_opening_offensive } remove_ideas = COLDWAR_IRQ_iran_opening_offensive }\n  if = { limit = { has_idea = COLDWAR_IRQ_iran_sustained_offensive } remove_ideas = COLDWAR_IRQ_iran_sustained_offensive }\n  if = { limit = { has_idea = COLDWAR_IRQ_iran_followup_offensive } remove_ideas = COLDWAR_IRQ_iran_followup_offensive }\n  if = { limit = { has_idea = COLDWAR_IRQ_iran_attrition_bill } remove_ideas = COLDWAR_IRQ_iran_attrition_bill }\n }\n # After any earned territorial package, re-evaluate current control, ownership and infrastructure daily.\n # These flags are actual package-earned flags emitted by effect_body, not completion assumptions.\n if = {\n  limit = { OR = {\n   has_country_flag = COLDWAR_IRQ_iran_secure_khuzestan_package_earned\n   has_country_flag = COLDWAR_IRQ_iran_oil_rehabilitation_package_earned\n   has_country_flag = COLDWAR_IRQ_iran_civil_administration_package_earned\n   has_country_flag = COLDWAR_IRQ_iran_regional_power_package_earned\n   has_country_flag = COLDWAR_IRQ_iran_provincial_settlement_package_earned\n   has_country_flag = COLDWAR_IRQ_iran_equal_citizenship_package_earned\n   has_country_flag = COLDWAR_IRQ_iran_central_administration_package_earned\n  } }\n  set_country_flag = COLDWAR_IRQ_iran_programme_refresh_needed\n }\n if = {\n  limit = { has_country_flag = COLDWAR_IRQ_iran_programme_refresh_needed }\n  COLDWAR_IRQ_reconcile_programmes = yes # NEW existing-concept reconciler; never replay once-only delivery.\n  clr_country_flag = COLDWAR_IRQ_iran_programme_refresh_needed\n }\n # NEVER clear first_war_seen, opening_used, disarray_used, focus delivery or invoice flags.\n # NEVER remove mobilization_bill or followup_bill here: their original expiry survives peace.\n # War transitions and the territorial guard request one cache refresh per observer call.\n}\n'
