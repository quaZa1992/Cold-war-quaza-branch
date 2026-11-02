# IMPERIA COLD WAR — narrow SSR tree, Union Plan and finance integrations.
from pathlib import Path
import shared

ROOT=shared.ROOT
HEADER='# IMPERIA COLD WAR — Universal SSR focus programme integration.\n'

def patch(path,transform):
    text=path.read_text(encoding='utf-8-sig')
    changed=transform(text)
    if not changed.startswith(HEADER):changed=HEADER+changed
    if changed!=text:path.write_text(changed,encoding='utf-8')
    return str(path.relative_to(ROOT))

def generate():
    outputs=[]
    for tag in shared.TAGS:
        paths=list((ROOT/'history/countries').glob(tag+' - *.txt'))
        assert len(paths)==1,(tag,paths)
        outputs.append(patch(paths[0],lambda s:s.replace('load_focus_tree = mdcw_1970_generic_focus','load_focus_tree = COLDWAR_SSR_1970_focus')))

    start='# IMPERIA COLD WAR — SSR weekly programme expenses BEGIN'
    end='# IMPERIA COLD WAR — SSR weekly programme expenses END'
    code=start+'\n\tCOLDWAR_SSR_add_weekly_expenses = yes\n\t'+end
    def finance(text):
        if start in text:
            return text[:text.index(start)]+code+text[text.index(end)+len(end):]
        anchor='\t# IMPERIA CW — Cold War: Economic calibration and weekly finances.\n\t# Current Cold War monthly programme/bloc costs enter weekly accounts once.'
        assert text.count(anchor)==1
        return text.replace(anchor,code+'\n'+anchor,1)
    outputs.append(patch(ROOT/'common/scripted_effects/00_money_system.txt',finance))

    # Old donor events may request a fallback tree long after scenario startup.
    # Preserve this authored tree and every completed focus on that route too.
    fstart='# IMPERIA COLD WAR — SSR authored-tree exemption BEGIN'
    fend='# IMPERIA COLD WAR — SSR authored-tree exemption END'
    exemption=fstart+'\n\t\t\t\t\tAND = { IMP_is_1970_scenario = yes has_focus_tree = COLDWAR_SSR_1970_focus }\n\t\t\t\t\t'+fend
    def fallback(text):
        if fstart in text:return text[:text.index(fstart)]+exemption+text[text.index(fend)+len(fend):]
        anchor='\t\t\t\tOR = {\n'
        assert text.count(anchor)==1
        return text.replace(anchor,anchor+'\t\t\t\t\t'+exemption+'\n',1)
    outputs.append(patch(ROOT/'common/scripted_effects/mdcw_1970_focus_tree_effects.txt',fallback))

    budget='''COLDWAR_SSR_add_weekly_expenses = {
	COLDWAR_SSR_lifecycle_refresh_budget = yes
	COLDWAR_SSR_market_refresh_budget = yes
	COLDWAR_SSR_diplomacy_refresh_budget = yes
	add_to_variable = { additional_expenses_rate = COLDWAR_SSR_lifecycle_weekly_expense }
	add_to_variable = { additional_expenses_rate = COLDWAR_SSR_market_weekly_expense }
	add_to_variable = { additional_expenses_rate = COLDWAR_SSR_diplomacy_weekly_expense }
}

# Called only by a settlement that has actually recognised this country.
COLDWAR_SSR_record_union_successor = {
	if = { limit = { IMP_is_1970_scenario = yes is_subject = no }
		save_global_event_target_as = COLDWAR_SSR_recognised_union_successor
	}
}
'''
    outputs.append(shared.write('common/scripted_effects/COLDWAR_SSR_finance.txt',budget))

    ustart='# IMPERIA COLD WAR — SSR Union Plan position BEGIN'
    uend='# IMPERIA COLD WAR — SSR Union Plan position END'
    offset=ustart+'\n\toffset = {\n\t\tx = -285\n\t\ty = -8\n\t\ttrigger = { has_focus_tree = COLDWAR_SSR_1970_focus }\n\t}\n\t'+uend
    def union(text):
        if ustart in text:return text[:text.index(ustart)]+offset+text[text.index(uend)+len(uend):]
        anchor='\tcost = 2\n'
        assert anchor in text
        return text.replace(anchor,'\t'+offset+'\n'+anchor,1)
    outputs.append(patch(ROOT/'common/national_focus/COLDWAR_UNI_1970_union_joint.txt',union))

    # Preserve the same narrow attachment when the owning Soviet generator runs.
    generator=ROOT/'Claude outputs/COLDWAR_SOV_generator/cw_union.py'
    def union_generator(text):
        marker='# IMPERIA COLD WAR: SSR joint-tree host offset'
        if marker in text:return text
        anchor='"trigger = { has_focus_tree = mdcw_1970_generic_focus }", "}"]'
        assert text.count(anchor)==1
        addition='\n            '+marker+'\n            L += ["# IMPERIA COLD WAR — SSR Union Plan position BEGIN", "offset = {", "x = -285", "y = -8", "trigger = { has_focus_tree = COLDWAR_SSR_1970_focus }", "}", "# IMPERIA COLD WAR — SSR Union Plan position END"]'
        return text.replace(anchor,anchor+addition,1)
    outputs.append(patch(generator,union_generator))
    return outputs
