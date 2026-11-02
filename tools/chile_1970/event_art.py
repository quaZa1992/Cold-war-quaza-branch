# IMPERIA COLD WAR — Chile 1970 event-picture selection.
"""Preserve the selected restored photographs when rebuilding Chile's tree."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'south_america_event_art'))
from sa_photo_catalogue import CHILE, PREFIX, GFX, picture_for, registry_text
from sa_photo_export import build_assets

EVENT_PICTURES = {'COLDWAR_CHL_event_'+key:PREFIX+asset for key,asset in CHILE.items()}


def build():
    """Emit the shared native-frame registry and retain the reviewed masters."""
    build_assets()
    return {GFX:registry_text()}
