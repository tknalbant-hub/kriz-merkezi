import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="5a48k TAHMİN MOTORU", layout="wide")
st.title("🌐 PANDEMİ RİSK ANALİZ VE TAHMİN MOTORU")

# 1. YEDEK HAFIZA: İnternet kesilirse diye buraya son bildiğimiz verileri koyduk
YEDEK_VERI = pd.DataFrame({'Value': [150, 200, 300, 450, 620]})

def get_live_data():
    url = "https://raw.githubusercontent.com/datasets/ebola/master/data/ebola_data_db_format.csv"
    try:
        # 5 saniye zaman aşımı ekledik, bekleyip durmasın
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return pd.read_csv(url)
        return YEDEK_VERI
    except:
        return YEDEK_VERI

df = get_live_data()

# Analiz Motoru
son_deger = float(df['Value'].iloc[-1])
onceki_deger = float(df['Value'].iloc[-2])
artis_hizi = ((son_deger - onceki_deger) / (onceki_deger + 0.1)) * 100
pandemi_ihtimali = min(100, (son_deger / 500) * (1 + (artis_hizi / 100)))

# Dashboard
col1, col2 = st.columns(2)
col1.metric("GÜNCEL VAKA", int(son_deger))
col2.metric("ARTIŞ HIZI", f"%{artis_hizi:.2f}")

st.divider()
st.subheader(f"📊 HESAPLANAN PANDEMİ OLASILIĞI: %{pandemi_ihtimali:.2f}")

if pandemi_ihtimali > 70:
    st.error("KRİTİK SEVİYE: Yayılım hızı kontrol edilemiyor. İzolasyon şart.")
else:
    st.info("Sistem stabil. Gözlem devam ediyor.")

st.line_chart(df['Value'])
