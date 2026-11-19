---
description: Build a presentation assignment from a brief: researched outline, slides with speaker notes, review, and an editable .pptx
argument-hint: "[brief file, or topic + length]"
---

Use the `presentation-assignment` skill and follow its steps in order.

Brief: $ARGUMENTS

1. If $ARGUMENTS is a file path, read it (and any rubric or template files it names). Fill the brief fields; ask for anything still missing, always including length, in one short list. The template is `references/brief-template.md`.
2. Research and build the sources table.
3. Show the outline with the rubric map and timings. Ask the user to approve or change it before writing slides, unless they said to go straight through.
4. Write the slides, notes, references, Q&A prep, and sources table to `presentation-<topic>.md`.
5. Run the `presentation-reviewer` agent on the file with the brief, and fix what it confirms.
6. Build the .pptx with `scripts/build_pptx.py`. Give the user both file paths, a short summary of what the review found and changed, and every `[check in book]` and `[source needed]` item left for them.
