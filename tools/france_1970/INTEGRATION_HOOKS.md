IMPERIA COLD WAR

# France 1970 integration hooks

The 1970 country history now selects `COLDWAR_FRA_1970_focus` only when `IMP_is_1970_scenario` is true and calls `COLDWAR_FRA_1970_initialize` immediately after loading that tree. Pompidou, the existing scenario equipment research, and the economic and labour setup remain in the history block.

The generic fallback effect routes France to its authored tree if the tree is missing, then exempts France in the 1970 scenario from subsequent generic or empty-tree fallback replacements. The `has_focus_tree` guard keeps repeated legacy fallback calls from resetting focus progress.

The existing exact subparty callback still invokes `FRA_update_party_programmes`. In the 1970 scenario this delegates to `COLDWAR_FRA_refresh_programmes`; outside that scenario, the existing modern France programme logic continues unchanged.

## Risks and follow-up

The France-specific effects and focus tree must be loaded under the exact names referenced here. The root integration owns their definitions and startup or weekly refresh scheduling. The generic fallback dispatcher is shared; its France exception is scenario-gated so other start dates retain current routing.