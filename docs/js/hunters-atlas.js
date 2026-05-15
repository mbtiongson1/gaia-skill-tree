/**
 * hunters-atlas.js — Populates the new Hunter's Atlas sections:
 *   1. Available Ultimates (Path B)
 *   2. Hall of Heroes (contributor plates)
 *   3. Ascension Cycle hover captions
 */
(function () {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Wait for data to be available (named-skills.js populates these globals)
  function waitForData(cb) {
    var attempts = 0;
    var timer = setInterval(function () {
      attempts++;
      if (window._gaiaSkillMap && window._gaiaNamedAll) {
        clearInterval(timer);
        cb(window._gaiaSkillMap, window._gaiaNamedAll, window._gaiaNamedBuckets || {});
      } else if (attempts > 50) {
        clearInterval(timer);
        // Fallback: try loading directly
        Promise.all([
          fetch('graph/gaia.json').then(function (r) { return r.json(); }).catch(function () { return { skills: [] }; }),
          fetch('graph/named/index.json').then(function (r) { return r.json(); }).catch(function () { return { buckets: {} }; }),
        ]).then(function (res) {
          var skillMap = {};
          (res[0].skills || []).forEach(function (s) { skillMap[s.id] = s; });
          var buckets = res[1].buckets || {};
          var allNamed = [];
          Object.values(buckets).forEach(function (arr) { if (Array.isArray(arr)) Array.prototype.push.apply(allNamed, arr); });
          cb(skillMap, allNamed, buckets);
        });
      }
    }, 100);
  }

  // ── 1. AVAILABLE ULTIMATES ──
  function populateUltimates(skillMap, allNamed) {
    var list = document.getElementById('unclaimedUltimatesList');
    if (!list) return;

    // Find all ultimate skills
    var ultimateSkills = [];
    Object.values(skillMap).forEach(function (s) {
      if (s.type === 'ultimate') ultimateSkills.push(s);
    });

    // Find which ones have named implementations
    var namedRefs = {};
    allNamed.forEach(function (ns) {
      if (ns.genericSkillRef) namedRefs[ns.genericSkillRef] = true;
    });

    var unclaimed = ultimateSkills.filter(function (s) { return !namedRefs[s.id]; });
    var claimed = ultimateSkills.filter(function (s) { return namedRefs[s.id]; });

    // Update live count
    var liveCount = document.querySelector('.live-ultimates');
    if (liveCount) {
      liveCount.textContent = unclaimed.length + ' currently unclaimed';
    }

    if (unclaimed.length === 0) {
      list.innerHTML = '<div style="color:var(--muted);padding:1rem;font-size:.9rem;">All Ultimates currently claimed. <a href="#named" style="color:var(--apex-gold)">Propose a new one →</a></div>';
      return;
    }

    var html = '';
    unclaimed.sort(function (a, b) { return (a.name || a.id).localeCompare(b.name || b.id); });
    unclaimed.forEach(function (s) {
      html += '<div class="ultimate-row" onclick="if(typeof openSkillExplorer===\'function\')openSkillExplorer(\'' + esc(s.id) + '\')">' +
        '<span class="ultimate-id">◆ /' + esc(s.id) + '</span>' +
        '<span class="ultimate-claim">Claim →</span>' +
        '</div>';
    });
    list.innerHTML = html;
  }

  // ── 2. HALL OF HEROES ──
  function populateHallOfHeroes(skillMap, allNamed) {
    var strip = document.getElementById('hallOfHeroesStrip');
    if (!strip) return;

    // Group named skills by contributor, pick highest-starred skill per contributor
    var contribs = {};
    allNamed.forEach(function (ns) {
      var handle = ns.contributor;
      if (!handle) return;
      var levelOrder = { '6★': 6, '5★': 5, '4★': 4, '3★': 3, '2★': 2 };
      var thisLevel = levelOrder[ns.level] || 0;
      if (!contribs[handle] || thisLevel > (contribs[handle]._bestLevel || 0)) {
        contribs[handle] = ns;
        contribs[handle]._bestLevel = thisLevel;
      }
    });

    // Sort by level descending, then alphabetical
    var sorted = Object.values(contribs).sort(function (a, b) {
      var diff = (b._bestLevel || 0) - (a._bestLevel || 0);
      return diff !== 0 ? diff : (a.contributor || '').localeCompare(b.contributor || '');
    });

    // Take top 8
    var top = sorted.slice(0, 8);
    var tierGlyphs = { ultimate: '◆', unique: '◉', extra: '◇', basic: '○' };

    var html = '';
    top.forEach(function (ns) {
      var g = skillMap[ns.genericSkillRef];
      var glyph = g ? (tierGlyphs[g.type] || '○') : '○';
      html += '<div class="plate">' +
        '<div class="plate-glyph">' + glyph + '</div>' +
        '<div class="plate-handle">' + esc(ns.contributor) + '</div>' +
        '<div class="plate-skill">' + esc(ns.name || ns.id.split('/')[1]) + '</div>' +
        '</div>';
    });
    strip.innerHTML = html;
  }

  // ── 3. ASCENSION CYCLE HOVER ──
  function wireAscensionCycle() {
    var caption = document.getElementById('ascensionCaption');
    var stages = document.querySelectorAll('.cycle-stage');
    if (!caption || !stages.length) return;

    var defaultText = caption.textContent;
    stages.forEach(function (stage) {
      stage.addEventListener('mouseenter', function () {
        caption.textContent = stage.dataset.caption || '';
      });
      stage.addEventListener('mouseleave', function () {
        caption.textContent = defaultText;
      });
    });
  }

  // ── INIT ──
  function init() {
    wireAscensionCycle();
    waitForData(function (skillMap, allNamed, buckets) {
      populateUltimates(skillMap, allNamed);
      populateHallOfHeroes(skillMap, allNamed);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
