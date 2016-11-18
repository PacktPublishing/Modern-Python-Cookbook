"""Python Cookbook

Chapter 9, recipe 1a.
"""
from types import SimpleNamespace

from pathlib import Path

import datetime
from hashlib import md5

def file_facts(path):
    return SimpleNamespace(
        name = str(path),
        modified = datetime.datetime.fromtimestamp(
            path.stat().st_mtime).isoformat(),
        size = path.stat().st_size,
        checksum = md5(path.read_bytes()).hexdigest()
    )

if __name__ == "__main__":
    summary_path = Path('summary.dat')
    with summary_path.open('w') as summary_file:

        base = Path(".")
        for member in base.glob("*.py"):
            print(file_facts(member), file=summary_file)
