import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Sayfa Ayarları
st.set_page_config(page_title="Dijital Beyin 2.0", layout="wide")
st.title("🧠 Öğrenen Beyin Simülasyonu (Hebbian Model)")

# Oturum durumunda ağı sakla (Sayfa yenilenince ağ silinmesin)
if 'G' not in st.session_state:
    n = 200
    st.session_state.G = nx.erdos_renyi_graph(n, 0.05)
    # Başlangıçta tüm bağlantı ağırlıklarını 1.0 yap
    for u, v in st.session_state.G.edges():
        st.session_state.G[u][v]['weight'] = 0.1
    for node in st.session_state.G.nodes():
        st.session_state.G.nodes[node]['voltaj'] = -70.0

G = st.session_state.G

# 1. Simülasyon Motoru (İnhibisyon ve Hebbian Öğrenme ile)
def simule_et(G):
    ateslenenler = []
    # Eşik değerini geçenleri bul
    for node in G.nodes():
        if G.nodes[node]['voltaj'] > -50:
            ateslenenler.append(node)
    
    # Sinyal Yayılımı ve Öğrenme
    for node in ateslenenler:
        for komsu in G.neighbors(node):
            # 1. Yayılım (Ağırlığa göre sinyal geçişi)
            G.nodes[komsu]['voltaj'] += G[node][komsu]['weight'] * 20
            
            # 2. Hebbian Öğrenme: Birlikte ateşlenenlerin bağı güçlenir
            if G.nodes[komsu]['voltaj'] > -50:
                G[node][komsu]['weight'] += 0.05 # Yolu güçlendir
                
        # 3. İnhibisyon: Ateşlenen nöronun voltajını sıfırla (Dinlenme süreci)
        G.nodes[node]['voltaj'] = -70.0
        
    return ateslenenler

# Arayüz
if st.button("Sinyal Gönder (Öğrenmeyi Tetikle)"):
    ateslenenler = simule_et(G)
    
    # Görselleştirme
    fig, ax = plt.subplots(figsize=(10, 6))
    pos = nx.spring_layout(G)
    
    # Bağlantı kalınlıklarını ağırlığa göre ayarla
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    
    nx.draw(G, pos, width=weights, node_size=50, node_color='blue', alpha=0.3)
    nx.draw_networkx_nodes(G, pos, nodelist=ateslenenler, node_color='red', node_size=100)
    
    st.pyplot(fig)
    st.metric("Öğrenilen Bağlantı Sayısı", sum(1 for u, v in G.edges() if G[u][v]['weight'] > 0.2))
else:
    st.write("Simülasyon hazır. Butona basarak ağın 'öğrenmesini' başlat.")
