import streamlit as st
import numpy as np
import random
import smtplib
from email.message import EmailMessage
from datetime import datetime

# --- AYARLAR ---
G_MAIL = "tknalbant@gmail.com"
# Şifreyi koda yazma! Streamlit Cloud 'Secrets' kısmına ekleyeceğiz.
G_PASSWORD = st.secrets["G_PASSWORD"]

# --- E-POSTA MOTORU ---
def send_email(risk, vaka):
    msg = EmailMessage()
    msg.set_content(f"!!! KRİTİK ALARM !!!\nRisk Skoru: {risk}/100\nGüncel Vaka: {vaka}\n\n'Dark Winter' protokolü aktif.")
    msg['Subject'] = "🚨 5a48k KRİZ MERKEZİ - ACİL BİLDİRİM"
    msg['From'] = G_MAIL
    msg['To'] = G_MAIL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(G_MAIL, G_PASSWORD)
        smtp.send_message(msg)

# --- WEB SİTESİ ARAYÜZÜ ---
st.set_page_config(page_title="5a48k OTONOM KRİZ", layout="wide")
st.title("🛡️ 5a48k GLOBAL KRİZ VE HAYATTA KALMA MERKEZİ")

# --- VERİ VE SİMÜLASYON ---
vaka = 620
lojistik = random.randint(50, 99)
panik = random.randint(40, 95)
risk = (vaka * 0.05) + (lojistik * 0.4) + (panik * 0.3)
risk = min(risk, 100)

# --- PANEL ---
col1, col2, col3 = st.columns(3)
col1.metric("GENEL RİSK", f"{risk:.1f}/100")
col2.metric("HASTANE YÜKÜ", f"%{lojistik}")
col3.metric("SOSYAL PANİK", f"%{panik}")

# --- PROTOKOLLER VE OTOMATİK E-POSTA ---
if risk > 70:
    st.error("!!! PROTOKOL: 'DARK WINTER' DEVREDE !!!")
    
    # Sayfa yenilendiğinde tekrar mail atmasın diye kontrol
    if 'mail_sent' not in st.session_state:
        try:
            send_email(risk, vaka)
            st.session_state.mail_sent = True
            st.success("Uyarı: Otomatik e-posta gönderildi.")
        except Exception as e:
            st.error(f"E-posta gönderim hatası: {e}")
    
    st.markdown("""
    * **Lojistik:** Yerel tedarik zincirleri kontrol altında.
    * **Biyolojik:** Mutasyon takibi aktif.
    * **Savunma:** Maksimum izolasyon seviyesi.
    """)
else:
    st.success("Sistem beklemede: 'Green Zone' aktif.")

st.line_chart([150, 200, 350, 620, vaka])
st.info(f"Son Güncelleme: {datetime.now().strftime('%H:%M:%S')} | Otonom Mod: AKTİF")