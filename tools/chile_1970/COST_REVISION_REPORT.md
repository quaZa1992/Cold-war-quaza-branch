IMPERIA COLD WAR — Chile 1970 static monetary cost revision report

## Basis and method

The 1 January 1970 native run records Chile GDP as 31.48733 internal billion and GDP display as 9.26097 historical-1970 billion. The scenario uses a 3.4 display conversion for GDP; treasury costs stay in internal units and do not receive that conversion. The overlay therefore uses a fixed factor of `0.05` against approved internal-bn values, not a new dynamic GDP pricing mechanism.

The Python overlay reads the approved JSON into memory, deep-copies it, and scales only the specified money fields: focus node `money`/`weekly`; agreement Chile and recipient `setup`/`weekly`; event-option `money`/`weekly`; and decision-contract `money`/`weekly`. It uses Decimal arithmetic and `ROUND_HALF_UP` to five decimal places. Existing zero values remain zero. For positive values, an exact half step such as `0.000025` rounds to `0.00003`. Rewards, modifiers, requirements, prerequisites, text, and layout are unchanged. `approved_design.json` remains the source-of-truth design and is never rewritten by the overlay.

## Magnitudes

| Measure | Approved amount | Revised amount | Revised share of 31.48733bn GDP |
| --- | ---: | ---: | ---: |
| Largest individual focus or decision cost | 6bn | 0.30bn | 0.953% |
| Largest individual event-option cost | 3bn | 0.15bn | 0.477% |
| Largest individual bilateral setup fee | 4bn | 0.20bn | 0.635% |
| All nine Chile-side agreement setup fees | 19bn | 0.95bn | 3.017% |
| All nine recipient-side agreement setup fees | 15bn | 0.75bn | 2.382% |
| Summed focus-node setup amounts, across mutually exclusive routes | 295bn | 14.75bn | Not an attainable route total |

With per-field five-place rounding, the highest party weekly focus stream is the non-party-specific stream at about `0.00038bn/week`; the largest party-specific total is the military programme at `0.00035bn/week`. All nine accepted agreements add about `0.00061bn/week` in Chile plus `0.00039bn/week` across recipient countries. A conservative Chile-side combination of the highest party stream and all agreement streams is therefore about `0.00099bn/week`, around 0.14% of the native log's 0.72514bn weekly income. The nine recipients' combined additional cost is about `0.00039bn/week` across those countries. These figures sum fees only; they do not assert that every focus or agreement is reachable at once.

The reduction from one-time fees of 1–6bn to 0.05–0.30bn keeps the previous ordering of costs while bringing the largest single setup cost below 1% of the measured 1970 GDP baseline. Fees above the revised ceiling should be treated as exceptional and justified separately by project scale or outside financing.

## Verification

`test_costs.py` checks that the approved input is unchanged, every designated cost field is scaled with the configured factor and rounding, zero costs remain zero, unrelated fields remain identical, the half-up boundary is respected, and invalid costs are rejected. The test module was run with the bundled Python runtime: 6 tests passed. No engine run was performed as part of this cost overlay.
