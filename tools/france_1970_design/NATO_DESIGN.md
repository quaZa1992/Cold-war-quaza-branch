IMPERIA COLD WAR

**Historical revision 1.1 note.** Its fixed prices and reward table are superseded by `GDP_REWARD_REVISION.md` and current `concept.json` revision 1.2. The original policy structure and coordinates remain unchanged. Current monetary terms and building/slot rewards are shown in the regenerated preview and `FOCUS_CATALOGUE.md`.

# Gaullist NATO strategy: concept extension

Status: unapproved design and external preview only. No replacement tree, decision, spirit, party gate or budget reader is installed in the loaded mod.

The requested extension adds **18 focuses, seven exclusive pairs and four bilateral programmes**. The complete French concept now has **152 focuses, 14 sections, 46 exclusive pairs and 19 offers**. This is a UDR sub-tree using the same exact native slot-1 requirement, not another political party. Every NATO focus also requires `NATO_member` in availability, reward guards and programme activation.

## Historical boundary

France is a NATO treaty member in January 1970 and retains Article 5. Its 1966 withdrawal concerned integrated military command. National command, independent nuclear decisions and alliance membership are separate. Existing Ailleret-Lemnitzer arrangements are historical starting context; new offers finance additional cooperation rather than retroactive approval of an existing treaty.

All three strategies retain membership and French authority over the deterrent. They allocate a discretionary programme rather than claiming France historically had to choose between every form of autonomy, exercise and European cooperation. No German or British acceptance speaks for the entire Alliance, assigns forces to an integrated command, transfers nuclear authority or grants basing rights. The later Ottawa, Valentin-Ferber and Franco-German defence precedents are identified as later developments.

Primary historical sources: `NATO_HISTORY.md`. Exact native providers and the old `FRA_distance_nato` cancellation inconsistency: `NATO_MECHANICS.md`.

## Structure and trade-offs

The entry follows **Gaullist Majority**. First choose **National Nuclear Veto** or **Nuclear Consultation**. The veto programme costs 40 PP, grants +5% Political Power Gain and adds +2% to the recurring equipment bill. Consultation costs 40 PP, grants one 25% land-doctrine reduction and +3% Foreign Influence, with -3% Political Power Gain. Consultation retains the final French decision and does not entail NPG participation or nuclear sharing.

| Exclusive strategy | Direct outcome | Internal choice and continuation |
|---|---|---|
| An Independent Ally | Treasury -$0.100 billion; Foreign Influence Defence +5%; Equipment Cost Multiplier +2% | Fund National Land Forces: Factory Output +4%, equipment bill +3%; or National Sea Power: Dockyard Output +5%, navy personnel bill +5%. Each costs $0.150 billion. A further $0.150 billion funds one 50% armour/naval research use and one 25% corresponding doctrine reduction. |
| Selective Cooperation | Treasury -$0.080 billion; Supply Consumption -2%; Bureaucracy Cost Multiplier +2% | German land exercises or British naval exercises require recipient approval. Active German cooperation enables Maximum Planning +3% with army personnel costs +3%; British cooperation enables Supply Consumption -3% with navy personnel costs +3%. Each follow-up costs $0.060 billion. |
| A European Pillar | Treasury -$0.120 billion; one 25% electronics research use; Foreign Influence +4%; Bureaucracy Cost Multiplier +3% | German land standardisation or British naval industry require recipient approval. Active German cooperation enables one 25% land-doctrine reduction with army personnel costs +2%; British cooperation enables one 50% naval-doctrine reduction with bureaucracy costs +2%. Each follow-up costs $0.080 billion. |

Cost modifiers alter their existing weekly MD expense. `equipment_cost_multiplier_modifier` changes the recurring equipment bill, not factory IC or equipment design cost. Doctrine and research awards are separate finite native effects. No completed technology, ship or weapon is granted.

## Exact bilateral terms

Amounts are billions of MD dollars. Setup is charged once on acceptance; weekly expenses run only while both treaty spirits are active. The same complete terms appear in each focus inspector before acceptance and while locked.

| Offer | France | Recipient |
|---|---|---|
| Rhine Field Exercises, GER | Setup -$0.080; Division Recovery Rate +2%; $0.0015/week | Setup -$0.080; Division Recovery Rate +2%; $0.001/week |
| Atlantic Exercises, ENG | Setup -$0.080; Naval Accident Chance -5%; +15 Navy XP once; $0.0015/week | Setup -$0.080; Naval Accident Chance -5%; +15 Navy XP once; $0.001/week |
| Land Standardisation, GER | Setup -$0.120; one 50% armour research use; Equipment Cost Multiplier -4%; $0.002/week | Setup -$0.120; one 50% armour research use; Equipment Cost Multiplier -4%; $0.002/week |
| Naval Industry Pact, ENG | Setup -$0.120; one 50% naval research use; Dockyard Output +4%; $0.002/week | Setup -$0.120; one 50% naval research use; Dockyard Output +4%; $0.002/week |

Each operational pair excludes its alternative; the main strategies also exclude one another. The extension therefore adds at most $0.002 billion/week to simultaneous French agreement streams, not the sum of all four proposals.

Acceptance rechecks named recipient consent, both countries' existence and NATO membership, bilateral peace, native embargo, all four mirrored sanction classes and an unapplied valid proposal. It charges and grants both sides atomically once. Signed agreements survive government changes. Loss of NATO membership suspends both spirits and streams while retaining signatures; restored membership restores the programme without repeating setup, research or XP. This subsystem never grants NATO readmission. Party follow-ups additionally require UDR rule and the actual active parent spirit.

These are explicit specifications, not an implemented runtime transaction. The independent review distinguishes them accordingly.

## Positions and preservation

Root **(20,7)**; nuclear choice **(18,8)/(22,8)**; main policies **(16,9)/(20,9)/(24,9)**; six programme choices at x=15/17/19/21/23/25, y=10, with matching follow-ups at y=11. Every anchor precedes its dependants. The NATO fit includes its external Gaullist Majority prerequisite. Adjacent links depict the three-way exclusion without drawing through its middle card; the complete reciprocal exclusions remain in data and inspectors.

The economy footprint translates exactly +20 x units to reserve this space. `NATO_PRESERVATION.json` verifies that all 134 original focus records retain every non-coordinate semantic field and all other existing positions remain unchanged. Government shading compares actual party slots, so this section belongs to UDR rather than creating a tenth government option.

Current browser checks cover 152 inspectors, 19 bilateral previews, nine governments and 42 section/width fits at 320/736/1024 px. Weekly values such as 0.0015 display without rounding. Current independent checks find no title overflows at the approximate 15px Arial/147px title field and no unrelated-card connector intersections. Native font metrics, engine routing, execution, save/reload and live MP remain untested.

Current reviews: `NATO_REVIEW.md`, `NATO_LAYOUT_REVIEW.md/json`. Earlier 134-node reports remain historical baseline evidence. The additional NATO icon is an unchanged conversion of the current MD goal texture; provenance and unknown individual credits/permissions are in `art/NOTICE.md`. No artwork is installed by this concept update.
