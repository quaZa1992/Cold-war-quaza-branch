# IMPERIA COLD WAR — France 1970 dated party identities.
"""Build a narrow dated party-name overlay for France's native MD slots."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import date, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "tools/party_registry_1970/data/FRA.json"
GETTERS = ROOT / "common/scripted_localisation/mdcw_historical_parties.txt"
PARTY_LOC = ROOT / "localisation/english/mdcw_1970_party_registry_l_english.yml"
PREFIX = "COLDWAR FRA2 PARTY IDENTITY"
PROJECT = "# IMPERIA COLD WAR — France 1970 dated party identity integration.\n"

IDENTITIES: tuple[dict[str, Any], ...] = (
    {
        "slot": 1,
        "from": "1976.12.5",
        "entry": {
            "name": "Rassemblement pour la République",
            "english": "Rally for the Republic",
            "native_full": "Rassemblement pour la République",
            "language": "French",
            "abbr": "RPR",
            "catchy": False,
            "ideology": "Gaullism",
            "text": (
                "The Rally for the Republic emerged from the transformation of the UDR at "
                "the Porte de Versailles meeting on 5 December 1976, with Jacques Chirac "
                "elected its president. It reorganised the Gaullist movement around a more "
                "disciplined national party.\n\n"
                "The RPR defended a strong presidency, national independence and a distinct "
                "French voice in Europe. Its relationship with President Valéry Giscard "
                "d'Estaing's government remained a central question for the Gaullist right."
            ),
            "icon": None,
            "wiki": "Rally for the Republic",
        },
    },
    {
        "slot": 2,
        "from": "1977.5.19",
        "entry": {
            "name": "Parti républicain",
            "english": "Republican Party",
            "native_full": "Parti républicain",
            "language": "French",
            "abbr": "PR",
            "catchy": False,
            "ideology": "Liberal Conservatism",
            "text": (
                "Founded at Fréjus on 19 May 1977, the Republican Party brought together "
                "the Independent Republicans and other supporters of Valéry Giscard "
                "d'Estaing. It succeeded the FNRI as the organised party of the liberal "
                "presidential majority.\n\n"
                "The PR favoured private enterprise, European integration and a modernised "
                "liberal conservatism. It retained a distinct identity within the broader "
                "presidential majority and competed with the Gaullists for influence."
            ),
            "icon": None,
            "wiki": "Republican Party (France)",
        },
    },
    {
        "slot": 14,
        "from": "1976.5.23",
        "entry": {
            "name": "Centre des démocrates sociaux",
            "english": "Centre of Social Democrats",
            "native_full": "Centre des démocrates sociaux",
            "language": "French",
            "abbr": "CDS",
            "catchy": False,
            "ideology": "Christian Democracy",
            "text": (
                "Created at Rennes on 23 May 1976, the Centre of Social Democrats united "
                "Jean Lecanuet's Centre démocrate with Jacques Duhamel and Joseph "
                "Fontanet's Centre démocratie et progrès. Lecanuet led the new centrist "
                "party.\n\n"
                "The CDS combined Christian social principles with European federalism, "
                "parliamentary government and decentralisation. It remained an autonomous "
                "centrist organisation while cooperating with the governing majority."
            ),
            "icon": None,
            "wiki": "Centre of Social Democrats",
        },
    },
    {
        "slot": 17,
        "from": "1984.1.28",
        "entry": {
            "name": "Les Verts",
            "english": "The Greens",
            "native_full": "Les Verts",
            "language": "French",
            "abbr": None,
            "catchy": False,
            "ideology": "Political Ecology",
            "text": (
                "The Greens were founded at Clichy on 28 and 29 January 1984, when the "
                "Verts-Parti écologiste and the Confédération écologiste united in a "
                "national political organisation. The new party gave France's ecological "
                "movement a lasting electoral structure.\n\n"
                "The Greens linked environmental protection with political reform and "
                "grassroots participation. They challenged the priorities of both the "
                "traditional right and left, while debates over electoral alliances and "
                "party organisation continued within the movement."
            ),
            "icon": None,
            "wiki": "The Greens (France)",
        },
    },
)

IDEOLOGY_BY_SLOT = {
    1: "conservatism",
    2: "liberalism",
    14: "Neutral_conservatism",
    17: "Neutral_green",
}

SOURCE_NOTE = """IMPERIA COLD WAR

# France 1970 party identity sources and boundaries

This integration changes only the dated name, description and icon selectors for
FRA party-registry slots 1, 2, 14 and 17, plus their later-period data in
`tools/party_registry_1970/data/FRA.json`. It preserves all January 1970 entries,
party slots, political leaders, ruling-party triggers and election providers. The
four icon selectors reuse the current generic MD icon for each existing ideology.

Historical basis:

- Slot 1: Larousse's contemporary 1977 yearbook records the UDR transformation
  into the RPR and dates the new name to 5 December 1976. Source: Larousse,
  *Journal de l'année 1977*, “Synthèse”,
  https://www.larousse.fr/archives/journaux_annee/1977/3/synthese. Publication
  credit: Larousse editorial staff; individual author unknown. Licence for the
  archived page is unknown. The game description paraphrases the historical facts.
- Slot 2: the same Larousse item records the Republican Party's founding at
  Fréjus on 19 May 1977 and its gathering of Independent Republicans and
  Giscardian supporters. Credit and licence as above; game text is paraphrased.
- Slot 14: the French National Archives' SIV Garance record for Centre démocrate
  gives its end date as 23 May 1976 and describes its merger with Centre
  Démocratie et progrès into Centre des démocrates sociaux. Source:
  https://rdf.archives-nationales.culture.gouv.fr/garance/entities/agent/050624/.
  Credit: Archives nationales; individual record author unknown. Record/page
  licence is unknown. The game description paraphrases the record.
- Slot 17: the Ministry's historical archives identify the Clichy meetings on
  28-29 January 1984 as the founding of Les Verts through the union of two
  ecological movements. Source:
  https://www.archives.developpement-durable.gouv.fr/fonds-europe-ecologie-les-verts-secretariat-a48139.html.
  Credit: Ministry historical archives; individual record author unknown. Page
  licence is unknown. The game description paraphrases the record.

No third-party wording, icon or logo is copied. Existing generic ideology icons
remain in use. The historical sources establish factual dates and identities;
they do not establish a licence for archival page text or third-party assets.
"""


def _day_before(value: str) -> str:
    year, month, day = (int(x) for x in value.split("."))
    previous = date(year, month, day) - timedelta(days=1)
    return f"{previous.year}.{previous.month}.{previous.day}"


def _display_name(entry: dict[str, Any]) -> str:
    if entry.get("catchy"):
        return entry["name"]
    if entry.get("abbr"):
        return f"({entry['abbr']}) - {entry['english']}"
    return entry["english"]


def _description(entry: dict[str, Any]) -> str:
    parts = []
    native = entry.get("native_full") or (entry["name"] if entry.get("catchy") else None)
    if entry.get("language") and native and native.casefold() != entry["english"].casefold():
        parts.append(f"{entry['language']}: {native}")
    if entry.get("abbr") and not entry["english"].endswith(f"({entry['abbr']})"):
        parts.append(entry["abbr"])
    head = f"({entry['ideology']}) - {entry['english']}" + (f" ({', '.join(parts)})" if parts else "")
    return head + "\n\n" + entry["text"].strip()


def _remove_identity_blocks(source: str) -> str:
    lines = source.splitlines(keepends=True)
    out: list[str] = []
    in_block = False
    for line in lines:
        if re.match(r"\s*# COLDWAR FRA2 PARTY IDENTITY .* BEGIN\s*$", line):
            if in_block:
                raise ValueError("Nested France party identity preservation markers")
            in_block = True
            continue
        if in_block:
            if re.match(r"\s*# COLDWAR FRA2 PARTY IDENTITY .* END\s*$", line):
                in_block = False
            continue
        out.append(line)
    if in_block:
        raise ValueError("Unclosed France party identity preservation marker")
    return "".join(out)


def _getter_span(source: str, name: str) -> tuple[int, int]:
    pattern = re.compile(r"(?m)^defined_text\s*=\s*\{\s*\n\s*name\s*=\s*" + re.escape(name) + r"\s*$")
    match = pattern.search(source)
    if not match:
        raise ValueError(f"Native party getter is missing: {name}")
    opening = source.find("{", match.start())
    depth = 0
    for index in range(opening, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return match.start(), index + 1
    raise ValueError(f"Unbalanced native party getter: {name}")


def _selector(slot: int, key: str, start: str, variant: str) -> str:
    before = _day_before(start)
    marker = f"{PREFIX} SLOT {slot} {variant.upper()}"
    return (
        f"\t# {marker} BEGIN\n"
        "\ttext = {\n"
        "\t\ttrigger = {\n"
        "\t\t\toriginal_tag = FRA\n"
        "\t\t\tIMP_is_1970_scenario = yes\n"
        f"\t\t\tdate > {before}\n"
        "\t\t}\n"
        f"\t\tlocalization_key = {key}\n"
        "\t}\n"
        f"\t# {marker} END\n"
    )


def _insert_selector(source: str, getter: str, slot: int, key: str, start: str, variant: str) -> str:
    begin, end = _getter_span(source, getter)
    body = source[begin:end]
    base_key = f"MDCW_HP_FRA_{slot}_0"
    found = re.search(r"(?m)^\s*localization_key\s*=\s*" + re.escape(base_key) + r"(?:_(?:desc|icon))?\s*$", body)
    if not found:
        raise ValueError(f"Base France selector {base_key} missing from {getter}")
    insertion = body.rfind("\ttext = {", 0, found.start())
    if insertion < 0:
        raise ValueError(f"Cannot locate France selector block in {getter}")
    selector = _selector(slot, key, start, variant)
    return source[:begin + insertion] + selector + source[begin + insertion:]


def _generic_icon(slot: int) -> str:
    key = f"MDCW_HP_FRA_{slot}_0_icon"
    text = PARTY_LOC.read_text(encoding="utf-8-sig")
    match = re.search(r"(?m)^\s*" + re.escape(key) + r":0\s+\"([^\"]*)\"\s*$", text)
    if not match:
        raise ValueError(f"Existing generic icon localisation is missing: {key}")
    return match.group(1)


def build_identity() -> dict[str, dict[str, Any]]:
    """Return the dated registry sources and English strings without writing files."""
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if registry.get("tag") != "FRA":
        raise ValueError("Expected the canonical FRA party registry record")
    updated = {"project": "IMPERIA COLD WAR", **deepcopy(registry)}
    loc: dict[str, str] = {}
    source = _remove_identity_blocks(GETTERS.read_text(encoding="utf-8-sig"))
    if source.startswith(PROJECT):
        source = source[len(PROJECT):]

    for identity in IDENTITIES:
        slot = int(identity["slot"])
        start = str(identity["from"])
        entry = deepcopy(identity["entry"])
        periods = updated["slots"].get(str(slot), [])
        if not periods:
            raise ValueError(f"France registry slot {slot} has no January 1970 identity")
        entry["from"] = start
        existing_index = next((i for i, period in enumerate(periods) if period.get("from") == start), None)
        if existing_index is None:
            period_index = len(periods)
            updated["slots"][str(slot)].append(entry)
        else:
            if periods[existing_index] != entry:
                raise ValueError(f"France registry slot {slot} has conflicting data for {start}")
            period_index = existing_index
        key = f"MDCW_HP_FRA_{slot}_{period_index}"
        icon = _generic_icon(slot)
        loc[key] = f"{icon} {_display_name(entry)}"
        loc[key + "_desc"] = _description(entry)
        loc[key + "_icon"] = icon

        for variant, suffix in (("name", ""), ("desc", "_desc"), ("icon", "_icon")):
            getter = f"MDCW_HP_{IDEOLOGY_BY_SLOT[slot]}{suffix}"
            source = _insert_selector(source, getter, slot, key + suffix, start, variant)

    source = PROJECT + source
    source_doc = SOURCE_NOTE
    files = {
        "common/scripted_localisation/mdcw_historical_parties.txt": source,
        "tools/party_registry_1970/data/FRA.json": json.dumps(updated, ensure_ascii=False, indent=2) + "\n",
        "tools/france_1970_runtime/IDENTITY_SOURCES.md": source_doc,
    }
    return {"files": files, "loc": loc}
