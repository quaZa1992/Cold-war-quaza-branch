# IMPERIA CW — Cold War: retired Spain authoring entry point.
"""Compatibility redirect. The rejected Spain design is archived outside the mod."""
from pathlib import Path
import runpy,sys
target=Path(__file__).resolve().parents[1]/'spain_1970_v2'/'compile.py'
sys.path.insert(0,str(target.parent))
runpy.run_path(str(target),run_name='__main__')
