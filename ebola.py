import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="5a48k TAHMİN MOTORU", layout="wide")
st.title("🌐 PANDEMİ RİSK ANALİZ VE TAHMİN MOTORU")

@st.cache_data(ttl=3600)
def get_live_data():
    # Güncel ve çalışan güvenilir bir kaynak
    url = "https://raw.githubusercontent.com/datasets/ebola/master/data/ebola_data_db_format.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception:
        # Bağlantı kopsa bile sistemin çökmesini engelliyoruz
        return None

df = get_live_data()

if df is not None:
    # Veri setindeki 'Value' (Vaka) sütununu kullanıyoruz
    son_deger = float(df['Value'].iloc[-1])
    onceki_deger = float(df['Value'].iloc[-2])
    artis_hizi = ((son_deger - onceki_deger) / (onceki_deger + 0.1)) * 100
    
    pandemi_ihtimali = min(100, (son_deger / 500) * (1 + (artis_hizi / 100)))

    col1, col2 = st.columns(2)
    col1.metric("GÜNCEL VAKA", int(son_deger))
    col2.metric("ARTIŞ HIZI", f"%{artis_hizi:.2f}")

    st.divider()
    st.subheader(f"📊 HESAPLANAN PANDEMİ OLASILIĞI: %{pandemi_ihtimali:.2f}")
else:
    st.error("Veri kaynağına ulaşılamadı. Sistem 'Bekleme Modu'nda.")
