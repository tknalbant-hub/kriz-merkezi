import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="5A48K ULTIMATE ENGINE", layout="wide")
st.title("🌐 5A48K GLOBAL BIO-INTEL ENGINE v12.0")

# Evrensel Patojen Veritabanı
db = {
    "covid-19": {"total": 704753890, "last_month": 35000},
    "ebola": {"total": 28646, "last_month": 50},
    "mpox": {"total": 95000, "last_month": 5},
    "tuberculosis": {"total": 10600000, "last_month": 90000}
}

# Arayüz
col1, col2 = st.columns([2, 1])
virus = col1.text_input("Patojen Adı (Örn: covid-19, ebola):", "covid-19").lower()
tarih_sec = col2.date_input("Analiz Tarihi (Geçmiş/Gelecek):", datetime(2026, 5, 31))

if st.button("ANALİZİ BAŞLAT"):
    data = db.get(virus)
    if data:
        # Hesaplama Modeli
        bugun = datetime.now().date()
        gun_farki = (tarih_sec - bugun).days
        growth_rate = (data['last_month'] / 30) / data['total']
        tahmin = data['total'] * ((1 + growth_rate) ** gun_farki)
        risk = min(100, (data['last_month'] / data['total']) * 5000)
        
        # Dashboard
        c1, c2, c3 = st.columns(3)
        c1.metric("TOPLAM YÜK", f"{int(data['total']):,}")
        c2.metric("PROJEKSİYON", f"{int(tahmin):,}")
        c3.metric("PANDEMİ RİSKİ", f"%{risk:.2f}")
        
        # Grafik
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[bugun, tarih_sec], y=[data['total'], tahmin], 
                                 mode='lines+markers', line=dict(color='#00f2ff', width=4)))
        fig.update_layout(title=f"{virus.upper()} Yayılım Simülasyonu", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        # Yorum
        st.info(f"Sistem, {tarih_sec} tarihinde vaka sayısının {int(tahmin):,} seviyesine ulaşacağını öngörüyor.")
    else:
        st.error("Patojen bulunamadı. Lütfen veritabanını kontrol edin.")
