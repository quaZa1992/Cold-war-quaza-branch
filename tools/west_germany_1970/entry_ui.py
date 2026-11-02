# IMPERIA COLD WAR — German politics minigame launcher icon assets
"""Generate two compact politics-panel launchers and a placement audit preview.

The artwork is original Pillow vector drawing authored for this mod. The preview is a
coordinate audit of the native politics panel's 520 px layout, not a game screenshot.
"""
from pathlib import Path
import argparse

from PIL import Image, ImageDraw, ImageFont

SIZE = 32
BUTTON_SIZE = 20
RELATIONS_X, SECURITY_X, BUTTON_Y = 424, 446, 248
OUT = Path(__file__).resolve().parent / "entry_ui_preview"
PROVENANCE = """IMPERIA COLD WAR — German politics minigame launcher icons

Assets: GFX_cwgg_launcher_relations and GFX_cwgg_launcher_security, each 20x20 RGBA.
Source: Original procedural artwork created in tools/west_germany_1970/entry_ui.py.
Original author/credit: Unknown; procedural artwork was created for this project with Codex.
Licence/permission: No third-party assets used. The project notice does not establish
a separate licence for this project or any other mod material.
Modifications: Drawn at 32 px in Pillow and resampled to 20 px to clear native faction controls.
Outputs: gfx/interface/cwger_1970/cwgg_launcher_relations.dds and
gfx/interface/cwger_1970/cwgg_launcher_security.dds.
"""


def icon_base():
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 31, 31), 5, fill=(41, 36, 25, 248), outline=(202, 178, 116, 255), width=1)
    d.rounded_rectangle((2, 2, 29, 29), 3, outline=(109, 94, 61, 255), width=1)
    return im, d


def relations_icon():
    im, d = icon_base()
    # Two compact flags make the subject legible without relying on a numerical badge.
    for x in (6, 19):
        for i, col in enumerate(((25, 25, 25, 255), (194, 39, 37, 255), (226, 190, 86, 255))):
            d.rectangle((x, 6 + i * 4, x + 7, 9 + i * 4), fill=col)
        d.line((x + 8, 6, x + 8, 18), fill=(226, 210, 166, 255), width=1)
    d.ellipse((20, 9, 24, 13), fill=(52, 123, 77, 255), outline=(231, 211, 148, 255), width=1)
    d.rectangle((22, 10, 23, 12), fill=(238, 221, 172, 255))
    # A divided line and a bridge indicate the political channel between the two states.
    d.line((16, 5, 16, 20), fill=(231, 199, 119, 255), width=1)
    d.line((7, 22, 25, 22), fill=(222, 204, 159, 255), width=2)
    d.arc((8, 18, 24, 28), 180, 360, fill=(222, 204, 159, 255), width=2)
    d.line((10, 22, 10, 25), fill=(222, 204, 159, 255), width=1)
    d.line((22, 22, 22, 25), fill=(222, 204, 159, 255), width=1)
    return im


def security_icon():
    im, d = icon_base()
    # File sheet behind a shield; the shield remains the strongest shape at 32 px.
    d.rounded_rectangle((17, 5, 26, 18), 1, fill=(210, 198, 164, 255), outline=(245, 229, 189, 255), width=1)
    for y in (8, 11, 14):
        d.line((19, y, 24, y), fill=(80, 73, 57, 255), width=1)
    shield = [(6, 7), (17, 7), (17, 16), (15, 22), (11, 26), (7, 22), (5, 16)]
    d.polygon(shield, fill=(51, 102, 75, 255), outline=(227, 209, 157, 255))
    d.line((8, 13, 10, 16, 14, 11), fill=(239, 225, 186, 255), width=2)
    d.line((10, 21, 10, 24), fill=(222, 204, 159, 255), width=1)
    d.line((14, 21, 14, 24), fill=(222, 204, 159, 255), width=1)
    return im


def build(reg):
    """Register the generated icons with the existing interface sprite exporter."""
    reg("cwgg_launcher_relations", launcher(relations_icon()))
    reg("cwgg_launcher_security", launcher(security_icon()))


def launcher(im):
    return im.resize((BUTTON_SIZE,BUTTON_SIZE),Image.Resampling.LANCZOS)


def files():
    """Return output-relative DDS paths and source images for bounded compilers."""
    return {
        "gfx/interface/cwger_1970/cwgg_launcher_relations.dds": launcher(relations_icon()),
        "gfx/interface/cwger_1970/cwgg_launcher_security.dds": launcher(security_icon()),
    }


def write_assets(root):
    """Write only these launcher assets below a bounded compiler output root."""
    from gui_sprites import write_dds
    root = Path(root)
    outputs = []
    for relative, image in files().items():
        write_dds(str(root / relative), image)
        outputs.append(relative)
    return outputs


def _font(size, bold=False):
    candidates = (["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeui.ttf"] if bold else
                  ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"])
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def ddr_gui():
    """Return the two DDR-only launcher containers, sharing the native-sized icons."""
    rows = (("relations", RELATIONS_X, "GFX_cwgg_launcher_relations", "cwgg_east_relations_tt"),
            ("security", SECURITY_X, "GFX_cwgg_launcher_security", "cwgg_east_security_tt"))
    return [f'''\tcontainerWindowType = {{
\t\tname = "cwgg_east_{kind}_launcher_container"
\t\tposition = {{ x = {x} y = {BUTTON_Y} }}
\t\tsize = {{ width = {BUTTON_SIZE} height = {BUTTON_SIZE} }}
\t\tbuttonType = {{
\t\t\tname = "cwgg_east_{kind}_launcher_button"
\t\t\tposition = {{ x = 0 y = 0 }}
\t\t\tspriteType = "{sprite}"
\t\t\tpdx_tooltip = "{tip}"
\t\t\tclicksound = click_close
\t\t}}
\t}}''' for kind, x, sprite, tip in rows]


def ddr_scripted_gui():
    """Return DDR-only launcher handlers; destination views are opened by shared providers."""
    rows = (("relations", "COLDWAR_GER_1970_east_open_relations"),
            ("security", "COLDWAR_GER_1970_east_open_domestic"))
    return [f'''\tcwgg_east_{kind}_launcher = {{
\t\tcontext_type = player_context
\t\twindow_name = "cwgg_east_{kind}_launcher_container"
\t\tparent_window_token = politics_tab
\t\tdirty = ROOT.cwgg_east_gui_dirty
\t\tai_enabled = {{ always = no }}
\t\tvisible = {{ is_ai = no original_tag = DDR IMP_is_1970_scenario = yes }}
\t\teffects = {{
\t\t\tcwgg_east_{kind}_launcher_button_click = {{ {provider} = yes }}
\t\t}}
\t}}''' for kind, provider in rows]


def render_preview(path=None):
    """Render a reproducible diagram showing button bounds against native panel bounds."""
    w, h, scale = 920, 700, 1.4
    im = Image.new("RGBA", (w, h), (24, 27, 30, 255))
    d = ImageDraw.Draw(im)
    panel = (90, 70, 870, 670)
    d.rounded_rectangle(panel, radius=12, fill=(62, 58, 48), outline=(184, 166, 119), width=2)
    d.rectangle((91, 71, 869, 122), fill=(43, 42, 38))
    d.text((112, 84), "POLITICS PANEL · native 550 px wide", font=_font(21, True), fill=(238, 226, 198))
    # Scaled native coordinates: origin at panel's upper-left; launcher placement x350/y250.
    ox, oy = panel[0], panel[1]
    x1, y1 = ox + round(RELATIONS_X * scale), oy + round(BUTTON_Y * scale)
    x2 = ox + round(SECURITY_X * scale)
    sz = round(BUTTON_SIZE * scale)
    # Audited native faction row: membership name ends at local x≈371; native action begins at x=468.
    row_y = oy + round(BUTTON_Y * scale)
    d.line((ox + round(195 * scale), row_y + 24, ox + round(390 * scale), row_y + 24), fill=(203, 197, 181), width=2)
    d.text((ox + round(228 * scale), row_y - 4), "faction membership", font=_font(15), fill=(218, 212, 194))
    d.rounded_rectangle((ox + round(468 * scale), row_y - 5, ox + round(500 * scale), row_y + 27), 4,
                        fill=(82, 78, 65), outline=(191, 181, 153), width=2)
    d.text((ox + round(458 * scale), row_y + 33), "native", font=_font(12), fill=(191, 181, 153))
    dx,dy=ox+round(392*scale),oy+round(254*scale)
    d.rectangle((dx,dy,dx+round(31*scale),dy+round(31*scale)),outline=(190,137,120),width=2)
    d.text((dx-15,dy+47),"dismantle",font=_font(11),fill=(190,137,120))
    im.alpha_composite(launcher(relations_icon()).resize((sz, sz), Image.Resampling.LANCZOS), (x1, y1))
    im.alpha_composite(launcher(security_icon()).resize((sz, sz), Image.Resampling.LANCZOS), (x2, y1))
    # Explain exact panel-relative coordinates in a clear review label.
    d.text((112, 625), "Launcher bounds: relations (424, 248)–(444, 268) · security (446, 248)–(466, 268)",
           font=_font(16), fill=(228, 220, 199))
    out = Path(path) if path else OUT / "launcher_placement.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    (OUT / "PROVENANCE.md").write_text(PROVENANCE, encoding="utf-8")
    (OUT / "PLACEMENT_AUDIT.md").write_text('''IMPERIA COLD WAR — German politics launcher placement audit

The launcher anchors to the native `politics_tab` token. Coordinates below are local to that token.

In `interface/countrypoliticsview.gui`, the faction row begins inside `ruling_party_info` at
(88, 300), then `faction` is offset by (95, -46), giving row origin (183, 254). The faction
member label begins at x=45 and has maxWidth=143 (outer x=228..371); the no-faction label
is x=236..379. The original_in_faction label occupies x=195..390. Its dismantle_faction
control starts at (392,254); the installed base-game GFX_dismantle_faction_button texture
is 31x31 (interface/countrypoliticsview.gfx -> gfx/interface/dismantle_faction_button.dds),
so that full native hitbox ends at (423,285). The faction open/create button uses
gfx/interface/factions/ui/factions_button.dds, 573x57 in 3 frames: 191x57 per frame,
occupying x=183..374. These controls are checked even for the engine-selected branches.
The native `view_factions_button` starts at faction-local x=285, giving x=468. Its 32 px hitbox
spans x=468..500; its y offset is -8 from the row, giving y=246..278. The native membership
controls leave a 45 px gap between x=423 and x=468 when dismantle is present.

Relations launcher bounds: (424,248)..(444,268). Security launcher bounds: (446,248)..(466,268).
Both 20x20 hitboxes clear the native dismantle button by 1 px, each other by 2 px,
and the native faction-view button by 2 px. They clear all faction-label boxes and the
national-spirit scroll area ending at y=242. The same placement is used for the DDR-only pair.

The placement preview is a coordinate diagram, not a screenshot of Hearts of Iron IV. It is rendered
by `tools/west_germany_1970/entry_ui.py --preview`.
''', encoding="utf-8")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="write the placement preview and provenance record")
    parser.add_argument("--output", help="optional preview output path")
    args = parser.parse_args()
    if args.preview:
        print(render_preview(args.output))
