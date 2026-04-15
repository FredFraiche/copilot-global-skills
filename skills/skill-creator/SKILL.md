---
name: skill-creator
description: >
  Guide for creating effective agent skills. Use when users want to create a new skill,
  update an existing skill, or need guidance on skill architecture, progressive disclosure
  patterns, or bundled resources (scripts/references/assets). Triggers on "create a skill",
  "new skill", "skill template", "SKILL.md", "init skill", "package skill".
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend the agent's capabilities by providing specialized knowledge, workflows, and tools. They transform a general-purpose agent into a specialized one.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share it with everything else the agent needs.

**Default assumption: the agent is already very smart.** Only add context it doesn't already have. Challenge each piece of information: "Does it really need this explanation?"

Prefer concise examples over verbose explanations.

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description - required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts)
```

#### SKILL.md (required)

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields used for triggering.
- **Body** (Markdown): Instructions and guidance. Only loaded AFTER the skill triggers.

#### Bundled Resources (optional)

**Scripts (`scripts/`)** - Executable code for deterministic reliability
- When to include: When the same code is being rewritten repeatedly
- Benefits: Token efficient, deterministic, may be executed without loading into context

**References (`references/`)** - Documentation loaded as needed
- When to include: For documentation the agent should reference while working
- Benefits: Keeps SKILL.md lean, loaded only when needed
- Best practice: If files are large (>10k words), include grep search patterns in SKILL.md

**Assets (`assets/`)** - Files used in output
- Examples: Templates (.pptx, .docx), images, fonts, boilerplate code
- Benefits: Separates output resources from documentation

#### What NOT to Include

- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, etc.
- The skill should only contain information needed for an AI agent to do the job

### Progressive Disclosure Design

Skills use a three-level loading system:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words, <500 lines)
3. **Bundled resources** - As needed

**Key principle:** Keep only the core workflow in SKILL.md. Move variant-specific details into separate reference files.

**Pattern 1: High-level guide with references**
```markdown
## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

**Guidelines:**
- Keep SKILL.md under 500 lines
- Avoid deeply nested references - keep one level deep from SKILL.md
- Structure longer reference files (>100 lines) with table of contents

## Skill Creation Process

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, assets)
3. Initialize the skill (run init_skill.py)
4. Edit the skill (implement resources, write SKILL.md)
5. Validate the skill (run quick_validate.py)
6. Register in the global skills router
7. Iterate based on real usage

### Step 1: Understanding the Skill

Ask questions to understand concrete usage examples:
- "What functionality should this skill support?"
- "What would a user say that should trigger this skill?"
- "Can you give examples of how this skill would be used?"

### Step 2: Planning Reusable Contents

Analyze each concrete example to identify:
- Scripts: Code that would be rewritten each time
- References: Documentation that would need to be rediscovered
- Assets: Templates or files used in output

### Step 3: Initializing the Skill

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates:
- Skill directory with SKILL.md template
- Example resource directories: `scripts/`, `references/`, `assets/`

### Step 4: Edit the Skill

#### Frontmatter

Write YAML frontmatter with `name` and `description`:

- `name`: The skill name (lowercase, hyphens)
- `description`: Primary triggering mechanism. Include:
  - WHAT the skill does
  - WHEN to use it (specific triggers/contexts)
  - KEYWORDS users might say

**Example:**
```yaml
description: "Comprehensive document creation and editing for .docx files. Use when users need to: (1) Create new Word documents, (2) Modify or edit content, (3) Work with tracked changes. Triggers on 'Word doc', '.docx', 'create a report', 'edit my letter'."
```

#### Body

- Use imperative/infinitive form
- Include only non-obvious information
- Reference bundled resources appropriately

### Step 5: Validate the Skill

```bash
python scripts/quick_validate.py <path/to/skill-folder>
```

Checks:
- YAML frontmatter format and required fields
- Description completeness
- Directory structure

### Step 6: Register in Global Skills Router

Every skill that isn't hyper-specific to a single workspace should be registered
in the global skills router so it fires automatically in any workspace.

**The router file location** is the `global-skills-router.instructions.md` in your
VS Code prompts folder (set up during installation).

**Actions:**
1. Copy the skill folder to your global skills directory (the path configured in your router)
2. Add a row to the `## Skill Registry` table in the router file with the skill name and its trigger words
3. The trigger words should match the keywords from the skill's `description` field

**When to skip global registration:**
- The skill is tightly coupled to one specific workspace (e.g., a project's deploy pipeline)
- The skill references workspace-specific paths, files, or tools that don't exist elsewhere
- The user explicitly says it's a workspace-only skill

**When in doubt, register globally.** A skill that fires and isn't needed costs nothing. A skill that doesn't fire when needed wastes the user's time.

## Resources

- **scripts/init_skill.py** - Initialize new skills from template
- **scripts/quick_validate.py** - Validate skill structure
- **references/workflows.md** - Sequential and conditional workflow patterns
