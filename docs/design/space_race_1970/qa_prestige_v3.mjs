// IMPERIA CW — Cold War: shared player rankings, transferable benefits and actual upkeep accounting.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const engineFile = new URL('space-race-engine-v2.js', import.meta.url);
vm.runInThisContext(fs.readFileSync(engineFile, 'utf8'));
const Engine = globalThis.SpaceRaceEngine;
const defs = [0, 1, 2].map(i => ({ id: 'p' + i, name: 'Mission ' + i, region: 'leo',
  minYear: 1970, durationMonths: 12, totalCostB: 12, upkeepB: i === 0 ? 12 : 0,
  missionCostB: 0, flightMonths: 6, pLaunch: 0.9, pObjective: 0.8, prestige: i === 2 ? 120 : 100,
  grants: [], prerequisites: [], capabilityRequirements: [], supportingProgrammes: [] }));
const profiles = ['USA', 'SOV', 'FRA'].map((id, i) => ({ id,
  name: ['United States', 'Soviet Union', 'France'][i], year: 1970,
  annualBudgetB: 0, annualGrantB: 0, reserveB: 1000, capabilities: [] }));
const catalogue = { programmes: defs, profiles };
const world = { schema: 1, firsts: {}, news: [], standings: {
  CHI: { countryName: 'China', prestige: 9999, playerControlled: false, isAI: true }
} };
function prepared(profile, prestige) {
  const fresh = Engine.create(catalogue, profile, null, world), saved = fresh.serialize();
  saved.prestige = prestige;
  for (const p of Object.values(saved.programmes)) Object.assign(p, {
    work: 1, calendarMonths: 12, spentB: 12, status: 'ready'
  });
  Object.assign(saved.programmes.p0, { status: 'operational', deployed: true, firstAwardGranted: true });
  return Engine.create(catalogue, profile, saved, world);
}
const usa = prepared(profiles[0], 100), sov = prepared(profiles[1], 80), fra = prepared(profiles[2], 60);
const row = (engine, id) => engine.state().programmes.find(p => p.id === id);
assert.deepEqual(usa.state().topThree.map(e => e.country), ['USA', 'SOV', 'FRA']);
assert(usa.state().leadership.active && !sov.state().leadership.active);
assert(Math.abs(row(usa, 'p1').pObjective - row(sov, 'p1').pObjective - 0.02) < 1e-9);
const before = usa.state().reserveB;
usa.advance(1);
assert(Math.abs(before - usa.state().reserveB - 0.95) < 1e-9, 'leader actually pays 5% less upkeep');
assert(Math.abs(usa.state().annualOperatingCostB - 11.4) < 1e-9);
assert(usa.launch('p1', () => 0).ok);
const locked = row(usa, 'p1').pObjective;
const staleSnapshot = usa.exportState();
assert(sov.launch('p1', () => 0).ok);
sov.advance(6);
assert(sov.state().leadership.active && !usa.state().leadership.active, 'lead transfers after earned prestige overtakes');
const reconnect = Engine.create(catalogue, profiles[0], staleSnapshot, world);
assert.equal(reconnect.state().leadership.leader.country, 'SOV', 'a stale national save cannot overwrite another player’s current host score');
assert.equal(row(usa, 'p1').pObjective, locked, 'a departed mission retains its authorised risk');
assert.equal(usa.state().annualOperatingCostB, 12, 'former leader immediately loses discount');
const previous = usa.state().reserveB;
usa.advance(1);
assert(Math.abs(previous - usa.state().reserveB - 1) < 1e-9);
assert(fra.launch('p2', () => 0).ok);
fra.advance(6);
assert(fra.state().leadership.tied && !fra.state().leadership.active && !sov.state().leadership.active);
assert.deepEqual(fra.state().topThree.map(e => e.rank), [1, 1, 3]);
sov.setPlayerControlled(false);
assert(fra.state().leadership.active && !fra.state().topThree.some(e => e.country === 'SOV'));
sov.setPlayerControlled(true);
assert(fra.state().leadership.tied && !fra.state().leadership.active);
const restored = Engine.create(catalogue, profiles[0], usa.exportState());
assert.deepEqual(restored.state().topThree, usa.state().topThree);
assert.equal(row(restored, 'p1').pObjective, locked);
const empty = Engine.create(catalogue, profiles[0]);
assert.equal(empty.state().topThree.length, 0);
assert(!empty.state().leadership.active && !empty.state().leadership.leader);
console.log(JSON.stringify({ok:true, checks:'shared top three, actual upkeep, transfer, ties, AI exclusion, frozen risk, save restoration, empty start'}));
