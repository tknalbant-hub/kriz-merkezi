import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="5a48k GÖZLEMEVİ", layout="wide")
st.title("🌐 5a48k GLOBAL EPİDEMİYOLOJİK TAKİP")

# HDX yerine doğrudan veri kaynağına bağlanıyoruz (Hata payı sıfır)
def get_data():
    # Örnek bir veri seti (Ebola vaka verisi)
    url = "https://raw.githubusercontent.com/owid/ebola-data/master/data/ebola.csv"
    try:
        df = pd.read_csv(url)
        return df
    except:
        return None

df = get_data()

if df is not None:
    current_cases = int(df['Value'].iloc[-1])
    st.success(f"Güncel Vaka: {current_cases}")
else:
    current_cases = 620
    st.warning("Canlı veriye ulaşılamıyor, baz mod aktif.")

risk_skoru = (current_cases / 1000) * 100
st.metric("CANLI RİSK İNDEKSİ", f"{risk_skoru:.2f}/100")
