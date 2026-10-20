"""Supply the inverse text HOI4 implicitly requests for negated requirements."""
from pathlib import Path
import json
import re
from validate_content import parse, walk, first


def inverse(text):
    overrides = {
        'The party and officer corps have accepted a command settlement.': 'The party and officer corps have not yet accepted a command settlement.',
        'Officer backing has not yet reached its maximum.': 'Officer backing has reached its maximum.',
        'Israel has not yet answered the limited-war notice.': 'No limited-war notice is awaiting an Israeli response.',
        'Egypt has not yet answered the operational coordination proposal.': 'No operational coordination proposal is awaiting an Egyptian response.',
        'The Soviet government has not yet answered the friendship treaty proposal.': 'No friendship treaty proposal is awaiting a Soviet response.',
        'The selected government has not yet answered the civil-project proposal.': 'No civil-project proposal is awaiting the selected government\'s response.',
        'A donor must be selected before the civil-project proposal can be sent.': 'No donor-selection process is pending for a civil-project proposal.',
        'Iraq has not yet answered the pipeline transit proposal.': 'No pipeline transit proposal is awaiting an Iraqi response.',
        'Israel has not yet answered the Golan negotiating proposal.': 'No Golan negotiating proposal is awaiting an Israeli response.',
        'Egypt has not yet answered the peacetime staff-cooperation proposal.': 'No peacetime staff-cooperation proposal is awaiting an Egyptian response.',
        'Lebanon has not yet answered the offer of security assistance.': 'No security assistance offer is awaiting a Lebanese response.',
        'Iran has not yet answered the supply and credit proposal.': 'No supply and credit proposal is awaiting an Iranian response.',
    }
    if text in overrides:
        return overrides[text]
    if text.startswith('Fewer than three'):
        return text.replace('Fewer than three', 'Three', 1)
    if text.startswith('At least '):
        return text.replace('At least ', 'Less than ', 1)
    if ';' in text or ', ' in text or ' and ' in text:
        return 'The following requirement is not satisfied: '+text
    if ' has not yet ' in text:
        return text.replace(' has not yet ', ' has already ', 1)
    if ' have not yet ' in text:
        return text.replace(' have not yet ', ' have already ', 1)
    if ' has already ' in text:
        return text.replace(' has already ', ' has not yet ', 1)
    if ' have already ' in text:
        return text.replace(' have already ', ' have not yet ', 1)
    if ' has been ' in text:
        return text.replace(' has been ', ' has not been ', 1)
    if ' have been ' in text:
        return text.replace(' have been ', ' have not been ', 1)
    # Composite requirements must negate the whole conjunction, not just one verb.
    if ';' not in text and ', ' not in text and ' and ' not in text:
        for verb, negative in (('leads', 'does not lead'), ('directs', 'does not direct'), ('participates', 'does not participate'), ('remains', 'does not remain'), ('can', 'cannot'), ('is', 'is not'), ('are', 'are not')):
            pattern = r'\b'+verb+r'\b'
            if re.search(pattern, text):
                return re.sub(pattern, negative, text, count=1)
    return 'The following requirement is not satisfied: '+text


def install(root, write):
    root = Path(root)
    output = 'COLDWAR_SYR_negative_requirements_l_english.yml'
    loc = {}
    for path in (root/'localisation/english').glob('COLDWAR_SYR*.yml'):
        if path.name == output:
            continue
        for key, value in re.findall(r'^\s+(\S+):\d+\s+(".*")\s*$', path.read_text(encoding='utf-8-sig'), re.M):
            loc[key] = json.loads(value)
    references = set()
    for directory in ('common/national_focus', 'common/decisions', 'common/scripted_effects', 'events'):
        for path in (root/directory).glob('COLDWAR_SYR*.txt'):
            for key, _, value in walk(parse(path.read_text(encoding='utf-8-sig'))):
                if key == 'custom_trigger_tooltip' and isinstance(value, list):
                    tip = first(value, 'tooltip')
                    if isinstance(tip, str) and tip.startswith('COLDWAR_SYR_'):
                        references.add(tip)
    lines = ['l_english:']
    for key in sorted(references):
        assert isinstance(loc.get(key), str), ('Missing positive requirement text', key)
        if key+'_NOT' not in loc:
            lines.append(' '+key+'_NOT:0 '+json.dumps(inverse(loc[key]), ensure_ascii=False))
    write('localisation/english/'+output, '\n'.join(lines)+'\n', True)
    return len(references)
