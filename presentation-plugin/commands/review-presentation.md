---
description: Review a presentation for invented facts, wrong references, AI-style writing, and rubric and timing fit
argument-hint: "<presentation .md or .pptx> [rubric or brief]"
---

Review the presentation at: $ARGUMENTS

If it's a .pptx, extract the slide text and speaker notes first (python-pptx) into a Markdown file in the skill's slide format. Hand the file and any brief or rubric to the `presentation-reviewer` agent. Report its findings in its order: serious problems, can't check, AI writing, rubric and timing, top fixes.

Don't edit the presentation unless the user asks. If they do, apply only the fixes they approve, and rebuild the .pptx with `scripts/build_pptx.py` if the source was Markdown.
