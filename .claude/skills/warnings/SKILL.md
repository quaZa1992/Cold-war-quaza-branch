---
name: warnings
description: 'Print the complete, untruncated list of findings from the Cold War 1970 fork''s static checker, optionally filtered by severity, folder, or message text. Use when the user asks for all warnings/errors, e.g. "/warnings localisation errors", "/warnings common/decisions bom". Args: optional folder or file, optional "errors"/"warnings", optional message filter, optional "staged".'
disable-model-invocation: true
model: haiku
---

Print every finding the static checker reports, with no truncation. `/validate` remains
the command for a summarized run. Upstream MD's per-validator JSON sidecars do not
exist here; the checker prints every finding as one line, so this skill runs it and
filters its output.

Requested arguments: $ARGUMENTS

Grammar (all optional, order-independent):
`[folder-or-file] [errors|warnings] [message filter words] [staged]`

## Step 1 — resolve the scope

- A path (anything with `/` or a known top folder: `common`, `events`, `history`,
  `interface`, `gfx`, `map`, `localisation`) becomes `--path <it>`. Several are allowed.
- `staged` → one `--path` per staged `.txt`, `.gui`, `.gfx` or `localisation/**/*.yml`
  file from `git diff --cached --name-only`.
- No path and no `staged` → the full default scan. Say it will include inherited MD
  findings.
- Remaining words (other than `errors`/`warnings`) are a case-insensitive message
  filter, for example `bom`, `duplicate`, `malformed`, `colour`, `brace`.

If `.agents/skills/hoi4-validate-debug/scripts/check_hoi4_files.py` is missing, say so
and stop.

## Step 2 — run and filter

```bash
python -X utf8 .agents/skills/hoi4-validate-debug/scripts/check_hoi4_files.py --root . [--path ...] > "<scratchpad>/warnings.txt"
python -X utf8 - "<scratchpad>/warnings.txt" "<severity or empty>" "<filter or empty>" <<'PY'
import collections, re, sys
p, sev, flt = sys.argv[1], sys.argv[2].upper(), sys.argv[3].lower()
rows = [l.rstrip("\n") for l in open(p, encoding="utf-8") if ": ERROR: " in l or ": WARNING: " in l]
if sev: rows = [r for r in rows if f": {sev}: " in r]
if flt: rows = [r for r in rows if flt in r.lower()]
kinds = collections.Counter(re.split(r"[:;']", r.split(": ", 2)[2])[0].strip()[:60] for r in rows)
print(f"TOTAL {len(rows)}")
for k, n in kinds.most_common(): print(f"{n:6d}  {k}")
print()
for i, r in enumerate(rows, 1): print(f"{i}. {r}")
PY
```

The last line of the raw file (`Checked N files: E errors, W warnings.`) is the
unfiltered total; report it too.

## Step 3 — present

Copy the filtered stdout through verbatim inside one fenced block.

- Lead with the total, the scope and filters used, and the current branch.
- **Never truncate, summarize, sample, re-order, or re-word a line, and never write
  "and N more".** A long list stays long.

Then state these caveats:

- The checker is a preflight: encoding, brace and quote balance, localisation syntax.
  It does not check scopes, references, or engine behaviour.
- Inherited MD files produce findings unrelated to the branch; compare against a run on
  `origin/main` before treating them as new.
- Counts drift with the worktree; report the count from the run just performed.
- Say so explicitly when `staged` or a path filter was applied, so a short list is not
  mistaken for a clean repo.
