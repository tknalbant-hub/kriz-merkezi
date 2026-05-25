import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime

st.set_page_config(page_title="5A48K ULTIMATE ENGINE", layout="wide")
st.title("🌐 5A48K GLOBAL BIO-INTEL MULTIVERSE ENGINE v15.0")

# 1. VERİ KAYNAKLARI VE SÖZLÜK
db = {
    "covid-19": {"total": 704753890, "last": 35000},
    "ebola": {"total": 28646, "last": 50},
    "mpox": {"total": 95000, "last": 5}
}

# 2. GİRDİLER
c1, c2 = st.columns([2, 1])
virus = c1.text_input("Patojen Adı (Örn: covid-19, ebola):", "ebola").lower()
tarih_sec = c2.date_input("Analiz Tarihi:", datetime(2026, 5, 31))

if st.button("KUANTUM ANALİZİ BAŞLAT"):
    data = db.get(virus)
    if data:
        # A. CANLI VE TARİHSEL HESAPLAMA
        bugun = datetime.now().date()
        gun_farki = (tarih_sec - bugun).days
        real_k = (data['last'] / 30) / data['total']
        
        # B. 1 MİLYON EVREN (MONTE CARLO)
        n = 1000000
        k_values = np.random.uniform(real_k * 0.5, real_k * 2.0, n)
        best_k = k_values[np.argmin(np.abs(k_values - real_k))]
        
        # C. METRİKLER VE RİSK
        risk = min(100, (data['last'] / data['total']) * 5000)
        tahmin = data['total'] * ((1 + best_k) ** gun_farki)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("TOPLAM YÜK", f"{int(data['total']):,}")
        col2.metric("EVRENSEL TAHMİN", f"{int(tahmin):,}")
        col3.metric("PANDEMİ RİSKİ", f"%{risk:.2f}")
        
        # D. GÖRSELLEŞTİRME (BULUT SİMÜLASYONU)
        fig = go.Figure()
        
        # Rastgele 500 evren örneği (Görsel performans için)
        for i in range(500):
            forecast = [data['total'] * ((1 + k_values[i])**d) for d in range(31)]
            fig.add_trace(go.Scatter(y=forecast, mode='lines', line=dict(color='rgba(0, 242, 255, 0.03)'), showlegend=False))
            
        # Ana Evren (Dünya)
        main_forecast = [data['total'] * ((1 + best_k)**d) for d in range(31)]
        fig.add_trace(go.Scatter(y=main_forecast, mode='lines', name='Dünya (Best Fit)', line=dict(color='#ff4b4b', width=4)))
        
        fig.update_layout(title="1 Milyon Evren Olasılık Bulutu", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"Kuantum Gözlemcisi: Mevcut dünyamız, {best_k:.6f} yayılım katsayılı evren ile uyumlu seyrediyor.")
        
    else:
        st.error("Patojen veritabanında tanımlı değil.")
