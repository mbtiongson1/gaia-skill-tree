/* ───────────────────────────────────────────────────────────────────────
   AlphaRail — universal alphabetical scrubber (no dependencies).

   Usage:
     var rail = new AlphaRail({
       side: "right",                 // "right" | "left"
       onSelect: function (letter) {}, // user tapped/scrubbed a letter
       mount: document.body            // optional host (default body)
     });
     rail.render({ A: 17, B: 4, ... }); // letter -> entry count
     rail.setActive("C");               // reflect scroll position (no callback)

   Behaviour:
     • Letters spaced proportionally (tick fillers ∝ count) with uniform ticks.
     • Active letter is pulled to the vertical centre; the strip overflows and
       fades off the top/bottom edges (wheel feel, Niagara-style).
     • Hover/scrub magnifies nearest items like a macOS dock.
     • Tap a letter or drag along the rail to scrub; both fire onSelect.
   ─────────────────────────────────────────────────────────────────────── */
(function (global) {
  "use strict";

  var ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

  function AlphaRail(opts) {
    opts = opts || {};
    this.side = opts.side === "left" ? "left" : "right";
    this.onSelect = typeof opts.onSelect === "function" ? opts.onSelect : function () {};
    this.tickPer = opts.tickPer || 1;     // ticks per unit of count
    this.maxScale = opts.maxScale || 1.95; // dock peak magnification
    this.radius = opts.radius || 58;       // px magnify falloff radius
    this.pop = opts.pop || 11;             // px the peak item pops toward content
    this.reduced = !!(global.matchMedia &&
      global.matchMedia("(prefers-reduced-motion: reduce)").matches);

    this.active = null;
    this._ty = 0;            // current track translateY
    this._scrubbing = false;
    this._raf = null;
    this._pointerY = null;
    this._centers = [];      // cached item centre offsets within the track
    this._letterCenter = {}; // letter -> centre offset within the track

    this._build(opts.mount || document.body);
  }

  AlphaRail.prototype._build = function (mount) {
    var el = document.createElement("div");
    el.className = "arail";
    el.setAttribute("data-side", this.side);
    el.setAttribute("role", "navigation");
    el.setAttribute("aria-label", "Alphabetical index");

    var track = document.createElement("div");
    track.className = "arail-track";
    el.appendChild(track);
    mount.appendChild(el);

    document.body.setAttribute("data-arail", this.side);

    this.el = el;
    this.track = track;
    this._wire();
  };

  // Rebuild from a { letter: count } map.
  AlphaRail.prototype.render = function (counts) {
    counts = counts || {};
    var self = this;
    this.track.innerHTML = "";
    this.letterEls = {};

    ALPHA.forEach(function (L) {
      var c = counts[L] || 0;

      var b = document.createElement("button");
      b.type = "button";
      b.className = "arail-letter" + (c > 0 ? "" : " is-empty");
      b.setAttribute("data-letter", L);
      b.setAttribute("aria-label", "Jump to " + L);
      b.textContent = L;
      if (c > 0) {
        b.addEventListener("click", function () { self.select(L); });
      } else {
        b.disabled = true;
      }
      self.track.appendChild(b);
      self.letterEls[L] = b;

      var ticks = c > 0 ? Math.max(1, Math.round(c * self.tickPer)) : 0;
      for (var i = 0; i < ticks; i++) {
        var t = document.createElement("span");
        t.className = "arail-tick";
        self.track.appendChild(t);
      }
    });

    this.items = [].slice.call(this.track.children);
    this._measure();

    // Keep a sensible active letter after re-render (search/filter changes).
    if (!this.active || !this.letterEls[this.active] || this.letterEls[this.active].disabled) {
      this.active = this._firstPresent();
    }
    this._highlight();
    this._recenter(true);
  };

  AlphaRail.prototype._firstPresent = function () {
    for (var i = 0; i < ALPHA.length; i++) {
      var b = this.letterEls[ALPHA[i]];
      if (b && !b.disabled) return ALPHA[i];
    }
    return null;
  };

  // Cache transform-independent geometry (offsetTop is unaffected by scale).
  AlphaRail.prototype._measure = function () {
    var self = this;
    this._centers = this.items.map(function (it) {
      return it.offsetTop + it.offsetHeight / 2;
    });
    this._letterCenter = {};
    ALPHA.forEach(function (L) {
      var b = self.letterEls[L];
      if (b) self._letterCenter[L] = b.offsetTop + b.offsetHeight / 2;
    });
  };

  // User-driven selection (tap/scrub/click) — highlights, recenters, callback.
  AlphaRail.prototype.select = function (L) {
    if (!L || !this.letterEls[L] || this.letterEls[L].disabled) return;
    this.active = L;
    this._highlight();
    if (!this._scrubbing) this._recenter(false);
    this.onSelect(L);
  };

  // Scroll-spy driven update — highlights + recenters, no callback.
  AlphaRail.prototype.setActive = function (L) {
    if (!L || L === this.active || !this.letterEls[L]) return;
    this.active = L;
    this._highlight();
    if (!this._scrubbing) this._recenter(false);
  };

  AlphaRail.prototype._highlight = function () {
    var L = this.active;
    for (var i = 0; i < ALPHA.length; i++) {
      var b = this.letterEls[ALPHA[i]];
      if (b) b.setAttribute("aria-current", ALPHA[i] === L ? "true" : "false");
    }
  };

  AlphaRail.prototype._recenter = function (instant) {
    var c = this.active && this._letterCenter[this.active];
    if (c == null) {
      c = this._centers.length ? this._centers[Math.floor(this._centers.length / 2)] : 0;
    }
    this._ty = (global.innerHeight / 2) - c;
    if (instant || this.reduced) {
      var prev = this.track.style.transition;
      this.track.style.transition = "none";
      this.track.style.transform = "translateY(" + this._ty + "px)";
      // force reflow so the next transition (if any) starts from here
      void this.track.offsetHeight;
      this.track.style.transition = prev;
    } else {
      this.track.style.transform = "translateY(" + this._ty + "px)";
    }
  };

  // ── Magnify (macOS dock). Reads cached centres only, so no layout thrash. ──
  AlphaRail.prototype._applyMagnify = function () {
    this._raf = null;
    var y = this._pointerY;
    var dir = this.side === "right" ? -1 : 1;
    for (var i = 0; i < this.items.length; i++) {
      var center = this._ty + this._centers[i];
      var s = 1, tx = 0;
      if (y != null) {
        var d = Math.abs(center - y);
        if (d < this.radius) {
          var f = 1 - d / this.radius;        // 1 at pointer → 0 at edge
          s = 1 + (this.maxScale - 1) * f * f; // eased peak
          tx = dir * this.pop * f;
        }
      }
      this.items[i].style.transform = "translateX(" + tx + "px) scale(" + s + ")";
    }
  };

  AlphaRail.prototype._scheduleMagnify = function (y) {
    this._pointerY = y;
    if (!this._raf) this._raf = global.requestAnimationFrame(this._applyMagnify.bind(this));
  };

  AlphaRail.prototype._scrubTo = function (y) {
    var best = null, bestD = Infinity;
    for (var L in this._letterCenter) {
      if (!this.letterEls[L] || this.letterEls[L].disabled) continue;
      var d = Math.abs((this._ty + this._letterCenter[L]) - y);
      if (d < bestD) { bestD = d; best = L; }
    }
    if (best) this.select(best);
  };

  AlphaRail.prototype._wire = function () {
    var self = this;

    this.el.addEventListener("pointermove", function (e) {
      self._scheduleMagnify(e.clientY);
      if (self._scrubbing) self._scrubTo(e.clientY);
    });
    this.el.addEventListener("pointerleave", function () {
      if (!self._scrubbing) self._scheduleMagnify(null);
    });
    this.el.addEventListener("pointerdown", function (e) {
      self._scrubbing = true;
      try { self.el.setPointerCapture(e.pointerId); } catch (_) {}
      self._scrubTo(e.clientY);
      self._scheduleMagnify(e.clientY);
      e.preventDefault();
    });
    function end(e) {
      if (!self._scrubbing) return;
      self._scrubbing = false;
      try { self.el.releasePointerCapture(e.pointerId); } catch (_) {}
      self._recenter(false);          // settle the active letter to centre
      self._scheduleMagnify(null);
    }
    this.el.addEventListener("pointerup", end);
    this.el.addEventListener("pointercancel", end);

    global.addEventListener("resize", function () {
      self._measure();
      self._recenter(true);
    });
  };

  global.AlphaRail = AlphaRail;
})(window);
