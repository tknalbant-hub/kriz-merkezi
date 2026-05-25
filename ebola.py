import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("🧠 İnsan Beyni: Tam Ölçekli Otonom Simülasyon")

if 'G' not in st.session_state:
    G = nx.erdos_renyi_graph(80, 0.05)
    for n in G.nodes(): 
        G.nodes[n]['v'] = 0.0      # Voltaj
        G.nodes[n]['threshold'] = 20.0 # Bireysel eşik
    for u, v in G.edges(): 
        G[u][v]['w'] = 0.1         # Bağlantı gücü
    st.session_state.G = G

G = st.session_state.G

def otonom_beyin(G):
    # 1. RASTGELE DÜŞÜNCE (Dış etki)
    if np.random.rand() > 0.3:
        target = np.random.choice(list(G.nodes()))
        G.nodes[target]['v'] += 50.0
    
    ateslenenler = []
    # 2. ATEŞLEME & İNHİBİSYON
    for n in G.nodes():
        if G.nodes[n]['v'] > G.nodes[n]['threshold']:
            ateslenenler.append(n)
            # İnhibisyon: Ateşlenen nöron etrafı "susturur" (denge)
            for komsu in G.neighbors(n):
                G.nodes[komsu]['v'] += (G[n][komsu]['w'] * 30.0)
                # ÖĞRENME: Dopamin etkisi (Ateşlenen yollar güçlenir)
                G[n][komsu]['w'] = min(4.0, G[n][komsu]['w'] + 0.3)
        else:
            # UNUTMA: Kullanılmayan yollar zamanla zayıflar
            for komsu in G.neighbors(n):
                G[n][komsu]['w'] = max(0.01, G[n][komsu]['w'] - 0.01)
                
    # 3. VOLTAJ SIFIRLAMA
    for n in G.nodes(): G.nodes[n]['v'] = max(0, G.nodes[n]['v'] - 5.0)
    return ateslenenler

# Arayüz
col1, col2 = st.columns([3, 1])

with col1:
    if st.checkbox("Bilinci Başlat"):
        at = otonom_beyin(G)
        weights = [G[u][v]['w'] for u, v in G.edges()]
        colors = ['red' if w > 1.5 else 'black' for w in weights]
        
        fig, ax = plt.subplots(figsize=(8,6))
        nx.draw(G, pos=nx.spring_layout(G), node_color=['red' if n in at else 'blue' for n in G.nodes()], 
                edge_color=colors, width=weights, node_size=50)
        st.pyplot(fig)
        time.sleep(0.3)
        st.rerun()

with col2:
    st.write("### Beyin Durumu")
    st.metric("Kalıcı Hafıza (Güçlü Bağlantı)", sum(1 for u, v in G.edges() if G[u][v]['w'] > 1.5))
    st.write("---")
    st.write("**Biyolojik Kurallar:**")
    st.write("• **Hebbian Öğrenme:** Birlikte ateşlenenler bağlanır.")
    st.write("• **Sinaptik Budama:** Kullanılmayan yollar silinir (Unutma).")
    st.write("• **Homeostaz:** Nöronlar dinlenmeye çalışır.")

if st.button("Beyni Sıfırla"):
    del st.session_state.G
    st.rerun()
