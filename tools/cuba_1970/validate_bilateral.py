# IMPERIA COLD WAR — independent validation for Cuba bilateral output.
"""Static structural checks for the generated Cuba bilateral agreements."""
from pathlib import Path
from collections import Counter
import re
import sys
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools" / "vietnam_1970"))
from script_ast import emit, first, parse, walk  # noqa: E402

PARTNERS = {
    "sov": ("SOV", ("commodity", "industry")),
    "mex": ("MEX", ("energy", "agro")),
    "spr": ("SPR", ("nickel", "training")),
    "can": ("CAN", ("rail", "industry")),
}
SCRIPT_FILES = (
    "common/scripted_effects/COLDWAR_CUB_1970_bilateral.txt",
    "common/scripted_triggers/COLDWAR_CUB_1970_bilateral.txt",
    "common/ideas/COLDWAR_CUB_1970_bilateral_ideas.txt",
    "common/decisions/COLDWAR_CUB_1970_bilateral.txt",
    "common/decisions/categories/COLDWAR_CUB_1970_bilateral.txt",
    "events/COLDWAR_CUB_1970_bilateral.txt",
)
LOC_FILE = "localisation/english/COLDWAR_CUB_1970_bilateral_l_english.yml"
CHECKS = 0


def require(condition, message, errors):
    global CHECKS
    CHECKS += 1
    if not condition:
        errors.append(message)


def find_node(rows, name):
    for key, op, value in rows:
        if key == name and isinstance(value, list):
            return value
        if isinstance(value, list):
            found = find_node(value, name)
            if found is not None:
                return found
    return None


def node_text(node):
    return emit(node) if isinstance(node, list) else ""


def scalar(value):
    return value[1:-1] if isinstance(value, str) and len(value) >= 2 and value[0] == value[-1] == '"' else value


def normalized(value):
    try:
        return float(value.strip('"') if isinstance(value, str) else value)
    except (TypeError, ValueError):
        return value.strip('"') if isinstance(value, str) else value


def has_scoped_flag(node, tag, flag):
    if node is None:
        return False
    for key, op, value in node:
        if key == tag and isinstance(value, list):
            if any(k == "has_country_flag" and v == flag for k, _, v in value):
                return True
        if isinstance(value, list) and has_scoped_flag(value, tag, flag):
            return True
    return False


def legacy_main():
    errors = []
    texts = {}
    trees = {}
    for rel in SCRIPT_FILES:
        path = ROOT / rel
        require(path.is_file(), f"missing script output: {rel}", errors)
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        require(not raw.startswith("\ufeff"), f"script has UTF-8 BOM: {rel}", errors)
        require(raw.splitlines()[0].startswith("# IMPERIA COLD WAR — "),
                f"script lacks exact IMPERIA COLD WAR feature marker: {rel}", errors)
        texts[rel] = raw
        try:
            trees[rel] = parse(raw)
        except Exception as exc:
            errors.append(f"script AST parse failed: {rel}: {exc}")

    loc_path = ROOT / LOC_FILE
    require(loc_path.is_file(), f"missing English localisation: {LOC_FILE}", errors)
    loc = loc_path.read_text(encoding="utf-8-sig") if loc_path.is_file() else ""
    require(loc.startswith("l_english:"), "bilateral loc is not English", errors)
    require((loc_path.read_bytes().startswith(b"\xef\xbb\xbf") if loc_path.is_file() else False),
            "localisation must use UTF-8 BOM", errors)

    decision_tree = trees.get(SCRIPT_FILES[3], [])
    effects = texts.get(SCRIPT_FILES[0], "")
    triggers = texts.get(SCRIPT_FILES[1], "")
    ideas = texts.get(SCRIPT_FILES[2], "")
    categories = texts.get(SCRIPT_FILES[4], "")
    events = texts.get(SCRIPT_FILES[5], "")

    expected_ideas = set()
    for partner, (tag, terms) in PARTNERS.items():
        for term in terms:
            tid = f"COLDWAR_CUB_bilat_{partner}_{term}"
            expected_ideas.update((tid + "_cub", tid + "_" + partner))
            for key in (
                f"COLDWAR_CUB_accept_bilat_{partner}_{term}",
                f"COLDWAR_CUB_refuse_bilat_{partner}_{term}",
                f"COLDWAR_CUB_cancel_bilat_{partner}_{term}",
                f"COLDWAR_CUB_cancel_bilat_{partner}_{term}_as_partner",
                f"COLDWAR_CUB_offer_{partner}_{term}",
            ):
                require(find_node(decision_tree, key) is not None,
                        f"missing decision: {key}", errors)
                require(re.search(rf"(?m)^\s*{re.escape(key)}:0\s+\"", loc) is not None,
                        f"missing English decision localisation: {key}", errors)
            # Offers must be guarded on the proposer by bilateral eligibility and refusal expiry.
            offer = find_node(decision_tree, f"COLDWAR_CUB_offer_{partner}_{term}")
            offer_text = node_text(offer) if offer is not None else ""
            require(offer is not None and f"COLDWAR_CUB_pair_{partner}_clear" in offer_text,
                    f"offer lacks bilateral eligibility guard: {partner}/{term}", errors)
            require(offer is not None and f"COLDWAR_CUB_bilat_{partner}_refused" in offer_text,
                    f"offer can reopen during refusal lockout: {partner}/{term}", errors)
            # Partner acceptance requires both pending/open receipts and a second clear check in Cuba scope.
            accept = find_node(decision_tree, f"COLDWAR_CUB_accept_bilat_{partner}_{term}")
            accept_text = node_text(accept) if accept is not None else ""
            require(accept is not None and f"{tid}_offer_pending" in accept_text,
                    f"acceptance lacks term-specific pending receipt: {partner}/{term}", errors)
            require(accept is not None and f"COLDWAR_CUB_pair_{partner}_clear" in accept_text,
                    f"acceptance lacks mutual peace/sanctions guard: {partner}/{term}", errors)
            require(accept is not None and "effect_tooltip" in accept_text,
                    f"acceptance has no native effect preview: {partner}/{term}", errors)
            require(accept is not None and "hidden_effect" in accept_text,
                    f"acceptance mutations are not hidden behind preview: {partner}/{term}", errors)
            # Cancellation must clear the matching paired signature and reconcile ideas, while paid receipt persists.
            effect_tree = trees.get(SCRIPT_FILES[0], [])
            cancel = find_node(effect_tree, f"COLDWAR_CUB_cancel_{partner}_{term}")
            cancel_text = node_text(cancel) if cancel is not None else ""
            require(cancel is not None and f"{tid}_signed" in cancel_text,
                    f"cancel effect misses term signature: {partner}/{term}", errors)
            require(cancel is not None and "COLDWAR_CUB_reconcile_bilateral" in cancel_text,
                    f"cancel effect does not reconcile paired spirits: {partner}/{term}", errors)
            require(cancel is not None and f"{tid}_paid" not in cancel_text,
                    f"cancellation clears first-payment receipt unexpectedly: {partner}/{term}", errors)

    declared_ideas = set()
    for tree in trees.get(SCRIPT_FILES[2], []):
        if tree[0] == "ideas":
            def visit(rows):
                for key, op, value in rows:
                    if key != "_bare" and isinstance(value, list) and key.startswith("COLDWAR_CUB_bilat_"):
                        declared_ideas.add(key)
                    if isinstance(value, list):
                        visit(value)
            visit(tree[2])
    require(expected_ideas <= declared_ideas,
            "missing paired idea definitions: " + ", ".join(sorted(expected_ideas - declared_ideas)), errors)
    for key in expected_ideas:
        require(re.search(rf"(?m)^\s*{re.escape(key)}:0\s+\"", loc) is not None,
                f"missing idea localisation: {key}", errors)

    # Historical agreement migration must be one-time, bilateral, and cancellation-safe.
    reconcile = find_node(trees.get(SCRIPT_FILES[0], []), "COLDWAR_CUB_reconcile_bilateral")
    reconcile_text = node_text(reconcile) if reconcile is not None else ""
    require("COLDWAR_CUB_bilateral_legacy_migrated" in reconcile_text,
            "legacy agreement migration lacks its once-only receipt", errors)
    for tag, flag in (("SOV", "COLDWAR_CUB_soviet_assistance_active"),
                      ("DDR", "COLDWAR_CUB_symbolic_cooperation_active")):
        require(has_scoped_flag(reconcile, tag, flag),
                f"legacy migration does not require paired {tag} active receipt", errors)
    medical_cancel = find_node(trees.get(SCRIPT_FILES[0], []), "COLDWAR_CUB_cancel_medical_mission")
    medical_cancel_text = node_text(medical_cancel) if medical_cancel is not None else ""
    require("COLDWAR_CUB_medical_mission_365" in medical_cancel_text and
            "COLDWAR_CUB_reconcile_bilateral" in medical_cancel_text,
            "medical cancellation can re-adopt the legacy timed spirit", errors)
    for p, (tag, _) in PARTNERS.items():
        for term in PARTNERS[p][1]:
            refuse = find_node(decision_tree, f"COLDWAR_CUB_refuse_bilat_{p}_{term}")
            refuse_text = node_text(refuse) if refuse is not None else ""
            require(refuse is not None and f"COLDWAR_CUB_bilat_{p}_refused" in refuse_text and
                    f"COLDWAR_CUB_bilat_{p}_{term}_offer_pending" in refuse_text and
                    f"COLDWAR_CUB_bilat_{p}_{term}_offer_open" in refuse_text,
                    f"refusal does not clear both term receipts and set pair lockout: {p}/{term}", errors)

    # Check that every partner clear trigger checks both native embargo directions and all 4 x 2 IMP arrays.
    for partner, (tag, _) in PARTNERS.items():
        match = re.search(rf"(?ms)^COLDWAR_CUB_pair_{partner}_clear\s*=\s*\{{(.*?)^\}}", triggers)
        require(match is not None, f"missing bilateral clear trigger: {partner}", errors)
        if match:
            body = match.group(1)
            require("NOT = { is_embargoing = " + tag + " }" in body,
                    f"missing proposer-to-partner embargo check: {partner}", errors)
            require(f"NOT = {{ is_embargoing = CUB }}" in body,
                    f"missing partner-to-Cuba embargo check: {partner}", errors)
            for typ in ("dip", "fin", "eco", "mil"):
                for direction in ("on_us", "by_us"):
                    require(f"array = imp_{typ}_sanc_{direction} value = {tag}" in body,
                            f"missing proposer-side sanction array {typ}/{direction}: {partner}", errors)
                    require(f"array = imp_{typ}_sanc_{direction} value = CUB" in body,
                            f"missing partner-side sanction array {typ}/{direction}: {partner}", errors)

    medical_clear = re.search(r"(?ms)^COLDWAR_CUB_medical_pair_clear\s*=\s*\{(.*?)^\}", triggers)
    require(medical_clear is not None and "CUB = {" in medical_clear.group(1) and
            "PREV" in medical_clear.group(1),
            "medical bilateral trigger does not restore recipient scope through PREV", errors)

    for n in range(1, 9):
        event_id = f"COLDWAR_CUB_bilateral.{n}"
        require(f"id = {event_id}" in events, f"missing proposal event: {event_id}", errors)
        require(f"{event_id}.t:0 \"" in loc and f"{event_id}.d:0 \"" in loc,
                f"missing proposal event localisation: {event_id}", errors)

    # Current picture aliases must resolve through the local MD sprite registry.
    picture_names = set(re.findall(r"\bpicture\s*=\s*([A-Za-z0-9_]+)", ideas))
    registered = set()
    for gfx in (ROOT / "interface").glob("*.gfx"):
        try:
            registered.update(re.findall(r'name\s*=\s*"GFX_idea_([A-Za-z0-9_]+)"',
                                         gfx.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            pass
    require(picture_names <= registered,
            "idea pictures lack local GFX_idea registrations: " + ", ".join(sorted(picture_names - registered)), errors)

    print({"status": "pass" if not errors else "fail", "checks": CHECKS, "errors": errors})
    return 0 if not errors else 1


# IMPERIA COLD WAR — concept-derived bilateral contract validation.
def main():
    global CHECKS
    CHECKS = 0
    errors = []
    concept_path = HERE / "revision_design.json"
    approval_path = HERE / "revision_approval.json"
    concept = json.loads(concept_path.read_text(encoding="utf-8"))
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    import hashlib
    require(hashlib.sha256(concept_path.read_bytes()).hexdigest() == approval.get("sha256"),
            "revision concept hash differs from explicit approval", errors)
    parent_approval = json.loads((HERE / "foreign_approval.json").read_text(encoding="utf-8"))
    require(concept.get("parent_concept_sha256") == parent_approval.get("sha256") ==
            approval.get("parent_concept_sha256"),
            "revision does not bind the previously approved foreign concept", errors)
    nodes = [n for n in concept["nodes"] if n.get("partner")]
    require(len(nodes) == 23, f"approved foreign contract count changed: {len(nodes)}", errors)

    files = {
        "effects": "common/scripted_effects/COLDWAR_CUB_1970_foreign_contracts.txt",
        "triggers": "common/scripted_triggers/COLDWAR_CUB_1970_foreign_contracts.txt",
        "ideas": "common/ideas/COLDWAR_CUB_1970_foreign_contracts.txt",
        "responses": "common/decisions/COLDWAR_CUB_1970_foreign_contracts.txt",
        "cub_cancel": "common/decisions/COLDWAR_CUB_1970_foreign_cancel.txt",
        "categories": "common/decisions/categories/COLDWAR_CUB_1970_foreign_contracts.txt",
        "events": "events/COLDWAR_CUB_1970_foreign_contracts.txt",
        "loc": "localisation/english/COLDWAR_CUB_1970_foreign_contracts_l_english.yml",
    }
    texts = {}
    trees = {}
    for kind, rel in files.items():
        path = ROOT / rel
        require(path.is_file(), f"missing contract output: {rel}", errors)
        if not path.is_file():
            continue
        raw = path.read_bytes()
        if kind == "loc":
            require(raw.startswith(b"\xef\xbb\xbf"), f"localisation must have UTF-8 BOM: {rel}", errors)
            try:
                texts[kind] = raw.decode("utf-8-sig")
            except UnicodeDecodeError as exc:
                errors.append(f"localisation is not UTF-8: {rel}: {exc}")
                texts[kind] = ""
        else:
            require(not raw.startswith(b"\xef\xbb\xbf"), f"script has UTF-8 BOM: {rel}", errors)
            try:
                texts[kind] = raw.decode("utf-8")
                require(texts[kind].splitlines()[0].startswith("# IMPERIA COLD WAR — "),
                        f"script lacks required feature marker: {rel}", errors)
                trees[kind] = parse(texts[kind])
            except (UnicodeDecodeError, ValueError, IndexError) as exc:
                errors.append(f"script AST/encoding error: {rel}: {exc}")
                texts[kind] = ""
                trees[kind] = []

    effects = trees.get("effects", [])
    triggers = trees.get("triggers", [])
    ideas = trees.get("ideas", [])
    responses = trees.get("responses", [])
    cub_cancel = trees.get("cub_cancel", [])
    categories = trees.get("categories", [])
    events = trees.get("events", [])
    loc = texts.get("loc", "")
    effect_text = texts.get("effects", "")
    trigger_text = texts.get("triggers", "")
    embargo_sync = []
    embargo_sync_path = ROOT / "common/scripted_effects/COLDWAR_CUB_1970_diplomacy.txt"
    if embargo_sync_path.is_file():
        try:
            embargo_sync = find_node(
                parse(embargo_sync_path.read_text(encoding="utf-8-sig")),
                "COLDWAR_CUB_sync_embargo",
            ) or []
        except (UnicodeDecodeError, ValueError, IndexError) as exc:
            errors.append(f"could not parse native embargo reconciliation helper: {exc}")
    else:
        errors.append("missing native embargo reconciliation helper COLDWAR_CUB_sync_embargo")

    def suffix(node):
        return node["key"].removeprefix("foreign_")

    def flag(node, kind):
        return f"COLDWAR_CUB_foreign_{suffix(node)}_{kind}"

    def idea(node, side):
        if node["key"] == "foreign_cmea" and side == "cub":
            return "COLDWAR_CUB_cmea_member"
        return f"COLDWAR_CUB_foreign_{suffix(node)}_{side}"

    def has_flag(rows, name):
        return any(k == "has_country_flag" and v == name for k, _, v in walk(rows))

    def has_negated_flag(rows, name):
        for key, _, body in walk(rows):
            if key == "NOT" and isinstance(body, list) and has_flag(body, name):
                return True
        return False

    def scope(rows, tag):
        bodies = [body for key, _, body in walk(rows) if key == tag and isinstance(body, list)]
        return [entry for body in bodies for entry in body]

    def temp_values(rows):
        return [normalized(first(body, "treasury_change"))
                for key, _, body in walk(rows)
                if key == "set_temp_variable" and isinstance(body, list)
                and first(body, "treasury_change") is not None]

    def script_idea_ids(rows):
        found = set()
        for key, _, body in walk(rows):
            if key in ("add_ideas", "remove_ideas") and isinstance(body, str):
                found.add(body)
        return found

    def idea_transforms(rows):
        """Return distinct native add/remove idea IDs, including brace lists."""
        result = {"add_ideas": set(), "remove_ideas": set()}
        for key, _, body in walk(rows):
            if key not in result:
                continue
            if isinstance(body, str):
                result[key].add(body.strip('"'))
            elif isinstance(body, list):
                result[key].update(value.strip('"') for name, _, value in body
                                   if name == "_bare" and isinstance(value, str))
        return result

    def preview_variable_map(rows):
        result = {}
        for key, _, body in walk(rows):
            if key != "add_to_variable" or not isinstance(body, list):
                continue
            tooltip = first(body, "tooltip")
            for variable, _, value in body:
                if variable.startswith("COLDWAR_CUB_foreign_preview_"):
                    result[variable] = (normalized(value), tooltip)
        return result

    def idea_modifiers(idea_node):
        modifier = first(idea_node or [], "modifier", [])
        return {key: normalized(value) for key, _, value in modifier if key != "_bare"}

    def parse_loc_keys(source):
        return {m.group(1) for m in re.finditer(r"(?m)^\s*([^\s:]+):(?:\d+)?\s+\"", source)}

    def event_block(rows, event_id):
        for key, _, body in rows:
            if key == "country_event" and isinstance(body, list) and first(body, "id") == event_id:
                return body
            if isinstance(body, list):
                found = event_block(body, event_id)
                if found is not None:
                    return found
        return None

    # Namespace and event payloads are concept ordered and contiguous.
    require("add_namespace = COLDWAR_CUB_foreign_contracts" in texts.get("events", ""),
            "foreign proposal event namespace is missing", errors)
    gfx_names = set()
    for gfx_path in (ROOT / "interface").glob("*.gfx"):
        gfx_names.update(re.findall(r'name\s*=\s*"(GFX_[A-Za-z0-9_]+)"',
                                    gfx_path.read_text(encoding="utf-8", errors="ignore")))
    proposal_previews = {}
    for index, node in enumerate(nodes):
        event_id = f"COLDWAR_CUB_foreign_contracts.{400 + index}"
        require(f"id = {event_id}" in texts.get("events", ""),
                f"missing proposal event {event_id}", errors)
        proposal = event_block(events, event_id)
        proposal_text = node_text(proposal) if proposal is not None else ""
        key = suffix(node)
        tag = node["partner"]
        pending = flag(node, "offer_pending")
        opened = flag(node, "offer_open")
        require(proposal is not None and first(proposal, "is_triggered_only") == "yes",
                f"proposal event is not trigger-only: {key}", errors)
        proposal_trigger = find_node(proposal or [], "trigger") or []
        require(f"tag = {tag}" in node_text(proposal_trigger)
                and has_flag(proposal_trigger, pending)
                and opened in node_text(proposal_trigger)
                and "CUB" in node_text(proposal_trigger),
                f"proposal event does not require the named recipient and mirrored live-offer receipts: {key}", errors)
        immediate = find_node(proposal or [], "immediate") or []
        require(f"COLDWAR_CUB_EVENT_DELIVERED {node['key']} {tag}" in node_text(immediate)
                and f"COLDWAR_CUB_foreign_{key}_notified" in node_text(immediate),
                f"proposal event lacks its recipient-side delivery log/receipt: {key}", errors)
        options = [body for name, _, body in proposal or [] if name == "option" and isinstance(body, list)]
        accept_option = next((body for body in options
                              if first(body, "name") == f"COLDWAR_CUB_foreign_contracts.{key}.accept"), None)
        refuse_option = next((body for body in options
                              if first(body, "name") == f"COLDWAR_CUB_foreign_contracts.{key}.refuse"), None)
        require(accept_option is not None and refuse_option is not None,
                f"proposal event lacks explicit accept/refuse options: {key}", errors)
        for option_key in (f"COLDWAR_CUB_foreign_contracts.{key}.accept",
                           f"COLDWAR_CUB_foreign_contracts.{key}.refuse"):
            require(option_key in parse_loc_keys(texts.get("loc", "")),
                    f"proposal option lacks English localization: {key}/{option_key}", errors)
        accept_preview = find_node(accept_option or [], "effect_tooltip") or []
        proposal_previews[key] = accept_preview
        accept_hidden = find_node(accept_option or [], "hidden_effect") or []
        require(script_idea_ids(accept_preview) >= {idea(node, "cub"), idea(node, "partner")},
                f"recipient acceptance preview does not show both bilateral spirits: {key}", errors)
        require(f"COLDWAR_CUB_foreign_accept_{key} = yes" in node_text(accept_hidden),
                f"recipient acceptance option does not call its guarded acceptance transaction: {key}", errors)
        picture = scalar(first(proposal or [], "picture"))
        require(picture in gfx_names,
                f"proposal event picture is not registered: {key}/{picture}", errors)
    for event_id in ("COLDWAR_CUB_foreign_contracts.900", "COLDWAR_CUB_foreign_contracts.901"):
        require(f"id = {event_id}" in texts.get("events", ""), f"missing response event {event_id}", errors)

    expected_ideas = set()
    declared_ideas = {k for k, _, v in walk(ideas) if isinstance(v, list)
                      and k.startswith("COLDWAR_CUB_foreign_")}
    legacy_idea_path = ROOT / "common/ideas/COLDWAR_CUB_1970_diplomacy_ideas.txt"
    legacy_ideas = []
    if legacy_idea_path.is_file():
        try:
            legacy_ideas = parse(legacy_idea_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"cannot parse legacy Cuba membership idea provider: {exc}")
    response_root = find_node(responses, "COLDWAR_CUB_foreign_responses")
    response_decision_ids = {k for k, _, _ in (response_root or [])}
    for node in nodes:
        key = suffix(node)
        tag = node["partner"]
        term = f"foreign_{key}"
        base = f"COLDWAR_CUB_foreign_{key}"
        signed = flag(node, "signed")
        offer_open = flag(node, "offer_open")
        pending = flag(node, "offer_pending")
        paid = flag(node, "paid")
        pair_clear = f"COLDWAR_CUB_foreign_pair_clear_{key}"
        accept_valid = f"COLDWAR_CUB_foreign_accept_valid_{key}"
        offer_name = f"COLDWAR_CUB_foreign_offer_{key}"
        offer = find_node(effects, offer_name)
        pair = find_node(triggers, pair_clear)
        valid = find_node(triggers, accept_valid)
        accept_helper = find_node(effects, f"COLDWAR_CUB_foreign_accept_{key}")
        cancel_effect = find_node(effects, f"COLDWAR_CUB_foreign_cancel_{key}")

        require(offer is not None, f"missing proposal effect {offer_name}", errors)
        offer_text = node_text(offer) if offer is not None else ""
        require(f"country_exists = {tag}" in offer_text and f"{tag} =" in offer_text,
                f"proposal does not route to concept partner {tag}: {key}", errors)
        require("days = 90" in offer_text and "value = 1" in offer_text,
                f"proposal window is not a 90-day timed offer: {key}", errors)
        require(pending in offer_text and offer_open in offer_text,
                f"offer does not mirror pending/open receipts: {key}", errors)
        require(f"country_event = {{ id = COLDWAR_CUB_foreign_contracts.{400 + nodes.index(node)} }}" in offer_text,
                f"proposal event ID does not match concept order: {key}", errors)

        pair_text = node_text(pair) if pair is not None else ""
        require("has_war_with" in pair_text and "is_embargoing" in pair_text,
                f"pair trigger omits mutual peace or native embargo check: {key}", errors)
        for cls in ("dip", "fin", "eco", "mil"):
            for direction in ("on_us", "by_us"):
                require(f"imp_{cls}_sanc_{direction}" in pair_text,
                        f"pair trigger omits {cls}/{direction} sanctions: {key}", errors)
        require(tag in pair_text and "CUB" in pair_text,
                f"pair trigger does not evaluate both signatories: {key}", errors)

        valid_text = node_text(valid) if valid is not None else ""
        require(has_flag(valid or [], pending) and has_negated_flag(valid or [], signed),
                f"acceptance trigger lacks pending/current-signature guards: {key}", errors)
        require(offer_open in valid_text and has_flag(valid or [], pending)
                and f"tag = {tag}" in valid_text,
                f"acceptance trigger does not recheck the active offer without blocking signatures under sanctions: {key}", errors)

        # Four recipient decisions, plus a separate Cuba-side cancel action.
        for kind in ("accept", "refuse", "reopen", "cancel"):
            name = f"COLDWAR_CUB_foreign_{kind}_{key}"
            decision = find_node(responses, name)
            require(decision is not None, f"missing recipient decision: {name}", errors)
            require(re.search(rf"(?m)^\s*{re.escape(name)}:0\s+\"", loc) is not None,
                    f"missing English localisation for decision: {name}", errors)
        cub_cancel_name = f"COLDWAR_CUB_foreign_cancel_{key}_as_cub"
        require(find_node(cub_cancel, cub_cancel_name) is not None,
                f"missing Cuba-side cancel decision: {cub_cancel_name}", errors)
        require(f"COLDWAR_CUB_foreign_offer_{key}" not in response_decision_ids,
                f"an offer selector/decision was added outside the Cuban focus: {key}", errors)

        accept = find_node(responses, f"COLDWAR_CUB_foreign_accept_{key}")
        accept_text = node_text(accept) if accept is not None else ""
        accept_decision_hidden = find_node(accept or [], "hidden_effect")
        accept_decision_hidden_text = node_text(accept_decision_hidden) if accept_decision_hidden is not None else ""
        accept_effect_text = node_text(accept_helper) if accept_helper is not None else ""
        require("effect_tooltip" in accept_text and "hidden_effect" in accept_text,
                f"accept decision must separate native preview from effects: {key}", errors)
        require(f"COLDWAR_CUB_foreign_accept_{key} = yes" in accept_decision_hidden_text,
                f"accept decision does not invoke its validated transaction helper: {key}", errors)
        preview_ideas = script_idea_ids(find_node(accept or [], "effect_tooltip") or [])
        preview_body = find_node(accept or [], "effect_tooltip") or []
        expected_pair_ideas = {idea(node, "cub"), idea(node, "partner")}
        expected_ideas.update(expected_pair_ideas)
        for ident in expected_pair_ideas:
            if ident == "COLDWAR_CUB_cmea_member":
                require(find_node(legacy_ideas, ident) is not None,
                        "COMECON membership agreement references an undefined legacy member spirit", errors)
            else:
                require(ident in declared_ideas,
                        f"missing paired agreement spirit definition: {ident}", errors)
        require(expected_pair_ideas <= preview_ideas,
                f"accept preview does not show both agreement spirits: {key}", errors)

        # US normalization previews must expose the actual Cuban restriction
        # transition: limited easing replaces the full embargo with its limited
        # spirit; final settlement removes both. The limited spirit must not
        # appear in the settlement preview or be re-added there.
        cub_preview_transforms = idea_transforms(scope(preview_body, "CUB"))
        full_embargo = "COLDWAR_CUB_american_embargo"
        limited_embargo = "COLDWAR_CUB_american_embargo_limited"
        if key == "limited":
            require(full_embargo in cub_preview_transforms["remove_ideas"]
                    and limited_embargo in cub_preview_transforms["add_ideas"],
                    "limited US easing preview must replace the full embargo spirit with the limited spirit", errors)
        elif key == "settlement":
            require({full_embargo, limited_embargo} <= cub_preview_transforms["remove_ideas"]
                    and limited_embargo not in cub_preview_transforms["add_ideas"],
                    "US settlement preview must remove both embargo spirits and not re-add limited embargo", errors)

        if key == "limited":
            require("set_country_flag = COLDWAR_CUB_us_easing_limited" in accept_effect_text
                    and "COLDWAR_CUB_sync_embargo = yes" in accept_effect_text,
                    "limited US easing acceptance must stamp its policy receipt and reconcile embargo spirits", errors)
        elif key == "settlement":
            require("set_country_flag = COLDWAR_CUB_us_full_settlement" in accept_effect_text
                    and "clr_country_flag = COLDWAR_CUB_us_easing_limited" in accept_effect_text
                    and "COLDWAR_CUB_sync_embargo = yes" in accept_effect_text,
                    "US settlement acceptance must stamp final settlement, clear limited easing and reconcile", errors)

        # The runtime change is applied through the shared native burden reconciler.
        # Verify its partial-easing branch grants only the limited spirit and its
        # settled branch removes both spirits without restoring the full embargo.
        limited_sync_branch = find_node(embargo_sync, "else_if")
        limited_sync_transforms = idea_transforms(limited_sync_branch or [])
        limited_sync_text = node_text(limited_sync_branch) if limited_sync_branch else ""
        require("COLDWAR_CUB_us_easing_limited" in limited_sync_text
                and full_embargo in limited_sync_transforms["remove_ideas"]
                and limited_embargo in limited_sync_transforms["add_ideas"],
                "native embargo sync lacks the limited-easing branch that replaces full embargo with limited spirit", errors)
        settled_sync_branch = find_node(embargo_sync, "else")
        settled_sync_transforms = idea_transforms(settled_sync_branch or [])
        settled_sync_text = node_text(settled_sync_branch) if settled_sync_branch else ""
        require({full_embargo, limited_embargo} <= settled_sync_transforms["remove_ideas"]
                and limited_embargo not in settled_sync_transforms["add_ideas"]
                and "COLDWAR_CUB_us_full_settlement" in settled_sync_text,
                "native embargo sync must clear both spirits after full settlement and never restore limited spirit", errors)

        # Each side's effect preview is derived from the concept's modifier map,
        # using MD's parameterized tooltip keys and no hand-written deltas.
        for side_name, side_tag in (("cub", "CUB"), ("partner", tag)):
            side_preview = scope(preview_body, side_tag)
            expected_modifiers = node.get("cub_modifiers" if side_name == "cub" else "partner_modifiers", {})
            def native_tooltip(modifier):
                # These two fields use MD's shared formatter names rather than
                # the mechanical modifier name. validate.py separately checks
                # that every referenced key resolves and uses RIGHT formatting.
                aliases = {
                    "imp_sanction_resistance": "COLDWAR_imp_sanction_resistance_tt",
                    "research_speed_factor": "COLDWAR_research_speed_factor_tt",
                    "army_org_factor": "COLDWAR_army_org_factor_tt",
                }
                return aliases.get(modifier, modifier + "_tt")
            expected_map = {
                f"COLDWAR_CUB_foreign_preview_{key}_{side_name}_{modifier}":
                    (float(value), native_tooltip(modifier))
                for modifier, value in expected_modifiers.items()
            }
            actual_map = preview_variable_map(side_preview)
            require(actual_map == expected_map,
                    f"native modifier preview differs from concept for {key}/{side_name}: {actual_map} != {expected_map}", errors)

            idea_name = idea(node, side_name)
            if idea_name != "COLDWAR_CUB_cmea_member":
                definition = find_node(ideas, idea_name)
                require(definition is not None,
                        f"missing bilateral idea definition {idea_name}", errors)
                actual_modifiers = idea_modifiers(definition)
                require(actual_modifiers == {m: float(v) for m, v in expected_modifiers.items()},
                        f"paired idea modifier values differ from concept for {key}/{side_name}: {actual_modifiers}", errors)
                cancel_block = find_node(definition, "cancel")
                cancel_or = find_node(cancel_block or [], "OR")
                cancelled_tags = set()
                for clause, _, body in cancel_or or []:
                    if clause == "NOT" and isinstance(body, list):
                        cancelled_tags.update(
                            scalar(value) for name, _, value in body
                            if name == "country_exists"
                        )
                require(cancel_or is not None and cancelled_tags == {"CUB", tag},
                        f"paired idea cancellation must remove the spirit if either signatory ceases to exist: {idea_name} ({cancelled_tags})", errors)
        require(accept_valid in accept_effect_text,
                f"accept effect does not use the validated bilateral trigger: {key}", errors)
        require(signed in accept_effect_text and pending in accept_effect_text and offer_open in accept_effect_text,
                f"acceptance does not stamp/clear mirrored agreement receipts: {key}", errors)
        require(paid in accept_effect_text and has_negated_flag(accept_helper or [], paid),
                f"setup costs are not protected by a one-time paid receipt: {key}", errors)

        # Confirm concept setup costs on each country side in the accepted reward.
        costs = node.get("setup_costs", [0, 0])
        accepted_treasury_values = temp_values(accept_helper or [])
        if len(costs) >= 2:
            if float(costs[0]):
                require(any(abs(v + float(costs[0])) < 1e-7 for v in accepted_treasury_values),
                        f"Cuban setup cost differs from concept for {key}: {costs[0]}", errors)
            if float(costs[1]):
                require(any(abs(v + float(costs[1])) < 1e-7 for v in accepted_treasury_values),
                        f"Partner setup cost differs from concept for {key}/{tag}: {costs[1]}", errors)

        refuse = find_node(responses, f"COLDWAR_CUB_foreign_refuse_{key}")
        refuse_text = node_text(refuse) if refuse is not None else ""
        require(pending in refuse_text and offer_open in refuse_text,
                f"refusal lacks pending/open guard/cleanup: {key}", errors)
        require(paid not in refuse_text,
                f"refusal incorrectly charges a setup cost: {key}", errors)

        require(cancel_effect is not None, f"missing bilateral cancel effect: {key}", errors)
        cancel_text = node_text(cancel_effect) if cancel_effect is not None else ""
        require(signed in cancel_text and "COLDWAR_CUB_foreign_reconcile_all" in cancel_text,
                f"cancellation does not clear both signatures and reconcile paired spirits: {key}", errors)
        require(paid not in cancel_text,
                f"cancellation clears the persistent paid receipt: {key}", errors)

        # First-time grant receipts survive cancellation, so re-entry never
        # duplicates construction, research, compensation, experience, or lifting.
        grant = flag(node, "grant_receipt")
        if node.get("accepted_effects"):
            require(grant in accept_effect_text and has_negated_flag(accept_helper or [], grant),
                    f"one-time accepted terms lack a durable bilateral receipt: {key}", errors)
            research_name = f"COLDWAR_CUB_foreign_{key}_research"
            expected_research = {"CUB": [], tag: []}
            for effect in node["accepted_effects"]:
                if effect["kind"] == "lift_mutual_sanctions":
                    helper = f"COLDWAR_CUB_foreign_lift_sanctions_{key}"
                    helper_ast = find_node(effects, helper)
                    helper_text = node_text(helper_ast) if helper_ast is not None else ""
                    require(helper in accept_effect_text and helper_ast is not None,
                            f"accepted sanctions term does not call its native removal helper: {key}", errors)
                    class_map = {"diplomatic": "dip", "financial": "fin", "economic": "eco", "military": "mil"}
                    expected_arrays = {f"imp_{class_map.get(cls, cls)}_sanc_{direction}"
                                       for cls in effect["classes"] for direction in ("on_us", "by_us")}
                    actual_arrays = set(re.findall(r"array\s*=\s*(imp_[a-z]+_sanc_(?:on_us|by_us))", helper_text))
                    require(actual_arrays == expected_arrays,
                            f"sanctions helper class/direction scope differs for {key}: {actual_arrays} != {expected_arrays}", errors)
                    cub_scope = find_node(helper_ast or [], "CUB")
                    partner_scope = find_node(helper_ast or [], tag)
                    require(any(k == "imp_sanctions_calculate" for k, _, _ in scope(helper_ast or [], "CUB"))
                            and any(k == "imp_sanctions_calculate" for k, _, _ in scope(helper_ast or [], tag)),
                            f"sanctions helper does not recalculate both signatories: {key}", errors)
                elif effect["kind"] == "transfer_state":
                    require(f"transfer_state = {effect['state']}" in accept_effect_text,
                            f"cession term does not transfer concept state {effect['state']}: {key}", errors)
                elif effect["kind"] == "treasury":
                    country = effect["country"]
                    recipient = scope(accept_helper or [], country)
                    amount = float(effect["amount"])
                    require(any(abs(v - amount) < 1e-7 for v in temp_values(recipient)),
                            f"one-time compensation differs from concept for {key}/{country}", errors)
                elif effect["kind"] == "experience":
                    country_body = scope(accept_helper or [], effect.get("country", "CUB"))
                    require(any(k == "army_experience" and normalized(v) == effect["army"]
                                for k, _, v in walk(country_body)),
                            f"one-time Army Experience differs from concept for {key}", errors)
                elif effect["kind"] == "building":
                    state_body = find_node(accept_helper or [], str(effect["state"]))
                    require(state_body is not None and any(k == "add_building_construction"
                                and scalar(first(v, "type")) == effect["building"]
                                and normalized(first(v, "level")) == effect["levels"]
                                for k, _, v in walk(state_body)),
                            f"one-time building project differs from concept for {key}", errors)
                elif effect["kind"] == "research":
                    research_country = effect.get("country", "CUB")
                    expected_research.setdefault(research_country, []).append(
                        (research_name, effect["category"], float(effect["bonus"]), int(effect["uses"]))
                    )

            def research_counter(rows, country):
                return Counter(
                    (scalar(first(body, "name")), scalar(first(body, "category")),
                     float(normalized(first(body, "bonus"))), int(normalized(first(body, "uses"))))
                    for k, _, body in walk(scope(rows, country))
                    if k == "add_tech_bonus" and isinstance(body, list)
                )

            for country in set(expected_research) | {"CUB", tag}:
                expected_rows = Counter(expected_research.get(country, []))
                event_preview_rows = research_counter(proposal_previews.get(key, []), country)
                decision_preview_rows = research_counter(preview_body, country)
                runtime_rows = research_counter(accept_helper or [], country)
                require(event_preview_rows == expected_rows,
                        f"offer-event research preview differs from approved recipient/category/uses for {key}/{country}: "
                        f"{event_preview_rows} != {expected_rows}", errors)
                require(decision_preview_rows == expected_rows,
                        f"recipient-decision research preview differs from approved recipient/category/uses for {key}/{country}: "
                        f"{decision_preview_rows} != {expected_rows}", errors)
                require(runtime_rows == expected_rows,
                        f"accepted research reward differs from approved recipient/category/uses for {key}/{country}: "
                        f"{runtime_rows} != {expected_rows}", errors)
            if any(node_effect["kind"] == "research" for node_effect in node.get("accepted_effects", [])):
                research_loc_lines = re.findall(rf"(?m)^\s*{re.escape(research_name)}:0\s+\"", loc)
                require(len(research_loc_lines) == 1,
                        f"research local key must be declared exactly once: {research_name} ({len(research_loc_lines)})", errors)

        # Decision and spirit localisation are part of the actual recipient UI.
        for ident in expected_pair_ideas:
            idea_loc = loc
            if ident == "COLDWAR_CUB_cmea_member":
                idea_loc = "\n".join(path.read_text(encoding="utf-8-sig", errors="replace")
                                       for path in (ROOT / "localisation/english").glob("*.yml"))
            require(re.search(rf"(?m)^\s*{re.escape(ident)}:0\s+\"", idea_loc) is not None,
                    f"missing agreement spirit localisation: {ident}", errors)

    # Paired spirits exist only while both signature receipts are present and
    # the mutual peace/sanctions gate remains clear. The else branch removes them.
    reconcile = find_node(effects, "COLDWAR_CUB_foreign_reconcile_all")
    reconcile_text = node_text(reconcile) if reconcile is not None else ""
    require(reconcile is not None, "missing paired-spirit reconciliation effect", errors)
    for node in nodes:
        key = suffix(node)
        cond = f"COLDWAR_CUB_foreign_pair_clear_{key}"
        require(flag(node, "signed") in reconcile_text and cond in reconcile_text,
                f"reconciliation does not gate both agreement signatures and eligibility: {key}", errors)
        require(idea(node, "cub") in reconcile_text and idea(node, "partner") in reconcile_text,
                f"reconciliation does not add/remove both paired spirits: {key}", errors)

    # The categories belong in the category file, not embedded inside decision
    # definitions, and only the recipient can accept/refuse/reopen proposals.
    cat_text = texts.get("categories", "")
    require("COLDWAR_CUB_foreign_responses = {" in cat_text and "allowed = { NOT = { tag = CUB } }" in cat_text,
            "recipient response category is missing or incorrectly scoped", errors)
    require("COLDWAR_CUB_foreign_cancellation = {" in cat_text and "allowed = { tag = CUB }" in cat_text,
            "Cuba cancellation category is missing or incorrectly scoped", errors)

    # All proposals and both terminal events must have complete English strings.
    loc_keys = parse_loc_keys(loc)
    for node in nodes:
        key = suffix(node)
        for loc_key in (f"COLDWAR_CUB_foreign_contracts.{key}.t",
                        f"COLDWAR_CUB_foreign_contracts.{key}.d",
                        f"COLDWAR_CUB_foreign_accept_{key}",
                        f"COLDWAR_CUB_foreign_refuse_{key}",
                        f"COLDWAR_CUB_foreign_reopen_{key}",
                        f"COLDWAR_CUB_foreign_cancel_{key}"):
            require(loc_key in loc_keys, f"missing English localization: {loc_key}", errors)
    for event_key in ("COLDWAR_CUB_foreign_contracts.accepted.t",
                      "COLDWAR_CUB_foreign_contracts.accepted.d",
                      "COLDWAR_CUB_foreign_contracts.refused.t",
                      "COLDWAR_CUB_foreign_contracts.refused.d"):
        require(event_key in loc_keys, f"missing terminal event English localization: {event_key}", errors)

    # Ethiopia's recipient-political gate is visible in the focus and is
    # repeated in the offer, acceptance, and reopen checks. Assert MD's named
    # party predicates at each provider instead of numeric ruling_party IDs.
    party_trigger_path = ROOT / "common/scripted_triggers/COLDWAR_CUB_1970_triggers.txt"
    require(party_trigger_path.is_file(), "missing Cuba focus trigger provider for Ethiopia eligibility", errors)
    try:
        party_triggers = parse(party_trigger_path.read_text(encoding="utf-8")) if party_trigger_path.is_file() else []
    except Exception as exc:
        errors.append(f"cannot parse Cuba focus trigger provider for Ethiopia eligibility: {exc}")
        party_triggers = []
    expected_eth_party = {
        "emerging_communist_state_are_in_power",
        "neutrality_neutral_communism_are_in_power",
        "nationalist_military_junta_are_in_power",
    }

    def valid_eth_party_gate(rows):
        eth_scopes = [body for key, _, body in walk(rows) if key == "ETH" and isinstance(body, list)]
        named = set()
        numeric = False
        for body in eth_scopes:
            for key, _, value in walk(body):
                if key in expected_eth_party and scalar(value) == "yes":
                    named.add(key)
                if key == "check_variable" and isinstance(value, list) and first(value, "ruling_party") is not None:
                    numeric = True
        return expected_eth_party <= named and not numeric

    eth_party_providers = [
        ("visible Cuba focus availability", find_node(party_triggers, "COLDWAR_CUB_can_foreign_ethiopia")),
        ("Cuba offer issuance", find_node(effects, "COLDWAR_CUB_foreign_offer_ethiopia")),
        ("recipient acceptance", find_node(triggers, "COLDWAR_CUB_foreign_accept_valid_ethiopia")),
        ("recipient reopening", find_node(responses, "COLDWAR_CUB_foreign_reopen_ethiopia")),
    ]
    for label, provider in eth_party_providers:
        require(provider is not None and valid_eth_party_gate(provider),
                f"Ethiopia {label} must use the three exact native party predicates in ETH scope and no numeric ruling_party check",
                errors)

    # The acceptance event hooks execute each native embargo break in the
    # country that imposed it, and re-run each country's sanctions calculation.
    event_950 = event_block(events, "COLDWAR_CUB_foreign_contracts.950")
    event_951 = event_block(events, "COLDWAR_CUB_foreign_contracts.951")
    event_950_text = node_text(event_950) if event_950 is not None else ""
    event_951_text = node_text(event_951) if event_951 is not None else ""
    require("tag" in event_950_text and "is_embargoing" in event_950_text and "break_embargo" in event_950_text
            and "USA" in event_950_text,
            "Cuba-side native embargo event does not lift the USA embargo in Cuban scope", errors)
    require("tag" in event_951_text and "is_embargoing" in event_951_text and "break_embargo" in event_951_text
            and "CUB" in event_951_text and "USA" in event_951_text,
            "USA-side native embargo event does not lift the Cuban embargo in USA scope", errors)

    result = {"status": "pass" if not errors else "fail", "checks": CHECKS,
              "errors": errors, "approved_partner_focuses": len(nodes),
              "expected_event_ids": [f"COLDWAR_CUB_foreign_contracts.{i}" for i in range(400, 423)],
              "native_engine_tested": False}
    out_path = HERE / "BILATERAL_VALIDATION.json"
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
