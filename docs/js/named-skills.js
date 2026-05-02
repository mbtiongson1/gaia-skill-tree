(function () {
  function esc(str) {
    return String(str == null ? '' : str)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function nsClick(id) { return 'onclick="openSkillExplorer(\''+id.replace(/'/g,"\\'")+'\')\"'; }
  function nsDisplayName(ns) { return ns.name || ns.id.split('/')[1] || ns.id; }

  // ── TAG COLORS (8-color hash wheel, matches DESIGN.md palette) ──
  var TAG_PAL=[
    {c:'#38bdf8',bg:'rgba(56,189,248,.12)',bd:'rgba(56,189,248,.3)'},
    {c:'#c084fc',bg:'rgba(192,132,252,.12)',bd:'rgba(192,132,252,.3)'},
    {c:'#63cab7',bg:'rgba(99,202,183,.12)',bd:'rgba(99,202,183,.3)'},
    {c:'#a78bfa',bg:'rgba(167,139,250,.12)',bd:'rgba(167,139,250,.3)'},
    {c:'#f59e0b',bg:'rgba(245,158,11,.12)',bd:'rgba(245,158,11,.3)'},
    {c:'#e879f9',bg:'rgba(232,121,249,.12)',bd:'rgba(232,121,249,.3)'},
    {c:'#fb923c',bg:'rgba(251,146,60,.12)',bd:'rgba(251,146,60,.3)'},
    {c:'#4ade80',bg:'rgba(74,222,128,.12)',bd:'rgba(74,222,128,.3)'},
  ];
  function tagStyle(t){var h=0;for(var i=0;i<t.length;i++)h=(h*31+t.charCodeAt(i))%TAG_PAL.length;var p=TAG_PAL[h];return 'style="color:'+p.c+';background:'+p.bg+';border-color:'+p.bd+'"';}
  function tagHtml(t){return '<span class="ns-tag" '+tagStyle(t)+'>'+esc(t)+'</span>';}

  // ── TERMINAL INSTALL ROW ──
  var CLIP_SM='<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="5" width="9" height="9" rx="1.5"/><path d="M11 5V3a1 1 0 00-1-1H3a1 1 0 00-1 1v7a1 1 0 001 1h2"/></svg>';
  var CHECK_SM='<svg width="13" height="13" viewBox="0 0 16 16" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8l4 4 8-8"/></svg>';
  function installRow(id){
    var cmd='gaia install '+id;
    return '<div class="ns-install-row"><span class="ns-install-prompt">$</span>'+
      '<span class="ns-install-cmd-txt">'+esc(cmd)+'</span>'+
      '<button class="ns-install-copy" title="Copy install command" data-cmd="'+esc(cmd)+'" onclick="event.stopPropagation();nsInstCopy(this)">'+CLIP_SM+'</button>'+
    '</div>';
  }
  window.nsInstCopy = function(btn){
    navigator.clipboard.writeText(btn.dataset.cmd).then(function(){
      var prev=btn.innerHTML; btn.innerHTML=CHECK_SM;
      setTimeout(function(){btn.innerHTML=prev;},1500);
    }).catch(function(){});
  };

  function renderTile(ns, lm) {
    var tags = (ns.tags||[]).slice(0,3).map(tagHtml).join('');
    return '<article class="ns-tile" data-level="'+esc(ns.level)+'" data-type="'+esc(ns.type||'basic')+'" '+nsClick(ns.id)+'>' +
      '<div class="ns-tile-head">' +
        '<span class="ns-level-badge" style="color:'+lm.color+';background:'+lm.bg+';border-color:'+lm.border+'">'+esc(ns.level)+'</span>' +
        (ns.origin ? '<span class="ns-origin">\u2605</span>' : '') +
      '</div>' +
      '<div class="ns-tile-name">' + esc(nsDisplayName(ns)) + '</div>' +
      '<div class="ns-tile-id">' + esc(ns.id) + '</div>' +
      (tags ? '<div class="ns-tile-tags">' + tags + '</div>' : '') +
      installRow(ns.id) +
    '</article>';
  }

  function renderListRow(ns, lm) {
    var tags = (ns.tags||[]).slice(0,2).map(tagHtml).join('');
    return '<article class="ns-list-row" data-level="'+esc(ns.level)+'" data-type="'+esc(ns.type||'basic')+'" '+nsClick(ns.id)+'>' +
      '<span class="ns-level-badge" style="color:'+lm.color+';background:'+lm.bg+';border-color:'+lm.border+'">'+esc(ns.level)+'</span>' +
      '<span class="ns-lr-name">' + esc(nsDisplayName(ns)) + '</span>' +
      '<span class="ns-lr-id">' + esc(ns.id) + '</span>' +
      '<span class="ns-lr-tags">' + tags + '</span>' +
      '<span style="flex:1"></span>' +
      installRow(ns.id) +
      '<span class="ns-lr-arrow">\u203a</span>' +
    '</article>';
  }

  function renderFlowchartView(allNamed, lm) {
    var groups = {};
    allNamed.forEach(function(ns) {
      var ref = ns.genericSkillRef || 'other';
      if (!groups[ref]) groups[ref] = [];
      groups[ref].push(ns);
    });
    return Object.keys(groups).sort().map(function(ref) {
      var cards = groups[ref].map(function(ns) {
        var m = lm[ns.level] || lm['II'];
        return '<div class="ns-fc-leaf-wrap">' +
          '<article class="ns-fc-card" data-level="'+esc(ns.level)+'" data-type="'+esc(ns.type||'basic')+'" '+nsClick(ns.id)+'>' +
            '<div style="margin-bottom:.3rem"><span class="ns-level-badge" style="color:'+m.color+';background:'+m.bg+';border-color:'+m.border+'">'+esc(ns.level)+'</span>' +
            (ns.origin ? ' <span class="ns-origin">\u2605</span>' : '') + '</div>' +
            '<div class="ns-fc-card-name">'+esc(nsDisplayName(ns))+'</div>' +
            '<div class="ns-fc-card-id">'+esc(ns.id)+'</div>' +
          '</article>' +
        '</div>';
      }).join('');
      return '<div class="ns-fc-group">' +
        '<div class="ns-fc-root"><span style="opacity:.5">&#9671;</span> '+esc(ref)+'</div>' +
        '<div class="ns-fc-connector"></div>' +
        '<div class="ns-fc-branches-wrap"><div class="ns-fc-hbar"></div>' +
          '<div class="ns-fc-branches">'+cards+'</div>' +
        '</div>' +
      '</div>';
    }).join('');
  }

  function initNamedSkills() {
    var grid = document.getElementById('nsGrid');
    var tabsEl = document.getElementById('nsLevelTabs');
    var viewBtnsEl = document.getElementById('nsViewBtns');
    var searchEl = document.getElementById('nsSearch');
    var sortEl = document.getElementById('nsSort');
    if (!grid) return;

    var viewMode = 'tile';
    var levelFilter = 'all';
    var searchQuery = '';
    var sortMode = 'level';
    var FALLBACK_NAMED_INDEX = { buckets: {
      'automated-testing':           [{ id:'0xdarkmatter/pytest-patterns',            name:'Pytest Patterns',               contributor:'0xdarkmatter',       origin:true,  genericSkillRef:'automated-testing',           status:'named', level:'III', description:'Comprehensive pytest skill covering modern patterns for Python test automation including fixtures, parametrize, async testing, mocking, coverage strategies, integration tests, and conftest organisation for pytest 7.0+ projects.',            title:'The Quality Guardian',           tags:['pytest','python','test-automation','fixtures','async-testing','coverage','mocking'],                   links:{ github:'https://github.com/aiskillstore/marketplace' } }],
      'test-driven-development':     [{ id:'addy-osmani/test-driven-development',     name:'Test-Driven Development',       contributor:'addy-osmani',        origin:true,  genericSkillRef:'test-driven-development',     status:'named', level:'II',  description:'Forces the AI agent to follow a strict red-green-refactor TDD workflow — writing failing tests before any implementation code, blocking code generation that skips the test step, and enforcing coverage thresholds before completing a task.', title:'The Red-Green Oath',             tags:['tdd','testing','red-green-refactor','workflow-enforcement','software-quality'],              links:{ github:'https://github.com/addyosmani/agent-skills' } }],
      'document-editing':            [{ id:'anthropic/pptx',                           name:'PPTX Editor',                   contributor:'anthropic',          origin:true,  genericSkillRef:'document-editing',            status:'named', level:'II',  description:'Extracts slide content from PowerPoint (.pptx) files using markitdown, applies edits or design principles in-place, and repacks the file — enabling agents to read, modify, and write structured presentation files without a GUI.',            title:'The Slide Artisan',              tags:['pptx','powerpoint','document-editing','markitdown','presentations'],                          links:{ github:'https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md' } }],
      'tool-creation':               [{ id:'anthropic/skill-creator',                 name:'Skill Creator',                 contributor:'anthropic',          origin:true,  genericSkillRef:'tool-creation',               status:'named', level:'II',  description:'Interviews the user through a structured dialogue to elicit the skill\'s purpose, trigger conditions, and step-by-step instructions, then programmatically writes a new SKILL.md file ready for use in a Claude Code or Codex CLI skills directory.', title:'The Skill Forger\'s Art',        tags:['skill-authoring','meta-agent','claude-code','tool-creation'],                                links:{ github:'https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md' } }],
      'autonomous-debug':            [{ id:'devin-ai/autonomous-swe',                 name:'Autonomous SWE',                contributor:'devin-ai',           origin:true,  genericSkillRef:'autonomous-debug',            status:'named', level:'III', description:'Autonomous software engineering agent capable of end-to-end debugging, code generation, and self-correction across complex multi-file codebases.',                                                                                               title:'The Codebreaker\'s Will',        tags:['software-engineering','autonomous','debugging','code-generation','self-correction'],         links:{ github:'https://github.com/cognition-labs/devin' } }],
      'write-report':                [{ id:'glincker/readme-generator',               name:'README Generator',              contributor:'glincker',           origin:true,  genericSkillRef:'write-report',                status:'named', level:'II',  description:'Analyzes a project\'s directory structure, dependency manifests, and configuration files to generate a professional README.md covering installation, usage, API reference, and contributing guidelines.',                                          title:'The Document Weaver',            tags:['documentation','readme','code-analysis','project-structure'],                                links:{ github:'https://github.com/GLINCKER/claude-code-marketplace/blob/main/skills/documentation/readme-generator/SKILL.md' } },
                                      { id:'spring-ai/readme-generate',               name:'REST API README Generator',     contributor:'spring-ai',          origin:false, genericSkillRef:'write-report',                status:'named', level:'II',  description:'Scans a Java Spring project for controller annotations, extracts REST API endpoint definitions, and automatically generates structured API documentation in README format.',                                                                      title:'The Endpoint Scribe',            tags:['java','spring','rest-api','documentation','readme'],                                         links:{ github:'https://github.com/spring-ai-alibaba/examples/tree/main/.claude/skills' } }],
      'browser-automation':          [{ id:'gooseworks/notte-browser',                name:'Notte Browser',                 contributor:'gooseworks',         origin:true,  genericSkillRef:'browser-automation',          status:'named', level:'III', description:'AI-first browser automation using the Notte Browser API to control browser sessions, scrape pages, fill forms, take screenshots, and run autonomous web agents with managed credential handling.',                                              title:'The Digital Navigator',          tags:['browser','automation','web-agent','scraping','notte'],                                       links:{ github:'https://github.com/gooseworks-ai/goose-skills' } }],
      'autonomous-research-agent':   [{ id:'karpathy/autoresearch',                   name:'AutoResearch',                  contributor:'karpathy',           origin:true,  genericSkillRef:'autonomous-research-agent',   status:'named', level:'VI',  description:'Autonomous research agent that iteratively searches, reads, and synthesizes academic papers into structured summaries.',                                                                                                                           title:'The Scholar\'s Compass',         tags:['research','autonomous','paper-synthesis'],                                                   links:{ github:'https://github.com/karpathy/autoresearch' } }],
      'framework-upgrade':           [{ id:'laravel/upgrade-laravel-v13',             name:'Upgrade Laravel v13',           contributor:'laravel',            origin:true,  genericSkillRef:'framework-upgrade',           status:'named', level:'II',  description:'Guides an AI agent through upgrading a Laravel 12 application to Laravel 13 safely, covering breaking changes, dependency updates, config migrations, and post-upgrade test validation.',                                                       title:'The Versionist\'s Trial',        tags:['laravel','php','framework-upgrade','migration'],                                             links:{ github:'https://github.com/laravel/boost/issues/698' } }],
      'ux-audit':                    [{ id:'martin-stepanoski/nielsen-heuristics-audit',name:'Nielsen Heuristics Audit',    contributor:'martin-stepanoski',  origin:true,  genericSkillRef:'ux-audit',                    status:'named', level:'II',  description:'Audits a UI interface against Jakob Nielsen\'s 10 usability heuristics step-by-step, scoring each heuristic, surfacing violations, and producing a prioritized remediation report.',                                                             title:'The Ten Laws of Sight',          tags:['ux','usability','nielsen','heuristics','accessibility'],                                     links:{ npm:'https://classic.yarnpkg.com/en/package/@mastepanoski/claude-skills' } }],
      'multi-agent-orchestration-v': [{ id:'ruvnet/flow-nexus-swarm',                 name:'Flow Nexus Swarm',              contributor:'ruvnet',             origin:true,  genericSkillRef:'multi-agent-orchestration-v', status:'named', level:'III', description:'Cloud-based AI swarm orchestration platform supporting hierarchical, mesh, ring, and star topologies with event-driven workflows, message queue processing, and intelligent agent assignment.',                                                  title:'The Grand Conductor\'s Blueprint',tags:['multi-agent','swarm','orchestration','event-driven','workflow'],                             links:{ github:'https://github.com/ruvnet/ruflo' } }],
      'generate-test':               [{ id:'upsonic/unittest-generator',              name:'Unittest Generator',            contributor:'upsonic',            origin:true,  genericSkillRef:'generate-test',               status:'named', level:'II',  description:'Autonomous Claude agent that generates comprehensive unittest.TestCase suites from source code, organising tests into concept-based subfolders under a tests/ directory with proper imports, fixtures, and edge-case coverage.',                 title:'The Test Weaver',                tags:['unit-testing','unittest','test-generation','python','autonomous-agent'],                      links:{ github:'https://github.com/Upsonic/Upsonic' } }],
      'skill-discovery':             [{ id:'vercel/find-skills',                      name:'Find Skills',                   contributor:'vercel',             origin:true,  genericSkillRef:'skill-discovery',             status:'named', level:'II',  description:'Searches the skills.sh registry by keyword or category, queries install counts to surface popular skills, and auto-installs the selected skill into the current project\'s skills directory.',                                                   title:'The Registry Scout',             tags:['skill-registry','discovery','skills-sh','auto-install'],                                     links:{ github:'https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md' } }],
      'rag-pipeline':                [{ id:'yonatangross/orchestkit-rag',             name:'OrchestrKit RAG',               contributor:'yonatangross',       origin:true,  genericSkillRef:'rag-pipeline',                status:'named', level:'III', description:'Production-grade RAG retrieval skill covering 30+ patterns including core pipeline composition, HyDE query expansion, pgvector hybrid search, cross-encoder reranking, multimodal chunking, and agentic self-RAG and corrective-RAG loops.', title:'The Knowledge Architect',        tags:['rag','retrieval','hybrid-search','hyde','pgvector','reranking','agentic-rag'],               links:{ github:'https://github.com/yonatangross/orchestkit' } }],
    }};

    Promise.all([
      fetch('graph/named/index.json').then(function(r){ if (!r.ok) throw r; return r.json(); }).catch(function(){ return FALLBACK_NAMED_INDEX; }),
      fetch('graph/gaia.json').then(function(r){ if (!r.ok) throw r; return r.json(); }).catch(function(){ return { skills: [] }; }),
    ]).then(function(results) {
      var indexData = results[0], fullGraph = results[1];
      var skillMap = {};
      (fullGraph.skills || []).forEach(function(s){ skillMap[s.id] = s; });

      var buckets = indexData.buckets || {};
      var allNamed = [];
      Object.values(buckets).forEach(function(arr){ if (Array.isArray(arr)) Array.prototype.push.apply(allNamed, arr); });

      window._gaiaSkillMap = skillMap;
      window._gaiaNamedBuckets = buckets;
      window._gaiaNamedAll = allNamed;

      // Augment each named skill with type + level from the generic skill in gaia.json
      allNamed.forEach(function(ns) {
        var g = skillMap[ns.genericSkillRef];
        if (g) {
          if (!ns.type) ns.type = g.type;
          if (g.level) ns.level = g.level;
        }
      });

      var levelOrder = ['II','III','IV','V','VI'];
      allNamed.sort(function(a, b) {
        var d = levelOrder.indexOf(a.level) - levelOrder.indexOf(b.level);
        return d !== 0 ? d : String(a.id).localeCompare(String(b.id));
      });

      if (!allNamed.length) {
        grid.innerHTML = '<div class="ns-empty">No named skills yet. Publish the first with <code>gaia name</code>.</div>';
        return;
      }

      var LEVEL_META = {
        'II':  { name:'Named',          color:'#63cab7', bg:'rgba(99,202,183,.15)',  border:'rgba(99,202,183,.4)'  },
        'III': { name:'Evolved',        color:'#a78bfa', bg:'rgba(167,139,250,.15)', border:'rgba(167,139,250,.4)' },
        'IV':  { name:'Hardened',       color:'#e879f9', bg:'rgba(232,121,249,.15)', border:'rgba(232,121,249,.4)' },
        'V':   { name:'Transcendent',   color:'#fbbf24', bg:'rgba(251,191,36,.15)',  border:'rgba(251,191,36,.4)'  },
        'VI':  { name:'Transcendent ★', color:'#fbbf24', bg:'rgba(251,191,36,.22)', border:'rgba(251,191,36,.55)' },
      };

      var TYPE_ORDER = ['ultimate','extra','basic'];
      var TYPE_META_G = {
        ultimate: { glyph:'◆', label:'Ultimate', color:'#f59e0b' },
        extra:    { glyph:'◇', label:'Extra',    color:'#c084fc' },
        basic:    { glyph:'○', label:'Basic',    color:'#38bdf8' },
      };

      function nsType(ns) { return ns.type || 'basic'; }

      function groupHeader(type, id) {
        var tm = TYPE_META_G[type]; if (!tm) return '';
        return '<div class="ns-group-header" id="ns-group-'+id+'">' +
          '<span class="ns-group-glyph" style="color:'+tm.color+'">'+tm.glyph+'</span>'+tm.label+
        '</div>';
      }

      function renderCurrent() {
        var q = searchQuery.toLowerCase();
        var filtered = allNamed.filter(function(ns) {
          if (levelFilter !== 'all' && ns.level !== levelFilter) return false;
          if (q) {
            var hay = (nsDisplayName(ns)+' '+ns.id+' '+(ns.tags||[]).join(' ')+' '+(ns.contributor||'')).toLowerCase();
            if (hay.indexOf(q) === -1) return false;
          }
          return true;
        });
        if (sortMode === 'creator') filtered.sort(function(a,b){return (a.contributor||'').localeCompare(b.contributor||'');});
        else if (sortMode === 'name') filtered.sort(function(a,b){return nsDisplayName(a).localeCompare(nsDisplayName(b));});
        if (!filtered.length) { grid.innerHTML='<div class="ns-empty">No skills match.</div>'; return; }
        function lm(ns) { return LEVEL_META[ns.level] || LEVEL_META['II']; }

        if (viewMode === 'flow') {
          grid.className = 'ns-grid-flow';
          grid.innerHTML = renderFlowchartView(filtered, LEVEL_META);
        } else {
          // Group by type: ultimate → extra → basic
          var groups = { ultimate:[], extra:[], basic:[] };
          filtered.forEach(function(ns){ var t=nsType(ns); (groups[t]||(groups[t]=[])).push(ns); });
          var html = '';
          TYPE_ORDER.forEach(function(type) {
            var items = groups[type]; if (!items || !items.length) return;
            html += groupHeader(type, type);
            if (viewMode === 'list') html += items.map(function(ns){ return renderListRow(ns, lm(ns)); }).join('');
            else html += items.map(function(ns){ return renderTile(ns, lm(ns)); }).join('');
          });
          grid.className = viewMode === 'list' ? 'ns-grid-list' : 'ns-grid-tile';
          grid.innerHTML = html;
        }
      }

      if (tabsEl) {
        tabsEl.addEventListener('click', function(e) {
          var btn = e.target.closest('.ns-tab');
          if (!btn) return;
          tabsEl.querySelectorAll('.ns-tab').forEach(function(t){ t.classList.remove('active'); });
          btn.classList.add('active');
          levelFilter = btn.dataset.level || 'all';
          renderCurrent();
        });
      }

      if (viewBtnsEl) {
        viewBtnsEl.addEventListener('click', function(e) {
          var btn = e.target.closest('.ns-view-btn');
          if (!btn) return;
          viewBtnsEl.querySelectorAll('.ns-view-btn').forEach(function(b){ b.classList.remove('active'); });
          btn.classList.add('active');
          viewMode = btn.dataset.view || 'tile';
          renderCurrent();
        });
      }

      if (searchEl) {
        searchEl.addEventListener('input', function(){ searchQuery = searchEl.value; renderCurrent(); });
      }

      if (sortEl) {
        sortEl.addEventListener('change', function(){ sortMode = sortEl.value; renderCurrent(); });
      }

      // Dock: click to jump to group
      renderCurrent();
    }).catch(function() {
      grid.innerHTML = '<div class="ns-empty">Unable to render named skills.</div>';
    });

    // Grab-to-scroll: click+drag anywhere in the Named Skills section scrolls the page
    var named = document.getElementById('named');
    if (named) {
      var _startY, _startSY, _pressing = false, _dragged = false;
      named.addEventListener('mousedown', function(e) {
        if (e.button !== 0) return;
        if (e.target.closest('button,input,select,a,[role="button"]')) return;
        _pressing = true; _dragged = false;
        _startY = e.clientY; _startSY = window.scrollY;
      }, { passive: true });
      window.addEventListener('mousemove', function(e) {
        if (!_pressing) return;
        var dy = e.clientY - _startY;
        if (!_dragged && Math.abs(dy) > 4) { _dragged = true; named.classList.add('ns-grabbing'); }
        if (_dragged) window.scrollTo(0, _startSY - dy);
      });
      window.addEventListener('mouseup', function() {
        if (!_pressing) return;
        _pressing = false;
        named.classList.remove('ns-grabbing');
        if (_dragged) {
          named.addEventListener('click', function killClick(ev) {
            ev.stopPropagation(); named.removeEventListener('click', killClick, true);
          }, true);
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNamedSkills);
  } else {
    initNamedSkills();
  }
})();
