/* Proposed hardware routes, illustrated locally. No Grok or device calls. */
(() => {
  'use strict';

  const NS = 'http://www.w3.org/2000/svg';
  const mounted = new WeakMap();
  const platforms = [
    {
      id: 'esp32', label: 'C124 · ESP32', x: 165, y: 275,
      title: 'C124 · RGB light + button', href: 'esp32.html',
      route: 'Gateway + USB · proposed HTTPS',
      description: 'C124 LED and button example. Proposed route: Grok Bot, operator HTTPS, gateway, host USB bridge, ESP32 firmware. Firmware compiles; physical C124 and Grok Bot tests are pending.',
      port: 'Gateway', portX: 302, portY: 308,
      points: [[430, 275], [350, 275], [255, 275], [165, 275]],
    },
    {
      id: 'linux', label: 'Raspberry Pi', x: 825, y: 145,
      title: 'Linux · custom Python gadgets', href: 'linux.html',
      route: 'Gateway + Python · proposed HTTPS',
      description: 'Declare custom capabilities with the Linux Python SDK. Proposed route: Grok Bot, operator HTTPS, gateway, Linux gadget agent. Software is checked; Raspberry Pi hardware and Grok Bot tests are pending.',
      port: 'Gateway', portX: 675, portY: 127,
      points: [[556, 227], [647, 197], [702, 145], [825, 145]],
    },
    {
      id: 'home', label: 'Home Assistant', x: 810, y: 385,
      title: 'Home Assistant · exposed entities', href: 'home-assistant.html',
      route: 'Own MCP server · proposed HTTPS',
      description: 'Use entities exposed by Home Assistant through its own MCP server. The proposed Grok Bot route uses the Home Assistant operator endpoint, independently of the Grok Gadgets gateway. Discovery is checked against fixtures; a real home and Grok Bot tests are pending.',
      port: 'Own MCP', portX: 665, portY: 332,
      points: [[566, 308], [646, 331], [697, 385], [810, 385]],
    },
  ];

  function svgElement(name, attributes, parent) {
    const element = document.createElementNS(NS, name);
    Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, String(value)));
    parent.appendChild(element);
    return element;
  }

  function hardwareIcon(kind, parent) {
    const svg = svgElement('svg', {
      class: 'signal-device-icon', viewBox: '0 0 100 100', 'aria-hidden': 'true', focusable: 'false',
    }, parent);
    const line = attributes => svgElement('path', attributes, svg);
    if (kind === 'esp32') {
      svgElement('rect', {x: 17, y: 10, width: 66, height: 77, rx: 8}, svg);
      svgElement('rect', {x: 28, y: 20, width: 44, height: 44, rx: 4}, svg);
      line({d: 'M29 73h15m12 0h15M38 87v5h24v-5M21 17h2m54 0h2M21 80h2m54 0h2'});
      return svgElement('circle', {class: 'signal-device-indicator', cx: 50, cy: 42, r: 9}, svg);
    }
    if (kind === 'linux') {
      svgElement('rect', {x: 7, y: 17, width: 85, height: 66, rx: 5}, svg);
      svgElement('rect', {x: 34, y: 34, width: 27, height: 27, rx: 1}, svg);
      line({d: 'M78 20h17v23H78zM78 49h17v23H78zM6 58h20v20H6zM29 83v8h17v-8M30 34h-5m5 8h-5m5 8h-5m5 8h-5M65 35h5m-5 9h5m-5 9h5m-5 8h5'});
      for (let x = 18; x < 72; x += 8) {
        svgElement('circle', {cx: x, cy: 23, r: 1.2}, svg);
        svgElement('circle', {cx: x, cy: 28, r: 1.2}, svg);
      }
      return svgElement('circle', {class: 'signal-device-indicator', cx: 69, cy: 75, r: 3.5}, svg);
    }
    line({d: 'M10 44 50 10l40 34M18 38v49h64V38M50 50v16M50 66H33m17 0h17'});
    svgElement('circle', {cx: 33, cy: 68, r: 6}, svg);
    svgElement('circle', {cx: 67, cy: 68, r: 6}, svg);
    return svgElement('circle', {class: 'signal-device-indicator', cx: 50, cy: 44, r: 8}, svg);
  }

  function pointOnRoute(points, progress) {
    const rest = 1 - progress;
    return [0, 1].map(axis => rest ** 3 * points[0][axis]
      + 3 * rest ** 2 * progress * points[1][axis]
      + 3 * rest * progress ** 2 * points[2][axis]
      + progress ** 3 * points[3][axis]);
  }

  function mount(container) {
    if (!(container instanceof Element)) throw new TypeError('Signal scene needs a container element.');
    if (mounted.has(container)) return mounted.get(container);
    const root = document.createElement('section');
    root.className = 'signal-scene';
    root.setAttribute('aria-label', 'Proposed hardware connections for your Grok Bot');
    root.hidden = true;
    root.dataset.frame = '0';
    root.dataset.phase = '0';

    const canvas = svgElement('svg', {
      class: 'signal-canvas', viewBox: '0 0 1000 700', 'aria-hidden': 'true', focusable: 'false',
    }, root);
    const wires = svgElement('g', {class: 'signal-wires'}, canvas);
    const packet = svgElement('circle', {class: 'signal-packet', r: 4, opacity: 0}, canvas);
    const trail = Array.from({length: 5}, (_, index) => svgElement('circle', {
      class: 'signal-trail', r: 1.7 + index * .35, opacity: 0,
    }, canvas));

    const bot = document.createElement('button');
    bot.type = 'button';
    bot.className = 'signal-bot';
    bot.innerHTML = '<img src="media/grok-bot-mark.svg" alt="" width="172" height="172"><span>Grok Bot</span>';
    root.appendChild(bot);

    const destinations = platforms.map(platform => {
      const [a, b, c, d] = platform.points;
      const wire = svgElement('path', {
        d: `M${a.join(' ')} C${b.join(' ')} ${c.join(' ')} ${d.join(' ')}`,
        class: 'signal-wire',
      }, wires);
      const port = document.createElement('span');
      port.className = 'signal-port';
      port.textContent = platform.port;
      port.style.left = `${platform.portX / 10}%`;
      port.style.top = `${platform.portY / 7}%`;
      port.setAttribute('aria-hidden', 'true');
      root.appendChild(port);
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'signal-device';
      button.dataset.signalTarget = platform.id;
      button.style.left = `${platform.x / 10}%`;
      button.style.top = `${platform.y / 7}%`;
      button.setAttribute('aria-label', `Explore ${platform.label}. Replay its conceptual command and state route.`);
      button.setAttribute('aria-pressed', 'false');
      const indicator = hardwareIcon(platform.id, button);
      const label = document.createElement('span');
      label.className = 'signal-device-name';
      label.textContent = platform.label;
      button.appendChild(label);
      root.appendChild(button);
      return {...platform, wire, port, button, indicator};
    });

    const detail = document.createElement('div');
    detail.className = 'signal-detail';
    detail.innerHTML = '<a class="signal-detail-link"><span></span><span aria-hidden="true">↗</span></a><p class="signal-detail-route"></p><div class="signal-evidence"><span>Bot + hardware pending</span><span class="signal-phase">Conceptual</span></div>';
    root.appendChild(detail);
    const detailLink = detail.querySelector('.signal-detail-link');
    const detailTitle = detailLink.firstElementChild;
    const detailRoute = detail.querySelector('.signal-detail-route');
    const phaseLabel = detail.querySelector('.signal-phase');
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
    let selected = destinations[0];
    let sequence = null;
    let instantResponse = false;
    let raf = 0;
    let frame = 0;
    let lastTime = null;
    let lastDraw = 0;

    function canAnimate() {
      return active && visible && permitted && !media.matches && !document.hidden && !destroyed;
    }

    function render() {
      if (destroyed) return;
      packet.setAttribute('opacity', 0);
      trail.forEach(dot => dot.setAttribute('opacity', 0));
      const time = sequence === null ? -1 : sequence % 6;
      const responding = instantResponse || time >= 1.4;
      destinations.forEach(destination => {
        destination.indicator.classList.toggle('is-lit', destination === selected && responding);
      });
      let label = 'Conceptual';
      if (time >= 0 && time < 3.5) {
        const returning = time >= 2.1;
        const travelling = time < 1.4 || returning;
        const progress = returning ? (time - 2.1) / 1.4 : Math.min(1, time / 1.4);
        label = returning ? 'State returns' : 'Command out';
        if (travelling) {
          const position = pointOnRoute(selected.points, returning ? 1 - progress : progress);
          packet.setAttribute('cx', position[0]);
          packet.setAttribute('cy', position[1]);
          packet.setAttribute('opacity', 1);
          trail.forEach((dot, index) => {
            const distance = (trail.length - index) * .032;
            if (progress < distance) return;
            const p = pointOnRoute(selected.points, returning ? 1 - progress + distance : progress - distance);
            dot.setAttribute('cx', p[0]);
            dot.setAttribute('cy', p[1]);
            dot.setAttribute('opacity', .1 + index * .08);
          });
        }
      }
      phaseLabel.textContent = label;
      root.dataset.frame = String(++frame);
      root.dataset.phase = sequence === null ? '0' : sequence.toFixed(3);
    }

    function select(destination, replay = true) {
      selected = destination;
      destinations.forEach(item => {
        const isSelected = item === selected;
        item.button.setAttribute('aria-pressed', String(isSelected));
        item.wire.classList.toggle('is-selected', isSelected);
        item.port.classList.toggle('is-selected', isSelected);
      });
      detailTitle.textContent = selected.title;
      detailLink.href = selected.href;
      detailRoute.textContent = selected.route;
      bot.setAttribute('aria-label', `Grok Bot. Replay the conceptual ${selected.label} route. Bot connection is pending.`);
      status.textContent = selected.description;
      if (replay) {
        sequence = canAnimate() ? 0 : null;
        instantResponse = !canAnimate();
      }
      render();
    }

    function tick(time) {
      raf = 0;
      if (!canAnimate()) {lastTime = null; return;}
      if (sequence === null) sequence = 0;
      if (lastTime !== null) sequence += Math.min((time - lastTime) / 1000, .08);
      lastTime = time;
      if (time - lastDraw >= 32) {render(); lastDraw = time;}
      raf = requestAnimationFrame(tick);
    }

    function syncMotion() {
      if (raf) cancelAnimationFrame(raf);
      raf = 0;
      lastTime = null;
      if (canAnimate()) {
        instantResponse = false;
        raf = requestAnimationFrame(tick);
      }
    }
    function onBotClick() {if (active && !destroyed) select(selected);}
    function onDeviceClick(event) {
      if (!active || destroyed) return;
      const destination = destinations.find(item => item.button === event.currentTarget);
      if (destination) select(destination);
    }
    function onMotionChange(event) {
      if (typeof event.detail?.canAnimate === 'boolean') permitted = event.detail.canAnimate;
      syncMotion();
    }

    bot.addEventListener('click', onBotClick);
    destinations.forEach(item => item.button.addEventListener('click', onDeviceClick));
    document.addEventListener('grok:motion-change', onMotionChange);
    document.addEventListener('visibilitychange', syncMotion);
    media.addEventListener('change', syncMotion);
    const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
      visible = entries.some(entry => entry.isIntersecting);
      syncMotion();
    }, {threshold: .01}) : null;
    observer?.observe(root);
    select(selected, false);

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
        if (raf) cancelAnimationFrame(raf);
        observer?.disconnect();
        bot.removeEventListener('click', onBotClick);
        destinations.forEach(item => item.button.removeEventListener('click', onDeviceClick));
        document.removeEventListener('grok:motion-change', onMotionChange);
        document.removeEventListener('visibilitychange', syncMotion);
        media.removeEventListener('change', syncMotion);
        root.remove();
        mounted.delete(container);
      },
    };
    mounted.set(container, api);
    return api;
  }

  window.GrokSignalScene = Object.freeze({mount});
})();
