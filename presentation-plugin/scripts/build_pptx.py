#!/usr/bin/env python3
"""Build an editable .pptx (with speaker notes) from a presentation Markdown file.

Usage: python3 build_pptx.py <presentation.md> [output.pptx] [--template template.pptx]

Reads only "## Slide N: Title" sections; everything else (Q&A prep, source table) is ignored.
Inside a section:
  - "- text" / "* text"   bullet
  - "1. text"             numbered line (kept as typed; used for the References slide)
  - "**Visual:** text"    goes into the speaker notes as a reminder
  - "**Notes ...:**"      everything after this line is the speaker notes
  - <sup>1,3</sup>        real superscript (Vancouver citations); *text* italic; **text** bold
  - a ```flow fenced block draws a left-to-right flowchart (boxes + arrows) instead of bullets;
    one chain per line, e.g. "Smoking -> Oxidative stress -> COPD"; repeat a label to branch or merge
  - "**Photo:** what to insert | source"  an empty, labelled photo slot on the right (bullets shrink to
    the left) with a caption underneath; up to two per slide; a slide with no bullets gets a large slot
Slide 1 uses the title layout: its bullets become subtitle lines.
Needs python-pptx (pip install python-pptx).
"""
import re
import sys

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

SLIDE_RE = re.compile(r"^##\s+Slide\s+\d+\s*[:.\-]\s*(.+?)\s*$", re.I)
NOTES_RE = re.compile(r"^\*\*(Notes|Speaker notes|Catatan pembicara)\b.*?\*\*\s*(.*)$", re.I)
PHOTO_RE = re.compile(r"^\*\*(Photo|Figure|Image|Gambar):?\*\*:?\s*(.*)$", re.I)
VISUAL_RE = re.compile(r"^\*\*Visual:?\*\*:?\s*(.*)$", re.I)
SOURCES_RE = re.compile(r"^\*\*(Sources?|Sumber):?\*\*", re.I)
BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")
NUMBERED_RE = re.compile(r"^\s*(\d+\.\s+.*)$")
CHECK = "[check in book]"
INLINE_RE = re.compile(r"(<sup>.*?</sup>|\*\*.+?\*\*|\*[^*]+?\*)")


def parse(md):
    slides, cur, in_notes, in_flow = [], None, False, False
    for line in md.splitlines():
        m = SLIDE_RE.match(line)
        if m:
            cur = {"title": m.group(1), "body": [], "notes": [], "visual": "", "flow": [], "photos": []}
            slides.append(cur)
            in_notes = in_flow = False
            continue
        if cur is None:
            continue
        if line.startswith("# ") or (line.startswith("## ") and not SLIDE_RE.match(line)):
            cur, in_notes = None, False  # a non-slide section ends the deck part
            continue
        if in_flow:
            if line.strip().startswith("```"):
                in_flow = False
            elif "->" in line:
                cur["flow"].append([n.strip() for n in line.split("->") if n.strip()])
            continue
        if line.strip().startswith("```flow"):
            in_flow = True
            continue
        if in_notes:
            cur["notes"].append(line)
            continue
        if (m := NOTES_RE.match(line)):
            in_notes = True
            if m.group(2):
                cur["notes"].append(m.group(2))
        elif (m := PHOTO_RE.match(line)):
            what, _, source = m.group(2).partition("|")
            cur["photos"].append((what.strip(), source.strip()))
        elif (m := VISUAL_RE.match(line)):
            cur["visual"] = m.group(1).strip()
        elif SOURCES_RE.match(line):
            pass  # citations are already superscripts on the bullets
        elif (m := BULLET_RE.match(line)):
            cur["body"].append(m.group(1).strip())
        elif (m := NUMBERED_RE.match(line)):
            cur["body"].append(m.group(1).strip())
    for s in slides:
        s["notes"] = "\n".join(s["notes"]).strip()
    return slides


def add_runs(paragraph, text):
    for part in INLINE_RE.split(text):
        if not part:
            continue
        run = paragraph.add_run()
        if part.startswith("<sup>"):
            run.text = part[5:-6]
            run.font._rPr.set("baseline", "30000")
        elif part.startswith("**") and part.endswith("**"):
            run.text, run.font.bold = part[2:-2], True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            run.text, run.font.italic = part[1:-1], True
        else:
            run.text = part


def fill(frame, lines, size=None):
    frame.clear()
    for i, line in enumerate(lines):
        p = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        add_runs(p, line)
        if NUMBERED_RE.match(line):  # typed number already; drop the layout's bullet glyph
            p._p.get_or_add_pPr().insert(0, p._p.makeelement(qn("a:buNone"), {}))
        if size:
            for r in p.runs:
                r.font.size = Pt(size)


def flow_layout(chains):
    """Column = longest path from a start node, outcomes last; rows follow parents' rows to limit crossings."""
    nodes, edges = [], []
    for chain in chains:
        for n in chain:
            if n not in nodes:
                nodes.append(n)
        edges += [(a, b) for a, b in zip(chain, chain[1:]) if (a, b) not in edges]
    level = {n: 0 for n in nodes}
    for _ in nodes:  # relax; a cycle just stops growing after len(nodes) passes
        for a, b in edges:
            if level[b] < level[a] + 1 <= len(nodes):
                level[b] = level[a] + 1
    last = max(level.values())
    for n in nodes:  # outcomes (no outgoing arrow) line up in the last column
        if not any(a == n for a, _ in edges):
            level[n] = last
    cols = [[n for n in nodes if level[n] == c] for c in range(last + 1)]
    row = {}
    for c, col in enumerate(cols):
        if c:
            def key(n):
                ps = [row[a] for a, b in edges if b == n and a in row]
                return sum(ps) / len(ps) if ps else 0
            col.sort(key=key)
        for i, n in enumerate(col):
            row[n] = (i + 0.5) / len(col)
    return cols, edges


def draw_flow(slide, prs, chains):
    cols, edges = flow_layout(chains)
    left, top = Inches(0.4), Inches(1.6)
    width, height = prs.slide_width - Inches(0.8), prs.slide_height - Inches(2.0)
    colw = width / len(cols)
    rowh = height / max(len(c) for c in cols)
    bw, bh = int(min(Inches(2.4), colw * 0.72)), int(min(Inches(1.0), rowh * 0.72))
    boxes = {}
    for c, col in enumerate(cols):
        for i, n in enumerate(col):
            cx = left + colw * (c + 0.5)
            cy = top + height * (i + 0.5) / len(col)
            box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                         Emu(int(cx - bw / 2)), Emu(int(cy - bh / 2)), Emu(bw), Emu(bh))
            tf = box.text_frame
            tf.word_wrap = True
            add_runs(tf.paragraphs[0], n)
            for r in tf.paragraphs[0].runs:
                r.font.size = Pt(16 if len(cols) <= 4 else 14)
            boxes[n] = box
    for a, b in edges:
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, 0, 0, 0, 0)
        line.begin_connect(boxes[a], 3)  # right side
        line.end_connect(boxes[b], 1)  # left side
        line.line.width = Pt(1.5)
        line.line._get_or_add_ln().append(line.line._ln.makeelement(qn("a:tailEnd"), {"type": "triangle"}))
        tree = slide.shapes._spTree  # send arrows behind the boxes so a long arrow never covers one
        tree.remove(line._element)
        tree.insert(3, line._element)


def draw_photo_slots(slide, prs, photos, full):
    """Dashed empty boxes to paste book figures into, each with an editable caption below."""
    W, H = prs.slide_width, prs.slide_height
    x0 = Inches(0.8) if full else int(W * 0.56)
    area_w = W - Inches(0.8) - x0 if full else W - Inches(0.5) - x0
    top, area_h = Inches(1.7), H - Inches(1.9)
    side_by_side = full and len(photos) == 2
    for k, (what, source) in enumerate(photos):
        if side_by_side:  # two slots next to each other on a photo-only slide
            width, left, y, slot_h = (area_w - Inches(0.4)) / 2, x0 + k * (area_w + Inches(0.4)) / 2, top, area_h - Inches(0.75)
        else:  # stacked in the right-hand column
            each = area_h / len(photos)
            width, left, y, slot_h = area_w, x0, top + each * k, each - Inches(0.75)
        slot_h = int(slot_h)
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(int(left)), Emu(int(y)), Emu(int(width)), Emu(slot_h))
        box.name = "Photo slot"
        box.fill.background()
        box.line.color.rgb = RGBColor(0x99, 0x99, 0x99)
        box.line.dash_style = MSO_LINE.DASH
        box.line.width = Pt(1.5)
        tf = box.text_frame
        tf.word_wrap = True
        tf.text = f"PHOTO SLOT\n{what}\n(delete this box and paste the figure)"
        for p in tf.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                r.font.size, r.font.italic = Pt(14), True
                r.font.color.rgb = RGBColor(0x77, 0x77, 0x77)
        cap = slide.shapes.add_textbox(Emu(int(left)), Emu(int(y + slot_h + Inches(0.05))), Emu(int(width)), Inches(0.6))
        cap.name = "Photo caption"
        cap.text_frame.word_wrap = True
        add_runs(cap.text_frame.paragraphs[0], f"{what}." + (f" Source: {source}" if source else ""))
        for r in cap.text_frame.paragraphs[0].runs:
            r.font.size = Pt(12)


def place_16x9(slide, is_title):
    """The built-in layouts are drawn for 4:3, so position the placeholders for 16:9 by hand."""
    boxes = ([(0.9, 2.2, 11.5, 1.6), (0.9, 4.0, 11.5, 1.6)] if is_title
             else [(0.6, 0.35, 12.1, 1.2), (0.6, 1.7, 12.1, 5.4)])
    for ph, (x, y, w, h) in zip(slide.placeholders, boxes):
        ph.left, ph.top, ph.width, ph.height = Inches(x), Inches(y), Inches(w), Inches(h)


def build(slides, out, template=None):
    prs = Presentation(template) if template else Presentation()
    if not template:  # python-pptx's built-in template is 4:3; make it 16:9
        prs.slide_width = Inches(13.333)
    title_layout, content_layout = prs.slide_layouts[0], prs.slide_layouts[1]
    for i, s in enumerate(slides):
        is_title = i == 0
        layout = title_layout if is_title else prs.slide_layouts[5] if s["flow"] else content_layout
        slide = prs.slides.add_slide(layout)
        if not template:
            place_16x9(slide, is_title)
        fill(slide.shapes.title.text_frame, [s["title"]])
        if s["flow"]:
            draw_flow(slide, prs, s["flow"])
        elif s["body"] and len(slide.placeholders) > 1:
            is_refs = re.match(r"(references|daftar pustaka|bibliography)", s["title"], re.I)
            body = slide.placeholders[1]
            fill(body.text_frame, s["body"], 16 if is_refs else None)
            if s["photos"]:
                body.width = int(prs.slide_width * 0.53) - body.left
                for p in body.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.size = r.font.size or Pt(24)
        elif len(slide.placeholders) > 1:
            slide.placeholders[1]._element.getparent().remove(slide.placeholders[1]._element)
        checks = [w for w, src in s["photos"] if CHECK in src]
        if s["photos"] and not is_title:
            photos = [(w, src.replace(CHECK, "").strip()) for w, src in s["photos"][:2]]
            draw_photo_slots(slide, prs, photos, full=not s["body"] or bool(s["flow"]))
        notes = s["notes"]
        if checks:  # keep the reminder off the slide, in the notes
            notes = f"[Check in your book before presenting: {'; '.join(checks)}]\n\n{notes}".strip()
        if s["visual"] and s["visual"].lower() not in ("none", "-"):
            notes = f"[Visual: {s['visual']}]\n\n{notes}".strip()
        if notes:
            slide.notes_slide.notes_text_frame.text = notes
    prs.save(out)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    template = argv[argv.index("--template") + 1] if "--template" in argv else None
    if template in args:
        args.remove(template)
    if not args:
        sys.exit(__doc__)
    src = args[0]
    out = args[1] if len(args) > 1 else re.sub(r"\.md$", "", src) + ".pptx"
    slides = parse(open(src, encoding="utf-8").read())
    if not slides:
        sys.exit("No '## Slide N: Title' sections found.")
    build(slides, out, template)
    print(f"Wrote {out} ({len(slides)} slides)")


if __name__ == "__main__":
    main(sys.argv[1:])
