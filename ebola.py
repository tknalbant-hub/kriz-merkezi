import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="5a48k TAHMİN MOTORU", layout="wide")
st.title("🌐 PANDEMİ RİSK ANALİZ VE TAHMİN MOTORU")

@st.cache_data(ttl=3600)
def get_live_data():
    # Güncel veri setini çek
    url = "https://raw.githubusercontent.com/owid/ebola-data/master/data/ebola.csv"
    return pd.read_csv(url)

df = get_live_data()

# Veriden son iki değeri alıp artış hızını hesapla
son_deger = df['Value'].iloc[-1]
onceki_deger = df['Value'].iloc[-2]
artis_hizi = ((son_deger - onceki_deger) / onceki_deger) * 100

# Pandemi İhtimali Hesaplama (Basit Logaritmik Model)
pandemi_ihtimali = min(100, (son_deger / 1000) * (1 + (artis_hizi / 100)))

# Arayüz
col1, col2 = st.columns(2)
col1.metric("GÜNCEL VAKA", int(son_deger))
col2.metric("ARTIŞ HIZI", f"%{artis_hizi:.2f}")

st.divider()
st.subheader(f"📊 HESAPLANAN PANDEMİ OLASILIĞI: %{pandemi_ihtimali:.2f}")

if pandemi_ihtimali > 70:
    st.error("KRİTİK SEVİYE: Yayılım hızı kontrol edilemiyor.")
elif pandemi_ihtimali > 40:
    st.warning("DİKKAT: Bölgesel yayılım riski yüksek.")
else:
    st.success("STABİL: Mevcut verilerde pandemi tehdidi düşük.")
