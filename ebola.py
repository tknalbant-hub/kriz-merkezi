import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("🧠 Otonom Öğrenen Beyin (Self-Learning)")

# Ağın kendi kendine gelişmesi için session_state'i başlat
if 'G' not in st.session_state:
    G = nx.erdos_renyi_graph(100, 0.05)
    for n in G.nodes(): G.nodes[n]['v'] = 0.0
    for u, v in G.edges(): G[u][v]['w'] = 0.5
    st.session_state.G = G

G = st.session_state.G

def otonom_beyin(G):
    # 1. KENDİ KENDİNE TETİKLEME (Düşünce üretimi)
    if np.random.rand() > 0.3: # %70 ihtimalle kendi kendine bir bölgeyi tetikle
        node = np.random.choice(list(G.nodes()))
        G.nodes[node]['v'] = 100.0
    
    # 2. ÖĞRENME DÖNGÜSÜ
    ateslenenler = []
    for n in G.nodes():
        if G.nodes[n].get('v', 0) > 20:
            ateslenenler.append(n)
            for k in G.neighbors(n):
                # Bilgi akışı ve sinaptik güçlenme (Öğrenme)
                G.nodes[k]['v'] = G.nodes[k].get('v', 0) + (G[n][k].get('w', 1) * 20)
                G[n][k]['w'] = min(2.0, G[n][k].get('w', 1) + 0.1) # Sabit öğrenme
                
    # 3. VOLTAJ SIFIRLAMA (Beynin soğuması)
    for n in G.nodes(): G.nodes[n]['v'] = 0.0
    return ateslenenler

# Arayüz
if st.checkbox("Simülasyonu Otomatik Başlat"):
    while True:
        at = otonom_beyin(G)
        fig, ax = plt.subplots()
        colors = ['red' if n in at else 'blue' for n in G.nodes()]
        nx.draw(G, pos=nx.spring_layout(G), node_color=colors, node_size=30)
        st.pyplot(fig)
        time.sleep(1) # Saniyede bir güncelle
        st.rerun() # Sayfayı otomatik yenile

if st.button("Ağı Sıfırla"):
    del st.session_state.G
    st.rerun()
