# presentation-plugin

A Claude Code plugin for presentation assignments. Give it the brief (topic, length, language, rubric) and it produces a researched outline, slides with speaker notes, a review for invented facts, wrong references, and AI-style writing, and an editable PowerPoint file.

Defaults: English, literature review, textbooks as main sources, Vancouver superscript citations, .pptx output. The brief can change any of them.

## Contents

| Type | Name | Purpose |
|---|---|---|
| Skill | `presentation-assignment` | The workflow: brief → research → outline → slides and notes → review → .pptx |
| Command | `/make-presentation [brief file or topic]` | Runs the whole workflow |
| Command | `/review-presentation <file> [rubric]` | Reviews an existing .md or .pptx presentation |
| Agent | `presentation-reviewer` | Read-only: verifies books, articles, and claims; flags AI patterns; checks rubric and timing |
| Script | `scripts/build_pptx.py` | Turns the slide Markdown into a 16:9 .pptx with speaker notes, real superscript citations, and editable flowcharts for framework slides |

An example deck is in `examples/sample-smoking-presentation.md`.

References in `skills/presentation-assignment/references/`:
- `brief-template.md`: the brief to fill in
- `rubric.md`: the default rubric (edit it to match your course)
- `ai-writing-patterns.md`: patterns the reviewer flags

## Building a deck by hand

```
pip install python-pptx
python3 presentation-plugin/scripts/build_pptx.py presentation-topic.md [out.pptx] [--template my-template.pptx]
```

## Installation

```
/plugin marketplace add bryfarhamni/yaya
/plugin install presentation-plugin@yaya
```

For local testing: `claude --plugin-dir ./presentation-plugin`.
