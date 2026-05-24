import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="5A48K DASHBOARD v5.0", layout="wide")
st.title("🌐 5A48K GLOBAL CRISIS OBSERVATORY v5.0")

# API Kaynakları
sources = {
    "COVID-19": "https://disease.sh/v3/covid-19/all",
    "Mpox": "https://disease.sh/v3/covid-19/mpox/all",
    "Influenza (Grip)": "https://disease.sh/v3/covid-19/influenza/all"
}

def get_data(url):
    try:
        data = requests.get(url, timeout=10).json()
        return data
    except:
        return None

# Panel Verileri
data_list = []
for name, url in sources.items():
    res = get_data(url)
    if res:
        # Haftalık tahmini artış (Basitleştirilmiş hesaplama)
        cases = res.get('cases', 0)
        today = res.get('todayCases', 0)
        growth = (today / (cases - today + 1)) * 100
        data_list.append({
            "Patojen": name,
            "Toplam Vaka": cases,
            "Bugünkü Vaka": today,
            "Artış Hızı (%)": round(growth, 4)
        })

# Tablo Görünümü
df = pd.DataFrame(data_list)
st.subheader("📊 Haftalık Küresel Patojen Tablosu")
st.table(df)

st.divider()
st.info("Sistem, her patojenin küresel vaka ivmesini otomatik olarak analiz eder.")
