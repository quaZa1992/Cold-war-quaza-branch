# Regional1970 runtime

`compile.py` consumes the completed `assets.json` in each country directory.
Every character requires both an existing large and small portrait. A missing
military portrait omits that person altogether. Unrepresented political slots
use an institutional emblem, never somebody else's face.

Run the asset builder first, then:

```powershell
python tools/eastern_mediterranean_1970/compile.py
python tools/eastern_mediterranean_1970/validate_runtime.py
```

The generated character files cover the reviewed Greek/Turkish roster and the
photographed Cypriot commanders. Cyprus political leadership remains owned
by `tools/cyprus_1970/`. No other Cypriot army chief receives a substitute face.
The compiler does not modify research photographs, generation records, source
prompts, the Cyprus tree or the Cyprus compiler/runtime.

Dates determine when a person can be recruited or newly appointed as a service
chief/advisor. These are separate windows: a division commander does not become
the army chief at the scenario start merely because his portrait exists.
Ranks/strategic skill scores are balance values, not a historical assessment.
Year/month boundaries marked approximate in the research remain approximations.

The daily pulse recruits available candidates and removes any accidentally
recruited native modern roster. It never appoints a cabinet, calls an election,
changes party popularity, switches the governing political slot, launches a
coup, begins a war or schedules a historical assassination. Existing historical
field commanders are not dismissed at the end of their recruitment window.
Georgitsis is the explicit exception: his recruitment requires an actual active
Cypriot coup regime, and he is removed when that regime actually ends. This
does not start a coup or authorize foreign action.

Greece and Turkey intercept MD's central leader dispatcher only for a1970-start
campaign, before its modern kill/rotation path. All24 MD political slots are
handled, with historical names only for supported political currents. The
existing modern dispatcher remains available to later scenario starts.
Political representatives can be selected by human decisions for the current
political slot. Presidents/regents are distinct political advisors; choosing a
prime-minister/party representative does not appoint the head of state.

Calendar changes do not replace the incumbent. A newly available party leader
is an optional choice. A selected representative is revalidated against the
applicable window if MD is explicitly asked to dispatch leadership again;
historical coup-related bans are not unconditional calendar cutoffs. No1980
Turkish coup is implied by the dates in the research manifest.

Small custom traits use only existing MD keys: political power+3%, bureaucracy
cost−3%, foreign-influence defence+3%, army organization+3%, naval experience
gain+3% or air mission efficiency+3%. They are ordinary advisor traits with a75PP
appointment cost. No political decision grants a repeatable reward.

`runtime_roster.json` records the actual compiled subset; `runtime_build.json`
records omissions and the files written. The validator parses the generated
scripts, checks portrait paths and advisor windows, confirms all48 political
slots, checks that modern retirements are guarded, rejects sovereign actions,
checks the coup-only recruitment and verifies byte-for-byte regeneration.
These checks do not replace a game launch and in-game UI/save test.
