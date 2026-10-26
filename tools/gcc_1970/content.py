# IMPERIA CW — Cold War: gcc 1970 — content.
"""COLDWAR adaptation of the fourteen plausible native GCC institutions.

Costs are balance shares of the completing country's current annual GDP.
Each focus implements national policy, not another member's domestic policy.
"""
TAGS = ('SAU', 'KUW', 'BHR', 'QAT', 'OMA', 'UAE')
P = 'COLDWAR_GCC_'


def node(key, native, title, description, share=0, modifiers=None, xp=None):
    return dict(key=key, id=P+key, native='GCC_'+native, title=title,
                description=description, share=share, modifiers=modifiers or {}, xp=xp or {})


NODES = [
    node('council', 'the_gcc', 'A Gulf Council',
         'Britain\'s withdrawal and the growth of oil revenues are changing the balance along the Gulf. Membership in the Gulf Cooperation Council provides a framework for consultation without surrendering our sovereignty. Our administration must now turn the charter\'s commitments into practical cooperation.'),
    node('economic_agreement', 'economic_union', 'Economic Agreement',
         'Common principles for economic cooperation can give merchants and ministries a more dependable framework. Each state must prepare its own administration, reconcile the agreement with its laws and bear the continuing cost of implementation.',
         .01, dict(offices_productivity=.05, bureaucracy_cost_multiplier_modifier=.02)),
    node('regional_trade', 'intra_gcc_trade', 'Trade within the Gulf',
         'Rules of origin, customs documentation and more predictable treatment of regional goods can make neighbouring markets easier to serve. Better access rewards local enterprise, while inspection and certification create work for the customs administration.',
         .005, dict(offices_productivity=.03, trade_opinion_factor=.05, bureaucracy_cost_multiplier_modifier=.01)),
    node('technical_standards', 'standardize_regulations', 'Technical Standards',
         'Engineers, laboratories and ministries can compare technical standards and exchange practical research. Participating countries must establish their own committees and contribute expertise to sustain the exchange.',
         .0075, dict(bureaucracy_cost_multiplier_modifier=.01)),
    node('investment', 'common_market', 'Joint Investment',
         'Industrial partnerships need serviced sites, dependable utilities and firms able to work across national boundaries. Preparing our own economy for those partnerships can raise industrial performance, at the cost of investment and a larger demand for energy.',
         .02, dict(production_speed_industrial_complex_factor=.15, industrial_capacity_factory=.05, energy_use_multiplier=.03)),
    node('payments', 'monetary_union', 'Payment Consultations',
         'Central banks and commercial banks can improve settlement, accounting and the handling of cross-border payments. Practical coordination can make trade less cumbersome while each state retains its currency and control of monetary policy.',
         .0025, dict(offices_productivity=.02, bureaucracy_cost_multiplier_modifier=-.02)),
    node('transit', 'cross_border_transit_systems', 'Roads and Border Posts',
         'Road connections and dependable border procedures are more immediate needs than grand schemes for a single regional transport network. Planning, utilities and trained customs staff can support construction and commercial traffic, while heavier activity raises energy demand.',
         .015, dict(production_speed_infrastructure_factor=.20, offices_productivity=.03, energy_use_multiplier=.03)),
    node('defence_consultation', 'military_union', 'Defence Consultation',
         'Staff talks and shared exercises can help small armed forces understand their neighbours\' capabilities. Our services must assign personnel, prepare useful training and maintain liaison arrangements while retaining their national chains of command.',
         .005, dict(bureaucracy_cost_multiplier_modifier=.01), dict(army_experience=15, navy_experience=15, air_experience=15)),
    node('peninsula_shield', 'joint_defense_agreement', 'Peninsula Shield',
         'A limited contribution to a common defensive force can make regional consultation more useful in a crisis. Preparing that contribution requires trained personnel, compatible procedures and a lasting military payroll; national governments retain command of their own forces.',
         .02, dict(army_org_factor=.05, army_personnel_cost_multiplier_modifier=.05)),
    node('officer_exchange', 'gulf_academy', 'Officer Exchanges',
         'Training places, visiting instructors and exchanges between military schools can spread useful experience. Sending officers abroad and maintaining a professional training cadre require additional personnel expenditure and sustained attention from our military schools.',
         .005, dict(experience_gain_army_factor=.10, training_time_factor=-.05, army_personnel_cost_multiplier_modifier=.03), dict(army_experience=20)),
    node('joint_staff', 'limited_unified_command', 'Joint Staff Liaison',
         'Liaison officers can compare contingency plans, communications procedures and mobilisation requirements. A permanent liaison staff makes national planning more coherent, while its officers and administration require continuing support.',
         .01, dict(planning_speed=.10, max_planning_factor=.05, bureaucracy_cost_multiplier_modifier=.02)),
    node('maintenance', 'joint_military_ventures', 'Procurement and Repair',
         'Compatible equipment, repair standards and coordinated procurement can reduce the waste caused by small and incompatible production runs. Our own factories and workshops must still supply the investment, machinery and power needed to take part.',
         .02, dict(production_factory_max_efficiency_factor=.05, production_factory_efficiency_gain_factor=.05, industrial_capacity_factory=.05, energy_use_multiplier=.03)),
    node('contingency', 'a_robust_alliance', 'Contingency Planning',
         'The Gulf\'s security depends on national governments being able to coordinate when a crisis arrives. Rehearsed defensive plans and supply procedures can improve our national contribution. Liaison officers must keep those plans current as forces, equipment and regional risks change.',
         .005, dict(army_defence_factor=.05, supply_consumption_factor=-.03, bureaucracy_cost_multiplier_modifier=.01)),
    node('consultative_council', 'political_union', 'Council Meetings',
         'Regular meetings give rulers and ministers a place to discuss disputes before they grow into larger confrontations. Maintaining that channel can strengthen political coordination and diplomacy, while adding continuing duties to the national administration.',
         .0025, dict(political_power_factor=.05, improve_relations_maintain_cost_factor=-.20, bureaucracy_cost_multiplier_modifier=.02)),
]

ROOT_KEY = 'council'
GROUP = P+'technical_exchange'
ROUNDS = 32
