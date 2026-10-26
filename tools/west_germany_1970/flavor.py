# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Millennium Dawn-style flavor texts for the focus tree.

The modules define each focus with a short working description; the full flavor texts live in the
flv_*.py dictionaries and replace them here, after every module has registered its focuses.
"""
import tree
import flv_chancellery1, flv_chancellery2, flv_economy, flv_security, flv_west, flv_dp, flv_civil

FLAVOR = {}
for _m in (flv_chancellery1, flv_chancellery2, flv_economy, flv_security, flv_west, flv_dp, flv_civil):
    FLAVOR.update(_m.D)

_unknown = [k for k in FLAVOR if k not in tree.BY_KEY]
if _unknown:
    raise ValueError("flavor text for unknown focus: " + ", ".join(_unknown))
for _k, _d in FLAVOR.items():
    tree.BY_KEY[_k]["desc"] = _d
