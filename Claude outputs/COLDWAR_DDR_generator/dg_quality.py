# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
"""Maintained runtime sources for the approved 20 October 2026 quality pass.

Kept separate from the legacy event/decision registry so new numeric IDs cannot
collide with the existing generated succession and treaty events.
"""
from pathlib import Path


def runtime_files():
    base = Path(__file__).resolve().parent / 'quality_runtime'
    return {p.relative_to(base).as_posix(): p.read_text(encoding='utf-8-sig')
            for p in base.rglob('*') if p.is_file()}
