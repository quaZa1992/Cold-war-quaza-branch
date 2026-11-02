---
name: mdcw-standardize
description: Standardize or reformat specified IMPERIA COLD WAR script files while preserving their semantics, generators, project markers, encoding and upstream attribution. Use for requested formatting/convention work, not automatic broad cleanup.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Semantics-preserving standardization

Read `AGENTS.md`. Establish the requested files and formatting scope, their current worktree state, canonical generators and output consumers. Do not classify every file containing the word focus as a national focus file.

Check whether the relevant upstream standardization tool is installed. `tools/standardization` was absent during adaptation. If a tool exists, inspect its implementation, help, write behavior and defaults before running it. It may rename IDs, insert logs or change conditions rather than merely format text.

Use a dry run or a contained copy when a formatter's behavior is uncertain. Compare parsed structure before and after, preserving prerequisite groups, duplicate-key semantics, code order where significant, party gates, random weights, transaction receipts, unit values and dynamic interpolation. Do not sort away ordered native constructs or flatten conditional branches for appearance.

Preserve original IDs and all external callers unless renaming was requested. Never delete project comments or upstream notices under upstream AI's zero-comments convention. Put the required IMPERIA COLD WAR marker at the file beginning, with mandatory syntax exceptions. Scripts remain UTF-8 without BOM; localisation alone uses BOM.

For generated content, make the durable change in the emitter and rebuild only the relevant outputs after confirming overwrite scope. Do not rewrite unrelated countries, immutable approval snapshots or archived source just to satisfy a formatter.

Review the resulting diff for semantic changes and noise. Run appropriate parser/encoding checks; add behavioral tests only if the transformation actually risks behavior. Report what was standardized, whether gameplay changed and any unresolved tool limitations. Do not automatically commit or publish formatting work.

Source and adaptation: [references/source.md](references/source.md).
