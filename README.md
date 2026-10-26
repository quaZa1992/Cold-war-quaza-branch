# MD Cold War

Cold War / Imperia content migrated to the Millennium Dawn 2.0.2 base for Hearts of Iron IV 1.19.*.

The Mod is intended for internal, non-commercial use within Imperia Roleplay. Use on outside servers and sharing of Reserved Imperia Content may be approved case by case in writing, with the required credits, subject to the independent rights preserved in the license.

Copyright, contributor credits, permissions and enforcement terms are set out in [license.txt](license.txt), including international enforcement and US takedown procedures. Rights are reserved in eligible independent Imperia contributions; Millennium Dawn's CC BY-SA 4.0 terms, other third-party licenses and applicable platform rights remain in effect.

The playable scenario starts in 1970 and uses English localisation. Starting forces, equipment stockpiles and historical starting research are reserved for later work. The migrated Cold War systems and the selected Imperia balance changes are included.

<!-- IMPERIA COLD WAR: Preserve attribution for the SSR agency creation restriction. -->
The SSR intelligence-agency restriction adapts the two-layer button blocker and AI factory-budget technique from [Yard1's Intelligence Agency Blocker](https://github.com/Yard1/HoI4-Intelligence-Agency-Blocker). The SSR eligibility rule and MD reward safeguards are Imperia Cold War additions.

<!-- IMPERIA CW — Cold War: Match the local launcher path and require complete LFS assets. -->
Install the repository as `mod/mdcoldwar-main` and copy the supplied `mdcoldwar.mod` launcher descriptor into the parent `mod` directory. Its `path` must match the actual content folder. Keep `descriptor.mod` inside the content folder; it is not the launcher descriptor.

Graphics, maps and audio assets use Git LFS. Install Git LFS before cloning, then run `git lfs pull` in the cloned repository. A downloaded source ZIP can contain small text pointers instead of the actual assets, causing black loading screens and invalid image or sound errors. Extracting that ZIP does not download its LFS content, and `git lfs pull` requires a Git checkout.

This remains a work in progress. A USA 1970 startup, seven days of play, saving and reloading were confirmed. A later first-month crash was recorded; two stale power-rank references were corrected, but the monthly crash still requires an in-game retest. Static file verification is not a runtime compatibility guarantee.

Legacy source, development tools, deferred features and migration records were archived separately on E on 13 October 2026. They are not part of the runtime mod tree. The local archive is `E:/MDColdWar_Backups/mdcoldwar_2026-10-13_old_mod_and_migration_archive`; the original pre-migration backup is retained separately.
