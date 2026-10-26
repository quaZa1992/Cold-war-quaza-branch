# Energy and Power-Plant Balance

Read before touching a power-plant building, an energy technology, or the renewable
hotspot system. Hydroelectric and geothermal are separate systems.

## Model

Cost-effectiveness is power output per unit of build cost:

```
metric = base_GW * state_factor * (1 + sum of power techs)
         / (base_cost / (1 + sum of construction-speed techs))
```

- `base_GW` and `base_cost` come from `common/buildings/00_buildings.txt`
  (`*_energy_gain` and `base_cost`). With no techs, fossil is the most cost-effective,
  then nuclear, then renewable.
- Build cost is `base_cost`, the construction effort. It is not the `$` figure in the
  building header comments, which belongs to the investment system.
- `state_factor` is `state_renewable_capacity_factor_modifier`. It applies to renewables
  only, averages 1.0, and upstream sets it with a balance script that is not in this
  repository.
- Runtime formulas: `00_money_system.txt` (per-state generation) and
  `!_energy_effects.txt` (country roll-up and the renewable monthly random).

## Intended timeline

At state factor 1.0, by techs alone:

```
fossil  < 2015 <  nuclear (fission)  < 2020 <  renewable  < 2060 <  nuclear (fusion)
```

Each source's cumulative tech bonus, for power and for construction speed, follows a
logistic S-curve. Fossil has one small curve that rises early. Renewable has one large
curve with a steep rise through the 2010s and 2020s and a plateau near 2040. Nuclear
has two stacked curves: fission (about 1990 to 2015) and fusion (about 2050 to 2065).
The amplitudes are solved so the crossovers land on 2015, 2020, and 2060.

## Upkeep relief

Each energy tech also lowers the weekly upkeep of its own plant type. `update_infra_rate`
in `00_money_system.txt` computes per-source expense as plant count times per-plant rate
times the source's multiplier: `infra_cost_multiplier` plus
`nuclear_infra_cost_multiplier_modifier`, `fossil_infra_cost_multiplier_modifier`, or
`renewable_infra_cost_multiplier_modifier`. The relief follows each source's power curve
and reaches `INFRA_CAP` (-0.40) on a fully researched chain.

## Tools

- Upstream, `tools/balance/set_energy_tech_scurves.py` owns the numbers (not in this
  repository; the values in this 2.0.2 tree may predate it). It solves the curves and
  writes the per-tech power, construction-speed, and upkeep values into
  `common/technologies/industry.txt`. Retune by editing its `SHAPE`, `SPEED_RATIO`, `PF`,
  and `INFRA_CAP` constants and running `--apply`. Hand edits to those tech values are
  overwritten.
- Upstream charts power per build cost with `tools/analysis/renewable_power_per_cost.py`
  (not in this repository). Recompute crossovers by hand after a change.
- Energy technologies, buildings and costs here must still make sense for a 1970
  start: renewables that are research-gated in the 2000s should not be available or
  cheap in the early 1970s.

## Not in the model

- The renewable monthly random(0..1). A renewable plant averages about half its rated
  output, so real renewable crossovers land a little later than the chart.
- Fuel upkeep, which only favors renewables.
