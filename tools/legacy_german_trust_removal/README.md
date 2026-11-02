# IMPERIA COLD WAR — Legacy DDR trust removal

This bounded transform removes the two 1985 legacy DDR meters, `DDR_state_trust` and `DDR_moscow_trust`. It only touches the five allow-listed script files and two English localisation files in `remove_legacy_german_trust.py`; it does not rewrite any complete national-focus, event, or modifier file from a generator.

Run `python tools/legacy_german_trust_removal/remove_legacy_german_trust.py --apply` to apply or reapply the transform and validate it. Run the same command without `--apply` to validate only. The script preserves script UTF-8 without BOM and localisation UTF-8 with BOM, and retains each file's line endings.

Focus and event rewards that affected either meter lose only those variable writes. Their unrelated effects remain. The Bonn focus effect, DDR events, and western pressure effects likewise lose only their legacy trust writes. The dynamic crisis modifier itself remains in place.

The old trust inputs were removed from mixed derived formulas. Their remaining control and pressure inputs retain their original signs and divisors; outputs now respond only to those independent inputs:

| Derived output | Remaining inputs | Divisor |
| --- | --- | ---: |
| Stability factor | SED control + NVA loyalty - reform pressure - emigration pressure - mass protest pressure - supply pressure | 2600 |
| Drift defence factor | SED control + Stasi penetration - West media penetration - West dependency | 1100 |
| Communism drift | SED control - reform pressure | 2600 |
| Nationalist drift | NVA loyalty + border crisis pressure + emigration pressure | 2400 |
| Resistance growth | reform pressure + mass protest pressure + emigration pressure + youth unrest - Stasi penetration | 2000 |
| Productivity growth | West dependency + KoKo funds - supply pressure - SED control - emigration pressure | 2200 |
| Bureaucracy cost | SED control + supply pressure | 2200 |
| War support factor | NVA loyalty + border crisis pressure | 2400 |
| Army organisation factor | NVA loyalty - regime panic | 2200 |

The two outputs that previously used a trust meter as their `set_variable` initializer now initialize to zero before applying their independent terms. No trust variable, frozen offset, or replacement meter remains in the 1985 runtime. Existing save values for the two removed variables can remain unused until a separate save migration clears them.

This change does not add an initialization call or set `DDR_state_crisis_system_enabled`; the prior 1985 crisis system is still inactive unless another authorized change activates it. The separate 1970 meter is handled outside this bounded transform, which does not read or write 1970 files or GUI.

The validator checks the allow-listed scripts for legacy meter tokens and BOM errors, and checks each affected derived formula's remaining independent inputs and original divisor. It rejects fixed trust offsets. It also checks that both localized crisis descriptions no longer list the meters and retain BOMs.
