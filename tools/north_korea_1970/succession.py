# IMPERIA CW — Cold War: North Korea 1994 succession and illustration export.
"""Deterministic emitter for the NKO 1994 succession scripts and news image.

The main scenario integration owns initialization and calls
COLDWAR_NKO_succession_daily in NKO scope each day.
"""

from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/COLDWAR_NKO_1970_concept/v2/assets/COLDWAR_NKO_1994_funeral_colorized.png"
TARGET = ROOT / "gfx/event_pictures/COLDWAR_NKO_1994_funeral.dds"
TARGET_SIZE = (410, 164)
EVENTS_PATH = ROOT / "events/COLDWAR_NKO_1970_succession_events.txt"
EFFECTS_PATH = ROOT / "common/scripted_effects/COLDWAR_NKO_1970_succession_effects.txt"
GFX_PATH = ROOT / "interface/COLDWAR_NKO_1970_news.gfx"
SCRIPT_FILES = (
    EVENTS_PATH,
    EFFECTS_PATH,
    GFX_PATH,
)
LOCALIZATION = ROOT / "localisation/english/COLDWAR_NKO_1970_succession_l_english.yml"
PORTRAIT = ROOT / "gfx/Leaders/NKO/Kim_Jong_il.dds"

EFFECTS = """# IMPERIA CW — Cold War: NKO historical death and succession.
# The 1970 leader expiry is 9 July so this 8 July event can identify the living incumbent.
COLDWAR_NKO_succession_daily = {
 if = {
  limit = { tag = NKO IMP_is_1970_scenario = yes NOT = { date < 1994.7.8 } date < 1994.7.9 NOT = { has_global_flag = COLDWAR_NKO_kim_il_sung_death_news_sent } }
  set_global_flag = COLDWAR_NKO_kim_il_sung_death_news_sent
  set_country_flag = COLDWAR_NKO_kim_il_sung_death_recorded
  if = {
   limit = { check_variable = { ruling_party = 4 } has_country_leader = { name = "Kim Il Sung" ruling_only = yes } }
   kill_country_leader = yes
   if = {
    limit = { NOT = { has_country_flag = COLDWAR_NKO_kim_jong_il_unavailable } }
    create_country_leader = { name = "Kim Jong-il" picture = "gfx/Leaders/NKO/Kim_Jong_il.dds" ideology = communist_state }
    set_country_flag = COLDWAR_NKO_kim_jong_il_succeeded
    set_global_flag = COLDWAR_NKO_1994_succession_announced
   }
  }
  COLDWAR_NKO_refresh_programmes = yes
  news_event = { id = COLDWAR_NKO_succession.1 }
 }
}
# Country daily scope. This fallback broadcasts the death even if NKO no longer exists.
COLDWAR_NKO_world_succession_daily = {
 if = {
  limit = { IMP_is_1970_scenario = yes NOT = { date < 1994.7.8 } date < 1994.7.9 NOT = { has_global_flag = COLDWAR_NKO_kim_il_sung_death_news_sent } }
  if = { limit = { country_exists = NKO } NKO = { COLDWAR_NKO_succession_daily = yes } }
  else = { set_global_flag = COLDWAR_NKO_kim_il_sung_death_news_sent news_event = { id = COLDWAR_NKO_succession.1 } }
 }
}
"""

EVENTS = """# IMPERIA CW — Cold War: NKO 1994 death and global succession news.
add_namespace = COLDWAR_NKO_succession

# One major news event, broadcast globally by the daily NKO helper.
news_event = {
\tid = COLDWAR_NKO_succession.1
\ttitle = COLDWAR_NKO_succession.1.t
\tdesc = {
\t\ttrigger = { has_global_flag = COLDWAR_NKO_1994_succession_announced }
\t\ttext = COLDWAR_NKO_succession.1.d_successor
\t}
\tdesc = {
\t\ttrigger = { NOT = { has_global_flag = COLDWAR_NKO_1994_succession_announced } }
\t\ttext = COLDWAR_NKO_succession.1.d_no_successor
\t}
\tpicture = GFX_COLDWAR_NKO_1994_funeral
\tis_triggered_only = yes
\tmajor = yes

\toption = { name = COLDWAR_NKO_succession.1.a }
}
"""

NEWS_GFX = """# IMPERIA CW — Cold War: NKO 1994 succession news illustration.
spriteTypes = {
\tspriteType = {
\t\tname = "GFX_COLDWAR_NKO_1994_funeral"
\t\ttexturefile = "gfx/event_pictures/COLDWAR_NKO_1994_funeral.dds"
\t}
}
"""

ENGLISH_LOCALIZATION = """l_english:
# IMPERIA CW — Cold War: North Korea 1994 succession news.
 COLDWAR_NKO_succession.1.t: "Kim Il Sung Has Died"
 COLDWAR_NKO_succession.1.d_successor: "Pyongyang has announced the death of Kim Il Sung at the age of 82. Kim Jong Il has assumed the leadership of North Korea, ending the founder’s forty-six years in power."
 COLDWAR_NKO_succession.1.d_no_successor: "Kim Il Sung, North Korea’s former leader, has died at the age of 82. His death closes the era of the Republic’s founding generation."
 COLDWAR_NKO_succession.1.a: "The end of an era."
"""


def emit_sources() -> None:
    """Deterministically emit the assigned event, effect, gfx and English localization files."""
    for path, text in ((EVENTS_PATH, EVENTS), (EFFECTS_PATH, EFFECTS), (GFX_PATH, NEWS_GFX)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
    LOCALIZATION.parent.mkdir(parents=True, exist_ok=True)
    localized = "\ufeff" + ENGLISH_LOCALIZATION.replace("\n", "\r\n")
    LOCALIZATION.write_bytes(localized.encode("utf-8"))


def convert_news_picture() -> Path:
    """Crop/resize the approved restoration to the MD news frame and encode BC3 DDS."""
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as source:
        image = source.convert("RGBA")
        width, height = image.size
        target_ratio = TARGET_SIZE[0] / TARGET_SIZE[1]
        crop_height = round(width / target_ratio)
        if crop_height > height:
            crop_width = round(height * target_ratio)
            left = (width - crop_width) // 2
            image = image.crop((left, 0, left + crop_width, height))
        else:
            # Keep the lower part of the procession visible while retaining the arch.
            top = min(max(0, round((height - crop_height) * 0.58)), height - crop_height)
            image = image.crop((0, top, width, top + crop_height))
        image = image.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        image.save(TARGET, format="DDS", pixel_format="BC3")
    with Image.open(TARGET) as result:
        if result.size != TARGET_SIZE:
            raise ValueError(f"Unexpected DDS dimensions: {result.size}")
    if TARGET.read_bytes()[:4] != b"DDS ":
        raise ValueError("Output is not a DDS texture")
    return TARGET


def check_script_encoding_and_braces() -> None:
    """Check the three new Clausewitz scripts for UTF-8/no-BOM and balanced blocks."""
    for path in SCRIPT_FILES:
        raw = path.read_bytes()
        if raw.startswith(bytes.fromhex("efbbbf")):
            raise ValueError(f"Script contains a UTF-8 BOM: {path}")
        text = raw.decode("utf-8")
        depth = 0
        quoted = escaped = comment = False
        for char in text:
            if comment:
                if char == "\n":
                    comment = False
                continue
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
                continue
            if char == "#":
                comment = True
            elif char == '"':
                quoted = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth < 0:
                    raise ValueError(f"Unmatched closing brace: {path}")
        if depth != 0 or quoted:
            raise ValueError(f"Unbalanced script structure: {path} (depth={depth})")
    if not LOCALIZATION.read_bytes().startswith(bytes.fromhex("efbbbf")):
        raise ValueError("English localization must have a UTF-8 BOM")
    if not PORTRAIT.is_file():
        raise FileNotFoundError(f"Expected native leader portrait is absent: {PORTRAIT}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        check_script_encoding_and_braces()
        with Image.open(TARGET) as image:
            if image.size != TARGET_SIZE:
                raise ValueError(f"Unexpected news DDS dimensions: {image.size}")
        print("NKO succession source checks passed")
    else:
        emit_sources()
        print(convert_news_picture())
