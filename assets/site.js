
const search = document.getElementById('publication-search');
const year = document.getElementById('publication-year');
if (search && year) {
  const entries = [...document.querySelectorAll('.publications li')];
  const filter = () => {
    const query = search.value.trim().toLowerCase();
    let count = 0;
    entries.forEach(entry => {
      entry.hidden = !(entry.textContent.toLowerCase().includes(query) && (!year.value || entry.dataset.year === year.value));
      if (!entry.hidden) count++;
    });
    document.getElementById('publication-count').textContent = `${count} of ${entries.length} journal entries shown`;
  };
  search.addEventListener('input', filter);
  year.addEventListener('change', filter);
}
