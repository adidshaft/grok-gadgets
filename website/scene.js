/* A local illustration. No network or hardware requests are made. */
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
    grok: ['Grok', 'Your existing Grok Bot. Actual connection remains pending.', 'start.html', 'The connection path'],
    gateway: ['Gateway', 'Routes commands. Reports device state.', 'architecture.html', 'Explore the architecture'],
    esp32: ['ESP32', 'AtomS3 Lite C124. USB first. LED and button.', 'esp32.html', 'Meet the first gadget'],
    linux: ['Linux', 'Declare capabilities. Connect your own device application.', 'linux.html', 'Build with the Linux SDK'],
    home: ['Home Assistant', 'A direct upstream MCP route for exposed entities.', 'home-assistant.html', 'Connect an existing home'],
  };
  const palette = {off: '#fbfbf8', green: '#55866c', blue: '#446da4', coral: '#c66b50'};
  let selected = 'gateway';
  let view = 'system';
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
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  let reduced = preference.matches || document.documentElement.hasAttribute('data-reduced-motion');
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

  function project(point) {
    const [x, y, z] = point;
    const theta = .18 + Math.sin(phase * .35) * .29;
    const c = Math.cos(theta), s = Math.sin(theta);
    const rx = x * c - z * s;
    const rz = x * s + z * c;
    return [500 + rx * 1.11, 344 + rz * .48 - y * .93 + Math.sin(phase * .45) * 11];
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
  function activeRoute(route) {
    if (view !== 'system') return route.to === 'esp32' || route.to === 'gateway';
    return selected === 'grok' || selected === 'gateway' && route.to !== 'home' || route.to === selected;
  }
  function render() {
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
    ledSurface.setAttribute('fill', connected ? palette[led] : palette.off);
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
      const active = activeRoute(route);
      const available = connected || route.to !== 'esp32';
      route.path.setAttribute('stroke', active && available ? '#20201c' : '#cecec5');
      route.path.setAttribute('stroke-width', active ? '1.3' : '.8');
      const t = ((phase * .15 + index * .24) % 1);
      const reverse = view === 'button' && route.to === 'esp32';
      const u = reverse ? 1 - t : t;
      const p = [Math.pow(1 - u, 2) * a[0] + 2 * (1 - u) * u * b[0] + u * u * c[0], Math.pow(1 - u, 2) * a[1] + 2 * (1 - u) * u * b[1] + u * u * c[1]];
      route.packet.setAttribute('cx', p[0]); route.packet.setAttribute('cy', p[1]);
      route.packet.setAttribute('opacity', active && available ? '.95' : '0');
    });
    const scale = Math.min(rect.width / 1000, rect.height / 700);
    const dx = (rect.width - scale * 1000) / 2, dy = (rect.height - scale * 700) / 2;
    buttons.forEach((button) => {
      const key = button.dataset.node;
      const p = project(positions[key]);
      const offset = key === 'grok' ? -82 : key === 'linux' ? -118 : key === 'home' ? 35 : key === 'gateway' ? -105 : 53;
      const half = button.offsetWidth / 2 + 8;
      const x = dx + p[0] * scale;
      button.style.left = `${Math.max(half, Math.min(rect.width - half, x))}px`;
      button.style.top = `${dy + (p[1] + offset) * scale}px`;
    });
    const elapsed = phase - eventAt;
    const pulse = project([e[0] - 34, e[1] + 14, e[2] + 32]);
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
    render();
  }
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
  function feedback(message) {
    root.querySelector('#scene-feedback').textContent = message || `LED ${led} · ${events} button events · ${connected ? 'connected' : 'disconnected'}`;
  }
  buttons.forEach((button) => button.addEventListener('click', () => {view = 'system'; root.dataset.view = 'system'; root.querySelectorAll('[data-view]').forEach((control) => control.setAttribute('aria-pressed', String(control.dataset.view === 'system'))); setDetail(button.dataset.node);}));
  root.querySelectorAll('[data-view]').forEach((button) => button.addEventListener('click', () => setView(button.dataset.view)));
  root.querySelectorAll('[data-led]').forEach((button) => button.addEventListener('click', () => {
    setView('led');
    if (!connected) {feedback('Device disconnected · command unconfirmed'); return;}
    led = button.dataset.led;
    root.querySelectorAll('[data-led]').forEach((control) => control.setAttribute('aria-pressed', String(control.dataset.led === led)));
    feedback(); render();
  }));
  root.querySelector('#scene-press').addEventListener('click', () => {
    setView('button');
    if (!connected) {feedback('Device disconnected · no button event'); return;}
    events += 2; eventAt = phase;
    feedback(); render();
  });
  root.querySelector('#scene-disconnect').addEventListener('click', (event) => {
    connected = !connected;
    root.toggleAttribute('data-disconnected', !connected);
    event.currentTarget.setAttribute('aria-pressed', String(!connected));
    event.currentTarget.textContent = connected ? 'Disconnect' : 'Reconnect';
    feedback(); render();
  });
  function tick(time) {
    raf = 0;
    if (reduced || document.hidden || !visible) {lastTime = null; return;}
    if (lastTime !== null) phase += Math.min((time - lastTime) / 1000, .1);
    lastTime = time;
    if (time - drawAt >= 32) {render(); drawAt = time;}
    raf = requestAnimationFrame(tick);
  }
  function syncMotion() {
    if (raf) cancelAnimationFrame(raf);
    raf = 0; lastTime = null;
    if (!reduced && !document.hidden && visible) raf = requestAnimationFrame(tick);
  }
  document.addEventListener('grok:motion-change', (event) => {reduced = Boolean(event.detail.reduced); syncMotion();});
  preference.addEventListener('change', () => {reduced = preference.matches || document.documentElement.hasAttribute('data-reduced-motion'); syncMotion();});
  document.addEventListener('visibilitychange', syncMotion);
  if ('IntersectionObserver' in window) new IntersectionObserver(([entry]) => {visible = entry.isIntersecting; syncMotion();}, {threshold: .01}).observe(stage);
  if ('ResizeObserver' in window) new ResizeObserver(() => {rect = stage.getBoundingClientRect(); render();}).observe(stage);
  else window.addEventListener('resize', () => {rect = stage.getBoundingClientRect(); render();});
  render(); syncMotion();
})();
