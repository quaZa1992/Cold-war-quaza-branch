# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Independently validate a staged 1970 historical politics build.

This is a read-only QA helper. It parses HOI4 braced blocks with quote/comment
awareness, checks the generated scope and exact stage deltas, and writes no game
files. Example: ``python validate.py --stage OUT/staged --catalogue data.json``.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from leader_segments import expand_country
import unicodedata


ROOT = Path(__file__).resolve().parents[2]
SPECIAL = {"CYP", "NCY", "GRE", "TUR", "EGY", "ISR", "SOV", "SPR", "USA"}
IDEOLOGIES = [
    "Western_Autocracy", "conservatism", "liberalism", "socialism",
    "communist_state", "anarchist_communism", "Conservative", "Autocracy",
    "Mod_Vilayat_e_Faqih", "Vilayat_e_Faqih", "Kingdom", "Caliphate",
    "Neutral_Muslim_Brotherhood", "Neutral_Autocracy", "Neutral_conservatism",
    "oligarchism", "Neutral_Libertarian", "Neutral_green", "neutral_Social",
    "Neutral_Communism", "Nat_Populism", "Nat_Fascism", "Nat_Autocracy",
    "Monarchist",
]
EXPECTED_HOOKS = 24 * 3 + 1
PARTY_MARKER = "# MDCW HISTORICAL PARTY REGISTRY"
NATIVE_POOL_BEGIN = "# MDCW HISTORICAL NATIVE POOLS BEGIN"
NATIVE_POOL_END = "# MDCW HISTORICAL NATIVE POOLS END"
OLD_ROUTE_BEGIN = "# MDCW HISTORICAL LEADER ROUTE BEGIN"
OLD_ROUTE_END = "# MDCW HISTORICAL LEADER ROUTE END"
RETIRE_BEGIN = "# MDCW HISTORICAL RETIRE REQUEST BEGIN"
RETIRE_END = "# MDCW HISTORICAL RETIRE REQUEST END"

GENERATED_FILES = {
    "common/scripted_localisation/mdcw_historical_parties.txt",
    "common/scripted_triggers/mdcw_historical_party_countries.txt",
    "common/scripted_effects/mdcw_historical_native_pools.txt",
    "common/scripted_triggers/mdcw_historical_native_pools.txt",
    "common/scripted_effects/mdcw_historical_special_successors.txt",
    "common/scripted_triggers/mdcw_historical_special_successors.txt",
    "common/scripted_effects/mdcw_historical_sov_egy_successors.txt",
    "common/scripted_triggers/mdcw_historical_sov_egy_successors.txt",
    "common/scripted_triggers/mdcw_historical_retirement_alternatives.txt",
    "interface/mdcw_historical_parties.gfx",
    "localisation/english/mdcw_historical_politics_1970_l_english.yml",
}
PARTY_HOOK_FILE = "common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt"
SETUP_HOOK_FILE = "common/scripted_effects/00_leader_setup_scripted_effects.txt"
NATIVE_POOL_EFFECT_FILE = "common/scripted_effects/mdcw_historical_native_pools.txt"
NATIVE_POOL_TRIGGER_FILE = "common/scripted_triggers/mdcw_historical_native_pools.txt"
LEGACY_OUTPUTS = {
    "common/scripted_effects/mdcw_historical_leadership.txt",
    "common/scripted_effects/mdcw_historical_dispatch.txt",
    "common/scripted_triggers/mdcw_historical_dispatch.txt",
    "common/decisions/categories/mdcw_historical_leadership.txt",
    "common/decisions/mdcw_historical_leadership.txt",
}
LEGACY_LOCALIZATION_IDS = {"MDCW_HP_historical_leadership", "MDCW_HP_historical_leadership_desc"}


class Validator:
    def __init__(self, root: Path, stage: Path, catalogue: Path, manifest=None):
        self.root = Path(root)
        self.stage = Path(stage)
        self.catalogue_path = Path(catalogue)
        self.manifest_path = Path(manifest) if manifest else None
        self.issues: list[dict] = []
        self.pending: list[dict] = []
        self.countries = self._load_catalogue()
        self.manifest = self._load_manifest()
        self.tags = {c.get("tag") for c in self.countries}
        self.people = {(c.get("tag"), p.get("id")): p for c in self.countries for p in c.get("leaders", [])}
        self.candidates = {}
        for country in self.countries:
            tag = country.get("tag")
            try:
                for candidate in expand_country(country):
                    self.candidates[(tag, candidate.get("id"))] = candidate
            except (KeyError, TypeError, ValueError) as exc:
                self.issue("leader_segments", f"Invalid temporal leader segments for {tag}: {exc}", tag=tag)
        self.baseline = self._load_inventory()
        self._history_leader_name_cache = {}

    def issue(self, code, message, severity="error", **context):
        self.issues.append({"severity": severity, "code": code, "message": message, **context})

    def read(self, relpath: str, stage=True):
        path = (self.stage if stage else self.root) / relpath
        if not path.is_file():
            return None
        return path.read_text(encoding="utf-8-sig")

    def _load_catalogue(self):
        path = self.catalogue_path
        payloads = []
        if path.is_dir():
            for item in sorted(path.glob("*.json")):
                try:
                    value = json.loads(item.read_text(encoding="utf-8-sig"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
                if isinstance(value, dict) and isinstance(value.get("countries"), list):
                    payloads.append(value)
        elif path.is_file():
            value = json.loads(path.read_text(encoding="utf-8-sig"))
            if isinstance(value, dict) and isinstance(value.get("countries"), list):
                payloads.append(value)
            elif isinstance(value, list):
                payloads.append({"countries": value})
        countries = []
        for payload in payloads:
            countries.extend(payload["countries"])
        unique = {}
        for country in countries:
            tag = country.get("tag")
            if tag in unique:
                self.issue("duplicate_country", f"Catalogue repeats country tag {tag}", tag=tag)
            unique[tag] = country
        return list(unique.values())

    def _load_manifest(self):
        if self.manifest_path is None:
            return {}
        if self.manifest_path.is_dir():
            records = {}
            for item in sorted(self.manifest_path.glob("*.json")):
                try:
                    value = json.loads(item.read_text(encoding="utf-8-sig"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
                if isinstance(value, dict):
                    records.update(value)
            return records
        return json.loads(self.manifest_path.read_text(encoding="utf-8-sig"))

    def _load_inventory(self):
        candidates = []
        if self.catalogue_path.is_file():
            candidates.append(self.catalogue_path.parent / "party_inventory.json")
            candidates.append(self.catalogue_path.parent.parent / "party_inventory.json")
        if self.catalogue_path.is_dir():
            candidates.append(self.catalogue_path / "party_inventory.json")
        for path in candidates:
            if path.is_file():
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
                if isinstance(payload, dict) and isinstance(payload.get("countries"), list):
                    return {x["tag"]: x for x in payload["countries"]}
        return {}

    @staticmethod
    def _parse_blocks(text: str, lower=0, upper=None):
        """Yield assignment blocks while ignoring braces in comments/strings."""
        upper = len(text) if upper is None else upper
        i = lower
        quoted = escaped = comment = False
        while i < upper:
            ch = text[i]
            if comment:
                if ch == "\n":
                    comment = False
                i += 1
                continue
            if quoted:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    quoted = False
                i += 1
                continue
            if ch == "#":
                comment = True
                i += 1
                continue
            if ch == '"':
                quoted = True
                i += 1
                continue
            if ch.isalpha() or ch == "_":
                start = i
                i += 1
                while i < upper and (text[i].isalnum() or text[i] in "_-"):
                    i += 1
                key = text[start:i]
                j = i
                while j < upper and text[j].isspace():
                    j += 1
                if j < upper and text[j] == "=":
                    j += 1
                    while j < upper and text[j].isspace():
                        j += 1
                    if j < upper and text[j] == "{":
                        end = Validator._brace_end(text, j, upper)
                        yield key, start, j, end
                        # Keep scanning inside the block as well. Callers need
                        # both outer decisions/functions and their nested
                        # allowed/effect/create_country_leader blocks.
                        i = j + 1
                        continue
                continue
            i += 1

    @staticmethod
    def _brace_end(text, start, upper):
        depth = 0
        quoted = escaped = comment = False
        for i in range(start, upper):
            ch = text[i]
            if comment:
                if ch == "\n":
                    comment = False
                continue
            if quoted:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    quoted = False
                continue
            if ch == "#":
                comment = True
            elif ch == '"':
                quoted = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i + 1
        raise ValueError("Unbalanced block in staged HOI4 file")

    @staticmethod
    def _quoted_fields(text: str, key: str):
        pattern = re.compile(r"(?<![\w-])" + re.escape(key) + r"\s*=\s*\"((?:\\.|[^\"\\])*)\"")
        for match in pattern.finditer(text):
            line_start = text.rfind("\n", 0, match.start()) + 1
            if "#" in text[line_start:match.start()]:
                continue
            yield match, match.group(1).replace('\\"', '"').replace("\\\\", "\\")

    @staticmethod
    def _scalar_fields(text: str, key: str):
        pattern = re.compile(r"(?m)(?<![\w-])" + re.escape(key) + r"\s*=\s*([A-Za-z0-9_]+)\s*(?:#.*)?$")
        for match in pattern.finditer(text):
            yield match, match.group(1)

    @staticmethod
    def _field_block(text: str, key: str):
        for name, _, opening, end in Validator._parse_blocks(text):
            if name == key:
                return text[opening + 1:end - 1]
        return None

    @staticmethod
    def _normalized_person_name(value: str) -> str:
        decomposed = unicodedata.normalize("NFKD", value)
        return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).replace("’", "'").replace("‘", "'").casefold()

    @staticmethod
    def _identity_name_key(value: str) -> str:
        decomposed = unicodedata.normalize("NFKD", value).casefold()
        return "".join(ch for ch in decomposed if ch.isalnum())

    def _history_starting_name(self, tag):
        """Return the sole leader name created in this tag's 1970.1.1 block."""
        if tag not in self._history_leader_name_cache:
            files = sorted((self.root / "history/countries").glob(f"{tag} - *.txt"))
            starter = None
            if len(files) == 1:
                try:
                    text = files[0].read_text(encoding="utf-8-sig")
                    date_block = re.search(r"(?m)^[ \t]*1970\.1\.1\s*=\s*\{", text)
                    if date_block:
                        opening = text.find("{", date_block.start(), date_block.end())
                        ending = self._brace_end(text, opening, len(text))
                        body = text[opening + 1:ending - 1]
                        names = []
                        for key, _, leader_open, leader_end in self._parse_blocks(body):
                            if key == "create_country_leader":
                                name_values = [value for _, value in self._quoted_fields(body[leader_open + 1:leader_end - 1], "name")]
                                if len(name_values) == 1:
                                    names.append(name_values[0])
                        unique_names = sorted(set(names), key=str.casefold)
                        if len(unique_names) == 1:
                            starter = unique_names[0]
                except (OSError, UnicodeDecodeError, ValueError):
                    starter = None
            self._history_leader_name_cache[tag] = starter
        return self._history_leader_name_cache[tag]

    def _history_name_alias(self, tag, index, person, pools):
        starter = self._history_starting_name(tag)
        if not starter or starter == person["name"]:
            return None
        identity = self._identity_name_key(starter)
        matches = [
            (candidate_index, row)
            for (candidate_tag, candidate_index), rows in pools.items()
            if candidate_tag == tag
            for row in rows
            if self._identity_name_key(row["name"]) == identity
        ]
        unique_matches = {(candidate_index, row["id"], row["name"].casefold()) for candidate_index, row in matches}
        if len(unique_matches) == 1 and matches[0][0] == index and matches[0][1]["id"] == person["id"]:
            return starter
        return None

    def _portrait(self, tag, person):
        key = f"{tag}_{person.get('catalogue_id', person.get('id', ''))}"
        manifest_value = self.manifest.get(key) if isinstance(self.manifest, dict) else None
        value = None
        if isinstance(manifest_value, dict):
            status = manifest_value.get("status")
            provenance = manifest_value.get("provenance")
            if status in {"visually_reviewed", "edited_visually_reviewed", "original_historical_user_approved", "reviewed", "approved", "existing_exact_name_md_reference"} or (status is None and provenance == "existing exact-name MD reference"):
                value = manifest_value.get("portrait") or manifest_value.get("path")
        if not value:
            return None
        path = Path(str(value).replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts:
            return None
        if (self.stage / path).is_file() or (self.root / path).is_file():
            return path.as_posix()
        return None

    def check_coverage(self):
        if len(self.countries) != 163:
            self.issue("coverage_count", f"Expected 163 country records; found {len(self.countries)}")
        tags = [c.get("tag") for c in self.countries]
        if len(set(tags)) != len(tags):
            self.issue("duplicate_country", "Catalogue country tags are not unique")
        bad = [c.get("tag") for c in self.countries if not re.fullmatch(r"[A-Z0-9]{3}", str(c.get("tag", "")))]
        if bad:
            self.issue("invalid_tags", "Catalogue contains malformed country tags", tags=bad)
        for country in self.countries:
            tag = country.get("tag")
            for party in country.get("parties", []):
                if not isinstance(party.get("index"), int) or not 0 <= party["index"] < 24:
                    self.issue("invalid_party_index", f"Invalid native party slot for {tag}", tag=tag, party=party)
                if party.get("source_urls") is not None and not party.get("source_urls"):
                    self.issue("missing_party_sources", f"Party row lacks sources for {tag}", tag=tag, party=party.get("name"))
            try:
                candidates = expand_country(country)
            except (KeyError, TypeError, ValueError) as exc:
                self.issue("leader_segments", f"Invalid temporal leader segments for {tag}: {exc}", tag=tag)
                candidates = []
            for candidate in candidates:
                index = candidate.get("party_index")
                if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < 24:
                    self.issue("invalid_leader_party", f"Invalid MD family for {tag}/{candidate.get('id')}", tag=tag)
                portrait = self._portrait(tag, candidate)
                if portrait is None:
                    canonical_id = candidate.get("catalogue_id", candidate.get("id"))
                    if not any(row.get("tag") == tag and row.get("id") == canonical_id for row in self.pending):
                        self.pending.append({"tag": tag, "id": canonical_id, "name": candidate.get("name"), "reason": "no installed/reviewed portrait"})

    def check_party_localisation(self):
        registry = self.read("common/scripted_localisation/mdcw_historical_parties.txt")
        hooks = self.read(PARTY_HOOK_FILE)
        english = self.read("localisation/english/mdcw_historical_politics_1970_l_english.yml")
        if not registry or not hooks or not english:
            self.issue("missing_party_outputs", "Missing one or more generated party localisation outputs")
            return
        definitions = []
        for key, _, opening, end in self._parse_blocks(registry):
            if key == "defined_text":
                body = registry[opening + 1:end - 1]
                values = list(self._scalar_fields(body, "name"))
                if values:
                    definitions.append(values[0][1])
        expected = {f"MDCW_HP_{ideology}{suffix}" for ideology in IDEOLOGIES for suffix in ("", "_desc", "_icon")}
        expected.add("MDCW_HP_ruling_party")
        counts = Counter(definitions)
        missing = sorted(expected - set(counts))
        duplicate = sorted(k for k, v in counts.items() if v != 1)
        if missing or duplicate or len(definitions) != EXPECTED_HOOKS:
            self.issue("resolver_definitions", "Party resolvers are incomplete or duplicated",
                       missing=missing, duplicate=duplicate, found=len(definitions), expected=EXPECTED_HOOKS)

        marker_lines = [line for line in hooks.splitlines() if PARTY_MARKER in line]
        if len(marker_lines) != EXPECTED_HOOKS:
            self.issue("party_hooks", f"Expected 73 inserted localisation hooks, found {len(marker_lines)}", count=len(marker_lines))
        for name in sorted(expected):
            key_literal = f'localization_key = "[{name}]"'
            count = sum(key_literal in line for line in marker_lines)
            if count != 1:
                self.issue("party_hook_name", f"Expected one shared hook for {name}, found {count}", name=name)

        ids = re.findall(r"(?m)^\s*(MDCW_HP_[A-Za-z0-9_]+):\d+\s+\"", english)
        duplicates = sorted(k for k, n in Counter(ids).items() if n > 1)
        if duplicates:
            self.issue("duplicate_english_ids", "Generated English localisation identifiers are duplicated", ids=duplicates)
        self.check_timeline(english)

    def check_timeline(self, english):
        from party_presentation import load_names
        native_names = load_names().get("USA", {}).get("party_names", {})
        usa = next((c for c in self.countries if c.get("tag") == "USA"), None)
        if not usa:
            self.issue("usa_timeline", "USA record missing from catalogue")
            return
        dates = ["1970.1.1", "1976.1.1", "1980.1.1", "1990.1.1", "2000.1.1"]
        observed = {}
        loc_values = {}
        for match in re.finditer(r"(?m)^\s*(MDCW_HP_[A-Za-z0-9_]+):\d+\s+\"((?:\\.|[^\"\\])*)\"", english):
            loc_values[match.group(1)] = match.group(2).replace('\\"', '"')
        for sample in dates:
            d = date(*map(int, sample.split(".")))
            observed[sample] = {}
            for family in (2, 16):
                active = []
                for party in usa.get("parties", []):
                    if party.get("index") != family:
                        continue
                    start = date(*map(int, party.get("from", "1970.1.1").split(".")))
                    end = date(*map(int, party["until"].split("."))) if party.get("until") else date(2001, 1, 1)
                    if start <= d < end:
                        active.append(party["name"])
                label = " / ".join(dict.fromkeys(active))
                observed[sample][str(family)] = label
                display = " / ".join(dict.fromkeys(native_names.get(name, name) for name in active))
                actual_localized = [v for k, v in loc_values.items()
                                    if k.startswith(f"MDCW_HP_USA_party_{family}_")
                                    and re.sub(r"£\w+\s*", "", v) == display]
                if label and not actual_localized:
                    self.issue("usa_timeline", f"USA family index {family} label missing at {sample}", date=sample, expected=display)
                if family == 2 and "Libertarian Party" in label:
                    self.issue("usa_party_slot", "USA Libertarian Party must remain in native index 16, not index 2", date=sample)
                if family == 16 and "Democratic Party" in label:
                    self.issue("usa_party_slot", "USA Democratic Party must remain in native index 2, not index 16", date=sample)
            if "Democratic Party" not in observed[sample]["2"]:
                self.issue("usa_timeline", f"USA native liberal family index 2 lacks Democratic Party at {sample}", date=sample)
            expected_libertarian = d >= date(1971, 12, 11)
            has_libertarian = "Libertarian Party" in observed[sample]["16"]
            if has_libertarian != expected_libertarian:
                self.issue("usa_libertarian_family", f"USA Libertarian Party should appear in native index 16 from 1971.12.11; sample {sample}", observed=observed[sample])
        self.timeline = observed

    def expected_native_pools(self):
        """Return reviewed, non-delegated candidate rows grouped by MD family."""
        expected = defaultdict(list)
        for country in self.countries:
            tag = country.get("tag")
            if tag in SPECIAL:
                continue
            try:
                candidates = expand_country(country)
            except (KeyError, TypeError, ValueError):
                continue
            for person in candidates:
                if person.get("managed_by_existing_system"):
                    continue
                portrait = self._portrait(tag, person)
                if portrait is None:
                    continue
                expected[(tag, person["party_index"])].append({
                    "id": person.get("id"),
                    "catalogue_id": person.get("catalogue_id", person.get("id")),
                    "name": person.get("name", ""),
                    "ideology": IDEOLOGIES[person["party_index"]],
                    "portrait": portrait,
                    "available_from": person["available_from"],
                })
        for rows in expected.values():
            rows.sort(key=lambda row: (date(*map(int, row["available_from"].split("."))), row["id"]))
        deduped = {}
        for key, rows in expected.items():
            seen = set()
            for row in rows:
                person_key = row["name"].casefold()
                if person_key not in seen:
                    deduped.setdefault(key, []).append(row)
                    seen.add(person_key)
        return deduped

    def check_native_pools(self):
        """Check native leader pools against reviewed identities and chronology."""
        effects = self.read(NATIVE_POOL_EFFECT_FILE) or ""
        trigger = self.read(NATIVE_POOL_TRIGGER_FILE) or ""
        pools = self.expected_native_pools()
        helper_rows = {}
        for key, _, opening, end in self._parse_blocks(effects):
            match = re.fullmatch(r"MDCW_HP_native_pool_([A-Z0-9]{3})_(\d+)", key)
            if not match:
                continue
            pool = (match.group(1), int(match.group(2)))
            if pool in helper_rows:
                self.issue("duplicate_native_pool", f"Duplicate native leader pool helper {key}")
            body = effects[opening + 1:end - 1]
            candidates = []
            for name, _, candidate_open, candidate_end in self._parse_blocks(body):
                if name != "create_country_leader":
                    continue
                candidate_body = body[candidate_open + 1:candidate_end - 1]
                names = [value for _, value in self._quoted_fields(candidate_body, "name")]
                pictures = [value.replace("\\", "/") for _, value in self._quoted_fields(candidate_body, "picture")]
                ideologies = [value for _, value in self._scalar_fields(candidate_body, "ideology")]
                if len(names) != 1 or len(pictures) != 1 or len(ideologies) != 1:
                    self.issue("native_pool_candidate_shape", f"{key} has a candidate without exactly one name, portrait and ideology")
                    continue
                candidates.append({"name": names[0], "portrait": pictures[0], "ideology": ideologies[0]})
            helper_rows[pool] = (body, candidates)

        expected_keys = set(pools)
        actual_keys = set(helper_rows)
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys)
        if missing or extra:
            self.issue("native_pool_coverage", "Native leader pools do not cover exactly the reviewed portrait-ready families",
                       missing=[f"{tag}/{index}" for tag, index in missing],
                       extra=[f"{tag}/{index}" for tag, index in extra])

        counters_by_index = {index: ideology + "_leader" for index, ideology in enumerate(IDEOLOGIES)}
        for key in sorted(expected_keys & actual_keys):
            tag, index = key
            body, actual = helper_rows[key]
            expected = pools[key]
            expected_triplets = [(r["name"], r["portrait"], r["ideology"]) for r in expected]
            actual_triplets = [(r["name"], r["portrait"], r["ideology"]) for r in actual]
            # The final else is a deliberate corruption-safe fallback to slot 0.
            if len(actual_triplets) == len(expected_triplets) + 1 and actual_triplets[-1:] == actual_triplets[:1]:
                actual_triplets.pop()
            if actual_triplets != expected_triplets:
                self.issue("native_pool_members", f"Native pool {tag}/{index} has missing, extra, mis-portrayed, or misordered candidates",
                           expected=expected_triplets, actual=actual_triplets)
            unique_actual = actual[:-1] if len(actual) == len(expected) + 1 and actual[-1] == actual[0] else actual
            if len({row["name"] for row in unique_actual}) != len(unique_actual):
                self.issue("native_pool_duplicate_person", f"Native pool {tag}/{index} repeats a person")
            # The generated pool deliberately has no per-person dates: the native
            # counter must keep the entire historical pool available in every
            # 1970-scenario year. Chronological order determines first priority.
            if re.search(r"(?m)^\s*date\s*[<>]=?\s*", body):
                self.issue("native_pool_person_dates", f"Native pool {tag}/{index} gates individual candidates by date")
            if re.search(r"2001\.1\.1", body):
                self.issue("native_pool_end_gate", f"Native pool {tag}/{index} has an end-of-2000 gate")
            counter = counters_by_index[index]
            if counter not in body:
                self.issue("native_pool_counter", f"Native pool {tag}/{index} does not use its native {counter} counter")
            if "do_not_retire" not in body:
                self.issue("native_pool_protection", f"Native pool {tag}/{index} does not preserve do_not_retire incumbents")
            slots = [int(value) for value in re.findall(
                r"check_variable\s*=\s*\{\s*" + re.escape(counter) + r"\s*=\s*(\d+)\s*\}", body)]
            if slots != list(range(len(expected))):
                self.issue("native_pool_slot_order", f"Native pool {tag}/{index} counter slots are not contiguous in chronological order",
                           expected=list(range(len(expected))), actual=slots)
            for slot in range(len(expected)):
                guard = re.search(
                    r"has_country_flag\s*=\s*do_not_retire\s*\}\s*set_variable\s*=\s*\{\s*" +
                    re.escape(counter) + rf"\s*=\s*{slot}\s*\}}.*?else\s*=\s*\{{\s*set_variable\s*=\s*\{{\s*" +
                    re.escape(counter) + rf"\s*=\s*{(slot + 1) % len(expected)}\s*\}}",
                    body, re.S)
                if not guard:
                    self.issue("native_pool_counter_advance", f"Native pool {tag}/{index} slot {slot} does not advance and wrap its counter safely")
            if re.search(r"(?m)^\s*(?:set_politics\s*=|set_ruling_party\s*=|add_popularity\s*=|on_actions\s*=|country_event\s*=)", body):
                self.issue("native_pool_changes_government", f"Native pool {tag}/{index} changes government or popularity")

        if not trigger:
            self.issue("missing_native_pool_trigger", "Native pool availability trigger is missing")
        elif "MDCW_HP_has_native_pool" not in trigger:
            self.issue("native_pool_trigger_name", "Native pool trigger has no MDCW_HP_has_native_pool definition")
        elif "IMP_is_1970_scenario = yes" not in trigger or "has_variable = ruling_party" not in trigger:
            self.issue("native_pool_trigger_gate", "Native pool trigger lacks the 1970-scenario or ruling-party guard")
        self.check_native_pool_setters(pools)
        self.check_native_counter_sync(pools, effects)
        self.check_legacy_outputs()

    def check_native_pool_setters(self, pools):
        expected_tags = {tag for tag, _ in pools}
        for tag in sorted(expected_tags):
            rel = f"common/scripted_effects/{tag}_political_leaders.txt"
            text = self.read(rel)
            if not text:
                self.issue("missing_native_setter", f"Missing native set_leader pool patch for {tag}")
                continue
            marker_begin = f"# MDCW HISTORICAL NATIVE POOL {tag} BEGIN"
            marker_end = f"# MDCW HISTORICAL NATIVE POOL END {tag}"
            if text.count(marker_begin) != 1 or text.count(marker_end) != 1:
                self.issue("native_setter_marker", f"{tag} setter must contain one marked native-pool branch")
                continue
            region = self._marked_region(text, marker_begin, marker_end)
            if not region:
                self.issue("native_setter_marker", f"Cannot extract marked native-pool branch for {tag}")
                continue
            indices = sorted(index for candidate_tag, index in pools if candidate_tag == tag)
            if "IMP_is_1970_scenario = yes" not in region:
                self.issue("native_setter_scenario", f"{tag} native pool branch lacks the 1970-scenario gate")
            for index in indices:
                helper = f"MDCW_HP_native_pool_{tag}_{index} = yes"
                if helper not in region:
                    self.issue("native_setter_family", f"{tag} setter omits current family {index}")
            family_branch = re.split(r"\belse\s*=\s*\{", region, maxsplit=1)[0]
            observed = {int(x) for x in re.findall(r"check_variable\s*=\s*\{\s*ruling_party\s*=\s*(\d+)\b", family_branch)}
            if observed != set(indices):
                self.issue("native_setter_family", f"{tag} setter family branches do not match reviewed pools", expected=indices, actual=sorted(observed))

    def check_native_counter_sync(self, pools, effects):
        setup = self.read(SETUP_HOOK_FILE)
        counters_by_index = {index: ideology + "_leader" for index, ideology in enumerate(IDEOLOGIES)}
        if not setup:
            self.issue("missing_native_sync_hook", "Native leader setup hook is missing")
            return
        if effects.count("MDCW_HP_sync_native_counter") != 1:
            self.issue("native_sync_effect", "Generated effects must define one native incumbent counter sync helper")
        sync_positions = [m.start() for m in re.finditer(r"(?m)^\s*MDCW_HP_sync_native_counter\s*=\s*yes\s*$", setup)]
        kill_positions = [m.start() for m in re.finditer(r"(?m)^\s*kill_country_leader\s*=\s*yes\s*$", setup)]
        if len(sync_positions) != 1 or not kill_positions or sync_positions[0] >= kill_positions[0]:
            self.issue("native_sync_order", "Incumbent counter sync must run once before native leader removal")
        sync = self._field_block(effects, "MDCW_HP_sync_native_counter") or ""
        if "ruling_only = yes" not in sync or "has_country_leader" not in sync:
            self.issue("native_sync_identity", "Counter sync must match the exact current ruling leader")
        if "original_tag" not in sync or "ruling_party" not in sync:
            self.issue("native_sync_scope", "Counter sync must be scoped to original tag and current ruling family")
        if "seeded_" in sync or re.search(r"has_variable\s*=\s*MDCW_HP_native_pool_seeded_", sync):
            self.issue("native_sync_one_shot", "Incumbent counter sync must run on every central set_leader call, without one-shot seed state")
        for (tag, index), rows in pools.items():
            branches = []
            for name, _, opening, end in self._parse_blocks(sync):
                if name != "if":
                    continue
                body = sync[opening + 1:end - 1]
                limit = self._field_block(body, "limit") or ""
                if re.search(rf"\boriginal_tag\s*=\s*{tag}\b", limit) and re.search(
                        rf"check_variable\s*=\s*\{{\s*ruling_party\s*=\s*{index}\s*\}}", limit):
                    branches.append(body)
            if len(branches) != 1:
                self.issue("native_sync_pool_branch", f"Expected one repeating incumbent-sync branch for {tag}/{index}", count=len(branches))
                continue
            branch = branches[0]
            counter = counters_by_index[index]
            compact_branch = re.sub(r"\s+", " ", branch).strip()
            for slot, person in enumerate(rows):
                name = person["name"].replace("\\", "\\\\").replace('"', '\\"')
                alias = self._history_name_alias(tag, index, person, pools)
                name_test = f'has_country_leader = {{ name = "{name}" ruling_only = yes }}'
                if alias:
                    alias = alias.replace("\\", "\\\\").replace('"', '\\"')
                    name_test = f'OR = {{ {name_test} has_country_leader = {{ name = "{alias}" ruling_only = yes }} }}'
                next_slot = (slot + 1) % len(rows)
                expected_flow = (
                    f'{"if" if slot == 0 else "else_if"} = {{ '
                    f'limit = {{ {name_test} }} '
                    f'if = {{ limit = {{ has_country_flag = do_not_retire }} '
                    f'set_variable = {{ {counter} = {slot} }} }} '
                    f'else = {{ set_variable = {{ {counter} = {next_slot} }} }} }}'
                )
                if expected_flow not in compact_branch:
                    self.issue("native_sync_counter_choice", f"Sync for {tag}/{index} does not map {person['name']} to current slot when protected and next slot otherwise",
                               slot=slot, expected_next=next_slot)
        if "MDCW_HP_has_native_pool = yes" not in setup or not re.search(
                r"NOT\s*=\s*\{\s*MDCW_HP_has_native_pool\s*=\s*yes\s*\}", setup):
            self.issue("native_setup_guard", "DDR/PAK native setup bypass must depend on an available native pool")

    def check_legacy_outputs(self):
        for rel in sorted(LEGACY_OUTPUTS):
            if (self.stage / rel).exists():
                self.issue("legacy_output_present", f"Retired manual-leadership output is still staged: {rel}")
        english = self.read("localisation/english/mdcw_historical_politics_1970_l_english.yml") or ""
        legacy_ids = sorted(set(re.findall(r"(?m)^\s*(MDCW_HP_[A-Za-z0-9_]+):\d+", english)) & LEGACY_LOCALIZATION_IDS)
        legacy_ids += sorted(set(re.findall(r"(?m)^\s*(MDCW_HP_select_[A-Za-z0-9_]+):\d+", english)))
        if legacy_ids:
            self.issue("legacy_leadership_localisation", "Manual-decision localization keys remain", ids=legacy_ids)
        for rel in (SETUP_HOOK_FILE, "common/scripted_guis/00_MD_politicsview_scripted_guis.txt"):
            text = self.read(rel) or ""
            if "MDCW HISTORICAL LEADER ROUTE" in text or "MDCW_HP_retire_request" in text:
                self.issue("legacy_leadership_hook", f"Retired custom leadership routing remains in {rel}")

    def check_native_file_deltas(self):
        changed = []
        # Regenerate presentation only: this permits its exact intentional
        # branch/icon changes without weakening unrelated shared-file checks.
        # A local import avoids the build -> presentation -> validator cycle.
        from build import Builder
        party_builder = Builder({country["tag"]: country for country in self.countries})
        party_builder.parties()
        party_outputs = party_builder.outputs
        for rel, expected in party_outputs.items():
            actual = self.read(rel)
            if actual is None or self._normalized(actual) != self._normalized(expected.removeprefix("\ufeff")):
                self.issue("party_presentation_delta", f"Staged party presentation differs from exact current-input regeneration: {rel}", file=rel)
        expected_tags = {tag for tag, _ in self.expected_native_pools()}
        native_refs = defaultdict(lambda: defaultdict(set))
        for country in self.countries:
            for person in country.get("leaders", []):
                for ref in person.get("native_sources", []):
                    if not isinstance(ref, str) or "#" not in ref:
                        continue
                    source, func = ref.rsplit("#", 1)
                    native_refs[source.replace("\\", "/")][func].add(person.get("native_name", person.get("name", "")))
        # Bespoke country portrait patches use a separate reviewed catalogue
        # from the generic 163-country world data.
        special_catalogues = [self.stage.parent.parent / "existing_special_portraits.json",
                              self.root / "tools/historical_politics_1970/special_portraits.json"]
        for special_path in special_catalogues:
            if not special_path.is_file():
                continue
            try:
                special = json.loads(special_path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                continue
            for country in special.get("countries", []):
                for person in country.get("leaders", []):
                    for ref in person.get("native_sources", []):
                        if isinstance(ref, str) and "#" in ref:
                            source, func = ref.rsplit("#", 1)
                            native_refs[source.replace("\\", "/")][func].add(person.get("native_name", person.get("name", "")))
            break
        for staged_file in self.stage.rglob("*"):
            if not staged_file.is_file():
                continue
            rel = staged_file.relative_to(self.stage).as_posix()
            original = self.root / rel
            if not original.is_file():
                if rel.startswith("common/on_actions/") or rel.startswith("events/"):
                    self.issue("new_automatic_hook", f"Unexpected new event/on_action file in stage: {rel}")
                continue
            new = staged_file.read_text(encoding="utf-8-sig")
            old = original.read_text(encoding="utf-8-sig")
            if new == old:
                continue
            changed.append(rel)
            if rel in party_outputs:
                continue  # Exact regeneration above already checked all bytes.
            elif rel == SETUP_HOOK_FILE:
                expected_old = self._strip_marker_region(old, OLD_ROUTE_BEGIN, OLD_ROUTE_END)
                expected_old = self._normalize_setup_guard(expected_old)
                expected_old = self._strip_marker_region(expected_old,
                    "# MDCW HISTORICAL NATIVE COUNTER SYNC BEGIN",
                    "# MDCW HISTORICAL NATIVE COUNTER SYNC END")
                stripped = self._strip_marker_region(new,
                    "# MDCW HISTORICAL NATIVE COUNTER SYNC BEGIN",
                    "# MDCW HISTORICAL NATIVE COUNTER SYNC END")
                stripped = self._strip_marker_region(stripped,
                    "# MDCW SPECIAL RETIREMENT SYNC BEGIN",
                    "# MDCW SPECIAL RETIREMENT SYNC END")
                stripped = self._strip_marker_region(stripped,
                    "# MDCW SOVIET RETIREMENT ROUTE BEGIN",
                    "# MDCW SOVIET RETIREMENT ROUTE END")
                stripped = re.sub(
                    r"(?m)^(\t)else_if(?= = \{\n\t\tlimit = \{ original_tag = CYP IMP_is_1970_scenario = yes \})",
                    r"\1if", stripped)
                if self._normalized_script(stripped) != self._normalized_script(expected_old):
                    self.issue("native_setup_delta", "Shared leader setup changed beyond documented counter sync, SOV manual route, and DDR/PAK pool guard")
            elif rel == "common/scripted_guis/00_MD_politicsview_scripted_guis.txt":
                restored_old, count = self._restore_retire_wrapper(old)
                restored_new, new_count = self._restore_retire_wrapper(new)
                restored_new = self._restore_native_retirement_context(restored_new)
                restored_new = self._strip_marker_region(restored_new,
                    "# MDCW SOVIET RETIREMENT AVAILABILITY BEGIN",
                    "# MDCW SOVIET RETIREMENT AVAILABILITY END")
                restored_new = restored_new.replace(
                    "NOT = { AND = { OR = { original_tag = DDR original_tag = PAK } IMP_is_1970_scenario = yes NOT = { MDCW_HP_has_native_pool = yes } } }",
                    "NOT = { AND = { OR = { original_tag = DDR original_tag = PAK } IMP_is_1970_scenario = yes } }")
                if count > 1 or new_count > 1 or self._normalized_script(restored_new) != self._normalized_script(restored_old):
                    self.issue("retire_shared_delta", "Retire GUI changed outside its temporary native-retirement context and reviewed availability guards")
            elif re.fullmatch(r"common/scripted_effects/[A-Z0-9]{3}_political_leaders\.txt", rel):
                tag = Path(rel).name[:3]
                if tag in {"USA", "SPR"}:
                    restored = self._restore_special_successor_setter(new, tag)
                    if restored is None or self._normalized_script(restored) != self._normalized_script(old):
                        self.issue("special_setter_fallback_delta", f"{rel} changes the existing native selector outside its marked manual-successor wrapper")
                elif tag == "EGY":
                    restored = self._restore_egy_successor_setter(new)
                    if restored is None or self._normalized_script(restored) != self._normalized_script(old):
                        self.issue("egy_setter_fallback_delta", "EGY native selector changes beyond its temporary manual-successor branch")
                elif tag == "SOV":
                    restored = self._strip_marker_region(new, "# MDCW HP SOV CIVILIAN SUCCESSOR BEGIN", "# MDCW HP SOV CIVILIAN SUCCESSOR END")
                    if self._normalized_script(restored) != self._normalized_script(old):
                        self.issue("sov_setter_fallback_delta", "SOV native selector changes beyond the marked civilian successor branch")
                elif tag not in expected_tags:
                    self.issue("unexpected_native_setter", f"Native setter patch has no reviewed pool: {rel}")
                else:
                    restored = self._restore_native_pool_setter(new, tag)
                    if restored is None or self._normalized_script(restored) != self._normalized_script(old):
                        self.issue("native_setter_fallback_delta", f"{rel} changes the existing native selector outside its marked pool wrapper")
            elif rel == "localisation/english/mdcw_historical_politics_1970_l_english.yml":
                strip_generated = lambda value: re.sub(r"(?m)^\s*MDCW_HP_[A-Za-z0-9_]+:\d+.*(?:\n|$)", "", value)
                if self._normalized(strip_generated(new)) != self._normalized(strip_generated(old)):
                    self.issue("historical_localization_delta", "Generated historical localization changed unrelated English localization lines")
            elif rel == "common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt":
                restored = self._restore_sov_retirement_patches(new)
                if restored is None or self._normalized_script(restored) != self._normalized_script(old):
                    self.issue("sov_history_delta", "SOV succession source changed outside marked pending-state handoff/clear effects")
            elif rel in native_refs:
                masked_new = self._mask_native_pictures(rel, new, native_refs[rel])
                masked_old = self._mask_native_pictures(rel, old, native_refs[rel])
                if masked_new is None or masked_old is None or self._normalized(masked_new) != self._normalized(masked_old):
                    self.issue("native_shared_delta", f"Native source {rel} changed outside referenced exact leader picture fields")
            else:
                self.issue("unexpected_shared_delta", f"Staged existing file changed outside allowlisted hook/portrait files: {rel}")
        for rel in (PARTY_HOOK_FILE, SETUP_HOOK_FILE, "common/scripted_guis/00_MD_politicsview_scripted_guis.txt"):
            if not (self.stage / rel).is_file():
                self.issue("missing_shared_stage", f"Expected modified shared file absent from stage: {rel}")
        for tag in expected_tags:
            rel = f"common/scripted_effects/{tag}_political_leaders.txt"
            if not (self.stage / rel).is_file():
                self.issue("missing_native_setter", f"Expected staged native setter file is absent: {rel}")
        self.changed_shared = changed

    def check_native_retirement_wiring(self):
        """Check manual-retirement scoping and routing without trusting the builder."""
        setup = self.read(SETUP_HOOK_FILE) or ""
        gui = self.read("common/scripted_guis/00_MD_politicsview_scripted_guis.txt") or ""
        effects = self.read(NATIVE_POOL_EFFECT_FILE) or ""
        trigger = self.read("common/scripted_triggers/mdcw_historical_sov_egy_successors.txt") or ""
        gui_markers = (
            "# MDCW NATIVE RETIREMENT CONTEXT BEGIN",
            "# MDCW NATIVE RETIREMENT CONTEXT END",
            "# MDCW SOVIET RETIREMENT AVAILABILITY BEGIN",
            "# MDCW SOVIET RETIREMENT AVAILABILITY END",
        )
        setup_markers = (
            "# MDCW SPECIAL RETIREMENT SYNC BEGIN",
            "# MDCW SPECIAL RETIREMENT SYNC END",
            "# MDCW SOVIET RETIREMENT ROUTE BEGIN",
            "# MDCW SOVIET RETIREMENT ROUTE END",
        )
        for marker in gui_markers:
            if gui.count(marker) != 1:
                self.issue("retirement_gui_marker", f"Expected exactly one retirement GUI marker: {marker}")
        for marker in setup_markers:
            if setup.count(marker) != 1:
                self.issue("retirement_setup_marker", f"Expected exactly one retirement setup marker: {marker}")
        context = self._marked_region(gui,
            "# MDCW NATIVE RETIREMENT CONTEXT BEGIN",
            "# MDCW NATIVE RETIREMENT CONTEXT END")
        if context is None:
            self.issue("retirement_gui_context", "Manual retirement context is not a single well-formed marked region")
        else:
            calls = re.findall(r"(?m)^\s*set_leader\s*=\s*yes\s*$", context)
            if len(calls) != 1:
                self.issue("retirement_gui_context", "Temporary context must wrap exactly one native set_leader call")
            if not re.search(r"set_temp_variable\s*=\s*\{\s*MDCW_HP_native_retirement\s*=\s*1\s*\}", context):
                self.issue("retirement_gui_context", "Manual retire button does not set the retirement context")
            if not re.search(r"set_temp_variable\s*=\s*\{\s*MDCW_HP_native_retirement\s*=\s*0\s*\}", context):
                self.issue("retirement_gui_context", "Manual retire button does not clear the retirement context")
            if "has_country_flag = MDCW_HP_native_retirement" in context or "set_country_flag = MDCW_HP_native_retirement" in context:
                self.issue("retirement_gui_context", "Manual-retirement context must be temporary, not a persistent country flag")
        if "MDCW_HP_sync_special_counter = yes" not in setup or "MDCW_HP_sync_sov_egy_counter = yes" not in setup:
            self.issue("retirement_sync_calls", "Central leader setup must synchronize special and SOV/EGY counters")
        special_sync = self._marked_region(setup,
            "# MDCW SPECIAL RETIREMENT SYNC BEGIN",
            "# MDCW SPECIAL RETIREMENT SYNC END") or ""
        generic_kill = setup.find("kill_country_leader")
        sync_pos = setup.find("# MDCW SPECIAL RETIREMENT SYNC BEGIN")
        if generic_kill >= 0 and sync_pos > generic_kill:
            self.issue("retirement_sync_order", "Special and SOV/EGY incumbent sync must run before the central leader removal")
        sov_route = self._marked_region(setup,
            "# MDCW SOVIET RETIREMENT ROUTE BEGIN",
            "# MDCW SOVIET RETIREMENT ROUTE END") or ""
        if not re.search(r"original_tag\s*=\s*SOV", sov_route) or not re.search(r"ruling_party\s*=\s*4", sov_route):
            self.issue("soviet_retirement_scope", "SOV manual route must be limited to the communist family")
        if "is_dynamic_country = no" not in sov_route:
            self.issue("soviet_retirement_scope", "SOV manual route must be limited to the original country, not dynamic rebels")
        if "check_variable = { MDCW_HP_native_retirement = 1 }" not in sov_route:
            self.issue("soviet_retirement_scope", "SOV manual route must require the temporary GUI context")
        if "MDCW_HP_SOV_native_retirement = yes" not in sov_route:
            self.issue("soviet_retirement_route", "SOV communist manual retirement does not call the native succession route")
        availability = self._marked_region(gui,
            "# MDCW SOVIET RETIREMENT AVAILABILITY BEGIN",
            "# MDCW SOVIET RETIREMENT AVAILABILITY END") or ""
        if "original_tag = SOV" not in availability or "ruling_party = 4" not in availability or "MDCW_HP_SOV_retirement_available = yes" not in availability or "is_dynamic_country = no" not in availability:
            self.issue("soviet_retirement_availability", "Retirement button must expose SOV only when the communist successor route is available")
        if "NOT = { MDCW_HP_has_native_pool = yes }" not in gui:
            self.issue("native_retirement_availability", "DDR/PAK manual retirement guard must depend on a reviewed native pool")
        alternative_trigger = self.read("common/scripted_triggers/mdcw_historical_retirement_alternatives.txt") or ""
        if "MDCW_HP_retirement_has_alternative" not in alternative_trigger or "custom_trigger_tooltip = { tooltip = MDCW_HP_retirement_no_alternative_tt MDCW_HP_retirement_has_alternative = yes }" not in gui:
            self.issue("retirement_alternative_guard", "Manual retirement must be blocked with the no-alternative tooltip when the current leader is the sole pool member")
        if "MDCW_HP_retirement_no_alternative_tt:" not in (self.read("localisation/english/mdcw_historical_politics_1970_l_english.yml") or ""):
            self.issue("retirement_alternative_localisation", "No-alternative retirement tooltip localization is missing")
        if "MDCW_HP_has_sov_egy_successor_pool" not in trigger or "MDCW_HP_SOV_retirement_available" not in trigger:
            self.issue("soviet_retirement_trigger", "SOV/EGY successor availability triggers are missing from the native trigger file")
        for rel, begin in (
            ("common/scripted_effects/EGY_political_leaders.txt", "# MDCW HP EGY MANUAL SUCCESSORS BEGIN"),
            ("common/scripted_effects/SOV_political_leaders.txt", "# MDCW HP SOV CIVILIAN SUCCESSOR BEGIN"),
        ):
            text = self.read(rel) or ""
            if begin not in text:
                self.issue("manual_successor_provider", f"Missing manual-successor provider marker in {rel}")
            elif "check_variable = { MDCW_HP_native_retirement = 1 }" not in text:
                self.issue("manual_successor_context", f"{rel} provider must require the temporary manual-retirement context")
            elif "has_country_flag = MDCW_HP_native_retirement" in text or "has_global_flag = MDCW_HP_native_retirement" in text:
                self.issue("manual_successor_context", f"{rel} must not use a persistent flag as the manual-retirement context")

    def _special_portrait_catalogue(self):
        candidates = [self.stage.parent.parent / "existing_special_portraits.json",
                      self.root / "tools/historical_politics_1970/special_portraits.json"]
        for path in candidates:
            if path.is_file():
                try:
                    return json.loads(path.read_text(encoding="utf-8-sig"))
                except (OSError, json.JSONDecodeError):
                    self.issue("special_portrait_catalogue", "Cannot read special portrait approval catalogue")
                    return {}
        return {}

    def _approved_special_portrait(self, tag, person):
        manifest = self.manifest if isinstance(self.manifest, dict) else {}
        keys = [f"{tag}_{person.get('id', '')}"]
        native_name = person.get("native_name") or person.get("name", "")
        keys.append(f"{tag}_{re.sub(r'[^a-z0-9]+', '_', self._identity_name_key(native_name))}")
        for key in dict.fromkeys(keys):
            record = manifest.get(key)
            if not isinstance(record, dict):
                continue
            status = record.get("status")
            provenance = record.get("provenance")
            accepted = status in {"visually_reviewed", "edited_visually_reviewed", "original_historical_user_approved", "reviewed", "approved", "existing_exact_name_md_reference"} or (status is None and provenance == "existing exact-name MD reference")
            path = record.get("portrait") or record.get("path")
            if not accepted or not isinstance(path, str) or not path:
                continue
            relative = Path(path.replace("\\", "/"))
            if relative.is_absolute() or ".." in relative.parts:
                continue
            if (self.stage / relative).is_file() or (self.root / relative).is_file():
                return relative.as_posix()
        return None

    @staticmethod
    def _ideology_family(ideology):
        mapping = {
            "western_autocracy": 0, "conservatism": 1, "liberalism": 2, "socialism": 3,
            "communist_state": 4, "anarchist_communism": 5, "conservative": 6, "autocracy": 7,
            "mod_vilayat_e_faqih": 8, "vilayat_e_faqih": 9, "kingdom": 10, "caliphate": 11,
            "neutral_muslim_brotherhood": 12, "neutral_autocracy": 13, "neutral_conservatism": 14,
            "oligarchism": 15, "neutral_libertarian": 16, "neutral_green": 17, "neutral_social": 18,
            "neutral_communism": 19, "nat_populism": 20, "nat_fascism": 21, "nat_autocracy": 22,
            "monarchist": 23,
        }
        return mapping.get(str(ideology).casefold())

    def check_special_successor_pools(self):
        """Verify USA/SPR successor pools against reviewed identities and MD native order."""
        effect_path = "common/scripted_effects/mdcw_historical_special_successors.txt"
        effects = self.read(effect_path) or ""
        catalogue = self._special_portrait_catalogue()
        curated = {country.get("tag"): country.get("leaders", []) for country in catalogue.get("countries", [])}
        expected = {}
        for tag in ("USA", "SPR"):
            native_sources = ([
                ("common/scripted_effects/USA_1970_scripted_effects.txt", "USA_1970_set_scenario_leader"),
            ] if tag == "USA" else [
                ("common/scripted_effects/COLDWAR_SPR_politics.txt", "COLDWAR_SPR_set_scenario_leader"),
                ("common/scripted_effects/SPR_political_leaders.txt", "set_leader_SPR"),
            ])
            native_candidates = []
            for source, function in native_sources:
                text = self.read(source, stage=False) or ""
                function_body = self._field_block(text, function) or ""
                for key, _, opening, end in self._parse_blocks(function_body):
                    if key != "create_country_leader":
                        continue
                    body = function_body[opening + 1:end - 1]
                    names = [value for _, value in self._quoted_fields(body, "name")]
                    ideologies = [value for _, value in self._scalar_fields(body, "ideology")]
                    if len(names) == 1 and len(ideologies) == 1:
                        family = self._ideology_family(ideologies[0])
                        if family is not None:
                            native_candidates.append((family, names[0]))
            unique_native = {}
            for family, name in native_candidates:
                unique_native.setdefault((family, self._identity_name_key(name)), name)
            expected[tag] = {}
            person_rows = list(curated.get(tag, []))
            person_rows += [person for (person_tag, _), person in self.people.items() if person_tag == tag]
            for (family, name_key), native_name in unique_native.items():
                matches = [person for person in person_rows
                           if self._identity_name_key(person.get("native_name") or person.get("name", "")) == name_key]
                portrait = None
                for person in matches:
                    if person in curated.get(tag, []):
                        portrait = self._approved_special_portrait(tag, person)
                    else:
                        portrait = self._portrait(tag, person)
                    if portrait:
                        break
                if portrait:
                    expected[tag].setdefault(family, []).append((len(expected[tag].get(family, [])), native_name, portrait))
        actual = defaultdict(list)
        for key, _, opening, end in self._parse_blocks(effects):
            match = re.fullmatch(r"MDCW_HP_special_retire_(USA|SPR)_(\d+)", key or "")
            if not match:
                continue
            tag, family = match.group(1), int(match.group(2))
            body = effects[opening + 1:end - 1]
            all_blocks = list(self._parse_blocks(body))
            branches = [(key, block_open, block_end) for key, _, block_open, block_end in all_blocks if key in {"if", "else_if", "else"}]
            for candidate, _, candidate_open, candidate_end in all_blocks:
                if candidate != "create_country_leader":
                    continue
                containers = [(branch, branch_open, branch_end) for branch, branch_open, branch_end in branches
                              if branch_open < candidate_open and branch_end > candidate_end]
                nearest = min(containers, key=lambda item: item[2] - item[1]) if containers else None
                if nearest and nearest[0] == "else":
                    continue  # circular default repeats slot 0; it is not a separate member
                block = body[candidate_open + 1:candidate_end - 1]
                names = [value for _, value in self._quoted_fields(block, "name")]
                pictures = [value.replace("\\", "/") for _, value in self._quoted_fields(block, "picture")]
                ideologies = [value for _, value in self._scalar_fields(block, "ideology")]
                if len(names) != 1 or len(pictures) != 1 or len(ideologies) != 1:
                    self.issue("special_successor_shape", f"{key} candidate must define one name, picture, and ideology")
                    continue
                actual[tag, family].append((names[0], pictures[0], ideologies[0]))
            if re.search(r"(?m)^\s*date\s*[<>]=?\s*", body):
                self.issue("special_successor_date_gate", f"{key} gates an always-available historical successor by date")
            if re.search(r"set_popularity|set_politics|set_government|set_ruling_party", body):
                self.issue("special_successor_government_change", f"{key} changes government or party popularity")
        expected_keys = {(tag, int(family)) for tag, groups in expected.items() for family, rows in groups.items() if rows}
        actual_keys = set(actual)
        if expected_keys != actual_keys:
            self.issue("special_successor_coverage", "USA/SPR pools do not cover exactly the portrait-approved identities in their native families",
                       missing=sorted(f"{tag}/{family}" for tag, family in expected_keys - actual_keys),
                       extra=sorted(f"{tag}/{family}" for tag, family in actual_keys - expected_keys))
        for tag, groups in expected.items():
            for family, rows in groups.items():
                observed = actual.get((tag, int(family)), [])
                wanted = [(name, portrait) for _, name, portrait in rows]
                got = [(name, portrait) for name, portrait, _ in observed]
                if wanted != got:
                    self.issue("special_successor_members", f"{tag}/{family} successor identities, portraits, or native order differ from reviewed source data",
                               expected=wanted, actual=got)
        if "MDCW_HP_sync_special_counter" not in effects or "MDCW_HP_has_special_successor_pool" not in (self.read("common/scripted_triggers/mdcw_historical_special_successors.txt") or ""):
            self.issue("special_successor_helpers", "USA/SPR counter sync helper or availability trigger is missing")

    def check_sov_egy_successors(self):
        effects = self.read("common/scripted_effects/mdcw_historical_sov_egy_successors.txt") or ""
        triggers = self.read("common/scripted_triggers/mdcw_historical_sov_egy_successors.txt") or ""
        if not effects or not triggers:
            self.issue("sov_egy_successor_outputs", "SOV/EGY successor effect and trigger outputs are required")
            return
        for helper in ("MDCW_HP_SOV_native_retirement", "MDCW_HP_SOV_clear_manual_retirement_request",
                       "MDCW_HP_SOV_clear_manual_retirement_pending", "MDCW_HP_sync_sov_egy_counter",
                       "MDCW_HP_set_egy_manual_leader"):
            if self._field_block(effects, helper) is None:
                self.issue("sov_egy_successor_helper", f"Missing generated SOV/EGY effect {helper}")
        if self._field_block(triggers, "MDCW_HP_SOV_retirement_available") is None or self._field_block(triggers, "MDCW_HP_has_sov_egy_successor_pool") is None:
            self.issue("sov_egy_successor_trigger", "SOV/EGY successor availability triggers are incomplete")
        if "check_variable = { MDCW_HP_native_retirement = 1 }" not in effects:
            self.issue("sov_egy_successor_context", "SOV/EGY manual helper must require temporary GUI context")
        if "has_country_flag = MDCW_HP_native_retirement" in effects or "set_country_flag = MDCW_HP_native_retirement" in effects:
            self.issue("sov_egy_successor_context", "SOV/EGY helper must not convert manual context into a persistent flag")
        egypt = self._field_block(effects, "MDCW_HP_set_egy_manual_leader") or ""
        for counter in ("conservatism_leader", "neutral_Social_leader"):
            if counter not in egypt:
                self.issue("egy_native_counter", f"Egypt manual successors must use the existing {counter} counter")
        if not re.search(r"has_country_flag\s*=\s*do_not_retire", egypt):
            self.issue("egy_incumbent_protection", "Egypt special selector must preserve do_not_retire behavior")
        if re.search(r"set_variable\s*=\s*\{\s*(?:MDCW_HP_)?egy_.*(?:counter|index)", effects, re.I):
            self.issue("egy_invented_counter", "Egypt successor output introduces a new counter instead of MD native counters")
        sov_provider = self.read("common/scripted_effects/SOV_political_leaders.txt") or ""
        if "MDCW_HP_set_sov_yeltsin = yes" in sov_provider:
            if "has_country_flag = do_not_retire" not in (self._field_block(effects, "MDCW_HP_set_sov_yeltsin") or ""):
                self.issue("sov_incumbent_protection", "Yeltsin native successor must preserve do_not_retire")
            if re.search(r"date\s*[<>]=?", self._field_block(effects, "MDCW_HP_set_sov_yeltsin") or ""):
                self.issue("sov_successor_date_gate", "Yeltsin successor must remain available without an individual date gate")
        for rel in ("common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt",):
            text = self.read(rel) or ""
            for begin, end in (
                ("# MDCW HP SOV PENDING CLEAR BEGIN", "# MDCW HP SOV PENDING CLEAR END"),
                ("# MDCW HP SOV VOTE RETIREMENT HANDOFF BEGIN", "# MDCW HP SOV VOTE RETIREMENT HANDOFF END"),
                ("# MDCW HP SOV DIRECT HEIR CLEAR COLDWAR_SOV_heir_takes_over_aliyev BEGIN", "# MDCW HP SOV DIRECT HEIR CLEAR COLDWAR_SOV_heir_takes_over_aliyev END"),
                ("# MDCW HP SOV DIRECT HEIR CLEAR COLDWAR_SOV_heir_takes_over_grishin BEGIN", "# MDCW HP SOV DIRECT HEIR CLEAR COLDWAR_SOV_heir_takes_over_grishin END"),
            ):
                if text.count(begin) != 1 or text.count(end) != 1:
                    self.issue("sov_retirement_marker", f"Expected one complete SOV handoff/clear marker pair: {begin}")

    @staticmethod
    def _normalize_setup_guard(text):
        old = re.compile(
            r"NOT\s*=\s*\{\s*AND\s*=\s*\{\s*OR\s*=\s*\{\s*original_tag\s*=\s*DDR\s+original_tag\s*=\s*PAK\s*\}\s*IMP_is_1970_scenario\s*=\s*yes\s*\}\s*\}"
        )
        new = "NOT = { AND = { OR = { original_tag = DDR original_tag = PAK } IMP_is_1970_scenario = yes NOT = { MDCW_HP_has_native_pool = yes } } }"
        return old.sub(new, text)

    def _restore_native_pool_setter(self, text, tag):
        begin = f"# MDCW HISTORICAL NATIVE POOL {tag} BEGIN"
        end = f"# MDCW HISTORICAL NATIVE POOL END {tag}"
        start = text.find(begin)
        finish = text.find(end, start + len(begin)) if start >= 0 else -1
        if start < 0 or finish < 0:
            return None
        wrapper = text[start:finish]
        else_match = re.search(r"\belse\s*=\s*\{", wrapper)
        if not else_match:
            return None
        opening = wrapper.find("{", else_match.start(), else_match.end())
        try:
            block_end = self._brace_end(wrapper, opening, len(wrapper))
        except ValueError:
            return None
        original_body = wrapper[opening + 1:block_end - 1]
        return text[:start] + original_body + text[finish + len(end):]

    def _restore_special_successor_setter(self, text, tag):
        begin = f"# MDCW HISTORICAL SPECIAL SUCCESSORS {tag} BEGIN"
        end = f"# MDCW HISTORICAL SPECIAL SUCCESSORS {tag} END"
        start = text.find(begin)
        finish = text.find(end, start + len(begin)) if start >= 0 else -1
        if start < 0 or finish < 0 or text.count(begin) != 1 or text.count(end) != 1:
            return None
        wrapper = text[start:finish]
        else_match = re.search(r"\belse\s*=\s*\{", wrapper)
        if not else_match:
            return None
        opening = wrapper.find("{", else_match.start(), else_match.end())
        try:
            end_offset = self._brace_end(wrapper, opening, len(wrapper))
        except ValueError:
            return None
        native = wrapper[opening + 1:end_offset - 1]
        prefix = text[:start]
        if prefix.endswith("\n"):
            prefix = prefix[:-1]
        suffix = text[finish + len(end):]
        if suffix.startswith("\n"):
            suffix = suffix[1:]
        return prefix + native + suffix

    def _restore_egy_successor_setter(self, text):
        begin = "# MDCW HP EGY MANUAL SUCCESSORS BEGIN"
        end = "# MDCW HP EGY MANUAL SUCCESSORS END"
        if text.count(begin) != 1 or text.count(end) != 1:
            return None
        pattern = re.compile(r"(?ms)^([ \t]*)" + re.escape(begin) + r"\n(.*?)^[ \t]*" + re.escape(end) + r"\s*$")
        match = pattern.search(text)
        if not match:
            return None
        native_branch = re.search(r"(?m)^([ \t]*)else\s*=\s*\{\s*COLDWAR_EGY_set_party_leader_1970\s*=\s*yes\s*\}", match.group(2))
        if not native_branch:
            return None
        replacement = native_branch.group(1) + "COLDWAR_EGY_set_party_leader_1970 = yes"
        return text[:match.start()] + replacement + text[match.end():]

    def _restore_native_retirement_context(self, text):
        begin = "# MDCW NATIVE RETIREMENT CONTEXT BEGIN"
        end = "# MDCW NATIVE RETIREMENT CONTEXT END"
        if text.count(begin) != 1 or text.count(end) != 1:
            return text
        pattern = re.compile(r"(?ms)^([ \t]*)" + re.escape(begin) + r"\n.*?^\1" + re.escape(end) + r"\n?")
        return pattern.sub(lambda match: match.group(1) + "set_leader = yes\n", text)

    def _restore_sov_retirement_patches(self, text):
        regions = [
            ("# MDCW HP SOV PENDING CLEAR BEGIN", "# MDCW HP SOV PENDING CLEAR END"),
            ("# MDCW HP SOV VOTE RETIREMENT HANDOFF BEGIN", "# MDCW HP SOV VOTE RETIREMENT HANDOFF END"),
            ("# MDCW HP SOV DIRECT HEIR CLEAR COLDWAR_SOV_heir_takes_over_aliyev BEGIN", "# MDCW HP SOV DIRECT HEIR CLEAR COLDWAR_SOV_heir_takes_over_aliyev END"),
            ("# MDCW HP SOV DIRECT HEIR CLEAR COLDWAR_SOV_heir_takes_over_grishin BEGIN", "# MDCW HP SOV DIRECT HEIR CLEAR COLDWAR_SOV_heir_takes_over_grishin END"),
        ]
        restored = text
        for begin, end in regions:
            # Require paired, single markers. This rejects partial/incomplete staged patches.
            if restored.count(begin) != restored.count(end):
                return None
            if restored.count(begin) > 1:
                return None
            if restored.count(begin) == 1:
                restored = self._strip_marker_region(restored, begin, end)
        return restored

    @staticmethod
    def _normalized(text):
        return text.replace("\r\n", "\n").rstrip() + "\n"

    @staticmethod
    def _normalized_script(text):
        return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").splitlines() if line.strip()) + "\n"

    @staticmethod
    def _strip_marker_region(text, begin, end):
        pattern = re.compile(r"(?ms)^[ \t]*" + re.escape(begin) + r"\n.*?^[ \t]*" + re.escape(end) + r"\n?")
        return pattern.sub("", text)

    @staticmethod
    def _marked_region(text, begin, end):
        pattern = re.compile(r"(?ms)^[ \t]*" + re.escape(begin) + r"[ \t]*\n(.*?)^[ \t]*" + re.escape(end) + r"[ \t]*(?:\})?[ \t]*$")
        matches = list(pattern.finditer(text))
        return matches[0].group(1) if len(matches) == 1 else None

    @staticmethod
    def _restore_retire_wrapper(text):
        pattern = re.compile(r"(?ms)^[ \t]*" + re.escape(RETIRE_BEGIN) + r"\n.*?^[ \t]*" + re.escape(RETIRE_END) + r"\n?")
        def restore(match):
            setter = re.search(r"(?m)^([ \t]*)set_leader = yes\s*$", match.group(0))
            if not setter:
                return ""
            return setter.group(1) + "set_leader = yes\n"
        return pattern.subn(restore, text)

    def _mask_native_pictures(self, rel, text, functions):
        edits = []
        for func, names in functions.items():
            fn_blocks = [(opening, end) for key, _, opening, end in self._parse_blocks(text) if key == func]
            if len(fn_blocks) != 1:
                return None
            opening, fn_end = fn_blocks[0]
            for leader_key, _, leader_open, leader_end in self._parse_blocks(text, opening + 1, fn_end - 1):
                if leader_key != "create_country_leader":
                    continue
                body_start, body_end = leader_open + 1, leader_end - 1
                body = text[body_start:body_end]
                actual_names = [name for _, name in self._quoted_fields(body, "name")]
                name_matches = len(actual_names) == 1 and any(
                    actual_names[0] == name or self._normalized_person_name(actual_names[0]) == self._normalized_person_name(name)
                    for name in names
                )
                if not name_matches:
                    continue
                for match, _ in self._quoted_fields(body, "picture"):
                    local_start = body.rfind("picture", 0, match.start(1))
                    local_end = match.end(1) + 1  # include the closing quote
                    while local_start > 0 and body[local_start - 1].isspace():
                        local_start -= 1
                    edits.append((body_start + local_start, body_start + local_end, ""))
        for start, end, value in sorted(edits, reverse=True):
            text = text[:start] + value + text[end:]
        return text

    def check_assets(self):
        for rel in GENERATED_FILES:
            if not (self.stage / rel).is_file():
                self.issue("missing_generated_file", f"Required generated file is absent from stage: {rel}")
        # Portrait references in the native pool must resolve to installed or
        # staged assets, including portraits reused from MD's existing pool.
        seen = set()
        for rel in (NATIVE_POOL_EFFECT_FILE,
                    "common/scripted_effects/mdcw_historical_special_successors.txt",
                    "common/scripted_effects/mdcw_historical_sov_egy_successors.txt"):
            effect = self.read(rel) or ""
            for _, path in self._quoted_fields(effect, "picture"):
                path = path.replace("\\", "/")
                if path in seen:
                    continue
                seen.add(path)
                if not ((self.stage / path).is_file() or (self.root / path).is_file()):
                    self.issue("missing_portrait_asset", f"Generated portrait path does not resolve: {path}", source=rel)
        # A bespoke EGY appointment can already have a reviewed native portrait
        # even when it has no generic decision portrait. Count that only when
        # the referenced source function contains the exact person and the
        # picture resolves to a local asset.
        self.egypt_pending = []
        egypt = next((c for c in self.countries if c.get("tag") == "EGY"), None)
        if egypt:
            for person in egypt.get("leaders", []):
                if self._portrait("EGY", person) or self._has_native_portrait(person):
                    continue
                self.egypt_pending.append({"tag": "EGY", "id": person.get("id"), "name": person.get("name"),
                                           "reason": "no reviewed generic portrait or exact native-source portrait"})
        self.check_native_portrait_pending()
        self.check_party_icon_registry()
        self.check_native_portrait_assets()

    def check_native_portrait_pending(self):
        self.pending_native_portraits = []
        special_path = self.stage.parent.parent / "existing_special_portraits.json"
        if not special_path.is_file():
            special_path = self.root / "tools/historical_politics_1970/special_portraits.json"
        if not special_path.is_file():
            return
        try:
            payload = json.loads(special_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            self.issue("special_portrait_catalogue", "Cannot read reviewed native portrait catalogue")
            return
        for country in payload.get("countries", []):
            tag = country.get("tag")
            for person in country.get("leaders", []):
                if not person.get("native_sources"):
                    continue
                value = person.get("portrait")
                record = self.manifest.get(f"{tag}_{person.get('id', '')}") if isinstance(self.manifest, dict) else None
                if not value and isinstance(record, dict):
                    status = record.get("status")
                    provenance = record.get("provenance")
                    if status in {"visually_reviewed", "edited_visually_reviewed", "original_historical_user_approved", "reviewed", "approved"} or provenance == "existing exact-name MD reference":
                        value = record.get("portrait")
                path = Path(str(value).replace("\\", "/")) if value else None
                if path and not path.is_absolute() and ".." not in path.parts and ((self.stage / path).is_file() or (self.root / path).is_file()):
                    continue
                self.pending_native_portraits.append({"tag": tag, "id": person.get("id"), "name": person.get("name"),
                                                      "reason": "no reviewed exact-person native portrait"})

    def check_native_portrait_assets(self):
        sources = defaultdict(lambda: defaultdict(set))
        catalogs = [self.catalogue_path]
        special_paths = [self.stage.parent.parent / "existing_special_portraits.json",
                         self.root / "tools/historical_politics_1970/special_portraits.json"]
        for path in special_paths:
            if path.is_file():
                catalogs.append(path)
                break
        for path in catalogs:
            try:
                value = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                continue
            countries = value.get("countries", []) if isinstance(value, dict) else []
            for country in countries:
                for person in country.get("leaders", []):
                    for ref in person.get("native_sources", []):
                        if isinstance(ref, str) and "#" in ref:
                            source, function = ref.rsplit("#", 1)
                            sources[source.replace("\\", "/")][function].add(person.get("native_name", person.get("name", "")))
        for source, functions in sources.items():
            text = self.read(source, stage=True) or self.read(source, stage=False)
            if not text:
                continue
            for function, names in functions.items():
                fn_blocks = [(opening, end) for key, _, opening, end in self._parse_blocks(text) if key == function]
                if len(fn_blocks) != 1:
                    continue
                start, end = fn_blocks[0]
                for key, _, opening, block_end in self._parse_blocks(text, start + 1, end - 1):
                    if key != "create_country_leader":
                        continue
                    body = text[opening + 1:block_end - 1]
                    actual_names = [name for _, name in self._quoted_fields(body, "name")]
                    name_matches = len(actual_names) == 1 and any(
                        actual_names[0] == name or self._normalized_person_name(actual_names[0]) == self._normalized_person_name(name)
                        for name in names
                    )
                    if not name_matches:
                        continue
                    for _, portrait in self._quoted_fields(body, "picture"):
                        normalized = portrait.replace("\\", "/")
                        path = Path(normalized)
                        if path.is_absolute() or ".." in path.parts or not ((self.stage / path).is_file() or (self.root / path).is_file()):
                            self.issue("missing_native_portrait_asset", f"Native leader portrait path does not resolve: {normalized}", source=source, function=function, name=actual_names[0] if actual_names else "")

    def check_party_icon_registry(self):
        manifest_path = self.root / "tools/historical_politics_1970/party_icon_manifest.json"
        if not manifest_path.is_file():
            self.issue("missing_party_icon_manifest", "Party icon manifest is missing from the builder inputs")
            return
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        gfx = self.read("interface/mdcw_historical_parties.gfx")
        if not gfx:
            self.issue("missing_party_icon_registry", "Generated party sprite registry is missing from the stage")
            return
        sprites = {}
        for key, _, opening, end in self._parse_blocks(gfx):
            if key != "spriteType":
                continue
            body = gfx[opening + 1:end - 1]
            names = [v for _, v in self._quoted_fields(body, "name")]
            textures = [v for _, v in self._quoted_fields(body, "texturefile")]
            if len(names) != 1 or len(textures) != 1:
                self.issue("party_sprite_block", "Each historical party sprite needs one name and one texturefile")
                continue
            if names[0] in sprites:
                self.issue("duplicate_party_sprite", f"Party sprite is defined twice: {names[0]}")
            sprites[names[0]] = textures[0].replace("\\", "/")
        for iconid, row in manifest.items():
            if not isinstance(row, dict) or row.get("install_action") != "add_staged":
                continue
            sprite = row.get("sprite")
            expected_sprite = "GFX_" + iconid
            if sprite != expected_sprite:
                self.issue("party_sprite_prefix", f"{iconid} must register as exactly {expected_sprite}", sprite=sprite)
            text_icon = row.get("text_icon", "")
            if text_icon != "£" + iconid or text_icon.startswith("£GFX_"):
                self.issue("party_text_icon_prefix", f"{iconid} text icon must use the icon id without a GFX_ prefix", text_icon=text_icon)
            texture = sprites.get(expected_sprite)
            if not texture:
                self.issue("missing_party_sprite", f"No GFX registry entry for {expected_sprite}")
                continue
            candidates = [self.stage / texture, self.root / texture]
            asset = next((p for p in candidates if p.is_file()), None)
            if asset is None:
                self.issue("missing_party_texture", f"Party icon texture does not resolve: {texture}", icon=iconid)
                continue
            try:
                with asset.open("rb") as stream:
                    header = stream.read(20)
                if len(header) < 20 or header[:4] != b"DDS ":
                    raise ValueError("not a DDS file")
                height = int.from_bytes(header[12:16], "little")
                width = int.from_bytes(header[16:20], "little")
                if (width, height) != (22, 22):
                    self.issue("party_texture_dimensions", f"Expected 22x22 party DDS, found {width}x{height}: {texture}", icon=iconid)
            except OSError as exc:
                self.issue("party_texture_read", f"Cannot read party texture {texture}: {exc}", icon=iconid)
            except ValueError as exc:
                self.issue("party_texture_format", f"Invalid party texture {texture}: {exc}", icon=iconid)
        expected = {row.get("sprite") for row in manifest.values()
                    if isinstance(row, dict) and row.get("install_action") == "add_staged"}
        extras = sorted(set(sprites) - expected)
        if extras:
            self.issue("unmanifested_party_sprites", "GFX registry contains sprite IDs absent from the reviewed icon manifest", sprites=extras)
        self.party_icon_count = len(expected)
        self.party_icon_texture_count = sum(1 for s in expected if s in sprites and ((self.stage / sprites[s]).is_file() or (self.root / sprites[s]).is_file()))

    def _has_native_portrait(self, person):
        native_name = person.get("native_name", person.get("name", ""))
        for ref in person.get("native_sources", []):
            if not isinstance(ref, str) or "#" not in ref:
                continue
            rel, function = ref.rsplit("#", 1)
            text = self.read(rel.replace("\\", "/"), stage=False)
            if not text:
                continue
            fn = [(opening, end) for key, _, opening, end in self._parse_blocks(text) if key == function]
            if len(fn) != 1:
                continue
            start, end = fn[0]
            for key, _, opening, block_end in self._parse_blocks(text, start + 1, end - 1):
                if key != "create_country_leader":
                    continue
                body = text[opening + 1:block_end - 1]
                names = [name for _, name in self._quoted_fields(body, "name")]
                if names != [native_name]:
                    continue
                for _, portrait in self._quoted_fields(body, "picture"):
                    path = Path(portrait.replace("\\", "/"))
                    if not path.is_absolute() and ".." not in path.parts and ((self.stage / path).is_file() or (self.root / path).is_file()):
                        return True
        return False

    def run(self):
        self.check_coverage()
        self.check_party_localisation()
        self.check_native_pools()
        self.check_native_retirement_wiring()
        self.check_special_successor_pools()
        self.check_sov_egy_successors()
        self.check_assets()
        self.check_native_file_deltas()
        pools = self.expected_native_pools()
        ready_records = {(tag, row["catalogue_id"]) for (tag, _), rows in pools.items() for row in rows}
        ready_people = {(tag, str(row["name"]).casefold()) for (tag, _), rows in pools.items() for row in rows}
        ready_periods = sum(
            1 for (tag, ident), person in self.candidates.items()
            if tag not in SPECIAL and not person.get("managed_by_existing_system") and self._portrait(tag, person)
        )
        catalogue_rows = [(country.get("tag"), person) for country in self.countries for person in country.get("leaders", [])]
        return {
            "ok": not any(x["severity"] == "error" for x in self.issues),
            "catalogue_countries": len(self.countries),
            "catalogue_leaders": sum(len(c.get("leaders", [])) for c in self.countries),
            "catalogue_leader_records": sum(len(c.get("leaders", [])) for c in self.countries),
            "catalogue_person_records": len(catalogue_rows),
            "catalogue_people": len({(tag, str(person.get("name", "")).casefold()) for tag, person in catalogue_rows}),
            "catalogue_unique_named_people": len({(tag, str(person.get("name", "")).casefold()) for tag, person in catalogue_rows}),
            "candidate_periods": len(self.candidates),
            "catalogue_party_rows": sum(len(c.get("parties", [])) for c in self.countries),
            "native_pool_families": len(pools),
            "ready_candidate_periods": ready_periods,
            "ready_pool_entries": sum(len(rows) for rows in pools.values()),
            "ready_catalogue_records": len(ready_records),
            "ready_unique_people": len(ready_people),
            "pending_unique_people": len(self.pending),
            "pending_catalogue_records": len(self.pending),
            "changed_shared_files": getattr(self, "changed_shared", []),
            "timeline_samples": getattr(self, "timeline", {}),
            "pending_portraits": self.pending,
            "pending_native_portraits": getattr(self, "pending_native_portraits", []),
            "egypt_portrait_pending": getattr(self, "egypt_pending", []),
            "party_icon_registry_entries": getattr(self, "party_icon_count", 0),
            "party_icon_textures_present": getattr(self, "party_icon_texture_count", 0),
            "issues": self.issues,
        }


def validate(stage, catalogue, manifest=None, root=ROOT):
    """Return a JSON-serializable QA report for the staged tree."""
    return Validator(Path(root), Path(stage), Path(catalogue), manifest).run()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--catalogue", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = validate(args.stage, args.catalogue, args.manifest, args.root)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    # Keep JSON output readable and valid even in Windows consoles whose code
    # page cannot encode the historical names in the catalogue.
    print(output.encode("ascii", errors="backslashreplace").decode("ascii"))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
