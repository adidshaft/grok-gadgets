/* One motion controller preserves user pause across system and page lifecycle changes. */
(() => {
  const toggle = document.querySelector('#motion-toggle');
  const menu = document.querySelector('#site-menu');
  const open = document.querySelector('#menu-open');
  const close = document.querySelector('#menu-close');
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  let userPaused = false;

  const update = () => {
    const systemReduced = media.matches;
    const menuOpen = menu.open || Boolean(document.querySelector('#scene-inspector')?.open);
    const canAnimate = !userPaused && !systemReduced && !document.hidden && !menuOpen;
    document.documentElement.toggleAttribute('data-reduced-motion', !canAnimate);
    document.body.toggleAttribute('data-reduced-motion', !canAnimate);
    toggle.setAttribute('aria-pressed', String(userPaused));
    toggle.disabled = systemReduced;
    toggle.title = systemReduced ? 'Motion is reduced by your system setting' : '';
    toggle.innerHTML = systemReduced ? 'Reduced motion <span>[OS]</span>' : userPaused ? 'Resume motion <span>[▶]</span>' : 'Pause motion <span>[Ⅱ]</span>';
    document.dispatchEvent(new CustomEvent('grok:motion-change', {detail:{canAnimate, userPaused, systemReduced, menuOpen}}));
  };
  const openMenu = () => { if (!menu.open) { menu.showModal(); document.body.classList.add('menu-is-open'); update(); } };
  const closeMenu = () => menu.close();
  toggle.addEventListener('click', () => { if (!media.matches) { userPaused = !userPaused; update(); } });
  media.addEventListener('change', update);
  open.addEventListener('click', openMenu);
  close.addEventListener('click', closeMenu);
  menu.addEventListener('close', () => { document.body.classList.remove('menu-is-open'); update(); open.focus(); });
  menu.addEventListener('click', (event) => {
    if (event.target !== menu) return;
    const bounds = menu.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) closeMenu();
  });
  document.addEventListener('visibilitychange', update);
  document.addEventListener('grok:panel-change', update);
  update();
})();
