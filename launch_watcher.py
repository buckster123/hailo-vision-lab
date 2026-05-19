#!/usr/bin/env python3
"""Launch the room entry watcher (assumes vision server is already running on the Pi)."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent

if __name__ == "__main__":
    print("Starting room entry watcher...")
    subprocess.run([sys.executable, str(HERE / "room_entry_watcher.py")])
