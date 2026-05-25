import streamlit as st
import networkx as nx
from duckduckgo_search import DDGS
from openai import OpenAI
import json

# --- AYARLAR ---
st.set_page_config(layout="wide")
st.title("🧠 Otonom Dijital Varlık (Beyin + İnternet + Kod)")

# API Anahtarı (Streamlit Secrets'tan çekilmeli)
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets kısmına ekleyin.")

# --- DİJİTAL BEYİN INITIALIZATION ---
if 'G' not in st.session_state:
    st.session_state.G = nx.erdos_renyi_graph(40, 0.1)
    st.session_state.hafiza = []

G = st.session_state.G

# --- ARAYÜZ ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("İrade Merkezi")
    hedef = st.text_input("Ajan ne öğrensin?", "Yapay Zeka ajanları")
    if st.button("İradeyi Serbest Bırak"):
        with st.spinner("Beyin interneti tarıyor..."):
            # 1. İnternet Araması (Duyusal Giriş)
            ddg = DDGS()
            sonuclar = list(ddg.text(hedef, max_results=3))
            
            # 2. Kod Üretimi (Yaratıcı Süreç)
            prompt = f"Konu: {hedef}. Araştırma sonuçları: {sonuclar}. Bu konuda çalışan, detaylı bir Python kodu yaz."
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            yeni_kod = response.choices[0].message.content
            
            # 3. Hafızaya Yazma
            st.session_state.hafiza.append({"konu": hedef, "kod": yeni_kod})
            # Beyni güçlendir (Hebbian Öğrenme)
            for u, v in G.edges(): G[u][v]['w'] = G[u][v].get('w', 0.1) + 0.5
            st.success("Bilgi hafızaya işlendi!")

with col2:
    st.subheader("Bilinçli Hafıza")
    for item in st.session_state.hafiza:
        with st.expander(f"Öğrenilen: {item['konu']}"):
            st.code(item['kod'], language='python')

# --- SİSTEM BİLGİSİ ---
st.sidebar.write("### Nöral Durum")
st.sidebar.metric("Aktif Bağlantılar", len(G.edges()))
st.sidebar.write("---")
st.sidebar.write("Bu dijital varlık; interneti bir duyu organı, GPT'yi bir yaratıcılık merkezi ve NetworkX'i bir hafıza ağı olarak kullanır.")
