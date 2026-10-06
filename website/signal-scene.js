/* A local, conceptual signal sculpture. This illustration makes no requests. */
(() => {
  'use strict';

  const NS = 'http://www.w3.org/2000/svg';
  const TAU = Math.PI * 2;
  const CENTER = {x: 500, y: 322};
  const MODES = [
    {id: 'light', label: 'Light', angle: .05, response: 'Light responds'},
    {id: 'sensor', label: 'Sensor', angle: 1.78, response: 'Reading returns'},
    {id: 'display', label: 'Display', angle: 3.53, response: 'Display responds'},
  ];
  const instances = new WeakMap();

  function svgElement(tag, attributes, parent) {
    const element = document.createElementNS(NS, tag);
    Object.entries(attributes).forEach(([name, value]) => element.setAttribute(name, value));
    parent.appendChild(element);
    return element;
  }

  function ellipsePoint(angle, radiusX, radiusY, rotation) {
    const x = Math.cos(angle) * radiusX;
    const y = Math.sin(angle) * radiusY;
    return {
      x: CENTER.x + x * Math.cos(rotation) - y * Math.sin(rotation),
      y: CENTER.y + x * Math.sin(rotation) + y * Math.cos(rotation),
    };
  }

  function ellipsePath(radiusX, radiusY, rotation) {
    const points = [];
    for (let step = 0; step <= 96; step += 1) {
      const point = ellipsePoint(step / 96 * TAU, radiusX, radiusY, rotation);
      points.push(`${step ? 'L' : 'M'}${point.x.toFixed(2)} ${point.y.toFixed(2)}`);
    }
    return points.join(' ') + 'Z';
  }

  function curvePoint(start, control, end, progress) {
    const rest = 1 - progress;
    return {
      x: rest * rest * start.x + 2 * rest * progress * control.x + progress * progress * end.x,
      y: rest * rest * start.y + 2 * rest * progress * control.y + progress * progress * end.y,
    };
  }

  function place(element, point) {
    element.setAttribute('cx', point.x.toFixed(2));
    element.setAttribute('cy', point.y.toFixed(2));
  }

  function mount(container) {
    if (!(container instanceof Element)) throw new TypeError('Signal scene needs a container element.');
    if (instances.has(container)) return instances.get(container);

    const root = document.createElement('div');
    root.className = 'signal-scene';
    root.setAttribute('role', 'group');
    root.setAttribute('aria-label', 'Conceptual signal illustration with simulated destinations');
    root.hidden = true;

    const svg = svgElement('svg', {
      class: 'signal-canvas', viewBox: '0 0 1000 700',
      'aria-hidden': 'true', focusable: 'false',
    }, root);
    const orbitGroup = svgElement('g', {class: 'signal-orbits', fill: 'none'}, svg);
    const orbits = Array.from({length: 4}, (_, index) => svgElement('path', {
      class: `signal-orbit signal-orbit-${index}`,
    }, orbitGroup));
    const ticks = svgElement('path', {class: 'signal-ticks'}, orbitGroup);
    const route = svgElement('path', {class: 'signal-route'}, orbitGroup);

    const ambientGroup = svgElement('g', {class: 'signal-ambient'}, svg);
    const ambient = Array.from({length: 3}, () => svgElement('circle', {r: 2.5}, ambientGroup));
    const sourceHalo = svgElement('circle', {
      class: 'signal-source-halo', cx: CENTER.x, cy: CENTER.y, r: 58, fill: 'none',
    }, svg);
    const sourcePulse = svgElement('circle', {
      class: 'signal-pulse', cx: CENTER.x, cy: CENTER.y, r: 58, fill: 'none', opacity: 0,
    }, svg);

    const targetGroup = svgElement('g', {class: 'signal-target-marks'}, svg);
    const trailGroup = svgElement('g', {class: 'signal-trail'}, svg);
    const trail = Array.from({length: 10}, (_, index) => svgElement('circle', {
      r: 1.3 + index * .21, opacity: 0,
    }, trailGroup));
    const packet = svgElement('circle', {class: 'signal-packet', r: 4, opacity: 0}, svg);

    const source = document.createElement('button');
    source.type = 'button';
    source.className = 'signal-source';
    source.innerHTML = '<span>Grok Bot</span><span class="signal-source-action" aria-hidden="true">Send ↗</span>';
    source.style.left = `${CENTER.x / 10}%`;
    source.style.top = `${CENTER.y / 7}%`;
    root.appendChild(source);

    const targets = MODES.map(mode => {
      const point = ellipsePoint(mode.angle, 328, 190, -.17);
      const ring = svgElement('circle', {
        class: 'signal-target-ring', cx: point.x, cy: point.y, r: 14, fill: 'none',
      }, targetGroup);
      const responseRing = svgElement('circle', {
        class: 'signal-response', cx: point.x, cy: point.y, r: 18, fill: 'none', opacity: 0,
      }, targetGroup);
      const dot = svgElement('circle', {
        class: 'signal-target-dot', cx: point.x, cy: point.y, r: 4,
      }, targetGroup);
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'signal-target';
      button.dataset.signalTarget = mode.id;
      button.setAttribute('aria-label', `${mode.label}: send a conceptual signal`);
      button.setAttribute('aria-pressed', 'false');
      button.style.left = `${point.x / 10}%`;
      button.style.top = `${point.y / 7}%`;
      const label = document.createElement('span');
      label.textContent = mode.label;
      button.appendChild(label);
      root.appendChild(button);
      return {...mode, point, ring, responseRing, dot, button};
    });

    const caption = document.createElement('div');
    caption.className = 'signal-caption';
    const label = document.createElement('span');
    label.textContent = 'Conceptual signal';
    const phaseLabel = document.createElement('span');
    phaseLabel.className = 'signal-phase';
    caption.append(label, phaseLabel);
    root.appendChild(caption);

    const status = document.createElement('p');
    status.className = 'signal-sr-only';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.setAttribute('aria-atomic', 'true');
    root.appendChild(status);
    container.appendChild(root);

    const media = window.matchMedia('(prefers-reduced-motion: reduce)');
    let permitted = !document.documentElement.hasAttribute('data-reduced-motion');
    let active = false;
    let visible = true;
    let destroyed = false;
    let selected = targets[0];
    let phase = 0;
    let transmission = null;
    let completed = false;
    let frame = 0;
    let lastTime = null;
    let lastDraw = 0;
    let pointer = {x: 0, y: 0};
    let tilt = {x: 0, y: 0};
    let lastPhaseLabel = '';

    function canAnimate() {
      return active && visible && permitted && !media.matches && !document.hidden && !destroyed;
    }

    function setPhaseLabel(value) {
      if (lastPhaseLabel === value) return;
      phaseLabel.textContent = value;
      lastPhaseLabel = value;
    }

    function routeControl(returning) {
      const dx = selected.point.x - CENTER.x;
      const dy = selected.point.y - CENTER.y;
      const side = returning ? -.28 : .28;
      return {x: CENTER.x + dx * .5 - dy * side, y: CENTER.y + dy * .5 + dx * side};
    }

    function packetPoint(progress, returning) {
      const control = routeControl(returning);
      return returning
        ? curvePoint(selected.point, control, CENTER, progress)
        : curvePoint(CENTER, control, selected.point, progress);
    }

    function finishTransmission() {
      transmission = null;
      completed = true;
      root.removeAttribute('data-transmitting');
      setPhaseLabel(`${selected.label} · simulated`);
      status.textContent = `${selected.response} in this local illustration. No Grok Bot or hardware connection.`;
    }

    function updateSelection() {
      targets.forEach(target => {
        const isSelected = target === selected;
        target.button.setAttribute('aria-pressed', String(isSelected));
        target.ring.classList.toggle('is-selected', isSelected);
        target.dot.classList.toggle('is-selected', isSelected);
        target.responseRing.setAttribute('opacity', 0);
      });
      source.setAttribute('aria-label', `Send a conceptual signal to the simulated ${selected.label.toLowerCase()}`);
      setPhaseLabel(`${selected.label} · simulated`);
    }

    function render() {
      if (destroyed) return;
      const configurations = [
        [328, 190, -.17],
        [286, 115 + Math.sin(phase * .18) * 13 + tilt.y * 9, .52 + Math.sin(phase * .15) * .14 + tilt.x * .08],
        [245, 153 + Math.sin(phase * .14 + 1) * 12, -.83 + Math.sin(phase * .17) * .12 - tilt.x * .07],
        [238, 76 + Math.sin(phase * .17 + 2) * 9, 1.28 + Math.sin(phase * .13) * .11 + tilt.y * .07],
      ];
      configurations.forEach((configuration, index) => {
        orbits[index].setAttribute('d', ellipsePath(...configuration));
      });
      ambient.forEach((dot, index) => {
        place(dot, ellipsePoint(phase * (.085 + index * .019) + index * 2.1, ...configurations[index + 1]));
      });
      sourceHalo.setAttribute('r', (58 + Math.sin(phase * .9) * 2).toFixed(2));
      const control = routeControl(false);
      route.setAttribute('d', `M${CENTER.x} ${CENTER.y} Q${control.x.toFixed(2)} ${control.y.toFixed(2)} ${selected.point.x.toFixed(2)} ${selected.point.y.toFixed(2)}`);

      packet.setAttribute('opacity', 0);
      trail.forEach(dot => dot.setAttribute('opacity', 0));
      sourcePulse.setAttribute('opacity', 0);
      targets.forEach(target => target.responseRing.setAttribute('opacity', 0));

      if (transmission !== null) {
        const time = transmission;
        const returning = time >= 1.8;
        const progress = returning ? Math.min(1, (time - 1.8) / 1.35) : Math.min(1, time / 1.4);
        const travelling = time < 1.4 || returning;
        if (travelling) {
          place(packet, packetPoint(progress, returning));
          packet.setAttribute('opacity', 1);
          trail.forEach((dot, index) => {
            const distance = (trail.length - index) * .023;
            if (progress < distance) return;
            place(dot, packetPoint(progress - distance, returning));
            dot.setAttribute('opacity', (.06 + index * .045).toFixed(2));
          });
        }
        if (time < .9) {
          sourcePulse.setAttribute('r', (58 + time * 65).toFixed(2));
          sourcePulse.setAttribute('opacity', ((1 - time / .9) * .55).toFixed(2));
        }
        if (time > 1.15 && time < 2.5) {
          const responseTime = time - 1.15;
          selected.responseRing.setAttribute('r', (14 + responseTime * 31).toFixed(2));
          selected.responseRing.setAttribute('opacity', (Math.sin(responseTime / 1.35 * Math.PI) * .7).toFixed(2));
        }
        setPhaseLabel(returning ? 'Simulated return' : `${selected.label} · signal`);
      } else if (completed) {
        selected.responseRing.setAttribute('r', 22);
        selected.responseRing.setAttribute('opacity', .42);
      }
    }

    function tick(time) {
      frame = 0;
      if (!canAnimate()) {lastTime = null; return;}
      const delta = lastTime === null ? 0 : Math.min((time - lastTime) / 1000, .08);
      lastTime = time;
      phase += delta;
      tilt.x += (pointer.x - tilt.x) * Math.min(1, delta * 4);
      tilt.y += (pointer.y - tilt.y) * Math.min(1, delta * 4);
      if (transmission !== null) {
        transmission += delta;
        if (transmission >= 3.15) finishTransmission();
      }
      if (time - lastDraw >= 32) {render(); lastDraw = time;}
      frame = requestAnimationFrame(tick);
    }

    function syncMotion() {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
      lastTime = null;
      if (canAnimate()) frame = requestAnimationFrame(tick);
    }

    function send(target) {
      if (!active || destroyed) return;
      selected = target;
      completed = false;
      updateSelection();
      if (canAnimate()) {
        transmission = 0;
        root.setAttribute('data-transmitting', '');
        status.textContent = `Conceptual signal to the simulated ${selected.label.toLowerCase()}.`;
      } else {
        finishTransmission();
      }
      render();
      syncMotion();
    }

    function onSourceClick() {send(selected);}
    function onTargetClick(event) {
      const target = targets.find(item => item.button === event.currentTarget);
      if (target) send(target);
    }
    function onPointerMove(event) {
      if (!canAnimate() || event.pointerType === 'touch') return;
      const rect = root.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      pointer = {
        x: Math.max(-1, Math.min(1, (event.clientX - rect.left) / rect.width * 2 - 1)),
        y: Math.max(-1, Math.min(1, (event.clientY - rect.top) / rect.height * 2 - 1)),
      };
    }
    function onPointerLeave() {pointer = {x: 0, y: 0};}
    function onMotionChange(event) {
      if (typeof event.detail?.canAnimate !== 'boolean') return;
      permitted = event.detail.canAnimate;
      syncMotion();
    }
    function onMediaChange() {syncMotion();}
    function onVisibilityChange() {syncMotion();}

    const tickPaths = [];
    for (let index = 0; index < 40; index += 1) {
      const angle = index / 40 * TAU;
      const inside = ellipsePoint(angle, 324, 187, -.17);
      const outside = ellipsePoint(angle, 332, 193, -.17);
      tickPaths.push(`M${inside.x.toFixed(2)} ${inside.y.toFixed(2)}L${outside.x.toFixed(2)} ${outside.y.toFixed(2)}`);
    }
    ticks.setAttribute('d', tickPaths.join(' '));
    source.addEventListener('click', onSourceClick);
    targets.forEach(target => target.button.addEventListener('click', onTargetClick));
    root.addEventListener('pointermove', onPointerMove, {passive: true});
    root.addEventListener('pointerleave', onPointerLeave, {passive: true});
    document.addEventListener('grok:motion-change', onMotionChange);
    document.addEventListener('visibilitychange', onVisibilityChange);
    if (media.addEventListener) media.addEventListener('change', onMediaChange);

    const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
      visible = entries.some(entry => entry.isIntersecting);
      syncMotion();
    }, {threshold: .01}) : null;
    if (observer) observer.observe(root);

    updateSelection();
    status.textContent = 'Light selected. This is a local illustration with simulated destinations, without a Grok Bot or hardware connection.';
    render();

    const api = {
      setActive(value) {
        if (destroyed) return;
        active = Boolean(value);
        root.hidden = !active;
        if (active) render();
        syncMotion();
      },
      destroy() {
        if (destroyed) return;
        destroyed = true;
        if (frame) cancelAnimationFrame(frame);
        if (observer) observer.disconnect();
        source.removeEventListener('click', onSourceClick);
        targets.forEach(target => target.button.removeEventListener('click', onTargetClick));
        root.removeEventListener('pointermove', onPointerMove);
        root.removeEventListener('pointerleave', onPointerLeave);
        document.removeEventListener('grok:motion-change', onMotionChange);
        document.removeEventListener('visibilitychange', onVisibilityChange);
        if (media.removeEventListener) media.removeEventListener('change', onMediaChange);
        root.remove();
        instances.delete(container);
      },
    };
    instances.set(container, api);
    return api;
  }

  window.GrokSignalScene = {mount};
})();
