# COLDWAR_CUB — isolated approval concept

Build design documents and a local preview only; no installation into game directories.

- content.py: canonical graph, effects, contracts, historical chronology.
- lifecycle.py: explicit initialization, replacements, expiry and no-replay requirements.
- build_concept.py: generated model, full effect matrix, native review excerpts and preview.
- native_font.py: reads the installed hoi_16mbs atlas without modifying it.
- audit_balance.py: compatible direct-modifier ranges; no whole-economy simulation.
- verify_preview.cjs: local headless Chrome QA and screenshots.

Run build_concept.py, audit_balance.py, then verify_preview.cjs from the repository root. Uses Pillow and the existing Codex Playwright runtime. VIS is the chat-owned preview location; change deliberately for a new chat. Script excerpts comment out new contract/refresh requirements and are not runnable game files. Runtime implementation and engine checks await user approval.
