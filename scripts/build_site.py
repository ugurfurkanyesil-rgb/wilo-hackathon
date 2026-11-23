"""Copy simulation results the web page needs into site/data/.

Run after run_leak.py and run_tank.py:  python scripts/build_site.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DST = ROOT / "site" / "data"
DST.mkdir(parents=True, exist_ok=True)
for name in ("leak_summary.json", "tank_summary.json", "tank_week_trace.json"):
    shutil.copy(ROOT / "results" / name, DST / name)
    print("copied", name)
