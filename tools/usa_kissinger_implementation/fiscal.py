# IMPERIA COLD WAR — GDP-indexed statecraft costs and mirrored weekly transfers.
from .shared import *

# All rates are percentages of current annual GDP. Weekly rates are charged
# per week, not annual percentages divided by 52. Every literal has <=5 decimals.
HOST_SETUP={'security_quote':2,'investment_quote':1,'settlement_quote':10,
 'reform_quote_1':10,'reform_quote_2':12,'reform_quote_3':15,'reform_quote_4':18,
 'emergency_quote':2,'repression_quote':4}
US_SETUP={'covert':.0005,'clients':.0003,'angola':.0005,'political':.0002,
 'chile':.0003,'kurds':.0002,'irq_fund':.0005,'irq_front':.0003,
 'irn_contacts':.0002,'irn_fund':.0005,'irn_front':.0003,
 'tur_networks':.0002,'tur_front':.0005,'syr_voice':.0002,
 'syr_organisation':.0003,'syr_front':.0005,
 'intensify':.0025,'air_route':.0002,'resupply':.0003,'legacy':.025,'networks':.0005}
WEEKLY={'security':.004,'investment':.002,'rights':.001,
 'us_funded':.00002,'us_armed':.00005,'us_legacy':.005,
 'us_surge':.0002,'us_air':.00004,'us_chile':.00002}
DEAL_PCTS={'beijing':.00002,'moscow':.00002,'irq_transit':.00002,
 'irq_anatolia':.00004,'tur_alliance':.00002,'irq_settlement':.00002,
 'irn_rights':.00002,'tur_rights':.00002,'syr_rights':.00002,'angola':.00004}
WEEKLY.update({'deal_'+key+'_usa':rate for key,rate in DEAL_PCTS.items()})
WEEKLY['deal_moscow_partner']=DEAL_PCTS['moscow']


def calculate(variable,percent,basis='gdp_total',temporary=False):
    kind='temp_variable' if temporary else 'variable'
    return '\n'.join([f'set_{kind} = {{ {variable} = {basis} }}',
      f'multiply_{kind} = {{ {variable} = {num(percent)} }}',
      f'divide_{kind} = {{ {variable} = 100 }}'])


def charge(percent,basis='gdp_total'):
    return calculate('treasury_change',-Decimal(str(percent)),basis,True)+'\nmodify_treasury_effect = yes'


def purchase(percent,body,basis='gdp_total'):
    invoice=calculate(P+'invoice',percent,basis,True)
    pay='set_temp_variable = { treasury_change = '+P+'invoice }\nmultiply_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes'
    return invoice+'\n'+guard('check_variable = { '+P+'invoice > 0 }\n'+at_least('treasury',P+'invoice'),pay+'\n'+body)


def cost_rows(percent,basis='gdp_total'):
    return percentage_row('gdp_cost',-Decimal(str(percent)))+'\n'+charge(percent,basis)


def percentage_row(label,percent):
    # Preserve small rates without padding integer percentages with zeroes.
    places=max(0,-Decimal(str(percent)).normalize().as_tuple().exponent)
    assert places<=5
    return f'add_to_variable = {{ {P}preview_{label} = {num(percent)} tooltip = {P}{label}_{places}_tt }}'


def weekly_rows(key,sign=-1,basis='gdp_total',donor=False):
    pct=Decimal(str(WEEKLY[key]))*sign
    label='weekly_usa_gdp' if donor else 'weekly_gdp'
    return percentage_row(label,pct)+'\n'+calculate(P+'preview_weekly_amount',pct,basis,True)+'\nadd_to_variable = { '+P+'preview_weekly = '+P+'preview_weekly_amount tooltip = '+P+'weekly_tt }'


def stream(kind,key,donor=False):
    return 'add_to_variable = { '+P+'weekly_'+kind+' = '+('USA.' if donor else '')+P+'week_'+key+' }'


def weekly_text(key,sign=-1,donor=False):
    symbol='-' if sign<0 else '+';colour='R' if sign<0 else 'G'
    basis='US GDP' if donor else 'current GDP'
    variable=('USA.' if donor else '')+P+'week_'+key
    return 'Programme balance: §'+colour+symbol+num(WEEKLY[key])+'%§! of '+basis+' per week (§'+colour+symbol+'$[?'+variable+'|5] billion/week§!).'


def affordable(quote):
    return requirement('treasury_gdp_tt','check_variable = { gdp_total > 0 }\ncheck_variable = { '+P+quote+' > 0 }\n'+at_least('treasury',P+quote))


def register(loc,fx):
    for places in range(6):
        for label,title,basis in [('gdp_cost','Treasury','current GDP'),
          ('weekly_gdp','Weekly programme balance','current GDP'),
          ('weekly_usa_gdp','Weekly programme balance','US GDP')]:
            loc[P+label+'_'+str(places)+'_tt']=title+': $RIGHT|+='+str(places)+'$% of '+basis
    loc[P+'treasury_gdp_tt']='Sufficient treasury for the current GDP-based programme cost.'
    fx[P+'refresh_fiscal_host']='\n'.join([*(calculate(P+key,value) for key,value in HOST_SETUP.items()),
      *(calculate(P+'week_'+key,WEEKLY[key]) for key in ('security','investment','rights'))])
    fx[P+'refresh_fiscal_usa']='\n'.join([*(calculate(P+'us_'+key+'_quote',value) for key,value in US_SETUP.items()),
      *(calculate(P+'week_'+key,value) for key,value in WEEKLY.items() if key.startswith('us_') or key.endswith('_usa'))])
    recipients=' '.join('tag = '+tag for tag in ('PER','TUR','KUR','PUK','KPI','KPT','KPS'))
    hosts=' '.join('tag = '+d['tag'] for d in HOSTS.values())
    fx[P+'refresh_fiscal']='\n'.join([
      guard('tag = USA',P+'refresh_fiscal_usa = yes'),
      guard('OR = { '+hosts+' }',P+'refresh_fiscal_host = yes'),
      guard('tag = SOV',calculate(P+'week_deal_moscow_partner',DEAL_PCTS['moscow'])),
      guard('tag = CHL',calculate(P+'investment_quote',1)),
      guard('OR = { '+recipients+' }','USA = { '+P+'refresh_fiscal_usa = yes }')])
