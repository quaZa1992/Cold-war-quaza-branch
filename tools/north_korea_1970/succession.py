# IMPERIA COLD WAR — Cold War: North Korea 1994 succession and illustration export.
"""Deterministic emitter for the NKO 1994 succession scripts and news image.

The main scenario integration owns initialization and calls
COLDWAR_NKO_succession_daily in NKO scope each day.
"""

from __future__ import annotations

from pathlib import Path
import sys
import struct

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/COLDWAR_NKO_1970_concept/v2/assets/COLDWAR_NKO_1994_funeral_colorized.png"
TARGET = ROOT / "gfx/event_pictures/COLDWAR_NKO_1994_funeral.dds"
TARGET_SIZE = (410, 164)
EVENTS_PATH = ROOT / "events/COLDWAR_NKO_1970_succession_events.txt"
EFFECTS_PATH = ROOT / "common/scripted_effects/COLDWAR_NKO_1970_succession_effects.txt"
GFX_PATH = ROOT / "interface/COLDWAR_NKO_1970_news.gfx"
DECISIONS_PATH = ROOT / "common/decisions/COLDWAR_NKO_1970_succession.txt"
CATEGORY_PATH = ROOT / "common/decisions/categories/COLDWAR_NKO_1970_succession_category.txt"
SCRIPT_FILES = (
    EVENTS_PATH,
    EFFECTS_PATH,
    GFX_PATH,
    DECISIONS_PATH,
    CATEGORY_PATH,
)
LOCALIZATION = ROOT / "localisation/english/COLDWAR_NKO_1970_succession_l_english.yml"
PORTRAIT = ROOT / "gfx/Leaders/NKO/Kim_Jong_il.dds"
MEMORIAL_PORTRAIT = ROOT / "gfx/Leaders/NKO/COLDWAR_NKO_Kim_Il_Sung_memorial.dds"

EFFECTS = """# IMPERIA COLD WAR — Cold War: NKO historical death and succession.
# Catch up on loaded campaigns after 8 July 1994; the recorded death runs once.
COLDWAR_NKO_succession_daily = {
 if = {
  limit = { tag = NKO IMP_is_1970_scenario = yes NOT = { date < 1994.7.8 } NOT = { has_global_flag = COLDWAR_NKO_kim_il_sung_death_news_sent } }
  set_global_flag = COLDWAR_NKO_kim_il_sung_death_news_sent
  set_country_flag = COLDWAR_NKO_kim_il_sung_death_recorded
  if = {
   limit = { OR = { has_country_leader = { name = "Kim Il Sung" ruling_only = yes } has_country_leader = { name = "Kim Il-sung" ruling_only = yes } } }
   set_global_flag = COLDWAR_NKO_1994_kim_il_sung_died_in_office
   kill_country_leader = yes
   create_country_leader = { name = "Funeral Committee" picture = "gfx/Leaders/NKO/COLDWAR_NKO_Kim_Il_Sung_memorial.dds" ideology = communist_state }
   set_country_flag = COLDWAR_NKO_succession_pending
  }
  COLDWAR_NKO_refresh_programmes = yes
  news_event = { id = COLDWAR_NKO_succession.1 }
 }
}
# Called from the shared leader router while succession is pending. It preserves only the
# caretaker and never repeats the death transaction or its news.
COLDWAR_NKO_preserve_mourning_government = {
 if = {
  limit = {
   tag = NKO
   IMP_is_1970_scenario = yes
   check_variable = { ruling_party = 4 }
   has_country_flag = COLDWAR_NKO_kim_il_sung_death_recorded
   has_country_flag = COLDWAR_NKO_succession_pending
   NOT = { has_country_flag = COLDWAR_NKO_kim_jong_il_succeeded }
  }
  if = {
   limit = { NOT = { has_country_leader = { name = "Funeral Committee" ruling_only = yes } } }
   create_country_leader = { name = "Funeral Committee" picture = "gfx/Leaders/NKO/COLDWAR_NKO_Kim_Il_Sung_memorial.dds" ideology = communist_state }
  }
 }
}
# Country daily scope. Catch up on the recorded date even when NKO no longer exists.
COLDWAR_NKO_world_succession_daily = {
 if = {
  limit = { IMP_is_1970_scenario = yes NOT = { date < 1994.7.8 } NOT = { has_global_flag = COLDWAR_NKO_kim_il_sung_death_news_sent } }
  if = {
   limit = { country_exists = NKO }
   NKO = { COLDWAR_NKO_succession_daily = yes }
  }
  else = {
   set_global_flag = COLDWAR_NKO_kim_il_sung_death_news_sent
   news_event = { id = COLDWAR_NKO_succession.1 }
  }
 }
}
COLDWAR_NKO_install_kim_jong_il = {
 if = {
  limit = {
   tag = NKO
   IMP_is_1970_scenario = yes
   check_variable = { ruling_party = 4 }
   has_country_flag = COLDWAR_NKO_kim_il_sung_death_recorded
   has_country_flag = COLDWAR_NKO_succession_pending
   NOT = { has_country_flag = COLDWAR_NKO_kim_jong_il_unavailable }
   NOT = { has_country_flag = COLDWAR_NKO_kim_jong_il_succeeded }
  }
  create_country_leader = { name = "Kim Jong-il" picture = "gfx/Leaders/NKO/Kim_Jong_il.dds" ideology = communist_state }
  clr_country_flag = COLDWAR_NKO_succession_pending
  set_country_flag = COLDWAR_NKO_kim_jong_il_succeeded
  set_global_flag = COLDWAR_NKO_1994_succession_announced
  COLDWAR_NKO_refresh_programmes = yes
  news_event = { id = COLDWAR_NKO_succession.2 }
 }
}
"""

EVENTS = """# IMPERIA COLD WAR — Cold War: NKO 1994 death and global succession news.
add_namespace = COLDWAR_NKO_succession

# Death news reports a caretaker only when Kim Il Sung died in office.
news_event = {
	id = COLDWAR_NKO_succession.1
	title = COLDWAR_NKO_succession.1.t
	desc = {
		trigger = { has_global_flag = COLDWAR_NKO_1994_kim_il_sung_died_in_office }
		text = COLDWAR_NKO_succession.1.d_incumbent
	}
	desc = {
		trigger = { NOT = { has_global_flag = COLDWAR_NKO_1994_kim_il_sung_died_in_office } }
		text = COLDWAR_NKO_succession.1.d_former
	}
	picture = GFX_COLDWAR_NKO_1994_funeral
	is_triggered_only = yes
	major = yes
	option = { name = COLDWAR_NKO_succession.1.a }
}

news_event = {
	id = COLDWAR_NKO_succession.2
	title = COLDWAR_NKO_succession.2.t
	desc = COLDWAR_NKO_succession.2.d
	picture = GFX_COLDWAR_NKO_1994_funeral
	is_triggered_only = yes
	major = yes
	option = { name = COLDWAR_NKO_succession.2.a }
}
"""

DECISIONS = """# IMPERIA COLD WAR — Cold War: NKO player-controlled 1994 succession.
COLDWAR_NKO_succession_category = {
	COLDWAR_NKO_confirm_kim_jong_il = {
		icon = GFX_decision_generic_political_discourse
		cost = 0
		allowed = { original_tag = NKO }
		visible = { tag = NKO IMP_is_1970_scenario = yes has_country_flag = COLDWAR_NKO_succession_pending }
		available = {
			hidden_trigger = {
			tag = NKO
			IMP_is_1970_scenario = yes
			check_variable = { ruling_party = 4 }
			has_country_flag = COLDWAR_NKO_kim_il_sung_death_recorded
			has_country_flag = COLDWAR_NKO_succession_pending
			NOT = { has_country_flag = COLDWAR_NKO_kim_jong_il_unavailable }
			NOT = { has_country_flag = COLDWAR_NKO_kim_jong_il_succeeded }
			}
			emerging_communist_state_are_in_power = yes
		}
		complete_effect = {
			effect_tooltip = { create_country_leader = { name = "Kim Jong-il" picture = "gfx/Leaders/NKO/Kim_Jong_il.dds" ideology = communist_state } }
			hidden_effect = { COLDWAR_NKO_install_kim_jong_il = yes }
		}
		fire_only_once = yes
		ai_will_do = { base = 1 }
	}
}
"""

CATEGORY = """# IMPERIA COLD WAR — Cold War: NKO succession decision category.
 COLDWAR_NKO_succession_category = {
	icon = GFX_decision_category_generic_political_actions
	allowed = { original_tag = NKO IMP_is_1970_scenario = yes }
	visible = { has_country_flag = COLDWAR_NKO_succession_pending }
}
"""

NEWS_GFX = """# IMPERIA COLD WAR — Cold War: NKO 1994 succession news illustration.
spriteTypes = {
\tspriteType = {
\t\tname = "GFX_COLDWAR_NKO_1994_funeral"
\t\ttexturefile = "gfx/event_pictures/COLDWAR_NKO_1994_funeral.dds"
\t}
}
"""

ENGLISH_LOCALIZATION = """l_english:
# IMPERIA COLD WAR — Cold War: North Korea 1994 succession.
 COLDWAR_NKO_succession.1.t: "Kim Il Sung Has Died"
 COLDWAR_NKO_succession.1.d_incumbent: "Kim Il Sung has died at the age of 82 after leading North Korea for nearly half a century. A Funeral Committee has assumed interim duties as the Workers’ Party considers the succession."
 COLDWAR_NKO_succession.1.d_former: "Kim Il Sung, North Korea’s former leader, has died at the age of 82. His death closes the era of the Republic’s founding generation."
 COLDWAR_NKO_succession.1.a: "The end of an era."
 COLDWAR_NKO_succession.2.t: "Kim Jong Il Assumes Leadership"
 COLDWAR_NKO_succession.2.d: "The Workers’ Party has confirmed Kim Jong Il as North Korea’s leader, ending the Funeral Committee’s interim administration."
 COLDWAR_NKO_succession.2.a: "A new chapter begins."
 COLDWAR_NKO_confirm_kim_jong_il: "Confirm Kim Jong Il as Leader"
 COLDWAR_NKO_confirm_kim_jong_il_desc: "The Workers’ Party may confirm Kim Jong Il as leader and end the Funeral Committee’s interim administration."
 COLDWAR_NKO_succession_category: "The Leadership Succession"
 COLDWAR_NKO_succession_category_desc: "The Funeral Committee administers the state during the mourning period. The Workers’ Party must settle the succession before a new leadership programme can take effect."
"""


def emit_sources() -> None:
    """Deterministically emit the assigned event, effect, gfx and English localization files."""
    for path, text in ((EVENTS_PATH, EVENTS), (EFFECTS_PATH, EFFECTS), (GFX_PATH, NEWS_GFX), (DECISIONS_PATH, DECISIONS), (CATEGORY_PATH, CATEGORY)):
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
        image.save(TARGET, format="DDS", pixel_format="DXT5")
        raw = bytearray(TARGET.read_bytes())
        struct.pack_into('<I', raw, 20, ((TARGET_SIZE[0]+3)//4)*((TARGET_SIZE[1]+3)//4)*16)
        struct.pack_into('<I', raw, 28, 1)
        TARGET.write_bytes(raw)
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
    if not MEMORIAL_PORTRAIT.is_file():
        raise FileNotFoundError(f"Expected Kim Il Sung memorial portrait is absent: {MEMORIAL_PORTRAIT}")


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
