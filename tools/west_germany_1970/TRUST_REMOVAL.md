IMPERIA COLD WAR — German trust retirement and politics-panel access

The user requested removal of Moscow Trust and the previous DDR national-course link to the bilateral dossier, then explicitly confirmed removal of Western Integration and Moscow's Guarantee point values. The national DDR course/BOP, genuine alliances, treaty requirements and human Soviet consent remain independent systems.

Retired runtime inputs are `COLDWAR_DDR_moscow_trust`, `COLDWAR_DDR_trust_delta`, `DDR_state_trust`, `DDR_moscow_trust`, `cwger_westbindung` and `cwddr_moscow_backing`. Their writes, score thresholds, displays, automatic schedules and derived contributions are removed from both canonical sources and loaded scripts. Derived trust-only offsets are removed rather than frozen. Native DDR retains 821 focuses, with no empty completion rewards introduced.

Five obsolete DDR trust modifier IDs survive only as empty, disabled definitions. The GER startup cleanup clears retired score variables and their unused display/derived caches; it does not call `remove_dynamic_modifier` for those disabled IDs because HOI4 reports them as unregistered at startup. Cleanup runs through `on_startup`, once per German country, without a recurring country scan. It recalculates the independent Bonn and already-active legacy DDR formulas; it does not initialize the dormant 1985 crisis system. Native HOI4 save loading has not been tested.

The national DDR course no longer contributes ±12 to bilateral climate. The Moscow readout now reports actual war/alliance status, without promising intervention. A previous Soviet refusal of Unity talks can be revisited after an existing Soviet reform-course focus. Soviet war entry uses existing explicit orders or actual AI faction membership. DDR socialist reform retains its price, one-time receipt, institutional tradeoffs and SED-government requirement without a replacement Soviet-score gate. Krolikowski, garrison repatriation and Fraternal Assistance preserve their human Soviet/DDR response routes. Previously queued ambassador and decision-receipt events retain their independent diplomatic options; they no longer operate a trust system.

The two new launcher sprites use original procedural artwork and 20×20 DDS textures. They sit at (424,248) and (446,248), beside faction membership in the native 550-pixel politics panel. Their full native-control audit includes both faction labels, the 191×57 faction create/open button, the 31×31 dismantle button and the 32×32 faction-view button. The first icon opens Inner-German Relations. The second opens BRD Internal Security or DDR Domestic Affairs. [Placement audit](entry_ui_preview/PLACEMENT_AUDIT.md) and [asset provenance](entry_ui_preview/PROVENANCE.md) record sources and bounds.

Launchers use `politics_tab`, player-only visibility and country-local dirty counters. Opening lazily initializes missing national dossier state through existing guarded providers. A legacy undefined BRD security-window trigger is replaced by its actual scenario/initialization conditions. Hidden economy UI and a missing German counterpart do not hide the entry points. DDR domestic controls continue to work when Bonn is absent; bilateral controls still require a valid, initialized counterpart. There is still one GER-owned bilateral monthly simulation. Closed/AI views do no full presentation arithmetic.

Validation completed against the installed scripts:

- 51 shared colonial/security runtime tests, 12 German security-contract tests, 16 DDR dossier tests and 5 trust-retirement/migration tests pass: 84 script-model tests.
- 106 GUI/performance regression checks pass. Full presentation runs only for open human views; there is no added simulation tick or presentation border scan.
- The German content validator reports zero errors, with its existing average-focus-cost warning. The bounded legacy DDR formula validator passes.
- Native DDR was independently reviewed for consent routing, inert modifier tombstones, empty rewards and empty conditional branches. None were found.
- All five DDR tab previews render without reported text overflows. The launcher placement was independently audited using the installed native sprite dimensions.
- Script brace parsing, localisation/script BOM checks and scoped `git diff --check` pass. The archived DDR validator was not run: its configured output/index paths are missing. Focused native-script checks and independent review cover this change; they do not replace a full native game test.

HOI4 rendering, native tooltips, UI scaling, multiplayer synchronization, save/reload and measured frame times remain untested. Restart the game to load changed GUI definitions. The narrow 1–2 pixel launcher clearances should be checked at the player's UI scale.

Bounded installers preserve unrelated working-tree changes. `compile_relations.py` installs the dossier, launcher and startup-cleanup blocks. The source generators contain the same final mechanics for future builds; no full national generator was run over the live mod.

The subsequent two-player sandbox changes and current validation are recorded in [SANDBOX.md](SANDBOX.md). That record supersedes the earlier treaty, historical-event and validator-warning details above.
