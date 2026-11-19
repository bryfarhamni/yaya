---
description: Susun tugas presentasi dari brief: kerangka berbasis riset, isi slide, catatan pembicara
argument-hint: "[file brief atau topik + durasi + bahasa]"
---

Use the `presentation-assignment` skill and follow its steps in order.

Brief: $ARGUMENTS

1. If $ARGUMENTS is a file path, read it (rubric files too). Fill the brief fields from it; ask for anything still missing in one short list. The template is in `references/brief-template.md`.
2. Research and build the source table.
3. Show the outline with the rubric map and timings. Ask the user to approve or change it before writing slides, unless they said to go straight through.
4. Write the slides, speaker notes, references, and Q&A prep, and save them to `presentasi-<topik>.md`.
5. Run the `presentation-reviewer` agent on the file with the brief. Fix what it confirms, then give the user the file path, a short summary of what the review found and changed, and any `[perlu sumber]` items left for them.
