import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="5A48K ULTIMATE OBSERVATORY", layout="wide")

# --- STİL ---
st.markdown("""<style>.stMetric {background-color: #1a1c24; padding: 15px; border-radius: 10px;}</style>""", unsafe_allow_html=True)

st.title("🌐 5A48K ULTIMATE CRISIS OBSERVATORY v6.0")

# --- GİRDİLER ---
col_a, col_b, col_c = st.columns([2, 1, 1])
virus = col_a.text_input("Patojen Adı (Örn: covid-19, mpox):", "covid-19").lower()
yil = col_b.number_input("Yıl:", 2020, 2026, 2026)
ay = col_c.number_input("Ay:", 1, 12, 5)

def get_data(v, y, a):
    curr_y, curr_m = datetime.now().year, datetime.now().month
    
    # CANLI MOD (Güncel)
    if y == curr_y and a == curr_m:
        url = f"https://disease.sh/v3/covid-19/{v if v != 'covid-19' else 'all'}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200: return "live", res.json()
    
    # ARŞİV MODU
    url = f"https://disease.sh/v3/covid-19/historical/{v}?lastdays=all"
    res = requests.get(url, timeout=5)
    if res.status_code == 200: return "archive", res.json()
    return None, None

if st.button("SİSTEMİ ÇALIŞTIR"):
    mode, data = get_data(virus, yil, ay)
    
    if mode == "live":
        st.info("⚡ CANLI VERİ AKIŞI AKTİF")
        cases = data.get('cases', 0)
        today = data.get('todayCases', 0)
        growth = (today / (cases + 1)) * 100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("TOPLAM VAKA", f"{cases:,}")
        c2.metric("BUGÜNKÜ ARTIŞ", f"{today:,}")
        c3.metric("ARTIŞ HIZI (%)", f"%{growth:.4f}")
        
        # Gelecek Projeksiyonu
        fig = go.Figure(go.Indicator(mode="gauge+number", value=growth, title={'text': "Risk İvmesi"}))
        st.plotly_chart(fig)

    elif mode == "archive":
        st.warning(f"📦 ARŞİV VERİSİ: {yil}/{ay}")
        timeline = data['timeline']['cases']
        df = pd.DataFrame(list(timeline.items()), columns=['Tarih', 'Vaka'])
        df['Tarih'] = pd.to_datetime(df['Tarih'])
        filtered = df[(df['Tarih'].dt.year == yil) & (df['Tarih'].dt.month == ay)]
        
        st.dataframe(filtered, use_container_width=True)
        fig = px.line(filtered, x='Tarih', y='Vaka', title="Tarihsel Gelişim")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Veri bulunamadı. Lütfen patojen adını ve tarihleri kontrol edin.")
