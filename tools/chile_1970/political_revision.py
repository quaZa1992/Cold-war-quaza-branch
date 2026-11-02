# IMPERIA COLD WAR — Chile player-directed military transition.
"""Authorized political-route amendment; retain the immutable approval snapshot."""

INTERVENTION_PP = 100
INTERVENTION_DAYS = 90


def apply_politics(data):
    for node in data['nodes']:
        if node['key'] == 'military_staff':
            node['description'] += (' A civilian government can open talks with the officer corps through Secure the Officer Corps in Chile: Political Transition. '
                                    'The resulting constitutional crisis offers civilian guarantees or a military takeover; the junta then chooses collective authority or Augusto Pinochet.')
        elif node['key'] == 'pinochet_command':
            node['description'] += (' To bring Pinochet to power without an election, prepare a military intervention through Chile: Political Transition, '
                                    'permit the service chiefs to take office and choose Pinochet for the junta presidency.')
    junta = next(event for event in data['events'] if event['key'] == 'junta')
    junta['description'] = ('The service chiefs must settle the leadership of their new government. Collective authority leaves room for a constitutional exit; '
                            'concentrating the presidency under Augusto Pinochet places the armed forces behind a personal executive. '
                            'Historically, Pinochet chaired the junta from September 1973. An earlier appointment would break with the existing command hierarchy.')
    return data
