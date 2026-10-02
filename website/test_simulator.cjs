const test = require('node:test');
const assert = require('node:assert/strict');
const {Simulator, defaults, validateConfig} = require('./simulator.js');

test('strict export contract rejects unsafe and malformed settings', () => {
  for (const patch of [{schema_version: true}, {device_id: 'sim\n'}, {display_name: 'Name\n'},
    {display_name: '   '}, {device_id: '../device'}, {response_delay_ms: 2001},
    {response_delay_ms: 0.5}, {start_disconnected: 1}, {command: 'run code'},
    {initial_rgb: {r: true, g: 0, b: 0, on: true}}, {initial_rgb: {r: 0, g: 0, b: 0, on: true, extra: 1}}]) {
    assert.throws(() => validateConfig({...defaults, ...patch}));
  }
  assert.deepEqual(validateConfig({schema_version: 1}), defaults);
});
test('configured light applies commands and preserves state on rejection', async () => {
  const simulator = new Simulator({...defaults, device_id: 'my-light', display_name: 'My light', initial_rgb: {r: 23, g: 45, b: 67, on: true}});
  assert.equal(simulator.snapshot().display_name, 'My light');
  assert.equal((await simulator.command({r: 0, g: 0, b: 255, on: true})).command.status, 'executed');
  assert.equal((await simulator.command({r: 300, g: 0, b: 0, on: true})).error.code, 'invalid_arguments');
  assert.deepEqual(simulator.state.rgb, {r: 0, g: 0, b: 255, on: true});
  assert.equal(simulator.snapshot().physical_verified, false);
});
test('offline start, ordered button edges and reconnect restore initial state', async () => {
  const simulator = new Simulator({...defaults, start_disconnected: true, initial_rgb: {r: 10, g: 20, b: 30, on: true}});
  assert.equal((await simulator.command({r: 0, g: 0, b: 255, on: true})).error.code, 'unavailable');
  assert.equal(simulator.press().ok, false);
  simulator.reconnect();
  assert.deepEqual(simulator.state.rgb, {r: 10, g: 20, b: 30, on: true});
  assert.deepEqual(simulator.press().events.map(event => event.pressed), [true, false]);
  for (let i = 0; i < 100; i++) simulator.press();
  assert.equal(simulator.events.length, 128);
  assert.equal(simulator.sequence, 202);
});
test('delay is bounded, concurrent actions rejected and stale results cannot change reset state', async () => {
  let release;
  const simulator = new Simulator({...defaults, response_delay_ms: 750});
  const pending = simulator.command({r: 255, g: 0, b: 0, on: true}, ms => {assert.equal(ms, 750); return new Promise(resolve => {release = resolve;});});
  assert.equal((await simulator.command({r: 0, g: 0, b: 255, on: true})).error.code, 'busy');
  simulator.reset({...defaults, initial_rgb: {r: 1, g: 2, b: 3, on: true}});
  release();
  assert.equal((await pending).error.code, 'cancelled');
  assert.deepEqual(simulator.state.rgb, {r: 1, g: 2, b: 3, on: true});
});
test('configuration and snapshots are detached copies', () => {
  const config = structuredClone(defaults);
  const simulator = new Simulator(config);
  config.initial_rgb.r = 222;
  const snapshot = simulator.snapshot(); snapshot.state.rgb.g = 222;
  assert.deepEqual(simulator.state.rgb, defaults.initial_rgb);
});
