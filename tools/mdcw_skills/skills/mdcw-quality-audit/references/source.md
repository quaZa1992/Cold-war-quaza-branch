# IMPERIA COLD WAR — Cold War Quality Audit source and adaptation

Source: MillenniumDawn/Millennium-Dawn, commit `e1bb482ce492aa54e863d3c420f811f46054ea78`, retrieved 24 October 2026. Credit: the Millennium Dawn contributors. Individual authors of these instruction files are unknown in the reviewed snapshot.

Upstream repository licence: [CC BY-SA 4.0](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/LICENSE). This adapted instructional text is also offered under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). No endorsement is implied. This applies to this skill, not the mod, third-party game assets or unrelated installed skills.

Adapted for Codex, January 1970, Cold War multiplayer RP, the actual local toolchain and the current IMPERIA COLD WAR project standards. Claude tool/model declarations, automatic agent dispatch, upstream repository publication defaults and conflicting modern scenario rules are not imported. New wording and project-specific corrections were prepared with Codex assistance for Enes.

Reviewed sources:

- [.claude/agents/ai-debugger.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/ai-debugger.md), SHA-256 `df0fb27281c0206e75c9790326915a28053b5292ba3fc5c5c64979ab17199bb8`.
- [.claude/agents/bug-fixer.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/bug-fixer.md), SHA-256 `8631e56b02125e9439558934ac689f71a0b00a8ab6c17c6fbb4af22e37cd744f`.
- [.claude/agents/code-quality-reviewer.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/code-quality-reviewer.md), SHA-256 `570f7c1d1659bf68dd121e41f17df1c39e8eb27cc036779b39efd53e8233604f`.
- [.claude/agents/event-builder.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/event-builder.md), SHA-256 `5036ee9f3732265dda256f586c4603666c6ba8afc5a7de3d417be5cadd6bf5ca`.
- [.claude/agents/focus-tree-builder.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/focus-tree-builder.md), SHA-256 `d7c68ae4499bc4586dd4037b61fcda7e7073c7eaffc2a61e75e9f089e86b9cb2`.
- [.claude/agents/head-mod-developer.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/head-mod-developer.md), SHA-256 `47b20c2b95e5e21303af8ad51a063d173a268d8dc1461cce2579f8be1fbf6886`.
- [.claude/agents/localisation-editor.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/localisation-editor.md), SHA-256 `aeaa777862f1cdc113eecee0476f91c1a4cb2f27a4969f3a646cb050ec280d2b`.
- [.claude/agents/performance-analyzer.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/performance-analyzer.md), SHA-256 `51f668fb32555f80c6abdfd7ba013e15d8eda42389c1348d2655630b3096a342`.
- [.claude/agents/simplify-analyzer.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/simplify-analyzer.md), SHA-256 `9c7e2f835780eed0ffd48a024eb4413b9735299a107c7d2739f41953386504ba`.
- [.claude/agents/tools-reviewer.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/agents/tools-reviewer.md), SHA-256 `253bf70cc880f2c63e2c6eea9b362f4aa1d071f68cf47fecae91345353a3e4db`.
- [.claude/docs/agent-conventions.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/docs/agent-conventions.md), SHA-256 `498841e2913be8bdbeb96463cf3672d7907c9643ebf073a0a12e907c0a4d2461`.
- [.claude/docs/bug-patterns.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/docs/bug-patterns.md), SHA-256 `0f1037705ca4e06140fa7bb1b81b8c6abb261d30d9f5cd97d9b0b279e6e1fda1`.
- [.claude/docs/performance-patterns.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/docs/performance-patterns.md), SHA-256 `e0ccdb1dbe4d64394651a726608c41f6d3ef5b720a8aa47e9338896394a44996`.
- [.claude/docs/regression-test-scope.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/docs/regression-test-scope.md), SHA-256 `def2db5af06a34f7d78c355bc1df47b14908123ed3745fef5d5ad83c9a1df322`.
- [.claude/docs/un-system-reference.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/docs/un-system-reference.md), SHA-256 `29b47a546fc386a1057d660301e04c10719e4aaaa12896549418a0b86e56c6b2`.
- [.claude/skills/audit/SKILL.md](https://github.com/MillenniumDawn/Millennium-Dawn/blob/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude/skills/audit/SKILL.md), SHA-256 `c9dd5ce4bb56efc38372853f27207aba9c1d9944fe8e73edef59da113084ba9d`.
