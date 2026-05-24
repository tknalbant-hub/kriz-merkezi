import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="5A48K CHRONO-PREDICTIVE", layout="wide")
st.title("🌐 5A48K CHRONO-CRISIS OBSERVATORY")

# 1. ZAMANLI VERİ ÇEKME (Geçmiş 30 gün + Gelecek 30 gün)
@st.cache_data(ttl=3600)
def get_chrono_data(pathogen):
    # disease.sh'den son 30 günün geçmiş verisini çek
    url = f"https://disease.sh/v3/covid-19/historical/{pathogen}?lastdays=30"
    try:
        response = requests.get(url, timeout=10).json()
        timeline = response['timeline']['cases']
        df = pd.DataFrame(list(timeline.items()), columns=['Tarih', 'Vaka Sayısı'])
        df['Tarih'] = pd.to_datetime(df['Tarih'])
        return df
    except: return None

# Patojen Seçimi
patojen = st.sidebar.selectbox("Patojen Seçimi", ["covid-19", "mpox"])
df = get_chrono_data(patojen)

if df is not None:
    # 2. PROJEKSİYON HESAPLAMA
    last_val = df['Vaka Sayısı'].iloc[-1]
    growth = (df['Vaka Sayısı'].iloc[-1] - df['Vaka Sayısı'].iloc[-2]) / df['Vaka Sayısı'].iloc[-2]
    
    # Gelecek 30 günü simüle et
    future_dates = [df['Tarih'].iloc[-1] + timedelta(days=i) for i in range(1, 31)]
    future_vals = [last_val * (1 + growth)**i for i in range(1, 31)]
    
    future_df = pd.DataFrame({'Tarih': future_dates, 'Vaka Sayısı': future_vals})
    
    # 3. GRAFİKLEŞTİRME
    fig = go.Figure()
    # Geçmiş
    fig.add_trace(go.Scatter(x=df['Tarih'], y=df['Vaka Sayısı'], name='Geçmiş (Gerçek)', line=dict(color='blue')))
    # Gelecek
    fig.add_trace(go.Scatter(x=future_df['Tarih'], y=future_df['Vaka Sayısı'], name='Gelecek (Simülasyon)', line=dict(color='red', dash='dash')))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # İstatistikler
    col1, col2 = st.columns(2)
    col1.metric("SON VAKA GİRİŞİ", f"{last_val:,}")
    col2.metric("GÜNLÜK BÜYÜME HIZI", f"%{growth*100:.2f}")
    
    st.info("Mavi: Resmi sağlık kayıtları (Geçmiş). Kırmızı: Mevcut ivmeye göre tahmin edilen gelecek (Simülasyon).")
else:
    st.error("Veri akışında zaman aşımı.")
