import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

st.title("🧠 İnsan Beyni Simülasyon Motoru")

if 'G' not in st.session_state:
    G = nx.erdos_renyi_graph(100, 0.1)
    # Tüm düğüm ve kenar verilerini hatasız tanımla
    for n in G.nodes(): G.nodes[n]['v'] = 0.0
    for u, v in G.edges(): G[u][v]['w'] = 1.0
    st.session_state.G = G

G = st.session_state.G

def tetikle(G):
    ateslenenler = []
    # Rastgele tetikle
    for i in np.random.choice(list(G.nodes()), 20): G.nodes[i]['v'] = 100.0
    
    for n in G.nodes():
        if G.nodes[n].get('v', 0) > 50:
            ateslenenler.append(n)
            for k in G.neighbors(n):
                # Önce değerin varlığını kontrol et
                G.nodes[k]['v'] = G.nodes[k].get('v', 0) + (G[n][k].get('w', 1) * 50)
                G[n][k]['w'] = G[n][k].get('w', 1) + 0.5
    
    for n in G.nodes(): G.nodes[n]['v'] = 0.0
    return ateslenenler

if st.button("Sinyal Gönder"):
    at = tetikle(G)
    fig, ax = plt.subplots()
    colors = ['red' if n in at else 'blue' for n in G.nodes()]
    nx.draw(G, pos=nx.spring_layout(G), node_color=colors, node_size=50)
    st.pyplot(fig)
    st.write(f"Ateşlenen: {len(at)}")

if st.button("Sıfırla"):
    del st.session_state.G
    st.rerun()
