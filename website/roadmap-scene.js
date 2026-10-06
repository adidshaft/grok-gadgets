/* A conceptual roadmap. Evidence levels come from docs/public/support-matrix.md,
 * docs/getting-started/physical-test.md and the independent software milestone.
 * The full roadmap page retains the authoritative, timestamped issue snapshot. */
(() => {
  'use strict';

  const SVG_NS = 'http://www.w3.org/2000/svg';
  const mounted = new WeakMap();
  let mountId = 0;

  const milestones = [
    {
      name: 'Local software', label: 'Software', status: 'Checked', evidence: 'checked',
      detail: 'Gateway and SDK software checked. C124 firmware compiles.',
      href: 'doc-docs-public-support-matrix.html', linkLabel: 'Read the software status', t: .07,
    },
    {
      name: 'Public source', label: 'Source', status: 'Published', evidence: 'checked',
      detail: 'Five open-source repositories. A local simulator ready to try.',
      href: 'components.html', linkLabel: 'Explore the source repositories', t: .285,
    },
    {
      name: 'Grok Bot', label: 'Grok Bot', status: 'Pending', evidence: 'pending',
      detail: 'Connect your existing Grok Bot. Native tool calls need evidence.',
      href: 'doc-docs-getting-started-hosting.html', linkLabel: 'Read about the Grok Bot connection', t: .5,
    },
    {
      name: 'C124 hardware', label: 'Hardware', status: 'Pending', evidence: 'pending',
      detail: 'Flash a C124. Observe its LED, button and USB recovery.',
      href: 'doc-docs-getting-started-physical-test.html', linkLabel: 'Read the physical test procedure', t: .715,
    },
    {
      name: 'Independent setup', label: 'Reproduce', status: 'Needs testers', evidence: 'open',
      detail: 'Help another person reproduce the software setup.',
      href: 'contribute.html', linkLabel: 'Find a way to contribute', t: .93,
    },
  ];

  function svgElement(name, attributes, parent) {
    const element = document.createElementNS(SVG_NS, name);
    Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, String(value)));
    if (parent) parent.append(element);
    return element;
  }

  function point(t, side = 0, depth = 0) {
    const angle = t * Math.PI * 2 - .55;
    const tangentY = 95 * Math.PI * 2 * Math.cos(angle);
    const length = Math.hypot(790, tangentY);
    return {
      x: 105 + 790 * t - (tangentY / length) * side,
      y: 235 + 95 * Math.sin(angle) + (790 / length) * side + depth,
    };
  }

  function pathFor(from, to, side = 0, depth = 0, steps = 80) {
    const points = [];
    for (let index = 0; index <= steps; index += 1) {
      const p = point(from + ((to - from) * index) / steps, side, depth);
      points.push(`${index ? 'L' : 'M'}${p.x.toFixed(2)} ${p.y.toFixed(2)}`);
    }
    return points.join(' ');
  }

  function mount(container) {
    if (!(container instanceof Element)) throw new TypeError('A roadmap container is required.');
    mounted.get(container)?.destroy();

    const detailId = `roadmap-detail-${++mountId}`;
    const instructionsId = `roadmap-instructions-${mountId}`;
    const root = document.createElement('section');
    root.className = 'roadmap-scene';
    root.setAttribute('aria-label', 'Project roadmap');
    root.setAttribute('aria-hidden', 'true');
    root.inert = true;
    root.dataset.active = 'false';
    root.dataset.frame = '0';
    root.dataset.phase = '0.000';
    root.innerHTML = `
      <div class="roadmap-heading" aria-hidden="true">
        <span>From software to real devices</span>
        <span class="roadmap-position">01 / 05</span>
      </div>
      <div class="roadmap-visual">
        <svg class="roadmap-wire" viewBox="0 0 1000 470" preserveAspectRatio="none" aria-hidden="true" focusable="false">
          <g class="roadmap-construction"></g>
          <g class="roadmap-ribbon"></g>
          <g class="roadmap-markers"></g>
          <g class="roadmap-inspection">
            <path class="roadmap-inspection-shadow"></path>
            <path class="roadmap-inspection-ring"></path>
            <path class="roadmap-inspection-cross"></path>
          </g>
        </svg>
        <div class="roadmap-stations" role="group" aria-label="Choose a milestone" aria-describedby="${instructionsId}"></div>
      </div>
      <div class="roadmap-detail" id="${detailId}" aria-live="polite" aria-atomic="true">
        <div class="roadmap-detail-heading">
          <a class="roadmap-detail-link"><span class="roadmap-detail-name"></span><span aria-hidden="true">↗</span></a>
          <span class="roadmap-status"></span>
        </div>
        <p class="roadmap-description"></p>
      </div>
      <p class="roadmap-instructions" id="${instructionsId}">Select a milestone. Use arrow keys to move between points.</p>`;
    container.append(root);

    const visual = root.querySelector('.roadmap-visual');
    const construction = root.querySelector('.roadmap-construction');
    const ribbon = root.querySelector('.roadmap-ribbon');
    const markers = root.querySelector('.roadmap-markers');
    const stationLayer = root.querySelector('.roadmap-stations');
    const inspection = root.querySelector('.roadmap-inspection');
    const ring = root.querySelector('.roadmap-inspection-ring');
    const ringShadow = root.querySelector('.roadmap-inspection-shadow');
    const cross = root.querySelector('.roadmap-inspection-cross');
    const detailName = root.querySelector('.roadmap-detail-name');
    const detailLink = root.querySelector('.roadmap-detail-link');
    const status = root.querySelector('.roadmap-status');
    const description = root.querySelector('.roadmap-description');
    const position = root.querySelector('.roadmap-position');

    // A light construction baseline and its two end marks give the ribbon scale.
    svgElement('path', {d: 'M88 408H910 M88 401V415 M910 401V415'}, construction);
    for (let index = 1; index < 20; index += 1) {
      const x = 88 + (822 * index) / 20;
      svgElement('path', {d: `M${x} 405V411`}, construction);
    }

    [-48, 48].forEach(side => {
      svgElement('path', {d: pathFor(0, 1, side, 22), class: 'roadmap-lower-rail'}, ribbon);
      svgElement('path', {d: pathFor(0, 1, side), class: 'roadmap-upper-rail'}, ribbon);
      svgElement('path', {d: pathFor(.025, .285, side), class: 'roadmap-checked-rail'}, ribbon);
    });

    for (let index = 0; index <= 52; index += 1) {
      const t = index / 52;
      const left = point(t, -48);
      const right = point(t, 48);
      svgElement('path', {
        d: `M${left.x} ${left.y}L${right.x} ${right.y}`,
        class: index % 4 ? 'roadmap-rib' : 'roadmap-rib roadmap-major-rib',
      }, ribbon);
      if (index % 4 === 0) {
        svgElement('path', {
          d: `M${left.x} ${left.y}v22M${right.x} ${right.y}v22`,
          class: 'roadmap-edge',
        }, ribbon);
      }
    }
    svgElement('path', {d: pathFor(0, 1), class: 'roadmap-centerline'}, ribbon);

    const buttons = milestones.map((milestone, index) => {
      const anchor = point(milestone.t);
      svgElement('ellipse', {
        cx: anchor.x, cy: anchor.y + 3, rx: 28, ry: 11, class: 'roadmap-footprint',
      }, markers);
      svgElement('path', {
        d: `M${anchor.x - 35} ${anchor.y + 3}h-10M${anchor.x + 35} ${anchor.y + 3}h10`,
        class: 'roadmap-marker-tick',
      }, markers);

      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'roadmap-station';
      button.dataset.index = String(index);
      button.dataset.evidence = milestone.evidence;
      button.style.left = `${anchor.x / 10}%`;
      button.style.top = `${(anchor.y / 470) * 100}%`;
      button.setAttribute('aria-controls', detailId);
      button.setAttribute('aria-pressed', 'false');
      button.setAttribute('aria-label', `${index + 1}. ${milestone.name}. ${milestone.status}.`);
      const number = document.createElement('span');
      number.className = 'roadmap-station-number';
      number.setAttribute('aria-hidden', 'true');
      number.textContent = String(index + 1).padStart(2, '0');
      const label = document.createElement('span');
      label.className = 'roadmap-station-label';
      label.setAttribute('aria-hidden', 'true');
      label.textContent = milestone.label;
      button.append(number, label);
      stationLayer.append(button);
      return button;
    });

    const media = window.matchMedia('(prefers-reduced-motion: reduce)');
    let active = false;
    let destroyed = false;
    let visible = true;
    let selected = 0;
    let phase = 0;
    let frame = 0;
    let raf = 0;
    let lastTime = null;
    let lastDraw = 0;
    let motionAllowed = readMotionPreference();
    let cursor = point(milestones[0].t);

    function readMotionPreference() {
      return !media.matches
        && !document.documentElement.hasAttribute('data-reduced-motion')
        && !document.body?.hasAttribute('data-reduced-motion');
    }

    function canAnimate() {
      return active && visible && motionAllowed && !media.matches && !document.hidden && !destroyed;
    }

    function draw(snap = false) {
      const target = point(milestones[selected].t);
      const amount = snap || !canAnimate() ? 1 : .22;
      cursor.x += (target.x - cursor.x) * amount;
      cursor.y += (target.y - cursor.y) * amount;
      // The ring is an inspection cursor, never a changing completion indicator.
      const yaw = .42 + Math.sin(phase * .45) * .24;
      const lean = Math.sin(phase * .32) * 5;
      const near = [];
      const far = [];
      for (let index = 0; index <= 64; index += 1) {
        const angle = (index / 64) * Math.PI * 2;
        const x = Math.cos(angle) * 58 * Math.cos(yaw) + Math.sin(angle) * lean;
        const y = Math.sin(angle) * 57 + Math.cos(angle) * 13 * Math.sin(yaw) - 42;
        const prefix = index ? 'L' : 'M';
        near.push(`${prefix}${x.toFixed(2)} ${y.toFixed(2)}`);
        far.push(`${prefix}${(x + 9).toFixed(2)} ${(y + 4).toFixed(2)}`);
      }
      inspection.setAttribute('transform', `translate(${cursor.x.toFixed(2)} ${cursor.y.toFixed(2)})`);
      ring.setAttribute('d', `${near.join(' ')}Z`);
      ringShadow.setAttribute('d', `${far.join(' ')}Z`);
      const sweep = Math.sin(phase * .7) * 34;
      const halfWidth = Math.sqrt(Math.max(0, 1 - (sweep / 57) ** 2)) * 58 * Math.cos(yaw);
      cross.setAttribute('d', `M${-halfWidth} ${sweep - 42}H${halfWidth}`);
      root.dataset.phase = phase.toFixed(3);
      root.dataset.frame = String(frame);
    }

    function select(index, moveFocus = false) {
      if (destroyed) return;
      selected = (index + milestones.length) % milestones.length;
      const milestone = milestones[selected];
      buttons.forEach((button, buttonIndex) => {
        const isSelected = selected === buttonIndex;
        button.setAttribute('aria-pressed', String(isSelected));
        button.tabIndex = isSelected ? 0 : -1;
      });
      detailName.textContent = milestone.name;
      detailLink.href = milestone.href;
      detailLink.setAttribute('aria-label', `${milestone.name}: ${milestone.linkLabel}`);
      status.textContent = milestone.status;
      status.dataset.evidence = milestone.evidence;
      description.textContent = milestone.detail;
      position.textContent = `${String(selected + 1).padStart(2, '0')} / 05`;
      root.dataset.selected = String(selected + 1);
      draw(!canAnimate());
      if (moveFocus) buttons[selected].focus({preventScroll: true});
    }

    function onClick(event) {
      const button = event.target.closest('.roadmap-station');
      if (button && stationLayer.contains(button)) select(Number(button.dataset.index));
    }

    function onKeydown(event) {
      const button = event.target.closest('.roadmap-station');
      if (!button || !stationLayer.contains(button)) return;
      const index = Number(button.dataset.index);
      let next;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = index + 1;
      else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = index - 1;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = milestones.length - 1;
      else return;
      event.preventDefault();
      select(next, true);
    }

    function tick(time) {
      raf = 0;
      if (!canAnimate()) { lastTime = null; return; }
      if (lastTime !== null) phase += Math.min((time - lastTime) / 1000, .08);
      lastTime = time;
      if (time - lastDraw >= 40) {
        frame += 1;
        draw();
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

    function onMotionChange(event) {
      motionAllowed = typeof event.detail?.canAnimate === 'boolean'
        ? event.detail.canAnimate : readMotionPreference();
      syncMotion();
    }

    function onSystemMotionChange() {
      motionAllowed = readMotionPreference();
      syncMotion();
    }

    stationLayer.addEventListener('click', onClick);
    stationLayer.addEventListener('keydown', onKeydown);
    document.addEventListener('grok:motion-change', onMotionChange);
    document.addEventListener('visibilitychange', syncMotion);
    media.addEventListener('change', onSystemMotionChange);

    const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      syncMotion();
    }, {threshold: .01}) : null;
    observer?.observe(visual);

    const api = {
      setActive(value) {
        if (destroyed) return;
        active = Boolean(value);
        root.dataset.active = String(active);
        root.inert = !active;
        root.setAttribute('aria-hidden', String(!active));
        if (active) draw(true);
        syncMotion();
      },
      destroy() {
        if (destroyed) return;
        destroyed = true;
        syncMotion();
        observer?.disconnect();
        stationLayer.removeEventListener('click', onClick);
        stationLayer.removeEventListener('keydown', onKeydown);
        document.removeEventListener('grok:motion-change', onMotionChange);
        document.removeEventListener('visibilitychange', syncMotion);
        media.removeEventListener('change', onSystemMotionChange);
        root.remove();
        mounted.delete(container);
      },
    };

    select(0);
    mounted.set(container, api);
    return api;
  }

  window.GrokRoadmapScene = Object.freeze({mount});
})();
