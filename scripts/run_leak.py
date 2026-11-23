"""V1 leak experiment: simulate nights, estimate leak, compare with naive baselines.

Run:  python scripts/run_leak.py
Out:  results/leak_*.png, results/leak_metrics.csv, results/leak_summary.json
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
from src.sim import leak_estimator as est  # noqa: E402
from src.sim.leak_sim import Building, Leak, NightUse, simulate_nights  # noqa: E402

OUT = ROOT / "results"
NIGHTS = 7
RATES = [2, 3, 5, 10, 20, 50]
SCENARIOS = [("none", 0)] + [(k, r) for k in ("pipe", "reservoir") for r in RATES]
TRAIN_SEEDS = range(1, 16)
TEST_SEEDS = range(100, 120)
TANKS = [24, 50, 100]  # L [V]


def one_run(kind: str, lph: float, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    b = Building(V0=float(rng.choice(TANKS)))
    use = NightUse(rate_per_h=float(rng.uniform(0.5, 3.0)))
    # installation test: known 10 L/h test valve, quiet night
    dv, half_cal = est.calibrate(simulate_nights(b, NightUse(rate_per_h=0.3), Leak("pipe", 10), 3, seed + 10_000), 10)
    nights = simulate_nights(b, use, Leak(kind, lph), NIGHTS, seed)
    return {"kind": kind, "lph": lph, "seed": seed, "V0": b.V0, "use_rate": use.rate_per_h,
            "dv": dv, "half_cal": half_cal, "nights": nights}


def evaluate(runs: list[dict], cv_max: float, model=None) -> pd.DataFrame:
    rows = []
    for r in runs:
        e = est.estimate_leak(r["nights"], r["dv"], cv_max=cv_max, half_cal=r["half_cal"], type_model=model)
        rows.append({
            "kind": r["kind"], "true_lph": r["lph"], "seed": r["seed"], "V0": r["V0"],
            "use_rate": round(r["use_rate"], 2), "est_lph": round(e.leak_lph, 2),
            "detected": e.leak_type != "none", "est_type": e.leak_type,
            "type_ok": e.leak_type == r["kind"],
            "feat": e.type_features(r["dv"], r["half_cal"]) if e.leak_type != "none" else None,
            "naive_pumped_lph": round(est.baseline_pumped_volume(r["nights"], 2000), 2),
            "naive_flow_lph": est.baseline_flow_reading(r["nights"]),
        })
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    print("simulating train runs ...")
    train = [one_run(k, r, s) for k, r in SCENARIOS for s in TRAIN_SEEDS]
    # pick the loosest cluster threshold with zero false alarms on no-leak training runs
    best = None
    for cv in np.arange(0.04, 0.26, 0.02):
        df = evaluate(train, cv)
        fa = df[df.kind == "none"].detected.mean()
        det = df[df.kind != "none"].detected.mean()
        if fa == 0 and (best is None or det > best[1]):
            best = (round(float(cv), 2), det)
    cv_max = best[0]
    print(f"chosen CV_MAX = {cv_max}")
    tr = evaluate(train, cv_max)
    tr = tr[tr.detected & (tr.kind != "none")]
    X = np.vstack(tr.feat.to_numpy()); y = (tr.kind == "reservoir").to_numpy(float)
    ok = np.isfinite(X).all(axis=1)
    model = est.fit_type_model(X[ok], y[ok])
    print("type model w", np.round(model.w, 3), "train acc", round(float(((np.array([model.p_reservoir(x) for x in X[ok]]) > 0.5) == y[ok]).mean()), 3))

    print("simulating test runs ...")
    test = [one_run(k, r, s) for k, r in SCENARIOS for s in TEST_SEEDS]
    df = evaluate(test, cv_max, model)

    # robustness: leak physics different from training (N1, cistern refill volume)
    rob = []
    for label, lk in [("boru N1=1.0", lambda r: Leak("pipe", r, n1=1.0)),
                      ("rezervuar 0.3 L", lambda r: Leak("reservoir", r, v_trig=0.3)),
                      ("rezervuar 0.8 L", lambda r: Leak("reservoir", r, v_trig=0.8))]:
        for rate in (10, 20, 50):
            for seed in range(200, 210):
                rng = np.random.default_rng(seed)
                b = Building(V0=float(rng.choice(TANKS)))
                dv, hc = est.calibrate(simulate_nights(b, NightUse(rate_per_h=0.3), Leak("pipe", 10), 3, seed + 10_000), 10)
                leak = lk(rate)
                e = est.estimate_leak(simulate_nights(b, NightUse(rate_per_h=float(rng.uniform(0.5, 3))), leak, NIGHTS, seed),
                                      dv, cv_max=cv_max, half_cal=hc, type_model=model)
                if e.leak_type != "none":
                    rob.append({"case": label, "ok": e.leak_type == leak.kind})
    rob = pd.DataFrame(rob).groupby("case").ok.agg(["mean", "count"])
    print(rob)
    df.drop(columns="feat").to_csv(OUT / "leak_metrics.csv", index=False)

    leak = df[df.kind != "none"]
    rows = []
    for (kind, lph), g in leak.groupby(["kind", "true_lph"]):
        d = g[g.detected]
        rows.append({
            "kind": kind, "true_lph": lph,
            "detection_rate": g.detected.mean(),
            "mae_lph_detected": (d.est_lph - d.true_lph).abs().mean() if len(d) else None,
            "type_acc_detected": d.type_ok.mean() if len(d) else None,
            "mae_naive_pumped": (g.naive_pumped_lph - g.true_lph).abs().mean(),
            "naive_flow_median": g.naive_flow_lph.median(),
        })
    by = pd.DataFrame(rows)
    by_rate = leak.groupby("true_lph").detected.mean()
    min_90 = next((int(r) for r in RATES if by_rate.get(r, 0) >= 0.9 and all(by_rate.get(x, 0) >= 0.9 for x in RATES if x >= r)), None)
    det = leak[leak.detected]
    summary = {
        "nights_per_estimate": NIGHTS, "night_window": "00:00-05:00", "cv_max": cv_max,
        "n_test_runs": int(len(df)),
        "false_alarm_rate_no_leak": float(df[df.kind == "none"].detected.mean()),
        "min_leak_lph_90pct_detection": min_90,
        "detection_rate_by_tank_L": {int(k): round(float(v), 3) for k, v in leak.groupby("V0").detected.mean().items()},
        "type_accuracy_detected": float(det.type_ok.mean()),
        "type_accuracy_by_tank_L": {int(k): round(float(v), 3) for k, v in det.groupby("V0").type_ok.mean().items()},
        "type_model": {"features": ["lp=log peak_ratio", "lh=log half_ratio/half_cal", "lq=log q", "ldv=log dV", "lh*ldv", "lp*ldv", "lp*lq", "lh*lq"],
                       "mean": model.mean.round(4).tolist(), "std": model.std.round(4).tolist(), "w": model.w.round(4).tolist()},
        "type_accuracy_robustness": {k: {"acc": round(float(v["mean"]), 3), "n": int(v["count"])} for k, v in rob.iterrows()},
        "mape_detected": float(((det.est_lph - det.true_lph).abs() / det.true_lph).mean()),
        "naive_pumped_mape": float(((leak.naive_pumped_lph - leak.true_lph).abs() / leak.true_lph).mean()),
        "naive_flow_median_lph": float(leak.naive_flow_lph.median()),
        "by_scenario": by.round(3).to_dict(orient="records"),
    }
    (OUT / "leak_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "by_scenario"}, indent=2))
    print(by.round(2).to_string())

    # --- Fig 1: S-ARG, one night without leak vs 5 L/h pipe leak ---
    b = Building()
    rng_use = NightUse(rate_per_h=1.0)
    n0 = simulate_nights(b, rng_use, Leak("none", 0), 1, 7)[0]
    n5 = simulate_nights(b, rng_use, Leak("pipe", 5), 1, 7)[0]
    fig, ax = plt.subplots(2, 1, figsize=(11, 5.5), sharex=True)
    for a, n, title in [(ax[0], n0, "Kaçak yok"), (ax[1], n5, "Boru kaçağı 5 L/sa")]:
        h = (n.index - n.index[0]).total_seconds() / 3600
        a.plot(h, n.pressure_bar, lw=0.6, color="#0F7C83", label="Basınç (0,1 bar adımlı)")
        a.fill_between(h, 2.5, 2.5 + 0.4 * n.pump1_running, color="#E4572E", alpha=0.6, step="post", label="Pompa çalışıyor")
        a.set_ylabel("bar"); a.set_ylim(2.4, 4.4); a.set_title(title, loc="left", fontsize=11)
        med_flow = n.flow_calc_m3h.median() * 1000
        a.text(4.98, 4.25, f"Hesaplanmış debi medyanı: {med_flow:.0f} L/sa", ha="right", fontsize=9)
    ax[0].legend(loc="lower left", fontsize=8, ncol=2)
    ax[1].set_xlabel("Gece saati (00:00'dan itibaren)")
    fig.suptitle("Kaçak, pompanın düzenli duruş-kalkış döngüsünde görünür; anlık debi okuması sıfırdır", fontsize=12)
    fig.tight_layout(); fig.savefig(OUT / "leak_night_trace.png", dpi=130); plt.close(fig)

    # --- Fig 2: estimated vs true ---
    fig, ax = plt.subplots(figsize=(6.5, 5))
    for kind, c in [("pipe", "#0F7C83"), ("reservoir", "#E4572E")]:
        d = leak[(leak.kind == kind) & leak.detected]
        ax.scatter(d.true_lph * (1 + 0.04 * (kind == "reservoir")), d.est_lph, s=14, alpha=0.6, c=c,
                   label={"pipe": "Boru", "reservoir": "Rezervuar"}[kind])
    p = leak.groupby("true_lph").naive_pumped_lph.median()
    ax.plot(p.index, p.values, "k--", lw=1, label="Basit yöntem: pompalanan hacim / süre (medyan)")
    ax.plot([1, 60], [1, 60], color="#999", lw=0.8)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("Gerçek kaçak (L/sa)"); ax.set_ylabel("Tahmin (L/sa)")
    ax.set_title("NABIZ kaçak tahmini (yalnız tespit edilenler), test kümesi", fontsize=11)
    ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(OUT / "leak_estimate_vs_true.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    main()
