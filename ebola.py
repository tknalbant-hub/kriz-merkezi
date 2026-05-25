import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🧠 İnsan Beyni Simülasyon Motoru (En Üst Sürüm)")

if 'G' not in st.session_state:
    n = 100
    st.session_state.G = nx.erdos_renyi_graph(n, 0.1)
    for u, v in st.session_state.G.edges(): st.session_state.G[u][v]['w'] = 1.0
    for node in st.session_state.G.nodes(): st.session_state.G.nodes[node]['v'] = 0.0

G = st.session_state.G

def tetikle(G):
    ateslenenler = []
    # Rastgele 20 nöronu patlat
    for i in np.random.choice(list(G.nodes()), 20): G.nodes[i]['v'] = 100.0
    
    for n in G.nodes():
        if G.nodes[n]['v'] > 50:
            ateslenenler.append(n)
            for k in G.neighbors(n):
                G.nodes[k]['v'] += G[n][k]['w'] * 50
                G[n][k]['w'] += 0.5 # Hızlı öğrenme
    
    for n in G.nodes(): G.nodes[n]['v'] = 0.0 # Reset
    return ateslenenler

if st.button("Sinyal Gönder"):
    at = tetikle(G)
    fig, ax = plt.subplots()
    nx.draw(G, pos=nx.spring_layout(G), node_color=['red' if n in at else 'blue' for n in G.nodes()])
    st.pyplot(fig)
    st.write(f"Ateşlenen: {len(at)}")

if st.button("Sıfırla"):
    del st.session_state.G
    st.rerun()
