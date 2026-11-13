# writer-plugin

A Claude Code plugin for writing and reviewing research articles (IMRAD) following the guide *Format Penulisan Artikel Penelitian* (Saleha Sungkar, Fakultas Kedokteran Universitas Indonesia).

## Contents

| Type | Name | Purpose |
|---|---|---|
| Skill | `research-article` | Writing rules: judul, penulis, abstrak, pendahuluan, metode, hasil, tabel, bilangan, statistik, pembahasan, simpulan |
| Command | `/write-article [file/topik]` | Drafts an article from research notes or data |
| Command | `/review-article <naskah> [bagian]` | Reviews a manuscript against the guide |
| Command | `/check-title "<judul>"` | Checks a title and suggests alternatives |
| Agent | `article-reviewer` | Read-only reviewer, findings grouped by section |

The full guide is in `skills/research-article/references/format-penulisan.md`.

## Installation

```
/plugin marketplace add bryfarhamni/yaya
/plugin install writer-plugin@yaya
```

For local testing: `claude --plugin-dir ./writer-plugin`.
