# IMPERIA COLD WAR — Chile authorized cost and compact-layout revision.
"""Keep the original approval immutable and apply the user's later revisions."""
import json
from pathlib import Path
from cost_revision import apply_costs
from layout_revision import apply_layout
from political_revision import apply_politics

def load_design(path=None):
    source=Path(path) if path else Path(__file__).resolve().parent/'approved_design.json'
    return apply_politics(apply_layout(apply_costs(json.loads(source.read_text(encoding='utf-8')))))
