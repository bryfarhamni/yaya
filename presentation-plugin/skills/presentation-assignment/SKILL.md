---
name: presentation-assignment
description: Plan, research, write, or review a presentation assignment (tugas presentasi) from a brief with a topic, length, language, and rubric. Use when the user wants an outline, slide content, speaker notes (catatan pembicara), or a check of a presentation for made-up facts, unverifiable citations, rubric gaps, or AI-sounding writing, in Bahasa Indonesia or English.
---

# Presentation Assignment

Turns an assignment brief into a presentation the student can deliver and defend: researched outline → slides with speaker notes → review. Write in the language the brief asks for (usually Bahasa Indonesia). Keep foreign terms and Latin species names in *italics*.

## 1. Read the brief

Collect these before planning. Ask for anything missing in one short list, then wait.

| Field | Why it matters | Default if the user says "terserah" |
|---|---|---|
| Topic and exact assignment wording | Scope | none: must be given |
| Length (minutes) and Q&A time | Slide count | 10 minutes, no Q&A |
| Language | Everything | Bahasa Indonesia |
| Rubric or grading criteria | What gets marked | General rubric in `references/brief-template.md` |
| Assignment type (topic review, journal reading, case, group) | Structure | Topic review |
| Source rules (recency, database, citation style) | Research | Peer-reviewed, last 10 years, Vancouver |
| Audience (classmates, lecturer, lay public) | Depth and jargon | Classmates and lecturer |
| Group size and who presents what | Split of slides | Solo |

Slide count: about one content slide per minute of talk, plus title, outline (optional), conclusion, and references. Never exceed the rubric's limit if it has one.

## 2. Research

- Search before writing. Prefer PubMed, Consensus, or Elicit tools when available; otherwise web search. Prefer guidelines (WHO, Kemenkes, specialist societies), systematic reviews, and recent primary studies.
- Record each source in a source table with: number, full Vancouver reference, DOI or URL, and the specific facts you took from it. Only cite what you opened and read (abstract at minimum). If you could not open a source, do not cite it.
- Every number (prevalence, deaths, risk ratios, percentages) must trace to a row in the source table. A fact with no source is either removed or marked `[perlu sumber]`.
- If the user supplied sources (PDFs, links, a journal for journal reading), use those first and say which extra sources you added.

## 3. Outline

Write the outline before any slide text and show it to the user as the first deliverable:

- One line per slide: slide number, title, the one point it makes, sources used, and seconds allotted. Times must add up to the length.
- Map each rubric criterion to the slides that satisfy it. Flag any criterion no slide covers.
- Common structures (adapt to the rubric):
  - **Topic review**: hook/why it matters → definition and epidemiology → mechanism/pathophysiology → main content (2–4 slides) → prevention or management → conclusion → references.
  - **Journal reading**: identity of the article → background and aim → methods (design, sample, analysis) → key results → critical appraisal (validity, importance, applicability) → conclusion and relevance.
  - **Case presentation**: patient identity → history → examination → investigations → diagnosis and differentials → management → discussion with literature → conclusion.

## 4. Slides and speaker notes

Write each slide in this exact shape so it can be pasted into PowerPoint or Google Slides:

```
## Slide N: <Judul slide>

- <bullet, at most ~10 words>
- <bullet>
- <bullet>

**Visual:** <suggested chart, diagram, image, or "none">
**Sumber:** [1], [3]

**Catatan pembicara (~XX detik):**
<What to say, in full spoken sentences, ~130 words per minute. Explains the bullets, does not read them out.>
```

Slide rules:
- 3–5 bullets, no full sentences on the slide, one idea per slide. Numbers on slides carry their citation.
- The title says the point ("Merokok melipatgandakan risiko PJK"), not just the topic ("PJK").
- Speaker notes sound like a student talking: plain words, short sentences, a transition to the next slide at the end.
- Final slide: references in the requested style (Vancouver default), numbered in order of first use.
- After the deck, add a **Persiapan tanya jawab** section: 5 likely questions from the lecturer with short, sourced answers.

Save the result as a Markdown file in the working directory (`presentasi-<topik>.md`) and give the user its path.

## 5. Review

Before handing over, run the `presentation-reviewer` agent on the file (or follow `references/ai-writing-patterns.md` and the agent's steps yourself if agents are unavailable). Fix every confirmed problem, and tell the user what the reviewer found and what you changed.

## Never

- Invent a study, author, journal, DOI, statistic, guideline, or quote. If you cannot find support, say so.
- Cite a source for a claim it does not make.
- Pad slides with filler or generic motivational lines.
