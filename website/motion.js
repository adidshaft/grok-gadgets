// Preference controls animation; the interactive illustration remains operable when paused.
(() => {
  const toggle = document.querySelector('#motion-toggle');
  const menu = document.querySelector('#site-menu');
  const open = document.querySelector('#menu-open');
  const close = document.querySelector('#menu-close');
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  let manual = null;
  const preference = () => manual === null ? media.matches : manual;
  const update = () => {
    const reduced = preference() || menu.open;
    document.documentElement.toggleAttribute('data-reduced-motion', reduced);
    document.body.toggleAttribute('data-reduced-motion', reduced);
    toggle.setAttribute('aria-pressed', String(preference()));
    toggle.innerHTML = preference() ? 'Resume motion <span>[▶]</span>' : 'Pause motion <span>[Ⅱ]</span>';
    document.dispatchEvent(new CustomEvent('grok:motion-change', {detail:{reduced}}));
  };
  const openMenu = () => { if (!menu.open) { menu.showModal(); document.body.classList.add('menu-is-open'); update(); } };
  const closeMenu = () => menu.close();
  toggle.addEventListener('click', () => { manual = !preference(); update(); });
  media.addEventListener('change', update);
  open.addEventListener('click', openMenu);
  close.addEventListener('click', closeMenu);
  menu.addEventListener('close', () => { document.body.classList.remove('menu-is-open'); update(); open.focus(); });
  menu.addEventListener('click', (event) => {
    if (event.target !== menu) return;
    const bounds = menu.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) closeMenu();
  });
  update();
})();
