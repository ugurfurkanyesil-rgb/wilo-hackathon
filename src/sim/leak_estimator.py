"""Leak estimator from Modbus-like Level 1 data (pressure + pump running bit).

Idea (docs/v1-simulation-design.md §0, §5): while the pump is stopped, a leak
drains the membrane tank, so the stop interval is T_off ≈ ΔV / Q_leak. Night use
(flushes, taps) can only make T_off SHORTER. So over several nights, the longest
stop intervals form a tight cluster at ΔV / Q_leak; without a leak they are spread
out (waiting times between random uses).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

# Defaults chosen on training seeds in scripts/run_leak.py; see results/summary.md.
CV_MAX = 0.10         # max spread of the long-interval cluster to call it a leak
MIN_CLUSTER = 4       # min number of intervals in the cluster
CLUSTER_FRAC = 0.9    # intervals >= this x 90th percentile form the cluster

MIN_NIGHTS = 3       # cluster must appear on at least this many different nights


@dataclass
class Interval:
    t_off_s: float
    night: int
    peak_ratio: float  # 99th pct of 30 s pressure drop / mean 30 s drop (step-likeness)


def stop_intervals(night: pd.DataFrame, night_no: int = 0) -> list[Interval]:
    """Complete pump-stopped intervals (stop edge -> next start edge) in one night."""
    run = night["pump1_running"].to_numpy()
    p = night["pressure_bar"].to_numpy()
    starts = np.flatnonzero((run[1:] == 1) & (run[:-1] == 0)) + 1
    stops = np.flatnonzero((run[1:] == 0) & (run[:-1] == 1)) + 1
    if run[0] == 0:
        stops = np.r_[0, stops]          # simulator starts right after a stop
    out = []
    for s in stops:
        nxt = starts[starts > s]
        if len(nxt) == 0:
            break                        # censored at window end
        e = nxt[0]
        seg = p[s:e]
        ratio = float("nan")
        if len(seg) > 60:
            m = np.convolve(seg, np.ones(10) / 10, "valid")
            d = m[:-30] - m[30:]
            if len(d) and d.mean() > 1e-4:
                ratio = float(np.percentile(d, 99) / d.mean())
        out.append(Interval(float(e - s), night_no, ratio))
    return out


@dataclass
class Estimate:
    leak_lph: float
    leak_type: str        # none | leak
    cv: float
    n_cluster: int
    n_intervals: int
    peak_ratio: float = float("nan")
    n_nights: int = 0



def estimate_leak(nights: list[pd.DataFrame], delta_v_l: float,
                  cv_max: float = CV_MAX, min_cluster: int = MIN_CLUSTER,
                  min_nights: int = MIN_NIGHTS) -> Estimate:
    """Leak flow from the cluster of longest stop intervals over several nights.

    Leak type is NOT classified: with 0.1 bar pressure steps the pipe/reservoir
    signature (smooth vs pulsed drain) was not separable in simulation for 50-100 L
    tanks (see results/summary.md). `peak_ratio` is kept as a candidate feature.
    """
    iv = [x for i, n in enumerate(nights) for x in stop_intervals(n, i)]
    if len(iv) < min_cluster:
        return Estimate(0.0, "none", float("nan"), 0, len(iv))
    t = np.array([x.t_off_s for x in iv])
    mask = t >= CLUSTER_FRAC * np.percentile(t, 90)
    cl = t[mask]
    n_n = len({x.night for x, m in zip(iv, mask) if m})
    cv = float(cl.std() / cl.mean()) if len(cl) > 1 else float("inf")
    ratio = float(np.nanmedian([x.peak_ratio for x, m in zip(iv, mask) if m]))
    if len(cl) < min_cluster or cv > cv_max or n_n < min_nights:
        return Estimate(0.0, "none", cv, int(len(cl)), len(iv), ratio, n_n)
    q = float(delta_v_l / np.median(cl) * 3600)
    return Estimate(q, "leak", cv, int(len(cl)), len(iv), ratio, n_n)


def calibrate_delta_v(nights: list[pd.DataFrame], known_lph: float) -> float:
    """Effective ΔV (L) from an installation test with a known leak (e.g. a test valve).

    Needed because the pump overshoots p_off, so the real drawn volume is a bit
    larger than the Boyle value from nameplate pressures.
    """
    t = np.array([x.t_off_s for n in nights for x in stop_intervals(n)])
    cl = t[t >= CLUSTER_FRAC * np.percentile(t, 90)]
    return float(known_lph / 3600 * np.median(cl))


def baseline_pumped_volume(nights: list[pd.DataFrame], q_pump_lph: float) -> float:
    """Naive: pumped volume / time (= leak + night use). Needs no model."""
    run = np.concatenate([n["pump1_running"].to_numpy() for n in nights])
    return float(run.mean() * q_pump_lph)


def baseline_flow_reading(nights: list[pd.DataFrame]) -> float:
    """Naive Level 2: median of the instantaneous calculated flow register, L/h."""
    f = np.concatenate([n["flow_calc_m3h"].to_numpy() for n in nights])
    return float(np.median(f) * 1000)


def cost_tl_month(leak_lph: float, water_tl_m3: float = 35.26, waste_tl_m3: float = 17.62) -> float:
    """İSKİ residential tariff Jan 2026, VAT excluded (design doc §7)."""
    return leak_lph * 24 * 30 / 1000 * (water_tl_m3 + waste_tl_m3)
