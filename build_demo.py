"""Embed data/sample.json into template.html -> index.html (single self-contained file)."""
import json
from datetime import date
from pathlib import Path
from generate_sample import LAYOUT, FLOOR_BINS, AS_OF, WAREHOUSE, PLANT

ROOT = Path(__file__).resolve().parent.parent
NAMES = {"001": "Pallet Racking", "002": "Overflow Racking", "003": "High Bay", "900": "Floor Staging"}

rows = json.load(open(ROOT / "data" / "sample.json"))
mats, idx, out = [], {}, []
for r in rows:
    if r["Material"] not in idx:
        idx[r["Material"]] = len(mats)
        mats.append([r["Material"], r["Material Description"], r["Base Unit of Measure"]])
    age = (AS_OF - date.fromisoformat(r["GR Date"])).days
    out.append([r["Storage Type"], r["Storage Bin"], r["Storage Unit"], idx[r["Material"]],
                r["Batch"], r["Total Stock"], r["Available Stock"], age])

# list (not dict) keeps order: JS reorders integer-like keys such as "900"
layout = [{"type": t, "name": NAMES[t], "aisles": a, "bays": b, "levels": l} for t, a, b, l, _ in LAYOUT]
layout.append({"type": "900", "name": NAMES["900"], "bins": FLOOR_BINS})
data = {"meta": {"warehouse": WAREHOUSE, "plant": PLANT}, "layout": layout, "mats": mats, "rows": out}

html = (ROOT / "template.html").read_text().replace("__DATA__", json.dumps(data, separators=(",", ":")))
(ROOT / "index.html").write_text(html)
print(f"index.html {len(html)/1024:.1f} KB, {len(out)} rows")
