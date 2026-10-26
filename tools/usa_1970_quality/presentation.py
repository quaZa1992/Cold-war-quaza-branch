# IMPERIA CW — Cold War: usa 1970 quality — presentation.
"""Preserve runtime conditions while hiding internal focus-routing plumbing."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from focus_prerequisite_ui import nodes, field, hide_redundant_prerequisites

def hide_routing(text):
    edits=[]
    routing={'original_tag','tag','exists','IMP_is_1970_scenario','is_ai'}
    def leaves(node):
        return [leaf for child in node.children() for leaf in leaves(child)] if isinstance(node.value,list) else [node]
    def internal(node):
        if node.key in routing:return True
        if node.key=='has_country_flag' and str(node.value).endswith(('human_seat_reserved','dedicated_historical_ai')):return True
        if node.key in ('AND','OR','NOT'):
            flat=leaves(node)
            # Date tests inside an AI reservation policy are routing, not a
            # historical formation date for the player's programme.
            if any(x.key=='is_ai' for x in flat):
                return all(x.key in routing|{'date'} or internal(x) for x in flat)
        return False
    def visit(node):
        if node.key in ('hidden_trigger','custom_trigger_tooltip'):return
        if internal(node):
            edits.append((node.start,node.end,'hidden_trigger = { '+text[node.start:node.end]+' }'))
        elif node.key in ('AND','OR','NOT'):
            for child in node.children():visit(child)
    for n in nodes(text):visit(n)
    for start,end,value in sorted(edits,reverse=True):text=text[:start]+value+text[end:]
    return text

def focus_availability(text, groups):
    return hide_routing(hide_redundant_prerequisites(text,groups))

def patch_usa(text):
    edits=[]
    for root in nodes(text):
        if root.key!='focus_tree':continue
        for focus in root.children():
            if focus.key!='focus':continue
            fid=field(focus.children(),'id')
            groups=[[p.value for p in n.children() if p.key=='focus'] for n in focus.children() if n.key=='prerequisite']
            for available in focus.children():
                if available.key!='available':continue
                body=text[available.start:available.end]
                left=body.index('{')+1;right=body.rfind('}')
                condition=body[left:right]
                # Keep the actual presidency and term-end checks. Give the
                # combined condition a native, readable label, without flags.
                if str(fid).startswith('USA_1970_NIX_'):
                    terms=nodes(condition)
                    term=[n for n in terms if (n.key=='has_country_flag' and n.value=='USA_1970_nixon_presidency') or (n.key=='date' and n.op=='<' and n.value=='1973.1.20')]
                    if term:
                        pieces=[condition[n.start:n.end] for n in term]
                        for n in sorted(term,key=lambda n:n.start,reverse=True):condition=condition[:n.start]+condition[n.end:]
                        condition+='\ncustom_trigger_tooltip = { tooltip = USA_1970_nixon_first_term_tt '+ ' '.join(pieces)+' }\n'
                updated=focus_availability(condition,groups)
                edits.append((available.start,available.end,'available = {'+updated+'}'))
    for start,end,replacement in sorted(edits,reverse=True):text=text[:start]+replacement+text[end:]
    return text
