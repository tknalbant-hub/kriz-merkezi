import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="5A48K FINAL", layout="wide")
st.title("🌐 5A48K ARCHITECT: FINAL SINGULARITY ENGINE")

# 1. MUTASYON FAKTÖRLÜ KAOS MOTORU
def architect_engine(t, mutation_state):
    # Mutasyon varsa dalga boyu uzar, yoksa sönümlenir
    decay = 1.0 if not mutation_state else 0.2
    return np.sin(t) * np.exp(-abs(t) * decay)

st.subheader("🏛️ MİMARIN SON ANALİZİ: EBOLA ÖLÇEĞİ")
mutasyon_var_mi = st.toggle("MUTASYON RİSKİNİ TETİKLE (Biyolojik Kırılma)")

if st.button("GERÇEKLİĞİ İNŞA ET"):
    t = np.linspace(-20, 20, 2000)
    
    # 1. Doğal Durum (Kırmızı)
    doğal = architect_engine(t, False)
    # 2. Mutasyon Durumu (Mor/Kritik)
    mutasyonlu = architect_engine(t, mutasyon_var_mi)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=doğal, name='Doğal Ebola (Sönümlenen)', line=dict(color='cyan', width=2)))
    if mutasyon_var_mi:
        fig.add_trace(go.Scatter(x=t, y=mutasyonlu, name='MUTASYONLU PANDEMİK DALGA', line=dict(color='red', width=4)))
    
    fig.update_layout(template="plotly_dark", title="SİSTEM: Olasılık Dokusundaki Kırılma Analizi")
    st.plotly_chart(fig, use_container_width=True)

    if mutasyon_var_mi:
        st.error("⚠️ SİSTEM UYARISI: Dalga formu sönümlenmiyor. Pandemik Yayılım Enerjisi Tespit Edildi.")
    else:
        st.success("✅ SİSTEM DURUMU: Stabil. Ebola dalgası zaman/mekan içinde sönümleniyor.")
