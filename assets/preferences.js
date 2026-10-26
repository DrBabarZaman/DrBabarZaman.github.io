(() => {
  'use strict';
  const key = 'sil-colour-theme';
  let choice = 'dark';
  try {
    const saved = localStorage.getItem(key);
    if (saved === 'light' || saved === 'dark') choice = saved;
    // Convert a previous System preference once; subsequent OS changes do not affect it.
    else if (saved === 'system') {
      choice = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      localStorage.setItem(key, choice);
    }
  } catch (_) {}
  const apply = () => {
    document.documentElement.dataset.theme = choice;
    const picker = document.getElementById('theme-select');
    if (picker) picker.value = choice;
  };
  apply();
  const start = () => {
    const picker = document.getElementById('theme-select');
    if (picker) picker.addEventListener('change', () => {
      if (picker.value !== 'light' && picker.value !== 'dark') return;
      choice = picker.value;
      try { localStorage.setItem(key, choice); } catch (_) {}
      apply();
    });
    apply();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
