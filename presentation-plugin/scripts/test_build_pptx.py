"""Self-check for build_pptx.py: python3 test_build_pptx.py"""
import os
import tempfile

from pptx import Presentation
from pptx.util import Inches

from build_pptx import build, flow_layout, parse

MD = """# Deck
## Slide 1: Title
- Presenter
**Notes (~10 s):**
Hello.
## Slide 2: Point
- Fact<sup>1,2</sup> about *E. coli*
**Visual:** chart
**Photo:** Emphysema histology | Robbins, ch. 15<sup>2</sup> [check in book]
**Notes (~30 s):**
Line one.
Line two.
## Slide 3: Framework
```flow
Smoking -> Oxidative stress -> COPD
Smoking -> Atherosclerosis
Oxidative stress -> Atherosclerosis
```
## Slide 4: References
1. Ref one.
# Q&A prep
- not a slide
"""

slides = parse(MD)
assert [s["title"] for s in slides] == ["Title", "Point", "Framework", "References"], slides
assert slides[1]["notes"] == "Line one.\nLine two." and slides[1]["visual"] == "chart"
assert slides[3]["body"] == ["1. Ref one."]
assert len(slides[2]["flow"]) == 3 and not slides[2]["body"]
cols, edges = flow_layout(slides[2]["flow"])
assert cols == [["Smoking"], ["Oxidative stress"], ["COPD", "Atherosclerosis"]] and len(edges) == 4, cols

out = os.path.join(tempfile.mkdtemp(), "t.pptx")
build(slides, out)
prs = Presentation(out)
runs = prs.slides[1].placeholders[1].text_frame.paragraphs[0].runs
assert [(r.text, r.font._rPr.get("baseline"), r.font.italic) for r in runs] == [
    ("Fact", None, None), ("1,2", "30000", None), (" about ", None, None), ("E. coli", None, True)]
assert prs.slides[1].notes_slide.notes_text_frame.text.count("[Visual: chart]") == 1
shapes = prs.slides[2].shapes
assert sum(sh.shape_type == 9 or "Connector" in sh.name for sh in shapes) == 4  # arrows
assert {sh.text_frame.text for sh in shapes if sh.has_text_frame} >= {"Smoking", "COPD"}
assert flow_layout([["A", "B", "C", "D"], ["A", "E"]])[0][-1] == ["D", "E"]  # outcomes in last column
assert prs.slide_width == Inches(13.333)
assert slides[1]["photos"] == [("Emphysema histology", "Robbins, ch. 15<sup>2</sup> [check in book]")]
names = [sh.name for sh in prs.slides[1].shapes]
assert "Photo slot" in names and "Photo caption" in names
body = prs.slides[1].placeholders[1]
cap = next(sh for sh in prs.slides[1].shapes if sh.name == "Photo caption").text_frame.text
assert "check in book" not in cap and "check in your book" in prs.slides[1].notes_slide.notes_text_frame.text.lower()
assert body.left + body.width <= prs.slide_width * 0.56  # bullets moved left of the slot
print("ok")
