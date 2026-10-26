# IMPERIA CW — Cold War: iraq 1970 — flavour.
"""English national narratives, separate from the frozen mechanical design."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def descriptions():
    result={}
    for name in ('flavour_politics.json','flavour_national.json'):
        part=json.loads((HERE/name).read_text(encoding='utf-8-sig'))
        assert not result.keys() & part.keys(),('Repeated focus narrative',name)
        result.update(part)
    approved=json.loads((HERE/'approved_iraq.json').read_text(encoding='utf-8-sig'))
    assert result.keys()=={n['id'] for n in approved['nodes']},'Incomplete Iraqi focus narratives'
    assert all(isinstance(v,str) and v.strip() for v in result.values())
    return result
