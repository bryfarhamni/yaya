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
Slide 1 uses the title layout: its bullets become subtitle lines.
Needs python-pptx (pip install python-pptx).
"""
import re
import sys

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Pt

SLIDE_RE = re.compile(r"^##\s+Slide\s+\d+\s*[:.\-]\s*(.+?)\s*$", re.I)
NOTES_RE = re.compile(r"^\*\*(Notes|Speaker notes|Catatan pembicara)\b.*?\*\*\s*(.*)$", re.I)
VISUAL_RE = re.compile(r"^\*\*Visual:?\*\*:?\s*(.*)$", re.I)
SOURCES_RE = re.compile(r"^\*\*(Sources?|Sumber):?\*\*", re.I)
BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")
NUMBERED_RE = re.compile(r"^\s*(\d+\.\s+.*)$")
INLINE_RE = re.compile(r"(<sup>.*?</sup>|\*\*.+?\*\*|\*[^*]+?\*)")


def parse(md):
    slides, cur, in_notes = [], None, False
    for line in md.splitlines():
        m = SLIDE_RE.match(line)
        if m:
            cur = {"title": m.group(1), "body": [], "notes": [], "visual": ""}
            slides.append(cur)
            in_notes = False
            continue
        if cur is None:
            continue
        if line.startswith("# ") or (line.startswith("## ") and not SLIDE_RE.match(line)):
            cur, in_notes = None, False  # a non-slide section ends the deck part
            continue
        if in_notes:
            cur["notes"].append(line)
            continue
        if (m := NOTES_RE.match(line)):
            in_notes = True
            if m.group(2):
                cur["notes"].append(m.group(2))
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


def build(slides, out, template=None):
    prs = Presentation(template) if template else Presentation()
    title_layout, content_layout = prs.slide_layouts[0], prs.slide_layouts[1]
    for i, s in enumerate(slides):
        is_title = i == 0
        slide = prs.slides.add_slide(title_layout if is_title else content_layout)
        fill(slide.shapes.title.text_frame, [s["title"]])
        if s["body"] and len(slide.placeholders) > 1:
            is_refs = re.match(r"(references|daftar pustaka|bibliography)", s["title"], re.I)
            fill(slide.placeholders[1].text_frame, s["body"], 14 if is_refs else None)
        notes = s["notes"]
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
