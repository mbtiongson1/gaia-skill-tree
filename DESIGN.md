# DESIGN.md — Gaia Visual Design Language

## Color Palette

CSS custom properties defined in `docs/index.html`:

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#030712` | Page background |
| `--surface` | `#0f172a` | Card / panel background |
| `--border` | `#1e293b` | Dividers, card borders |
| `--text` | `#e2e8f0` | Primary text |
| `--muted` | `#64748b` | Secondary / subdued text |
| `--basic`     | `#38bdf8` | Basic tier accent (sky blue) |
| `--extra`     | `#c084fc` | Extra Skill tier accent (purple) |
| `--ultimate`  | `#f59e0b` | Ultimate Skill tier accent (amber) |

---

## Skill Tiers

Three tiers, each with a fixed color identity and symbolic glyph.

| Tier | Symbol | Display Name | Hex | RGB |
|---|---|---|---|---|
| `basic`     | ○ | Basic        | `#38bdf8` | `56,189,248`  |
| `extra`     | ◇ | Extra Skill  | `#c084fc` | `192,132,252` |
| `ultimate`  | ◆ | Ultimate Skill | `#f59e0b` | `245,158,11` |

Badge styles follow a consistent formula: `rgba({rgb}, .15)` background, `rgba({rgb}, .3)` border, solid hex text.

Card glow per tier (radial gradient, 35% opacity):
- Basic: `rgba(56,189,248,.4)`
- Extra: `rgba(192,132,252,.4)`
- Ultimate: `rgba(245,158,11,.4)`

---

## Rank System

Skills level up from 0 → VI. Each rank has a distinct RPG-inspired color.

| Level | Rank | Color | Hex | Background tint |
|---|---|---|---|---|
| `0` | Basic | Slate | `#94a3b8` | `rgba(100,116,139,.12)` |
| `I` | Awakened | Sky blue | `#38bdf8` | `rgba(56,189,248,.12)` |
| `II` | Named | Teal | `#63cab7` | `rgba(99,202,183,.12)` |
| `III` | Evolved | Violet | `#a78bfa` | `rgba(167,139,250,.12)` |
| `IV` | Hardened | Fuchsia | `#e879f9` | `rgba(232,121,249,.12)` |
| `V` | Transcendent | Amber | `#fbbf24` | `rgba(251,191,36,.12)` |
| `VI ★` | Transcendent ★ | Amber (bright) | `#fbbf24` | `rgba(251,191,36,.20)` |

The rank color sequence intentionally mirrors an RPG rarity ramp: neutral → cold → teal → violet → pink → gold, with the apex doubling its background opacity.

---

## Level VI — Transcendent ★ Special Rendering

VI nodes bypass `drawNode` entirely and use `drawNodeVI`, which runs every animation frame using the shared `state.t` clock:

| Layer | Description |
|---|---|
| Outer glow | `createRadialGradient` from `r×0.5` to `r×(4.8 + 0.3·sin(t·1.8))` — hue cycles at 45°/s, with a 90° offset second stop and a fixed gold fade |
| Core node | Radial gradient with three rainbow stops (hue, hue+200, hue+60) converging to `hsl(45,100%,45%)` gold at the rim |
| Orbit sparkles | 6 dots, each rotating at 0.4 rad/s, distance pulsing with `sin(t·2.1 + i)`, each a different hue 60° apart, alpha pulsing at 3 rad/s |
| Specular | Same white highlight as standard nodes, boosted to 85% alpha |

The hue cycle formula: `hue = (t × 45) % 360` (full rainbow every ~8 s).  
Gold dominates the outer fringe (`hsl(45,…)`) so the node reads as amber at a glance but shimmers through the full spectrum up close.

---

## Graph Canvas

Node radii (before depth/projection scale):

| Type | Base radius |
|---|---|
| `ultimate`  | 12.5 |
| `extra`     | 6.9  |
| `basic`     | 3.5  |

Edge line width:

| Condition | Ultimate | Other |
|---|---|---|
| Highlighted (hover neighbor) | 2.2 px | 1.4 px |
| Default | 1.55 px | 0.92 px |

Sphere layout radii (at scale 1.25):
- Basic: 250 × scale = **312 px**
- Extra: 145 × scale = **181 px**
- Ultimate: 44 × scale = **55 px** (innermost)

---

## Typography

| Context | Stack |
|---|---|
| Body | `Inter, system-ui, sans-serif` |
| Code / CLI | `JetBrains Mono, Fira Code, Courier New, monospace` |

Type scale:
- Hero h1: `clamp(2.4rem, 6vw, 4rem)`, weight 800, line-height 1.1
- Section h2: `clamp(1.6rem, 4vw, 2.2rem)`, weight 700
- Body: 1rem / 1.65
- Small / badge: 0.72–0.82rem

Syntax highlighting in `<pre>` blocks:
- `.comment` — `#4b6378`
- `.cmd` — `#38bdf8` (sky / basic)
- `.str` — `#86efac` (green)
- `.kw` — `#a78bfa` (violet)

---

## Key UI Patterns

**Nav** — frosted glass: `background: rgba(3,7,18,.75)`, `backdrop-filter: blur(12px)`.

**Hero gradient** — three-stop sweep across all three tier colors:
```
linear-gradient(135deg, #38bdf8 0%, #c084fc 50%, #f59e0b 100%)
```

**Buttons**
- Primary: `linear-gradient(135deg, --basic, --extra)`, white text, `box-shadow: 0 0 20px rgba(56,189,248,.3)`
- Ghost: transparent bg, `--border` outline → `--basic` on hover

**Cards** — `var(--surface)` background, `var(--border)` 1 px border, 14 px radius, radial glow overlay per tier (see Skill Tiers above).

**Callout** — dual-gradient tint: `linear-gradient(135deg, rgba(56,189,248,.08), rgba(167,139,250,.08))`, `--extra` title.

**Graph dialog** — `border: 1px solid rgba(56,189,248,.35)`, `box-shadow: 0 30px 100px rgba(0,0,0,.72), 0 0 55px rgba(56,189,248,.16)`, backdrop `rgba(0,0,0,.72) blur(6px)`.

---

## Skill Explorer

The skill explorer overlay (`#skillExplorer`) introduces per-level glow tokens, a shimmer animation for Level VI nodes, and a pulse animation for Level V nodes. These augment the rank colors defined above.

### Glow Tokens

| Token | Value | Level | Rank |
|---|---|---|---|
| `--glow-II`  | `0 0 8px #63cab7, 0 0 22px rgba(99,202,183,.35)`   | II  | Named |
| `--glow-III` | `0 0 10px #a78bfa, 0 0 26px rgba(167,139,250,.4)` | III | Evolved |
| `--glow-IV`  | `0 0 14px #e879f9, 0 0 32px rgba(232,121,249,.45)`| IV  | Hardened |
| `--glow-V`   | `0 0 18px #fbbf24, 0 0 40px rgba(251,191,36,.5)`  | V   | Transcendent |
| `--glow-VI`  | `0 0 20px #fbbf24, 0 0 50px rgba(251,191,36,.6), 0 0 80px rgba(56,189,248,.3)` | VI | Transcendent ★ |

Glow tokens use the same base colors as the rank system above. Tokens are applied as `box-shadow` values on `.flow-node[data-level="X"]` and `.se-hero-card[data-level="X"]`.

### Animations

| Animation | Element | Behavior |
|---|---|---|
| `se-pulse` / `flow-pulse-V` | Level V nodes | Gold `box-shadow` oscillates between `--glow-V` and a brighter `0 0 28px #fbbf24, 0 0 60px rgba(251,191,36,.65)` on a 2.4s loop |
| `se-shimmer` / `flow-shimmer-VI` | Level VI nodes | `border-color` cycles through cyan → purple → amber → fuchsia on a 3s loop, combined with the pulse |

### Explorer UI Tokens

Additional tokens used only in the explorer overlay (not added to `:root` — defined inline):

| Color | Hex | Use |
|---|---|---|
| Skill Explorer background | `rgba(3,7,18,.88)` | Topbar background (matches `--bg` + blur) |
| Install recommended border | `rgba(56,189,248,.35)` | Gaia install block highlight |
| Evidence class color | `#f59e0b` (`--ultimate`) | Evidence class labels (A/B/C) |
| Flowchart edge stroke | `rgba(56,189,248,.22)` | SVG bezier curves connecting flowchart rows |

---

## Rarity (computed)

Rarity is derived from real agent prevalence by `scripts/computeRarity.py` — never declared by contributors. It does not have a fixed color in the UI; rarity labels are rendered in `var(--muted)` text within skill pages and tree views.
