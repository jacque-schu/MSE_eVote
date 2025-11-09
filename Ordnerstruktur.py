from pathlib import Path

root = Path(".").resolve()
exclude = {".git", ".idea", "venv", "__pycache__"}

def walk(p: Path, prefix=""):
    entries = [e for e in sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
               if e.name not in exclude]
    for i, e in enumerate(entries):
        connector = "└── " if i == len(entries)-1 else "├── "
        print(prefix + connector + e.name)
        if e.is_dir():
            extension = "    " if i == len(entries)-1 else "│   "
            walk(e, prefix + extension)

print(root.name)
walk(root)
