# Approved Iraqi reward revision: integration contract

Implemented by `audit_rewards.py` as a pure transformation of a caller-owned deepcopy of the immutable approved catalogue. This module never writes loaded files, runs a compiler, removes nodes, alters prerequisites, positions, starting spirits or country/party gates. `apply(data)` returns the same data object, is idempotent and sets `audit_rewards_revision=2026_10_19_v1`.

The parent integration must consume this transformed data in **every** generator that owns focus, programme, availability, decisions, previews or save recovery. The original JSON remains the old-save reference, not the new reward source. A raw read of that JSON after transformation would silently restore the rejected values.

## Exports

- `RETIRED`: eleven old IDs to survivor IDs. The root keeps the426IDs as hidden empty save stubs and performs graph splicing. Entry retirement targets are identifiers, not permission to add a Heavy prerequisite to Light. `REPLACEMENT_CANDIDATES` records alternative entry branches.
- `DESCRIPTIONS`: polished English narratives for changed substantive focuses. Merge these **after** the existing flavour loader. Inspector and queue prose must not become focus narrative.
- `BONUS_LOCALISATION`: unique native research/doctrine bonus names. It is populated by `apply`; merge into English localization after calling it. Different category bonuses use separate names so the College's50%Construction and25%Industry cannot overwrite each other.
- `MERGED_SOURCES`: retired delivery sources folded into survivors.
- `data.audit_retired_rewards`: complete historical source payloads, quoted/implemented flag names, invoice variable, old share and decisions. This preserves real paid assets and old money; it does not grant anything.

## Fresh game rewards

All six pairs use the consolidated AUDIT.md tables, including the final conservative military values. Heavy/Light and Oil Revenue/Diversification each move their one existing downstream building into the selected headline package. The retired building focus must not grant another copy. Staff Training gives35ArmyXP,one25%land_doctrine cost reduction and retains+4%training time; its+3%organisation is removed. It does not gain the20XP alternative suggested only for a retained defence_accounts entry. State organisation remains unchanged.

Industry Maintenance absorbs Quality Inspection:35days,2%GDP,+8%efficiency growth,+2%efficiency cap,-1%military factory output,+2%bureaucracy. Oil engineering becomes one35%Industry research use with existing+2%efficiency growth and2%GDP. Refinery Operators merges into Baiji: Baiji retains its+6%fuel/+2%bureaucracy and gains+2%efficiency growth, while Operators' generic+1%research is removed. Baiji's existing3%GDP remains; the separate1.5%Operators fee disappears.

**1970 category check:** the native CAT_fuel_refining category is valid but its earliest actual technology in this checkout is1990. Giving it to the early Iraqi engineering focus would have little immediate value. The module therefore uses native CAT_industry, which has real1960/1970/1975extension targets, for the approved bounded oil-engineering research milestone. Construction and aircraft bonuses also have1960–1975targets. This changes no technology or research-tree file and adds no ahead-of-time exemption.

Industry inspection and the existing investment-reallocation decision move to both Heavy and Light. Social-coverage revision moves to Schools and Skills. The two former49-day review-only finales retire. Their actual decision handlers/availability must still read the transformed catalogue. Sustainable Readiness retains its focus and grants25one-timeArmyXP alongside its decision; the recurring cycle itself grants no XP.

The readiness **catalogue** and embedded focus-decision data become0.5%GDP,+4%organisation,+4%recovery,+4%army personnel for90days,180-daycooldown. The separate `decisions_module.py` actual native idea/quote/paid effect must receive the identical values; this module cannot patch that other owner's implementation.

## Distinct party finales

The audit approved replacing the ten repeated+3%Stability/-2%PP finales, but did not prescribe every replacement institution's number. The following modest direct programme packages implement that instruction, preserve all actual party/leader ownership and existing decisions, and never substitute coalition membership for governing authority:

| Focus | New outcome |
|---|---|
| Negotiated Succession |21days; no generic modifier; keeps the real consent/eligible-successor decision |
| The Socialist Republic |+5%military factory output,+3%social expenditure |
| The Party Mandate |21days;+3%tax collection,-4%bureaucracy; keeps actual leadership-renewal vote |
| A Civilian Mandate |+6%tax collection,-3%bureaucracy; retains policy revision |
| Constitutional Charter |+8%foreign influence,+2%bureaucracy |
| A Common Republic |army personnel costs-5%,bureaucracy+3%; selected northern constitutional form retained |
| A Federal Mandate |+8%efficiency growth,+2%social expenditure |
| The Islamic Cabinet |+4%research,+3%social expenditure |
| SCIRI Governing Mandate |+3%organisation,+4%army personnel costs |
| IIP Renew the Mandate |+6%efficiency growth,-2%tax collection |

These values are explicit implementation choices within the approved institution-level rework, not newly discovered historical percentages. No other party programmes can simultaneously contribute to the compatible Saddam routes. The root's structural work must enforce any relevant **existing real northern settlement**, accepted constitution or succession contract before narrating one as implemented. No foreign state, treaty or cabinet consent is invented here.

State Compact explicitly becomes bureaucracy-6%,tax+4%. Baath Future keeps+3%PP and gains one25%Industry research use instead of+2%bureaucracy. The starting-patronage relief and other starting-spirit reform stages remain untouched.

## Save migration and one-time atoms

Each changed survivor has `audit_delivery_components`. Each component has:

- `kind`: building,army_xp,literacy or instant;
- `receipt`: unique COLDWAR_IRQ flag for the revised component;
- `legacy_sources`: survivor and merged old delivery IDs;
- `legacy_amounts`: numerical credit **only if that source's old implemented receipt is true**;
- building:[state,type,count], amount:<XP/literacy> or instant:[native effect blocks].

XP and literacy credits are partial, not booleans. Old Staff Training's15XP means the new35XP package owes20XP. Old Mass Literacy's0.025 means the0.06package owes0.035. Literacy is one atom containing the temp variable and native update call together. Never guard the setup and update separately or replay the original amount. An old Steel/Consumers/Export-Terminals/Industrial-Fund implemented receipt credits one matching state/building level. New research/doctrine/air-XP atoms have no historical credit.

The complete n.building/army_xp/instant fields remain the fresh-game payload and native reward preview. Root execution must guard components individually and mark each delivered component once. UI effect_tooltip remains non-executing. A migrated old survivor being implemented does **not** imply its newly added research/XP was already received; offer the revision through an explicit pending upgrade without repeating the old physical grant.

`audit_legacy_cost_credits` identifies exact historical invoice variables and flags. Freeze max(new approved invoice minus actually paid applicable old invoices,0) as a new upgrade top-up once; no cash refund if the old two-focus route cost more. Paid old invoices may only be used once. A quoted but unimplemented old source is **not** a paid cost credit or completed delivery. An old survivor's persistent policy reward should not require repaying its whole old fee after loading. An old completed focus lacking an implemented receipt follows the normal pending recovery, not an automatic free reward.

Root must suppress retired queued projects and retire old programme contributions without deleting historical economic facts. It must also avoid any separate pending upgrade for an undiscovered opposite branch: previous payment/delivery facts and the selected native mutual path remain authoritative.

## Verification

Run `python tools/iraq_1970/test_audit_rewards.py`. Twelve source/data checks cover immutable input/idempotence, untouched graph/startup contracts, exact consolidated costs/assets, conservative army values and compatible route sums, partial credits, native research/doctrine payloads, actual1970technology consumers, decision movement, readiness data, distinctive finales and unique receipts. They execute no loaded game file or broad generator and write no test report. This is not an engine tooltip, campaign affordability or multiplayer verification.

## Additional full-audit implementation: rural credit, accounts and concession

The state-account recommendations are exact: Courts Budget35days,1.5%GDP,+5%tax,+2%bureaucracy; Budget Accounts0.5%GDP,+4%tax,-3%bureaucracy, replacing its oldPPpenalty. Industry titles are exactly Basic Industries First and Consumer Expansion.

Cooperatives and cooperative credit become49days/4%GDP,+12%agricultural productivity,+3%bureaucracy and one native agriculture_district in Wasit1141. This moves the **existing** Wasit district into the priority programme. Retire agri_cooperative_credit and agri_wasit; the latter is a historical building-credit source, not another grant. Old Wasit's later large-irrigation prerequisites must be spliced by the root so a surviving shared node never forces the opposite first credit policy. Smallholders and smallholder credit become35days/2.5%GDP,+8%agricultural productivity,-2%relative consumer-goods factor,+2%social expenditure. Retire agri_smallholder_credit. Dhi Qar's existing district is unchanged. These numeric rural packages operationalise the qualitative approved audit conflict; they are balance implementation choices, not historical measurements. The actual building type is registered in common/buildings/00_buildings.txt, and its existing Wasit delivery is copied rather than invented.

Accepted Concession Delivery now also builds one infrastructure in171 and gives one25%Industry research use, preserving its existing export/influence/bureaucracy values and actual accepted-concession condition. **Its focus invoice remains zero:** the existing recipient-owned concession acceptance charges Iraq1%GDP and transfers that fee toENG. The parent corrected the earlier2%assumption and confirmed retaining the real original1%contract price, without any additional focus charge. New assets are delivered only after the accepted actual contract; they are never fabricated on refusal. The new components have no historical delivery credit because they did not exist before. Root owns the proposed90-day nationalisation marketing adjustment and must gate it to a genuinely new ownership delivery, never a backfilled research upgrade. Ownership/control/capacity must be checked before the contractual money transfer as well as before asset delivery, preserving the old recipient-owned acceptance guards.

The focused suite now contains14tests, including native building registration, old agricultural-building credits, unchanged Dhi Qar content and actual concession acceptance without duplicate focus charges.

## Final procurement priority implementation

Soviet Standardisation now gives supply consumption-10% (previously-4%), retaining foreign influence-3% and2%GDP. Mixed Supply removes its old+3%factory efficiency cap, retaining supply consumption+3% as its logistical cost and2%GDP, and grants one35%CAT_aircraft research use. The actual category has1960–1975consumers; no automatic aircraft, foreign equipment or mission is created by taking this priority. New English narratives explain common-standard dependency versus specialised capacity and heterogeneous stores.

The separate actual recipient-owned SOVadvisory offer is unchanged here. The parent assigned the additional first-acceptedFRA/ENGmission reward (one25%Artillery research use, programme-wide once) to the political contract owner; it is not granted early by this focus transform. The focused reward suite now contains15tests.

The previously audited conservative organisation/recovery/training/personnel route numbers remain unchanged. A route choosing Soviet Standardisation now has six more supply-consumption modifier points of reduction; all generic programme bonuses remain subject to existing party/leader/selected-policy eligibility. No new hidden bonus cap is introduced.
