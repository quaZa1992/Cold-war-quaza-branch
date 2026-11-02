IMPERIA COLD WAR: Annual Council ballot and programme referrals
=============================================================

The user approved one annual ballot, fifteen game days, national-flag voting, plurality selection and institutional English guidance. This replaces the earlier Soviet-first permanent editor rule. The existing human chair remains acting chair during the first ballot; an eligible elected chair is preserved by normal authority refresh. The permanent Secretariat remains in Moscow.

Historical basis and deliberate adaptation
-----------------------------------------

[UN Treaty Series 368, No. 5245](https://treaties.un.org/doc/Publication/UNTS/Volume%20368/volume-368-I-5245-English.pdf) lists the USSR as a Council member, not the individual Soviet republics. Articles IV, VI and IX distinguish national proposals, interested-state consent, the session chair and the Secretariat. Separate republican Council votes are therefore not enabled. A republic that actually becomes independent and is admitted through the ordinary membership procedure can acquire normal member rights.

[Alexander Uschakow, APuZ 2/1966](https://www.bpb.de/shop/zeitschriften/apuz/archiv/527378/der-rat-fuer-gegenseitige-wirtschaftshilfe-comecon/) describes the Executive Committee's rotating chair. The user's annual plurality election is an explicit RP game adaptation, not a claim that historical COMECON elected a president this way. The human-only franchise and passive AI policy are also user-defined game rules.

Procedure shown in the game
---------------------------

The Council tab contains the electoral register and a clickable Rules of Procedure sheet. The text addresses the delegation through the Secretariat and describes the complete process without AI, multiplayer or implementation terminology. The header displays the actual presiding country's current flag and name. The Council tab reads Council Ballot during the electoral period.

The register opens once in each native calendar year. New saves or older saves without this schema receive an initial fifteen-day ballot. The opening register contains actual represented full members only. Each delegation has one vote regardless of its financial contribution. Clicking a national flag seals that country's ballot; subsequent clicks cannot replace it. The selected country keeps its coloured flag and seal, while the remaining flag buttons are disabled. The largest valid tally appoints the chair when the fifteen days expire. The outgoing chair can be re-elected by a larger tally.

Equal tallies use a fixed order of succession starting after the outgoing chair. The original members and Cuba use the historical Russian-alphabetical order; any additional admitted countries follow their saved Council registration order. No ballots uses the same order without inventing votes. A withdrawn or unrepresented voter/candidate is excluded from the count. The opening register remains fixed; newly represented members join the next annual register. An eligible acting delegation maintains business if the chair becomes unavailable.

Programme workflow
------------------

Every observer can inspect the full 22-programme, 44-offer Catalogue, including investment tiers, complete host/partner numeric rewards, national services, capital formula and requirements. Sidebar selections now browse the catalogue independently of the shared contract. No viewing action changes a contribution, signature, quote, payment or asset.

Represented full members may Request Agenda Item. Each delegation has one current referral, storing the offer, investment tier and revision. The Council correspondence pages show four referrals per sheet. The selected referral has a red border. Only the presiding delegation can prepare it in the selected unsigned contract file. Execution rechecks the referral revision and membership. A changed or withdrawn referral cannot be substituted for an earlier selection. Preparation creates a draft without ratifying it or assigning another government's contribution.

Drafts and running contracts keep their existing review, invoice and delivery guards. Changing the chair never moves liabilities, rewrites signed terms or repeats assets. Human Union republics may confirm their actual local implementation as before, but cannot cast a Council ballot, stand for chair or submit a separate national referral while they remain Union republics.

Implementation and saved state
------------------------------

`tools/comecon/elections.py` owns the saved ballot and referral effects. `governance.py` retains authority and project consent. `council_ui.py`, `compact_ui.py`, `controls.py`, `view.py` and `assets.py` own the native office, catalogue, footer and current-flag bindings. `cc_elections_v1` seeds old saves without resetting project state.

The single organisation clock compares saved `cc_ballot_year` with native `global.year`. Deadline calculation uses native `global.num_days` minus the saved opening day. Repeated callbacks on the same game day cannot shorten the window, and pausing the game cannot expire a ballot. There is no wall-clock helper or unsupported yearly on_action. The active electoral register is bounded by the 32-member Council cap. Counting is bounded and deterministic, with no random tie-break. Per-view arrays and referrals are refreshed when the relevant open interface is invalidated; no world/state scan is added to a frequently evaluated GUI property.

The proposal input buffer is separate from the sealed vote target. Receipt and issue guards are rechecked before that target is written. The issue number prevents an old ballot from being used for a later register. The annual result has its own closed-round receipt. The chair-authority refresh replaces a chair only when that chair is no longer eligible.

Presentation geometry
---------------------

The dossier stays 900 x 580. Five top tabs end at x=844, before the paper's x=880 right edge. The office, catalogue and existing programme pages are mutually exclusive native scripted-GUI containers in the same 658 x 340 viewport. Eight candidate cards occupy four columns and two 76-pixel rows. Additional candidates and referrals use the existing page controls. Rules have their own page with a return control. No overlay or election panel is drawn over an active programme page. Footer action containers occupy only their own 640 x 35 bottom strip.

Validation limits
-----------------

Source checks validate native syntax, references, exact widget bindings, text bounds, actor gates, per-file actions and electoral guards. Native fixture assertions cover actual human Soviet/Hungarian control, actual AI exclusion, the fifteen-day arithmetic, one sealed vote, a second-year opening, stale issue rejection, unchanged money/contracts, invalid candidates and referral preparation. A genuine multiple-human plurality contest, co-op command ordering, save/reload and rehost remain distinct tests; a one-client fixture does not establish absence of multiplayer desynchronisation.

The retired first office fixture passed its assertions but reported an uninitialised `cc_office_page` during display refresh. The generator now initialises saved page/help fields before clamping. Its report is retained as `native-retired-council-unset-page.json` and is not counted as a passing run.

Provenance
----------

Authority and game rules: the user's instructions in this conversation. Institutional source credits are above. Original procedural paper, ballot-card and selection-border textures extend the existing COMECON generator. Country flags remain live native GetFlag images and are not copied into new textures. Existing HOI4/MD art, shaders and fonts retain their previous source records, credits and unknown separate redistribution permissions. No new third-party media or historical source text is redistributed.
