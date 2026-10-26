# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Expand one canonical person into bounded, dated MD-family affiliations."""
from __future__ import annotations

import re
from datetime import date


def _day(value: str, label: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a YYYY.M.D string")
    try:
        return date(*map(int, value.split(".")))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid {label}: {value!r}") from exc


def _fmt(value: date) -> str:
    return f"{value.year}.{value.month}.{value.day}"


def expand_person(tag: str, person: dict) -> list[dict]:
    """Return dated candidate variants while retaining canonical portrait identity.

    A person's canonical availability is clipped to the 1970–2000 pool. If
    ``party_index_segments`` is present, each non-overlapping segment produces
    one candidate period. Gaps remain gaps; this is useful when a person had no
    documented named-party affiliation in part of the pool.
    """
    canonical_id = person.get("id")
    if not isinstance(canonical_id, str) or not re.fullmatch(r"[a-z0-9_]+", canonical_id):
        raise ValueError(f"Invalid canonical leader id for {tag}: {canonical_id!r}")
    lower = max(_day(person["available_from"], f"{tag}/{canonical_id} available_from"), date(1970, 1, 1))
    upper = min(_day(person["available_until"], f"{tag}/{canonical_id} available_until"), date(2001, 1, 1))
    if lower >= upper:
        raise ValueError(f"Canonical leader window is outside 1970–2000: {tag}/{canonical_id}")

    raw_segments = person.get("party_index_segments")
    if raw_segments is None:
        segments = [{
            "party_index": person["party_index"],
            "from": _fmt(lower),
            "until": _fmt(upper),
            "id": None,
        }]
    else:
        if not isinstance(raw_segments, list) or not raw_segments:
            raise ValueError(f"{tag}/{canonical_id} party_index_segments must be a nonempty list")
        segments = []
        for number, segment in enumerate(raw_segments, 1):
            if not isinstance(segment, dict):
                raise ValueError(f"{tag}/{canonical_id} segment {number} must be an object")
            index = segment.get("party_index")
            if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < 24:
                raise ValueError(f"{tag}/{canonical_id} segment {number} has invalid party_index {index!r}")
            start = _day(segment.get("from"), f"{tag}/{canonical_id} segment {number} from")
            end = _day(segment.get("until"), f"{tag}/{canonical_id} segment {number} until")
            if start >= end:
                raise ValueError(f"{tag}/{canonical_id} segment {number} has an empty/reversed window")
            start, end = max(start, lower), min(end, upper)
            if start >= end:
                raise ValueError(f"{tag}/{canonical_id} segment {number} is outside canonical availability")
            segment_id = segment.get("id", segment.get("segment_id"))
            if segment_id is not None and (not isinstance(segment_id, str) or not re.fullmatch(r"[a-z0-9_]+", segment_id)):
                raise ValueError(f"{tag}/{canonical_id} segment {number} has invalid id {segment_id!r}")
            segments.append({"party_index": index, "from": _fmt(start), "until": _fmt(end), "id": segment_id})

    segments.sort(key=lambda row: (_day(row["from"], "segment from"), _day(row["until"], "segment until")))
    previous_end = None
    for segment in segments:
        start, end = _day(segment["from"], "segment from"), _day(segment["until"], "segment until")
        if previous_end is not None and start < previous_end:
            raise ValueError(f"Overlapping party_index_segments for {tag}/{canonical_id}")
        previous_end = end

    variants = []
    identifiers = set()
    for number, segment in enumerate(segments):
        if number == 0:
            variant_id = canonical_id
        else:
            suffix = segment["id"] or f"party_{segment['party_index']}_{segment['from'].replace('.', '_')}"
            variant_id = f"{canonical_id}_{suffix}"
        if not re.fullmatch(r"[a-z0-9_]+", variant_id) or variant_id in identifiers:
            raise ValueError(f"Duplicate/invalid temporal leader id for {tag}/{canonical_id}: {variant_id!r}")
        identifiers.add(variant_id)
        variant = dict(person)
        variant.pop("party_index_segments", None)
        variant.update({
            "id": variant_id,
            "catalogue_id": canonical_id,
            "portrait_key": f"{tag}_{canonical_id}",
            "party_index": segment["party_index"],
            "available_from": segment["from"],
            "available_until": segment["until"],
        })
        variants.append(variant)
    return variants


def expand_country(country: dict) -> list[dict]:
    """Expand a country's canonical people and reject colliding variant IDs."""
    tag = country["tag"]
    result = []
    seen = set()
    for person in country.get("leaders", []):
        for variant in expand_person(tag, person):
            ident = variant["id"]
            if ident in seen:
                raise ValueError(f"Temporal leader id collision for {tag}/{ident}")
            seen.add(ident)
            result.append(variant)
    return result
