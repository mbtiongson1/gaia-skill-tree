/* profile-sort.js — sort bar for the Named Skills plaque grid.
 * Reads data-level / data-type / data-skill-id from plaque articles.
 * No dependencies beyond DOM.
 */
(function () {
  var TYPE_ORDER = { ultimate: 0, unique: 1, extra: 2, basic: 3 };

  function sortPlaques(grid, mode) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.plaque'));
    cards.sort(function (a, b) {
      if (mode === 'rank') {
        var diff = parseInt(b.dataset.level || 0, 10) - parseInt(a.dataset.level || 0, 10);
        if (diff !== 0) return diff;
        return (a.dataset.skillId || '').localeCompare(b.dataset.skillId || '');
      }
      if (mode === 'alpha') {
        var aName = (a.querySelector('.plaque__title') || {}).textContent || a.dataset.skillId || '';
        var bName = (b.querySelector('.plaque__title') || {}).textContent || b.dataset.skillId || '';
        return aName.toLowerCase().localeCompare(bName.toLowerCase());
      }
      if (mode === 'type') {
        var aT = TYPE_ORDER[a.dataset.type] !== undefined ? TYPE_ORDER[a.dataset.type] : 99;
        var bT = TYPE_ORDER[b.dataset.type] !== undefined ? TYPE_ORDER[b.dataset.type] : 99;
        if (aT !== bT) return aT - bT;
        return parseInt(b.dataset.level || 0, 10) - parseInt(a.dataset.level || 0, 10);
      }
      return 0;
    });

    /* animate out → reorder → animate in */
    grid.style.opacity = '0.4';
    grid.style.transition = 'opacity .15s';
    setTimeout(function () {
      cards.forEach(function (c) { grid.appendChild(c); });
      grid.style.opacity = '1';
    }, 130);
  }

  function init() {
    var bars = document.querySelectorAll('.profile-sort-bar');
    bars.forEach(function (bar) {
      var grid = bar.nextElementSibling;
      if (!grid || !grid.classList.contains('plaque-grid')) return;

      bar.querySelectorAll('.profile-sort-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          bar.querySelectorAll('.profile-sort-btn').forEach(function (b) { b.classList.remove('active'); });
          btn.classList.add('active');
          sortPlaques(grid, btn.dataset.sort);
        });
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
