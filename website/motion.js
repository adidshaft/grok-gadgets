// Content is visible without JavaScript; OS and explicit user preference supported.
const toggle = document.querySelector('#motion-toggle');
const systemReduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
let reduced = systemReduced;
function updateMotion() {
  document.body.toggleAttribute('data-reduced-motion', reduced);
  toggle.setAttribute('aria-pressed', String(reduced));
  document.querySelector('main').classList.toggle('reveal', !reduced);
}
toggle.addEventListener('click', () => { reduced = !reduced; updateMotion(); });
updateMotion();
