# IMPERIA COLD WAR: MD 2.0.3 update implemented

Implemented after the user approved the recommended proposal on 28 October 2026. The short interruption concerning national tactics was explicitly withdrawn and caused no content change.

## Actual changes

- Updated the mod descriptor, portable launcher descriptor and actual external launcher descriptor to version 2.0.3. The MD Cold War identity, supported game-version range and custom replace paths are retained.
- Synchronized existing frontend version labels without generating new translations. Localisation retains its BOM and project marker position.
- Updated eleven existing description version lines to 2.0.3 and removed their fixed upstream MD checksum claim. The source descriptions still contain stale 2.0.0/2.0.1 labels and the MD-specific 8751/ccc6 checksum values; these were not misrepresented as this custom mod's verified checksum. This corrects the initial proposal's overly broad description of these fields.
- Adopted the supplied short upstream update note with explicit provenance. Its inherited v2.0.2 heading is identified as source text.
- Removed exactly twelve already empty auto-agency compatibility files. No active queue implementation was deleted by this transaction.
- Updated the README base version and root provenance notice. The two source-folder Egyptian development PNGs were excluded.

There are 26 updated repository files and twelve empty-file removals, plus the one external launcher update. No national focus, game effect, trigger, map, GUI implementation, economy formula, equipment definition or artwork was replaced. The technical MD 2.0.3 changes were already present alongside the Cold War additions before this finalization.

## Complete comparison and preservation

A fresh raw SHA256 pass reread all 79,711 files in the supplied Workshop folder and found no change since the individually reviewed source. The original MD inventory and current source differ at exactly 73 paths even when raw bytes, rather than normalized text, are compared. These comprise 59 changed existing files, twelve removed files and two development image additions. No additional formatting-only source changes were hidden by the normalized comparison.

The full post-implementation pass verified 98,728 installed files. Exactly 98,702 files retain their original bytes. Every difference is listed in implementation.json; unexpected differences: zero. Our research, uranium, Space Race, SSR, country content, settlement programmes and other authored mechanics are retained.

The comparison is against the exact local MD folder supplied by the user and the archived original MD source used for the prior migration. It is not a claim that Steam cannot publish another update, nor certification that every source-folder artifact belongs to a pristine public GitHub release. Private caches/Git metadata/audit outputs are explicitly excluded; asset junction aliases are not traversed. Actual loaded asset directories were included.

## Verification and limits

- Full upstream hash recheck and complete installed-file preservation: PASS.
- Exact metadata transactions, mod identity, paths, localisation encoding and removed empty files: PASS.
- Existing Israel content/reference/integration checks: PASS. Settlement-presence model: 341 checks. Palestinian pressure model: 867 checks.
- Native game: the isolated test reached January 1970 startup but failed before its day-three checkpoints. The engine produced a crash report. See native_report.json and FOLLOW_UP_VERIFICATION.md. Full runtime compatibility is not certified.
- Manual hover/UI operation, save/reload, first-month and multiplayer checks remain unperformed for this update. Source preservation is not substituted for those tests.

## Recovery and provenance

Original affected files and the external launcher were backed up before writes to `E:/MDColdWar_Backups/Codex_Test_Archives/MD_203_before_update_20261028_174132_730209.zip`. The archive hash and every before/after file hash are recorded in implementation.json. Original audit inventories remain unchanged.

Existing Millennium Dawn and Cold War/Imperia credits and licences remain in effect. No artwork was modified. Individual third-party authors or separate permissions remain unknown where not identified by the inherited source. The implementation tooling and this English report were authored for IMPERIA COLD WAR with Codex.
