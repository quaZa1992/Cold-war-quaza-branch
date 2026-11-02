# IMPERIA COLD WAR — Bounded direct country-history profiles for the 1970 bookmark.
"""Keep all original bytes outside inserted, marked history blocks.

The token spans ignore comments and quoted braces. Every same-date block receives
the same profile, so existing duplicate date entries cannot pick a different setup.
No startup/monthly effect or gameplay provider is introduced.
"""
from pathlib import Path
import re

FEATURE = "1970 researched monetary, religious and internal-faction baseline"
BEGIN = "# IMPERIA COLD WAR — " + FEATURE + ". BEGIN"
END = "# IMPERIA COLD WAR — " + FEATURE + ". END"
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\#[^\r\n]*|[{}=]|[^\s{}=#"]+')


def date_blocks(text, date="1970.1.1"):
    tokens = [(m.group(), m.start(), m.end()) for m in TOKEN.finditer(text) if not m.group().startswith("#")]
    result, depth = [], 0
    for i, (value, start, end) in enumerate(tokens):
        if value == "{": depth += 1
        elif value == "}":
            depth -= 1
            if depth < 0: raise ValueError("Unexpected closing brace")
        elif depth == 0 and value == date and tokens[i + 1][0] == "=" and tokens[i + 2][0] == "{":
            inside = 1
            for j in range(i + 3, len(tokens)):
                if tokens[j][0] == "{": inside += 1
                elif tokens[j][0] == "}": inside -= 1
                if inside == 0:
                    result.append((start, tokens[i + 2][2], tokens[j][1], tokens[j][2]))
                    break
            else: raise ValueError("Unclosed date block")
    if depth: raise ValueError("Unclosed country history")
    return result


def strip_profile(text):
    pattern = re.compile(r"\t" + re.escape(BEGIN) + r"\r?\n.*?\t" + re.escape(END) + r"\r?\n", re.S)
    return pattern.sub("", text)


def render(profile, newline="\n"):
    currency, religion = profile["currency"], profile["religion"]
    factions = profile["factions"]
    remove = sorted(set(profile.get("remove_ideas", [])) - {currency, religion, *factions})
    lines = ["\t" + BEGIN, "\tif = {", "\t\tlimit = { IMP_is_1970_scenario = yes }"]
    # IMPERIA COLD WAR — Capture opinions before native on_add cleanup can clear them.
    temp_prefix = "COLDWAR_1970_society_"
    added = temp_prefix + "faction_added"
    lines.append("\t\tset_temp_variable = { " + added + " = 0 }")
    for faction in factions:
        opinion = faction + "_opinion"
        saved = temp_prefix + opinion
        lines += [
            "\t\tset_temp_variable = { " + saved + " = 50 }",
            "\t\tif = {",
            "\t\t\tlimit = { has_variable = " + opinion + " }",
            "\t\t\tset_temp_variable = { " + saved + " = " + opinion + " }",
            "\t\t}",
        ]
    for idea in remove:
        lines += [
            "\t\tif = {",
            "\t\t\tlimit = { has_idea = " + idea + " }",
            "\t\t\tremove_ideas = " + idea,
            "\t\t}",
        ]
    for idea in [currency, religion, *factions]:
        lines += [
            "\t\tif = {",
            "\t\t\tlimit = { NOT = { has_idea = " + idea + " } }",
            "\t\t\tadd_ideas = " + idea,
        ]
        if idea in factions:
            lines.append("\t\t\tset_temp_variable = { " + added + " = 1 }")
        lines.append("\t\t}")
    lines.append("\t\tset_variable = { no_foreign_reserve = " + str(profile["no_foreign_reserve"]) + " }")
    for faction in factions:
        opinion = faction + "_opinion"
        lines.append("\t\tset_variable = { " + opinion + " = " + temp_prefix + opinion + " }")
    # IMPERIA COLD WAR — Refresh once after restoration only when membership changed.
    lines += [
        "\t\tif = {",
        "\t\t\tlimit = { exists = yes check_variable = { " + added + " > 0 } }",
        "\t\t\tinitialize_internal_faction_dynamic_modifiers = yes",
        "\t\t}",
    ]
    lines += ["\t}", "\t" + END, ""]
    return newline.join(lines)


def patched(text, profile):
    original = strip_profile(text)
    spans = date_blocks(original)
    if not spans: raise ValueError("Country has no 1970.1.1 snapshot")
    newline = "\r\n" if "\r\n" in original else "\n"
    result = original
    for _, _, close, _ in reversed(spans):
        # Keep the original closing brace and its leading indentation untouched.
        line_start = result.rfind("\n", 0, close) + 1
        insertion = line_start if not result[line_start:close].strip() else close
        # The marker's leading tab also separates an inline preceding statement.
        # Do not add a newline outside the marked span: inverse removal must
        # restore inline closing braces byte for byte as well as line-only ones.
        result = result[:insertion] + render(profile, newline) + result[insertion:]
    return result
