# Political direct-reward overhaul: authored data and route audit

252 political focuses / 14 party or office chapters, all covered in `tools/iraq_1970/reward_overhaul_politics.json`. Geometry, exclusions, government/office/formation gates and actual political/foreign agreements are unchanged. The file changes reward data only; the root compiler owns installation and save receipts. Every focus carries direct reward beyond its decision unlock. Very short political gateways remain for actual successions/elections.

29 focuses carry a finite one-time technical/experience/literacy/corruption result. All standing changes use the existing current-party/office programmes. 6 existing political physical assets retain their exact state/type/count; 4 selected paid projects are added: Bakr Baghdad infrastructure1 at2.5%GDP; Nasserist Baghdad military factory1 at5%; ICP Baghdad civilian factory1 at4%; royal Basra infrastructure1 at3%. All physical effects are in `building`, never hidden in `instant`; no charged MD random-building helper is used. The sole new permanent corruption-level change is Civic Commercial Courts. Shared chapters have no additional such level change according to their owner.

Research/doctrine names are unique `COLDWAR_IRQ_v3_<focuskey>_<category>`. Only categories with real period consumers are used: industry, construction, information technology and land doctrine. No fuel-refining1990/agriculture1990-only category, modern equipment, free foreign transfer or fake army is introduced. No new raw state effect needs separate ownership/control wrapping; root normal building guards remain necessary for all10 assets.

A 48-key palette is supported by actual native main-MD uses/readers. 47 keys already pass the existing numeric formatter lookup. `equipment_upgrade_xp_cost` is a real native effect (main MD `Iraqi.txt:335`, equipment design XP expenditure), but its exact `*_tt` is absent and needs the root's reviewed native numeric formatter. Replacing it with equipment conversion would be a different mechanic.

## Native reference basis

Original main MD `05_iraq.txt`, `05_russia.txt`, `05_iran.txt` were read before authoring. IRQ Restore Faith gives25 armyXP/25 command power plus actual military-spending law; Address Army Corruption gives a real corruption step and25XP in each service. Main Iraqi ground forces give100armyXP and Rustamiyah a100% doctrine discount plus higher real military spending. Our party-specific awards are smaller and explicitly funded, and shared military instruction is counted below. PER Ministry of Education changes real education costs; Pillar of Welfare/Workers House affect health/welfare/growth/production rather than universal research. Original IRQ construction helpers can charge money and include undeclared extra power plants, so none are copied into our own GDP invoice.

PER native dynamic fields supply office/civil-sector productivity, population/corporate/sector tax channels, medical/education/police expenditure and investment terms. Native readers in `00_money_system.txt:463/526/785/3341/3374/3476/3505` establish the actual fields, while `99_investment_scripted_effects.txt:421–449` establishes receiving-investment duration. The original MD benchmark report and its limits are in `MD_REFERENCE_REVIEW.md`.

## Compatible whole programmes

Each row's interval covers its actual compatible choices; maxima in different columns need not belong to the same choice. Full exact choices and modifier packets are recorded in `POLITICAL_ROUTE_TOTALS.json`. AND/OR prerequisites and mutually exclusive losing descendants are respected. Only Baath+Bakr, Baath+Saddam and ICP+Aziz are combined. Other parties are alternatives; Bakr and Saddam are never combined. Standing party/leader ownership, current constitutional mode and genuine accepted agreements must hold.

| Current governing programme | Routes | Org | Defence | Military output | Civ productivity | Office productivity | Tax | Health costs | Education costs | Bureaucracy | XP | Once literacy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| aziz | 4 | +0% | +0% | -2% | +7% | +13..+24% | +0..+8% | -16..-11% | -16..-4% | -4..+0% | 0 | 0..1.5pp |
| baath | 4 | -1..+0% | +0% | +4% | +13% | +8% | +0% | -11..-6% | -18..-7% | -4..+1% | 0 | 0pp |
| bakr | 4 | +0..+2% | +0% | +0% | +0% | +12..+22% | -4..-2% | +0% | -11..-7% | -8..-3% | 15..30 | 0pp |
| civic | 4 | +0% | +0% | -2% | +0..+5% | +14..+23% | +1..+12% | -19..-4% | -9..-3% | -1..+2% | 0 | 2.5pp |
| communists | 4 | +0% | +0% | +1..+15% | +10..+16% | +4..+12% | -2% | -6% | -17..-8% | +3..+4% | 0 | 0pp |
| dawa | 4 | +0% | +0% | -2% | +4..+12% | +5..+14% | -2..+0% | -35..-19% | -21..-13% | +0..+4% | 0 | 2.0pp |
| kurds | 4 | +2% | +0% | +0% | +0..+4% | +18..+26% | -8..-3% | -7..+0% | -5..+2% | +2..+8% | 20 | 2.0pp |
| monarchy | 4 | +0% | +0% | +0% | +0% | +10..+18% | +2% | -4% | -10% | +1..+3% | 0 | 2.0pp |
| nasserist | 4 | +0% | +0% | +0..+10% | +5..+17% | +14..+15% | -2..+0% | -6% | -14% | -5..+2% | 15 | 0pp |
| officers | 4 | +3..+9% | +4% | +0% | +0..+6% | +1..+11% | +3% | +0% | -3% | +4..+7% | 0..25 | 0pp |
| puk | 4 | +2% | +0% | +0% | +8% | +4..+17% | -2% | -7..+0% | -16..-5% | +1..+8% | 20 | 0pp |
| saddam | 4 | +0..+3% | +3..+7% | +9% | +0..+4% | +5..+13% | +2% | -8% | -5..+0% | -2% | 15..40 | 0pp |
| sciri | 4 | +5% | +0% | +0% | +0% | +8..+16% | +0..+3% | -4% | -16..-12% | +0..+2% | 20..35 | 2.5pp |
| sunni | 4 | +0% | +0% | -2% | +6..+11% | +13..+20% | -4..-2% | -20..-9% | -9..-3% | -4..+0% | 0 | 1.5pp |
| baath+bakr | 16 | -1..+2% | +0% | +4% | +13% | +20..+30% | -4..-2% | -11..-6% | -29..-14% | -12..-2% | 15..30 | 0pp |
| baath+saddam | 16 | -1..+3% | +3..+7% | +13% | +13..+17% | +13..+21% | +2% | -19..-14% | -23..-7% | -6..-1% | 15..40 | 0pp |
| communists+aziz | 16 | +0% | +0% | -1..+13% | +17..+23% | +17..+36% | -2..+6% | -22..-17% | -33..-12% | -1..+4% | 0 | 0..1.5pp |

The political positive-stability spam is removed: only10 political focuses retain a stability modifier, mostly explicit political drawbacks; the common+15-point positive-programme cap is retained. There are no new positive universal research modifiers; remaining general research entries are the Baath monopoly/Bakr trusted-officer expertise trade-offs. This does not erase literacy research effects or shared education programmes.

Shared maximum professional-organization path adds13 points according to the shared owner's plan (8professional +5other). Add this to the appropriate political row, not to every mutually exclusive army choice at once. Examples: Baath+Saddam Guard +3 gives16 total before starting burdens; Baath+Bakr trusted officers +2 gives15; officer merit route +9 gives22; SCIRI +5 gives18. The patronage −5 starting penalty remains unless its actual command reform has been delivered.

Meaningful major choices: Front industrial/education institution vs monopoly executive command with expertise loss; mass mobilization vs skilled initial production; Bakr collective civil competence vs presidential command; Saddam Guard cohesion/defence vs regular-army recovery/training; officers merit organization vs loyalty mobilization/command with poorer cohesion; Nasserist public military industry vs civilian mixed-sector expansion; pluralist ICP civilian education vs vanguard military output; independent unions efficiency recovery vs state-union maximum output; constitutional crown civilian finance vs executive command; KDP autonomy service/security savings vs federal transport and revenue concessions; PUK cooperation logistics vs independent apparatus; Dawa medical provision vs enterprise/endowment production; SCIRI sovereign finance vs patron-oriented licensing/support and reduced influence defence; IIP civilian expansion vs medical/welfare efficiency. Foreign counterparts are never compelled by the direct domestic capability.

Civilian/office productivity modifiers are real sector consumers, not promises of the same percentage national GDP growth. Health/education/police savings act on actual law-selected expenditure and do not pay cash. Receiving-investment−0.15 is a native modifier, not exactly15% fewer calendar days. `monthly_population=.03/.05` is growth-rate support, not free population or military manpower. `foreign_influence_modifier` controls own offensive influence; defensive sovereignty uses `foreign_influence_defense_modifier`.

No compiler, loaded gameplay file, save or native game process was touched by this author. Root integration must preserve one-time v2 credits, actual spending/loan consent, current-programme conditions, all building capacity guards and informative native previews. Statistical/AST checks do not prove HOI4 rendering or multiplayer runtime.
