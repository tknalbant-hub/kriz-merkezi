import streamlit as st
import pandas as pd
import requests
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="5a48k GÖZLEMEVİ", layout="wide")
st.title("🌐 5a48k GLOBAL EPİDEMİYOLOJİK TAKİP")

# E-posta gönderme fonksiyonu
def send_alert(risk):
    msg = EmailMessage()
    msg.set_content(f"DİKKAT! Risk seviyesi {risk} üzerine çıktı. Protokol 'Dark Winter' devrede.")
    msg['Subject'] = "🚨 KRİZ MERKEZİ ACİL BİLDİRİM"
    msg['From'] = "senin-mailin@gmail.com"
    msg['To'] = "senin-mailin@gmail.com"
    
    password = st.secrets["G_PASSWORD"]
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("senin-mailin@gmail.com", password)
            smtp.send_message(msg)
        return True
    except:
        return False

# Veri çekme ve Risk Hesaplama
risk_skoru = 80.2 # Test için sabit, sonra canlı veriye bağlayacağız

st.metric("CANLI RİSK İNDEKSİ", f"{risk_skoru:.2f}/100")

if risk_skoru > 70:
    st.error("!!! PROTOKOL: 'DARK WINTER' DEVREDE !!!")
    if st.button("Acil Durum Bildirimi Gönder"):
        if send_alert(risk_skoru):
            st.success("Uyarı maili başarıyla gönderildi!")
        else:
            st.error("Mail gönderilemedi, uygulama şifresini kontrol et.")
