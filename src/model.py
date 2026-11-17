"""Placeholder models for a generic time series flow.

- Anomaly: seasonal-median profile (e.g. time-of-day) + robust z-score (MAD).
- Forecast: seasonal naive (mean of the last k seasons).

Both are deliberately simple baselines; swap them for the real model once the
hackathon question is known.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def detect_anomalies(series: pd.Series, season: int = 96, threshold: float = 4.0,
                     smooth: int = 1) -> pd.DataFrame:
    """Flag points whose robust z-score vs the seasonal median profile exceeds threshold.

    `season` = points per cycle (96 for 15-min data with a daily cycle).
    `smooth` > 1 averages the score over a trailing window to catch sustained shifts.
    """
    s = series.astype(float).interpolate(limit_direction="both")
    pos = np.arange(len(s)) % max(1, season)
    profile = s.groupby(pos).median()
    expected = pd.Series(profile.reindex(pos).to_numpy(), index=s.index)
    resid = s - expected
    mad = (resid - resid.median()).abs().median()
    scale = 1.4826 * mad if mad > 0 else (resid.std() or 1.0)
    score = (resid / scale).abs()
    if smooth > 1:
        score = score.rolling(smooth, min_periods=1).mean()
    return pd.DataFrame({
        "value": s,
        "expected": expected,
        "score": score,
        "is_anomaly": score > threshold,
    })


def detect_anomalies_multi(df: pd.DataFrame, season: int = 96, threshold: float = 4.0,
                           smooth: int = 1) -> pd.DataFrame:
    """Multivariate placeholder: max of per-column robust z-scores."""
    scores = pd.DataFrame({
        c: detect_anomalies(df[c], season, threshold, smooth)["score"] for c in df.columns
    })
    score = scores.max(axis=1)
    return pd.DataFrame({
        "score": score,
        "driver": scores.idxmax(axis=1),
        "is_anomaly": score > threshold,
    })


def forecast(series: pd.Series, horizon: int, season: int, n_seasons: int = 3) -> pd.Series:
    """Seasonal naive forecast: average of the same position in the last n seasons."""
    s = series.astype(float).interpolate(limit_direction="both")
    k = max(1, min(n_seasons, len(s) // season))
    hist = s.to_numpy()[-k * season:].reshape(k, season)
    profile = hist.mean(axis=0)
    values = np.resize(profile, horizon)

    step = pd.Series(s.index).diff().median()
    future_idx = pd.date_range(s.index[-1] + step, periods=horizon, freq=step)
    return pd.Series(values, index=future_idx, name="forecast")


def backtest_mae(series: pd.Series, horizon: int, season: int) -> dict[str, float]:
    """Hold out the last `horizon` points; compare seasonal naive vs last-value naive."""
    train, test = series.iloc[:-horizon], series.iloc[-horizon:]
    seasonal = forecast(train, horizon, season).to_numpy()
    naive = np.full(horizon, float(train.iloc[-1]))
    return {
        "mae_seasonal": float(np.mean(np.abs(test.to_numpy() - seasonal))),
        "mae_last_value": float(np.mean(np.abs(test.to_numpy() - naive))),
    }


def classification_scores(y_true: pd.Series, y_pred: pd.Series) -> dict[str, float]:
    """Point-wise precision / recall / F1."""
    t = y_true.astype(bool).to_numpy()
    p = y_pred.astype(bool).to_numpy()
    tp = int((t & p).sum()); fp = int((~t & p).sum()); fn = int((t & ~p).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
