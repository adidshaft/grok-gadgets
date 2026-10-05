// Native details keep navigation usable without JavaScript.
(() => {
  const menu = document.querySelector('.doc-menu');
  if (!menu) return;
  const narrow = matchMedia('(max-width: 850px)');
  const update = () => { menu.open = !narrow.matches; };
  update();
  narrow.addEventListener('change', update);
})();
