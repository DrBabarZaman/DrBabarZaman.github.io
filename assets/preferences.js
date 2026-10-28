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

// London civil time automatically follows GMT and British Summer Time.
(() => {
  const startClock = () => {
    const clock = document.getElementById('london-datetime');
    const zone = document.getElementById('london-zone');
    if (!clock || !zone) return;
    const format = new Intl.DateTimeFormat('en-GB', {timeZone:'Europe/London', weekday:'short', day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit', second:'2-digit', hourCycle:'h23'});
    const zoneFormat = new Intl.DateTimeFormat('en-GB', {timeZone:'Europe/London', timeZoneName:'short'});
    const tick = () => {
      const now = new Date();
      clock.textContent = format.format(now);
      clock.dateTime = now.toISOString();
      zone.textContent = zoneFormat.formatToParts(now).find(part => part.type === 'timeZoneName').value;
    };
    tick();
    setInterval(tick, 1000);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', startClock); else startClock();
})();
