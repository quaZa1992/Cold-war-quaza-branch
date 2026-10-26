# Localisation Smoke Checklist

The static checker proves a `.yml` file is well formed (BOM, header, key syntax,
duplicates, unclosed colour codes). Only the game proves dynamic text renders. Run this
list by hand after a change to dynamic localisation (scripted localisation, `[...]`
getters, variables in tooltips, FROM/PREV text) and report it apart from the static
result.

## What to record

Write one block per run in the PR or issue:

```text
Commit:        <git rev-parse --short HEAD>
Game version:  <bottom-left of the main menu, e.g. 1.19.3>
Playset:       MD Cold War (+ any test mod)
Bookmark:      Cold War 1970
Clients:       1 (single player) | 2 (multiplayer)
Date:          <YYYY-MM-DD>

| Row | Expected text | Observed text | Pass |
|-----|---------------|---------------|------|

error.log: <lines that name a key, "loc", "color", or "unknown", or "none">
```

`error.log` is in `Documents/Paradox Interactive/Hearts of Iron IV/logs/`. Delete it
before the run so it holds only this session. Attach a screenshot for every failed row.

## Setup

1. Start the 1970 bookmark with the country named in the row.
2. Open the console (the key left of `1`). `focus.autocomplete` finishes focuses in a
   day, `tag <TAG>` switches the played country, and `event <id>` fires an event for
   the played country.
3. A console-fired event has no real FROM or PREV. Use it only for strings that read
   no other scope. For sender/recipient text, trigger the real action and switch tags,
   or better, use two clients.

## Building rows

Derive rows from the change, one per distinct dynamic string:

| Kind                  | How to reach it                                     | Fails when                                      |
| --------------------- | --------------------------------------------------- | ----------------------------------------------- |
| Percent / points      | Hover the decision or focus that shows the value    | `500%` instead of `5%`, or a raw `[?var]`       |
| Money                 | Hover the cost or payout tooltip                    | Missing amount, wrong sign, broken icon         |
| Getter with a flag    | Open the GUI or decision list that names a country  | Literal `[TAG.GetName]` or empty name           |
| Sender side           | Acting country takes the action                     | Wrong country named as actor                    |
| Recipient side        | Switch to the target (or second client)             | Recipient text names itself as the sender       |
| Gated party / leader  | Politics view on 1 January 1970, then after the gate | Inherited 2000-era name shows at 1970           |
| Expiry / deadline     | Let a proposal time out (pause, resume, then wait)  | Deadline text wrong after pause or reload       |

Rows that need a long game or rare state are marked `not reached` rather than forced
from the console.
