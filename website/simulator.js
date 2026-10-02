/* Apache-2.0. Browser-only behavior; never calls Grok or physical devices. */
(function (scope) {
  'use strict';
  const defaults = {schema_version: 1, device_id: 'sim-c124', display_name: 'Desk light',
    initial_rgb: {r: 0, g: 0, b: 0, on: false}, response_delay_ms: 0, start_disconnected: false};
  const clone = value => JSON.parse(JSON.stringify(value));
  const exact = (value, fields) => value && typeof value === 'object' && !Array.isArray(value)
    && Object.keys(value).every(key => fields.includes(key));
  function rgb(value) {
    return exact(value, ['r', 'g', 'b', 'on']) && ['r', 'g', 'b'].every(key =>
      Number.isInteger(value[key]) && value[key] >= 0 && value[key] <= 255) && typeof value.on === 'boolean';
  }
  function validateConfig(value) {
    if (!exact(value, Object.keys(defaults)) || value.schema_version !== 1) throw new Error('Use simulator configuration version 1.');
    const config = {...clone(defaults), ...clone(value)};
    if (typeof config.device_id !== 'string' || (!/^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$/.test(config.device_id) || /[^A-Za-z0-9._:-]/.test(config.device_id))) throw new Error('Device ID: 1–64 letters, numbers, dots, underscores, colons or hyphens.');
    if (typeof config.display_name !== 'string' || (!/^[\x20-\x7E]{1,80}$/.test(config.display_name) || /[^\x20-\x7E]/.test(config.display_name)) || !config.display_name.trim()) throw new Error('Name: 1–80 printable English characters.');
    if (!rgb(config.initial_rgb)) throw new Error('Starting LED needs integer RGB channels 0–255 and an on/off value.');
    if (!Number.isInteger(config.response_delay_ms) || config.response_delay_ms < 0 || config.response_delay_ms > 2000) throw new Error('Response delay must be 0–2000 milliseconds.');
    if (typeof config.start_disconnected !== 'boolean') throw new Error('Offline startup must be true or false.');
    return config;
  }
  class Simulator {
    constructor(config = defaults) { this.generation = 0; this.reset(config); }
    reset(config = this.config) {
      this.config = validateConfig(config); this.generation += 1;
      this.state = {rgb: clone(this.config.initial_rgb), button: {pressed: false}};
      this.available = !this.config.start_disconnected;
      this.events = []; this.sequence = 0; this.commands = []; this.busy = false;
    }
    snapshot() { return {device_id: this.config.device_id, display_name: this.config.display_name,
      simulated: true, physical_verified: false, available: this.available, state: clone(this.state)}; }
    disconnect() { this.available = false; this.generation += 1; this.busy = false; }
    reconnect() {
      this.available = true; this.generation += 1; this.busy = false;
      this.state = {rgb: clone(this.config.initial_rgb), button: {pressed: false}};
    }
    press() {
      if (!this.available) return {ok: false, error: {code: 'unavailable'}};
      const edges = [true, false].map(pressed => ({sequence: ++this.sequence, pressed, simulated: true}));
      this.events.push(...edges); this.events = this.events.slice(-128);
      return {ok: true, events: clone(edges)};
    }
    async command(arguments_, wait = ms => new Promise(resolve => setTimeout(resolve, ms))) {
      if (!rgb(arguments_)) return {ok: false, error: {code: 'invalid_arguments'}};
      if (!this.available) return {ok: false, error: {code: 'unavailable'}};
      if (this.busy) return {ok: false, error: {code: 'busy'}};
      const generation = this.generation;
      this.busy = true;
      await wait(this.config.response_delay_ms);
      if (generation !== this.generation) return {ok: false, error: {code: 'cancelled'}};
      this.busy = false;
      if (!this.available) return {ok: false, error: {code: 'unavailable'}};
      this.state.rgb = clone(arguments_);
      const command = {capability: 'rgb.set', arguments: clone(arguments_), status: 'executed',
        simulated: true, physical_verified: false, reported_state: clone(this.state)};
      this.commands.push(command); this.commands = this.commands.slice(-8);
      return {ok: true, command};
    }
  }
  const api = {defaults: clone(defaults), validateConfig, Simulator};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else scope.GrokSimulator = api;
})(typeof window !== 'undefined' ? window : globalThis);
