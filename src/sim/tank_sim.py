"""Apartment storage tank ("Taze Depo") simulator: hourly, with supply interruptions.

Compares fill policies on two goals that pull against each other:
- freshness: age of the water delivered from the tank (fully mixed model, EPANET "MIXED")
- security: hours in which the tank cannot meet demand during a supply cut

All numbers are assumptions [V] unless marked [K]; see docs/taze-depo-validation.md.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

L_PER_PERSON_DAY = 146  # [K, secondary] SYGM 2021 urban use, via Ekonomi Gazetesi 26.03.2026

# relative hourly use profile (morning + evening peaks) [V]
PROFILE = np.array([0.3, 0.2, 0.15, 0.15, 0.2, 0.5, 1.2, 1.8, 1.6, 1.2, 1.0, 1.0,
                    1.1, 1.0, 0.9, 0.9, 1.0, 1.3, 1.6, 1.7, 1.5, 1.2, 0.8, 0.5])
PROFILE = PROFILE / PROFILE.sum()


@dataclass
class TankBuilding:
    persons: int = 36             # 12 flats x 3 [V]
    capacity_l: float = 10_000    # ≈1.9 days of use [V]
    v_min_l: float = 500          # pump dry-run protection [V]
    inflow_lph: float = 4_000     # mains refill rate with valve open [V]
    age_limit_h: float = 48       # freshness limit used for the KPI [V]

    @property
    def daily_l(self) -> float:
        return self.persons * L_PER_PERSON_DAY


def make_demand(b: TankBuilding, days: int, rng: np.random.Generator) -> np.ndarray:
    """Hourly demand (L). Day factor, weekend bump and hourly noise are [V]."""
    d = np.empty(days * 24)
    for day in range(days):
        f = rng.lognormal(0, 0.1) * (1.1 if day % 7 in (5, 6) else 1.0)
        d[day * 24:(day + 1) * 24] = b.daily_l * f * PROFILE * rng.lognormal(0, 0.2, 24)
    return d


def make_supply(days: int, rng: np.random.Generator) -> tuple[np.ndarray, list[dict]]:
    """Hourly mains availability (True = water). Scenario [V], built from two facts:
    İzmir 2025 changed its cut frequency (every 3rd day -> every 2nd day -> every day) [K, news];
    Ankara 2025 supplied water only in low-use hours [K, Habertürk/AA]. Window times and the
    unannounced cuts are assumptions [V]."""
    on = np.ones(days * 24, dtype=bool)
    phases = [
        {"days": (0, 60), "every": 3, "start": 23, "hours": 6, "label": "3 günde 1, 23-05"},
        {"days": (60, 120), "every": 2, "start": 9, "hours": 12, "label": "2 günde 1, 09-21"},
        {"days": (120, days), "every": 1, "start": 8, "hours": 14, "label": "her gün, 08-22"},
    ]
    for ph in phases:
        for day in range(*ph["days"]):
            if (day - ph["days"][0]) % ph["every"] == 0:
                s = day * 24 + ph["start"]
                on[s:s + ph["hours"]] = False
    # unannounced cuts (e.g. pipe bursts): ~2 per month, 4-16 h [V]
    t = rng.exponential(15 * 24)
    while t < days * 24:
        on[int(t):int(t) + int(rng.uniform(4, 16))] = False
        t += rng.exponential(15 * 24)
    return on, phases


# ---------------- policies: return target level (L) for hour t ----------------

class Float:
    """Today: float valve keeps the tank full."""
    name = "Şamandıra (hep dolu)"

    def target(self, t, hist, b):
        return b.capacity_l


class FixedDay:
    """Fixed rule: keep k days of average use (k=1 is HSE-style), no outage awareness."""

    def __init__(self, k: float = 1.0):
        self.k = k
        self.name = f"Sabit kural ({k:g} günlük)"

    def target(self, t, hist, b):
        return self.k * b.daily_l


class FixedSchedule:
    """Timer configured once at install (Tanktronic-like): fill up before the
    outage schedule known at that time (every 3rd day from 23:00), else 1 day."""
    name = "Sabit takvim (kurulumda girilen)"

    def target(self, t, hist, b):
        day, hour = divmod(t, 24)
        if day % 3 == 0 and 15 <= hour <= 23:
            return b.capacity_l
        return b.daily_l


class Nabiz:
    """Learns the building's own outage pattern and demand, sets the level just high
    enough to bridge the next expected cut.

    - Supply state is observed every hour with a short valve-open test [V]
      (valve open, level not rising -> mains is off).
    - Outage probability per hour-of-day from the last `window_d` days.
    - Demand forecast: q-th percentile of the same hour over the last 28 days.
    """
    def __init__(self, window_d: int = 10, p_cut: float = 0.25, q: float = 90,
                 base_h: int = 12, lead_h: int = 8):
        self.window_d, self.p_cut, self.q, self.base_h, self.lead_h = window_d, p_cut, q, base_h, lead_h
        self.name = f"NABIZ (taban {base_h} sa)"

    def target(self, t, hist, b):
        if t < 48:
            return b.capacity_l                          # learning period: behave like today
        hour = t % 24
        sup = hist["supply"][max(0, t - self.window_d * 24):t]
        dem = hist["demand"][max(0, t - 28 * 24):t]
        n_sup = len(sup) // 24 * 24
        p_off = 1 - sup[-n_sup:].reshape(-1, 24).mean(axis=0) if n_sup else np.zeros(24)
        n_dem = len(dem) // 24 * 24
        qd = np.percentile(dem[-n_dem:].reshape(-1, 24), self.q, axis=0)
        # hours h = t .. t+47 (index by hour of day, rolled so that 0 = now)
        hrs = (hour + np.arange(48)) % 24
        cut = p_off[hrs] > self.p_cut
        base = qd[hrs[:self.base_h]].sum()
        need = 0.0
        if cut[:self.lead_h + 1].any():
            k0 = int(np.argmax(cut))                     # first expected cut hour
            k1 = k0
            while k1 < 47 and cut[k1 + 1]:
                k1 += 1
            need = qd[hrs[:k1 + 1]].sum()                # bridge until the cut ends
        return float(np.clip(max(base, need) * 1.15, b.v_min_l * 2, b.capacity_l))


def run(policy, b: TankBuilding, demand: np.ndarray, supply: np.ndarray) -> pd.DataFrame:
    n = len(demand)
    v, age = b.capacity_l, 24.0
    hist = {"supply": supply, "demand": demand}   # policies only read indices < t
    rows = np.zeros((n, 6))
    for t in range(n):
        tgt = min(policy.target(t, hist, b), b.capacity_l)
        inflow = 0.0
        if supply[t] and v < tgt:
            inflow = min(b.inflow_lph, tgt - v)
        age = age + 1.0
        if inflow > 0:
            age = (v * age) / (v + inflow)                # fresh water mixes in (age 0)
            v += inflow
        delivered = min(demand[t], max(0.0, v - b.v_min_l))
        unmet = demand[t] - delivered
        v -= delivered
        rows[t] = (v, tgt, inflow, delivered, unmet, age)
    df = pd.DataFrame(rows, columns=["level_l", "target_l", "inflow_l", "delivered_l", "unmet_l", "age_h"])
    df["supply_on"] = supply
    df["demand_l"] = demand
    return df


def kpis(df: pd.DataFrame, b: TankBuilding, warmup_h: int = 14 * 24) -> dict:
    d = df.iloc[warmup_h:]
    w = d.delivered_l
    return {
        "mean_age_h": float((d.age_h * w).sum() / w.sum()),
        "share_over_limit": float(w[d.age_h > b.age_limit_h].sum() / w.sum()),
        "dry_hours": int((d.unmet_l > 1).sum()),
        "unmet_l": float(d.unmet_l.sum()),
        "mean_level_l": float(d.level_l.mean()),
    }
