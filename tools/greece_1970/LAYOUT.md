# Greece 1970: structural review against Millennium Dawn Russia 2000

The reference was checked directly in the installed Millennium Dawn Workshop
source:

`E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_russia.txt`

SHA-256: `db03d72e1fdbc239076eba9f7e9259e1791e909eab425186304cd6b14858b602`.
Its geometry matches the local `common/national_focus/05_russia.txt`. The local
differences concern tree selection and two removed aircraft research bonuses;
they do not change the layout used as the reference.

## Concrete comparison

Russia contains 806 directly defined focuses, resolved to x=0..235 and y=0..26,
with six sector shortcuts. Political alternatives spread horizontally from the
initial political area; the economy and military have their own upper-level
anchors. Subsectors use local branches, asymmetric arrangements, parallel work,
and later joins. Camera position and continuous-focus position are explicit.

The archived Greek design instead extends to y=117. Seven almost identical
political diamond chains sit below the regime tree; six more policy chains sit
below the parties. This makes unrelated programmes look like successive stages
and requires substantial vertical scrolling. Several genuine event-driven roots
are mixed into those chains without an explanation of their independence.

`layout.py` keeps the 313 IDs and all gameplay payloads, applies a separate layout
to the in-memory design, and leaves the original JSON intact. All sectors now
start beside one another. Political settlement and elections remain in the
central initial view. The resulting bounds are x=1..272 and y=0..25. The wider
horizontal spread allows label clearance and retains the event-driven Cyprus
response shelves without compressing them into ordinary political programmes.

## Dependency changes

The 60 prerequisite overrides each have a machine-readable reason in the
returned `prerequisite_overrides` metadata.

* Political parties retain their constitutional choice before any programme.
  Economic and diplomatic work then run in parallel. Their later settlement
  combines the fiscal programme with either diplomatic strategy; domestic
  administrative follow-through can proceed while foreign negotiations wait.
* Economy has three visible arms for production, rural development, and
  tourism/coastal policy. The tax and resilience focuses join those programmes.
* Army keeps command reform as its common spine and divides defence planning
  from procurement. Exercises and final doctrine bring those arms together.
* Navy separates fleet mission and island support, then adds merchant-marine
  policy. Rescue and fleet sustainability combine the results.
* Air force separates combat mission and technical training. Airfield planning
  can proceed while foreign instructor negotiations remain unresolved; the
  final aircraft programme requires availability and a procurement budget.
* Foreign policy separates Europe, USA/NATO and regional diplomacy. Choosing
  continued security exceptions still blocks European rehabilitation, as the
  original availability gate requires. It no longer also blocks American base
  policy and all Balkan/Mediterranean work. The European dossier has the one
  valid monitoring predecessor rather than a misleading alternative that its
  existing availability condition would reject.

No original exclusion, funding cost, event condition, reward, modifier, leader
condition or political mandate is edited. The civilian-transition sequence and
all political root eligibility gates are unchanged. In particular, Cyprus crisis
and factual-outcome roots remain independent: events can occur without Greece
first completing a dossier or participating in a coup. An unanswered response
window still permits Greek action without inventing a foreign response.

## Navigation and integration

Import `apply_layout` in `compile.py` and call it immediately after loading the
JSON, before `NODES`, `BY`, modifier-slot or reward tables are constructed:

```python
LAYOUT = apply_layout(D)
NODES = D['focuses']
```

Use `LAYOUT['initial_show_position']` and
`LAYOUT['continuous_focus_position']` in the tree header. Existing section
shortcuts continue to work; the section anchors are kept consistent. Add the
four `extra_shortcuts` using the existing shortcut/localisation helper: civilian
elections, Cyprus crisis response, Cyprus outcome/relief, and credit financing.
Every node has `search_filters` using existing MD filters; emit these with the
native `search_filters` block. No additional GUI assets or new filter labels are
needed. Metadata is suitable for a generated `layout_review.json` manifest.

The validator must apply the same transform to its own JSON load before
comparing emitted geometry and prerequisites. Its design-file hash should still
refer to the untouched JSON. Existing hardcoded civilian-transition and party
entry tests require no sequence changes; party programme or specialist-arm
tests should follow the new explicit prerequisites instead of assuming that
every 20-focus section is the same serial template.

## Structural QA

`python tools/greece_1970/layout.py` reads the design and prints metadata without
writing runtime files or opening a preview window. The checks report:

* All 313 focuses positioned; zero duplicate coordinates.
* At least two horizontal grid units between focuses on the same row.
* Every prerequisite points to an earlier row; no missing IDs or graph cycles.
* All 313 focuses have at least one prerequisite history compatible with their
  mutually exclusive choices. The checker backtracks through OR and AND groups;
  a simple reachability walk would miss impossible exclusive-branch joins.
* Zero prerequisite-line overlaps with foreign focus icon/label bounds under
  either tested orthogonal routing: a horizontal gutter below the parent or
  above the target. Long edges were specifically repositioned to clear both.
* A payload guard rejects changes outside geometry, prerequisites and native
  search filters.

These are static checks, not an engine rendering test. The renderer's exact
line routing and text placement are closed-source. No live window was opened.
