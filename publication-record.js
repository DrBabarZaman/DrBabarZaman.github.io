(() => {
 const search = document.getElementById('publication-search');
 const year = document.getElementById('publication-year');
 const area = document.getElementById('publication-area');
 const type = document.getElementById('publication-type');
 const publisher = document.getElementById('publication-publisher');
 const journal = document.getElementById('publication-journal');
 if (!search || !year || !area || !type || !publisher || !journal) return;
 const journalOptions = [...journal.options].map(option => option.cloneNode(true));
 const syncJournals = () => {
  const previous = journal.value;
  const available = journalOptions.filter(option => !option.value || !publisher.value || option.dataset.publisher === publisher.value);
  journal.replaceChildren(...available.map(option => option.cloneNode(true)));
  journal.value = available.some(option => option.value === previous) ? previous : '';
 };
 const entries = [...document.querySelectorAll('.publication-year-group .publication-entry')];
 const groups = [...document.querySelectorAll('.publication-year-group')];
 const normalize = text => text.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
 const eligible = entry => ['article', 'review'].includes(entry.dataset.type);
 const filter = () => {
  const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
  let count = 0;
  entries.forEach(entry => {
   const text = normalize(entry.textContent);
   const matchType = !type.value || (type.value === 'published' ? entry.dataset.type !== 'manuscript' : type.value === 'eligible' ? eligible(entry) : entry.dataset.type === type.value);
   const show = terms.every(term => text.includes(term)) && (!year.value || entry.dataset.year === year.value) && (!area.value || entry.dataset.area.split(' ').includes(area.value)) && (!publisher.value || entry.dataset.publisher === publisher.value) && (!journal.value || entry.dataset.journal === journal.value) && matchType;
   entry.hidden = !show;
   if (show) count++;
  });
  groups.forEach(group => { group.hidden = ![...group.querySelectorAll('.publication-entry')].some(entry => !entry.hidden); });
  const scope = type.value === 'published' ? 'published-record entries' : type.value === 'eligible' ? 'eligible papers' : type.value === 'manuscript' ? 'manuscripts' : 'outputs';
  const total = type.value === 'published' ? entries.filter(e => e.dataset.type !== 'manuscript').length : type.value === 'eligible' ? entries.filter(eligible).length : type.value ? entries.filter(e => e.dataset.type === type.value).length : entries.length;
  document.getElementById('publication-count').textContent = `Showing ${count} of ${total} ${scope}`;
  document.getElementById('publication-empty').hidden = count !== 0;
 };
 search.addEventListener('input', filter);
 [year, area, type, journal].forEach(control => control.addEventListener('change', filter));
 publisher.addEventListener('change', () => { syncJournals(); filter(); });
 document.getElementById('publication-reset').addEventListener('click', () => {
  search.value = ''; year.value = ''; area.value = ''; publisher.value = ''; journal.value = ''; syncJournals(); type.value = 'published'; filter(); search.focus();
 });
 document.querySelectorAll('.journal-paper-count').forEach(link => link.addEventListener('click', event => {
  event.preventDefault();
  search.value = ''; year.value = ''; area.value = ''; type.value = 'eligible';
  publisher.value = link.dataset.filterPublisher; journal.value = ''; syncJournals(); journal.value = link.dataset.filterJournal;
  filter();
  search.focus({preventScroll: true});
  document.getElementById('publication-list').scrollIntoView({block: 'start', behavior: 'instant'});
 }));
 // Open methodological details when their anchor is followed.
 const revealSources = () => {
  if (window.location.hash === '#journal-summary-title') document.getElementById('journal-summary-title').open = true;
 };
 window.addEventListener('hashchange', revealSources);
 revealSources();
 filter();
})();
