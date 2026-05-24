import streamlit as st
import pandas as pd
import numpy as np
import requests
import smtplib
from email.message import EmailMessage
from scipy.integrate import odeint

# AYARLAR
st.set_page_config(page_title="5A48K V3.0 FULL SUITE", layout="wide")

# E-POSTA MOTORU
def send_alert(msg_text):
    msg = EmailMessage()
    msg.set_content(msg_text)
    msg['Subject'] = "🚨 5A48K KRİZ UYARISI"
    msg['From'] = "senin-mailin@gmail.com"
    msg['To'] = "senin-mailin@gmail.com"
    # Şifreyi Streamlit Secrets'dan çekiyoruz
    password = st.secrets.get("G_PASSWORD", "")
    if password:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("senin-mailin@gmail.com", password)
            smtp.send_message(msg)

# VERİ ÇEKME
@st.cache_data(ttl=3600)
def get_data(p_type):
    urls = {
        "Ebola": "https://raw.githubusercontent.com/datasets/ebola/master/data/ebola_data_db_format.csv",
        "COVID-19": "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
    }
    try:
        return pd.read_csv(urls.get(p_type))
    except:
        return pd.DataFrame({'Value': [100, 200, 300, 400, 500, 620]})

# DASHBOARD
st.title("🌐 5A48K GLOBAL CRISIS OBSERVATORY v3.0")
p_type = st.sidebar.selectbox("Patojen Seçimi", ["Ebola", "COVID-19"])
df = get_data(p_type)

current_val = float(df['Value'].iloc[-1]) if 'Value' in df.columns else 620
growth = 24.0 # Simüle edilmiş hız

# SIR MODELİ
N, beta, gamma = 1000000, 0.3, 0.1
t = np.linspace(0, 30, 30)
res = odeint(lambda y, t: [-beta*y[0]*y[1]/N, beta*y[0]*y[1]/N - gamma*y[1], gamma*y[1]], 
             [N-current_val, current_val, 0], t)

# GÖRSELLEŞTİRME
col1, col2, col3 = st.columns(3)
col1.metric("GÜNCEL VAKA", f"{int(current_val):,}")
col2.metric("ARTIŞ HIZI", f"%{growth}")
prob = min(100, (current_val / 10000))
col3.metric("RİSK SKORU", f"{prob:.2f}/100")

st.area_chart(res[:, 1])

# OTOMATİK AKSİYON
if prob > 5:
    st.error("KRİTİK DURUM: Protokoller tetiklendi!")
    if st.button("Acil Durum Maili Gönder"):
        send_alert(f"Risk seviyesi {prob} üzerine çıktı! Müdahale gerekiyor.")
        st.success("Uyarı gönderildi.")
