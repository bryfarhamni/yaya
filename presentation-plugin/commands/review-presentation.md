---
description: Telaah presentasi untuk halusinasi, sitasi palsu, gaya tulisan AI, dan kesesuaian rubrik
argument-hint: "<path presentasi> [path rubrik/brief]"
---

Review the presentation at: $ARGUMENTS

Hand it to the `presentation-reviewer` agent with the file path and any brief or rubric. Report its findings to the user in its order: serious problems, AI writing, rubric and timing fit, top fixes.

Don't edit the file unless the user asks. If they do, apply only the fixes they approve.
