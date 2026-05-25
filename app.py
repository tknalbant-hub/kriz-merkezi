import streamlit as st
import os
import shutil
from ai_engine import AIEngine
from backup_system import take_backup

# --- SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="Otonom Dijital Varlık", layout="wide")

# --- EVRİM FONKSİYONU ---
def evrimles(yeni_kod):
    """Ajanın kendi kod tabanını genişletmesi."""
    # 1. Güvenlik: Kod değişmeden önce yedek al
    take_backup("app.py")
    
    # 2. Kod tabanına yeni zekayı/özelliği ekle
    with open("app.py", "a") as f:
        f.write(f"\n\n# --- OTONOM EVRİM: {st.session_state.get('hedef', 'GENEL')} ---\n{yeni_kod}")

# --- ARAYÜZ (FRONTEND) ---
st.title("🧠 Otonom Dijital Varlık: Evrim Modu")

# Sistem Durum Kontrolü
if "GEMINI_API_KEY" not in st.secrets:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets ayarlarını kontrol edin.")
    st.stop()

# Kontrol Paneli
hedef = st.text_input("Ajanın üzerinde çalışmasını istediğin yeni özellik/kod:")
st.session_state['hedef'] = hedef

if st.button("Sistemi Evrimleştir (Self-Evolution)"):
    with st.spinner("Ajan Google Gemini ile düşünüyor ve kendini güncelliyor..."):
        try:
            # 1. Zeka Motorunu Başlat
            ai = AIEngine()
            
            # 2. Kod üret
            yeni_kod = ai.generate_logic(hedef)
            
            # 3. Kodu sisteme işle
            evrimles(yeni_kod)
            
            st.success("Evrim tamamlandı! Sistem güncellendi.")
            st.code(yeni_kod, language="python")
            st.info("Değişikliklerin aktif olması için lütfen sayfayı yenile (Reboot).")
            
        except Exception as e:
            st.error(f"Evrim sırasında hata oluştu: {e}")
            st.warning("Sistem güvenli yedeğe geri döndürülmeye hazır.")

# Hafıza / Log Görüntüleyici
st.subheader("Sistem Logları")
if os.path.exists("varlik.log"):
    with open("varlik.log", "r") as f:
        st.text(f.read())
