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
| `--atomic` | `#38bdf8` | Atomic tier accent (sky blue) |
| `--composite` | `#c084fc` | Composite tier accent (purple) |
| `--legendary` | `#f59e0b` | Legendary tier accent (amber) |

---

## Skill Tiers

Three tiers, each with a fixed color identity and symbolic glyph.

| Tier | Symbol | Display Name | Hex | RGB |
|---|---|---|---|---|
| `atomic` | ○ | Intrinsic | `#38bdf8` | `56,189,248` |
| `composite` | ◇ | Extra Skill | `#c084fc` | `192,132,252` |
| `legendary` | ◆ | Ultimate | `#f59e0b` | `245,158,11` |

Badge styles follow a consistent formula: `rgba({rgb}, .15)` background, `rgba({rgb}, .3)` border, solid hex text.

Card glow per tier (radial gradient, 35% opacity):
- Atomic: `rgba(56,189,248,.4)`
- Composite: `rgba(192,132,252,.4)`
- Legendary: `rgba(245,158,11,.4)`

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

## Graph Canvas

Node radii (before depth/projection scale):

| Type | Base radius |
|---|---|
| `legendary` | 12.5 |
| `composite` | 6.9 |
| `atomic` | 3.5 |

Edge line width:

| Condition | Legendary | Other |
|---|---|---|
| Highlighted (hover neighbor) | 2.2 px | 1.4 px |
| Default | 1.55 px | 0.92 px |

Sphere layout radii (at scale 1.25):
- Atomic: 250 × scale = **312 px**
- Composite: 145 × scale = **181 px**
- Legendary: 44 × scale = **55 px** (innermost)

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
- `.cmd` — `#38bdf8` (sky / atomic)
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
- Primary: `linear-gradient(135deg, --atomic, --composite)`, white text, `box-shadow: 0 0 20px rgba(56,189,248,.3)`
- Ghost: transparent bg, `--border` outline → `--atomic` on hover

**Cards** — `var(--surface)` background, `var(--border)` 1 px border, 14 px radius, radial glow overlay per tier (see Skill Tiers above).

**Callout** — dual-gradient tint: `linear-gradient(135deg, rgba(56,189,248,.08), rgba(167,139,250,.08))`, `--composite` title.

**Graph dialog** — `border: 1px solid rgba(56,189,248,.35)`, `box-shadow: 0 30px 100px rgba(0,0,0,.72), 0 0 55px rgba(56,189,248,.16)`, backdrop `rgba(0,0,0,.72) blur(6px)`.

---

## Rarity (computed)

Rarity is derived from real agent prevalence by `scripts/computeRarity.py` — never declared by contributors. It does not have a fixed color in the UI; rarity labels are rendered in `var(--muted)` text within skill pages and tree views.
