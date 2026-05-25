document.addEventListener('DOMContentLoaded', () => {
  const bar = document.querySelector('.profile-sort-bar');
  const grid = document.querySelector('.plaque-grid');
  if (!bar || !grid) return;

  const typeOrder = { ultimate: 0, unique: 1, extra: 2, basic: 3 };
  const buttons = [...bar.querySelectorAll('.profile-sort-btn')];

  const applySort = (mode) => {
    const cards = [...grid.querySelectorAll('article')];
    cards.sort((a, b) => {
      if (mode === 'alpha') {
        return (a.querySelector('.plaque__slug')?.textContent || '').localeCompare(b.querySelector('.plaque__slug')?.textContent || '');
      }
      if (mode === 'type') {
        const t = (typeOrder[a.dataset.type] ?? 99) - (typeOrder[b.dataset.type] ?? 99);
        if (t !== 0) return t;
      }
      return Number(b.dataset.level || 0) - Number(a.dataset.level || 0);
    });

    grid.classList.add('is-sorting');
    cards.forEach((c) => grid.appendChild(c));
    setTimeout(() => grid.classList.remove('is-sorting'), 180);
  };

  buttons.forEach((btn) => btn.addEventListener('click', () => {
    buttons.forEach((b) => b.classList.remove('is-active'));
    btn.classList.add('is-active');
    applySort(btn.dataset.sort || 'rank');
  }));
});
