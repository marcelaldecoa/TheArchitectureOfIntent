"""
Build the modern teaching deck (HTML).

Output: paper/architecture-of-intent.html

A single self-contained HTML file. Each <section> is a slide.
- Arrow keys / Page Down / Space → next
- Arrow Left / Page Up           → prev
- Home / End                      → first / last
- "o" or ESC                      → overview grid
- "p" or "f"                      → toggle full-screen / print

The two paper figures (decision tree, orthogonality) are embedded as
inline SVG so the file is portable and prints cleanly.
"""
from pathlib import Path
import html

from presentation_content import SLIDES, PALETTE, TITLE, SUBTITLE, AUTHOR, YEAR, PAPER_KIND


HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
OUT = HERE / "architecture-of-intent.html"


def esc(s):
    return html.escape(str(s), quote=True)


def load_svg(name):
    path = FIG_DIR / name
    if not path.exists():
        return ""
    text = path.read_text()
    # Strip the XML declaration; keep the <svg ...>
    if text.startswith("<?xml"):
        text = text.split("?>", 1)[1].lstrip()
    # Add a class for sizing
    text = text.replace("<svg ", '<svg class="figure-svg" ', 1)
    return text


# ========================================================================
# Slide renderers
# ========================================================================

def slide_open(kind, dark=False):
    cls = ["slide", f"slide-{kind}"]
    if dark:
        cls.append("dark")
    return f'<section class="{" ".join(cls)}">'


def render_cover(d):
    return f'''
{slide_open("cover", dark=True)}
  <div class="cover-frame">
    <div class="accent-bar"></div>
    <div class="cover-body">
      <div class="eyebrow">{esc(d["eyebrow"])}</div>
      <h1 class="cover-title">{esc(d["title"])}</h1>
      <div class="cover-subtitle">{esc(d["subtitle"])}</div>
      <div class="cover-meta">
        <span class="cover-author">{esc(d["author"])}</span>
        <span class="cover-sep">·</span>
        <span>{esc(d["year"])}</span>
      </div>
      <div class="cover-note">{esc(d["note"])}</div>
    </div>
  </div>
  <div class="cover-tag">TEACHING DECK · COMPANION TO THE PAPER</div>
</section>
'''


def render_roadmap(d, page, total):
    items_html = ""
    for num, head, sub in d["items"]:
        items_html += f'''
        <div class="roadmap-item">
          <div class="roadmap-num">{esc(num)}</div>
          <div class="roadmap-rule"></div>
          <div class="roadmap-text">
            <div class="roadmap-head">{esc(head)}</div>
            <div class="roadmap-sub">{esc(sub)}</div>
          </div>
        </div>
        '''
    return f'''
{slide_open("roadmap")}
  {chip(d["section"])}
  <h2 class="slide-title">{esc(d["title"])}</h2>
  <div class="roadmap-list">
    {items_html}
  </div>
  {footer(page, total)}
</section>
'''


def render_quote(d, page, total):
    body = "<br>".join(esc(line) for line in d["body"])
    return f'''
{slide_open("quote")}
  {chip(d["section"])}
  <div class="quote-grid">
    <div class="quote-mark">&ldquo;</div>
    <div class="quote-text">
      <div class="quote-headline">{esc(d["headline"])}</div>
      <div class="quote-body">{body}</div>
    </div>
  </div>
  <div class="quote-footnote">{esc(d["footnote"])}</div>
  {footer(page, total)}
</section>
'''


def render_compare(d, page, total):
    def col(side):
        items_html = "".join(
            f'<li><span class="dot dot-{side["color"]}"></span>{esc(item)}</li>'
            for item in side["items"]
        )
        return f'''
        <div class="compare-col">
          <div class="compare-bar bar-{side["color"]}"></div>
          <div class="compare-eyebrow eyebrow-{side["color"]}">{esc(side["label"])}</div>
          <ul class="compare-list">
            {items_html}
          </ul>
        </div>
        '''
    return f'''
{slide_open("compare")}
  {chip(d["section"])}
  <h2 class="slide-title">{esc(d["title"])}</h2>
  <div class="slide-tagline">{esc(d["tagline"])}</div>
  <div class="compare-grid">
    {col(d["left"])}
    {col(d["right"])}
  </div>
  {footer(page, total)}
</section>
'''


def render_cards4(d, page, total):
    cards_html = ""
    for card in d["cards"]:
        if len(card) == 5:
            num, head, body, extra, color = card
        elif len(card) == 4:
            num, head, body, extra = card
            color = "indigo"
        else:
            head, body, extra = card
            num = ""
            color = "indigo"
        extra_html = (
            f'<div class="card-extra">{esc(extra)}</div>' if extra else ""
        )
        num_html = (
            f'<div class="card-num">{esc(num)}</div>' if num else ""
        )
        cards_html += f'''
        <div class="card4 card-{color}">
          <div class="card-bar"></div>
          {num_html}
          <div class="card-head">{esc(head)}</div>
          <div class="card-body">{esc(body)}</div>
          {extra_html}
        </div>
        '''
    return f'''
{slide_open("cards4")}
  {chip(d["section"])}
  <h2 class="slide-title">{esc(d["title"])}</h2>
  <div class="slide-tagline">{esc(d["tagline"])}</div>
  <div class="cards4-grid">
    {cards_html}
  </div>
  {footer(page, total)}
</section>
'''


def render_table(d, page, total):
    th = "".join(f'<th>{esc(h)}</th>' for h in d["headers"])
    rows = ""
    for row in d["rows"]:
        cells = ""
        for i, cell in enumerate(row):
            cls = "first" if i == 0 else ""
            cells += f'<td class="{cls}">{esc(cell)}</td>'
        rows += f'<tr>{cells}</tr>'
    return f'''
{slide_open("table")}
  {chip(d["section"])}
  <h2 class="slide-title">{esc(d["title"])}</h2>
  <div class="slide-tagline">{esc(d["tagline"])}</div>
  <table class="modern-table"><thead><tr>{th}</tr></thead>
    <tbody>{rows}</tbody>
  </table>
  {footer(page, total)}
</section>
'''


def render_figure(d, page, total):
    svg = load_svg(d["svg"])
    return f'''
{slide_open("figure")}
  {chip(d["section"])}
  <h2 class="slide-title">{esc(d["title"])}</h2>
  <div class="slide-tagline">{esc(d["tagline"])}</div>
  <div class="figure-wrap">
    {svg}
  </div>
  <div class="figure-caption">{esc(d["caption"])}</div>
  {footer(page, total)}
</section>
'''


def render_taxonomy(d, page, total):
    rows = ""
    for cat, name, shape, fix, novel in d["rows"]:
        cls = "novel" if novel else ""
        rows += f'''
        <tr class="{cls}">
          <td class="cat">{esc(cat)}</td>
          <td class="name">{esc(name)}</td>
          <td>{esc(shape)}</td>
          <td>{esc(fix)}</td>
        </tr>
        '''
    return f'''
{slide_open("taxonomy")}
  {chip(d["section"])}
  <h2 class="slide-title">{esc(d["title"])}</h2>
  <div class="slide-tagline">{esc(d["tagline"])}</div>
  <table class="taxonomy-table">
    <thead><tr><th>#</th><th>Name</th><th>Failure shape</th><th>Fix locus</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  {footer(page, total)}
</section>
'''


def render_cat7(d, page, total):
    subs_html = ""
    for name, fix in d["subs"]:
        subs_html += f'''
        <div class="cat7-sub">
          <div class="cat7-sub-bar"></div>
          <div class="cat7-sub-name">{esc(name)}</div>
          <div class="cat7-sub-fix">{esc(fix)}</div>
        </div>
        '''
    why_html = "".join(
        f'<li>{esc(line)}</li>' for line in d["why"]
    )
    return f'''
{slide_open("cat7")}
  {chip(d["section"])}
  <h2 class="slide-title cat7-title">{esc(d["title"])}</h2>
  <div class="slide-tagline">{esc(d["tagline"])}</div>
  <div class="cat7-grid">
    <div>
      <div class="eyebrow eyebrow-ink">FOUR SUB-CATEGORIES</div>
      <div class="cat7-subs">{subs_html}</div>
    </div>
    <div>
      <div class="eyebrow eyebrow-ink">WHY A SEPARATE CATEGORY</div>
      <ul class="cat7-why">{why_html}</ul>
    </div>
  </div>
  {footer(page, total)}
</section>
'''


def render_split_list(d, page, total):
    accent = "amber" if d.get("use_amber") else "indigo"

    def render_items(items, two_col=False):
        out = ""
        if items and isinstance(items[0], tuple):
            for head, sub in items:
                out += f'''
                <div class="split-row">
                  <span class="dot dot-{accent}"></span>
                  <div>
                    <div class="split-head">{esc(head)}</div>
                    <div class="split-sub">{esc(sub)}</div>
                  </div>
                </div>'''
        else:
            wrap_class = "split-rows-2col" if two_col else ""
            for line in items:
                out += f'''
                <div class="split-row">
                  <span class="dot dot-{accent}"></span>
                  <div class="split-head plain">{esc(line)}</div>
                </div>'''
            if two_col:
                out = f'<div class="split-rows-2col">{out}</div>'
        return out

    left_two_col = (
        d["left_items"] and not isinstance(d["left_items"][0], tuple)
        and len(d["left_items"]) > 8
    )
    right_two_col = (
        d["right_items"] and not isinstance(d["right_items"][0], tuple)
        and len(d["right_items"]) > 8
    )

    return f'''
{slide_open("split-list")}
  {chip(d["section"])}
  <h2 class="slide-title">{esc(d["title"])}</h2>
  <div class="slide-tagline">{esc(d["tagline"])}</div>
  <div class="split-grid">
    <div>
      <div class="eyebrow eyebrow-{accent}">{esc(d["left_title"].upper())}</div>
      <div class="split-rows">{render_items(d["left_items"], left_two_col)}</div>
    </div>
    <div>
      <div class="eyebrow eyebrow-{accent}">{esc(d["right_title"].upper())}</div>
      <div class="split-rows">{render_items(d["right_items"], right_two_col)}</div>
    </div>
  </div>
  {footer(page, total)}
</section>
'''


def render_callout_list(d, page, total):
    items_html = ""
    for i, (head, body) in enumerate(d["items"], start=1):
        items_html += f'''
        <div class="callout">
          <div class="callout-num">{i:02d}</div>
          <div>
            <div class="callout-head">{esc(head)}</div>
            <div class="callout-body">{esc(body)}</div>
          </div>
        </div>
        '''
    return f'''
{slide_open("callouts")}
  {chip(d["section"])}
  <h2 class="slide-title">{esc(d["title"])}</h2>
  <div class="slide-tagline">{esc(d["tagline"])}</div>
  <div class="callouts">{items_html}</div>
  {footer(page, total)}
</section>
'''


def render_discussion(d):
    qs_html = ""
    for i, q in enumerate(d["questions"], start=1):
        qs_html += f'''
        <div class="discuss-row">
          <div class="discuss-num">{i:02d}</div>
          <div class="discuss-q">{esc(q)}</div>
        </div>
        '''
    return f'''
{slide_open("discussion", dark=True)}
  <div class="discuss-frame">
    <div class="accent-bar"></div>
    <div class="discuss-body">
      <div class="eyebrow eyebrow-amber">{esc(d["section"])}</div>
      <h2 class="discuss-title">{esc(d["title"])}</h2>
      <div class="discuss-list">{qs_html}</div>
      <div class="discuss-footer">{esc(d["footer"])}</div>
    </div>
  </div>
</section>
'''


def chip(section_label):
    return f'''
    <div class="section-chip">
      <span class="chip-square"></span>
      <span class="chip-label">{esc(section_label)}</span>
    </div>'''


def footer(page, total):
    return f'''
    <div class="page-footer">
      <span class="footer-left">{esc(TITLE)}  ·  {esc(AUTHOR)}, {esc(YEAR)}</span>
      <span class="footer-right">{page:02d} / {total:02d}</span>
    </div>'''


KIND = {
    "cover": render_cover,
    "roadmap": render_roadmap,
    "quote": render_quote,
    "compare": render_compare,
    "cards4": render_cards4,
    "table": render_table,
    "figure": render_figure,
    "taxonomy": render_taxonomy,
    "cat7": render_cat7,
    "split_list": render_split_list,
    "callout_list": render_callout_list,
    "discussion": render_discussion,
}


# ========================================================================
# Page assembly
# ========================================================================

CSS = """
:root {
  --bg: #FAFAF7;
  --bg-dark: #0F1729;
  --ink: #0F1729;
  --ink-light: #FFFFFF;
  --muted: #64748B;
  --muted-2: #94A3B8;
  --rule: #E2E8F0;
  --card: #FFFFFF;
  --indigo: #6366F1;
  --indigo-dark: #4338CA;
  --indigo-pale: #EEF2FF;
  --amber: #F59E0B;
  --amber-pale: #FEF3C7;
  --amber-dark: #92400E;
  --emerald: #10B981;
  --emerald-dark: #166534;
  --rose: #E11D48;
  --rose-dark: #9F1239;
}

* { box-sizing: border-box; }

html, body {
  margin: 0; padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, sans-serif;
  background: #1a1a1f;
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ============== Stage =============== */
.stage {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.deck {
  position: relative;
  width: 1280px;
  height: 720px;
  transform-origin: center;
}

/* ============== Slide =============== */
.slide {
  position: absolute;
  inset: 0;
  background: var(--bg);
  padding: 48px 64px;
  display: none;
  flex-direction: column;
  overflow: hidden;
  font-size: 16px;
  line-height: 1.5;
}

.slide.active { display: flex; }
.slide.dark { background: var(--bg-dark); color: var(--ink-light); }

/* ============== Section chip =============== */
.section-chip {
  position: absolute;
  top: 48px; left: 64px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.chip-square {
  display: inline-block;
  width: 12px; height: 12px;
  background: var(--amber);
}
.chip-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2.5px;
  color: var(--muted);
  text-transform: uppercase;
}

/* ============== Title block =============== */
.slide-title {
  margin: 80px 0 0 0;
  font-size: 36px;
  font-weight: 800;
  color: var(--ink);
  letter-spacing: -0.5px;
}
.slide-tagline {
  margin-top: 12px;
  font-size: 15px;
  font-style: italic;
  color: var(--muted);
  max-width: 1100px;
  line-height: 1.55;
}

.slide-figure .slide-title {
  margin: 56px 0 0 0;
  font-size: 28px;
}
.slide-figure .slide-tagline {
  margin-top: 6px;
  font-size: 13px;
}

/* ============== Eyebrow =============== */
.eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  margin-bottom: 12px;
}
.eyebrow-indigo { color: var(--indigo); }
.eyebrow-amber  { color: var(--amber); }
.eyebrow-emerald{ color: var(--emerald-dark); }
.eyebrow-rose   { color: var(--rose-dark); }
.eyebrow-muted  { color: var(--muted); }
.eyebrow-ink    { color: var(--ink); }

/* ============== Footer =============== */
.page-footer {
  position: absolute;
  left: 64px; right: 64px;
  bottom: 32px;
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  letter-spacing: 1px;
  color: var(--muted-2);
}

/* ============== Cover =============== */
.cover-frame {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 32px;
  align-items: center;
  height: 100%;
  padding: 0 32px 0 0;
}
.accent-bar {
  width: 8px;
  height: 280px;
  background: var(--amber);
}
.cover-body { padding-left: 16px; }
.cover-title {
  font-size: 76px;
  font-weight: 800;
  letter-spacing: -2px;
  margin: 16px 0 18px 0;
  line-height: 1.05;
  color: var(--ink-light);
}
.cover-subtitle {
  font-size: 26px;
  font-style: italic;
  color: var(--muted-2);
  margin-bottom: 36px;
  font-weight: 300;
}
.cover-meta {
  font-size: 18px;
  letter-spacing: 1.5px;
  color: var(--ink-light);
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 8px;
}
.cover-sep { color: var(--muted-2); }
.cover-note {
  font-size: 13px;
  color: var(--muted-2);
  font-style: italic;
}
.cover-tag {
  position: absolute;
  bottom: 32px;
  right: 64px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 3px;
  color: var(--muted-2);
}
.eyebrow.eyebrow-amber {
  font-size: 12px;
  letter-spacing: 3px;
}
.cover-body .eyebrow { color: var(--amber); }

/* ============== Roadmap =============== */
.roadmap-list { margin-top: 28px; flex: 1; display: flex; flex-direction: column; justify-content: center; }
.roadmap-item {
  display: grid;
  grid-template-columns: 80px 1px 1fr;
  gap: 24px;
  align-items: center;
  padding: 12px 0;
}
.roadmap-num {
  font-size: 38px;
  font-weight: 800;
  color: var(--indigo);
  letter-spacing: -1px;
}
.roadmap-rule {
  width: 1px;
  height: 50px;
  background: var(--rule);
}
.roadmap-head {
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
}
.roadmap-sub {
  font-size: 13px;
  color: var(--muted);
  font-style: italic;
  margin-top: 4px;
}

/* ============== Quote =============== */
.quote-grid {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 16px;
  margin-top: 28px;
  flex: 1;
  align-items: center;
}
.quote-mark {
  font-family: Georgia, serif;
  font-size: 220px;
  color: var(--indigo);
  line-height: 0.7;
  font-weight: 700;
}
.quote-headline {
  font-size: 44px;
  font-weight: 800;
  color: var(--ink);
  letter-spacing: -1px;
  line-height: 1.1;
}
.quote-body {
  font-size: 22px;
  font-style: italic;
  color: var(--muted);
  margin-top: 22px;
  line-height: 1.5;
}
.quote-footnote {
  background: var(--card);
  border: 1px solid var(--rule);
  border-left: 3px solid var(--indigo);
  border-radius: 4px;
  padding: 16px 20px;
  font-size: 14px;
  color: var(--ink);
  margin-bottom: 64px;
}

/* ============== Compare =============== */
.compare-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 28px;
  flex: 1;
}
.compare-col {
  position: relative;
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: 8px;
  padding: 24px 28px;
}
.compare-bar {
  position: absolute;
  left: 0; top: 0;
  width: 6px;
  height: 100%;
  border-radius: 8px 0 0 8px;
}
.bar-indigo  { background: var(--indigo); }
.bar-amber   { background: var(--amber); }
.bar-emerald { background: var(--emerald); }
.bar-rose    { background: var(--rose); }
.bar-muted   { background: var(--muted); }
.compare-eyebrow {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  margin-bottom: 18px;
  margin-left: 8px;
}
.compare-list { list-style: none; margin: 0; padding: 0 0 0 8px; }
.compare-list li {
  position: relative;
  padding: 10px 0 10px 20px;
  font-size: 15px;
  color: var(--ink);
  line-height: 1.5;
}
.dot {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 2px;
  margin-right: 12px;
  vertical-align: 2px;
}
.dot-indigo  { background: var(--indigo); }
.dot-amber   { background: var(--amber); }
.dot-emerald { background: var(--emerald); }
.dot-rose    { background: var(--rose); }
.dot-muted   { background: var(--muted); }

/* ============== 4 cards =============== */
.cards4-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-top: 28px;
  flex: 1;
}
.card4 {
  position: relative;
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: 8px;
  padding: 32px 24px 24px 24px;
  display: flex;
  flex-direction: column;
}
.card-bar {
  position: absolute;
  left: 0; right: 0; top: 0;
  height: 6px;
  border-radius: 8px 8px 0 0;
}
.card-indigo .card-bar { background: var(--indigo); }
.card-amber .card-bar  { background: var(--amber); }
.card-num {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 16px;
}
.card-indigo .card-num { color: var(--indigo); }
.card-amber  .card-num { color: var(--amber); }
.card-head {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--ink);
  margin-bottom: 12px;
}
.card-body {
  font-size: 14px;
  font-style: italic;
  color: var(--ink);
  line-height: 1.5;
  flex: 1;
}
.card-extra {
  font-size: 11px;
  color: var(--muted);
  border-top: 1px solid var(--rule);
  padding-top: 12px;
  margin-top: 12px;
  letter-spacing: 0.3px;
}

/* ============== Table =============== */
.modern-table, .taxonomy-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 24px;
  font-size: 14px;
}
.modern-table thead, .taxonomy-table thead { background: var(--bg-dark); }
.modern-table thead th, .taxonomy-table thead th {
  color: var(--ink-light);
  text-align: left;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 14px 16px;
}
.modern-table tbody tr:nth-child(odd), .taxonomy-table tbody tr:nth-child(odd) {
  background: var(--card);
}
.modern-table tbody td, .taxonomy-table tbody td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--rule);
  color: var(--ink);
  vertical-align: middle;
}
.modern-table tbody td.first {
  font-weight: 700;
  color: var(--indigo);
}
.taxonomy-table tbody td.cat,
.taxonomy-table tbody td.name {
  font-weight: 700;
  color: var(--indigo);
  width: 12%;
}
.taxonomy-table tbody td.cat { width: 8%; }
.taxonomy-table tbody tr.novel {
  background: var(--amber-pale) !important;
  border-left: 4px solid var(--amber);
}
.taxonomy-table tbody tr.novel td.cat,
.taxonomy-table tbody tr.novel td.name {
  color: var(--amber-dark);
}

/* ============== Figure =============== */
.figure-wrap {
  flex: 1 1 auto;
  display: block;
  position: relative;
  margin-top: 16px;
  overflow: hidden;
  min-height: 0;
}
.figure-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
}
.figure-caption {
  text-align: center;
  font-size: 11px;
  font-style: italic;
  color: var(--muted);
  margin-top: 8px;
  margin-bottom: 48px;
}

/* ============== Cat 7 deep dive =============== */
.cat7-title { color: var(--amber-dark); }
.cat7-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-top: 24px;
  flex: 1;
}
.cat7-subs { display: flex; flex-direction: column; gap: 10px; }
.cat7-sub {
  position: relative;
  display: grid;
  grid-template-columns: 200px 1fr;
  align-items: center;
  background: var(--card);
  border: 1px solid var(--rule);
  border-radius: 6px;
  padding: 14px 18px 14px 24px;
}
.cat7-sub-bar {
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 4px;
  background: var(--amber);
  border-radius: 6px 0 0 6px;
}
.cat7-sub-name { font-size: 15px; font-weight: 700; color: var(--ink); }
.cat7-sub-fix  { font-size: 13px; color: var(--amber-dark); font-style: italic; }
.cat7-why {
  list-style: none;
  margin: 0; padding: 0;
}
.cat7-why li {
  position: relative;
  padding: 10px 0 10px 22px;
  font-size: 14px;
  color: var(--ink);
}
.cat7-why li::before {
  content: "■";
  color: var(--amber);
  position: absolute;
  left: 0;
  font-size: 14px;
  top: 10px;
}

/* ============== Split list =============== */
.split-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  margin-top: 24px;
  flex: 1;
}
.split-rows { display: flex; flex-direction: column; gap: 12px; }
.split-rows-2col {
  display: grid !important;
  grid-template-columns: 1fr 1fr;
  gap: 8px 24px;
}
.split-row {
  display: grid;
  grid-template-columns: 16px 1fr;
  gap: 8px;
  align-items: start;
}
.split-row .dot { margin-top: 6px; }
.split-head { font-size: 14px; font-weight: 700; color: var(--ink); }
.split-head.plain { font-weight: 500; }
.split-sub { font-size: 12px; font-style: italic; color: var(--muted); margin-top: 2px; }

/* ============== Callouts =============== */
.callouts {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  flex: 1;
}
.callout {
  display: grid;
  grid-template-columns: 50px 1fr;
  gap: 18px;
  align-items: start;
}
.callout-num {
  width: 44px; height: 44px;
  border-radius: 50%;
  background: var(--indigo);
  color: var(--ink-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.5px;
}
.callout-head { font-size: 16px; font-weight: 700; color: var(--ink); }
.callout-body { font-size: 13px; font-style: italic; color: var(--muted); margin-top: 4px; line-height: 1.5; }

/* ============== Discussion =============== */
.discuss-frame {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 24px;
  height: 100%;
  align-items: center;
  padding: 0 32px 0 0;
}
.discuss-body { padding-left: 16px; }
.discuss-title {
  font-size: 64px;
  font-weight: 800;
  letter-spacing: -1.5px;
  margin: 16px 0 36px 0;
  color: var(--ink-light);
  line-height: 1.05;
}
.discuss-list { display: flex; flex-direction: column; gap: 24px; }
.discuss-row { display: grid; grid-template-columns: 60px 1fr; gap: 16px; align-items: start; }
.discuss-num {
  font-size: 22px;
  font-weight: 800;
  color: var(--amber);
  letter-spacing: -0.5px;
}
.discuss-q {
  font-size: 19px;
  color: var(--ink-light);
  line-height: 1.5;
}
.discuss-footer {
  margin-top: 36px;
  font-size: 12px;
  font-style: italic;
  color: var(--muted-2);
  letter-spacing: 0.5px;
}

/* ============== Nav UI =============== */
.nav-hint {
  position: fixed;
  bottom: 16px; left: 16px;
  background: rgba(15, 23, 41, 0.85);
  color: white;
  padding: 8px 14px;
  border-radius: 4px;
  font-size: 11px;
  font-family: 'SF Mono', monospace;
  letter-spacing: 0.5px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
}
.nav-hint.show { opacity: 1; }

.progress-bar {
  position: fixed;
  bottom: 0; left: 0;
  height: 3px;
  background: var(--amber);
  transition: width 0.3s ease;
  z-index: 100;
}

/* ============== Overview mode =============== */
body.overview .stage { display: block; padding: 24px; overflow: auto; background: #1a1a1f; }
body.overview .deck { display: grid; position: static; transform: none; width: auto; height: auto; grid-template-columns: repeat(4, 1fr); gap: 16px; }
body.overview .slide {
  position: relative;
  display: flex !important;
  width: 100%; height: 0;
  padding-bottom: 56.25%;
  transform: scale(1);
  cursor: pointer;
  border-radius: 6px;
  overflow: hidden;
  border: 2px solid transparent;
  transition: border-color 0.15s;
}
body.overview .slide:hover { border-color: var(--amber); }
body.overview .slide > * { transform: scale(0.32); transform-origin: top left; width: 312%; }

/* ============== Print =============== */
@media print {
  @page { size: 13.333in 7.5in; margin: 0; }
  body { background: white; }
  .stage { position: static; }
  .deck { width: 13.333in; height: auto; transform: none !important; }
  .slide {
    display: flex !important;
    page-break-after: always;
    width: 13.333in;
    height: 7.5in;
    position: relative;
  }
  .nav-hint, .progress-bar { display: none !important; }
}
"""


JS = """
(function(){
  const slides = Array.from(document.querySelectorAll('.slide'));
  const total = slides.length;
  const progress = document.querySelector('.progress-bar');
  const hint = document.querySelector('.nav-hint');
  let idx = 0;
  let hintTimer = null;

  function showHint(msg){
    hint.textContent = msg;
    hint.classList.add('show');
    clearTimeout(hintTimer);
    hintTimer = setTimeout(() => hint.classList.remove('show'), 1500);
  }

  function go(i){
    idx = Math.max(0, Math.min(total - 1, i));
    slides.forEach((s, k) => s.classList.toggle('active', k === idx));
    progress.style.width = ((idx + 1) / total * 100) + '%';
    location.hash = idx + 1;
    showHint((idx + 1) + ' / ' + total);
  }

  function fitDeck(){
    if (document.body.classList.contains('overview')) return;
    const deck = document.querySelector('.deck');
    if (!deck) return;
    const sx = window.innerWidth / 1280;
    const sy = window.innerHeight / 720;
    const s = Math.min(sx, sy);
    deck.style.transform = 'scale(' + s + ')';
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
      e.preventDefault(); go(idx + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault(); go(idx - 1);
    } else if (e.key === 'Home') {
      e.preventDefault(); go(0);
    } else if (e.key === 'End') {
      e.preventDefault(); go(total - 1);
    } else if (e.key === 'o' || e.key === 'Escape') {
      e.preventDefault();
      document.body.classList.toggle('overview');
      if (!document.body.classList.contains('overview')) fitDeck();
    } else if (e.key === 'f') {
      e.preventDefault();
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        document.exitFullscreen();
      }
    } else if (e.key === 'p') {
      e.preventDefault();
      window.print();
    }
  });

  document.addEventListener('click', (e) => {
    if (document.body.classList.contains('overview')) {
      const slide = e.target.closest('.slide');
      if (slide) {
        const i = slides.indexOf(slide);
        if (i >= 0) {
          document.body.classList.remove('overview');
          fitDeck();
          go(i);
        }
      }
    }
  });

  window.addEventListener('resize', fitDeck);

  // Initial
  const initial = parseInt(location.hash.slice(1), 10);
  go((initial && initial >= 1 && initial <= total) ? initial - 1 : 0);
  fitDeck();
})();
"""


def main():
    parts = []
    total = len(SLIDES)
    for i, data in enumerate(SLIDES, start=1):
        renderer = KIND[data["kind"]]
        if data["kind"] in ("cover", "discussion"):
            parts.append(renderer(data))
        else:
            parts.append(renderer(data, i, total))

    body = "\n".join(parts)
    page_title = f"{TITLE} · {SUBTITLE}"

    html_doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(page_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="stage">
  <div class="deck">
{body}
  </div>
</div>
<div class="nav-hint">1 / {total}</div>
<div class="progress-bar"></div>
<script>{JS}</script>
</body>
</html>
'''
    OUT.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {OUT} ({total} slides, {len(html_doc)//1024} KB)")


if __name__ == "__main__":
    main()
