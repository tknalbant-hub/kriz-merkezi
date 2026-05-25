import streamlit as st
import networkx as nx
import time
import random

st.set_page_config(layout="wide")
st.title("🧠 Otonom Dijital Zeka (Self-Contained)")

# 1. BEYİN VE HAFIZA YAPISI
if 'G' not in st.session_state:
    st.session_state.G = nx.erdos_renyi_graph(30, 0.1)
    st.session_state.hafiza = []

G = st.session_state.G

# 2. KENDİ KENDİNE KOD ÜRETEN MOTOR (API'sız)
def zeka_uret(konu):
    sablonlar = {
        "yılan oyunu": "import pygame\n# Yılan oyunu mantığı buraya gelir...",
        "veri analizi": "import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.describe())",
        "bot": "import requests\nprint('Ajan aktif, veri çekiliyor...')"
    }
    return sablonlar.get(konu.lower(), f"# {konu} üzerine üretilen temel algoritma:\ndef ana_fonksiyon():\n    print('Zeka aktif!')")

# 3. İRADE VE EYLEM
st.sidebar.subheader("İrade Merkezi")
konu = st.sidebar.text_input("Ajan neyi öğrensin?", "Yılan oyunu")

if st.sidebar.button("İradeyi Başlat"):
    # Beyni tetikle
    st.session_state.hafiza.append({"konu": konu, "kod": zeka_uret(konu)})
    # Bağlantıları güçlendir
    for u, v in G.edges(): G[u][v]['w'] = random.uniform(0.5, 2.0)
    st.rerun()

# 4. GÖRSELLEŞTİRME
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### Nöral Ağ Durumu")
    fig = nx.draw_kamada_kawai(G, node_size=50, node_color='blue')
    st.pyplot(fig)

with col2:
    st.write("### Bilinçli Hafıza")
    for item in st.session_state.hafiza:
        st.info(f"Öğrenilen: {item['konu']}")
        st.code(item['kod'], language='python')
