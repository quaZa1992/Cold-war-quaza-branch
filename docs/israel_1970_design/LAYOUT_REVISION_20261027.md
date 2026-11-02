IMPERIA COLD WAR: Israel 1970 layout revision 10

The layout is authored in `tools/israel_1970/layout.py`. It preserves all focus
IDs, rewards, costs, grouped prerequisites, exclusions and political gates. No
party branch is hidden. The compiler and preview consume the same positions.

National institutions occupy the upper terrace: economic development and social
institutions on the left, the Knesset in the centre, the armed forces and foreign
policy on the right. The security and territorial choices continue beneath
foreign policy. Political families occupy the middle terrace, with extra space
for the Alignment's succession programme and Gahal's coalition choices. All six
policy programmes share one lower terrace, ordered from citizenship and finance
through settlement policy, Sinai development, civil status and radical routes.

This removes the former second policy shelf at row 42. The 389 existing focuses
now span x=4 through x=145 and y=0 through y=34. The earlier installed design
spanned x=-4 through x=123 and y=0 through y=50. The bounding rectangle decreases
from 129 by 51 to 143 by 35 grid units, a reduction of approximately 24 percent.
The extra width allows distinct policy footprints and reduces vertical travel.

The military preparedness join now sits inside the reserve and air-defence
cluster. The armour programme leaves the vertical General Staff to intelligence
corridor clear. The industrial electronics chain continues directly below the
power grid rather than leaving an empty row. Cabinet and territorial choices
use three-unit forks for clearer paired alternatives.

Revision 8 accommodates the separately authored roleplay graph: military policy
and the civilian territorial cabinet programme form two independent roots.
Attrition posture, diplomatic contacts and a negotiated ceasefire are no longer
drawn as a mandatory historical sequence. The military root lies on the left,
with separate attrition and diplomatic lanes. The territorial root lies on the
right, with its strategic alternatives and direct Golan/Gaza administrative
branches. Sinai negotiations, West Bank autonomy and permanent administration
continue below those choices. This geometry does not itself rewrite the graph.
An isolated check using the parent compiler's specified new prerequisite groups
found no card overlaps, upward links or connector intersections across 389 nodes.

Revision 9 adds the ten-focus external-association and controlled-development
group at origin (67,38). Its independent roots resolve to (59,38) and (75,38).
Four foreign offers occupy x=53,57,61,65 at row 40; four controlled-state
development focuses occupy x=69,73,77,81 at row 40. Neither spine intersects the
six policy blocks above it. All previous 389 coordinates are preserved. An
isolated 399-node check finds no same-row overlaps, upward links or connector
intersections. The 143 by 41 bounding rectangle gives 14.69 grid cells per
focus, below the existing validator's 17.99 threshold. Generated-output and
rendered verification of this new group remain separate checks.

Revision 10 supersedes the wide revision 9 association block with two stacked,
independent fans at origin (67,36). The external-association root is at (67,36),
with its four offers at x=61,65,69,73 on row 38. The controlled-development root
is at (67,40), with its four territorial projects at the same four x positions
on row 42. This reduces the new group's width from 28 to 12 coordinate units,
allowing a larger fit zoom and clearer title text in the branch preview. All
previous 389 focus coordinates remain unchanged. The 399-node in-memory geometry
check again finds no card overlap, upward prerequisite or connector intersection.
The full bounding rectangle is 143 by 43, giving 15.41 grid cells per focus,
below the existing validator's 17.99 threshold. Source and render verification
remain separate checks.

The local reference is Millennium Dawn 2.0.3, supported game version 1.19.*,
Workshop item 2777392649. Its generic tree uses a one-row descent and two-unit
spacing for paired branches, for example cabinet reform at x=-4, y=1 and
strengthen government at x=-2, y=1 relative to political reform. Its Russia tree
contains 800 relative-position references. These establish the native coordinate
and anchoring pattern; they do not determine this country's exact canvas size.

An isolated check of the new coordinate model covered all 389 nodes and all
visible prerequisite connectors. It found no same-row card collisions, upward
prerequisites or orthogonal preview connectors crossing unrelated focus cards.
The check uses the existing preview's 80 by 190 unit conversion and 148 by 160
card bounds. These are external-preview assumptions, not observed HOI4 routing.
Policy-local positions and grouped prerequisites remain unchanged.

The layout metadata suggests an initial camera at x=53, y=0. The compiler must
consume this value, since its former x=34 literal would open away from the new
Knesset root. Existing focus shortcuts target IDs and continue to resolve.

Pending verification: rebuild generated code, compare its resolved coordinates
and anchor declaration order, inspect the full overview and normal-size branch
renders, check all-party visibility and click inspection, and inspect the actual
tree in HOI4. This document does not claim those later checks passed.
