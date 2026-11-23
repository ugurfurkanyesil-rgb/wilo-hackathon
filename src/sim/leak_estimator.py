"""Leak estimator from Modbus-like Level 1 data (pressure + pump running bit).

Idea (docs/v1-simulation-design.md §0, §5): while the pump is stopped, a leak
drains the membrane tank, so the stop interval is T_off ≈ ΔV / Q_leak. Night use
(flushes, taps) can only make T_off SHORTER. So over several nights, the longest
stop intervals form a tight cluster at ΔV / Q_leak; without a leak they are spread
out (waiting times between random uses).

Leak type (pipe vs. WC cistern) uses two physical signatures of the same clean intervals:
- half_ratio: a pipe leak follows Q ∝ p^N1, so it drains the high-pressure half of the
  cycle faster than the low-pressure half; a cistern leak drains at a pressure-
  independent rate. Measured as (time in lower half) / (time in upper half), averaged
  over many cycles and normalised by the installation test (a pipe-like test valve).
- peak_ratio: a cistern refills in pulses, so pressure falls in steps (large 30 s drops
  relative to the mean drop). Visible only when a pulse is larger than ~0.1 bar,
  i.e. in small tanks.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

# Defaults chosen on training seeds in scripts/run_leak.py; see results/summary.md.
CV_MAX = 0.10         # max spread of the long-interval cluster to call it a leak
MIN_CLUSTER = 4       # min number of intervals in the cluster
CLUSTER_FRAC = 0.9    # intervals >= this x 90th percentile form the cluster
MIN_NIGHTS = 3        # cluster must appear on at least this many different nights
BUSY_FRAC = 0.9       # pump running > this share of the night -> "large" leak (SCe)


@dataclass
class Interval:
    t_off_s: float
    night: int
    peak_ratio: float  # 99th pct of 30 s pressure drop / mean 30 s drop (step-likeness)
    half_ratio: float  # time below mid pressure / time above it


def stop_intervals(night: pd.DataFrame, night_no: int = 0, p_mid: float = 3.5) -> list[Interval]:
    """Complete pump-stopped intervals (stop edge -> next start edge) in one night.

    p_mid: midpoint of the controller's start/stop pressures (known setpoints).
    """
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
        peak = half = float("nan")
        if len(seg) > 60:
            m = np.convolve(seg, np.ones(10) / 10, "valid")
            d = m[:-30] - m[30:]
            if len(d) and d.mean() > 1e-4:
                peak = float(np.percentile(d, 99) / d.mean())
        if len(seg) > 120:
            sm = np.convolve(seg, np.ones(31) / 31, "same")[15:-15]
            below = np.flatnonzero(sm < p_mid)
            if len(below):
                tm = below[0] + 15
                half = float((len(seg) - tm) / max(tm, 1))
        out.append(Interval(float(e - s), night_no, peak, half))
    return out


def start_intervals(night: pd.DataFrame, night_no: int = 0) -> list[Interval]:
    """Cycle lengths from the cumulative start counter (Modbus reg. 40077/40081).

    A counter never misses a start, even when it is read only every minute: the pump
    runs ~10 s per cycle, so a coarse "running" bit misses most runs. The cycle length
    (start to next start) is T_off + T_on; T_on is a few seconds and is absorbed by the
    calibration, which uses the same function. Pressure-shape features are not computed.
    """
    c = night["pump1_starts_total"].to_numpy()
    idx = np.flatnonzero(np.diff(c) > 0) + 1
    if len(idx) == 0:
        return []
    marks = np.r_[0, idx]                # simulator starts right after a stop
    return [Interval(float(e - s), night_no, float("nan"), float("nan"))
            for s, e in zip(marks[:-1], marks[1:])]


@dataclass
class Estimate:
    leak_lph: float
    leak_type: str        # none | leak (type not classified) | pipe | reservoir | large (SCe, flow unknown)
    cv: float
    n_cluster: int
    n_intervals: int
    peak_ratio: float = float("nan")
    half_ratio: float = float("nan")
    n_nights: int = 0

    def type_features(self, delta_v_l: float, half_cal: float) -> np.ndarray:
        """Log features plus interactions: which signature is informative depends on
        tank size (pulse vs. 0.1 bar step) and on leak rate."""
        lp, lh = np.log(self.peak_ratio), np.log(self.half_ratio / half_cal)
        lq, ldv = np.log(self.leak_lph), np.log(delta_v_l)
        return np.array([lp, lh, lq, ldv, lh * ldv, lp * ldv, lp * lq, lh * lq])


@dataclass
class TypeModel:
    """Logistic regression for P(reservoir), on standardised features."""
    mean: np.ndarray
    std: np.ndarray
    w: np.ndarray

    def p_reservoir(self, x: np.ndarray) -> float:
        z = np.r_[1.0, (x - self.mean) / self.std]
        return float(1 / (1 + np.exp(-z @ self.w)))


def fit_type_model(X: np.ndarray, y: np.ndarray, l2: float = 1e-3, iters: int = 20000) -> TypeModel:
    """Plain gradient-descent logistic regression. y = 1 for reservoir."""
    mean, std = X.mean(axis=0), X.std(axis=0) + 1e-9
    Z = np.c_[np.ones(len(X)), (X - mean) / std]
    w = np.zeros(Z.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Z @ w))
        w -= 0.5 * (Z.T @ (p - y) / len(y) + l2 * np.r_[0, w[1:]])
    return TypeModel(mean, std, w)


def estimate_leak(nights: list[pd.DataFrame], delta_v_l: float,
                  cv_max: float = CV_MAX, min_cluster: int = MIN_CLUSTER,
                  min_nights: int = MIN_NIGHTS, p_mid: float = 3.5,
                  half_cal: float | None = None, type_model: TypeModel | None = None,
                  use_counter: bool = False) -> Estimate:
    """Leak flow from the cluster of longest stop intervals over several nights.

    If `type_model` and `half_cal` (from calibrate()) are given, the leak type is
    classified; otherwise a detected leak is reported as "leak".
    """
    # SCe: a leak above the zero-flow threshold keeps the pump running all night
    busy = sum(n["pump1_running"].mean() > BUSY_FRAC for n in nights)
    if busy >= min_nights:
        return Estimate(float("nan"), "large", float("nan"), 0, 0, n_nights=int(busy))
    iv = [x for i, n in enumerate(nights)
          for x in (start_intervals(n, i) if use_counter else stop_intervals(n, i, p_mid))]
    if len(iv) < min_cluster:
        return Estimate(0.0, "none", float("nan"), 0, len(iv))
    t = np.array([x.t_off_s for x in iv])
    mask = t >= CLUSTER_FRAC * np.percentile(t, 90)
    cl = t[mask]
    sel = [x for x, m in zip(iv, mask) if m]
    n_n = len({x.night for x in sel})
    cv = float(cl.std() / cl.mean()) if len(cl) > 1 else float("inf")
    peak = float(np.nanmedian([x.peak_ratio for x in sel]))
    half = float(np.nanmedian([x.half_ratio for x in sel]))
    if len(cl) < min_cluster or cv > cv_max or n_n < min_nights:
        return Estimate(0.0, "none", cv, int(len(cl)), len(iv), peak, half, n_n)
    q = float(delta_v_l / np.median(cl) * 3600)
    e = Estimate(q, "leak", cv, int(len(cl)), len(iv), peak, half, n_n)
    if type_model is not None and half_cal:
        x = e.type_features(delta_v_l, half_cal)
        if np.isfinite(x).all():
            e.leak_type = "reservoir" if type_model.p_reservoir(x) > 0.5 else "pipe"
    return e


def calibrate(nights: list[pd.DataFrame], known_lph: float, p_mid: float = 3.5,
              use_counter: bool = False) -> tuple[float, float]:
    """Installation test with a known pipe-like leak (test valve), quiet night.

    Returns (effective ΔV in L, reference half_ratio). ΔV is needed because the pump
    overshoots p_off, so the real drawn volume is a bit larger than the Boyle value.
    """
    iv = [x for n in nights for x in (start_intervals(n) if use_counter else stop_intervals(n, 0, p_mid))]
    t = np.array([x.t_off_s for x in iv])
    if len(t) == 0:                      # e.g. data too coarse to see any pump start
        return float("nan"), float("nan")
    mask = t >= CLUSTER_FRAC * np.percentile(t, 90)
    dv = float(known_lph / 3600 * np.median(t[mask]))
    half = float(np.nanmedian([x.half_ratio for x, m in zip(iv, mask) if m]))
    return dv, half


def baseline_pumped_volume(nights: list[pd.DataFrame], q_pump_lph: float) -> float:
    """Naive: pumped volume / time (= leak + night use). Needs no model."""
    run = np.concatenate([n["pump1_running"].to_numpy() for n in nights])
    return float(run.mean() * q_pump_lph)


def baseline_flow_reading(nights: list[pd.DataFrame]) -> float:
    """Naive Level 2: median of the instantaneous calculated flow register, L/h."""
    f = np.concatenate([n["flow_calc_m3h"].to_numpy() for n in nights])
    return float(np.median(f) * 1000)


def cost_tl_month(leak_lph: float, water_tl_m3: float = 44.63, waste_tl_m3: float = 22.28) -> float:
    """İSKİ residential tier 1, November 2026, VAT excluded (Endeks24, 19.11.2026; updated monthly)."""
    return leak_lph * 24 * 30 / 1000 * (water_tl_m3 + waste_tl_m3)
