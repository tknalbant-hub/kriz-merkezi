import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="5A48K DYNAMIC SEARCH", layout="wide")
st.title("🌐 5A48K DYNAMIC CRISIS SEARCH")

# 1. KULLANICI GİRİŞİ
virus_adi = st.text_input("Sorgulanacak Virüs/Patojen Adı (Örn: covid-19, mpox):", value="covid-19").lower()

@st.cache_data(ttl=3600)
def get_chrono_data(pathogen):
    # Dinamik URL oluşturma
    url = f"https://disease.sh/v3/covid-19/historical/{pathogen}?lastdays=30"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            timeline = response.json()['timeline']['cases']
            df = pd.DataFrame(list(timeline.items()), columns=['Tarih', 'Vaka Sayısı'])
            df['Tarih'] = pd.to_datetime(df['Tarih'])
            return df
        return None
    except: return None

if st.button("Sorgula"):
    df = get_chrono_data(virus_adi)
    
    if df is not None:
        st.success(f"'{virus_adi}' başarıyla yüklendi.")
        
        # Projeksiyon (Son 30 günün ortalama büyüme hızı)
        growth = (df['Vaka Sayısı'].iloc[-1] - df['Vaka Sayısı'].iloc[-2]) / (df['Vaka Sayısı'].iloc[-2] + 1)
        
        # Gelecek 30 gün simülasyonu
        last_date = df['Tarih'].iloc[-1]
        future_dates = [last_date + timedelta(days=i) for i in range(1, 31)]
        future_vals = [df['Vaka Sayısı'].iloc[-1] * (1 + growth)**i for i in range(1, 31)]
        
        # Grafik
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Tarih'], y=df['Vaka Sayısı'], name='Geçmiş', line=dict(color='cyan')))
        fig.add_trace(go.Scatter(x=future_dates, y=future_vals, name='Projeksiyon', line=dict(color='red', dash='dot')))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrikler
        col1, col2 = st.columns(2)
        col1.metric("SON VAKA SAYISI", f"{int(df['Vaka Sayısı'].iloc[-1]):,}")
        col2.metric("GÜNLÜK BÜYÜME", f"%{growth*100:.3f}")
    else:
        st.error(f"'{virus_adi}' verisi bulunamadı veya yazım hatası var. 'covid-19' veya 'mpox' deneyin.")
