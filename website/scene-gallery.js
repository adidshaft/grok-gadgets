/* Distinct canvas scenes; route stories remain local to the device illustration. */
(() => {
  'use strict';
  const root = document.querySelector('.home-scene');
  if (!root || !window.GrokRoadmapScene || !window.GrokSignalScene) return;
  const nav = root.querySelector('.scene-gallery-nav');
  const buttons = [...nav.querySelectorAll('[data-scene]')];
  const stages = {
    devices: root.querySelector('.scene-stage'),
    signal: root.querySelector('#signal-stage'),
    roadmap: root.querySelector('#roadmap-stage'),
  };
  const scenes = {
    signal: GrokSignalScene.mount(stages.signal),
    roadmap: GrokRoadmapScene.mount(stages.roadmap),
  };
  const stories = root.querySelector('.scene-selector');
  const hint = root.querySelector('.scene-gallery-hint');
  let selected = 'devices';
  function select(name) {
    if (!Object.hasOwn(stages, name)) return;
    selected = name;
    root.dataset.activeScene = name;
    Object.entries(stages).forEach(([key, stage]) => {stage.hidden = key !== name;});
    Object.entries(scenes).forEach(([key, scene]) => scene.setActive(key === name));
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.scene === name)));
    stories.hidden = name !== 'devices';
    hint.hidden = name === 'devices';
    hint.textContent = name === 'roadmap' ? 'Select a milestone to explore' : 'Send a conceptual signal';
    document.dispatchEvent(new CustomEvent('grok:scene-change', {detail: {scene: name}}));
  }
  buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.scene)));
  nav.addEventListener('keydown', event => {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    const focused = event.target.closest('[data-scene]');
    let index = buttons.indexOf(focused);
    if (index < 0) index = buttons.findIndex(button => button.dataset.scene === selected);
    index = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1 : (index + (['ArrowLeft', 'ArrowUp'].includes(event.key) ? -1 : 1) + buttons.length) % buttons.length;
    select(buttons[index].dataset.scene);
    buttons[index].focus();
  });
  root.querySelector('#scene-replay').addEventListener('click', () => select('devices'));
  nav.hidden = false;
  select('devices');
})();
