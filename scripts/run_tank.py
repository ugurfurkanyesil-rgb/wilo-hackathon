"""Taze Depo experiment: freshness vs. security of fill policies under changing cuts.

Run:  python scripts/run_tank.py
Out:  results/tank_*.png, results/tank_kpis.csv, results/tank_summary.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.sim.tank_sim import (FixedDay, FixedSchedule, Float, Nabiz, TankBuilding,  # noqa: E402
                              kpis, make_demand, make_supply, run)

OUT = ROOT / "results"
DAYS = 180
SEEDS = range(1, 21)
HEADLINE = "NABIZ (taban 18 sa)"


def policies():
    return ([Float(), FixedSchedule()] + [FixedDay(k) for k in (0.75, 1.0, 1.25, 1.5, 1.75)]
            + [Nabiz(base_h=h) for h in (6, 12, 18, 24)])


def main() -> None:
    OUT.mkdir(exist_ok=True)
    b = TankBuilding()
    rows, traces = [], {}
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        demand = make_demand(b, DAYS, rng)
        supply, phases = make_supply(DAYS, rng)
        for p in policies():
            df = run(p, b, demand, supply)
            rows.append({"policy": p.name, "seed": seed, **kpis(df, b)})
            if seed == 1:
                traces[p.name] = df
    k = pd.DataFrame(rows)
    k.to_csv(OUT / "tank_kpis.csv", index=False)
    agg = k.groupby("policy", sort=False).mean(numeric_only=True).drop(columns="seed")
    print(agg.round(2).to_string())

    summary = {
        "days": DAYS, "warmup_days": 14, "seeds": len(SEEDS),
        "building": {"persons": b.persons, "daily_l": b.daily_l, "capacity_l": b.capacity_l,
                     "inflow_lph": b.inflow_lph, "age_limit_h": b.age_limit_h},
        "phases": [{"days": list(p["days"]), "label": p["label"]} for p in phases],
        "policies": agg.round(3).reset_index().to_dict(orient="records"),
        "headline_policy": HEADLINE,
    }
    (OUT / "tank_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # --- Fig 1: freshness vs. security trade-off ---
    fig, ax = plt.subplots(figsize=(7.5, 5))
    fx = agg.loc[[n for n in agg.index if n.startswith("Sabit kural")]]
    nb = agg.loc[[n for n in agg.index if n.startswith("NABIZ")]]
    ax.plot(fx.mean_age_h, fx.dry_hours, "o-", color="#5B6B6E", label="Sabit kural (k günlük tüketim)")
    for n, r in fx.iterrows():
        ax.annotate(n.split("(")[1].rstrip(")"), (r.mean_age_h, r.dry_hours), textcoords="offset points", xytext=(6, 4), fontsize=8, color="#5B6B6E")
    ax.plot(nb.mean_age_h, nb.dry_hours, "o-", color="#0F7C83", lw=2, label="NABIZ (taban yedek değişiyor)")
    for n, r in nb.iterrows():
        ax.annotate(n.split("(")[1].rstrip(")"), (r.mean_age_h, r.dry_hours), textcoords="offset points", xytext=(6, -10), fontsize=8, color="#0F7C83")
    for n, c, m in [("Şamandıra (hep dolu)", "#E4572E", "s"), ("Sabit takvim (kurulumda girilen)", "#F2B134", "D")]:
        r = agg.loc[n]
        ax.scatter(r.mean_age_h, r.dry_hours, color=c, marker=m, s=60, zorder=3, label=n)
    ax.set_yscale("symlog", linthresh=5)
    ax.set_xlabel("Musluğa gelen suyun ortalama depo yaşı (saat)  ← daha taze")
    ax.set_ylabel("Susuz kalınan saat (166 gün)  ← daha güvenli")
    ax.set_title("Tazelik ve kesinti güvencesi dengesi (20 senaryo ortalaması)", fontsize=11)
    ax.legend(fontsize=8, loc="upper right"); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT / "tank_tradeoff.png", dpi=130); plt.close(fig)

    # --- Fig 2: one week after the schedule changed to daily daytime cuts ---
    s0, s1 = 124 * 24, 131 * 24
    fig, ax = plt.subplots(2, 1, figsize=(11, 5.5), sharex=True)
    h = np.arange(s0, s1) / 24
    sup = traces["Şamandıra (hep dolu)"].supply_on.to_numpy()[s0:s1]
    for a in ax:
        a.fill_between(h, 0, 1, where=~sup, transform=a.get_xaxis_transform(), color="#E4572E", alpha=0.12, step="post")
    for n, c in [("Şamandıra (hep dolu)", "#E4572E"), ("Sabit takvim (kurulumda girilen)", "#F2B134"), (HEADLINE, "#0F7C83")]:
        d = traces[n].iloc[s0:s1]
        ax[0].plot(h, d.level_l / 1000, color=c, lw=1.4, label=n)
        ax[1].plot(h, d.age_h, color=c, lw=1.4)
    ax[0].set_ylabel("Depo (m³)"); ax[1].set_ylabel("Su yaşı (saat)"); ax[1].set_xlabel("Gün")
    ax[0].legend(fontsize=8, ncol=3, loc="upper left")
    ax[0].set_title("Kesinti takvimi her gün 08-22 olduktan sonraki bir hafta (kırmızı: şebekede su yok)", fontsize=11, loc="left")
    fig.tight_layout(); fig.savefig(OUT / "tank_week_trace.png", dpi=130); plt.close(fig)

    # small trace for the web page
    d = {n: traces[n].iloc[s0:s1][["level_l", "age_h"]].round(1).to_dict(orient="list")
         for n in ("Şamandıra (hep dolu)", "Sabit takvim (kurulumda girilen)", HEADLINE)}
    d["supply_on"] = traces[HEADLINE].supply_on.iloc[s0:s1].astype(int).tolist()
    d["start_day"] = 124
    (OUT / "tank_week_trace.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
