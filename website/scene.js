/* A browser simulator and architecture illustration. No network or hardware requests. */
(() => {
  'use strict';
  const root = document.querySelector('.home-scene');
  if (!root) return;
  const stage = root.querySelector('.scene-stage');
  const svg = root.querySelector('.scene-canvas');
  const NS = 'http://www.w3.org/2000/svg';
  const group = (id) => root.querySelector(`#${id}`);
  const make = (tag, attrs, parent) => {
    const element = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([key, value]) => element.setAttribute(key, value));
    parent.appendChild(element);
    return element;
  };
  const positions = {
    grok: [-230, 175, -135], gateway: [5, 45, 0],
    esp32: [240, 5, 165], linux: [250, 40, -235], home: [-265, 5, 205],
  };
  const details = {
    grok: ['Grok Bot', 'Your existing Grok Bot. Actual connection remains pending.', 'start.html', 'The connection path'],
    gateway: ['Gateway', 'Routes commands. Reports device state.', 'architecture.html', 'Explore the architecture'],
    esp32: ['ESP32', 'AtomS3 Lite C124. USB first. LED and button.', 'esp32.html', 'Meet the first gadget'],
    linux: ['Linux', 'Declare capabilities. Connect your own device application.', 'linux.html', 'Build with the Linux SDK'],
    home: ['Home Assistant', 'A direct upstream MCP route for exposed entities.', 'home-assistant.html', 'Connect an existing home'],
  };
  const palette = {off: '#fbfbf8', green: '#55866c', blue: '#446da4', coral: '#c66b50'};
  let selected = 'gateway';
  let view = 'system';
  const simulator = new GrokSimulator.Simulator();
  let led = 'off';
  let connected = true;
  let events = 0;
  let eventAt = -10;
  let frame = 0;
  let phase = 0;
  let raf = 0;
  let lastTime = null;
  let drawAt = 0;
  let visible = true;
  let story = 'light';
  let storyStarted = 0;
  let geometryDirty = true;
  const storyRoutes = {light: 'esp32', sensor: 'linux', display: 'linux', home: 'home'};
  const storyCopy = {
    light: ['Virtual light', 'Conceptual route to the browser simulator. Controls below change only simulated state.', 'simulator.html', 'Try the simulator'],
    sensor: ['Sample sensor', 'Conceptual sensor reading over the Linux SDK route. No live sensor is connected.', 'linux.html', 'Explore Linux'],
    display: ['Pi display', 'Conceptual Raspberry Pi display route. No Pi or screen is connected.', 'linux.html', 'Explore Linux'],
    home: ['Home Assistant', 'Conceptual route to entities exposed by Home Assistant’s own MCP server.', 'home-assistant.html', 'Explore Home Assistant'],
  };
  let reduced = document.documentElement.hasAttribute('data-reduced-motion');
  const buttons = [...root.querySelectorAll('[data-node]')];
  const groundPath = make('path', {fill: 'none', stroke: '#dcdcd4', 'stroke-width': '.7'}, group('scene-ground'));
  const edgePath = make('path', {fill: 'none', stroke: '#b9b9af', 'stroke-width': '.8'}, group('scene-ground'));
  const orbitalPath = make('path', {fill: 'none', stroke: '#d7d7ce', 'stroke-width': '.8'}, group('scene-ground'));
  const objectPaths = {};
  Object.keys(positions).forEach((key) => {
    objectPaths[key] = make('path', {fill: 'none', stroke: '#76766e', 'stroke-width': '1', 'stroke-linejoin': 'round'}, group('scene-objects'));
  });
  const ledSurface = make('path', {fill: palette.off, stroke: '#31312c', 'stroke-width': '1'}, group('scene-objects'));
  const routes = [['grok', 'gateway'], ['gateway', 'esp32'], ['gateway', 'linux'], ['grok', 'home']].map(([from, to]) => ({
    from, to,
    path: make('path', {fill: 'none', stroke: '#b8b8af', 'stroke-width': '1', 'stroke-dasharray': from === 'grok' && to === 'home' ? '3 5' : 'none'}, group('scene-routes')),
    packet: make('circle', {r: '2.5', fill: '#32322d'}, group('scene-packets')),
  }));
  const buttonPulse = make('circle', {fill: 'none', stroke: '#20201d', 'stroke-width': '1', opacity: '0'}, group('scene-packets'));
  let rect = stage.getBoundingClientRect();
  const buttonSizes = new Map(buttons.map(button => [button, button.getBoundingClientRect().width]));
  const curves = new Map();

  function project(point) {
    const [x, y, z] = point;
    const theta = .18;
    const c = Math.cos(theta), s = Math.sin(theta);
    const rx = x * c - z * s;
    const rz = x * s + z * c;
    return [500 + rx * 1.11, 344 + rz * .48 - y * .93];
  }
  function line(a, b) {
    const p = project(a), q = project(b);
    return `M${p[0].toFixed(2)},${p[1].toFixed(2)}L${q[0].toFixed(2)},${q[1].toFixed(2)}`;
  }
  function polygon(points) {
    return points.map((point, index) => {
      const p = project(point);
      return `${index ? 'L' : 'M'}${p[0].toFixed(2)},${p[1].toFixed(2)}`;
    }).join('') + 'Z';
  }
  function wireBox(center, width, height, depth) {
    const [x, y, z] = center;
    const points = [[-1, 0, -1], [1, 0, -1], [1, 0, 1], [-1, 0, 1], [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1]]
      .map(([a, b, c]) => [x + a * width / 2, y + b * height, z + c * depth / 2]);
    return [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]].map(([a, b]) => line(points[a], points[b])).join('');
  }
  function ring(center, radius, axis = 'y', segments = 72) {
    let result = '';
    let prior = null;
    for (let i = 0; i <= segments; i++) {
      const a = Math.PI * 2 * i / segments;
      const u = Math.cos(a) * radius, v = Math.sin(a) * radius;
      const p = axis === 'x' ? [center[0], center[1] + u, center[2] + v] : axis === 'z' ? [center[0] + u, center[1] + v, center[2]] : [center[0] + u, center[1], center[2] + v];
      if (prior) result += line(prior, p);
      prior = p;
    }
    return result;
  }
  function render() {
    if (geometryDirty) {
    let grid = '';
    for (let x = -375; x <= 375; x += 75) grid += line([x, -68, -310], [x, -68, 310]);
    for (let z = -310; z <= 310; z += 62) grid += line([-375, -68, z], [375, -68, z]);
    groundPath.setAttribute('d', grid);
    edgePath.setAttribute('d', polygon([[-375, -68, -310], [375, -68, -310], [375, -68, 310], [-375, -68, 310]]) + line([-375, -75, 310], [-375, -105, 310]) + line([375, -75, 310], [375, -105, 310]) + line([375, -75, -310], [375, -105, -310]));
    orbitalPath.setAttribute('d', ring([0, -68, 0], 440) + ring([0, -68, 0], 457));
    const g = positions.grok;
    objectPaths.grok.setAttribute('d', ring(g, 64) + ring(g, 64, 'x') + ring(g, 64, 'z') + ring([g[0], g[1] - 34, g[2]], 52) + ring([g[0], g[1] + 34, g[2]], 52) + line([g[0], g[1] - 64, g[2]], [g[0], -68, g[2]]));
    const w = positions.gateway;
    let gateway = wireBox(w, 100, 82, 100) + wireBox([w[0], w[1] + 12, w[2]], 77, 58, 77);
    for (let y = 45; y <= 125; y += 20) gateway += polygon([[-50, y, -50], [60, y, -50], [60, y, 50], [-50, y, 50]]);
    gateway += ring([w[0], 31, w[2]], 106) + ring([w[0], 26, w[2]], 111) + line([w[0], w[1], w[2]], [w[0], -68, w[2]]);
    objectPaths.gateway.setAttribute('d', gateway);
    const e = positions.esp32;
    let board = wireBox(e, 118, 12, 118) + wireBox([e[0] - 9, e[1] + 12, e[2] - 9], 46, 12, 46) + wireBox([e[0], e[1] - 4, e[2] + 64], 34, 14, 13);
    for (let p = -44; p <= 44; p += 11) board += line([e[0] - 59, 17, e[2] + p], [e[0] - 46, 17, e[2] + p]) + line([e[0] + 46, 17, e[2] + p], [e[0] + 59, 17, e[2] + p]);
    board += ring([e[0] - 34, e[1] + 14, e[2] + 32], 10) + line([e[0], e[1], e[2]], [e[0], -68, e[2]]);
    objectPaths.esp32.setAttribute('d', board);
    ledSurface.setAttribute('d', polygon([[e[0] + 23, 18, e[2] - 41], [e[0] + 44, 18, e[2] - 41], [e[0] + 44, 18, e[2] - 20], [e[0] + 23, 18, e[2] - 20]]));
    const output = simulator.state.rgb;
    ledSurface.setAttribute('fill', output.on ? `rgb(${output.r},${output.g},${output.b})` : palette.off);
    const l = positions.linux;
    let linux = wireBox(l, 90, 100, 67) + wireBox([l[0], l[1] + 15, l[2] + 35], 64, 59, 5);
    for (let y = 125; y <= 135; y += 5) linux += line([l[0] - 29, y, l[2] + 34], [l[0] + 29, y, l[2] + 34]);
    linux += line([l[0], l[1], l[2]], [l[0], -68, l[2]]);
    objectPaths.linux.setAttribute('d', linux);
    const h = positions.home;
    let home = wireBox(h, 92, 60, 90);
    const roof = [[h[0] - 54, 65, h[2] - 51], [h[0], 110, h[2] - 51], [h[0] + 54, 65, h[2] - 51], [h[0] - 54, 65, h[2] + 51], [h[0], 110, h[2] + 51], [h[0] + 54, 65, h[2] + 51]];
    home += [[0, 1], [1, 2], [3, 4], [4, 5], [0, 3], [1, 4], [2, 5]].map(([a, b]) => line(roof[a], roof[b])).join('');
    home += wireBox([h[0], h[1], h[2] + 46], 24, 40, 1) + line([h[0], h[1], h[2]], [h[0], -68, h[2]]);
    objectPaths.home.setAttribute('d', home);
    Object.entries(objectPaths).forEach(([name, path]) => path.setAttribute('stroke', name === selected ? '#171714' : '#898981'));
    routes.forEach((route, index) => {
      const from = positions[route.from], to = positions[route.to];
      const start = [from[0], from[1] + 15, from[2]], end = [to[0], to[1] + 20, to[2]];
      const middle = [(start[0] + end[0]) / 2, Math.max(start[1], end[1]) + 40, (start[2] + end[2]) / 2];
      const a = project(start), b = project(middle), c = project(end);
      route.path.setAttribute('d', `M${a.join(',')}Q${b.join(',')} ${c.join(',')}`);
      curves.set(route.to, [a, b, c]);
      route.path.setAttribute('stroke', '#cecec5');
      route.path.setAttribute('stroke-width', '.8');
    });
    const scale = Math.min(rect.width / 1000, rect.height / 700);
    const dx = (rect.width - scale * 1000) / 2, dy = (rect.height - scale * 700) / 2;
    buttons.forEach((button) => {
      const key = button.dataset.node;
      const p = project(positions[key]);
      const offset = key === 'grok' ? -82 : key === 'linux' ? -118 : key === 'home' ? 35 : key === 'gateway' ? -105 : 53;
      const half = (buttonSizes.get(button) || 44) / 2 + 8;
      const x = dx + p[0] * scale;
      button.style.left = `${Math.max(half, Math.min(rect.width - half, x))}px`;
      const halfY = button.getBoundingClientRect().height / 2 + 8;
      const centerY = dy + (p[1] + offset) * scale;
      button.style.top = `${Math.max(halfY, Math.min(rect.height - halfY, centerY))}px`;
    });
      geometryDirty = false;
    }
    const output = simulator.state.rgb;
    ledSurface.setAttribute('fill', output.on ? `rgb(${output.r},${output.g},${output.b})` : palette.off);
    const selectedRoute = storyRoutes[story];
    routes.forEach(route => {
      const active = route.to === selectedRoute;
      const [a, b, c] = curves.get(route.to);
      const t = active ? Math.min(1, Math.max(0, (phase - storyStarted) / 3.3)) : 0;
      const point = [Math.pow(1-t,2)*a[0]+2*(1-t)*t*b[0]+t*t*c[0], Math.pow(1-t,2)*a[1]+2*(1-t)*t*b[1]+t*t*c[1]];
      route.path.setAttribute('stroke', active && (connected || route.to !== 'esp32') ? '#20201c' : '#cecec5');
      route.path.setAttribute('stroke-width', active ? '1.3' : '.8');
      route.packet.setAttribute('cx', point[0]); route.packet.setAttribute('cy', point[1]);
      route.packet.setAttribute('opacity', active && !reduced && phase-storyStarted < 3.3 ? '.95' : '0');
    });
    const elapsed = phase - eventAt;
    const board = positions.esp32;
    const pulse = project([board[0] - 34, board[1] + 14, board[2] + 32]);
    buttonPulse.setAttribute('cx', pulse[0]); buttonPulse.setAttribute('cy', pulse[1]);
    buttonPulse.setAttribute('r', 12 + Math.min(elapsed, 1) * 34);
    buttonPulse.setAttribute('opacity', !reduced && connected && elapsed >= 0 && elapsed < 1 ? 1 - elapsed : 0);
    stage.dataset.frame = String(++frame);
    stage.dataset.phase = phase.toFixed(3);
  }
  function setDetail(name) {
    selected = name;
    buttons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.node === name)));
    const detail = details[name];
    root.querySelector('#scene-detail-name').textContent = detail[0];
    root.querySelector('#scene-detail').textContent = detail[1];
    const link = root.querySelector('#scene-detail-link');
    link.href = detail[2]; link.textContent = `${detail[3]} ↗`;
    geometryDirty = true;
    render();
  }
  function selectStory(name) {
    story = name; storyStarted = phase;
    selected = name === 'home' ? 'home' : name === 'sensor' || name === 'display' ? 'linux' : 'esp32';
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.node === selected)));
    root.querySelectorAll('[data-story]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.story === name)));
    const copy = storyCopy[name];
    root.querySelector('#scene-detail-name').textContent = copy[0];
    root.querySelector('#scene-detail').textContent = copy[1];
    const link = root.querySelector('#scene-detail-link');
    link.href = copy[2]; link.textContent = `${copy[3]} ↗`;
    geometryDirty = true; render(); syncMotion();
  }
  root.querySelectorAll('[data-story]').forEach(button => button.addEventListener('click', () => selectStory(button.dataset.story)));
  root.querySelector('#scene-replay').addEventListener('click', () => selectStory(story));
  function setView(name) {
    view = name;
    root.dataset.view = name;
    root.querySelectorAll('[data-view]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.view === name)));
    setDetail(name === 'system' ? 'gateway' : 'esp32');
    if (name !== 'system') {
      root.querySelector('#scene-detail-name').textContent = name === 'led' ? 'LED output' : 'Button input';
      root.querySelector('#scene-detail').textContent = name === 'led' ? 'Set a colour. See a simulated execution report.' : 'Press once. Read a simulated press and release.';
    }
  }
  const form = document.querySelector('#playground-config');
  const stateOutput = document.querySelector('#playground-state');
  const report = document.querySelector('#playground-report');
  const phaseLabel = document.querySelector('#playground-phase');
  const configFeedback = document.querySelector('#playground-config-feedback');
  function feedback(message) {
    const output = simulator.state.rgb;
    const reported = output.on ? `last reported #${[output.r,output.g,output.b].map(value => value.toString(16).padStart(2,'0')).join('')}` : 'last reported off';
    root.querySelector('#scene-feedback').textContent = message || (connected
      ? `${simulator.config.display_name} · LED ${led} · ${events} button events · connected`
      : `${simulator.config.display_name} · ${reported} · disconnected · current output unknown · ${events} button events`);
  }
  function sync(message, result) {
    connected = simulator.available; events = simulator.sequence;
    const color = simulator.state.rgb;
    led = color.on ? `#${[color.r, color.g, color.b].map(value => value.toString(16).padStart(2, '0')).join('')}` : 'off';
    root.toggleAttribute('data-disconnected', !connected);
    const disconnect = root.querySelector('#scene-disconnect');
    disconnect.setAttribute('aria-pressed', String(!connected));
    disconnect.textContent = connected ? 'Disconnect' : 'Reconnect';
    root.querySelectorAll('[data-led]').forEach(control => control.setAttribute('aria-pressed', String(control.dataset.led === 'off' && !color.on || palette[control.dataset.led] === led)));
    stateOutput.textContent = JSON.stringify(simulator.snapshot(), null, 2);
    if (result) report.textContent = JSON.stringify(result, null, 2);
    feedback(message); render();
  }
  function readConfig() {
    const hex = form.elements.color.value;
    const brightness = Number(form.elements.brightness.value) / 100;
    return GrokSimulator.validateConfig({schema_version: 1,
      device_id: form.elements.device_id.value, display_name: form.elements.display_name.value,
      initial_rgb: {r: Math.round(parseInt(hex.slice(1, 3), 16) * brightness),
        g: Math.round(parseInt(hex.slice(3, 5), 16) * brightness), b: Math.round(parseInt(hex.slice(5, 7), 16) * brightness),
        on: form.elements.start_on.checked}, response_delay_ms: Number(form.elements.response_delay_ms.value),
      start_disconnected: form.elements.start_disconnected.checked});
  }
  function configAction(action) {
    try {
      if (!form.reportValidity()) return;
      const config = readConfig(); action(config);
    } catch (error) { configFeedback.textContent = error.message; }
  }
  async function send(arguments_, label) {
    if (simulator.busy) { feedback('A command is pending · wait for its execution report'); return; }
    const generation = simulator.generation;
    setView('led');
    phaseLabel.textContent = simulator.available ? 'Requested → accepted · waiting for the virtual device' : 'Requested → unavailable';
    feedback(simulator.available ? 'Command accepted · waiting for simulated execution' : 'Device disconnected · command unconfirmed');
    const result = await simulator.command(arguments_);
    if (generation !== simulator.generation) return;
    phaseLabel.textContent = result.ok ? 'Requested → accepted → simulated execution reported' : `Requested → ${result.error.code}`;
    sync(result.ok ? null : `Command ${result.error.code} · LED unchanged`, result);
    if (result.ok && label) feedback(`${simulator.config.display_name} · LED ${label} · ${events} button events · connected`);
  }
  buttons.forEach(button => button.addEventListener('click', () => {view = 'system'; root.dataset.view = 'system'; root.querySelectorAll('[data-view]').forEach(control => control.setAttribute('aria-pressed', String(control.dataset.view === 'system'))); setDetail(button.dataset.node);}));
  root.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => setView(button.dataset.view)));
  root.querySelectorAll('[data-led]').forEach(button => button.addEventListener('click', () => {
    const choice = button.dataset.led;
    if (choice === 'off') {send({...simulator.state.rgb, on: false}, 'off'); return;}
    const hex = palette[choice];
    send({r: parseInt(hex.slice(1, 3), 16), g: parseInt(hex.slice(3, 5), 16), b: parseInt(hex.slice(5, 7), 16), on: true}, choice);
  }));
  root.querySelector('#scene-press').addEventListener('click', () => {
    setView('button');
    const result = simulator.press(); eventAt = phase;
    phaseLabel.textContent = result.ok ? 'Simulated button press → release → two events' : 'Device unavailable · no event';
    sync(result.ok ? null : 'Device disconnected · no button event', result); syncMotion();
  });
  root.querySelector('#scene-disconnect').addEventListener('click', () => {
    if (simulator.available) simulator.disconnect(); else simulator.reconnect();
    phaseLabel.textContent = simulator.available ? 'Reconnected · starting state restored' : 'Offline · commands will fail';
    sync();
  });
  form.addEventListener('submit', event => {
    event.preventDefault(); configAction(config => {
      document.querySelector('#playground-export-preview').hidden = true; simulator.reset(config); report.textContent = 'No command yet.'; phaseLabel.textContent = 'Restarted · your starting state';
      configFeedback.textContent = 'Applied. The virtual device has restarted.';
      setView('led'); sync();
    });
  });
  document.querySelector('#playground-custom-color').addEventListener('click', () => configAction(config => send({...config.initial_rgb, on: true}, 'custom')));
  document.querySelector('#playground-export').addEventListener('click', () => configAction(config => {
    const exported = GrokSimulator.exportConfiguration(config);
    const json = exported.content;
    document.querySelector('#playground-export-json').value = json;
    document.querySelector('#playground-export-preview').hidden = false;
    const url = URL.createObjectURL(new Blob([json], {type: 'application/json'}));
    const link = document.createElement('a'); link.href = url; link.download = exported.filename;
    document.body.appendChild(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    configFeedback.textContent = 'Configuration ready. Save the download, or copy the JSON below into my-light.json. Keep the kit’s simulator-config.json unchanged.';
  }));
  document.querySelector('#playground-copy').addEventListener('click', async () => {
    const output = document.querySelector('#playground-export-json');
    try { await navigator.clipboard.writeText(output.value); configFeedback.textContent = 'Copied. Save as my-light.json and use --config ./my-light.json. Keep the bundled default unchanged.'; }
    catch { output.focus(); output.select(); configFeedback.textContent = 'Select and copy the JSON, then save it as my-light.json. Keep the bundled default unchanged.'; }
  });
  form.elements.brightness.addEventListener('input', () => {document.querySelector('#playground-brightness').value = `${form.elements.brightness.value}%`;});
  document.querySelector('#playground-reset').addEventListener('click', () => {
    form.reset(); document.querySelector('#playground-export-preview').hidden = true; document.querySelector('#playground-brightness').value = '100%';
    simulator.reset(readConfig()); report.textContent = 'No command yet.'; phaseLabel.textContent = 'Ready · browser simulation'; configFeedback.textContent = 'Defaults restored.'; sync();
  });
  simulator.reset(readConfig()); sync();
  function tick(time) {
    raf = 0;
    if (reduced || document.hidden || !visible) {lastTime = null; return;}
    if (lastTime !== null) phase += Math.min((time - lastTime) / 1000, .1);
    lastTime = time;
    if (time - drawAt >= 32) {render(); drawAt = time;}
    if (phase - storyStarted < 3.3 || phase - eventAt < 1) raf = requestAnimationFrame(tick);
  }
  function syncMotion() {
    if (raf) cancelAnimationFrame(raf);
    raf = 0; lastTime = null;
    if (!reduced && !document.hidden && visible) raf = requestAnimationFrame(tick);
  }
  document.addEventListener('grok:motion-change', (event) => {reduced = !event.detail.canAnimate; syncMotion();});
  document.addEventListener('visibilitychange', syncMotion);
  if ('IntersectionObserver' in window) new IntersectionObserver(([entry]) => {visible = entry.isIntersecting; syncMotion();}, {threshold: .01}).observe(stage);
  if ('ResizeObserver' in window) new ResizeObserver(() => {rect = stage.getBoundingClientRect(); buttons.forEach(button => buttonSizes.set(button, button.getBoundingClientRect().width)); geometryDirty = true; render();}).observe(stage);
  else window.addEventListener('resize', () => {rect = stage.getBoundingClientRect(); buttons.forEach(button => buttonSizes.set(button, button.getBoundingClientRect().width)); geometryDirty = true; render();});
  root.classList.add('scene-ready');
  buttons.forEach(button => buttonSizes.set(button, button.getBoundingClientRect().width));
  geometryDirty = true; selectStory('light'); sync(); syncMotion();
})();
