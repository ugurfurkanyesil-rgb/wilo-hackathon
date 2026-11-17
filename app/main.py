"""Streamlit demo: load time series -> anomaly / forecast -> chart.

Run from the project root:  streamlit run app/main.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data import LABEL_COL, load_sample, load_timeseries, points_per_day  # noqa: E402
from src.model import (backtest_mae, classification_scores,  # noqa: E402
                       detect_anomalies, detect_anomalies_multi, forecast)

ALL_COLS = "Tüm sütunlar (maks. skor)"

st.set_page_config(page_title="Water AI Demo", layout="wide")
st.title("Water AI Hackathon — Demo")

# ---- 1. Data ----
with st.sidebar:
    st.header("1. Veri")
    source = st.radio("Kaynak", ["Örnek (sentetik)", "Dosya yükle"])
    upload = None
    if source == "Dosya yükle":
        upload = st.file_uploader("CSV veya XLSX", type=["csv", "xlsx", "xls"])

try:
    if upload is not None:
        df = load_timeseries(upload, name=upload.name)
    else:
        df = load_sample()
except ValueError as e:
    st.error(str(e))
    st.stop()

if upload is None and source == "Dosya yükle":
    st.info("Dosya yüklenmedi; örnek veri gösteriliyor.")

value_cols = [c for c in df.columns if c != LABEL_COL]
if not value_cols:
    st.error("Sayısal sütun bulunamadı.")
    st.stop()

ppd = points_per_day(df.index)

with st.sidebar:
    st.header("2. Model")
    mode = st.radio("Görev", ["Anomali tespiti", "Tahmin"])
    options = ([ALL_COLS] if mode == "Anomali tespiti" and len(value_cols) > 1 else []) + value_cols
    col = st.selectbox("Sütun", options)
    season = st.number_input("Sezon uzunluğu (nokta; varsayılan = 1 gün)", 1,
                             max(1, len(df) // 2), min(ppd, max(1, len(df) // 2)))
    if mode == "Anomali tespiti":
        threshold = st.slider("Eşik (robust z)", 1.0, 10.0, 4.0, 0.5)
        smooth = st.slider("Skor yumuşatma (nokta)", 1, 24, 4)
    else:
        horizon = st.slider("Ufuk (nokta)", 1, max(2, 7 * ppd), min(ppd, 7 * ppd))

c1, c2, c3 = st.columns(3)
c1.metric("Satır", f"{len(df):,}")
c2.metric("Başlangıç", str(df.index.min().date()))
c3.metric("Bitiş", str(df.index.max().date()))

# ---- 2. Model + 3. Chart ----
fig = go.Figure()
if mode == "Anomali tespiti":
    if col == ALL_COLS:
        res = detect_anomalies_multi(df[value_cols], season=int(season),
                                     threshold=threshold, smooth=smooth)
        flagged = res[res["is_anomaly"]]
        fig.add_scatter(x=res.index, y=res["score"], name="maks. skor", mode="lines")
        fig.add_hline(y=threshold, line_dash="dot", annotation_text="eşik")
        fig.add_scatter(x=flagged.index, y=flagged["score"], name="anomali", mode="markers",
                        marker=dict(size=7, symbol="x"), text=flagged["driver"],
                        hovertemplate="%{x}<br>skor %{y:.1f}<br>sütun: %{text}")
    else:
        res = detect_anomalies(df[col].dropna(), season=int(season),
                               threshold=threshold, smooth=smooth)
        flagged = res[res["is_anomaly"]]
        fig.add_scatter(x=res.index, y=res["value"], name=col, mode="lines")
        fig.add_scatter(x=res.index, y=res["expected"], name="beklenen", mode="lines",
                        line=dict(dash="dash"))
        fig.add_scatter(x=flagged.index, y=flagged["value"], name="anomali", mode="markers",
                        marker=dict(size=7, symbol="x"))
    st.write(f"İşaretlenen nokta: **{len(flagged)}**")
    if LABEL_COL in df.columns:
        scores = classification_scores(df.loc[res.index, LABEL_COL], res["is_anomaly"])
        m1, m2, m3 = st.columns(3)
        m1.metric("Precision", f"{scores['precision']:.2f}")
        m2.metric("Recall", f"{scores['recall']:.2f}")
        m3.metric("F1", f"{scores['f1']:.2f}")
else:
    series = df[col].dropna()
    if len(series) < 2 * season:
        st.error("Seri, seçilen sezon uzunluğunun en az 2 katı olmalı.")
        st.stop()
    fc = forecast(series, horizon=horizon, season=int(season))
    fig.add_scatter(x=series.index, y=series, name=col, mode="lines")
    fig.add_scatter(x=fc.index, y=fc, name="tahmin", mode="lines", line=dict(dash="dash"))
    if len(series) > horizon + 2 * season:
        bt = backtest_mae(series, horizon=horizon, season=int(season))
        m1, m2 = st.columns(2)
        m1.metric("Backtest MAE (sezonsal)", f"{bt['mae_seasonal']:.3f}")
        m2.metric("Backtest MAE (son değer)", f"{bt['mae_last_value']:.3f}")

fig.update_layout(height=480, margin=dict(l=10, r=10, t=30, b=10), hovermode="x unified")
st.plotly_chart(fig, width="stretch")

with st.expander("Ham veri"):
    st.dataframe(df.tail(200))
