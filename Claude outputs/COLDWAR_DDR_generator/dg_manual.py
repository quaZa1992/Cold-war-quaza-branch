# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Hand-written effects of single foci (the design's "note" and "custom" lines).
import re
from dg_common import *

DYN_ORDER = ["party_state", "planned_economy", "nva", "mfs", "socialist_camp"]


def _tt(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def clean(text):
    return re.sub(r" ?\(`[^`]+`[^)]*\)", "", text).replace("`", "")


def manual(f, e, text):
    sid = short(f["id"])
    if e["k"] == "custom" and sid == "the_republic_at_twenty":
        # the five country modifiers are added at the start (COLDWAR_DDR_initialize_1970), like MD's base modifiers
        import dg_effects as E
        for g in DYN_ORDER:
            E.R.dyn.setdefault(f"{PFX}{g}_modifier", [])
        return []
    if e["k"] == "custom" and sid == "pcc_the_kingdom_of_prussia":
        LOC[f"{PFX}kingdom_of_prussia"] = "Kingdom of Prussia"
        LOC[f"{PFX}kingdom_of_prussia_DEF"] = "the Kingdom of Prussia"
        LOC[f"{PFX}kingdom_of_prussia_ADJ"] = "Prussian"
        return [_tt("kingdom_of_prussia", "The republic becomes the §YKingdom of Prussia§!: new name and flag."),
                f"hidden_effect = {{ set_cosmetic_tag = {PFX}kingdom_of_prussia }}"]
    if e["k"] == "note":
        return [_tt(f"note_{sid}", clean(text))]
    raise KeyError((f["id"], e))
