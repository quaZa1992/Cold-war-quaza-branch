// IMPERIA COLD WAR — Persistent design-only regional contest model.
const KSContestModel = (() => {
  const policies = ['routine', 'security', 'investment', 'autonomy'];
  function initial(base) {
    return {day:0, levels:[...base], sustained:0, warning:0, resetDays:0,
      opened:false, investmentDays:0, pacification:0, usSpent:0, defenderSpent:0,
      history:[[0, Math.max(...base)]]};
  }
  function restore(value, base) {
    if (!value || !Number.isSafeInteger(value.day) || value.day < 0 ||
        !Array.isArray(value.levels) || value.levels.length !== 4 ||
        !value.levels.every(v => Number.isFinite(v) && v >= 0 && v <= 100)) return initial(base);
    const run = initial(base);
    run.day = value.day;
    run.levels = [...value.levels];
    for (const key of ['sustained','warning','resetDays','investmentDays','pacification','usSpent','defenderSpent']) {
      if (Number.isFinite(value[key]) && value[key] >= 0) run[key] = value[key];
    }
    run.sustained = Math.min(30, run.sustained);
    run.warning = Math.min(45, run.warning);
    run.pacification = Math.min(100, run.pacification);
    run.opened = !!value.opened;
    if (Array.isArray(value.history)) {
      const points = value.history.filter(p => Array.isArray(p) && p.length === 2 &&
        p.every(Number.isFinite) && p[0] >= 0 && p[0] <= run.day && p[1] >= 0 && p[1] <= 100);
      if (points.length) run.history = points.slice(-54).map(p => [...p]);
    }
    return run;
  }
  function inspect(run, controls) {
    return {...run, unrest:Math.max(...run.levels),accepted:controls.policy === 'autonomy' && controls.settlement,
      hot:run.levels.filter(v => v >= 80).length};
  }
  function advance(source, controls, days, weekly) {
    const run = restore(source, source.levels);
    const accepted = controls.policy === 'autonomy' && controls.settlement;
    const policy = policies.includes(controls.policy) ? controls.policy : 'routine';
    const support = controls.delivery === 'active' && !accepted ? [0,.7,1.5,2.8][controls.funding] : 0;
    const actualUSWeekly = controls.delivery === 'active' && !accepted ? weekly.us : 0;
    for (let step = 0; step < days; step++) {
      run.day++;
      if (policy === 'investment') run.investmentDays++;
      // Successful operations leave a lasting local effect. Withdrawal does not erase it.
      const rebuilding = policy === 'security' && controls.divisions > 0 ?
        .5*Math.min(1,controls.divisions/2) : policy === 'investment' ? .14 : accepted ? .2 : -.1;
      run.pacification = Math.max(0,Math.min(100,run.pacification+rebuilding));
      const governance = policy === 'security' ? 3 : policy === 'investment' ?
        (run.investmentDays > 42 ? 2.1 : 0) : policy === 'autonomy' ? .5 : 0;
      run.levels = run.levels.map((v,i) => Math.max(0,Math.min(100,
        v + ((1 + support*1.9 - controls.divisions*1.2 - governance - run.pacification*.08) *
        [.95,1.05,.85,1.12][i] - (accepted ? 4.5 : 0))/7)));
      if (run.levels.filter(v => v >= 80).length >= 2 && !accepted) {
        run.resetDays = 0;
        if (run.sustained < 30) run.sustained++;
        else run.warning = Math.min(45,run.warning+1);
      } else {
        run.resetDays++;
        if (run.resetDays >= 15) { run.sustained=0; run.warning=0; run.opened=false; }
      }
      if (run.sustained >= 30 && run.warning >= 45) run.opened=true;
      run.usSpent += actualUSWeekly/7;
      run.defenderSpent += weekly.defender/7;
      if (run.day%7 === 0) run.history.push([run.day,Math.max(...run.levels)]);
    }
    run.history = run.history.slice(-54);
    return run;
  }
  return {initial,restore,inspect,advance};
})();
if (typeof module !== 'undefined' && module.exports) module.exports=KSContestModel;
