import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="5A48K GLOBAL OBSERVATORY", layout="wide")

st.title("🌐 5A48K GLOBAL CRISIS OBSERVATORY")
st.subheader("CANLI VERİ AKIŞI: COVID-19 (FAST API)")

@st.cache_data(ttl=3600)
def get_fast_data():
    # Devasa CSV yerine, sadece güncel veriyi sağlayan API kullanıyoruz
    url = "https://disease.sh/v3/covid-19/all"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    return None

try:
    data = get_fast_data()
    if data:
        col1, col2 = st.columns(2)
        col1.metric("TOPLAM VAKA (DÜNYA)", f"{data['cases']:,}")
        col2.metric("BUGÜNKÜ VAKA", f"{data['todayCases']:,}")
        st.success("SİSTEM GÜNCEL: Veri akışı aktif.")
    else:
        st.error("Veri kaynağına ulaşılamadı. Sunucu meşgul olabilir.")
except Exception as e:
    st.error("Bağlantı hatası.")
