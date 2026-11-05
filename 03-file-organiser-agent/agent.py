"""Project 03: an agent that changes things, carefully.

The agent proposes how to tidy a folder. It runs in dry-run mode unless you
pass --apply, and it can never touch anything outside the folder you give it.

    python 03-file-organiser-agent/agent.py ~/Downloads            # dry run
    python 03-file-organiser-agent/agent.py ~/Downloads --apply    # really move files
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path

from agentkit import Tool, run_agent


def make_tools(root: Path, apply: bool) -> list[Tool]:
    root = root.resolve()

    def inside_root(relative: str) -> Path:
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise PermissionError(f"{relative!r} is outside {root}")
        return path

    def list_files(subfolder: str = ".") -> list[dict]:
        folder = inside_root(subfolder)
        return [
            {
                "name": str(p.relative_to(root)),
                "type": "folder" if p.is_dir() else (p.suffix.lower() or "no extension"),
                "size_kb": round(p.stat().st_size / 1024, 1),
                "modified": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d"),
            }
            for p in sorted(folder.iterdir())
        ]

    def move_file(file: str, destination_folder: str) -> str:
        source, target_dir = inside_root(file), inside_root(destination_folder)
        if not source.is_file():
            raise FileNotFoundError(file)
        target = target_dir / source.name
        if target.exists():
            raise FileExistsError(f"{target.relative_to(root)} already exists")
        if not apply:
            return f"DRY RUN: would move {file} -> {target.relative_to(root)}"
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(source, target)
        return f"moved {file} -> {target.relative_to(root)}"

    return [
        Tool(
            "list_files",
            "List files in a folder (relative to the root) with type, size and last-modified date.",
            {"subfolder": {"type": "string", "description": "Relative path, '.' for the root"}},
            list_files,
            required=[],
        ),
        Tool(
            "move_file",
            "Move one file into a folder (created if missing). Both paths are relative to the root.",
            {"file": {"type": "string"}, "destination_folder": {"type": "string"}},
            move_file,
        ),
    ]


SYSTEM = """You tidy folders. Group files into a few clear folders such as
Documents, Images, Installers, Archives and Spreadsheets. Leave existing folders
alone and never move a file into a folder it is already in. When done, summarise
what you moved (or would move) as a short table."""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("--apply", action="store_true", help="really move files (default: dry run)")
    args = parser.parse_args()

    print("Mode:", "APPLY" if args.apply else "DRY RUN")
    answer, _ = run_agent("Tidy this folder.", make_tools(args.folder, args.apply), SYSTEM, max_turns=40)
    print(answer)
