# IMPERIA COLD WAR — Bounded native recognition integration.
"""Keep native MD ownership and unrelated event content intact; fail on source drift."""
from pathlib import Path


def apply_recognition_hooks(root):
    effects_path = Path(root) / 'common/scripted_effects/01_international_systems_effects.txt'
    effects = effects_path.read_text(encoding='utf-8-sig')
    generated_path = Path(root) / 'common/scripted_effects/COLDWAR_diplomacy_1970.txt'
    generated = generated_path.read_text(encoding='utf-8-sig')
    assert 'COLDWAR_Germany_recognition_pp_once = {' in generated, 'German recognition PP receipt effect is missing'
    # IMPERIA COLD WAR — Reapply the bounded German-only reward guard when native MD is rebuilt.
    pp_before = '''	if = { limit = { PREV = { has_idea = non_power } } add_political_power = 5 }
	else_if = { limit = { PREV = { has_idea = minor_power } } add_political_power = 10 }
	else_if = { limit = { PREV = { has_idea = regional_power } } add_political_power = 15 }
	else_if = { limit = { PREV = { has_idea = large_power } } add_political_power = 25 }
	else_if = { limit = { PREV = { has_idea = great_power } } add_political_power = 50 }
	else_if = { limit = { PREV = { has_idea = super_power } } add_political_power = 100 }'''
    pp_after = '''	# IMPERIA COLD WAR — German 1970 recognition pays each distinct recogniser once; all other callers retain native MD tiers.
	if = { limit = { COLDWAR_Germany_recognition_subject = yes IMP_is_1970_scenario = yes } COLDWAR_Germany_recognition_pp_once = yes }
	else = {
		if = { limit = { PREV = { has_idea = non_power } } add_political_power = 5 }
		else_if = { limit = { PREV = { has_idea = minor_power } } add_political_power = 10 }
		else_if = { limit = { PREV = { has_idea = regional_power } } add_political_power = 15 }
		else_if = { limit = { PREV = { has_idea = large_power } } add_political_power = 25 }
		else_if = { limit = { PREV = { has_idea = great_power } } add_political_power = 50 }
		else_if = { limit = { PREV = { has_idea = super_power } } add_political_power = 100 }
	}'''
    if pp_after not in effects:
        assert effects.count(pp_before) == 1, 'Native recognition PP tiers have drifted'
        effects = effects.replace(pp_before, pp_after, 1)
        effects_path.write_text(effects, encoding='utf-8', newline='\n')
    assert effects.count('COLDWAR_Germany_recognition_pp_once = yes') == 1, 'German PP guard is missing or duplicated'
    path = Path(root) / 'events/International Recognition.txt'
    text = path.read_text(encoding='utf-8-sig')
    original = text
    before = '''\t\t\trecognition_grant_increment = yes
\t\t\tROOT = {
\t\t\t\tif = {
\t\t\t\t\tlimit = { NOT = { is_in_array = { recognised_countries = PREV } } }
\t\t\t\t\tadd_to_array = { recognised_countries = PREV }
\t\t\t\t}
\t\t\t}'''
    after = before.removeprefix('\t\t\trecognition_grant_increment = yes\n') + '''
\t\t\t# IMPERIA COLD WAR — Count and notify only after recognition is present in the native ledger.
\t\t\trecognition_grant_increment = yes'''
    if after not in text:
        assert text.count(before) == 1, 'Recognition pressure event has drifted'
        text = text.replace(before, after, 1)
    before = '''\t\tname = recognition.31.b
\t\tlog = "[GetDateText]: [This.GetName]: recognition.31.b"
\t\tif = {
\t\t\tlimit = { NOT = { is_in_array = { recognised_countries = FROM } } }
\t\t\tadd_to_array = { recognised_countries = FROM }'''
    after = before + '''
\t\t\t# IMPERIA COLD WAR — Update the German dossier immediately, independently of the later reply event.
\t\t\tFROM = { if = { limit = { COLDWAR_Germany_recognition_subject = yes } COLDWAR_Germany_recount_recognition = yes } }'''
    if after not in text:
        assert text.count(before) == 1, 'Recognition independence event has drifted'
        text = text.replace(before, after, 1)
    marker = '# IMPERIA COLD WAR — German recognition integration in native MD events.\n'
    if not text.startswith(marker):
        text = marker + text
    if text != original:
        path.write_text(text, encoding='utf-8', newline='\n')


if __name__ == '__main__':
    apply_recognition_hooks(Path(__file__).resolve().parents[2])
