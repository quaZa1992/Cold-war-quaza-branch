# IMPERIA COLD WAR — Canonical entry point for current France programme tests.
"""V4 test implementation is archived; run the independent V5 AST suite."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('test_core_v5.py')), run_name='__main__')
