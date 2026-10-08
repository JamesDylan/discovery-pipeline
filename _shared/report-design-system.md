# Report design system — "The Company Layer"

This is the visual contract for every report this workspace produces. It is a **reference layer asset** — stable across runs, like `house-view.md`. Change it here, never in a generated report.

The source was a compiled artifact with 100% inline styles. A generated report should use real CSS custom properties and classes. The **values** below are the contract; the authoring method is not.

---

## The ten rules

If a generated report breaks any of these, it is off-system.

1. Warm paper `#f3f0e9`, never white. `#fffdf8` is the raised alternate.
2. Georgia at **weight 500** with negative tracking for every heading. Helvetica Neue for
   everything else. No webfonts — the page loads zero network fonts by design.
3. Zero border-radius. Two exceptions: the 42px circular section badge, one 100px pill button.
4. **Zero box-shadow.** Depth is background colour + 1px hairlines + accent top-rules. Only effect
   in the document is `backdrop-filter:blur(16px)` on the sticky header.
5. `max-width:1480px`; section padding `100px 96px`; body content indented `margin-left:80px` under
   a `62px 1fr` section header. That 80px indent is the strongest layout signature.
6. One circular Georgia badge per section, containing a number or a glyph.
7. Alternate section grounds on a fixed rhythm. Invert to ink `#17211f` **exactly once**. Forest
   `#1f5146` is for bands only.
8. Coral `#e9684b` = problem / unanswered. Forest `#1f5146` = ours / answer. Gold `#f4d073` is only
   ever inline emphasis on a dark ground.
9. Every headline claim gets a matching `<details>` carrying the raw evidence, plus one global
   expand/collapse pill in the header.
10. End with a self-critical caveat section and a dated, linked source grid.

---

## 1. Colour

```css
/* ground */
--paper:      #f3f0e9;   /* body, default section ground */
--surface:    #fffdf8;   /* raised alternate section, cards on figures, text on dark */
--ink:        #17211f;   /* text primary; the one inverted section; footer */

/* text ramp on light */
--ink-70:     #46514e;   /* hero deck, band body */
--ink-70-alt: #4f5d57;   /* prose inside green/light sections, evidence body */
--muted:      #66706d;   /* captions, table de-emphasis, nav, most-used text colour */

/* structure */
--rule:       #cfc9be;   /* THE hairline. 1px section dividers, table rows, grid cells */
--rule-dark:  #4b5552;   /* hairline on the ink ground */
--rule-sage:  #aab8ad;   /* hairline on sage/sand grounds */

/* brand */
--forest:     #1f5146;   /* primary. verdict band, links, accent rules, numbered eyebrows */
--coral:      #e9684b;   /* attention/alarm. leaks, "None", link hover, badge numbers */
--gold:       #f4d073;   /* inline emphasis on dark grounds ONLY */
--gold-alt:   #e8c766;   /* a card top-rule */
--blush:      #f4d3c8;   /* ::selection, the keystone card fill */

/* section tints */
--sage:       #dfe8df;   /* one "what we build" section */
--sand:       #e9e3d8;   /* the caveats section */
--mint-hover: #d9e7df;   /* source-tile hover fill */
--mint-text:  #bcd3c7;   /* eyebrow on forest ground */

/* text ramp on ink */
--on-ink-1:   #fffdf8;
--on-ink-2:   #d9dddb;   /* list items */
--on-ink-3:   #c2c9c6;   /* body */
--on-ink-4:   #aab4b0;   /* deck / eyebrow */
--on-ink-5:   #b4bfbb;   /* footer */
--badge-dark: #73807c;   /* circle badge border on ink */

/* alpha, verbatim */
--header-bg:  rgba(243,240,233,0.94);
--dot-grid:   rgba(31,81,70,0.13);
```

**No dark mode.** No data-viz palette — there are no charts. The nearest categorical scale is the
four-gear top-rule sequence: `forest → gold-alt → coral (keystone) → ink`.

Status semantics are absolute: coral = leak / unanswered / "None". Forest = ours / answer.
Muted = "Partial".

---

## 2. Typography

```css
--font-sans:  'Helvetica Neue', Helvetica, Arial, sans-serif;  /* all running text */
--font-serif: Georgia, serif;                                   /* all display + numerals */
body { -webkit-font-smoothing: antialiased }
```

The serif/sans split is the system's signature: **Georgia for anything that is a headline, a
number, a stat or a glyph; Helvetica Neue for all prose, captions, table bodies and nav.** Georgia
headings are always `font-weight:500` — deliberately not bold — with negative tracking.

### Display (Georgia, weight 500)

| Role | Size | Line-height | Tracking |
|---|---|---|---|
| H1 hero | `76px` | `0.98` | `-0.045em` |
| H2 section | `50px` | `1` | `-0.035em` |
| H2 minor section | `44px` | `1` | `-0.035em` |
| H3 band headline | `38px` / `36px` | `1.05` / `1.1` | — |
| Verdict pull-quote | `34px` | `1.22` | `-0.02em` |
| H3 article | `32` / `30` / `28px` | — | — |
| H3 card | `26px` | — | — |
| H3 small card | `21px` | — | — |
| Big stat value | `30px` | — | — |
| Gear metric | `27px` | — | — |
| Ordinal (`1st`, `01`) | `24px` | — | — |
| Step number | `23px` | — | — (coral) |
| Arrow glyph `⟶ ↑ ↓ ⟵` | `22px` | — | — (forest) |
| Section badge glyph | `14px` | — | — |
| Wordmark | `21px` | **700** | — |

Three negative-tracking steps only: `-0.02em` at 34px, `-0.035em` at 44–50px, `-0.045em` at 76px.

### Prose (Helvetica Neue, weight 400)

| Role | Size | Line-height | Colour |
|---|---|---|---|
| Hero deck | `21px` | `1.45` | `--ink-70` |
| Section deck | `17px` | `1.5` | `--muted` |
| Band body | `16px` | `1.5–1.6` | `--ink-70` / `--surface` |
| Article body | `15px` | `1.55` | `--ink-70-alt` (max-width `880px`) |
| Card body | `14px` | `1.5` | `--muted` |
| Evidence body | `14px` | **`1.7`** | `--ink-70-alt` |
| Table cell | `14px` | `1.45` | inherit |
| Annotation | `13px` | `1.7` | `--ink-70` |
| Caption / footer | `12px` | `1.45–1.55` | `--muted` |
| Gear leak note | `12.5px` | `1.5` | `--muted` |

Bold-700 exceptions in sans: table first column, `<summary>` label, tagline (`Turns gear 03 · …`),
source-link label, wordmark, all eyebrows.

### All-caps micro-type — three tracking steps

| Role | Size | Tracking | Colour |
|---|---|---|---|
| Hero eyebrow | `12px`/700 | `0.14em` | `--forest` |
| Section eyebrow, gear label | `12px`/700 | `0.12em` | `--mint-text` / `--muted` |
| Card kicker, band kicker, figcaption | `10px`/700 (figcaption 400) | `0.1em` | `--muted` / `--on-ink-4` |
| Table header | `11px`/400 | `0.09em` | `--muted`, left-aligned |

---

## 3. Layout

```css
main, footer { max-width: 1480px; margin: 0 auto }
header { height: 70px; padding: 0 72px }
section { padding: 100px 96px }          /* hero: 110px 96px 70px, min-height 560px */
html { scroll-behavior: smooth; scroll-padding-top: 90px }
```

- **96px is the canonical section gutter.** Header is 72px. Footer `32px 96px`.
- **The 80px indent:** every section body sits in a `margin-left:80px` wrapper, aligning under the
  section header's text column (a `62px 1fr` grid with 18px gap = 80px).
- Section header → body gap: `50px` on stages, `44px` elsewhere.
- Verdict band is inset from main: `margin: 0 40px`, `padding: 48px 54px`.

### Spacing scale
`2 · 6 · 8 · 12 · 14 · 18 · 20 · 24 · 26 · 28 · 32 · 38 · 44 · 48 · 54 · 70 · 80 · 96 · 100`
Grid gaps cluster at `12, 14, 18, 20, 22, 24, 28, 30, 48`.

### Prose measures
Hero H1 `1080px` · hero deck `740px` · section deck `680px` · article body `880px` ·
evidence & method note `1000px`.

### Recurring grids
```css
62px 1fr / gap 18px              /* section header: badge + title block */
180px 1fr / gap 30px             /* verdict band */
repeat(5, 1fr)                   /* journey steps */
repeat(3, 1fr) / gap 24px        /* comparison cards */
repeat(3, minmax(0,1fr))         /* asset grid — NO gap, cells share hairlines */
70px 1fr / gap 20px              /* numbered article row */
1fr 1.2fr / gap 48px, align-end  /* accent decision band */
1fr 250px 1fr · auto 170px auto  /* the flywheel figure */
1fr 1fr                          /* sources grid */
38px 1fr / gap 12px              /* source link row */
```

### Border weights — a real scale

| Weight | Meaning |
|---|---|
| `1px solid var(--rule)` | default hairline |
| `1px dashed var(--coral)` | "leaks here" divider |
| `1px solid var(--ink)` | strong rule under the hero stat strip and the journey grid |
| `2px solid var(--ink)` or `var(--forest)` | opens a list of numbered articles, or a table |
| `4px solid <accent>` | card top-rule / category marker |

### Radius
`0` everywhere · `50%` on the 42×42 badge · `100px` on the header pill. Nothing else.

### Breakpoints
The source has **none** — it is desktop-first and effectively non-responsive, with only
`overflow-x:auto` table wrappers and a `26vw` hero disc. **Fix this in generation.** A stakeholder
asset gets read on a laptop in a room, but it also gets forwarded. Add breakpoints at 1024 and 768
that collapse multi-column grids to one column, reduce the section gutter `96 → 40 → 24`, drop the
80px indent to 0, and step the display scale down (`76 → 52 → 40`). Keep everything else.

---

## 4. Components

Sixteen block patterns. A generated report composes from these and adds nothing.

| ID | Name | What it does |
|---|---|---|
| C1 | Sticky header | wordmark + meta line + anchor nav + C2. `blur(16px)` over 94% paper |
| C2 | Pill toggle | the only button. Expands/collapses all evidence. Hover = coral fill |
| C3 | Hero | eyebrow · 2-line display headline with a forest `<em>` · deck · C4 · dot-grid disc |
| C4 | Stat strip | `border-top:1px solid ink`, 4 flex cells: Georgia 30px value + 12px caption |
| C5 | Verdict band | forest ground, `180px 1fr`, eyebrow + Georgia 34px statement, gold `<strong>` |
| C6 | Section header | 42px circle badge (`01`, `AI`, `†`, `§`, `▪`) + H2 + deck |
| C7 | Journey strip | 5-cell bordered `<ol>`, coral ordinal + title + one line. min-height 200px |
| C8 | Comparison cards | 3 × `border-top:4px accent`, kicker · H3 · body · "The catch:" counterweight |
| C9 | Asset grid | 3×2 on ink, shared hairlines, no gap. Bottom-pinned proof list. 6th cell is forest |
| C10 | Flywheel figure | 4 corner gear cards + 4 connector glyphs + forest keystone centre. `role="img"` |
| C11 | Numbered articles | `2px` rule opens; `70px 1fr` rows; ordinal · H3 · body · `·`-separated tagline |
| C12 | Accent band | coral or forest, `1fr 1.2fr` align-end, kicker · H3 38px · body with gold strong |
| C13 | Evidence disclosure | `<details>`, hand-typed `▸`, marker hidden, `reveal 0.22s` body animation |
| C14 | Data table | uppercase `th`, hairline rows, first col bold+nowrap, **numerics in Georgia** |
| C15 | Caution list | `border-top:4px coral`, `<ol>` of claim + explanation |
| C16 | Sources grid + footer | 2-col bordered link tiles, hover mint · method note · ink footer |

**Not in the system — do not invent:** tabs, filters, charts or SVG data-viz, chips, scroll-spy,
modals, icons of any kind, photography, search, sidebar TOC, progress bar, dark-mode toggle.

### C13, in detail — the core interaction
```html
<details>
  <summary>▸&nbsp; See the full release log, dated</summary>
  <div class="reveal"> … </div>
</details>
```
`summary::-webkit-details-marker{display:none}`; the `▸` is typed and does **not** rotate. Summary
is 13px/700 forest, padding `16px 0` (big) or `14px 0` (small). Body layouts: table in an
`overflow-x:auto` wrapper · two-column prose (`1fr 1fr`, gap 28px, max 1000px) · single prose ·
stacked prose.

---

## 5. Interactivity

The entire behavioural surface is **one toggle plus native HTML**.

```js
btn.addEventListener('click', () => {
  open = !open;
  document.querySelectorAll('details').forEach(d => d.open = open);
  btn.textContent = open ? 'Collapse evidence' : 'Expand all evidence';
});
```

Plus the whole of the source's CSS behaviour:
```css
::selection { color:#17211f; background:#f4d3c8 }
a { color:#1f5146 }
a:hover { color:#e9684b }
summary::-webkit-details-marker { display:none }
html { scroll-behavior:smooth; scroll-padding-top:90px }
@keyframes reveal { from{opacity:0;transform:translateY(-4px)} to{opacity:1;transform:none} }
```

Behaviour list: sticky header (no shrink, no scroll-spy) · smooth anchor nav · native `<details>`
×4 · one `reveal` animation, the only animation in the document · global expand/collapse · hover
states on nav, pill, source tiles · horizontal table scroll.

**Accessibility is load-bearing, not decoration.** The figure carries `role="img"` with a
descriptive `aria-label`. Clean `h1 → h2 → h3`. `<ol>` for sequences, `<article>` per item,
`<figure>/<figcaption>`. Native `<details>` means keyboard access and find-in-page for free.

### Two things to add that the source lacks
- **`@media print`** — force all `<details>` open, drop the sticky header, remove the dot-grid.
  This asset will get printed for a room.
- **A deep-link parameter** (`?expand=1`) replacing the source's build-time `expandEvidence` prop,
  so a reader can be sent straight to the fully-opened version.

---

## 6. Content architecture

The source's section rhythm, which a generated report should hold:

| # | Section | Ground |
|---|---|---|
| 1 | Hero | paper |
| 2 | Verdict | **forest band** |
| 3 | The journey, in one view | paper |
| 4 | Stage 1 — what changed | paper |
| 5 | Stage 2 — what we own | **ink (the one inversion)** |
| 6 | Stage 3 — where we stall | surface |
| 7 | Stage 4 — what we build | **sage** |
| 8 | The AI interaction | surface |
| 9 | Stage 5 — where this lands | paper |
| 10 | Read with care | **sand** |
| 11 | Sources | surface |
| — | Footer | **ink** |

### The rhetorical shape
Claim → verdict stated up front → roadmap → threat → asset → **self-criticism** → prescription →
adjacency → forcing function → **epistemic honesty** → provenance. Headlines first; evidence folded
underneath. A skimmer can stop after the verdict and still have the argument.

Devices worth reproducing: a **keystone** (one metric that moves everything) · **convergence**
claims (two independent methods landing on the same number) · a "The catch / Watch" counterweight
on every positive card · explicit "leaks here" labelling on every loop stage · `·`-separated
tagline chains binding each recommendation to a mechanism, a rival and a target.

The self-criticism and the caveats sections are not modesty. They are the trust move, and a
generated report that drops them loses the thing that made the original credible.

---

## 7. Text conventions

- `&nbsp;` to prevent bad breaks in display type (`company&nbsp;graph`) and after every `▸`.
- Curly quotes and real typographic marks: `’ “ ” — → ⟶ ⟵ ↑ ↓ × § † ▪`.
- `·` as the separator in taglines and meta lines.
- Emphasis in prose is `<strong>` with an explicit colour and `font-weight:500` on coloured
  grounds — so gold/forest emphasis reads as a **colour** change, not a weight change.
- Numbers carry their unit and comparator inline: `12.4 vs 3.1` · `+40% YoY` · `€2.3M` · `~4,800` (illustrative).
- Copy bound for a prototyping tool follows that tool's house style (see `prototype-target.md`).
  The report is not bound by it, and uses em dashes freely.
