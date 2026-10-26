# COLDWAR Northern Air Shield: native-mechanics review

Reviewed catalogue SHA-256: `bdbec679bbe773ec793cba69f68fc5d37f83e2730548c459f055f02a2975fd34`.

Inputs: `COLDWAR_USA_GULF_CONCEPT.json`, `COLDWAR_AIR_SHIELD_IDEAS_SPECIMEN.txt`, and the corresponding authoring entries in `tools/iraq_1970_concept/usa_gulf.py`. This is a bounded static review of the new air package; the resistance extension is covered separately in `MECHANICS_REVIEW.md` and `RESISTANCE_MECHANICS_RESEARCH.md`. No loaded mod file was changed and no engine test is claimed.

## Supported native payloads

Both emitted country-idea definitions use real modifiers with appropriate country application:

| Recipient | Native modifier | Value | Meaning and scope |
| --- | --- | --- | --- |
| USA | `air_intercept_efficiency` | 0.15 | Interception mission efficiency for actual US aircraft |
| USA | `air_superiority_efficiency` | 0.10 | Air-superiority mission efficiency for actual US aircraft |
| USA | `airforce_personnel_cost_multiplier_modifier` | 0.15 | Higher native US air-force personnel spending component |
| Existing, consenting KUR/PUK | `cas_damage_reduction` | 0.25 | Additional damage reduction against CAS for recipient forces |
| Existing, consenting KUR/PUK | `enemy_army_bonus_air_superiority_factor` | -0.20 | Reduced enemy air-superiority effect on recipient divisions |
| Existing, consenting KUR/PUK | `army_personnel_cost_multiplier_modifier` | 0.05 | Higher recipient army-personnel spending component |

These are national modifier inputs. They do not restrict Iraqi flights, affect only northern territory or only an Iraqi enemy, create aircraft, or guarantee a particular battle result after all other modifiers and engine caps. The exact interception key is `air_intercept_efficiency`; the invalid `air_interception_efficiency` is not used in the emitted definitions.

Source evidence, relative to main MD `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`:

- `common/ideas/05_Australia.txt:440–441` and `05_china.txt:823–824`: interception/superiority efficiency.
- `common/ideas/free_states_of_america.txt:550–551`: the combination of negative enemy air-superiority effect and positive CAS reduction.
- `common/ideas/Iraqi.txt:1664,1674`: CAS reduction in native Iraqi ideas.
- Workspace `common/modifier_definitions/money_modifier_definitions.txt:23–41`: army/air-force personnel financial modifiers; workspace `00_money_system.txt:3182–3195` reads them into their respective native personnel components. The values are additive within the relevant multiplier, not fixed dollar bills or increases to every military expense.
- Primary installed-game `documentation/modifiers_documentation.html:1658–1666,1753–1771,2223–2226,2540–2543`: registered keys and categories. CAS reduction and enemy air-superiority modifiers are not state-category geographic protection effects.

## Expiry, acceptance and basing

The USA completion payload uses native `add_timed_idea` for 90 days, documented in the installed game's `effects_documentation.html:2018–2038`. The separate recipient-scope acceptance payload also grants 90 days. The recipient idea's native `cancel` checks that USA exists and still has the readiness idea, and that the recipient is not at war with USA. Thus a late acceptance does not survive an actual end of sponsor readiness merely because its own timer has time left. Native cancellation evaluation timing still requires engine validation.

Accepted basing uses `USA = { diplomatic_relation = { country = TUR relation = air_base_access active = yes } }`. This matches the guest-USA pattern in installed vanilla `common/national_focus/philippines.txt:3936–3940`; main MD `events/UN_Voting_Events.txt:1885–1889` demonstrates the host-side `offer_air_base_access` equivalent. Actual host consent must precede the effect; choosing another host must change the target. This is distinct from ground military access. Aircraft capacity, range and normal hostile-war/mission rules remain necessary; no automatic peacetime interception is promised.

No recipient country means no recipient idea. The USA package still affects its actual aircraft, and recipient cover can be offered after a valid actor appears. The rejected fixed $0.10bn weekly patrol bill is absent; the replacement increases actual native personnel expenses.

## Lifecycle findings closed in this revision

1. **Access-loss behavior is explicit:** the focus rewards, management decision and persistence rule now describe earned readiness/liaison training and its personnel costs continuing to expiry or explicit USA withdrawal after host access loss. Actual basing follows native diplomatic access. No unverified access observer or automatic idea cancellation is promised. Withdrawal explicitly removes both the USA idea and current KUR/PUK cover ideas; native recipient cancellation remains a backstop.
2. **Renewal has an exact replacement contract:** the focus payload and management decision now specify `remove_ideas` followed by `add_timed_idea` with `days = 90`. Renewal requires a continuing crisis and fresh host consent; each recipient must accept again before its own remove/add sequence. This avoids relying on undocumented repeated-application duration behavior and prevents stacked copies of these packages.

The bounded static review passes with both findings closed. The native modifier/basing replacement and the revised lifecycle contract are supported by the cited APIs. Event, decision and diplomatic consent wiring remains review-only; native cancellation evaluation, save/load, recipient late acceptance, renewal and host revocation require subsequent engine validation when implementation is approved. This does not change the separately documented requirement for new resistance/uprising integration.
