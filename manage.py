#!/usr/bin/env python3
import sys
from pathlib import Path
import runpy

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        script = BASE / sys.argv[1]
    else:
        script = BASE / "server.py"
    if not script.exists():
        print(f"Error: {script} not found.")
        sys.exit(1)
    runpy.run_path(str(script), run_name="__main__")
