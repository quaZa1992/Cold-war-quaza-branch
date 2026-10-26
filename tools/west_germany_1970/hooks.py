# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Connects focus rewards to systems that already exist in the mod.

Kept in one place so the links are easy to review:
* MD/EU europeanism (europeanism_change) for the European focuses,
* the Soviet 1970 tree (treaty partner opinion, improved trade agreement, Helsinki signatures),
* MD trade agreements, MD protests and MD corruption.
"""
from cw_lib import P, J, europe, protest, corruption, tt
from tree import FOCUSES

SOV_TREATY = ("if = { limit = { country_exists = SOV } "
              "add_opinion_modifier = { target = SOV modifier = COLDWAR_SOV_treaty_partner } "
              "reverse_add_opinion_modifier = { target = SOV modifier = COLDWAR_SOV_treaty_partner } "
              "set_temp_variable = { receiver_nation = SOV.id } set_temp_variable = { sender_nation = ROOT.id } "
              "set_improved_trade_agreement = yes }")
HELSINKI = ("if = { limit = { country_exists = SOV } "
            "add_opinion_modifier = { target = SOV modifier = COLDWAR_SOV_detente_partner } "
            "reverse_add_opinion_modifier = { target = SOV modifier = COLDWAR_SOV_detente_partner } } "
            "add_to_variable = { global.COLDWAR_SOV_helsinki_signatures = 1 }")

EXTRA = {
    # Europe
    "ems": europe(5),
    "ec_enlargement": europe(5),
    "single_market": europe(8),
    "schengen": europe(5),
    "maastricht": europe(10),
    "euro_founder": J(europe(10), tt(f"{P}_tt_euro_join", "From 1999 the D-Mark is replaced by the §Yeuro§! (MD currency system).")),
    "dmark_bloc": europe(-10),
    # the Soviet tree sees the same treaties
    "moscow_treaty": J(SOV_TREATY, tt(f"{P}_tt_sov_treaty", "The Soviet Union counts the Federal Republic as a §Ytreaty partner§! and an improved trade agreement is signed.")),
    "helsinki": J(HELSINKI, tt(f"{P}_tt_helsinki_sig", "The Federal Republic's signature counts towards the Soviet §YHelsinki§! process.")),
    # protests
    "double_track": protest(10),
    "deployment_vote": protest(15),
    "no_deployment": protest(-10),
    "nuclear_moratorium": protest(-8),
    "atomkonsens": protest(-6),
    "asylum_compromise": protest(5),
    # corruption
    "arms_export_guidelines": corruption(False),
}


def apply():
    keys = {f["key"]: f for f in FOCUSES}
    for k, eff in EXTRA.items():
        if k not in keys:
            raise KeyError("hooks.py: unknown focus " + k)
        keys[k]["reward"] = J(keys[k]["reward"], eff)
