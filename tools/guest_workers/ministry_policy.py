# IMPERIA CW — Cold War: Native policy page, keeping the country/community register uncluttered.
def add(label,button,local,dt,flag):
    tab=3
    label('gw_dp_national_heading','SETTLEMENT AND HOMECOMING',24,247,tab=tab,font='hoi4_typewriter22',height=28)
    def action(name,text,x,y,guard,effect,tip):
        condition=guard+' NOT = { has_country_flag = gw_dialog_window }'
        button(name,text,x,y,'wide',tab=tab,condition=condition,enabled=condition,effect=effect,tip=tip)
        button(name+'_unavailable',text,x,y,'wide_muted',tab=tab,condition='NOT = { '+condition+' }',enabled='always = no',tip=tip)
    action('gw_dp_retention','Residence & Settlement',24,280,'mdcw_dp_can_retention = yes','mdcw_dp_open_retention = yes','gw_dp_retention_button_tt')
    action('gw_dp_homecoming','Homecoming Campaign',264,280,'mdcw_dp_can_homecoming = yes','mdcw_dp_open_homecoming = yes','gw_dp_homecoming_button_tt')
    dt('gw_dp_retention_price_text',[('has_country_flag = gw_dp_retention',local('gw_dp_retention_active','ACTIVE | Settlement support'))],local('gw_dp_retention_inactive','75 PP | $25m/week per 100,000'))
    dt('gw_dp_homecoming_price_text',[('has_country_flag = gw_dp_homecoming',local('gw_dp_homecoming_active','ACTIVE | Return incentive +4pp'))],local('gw_dp_homecoming_inactive','75 PP | $500m per 100,000'))
    label('gw_dp_retention_price','[gw_dp_retention_price_text]',24,316,width=228,tab=tab)
    label('gw_dp_homecoming_price','[gw_dp_homecoming_price_text]',264,316,width=228,tab=tab)
    label('gw_dp_foreign_heading','OVERSEAS COMMUNITY',24,349,width=300,tab=tab)
    button('gw_dp_choose_host','Choose Community',340,341,tab=tab,effect='set_variable = { gw_ui_tab = 1 } set_country_flag = gw_ui_show_abroad mdcw_gw_ministry_host_page = yes')
    flag('gw_dp_selected_flag','gw_dp_target',31,379,tab,'check_variable = { gw_dp_target > -1 }',None)
    label('gw_dp_selected_host','[?gw_dp_target.GetName]',81,379,width=397,tab=tab,font='hoi4_typewriter16',height=28,condition='check_variable = { gw_dp_target > -1 }')
    label('gw_dp_selected_empty','Select one of our communities abroad.',24,379,tab=tab,condition='NOT = { check_variable = { gw_dp_target > -1 } }')
    label('gw_dp_selected_population','Community: [?gw_dp_stock|1] thousand',24,410,width=300,tab=tab)
    label('gw_dp_slots_used','Places in use: [?gw_dp_active_count|0]/2',340,410,width=148,tab=tab)
    action('gw_dp_remittance','Remittance Campaign',24,438,'mdcw_dp_can_remittance = yes','mdcw_dp_open_remittance = yes','gw_dp_remittance_button_tt')
    action('gw_dp_trade','Diaspora Trade Agreement',264,438,'mdcw_dp_can_trade = yes','mdcw_dp_request_trade = yes','gw_dp_trade_button_tt')
    label('gw_dp_remittance_price','75 PP | $[?gw_dp_campaign_cash|2]bn',24,475,width=228,tab=tab)
    label('gw_dp_trade_price','50 PP | $[?gw_dp_trade_cash|2]bn',264,475,width=228,tab=tab)
    action('gw_dp_skill','Skilled Return Programme',24,502,'mdcw_dp_can_skill = yes','mdcw_dp_request_skill = yes','gw_dp_skill_button_tt')
    label('gw_dp_skill_price','100 PP | up to $[?gw_dp_skill_cash|2]bn',264,511,width=228,tab=tab)
    label('gw_dp_policy_status','[gw_dp_policy_status]',24,544,height=36,tab=tab)
    label('gw_dp_active_heading','CURRENT OVERSEAS PROGRAMMES',24,588,tab=tab)
    for slot,y in ((1,615),(2,649)):
        name=f'gw_dp_slot{slot}_name'
        dt(name,[(f'check_variable = {{ gw_dp_type_{slot} = {kind} }}',local(f'gw_dp_type_{kind}',title)) for kind,title in ((1,'Remittance Campaign'),(2,'Diaspora Trade'),(3,'Skilled Return'))],local('gw_dp_no_programme','No programme assigned'))
        dt(f'gw_dp_slot{slot}_receipt_terms',[(f'check_variable = {{ gw_dp_type_{slot} = 2 }}',f'gw_dp_slot{slot}_trade_receipt')],f'gw_dp_slot{slot}_skill_receipt')
        dt(f'gw_dp_slot{slot}_line',[(f'has_country_flag = gw_dp_active_{slot}',local(f'gw_dp_slot{slot}_active',f'[?gw_dp_host_{slot}.GetName]: [{name}]'))],local(f'gw_dp_slot{slot}_empty',f'Programme place {slot}: available'))
        label(f'gw_dp_slot{slot}','[gw_dp_slot'+str(slot)+'_line]',24,y,height=32,tab=tab,tip=f'gw_dp_slot{slot}_tooltip')
        local(f'gw_dp_slot{slot}_tooltip',f'[{name}]\nParticipants or return target: [?gw_dp_cohort_{slot}|1] thousand\nVoluntary returns credited: [?gw_dp_returned_{slot}|1] thousand\nCampaign: 180 days. Trade and return preparation: 365 days.\nA community may take another programme 365 days after approval. Skilled return programmes have a national 730-day interval.')
    dt('gw_dp_policy_status',[
        ('has_country_flag = gw_dp_request',local('gw_dp_status_wait','Awaiting a reply from [?gw_dp_partner.GetName].')),
        ('OR = { has_country_flag = gw_dp_offer has_country_flag = gw_dp_offer_window has_country_flag = mdcw_gw_offer_pending has_country_flag = mdcw_gw_request_pending }',local('gw_dp_status_busy','Conclude our current overseas negotiations first.')),
        ('has_country_flag = gw_dialog_window',local('gw_dp_status_dialog','Review the programme awaiting authorisation.')),
        ('check_variable = { gw_dp_active_count > 1 }',local('gw_dp_status_full','Both overseas programme places are in use.')),
        ('NOT = { check_variable = { gw_dp_stock > 0 } }',local('gw_dp_status_choose','Choose a community under Communities / Abroad.')),
        ('check_variable = { gw_dp_target_free = 0 }',local('gw_dp_status_cooldown','This community is negotiating or awaiting programme renewal.')),
    ],local('gw_dp_status_ready','Review programme costs and terms before applying.'))
    local('gw_dp_retention_button_tt','Fund settlement and family support for 365 days.\n\n75 Political Power\nAdditional weekly spending: $$25 million per 100,000 residents.\nAnnual voluntary return rate: -35% relative.\n[gw_dp_policy_status]')
    local('gw_dp_homecoming_button_tt','Offer relocation and employment assistance to our citizens abroad.\n\n75 Political Power | $$[?gw_dp_homecoming_cash|2] billion\nAnnual return rate: +4 percentage points for 365 days for the funded population. Later emigration does not enlarge the funded group.\n[gw_dp_policy_status]')
    local('gw_dp_remittance_button_tt','Arrange cheaper transfers and family savings schemes.\n\n75 Political Power | $$[?gw_dp_campaign_cash|2] billion\nParticipants: [?gw_dp_campaign_k|1] thousand\nAdditional weekly remittances: up to $$[?gw_dp_campaign_k|1] million, for 180 days.\nNational campaign limit: $$300 million/week.\nAll remittances share the $$3 billion weekly ceiling.\nRequires 25,000 eligible net emigrants and an available programme place.\n[gw_dp_policy_status]')
    local('gw_dp_trade_button_tt','Negotiate household goods deliveries through our overseas community.\n\n50 Political Power | $$[?gw_dp_trade_cash|2] billion\nConsumer Goods Factor: [?gw_dp_trade_preview|%1] for 365 days.\nThe host government must approve and receives the full payment. Requires 25,000 residents. Total trade relief is limited to -6%.\n[gw_dp_policy_status]')
    local('gw_dp_skill_button_tt','Negotiate employment preparation and resettlement at home.\n\n100 Political Power | up to $$[?gw_dp_skill_cash|2] billion at completion\nReturn target: [?gw_dp_skill_k|1] thousand over 365 days.\nResearch Speed: up to +[?gw_dp_skill_research|%1] for 730 days.\nThe host must approve and receives half the completion payment. Earlier voluntary returns count towards the target. Payments and research scale with actual funded returns; national research relief is capped at +3%.\nRequires 25,000 residents, an available programme place and expiry of the 730-day national interval.\n[gw_dp_policy_status]')
    local('gw_dp_migration_tt','Latest annual return rate: [?gw_ui_return_rate|1]%\nExpected returns from the eligible stock: [?gw_ui_return_expected|1] thousand\nLast annual return: [?gw_ui_return_last|1] thousand\n\nA smaller income advantage abroad encourages return. Each full 5 percentage points of stability advantage changes the annual return rate by 1 percentage point, up to +/-2.\nWar in the host country alone multiplies returns by 4, up to 60% a year. War in the home country alone reduces returns to one quarter. If both are at war, neither war adjustment applies.\nRates are reviewed quarterly and population returns annually. New arrivals enter the following return-year cohort. Settlement and integration can reduce return by up to 60%; the final annual rate is 0.5-15%, or up to 60% if only the host country is at war. Earlier organised returns discharge the corresponding annual return allowance. Ordinary returns carry no forced-repatriation penalties.')
