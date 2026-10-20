"""Localize decision requirements without changing their executable predicates."""
from pathlib import Path
import hashlib
import json
from validate_content import parse, first
from presentation import FLAG_TEXT
from politics import LEADERS, PARTIES

PREFIX = 'COLDWAR_SYR_'
FLAGS = {
    **FLAG_TEXT,
    'appeals_commission_open': 'An independent citizenship appeals commission is open.',
    'land_settlement_decided': 'The cabinet has decided the Jazira land-settlement policy.',
    'national_pact': 'A constitutional pact permitting legal opposition and competitive elections has been accepted.',
    'military_transfer_agreed': 'The military cabinet has agreed to transfer authority to civilian institutions.',
    'internal_crisis': 'An unresolved domestic unrest crisis is under way.',
    'security_response_used': 'Emergency security operations have already been authorized.',
    'security_scrutiny_requested': 'Foreign scrutiny of the security operations has already been requested.',
    'president_incapacitated': 'The president is incapacitated and a succession conference is required.',
    'rival_guard_commands': 'Rival guard commands remain a source of conflict.',
    'reopen_citizenship_review': 'The government has agreed to reopen the citizenship registers.',
    'pact_rejected': 'An earlier constitutional pact proposal was rejected.',
    'crop_crisis': 'Failed harvests have caused an agricultural emergency.',
    'operational_mandate': 'The war cabinet has authorized the Golan operational mandate.',
    'window_committed': 'An offensive operational window has already been funded.',
    'window_authorization_pending': 'The cabinet is considering an offensive operational window.',
    'bridge_credit_taken': 'Emergency campaign credit has already been drawn.',
    'notice_sent': 'The government has already sent its limited-war notice to Israel.',
    'notice_pending': 'Israel has not yet answered the limited-war notice.',
    'mediation_pending': 'A disengagement proposal is awaiting an Israeli response.',
    'egypt_offer_pending': 'Egypt has not yet answered the operational coordination proposal.',
    'training_request_pending': 'A request for Soviet military training is awaiting an answer.',
    'credit_pending': 'A development-loan request is awaiting an answer.',
    'credit_drawn_recently': 'A development loan has recently been drawn.',
    'friendship_pending': 'The Soviet government has not yet answered the friendship treaty proposal.',
    'project_pending': 'The selected government has not yet answered the civil-project proposal.',
    'project_selection_pending': 'A donor must be selected before the civil-project proposal can be sent.',
    'foreign_project_completed': 'The agreed foreign-funded development project has been completed.',
    'pipeline_pending': 'Iraq has not yet answered the pipeline transit proposal.',
    'pipeline_operating': 'The agreed Iraqi–Syrian pipeline transit contract is operating.',
    'federal_offer_pending': 'The proposed Arab cooperation agreement is awaiting an answer.',
    'golan_offer_pending': 'Israel has not yet answered the Golan negotiating proposal.',
    'joint_plan_pending': 'Egypt has not yet answered the peacetime staff-cooperation proposal.',
    'lebanon_pending': 'Lebanon has not yet answered the offer of security assistance.',
    'lebanon_invitation': 'Lebanon has issued an active invitation for Syrian security assistance.',
    'lebanon_mission': 'An invited Syrian assistance mission is active in Lebanon.',
    'hard_currency_crisis': 'A shortage of foreign exchange requires a cabinet response.',
    'currency_package_active': 'A temporary foreign-exchange adjustment package is already in force.',
    'iran_supply_pending': 'Iran has not yet answered the supply and credit proposal.',
    'iranian_supply_counterparty': 'The post-revolutionary Iranian government is available for supply negotiations.',
}
TRIGGERS = {
    'COLDWAR_SYR_golan_objective_unresolved': 'Israel exists, controls the Golan and is outside our faction; Syria has not recovered the Golan.',
    'COLDWAR_SYR_campaign_is_valid': 'Israel controls the Golan, is outside our faction, and Syria is at war with Israel or holds a war goal against it.',
    'COLDWAR_SYR_training_can_request': 'The Soviet Union is available for cooperation: neither a Soviet training mission nor another Soviet aid request is active, the two countries are at peace, and Syria can pay the $0.060 billion hosting cost.',
}
FRACTIONS = {'quarter': '0.25', 'half': '0.50', 'three_quarter': '0.75'}


def emit(body):
    return '\n'.join(str(v) if k == '_bare' else '{\n'+emit(v)+'\n}' if k == '_list' else k+' '+op+' '+('{\n'+emit(v)+'\n}' if isinstance(v, list) else v) for k, op, v in body)


def semantic(body):
    """Remove presentation wrappers while retaining all gameplay predicates."""
    result = []
    for key, op, value in body:
        if key == 'tooltip':
            continue
        if key in ('custom_trigger_tooltip', 'hidden_trigger', 'hidden_effect') and isinstance(value, list):
            result.extend(semantic([item for item in value if item[0] != 'tooltip']))
        else:
            result.append((key, op, semantic(value) if isinstance(value, list) else value))
    return result


def install(root, data, write):
    root = Path(root)
    focus_ids = {n['id'] for n in data['nodes']}
    decisions = {d['id'] for d in data['decisions']}
    labels = {}
    counts = {'decisions': 0, 'wrapped_requirements': 0, 'hidden_technical_requirements': 0}

    def flag_text(ident):
        suffix = ident.removeprefix(PREFIX)
        if ident.endswith('_implemented') and ident[:-12] in focus_ids:
            return 'The programme §Y$'+ident[:-12]+'$§! has been implemented.'
        if ident.endswith('_completed') and ident[:-10] in decisions:
            return '§Y$'+ident[:-10]+'$§! has already been carried out.'
        if suffix.startswith('leader_'):
            person = LEADERS[suffix.removeprefix('leader_')][0] if suffix != 'leader_jadid' else 'Salah Jadid'
            return person+' directs the governing programme.'
        assert suffix in FLAGS, ('Untranslated decision flag', ident)
        return FLAGS[suffix]

    def variable_text(value):
        if first(value, 'var') == 'treasury':
            cost = first(value, 'value')
            amount = next((v for k, v in FRACTIONS.items() if cost == PREFIX+'cost_'+k+'_percent_gdp'), None)
            assert amount, ('Unknown GDP appropriation', value)
            return 'The treasury can fund an appropriation of §Y'+amount+'% of current GDP§!.'
        variable, comparison, target = value[0]
        if variable == 'ruling_party':
            assert comparison == '=' and int(target) in PARTIES
            return '§Y$COLDWAR_SYR_party_'+target+'$§! leads the government.'
        if variable.startswith('party_banned_array^'):
            slot = variable.split('^')[1]
            assert int(slot) in PARTIES and comparison == '=' and target == '0'
            return '§Y$COLDWAR_SYR_party_'+slot+'$§! is legally registered.'
        if variable.startswith('party_pop_array^'):
            slot = variable.split('^')[1]
            assert int(slot) in PARTIES and comparison == '>'
            return '§Y$COLDWAR_SYR_party_'+slot+'$§! has at least '+f'{(float(target)+.000001)*100:g}'+'% public support.'
        if variable == 'treasury':
            assert comparison == '>'
            return 'At least §Y$'+f'{float(target)+.000001:.3f}'+' billion§! is available in the treasury.'
        if variable == PREFIX+'baath_head':
            assert comparison == '=' and target == '0'
            return 'Nureddin al-Atassi remains the formal president.'
        counters = {
            'officer_backing': 'Officer backing has not yet reached its maximum.',
            'citizenship_stages': 'Fewer than three stages of citizenship appeals have been completed.',
            'enterprise_audits': 'Fewer than three enterprise-contract investigations have been completed.',
            'irrigation_trials': 'Fewer than three irrigation and drainage trials have been completed.',
        }
        short = variable.removeprefix(PREFIX)
        assert short in counters, ('Untranslated decision variable', value)
        if comparison == '<' and target == '3':
            return counters[short]
        if comparison == '>' and target == '2':
            return counters[short].replace('Fewer than three', 'Three')
        raise AssertionError(('Untranslated decision comparison', value))

    def present(body):
        result = []
        for key, op, value in body:
            # Existing reviewed focus-requirement wrappers already carry real labels.
            if key in ('custom_trigger_tooltip', 'hidden_trigger'):
                result.append((key, op, value))
                continue
            technical = key in ('original_tag', 'IMP_is_1970_scenario')
            if key == 'has_country_flag' and value == 'mdcw_cw_initialized':
                technical = True
            if key == 'check_variable' and isinstance(value, list):
                technical |= value[0][0] == 'gdp_total' or value[0][0].startswith(PREFIX+'cost_')
            if technical:
                result.append(('hidden_trigger', '=', [(key, op, value)]))
                counts['hidden_technical_requirements'] += 1
                continue
            text = None
            if key == 'has_country_flag' and isinstance(value, str) and value.startswith(PREFIX):
                text = flag_text(value)
            elif key == 'check_variable':
                text = variable_text(value)
            elif key == 'is_in_array' and isinstance(value, list) and value[0][0] == 'gov_coalition_array':
                slot = value[0][2]
                assert int(slot) in PARTIES
                text = '§Y$COLDWAR_SYR_party_'+slot+'$§! participates in the governing coalition.'
            elif key in TRIGGERS:
                assert value == 'yes'
                text = TRIGGERS[key]
            if text:
                assert isinstance(text, str), ('Invalid requirement localization', key, text)
                ident = PREFIX+'requirement_'+hashlib.sha256(emit([(key, op, value)]).encode()).hexdigest()[:16]
                assert ident not in labels or labels[ident] == text
                labels[ident] = text
                result.append(('custom_trigger_tooltip', '=', [('tooltip', '=', ident), (key, op, value)]))
                counts['wrapped_requirements'] += 1
            else:
                result.append((key, op, present(value) if isinstance(value, list) else value))
        return result

    def present_effects(body):
        result = []
        progress = {
            PREFIX+'officer_backing': 'Officer backing: §G+1§! (maximum 3).',
            PREFIX+'citizenship_stages': 'Completed citizenship appeals: §G+1 stage§! (3 required).',
            PREFIX+'enterprise_audits': 'Completed enterprise-contract investigations: §G+1§! (3 required).',
            PREFIX+'irrigation_trials': 'Completed irrigation and drainage trials: §G+1§! (3 required).',
        }
        for key, op, value in body:
            if key == 'hidden_effect':
                result.append((key, op, value))
            elif key in ('clamp_variable', 'COLDWAR_SYR_update_operation_costs', 'COLDWAR_SYR_refresh_programmes', 'update_money_dirty_variable'):
                result.append(('hidden_effect', '=', [(key, op, value)]))
            elif key == 'limit':
                result.append((key, op, present(value)))
            elif key == 'add_to_variable' and isinstance(value, list) and value[0][0] in progress:
                variable = value[0][0]
                assert value[0][1:] == ('=', '1')
                tip = variable+'_change_tt'
                labels[tip] = progress[variable]
                result.append((key, op, value+[('tooltip', '=', tip)]))
            else:
                result.append((key, op, present_effects(value) if isinstance(value, list) else value))
        return result

    for path in sorted((root/'common/decisions').glob('COLDWAR_SYR*.txt')):
        original = parse(path.read_text(encoding='utf-8-sig'))
        updated = []
        for category_id, op, category in original:
            entries = []
            for ident, decision_op, body in category:
                if not isinstance(body, list):
                    entries.append((ident, decision_op, body))
                    continue
                counts['decisions'] += 1
                fields = []
                for key, field_op, value in body:
                    if key in ('available', 'target_trigger', 'cancel_trigger', 'remove_trigger'):
                        value = present(value)
                    elif key in ('complete_effect', 'remove_effect', 'cancel_effect', 'timeout_effect'):
                        value = present_effects(value)
                    fields.append((key, field_op, value))
                entries.append((ident, decision_op, fields))
            updated.append((category_id, op, entries))
        # Includes every untouched effect, timing, price, scope and visibility rule.
        assert semantic(original) == semantic(updated), ('Decision semantics changed', path)
        assert parse(emit(updated)) == updated, ('Decision serialization changed AST', path)
        counts.setdefault('gameplay_sha256', {})[path.relative_to(root).as_posix()] = hashlib.sha256(json.dumps(semantic(original), separators=(',', ':')).encode()).hexdigest()
        write(path.relative_to(root).as_posix(), '# COLDWAR | Generated decision requirements.\n'+emit(updated))
    # These public helpers contribute conditional text to decision tooltips too.
    # Do not recode weekly logic or unrelated helpers while polishing their UI.
    path = root/'common/scripted_effects/COLDWAR_SYR_foreign_effects.txt'
    original = parse(path.read_text(encoding='utf-8-sig'))
    exposed = {'COLDWAR_SYR_create_limited_wargoal', 'COLDWAR_SYR_request_sanctions_review'}
    updated = [(key, op, present_effects(body) if key in exposed else body) for key, op, body in original]
    assert semantic(original) == semantic(updated), 'Foreign helper semantics changed'
    assert parse(emit(updated)) == updated, 'Foreign helper serialization changed AST'
    counts['gameplay_sha256'][path.relative_to(root).as_posix()] = hashlib.sha256(json.dumps(semantic(original), separators=(',', ':')).encode()).hexdigest()
    counts['public_helpers_checked'] = len(exposed)
    write(path.relative_to(root).as_posix(), '# COLDWAR | Generated foreign contracts and localized decision helpers.\n'+emit(updated))
    lines = ['l_english:']+[f' {key}:0 '+json.dumps(value, ensure_ascii=False) for key, value in sorted(labels.items())]
    write('localisation/english/COLDWAR_SYR_decision_requirements_l_english.yml', '\n'.join(lines)+'\n', True)
    counts['english_requirement_labels'] = len(labels)
    counts['gameplay_semantics_unchanged'] = True
    (root/'tools/syria_1970/decision_presentation_build.json').write_text(json.dumps(counts, indent=2)+'\n', encoding='utf-8')
