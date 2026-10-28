(() => {
 const header = document.querySelector('.site-header');
 if (!header) return;
 const update = () => document.documentElement.style.setProperty('--site-header-height', `${Math.ceil(header.getBoundingClientRect().height)}px`);
 update();
 if (window.ResizeObserver) new ResizeObserver(update).observe(header);
 else window.addEventListener('resize', update);
 if (document.fonts && document.fonts.ready) document.fonts.ready.then(update);
 // Correct an initial deep-link position once the actual header height is known.
 if (window.location.hash) requestAnimationFrame(() => {
  let target;
  try { target = document.getElementById(decodeURIComponent(window.location.hash.slice(1))); } catch (_) { return; }
  if (target) target.scrollIntoView({ block: 'start', behavior: 'instant' });
 });
})();
