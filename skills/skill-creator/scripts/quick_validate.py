#!/usr/bin/env python3
"""
Quick Skill Validator - Validates skill structure and frontmatter

Usage:
    quick_validate.py <path/to/skill-folder>
"""

import sys
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Warning: PyYAML not installed. Install with: pip install pyyaml")
    yaml = None


def validate_skill(skill_path):
    """
    Basic validation of a skill.

    Args:
        skill_path: Path to the skill folder

    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read content
    content = skill_md.read_text(encoding='utf-8')

    # Check frontmatter exists
    if not content.startswith('---'):
        return False, "No YAML frontmatter found (must start with ---)"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format (missing closing ---)"

    frontmatter_text = match.group(1)

    # Parse YAML if available
    if yaml:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return False, "Frontmatter must be a YAML dictionary"
        except yaml.YAMLError as e:
            return False, f"Invalid YAML in frontmatter: {e}"
    else:
        # Basic parsing without PyYAML
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key = line.split(':')[0].strip()
                frontmatter[key] = True

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing required field: name"
    if 'description' not in frontmatter:
        return False, "Missing required field: description"

    # Check description quality
    if yaml:
        description = frontmatter.get('description', '')
        if isinstance(description, str):
            if len(description) < 50:
                return False, f"Description too short ({len(description)} chars). Should be at least 50 chars with WHAT/WHEN/KEYWORDS."
            if '[TODO' in description:
                return False, "Description contains TODO placeholder"

    # Check for body content
    body_start = content.find('---', 3)
    if body_start == -1:
        return False, "No body content after frontmatter"

    body = content[body_start + 3:].strip()
    if len(body) < 50:
        return False, "Body content too short (less than 50 chars)"

    # Count lines
    line_count = len(content.split('\n'))
    if line_count > 500:
        return False, f"SKILL.md too long ({line_count} lines). Maximum is 500 lines. Split to references/."

    return True, f"Valid ({line_count} lines)"


def main():
    if len(sys.argv) < 2:
        print("Usage: quick_validate.py <path/to/skill-folder>")
        print("\nExample:")
        print("  quick_validate.py ./skills/my-skill")
        sys.exit(1)

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"❌ Error: Path not found: {skill_path}")
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        sys.exit(1)

    print(f"Validating skill: {skill_path.name}")
    print("-" * 40)

    valid, message = validate_skill(skill_path)

    if valid:
        print(f"✅ {message}")

        # Additional info
        skill_md = skill_path / 'SKILL.md'
        content = skill_md.read_text(encoding='utf-8')

        # Check for resources
        if (skill_path / 'scripts').exists():
            scripts = list((skill_path / 'scripts').glob('*.py'))
            print(f"   scripts/: {len(scripts)} Python files")

        if (skill_path / 'references').exists():
            refs = list((skill_path / 'references').glob('*.md'))
            print(f"   references/: {len(refs)} Markdown files")

        if (skill_path / 'assets').exists():
            assets = list((skill_path / 'assets').iterdir())
            print(f"   assets/: {len(assets)} files")

        sys.exit(0)
    else:
        print(f"❌ {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
