"""Robustness checks for the leak estimator, beyond the main test set (run_leak.py).

A. SCe control (frequency converter, zero-flow test) instead of SC
B. Membrane tank losing its air pre-charge after the installation test
C. Noisier pressure sensor, D. busier nights
E. Coarser data (10 s / 60 s / 5 min polling, e.g. via a cloud gateway instead of a local 1 s reader)
F. Extra pump starts caused by a leak (load on the pump)

The pipe/cistern classifier is the one fitted in run_leak.py (results/leak_summary.json);
it is NOT refitted here. Run run_leak.py first.

Run:  python scripts/run_checks.py               (all groups)
      python scripts/run_checks.py --groups E,F   (only some; merged with earlier results)
Out:  results/checks_summary.json, results/checks_runs.csv
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.sim import leak_estimator as est  # noqa: E402
from src.sim.leak_sim import Building, Leak, NightUse, simulate_nights  # noqa: E402

OUT = ROOT / "results"
SEEDS = range(100, 120)
TANKS = [24, 50, 100]
NIGHTS = 7


def load_model() -> tuple[est.TypeModel, float]:
    s = json.loads((OUT / "leak_summary.json").read_text(encoding="utf-8"))
    m = s["type_model"]
    return est.TypeModel(np.array(m["mean"]), np.array(m["std"]), np.array(m["w"])), s["cv_max"]


def t_on_median(nights) -> float:
    """Median pump run length (s) over the nights: used to re-estimate ΔV = Q_pump · T_on."""
    out = []
    for n in nights:
        r = n["pump1_running"].to_numpy()
        up = np.flatnonzero((r[1:] == 1) & (r[:-1] == 0)) + 1
        dn = np.flatnonzero((r[1:] == 0) & (r[:-1] == 1)) + 1
        for u in up:
            d = dn[dn > u]
            if len(d):
                out.append(d[0] - u)
    return float(np.median(out)) if out else float("nan")


def poll(nights, k: int):
    """Sample-and-hold every k seconds: what a reader polling at k s would see."""
    if k <= 1:
        return nights
    return [n.iloc[::k].reindex(n.index, method="ffill") for n in nights]


def run_case(group: str, kind: str, lph: float, seed: int, model, cv_max: float,
             mode: str = "SC", q_zf: float = 30.0, p0_loss: float = 0.0, noise: float = 0.02,
             use_range=(0.5, 3.0), feats: list | None = None, poll_s: int = 1,
             use_counter: bool = False) -> dict:
    rng = np.random.default_rng(seed)
    V0 = float(rng.choice(TANKS))
    use = NightUse(rate_per_h=float(rng.uniform(*use_range)))
    p_on = 3.5 if mode == "SCe" else 3.0
    kw = dict(V0=V0, p_on=p_on, mode=mode, q_zf_lph=q_zf, noise_bar=noise)
    p_mid = (p_on + 4.0) / 2
    b_inst = Building(**kw)                                   # at installation
    cal_n = poll(simulate_nights(b_inst, NightUse(rate_per_h=0.3), Leak("pipe", 10), 3, seed + 10_000), poll_s)
    dv, half_cal = est.calibrate(cal_n, 10, p_mid=p_mid, use_counter=use_counter)
    b_now = Building(**kw, p0=b_inst.p0 - p0_loss)            # later, maybe lost pre-charge
    nights = poll(simulate_nights(b_now, use, Leak(kind, lph), NIGHTS, seed), poll_s)
    e = est.estimate_leak(nights, dv, cv_max=cv_max, p_mid=p_mid, half_cal=half_cal,
                          type_model=None if use_counter else model, use_counter=use_counter)
    if feats is not None and e.leak_type in ("pipe", "reservoir"):
        feats.append((e.type_features(dv, half_cal), kind == "reservoir"))
    row = {"group": group, "mode": mode, "q_zf": q_zf, "p0_loss": p0_loss, "noise": noise, "poll_s": poll_s, "counter": use_counter,
           "kind": kind, "true_lph": lph, "seed": seed, "V0": V0, "est_type": e.leak_type,
           "est_lph": e.leak_lph, "detected": e.leak_type != "none",
           "type_ok": e.leak_type == kind}
    if p0_loss > 0 and e.leak_type in ("pipe", "reservoir"):
        # mitigation: re-derive ΔV from pump run time and nominal pump flow (2 m3/h [V]),
        # scaled by the ratio seen at installation
        k = dv / (b_inst.q_pump_lps * t_on_median(cal_n))
        dv_now = k * b_now.q_pump_lps * t_on_median(nights)
        row["est_lph_recal"] = e.leak_lph * dv_now / dv
    return row


def starts_per_hour(V0: float, lph: float, use_rate: float, seed: int = 7) -> float:
    b = Building(V0=V0)
    nights = simulate_nights(b, NightUse(rate_per_h=use_rate), Leak("pipe" if lph else "none", lph), 3, seed)
    starts = sum(int(((n.pump1_running.diff() == 1)).sum()) for n in nights)
    return starts / (3 * 5)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", default="A,B,C,D,E,F")
    groups = set(ap.parse_args().groups.split(","))
    model, cv_max = load_model()
    rows = []
    rates = [2, 5, 10, 20, 50]
    if "A" in groups:
        print("A. SCe ...")
        # the SC-trained classifier does not transfer to SCe (different pressure band);
        # fit an SCe classifier on separate training seeds, then test
        feats: list = []
        for kind, lph in [(k, r) for k in ("pipe", "reservoir") for r in rates]:
            for s in range(1, 16):
                run_case("A_train", kind, lph, s, model, cv_max, mode="SCe", feats=feats)
        X = np.vstack([f for f, _ in feats]); y = np.array([float(t) for _, t in feats])
        ok = np.isfinite(X).all(axis=1)
        model_sce = est.fit_type_model(X[ok], y[ok])
        for kind, lph in [("none", 0)] + [(k, r) for k in ("pipe", "reservoir") for r in rates]:
            for s in SEEDS:
                rows.append(run_case("A_SCe_SCmodel", kind, lph, s, model, cv_max, mode="SCe"))
                rows.append(run_case("A_SCe", kind, lph, s, model_sce, cv_max, mode="SCe"))
        for q_zf in (15, 60):
            for lph in (20, 50):
                for s in SEEDS:
                    rows.append(run_case("A_SCe_qzf", "pipe", lph, s, model_sce, cv_max, mode="SCe", q_zf=q_zf))
    if "B" in groups:
        print("B. pre-charge loss ...")
        for loss in (0.3, 0.6, 1.0):
            for kind, lph in [("none", 0), ("pipe", 10), ("pipe", 20), ("reservoir", 20)]:
                for s in SEEDS:
                    rows.append(run_case("B_precharge", kind, lph, s, model, cv_max, p0_loss=loss))
    if "C" in groups or "D" in groups:
        print("C/D. noise and busy nights ...")
        for kind, lph in [("none", 0), ("pipe", 10), ("pipe", 20), ("reservoir", 10), ("reservoir", 20)]:
            for s in SEEDS:
                if "C" in groups:
                    rows.append(run_case("C_noise", kind, lph, s, model, cv_max, noise=0.05))
                if "D" in groups:
                    rows.append(run_case("D_busy", kind, lph, s, model, cv_max, use_range=(3.0, 5.0)))
    if "E" in groups:
        print("E. polling interval ...")
        for k in (10, 60, 300):
            for kind, lph in [("none", 0)] + [(kk, r) for kk in ("pipe", "reservoir") for r in (5, 10, 20, 50)]:
                for s in SEEDS:
                    rows.append(run_case("E_poll", kind, lph, s, model, cv_max, poll_s=k))
                    rows.append(run_case("E_poll_counter", kind, lph, s, model, cv_max, poll_s=k, use_counter=True))
    new = pd.DataFrame(rows)
    csv = OUT / "checks_runs.csv"
    if csv.exists() and groups != {"A", "B", "C", "D", "E", "F"}:
        old = pd.read_csv(csv)
        old = old[~old.group.str[0].isin(groups)]
        df = pd.concat([old, new], ignore_index=True)
    else:
        df = new
    if "poll_s" in df:
        df["poll_s"] = df["poll_s"].fillna(1).astype(int)
    df.to_csv(csv, index=False)

    def summ(d: pd.DataFrame) -> dict:
        leak = d[d.kind != "none"]
        est_ok = leak[leak.est_type.isin(["pipe", "reservoir", "leak"])]
        typed = leak[leak.est_type.isin(["pipe", "reservoir"])]
        out = {
            "false_alarm": float(d[d.kind == "none"].detected.mean()) if (d.kind == "none").any() else None,
            "detection": float(leak.detected.mean()) if len(leak) else None,
            "mape": float(((est_ok.est_lph - est_ok.true_lph).abs() / est_ok.true_lph).mean()) if len(est_ok) else None,
            "type_acc": float(typed.type_ok.mean()) if len(typed) else None,
            "large_flag": float((leak.est_type == "large").mean()) if len(leak) else None,
            "n": int(len(d)),
        }
        if "est_lph_recal" in d and d.est_lph_recal.notna().any():
            r = d[d.est_lph_recal.notna() & (d.kind != "none")]
            out["mape_recal"] = float(((r.est_lph_recal - r.true_lph).abs() / r.true_lph).mean())
        return out

    old_res = json.loads((OUT / "checks_summary.json").read_text(encoding="utf-8")) if (OUT / "checks_summary.json").exists() else {}
    res = {}
    a = df[df.group == "A_SCe"]
    res["A_SCe_all"] = summ(a)
    res["A_SCe_with_SC_classifier"] = summ(df[df.group == "A_SCe_SCmodel"])
    res["A_SCe_by_rate"] = {f"{k}_{int(r)}": summ(g) for (k, r), g in a[a.kind != "none"].groupby(["kind", "true_lph"])}
    res["A_SCe_qzf"] = {f"qzf{int(q)}_pipe{int(r)}": summ(g) for (q, r), g in df[df.group == "A_SCe_qzf"].groupby(["q_zf", "true_lph"])}
    res["B_precharge"] = {f"loss{l}": summ(g) for l, g in df[df.group == "B_precharge"].groupby("p0_loss")}
    res["C_noise_0.05bar"] = summ(df[df.group == "C_noise"])
    res["D_busy_3to5_per_h"] = summ(df[df.group == "D_busy"])
    res["E_poll"] = {f"{int(k)}s": summ(g) for k, g in df[df.group == "E_poll"].groupby("poll_s")}
    res["E_poll_counter"] = {f"{int(k)}s": summ(g) for k, g in df[df.group == "E_poll_counter"].groupby("poll_s")}
    if "F" in groups:
        print("F. extra pump starts ...")
        f = {}
        for V0 in TANKS:
            dv = Building(V0=V0).delta_v
            f[f"{V0}L"] = {"delta_v_l": round(dv, 2), **{f"leak{l}_use{u}": round(starts_per_hour(V0, l, u), 2)
                                                         for l in (0, 5, 10, 20) for u in (0.0, 1.5)}}
        res["F_starts_per_hour"] = f
    elif "F_starts_per_hour" in old_res:
        res["F_starts_per_hour"] = old_res["F_starts_per_hour"]
    res = json.loads(json.dumps(res, default=lambda x: None).replace("NaN", "null"))
    (OUT / "checks_summary.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
