# IMPERIA CW — Cold War: emitted-tree preview entry point.
"""Render current emitted positions, native focus art and all sections."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("render_presentation.py")), run_name="__main__")
