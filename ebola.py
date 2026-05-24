import streamlit as st
import pandas as pd
import numpy as np
import requests
from scipy.integrate import odeint

st.set_page_config(page_title="5A48K OBSERVATORY v2.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1a1c24; padding: 20px; border-radius: 15px; border: 1px solid #2d2f3b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 5A48K GLOBAL CRISIS OBSERVATORY v2.0")

@st.cache_data(ttl=3600)
def load_data():
    url = "https://raw.githubusercontent.com/datasets/ebola/master/data/ebola_data_db_format.csv"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame({'Value': [100, 200, 300, 400, 500, 620]})

df = load_data()
current_val = float(df['Value'].iloc[-1])
prev_val = float(df['Value'].iloc[-2])

# SIR Modeli Hesaplama
N = 1000000
beta, gamma = 0.3, 0.1
t = np.linspace(0, 30, 30)
res = odeint(lambda y, t: [-beta*y[0]*y[1]/N, beta*y[0]*y[1]/N - gamma*y[1], gamma*y[1]], 
             [N-current_val, current_val, 0], t)

# Dashboard
m1, m2, m3 = st.columns(3)
m1.metric("GÜNCEL VAKA", f"{int(current_val):,}")
growth = ((current_val - prev_val) / (prev_val + 0.1)) * 100
m2.metric("ARTIŞ HIZI", f"%{growth:.2f}")
prob = min(100, (current_val / 50000) * (1 + growth/100))
m3.metric("PANDEMİ OLASILIĞI", f"%{prob:.2f}")

st.subheader("🚀 30 Günlük Tahmin (SIR Model)")
st.area_chart(pd.DataFrame({'Enfekte': res[:, 1]}))

if prob > 70:
    st.error("KRİTİK: DARK WINTER PROTOKOLÜ AKTİF")
elif prob > 30:
    st.warning("UYARI: YÜKSEK YAYILIM RİSKİ")
else:
    st.success("SİSTEM STABİL")
