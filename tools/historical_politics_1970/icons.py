#!/usr/bin/env python3
# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Stage historically bounded party marks from Wikimedia Commons for review.

This tool writes only to the artifact directory passed with --out. It does not
modify the mod's live sprite registry or party localisation. Commons API access
uses a descriptive User-Agent and is capped at three concurrent thumbnails.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

UA = "MDCW-Historical-Party-Icon-Audit/1.0 (historical game-mod icon research; Commons thumbnails only; contact via Wikimedia Commons user page)"
API = "https://commons.wikimedia.org/w/api.php"

# Start/end are periods for which the mark is evidenced for the named party.
# Indices remain null unless the current scenario registry has been checked.
ITEMS = [
    dict(tag="USA", index=None, from_="1970.1.1", until=None, name="Democratic Party", title="Democratic Disc.svg", match="Democratic donkey mascot (historic symbol); modern disc styling is not claimed as a period logo", evidence="https://www.loc.gov/lcm/pdf/LCM_2017_0102.pdf", page="https://commons.wikimedia.org/wiki/File:Democratic_Disc.svg", license="Public domain in the United States; Commons says published 1931–1977 without copyright notice"),
    dict(tag="USA", index=None, from_="1970.1.1", until=None, name="Republican Party", title="Republican Disc.svg", match="Republican elephant mascot (historic symbol); modern disc styling is not claimed as a period logo", evidence="https://www.loc.gov/lcm/pdf/LCM_2017_0102.pdf", page="https://commons.wikimedia.org/wiki/File:Republican_Disc.svg", license="Public domain in the United States; Commons says published 1931–1977 without copyright notice"),
    dict(tag="DDR", index=None, from_="1946.4.21", until="1989.12.16", name="Socialist Unity Party of Germany (SED)", title="Sozialistische Einheitspartei Deutschlands Logo.svg", match="Official SED clasped-hands emblem; party name changed to SED-PDS at the 16 December 1989 special congress", evidence="https://www.bpb.de/themen/zeit-kulturgeschichte/deutschland-chronik/132304/16-17-dez-1989/", page="https://commons.wikimedia.org/wiki/File:Sozialistische_Einheitspartei_Deutschlands_Logo.svg", license="Public domain: Commons states emblem ineligible for copyright"),
    dict(tag="CHI", index=4, from_="1921.7.1", until="1996.9.28", name="Chinese Communist Party (CCP/CPC)", title="Danghui (pre-1996).svg", match="Pre-1996 CPC hammer-and-sickle emblem (use only this historical variant)", evidence="https://www.gov.cn/test/2008-06/17/content_1012269.htm", page="https://commons.wikimedia.org/wiki/File:Danghui_(pre-1996).svg", license="Commons file page; emblem status and use restrictions are jurisdiction-specific"),
    dict(tag="SOV", index=4, from_="1970.1.1", until="1991.12.26", name="Communist Party of the Soviet Union (CPSU)", title="КПСС.svg", match="CPSU-specific Cyrillic logotype, not a generic state mark", evidence="https://www.prlib.ru/node/619693", page="https://commons.wikimedia.org/wiki/File:%D0%9A%D0%9F%D0%A1%D0%A1.svg", license="Commons file page; license to be reviewed before integration"),
    dict(tag="JAP", index=1, from_="1955.11.15", until=None, name="Liberal Democratic Party (LDP)", title="Liberal Democratic Party (Japan) Emblem.svg", match="LDP emblem (chrysanthemum seal with 自民 characters)", evidence="https://www.jimin.jp/english/about-ldp/history/", page="https://commons.wikimedia.org/wiki/File:Liberal_Democratic_Party_(Japan)_Emblem.svg", license="Public domain: simple geometric shapes/text per Commons"),
    dict(tag="PAK", index=3, from_="1967.11.30", until=None, name="Pakistan People's Party", title="Flag of Pakistan People's Party.svg", match="PPP tricolor party flag, reduced to icon size", evidence="https://www.ppp.org.pk/history/", page="https://commons.wikimedia.org/wiki/File:Flag_of_Pakistan_People%27s_Party.svg", license="Public domain: simple geometry per Commons; insignia restrictions may apply"),
    dict(tag="RAJ", index=3, from_="1971.1.25", until="1978.2.2", name="Indian National Congress (INC)", title="Cow and Calf INC.svg", match="Cow-and-calf symbol allotted to Congress (R) following ECI recognition in January 1971; not valid for the full INC period", evidence="https://indiankanoon.org/doc/821162/", page="https://commons.wikimedia.org/wiki/File:Cow_and_Calf_INC.svg", license="Commons file page; election symbol is official insignia"),
    dict(tag="RAJ", index=None, from_="1952.1.1", until=None, name="Communist Party of India", title="CPI Election Symbol.png", match="CPI hammer-and-sickle election emblem; not interchangeable with CPI(M)", evidence="https://eci.gov.in/files/category/97-statistical-reports/", page="https://commons.wikimedia.org/wiki/File:CPI_Election_Symbol.png", license="Commons file page; election symbol is official insignia"),
    dict(tag="RAJ", index=None, from_="1964.11.7", until=None, name="Communist Party of India (Marxist)", title="CPI(M) election symbol - Hammer Sickle and Star.svg", match="CPI(M) hammer-sickle-star election symbol", evidence="https://eci.gov.in/files/category/97-statistical-reports/", page="https://commons.wikimedia.org/wiki/File:CPI(M)_election_symbol_-_Hammer_Sickle_and_Star.svg", license="Commons file page; election symbol is official insignia"),
    dict(tag="BUL", index=4, from_="1948.12.18", until="1990.4.3", name="Bulgarian Communist Party (BCP)", title="LogoBKP.svg", match="BKP hammer-and-sickle logo; includes a source-based redraw", evidence="https://www.refworld.org/reference/countryrep/irbc/1990/92630", page="https://commons.wikimedia.org/wiki/File:LogoBKP.svg", license="CC BY-SA 4.0; preserve attribution and share-alike terms"),
    dict(tag="ROM", index=4, from_="1965.7.24", until="1989.12.22", name="Romanian Communist Party (PCR)", title="Coat of arms of PCR.svg", match="Official PCR emblem; traced from a contemporary 1974 congress directive image", evidence="https://www.cnsas.ro/imagini/istoria_comunism/congrese/1974%20Directivele%20Congresului%20al%20XI-lea.jpg", page="https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_PCR.svg", license="Commons file page; check local government-emblem restrictions"),
    dict(tag="BAN", index=None, from_="1954.3.8", until=None, name="Bangladesh Awami League", title="বাংলাদেশ আওয়ামী লীগের প্রতীক.svg", match="Boat election symbol; Commons page says first used in 1954 East Bengal election", evidence="https://www.albd.org/", page="https://commons.wikimedia.org/wiki/File:%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6_%E0%A6%86%E0%Aও%E0%A6%AF%E0%A6%BC%E0%A6%BE%E0%A6%AE%E0%A7%80_%E0%A6%B2%E0%A7%80%E0%A6%97%E0%A7%87%E0%Aর_%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%A4%E0%A7%80%E0%A6%95.svg", license="Public domain per Commons simple-logo and Bangladesh government-work tags; insignia restrictions apply"),
    dict(tag="TAI", index=22, from_="1970.1.1", until=None, name="Kuomintang", title="Kuomintang Emblem.svg", match="Blue Sky with a White Sun party emblem", evidence="https://www.kmt.org.tw/", page="https://commons.wikimedia.org/wiki/File:Kuomintang_Emblem.svg", license="Public domain: simple geometric shapes per Commons"),
    dict(tag="TUR", index=3, from_="1935.5.9", until=None, name="Republican People’s Party (CHP)", title="CHP six arrows.svg", match="Six Arrows, official CHP/Kemalist symbol; existing 1970 party label confirms slot 3", evidence="https://www.chp.org.tr/chp-tarihi", page="https://commons.wikimedia.org/wiki/File:CHP_six_arrows.svg", license="Commons file page; check trademark/official-insignia restrictions"),
    dict(tag="FRA", index=4, from_="1978.1.1", until=None, name="French Communist Party (PCF)", title="Logo du Parti communiste français.png", match="PCF emblem explicitly dated 1978; not valid at 1970 start", evidence="https://www.pcf.fr/", page="https://commons.wikimedia.org/wiki/File:Logo_du_Parti_communiste_fran%C3%A7ais.png", license="Public domain claim on Commons file page; verify before redistribution"),
    dict(tag="SPR", index=4, from_="1977.1.1", until="2001.1.1", name="Spanish Communist Party (PCE)", title="Logo PCE, 1977-2018.svg", match="PCE logo explicitly used 1977–2018; available only 1977–2000 within scenario", evidence="https://www.pce.es/", page="https://commons.wikimedia.org/wiki/File:Logo_PCE,_1977-2018.svg", license="Commons file page; verify license and adaptation terms before redistribution"),
    dict(tag="ITA", index=4, from_="1970.1.1", until="1991.2.3", name="Italian Communist Party (PCI)", title="PCI flag.png", match="PCI red party flag with hammer-and-sickle and initials; flag is used as mark", evidence="https://www.treccani.it/enciclopedia/partito-comunista-italiano/", page="https://commons.wikimedia.org/wiki/File:PCI_flag.png", license="Commons file page; verify license and symbol rights before redistribution"),
    dict(tag="ENG", index=3, from_="1970.1.1", until="1987.6.11", name="Labour Party", title="Labour Party logo, 1966.svg", match="Documented Labour campaign logo used in 1966 and reused under Foot and Kinnock until the 1987 general election", evidence="https://commons.wikimedia.org/wiki/File:Labour_Party_logo,_1966.svg", page="https://commons.wikimedia.org/wiki/File:Labour_Party_logo,_1966.svg", license="Public domain text/geometric logo per Commons; verify any jurisdiction-specific marks"),
    dict(tag="FRA", index=3, from_="1971.9.1", until=None, name="Socialist Party (PS)", title="Fist and Rose.svg", match="Fist-and-rose emblem became the French PS national emblem in September 1971; Paris federation use in 1970 is not treated as national-party use", evidence="https://www.ps70.fr/le-ps/", page="https://commons.wikimedia.org/wiki/File:Fist_and_Rose.svg", license="CC0 per Commons; generic redraw of historical emblem, not claimed as the exact signed 1970 original"),
    dict(tag="GER", index=3, from_="1970.1.1", until=None, name="Social Democratic Party of Germany (SPD)", title="Generated neutral marker: SPD", generated_text="SPD", match="Neutral monochrome acronym marker generated for UI recognition; not a historical or official party logo", evidence="https://www.spd.de/160-jahre/1969-mehr-demokratie-wagen", page="https://www.spd.de/160-jahre/1969-mehr-demokratie-wagen", license="Original neutral text marker generated for this review; no third-party logo artwork"),
    dict(tag="GER", index=1, from_="1970.1.1", until=None, name="Christian Democratic Union (CDU)", title="Generated neutral marker: CDU", generated_text="CDU", match="Neutral monochrome acronym marker generated for UI recognition; not a historical or official party logo", evidence="https://www.kas.de/en/web/geschichte-der-cdu", page="https://www.kas.de/en/web/geschichte-der-cdu", license="Original neutral text marker generated for this review; no third-party logo artwork"),
    dict(tag="GER", index=2, from_="1970.1.1", until=None, name="Free Democratic Party (FDP)", title="Generated neutral marker: FDP", generated_text="FDP", match="Neutral monochrome acronym marker generated for UI recognition; not a historical or official party logo", evidence="https://www.fdp.de/geschichte", page="https://www.fdp.de/geschichte", license="Original neutral text marker generated for this review; no third-party logo artwork"),
]

# Exact, keyed targets in normalized_world.json or the existing regional party
# source. Rows omitted here have no matching native party row and remain
# deliberately unbound (notably CPI/CPI(M) and Awami League in this catalog).
BINDINGS = {
    ("USA", "Democratic Party"): dict(index=2, normalized_name="Democratic Party", name_regex="^Democratic Party$", valid_from="1970.1.1", valid_until=None, reuse_sprite="GFX_USA_liberalism_small", reuse_texture="gfx/texticons/parties_icons/usa/USA_liberalism_small.dds", reason="existing local donkey icon is a historically attested party mascot; staged disc treatment is modern"),
    ("USA", "Republican Party"): dict(index=1, normalized_name="Republican Party", name_regex="^Republican Party$", valid_from="1970.1.1", valid_until=None, reuse_sprite="GFX_USA_conservatism_small", reuse_texture="gfx/texticons/parties_icons/usa/USA_conservatism_small.dds", reason="existing local elephant icon is a historically attested party mascot; staged disc treatment is modern"),
    ("DDR", "Socialist Unity Party of Germany (SED)"): dict(index=4, normalized_name="Socialist Unity Party of Germany (SED)", name_regex="^Socialist Unity Party of Germany \\(SED\\)$", valid_from="1970.1.1", valid_until="1989.12.16"),
    ("CHI", "Chinese Communist Party (CCP/CPC)"): dict(index=4, normalized_name="Chinese Communist Party (CCP/CPC)", name_regex="^Chinese Communist Party \\(CCP/CPC\\)$", valid_from="1970.1.1", valid_until="1996.9.28", reuse_sprite="GFX_CHI_communism", reuse_texture="gfx/texticons/parties_icons/china/CHI_communism.dds", reason="staged pre-1996 emblem duplicates the already-registered CPC hammer-and-sickle symbol"),
    ("SOV", "Communist Party of the Soviet Union (CPSU)"): dict(index=4, normalized_name="Communist Party of the Soviet Union (CPSU)", name_regex="^Communist Party of the Soviet Union \\(CPSU\\)$", valid_from="1970.1.1", valid_until="1991.12.26"),
    ("JAP", "Liberal Democratic Party (LDP)"): dict(index=1, normalized_name="Liberal Democratic Party (LDP)", name_regex="^Liberal Democratic Party \\(LDP\\)$", valid_from="1970.1.1", valid_until=None),
    ("PAK", "Pakistan People's Party"): dict(index=3, normalized_name="Pakistan People's Party", name_regex="^Pakistan People's Party(?: \\(PPP\\))?$", valid_from="1970.1.1", valid_until=None),
    ("RAJ", "Indian National Congress (INC)"): dict(index=3, normalized_name="Indian National Congress (INC)", name_regex="^Indian National Congress \\(INC\\)$", valid_from="1971.1.25", valid_until="1978.2.2"),
    ("BUL", "Bulgarian Communist Party (BCP)"): dict(index=4, normalized_name="Bulgarian Communist Party (BCP)", name_regex="^Bulgarian Communist Party \\(BCP\\)$", valid_from="1970.1.1", valid_until="1990.4.3"),
    ("ROM", "Romanian Communist Party (PCR)"): dict(index=4, normalized_name="Romanian Communist Party (PCR)", name_regex="^Romanian Communist Party \\(PCR\\)$", valid_from="1970.1.1", valid_until="1989.12.22"),
    ("TAI", "Kuomintang"): dict(index=22, normalized_name="Kuomintang", name_regex="^Kuomintang$", valid_from="1970.1.1", valid_until=None),
    ("TUR", "Republican People’s Party (CHP)"): dict(index=3, normalized_name="CHP — Republican People’s Party", name_regex="^CHP.*Republican People.s Party$", valid_from="1970.1.1", valid_until=None),
    ("FRA", "French Communist Party (PCF)"): dict(index=4, normalized_name="French Communist Party (PCF)", name_regex="^French Communist Party \\(PCF\\)$", valid_from="1978.1.1", valid_until=None),
    ("SPR", "Spanish Communist Party (PCE)"): dict(index=4, normalized_name="Spanish Communist Party (PCE)", name_regex="^Spanish Communist Party \\(PCE\\)$", valid_from="1977.1.1", valid_until="2001.1.1"),
    ("ITA", "Italian Communist Party (PCI)"): dict(index=4, normalized_name="Italian Communist Party (PCI)", name_regex="^Italian Communist Party \\(PCI\\)$", valid_from="1970.1.1", valid_until="1991.2.3"),
    ("ENG", "Labour Party"): dict(index=3, normalized_name="Labour Party", name_regex="^Labour Party$", valid_from="1970.1.1", valid_until="1987.6.11"),
    ("FRA", "Socialist Party (PS)"): dict(index=3, normalized_name="Socialist Party (PS)", name_regex="^Socialist Party \\(PS\\)$", valid_from="1971.9.1", valid_until=None),
    ("GER", "Social Democratic Party of Germany (SPD)"): dict(index=3, normalized_name="Social Democratic Party of Germany (SPD)", name_regex="^Social Democratic Party of Germany \\(SPD\\)$", valid_from="1970.1.1", valid_until=None),
    ("GER", "Christian Democratic Union (CDU)"): dict(index=1, normalized_name="Christian Democratic Union (CDU)", name_regex="^Christian Democratic Union \\(CDU\\)$", valid_from="1970.1.1", valid_until=None),
    ("GER", "Free Democratic Party (FDP)"): dict(index=2, normalized_name="Free Democratic Party (FDP)", name_regex="^Free Democratic Party \\(FDP\\)$", valid_from="1970.1.1", valid_until=None),
}


def api_metadata(title: str) -> dict:
    params = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + title,
                                    "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 256})
    req = urllib.request.Request(API + "?" + params, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as response:
        page = next(iter(json.load(response)["query"]["pages"].values()))
    info = page["imageinfo"][0]
    return {"download_url": info.get("thumburl") or info["url"], "description_url": info["descriptionurl"],
            "metadata": info.get("extmetadata", {})}


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as response:
        return response.read()


def fallback_thumbnail(item: dict) -> tuple[bytes, dict]:
    """Fetch Wikimedia's standard bounded thumbnail redirect after API 429."""
    quoted = urllib.parse.quote(item["title"], safe="")
    url = f"https://commons.wikimedia.org/wiki/Special:Redirect/file/{quoted}?width=256"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as response:
        return response.read(), {"download_url": response.geturl(),
                                 "description_url": item["page"], "metadata": {}}


def normalized_mark(raw: bytes) -> Image.Image:
    import io
    im = Image.open(io.BytesIO(raw)).convert("RGBA")
    # Preserve shape and transparent margins. The checker background is only
    # for the review sheet; generated 22x22 DDS files remain alpha transparent.
    im.thumbnail((20, 20), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (22, 22), (0, 0, 0, 0))
    canvas.alpha_composite(im, ((22 - im.width) // 2, (22 - im.height) // 2))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.out.resolve()
    (root / "dds").mkdir(parents=True, exist_ok=True)
    manifests = [dict(x, from_=x.pop("from_")) for x in ITEMS]
    failures = []

    # Resolve metadata and acquire thumbnail with no more than 3 active fetches.
    def fetch(item: dict) -> tuple[dict, bytes | None, dict | None, str | None]:
        try:
            if item.get("generated_text"):
                from io import BytesIO
                marker = Image.new("RGBA", (22, 22), (0, 0, 0, 0))
                marker_draw = ImageDraw.Draw(marker)
                try:
                    marker_font = ImageFont.truetype("arialbd.ttf", 8)
                except OSError:
                    marker_font = ImageFont.load_default()
                text = item["generated_text"]
                bounds = marker_draw.textbbox((0, 0), text, font=marker_font)
                width, height = bounds[2] - bounds[0], bounds[3] - bounds[1]
                marker_draw.rounded_rectangle((0, 3, 21, 18), radius=2, outline=(48, 58, 70, 255), width=1)
                marker_draw.text(((22 - width) // 2 - bounds[0], (22 - height) // 2 - bounds[1]), text,
                                 fill=(35, 45, 55, 255), font=marker_font)
                buf = BytesIO()
                marker.save(buf, format="PNG")
                md = {"download_url": "generated://neutral-acronym-marker", "description_url": item["page"],
                      "metadata": {"LicenseShortName": {"value": "Original neutral text marker"}}}
                return item, buf.getvalue(), md, None
            # Commons applies shared-IP throttles; pace API requests while
            # keeping total request concurrency at the required maximum of 3.
            time.sleep(1.5)
            try:
                md = api_metadata(item["title"])
                time.sleep(0.75)
                raw = get_bytes(md["download_url"])
            except Exception as api_exc:
                # When the API responds 429, use Commons' width-limited file
                # redirect. It resolves to a normal thumbnail rather than the
                # full original and retains the same source attribution.
                if "429" not in str(api_exc):
                    raise
                raw, md = fallback_thumbnail(item)
            return item, raw, md, None
        except Exception as exc:  # record missing/unavailable items, do not fake.
            return item, None, None, f"{type(exc).__name__}: {exc}"

    acquired = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for row in pool.map(fetch, manifests):
            acquired.append(row)

    final_rows = []
    cols, cell_w, cell_h = 4, 260, 124
    sheet = Image.new("RGB", (cols * cell_w, ((len(manifests) + cols - 1) // cols) * cell_h), (35, 35, 40))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except OSError:
        font = ImageFont.load_default()
    for n, (item, raw, md, error) in enumerate(acquired):
        key = re.sub(r"[^A-Z0-9]+", "_", item["tag"] + "_" + item["name"].upper()).strip("_")
        iconid = "MDCW_HP_" + key
        texture = f"dds/{iconid}.dds"
        from_precision = "year" if item["from_"].endswith(".1.1") else "day"
        until_precision = "year" if item["until"] and item["until"].endswith(".1.1") else ("day" if item["until"] else None)
        binding = BINDINGS.get((item["tag"], item["name"]))
        if binding:
            item["index"] = binding["index"]
            install_action = "reuse_existing" if binding.get("reuse_sprite") else "add_staged"
            binding_row = {"status": "confirmed", "tag": item["tag"], "index": binding["index"],
                           "match_normalized_name": binding["normalized_name"], "party_name_regex": binding["name_regex"],
                           "iconid": iconid, "valid_from": binding["valid_from"], "valid_until": binding["valid_until"],
                           "install_action": install_action}
            if binding.get("reuse_sprite"):
                binding_row.update(existing_sprite=binding["reuse_sprite"], existing_texture=binding["reuse_texture"], reason=binding["reason"])
        else:
            install_action = "unbound_no_native_party_row"
            if item["tag"] == "BAN":
                unbound_reason = "Bangladesh was not a separate active country in the 1970 start dataset; no native BAN row exists. Do not bind the boat symbol to Pakistan."
            elif item["tag"] == "RAJ":
                unbound_reason = "No native named CPI/CPI(M) row was present in the reviewed India catalogue; do not infer a new party from communist ideology index 4."
            else:
                unbound_reason = "No exact matching native party row in the reviewed catalogue; do not add a row or map by ideology alone."
            binding_row = {"status": "unbound", "tag": item["tag"], "index": None, "iconid": iconid,
                           "valid_from": None, "valid_until": None,
                           "party_name_regex": None, "reason": unbound_reason}
        if binding:
            binding_row["text_icon"] = "£" + binding.get("reuse_sprite", "GFX_" + iconid)
            binding_row["valid_from_precision"] = "scenario_start" if binding["valid_from"] == "1970.1.1" else ("year" if binding["valid_from"].endswith(".1.1") else "day")
            binding_row["valid_until_precision"] = "year" if binding["valid_until"] and binding["valid_until"].endswith(".1.1") else ("day" if binding["valid_until"] else None)
        generated_marker = bool(item.get("generated_text"))
        row = {"tag": item["tag"], "index": item["index"], "from": item["from_"], "from_precision": from_precision,
               "until": item["until"], "until_precision": until_precision,
               "party_name_match": item["name"], "iconid": iconid, "text_icon": "£" + iconid, "sprite": "GFX_" + iconid,
               "path": texture, "texture_path": texture, "commons_file": None if generated_marker else item["title"],
               "asset_origin": "generated_neutral_acronym_marker" if generated_marker else "Wikimedia_Commons_source",
               "symbol_kind": "neutral_acronym_marker_not_historical_logo" if generated_marker else "historical_party_mark",
               "source": None if generated_marker else item["page"], "source_url": None if generated_marker else item["page"],
               "period_evidence_url": item["evidence"], "license_note": item["license"],
               "match_note": item["match"], "status": "staged_candidate", "install_action": install_action, "binding": binding_row}
        if raw is None:
            row.update(status="unavailable", fetch_error=error)
            failures.append({"title": item["title"], "error": error})
        else:
            try:
                icon = normalized_mark(raw)
                icon.save(root / texture, format="DDS")
                cell_x, cell_y = (n % cols) * cell_w, (n // cols) * cell_h
                tile = Image.new("RGBA", (88, 88), (220, 220, 220, 255))
                tile.alpha_composite(icon.resize((88, 88), Image.Resampling.NEAREST), (0, 0))
                sheet.paste(tile.convert("RGB"), (cell_x + 8, cell_y + 14))
                draw.text((cell_x + 108, cell_y + 9), item["tag"], fill="white", font=font)
                draw.text((cell_x + 108, cell_y + 29), item["name"][:34], fill="white", font=font)
                draw.text((cell_x + 108, cell_y + 49), item["from_"] + ("–" + item["until"] if item["until"] else "–"), fill="#cccccc", font=font)
                draw.text((cell_x + 108, cell_y + 70), item["title"][:35], fill="#aaaaaa", font=font)
                lic = md.get("metadata", {}).get("LicenseShortName", {}).get("value", "Commons license metadata unavailable")
                if generated_marker:
                    row["asset_license_metadata"] = lic
                    row["asset_description"] = "Generated monospace acronym UI marker. It is a neutral user-interface shorthand, not a historical or official party logo."
                else:
                    row["commons_license_metadata"] = re.sub(r"<[^>]+>", "", lic)
                    row["commons_description_url"] = md["description_url"]
                row["dds_dimensions"] = "22x22 RGBA"
            except Exception as exc:
                row.update(status="conversion_failed", fetch_error=f"{type(exc).__name__}: {exc}")
                failures.append({"title": item["title"], "error": row["fetch_error"]})
        final_rows.append(row)

    sprites = "\n".join(f'spriteType = {{ name = "{r["sprite"]}" texturefile = "gfx/texticons/parties_icons/1970_historical/{r["texture_path"].split("/")[-1]}" legacy_lazy_load = no }}'
                        for r in final_rows if r["status"] == "staged_candidate" and r["install_action"] == "add_staged")
    (root / "party_icon_manifest.json").write_text(json.dumps({"schema": "mdcw.party-icon-candidates.v1", "generated_by": "tools/historical_politics_1970/icons.py", "notes": ["Staged artifacts only; no live mod asset or sprite registry changed.", "A null index means the exact native 1970 registry slot still needs party-name binding.", "Commons-sourced files were fetched as bounded thumbnails using a descriptive User-Agent; maximum concurrency 3. Generated German acronym markers are original neutral UI shorthand, not party logos.", "Historical-period evidence is separate from icon copyright/licensing. Review jurisdiction-specific insignia restrictions before integration."], "icons": final_rows, "fetch_or_conversion_failures": failures}, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "sprite_types.gfx.txt").write_text("# Staged proposals only; do not install until party index binding and license review.\n" + sprites + "\n", encoding="utf-8")
    sheet.save(root / "party_icon_contact_sheet.png")
    print(json.dumps({"out": str(root), "candidates": sum(r["status"] == "staged_candidate" for r in final_rows), "failures": failures}, ensure_ascii=True))


if __name__ == "__main__":
    main()
