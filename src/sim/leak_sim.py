"""Night-window simulator: building booster (SC two-point control) + membrane tank + leak.

Implements the MVP of docs/v1-simulation-design.md, simplified:
- Only the night window is simulated (default 00:00-05:00), because the leak
  estimator only uses night data. Day-time demand is not needed.
- Time step 1 s (design says 0.1 s); output is polled every 1 s like Modbus.
- Two control modes, from the Wilo-Control SC2.0-Booster manual (s.10-14) [K, behaviour]:
  SC  = fixed speed, two-point control (start below p_on, stop above p_off);
  SCe = frequency converter holding p_off as setpoint; a cyclic zero-flow test stops the
        pump when outflow < q_zf; it restarts below p_on. The zero-flow threshold and test
        interval are factory settings we do not know [V].

Every numeric default below is an assumption [V] unless noted; see the design doc.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

P_ATM = 1.013  # bar


@dataclass
class Building:
    V0: float = 24.0            # tank volume, L [V]
    p_on: float = 3.0           # bar(g), pump starts below this [V]
    p_off: float = 4.0          # bar(g), pump stops above this [V]
    p0: float | None = None     # pre-charge bar(g); default p_on - 0.2 [V]
    q_pump_lps: float = 2000 / 3600  # Q_nom 2 m3/h [V]
    noise_bar: float = 0.02     # pressure sensor noise sigma [V]
    quant_bar: float = 0.1      # Modbus register 40026 resolution [K]
    mode: str = "SC"            # SC | SCe
    q_zf_lph: float = 30.0      # SCe zero-flow threshold [V]
    t_zf_s: int = 60            # SCe zero-flow test interval [V]

    def __post_init__(self):
        if self.p0 is None:
            self.p0 = self.p_on - 0.2

    def water_volume(self, p_g: float) -> float:
        """Water in the membrane tank at gauge pressure p_g (isothermal Boyle)."""
        pa, p0a = p_g + P_ATM, self.p0 + P_ATM
        return max(0.0, self.V0 * (1 - p0a / pa))

    def pressure(self, vw: float) -> float:
        p0a = self.p0 + P_ATM
        vw = min(vw, 0.95 * self.V0)
        if vw <= 0:
            return self.p0  # tank empty: pressure falls to pre-charge (pipe pressure ignored)
        return p0a * self.V0 / (self.V0 - vw) - P_ATM

    @property
    def delta_v(self) -> float:
        """Water drawn from the tank between p_off and p_on (design doc §2.1)."""
        return self.water_volume(self.p_off) - self.water_volume(self.p_on)


@dataclass
class NightUse:
    rate_per_h: float = 1.5               # building-wide events/hour at night [V]
    p_flush: float = 0.6                  # share of events that are WC cistern refills [V]
    flush_l: tuple = (5.0, 7.0)           # refill volume, L [V]
    flush_lps: float = 0.10               # refill flow [V]
    tap_s: tuple = (5.0, 30.0)            # tap duration, s [V]
    tap_lps: float = 0.08                 # [V]


@dataclass
class Leak:
    kind: str = "none"        # none | pipe | reservoir
    lph: float = 0.0          # mean leak flow at nominal pressure, L/h
    p_nom: float = 3.5        # bar(g) where pipe leak equals lph
    n1: float = 0.5           # orifice exponent (FAVAD N1) [K: Autodesk InfoWorks]
    v_trig: float = 0.5       # reservoir: refill starts after this much is lost, L [V]
    fill_lps: float = 0.05    # reservoir refill flow, L/s [V]


def simulate_night(b: Building, use: NightUse, leak: Leak, rng: np.random.Generator,
                   start: pd.Timestamp, hours: float = 5.0) -> pd.DataFrame:
    """Simulate one night at 1 s resolution. Returns Modbus-like 1 Hz rows."""
    n = int(hours * 3600)
    # demand schedule: per-second draw (L/s)
    demand = np.zeros(n)
    t = rng.exponential(3600 / use.rate_per_h) if use.rate_per_h > 0 else n
    while t < n:
        i = int(t)
        if rng.random() < use.p_flush:
            dur = int(rng.uniform(*use.flush_l) / use.flush_lps)
            q = use.flush_lps
        else:
            dur = int(rng.uniform(*use.tap_s))
            q = use.tap_lps
        demand[i:i + dur] += q
        t += rng.exponential(3600 / use.rate_per_h)

    vw = b.water_volume(b.p_off)  # night starts right after a pump stop
    running = False
    res_level = 0.0               # reservoir: volume lost since last refill
    res_filling = False
    starts = 0
    tz = 0
    v_set = b.water_volume(b.p_off)

    pres = np.empty(n); run = np.empty(n, dtype=np.int8); st = np.empty(n, dtype=np.int64)
    gt_leak = np.empty(n); flow_calc = np.empty(n)
    k_pipe = leak.lph / 3600 / max(leak.p_nom, 1e-6) ** leak.n1 if leak.kind == "pipe" else 0.0
    q_res = leak.lph / 3600 if leak.kind == "reservoir" else 0.0

    for i in range(n):
        p = b.pressure(vw)
        # leak draw from the building network this second
        if leak.kind == "pipe":
            ql = k_pipe * max(p, 0.0) ** leak.n1
        elif leak.kind == "reservoir":
            res_level += q_res            # cistern leaks into bowl continuously
            if not res_filling and res_level >= leak.v_trig:
                res_filling = True
            if res_filling:
                ql = min(leak.fill_lps, res_level)
                res_level -= ql
                if res_level <= 1e-9:
                    res_filling = False
            else:
                ql = 0.0
        else:
            ql = 0.0
        if b.mode == "SCe":
            out = demand[i] + ql
            if not running and p < b.p_on:
                running = True; starts += 1; tz = 0
            qp = 0.0
            if running:
                if vw < v_set - 1e-9:
                    qp = min(b.q_pump_lps, v_set - vw + out)   # refill to setpoint
                else:
                    qp = out                                     # hold the setpoint
                tz += 1
                if tz >= b.t_zf_s and vw >= v_set - 1e-6:
                    tz = 0
                    if out * 3600 < b.q_zf_lph:                 # zero-flow test passed
                        running = False
        else:
            # SC two-point control
            if not running and p < b.p_on:
                running = True; starts += 1
            elif running and p >= b.p_off:
                running = False
            qp = b.q_pump_lps if running else 0.0
        vw = max(0.0, vw + qp - demand[i] - ql)

        pres[i] = p; run[i] = running; st[i] = starts; gt_leak[i] = ql * 3600
        flow_calc[i] = round(qp * 3.6, 1)   # m3/h, 0.1 resolution, 0 when stopped [K res, V stop]

    noisy = pres + rng.normal(0, b.noise_bar, n)
    q = np.round(noisy / b.quant_bar) * b.quant_bar
    idx = pd.date_range(start, periods=n, freq="1s", name="timestamp")
    return pd.DataFrame({
        "pressure_bar": np.round(q, 1),
        "pump1_running": run,
        "pump1_starts_total": st,
        "flow_calc_m3h": flow_calc,
        "gt_leak_lph": gt_leak,
        "gt_leak_type": leak.kind,
        "gt_demand_lph": demand * 3600,
    }, index=idx)


def simulate_nights(b: Building, use: NightUse, leak: Leak, nights: int, seed: int,
                    hours: float = 5.0) -> list[pd.DataFrame]:
    rng = np.random.default_rng(seed)
    base = pd.Timestamp("2026-01-01 00:00")
    return [simulate_night(b, use, leak, rng, base + pd.Timedelta(days=d), hours)
            for d in range(nights)]
