# IMPERIA CW — Cold War: art — politburo art.
# COLDWAR | Paints the Politburo dossier (decision category GUI) and writes the textures as DDS.
# Dev tool, not part of the build: python3 art/politburo_art.py [--preview]
# Needs Playwright (Chromium) and the fontsource fonts (FONTS dir). The DDS output in art/dds/ is copied by cw_build.py.
# Look (Enes, 19.10.2026): a Soviet file folder - red banner, typed form, pinned photos, rubber stamps.
import os, sys, struct, json, base64, io
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pb_layout as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "dds")
PNGDIR = os.path.join(HERE, "png")
FONTS = os.environ.get("CW_FONTS", "/home/claude/pbgui/node_modules/@fontsource")

INK = "#2a2520"          # typewriter ink
LABEL = "#7a6249"        # printed form labels
RED = "#9e1b1b"
GOLD = "#e3b955"


def ff(family, path):
    return f"@font-face {{ font-family: '{family}'; src: url('file://{FONTS}/{path}'); }}"


FONT_CSS = "\n".join([
    ff("Oswald", "oswald/files/oswald-latin-700-normal.woff2"), ff("Oswald", "oswald/files/oswald-cyrillic-700-normal.woff2"),
    ff("OswaldM", "oswald/files/oswald-latin-500-normal.woff2"),
    ff("Stencil", "stardos-stencil/files/stardos-stencil-latin-700-normal.woff2"),
    ff("Elite", "special-elite/files/special-elite-latin-400-normal.woff2"),
    ff("Russo", "russo-one/files/russo-one-cyrillic-400-normal.woff2"), ff("Russo", "russo-one/files/russo-one-latin-400-normal.woff2"),
    ff("PTSerif", "pt-serif/files/pt-serif-cyrillic-700-normal.woff2"), ff("PTSerif", "pt-serif/files/pt-serif-latin-700-normal.woff2"),
    ff("Courier", "courier-prime/files/courier-prime-latin-700-normal.woff2"),
])

SVG_DEFS = """
<svg width="0" height="0" style="position:absolute">
 <defs>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff0b0"/><stop offset=".45" stop-color="#e0b04a"/><stop offset="1" stop-color="#8f6414"/></linearGradient>
  <filter id="paper" x="0" y="0" width="100%" height="100%">
   <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="7" result="fine"/>
   <feColorMatrix in="fine" type="matrix" values="0 0 0 0 .32  0 0 0 0 .25  0 0 0 0 .16  0 0 0 .55 -.18" result="grain"/>
   <feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="3" seed="11" result="big"/>
   <feColorMatrix in="big" type="matrix" values="0 0 0 0 .45  0 0 0 0 .32  0 0 0 0 .14  0 0 0 .9 -.38" result="blot"/>
   <feMerge><feMergeNode in="blot"/><feMergeNode in="grain"/></feMerge>
  </filter>
  <filter id="cloth" x="0" y="0" width="100%" height="100%">
   <feTurbulence type="fractalNoise" baseFrequency=".9 .05" numOctaves="2" seed="3" result="n"/>
   <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .5 -.2"/>
  </filter>
  <filter id="grunge" x="-5%" y="-5%" width="110%" height="110%">
   <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="5" result="n"/>
   <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 1.75" result="m"/>
   <feComposite in="SourceGraphic" in2="m" operator="in"/>
  </filter>
  <filter id="grunge2" x="-5%" y="-5%" width="110%" height="110%">
   <feTurbulence type="fractalNoise" baseFrequency=".6" numOctaves="3" seed="21" result="n"/>
   <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.0 1.55" result="m"/>
   <feComposite in="SourceGraphic" in2="m" operator="in"/>
  </filter>
  <filter id="grunge3" x="-10%" y="-10%" width="120%" height="120%">
   <feTurbulence type="fractalNoise" baseFrequency="1.3" numOctaves="2" seed="9" result="n"/>
   <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 2.05" result="m"/>
   <feComposite in="SourceGraphic" in2="m" operator="in"/>
  </filter>
  <filter id="soft"><feGaussianBlur stdDeviation=".35"/></filter>
 </defs>
</svg>"""

HAMMER = """<svg width="{s}" height="{s}" viewBox="0 0 100 100"><g fill="{fill}">
 <path d="M 62 14 C 86 22 94 50 80 70 C 68 87 44 90 30 80 L 24 88 L 16 82 L 23 74 C 18 66 18 58 20 52 C 26 66 40 76 56 74 C 74 71 84 52 78 36 C 75 27 69 19 62 14 Z"/>
 <path d="M 22 30 L 28 24 L 82 80 L 76 86 Z"/><path d="M 14 30 L 34 10 L 44 20 L 38 26 L 32 20 L 20 36 Z"/></g></svg>"""
STAR = """<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path fill="{fill}" stroke="{stroke}" stroke-width="{sw}"
 d="M50 4 L61 38 L97 38 L68 59 L79 94 L50 72 L21 94 L32 59 L3 38 L39 38 Z"/></svg>"""


def hammer(s, fill="url(#gold)"):
    return HAMMER.format(s=s, fill=fill)


def star(s, fill="url(#gold)", stroke="none", sw=0):
    return STAR.format(s=s, fill=fill, stroke=stroke, sw=sw)


# ------------------------------------------------------------------ icons of the emulation table (simple pictograms)
ICONS = {
    "growth": """<svg width="18" height="16" viewBox="0 0 18 16"><path d="M1 15 H17" stroke="#5b4630" stroke-width="1.4"/>
      <rect x="2" y="10" width="3" height="5" fill="#5b4630"/><rect x="7" y="7" width="3" height="8" fill="#5b4630"/><rect x="12" y="3" width="3" height="12" fill="#5b4630"/>
      <path d="M2 8 L8 4 L11 6 L16 1" stroke="#9e1b1b" stroke-width="1.6" fill="none"/><path d="M13 1 H16.5 V4.5" stroke="#9e1b1b" stroke-width="1.6" fill="none"/></svg>""",
    "industry": """<svg width="18" height="16" viewBox="0 0 18 16"><path fill="#5b4630" d="M1 15 V7 L5 9 V7 L9 9 V7 L13 9 V1 H16 V15 Z"/>
      <rect x="3" y="11" width="2" height="2" fill="#e6d6b4"/><rect x="7" y="11" width="2" height="2" fill="#e6d6b4"/><rect x="11" y="11" width="2" height="2" fill="#e6d6b4"/></svg>""",
    "output": """<svg width="18" height="16" viewBox="0 0 18 16"><circle cx="9" cy="8" r="5" fill="none" stroke="#5b4630" stroke-width="2.6" stroke-dasharray="2.2 1.7"/>
      <circle cx="9" cy="8" r="2.6" fill="#5b4630"/><circle cx="9" cy="8" r="1.1" fill="#e6d6b4"/></svg>""",
    "plan": """<svg width="18" height="16" viewBox="0 0 18 16"><path d="M3 1 V15" stroke="#5b4630" stroke-width="1.6"/>
      <path fill="#9e1b1b" d="M3.8 1.5 H16 L13.5 4.5 L16 7.5 H3.8 Z"/></svg>""",
}
# icons of the honour roll (Enes, 19.10.2026): last place, Moscow's favourite, the Spartakiad
HONOUR_ICONS = {
    "lag": """<svg width="18" height="16" viewBox="0 0 18 16"><path d="M1 15 H17" stroke="#5b4630" stroke-width="1.4"/>
      <path d="M2 3 L7 8 L10 6 L15 11" stroke="#9e1b1b" stroke-width="1.8" fill="none"/><path d="M11 11.6 H15.4 V7.2" stroke="#9e1b1b" stroke-width="1.8" fill="none"/></svg>""",
    "fav": """<svg width="16" height="18" viewBox="0 0 16 18"><path fill="#7a1a14" d="M4 17 V8 L8 3.6 L12 8 V17 Z"/>
      <rect x="3" y="12" width="10" height="5" fill="#9b2a20"/><rect x="7" y="13.4" width="2" height="3.6" fill="#e6d6b4"/>
      <path fill="#d43a2a" stroke="#8f6414" stroke-width=".5" d="M8 0.2 L8.8 2.3 L11 2.3 L9.2 3.6 L9.9 5.7 L8 4.4 L6.1 5.7 L6.8 3.6 L5 2.3 L7.2 2.3 Z"/></svg>""",
    "medal": """<svg width="16" height="18" viewBox="0 0 16 18"><path fill="#9e1b1b" d="M3 0 H7 L9 6 H5 Z"/><path fill="#3a5c8c" d="M13 0 H9 L7 6 H11 Z"/>
      <circle cx="8" cy="11.5" r="5.6" fill="#d9a838" stroke="#8f6414" stroke-width="1"/><circle cx="8" cy="11.5" r="3.6" fill="none" stroke="#fff0b0" stroke-width=".7"/>
      <path fill="#8f6414" d="M8 8.6 L8.8 10.8 L11 10.8 L9.2 12.1 L9.9 14.2 L8 12.9 L6.1 14.2 L6.8 12.1 L5 10.8 L7.2 10.8 Z"/></svg>""",
}


def red_banner(held=True):
    """The Transferable Red Banner of a column: bright when the leader holds it, faded when it still hangs elsewhere."""
    style = "" if held else "filter:grayscale(.8);opacity:.5"
    return (f'<div id="banner_{"held" if held else "away"}" style="position:relative;width:{L.BANNER_W}px;height:{L.BANNER_H_}px;{style}">'
            f'<svg width="{L.BANNER_W}" height="{L.BANNER_H_}" viewBox="0 0 15 18">'
            '<rect x="1" y="1.2" width="1.4" height="16.8" fill="#5b4630"/><circle cx="1.7" cy="1.3" r="1.25" fill="#e0b04a"/>'
            '<path d="M2.4 2.2 H14.4 V11.4 L11.4 9.8 L8.4 11.4 L5.4 9.8 L2.4 11.4 Z" fill="#c4231c" stroke="#7a1410" stroke-width=".6"/>'
            '<path d="M2.6 11.6 L5.4 10.1 L8.4 11.7 L11.4 10.1 L14.2 11.6" fill="none" stroke="#e0b04a" stroke-width="1.1"/>'
            '<path fill="#f0c95a" d="M6.2 3.6 L6.8 5.2 L8.5 5.2 L7.1 6.2 L7.7 7.8 L6.2 6.8 L4.7 7.8 L5.3 6.2 L3.9 5.2 L5.6 5.2 Z"/>'
            '<path d="M9.6 4.4 H12.8 M9.6 6.2 H12.8 M9.6 8 H12" stroke="#f0c95a" stroke-width=".7"/></svg></div>')


def paper_bg():
    """The whole dossier page (static parts)."""
    rows = []
    labels = {"office": "OFFICE", "name": "NAME", "heir": "DESIGNATED HEIR", "balance": "POLITBURO BALANCE",
              "cohesion": "UNION COHESION", "session": "NEXT SESSION", "congress": "PARTY CONGRESS"}
    for k, y in L.ROWS.items():
        h = 26 if k == "name" else L.ROW_H
        rows.append(f'<div class="lbl" style="left:{L.LABEL_X}px;top:{y + 5}px">{labels[k]}</div>')
        if k != "balance":
            rows.append(f'<div class="line" style="left:{L.VALUE_X - 2}px;top:{y + h - 3}px;width:{L.VALUE_W}px"></div>')
    bx, by, bw, bh = L.BAR
    ticks = "".join(f'<div style="position:absolute;left:{bx + round(i * bw / 10)}px;top:{by + bh}px;width:1px;height:{4 if i % 5 else 6}px;background:#6b5a45"></div>'
                    for i in range(11))
    bar = (f'<div style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px;border:1px solid #4b3b2b;'
           f'background:linear-gradient(90deg,#3c5f86 0%,#9aa3a8 50%,#a3261e 100%);box-shadow:inset 0 1px 2px rgba(0,0,0,.35)"></div>'
           f'{ticks}<div class="tiny" style="left:{bx}px;top:{by - 9}px">REFORMERS</div>'
           f'<div class="tiny" style="left:{bx + bw - 44}px;top:{by - 9}px">ORTHODOX</div>')
    gx, gy = L.GS_PHOTO
    gs_paper = (f'<div class="photo" style="left:{gx - 6}px;top:{gy - 6}px;width:{L.GS_PW + 12}px;height:{L.GS_PH + 22}px"></div>'
                f'<div class="cap" style="left:{gx - 6}px;top:{gy + L.GS_PH + 2}px;width:{L.GS_PW + 12}px">ARCHIVE PHOTOGRAPH</div>')
    seats = []
    for i, x in enumerate(L.SEAT_X):
        seats.append(f'<div class="photo" style="left:{x}px;top:{L.SEAT_Y}px;width:{L.SEAT_PW + 12}px;height:{L.SEAT_PH + 12}px"></div>')
        seats.append(f'<div class="seatno" style="left:{x + L.SEAT_FLAG_DX}px;top:{L.SEAT_Y + 46}px">SEAT</div>'
                     f'<div class="seatnum" style="left:{x + L.SEAT_FLAG_DX}px;top:{L.SEAT_Y + 56}px">{"I" * (i + 1) if i < 3 else ""}</div>')
        seats.append(f'<div class="line" style="left:{x}px;top:{L.SEAT_NAME_Y + 16}px;width:{L.SEAT_W}px"></div>')
    emu = []
    names = {"growth": "Economic growth", "industry": "Industry", "output": "Output per head", "plan": "Plan targets"}
    for i, k in enumerate(L.EMU_ROWS):
        y = L.EMU_ROW_Y + i * L.EMU_ROW_H
        shade = "rgba(120,90,50,.07)" if i % 2 == 0 else "transparent"
        emu.append(f'<div style="position:absolute;left:10px;top:{y}px;width:490px;height:{L.EMU_ROW_H}px;background:{shade}"></div>')
        emu.append(f'<div style="position:absolute;left:{L.EMU_COLS["icon"]}px;top:{y + 2}px">{ICONS[k]}</div>')
        emu.append(f'<div class="typed" style="left:{L.EMU_COLS["label"]}px;top:{y + 2}px">{names[k]}</div>')
    c = L.EMU_COLS
    hon = []   # the honour roll: one dotted line per row, the icons left (and the favourite's in the middle)
    for y in (L.PRIDE_Y, L.LAG_Y, L.SPART_Y):
        hon.append(f'<div class="line" style="left:{L.HONOUR_TEXT_X - 2}px;top:{y + 18}px;width:{L.W - L.HONOUR_TEXT_X - 10}px"></div>')
    hon.append(f'<div style="position:absolute;left:{L.HONOUR_ICON_X}px;top:{L.PRIDE_Y + 1}px">{star(14, '#c9302a', '#7a1410', 4)}</div>')
    hon.append(f'<div style="position:absolute;left:{L.HONOUR_ICON_X - 1}px;top:{L.LAG_Y + 1}px">{HONOUR_ICONS["lag"]}</div>')
    hon.append(f'<div style="position:absolute;left:{L.FAV_X + 2}px;top:{L.LAG_Y}px">{HONOUR_ICONS["fav"]}</div>')
    hon.append(f'<div style="position:absolute;left:{L.HONOUR_ICON_X}px;top:{L.SPART_Y}px">{HONOUR_ICONS["medal"]}</div>')
    emu.append(f'<div class="tiny" style="left:{c["flag"]}px;top:{L.EMU_ROW_Y - 10}px">LEADING REPUBLIC</div>'
               f'<div class="tiny" style="left:{c["value"]}px;top:{L.EMU_ROW_Y - 11}px">RESULT</div>'
               f'<div class="tiny" style="left:{c["rank"]}px;top:{L.EMU_ROW_Y - 11}px">OUR PLACE</div>')
    emu += hon
    return f"""
<div id="bg" class="sheet" style="width:{L.W}px;height:{L.H}px">
 <div class="paper"></div>
 <svg class="fill" width="{L.W}" height="{L.H}"><rect width="100%" height="100%" filter="url(#paper)"/></svg>
 <div class="vignette"></div>
 <div class="fold" style="top:{L.SEATS_HEAD_Y - 6}px"></div>
 <!-- banner -->
 <div class="banner" style="height:{L.BANNER_H}px">
   <svg class="fill" width="{L.W}" height="{L.BANNER_H}"><rect width="100%" height="100%" filter="url(#cloth)"/></svg>
   <div style="position:absolute;left:12px;top:5px">{hammer(52)}</div>
   <div style="position:absolute;left:52px;top:3px">{star(16)}</div>
   <div class="btitle">POLITBURO</div>
   <div class="bsub">OF THE CENTRAL COMMITTEE OF THE COMMUNIST PARTY OF THE SOVIET UNION</div>
   <div class="bcyr">ЦК КПСС</div>
   <div class="trim" style="top:{L.BANNER_H - 6}px"></div><div class="trim2" style="top:{L.BANNER_H - 2}px"></div>
 </div>
 <div class="typed small" style="left:14px;top:{L.STRIP_Y}px">Fond 3 &middot; Opis 72 &middot; File No. 1970/ПБ &middot; members of the Politburo only</div>
 <!-- top secret stamp -->
 <div class="stampbox" style="left:384px;top:{L.STRIP_Y - 5}px;transform:rotate(-5deg);color:#b0221c;border-color:#b0221c;padding:1px 6px 1px">
   <div style="font:700 12px/12px Stencil;letter-spacing:2px">TOP SECRET</div><div style="font:700 7.5px/8px Oswald;letter-spacing:1px">СОВЕРШЕННО СЕКРЕТНО</div></div>
 {gs_paper}
 {''.join(rows)}
 {bar}
 <!-- seats -->
 <div class="head" style="top:{L.SEATS_HEAD_Y}px">{star(11, '#9e1b1b')}<span>REPUBLICAN MEMBERS OF THE POLITBURO</span>{star(11, '#9e1b1b')}</div>
 {''.join(seats)}
 <!-- ballot -->
 <div class="ballot" style="top:{L.BALLOT_Y}px;height:{L.BALLOT_H}px"><div class="ballotlbl">BALLOT</div></div>
 <!-- emulation -->
 <div class="head" style="top:{L.EMU_HEAD_Y}px">{star(11, '#9e1b1b')}<span>SOCIALIST EMULATION OF THE REPUBLICS</span>{star(11, '#9e1b1b')}</div>
 {''.join(emu)}
 <div class="line" style="left:10px;top:{L.EMU_ROW_Y + 4 * L.EMU_ROW_H + 1}px;width:490px;border-top:1px solid #7a6249"></div>
 <!-- footer: certified by the General Department of the Central Committee -->
 <div class="line" style="left:10px;top:{L.FOOT_Y - 2}px;width:490px;border-top:1px solid #7a6249"></div>
 <div class="lbl" style="left:14px;top:{L.FOOT_Y + 6}px">CERTIFIED: GENERAL DEPARTMENT OF THE CC CPSU</div>
 <svg style="position:absolute;left:250px;top:{L.FOOT_Y - 2}px" width="120" height="34" viewBox="0 0 120 34">
  <path d="M4 24 C 10 6, 18 4, 16 18 C 15 26, 24 26, 30 14 C 34 6, 38 8, 36 18 C 35 24, 42 24, 48 16 C 52 10, 58 10, 56 18
           C 55 24, 64 22, 70 14 C 74 9, 80 9, 79 17 C 78 23, 90 22, 104 12 M 20 28 C 40 30, 70 29, 112 22"
        fill="none" stroke="#2c3e78" stroke-width="1.4" stroke-linecap="round" opacity=".85"/></svg>
 <div class="typed" style="left:360px;top:{L.FOOT_Y + 4}px">K. Chernenko</div>
 <!-- archive stamp -->
 <div class="round" style="left:420px;top:{L.FOOT_Y - 26}px;transform:rotate(-14deg)">
   <svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="29" fill="none" stroke="#4d3f8a" stroke-width="2.2"/>
   <circle cx="32" cy="32" r="22" fill="none" stroke="#4d3f8a" stroke-width="1"/>
   <path id="arc" d="M 32 32 m -25.5 0 a 25.5 25.5 0 1 1 51 0 a 25.5 25.5 0 1 1 -51 0" fill="none"/>
   <text font-family="Oswald" font-size="7" fill="#4d3f8a" letter-spacing="1.4"><textPath href="#arc">ЦК КПСС &#183; ОБЩИЙ ОТДЕЛ &#183; АРХИВ &#183;</textPath></text>
   <g transform="translate(19,18) scale(.26)">{hammer(100, '#4d3f8a')}</g></svg></div>
</div>"""


CSS = f"""
{FONT_CSS}
body {{ margin:0; background:transparent; }}
.sheet {{ position:relative; overflow:hidden; }}
.paper {{ position:absolute; inset:0; background:#e8d9b8; }}
.fill {{ position:absolute; left:0; top:0; }}
.vignette {{ position:absolute; inset:0; box-shadow: inset 0 0 38px rgba(90,60,20,.45), inset 0 0 6px rgba(60,40,10,.6); }}
.fold {{ position:absolute; left:0; width:100%; height:2px; background:linear-gradient(90deg,transparent,rgba(110,80,40,.18),transparent); }}
.banner {{ position:absolute; left:0; top:0; width:100%; background:linear-gradient(180deg,#a51e1e 0%,#861414 55%,#6a0d0d 100%); overflow:hidden; }}
.btitle {{ position:absolute; left:80px; top:2px; font:700 30px/34px Oswald; letter-spacing:7px; color:{GOLD};
          text-shadow:0 1px 0 #5a0a0a, 0 0 6px rgba(0,0,0,.35); }}
.bsub {{ position:absolute; left:81px; top:37px; font:500 9.5px/12px OswaldM; letter-spacing:1.2px; color:#f1d48a; }}
.bcyr {{ position:absolute; right:14px; top:8px; font:400 21px/24px Russo; color:{GOLD}; letter-spacing:2px; opacity:.95; text-shadow:0 1px 0 #5a0a0a; }}
.trim {{ position:absolute; left:0; width:100%; height:2px; background:#d8ab48; }}
.trim2 {{ position:absolute; left:0; width:100%; height:1px; background:#d8ab48; }}
.typed {{ position:absolute; font:400 12px/14px Elite; color:{INK}; white-space:nowrap; }}
.small {{ font-size:10px; opacity:.85; }}
.lbl {{ position:absolute; font:500 8.5px/10px OswaldM; letter-spacing:1.3px; color:{LABEL}; white-space:nowrap; }}
.tiny {{ position:absolute; font:500 7.5px/8px OswaldM; letter-spacing:1.2px; color:{LABEL}; white-space:nowrap; }}
.line {{ position:absolute; height:0; border-top:1px dotted #8a7254; }}
.photo {{ position:absolute; background:#f6f1e4; box-shadow:1px 2px 4px rgba(40,25,5,.45), 0 0 0 1px rgba(80,60,30,.25); }}
.cap {{ position:absolute; font:500 8px/12px OswaldM; letter-spacing:1.4px; color:#5c4a36; text-align:center; }}
.head {{ position:absolute; left:10px; width:490px; height:18px; display:flex; align-items:center; justify-content:center; gap:8px;
         border-top:1px solid #9e1b1b; border-bottom:1px solid #9e1b1b; font:700 13px/18px Stencil; letter-spacing:2.5px; color:#9e1b1b; }}
.seatno {{ position:absolute; font:500 7.5px/8px OswaldM; letter-spacing:1.5px; color:{LABEL}; }}
.seatnum {{ position:absolute; font:700 18px/20px Stencil; color:#9e1b1b; letter-spacing:1px; }}
.ballot {{ position:absolute; left:10px; width:488px; border:1px solid #7a6249; background:rgba(255,250,235,.35); }}
.ballotlbl {{ position:absolute; left:6px; top:9px; font:700 12px/14px Stencil; letter-spacing:2px; color:#9e1b1b; }}
.stampbox {{ position:absolute; padding:3px 7px 2px; border:2px solid; border-radius:2px; text-align:center; filter:url(#grunge); opacity:.82; }}
.round {{ position:absolute; filter:url(#grunge2); opacity:.55; }}
"""


# ------------------------------------------------------------------ separate sprites
def photo_corners(w, h, cid):
    """Black album photo corners and a paper clip, drawn over the portrait (transparent elsewhere)."""
    c = 13 if w > 90 else 9
    clip = (f'<svg style="position:absolute;left:{w // 2 + 14}px;top:0px" width="22" height="46" viewBox="0 0 22 46">'
            '<path d="M7 40 V8 a4 4 0 0 1 8 0 V36 a6.5 6.5 0 0 1 -13 0 V12" fill="none" stroke="#5f6870" stroke-width="2.6" stroke-linecap="round"/>'
            '<path d="M7 40 V8 a4 4 0 0 1 8 0 V36 a6.5 6.5 0 0 1 -13 0 V12" fill="none" stroke="#e3e8ec" stroke-width="1" stroke-linecap="round" transform="translate(-.6,-.6)"/></svg>') if w > 90 else ""
    tri = lambda style: f'<div style="position:absolute;width:0;height:0;{style}"></div>'
    return (f'<div id="{cid}" style="position:relative;width:{w + 8}px;height:{h + 8}px">'
            + tri(f"left:0;top:0;border-top:{c}px solid #2b2621;border-right:{c}px solid transparent")
            + tri(f"right:0;top:0;border-top:{c}px solid #2b2621;border-left:{c}px solid transparent")
            + tri(f"left:0;bottom:0;border-bottom:{c}px solid #2b2621;border-right:{c}px solid transparent")
            + tri(f"right:0;bottom:0;border-bottom:{c}px solid #2b2621;border-left:{c}px solid transparent")
            + clip + "</div>")


STAMPS = {   # id -> (English, Russian, colour, rotation)
    "for": ("FOR", "ЗА", "#1d8a3a", -9),
    "against": ("AGAINST", "ПРОТИВ", "#b0221c", 7),
    "abstain": ("ABSTAINED", "ВОЗДЕРЖАЛСЯ", "#55606e", -6),
    "pending": ("AWAITING", "ГОЛОСОВАНИЕ", "#3d3a8f", 5),
    "vacant": ("VACANT", "ВАКАНСИЯ", "#8a4a1c", -8),
    "adopted": ("ADOPTED", "ПРИНЯТО", "#24733a", -4),
    "rejected": ("REJECTED", "ОТКЛОНЕНО", "#b0221c", 4),
}


def stamp(k):
    en, ru, col, rot = STAMPS[k]
    size = 15 if len(en) <= 8 else 12
    return (f'<div id="stamp_{k}" style="display:inline-block;padding:14px 14px">'
            f'<div class="stampbox" style="position:relative;color:{col};border:3px solid {col};transform:rotate({rot}deg);opacity:1;'
            f'filter:url(#grunge3);outline:1.5px solid {col};outline-offset:2px;padding:3px 8px 2px;background:rgba(255,255,255,.0)">'
            f'<div style="font:700 {size + 3}px/{size + 4}px Stencil;letter-spacing:2px">{en}</div>'
            f'<div style="font:700 8.5px/10px Oswald;letter-spacing:1.4px">{ru}</div></div></div>')


def marker_frames():
    bx, by, bw, bh = L.BAR
    fw = bw + 2 * L.BAR_PAD
    out = []
    for i in range(L.BAR_FRAMES):
        x = L.BAR_PAD + round(i * bw / (L.BAR_FRAMES - 1))
        out.append(f'<div style="position:relative;width:{fw}px;height:24px;float:left">'
                   f'<div style="position:absolute;left:{x - 1}px;top:5px;width:2px;height:14px;background:#1d1a17"></div>'
                   f'<div style="position:absolute;left:{x - 5}px;top:0px;width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-top:6px solid #1d1a17"></div>'
                   f'<div style="position:absolute;left:{x - 5}px;top:18px;width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:6px solid #1d1a17"></div>'
                   "</div>")
    return f'<div id="marker" style="width:{fw * L.BAR_FRAMES}px;height:24px">{"".join(out)}</div>'


def unknown_portrait():
    """Fallback portrait for a leader without a picture: a grey silhouette on photo paper."""
    return ('<div id="unknown" style="position:relative;width:156px;height:210px;background:linear-gradient(180deg,#b9b2a4,#8f887b);overflow:hidden">'
            '<svg width="156" height="210" viewBox="0 0 156 210"><circle cx="78" cy="78" r="34" fill="#5d574d"/>'
            '<path d="M14 210 C18 150 46 128 78 128 C110 128 138 150 142 210 Z" fill="#5d574d"/>'
            '<path d="M66 128 L78 150 L90 128 Z" fill="#8f887b"/></svg>'
            '<div style="position:absolute;left:0;bottom:8px;width:100%;text-align:center;font:700 11px Stencil;letter-spacing:2px;color:#e8e1d2">NO PHOTOGRAPH</div></div>')


def page(body):
    return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{SVG_DEFS}{body}</body></html>"


def write_dds(png_path, dds_path):
    """Uncompressed 32-bit BGRA DDS (HOI4 reads it as A8R8G8B8)."""
    im = Image.open(png_path).convert("RGBA")
    w, h = im.size
    r, g, b, a = im.split()
    data = Image.merge("RGBA", (b, g, r, a)).tobytes()
    hdr = struct.pack("<4sIIIIIII44sIIIIIIIIIIIII", b"DDS ", 124, 0x1 | 0x2 | 0x4 | 0x1000 | 0x8, h, w, w * 4, 0, 1, b"\0" * 44,
                      32, 0x41, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000, 0x1000, 0, 0, 0, 0)
    with open(dds_path, "wb") as f:
        f.write(hdr + data)


ASSETS = {   # file stem -> (element id, html)
    "politburo_dossier": ("bg", lambda: paper_bg()),
    "photo_corners_large": ("pc_l", lambda: photo_corners(L.GS_PW, L.GS_PH, "pc_l")),
    "photo_corners_small": ("pc_s", lambda: photo_corners(L.SEAT_PW, L.SEAT_PH, "pc_s")),
    "balance_marker": ("marker", lambda: marker_frames()),
    "portrait_unknown": ("unknown", lambda: unknown_portrait()),
}
for _k in STAMPS:
    ASSETS[f"stamp_{_k}"] = (f"stamp_{_k}", (lambda k=_k: stamp(k)))
ASSETS["banner_held"] = ("banner_held", lambda: red_banner(True))
ASSETS["banner_away"] = ("banner_away", lambda: red_banner(False))


def render(preview=False):
    from playwright.sync_api import sync_playwright
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(PNGDIR, exist_ok=True)
    sizes = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(device_scale_factor=1)
        for stem, (eid, fn) in ASSETS.items():
            path = os.path.join(PNGDIR, stem + ".html")
            open(path, "w").write(page(fn()))
            pg.goto("file://" + path)
            pg.wait_for_timeout(250)
            png = os.path.join(PNGDIR, stem + ".png")
            pg.locator("#" + eid).screenshot(path=png, omit_background=True)
            if stem == "balance_marker":
                # one texture per marker position (the GUI picks the sprite live from the balance)
                strip = Image.open(png).convert("RGBA")
                fw = L.BAR[2] + 2 * L.BAR_PAD
                for i in range(L.BAR_FRAMES):
                    fp = os.path.join(PNGDIR, f"marker_{i:02d}.png")
                    strip.crop((fw * i, 0, fw * (i + 1), strip.size[1])).save(fp)
                    write_dds(fp, os.path.join(OUTDIR, f"marker_{i:02d}.dds"))
                    sizes[f"marker_{i:02d}"] = (fw, strip.size[1])
                continue
            write_dds(png, os.path.join(OUTDIR, stem + ".dds"))
            sizes[stem] = Image.open(png).size
        b.close()
    json.dump(sizes, open(os.path.join(OUTDIR, "sizes.json"), "w"), indent=1)
    return sizes


if __name__ == "__main__":
    print(render())
