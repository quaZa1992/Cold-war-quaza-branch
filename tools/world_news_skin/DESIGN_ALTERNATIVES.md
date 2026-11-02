IMPERIA COLD WAR: Alternative global world-news presentation

29 October 2026. The user rejected the installed World Dispatch appearance and requested several substantially different concepts. This is a design round. No new variant has been selected or installed; the previous texture remains the current technical state, not an approved final visual direction.

Four original concepts are presented with the same fictional English report and the same colour settler illustration for comparison:

- **Illustrated Review**: a political weekly with a red editorial masthead, a prominent full-width photograph, a large serif headline and a small section rail beside the report.
- **Wire Bulletin**: a press-service dispatch with continuous-feed paper, monospaced typography, transmission details and a side photograph. The compact layout places the image above the report at narrow widths.
- **Evening News**: a period-inspired television bulletin with a recessed screen, colour photograph, keyed headline, separate report text and standard event acknowledgement.
- **Front Page**: a compact illustrated newspaper with a dark slab masthead, strong condensed headline above the image and a single readable report field.

All names and layouts are original concept work with Codex. None reproduces a real newspaper or broadcaster identity. The illustration is the existing generated mid-1970s reconstruction documented in `NOTICE.md`, not an archival photograph or evidence of actual perpetrators. No additional image generation or scene editing was performed in this design round. The retained master uses exactly the approved native wide crop at a higher preview resolution, without recolouring or changing its composition. Existing upstream pictures may need proportional fitting in a selected native layout; a preview does not add detail to low-resolution inherited artwork.

These alternatives go beyond replacing the background texture. A selected implementation must adapt the common native `EventWindow_News` layout while preserving dynamic event titles, arbitrary MD descriptions, actual event pictures, scroll behaviour and the shared options contract. Each design contains one continuous description field; it does not assume unsupported automatic newspaper-column flow. The original national spirits, focuses, occupation design, costs and rewards are unaffected.

The editable comparison and compact provenance/QA records are in the authorized visualization directory as `news-design-directions-template.html`, `news-design-directions.html`, `news-design-directions-provenance.json` and `news-design-directions-browser-check.json`. The comparison uses the host's named variant carousel and offers a local article-type-size adjustment. Native rendering is not established by a browser check. A new choice must be made before applying a replacement to the installed common news window.

## Wire Bulletin refinement round

The user preferred Wire Bulletin and requested larger pictures where useful, clearer structure and several variations of that direction. This selects the visual direction, not a final installed layout. Three further original concepts are available in `wire-bulletin-refinements.html`:

- **Photo Dispatch**: a clear metadata row, headline, substantially larger full-width wide photograph, one full-width typewriter report and a distinct acknowledgement area. This retains the existing native picture proportions.
- **Picture Lead**: a larger original photograph above the headline and a continuous report in print type. It uses the retained full colour illustration rather than the earlier wide news crop.
- **Desk Bulletin**: a wider window with a larger photograph beside a single report field. Print type improves the narrow text column; the small-screen preview stacks the picture and report.

All three retain feed-paper and press-wire details. Local design controls compare body typefaces and size, image width or column share, and the filing strip. There is no new image generation or scene editing. The picture alternatives use the retained generated master documented in `NOTICE.md`. The full original composition remains an illustrative reconstruction, not historical proof of the fictional report.

Photo Dispatch is the closest fit for inherited MD wide news artwork. The other concepts need proportional fitting or letterboxing for older wide pictures; no stretched faces or assumed availability of taller archival originals. A selected implementation must support long and short actual MD titles, descriptions and option lists. These are browser concepts, not installed native windows. The existing skin, registered art and GUI hashes are retained in the refinement provenance record.

## Native MD tablet study

Status update: the user subsequently rejected the tablet direction as unsuitable for the 1980s/1990s setting. Both tablet proposals below are retired design studies, not candidates for implementation without a new explicit request. No tablet skin was installed.

The user liked Photo Dispatch and asked whether it could be improved using MD's tablet. The inspected MD 2.0.3 ordinary country-event window already has a tablet-like frame with a Local News masthead. Its world-news window remains a separate 528 x 595 newspaper. The donor is `interface/eventwindow.gui`: the complete ordinary event window, adjacent shared option entry and world-news block were read. Native sprite mapping comes from the installed engine's `interface/eventwindow.gfx`.

Two further unapproved concepts use the actual MD frame pieces rather than drawing an unrelated generic tablet:

- **Tablet Dispatch**: Photo Dispatch as a digital agency report within the MD device. A larger wide photograph, one broad readable report field and a clear acknowledgement area accompany the retained Presswire identity.
- **Paper Dispatch**: the preferred teletype report appears as a paper document inside the same native device. It keeps the paper stock, typewriter headline and filing stamp while retaining normal MD-style options outside the document.

Native source pieces are `event_report_top_win.dds` (581 x 121), `event_report_tileable_midsection.dds` (580 x 66) and `event_report_bottom_win.dds` (581 x 206). Viewing copies retain every decoded RGBA pixel and the original alpha. Header branding and notices remain intact. Original artists and separate redistribution permission are unknown; MD/Paradox retain their rights. No global game font or native window is changed during this study.

The concepts are donor-composed external previews. Moving those frame pieces into world news still needs a proper native layout adaptation preserving actual news delivery, long titles, scrollable descriptions, pictures, the news grid and all event options. Copying the country-event window wholesale is not the proposed implementation. No paper/tablet choice, occupation rule or event delivery is installed by these previews.

The editable source is `md-tablet-dispatch-template.html`; `md-tablet-dispatch.html` is the built comparison. The authorized visualization directory also holds the donor provenance, source hashes and browser checks. The same generated colour illustration and fictional report are used in both alternatives. Runtime artwork, registrations and GUI hashes are checked unchanged.

## Non-tablet late Cold War study

Photo Dispatch remains the liked foundation. Following the tablet rejection, `cold-war-news-directions.html` presents three further unapproved concepts:

- **Agency Print**: the physical wire-service printout, retaining the larger wide colour photograph, typewriter heading, feed-paper detail and one continuous report.
- **Press Folder**: a press-bureau folder containing an editorial print, with the photo and report on the document. Its report uses print type for readability while agency labels retain the typewriter identity.
- **News Monitor**: a stationary colour CRT workstation with a substantial cabinet and stand. The news remains one simple report, without a handheld/tablet frame, modern app navigation, fictional streaming controls or animation.

These are original period-inspired interface proposals, not reproductions of a named historical newsroom system. They propose no new in-game hardware, technology unlock or automatic date-driven skin switching. The example date is 13 October 1986; it is a fictional report used for layout comparison. The unchanged generated illustration remains an illustrative reconstruction, not a documented photograph of the fictional incident.

The code-native frames and retained picture require no new image generation or recolouring. Runtime source/artwork hashes remain unchanged. A chosen variant would still need native news-window adaptation and checks for long titles, long descriptions, multiple real options, old wide pictures and the actual target game resolution. Browser verification does not establish native game behaviour.

## Neutral paper and depth refinement

The user then requested use of the shadow graphic, more depth and neutral white/grey instead of green. `agency-print-neutral-depth.html` refines the liked Agency Print / Photo Dispatch direction as a single concept, rather than introducing another device.

The interface palette is now achromatic white, grey and charcoal, including its filing strip, stamp, rules and button. The existing generated photograph remains in colour. Physical depth comes from two slightly offset paper edges, a cast shadow, a thin raised photo-print mount, a fine lit paper edge and restrained button relief. Local design controls adjust shadow depth, paper layers and report size.

The edge shading actually uses the native `GFX_popup_window_shadow` texture registered by MD in `interface/popupwindow.gfx`. Its source is inherited from `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/gfx/interface/popup_window/popup_window_shadow_bd_x79_y107.dds`, size 160 x 216, native border sizes x79/y107. The original RGBA texture is reused as a low-opacity nine-slice edge shade; its decoded pixels and alpha are retained in the viewing copy. Outer cast shadows and paper/photo relief are original code-native effects. No tablet chassis or MD Local News masthead is included.

Original native-shadow artist and separate redistribution permission are unknown. Existing Paradox/MD rights remain separate from the new design work. The viewing-source record includes the registration and texture hashes, palette checks and unchanged runtime hashes. The new concept does not repaint the retained photograph or install new game assets.

## Detailed newspaper study

30 October 2026. The user requested further detailed newspaper concepts. `newspaper-detail-studies.html` in the authorized conversation visualization directory presents five original neutral print directions:

- **World Ledger**: a traditional serif masthead, double rules, centred headline, framed wide photograph and a continuous serif report on layered newsprint.
- **Evening Report**: a condensed masthead and uppercase headline, heavy editorial rules, a full-width image and a compact article area.
- **Photo Edition**: a restrained review masthead followed immediately by the raised photograph. The large serif headline sits beneath the image and the report uses clean sans-serif type.
- **Press Cutting**: a clipped article mounted on grey backing, translucent tape, irregular lower paper edge, an inset photograph and a serif report.
- **Wire Edition**: continuous-feed paper with perforated margins, a generic press-copy stamp, monospaced text and a mounted wide photograph.

All five exclude fabricated datelines, location lines, page/edition numbers and image captions. Static mastheads are original fictional identities. The article is a fictional layout sample. The one continuous description and response area remain separate native content fields; there are no simulated secondary articles, adverts, stock quotations or automatically split newspaper columns.

Paper layers, fine fibre patterns, restrained folds, raised photo mounts and cast shadows supply the detail. The previously inspected native popup shadow is retained as low-opacity nine-slice edge shading. The generated illustration uses its existing approved crop, rebuilt from the source master at 1197 x 465 for the external preview. Its composition and colour are unchanged. The in-game 399 x 155 DDS remains untouched. Full source, artist/permission limitations, hashes and modifications are recorded in `newspaper-detail-studies-provenance.json` beside the study.

Per-design controls compare long headlines, long reports and four responses, and adjust type size, paper depth, grain, sheet layers and inset photography where applicable. Browser checks cover 120 combinations of five designs, three widths, two surrounding themes and four content samples. Long report endings and the fourth response are reachable. This is external layout verification, not native game verification or installation. The previous installation task remains separate and unfinished; none of these new alternatives is approved for runtime use.

## World Ledger selection and installation

Later on 30 October 2026, the user explicitly selected the first design, World Ledger, with the shown default settings and requested implementation. `APPROVED_WORLD_LEDGER.json` and `source/world_ledger_approved.html` freeze that approval. This supersedes the unapproved-concept status above and the previous Agency Print direction without rewriting their historical records.

World Ledger is now installed into the ordinary native world-news window. The paper raster is exported directly from the approved design with real-event fields hidden. The in-game title, picture, report and responses remain native. Separate serif fonts are registered through MD's `fontfiles` syntax. The complete non-news windows and shared event-option entry are retained.

## Compact native-size correction

The user subsequently supplied an in-game screenshot and requested the exact original MD size, dragging and original functions, followed by an explicit requirement that all text remain readable. This supersedes the 656 x 875 window dimensions. The current window and background are 528 x 595, with an unscaled 399 x 155 picture. World Ledger's paper, masthead, rules and depth remain; the immutable earlier approval is retained as a historical input.

The complete MD 2.0.3 donor now supplies the root geometry, original background registration, movement flag, sounds, hierarchy, news grid and uncut native option container. Only visual fields are adapted. The previous mouse-transparent custom background registration is removed, along with the added clipped option wrapper. Actual event titles and reports are kept whole, in separate native scrollable text controls. Browser checks reach the final words of a long headline and report without photo or footer overlap. Current source, file, provenance and text checks are in `FINAL_REPORT.json`; no computer-use actions or game launches are used for this correction.

`build.py --install` and `build.py --check` passed for all 14 runtime files. `install_receipt.json` records the verified E: backup and exact installed hashes. `FINAL_REPORT.json` records installed-file, parser, encoding, bitmapfont-reference and approved-paper checks. Native startup was reached during the earlier private attempt; the actual news-window interaction checks were interrupted. At the user's request, installation was completed without any further computer-use actions, game launches or UI input. `NATIVE_REPORT.json` records that evidence limit. Restarting the game loads the new interface. No live multiplayer behaviour is claimed by these checks.
