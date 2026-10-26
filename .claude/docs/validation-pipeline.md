# Validation Pipeline

This fork has no upstream MD validator suite, no pre-commit hooks, no pytest suite and
no CI gate. Validation is the four layers below, in this order. Report each layer's
result separately and never present a lower layer as proof of a higher one.

## 1. Static preflight (always)

```bash
python -X utf8 .agents/skills/hoi4-validate-debug/scripts/check_hoi4_files.py --root . --path <file> [--path <file> ...]
```

- Without `--path` it scans `common`, `events`, `history`, `interface`, `gfx`, `map` and
  `localisation`. That surfaces inherited MD findings; compare against a run on the base
  branch before calling anything new.
- `--strict` makes warnings fail the exit code.
- Output: one `path:line: LEVEL: message` per finding, then
  `Checked N files: E errors, W warnings.` It is never truncated.
- It checks brace and quote balance, BOM rules (scripts without BOM, `.yml` with BOM),
  `l_<language>:` headers, malformed or duplicate loc keys, and unclosed `§` colour
  codes. It does not parse Clausewitz semantics, scopes, triggers or effects, and it
  does not resolve references.

## 2. Reference trace (manual, for every new or renamed id)

The checker cannot see these. Grep them:

- Every focus, decision, event, idea, dynamic modifier, scripted effect or trigger the
  change adds is defined once and invoked somewhere reachable at 1970.
- Every `tooltip =`, `custom_effect_tooltip`, `custom_trigger_tooltip`, `_desc` and
  modifier `_tt` key resolves in `localisation/english/`.
- Every `GFX_` name resolves in `interface/*.gfx` or in vanilla (see
  `known-false-positives.md`), and every texture path exists.
- Event namespaces, ids and GUI element names are unique across the repository.
- Gates: new content is reachable under `IMP_is_1970_scenario = yes` and does not leak
  into inherited 2000-era systems.

## 3. Country validators (when the country has them)

Several 1970 countries ship their own checks under `tools/<country>_1970/`, for example
`validate.py`, `validate_content.py`, `validate_runtime.py`, `validate_tree.py`,
`validate_integration.py` and `check_rebuild.py`. Run the ones for the country you
touched, from the repository root, with `python -X utf8`. Runtime-cost harnesses live in
`tools/runtime_performance/` (`check_runtime.py`, `check_md202.py`, `check_greece.py`).
Read a tool's README or argparse help before running it; some rebuild loaded files.

## 4. Engine and multiplayer (cannot be run by the agent)

- Single player: start the 1970 bookmark in a clean playset, reproduce the change, then
  read `Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log` (delete it first
  so it only holds this session). `debug-commands.md` has console recipes.
- Multiplayer: the two-client matrix from `AGENTS.md`. Only a real two-client session
  supports an OOS or synchronisation claim.

Write the outcome as: static check (result), reference trace (done or gaps), country
validators (which, result), single player (not run or result), two-client MP (not run
or result).
