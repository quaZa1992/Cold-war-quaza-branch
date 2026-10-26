# Independent GCC layout review

Status: **pass**, no outstanding layout finding. Review reads emitted game
files independently of the GCC compiler and compares the14 retained nodes to
the actual native `gulf_shared.txt` relative positions and grouped prerequisites.

The shared GCC root is32/11 in the349-focus generic host used by Saudi Arabia,
Kuwait, Qatar, Bahrain and Oman. The UAE conditional offset16/7 places it at48/18
beside the110-focus national host's diplomacy section. Native economic,
defence and political columns remain intact. Every host has a GCC shortcut;
existing initial camera and continuous-panel positions remain unchanged.
The Union shared tree is correctly excluded: its actual country trigger does
not contain any of the six Gulf states.

Measured using actual96×130px native focus spacing and complete icon/titlebar
rectangles: zero GCC/GCC or GCC/host card overlaps, and zero unrelated card
intersections with the simulated orthogonal GCC/host links. The two defence
finales retain both native prerequisite groups, requiring Officer Exchanges
and Joint Staff Liaison together.

Three labels initially exceeded the native147px field and were corrected:
Economic Agreement, Joint Investment and Council Meetings. Every new title
now fits; the widest is Procurement and Repair at141px in `hoi_16mbs`.

The reviewer opened all five generated proofs:

- `GCC_BRANCH_NATIVE.png`: native-scale complete14-focus branch.
- `SAU_HOST_OVERVIEW.png`: complete349-focus host plus GCC.
- `SAU_GCC_NEIGHBOURS_NATIVE.png`: GCC with nearby existing generic sections.
- `UAE_HOST_OVERVIEW.png`: complete110-focus host plus GCC.
- `UAE_GCC_NEIGHBOURS_NATIVE.png`: GCC, existing diplomacy and industrial neighbours.

These use actual sprite textures, native titlebars and native bitmap glyphs.
The reused art depicts appropriate economic, military and consultation themes;
no unrelated country's flag was visible in the14 new focus icons. Connectors
are approximate, unavailable cards are shown uniformly, and the overview
images are scaled. In-game routing, branch loading, scrolling, shortcuts and
hover behaviour remain untested. Preexisting generic labels that exceed their
fields were not changed by this additional-branch review.

Reproduce: `python tools/gcc_1970/preview.py`.
Detailed geometry and source hashes: `LAYOUT_REVIEW.json`.

After the UAE compiler rebuild, the separate Qatar identity regression also
passed205 checks: `python tools/historical_politics_1970/test_qatar_identity.py`.
