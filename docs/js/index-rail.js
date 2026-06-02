/* ───────────────────────────────────────────────────────────────────────
   index-rail.js — a real, 1:1 page minimap for the landing page.

   The whole document is mapped linearly onto a fixed vertical strip, like an
   IDE minimap. Every marker sits at its TRUE position (targetOffset / docHeight)
   — not a proxy progress. A viewport "thumb" shows the actual scroll position in
   real time, and dragging the strip scrolls to the exact corresponding place.

   Markers above the explorer are the page's section headers (small dots that
   reveal their label on hover); the "Named Skills Explorer" marker is the red
   accent. Markers inside the explorer are dynamic — they mirror whatever the
   Named Skills Explorer is showing (type glyphs, A-Z letters, or DAG tiers),
   rebuilt on every view / sort / filter / search change via the
   `gaia:explorer-rendered` event from js/named-skills.js.
   ─────────────────────────────────────────────────────────────────────── */
(function () {
  "use strict";

  if (!document.getElementById("named")) return;

  var REDUCED = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Fixed section markers, top → bottom. Explorer markers are appended after.
  var SECTIONS = [
    { key: "sec:paths",          label: "Register Your Repo",    targetId: "paths" },
    { key: "sec:ultimates",      label: "Claim an Ultimate",     targetId: "ultimates" },
    { key: "sec:hall-of-heroes", label: "Hall of Heroes",        targetId: "hall-of-heroes" },
    { key: "sec:ascension",      label: "The Ascension Cycle",   targetId: "ascension" },
    { key: "sec:named",          label: "Named Skills Explorer", targetId: "named", accent: "red" }
  ];

  // ── DOM ──────────────────────────────────────────────────────────────
  var host = document.createElement("div");
  host.className = "mrail";
  host.setAttribute("role", "navigation");
  host.setAttribute("aria-label", "Page minimap");

  var track = document.createElement("div");
  track.className = "mrail-track";

  var thumb = document.createElement("div");
  thumb.className = "mrail-thumb";
  thumb.setAttribute("aria-hidden", "true");
  track.appendChild(thumb);

  host.appendChild(track);
  document.body.appendChild(host);
  document.body.setAttribute("data-mrail", "right");

  var marks = [];        // [{ el, targetId, off }]
  var docHpx = 0;        // cached document height (px)

  function docHeight() {
    var d = document.documentElement, b = document.body;
    return Math.max(d.scrollHeight, b ? b.scrollHeight : 0, d.offsetHeight);
  }
  function scrollY() { return window.scrollY || window.pageYOffset || 0; }
  function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }

  function jumpTo(id) {
    var el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: REDUCED ? "auto" : "smooth", block: "start" });
  }

  // ── Build markers (on explorer re-render) ────────────────────────────
  function buildMarks() {
    marks.forEach(function (m) { if (m.el.parentNode) m.el.parentNode.removeChild(m.el); });
    marks = [];

    var list = SECTIONS.map(function (s) {
      return {
        key: s.key, label: s.label, targetId: s.targetId, kind: "section",
        accent: s.accent, color: s.accent === "red" ? "var(--honor-red)" : "var(--muted)"
      };
    }).concat(window._gaiaExplorerMarkers || []);

    list.forEach(function (d) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "mrail-mark";
      b.setAttribute("data-kind", d.kind || "group");
      if (d.accent) b.setAttribute("data-accent", d.accent);
      if (d.color) b.style.setProperty("--mark-color", d.color);
      b.setAttribute("aria-label", "Jump to " + (d.label || d.key));

      var dot = document.createElement("span");
      dot.className = "mrail-dot";
      dot.textContent = d.kind === "section" ? "" : (d.glyph || "");
      b.appendChild(dot);

      var lab = document.createElement("span");
      lab.className = "mrail-label";
      lab.textContent = d.label || "";
      b.appendChild(lab);

      // Keyboard affordance only — pointer taps are handled by the track so a
      // drag that ends on a marker doesn't also fire a jump.
      b.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); jumpTo(d.targetId); }
      });

      track.appendChild(b);
      marks.push({ el: b, targetId: d.targetId, off: 0 });
    });

    layout();
  }

  // ── Position markers at their true document offset ───────────────────
  function layout() {
    docHpx = docHeight();
    var base = scrollY();
    marks.forEach(function (m) {
      var el = document.getElementById(m.targetId);
      if (!el) { m.el.style.display = "none"; m.off = -1; return; }
      m.el.style.display = "";
      m.off = el.getBoundingClientRect().top + base;     // absolute doc offset
      m.el.style.top = (docHpx > 0 ? (m.off / docHpx * 100) : 0) + "%";
    });
    updateThumb();
  }

  // ── Reflect the actual scroll position in real time ──────────────────
  function updateThumb() {
    var vh = window.innerHeight;
    if (docHpx <= vh + 1) { host.classList.add("is-hidden"); return; }
    host.classList.remove("is-hidden");

    var sy = scrollY();
    thumb.style.top = (sy / docHpx * 100) + "%";
    thumb.style.height = (vh / docHpx * 100) + "%";

    // Highlight the marker nearest the viewport centre (cached offsets only).
    var center = sy + vh / 2, best = null, bd = Infinity;
    for (var i = 0; i < marks.length; i++) {
      if (marks[i].off < 0) continue;
      var dd = Math.abs(marks[i].off - center);
      if (dd < bd) { bd = dd; best = marks[i]; }
    }
    for (var j = 0; j < marks.length; j++) {
      marks[j].el.setAttribute("aria-current", marks[j] === best ? "true" : "false");
    }
  }

  // ── Drag = 1:1 scroll. The rail point you touch becomes the viewport
  //    centre, so the thumb tracks your finger exactly (no easing/proxy).
  //    pointermove is coalesced to one scrollTo per frame to avoid reflow. ──
  var press = null, pendingY = null, raf = null;

  function trackRect() { return track.getBoundingClientRect(); }

  function applyScroll() {
    raf = null;
    if (pendingY == null) return;
    var r = trackRect();
    var f = r.height > 0 ? clamp((pendingY - r.top) / r.height, 0, 1) : 0;
    var target = clamp(f * docHpx - window.innerHeight / 2, 0, Math.max(0, docHpx - window.innerHeight));
    window.scrollTo(0, target);
    pendingY = null;
  }
  function queue(y) {
    pendingY = y;
    if (raf == null) raf = requestAnimationFrame(applyScroll);
  }

  track.addEventListener("pointerdown", function (e) {
    docHpx = docHeight();   // fresh frame for the drag math
    press = { y0: e.clientY, moved: false, markEl: e.target.closest(".mrail-mark") };
    try { track.setPointerCapture(e.pointerId); } catch (_) {}
    e.preventDefault();
  });
  track.addEventListener("pointermove", function (e) {
    if (!press) return;
    if (!press.moved && Math.abs(e.clientY - press.y0) > 3) {
      press.moved = true;
      host.classList.add("is-dragging");
    }
    if (press.moved) queue(e.clientY);
  });
  function endPress(e) {
    if (!press) return;
    try { track.releasePointerCapture(e.pointerId); } catch (_) {}
    host.classList.remove("is-dragging");
    if (!press.moved) {
      if (press.markEl) {
        var idx = [].indexOf.call(track.children, press.markEl);
        // find the mark record for this element
        for (var i = 0; i < marks.length; i++) {
          if (marks[i].el === press.markEl) { jumpTo(marks[i].targetId); break; }
        }
        void idx;
      } else {
        queue(press.y0);   // tap on empty rail → scroll to that point
      }
    }
    press = null;
  }
  track.addEventListener("pointerup", endPress);
  track.addEventListener("pointercancel", endPress);

  // ── Real-time follow + relayout triggers ─────────────────────────────
  var followQueued = false;
  window.addEventListener("scroll", function () {
    if (followQueued) return;
    followQueued = true;
    requestAnimationFrame(function () { followQueued = false; updateThumb(); });
  }, { passive: true });

  var resizeT;
  window.addEventListener("resize", function () {
    clearTimeout(resizeT);
    resizeT = setTimeout(layout, 120);
  });
  window.addEventListener("load", layout);
  document.addEventListener("gaia:explorer-rendered", buildMarks);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildMarks);
  } else {
    buildMarks();
  }
})();
