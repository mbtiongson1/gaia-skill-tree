(function () {
  const GRAPH_JSON_URL = 'graph/gaia.json';
  const GRAPH_SCALE = 1.25;

  // Defaults — overwritten from meta once data loads
  let PALETTE = {
    basic:    { rgb:'56,189,248',   hex:'#38bdf8' },
    extra:    { rgb:'192,132,252',  hex:'#c084fc' },
    unique:   { rgb:'124,58,237',   hex:'#7c3aed' },
    ultimate: { rgb:'245,158,11',   hex:'#f59e0b' },
  };
  let TYPE_ORDER = { basic:0, extra:1, unique:2, ultimate:3 };
  let RANK_META = {
    '1★':  { name:'Awakened',       hex:'#38bdf8', bg:'rgba(56,189,248,.12)' },
    '2★': { name:'Named',          hex:'#63cab7', bg:'rgba(99,202,183,.12)' },
    '3★':{ name:'Evolved',        hex:'#a78bfa', bg:'rgba(167,139,250,.12)' },
    '4★': { name:'Hardened',       hex:'#e879f9', bg:'rgba(232,121,249,.12)' },
    '5★':  { name:'Transcendent',   hex:'#fbbf24', bg:'rgba(251,191,36,.12)' },
    '6★': { name:'Transcendent ★', hex:'#fbbf24', bg:'rgba(251,191,36,.20)' },
  };

  function _initMetaGraph(meta) {
    if (!meta) return;
    if (meta.typeColors) {
      PALETTE = {};
      Object.keys(meta.typeColors).forEach(function(t) {
        PALETTE[t] = { rgb: meta.typeColors[t].rgb, hex: meta.typeColors[t].hex };
      });
    }
    if (meta.levelColors && meta.levelLabels) {
      RANK_META = {};
      Object.keys(meta.levelColors).forEach(function(k) {
        if (k === '0★') return;
        RANK_META[k] = { name: meta.levelLabels[k] || k, hex: meta.levelColors[k].hex, bg: meta.levelColors[k].bg };
      });
    }
  }

  const FALLBACK_SKILLS = [
    { id:'tokenize', type:'basic', name:'Tokenize', prerequisites:[] },
    { id:'retrieve', type:'basic', name:'Retrieve', prerequisites:[] },
    { id:'embed-text', type:'basic', name:'Embed Text', prerequisites:[] },
    { id:'score-relevance', type:'basic', name:'Score Relevance', prerequisites:[] },
    { id:'web-search', type:'basic', name:'Web Search', prerequisites:[] },
    { id:'summarize', type:'basic', name:'Summarize', prerequisites:[] },
    { id:'cite-sources', type:'basic', name:'Cite Sources', prerequisites:[] },
    { id:'code-generation', type:'basic', name:'Code Generation', prerequisites:[] },
    { id:'execute-bash', type:'basic', name:'Execute Bash', prerequisites:[] },
    { id:'tool-select', type:'basic', name:'Tool Select', prerequisites:[] },
    { id:'chunk-document', type:'basic', name:'Chunk Document', prerequisites:[] },
    { id:'rank', type:'basic', name:'Rank', prerequisites:[] },
    { id:'rag-pipeline', type:'extra', name:'RAG Pipeline', prerequisites:['retrieve','chunk-document','embed-text','score-relevance','tokenize','rank'] },
    { id:'research', type:'extra', name:'Research', prerequisites:['web-search','summarize','cite-sources'] },
    { id:'error-interpretation', type:'basic', name:'Error Interpretation', prerequisites:[] },
    { id:'autonomous-debug', type:'extra', name:'Autonomous Debug', prerequisites:['code-generation','execute-bash','error-interpretation'] },
    { id:'ghostwrite', type:'extra', name:'Ghostwrite', prerequisites:['research','write-report','audience-model'] },
    { id:'knowledge-harvest', type:'extra', name:'Knowledge Harvest', prerequisites:['web-scrape','embed-text','extract-entities'] },
    { id:'autonomous-research-agent', type:'ultimate', name:'Autonomous Research Agent', prerequisites:['research','ghostwrite','knowledge-harvest'] },
  ];
  const FALLBACK_NAMED_MAP = {
    'automated-testing':           '0xdarkmatter/pytest-patterns',
    'test-driven-development':     'addy-osmani/test-driven-development',
    'document-editing':            'anthropic/pptx',
    'tool-creation':               'anthropic/skill-creator',
    'autonomous-debug':            'devin-ai/autonomous-swe',
    'write-report':                'glincker/readme-generator',
    'browser-automation':          'gooseworks/notte-browser',
    'autonomous-research-agent':   'karpathy/autoresearch',
    'framework-upgrade':           'laravel/upgrade-laravel-v13',
    'ux-audit':                    'martin-stepanoski/nielsen-heuristics-audit',
    'multi-agent-orchestration-v': 'ruvnet/flow-nexus-swarm',
    'generate-test':               'upsonic/unittest-generator',
    'skill-discovery':             'vercel/find-skills',
    'rag-pipeline':                'yonatangross/orchestkit-rag',
  };
  const FALLBACK_TITLE_MAP = {
    'automated-testing':           'The Quality Guardian',
    'test-driven-development':     'The Red-Green Oath',
    'document-editing':            'The Slide Artisan',
    'tool-creation':               "The Skill Forger's Art",
    'autonomous-debug':            "The Codebreaker's Will",
    'write-report':                'The Document Weaver',
    'browser-automation':          'The Digital Navigator',
    'autonomous-research-agent':   "The Scholar's Compass",
    'framework-upgrade':           "The Versionist's Trial",
    'ux-audit':                    'The Ten Laws of Sight',
    'multi-agent-orchestration-v': "The Grand Conductor's Blueprint",
    'generate-test':               'The Test Weaver',
    'skill-discovery':             'The Registry Scout',
    'rag-pipeline':                'The Knowledge Architect',
  };

  function normalizeSkills(graph) {
    const TYPE_ALIASES = { atomic: 'basic', composite: 'extra', legendary: 'ultimate' };
    const skills = (graph && graph.skills) ? graph.skills : FALLBACK_SKILLS;
    return skills.map(skill => ({
      id: skill.id,
      name: skill.name || skill.id,
      type: TYPE_ALIASES[skill.type] || skill.type || 'basic',
      level: skill.level || '',
      effectiveLevel: skill.effectiveLevel || (skill.level || ''),
      demerits: Array.isArray(skill.demerits) ? skill.demerits : [],
      rarity: skill.rarity || '',
      prerequisites: Array.isArray(skill.prerequisites) ? skill.prerequisites : [],
    })).filter(skill => skill.id);
  }

  function stableHash(str) {
    let h = 2166136261;
    for (let i = 0; i < str.length; i += 1) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return Math.abs(h >>> 0);
  }

  function spherePoint(radius, seed, index, count) {
    const golden = Math.PI * (3 - Math.sqrt(5));
    const i = index + (seed % 17) / 17;
    const y = 1 - (i / Math.max(count - 1, 1)) * 2;
    const ring = Math.sqrt(Math.max(0, 1 - y * y));
    const theta = golden * i + (seed % 360) * Math.PI / 180;
    return {
      x: Math.cos(theta) * ring * radius,
      y: y * radius,
      z: Math.sin(theta) * ring * radius,
      phase: (seed % 628) / 100,
    };
  }

  function buildPositions(skills, scale) {
    const groups = { basic:[], extra:[], ultimate:[] };
    const satellite = { unique:[], orphan:[] };
    const allPrereqRefs = new Set();
    skills.forEach(skill => skill.prerequisites.forEach(pid => allPrereqRefs.add(pid)));
    skills.forEach(skill => {
      if (skill.type === 'unique') { satellite.unique.push(skill); }
      else if (skill.type === 'basic' && !skill.prerequisites.length && !allPrereqRefs.has(skill.id)) {
        satellite.orphan.push(skill);
      } else {
        (groups[skill.type] || groups.basic).push(skill);
      }
    });
    Object.values(groups).forEach(group => group.sort((a,b) => (a.name || a.id).localeCompare(b.name || b.id)));
    satellite.unique.sort((a,b) => (a.name || a.id).localeCompare(b.name || b.id));
    satellite.orphan.sort((a,b) => (a.name || a.id).localeCompare(b.name || b.id));
    const positions = {};
    const radii = { basic: 250 * scale, extra: 145 * scale, ultimate: 44 * scale };
    Object.entries(groups).forEach(([type, group]) => {
      group.forEach((skill, index) => {
        positions[skill.id] = spherePoint(radii[type] || radii.basic, stableHash(skill.id), index, group.length);
      });
    });
    const uniqueCount = satellite.unique.length;
    satellite.unique.forEach((skill, idx) => {
      const seed = stableHash(skill.id);
      const spread = uniqueCount > 1 ? (idx - (uniqueCount - 1) / 2) * 120 * scale : 0;
      positions[skill.id] = {
        x: -340 * scale + spread * 0.4,
        y: spread,
        z: ((seed % 80) - 40) * scale,
        phase: (seed % 628) / 100,
        _satellite: 'unique',
      };
    });
    satellite.orphan.forEach((skill) => {
      const seed = stableHash(skill.id);
      const angle = Math.PI * 0.4 + (seed % 1000) / 1000 * Math.PI * 1.2;
      const dist = (160 + (seed % 140)) * scale;
      positions[skill.id] = {
        x: -340 * scale + Math.cos(angle) * dist,
        y: Math.sin(angle) * dist * 0.7,
        z: ((seed % 100) - 50) * scale,
        phase: (seed % 628) / 100,
        _satellite: 'orphan',
        _orbitSpeed: 0.3 + (seed % 100) / 100 * 0.9,
        _orbitRadius: dist,
        _orbitAngle: angle,
      };
    });
    return positions;
  }

  function createSkillGraph(canvas, options) {
    const ctx = canvas.getContext('2d');
    const DPR = Math.min(window.devicePixelRatio || 1, 2);
    const NAMED_LEVELS = new Set(['2★','3★','4★','5★','6★']);
    const state = {
      skills: FALLBACK_SKILLS,
      positions: buildPositions(FALLBACK_SKILLS, GRAPH_SCALE),
      stars: [],
      width: 0,
      height: 0,
      t: 0,
      mx: 0,
      my: 0,
      labelMode: options.labelMode || 'ultimate',
      scale: options.scale || GRAPH_SCALE,
      zoom: 1,
      statusEl: options.statusEl || null,
      running: options.autostart !== false,
      frame: null,
      orbitX: 0,
      orbitY: 0,
      dragging: false,
      dragLastX: 0,
      dragLastY: 0,
      dragStartX: 0,
      dragStartY: 0,
      dragMoved: false,
      hoveredId: null,
      lastHoveredId: null,
      projectedNodes: {},
      tooltipEl: null,
      nodeAlphas: {},
      searchText: '',
      legendFilterType: null,
      legendFilterRank: null,
      legendHoverType: null,
      legendHoverRank: null,
      legendEl: null,
      showTitles: false,
      redPillActive: false,
      namedMap: FALLBACK_NAMED_MAP,
      titleMap: FALLBACK_TITLE_MAP,
    };

    function resize() {
      const parent = canvas.parentElement;
      state.width = parent.clientWidth;
      state.height = parent.clientHeight;
      canvas.width = state.width * DPR;
      canvas.height = state.height * DPR;
      canvas.style.width = state.width + 'px';
      canvas.style.height = state.height + 'px';
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      state.stars = Array.from({ length: options.stars || 260 }, (_, i) => {
        const seed = i * 7919 + 97;
        const point = spherePoint((500 + (seed % 280)) * state.scale, seed, i, options.stars || 260);
        return { ...point, size: 0.4 + (seed % 13) / 10, alpha: 0.22 + (seed % 55) / 100 };
      });
    }

    function setSkills(skills) {
      state.skills = skills;
      state.positions = buildPositions(skills, state.scale);
      const newAlphas = {};
      skills.forEach(s => { newAlphas[s.id] = state.nodeAlphas[s.id] !== undefined ? state.nodeAlphas[s.id] : 1.0; });
      state.nodeAlphas = newAlphas;
      if (state.statusEl) {
        const edgeCount = skills.reduce((sum, skill) => sum + skill.prerequisites.length, 0);
        const zoomNote = options.zoomable ? ' · scroll to zoom' : '';
        const dragNote = options.draggable ? ' · drag to orbit' : '';
        state.statusEl.textContent = `${skills.length} skills · ${edgeCount} links${zoomNote}${dragNote}`;
      }
    }

    function rotX(p, a) {
      const c = Math.cos(a), s = Math.sin(a);
      return { x: p.x, y: c*p.y - s*p.z, z: s*p.y + c*p.z, phase: p.phase };
    }
    function rotY(p, a) {
      const c = Math.cos(a), s = Math.sin(a);
      return { x: c*p.x + s*p.z, y: p.y, z: -s*p.x + c*p.z, phase: p.phase };
    }
    function project(p) {
      const fov = Math.min(state.width, state.height) * 0.75;
      const dist = fov / (fov + p.z + 360 * state.scale);
      const z = state.zoom;
      return { sx: state.width / 2 + p.x * dist * z, sy: state.height / 2 + p.y * dist * z, scale: dist * z };
    }
    function drawNode(sx, sy, r, color, alpha) {
      const grad = ctx.createRadialGradient(sx, sy, 0, sx, sy, r * 3.9);
      grad.addColorStop(0, `rgba(${color.rgb},${Math.min(alpha * 0.68, 1).toFixed(2)})`);
      grad.addColorStop(0.42, `rgba(${color.rgb},${Math.min(alpha * 0.24, 1).toFixed(2)})`);
      grad.addColorStop(1, `rgba(${color.rgb},0)`);
      ctx.beginPath(); ctx.arc(sx, sy, r * 3.9, 0, Math.PI * 2); ctx.fillStyle = grad; ctx.fill();
      ctx.beginPath(); ctx.arc(sx, sy, r, 0, Math.PI * 2); ctx.fillStyle = `rgba(${color.rgb},${Math.min(alpha * 1.18, 1).toFixed(2)})`; ctx.fill();
      ctx.beginPath(); ctx.arc(sx - r * 0.28, sy - r * 0.28, r * 0.32, 0, Math.PI * 2); ctx.fillStyle = `rgba(255,255,255,${(alpha * 0.65).toFixed(2)})`; ctx.fill();
    }
    function drawNodeNamed(sx, sy, r, alpha) {
      const glow = ctx.createRadialGradient(sx, sy, 0, sx, sy, r * 4.2);
      glow.addColorStop(0,   `rgba(239,68,68,${Math.min(alpha * 0.7, 1).toFixed(2)})`);
      glow.addColorStop(0.4, `rgba(239,68,68,${Math.min(alpha * 0.25, 1).toFixed(2)})`);
      glow.addColorStop(1,   'rgba(239,68,68,0)');
      ctx.beginPath(); ctx.arc(sx, sy, r * 4.2, 0, Math.PI * 2); ctx.fillStyle = glow; ctx.fill();
      ctx.beginPath(); ctx.arc(sx, sy, r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(239,68,68,${Math.min(alpha * 1.2, 1).toFixed(2)})`; ctx.fill();
      ctx.beginPath(); ctx.arc(sx - r * 0.28, sy - r * 0.28, r * 0.32, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${(alpha * 0.65).toFixed(2)})`; ctx.fill();
    }
    function drawNodeVI(sx, sy, r, alpha, t, p) {
      const hue = (t * 45) % 360;
      const phase = p.phase || 0;
      const spin = t * 1.4 + phase;
      const glowPulse = 0.7 + 0.3 * Math.sin(t * 1.8 + phase);
      const glowR = r * (4.8 + glowPulse);
      const glow = ctx.createRadialGradient(sx, sy, r * 0.5, sx, sy, glowR);
      glow.addColorStop(0,    `hsla(${hue},100%,72%,${(alpha * 0.55).toFixed(2)})`);
      glow.addColorStop(0.35, `hsla(${(hue + 90) % 360},100%,65%,${(alpha * 0.32).toFixed(2)})`);
      glow.addColorStop(0.65, `hsla(45,100%,58%,${(alpha * 0.18).toFixed(2)})`);
      glow.addColorStop(1,    'hsla(45,100%,50%,0)');
      ctx.beginPath(); ctx.arc(sx, sy, glowR, 0, Math.PI * 2); ctx.fillStyle = glow; ctx.fill();
      // Super white spinning glow overlay
      ctx.save();
      ctx.translate(sx, sy);
      ctx.rotate(spin);
      const whiteR = r * 5.5;
      const whiteGlow = ctx.createRadialGradient(0, 0, r * 0.3, 0, 0, whiteR);
      whiteGlow.addColorStop(0, `rgba(255,255,255,${(alpha * 0.5).toFixed(2)})`);
      whiteGlow.addColorStop(0.2, `rgba(255,255,255,${(alpha * 0.25).toFixed(2)})`);
      whiteGlow.addColorStop(0.5, `rgba(255,255,255,${(alpha * 0.08).toFixed(2)})`);
      whiteGlow.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.beginPath(); ctx.arc(0, 0, whiteR, 0, Math.PI * 2);
      ctx.fillStyle = whiteGlow; ctx.fill();
      // White spinning rays
      for (let i = 0; i < 5; i++) {
        const rayAngle = (Math.PI * 2 * i / 5);
        const rayAlpha = alpha * (0.3 + 0.2 * Math.sin(t * 3 + i * 1.2));
        ctx.beginPath();
        ctx.moveTo(Math.cos(rayAngle) * r * 1.3, Math.sin(rayAngle) * r * 1.3);
        ctx.lineTo(Math.cos(rayAngle) * r * 4.5, Math.sin(rayAngle) * r * 4.5);
        ctx.strokeStyle = `rgba(255,255,255,${rayAlpha.toFixed(2)})`;
        ctx.lineWidth = r * 0.25;
        ctx.lineCap = 'round';
        ctx.stroke();
      }
      ctx.restore();
      const coreGrad = ctx.createRadialGradient(sx - r * 0.25, sy - r * 0.25, 0, sx, sy, r * 1.05);
      coreGrad.addColorStop(0,    `hsla(${(hue + 200) % 360},100%,88%,${Math.min(alpha * 1.1, 1).toFixed(2)})`);
      coreGrad.addColorStop(0.45, `hsla(${hue},100%,68%,${Math.min(alpha * 1.1, 1).toFixed(2)})`);
      coreGrad.addColorStop(0.8,  `hsla(${(hue + 60) % 360},90%,55%,${alpha.toFixed(2)})`);
      coreGrad.addColorStop(1,    `hsla(45,100%,45%,${alpha.toFixed(2)})`);
      ctx.beginPath(); ctx.arc(sx, sy, r, 0, Math.PI * 2); ctx.fillStyle = coreGrad; ctx.fill();
      for (let i = 0; i < 6; i++) {
        const angle = (Math.PI * 2 * i / 6) + t * 0.4;
        const dist = r * (1.65 + 0.35 * Math.sin(t * 2.1 + i));
        const sAlpha = alpha * (0.5 + 0.5 * Math.sin(t * 3.0 + i * 1.05));
        ctx.beginPath();
        ctx.arc(sx + Math.cos(angle) * dist, sy + Math.sin(angle) * dist, r * 0.2, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${(hue + i * 60) % 360},100%,82%,${sAlpha.toFixed(2)})`;
        ctx.fill();
      }
      ctx.beginPath(); ctx.arc(sx - r * 0.28, sy - r * 0.28, r * 0.32, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${(alpha * 0.85).toFixed(2)})`; ctx.fill();
    }
    function drawNodeUnique(sx, sy, r, alpha, t, p) {
      const phase = p.phase || 0;
      const spin = t * 2.2 + phase;
      // Big dark spinning void glow
      const voidR = r * 6;
      ctx.save();
      ctx.translate(sx, sy);
      ctx.rotate(spin * 0.3);
      const voidGrad = ctx.createRadialGradient(0, 0, r * 0.8, 0, 0, voidR);
      voidGrad.addColorStop(0, `rgba(10,0,20,${(alpha * 0.7).toFixed(2)})`);
      voidGrad.addColorStop(0.3, `rgba(26,5,51,${(alpha * 0.4).toFixed(2)})`);
      voidGrad.addColorStop(0.6, `rgba(124,58,237,${(alpha * 0.12).toFixed(2)})`);
      voidGrad.addColorStop(1, `rgba(124,58,237,0)`);
      ctx.beginPath(); ctx.arc(0, 0, voidR, 0, Math.PI * 2);
      ctx.fillStyle = voidGrad; ctx.fill();
      // Spinning dark arms (like a spiral galaxy but dark)
      for (let arm = 0; arm < 3; arm++) {
        const armAngle = (Math.PI * 2 * arm / 3) + spin * 0.7;
        ctx.beginPath();
        for (let j = 0; j <= 20; j++) {
          const frac = j / 20;
          const spiralR = r * 1.2 + frac * voidR * 0.7;
          const spiralA = armAngle + frac * Math.PI * 1.5;
          const px = Math.cos(spiralA) * spiralR;
          const py = Math.sin(spiralA) * spiralR * 0.45;
          if (j === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.strokeStyle = `rgba(26,5,51,${(alpha * 0.4).toFixed(2)})`;
        ctx.lineWidth = r * 0.4;
        ctx.stroke();
      }
      ctx.restore();
      // Accretion disk particles spinning wildly
      for (let i = 0; i < 16; i++) {
        const a = (Math.PI * 2 * i / 16) + spin * (1.5 + (i % 4) * 0.4);
        const orbitR = r * (1.6 + 0.4 * Math.sin(spin * 0.9 + i * 0.7));
        const dx = Math.cos(a) * orbitR;
        const dy = Math.sin(a) * orbitR * 0.35;
        const particleAlpha = alpha * (0.4 + 0.35 * Math.sin(spin * 2.5 + i * 1.1));
        const particleR = r * (0.1 + 0.05 * Math.sin(t * 4 + i));
        ctx.beginPath();
        ctx.arc(sx + dx, sy + dy, particleR, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(167,139,250,${particleAlpha.toFixed(2)})`;
        ctx.fill();
      }
      // Event horizon ring — bright purple edge
      ctx.beginPath(); ctx.arc(sx, sy, r * 1.12, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(124,58,237,${(alpha * 0.9).toFixed(2)})`;
      ctx.lineWidth = 2; ctx.stroke();
      // Void core — pure darkness
      ctx.beginPath(); ctx.arc(sx, sy, r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(10,0,20,${Math.min(alpha * 1.2, 1).toFixed(2)})`;
      ctx.fill();
    }
    function shouldLabel(skill) {
      if (state.redPillActive && state.namedMap[skill.id]) return true;
      if (state.labelMode === 'none') return false;
      if (state.labelMode === 'all') return true;
      if (state.labelMode === 'modal') return skill.type !== 'basic' || stableHash(skill.id) % 7 === 0;
      return skill.type === 'ultimate' || skill.type === 'unique';
    }
    function draw() {
      if (!state.running) return;
      state.t += 0.006;
      ctx.clearRect(0, 0, state.width, state.height);
      state.projectedNodes = {};
      const ry = options.draggable
        ? state.t * 0.16 + state.orbitY
        : state.t * 0.16 + state.mx * 0.10;
      const rx = options.draggable
        ? Math.sin(state.t * 0.055) * 0.20 + state.orbitX
        : Math.sin(state.t * 0.055) * 0.20 + state.my * 0.055;
      const xf = {};
      const allPrereqRefs = new Set();
      state.skills.forEach(skill => skill.prerequisites.forEach(pid => allPrereqRefs.add(pid)));
      state.skills.forEach(skill => {
        const p0 = state.positions[skill.id];
        if (!p0) return;
        if (p0._satellite === 'unique') {
          xf[skill.id] = { x: p0.x, y: p0.y, z: p0.z, phase: p0.phase };
        } else if (p0._satellite === 'orphan') {
          const a = p0._orbitAngle + state.t * p0._orbitSpeed;
          const cx = -340 * state.scale;
          xf[skill.id] = {
            x: cx + Math.cos(a) * p0._orbitRadius,
            y: Math.sin(a) * p0._orbitRadius * 0.7,
            z: p0.z * Math.cos(state.t * p0._orbitSpeed * 0.5),
            phase: p0.phase,
          };
        } else {
          xf[skill.id] = rotX(rotY(p0, ry), rx);
        }
      });
      const neighborSet = new Set();
      if (state.hoveredId) {
        neighborSet.add(state.hoveredId);
        const hoveredSkill = state.skills.find(s => s.id === state.hoveredId);
        if (hoveredSkill) hoveredSkill.prerequisites.forEach(pid => neighborSet.add(pid));
        state.skills.forEach(s => { if (s.prerequisites.includes(state.hoveredId)) neighborSet.add(s.id); });
      }
      const hovering = Boolean(state.hoveredId);
      const isSearchActive = Boolean(state.searchText);
      const searchQuery = isSearchActive ? state.searchText.toLowerCase() : '';
      const legendHovering = Boolean(state.legendHoverType || state.legendHoverRank);
      const legendFiltering = Boolean(state.legendFilterType || state.legendFilterRank);
      state.skills.forEach(skill => {
        let targetVis;
        if (hovering) {
          targetVis = skill.id === state.hoveredId ? 1.0 : neighborSet.has(skill.id) ? 0.88 : 0.12;
        } else if (legendHovering) {
          const mt = !state.legendHoverType || skill.type === state.legendHoverType;
          const mr = !state.legendHoverRank || skill.level === state.legendHoverRank;
          targetVis = (mt && mr) ? 1.0 : 0.12;
        } else if (legendFiltering) {
          const mt = !state.legendFilterType || skill.type === state.legendFilterType;
          const mr = !state.legendFilterRank || skill.level === state.legendFilterRank;
          const matchesLegend = mt && mr;
          if (isSearchActive) {
            const matchesSearch = (skill.name || skill.id).toLowerCase().includes(searchQuery);
            targetVis = (matchesLegend && matchesSearch) ? 1.0 : 0.12;
          } else {
            targetVis = matchesLegend ? 1.0 : 0.12;
          }
        } else if (isSearchActive) {
          targetVis = (skill.name || skill.id).toLowerCase().includes(searchQuery) ? 1.0 : 0.12;
        } else {
          targetVis = 1.0;
        }
        if (state.redPillActive && !state.namedMap[skill.id]) targetVis = Math.min(targetVis, 0.07);
        if (state.nodeAlphas[skill.id] === undefined) state.nodeAlphas[skill.id] = targetVis;
        state.nodeAlphas[skill.id] += (targetVis - state.nodeAlphas[skill.id]) * 0.15;
      });
      state.stars.forEach(star => {
        const p = rotX(rotY(star, ry), rx);
        const pr = project(p);
        if (pr.scale < 0.01) return;
        ctx.beginPath();
        ctx.arc(pr.sx, pr.sy, star.size * pr.scale * 1.55, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${(star.alpha * Math.min(pr.scale * 2, 1)).toFixed(2)})`;
        ctx.fill();
      });
      const edges = [];
      state.skills.forEach(skill => {
        if (!xf[skill.id]) return;
        skill.prerequisites.forEach(pid => {
          if (!xf[pid]) return;
          edges.push({ from: pid, to: skill.id, type: skill.type, avgZ: (xf[skill.id].z + xf[pid].z) / 2 });
        });
      });
      edges.sort((a,b) => a.avgZ - b.avgZ);
      edges.forEach(edge => {
        const pa = project(xf[edge.from]), pb = project(xf[edge.to]);
        const col = PALETTE[edge.type] || PALETTE.basic;
        const depthAlpha = Math.min(Math.max((xf[edge.to].z + 430 * state.scale) / (860 * state.scale), 0.08), 1);
        const isNeighborEdge = hovering && neighborSet.has(edge.from) && neighborSet.has(edge.to);
        const fromVis = state.nodeAlphas[edge.from] !== undefined ? state.nodeAlphas[edge.from] : 1.0;
        const toVis   = state.nodeAlphas[edge.to]   !== undefined ? state.nodeAlphas[edge.to]   : 1.0;
        const edgeVis = (fromVis + toVis) / 2;
        const baseEdgeAlpha = isNeighborEdge ? 0.72 : 0.31;
        ctx.beginPath(); ctx.moveTo(pa.sx, pa.sy); ctx.lineTo(pb.sx, pb.sy);
        ctx.strokeStyle = `rgba(${col.rgb},${(depthAlpha * baseEdgeAlpha * edgeVis).toFixed(2)})`;
        ctx.lineWidth = isNeighborEdge ? (edge.type === 'ultimate' ? 2.2 : 1.4) : (edge.type === 'ultimate' ? 1.55 : 0.92);
        ctx.stroke();
      });
      const nodes = state.skills.map(skill => ({ skill, z: xf[skill.id] ? xf[skill.id].z : -9999 })).sort((a,b) => a.z - b.z);
      nodes.forEach(({ skill }) => {
        const p = xf[skill.id]; if (!p) return;
        const pr = project(p);
        state.projectedNodes[skill.id] = pr;
        const pulse = 0.84 + 0.16 * Math.sin(state.t * 2.2 + p.phase);
        const depthAlpha = Math.min(Math.max((p.z + 430 * state.scale) / (860 * state.scale), 0.16), 1);
        const col = PALETTE[skill.type] || PALETTE.basic;
        const baseR = skill.type === 'ultimate' ? 12.5 : skill.type === 'unique' ? 9.5 : skill.type === 'extra' ? 6.9 : 3.5;
        const vis = state.nodeAlphas[skill.id] !== undefined ? state.nodeAlphas[skill.id] : 1.0;
        if (skill.level === '6★') {
          drawNodeVI(pr.sx, pr.sy, baseR * state.scale * pr.scale * pulse, depthAlpha * vis, state.t, p);
        } else if (skill.type === 'unique') {
          drawNodeUnique(pr.sx, pr.sy, baseR * state.scale * pr.scale * pulse, depthAlpha * vis, state.t, p);
        } else if (state.redPillActive && state.namedMap[skill.id]) {
          drawNodeNamed(pr.sx, pr.sy, baseR * state.scale * pr.scale * pulse, depthAlpha * vis);
        } else {
          drawNode(pr.sx, pr.sy, baseR * state.scale * pr.scale * pulse, col, depthAlpha * vis);
        }
      });
      const labelNodes = nodes.filter(({ skill }) => shouldLabel(skill));
      function drawLabel(skill, highlighted) {
        const p = xf[skill.id]; if (!p) return;
        const pr = project(p);
        const depthAlpha = Math.min(Math.max((p.z + 430 * state.scale) / (860 * state.scale), 0), 1);
        if (!highlighted && depthAlpha < 0.22) return;
        const vis = state.nodeAlphas[skill.id] !== undefined ? state.nodeAlphas[skill.id] : 1.0;
        const labelAlpha = highlighted ? 1.0 : depthAlpha * Math.max(0.22, vis) * 0.9;
        if (labelAlpha < 0.04) return;
        const col = (state.redPillActive && state.namedMap[skill.id])
          ? { rgb:'239,68,68' }
          : (PALETTE[skill.type] || PALETTE.basic);
        const size = skill.type === 'ultimate' ? 13 : skill.type === 'extra' ? 10 : 8;
        ctx.font = `bold ${Math.max(6, Math.round(size * pr.scale * 1.16))}px Inter,system-ui,sans-serif`;
        ctx.fillStyle = `rgba(${col.rgb},${labelAlpha.toFixed(2)})`;
        ctx.textAlign = 'center';
        const labelText = (state.redPillActive && state.namedMap && state.namedMap[skill.id])
          ? state.namedMap[skill.id]
          : state.showTitles
            ? ((state.titleMap && state.titleMap[skill.id]) || skill.name)
            : '/' + skill.id;
        ctx.fillText(labelText, pr.sx, pr.sy + 18 * pr.scale);
      }
      labelNodes.forEach(({ skill }) => {
        const vis = state.nodeAlphas[skill.id] !== undefined ? state.nodeAlphas[skill.id] : 1.0;
        if (vis <= 0.95) drawLabel(skill, false);
      });
      labelNodes.forEach(({ skill }) => {
        const vis = state.nodeAlphas[skill.id] !== undefined ? state.nodeAlphas[skill.id] : 1.0;
        if (vis > 0.95) drawLabel(skill, true);
      });
      if (options.hoverable && state.tooltipEl) {
        const pr = state.projectedNodes[state.hoveredId];
        if (state.hoveredId && pr) {
          if (state.hoveredId !== state.lastHoveredId) {
            const skill = state.skills.find(s => s.id === state.hoveredId);
            const col = PALETTE[skill.type] || PALETTE.basic;
            const typeClass = `skill-tooltip-type-${skill.type}`;
            const rm = skill.level ? RANK_META[skill.level] : null;
            const rankPill = rm
              ? `<span style="display:inline-block;padding:.12rem .42rem;border-radius:999px;font-size:.62rem;font-weight:700;background:${rm.bg};color:${rm.hex}">${skill.level}</span>`
              : '';
            const effectivePill = (skill.effectiveLevel && skill.effectiveLevel !== skill.level)
              ? `<span style="display:inline-block;padding:.12rem .42rem;border-radius:999px;font-size:.62rem;font-weight:700;background:rgba(251,191,36,.16);color:#fbbf24">effective ${skill.effectiveLevel}</span>`
              : '';
            const demeritNote = skill.demerits && skill.demerits.length
              ? `<div style="color:#fbbf24;font-size:.66rem;margin-top:.26rem">${skill.demerits.length} demerit${skill.demerits.length === 1 ? '' : 's'}</div>`
              : '';
            state.tooltipEl.innerHTML =
              `<div class="skill-tooltip-name" style="color:rgba(${col.rgb},1)">${skill.name}</div>` +
              `<div style="color:#64748b;font-size:.68rem;font-weight:500;margin-bottom:.3rem;font-family:monospace">${skill.id}</div>` +
              `<div class="skill-tooltip-row"><span class="skill-tooltip-badge ${typeClass}">${skill.type.toUpperCase()}</span>${rankPill}${effectivePill}</div>${demeritNote}`;
            state.lastHoveredId = state.hoveredId;
          }
          let tx = pr.sx + 18, ty = pr.sy - 34;
          tx = Math.min(tx, state.width - 240); ty = Math.max(ty, 8);
          state.tooltipEl.style.left = tx + 'px';
          state.tooltipEl.style.top  = ty + 'px';
          state.tooltipEl.style.display = 'block';
        } else {
          state.tooltipEl.style.display = 'none';
          state.lastHoveredId = null;
        }
      }
      state.frame = requestAnimationFrame(draw);
    }

    function start() {
      if (state.running) return;
      state.running = true;
      draw();
    }

    function stop() {
      state.running = false;
      if (state.frame) cancelAnimationFrame(state.frame);
      state.frame = null;
    }

    resize();
    if (options.hoverable) {
      const tip = document.createElement('div');
      tip.className = 'skill-tooltip';
      canvas.parentElement.appendChild(tip);
      state.tooltipEl = tip;
      const searchWrap = document.createElement('div');
      searchWrap.className = 'graph-search-wrap';
      const searchInput = document.createElement('input');
      searchInput.type = 'text';
      searchInput.className = 'graph-search';
      searchInput.placeholder = 'Search skills…';
      searchInput.setAttribute('aria-label', 'Filter skill graph');
      searchInput.addEventListener('input', () => { state.searchText = searchInput.value.trim(); });
      searchInput.addEventListener('mousedown', e => e.stopPropagation());
      searchWrap.appendChild(searchInput);
      canvas.parentElement.appendChild(searchWrap);
      state.searchInputEl = searchInput;

      const legend = document.createElement('div');
      legend.className = 'graph-legend';
      legend.innerHTML =
        '<div class="graph-legend-section"><div class="graph-legend-heading">Type</div>' +
        '<div class="graph-legend-item" data-legend-type="basic"><span class="graph-legend-swatch" style="background:#38bdf8;width:7px;height:7px"></span>Basic</div>' +
        '<div class="graph-legend-item" data-legend-type="extra"><span class="graph-legend-swatch" style="background:#c084fc;width:10px;height:10px"></span>Extra</div>' +
        '<div class="graph-legend-item" data-legend-type="unique"><span class="graph-legend-swatch" style="background:#7c3aed;width:12px;height:12px"></span>Unique</div>' +
        '<div class="graph-legend-item" data-legend-type="ultimate"><span class="graph-legend-swatch" style="background:#f59e0b;width:14px;height:14px"></span>Ultimate</div>' +
        '</div><div class="graph-legend-section"><div class="graph-legend-heading">Rank</div>' +
        '<div class="graph-legend-ranks">' +
        '<span class="graph-legend-rank-pill" data-legend-rank="1★" style="background:rgba(56,189,248,.12);color:#38bdf8">1★</span>' +
        '<span class="graph-legend-rank-pill" data-legend-rank="2★" style="background:rgba(99,202,183,.12);color:#63cab7">2★</span>' +
        '<span class="graph-legend-rank-pill" data-legend-rank="3★" style="background:rgba(167,139,250,.12);color:#a78bfa">3★</span>' +
        '<span class="graph-legend-rank-pill" data-legend-rank="4★" style="background:rgba(232,121,249,.12);color:#e879f9">4★</span>' +
        '<span class="graph-legend-rank-pill" data-legend-rank="5★" style="background:rgba(251,191,36,.12);color:#fbbf24">5★</span>' +
        '<span class="graph-legend-rank-pill" data-legend-rank="6★" style="background:rgba(251,191,36,.20);color:#fbbf24">6★</span>' +
        '</div></div>';
      legend.addEventListener('mousedown', e => e.stopPropagation());
      legend.querySelectorAll('.graph-legend-item[data-legend-type]').forEach(item => {
        item.addEventListener('mouseenter', () => { state.legendHoverType = item.dataset.legendType; });
        item.addEventListener('mouseleave', () => { state.legendHoverType = null; });
        item.addEventListener('click', () => {
          const val = state.legendFilterType === item.dataset.legendType ? null : item.dataset.legendType;
          state.legendFilterType = val;
          legend.querySelectorAll('[data-legend-type]').forEach(el => el.classList.remove('active'));
          if (val) item.classList.add('active');
        });
      });
      legend.querySelectorAll('.graph-legend-rank-pill').forEach(pill => {
        pill.addEventListener('mouseenter', () => { state.legendHoverRank = pill.dataset.legendRank; });
        pill.addEventListener('mouseleave', () => { state.legendHoverRank = null; });
        pill.addEventListener('click', () => {
          const val = state.legendFilterRank === pill.dataset.legendRank ? null : pill.dataset.legendRank;
          state.legendFilterRank = val;
          legend.querySelectorAll('.graph-legend-rank-pill').forEach(el => el.classList.remove('active'));
          if (val) pill.classList.add('active');
        });
      });
      canvas.parentElement.appendChild(legend);
      state.legendEl = legend;

      const redPill = document.createElement('button');
      redPill.type = 'button';
      redPill.className = 'graph-redpill';
      redPill.textContent = 'Named Skills';
      redPill.title = 'Highlight Named skills (2★+) with contributor attribution and red glow';
      redPill.addEventListener('mousedown', e => e.stopPropagation());
      redPill.addEventListener('click', () => {
        state.redPillActive = !state.redPillActive;
        redPill.classList.toggle('active', state.redPillActive);
      });
      canvas.parentElement.appendChild(redPill);
      state.redPillEl = redPill;

      const labelToggle = document.createElement('button');
      labelToggle.type = 'button';
      labelToggle.className = 'graph-label-toggle';
      labelToggle.textContent = 'Show Title';
      labelToggle.addEventListener('mousedown', e => e.stopPropagation());
      labelToggle.addEventListener('click', () => {
        state.showTitles = !state.showTitles;
        labelToggle.classList.toggle('active', state.showTitles);
      });
      canvas.parentElement.appendChild(labelToggle);
      state.labelToggleEl = labelToggle;
    }
    window.addEventListener('resize', resize);
    const pointerTarget = options.pointerTarget || canvas;
    pointerTarget.addEventListener('mousemove', event => {
      const rect = canvas.getBoundingClientRect();
      if (options.draggable && state.dragging) {
        state.orbitY += (event.clientX - state.dragLastX) * 0.007;
        state.orbitX += (event.clientY - state.dragLastY) * 0.007;
        state.dragLastX = event.clientX;
        state.dragLastY = event.clientY;
        if (Math.hypot(event.clientX - state.dragStartX, event.clientY - state.dragStartY) > 5) state.dragMoved = true;
        state.hoveredId = null;
      } else {
        state.mx = ((event.clientX - rect.left) / Math.max(rect.width, 1) - 0.5) * 2;
        state.my = ((event.clientY - rect.top) / Math.max(rect.height, 1) - 0.5) * 2;
        if (options.hoverable) {
          const mx = event.clientX - rect.left;
          const my = event.clientY - rect.top;
          let closest = null, closestDist = 22;
          Object.entries(state.projectedNodes).forEach(([id, pr]) => {
            const d = Math.hypot(pr.sx - mx, pr.sy - my);
            if (d < closestDist) { closestDist = d; closest = id; }
          });
          state.hoveredId = closest;
          canvas.style.cursor = closest ? 'pointer' : (options.draggable ? 'grab' : 'default');
        }
      }
    });
    if (options.draggable) {
      canvas.style.cursor = 'grab';
      canvas.addEventListener('mouseleave', () => { if (!state.dragging) state.hoveredId = null; });
      canvas.addEventListener('mousedown', e => {
        e.preventDefault();
        state.dragging = true;
        state.dragMoved = false;
        state.dragStartX = e.clientX;
        state.dragStartY = e.clientY;
        state.dragLastX = e.clientX;
        state.dragLastY = e.clientY;
        canvas.style.cursor = 'grabbing';
      });
      window.addEventListener('mouseup', e => {
        if (!state.dragging) return;
        const didClick = !state.dragMoved && state.hoveredId;
        state.dragging = false;
        state.dragMoved = false;
        canvas.style.cursor = state.hoveredId ? 'pointer' : 'grab';
        if (didClick && options.onNodeClick) options.onNodeClick(state.hoveredId);
      });
    }
    if (options.zoomable) {
      canvas.addEventListener('wheel', e => {
        e.preventDefault();
        state.zoom = Math.max(0.3, Math.min(3.0, state.zoom * (1 - e.deltaY * 0.001)));
      }, { passive: false });
    }
    function resetFilters() {
      state.legendFilterType = null;
      state.legendFilterRank = null;
      state.legendHoverType = null;
      state.legendHoverRank = null;
      state.showTitles = false;
      state.searchText = '';
      state.redPillActive = false;
      if (state.redPillEl) state.redPillEl.classList.remove('active');
      if (state.legendEl) {
        state.legendEl.querySelectorAll('.active').forEach(el => el.classList.remove('active'));
      }
      if (state.searchInputEl) state.searchInputEl.value = '';
      if (state.labelToggleEl) state.labelToggleEl.classList.remove('active');
    }
    if (state.running) draw();
    function setNamedMap(map) { state.namedMap = map || {}; }
    function setTitleMap(map) { state.titleMap = map || {}; }
    return { setSkills, setNamedMap, setTitleMap, resize, start, stop, resetFilters };
  }

  const hero = document.getElementById('hero');
  const trigger = document.querySelector('[data-graph-trigger]');
  const dialog = document.getElementById('skillGraphDialog');
  const closeBtn = document.querySelector('[data-graph-close]');
  const heroGraph = createSkillGraph(document.getElementById('canvas3d'), { labelMode:'none', scale:GRAPH_SCALE, stars:280, pointerTarget:hero });
  const modalGraph = createSkillGraph(document.getElementById('graphDialogCanvas'), {
    labelMode:'all', scale:1.38, stars:320, statusEl:document.querySelector('[data-graph-status]'), autostart:false, zoomable:true, draggable:true, hoverable:true,
    onNodeClick: function(id) {
      var buckets = window._gaiaNamedBuckets || {};
      if (buckets[id] && buckets[id].length) {
        if (window.openNamedPopup) window.openNamedPopup(buckets[id][0]);
        else window.openSkillExplorer(buckets[id][0].id);
      } else {
        var skill = (window._gaiaSkillMap || {})[id] || { id: id, name: id, type: 'basic' };
        window.openUnnamedPopup(skill);
      }
    }
  });

  function peek(on) { hero.classList.toggle('hero-graph-peek', Boolean(on)); }
  trigger.addEventListener('mouseenter', () => peek(true));
  trigger.addEventListener('mouseleave', () => peek(false));
  trigger.addEventListener('focus', () => peek(true));
  trigger.addEventListener('blur', () => peek(false));
  trigger.addEventListener('click', () => {
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
    modalGraph.resize();
    modalGraph.start();
    peek(false);
  });
  function closeDialog() {
    if (dialog.close) dialog.close();
    else dialog.removeAttribute('open');
    modalGraph.resetFilters();
    modalGraph.stop();
  }
  closeBtn.addEventListener('click', closeDialog);
  dialog.addEventListener('click', event => {
    if (event.target === dialog) closeDialog();
  });
  dialog.addEventListener('close', () => modalGraph.stop());

  fetch(GRAPH_JSON_URL)
    .then(response => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(graph => {
      _initMetaGraph(graph.meta);
      return normalizeSkills(graph);
    })
    .then(skills => { heroGraph.setSkills(skills); modalGraph.setSkills(skills); })
    .catch(error => {
      console.warn('Using embedded fallback skill graph:', error);
      const status = document.querySelector('[data-graph-status]');
      if (status) status.textContent = 'Using embedded preview graph. Run the page from docs/ to load the full graph.';
    });

  fetch('graph/named/index.json')
    .then(r => r.ok ? r.json() : Promise.reject())
    .then(indexData => {
      const map = {};
      const titleMap = {};
      const buckets = indexData.buckets || {};
      Object.entries(buckets).forEach(([skillId, arr]) => {
        if (Array.isArray(arr) && arr.length) {
          const origin = arr.find(e => e.origin) || arr[0];
          if (origin && origin.id) map[skillId] = origin.id;
          if (origin && origin.title) titleMap[skillId] = origin.title;
        }
      });
      heroGraph.setNamedMap(map);
      modalGraph.setNamedMap(map);
      heroGraph.setTitleMap(titleMap);
      modalGraph.setTitleMap(titleMap);
    })
    .catch(() => {});
})();
