"""Data loading: generic time series from CSV/Excel, plus a synthetic sample.

The synthetic sample is illustrative only (not real measurements). It mimics a
pump with a daily demand cycle and a few injected faults so the demo runs
end-to-end without any download.
"""
from __future__ import annotations

from pathlib import Path
from typing import IO

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "sample" / "synthetic_pump.csv"
LABEL_COL = "anomaly"


def make_synthetic(days: int = 14, freq: str = "15min", seed: int = 42) -> pd.DataFrame:
    """Synthetic pump time series with labelled anomalies."""
    rng = np.random.default_rng(seed)
    n = int(pd.Timedelta(days=days) / pd.Timedelta(freq))
    idx = pd.date_range("2026-01-01", periods=n, freq=freq, name="timestamp")
    hours = idx.hour.to_numpy() + idx.minute.to_numpy() / 60
    weekday = (idx.day_of_week.to_numpy() < 5).astype(float)

    daily = np.sin(2 * np.pi * (hours - 6) / 24)
    flow = 20 + 8 * daily + 2 * weekday + rng.normal(0, 0.8, n)
    pressure = 4.0 - 0.03 * (flow - 20) + rng.normal(0, 0.05, n)
    current = 5 + 0.15 * flow + rng.normal(0, 0.1, n)
    label = np.zeros(n, dtype=int)

    def window(day: float, length_h: float) -> slice:
        start = int(day * 96)
        return slice(start, start + int(length_h * 4))

    # 1) current spikes (e.g. bearing / clogging)
    s = window(3.4, 1.5)
    current[s] += rng.normal(2.5, 0.4, s.stop - s.start)
    label[s] = 1
    # 2) sustained pressure drop with higher flow (leak-like)
    s = window(7.1, 6)
    pressure[s] -= 0.35
    flow[s] += 3
    label[s] = 1
    # 3) slow current drift (wear)
    s = window(11.0, 12)
    current[s] += np.linspace(0, 1.5, s.stop - s.start)
    label[s] = 1

    return pd.DataFrame(
        {"flow_m3h": flow, "pressure_bar": pressure, "current_a": current, LABEL_COL: label},
        index=idx,
    ).round(4)


def load_timeseries(source: str | Path | IO[bytes], name: str | None = None,
                    time_col: str | None = None) -> pd.DataFrame:
    """Load CSV/XLSX into a DataFrame indexed by a sorted DatetimeIndex.

    If `time_col` is None, the first column that parses as datetime is used.
    Only numeric columns are kept.
    """
    fname = (name or str(getattr(source, "name", source))).lower()
    if fname.endswith((".xlsx", ".xls")):
        df = pd.read_excel(source)
    else:
        df = pd.read_csv(source, sep=None, engine="python")

    if time_col is None:
        for col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                parsed = pd.to_datetime(df[col], errors="coerce")
                if parsed.notna().mean() > 0.9:
                    time_col = col
                    break
    if time_col is None:
        raise ValueError("No datetime column found; pass time_col explicitly.")

    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
    df = df.dropna(subset=[time_col]).set_index(time_col).sort_index()
    df.index.name = "timestamp"
    return df.select_dtypes(include="number")


def load_sample() -> pd.DataFrame:
    """Load the committed sample; regenerate it if missing."""
    if not SAMPLE_PATH.exists():
        SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)
        make_synthetic().to_csv(SAMPLE_PATH)
    return load_timeseries(SAMPLE_PATH)


def points_per_day(index: pd.DatetimeIndex) -> int:
    """Number of samples per day, inferred from the median time step."""
    step = pd.Series(index).diff().median()
    if pd.isna(step) or step <= pd.Timedelta(0):
        return 1
    return max(1, int(round(pd.Timedelta(days=1) / step)))


if __name__ == "__main__":
    SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    make_synthetic().to_csv(SAMPLE_PATH)
    print(f"Wrote {SAMPLE_PATH}")
