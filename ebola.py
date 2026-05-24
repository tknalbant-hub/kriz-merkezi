import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="5A48K GLOBAL DASHBOARD", layout="wide")
st.title("🌐 5A48K GLOBAL CRISIS OBSERVATORY v5.1")

# API Kaynakları
sources = {
    "COVID-19": "https://disease.sh/v3/covid-19/all",
    "Mpox": "https://disease.sh/v3/covid-19/mpox/all",
    "Influenza": "https://disease.sh/v3/covid-19/influenza/all"
}

@st.cache_data(ttl=3600)
def fetch_all_data():
    results = []
    for name, url in sources.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "Patojen": name,
                    "Toplam Vaka": data.get('cases', 0),
                    "Artış Hızı (%)": round((data.get('todayCases', 0) / (data.get('cases', 1))) * 100, 4)
                })
        except:
            continue
    return pd.DataFrame(results)

# Veriyi çek ve tabloyu oluştur
df = fetch_all_data()

if not df.empty:
    st.subheader("📋 Küresel Patojen İzleme Tablosu")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.subheader("📈 Karşılaştırmalı Vaka Analizi")
    fig = px.bar(df, x="Patojen", y="Toplam Vaka", color="Patojen", text_auto='.2s')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Veriler yükleniyor veya API bağlantısı meşgul, lütfen sayfayı yenile.")
