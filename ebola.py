import streamlit as st
import pandas as pd

st.set_page_config(page_title="5A48K GLOBAL OBSERVATORY", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #e0e0e0; }
    .stMetric { background-color: #161616; padding: 20px; border-radius: 12px; border: 1px solid #333; }
    h1 { color: #00ffcc; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 5A48K GLOBAL CRISIS OBSERVATORY")
st.subheader("CANLI VERİ AKIŞI: COVID-19 (RESMİ WHO/OWID)")

@st.cache_data(ttl=3600)
def get_live_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    # Sadece gerekli sütunları çekerek sistemi hızlandırıyoruz
    df = pd.read_csv(url, usecols=['location', 'date', 'new_cases', 'total_cases'])
    # Dünya genelindeki son veriyi al
    world_data = df[df['location'] == 'World'].dropna()
    return world_data.tail(1)

try:
    data = get_live_data()
    total = int(data['total_cases'].iloc[0])
    new = int(data['new_cases'].iloc[0])

    col1, col2 = st.columns(2)
    col1.metric("TOPLAM VAKA (DÜNYA)", f"{total:,}")
    col2.metric("GÜNLÜK YENİ VAKA", f"{new:,}")

    st.divider()
    st.success("SİSTEM GÜNCEL: Canlı veri akışı aktif.")
    st.write(f"Son Güncelleme: {data['date'].iloc[0]}")
    
except Exception as e:
    st.error("Veri akışında geçici bir kesinti var. Sistem WHO kaynaklarını bekliyor.")

st.sidebar.info("5A48K Gözlemevi v4.1 - Operasyonel")
