# IMPERIA COLD WAR — Chile 1970 static cost overlay checks.
"""Focused checks for the cost overlay and its approved-design invariants."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import unittest

try:
    from .cost_revision import apply_costs
except ImportError:
    from cost_revision import apply_costs


HERE = Path(__file__).parent


def _non_cost_projection(value):
    if isinstance(value, dict):
        return {
            key: _non_cost_projection(item)
            for key, item in value.items()
            if key not in {"money", "weekly", "setup"}
        }
    if isinstance(value, list):
        return [_non_cost_projection(item) for item in value]
    return value


def _pairs(original, revised, fields, path="root"):
    for field in fields:
        if field in original:
            yield f"{path}.{field}", original[field], revised[field]


def monetary_pairs(data, path="root"):
    for node in data.get("nodes", []):
        yield from _pairs(node, node, ("money", "weekly"), f"nodes[{node.get('key', '?')}]" )
    for agreement in data.get("agreements", []):
        for side in ("chile", "recipient"):
            item = agreement.get(side)
            if item:
                yield from _pairs(item, item, ("setup", "weekly"), f"agreements[{agreement.get('id', '?')}].{side}")
    for event in data.get("events", []):
        for index, option in enumerate(event.get("options", [])):
            yield from _pairs(option, option, ("money", "weekly"), f"events[{event.get('id', '?')}].options[{index}]")
    for contract in data.get("decision_contracts", []):
        yield from _pairs(contract, contract, ("money", "weekly"), f"decision_contracts[{contract.get('id', '?')}]" )


def _collect_pairs(original, revised):
    result = []
    for records in (
        ((item, f"nodes[{item.get('key', '?')}]", ("money", "weekly")) for item in original.get("nodes", [])),
        ((item, f"agreements[{item.get('id', '?')}].{side}", ("setup", "weekly")) for item in original.get("agreements", []) for side in ("chile", "recipient") if item.get(side)),
        ((option, f"events[{event.get('id', '?')}].options[{index}]", ("money", "weekly")) for event in original.get("events", []) for index, option in enumerate(event.get("options", []))),
        ((item, f"decision_contracts[{item.get('id', '?')}]", ("money", "weekly")) for item in original.get("decision_contracts", [])),
    ):
        for source, path, fields in records:
            for field in fields:
                if field in source:
                    updated = _lookup(revised, path, field)
                    result.append((f"{path}.{field}", source[field], updated))
    return result


def _lookup(data, path, field):
    # Resolve records through stable array IDs/keys without mutating either source.
    if path.startswith("nodes["):
        token = path[6:-1]
        row = next(row for row in data["nodes"] if row.get("key") == token)
    elif path.startswith("agreements["):
        token, side = path[11:].split("].")
        row = next(row for row in data["agreements"] if row.get("id") == token)[side]
    elif path.startswith("events["):
        token, option_part = path[7:-1].split("].options[")
        row = data["events"][next(i for i, event in enumerate(data["events"]) if event.get("id") == token)]["options"][int(option_part)]
    else:
        token = path[len("decision_contracts["):-1]
        row = next(row for row in data["decision_contracts"] if row.get("id") == token)
    return row[field]


class CostRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (HERE / "approved_design.json").open("r", encoding="utf-8") as stream:
            cls.approved = json.load(stream)
        cls.adjusted = apply_costs(cls.approved)

    def test_returns_copy_and_preserves_approved_input(self):
        before = deepcopy(self.approved)
        adjusted = apply_costs(self.approved)
        self.assertIsNot(adjusted, self.approved)
        self.assertEqual(self.approved, before)

    def test_all_cost_fields_use_half_up_factor_and_five_decimal_precision(self):
        pairs = _collect_pairs(self.approved, self.adjusted)
        self.assertGreater(len(pairs), 0)
        for path, source, revised in pairs:
            expected = (Decimal(str(source)) * Decimal("0.05")).quantize(Decimal("0.00001"), rounding="ROUND_HALF_UP")
            self.assertEqual(Decimal(str(revised)), expected, path)
            self.assertGreaterEqual(revised, 0, path)
            self.assertLessEqual(max(0, -Decimal(str(revised)).as_tuple().exponent), 5, path)

    def test_only_monetary_fields_change(self):
        self.assertEqual(_non_cost_projection(self.approved), _non_cost_projection(self.adjusted))

    def test_zero_costs_remain_zero(self):
        zeros = [revised for _, original, revised in _collect_pairs(self.approved, self.adjusted) if Decimal(str(original)) == 0]
        self.assertTrue(zeros)
        self.assertTrue(all(value == 0 for value in zeros))

    def test_half_up_boundary(self):
        synthetic = {"nodes": [{"key": "rounding", "money": 0.0005, "weekly": 0.0005}]}
        result = apply_costs(synthetic)
        self.assertEqual(result["nodes"][0]["money"], 0.00003)
        self.assertEqual(result["nodes"][0]["weekly"], 0.00003)

    def test_rejects_negative_or_non_numeric_costs(self):
        for value, exception in ((-1, ValueError), (float("nan"), ValueError), ("1", TypeError), (True, TypeError)):
            with self.subTest(value=value):
                with self.assertRaises(exception):
                    apply_costs({"nodes": [{"key": "invalid", "money": value}]})


if __name__ == "__main__":
    unittest.main()
