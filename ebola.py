import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="5A48K PANDEMIC ENGINE", layout="wide")
st.title("🌐 5A48K PANDEMIC RISK ENGINE v8.0")

# Evrensel Veritabanı
global_db = {
    "ebola": {"cases": 28646, "today": 12, "type": "Viral"},
    "covid-19": {"cases": 704753890, "today": 1200, "type": "Viral"},
    "tuberculosis": {"cases": 10600000, "today": 3000, "type": "Bacterial"},
    "malaria": {"cases": 249000000, "today": 15000, "type": "Parasitic"}
}

virus = st.text_input("Patojen Adı girin:", "covid-19").lower()

def calculate_pandemic_risk(cases, today):
    # Pandemi Risk Skoru Algoritması: 
    # (Günlük Artış / Toplam Vaka) * Logaritmik Çarpan
    risk = (today / (cases + 1)) * 10000 
    return min(100, risk)

if st.button("RİSK ANALİZİNİ BAŞLAT"):
    data = global_db.get(virus, None)
    
    if data:
        risk_score = calculate_pandemic_risk(data['cases'], data['today'])
        
        # 1. Metrikler
        c1, c2, c3 = st.columns(3)
        c1.metric("TOPLAM VAKA", f"{data['cases']:,}")
        c2.metric("RİSK SKORU", f"%{risk_score:.2f}")
        c3.metric("DURUM", "KRİTİK" if risk_score > 5 else "STABİL")
        
        # 2. Gelecek Projeksiyonu (Pandemi Simülasyonu)
        st.subheader("🔮 30 Günlük Projeksiyon")
        growth_rate = (data['today'] / (data['cases'] + 1))
        future_vals = [data['cases'] * ((1 + growth_rate)**i) for i in range(31)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=future_vals, mode='lines+markers', line=dict(color='red', width=3)))
        fig.update_layout(title="Yayılım Tahmini", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        # 3. Pandemi Riski Yorumu
        if risk_score > 5:
            st.error("⚠️ ALARM: Bu patojen yüksek yayılım hızına sahip. Pandemi riski artıyor!")
        else:
            st.success("✅ STABİL: Yayılım kontrol altında veya düşük seyrediyor.")
    else:
        st.error("Patojen veritabanında bulunamadı. Veri eklenmesini talep edin.")
