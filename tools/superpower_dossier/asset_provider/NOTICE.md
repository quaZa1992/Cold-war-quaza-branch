IMPERIA COLD WAR: current native test asset provider
=================================================

The `gfx`, `map`, `sound` and `music` directories are directory junctions to the corresponding directories of this workspace. They are used only to read the current mod assets during the isolated dossier UI test. Do not write, delete, move or regenerate files through these junction paths. Runtime script sources and private dossier fonts/art are copied into each separate snapshot.

This provider contains no country history, events, common scripts, interface definitions or localisation. The test descriptor preserves the source mod's original asset replacement masks. Original authorship and licence/permission of the inherited assets remain as documented by their original notices; individual asset-specific information is unknown here. The junctions make no ownership claim and are ignored by Git.
