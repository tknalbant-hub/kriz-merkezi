import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Sayfa Yapılandırması
st.set_page_config(page_title="Dijital Beyin 2.0", layout="wide")
st.title("🧠 İnsan Beyni Simülasyon Motoru (Öğrenen Ağ)")

# 1. Oturum Yönetimi: Ağın hafızasını koru
if 'G' not in st.session_state:
    n = 150 # Nöron sayısı
    st.session_state.G = nx.erdos_renyi_graph(n, 0.06)
    # Başlangıç ağırlıkları ve voltajları
    for u, v in st.session_state.G.edges():
        st.session_state.G[u][v]['weight'] = 0.1
    for node in st.session_state.G.nodes():
        st.session_state.G.nodes[node]['voltaj'] = -70.0

G = st.session_state.G

# 2. Simülasyon Motoru
def simule_et(G):
    ateslenenler = []
    
    # A) TETİKLEME: Rastgele 10 nöronu "düşünce" olarak uyar
    tetikleyiciler = np.random.choice(list(G.nodes()), size=10)
    for node in tetikleyiciler:
        G.nodes[node]['voltaj'] = -40.0 
    
    # B) ATEŞLEME VE YAYILIM
    for node in G.nodes():
        if G.nodes[node]['voltaj'] > -50: # Eşik değeri
            ateslenenler.append(node)
            # Komşulara sinyal gönder
            for komsu in G.neighbors(node):
                # Sinyal iletimi
                G.nodes[komsu]['voltaj'] += G[node][komsu]['weight'] * 25.0
                
                # Hebbian Öğrenme: Birlikte ateşlenenlerin bağı güçlenir
                if G.nodes[komsu]['voltaj'] > -50:
                    G[node][komsu]['weight'] = min(2.0, G[node][komsu]['weight'] + 0.2)
    
    # C) İNHİBİSYON (Sıfırlama)
    for node in ateslenenler:
        G.nodes[node]['voltaj'] = -70.0
        
    return ateslenenler

# 3. Streamlit Arayüzü
if st.button("Sinyal Gönder (Düşünceyi Tetikle)"):
    ateslenenler = simule_et(G)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        pos = nx.spring_layout(G)
        
        # Kenar kalınlıklarını öğrenme durumuna göre ayarla
        weights = [G[u][v]['weight'] * 2 for u, v in G.edges()]
        
        # Ağı çiz
        nx.draw(G, pos, width=weights, node_size=60, node_color='#a0cbe2', edge_color='gray', alpha=0.5)
        # Ateşlenenleri kırmızıyla çiz
        nx.draw_networkx_nodes(G, pos, nodelist=ateslenenler, node_color='red', node_size=150)
        
        st.pyplot(fig)
        
    with col2:
        st.write("### Beyin Durumu")
        st.metric("Toplam Nöron", len(G.nodes()))
        st.metric("Ateşlenen Nöron", len(ateslenenler))
        ogrenilen = sum(1 for u, v in G.edges() if G[u][v]['weight'] > 0.5)
        st.metric("Güçlü Bağlantı (Hafıza)", ogrenilen)
        st.info("Kırmızı noktalar 'düşünce' sinyalinin ağ içindeki yayılımıdır.")
else:
    st.write("Simülasyon hazır. Butona basarak ağın 'öğrenme' sürecini izle.")

if st.button("Ağı Sıfırla"):
    del st.session_state.G
    st.rerun()
