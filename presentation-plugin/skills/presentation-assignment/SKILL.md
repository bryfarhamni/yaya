---
name: presentation-assignment
description: Plan, research, write, or review a presentation assignment from a brief with a topic, length, language, and rubric, and build it as an editable PowerPoint (.pptx) with speaker notes. Use when the user wants a literature-review presentation, an outline, slide content, speaker notes, a .pptx deck, or a check of a presentation for made-up facts, unverifiable citations, rubric gaps, or AI-sounding writing.
---

# Presentation Assignment

Turns an assignment brief into a presentation the student can deliver and defend: researched outline → slides with speaker notes → review → editable .pptx.

Defaults for this user (the brief can override any of them): **English**, **literature review**, **textbooks as the main sources** with journals as support, **Vancouver style with superscript citation numbers**, output as a **.pptx**. Keep Latin species names and foreign terms in *italics*.

## 1. Read the brief

Collect these before planning. Ask for anything missing in one short list, then wait. Length varies between assignments, so always ask for it.

| Field | Default if not given |
|---|---|
| Topic and the exact assignment wording | none: must be given |
| Length in minutes, and Q&A time | none: ask |
| Language | English |
| Rubric | `references/rubric.md` |
| Assignment type | Literature review |
| Sources | Standard textbooks first, recent reviews and guidelines to support or update |
| Citation style | Vancouver, superscript numbers |
| Audience | Classmates and lecturer |
| Group size and who presents what | Solo |
| Textbooks the student owns or was assigned | Ask; prefer those |
| PowerPoint template file | python-pptx default |

Slide count: about one content slide per minute of talk, plus title, conclusion, and references.

## 2. Research

- Textbooks first. Prefer the student's own or assigned books. Otherwise use standard current editions in the field (for medicine, e.g. Harrison's, Guyton and Hall, Robbins, Sherwood, Kumar and Clark). Use the newest edition you can confirm exists, with its correct editors, publisher, and year.
- Confirm a book's edition, editors, publisher, and year from the publisher, Google Books, WorldCat, or the NLM catalog. You usually cannot read the page itself, so cite the chapter, and add pages only when you saw them. Mark book facts you could not check against the text with `[check in book]` so the student confirms them against their copy.
- Use journal articles (PubMed, Consensus, or Elicit tools if available, otherwise web search) for numbers that change over time, such as prevalence or mortality, and for anything newer than the textbook edition. Prefer WHO and specialist-society guidelines and systematic reviews.
- Keep a source table: number, full Vancouver reference, DOI/ISBN/URL, and the exact facts taken from it. Only cite what you opened (an abstract at minimum for articles, a catalog record plus a seen passage or the student's confirmation for books).
- Every number must trace to a row in the source table. A fact with no source is removed or marked `[source needed]`.

## 3. Outline

Show the outline before writing any slides. It is the first deliverable.

- One line per slide: number, title, the one point it makes, sources, and seconds allotted. The times must add up to the length.
- Map each rubric criterion to the slides that cover it, and flag any criterion that no slide covers.
- Use this flow for every deck (the user's standard). It is also a story arc: the introduction is the setup (the problem), the questions are the tension (what isn't obvious, common misconceptions, why the simple answer falls short), and the answers and takeaways are the resolution.

  1. **Title slide.**
  2. **Visual hook (slide 2, about 20 seconds).** Grab attention before any bullets: one striking number from a source (`**Big:**`), a provocative question, a chart, or a large photo slot. No bullet list on this slide. Its notes open with one sentence the audience will remember.
  3. **Introduction: why this happens, then the foundation.** First, why the topic matters and why the problem occurs (burden, the problem in one or two slides). Then the basic concepts the audience needs before the main topic: definitions, the normal anatomy or physiology, key terms, and optionally a framework flowchart that maps the talk. Nothing from the body is explained here; the introduction only lays the ground.
  4. **Questions slide.** The questions the body will answer, in the order they will be answered. Use the lecturer's questions if the brief has them; otherwise write 3–5 from the assignment wording and show them in the outline for approval.
  5. **Body: one section per question, in a logical order.** Order the questions so related ones sit together: group by similarity or by subtopic category (for example by organ system, or cause → mechanism → effect → management), and say the grouping in the outline. Each section opens with the question as the slide title (or a short form of it), then answers it from top to bottom: the general answer first, then the explanation, then the specific details and examples. Give each body slide a photo slot when a book diagram or photo would explain it better than bullets.
  6. **Conclusion: short key takeaways.** One slide, 3–5 one-line takeaways, roughly one per question. No new information.
  7. **References.**
  8. **Backup slides** (after References, titled `Backup: …`): 2–3 slides with extra detail for the hardest likely questions (a mechanism in more depth, a limitation of the sources, numbers that didn't fit). They're only shown if someone asks.

- **Interaction:** plan 1–2 moments that make the audience do something, at most one per 5 minutes: a show of hands in the introduction ("Raise your hand if…"), and a one-question quick check before the takeaways (question on the slide, answer in the notes and said aloud). Mark them in the outline.
- **One idea per slide.** If a slide needs "and" in its title, split it.

## 4. Slides and speaker notes

Write each slide in this exact shape. `scripts/build_pptx.py` reads it.

```
## Slide N: <Slide title that states the point>

- <bullet, at most ~10 words><sup>1</sup>
- <bullet><sup>2,3</sup>
- <bullet>

**Visual:** <suggested chart, diagram, or image, or "none">

**Notes (~XX s):**
<What to say, in full spoken sentences, ~130 words per minute. It explains the bullets instead of reading them out, and ends with a transition to the next slide.>
```

- Framework or process slides use a flow block instead of bullets. One chain per line; repeat a label to branch or merge. The builder lays it out left to right, with outcomes (boxes with no outgoing arrow) in the last column. Keep it to about 12 boxes and 5 columns, and short labels:

  ````
  ```flow
  Cigarette smoke -> Oxidants and free radicals -> Airway inflammation -> COPD
  Oxidants and free radicals -> Endothelial damage -> Atherosclerosis -> Coronary heart disease
  Cigarette smoke -> Nicotine -> Atherosclerosis
  ```
  ````

  Each box on the framework should be explained by a later slide, and the notes should walk the chart from left to right.
- Photo slots: add `**Photo:** <what to insert> | <source with chapter, figure, or page><sup>n</sup>` to a slide. The builder leaves an empty, labelled box on the right with a caption under it, and moves the bullets to the left; the student pastes the figure from their book. Up to two per slide. A slide with only a photo line and no bullets gets one large slot. Name a figure only if you know the book has it; otherwise describe what to look for (for example "Diagram of an atherosclerotic plaque | Robbins, chapter on blood vessels [check in book]").
- Hook and statement slides: `**Big:** 8 million` puts a huge number or short question in the middle of the slide; a second `**Big:**` line adds a smaller line under it ("deaths a year<sup>1</sup>"). No bullets on these slides.
- Numbers go in charts, not tables. Any comparison of two or more numbers from the sources (prevalence by group, risk by dose, trend over years) is a chart block. Only chart numbers taken directly from a source; never estimate or fill gaps, and never chart a single number (use `**Big:**` instead). Cite the source in the slide title or a bullet.

  ````
  ```chart
  type: column
  title: <what is measured, with unit>
  <Group A>: <value from source>
  <Group B>: <value from source>
  <Group C>: <value from source>
  ```
  ````

  Types: column (default), bar (long labels), line (trends over time), pie (parts of one whole only). Add `series: A, B` and `Label: v1, v2` for grouped data. With bullets the chart goes on the right; without, it fills the slide.
- Legible from the back row: the builder uses 24pt or larger for slide text, 18–20pt in flowcharts, and dark text on a light background. Keep bullets short enough to fit at that size; if they don't fit, the slide has too much on it. Never colour text red on a dark background. Exceptions: figure captions (14pt) and the reference list (18pt).
- Slide 1 is the title slide: its bullets become subtitle lines (presenter, course, date).
- 3–5 bullets per slide, no full sentences, one idea per slide.
- Citations: Vancouver superscript numbers right after the fact, `<sup>1</sup>` or `<sup>1,3</sup>` or `<sup>2–4</sup>`, numbered in order of first use and reused when a source is cited again.
- The title states the point ("Smoking doubles the risk of coronary heart disease"), not just the topic ("Coronary heart disease").
- After the takeaways comes `## Slide N: References` (followed only by backup slides), written as a numbered list (`1. …`) in Vancouver format:
  - Book: `Loscalzo J, Fauci AS, Kasper DL, Hauser SL, Longo DL, Jameson JL, editors. Harrison's principles of internal medicine. 21st ed. New York: McGraw Hill; 2022.`
  - Book chapter: `Author AA. Chapter title. In: Editor AA, editor. Book title. 14th ed. Philadelphia: Elsevier; 2021. p. 100–15.`
  - Journal: `Author AA, Author BB. Title. Abbrev Journal. Year;Vol(Issue):pages. doi:…`
- After the slides, add these sections. None of them goes into the .pptx.
  - `# Q&A prep`: five likely questions from the lecturer with short, sourced answers, each pointing to a backup slide where one exists.
  - `# Rehearsal sheet`: a table of slide number, title, seconds, and the cumulative time at the end of that slide, so the student can check their pace during practice. Below it: "Rehearse out loud at least three times, timing each run, ideally once in front of a friend. If a run is more than 30 seconds over, cut a bullet, not your speaking speed."
  - `# Before presenting`: a short checklist: open the .pptx on the room's projector or a similar one if possible; check text is readable from the back row and colours still contrast; check the pasted figures are sharp; bring the file in two places (USB and cloud); know which slide each backup answers.
  - `# Sources table`.

Save the file as `presentation-<topic>.md` in the working directory.

## 5. Review

Run the `presentation-reviewer` agent on the file and the brief. If agents are unavailable, follow its steps yourself using `references/ai-writing-patterns.md`. Fix every confirmed problem.

## 6. Build the .pptx

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_pptx.py" presentation-<topic>.md [presentation-<topic>.pptx] [--template their-template.pptx]
```

Install python-pptx first if it's missing (`pip install python-pptx`). Ask for the student's or course's PowerPoint template and pass it with `--template` so every slide shares the same fonts, colours, and layouts. Without one, the deck uses a plain 16:9 white theme. The deck uses the template's title, title-and-content, and title-only layouts, real superscript citations, and speaker notes with the visual suggestion at the top. Give the user both the .pptx and the .md file paths, what the review changed, and every `[check in book]` and `[source needed]` item left for them.

## Never

- Invent a book, edition, chapter, page, study, author, DOI, statistic, guideline, or quote. If you can't find support, say so.
- Cite a source for a claim it doesn't make.
- Pad slides with filler or generic motivational lines.
