"""Compatibility entry point for the current English Israel compiler.

The original design input is preserved in design_source.json. Runtime layout,
party access and rewards are maintained by the modules imported by build_content.
"""
from pathlib import Path
import subprocess
import sys

if __name__ == '__main__':
    here=Path(__file__).resolve().parent
    subprocess.run([sys.executable,str(here/'build_content.py')],check=True)
    subprocess.run([sys.executable,str(here/'update_documents.py')],check=True)
