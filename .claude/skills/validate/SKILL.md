---
name: validate
description: 'Run the Cold War 1970 fork''s validation (bundled static checker on changed or given files, plus the touched countries'' own tools/<country>_1970 validators) and summarize errors by category as file:line. Use only when the user explicitly asks to validate, e.g. "/validate", "run the validators". Args: "staged", "all", "strict", or paths.'
disable-model-invocation: true
---

Run this fork's validation and summarize the results. Upstream MD's
`tools/validation/run_all_validators.py` is **not in this repository**; the layers that
exist are in `.claude/docs/validation-pipeline.md`.

Supported arguments: `staged` (only git-staged files), `all` (whole mod tree),
`strict` (warnings fail), or explicit paths. Default: files changed on the branch.
Requested arguments: $ARGUMENTS

Steps:

1. Pick the file set:
   - paths given → those;
   - `staged` → `git diff --cached --name-only`;
   - `all` → no `--path` (scans `common`, `events`, `history`, `interface`, `gfx`, `map`,
     `localisation`; inherited MD findings will appear);
   - default → `git diff --name-only origin/main...HEAD` plus uncommitted changes
     (`git diff --name-only`).
   Keep only `.txt`, `.gui`, `.gfx` and `localisation/**/*.yml` files that still exist.

2. Run from the mod root, one `--path` per file (add `--strict` when asked):

   ```
   python -X utf8 .agents/skills/hoi4-validate-debug/scripts/check_hoi4_files.py --root . --path <file> [--path <file> ...]
   ```

   If `.agents/` is missing (it is git-ignored local tooling), say so and stop.

3. For each country prefix in the file set (`COLDWAR_<TAG>_...`), run that country's
   validators under `tools/<country>_1970/` (`validate*.py`, `check_*.py`) after reading
   their `--help`; skip any that rebuild loaded files unless the user asked.

4. Present results grouped by category: encoding/BOM, braces and quotes, localisation
   syntax (header, malformed, duplicate keys, colour codes), country validator findings.
   Show each finding as `file:line — description`.

5. End with a summary line: totals per layer, or "All checks passed", followed by
   "Static only: not tested in game or with two clients."
