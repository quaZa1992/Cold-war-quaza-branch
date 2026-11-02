# IMPERIA COLD WAR — Israel 1970 player-directed diplomacy and domestic choices.
"""Historical institutions provide context; players select their own agenda.

Stable legacy IDs remain for saves. These explicit graph changes implement the
owner's multiplayer correction of 27 October 2026, rather than a layout shortcut.
"""
import re

PREREQUISITES={
    'ISR70_rogers':[['ISR70_suez']],
    'ISR70_armed_stalemate':[['ISR70_limited_attrition','ISR70_deep_raids']],
    'ISR70_territorial_policy':[['ISR70_january_1970']],
    'ISR70_land_survey':[['ISR70_territorial_policy']],
    'ISR70_gi_resident_status':[['ISR70_territorial_policy']],
}

def apply(data):
    nodes={n['id']:n for n in data['nodes']}
    for key,parents in PREREQUISITES.items():nodes[key]['prerequisites']=parents
    for key,other in (('ISR70_ceasefire','ISR70_armed_stalemate'),('ISR70_armed_stalemate','ISR70_ceasefire')):
        nodes[key]['mutually_exclusive']=[v for v in nodes[key]['mutually_exclusive'] if v!=other]
    text={
        'rogers':('Open Ceasefire Negotiations','The cabinet can propose a ceasefire on terms it is willing to defend. A military posture and negotiations can proceed in parallel. Egypt decides whether to accept the proposal; broader territorial questions remain for separate talks.'),
        'armed_stalemate':('Forward Defensive Readiness','Prepared positions, supply reserves and trained headquarters can support the cabinet during a confrontation or while negotiations proceed. Maintaining the posture demands a continuing personnel commitment.'),
        'territorial_policy':('Set the Territorial Programme','The cabinet must decide how to administer the territories under its control and what it is prepared to negotiate. Civil administration, development and diplomacy can begin alongside the military policy at the Suez front.'),
        'all_on':('Defensible Frontiers and Negotiating Reserves','Agricultural security zones and retained negotiating reserves offer one approach to territorial policy. Allon and other cabinet ministers have advanced competing proposals; the government must choose its own balance between a defensible frontier and room for agreement.'),
        'golda_succession':('Choose the Alignment Leadership','The governing Alignment can retain Golda Meir or seek a cabinet led by Yitzhak Rabin or Shimon Peres. Parliamentary and party support determine the choice; the government need not wait for a historical succession date.'),
        'golda_panthers':('Hear Development-Town Representatives','Housing, education and employment grievances give municipal activists reason to approach the cabinet. A hearing can respond to those demands before frustration grows into a wider political confrontation.'),
    }
    for short,(label,description) in text.items():
        node=nodes['ISR70_'+short]
        node.update(label=label,description=description,note=description)
        idea=data['idea_definitions'].get(short+'_idea')
        if idea:idea.update(label=label,treatment=description)
    for short in ('golda_succession','golda_panthers'):
        node=nodes['ISR70_'+short]
        node['available']=re.sub(r'(?m)^date\s*>\s*\d+\.\d+\.\d+\s*\n?','',node['available']).strip()
    readiness=nodes['ISR70_armed_stalemate']
    readiness['modifiers']['personnel_cost_multiplier_modifier']=.03
    data['idea_definitions']['armed_stalemate_idea']['modifiers']=dict(readiness['modifiers'])
    data['roleplay_revision']={'project':'IMPERIA COLD WAR','revision':1,
        'prerequisites':PREREQUISITES,'removed_exclusion':['ISR70_ceasefire','ISR70_armed_stalemate'],
        'removed_calendar_gates':['ISR70_golda_succession','ISR70_golda_panthers'],
        'principle':'Players initiate diplomatic proposals; recipients retain acceptance/refusal. Territorial administration does not require a historical ceasefire sequence.'}
    return data
