(() => {
 const dropdowns = [...document.querySelectorAll('.teaching-dropdown')];
 if (!dropdowns.length) return;
 dropdowns.forEach(dropdown => {
  dropdown.addEventListener('toggle', () => {
   if (dropdown.open) dropdowns.forEach(other => { if (other !== dropdown) other.open = false; });
  });
 });
 document.addEventListener('click', event => {
  dropdowns.forEach(dropdown => { if (!dropdown.contains(event.target)) dropdown.open = false; });
 });
 document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  const nested = document.querySelector('.course-level-dropdown[open]');
  if (nested && nested.contains(document.activeElement)) { nested.open = false; nested.querySelector('summary').focus(); event.stopImmediatePropagation(); return; }
  const dropdown = dropdowns.find(item => item.open && item.contains(document.activeElement)) || dropdowns.find(item => item.open);
  if (dropdown) { dropdown.open = false; dropdown.querySelector('summary').focus(); event.stopImmediatePropagation(); }
 }, true);
 const mainToggle = document.querySelector('.nav-toggle');
 if (mainToggle) mainToggle.addEventListener('click', () => {
  if (mainToggle.getAttribute('aria-expanded') === 'false') dropdowns.forEach(dropdown => { dropdown.open = false; });
 });
})();
