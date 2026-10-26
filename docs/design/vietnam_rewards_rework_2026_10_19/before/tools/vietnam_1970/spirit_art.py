"""Native MD national-spirit textures, separate from the larger focus art."""
BASE = 'gfx/interface/ideas/'

SPIRIT_ART = {key: BASE+path for key,path in {
    'war_damage': 'army/recovering_from_the_civil_war.dds',
    'rationing': 'diplomacy/risk_of_famine.dds',
    'mobilisation': 'army/national_mobilization.dds',
    'patrons': 'diplomacy/international_treaty.dds',
    'cadre_state': 'ideology/collective_soceity.dds',
    'division': 'diplomacy/rival_government.dds',
}.items()}

PROGRAMME_ART = {key: BASE+path for key,path in {
    'state': 'diplomacy/political_power_bonus.dds',
    'duan': 'ideology/communism.dds',
    'chinh': 'ideology/collective_soceity.dds',
    'linh': 'economy/agricultural_reforms.dds',
    'kiet': 'economy/construction.dds',
    'front': 'ideology/popular_front.dds',
    'dem': 'ideology/social_liberalism.dds',
    'soc': 'ideology/social_democracy.dds',
    'nat': 'ideology/nationalism.dds',
    'junta': 'army/national_mobilization.dds',
    'industry': 'economy/construction.dds',
    'farm': 'economy/agriculture.dds',
    'army': 'army/planning_bonus.dds',
    'unity': 'diplomacy/national_unity.dds',
    'diplomacy': 'diplomacy/international_treaty.dds',
}.items()}

CRISIS_ART = {key: BASE+path for key,path in {
    'flood': 'diplomacy/risk_of_famine.dds',
    'integration': 'diplomacy/rival_government.dds',
    'screening': 'ideology/collective_soceity.dds',
    'prices': 'economy/inflation.dds',
    'border': 'army/national_mobilization.dds',
    'patron': 'diplomacy/international_treaty.dds',
}.items()}
