# Copilot Global Skills

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

### Recommended: Agent-Driven Setup

Clone the repo, open it in VS Code, and tell Copilot:

```
Set up global skills
```

The repo includes a setup skill that handles everything automatically — detects your OS, asks where to put the skills folder, lets you pick which skills to install, generates the router with correct paths, and copies it to your prompts folder.

That's it. One sentence, fully interactive, no manual file editing.

### Manual Setup (Fallback)

If you prefer to do it by hand, or the agent setup doesn't work for you:

<details>
<summary>Click to expand manual steps</summary>

#### 1. Clone this repo

```bash
git clone https://github.com/FredFraiche/copilot-global-skills.git
```

#### 2. Copy the skills folder to a permanent location

| OS | Suggested path |
|----|----------------|
| Windows | `C:\Users\<you>\copilot-skills\` |
| macOS | `~/copilot-skills/` |
| Linux | `~/copilot-skills/` |

```bash
# Windows PowerShell
Copy-Item -Path ".\skills\*" -Destination "$env:USERPROFILE\copilot-skills\" -Recurse

# macOS/Linux
cp -r ./skills/ ~/copilot-skills/
```

#### 3. Edit the router file — set one path

Open `router/global-skills-router.instructions.md` and replace the placeholder path in the header with your actual skills folder path. Skill paths in the table are relative to this — no per-row editing needed.

#### 4. Copy the router to your VS Code prompts folder

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

</details>

## Adding Your Own Skills

The **skill-creator** skill (included in `skills/`) guides you through creating new skills with proper structure. If it's installed globally, just say:

```
Create a new skill for [topic]
```

Or do it manually:

1. Create `<your-skills-dir>/my-skill/SKILL.md` with YAML frontmatter (`description` field with trigger keywords)
2. Add a row to the trigger table in your installed `global-skills-router.instructions.md`

```markdown
| **my-skill** | keyword1, keyword2, keyword3 |
```

See `skills/skill-creator/SKILL.md` for full guidance on writing effective skills.

## Included Skills

| Skill | Type | What it does |
|-------|------|-------------|
| **honest-evaluation** | Behavioral | Prevents fabricated success, rigged tests, sycophantic framing. Forces accurate reporting. |
| **feasibility-gate** | Behavioral | Pre-checks before significant work. Catches doomed approaches before hours are wasted. |
| **plan-execution** | Behavioral | Prevents lazy stub implementations when working from plans. Enforces real content over structure. |
| **skill-creator** | Utility | Guides creation of new skills with proper SKILL.md structure, bundled resources, and global registration. |

## Known Limitations

- **Trigger matching is probabilistic.** Native skills use deterministic matching. This router relies on the LLM reading the table — reliable (~95%) but not guaranteed.
- **Adds tokens to every conversation.** The router table is ~150-200 tokens. Each loaded skill adds more. Small but non-zero.
- **Paths are absolute and OS-specific.** Hardcoded once during setup.
- **No native conflict resolution.** If the workspace has the same skill in `.github/skills/`, the router tells the agent to defer — advisory, not enforced.
- **`read_file` adds latency.** Each skill load is a tool call.

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
