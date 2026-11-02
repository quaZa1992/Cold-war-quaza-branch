# IMPERIA COLD WAR — narrow Cuba tree, leader and migration integrations.
"""Install Cuba's narrow 1970 tree routing without rewriting country history."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORY = ROOT / "history/countries/CUB - Cuba.txt"
FALLBACK = ROOT / "common/scripted_effects/mdcw_1970_focus_tree_effects.txt"
LEADERS = ROOT / "common/scripted_effects/CUB_political_leaders.txt"
MIGRATION = ROOT / "common/scripted_effects/mdcw_diaspora_migration_effects.txt"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8-sig")
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one integration anchor in {path}, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def main() -> None:
    # IMPERIA COLD WAR — Upgrade only our existing block labels before idempotent matching.
    for path in (MIGRATION, LEADERS, HISTORY, FALLBACK):
        text=path.read_text(encoding='utf-8-sig')
        for feature in (
            'observe actual voluntary Cuban returns; no duplicate population grant.',
            'refresh the exact governing programme after either leader route.',
            'Cuba authored 1970 tree fallback routing.',
            "load Cuba's approved 1970 national programme.",
        ):
            text=text.replace('# IMPERIA '+'CW — Cold War: '+feature,'# IMPERIA COLD WAR — '+feature)
        if text!=path.read_text(encoding='utf-8-sig'):
            path.write_text(text,encoding='utf8',newline='\n')
    replace_once(
        MIGRATION,
        "     set_variable = { gw_return_last^gw_mi = gw_move_actual_k }\n",
        "     set_variable = { gw_return_last^gw_mi = gw_move_actual_k }\n"
        "     # IMPERIA COLD WAR — observe actual voluntary Cuban returns; no duplicate population grant.\n"
        "     COLDWAR_CUB_observe_voluntary_return = yes\n",
    )
    # The existing native-pool end marker had swallowed the final outer brace.
    # Keep the callback after BOTH the historical pool and modern fallback.
    leader_text = LEADERS.read_text(encoding="utf-8-sig")
    callback = "\tif = {\n\t\tlimit = { COLDWAR_CUB_is_1970 = yes }\n\t\tCOLDWAR_CUB_sync_programmes = yes\n\t}\n"
    comment = "# IMPERIA COLD WAR — refresh the exact governing programme after either leader route.\n"
    if comment not in leader_text:
        leader_text = leader_text.replace(callback, "")
        leader_text = leader_text.replace("# MDCW HISTORICAL NATIVE POOL END CUB}", "# MDCW HISTORICAL NATIVE POOL END CUB\n}")
        end = leader_text.rfind("}")
        if end < 0:
            raise RuntimeError("Missing CUB leader effect closing brace")
        leader_text = leader_text[:end]+comment+callback+leader_text[end:]
        LEADERS.write_text(leader_text, encoding="utf-8", newline="\n")
    replace_once(
        HISTORY,
        "\t\tload_focus_tree = mdcw_1970_generic_focus\n",
        "\t\tif = {\n"
        "\t\t\tlimit = { COLDWAR_CUB_is_1970 = yes }\n"
        "\t\t\tload_focus_tree = COLDWAR_CUB_1970_focus\n"
        "\t\t\tCOLDWAR_CUB_initialize = yes\n"
        "\t\t}\n"
        "\t\telse = { load_focus_tree = mdcw_1970_generic_focus }\n",
    )
    replace_once(
        FALLBACK,
        "mdcw_load_1970_fallback_tree = {\n",
        """mdcw_load_1970_fallback_tree = {
	# IMPERIA COLD WAR — Cuba authored 1970 tree fallback routing.
	if = {
		limit = {
			tag = CUB
			IMP_is_1970_scenario = yes
			NOT = { has_focus_tree = COLDWAR_CUB_1970_focus }
		}
		load_focus_tree = COLDWAR_CUB_1970_focus
		COLDWAR_CUB_initialize = yes
	}
""",
    )
    replace_once(
        FALLBACK,
        "\t\t\t\t\toriginal_tag = USA\n",
        "\t\t\t\t\tAND = { tag = CUB IMP_is_1970_scenario = yes } # COLDWAR | own 1970 tree\n"
        "\t\t\t\t\toriginal_tag = USA\n",
    )
    replace_once(
        HISTORY,
        "\t\tif = {\n\t\t\tlimit = { COLDWAR_CUB_is_1970 = yes }\n",
        "\t\t# IMPERIA COLD WAR — load Cuba's approved 1970 national programme.\n"
        "\t\tif = {\n\t\t\tlimit = { COLDWAR_CUB_is_1970 = yes }\n",
    )


if __name__ == "__main__":
    main()
