---
description: "Global skill router — loads skills from a central location when triggers match"
---

# Global Skills Router

You have access to centrally-hosted skills. The skills directory is located at:

- **Windows**: `C:\Users\<you>\copilot-skills\`
- **macOS/Linux**: `~/copilot-skills/`

When the user's message or task context matches the triggers below, **read the corresponding SKILL.md file using read_file** and follow its instructions. Check triggers at the start of every conversation turn.

## Skill Registry

| Skill | Triggers | Path |
|-------|----------|------|
| **honest-evaluation** | test, result, success, fail, error, bug, fix, simulate, evaluate, benchmark, compare, review, deploy, ship | `<SKILLS_DIR>/honest-evaluation/SKILL.md` |
| **feasibility-gate** | train, model, dataset, build, surrogate, pipeline, rewrite, deploy, GPU, ensemble, fine-tune, scrape, crawl | `<SKILLS_DIR>/feasibility-gate/SKILL.md` |
| **plan-execution** | plan.md, complete the plan, implement this, spec, roadmap, task list, follow the plan, execute this | `<SKILLS_DIR>/plan-execution/SKILL.md` |

> **Add your own skills** by dropping a folder with a SKILL.md in your skills directory and adding a row to this table.

## Rules

1. **Multiple skills can fire on the same message.** If both honest-evaluation and feasibility-gate match, load both.
2. **honest-evaluation fires broadly.** This is intentional — it is a behavioral constraint, not a capability. When in doubt, load it.
3. **Always `read_file` the SKILL.md.** Do not summarize from memory, do not cache, do not paraphrase. Re-read each time.
4. **Workspace skills take precedence.** If the current workspace has the same skill in `.github/skills/`, the workspace copy wins (VS Code loads it natively — skip the `read_file`).
5. **To add a skill:** create `<SKILLS_DIR>/<skill-name>/SKILL.md` and add a row to the table above.
6. **To remove a skill:** delete the row from the table. The folder can stay or go — the router only acts on table entries.
