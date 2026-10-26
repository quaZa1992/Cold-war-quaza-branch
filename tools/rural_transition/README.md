# IMPERIA CW — Cold War: Rural labour and directed urbanisation

The existing Green Revolution policy now reduces both native agricultural labour
requirements: subsistence agriculture by 15% instead of 5%, and agricultural
districts by 15%. Its existing 15% agricultural productivity bonus and drawbacks
remain. A new economic-selector policy, Directed Urbanisation, reduces subsistence
labour by 30% and raises civilian factory construction speed by 15%, at the cost of
25% agricultural productivity, 15 percentage points of stability, 40% higher social
spending costs, 35% higher bureaucracy costs, 20% higher healthcare costs and a
10% consumer-goods factor (displayed as Tax Cost Factor).
It costs 300 PP, carries the selector's 1,440-day commitment, and costs 200 PP to
remove. It is available in the 1970 scenario to countries with subsistence workers.
AI does not adopt it. Losing the rural workforce does not bypass the commitment.

Both policies use existing MD modifier consumers, without editing the economy
formula or introducing a new recurring callback. Adoption/removal refresh the
country's existing economy. No population or military manpower is created or
transferred, and no geographical urban population is tracked. Existing workers
become available to the normal allocation process. Without jobs, they can be
unemployed. The modifiers revert on removal; this is an ongoing policy rather
than permanent migration between states.

MD combines these modifiers additively. The two policies together reduce normal
subsistence labour requirements by 45% before other modifiers, rather than
multiplying two sequential reductions. Agricultural districts receive only the
Green Revolution's 15% reduction. The native subsistence clamp and district
minimum requirement remain unchanged.

## Historical basis

* **Mechanisation and the Green Revolution:** the policy represents high-yield
  seeds **combined with** irrigation, machinery and public investment. Improved
  seeds alone do not justify a universal claim that agricultural employment falls.
  IRRI's [retrospective of its 1970 annual report](https://ricetoday.irri.org/in-retrospect-irri-annual-report-1970/)
  explicitly notes that Philippine mechanisation had not necessarily displaced
  labour and sometimes increased requirements with intensive cropping. IRRI's
  [IR8 breeding history](https://ricetoday.irri.org/changing-the-world-with-seeds-the-breeding-history-of-ir8/)
  documents the 1966 release and subsequent spread, including India, the Philippines
  and Mexico. The labour-saving component here is the mechanisation package.
* **Farm machinery subsidies:** the World Bank's
  [World Development Report 1986, printed pages 97–98](https://documents.worldbank.org/curated/en/143091468331808738/pdf/PUB61340REPLACEMENT0WDR01986.pdf)
  discusses subsidised mechanisation in India, Pakistan, Egypt, Colombia and Brazil,
  as well as its unequal benefits, dependence on policy support and displacement
  of labour. These support retaining the programme's fiscal, social and fuel costs.
* **Directed industrial labour mobilisation:** Robert C. Allen's 1997 research,
  [Agricultural Marketing and the Possibilities for Industrialization in the Soviet Union in the 1930s](https://ora.ox.ac.uk/objects/uuid%3Ab13e82e4-23d5-4c3b-80e0-89531fee1f03),
  finds that collectivisation accelerated rural-to-urban migration. This is a
  precedent for coercive labour mobilisation, not a claim that all migration was
  forced or that the historical policy was necessary for industrialisation.
* **Romanian industrial towns:** the Library of Congress's
  [Romania: A Country Study, The New Social Order](https://countrystudies.us/romania/43.htm)
  describes peasants entering industrial work, commuting and migration, the
  deterioration of the remaining agricultural workforce and pressure on urban
  services. The World Bank's
  [1994 Employment and Social Protection Project](https://documents1.worldbank.org/curated/en/132151468759297466/pdf/multi0page.pdf)
  also identifies forced industrialisation and artificially maintained employment
  as inherited distortions. These justify the agricultural and spending trade-offs.
  The policy does not treat Romania's later village-demolition campaign as an
  accomplished fact at the 1970 start.

The percentages are gameplay choices, not estimates of historical causal effects.
The stronger urbanisation penalties reflect the same documented trade-offs:
weakened agricultural labour, disrupted communities and the cost of housing,
welfare, clinics and administration in expanding industrial towns. Healthcare is
charged through MD's existing weekly public-health budget, alongside the other
native spending multipliers; the revision adds no recurring script hooks.
Run `python tools/rural_transition/test_policy.py` for the native-consumer,
allocation, stacking, eligibility, removal and asset checks. Native-game and
multiplayer behaviour still need an engine session.
