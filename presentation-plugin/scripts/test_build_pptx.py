"""Self-check for build_pptx.py: python3 test_build_pptx.py"""
import os
import tempfile

from pptx import Presentation

from build_pptx import build, parse

MD = """# Deck
## Slide 1: Title
- Presenter
**Notes (~10 s):**
Hello.
## Slide 2: Point
- Fact<sup>1,2</sup> about *E. coli*
**Visual:** chart
**Notes (~30 s):**
Line one.
Line two.
## Slide 3: References
1. Ref one.
# Q&A prep
- not a slide
"""

slides = parse(MD)
assert [s["title"] for s in slides] == ["Title", "Point", "References"], slides
assert slides[1]["notes"] == "Line one.\nLine two." and slides[1]["visual"] == "chart"
assert slides[2]["body"] == ["1. Ref one."]

out = os.path.join(tempfile.mkdtemp(), "t.pptx")
build(slides, out)
prs = Presentation(out)
runs = prs.slides[1].placeholders[1].text_frame.paragraphs[0].runs
assert [(r.text, r.font._rPr.get("baseline"), r.font.italic) for r in runs] == [
    ("Fact", None, None), ("1,2", "30000", None), (" about ", None, None), ("E. coli", None, True)]
assert prs.slides[1].notes_slide.notes_text_frame.text.startswith("[Visual: chart]")
print("ok")
