# IMPERIA COLD WAR — proposed state transitions, not runtime game code.
"""Explicit replacement and expiry rules prevent tree/event/party double rewards."""
SETUP = {
 'title':'Proposed 1970 initialization',
 'text':'The existing 1970 Cuba history has no education, health or corruption idea tiers. The edu_02/health_02 entries belong to 2000. This concept proposes edu_02, health_02 and corruption_level_04 when the corresponding category is genuinely uninitialized; preserve a valid existing tier. These are balance baselines for broad public provision and bureaucratic constraints, not historical statistical measurements. No 2000 Special Period or migration-crisis spirit is imported.',
 'ideas':['edu_02','health_02','corruption_level_04'],
 'guard':'1970 scenario, original CUB, one-time setup receipt; initialize only missing categories, recalculate native budget/law variables afterward.',
}
LIFECYCLES = [
 dict(title='The 1970 harvest',rules=[
  'The initial campaign is active on 1 January. Finish the Zafra programme modifiers expire at the 26 July review; Restore the Sectors is a lasting national reallocation.',
  'The May announcement is informational. At the July review remove the original campaign and any temporary Finish the Zafra programme before applying the selected 180-day settlement.',
  'Mobilisation or no completed harvest verdict: recovery burden = civilian industry productivity −6%, construction speed −4%, for 180 days. Rebalanced course: civilian industry productivity −3%, construction speed −2%, for 90 days. The timed July event choice is additional and explicitly listed.',
  'A player starting late can resolve an overdue historical harvest once. There is no permanent +12% farm mobilisation from a finished 1970 campaign.',
 ]),
 dict(title='Ownership and the Revolutionary Offensive',rules=[
  'Protected Enterprises or Joint Ventures removes the original Revolutionary Offensive spirit. Its replacement is the chosen national economic programme with exactly the focus deltas; there is no second hidden reform bonus.',
  'Shared ownership priorities survive a government change until formally repealed. Party-specific tax/incentive programmes follow the governing subparty. Built factories and infrastructure remain national assets.',
 ]),
 dict(title='Sugar, diversification and Soviet supply',rules=[
  'Default Sugar and Soviet Oil: agriculture +10%, sanction resistance −10%, foreign influence defence −10%.',
  'Food before Sugar only: replace it with Imported Machinery, agriculture +0%, sanction resistance −4%, foreign influence defence −5%. Light Industry only: agriculture +5%, sanction resistance −6%, foreign influence defence −6%. Both completed: agriculture +0%, sanction resistance −2%, foreign influence defence −3%. Exactly one variant is active.',
  'A Soviet supply shock requires an actual withdrawal of a recorded support/supply commitment or a verified contraction of bilateral fuel/trade deliveries. Calendar year 1990 and CMEA exit alone are insufficient. The counterpart must control withdrawal; no new autonomous annual subsidy is assumed.',
  'While the verified shortage remains: no diversification gives civilian productivity −20%, construction −15%, agriculture −8%; one of Food before Sugar/Light Industry gives −12%, −10%, −4%; both gives −6%, −5%, −2%. These replace one another and clear when deliveries recover or a substitute supply accord actually takes effect.',
  'The 1990 emergency choice adds only its stated 365-day adjustment. It does not add the modern Special Period idea or repeat the shock under another name.',
 ]),
 dict(title='The embargo and diplomatic easing',rules=[
  'The custom embargo spirit is the fallback representation of the US restriction. If an active native US embargo or an Imperia comprehensive US economic sanction already supplies that restriction, suspend this fallback and use that system. Third-country sanctions remain separate.',
  'Limited accepted easing: replace the fallback with resource export revenue −10%, civilian productivity −3%; reciprocal opinion +10. Claims commission costs CUB 0.10 Treasury.',
  'Full accepted executive trade settlement in 1970–90: remove actual US embargo restrictions and this fallback, reciprocal opinion +20. CUB pays a total 0.25 Treasury (only a further 0.15 if the earlier 0.10 commission was paid). Restore the fallback if comprehensive restrictions are subsequently reimposed.',
  'MFN tariff treatment, official credits, private claims and Guantánamo require their own terms. The later 1996 statutory codification is not a retroactive Congress-only embargo gate.',
 ]),
 dict(title='Security institutions',rules=[
  'The initial CDR/security institution remains a national starting constraint. A professional settlement through Socialist Constitution, Accountable Officers or Professional Intelligence replaces it with counterintelligence defence +10%, political power gain −4%, research −2%.',
  'A completed civilian constitutional settlement (Auténtico, Ortodoxo, Christian Democrat, Liberal, RECE charter or Alpha civic-demobilisation endpoint) replaces that institution with civilian counterintelligence defence +5% and weekly bureaucracy expenditure +3%. The institutional replacement is persistent, not a second party buff.',
  'An explicit later surveillance-restoration decision must replace the institution again and pay its political cost; merely changing a party does not resurrect dismantled institutions. Party programme modifiers still deactivate/reactivate with the exact current slot.',
 ]),
 dict(title='Exile and dialogue',rules=[
  'The exile spirit begins at workforce −4%, stability −3%. A completed voluntary family/return agreement plus actual registered returns reduces it to workforce −2%, stability −1%. A dialogue announcement alone grants only its listed event effects.',
  'Historical migration totals are context, not an automatic population debit. All departures and returns pass once through the existing native/Imperia migration ledger; forced removal is not a selectable development reward.',
 ]),
 dict(title='Budget and corruption caps',rules=[
  'A valid budget tier is required in availability and completion. Below cap use the native +1 tier helper. At edu_05/health_06 use one named sector-efficiency idea giving −3% weekly sector expenditure. Repeated cap rewards reuse that same idea and never stack.',
  'Corruption reform calls decrease_corruption only at corruption_level_02 through _10. At _01 use a single named Public Oversight idea: weekly bureaucracy expenditure −3%. Missing law category blocks enactment and requests initialization; no helper is allowed to fall through to unrelated +150 political power.',
  'These national service/oversight institutions remain after a government leaves. Their recurring budget obligations remain real; completed grants cannot be farmed by switching parties.',
 ]),
 dict(title='Fidel-era social, scientific and economic programmes',rules=[
  'The Family Code completion records a legal reform. Its funded childcare/work-participation modifier is a governing programme; switching parties does not automatically repeal family rights. Actual repeal requires its own political decision.',
  'Family Doctor Teams grants a native healthcare budget tier once, after the same valid-tier and cap guards as other health reforms. The law tier persists across governments; the PCC coordination/cost modifiers follow the exact governing slot. No healthcare tax-income modifier is described as clinical care.',
  'The Biological Front grants a single 50% CAT_genetics research bonus and one civilian factory in State 854 after legal construction/payment checks. Both are durable national gains; the weekly research-training expenditure is part of the current PCC programme. Refresh never repeats the factory or research use.',
  'Peasant Markets follows continued SDPE; Revive Microbrigades follows Rectification. Their ancestors are mutually exclusive, so both economic programmes cannot stack. The 1986 congress event respects the completed verdict and never grants either new follow-up as a second bonus.',
  'The microbrigade infrastructure level represents Havana neighbourhood utilities/access works. Construction speed, redirected civilian output and welfare expenditure model the mobilisation programme; no apartment count or housing-stock system is invented.',
 ]),
 dict(title='Government lifecycle and international agreements',rules=[
  'Each governmental programme uses the exact ruling_party slot in availability and reward. Completed receipts persist; current modifiers are rebuilt from the receipts of the current slot only.',
  'Government change refresh, initial load and weekly reconciliation remove inactive party dynamic modifiers and restore eligible ones. Refresh contains no Treasury, debt, construction, research, experience, law-tier or migration grant.',
  'CMEA member programme requires the actual admission spirit, including in the reward and subsequent refresh. Leaving suspends it; readmission restores the programme but never repeats its research grant.',
  'Accepted technical/cultural support runs until terminated by its diplomatic terms. An offer focus only creates a 90-day recipient-owned proposal; refusal or expiry charges nobody. Every accepted transaction has a once-only receipt and validates ownership/control/caps before charging.',
 ]),
]
