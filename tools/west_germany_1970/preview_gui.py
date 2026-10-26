# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Render mock-ups of the generated windows (one PNG per tab) to catch layout errors.

    python3 preview_gui.py <build_root> <mdcw_png_dir> <out_dir> [state.json]

Texts are resolved through the localisation with sample variable values; scripted
localisation shows its first matching entry. Not a perfect renderer - good enough to see
overlaps, cut-off text and empty areas.
"""
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

FONT = {"hoi_16mbs": 12, "hoi_18mbs": 14, "hoi_24header": 20}
COL = {"Y": (240, 210, 90), "G": (110, 210, 120), "R": (230, 90, 80), "g": (150, 150, 150), "W": (240, 240, 240), "!": None}


def font(sz, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, sz)


def load_dds(path):
    try:
        return Image.open(path).convert("RGBA")
    except Exception:
        return None


def parse_gui(text):
    """Return {window_name: [elements]} for containerWindowType blocks (flat)."""
    wins = {}
    for m in re.finditer(r'containerWindowType = \{\s*name = "(\w+)"\s*position = \{ x = (-?\d+) y = (-?\d+) \}', text):
        name = m.group(1)
        start = m.end()
        depth, i = 1, text.index("{", m.start()) + 1
        while depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[start:i]
        els = []
        for em in re.finditer(r'(iconType|instantTextBoxType|buttonType) = \{(.*?)\n\t\t\}', body, re.S):
            kind, b = em.group(1), em.group(2)
            d = dict(kind=kind)
            for k in ("name", "spriteType", "text", "font", "format", "pdx_tooltip"):
                mm = re.search(r"\b" + k + r' = "?([^"\s]*)"?', b)
                if mm:
                    d[k] = mm.group(1)
            mm = re.search(r"position = \{ x = (-?\d+) y = (-?\d+) \}", b)
            d["x"], d["y"] = int(mm.group(1)), int(mm.group(2))
            for k in ("maxWidth", "maxHeight"):
                mm = re.search(k + r" = (\d+)", b)
                if mm:
                    d[k] = int(mm.group(1))
            mm = re.search(r"scale = ([\d.]+)", b)
            d["scale"] = float(mm.group(1)) if mm else 1.0
            els.append(d)
        mb = re.search(r'quadTextureSprite = "(\w+)"', body)
        wins[name] = dict(x=int(m.group(2)), y=int(m.group(3)), els=els, bg=mb.group(1) if mb else "GFX_mdcw_cw_window_bg")
    return wins


class Renderer:
    def __init__(self, build, pngdir, state):
        self.build, self.pngdir, self.state = build, pngdir, state
        loc_t = open(os.path.join(build, "localisation/english/COLDWAR_GER_1970_l_english.yml"), encoding="utf-8-sig").read()
        self.loc = {k: v.replace("\\n", "\n") for k, v in re.findall(r'^ ([^:\s]+):0 "(.*)"$', loc_t, re.M)}
        sl = open(os.path.join(build, "common/scripted_localisation/COLDWAR_GER_1970_windows.txt"), encoding="utf-8").read()
        self.dt = {}
        for m in re.finditer(r"defined_text = \{\s*name = (\w+)(.*?)\n\}", sl, re.S):
            entries = re.findall(r"text = \{\s*(?:trigger = \{ (.*?) \}\s*)?localization_key = (\w+)", m.group(2), re.S)
            self.dt[m.group(1)] = entries
        gfx = open(os.path.join(build, "interface/COLDWAR_GER_1970_windows.gfx"), encoding="utf-8").read()
        self.sprites = {}
        for name, tex, fr in re.findall(r'name = "(GFX_\w+)"\s+(?:size = \{[^}]*\}\s+)?texturefile = "([^"]+)"(?:\s+noOfFrames = (\d+))?', gfx):
            self.sprites[name] = (os.path.join(build, tex), int(fr or 1))

    def var(self, name):
        name = name.replace("DDR.", "")
        return self.state.get(name, 0)

    def cond(self, trig):
        """Evaluate a trigger string against the sample state (check_variable, flags, NOT/OR/AND)."""
        toks = re.findall(r"[{}]|[^\s{}]+", trig)
        pos = [0]

        def block():
            vals = []
            while pos[0] < len(toks) and toks[pos[0]] != "}":
                vals.append(term())
            return vals

        def term():
            t = toks[pos[0]]
            pos[0] += 1
            if pos[0] < len(toks) and toks[pos[0]] == "=":
                pos[0] += 1
                if toks[pos[0]] == "{":
                    pos[0] += 1
                    if t == "check_variable":
                        var, op, val = toks[pos[0]], toks[pos[0] + 1], toks[pos[0] + 2]
                        pos[0] += 4
                        x = self.var(var)
                        try:
                            v = float(val)
                        except ValueError:
                            v = self.var(val)
                        return {"<": x < v, ">": x > v, "=": x == v}[op]
                    vals = block()
                    pos[0] += 1
                    if t == "NOT":
                        return not any(vals)
                    if t == "OR":
                        return any(vals)
                    if t == "AND" or t in ("DDR", "SOV", "GER"):
                        return all(vals)
                    return True
                val = toks[pos[0]]
                pos[0] += 1
                if t == "has_country_flag":
                    return val in self.state.get("_flags", [])
                if t.endswith("_can_" + t.split("_can_")[-1]) and "_can_" in t:
                    return val == "yes"
                return True
            return True
        return all(block())

    def resolve(self, text, depth=0):
        if depth > 6:
            return text
        text = re.sub(r"\$(\w+)\$", lambda m: self.loc.get(m.group(1), m.group(1)), text).replace("%%", "%")

        def sub_dt(m):
            n = m.group(1)
            if n in self.dt:
                for trig, key in self.dt[n]:
                    if not trig or self.cond(trig):
                        return self.resolve(self.loc.get(key, key), depth + 1)
                return ""
            if n.endswith("GetLeader"):
                return "Willy Brandt" if n.startswith("Root") else "Walter Ulbricht"
            return n
        text = re.sub(r"\[([A-Za-z][\w.]*)\]", sub_dt, text)

        def sub_var(m):
            v = self.var(m.group(1))
            return str(int(v)) if float(v).is_integer() else f"{v:.1f}"
        text = re.sub(r"\[\?([\w.]+)\|[^\]]*\]", sub_var, text)
        return text

    def draw_text(self, img, x, y, w, h, txt, fsz, fmt):
        d = ImageDraw.Draw(img)
        f = font(fsz)
        lines = []
        for para in txt.split("\n"):
            words, line = para.split(" "), ""
            for wd in words:
                test = (line + " " + wd).strip()
                if d.textlength(re.sub(r"§.", "", test), font=f) > w and line:
                    lines.append(line)
                    line = wd
                else:
                    line = test
            lines.append(line)
        lh = fsz + 4
        overflow = len(lines) * lh > h + 4
        for li, line in enumerate(lines):
            if (li + 1) * lh > h + 4:
                break
            plain = re.sub(r"§.", "", line)
            tw = d.textlength(plain, font=f)
            cx = x + (w - tw) / 2 if fmt == "center" else (x + w - tw if fmt == "right" else x)
            col = COL["W"]
            for part in re.split(r"(§.)", line):
                if part.startswith("§"):
                    c = COL.get(part[1])
                    col = c if c else COL["W"]
                    continue
                d.text((cx, y + li * lh), part, font=f, fill=col)
                cx += d.textlength(part, font=f)
        return overflow

    def sprite(self, name, frame=1):
        if name in self.sprites:
            path, n = self.sprites[name]
            im = load_dds(path)
            if im and n > 1:
                fw = im.width // n
                f = max(1, min(n, int(frame)))
                im = im.crop(((f - 1) * fw, 0, f * fw, im.height))
            return im
        p = os.path.join(self.pngdir, name.replace("GFX_", "") + ".png")
        if os.path.exists(p):
            return Image.open(p).convert("RGBA")
        return None

    def render(self, wins, main, bars, sg, tab, out):
        W = wins[main]
        img = Image.new("RGBA", (780, 700), (10, 14, 22, 255))
        bg = self.sprite(W.get("bg", "GFX_mdcw_cw_window_bg"))
        if bg:
            img.paste(bg, (0, 0), bg)
        props = dict(re.findall(r"^\t\t\t(\w+) = \{ (.*?) \}$", sg, re.M))
        vis = dict(re.findall(r"^\t\t\t(\w+)_visible = \{ (.*?) \}$", sg, re.M))
        problems = []
        for e in W["els"]:
            name = e.get("name", "")
            if name in vis and not self.cond(vis[name].replace("cwgg_tab", "__tab").replace("cwgg_sec_tab", "__tab").replace("__tab", "cwgg_tab") if False else vis[name]):
                continue
            x, y = e["x"], e["y"]
            p = props.get(name, "")
            mx = re.search(r"\bx = (\w+)", p)
            if mx:
                x = int(self.var(mx.group(1)))
            my = re.search(r"\by = (\w+)", p)
            if my:
                y = int(self.var(my.group(1)))
            frame = 1
            mf = re.search(r"frame = (\w+)", p)
            if mf:
                frame = self.var(mf.group(1))
            spr = e.get("spriteType")
            mi = re.search(r'image = "\[(\w+)\]"', p)
            if mi:
                spr = self.resolve(f"[{mi.group(1)}]")
            if spr:
                im = self.sprite(spr, frame)
                if im is None:
                    ImageDraw.Draw(img).rectangle([x, y, x + 60, y + 30], outline=(255, 0, 255))
                else:
                    if e["scale"] != 1.0:
                        im = im.resize((int(im.width * e["scale"]), int(im.height * e["scale"])))
                    img.paste(im, (x, y), im)
                    if e["kind"] == "buttonType" and e.get("text"):
                        txt = self.resolve(self.loc.get(e["text"], e["text"]))
                        self.draw_text(img, x + 2, y + (im.height - 15) // 2, im.width - 4, 18, txt, FONT.get(e.get("font", "hoi_16mbs"), 13), "center")
            if e["kind"] == "instantTextBoxType":
                txt = self.resolve(self.loc.get(e["text"], e["text"]))
                if self.draw_text(img, x, y, e.get("maxWidth", 200), e.get("maxHeight", 20), txt, FONT.get(e.get("font"), 13), e.get("format", "left")):
                    problems.append(f"text overflow: {name}")
        for b in bars:
            win = wins[b]
            vis_b = re.search(r'\t' + re.escape(b.replace("_window", "_bar")) + r' = \{.*?visible = \{ ([^\n]*) \}\n', sg, re.S)
            if vis_b and not self.cond(vis_b.group(1)):
                continue
            track = self.sprite(win["els"][0]["spriteType"])
            fill = self.sprite(win["els"][1]["spriteType"])
            mfv = re.search(re.escape(win["els"][1]["name"]) + r" = \{ x = (\w+) \}", sg)
            fx = int(self.var(mfv.group(1))) if mfv else -300
            if track:
                img.paste(track, (win["x"], win["y"]), track)
            if fill:
                crop = fill.crop((max(0, -fx), 0, fill.width, fill.height)) if fx < 0 else fill
                sub = Image.new("RGBA", track.size if track else fill.size, (0, 0, 0, 0))
                sub.paste(fill, (fx, 0), fill)
                img.paste(sub, (win["x"], win["y"]), sub)
        img.save(out)
        return problems


def compute_display(state, refresh):
    """Run the refresh effect's arithmetic on the sample state (subset of the script language)."""
    st = dict(state)
    lines = refresh.split("\n")
    stack = []
    for raw in lines:
        line = raw.strip()
        for op, var, val in re.findall(r"(set_variable|add_to_variable|subtract_from_variable|multiply_variable) = \{ (\w+) = ([\w.\-]+) \}", line):
            v = st.get(val.replace("DDR.", ""), None) if re.match(r"[A-Za-z]", val) else float(val)
            if v is None:
                v = 0
            if op == "set_variable":
                st[var] = v
            elif op == "add_to_variable":
                st[var] = st.get(var, 0) + v
            elif op == "subtract_from_variable":
                st[var] = st.get(var, 0) - v
            else:
                st[var] = st.get(var, 0) * v
        m = re.search(r"clamp_variable = \{ var = (\w+) min = (-?[\d.]+) max = (-?[\d.]+) \}", line)
        if m:
            st[m.group(1)] = max(float(m.group(2)), min(float(m.group(3)), st.get(m.group(1), 0)))
    return st


if __name__ == "__main__":
    build, pngdir, outdir = sys.argv[1:4]
    state = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {}
    os.makedirs(outdir, exist_ok=True)
    gui_t = open(os.path.join(build, "interface/COLDWAR_GER_1970_windows.gui"), encoding="utf-8").read()
    sg = open(os.path.join(build, "common/scripted_guis/COLDWAR_GER_1970_windows.txt"), encoding="utf-8").read()
    wins = parse_gui(gui_t)
    r = Renderer(build, pngdir, state)
    for main, tabvar, ntabs in (("cwgg_rv_main_window", "cwgg_tab", 5), ("cwgg_sec_main_window", "cwsec_tab", 4)):
        if main not in wins:
            continue
        prefix = main.replace("_main_window", "")
        bars = [w for w in wins if w.startswith(prefix + "_") and w.endswith("_window") and w != main]
        for t in range(1, ntabs + 1):
            r.state[tabvar] = t
            probs = r.render(wins, main, bars, sg, t, os.path.join(outdir, f"{prefix}_tab{t}.png"))
            for p_ in probs:
                print(prefix, t, p_)
