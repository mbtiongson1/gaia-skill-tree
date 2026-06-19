---
name: sticky-terminal-simulation
description: Generate interactive, animated, responsive HTML-based terminal simulators with a sticky layout (left or right column) to showcase pipelines or CLI executions.
---

# Sticky Terminal Simulation

An agent skill for implementing highly polished, interactive terminal/CLI simulators in side-by-side split layouts. Rather than stacking elements vertically, the terminal panel is fixed or sticky on one column while steps or timeline cards scroll on the adjacent column.

## Template Components

### 1. HTML Layout

Structure the split view with a wrapper class and layout columns. Use the class `sticky-left` or `sticky-right` to position the simulator:

```html
<div class="split-layout sticky-left">
  <!-- Left Side: Sticky Simulator Column -->
  <div class="simulator-col">
    <div class="simulator-wrapper" id="simWrapper">
      <div class="simulator-header">
        <div class="simulator-dots">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
        </div>
        <div class="simulator-title">sticky-cli-simulation.sh</div>
        <button class="simulator-btn" id="startSimBtn">Run Simulation</button>
      </div>
      <div class="simulator-body" id="simulatorConsole">
        <div class="console-line system">> Scroll to start or click "Run Simulation".</div>
      </div>
    </div>
  </div>

  <!-- Right Side: Scrollable Timeline Steps -->
  <div class="scrollable-col">
    <!-- Steps cards go here -->
    <div class="step-card">Step Content 1</div>
    <div class="step-card">Step Content 2</div>
  </div>
</div>
```

---

### 2. Premium CSS (Split & Sticky Layout)

```css
/* Layout Wrapper */
.split-layout {
  display: grid;
  gap: 3.5rem;
  align-items: start;
}

/* Position mapping */
.split-layout.sticky-left {
  grid-template-columns: 1.15fr 0.85fr;
}

.split-layout.sticky-left .simulator-col {
  grid-column: 1;
  position: sticky;
  top: 3rem;
}

.split-layout.sticky-left .scrollable-col {
  grid-column: 2;
}

.split-layout.sticky-right {
  grid-template-columns: 0.85fr 1.15fr;
}

.split-layout.sticky-right .simulator-col {
  grid-column: 2;
  position: sticky;
  top: 3rem;
}

.split-layout.sticky-right .scrollable-col {
  grid-column: 1;
}

/* Tablet & Mobile Stack styling */
@media (max-width: 1024px) {
  .split-layout.sticky-left,
  .split-layout.sticky-right {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .split-layout.sticky-left .simulator-col,
  .split-layout.sticky-right .simulator-col {
    grid-column: 1;
    position: static;
  }
  
  .split-layout.sticky-left .scrollable-col,
  .split-layout.sticky-right .scrollable-col {
    grid-column: 1;
  }
}

/* Terminal Simulator styling */
.simulator-wrapper {
  background: #08080a;
  border: 1px solid var(--border, #222);
  border-radius: 12px;
  overflow: hidden;
  font-family: var(--font-mono, ui-monospace, monospace);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
}

.simulator-header {
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid var(--border, #222);
  padding: 0.75rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.simulator-dots .dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 4px;
}
.simulator-dots .dot.red { background: #ef4444; }
.simulator-dots .dot.yellow { background: #fbbf24; }
.simulator-dots .dot.green { background: #22c55e; }

.simulator-title {
  font-size: 0.8rem;
  color: var(--muted, #666);
}

.simulator-btn {
  font-size: 0.8rem;
  padding: 0.4rem 0.9rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border, #222);
  color: var(--text, #eee);
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.simulator-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--text, #eee);
}

.simulator-body {
  padding: 1.25rem;
  font-size: 0.85rem;
  line-height: 1.6;
  height: 380px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: #c9d1d9;
}

.console-line.system { color: #8b949e; }
.console-line.agent { color: #58a6ff; }
.console-line.cmd { color: #58a6ff; font-weight: bold; }
.console-line.gate-pass { color: #34d399; }
```

---

### 3. JavaScript Auto-Start Engine

To start the simulator script automatically when the console enters the user's viewport, instantiate an `IntersectionObserver`:

```javascript
(function() {
  const startBtn = document.getElementById("startSimBtn");
  const consoleBox = document.getElementById("simulatorConsole");
  let isRunning = false;

  function addLog(msg, type = "system") {
    const line = document.createElement("div");
    line.className = `console-line ${type}`;
    line.innerHTML = msg;
    consoleBox.appendChild(line);
    consoleBox.scrollTop = consoleBox.scrollHeight;
  }

  if (startBtn && consoleBox) {
    // Setup observer to trigger click automatically on scroll
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !isRunning) {
          startBtn.click();
        }
      });
    }, { threshold: 0.25 });

    observer.observe(document.getElementById("simWrapper"));

    startBtn.addEventListener("click", () => {
      if (isRunning) return;
      isRunning = true;
      startBtn.disabled = true;
      startBtn.innerText = "Running...";
      consoleBox.innerHTML = "";

      let currentFrame = 0;
      const timeline = [
        { delay: 300, action: () => addLog("[System] Executing pipeline simulation...", "system") },
        { delay: 1000, action: () => addLog("[System] Completed task.", "gate-pass") }
      ];

      function runNext() {
        if (currentFrame >= timeline.length) {
          startBtn.disabled = false;
          isRunning = false;
          startBtn.innerText = "Run Simulation";
          return;
        }

        const frame = timeline[currentFrame];
        setTimeout(() => {
          frame.action();
          currentFrame++;
          runNext();
        }, frame.delay);
      }

      runNext();
    });
  }
})();
```
