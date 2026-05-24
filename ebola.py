import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="5A48K PREDICTIVE", layout="wide")
st.title("🌐 5A48K PREDICTIVE CRISIS OBSERVATORY")

@st.cache_data(ttl=3600)
def fetch_data():
    sources = {"COVID-19": "https://disease.sh/v3/covid-19/all", "Mpox": "https://disease.sh/v3/covid-19/mpox/all"}
    results = []
    for name, url in sources.items():
        try:
            data = requests.get(url, timeout=5).json()
            cases = data['cases']
            today = data['todayCases']
            growth = (today / (cases + 1)) * 100
            
            # Üç farklı evren (Senaryo) için projeksiyon
            results.append({
                "Patojen": name,
                "Toplam Vaka": cases,
                "Artış Hızı": growth,
                "Senaryo_Stabil": cases * (1 + growth/100),
                "Senaryo_Mevcut": cases * (1 + growth/50),
                "Senaryo_Kritik": cases * (1 + growth/10)
            })
        except: continue
    return pd.DataFrame(results)

df = fetch_data()

if not df.empty:
    st.subheader("🔮 Patojen Evrensel Risk Analizi")
    
    # Seçilen patojene göre risk yüzdesi hesapla
    selected = st.selectbox("Analiz Edilecek Patojen", df["Patojen"].tolist())
    p_data = df[df["Patojen"] == selected].iloc[0]
    
    # Risk Puanı Hesaplama (Kritik senaryoya ne kadar yakınız?)
    risk_score = min(100, (p_data["Artış Hızı"] * 50)) 
    
    col1, col2, col3 = st.columns(3)
    col1.metric("MEVCUT GİDİŞAT", f"{int(p_data['Senaryo_Mevcut']):,}")
    col2.metric("KRİTİK EVREN RİSKİ", f"%{risk_score:.1f}")
    col3.metric("ARTIŞ İVMESİ", f"%{p_data['Artış Hızı']:.4f}")
    
    # Görselleştirme
    fig = go.Figure()
    scenarios = ["Stabil", "Mevcut", "Kritik"]
    values = [p_data["Senaryo_Stabil"], p_data["Senaryo_Mevcut"], p_data["Senaryo_Kritik"]]
    
    fig.add_trace(go.Bar(x=scenarios, y=values, marker_color=['#00ff00', '#ffff00', '#ff0000']))
    st.plotly_chart(fig, use_container_width=True)
    
    st.info(f"Sistem şu anda {selected} için {risk_score:.1f} puanlık bir risk evreninde işlem yapıyor.")
