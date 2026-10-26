# Political integration and transaction review

Implementation source: `tools/iraq_1970/decisions_module.py`. Pure extension `extra_focus_decisions(data)` is called by the audit loader; `generate()` consumes that same loader. This report concerns the current revision, not the unchanged historical catalogue.

## Political operation

- **Before ICP accession:** The Communist Question is available under the incumbent Baath or an actual ICP government. It opens legal-activity and Front negotiations or a paid independent organization campaign. A Front agreement legalizes the ICP and adds the appropriate partner to native `gov_coalition_array`. It neither replaces `ruling_party` nor grants ICP/leader programme receipts. Independent organization costs 0.5% GDP, supplies native +2-point party/outlook inputs, and has a protected 180-day cooldown.
- **Current constitutional contract:** Executive/representative authority is selected from the first actual chosen constitutional policy. A selected policy takes precedence over ambiguous old receipts. A start-accessible conference can revise authority at 1% GDP and 100 PP. Once explicitly bound, daily reconciliation cannot overwrite it. Earned packages remain recorded; root programme eligibility uses the exported constitutional predicates. A government change does not impose a lifetime party ban.
- **Front versus monopoly:** The Front's active programme requires maintained legal and native coalition rights. A funded labour charter costs 1% GDP and gives +5% production-efficiency growth / +2% social costs for 180 days. Party mobilization instead gives +5% political-power gain / +2% bureaucracy costs for 180 days at 1% GDP. Their conditions exclude simultaneous operation. Leaving the Front, removing its coalition partner or breaking guarantees removes its current charter benefit. The entry focus can unlock negotiation before agreement; its active government bonus waits for the contract.
- **Guard/general-staff priority:** A paid 1%-GDP review changes only the already reached current priority and its earned programme flags. It does not call a focus-apply helper or repeat original experience, equipment, research or buildings. The actual distinct Guard/regular-army national packages are owned by the approved reward revision.
- **Readiness:** Exactly 0.5% GDP, 90 days, +4% organization / +4% organization recovery / +4% army personnel cost, 180-day cooldown. There are no repeatable XP grants.

## Northern contract

The generic Baghdad route unlocks after Northern Talks; actual ICP/KDP/PUK negotiation providers also access the same contract. A live respected autonomy settlement and Iraqi ownership/control of Kirkuk are required.

Revenue-sharing ratification costs 2% GDP, applies −5% central tax-revenue multiplier / +2% bureaucracy costs, and selects the existing broader federal northern-relief stage. Central administration with accepted local guarantees costs 2% GDP, applies +3% army personnel / +1% bureaucracy costs, and retains the existing narrower autonomy-relief stage. It grants no extra central tax income.

Where Kurdish states exist, each existing KUR/PUK government receives its own response and all must agree. No payment or replacement occurs before all required consent. Where neither country exists, domestic delegates explicitly accept or reject. War, expired consent, lost Kirkuk control and invalid positive quotes block execution. An accepted but temporarily unaffordable offer waits for the original quoted payment; the later treasury change cannot reprice it. Old ratified federal/local settlements migrate to the corresponding current ongoing cost without receiving assets.

The revenue-sharing cost is a native central-retention abstraction. It is **not** an authored matching recurring payment into another country's treasury. No territory, cores, units or free money are granted by fiscal ratification.

## Procurement and economic priorities

The diversified-supplier branch offers real recipient-owned French/British advisory negotiations. The first paid and accepted mission gives one 25% artillery research bonus; a permanent delivery receipt prevents duplicate callbacks or a second supplier replaying it. The advisory upkeep and duration use the existing native mission. A dispatch or refusal grants nothing. Soviet standardization's headline logistics improvement and mixed supply's aircraft research are owned by the reward revision.

Rural-credit and oil-revenue allocation reviews replace current priority flags at 1% GDP without replaying the respective original physical deliveries. The oil review covers only export-revenue emphasis versus non-oil development; it does not reverse nationalization or create concession rights. Existing concession acceptance retains its actual native 1%-GDP contractual fee and no additional focus fee. Existing machinery, counterpart acceptance and later implementation conditions remain authoritative.

## Source and save contracts

- Decision eligibility uses the audit loader's alternative `audit_providers`, rather than requiring a now-retired review/root focus.
- `POLICY_CONTRACT_GATES` is for current constitutional eligibility. `PROGRAMME_CONTRACT_GATES` additionally holds the Front/monopoly live-contract conditions. The latter must gate active programmes without creating a negotiation-unlock deadlock.
- `reconcile_political_contracts` never calls the programme reconciler; the root calls it before computing current programme totals.
- `decision_event_ids.json` froze all 115 old event IDs and their source hashes before compilation. Existing titles/explicit aliases retain their IDs; fourteen new events have reserved IDs 10000–10013. Inserting an unregistered event fails generation rather than shifting saved callbacks. Event options still recheck current authority before payment/delivery.

## Validation boundaries

`test_audit_politics.py` executes freshly generated effects/events with strict authority, consent, treasury and native-call boundaries. It covers pre-accession rights, stale callbacks, exact costs, both northern recipients, refusal/expiry/war/control failures, deferred payment, zero GDP, current contract replacement, coalition cleanup and one-time research.

`test_audit_transactions.py` separately imports the actual compiler without writing outputs, generates focus/programme/queue sources and executes those fresh reward/migration bodies. It covers fresh Heavy delivery, historical partial/full investment credits, incremental research/XP/literacy, supplementary quotes and current country/party/capacity/cash guards. Native research, building and literacy APIs are recorded calls; these tests do not prove their complete engine behaviour, tooltip rendering, technology usability or multiplayer networking.

Latest executed checks: **18 political scenarios and 14 fresh compiler transaction scenarios passed**. The existing fifteen decision/credit scenarios also passed using the extended political interpreter. The migration review found and root corrected two concrete issues: an unpaid old positive quote needed a once-only conversion to the new bundle using its original implied GDP; already repaired saves needed current decision-unlock metadata restored by the new revision. Historical financing credits now subtract actual recorded paid invoices, not an invented percentage of a later, larger GDP. A GDP20 Heavy upgrade with an actual historical payment of 0.2 therefore quotes 1.0 − 0.2 = 0.8, frozen at inspection. Research additions to already financed/delivered programmes remain free where the revision defines them as balance upgrades.
