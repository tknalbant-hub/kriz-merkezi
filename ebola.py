import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="5A48K GLOBAL OBSERVATORY", layout="wide")
st.title("🌐 5A48K UNIVERSAL CRISIS ENGINE")

# 1. YEREL VERİ YEDEĞİ (Eğer API'de yoksa buraya döner)
local_data = {
    "ebola": {"cases": 28646, "todayCases": 12},
    "covid-19": {"cases": 704753890, "todayCases": 120},
    "mpox": {"cases": 95000, "todayCases": 5}
}

virus_adi = st.text_input("Patojen Adı girin (örn: covid-19, ebola, mpox):", value="covid-19").lower()

def get_data(v):
    # Önce API'yi dene
    url = f"https://disease.sh/v3/covid-19/{v if v != 'covid-19' else 'all'}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return data['cases'], data.get('todayCases', 0)
    except: pass
    
    # API başarısız olursa yerel veriyi dön
    if v in local_data:
        return local_data[v]['cases'], local_data[v]['todayCases']
    return None, None

if st.button("Sorgula"):
    cases, today = get_data(virus_adi)
    
    if cases:
        st.success(f"{virus_adi.upper()} verisi yüklendi.")
        growth = (today / (cases + 1)) * 100
        
        # Gelecek projeksiyonu (30 gün)
        future_vals = [cases * (1 + growth/100)**i for i in range(31)]
        
        # Grafik
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=future_vals, mode='lines', name='Projeksiyon', line=dict(color='red')))
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrikler
        c1, c2, c3 = st.columns(3)
        c1.metric("TOPLAM VAKA", f"{cases:,}")
        c2.metric("GÜNLÜK ARTIŞ", f"{today:,}")
        c3.metric("RİSK YÜZDESİ", f"%{growth:.4f}")
    else:
        st.error("Bu patojen veritabanımızda kayıtlı değil.")
