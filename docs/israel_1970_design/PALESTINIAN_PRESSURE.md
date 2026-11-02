# IMPERIA COLD WAR: Palestinian consequences of Israeli settlement programmes

Implemented on 27 October 2026. This extends the 399-focus Israel module without
adding another historical diplomatic sequence. All percentages below are proposed
game balance, not measured historical effects.

## Conditions and costs

Corrected on 28 October 2026: foreign settlement presence is unilateral. There
is no Palestinian or other host permission decision. Generic controller burdens
are additional and recorded in `UNILATERAL_SETTLEMENTS.md`; the table below
contains only this separate Palestinian programme.

An existing Palestine receives separate country modifiers for the West Bank
(208) and Gaza (209), provided Palestine still owns the area or retains its core.
Each area needs either a completed settlement project under current Israeli
control, or an actually funded, operating unilateral foreign foothold.
An existing funded foothold also retains initial-tier pressure when Israel takes
control, even before another controlled construction project is delivered.
Occupation alone, a survey, an unfinished project or an unfunded plan
does not activate this added programme.

| Palestinian country effect | Initial settlement presence, per area | Extensive network, per area | Both areas at maximum |
| --- | ---: | ---: | ---: |
| Stability | -2% | -4% | -8% |
| Political power gain | -2.5% | -5% | -10% |
| Office productivity | -4% | -8% | -16% |
| Bureaucracy cost modifier | +4% | +8% | +16% |
| Social cost modifier | +3% | +6% | +12% |

The initial tier follows delivered designated sites, a regional controlled-state
project, or an operating foreign foothold. Delivered settlement packages,
entrenched networks and any completed extension use the extensive tier under
Israeli control. Multiple receipts never stack within one area beyond tier two.
Sinai and Golan programmes do not impose these Palestinian penalties.

Bureaucracy and social costs modify their native weekly spending components.
Office productivity changes the actual MD productivity input. Stability and
political power use native country modifiers. No population, workforce size,
building, cash transfer or ownership changes are added by this extension.

## Negotiation, relief and lifecycle

The affected government receives adverse settlement effects without an acceptance,
refusal or termination menu. Palestine also bears the corresponding institutional
and commercial pressures if it exists and retains its territorial connection.
No automatic declaration of war, mandatory political answer or dated uprising
is attached. Voluntary compensation negotiations remain a separate mitigation
policy and never act as permission to establish the settlements.

A selected, actually funded settlement-compensation programme limits that
area's pressure to the initial tier. A completed negotiating focus or an
unfunded agreement is insufficient. Relief never applies to both areas merely
because one area was selected.

Loss of Israeli control ends the controlled-project basis. A surviving funded
foreign foothold can independently maintain initial-tier pressure. Israel ending
its funding removes that basis; war, embargoes or sanctions do not automatically
erase the presence. If neither basis remains, the area's modifier is disabled and
removed on reconciliation. Losing Palestine's ownership and core also ends it.
Return of the actual conditions restores the appropriate tier without fees or
asset grants. An absent Palestine receives no country effect; later creation is
evaluated against the then-current conditions.

Full prospective Palestinian numeric effects appear in the relevant project
and unilateral foreign-establishment previews, including locked focuses.
Compensation previews show the resulting reduced programme on the focus,
Palestinian acceptance event and Israeli funding decision. Their display
arithmetic never invokes the real grant or treasury providers.

## Period research and interpretation

- [UN Special Committee, A/8389/Add.1, 1971](https://unispal.un.org/pdfs/0E7ECB64C366F509852569F400684BF3.pdf),
  paragraphs 11-12: recorded ministerial and press statements concerning
  settlement expansion, fenced land near Deir el-Balah and Kiryat Arba. This
  supports linking consequences to actual projects and territorial commitments.
  The committee's reported evidence and conclusions are attributed to that body.
- [UN Special Committee, A/8828, 1972](https://www.un.org/unispal/document/auto-insert-177238/),
  sections III.A-B and III.G: examined settlement, property and displacement
  allegations and cumulative consequences. The committee lacked permission for
  an on-site visit. This is period evidence of contested institutions and land,
  not a direct numerical estimate of stability or administrative costs.
- [Bank of Israel, Annual Report 1972, chapter IX](https://www.boi.org.il/media/ti3nzv2j/pe_9.pdf),
  opening discussion and employment tables: documents increased employment from
  the administered territories in Israel and reduced employment within the
  territories themselves. It supports economic interdependence and institutional
  trade-offs; it does not prove that every cross-border link reduced income.

The existing 1970 PAL game tag is an RP/scenario abstraction. These modifiers do
not assert that a sovereign Palestinian administration historically existed in
1970, nor import post-1994 institutions or later closure regimes into the start.
The unilateral foothold under another country's effective control is an explicit
RP abstraction; optional compensation relief is a selectable mitigation policy.
The specific tiers and causal weights are design choices.

## Verification and provenance

`validate_palestinian_pressure.py` records the current emitted-script model and
structural checks in `palestinian_pressure_validation.json`. It covers actual
country/state scopes, both tiers and their combined
cap, every qualifying project receipt, absent/dead countries, claims,
unfunded plans, unilateral establishment, restoration, compensation specificity and
prospective effects from the actual Israeli and Palestinian display scopes.
The existing presence and rework validators remain separate regression checks.
The browser report is `preview_validation.json`. These are source/model/browser
checks; native HOI4 tooltips, save/reload and live multiplayer have not been run.

Custom code and English text were authored for IMPERIA COLD WAR with Codex.
The referenced documents retain their original institutional authorship; no
source text, photograph or new third-party art is embedded by this extension.
Separate redistribution permission for those source documents is unknown.
Existing MD/Cold War artwork is unchanged and retains its existing credits and
unknown individual asset permissions. See `PREVIEW_NOTICE.md` and the root
`IMPERIA_COLD_WAR_NOTICE.md`.
