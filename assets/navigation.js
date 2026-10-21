const menuButton = document.querySelector('.nav-toggle');
const menu = document.getElementById('main-nav');
if (menuButton && menu) {
  menuButton.hidden = false;
  document.documentElement.classList.add('nav-ready');
  const closeMenu = () => { menuButton.setAttribute('aria-expanded', 'false'); menu.classList.remove('is-open'); };
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open)); menu.classList.toggle('is-open', open);
  });
  menu.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.classList.contains('is-open')) { closeMenu(); menuButton.focus(); } });
  document.addEventListener('click', e => { if (!e.target.closest('.header-inner')) closeMenu(); });
}
