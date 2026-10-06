/* Conceptual C124 workbench; no device or network access.
 * Behavior follows docs/architecture/overview.md, the current support matrix,
 * and docs/getting-started/physical-test.md. Geometry is not a board pinout. */
(() => {
  'use strict';

  const NS = 'http://www.w3.org/2000/svg';
  const instances = new WeakMap();
  const colors = [
    {name: 'green', value: '#668d70'},
    {name: 'coral', value: '#b47760'},
    {name: 'blue', value: '#688797'},
  ];
  const remoteRoute = [
    {x: 170, y: 188}, {x: 229, y: 223}, {x: 167, y: 301}, {x: 246, y: 369},
  ];

  function element(tag, attributes, parent) {
    const node = document.createElementNS(NS, tag);
    Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, String(value)));
    parent.append(node);
    return node;
  }

  function iso(u, v, height = 0) {
    return {x: 685 + u - v, y: 350 + (u + v) * .43 - height};
  }

  function polygon(points) {
    return points.map(point => `${point.x.toFixed(2)},${point.y.toFixed(2)}`).join(' ');
  }

  function square(size, height, u = 0, v = 0) {
    return polygon([
      iso(u - size, v - size, height), iso(u + size, v - size, height),
      iso(u + size, v + size, height), iso(u - size, v + size, height),
    ]);
  }

  function segment(points) {
    return points.map((point, index) => `${index ? 'L' : 'M'}${point.x.toFixed(2)} ${point.y.toFixed(2)}`).join(' ');
  }

  function curvePath(route) {
    return `M${route[0].x} ${route[0].y}C${route[1].x} ${route[1].y} ${route[2].x} ${route[2].y} ${route[3].x} ${route[3].y}`;
  }

  function curvePoint(route, progress) {
    const t = Math.max(0, Math.min(1, progress));
    const rest = 1 - t;
    return {
      x: rest ** 3 * route[0].x + 3 * rest ** 2 * t * route[1].x + 3 * rest * t ** 2 * route[2].x + t ** 3 * route[3].x,
      y: rest ** 3 * route[0].y + 3 * rest ** 2 * t * route[1].y + 3 * rest * t ** 2 * route[2].y + t ** 3 * route[3].y,
    };
  }

  function mount(container) {
    if (!(container instanceof Element)) throw new TypeError('A hardware scene container is required.');
    instances.get(container)?.destroy();

    const root = document.createElement('section');
    root.className = 'hardware-scene';
    root.setAttribute('aria-label', 'Conceptual hardware workbench');
    root.setAttribute('aria-hidden', 'true');
    root.inert = true;
    root.dataset.active = 'false';
    root.dataset.online = 'true';
    root.dataset.mode = 'led';
    root.dataset.frame = '0';
    root.dataset.phase = '0.000';
    root.innerHTML = `
      <div class="hardware-art">
        <svg class="hardware-canvas" viewBox="0 0 1000 560" preserveAspectRatio="none" aria-hidden="true" focusable="false"></svg>
        <img class="hardware-bot-mark" src="media/grok-bot-mark.svg" alt="" width="86" height="86">
        <span class="hardware-label hardware-bot-label">Grok Bot</span>
        <span class="hardware-label hardware-future-label">Future link</span>
        <span class="hardware-label hardware-gateway-label">Gateway<span>USB bridge</span></span>
        <span class="hardware-label hardware-usb-label">USB</span>
        <span class="hardware-label hardware-board-label">C124 concept</span>
      </div>
      <div class="hardware-console">
        <div class="hardware-controls" role="group" aria-label="Explore the hardware stories">
          <button type="button" data-hardware-action="led" aria-pressed="true" aria-label="Illustrate an LED command; press again to change color"><span class="hardware-control-icon hardware-led-icon" aria-hidden="true"></span>LED</button>
          <button type="button" data-hardware-action="button" aria-pressed="false" aria-label="Illustrate a button press and release"><span class="hardware-control-icon hardware-button-icon" aria-hidden="true"></span>Button</button>
          <button type="button" data-hardware-action="usb" aria-pressed="false" aria-label="Unplug the illustrated USB cable"><span class="hardware-control-icon hardware-usb-icon" aria-hidden="true"></span>USB</button>
        </div>
        <p class="hardware-readout" role="status" aria-live="polite" aria-atomic="true">LED command → device report.</p>
        <a class="hardware-caption" href="doc-docs-public-support-matrix.html">Illustration · Grok Bot + hardware unverified.</a>
      </div>`;
    container.append(root);

    const svg = root.querySelector('.hardware-canvas');
    const art = root.querySelector('.hardware-art');
    const readout = root.querySelector('.hardware-readout');
    const controls = root.querySelector('.hardware-controls');
    const buttons = [...controls.querySelectorAll('button')];
    const usbLabel = root.querySelector('.hardware-usb-label');
    const bench = element('g', {class: 'hardware-bench'}, svg);
    element('polygon', {points: square(132, -16)}, bench);
    [[-145, 0], [145, 0], [0, -145], [0, 145]].forEach(([u, v]) => {
      element('path', {d: segment([iso(u - 8, v, -16), iso(u + 8, v, -16)])}, bench);
      element('path', {d: segment([iso(u, v - 8, -16), iso(u, v + 8, -16)])}, bench);
    });

    const linkGroup = element('g', {class: 'hardware-links'}, svg);
    element('path', {d: curvePath(remoteRoute), class: 'hardware-future-route'}, linkGroup);
    element('path', {d: 'M186 280l-4 10 9-4', class: 'hardware-future-arrow'}, linkGroup);
    const cable = element('path', {class: 'hardware-cable'}, linkGroup);
    const cableTwin = element('path', {class: 'hardware-cable-twin'}, linkGroup);

    const gateway = element('g', {class: 'hardware-gateway'}, svg);
    element('path', {
      d: 'M214 383l71-38 72 38-72 40Z M214 383v13l71 40 72-40v-13 M285 423v13',
      class: 'hardware-gateway-case',
    }, gateway);
    element('path', {d: 'M251 380l34-18 35 18-35 19Z M262 382l23-12 23 12-23 12Z', class: 'hardware-gateway-chip'}, gateway);
    const eventMarks = element('g', {class: 'hardware-event-marks', opacity: 0}, gateway);
    element('path', {d: 'M241 399l17 9M264 412l13 7'}, eventMarks);
    element('path', {d: 'M313 414l16-9M333 403l9-5', class: 'hardware-gateway-ports'}, gateway);

    const guides = element('g', {class: 'hardware-layer-guides'}, svg);
    [[-100, -100], [100, -100], [100, 100], [-100, 100]].forEach(([u, v]) => {
      element('path', {d: segment([iso(u, v, 0), iso(u, v, 176)])}, guides);
    });

    const base = element('g', {class: 'hardware-base'}, svg);
    element('polygon', {points: square(100, 0), class: 'hardware-base-bottom'}, base);
    element('polygon', {points: polygon([iso(-100, 100, 0), iso(100, 100, 0), iso(100, 100, 51), iso(-100, 100, 51)]), class: 'hardware-base-face'}, base);
    element('polygon', {points: polygon([iso(100, -100, 0), iso(100, 100, 0), iso(100, 100, 51), iso(100, -100, 51)]), class: 'hardware-base-face'}, base);
    element('polygon', {points: square(100, 51), class: 'hardware-base-rim'}, base);
    element('polygon', {points: square(87, 51), class: 'hardware-base-inner'}, base);
    element('path', {d: segment([iso(-100, 100, 7), iso(100, 100, 7), iso(100, -100, 7)]), class: 'hardware-case-seam'}, base);

    const pcb = element('g', {class: 'hardware-pcb'}, svg);
    element('polygon', {points: square(88, 107), class: 'hardware-pcb-plane'}, pcb);
    element('path', {d: segment([iso(-88, 88, 107), iso(-88, 88, 101), iso(88, 88, 101), iso(88, -88, 101), iso(88, -88, 107)]), class: 'hardware-pcb-edge'}, pcb);
    const chip = element('g', {class: 'hardware-chip'}, pcb);
    element('polygon', {points: square(32, 113, 5, -5)}, chip);
    element('polygon', {points: square(23, 113, 5, -5), class: 'hardware-chip-inner'}, chip);
    // These traces and pads are illustrative; their placement is not a pin map.
    for (let index = 0; index < 6; index += 1) {
      const offset = -23 + index * 10;
      element('path', {d: segment([iso(offset, -41, 112), iso(offset, -32, 112)])}, chip);
      element('path', {d: segment([iso(offset + 10, 23, 112), iso(offset + 10, 32, 112)])}, chip);
      element('path', {d: segment([iso(-31, offset - 5, 112), iso(-40, offset - 5, 112)])}, chip);
      element('path', {d: segment([iso(37, offset - 5, 112), iso(46, offset - 5, 112)])}, chip);
    }
    const traces = [
      [[-40, -20], [-66, -20], [-66, -61], [-77, -61]],
      [[-40, 0], [-55, 0], [-55, 57], [-77, 57]],
      [[46, 12], [68, 12], [68, 64], [77, 64]],
      [[18, -41], [18, -66], [63, -66], [63, -76]],
      [[5, 32], [5, 59], [44, 59], [44, 76]],
    ];
    traces.forEach(trace => element('path', {d: segment(trace.map(([u, v]) => iso(u, v, 109))), class: 'hardware-trace'}, pcb));
    [[-72, -68], [72, -68], [72, 68], [-72, 68]].forEach(([u, v]) => {
      const center = iso(u, v, 108);
      element('ellipse', {cx: center.x, cy: center.y, rx: 7, ry: 3.1, class: 'hardware-pcb-hole'}, pcb);
    });

    const lid = element('g', {class: 'hardware-lid'}, svg);
    element('polygon', {points: square(100, 176), class: 'hardware-lid-top'}, lid);
    element('path', {d: segment([iso(-100, 100, 176), iso(-100, 100, 165), iso(100, 100, 165), iso(100, -100, 165), iso(100, -100, 176)]), class: 'hardware-lid-edge'}, lid);
    element('path', {d: segment([iso(100, 100, 165), iso(100, 100, 176)]), class: 'hardware-lid-edge'}, lid);
    element('polygon', {points: square(78, 177), class: 'hardware-button-plate'}, lid);
    const ledSurface = element('polygon', {points: square(56, 178), class: 'hardware-led-surface'}, lid);
    const ledInner = element('polygon', {points: square(38, 179), class: 'hardware-led-inner'}, lid);
    element('path', {d: segment([iso(-63, -63, 178), iso(-63, -44, 178)]) + ' ' + segment([iso(63, 63, 178), iso(63, 44, 178)]), class: 'hardware-button-detail'}, lid);

    const port = element('g', {class: 'hardware-port'}, svg);
    element('polygon', {points: polygon([iso(-80, 101, 13), iso(-36, 101, 13), iso(-36, 101, 35), iso(-80, 101, 35)])}, port);
    element('path', {d: segment([iso(-72, 102, 24), iso(-44, 102, 24)]), class: 'hardware-port-contact'}, port);
    const plug = element('g', {class: 'hardware-plug'}, svg);
    element('polygon', {points: polygon([iso(-75, 107, 18), iso(-41, 107, 18), iso(-41, 136, 18), iso(-75, 136, 18)])}, plug);
    element('path', {d: segment([iso(-75, 107, 18), iso(-75, 107, 32), iso(-41, 107, 32), iso(-41, 136, 32), iso(-75, 136, 32), iso(-75, 107, 32)])}, plug);
    element('path', {d: segment([iso(-75, 136, 32), iso(-75, 136, 18), iso(-41, 136, 18), iso(-41, 136, 32)]), class: 'hardware-plug-end'}, plug);
    element('path', {d: segment([iso(-75, 127, 32), iso(-41, 127, 32)]), class: 'hardware-plug-seam'}, plug);

    const packets = [0, 1].map(() => {
      const group = element('g', {class: 'hardware-packet', opacity: 0}, svg);
      element('path', {d: 'M-10 0H3M-2-5 4 0-2 5'}, group);
      return group;
    });

    const media = window.matchMedia('(prefers-reduced-motion: reduce)');
    let active = false;
    let destroyed = false;
    let visible = true;
    let permitted = !document.documentElement.hasAttribute('data-reduced-motion')
      && !document.body?.hasAttribute('data-reduced-motion');
    let online = true;
    let mode = 'led';
    let colorIndex = 0;
    let ledOn = false;
    let retainedEvents = false;
    let journey = {kind: 'led', elapsed: 0};
    let phase = 0;
    let unplug = 0;
    let raf = 0;
    let frame = 0;
    let lastTime = null;
    let lastDraw = 0;

    function canAnimate() {
      return active && visible && permitted && !media.matches && !document.hidden && !destroyed;
    }

    function usbRoute() {
      const end = iso(-58, 138, 24);
      return [{x: 351, y: 396}, {x: 403, y: 441}, {x: 445 - unplug * .3, y: 376}, {x: end.x - unplug, y: end.y + unplug * .43}];
    }

    function placePacket(index, route, progress, returning = false) {
      if (!online || progress < 0 || progress > 1) return;
      const t = returning ? 1 - progress : progress;
      const at = curvePoint(route, t);
      const before = curvePoint(route, Math.max(0, t - .005));
      const after = curvePoint(route, Math.min(1, t + .005));
      const angle = Math.atan2(after.y - before.y, after.x - before.x) * 180 / Math.PI + (returning ? 180 : 0);
      packets[index].setAttribute('transform', `translate(${at.x.toFixed(2)} ${at.y.toFixed(2)}) rotate(${angle.toFixed(2)})`);
      packets[index].setAttribute('opacity', 1);
    }

    function finishJourney() {
      if (!journey) return;
      if (journey.kind === 'led') {
        ledOn = true;
        readout.textContent = 'Execution reported · physical check pending.';
      } else {
        retainedEvents = true;
        readout.textContent = 'Button → gateway · no Bot wake.';
      }
      journey = null;
      root.dataset.transmitting = 'false';
    }

    function render(snap = false) {
      if (destroyed) return;
      const targetUnplug = online ? 0 : 58;
      unplug += (targetUnplug - unplug) * (snap || !canAnimate() ? 1 : .2);
      const route = usbRoute();
      cable.setAttribute('d', curvePath(route));
      cableTwin.setAttribute('d', curvePath(route.map(point => ({x: point.x, y: point.y + 4}))));
      plug.setAttribute('transform', `translate(${-unplug.toFixed(2)} ${(unplug * .43).toFixed(2)})`);
      const press = journey?.kind === 'button' && journey.elapsed < .62
        ? Math.sin((journey.elapsed / .62) * Math.PI) * 16 : 0;
      const hover = Math.sin(phase * .8) * 4;
      lid.setAttribute('transform', `translate(0 ${(hover + press).toFixed(2)})`);
      pcb.setAttribute('transform', `translate(0 ${(Math.sin(phase * .8 + 1.2) * 2).toFixed(2)})`);
      const light = online && (ledOn || (journey?.kind === 'led' && journey.elapsed >= 2.6));
      ledSurface.setAttribute('fill-opacity', light ? .17 : .025);
      ledInner.setAttribute('fill-opacity', light ? .45 : .025);
      ledInner.setAttribute('stroke-opacity', light ? .7 : .25);
      eventMarks.setAttribute('opacity', retainedEvents ? .8 : 0);
      packets.forEach(packet => packet.setAttribute('opacity', 0));
      if (journey && online) {
        const time = journey.elapsed;
        if (journey.kind === 'led') {
          if (time <= 1.15) placePacket(0, remoteRoute, time / 1.15);
          else if (time >= 1.4 && time <= 2.6) placePacket(0, route, (time - 1.4) / 1.2);
          else if (time >= 2.9 && time <= 4.1) placePacket(0, route, (time - 2.9) / 1.2, true);
          else if (time >= 4.35 && time <= 5.5) placePacket(0, remoteRoute, (time - 4.35) / 1.15, true);
        } else {
          placePacket(0, route, (time - .25) / 1.25, true);
          placePacket(1, route, (time - .65) / 1.25, true);
          if (time >= 1.5) eventMarks.setAttribute('opacity', .8);
        }
      }
      root.dataset.phase = phase.toFixed(3);
      root.dataset.frame = String(frame);
      root.dataset.packets = String(packets.filter(packet => packet.getAttribute('opacity') === '1').length);
    }

    function updateControls() {
      root.dataset.mode = mode;
      root.dataset.online = String(online);
      root.style.setProperty('--hardware-led', colors[colorIndex].value);
      buttons.forEach(button => {
        const action = button.dataset.hardwareAction;
        button.setAttribute('aria-pressed', String(action === 'usb' ? !online : mode === action));
        if (action === 'usb') button.setAttribute('aria-label', online ? 'Unplug the illustrated USB cable' : 'Reconnect the illustrated USB cable');
      });
      usbLabel.textContent = online ? 'USB' : 'Offline';
    }

    function perform(action) {
      if (!active || destroyed) return;
      mode = action;
      if (action === 'usb') {
        const interruptedCommand = online && journey?.kind === 'led'
          && journey.elapsed >= 1.4 && journey.elapsed < 4.1;
        online = !online;
        journey = null;
        ledOn = false;
        root.dataset.transmitting = 'false';
        readout.textContent = online ? 'USB restored · send a new command.'
          : interruptedCommand ? 'USB offline · command unconfirmed.' : 'USB offline · commands unavailable.';
      } else if (!online) {
        journey = null;
        readout.textContent = action === 'button' ? 'USB offline · no button event reaches the gateway.' : 'USB offline · commands unavailable.';
      } else {
        if (action === 'led') {
          colorIndex = (colorIndex + 1) % colors.length;
          ledOn = false;
          readout.textContent = `LED ${colors[colorIndex].name} → device report.`;
        } else {
          readout.textContent = 'Button → gateway · no Bot wake.';
        }
        journey = {kind: action, elapsed: 0};
        root.dataset.transmitting = 'true';
        if (!canAnimate()) finishJourney();
      }
      updateControls();
      render(!canAnimate());
    }

    function onAction(event) {
      const button = event.target.closest('[data-hardware-action]');
      if (button && controls.contains(button)) perform(button.dataset.hardwareAction);
    }

    function tick(time) {
      raf = 0;
      if (!canAnimate()) {lastTime = null; return;}
      const elapsed = lastTime === null ? 0 : Math.min((time - lastTime) / 1000, .08);
      lastTime = time;
      phase += elapsed;
      if (journey) {
        journey.elapsed += elapsed;
        if (journey.kind === 'button' && journey.elapsed >= 1.5) retainedEvents = true;
        if (journey.elapsed >= (journey.kind === 'led' ? 5.5 : 2.05)) finishJourney();
      }
      if (time - lastDraw >= 32) {
        frame += 1;
        render();
        lastDraw = time;
      }
      raf = window.requestAnimationFrame(tick);
    }

    function syncMotion() {
      if (raf) window.cancelAnimationFrame(raf);
      raf = 0;
      lastTime = null;
      root.dataset.moving = String(canAnimate());
      if (canAnimate()) raf = window.requestAnimationFrame(tick);
    }

    function onMotion(event) {
      if (typeof event.detail?.canAnimate === 'boolean') permitted = event.detail.canAnimate;
      syncMotion();
    }

    function onMediaChange() {
      permitted = !document.documentElement.hasAttribute('data-reduced-motion')
        && !document.body?.hasAttribute('data-reduced-motion');
      syncMotion();
    }

    controls.addEventListener('click', onAction);
    document.addEventListener('grok:motion-change', onMotion);
    document.addEventListener('visibilitychange', syncMotion);
    media.addEventListener('change', onMediaChange);
    const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      syncMotion();
    }, {threshold: .01}) : null;
    observer?.observe(art);

    const api = {
      setActive(value) {
        if (destroyed) return;
        active = Boolean(value);
        root.dataset.active = String(active);
        root.inert = !active;
        root.setAttribute('aria-hidden', String(!active));
        if (active && (!permitted || media.matches)) finishJourney();
        if (active) render(true);
        syncMotion();
      },
      destroy() {
        if (destroyed) return;
        destroyed = true;
        syncMotion();
        observer?.disconnect();
        controls.removeEventListener('click', onAction);
        document.removeEventListener('grok:motion-change', onMotion);
        document.removeEventListener('visibilitychange', syncMotion);
        media.removeEventListener('change', onMediaChange);
        root.remove();
        instances.delete(container);
      },
    };

    updateControls();
    root.dataset.transmitting = 'true';
    render(true);
    instances.set(container, api);
    return api;
  }

  window.GrokHardwareScene = Object.freeze({mount});
})();
