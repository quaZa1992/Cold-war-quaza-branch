// IMPERIA CW — Cold War: meaningful invariants for the standalone Space Race prototype.
// Run: node docs/design/space_race_1970/qa_engine_v2.mjs
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';

const folder = new URL('.', import.meta.url);
for (const name of ['space-race-engine-v2.js', 'space-race-catalogue-v2.js']) {
  const bytes = fs.readFileSync(new URL(name, folder));
  assert(!(bytes[0] === 239 && bytes[1] === 187 && bytes[2] === 191), name + ' must not have a BOM');
  vm.runInThisContext(bytes.toString('utf8'), { filename: fileURLToPath(new URL(name, folder)) });
}
const Engine = globalThis.SpaceRaceEngine;
const Catalogue = globalThis.SpaceRaceCatalogue;
const profile = { id: 'SOV', year: 1970, capabilities: [], annualBudgetB: 10000,
  reserveB: 10000, annualGrantB: 10000, initialCompleted: [] };
const base = { region: 'leo', kind: 'plausible', minYear: 1970, durationMonths: 120,
  totalCostB: 120, upkeepB: 1, prerequisites: [], capabilityRequirements: [], grants: [],
  flightMonths: 6, missionCostB: 2, pLaunch: 0.9, pObjective: 0.8, prestige: 100,
  initialProgress: {}, owners: ['OTHER'] };
const catalogue = [0, 1, 2, 3].map(index => ({ ...base, id: 'p' + index, name: 'P' + index, grants: ['c' + index] }));
catalogue.push({ ...base, id: 'dependent', name: 'Dependency', prerequisites: ['p0'], capabilityRequirements: ['c0'] });
catalogue.push({ ...base, id: 'future', name: 'Future', minYear: 1980 });
const row = (engine, id) => engine.state().programmes.find(item => item.id === id);

// IMPERIA CW — Cold War: only a current human controller may operate this preview simulation.
assert.throws(() => Engine.create(catalogue, { ...profile, isAI: true }), /player-controlled/);
assert.throws(() => Engine.create(catalogue, { ...profile, playerControlled: false }), /player-controlled/);
assert.throws(() => Engine.create(catalogue, { ...profile, isAI: true, playerControlled: true }), /player-controlled/);
const controlled = Engine.create(catalogue, { ...profile, playerControlled: true, initialCompleted: ['p1'] });
controlled.start('p0');
controlled.start('p2');
controlled.pause('p2');
let suspendedRolls = 0;
controlled.launch('p1', () => { suspendedRolls += 1; return 0; });
assert.equal(suspendedRolls, 1);
assert(controlled.setPlayerControlled(false).ok);
assert(controlled.state().playersOnly);
assert(controlled.state().suspended);
const frozen = controlled.serialize();
for (const action of [
  () => controlled.select('p3'),
  () => controlled.setBudget(999),
  () => controlled.setPolicy('p0', 'accelerated'),
  () => controlled.start('p3'),
  () => controlled.pause('p0'),
  () => controlled.resume('p2'),
  () => controlled.cancel('p0'),
  () => controlled.advance(12),
  () => controlled.launch('p1', () => { suspendedRolls += 1; return 0; })
]) {
  const result = action();
  assert.equal(result.ok, false);
  assert.match(result.message, /player-controlled/);
  assert.deepEqual(controlled.serialize(), frozen, 'AI-blocked actions must not spend, accrue income, advance flights, progress engineering or change settings');
}
assert.equal(suspendedRolls, 1);
assert(!controlled.setPlayerControlled('AI').ok);
for (const snapshot of [controlled.serialize(), { ...controlled.exportState(), playerControlled: false, isAI: true }]) {
  const humanRestored = Engine.create(catalogue, { ...profile, initialCompleted: ['p1'], playerControlled: true }, snapshot);
  assert(humanRestored.state().playerControlled, 'snapshot controller flags cannot override the current host profile');
  assert.throws(() => Engine.create(catalogue, { ...profile, isAI: true }, snapshot), /player-controlled/);
}
controlled.setPlayerControlled(true);
assert(controlled.advance(6).ok);
assert.equal(suspendedRolls, 2, 'arrival only resumes after human control returns');

// IMPERIA CW — Cold War: catalogue additions and new historical baseline receipts preserve an old plan.
const legacyPlanning = Engine.create(catalogue.slice(0, 2), { ...profile, capabilities: ['old-baseline'], initialCompleted: ['p1'] });
legacyPlanning.start('p0');
legacyPlanning.advance(3);
const enlargedCatalogue = [...catalogue, { ...base, id: 'new-entry', name: 'New Entry', initialProgress: { SOV: 25 } }];
for (const snapshot of [legacyPlanning.serialize(), legacyPlanning.exportState()]) {
  const migrated = Engine.create(enlargedCatalogue, { ...profile,
    capabilities: ['old-baseline', 'space-administration'], initialCompleted: ['p1'] }, snapshot);
  assert(migrated.state().capabilities.includes('space-administration'), 'new historical baseline capabilities survive import');
  assert(migrated.state().capabilities.includes('c1'), 'saved completed capabilities survive import');
  assert.equal(row(migrated, 'p0').progress, row(legacyPlanning, 'p0').progress);
  assert.equal(row(migrated, 'p0').spentB, row(legacyPlanning, 'p0').spentB);
  assert(row(migrated, 'p1').deployed);
  assert.equal(row(migrated, 'new-entry').progress, 25);
  assert.equal(migrated.state().reserveB, legacyPlanning.state().reserveB);
  assert.equal(migrated.state().elapsedMonths, legacyPlanning.state().elapsedMonths);
}

const engine = Engine.create(catalogue, profile);
for (const id of ['p0', 'p1', 'p2']) assert(engine.start(id).ok);
assert(!engine.start('p3').ok, 'three engineering slots must be enforced');
assert(!engine.start('dependent').ok, 'undeployed predecessors must block development');
assert(!engine.start('future').ok, 'development dates must be enforced');
engine.advance(3);
assert(row(engine, 'p0').progress < 3, 'cash cannot compress ten years of engineering into one quarter');
engine.pause('p0');
const paused = row(engine, 'p0').progress;
engine.advance(12);
assert.equal(row(engine, 'p0').progress, paused, 'paused work must remain unchanged');
assert(engine.start('p3').ok);
assert(!engine.resume('p0').ok);
engine.pause('p3');
assert(engine.resume('p0').ok);
engine.setPolicy('p0', 'accelerated');
assert.equal(row(engine, 'p0').progress, paused, 'a policy switch cannot rewrite prior work');
engine.advance(120);
assert(row(engine, 'p0').completed);
assert(!row(engine, 'p0').deployed);
assert(!engine.state().capabilities.includes('c0'));
assert(!engine.start('dependent').ok, 'engineering alone must not grant a flight qualification');
let randomCalls = 0;
assert(engine.launch('p0', () => { randomCalls += 1; return 0; }).ok);
assert.equal(randomCalls, 1);
engine.advance(3);
assert.equal(randomCalls, 1, 'objective must remain unresolved during flight');
assert.equal(engine.state().prestige, 0);
engine.advance(3);
assert.equal(randomCalls, 2, 'exactly one launcher roll and one arrival roll');
assert(row(engine, 'p0').deployed);
assert.equal(engine.state().prestige, 100);
assert(engine.start('dependent').ok);
const firstPrestige = engine.state().prestige;
engine.launch('p0', () => 0);
engine.advance(6);
assert(engine.state().prestige - firstPrestige <= 2, 'repeated missions cannot repeat the first award');
assert.deepEqual(Engine.create(catalogue, profile, engine.serialize()).state(), engine.state());

const unfunded = Engine.create(catalogue, { ...profile, annualBudgetB: 0, reserveB: 0, annualGrantB: 0 });
unfunded.start('p0');
unfunded.advance(60);
assert.equal(row(unfunded, 'p0').progress, 0, 'unfunded projects cannot advance on calendar alone');
const investigation = Engine.create(catalogue, { ...profile, initialCompleted: ['p0'] });
investigation.launch('p0', () => 0.9999);
assert.equal(row(investigation, 'p0').status, 'investigating');
assert(!investigation.launch('p0', () => 0).ok);
investigation.setBudget(0);
investigation.advance(24);
assert(row(investigation, 'p0').investigationRemainingMonths > 0, 'an unfunded investigation cannot finish');
investigation.setBudget(10000);
investigation.advance(12);
assert(row(investigation, 'p0').deployable);

const almostDone = Engine.create([{ ...base, id: 'near', name: 'Near', initialProgress: { SOV: 99.9999 } }], profile);
assert.equal(Math.round(row(almostDone, 'near').progress), 100);
assert(!row(almostDone, 'near').completed, 'rounded display percentages are not phase receipts');
assert(!almostDone.launch('near', () => 0).ok);

const groundDefinition = { ...base, id: 'ground', name: 'Ground Centre', region: 'ground',
  commissioningOnly: true, pLaunch: 1, missionCostB: 0, flightMonths: 0,
  initialProgress: { SOV: 100 }, grants: ['ground-capability'] };
const ground = Engine.create([groundDefinition], profile);
assert.equal(row(ground, 'ground').pLaunch, 1);
let acceptanceCalls = 0;
ground.launch('ground', () => { acceptanceCalls += 1; return 0; });
assert.equal(acceptanceCalls, 1, 'ground facilities have one acceptance roll and no launcher roll');
assert(row(ground, 'ground').deployed);
assert.equal(ground.state().elapsedMonths, 0, 'zero-duration ground acceptance has no artificial flight delay');
assert(!/launch/i.test(row(ground, 'ground').lastOutcome.details));

const windowDefinition = { ...base, id: 'mars', name: 'Mars', initialProgress: { SOV: 100 },
  windowCycleMonths: 26, windowOffsetMonths: 16, windowOpenMonths: 2, flightMonths: 9 };
const windows = Engine.create([windowDefinition], profile);
assert.equal(row(windows, 'mars').launchWindowWaitMonths, 16);
assert(!windows.launch('mars', () => 0).ok);
windows.advance(16);
assert.equal(row(windows, 'mars').launchWindowWaitMonths, 0);
assert(windows.launch('mars', () => 0).ok);
windows.advance(8.99);
assert(!row(windows, 'mars').deployed);
windows.advance(0.01);
assert(row(windows, 'mars').deployed);
assert(row(windows, 'mars').launchWindowWaitMonths > 0);

const fixedDefinition = { ...windowDefinition, id: 'fixed', name: 'One-off Encounter',
  fixedWindowStartMonth: 179, fixedWindowEndMonth: 180, flightMonths: 16 };
const fixed = Engine.create([fixedDefinition], profile);
assert.equal(row(fixed, 'fixed').launchWindowWaitMonths, 179);
assert(!fixed.launch('fixed', () => 0).ok);
fixed.advance(179);
assert.equal(row(fixed, 'fixed').launchWindowWaitMonths, 0);
assert(fixed.launch('fixed', () => 0).ok);
fixed.advance(16);
assert(row(fixed, 'fixed').deployed, 'a launched one-off encounter remains valid after its departure window closes');
const expired = Engine.create([fixedDefinition], profile);
expired.advance(180);
assert(row(expired, 'fixed').launchWindowExpired);
assert.equal(row(expired, 'fixed').launchWindowWaitMonths, null);
assert(!expired.launch('fixed', () => 0).ok, 'an expired one-off encounter cannot wrap into recurring windows');

// IMPERIA CW — Cold War: landing reports distinguish brief surface contact from accepted science,
// and describe a crewed return only after the complete flight campaign has elapsed.
const missionReports = {
  full_success: 'Surface expedition and Earth return verified.',
  partial_success: 'Brief touchdown telemetry received; sustained surface science remains unqualified.',
  objective_failure: 'Descent failed before surface operations could begin.',
  catastrophic_failure: 'The expedition was lost; an extended safety investigation is required.',
  launch_failure: 'THIS ARRIVAL REPORT MUST NOT OVERRIDE A LAUNCH ACCIDENT'
};
for (const [expected, objectiveDraw] of [['full_success', 0.2], ['partial_success', 0.82],
  ['objective_failure', 0.94], ['catastrophic_failure', 0.999]]) {
  const mission = Engine.create([{ ...base, id: 'surface', name: 'Mars Surface Expedition',
    initialProgress: { SOV: 100 }, flightMonths: 34, grants: ['surface-return'], outcomeDetails: missionReports }], profile);
  const draws = [0, objectiveDraw];
  assert(mission.launch('surface', () => draws.shift()).ok);
  mission.advance(33);
  assert(!row(mission, 'surface').deployed, 'arrival wording must not grant a premature surface or return receipt');
  assert.equal(draws.length, 1, 'arrival report must not resolve before the complete campaign');
  mission.advance(1);
  assert.equal(row(mission, 'surface').lastOutcome.type, expected);
  assert.equal(row(mission, 'surface').lastOutcome.details, missionReports[expected]);
  assert.equal(mission.state().capabilities.includes('surface-return'), expected === 'full_success',
    'brief contact and failed missions cannot qualify a sustained or returned expedition');
}
const reportLaunchFailure = Engine.create([{ ...base, id: 'surface', name: 'Mars Surface Expedition',
  initialProgress: { SOV: 100 }, outcomeDetails: missionReports }], profile);
reportLaunchFailure.launch('surface', () => 0.95);
assert.equal(row(reportLaunchFailure, 'surface').lastOutcome.type, 'launch_failure');
assert.match(row(reportLaunchFailure, 'surface').lastOutcome.details, /Launch failed/);
assert(!row(reportLaunchFailure, 'surface').lastOutcome.details.includes('ARRIVAL REPORT'));

// IMPERIA CW — Cold War: half-length campaign calendars and existing preview progress.
assert.equal(Catalogue.pacing.campaignYears, 25);
for (const definition of Catalogue.programmes) {
  assert.equal(definition.durationMonths, definition.baselineDurationMonths * 0.5);
}
const oldCatalogue = { ...Catalogue, pacing: { developmentScale: 1 },
  programmes: Catalogue.programmes.map(definition => ({ ...definition, durationMonths: definition.baselineDurationMonths })) };
const soviet = Catalogue.profiles.find(item => item.id === 'SOV');
const oldPlanning = Engine.create(oldCatalogue, soviet);
assert(oldPlanning.start('docking-tests').ok);
oldPlanning.advance(1);
const priorRow = row(oldPlanning, 'docking-tests');
for (const oldSave of [oldPlanning.serialize(), oldPlanning.exportState()]) {
  delete oldSave.developmentScale; // Earlier schema-2 previews had no pacing field.
  const migrated = Engine.create(Catalogue, soviet, oldSave);
  const migratedRow = row(migrated, 'docking-tests');
  assert.equal(migratedRow.progress, priorRow.progress);
  assert.equal(migratedRow.spentB, priorRow.spentB);
  assert.equal(migratedRow.calendarMonths, priorRow.calendarMonths * 0.5);
  assert.equal(migrated.state().reserveB, oldPlanning.state().reserveB);
  assert.equal(migrated.state().elapsedMonths, oldPlanning.state().elapsedMonths);
  assert.equal(row(migrated, 'salyut').calendarProgress, 90, 'omitted compact defaults must not be halved twice');
  const reopened = Engine.create(Catalogue, soviet, migrated.exportState());
  assert.equal(row(reopened, 'docking-tests').calendarMonths, migratedRow.calendarMonths);
}
const oldFlight = Engine.create(oldCatalogue, soviet);
oldFlight.start('docking-tests');
oldFlight.advance(6);
assert(oldFlight.launch('docking-tests', () => 0).ok);
const migratedFlight = Engine.create(Catalogue, soviet, oldFlight.exportState());
assert.equal(row(migratedFlight, 'docking-tests').flight.arrivesAt, row(oldFlight, 'docking-tests').flight.arrivesAt);
assert.equal(Catalogue.programmes.find(item => item.id === 'vega').fixedWindowStartMonth, 179);
assert.equal(Catalogue.programmes.find(item => item.id === 'salyut').durationMonths, 60);
assert.equal(Catalogue.programmes.find(item => item.id === 'lunar-outpost').durationMonths, 120);

// IMPERIA CW — Cold War: DDR heritage supports partner payloads, not a retroactive national launcher
// or crew transport service. A research-cosmonaut flight must retain that distinction.
const ddr = Catalogue.profiles.find(item => item.id === 'DDR');
assert(ddr, 'the DDR must have a separate historical starting situation');
for (const capability of ['space-administration', 'scientific-instruments', 'ground-tracking',
  'interkosmos-cooperation', 'orbital-payload-experience']) assert(ddr.capabilities.includes(capability));
for (const capability of ['launch-basic', 'orbital-flight', 'satellite-engineering', 'crewed-flight']) {
  assert(!ddr.capabilities.includes(capability), 'DDR payload heritage does not qualify ' + capability);
}
const researchCosmonaut = Catalogue.programmes.find(item => item.id === 'interkosmos-cosmonaut');
assert(researchCosmonaut);
assert(!researchCosmonaut.grants.includes('crewed-flight'), 'a guest research-cosmonaut flight is not independent crew transport');
assert(!researchCosmonaut.grants.includes('launch-basic'));

// IMPERIA CW — Cold War: a brief Mars surface signal cannot qualify sustained science, while the
// actual crewed expedition needs proven heavy landing, habitat endurance and complete Earth return.
const scienceLander = Catalogue.programmes.find(item => item.id === 'mars-lander');
const partialLander = Engine.create([{ ...scienceLander, initialProgress: { TEST: 100 } }],
  { ...profile, id: 'TEST', capabilities: [...scienceLander.capabilityRequirements] });
partialLander.advance(row(partialLander, scienceLander.id).launchWindowWaitMonths);
const landerDraws = [0, scienceLander.pObjective + (1 - scienceLander.pObjective) * 0.25];
assert(partialLander.launch(scienceLander.id, () => landerDraws.shift()).ok);
partialLander.advance(scienceLander.flightMonths);
assert.equal(row(partialLander, scienceLander.id).lastOutcome.type, 'partial_success');
assert(!partialLander.state().capabilities.includes('mars-surface-science'));

const crewedMars = Catalogue.programmes.find(item => item.id === 'mars-crewed-landing');
assert(crewedMars);
for (const capability of ['mars-heavy-landing-qualified', 'interplanetary-habitat-qualified',
  'mars-orbital-science', 'mars-surface-science', 'regenerative-life-support', 'heavy-lift',
  'rendezvous-docking', 'crewed-flight', 'deep-space-communications']) {
  assert(crewedMars.capabilityRequirements.includes(capability), 'crewed Mars requires ' + capability);
}
assert(!crewedMars.capabilityRequirements.includes('nuclear-thermal-flight'), 'chemical transfer must remain possible');
assert(!crewedMars.capabilityRequirements.includes('robotic-mars-ascent-return'), 'robotic sample ascent does not replace crew-scale ascent qualification');
const expeditionProfile = { ...profile, id: 'TEST', capabilities: [...crewedMars.capabilityRequirements] };
const missingHabitat = Engine.create([crewedMars], { ...expeditionProfile,
  capabilities: expeditionProfile.capabilities.filter(capability => capability !== 'interplanetary-habitat-qualified') });
missingHabitat.advance((crewedMars.minYear - profile.year) * 12);
assert(!missingHabitat.start(crewedMars.id).ok, 'funding alone cannot replace habitat qualification');
const expedition = Engine.create([crewedMars], expeditionProfile);
expedition.advance((crewedMars.minYear - profile.year) * 12);
assert(expedition.start(crewedMars.id).ok);
expedition.advance(crewedMars.durationMonths);
assert(row(expedition, crewedMars.id).completed);
const departureWait = row(expedition, crewedMars.id).launchWindowWaitMonths;
if (departureWait > 0) {
  assert(!expedition.launch(crewedMars.id, () => 0).ok, 'completed hardware must still wait for a Mars opportunity');
  expedition.advance(departureWait);
}
assert(expedition.launch(crewedMars.id, () => 0).ok);
assert.equal(row(expedition, crewedMars.id).flightRemainingMonths, 34);
expedition.advance(33);
assert(!expedition.state().capabilities.includes('crewed-mars-landing'));
assert(!expedition.state().capabilities.includes('crewed-mars-return'));
expedition.advance(1);
assert(expedition.state().capabilities.includes('crewed-mars-landing'));
assert(expedition.state().capabilities.includes('crewed-mars-return'));
assert(row(expedition, crewedMars.id).deployed);

// IMPERIA CW — Cold War: a country without inherited hardware can commission a national programme
// and purchase a foreign launch without first constructing an independent rocket industry.
const newcomer = Catalogue.profiles.find(item => item.id === 'CUSTOM');
if (newcomer) {
  assert(Catalogue.availability.playersOnly);
  for (const nation of Catalogue.profiles) assert.equal(nation.playerControlled, true);
  assert.equal(newcomer.capabilities.length, 0);
  const starter = Engine.create(Catalogue, { ...newcomer, annualBudgetB: 10000, annualGrantB: 10000, reserveB: 10000 });
  const provider = Catalogue.programmes.find(item => item.grants.includes('contracted-orbital-access'));
  assert(provider, 'a foreign provider entry must exist');
  const visiting = new Set();
  function qualify(id) {
    const definition = Catalogue.programmes.find(item => item.id === id);
    assert(definition, 'missing provider: ' + id);
    if (row(starter, id).deployed) return;
    assert(!visiting.has(id), 'entry path must not contain a dependency cycle');
    visiting.add(id);
    for (const prerequisite of definition.prerequisites) qualify(prerequisite);
    for (const capability of definition.capabilityRequirements) {
      if (starter.state().capabilities.includes(capability)) continue;
      assert.notEqual(capability, 'launch-basic', 'contracted access must not require an indigenous launcher');
      const source = Catalogue.programmes.find(item => item.grants.includes(capability)
        && !item.capabilityRequirements.includes('launch-basic'));
      assert(source, 'missing starter provider for ' + capability);
      qualify(source.id);
    }
    if (starter.state().numericYear < definition.minYear) starter.advance((definition.minYear - starter.state().numericYear) * 12);
    assert(starter.start(id).ok, 'starter path could not start ' + id);
    starter.advance(Math.max(0.01, row(starter, id).remainingMonths) + 0.01);
    assert(row(starter, id).completed, 'starter path did not finish ' + id);
    assert(starter.launch(id, () => 0).ok, 'starter path could not accept/launch ' + id);
    if (row(starter, id).flight) starter.advance(row(starter, id).flightRemainingMonths);
    assert(row(starter, id).deployed, 'starter path did not establish ' + id);
    visiting.delete(id);
  }
  qualify(provider.id);
  assert(starter.state().capabilities.includes('contracted-orbital-access'));
  assert(starter.state().capabilities.includes('orbital-flight'));
  assert(!starter.state().capabilities.includes('launch-basic'));
}

// IMPERIA CW — Cold War: funding quality must be earned over time, never bought by moving a slider.
const riskDefinition = { ...base, id: 'risk', name: 'Risk Demonstrator', durationMonths: 12, totalCostB: 12,
  grants: ['risk-flight'], supportingProgrammes: [], missionFamily: 'qualification' };
const riskFunding = Engine.create([riskDefinition], { ...profile, annualBudgetB: 0 });
const originalOdds = row(riskFunding, 'risk').pFull;
riskFunding.start('risk');
riskFunding.advance(12);
assert.equal(row(riskFunding, 'risk').progress, 0);
assert(row(riskFunding, 'risk').pFull < originalOdds, 'unfunded active work must record continuity risk');
assert(row(riskFunding, 'risk').probabilityFactors.some(item => item.id === 'funding-continuity'));
const disruptedOdds = row(riskFunding, 'risk').pFull;
riskFunding.setBudget(10000);
assert.equal(row(riskFunding, 'risk').pFull, disruptedOdds, 'raising the budget has no instantaneous assurance benefit');
riskFunding.setPolicy('risk', 'assurance');
assert.equal(row(riskFunding, 'risk').pFull, disruptedOdds, 'changing policy has no retrospective assurance benefit');
riskFunding.advance(12);
assert.equal(row(riskFunding, 'risk').fundingDisruptionMonths, 0, 'paid extended qualification repairs recorded disruption');
assert(row(riskFunding, 'risk').pFull > originalOdds);

// Delivered support, maintained facilities and related flight receipts have different meanings.
const supportDefinition = { ...base, id: 'support', name: 'Tracking Facility', region: 'ground', durationMonths: 12,
  totalCostB: 1, upkeepB: 12, missionCostB: 0, flightMonths: 0, commissioningOnly: true, pLaunch: 1,
  initialProgress: { SOV: 100 }, grants: ['tracking-proof'] };
const supportedDefinition = { ...riskDefinition, supportingProgrammes: ['support'], initialProgress: { SOV: 100 } };
const supportRisk = Engine.create([supportedDefinition, supportDefinition], { ...profile, reserveB: 0, annualGrantB: 0 });
const beforeSupport = row(supportRisk, 'risk').pFull;
assert(row(supportRisk, 'support').completed && !row(supportRisk, 'support').deployed);
assert(!row(supportRisk, 'risk').probabilityFactors.some(item => item.id === 'qualified-support'));
supportRisk.launch('support', () => 0);
assert(row(supportRisk, 'risk').pFull > beforeSupport, 'only commissioned support receives a reliability credit');
supportRisk.advance(12);
assert(row(supportRisk, 'support').maintenanceArrearsB > 0);
assert(row(supportRisk, 'risk').pFull < beforeSupport, 'unpaid support loses its credit and adds a bounded neglect penalty');

// IMPERIA CW — Cold War: explicit crew manifests create real fatality receipts, with no early arrival roll.
const crewDefinition = { ...base, id: 'crew', name: 'Crewed Expedition', durationMonths: 12, totalCostB: 12,
  initialProgress: { SOV: 100, USA: 100 }, crewSize: 3, crewAtLaunch: true, flightMonths: 2,
  grants: ['crew-proof'], pLaunch: 0.8, pObjective: 0.7, rewardEffects: { researchPoints: 5, politicalCapital: 7 },
  imageKey: 'station', supportingProgrammes: [], missionFamily: 'crew-test' };
const launchLoss = Engine.create([crewDefinition], profile);
assert(Math.abs(row(launchLoss, 'crew').pCrewLoss - 0.04) < 1e-8);
launchLoss.launch('crew', () => 0.999);
assert.equal(launchLoss.state().crewFatalities, 3);
assert.equal(launchLoss.state().politicalCapital, -12);
assert.equal(launchLoss.state().events[0].crewFatalities, 3);
assert.equal(launchLoss.state().events[0].scope, 'world');
assert(row(launchLoss, 'crew').investigationRemainingMonths >= 12);
const abort = Engine.create([crewDefinition], profile);
abort.launch('crew', () => 0.85);
assert.equal(abort.state().crewFatalities, 0, 'a launch failure with successful escape does not kill the crew');
const uncrewedCarrier = Engine.create([{ ...crewDefinition, crewAtLaunch: false }], profile);
uncrewedCarrier.launch('crew', () => 0.999);
assert.equal(uncrewedCarrier.state().crewFatalities, 0, 'an uncrewed station launch cannot kill its later visiting crew');
const arrivalLoss = Engine.create([crewDefinition], profile);
let crewRolls = 0;
arrivalLoss.launch('crew', () => ++crewRolls === 1 ? 0 : 0.999);
arrivalLoss.advance(1);
assert.equal(crewRolls, 1);
assert.equal(arrivalLoss.state().crewFatalities, 0);
arrivalLoss.advance(1);
assert.equal(crewRolls, 2);
assert.equal(arrivalLoss.state().crewFatalities, 3, 'a severe post-launch accident can lose the assigned crew');
const visitingCrew = Engine.create([{ ...crewDefinition, crewAtLaunch: false, nationalCrewSize: 1 }], profile);
let guestRolls = 0;
visitingCrew.launch('crew', () => ++guestRolls === 1 ? 0 : 0.999);
visitingCrew.advance(2);
assert.equal(visitingCrew.state().events[0].crewFatalities, 3);
assert.equal(visitingCrew.state().events[0].nationalCrewFatalities, 1);
for (const snapshot of [visitingCrew.serialize(), visitingCrew.exportState()]) {
  const restored = Engine.create([{ ...crewDefinition, crewAtLaunch: false, nationalCrewSize: 1 }], profile, snapshot);
  assert.equal(restored.state().crewFatalities, 3);
  assert.equal(restored.state().events[0].nationalCrewFatalities, 1);
}

// World firsts are authoritative once-only receipts, separate from each country's national achievement.
const firstCatalogue = { programmes: [crewDefinition], milestones: [{ id: 'first-test', capability: 'crew-proof',
  title: 'First Accepted Expedition', summary: 'The first accepted expedition returns.', prestige: 50,
  researchPoints: 3, politicalCapital: 4, imageKey: 'station' }], historicalFirsts: [] };
const sharedWorld = { schema: 1, firsts: {}, news: [] };
const winner = Engine.create(firstCatalogue, profile, null, sharedWorld);
const later = Engine.create(firstCatalogue, { ...profile, id: 'USA' }, null, sharedWorld);
winner.launch('crew', () => 0);
assert.equal(winner.state().researchPoints, 0, 'launch alone confers no mission research reward');
winner.advance(2);
assert.equal(winner.state().prestige, 150);
assert.equal(winner.state().researchPoints, 8);
assert.equal(winner.state().politicalCapital, 11);
assert.equal(winner.state().events[0].firstMilestone, 'first-test');
assert.equal(later.state().events[0].scope, 'world', 'other player profiles receive the shared world bulletin');
later.launch('crew', () => 0);
later.advance(2);
assert.equal(later.state().prestige, 100);
assert.equal(later.state().researchPoints, 5);
assert.equal(later.state().politicalCapital, 7);
assert.equal(later.state().events.find(event => event.country === 'USA').firstMilestone, null);
assert.equal(sharedWorld.firsts['first-test'].country, 'SOV');
const restoredWinner = Engine.create(firstCatalogue, profile, winner.exportState());
restoredWinner.launch('crew', () => 0);
restoredWinner.advance(2);
assert.equal(restoredWinner.state().researchPoints, 8, 'repeat flights do not farm national or world research rewards');
assert.equal(restoredWinner.state().politicalCapital, 11);
assert(restoredWinner.state().prestige <= 152);
const exportedWorld = winner.exportWorldState();
const importedWorld = Engine.create(firstCatalogue, { ...profile, id: 'USA' });
assert(importedWorld.importWorldState(exportedWorld).ok);
assert.equal(importedWorld.state().worldFirsts['first-test'].country, 'SOV');
importedWorld.setPlayerControlled(false);
assert(!importedWorld.importWorldState(exportedWorld).ok, 'AI profiles cannot manage the host ledger');
const historicalWinner = Engine.create({ ...firstCatalogue,
  historicalFirsts: [{ milestoneId: 'first-test', country: 'SOV', date: '1969-01-01' }] }, profile);
historicalWinner.launch('crew', () => 0);
historicalWinner.advance(2);
assert.equal(historicalWinner.state().prestige, 100, 'pre-1970 historical achievements are never awarded again');
assert.equal(historicalWinner.state().researchPoints, 5);
const partialFirst = Engine.create(firstCatalogue, profile);
let partialRolls = 0;
partialFirst.launch('crew', () => ++partialRolls === 1 ? 0 : 0.8);
partialFirst.advance(2);
assert.equal(partialFirst.state().researchPoints, 0);
assert.equal(partialFirst.state().worldFirsts['first-test'], undefined, 'a partial result cannot claim a world first');

// IMPERIA CW — Cold War: a Soviet first national Moon landing remains world news after Apollo 11.
const moonArchitectures = ['lunar-expedition', 'n1-l3-recovery'].map(id => ({
  ...Catalogue.programmes.find(item => item.id === id), initialProgress: { SOV: 100, USA: 100 },
  capabilityRequirements: [], prerequisites: []
}));
const nationalMoonCatalogue = { ...Catalogue, programmes: moonArchitectures };
const nationalSovietProfile = { ...Catalogue.profiles.find(item => item.id === 'SOV'), annualBudgetB: 10000,
  annualGrantB: 10000, reserveB: 10000 };
const nationalMoon = Engine.create(nationalMoonCatalogue, nationalSovietProfile);
assert(!nationalMoon.state().capabilities.includes('lunar-landing'));
nationalMoon.launch('lunar-expedition', () => 0);
nationalMoon.advance(0.5);
const sovietMoonNews = nationalMoon.state().events[0];
assert.equal(sovietMoonNews.scope, 'world');
assert.equal(sovietMoonNews.majorNationalAchievement, true);
assert.equal(sovietMoonNews.firstMilestone, null, 'a national achievement never becomes a second worldwide lunar first');
assert.equal(nationalMoon.state().worldFirsts['first-crewed-lunar-landing'].country, 'USA');
assert.equal(nationalMoon.state().worldFirsts['first-crewed-lunar-landing'].date, '1969-07-20');
assert.equal(nationalMoon.state().prestige, moonArchitectures[0].prestige, 'national Moon news receives no false worldwide-first bonus');
nationalMoon.launch('n1-l3-recovery', () => 0);
nationalMoon.advance(0.5);
assert.equal(nationalMoon.state().events[0].majorNationalAchievement, false, 'a second architecture cannot duplicate a national first');
assert.equal(nationalMoon.state().events[0].scope, 'national');
for (const snapshot of [nationalMoon.serialize(), nationalMoon.exportState()]) {
  const restored = Engine.create(nationalMoonCatalogue, nationalSovietProfile, snapshot);
  const firstNews = restored.state().events.find(event => event.programmeId === 'lunar-expedition');
  assert(firstNews.majorNationalAchievement && firstNews.scope === 'world');
  assert.equal(firstNews.firstMilestone, null);
}
const nationalUSProfile = { ...Catalogue.profiles.find(item => item.id === 'USA'), annualBudgetB: 10000,
  annualGrantB: 10000, reserveB: 10000 };
const nationalUSMoon = Engine.create(nationalMoonCatalogue, nationalUSProfile);
nationalUSMoon.launch('lunar-expedition', () => 0);
nationalUSMoon.advance(0.5);
assert.equal(nationalUSMoon.state().events[0].majorNationalAchievement, false, 'the USA already inherits its national lunar achievement');
assert.equal(nationalUSMoon.state().events[0].scope, 'national');
const foreignMoonBulletin = Engine.create(nationalMoonCatalogue, nationalUSProfile, null, nationalMoon.exportWorldState());
assert(foreignMoonBulletin.state().events.some(event => event.country === 'SOV' && event.majorNationalAchievement
  && event.scope === 'world' && event.firstMilestone === null), 'the host ledger restores major national news for other player countries');

// IMPERIA CW — Cold War: programme decisions and real transitions issue named national news without rewards.
const noticeProfile = { ...profile, id: 'GER', name: 'West Germany' };
const notices = Engine.create(catalogue, noticeProfile);
assert(notices.start('p0').ok);
assert.equal(notices.state().events[0].kind, 'programme');
assert.equal(notices.state().events[0].type, 'programme_authorised');
assert.equal(notices.state().events[0].scope, 'national');
assert(notices.state().events[0].title.startsWith('West Germany: '));
assert(notices.state().events[0].description.includes('West Germany'));
assert.deepEqual(notices.state().events[0].rewardEffects, {});
const authorisedNotices = notices.state().events.length;
assert(!notices.start('p0').ok);
notices.select('p0'); notices.setBudget(10000); notices.setPolicy('p0', 'standard');
assert.equal(notices.state().events.length, authorisedNotices, 'failed actions, selection and unchanged settings cannot generate news');
assert(notices.pause('p0').ok);
assert.equal(notices.state().events[0].type, 'programme_paused');
assert(notices.resume('p0').ok);
assert.equal(notices.state().events[0].type, 'programme_resumed');
assert(notices.cancel('p0').ok);
assert.equal(notices.state().events[0].type, 'programme_cancelled');
assert.equal(notices.state().prestige, 0);
assert.equal(notices.state().researchPoints, 0);
assert.equal(notices.state().politicalCapital, 0);
assert.equal(notices.state().crewFatalities, 0);
assert.deepEqual(notices.state().worldFirsts, {});
assert(notices.start('p0').ok);
notices.advance(120);
assert.equal(notices.state().events.filter(event => event.type === 'hardware_ready').length, 1);
notices.advance(3);
assert.equal(notices.state().events.filter(event => event.type === 'hardware_ready').length, 1, 'readiness is announced once on its real transition');
let noticeRolls = 0;
assert(notices.launch('p0', () => { noticeRolls += 1; return 0; }).ok);
assert.equal(noticeRolls, 1, 'a launch bulletin cannot consume another random draw');
assert.equal(notices.state().events[0].type, 'launch_success');
assert.equal(notices.state().prestige, 0, 'a launch bulletin does not confer mission rewards');
notices.advance(6);
assert.equal(noticeRolls, 2);
assert.equal(notices.state().events[0].kind, 'mission');
assert.equal(notices.state().events[0].type, 'full_success');
assert.equal(notices.state().events[0].countryName, 'West Germany');
assert(notices.state().events[0].title.startsWith('West Germany: '));
assert(notices.state().events[0].description.includes('West Germany'));
assert(notices.launch('p0', () => 0.9999).ok);
notices.advance(12);
assert.equal(notices.state().events[0].type, 'investigation_completed');
assert.equal(notices.state().events.filter(event => event.type === 'investigation_completed').length, 1);
notices.advance(2);
assert.equal(notices.state().events.filter(event => event.type === 'investigation_completed').length, 1);
for (const snapshot of [notices.serialize(), notices.exportState()]) {
  const reopened = Engine.create(catalogue, noticeProfile, snapshot);
  assert.equal(reopened.state().events[0].type, 'investigation_completed');
  assert(reopened.state().events.every(event => event.title.startsWith('West Germany: ') && event.description.includes('West Germany')));
  const eventCount = reopened.state().events.length;
  reopened.advance(1);
  assert.equal(reopened.state().events.length, eventCount, 'loading and advancing a stable programme cannot replay news');
  assert(reopened.start('p1').ok);
  assert.equal(new Set(reopened.state().events.map(event => event.id)).size, reopened.state().events.length, 'notice IDs remain unique after reopening');
}
const customNamedProfile = { ...profile, id: 'CUSTOM', name: 'Republic of Test' };
const customNamedCatalogue = { ...firstCatalogue,
  programmes: [{ ...crewDefinition, initialProgress: { CUSTOM: 100 } }] };
const customNamed = Engine.create(customNamedCatalogue, customNamedProfile);
customNamed.launch('crew', () => 0); customNamed.advance(2);
const namedForeign = Engine.create(customNamedCatalogue, { ...profile, id: 'USA', name: 'United States' }, null, customNamed.exportWorldState());
assert.equal(namedForeign.state().events[0].countryName, 'Republic of Test');
assert(namedForeign.state().events[0].title.startsWith('Republic of Test: '), 'foreign custom-country news retains the source nation');
assert(!namedForeign.state().events[0].title.startsWith('United States: '));
const namedRestored = Engine.create(customNamedCatalogue, customNamedProfile, customNamed.exportState());
assert(namedRestored.state().events.every(event => event.countryName === 'Republic of Test'));
const accepting = Engine.create([{ ...base, id: 'facility-trial', name: 'Facility Acceptance Trial', region: 'ground',
  initialProgress: { GER: 100 }, commissioningOnly: true, pLaunch: 1, flightMonths: 2 }], noticeProfile);
let groundNewsRolls = 0;
accepting.launch('facility-trial', () => { groundNewsRolls += 1; return 0; });
assert.equal(groundNewsRolls, 0);
assert.equal(accepting.state().events[0].type, 'commissioning_started');
accepting.advance(2);
assert.equal(groundNewsRolls, 1);
assert.equal(accepting.state().events[0].type, 'full_success');
assert(accepting.state().events[0].title.startsWith('West Germany: '));

const results = [];
for (const actualProfile of Catalogue.profiles) {
  const caps = new Set(actualProfile.capabilities);
  const deployed = new Set(actualProfile.initialCompleted || []);
  for (let pass = 0; pass < Catalogue.programmes.length; pass += 1) {
    let changed = false;
    for (const definition of Catalogue.programmes) {
      if (deployed.has(definition.id) || definition.minYear > 2020) continue;
      if (definition.capabilityRequirements.every(capability => caps.has(capability))
        && definition.prerequisites.every(id => deployed.has(id))) {
        deployed.add(definition.id);
        definition.grants.forEach(capability => caps.add(capability));
        changed = true;
      }
    }
    if (!changed) break;
  }
  assert.equal(deployed.size, Catalogue.programmes.length, actualProfile.id + ' has a blocked capability graph');
  const actual = Engine.create(Catalogue, actualProfile);
  const stress = actual.serialize();
  for (const definition of Catalogue.programmes) {
    const item = stress.programmes[definition.id];
    Object.assign(item, { status: 'operational', work: 1, calendarMonths: definition.durationMonths,
      spentB: definition.totalCostB * 1.18, launchAdjustment: 0.025, objectiveAdjustment: 0.04,
      deployed: true, launchCount: 20, missionCount: 20, successfulMissions: 20,
      firstAwardGranted: true, partialAwardGranted: 0, repeatAwardGranted: definition.prestige * 0.15 });
  }
  const advanced = Engine.create(Catalogue, actualProfile, stress);
  const compact = advanced.exportState();
  const size = Buffer.byteLength(JSON.stringify(compact), 'utf8');
  assert(size < 14000, actualProfile.id + ' persistence must leave space within the 16KB UI limit');
  const restored = Engine.create(Catalogue, actualProfile, compact);
  assert.deepEqual(restored.state().programmes, advanced.state().programmes, 'compact restore must preserve programme receipts and expenditure');
  assert.equal(restored.state().reserveB, advanced.state().reserveB);
  results.push({ profile: actualProfile.id, graphReachableThrough2020: deployed.size,
    totalProgrammes: Catalogue.programmes.length, advancedCompactBytes: size });
}
// IMPERIA CW — Cold War: active flights, world news and quality history must fit the same persistent snapshot.
const stressProfile = { ...Catalogue.profiles.find(item => item.id === 'USA'), annualBudgetB: 10000,
  annualGrantB: 10000, reserveB: 100000 };
const crowded = Engine.create(Catalogue, stressProfile).serialize();
crowded.elapsedMonths = 180;
crowded.capabilities = [...new Set(Catalogue.programmes.flatMap(item => item.grants))];
for (const definition of Catalogue.programmes) Object.assign(crowded.programmes[definition.id], {
  status: 'operational', work: 1, calendarMonths: definition.durationMonths, spentB: definition.totalCostB * 1.18,
  launchAdjustment: 0.025, objectiveAdjustment: 0.04, deployed: true,
  launchCount: 20, missionCount: 20, successfulMissions: 20, firstAwardGranted: true,
  repeatAwardGranted: definition.prestige * 0.15, fundingDisruptionMonths: 24, completedInvestigations: 2
});
const crowdedEngine = Engine.create(Catalogue, stressProfile, crowded);
for (const id of ['lunar-rover', 'lunar-sample-return', 'salyut', 'mars-lander']) {
  const wait = row(crowdedEngine, id).launchWindowWaitMonths;
  if (wait > 0) crowdedEngine.advance(wait);
  assert(crowdedEngine.launch(id, () => 0).ok);
  crowdedEngine.advance(row(crowdedEngine, id).flightRemainingMonths);
}
for (const id of ['deep-space-habitat', 'reusable-shuttle', 'cargo-ferry']) assert(crowdedEngine.launch(id, () => 0).ok);
const crowdedCompact = crowdedEngine.exportState();
const crowdedBytes = Buffer.byteLength(JSON.stringify(crowdedCompact), 'utf8');
assert(crowdedBytes < 14500, 'three active missions, firsts, news and funding history must leave room for UI state: ' + crowdedBytes);
const crowdedRestored = Engine.create(Catalogue, stressProfile, crowdedCompact);
assert.deepEqual(crowdedRestored.state().programmes, crowdedEngine.state().programmes);
assert.equal(crowdedRestored.state().researchPoints, crowdedEngine.state().researchPoints);
console.log(JSON.stringify({ ok: true, note: 'Graph reachability does not assert that all programmes can be financed or completed by 2020.',
  crowdedSnapshotBytes: crowdedBytes, results }, null, 2));
