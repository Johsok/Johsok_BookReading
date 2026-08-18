from pathlib import Path
base = Path(__file__).resolve().parent
for n in range(51, 61):
    p = base / f"03_natural_science-20260717-{n:02d}.json"
    raw = p.read_bytes()
    print(n, p.stat().st_size, raw[:12], "empty" if not raw.strip() else "ok")
