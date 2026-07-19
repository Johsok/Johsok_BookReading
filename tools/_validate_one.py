# -*- coding: utf-8 -*-
import json
import subprocess
import sys
from pathlib import Path

batch = json.loads(Path("tools/_batch1.json").read_text(encoding="utf-8"))
book = next(b for b in batch if b["id"] == sys.argv[1])
path = Path(f"tools/.findbook_results_grok_{book['id']}.json")
r = subprocess.run(
    [sys.executable, "tools/_check_hl.py", str(path), book["title"], book["author"]],
    capture_output=True,
    text=True,
    encoding="utf-8",
)
print(r.stdout)
print(r.stderr, file=sys.stderr)
sys.exit(r.returncode)
