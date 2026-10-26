# IMPERIA CW — Cold War: gulf 1970 — validate.
"""Check Gulf 1970 starter recruitment, exact portraits and wrapper regeneration.

Run with Python and Pillow. This does not claim native game rendering coverage.
"""
from pathlib import Path
import ast
import hashlib
import json
import re
import struct
import sys
from unittest.mock import patch

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "docs/gulf_start_1970_portraits_20261019.json"
sys.path.insert(0, str(ROOT / "tools/historical_politics_1970"))
from dispatch import _restore_setter, _wrap_native_setter

# Reuse the established strict parser without executing unrelated country QA.
module = ast.parse((ROOT / "tools/israel_1970/validate_content.py").read_text(encoding="utf-8"))
functions = [node for node in module.body if isinstance(node, ast.FunctionDef)
             and node.name in {"tokens", "parse", "values", "first", "walk"}]
namespace = {"re": re}
exec(compile(ast.Module(body=functions, type_ignores=[]), "hoi4_parser", "exec"), namespace)
parse, first, values, walk = (namespace[name] for name in ("parse", "first", "values", "walk"))


def main():
    checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        assert condition, message

    def read(relative):
        return parse((ROOT / relative).read_text(encoding="utf-8-sig"))

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    ideology_groups = first(read("common/ideologies/00_ideologies.txt"), "ideologies")
    outlooks = {ideology: group for group, _, definition in ideology_groups
                if isinstance(definition, list) for ideology, _, _ in first(definition, "types", [])}
    revised_roles = {"BHR": "Western_Autocracy", "KUW": "Western_Autocracy", "UAE": "Western_Autocracy"}
    characters = first(read("common/characters/mdcw_gulf_1970.txt"), "characters")
    sprites = values(first(read("interface/mdcw_gulf_1970_portraits.gfx"), "spriteTypes"), "spriteType")
    binder = first(read("common/scripted_effects/mdcw_gulf_1970_portraits.txt"),
                   "MDCW_GULF_1970_bind_active_portrait")
    scenario = first(binder, "if")
    check(first(first(scenario, "limit"), "IMP_is_1970_scenario") == "yes",
          "Portrait repair can affect later bookmarks")
    setup = first(read("common/scripted_effects/00_leader_setup_scripted_effects.txt"), "set_leader")
    check(setup[-1] == ("MDCW_GULF_1970_bind_active_portrait", "=", "yes"),
          "Known portraits are not restored after native leader recreation")
    for row in report["items"]:
        tag, token, sprite = row["tag"], row["token"], row["sprite"]
        expected_ideology = revised_roles.get(tag, row["ideology"])
        history_path = next((ROOT / "history/countries").glob(tag + " - *.txt"))
        raw = history_path.read_bytes()
        history = parse(raw.decode("utf-8-sig"))
        starter = first(history, "1970.1.1")
        character = first(characters, token)
        check(first(character, "name").strip('"') == row["name"], tag + ": wrong historical identity")
        leader = first(starter, "create_country_leader") if tag == "UAE" else first(character, "country_leader")
        check(first(leader, "ideology") == expected_ideology, tag + ": wrong current leader role")
        if tag == "UAE":
            check(first(leader, "name").strip('"') == "Trucial States Council" and first(leader, "expire") is None,
                  "Council must use its direct canonical provider until actual federation, without a1971 expiry")
        else:
            check(first(leader, "expire").strip('"') == row["expires"], tag + ": wrong leader expiry")
        check(first(first(first(character, "portraits"), "civilian"), "large") == sprite,
              tag + ": civilian portrait is not explicitly bound")
        bindings = [node for node in sprites if first(node, "name").strip('"') == sprite]
        check(len(bindings) == 1 and first(bindings[0], "texturefile").strip('"') == row["portrait"],
              tag + ": missing or ambiguous sprite")
        asset = ROOT / row["portrait"]
        data = asset.read_bytes()
        check(hashlib.sha256(data).hexdigest() == row["portrait_sha256"], tag + ": asset changed without review")
        check(data[:4] == b"DDS " and data[84:88] == b"DXT5"
              and struct.unpack_from("<II", data, 12) == (210, 156)
              and struct.unpack_from("<I", data, 28)[0] == 1
              and len(data) == 128 + 39 * 53 * 16, tag + ": invalid or incomplete DDS mip payload")
        with Image.open(asset) as image:
            check(image.convert("RGBA").getextrema()[3] == (255, 255), tag + ": transparent portrait")
            if tag == "UAE":
                pixels = image.convert("RGB")
                for y in (0, image.height - 1):
                    check(len({pixels.getpixel((x, y)) for x in range(image.width)}) > 8,
                          "Council portrait has flat padding instead of a full-bleed photograph")
        promotion = first(starter, "promote_character")
        check(first(first(starter, "set_politics"), "ruling_party") == outlooks[expected_ideology],
              tag + ": actual ruling outlook disagrees with incumbent ideology")
        if tag == "UAE":
            check(promotion is None and not any(key == "recruit_character" and value == token for key, _, value in walk(history)),
                  "Council must not recruit/promote the obsolete expiring1971 character")
            party_name = first(starter, "set_party_name")
            check(first(party_name, "ideology") == "democratic"
                  and first(party_name, "name") == "COLDWAR_UAE_party_0"
                  and any(first(entry, "ruling_party") == "0" for entry in values(starter, "set_variable")),
                  "Council's native preview party name still displays a generic outlook")
        else:
            check(first(starter, "recruit_character") == token,
                  tag + ": defined historical character is not attached to its country")
            check(promotion is not None and first(promotion, "character") == token,
                  tag + ": recruited starter is not explicitly made party leader")
            check(first(promotion, "ideology") == expected_ideology
                  and first(starter, "create_country_leader") is None,
                  tag + ": starter promotion uses a wrong role or duplicate legacy name lookup")
            keys = [key for key, _, _ in starter]
            check(sum(key == "recruit_character" and value == token for key, _, value in walk(history)) == 1
                  and keys.index("recruit_character") < keys.index("set_politics") < keys.index("promote_character"),
                  tag + ": duplicate or incorrectly ordered starter recruitment/promotion")
        check(hashlib.sha256(raw[raw.index(b"2000.1.1"):]).hexdigest() == row["later_history_sha256"],
              tag + ": later bookmark history was changed")
        setter = read(f"common/scripted_effects/{tag}_political_leaders.txt")
        check(len(setter) == 1 and setter[0][0] == "set_leader_" + tag,
              tag + ": setter is unclosed or parsed into another scope")
        repair = next(node for node in values(scenario, "if")
                      if first(first(node, "limit"), "original_tag") == tag)
        check(first(first(first(repair, "limit"), "has_country_leader"), "name").strip('"') == row["name"]
              and first(first(repair, "set_country_leader_portrait"), "portrait") == sprite,
              tag + ": repair could replace another ruler's portrait")
    check(len(characters) == len(sprites) == len(report["items"]) == 6, "Incomplete Gulf roster")

    # Exercise the actual generator without creating game files or needing temp permissions.
    original = "set_leader_UAE = {\n\tset_variable = { Monarchist_leader = 0 }\n}\n"
    with patch.object(Path, "exists", return_value=True), patch.object(Path, "read_text", return_value=original):
        wrapped = _wrap_native_setter(ROOT, "UAE", {23: []})
    check(len(parse(wrapped)) == 1, "Generator comments out the closing brace")
    check(_restore_setter(wrapped, "UAE") == original, "Generator changes preserved native content")
    with patch.object(Path, "exists", return_value=True), patch.object(Path, "read_text", return_value=wrapped):
        check(_wrap_native_setter(ROOT, "UAE", {23: []}) == wrapped, "Regeneration is not idempotent")
    broken = wrapped.replace("# MDCW HISTORICAL NATIVE POOL END UAE\n}",
                             "# MDCW HISTORICAL NATIVE POOL END UAE}")
    try:
        parse(broken)
    except AssertionError:
        check(True, "")
    else:
        check(False, "Regression check accepts the old swallowed-brace bug")
    print(f"PASS: Gulf 1970 characters, historical portraits and native generation ({checks} checks)")
    return {"passed": True, "checks": checks, "engine_rendering_tested": False}


if __name__ == "__main__":
    main()
