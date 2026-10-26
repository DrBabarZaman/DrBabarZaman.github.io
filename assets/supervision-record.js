(() => {
 const search = document.getElementById('student-search');
 const degree = document.getElementById('student-degree');
 const year = document.getElementById('student-year');
 const university = document.getElementById('student-university');
 if (!search || !degree || !year || !university) return;
 const rows = [...document.querySelectorAll('[data-student-row]')];
 const normalize = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
 const filter = () => {
  const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
  let count = 0;
  rows.forEach(row => {
   const text = normalize(row.textContent);
   const match = terms.every(term => text.includes(term)) && (!degree.value || row.dataset.degree === degree.value) && (!year.value || row.dataset.year === year.value) && (!university.value || row.dataset.university === university.value);
   row.hidden = !match;
   if (match) count++;
  });
  document.getElementById('student-result-count').textContent = `Showing ${count} of ${rows.length} students`;
  document.getElementById('student-empty').hidden = count !== 0;
 };
 search.addEventListener('input', filter);
 [degree, year, university].forEach(control => control.addEventListener('change', filter));
 document.getElementById('student-reset').addEventListener('click', () => {
  search.value = ''; degree.value = ''; year.value = ''; university.value = '';
  filter(); search.focus();
 });
 filter();
})();
