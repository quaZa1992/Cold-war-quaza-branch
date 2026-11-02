# IMPERIA COLD WAR — Compact Cyprus 1970 integration.
"""Retired large-tree entry point. Compile the approved compact replacement."""
from pathlib import Path
import runpy
import sys
target = Path(__file__).resolve().parents[1] / 'cyprus_1970_rework' / 'compile.py'
sys.path.insert(0, str(target.parent))
if '--check' not in sys.argv and '--install' not in sys.argv:
    sys.argv.append('--install')
runpy.run_path(str(target), run_name='__main__')
