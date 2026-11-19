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
- Literature review structure (adapt to the topic and rubric): title → why it matters (burden, a hook) → **conceptual framework flowchart** (exposure → mechanisms → outcomes, used as the map for the rest of the talk) → definition and classification → epidemiology → etiology and risk factors → pathophysiology → clinical features and diagnosis → management or prevention → synthesis (what the sources agree and disagree on, gaps) → conclusion → references.

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
- Slide 1 is the title slide: its bullets become subtitle lines (presenter, course, date).
- 3–5 bullets per slide, no full sentences, one idea per slide.
- Citations: Vancouver superscript numbers right after the fact, `<sup>1</sup>` or `<sup>1,3</sup>` or `<sup>2–4</sup>`, numbered in order of first use and reused when a source is cited again.
- The title states the point ("Smoking doubles the risk of coronary heart disease"), not just the topic ("Coronary heart disease").
- The last slide is `## Slide N: References`, written as a numbered list (`1. …`) in Vancouver format:
  - Book: `Loscalzo J, Fauci AS, Kasper DL, Hauser SL, Longo DL, Jameson JL, editors. Harrison's principles of internal medicine. 21st ed. New York: McGraw Hill; 2022.`
  - Book chapter: `Author AA. Chapter title. In: Editor AA, editor. Book title. 14th ed. Philadelphia: Elsevier; 2021. p. 100–15.`
  - Journal: `Author AA, Author BB. Title. Abbrev Journal. Year;Vol(Issue):pages. doi:…`
- After the slides, add `# Q&A prep`: five likely questions from the lecturer with short, sourced answers. Then add `# Sources table`. Neither goes into the .pptx.

Save the file as `presentation-<topic>.md` in the working directory.

## 5. Review

Run the `presentation-reviewer` agent on the file and the brief. If agents are unavailable, follow its steps yourself using `references/ai-writing-patterns.md`. Fix every confirmed problem.

## 6. Build the .pptx

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/build_pptx.py" presentation-<topic>.md [presentation-<topic>.pptx] [--template their-template.pptx]
```

Install python-pptx first if it's missing (`pip install python-pptx`). The deck uses the template's title and title-and-content layouts, real superscript citations, and speaker notes with the visual suggestion at the top. Give the user both the .pptx and the .md file paths, what the review changed, and every `[check in book]` and `[source needed]` item left for them.

## Never

- Invent a book, edition, chapter, page, study, author, DOI, statistic, guideline, or quote. If you can't find support, say so.
- Cite a source for a claim it doesn't make.
- Pad slides with filler or generic motivational lines.
