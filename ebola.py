import streamlit as st
import pandas as pd
import numpy as np
from scipy.integrate import odeint

st.set_page_config(page_title="5A48K V4.0 UNIVERSAL", layout="wide")
st.title("🌐 5A48K GLOBAL CRISIS OBSERVATORY v4.0")

# 1. EVRENSEL VERİ YÖNETİCİSİ
@st.cache_data(ttl=3600)
def get_pathogen_data(p_type):
    # Farklı patojenler için simüle edilmiş veya gerçek veri kaynakları
    data_map = {
        "Ebola": [100, 200, 350, 620],
        "COVID-19": [50000, 52000, 55000, 60000],
        "Mpox": [5, 12, 28, 45],
        "Grip (Influenza)": [1000, 1100, 1250, 1500],
        "Marburg": [1, 2, 2, 4]
    }
    vals = data_map.get(p_type, [0, 0, 0, 1])
    return pd.DataFrame({'Value': vals})

# 2. SEÇİM PANELİ
p_type = st.sidebar.selectbox("Patojen Seçimi", ["Ebola", "COVID-19", "Mpox", "Grip (Influenza)", "Marburg"])
df = get_pathogen_data(p_type)
current_val = float(df['Value'].iloc[-1])
prev_val = float(df['Value'].iloc[-2])

# 3. İLERİ ANALİZ (SIR MODELİ)
N = 1000000
beta, gamma = 0.4, 0.15 # Patojen türüne göre bu katsayılar optimize edilebilir
t = np.linspace(0, 30, 30)
res = odeint(lambda y, t: [-beta*y[0]*y[1]/N, beta*y[0]*y[1]/N - gamma*y[1], gamma*y[1]], 
             [N-current_val, current_val, 0], t)

# 4. DİNAMİK DASHBOARD
col1, col2, col3 = st.columns(3)
col1.metric("GÜNCEL VAKA", f"{int(current_val):,}")
growth = ((current_val - prev_val) / (prev_val + 0.1)) * 100
col2.metric("ARTIŞ HIZI", f"%{growth:.1f}")
prob = min(100, (current_val / 2000) * (1 + growth/100))
col3.metric("RİSK SKORU", f"{prob:.1f}/100")

st.subheader(f"🚀 {p_type} İçin 30 Günlük Projeksiyon")
st.area_chart(res[:, 1])

if prob > 50:
    st.error("!!! PROTOKOL: DARK WINTER AKTİF !!!")
elif prob > 20:
    st.warning("DİKKAT: YÜKSEK İZLEME")
else:
    st.success("SİSTEM STABİL")
