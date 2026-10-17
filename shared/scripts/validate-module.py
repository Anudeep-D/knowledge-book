#!/usr/bin/env python3
"""
Enterprise Knowledge Book Module Linter & Contract Validator
Enforces frontmatter schema, the 4-part pedagogical contract, and directory conventions.
"""

import argparse
import os
import re
import sys
from pathlib import Path

REQUIRED_FRONTMATTER_KEYS = [
    "id",
    "title",
    "track",
    "difficulty",
    "estimated_minutes",
    "tags",
]

VALID_TRACKS = [
    "01-cloud-native-infra",
    "02-ai-models-inference",
    "03-modern-data-layers",
    "04-agentic-workflows",
]

REQUIRED_SECTIONS = [
    "1. Interactive Concept Breakdown",
    "2. Visual Architecture",
    "3. Real-World Code & Configuration",
    "4. Edge Cases, Failure Modes & Trade-offs",
]


def parse_frontmatter(content: str):
    """Extract YAML frontmatter without external dependencies."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None, "Missing opening and closing '---' frontmatter delimiters."

    raw_yaml = match.group(1)
    meta = {}
    current_key = None
    list_items = []

    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Check list item
        if line.startswith("- "):
            val = line[2:].strip().strip('"').strip("'")
            if current_key:
                list_items.append(val)
            continue

        # Check key-value pair
        kv_match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if kv_match:
            # Commit previous list
            if current_key and list_items:
                meta[current_key] = list_items
                list_items = []

            key, value = kv_match.group(1), kv_match.group(2).strip()
            # Remove trailing comments
            if " #" in value:
                value = value.split(" #")[0].strip()

            value = value.strip('"').strip("'")
            current_key = key
            if value:
                meta[key] = value
            else:
                meta[key] = []

    if current_key and list_items:
        meta[current_key] = list_items

    return meta, None


def validate_module(module_path: Path) -> list:
    """Validate a single module directory against the contract."""
    errors = []
    if not module_path.is_dir():
        return [f"Target path is not a directory: {module_path}"]

    index_file = module_path / "index.md"
    if not index_file.exists():
        return [f"Missing 'index.md' in {module_path}"]

    # Check companion directories
    diagrams_dir = module_path / "diagrams"
    artifacts_dir = module_path / "artifacts"

    if not diagrams_dir.exists():
        errors.append(f"Missing companion 'diagrams/' directory in {module_path}")
    if not artifacts_dir.exists():
        errors.append(f"Missing companion 'artifacts/' directory in {module_path}")

    try:
        content = index_file.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Failed to read {index_file}: {e}"]

    # 1. Frontmatter Validation
    meta, fm_err = parse_frontmatter(content)
    if fm_err:
        errors.append(f"Frontmatter Error: {fm_err}")
    else:
        for key in REQUIRED_FRONTMATTER_KEYS:
            if key not in meta or not meta[key]:
                errors.append(f"Frontmatter missing required key: '{key}'")

        if "track" in meta and meta["track"] not in VALID_TRACKS:
            errors.append(
                f"Invalid track '{meta['track']}'. Must be one of: {', '.join(VALID_TRACKS)}"
            )

        if "estimated_minutes" in meta:
            try:
                mins = int(meta["estimated_minutes"])
                if mins <= 0:
                    errors.append("estimated_minutes must be greater than 0.")
            except ValueError:
                errors.append(f"estimated_minutes must be an integer, got: {meta['estimated_minutes']}")

    # 2. Section Header Validation
    header_pattern = re.compile(r"^#\s+(.+)$", re.MULTILINE)
    h1_headers = [m.strip() for m in header_pattern.findall(content)]

    # The title may be an H1, but sections 1 through 4 must be present in sequential order
    for req in REQUIRED_SECTIONS:
        found = any(h.startswith(req) or req in h for h in h1_headers)
        if not found:
            errors.append(f"Missing mandatory section header: '# {req}'")

    # 3. Visual Architecture (Diagrams) Check
    has_mermaid = "```mermaid" in content
    has_ascii_diagram = "+---" in content or "|---" in content or "===>" in content or "<---" in content
    if not (has_mermaid or has_ascii_diagram):
        errors.append("Section 2 (Visual Architecture) must include at least one Mermaid or ASCII diagram.")

    # 4. Comparative Table Check
    table_pattern = re.compile(r"\|.+?\|.+?\|\s*\n\|(?:\s*:?-+:?\s*\|)+\s*\n\|.+?\|", re.DOTALL)
    if not table_pattern.search(content):
        errors.append("Section 4 (Edge Cases & Trade-offs) must include at least one comparative Markdown table.")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate knowledge book modules against the 4-part contract.")
    parser.add_argument("--path", type=str, help="Path to specific module directory.")
    parser.add_argument("--all", action="store_true", help="Validate all modules across tracks/.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent

    if not args.path and not args.all:
        parser.print_help()
        sys.exit(1)

    target_dirs = []
    if args.path:
        target_dirs.append(Path(args.path).resolve())
    elif args.all:
        tracks_dir = repo_root / "tracks"
        for track in tracks_dir.iterdir():
            if track.is_dir() and not track.name.startswith("."):
                for mod in track.iterdir():
                    if mod.is_dir() and (mod / "index.md").exists():
                        target_dirs.append(mod)

    if not target_dirs:
        print("[WARNING] No module directories found to validate.")
        sys.exit(0)

    total_failures = 0
    print(f"\n[MODULE VALIDATOR] Scanning {len(target_dirs)} module(s)...")

    for mod_path in target_dirs:
        rel_path = mod_path.relative_to(repo_root) if repo_root in mod_path.parents else mod_path
        errors = validate_module(mod_path)
        if errors:
            total_failures += 1
            print(f"\n[FAIL] {rel_path}:")
            for err in errors:
                print(f"   ✖ {err}")
        else:
            print(f"[PASS] {rel_path} satisfies 4-part contract.")

    print(f"\n[SUMMARY] {len(target_dirs) - total_failures}/{len(target_dirs)} module(s) passed validation.")

    if total_failures > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
