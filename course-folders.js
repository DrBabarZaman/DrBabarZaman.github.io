(() => {
 // Direct links such as #data reveal that category; ordinary visits start collapsed.
 const revealHash = () => {
  const id = window.location.hash.slice(1);
  if (!['lectures', 'labs', 'data'].includes(id)) return;
  const section = document.getElementById(id);
  if (section && section.matches('.course-material-disclosure')) section.open = true;
 };
 revealHash();
 window.addEventListener('hashchange', revealHash);
})();
