# IMPERIA COLD WAR — Exact native MD country-picture frame and news viewport.
from pathlib import Path
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[2]
FRAME=ROOT/'tools/event_art/source/MD_country_event_frame_reference.png'
REPORT_SIZE=(217,163)
INSET=(19,6,180,150)
NEWS_SIZE=(397,153)
SOURCES={'mission-control':'apollo13-mission-control-colourised-v1.png','station':'skylab-original.jpg','mars':'viking-first-surface-colourised-v1.png','soviet-lunar':'soviet-lunar-landing-user-v1.png','french-lunar':'french-lunar-landing-user-v1.png','saudi-lunar':'saudi-lunar-landing-user-v1.png','us-mars':'us-mars-landing-user-v1.png','soviet-mars':'soviet-mars-landing-user-v1.png'}


def build_image(kind,key):
    source=Image.open(ROOT/'docs/design/space_race_1970/assets'/SOURCES[key]).convert('RGB')
    centering=(.5,.12) if key in ['soviet-lunar','french-lunar','saudi-lunar','us-mars','soviet-mars'] else (.5,.5)
    if kind=='news':return ImageOps.fit(source,NEWS_SIZE,method=Image.Resampling.LANCZOS,centering=centering).convert('RGBA')
    assert kind=='report'
    native=Image.open(FRAME).convert('RGBA');assert native.size==REPORT_SIZE
    image=native.copy()
    image.paste(ImageOps.fit(source,INSET[2:],method=Image.Resampling.LANCZOS,centering=centering),(INSET[0],INSET[1]))
    return image
