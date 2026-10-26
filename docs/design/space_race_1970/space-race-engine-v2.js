// IMPERIA CW — Cold War: standalone Space Race planning prototype, version 2.
// Illustrative simulation only; this module does not change Hearts of Iron IV runtime data.
(function (root) {
  'use strict';

  const EPS = 1e-8;
  const POLICIES = Object.freeze({
    standard: { name: 'Standard Programme', time: 1, cost: 1, launch: 0, objective: 0 },
    assurance: { name: 'Extended Assurance', time: 1.18, cost: 1.18, launch: 0.025, objective: 0.04 },
    accelerated: { name: 'Accelerated Schedule', time: 0.85, cost: 1.25, launch: -0.045, objective: -0.035 },
    reduced: { name: 'Reduced Expenditure', time: 1.35, cost: 0.8, launch: -0.025, objective: -0.02 }
  });
  const copy = value => JSON.parse(JSON.stringify(value));
  const num = (value, fallback) => Number.isFinite(Number(value)) ? Number(value) : fallback;
  const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
  const round = value => Math.round(value * 1000000) / 1000000;
  const FACTOR_LABELS = Object.freeze({
    'qualification-policy': 'Funded qualification policy', 'qualified-support': 'Qualified supporting programmes',
    'flight-experience': 'Relevant flight experience', 'funding-continuity': 'Interrupted programme funding',
    'corrective-engineering': 'Completed corrective engineering', 'support-maintenance': 'Support infrastructure arrears',
    'research-assurance': 'Validated research and analysis',
    'space-leadership': 'Leading Space Power'
  });
  const FACTOR_IDS = Object.keys(FACTOR_LABELS);
  const SAVE_FIELDS = Object.freeze({ status: 's', policy: 'p', work: 'w', calendarMonths: 'c', spentB: 'b',
    launchAdjustment: 'l', objectiveAdjustment: 'o', deployed: 'd', maintenanceArrearsB: 'a', flight: 'f',
    investigationRemainingMonths: 'im', investigationRemainingCostB: 'ic', investigationSpentB: 'is',
    missionSpentB: 'ms', launchCount: 'lc', missionCount: 'mc', successfulMissions: 'sm',
    firstAwardGranted: 'fa', partialAwardGranted: 'pa', repeatAwardGranted: 'ra',
    fundingDisruptionMonths: 'fd', completedInvestigations: 'ci', crewFatalities: 'cf' });
  // IMPERIA CW — Cold War: national programme decisions and transitions generate reward-free news.
  const programmeBulletins = {
    programme_authorised: ['Authorises a Space Programme', 'has authorised development of the programme. Engineering teams will begin funded design, construction and qualification work.'],
    programme_resumed: ['Resumes Space Programme Development', 'has resumed development of the programme. Previously accepted work is retained and further progress requires sustained funding.'],
    programme_paused: ['Suspends Space Programme Development', 'has suspended development of the programme. Existing engineering work is retained while its development allocation is released.'],
    programme_cancelled: ['Cancels a Space Programme', 'has cancelled the programme. Previous spending remains committed and a later restart must repeat part of the validated engineering work.'],
    hardware_ready: ['Qualifies New Space Mission Hardware', 'has completed the funded development and qualification programme. A separately authorised mission or facility acceptance is still required before operational capability is established.'],
    launch_success: ['Launches a New Space Mission', 'has successfully launched the mission. Flight operations are under way; the final scientific and operational result will be assessed after the mission campaign.'],
    commissioning_started: ['Begins Space Facility Acceptance', 'has begun acceptance trials for the new facility. Operational approval depends on the completed technical review.'],
    investigation_completed: ['Completes a Spaceflight Investigation', 'has completed the funded investigation and corrective engineering programme. The space authority may now consider the next operating or flight decision.']
  };

  function create(catalogue, profile, saved, worldContext) {
    // IMPERIA CW — Cold War: controller eligibility comes from the current host profile, never a saved plan.
    if (profile.isAI === true || profile.playerControlled === false) {
      throw new Error('The Space Race is available only to player-controlled countries.');
    }
    const list = Array.isArray(catalogue) ? catalogue : (catalogue.programmes || []);
    const definitions = new Map(list.map(item => [item.id, copy(item)]));
    if (definitions.size !== list.length) throw new Error('Programme IDs must be unique.');
    const initialYear = num(profile.year, 1970);
    const developmentScale = Math.max(0.001, num(catalogue.pacing?.developmentScale, 1));
    const arrivalRandom = new Map();
    // IMPERIA CW — Cold War: the prototype host owns this ledger; it is not a network service.
    const milestones = Array.isArray(catalogue.milestones) ? copy(catalogue.milestones) : [];
    const world = worldContext || { schema: 1, firsts: {}, news: [] };
    if (!world.firsts || typeof world.firsts !== 'object') world.firsts = {};
    if (!Array.isArray(world.news)) world.news = [];
    // IMPERIA CW — Cold War: the shared player roster owns campaign prestige standings.
    if (!world.standings || typeof world.standings !== 'object') world.standings = {};
    for (const [id, receipt] of Object.entries(world.firsts)) if (Array.isArray(receipt)) world.firsts[id] = {
      country: receipt[0], date: receipt[1], programmeId: receipt[2] || null, historical: receipt[3] === true
    };
    world.news = world.news.map(entry => Array.isArray(entry) ? expandEvent(entry) : normaliseEvent(entry));
    for (const first of catalogue.historicalFirsts || []) {
      if (!world.firsts[first.milestoneId]) world.firsts[first.milestoneId] = {
        country: first.country, date: first.date, historical: true
      };
    }
    let data = {
      schema: 2, developmentScale, profileId: profile.id, playerControlled: true,
      baseYear: initialYear, elapsedMonths: 0,
      reserveB: Math.max(0, num(profile.reserveB, 0)),
      annualBudgetB: Math.max(0, num(profile.annualBudgetB, 0)),
      annualGrantB: Math.max(0, num(profile.annualGrantB, profile.annualBudgetB || 0)),
      capabilities: [...new Set(profile.capabilities || [])], selectedId: list[0]?.id || null,
      prestige: 0, researchPoints: 0, politicalCapital: 0, crewFatalities: 0,
      maxActive: 3, newsSequence: 0, log: [], history: [], events: [], programmes: {}
    };
    for (const definition of list) {
      const progress = clamp(num(definition.initialProgress?.[profile.id], 0) / 100, 0, 1);
      const historicCompletion = (profile.initialCompleted || []).includes(definition.id);
      const work = historicCompletion ? 1 : progress;
      const duration = Math.max(1, num(definition.durationMonths, 12));
      const cost = Math.max(0.001, num(definition.totalCostB, 1));
      data.programmes[definition.id] = {
        id: definition.id, status: historicCompletion ? 'operational' : work >= 1 ? 'ready' : 'planned',
        policy: 'standard', work, calendarMonths: work * duration, spentB: work * cost,
        launchAdjustment: 0, objectiveAdjustment: 0, deployed: historicCompletion,
        maintenanceArrearsB: 0, flight: null, investigationRemainingMonths: 0,
        investigationRemainingCostB: 0, investigationSpentB: 0, missionSpentB: 0,
        launchCount: 0, missionCount: 0, successfulMissions: historicCompletion ? 1 : 0,
        firstAwardGranted: historicCompletion, partialAwardGranted: 0, repeatAwardGranted: 0,
        fundingDisruptionMonths: 0, completedInvestigations: 0, crewFatalities: 0,
        lastOutcome: null
      };
      if (historicCompletion) grant(definition);
    }
    const defaults = copy(data);
    if (saved) {
      let candidate = typeof saved === 'string' ? JSON.parse(saved) : copy(saved);
      if (candidate.schema !== 2 || candidate.profileId !== profile.id) {
        throw new Error('This snapshot belongs to another profile or engine version.');
      }
      if (candidate.world) restoreWorld(candidate.world);
      // IMPERIA CW — Cold War: retain progress when a campaign development calendar changes.
      const calendarRatio = developmentScale / Math.max(0.001, num(candidate.developmentScale, 1));
      if (candidate.compact) {
        const expanded = copy(defaults);
        for (const key of ['baseYear', 'elapsedMonths', 'reserveB', 'annualBudgetB', 'annualGrantB', 'selectedId', 'prestige', 'capabilities', 'researchPoints', 'politicalCapital', 'crewFatalities', 'newsSequence']) {
          if (candidate[key] !== undefined) expanded[key] = candidate[key];
        }
        for (const [id, values] of Object.entries(candidate.programmes || {})) {
          if (!expanded.programmes[id]) throw new Error('This snapshot does not match the programme catalogue.');
          let packedCursor = 1;
          for (const [index, [field, key]] of Object.entries(SAVE_FIELDS).entries()) {
            const present = Array.isArray(values) ? Math.floor(values[0] / 2 ** index) % 2 === 1 : values[key] !== undefined;
            if (present) {
              const value = Array.isArray(values) ? values[packedCursor++] : values[key];
              expanded.programmes[id][field] = field === 'calendarMonths' ? value * calendarRatio
                : field === 'flight' && Array.isArray(value) ? expandFlight(value, definitions.get(id)) : value;
            }
          }
        }
        expanded.history = (candidate.history || []).map(entry => ({
          programmeId: entry[0], programmeName: definitions.get(entry[0])?.name || entry[0], type: entry[1], country: profile.id,
          month: entry[2], prestige: entry[3], details: entry[4], crewFatalities: entry[5] || 0,
          rewardEffects: entry[6] || {}, firstMilestone: entry[7] || null, phase: entry[8] || 'objective',
          eventId: entry[9], nationalCrewFatalities: entry[10] ?? entry[5] ?? 0,
          majorNationalAchievement: entry[11] === true,
          countryName: countryNameFor(profile.id, entry[12]), sequence: entry[13] || 0,
          date: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][Math.floor(entry[2]) % 12]
            + ' ' + (expanded.baseYear + Math.floor(entry[2] / 12))
        }));
        for (const outcome of expanded.history) {
          const programme = expanded.programmes[outcome.programmeId];
          if (programme && !programme.lastOutcome) programme.lastOutcome = outcome;
        }
        expanded.events = [...expanded.history.map(eventForOutcome), ...(candidate.bulletins || []).map(expandEvent)]
          .sort(compareEvents).slice(0, 32);
        candidate = expanded;
      } else if (Math.abs(calendarRatio - 1) > EPS) {
        for (const programme of Object.values(candidate.programmes || {})) {
          programme.calendarMonths *= calendarRatio;
        }
      }
      candidate.developmentScale = developmentScale;
      if (!candidate.programmes || Object.keys(candidate.programmes).some(id => !definitions.has(id))) {
        throw new Error('This snapshot does not match the programme catalogue.');
      }
      // IMPERIA CW — Cold War: additive catalogue updates retain saved work and current historical baselines.
      candidate.capabilities = [...new Set([...defaults.capabilities, ...(candidate.capabilities || [])])];
      data = candidate;
      for (const key of ['researchPoints', 'crewFatalities']) data[key] = Math.max(0, num(data[key], 0));
      data.politicalCapital = num(data.politicalCapital, 0);
      data.newsSequence = Math.max(0, num(data.newsSequence, 0));
      if (!Array.isArray(data.events)) data.events = (data.history || []).map(eventForOutcome);
      else data.events = data.events.map(normaliseEvent);
      for (const item of list) if (!data.programmes[item.id]) {
        data.programmes[item.id] = copy(defaults.programmes[item.id]);
      }
      for (const programme of Object.values(data.programmes)) {
        for (const field of ['fundingDisruptionMonths', 'completedInvestigations', 'crewFatalities']) programme[field] = Math.max(0, num(programme[field], 0));
      }
    }
    data.playerControlled = true;
    syncStanding();

    function syncStanding() {
      world.standings[profile.id] = { countryName: profile.name || profile.id,
        prestige: Math.max(0, num(data.prestige, 0)), playerControlled: data.playerControlled === true };
    }
    function standings() {
      const rows = Object.entries(world.standings).map(([country, entry]) => ({ country,
        countryName: Array.isArray(entry) ? countryNameFor(country, entry[2]) : countryNameFor(country, entry.countryName),
        prestige: Math.max(0, num(Array.isArray(entry) ? entry[0] : entry.prestige, 0)),
        playerControlled: Array.isArray(entry) ? entry[1] === true : entry.playerControlled === true && entry.isAI !== true }))
        .filter(entry => entry.playerControlled && entry.prestige > EPS)
        .sort((a, b) => b.prestige - a.prestige || a.country.localeCompare(b.country));
      return rows.map(entry => ({ ...entry, rank: 1 + rows.filter(other => other.prestige > entry.prestige + EPS).length }));
    }
    function leadership() {
      const ranked = standings(), first = ranked[0];
      const tied = first && ranked.filter(entry => Math.abs(entry.prestige - first.prestige) <= EPS).length > 1;
      const leader = first && !tied ? first : null;
      const active = data.playerControlled && leader?.country === profile.id;
      return { leader: leader ? copy(leader) : null, tied: Boolean(tied), active: Boolean(active),
        objectiveBonus: active ? 0.02 : 0, operatingCostMultiplier: active ? 0.95 : 1 };
    }

    function grant(definition) {
      for (const capability of definition.grants || []) {
        if (!data.capabilities.includes(capability)) data.capabilities.push(capability);
      }
    }
    function now() { return data.baseYear + data.elapsedMonths / 12; }
    function dateLabel() {
      const monthNumber = Math.floor(data.elapsedMonths + EPS);
      return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][monthNumber % 12]
        + ' ' + (data.baseYear + Math.floor(monthNumber / 12));
    }
    function log(message, type = 'info', id = null) {
      data.log.unshift({ date: dateLabel(), month: round(data.elapsedMonths), message, type, id });
      data.log = data.log.slice(0, 120);
    }
    function result(ok, message, extra) { return { ok, message, ...(extra || {}) }; }
    // IMPERIA CW — Cold War: compact host-owned worldwide firsts and national mission bulletins.
    function countryNameFor(country, suppliedName) {
      if (typeof suppliedName === 'string' && suppliedName.trim()) return suppliedName;
      if (country === profile.id && typeof profile.name === 'string' && profile.name.trim()) return profile.name;
      const countries = Array.isArray(catalogue.profiles) ? catalogue.profiles : Object.values(catalogue.profiles || {});
      return countries.find(item => item.id === country)?.name || country;
    }
    function compareEvents(a, b) {
      return num(b.month, 0) - num(a.month, 0) || num(b.sequence, 0) - num(a.sequence, 0);
    }
    function eventForProgramme(record) {
      const definition = definitions.get(record.programmeId) || {};
      const country = record.country || profile.id;
      const countryName = countryNameFor(country, record.countryName);
      const wording = programmeBulletins[record.type] || ['Reports Space Programme Progress', 'has issued a national space programme report.'];
      const programmeName = definition.name || record.programmeName || record.programmeId;
      return {
        id: record.eventId || record.id, country, countryName, kind: 'programme',
        programmeId: record.programmeId, type: record.type,
        title: countryName + ': ' + wording[0] + ' — ' + programmeName,
        description: countryName + ' ' + wording[1] + ' Programme: ' + programmeName + '.',
        date: record.date, month: record.month, sequence: record.sequence || 0,
        scope: 'national', crewFatalities: 0, nationalCrewFatalities: 0, rewardEffects: {},
        firstMilestone: null, majorNationalAchievement: false,
        imageKey: record.type === 'investigation_completed' ? 'mission-control' : definition.imageKey || 'mission-control'
      };
    }
    function programmeNews(definition, type) {
      data.newsSequence += 1;
      const event = eventForProgramme({ programmeId: definition.id, type, country: profile.id,
        countryName: countryNameFor(profile.id), date: dateLabel(), month: round(data.elapsedMonths),
        sequence: data.newsSequence, eventId: profile.id + ':programme:' + data.newsSequence });
      data.events.unshift(event);
      data.events = data.events.slice(0, 32);
      return event;
    }
    function normaliseEvent(event) {
      if (event.kind && event.countryName) return copy(event);
      if (event.kind === 'programme' || programmeBulletins[event.type]) return eventForProgramme({ ...event, eventId: event.id });
      return eventForOutcome({ ...event, eventId: event.id, details: event.details || event.description,
        prestige: event.rewardEffects?.prestige || 0 });
    }
    function eventForOutcome(outcome) {
      const definition = definitions.get(outcome.programmeId) || {};
      const milestone = milestones.find(item => item.id === outcome.firstMilestone);
      const country = outcome.country || profile.id;
      const countryName = countryNameFor(country, outcome.countryName);
      const typeTitle = outcome.crewFatalities > 0 ? 'Crew Lost in Spaceflight Accident'
        : outcome.type === 'full_success' ? 'Mission Objectives Achieved'
        : outcome.type === 'partial_success' ? 'Partial Mission Results Returned'
        : outcome.type === 'catastrophic_failure' ? 'Major Spaceflight Accident'
        : outcome.type === 'launch_failure' ? 'Launch Failure' : 'Mission Objectives Not Achieved';
      const majorNationalTitle = definition.majorNationalCapability === 'lunar-landing' ? 'First National Crewed Lunar Landing'
        : definition.majorNationalCapability === 'crewed-mars-return' ? 'First National Crewed Mars Expedition Completed'
        : 'Major National Spaceflight Achievement';
      return {
        id: outcome.eventId || country + ':' + outcome.programmeId + ':' + outcome.month + ':' + outcome.type,
        country, countryName, kind: 'mission', programmeId: outcome.programmeId, type: outcome.type,
        title: countryName + ': ' + (milestone ? milestone.title : outcome.majorNationalAchievement ? majorNationalTitle
          : (definition.name || outcome.programmeName || outcome.programmeId) + ' — ' + typeTitle),
        details: outcome.details || milestone?.summary || '',
        description: countryName + ' reports on ' + (definition.name || outcome.programmeName || outcome.programmeId)
          + '. ' + (outcome.details || milestone?.summary || ''), date: outcome.date,
        month: outcome.month, sequence: outcome.sequence || 0,
        scope: milestone || outcome.crewFatalities > 0 || outcome.majorNationalAchievement ? 'world' : 'national',
        crewFatalities: outcome.crewFatalities || 0,
        nationalCrewFatalities: outcome.nationalCrewFatalities ?? outcome.crewFatalities ?? 0,
        rewardEffects: { prestige: outcome.prestige || 0, ...(outcome.rewardEffects || {}) },
        firstMilestone: outcome.firstMilestone || null,
        majorNationalAchievement: outcome.majorNationalAchievement === true,
        imageKey: outcome.crewFatalities > 0 ? 'mission-control' : milestone?.imageKey || definition.imageKey || 'mission-control'
      };
    }
    function compactEvent(event) {
      const countries = Array.isArray(catalogue.profiles) ? catalogue.profiles : Object.values(catalogue.profiles || {});
      const savedName = countries.some(item => item.id === event.country && item.name === event.countryName) ? null : event.countryName;
      return [event.id, event.country, event.programmeId, event.type, event.date, event.month,
        event.crewFatalities || 0, event.rewardEffects || {}, event.firstMilestone || null,
        event.nationalCrewFatalities ?? event.crewFatalities ?? 0, event.kind === 'programme' || event.firstMilestone ? null : event.details || event.description,
        event.majorNationalAchievement === true, savedName, event.sequence || 0];
    }
    function expandEvent(entry) {
      if (programmeBulletins[entry[3]]) return eventForProgramme({ eventId: entry[0], country: entry[1],
        programmeId: entry[2], type: entry[3], date: entry[4], month: entry[5], countryName: entry[12], sequence: entry[13] });
      const milestone = milestones.find(item => item.id === entry[8]);
      return eventForOutcome({ eventId: entry[0], country: entry[1], programmeId: entry[2], type: entry[3],
        date: entry[4], month: entry[5], crewFatalities: entry[6], rewardEffects: entry[7], firstMilestone: entry[8],
        nationalCrewFatalities: entry[9], details: entry[10] || milestone?.summary || '', prestige: entry[7]?.prestige || 0,
        majorNationalAchievement: entry[11] === true, countryName: entry[12], sequence: entry[13] });
    }
    function restoreWorld(value, replaceStandings = false) {
      if (!value || typeof value !== 'object') return;
      for (const [id, receipt] of Object.entries(value.firsts || {})) {
        if (!world.firsts[id]) world.firsts[id] = Array.isArray(receipt)
          ? { country: receipt[0], date: receipt[1], programmeId: receipt[2] || null, historical: receipt[3] === true }
          : copy(receipt);
      }
      for (const entry of value.news || []) {
        const event = Array.isArray(entry) ? expandEvent(entry) : normaliseEvent(entry);
        if (!world.news.some(item => item.id === event.id)) world.news.push(event);
      }
      world.news.sort(compareEvents);
      world.news = world.news.slice(0, 20);
      for (const [country, entry] of Object.entries(value.standings || {})) {
        if (!replaceStandings && world.standings[country]) continue;
        world.standings[country] = Array.isArray(entry)
          ? { prestige: Math.max(0, num(entry[0], 0)), playerControlled: entry[1] === true, countryName: countryNameFor(country, entry[2]) }
          : copy(entry);
      }
    }
    function exportWorldState() {
      const countries = Array.isArray(catalogue.profiles) ? catalogue.profiles : Object.values(catalogue.profiles || {});
      return { schema: 1, firsts: Object.fromEntries(Object.entries(world.firsts).map(([id, receipt]) =>
        [id, [receipt.country, receipt.date, receipt.programmeId || null, receipt.historical === true]])),
        news: world.news.slice(0, 4).map(compactEvent),
        standings: Object.fromEntries(Object.entries(world.standings).map(([country, entry]) => {
          const name = Array.isArray(entry) ? entry[2] : entry.countryName;
          return [country, [Array.isArray(entry) ? entry[0] : entry.prestige,
            Array.isArray(entry) ? entry[1] === true : entry.playerControlled === true && entry.isAI !== true,
            countries.some(item => item.id === country && item.name === name) ? null : name || null]];
        })) };
    }
    function importWorldState(value) {
      const denied = playerGuard(); if (denied) return denied;
      if (!value || value.schema !== 1) return result(false, 'Unrecognised worldwide mission ledger.');
      restoreWorld(value, true);
      syncStanding();
      return result(true, 'Worldwide mission ledger updated by the host.');
    }
    function playerGuard() {
      return data.playerControlled ? null : result(false, 'The Space Race is available only to player-controlled countries.');
    }
    function setPlayerControlled(value) {
      if (typeof value !== 'boolean') return result(false, 'Controller status must be a boolean supplied by the host.');
      data.playerControlled = value;
      syncStanding();
      return result(true, value ? 'Player control restored; planning actions are available.'
        : 'AI control assigned; Space Race planning and simulation are suspended.');
    }
    function lookup(id) {
      const definition = definitions.get(id);
      const programme = data.programmes[id];
      return definition && programme ? { definition, programme } : null;
    }
    function activeCount() {
      return Object.values(data.programmes).filter(item => item.status === 'active').length;
    }
    function commissioningOnly(definition) {
      return definition.commissioningOnly === true || (definition.commissioningOnly !== false
        && definition.region === 'ground' && definition.pLaunch === 1 && num(definition.missionCostB, 0) === 0);
    }
    function launchWindowWait(definition) {
      if (commissioningOnly(definition)) return 0;
      if (definition.fixedWindowStartMonth !== undefined) {
        const start = Math.max(0, num(definition.fixedWindowStartMonth, 0));
        const end = num(definition.fixedWindowEndMonth, Infinity);
        if (data.elapsedMonths >= end - EPS) return null;
        return Math.max(0, start - data.elapsedMonths);
      }
      const cycle = Math.max(0, num(definition.windowCycleMonths, 0));
      if (!cycle) return 0;
      const offset = num(definition.windowOffsetMonths, 0);
      const width = clamp(num(definition.windowOpenMonths, 2), 0.01, cycle);
      const phase = ((data.elapsedMonths - offset) % cycle + cycle) % cycle;
      return phase < width - EPS ? 0 : Math.max(0, cycle - phase);
    }
    function gates(definition, programme, mode) {
      const reasons = [];
      if (!data.playerControlled) reasons.push('Available only to player-controlled countries');
      if (now() + EPS < num(definition.minYear, initialYear)) reasons.push('Available from ' + definition.minYear);
      for (const id of definition.prerequisites || []) {
        if (!data.programmes[id]?.deployed) reasons.push('Successful predecessor: ' + (definitions.get(id)?.name || id));
      }
      for (const capability of definition.capabilityRequirements || []) {
        if (!data.capabilities.includes(capability)) reasons.push('Required capability: ' + capability.replace(/-/g, ' '));
      }
      if (mode === 'launch') {
        if (programme.work < 1 - EPS) reasons.push('Development and acceptance remain incomplete');
        const minimum = Math.max(1, num(definition.durationMonths, 12)) * 0.85;
        if (programme.calendarMonths + EPS < minimum) reasons.push('Minimum engineering calendar remains incomplete');
        if (programme.flight) reasons.push('A mission is already in flight');
        if (programme.investigationRemainingMonths > EPS || programme.investigationRemainingCostB > EPS) {
          reasons.push('Investigation and corrective work remain incomplete');
        }
        if (programme.maintenanceArrearsB > EPS) reasons.push('Outstanding operating costs');
        const wait = launchWindowWait(definition);
        if (wait === null) reasons.push('The fixed mission opportunity has expired; this encounter cannot be repeated on a recurring planetary window');
        else if (wait > EPS) reasons.push('Next transfer opportunity in ' + round(wait) + ' months');
        if (data.reserveB + EPS < Math.max(0, num(definition.missionCostB, 0))) reasons.push('Insufficient treasury for mission hardware and operations');
      }
      return reasons;
    }
    function odds(definition, programme) {
      if (programme.flight) return {
        pLaunch: programme.flight.pLaunch, pObjective: programme.flight.pObjective,
        pFull: programme.flight.pFull, pCrewLoss: programme.flight.pCrewLoss || 0,
        probabilityFactors: copy(programme.flight.probabilityFactors || [])
      };
      const factors = [];
      function factor(id, label, launchDelta, objectiveDelta, reason) {
        if (Math.abs(launchDelta) > EPS || Math.abs(objectiveDelta) > EPS) factors.push({ id, label, launchDelta: round(launchDelta), objectiveDelta: round(objectiveDelta), reason });
      }
      factor('qualification-policy', 'Funded qualification policy', programme.launchAdjustment, programme.objectiveAdjustment,
        'Only the policy used during completed, paid engineering work contributes.');
      const support = (definition.supportingProgrammes || []).map(id => lookup(typeof id === 'string' ? id : id.id))
        .filter(entry => entry && entry.programme.deployed && entry.programme.maintenanceArrearsB < EPS);
      factor('qualified-support', 'Qualified supporting programmes', Math.min(0.02, support.length * 0.005), Math.min(0.04, support.length * 0.01),
        support.map(entry => entry.definition.name).join('; '));
      const family = definition.missionFamily;
      const relatedSuccesses = family ? list.filter(item => item.id !== definition.id && item.missionFamily === family && !commissioningOnly(item))
        .reduce((sum, item) => sum + Math.min(2, data.programmes[item.id].successfulMissions), 0) : 0;
      factor('flight-experience', 'Relevant flight experience', Math.min(0.025, programme.successfulMissions * 0.0075 + relatedSuccesses * 0.003),
        Math.min(0.04, programme.successfulMissions * 0.01 + relatedSuccesses * 0.005),
        programme.successfulMissions + ' successful missions of this architecture; ' + relatedSuccesses + ' accepted related flights.');
      const disruption = clamp(programme.fundingDisruptionMonths / Math.max(1, num(definition.durationMonths, 12)), 0, 1);
      factor('funding-continuity', 'Interrupted programme funding', -0.02 * disruption, -0.03 * disruption,
        round(programme.fundingDisruptionMonths) + ' equivalent months of unfunded engineering demand. Paid extended qualification can reduce this disruption.');
      factor('corrective-engineering', 'Completed corrective engineering', Math.min(0.012, programme.completedInvestigations * 0.004),
        Math.min(0.018, programme.completedInvestigations * 0.006), 'Credit requires a completed and funded post-flight investigation.');
      const neglectedSupport = (definition.supportingProgrammes || []).map(id => lookup(typeof id === 'string' ? id : id.id))
        .filter(entry => entry && entry.programme.deployed && entry.programme.maintenanceArrearsB > EPS);
      factor('support-maintenance', 'Support infrastructure arrears', -Math.min(0.03, neglectedSupport.length * 0.01),
        -Math.min(0.045, neglectedSupport.length * 0.015), neglectedSupport.map(entry => entry.definition.name).join('; '));
      factor('research-assurance', 'Validated research and analysis', 0, Math.min(0.02, data.researchPoints * 0.0002),
        'Accepted scientific results improve institutional analysis; the total effect is capped at two percentage points.');
      factor('space-leadership', 'Leading Space Power', 0, leadership().objectiveBonus,
        'A unique campaign-prestige lead supports recruitment and mission preparation. This benefit applies to newly authorised missions.');
      const pLaunch = commissioningOnly(definition) ? 1 : clamp(num(definition.pLaunch, 0.85) + factors.reduce((sum, item) => sum + item.launchDelta, 0), 0.02, 0.995);
      const pObjective = clamp(num(definition.pObjective, 0.8) + factors.reduce((sum, item) => sum + item.objectiveDelta, 0), 0.02, 0.995);
      const hasCrew = Math.max(0, Math.floor(num(definition.crewSize, 0))) > 0;
      const pCrewLoss = hasCrew ? (definition.crewAtLaunch === false ? 0 : (1 - pLaunch) * 0.14) + pLaunch * (1 - pObjective) * 0.05 : 0;
      return { pLaunch, pObjective, pFull: pLaunch * pObjective, pCrewLoss, probabilityFactors: factors };
    }
    function compactFlight(flight) {
      if (!flight) return null;
      const factors = (flight.probabilityFactors || []).map(factor => {
        let evidence = null;
        if (['qualified-support', 'support-maintenance'].includes(factor.id)) evidence = factor.reason.split('; ')
          .map(name => list.find(item => item.name === name)?.id || name);
        else if (factor.id === 'flight-experience') evidence = (factor.reason.match(/\d+/g) || []).map(Number);
        else if (factor.id === 'funding-continuity') evidence = parseFloat(factor.reason);
        return [FACTOR_IDS.indexOf(factor.id), factor.launchDelta, factor.objectiveDelta, evidence];
      });
      return [flight.startedAt, flight.arrivesAt, flight.kind === 'commissioning' ? 1 : 0,
        flight.pLaunch, flight.pObjective, factors];
    }
    function expandFlight(entry, definition) {
      const pLaunch = entry[3], pObjective = entry[4];
      const reasons = {
        'qualification-policy': 'Only the policy used during completed, paid engineering work contributes.',
        'corrective-engineering': 'Credit requires a completed and funded post-flight investigation.',
        'research-assurance': 'Accepted scientific results improve institutional analysis; the total effect is capped at two percentage points.',
        'space-leadership': 'A unique campaign-prestige lead supports recruitment and mission preparation. This benefit applies to newly authorised missions.'
      };
      const factors = (entry[5] || []).map(factor => {
        const id = FACTOR_IDS[factor[0]], evidence = factor[3];
        let reason = reasons[id] || '';
        if (['qualified-support', 'support-maintenance'].includes(id)) reason = (evidence || []).map(key => definitions.get(key)?.name || key).join('; ');
        else if (id === 'flight-experience') reason = evidence[0] + ' successful missions of this architecture; ' + evidence[1] + ' accepted related flights.';
        else if (id === 'funding-continuity') reason = evidence + ' equivalent months of unfunded engineering demand. Paid extended qualification can reduce this disruption.';
        return { id, label: FACTOR_LABELS[id], launchDelta: factor[1], objectiveDelta: factor[2], reason };
      });
      const hasCrew = Math.max(0, Math.floor(num(definition.crewSize, 0))) > 0;
      return { startedAt: entry[0], arrivesAt: entry[1], kind: entry[2] ? 'commissioning' : 'flight',
        pLaunch, pObjective, pFull: pLaunch * pObjective,
        pCrewLoss: hasCrew ? (definition.crewAtLaunch === false ? 0 : (1 - pLaunch) * 0.14) + pLaunch * (1 - pObjective) * 0.05 : 0,
        probabilityFactors: factors };
    }
    function state() {
      const leadershipState = leadership();
      const programmes = list.map(definition => {
        const programme = data.programmes[definition.id];
        const policy = POLICIES[programme.policy];
        const remainingWork = Math.max(0, 1 - programme.work);
        const baseCost = Math.max(0.001, num(definition.totalCostB, 1));
        const remainingCostB = remainingWork * baseCost * policy.cost;
        const physicalCalendarRemainingMonths = Math.max(0, Math.max(1, num(definition.durationMonths, 12)) * 0.85 - programme.calendarMonths);
        const engineeringRemainingMonths = Math.max(physicalCalendarRemainingMonths,
          remainingWork * Math.max(1, num(definition.durationMonths, 12)) * policy.time);
        const shares = Math.max(1, activeCount() + (programme.status === 'active' ? 0 : 1));
        const monthlyShare = data.annualBudgetB / 12 / shares;
        const fundingRemainingMonths = remainingCostB > EPS && monthlyShare <= EPS ? null : remainingCostB / Math.max(EPS, monthlyShare);
        const startGates = gates(definition, programme, 'start');
        const launchGates = gates(definition, programme, 'launch');
        const completed = programme.work >= 1 - EPS && programme.calendarMonths + EPS >= Math.max(1, num(definition.durationMonths, 12)) * 0.85;
        return {
          ...copy(definition), ...copy(programme), ...odds(definition, programme),
          progress: clamp(programme.work * 100, 0, 100),
          calendarProgress: clamp(programme.calendarMonths / Math.max(1, num(definition.durationMonths, 12)) * 100, 0, 100),
          paidProgress: programme.work * 100,
          baseCostB: baseCost, totalCostB: programme.spentB + remainingCostB,
          remainingCostB, engineeringRemainingMonths, physicalCalendarRemainingMonths, fundingRemainingMonths,
          remainingMonths: fundingRemainingMonths === null ? null : Math.max(engineeringRemainingMonths, fundingRemainingMonths),
          upkeepB: programme.deployed ? Math.max(0, num(definition.upkeepB, 0)) * leadershipState.operatingCostMultiplier : 0,
          plannedUpkeepB: Math.max(0, num(definition.upkeepB, 0)) * leadershipState.operatingCostMultiplier,
          completed, deployable: completed && launchGates.length === 0,
          startable: !completed && programme.status !== 'active' && startGates.length === 0 && activeCount() < data.maxActive,
          gates: completed ? launchGates : startGates,
          startGates, launchGates,
          flightRemainingMonths: programme.flight ? Math.max(0, programme.flight.arrivesAt - data.elapsedMonths) : 0,
          commissioningOnly: commissioningOnly(definition), launchWindowWaitMonths: launchWindowWait(definition),
          launchWindowExpired: launchWindowWait(definition) === null,
          policyDescription: policy.name,
          policyTimeMultiplier: policy.time, policyCostMultiplier: policy.cost
        };
      });
      return {
        schema: 2, profileId: data.profileId, playersOnly: true,
        playerControlled: data.playerControlled, suspended: !data.playerControlled,
        year: Math.floor(now() + EPS),
        month: Math.floor(data.elapsedMonths + EPS) % 12 + 1, numericYear: now(), dateLabel: dateLabel(),
        elapsedMonths: data.elapsedMonths, reserveB: data.reserveB,
        annualBudgetB: data.annualBudgetB, annualGrantB: data.annualGrantB,
        annualTreasuryTransferB: data.annualGrantB,
        annualOperatingCostB: programmes.reduce((sum, item) => sum + item.upkeepB, 0),
        maintenanceArrearsB: programmes.reduce((sum, item) => sum + item.maintenanceArrearsB, 0),
        prestige: data.prestige, researchPoints: data.researchPoints, politicalCapital: data.politicalCapital,
        crewFatalities: data.crewFatalities, totalCrewFatalities: data.crewFatalities,
        capabilities: [...data.capabilities],
        currentModifiers: [{ id: 'research-assurance', label: 'Validated research and analysis',
          launchDelta: 0, objectiveDelta: Math.min(0.02, data.researchPoints * 0.0002) },
          ...(leadershipState.active ? [{ id: 'space-leadership', label: 'Leading Space Power',
            launchDelta: 0, objectiveDelta: 0.02, operatingCostMultiplier: 0.95 }] : [])],
        prestigeStandings: standings(), topThree: standings().slice(0, 3), leadership: leadershipState,
        activeCount: activeCount(), maxActive: data.maxActive, selectedId: data.selectedId,
        programmes, log: copy(data.log), history: copy(data.history), policies: copy(POLICIES),
        events: copy([...data.events, ...world.news.filter(event => event.country !== data.profileId)]
          .sort(compareEvents).slice(0, 32)),
        worldFirsts: copy(world.firsts)
      };
    }
    function select(id) {
      const denied = playerGuard(); if (denied) return denied;
      if (!lookup(id)) return result(false, 'Unknown programme.');
      data.selectedId = id;
      return result(true, 'Programme selected.');
    }
    function setBudget(value) {
      const denied = playerGuard(); if (denied) return denied;
      const amount = Number(value);
      if (!Number.isFinite(amount) || amount < 0 || amount > 1000000) return result(false, 'Enter a valid non-negative annual budget.');
      data.annualBudgetB = amount;
      log('Annual development ceiling set to $' + amount.toFixed(2) + 'B. Treasury support remains unchanged.');
      return result(true, 'Annual development ceiling updated.');
    }
    function setPolicy(id, policyId) {
      const denied = playerGuard(); if (denied) return denied;
      const entry = lookup(id);
      if (!entry || !POLICIES[policyId]) return result(false, 'Unknown programme or policy.');
      if (entry.programme.work >= 1 - EPS) return result(false, 'The completed engineering record cannot be changed retrospectively.');
      entry.programme.policy = policyId;
      log(entry.definition.name + ': ' + POLICIES[policyId].name + ' applies to future engineering work.', 'policy', id);
      return result(true, 'Policy applies prospectively; completed work and paid expenditure remain recorded.');
    }
    function start(id) {
      const denied = playerGuard(); if (denied) return denied;
      const entry = lookup(id);
      if (!entry) return result(false, 'Unknown programme.');
      const { definition, programme } = entry;
      if (programme.work >= 1 - EPS) return result(false, 'Development is complete; prepare a mission.');
      if (programme.status === 'active') return result(false, 'Programme is already active.');
      const reasons = gates(definition, programme, 'start');
      if (reasons.length) return result(false, reasons.join('; '));
      if (activeCount() >= data.maxActive) return result(false, 'All three engineering programme slots are occupied.');
      const resuming = programme.status === 'paused';
      programme.status = 'active';
      log(definition.name + ': engineering authorised.', 'programme', id);
      programmeNews(definition, resuming ? 'programme_resumed' : 'programme_authorised');
      return result(true, 'Programme active. Progress requires time and actual development allocation.');
    }
    function pause(id) {
      const denied = playerGuard(); if (denied) return denied;
      const entry = lookup(id);
      if (!entry || entry.programme.status !== 'active') return result(false, 'Only an active development programme can be paused.');
      entry.programme.status = 'paused';
      log(entry.definition.name + ': development paused; engineering work and expenditure retained.', 'programme', id);
      programmeNews(entry.definition, 'programme_paused');
      return result(true, 'Development paused; the engineering slot is available.');
    }
    function resume(id) {
      const denied = playerGuard(); if (denied) return denied;
      const entry = lookup(id);
      if (!entry || entry.programme.status !== 'paused') return result(false, 'This programme is not paused.');
      return start(id);
    }
    function cancel(id) {
      const denied = playerGuard(); if (denied) return denied;
      const entry = lookup(id);
      if (!entry) return result(false, 'Unknown programme.');
      const programme = entry.programme;
      if (!['active', 'paused', 'planned'].includes(programme.status) || programme.work >= 1 - EPS) {
        return result(false, 'Only an unfinished development programme can be cancelled.');
      }
      programme.work *= 0.75;
      programme.calendarMonths *= 0.75;
      programme.launchAdjustment *= 0.75;
      programme.objectiveAdjustment *= 0.75;
      programme.status = 'cancelled';
      log(entry.definition.name + ': cancelled; all spending is sunk and 25% of validated work must be repeated after restart.', 'warning', id);
      programmeNews(entry.definition, 'programme_cancelled');
      return result(true, 'Programme cancelled. Expenditure is retained; 25% of validated work is forfeited.');
    }
    function investigate(definition, programme, severity) {
      const months = severity === 'partial_success' ? 3 : severity === 'catastrophic_failure' ? 12 : 6;
      const fraction = severity === 'partial_success' ? 0.08 : severity === 'catastrophic_failure' ? 0.3 : 0.18;
      programme.investigationRemainingMonths = months;
      programme.investigationRemainingCostB = Math.max(0.025, num(definition.missionCostB, 0) * fraction);
      programme.status = 'investigating';
    }
    function recordOutcome(definition, programme, type, details, phase = 'objective') {
      const value = Math.max(0, num(definition.prestige, 0));
      const firstNationalSuccess = type === 'full_success' && !programme.firstAwardGranted;
      // IMPERIA CW — Cold War: a national first remains major news after another nation won the worldwide race.
      const majorNationalAchievement = firstNationalSuccess && typeof definition.majorNationalCapability === 'string'
        && (definition.grants || []).includes(definition.majorNationalCapability)
        && !data.capabilities.includes(definition.majorNationalCapability);
      const rewardEffects = { researchPoints: 0, politicalCapital: 0 };
      let firstMilestone = null;
      let award = 0;
      if (type === 'full_success') {
        programme.deployed = true;
        programme.successfulMissions += 1;
        grant(definition);
        if (!programme.firstAwardGranted) {
          award = Math.max(0, value - programme.partialAwardGranted);
          programme.firstAwardGranted = true;
        } else {
          award = Math.max(0, Math.min(2, value * 0.03, value * 0.15 - programme.repeatAwardGranted));
          programme.repeatAwardGranted += award;
        }
        programme.status = 'operational';
      } else if (type === 'partial_success') {
        if (!programme.firstAwardGranted && programme.partialAwardGranted === 0) {
          award = value * 0.1;
          programme.partialAwardGranted = award;
        }
        investigate(definition, programme, type);
      } else {
        if (type === 'catastrophic_failure') award = -Math.min(data.prestige, Math.max(1, value * 0.08));
        investigate(definition, programme, type);
      }
      if (firstNationalSuccess) {
        rewardEffects.researchPoints += Math.max(0, num(definition.rewardEffects?.researchPoints, 0));
        rewardEffects.politicalCapital += Math.max(0, num(definition.rewardEffects?.politicalCapital, 0));
      }
      if (type === 'full_success') {
        for (const milestone of milestones.filter(item => (definition.grants || []).includes(item.capability))) {
          if (world.firsts[milestone.id]) continue;
          world.firsts[milestone.id] = { country: profile.id, date: dateLabel(), programmeId: definition.id, historical: false };
          firstMilestone = firstMilestone || milestone.id;
          award += Math.max(0, num(milestone.prestige, 0));
          rewardEffects.researchPoints += Math.max(0, num(milestone.researchPoints, 0));
          rewardEffects.politicalCapital += Math.max(0, num(milestone.politicalCapital, 0));
        }
      }
      const crewSize = Math.max(0, Math.floor(num(definition.crewSize, 0)));
      const crewFatalities = type === 'catastrophic_failure' && (phase !== 'launch' || definition.crewAtLaunch !== false) ? crewSize : 0;
      const nationalCrewFatalities = crewFatalities ? Math.min(crewFatalities, Math.max(0, Math.floor(num(definition.nationalCrewSize, crewSize)))) : 0;
      if (crewFatalities) {
        data.crewFatalities += crewFatalities;
        programme.crewFatalities += crewFatalities;
        rewardEffects.politicalCapital -= nationalCrewFatalities * 4;
        details += ' Crew fatalities: ' + crewFatalities + (nationalCrewFatalities !== crewFatalities ? ' (' + nationalCrewFatalities + ' national)' : '') + '.';
      }
      data.researchPoints += rewardEffects.researchPoints;
      data.politicalCapital += rewardEffects.politicalCapital;
      data.prestige = Math.max(0, data.prestige + award);
      syncStanding();
      programme.missionCount += 1;
      data.newsSequence += 1;
      const outcome = {
        programmeId: definition.id, programmeName: definition.name, type,
        date: dateLabel(), month: round(data.elapsedMonths), prestige: round(award), details,
        country: profile.id, countryName: countryNameFor(profile.id), sequence: data.newsSequence,
        eventId: profile.id + ':' + definition.id + ':' + programme.missionCount,
        crewFatalities, nationalCrewFatalities, rewardEffects, firstMilestone, phase, majorNationalAchievement
      };
      programme.lastOutcome = outcome;
      data.history.unshift(outcome);
      data.history = data.history.slice(0, 80);
      const event = eventForOutcome(outcome);
      data.events.unshift(event);
      data.events = data.events.slice(0, 32);
      if (firstMilestone || crewFatalities || majorNationalAchievement) {
        world.news.unshift(copy(event));
        world.news = world.news.slice(0, 20);
      }
      log(definition.name + ': ' + details + (award ? ' Prestige ' + (award > 0 ? '+' : '') + round(award) + '.' : ''),
        type === 'full_success' ? 'success' : 'warning', definition.id);
      return outcome;
    }
    function randomValue(rng) {
      const value = Number(rng());
      if (!Number.isFinite(value) || value < 0 || value >= 1) throw new Error('Random generator must return a number in [0, 1).');
      return value;
    }
    function launch(id, rng = Math.random) {
      const denied = playerGuard(); if (denied) return denied;
      const entry = lookup(id);
      if (!entry) return result(false, 'Unknown programme.');
      const { definition, programme } = entry;
      const reasons = gates(definition, programme, 'launch');
      if (reasons.length) return result(false, reasons.join('; '));
      const probabilities = odds(definition, programme);
      // One launcher roll. Arrival resolves a separate post-insertion objective, never a second launcher roll.
      const groundAcceptance = commissioningOnly(definition);
      const draw = groundAcceptance ? 0 : randomValue(rng);
      const cost = Math.max(0, num(definition.missionCostB, 0));
      data.reserveB = Math.max(0, data.reserveB - cost);
      programme.missionSpentB += cost;
      programme.launchCount += 1;
      if (draw >= probabilities.pLaunch) {
        const severity = (draw - probabilities.pLaunch) / (1 - probabilities.pLaunch);
        const type = severity >= 0.86 ? 'catastrophic_failure' : 'launch_failure';
        const outcome = recordOutcome(definition, programme, type,
          type === 'catastrophic_failure' ? 'Severe launch accident; investigation and corrective work required.' : 'Launch failed; mission hardware lost and flight operations suspended.', 'launch');
        return result(true, outcome.details, { outcome });
      }
      const flightMonths = groundAcceptance ? Math.max(0, num(definition.flightMonths, 0)) : Math.max(0.01, num(definition.flightMonths, 1));
      programme.flight = { startedAt: data.elapsedMonths, arrivesAt: data.elapsedMonths + flightMonths,
        kind: groundAcceptance ? 'commissioning' : 'flight', ...probabilities };
      programme.status = 'inflight';
      arrivalRandom.set(id, rng);
      if (groundAcceptance) {
        log(definition.name + ': ground acceptance authorised. Facility commissioning requires no rocket launch.', 'commissioning', id);
        if (flightMonths <= EPS) {
          resolveArrival(definition, programme);
          return result(true, programme.lastOutcome.details, { outcome: programme.lastOutcome });
        }
        programmeNews(definition, 'commissioning_started');
        return result(true, 'Ground acceptance started; commissioning review is pending.');
      }
      log(definition.name + ': successful launch. Mission outcome pending; ' + flightMonths + ' months of flight and commissioning remain.', 'launch', id);
      programmeNews(definition, 'launch_success');
      return result(true, 'Launch succeeded. Mission objectives will be assessed after flight and commissioning.');
    }
    function resolveArrival(definition, programme) {
      const flight = programme.flight;
      if (!flight || flight.arrivesAt > data.elapsedMonths + EPS) return;
      const rng = arrivalRandom.get(definition.id) || Math.random;
      arrivalRandom.delete(definition.id);
      programme.flight = null;
      const required = gates(definition, programme, 'start');
      if (required.length) {
        recordOutcome(definition, programme, 'objective_failure', 'Mission acceptance withheld: ' + required.join('; '));
        return;
      }
      // IMPERIA CW — Cold War: arrival reports distinguish brief contact, sustained operations and return.
      // A report changes no probability, capability receipt, investigation or launcher outcome.
      const arrivalDetails = (type, fallback) => {
        const detail = definition.outcomeDetails && definition.outcomeDetails[type];
        return typeof detail === 'string' && detail.trim() ? detail : fallback;
      };
      const draw = randomValue(rng);
      if (draw < flight.pObjective) {
        recordOutcome(definition, programme, 'full_success', arrivalDetails('full_success', flight.kind === 'commissioning'
          ? 'Ground acceptance verified; facility commissioned and operational capability accepted.'
          : 'Mission objective verified; operational capability accepted.'));
      } else {
        const degree = (draw - flight.pObjective) / (1 - flight.pObjective);
        if (degree < 0.6) recordOutcome(definition, programme, 'partial_success', arrivalDetails('partial_success', flight.kind === 'commissioning'
          ? 'Restricted ground acceptance; further corrective engineering is required before commissioning.'
          : 'Partial scientific or operational result; the principal objective remains unqualified.'));
        else if (degree < 0.95) recordOutcome(definition, programme, 'objective_failure', arrivalDetails('objective_failure', flight.kind === 'commissioning'
          ? 'Ground acceptance failed; corrective engineering required before another commissioning review.'
          : 'Post-insertion mission failed; corrective engineering required before another attempt.'));
        else recordOutcome(definition, programme, 'catastrophic_failure', arrivalDetails('catastrophic_failure', flight.kind === 'commissioning'
          ? 'Severe qualification deficiency; extended facility safety review required.'
          : 'Severe post-insertion failure; extended safety investigation required.'));
      }
    }
    function allocate(candidates, available) {
      let pending = candidates.map(item => ({ ...item, allocation: 0 }));
      let remaining = Math.max(0, available);
      for (let pass = 0; pass < candidates.length + 1 && remaining > EPS; pass += 1) {
        const open = pending.filter(item => item.demand - item.allocation > EPS);
        if (!open.length) break;
        const share = remaining / open.length;
        let used = 0;
        for (const item of open) {
          const amount = Math.min(share, item.demand - item.allocation);
          item.allocation += amount;
          used += amount;
        }
        remaining -= used;
      }
      return pending;
    }
    function advance(months) {
      const denied = playerGuard(); if (denied) return denied;
      const amount = Number(months);
      if (!Number.isFinite(amount) || amount <= 0 || amount > 1200) return result(false, 'Advance between a fraction of a month and 1,200 months.');
      const oldLogMonth = data.elapsedMonths;
      let remaining = amount;
      while (remaining > EPS) {
        const nextArrival = Object.values(data.programmes)
          .filter(item => item.flight && item.flight.arrivesAt > data.elapsedMonths + EPS)
          .reduce((nearest, item) => Math.min(nearest, item.flight.arrivesAt - data.elapsedMonths), Infinity);
        const dt = Math.min(1, remaining, nextArrival);
        data.reserveB += data.annualGrantB * dt / 12;
        const operating = list.filter(item => data.programmes[item.id].deployed);
        const operatingCostMultiplier = leadership().operatingCostMultiplier;
        const upkeepDue = operating.reduce((sum, item) => sum + Math.max(0, num(item.upkeepB, 0)) * operatingCostMultiplier * dt / 12 + data.programmes[item.id].maintenanceArrearsB, 0);
        const paidRatio = upkeepDue > EPS ? Math.min(1, data.reserveB / upkeepDue) : 1;
        for (const item of operating) {
          const programme = data.programmes[item.id];
          const due = Math.max(0, num(item.upkeepB, 0)) * operatingCostMultiplier * dt / 12 + programme.maintenanceArrearsB;
          const paid = due * paidRatio;
          programme.maintenanceArrearsB = Math.max(0, due - paid);
          data.reserveB -= paid;
        }
        data.reserveB = Math.max(0, data.reserveB);
        const candidates = [];
        for (const definition of list) {
          const programme = data.programmes[definition.id];
          if (programme.investigationRemainingMonths > EPS) {
            const rate = programme.investigationRemainingCostB / programme.investigationRemainingMonths;
            candidates.push({ id: definition.id, kind: 'investigation', rate,
              demand: Math.min(dt, programme.investigationRemainingMonths) * rate });
          }
          if (programme.status !== 'active') continue;
          if (gates(definition, programme, 'start').length) continue;
          const policy = POLICIES[programme.policy];
          const duration = Math.max(1, num(definition.durationMonths, 12));
          const costPerWork = Math.max(0.001, num(definition.totalCostB, 1)) * policy.cost;
          const workLimit = Math.min(1 - programme.work, dt / (duration * policy.time));
          if (workLimit > EPS) candidates.push({ id: definition.id, kind: 'development', costPerWork,
            duration, policy, demand: workLimit * costPerWork });
        }
        const budget = Math.min(data.reserveB, data.annualBudgetB * dt / 12);
        data.elapsedMonths += dt;
        for (const allocation of allocate(candidates, budget)) {
          const programme = data.programmes[allocation.id];
          if (allocation.kind === 'development' && allocation.demand > EPS) {
            const fundedShare = clamp(allocation.allocation / allocation.demand, 0, 1);
            programme.fundingDisruptionMonths += dt * (1 - fundedShare);
          }
          if (allocation.allocation <= EPS) continue;
          data.reserveB = Math.max(0, data.reserveB - allocation.allocation);
          if (allocation.kind === 'investigation') {
            const calendar = allocation.allocation / allocation.rate;
            programme.investigationRemainingMonths = Math.max(0, programme.investigationRemainingMonths - calendar);
            programme.investigationRemainingCostB = Math.max(0, programme.investigationRemainingCostB - allocation.allocation);
            programme.investigationSpentB += allocation.allocation;
            if (programme.investigationRemainingMonths < EPS && programme.investigationRemainingCostB < EPS) {
              programme.status = programme.deployed ? 'operational' : 'ready';
              programme.completedInvestigations += 1;
              log(definitions.get(allocation.id).name + ': investigation closed; corrective work funded and complete.', 'programme', allocation.id);
              programmeNews(definitions.get(allocation.id), 'investigation_completed');
            }
          } else {
            const work = allocation.allocation / allocation.costPerWork;
            programme.work = Math.min(1, programme.work + work);
            programme.calendarMonths += work * allocation.duration * allocation.policy.time;
            programme.spentB += allocation.allocation;
            programme.launchAdjustment += work * allocation.policy.launch;
            programme.objectiveAdjustment += work * allocation.policy.objective;
            if (programme.policy === 'assurance') programme.fundingDisruptionMonths = Math.max(0,
              programme.fundingDisruptionMonths - work * allocation.duration * 2);
            if (programme.work >= 1 - EPS && programme.calendarMonths + EPS >= allocation.duration * 0.85) {
              programme.work = 1;
              programme.status = 'ready';
              log(definitions.get(allocation.id).name + ': development and acceptance complete. A funded mission is still required to establish the capability.', 'programme', allocation.id);
              programmeNews(definitions.get(allocation.id), 'hardware_ready');
            }
          }
        }
        for (const definition of list) resolveArrival(definition, data.programmes[definition.id]);
        remaining -= dt;
      }
      log('Planning clock advanced ' + round(data.elapsedMonths - oldLogMonth) + ' months. Treasury support, operating costs and funded engineering were accounted for.', 'calendar');
      return result(true, 'Advanced ' + round(amount) + ' months.');
    }
    function serialize() { return { ...copy(data), world: exportWorldState() }; }
    function exportState() {
      // Compact persistence retains receipts, costs and resources; old narrative logs are deliberately omitted.
      const savedState = { schema: 2, compact: true, packed: true, developmentScale: data.developmentScale, profileId: data.profileId,
        baseYear: data.baseYear, elapsedMonths: data.elapsedMonths, reserveB: data.reserveB,
        annualBudgetB: data.annualBudgetB, annualGrantB: data.annualGrantB, selectedId: data.selectedId,
        prestige: data.prestige, researchPoints: data.researchPoints, politicalCapital: data.politicalCapital,
        crewFatalities: data.crewFatalities, newsSequence: data.newsSequence, capabilities: [...data.capabilities], programmes: {},
        world: exportWorldState(),
        bulletins: data.events.filter(event => event.kind === 'programme').slice(0, 4).map(compactEvent),
        history: data.history.slice(0, 4).map(entry => [entry.programmeId, entry.type, entry.month, entry.prestige, entry.details,
          entry.crewFatalities || 0, entry.rewardEffects || {}, entry.firstMilestone || null, entry.phase || 'objective',
          entry.eventId, entry.nationalCrewFatalities ?? entry.crewFatalities ?? 0, entry.majorNationalAchievement === true,
          profile.id === 'CUSTOM' ? entry.countryName : null, entry.sequence || 0]) };
      for (const [id, programme] of Object.entries(data.programmes)) {
        let mask = 0;
        const values = [];
        for (const [index, [field]] of Object.entries(SAVE_FIELDS).entries()) {
          if (JSON.stringify(programme[field]) !== JSON.stringify(defaults.programmes[id][field])) {
            mask += 2 ** index;
            values.push(field === 'flight' ? compactFlight(programme[field]) : programme[field]);
          }
        }
        if (mask) savedState.programmes[id] = [mask, ...values];
      }
      return savedState;
    }
    return Object.freeze({ state, select, setBudget, setPolicy, start, pause, resume, cancel, advance, launch,
      setPlayerControlled, exportWorldState, importWorldState,
      serialize, export: exportState, exportState });
  }

  root.SpaceRaceEngine = Object.freeze({ create, policies: POLICIES, schema: 2 });
})(globalThis);
