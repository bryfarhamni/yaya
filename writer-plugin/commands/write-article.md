---
description: Susun draf artikel penelitian (IMRAD) dari data/catatan penelitian
argument-hint: "[file catatan/data atau topik penelitian]"
---

Use the `research-article` skill and read its `references/format-penulisan.md` first.

Write a draft research article from: $ARGUMENTS

1. If $ARGUMENTS is a file path, read it. If anything needed is missing (design, setting and time, population and n, aims, main results, statistical tests), ask for it in one short list before writing.
2. Write in this order: Judul, Penulis & institusi, Abstrak (150–200 words) + Kata kunci, Pendahuluan (with tujuan umum and tujuan khusus), Metode, Hasil (with tables only where they help), Pembahasan, Simpulan.
3. Follow the rules on numbers, statistics, and percentages exactly. Never invent data or citations; use `[…]` for gaps.
4. Save the draft as a Markdown file in the working directory and give the user its path, plus a list of the `[…]` items they still need to fill in.
