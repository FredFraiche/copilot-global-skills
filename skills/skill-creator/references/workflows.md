# Workflow Patterns

## Table of Contents

- [Sequential Workflows](#sequential-workflows)
- [Conditional Workflows](#conditional-workflows)
- [Decision Trees](#decision-trees)
- [Output Patterns](#output-patterns)

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. Give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Decision Trees

For complex decision-making, use decision trees:

```markdown
## Quick Start Decision Tree

**What do you want to do?**

├── **Read/extract content**
│   └── `python -m markitdown file.pptx`
│
├── **Create from scratch**
│   └── Read [pptxgenjs.md](pptxgenjs.md)
│
└── **Edit existing file**
    ├── **Simple edits** → Use XML manipulation
    └── **Complex edits** → Read [editing.md](editing.md)
```

## Output Patterns

### Template Pattern

When skills produce specific output formats:

```markdown
## Output Format

Always produce output in this structure:

1. **Summary** - 2-3 sentence summary of changes
2. **Details** - Bullet list of specific modifications
3. **Next Steps** - Suggested follow-up actions
```

### Example-Based Pattern

When examples are the most efficient way to teach:

```markdown
## Examples

**User request:** "Add a slide with a chart"

**Claude output:**
- Creates new slide using template
- Adds chart with sample data
- Formats according to brand guidelines
```

### Validation Pattern

For skills that produce files or code:

```markdown
## Quality Assurance (Required)

After completing the task:

1. Verify file opens correctly
2. Check all content renders
3. Validate against requirements
4. Report any issues to user
```
