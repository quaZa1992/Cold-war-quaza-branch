# IMPERIA COLD WAR — Argentina GDP-relative programme financing.
"""Native MD annual-GDP appropriations, converted to weekly units at runtime."""
from decimal import Decimal

# Native small/medium/large expenditure is 0.2/0.4/0.6 percent GDP.
# One-state capital investments and exceptional programmes use 1/1.5 percent.
SETUP_SHARES={0:0,1:0.002,2:0.004,3:0.006,4:0.01,5:0.015,6:0.02}
P='COLDWAR_ARG_'

def num(v):return format(Decimal(str(v)),'f').rstrip('0').rstrip('.') if '.' in str(v) else str(v)
def setup_share(weight):return SETUP_SHARES[weight] if weight>0 else 0
def annual_share(weight):return float(Decimal(str(weight))*Decimal('0.5'))
def money(weight,basis='gdp_total'):
    if not weight:return ''
    # Preserve the approved, once-only asset-sale proceeds. This revision reprices spending.
    value=str(-weight) if weight<0 else '{ value = '+basis+' multiply = -'+num(setup_share(weight))+' }'
    return 'set_temp_variable = { treasury_change = '+value+' }\nmodify_treasury_effect = yes\n'
def weekly_value(share,basis='gdp_total'):
    return '{ value = '+basis+' multiply = '+num(share)+' divide = 52 }'
def weekly_add(target,share,basis='gdp_total'):
    if not share:return ''
    return 'set_temp_variable = { '+P+'weekly_amount = '+weekly_value(share,basis)+' }\nadd_to_variable = { '+target+' = '+P+'weekly_amount }\n'
def weekly_preview(weight,tooltip=P+'weekly_expense_tt',basis='gdp_total'):
    if not weight:return ''
    share=annual_share(weight)
    return 'set_temp_variable = { '+P+'weekly_amount = '+weekly_value(share,basis)+' }\nadd_to_variable = { '+P+'weekly_preview = '+P+'weekly_amount tooltip = '+tooltip+' }\n'
def compensation(share,basis='ARG.gdp_total'):
    return 'set_temp_variable = { treasury_change = { value = '+basis+' multiply = '+num(share)+' } }\nmodify_treasury_effect = yes\n'
def own_weekly_weight(agreement,side):
    weight=Decimal(str(agreement[side].get('weekly',0)))
    if agreement['id']=='bolivia_gas' and side=='argentina':weight-=Decimal(str(agreement['recipient']['credit']))
    if agreement['id']=='soviet_grain' and side=='recipient':weight-=Decimal(str(agreement['argentina']['credit']))
    return float(weight)
def transfer(agreement):
    # The traded Argentine export/import volume follows ARG GDP. The exact same
    # annual appropriation is debited to its payer and credited to its recipient.
    if agreement['id']=='bolivia_gas':return ('ARG','BOL',annual_share(agreement['recipient']['credit']))
    if agreement['id']=='soviet_grain':return ('SOV','ARG',annual_share(agreement['argentina']['credit']))
    return None
def annotate(d):
    for n in d['nodes']+d['decisions']+[o for e in d['events'] for o in e['options']]:
        n['money_gdp_share']=setup_share(n['money'])
        n['weekly_annual_gdp_share']=annual_share(n['weekly'])
    for a in d['agreements']:
        for side in ('argentina','recipient'):
            a[side]['setup_gdp_share']=setup_share(a[side].get('setup',0))
            a[side]['weekly_own_annual_gdp_share']=annual_share(own_weekly_weight(a,side))
        a['transfer']=dict(zip(('payer','recipient','annual_arg_gdp_share'),transfer(a))) if transfer(a) else None
        if a['id']=='uk_sovereignty':a['recipient']['grant_arg_gdp_share']=0.015
    d['budget_revision']=dict(project='IMPERIA COLD WAR',revision='Argentina GDP financing 2026-11-01',basis='Live native gdp_total in the paying country; annual appropriations divided by 52',setup_shares=SETUP_SHARES,annual_share_per_legacy_weekly_unit=0.5,arg_1970_internal_gdp=107.38543,arg_1970_historical_display_gdp=31.58395,price_basis_factor=3.4)
    return d
