# IMPERIA COLD WAR: Israel V2 focus-only content review

Independent review dated 28 October 2026. Reviewed `tools/israel_v2/focus_actions.py` and the regenerated 213-focus `tools/israel_v2/design.json`, SHA256 `f11d49aab12b44f9ecb20d576a1850d95046be3e7148b0a5b5127358ad5979fd`.

Scope: the design proposal and its preview data. No loaded mod file was edited or tested. National-focus lifecycle records describe required future implementation, not a working runtime. The historical precedents support country relationships and institutions; numerical contracts remain authored game balance.

## Final corrections confirmed

- `ISR2_irrigation_exports` now uses the same fixed $0.00600 billion invoice for both countries, Israeli setup of $0.00200 billion and maintenance of $0.00002 billion weekly for 104 weeks. The full-term margin is $0.00192 billion before other national costs. Country GDP differences no longer turn the proposed commercial sale into an unintended Israeli subsidy.
- All four `ISR2_close_*` focuses distinguish normal weekly expense removal of 0.015% GDP plus the optional 0.005% network supplement from discounted removal of 0.012% plus 0.004% under the 20% maintenance discount. These are reductions of the actual expense, not new permanent income.

## Important design guards retained

There are zero decision-unlock rows. Mafdal's three land appropriations, reserve exercise/call-up/release, two Sapir tenders, the two Gahal matched appropriations and regional settlement actions occupy concrete focus cards. The Mafdal service continuation accepts any of its three exclusive land choices through an OR prerequisite.

Each diplomatic offer names its country and sends an acceptance/refusal event directly. Both participants' full prospective numerical Effects remain visible. Pending and active agreements prevent duplicate offers; 104-week agreements have 104-week renewal cycles. Gahal and HaOlam service agreements share a replacement family. Resending an offer does not itself grant rewards or charge setup.

Controlled and uncontrolled settlement actions use separate availability rules, with common area-tier limits, Palestinian-pressure attribution and freeze reasons across national and party projects. Closing sponsorship is restricted to a funded foreign foothold outside Israeli control. It cannot delete the security costs or pressure consequences of productive controlled sites whose buildings remain. Reopening appropriations removes both applicable freeze benefits before enabling new projects. Unilateral settlements retain adverse host consequences without requiring host or Palestinian consent.

Private matching contributions remain actual financing requirements. Guarantee reserves are separate from administration expense and included in gross claim limits. Reopening a focus does not reset children, one-time building receipts or debt. The existing native `uncomplete_national_focus` provider was inspected in `common/scripted_effects/99_ENG_scripted_effects..txt` around line 956; country-specific timers and execution guards are still proposed integrations.

Workforce remains exactly three +5% reforms, totalling +15%, with no negative workforce modifier. Targeted final assertions passed for the contract arithmetic, discounted closures, offer recipients, long agreement cycles and workforce cap. The preceding graph review found no missing predecessors, empty Effects or node impossible in every prerequisite/exclusion selection for the six expanded political programmes. These are static design checks, not engine or multiplayer results.

## Evidence for the fixed counterparties

- **Kenya, MASHAV:** the [Israeli Embassy's bilateral chronology](https://embassies.gov.il/kenya/en/the-embassy/bilateral-relations) dates the first Kenyan trainees to 1965. This is an official retrospective, not proof of the exact proposed mission.
- **Ethiopia, technical assistance and irrigation:** [JTA, 27 September 1960](https://www.jta.org/archive/israel-ethiopian-ties-to-be-strengthened-joint-enterprises-planned) reports contemporary water, irrigation and technical-training cooperation. The new invoice and productivity package are RP proposals.
- **Uganda and Congo-Kinshasa, equipment contracts:** [JTA, 8 May 1969](https://www.jta.org/archive/israels-aid-to-african-countries-has-had-mixed-results-washington-post-reports) reports contemporary training/arms assistance. The fixed stock-based orders are new offers. Congo-Kinshasa means `DRC`, not Congo-Brazzaville or a backdated Zaire identity.
- **Romania, civilian workshops:** the [Israeli Film Archive's 1969 trade-agreement newsreel record](https://jfc.org.il/en/news_journal/60675-2/102167-2/) supplies contemporary commercial context. The specific workshop agreement remains a plausible new policy.
- **Iran and Turkey, limited signals liaison:** the [CIA's March 1979 study](https://nsarchive2.gwu.edu/NSAEBB/NSAEBB407/docs/EBB-PollardDoc1.pdf) retrospectively describes intelligence cooperation from 1958. The proposed limited contract is a new RP extension, not automatic Trident membership or a prescribed intelligence operation.

No material content-review blocker remains within this reviewed focus-only proposal. Implementation must still deliver the stated transactions, consent, counters, expiry and reopening behavior. This review does not certify native gameplay or resolve the separate MD-update runtime issue.

Provenance: original IMPERIA COLD WAR review by Codex. Historical documents remain credited to their originating authors and archives. No third-party artwork or historical text was incorporated as a mod asset; third-party reuse permissions were not established.
