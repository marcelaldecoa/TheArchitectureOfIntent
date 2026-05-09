"""
Build the modern teaching deck (PPTX).

Output: paper/architecture-of-intent.pptx
Design: 16:9 widescreen, off-white background, indigo + amber accents,
generous whitespace, asymmetric layouts, native python-pptx shapes
plus the two SVG-derived figure PNGs.
"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

from presentation_content import SLIDES, PALETTE, TITLE, SUBTITLE, AUTHOR, YEAR, PAPER_KIND


HERE = Path(__file__).resolve().parent
FIG_DIR = HERE / "figures"
OUT = HERE / "architecture-of-intent.pptx"


def hx(name):
    h = PALETTE[name].lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# Convenience colour aliases
BG       = hx("bg")
INK      = hx("ink")
INK_LT   = hx("ink_light")
MUTED    = hx("muted")
MUTED2   = hx("muted_2")
RULE     = hx("rule")
CARD     = hx("card")
INDIGO   = hx("indigo")
INDIGO_D = hx("indigo_dark")
AMBER    = hx("amber")
AMBER_PA = hx("amber_pale")
AMBER_D  = hx("amber_dark")
EMERALD  = hx("emerald")
EMERALD_D= hx("emerald_dark")
ROSE     = hx("rose")
ROSE_D   = hx("rose_dark")
DARK     = hx("bg_dark")

ACCENTS = {"indigo": INDIGO, "amber": AMBER, "emerald": EMERALD,
           "rose": ROSE, "muted": MUTED}


# ========================================================================
# Helpers
# ========================================================================

def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, left, top, width, height, fill=None, line=None,
             line_w=Pt(1), shadow=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    if fill is not None:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = line_w
    if not shadow:
        # Remove shadow effect
        spPr = shp.fill._xPr  # shape properties
        for el in spPr.findall(qn("a:effectLst")):
            spPr.remove(el)
        spPr.append(etree.fromstring(
            '<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
    return shp


def add_round(slide, left, top, width, height, fill=None, line=None,
              line_w=Pt(1), corner=0.06):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top,
                                 width, height)
    # adjust corner radius
    shp.adjustments[0] = corner
    if fill is not None:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = line_w
    return shp


def add_line(slide, x1, y1, x2, y2, color=RULE, width=Pt(1)):
    line = slide.shapes.add_connector(1, x1, y1, x2, y2)
    line.line.color.rgb = color
    line.line.width = width
    return line


def add_text(slide, left, top, width, height, text, *,
             size=18, bold=False, color=INK, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, italic=False, font="Calibri",
             tracking=None):
    """Add a text box. `text` may be a single string (newlines split into
    paragraphs) or a list of (text, kwargs-dict) tuples for inline runs
    on a single line. Returns the textbox shape."""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.02)
    tf.margin_top = tf.margin_bottom = Inches(0.02)

    if isinstance(text, str):
        lines = text.split("\n")
        for i, line in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            run = p.add_run()
            run.text = line
            f = run.font
            f.size = Pt(size)
            f.bold = bold
            f.italic = italic
            f.color.rgb = color
            f.name = font
            if tracking is not None:
                # spc unit = 1/100 pt, character spacing
                run._r.get_or_add_rPr().set("spc", str(int(tracking * 100)))
    else:
        # Single paragraph with multiple runs
        p = tf.paragraphs[0]
        p.alignment = align
        for run_text, run_kwargs in text:
            run = p.add_run()
            run.text = run_text
            f = run.font
            f.size = Pt(run_kwargs.get("size", size))
            f.bold = run_kwargs.get("bold", bold)
            f.italic = run_kwargs.get("italic", italic)
            f.color.rgb = run_kwargs.get("color", color)
            f.name = run_kwargs.get("font", font)
    return tb


def eyebrow(slide, x, y, w, label, color=INDIGO):
    """Small uppercase tracked label."""
    add_text(slide, x, y, w, Inches(0.32), label,
             size=11, bold=True, color=color, font="Calibri",
             tracking=2)


def section_chip(slide, label):
    """Top-left section chip."""
    add_rect(slide, Inches(0.7), Inches(0.55), Inches(0.16), Inches(0.16),
             fill=AMBER)
    eyebrow(slide, Inches(0.95), Inches(0.5), Inches(8), label, color=MUTED)


def page_footer(slide, page, total):
    add_text(slide, Inches(0.7), Inches(7.05), Inches(8), Inches(0.32),
             f"{TITLE}  ·  {AUTHOR}, {YEAR}",
             size=9, color=MUTED2, tracking=1)
    add_text(slide, Inches(11.5), Inches(7.05), Inches(1.13), Inches(0.32),
             f"{page:02d} / {total:02d}",
             size=9, color=MUTED2, align=PP_ALIGN.RIGHT, tracking=1)


def slide_title(slide, title, tagline=None,
                title_size=34, tag_size=14,
                title_y=1.05, tag_y=1.85):
    """Standard headline + tagline block."""
    add_text(slide, Inches(0.7), Inches(title_y), Inches(12), Inches(0.8),
             title, size=title_size, bold=True, color=INK)
    if tagline:
        add_text(slide, Inches(0.7), Inches(tag_y), Inches(12), Inches(0.7),
                 tagline, size=tag_size, italic=True, color=MUTED)


# ========================================================================
# Slide builders
# ========================================================================

def s_cover(prs, data):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, DARK)

    # Vertical accent
    add_rect(s, Inches(0.7), Inches(2.5), Inches(0.12), Inches(2.6),
             fill=AMBER)

    # Eyebrow
    add_text(s, Inches(1.05), Inches(2.5), Inches(8), Inches(0.4),
             data["eyebrow"], size=12, bold=True, color=AMBER, tracking=3)

    # Title (allow wrapping for long titles)
    add_text(s, Inches(1.05), Inches(2.85), Inches(11), Inches(1.4),
             data["title"], size=54, bold=True, color=INK_LT)

    # Subtitle
    add_text(s, Inches(1.05), Inches(4.2), Inches(11), Inches(0.7),
             data["subtitle"], size=22, italic=True, color=MUTED2)

    # Author + year + paper kind
    add_text(s, Inches(1.05), Inches(5.1), Inches(11), Inches(0.4),
             f"{data['author']}    ·    {data['year']}",
             size=16, color=INK_LT, tracking=1)
    add_text(s, Inches(1.05), Inches(5.5), Inches(11), Inches(0.4),
             data["note"], size=12, color=MUTED2, italic=True)

    # Bottom-right tag
    add_text(s, Inches(8.5), Inches(7.05), Inches(4.13), Inches(0.32),
             "TEACHING DECK  ·  COMPANION TO THE PAPER",
             size=10, color=MUTED2, align=PP_ALIGN.RIGHT, tracking=2.5)


def s_roadmap(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])
    slide_title(s, data["title"])

    y0 = Inches(2.55)
    row_h = Inches(0.85)
    for i, (num, head, sub) in enumerate(data["items"]):
        y = y0 + i * row_h
        # number
        add_text(s, Inches(0.7), y, Inches(1.1), row_h,
                 num, size=36, bold=True, color=INDIGO,
                 anchor=MSO_ANCHOR.MIDDLE)
        # divider line
        add_line(s, Inches(1.85), y + Inches(0.15),
                 Inches(1.85), y + row_h - Inches(0.15),
                 color=RULE, width=Pt(1))
        # heading
        add_text(s, Inches(2.05), y + Inches(0.05), Inches(10), Inches(0.42),
                 head, size=20, bold=True, color=INK)
        # sub
        add_text(s, Inches(2.05), y + Inches(0.45), Inches(10), Inches(0.4),
                 sub, size=13, color=MUTED, italic=True)

    page_footer(s, page, total)


def s_quote(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])

    # Decorative oversized quote mark
    add_text(s, Inches(0.7), Inches(1.4), Inches(2), Inches(2),
             "“", size=200, bold=True, color=INDIGO, font="Georgia")

    # Headline (the bold claim)
    add_text(s, Inches(2.5), Inches(2.0), Inches(10), Inches(1.0),
             data["headline"],
             size=40, bold=True, color=INK)

    # Body
    add_text(s, Inches(2.5), Inches(3.2), Inches(10), Inches(1.5),
             "\n".join(data["body"]),
             size=22, italic=True, color=MUTED)

    # Footnote
    add_rect(s, Inches(0.7), Inches(5.7), Inches(11.93), Inches(1.05),
             fill=CARD, line=RULE)
    add_text(s, Inches(0.95), Inches(5.85), Inches(11.43), Inches(0.85),
             data["footnote"], size=13, color=INK)

    page_footer(s, page, total)


def s_compare(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])
    slide_title(s, data["title"], data["tagline"])

    col_w = Inches(5.95)
    col_h = Inches(4.3)
    y0    = Inches(2.55)
    gap   = Inches(0.13)

    # Left card
    left_color = ACCENTS[data["left"]["color"]]
    add_round(s, Inches(0.7), y0, col_w, col_h,
              fill=CARD, line=RULE, line_w=Pt(1), corner=0.05)
    add_rect(s, Inches(0.7), y0, Inches(0.18), col_h, fill=left_color)
    eyebrow(s, Inches(1.0), y0 + Inches(0.35), col_w - Inches(0.6),
            data["left"]["label"], color=left_color)
    for i, item in enumerate(data["left"]["items"]):
        add_text(s, Inches(1.0), y0 + Inches(0.85 + i * 0.65),
                 col_w - Inches(0.4), Inches(0.6),
                 [
                    ("•   ", {"color": left_color, "bold": True, "size": 16}),
                    (item, {"color": INK, "size": 14}),
                 ])

    # Right card
    right_color = ACCENTS[data["right"]["color"]]
    add_round(s, Inches(0.7) + col_w + gap, y0, col_w, col_h,
              fill=CARD, line=RULE, line_w=Pt(1), corner=0.05)
    add_rect(s, Inches(0.7) + col_w + gap, y0, Inches(0.18), col_h,
             fill=right_color)
    eyebrow(s, Inches(0.7) + col_w + gap + Inches(0.3),
            y0 + Inches(0.35), col_w - Inches(0.6),
            data["right"]["label"], color=right_color)
    for i, item in enumerate(data["right"]["items"]):
        add_text(s, Inches(0.7) + col_w + gap + Inches(0.3),
                 y0 + Inches(0.85 + i * 0.65),
                 col_w - Inches(0.4), Inches(0.6),
                 [
                    ("•   ", {"color": right_color, "bold": True, "size": 16}),
                    (item, {"color": INK, "size": 14}),
                 ])

    page_footer(s, page, total)


def s_cards4(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])
    slide_title(s, data["title"], data["tagline"], title_size=30, tag_size=13)

    # 4 cards in a row
    n = len(data["cards"])
    total_w = Inches(11.93)
    gap = Inches(0.18)
    card_w = (total_w - gap * (n - 1)) / n
    y0 = Inches(2.85)
    h  = Inches(4.0)

    for i, card in enumerate(data["cards"]):
        left = Inches(0.7) + (card_w + gap) * i
        # Determine if this is the (eyebrow,body) or (number,head,body,extra)
        # tuple form
        num = head = body = extra = ""
        color = INDIGO
        if len(card) == 5:
            num, head, body, extra, color_name = card
            color = ACCENTS[color_name]
        elif len(card) == 4:
            num, head, body, extra = card
        elif len(card) == 3:
            head, body, extra = card

        # Card background
        add_round(s, left, y0, card_w, h, fill=CARD, line=RULE,
                  line_w=Pt(1), corner=0.04)
        # Top accent bar
        add_rect(s, left, y0, card_w, Inches(0.12), fill=color)

        # Number / label area
        if num:
            add_text(s, left + Inches(0.25), y0 + Inches(0.35),
                     card_w - Inches(0.5), Inches(0.55),
                     num, size=28, bold=True, color=color)
        # Heading
        add_text(s, left + Inches(0.25), y0 + Inches(1.05),
                 card_w - Inches(0.5), Inches(0.5),
                 head, size=14, bold=True, color=INK, tracking=2)
        # Body
        add_text(s, left + Inches(0.25), y0 + Inches(1.6),
                 card_w - Inches(0.5), Inches(1.2),
                 body, size=14, color=INK, italic=True)
        # Extra
        if extra:
            add_text(s, left + Inches(0.25), y0 + Inches(2.85),
                     card_w - Inches(0.5), Inches(1.0),
                     extra, size=11, color=MUTED)

    page_footer(s, page, total)


def s_table(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])
    slide_title(s, data["title"], data["tagline"], title_size=30, tag_size=13)

    cols = len(data["headers"])
    # Column widths
    if cols == 3:
        col_widths = [Inches(2.4), Inches(4.3), Inches(5.2)]
    else:
        each = Inches(11.9 / cols)
        col_widths = [each] * cols
    col_x = [Inches(0.7)]
    for w in col_widths[:-1]:
        col_x.append(col_x[-1] + w)

    y0 = Inches(2.7)
    header_h = Inches(0.55)
    row_h = Inches(0.62)

    # Header row
    add_rect(s, Inches(0.7), y0, sum(col_widths, Inches(0)), header_h,
             fill=DARK)
    for i, h in enumerate(data["headers"]):
        add_text(s, col_x[i] + Inches(0.2), y0,
                 col_widths[i] - Inches(0.4), header_h,
                 h, size=13, bold=True, color=INK_LT,
                 anchor=MSO_ANCHOR.MIDDLE, tracking=2)

    # Data rows
    for r, row in enumerate(data["rows"]):
        y = y0 + header_h + r * row_h
        if r % 2 == 0:
            add_rect(s, Inches(0.7), y, sum(col_widths, Inches(0)),
                     row_h, fill=CARD)
        for i, cell in enumerate(row):
            color = INDIGO if i == 0 else INK
            bold = (i == 0)
            add_text(s, col_x[i] + Inches(0.2), y,
                     col_widths[i] - Inches(0.4), row_h,
                     cell, size=13, bold=bold, color=color,
                     anchor=MSO_ANCHOR.MIDDLE)

    page_footer(s, page, total)


def s_figure(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])
    slide_title(s, data["title"], data["tagline"], title_size=28, tag_size=12)

    img_path = FIG_DIR / data["image"]
    if img_path.exists():
        # Center the image; cap by both width and height
        # Compute fit: max width 11.5", max height 4.0"
        from PIL import Image
        with Image.open(img_path) as im:
            iw, ih = im.size
        max_w = Inches(11.5)
        max_h = Inches(4.0)
        # scale
        scale = min(max_w.emu / (iw * 9525), max_h.emu / (ih * 9525))
        w = Emu(int(iw * 9525 * scale))
        h = Emu(int(ih * 9525 * scale))
        left = Emu((Inches(13.333).emu - w) // 2)
        top = Inches(2.6)
        s.shapes.add_picture(str(img_path), left, top, width=w, height=h)

    add_text(s, Inches(0.7), Inches(6.7), Inches(11.93), Inches(0.35),
             data["caption"], size=11, italic=True, color=MUTED,
             align=PP_ALIGN.CENTER)

    page_footer(s, page, total)


def s_taxonomy(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])
    slide_title(s, data["title"], data["tagline"], title_size=28, tag_size=12)

    headers = ["#", "Name", "Failure shape", "Fix locus"]
    col_w = [Inches(0.95), Inches(1.65), Inches(4.55), Inches(4.78)]
    col_x = [Inches(0.7)]
    for w in col_w[:-1]:
        col_x.append(col_x[-1] + w)

    y0 = Inches(2.65)
    header_h = Inches(0.5)
    row_h = Inches(0.55)

    # Header row
    add_rect(s, Inches(0.7), y0, sum(col_w, Inches(0)), header_h, fill=DARK)
    for i, h in enumerate(headers):
        add_text(s, col_x[i] + Inches(0.2), y0,
                 col_w[i] - Inches(0.4), header_h,
                 h, size=12, bold=True, color=INK_LT,
                 anchor=MSO_ANCHOR.MIDDLE, tracking=2)

    for r, row in enumerate(data["rows"]):
        cat_id, name, shape, fix, is_novel = row
        y = y0 + header_h + r * row_h
        bg_fill = AMBER_PA if is_novel else (CARD if r % 2 == 0 else BG)
        add_rect(s, Inches(0.7), y, sum(col_w, Inches(0)), row_h, fill=bg_fill)
        if is_novel:
            add_rect(s, Inches(0.7), y, Inches(0.08), row_h, fill=AMBER)
        cells = [cat_id, name, shape, fix]
        for i, cell in enumerate(cells):
            color = AMBER_D if (is_novel and i <= 1) else (INDIGO if i <= 1 else INK)
            bold = (i <= 1)
            add_text(s, col_x[i] + Inches(0.2), y,
                     col_w[i] - Inches(0.4), row_h,
                     cell, size=12, bold=bold, color=color,
                     anchor=MSO_ANCHOR.MIDDLE)

    page_footer(s, page, total)


def s_cat7(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])

    # Big amber title
    add_text(s, Inches(0.7), Inches(1.05), Inches(12), Inches(0.8),
             data["title"], size=40, bold=True, color=AMBER_D)
    # Tagline
    add_text(s, Inches(0.7), Inches(1.95), Inches(12), Inches(0.7),
             data["tagline"], size=14, italic=True, color=MUTED)

    # Left: 4 sub-categories
    eyebrow(s, Inches(0.7), Inches(2.85), Inches(6),
            "FOUR SUB-CATEGORIES", color=INK)
    for i, (name, fix) in enumerate(data["subs"]):
        y = Inches(3.25 + i * 0.78)
        add_round(s, Inches(0.7), y, Inches(6.0), Inches(0.65),
                  fill=CARD, line=RULE, line_w=Pt(1), corner=0.1)
        add_rect(s, Inches(0.7), y, Inches(0.12), Inches(0.65), fill=AMBER)
        add_text(s, Inches(0.95), y, Inches(2.3), Inches(0.65),
                 name, size=14, bold=True, color=INK,
                 anchor=MSO_ANCHOR.MIDDLE)
        add_line(s, Inches(3.25), y + Inches(0.12),
                 Inches(3.25), y + Inches(0.53),
                 color=RULE, width=Pt(1))
        add_text(s, Inches(3.4), y, Inches(3.2), Inches(0.65),
                 fix, size=12, color=AMBER_D,
                 anchor=MSO_ANCHOR.MIDDLE, italic=True)

    # Right: why a separate category
    rx = Inches(7.0)
    eyebrow(s, rx, Inches(2.85), Inches(6),
            "WHY A SEPARATE CATEGORY", color=INK)
    for i, line in enumerate(data["why"]):
        y = Inches(3.25 + i * 0.78)
        add_text(s, rx, y, Inches(0.3), Inches(0.4),
                 "■", size=14, bold=True, color=AMBER)
        add_text(s, rx + Inches(0.4), y, Inches(5.6), Inches(0.78),
                 line, size=13, color=INK)

    page_footer(s, page, total)


def s_split_list(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])
    slide_title(s, data["title"], data["tagline"], title_size=28, tag_size=12)

    use_amber = data.get("use_amber", False)
    accent = AMBER if use_amber else INDIGO

    # Two columns
    eyebrow(s, Inches(0.7), Inches(2.7), Inches(6),
            data["left_title"].upper(), color=accent)
    items = data["left_items"]
    if items and isinstance(items[0], tuple):
        for i, (head, sub) in enumerate(items):
            y = Inches(3.1 + i * 0.7)
            add_text(s, Inches(0.7), y, Inches(0.3), Inches(0.5),
                     "■", size=14, bold=True, color=accent)
            add_text(s, Inches(1.0), y, Inches(5.2), Inches(0.4),
                     head, size=14, bold=True, color=INK)
            add_text(s, Inches(1.0), y + Inches(0.32), Inches(5.2),
                     Inches(0.4), sub, size=12, color=MUTED, italic=True)
    else:
        # plain list, two columns inside
        for i, line in enumerate(items):
            col = i % 2
            row = i // 2
            x = Inches(0.7 + col * 3.05)
            y = Inches(3.1 + row * 0.45)
            add_text(s, x, y, Inches(3), Inches(0.4),
                     "·  " + line, size=12, color=INK)

    # Right column
    rx = Inches(7.0)
    eyebrow(s, rx, Inches(2.7), Inches(6),
            data["right_title"].upper(), color=accent)
    items_r = data["right_items"]
    for i, item in enumerate(items_r):
        y = Inches(3.1 + i * 0.7)
        add_text(s, rx, y, Inches(0.3), Inches(0.5),
                 "■", size=14, bold=True, color=accent)
        if isinstance(item, tuple):
            head, sub = item
            add_text(s, rx + Inches(0.3), y, Inches(5.5), Inches(0.4),
                     head, size=14, bold=True, color=INK)
            add_text(s, rx + Inches(0.3), y + Inches(0.32), Inches(5.5),
                     Inches(0.4), sub, size=12, color=MUTED, italic=True)
        else:
            add_text(s, rx + Inches(0.3), y, Inches(5.5), Inches(0.4),
                     item, size=14, color=INK)

    page_footer(s, page, total)


def s_callout_list(prs, data, page, total):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, BG)
    section_chip(s, data["section"])
    slide_title(s, data["title"], data["tagline"], title_size=28, tag_size=12)

    y0 = Inches(2.75)
    row_h = Inches(0.78)
    n = len(data["items"])
    for i, (head, body) in enumerate(data["items"]):
        y = y0 + i * row_h
        # number badge
        add_round(s, Inches(0.7), y, Inches(0.65), Inches(0.65),
                  fill=INDIGO, line=INDIGO, corner=0.5)
        add_text(s, Inches(0.7), y, Inches(0.65), Inches(0.65),
                 f"{i+1:02d}", size=14, bold=True, color=INK_LT,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # head
        add_text(s, Inches(1.55), y - Inches(0.02), Inches(11), Inches(0.4),
                 head, size=15, bold=True, color=INK)
        # body
        add_text(s, Inches(1.55), y + Inches(0.32), Inches(11), Inches(0.4),
                 body, size=12, color=MUTED, italic=True)

    page_footer(s, page, total)


def s_discussion(prs, data):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(s, DARK)

    add_rect(s, Inches(0.7), Inches(1.5), Inches(0.12), Inches(2.0), fill=AMBER)
    eyebrow(s, Inches(1.05), Inches(1.5), Inches(8),
            data["section"], color=AMBER)
    add_text(s, Inches(1.05), Inches(1.85), Inches(11), Inches(1.0),
             data["title"], size=46, bold=True, color=INK_LT)

    for i, q in enumerate(data["questions"]):
        y = Inches(3.7 + i * 0.85)
        add_text(s, Inches(1.05), y, Inches(0.7), Inches(0.6),
                 f"{i+1:02d}", size=22, bold=True, color=AMBER)
        add_text(s, Inches(1.85), y, Inches(11), Inches(0.7),
                 q, size=18, color=INK_LT)

    add_text(s, Inches(1.05), Inches(6.85), Inches(11), Inches(0.35),
             data["footer"], size=11, italic=True, color=MUTED2)


# ========================================================================
# Build
# ========================================================================

KIND_TO_BUILDER = {
    "cover": s_cover,
    "roadmap": s_roadmap,
    "quote": s_quote,
    "compare": s_compare,
    "cards4": s_cards4,
    "table": s_table,
    "figure": s_figure,
    "taxonomy": s_taxonomy,
    "cat7": s_cat7,
    "split_list": s_split_list,
    "callout_list": s_callout_list,
    "discussion": s_discussion,
}


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    total = len(SLIDES)
    for i, data in enumerate(SLIDES, start=1):
        builder = KIND_TO_BUILDER[data["kind"]]
        if data["kind"] in ("cover", "discussion"):
            builder(prs, data)
        else:
            builder(prs, data, i, total)

    prs.save(OUT)
    print(f"Wrote {OUT} ({total} slides)")


if __name__ == "__main__":
    main()
