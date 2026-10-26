# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Apply the four small integration edits to existing mod files (idempotent).

    python3 apply.py <mod_root_in> <mod_root_out>
"""
import os
import sys

EDITS = {
    "history/countries/GER - Germany.txt": [
        ("\t\tload_focus_tree = mdcw_1970_generic_focus\n", "\t\tload_focus_tree = COLDWAR_GER_1970_focus\n"),
    ],
    "common/scripted_effects/mdcw_1970_focus_tree_effects.txt": [
        ("\t\t\t\t\tAND = { original_tag = GRE IMP_is_1970_scenario = yes } # COLDWAR_GRE_1970_focus\n",
         "\t\t\t\t\tAND = { original_tag = GRE IMP_is_1970_scenario = yes } # COLDWAR_GRE_1970_focus\n"
         "\t\t\t\t\tAND = { original_tag = GER IMP_is_1970_scenario = yes } # COLDWAR_GER_1970_focus\n"),
    ],
    "common/scripted_effects/00_leader_setup_scripted_effects.txt": [
        ("\telse_if = {\n\t\tlimit = { original_tag = GRE IMP_is_1970_scenario = yes }\n\t\tCOLDWAR_GRE_1970_set_leader = yes\n\t}\n",
         "\telse_if = {\n\t\tlimit = { original_tag = GRE IMP_is_1970_scenario = yes }\n\t\tCOLDWAR_GRE_1970_set_leader = yes\n\t}\n"
         "\t# IMPERIA CW — Cold War: West Germany party-specific chancellors.\n"
         "\telse_if = {\n\t\tlimit = { original_tag = GER IMP_is_1970_scenario = yes }\n\t\tCOLDWAR_GER_1970_set_leader = yes\n\t}\n"),
    ],
    "common/decisions/categories/99_GER_decision_categories.txt": [
        ("\tvisible = { NOT = { has_completed_focus = GER_bringing_germany_closer_together } }\n",
         "\tvisible = { NOT = { has_completed_focus = GER_bringing_germany_closer_together } NOT = { IMP_is_1970_scenario = yes } }\n"),
        ("\tvisible = { NOT = { has_country_flag = GER_bavaria_gone } }\n",
         "\tvisible = { NOT = { has_country_flag = GER_bavaria_gone } NOT = { IMP_is_1970_scenario = yes } }\n"),
    ],
}
MARK = "COLDWAR_GER_1970"


def main(src, dst):
    for rel, edits in EDITS.items():
        raw = open(os.path.join(src, rel), "rb").read()
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        crlf = "\r\n" in text
        text = text.replace("\r\n", "\n")
        for old, new in edits:
            if new in text:
                continue  # already applied
            if text.count(old) != 1:
                raise SystemExit(f"{rel}: anchor found {text.count(old)} times: {old!r}")
            text = text.replace(old, new)
        if crlf:
            text = text.replace("\n", "\r\n")
        out = os.path.join(dst, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "wb").write(text.encode("utf-8"))
        print(rel, "bom" if bom else "", "crlf" if crlf else "lf")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
