IMPERIA COLD WAR

Design-only US foreign-policy and Kurdish chapter layout review, 2026-10-28.

No loaded tree, generator, sprite registration or immutable approval was changed.
This note measures the current donor and proposes a footprint. It does not claim
a native screenshot, rendered final proposal or engine-verified connector route.

## Current source and ownership

The current `common/national_focus/USA_1970.txt` has 301 direct focus IDs and
300 visible cards. Its inspected SHA256 is
`5d18bafd4d1c972115cb2f7cd9395e6694de33ab8a8b6209fc6f82c777c1f32b`.
The direct tree spans x=-33 through x=38 and reaches y=58. Coordinates include
fractional x positions, so a resolver must use floating-point values.

The existing Gulf pocket is already a fifteen-ID programme, rather than the
older six-card screenshot. Its owner is `tools/iraq_1970/usa_module.py`, called
through `tools/usa_1970_expansion/gulf_revision.py`. The latter preserves all
fifteen IDs and moves the pocket using the Desert Storm anchor. Do not run it
for this proposal or overwrite those programme receipts.

| Existing suffix after COLDWAR_USA_gulf_ | Current position | Existing dependency |
| --- | --- | --- |
| desert_shield | 30,0 | Independent crisis entry |
| desert_storm | 34,0 | Independent crisis entry |
| coalition | 38,0 | Independent crisis entry |
| appeal | 34,1 | Shield OR Storm OR Coalition |
| contacts | 34,2 | Hidden legacy receipt, keep hidden |
| limited_war | 32,2 | Appeal; excludes Arm the Front |
| arm_front | 36,2 | Appeal; excludes A Limited War |
| northern_access | 30,3 | Independent access programme |
| comfort | 34,3 | Independent humanitarian programme |
| safe_haven | 32,4 | Comfort AND Northern Access |
| no_fly | 36,4 | Comfort AND Northern Access |
| assembly | 32,5 | Safe Haven |
| baghdad_accord | 30,6 | Assembly |
| self_rule | 34,6 | Assembly |
| recovery | 32,7 | Baghdad Accord OR Self-Rule |

The labels come from `localisation/english/COLDWAR_USA_gulf_l_english.yml`.
Existing Open Northern Channels is `appeal`; the hidden `contacts` card should
not be revived as a second visible early-support entry.

## Native visual reference

The inspected `interface/nationalfocusview.gui` has a 165x128 focus container,
a 147x20 title area using `hoi_16mbs`, and a symbol placed above the titlebar.
The inspected bar texture is 164x50. The existing installed renderer uses a
96x130 focus grid. A two-column centre gap is 192 pixels, leaving only 27 pixels
between containers; a four-column gap is 384 pixels. These are current donor
measurements, not universal engine limits.

Useful existing assets, under `gfx/interface/goals/`, are:

| Sprite and relative texture | Actual texture size |
| --- | --- |
| army_reform: 00_army/army_reform.dds | 97x86 |
| focus_generic_supply_line: 00_army/focus_generic_supply_line.dds | 100x88 |
| diplomatic_treaty: 00_diplomacy/diplomatic_treaty.dds | 82x83 |
| government_beu: 00_politics/government_beu.dds | 85x85 |
| welfare: 00_politics/welfare.dds | 96x86 |
| self_management: 00_politics/self_management.dds | 100x88 |
| Election_graphics: 00_politics/Election_graphics.dds | 94x80 |
| air_superiority: 00_airforce/air_superiority.dds | 102x90 |

The native bar is available at the installed game's
`gfx/interface/focusview/titlebar/focus_unavailable_bg.dds`. No Kissinger sprite
or character match was found in the current target interface registrations or
character providers. A new portrait icon should depict him circa 1970, in his
late forties, with dark wavy hair and distinctive spectacles. His much older
public image would be the wrong period. Use compact painted focus artwork and
an appropriate metallic frame rather than an oversized photograph.

## Proposed footprint and hierarchy

The current defence cluster occupies approximately x=21..25, y=1..12; the
adapted naval cluster occupies x=23..32, y=16..21. Direct cards stop at x=38.
A Kurdish chapter can therefore start at x>=43 without intersecting those
current direct-card containers. This does not yet certify conditional imported
shared-focus states.

Suggested country-column centres are Iraq43, Iran51, Turkey59 and Syria67,
with entries near row5 and meaningful policy follow-through through row13.
Eight grid columns per country leave room for genuine two-way forks at centre
minus2 and plus2. Keep a shared THE KURDS hub above these columns. Larger
foreign-policy theatres should sit in their own neighbouring cluster, rather
than be threaded through these four country columns.

If actual implementation follows this design, moving the complete Gulf pocket
to a Desert Storm centre at43,16 would put its retained cards in x=39..47,
y=16..23, clear of the current naval footprint. Early Iraqi Kurdish support can
then appear above it. This is a proposed move, not an implemented coordinate
change. The final full-tree preview must include the retained defence and naval
neighbours and the whole existing Gulf pocket.

## Logical review requirements

- Keep Kuwait intervention independent of prior covert action. The user wants
  early Kurdish support, but failure to fund that support must not prevent a
  response to an Iraqi invasion of Kuwait.
- Funding, local contacts and arms shipments are generally complementary.
  Reserve exclusions for genuinely different political commitments, such as
  accepting negotiated autonomy versus guaranteeing unilateral separation.
- A common continuation after any country campaign uses one prerequisite block
  containing the alternatives. Do not require all four target campaigns at an
  AND join, which can be impossible under their diplomatic conditions.
- Preserve local Kurdish political agency and the existing postwar relief,
  access, assembly and settlement paths. A new regional contest should not
  bypass them with an automatic independent state.
- Distinguish a historical Iraq programme from counterfactual operations against
  the Shah's Iran or NATO Turkey. Give alternative escalation a visible
  diplomatic cost and meaningful context; do not silently label every target
  an existing American enemy.
- Offer acceptance, such as a consenting transit partner, must expose both
  countries' prospective numerical effects while unsigned. Hostile covert
  pressure instead requires warning and practical defender counterplay, rather
  than consent from its target.

Every concept card, including locked and excluded ones, should be clickable.
Use an inspector that leaves the selected focus visible, clear OR/AND joins,
normal-scale icon/title views and a full-tree overview. Keep simulation controls
separate from focus geometry. Mark generated icon concepts and the mockup as
design material, not installed sprites or running-game evidence.

## Provenance and verification boundary

This review reads current IMPERIA COLD WAR source, installed HOI4/MD donor
geometry, and the existing native renderer. Original Paradox, Millennium Dawn
and project attribution remains under the source providers and
`IMPERIA_COLD_WAR_NOTICE.md`. Separate individual credits or redistribution
permissions are unknown where existing notices do not identify them. No binary
asset was copied or altered by this review. Historical verification is handled
by the separate mechanics/reference reviewer. Final concept render review is
pending receipt of the parent's draft.
