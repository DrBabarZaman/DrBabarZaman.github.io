const filterGroup = document.querySelector('.material-filters');
const materialCards = [...document.querySelectorAll('.material-card[data-category]')];
if (filterGroup && materialCards.length) {
  const buttons = [...filterGroup.querySelectorAll('[data-material-filter]')];
  const status = document.getElementById('material-filter-status');
  const categories = ['all', ...materialCards.map(card => card.dataset.category)];
  const filterMaterials = category => {
    if (!categories.includes(category)) return;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.materialFilter === category)));
    materialCards.forEach(card => { card.hidden = category !== 'all' && card.dataset.category !== category; });
    if (status) status.textContent = category === 'all' ? 'Showing all three material categories.' : `Showing ${category === 'data' ? 'data materials' : category === 'labs' ? 'lab materials' : 'lecture materials'}.`;
  };
  filterGroup.hidden = false;
  filterGroup.addEventListener('click', event => {
    const button = event.target.closest('[data-material-filter]');
    if (button) filterMaterials(button.dataset.materialFilter);
  });
  if (categories.includes(location.hash.slice(1))) filterMaterials(location.hash.slice(1));
}
