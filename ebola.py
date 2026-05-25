import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Sayfa Ayarları
st.set_page_config(page_title="Dijital Beyin Simülasyonu", layout="wide")
st.title("🧠 İnsan Beyni Simülasyon Motoru (Beta)")
st.sidebar.header("Simülasyon Ayarları")

# 1. Nöral Ağ Kurulumu
def ag_kur(n_noron):
    G = nx.erdos_renyi_graph(n_noron, 0.05) # Rastgele bağlantılı nöral ağ
    for node in G.nodes():
        G.nodes[node]['voltaj'] = np.random.uniform(-70, -50)
    return G

# Sidebar kontrolleri
n = st.sidebar.slider("Nöron Sayısı", 50, 500, 100)
G = ag_kur(n)

# 2. Simülasyon Motoru
def simule_et(G):
    ateslenenler = []
    for node in G.nodes():
        # Eşik değeri -55mV (Biyolojik gerçeklik)
        if G.nodes[node]['voltaj'] > -55:
            ateslenenler.append(node)
            # Ateşlenen nöron komşularını etkiler
            for komsu in G.neighbors(node):
                G.nodes[komsu]['voltaj'] += 5 
    return ateslenenler

# 3. Görselleştirme
if st.button("Düşünce Sinyali Gönder"):
    ateslenenler = simule_et(G)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("### Nöral Ağ Aktivitesi")
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, node_size=50, node_color='blue', alpha=0.6)
        nx.draw_networkx_nodes(G, pos, nodelist=ateslenenler, node_color='red', node_size=100)
        st.pyplot(fig)
        
    with col2:
        st.write("### İstatistikler")
        st.metric("Toplam Nöron", n)
        st.metric("Ateşlenen Nöron", len(ateslenenler))
        st.success("Sinyal ağ boyunca yayıldı.")
else:
    st.info("Simülasyonu başlatmak için butona bas.")
