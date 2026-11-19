# presentation-plugin

A Claude Code plugin for presentation assignments. Give it the brief (topic, length, language, rubric) and it produces a researched outline, slide content with speaker notes, and a review that checks for invented facts, citations that don't exist, and AI-style writing.

## Contents

| Type | Name | Purpose |
|---|---|---|
| Skill | `presentation-assignment` | The workflow: brief → research → outline → slides and notes → review |
| Command | `/make-presentation [brief file or topic]` | Runs the whole workflow and saves `presentasi-<topik>.md` |
| Command | `/review-presentation <file> [rubric]` | Reviews an existing presentation |
| Agent | `presentation-reviewer` | Read-only reviewer: verifies citations and claims, flags AI patterns, checks rubric and timing |

References in `skills/presentation-assignment/references/`:
- `brief-template.md`: the brief to fill in, and a default rubric
- `ai-writing-patterns.md`: patterns the reviewer flags, in English and Bahasa Indonesia

## Output shape

Each slide comes as a title, 3–5 short bullets, a visual suggestion, its sources, and timed speaker notes, followed by a numbered reference list and five likely Q&A questions with answers. Paste it into PowerPoint, Google Slides, Canva, or Gamma.

## Installation

```
/plugin marketplace add bryfarhamni/yaya
/plugin install presentation-plugin@yaya
```

For local testing: `claude --plugin-dir ./presentation-plugin`.
