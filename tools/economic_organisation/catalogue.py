# IMPERIA COLD WAR — Economic organisation policy catalogue
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MARKER = '# IMPERIA COLD WAR — Economic organisation'

# Each entry is a complete alternative policy. The modifier keys have existing MD readers.
TIERS = [
    ('command', 'Command Economy', -100, -70, {
        'total_workforce_modifier': .05, 'country_productivity_growth_modifier': -.20,
        'production_speed_industrial_complex_factor': .10, 'production_speed_infrastructure_factor': .15,
        'production_speed_offices_factor': -.15, 'offices_productivity': -.10,
        'production_factory_max_efficiency_factor': .10, 'production_factory_efficiency_gain_factor': -.20,
        'receiving_investment_cost_modifier': .15, 'receiving_investment_duration_modifier': .15,
        'internal_investments_money_cost_modifier': -.10, 'globalism_equilibrium': -15, 'mdcw_cw_market_exposure': -.25,
        'communism_drift': .02}),
    ('planning', 'Central Planning', -70, -40, {
        'total_workforce_modifier': .03, 'country_productivity_growth_modifier': -.12,
        'production_speed_industrial_complex_factor': .07, 'production_speed_infrastructure_factor': .10,
        'production_speed_offices_factor': -.10, 'offices_productivity': -.07,
        'production_factory_max_efficiency_factor': .05, 'production_factory_efficiency_gain_factor': -.12,
        'receiving_investment_cost_modifier': .10, 'receiving_investment_duration_modifier': .10,
        'internal_investments_money_cost_modifier': -.07, 'globalism_equilibrium': -10, 'mdcw_cw_market_exposure': -.15,
        'communism_drift': .01}),
    ('development', 'State-Led Development', -40, -15, {
        'bureaucracy_cost_multiplier_modifier': .05,
        'production_speed_industrial_complex_factor': .08, 'production_speed_infrastructure_factor': .05,
        'production_speed_offices_factor': -.05, 'offices_productivity': -.03,
        'production_factory_max_efficiency_factor': .02, 'production_factory_efficiency_gain_factor': -.05,
        'receiving_investment_cost_modifier': .05, 'receiving_investment_duration_modifier': .05,
        'internal_investments_money_cost_modifier': -.05, 'globalism_equilibrium': -5, 'mdcw_cw_market_exposure': -.05}),
    ('mixed', 'Mixed Economy', -15, 15, {
        'internal_investments_money_cost_modifier': -.02, 'production_factory_efficiency_gain_factor': .03}),
    ('regulated', 'Regulated Market Economy', 15, 40, {
        'country_productivity_growth_modifier': .05, 'bureaucracy_cost_multiplier_modifier': .05,
        'production_speed_offices_factor': .05, 'offices_productivity': .03,
        'receiving_investment_cost_modifier': -.03, 'receiving_investment_duration_modifier': -.05,
        'internal_investments_money_cost_modifier': .04, 'globalism_equilibrium': 5, 'mdcw_cw_market_exposure': .05}),
    ('liberal', 'Liberal Market Economy', 40, 70, {
        'country_productivity_growth_modifier': .10,
        'production_speed_offices_factor': .10, 'offices_productivity': .07,
        'receiving_investment_cost_modifier': -.07, 'receiving_investment_duration_modifier': -.10,
        'internal_investments_money_cost_modifier': .10, 'globalism_equilibrium': 10, 'mdcw_cw_market_exposure': .15,
        'democratic_drift': .01}),
    ('laissez', 'Laissez-Faire Economy', 70, 101, {
        'country_productivity_growth_modifier': .15, 'return_on_investment_modifier': .01,
        'production_speed_offices_factor': .15, 'offices_productivity': .10,
        'receiving_investment_cost_modifier': -.10, 'receiving_investment_duration_modifier': -.15,
        'internal_investments_money_cost_modifier': .20, 'globalism_equilibrium': 15, 'mdcw_cw_market_exposure': .25,
        'democratic_drift': .02}),
]
# IMPERIA COLD WAR — Native economic modifier display units
LABELS = {
    'total_workforce_modifier': ('Available Workforce', True, True),
    'country_productivity_growth_modifier': ('Productivity Growth', True, True),
    'bureaucracy_cost_multiplier_modifier': ('Administration Cost', False, True),
    'return_on_investment_modifier': ('Annual Investment Return', True, True),
    'production_speed_industrial_complex_factor': ('Civilian Industry Construction Speed', True, True),
    'production_speed_infrastructure_factor': ('Infrastructure Construction Speed', True, True),
    'production_speed_offices_factor': ('Office Construction Speed', True, True),
    'offices_productivity': ('Office Productivity', True, True),
    'production_factory_max_efficiency_factor': ('Production Efficiency Cap', True, True),
    'production_factory_efficiency_gain_factor': ('Production Efficiency Growth', True, True),
    'receiving_investment_cost_modifier': ('Incoming Investment Cost', False, True),
    'receiving_investment_duration_modifier': ('Incoming Investment Duration', False, True),
    'internal_investments_money_cost_modifier': ('Domestic Investment Money Cost', False, True),
    'globalism_equilibrium': ('Globalisation Equilibrium', True, False),
    'mdcw_cw_market_exposure': ('Exposure to World Market Swings', False, True),
    'democratic_drift': ('Daily Western Support', True, 'daily'),
    'communism_drift': ('Daily Emerging Support', True, 'daily'),
}
# One-off sale receipt: 0.5% of current native MD GDP for ten newly liberalised points.
# A saved maximum market position prevents collecting again after a reversal.
SALE_GDP_PER_POINT = .0005
DESCRIPTIONS = {
    'command': 'Binding production targets and public ownership concentrate investment in industry and national infrastructure. Standardised production gains priority over enterprise flexibility and commercial services.',
    'planning': 'Central agencies coordinate industrial investment and production targets. Public projects benefit from a common programme, while businesses and foreign investors face tighter administrative controls.',
    'development': 'Public investment and selected industrial priorities guide development alongside privately managed enterprises. Commercial investment remains subject to national economic priorities.',
    'mixed': 'Public institutions and private enterprises share responsibility for investment, employment and production. Sectoral policy remains open to parliamentary and ministerial choices.',
    'regulated': 'Private enterprise operates within an established regulatory and public-service framework. Commercial services benefit from competition while public investment carries additional coordination costs.',
    'liberal': 'Private investment and commercial competition guide most economic activity. Foreign capital gains easier access, while state programmes face higher financing and coordination costs.',
    'laissez': 'Private enterprise and international capital markets determine most investment decisions. Commercial services expand, while public investment is costlier and world-market fluctuations have greater domestic impact.',
}
REFORMS = [
    ('ownership', 'Expand State Ownership', -10, 50, 'Public ownership will give national institutions a larger role in allocating investment and directing production.'),
    ('targets', 'Introduce Production Targets', -5, 35, 'A more binding framework of production targets will strengthen coordination between enterprises and public agencies.'),
    ('autonomy', 'Grant Enterprise Autonomy', 5, 35, 'Enterprise managers will receive greater discretion over procurement, production and commercial contracts.'),
    ('privatisation', 'Privatise State Enterprises', 10, 50, 'Selected state enterprises will pass into private ownership under a national privatisation programme.'),
    ('capital', 'Open International Capital Markets', 15, 75, 'A sufficiently integrated economy can admit a wider range of international investors and commercial financial arrangements.'),
]

# Initial institutional profiles, not party/outlook assignments. Unknown/released countries use Mixed Economy.
STARTS = {
    -90: ['NKO', 'ALB'], -80: ['SOV', 'DDR', 'CZE', 'BUL', 'ROM', 'CUB', 'MON'],
    -70: ['POL', 'VIE'], -55: ['HUN', 'ALG', 'SYR', 'IRQ'], -30: ['RAJ', 'EGY'],
    -25: ['FRA', 'SER'], 20: ['GER', 'ENG', 'SWE', 'NOR', 'DEN', 'FIN', 'AUT', 'ITA', 'JAP', 'KOR', 'SIN'],
    45: ['USA', 'CAN', 'AST', 'NZL', 'HOL', 'BEL'], 55: ['SWI'], 85: ['HKG'],
}
