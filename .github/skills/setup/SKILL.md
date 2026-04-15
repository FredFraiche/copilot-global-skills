---
description: >
  Automated onboarding for copilot-global-skills. Clones the repo, creates the skills
  folder, configures the router, and installs everything in the right places.
  Triggers: 'global skill', 'global skills', 'copilot-global-skills', 'setup global',
  'install global skills', 'FredFraiche/copilot-global-skills',
  'github.com/FredFraiche/copilot-global-skills'.
---

# Global Skills Setup

You are setting up the copilot-global-skills system. This automates making VS Code Copilot skills available across all workspaces.

**Repo:** `https://github.com/FredFraiche/copilot-global-skills.git`

## Step 1 — Detect OS and Suggest Paths

Detect the user's OS from environment context. Set these defaults:

| OS | Skills folder | Prompts folder |
|----|---------------|----------------|
| Windows | `%USERPROFILE%\copilot-skills\` | `%APPDATA%\Code\User\prompts\` |
| macOS | `~/copilot-skills/` | `~/Library/Application Support/Code/User/prompts/` |
| Linux | `~/copilot-skills/` | `~/.config/Code/User/prompts/` |

## Step 2 — Ask: Skills Folder Location

Use the `ask-questions` tool. Single question:

```
Header: "Skills folder location"
Question: "Where should I create the global skills folder?"
Options:
  - [OS-appropriate default path] (recommended)
  - "Choose a different location"
```

If they choose a different location, ask for the path as freeform.

## Step 3 — Clone or Copy

If the user already has the repo cloned (check if the current workspace IS the repo — look for `router/global-skills-router.instructions.md`):
- **Copy** the `skills/` folder contents to the chosen skills folder location.

If they don't have it:
- **Clone** `https://github.com/FredFraiche/copilot-global-skills.git` to a temp location, copy `skills/` to the chosen path, then clean up.

## Step 4 — Ask: Which Skills?

List all available skills from the `skills/` directory. Use `ask-questions` with **multiSelect: true**.

```
Header: "Select global skills"
Question: "Which skills should be active globally? (select all that apply)"
Options:
  - "honest-evaluation" — Prevents fabricated results, rigged tests, sycophantic framing (recommended)
  - "feasibility-gate" — Pre-checks before significant work to catch doomed approaches (recommended)
  - "plan-execution" — Prevents lazy stub implementations when working from plans (recommended)
  - "skill-creator" — Guides creation of new skills with proper structure and global registration (recommended)
  - [any additional skills found in skills/ directory]
```

Mark the behavioral skills and skill-creator as recommended.

## Step 5 — Generate Router

Create `global-skills-router.instructions.md` with:

1. The YAML frontmatter:
```yaml
---
description: "Global skill router — loads skills from a central location when triggers match"
---
```

2. The header pointing to the chosen skills folder path. Use a single path line:
```markdown
All skill paths follow the pattern `<actual-path>/<skill-name>/SKILL.md`.
```

3. A trigger table containing **only** the skills the user selected. Use a **2-column format** (Skill | Triggers) — no Path column, since paths are derived from the header:
```markdown
| Skill | Triggers |
|-------|----------|
| **skill-name** | keyword1, keyword2, keyword3 |
```
Pull the trigger keywords from each selected skill's YAML `description` field.

4. The standard rules section (multiple skills can fire, always read_file, workspace skills take precedence, etc.).

## Step 6 — Install Router

Copy the generated `global-skills-router.instructions.md` to the OS-appropriate prompts folder.

If the prompts folder doesn't exist, create it.

If a `global-skills-router.instructions.md` already exists there, ask before overwriting:

```
Header: "Existing router found"
Question: "A global skills router already exists. Replace it?"
Options:
  - "Replace with new configuration" (recommended)
  - "Keep existing, skip this step"
```

## Step 7 — Verify

1. Confirm the skills folder exists and contains the selected skills
2. Confirm the router file exists in the prompts folder
3. List what was installed

Report in this format:

```
INSTALLED:
  Skills folder: [path]
  Skills: [list of installed skill names]
  Router: [prompts folder path]/global-skills-router.instructions.md

HOW IT WORKS:
  Every new Copilot conversation will now check the trigger table.
  When triggers match, the skill's SKILL.md is loaded via read_file.

TO ADD MORE SKILLS LATER:
  1. Drop a folder with SKILL.md in [skills folder path]
  2. Add a row to the trigger table in [router path]
```

## Important

- **Do not skip the questions.** The user must confirm the folder location and skill selection.
- **Use absolute paths** in the router file. No environment variables — resolve them to actual paths.
- **Create directories** if they don't exist. Don't fail because a folder is missing.
- **If git is not available**, fall back to downloading the repo as a ZIP or copying files directly from the current workspace.
