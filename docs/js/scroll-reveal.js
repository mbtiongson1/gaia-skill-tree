(function () {
  var revealEls = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  if (!revealEls.length) return;

  function show(el) {
    el.classList.add('visible');
  }

  if (!('IntersectionObserver' in window)) {
    revealEls.forEach(show);
    return;
  }

  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting || entry.intersectionRatio > 0) {
        show(entry.target);
        obs.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0,
    rootMargin: '0px 0px -10% 0px'
  });

  revealEls.forEach(function (el) {
    obs.observe(el);
  });
})();
