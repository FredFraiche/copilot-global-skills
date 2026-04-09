# Copilot Global Skills Router

Make VS Code Copilot skills work **across all workspaces** — not just the one they're defined in.

## The Problem

VS Code Copilot skills (`.github/skills/`) are workspace-scoped. They only fire inside the project that contains them. There is no native way to make a skill available globally.

This is fine for project-specific skills. It's a problem for **behavioral skills** — constraints like "don't fabricate test results" or "check feasibility before building" that should apply everywhere, regardless of what project you're working in.

## The Solution

A `.instructions.md` file placed in your global prompts folder. Unlike skills, instruction files in this folder **are loaded into every conversation in every workspace**.

The router file contains a trigger table. When a conversation matches trigger keywords, it tells Copilot to `read_file` the corresponding SKILL.md from a central folder on your machine. This gives you the same context-triggered behavior as native skills, but globally.

### How it works

```
User says "train a model" in any workspace
       │
       ▼
Router (.instructions.md) is loaded — it's always present
       │
       ▼
Trigger table matches "train" → feasibility-gate
       │
       ▼
Agent calls read_file("~/copilot-skills/feasibility-gate/SKILL.md")
       │
       ▼
Skill instructions are now in context — agent follows them
```

## Installation

### 1. Clone this repo (or just download the files)

```bash
git clone https://github.com/YOUR_USERNAME/copilot-global-skills-router.git
```

### 2. Copy the skills folder to a permanent location

Pick a path you won't accidentally delete. Examples:

| OS | Suggested path |
|----|----------------|
| Windows | `C:\Users\<you>\copilot-skills\` |
| macOS | `~/copilot-skills/` |
| Linux | `~/copilot-skills/` |

```bash
# Example (Windows PowerShell)
Copy-Item -Path ".\skills\*" -Destination "$env:USERPROFILE\copilot-skills\" -Recurse

# Example (macOS/Linux)
cp -r ./skills/ ~/copilot-skills/
```

### 3. Edit the router file — update the paths

Open `router/global-skills-router.instructions.md` and replace `<SKILLS_DIR>` with your actual path in every table row.

For example, on Windows:
```
| **honest-evaluation** | test, result, fail, ... | C:\Users\me\copilot-skills\honest-evaluation\SKILL.md |
```

### 4. Copy the router to your VS Code prompts folder

| OS | Prompts folder |
|----|----------------|
| Windows | `%APPDATA%\Code\User\prompts\` |
| macOS | `~/Library/Application Support/Code/User/prompts/` |
| Linux | `~/.config/Code/User/prompts/` |

```bash
# Windows PowerShell
Copy-Item ".\router\global-skills-router.instructions.md" "$env:APPDATA\Code\User\prompts\"

# macOS/Linux
cp ./router/global-skills-router.instructions.md ~/Library/Application\ Support/Code/User/prompts/
# or for Linux:
cp ./router/global-skills-router.instructions.md ~/.config/Code/User/prompts/
```

That's it. Every new Copilot conversation will now have access to the router.

## Adding Your Own Skills

1. Create a folder: `~/copilot-skills/my-skill/SKILL.md`
2. Write the skill instructions in SKILL.md (follow the examples in `skills/`)
3. Add a row to the trigger table in your installed `global-skills-router.instructions.md`

```markdown
| **my-skill** | keyword1, keyword2, keyword3 | ~/copilot-skills/my-skill/SKILL.md |
```

## Included Example Skills

Three behavioral skills are included as examples. These are **constraints on model behavior**, not capabilities — they work in any project.

| Skill | What it does |
|-------|-------------|
| **honest-evaluation** | Prevents the model from fabricating success, rigging tests, softening bad results, or hiding failure. Forces accurate reporting of all outcomes. |
| **feasibility-gate** | Forces a precondition check before significant work (training models, large datasets, multi-file systems). Catches doomed approaches before hours are wasted. |
| **plan-execution** | Prevents lazy stub-and-scaffold implementations when working from a plan. Enforces real content over empty structure. |

## Known Limitations

Be aware of these before relying on this in production:

- **Trigger matching is probabilistic.** Native `.github/skills/` triggers are deterministic (VS Code matches them internally). This router relies on the LLM reading the table and deciding to fire — which it does reliably but not 100% of the time.
- **Adds tokens to every conversation.** The router table is ~150-200 tokens. Each loaded skill adds more. This is small but non-zero.
- **Paths are absolute and OS-specific.** No environment variable expansion inside the table. You hardcode your path once during setup.
- **No native conflict resolution.** If a workspace has the same skill in `.github/skills/`, the router tells the agent to defer — but this is advisory, not enforced by VS Code.
- **`read_file` adds latency.** Each skill load is a tool call. Native skills are injected without one.

## Why Not Just Use `.instructions.md` Directly?

You could paste all your skill content directly into the `.instructions.md` file. That works, and it's even more reliable (no `read_file` indirection). But:

- Skill files get long. 3 behavioral skills = ~300 lines. 10 skills = unmanageable.
- The router pattern keeps the always-on cost fixed (~200 tokens) and only loads what's relevant.
- Skills can be updated independently without touching the router.
- Skills can be shared, composed, and versioned as separate units.

## How It Compares to Native Skills

| | Native `.github/skills/` | This router |
|---|---|---|
| Trigger reliability | Deterministic | Probabilistic (~95%) |
| Scope | Workspace only | Global |
| Setup cost | Drop folder in repo | One-time install |
| Token cost (idle) | 0 | ~200 |
| Token cost (active) | Injected | `read_file` call |
| Conflict handling | N/A | Advisory "workspace wins" rule |

## License

MIT
